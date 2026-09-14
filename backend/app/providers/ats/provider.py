import asyncio
from datetime import datetime
from html import unescape
import re

import httpx

from app.providers.base import JobSearchProvider
from app.schemas.job import JobResult, JobSearchFilters
from app.providers.ats.company_registry import get_registry


class ATSProvider(JobSearchProvider):
    name = "ats"
    provider_type = "ats"

    GREENHOUSE_URL = (
        "https://boards-api.greenhouse.io/v1/boards"
    )

    LEVER_URL = (
        "https://api.lever.co/v0/postings"
    )

    ASHBY_URL = (
        "https://api.ashbyhq.com/posting-api/job-board"
    )

    # =====================================================
    # CONFIGURATION
    # =====================================================

    REQUEST_TIMEOUT = 30.0

    MAX_CONCURRENT_REQUESTS = 10

    # =====================================================
    # TEXT CLEANING
    # =====================================================

    @staticmethod
    def clean_html(
        value: str | None,
    ) -> str | None:

        if not value:
            return None

        value = unescape(str(value))

        value = re.sub(
            r"<[^>]+>",
            " ",
            value,
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value.strip()

    # =====================================================
    # DATETIME PARSING
    # =====================================================

    @staticmethod
    def parse_datetime(
        value: str | None,
    ) -> datetime | None:

        if not value:
            return None

        try:
            value = value.strip()

            if value.endswith("Z"):
                value = value[:-1] + "+00:00"

            return datetime.fromisoformat(value)

        except (
            ValueError,
            TypeError,
        ):
            return None

    # =====================================================
    # LOCATION NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize_location(
        value: str | None,
    ) -> str:

        if not value:
            return ""

        value = str(value).lower().strip()

        aliases = {
            "bengaluru": "bangalore",
            "new delhi": "delhi",
            "gurugram": "gurgaon",
        }

        for old, new in aliases.items():
            value = value.replace(
                old,
                new,
            )

        return value

    # =====================================================
    # QUERY MATCHING
    # =====================================================

    @classmethod
    def matches_query(
        cls,
        job: dict,
        query: str,
        location: str | None,
    ) -> bool:

        search_text = " ".join(
            [
                str(job.get("title", "")),
                str(job.get("description", "")),
                str(job.get("location", "")),
                str(job.get("department", "")),
                str(job.get("team", "")),
            ]
        ).lower()

        # -------------------------------------------------
        # QUERY
        # -------------------------------------------------

        query_words = [
            word.lower().strip()
            for word in query.split()
            if len(word.strip()) > 2
        ]

        if query_words:

            matched_query_words = sum(
                1
                for word in query_words
                if word in search_text
            )

            # At least one meaningful query term
            # must appear.
            if matched_query_words == 0:
                return False

        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        if location:

            requested_location = cls.normalize_location(
                location
            )

            job_location = cls.normalize_location(
                str(
                    job.get(
                        "location",
                        "",
                    )
                )
            )

            # Remote jobs should not be rejected simply
            # because the user specified a city.
            remote_keywords = [
                "remote",
                "work from home",
                "india remote",
                "remote india",
            ]

            is_remote = any(
                keyword in search_text
                for keyword in remote_keywords
            )

            location_matches = (
                requested_location in job_location
                or requested_location in search_text
                or (
                    requested_location == "bangalore"
                    and "bengaluru" in search_text
                )
                or (
                    requested_location == "delhi"
                    and "new delhi" in search_text
                )
                or (
                    requested_location == "gurgaon"
                    and "gurugram" in search_text
                )
            )

            if not location_matches and not is_remote:
                return False

        return True

    # =====================================================
    # GREENHOUSE
    # =====================================================

    async def search_greenhouse_board(
        self,
        client: httpx.AsyncClient,
        company: str,
        board_token: str,
        query: str,
        location: str | None,
    ) -> list[JobResult]:

        url = (
            f"{self.GREENHOUSE_URL}/"
            f"{board_token}/jobs"
        )

        params = {
            "content": "true",
        }

        try:

            response = await client.get(
                url,
                params=params,
            )

            if response.status_code != 200:

                print(
                    f"Greenhouse {company}: "
                    f"HTTP {response.status_code}"
                )

                return []

            data = response.json()

        except httpx.RequestError as e:

            print(
                f"Greenhouse {company} "
                f"request error: {e}"
            )

            return []

        except Exception as e:

            print(
                f"Greenhouse {company} "
                f"error: {type(e).__name__}: {e}"
            )

            return []

        jobs = data.get(
            "jobs",
            [],
        )

        if not isinstance(
            jobs,
            list,
        ):
            return []

        results: list[JobResult] = []

        for job in jobs:

            if not isinstance(
                job,
                dict,
            ):
                continue

            title = job.get(
                "title"
            )

            if not title:
                continue

            # ---------------------------------------------
            # LOCATION
            # ---------------------------------------------

            location_data = job.get(
                "location",
                {},
            )

            if isinstance(
                location_data,
                dict,
            ):

                job_location = (
                    location_data.get(
                        "name"
                    )
                    or ""
                )

            else:

                job_location = str(
                    location_data
                )

            # ---------------------------------------------
            # DESCRIPTION
            # ---------------------------------------------

            description = (
                job.get(
                    "content"
                )
                or ""
            )

            clean_description = (
                self.clean_html(
                    description
                )
                or ""
            )

            # ---------------------------------------------
            # DEPARTMENTS
            # ---------------------------------------------

            departments = job.get(
                "departments",
                [],
            )

            if not isinstance(
                departments,
                list,
            ):
                departments = []

            department_names = []

            for department in departments:

                if isinstance(
                    department,
                    dict,
                ):

                    name = department.get(
                        "name"
                    )

                    if name:
                        department_names.append(
                            name
                        )

                elif department:
                    department_names.append(
                        str(department)
                    )

            department_text = " ".join(
                department_names
            )

            # ---------------------------------------------
            # SEARCH MATCH
            # ---------------------------------------------

            search_data = {
                "title": title,
                "description": clean_description,
                "location": job_location,
                "department": department_text,
            }

            if not self.matches_query(
                search_data,
                query,
                location,
            ):
                continue

            # ---------------------------------------------
            # URL
            # ---------------------------------------------

            job_url = job.get(
                "absolute_url"
            )

            if not job_url:
                continue

            # ---------------------------------------------
            # DATE
            # ---------------------------------------------

            posted_at = self.parse_datetime(
                job.get(
                    "updated_at"
                )
            )

            # ---------------------------------------------
            # RESULT
            # ---------------------------------------------

            results.append(
                JobResult(
                    source="ats",
                    external_id=str(
                        job.get(
                            "id"
                        )
                    ),
                    title=title,
                    company=company,
                    location=job_location,
                    description=clean_description,
                    job_url=job_url,
                    apply_url=job_url,
                    posted_at=posted_at,
                    employment_type=None,
                    work_mode=None,
                    salary_min=None,
                    salary_max=None,
                    currency=None,
                    source_metadata={
                        "ats_type": "greenhouse",
                        "company": company,
                        "board_token": board_token,
                        "departments": departments,
                        "offices": job.get(
                            "offices",
                            [],
                        ),
                        "updated_at": job.get(
                            "updated_at"
                        ),
                        "requisition_id": job.get(
                            "requisition_id"
                        ),
                    },
                )
            )

        return results

    # =====================================================
    # ASHBY
    # =====================================================

    async def search_ashby_board(
        self,
        client: httpx.AsyncClient,
        company: str,
        board_name: str,
        query: str,
        location: str | None,
    ) -> list[JobResult]:

        url = (
            f"{self.ASHBY_URL}/"
            f"{board_name}"
        )

        params = {
            "includeCompensation": "true",
        }

        try:

            response = await client.get(
                url,
                params=params,
            )

            if response.status_code != 200:

                print(
                    f"Ashby {company}: "
                    f"HTTP {response.status_code}"
                )

                return []

            data = response.json()

        except httpx.RequestError as e:

            print(
                f"Ashby {company} "
                f"request error: {e}"
            )

            return []

        except Exception as e:

            print(
                f"Ashby {company} "
                f"error: {type(e).__name__}: {e}"
            )

            return []

        jobs = data.get(
            "jobs",
            [],
        )

        if not isinstance(
            jobs,
            list,
        ):
            return []

        results: list[JobResult] = []

        for job in jobs:

            if not isinstance(
                job,
                dict,
            ):
                continue

            # Only published/listed jobs.
            if not job.get(
                "isListed",
                True,
            ):
                continue

            title = job.get(
                "title"
            )

            if not title:
                continue

            job_location = (
                job.get(
                    "location"
                )
                or ""
            )

            description = (
                job.get(
                    "descriptionPlain"
                )
                or ""
            )

            department = (
                job.get(
                    "department"
                )
                or ""
            )

            team = (
                job.get(
                    "team"
                )
                or ""
            )

            # ---------------------------------------------
            # SEARCH MATCH
            # ---------------------------------------------

            search_data = {
                "title": title,
                "description": description,
                "location": job_location,
                "department": department,
                "team": team,
            }

            if not self.matches_query(
                search_data,
                query,
                location,
            ):
                continue

            # ---------------------------------------------
            # URL
            # ---------------------------------------------

            job_url = job.get(
                "jobUrl"
            )

            apply_url = job.get(
                "applyUrl"
            )

            if not job_url:
                continue

            # ---------------------------------------------
            # DATE
            # ---------------------------------------------

            posted_at = self.parse_datetime(
                job.get(
                    "publishedAt"
                )
            )

            # ---------------------------------------------
            # COMPENSATION
            # ---------------------------------------------

            compensation = job.get(
                "compensation"
            )

            if not isinstance(
                compensation,
                dict,
            ):
                compensation = None

            # ---------------------------------------------
            # SECONDARY LOCATIONS
            # ---------------------------------------------

            secondary_locations = (
                job.get(
                    "secondaryLocations",
                    [],
                )
            )

            if not isinstance(
                secondary_locations,
                list,
            ):
                secondary_locations = []

            # ---------------------------------------------
            # RESULT
            # ---------------------------------------------

            results.append(
                JobResult(
                    source="ats",
                    external_id=str(
                        job_url
                    ),
                    title=title,
                    company=company,
                    location=job_location,
                    description=description,
                    job_url=job_url,
                    apply_url=(
                        apply_url
                        or job_url
                    ),
                    posted_at=posted_at,
                    employment_type=(
                        job.get(
                            "employmentType"
                        )
                    ),
                    work_mode=(
                        job.get(
                            "workplaceType"
                        )
                    ),
                    salary_min=None,
                    salary_max=None,
                    currency=None,
                    source_metadata={
                        "ats_type": "ashby",
                        "company": company,
                        "board_name": board_name,
                        "department": department,
                        "team": team,
                        "is_remote": job.get(
                            "isRemote"
                        ),
                        "secondary_locations": (
                            secondary_locations
                        ),
                        "compensation": compensation,
                    },
                )
            )

        return results

    # =====================================================
    # LEVER
    # =====================================================

    async def search_lever_account(
        self,
        client: httpx.AsyncClient,
        company: str,
        account: str,
        query: str,
        location: str | None,
    ) -> list[JobResult]:

        url = (
            f"{self.LEVER_URL}/"
            f"{account}"
        )

        params = {
            "mode": "json",
        }

        try:

            response = await client.get(
                url,
                params=params,
            )

            if response.status_code != 200:

                print(
                    f"Lever {company}: "
                    f"HTTP {response.status_code}"
                )

                return []

            data = response.json()

        except httpx.RequestError as e:

            print(
                f"Lever {company} "
                f"request error: {e}"
            )

            return []

        except Exception as e:

            print(
                f"Lever {company} "
                f"error: {type(e).__name__}: {e}"
            )

            return []

        if not isinstance(
            data,
            list,
        ):
            return []

        results: list[JobResult] = []

        for job in data:

            if not isinstance(
                job,
                dict,
            ):
                continue

            title = job.get(
                "text"
            )

            if not title:
                continue

            # ---------------------------------------------
            # CATEGORIES
            # ---------------------------------------------

            categories = job.get(
                "categories",
                {},
            )

            if not isinstance(
                categories,
                dict,
            ):
                categories = {}

            job_location = (
                categories.get(
                    "location"
                )
                or ""
            )

            department = (
                categories.get(
                    "department"
                )
                or ""
            )

            team = (
                categories.get(
                    "team"
                )
                or ""
            )

            commitment = (
                categories.get(
                    "commitment"
                )
                or ""
            )

            # ---------------------------------------------
            # DESCRIPTION
            # ---------------------------------------------

            content = (
                job.get(
                    "descriptionPlain"
                )
                or ""
            )

            if not content:

                content = (
                    job.get(
                        "description"
                    )
                    or ""
                )

            content = (
                self.clean_html(
                    content
                )
                or ""
            )

            # ---------------------------------------------
            # SEARCH MATCH
            # ---------------------------------------------

            search_data = {
                "title": title,
                "description": content,
                "location": job_location,
                "department": department,
                "team": team,
            }

            if not self.matches_query(
                search_data,
                query,
                location,
            ):
                continue

            # ---------------------------------------------
            # URLS
            # ---------------------------------------------

            hosted_url = job.get(
                "hostedUrl"
            )

            apply_url = job.get(
                "applyUrl"
            )

            job_url = (
                hosted_url
                or apply_url
            )

            if not job_url:
                continue

            # ---------------------------------------------
            # SALARY
            # ---------------------------------------------

            salary = job.get(
                "salaryRange"
            )

            if not isinstance(
                salary,
                dict,
            ):
                salary = {}

            salary_min = salary.get(
                "min"
            )

            salary_max = salary.get(
                "max"
            )

            currency = salary.get(
                "currency"
            )

            # ---------------------------------------------
            # RESULT
            # ---------------------------------------------

            results.append(
                JobResult(
                    source="ats",
                    external_id=str(
                        job.get(
                            "id"
                        )
                    ),
                    title=title,
                    company=company,
                    location=job_location,
                    description=content,
                    job_url=job_url,
                    apply_url=(
                        apply_url
                        or job_url
                    ),
                    posted_at=None,
                    employment_type=commitment,
                    work_mode=(
                        job.get(
                            "workplaceType"
                        )
                    ),
                    salary_min=salary_min,
                    salary_max=salary_max,
                    currency=currency,
                    source_metadata={
                        "ats_type": "lever",
                        "company": company,
                        "account": account,
                        "team": team,
                        "department": department,
                        "commitment": commitment,
                        "all_locations": (
                            categories.get(
                                "allLocations",
                                [],
                            )
                        ),
                        "salary_description": (
                            job.get(
                                "salaryDescriptionPlain"
                            )
                        ),
                    },
                )
            )

        return results

    # =====================================================
    # MAIN SEARCH
    # =====================================================

    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:

        registry = get_registry()

        if not registry:

            print(
                "ATS: Company registry is empty."
            )

            return []

        # -------------------------------------------------
        # SEMAPHORE
        # -------------------------------------------------

        semaphore = asyncio.Semaphore(
            self.MAX_CONCURRENT_REQUESTS
        )

        async def limited_call(
            coroutine,
        ):
            async with semaphore:
                return await coroutine

        # -------------------------------------------------
        # HTTP CLIENT
        # -------------------------------------------------

        async with httpx.AsyncClient(
            timeout=self.REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "JobLensAI/1.0 "
                    "(job discovery service)"
                ),
                "Accept": "application/json",
            },
        ) as client:

            tasks = []

            # -------------------------------------------------
            # CREATE TASKS FROM REGISTRY
            # -------------------------------------------------

            for company in registry:

                ats_type = (
                    company.ats
                    .strip()
                    .lower()
                )

                if ats_type == "greenhouse":

                    tasks.append(
                        limited_call(
                            self.search_greenhouse_board(
                                client=client,
                                company=company.company,
                                board_token=company.identifier,
                                query=query,
                                location=location,
                            )
                        )
                    )

                elif ats_type == "lever":

                    tasks.append(
                        limited_call(
                            self.search_lever_account(
                                client=client,
                                company=company.company,
                                account=company.identifier,
                                query=query,
                                location=location,
                            )
                        )
                    )

                elif ats_type == "ashby":

                    tasks.append(
                        limited_call(
                            self.search_ashby_board(
                                client=client,
                                company=company.company,
                                board_name=company.identifier,
                                query=query,
                                location=location,
                            )
                        )
                    )

                else:

                    print(
                        f"ATS: Unsupported ATS "
                        f"'{company.ats}' "
                        f"for {company.company}"
                    )

            if not tasks:

                print(
                    "ATS: No valid registry "
                    "providers configured."
                )

                return []

            # -------------------------------------------------
            # PARALLEL SEARCH
            # -------------------------------------------------

            results = await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        # -------------------------------------------------
        # FLATTEN RESULTS
        # -------------------------------------------------

        jobs: list[JobResult] = []

        for result in results:

            if isinstance(
                result,
                Exception,
            ):

                print(
                    "ATS task failed: "
                    f"{type(result).__name__}: "
                    f"{result}"
                )

                continue

            if not isinstance(
                result,
                list,
            ):
                continue

            jobs.extend(
                result
            )

        # -------------------------------------------------
        # BASIC FILTERS
        # -------------------------------------------------

        if filters:

            filtered_jobs = []

            for job in jobs:

                # Experience level is not consistently
                # available across ATS APIs, so do not
                # aggressively remove jobs here.

                if (
                    filters.work_mode
                    and job.work_mode
                ):

                    requested_mode = (
                        filters.work_mode
                        .lower()
                        .strip()
                    )

                    actual_mode = (
                        job.work_mode
                        .lower()
                        .strip()
                    )

                    if (
                        requested_mode
                        not in actual_mode
                    ):
                        continue

                if (
                    filters.job_type
                    and job.employment_type
                ):

                    requested_type = (
                        filters.job_type
                        .lower()
                        .strip()
                    )

                    actual_type = (
                        job.employment_type
                        .lower()
                        .strip()
                    )

                    if (
                        requested_type
                        not in actual_type
                    ):
                        continue

                filtered_jobs.append(
                    job
                )

            jobs = filtered_jobs

        # -------------------------------------------------
        # SORT BY REGISTRY PRIORITY
        # -------------------------------------------------

        priority_map = {
            company.company.lower(): company.priority
            for company in registry
        }

        def priority_key(
            job: JobResult,
        ) -> int:

            company_name = (
                job.company or ""
            ).lower()

            return priority_map.get(
                company_name,
                3,
            )

        jobs.sort(
            key=priority_key
        )

        # -------------------------------------------------
        # FINAL LOG
        # -------------------------------------------------

        print(
            f"ATS companies searched: "
            f"{len(registry)}"
        )

        print(
            f"ATS jobs found: "
            f"{len(jobs)}"
        )

        return jobs