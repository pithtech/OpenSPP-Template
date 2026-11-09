---
marp: true
theme: default
paginate: true
size: 16:9
title: "Module 5: DSWD-specific implementation of OpenSPP"
style: |
  section pre { font-size: 0.6em; }
  section table { font-size: 0.85em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 5

## DSWD-specific implementation of OpenSPP: the 4Ps modules, discussed

OpenSPP and Odoo Foundations Training, Day 2, 1:00 to about 5:08

Edwin Gonzales, OpenSPP

---

<!-- _footer: "Guide 5.1" -->

<style scoped>ol, p { font-size: 0.72em; }</style>

## By five you can

1. Place any `dswd_4ps_*` module on the map: what part of the 4Ps process it serves and which instance it installs on.
2. Given a 4Ps event (a grantee changes, a school attendance form arrives, a payroll run, an SWDI assessment), name the module that handles it and the `spp_*` module it extends.
3. Given a ticket, name the module and the part to open first.
4. Recognise the production traps (context keys that skip checks, `x_4ps_` fields, raw SQL, `noupdate` data and install hooks, system parameters, approval state) and say why "simplifying" them is dangerous.
5. Find any module in the catalogue and read its card.
6. Use Claude Code to read and change code in your repository, and review what it wrote before you trust it (5.13).
7. Give Claude Code a specification and the project's decisions as files, and take a module from them through research, a plan, a test and the code (5.14).

A discussion of modules: we read the code, at the file each point is about.

---

<!-- _footer: "Guide 5.2 · Catalogue: How to read a card" -->

## How to read a card

| Part                      | Says                                                        |
| ------------------------- | ----------------------------------------------------------- |
| Table                     | 4Ps process, instance, depends on, used by, size            |
| Key models                | **new table** (`_name`) or **extends** (`_inherit`)         |
| The strip                 | the twelve parts of a module from this morning; ■ = notable |
| Important points          | what changes how you work on it                             |
| A ticket usually lands in | files, each with a symptom                                  |
| Code moment, excerpt      | the file we open now, and the lines shown                   |

The strip: Manifest 3.6 · Models 3.7/4.6 · Fields 3.8 · Views 3.9/4.7-4.8 · Wizards 3.10 · Security 3.11-3.12/4.9 · Tests 3.13/4.10 · ORM 3.15 · Jobs 3.17 · Reports 3.18 · Vocabularies 4.4 · Migrations 4.13

---

<!-- _footer: "Guide 5.2, 5.11 · Category cards" -->

## Your category cards

**M** model · **V** view · **D** data or vocabulary · **S** security · **W** wizard · **J** job · **A** API · **T** test

I read a symptom. Your pair holds up the card for the file you would **open first**.

Warm-up: "The list of reasons for a grantee change needs 'working abroad'."

---

<!-- _footer: "Guide 5.3 · Map poster" -->

<style scoped>table { font-size: 0.65em; } td:last-child { white-space: nowrap; } p { font-size: 0.75em; }</style>

## The map: 66 modules, 26 cards

| Question       | Modules                                                                                          | Cards    |
| -------------- | ------------------------------------------------------------------------------------------------ | -------- |
| Where          | `area`                                                                                           | 2        |
| Who            | `registry`                                                                                       | 3        |
| Who may        | `roles`, `approval_multi_group`, `approval_flow_data`                                            | 4 to 6   |
| When           | `period`                                                                                         | 7        |
| Change         | `change_request`, `supporting_docs_data`, `field_limit`                                          | 8 to 10  |
| Verify         | `compliance`, `fds_operations`                                                                   | 11, 12   |
| Pay            | `payroll`, `catchup_payroll`, `retro_payroll`                                                    | 13 to 15 |
| Assess, manage | `swdi`, `cms`, `swdi_cms`                                                                        | 16 to 18 |
| Connect        | the bridge, `api` and its route modules, the portal APIs, `integration`, `newgrs`, `ods`, `auth` | 19 to 26 |

Under all of them sits OpenSPP: `spp_registry`, `spp_area`, `spp_vocabulary`, `spp_security`, `spp_programs`, `spp_change_request_v2`, `spp_event_data`, `spp_case_base`, `spp_api_v2`.

---

<!-- _footer: "Guide 5.3 · Card 1" -->

## Two instances, or one (card 1)

- **Instance 1**, registry and operations: `dswd_4ps_instance1`, with `bridge_server`.
- **Instance 2**, casework: `dswd_4ps_instance2`, with `bridge_client`: SWDI, CMS, the casework portal API.
- **Single**: `dswd_4ps_starter` installs both sides on one database, no bridge.
- Manifest `excludes` enforce the split: 26 modules exclude `bridge_client`, 8 exclude `bridge_server`.

Code moment: `dswd_4ps_instance1/__manifest__.py`. A manifest is the map of a deployment (3.6).

---

<!-- _footer: "Guide 5.2, 3.12, 3.17, 4.13, 4.4, 5.10, 3.10 · Cards 2, 4, 11, 13" -->

<style scoped>table { font-size: 0.6em; }</style>

## Primer: five things on every card

| Concept                               | What it is                                                                                                             | In production                                                                                             |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Record rules (3.12)                   | An access row says which models a group may use; a record rule says which rows of a model a user may see.              | `dswd_4ps_area` shows each user only the areas in or above their center areas, none without one (card 2). |
| Jobs and scheduled actions (3.17)     | A job is work queued with `with_delay()` that runs later in the background; a scheduled action (cron) runs on a clock. | A school attendance event queues a job on `cv_events`, and a daily cron finishes the household (card 11). |
| Migrations and `noupdate` (4.13, 4.4) | A `noupdate` data file loads once, at install; changing its records on a running database takes a migration.           | Every group, role and rule file in `dswd_4ps_roles` is `noupdate`: 20 migrations so far (card 4).         |
| Hooks (5.10)                          | A hook is code Odoo calls at a fixed moment: `post_init_hook` once after install, `_register_hook` at every load.      | The `post_init_hook` of `dswd_4ps_area` loads the PSGC areas at install, and never again (card 2).        |
| Wizards (3.10)                        | A wizard is a temporary model behind a dialog: the user fills in a small form, and its button does the work.           | The payroll Reject + Rewind wizard offers no rewind once credit instructions exist (card 13).             |

The glossary (7.6) has a line on each of the five.

---

<!-- _footer: "Guide 5.4 · Card 2" -->

## Foundation: area (card 2)

- PSGC regions to barangays in `spp.area`; about 42,000 barangays queued as jobs at install.
- The install hook runs once: every later data fix is a migration (10 so far).
- Fail-closed: a user with no center areas sees no areas.
- `area_scope_ids`: 15 to 20 s per dashboard tile at 7.4 million households, 99 ms after. Do not simplify it.

---

<!-- _footer: "Guide 5.4, 3.12 · Card 2" -->

## Area: a fail-closed record rule (3.12)

`dswd_4ps_area/security/area_record_rules.xml`, lines 41 to 52, abridged (domain wrapped; the `name` line and the four `perm_` lines cut: the rule is read only). Card 2 has every line.

```xml
<record id="rule_spp_area_center_area_filter" model="ir.rule">
    <field name="model_id" ref="spp_area.model_spp_area" />
    <field
        name="domain_force"
    >[] if user.sees_all_areas
       else (['|', ('id', 'child_of', user.center_area_ids.ids),
                   ('id', 'parent_of', user.center_area_ids.ids)]
             if user.center_area_ids
             else [('id', '=', False)])</field>
    <field name="global" eval="True" />
</record>
```

---

<!-- _footer: "Guide 5.4 · Card 3" -->

## Foundation: registry (card 3)

- Extends `res.partner`: `listahanan_id`, `client_status_id`, `grantee_id`, `member_id_4ps`, ...
- 27 vocabularies: 32 client statuses in 9 categories, 57 set groups, 394 IP groups. A status's `parent_id` is its category.
- Writes go through `_4ps_write_hook`, wired into the audit decorator by `_register_hook`: a breakpoint in `write()` may never be reached.
- Status 3 is a permanent exit: a normal user's write cannot move a household out; a server-side path can.
- Three field-name styles: no prefix, `x_4ps_`, `dswd_export_`. Search all three before adding a field.

---

<!-- _footer: "Guide 5.4, 4.4 · Card 3" -->

## Registry: a status and its category (4.4)

`dswd_4ps_registry/data/vocabulary_client_status.xml`, lines 95 to 101

```xml
<record id="client_status_3" model="spp.vocabulary.code">
    <field name="vocabulary_id" ref="vocab_client_status" />
    <field name="code">3</field>
    <field name="display">3 - Graduated Due to Improved Level of Well-Being</field>
    <field name="parent_id" ref="client_status_category_delisted" />
    <field name="sequence">3</field>
</record>
```

---

<!-- _footer: "Guide 5.4 · Card 4" -->

## Foundation: roles (card 4)

- 54 groups and 48 roles: POO, RPMO and NPMO umbrella groups are the approval tiers; sub-roles such as MSWDO and SWO III imply them through `implied_ids` (3.11).
- Local roles take their areas from the identity provider; RITO may lock them.
- Every group, role and rule file is `noupdate`: 20 migrations so far.

`dswd_4ps_roles/security/groups.xml`, lines 103 to 110, abridged (the `comment` line cut; card 4 has every line)

```xml
<record id="group_4ps_poo_mswdo" model="res.groups">
    <field name="name">4Ps POO: MSWDO</field>
    <field name="implied_ids" eval="[
        Command.link(ref('group_4ps_poo')),
        Command.link(ref('spp_registry.group_registry_officer')),
    ]"/>
</record>
```

---

<!-- _footer: "Guide 5.4 · Cards 5, 6" -->

## Approvals (cards 5 and 6)

- `approval_multi_group`: several groups per tier, any of them may approve. It replaces two upstream constraints **without `super()`**.
- `approval_flow_data`: 21 definitions, 19 linked to 6 change-request types, chosen by CEL on the status transition.
- No match: approves on submit. Reinstate Household keeps a catch-all; Change Address has no linked definition.

---

<!-- _footer: "Guide 5.4 · Card 6" -->

## Approval flow data: 24 to 3, two tiers

`dswd_4ps_approval_flow_data/data/approval_defs_update_hh_info.xml`, lines 81 to 91, abridged (group and condition wrapped; `model_id`, `approval_type` and `sequence` cut; card 6 has every line); its two tiers, SWO III then RGO, follow at lines 94 to 112

```xml
<record id="approval_def_hh_info_poo_rpmo" model="spp.approval.definition">
    <field name="name">Family - Update Family Info - CS (24 → 3)</field>
    <field name="approval_group_ids" eval="[
        Command.link(ref('dswd_4ps_roles.group_4ps_swo_iii'))]" />
    <field name="use_cel_condition" eval="True" />
    <field name="cel_condition">record.selected_field_name == "client_status_id"
        and old_value.code == "24" and new_value.code == "3"</field>
    <field name="sla_days">10</field>
    <field name="is_require_comment" eval="True" />
</record>
```

---

<!-- _footer: "Guide 5.4 · Card 7" -->

<style scoped>ul, p { font-size: 0.8em; }</style>

## Foundation: period (card 7)

- One `spp.compliance.period` per month; the Philippine working-day calendar.
- Fail-loud: a year not marked Seeded raises an error rather than give a deadline that is too early.
- Each December, an administrator enters next year's holidays and marks the year Seeded.
- Dates only, never datetimes.

`dswd_4ps_period/models/holiday_year.py`, lines 34 to 44, abridged (`string`, `required` and `default` cut; card 7 has every line)

```python
state = fields.Selection(
    selection=[
        ("draft", "Draft"),
        ("seeded", "Seeded"),
    ],
    help="Deadlines are only computed across years marked Seeded. A Draft "
    "year is treated as unmaintained and refused.",
)
```

---

<!-- _class: lead -->

# Checkpoint 1

Stand up. Three symptoms. Category card, then the module.

---

<!-- _footer: "Guide 5.5" -->

## Change requests: the upstream shape

| Part           | Is                                                                       |
| -------------- | ------------------------------------------------------------------------ |
| Type           | A data record, `spp.change.request.type`, in a `data/cr_type_*.xml` file |
| Detail model   | The proposed values, one model per type (`models/cr_detail_*.py`)        |
| Apply strategy | Validates, previews and applies the change                               |
| Approval       | `spp.approval.mixin`, multi-tier, routed by the approval definitions     |

4Ps adds 20 new types and rules. It does not change this shape.

---

<!-- _footer: "Guide 5.5 · Card 8" -->

## Card 8: a type is a data record

`dswd_4ps_change_request/data/cr_type_change_address.xml`, lines 13 to 23, abridged (`description`, `detail_form_view_id`, `icon` and `sequence` cut; card 8 has every line)

```xml
<record id="cr_type_change_address" model="spp.change.request.type">
    <field name="name">Change Address</field>
    <field name="code">change_address</field>
    <field name="target_type">group</field>
    <field name="detail_model">spp.cr.detail.change_address</field>
    <field name="apply_strategy">field_mapping</field>
    <field name="auto_apply_on_approve">True</field>
```

9 of the 20 new types are pure field mappings; 11 have a Python apply model.

---

<!-- _footer: "Guide 5.5, 5.10 · Card 8" -->

## Change requests: what to know (card 8)

- Requests are batched under a ticket number; a `cancelled` state is added to the approval mixin.
- Some requests create others: a newborn's Add Member creates Update Pregnancy and Update Member Additional Information requests for the parents.
- Record access is checked in code (`models/cr_parent_access.py`), not by a record rule. Its docstring says why.
- 14 context keys of its own; 11 skip or override a check. Never pass one to make a test pass.

---

<!-- _footer: "Guide 5.5 · Cards 9, 10" -->

## Documents and limits (cards 9 and 10)

<style scoped>ul, p { font-size: 0.8em; }</style>

- `supporting_docs_data`: which documents each type needs. Add Member needs any one of seven.
- `field_limit`: caps how often a field may change, in a `write` override.
- Adding a field to a request type touches more than one file: the detail model and its view; the field mapping in the type's `noupdate` data file, so a migration and a version bump; the API schema and service if the mobile app sends the field; the supporting-documents trigger path; the tests.

`dswd_4ps_supporting_docs_data/data/cr_type_add_member_4ps.xml`, lines 13 to 17 (record line wrapped)

```xml
<odoo noupdate="1">

    <record id="dswd_4ps_change_request.cr_type_add_member_4ps"
            model="spp.change.request.type">
        <field name="document_validation_mode">required</field>
        <field name="trigger_api_paths">addMembers[]</field>
```

---

<!-- _class: lead -->

# Break

Back at 2:48

---

<!-- _footer: "Guide 5.6 · Card 11" -->

## Compliance (card 11)

- School attendance, health and deworming forms arrive through the `/cv` API (the router is in `dswd_4ps_api_compliance`) as `spp.event.data` events.
- The event's `create` hands the work to a job (3.17); the job takes a per-household lock, writes one row and marks the household; a daily reconcile finishes it. Status rows are a cache rebuilt from events.
- When a submitted form changes nothing, look at the event and its job before the code.
- The school threshold is the constant 85 in `models/compliance_pipeline.py`. A system parameter with a similar name only feeds display fields.

---

<!-- _footer: "Guide 5.6, 3.17 · Card 11" -->

## Compliance: the job retries on a busy lock, then marks the household (3.17)

`dswd_4ps_compliance/models/event_data.py`, lines 160 to 171

```python
    self.with_delay(
        channel="cv_events",
        description="CV: Process compliance event (retry)",
        eta=5,
    )._cv_process_compliance()
    return

self._cv_compute_from_event(self.env["spp.cv.compliance.pipeline"])

# Mark household for deferred aggregation by the reconciliation cron
if household:
    household.write({"x_4ps_cv_needs_reconcile": True})
```

---

<!-- _footer: "Guide 5.6 · Card 12" -->

## FDS operations (card 12)

- Session library, parent groups (up to `pg_max_members`, 30 by default), plans with approval, attendance, the FDS Accomplishment Report.
- FDS attendance arrives as session attendance, not as event data.
- An equivalency creates a synthetic session, so the compliance pipeline needs no special case.

`dswd_4ps_fds_operations/models/fds_equivalency.py`, lines 439 to 446, abridged (lines 443 to 445 cut; card 12 has every line)

```python
session_vals = {
    "name": _("Equivalency: %(ref)s", ref=self.name),
    "session_type_id": fds_type.id,
    "date": self.date_completed,
}
```

---

<!-- _footer: "Guide 5.7 · Cards 13 to 15" -->

<style scoped>ul, p { font-size: 0.75em; }</style>

## Payroll: what not to break (cards 13 to 15)

- The cycle run is a state machine (`STATE_SELECTION`). Once credit instructions exist, cancel and rewind are refused: the point of no return.
- The snapshot, which the code calls NAPA, is sealed: `models/snapshot_beneficiary.py` refuses writes, and every later step reads it. A name corrected after the seal does not appear on that cycle's payroll list, by design.

- Grant rates are never deleted. Five job channels; about 110 raw SQL calls.

`dswd_4ps_payroll/models/payroll_cycle_run.py`, lines 147 to 149 (the set wrapped; card 13 has lines 147 to 152)

```python
# States from Step 8b onward — Credit Instructions is the point of no return.
# Cancel is disabled from these states.
POINT_OF_NO_RETURN_STATES = frozenset(
    {"instructions_generated", "lbp_uploaded", "done"}
)
```

Catch-up (card 14): the same state machine, its own point of no return. Retro (card 15): over- and underpayment ledgers, reusing the regular run.

---

<!-- _footer: "Guide 5.8 · Cards 16, 17" -->

<style scoped>ul, p { font-size: 0.75em; }</style>

## Casework: the SWDI level (card 16)

- `swdi`: the yearly well-being assessment. The level comes from the total score (level 3 from 2.83, level 2 from 1.83). This is the well-being level of Module 4, computed: the household's level is copied from the latest assessment, not chosen from a dropdown.
- `cms` (card 17): Kilos-Unlad case management on `spp_case_base`, with 117 record rules for six groups, each scoped by the user's own center areas (3.12 at production scale).

`dswd_4ps_swdi/models/assessment.py`, lines 1233 to 1241, the end of `_classify_lowb` (card 16 has lines 1230 to 1241)

```python
- Level 3: score >= 2.83
- Level 2: score >= 1.83
- Level 1: otherwise
"""
if score >= LOWB_LEVEL_3_MIN_SCORE:
    return "3"
if score >= LOWB_LEVEL_2_MIN_SCORE:
    return "2"
return "1"
```

---

<!-- _footer: "Guide 5.8, 5.10 · Cards 18, 19" -->

<style scoped>ul, p { font-size: 0.8em; }</style>

## Assessments become cases (card 18)

- Seven triggers, each a data record. Approving an assessment queues an event; a job creates the case.
- Retries after 5 minutes, 15 minutes, 1 hour. A failed event stays as a row in state `failed`, with a Retry action.

`dswd_4ps_swdi_cms/models/cms_trigger_config.py`, lines 41 to 43 (abridged; card 18 has the field in full)

```python
trigger_type = fields.Char(
    string="Trigger Type",
    required=True,
```

Its `help`: "One of: PRIORITY_CASE, GRADUATION, FRVA_HIGH_RISK, CHILD_PROTECTION, MISBEHAVIOR, WAIVE_EXIT."

The bridge (card 19): the registry instance is the master. Casework looks households up and imports them synchronously, waiting at most 5 seconds; case events flow back through jobs.

---

<!-- _footer: "Guide 5.9 · Cards 20 to 26" -->

<style scoped>p { font-size: 0.8em; }</style>

## The API's rules (card 20)

`dswd_4ps_api/routers/household.py`, lines 96 to 106

```python
async def read_grantee_history(
    identifier: Annotated[str, Path(description="Format: {system}|{value}")],
    env: Annotated[Environment, Depends(authenticated_env)],
    auth: Annotated[dict, Depends(get_auth_with_rate_limit)],
):
    """Grantee change audit trail."""
    _check_read_access(auth)

    system, value = parse_identifier(identifier)
    service = HouseholdService(env)
    household = service.find_by_identifier(system, value)
```

The caller's rights (`authenticated_env`: record rules apply while `dswd_4ps_api.enforce_rbac` is on, seeded on), a scope check, an identifier, never a database id, then a service.

The rest of integration is on cards 21 to 26.

---

<!-- _footer: "Guide 5.11 · Triage sheet" -->

## Ticket triage

In pairs. Eight training scenarios, not real incidents.

For each: the **module**, the **category card**, the **first file**. Use your catalogue.

Ten minutes, then report-back.

---

<!-- _footer: "Triage sheet · Cards 2, 6, 8, 9, 12, 18, 22; index" -->

<style scoped>table { font-size: 0.7em; }</style>

## Triage: the answers

| #   | Module (card)              | Letter | First file                                                     |
| --- | -------------------------- | ------ | -------------------------------------------------------------- |
| 1   | `area` (2)                 | M or S | `models/registrant.py`, then `hooks.py`                        |
| 2   | `change_request` (8)       | V      | `views/change_request_views.xml`: the search view              |
| 3   | `approval_flow_data` (6)   | D      | `data/approval_defs_update_hh_info.xml`                        |
| 4   | `fds_operations` (12)      | W      | `wizards/fds_parent_group_transfer.py`: the cap, Max Members   |
| 5   | `supporting_docs_data` (9) | D      | `data/cr_type_add_member_4ps.xml`, then a migration            |
| 6   | `export` (no card)         | J      | `models/dswd_export_batch.py`: the chunk jobs on `dswd_export` |
| 7   | `swdi_cms` (18)            | J      | `models/cms_event.py`                                          |
| 8   | `payroll_api` (22)         | A      | `services/payroll_service.py`                                  |

---

<!-- _footer: "Guide 5.13" -->

## Claude Code in development: what it is

A demo on the trainer's laptop, in a repository made from the template.

An AI assistant in your terminal, inside your repository: it reads files, runs commands such as `./odoo-project test`, and writes changes, asking before each action.

| It is good at                              | It stays with you              |
| ------------------------------------------ | ------------------------------ |
| Reading a large code base                  | Deciding what to build         |
| The repetitive parts of a change           | Reviewing what it wrote        |
| Running the loop: test, change, test again | Testing, and owning the change |

---

<!-- _footer: "Guide 5.13" -->

<style scoped>table { font-size: 0.75em; }</style>

## What it reads before it answers

| File                    | What it gives Claude Code                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`             | The project's rules: naming, extension patterns, the checklist, the commands, the known pitfalls     |
| `.claude/rules/`        | Loaded when it edits matching files: models, views and data, security, tests, manifests              |
| `.claude/agents/`       | Five specialists: `odoo-developer`, `code-reviewer`, `ux-expert`, `code-simplifier`, `verify-module` |
| `.claude/commands/`     | `/implement`, `/verify-tests`, `/analyze`, `/expert-review`, `/commit`, `/pr`                        |
| `.claude/settings.json` | Allowed commands; no edits under `upstream/`; a lint hook after every edit; no AI attribution        |
| `docs/specs/`, ADRs     | The change you ask for, and the decisions the project has taken (guide 5.14)                         |

Your repository has all of them: they came with the template.

---

<!-- _footer: "Guide 5.13" -->

<style scoped>ul, p { font-size: 0.75em; }</style>

## Demo A: reading code

_"Where does OpenSPP keep a household's members, and how do I get each member's age?"_

Check the answer against the files in `upstream/openspp/spp_registry/models/`:

- `group.py`: the household is a `res.partner` with `is_group`; its members are `group_membership_ids`.
- `group_membership.py`: `spp.group.membership` with `group`, `individual`, `start_date`, `ended_date`, `is_ended`.
- `individual.py`: `birthdate`, and `age`. **Trap 1**: `age` is a text field (`"5"`, or `"No Birthdate!"`). Count by `birthdate`.

_"Use OpenSPP's existing `children_count` field on the household."_

**Trap 2**: there is no such field. The name is only an example in a help text and a Studio variable name. A name seen somewhere is not a field: check the model.

---

<!-- _footer: "Guide 5.14" -->

<style scoped>table { font-size: 0.7em; } ol { font-size: 0.8em; }</style>

## From a specification to a module

| File                                | Holds                                               | Written by                      |
| ----------------------------------- | --------------------------------------------------- | ------------------------------- |
| `docs/architecture/decisions/`      | A decision that outlives one change (ADR)           | You, reviewed in a pull request |
| `docs/specs/<module>.md`            | One change: need, rules, acceptance examples, scope | You, or the analyst             |
| `docs/planning/research-<topic>.md` | What exists, what is missing, open questions        | Claude Code, checked by you     |
| `docs/planning/plan-<topic>.md`     | The files, the tests first, the steps               | Claude Code, annotated by you   |

1. Write the specification and any ADR, on a branch.
2. Research: it reads them and the OpenSPP code they name, and writes a file. Check it.
3. Plan: it writes the plan to a file. Add your notes; it addresses them.
4. Implement, test first. For a larger change, `/implement`; say "test first".
5. Review with the checklist, including point 9, then `/commit` and `/pr`. The body links the specification and the ADR.

---

<!-- _footer: "Guide 5.14" -->

<style scoped>table { font-size: 0.72em; } p { font-size: 0.85em; }</style>

## What a specification states

| Kind                             | The specification states                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| A new module with a new model    | The model and its fields with types; which are required; who reads and who writes (the three tiers); the menu |
| An extension of an OpenSPP model | The upstream model and view, by their names in `upstream/openspp/`; what to add; where on the view            |
| A customization through data     | The records to create; the vocabulary namespace and codes; `noupdate` or not; what keeps the codes valid      |
| All three                        | The 4Ps need in the users' words; the rules; acceptance examples as a table; out of scope; the ADRs it uses   |

It says what and why, not which fields or files: that is the plan's job. Each acceptance example becomes a test.

A rule not written down is one Claude Code will guess.

---

<!-- _footer: "Guide 5.14" -->

<style scoped>ul, p { font-size: 0.75em; }</style>

## Demo B: the specification, the research, the plan

- `docs/specs/dswd_household_children.md`: current members aged 0 to 18, from the birthdate, on the household Profile page; four acceptance examples.
- `ADR-002`: a count that depends on age is computed when read, not stored. A child turns 19 with no write to the database.

_"Read docs/specs/dswd_household_children.md and the ADRs it links, then the OpenSPP models they name in upstream/openspp/. Write docs/planning/research-household-children.md: what exists, what is missing, your questions. Do not write code."_

_"Write the plan to docs/planning/plan-household-children.md: the files, the tests first, the steps."_

`> NOTE: Add a test for a member with no birthdate.` Then: _"Address my notes in the plan."_

---

<!-- _footer: "Guide 5.14, 5.13" -->

<style scoped>ul, p { font-size: 0.75em; } table { font-size: 0.7em; }</style>

## Demo B: test first, then the code

_"Carry out the plan, test first: write the failing test, run it, then the code."_

| Test                        | Household members                     | Expects            |
| --------------------------- | ------------------------------------- | ------------------ |
| Counts current children     | aged 5, 12, 17 (membership ended), 30 | 2                  |
| 0 to 18 inclusive           | aged 18 and 19                        | 1                  |
| No birthdate, not counted   | aged 7, and one with no birthdate     | 1                  |
| No members                  | none                                  | 0                  |
| Shown on the household form | the Profile page                      | the field is there |

Say "test first": `/implement` writes the tests after the code unless you ask.

`./odoo-project test dswd_household_children`: red, then green. The lint hook runs after every edit.

**Trap 3**: a test that ends a membership also sets `start_date` in the past. OpenSPP refuses an end date earlier than the start date, which defaults to now.

---

<!-- _footer: "Guide 5.13" -->

<style scoped>ol { font-size: 0.68em; }</style>

## Review what it wrote

1. Does the test fail without the change and pass with it? Does it test the behaviour, not the implementation?
2. Is every new file in the manifest? Is every new field in a view, if users need it?
3. Is anything changed under `upstream/openspp/`? (It should be blocked; check anyway.)
4. Do names follow guide 7.1 (`dswd_` prefix, model and XML id patterns)?
5. Does it claim something about the code you have not seen in a file? Open the file.
6. Did it run the module's tests, and did you read the summary line yourself?
7. Nothing secret or personal in the prompt or the diff: no beneficiary data, passwords, tokens or keys.
8. Commit messages and pull requests carry no AI attribution in this project (`settings.json` turns it off; `/commit` and `/pr` repeat it).
9. When the change has a specification: does the code do what each of its acceptance examples says?

---

<!-- _footer: "Guide 5.13" -->

<style scoped>ul, p { font-size: 0.85em; }</style>

## Safe use

What you type goes to an external AI service. **Never in a prompt, or in a file you ask it to read**: beneficiary or other personal data, passwords, tokens, keys, database dumps, code you may not share.

Read every permission request. Never approve a command you do not understand.

Live: ask it to edit a file under `upstream/`. `.claude/settings.json` refuses (line 26, abridged):

```json
"deny": ["Edit(upstream/**)", "Write(upstream/**)", ...]
```

A change to OpenSPP is a pull request to OpenSPP, not an edit here.

---

<!-- _footer: "Guide 5.13" -->

## Demo C: commit, pull request, CI

1. `/commit`: a conventional commit message; the pre-commit hooks run.
2. `/pr`: pushes the branch, opens the pull request and fills its template; the body links the specification and ADR-002.
3. No AI attribution: `settings.json` has `includeCoAuthoredBy: false`, and `/commit` and `/pr` say so.
4. CI on a pull request prepared yesterday evening: pre-commit, image build, module tests.
5. Review and merge, as for a change you wrote yourself (guide 7.4).

---

<!-- _footer: "Guide 5.13, 5.14" -->

## Where to read more

- Guide 5.13: what it reads, the test-first loop, the review checklist, safe use, commit and pull request.
- Guide 5.14 and `docs/specs/README.md`: the specification template. Try the flow yourself on `docs/specs/dswd_household_children.md`.
- `docs/guides/claude-code-for-developers.md` in your repository: every file under `.claude/`, and your personal settings in `.claude/settings.local.json`.
- `CLAUDE.md` in your repository: read it once yourself. It is what Claude Code reads first.

Questions.

---

<!-- _footer: "Guide 5.11" -->

## How to approach a 4Ps ticket

1. Read the symptom in the user's words, and reproduce it.
2. Find the module on the map (5.3) and open its card.
3. Read the strip: the shaded boxes are where its tickets land. Pick the first file.
4. Before changing code, check what runs around it: `noupdate` data, context keys, jobs and their state, system parameters.
5. Write a failing test that reproduces the ticket, then fix, then run the module's tests.

---

<!-- _footer: "Guide 5.12 · Catalogue index" -->

## Not today

The modules on no card are in the catalogue index, for the post-training sessions:

- Registry tools: `registry_import`, `export`, `ecr`, `hazard`, `account_creation`
- Operations: `theme`, `attachment_hardening`, `post_sql_repair`, `pg_partition`
- Dashboards: `swdi_dashboard`, `cms_nas`
- 17 sample-data, demo and test modules

Keep the catalogue.
