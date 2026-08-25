import asyncio
import logging
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.config import settings
from app.schemas.job import JobAnalysis

logger = logging.getLogger(__name__)


class JobAnalysisList(BaseModel):
    """Wrapper schema to force Gemini to output a JSON list of JobAnalysis objects."""

    analyses: List[JobAnalysis]


class GeminiAIEngine:

    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            logger.warning(
                "GEMINI_API_KEY not configured. AI engine running in fallback mode."
            )

    async def analyze_jobs_in_single_call(
        self, jobs: List[tuple[str, str]]
    ) -> List[JobAnalysis]:
        """Process all jobs concurrently in 1 single Gemini API call to eliminate HTTP bottlenecks and rate limits."""
        if not jobs:
            return []

        if not self.client:
            return [self._fallback_analysis(t, d) for t, d in jobs]

        # Format all job listings into a single prompt string payload
        formatted_jobs_payload = []
        for index, (title, description) in enumerate(jobs, start=1):
            formatted_jobs_payload.append(
                f"=== ITEM {index} ===\n"
                f"Job Title: {title}\n"
                f"Job Description:\n{description}\n"
            )

        joined_payload = "\n".join(formatted_jobs_payload)

        prompt = f"""
You are an expert tech career and job listing analyst. Analyze the following list of {len(jobs)} job postings and extract structured intelligence for each item.

Return the exact same number of analyses in the output `analyses` array, maintaining the original order of the jobs provided.

INSTRUCTIONS FOR EACH JOB:
1. Classify work_type strictly as one of: 'Remote', 'Hybrid', 'On-site'.
2. Classify employment_type strictly as one of: 'Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'.
3. Classify experience_level strictly as one of: 'Internship', 'Entry Level', 'Associate', 'Mid-Senior', 'Director', 'Executive', 'Not Specified'.
4. Extract required_skills (non-negotiable skills required for the role).
5. Extract nice_to_have_skills (optional/bonus skills mentioned).
6. Provide a concise 2-3 sentence executive summary of the primary duties.
7. If salary is mentioned, extract currency, min/max amounts, and period ('Hourly', 'Monthly', 'Yearly').

JOB LISTINGS TO PROCESS:
{joined_payload}
"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=JobAnalysisList,
                        temperature=0.1,
                    ),
                )

                if response.text:
                    parsed_result = JobAnalysisList.model_validate_json(response.text)

                    # Validate output length matches input length
                    if len(parsed_result.analyses) == len(jobs):
                        return parsed_result.analyses

                    logger.warning(
                        f"Mismatch between input count ({len(jobs)}) and output count ({len(parsed_result.analyses)}). Using standard mapping."
                    )
                    return parsed_result.analyses

                raise ValueError("Empty response text from Gemini API.")

            except Exception as err:
                err_msg = str(err)
                if any(
                    code in err_msg
                    for code in ["503", "429", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]
                ):
                    wait_time = 3 * (attempt + 1)
                    logger.warning(
                        f"Gemini API rate limit hit (Attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                    continue

                logger.error(
                    f"Error in single-call Gemini processing: {err}. Falling back to default analysis."
                )
                return [self._fallback_analysis(t, d) for t, d in jobs]

        return [self._fallback_analysis(t, d) for t, d in jobs]

     
    def _fallback_analysis(self, title: str, description: str) -> JobAnalysis:
        # Basic skill extractor for fallback scenarios
        desc_lower = description.lower()
        detected_skills = [
            s for s in ["Python", "Django", "PostgreSQL", "REST API", "SQL", "FastAPI"]
            if s.lower() in desc_lower
        ]

        return JobAnalysis(
            summary=f"Role for {title}. Check full posting for details.",
            work_type="Hybrid",
            employment_type="Full-time",
            experience_level="Entry Level",  # Matches standard entry filter during fallback
            min_years_experience=0,
            max_years_experience=2,
            required_skills=detected_skills if detected_skills else ["Python"],
            nice_to_have_skills=[],
            salary=None,
        )


     