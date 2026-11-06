"""Tests for the Claude Code configuration shipped with the template."""

import json
import os
import re
import subprocess
import sys

import pytest

from tests.conftest import ROOT

CLAUDE_DIR = ROOT / ".claude"
BANNED = ("tpl_", "tpl.", "queue_job", "OCA/queue", "{Project}")


def _claude_text_files():
    files = [ROOT / "CLAUDE.md"]
    files += sorted(CLAUDE_DIR.rglob("*.md"))
    files += sorted(CLAUDE_DIR.rglob("*.json"))
    files += sorted(CLAUDE_DIR.rglob("*.py"))
    return files


class TestContent:
    @pytest.mark.parametrize("path", _claude_text_files(), ids=lambda p: str(p.relative_to(ROOT)))
    def test_no_template_leftovers(self, path):
        text = path.read_text()
        for banned in BANNED:
            assert banned not in text, f"{path.relative_to(ROOT)} still mentions {banned!r}"

    def test_claude_md_points_at_vendor_and_dswd(self):
        text = (ROOT / "CLAUDE.md").read_text()
        assert "vendor/openspp/" in text
        assert "dswd_" in text
        assert "Never edit anything under `vendor/openspp/`" in text

    @pytest.mark.parametrize("path", sorted((CLAUDE_DIR / "rules").glob("*.md")), ids=lambda p: p.name)
    def test_rules_have_path_frontmatter(self, path):
        text = path.read_text()
        assert text.startswith("---\npaths:\n"), path.name

    @pytest.mark.parametrize("path", sorted((CLAUDE_DIR / "agents").glob("*.md")), ids=lambda p: p.name)
    def test_agent_name_matches_filename(self, path):
        match = re.search(r"^name: (\S+)$", path.read_text(), re.M)
        assert match and match.group(1) == path.stem

    def test_expected_files_exist(self):
        for rel in (
            "rules/odoo-python.md",
            "rules/odoo-xml.md",
            "rules/security.md",
            "rules/testing.md",
            "rules/module-setup.md",
            "agents/odoo-developer.md",
            "agents/code-reviewer.md",
            "agents/ux-expert.md",
            "agents/code-simplifier.md",
            "agents/verify-module.md",
            "commands/implement.md",
            "commands/verify-tests.md",
            "commands/analyze.md",
            "commands/expert-review.md",
            "commands/commit.md",
            "commands/pr.md",
            "hooks/post-edit-lint.py",
            "hooks.json",
            "settings.json",
        ):
            assert (CLAUDE_DIR / rel).exists(), rel
        assert not (CLAUDE_DIR / "hooks" / "post-edit-lint.sh").exists()


@pytest.fixture(scope="module")
def settings():
    return json.loads((CLAUDE_DIR / "settings.json").read_text())


class TestSettings:
    def test_vendor_is_protected_from_edits(self, settings):
        deny = settings["permissions"]["deny"]
        assert "Edit(vendor/**)" in deny and "Write(vendor/**)" in deny

    def test_cli_invocations_are_allowed(self, settings):
        allow = settings["permissions"]["allow"]
        assert "Bash(./odoo-project:*)" in allow
        assert "Bash(python odoo-project:*)" in allow

    def test_openspp_plugin_marketplace_registered_but_nothing_enabled(self, settings):
        """odoo-lsp needs an Odoo core checkout that the template does not ship, so it stays opt-in."""
        assert settings["extraKnownMarketplaces"]["openspp-plugins"]["source"]["repo"] == "OpenSPP/claude-plugins"
        assert not settings.get("enabledPlugins")
        assert not (ROOT / "odools.toml").exists()


class TestHook:
    def test_hooks_json_runs_the_python_hook(self):
        hooks = json.loads((CLAUDE_DIR / "hooks.json").read_text())
        entry = hooks["hooks"]["PostToolUse"][0]
        assert entry["matcher"] == "Edit|Write"
        assert "post-edit-lint.py" in entry["hooks"][0]["command"]
        assert entry["hooks"][0]["command"].startswith("python ")

    def _run_hook(self, payload, env=None):
        full_env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT))
        if env:
            full_env.update(env)
        return subprocess.run(
            [sys.executable, str(CLAUDE_DIR / "hooks" / "post-edit-lint.py")],
            input=payload,
            capture_output=True,
            text=True,
            env=full_env,
            timeout=60,
        )

    def test_hook_ignores_bad_input(self):
        assert self._run_hook("not json").returncode == 0
        assert self._run_hook("{}").returncode == 0

    def test_hook_skips_vendor_files(self, monkeypatch):
        payload = json.dumps({"tool_input": {"file_path": "vendor/openspp/spp_base/__manifest__.py"}})
        result = self._run_hook(payload)
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_hook_without_project_dir_is_a_noop(self):
        env = dict(os.environ)
        env.pop("CLAUDE_PROJECT_DIR", None)
        result = subprocess.run(
            [sys.executable, str(CLAUDE_DIR / "hooks" / "post-edit-lint.py")],
            input=json.dumps({"tool_input": {"file_path": "CLAUDE.md"}}),
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )
        assert result.returncode == 0 and result.stdout == ""
