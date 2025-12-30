#!/usr/bin/env python3
"""Example: Multi-URL scraping with PTC."""

import asyncio

from ptc_wrapper import PTCClient


async def main():
    """Scrape multiple documentation sites and compare them."""
    urls = [
        "https://docs.anthropic.com/en/docs/overview",
        "https://platform.openai.com/docs/overview",
    ]

    async with PTCClient() as client:
        # Load flaresolverr for web scraping
        await client.load_mcp_servers(["flaresolverr"])

        # Use high-level scrape_urls method
        result = await client.scrape_urls(urls, summarize=True)
        print("=== Summary ===")
        print(result)

        # Or use custom prompt for more control
        custom_result = await client.run(
            prompt=f"""
            Fetch these documentation pages and compare their structure:
            - {urls[0]}
            - {urls[1]}

            For each page:
            1. Use fetch_url to get the content
            2. Identify the main sections/topics covered
            3. Note the writing style and organization

            Return a structured comparison table.
            """,
            tools=["fetch_url"],
        )
        print("\n=== Custom Analysis ===")
        print(custom_result)


if __name__ == "__main__":
    asyncio.run(main())
