# Agent working agreement

## Repository map

- `src/investor/agents/`: agent loops, orchestration, and profile loading
- `src/investor/guardrails/`: policy checks applied before capabilities run
- `src/investor/skills/`: reusable instructions and capability declarations
- `src/investor/tools/`: local tool contracts and registry
- `src/investor/mcp/`: MCP adapters; transports belong behind `McpClient`
- `config/agents/`: declarative runtime profiles
- `.github/agents/` and `.github/skills/`: Copilot development agents and skills
- `apps/web/`: TypeScript research console

## Non-negotiable rules

1. Keep model providers, MCP transports, and domain logic behind protocols.
2. Authorize every tool invocation through `GuardrailPolicy`; do not bypass it.
3. Default new agents, tools, and MCP servers to no permissions.
4. Keep credentials in environment variables; never place values in config.
5. Bound agent loops and subagent fan-out.
6. Preserve evidence provenance and distinguish facts from inference.
7. Add focused tests for changed behavior and run `scripts/check.ps1` or its
   platform-equivalent commands before declaring work complete.
