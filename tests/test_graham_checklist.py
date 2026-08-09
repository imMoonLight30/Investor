import pytest

from investor.tools.graham_checklist import GrahamChecklistTool


async def test_graham_checklist_returns_all_six_mistakes() -> None:
    tool = GrahamChecklistTool()

    result = await tool.invoke({})

    assert not result.is_error
    assert result.metadata["count"] == 6
    assert "margin of safety" in result.content.lower()
    assert "speculation" in result.content.lower()


async def test_graham_checklist_filters_by_topic() -> None:
    tool = GrahamChecklistTool()

    result = await tool.invoke({"topic": "margin-of-safety"})

    assert not result.is_error
    assert result.metadata["count"] == 1
    assert "Forgetting the margin of safety" in result.content


async def test_graham_checklist_reports_unknown_topic() -> None:
    tool = GrahamChecklistTool()

    result = await tool.invoke({"topic": "unknown"})

    assert result.is_error


@pytest.mark.parametrize("topic_id", [
    "speculation-vs-investing",
    "mr-market",
    "following-the-crowd",
    "overpaying-for-quality",
    "ignoring-diversification",
    "margin-of-safety",
])
async def test_graham_checklist_every_topic_resolves(topic_id: str) -> None:
    tool = GrahamChecklistTool()

    result = await tool.invoke({"topic": topic_id})

    assert not result.is_error
    assert result.metadata["count"] == 1
