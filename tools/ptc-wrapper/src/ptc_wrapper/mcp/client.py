"""MCP client for stdio communication with MCP servers."""

import asyncio
import json
import os
import sys
from typing import Any

from ptc_wrapper.mcp.types import MCPRequest, MCPResponse, MCPTool, MCPToolResult


class MCPClient:
    """Client for communicating with MCP servers via stdio."""

    def __init__(
        self,
        command: str,
        args: list[str],
        env: dict[str, str] | None = None,
        name: str = "unknown",
    ):
        """Initialize MCP client.

        Args:
            command: Command to run (e.g., "python", "npx")
            args: Arguments for the command
            env: Environment variables (merged with current env)
            name: Server name for logging
        """
        self.command = command
        self.args = args
        self.env = {**os.environ, **(env or {})}
        self.name = name
        self.process: asyncio.subprocess.Process | None = None
        self.tools: dict[str, MCPTool] = {}
        self._request_id = 0
        self._connected = False

    async def connect(self) -> None:
        """Start MCP server process and initialize connection."""
        if self._connected:
            return

        # Resolve command path on Windows
        resolved_command = self.command
        if sys.platform == "win32" and self.command in ("python", "python3"):
            resolved_command = sys.executable

        self.process = await asyncio.create_subprocess_exec(
            resolved_command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.env,
        )

        # Send initialize request
        await self._send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ptc-wrapper", "version": "0.1.0"},
            },
        )

        # Send initialized notification
        await self._send_notification("notifications/initialized", {})

        # Fetch available tools
        response = await self._send_request("tools/list", {})
        tools_data = response.get("tools", [])

        for tool_data in tools_data:
            tool = MCPTool(
                name=tool_data["name"],
                description=tool_data.get("description", ""),
                inputSchema=tool_data.get("inputSchema", {"type": "object"}),
            )
            self.tools[tool.name] = tool

        self._connected = True

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> MCPToolResult:
        """Call an MCP tool and return the result.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            MCPToolResult with content or error
        """
        if not self._connected:
            await self.connect()

        response = await self._send_request(
            "tools/call", {"name": name, "arguments": arguments}
        )

        # Parse response into MCPToolResult
        content = response.get("content", [])
        is_error = response.get("isError", False)

        return MCPToolResult(content=content, isError=is_error)

    async def list_tools(self) -> list[MCPTool]:
        """List all available tools.

        Returns:
            List of MCPTool definitions
        """
        if not self._connected:
            await self.connect()

        return list(self.tools.values())

    async def _send_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Send JSON-RPC request to MCP server.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            Result from server response
        """
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("MCP server not connected")

        self._request_id += 1
        request = MCPRequest(id=self._request_id, method=method, params=params)

        # Send request
        request_json = request.model_dump_json()
        self.process.stdin.write(request_json.encode() + b"\n")
        await self.process.stdin.drain()

        # Read response
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError(f"MCP server {self.name} closed connection")

        response_data = json.loads(response_line.decode())
        response = MCPResponse(**response_data)

        if response.error:
            raise RuntimeError(
                f"MCP error from {self.name}: {response.error.get('message', 'Unknown error')}"
            )

        return response.result or {}

    async def _send_notification(self, method: str, params: dict[str, Any]) -> None:
        """Send JSON-RPC notification (no response expected).

        Args:
            method: RPC method name
            params: Method parameters
        """
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP server not connected")

        notification = {"jsonrpc": "2.0", "method": method, "params": params}
        notification_json = json.dumps(notification)
        self.process.stdin.write(notification_json.encode() + b"\n")
        await self.process.stdin.drain()

    async def close(self) -> None:
        """Terminate MCP server process."""
        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
            self.process = None
            self._connected = False

    async def __aenter__(self) -> "MCPClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
