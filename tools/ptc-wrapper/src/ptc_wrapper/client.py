"""Main PTC client for orchestrating MCP tools."""

import os
from typing import Any

from anthropic import Anthropic

from ptc_wrapper.mcp.client import MCPClient
from ptc_wrapper.mcp.loader import load_mcp_config, parse_server_command
from ptc_wrapper.tools.converter import convert_all_tools
from ptc_wrapper.orchestration.loop import AgenticLoop


class PTCClient:
    """Main client for Programmatic Tool Calling with MCP tools."""

    DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):
        """Initialize PTC client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (defaults to claude-sonnet-4-5)
        """
        self.anthropic = Anthropic(api_key=api_key)
        self.model = model or self.DEFAULT_MODEL
        self.mcp_clients: dict[str, MCPClient] = {}
        self._tool_registry: dict[str, str] = {}  # tool_name -> server_name

    async def load_mcp_servers(
        self,
        server_names: list[str] | None = None,
    ) -> None:
        """Load and connect to MCP servers from config.

        Args:
            server_names: Specific servers to load (None = all available)
        """
        configs = load_mcp_config()

        if server_names is None:
            server_names = list(configs.keys())

        for name in server_names:
            if name not in configs:
                raise ValueError(f"MCP server '{name}' not found in config")

            config = configs[name]

            # Skip non-stdio servers (HTTP, etc.)
            if "url" in config:
                continue

            command, args, env = parse_server_command(config)
            client = MCPClient(command=command, args=args, env=env, name=name)
            await client.connect()

            self.mcp_clients[name] = client

            # Register tools
            for tool in client.tools.values():
                self._tool_registry[tool.name] = name

    async def run(
        self,
        prompt: str,
        tools: list[str] | None = None,
        system: str | None = None,
        max_iterations: int = 50,
    ) -> str:
        """Run a prompt with PTC-enabled tools.

        Args:
            prompt: User prompt
            tools: Tool names to enable (None = all loaded tools)
            system: Optional system prompt
            max_iterations: Max tool-use iterations

        Returns:
            Text response from Claude
        """
        # Get tools to use
        ptc_tools = self._get_ptc_tools(tools)

        if not ptc_tools:
            raise ValueError("No tools available. Call load_mcp_servers first.")

        # Create agentic loop
        loop = AgenticLoop(
            client=self.anthropic,
            tool_executor=self._execute_tool,
            model=self.model,
        )

        # Run conversation
        messages = [{"role": "user", "content": prompt}]
        response = await loop.run(
            messages=messages,
            tools=ptc_tools,
            system=system,
            max_iterations=max_iterations,
        )

        return loop.extract_text_response(response)

    async def scrape_urls(
        self,
        urls: list[str],
        extract_content: bool = True,
        summarize: bool = True,
    ) -> str:
        """High-level multi-URL scraping with automatic orchestration.

        Args:
            urls: List of URLs to scrape
            extract_content: Whether to extract main content
            summarize: Whether to summarize results

        Returns:
            Combined results or summary
        """
        # Build prompt for efficient scraping
        url_list = "\n".join(f"- {url}" for url in urls)

        if summarize:
            prompt = f"""Fetch content from these URLs and provide a summary:
{url_list}

For each URL, use fetch_url to get the content, then extract key information.
After fetching all URLs, provide a structured summary comparing the content.
Only return the final summary, not the raw content."""
        else:
            prompt = f"""Fetch content from these URLs:
{url_list}

For each URL, use fetch_url with extract_content={extract_content}.
Return the key content from each page."""

        return await self.run(prompt, tools=["fetch_url"])

    async def browser_pipeline(
        self,
        instructions: str,
        initial_url: str | None = None,
    ) -> str:
        """High-level browser automation pipeline.

        Args:
            instructions: Natural language instructions for browser automation
            initial_url: Optional URL to navigate to first

        Returns:
            Results from browser automation
        """
        if initial_url:
            prompt = f"""Navigate to {initial_url} and then:
{instructions}

Use the browser tools (browser_navigate, browser_snapshot, browser_click, browser_type, etc.)
to accomplish this task. Return only the final results."""
        else:
            prompt = f"""{instructions}

Use the browser tools to accomplish this task. Return only the final results."""

        browser_tools = [
            "browser_navigate",
            "browser_snapshot",
            "browser_click",
            "browser_type",
            "browser_hover",
            "browser_press_key",
            "browser_select_option",
            "browser_wait",
            "browser_go_back",
            "browser_go_forward",
        ]

        # Filter to only available tools
        available = [t for t in browser_tools if t in self._tool_registry]
        return await self.run(prompt, tools=available if available else None)

    def _get_ptc_tools(self, tool_names: list[str] | None) -> list[dict[str, Any]]:
        """Get PTC-formatted tool definitions.

        Args:
            tool_names: Specific tools or None for all

        Returns:
            List of PTC tool definitions
        """
        all_tools = []

        for server_name, client in self.mcp_clients.items():
            for tool in client.tools.values():
                if tool_names is None or tool.name in tool_names:
                    all_tools.append(tool)

        return convert_all_tools(all_tools)

    async def _execute_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> Any:
        """Execute a tool via its MCP server.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool result
        """
        server_name = self._tool_registry.get(tool_name)
        if not server_name:
            raise ValueError(f"Unknown tool: {tool_name}")

        client = self.mcp_clients.get(server_name)
        if not client:
            raise ValueError(f"MCP server '{server_name}' not connected")

        result = await client.call_tool(tool_name, arguments)

        # Extract text content
        if result.content:
            texts = [c.text for c in result.content if hasattr(c, "text")]
            return "\n".join(texts) if texts else result.model_dump()

        return result.model_dump()

    async def close(self) -> None:
        """Close all MCP connections."""
        for client in self.mcp_clients.values():
            await client.close()
        self.mcp_clients.clear()
        self._tool_registry.clear()

    async def __aenter__(self) -> "PTCClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
