from typing import Protocol

from investor.domain.models import ProviderRequest, ProviderResponse


class ModelProvider(Protocol):
    async def complete(self, request: ProviderRequest) -> ProviderResponse:
        """Return a final response or one or more requested tool calls."""


class DevelopmentProvider:
    """Offline provider used to validate orchestration without external calls."""

    async def complete(self, request: ProviderRequest) -> ProviderResponse:
        query = next(
            (message.content for message in reversed(request.messages) if message.role == "user"),
            "",
        )
        return ProviderResponse(
            content=(
                "Development provider received the research task: "
                f"{query}. Configure a live model provider and approved tools "
                "to collect and synthesize external evidence."
            )
        )
