import re

from app.schemas.job import JobResult


def normalize_value(value: str | None) -> str:
    if not value:
        return ""

    value = value.lower().strip()

    value = re.sub(
        r"[^a-z0-9\s]",
        "",
        value,
    )

    return " ".join(value.split())


def create_job_key(job: JobResult) -> str:

    # Provider-specific ID is strongest
    if job.external_id:
        return (
            f"{job.source}:"
            f"{normalize_value(job.external_id)}"
        )

    # Fallback for jobs without external IDs
    return "|".join(
        [
            normalize_value(job.title),
            normalize_value(job.company),
            normalize_value(job.location),
        ]
    )


def deduplicate_jobs(
    jobs: list[JobResult],
) -> list[JobResult]:

    unique_jobs = []
    seen_keys = set()

    for job in jobs:

        key = create_job_key(job)

        if not key:
            continue

        if key in seen_keys:
            continue

        seen_keys.add(key)
        unique_jobs.append(job)

    return unique_jobs