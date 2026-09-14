from datetime import datetime

from pydantic import BaseModel, Field


class JobSearchFilters(BaseModel):
    experience_level: str | None = None
    work_mode: str | None = None
    job_type: str | None = None


class JobResult(BaseModel):
    source: str
    external_id: str | None = None

    title: str
    company: str | None = None
    location: str | None = None

    description: str | None = None

    job_url: str
    apply_url: str | None = None

    posted_at: datetime | None = None

    employment_type: str | None = None
    work_mode: str | None = None

    salary_min: float | None = None
    salary_max: float | None = None
    currency: str | None = None

    source_metadata: dict = Field(
        default_factory=dict
    )