"""Checks on the project lint scripts themselves: honest CLI options and doc links that resolve."""

import re
import subprocess
import sys

from tests.conftest import ROOT

LINT_DIR = ROOT / "scripts" / "lint"


def _heading_slugs(path):
    """GitHub-style anchors for the headings in a Markdown file."""
    slugs = set()
    for heading in re.findall(r"^#+\s+(.*)$", path.read_text(encoding="utf-8"), re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")
        slugs.add(slug)
    return slugs


class TestDocLinks:
    def test_every_doc_link_resolves(self):
        broken = []
        for script in LINT_DIR.glob("*.py"):
            for link in re.findall(r'doc_link="([^"]+)"', script.read_text(encoding="utf-8")):
                path, _, anchor = link.partition("#")
                target = ROOT / path
                if not target.exists():
                    broken.append(f"{script.name}: {link} (file missing)")
                elif anchor and anchor not in _heading_slugs(target):
                    broken.append(f"{script.name}: {link} (no such heading)")
        assert broken == []


class TestNamingChecker:
    def test_no_dead_fix_option(self):
        """check_naming never had an auto-fix; the option must not be advertised."""
        result = subprocess.run(
            [sys.executable, str(LINT_DIR / "check_naming.py"), "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "--fix" not in result.stdout
        source = (LINT_DIR / "check_naming.py").read_text(encoding="utf-8")
        assert "_apply_fixes" not in source
        assert "TODO" not in source


class TestRootDirChecker:
    """A top-level folder named like an Odoo SCSS import root breaks every stylesheet build."""

    def _run(self, root):
        return subprocess.run(
            [sys.executable, str(LINT_DIR / "check_root_dirs.py"), "--root", str(root)],
            capture_output=True,
            text=True,
        )

    def test_clean_root_passes(self, tmp_path):
        (tmp_path / "dswd_wellbeing").mkdir()
        result = self._run(tmp_path)
        assert result.returncode == 0, result.stdout + result.stderr

    def test_reserved_folder_fails_and_is_named(self, tmp_path):
        (tmp_path / "helpers").mkdir()
        (tmp_path / "vendor").mkdir()
        result = self._run(tmp_path)
        assert result.returncode == 1
        assert "helpers" in result.stdout and "vendor" in result.stdout
        assert "upstream" in result.stdout  # the way out for a stale checkout
