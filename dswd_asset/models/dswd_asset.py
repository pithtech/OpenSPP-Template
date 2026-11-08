# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DswdAsset(models.Model):
    """An IT asset (laptop, desktop, printer) and who looks after it.

    A new model: Odoo creates the table ``dswd_asset`` from this class.
    """

    _name = "dswd.asset"
    _description = "IT Asset"
    _order = "name"

    name = fields.Char(string="Asset Tag", required=True)
    model_name = fields.Char(string="Make and Model")
    # Hard-coded on purpose: Module 4 replaces this pattern with a vocabulary.
    asset_type = fields.Selection(
        [("laptop", "Laptop"), ("desktop", "Desktop"), ("printer", "Printer"), ("other", "Other")],
        required=True,
        default="laptop",
    )
    custodian_id = fields.Many2one("res.users", string="Custodian", default=lambda self: self.env.user)
    purchase_date = fields.Date()
    warranty_end_date = fields.Date()
    is_in_use = fields.Boolean(default=True)
    is_under_warranty = fields.Boolean(compute="_compute_is_under_warranty")

    @api.depends("warranty_end_date")
    def _compute_is_under_warranty(self):
        today = fields.Date.context_today(self)
        for asset in self:
            asset.is_under_warranty = bool(asset.warranty_end_date and asset.warranty_end_date >= today)

    @api.constrains("purchase_date", "warranty_end_date")
    def _check_warranty_after_purchase(self):
        """A warranty cannot end before the asset was bought."""
        for asset in self:
            if asset.purchase_date and asset.warranty_end_date and asset.warranty_end_date < asset.purchase_date:
                raise ValidationError(_("The warranty end date must be on or after the purchase date."))

    def action_assign_to_me(self):
        """Form button: the ORM write in one line. ``self`` is the asset(s) the button was pressed on."""
        self.write({"custodian_id": self.env.user.id})

    @api.model
    def find_warranty_expiring(self, days=30):
        """Assets still in use whose warranty ends within ``days``: a search with a domain.

        ``@api.model`` means the method works on the model, not on records:
        ``env["dswd.asset"].find_warranty_expiring(30)``.
        """
        today = fields.Date.context_today(self)
        return self.search(
            [
                ("is_in_use", "=", True),
                ("warranty_end_date", ">=", today),
                ("warranty_end_date", "<=", fields.Date.add(today, days=days)),
            ],
            order="warranty_end_date",
        )
