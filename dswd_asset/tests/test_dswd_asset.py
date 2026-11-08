# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from datetime import date, timedelta

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAsset(TransactionCase):
    """The asset model: defaults, the computed warranty flag and the date constraint."""

    def setUp(self):
        super().setUp()
        self.Asset = self.env["dswd.asset"]
        self.asset = self.Asset.create({"name": "LT-0001", "model_name": "Dell Latitude 5440"})

    def test_defaults(self):
        """A new asset is a laptop, in use, and the current user is its custodian."""
        self.assertEqual(self.asset.asset_type, "laptop")
        self.assertTrue(self.asset.is_in_use)
        self.assertEqual(self.asset.custodian_id, self.env.user)

    def test_warranty_flag_follows_the_end_date(self):
        """The flag is true while the warranty end date is today or later."""
        self.asset.warranty_end_date = date.today() + timedelta(days=30)
        self.assertTrue(self.asset.is_under_warranty)
        self.asset.warranty_end_date = date.today() - timedelta(days=1)
        self.assertFalse(self.asset.is_under_warranty)

    def test_warranty_before_purchase_is_refused(self):
        """A warranty that ends before the purchase date is a data-entry error and is refused."""
        with self.assertRaises(ValidationError):
            self.asset.write({"purchase_date": date(2026, 1, 10), "warranty_end_date": date(2025, 12, 31)})

    def test_menu_action_and_views_resolve(self):
        """The menu opens an action on the model whose form shows the custodian."""
        action = self.env.ref("dswd_asset.action_dswd_asset")
        self.assertEqual(action.res_model, "dswd.asset")
        self.assertEqual(self.env.ref("dswd_asset.menu_dswd_asset").action.id, action.id)
        arch = self.Asset.get_view(view_type="form")["arch"]
        self.assertIn('name="custodian_id"', arch)

    def test_assign_to_me_makes_the_current_user_the_custodian(self):
        """The form button writes the current user into custodian_id (the ORM write in one line)."""
        officer = self.env["res.users"].create(
            {
                "name": "asset_officer",
                "login": "asset_officer",
                "email": "asset_officer@example.test",
                "group_ids": [Command.set([self.env.ref("dswd_asset.group_asset_officer").id])],
            }
        )
        self.asset.custodian_id = self.env.ref("base.user_admin")
        self.asset.with_user(officer).action_assign_to_me()
        self.assertEqual(self.asset.custodian_id, officer)

    def test_find_warranty_expiring_returns_only_assets_ending_soon(self):
        """A model method built on search(): warranties ending within the window, still in use."""
        soon = self.Asset.create({"name": "LT-SOON", "warranty_end_date": date.today() + timedelta(days=10)})
        self.Asset.create({"name": "LT-LATER", "warranty_end_date": date.today() + timedelta(days=200)})
        self.Asset.create({"name": "LT-GONE", "warranty_end_date": date.today() - timedelta(days=5)})
        retired = self.Asset.create({"name": "LT-RETIRED", "warranty_end_date": date.today() + timedelta(days=10)})
        retired.is_in_use = False
        found = self.Asset.find_warranty_expiring(days=30)
        self.assertEqual(found, soon)
