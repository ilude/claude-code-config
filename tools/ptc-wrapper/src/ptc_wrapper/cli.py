"""Command-line interface for PTC wrapper."""

import argparse
import asyncio
import sys

from ptc_wrapper.client import PTCClient


async def cmd_scrape(args: argparse.Namespace) -> None:
    """Handle scrape command."""
    async with PTCClient() as client:
        await client.load_mcp_servers(["flaresolverr"])

        result = await client.scrape_urls(
            urls=args.urls,
            summarize=args.summarize,
        )

        print(result)


async def cmd_browser(args: argparse.Namespace) -> None:
    """Handle browser command."""
    async with PTCClient() as client:
        await client.load_mcp_servers(["browsermcp"])

        result = await client.browser_pipeline(
            instructions=args.instructions,
            initial_url=args.url,
        )

        print(result)


async def cmd_run(args: argparse.Namespace) -> None:
    """Handle run command."""
    servers = args.servers.split(",") if args.servers else None
    tools = args.tools.split(",") if args.tools else None

    async with PTCClient() as client:
        await client.load_mcp_servers(servers)

        result = await client.run(
            prompt=args.prompt,
            tools=tools,
            system=args.system,
        )

        print(result)


async def cmd_list(args: argparse.Namespace) -> None:
    """Handle list command."""
    from ptc_wrapper.mcp.loader import load_mcp_config

    configs = load_mcp_config()

    print("Available MCP servers:")
    for name, config in configs.items():
        server_type = "http" if "url" in config else "stdio"
        print(f"  - {name} ({server_type})")

    if args.tools:
        print("\nLoading tools...")
        async with PTCClient() as client:
            # Try to load stdio servers only
            stdio_servers = [
                name for name, cfg in configs.items() if "url" not in cfg
            ]
            if stdio_servers:
                try:
                    await client.load_mcp_servers(stdio_servers)
                    print("\nAvailable tools:")
                    for tool_name, server_name in client._tool_registry.items():
                        print(f"  - {tool_name} ({server_name})")
                except Exception as e:
                    print(f"\nError loading tools: {e}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="ptc",
        description="Programmatic Tool Calling wrapper for MCP tools",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scrape command
    scrape_parser = subparsers.add_parser(
        "scrape",
        help="Scrape multiple URLs using PTC",
    )
    scrape_parser.add_argument(
        "urls",
        nargs="+",
        help="URLs to scrape",
    )
    scrape_parser.add_argument(
        "--no-summarize",
        dest="summarize",
        action="store_false",
        help="Return raw content instead of summary",
    )

    # browser command
    browser_parser = subparsers.add_parser(
        "browser",
        help="Run browser automation pipeline",
    )
    browser_parser.add_argument(
        "instructions",
        help="Natural language instructions",
    )
    browser_parser.add_argument(
        "--url",
        help="Initial URL to navigate to",
    )

    # run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a custom prompt with PTC",
    )
    run_parser.add_argument(
        "prompt",
        help="Prompt to execute",
    )
    run_parser.add_argument(
        "--servers",
        help="Comma-separated list of MCP servers to use",
    )
    run_parser.add_argument(
        "--tools",
        help="Comma-separated list of tools to enable",
    )
    run_parser.add_argument(
        "--system",
        help="System prompt",
    )

    # list command
    list_parser = subparsers.add_parser(
        "list",
        help="List available servers and tools",
    )
    list_parser.add_argument(
        "--tools",
        action="store_true",
        help="Also list available tools (requires connecting to servers)",
    )

    args = parser.parse_args()

    # Run appropriate command
    if args.command == "scrape":
        asyncio.run(cmd_scrape(args))
    elif args.command == "browser":
        asyncio.run(cmd_browser(args))
    elif args.command == "run":
        asyncio.run(cmd_run(args))
    elif args.command == "list":
        asyncio.run(cmd_list(args))


if __name__ == "__main__":
    main()
