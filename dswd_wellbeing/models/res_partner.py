# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

WELL_BEING_NAMESPACE = "urn:dswd:4ps:well-being-level"


class ResPartner(models.Model):
    """Add the SWDI well-being level to 4Ps households.

    Households are ``res.partner`` records with ``is_registrant`` and
    ``is_group`` set, so the field lives on the upstream model rather than on
    a new one.
    """

    _inherit = "res.partner"

    dswd_well_being_level_id = fields.Many2one(
        comodel_name="spp.vocabulary.code",
        string="Well-Being Level",
        domain=[("namespace_uri", "=", WELL_BEING_NAMESPACE)],
        ondelete="restrict",
        help="SWDI level from the latest assessment: Survival, Subsistence or Self-Sufficient.",
    )
