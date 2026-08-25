import re
from datetime import datetime, timezone
from typing import Optional, Tuple
from app.enums import SalaryPeriod
from app.schemas.job import BasicJobData, RawJobListing
from app.cleaners.normalizer import DataNormalizer


class JobExtractor:
    """Deterministic extractor converting raw provider data to Scout BasicJobData."""

    def __init__(self):
        self.normalizer = DataNormalizer()

    @staticmethod
    def parse_posted_date(date_str: Optional[str]) -> datetime:
        if not date_str:
            return datetime.now(timezone.utc)
        try:
            clean_date = date_str.replace("Z", "+00:00")
            return datetime.fromisoformat(clean_date)
        except (ValueError, TypeError):
            return datetime.now(timezone.utc)

    def extract_salary(
        self,
        text: str,
        raw_min: Optional[float] = None,
        raw_max: Optional[float] = None,
        raw_curr: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[float], Optional[float], Optional[SalaryPeriod]]:
        if raw_min or raw_max:
            return raw_curr or "PKR", raw_min, raw_max, SalaryPeriod.MONTHLY

        pkr_match = re.search(
            r"pkr\s*([\d,]+)\s*k?\s*[-–\sto]+\s*([\d,]+)\s*k?", text, re.IGNORECASE
        )
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

    def extract(self, raw: RawJobListing) -> BasicJobData:
        clean_title = self.normalizer.clean_text(raw.title)
        clean_company = self.normalizer.clean_text(raw.company_name)
        clean_desc = self.normalizer.clean_text(raw.description_raw)

        full_text = f"{clean_title} {clean_desc}"

        location = self.normalizer.normalize_location(raw.location_raw)
        work_type = self.normalizer.normalize_work_type(raw.raw_work_mode, full_text)
        employment_type = self.normalizer.normalize_employment_type(
            raw.raw_employment_type, full_text
        )
        salary_currency, salary_min, salary_max, salary_period = self.extract_salary(
            full_text, raw.raw_salary_min, raw.raw_salary_max, raw.raw_salary_currency
        )

        return BasicJobData(
            title=clean_title,
            company=clean_company,
            location=location,
            description=clean_desc,
            url=raw.url,
            source=raw.source_name,
            posted_at=self.parse_posted_date(raw.posted_at_raw),
            employment_type=employment_type,
            work_type=work_type,
            salary_currency=salary_currency,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_period=salary_period,
        )
