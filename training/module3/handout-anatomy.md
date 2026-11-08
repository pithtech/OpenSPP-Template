# Module 3 Handout: A New Module from Scratch

Fill in the blanks during the session. The back of this page is the bridge to Module 4.

## 1. Odoo and MVC in one breath

Odoo: a Python and PostgreSQL platform, Community edition under LGPL, one release a year, Odoo 19 here; OpenSPP is a
hundred modules on top of it, your `dswd_*` modules sit on top of those. MVC in Odoo: the **model** is `models.Model`
and the ORM, the **view** is XML (`ir.ui.view`, QWeb), the **controller** is actions, menus and the methods on the
model.

## 2. Five words

| Word   | Means                                                | Where you see it              |
| ------ | ---------------------------------------------------- | ----------------------------- |
| Module | a folder with `__manifest__.py` on the addons path   | Apps                          |
| Model  | a table; `_name = "dswd.asset"` becomes `dswd_asset` | Settings > Technical > Models |
| Field  | a column with a type                                 | Settings > Technical > Fields |
| View   | how the table is drawn: list, form, search           | Settings > Technical > Views  |
| Menu   | menu, then action, then view, then model             | the top bar and the app tiles |

## 3. The file map (fill in the role of each file)

```
dswd_asset/
├── __manifest__.py                 ______________________________________
├── __init__.py                     ______________________________________
├── models/__init__.py              ______________________________________
├── models/dswd_asset.py            ______________________________________
├── views/dswd_asset_views.xml      ______________________________________
├── views/menus.xml                 ______________________________________
├── report/dswd_asset_report.xml    ______________________________________
├── security/groups.xml             ______________________________________
├── security/ir.model.access.csv    ______________________________________
├── tests/__init__.py                ______________________________________
├── tests/test_dswd_asset.py        ______________________________________
├── tests/test_access.py            ______________________________________
├── tests/test_report.py            ______________________________________
├── static/description/icon.png     ______________________________________
├── pyproject.toml                  ______________________________________
└── readme/DESCRIPTION.md           ______________________________________
```

## 4. The loop

| You changed                                              | Run                                                           |
| -------------------------------------------------------- | ------------------------------------------------------------- |
| Nothing yet: a new module                                | `./odoo-project install dswd_asset`                           |
| Manifest, data, security, a new field, a new view record | `./odoo-project update`                                       |
| A Python method body                                     | `./odoo-project restart` (nothing with `start --profile dev`) |
| An existing view's XML                                   | `./odoo-project update` (nothing with `start --profile dev`)  |
| A test                                                   | `./odoo-project test dswd_asset`, then read the summary line  |

## 5. The field types you saw

| Field               | Type                    | Why that type                                                                                |
| ------------------- | ----------------------- | -------------------------------------------------------------------------------------------- |
| `name`              | Char, required          | every record needs a tag; the first validation                                               |
| `model_name`        | Char                    | short text                                                                                   |
| `asset_type`        | Selection               | a fixed list in code (Module 4 changes this)                                                 |
| `custodian_id`      | Many2one to `res.users` | a link to another table                                                                      |
| `purchase_date`     | Date                    | a real date, with a picker                                                                   |
| `warranty_end_date` | Date                    | the pair the constraint checks                                                               |
| `is_in_use`         | Boolean                 | a filter in the search view                                                                  |
| `is_under_warranty` | Boolean, computed       | derived from another field, never typed in; not stored, so it cannot be searched or filtered |

## 6. The four mistakes of a new module

| Mistake                                       | Symptom                                                                                                                        | Where to look                                      |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| No access row                                 | `have no access rules` in the `install` or `update` output; the menu is hidden; `AccessError` on the action URL, even as admin | `security/ir.model.access.csv`                     |
| Action without a menu, or menu without action | clean update, nothing to click                                                                                                 | Settings > Technical > User Interface > Menu Items |
| A view field that is not on the model         | update fails: `Field "x" does not exist in model "dswd.asset"`                                                                 | compare with Settings > Technical > Fields         |
| `_name` versus `model_id` in the access file  | `No matching record found for external id 'model_dswd_...'`                                                                    | `model_` plus `_name` with dots as underscores     |

## 7. The code, step by step

### Step 0: the manifest

```python
{
    "name": "DSWD Training: IT Asset Register",
    "category": "DSWD 4Ps/Training",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base", "spp_security"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
```

At step 0 `data` lists only the access file, which holds just its header row. Each later step adds its files: views and
menus (step 2), groups (step 3), the report (step 6). A file not listed here does not exist to Odoo: no error, it is
simply ignored. A file listed here that does not exist stops the install.

### Step 1: the model (`models/dswd_asset.py`)

```python
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DswdAsset(models.Model):
    _name = "dswd.asset"
    _description = "IT Asset"
    _order = "name"

    name = fields.Char(string="Asset Tag", required=True)
    model_name = fields.Char(string="Make and Model")
    asset_type = fields.Selection(
        [("laptop", "Laptop"), ("desktop", "Desktop"), ("printer", "Printer"), ("other", "Other")],
        required=True, default="laptop",
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
        for asset in self:
            if asset.purchase_date and asset.warranty_end_date and asset.warranty_end_date < asset.purchase_date:
                raise ValidationError(_("The warranty end date must be on or after the purchase date."))
```

Plus `from . import dswd_asset` in `models/__init__.py` and `from . import models` in `__init__.py`.

### Step 2: the views and the menu

```xml
<record id="view_dswd_asset_list" model="ir.ui.view">
    <field name="name">dswd.asset.list</field>
    <field name="model">dswd.asset</field>
    <field name="arch" type="xml">
        <list>
            <field name="name" />
            <field name="model_name" />
            <field name="asset_type" />
            <field name="custodian_id" widget="many2one_avatar_user" />
            <field name="purchase_date" optional="show" />
            <field name="is_under_warranty" />
        </list>
    </field>
</record>

<record id="action_dswd_asset" model="ir.actions.act_window">
    <field name="name">IT Assets</field>
    <field name="res_model">dswd.asset</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'search_default_filter_in_use': 1}</field>
</record>

<menuitem id="menu_dswd_asset_root" name="IT Assets" web_icon="dswd_asset,static/description/icon.png" sequence="95" />
<menuitem id="menu_dswd_asset" name="Assets" parent="menu_dswd_asset_root" action="action_dswd_asset" sequence="10" />
```

The form view has the same shape: `<form><sheet>` with named `<group>` elements; the search view lists fields and
filters. In Odoo 19 the list view tag is `<list>`, not `<tree>`.

### Step 3: the groups and the access rows

```xml
<record id="group_asset_officer" model="res.groups">
    <field name="name">IT Assets: Officer</field>
    <field name="privilege_id" ref="privilege_asset_officer" />
    <field name="implied_ids" eval="[Command.link(ref('group_asset_viewer'))]" />
</record>

<record id="spp_security.group_spp_admin" model="res.groups">
    <field name="implied_ids" eval="[Command.link(ref('group_asset_manager'))]" />
</record>
```

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_dswd_asset_system,dswd.asset system,model_dswd_asset,base.group_system,1,1,1,1
access_dswd_asset_viewer,dswd.asset viewer,model_dswd_asset,group_asset_viewer,1,0,0,0
access_dswd_asset_officer,dswd.asset officer,model_dswd_asset,group_asset_officer,1,1,1,0
access_dswd_asset_manager,dswd.asset manager,model_dswd_asset,group_asset_manager,1,1,1,1
```

Viewer reads; officer reads, writes, creates; manager also deletes. The last record links the manager tier into the
OpenSPP admin group: every OpenSPP admin is an asset manager.

### Step 4: a test

```python
from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAsset(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Asset = self.env["dswd.asset"]
        self.asset = self.Asset.create({"name": "LT-0001", "model_name": "Dell Latitude 5440"})

    def test_warranty_before_purchase_is_refused(self):
        with self.assertRaises(ValidationError):
            self.asset.write({"purchase_date": date(2026, 1, 10), "warranty_end_date": date(2025, 12, 31)})
```

`./odoo-project test dswd_asset` builds a fresh database, installs the module, runs the tests and prints
`0 failed, 0 error(s) of N tests`.

### Step 5: the ORM in a method, and in the shell

```python
    def action_assign_to_me(self):
        self.write({"custodian_id": self.env.user.id})        # self = the record the button was pressed on

    @api.model
    def find_warranty_expiring(self, days=30):
        today = fields.Date.context_today(self)
        return self.search([("is_in_use", "=", True), ("warranty_end_date", ">=", today),
                            ("warranty_end_date", "<=", fields.Date.add(today, days=days))],
                           order="warranty_end_date")
```

`<button name="action_assign_to_me" type="object" string="Assign to me" groups="dswd_asset.group_asset_officer" />` in
the form header calls the first; `groups` hides it from viewers, who cannot write. From `./odoo-project shell`:
`env["dswd.asset"].search([...])`, `.browse(ids)`, `.create({...})`, `.write({...})`, `.unlink()`, `.mapped("name")`;
`write` and `unlink` return `True`; nothing is saved until `env.cr.commit()`.

### Step 6: a PDF report

```xml
<record id="action_report_dswd_asset" model="ir.actions.report">
    <field name="name">Asset Sheet</field>
    <field name="model">dswd.asset</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">dswd_asset.report_dswd_asset</field>
    <field name="binding_model_id" ref="model_dswd_asset" />
</record>

<template id="report_dswd_asset">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="asset">
            <t t-call="web.external_layout">
                <div class="page"><h2>Asset Sheet: <span t-field="asset.name" /></h2></div>
            </t>
        </t>
    </t>
</template>
```

`binding_model_id` puts it in the Print menu; `docs` is what is being printed; `t-field` draws a field the way the form
does. Test it by rendering the HTML:
`env["ir.actions.report"]._render_qweb_html("dswd_asset.action_report_dswd_asset", ids)`.

---

## 8. Today and in Module 4: the same files, three swaps

| Today, `dswd_asset`                           | Next, `dswd_wellbeing`                                              |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `_name = "dswd.asset"`, a new table           | `_inherit = "res.partner"`, columns on an existing table            |
| `asset_type = fields.Selection([...])`        | `dswd_well_being_level_id = fields.Many2one("spp.vocabulary.code")` |
| `<list>` and `<form>` written from scratch    | `inherit_id` plus one XPath on a named anchor                       |
| an action and a menu you created              | no menu: the household form already has one                         |
| groups and four access rows                   | access file: header only, "no new model, no rows"                   |
| `depends = ["base", "spp_security"]`          | `depends = ["spp_registry", "spp_vocabulary"]`                      |
| `TransactionCase`, `create()` your own record | `RegistryCommon` hands you a household                              |
| the field is yours: `asset_type`              | a field on someone else's model: prefix `dswd_`                     |

Three swaps matter most: `_inherit`, a vocabulary instead of a Selection, an inherited view. The other rows follow from
them.

Adding "Tablet" to `asset_type` today meant editing Python, releasing, and updating every server. In OpenSPP a code list
is data, under Settings > Vocabularies. That is the first file you see in Module 4.
