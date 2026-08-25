import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.ai.engine import GeminiAIEngine
from app.cleaners.deduplicator import JobDeduplicator
from app.extractors.base import JobExtractor
from app.models.job import JobModel
from app.providers.base import JobProvider
from app.providers.jsearch import JSearchProvider
from app.repositories.job_repository import JobRepository
from app.schemas.job import BasicJobData, JobSearchRequest, RawJobListing

logger = logging.getLogger(__name__)


def get_job_provider() -> JobProvider:
    return JSearchProvider()


class JobService:

    def __init__(self, db: Session, provider: Optional[JobProvider] = None):
        self.db = db
        self.provider = provider or get_job_provider()
        self.extractor = JobExtractor()
        self.deduplicator = JobDeduplicator()
        self.ai_engine = GeminiAIEngine()
        self.repository = JobRepository(db)

    def get_job_details(self, job_id: str) -> Optional[JobModel]:
        """Retrieves cached job details from the database without invoking AI."""
        return self.repository.get_job_by_id(job_id)

    async def execute_search(self, req: JobSearchRequest) -> List[JobModel]:
        """
        Complete Pipeline:
        1. Check DB cache first (unless force_refresh is True).
        2. If cache hit, return immediately.
        3. If cache miss, execute full Ingestion -> AI Analysis -> DB Save.
        """
        if not req.force_refresh:
            cached_jobs = self.repository.search_stored_jobs(req)
            if cached_jobs:
                logger.info(
                    f"Cache HIT: Returning {len(cached_jobs)} cached jobs for '{req.role}' in '{req.location}'."
                )
                return cached_jobs

        logger.info(
            f"Cache MISS/REFRESH: Executing search pipeline for '{req.role}' in '{req.location}'."
        )

        # 1. Fetch raw listings from provider
        is_remote = (
            any(wt.name == "REMOTE" for wt in req.work_types)
            if req.work_types
            else False
        )
        raw_listings: List[RawJobListing] = await self.provider.search_jobs(
            query=req.role,
            location=req.location,
            remote_only=is_remote,
        )

        # 2. Extract & Normalize text
        cleaned_jobs: List[BasicJobData] = [
            self.extractor.extract(raw) for raw in raw_listings
        ]

        # 3. Deduplicate listings
        unique_jobs: List[BasicJobData] = self.deduplicator.deduplicate(cleaned_jobs)

        if not unique_jobs:
            return []

###########
        unique_jobs = unique_jobs[:5]

        # 4. AI Processing in ONE single Gemini Call
        job_tuples = [(job.title, job.description) for job in unique_jobs]
        ai_analyses = await self.ai_engine.analyze_jobs_in_single_call(job_tuples)

        # 5. DB Persistence
        for job, analysis in zip(unique_jobs, ai_analyses):
            self.repository.save_or_update_analyzed_job(
                job_data=job, ai_analysis=analysis
            )

        # 6. Apply final SQL filter against newly processed jobs
        return self.repository.search_stored_jobs(req)

 