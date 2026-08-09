from collections.abc import Iterable
from typing import Any, Protocol

from investor.domain.models import ToolDescriptor, ToolResult


class Tool(Protocol):
    @property
    def descriptor(self) -> ToolDescriptor: ...

    async def invoke(self, arguments: dict[str, Any]) -> ToolResult: ...


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        name = tool.descriptor.name
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as error:
            raise LookupError(f"Tool '{name}' is not registered.") from error

    def descriptors(self, allowed: tuple[str, ...]) -> tuple[ToolDescriptor, ...]:
        missing = sorted(set(allowed).difference(self._tools))
        if missing:
            names = ", ".join(f"'{name}'" for name in missing)
            raise LookupError(f"Allowed tools are not registered: {names}.")
        return tuple(self._tools[name].descriptor for name in allowed)
