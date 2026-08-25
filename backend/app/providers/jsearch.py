import logging
from typing import List, Optional
import httpx
from app.core.config import settings
from app.providers.base import JobProvider
from app.schemas.job import RawJobListing

logger = logging.getLogger(__name__)


class JSearchProvider(JobProvider):
    """Real Job Data Provider backed by RapidAPI JSearch."""

    def __init__(self):
        self.api_key = getattr(settings, "RAPIDAPI_KEY", "").strip()
        self.host = "jsearch.p.rapidapi.com"
        self.base_url = "https://jsearch.p.rapidapi.com/search-v2"

    @property
    def provider_name(self) -> str:
        return "jsearch_rapidapi"

    async def search_jobs(
        self,
        query: str,
        location: str,
        page: int = 1,
        num_pages: int = 1,
        employment_types: Optional[List[str]] = None,
        remote_only: bool = False,
    ) -> List[RawJobListing]:
        if not self.api_key or self.api_key == "your_rapidapi_key_here":
            logger.warning(
                "RAPIDAPI_KEY not configured or set to placeholder. Falling back to empty response."
            )
            return []

        search_query = f"{query} in {location}".strip()
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host,
        }
        params = {
            "query": search_query,
            "page": str(page),
            "num_pages": str(num_pages),
            "date_posted": "all",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.get(
                    self.base_url, headers=headers, params=params
                )
                response.raise_for_status()
                data = response.json()

                # Print raw structure to Uvicorn terminal for immediate verification
                logger.info(
                    f"JSearch Raw Response Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
                )

                # Safely extract job objects array across both /search and /search-v2 structure variations
                raw_data = data.get("data", [])
                if isinstance(raw_data, dict):
                    raw_items = raw_data.get("jobs", raw_data.get("results", []))
                elif isinstance(raw_data, list):
                    raw_items = raw_data
                else:
                    raw_items = []

                listings: List[RawJobListing] = []
                for item in raw_items:
                    if not isinstance(item, dict):
                        continue

                    # Fallbacks for field names across API revisions
                    job_id = str(item.get("job_id") or item.get("id") or "")
                    publisher = str(
                        item.get("job_publisher") or item.get("publisher") or "JSearch"
                    )
                    title = str(
                        item.get("job_title") or item.get("title") or "Unknown Title"
                    )
                    company = str(
                        item.get("employer_name")
                        or item.get("company_name")
                        or "Unknown Company"
                    )
                    city = item.get("job_city") or item.get("city") or ""
                    country = item.get("job_country") or item.get("country") or ""
                    description = str(
                        item.get("job_description") or item.get("description") or ""
                    )
                    link = str(
                        item.get("job_apply_link")
                        or item.get("job_google_link")
                        or item.get("url")
                        or ""
                    )
                    posted_at = str(
                        item.get("job_posted_at_datetime_utc")
                        or item.get("posted_at")
                        or ""
                    )

                    listings.append(
                        RawJobListing(
                            raw_id=job_id,
                            source_name=publisher,
                            title=title,
                            company_name=company,
                            location_raw=f"{city}, {country}".strip(", "),
                            description_raw=description,
                            url=link,
                            posted_at_raw=posted_at,
                        )
                    )

                logger.info(f"Successfully extracted {len(listings)} job listings.")
                return listings

            except httpx.HTTPStatusError as err:
                logger.error(
                    f"JSearch API returned HTTP Status {err.response.status_code}: {err.response.text}"
                )
                return []
            except httpx.HTTPError as err:
                logger.error(f"Network error while reaching JSearch API: {err}")
                return []




 