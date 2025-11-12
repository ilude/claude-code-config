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


def find_sessions(base_dir):
    """Find all active sessions in .session/feature/"""
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

                # Try to extract "Right Now" from CURRENT.md
                right_now = None
                if current_file.exists():
                    try:
                        with open(current_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines):
                                if line.strip() == "## Right Now" and i + 1 < len(lines):
                                    right_now = lines[i + 1].strip()
                                    break
                    except Exception:
                        pass

                sessions.append({
                    'name': item.name,
                    'mtime': mtime,
                    'right_now': right_now,
                    'has_current': current_file.exists(),
                    'has_status': status_file.exists()
                })
    except Exception as e:
        return []

    # Sort by modification time (most recent first)
    sessions.sort(key=lambda x: x['mtime'] if x['mtime'] else datetime.min, reverse=True)
    return sessions


def format_session_list(sessions):
    """Format sessions for injection into context"""
    if not sessions:
        return "No active sessions found in .session/feature/"

    lines = ["Available active sessions (most recent first):\n"]
    for i, session in enumerate(sessions, 1):
        line = f"{i}. **{session['name']}**"
        if session['right_now']:
            line += f" - {session['right_now']}"
        if session['mtime']:
            line += f" (updated {session['mtime'].strftime('%Y-%m-%d %H:%M')})"
        lines.append(line)

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
