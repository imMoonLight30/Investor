# Investor Research Agents

A provider-neutral platform for running guarded research agents and subagents.
It provides typed Python contracts for model providers, tools, skills, MCP
adapters, agent profiles, and orchestration, plus a FastAPI service and a small
TypeScript web console.

## What is included

- Declarative agent profiles in `config/agents/`
- Deny-by-default tool and MCP authorization
- Bounded agent loops and subagent fan-out
- Pluggable model-provider, skill, tool, and MCP interfaces
- FastAPI and Typer entry points
- TypeScript/HTML research console
- Python and PowerShell developer scripts
- Copilot repository instructions, custom agents, and reusable skills
- Ruff, mypy, pytest, frontend builds, and GitHub Actions CI

The default `development` model provider is deterministic and makes no external
calls. Add a provider adapter before using the platform for live research.

## Quick start

### macOS/Linux

```bash
python scripts/bootstrap.py
source .venv/bin/activate
investor check
investor serve
```

### PowerShell

```powershell
./scripts/bootstrap.ps1
./scripts/check.ps1
investor serve
```

Open `http://localhost:8000/docs` for the API. To run the web console:

```bash
cd apps/web
npm install
npm run dev
```

Copy `.env.example` to `.env` to customize local settings. Never commit API
keys or credentials.

## Core concepts

1. **Agent profiles** define prompts, budgets, and allowed capabilities.
2. **Skills** add reusable instructions and declare required tools.
3. **Tools** perform local work; MCP adapters expose remote tools through the
   same registry.
4. **Guardrails** validate inputs and authorize every tool/MCP invocation.
5. **Providers** decide whether to return a final response or request tools.
6. **Orchestrators** run a primary agent or a bounded set of subagents.

See [Architecture](docs/architecture.md) and
[Agent development](docs/agent-development.md) for extension guides.

## Commands

```bash
investor check
investor agents
investor skills
investor research "Assess the durable advantages of a company"
investor research "Should I chase a hot IPO?" --agent graham-mentor
investor serve --reload
```

## Learn investing with the Graham mentor agent

The `graham-mentor` profile ([config/agents/graham-mentor.yaml](config/agents/graham-mentor.yaml))
is a dedicated teaching agent built around Benjamin Graham's six timeless
investing mistakes (speculation vs. investing, Mr. Market, following the
crowd, overpaying for quality, diversification, and the margin of safety). It
combines:

- The `graham-principles` skill
  ([src/investor/skills/builtin.py](src/investor/skills/builtin.py)), which
  encodes the six-mistakes checklist and the defensive vs. enterprising
  investor distinction as reusable instructions.
- The `graham-checklist` tool
  ([src/investor/tools/graham_checklist.py](src/investor/tools/graham_checklist.py)),
  a deterministic, offline reference the agent can call to retrieve or filter
  the six mistakes without any external network access.

This agent is for education only: it explains concepts and screens
user-described situations against Graham's framework, but it never
recommends buying or selling a specific security.

## Status

This repository is an extensible development foundation, not investment advice.
All live providers, tools, and MCP servers must be explicitly configured and
approved for the environment in which they run.
