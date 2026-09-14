from datetime import datetime

from app.schemas.job import JobResult


def clean_text(value: str | None) -> str | None:
    if not value:
        return None

    return " ".join(value.split()).strip()


def normalize_job(job: JobResult) -> JobResult:
    return JobResult(
        source=job.source.strip().lower(),

        external_id=(
            str(job.external_id)
            if job.external_id
            else None
        ),

        title=clean_text(job.title) or "Unknown Job",

        company=clean_text(job.company),

        location=clean_text(job.location),

        description=clean_text(job.description),

        job_url=job.job_url.strip(),

        apply_url=(
            job.apply_url.strip()
            if job.apply_url
            else job.job_url.strip()
        ),

        posted_at=job.posted_at,

        employment_type=clean_text(
            job.employment_type
        ),

        work_mode=clean_text(
            job.work_mode
        ),

        salary_min=job.salary_min,

        salary_max=job.salary_max,

        currency=clean_text(
            job.currency
        ),

        source_metadata=job.source_metadata or {},
    )


def normalize_jobs(
    jobs: list[JobResult],
) -> list[JobResult]:

    normalized = []

    for job in jobs:
        try:
            normalized_job = normalize_job(job)

            if not normalized_job.job_url:
                continue

            normalized.append(normalized_job)

        except Exception as e:
            print(
                f"Job normalization failed: {e}"
            )

    return normalized