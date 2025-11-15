#!/usr/bin/env python3
"""Analyze skill activation patterns from conversation history.

Detects missed skill activations and suggests trigger improvements.
Similar architecture to permission-analyzer.py.

Usage:
    python skill-analyzer.py --json output.json --checkpoint
    python skill-analyzer.py --json output.json --reset  # Re-analyze all
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


class SkillActivationSignal:
    """Represents a signal that should trigger skill activation."""

    def __init__(self, signal_type: str, value: str, line_num: int = 0):
        self.type = signal_type  # 'file', 'import', 'error', 'command'
        self.value = value
        self.line_num = line_num

    def __repr__(self):
        return f"Signal({self.type}={self.value}, line={self.line_num})"


class IntentSignal(SkillActivationSignal):
    """Signal from user message or bash command."""

    def __init__(self, signal_type: str, value: str, confidence: str, skill: str = None, line_num: int = 0):
        super().__init__(signal_type, value, line_num)
        self.confidence = confidence  # 'high', 'medium', 'low'
        self.skill = skill  # Suggested skill to activate


# Bash command to skill mapping
BASH_COMMAND_MAPPING = {
    'git': 'git-workflow',
    'git add': 'git-workflow',
    'git commit': 'git-workflow',
    'git push': 'git-workflow',
    'git pull': 'git-workflow',
    'git merge': 'git-workflow',
    'git checkout': 'git-workflow',
    'git branch': 'git-workflow',
    'git status': 'git-workflow',
    'git log': 'git-workflow',
    'docker': 'container-projects',
    'docker-compose': 'container-projects',
    'docker compose': 'container-projects',
    'kubectl': 'container-projects',
    'npm': 'web-projects',
    'yarn': 'web-projects',
    'pnpm': 'web-projects',
    'python': 'python-workflow',
    'pip': 'python-workflow',
    'uv': 'python-workflow',
    'pytest': 'testing-workflow',
    'make test': 'testing-workflow',
}


class Skill:
    """Represents a skill with its activation patterns."""

    def __init__(self, name: str, path: Path, description: str = ""):
        self.name = name
        self.path = path
        self.description = description
        self.activation_patterns = []  # List of regex patterns

    def should_activate(self, signals: List[SkillActivationSignal]) -> Optional[SkillActivationSignal]:
        """Check if any signal matches this skill's activation patterns."""
        for signal in signals:
            for pattern in self.activation_patterns:
                if re.search(pattern, signal.value, re.IGNORECASE):
                    return signal
        return None

    def __repr__(self):
        return f"Skill({self.name}, patterns={len(self.activation_patterns)})"


def get_checkpoint_path(claude_dir: Path) -> Path:
    """Get path to checkpoint file."""
    checkpoint_dir = claude_dir / ".checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    return checkpoint_dir / "skill-analyzer.json"


def load_checkpoint(claude_dir: Path, reset: bool = False) -> Optional[int]:
    """Load checkpoint timestamp.

    Args:
        claude_dir: Path to .claude directory
        reset: If True, ignore existing checkpoint

    Returns:
        Last analyzed timestamp in milliseconds, or None if no checkpoint or reset
    """
    if reset:
        return None

    checkpoint_path = get_checkpoint_path(claude_dir)
    if not checkpoint_path.exists():
        return None

    try:
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('last_analyzed_timestamp')
    except (json.JSONDecodeError, OSError):
        return None


def save_checkpoint(claude_dir: Path, last_timestamp: int, messages_analyzed: int):
    """Save checkpoint after successful analysis.

    Args:
        claude_dir: Path to .claude directory
        last_timestamp: Latest message timestamp analyzed (milliseconds)
        messages_analyzed: Number of messages analyzed in this run
    """
    checkpoint_path = get_checkpoint_path(claude_dir)

    data = {
        'last_analyzed_timestamp': last_timestamp,
        'last_run_date': datetime.now().isoformat(),
        'messages_analyzed': messages_analyzed,
    }

    with open(checkpoint_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def find_claude_dir() -> Path:
    """Find the .claude directory."""
    home = Path.home()
    claude_dir = home / ".claude"
    if not claude_dir.exists():
        raise FileNotFoundError(f"Claude directory not found: {claude_dir}")
    return claude_dir


def find_conversation_data(claude_dir: Path) -> Tuple[Optional[Path], List[Path]]:
    """Find history.jsonl and debug logs.

    Returns:
        (history_file, debug_files)
    """
    history_file = claude_dir / "history.jsonl"
    if not history_file.exists():
        history_file = None

    debug_dir = claude_dir / "debug"
    debug_files = []
    if debug_dir.exists():
        debug_files = sorted(debug_dir.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)

    return history_file, debug_files


def parse_history(history_file: Path, checkpoint_timestamp: Optional[int] = None) -> Tuple[List[dict], Optional[int]]:
    """Parse history.jsonl file.

    Args:
        history_file: Path to history.jsonl
        checkpoint_timestamp: Only parse entries after this timestamp (ms since epoch)

    Returns:
        Tuple of (messages list, latest timestamp in this batch)
    """
    messages = []
    latest_timestamp = None

    with open(history_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                timestamp = entry.get('timestamp', 0)

                # Skip if before checkpoint
                if checkpoint_timestamp and timestamp <= checkpoint_timestamp:
                    continue

                messages.append(entry)

                # Track latest timestamp
                if latest_timestamp is None or timestamp > latest_timestamp:
                    latest_timestamp = timestamp

            except json.JSONDecodeError:
                continue

    return messages, latest_timestamp


def parse_debug_logs(debug_files: List[Path]) -> Dict[str, List[SkillActivationSignal]]:
    """Parse debug logs for tool invocations and file operations.

    Returns:
        Dict with keys: 'files', 'imports', 'errors', 'commands', 'skills_activated'
    """
    signals = {
        'files': [],
        'imports': [],
        'errors': [],
        'commands': [],
        'skills_activated': []
    }

    for debug_file in debug_files:
        try:
            with open(debug_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Extract auto-activated skills (shows which skills Claude loaded)
                auto_skill_pattern = r'\[DEBUG\] Skills and commands included in Skill tool: ([^\n]+)'
                for match in re.finditer(auto_skill_pattern, content):
                    skills_list = match.group(1).strip()
                    # Parse comma-separated skill names
                    for skill_name in skills_list.split(','):
                        skill_name = skill_name.strip()
                        if skill_name:
                            signals['skills_activated'].append(
                                SkillActivationSignal('skill', skill_name, 0)
                            )

                # Extract manual skill invocations (when user explicitly calls Skill tool)
                tool_pattern = r'\[DEBUG\] executePreToolHooks called for tool: (\w+)'
                for match in re.finditer(tool_pattern, content):
                    tool_name = match.group(1)
                    if tool_name == 'Skill':
                        # Note: This only captures that Skill tool was used, not which skill
                        # Auto-activation pattern above is more accurate
                        pass

                # Extract file operations from FileHistory
                file_pattern = r'\[DEBUG\] FileHistory: Tracked file modification for ([^\n]+)'
                for match in re.finditer(file_pattern, content):
                    file_path = match.group(1).strip()
                    signals['files'].append(
                        SkillActivationSignal('file', file_path, 0)
                    )

                # Also extract from "File written" messages
                write_pattern = r'\[DEBUG\] File ([^\s]+) written atomically'
                for match in re.finditer(write_pattern, content):
                    file_path = match.group(1).strip()
                    signals['files'].append(
                        SkillActivationSignal('file', file_path, 0)
                    )

                # Extract errors with file paths
                error_pattern = r'\[ERROR\].*?expected ([^,]+),'
                for match in re.finditer(error_pattern, content):
                    file_path = match.group(1).strip()
                    if '\\' in file_path or '/' in file_path:
                        signals['files'].append(
                            SkillActivationSignal('file', file_path, 0)
                        )

        except Exception as e:
            print(f"Error parsing {debug_file}: {e}")

    return signals


def extract_bash_commands(debug_files: List[Path]) -> List[IntentSignal]:
    """Extract bash commands from permission logs in debug files.

    Looks for patterns like: Bash(git add:*) or Bash(docker compose:*)
    """
    signals = []

    for debug_file in debug_files:
        try:
            with open(debug_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Pattern: Bash(command:*) or Bash(command)
                bash_pattern = r'Bash\(([^:)]+)(?::?\*?)\)'

                for match in re.finditer(bash_pattern, content):
                    command = match.group(1).strip()

                    # Find matching skill
                    skill = None
                    confidence = 'low'

                    # Check exact matches first (high confidence)
                    for cmd_prefix, skill_name in BASH_COMMAND_MAPPING.items():
                        if command.startswith(cmd_prefix):
                            skill = skill_name
                            confidence = 'high'
                            break

                    # If no exact match, check first word (medium confidence)
                    if not skill:
                        first_word = command.split()[0] if command else ''
                        if first_word in ['git', 'docker', 'npm', 'yarn', 'pnpm', 'python', 'pip', 'uv']:
                            skill = BASH_COMMAND_MAPPING.get(first_word, None)
                            confidence = 'medium'

                    if skill:
                        signals.append(
                            IntentSignal('bash_command', command, confidence, skill)
                        )

        except Exception as e:
            # Skip files that can't be read
            continue

    return signals


def parse_user_messages(history_file: Path) -> List[IntentSignal]:
    """Parse user messages for skill-triggering intents.

    Reads history.jsonl and looks for keywords in 'display' field.
    """
    signals = []

    # Intent keyword mapping
    intent_patterns = {
        'git-workflow': {
            'high': ['commit my changes', 'push to', 'create a branch', 'merge'],
            'medium': ['git', 'commit', 'push', 'branch', 'staging'],
        },
        'adversarial-review': {
            'high': ['what could go wrong', 'find flaws', 'poke holes', 'red team'],
            'medium': ['review this', 'critique', 'edge cases', 'blind spots'],
        },
        'development-philosophy': {
            'high': ['MVP', 'over-engineering', 'keep it simple'],
            'medium': ['architecture', 'design', 'planning', 'approach'],
        },
        'structured-analysis': {
            'high': ['deep analyze', 'analyze this', 'validate'],
            'medium': ['analyze', 'review', 'evaluate', 'assess'],
        },
        'container-projects': {
            'high': ['docker compose', 'kubernetes', 'container'],
            'medium': ['docker', 'deploy', 'orchestration'],
        },
        'security-first-design': {
            'high': ['authentication', 'authorization', 'API security'],
            'medium': ['security', 'secrets', 'encryption', 'sensitive data'],
        },
    }

    try:
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    entry = json.loads(line)

                    # Only process user messages with display field
                    if 'display' in entry:
                        message = entry.get('display', '').lower()

                        # Check each skill's patterns
                        for skill, patterns in intent_patterns.items():
                            # Check high confidence patterns
                            for pattern in patterns.get('high', []):
                                if pattern.lower() in message:
                                    signals.append(
                                        IntentSignal('user_intent', pattern, 'high', skill)
                                    )
                                    break  # One match per skill per message
                            else:
                                # Check medium confidence if no high match
                                for pattern in patterns.get('medium', []):
                                    if pattern.lower() in message:
                                        signals.append(
                                            IntentSignal('user_intent', pattern, 'medium', skill)
                                        )
                                        break

                except json.JSONDecodeError:
                    continue

    except Exception:
        # If history file can't be read, return empty list
        pass

    return signals


def load_skills(claude_dir: Path) -> Dict[str, Skill]:
    """Load all skills from .claude/skills/ directories.

    Looks in:
    - ~/.claude/skills/ (user/personal)
    - ./.claude/skills/ (project, if exists)

    Returns:
        Dict of skill_name -> Skill object
    """
    skills = {}

    # Load from user directory
    user_skills_dir = claude_dir / "skills"
    if user_skills_dir.exists():
        for skill_dir in user_skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skill = parse_skill_file(skill_file)
                if skill:
                    skills[skill.name] = skill

    # Load from project directory (if in a project)
    # Note: This script runs from ~/.claude/scripts, so we'd need to find project dir
    # For now, skip project skills (would need project path as arg)

    return skills


def parse_skill_file(skill_file: Path) -> Optional[Skill]:
    """Parse SKILL.md file to extract activation patterns.

    Looks for:
    - Frontmatter with 'description' containing activation criteria
    - Section starting with "**Auto-activates when**:" or similar
    - Lists of activation criteria
    """
    try:
        content = skill_file.read_text(encoding='utf-8')
    except Exception:
        return None

    skill_name = skill_file.parent.name

    # Extract description from frontmatter
    description = ""
    desc_match = re.search(r'description:\s*(.+?)(?:\n---|\Z)', content, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()

    skill = Skill(skill_name, skill_file, description)

    # Extract activation patterns from description (for skills without explicit Auto-activates section)
    if 'when' in description.lower() or 'activate' in description.lower():
        # Look for patterns like "when working with X", "Activate when", etc.
        pattern_keywords = [
            r'working with ([^,\.]+)',
            r'when.*?with ([^,\.]+)',
            r'files? \(([^)]+)\)',
            r'importing from ([^,\.]+)',
            r'directories? like ([^,\.]+)',
        ]

        for keyword_pattern in pattern_keywords:
            for match in re.finditer(keyword_pattern, description, re.IGNORECASE):
                text = match.group(1)
                # Extract file patterns
                if '.py' in text:
                    skill.activation_patterns.append(r'\.py$')
                if 'tools/' in text:
                    skill.activation_patterns.append(r'tools[/\\]')
                if 'projects/' in text:
                    skill.activation_patterns.append(r'projects[/\\]')
                if '.services' in text:
                    skill.activation_patterns.append(r'tools\.services')

    # Also look for explicit "Auto-activates when" or "Auto-activate when" section
    # Handles both "**Auto-activates when:**" and "**Auto-activate when:**"
    activation_section = re.search(
        r'\*\*Auto-activates? when:?\*\*\s*(.*?)(?:\n\n|---|\n##)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if activation_section:
        activation_text = activation_section.group(1)

        # Extract patterns from bullet points
        bullet_pattern = r'[-*]\s+(.+?)(?:\n|$)'
        for match in re.finditer(bullet_pattern, activation_text):
            criterion = match.group(1).strip()

            # Extract code snippets
            code_snippets = re.findall(r'`([^`]+)`', criterion)
            for snippet in code_snippets:
                # Escape regex special chars except wildcards
                pattern = snippet.replace('.', r'\.').replace('*', '.*').replace('/', r'[/\\]')
                skill.activation_patterns.append(pattern)

        # Also extract from prose (non-bullet format)
        # Look for backtick-wrapped patterns in the text
        all_code_snippets = re.findall(r'`([^`]+)`', activation_text)
        for snippet in all_code_snippets:
            # Skip if already added from bullets
            pattern = snippet.replace('.', r'\.').replace('*', '.*').replace('/', r'[/\\]')
            if pattern not in skill.activation_patterns:
                skill.activation_patterns.append(pattern)

    return skill


def detect_missed_activations(
    signals: Dict[str, List[SkillActivationSignal]],
    skills: Dict[str, Skill]
) -> List[dict]:
    """Compare expected vs actual skill activations.

    Returns:
        List of missed activation suggestions
    """
    activated_skills = {s.value for s in signals['skills_activated']}
    missed = []

    # Combine all signals except skills_activated
    all_signals = (
        signals['files'] +
        signals['imports'] +
        signals['errors'] +
        signals['commands'] +
        signals.get('bash_commands', []) +
        signals.get('user_intents', [])
    )

    for skill_name, skill in skills.items():
        if skill_name in activated_skills:
            continue  # Already activated correctly

        # Check if this skill should have activated
        matching_signal = skill.should_activate(all_signals)
        if matching_signal:
            missed.append({
                'skill_name': skill_name,
                'skill_path': str(skill.path),
                'description': skill.description,
                'evidence': matching_signal.value,
                'evidence_type': matching_signal.type,
                'line_number': matching_signal.line_num,
                'current_triggers': skill.activation_patterns,
                'confidence': 'high' if matching_signal.type == 'file' else 'medium'
            })

    return missed


def normalize_path(file_path: str) -> Optional[str]:
    """Normalize a file path to project-relative or meaningful context.

    Returns None if path should be filtered out (system/infrastructure).
    """
    path = Path(file_path)
    parts = path.parts

    # Filter out system paths
    if len(parts) > 0:
        # Windows system paths
        if parts[0] in ('C:\\', 'D:\\', 'E:\\') and len(parts) > 1:
            if parts[1] in ('Windows', 'Program Files', 'Program Files (x86)'):
                return None

            # Home directory - filter out .claude infrastructure
            if parts[1] == 'Users' and len(parts) > 2:
                # Skip ~/.claude/ infrastructure work (meta/config)
                if '.claude' in parts:
                    claude_idx = parts.index('.claude')
                    # Allow .claude/skills/ but filter .claude/tools/, .claude/scripts/
                    if claude_idx + 1 < len(parts):
                        next_dir = parts[claude_idx + 1]
                        if next_dir in ('tools', 'scripts', 'debug', 'file-history', '.checkpoints'):
                            return None
                    # Return relative to .claude for skills
                    if claude_idx + 1 < len(parts) and parts[claude_idx + 1] == 'skills':
                        return str(Path(*parts[claude_idx:]))
                    return None

            # Find project root indicators (has .git, pyproject.toml, etc.)
            for i, part in enumerate(parts):
                if part in ('Projects', 'Code', 'src', 'repos', 'git'):
                    # Return path relative to this level
                    if i + 1 < len(parts):
                        return str(Path(*parts[i+1:]))

        # Unix-like paths
        if parts[0] == '/' and len(parts) > 1:
            if parts[1] in ('usr', 'etc', 'var', 'tmp', 'sys', 'proc'):
                return None

    # If we couldn't normalize, return original
    return str(path)


def extract_meaningful_pattern(normalized_path: str, skill_description: str) -> Optional[str]:
    """Extract a meaningful trigger pattern from a normalized path.

    Returns None if no meaningful pattern can be extracted.
    """
    if not normalized_path:
        return None

    path = Path(normalized_path)
    parts = path.parts

    if len(parts) == 0:
        return None

    # For project paths, extract meaningful depth
    # e.g., "agent-spike/tools/scripts/lib/" -> "tools/scripts/lib/"
    # e.g., "agent-spike/lessons/lesson-001/" -> "lessons/"

    # Look for semantic anchors in the skill description
    description_lower = skill_description.lower()

    # Build pattern from significant parts
    meaningful_parts = []
    for i, part in enumerate(parts):
        part_lower = part.lower()

        # Check if this part is mentioned in skill description
        if part_lower in description_lower:
            # Include this part and maybe 1-2 levels deeper
            meaningful_parts = list(parts[i:min(i+3, len(parts))])
            break

    # If no semantic match, use heuristics
    if not meaningful_parts:
        # Skip generic project names, go to meaningful directories
        skip_patterns = {'agent-spike', 'project', 'src', 'main', 'app'}
        start_idx = 0
        for i, part in enumerate(parts):
            if part.lower() not in skip_patterns:
                start_idx = i
                break

        # Take 2-3 levels of meaningful path
        if start_idx < len(parts):
            meaningful_parts = list(parts[start_idx:min(start_idx+3, len(parts))])

    if not meaningful_parts:
        return None

    # Build pattern string
    pattern = '/'.join(meaningful_parts)

    # If it's a file, convert to directory pattern
    if '.' in meaningful_parts[-1]:
        # Remove file, keep directory
        if len(meaningful_parts) > 1:
            pattern = '/'.join(meaningful_parts[:-1]) + '/'
        else:
            # File pattern like "test_*.py"
            if meaningful_parts[0].startswith('test_'):
                return 'test_*.py'
            return None
    else:
        pattern += '/'

    return pattern


def is_pattern_already_covered(pattern: str, existing_patterns: List[str]) -> bool:
    """Check if a pattern is already covered by existing triggers."""
    if not pattern:
        return True

    for existing in existing_patterns:
        # Convert glob/regex to comparable form
        existing_normalized = existing.replace('[/\\\\]', '/').replace(r'\.', '.')

        # Check if pattern is subset of existing
        if pattern in existing_normalized or existing_normalized in pattern:
            return True

    return False


def suggest_trigger_improvements(missed: List[dict], signals: Dict) -> List[dict]:
    """Generate suggestions for new activation patterns.

    Analyzes the evidence to suggest specific trigger additions.
    Uses path normalization and semantic matching to avoid garbage suggestions.
    """
    suggestions = []

    for item in missed:
        evidence_type = item['evidence_type']
        evidence = item['evidence']
        skill_description = item.get('description', '')
        current_triggers = item.get('current_triggers', [])

        # Generate specific trigger suggestion based on evidence
        suggested_triggers = []

        if evidence_type == 'file':
            # Check if existing patterns already match this file
            # If so, the pattern is correct but the skill just didn't activate (context-based)
            existing_match = False
            for pattern in current_triggers:
                if re.search(pattern, evidence, re.IGNORECASE):
                    existing_match = True
                    break

            if existing_match:
                # Pattern already matches - no need to suggest improvements
                # The skill just didn't activate for other reasons (context, relevance, etc.)
                continue

            # Normalize path to filter out system/infrastructure
            normalized = normalize_path(evidence)
            if normalized:
                # Extract meaningful pattern
                pattern = extract_meaningful_pattern(normalized, skill_description)
                if pattern and not is_pattern_already_covered(pattern, current_triggers):
                    suggested_triggers.append(f"Working with `{pattern}` directory")

        elif evidence_type == 'import':
            # Suggest import pattern
            # e.g., "tools.services.youtube" -> "tools.services.*"
            parts = evidence.split('.')
            if len(parts) >= 2:
                pattern = '.'.join(parts[:2]) + '.*'
                if not is_pattern_already_covered(pattern, current_triggers):
                    suggested_triggers.append(f"Importing from `{pattern}`")

        elif evidence_type == 'error':
            # Suggest error pattern
            if 'proxy' in evidence.lower():
                suggested_triggers.append("When proxy configuration errors occur")
            elif 'rate limit' in evidence.lower():
                suggested_triggers.append("When rate limiting errors occur")

        elif evidence_type == 'bash_command':
            # Suggest bash command pattern
            # Evidence format: "git commit -m ..." or "docker build ."
            if not is_pattern_already_covered(evidence.split()[0], current_triggers):
                suggested_triggers.append(f"When running `{evidence.split()[0]}` commands")

        elif evidence_type == 'user_intent':
            # Suggest user intent pattern
            # Evidence format: keyword like "commit my changes" or "create a branch"
            if not is_pattern_already_covered(evidence.lower(), current_triggers):
                suggested_triggers.append(f"User mentions: `{evidence}`")

        # Only include items with actual suggestions
        if suggested_triggers:
            suggestion = item.copy()
            suggestion['suggested_triggers'] = suggested_triggers
            # Add confidence if available (from IntentSignal)
            if hasattr(item, 'confidence'):
                suggestion['confidence'] = item['confidence']
            suggestions.append(suggestion)

    return suggestions


def export_json(
    stats: dict,
    suggestions: List[dict],
    output_file: Path
):
    """Export results to JSON file."""
    output = {
        'statistics': stats,
        'suggestions': suggestions
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze skill activation patterns from conversation history'
    )
    parser.add_argument(
        '--json',
        type=Path,
        help='Output file for JSON results'
    )
    parser.add_argument(
        '--checkpoint',
        action='store_true',
        default=True,
        help='Use checkpoint to only analyze new messages (default: enabled)'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Ignore checkpoint and re-analyze all messages'
    )
    parser.add_argument(
        '--claude-dir',
        type=Path,
        help='Path to .claude directory (default: ~/.claude)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed output'
    )

    args = parser.parse_args()

    # Find Claude directory
    if args.claude_dir:
        claude_dir = args.claude_dir
    else:
        claude_dir = find_claude_dir()

    if args.verbose:
        print(f"Using Claude directory: {claude_dir}")

    # Load checkpoint
    checkpoint_timestamp = load_checkpoint(claude_dir, reset=args.reset)
    if args.verbose:
        if args.reset:
            print("Reset mode: Analyzing all messages")
        elif checkpoint_timestamp:
            checkpoint_date = datetime.fromtimestamp(checkpoint_timestamp / 1000).isoformat()
            print(f"Using checkpoint: {checkpoint_date}")
        else:
            print("No checkpoint found: Analyzing all messages")

    # Find conversation data
    history_file, debug_files = find_conversation_data(claude_dir)

    latest_timestamp = None
    if not history_file:
        print("Warning: No history.jsonl file found")
        messages = []
    else:
        if args.verbose:
            print(f"Parsing history: {history_file}")
        messages, latest_timestamp = parse_history(history_file, checkpoint_timestamp)
        if args.verbose:
            print(f"  Found {len(messages)} messages")
            if checkpoint_timestamp:
                print(f"  (new messages since last run)")

    # Extract signals from debug logs instead of messages
    if args.verbose:
        print("Extracting activation signals from debug logs...")
    signals = parse_debug_logs(debug_files)

    # Extract bash commands from debug logs
    if args.verbose:
        print("Extracting bash commands from debug logs...")
    bash_commands = extract_bash_commands(debug_files[:10])
    signals['bash_commands'] = bash_commands

    # Extract user intents from history
    if args.verbose:
        print("Extracting user intents from history...")
    user_intents = parse_user_messages(history_file) if history_file else []
    signals['user_intents'] = user_intents

    if args.verbose:
        print(f"  Files: {len(signals['files'])}")
        print(f"  Imports: {len(signals['imports'])}")
        print(f"  Errors: {len(signals['errors'])}")
        print(f"  Skills activated: {len(signals['skills_activated'])}")
        print(f"  Bash commands: {len(signals['bash_commands'])}")
        print(f"  User intents: {len(signals['user_intents'])}")

    # Load skills
    if args.verbose:
        print("Loading skills...")
    skills = load_skills(claude_dir)

    if args.verbose:
        print(f"  Loaded {len(skills)} skills")
        for name, skill in skills.items():
            print(f"    {name}: {len(skill.activation_patterns)} patterns")

    # Detect missed activations
    if args.verbose:
        print("Detecting missed activations...")
    missed = detect_missed_activations(signals, skills)

    if args.verbose:
        print(f"  Found {len(missed)} missed activations")

    # Generate suggestions
    suggestions = suggest_trigger_improvements(missed, signals)

    # Statistics
    stats = {
        'total_skills': len(skills),
        'skills_activated': len(signals['skills_activated']),
        'missed_activations': len(missed),
        'messages_analyzed': len(messages),
        'files_touched': len(signals['files']),
        'bash_commands_detected': len(signals.get('bash_commands', [])),
        'user_intents_detected': len(signals.get('user_intents', [])),
    }

    # Output
    if args.json:
        export_json(stats, suggestions, args.json)
        if args.verbose:
            print(f"Results written to: {args.json}")
    else:
        # Print human-readable summary
        print(f"\nSkill Activation Analysis")
        print(f"=" * 50)
        print(f"Total skills: {stats['total_skills']}")
        print(f"Skills activated: {stats['skills_activated']}")
        print(f"Missed activations: {stats['missed_activations']}")
        print(f"Messages analyzed: {stats['messages_analyzed']}")
        print(f"Bash commands detected: {stats['bash_commands_detected']}")
        print(f"User intents detected: {stats['user_intents_detected']}")

        if suggestions:
            print(f"\nMissed Activations:")
            for s in suggestions:
                print(f"\n  {s['skill_name']}")
                print(f"    Evidence: {s['evidence'][:100]}")
                print(f"    Line: {s['line_number']}")
                if s.get('suggested_triggers'):
                    print(f"    Suggested: {', '.join(s['suggested_triggers'])}")

    # Save checkpoint if we processed messages
    if latest_timestamp and not args.reset:
        save_checkpoint(claude_dir, latest_timestamp, len(messages))
        if args.verbose:
            print(f"\nCheckpoint saved: {datetime.fromtimestamp(latest_timestamp / 1000).isoformat()}")


if __name__ == '__main__':
    main()
