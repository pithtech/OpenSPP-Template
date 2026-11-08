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
5. **26 cards cover 38 of the 66 modules.** The rest are named on a "not today" list for the post-training
   sessions. About a third of the 66 are sample data, demo seeders, bundles and test-only modules.

## 2. Learning objectives

By 5:00 a participant can:

1. Place any `dswd_4ps_*` module on the map: its layer (foundation, capabilities, integration, extensions) and its
   instance (instance 1: change requests, compliance, payroll, FDS, period, approvals, bridge server; instance 2: SWDI,
   CMS, casework portal API, bridge client; both: area, registry, roles, the API and auth; `starter` puts everything on
   one database).
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
| 1:10 | The map: 66 modules on the poster, layers, the two-instance split, bundles (`starter`, `instance1`, `instance2`), "26 cards today" | | 15 |
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

The talking points now live on the 26 cards in `training/module5/module-cards.md`, and what to say per card is in
`training/module5/runbook.md`. Four agents wrote the cards against production commit `ad98dac9`, each checking every
count, path and excerpt in the code. The cards are the source of truth; where this section's earlier draft disagreed,
the code won. The complete list of corrections to the earlier survey:

**Foundation**

1. Line counts in the earlier draft included migrations. With the catalogue's method: registry about 6,500 (not
   9,900), area about 2,200 (not 2,800), roles about 1,200 (not 2,650).
2. Registry has 27 vocabularies (22 in `vocabulary_namespaces.xml`, 5 in `vocabulary_education.xml`), not 22; 57 set
   groups, not 49; 20 view records inheriting 15 upstream views, not "about 12"; three crons, not two (the daily
   post-delivery reset was missing).
3. The permanent-exit lock lets any superuser write pass; there is no change-request check. By default only status 3
   is locked; the system parameter `dswd_4ps_registry.permanent_exit_codes` can widen it.
4. The "bridge from Module 4" was wrong: the vocabulary `urn:dswd:4ps:well-being-level` exists, but no `res.partner`
   field uses it. The household level is the text field `swdi_level`; the vocabulary is read only by a payroll
   eligibility filter. The bridge is now made on the SWDI card (the level as production computes it).
5. Area is fail-closed for `spp.area` only. Households are filtered by upstream's `spp_area.rule_res_partner_area_filter`,
   whose branch for users with no center areas is still `[]`. The performance comment says 15 to 20 seconds per
   dashboard tile at 7.4 million households (not "15 seconds"). Fail-open branches were removed from other modules
   through the helper `_fail_open_area_rules.py`; `dswd_4ps_swdi` keeps its branch on purpose (#2342).
6. There are 21 approval definitions, not 25 (my earlier count was wrong): 19 are linked to 6 change-request types, 2
   ship dormant. Only 3 of the 6 types route by CEL. Change Address has no linked definition and approves on submit
   (commit 4b20a63c3, 2026-04-21), so the approval code moment uses definition 4 in `approval_defs_update_hh_info.xml`
   (24 to 3) instead.
7. `dswd_4ps_approval_flow_data` is `auto_install` and excludes `dswd_4ps_bridge_client`.
8. Area, registry, roles, the API and auth install on both instances; period and the approval modules only with
   instance 1 or starter. Objective 1 in section 2 is corrected.
9. Not in the earlier draft: new models with `spp.` names inside `dswd_` modules (`spp.compliance.period`, the facility
   registries); three field-name styles on `res.partner` (none, `x_4ps_`, `dswd_export_`); the registry write path runs
   through `_4ps_write_hook`, wired into `spp_audit`'s write decorator by `_register_hook`.

**Change requests, compliance and FDS**

10. Line counts without migrations: change requests about 12,000 (not 13,700), compliance about 8,400 (not 10,350), FDS
    about 12,000 (not 13,500).
11. "A new type is mostly XML": only 9 of the 20 new types are pure field mappings; 11 use a Python apply model.
12. A newborn's Add Member creates two kinds of derived request (Update Pregnancy per pregnant parent, Update Member
    Additional Information per parent whose solo-parent flag changes), not exactly two requests.
13. The module uses 14 context keys of its own, 11 of which skip or override a check (not "about 15").
14. The access mechanism is in `models/cr_parent_access.py`; `cr_child_access.py` only lists the child models. The code
    moment points to the first.
15. FDS attendance arrives through `/cv/fds-attendance` as `spp.session.attendance`, not as `spp.event.data`. The `/cv`
    router lives in `dswd_4ps_api_compliance`.
16. The per-pillar household rollup (health all members, education any) is in payroll's `cv_entitlement_manager.py`.
    In compliance, `_is_household_compliant` requires every active member to be compliant on every pillar that applies.
17. Exemptions: in compliance a hazard sets a row to `waived` (paid like compliant); the client status 21 and 28
    override is applied in payroll, not in the compliance pipeline.
18. The school threshold is the constant `SCHOOL_ATTENDANCE_THRESHOLD = 85.0`; the parameter
    `dswd_4ps.education_attendance_threshold` only feeds display fields, and `dswd_4ps.fds_attendance_threshold` is read
    nowhere outside tests.
19. The reconcile is a daily cron that fans out into range jobs (not "nightly", run time not checked).
20. FDS has 14 area rules, 13 global (not "about 15"); 30 households is the default of the per-group field
    `pg_max_members`, not a fixed cap; a group has one Parent Leader and may have one Assistant Parent Leader.

**Payroll and casework**

21. Grant rates are never deleted (archive instead), but an existing row's amount and dates can still be edited: "never
    deleted", not "append-only".
22. `dswd_4ps_swdi_cms` has seven triggers, not six (`frva_safety_high` was missing; its own manifest still says six).
23. There is no separate dead-letter queue: a failed event is a `dswd.swdi.cms.event` row in state `failed`. The module
    retries itself after 5 minutes, 15 minutes and 1 hour. The event is created inside the approval transaction; an
    inactive trigger means no event at all, only a log warning.
24. CMS has 117 record rules for six groups, each scoped by the user's own center areas; no tier has a fixed
    geographic level.
25. There are three install modes, not two: `dswd_4ps_starter` is single-instance with no bridge. `excludes` enforce the
    split: 26 modules exclude `dswd_4ps_bridge_client`, 8 exclude `dswd_4ps_bridge_server`. The bridge folders are
    `dswd_4ps_bridge_shared`, `dswd_4ps_bridge_server` and `dswd_4ps_bridge_client`.

**Integration**

26. "Routers never use `sudo()`, so record rules apply" holds while the system parameter `dswd_4ps_api.enforce_rbac` is
    on, as seeded. When it is off, `authenticated_env` returns a superuser environment (the `dependencies.py` docstring
    says the default is off; ADR-0004 says off returns the public user; the code and the ADR disagree). A few `sudo()`
    calls remain in services and the JWKS router, as the ADR allows.
27. The route modules are more than four: `api_change_request`, `api_compliance`, `api_fds`, `api_field_limit`,
    `retro_api` and `swdi_api` (card 21). The portal card covers `portal_api_base`, `portal_api`,
    `portal_api_casework` and `payroll_api` (card 22). `integration`, `newgrs` and `bridge_server` also add routers.
28. One endpoint takes a record id: `/payroll/Household/{listahanan_id}/payout/{snapshot_id}`, documented as an opaque
    reference and checked against the household.
29. NEWGRS has three touchpoints behind three flags (inbound status push, outbound profile notice, profile read), not
    one feature. Auth also provisions users on first sign-in, copies the Keycloak area claims, enforces SSO-only login
    and strips technical error details.

## 6. The paper ticket triage (18 minutes)

Eight tickets in pairs, each answered with: module, category card, the first file to open. The tickets are fabricated
training scenarios, labelled as such on the sheet. Each answer was checked against the code; the key in
`training/module5/triage-answers.md` gives the reasoning and every file a full fix touches. The eight cover five of the
eight categories (S, M, D, J, A); view, wizard and test are not first-file answers in production tickets of this kind.
Edwin may swap in a real recent ticket the class will recognise.

1. "A provincial officer cannot see households in one barangay." (area; S)
2. "Add the place of birth to the Update Member Personal Information request." (change request; M) Rewritten: the
   mother's maiden name is already captured by Update Member Additional Information, and Update Member Info was renamed.
3. "Nobody can approve a client-status change from 24 to 3." (approval flow data; D)
4. "A child's school attendance was submitted but the household is still non-compliant." (compliance; J)
5. "Add Member must now always include the Household Head Declaration, not just any one of the usual documents."
   (supporting docs data; D) Reworded: Add Member requires any one of seven documents, not a list.
6. "The 2027 working-day deadline raises an error." (period; D)
7. "A Level 1 assessment was approved but no case was created." (swdi_cms; J)
8. "The beneficiary portal shows no payroll for a household that was paid." (payroll API; A) The service reads
   `spp.payment`, not the snapshot.

## 7. Not today: left for the post-training sessions

The post-training plan is made after the training (Edwin's decision). 26 cards cover 38 modules; the other 28, in the
catalogue index:

| Group | Modules |
| --- | --- |
| Registry tools | `registry_import`, `export`, `ecr`, `hazard`, `account_creation` |
| Payroll in depth | `pg_partition`; the payroll pipeline and files (the NAPA steps and roles: generate, endorse, file splits) |
| Casework in depth | `swdi_dashboard`, `cms_nas` |
| Operations | `attachment_hardening`, `post_sql_repair`, `theme` |
| Sample data, demo and test-only (17) | `sample_data`, `demo`, `fds_sample_data`, `payroll_sample_data`, `retro_payroll_sample_data`, `swdi_sample_data`, `cms_sample_data`, `cms_demo`, `cms_prototype_demo`, `cms_prototype_demo_registry`, `cms_prototype_demo_shared`, `cssp_sample_data_cms`, `cssp_sample_data_registry`, `test_household`, `e2e`, `security_tests`, `cms_nas_direct_tests` |

## 8. Materials

Built in `training/module5/` (see its README):

| Material | File |
| --- | --- |
| Deck, 34 slides, excerpts copied from the cards | `slides.md` |
| Trainer runbook: cut-offs, drop order, code moments in tab order, prompts per card | `runbook.md` |
| 26 module cards and the index of all 66 modules | `module-cards.md` |
| Module map poster (A1) | `module-map.md` |
| Ticket-triage sheet and answer key | `triage-sheet.md`, `triage-answers.md` |
| Category cards in eight colours per pair | `category-cards.md` |
| Checkpoint bank | `checkpoint-bank.md` |

## 9. Risks

| Risk | Mitigation |
| --- | --- |
| Overload after a full morning | 26 cards, strict tiers, one repeated format, the catalogue carries the rest |
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

7. **Production commit**: the cards and code moments are pinned to `ad98dac9` (2026-11-06), still production's HEAD
   when the materials were built. Re-check the week before if production moves.

## 11. Production documentation found stale, and other observations

To fix before the training or to mention when showing the docs. Found while writing and checking the cards.

- `docs/modules/dswd_4ps_change_request.md`: type and strategy counts are out of date; the post-delivery cron it
  mentions lives in `dswd_4ps_registry`, not in the change-request module.
- `docs/modules/dswd_4ps_area.md`: says users without areas "see everything"; area search (`spp.area`) is fail-closed.
- `docs/modules/dswd_4ps_swdi.md`: contradicts itself on the level-3 rule; the code uses the total score (thresholds
  1.83 and 2.83).
- `docs/modules/dswd_4ps_api.md`: calls the compliance API split "planned"; the module exists.
- `docs/modules/overview.md`: says "all 50 modules"; there are 66.
- `dswd_4ps_approval_flow_data` manifest: says 20 definitions across 7 types; the data has 21 definitions, 19 linked to
  6 types.
- `dswd_4ps_swdi_cms` manifest and the `trigger_type` help text: say six triggers; there are seven.
- `dswd_4ps_payroll` manifest: says the snapshot table is partitioned; partitioning comes from `dswd_4ps_pg_partition`.
- `dswd_4ps_payroll` cancel message: suggests Reject and Rewind, but rewind is also refused past the point of no return.
- `dswd_4ps_catchup_payroll` manifest: still calls the module a foundation with empty stub actions; the step actions
  are implemented. The drift-detection cron's docstring is stale too.
- `dswd_4ps_bridge_server` manifest: lists 3 endpoints; the router has 5.
- `dswd_4ps_ods` manifest: says 14 endpoints and lists 10; the client has 15 fetch methods.
- ADR-0004: its context counts four API modules and about 24 endpoints; there are many more. Its description of
  `enforce_rbac` off disagrees with the code (item 26 in section 5).
- `dswd_4ps_integration/models/outbound_event.py`: the docstring names `/events/since`; the endpoints are
  `GET /cssp/events` and `POST /cssp/events/ack`.
- `dswd_4ps_change_request/data/cr_type_change_address.xml`: a comment says 3 mappings; the file defines 2.
- `dswd_4ps_supporting_docs_data/tests/test_trigger_paths_match_submission.py::test_member_field_aliases_are_covered`
  always skips: it looks for `MEMBER_API_ALIAS`, which no longer exists.
- `dswd_4ps_compliance` and `dswd_4ps_fds_operations` set `application: True`.
- Observation: `dswd_4ps_integration` is only in instance 1 while CMS, one of its producers, runs on instance 2, so on
  a split deployment CMS notices are not emitted (the code guards on the model being present).
- In this repository, `training/4ps-program-reference.md` section 8 mapped periods to `spp.cycle` and program enrolment
  to `dswd_4ps_starter`; corrected in the same change as these materials.
