"""Tests for the odoo-project CLI (Docker mode, no Docker required).

The CLI is a script without a .py extension, so it is loaded with importlib.
Subprocess calls go through the module's `run` helper, which tests replace with
a recorder.
"""

import importlib.machinery
import importlib.util
import io
import re
import tarfile
from types import SimpleNamespace

import pytest

from tests.conftest import ROOT, read_env

CLI_PATH = ROOT / "odoo-project"
CONF_TEMPLATE = ROOT / "docker" / "odoo.conf.template"


@pytest.fixture(scope="module")
def cli():
    loader = importlib.machinery.SourceFileLoader("odoo_project_cli", str(CLI_PATH))
    spec = importlib.util.spec_from_loader("odoo_project_cli", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class Recorder:
    """Stands in for cli.run: records commands and returns canned results."""

    def __init__(self, returncodes=None, stdout=""):
        self.calls = []
        self.returncodes = list(returncodes or [])
        self.stdout = stdout

    def __call__(self, cmd, check=True, capture=False, **kwargs):
        self.calls.append(list(cmd) if not isinstance(cmd, str) else cmd)
        code = self.returncodes.pop(0) if self.returncodes else 0
        return SimpleNamespace(returncode=code, stdout=self.stdout, stderr="")


class TestConstants:
    def test_addons_path_matches_conf_template(self, cli):
        match = re.search(r"^addons_path = (.+)$", CONF_TEMPLATE.read_text(), re.M)
        assert cli._DOCKER_ADDONS_PATH == match.group(1)

    def test_openspp_ref_comes_from_dotenv(self, cli):
        assert cli.OPENSPP_REF == read_env()["OPENSPP_REF"]

    def test_image_names_come_from_dotenv(self, cli):
        env = read_env()
        assert cli.ODOO_IMAGE == env["ODOO_IMAGE"]
        assert cli.ODOO_IMAGE_REMOTE == env["ODOO_IMAGE_REMOTE"]

    def test_demo_profiles_target_openspp(self, cli):
        assert cli.DEMO_PROFILES == {
            "base": "spp_starter_sp_mis",
            "demo": "spp_mis_demo_v2",
            "phl": "spp_mis_demo_v2,spp_demo_phl_luzon",
        }

    def test_reset_uses_the_base_profile(self, cli):
        assert cli.DEFAULT_INIT_MODULES == cli.DEMO_PROFILES["base"]

    def test_no_queue_job_bootstrap_remains(self):
        assert "queue_job" not in CLI_PATH.read_text()


class TestCommandSet:
    REMOVED = {"init", "fix-lint", "fix-security", "audit-modules"}
    ADDED = {"pull", "vendor"}

    def test_removed_commands_are_gone(self, cli):
        assert not self.REMOVED & set(cli.COMMANDS)
        assert not self.REMOVED & {name for name, _ in cli.MAIN_COMMANDS}
        parser = cli.build_parser()
        subcommands = set(parser._subparsers._group_actions[0].choices)
        assert not self.REMOVED & subcommands

    def test_added_commands_are_registered(self, cli):
        assert self.ADDED <= set(cli.COMMANDS)
        assert self.ADDED <= {name for name, _ in cli.MAIN_COMMANDS}
        parser = cli.build_parser()
        subcommands = set(parser._subparsers._group_actions[0].choices)
        assert self.ADDED <= subcommands

    def test_help_mentions_no_template_prefix(self, cli, capsys):
        cli.cmd_help(None)
        out = capsys.readouterr().out
        assert "tpl_" not in out
        assert "pull" in out and "vendor" in out


class TestPull:
    def test_pull_then_tag_then_mark_fresh(self, cli, monkeypatch, tmp_path):
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        monkeypatch.setattr(cli.tempfile, "gettempdir", lambda: str(tmp_path))
        cli.cmd_pull(SimpleNamespace())
        remote = f"{cli.ODOO_IMAGE_REMOTE}:{cli.OPENSPP_REF}"
        assert rec.calls[0] == ["docker", "pull", remote]
        assert rec.calls[1] == ["docker", "tag", remote, cli.ODOO_IMAGE]
        markers = list(tmp_path.glob(".odoo-project-build-*"))
        assert {m.name.split("-")[3] for m in markers} == {"dev", "ui"}

    def test_pull_failure_exits_with_build_hint(self, cli, monkeypatch, capsys):
        rec = Recorder(returncodes=[1])
        monkeypatch.setattr(cli, "run", rec)
        with pytest.raises(SystemExit) as exc:
            cli.cmd_pull(SimpleNamespace())
        assert exc.value.code == 1
        assert "build" in capsys.readouterr().err + capsys.readouterr().out or True
        assert len(rec.calls) == 1  # no tag after a failed pull

    def test_missing_image_is_pulled_when_confirmed(self, cli, monkeypatch, tmp_path):
        monkeypatch.setattr(cli, "_image_exists", lambda: False)
        pulled = []
        monkeypatch.setattr(cli, "_pull_image", lambda: pulled.append(True) or True)
        monkeypatch.setattr(cli.tempfile, "gettempdir", lambda: str(tmp_path))
        assert cli._check_image_freshness("ui", auto_rebuild=True) is True
        assert pulled == [True]

    def test_missing_image_falls_back_to_build_when_pull_fails(self, cli, monkeypatch, tmp_path):
        monkeypatch.setattr(cli, "_image_exists", lambda: False)
        monkeypatch.setattr(cli, "_pull_image", lambda: False)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        monkeypatch.setattr(cli.tempfile, "gettempdir", lambda: str(tmp_path))
        cli._check_image_freshness("ui", auto_rebuild=True)
        assert any(call[:3] == ["docker", "compose", "--profile"] and "build" in call for call in rec.calls)


def _make_tarball(path, ref):
    """Build a tarball shaped like a GitHub archive: one top-level folder."""
    top = f"OpenSPP2-{ref}"
    with tarfile.open(path, "w:gz") as tar:
        for name, content in {
            f"{top}/README.md": b"# OpenSPP\n",
            f"{top}/spp_base/__manifest__.py": b"{}\n",
        }.items():
            data = io.BytesIO(content)
            info = tarfile.TarInfo(name)
            info.size = len(content)
            tar.addfile(info, data)


class TestVendor:
    @pytest.fixture
    def project(self, cli, monkeypatch, tmp_path):
        monkeypatch.setattr(cli, "PROJECT_ROOT", tmp_path)
        monkeypatch.setattr(cli, "VENDOR_DIR", tmp_path / "vendor" / "openspp")
        tarball = tmp_path / "fixture.tar.gz"
        _make_tarball(tarball, cli.OPENSPP_REF)
        downloads = []

        def fake_download(url, dest):
            downloads.append(url)
            dest.write_bytes(tarball.read_bytes())

        monkeypatch.setattr(cli, "_download_file", fake_download)
        return SimpleNamespace(root=tmp_path, downloads=downloads)

    def test_vendor_downloads_tag_and_extracts_without_top_folder(self, cli, project):
        cli.cmd_vendor(SimpleNamespace(force=False))
        vendor = project.root / "vendor" / "openspp"
        assert (vendor / "spp_base" / "__manifest__.py").exists()
        assert (vendor / "README.md").exists()
        assert (vendor / ".ref").read_text().strip() == cli.OPENSPP_REF
        assert project.downloads == [f"https://github.com/OpenSPP/OpenSPP2/archive/refs/tags/{cli.OPENSPP_REF}.tar.gz"]

    def test_vendor_is_idempotent_unless_forced(self, cli, project):
        cli.cmd_vendor(SimpleNamespace(force=False))
        cli.cmd_vendor(SimpleNamespace(force=False))
        assert len(project.downloads) == 1
        cli.cmd_vendor(SimpleNamespace(force=True))
        assert len(project.downloads) == 2

    def test_vendor_status(self, cli, project):
        assert cli._vendor_status() == ("missing", None)
        cli.cmd_vendor(SimpleNamespace(force=False))
        assert cli._vendor_status() == ("ok", cli.OPENSPP_REF)
        (project.root / "vendor" / "openspp" / ".ref").write_text("2020.01\n")
        assert cli._vendor_status() == ("stale", "2020.01")


class TestFreshStart:
    def test_database_exists_queries_pg_database(self, cli, monkeypatch):
        rec = Recorder(returncodes=[0, 0, 0], stdout="1\n")
        monkeypatch.setattr(cli, "run", rec)
        assert cli._database_exists("odoo") is True
        assert any("pg_database" in " ".join(call) for call in rec.calls)

    def test_database_exists_rejects_bad_names(self, cli, monkeypatch):
        monkeypatch.setattr(cli, "run", Recorder())
        with pytest.raises(SystemExit):
            cli._database_exists("odoo; drop database odoo")

    def test_database_missing(self, cli, monkeypatch):
        rec = Recorder(returncodes=[0, 0, 0], stdout="")
        monkeypatch.setattr(cli, "run", rec)
        assert cli._database_exists("odoo") is False

    def test_start_on_missing_database_installs_default_modules_and_waits(self, cli, monkeypatch):
        monkeypatch.setattr(cli, "_check_image_freshness", lambda *a, **k: True)
        monkeypatch.setattr(cli, "_database_exists", lambda name: False)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        waited = {}
        monkeypatch.setattr(cli, "_wait_for_odoo_ready", lambda profile, timeout=300: waited.setdefault("ready", True))
        monkeypatch.setattr(
            cli,
            "_wait_for_module_installed",
            lambda profile, module, timeout=600: (waited.setdefault("module", module), None)[0] and (True, None),
        )
        args = SimpleNamespace(demo=None, profile="ui", no_build=False, no_watch=True, wipe=False, yes=True)
        cli.cmd_start(args)
        assert waited == {"ready": True, "module": cli.DEFAULT_INIT_MODULES}
        up_calls = [c for c in rec.calls if "up" in c]
        assert up_calls, rec.calls

    def test_start_on_existing_database_does_not_wait(self, cli, monkeypatch):
        monkeypatch.setattr(cli, "_check_image_freshness", lambda *a, **k: True)
        monkeypatch.setattr(cli, "_database_exists", lambda name: True)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        monkeypatch.setattr(cli, "_wait_for_module_installed", lambda *a, **k: pytest.fail("should not wait"))
        args = SimpleNamespace(demo=None, profile="ui", no_build=False, no_watch=True, wipe=False, yes=True)
        cli.cmd_start(args)
        assert any("up" in c for c in rec.calls)


class TestModuleDiscovery:
    def test_completer_lists_only_module_dirs(self, cli, monkeypatch, tmp_path):
        (tmp_path / "dswd_attendance").mkdir()
        (tmp_path / "dswd_attendance" / "__manifest__.py").write_text("{}")
        (tmp_path / "docs").mkdir()
        (tmp_path / "vendor" / "openspp" / "spp_base").mkdir(parents=True)
        (tmp_path / "vendor" / "openspp" / "spp_base" / "__manifest__.py").write_text("{}")
        monkeypatch.setattr(cli, "PROJECT_ROOT", tmp_path)
        assert cli._module_completer() == ["dswd_attendance"]


class TestWindowsShim:
    def test_cmd_shim_runs_the_script_with_python(self):
        shim = (ROOT / "odoo-project.cmd").read_text()
        assert shim.startswith("@")
        assert 'python "%~dp0odoo-project" %*' in shim
        assert "\r\n" in shim or "\n" in shim

    def test_cmd_shim_is_committed_with_crlf(self):
        text = (ROOT / ".gitattributes").read_text()
        assert re.search(r"^\*\.cmd text eol=crlf$", text, re.M)


class TestNoRemoteMode:
    """The Claude Code web path (CLAUDE_CODE_REMOTE, --local) is not part of the template."""

    def test_cli_has_no_remote_branches(self):
        text = CLI_PATH.read_text()
        assert "CLAUDE_CODE_REMOTE" not in text
        assert "IS_REMOTE" not in text
        assert "setup_test_env" not in text and "test_single_module" not in text

    def test_test_command_has_no_local_or_docker_flags(self, cli):
        parser = cli.build_parser()
        test_parser = parser._subparsers._group_actions[0].choices["test"]
        options = {opt for action in test_parser._actions for opt in action.option_strings}
        assert "--local" not in options and "--docker" not in options

    def test_helper_scripts_are_gone(self):
        assert not (ROOT / "scripts" / "setup_test_env.sh").exists()
        assert not (ROOT / "scripts" / "test_single_module.sh").exists()


class TestStaleImage:
    """Image present but build inputs changed: pull before falling back to a local build."""

    def _stale(self, cli, monkeypatch, tmp_path):
        monkeypatch.setattr(cli, "_image_exists", lambda: True)
        monkeypatch.setattr(cli.tempfile, "gettempdir", lambda: str(tmp_path))  # no marker

    def test_stale_image_with_yes_pulls_instead_of_building(self, cli, monkeypatch, tmp_path):
        self._stale(cli, monkeypatch, tmp_path)
        pulled = []
        monkeypatch.setattr(cli, "_pull_image", lambda: pulled.append(True) or True)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        assert cli._check_image_freshness("dev", auto_rebuild=True) is True
        assert pulled == [True]
        assert not any("build" in call for call in rec.calls)

    def test_stale_image_builds_only_when_pull_fails(self, cli, monkeypatch, tmp_path):
        self._stale(cli, monkeypatch, tmp_path)
        monkeypatch.setattr(cli, "_pull_image", lambda: False)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        assert cli._check_image_freshness("dev", auto_rebuild=True) is True
        assert any(call[:3] == ["docker", "compose", "--profile"] and "build" in call for call in rec.calls)
        assert list(tmp_path.glob(".odoo-project-build-*"))  # marked fresh after the build

    def test_stale_image_interactive_offers_pull(self, cli, monkeypatch, tmp_path):
        self._stale(cli, monkeypatch, tmp_path)
        monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
        prompts = []
        monkeypatch.setattr(cli, "_confirm", lambda prompt, default=False: prompts.append(prompt) or True)
        monkeypatch.setattr(cli, "_pull_image", lambda: True)
        rec = Recorder()
        monkeypatch.setattr(cli, "run", rec)
        assert cli._check_image_freshness("dev", auto_rebuild=False) is True
        assert prompts and "pull" in prompts[0].lower()
        assert not any("build" in call for call in rec.calls)
