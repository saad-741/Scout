import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON
from app.core.db import Base


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)

    work_type = Column(String(50), nullable=False, index=True)
    employment_type = Column(String(50), nullable=False, index=True)
    experience_level = Column(String(50), nullable=False, index=True)

    min_years_exp = Column(Integer, nullable=True)
    max_years_exp = Column(Integer, nullable=True)

    # Store skills arrays natively as JSON
    required_skills = Column(JSON, nullable=False, default=list)
    nice_to_have_skills = Column(JSON, nullable=False, default=list)

    summary = Column(Text, nullable=True)
    raw_description = Column(Text, nullable=False)

    # Salary specifics
    salary_currency = Column(String(10), nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_period = Column(String(20), nullable=True)

    # Provenance tracking
    source = Column(String(100), nullable=False, index=True)
    source_url = Column(Text, nullable=False, unique=True)
    posted_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
