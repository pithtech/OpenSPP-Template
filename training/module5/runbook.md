# Module 5 Runbook: The DSWD 4Ps Modules, Discussed

Day 2, 1:00 to 5:00. Trainer copy. Objectives and rationale are in
[docs/planning/module5-training-design.md](../../docs/planning/module5-training-design.md); this page is what to do and
say. Card numbers refer to [module-cards.md](module-cards.md).

**This is a discussion of modules.** Nothing is clicked in a running system. The screen shows the deck or the production
code in an editor, at the file a point is about.

**Cut-offs are hard.** Drop order if late: integration to 5 minutes (poster and card 20 only); checkpoint 2; payroll to
12 minutes (card 13 only); casework to 15 minutes (cards 16 and 18). **Never dropped**: the map, foundation, change
requests, the triage and the closing.

## Before the session

- Editor: VS Code with the production repository `dswd-4ps-dp-openspp-v2-module` checked out at commit `ad98dac9`
  (`git checkout ad98dac9`, detached; the card line numbers match that commit). Font 20pt, light theme, minimap and
  sidebar off. No running stack is needed.
- Open the code-moment files in tabs, in card order (the list at the end of this page). Test each one opens at the right
  line: Ctrl+P, the path, `:` and the line.
- The deck rendered to PDF on the laptop as the projector fallback; the deck carries the same excerpts.
- Printed: the catalogue (A4, one card per sheet, front and back, bound; one per participant), the A1 map poster on the
  wall, one set of eight category cards per pair, the triage sheet (one per pair), the triage answer key and the
  checkpoint bank for yourself. Test-print card 8, the longest, before ordering the catalogue; if time or budget is
  short, print one catalogue per pair and share the PDF.
- Seat technicians next to developers before 1:00; pairs keep the same partner all afternoon.

## Block 1, 1:00 to 1:05: opener (slides 1 to 4)

1. The five objectives, one breath each. "This morning you learned the parts of a module. This afternoon you read the
   real ones. By five you can take a 4Ps ticket and say which module, which part, which file."
2. How to read a card (slide): hold up card 3, registry. Table, key models, the strip, important points, "a ticket
   usually lands in", the code moment. "The strip is the morning: twelve boxes, each with its guide section. A shaded
   box is a part this module uses in a way you must know."
3. The category cards: "M, V, D, S, W, J, A, T. I read a symptom; your pair holds up the card for the file you would
   open first, not the file the fix ends in."
4. Warm-up: "A user says: the list of reasons for a grantee change needs 'working abroad'." Count to three. Answer: D, a
   vocabulary data file, `dswd_4ps_registry/data/vocabulary_grantee_change_reasons.xml`. "Module 4, step 1: the
   vocabulary file. And this file is `noupdate`: on production, a new code also needs a migration; the primer at 1:15
   says what that means."

## Block 2, 1:05 to 1:15: the map (card 1; slides 5 and 6)

1. Map slide on screen, poster on the wall. "66 modules with a manifest. 26 cards cover 38 of them. About a quarter of
   the 66 (17 modules) are sample data, demo seeders and tests. You can ignore those on a ticket."
2. Read the poster top to bottom as the 4Ps process: where (area), who (registry), who may (roles, approvals), when
   (period); then change, verify, pay, assess, manage; then connect, which starts with the bridge (card 19). The Cards
   column sends participants from the slide to the printed card; under all of them sits OpenSPP.
3. Two instances: instance 1 is the registry and operations, instance 2 is casework; the bridge joins them; `starter`
   puts both on one database. **Code moment**: `dswd_4ps_instance1/__manifest__.py`, the `depends` list grouped by
   layer. "A manifest is the map of a deployment; section 3.6."
4. Predict: "Which modules install on both instances?" Area, registry, roles, the API and auth: the casework side
   depends on them (plus the bridge schemas, the portal API base, the theme and attachment hardening). Period and the
   approval modules: starter or instance 1 only.

## Block 2b, 1:15 to 1:25: primer (slides 7 to 11)

"Five things the production modules use on almost every card. This morning did not present them; each has a Reference
section in your guide. One sentence each now; the cards show them all afternoon." Two minutes per slide: the sentence,
the production example, the guide section. No questions until the end.

1. **Record rules** (guide 3.12): "An access row says which models a group may use; a record rule says which rows of a
   model a user may see." Example: `dswd_4ps_area` shows each user only the areas in or above their center areas, and
   none to a user without one (card 2).
2. **Jobs and scheduled actions** (3.17): "A job is work queued with `with_delay()` that runs later in the background; a
   scheduled action, or cron, runs on a clock." Example: a school attendance event queues a job on the `cv_events`
   channel, and a daily cron finishes the household (card 11).
3. **Migrations and `noupdate`** (4.13): "A `noupdate` data file loads once, at install; changing its records on a
   running database takes a migration." Example: every group, role and rule file in `dswd_4ps_roles` is `noupdate`, and
   the module has 20 migrations so far (card 4).
4. **Hooks** (5.10): "A hook is code Odoo calls at a fixed moment: `post_init_hook` once after install, `_register_hook`
   each time the server loads the module." Example: the `post_init_hook` of `dswd_4ps_area` loads the PSGC areas at
   install, and never again (card 2).
5. **Wizards** (3.10): "A wizard is a temporary model behind a dialog: the user fills in a small form, and its button
   does the work." Example: the payroll Reject + Rewind wizard offers no rewind once credit instructions exist (card
   13).

## Block 3, 1:25 to 2:05: foundation (deep, cards 2 to 7; slides 12 to 19)

The story for the board: _where they are, who they are, who may see and approve, when._

| Minutes | Card                   | Code moment (file, what to point at)                                                   | Category prompt (symptom) and answer                                    |
| ------- | ---------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 8       | 2 area                 | `security/area_record_rules.xml`: the fail-closed domain; `hooks.py`: the queued batch | "After install there are no barangays." J: the `psgc_load` jobs         |
| 14      | 3 registry             | `data/vocabulary_client_status.xml`: status 3 and its parent category                  | "A new set group is missing from the list." D: a vocabulary file        |
| 9       | 4 roles                | `security/groups.xml`: `implied_ids` to the umbrella; the `migrations/` listing        | "A SWO III cannot open the household form." S: `groups.xml`             |
| 3       | 5 approval multi-group | `models/approval_definition.py`: the override without `super()`                        |                                                                         |
| 4       | 6 approval flow data   | `data/approval_defs_update_hh_info.xml`: definition 4, 24 to 3, CEL and two tiers      | "Change Address is approved with no review." D: not linked, by design   |
| 2       | 7 period               | `models/holiday_year.py`: Draft and Seeded                                             | "The 2027 deadline raises an error." D: an administrator seeds the year |

Say, per card:

- **Area**: "The install hook runs once. Every later data fix is a migration: ten so far." Then "do not simplify
  `area_scope_ids` back to `child_of`: 15 to 20 seconds per dashboard tile at 7.4 million households, 99 ms after."
- **Registry**: three field-name styles (no prefix, `x_4ps_`, `dswd_export_`): "search all of them before adding a
  field." The write path goes through `_4ps_write_hook`, wired into the audit decorator: "a breakpoint in `write()` may
  never fire." The permanent-exit lock: a normal user's write cannot move a household out of status 3; a server-side
  path (an approved change request, CMS) can.
- **Roles**: every group, role and rule file is `noupdate`: "a role change is a migration, never only an XML edit." Keep
  the recursion context flags.
- **Approvals**: "an override without `super()`: if upstream adds a check, it does not run here." Then the flow data: 21
  definitions, 19 linked to 6 types; a transition no definition matches auto-approves, except on Reinstate Household,
  which keeps a catch-all.
- **Period**: fail-loud by design; the December duty: an administrator enters next year's holidays and marks the year
  Seeded.

## Block 4, 2:05 to 2:10: checkpoint 1 (slide 20)

Stand up. Three tickets from [checkpoint-bank.md](checkpoint-bank.md), set 1. Pairs hold up a category card, then name
the module aloud. Sit down when done.

## Block 5, 2:10 to 2:50: change requests (deep, cards 8 to 10; slides 21 to 24)

1. **The upstream architecture first** (8 min, slide): a type is a data record; a detail model holds the proposed
   values; an apply strategy validates, previews and applies; approval comes from `spp.approval.mixin`. "4Ps adds types
   and rules; it does not change this shape."
2. **Card 8, code moments** (15 min), one request through the files:
   - `data/cr_type_change_address.xml`: `detail_model`, `apply_strategy`, `noupdate="1"`, the field mappings. Predict
     first: "a new type: code or data?" Both: 9 of the 20 new types are pure field mappings, the other 11 have a Python
     apply model.
   - `models/cr_detail_change_address.py`: the detail model's `_inherit`.
   - Point out: Change Address has no linked approval definition, so it approves on submit (card 6). "The approval you
     saw just before the checkpoint is on Update Household Info."
   - `models/cr_parent_access.py`: the docstring says why access is checked in code, not by a record rule. "A follow-up
     to 3.12: a rule cannot say: whatever the header's rules allow you. So access follows the parent, in code." (Odoo
     evaluates rule domains as superuser, so a rule on the parent would skip the parent's own rules.)
3. **Important points** (7 min): batching under a ticket number; the `cancelled` state added to the approval mixin
   itself; derived requests (a newborn's Add Member creates Update Pregnancy and Update Member Additional Information
   requests); the context keys that skip checks (14, of which 11 skip or override): "never pass one to make a test
   green."
4. **Card 9, supporting documents** (4 min): code moment `data/cr_type_add_member_4ps.xml`: a data file that extends a
   record of another module. "Add Member needs any one of seven documents: a group with `min_required` 1."
5. **Card 10, field limits** (3 min): code moment `models/res_partner.py`, a `write` override and the context key that
   bypasses it.
6. **Category prompt** (3 min, on slide 24): "Add the place of birth to the Update Member Personal Information request."
   M, the detail model; then ask "and what else?" The view, the field mapping in the `noupdate` type data and its
   migration and version bump, the API schema and service, the supporting-documents trigger path, tests.

## Block 6, 2:50 to 3:05: break (slide 25)

## Block 7, 3:05 to 3:35: compliance and FDS (medium, cards 11 and 12; slides 26 to 28)

1. **Card 11** (18 min). Health, school and deworming arrive as `spp.event.data` events through `/cv` (the router lives
   in `dswd_4ps_api_compliance`); FDS attendance arrives as session attendance. Code moment: `models/event_data.py`:
   `_inherit = "spp.event.data"`, then `create` queuing the job with `with_delay` (section 3.17), the lock, the retry,
   the household flag. Then the top of `models/compliance_pipeline.py`, read for structure only.
2. Say: "Reconcile later, not on every write: the event job writes one row and marks the household; a daily reconcile
   finishes it. Status rows are a cache rebuilt from events." And: "the school threshold is the constant 85 in the
   pipeline; the system parameter of a similar name only feeds display fields." The per-pillar household rules for
   payment live in payroll's entitlement manager, not here.
3. Category prompt: "A child's attendance was submitted, the household is still non-compliant." J: the event job and the
   reconcile, before any code.
4. **Card 12** (12 min). Parent groups (`pg_max_members`, default 30), plans with approval, sessions, equivalency, the
   FDSAR. Code moment: `models/fds_equivalency.py`, `_create_credited_attendance`: "a synthetic session, so the
   compliance pipeline needs no special case."

## Block 8, 3:35 to 3:55: payroll (tour, cards 13 to 15; slides 29 and 30)

"Payroll is the riskiest code in the repository. Today you learn what not to touch, and why."

1. **Card 13** (12 min). Code moment: `models/payroll_cycle_run.py`, `STATE_SELECTION` and the frozensets under it, then
   `action_cancel`; then the `write()` guard in `models/snapshot_beneficiary.py`. Say: "About 50,000 lines. Once credit
   instructions exist, cancel and rewind are refused: the point of no return. The snapshot, which the code calls NAPA,
   is sealed and every later step reads it: a name corrected after the seal does not appear on that cycle's payroll
   list, by design. Grant rates are never deleted. Five job channels and about 110 raw SQL calls: read before you
   touch."
2. **Card 14** (3 min): catch-up, the same state-machine pattern with its own point of no return.
3. **Card 15** (5 min): retro, overpayment and underpayment ledgers, reusing the regular run; the frozen-after-create
   fields in `models/overpayment.py`.

## Block 9, 3:55 to 4:00: checkpoint 2 (slide 31)

Stand up. Set 2 from the checkpoint bank.

## Block 10, 4:00 to 4:20: casework (medium, cards 16 to 19; slides 32 to 34)

1. **Card 16, SWDI** (6 min). Code moment: `_classify_lowb` in `models/assessment.py` and the two thresholds in
   `constants/states.py`. "The well-being level from Module 4, as production computes it from the total score."
2. **Card 17, CMS** (5 min). Kilos-Unlad on upstream `spp_case_base`. Code moment: `security/ir_rule.xml`, the comment
   block and one rule: 117 rules for six groups, each scoped by the user's own center areas.
3. **Card 18, `swdi_cms`** (5 min). Seven triggers turn assessment results into cases through the job worker. Code
   moment: `data/trigger_config_data.xml`: "a trigger is a data record." A failed event is a row in state `failed`, with
   a Retry action; there is no separate queue. On the slide, the `trigger_type` help text lists six types; the data has
   seven. Ask: "which one do you trust?" The data; help text and manifests drift.
4. **Card 19, the bridge** (4 min, from the poster). The registry is the master; casework looks households up and
   imports them synchronously; events flow back through jobs. Code moment: `excludes` in the two bridge manifests.

## Block 11, 4:20 to 4:32: integration (tour, cards 20 to 26; slides 35 and 36)

1. **Card 20, the API** (6 min). Code moment: `routers/household.py`, `read_grantee_history`: `authenticated_env` (the
   caller's environment, so record rules apply while `dswd_4ps_api.enforce_rbac` is on, as seeded), the scope check, an
   identifier instead of a database id, the service call.
2. **Cards 21 to 26** (6 min, one sentence each, the slide's lines, which are the guide's): the route modules each add
   their routers with a short `_inherit` and `super()`, twelve lines of method (card 21); the portal APIs are what the
   beneficiary portal reads, and one four-line pattern opens every endpoint (card 22); `integration` is an outbound
   event log the portal polls (card 23); NEWGRS takes grievance status in and sends profile updates out, behind three
   flags (card 24); ODS is a read-only client for the old Pantawid ODS (card 25); auth is Keycloak sign-in, and a user
   gets their areas from the claims (card 26).

## Block 12, 4:32 to 4:50: ticket triage (slides 37 and 38)

1. Hand out [triage-sheet.md](triage-sheet.md), one per pair. "Training scenarios, not real incidents. Module, card,
   first file. Twelve minutes. Use your catalogue."
2. Walk the room. At 4:44, report-back from [triage-answers.md](triage-answers.md) on four tickets only: 1, 2, 4 and 6
   (four categories; ticket 6 has no card). One pair per ticket, then "who had something different?" Then the answers
   slide with all eight, and the three points at the top of the answer key.

## Block 13, 4:50 to 4:57: closing (slides 39 and 40)

1. How to approach a ticket (slide 39, guide 5.11's five steps): read the symptom in the user's words, and reproduce it;
   find the module on the map and open its card; read the strip and pick the first file; before changing code, check
   `noupdate` data, context keys, jobs and their state, system parameters; write a failing test that reproduces the
   ticket, then fix, then run the module's tests.
2. "Not today": the modules on no card, in the catalogue index. "They are for the post-training sessions."
3. "Keep the catalogue. Tomorrow is hands-on with the modules you built this morning."

## Block 14, 4:57 to 5:00: buffer

## If something fails

- Editor or laptop: the deck has every excerpt; run the code moments from the slides.
- Projector: the catalogue has every card and excerpt; run the session from paper.
- Running late: the drop order at the top. Never cut the triage: it is the only time participants do the skill.

## Code-moment files in tab order

All paths at production commit `ad98dac9`.

1. `dswd_4ps_instance1/__manifest__.py`
2. `dswd_4ps_area/security/area_record_rules.xml`, `dswd_4ps_area/hooks.py`
3. `dswd_4ps_registry/data/vocabulary_client_status.xml`, `dswd_4ps_registry/models/res_partner.py`
4. `dswd_4ps_roles/security/groups.xml`, `dswd_4ps_roles/migrations/`
5. `dswd_4ps_approval_multi_group/models/approval_definition.py`
6. `dswd_4ps_approval_flow_data/data/approval_defs_update_hh_info.xml`
7. `dswd_4ps_period/models/holiday_year.py`
8. `dswd_4ps_change_request/data/cr_type_change_address.xml`, `models/cr_detail_change_address.py`,
   `models/cr_parent_access.py`
9. `dswd_4ps_supporting_docs_data/data/cr_type_add_member_4ps.xml`
10. `dswd_4ps_field_limit/models/res_partner.py`
11. `dswd_4ps_compliance/models/event_data.py`, `models/compliance_pipeline.py`
12. `dswd_4ps_fds_operations/models/fds_equivalency.py`
13. `dswd_4ps_payroll/models/payroll_cycle_run.py`, `models/snapshot_beneficiary.py`
14. `dswd_4ps_catchup_payroll/models/catchup_cycle_run.py`
15. `dswd_4ps_retro_payroll/models/overpayment.py`
16. `dswd_4ps_swdi/models/assessment.py`, `constants/states.py`
17. `dswd_4ps_cms/security/ir_rule.xml`
18. `dswd_4ps_swdi_cms/models/cms_trigger_config.py`, `data/trigger_config_data.xml`
19. `dswd_4ps_bridge_client/__manifest__.py`, `dswd_4ps_bridge_server/__manifest__.py`
20. `dswd_4ps_api/routers/household.py`
21. `dswd_4ps_api_fds/models/fastapi_endpoint_registry.py`
22. `dswd_4ps_portal_api_casework/routers/portal_casework_router.py`
23. `dswd_4ps_integration/models/outbound_event.py`
24. `dswd_4ps_newgrs/models/change_request.py`
25. `dswd_4ps_ods/models/res_partner.py`
26. `dswd_4ps_auth/models/res_users.py`
