# Agent development

## Add an agent

Run `investor new-agent <name>`. The generated profile has no tools, no MCP
servers, a bounded step count, and delegation disabled. Tighten its prompt to a
single responsibility before assigning skills.

## Add a skill

Skills are reusable instructions, not unrestricted executable plugins. Define
the skill in `src/investor/skills/`, register it at composition time, declare
required tools, and test its prompt contribution.

## Add a tool

Implement the `Tool` protocol with a stable name, JSON-compatible input schema,
and typed `ToolResult`. Register the tool, then explicitly add its name to the
profiles that require it. Return `is_error=True` for operational failures;
the agent loop surfaces these failures.

## Add an MCP server

1. Implement or select an authenticated `McpClient` transport adapter.
2. Add a disabled, credential-free server entry based on the MCP example.
3. Register selected remote operations as `McpTool` instances.
4. Add the tool name and server name to only the necessary profiles.
5. Test denial of both the tool and server independently.

Do not dynamically expose every tool advertised by a server.

## Add a model provider

Implement `ModelProvider.complete`. Convert provider-specific messages and tool
calls only inside the adapter. Enforce request timeouts and surface provider
errors; do not return fabricated successful research.

## Validation

```bash
ruff check .
mypy
pytest
cd apps/web && npm run build
```
