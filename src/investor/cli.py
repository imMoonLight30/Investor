from pathlib import Path
from typing import Annotated

import typer
import uvicorn
import yaml

from investor.config import get_settings
from investor.domain.models import ResearchRequest
from investor.runtime import create_runtime

app = typer.Typer(
    no_args_is_help=True,
    help="Develop and run guarded investor research agents.",
)


@app.command()
def check() -> None:
    """Validate local agent and MCP configuration."""
    settings = get_settings()
    runtime = create_runtime(settings=settings)
    typer.echo(
        f"Configuration valid: {len(runtime.orchestrator.agent_names())} agents, "
        f"{len(runtime.skills.names())} skills."
    )


@app.command()
def agents() -> None:
    """List configured agent profiles."""
    for name in create_runtime().orchestrator.agent_names():
        typer.echo(name)


@app.command()
def skills() -> None:
    """List registered skills."""
    for name in create_runtime().skills.names():
        typer.echo(name)


@app.command()
def research(
    query: Annotated[str, typer.Argument(help="Research question or task.")],
    agent: Annotated[str, typer.Option(help="Lead agent profile.")] = "research-lead",
    subagent: Annotated[
        list[str] | None,
        typer.Option("--subagent", help="Subagent profile; may be repeated."),
    ] = None,
) -> None:
    """Run a research task using the configured provider."""
    import asyncio

    runtime = create_runtime()
    report = asyncio.run(
        runtime.orchestrator.research(
            ResearchRequest(
                query=query,
                agent=agent,
                subagents=tuple(subagent or ()),
            )
        )
    )
    typer.echo(report.model_dump_json(indent=2))


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Bind address.")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port.")] = 8000,
    reload: Annotated[bool, typer.Option(help="Reload when files change.")] = False,
) -> None:
    """Start the FastAPI service."""
    uvicorn.run("investor.api:app", host=host, port=port, reload=reload)


@app.command("new-agent")
def new_agent(
    name: Annotated[str, typer.Argument(help="Kebab-case agent name.")],
    config_dir: Annotated[
        Path | None,
        typer.Option(help="Override the configured agent directory."),
    ] = None,
) -> None:
    """Create a deny-by-default agent profile."""
    valid_characters = "abcdefghijklmnopqrstuvwxyz0123456789-"
    if not name or any(character not in valid_characters for character in name):
        raise typer.BadParameter("Agent name must use lowercase letters, numbers, and hyphens.")
    directory = config_dir or get_settings().agent_config_dir
    path = directory / f"{name}.yaml"
    if path.exists():
        raise typer.BadParameter(f"Agent profile already exists: {path}")
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "name": name,
        "description": "Describe this agent's narrow responsibility.",
        "system_prompt": "Define the agent's evidence standards and expected output.",
        "allowed_skills": ["source-quality"],
        "allowed_tools": [],
        "allowed_mcp_servers": [],
        "max_steps": 6,
        "can_delegate": False,
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    typer.echo(f"Created {path}")
