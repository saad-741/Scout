from typing import List
from fastapi import FastAPI, Query
from app.core.config import settings
from app.schemas.job import BasicJobData
from app.services.job_service import JobService

app = FastAPI(title=settings.APP_NAME)


@app.get("/", summary="Root Health Check")
async def root():
    return {"message": "Scout API is running"}


@app.get("/api/v1/jobs/extracted", response_model=List[BasicJobData], summary="Fetch & Extract Basic Job Data")
async def get_extracted_jobs(
    role: str = Query(..., example="Backend Developer"),
    location: str = Query(..., example="Lahore"),
    remote_only: bool = Query(False, example=False),
):
    """
    Search external providers and apply deterministic extractions to standardize fields.
    """
    service = JobService()
    return await service.fetch_and_extract_jobs(role=role, location=location, remote_only=remote_only)

 

 