from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str
    location: str | None = None
    priority: int = 1


class SearchPlan(BaseModel):
    original_query: str
    job_title: str | None = None
    location: str | None = None
    experience_level: str | None = None
    work_mode: str | None = None
    job_type: str | None = None
    queries: list[SearchQuery] = Field(default_factory=list)