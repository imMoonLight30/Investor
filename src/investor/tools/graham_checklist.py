from typing import Any

from investor.domain.models import ToolDescriptor, ToolResult

_MISTAKES: tuple[dict[str, str], ...] = (
    {
        "id": "speculation-vs-investing",
        "mistake": "Confusing speculation with investing",
        "lesson": (
            "An investment requires thorough analysis, safety of principal, and an adequate "
            "return; anything short of that is speculation. Cap speculative bets at roughly "
            "10% of a portfolio and keep them separate from core holdings."
        ),
    },
    {
        "id": "mr-market",
        "mistake": "Letting the market control your emotions",
        "lesson": (
            "Treat market quotes as offers from a moody counterparty (Mr. Market), not a "
            "verdict on business value. The market is a voting machine in the short run and a "
            "weighing machine in the long run."
        ),
    },
    {
        "id": "following-the-crowd",
        "mistake": "Following the crowd",
        "lesson": (
            "Watch for bubble signals: historic-high prices, low dividend yields, heavy use of "
            "borrowed money, weak new issues, and widespread public enthusiasm. Value businesses "
            "independently of prevailing sentiment."
        ),
    },
    {
        "id": "overpaying-for-quality",
        "mistake": "Overpaying for quality",
        "lesson": (
            "Price is a function of both business fundamentals and market expectations. Even a "
            "wonderful business can destroy capital if the price already assumes flawless future "
            "growth."
        ),
    },
    {
        "id": "ignoring-diversification",
        "mistake": "Ignoring diversification",
        "lesson": (
            "Concentrated bets expose an investor to catastrophic single-company risk. Favor "
            "roughly 10-30 positions spread across industries and economic sectors."
        ),
    },
    {
        "id": "margin-of-safety",
        "mistake": "Forgetting the margin of safety",
        "lesson": (
            "Buy with a cushion between estimated intrinsic value and price paid to absorb "
            "analytical errors and unforeseen events; the margin of safety is Graham's master "
            "concept."
        ),
    },
)


class GrahamChecklistTool:
    """Deterministic, offline reference to Benjamin Graham's six investing mistakes.

    Returns structured educational content only; it makes no external calls
    and never recommends buying or selling a specific security.
    """

    descriptor = ToolDescriptor(
        name="graham-checklist",
        description=(
            "Retrieve Benjamin Graham's six timeless investing mistakes and principles, "
            "optionally filtered by topic id."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Optional mistake id to filter to a single entry.",
                }
            },
        },
    )

    async def invoke(self, arguments: dict[str, Any]) -> ToolResult:
        topic = arguments.get("topic")
        entries = _MISTAKES
        if topic:
            entries = tuple(entry for entry in _MISTAKES if entry["id"] == topic)
            if not entries:
                return ToolResult(
                    content=f"No Graham checklist entry found for topic '{topic}'.",
                    is_error=True,
                )
        lines = [f"{entry['mistake']}: {entry['lesson']}" for entry in entries]
        return ToolResult(
            content="\n".join(lines),
            metadata={"source": "benjamin-graham-six-mistakes", "count": len(entries)},
        )
