#!/usr/bin/env python3
"""
Permission Analyzer for Claude Code

Analyzes debug logs to find permission requests and suggests
wildcard patterns for settings.json.
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


class PermissionRequest:
    """Represents a single permission request found in logs."""

    def __init__(self, tool_name: str, rule_content: str, log_file: str):
        self.tool_name = tool_name
        self.rule_content = rule_content
        self.log_file = log_file
        self.full_pattern = f"{tool_name}({rule_content})"

    def __repr__(self):
        return f"PermissionRequest({self.full_pattern})"

    def __hash__(self):
        return hash(self.full_pattern)

    def __eq__(self, other):
        return self.full_pattern == other.full_pattern


def find_debug_logs(claude_dir: Path) -> List[Path]:
    """Find all debug log files in ~/.claude/debug/ directory."""
    debug_dir = claude_dir / "debug"

    if not debug_dir.exists():
        print(f"Warning: Debug directory not found at {debug_dir}")
        return []

    log_files = list(debug_dir.glob("*.txt"))
    print(f"Found {len(log_files)} debug log files")
    return log_files


def extract_permissions_from_log(log_file: Path) -> List[PermissionRequest]:
    """
    Extract permission requests from a single log file.

    Looks for patterns like:
    [DEBUG] Permission suggestions for Bash: [
      {
        "type": "addRules",
        "rules": [
          {
            "toolName": "Bash",
            "ruleContent": "mkdir:*"
          }
        ]
    """
    permissions = []

    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Pattern to find permission suggestion blocks
        # Matches: [DEBUG] Permission suggestions for <Tool>: [
        pattern = r'\[DEBUG\] Permission suggestions for (\w+): \[\s*\{[^}]*"rules":\s*\[([^\]]*)\]'

        for match in re.finditer(pattern, content, re.DOTALL):
            tool_type = match.group(1)
            rules_json = match.group(2)

            # Extract individual rule objects
            rule_pattern = r'\{\s*"toolName":\s*"([^"]+)",\s*"ruleContent":\s*"([^"]+)"\s*\}'

            for rule_match in re.finditer(rule_pattern, rules_json):
                tool_name = rule_match.group(1)
                rule_content = rule_match.group(2)

                perm = PermissionRequest(tool_name, rule_content, log_file.name)
                permissions.append(perm)

    except Exception as e:
        print(f"Warning: Error reading {log_file.name}: {e}")

    return permissions


def extract_all_permissions(log_files: List[Path]) -> List[PermissionRequest]:
    """Extract permissions from all log files."""
    all_permissions = []

    for log_file in log_files:
        perms = extract_permissions_from_log(log_file)
        all_permissions.extend(perms)

    print(f"Extracted {len(all_permissions)} permission requests")
    return all_permissions


def analyze_patterns(permissions: List[PermissionRequest]) -> Dict[str, Dict]:
    """
    Analyze permission patterns and group by tool and command.

    Returns:
        Dict mapping tool names to command statistics:
        {
            'Bash': {
                'commands': {'ls': 5, 'git add': 3, ...},
                'full_patterns': Counter of full patterns,
                'total': 8,
                'unique': 2
            },
            ...
        }
    """
    tool_stats = defaultdict(lambda: {
        'commands': Counter(),
        'full_patterns': Counter(),
        'total': 0,
        'unique': 0
    })

    for perm in permissions:
        # Store full pattern
        tool_stats[perm.tool_name]['full_patterns'][perm.rule_content] += 1

        # Extract command from rule_content (before the colon)
        # e.g., "git add:*" -> "git add"
        command = perm.rule_content.split(':')[0] if ':' in perm.rule_content else perm.rule_content

        tool_stats[perm.tool_name]['commands'][command] += 1
        tool_stats[perm.tool_name]['total'] += 1

    # Calculate unique counts
    for tool in tool_stats:
        tool_stats[tool]['unique'] = len(tool_stats[tool]['commands'])

    return dict(tool_stats)


def get_safety_classification(pattern: str) -> str:
    """
    Classify a pattern as safe, risky, or dangerous.

    Returns:
        'safe', 'risky', or 'dangerous'
    """
    # Remove tool name to check command
    command = pattern.lower()
    if '(' in command:
        command = command.split('(')[1].rstrip(')')

    # Dangerous patterns - never auto-approve
    dangerous = [
        'git commit', 'git push', 'git rebase', 'git reset --hard',
        'git push --force', 'rm ', 'rmdir', 'del ', 'sudo ',
        'git rm -rf', 'git clean', 'docker rm', 'docker rmi',
        'docker system prune', 'npm uninstall', 'pip uninstall',
        'chown', 'chgrp', 'systemctl', 'service '
    ]

    for d in dangerous:
        if d in command:
            return 'dangerous'

    # Safe patterns - read-only operations
    safe = [
        'ls', 'pwd', 'echo', 'whoami', 'date', 'uname', 'which', 'where',
        'type', 'cat', 'head', 'tail', 'less', 'more', 'wc', 'grep',
        'find', 'git status', 'git diff', 'git log', 'git show', 'git branch',
        'docker ps', 'docker images', 'docker inspect', 'docker version',
        'npm list', 'yarn list', 'pip list', 'uv pip list', 'env', 'printenv',
        'history', 'jobs', 'ps', 'python --version', 'node --version'
    ]

    for s in safe:
        if s in command:
            return 'safe'

    # Everything else is risky
    return 'risky'


def suggest_wildcards(tool_stats: Dict[str, Dict], min_count: int = 3) -> List[Tuple[str, int, str, str]]:
    """
    Suggest wildcard patterns based on usage frequency.

    Returns:
        List of (pattern, count, reason, safety) tuples sorted by count descending
    """
    suggestions = []

    for tool_name, stats in tool_stats.items():
        full_patterns = stats['full_patterns']
        commands = stats['commands']
        total = stats['total']
        unique = stats['unique']

        # Check each full pattern that was used
        for pattern, count in full_patterns.items():
            if count >= min_count:
                full_pattern = f"{tool_name}({pattern})"
                safety = get_safety_classification(full_pattern)

                # Only suggest safe and risky patterns, never dangerous
                if safety != 'dangerous':
                    suggestions.append((
                        full_pattern,
                        count,
                        f"Used {count} times",
                        safety
                    ))

    # Sort by count descending
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions


def print_statistics(tool_stats: Dict[str, Dict]):
    """Print usage statistics by tool."""
    print("\n" + "="*70)
    print("PERMISSION USAGE STATISTICS")
    print("="*70)

    for tool_name in sorted(tool_stats.keys()):
        stats = tool_stats[tool_name]
        print(f"\n{tool_name}:")
        print(f"  Total requests: {stats['total']}")
        print(f"  Unique commands: {stats['unique']}")
        print(f"  Top commands:")

        for command, count in stats['commands'].most_common(10):
            print(f"    {command:40s} {count:>3d}x")

        if len(stats['full_patterns']) > 0:
            print(f"  Full patterns:")
            for pattern, count in stats['full_patterns'].most_common(10):
                print(f"    {pattern:40s} {count:>3d}x")


def load_existing_settings(claude_dir: Path) -> set:
    """Load existing permissions from settings.json."""
    settings_file = claude_dir / "settings.json"
    existing = set()

    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                if 'permissions' in settings and 'allow' in settings['permissions']:
                    existing = set(settings['permissions']['allow'])
        except Exception as e:
            print(f"Warning: Could not load existing settings: {e}")

    return existing


def print_suggestions(suggestions: List[Tuple[str, int, str, str]], existing_permissions: set):
    """Print wildcard pattern suggestions."""
    print("\n" + "="*70)
    print("SUGGESTED WILDCARD PATTERNS")
    print("="*70)

    # Filter out already existing permissions
    new_suggestions = [(p, c, r, s) for p, c, r, s in suggestions if p not in existing_permissions]

    if not new_suggestions:
        print("\nNo new patterns to suggest (all frequent patterns already approved)")
        return

    # Group by safety level
    safe_patterns = [(p, c, r) for p, c, r, s in new_suggestions if s == 'safe']
    risky_patterns = [(p, c, r) for p, c, r, s in new_suggestions if s == 'risky']

    if safe_patterns:
        print("\n[SAFE] patterns (read-only, no side effects):")
        print("\nAdd these to ~/.claude/settings.json under permissions.allow:\n")

        for pattern, count, reason in safe_patterns:
            print(f'      "{pattern}",  // {reason}')

    if risky_patterns:
        print("\n[REVIEW NEEDED] patterns (may have side effects):")
        print("Review these carefully before adding:\n")

        for pattern, count, reason in risky_patterns:
            print(f'      "{pattern}",  // {reason} - REVIEW')

    print("\n" + "-"*70)
    print("Note: Patterns for git commit/push are excluded (require manual approval)")
    print("-"*70)


def export_json(tool_stats: Dict, suggestions: List[Tuple], output_file: Path):
    """Export analysis results to JSON file."""
    data = {
        "statistics": {
            tool: {
                "total": stats["total"],
                "unique": stats["unique"],
                "commands": dict(stats["commands"]),
                "patterns": dict(stats["full_patterns"])
            }
            for tool, stats in tool_stats.items()
        },
        "suggestions": [
            {
                "pattern": pattern,
                "count": count,
                "reason": reason,
                "safety": safety
            }
            for pattern, count, reason, safety in suggestions
        ]
    }

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nResults exported to: {output_file}")


def main():
    """Main entry point for the permission analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze Claude Code permission requests from debug logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all debug logs
  python3 permission-analyzer.py

  # Export results to JSON
  python3 permission-analyzer.py --json results.json

  # Analyze with custom Claude directory
  python3 permission-analyzer.py --claude-dir /path/to/.claude

  # Use higher threshold for suggestions
  python3 permission-analyzer.py --min-count 5
        """
    )

    parser.add_argument(
        '--claude-dir',
        type=Path,
        default=Path.home() / '.claude',
        help='Path to .claude directory (default: ~/.claude)'
    )

    parser.add_argument(
        '--json',
        type=Path,
        help='Export results to JSON file'
    )

    parser.add_argument(
        '--min-count',
        type=int,
        default=3,
        help='Minimum usage count for wildcard suggestions (default: 3)'
    )

    args = parser.parse_args()

    # Validate Claude directory
    if not args.claude_dir.exists():
        print(f"Error: Claude directory not found: {args.claude_dir}")
        return 1

    print(f"Analyzing permissions from: {args.claude_dir}")

    # Find and parse logs
    log_files = find_debug_logs(args.claude_dir)
    if not log_files:
        print("No debug logs found. Run Claude Code to generate logs.")
        return 1

    permissions = extract_all_permissions(log_files)
    if not permissions:
        print("No permission requests found in logs.")
        return 0

    # Analyze patterns
    tool_stats = analyze_patterns(permissions)
    suggestions = suggest_wildcards(tool_stats, args.min_count)

    # Load existing settings to avoid duplicate suggestions
    existing = load_existing_settings(args.claude_dir)
    if existing:
        print(f"Found {len(existing)} existing permissions in settings.json")

    # Display results
    print_statistics(tool_stats)
    print_suggestions(suggestions, existing)

    # Export if requested
    if args.json:
        export_json(tool_stats, suggestions, args.json)

    return 0


if __name__ == '__main__':
    exit(main())