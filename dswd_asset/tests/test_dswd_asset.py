# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from datetime import date, timedelta

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
