from enum import Enum


class WorkType(str, Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ON_SITE = "On-site"


class EmploymentType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"


class ExperienceLevel(str, Enum):
    INTERNSHIP = "Internship"
    ENTRY_LEVEL = "Entry Level"
    ASSOCIATE = "Associate"
    MID_SENIOR = "Mid-Senior"
    DIRECTOR = "Director"
    EXECUTIVE = "Executive"
    NOT_SPECIFIED = "Not Specified"


class SalaryPeriod(str, Enum):
    HOURLY = "Hourly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"