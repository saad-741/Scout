from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy import String, or_, func
from sqlalchemy.orm import Session

from app.enums import ExperienceLevel, WorkType
from app.models.job import JobModel
from app.schemas.job import (
    BasicJobData,
    DatePostedFilter,
    JobAnalysis,
    JobSearchRequest,
)


class JobRepository:
    """Handles persistent storage and flexible query filtering for Jobs in Supabase."""

    def __init__(self, db: Session):
        self.db = db
    
    def search_stored_jobs(self, req: JobSearchRequest) -> List[JobModel]:
        """Applies explicit SQL filters matching search criteria."""
        query = self.db.query(JobModel)

        # 1. Fuzzy match title / role
        if req.role:
            query = query.filter(JobModel.title.ilike(f"%{req.role}%"))

        # 2. Location filter
        if req.location:
            query = query.filter(JobModel.location.ilike(f"%{req.location}%"))

        # 3. Work Type filter (extract string value)
        if req.work_types:
            work_modes = [
                w.value if hasattr(w, "value") else str(w) for w in req.work_types
            ]
            query = query.filter(JobModel.work_type.in_(work_modes))

        # 4. Experience Level filter (extract string value)
        if req.experience_levels:
            exp_levels = [
                e.value if hasattr(e, "value") else str(e)
                for e in req.experience_levels
            ]
            query = query.filter(JobModel.experience_level.in_(exp_levels))

        # 5. Date Posted filter
        if req.date_posted and req.date_posted != DatePostedFilter.ANY_TIME:
            now = datetime.now(timezone.utc)
            if req.date_posted == DatePostedFilter.PAST_24H:
                cutoff = now - timedelta(hours=24)
            elif req.date_posted == DatePostedFilter.PAST_WEEK:
                cutoff = now - timedelta(days=7)
            elif req.date_posted == DatePostedFilter.PAST_MONTH:
                cutoff = now - timedelta(days=30)
            else:
                cutoff = None

            if cutoff:
                query = query.filter(JobModel.posted_at >= cutoff)

        # 6. Skill match condition
        if req.skills:
            skill_conditions = []
            for skill in req.skills:
                skill_lower = skill.lower()
                skill_conditions.append(
                    func.lower(func.cast(JobModel.required_skills, String)).like(
                        f"%{skill_lower}%"
                    )
                )
            if skill_conditions:
                query = query.filter(or_(*skill_conditions))

        return query.order_by(JobModel.posted_at.desc()).all()

    def get_all_jobs(self, limit: int = 20) -> List[JobModel]:
        return (
            self.db.query(JobModel)
            .order_by(JobModel.posted_at.desc())
            .limit(limit)
            .all()
        )

    def get_job_by_id(self, job_id: str) -> Optional[JobModel]:
        """Fetches a single job by its primary key UUID."""
        return self.db.query(JobModel).filter(JobModel.id == job_id).first()

    def save_or_update_analyzed_job(
        self, job_data: BasicJobData, ai_analysis: JobAnalysis
    ) -> JobModel:
        existing_job = (
            self.db.query(JobModel).filter(JobModel.source_url == job_data.url).first()
        )

        salary_currency = (
            ai_analysis.salary.currency
            if ai_analysis.salary
            else job_data.salary_currency
        )
        salary_min = (
            ai_analysis.salary.min_amount if ai_analysis.salary else job_data.salary_min
        )
        salary_max = (
            ai_analysis.salary.max_amount if ai_analysis.salary else job_data.salary_max
        )
        salary_period = (
            ai_analysis.salary.period.value
            if ai_analysis.salary and ai_analysis.salary.period
            else None
        )

        if existing_job:
            existing_job.title = job_data.title
            existing_job.company = job_data.company
            existing_job.location = job_data.location
            existing_job.work_type = ai_analysis.work_type.value
            existing_job.employment_type = ai_analysis.employment_type.value
            existing_job.experience_level = ai_analysis.experience_level.value
            existing_job.min_years_exp = ai_analysis.min_years_experience
            existing_job.max_years_exp = ai_analysis.max_years_experience
            existing_job.required_skills = ai_analysis.required_skills
            existing_job.nice_to_have_skills = ai_analysis.nice_to_have_skills
            existing_job.summary = ai_analysis.summary
            existing_job.raw_description = job_data.description
            existing_job.salary_currency = salary_currency
            existing_job.salary_min = salary_min
            existing_job.salary_max = salary_max
            existing_job.salary_period = salary_period
            db_item = existing_job
        else:
            db_item = JobModel(
                title=job_data.title,
                company=job_data.company,
                location=job_data.location,
                work_type=ai_analysis.work_type.value,
                employment_type=ai_analysis.employment_type.value,
                experience_level=ai_analysis.experience_level.value,
                min_years_exp=ai_analysis.min_years_experience,
                max_years_exp=ai_analysis.max_years_experience,
                required_skills=ai_analysis.required_skills,
                nice_to_have_skills=ai_analysis.nice_to_have_skills,
                summary=ai_analysis.summary,
                raw_description=job_data.description,
                salary_currency=salary_currency,
                salary_min=salary_min,
                salary_max=salary_max,
                salary_period=salary_period,
                source=job_data.source,
                source_url=job_data.url,
                posted_at=job_data.posted_at,
            )
            self.db.add(db_item)

        self.db.commit()
        self.db.refresh(db_item)
        return db_item

