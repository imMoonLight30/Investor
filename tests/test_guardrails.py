import pytest

from investor.domain.models import AgentProfile, ToolDescriptor
from investor.guardrails import GuardrailPolicy, GuardrailViolation


def profile(**overrides: object) -> AgentProfile:
    values: dict[str, object] = {
        "name": "test-agent",
        "description": "Test",
        "system_prompt": "Test",
        "allowed_tools": ("search",),
        "allowed_mcp_servers": (),
        "can_delegate": False,
    }
    values.update(overrides)
    return AgentProfile.model_validate(values)


def test_rejects_unapproved_tool() -> None:
    policy = GuardrailPolicy(max_query_length=100, max_subagents=2)

    with pytest.raises(GuardrailViolation, match="not allowed to use tool"):
        policy.authorize_tool(
            profile(),
            ToolDescriptor(name="filesystem", description="Read files"),
        )


def test_mcp_tool_requires_server_permission() -> None:
    policy = GuardrailPolicy(max_query_length=100, max_subagents=2)

    with pytest.raises(GuardrailViolation, match="MCP server"):
        policy.authorize_tool(
            profile(),
            ToolDescriptor(
                name="search",
                description="Search",
                mcp_server="external-search",
            ),
        )


def test_non_delegating_agent_cannot_spawn_subagents() -> None:
    policy = GuardrailPolicy(max_query_length=100, max_subagents=2)

    with pytest.raises(GuardrailViolation, match="not allowed to delegate"):
        policy.validate_subagents(profile(), ("risk-agent",))


def test_lead_agent_cannot_be_its_own_subagent() -> None:
    policy = GuardrailPolicy(max_query_length=100, max_subagents=2)

    with pytest.raises(GuardrailViolation, match="lead agent"):
        policy.validate_subagents(
            profile(can_delegate=True),
            ("test-agent",),
        )
