#!/usr/bin/env python3
"""
UserPromptSubmit hook to auto-inject session context for /pickup and /snapshot commands.
Windows-safe using os.path for all file operations.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime


def parse_instances_from_current(current_file):
    """Parse all [instance:session] sections from CURRENT.md"""
    instances = []

    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        current_instance = None
        in_right_now = False

        for i, line in enumerate(lines):
            # Check for instance section header: ## [instance:session] Title
            if line.startswith('## [') and ']:' in line or line.startswith('## [') and ']' in line:
                # Extract instance:session tag
                start = line.find('[')
                end = line.find(']', start)
                if start != -1 and end != -1:
                    tag = line[start+1:end]
                    title = line[end+1:].strip()

                    if current_instance:
                        instances.append(current_instance)

                    current_instance = {
                        'tag': tag,
                        'title': title,
                        'right_now': None
                    }
                    in_right_now = False

            # Check for "### Right Now" within an instance section
            elif current_instance and line.strip() == "### Right Now":
                in_right_now = True

            # Extract Right Now content
            elif current_instance and in_right_now and line.strip() and not line.startswith('#'):
                current_instance['right_now'] = line.strip()
                in_right_now = False

        # Don't forget the last instance
        if current_instance:
            instances.append(current_instance)

    except Exception:
        pass

    return instances


def find_sessions(base_dir):
    """Find all active sessions in .session/feature/ (multi-instance aware)"""
    feature_dir = base_dir / ".session" / "feature"

    if not feature_dir.exists():
        return []

    sessions = []
    try:
        for item in feature_dir.iterdir():
            if item.is_dir():
                current_file = item / "CURRENT.md"
                status_file = item / "STATUS.md"

                # Get last modified time
                mtime = None
                if current_file.exists():
                    mtime = datetime.fromtimestamp(current_file.stat().st_mtime)
                elif status_file.exists():
                    mtime = datetime.fromtimestamp(status_file.stat().st_mtime)

                # Parse all instance sections from CURRENT.md
                instances = []
                if current_file.exists():
                    instances = parse_instances_from_current(current_file)

                sessions.append({
                    'name': item.name,
                    'mtime': mtime,
                    'instances': instances,
                    'has_current': current_file.exists(),
                    'has_status': status_file.exists()
                })
    except Exception as e:
        return []

    # Sort by modification time (most recent first)
    sessions.sort(key=lambda x: x['mtime'] if x['mtime'] else datetime.min, reverse=True)
    return sessions


def format_session_list(sessions):
    """Format sessions for injection into context (multi-instance aware)"""
    if not sessions:
        return "No active sessions found in .session/feature/"

    lines = ["Available active sessions (most recent first):\n"]

    item_num = 1
    for session in sessions:
        # Show feature name
        feature_name = session['name']
        mtime_str = session['mtime'].strftime('%Y-%m-%d %H:%M') if session['mtime'] else 'unknown'

        # If no instances found, show legacy format
        if not session['instances']:
            lines.append(f"{item_num}. **{feature_name}** (updated {mtime_str})")
            item_num += 1
        else:
            # Show each instance within the feature
            for instance in session['instances']:
                line = f"{item_num}. **{feature_name}** [{instance['tag']}]"
                if instance['title']:
                    line += f" - {instance['title']}"
                if instance['right_now']:
                    line += f" - {instance['right_now']}"
                line += f" (updated {mtime_str})"
                lines.append(line)
                item_num += 1

    return "\n".join(lines)


def main():
    try:
        # Read input from stdin
        data = json.load(sys.stdin)
        prompt = data.get('prompt', '')
        cwd = Path(data.get('cwd', os.getcwd()))

        # Check if prompt starts with /pickup or /snapshot
        if not (prompt.strip().startswith('/pickup') or prompt.strip().startswith('/snapshot')):
            # Not relevant, pass through
            print(json.dumps({}))
            return

        # Find sessions
        sessions = find_sessions(cwd)
        context = format_session_list(sessions)

        # Return additional context
        output = {
            "hookSpecificOutput": {
                "additionalContext": context
            }
        }
        print(json.dumps(output))

    except Exception as e:
        # On error, pass through silently
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        print(json.dumps({}))


if __name__ == "__main__":
    main()
