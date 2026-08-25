from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.job import RawJobListing


class JobProvider(ABC):
    """Abstract Base Class for all Job Data Providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier for the provider."""
        pass

    @abstractmethod
    async def search_jobs(
        self,
        query: str,
        location: str,
        page: int = 1,
        num_pages: int = 1,
        employment_types: Optional[List[str]] = None,
        remote_only: bool = False,
    ) -> List[RawJobListing]:
        """Fetch raw job listings from the provider matching search criteria."""
        pass