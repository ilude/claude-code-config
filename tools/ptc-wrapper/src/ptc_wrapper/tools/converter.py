"""Convert MCP tools to PTC-compatible format."""

from typing import Any

from ptc_wrapper.mcp.types import MCPTool
from ptc_wrapper.tools.examples import generate_input_examples


CODE_EXECUTION_CALLER = "code_execution_20250825"


def convert_mcp_to_ptc(
    mcp_tool: MCPTool,
    allowed_callers: list[str] | None = None,
    include_examples: bool = True,
) -> dict[str, Any]:
    """Convert MCP tool definition to PTC-compatible format.

    Args:
        mcp_tool: MCP tool definition
        allowed_callers: List of allowed callers (defaults to code_execution)
        include_examples: Whether to auto-generate input examples

    Returns:
        PTC-compatible tool definition dict
    """
    if allowed_callers is None:
        allowed_callers = [CODE_EXECUTION_CALLER]

    ptc_tool: dict[str, Any] = {
        "name": mcp_tool.name,
        "description": mcp_tool.description,
        "input_schema": mcp_tool.inputSchema.model_dump(),
        "allowed_callers": allowed_callers,
    }

    if include_examples:
        examples = generate_input_examples(mcp_tool)
        if examples:
            ptc_tool["input_examples"] = examples

    return ptc_tool


def convert_all_tools(
    mcp_tools: list[MCPTool],
    allowed_callers: list[str] | None = None,
    include_examples: bool = True,
) -> list[dict[str, Any]]:
    """Convert all MCP tools to PTC format.

    Args:
        mcp_tools: List of MCP tool definitions
        allowed_callers: List of allowed callers
        include_examples: Whether to include input examples

    Returns:
        List of PTC-compatible tool definitions
    """
    return [
        convert_mcp_to_ptc(tool, allowed_callers, include_examples)
        for tool in mcp_tools
    ]


def get_code_execution_tool() -> dict[str, Any]:
    """Get the code_execution tool definition.

    Returns:
        Code execution tool for PTC
    """
    return {
        "type": CODE_EXECUTION_CALLER,
        "name": "code_execution",
    }
