import asyncio
import httpx

from app.core.config import settings


async def test_serpapi():
    params = {
        "engine": "google_jobs",
        "q": "AI Engineer Bangalore",
        "api_key": settings.SERPAPI_KEY,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            "https://serpapi.com/search.json",
            params=params,
        )

        data = response.json()

        print("HTTP:", response.status_code)

        jobs_results = data.get("jobs_results")

        print("TYPE:", type(jobs_results))
        print("COUNT:", len(jobs_results) if jobs_results else 0)

        if jobs_results:
            print("\nFIRST JOB:")
            print(jobs_results[0])

        print("\nALL KEYS:")
        print(data.keys())


asyncio.run(test_serpapi())