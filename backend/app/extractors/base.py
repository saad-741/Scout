import re
from datetime import datetime, timezone
from typing import Optional, Tuple
from app.enums import EmploymentType, SalaryPeriod, WorkType
from app.schemas.job import BasicJobData, RawJobListing


class JobExtractor:
    """Deterministic extractor converting raw provider data to Scout BasicJobData."""

    @staticmethod
    def extract_work_type(text: str, explicit_mode: Optional[str] = None) -> WorkType:
        combined = f"{explicit_mode or ''} {text}".lower()
        if "remote" in combined or "work from home" in combined or "wfh" in combined:
            return WorkType.REMOTE
        if "hybrid" in combined:
            return WorkType.HYBRID
        return WorkType.ON_SITE

    @staticmethod
    def extract_employment_type(text: str, explicit_type: Optional[str] = None) -> EmploymentType:
        combined = f"{explicit_type or ''} {text}".lower()
        if "part-time" in combined or "part time" in combined:
            return EmploymentType.PART_TIME
        if "contract" in combined or "freelance" in combined or "temporary" in combined:
            return EmploymentType.CONTRACT
        if "internship" in combined or "intern" in combined:
            return EmploymentType.INTERNSHIP
        return EmploymentType.FULL_TIME

    @staticmethod
    def extract_salary(
        text: str,
        raw_min: Optional[float] = None,
        raw_max: Optional[float] = None,
        raw_curr: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[float], Optional[float], Optional[SalaryPeriod]]:
        if raw_min or raw_max:
            return raw_curr or "PKR", raw_min, raw_max, SalaryPeriod.MONTHLY

        # Regex pattern matching PKR / USD salary ranges (e.g., PKR 100K-150K or $50,000 - $80,000)
        pkr_match = re.search(r"pkr\s*([\d,]+)\s*k?\s*[-–\sto]+\s*([\d,]+)\s*k?", text, re.IGNORECASE)
        if pkr_match:
            try:
                min_val = float(pkr_match.group(1).replace(",", ""))
                max_val = float(pkr_match.group(2).replace(",", ""))
                if min_val < 1000:
                    min_val *= 1000
                if max_val < 1000:
                    max_val *= 1000
                return "PKR", min_val, max_val, SalaryPeriod.MONTHLY
            except ValueError:
                pass

        return None, None, None, None

    @staticmethod
    def parse_posted_date(date_str: Optional[str]) -> datetime:
        if not date_str:
            return datetime.now(timezone.utc)
        try:
            # ISO format handling
            clean_date = date_str.replace("Z", "+00:00")
            return datetime.fromisoformat(clean_date)
        except (ValueError, TypeError):
            return datetime.now(timezone.utc)

    def extract(self, raw: RawJobListing) -> BasicJobData:
        full_text = f"{raw.title} {raw.description_raw}"
        
        work_type = self.extract_work_type(full_text, raw.raw_work_mode)
        employment_type = self.extract_employment_type(full_text, raw.raw_employment_type)
        curr, s_min, s_max, s_period = self.extract_salary(
            full_text, raw.raw_salary_min, raw.raw_salary_max, raw.raw_salary_currency
        )
        posted_at = self.parse_posted_date(raw.posted_at_raw)

        return BasicJobData(
            title=raw.title.strip(),
            company=raw.company_name.strip(),
            location=raw.location_raw.strip() if raw.location_raw else "Lahore, Pakistan",
            description=raw.description_raw.strip(),
            url=raw.url,
            source=raw.source_name,
            posted_at=posted_at,
            employment_type=employment_type,
            work_type=work_type,
            salary_currency=curr,
            salary_min=s_min,
            salary_max=s_max,
            salary_period=s_period,
        )