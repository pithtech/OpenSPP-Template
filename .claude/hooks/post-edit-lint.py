#!/usr/bin/env python3
"""Post-edit lint hook for Claude Code.

Runs after Edit or Write and lints the touched file with the same tools as
pre-commit (ruff, ruff-format, prettier, Odoo 19 checks). Written in Python so
it behaves the same on Windows, macOS and Linux. Never fails the edit: problems
are printed for Claude to fix, and any tool error is swallowed.

Configured in .claude/settings.json ("hooks" > PostToolUse), where Claude Code reads project hooks.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def _run(cmd, cwd):
    try:
        subprocess.run(cmd, cwd=cwd, check=False, timeout=25)
    except (OSError, subprocess.SubprocessError):
        pass


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project_dir:
        return 0

    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0

    path = Path(file_path)
    if not path.is_absolute():
        path = Path(project_dir) / path
    if not path.is_file():
        return 0

    # Never lint the read-only OpenSPP checkout
    if {"upstream", "vendor"} & set(path.relative_to(project_dir).parts):
        return 0

    rel = str(path)
    suffix = path.suffix.lower()
    parts = path.parts

    if suffix == ".py":
        _run(["pre-commit", "run", "ruff", "--files", rel], project_dir)
        _run(["pre-commit", "run", "ruff-format", "--files", rel], project_dir)
        if "tests" not in parts:
            _run([sys.executable, "scripts/lint/check_odoo19.py", rel], project_dir)
    elif suffix == ".xml":
        _run(["pre-commit", "run", "prettier", "--files", rel], project_dir)
        if "data" not in parts and "demo" not in parts:
            _run([sys.executable, "scripts/lint/check_odoo19.py", "--xml", rel], project_dir)
    elif suffix in {".json", ".yml", ".yaml", ".md", ".js", ".css"}:
        _run(["pre-commit", "run", "prettier", "--files", rel], project_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
