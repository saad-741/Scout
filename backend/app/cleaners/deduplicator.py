import hashlib
from typing import Dict, List
from app.schemas.job import BasicJobData


class JobDeduplicator:
    """Identifies and eliminates duplicate job listings across providers using signature hashing."""

    @staticmethod
    def generate_signature(job: BasicJobData) -> str:
        """Creates a unique hash fingerprint from normalized core fields."""
        norm_company = job.company.lower().strip()
        norm_title = job.title.lower().strip()
        norm_location = job.location.lower().strip()
        
        # Clean URL to ignore trailing slashes or tracking query params
        norm_url = job.url.split("?")[0].rstrip("/").lower()

        raw_fingerprint = f"{norm_company}|{norm_title}|{norm_location}|{norm_url}"
        return hashlib.md5(raw_fingerprint.encode("utf-8")).hexdigest()

    def deduplicate(self, jobs: List[BasicJobData]) -> List[BasicJobData]:
        """Filters out duplicate listings, preserving the first instance received."""
        seen_signatures: Dict[str, BasicJobData] = {}
        unique_jobs: List[BasicJobData] = []

        for job in jobs:
            signature = self.generate_signature(job)
            if signature not in seen_signatures:
                seen_signatures[signature] = job
                unique_jobs.append(job)

        return unique_jobs