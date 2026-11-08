# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAssetAccess(TransactionCase):
    """Who may do what: viewer reads, officer creates and edits, manager also deletes, admin sees everything."""

    def setUp(self):
        super().setUp()
        self.viewer = self._make_user("asset_viewer", "dswd_asset.group_asset_viewer")
        self.officer = self._make_user("asset_officer", "dswd_asset.group_asset_officer")
        self.manager = self._make_user("asset_manager", "dswd_asset.group_asset_manager")
        self.asset = self.env["dswd.asset"].create({"name": "PR-0001", "asset_type": "printer"})

    def _make_user(self, login, group_xmlid):
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "email": f"{login}@example.test",
                "group_ids": [Command.set([self.env.ref(group_xmlid).id])],
            }
        )

    def test_viewer_reads_but_cannot_create(self):
        assets = self.env["dswd.asset"].with_user(self.viewer)
        self.assertEqual(assets.search_count([("name", "=", "PR-0001")]), 1)
        with self.assertRaises(AccessError):
            assets.create({"name": "LT-0002"})

    def test_officer_creates_and_edits_but_cannot_delete(self):
        assets = self.env["dswd.asset"].with_user(self.officer)
        created = assets.create({"name": "LT-0002"})
        created.write({"model_name": "HP ProBook"})
        self.assertEqual(created.model_name, "HP ProBook")
        with self.assertRaises(AccessError):
            created.unlink()

    def test_manager_deletes(self):
        assets = self.env["dswd.asset"].with_user(self.manager)
        created = assets.create({"name": "LT-0003"})
        created.unlink()
        self.assertEqual(assets.search_count([("name", "=", "LT-0003")]), 0)

    def test_admin_is_a_manager_through_the_openspp_admin_group(self):
        """The admin link in groups.xml is what lets the admin user open the app without extra setup."""
        admin = self.env.ref("base.user_admin")
        self.assertIn(self.env.ref("dswd_asset.group_asset_manager"), admin.all_group_ids)
