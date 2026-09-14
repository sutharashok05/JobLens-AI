import re

from app.schemas.job import JobResult


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {
    "python": [
        "python",
    ],

    "c++": [
        "c++",
        "cpp",
    ],

    "javascript": [
        "javascript",
        "java script",
        "js",
    ],

    "react.js": [
        "react.js",
        "reactjs",
        "react js",
        "react",
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js",
        "node",
    ],

    "express.js": [
        "express.js",
        "expressjs",
        "express js",
        "express",
    ],

    "fastapi": [
        "fastapi",
        "fast api",
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo",
    ],

    "postgresql": [
        "postgresql",
        "postgres",
    ],

    "sql": [
        "sql",
    ],

    "git": [
        "git",
    ],

    "github": [
        "github",
        "git hub",
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml",
    ],

    "pandas": [
        "pandas",
    ],

    "numpy": [
        "numpy",
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
    ],

    "rest api": [
        "rest api",
        "restful api",
        "rest apis",
        "rest-api",
    ],
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_for_matching(
    text: str | None,
) -> str:
    """
    Convert text into a matching-friendly format.
    """

    if not text:
        return ""

    text = text.lower()

    # Handle C++ before punctuation removal
    text = text.replace(
        "c++",
        " cpp ",
    )

    # Normalize common technology variations
    text = text.replace(
        "scikit learn",
        "scikit-learn",
    )

    # Convert punctuation to spaces
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# =========================================================
# SKILL MATCHING
# =========================================================

def skill_is_present(
    skill: str,
    job_text: str,
) -> bool:

    skill_key = skill.lower().strip()

    aliases = SKILL_ALIASES.get(
        skill_key,
        [skill_key],
    )

    normalized_job = normalize_for_matching(
        job_text
    )

    for alias in aliases:

        alias_normalized = (
            normalize_for_matching(alias)
        )

        if not alias_normalized:
            continue

        # Exact word / phrase matching
        pattern = (
            r"\b"
            + re.escape(alias_normalized)
            + r"\b"
        )

        if re.search(
            pattern,
            normalized_job,
        ):
            return True

        # Fallback substring matching
        if alias_normalized in normalized_job:
            return True

    return False


def calculate_skill_match(
    candidate_skills: list,
    job_text: str,
):
    matched_skills = []
    missing_skills = []

    for skill in candidate_skills:

        if not isinstance(
            skill,
            str,
        ):
            continue

        if skill_is_present(
            skill,
            job_text,
        ):
            matched_skills.append(
                skill
            )
        else:
            missing_skills.append(
                skill
            )

    total_skills = (
        len(matched_skills)
        + len(missing_skills)
    )

    if total_skills == 0:
        score = 0.0
    else:
        score = (
            len(matched_skills)
            / total_skills
        ) * 100

    return (
        round(score, 2),
        matched_skills,
        missing_skills,
    )


# =========================================================
# ROLE MATCHING
# =========================================================

def calculate_role_match(
    preferred_roles: list,
    job_title: str | None,
) -> float:

    if not preferred_roles:
        return 0.0

    if not job_title:
        return 0.0

    title = normalize_for_matching(
        job_title
    )

    role_groups = {
        "ai": [
            "ai",
            "artificial intelligence",
            "gen ai",
            "machine learning",
            "ml",
        ],

        "software": [
            "software engineer",
            "software developer",
            "software",
        ],

        "full stack": [
            "full stack",
            "fullstack",
        ],

        "backend": [
            "backend",
            "back end",
        ],

        "frontend": [
            "frontend",
            "front end",
        ],

        "data": [
            "data scientist",
            "data analyst",
            "data science",
            "data analysis",
        ],
    }

    for role in preferred_roles:

        if not isinstance(
            role,
            str,
        ):
            continue

        role_text = normalize_for_matching(
            role
        )

        if not role_text:
            continue

        # ---------------------------------------------
        # Exact role match
        # ---------------------------------------------

        if role_text in title:
            return 100.0

        # ---------------------------------------------
        # Related role match
        # ---------------------------------------------

        for keywords in role_groups.values():

            role_matches_group = any(
                normalize_for_matching(keyword)
                in role_text
                for keyword in keywords
            )

            title_matches_group = any(
                normalize_for_matching(keyword)
                in title
                for keyword in keywords
            )

            if (
                role_matches_group
                and title_matches_group
            ):
                return 70.0

    return 0.0


# =========================================================
# LOCATION ALIASES
# =========================================================

LOCATION_ALIASES = {
    "bangalore": [
        "bangalore",
        "bengaluru",
    ],

    "bengaluru": [
        "bangalore",
        "bengaluru",
    ],

    "delhi": [
        "delhi",
        "new delhi",
    ],

    "new delhi": [
        "delhi",
        "new delhi",
    ],

    "gurgaon": [
        "gurgaon",
        "gurugram",
    ],

    "gurugram": [
        "gurgaon",
        "gurugram",
    ],

    "mumbai": [
        "mumbai",
        "bombay",
    ],

    "chennai": [
        "chennai",
        "madras",
    ],

    "kolkata": [
        "kolkata",
        "calcutta",
    ],

    "hyderabad": [
        "hyderabad",
    ],

    "pune": [
        "pune",
    ],

    "noida": [
        "noida",
    ],
}


# =========================================================
# LOCATION MATCHING
# =========================================================

def calculate_location_match(
    preferred_locations: list,
    job_location: str | None,
    requested_location: str | None = None,
) -> float:

    if not job_location:
        return 0.0

    location = normalize_for_matching(
        job_location
    )

    if not location:
        return 0.0

    # -----------------------------------------------------
    # Combine profile locations + requested search location
    # -----------------------------------------------------

    locations_to_match = list(
        preferred_locations or []
    )

    if requested_location:
        locations_to_match.append(
            requested_location
        )

    # Remove duplicates
    locations_to_match = list(
        dict.fromkeys(
            locations_to_match
        )
    )

    if not locations_to_match:
        return 0.0

    # -----------------------------------------------------
    # Match locations
    # -----------------------------------------------------

    for preferred in locations_to_match:

        if not isinstance(
            preferred,
            str,
        ):
            continue

        preferred_key = (
            preferred.lower().strip()
        )

        aliases = LOCATION_ALIASES.get(
            preferred_key,
            [preferred_key],
        )

        for alias in aliases:

            normalized_alias = (
                normalize_for_matching(alias)
            )

            if not normalized_alias:
                continue

            if normalized_alias in location:
                return 100.0

    return 0.0


# =========================================================
# COMPLETE MATCH SCORE
# =========================================================

def calculate_match_score(
    job: JobResult,
    profile: dict,
) -> dict:

    # -----------------------------------------------------
    # Candidate information
    # -----------------------------------------------------

    candidate_skills = profile.get(
        "skills",
        [],
    )

    preferred_roles = profile.get(
        "preferred_roles",
        [],
    )

    preferred_locations = profile.get(
        "preferred_locations",
        [],
    )

    requested_location = profile.get(
        "requested_location"
    )

    # -----------------------------------------------------
    # Complete job text
    # -----------------------------------------------------

    job_text = " ".join(
        [
            job.title or "",
            job.company or "",
            job.location or "",
            job.description or "",
        ]
    )

    # -----------------------------------------------------
    # Skill matching
    # -----------------------------------------------------

    (
        skill_score,
        matched_skills,
        missing_skills,
    ) = calculate_skill_match(
        candidate_skills,
        job_text,
    )

    # -----------------------------------------------------
    # Role matching
    # -----------------------------------------------------

    role_score = calculate_role_match(
        preferred_roles,
        job.title,
    )

    # -----------------------------------------------------
    # Location matching
    # -----------------------------------------------------

    location_score = calculate_location_match(
        preferred_locations=preferred_locations,
        job_location=job.location,
        requested_location=requested_location,
    )

    # -----------------------------------------------------
    # Final resume-job match score
    #
    # Skills    = 60%
    # Role      = 25%
    # Location  = 15%
    # -----------------------------------------------------

    final_score = (
        skill_score * 0.60
        + role_score * 0.25
        + location_score * 0.15
    )

    return {
        "match_score": round(
            final_score,
            2,
        ),

        "skill_match_score": round(
            skill_score,
            2,
        ),

        "role_match_score": round(
            role_score,
            2,
        ),

        "location_match_score": round(
            location_score,
            2,
        ),

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,
    }


# =========================================================
# MATCH ALL JOBS
# =========================================================

def match_jobs(
    jobs: list[JobResult],
    profile: dict,
) -> list[JobResult]:

    matched_jobs = []

    for job in jobs:

        match_data = calculate_match_score(
            job,
            profile,
        )

        metadata = dict(
            job.source_metadata or {}
        )

        # -------------------------------------------------
        # Store matching information
        # -------------------------------------------------

        metadata["matching"] = match_data

        # -------------------------------------------------
        # Explicitly preserve links
        # -------------------------------------------------

        metadata["job_url"] = job.job_url

        metadata["apply_url"] = (
            job.apply_url
            or job.job_url
        )

        # -------------------------------------------------
        # Create updated job
        # -------------------------------------------------

        matched_job = job.model_copy(
            update={
                "source_metadata": metadata,
            }
        )

        matched_jobs.append(
            matched_job
        )

    return matched_jobs