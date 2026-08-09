from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RunStatus(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    REJECTED = "rejected"


class ChatRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ChatMessage(BaseModel):
    role: ChatRole
    content: str
    name: str | None = None
    tool_call_id: str | None = None


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolDescriptor(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    mcp_server: str | None = None


class ToolResult(BaseModel):
    content: str
    is_error: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProviderRequest(BaseModel):
    messages: tuple[ChatMessage, ...]
    tools: tuple[ToolDescriptor, ...] = ()


class ProviderResponse(BaseModel):
    content: str = ""
    tool_calls: tuple[ToolCall, ...] = ()
    is_final: bool = True


class Evidence(BaseModel):
    source: str
    content: str
    tool: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentProfile(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    system_prompt: str
    allowed_skills: tuple[str, ...] = ()
    allowed_tools: tuple[str, ...] = ()
    allowed_mcp_servers: tuple[str, ...] = ()
    max_steps: int = Field(default=6, ge=1, le=30)
    can_delegate: bool = False


class ResearchRequest(BaseModel):
    query: str
    agent: str = "research-lead"
    subagents: tuple[str, ...] = ()


class AgentRun(BaseModel):
    agent: str
    summary: str
    evidence: tuple[Evidence, ...] = ()
    steps: int = 0
    status: RunStatus = RunStatus.COMPLETED


class ResearchReport(BaseModel):
    query: str
    summary: str
    runs: tuple[AgentRun, ...]
    status: RunStatus
