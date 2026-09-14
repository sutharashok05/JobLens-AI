from app.providers.base import JobSearchProvider


class ProviderRegistry:
    """
    Central registry for all job search providers.
    """

    def __init__(self):
        self._providers: dict[str, JobSearchProvider] = {}

    def register(
        self,
        provider: JobSearchProvider,
    ) -> None:
        self._providers[provider.name] = provider

    def get(
        self,
        name: str,
    ) -> JobSearchProvider | None:
        return self._providers.get(name)

    def all(self) -> list[JobSearchProvider]:
        return list(self._providers.values())

    def names(self) -> list[str]:
        return list(self._providers.keys())