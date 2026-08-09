# Architecture

## Dependency direction

```text
domain
  ^-- providers, tools, skills, guardrails, MCP contracts
        ^-- agents
              ^-- runtime
                    ^-- API and CLI
```

The core does not import a model vendor or MCP SDK. Concrete integrations
implement `ModelProvider`, `Tool`, or `McpClient` and are assembled by the
runtime composition root.

## Research execution

1. The API or CLI validates a `ResearchRequest`.
2. The orchestrator resolves the lead profile and validates delegation limits.
3. Each agent receives only the tools listed in its immutable profile.
4. A provider returns a final response or requests typed tool calls.
5. The policy authorizes every requested tool and, for MCP tools, its server.
6. Successful tool results become evidence and retain source metadata.
7. Execution stops on a final response or the profile's step budget.

Subagents run concurrently only after the lead profile is allowed to delegate.
The global fan-out limit applies before any task is scheduled.

## Security model

- Agent profiles, MCP servers, and tools start disabled or with empty allowlists.
- Environment variables carry credentials; committed config contains references
  only.
- A tool error terminates the run visibly. It is never converted into
  success-shaped evidence.
- MCP transports are intentionally not assumed by the core. Authenticate,
  authorize, time-limit, and audit them in a concrete adapter.
- This platform structures research; it does not provide financial advice.

## Extension points

- Model vendor: implement `ModelProvider` and inject it into `create_runtime`.
- Local capability: implement `Tool` and register it in `ToolRegistry`.
- MCP capability: implement `McpClient`, wrap remote tools with `McpTool`, and
  update both tool and server allowlists.
- Research method: add a `Skill` and assign it to selected profiles.
- Specialist: add a YAML profile under `config/agents/`.
