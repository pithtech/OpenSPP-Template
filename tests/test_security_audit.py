"""The security audit must judge dswd_* modules against OpenSPP's spp_security, not a project module that
this template does not have."""

import subprocess
import sys

from tests.conftest import ROOT

SCRIPT = ROOT / "scripts" / "security_audit.py"

MANIFEST = """{{
    "name": "Test",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": {depends},
    "data": ["security/groups.xml", "security/ir.model.access.csv"],
    "installable": True,
}}
"""

GROUPS = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="category_dswd_thing" model="ir.module.category">
        <field name="name">DSWD 4Ps Thing</field>
    </record>
    <record id="privilege_thing_officer" model="res.groups.privilege">
        <field name="name">Thing Officer</field>
        <field name="category_id" ref="category_dswd_thing"/>
    </record>
    <record id="group_thing_manager" model="res.groups">
        <field name="name">Thing: Manager</field>
        <field name="privilege_id" ref="privilege_thing_officer"/>
    </record>
    {admin_link}
</odoo>
"""

ADMIN_LINK = """<record id="spp_security.group_spp_admin" model="res.groups">
        <field name="implied_ids" eval="[Command.link(ref('group_thing_manager'))]"/>
    </record>"""


def _module(tmp_path, name, depends, groups=None):
    module = tmp_path / name
    (module / "security").mkdir(parents=True)
    (module / "__manifest__.py").write_text(MANIFEST.format(depends=depends))
    (module / "security" / "ir.model.access.csv").write_text(
        "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
    )
    if groups is not None:
        (module / "security" / "groups.xml").write_text(groups)
    return module


def _audit(tmp_path, name):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), name, "--base-path", str(tmp_path), "--report", "--format", "text"],
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def test_module_without_groups_needs_no_security_dependency(tmp_path):
    """dswd_wellbeing-style module: fields on upstream models, no groups, depends on spp_registry only."""
    _module(tmp_path, "dswd_plain", '["spp_registry", "spp_vocabulary"]')
    out = _audit(tmp_path, "dswd_plain")
    assert "dswd_security" not in out
    assert "0 errors, 0 warnings" in out or "Warnings: 0" in out


def test_module_with_groups_must_depend_on_spp_security(tmp_path):
    _module(tmp_path, "dswd_groups", '["spp_registry"]', GROUPS.format(admin_link=ADMIN_LINK))
    out = _audit(tmp_path, "dswd_groups")
    assert "spp_security" in out and "depend" in out
    assert "dswd_security" not in out


def test_module_with_groups_and_spp_security_link_is_clean(tmp_path):
    _module(tmp_path, "dswd_linked", '["spp_registry", "spp_security"]', GROUPS.format(admin_link=ADMIN_LINK))
    out = _audit(tmp_path, "dswd_linked")
    assert "dswd_security" not in out
    assert "category" not in out.lower() or "Errors: 0" in out
    assert "Errors: 0" in out or "0 errors" in out


def test_manager_group_without_admin_link_is_reported_against_spp_security(tmp_path):
    _module(tmp_path, "dswd_nolink", '["spp_registry", "spp_security"]', GROUPS.format(admin_link=""))
    out = _audit(tmp_path, "dswd_nolink")
    assert "spp_security.group_spp_admin" in out
    assert "dswd_security" not in out


def _run_script(tmp_path, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--base-path", str(tmp_path)],
        capture_output=True,
        text=True,
    )


def test_several_modules_can_be_audited_in_one_call(tmp_path):
    """`./odoo-project audit-security dswd_a dswd_b` passes every module name to the script."""
    _module(tmp_path, "dswd_one", '["spp_registry"]')
    _module(tmp_path, "dswd_two", '["spp_registry"]')
    result = _run_script(tmp_path, "dswd_one", "dswd_two", "--format", "text")
    assert result.returncode == 0, result.stderr
    assert "dswd_one" in result.stdout and "dswd_two" in result.stdout


def test_named_module_with_report_audits_only_that_module(tmp_path):
    _module(tmp_path, "dswd_one", '["spp_registry"]')
    _module(tmp_path, "dswd_two", '["spp_registry"]')
    result = _run_script(tmp_path, "dswd_one", "--report", "--format", "text")
    assert result.returncode == 0, result.stderr
    assert "dswd_one" in result.stdout and "dswd_two" not in result.stdout


def test_json_format_prints_json(tmp_path):
    import json

    _module(tmp_path, "dswd_one", '["spp_registry"]')
    result = _run_script(tmp_path, "dswd_one", "--format", "json")
    assert result.returncode == 0, result.stderr
    json.loads(result.stdout)
