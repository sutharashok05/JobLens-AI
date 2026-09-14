from datetime import datetime, timezone

from app.schemas.job import JobResult


# ---------------------------------------------------------
# SCORE HELPERS
# ---------------------------------------------------------

def get_match_score(job: JobResult) -> float:
    matching = (job.source_metadata or {}).get("matching", {})
    return float(matching.get("match_score", 0))


def get_skill_match_score(job: JobResult) -> float:
    matching = (job.source_metadata or {}).get("matching", {})
    return float(matching.get("skill_match_score", 0))


def get_role_match_score(job: JobResult) -> float:
    matching = (job.source_metadata or {}).get("matching", {})
    return float(matching.get("role_match_score", 0))


def get_location_match_score(job: JobResult) -> float:
    matching = (job.source_metadata or {}).get("matching", {})
    return float(matching.get("location_match_score", 0))


# ---------------------------------------------------------
# VERIFICATION SCORE
# ---------------------------------------------------------

def get_verification_score(job: JobResult) -> float:
    verification = (
        (job.source_metadata or {})
        .get("verification", {})
    )

    verified = verification.get("verified")

    if verified is True:
        return 100.0

    if verified is False:
        return 0.0

    return 50.0


# ---------------------------------------------------------
# FRESHNESS SCORE
# ---------------------------------------------------------

def get_freshness_score(job: JobResult) -> float:

    # Adzuna normally provides actual posted_at
    if job.posted_at:

        posted = job.posted_at

        if posted.tzinfo is None:
            posted = posted.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        age_days = max(
            0,
            (now - posted).total_seconds()
            / 86400,
        )

        if age_days <= 1:
            return 100.0

        if age_days <= 3:
            return 90.0

        if age_days <= 7:
            return 75.0

        if age_days <= 14:
            return 50.0

        if age_days <= 30:
            return 25.0

        return 10.0

    # Google Jobs often stores relative
    # posting information in metadata.
    metadata = job.source_metadata or {}

    posted_text = str(
        metadata.get("posted_at", "")
    ).lower()

    if not posted_text:
        return 50.0

    if "today" in posted_text:
        return 100.0

    if "hour" in posted_text:
        return 100.0

    if "day" in posted_text:

        try:
            days = int(
                posted_text.split()[0]
            )

            if days <= 1:
                return 100.0

            if days <= 3:
                return 90.0

            if days <= 7:
                return 75.0

            if days <= 14:
                return 50.0

            return 25.0

        except (ValueError, IndexError):
            return 50.0

    if "week" in posted_text:
        return 25.0

    if "month" in posted_text:
        return 10.0

    return 50.0


# ---------------------------------------------------------
# SOURCE QUALITY
# ---------------------------------------------------------

def get_source_score(job: JobResult) -> float:

    source = job.source.lower()

    scores = {
        "company_careers": 100.0,
        "ats": 95.0,
        "google": 90.0,
        "adzuna": 85.0,
    }

    return scores.get(
        source,
        50.0,
    )


# ---------------------------------------------------------
# FINAL RANKING SCORE
# ---------------------------------------------------------

def calculate_ranking_score(
    job: JobResult,
) -> float:

    match_score = get_match_score(job)
    skill_score = get_skill_match_score(job)
    role_score = get_role_match_score(job)
    location_score = get_location_match_score(job)

    verification_score = get_verification_score(job)
    freshness_score = get_freshness_score(job)
    source_score = get_source_score(job)

    # -----------------------------------------------------
    # Weighted ranking
    # -----------------------------------------------------

    final_score = (
        match_score * 0.50
        + skill_score * 0.20
        + role_score * 0.10
        + location_score * 0.05
        + freshness_score * 0.05
        + verification_score * 0.05
        + source_score * 0.05
    )

    return round(
        min(final_score, 100.0),
        2,
    )


# ---------------------------------------------------------
# RANK JOBS
# ---------------------------------------------------------

def rank_jobs(
    jobs: list[JobResult],
) -> list[JobResult]:

    ranked_jobs = []

    for job in jobs:

        ranking_score = calculate_ranking_score(
            job
        )

        metadata = dict(
            job.source_metadata or {}
        )

        metadata["ranking"] = {
            "ranking_score": ranking_score,
            "match_score": get_match_score(job),
            "skill_score": get_skill_match_score(job),
            "role_score": get_role_match_score(job),
            "location_score": get_location_match_score(job),
            "verification_score": get_verification_score(job),
            "freshness_score": get_freshness_score(job),
            "source_score": get_source_score(job),
        }

        ranked_job = job.model_copy(
            update={
                "source_metadata": metadata
            }
        )

        ranked_jobs.append(ranked_job)

    # Highest ranking first
    ranked_jobs.sort(
        key=lambda job: (
            (job.source_metadata or {})
            .get("ranking", {})
            .get("ranking_score", 0)
        ),
        reverse=True,
    )

    return ranked_jobs