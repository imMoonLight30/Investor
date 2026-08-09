from typing import Any

from investor.agents.research import ResearchAgent
from investor.domain.models import (
    AgentProfile,
    ProviderRequest,
    ProviderResponse,
    ToolCall,
    ToolDescriptor,
    ToolResult,
)
from investor.guardrails import GuardrailPolicy
from investor.skills import Skill, SkillRegistry
from investor.tools import ToolRegistry


class StubProvider:
    def __init__(self) -> None:
        self.requests: list[ProviderRequest] = []

    async def complete(self, request: ProviderRequest) -> ProviderResponse:
        self.requests.append(request)
        if len(self.requests) == 1:
            return ProviderResponse(
                content="I need evidence.",
                tool_calls=(ToolCall(id="call-1", name="search", arguments={"q": "moat"}),),
                is_final=False,
            )
        return ProviderResponse(content="The evidence supports a cautious conclusion.")


class SearchTool:
    descriptor = ToolDescriptor(name="search", description="Search approved sources")

    async def invoke(self, arguments: dict[str, Any]) -> ToolResult:
        return ToolResult(
            content=f"Result for {arguments['q']}",
            metadata={"source": "test-primary-source"},
        )


async def test_agent_authorizes_tools_and_preserves_evidence() -> None:
    provider = StubProvider()
    agent = ResearchAgent(
        profile=AgentProfile(
            name="analyst",
            description="Test analyst",
            system_prompt="Use evidence.",
            allowed_skills=("quality",),
            allowed_tools=("search",),
            max_steps=3,
        ),
        provider=provider,
        tools=ToolRegistry((SearchTool(),)),
        skills=SkillRegistry(
            (
                Skill(
                    name="quality",
                    description="Quality",
                    instructions="Prefer primary evidence.",
                ),
            )
        ),
        policy=GuardrailPolicy(max_query_length=100, max_subagents=2),
    )

    run = await agent.run("Assess the moat")

    assert run.summary == "The evidence supports a cautious conclusion."
    assert run.steps == 2
    assert run.evidence[0].source == "test-primary-source"
    assert "Prefer primary evidence." in provider.requests[0].messages[0].content
    assistant_message = provider.requests[1].messages[2]
    assert assistant_message.tool_calls[0].id == "call-1"
    assert assistant_message.tool_calls[0].name == "search"
    assert assistant_message.tool_calls[0].arguments == {"q": "moat"}
