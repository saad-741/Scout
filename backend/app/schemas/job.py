from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.enums import EmploymentType, ExperienceLevel, SalaryPeriod, WorkType


# --- 1. Raw Ingestion Model (What external sources give us) ---
class RawJobListing(BaseModel):
    raw_id: str
    source_name: str
    title: str
    company_name: str
    location_raw: Optional[str] = None
    description_raw: str
    url: str
    posted_at_raw: Optional[str] = None
    raw_salary_min: Optional[float] = None
    raw_salary_max: Optional[float] = None
    raw_salary_currency: Optional[str] = None
    raw_employment_type: Optional[str] = None
    raw_work_mode: Optional[str] = None


class BasicJobData(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_at: datetime

    # Deterministically extracted metadata
    employment_type: EmploymentType
    work_type: WorkType

    # Salary extraction
    salary_currency: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_period: Optional[SalaryPeriod] = None

    model_config = ConfigDict(from_attributes=True)


# --- 2. AI Intelligence Model (Structured by LLM) ---
class SalaryInfo(BaseModel):
    currency: Optional[str] = Field(default=None, example="PKR")
    min_amount: Optional[float] = Field(default=None, example=100000.0)
    max_amount: Optional[float] = Field(default=None, example=150000.0)
    period: Optional[SalaryPeriod] = Field(default=None, example=SalaryPeriod.MONTHLY)


class JobAnalysis(BaseModel):
    summary: str = Field(
        description="2-3 sentence concise executive summary of the position."
    )
    work_type: WorkType
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    min_years_experience: Optional[int] = Field(default=0)
    max_years_experience: Optional[int] = Field(default=None)
    required_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    salary: Optional[SalaryInfo] = None


# --- 3. Internal Normalized Scout Job Model ---
class JobBase(BaseModel):
    title: str
    company: str
    location: str
    work_type: WorkType
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    min_years_exp: Optional[int] = 0
    max_years_exp: Optional[int] = None

    required_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)

    summary: Optional[str] = None
    raw_description: str

    salary_currency: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_period: Optional[SalaryPeriod] = None

    source: str
    source_url: str
    posted_at: datetime


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
