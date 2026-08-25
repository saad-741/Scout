from typing import List, Optional
from app.extractors.base import JobExtractor
from app.providers.base import JobProvider
from app.providers.jsearch import JSearchProvider
# from app.providers.mock import MockJobProvider
from app.schemas.job import BasicJobData, RawJobListing


# def get_job_provider() -> JobProvider:
#     from app.core.config import settings
#     if getattr(settings, "RAPIDAPI_KEY", ""):
#         return JSearchProvider()
#     return MockJobProvider()
def get_job_provider() -> JobProvider:
    """Always return the live JSearch Provider."""
    return JSearchProvider()

class JobService:
    def __init__(self, provider: Optional[JobProvider] = None):
        self.provider = provider or get_job_provider()
        self.extractor = JobExtractor()

    async def fetch_and_extract_jobs(
        self, role: str, location: str, remote_only: bool = False
    ) -> List[BasicJobData]:
        raw_listings: List[RawJobListing] = await self.provider.search_jobs(
            query=role, location=location, remote_only=remote_only
        )
        return [self.extractor.extract(raw) for raw in raw_listings]

 