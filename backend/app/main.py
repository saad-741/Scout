from fastapi import FastAPI

app = FastAPI(
    title="Scout API",
    description="Mobile Job-Search & Job-Intelligence Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", summary="Root Health Check")
async def root():
    return {"message": "Scout API is running"}