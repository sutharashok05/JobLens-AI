from app.providers.registry import ProviderRegistry

from app.providers.adzuna.provider import AdzunaProvider
from app.providers.google.provider import GoogleProvider
#from app.providers.ats.provider import ATSProvider
#from app.providers.company_careers.provider import CompanyCareerProvider


provider_registry = ProviderRegistry()

provider_registry.register(
    AdzunaProvider()
)

provider_registry.register(
    GoogleProvider()
)

# provider_registry.register(
#     ATSProvider()
# )

# provider_registry.register(
#     CompanyCareerProvider()
# )