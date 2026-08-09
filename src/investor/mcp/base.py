from typing import Any, Protocol

from investor.domain.models import ToolDescriptor, ToolResult


class McpClient(Protocol):
    async def call_tool(
        self, *, server: str, tool: str, arguments: dict[str, Any]
    ) -> ToolResult: ...


class McpTool:
    def __init__(
        self,
        *,
        client: McpClient,
        server: str,
        name: str,
        remote_name: str,
        description: str,
        input_schema: dict[str, Any] | None = None,
    ) -> None:
        self._client = client
        self._remote_name = remote_name
        self.descriptor = ToolDescriptor(
            name=name,
            description=description,
            input_schema=input_schema or {},
            mcp_server=server,
        )

    async def invoke(self, arguments: dict[str, Any]) -> ToolResult:
        server = self.descriptor.mcp_server
        if server is None:
            raise RuntimeError("MCP tool is missing its server identifier.")
        return await self._client.call_tool(
            server=server,
            tool=self._remote_name,
            arguments=arguments,
        )
