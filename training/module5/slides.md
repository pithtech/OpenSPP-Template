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

OpenSPP and Odoo Foundations Training, Day 2, 1:00 to 5:00

Edwin Gonzales, OpenSPP

---

## By five you can

1. Place any `dswd_4ps_*` module on the map: its layer and its instance.
2. Given a 4Ps event, name the module that handles it and the `spp_*` module it extends.
3. Given a ticket, name the module and the part to open first.
4. Recognise the production traps and say why "simplifying" them is dangerous.
5. Find any module in the catalogue and read its card.

A discussion of modules, not a tutorial. The screens are the NL training team's.

---

## How to read a card

| Part                      | Says                                                        |
| ------------------------- | ----------------------------------------------------------- |
| Table                     | 4Ps process, instance, depends on, used by, size            |
| Key models                | **new table** (`_name`) or **extends** (`_inherit`)         |
| The strip                 | the twelve parts of a module from this morning; ■ = notable |
| Important points          | what changes how you work on it                             |
| A ticket usually lands in | files, each with a symptom                                  |
| Code moment               | the file we open now                                        |

The strip: Manifest 3.6 · Models 3.7/4.6 · Fields 3.8 · Views 3.9/4.7-4.8 · Wizards 3.10 · Security 3.11-3.12/4.9 ·
Tests 3.13/4.10 · ORM 3.15 · Jobs 3.17 · Reports 3.18 · Vocabularies 4.4 · Migrations 4.13

---

## Your category cards

**M** model · **V** view · **D** data or vocabulary · **S** security · **W** wizard · **J** job · **A** API · **T** test

I read a symptom. Your pair holds up the card for the file you would **open first**.

Warm-up: "The list of reasons for a grantee change is missing 'deceased'."

---

## The map: 66 modules, 26 cards

| Question       | Modules                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| Where          | `area`                                                                           |
| Who            | `registry`                                                                       |
| Who may        | `roles`, `approval_multi_group`, `approval_flow_data`                            |
| When           | `period`                                                                         |
| Change         | `change_request`, `supporting_docs_data`, `field_limit`                          |
| Verify         | `compliance`, `fds_operations`                                                   |
| Pay            | `payroll`, `catchup_payroll`, `retro_payroll`                                    |
| Assess, manage | `swdi`, `cms`, `swdi_cms`                                                        |
| Connect        | `api` and its route modules, portal APIs, `integration`, `newgrs`, `ods`, `auth` |

---

## Two instances, or one (card 1)

- **Instance 1**, registry and operations: `dswd_4ps_instance1`, with `bridge_server`.
- **Instance 2**, casework: `dswd_4ps_instance2`, with `bridge_client`: SWDI, CMS, the casework portal API.
- **Single**: `dswd_4ps_starter` installs both sides on one database, no bridge.
- Manifest `excludes` enforce the split: 26 modules exclude `bridge_client`, 8 exclude `bridge_server`.

Code moment: `dswd_4ps_instance1/__manifest__.py`. A manifest is the map of a deployment (3.6).

---

## Foundation: area (card 2)

- PSGC regions to barangays in `spp.area`; about 42,000 barangays queued as jobs at install.
- The install hook runs once: every later data fix is a migration (10 so far).
- Fail-closed: no center areas, no areas.
- `area_scope_ids`: 15 to 20 s per dashboard tile at 7.4 million households, 99 ms after. Do not simplify it.

---

<!-- _class: excerpt -->

## Area: a fail-closed record rule (3.12)

`dswd_4ps_area/security/area_record_rules.xml`, lines 41 to 52 (domain wrapped)

```xml
    <record id="rule_spp_area_center_area_filter" model="ir.rule">
        <field name="name">Areas: visible only within user's center areas</field>
        <field name="model_id" ref="spp_area.model_spp_area" />
        <field
            name="domain_force"
        >[] if user.sees_all_areas
           else (['|', ('id', 'child_of', user.center_area_ids.ids),
                       ('id', 'parent_of', user.center_area_ids.ids)]
                 if user.center_area_ids
                 else [('id', '=', False)])</field>
        <field name="global" eval="True" />
        <field name="perm_read" eval="True" />
        <field name="perm_write" eval="False" />
        <field name="perm_create" eval="False" />
        <field name="perm_unlink" eval="False" />
    </record>
```

---

## Foundation: registry (card 3)

- Extends `res.partner`: `listahanan_id`, `client_status_id`, `grantee_id`, `member_id_4ps`, ...
- 27 vocabularies: 32 client statuses in 9 categories, 57 set groups, 394 IP groups.
- Writes go through `_4ps_write_hook`, wired into the audit decorator by `_register_hook`.
- Three field-name styles: none, `x_4ps_`, `dswd_export_`. Search all before adding a field.
- Status 3 is a permanent exit: only a server-side path can move a household out.

---

<!-- _class: excerpt -->

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

## Foundation: roles (card 4)

- 54 groups and 48 roles: POO, RPMO and NPMO umbrella groups are the approval tiers.
- Local roles take their areas from the identity provider; RITO may lock them.
- Every group, role and rule file is `noupdate`: 20 migrations so far.

`dswd_4ps_roles/security/groups.xml`, lines 103 to 110

```xml
    <record id="group_4ps_poo_mswdo" model="res.groups">
        <field name="name">4Ps POO: MSWDO</field>
        <field name="comment">Municipal Social Welfare and Development Officer at provincial level.</field>
        <field name="implied_ids" eval="[
            Command.link(ref('group_4ps_poo')),
            Command.link(ref('spp_registry.group_registry_officer')),
        ]"/>
    </record>
```

---

## Approvals (cards 5 and 6)

- `approval_multi_group`: several groups per tier, any of them may approve. It replaces two upstream constraints
  **without `super()`**.
- `approval_flow_data`: 21 definitions, 19 linked to 6 change-request types, chosen by CEL on the status transition.
- No match: the request approves on submit. Change Address has no linked definition.

---

<!-- _class: excerpt -->

## Approval flow data: 24 to 3, two tiers

`dswd_4ps_approval_flow_data/data/approval_defs_update_hh_info.xml`, lines 81 to 91 (condition wrapped)

```xml
    <record id="approval_def_hh_info_poo_rpmo" model="spp.approval.definition">
        <field name="name">Family - Update Family Info - CS (24 → 3)</field>
        <field name="model_id" ref="spp_change_request_v2.model_spp_change_request" />
        <field name="approval_type">group</field>
        <field name="approval_group_ids" eval="[Command.link(ref('dswd_4ps_roles.group_4ps_swo_iii'))]" />
        <field name="sequence">10</field>
        <field name="use_cel_condition" eval="True" />
        <field name="cel_condition">record.selected_field_name == "client_status_id"
            and old_value.code == "24" and new_value.code == "3"</field>
        <field name="sla_days">10</field>
        <field name="is_require_comment" eval="True" />
    </record>
```

---

## Foundation: period (card 7)

- One `spp.compliance.period` per month; the Philippine working-day calendar.
- Fail-loud: a year not Seeded raises an error. Each December, an administrator seeds next year.
- Dates only, never datetimes.

`dswd_4ps_period/models/holiday_year.py`, lines 34 to 44

```python
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("seeded", "Seeded"),
        ],
        string="Status",
        required=True,
        default="draft",
        help="Deadlines are only computed across years marked Seeded. A Draft "
        "year is treated as unmaintained and refused.",
    )
```

---

<!-- _class: lead -->

# Checkpoint 1

Stand up. Three symptoms. Category card, then the module.

---

## Change requests: the upstream shape

| Part           | Is                                                |
| -------------- | ------------------------------------------------- |
| Type           | a data record: `spp.change.request.type`          |
| Detail model   | the proposed values, one model per type           |
| Apply strategy | validate, preview, apply                          |
| Approval       | `spp.approval.mixin`, multi-tier, routed by rules |

4Ps adds 20 types (22 type files) and rules. It does not change this shape.

---

<!-- _class: excerpt -->

## Card 8: a type is a data record

`dswd_4ps_change_request/data/cr_type_change_address.xml`, lines 13 to 23

```xml
    <record id="cr_type_change_address" model="spp.change.request.type">
        <field name="name">Change Address</field>
        <field name="code">change_address</field>
        <field name="description">Change the geographic area and address for a household</field>
        <field name="target_type">group</field>
        <field name="detail_model">spp.cr.detail.change_address</field>
        <field name="detail_form_view_id" ref="dswd_4ps_change_request.spp_cr_detail_change_address_form" />
        <field name="apply_strategy">field_mapping</field>
        <field name="auto_apply_on_approve">True</field>
        <field name="icon">fa-map-marker</field>
        <field name="sequence">50</field>
```

9 of the 20 new types are pure field mappings; 11 have a Python apply model.

---

## Change requests: what to know (card 8)

- Batching under a ticket number; a `cancelled` state added to the approval mixin itself.
- Derived requests: a newborn's Add Member creates Update Pregnancy and Update Member Additional Information requests.
- Access is checked in code (`models/cr_parent_access.py`), not by a record rule. Read the docstring.
- 14 context keys of its own, 11 of them skip or override a check. Never pass one to make a test green.

---

## Documents and limits (cards 9 and 10)

- `supporting_docs_data`: which documents each type needs. Add Member needs any one of seven.
- `field_limit`: how often a field may change, enforced in a `write` override.

`dswd_4ps_supporting_docs_data/data/cr_type_add_member_4ps.xml`, lines 13 to 17

```xml
<odoo noupdate="1">

    <record id="dswd_4ps_change_request.cr_type_add_member_4ps" model="spp.change.request.type">
        <field name="document_validation_mode">required</field>
        <field name="trigger_api_paths">addMembers[]</field>
```

---

<!-- _class: lead -->

# Break

Back at 3:05

---

## Compliance (card 11)

- Health, school and deworming arrive as `spp.event.data` through `/cv` (router in `dswd_4ps_api_compliance`).
- Reconcile later: the event job writes one row and marks the household; a daily reconcile finishes it.
- Per-household advisory locks. Status rows are a cache rebuilt from events.
- The school threshold is the constant 85 in `compliance_pipeline.py`.

---

<!-- _class: excerpt -->

## Compliance: an event hands its work to a job (3.17)

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

## FDS operations (card 12)

- Session library, parent groups (`pg_max_members`, default 30), plans with approval, attendance, the FDSAR.
- Equivalency creates a synthetic session, so the compliance pipeline needs no special case.

`dswd_4ps_fds_operations/models/fds_equivalency.py`, lines 439 to 446

```python
        session_vals = {
            "name": _("Equivalency: %(ref)s", ref=self.name),
            "session_type_id": fds_type.id,
            "date": self.date_completed,
            "facilitator_id": self.env.user.id,
            "session_topic_id": self.substitute_session_id.id or False,
            "session_subtype_id": special_fds_code.id if special_fds_code else False,
        }
```

---

## Payroll: what not to break (card 13)

- The run is a state machine. Once credit instructions exist, cancel and rewind are refused.
- The snapshot, which the code calls NAPA, is sealed; every later step reads it.
- Grant rates are never deleted. Five job channels; about 110 raw SQL calls.

`dswd_4ps_payroll/models/payroll_cycle_run.py`, lines 147 to 152

```python
# States from Step 8b onward — Credit Instructions is the point of no return.
# Cancel is disabled from these states.
POINT_OF_NO_RETURN_STATES = frozenset({"instructions_generated", "lbp_uploaded", "done"})

# Terminal states: run is closed, no further action allowed.
TERMINAL_STATES = frozenset({"rejected", "cancelled", "done"})
```

---

## Catch-up and retro (cards 14 and 15)

- Catch-up pays households a regular cycle left out: the same state-machine pattern, its own point of no return.
- Retro keeps overpayment and underpayment ledgers and reuses the regular run.

`dswd_4ps_retro_payroll/models/overpayment.py`, lines 10 to 19

```python
Recovery is two-phase so it survives the payroll cycle's reject-and-rewind:

    _compute_proposed_recovery(partner, run, gross)   # PROPOSED line(s)
        → cycle reaches its point of no return (Step 8b)
    _commit_recovery_for_run(run)                     # PROPOSED → APPLIED
        → balance drops only now
    _reverse_recovery_for_run(run)                    # on reject/rewind/cancel
        → PROPOSED/APPLIED → REVERSED, balance restored
    _reverse_recovery_for_run(run, partner_ids)       # retro done, credit rejected (#2914)
        → those households' lines only
```

---

<!-- _class: lead -->

# Checkpoint 2

Stand up. Three symptoms.

---

## Casework (cards 16 and 17)

- `swdi`: the yearly well-being assessment. The level comes from the total score (thresholds 1.83 and 2.83).
- `cms`: Kilos-Unlad case management on `spp_case_base`; 117 record rules for six groups, scoped by the user's areas.

`dswd_4ps_swdi/models/assessment.py`, lines 1230 to 1241

```python
        classification is total-score-range-only; the earlier ES/SA dimensional
        gates were dropped. ES and SA are retained as reported sub-scores, not
        as gates. Mirrors the mobile engine (swdi-mobile #280/#281):
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

## Assessments become cases (card 18)

- Seven triggers, each a data record. Approving an assessment queues an event; a job creates the case.
- Retries after 5 minutes, 15 minutes, 1 hour. A failed event stays as a row in state `failed`, with a Retry action.

`dswd_4ps_swdi_cms/models/cms_trigger_config.py`, lines 41 to 50

```python
    trigger_type = fields.Char(
        string="Trigger Type",
        required=True,
        help=("One of: PRIORITY_CASE, GRADUATION, FRVA_HIGH_RISK, CHILD_PROTECTION, MISBEHAVIOR, WAIVE_EXIT."),
    )

    is_active = fields.Boolean(
        string="Active",
        default=True,
    )
```

---

## The bridge (card 19)

- The registry instance is the master. Casework looks households up and imports them synchronously (5 s timeout).
- Case events flow back through jobs.
- `excludes` decide which side a module can live on.

`dswd_4ps_bridge_client/__manifest__.py`, lines 37 to 45

```python
    "excludes": ["dswd_4ps_bridge_server"],
    "depends": [
        "dswd_4ps_cms",
        "dswd_4ps_swdi_cms",
        "dswd_4ps_bridge_shared",
        # The cross-instance user sync writes oauth_uid / oauth_provider_id and
        # overrides the _post_oauth_login hook — both from dswd_4ps_auth (the CMS
        # split instance authenticates against Keycloak via this module).
        "dswd_4ps_auth",
```

---

<!-- _class: excerpt -->

## The API: the caller's rights, an identifier, a service (card 20)

`dswd_4ps_api/routers/household.py`, lines 96 to 107

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

Record rules apply while `dswd_4ps_api.enforce_rbac` is on (seeded on).

---

## Integration in one line each (cards 21 to 26)

| Card | Module            | In one line                                             |
| ---- | ----------------- | ------------------------------------------------------- |
| 21   | the route modules | a twelve-line `_inherit` and `super()` adds the routers |
| 22   | the portal APIs   | one four-line pattern opens every endpoint              |
| 23   | `integration`     | an outbound event log the portal polls                  |
| 24   | `newgrs`          | three touchpoints, three flags                          |
| 25   | `ods`             | a read-only client for the old ODS                      |
| 26   | `auth`            | a Keycloak identity becomes a user with areas           |

---

## Ticket triage

In pairs. Eight training scenarios, not real incidents.

For each: the **module**, the **category card**, the **first file**. Use your catalogue.

Twelve minutes, then report-back.

---

## How to approach a 4Ps ticket

1. Read the symptom in the user's words.
2. Find the module on the map.
3. Read its card: which boxes are shaded?
4. Open the first file.
5. Before changing code: `noupdate` data, context flags, jobs.
6. Write the failing test first.

---

## Not today

The modules on no card are in the catalogue index: registry tools (`registry_import`, `export`, `ecr`, `hazard`,
`account_creation`), operations (`theme`, `attachment_hardening`, `post_sql_repair`, `pg_partition`), dashboards
(`swdi_dashboard`, `cms_nas`) and 17 sample-data, demo and test modules.

They are for the post-training sessions.

Keep the catalogue.
