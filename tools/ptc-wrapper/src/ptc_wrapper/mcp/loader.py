"""Load MCP server configurations."""

import json
import os
import re
from pathlib import Path
from typing import Any


def expand_env_vars(value: str) -> str:
    """Expand environment variables in a string.

    Supports ${VAR}, $VAR, and %VAR% (Windows) syntax.
    """
    # Handle ${VAR} syntax
    result = re.sub(
        r"\$\{(\w+)\}",
        lambda m: os.environ.get(m.group(1), m.group(0)),
        value,
    )
    # Handle $VAR syntax (but not $$)
    result = re.sub(
        r"\$(\w+)",
        lambda m: os.environ.get(m.group(1), m.group(0)),
        result,
    )
    # Handle %VAR% syntax (Windows)
    result = re.sub(
        r"%(\w+)%",
        lambda m: os.environ.get(m.group(1), m.group(0)),
        result,
    )
    return result


def expand_config_vars(config: dict[str, Any]) -> dict[str, Any]:
    """Recursively expand environment variables in config."""
    result = {}
    for key, value in config.items():
        if isinstance(value, str):
            result[key] = expand_env_vars(value)
        elif isinstance(value, list):
            result[key] = [
                expand_env_vars(v) if isinstance(v, str) else v for v in value
            ]
        elif isinstance(value, dict):
            result[key] = expand_config_vars(value)
        else:
            result[key] = value
    return result


def get_claude_config_paths() -> list[Path]:
    """Get possible paths for Claude config files."""
    home = Path.home()
    paths = [
        home / ".claude.json",  # Main Claude Code config
        home / ".claude" / ".mcp.json",  # Project-level MCP config
    ]
    return [p for p in paths if p.exists()]


def load_mcp_config() -> dict[str, dict[str, Any]]:
    """Load all MCP server configurations.

    Returns:
        Dict mapping server name to server config
    """
    servers: dict[str, dict[str, Any]] = {}

    for config_path in get_claude_config_paths():
        try:
            with open(config_path) as f:
                config = json.load(f)

            # Handle different config structures
            if "mcpServers" in config:
                # ~/.claude.json format
                for name, server_config in config["mcpServers"].items():
                    servers[name] = expand_config_vars(server_config)
            elif all(
                isinstance(v, dict) and ("command" in v or "url" in v)
                for v in config.values()
            ):
                # .mcp.json format (direct server definitions)
                for name, server_config in config.items():
                    servers[name] = expand_config_vars(server_config)

        except (json.JSONDecodeError, OSError) as e:
            # Skip invalid configs
            continue

    return servers


def get_server_config(server_name: str) -> dict[str, Any] | None:
    """Get configuration for a specific MCP server.

    Args:
        server_name: Name of the server

    Returns:
        Server configuration dict or None if not found
    """
    configs = load_mcp_config()
    return configs.get(server_name)


def parse_server_command(config: dict[str, Any]) -> tuple[str, list[str], dict[str, str] | None]:
    """Parse server config into command, args, and env.

    Args:
        config: Server configuration dict

    Returns:
        Tuple of (command, args, env)
    """
    command = config.get("command", "")
    args = config.get("args", [])
    env = config.get("env")

    # Expand variables in args
    args = [expand_env_vars(arg) if isinstance(arg, str) else arg for arg in args]

    # Handle Windows path conversion for USERPROFILE-based paths
    if os.name == "nt":
        args = [
            arg.replace("/", "\\") if isinstance(arg, str) and arg.startswith(os.path.expanduser("~")) else arg
            for arg in args
        ]

    return command, args, env
