import re

from app.schemas.search import JobSearchIntent


LOCATION_ALIASES = {
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "mumbai": "Mumbai",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "jaipur": "Jaipur",
    "udaipur": "Udaipur",
    "noida": "Noida",
    "gurgaon": "Gurgaon",
    "gurugram": "Gurgaon",
}


WORK_MODES = {
    "remote": "remote",
    "work from home": "remote",
    "wfh": "remote",
    "hybrid": "hybrid",
    "on site": "onsite",
    "onsite": "onsite",
    "office": "onsite",
}


JOB_TYPES = {
    "full time": "full-time",
    "full-time": "full-time",
    "part time": "part-time",
    "part-time": "part-time",
    "internship": "internship",
    "intern": "internship",
    "contract": "contract",
}


EXPERIENCE_LEVELS = {
    "fresher": "fresher",
    "entry level": "entry-level",
    "entry-level": "entry-level",
    "junior": "junior",
    "senior": "senior",
}


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.lower()).strip()


def extract_location(query: str) -> str | None:
    query_lower = normalize_query(query)

    for location, normalized_location in LOCATION_ALIASES.items():
        if location in query_lower:
            return normalized_location

    return None


def extract_work_mode(query: str) -> str | None:
    query_lower = normalize_query(query)

    for mode, normalized_mode in WORK_MODES.items():
        if mode in query_lower:
            return normalized_mode

    return None


def extract_job_type(query: str) -> str | None:
    query_lower = normalize_query(query)

    for job_type, normalized_type in JOB_TYPES.items():
        if job_type in query_lower:
            return normalized_type

    return None


def extract_experience_level(query: str) -> str | None:
    query_lower = normalize_query(query)

    for level, normalized_level in EXPERIENCE_LEVELS.items():
        if level in query_lower:
            return normalized_level

    return None


def extract_job_title(query: str) -> str | None:
    query_lower = normalize_query(query)

    patterns = [
        r"(?:find|search|looking for|get me)\s+(.+?)\s+jobs?",
        r"(.+?)\s+jobs?\s+(?:in|at|near)",
        r"(.+?)\s+jobs?$",
    ]

    for pattern in patterns:
        match = re.search(pattern, query_lower)

        if match:
            title = match.group(1).strip()

            title = re.sub(
                r"\b(remote|hybrid|onsite|internship|intern)\b",
                "",
                title,
            )

            title = title.strip()

            if title:
                return title

    return None


def parse_search_intent(query: str) -> JobSearchIntent:
    return JobSearchIntent(
        job_title=extract_job_title(query),
        location=extract_location(query),
        experience_level=extract_experience_level(query),
        work_mode=extract_work_mode(query),
        job_type=extract_job_type(query),
        keywords=[],
    )