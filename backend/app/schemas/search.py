from pydantic import BaseModel, Field


class JobSearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        description="Natural language job search query",
    )


class JobSearchIntent(BaseModel):
    job_title: str | None = None
    location: str | None = None
    experience_level: str | None = None
    work_mode: str | None = None
    job_type: str | None = None
    keywords: list[str] = Field(default_factory=list)