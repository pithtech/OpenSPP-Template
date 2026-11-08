# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAssetReport(TransactionCase):
    """The Asset Sheet report renders the asset's data and is offered in the Print menu."""

    def setUp(self):
        super().setUp()
        self.asset = self.env["dswd.asset"].create(
            {"name": "LT-0001", "model_name": "Dell Latitude 5440", "asset_type": "laptop"}
        )

    def test_report_renders_the_asset(self):
        """Rendering the QWeb template as HTML (the step before PDF) shows the tag and the model."""
        html, _report_type = self.env["ir.actions.report"]._render_qweb_html(
            "dswd_asset.action_report_dswd_asset", self.asset.ids
        )
        text = html.decode()
        self.assertIn("LT-0001", text)
        self.assertIn("Dell Latitude 5440", text)

    def test_report_is_bound_to_the_print_menu(self):
        report = self.env.ref("dswd_asset.action_report_dswd_asset")
        self.assertEqual(report.report_type, "qweb-pdf")
        self.assertEqual(report.binding_model_id.model, "dswd.asset")
