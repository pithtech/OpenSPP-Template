"""Shared helpers for repo-level tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_env(path: Path = ROOT / ".env") -> dict[str, str]:
    """Parse the committed .env file (KEY=VALUE lines, # comments)."""
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values
