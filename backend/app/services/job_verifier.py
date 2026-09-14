import httpx

from app.schemas.job import JobResult


def get_verification_urls(job: JobResult) -> list[str]:
    urls = []

    metadata = job.source_metadata or {}

    source_link = metadata.get("source_link")

    if source_link:
        urls.append(source_link)

    if job.apply_url:
        urls.append(job.apply_url)

    if job.job_url:
        urls.append(job.job_url)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(urls))


async def verify_job(job: JobResult) -> JobResult:

    verified = False
    verified_url = None
    status_code = None

    urls = get_verification_urls(job)

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/131.0 Safari/537.36"
                )
            },
        ) as client:

            for url in urls:

                try:
                    response = await client.get(url)

                    status_code = response.status_code

                    if 200 <= status_code < 400:
                        verified = True
                        verified_url = str(
                            response.url
                        )
                        break

                except httpx.RequestError:
                    continue

    except Exception:
        verified = False

    metadata = dict(
        job.source_metadata or {}
    )

    metadata["verification"] = {
        "verified": verified,
        "status_code": status_code,
        "verified_url": verified_url,
    }

    return job.model_copy(
        update={
            "source_metadata": metadata
        }
    )


async def verify_jobs(
    jobs: list[JobResult],
) -> list[JobResult]:

    if not jobs:
        return []

    results = []

    for job in jobs:
        results.append(
            await verify_job(job)
        )

    return results