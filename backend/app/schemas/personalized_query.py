from pydantic import BaseModel, Field


class PersonalizedQuery(BaseModel):
    query: str
    location: str | None = None
    role: str | None = None
    priority: int = 1
    reason: str | None = None


class PersonalizedQueryPlan(BaseModel):
    original_query: str
    queries: list[PersonalizedQuery] = Field(
        default_factory=list
    )