# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
from odoo.tests import tagged

from odoo.addons.spp_registry.tests.common import RegistryCommon

NAMESPACE = "urn:dswd:4ps:well-being-level"


@tagged("post_install", "-at_install")
class TestWellBeingVocabulary(RegistryCommon):
    """The module ships the SWDI well-being level vocabulary."""

    def test_vocabulary_is_a_system_vocabulary(self):
        """The vocabulary exists under its namespace and is locked against UI edits."""
        vocabulary = self.env["spp.vocabulary"].search([("namespace_uri", "=", NAMESPACE)])
        self.assertEqual(len(vocabulary), 1)
        self.assertTrue(vocabulary.is_system)

    def test_three_levels_in_swdi_order(self):
        """Survival, Subsistence and Self-Sufficient resolve by code and sort as SWDI levels 1 to 3."""
        codes = [self.VocabCode.get_code(NAMESPACE, code) for code in ("survival", "subsistence", "self_sufficient")]
        self.assertTrue(all(codes), "every level must resolve by namespace and code")
        self.assertEqual([c.display for c in codes], ["Survival", "Subsistence", "Self-Sufficient"])
        self.assertEqual([c.sequence for c in codes], sorted(c.sequence for c in codes))
