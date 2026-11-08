---
marp: true
theme: default
paginate: true
size: 16:9
title: "Module 4: Developing Custom Modules and Extending Odoo Models"
style: |
  section pre { font-size: 0.7em; }
  section table { font-size: 0.8em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 4

## Developing Custom Modules and Extending Odoo Models

OpenSPP and Odoo Foundations Training, Day 2, 10:10 to 12:00

Edwin Gonzales, OpenSPP

---

<!-- _footer: "Guide 4.1" -->

## By noon you can

1. Name the role of every file in a `dswd_*` module, and say why a file not in the manifest does not exist.
2. Pick the right pattern for a 4Ps requirement: inherit the upstream model, prefix the field `dswd_`, point it at a vocabulary code.
3. Explain how a view is extended, and recognise the error when the anchor is wrong.
4. Read a log excerpt and say which file to open.
5. Run a module's tests and read the summary line.

Nothing today needs your laptop. Read, predict, diagnose. Keyboard time is Day 3.

---

<!-- _footer: "Guide 4.3" -->

## The requirement

The SWDI assessment places every 4Ps household at one of three levels:

| Level | Code              | Meaning                                    |
| ----- | ----------------- | ------------------------------------------ |
| 1     | `survival`        | cannot meet basic needs without assistance |
| 2     | `subsistence`     | meets basic needs, no buffer               |
| 3     | `self_sufficient` | can sustain itself, may exit the program   |

Since Executive Order 120 (July 2026) the level decides whether a household stays past seven years.

**Today**: put that level on the household record in OpenSPP, as a dropdown on the household Profile page.

---

<!-- _footer: "Guide 4.3" -->

## What you will see at noon

![h:470](images/step3-household-dropdown.png)

---

<!-- _footer: "Guide 4.12" -->

## Where this lives in production

The production 4Ps registry module ships **27 vocabularies** the same way:

- `urn:dswd:4ps:client-status` (32 statuses in 9 categories)
- `urn:dswd:4ps:set-group` (57 set codes, `1A` to `14H`)
- `urn:dswd:4ps:ip-group` (394 codes)
- `urn:dswd:4ps:well-being-level` (the one we build)

Client status and the other household fields are `Many2one` to `spp.vocabulary.code`, exactly like ours.

In production the household's level is copied from the latest SWDI assessment (`dswd_4ps_swdi`, Module 5 card 16, guide 5.8).

---

<!-- _footer: "Guide 4.3" -->

## Anatomy of a module

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

Fill in section 2 of your handout as the steps go by.

---

<!-- _footer: "Guide 4.2" -->

## The three rules

1. **Never edit `upstream/openspp/`.** Read it. Extend it from your module. The next release overwrites it.

2. **Inherit, do not redefine.** `_inherit = "res.partner"` adds to the household. `_name` would create a new table. New fields on upstream models start with `dswd_`.

3. **A file not listed in `__manifest__.py` does not exist.** Data and view files load only if they are in `data`. No error. Just absence.

---

<!-- _footer: "Guide 3.6, 4.3" -->

## Step 0: the manifest

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
    ],
    "application": False,
    "installable": True,
}
```

Installable, does nothing. **Predict**: where will it appear after we install it?

---

<!-- _footer: "Guide 3.6" -->

## After step 0: Apps knows the module

![h:470](images/step0-apps-installed.png)

---

<!-- _footer: "Guide 0.4" -->

<style scoped>
section { font-size: 23px; }
</style>

## The loop

| You changed                                                                     | Run                                                              |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Nothing yet: a brand-new module                                                 | `./odoo-project install dswd_wellbeing`                          |
| `__manifest__.py`, a data file, a security file, a new field, a new view record | `./odoo-project update`                                          |
| A Python method body                                                            | `./odoo-project restart` (nothing with `start --profile dev`)    |
| An existing view's XML                                                          | `./odoo-project update` (nothing with `start --profile dev`)     |
| A record in a `noupdate="1"` data file                                          | a fresh database (`stop -v -y`, `start`, `install`); guide 4.4   |
| A test                                                                          | `./odoo-project test dswd_wellbeing`, then read the summary line |

`update` never installs a new module; `install` does. Both print their errors where you ran them; `./odoo-project logs` shows the running server.

---

<!-- _footer: "Guide 4.4" -->

<style scoped>
pre { font-size: 0.6em; }
</style>

## Step 1: the vocabulary

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

**Predict**: after `update`, where will the three codes show?

---

<!-- _footer: "Guide 4.4" -->

## After step 1: Settings > Vocabularies

![h:470](images/step1-vocabulary-codes.png)

---

<!-- _footer: "Guide 4.4" -->

## Why a vocabulary and not a `Selection`

```python
# Not this
level = fields.Selection([("1", "Survival"), ("2", "Subsistence"), ("3", "Self-Sufficient")])
```

- A code list changes without a release: Settings > Vocabularies, no code change.
- Deployments differ: a region can hide codes with a deployment profile.
- Every code has a URI (`urn:dswd:4ps:well-being-level#survival`) other systems can match.
- 32 client statuses and 394 indigenous peoples groups do not belong in Python.

Static selections are for internal workflow states only.

---

<!-- _footer: "Guide 4.5" -->

## Step 2: the field

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

Plus `from . import res_partner` in `models/__init__.py`. **Predict**: after `update`, what changes on screen?

---

<!-- _footer: "Guide 4.5, 4.11" -->

## The silent failure

`models/res_partner.py` is perfect. `update` says nothing. The field is nowhere.

```python
# models/__init__.py
from . import res_partner      # <- the line that was missing
```

Python never imported the file, so Odoo never saw the class.

Where to look: **Settings > Technical > Fields**, search `dswd_`.

A field without a view is invisible, not broken.

---

<!-- _footer: "Guide 4.5" -->

## Where a field without a view shows up

![h:470](images/step2-technical-fields.png)

---

<!-- _footer: "Guide 4.7" -->

<style scoped>
pre { font-size: 0.6em; }
</style>

## Step 3: the view

```xml
<record id="view_res_partner_form_wellbeing" model="ir.ui.view">
    <field name="name">res.partner.form.dswd.wellbeing</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="spp_registry.view_individuals_form" />
    <field name="arch" type="xml">
        <xpath expr="//group[@name='group_tags_section']" position="after">
            <group name="dswd_4ps_section" string="4Ps">
                <field
                    name="dswd_well_being_level_id"
                    readonly="disabled"
                    options="{'no_create': True, 'no_open': True}"
                />
            </group>
        </xpath>
    </field>
</record>
```

Find the anchor first: open `upstream/openspp/spp_registry/views/individual_views.xml` and search for `name="group_` (Ctrl+F in VS Code).

---

<!-- _footer: "Guide 4.7" -->

## After step 3: the household Profile page

![h:470](images/step3-household-saved.png)

---

<!-- _footer: "Guide 4.11" -->

## Reading an error, bottom up

```
ValueError: Wrong value for spp.vocabulary.domain: 'administrative'
odoo.tools.convert.ParseError: while parsing
  /mnt/extra-addons/custom/dswd_wellbeing/data/vocabulary_well_being_level.xml:10
```

```
Element '<xpath expr="//group[@name=&#39;group_tag_section&#39;]">' cannot be located in parent view
View error context:
{'file': '.../dswd_wellbeing/views/res_partner_views.xml', ..., 'xmlid': 'view_res_partner_form_wellbeing'}
```

Find the first line that names a file in **your** module, open it there, compare it with upstream (the selection, the view). Lint passed on both: it checks shape, not meaning.

---

<!-- _footer: "Guide 4.5, 4.9, 4.10" -->

<style scoped>
section { font-size: 23px; padding-top: 30px; } section pre { font-size: 0.66em; } section h2 { margin-bottom: 6px; } section p { margin: 8px 0; }
</style>

## Steps 4 and 5: the tests

```python
@tagged("post_install", "-at_install")
class TestHouseholdWellBeing(RegistryCommon):
    def test_household_stores_a_level(self):
        subsistence = self.VocabCode.get_code(NAMESPACE, "subsistence")
        self.group.dswd_well_being_level_id = subsistence
        self.assertEqual(self.group.dswd_well_being_level_id.display, "Subsistence")
```

```
$ ./odoo-project test dswd_wellbeing
========== TEST RESULTS ==========
0 failed, 0 error(s) of 5 tests
Passed: 5 | Failed: 0 | Errors: 0
Full log: .../odoo-test-logs/dswd_wellbeing_unittest_<date>_<time>.log
```

A `Many2one` `domain` only filters the dropdown: step 5 adds an `@api.constrains` so code and the API are guarded too.

`security/ir.model.access.csv`: header only. No new model, no rows; access to the field follows `res.partner`.

---

<!-- _footer: "Guide 7.4" -->

## Claude Code: the review is the job

Ask: _"Add a fourth well-being level, `graduated`, sequence 40, and a test that it resolves."_

Then read the diff before running anything:

- Is the new record in the right file, under the right vocabulary?
- Is the file still listed in the manifest?
- Does the test assert something that could fail?

Run the tests. Keep or discard. The tool types; you decide.

---

<!-- _footer: "Guide 7.4" -->

<style scoped>
section { font-size: 24px; }
</style>

## From a change to a merge

| On your laptop                                   | On GitHub                                                   |
| ------------------------------------------------ | ----------------------------------------------------------- |
| 1. `git switch main`, `git pull`                 | 11. Open a pull request (base `main`)                       |
| 2. `git switch -c feat/...`                      | 12. CI: pre-commit, image build, module tests               |
| 3. Test first, then code                         | 13. Review: a second person reads the diff                  |
| 4. `install` or `update` on your stack           | 14. Merge, delete the branch                                |
| 5. Check the screen                              |                                                             |
| 6. `.\odoo-project test <module>`: `0 failed`    | Back on your laptop:                                        |
| 7. `lint`, `audit-security`                      | 15. `git switch main`, `git pull`, `git branch -d feat/...` |
| 8. `git add <files>`, `git status`               |                                                             |
| 9. `git commit -m "feat(scope): ..."`: hooks run |                                                             |
| 10. `git push -u origin feat/...`                |                                                             |

---

<!-- _footer: "Guide 7.4" -->

## CI: the same checks, on a clean machine

Every pull request to `main` runs **pre-commit** and **CI**: the image is built, each changed module is installed in a fresh database, its tests run, coverage must reach 85%.

The first run builds the image: 10 to 25 minutes. Later runs reuse the cache.

Red? **Details**, read the log bottom up, reproduce on your laptop with the same command, fix, push again. Never merge red.

---

<!-- _footer: "Guide 7.4" -->

## Review, then merge

The reviewer reads **Files changed**: tests that could fail, every file in the manifest, nothing under `upstream/`, names that follow the rules, no secrets.

Comments on lines; the author pushes fixes; the reviewer approves; **Merge pull request**, then **Delete branch**.

Then on your laptop: `git switch main`, `git pull`, `git branch -d feat/...`, and `update` if the merge changed a module on your stack. The next change starts at step 1.

---

<!-- _footer: "Guide 4.11" -->

## The five mistakes

| Mistake                                                  | Symptom                                                                | Look at                                    |
| -------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| Data file written but not in manifest `data`             | update clean, UI unchanged                                             | the manifest's `data` list                 |
| Invalid value in a data file (`domain`)                  | `ParseError`, the registry fails to load                               | the upstream field definition              |
| Import missing in `models/__init__.py`                   | no error, field absent; `Field ... does not exist` once a view uses it | Settings > Technical > Fields              |
| Wrong XPath anchor (`group_tag_section`, `@class=`)      | `cannot be located in parent view`                                     | search `name="group_` in the upstream view |
| `restart` instead of `update`, or edited `noupdate` data | change never shows                                                     | the loop table (guide 0.4)                 |

Drill time: three real excerpts, in pairs, 12 minutes.

---

<!-- _footer: "Guide 4.1, 4.14" -->

## Recap, and what comes next

**Today**: manifest, data, model, view, security, tests. Inherit, prefix, point at a vocabulary. Read errors bottom up. Run the tests.

**Module 5 (this afternoon)**: the production 4Ps modules, read through today's parts.

**Module 6 (Day 3)**: your hands on the keyboard. Before Day 3:

```bash
./odoo-project start
./odoo-project test dswd_wellbeing     # 0 failed, 0 error(s) of 5 tests
```

No Docker on your laptop? Tomorrow you work with a pair that has one. Lunch triage table today.
