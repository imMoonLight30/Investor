import json
from pathlib import Path

import pytest

from investor.config import Settings
from investor.skills import Skill, SkillRegistry
from investor.tools import ToolRegistry


def test_tool_registry_rejects_missing_allowed_tools() -> None:
    registry = ToolRegistry()

    with pytest.raises(LookupError, match="'search'"):
        registry.descriptors(("search",))


def test_skill_registry_rejects_missing_required_tool_permission() -> None:
    registry = SkillRegistry(
        (
            Skill(
                name="web-research",
                description="Research the web",
                instructions="Search approved sources.",
                required_tools=("search",),
            ),
        )
    )

    with pytest.raises(ValueError, match="requires tools"):
        registry.validate_requirements(
            skill_names=("web-research",),
            allowed_tools=(),
        )


def test_runtime_rejects_enabled_mcp_server_without_adapter(tmp_path: Path) -> None:
    from investor.runtime import create_runtime

    config_path = tmp_path / "mcp.json"
    config_path.write_text(
        json.dumps(
            {
                "servers": {
                    "external-search": {
                        "enabled": True,
                        "transport": "http",
                        "url": "https://example.invalid/mcp",
                        "allowedTools": ["search"],
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(
        agent_config_dir=Path("config/agents"),
        mcp_config_path=config_path,
    )

    with pytest.raises(RuntimeError, match="no transport adapter"):
        create_runtime(settings=settings)
