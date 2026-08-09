---
name: create-research-skill
description: Add a reusable, guarded research skill to the platform.
---

1. Define a narrow `Skill` in `src/investor/skills/` with clear instructions
   and an explicit `required_tools` tuple.
2. Register it in the runtime registry.
3. Add it only to agent profiles that need it.
4. If tools are required, register typed implementations and add each tool to
   the profile allowlist. MCP tools also require a server allowlist entry.
5. Add tests for registration, prompt composition, and denied capabilities.
6. Update `docs/agent-development.md` when the extension pattern changes.
7. Run Ruff, mypy, and focused pytest tests.
