# Module 4 Training Design: Developing Custom Modules and Extending Odoo Models

> **Status**: proposal for Edwin's review (2026-11-08). Synthesised from
> [research-module4-first-module.md](research-module4-first-module.md), an instructional-design review and an Odoo
> trainer review (both run as independent agents on the same brief), plus facts verified in the repo.
> **Slot**: Day 2, 10:00 to 12:00, after Module 3 "Introduction to Odoo", before Module 5 (4 hours, DSWD-specific).
> **Audience**: about 87 DSWD IT staff of mixed skill (18 RITOs, 36 CMTs, 33 NPMO IT). Evaluation target: Tier-2/3
> troubleshooting, measured by pre-test, post-test and an observation checklist.

---

## 1. The strategy in five sentences

1. Module 4 is a **demo-led "read and predict" session**, not a typing session. One trainer, 87 people and a share of
   broken laptops make live participant coding the wrong tool; Module 6 on Day 3 is the hands-on slot.
2. Edwin builds **one small module live, `dswd_wellbeing`, in five steps of one or two files each**, from pre-made git
   tags, so any live failure is recoverable in one command and participants can jump to any step later.
3. Every step starts from a **4Ps requirement** (SWDI well-being level on a household) and lands on an **OpenSPP
   concept** (vocabulary, registrant, inherited form), so "Odoo" is never taught in the abstract.
4. **Four deliberate breakages** replace exercises as the participation mechanism. They work for every skill level, need
   no environment, and are exactly what the troubleshooting evaluation measures.
5. Everything complex (new models and menus, security groups, hooks, programs, compliance, change requests, the
   vocabulary-model extension) is **named and deferred to Module 5**, so beginners are not lost and experts know it is
   coming.

## 2. Learning objectives

By 12:00 a participant can:

| # | Objective | Post-test form |
| --- | --- | --- |
| 1 | Name the role of each file in a `dswd_*` module (manifest, data, model, view, security, test) and state that a file not listed in the manifest does not exist to Odoo. | Multiple choice |
| 2 | Given a 4Ps requirement, pick the right pattern: `_inherit` on the upstream model, a `dswd_` field, a Many2one to a vocabulary code; never a new model for an attribute, never a static Selection for a code list, never an edit under `vendor/openspp/`. | Multiple choice plus one sentence |
| 3 | Explain view inheritance (`inherit_id` plus one XPath on a named upstream anchor) and recognise the error when the anchor does not exist. | Short answer |
| 4 | Given a log excerpt (file missing from manifest, invalid vocabulary `domain`, bad XPath, failed assertion), say which step failed and which file to open. | Short answer, also the drill |
| 5 | Run the tests of a module and read the pass/fail summary. | Command plus one sentence |

## 3. Why `dswd_wellbeing`, and what it does and does not extend

Both reviews independently picked option A from the research doc over the alternatives:

- It is the only candidate that touches all six file roles in **under 60 lines total**; every file fits on one slide.
- The three SWDI levels (Survival, Subsistence, Self-Sufficient) are known to every RITO and CMT, and EO 120 (July
  2026) made the level the reason a household stays in the program, so the "why" takes thirty seconds.
- Option A' (a field on `spp.vocabulary.code` and inheriting the code form) teaches the same mechanics on a model the
  audience will never troubleshoot. It moves to Module 5 as the example of extending a capability model.
- Option B (Philippine ID types with regex) is data-only, weak for "extending models" as a demo, and ideal as the Day 3
  exercise because step 1 of A is its template.
- Option C (household status) invites "why not the real 32" arguments and hierarchy; afternoon material.

On Edwin's question "does it extend `spp_vocabulary`": the module extends `spp_vocabulary` **by data** (a new
vocabulary and codes, the way all 26 production vocabularies are shipped) and extends `spp_registry` **by model and
view** (a field on the household and its form). That pairing is the single most common shape of a `dswd_4ps_*` module,
which is why it is the right first example. The slide title should say "Extending OpenSPP: a vocabulary and a household
field", not "customising spp_vocabulary".

Decisions taken on the open questions from the research doc (override any of them):

| Question | Decision | Reason |
| --- | --- | --- |
| Module name | `dswd_wellbeing` | Short to type live; the naming rule allows it |
| Codes | `survival`, `subsistence`, `self_sufficient`; SWDI number in `definition` | Readable on a slide; the number keeps the PPIS link |
| Field placement | New group "4Ps" after `group_tags_section` on the household Profile page | One XPath; the group label makes the result obvious on screen |
| ACL file | Ship `security/ir.model.access.csv` header-only, listed in the manifest | Objective 1 needs the file to exist; one minute to explain "no new model, no rows" |
| Wrong-vocabulary code | `@api.constrains` on the field, written in step 5 with Claude Code, test first | A Many2one `domain` only filters the UI; the constraint is the honest guard and a clean TDD moment |

## 4. Run of show

Hard cut-off times are in the runbook. Drop order if late: block 8 (Claude Code), then breakage 4. Blocks 9 and 10 are
never dropped.

| Time | Block | Mode | Trainer | Participants |
| --- | --- | --- | --- | --- |
| 10:00 | 1. The end state | Demo | Open the finished module on a warm database: a household showing "Well-Being Level: Subsistence". One slide: SWDI levels, EO 120, where this lives in production (`dswd_4ps_registry`, 26 vocabulary files). | Watch |
| 10:05 | 2. Module anatomy | Paper | File tree slide, one sentence per file and the 4Ps requirement it serves; the three rules (never edit vendor, inherit, list it in the manifest). | Fill the anatomy map on the handout |
| 10:15 | 3. Step 0 and 1: manifest, data | Demo, predict | Install the empty module through Apps (developer mode, Update Apps List). Add the vocabulary file **without** the manifest line, update, nothing appears (**breakage 1**). Add the line, update, show Settings > Vocabularies. **Breakage 2**: `domain="administrative"`, read the traceback, fix to `social_assistance`. | Predict before each run |
| 10:35 | 4. Step 2: model | Demo, predict | `_inherit` versus `_name`, the `dswd_` prefix, Many2one with namespace domain, why not `Selection` (32 statuses, 2,000 IP groups, deployment profiles). Forget the import in `models/__init__.py` (**breakage 3**): no error, no field. Show Settings > Technical > Fields. | Spot the missing line on the printed diff |
| 10:50 | 5. Buffer | | Absorb overrun or take questions. | |
| 10:55 | 6. Step 3: view | Demo, predict | Open the upstream form in `vendor/` first, find `group_tags_section`. Inherit, one XPath, a "4Ps" group. Misspell the anchor (**breakage 4**): "cannot be located in parent view". Fix, open a household, set a value. | Predict where the field appears |
| 11:10 | 7. Step 4: test | Demo, predict | The test run was started in a second terminal at 10:55 (it builds a fresh database). Walk the test file while it runs; read the log path and the summary line. Flip an assertion if time allows. | Find the failing line on the handout |
| 11:25 | 8. Step 5: Claude Code | Demo | Ask it for the constraint plus a failing-first test; review the diff together; rerun. The point is "review the diff", not "the AI did it". | Watch |
| 11:35 | 9. Troubleshooting drill | Pairs, paper | Three log excerpts on a sheet; each pair names the file to open and the fix; three pairs report. This produces the observation-checklist evidence. | Work in pairs |
| 11:50 | 10. Recap and handoff | | Objectives slide; what moves to Module 5; the Day 3 exercise sheet; "before Module 6: `git checkout m4-step-5` and `./odoo-project start`". | Questions |

## 5. Handling the skill spread

- **Three self-selected tracks.** *Read*: no laptop needed, printed code per step and the handout. *Follow*: a working
  laptop, `git checkout m4-step-N` then `./odoo-project update`, no typing. *Stretch*: challenge cards (add the field as
  an optional column on the household list; start the Day 3 exercise early).
- **Pairs.** Seat CMTs next to RITOs or NPMO developers. Rule: ask your pair, then your row, then Edwin.
- **Git tags per step** (`m4-step-0` to `m4-step-5`) are the single source of truth; anyone can jump to a working state,
  and they double as the Day 3 starting point.
- **Predict-then-see** questions are the participation mechanism; they work at every level and need no environment.

## 6. What moves to Module 5 and Module 6

**Module 5 (afternoon, DSWD-specific)**: new models with menus and ACL rows; security groups and record rules on the
three OpenSPP tiers; the vocabulary-model extension (A'); hierarchical vocabularies (client status, 32 in 9
categories); programs, cycles and enrolment hooks; compliance events; change requests; the job worker; the production
module map in section 8 of the 4Ps reference.

**Module 6 (Day 3, hands-on, tiered)**:

- *Minimum, no environment*: a `dswd_wellbeing_broken` copy with three planted faults (data file missing from the
  manifest, misspelled anchor, invalid `domain`); find them and write the expected symptom for each.
- *Standard*: add the well-being field as an optional column on the household list view
  (`spp_registry.view_groups_list_tree`), update, show it.
- *Stretch*: `dswd_id_types`, adding `philsys` to the upstream ID Type vocabulary with
  `^\d{4}-\d{4}-\d{4}-\d{4}$`, plus one test that an invalid value raises `ValidationError` (the upstream
  `spp.registry.id` validates in a constraint, so this is testable).

## 7. The minimum concept set (and what to leave out)

Teach these, each tied to the file a participant will open when something breaks:

| Concept | What to say | Leave out until later |
| --- | --- | --- |
| Manifest | `name`, `depends`, `data`, `installable`. "A file not listed in `data` does not exist." | `auto_install`, `application`, categories, maintainers |
| `_inherit` versus `_name` | `_inherit` adds columns to an existing table; `_name` creates a table and then needs an ACL row. | New models live |
| Import chain | `__init__.py` to `models/__init__.py` to the file. Forgetting it gives no error, only a missing field. | |
| XML records and xml ids | `<record id= model=>`, `ref=`, `noupdate="1"`, and `module.id` as the address of everything. | Demo data, `Command` API |
| View inheritance | `inherit_id`, one XPath on a named anchor, `position="after"`. Mention `hasclass()` as the Odoo 19 rule only. | Positional XPath, attributes edits |
| ACL csv | Header and one row shape; "no new model, no rows". | Groups, record rules |
| The loop | Edit, `./odoo-project update`, refresh. Manifest, data, security, new fields and new views need `update`; `noupdate` data needs a fresh database or deleting the record. First install is Apps > Update Apps List. | Migrations |
| Logs | `./odoo-project logs`; the three lines to recognise: `Loading module dswd_...`, `ParseError`, `cannot be located in parent view`. | |
| One test | `TransactionCase` via `RegistryCommon`, `self.env[...]`, `assertEqual`, the summary line, the log file path. | Tags, tours, HTTP cases |

## 8. The five mistakes to drill (they are the quiz and the drill sheet)

| Mistake | Symptom | One-line diagnostic |
| --- | --- | --- |
| Module not in Apps (folder typo, no manifest, list not refreshed) | Search finds nothing | Developer mode on, Update Apps List; `./odoo-project logs` has no `dswd_` line |
| File written but not in manifest `data` | Update clean, UI unchanged | `grep vocabulary_ dswd_wellbeing/__manifest__.py` |
| Restart instead of update, or edited `noupdate` data | Change never shows | New field, view or data: `update`; changed `noupdate` record: delete it under Technical > External Identifiers, or `stop -v -y` |
| Wrong XPath anchor (`group_tag_section`, `@class=`) | `Element '<xpath ...>' cannot be located in parent view` | `grep -n 'name="group_' vendor/openspp/spp_registry/views/individual_views.xml` |
| New model without ACL, or import missing | `have no access rules` warning, `AccessError`, or field silently absent | Technical > Fields, search `dswd_` |

## 9. Materials to produce

| Material | Purpose | Priority |
| --- | --- | --- |
| `dswd_wellbeing` in the template, built test-first, with tags `m4-step-0` to `m4-step-5` | Source of truth; survives any live failure | Essential |
| `dswd_wellbeing_broken` folder (three planted faults) | Day 3 minimum track and the drill | Essential |
| Trainer runbook (`training/module4-runbook.md`) | Commands per block, the four breakages, cut-off times, drop order, fallbacks | Essential |
| Slides, about 18, one file per slide | Anatomy, patterns, objectives, Module 5 preview | Essential |
| Anatomy one-pager handout | Fill-in map; desk reference afterwards | Essential |
| Troubleshooting drill sheet and answer key | Observation-checklist evidence | Essential |
| Quiz bank, 10 items, 5 paired pre/post | Evaluation | Essential |
| Day 3 exercise sheet (three tiers) | Handoff | Essential |
| Screen recording of the full demo | Fallback if Edwin's machine fails; post-training reference | Strongly recommended |
| Printed per-step diffs | Read track | Nice to have |
| Command cheat sheet (`odoo-project`, git tags, Windows shim) | Follow track | Nice to have |
| Challenge cards | Stretch track | Nice to have |

## 10. Template work needed before the training

1. **Build `dswd_wellbeing`** test-first, commit per step, tag each step. Measure the wall time of
   `./odoo-project test dswd_wellbeing` on a participant-class Windows laptop.
2. **Add an `install` command to the CLI.** Today `update` only upgrades modules already installed and nothing installs
   a new module into the running database except the Apps UI or a fresh start. The Apps path is fine for the demo
   (it teaches module discovery), but every Follow-track participant and the Day 3 exercise will hit this.
3. **Fix the guide inaccuracies** a beginner would copy. Confirmed: the `domain="administrative"` example, the
   non-existent menu id `menu_spp_vocabulary_configuration`, the `urn:dswd:vocab:` namespace pattern, and the menu path
   "Registry > Configuration > Vocabularies" (it is Settings > Vocabularies). To verify before fixing: the Layer 0 list
   (`hr, stock, account`) contradicting CLAUDE.md; the scaffold referencing `dswd_attendance.group_dswd_attendance_officer`
   from a generic module; the scaffold menu under `base.menu_custom`; and the extending guide's Step 3 targeting an
   individual-page anchor without saying households use the `group_*` anchors. Add a sentence on first install.
4. **Point participants at one guide.** `extending-openspp.md` is the Module 4 companion; `module-development.md` is
   900 lines of starter and variant patterns and belongs to Module 5.
5. **Prepare the demo machine**: two databases warmed (step 0 and step 5), terminal and editor at 20pt, light theme,
   at most 25 lines per screen, tags pushed, recording made.
6. **Recruit two volunteer helpers** with a green `./odoo-project doctor` during Module 3 for a triage table at lunch.

## 11. Risks

| Risk | Mitigation |
| --- | --- |
| 30 to 50 percent of laptops not working | Nothing in Module 4 needs a participant laptop; Read track; triage at lunch before Module 5 and Day 3 |
| Time overrun | Cut-off per block in the runbook; drop order fixed in advance; drill and recap never dropped |
| Lost beginners | Every file introduced through the 4Ps requirement; predict questions; handout fill-in; pairing |
| Bored experts | Challenge cards; early start on the Day 3 exercise; production pattern shown as a Module 5 teaser |
| Live failure on Edwin's machine | Tags per step; warm databases; the recording |
| Test run too slow to show live | Start it in a second terminal at 10:55; show the log path and summary when it ends |
| Code unreadable from the back | 20pt, light theme, trimmed files, and the same code printed in the handout |

## 12. Sample post-test items

1. (Obj 1) A new `data/vocabulary_well_being_level.xml` exists, the module installs, but the vocabulary is absent.
   Most likely cause? a) missing ACL row b) file not listed in the manifest `data` c) wrong `_inherit` d) missing
   `tests/__init__.py`. Answer: b.
2. (Obj 2) 4Ps needs a well-being level on households. Correct approach? a) `_name = "res.partner"` b)
   `_inherit = "res.partner"` with `dswd_well_being_level_id` c) a new model `dswd.household` d) edit
   `vendor/openspp/spp_registry`. Answer: b.
3. (Obj 2) In one sentence, why a Many2one to `spp.vocabulary.code` instead of `fields.Selection`? Expected: codes can
   be added or varied per deployment through the Vocabularies UI without a code change.
4. (Obj 3 and 4) An update fails with `Element '<xpath expr="//group[@name='group_tag_section']">' cannot be located in
   parent view`. Which file do you open and what do you compare it against? Expected: the module's view file against
   the group names in the upstream `spp_registry` form view.
5. (Obj 5) Write the command that runs the tests of `dswd_wellbeing` and name the line that tells you whether they
   passed. Expected: `./odoo-project test dswd_wellbeing`; the summary line with the failure and error counts.

## 13. Open points for Edwin

1. Approve the strategy (demo-led Module 4, hands-on in Module 6) or ask for a typing block in Module 4 anyway.
2. Confirm the five decisions in section 3.
3. Should the `install` CLI command be added before the training (small change, one new subcommand)?
4. Training date: the folder name says November 2026. If it is within two weeks, the "Essential" materials are the
   only ones to build; say so and I will plan in that order.
5. Will Claude Code be available on the demo machine during the session (block 8), or should that block be a
   recording?
