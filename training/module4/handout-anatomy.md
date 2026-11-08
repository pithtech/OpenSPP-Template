# Module 4 Handout: Anatomy of a `dswd_*` Module

Fill in the blanks during the session. Keep this page; it is your desk reference afterwards.

## 1. The requirement

The SWDI assessment places every 4Ps household at one of three levels: Survival, Subsistence, Self-Sufficient. Since EO
120 (2026) the level decides whether a household stays in the program past seven years. We add the level to the
household record in OpenSPP.

## 2. The file map (fill in the role of each file)

```
dswd_wellbeing/
├── __manifest__.py                        ____________________________________________
├── __init__.py                            ____________________________________________
├── data/vocabulary_well_being_level.xml   ____________________________________________
├── models/__init__.py                     ____________________________________________
├── models/res_partner.py                  ____________________________________________
├── views/res_partner_views.xml            ____________________________________________
├── security/ir.model.access.csv           ____________________________________________
├── tests/test_wellbeing.py                ____________________________________________
└── readme/DESCRIPTION.md                  ____________________________________________
```

## 3. The three rules

1. **Never edit `vendor/openspp/`.** Read it; extend it from your module. The next release overwrites it.
2. **Inherit, do not redefine.** `_inherit = "res.partner"` adds to the household; `_name` would create a new table. New
   fields on upstream models are prefixed `dswd_`.
3. **A file not listed in `__manifest__.py` does not exist.** Data and view files load only if they are in `data`.

## 4. The loop

| You changed                                                             | Run                                                           | Then                    |
| ----------------------------------------------------------------------- | ------------------------------------------------------------- | ----------------------- |
| Nothing yet, new module                                                 | `./odoo-project install dswd_wellbeing`                       | Apps shows it installed |
| A Python method body, an existing view                                  | nothing (dev profile reloads)                                 | refresh the browser     |
| `__manifest__.py`, `data/`, `security/`, a new field, a new view record | `./odoo-project update`                                       | refresh                 |
| A record in a `noupdate="1"` data file                                  | delete the record, then `update`; or `stop -v -y` and `start` |                         |
| A test                                                                  | `./odoo-project test dswd_wellbeing`                          | read the summary line   |

Logs: `./odoo-project logs`. Three lines to recognise: `Loading module dswd_wellbeing`, `odoo.tools.convert.ParseError`,
`cannot be located in parent view`.

## 5. The five mistakes (fill in the diagnostic you saw)

| Mistake                                                  | Symptom                              | How you find it                  |
| -------------------------------------------------------- | ------------------------------------ | -------------------------------- |
| Data file not in the manifest                            | clean update, nothing appears        | **************\_\_************** |
| Invalid value in a data file (`domain`)                  | `ParseError`, registry fails to load | **************\_\_************** |
| Import missing in `models/__init__.py`                   | no error, field absent               | **************\_\_************** |
| XPath anchor misspelled                                  | `cannot be located in parent view`   | **************\_\_************** |
| `restart` instead of `update`, or `noupdate` data edited | change never shows                   | **************\_\_************** |

## 6. The code, step by step

### Step 0: the manifest (`__manifest__.py`)

```python
{
    "name": "DSWD 4Ps: Household Well-Being Level",
    "category": "DSWD 4Ps/Registry",
    "version": "19.0.1.0.0",
    "author": "DSWD",
    "license": "LGPL-3",
    "depends": ["spp_registry", "spp_vocabulary"],
    "data": [
        "security/ir.model.access.csv",
        "data/vocabulary_well_being_level.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
```

### Step 1: the vocabulary (`data/vocabulary_well_being_level.xml`)

```xml
<odoo noupdate="1">
    <record id="vocab_well_being_level" model="spp.vocabulary">
        <field name="name">4Ps Well-Being Level</field>
        <field name="namespace_uri">urn:dswd:4ps:well-being-level</field>
        <field name="is_system" eval="True" />
        <field name="domain">social_assistance</field>
    </record>

    <record id="code_well_being_survival" model="spp.vocabulary.code">
        <field name="vocabulary_id" ref="vocab_well_being_level" />
        <field name="code">survival</field>
        <field name="display">Survival</field>
        <field name="definition">SWDI level 1: the household cannot meet basic needs without assistance.</field>
        <field name="sequence">10</field>
    </record>
    <!-- subsistence (20) and self_sufficient (30) follow the same shape -->
</odoo>
```

`domain` must be one of `core`, `social_assistance`, `social_insurance`, `labor`, `disability`, `agriculture`, `health`,
`education`.

### Step 2: the field (`models/res_partner.py`, plus `from . import res_partner` in `models/__init__.py` and

`from . import models` in `__init__.py`)

```python
from odoo import fields, models

WELL_BEING_NAMESPACE = "urn:dswd:4ps:well-being-level"


class ResPartner(models.Model):
    _inherit = "res.partner"

    dswd_well_being_level_id = fields.Many2one(
        comodel_name="spp.vocabulary.code",
        string="Well-Being Level",
        domain=[("namespace_uri", "=", WELL_BEING_NAMESPACE)],
        ondelete="restrict",
    )
```

### Step 3: the view (`views/res_partner_views.xml`)

```xml
<odoo>
    <record id="view_res_partner_form_wellbeing" model="ir.ui.view">
        <field name="name">res.partner.form.dswd.wellbeing</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="spp_registry.view_individuals_form" />
        <field name="arch" type="xml">
            <xpath expr="//group[@name='group_tags_section']" position="after">
                <group name="dswd_4ps_section" string="4Ps">
                    <field name="dswd_well_being_level_id" options="{'no_create': True, 'no_open': True}" />
                </group>
            </xpath>
        </field>
    </record>
</odoo>
```

Find the anchor first: `grep -n 'name="group_' vendor/openspp/spp_registry/views/individual_views.xml`.

### Step 4: the security file and the tests

`security/ir.model.access.csv` has only its header: no new model, no rows.

```python
from odoo.tests import tagged

from odoo.addons.spp_registry.tests.common import RegistryCommon

NAMESPACE = "urn:dswd:4ps:well-being-level"


@tagged("post_install", "-at_install")
class TestHouseholdWellBeing(RegistryCommon):
    def test_household_stores_a_level(self):
        subsistence = self.VocabCode.get_code(NAMESPACE, "subsistence")
        self.group.dswd_well_being_level_id = subsistence
        self.assertEqual(self.group.dswd_well_being_level_id.display, "Subsistence")
```

`RegistryCommon` gives you `self.group` (a household), two individuals and `self.VocabCode`.

### Step 5: the constraint (written test first)

```python
    @api.constrains("dswd_well_being_level_id")
    def _check_well_being_level_namespace(self):
        for partner in self.filtered("dswd_well_being_level_id"):
            if partner.dswd_well_being_level_id.namespace_uri != WELL_BEING_NAMESPACE:
                raise ValidationError(_("Well-Being Level must be a code from the 4Ps Well-Being Level vocabulary."))
```

The field's `domain` only filters the dropdown. The constraint guards writes from code and the API.

## 7. Where this lives in production

The production 4Ps registry module ships 26 vocabularies the same way (`urn:dswd:4ps:client-status`,
`urn:dswd:4ps:set-group`, `urn:dswd:4ps:ip-group` with about 2,000 codes), and its household fields are `Many2one` to
`spp.vocabulary.code` exactly like this one. Module 5 shows them.
