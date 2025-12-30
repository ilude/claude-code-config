---
description: Run PTC (Programmatic Tool Calling) for efficient multi-tool workflows
argument-hint: <command> [args...] (scrape URLs | browser INSTRUCTIONS | run PROMPT)
---

# PTC - Programmatic Tool Calling

Run efficient multi-tool workflows using Anthropic's PTC feature. This reduces API round-trips and context usage by letting Claude write code that orchestrates multiple tool calls.

## Usage

The user wants to run: `ptc $ARGUMENTS`

Parse the arguments to determine the command:

### Commands

1. **scrape** - Multi-URL scraping
   ```bash
   python -m ptc_wrapper.cli scrape <url1> <url2> ... [--no-summarize]
   ```

2. **browser** - Browser automation pipeline
   ```bash
   python -m ptc_wrapper.cli browser "<instructions>" [--url <initial-url>]
   ```

3. **run** - Custom PTC prompt
   ```bash
   python -m ptc_wrapper.cli run "<prompt>" [--servers <servers>] [--tools <tools>]
   ```

4. **list** - List available servers/tools
   ```bash
   python -m ptc_wrapper.cli list [--tools]
   ```

## Execution

1. First ensure ptc-wrapper is installed:
   ```bash
   cd ~/.claude/tools/ptc-wrapper && uv pip install -e .
   ```

2. Then run the appropriate command based on user input.

3. Display the results to the user.

## Examples

- `/ptc scrape https://docs.anthropic.com https://platform.openai.com` - Compare two docs sites
- `/ptc browser "Extract top 5 stories" --url https://news.ycombinator.com` - Browser automation
- `/ptc run "Fetch and analyze these pages" --servers flaresolverr` - Custom workflow
- `/ptc list --tools` - Show available MCP tools
