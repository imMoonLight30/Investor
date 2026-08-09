from investor.domain.models import AgentProfile, ToolDescriptor


class GuardrailViolation(ValueError):
    """Raised when input or a capability request violates policy."""


class GuardrailPolicy:
    def __init__(self, *, max_query_length: int, max_subagents: int) -> None:
        self.max_query_length = max_query_length
        self.max_subagents = max_subagents

    def validate_query(self, query: str) -> str:
        normalized = query.strip()
        if not normalized:
            raise GuardrailViolation("Research query cannot be empty.")
        if len(normalized) > self.max_query_length:
            raise GuardrailViolation(
                f"Research query exceeds the {self.max_query_length}-character limit."
            )
        return normalized

    def validate_subagents(self, profile: AgentProfile, subagents: tuple[str, ...]) -> None:
        if subagents and not profile.can_delegate:
            raise GuardrailViolation(f"Agent '{profile.name}' is not allowed to delegate.")
        if len(subagents) > self.max_subagents:
            raise GuardrailViolation(
                f"Requested {len(subagents)} subagents; the limit is {self.max_subagents}."
            )
        if len(set(subagents)) != len(subagents):
            raise GuardrailViolation("Duplicate subagents are not allowed.")
        if profile.name in subagents:
            raise GuardrailViolation("The lead agent cannot also be selected as a subagent.")

    def authorize_tool(self, profile: AgentProfile, descriptor: ToolDescriptor) -> None:
        if descriptor.name not in profile.allowed_tools:
            raise GuardrailViolation(
                f"Agent '{profile.name}' is not allowed to use tool '{descriptor.name}'."
            )
        if (
            descriptor.mcp_server is not None
            and descriptor.mcp_server not in profile.allowed_mcp_servers
        ):
            raise GuardrailViolation(
                f"Agent '{profile.name}' is not allowed to use MCP server "
                f"'{descriptor.mcp_server}'."
            )
