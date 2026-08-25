import re
from typing import Optional, Tuple
from app.enums import EmploymentType, ExperienceLevel, WorkType


class DataNormalizer:
    """Sanitizes messy raw text and converts varied job attributes into standardized Scout formats."""

    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """Strip HTML tags, normalize whitespace, and remove non-standard padding."""
        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean)
        return clean.strip()

    @staticmethod
    def normalize_location(location_raw: Optional[str]) -> str:
        """Converts variations like 'Lahore, Pakistan', 'Lahore PK', ' Lahore ' into 'Lahore'."""
        cleaned = DataNormalizer.clean_text(location_raw)
        if not cleaned:
            return "Lahore"

        city_patterns = [
            (r"\blahore\b", "Lahore"),
            (r"\bkarachi\b", "Karachi"),
            (r"\bislamabad\b", "Islamabad"),
            (r"\brawalpindi\b", "Rawalpindi"),
            (r"\bfaisalabad\b", "Faisalabad"),
        ]

        for pattern, city_name in city_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return city_name

        parts = [p.strip() for p in cleaned.split(",")]
        if parts and parts[0]:
            return parts[0].title()

        return cleaned.title()

    @staticmethod
    def normalize_work_type(raw_mode: Optional[str], full_text: str) -> WorkType:
        """Normalizes variations ('wfh', '100% remote', 'work from home') into WorkType Enums."""
        combined = f"{raw_mode or ''} {full_text}".lower()

        remote_keywords = ["remote", "wfh", "work from home", "100% remote", "telecommute", "distributed"]
        hybrid_keywords = ["hybrid", "partially remote", "flexible location", "2 days office"]

        if any(k in combined for k in remote_keywords):
            return WorkType.REMOTE
        if any(k in combined for k in hybrid_keywords):
            return WorkType.HYBRID

        return WorkType.ON_SITE

    @staticmethod
    def normalize_employment_type(raw_type: Optional[str], full_text: str) -> EmploymentType:
        """Normalizes variations ('ft', 'full time', 'contractor', 'intern') into EmploymentType Enums."""
        combined = f"{raw_type or ''} {full_text}".lower()

        if re.search(r"\b(part[-\s]?time|pt)\b", combined):
            return EmploymentType.PART_TIME
        if re.search(r"\b(temporary|temp)\b", combined):
            return EmploymentType.TEMPORARY
        if re.search(r"\b(contract|contractor|freelance)\b", combined):
            return EmploymentType.CONTRACT
        if re.search(r"\b(intern|internship|trainee)\b", combined):
            return EmploymentType.INTERNSHIP

        return EmploymentType.FULL_TIME

    @staticmethod
    def normalize_experience_level(full_text: str) -> Tuple[ExperienceLevel, int, Optional[int]]:
        """Parses experience keywords and explicit year ranges (e.g., '2-4 years') from job text."""
        text_lower = full_text.lower()

        exp_match = re.search(r"(\d+)\s*[-–to]+\s*(\d+)\s*\+?\s*years?", text_lower)
        if exp_match:
            try:
                min_yrs = int(exp_match.group(1))
                max_yrs = int(exp_match.group(2))
                level = ExperienceLevel.ENTRY_LEVEL if min_yrs <= 2 else ExperienceLevel.MID_SENIOR
                return level, min_yrs, max_yrs
            except ValueError:
                pass

        single_match = re.search(r"(\d+)\+?\s*years?", text_lower)
        if single_match:
            try:
                min_yrs = int(single_match.group(1))
                level = ExperienceLevel.ENTRY_LEVEL if min_yrs <= 2 else ExperienceLevel.MID_SENIOR
                return level, min_yrs, None
            except ValueError:
                pass

        if "intern" in text_lower or "internship" in text_lower:
            return ExperienceLevel.INTERNSHIP, 0, 1
        if "entry level" in text_lower or "junior" in text_lower or "associate" in text_lower:
            return ExperienceLevel.ENTRY_LEVEL, 0, 2
        if "lead" in text_lower or "principal" in text_lower or "director" in text_lower:
            return ExperienceLevel.DIRECTOR, 7, None

        return ExperienceLevel.NOT_SPECIFIED, 0, None
 