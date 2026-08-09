import json

from investor.domain.models import (
    AgentProfile,
    AgentRun,
    ChatMessage,
    ChatRole,
    Evidence,
    ProviderRequest,
    RunStatus,
)
from investor.guardrails import GuardrailPolicy
from investor.providers import ModelProvider
from investor.skills import SkillRegistry
from investor.tools import ToolRegistry


class ResearchAgent:
    def __init__(
        self,
        *,
        profile: AgentProfile,
        provider: ModelProvider,
        tools: ToolRegistry,
        skills: SkillRegistry,
        policy: GuardrailPolicy,
    ) -> None:
        self.profile = profile
        self._provider = provider
        self._tools = tools
        self._skills = skills
        self._policy = policy

    async def run(self, query: str) -> AgentRun:
        normalized_query = self._policy.validate_query(query)
        skill_instructions = self._skills.instructions_for(self.profile.allowed_skills)
        system_prompt = self.profile.system_prompt
        if skill_instructions:
            system_prompt = f"{system_prompt}\n\nApplicable skills:\n{skill_instructions}"

        messages = [
            ChatMessage(role=ChatRole.SYSTEM, content=system_prompt),
            ChatMessage(role=ChatRole.USER, content=normalized_query),
        ]
        evidence: list[Evidence] = []
        descriptors = self._tools.descriptors(self.profile.allowed_tools)

        for step in range(1, self.profile.max_steps + 1):
            response = await self._provider.complete(
                ProviderRequest(messages=tuple(messages), tools=descriptors)
            )
            if response.is_final or not response.tool_calls:
                return AgentRun(
                    agent=self.profile.name,
                    summary=response.content,
                    evidence=tuple(evidence),
                    steps=step,
                )

            messages.append(
                ChatMessage(
                    role=ChatRole.ASSISTANT,
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )
            for call in response.tool_calls:
                tool = self._tools.get(call.name)
                self._policy.authorize_tool(self.profile, tool.descriptor)
                result = await tool.invoke(call.arguments)
                if result.is_error:
                    raise RuntimeError(f"Tool '{call.name}' failed: {result.content}")
                evidence.append(
                    Evidence(
                        source=str(result.metadata.get("source", call.name)),
                        content=result.content,
                        tool=call.name,
                        metadata=result.metadata,
                    )
                )
                messages.append(
                    ChatMessage(
                        role=ChatRole.TOOL,
                        name=call.name,
                        tool_call_id=call.id,
                        content=json.dumps(
                            {"content": result.content, "metadata": result.metadata},
                            sort_keys=True,
                        ),
                    )
                )

        return AgentRun(
            agent=self.profile.name,
            summary="The agent reached its step budget before producing a final response.",
            evidence=tuple(evidence),
            steps=self.profile.max_steps,
            status=RunStatus.PARTIAL,
        )
