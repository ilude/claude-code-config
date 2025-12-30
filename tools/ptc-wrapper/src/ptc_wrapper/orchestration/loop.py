"""Agentic loop for PTC orchestration."""

import json
from typing import Any, Callable, Awaitable

from anthropic import Anthropic
from anthropic.types.beta import BetaMessage


# Type alias for tool executor function
ToolExecutor = Callable[[str, dict[str, Any]], Awaitable[Any]]


class AgenticLoop:
    """Handles the iterative tool-use loop for PTC."""

    BETA_HEADER = "advanced-tool-use-2025-11-20"
    CODE_EXECUTION_TYPE = "code_execution_20250825"

    def __init__(
        self,
        client: Anthropic,
        tool_executor: ToolExecutor,
        model: str = "claude-sonnet-4-5-20250929",
    ):
        """Initialize the agentic loop.

        Args:
            client: Anthropic API client
            tool_executor: Async function to execute tools (name, args) -> result
            model: Model to use
        """
        self.client = client
        self.tool_executor = tool_executor
        self.model = model

    async def run(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system: str | None = None,
        max_iterations: int = 50,
        max_tokens: int = 4096,
    ) -> BetaMessage:
        """Run the agentic loop until completion or max iterations.

        Args:
            messages: Initial conversation messages
            tools: PTC-compatible tool definitions
            system: Optional system prompt
            max_iterations: Maximum tool-use iterations
            max_tokens: Max tokens per response

        Returns:
            Final response message
        """
        # Add code_execution tool to the list
        all_tools = [
            {"type": self.CODE_EXECUTION_TYPE, "name": "code_execution"},
            *tools,
        ]

        # Build request kwargs
        request_kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
            "tools": all_tools,
            "betas": [self.BETA_HEADER],
        }
        if system:
            request_kwargs["system"] = system

        iteration = 0
        while iteration < max_iterations:
            # Make API call
            response = self.client.beta.messages.create(**request_kwargs)

            # Check if we're done
            if response.stop_reason == "end_turn":
                return response

            if response.stop_reason != "tool_use":
                # Unexpected stop reason, return as-is
                return response

            # Process tool calls
            tool_results = await self._process_tool_calls(response)

            # Update messages for next iteration
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            # Update request kwargs with new messages
            request_kwargs["messages"] = messages

            iteration += 1

        return response

    async def _process_tool_calls(
        self, response: BetaMessage
    ) -> list[dict[str, Any]]:
        """Execute tool calls and return results.

        Args:
            response: API response containing tool_use blocks

        Returns:
            List of tool_result dicts
        """
        results = []

        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id

                # Skip code_execution tool itself (handled by API)
                if tool_name == "code_execution":
                    continue

                try:
                    # Execute tool via MCP
                    result = await self.tool_executor(tool_name, tool_input)

                    # Format result as string
                    if isinstance(result, str):
                        content = result
                    else:
                        content = json.dumps(result, default=str)

                    results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": content,
                    })

                except Exception as e:
                    # Return error as tool result
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": f"Error executing {tool_name}: {str(e)}",
                        "is_error": True,
                    })

        return results

    def extract_text_response(self, response: BetaMessage) -> str:
        """Extract text content from response.

        Args:
            response: API response

        Returns:
            Concatenated text from all text blocks
        """
        texts = []
        for block in response.content:
            if block.type == "text":
                texts.append(block.text)
        return "\n".join(texts)
