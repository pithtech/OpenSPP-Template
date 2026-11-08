# Day 3 Exercise: Answer Key

Trainer copy for [exercise-day3.md](exercise-day3.md). Line numbers are those of
[dswd_wellbeing_broken/](dswd_wellbeing_broken/); compare with the real [`dswd_wellbeing`](../../dswd_wellbeing/).

## Tier 1: the three faults

| Fault                | File and line                                                                            | One-line fix                                                                         |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1. Data file missing | `__manifest__.py`, the `data` list (lines 16 to 19)                                      | add `"data/vocabulary_well_being_level.xml",` after the access file, before the view |
| 2. Invalid `domain`  | `data/vocabulary_well_being_level.xml:15`, `<field name="domain">administrative</field>` | `administrative` to `social_assistance`                                              |
| 3. Misspelled anchor | `views/res_partner_views.xml:13`, `//group[@name='group_tag_section']`                   | `group_tag_section` to `group_tags_section`                                          |

What each one shows on its own:

1. **Data file missing**: no error at all. No "4Ps Well-Being Level" under Settings > Vocabularies, an empty Well-Being
   Level dropdown, and no `loading dswd_wellbeing/data/...` line in the install output. With the tests present, three of
   five fail (drill excerpt C).
2. **Invalid `domain`**: the install or update fails with
   `ValueError: Wrong value for spp.vocabulary.domain: 'administrative'` and
   `odoo.tools.convert.ParseError: while parsing .../data/vocabulary_well_being_level.xml:10, somewhere inside` (line 10
   is the `<record>` line; the bad value is on line 15). Allowed values are in
   `upstream/openspp/spp_vocabulary/models/vocabulary.py`.
3. **Misspelled anchor**: the install or update fails with
   `Element '<xpath expr="//group[@name=&#39;group_tag_section&#39;]">' cannot be located in parent view` and a
   `ParseError` naming `views/res_partner_views.xml:8` (the `<record>` line). The anchor is in
   `upstream/openspp/spp_registry/views/individual_views.xml`.

The faults mask each other, so accept both "what you see first" and "what this fault does alone", as long as the
participant can say why:

- **As shipped**, Odoo never reads the data file (fault 1), so the `administrative` value (fault 2) is never parsed and
  produces no symptom. The first and only error is fault 3, the XPath.
- **Fix fault 3 only**: the install succeeds and shows fault 1's silence (no vocabulary, empty dropdown).
- **Fix fault 1 first**: the data file loads before the view (manifest order), so fault 2's `ParseError` appears first
  and hides fault 3 until it is fixed.
- The file is `noupdate="1"`: fault 2 must be fixed before the file first loads. A failed load rolls back, so here it is
  enough to fix the value and run again.

A participant who writes "nothing" for fault 2 and one who writes "ParseError" are both right if they name the order.

**Bonus.** Fault 1. The hook is `oca-checks-odoo-module`, check `file-not-used`: in the real module with the manifest
line removed, it reports `File "dswd_wellbeing/data/vocabulary_well_being_level.xml" is not referenced in the manifest.`
Faults 2 and 3 are values that only Odoo checks: lint and the hooks see well-formed XML. The broken folder itself is
excluded from every hook, so running them on it reports nothing.

## Tier 2: the level on the household list

A second record in `dswd_wellbeing/views/res_partner_views.xml`:

```xml
<record id="view_groups_list_wellbeing" model="ir.ui.view">
    <field name="name">res.partner.list.dswd.wellbeing</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="spp_registry.view_groups_list_tree_base" />
    <field name="arch" type="xml">
        <field name="registration_date" position="after">
            <field name="dswd_well_being_level_id" optional="show" />
        </field>
    </field>
</record>
```

An `<xpath expr="//field[@name='registration_date']" position="after">` is equally correct. No manifest change: the file
is already listed. The test, next to the form test in `tests/test_wellbeing.py`:

```python
def test_level_shows_on_the_household_list(self):
    """The inherited household list offers the well-being level as a column."""
    view = self.env.ref("spp_registry.view_groups_list_tree_base")
    arch = self.Partner.get_view(view_id=view.id, view_type="list")["arch"]
    self.assertIn('name="dswd_well_being_level_id"', arch)
```

How to check: `./odoo-project update` is clean; Registry > Browse All (Audit) > All Groups shows the column (or offers
it in the optional-columns toggle at the right of the header); `./odoo-project test dswd_wellbeing` reports
`0 failed, 0 error(s) of 6 tests`. Common slips: inheriting `view_groups_list_tree` instead of the base view (it works,
but the sheet asks for the base); forgetting `optional="show"`; a typo in the field name, which fails the update with
`Field "..." does not exist in model "res.partner"`.

## Tier 3: `dswd_id_types`

A new module folder at the repo root, shaped like step 1 of `dswd_wellbeing`:

- `__manifest__.py`: `depends` `spp_registry` and `spp_vocabulary`; `data` lists `security/ir.model.access.csv` and
  `data/id_types.xml`; `application` and `auto_install` False. `__init__.py` empty (no models), `tests/__init__.py`
  imports the test file, `readme/DESCRIPTION.md`.
- `security/ir.model.access.csv`: header only.
- `data/id_types.xml`:

```xml
<odoo noupdate="1">
    <record id="code_id_type_philsys" model="spp.vocabulary.code">
        <field name="vocabulary_id" ref="spp_vocabulary.vocab_id_type" />
        <field name="code">philsys</field>
        <field name="display">PhilSys ID</field>
        <field name="target_type">individual</field>
        <field name="id_validation">^\d{4}-\d{4}-\d{4}-\d{4}$</field>
    </record>
</odoo>
```

- `tests/test_id_types.py`:

```python
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.spp_registry.tests.common import RegistryCommon


@tagged("post_install", "-at_install")
class TestPhilSysIdType(RegistryCommon):
    def setUp(self):
        super().setUp()
        self.philsys = self.env.ref("dswd_id_types.code_id_type_philsys")

    def test_valid_number_is_accepted(self):
        reg_id = self.env["spp.registry.id"].create(
            {"partner_id": self.individual_a.id, "id_type_id": self.philsys.id, "value": "1234-5678-9012-3456"}
        )
        self.assertEqual(reg_id.value, "1234-5678-9012-3456")

    def test_invalid_number_is_refused(self):
        with self.assertRaises(ValidationError):
            self.env["spp.registry.id"].create(
                {"partner_id": self.individual_a.id, "id_type_id": self.philsys.id, "value": "12345678"}
            )
```

How to check: `./odoo-project test dswd_id_types` reports `0 failed, 0 error(s) of 2 tests`; after
`./odoo-project install dswd_id_types`, the Identity tab of an individual offers "PhilSys ID", and `12345678` is refused
with "The provided PhilSys ID ID '12345678' is invalid." Points to look for: the record adds a code to an upstream
system vocabulary, which works from module data (Odoo loads it with `install_xmlid`) but not from the Vocabularies
screen; the data file is listed in the manifest (otherwise `env.ref` fails in `setUp`); the pattern sits in
`id_validation`, not in Python; no access rows, because there is no new model.
