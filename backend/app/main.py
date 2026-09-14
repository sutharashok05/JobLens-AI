from fastapi import FastAPI, HTTPException

from app.api.resumes import router as resume_router
from app.db.database import test_database_connection
from app.api.profile import router as profile_router
from app.api.search import router as search_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="JobLens AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://joblens-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resume_router)
app.include_router(profile_router)
app.include_router(search_router)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "JobLens AI backend is running",
        "docs": "/docs",
        "health": "/health",
    }



@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "JobLens AI backend is running",
    }


@app.get("/health/db")
async def database_health_check():
    try:
        result = await test_database_connection()

        return {
            "status": "ok",
            "database": result[0],
            "postgresql": result[1],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}",
        )