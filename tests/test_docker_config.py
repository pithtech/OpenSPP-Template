"""Tests for the Docker layer: the OpenSPP pin, addons path, and compose services.

These run without Docker. The one test that calls `docker compose config` is
marked slow and skips when Docker is not available.
"""

import re
import shutil
import subprocess

import pytest
import yaml

from tests.conftest import ROOT, read_env

DOCKERFILE = ROOT / "docker" / "Dockerfile"
CONF_TEMPLATE = ROOT / "docker" / "odoo.conf.template"
COMPOSE = ROOT / "docker-compose.yml"
ENTRYPOINT = ROOT / "docker" / "entrypoint.sh"

EXPECTED_ADDONS_PATH = ",".join(
    [
        "/opt/odoo/odoo/addons",
        "/opt/odoo/odoo/odoo/addons",
        "/mnt/extra-addons/custom",
        "/mnt/extra-addons/openspp",
        "/mnt/extra-addons/server-ux",
        "/mnt/extra-addons/server-tools",
        "/mnt/extra-addons/odoo-job-worker",
        "/mnt/extra-addons/server-backend",
        "/mnt/extra-addons/rest-framework",
        "/mnt/extra-addons/muk-it",
    ]
)


class TestOpenSPPPin:
    def test_env_pins_a_calendar_release(self):
        env = read_env()
        assert re.fullmatch(r"\d{4}\.\d{2}", env["OPENSPP_REF"]), env["OPENSPP_REF"]

    def test_dockerfile_default_matches_env(self):
        env = read_env()
        match = re.search(r"^ARG OPENSPP_REF=(\S+)$", DOCKERFILE.read_text(), re.M)
        assert match, "Dockerfile must declare ARG OPENSPP_REF"
        assert match.group(1) == env["OPENSPP_REF"]

    def test_dockerfile_downloads_openspp_tag_into_extra_addons(self):
        text = DOCKERFILE.read_text()
        assert "github.com/OpenSPP/OpenSPP2/archive/refs/tags/${OPENSPP_REF}.tar.gz" in text
        assert "/opt/extra-addons/openspp" in text

    def test_dockerfile_installs_openspp_requirements_from_the_tarball(self):
        text = DOCKERFILE.read_text()
        assert "/opt/extra-addons/openspp/requirements.txt" in text
        assert "/opt/extra-addons/openspp/docker/requirements.txt" in text

    def test_dockerfile_uses_job_worker_not_oca_queue(self):
        text = DOCKERFILE.read_text()
        assert "OpenSPP/odoo-job-worker" in text
        assert "OCA/queue" not in text

    def test_dockerfile_has_no_production_target(self):
        assert "AS production" not in DOCKERFILE.read_text()


class TestAddonsPath:
    def test_conf_template_addons_path(self):
        match = re.search(r"^addons_path = (.+)$", CONF_TEMPLATE.read_text(), re.M)
        assert match
        assert match.group(1) == EXPECTED_ADDONS_PATH

    def test_custom_precedes_openspp(self):
        parts = EXPECTED_ADDONS_PATH.split(",")
        assert parts.index("/mnt/extra-addons/custom") < parts.index("/mnt/extra-addons/openspp")

    def test_no_queue_job_server_wide_module(self):
        text = CONF_TEMPLATE.read_text()
        assert "queue_job" not in text
        assert re.search(r"^server_wide_modules = base,web$", text, re.M)

    def test_db_maxconn_configured(self):
        assert "db_maxconn = ${ODOO_DB_MAXCONN}" in CONF_TEMPLATE.read_text()
        assert "ODOO_DB_MAXCONN" in ENTRYPOINT.read_text()

    def test_entrypoint_has_no_queue_job_channels(self):
        assert "ODOO_QUEUE_JOB_CHANNELS" not in ENTRYPOINT.read_text()


@pytest.fixture(scope="module")
def compose():
    return yaml.safe_load(COMPOSE.read_text())


class TestCompose:
    def test_services_present(self, compose):
        assert set(compose["services"]) == {"db", "odoo-app", "odoo-dev", "jobworker", "test"}

    def test_odoo_services_share_the_configurable_image(self, compose):
        for name in ("odoo-app", "odoo-dev", "jobworker", "test"):
            assert compose["services"][name]["image"] == "${ODOO_IMAGE:-openspp-template-dev}", name

    def test_build_passes_openspp_ref(self, compose):
        for name in ("odoo-app", "odoo-dev"):
            build = compose["services"][name]["build"]
            assert build["target"] == "dev"
            assert build["args"]["OPENSPP_REF"] == "${OPENSPP_REF}"

    def test_participant_code_is_mounted_read_only(self, compose):
        for name in ("odoo-app", "odoo-dev", "jobworker", "test"):
            volumes = compose["services"][name]["volumes"]
            assert any(v.startswith(".:/mnt/extra-addons/custom:ro") for v in volumes), name

    def test_jobworker_runs_in_ui_and_dev_profiles(self, compose):
        svc = compose["services"]["jobworker"]
        assert set(svc["profiles"]) == {"ui", "dev"}
        assert "job_worker_runner.py" in " ".join(svc["command"])

    def test_default_init_module_is_the_sp_mis_starter(self, compose):
        env = compose["services"]["odoo-app"]["environment"]
        assert env["ODOO_INIT_MODULES"] == "${ODOO_INIT_MODULES:-spp_starter_sp_mis}"

    def test_db_is_postgis_18(self, compose):
        assert compose["services"]["db"]["image"].startswith("postgis/postgis:18-")

    @pytest.mark.slow
    def test_compose_config_is_valid(self):
        if not shutil.which("docker"):
            pytest.skip("docker not installed")
        result = subprocess.run(
            ["docker", "compose", "--profile", "ui", "config", "--quiet"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr


@pytest.fixture(scope="module")
def ci():
    return (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")


class TestCIParticipantFlow:
    """The smoke job must walk the participant's path through the CLI and fail on a broken stylesheet build."""

    def test_smoke_runs_the_cli_participant_flow(self, ci):
        for step in ("./odoo-project vendor", "./odoo-project start", "./odoo-project install dswd_wellbeing"):
            assert step in ci, step

    def test_smoke_fails_on_the_css_error_stub(self, ci):
        assert "css error" in ci.lower()
        assert "assetsbundle" in ci

    def test_cli_changes_trigger_the_smoke_job(self, ci):
        assert "odoo-project" in ci.split("image_changed=true")[0].rsplit("grep", 1)[-1]
