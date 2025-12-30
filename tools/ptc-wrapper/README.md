# PTC Wrapper

Programmatic Tool Calling (PTC) wrapper for MCP tools. Enables efficient multi-tool workflows with reduced API round-trips and context usage.

## Features

- **Multi-URL scraping**: Fetch multiple pages, return only summaries
- **Browser automation**: Chain browser actions with code orchestration
- **General orchestration**: Reduce round-trips for any multi-tool workflow

## Installation

```bash
cd ~/.claude/tools/ptc-wrapper
uv pip install -e .
```

## Usage

### CLI

```bash
# Scrape multiple URLs
ptc scrape https://docs.anthropic.com https://platform.openai.com

# Browser automation
ptc browser "Extract top stories" --url https://news.ycombinator.com

# Custom prompt
ptc run "Your multi-tool task" --servers flaresolverr

# List available tools
ptc list --tools
```

### Python API

```python
import asyncio
from ptc_wrapper import PTCClient

async def main():
    async with PTCClient() as client:
        await client.load_mcp_servers(["flaresolverr"])

        # High-level method
        result = await client.scrape_urls(
            ["https://example1.com", "https://example2.com"],
            summarize=True
        )

        # Or custom prompt
        result = await client.run(
            "Fetch these pages and compare them...",
            tools=["fetch_url"]
        )

        print(result)

asyncio.run(main())
```

## How It Works

1. **Loads MCP servers** from `~/.claude.json` configuration
2. **Converts tools** to PTC format with `allowed_callers` and `input_examples`
3. **Runs agentic loop** with `code_execution` tool enabled
4. **Routes tool calls** from code to appropriate MCP servers
5. **Returns final output** (intermediate results stay in code, not context)

## Architecture

```
User Script → PTCClient → Anthropic API (with code_execution)
                 ↓
              MCPClient → MCP Server (flaresolverr) via stdio
                       → MCP Server (browsermcp) via stdio
```

## Configuration

The wrapper reads MCP server configs from:
- `~/.claude.json` (main Claude Code config)
- `~/.claude/.mcp.json` (project-level config)

Example config:
```json
{
  "mcpServers": {
    "flaresolverr": {
      "command": "python",
      "args": ["~/.claude/tools/flaresolverr-mcp/server.py"]
    },
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    }
  }
}
```

## Benefits

Based on Anthropic's testing:
- **65% token reduction** on multi-tool workflows
- **60% fewer API calls** via code orchestration
- **53% faster** execution time

## Requirements

- Python 3.11+
- `anthropic>=0.40.0`
- MCP servers configured in Claude Code

## License

MIT
