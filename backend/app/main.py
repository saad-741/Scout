from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.schemas.job import JobResponse, JobSearchRequest
from app.services.job_service import JobService

app = FastAPI(
    title=settings.APP_NAME,
    description="Scout Mobile Job Intelligence API",
    version="1.0.0",
)


@app.get("/", summary="Root Health Check")
async def root():
    return {"message": "Scout API is running"}


# --- Testing Route ---
@app.post(
    "/api/v1/jobs/process",
    response_model=List[JobResponse],
    summary="Full End-to-End Search Pipeline (Fetch -> Deduplicate -> AI Process -> Supabase DB)",
)
async def process_jobs(
    role: str = Query(..., json_schema_extra={"example": "Backend Developer"}),
    location: str = Query(..., json_schema_extra={"example": "Lahore"}),
    remote_only: bool = Query(False, json_schema_extra={"example": False}),
    db: Session = Depends(get_db),
):
    service = JobService(db=db)
    return await service.process_search_pipeline(
        role=role, location=location, remote_only=remote_only
    )


# --- Search Route ---
@app.post(
    "/api/v1/jobs/search",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Search & AI-Structure Jobs for Mobile Client",
)
async def search_jobs(
    request: JobSearchRequest,
    db: Session = Depends(get_db),
):
    """
    Primary endpoint consumed by Flutter App.
    Accepts search filters, checks DB cache, executes pipeline on miss, and returns filtered jobs.
    """
    try:
        service = JobService(db=db)
        return await service.execute_search(request)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing job search: {str(err)}",
        )


# --- DB Fetch Route ---
@app.get(
    "/api/v1/jobs",
    response_model=List[JobResponse],
    summary="Fetch All Saved Jobs with AI Analysis",
)
async def get_jobs(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    from app.repositories.job_repository import JobRepository

    repo = JobRepository(db)
    return repo.get_all_jobs(limit=limit)


@app.get(
    "/api/v1/jobs/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch Detailed Job Information by ID",
)
async def get_job_details(
    job_id: str,
    db: Session = Depends(get_db),
):
    """
    Fetch complete job details by job_id.
    Reads directly from Supabase DB (0% Gemini Quota Usage).
    """
    service = JobService(db=db)
    job = service.get_job_details(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID '{job_id}' was not found.",
        )
    return job 

   