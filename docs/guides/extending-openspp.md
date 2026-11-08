# Extending OpenSPP

How to add 4Ps behaviour to OpenSPP without touching OpenSPP. Read this before your first module.

## The One Rule

**Never modify OpenSPP.** It runs from the Docker image and sits read-only in `upstream/openspp/`. Everything you
need is reachable through Odoo's extension mechanisms: `_inherit`, inherited views, hooks, security groups, data
files, and configuration. If upstream has a bug, work around it in your module and send OpenSPP a pull request.

## Step 1: Find What You Are Extending

```bash
./odoo-project vendor                  # once; fetches upstream/openspp at the pinned release
grep -rn "_name = \"spp.program\"" upstream/openspp/*/models/
grep -rln "is_registrant" upstream/openspp/spp_registry/models/
ls upstream/openspp/spp_programs/{models,views,security,tests}
```

Read, in this order: the module's `readme/DESCRIPTION.md`, the model file, its `security/` folder, the view you
will inherit, and one of its tests. Note the hooks (`_pre_*`, `_post_*`), the group XML IDs, and the named
groups/pages in the form view.

Key upstream modules:

| Need                                  | Module                    | Models                                         |
| ------------------------------------- | ------------------------- | ---------------------------------------------- |
| Registrants, households, IDs          | `spp_registry`            | `res.partner`, `spp.group.membership`, `spp.registry.id`, `spp.id.type` |
| Security categories and admin group   | `spp_security`            | groups and categories only                     |
| Geographic areas                      | `spp_area`                | `spp.area`                                     |
| Programs, cycles, entitlements        | `spp_programs`            | `spp.program`, `spp.program.membership`, `spp.cycle`, `spp.entitlement`, `spp.entitlement.inkind` |
| Event data (attendance, visits)       | `spp_event_data`          | `spp.event.data`                               |
| Change requests                       | `spp_change_request_v2`   | `spp.change.request`, `spp.change.request.type` |
| Approvals                             | `spp_approval`            | `spp.approval.mixin`, `spp.approval.review`    |
| Grievances                            | `spp_grm`                 | grievance models                               |
| Vocabularies                          | `spp_vocabulary`          | `spp.vocabulary`, `spp.vocabulary.code`        |
| REST API                              | `spp_api_v2*`             | FastAPI routers                                |

## Step 2: Extend the Model

```python
# dswd_registry_ph/models/res_partner.py
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    dswd_household_number = fields.Char(
        string="4Ps Household Number",
        help="Household identifier assigned by the 4Ps programme",
        index=True,
    )
    dswd_is_indigenous = fields.Boolean(string="Indigenous People")
```

- Prefix every added field with `dswd_` so it never collides with upstream or another extension.
- Do not override `create`/`write` unless you must; prefer computed fields, constraints, and hooks.
- Registrant searches must include `("is_registrant", "=", True)`; households also `("is_group", "=", True)`.

### Use upstream hooks

```python
class SppProgram(models.Model):
    _inherit = "spp.program"

    def _post_enrollment_hook(self, partner):
        super()._post_enrollment_hook(partner)
        partner.with_delay().dswd_initialise_compliance(self)
```

Search upstream for `_hook(` to find extension points. If none exists where you need one, extend the public
method with `super()` and keep your addition small.

## Step 3: Extend the View

```xml
<!-- dswd_registry_ph/views/res_partner_views.xml -->
<odoo>
  <record id="view_res_partner_form_dswd" model="ir.ui.view">
    <field name="name">res.partner.form.dswd</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="spp_registry.view_individuals_form"/>
    <field name="arch" type="xml">
      <xpath expr="//group[@name='demographics_section']" position="after">
        <group name="dswd_4ps" string="4Ps">
          <field name="dswd_household_number"/>
          <field name="dswd_is_indigenous"/>
        </group>
      </xpath>
    </field>
  </record>
</odoo>
```

- Find the upstream view id in `upstream/openspp/<module>/views/` and the named groups inside it.
- Target named elements only. Positional XPath breaks on the next OpenSPP release.
- One inherited view per upstream view per module.
- `spp_registry.view_individuals_form` serves both individuals and households. Individual sections are named
  `demographics_section`, `identity`, and so on; household sections are prefixed `group_` (`group_profile`,
  `group_tags_section`, `group_identity`). A household field goes after a `group_*` anchor.

## Step 4: Security

Put your groups under OpenSPP's categories and link your manager group into the OpenSPP administrator:

```xml
<!-- dswd_attendance/security/groups.xml -->
<odoo>
  <record id="privilege_dswd_attendance" model="res.groups.privilege">
    <field name="name">4Ps Attendance</field>
    <field name="category_id" ref="spp_security.category_spp_programs"/>
  </record>
  <record id="group_dswd_attendance_officer" model="res.groups">
    <field name="name">Officer</field>
    <field name="privilege_id" ref="privilege_dswd_attendance"/>
  </record>
  <record id="group_dswd_attendance_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="privilege_id" ref="privilege_dswd_attendance"/>
    <field name="implied_ids" eval="[Command.link(ref('group_dswd_attendance_officer'))]"/>
  </record>
  <record id="spp_security.group_spp_admin" model="res.groups">
    <field name="implied_ids" eval="[Command.link(ref('group_dswd_attendance_manager'))]"/>
  </record>
</odoo>
```

Then `ir.model.access.csv` for every new model (first row `base.group_system`, full CRUD), and record rules where
officers must see only their area. See `docs/principles/access-rights.md` and
`upstream/openspp/spp_registry/security/` for a complete example.

## Step 5: Tests

```python
from odoo.addons.spp_registry.tests.common import RegistryCommon
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHouseholdNumber(RegistryCommon):
    def test_household_number_is_stored(self):
        """The 4Ps household number is stored on the household registrant."""
        self.group.dswd_household_number = "PH-001"
        self.assertEqual(self.group.dswd_household_number, "PH-001")
```

`RegistryCommon` provides `self.group` (a household), `self.individual_a`, and `self.individual_b`. Run with
`./odoo-project test dswd_registry_ph`. Tests must also run as an officer user, not only as admin.

To see the module in the running instance, install it once with `./odoo-project install dswd_registry_ph`; after that,
`./odoo-project update` picks up changed files (`update` never installs a new module).

## Step 6: Background Work

Anything that touches more than a few hundred records runs in the job worker:

```python
partner.with_delay(channel="root", priority=10).dswd_recompute_compliance()
```

The `jobworker` compose service executes jobs; watch them under **Settings > Technical > Queue Jobs**.

## What Not To Do

- Edit files under `upstream/openspp/` or copy upstream models into your module
- Name modules or models `spp_*` / `spp.*`
- Depend on `spp_starter_sp_mis` (depend on the specific module you extend)
- Expose database ids in APIs, exports, or QR codes; use `spp.registry.id`
- Add `fields.Selection` for values that belong in a vocabulary
- `cr.commit()` in loops; `sudo()` to get past an `AccessError`

## Further Reading

- OpenSPP documentation: <https://docs.openspp.org>
- `upstream/openspp/AGENTS.md` for upstream conventions and pitfalls
- `docs/principles/module-architecture.md`, `docs/principles/access-rights.md`, `docs/principles/api-design.md`
