# Copilot repository instructions

This is a Python-first, provider-neutral research-agent platform with a
TypeScript web console.

- Read `AGENTS.md` and the relevant architecture document before changing core
  agent behavior.
- Keep the dependency direction:
  `domain <- skills/tools/guardrails/providers <- agents <- runtime <- API/CLI`.
- New capabilities must implement an existing protocol or add a narrow,
  well-tested protocol. Do not couple core agents directly to an SDK.
- Tool and MCP access is deny-by-default. Update an agent profile only when the
  capability is necessary, and add a policy test.
- Never log prompts containing credentials or place secrets in fixtures.
- Prefer primary-source evidence and preserve source metadata in `Evidence`.
- Run Ruff, mypy, pytest, and the web build for cross-cutting changes.
