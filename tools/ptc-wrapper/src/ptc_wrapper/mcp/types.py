"""MCP protocol types."""

from typing import Any, Literal
from pydantic import BaseModel, Field


class MCPToolSchema(BaseModel):
    """JSON Schema for tool input."""

    type: Literal["object"] = "object"
    properties: dict[str, Any] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)


class MCPTool(BaseModel):
    """MCP tool definition."""

    name: str
    description: str = ""
    inputSchema: MCPToolSchema = Field(default_factory=MCPToolSchema)


class MCPRequest(BaseModel):
    """JSON-RPC request to MCP server."""

    jsonrpc: Literal["2.0"] = "2.0"
    id: int
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    """JSON-RPC response from MCP server."""

    jsonrpc: Literal["2.0"] = "2.0"
    id: int
    result: Any | None = None
    error: dict[str, Any] | None = None


class MCPNotification(BaseModel):
    """JSON-RPC notification (no id)."""

    jsonrpc: Literal["2.0"] = "2.0"
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class TextContent(BaseModel):
    """Text content from tool result."""

    type: Literal["text"] = "text"
    text: str


class MCPToolResult(BaseModel):
    """Result from calling an MCP tool."""

    content: list[TextContent] = Field(default_factory=list)
    isError: bool = False
