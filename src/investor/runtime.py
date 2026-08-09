from dataclasses import dataclass

from investor.agents.orchestrator import AgentOrchestrator
from investor.agents.profiles import load_profiles
from investor.agents.research import ResearchAgent
from investor.config import Settings, get_settings
from investor.guardrails import GuardrailPolicy
from investor.mcp.config import load_mcp_config, reject_unconfigured_servers
from investor.providers import DevelopmentProvider, ModelProvider
from investor.skills import SkillRegistry
from investor.skills.builtin import built_in_skills
from investor.tools import ToolRegistry
from investor.tools.graham_checklist import GrahamChecklistTool


@dataclass(frozen=True, slots=True)
class Runtime:
    orchestrator: AgentOrchestrator
    skills: SkillRegistry
    tools: ToolRegistry


def create_runtime(
    *,
    settings: Settings | None = None,
    provider: ModelProvider | None = None,
    tools: ToolRegistry | None = None,
) -> Runtime:
    active_settings = settings or get_settings()
    active_provider = provider or DevelopmentProvider()
    active_tools = tools or ToolRegistry((GrahamChecklistTool(),))
    reject_unconfigured_servers(load_mcp_config(active_settings.mcp_config_path))
    skills = SkillRegistry(built_in_skills())
    profiles = load_profiles(active_settings.agent_config_dir)
    policy = GuardrailPolicy(
        max_query_length=active_settings.max_query_length,
        max_subagents=active_settings.max_subagents,
    )

    def make_agent(name: str) -> ResearchAgent:
        try:
            profile = profiles[name]
        except KeyError as error:
            raise LookupError(f"Agent '{name}' is not configured.") from error
        skills.validate_requirements(
            skill_names=profile.allowed_skills,
            allowed_tools=profile.allowed_tools,
        )
        active_tools.descriptors(profile.allowed_tools)
        return ResearchAgent(
            profile=profile,
            provider=active_provider,
            tools=active_tools,
            skills=skills,
            policy=policy,
        )

    agents = {name: make_agent(name) for name in profiles}
    return Runtime(
        orchestrator=AgentOrchestrator(
            agents=agents,
            policy=policy,
            agent_factory=make_agent,
        ),
        skills=skills,
        tools=active_tools,
    )
