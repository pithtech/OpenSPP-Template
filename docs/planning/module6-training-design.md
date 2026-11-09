# Module 6 Training Design: Three Modules of Your Own

> **Status**: proposal for Edwin's review (2026-11-09), revised with Edwin's decisions (section 8). Nothing is built and
> nothing goes into the participant guide until Edwin approves. **The reference solutions and the answer key are never
> in this repository**: participants create their repositories from it.
> **Sources**: Edwin's brief (one exercise each for module development, extending and customization, each related to
> DSWD 4Ps, running on the participant's own Docker stack, doable in 90 minutes); two expert proposals (instructional
> design; exercises checked against OpenSPP 2026.09 and Odoo 19); the program of activities (Day 3, 8:30 to 10:30,
> "Module 6: Hands-on Activity: Exploring Odoo and OpenSPP").
> **Slot**: Day 3, 8:30 to 10:30. 90 minutes of participant work, then 30 minutes in which Edwin discusses the work done.
> About 87 participants on Windows laptops. Followed by the Training Synthesis (10:30) and the post-test (11:00).

---

## 1. The strategy

1. **Three exercises, one per skill, each a module of the participant's own.** Development (a new model from scratch),
   extending (an OpenSPP model and view inherited), customization (OpenSPP configured through data). Each ends with the
   module installed on the participant's own stack, its tests passing, and the result on screen.
2. **Each one is a Day 2 pattern applied to a new 4Ps subject.** Exercise 1 follows Module 3 (`dswd_asset`), exercises
   2 and 3 follow Module 4 (`dswd_wellbeing`). Participants watched those modules built on Day 2; on Day 3 they type
   their own.
3. **Specs and a Day 2 file to copy, not the code.** The solutions are not shared, so a sheet never prints a complete
   file. Each step says what to build, which Day 2 file to copy and adapt (`dswd_asset` for exercise 1,
   `dswd_wellbeing` for exercises 2 and 3, both already in the participant's repository), the command to run, what the
   participant should see, and a hint for the one or two lines that are hard to guess (an XPath anchor, a vocabulary
   reference, a test assertion). The skill practised is the loop and reading errors, with real decisions to make. A short
   stretch at the end of each sheet keeps fast pairs busy.
4. **Showable by construction.** Every exercise ends in the same three proofs: the install line, the test summary
   (`0 failed`), and a screen. The 30-minute discussion is built on those.
5. **Pairs at one working laptop.** Participants without a working stack join a pair; nobody is parked.

## 2. Learning objectives

By 10:00 a participant can:

1. Create an Odoo module from scratch (manifest, model, views, menu, access rows, tests), install it and find it on
   screen.
2. Extend an OpenSPP model with a new field and show it on an OpenSPP view through view inheritance, without editing
   `upstream/openspp/`.
3. Customize OpenSPP through data (a code in an OpenSPP vocabulary) and prove the configuration with a test.
4. Run the loop on their own stack and read the output when something fails: which command after which change, where
   the error is printed, the first line that names a file in their module.

## 3. The three exercises

All three modules live at the root of the participant's repository, next to `dswd_asset` and `dswd_wellbeing`, follow
the repository rules (`dswd_` prefix, `application: False`, `auto_install: False`, `base.group_system` first in the
access file) and are installed with `./odoo-project install <module>`.

### Exercise 1, development: `dswd_fds_session` (40 minutes)

**The 4Ps subject.** Family Development Sessions are a monthly 4Ps condition (Module 5, card 12). A municipal office
wants a simple register of the sessions it held.

**What they build** (the sheet gives this as a specification; the solution is outside the repository). Copy and adapt
from: `dswd_asset` (manifest, model, views, menus, access file, tests).

| File                           | Content                                                                                                                                                  |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__manifest__.py`              | depends on `base`, `spp_area`, `spp_registry`                                                                                                            |
| `models/dswd_fds_session.py`   | `dswd.fds.session`: `name` (topic, required), `session_date` (required, default today), `area_id` (Many2one `spp.area`, the barangay), `facilitator_id` (Many2one `res.users`, default the current user), `attendee_count` (Integer); a constraint: the attendee count cannot be negative |
| `views/dswd_fds_session_views.xml` | list, form and search views (search by topic and barangay, group by barangay), an action                                                              |
| `views/menus.xml`              | a top-level menu "FDS Sessions"                                                                                                                          |
| `security/ir.model.access.csv` | `base.group_system` full; the OpenSPP registry viewer reads, the registry officer reads, writes and creates (`spp_registry.group_registry_viewer`, `group_registry_officer`) |
| `tests/test_dswd_fds_session.py` | the defaults are set; a negative attendee count is refused (`ValidationError`)                                                                         |

**Day 2 link.** Module 3 steps 0 to 4, one model instead of an asset, existing OpenSPP groups instead of new ones (so
there is no `groups.xml` to write), a real OpenSPP model (`spp.area`) in a Many2one.

**Done when.** `./odoo-project install dswd_fds_session` completes; `./odoo-project test dswd_fds_session` ends
`0 failed, 0 error(s) of 2 tests`; the "FDS Sessions" tile opens and a session saves; a negative count shows the
constraint message.

**Stretch.** A filter "This month" in the search view; a third test.

**Traps we expect** (to confirm in the dry run): the menu hidden until the access file loads (Module 3's step-2
lesson); a view field not on the model; the module not found in Apps because the default "Apps" filter hides it.

### Exercise 2, extending: `dswd_listahanan` (30 minutes)

**The 4Ps subject.** 4Ps households are identified from Listahanan, the national household targeting system; the
production registry keeps a Listahanan ID on every household (Module 5, card 3). Add it, unique.

**What they build** (as a specification). Copy and adapt from: `dswd_wellbeing` (manifest, `models/res_partner.py`,
`views/res_partner_views.xml`, header-only access file, tests); the uniqueness line from guide 3.8.

| File                             | Content                                                                                                                                                |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `__manifest__.py`                | depends on `spp_registry`                                                                                                                              |
| `models/res_partner.py`          | `_inherit = "res.partner"`; `dswd_listahanan_id` (Char; the UNIQUE constraint creates its index); no two households may share one                                                     |
| `views/res_partner_views.xml`    | inherits `spp_registry.view_individuals_form`, adds the field after `group_tags_section` (the anchor Module 4 used), shown only for households (`is_group`) |
| `security/ir.model.access.csv`   | header only: no new model                                                                                                                              |
| `tests/test_listahanan.py`       | a household takes an ID; a second household with the same ID is refused; the field is in the form's arch                                              |

**Day 2 link.** Module 4 steps 2 to 4 with a plain field instead of a vocabulary: `_inherit`, the `dswd_` prefix,
`inherit_id` plus one XPath on a named anchor, a test that reads the view.

**Uniqueness (decided).** A database constraint, `models.Constraint("UNIQUE(dswd_listahanan_id)", ...)`, the Odoo 19
replacement for `_sql_constraints` (guide 3.8). Its test expects the database error inside a savepoint; the sheet gives
that test idiom as a hint, because it cannot be guessed. The dry run records the message the user sees on screen.

**Done when.** `install` completes; `test` ends `0 failed of 3 tests`; the field shows on a household's Profile page
(Registry > Browse All (Audit) > All Groups) and not on an individual; a duplicate is refused on screen.

**Stretch.** The ID as an optional column on the household list (`spp_registry.view_groups_list_tree_base`, after
`registration_date`).

### Exercise 3, customization: `dswd_id_types` (15 minutes)

**The 4Ps subject.** 4Ps identifies members with PhilSys, the national ID; production adds PhilSys to OpenSPP's ID types
with a format check (Module 5, card 3; production `dswd_4ps_registry/data/id_types.xml`).

**What they build** (as a specification). Copy and adapt from: `dswd_wellbeing` (manifest, `data/` file, header-only
access file, tests); the record shape from upstream `spp_vocabulary/data/vocabulary_id_type.xml`.

| File                           | Content                                                                                                                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__manifest__.py`              | depends on `spp_registry`, `spp_vocabulary`                                                                                                                                     |
| `data/id_types.xml`            | one `spp.vocabulary.code` in OpenSPP's ID Type vocabulary (`spp_vocabulary.vocab_id_type`): code `philsys`, display "PhilSys ID", `target_type` `individual`, `id_validation` `^\d{4}-\d{4}-\d{4}-\d{4}$` |
| `security/ir.model.access.csv` | header only                                                                                                                                                                     |
| `tests/test_id_types.py`       | on `RegistryCommon`: an ID `1234-5678-9012-3456` is accepted; `12345678` is refused (`ValidationError`, OpenSPP's own constraint)                                               |

**Day 2 link.** Module 4 step 1 (a vocabulary as data, `noupdate`), Module 5's registry card. No model, no view: the
customization is pure data, and OpenSPP's existing code does the validation.

**Done when.** `install` completes; `test` ends `0 failed of 2 tests`; on an individual's Identity tab, PhilSys is in the
ID type list and an invalid number is refused with OpenSPP's message ("The provided PhilSys ID ID '12345678' is
invalid.", wording to confirm).

**Traps to put on the sheet.** Adding a manual `philsys` code in the Vocabularies screen first makes the install fail on
a duplicate code; forgetting the import in `tests/__init__.py` runs 0 tests; the ID Types screen under Studio edits a
different model (`spp.id.type`), which the Identity tab does not use.

**Stretch.** A second code (PhilHealth, with its pattern), and a test for it.

## 4. Run of show

| Time        | Min | Block                                                                   |
| ----------- | --- | ----------------------------------------------------------------------- |
| 8:00-8:30   |     | At the door: `start`, log in, `test dswd_wellbeing` once (warms up the first test run); pairs formed |
| 8:30-8:35   | 5   | Launch: the three modules, the three proofs, the rules (pair, then row, then helper, then trainer) |
| 8:35-9:15   | 40  | Exercise 1, development                                                 |
| 9:15-9:45   | 30  | Exercise 2, extending                                                   |
| 9:45-10:00  | 15  | Exercise 3, customization (planned for 20: the smallest module, one data record and a test; fast pairs finish it, the rest finish it after the session) |
| 10:00-10:30 | 30  | Discussion                                                              |

Checkpoints: at 9:15 and 9:45 a show of hands ("install done; tests green"); a pair still in exercise 1 at 9:25 moves to
exercise 2 and finishes 1 later. Driver swap at each exercise, so both partners type.

Without complete code on the sheets, exercise 3 is the one most pairs will not finish in the room. That is planned: it
is the smallest, the guide carries it, and the discussion still covers it from the pairs that did.

**If the dry run shows slow laptops** (a `test` or `update` over about 2 minutes): exercise 3 is announced as the
take-home at 8:30, and exercises 1 and 2 get 45 minutes each.

## 5. The 30-minute discussion

Pairs are picked while Edwin walks the room. The pair narrates from its laptop or its sheet; Edwin reproduces on the demo
laptop rather than switching laptops on the projector.

| Time        | Segment                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------- |
| 10:00-10:10 | Exercise 1: one pair shows its register; the errors pairs met on the way (hidden menu, a field not on the model) |
| 10:10-10:18 | Exercise 2: the field on the household and not on an individual; what happened with a duplicate               |
| 10:18-10:26 | Exercise 3: the refusal on the Identity tab; why OpenSPP validated without a line of Python from them          |
| 10:26-10:30 | Close: development, extending, customization: which one is the everyday job for 4Ps (extending and data), and where each lives in production |

## 6. Materials to build

In the repository, under `training/module6/`: only what participants may see. **Outside the repository**, in
`~/Documents/DSWD-4PS-Training-11-2026/module6/` on the trainer's machine: the three reference solutions as real
modules and `answers.md` (the expected output of each step, the errors participants meet and their fixes, the code of
every file).

| Material                                                   | For                 | Notes                                                                                   |
| ---------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------- |
| `exercise-1-development.md`, `exercise-2-extending.md`, `exercise-3-customization.md` | Participants, printed | Specification per step, the Day 2 file to copy, the command after each step, what you should see, hints, traps, stretch; no complete files |
| `runbook.md`                                               | Trainer             | Run of show, checkpoints, the discussion script, fallbacks                              |
| `slides.md`                                                | Projected           | 11 slides: door, launch, one per exercise, errors, push, discussion, after the training |
| `README.md`                                                | Trainer             | Index and preparation                                                                    |
| Participant guide, section 6                               | Participants        | Written after Edwin reviews the materials, as for Module 5                               |

**Verification before anything is printed.** The reference solutions are built by following the sheets, then copied
into a scratch checkout (never committed) and run on the stack: install, test, the screen, and the traps, so the expected
output on the sheets is the real output. Because the solutions are outside the repository, CI does not test them; the
trainer re-runs `./odoo-project test` on each before the session. For the demo, the trainer copies a solution into the
repository root of the demo laptop.

The current `training/module4/exercise-day3.md` and its answer key are replaced: the module 4 README and runbook, and
guide 4.14, point to Module 6 instead. `training/module4/dswd_wellbeing_broken/` stays as Module 4 drill material.

## 7. Risks

| Risk                                               | Mitigation                                                                                                     |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `update`, `install` and `test` slower on Windows than on the Mac (15 to 20 s here) | Edwin's Windows rehearsal times them; exercise 3 becomes the take-home if a cycle exceeds about 2 minutes        |
| Typing errors eat the time                         | Files given in full; the traps listed on each sheet; pair rule; helpers                                         |
| A laptop without a working stack                   | The participant joins a pair; the sheets also read as a worked example                                          |
| A failed `update` leaves the old server running and the old screens in the browser | Every sheet says: read the output to the end; if it does not say the update completed, it failed           |
| Without complete code, pairs fall behind      | Each sheet names the Day 2 file to copy; hints for the hard lines; exercise 3 planned to finish after the session for most |
| The solutions leak                                 | Solutions and answer key only outside the repository; the demo copies a solution to the root and does not commit |
| The default "Apps" filter hides the new modules    | The sheets use `./odoo-project install`; where Apps is used, they say to remove the filter                     |

## 8. Decisions

Taken by Edwin on 2026-11-09:

1. **The reference solutions stay outside the repository**, with the answer key: participants create their repositories
   from this template and must not receive them. Consequence: the sheets give specifications and the Day 2 file to copy,
   never complete files (Edwin's choice among three options: full code, skeletons with blanks, specifications).
2. **Uniqueness in exercise 2**: the database constraint, `models.Constraint`.
3. **No observation checklist** in Module 6.
