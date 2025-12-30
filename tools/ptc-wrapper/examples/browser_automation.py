#!/usr/bin/env python3
"""Example: Browser automation pipeline with PTC."""

import asyncio

from ptc_wrapper import PTCClient


async def main():
    """Automate browser to extract data from a website."""
    async with PTCClient() as client:
        # Load browsermcp for browser automation
        await client.load_mcp_servers(["browsermcp"])

        # Use high-level browser_pipeline method
        result = await client.browser_pipeline(
            initial_url="https://news.ycombinator.com",
            instructions="""
            1. Take a snapshot of the page
            2. Find the top 5 story titles and their point counts
            3. Return the data as a JSON list with title, points, and rank
            """,
        )
        print("=== Hacker News Top Stories ===")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
