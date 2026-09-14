from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyATS:
    company: str
    ats: str
    identifier: str
    category: str
    size: str
    priority: int = 1


# =========================================================
# COMPANY ATS REGISTRY
# =========================================================
#
# identifier:
#   Greenhouse -> board token
#   Lever      -> site/account slug
#   Ashby      -> job board name
#
# priority:
#   1 = high
#   2 = medium
#   3 = lower
#
# Add more companies here as they are verified.
# =========================================================

COMPANY_ATS_REGISTRY: list[CompanyATS] = [

    # =====================================================
    # ASHBY
    # =====================================================

    CompanyATS(
        company="Sarvam",
        ats="ashby",
        identifier="sarvam",
        category="ai_startup",
        size="startup",
        priority=1,
    ),

    CompanyATS(
        company="Ema",
        ats="ashby",
        identifier="ema",
        category="ai_startup",
        size="startup",
        priority=1,
    ),

    # =====================================================
    # LEVER
    # =====================================================

    CompanyATS(
        company="Gushwork",
        ats="lever",
        identifier="gushwork",
        category="startup",
        size="startup",
        priority=1,
    ),

    CompanyATS(
        company="Level AI",
        ats="lever",
        identifier="levelai",
        category="ai_startup",
        size="startup",
        priority=1,
    ),

    CompanyATS(
        company="Neuron7",
        ats="lever",
        identifier="neuron7",
        category="ai_startup",
        size="startup",
        priority=1,
    ),

    CompanyATS(
        company="Acceldata",
        ats="lever",
        identifier="acceldata",
        category="product",
        size="medium",
        priority=1,
    ),

    CompanyATS(
        company="Saviynt",
        ats="lever",
        identifier="saviynt",
        category="product",
        size="large",
        priority=1,
    ),

    CompanyATS(
        company="Kobie",
        ats="lever",
        identifier="kobie",
        category="product",
        size="medium",
        priority=2,
    ),

    # =====================================================
    # GREENHOUSE
    # =====================================================
    #
    # Add verified Greenhouse board tokens here.
    #
    # Example:
    #
    # CompanyATS(
    #     company="Company Name",
    #     ats="greenhouse",
    #     identifier="greenhouse-board-token",
    #     category="product",
    #     size="medium",
    #     priority=1,
    # ),
]


# =========================================================
# REGISTRY HELPERS
# =========================================================

def get_registry() -> list[CompanyATS]:
    """
    Return all registered companies.
    """
    return list(COMPANY_ATS_REGISTRY)


def get_companies_by_ats(
    ats: str,
) -> list[CompanyATS]:
    """
    Return companies using a specific ATS.
    """
    ats = ats.strip().lower()

    return [
        company
        for company in COMPANY_ATS_REGISTRY
        if company.ats.lower() == ats
    ]


def get_company(
    company_name: str,
) -> CompanyATS | None:
    """
    Find a company by display name.
    """
    company_name = company_name.strip().lower()

    for company in COMPANY_ATS_REGISTRY:
        if company.company.lower() == company_name:
            return company

    return None


def get_companies_by_category(
    category: str,
) -> list[CompanyATS]:
    """
    Return companies belonging to a category.
    """
    category = category.strip().lower()

    return [
        company
        for company in COMPANY_ATS_REGISTRY
        if company.category.lower() == category
    ]


def get_companies_by_size(
    size: str,
) -> list[CompanyATS]:
    """
    Return companies by size.
    """
    size = size.strip().lower()

    return [
        company
        for company in COMPANY_ATS_REGISTRY
        if company.size.lower() == size
    ]