# OpenSPP and Odoo Foundations Training: Participant Guide

DSWD Pantawid Pamilyang Pilipino Program (4Ps), Conditional Cash Transfer Group. This guide is the written form of the
training: read it before a session to know what is coming, follow it during the hands-on parts, and keep it as the
reference for the module development and support work that follows the training. It contains every command, every file
and every error message the sessions use. It contains no screenshots: everything in it can be reproduced on your own
laptop with your own repository.

Modules 1, 2, 5 and 6 are added as their sessions are prepared. This edition covers the two sessions of the Day 2
morning: Module 3, Introduction to Odoo, and Module 4, Developing Custom Modules and Extending Odoo Models.

---

## 0. Before you start

### 0.1 What you have

If you followed `training/SETUP.md`, you have:

- Docker Desktop, Git, Python, pre-commit and Claude Code installed and verified;
- your own repository, created from the template with "Use this template", cloned to your laptop;
- the OpenSPP image pulled, the OpenSPP source in `upstream/openspp/`, and a first start that ended at a styled login
  page.

Everything in this guide happens inside that repository folder. On Windows PowerShell, write `.\odoo-project` wherever
this guide writes `./odoo-project`.

### 0.2 The map of your repository

| Where                 | What                                                                             |
| --------------------- | -------------------------------------------------------------------------------- |
| `dswd_*/` at the root | Your modules. Every folder with `__manifest__.py` at the root is an Odoo module. |
| `dswd_asset/`         | The Module 3 module: an IT asset register built from scratch.                    |
| `dswd_wellbeing/`     | The Module 4 module: a 4Ps well-being level added to households.                 |
| `upstream/openspp/`   | The OpenSPP source for the release you run, read-only. Never edit it; read it.   |
| `training/`           | The setup guide, this guide, and the per-module materials.                       |
| `docs/`               | Guides, principles, architecture decisions.                                      |
| `odoo-project`        | The command-line tool that drives Docker for you.                                |

The repository root is mounted into the container as an addons folder. That is why your modules sit at the root, and why
no folder at the root may be called `forms`, `helpers`, `mixins`, `utilities` or `vendor` (section 7.3).

### 0.3 The eight commands

| When                                           | Run                               |
| ---------------------------------------------- | --------------------------------- |
| Start the stack                                | `./odoo-project start`            |
| Something is wrong before you even begin       | `./odoo-project doctor`           |
| Install a new module into the running database | `./odoo-project install <module>` |
| A module you already installed changed         | `./odoo-project update`           |
| You changed Python and run the default profile | `./odoo-project restart`          |
| Odoo said something you did not understand     | `./odoo-project logs`             |
| Run a module's tests on a clean database       | `./odoo-project test <module>`    |
| Pages lost their styling                       | `./odoo-project resetassets`      |
| End of the day                                 | `./odoo-project stop`             |

Login: `admin` / `admin`. Developer mode: Settings, scroll to the bottom, "Activate the developer mode". Developer mode
adds the Technical menu, which is the x-ray of everything in this guide.

### 0.4 The edit loop

Odoo reads your files when it installs or updates a module, not continuously. After a change:

| You changed                                                                     | Run                                                           |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Nothing yet: a brand-new module                                                 | `./odoo-project install <module>`                             |
| `__manifest__.py`, a data file, a security file, a new field, a new view record | `./odoo-project update`                                       |
| A Python method body                                                            | `./odoo-project restart` (nothing with `start --profile dev`) |
| An existing view's XML                                                          | `./odoo-project update` (nothing with `start --profile dev`)  |
| A record in a `noupdate="1"` data file                                          | delete the record, then `update`; or a fresh database         |
| A test                                                                          | `./odoo-project test <module>`, then read the summary line    |

`update` never installs a new module; `install` does. Both restart the server.

---

## Module 3: Introduction to Odoo

### 3.1 What you can do after this module

1. Say what Odoo is (the platform, its licence, its release, where OpenSPP sits on it) and name the three parts of MVC
   in Odoo terms.
2. Say what a module is, name the role of each file in one, and say why a file not listed in the manifest does not
   exist.
3. Write a model with Char, Selection, Date, Many2one and Boolean fields, and say "model = table, field = column".
4. Write a list view, a form view, an action and a menu, and explain the chain menu, action, view, model.
5. Write the access row a new model needs, and recognise its absence in the log and on screen.
6. Use the ORM from a method and from the shell: `search`, `browse`, `create`, `write`, `unlink`.
7. Add a PDF report to a model and find it in the Print menu.
8. Run a module's tests and read the summary line.

### 3.2 What Odoo is

Odoo is an open-source business application platform written in Python on PostgreSQL, with a web client written in
JavaScript. It began in 2005 as TinyERP, became OpenERP, and has been Odoo since 2014. One major version ships every
year in the autumn; this training runs on **Odoo 19** (2025). Two editions exist: **Community**, under the LGPL v3
licence, which is what OpenSPP builds on and what you run; and **Enterprise**, proprietary modules sold by Odoo S.A. on
top of Community. Everything in this training is Community.

What makes Odoo a platform rather than a product is the module system: every feature, including the core ones, is a
module, and a module can add tables, columns, screens, menus, reports and rules to any other module without changing its
code. OpenSPP is about a hundred such modules (`spp_*`) that turn Odoo into a social protection management information
system: registry, programs, cycles, entitlements, change requests, grievances, an API. Your `dswd_*` modules sit on top
of those, the same way OpenSPP sits on top of Odoo.

Three facts to keep:

- The database is PostgreSQL; every model is a table you could inspect with `./odoo-project sql`.
- The server is one Python process (several, in production) that loads every installed module at start.
- The web client is a single-page application; the XML views you write are turned into screens by it.

### 3.3 MVC, in Odoo terms

Odoo is a Model-View-Controller platform, with its own names for the three parts:

| MVC part   | In Odoo                                                                                                                                                   | Where you write it                                                          |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Model      | `models.Model` classes and their fields; the ORM maps them to tables and rows                                                                             | `models/*.py`                                                               |
| View       | XML records on `ir.ui.view` (list, form, search, kanban) and QWeb templates for reports; rendered by the web client                                       | `views/*.xml`, `report/*.xml`                                               |
| Controller | What happens when the user acts: window actions and menus route clicks to views; methods on the model run the business logic; HTTP controllers serve URLs | `views/*.xml` (actions, menus), `models/*.py` (methods), `controllers/*.py` |

The rule of thumb: data and rules live in the model, drawing lives in the view, and the controller is thin. A button on
a form calls a method on the model; the method uses the ORM; the view only says where the button sits.

### 3.4 Odoo in five words

| Word   | Means                                                | See it at                     |
| ------ | ---------------------------------------------------- | ----------------------------- |
| Module | a folder with `__manifest__.py` on the addons path   | Apps                          |
| Model  | a table: `_name = "dswd.asset"` becomes `dswd_asset` | Settings > Technical > Models |
| Field  | a column with a type                                 | Settings > Technical > Fields |
| View   | how the table is drawn: list, form, search           | Settings > Technical > Views  |
| Menu   | menu, then action, then view, then model             | the top bar and the app tiles |

Open Settings > Technical > Models and search `res.partner`. Its fields come from `base`, from `spp_registry`, from
`spp_vocabulary` and more. Many modules add columns to one table. Module 4 is about doing exactly that.

### 3.5 The module you build: `dswd_asset`

An IT asset register: the laptops, desktops and printers of an office and who looks after them. It is plain Odoo;
nothing in it is specific to 4Ps. The `dswd_` prefix is this project's naming rule, enforced by the repository's lint,
the way `spp_` is OpenSPP's: it says who owns the code, not what it is about.

```
dswd_asset/
├── __manifest__.py                 declares the module and lists its files
├── __init__.py                     imports the models package
├── models/__init__.py              imports the model file
├── models/dswd_asset.py            the model: table, fields, a computed field, a constraint
├── views/dswd_asset_views.xml      list, form and search views, and the action
├── views/menus.xml                 the app tile and the menu that opens the action
├── report/dswd_asset_report.xml    the Asset Sheet PDF report and its template
├── security/groups.xml             viewer, officer and manager groups
├── security/ir.model.access.csv    who may read, write, create, delete
├── tests/test_dswd_asset.py        what "working" means, as code
├── tests/test_access.py            the access rows, proven as each tier
└── readme/DESCRIPTION.md           what the module is for
```

The module ships in your repository with `auto_install: False`. It is installed only when you run
`./odoo-project install dswd_asset`.

### 3.6 Step 0: a module is a folder and a manifest

```python
{
    "name": "DSWD Training: IT Asset Register",
    "summary": "A plain Odoo module built from scratch in Module 3: an IT asset register",
    "category": "DSWD 4Ps/Training",
    "version": "19.0.1.0.0",
    "author": "DSWD",
    "license": "LGPL-3",
    "depends": ["base", "spp_security"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/dswd_asset_views.xml",
        "views/menus.xml",
        "report/dswd_asset_report.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
```

- `depends` lists the modules Odoo must install first. `base` is Odoo itself; `spp_security` is the OpenSPP module that
  owns the admin group the manager tier links into (step 3).
- `data` lists the files Odoo loads, in order. **A file not listed here does not exist to Odoo.** No error is raised;
  the file is simply ignored.
- `installable: True` makes it appear in Apps; `auto_install: False` keeps it out of the automatic first start.

With only this file and an empty `__init__.py`, the module installs. It does nothing yet. In Apps, turn on developer
mode, click Update Apps List, search "Asset", and install; or from the terminal: `./odoo-project install dswd_asset`.
`./odoo-project logs` shows `Loading module dswd_asset`.

### 3.7 Step 1: the model is the table

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
        for asset in self:
            if asset.purchase_date and asset.warranty_end_date and asset.warranty_end_date < asset.purchase_date:
                raise ValidationError(_("The warranty end date must be on or after the purchase date."))
```

What each line teaches:

| Line                           | Teaches                                                                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| `_name = "dswd.asset"`         | A new table, `dswd_asset`. `_description` is mandatory in Odoo 19.                                                                  |
| `fields.Char(required=True)`   | A text column; `required` is the first validation a user meets.                                                                     |
| `fields.Selection([...])`      | A fixed list of values **in code**. Adding one is a code change and a release (section 4.4).                                        |
| `fields.Many2one("res.users")` | A link to another table. The dropdown and the avatar come for free.                                                                 |
| `fields.Date()`                | A real date with a picker, not text.                                                                                                |
| `fields.Boolean(default=True)` | A checkbox; `default` applies to new records.                                                                                       |
| `compute=` with `@api.depends` | A value derived from other fields, recalculated when they change, never typed in. Not stored, so it cannot be searched or filtered. |
| `@api.constrains`              | A rule that refuses bad data with a sentence the user reads.                                                                        |

The model needs two import lines to be seen: `from . import dswd_asset` in `models/__init__.py` and
`from . import models` in `__init__.py`. Forgetting either raises no error; the model is simply absent. After
`./odoo-project update`, Settings > Technical > Fields, searched by model `dswd.asset`, lists the columns.

The log also says, at this point:

```
WARNING odoo.modules.loading: The models ['dswd.asset'] have no access rules in module dswd_asset, consider adding some
```

Nothing is broken. Nobody can open the table either.

### 3.8 Step 2: views draw the table, a menu opens it

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

<record id="view_dswd_asset_form" model="ir.ui.view">
    <field name="name">dswd.asset.form</field>
    <field name="model">dswd.asset</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <div class="oe_title">
                    <h1><field name="name" placeholder="Asset tag, e.g. LT-0001" /></h1>
                </div>
                <group name="group_main">
                    <group name="group_identity" string="Identity">
                        <field name="model_name" />
                        <field name="asset_type" />
                        <field name="custodian_id" widget="many2one_avatar_user" />
                    </group>
                    <group name="group_lifecycle" string="Lifecycle">
                        <field name="purchase_date" />
                        <field name="warranty_end_date" />
                        <field name="is_under_warranty" />
                        <field name="is_in_use" />
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>

<record id="view_dswd_asset_search" model="ir.ui.view">
    <field name="name">dswd.asset.search</field>
    <field name="model">dswd.asset</field>
    <field name="arch" type="xml">
        <search>
            <field name="name" />
            <field name="model_name" />
            <field name="custodian_id" />
            <filter name="filter_in_use" string="In use" domain="[('is_in_use', '=', True)]" />
            <group>
                <filter name="group_by_type" string="Type" context="{'group_by': 'asset_type'}" />
                <filter name="group_by_custodian" string="Custodian" context="{'group_by': 'custodian_id'}" />
            </group>
        </search>
    </field>
</record>

<record id="action_dswd_asset" model="ir.actions.act_window">
    <field name="name">IT Assets</field>
    <field name="res_model">dswd.asset</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'search_default_filter_in_use': 1}</field>
</record>
```

```xml
<menuitem id="menu_dswd_asset_root" name="IT Assets" web_icon="dswd_asset,static/description/icon.png" sequence="95" />
<menuitem id="menu_dswd_asset" name="Assets" parent="menu_dswd_asset_root" action="action_dswd_asset" sequence="10" />
```

- A view is a record of the model `ir.ui.view` whose `arch` is the XML that draws it. Three kinds here: `list` (rows),
  `form` (one record), `search` (the search box, filters and group-bys).
- In Odoo 19 the list view's tag is `<list>`; older code wrote `<tree>`.
- Named `<group>` elements in the form (`group_identity`, `group_lifecycle`) are the anchors another module could
  extend. Module 4 relies on upstream views having such names.
- An action says which model and which views; a menu points at the action. A top-level menu with a `web_icon` is an app
  tile.
- XML ids follow the repository's rules: `view_<model>_<type>`, `action_<model>`, `menu_<model>_<purpose>`.

After `./odoo-project update` the app tile "IT Assets" appears. Clicking it, even as `admin`, gives:

```
Access Error
You are not allowed to access 'IT Asset' (dswd.asset) records.
No group currently allows this operation.
```

The warning from step 1 became an error the moment there was a door to knock on.

### 3.9 Step 3: groups and access rows

```xml
<record id="category_dswd_asset" model="ir.module.category">
    <field name="name">DSWD Training: IT Assets</field>
    <field name="sequence">60</field>
</record>

<record id="privilege_asset_officer" model="res.groups.privilege">
    <field name="name">IT Assets</field>
    <field name="category_id" ref="category_dswd_asset" />
</record>

<record id="group_asset_viewer" model="res.groups">
    <field name="name">IT Assets: Viewer</field>
    <field name="privilege_id" ref="privilege_asset_officer" />
    <field name="implied_ids" eval="[Command.link(ref('base.group_user'))]" />
</record>

<record id="group_asset_officer" model="res.groups">
    <field name="name">IT Assets: Officer</field>
    <field name="privilege_id" ref="privilege_asset_officer" />
    <field name="implied_ids" eval="[Command.link(ref('group_asset_viewer'))]" />
</record>

<record id="group_asset_manager" model="res.groups">
    <field name="name">IT Assets: Manager</field>
    <field name="privilege_id" ref="privilege_asset_officer" />
    <field name="implied_ids" eval="[Command.link(ref('group_asset_officer'))]" />
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

- Three tiers is this project's convention: a viewer reads; an officer reads, writes and creates; a manager also
  deletes. `implied_ids` makes each tier include the one below, and the viewer include every internal user.
- A privilege and a category are what Odoo 19 shows on the user form, under Settings > Users, so an administrator can
  assign a tier with a dropdown.
- The last record adds a line to a group that another module owns, `spp_security.group_spp_admin`: whoever is an OpenSPP
  admin is an asset manager. That is why `admin` can open the app without extra setup.
- The access file: one row per group and model. The `base.group_system` row comes first, always. `model_dswd_asset` is
  `model_` plus `_name` with dots turned into underscores; a typo there fails at install with
  `No matching record found for external id`.
- `groups.xml` is listed in the manifest **before** the access file, because the access rows refer to the groups.

After `./odoo-project update`, the list opens. Register the laptop in front of you. Then set a warranty end date earlier
than the purchase date and read the dialog: that sentence is in the Python file.

### 3.10 Step 4: tests say what "working" means

```python
from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAsset(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Asset = self.env["dswd.asset"]
        self.asset = self.Asset.create({"name": "LT-0001", "model_name": "Dell Latitude 5440"})

    def test_defaults(self):
        self.assertEqual(self.asset.asset_type, "laptop")
        self.assertTrue(self.asset.is_in_use)
        self.assertEqual(self.asset.custodian_id, self.env.user)

    def test_warranty_flag_follows_the_end_date(self):
        self.asset.warranty_end_date = date.today() + timedelta(days=30)
        self.assertTrue(self.asset.is_under_warranty)
        self.asset.warranty_end_date = date.today() - timedelta(days=1)
        self.assertFalse(self.asset.is_under_warranty)

    def test_warranty_before_purchase_is_refused(self):
        with self.assertRaises(ValidationError):
            self.asset.write({"purchase_date": date(2026, 1, 10), "warranty_end_date": date(2025, 12, 31)})
```

```python
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDswdAssetAccess(TransactionCase):
    def setUp(self):
        super().setUp()
        self.viewer = self._make_user("asset_viewer", "dswd_asset.group_asset_viewer")
        self.officer = self._make_user("asset_officer", "dswd_asset.group_asset_officer")
        self.manager = self._make_user("asset_manager", "dswd_asset.group_asset_manager")
        self.asset = self.env["dswd.asset"].create({"name": "PR-0001", "asset_type": "printer"})

    def _make_user(self, login, group_xmlid):
        return self.env["res.users"].create(
            {"name": login, "login": login, "email": f"{login}@example.test",
             "group_ids": [(6, 0, [self.env.ref(group_xmlid).id])]}
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
        with self.assertRaises(AccessError):
            created.unlink()

    def test_manager_deletes(self):
        assets = self.env["dswd.asset"].with_user(self.manager)
        assets.create({"name": "LT-0003"}).unlink()
        self.assertEqual(assets.search_count([("name", "=", "LT-0003")]), 0)
```

- `TransactionCase` gives each test a database transaction that is rolled back afterwards; `setUp` runs before each
  test. `@tagged("post_install", "-at_install")` runs the tests after every module is installed, which is what this
  repository requires.
- `self.env["dswd.asset"]` is the model; `create`, `write`, `search_count`, `unlink` are the four operations of the ORM.
  `with_user(...)` runs the same operations as that user, which is how the access rows are proven rather than assumed.

```
$ ./odoo-project test dswd_asset
0 failed, 0 error(s) of 12 tests
Full log: .../dswd_asset_unittest_20261108_153000.log
```

The summary line is the first thing you read when someone says a module is broken; the log path is the second.

### 3.11 Step 5: the ORM, from a method and from the shell

The ORM (object-relational mapper) is how Python talks to the tables: a model is a class, a row is a record, a query is
a method call. Five operations cover almost everything:

| Operation        | Meaning                                                             | Returns        |
| ---------------- | ------------------------------------------------------------------- | -------------- |
| `search(domain)` | the records matching a domain, a list of `(field, operator, value)` | a recordset    |
| `browse(ids)`    | the records with these ids, without a query until a field is read   | a recordset    |
| `create(values)` | a new row                                                           | the new record |
| `write(values)`  | change fields on every record in the set                            | `True`         |
| `unlink()`       | delete every record in the set                                      | `True`         |

Two methods added to `dswd.asset` show the two shapes a method takes:

```python
    def action_assign_to_me(self):
        """Form button: the ORM write in one line. ``self`` is the asset the button was pressed on."""
        self.write({"custodian_id": self.env.user.id})

    @api.model
    def find_warranty_expiring(self, days=30):
        """Assets still in use whose warranty ends within ``days``: a search with a domain."""
        today = fields.Date.context_today(self)
        return self.search(
            [
                ("is_in_use", "=", True),
                ("warranty_end_date", ">=", today),
                ("warranty_end_date", "<=", fields.Date.add(today, days=days)),
            ],
            order="warranty_end_date",
        )
```

- A method without a decorator runs on records: `self` is the asset (or assets) it was called on. The form's
  `<button name="action_assign_to_me" type="object" />` calls it on the record being edited.
- `@api.model` marks a method that works on the model as a whole: `env["dswd.asset"].find_warranty_expiring(30)`.
- `self.env` is the environment: the current user (`self.env.user`), the other models (`self.env["res.users"]`), xml ids
  (`self.env.ref("dswd_asset.group_asset_manager")`).

The same operations from the shell, the fastest way to answer "what is in the database right now":

```
$ ./odoo-project shell
>>> Asset = env["dswd.asset"]
>>> Asset.search_count([])
2
>>> laptops = Asset.search([("asset_type", "=", "laptop")])
>>> laptops.mapped("name")
['LT-0001']
>>> a = Asset.create({"name": "LT-0099", "asset_type": "laptop"})
>>> a.write({"model_name": "Lenovo ThinkPad T14"})
>>> a.custodian_id.name
'OdooBot'
>>> Asset.find_warranty_expiring(365).mapped("name")
['LT-0001']
>>> a.unlink()
>>> env.cr.commit()      # the shell does not save until you say so
```

`mapped`, `filtered` and `sorted` work on any recordset; a Many2one field is itself a record, so `a.custodian_id.name`
walks the link. Nothing the shell does is saved until `env.cr.commit()`.

### 3.12 Step 6: a PDF report

A report is two records in one XML file: an `ir.actions.report` that names the model, the template and the format, and a
QWeb template that is ordinary HTML with `t-` attributes. Odoo renders the template to HTML, then to PDF with
wkhtmltopdf, which the image includes.

```xml
<record id="action_report_dswd_asset" model="ir.actions.report">
    <field name="name">Asset Sheet</field>
    <field name="model">dswd.asset</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">dswd_asset.report_dswd_asset</field>
    <field name="report_file">dswd_asset.report_dswd_asset</field>
    <field name="print_report_name">'Asset Sheet - %s' % (object.name)</field>
    <field name="binding_model_id" ref="model_dswd_asset" />
    <field name="binding_type">report</field>
</record>

<template id="report_dswd_asset">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="asset">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2>Asset Sheet: <span t-field="asset.name" /></h2>
                    <table class="table table-sm o_main_table">
                        <tbody>
                            <tr><th>Make and Model</th><td><span t-field="asset.model_name" /></td></tr>
                            <tr><th>Type</th><td><span t-field="asset.asset_type" /></td></tr>
                            <tr><th>Custodian</th><td><span t-field="asset.custodian_id" /></td></tr>
                            <tr><th>Purchase Date</th><td><span t-field="asset.purchase_date" /></td></tr>
                            <tr><th>Warranty End</th><td><span t-field="asset.warranty_end_date" /></td></tr>
                        </tbody>
                    </table>
                </div>
            </t>
        </t>
    </t>
</template>
```

- `binding_model_id` puts "Asset Sheet" in the Print menu of the asset list and form; `print_report_name` names the
  downloaded file.
- `docs` is the recordset being printed; `t-foreach` makes one page per record; `t-field` renders a field with its
  widget (dates, Many2one names, selections) the way the form does; `t-esc` prints any expression.
- `web.external_layout` adds the company header and footer; `web.html_container` is the page wrapper.
- A report is tested without a PDF engine by rendering the HTML:
  `self.env["ir.actions.report"]._render_qweb_html("dswd_asset.action_report_dswd_asset", asset.ids)`.

### 3.13 The four mistakes of a new module

| Mistake                                       | Symptom                                                        | Where to look                                      |
| --------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------- |
| No access row                                 | `have no access rules` in the log; `AccessError` even as admin | `security/ir.model.access.csv`                     |
| Action without a menu, or menu without action | clean update, nothing to click                                 | Settings > Technical > User Interface > Menu Items |
| A view field that is not on the model         | update fails: `Field "x" does not exist in model "dswd.asset"` | compare with Settings > Technical > Fields         |
| `_name` versus `model_id` in the access file  | `No matching record found for external id 'model_dswd_...'`    | `model_` plus `_name` with dots as underscores     |

### 3.14 From Module 3 to Module 4

4Ps needs a well-being level on every household. Which file do we start with?

The household already exists: it is a `res.partner` record, and that table already has hundreds of columns from several
modules. A new `dswd.household` model would mean two tables, two forms, two access files, and no link to programs.
Module 4 adds **one column** to the existing table instead.

And `asset_type`: adding "Tablet" to it means editing Python, releasing, and running `update` on every server. In
OpenSPP a code list is **data**, edited under Settings > Vocabularies, with a namespace other systems can match. That is
the first file of Module 4.

| Module 3, `dswd_asset`                        | Module 4, `dswd_wellbeing`                                          |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `_name = "dswd.asset"`, a new table           | `_inherit = "res.partner"`, columns on an existing table            |
| `asset_type = fields.Selection([...])`        | `dswd_well_being_level_id = fields.Many2one("spp.vocabulary.code")` |
| `<list>` and `<form>` written from scratch    | `inherit_id` plus one XPath on a named anchor                       |
| an action and a menu you created              | no menu: the household form already has one                         |
| groups and four access rows                   | access file: header only, "no new model, no rows"                   |
| `depends = ["base", "spp_security"]`          | `depends = ["spp_registry", "spp_vocabulary"]`                      |
| `TransactionCase`, `create()` your own record | `RegistryCommon` hands you a household                              |
| the field is yours: `asset_type`              | a field on someone else's model: prefix `dswd_`                     |

Same files, same loop, same `test`. Three swaps, each one line.

---

## Module 4: Developing Custom Modules and Extending Odoo Models

### 4.1 What you can do after this module

1. Name the role of each file in a `dswd_*` module and state that a file not listed in the manifest does not exist.
2. Given a 4Ps requirement, pick the right pattern: `_inherit` on the upstream model, a `dswd_` field, a Many2one to a
   vocabulary code; never a new model for an attribute, never a static Selection for a code list, never an edit under
   `upstream/openspp/`.
3. Explain view inheritance (`inherit_id` plus one XPath on a named anchor) and recognise the error when the anchor does
   not exist.
4. Given a log excerpt, say which step failed and which file to open.
5. Run the tests of a module and read the pass/fail summary.

### 4.2 The three rules

1. **Never edit `upstream/openspp/`.** Read it; extend it from your module. The next release overwrites it.
2. **Inherit, do not redefine.** `_inherit = "res.partner"` adds to the household; `_name` would create a new table. New
   fields on upstream models are prefixed `dswd_`.
3. **A file not listed in `__manifest__.py` does not exist.** Data and view files load only if they are in `data`.

### 4.3 The requirement

The Social Welfare and Development Indicators assessment (SWDI) places every 4Ps household at one of three levels:
Survival, Subsistence, Self-Sufficient. Since Executive Order 120 (July 2026) the level decides whether a household
stays in the program past seven years. We add the level to the household record in OpenSPP, as a dropdown on the
household Profile page.

```
dswd_wellbeing/
├── __manifest__.py                        depends on spp_registry and spp_vocabulary
├── __init__.py                            imports models
├── data/vocabulary_well_being_level.xml   the vocabulary and its three codes
├── models/__init__.py                     imports res_partner
├── models/res_partner.py                  the field on the household, and a constraint
├── views/res_partner_views.xml            where the field shows on the household form
├── security/ir.model.access.csv           header only: no new model, no rows
├── tests/test_wellbeing.py                what "working" means
└── readme/DESCRIPTION.md                  what the module is for
```

### 4.4 Vocabularies: a code list as data

OpenSPP's `spp_vocabulary` module stores code lists in two models: `spp.vocabulary`, a named list with a globally unique
namespace URI, and `spp.vocabulary.code`, one code in a list with a `code`, a `display` label, a `definition` and a
computed URI `namespace#code`. OpenSPP ships gender (ISO 5218), country, currency, language, occupation (ISCO-08),
education level, ID type and more. The production 4Ps modules ship 26 of their own: client status (32 statuses in 9
categories), member status, set groups, indigenous peoples groups (about 2,000 codes), well-being level, and so on, all
under `urn:dswd:4ps:...`.

Why a vocabulary and not a `Selection`:

- a code list changes without a release: Settings > Vocabularies, no code change;
- deployments differ: a region can hide codes with a deployment profile;
- every code has a URI other systems can match;
- 32 client statuses and 2,000 groups do not belong in Python.

Static selections are for internal workflow states only.

```xml
<odoo noupdate="1">
    <record id="vocab_well_being_level" model="spp.vocabulary">
        <field name="name">4Ps Well-Being Level</field>
        <field name="namespace_uri">urn:dswd:4ps:well-being-level</field>
        <field name="description">Household well-being level from the SWDI assessment</field>
        <field name="is_system" eval="True" />
        <field name="domain">social_assistance</field>
    </record>

    <record id="code_well_being_survival" model="spp.vocabulary.code">
        <field name="vocabulary_id" ref="vocab_well_being_level" />
        <field name="code">survival</field>
        <field name="display">Survival</field>
        <field name="definition">SWDI level 1: the household cannot meet basic needs without assistance.</field>
        <field name="target_type">group</field>
        <field name="sequence">10</field>
    </record>
    <!-- subsistence (sequence 20) and self_sufficient (sequence 30) follow the same shape -->
</odoo>
```

- `noupdate="1"`: these records are loaded once, on install, and never overwritten by an update. To change one after
  install, delete it (Settings > Technical > External Identifiers, or the Vocabularies screen) and update again, or
  start from a fresh database. A bad value in such a file is caught only the first time it loads.
- `domain` is a fixed selection: `core`, `social_assistance`, `social_insurance`, `labor`, `disability`, `agriculture`,
  `health` or `education`. Any other value fails at install with a `ParseError`.
- `is_system`: shipped codes are locked against editing in the UI; administrators add local codes next to them.
- Namespaces for your own vocabularies follow the production pattern, `urn:dswd:4ps:<name>`.

After `./odoo-project update`, Settings > Vocabularies > Manage Vocabularies lists "4Ps Well-Being Level" with three
System codes.

### 4.5 The field on the household

```python
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

WELL_BEING_NAMESPACE = "urn:dswd:4ps:well-being-level"


class ResPartner(models.Model):
    _inherit = "res.partner"

    dswd_well_being_level_id = fields.Many2one(
        comodel_name="spp.vocabulary.code",
        string="Well-Being Level",
        domain=[("namespace_uri", "=", WELL_BEING_NAMESPACE)],
        ondelete="restrict",
        help="SWDI level from the latest assessment: Survival, Subsistence or Self-Sufficient.",
    )

    @api.constrains("dswd_well_being_level_id")
    def _check_well_being_level_namespace(self):
        for partner in self.filtered("dswd_well_being_level_id"):
            if partner.dswd_well_being_level_id.namespace_uri != WELL_BEING_NAMESPACE:
                raise ValidationError(_("Well-Being Level must be a code from the 4Ps Well-Being Level vocabulary."))
```

- `_inherit = "res.partner"` with no `_name`: this class adds to the existing model. Households are `res.partner`
  records with `is_registrant` and `is_group` set.
- The field name starts with `dswd_`, so it never collides with a field OpenSPP adds later.
- The `domain` keeps the dropdown to the three codes. **A domain only filters the dropdown**: a write from code, an
  import or the API can store any code. The constraint is the real guard.
- `ondelete="restrict"`: a code in use cannot be deleted.

After `./odoo-project update` nothing changes on screen; the field exists in Settings > Technical > Fields (search
`dswd_`). A field without a view is invisible, not broken.

### 4.6 The view: one XPath on a named anchor

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

- `inherit_id` names the upstream view. In `spp_registry` one form serves individuals and households; the household
  pages and groups are prefixed `group_` (`group_profile`, `group_tags_section`, `group_identity`).
- Find the anchor before writing the XPath:
  `grep -n 'name="group_' upstream/openspp/spp_registry/views/individual_views.xml`. Target named elements only;
  positional XPath breaks on the next release.
- `no_create` and `no_open` keep users from creating or editing codes from the dropdown; codes are managed under
  Settings > Vocabularies.

After `./odoo-project update`: Registry > Groups > a household > Profile shows a "4Ps" section with the dropdown.

### 4.7 The security file

The module adds no model, so `security/ir.model.access.csv` holds only its header line. The repository's hooks require
the file to exist in every module; an empty one says "no new model, no rows". Access to the field follows the upstream
rules for `res.partner`.

### 4.8 The tests

```python
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.spp_registry.tests.common import RegistryCommon

NAMESPACE = "urn:dswd:4ps:well-being-level"


@tagged("post_install", "-at_install")
class TestWellBeingVocabulary(RegistryCommon):
    def test_three_levels_in_swdi_order(self):
        codes = [self.VocabCode.get_code(NAMESPACE, code) for code in ("survival", "subsistence", "self_sufficient")]
        self.assertTrue(all(codes))
        self.assertEqual([c.display for c in codes], ["Survival", "Subsistence", "Self-Sufficient"])


@tagged("post_install", "-at_install")
class TestHouseholdWellBeing(RegistryCommon):
    def test_household_stores_a_level(self):
        subsistence = self.VocabCode.get_code(NAMESPACE, "subsistence")
        self.group.dswd_well_being_level_id = subsistence
        self.assertEqual(self.group.dswd_well_being_level_id.display, "Subsistence")

    def test_level_shows_on_the_household_form(self):
        form = self.env.ref("spp_registry.view_individuals_form")
        arch = self.Partner.get_view(view_id=form.id, view_type="form")["arch"]
        self.assertIn('name="dswd_4ps_section"', arch)

    def test_rejects_a_code_from_another_vocabulary(self):
        female = self.VocabCode.get_code("urn:iso:std:iso:5218", "2")
        with self.assertRaises(ValidationError):
            self.group.dswd_well_being_level_id = female
```

- `RegistryCommon`, from `upstream/openspp/spp_registry/tests/common.py`, creates a household (`self.group`), two
  individuals and gives you the vocabulary model (`self.VocabCode`). Use upstream helpers before writing your own.
- `get_code(namespace, code)` and `resolve_by_uri(uri)` are the two cached lookups for codes in Python.

```
$ ./odoo-project test dswd_wellbeing
0 failed, 0 error(s) of 5 tests
```

### 4.9 The five mistakes of an extension

| Mistake                                                           | Symptom                                                                                   | One-line diagnostic                                                                      |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Module not in Apps (folder typo, no manifest, list not refreshed) | search finds nothing                                                                      | developer mode on, Update Apps List; `./odoo-project logs` has no `dswd_` line           |
| Data file written but not in manifest `data`                      | update clean, UI unchanged                                                                | `grep vocabulary_ dswd_wellbeing/__manifest__.py`                                        |
| `restart` instead of `update`, or edited `noupdate` data          | change never shows                                                                        | new field, view or data: `update`; changed `noupdate` record: delete it, or `stop -v -y` |
| Wrong XPath anchor (`group_tag_section`, `@class=`)               | `Element '<xpath ...>' cannot be located in parent view`                                  | `grep -n 'name="group_' upstream/openspp/spp_registry/views/individual_views.xml`        |
| Import missing in `models/__init__.py`                            | no error, field absent; or `Field "..." does not exist in model` once a view refers to it | Settings > Technical > Fields, search `dswd_`                                            |

Three real log excerpts, as the Day 3 drill uses them:

```
ValueError: Wrong value for spp.vocabulary.domain: 'administrative'
odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/data/vocabulary_well_being_level.xml:10
```

```
odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/views/res_partner_views.xml:8
Element '<xpath expr="//group[@name='group_tag_section']">' cannot be located in parent view
```

```
INFO odoo.modules.loading: loading dswd_wellbeing/security/ir.model.access.csv
INFO odoo.modules.loading: loading dswd_wellbeing/views/res_partner_views.xml
ERROR ...: FAIL: TestWellBeingVocabulary.test_three_levels_in_swdi_order
AssertionError: False is not true : every level must resolve by namespace and code
```

Read a traceback from the bottom up: the first line that names a file in **your** module is where you go. Lint passes on
all three; lint checks shape, not meaning.

### 4.10 Where this lives in production

The production 4Ps registry module ships 26 vocabularies the same way and extends `res.partner` with Many2one fields to
`spp.vocabulary.code` exactly like this one: client status, member status, set group, poverty status, indigenous peoples
group, well-being level. Its household form is extended by inheriting the same `spp_registry` view. What you built in
Module 4 is the shape of every `dswd_4ps_*` module. Module 5 shows them.

`training/4ps-program-reference.md`, section 8, maps every 4Ps concept (household, grantee, client status, sets,
periods, compliance, payroll, grievances) to the OpenSPP model and the production module that implements it.

### 4.11 Exercises (Module 6, Day 3)

The exercise sheet is `training/module4/exercise-day3.md`. Before you start, the pre-flight: `doctor` clean, `start`,
styled page, `test dswd_wellbeing` at 5 passed. Then:

- **Tier 1, no environment needed**: `training/module4/dswd_wellbeing_broken/` holds the module with three planted
  faults. Find each one, write the file and line, the symptom you expect, and the one-line fix.
- **Tier 2**: add the well-being level as an optional column on the household list view
  (`spp_registry.view_groups_list_tree_base`), with a test.
- **Tier 3**: a second module, `dswd_id_types`, adding the PhilSys number to the upstream ID Type vocabulary with the
  validation pattern `^\d{4}-\d{4}-\d{4}-\d{4}$`, and a test that an invalid number raises `ValidationError`.

---

## 5. Module 5: DSWD-specific implementation of OpenSPP

To be added.

## 6. Module 6: Hands-on activity

To be added. The Day 3 exercise sheet for Module 4 is already in `training/module4/exercise-day3.md`.

---

## 7. Reference

### 7.1 Naming rules of this repository

| Thing                      | Rule                                             | Example                         |
| -------------------------- | ------------------------------------------------ | ------------------------------- | --------- | --------------------- |
| Module folder              | `dswd_<domain>` or `dswd_<domain>_<feature>`     | `dswd_asset`, `dswd_wellbeing`  |
| New model                  | `dswd.<domain>` or `dswd.<domain>.<entity>`      | `dswd.asset`                    |
| Field on an upstream model | prefix `dswd_`                                   | `dswd_well_being_level_id`      |
| Many2one field             | ends in `_id`; One2many and Many2many in `_ids`  | `custodian_id`                  |
| Boolean field              | starts with `is_`, `has_` or `can_`              | `is_in_use`                     |
| View XML id                | `view_<model>_<type>` (`list`, `form`, `search`) | `view_dswd_asset_form`          |
| Action XML id              | `action_<model>`                                 | `action_dswd_asset`             |
| Menu XML id                | `menu_<model>` or `menu_<model>_<purpose>`       | `menu_dswd_asset_root`          |
| Group XML id               | `group*<domain>*<viewer                          | officer                         | manager>` | `group_asset_officer` |
| Access row id              | `access_<model>_<group>`                         | `access_dswd_asset_officer`     |
| Vocabulary namespace       | `urn:dswd:4ps:<name>`                            | `urn:dswd:4ps:well-being-level` |

The pre-commit hooks enforce most of these; `./odoo-project lint` runs the formatters on changed files, and `git commit`
runs the full set.

### 7.2 Odoo 19 notes

- The list view tag is `<list>`, not `<tree>`.
- `_description` is mandatory on every model.
- Groups carry a `privilege_id` so they appear on the user form; users link to groups through `group_ids`.
- Relational writes in XML use `Command.link`, `Command.set`, `Command.create`, not the old `(4, id)` tuples.
- Search-view `<group>` elements take no `string` or `expand` attributes.
- XPath on a class uses `hasclass('name')`, not `@class='name'`.

### 7.3 Things that break the whole stack

- A top-level folder named `forms`, `helpers`, `mixins`, `utilities` or `vendor` in your repository: Odoo resolves
  Bootstrap's stylesheet imports against the addons root, and every page loses its styling. `doctor` reports it, `start`
  refuses to run, the hooks block it. Rename the folder.
- Odoo keeps a compiled stylesheet bundle while its version hash matches, and the hash comes from the source files, not
  from a successful compile. After any broken build, `./odoo-project resetassets`.
- `./odoo-project update` cannot install a new module; `install` can. A first `start` on a fresh database installs
  OpenSPP and waits; do not run `install` until it has printed the URL.

### 7.4 Before you commit

1. `./odoo-project test <module>`: the summary line reads `0 failed, 0 error(s)`.
2. `./odoo-project lint`: clean.
3. `./odoo-project audit-security`: 0 errors, 0 warnings.
4. `git commit`: the hooks pass. Commit messages follow `feat(scope): ...`, `fix(scope): ...`, `docs(scope): ...`.

### 7.5 Where to read more

- `docs/guides/extending-openspp.md`: the companion of Module 4, step by step.
- `docs/guides/module-development.md`: the full scaffold for a new module, starter and variant patterns.
- `docs/guides/testing-guide.md` and `docs/principles/testing.md`.
- `docs/principles/access-rights.md`: the three-tier security model.
- `upstream/openspp/<module>/readme/DESCRIPTION.md` and `upstream/openspp/AGENTS.md`: what each OpenSPP module does and
  the upstream conventions.
- `training/4ps-program-reference.md`: the 4Ps program in the terms the code uses.
- <https://docs.openspp.org> and <https://www.odoo.com/documentation/19.0/developer.html>.

### 7.6 Glossary

| Term                         | Meaning                                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Addons path                  | The folders Odoo scans for modules; your repository root is one of them inside the container.                         |
| Manifest                     | `__manifest__.py`: the module's name, dependencies and data files.                                                    |
| ORM                          | Odoo's object layer: `create`, `write`, `search`, `unlink` on a model instead of SQL.                                 |
| MVC                          | Model, view, controller: in Odoo, `models.Model`, XML views and QWeb templates, and actions, menus and model methods. |
| QWeb                         | Odoo's template engine: HTML with `t-` attributes, used by reports and by the web client.                             |
| Domain                       | A list of `(field, operator, value)` conditions passed to `search` and to filters.                                    |
| Model, field                 | A table and a column, declared in Python.                                                                             |
| View                         | XML that draws a model as a list, a form or a search box; an `ir.ui.view` record.                                     |
| Action, menu                 | An action names a model and its views; a menu points at an action.                                                    |
| XML id                       | The address of a record defined in a data file, `module.name`; used by `ref=` and `env.ref`.                          |
| Access row                   | One line of `ir.model.access.csv`: what one group may do on one model.                                                |
| Group, privilege, category   | A permission tier; what the user form shows for it; the heading it sits under.                                        |
| `_inherit`                   | Add fields and behaviour to an existing model.                                                                        |
| Inherited view               | A view that modifies another with XPath on named elements.                                                            |
| `noupdate`                   | Data loaded once on install and never overwritten by an update.                                                       |
| Vocabulary, code             | OpenSPP's code lists as data, with namespace URIs; `spp.vocabulary` and `spp.vocabulary.code`.                        |
| Registrant, household, group | A `res.partner` with `is_registrant`; a household is also `is_group`.                                                 |
| SWDI                         | Social Welfare and Development Indicators: the 4Ps yearly well-being assessment, levels 1 to 3.                       |
| `TransactionCase`            | The Odoo test base class: each test runs in a rolled-back transaction.                                                |
