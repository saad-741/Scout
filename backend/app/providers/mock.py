# from typing import List, Optional
# from app.providers.base import JobProvider
# from app.schemas.job import RawJobListing


# class MockJobProvider(JobProvider):
#     @property
#     def provider_name(self) -> str:
#         return "mock_provider"

#     async def search_jobs(
#         self,
#         query: str,
#         location: str,
#         page: int = 1,
#         num_pages: int = 1,
#         employment_types: Optional[List[str]] = None,
#         remote_only: bool = False,
#     ) -> List[RawJobListing]:
#         return [
#             RawJobListing(
#                 raw_id="mock_101",
#                 source_name="Mock Board",
#                 title=f"Senior {query}",
#                 company_name="ABC Technologies",
#                 location_raw=f"{location}, Pakistan",
#                 description_raw=(
#                     "We are seeking a Backend Developer with 2+ years of experience in Python and FastAPI. "
#                     "Must know PostgreSQL and REST APIs. Experience with Docker and AWS is a plus."
#                 ),
#                 url="https://example.com/jobs/mock_101",
#                 posted_at_raw="2026-08-24T10:00:00Z",
#             ),
#             RawJobListing(
#                 raw_id="mock_102",
#                 source_name="Mock Board",
#                 title=f"Junior {query}",
#                 company_name="Innovate Tech Labs",
#                 location_raw=f"{location}, Pakistan",
#                 description_raw=(
#                     "Looking for an entry-level software engineer proficient in Python and Django. "
#                     "Knowledge of databases and basic Git workflows required."
#                 ),
#                 url="https://example.com/jobs/mock_102",
#                 posted_at_raw="2026-08-23T14:30:00Z",
#             ),
#         ]