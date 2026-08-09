import asyncio
from collections.abc import Callable

from investor.agents.research import ResearchAgent
from investor.domain.models import ResearchReport, ResearchRequest, RunStatus
from investor.guardrails import GuardrailPolicy


class AgentOrchestrator:
    def __init__(
        self,
        *,
        agents: dict[str, ResearchAgent],
        policy: GuardrailPolicy,
        agent_factory: Callable[[str], ResearchAgent],
    ) -> None:
        self._agents = agents
        self._policy = policy
        self._agent_factory = agent_factory

    def agent_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._agents))

    async def research(self, request: ResearchRequest) -> ResearchReport:
        try:
            lead = self._agents[request.agent]
        except KeyError as error:
            raise LookupError(f"Agent '{request.agent}' is not configured.") from error

        self._policy.validate_subagents(lead.profile, request.subagents)
        selected = (request.agent, *request.subagents)
        selected_agents = tuple(self._agent_factory(name) for name in selected)
        runs = await asyncio.gather(*(agent.run(request.query) for agent in selected_agents))
        status = (
            RunStatus.COMPLETED
            if all(run.status == RunStatus.COMPLETED for run in runs)
            else RunStatus.PARTIAL
        )
        summary = "\n\n".join(f"## {run.agent}\n{run.summary}" for run in runs)
        return ResearchReport(
            query=request.query,
            summary=summary,
            runs=tuple(runs),
            status=status,
        )
