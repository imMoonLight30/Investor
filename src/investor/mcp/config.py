import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class McpServerConfig(BaseModel):
    enabled: bool = False
    transport: Literal["stdio", "http"]
    command: str | None = None
    args: tuple[str, ...] = ()
    url: str | None = None
    env: dict[str, str] = Field(default_factory=dict)
    allowed_tools: tuple[str, ...] = Field(default=(), alias="allowedTools")


class McpConfig(BaseModel):
    servers: dict[str, McpServerConfig]


def load_mcp_config(path: Path) -> McpConfig:
    if not path.is_file():
        raise FileNotFoundError(f"MCP configuration file does not exist: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return McpConfig.model_validate(payload)


def reject_unconfigured_servers(config: McpConfig) -> None:
    enabled = sorted(name for name, server in config.servers.items() if server.enabled)
    if enabled:
        names = ", ".join(f"'{name}'" for name in enabled)
        raise RuntimeError(
            f"Enabled MCP servers have no transport adapter registered: {names}. "
            "Inject concrete McpTool instances into the runtime before enabling them."
        )
