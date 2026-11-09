"""Tests for the documentation shipped with the template (links, examples, consistency)."""

import re

import pytest

from tests.conftest import ROOT

SKIP_DIRS = {".git", ".venv", "vendor", "upstream", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Paths removed from the template; nothing outside docs/planning may still point at them.
REMOVED = (
    "claude-code-sandbox",
    "setup_test_env",
    "test_single_module",
    ".devcontainer",
)


def _markdown_files():
    return sorted(p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.parts))


def _text_files():
    files = []
    for pattern in ("*.md", "*.yml", "*.yaml", "*.json", "*.toml", "*.sh", "*.py"):
        files += [p for p in ROOT.rglob(pattern) if not SKIP_DIRS & set(p.parts)]
    files.append(ROOT / "odoo-project")
    return sorted(set(files))


class TestLinks:
    @pytest.mark.parametrize("path", _markdown_files(), ids=lambda p: str(p.relative_to(ROOT)))
    def test_relative_links_resolve(self, path):
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            link = match.group(1)
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = link.split("#")[0]
            if "upstream/openspp" in target:
                # The checkout is gitignored and fetched by `odoo-project vendor`; a fresh clone does not have it.
                continue
            if target:
                assert (path.parent / target).resolve().exists(), f"{path.relative_to(ROOT)} -> {link}"


class TestRemovedPaths:
    @pytest.mark.parametrize("name", REMOVED)
    def test_removed_files_are_gone(self, name):
        found = [p for p in ROOT.rglob(f"{name}*") if not SKIP_DIRS & set(p.parts)]
        assert not found, found

    @pytest.mark.parametrize("path", _text_files(), ids=lambda p: str(p.relative_to(ROOT)))
    def test_nothing_references_removed_paths(self, path):
        # The planning docs are history; the tests name removed paths to assert their absence.
        if "planning" in path.parts or "tests" in path.parts:
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        for name in REMOVED:
            assert name not in text, f"{path.relative_to(ROOT)} still mentions {name}"


class TestGuides:
    """The worked example in the guides is a 4Ps attendance module, not an inventory one."""

    @pytest.mark.parametrize(
        "path",
        sorted((ROOT / "docs" / "guides").glob("*.md")),
        ids=lambda p: p.name,
    )
    def test_no_inventory_example_leftovers(self, path):
        text = path.read_text(encoding="utf-8").lower()
        for leftover in ("stock_move", "stockmove", "stock move", "warehouse", "prefixstock", "prefixorder"):
            assert leftover not in text, f"{path.name} still uses the inventory example ({leftover})"

    def test_cli_guide_has_no_local_mode(self):
        text = (ROOT / "docs" / "guides" / "odoo-project-cli.md").read_text()
        assert "--local" not in text and "Claude Code on the web" not in text


class TestSetupGuide:
    def test_tool_versions_are_consistent(self):
        text = (ROOT / "training" / "SETUP.md").read_text()
        assert "Node.js 18" not in text
        assert "3.10+" not in text
        assert "Python 3.11+" in text and "Node.js 20+" in text


class TestGithubTemplates:
    @pytest.mark.parametrize(
        "path",
        sorted((ROOT / ".github").rglob("*.md")),
        ids=lambda p: str(p.relative_to(ROOT / ".github")),
    )
    def test_templates_are_written_for_this_project(self, path):
        text = path.read_text(encoding="utf-8")
        for leftover in ("country-specific", "QA team", "in the sprint"):
            assert leftover not in text, f"{path.name} still says {leftover!r}"


class TestSecurityPolicy:
    def test_reporting_channel_does_not_depend_on_a_missing_email(self):
        security = (ROOT / "SECURITY.md").read_text()
        contributors = (ROOT / "CONTRIBUTORS.md").read_text()
        if "email" in security.lower():
            assert "@" in contributors.replace(
                "[@", ""
            ), "SECURITY.md asks for an email that CONTRIBUTORS.md does not list"


def test_no_file_points_at_the_old_vendor_checkout_path():
    """A top-level `vendor/` breaks Odoo's SCSS build; the checkout lives in `upstream/openspp`."""
    offenders = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if not path.is_file() or SKIP_DIRS & set(rel.parts) or rel.parts[0] == "tests":
            continue
        if path.suffix not in {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".cfg"} and path.name != "odoo-project":
            continue
        if "vendor/openspp" in path.read_text(encoding="utf-8", errors="ignore"):
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


SPEC_SECTIONS = (
    "## The need",
    "## Who uses it",
    "## Rules",
    "## Where it appears",
    "## Acceptance examples",
    "## Out of scope",
    "## Upstream models and views it relies on",
)


class TestSpecifications:
    """Specifications in docs/specs/ are what Claude Code reads before it researches and plans a change."""

    def test_template_has_every_section(self):
        readme = (ROOT / "docs" / "specs" / "README.md").read_text(encoding="utf-8")
        for section in SPEC_SECTIONS:
            assert section in readme, f"docs/specs/README.md template lacks {section!r}"

    def test_demo_specification_follows_the_template(self):
        spec = (ROOT / "docs" / "specs" / "dswd_household_children.md").read_text(encoding="utf-8")
        assert "**Status**: Approved" in spec
        for section in SPEC_SECTIONS:
            assert section in spec, f"dswd_household_children.md lacks {section!r}"

    def test_demo_specification_links_its_adr(self):
        spec = (ROOT / "docs" / "specs" / "dswd_household_children.md").read_text(encoding="utf-8")
        assert "../architecture/decisions/ADR-002-computed-counts-not-stored.md" in spec

    def test_claude_md_points_at_the_specifications(self):
        assert "`docs/specs/`" in (ROOT / "CLAUDE.md").read_text(encoding="utf-8")


class TestDecisionRecords:
    def test_adr_002_is_accepted_and_indexed(self):
        decisions = ROOT / "docs" / "architecture" / "decisions"
        adr = (decisions / "ADR-002-computed-counts-not-stored.md").read_text(encoding="utf-8")
        assert "**Status**: Accepted" in adr
        for section in ("## Context", "## Options Considered", "## Decision", "## Consequences"):
            assert section in adr
        assert "(ADR-002-computed-counts-not-stored.md)" in (decisions / "README.md").read_text(encoding="utf-8")
