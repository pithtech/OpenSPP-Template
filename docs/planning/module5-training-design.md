# Module 5 Training Design: The DSWD 4Ps Modules, Discussed

> **Status**: proposal for Edwin's review (2026-11-08), revised with Edwin's answers to the first six decisions (section
> 10). Participants already have access to the production repository, so this design and the Module 5 materials live
> in this repository like Modules 3 and 4. Nothing goes into the participant guide until Edwin approves.
> **Sources**: Edwin's brief; an instructional-design review; three read-only surveys of the production repository
> (`dswd-4ps-dp-openspp-v2-module`, commit `ad98dac9`, 2026-11-06): foundation; change requests, compliance and FDS;
> payroll, casework and integration. This design names modules, models, fields and files; the session shows code from
> the production checkout on the trainer's screen.
> **Slot**: Day 2, 1:00 to 5:00 pm, after Modules 3 and 4. About 87 participants. No user-interface demonstration:
> the NL training team covers the screens. The trainer shows code in an editor only.

---

## 1. The strategy

1. **A discussion of modules, not a tutorial of the system.** For each module: what it is for, which 4Ps process it
   serves, and the important points about its components. The question every block answers: "if a ticket lands here,
   which file would I open?" Nothing is clicked in the running system; the screen shows the production code in an
   editor, at the file each point is about.
2. **Read every module through Modules 3 and 4.** The morning taught the parts of a module (manifest, models, fields,
   views, security, tests, ORM, `_inherit`, inherited views, vocabularies, wizards, jobs, migrations). The afternoon
   uses exactly those words. A fixed strip of those categories appears on every module card and in the corner of
   every slide.
3. **Organised by the 4Ps business process, not alphabetically.** Where they are (area), who they are (registry), who
   may see and approve (roles, approvals), when (period); then how records change (change requests), how compliance is
   verified (CVS, FDS), how grants are paid (payroll), how households are assessed and managed (SWDI, CMS), and how
   other systems connect (APIs).
4. **Three tiers of depth.** Deep for what support work touches most (foundation, change requests). Medium for
   compliance, FDS and casework. Tour for payroll (the riskiest code) and integration.
5. **About 25 of the 66 modules get a card.** The rest are named on a "not today" list for the post-training
   sessions. About a third of the 66 are sample data, demo seeders, bundles and test-only modules.

## 2. Learning objectives

By 5:00 a participant can:

1. Place any `dswd_4ps_*` module on the map: its layer (foundation, capabilities, integration, extensions) and its
   instance (instance 1: registry, change requests, compliance, payroll, FDS, APIs, bridge server; instance 2: SWDI,
   CMS, casework portal API, bridge client).
2. Given a 4Ps business event (a grantee changes, a school attendance form arrives, a payroll run, an SWDI
   assessment), name the module that handles it and the upstream `spp_*` module it extends.
3. Given a ticket, name the module and the component to open first, using the Module 3 and 4 categories.
4. Recognise the production traps (context skip flags, `x_4ps_` fields, raw SQL in payroll and compliance, `noupdate`
   data and install hooks, system parameters, approval state) and say why "simplifying" them is dangerous.
5. Find a module not discussed today in the module catalogue and read its card.

## 3. The module card

One A5 card per module, the same layout every time; the cards are bound into a catalogue participants keep.

**Front**: purpose in one sentence; the 4Ps process (with its section in `training/4ps-program-reference.md`);
instance 1, 2 or both; depends on and depended on by; size (non-test Python lines, tests); three to five key models,
each badged **new table** (`_name`) or **extends** (`_inherit`).

**Back**: the Module 3/4 strip; "important points" (three to five); "a ticket usually lands in" (files and an example
symptom); the code moment (one file to open on screen, see below).

**The strip**, twelve boxes in a fixed order, each labelled with its guide section; shaded where the module uses the
category in a way worth knowing, with one word in it:

```
Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 |
Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13
```

Participants learn to read a module as "which boxes are shaded", which is the triage skill itself.

**The code moment.** Each card names one production file the trainer opens in the editor (VS Code, the production
checkout at a fixed commit, 20pt font). It shows one Module 3 or 4 concept as it looks in 4Ps code: a manifest's
`depends`, a model's `_inherit`, a vocabulary data file, a record rule, a migration. One to three minutes, read from
the top of the file; method bodies only where the point is in them. It replaces a user-interface demonstration and
needs no running stack.

## 4. Run of show

| Time | Block | Tier | Minutes |
| --- | --- | --- | --- |
| 1:00 | Opener: objectives, how to read a card, warm-up ticket with category cards | | 10 |
| 1:10 | The map: 66 modules on the poster, layers, the two-instance split, bundles (`starter`, `instance1`, `instance2`), "about 25 matter today" | | 15 |
| 1:25 | Foundation: registry (14), area (8), roles (10), approvals (4), period (4) | Deep | 40 |
| 2:05 | Checkpoint 1: three quick tickets, standing vote | | 5 |
| 2:10 | Change requests: upstream architecture, 4Ps types, approvals, documents, limits, batching and cancellation, access mixin, code moments | Deep | 40 |
| 2:50 | Break | | 15 |
| 3:05 | Compliance with period (18) and FDS operations (12) | Medium | 30 |
| 3:35 | Payroll family: payroll (12), catch-up (3), retro (5) | Tour | 20 |
| 3:55 | Checkpoint 2 | | 5 |
| 4:00 | Casework: SWDI (6), CMS (7), the bridge and `swdi_cms` (7) | Medium | 20 |
| 4:20 | Integration: API authentication and scopes, split API modules, portal APIs, outbound events, NEWGRS, ODS | Tour | 12 |
| 4:32 | Paper ticket triage: eight tickets in pairs, report-back | | 18 |
| 4:50 | Closing: how to approach a ticket, the "not today" list, the catalogue | | 7 |
| 4:57 | Buffer | | 3 |

**Drop order if late**: integration to 5 minutes (poster only); checkpoint 2; payroll to 12 minutes; casework to 15
minutes. **Never dropped**: the map, foundation, change requests, the triage and the closing.

**Engagement without hands-on.** Before each card's back is revealed, a one-line symptom is read and rows hold up a
coloured category card (M model, V view, D data or vocabulary, S security, W wizard, J job, A API, T test). Predict
questions in the morning style. Two standing checkpoints. Deep blocks before the break, while energy is highest. No
block longer than 40 minutes without a prompt. Pairs for the triage, technicians next to developers.

## 5. The modules and their talking points

### 5.1 Foundation (deep, 40 minutes)

The story for the class: *where they are (area), who they are (registry), who may see and approve (roles and
approvals), when (period).*

**`dswd_4ps_registry`: the 4Ps household and member record** (about 9,900 lines; about 630 tests; used by about 30
modules).
- Extends `res.partner` (household: `listahanan_id`, `client_status_id`, `set_group_id`, `grantee_id`, stored computed
  `client_status_category_id`, `is_delisted`; member: `member_id_4ps`, `member_status_id`, `pregnancy_status_id`,
  stored computed `gestation_week`), `spp.group.membership`, `spp.registry.relationship`, `res.partner.bank`. New:
  grantee and head-of-household change histories, achievements, facility registries, grade-level and payroll-account
  configuration.
- Strip: vocabularies (22 namespaces: 32 client statuses in 9 categories, 49 set groups, about 390 IP groups), views
  (about 12 inherited upstream views, custom OWL household and member search screens), security (3 groups, no record
  rules here), wizards (reinstate, bulk status update), jobs (daily pregnancy, monthly aging delist), overrides,
  install hook, migrations (30+).
- Important points: the client-status hierarchy (a status's parent is its category; previous status stamped by raw SQL
  to avoid recursion); the permanent-exit write lock (only an approved change request or CMS can un-exit); grantee
  rules (Capable Grantee role, reason required, history row); the aging-delist cron (slow at scale); search
  performance at 50 million partners.
- Tickets land in `models/res_partner.py`, `models/group_membership.py`, `data/vocabulary_*.xml`, the search JS.
- Code moment: `data/vocabulary_client_status.xml` (a status's parent is its category; Module 4's vocabularies at
  scale), then the client-status fields in `models/res_partner.py`.
- **Bridge from Module 4**: the well-being level built that morning is one of these vocabulary fields.

**`dswd_4ps_area`: PSGC geography and area scoping** (about 2,800 lines; used by 22 modules).
- Loads the PSGC hierarchy (about 42,000 barangays, queued through the job worker at install) into `spp.area`; adds
  region, province and city on every registrant; maps each user's identity-provider region to areas.
- Important points: the install hook versus upgrade migrations (data fixes need migrations); rewriting a `noupdate`
  upstream rule in code; fail-closed scoping (no area, no data); a record-rule performance fix (from 15 seconds to
  99 milliseconds); removed fail-open branches.
- Tickets: "user cannot see a household" (center areas, region assignment), wrong parent area, stuck import jobs.
- Code moment: `security/area_record_rules.xml` (fail-closed domains, a follow-up to section 3.12), then `hooks.py`
  (the PSGC load queued through the job worker).

**`dswd_4ps_roles`: the 4Ps organisation chart as security** (about 2,650 lines; 54 groups, 48 roles, 5 record rules;
20 migration folders).
- POO, RPMO and NPMO umbrella groups are the approval tiers; sub-roles (MSWDO, SWO III, ProvLink, RGO, RCVO, and
  others), field positions (C/ML, RITO) and payroll units imply them. Local roles are area-scoped; global roles are not.
- Important points: the three-tier umbrella design; local roles synchronised from the user's region; the
  last-system-administrator safeguard; RITO as delegated user administrator; `noupdate` groups, so every change ships
  a migration.
- Tickets: "user lost access after a role change" (`models/res_users.py`), implied groups, rule rewrites in `hooks.py`.
- Code moment: `security/groups.xml` (umbrella groups and `implied_ids`, the same pattern as the Module 3 tiers), then
  the `migrations/` folder listing (20 versions: why `noupdate` groups need one per change).

**`dswd_4ps_approval_multi_group` and `dswd_4ps_approval_flow_data`.** An approval tier may name several groups (OR).
The flow data wires 25 approval definitions to the change-request types, routing by status transitions with CEL
conditions. Point to discuss: the module replaces upstream constraint methods without calling `super()`. Code moment:
`dswd_4ps_approval_flow_data/data/approval_defs_change_address.xml`.

**`dswd_4ps_period`.** Monthly compliance periods and the Philippine working-day calendar. Fail-loud: an unseeded
year raises an error. A yearly administrator duty in December. Dates only, never datetimes. Code moment:
`models/holiday_year.py`.

### 5.2 Change requests: the Beneficiary Update System (deep, 40 minutes)

**`dswd_4ps_change_request`** (about 13,700 lines; about 50 new models; about 826 tests; the largest module) with
`dswd_4ps_supporting_docs_data`, `dswd_4ps_approval_flow_data` and `dswd_4ps_field_limit`.

- First the upstream architecture (`spp_change_request_v2`): a **type** is a data record; a **detail model** holds the
  proposed values; an **apply strategy** validates, previews and applies; **approval** comes from
  `spp.approval.mixin`, multi-tier, with dynamic routing.
- How 4Ps plugs in: 22 type files (20 new 4Ps types, generic upstream types hidden rather than deleted); batching
  under a ticket number; a `cancelled` state added to the approval mixin itself; supporting documents per type,
  validated at submit and copied to the registrant's documents by a job; per-field update caps and per-type frequency
  limits.
- Important points: configuration over code (a new type is mostly XML); derived change requests (a newborn's Add
  Member creates two more that auto-apply only because no approval definition matches them); the identity-change
  guard; document pools differ per type (thin test data hides bugs); record access through a parent-access mixin
  instead of record rules, and why (a direct follow-up to the record-rules section of Module 3); about 15 context skip
  flags.
- Tickets: "add field X to type Y" (detail model, detail view, apply mapping, API payload, migration, tests); "new
  approver for transition A to B" (approval flow data, `noupdate`, needs a migration); "require document Z"
  (supporting documents data).
- Code moments, following one Change Address request through the files: `data/cr_type_change_address.xml` (the type
  as data), `models/cr_detail_change_address.py` (the detail model), the approval definition from section 5.1, then
  `models/cr_child_access.py` (access without record rules).

### 5.3 Compliance and FDS (medium, 30 minutes)

**`dswd_4ps_compliance`: the Compliance Verification System** (about 10,350 lines; about 693 tests).
- Monthly school attendance, health visits, FDS attendance and deworming become per-member and per-household status
  rows that payroll consumes. Forms arrive from the mobile app as `spp.event.data` events through the `/cv/*` API.
- Important points: reconcile later, not on every write (the event job writes one row and marks the household; a
  nightly cron rolls up), so status rows are a cache rebuilt from events; household rollup rules differ by pillar
  (health all members, education any); exemptions short-circuit everything (force majeure, client statuses 21 and
  28); per-household advisory locks; UI decisions driven by performance at 5.5 million households.
- Tickets: thresholds (system parameters or compliance rules), reasons (vocabulary), rule changes (the pipeline file
  plus tests that create events).
- Code moment: `models/event_data.py` (`_inherit` on `spp.event.data`, the job hand-off), then the top of
  `models/compliance_pipeline.py` (the reconcile, read for its structure only).

**`dswd_4ps_fds_operations`** (about 13,500 lines; about 1,115 tests).
- The session library, parent groups (at most 30 households, one Parent Leader), quarterly plans with approval,
  sessions and attendance, equivalency, outcome assessments and the FDS Accomplishment Report.
- Important points: `on_hold` added to an upstream selection; an equivalency creates a synthetic session so the
  compliance pipeline needs no special case; curriculum chosen by registration date and majority vote; about 15 global
  area rules.
- Code moment: `models/fds_equivalency.py` (the synthetic session).

### 5.4 Payroll (tour, 20 minutes)

**`dswd_4ps_payroll`** (about 50,000 lines; the riskiest code), with **`dswd_4ps_catchup_payroll`** and
**`dswd_4ps_retro_payroll`**.
- The cycle run as a state machine: enrolment, compliance reconciliation, entitlement computation (health, education
  in three tiers, First 1,000 Days, rice), the sealed snapshot, approvals, the output files to Land Bank, the result
  upload, fund allocation.
- Important points: the point of no return (once credit instructions exist, cancel and rewind are blocked; before it,
  a rewind archives instead of deleting); the snapshot, which the code calls NAPA, is immutable and everything
  downstream reads it; grant rates
  are append-only; five job channels with fan-out and a finalize barrier; heavy raw SQL; things not to change casually.
- Catch-up pays households deferred from a regular cycle; retro keeps overpayment and underpayment ledgers and reuses
  the regular run pipeline; both use explicit locks.
- Code moment: the state field of `models/payroll_cycle_run.py` (the run as a state machine and the point of no
  return), then `models/snapshot_beneficiary.py` (the write guard after the seal). Nothing is run.

### 5.5 Casework (medium, 20 minutes)

- **`dswd_4ps_swdi`**: the well-being assessment (indicators across economic sufficiency and social adequacy, levels 1
  to 3 by score), the risk assessment, assignment to C/MLs, two-person archiving, field-level return flags for the
  mobile app.
- **`dswd_4ps_cms`**: Kilos-Unlad case management on `spp.case`: case sources, approval workflows with timeouts, about
  25 crons, area rules in six tiers.
- **`dswd_4ps_swdi_cms`**: six triggers turn assessment outcomes into cases through the job worker, with retries and a
  dead-letter queue; approving an assessment never waits for case creation.
- **The bridge** (`bridge_shared`, `bridge_server`, `bridge_client`) and the two instances: the mode follows which
  modules are installed; the registry instance is the master; household imports are synchronous with a timeout;
  events flow back through jobs. Explained from the poster.
- Code moment: `dswd_4ps_swdi_cms/models/cms_trigger_config.py` (the six triggers as configuration).

### 5.6 Integration (tour, 12 minutes)

- **`dswd_4ps_api`** on `spp_api_v2`: routers, services, schemas, middleware; machine clients and identity-provider
  tokens; scopes per client; identifiers, never database ids; routers never use `sudo()`, so record rules apply to
  API traffic.
- The split API modules (change requests, compliance, FDS, field limits) register on the same application.
- Portal APIs for the beneficiary portal; `dswd_4ps_integration` as an outbound event log the portal polls;
  `dswd_4ps_newgrs` behind feature flags; `dswd_4ps_ods` as a read-only client; `dswd_4ps_auth` for single sign-on.
- Code moment: one router, `dswd_4ps_api/routers/household.py` (scopes, identifiers instead of database ids, no
  `sudo()`).

## 6. The paper ticket triage (18 minutes)

Eight tickets in pairs, each answered with: module, component category, the file to open first. The tickets are
fabricated training scenarios, labelled as such on the sheet, written as a user or field officer would report them,
and chosen so each category appears at least once. Before printing, each answer is checked against the production
code so the answer key names the real module and file. Edwin may swap in a real recent ticket the class will
recognise. Draft set:

1. "A provincial officer cannot see households in one barangay." (area / roles; security; center areas)
2. "Add the mother's maiden name to the Update Member Info request." (change request; model and view; detail model)
3. "Nobody can approve a client-status change from 24 to 3." (approval flow data; data; approval definition)
4. "A child's school attendance was submitted but the household is still non-compliant." (compliance; job; reconcile)
5. "A new required document for Add Member." (supporting docs data; data)
6. "The 2027 working-day deadline raises an error." (period; data; holiday year not seeded)
7. "A Level 1 assessment did not create a case." (swdi_cms; job; dead-letter queue)
8. "The beneficiary portal shows no payroll for a household." (payroll API; API; snapshot)

## 7. Not today: left for the post-training sessions

The post-training plan is made after the training (Edwin's decision). For now, the modules not discussed, grouped:

| Group | Modules |
| --- | --- |
| Registry tools | `registry_import`, `export`, `ecr`, `field_limit` (detail), `hazard`, `account_creation` |
| Payroll in depth | `payroll` (pipeline and files; the NAPA steps and roles: generate, endorse, file splits), `catchup_payroll`, `retro_payroll`, `pg_partition`, `retro_api`, `payroll_api` |
| Casework in depth | `swdi_dashboard`, `swdi_api`, `cms_nas`, `portal_api_casework` |
| Integration in depth | `api` family, `auth`, `integration`, `newgrs`, `ods`, bridge |
| Operations | `attachment_hardening`, `post_sql_repair`, `theme`, `security_tests`, `e2e` |
| Data and demo | all `*_sample_data`, `demo`, `cms_demo`, `cms_prototype_demo*`, `test_household` |

## 8. Materials

| Material | Priority |
| --- | --- |
| Deck, about 30 slides, strip in the corner, short code excerpts where a point needs one | Essential |
| Trainer runbook: cut-offs, drop order, the code moments (file, what to point at), prompts per card, answer keys | Essential |
| Module cards (about 25) and the bound catalogue with the full module index | Essential |
| Module map poster (A1): layers, the two instances, the bridge | Essential |
| Ticket-triage sheet and answer key | Essential |
| Category cards in eight colours per pair | Essential |
| Checkpoint item bank | Strongly recommended |

## 9. Risks

| Risk | Mitigation |
| --- | --- |
| Overload after a full morning | About 25 cards, strict tiers, one repeated format, the catalogue carries the rest |
| Production code on slides and cards | Participants already have access to the repository; excerpts are short and name their file; no real personal data anywhere |
| Code moments drift from production | Pin the production commit used for the cards and code moments; re-check every named file the week before |
| Editor on the trainer's laptop | No running stack needed; the deck carries the same excerpts if the laptop fails |
| Mixed skill | Category cards and pairs work for every level; technicians answer "which module", developers add "which file" |
| Afternoon energy | Deep blocks before the break, standing checkpoints, triage near the end |
| Cards drift from production | Generate the index from the production overview; check each card a week before; some production docs are stale (noted in section 11) |

## 10. Decisions

Taken by Edwin on 2026-11-08:

1. **Production code**: may be shown; participants already have access to the production repository.
2. **Where the material lives**: in this repository, like Modules 3 and 4 (`training/module5/`, this design in
   `docs/planning/`).
3. **Environment**: no user-interface demonstration (the NL training team covers the screens) and no production
   modules in the Docker image. The session reads code in an editor (the code moments in section 3). Adding the
   production modules to the template image would add install risk on 87 Windows laptops (the PSGC load alone queues
   about 42,000 barangays) and a stale copy of production, for no use in the session.
4. **Triage tickets**: fabricated training scenarios, labelled as such, each answer checked against the code (section
   6).
5. **Post-training sessions**: planned after the training; section 7 only lists the modules not discussed.
6. **NAPA**: named in one clause of the payroll tour, as the code's name for the sealed snapshot; its steps and roles
   are left for the post-training sessions.

Still open:

7. **Production commit**: which commit of the production repository the cards and code moments are pinned to (the
   surveys used `ad98dac9`, 2026-11-06).

## 11. Production documentation found stale during the surveys

To fix before the training or to mention when showing the docs:

- `docs/modules/dswd_4ps_change_request.md`: type and strategy counts are out of date; a post-delivery cron it
  mentions was not found in the module.
- `docs/modules/dswd_4ps_area.md`: says users without areas "see everything"; the code is fail-closed.
- `docs/modules/dswd_4ps_swdi.md`: contradicts itself on the level-3 rule; the code uses score thresholds.
- `docs/modules/dswd_4ps_api.md`: calls the compliance API split "planned"; the module exists.
- `docs/modules/overview.md`: says "all 50 modules"; there are 66.
- The approval-flow-data manifest description says 20 definitions; the data has 25.
