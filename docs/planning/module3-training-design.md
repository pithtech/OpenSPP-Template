# Module 3 Training Design: Introduction to Odoo

> **Superseded where the materials differ.** The run of show, commands and wording in
> [training/module3/runbook.md](../../training/module3/runbook.md) are current; this design is the rationale. As built:
> seven tagged steps (`m3-step-0` to `m3-step-6`); `depends = ["base", "spp_security"]`; `security/groups.xml` with
> viewer, officer and manager, and four access rows (system first); no Module 3 quiz and no pre-test or post-test (the
> Module 4 quiz is an optional self-check); at step 2 no tile appears, the AccessError is shown by opening the action's
> URL; a ten-minute break at 10:00, Module 4 from 10:10. Sections 4, 5, 8, 11 and 12 below were written before these
> changes.

> **Status**: proposal for Edwin's review (2026-11-08). Synthesised from Edwin's brief, an instructional-design review
> and an Odoo trainer review run as independent agents on the same brief, and facts verified in the repo.
> **Slot**: Day 2, 8:30 to 10:00, the first session of the day, then a ten-minute break and Module 4 (10:10 to 12:00). Same
> trainer. Day 1 covered the DPG ecosystem and how OpenSPP was built on Odoo, conceptually.
> **Audience**: about 87 DSWD IT staff of mixed skill; every participant arrives with a running stack (mandatory
> pre-training step 8.5).

---

## 1. The strategy in five sentences

1. Module 3 is **"build something new"**; Module 4 is **"extend what OpenSPP already has"**. Every slide, file and
   error in Module 3 is chosen so that Module 4 reads as the next step of the same arc, not a new topic.
2. The concept lecture is **twelve minutes**, each concept shown on the running stack rather than explained, because
   Day 1 already gave the conceptual picture and the rest of the time belongs to building.
3. Edwin builds **one generic module live, `dswd_asset`, an IT asset register, in seven steps** (0 to 6) from pre-made tags.
   Thirty-six of the 87 participants are computer maintenance technologists who keep exactly this register.
4. Participants touch their laptops **three times**: install the module, register their own laptop in it, start the
   test run. Each touch sits at the start of a demo-only block so the room absorbs the waiting.
5. Two things are **planted**: a missing access row, which produces the exact error participants will meet on Day 3,
   and a hard-coded Selection field, "asset type", which becomes the bridge to Module 4's vocabulary.

Changes to Edwin's brief, with reasons: the demo module ships in the participants' repositories as the finished
module (a template copy has no tags), so "install it manually" means one install when the UI appears, not one per
step; the lecture part is shorter than "lecture with demo" suggests, because every concept is cheaper to show than to
tell; and the module carries the `dswd_` prefix because the repo's lint requires it, with one honest sentence on the
slide ("Odoo needs a folder and a manifest; the prefix is our project's rule, like `spp_` is OpenSPP's").

## 2. Learning objectives, each one feeding a Module 4 objective

| #   | By 10:00 a participant can                                                                                                                      | Prepares Module 4 objective             |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 1   | State that a module is a folder with `__manifest__.py`, name the role of each file in a new module, and say that a file not in `data` does not exist. | 1, the same rule re-read                |
| 2   | Write a `_name` model with Char, Selection, Date, Many2one and Boolean fields, say "model = table, field = column", and say which changes need `update`. | 2, `_name` versus `_inherit`, Selection versus vocabulary |
| 3   | Write a list view, a form view, an action and a menu, and explain the chain menu, action, view, model.                                          | 3, inherit a view instead of writing one |
| 4   | Write the access row a new model needs, and recognise its absence in the log and in the UI.                                                     | 4, read a log line, name the file       |
| 5   | Run `./odoo-project test dswd_asset` and read the summary line.                                                                                 | 5, identical                            |

## 3. The demo module: `dswd_asset`

Chosen over a help-desk ticket (needs a state machine, the one legitimate use of a Selection, which would muddy the
hand-off) and a training attendance sheet (needs registrant relations, too close to Module 4). Model `dswd.asset`,
depends on `base` and `spp_security` (only to link its manager group into the OpenSPP admin group), so it is still plain
Odoo on the slide.

| Field              | Type                                            | Why it is there                                              |
| ------------------ | ----------------------------------------------- | ------------------------------------------------------------ |
| `name`             | Char, required, "Asset Tag"                     | the required-field error is the first validation they see    |
| `model_name`       | Char, "Make and Model"                          | Char versus Text in one glance                               |
| `asset_type`       | Selection: laptop, desktop, printer, other      | the planted hook: hard-coded today, a vocabulary in Module 4 |
| `custodian_id`     | Many2one `res.users`, default the current user  | Many2one is familiar before Module 4's Many2one to a code    |
| `purchase_date`    | Date                                            | a non-text type with a widget                                |
| `warranty_end_date`| Date                                            | the pair that the constraint checks                          |
| `is_in_use`        | Boolean, default True                           | a filter in the search view                                  |
| `is_under_warranty`| Boolean, computed from `warranty_end_date`      | one `@api.depends` so the word "computed" is not new in Module 4 |

Plus one constraint (warranty cannot end before purchase), which gives the test suite something to refuse and gives
participants an error dialog to read. Left out and named on a slide as "Module 5": One2many, chatter, Monetary, state
buttons, record rules, demo data (participant databases are created without demo data anyway).

Files, each short enough for one slide: `__manifest__.py`, `__init__.py`, `models/__init__.py`,
`models/dswd_asset.py`, `views/dswd_asset_views.xml` (list, form, search, action), `views/menus.xml` (a top-level
app menu with an icon, so the app tile appearing is the payoff moment), `security/groups.xml` (viewer, officer, manager) and `security/ir.model.access.csv` (four rows,
`base.group_system` first), `tests/test_dswd_asset.py` (defaults; the
constraint refuses; on `TransactionCase` with `setUp`), `readme/DESCRIPTION.md`.

The Selection deliberately contradicts the repo checklist "no static Selection for vocabulary-backed values". The
readme and the slide say so: it is the before picture.

## 4. Run of show

A door slide from 8:15: "Run `./odoo-project start` now and turn on developer mode. Do not touch it again until I
say." Nothing in the first twenty minutes needs a laptop, so late arrivals cost nothing.

| Time | Block                              | Mode              | Trainer                                                                                                                                                                                                                        | Laptops                                  |
| ---- | ---------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| 8:30 | 1. Objectives, hands up            | talk              | "Who sees the login page?" Recruit the two helpers Module 4 needs from the green hands.                                                        | `start` only                             |
| 8:35 | 2. Odoo in twelve minutes          | demo              | Five concepts, each on screen: module = folder with a manifest (the addons path in `logs`); model = table (Technical > Models, `res.partner`, "many modules add columns to one table, hold that thought until 10:40"); view = how a table is drawn (Technical > Views); menu, action, view, model (developer mode "Edit Action"); developer mode itself. | developer mode on                        |
| 8:47 | 3. Step 0, manifest and `__init__` | demo, predict     | The empty module; Apps > Update Apps List > Install on the demo machine; `Loading module dswd_asset` in the log. Then: **"Install now"**. Predict: "mine is empty, yours is finished; what differs in Apps?"                  | **touch 1**: `./odoo-project install dswd_asset` |
| 8:55 | 4. Step 1, the model               | demo, predict     | One field type per minute with its why. `update`. Technical > Fields shows fourteen rows (eight fields plus six automatic ones); the `update` output says `The models ['dswd.asset'] have no access rules in module dswd_asset, consider adding some, like:`. "No view yet: invisible, not broken." Plant the Selection question: "Region IV buys tablets. What do we change?" Hold the answer. | installs finish in the background        |
| 9:10 | 5. Checkpoint                      | buffer            | "Apps, search Asset: installed?" Helpers walk the rows.                                                                                                                                                                       | a glance                                 |
| 9:14 | 6. Step 2, views, action, menu     | demo, predict     | Predict: "where will the menu appear?" `update`; no tile appears, even for admin (Odoo hides a menu whose model the user cannot read); open the action by URL: **AccessError, even as admin** (planted: no access row).                                                           |                                          |
| 9:22 | 7. Step 3, the access row          | demo, then do     | Groups and four rows, `update`, the tile appears and the list opens. Create the demo laptop. Then participants register their own laptop, group by type, and set a warranty date before the purchase date to read the constraint's dialog.                       | **touch 2**: create a record             |
| 9:34 | 8. Step 4, tests                   | demo              | Walk the two tests; run on the demo machine (about 20 s once the image is warm). Participants start theirs and leave it running.                                                                                              | **touch 3**: `./odoo-project test dswd_asset` |
| 9:42 | 9. The hand-off (never dropped)    | demo, slide       | Section 5.                                                                                                                                                                                                                     | read the test summary when it lands      |
| 9:54 | 10. Close                          | talk              | Three quiz items by show of hands; "leave the stack running, Module 4 needs nothing from it"; the two helpers meet Edwin at the break.                                                                                         |                                          |

Drop order if late (current, see the runbook): the shell demo, then step 6 reduced to opening the PDF, then the
participants' test run (becomes the lunch task). The planted AccessError and the hand-off are never dropped.

## 5. The hand-off to Module 4

Three devices, in this order, at 9:42:

1. **The question.** "4Ps needs a well-being level on every household. Which file do we start with?" Most will answer
   a new `models/dswd_household.py`. Open Registry > Browse All (Audit) > All Groups: the household table already exists with dozens of columns
   from several modules (the Technical > Models x-ray from 8:40 said so). A new model means two tables, two forms,
   two access files, and no link to programs. "After the break you will add one column to the existing table instead."
2. **The planted Selection, resolved.** Add `("tablet", "Tablet")` to `asset_type` live, `update`, show it works, then:
   "that was a code change, a release, and an update on every server for one new word. In OpenSPP a code list is
   data, edited under Settings > Vocabularies. That is the first file you see after the break."
3. **The side-by-side table**, the last slide and the back of the handout:

| Today, `dswd_asset` (8:30)                          | Next, `dswd_wellbeing` (10:10)                                   |
| --------------------------------------------------- | ---------------------------------------------------------------- |
| `_name = "dswd.asset"`, a new table                 | `_inherit = "res.partner"`, columns on an existing table         |
| `asset_type = fields.Selection([...])`              | `dswd_well_being_level_id = fields.Many2one("spp.vocabulary.code")` |
| `<list>` and `<form>` written from scratch          | `inherit_id` plus one XPath on a named anchor                    |
| an action and a menu you created                    | no menu: the household form already has one                     |
| groups and four access rows                         | access file: header only, "no new model, no rows"                |
| `depends = ["base", "spp_security"]`                | `depends = ["spp_registry", "spp_vocabulary"]`                   |
| `TransactionCase`, `create()` your own record       | `RegistryCommon` hands you a household                           |
| the field is yours: `asset_type`                    | a field on someone else's model: prefix `dswd_`                  |

Close: "Same files, same loop, same `test`. Three things change, and each is a one-line swap in this table."

## 6. The loop, stated honestly for both profiles

The Module 4 handout says a Python edit needs nothing because the dev profile reloads. That is true only for
`start --profile dev` (it passes `--dev=reload,qweb,xml`); the default `start` uses the ui profile without it. Module 3
teaches the loop first, so its table says: manifest, data, security, a new field or a new view record: `update`; a
Python method body: `restart` (ui) or nothing (dev); an edited view: `update` (the arch lives in the database); a
brand-new module: `install`. The Module 4 handout gets the same two-line correction in this round.

## 7. New-module mistakes to drill (the Module 4 drill covers extension mistakes)

| Mistake                                  | Symptom                                                                                   | Diagnostic                                                        |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| No access row                            | `The models ['dswd.asset'] have no access rules` on update; menu hidden; `AccessError` by URL even as admin | `grep dswd_asset security/ir.model.access.csv`                    |
| Action without a menu, or menu without `action=` | clean update, nothing to click                                                    | Technical > User Interface > Menu Items, search the name          |
| A view field that is not on the model    | update fails: `Field "custodian" does not exist in model "dswd.asset"`, file and line     | compare against Technical > Fields                                |
| `_name` versus the access row's `model_id` | `No matching record found for external id 'model_dswd_assett'` at the csv line          | `model_` plus `_name` with dots as underscores, exactly           |

## 8. Materials (Module 4 formats, under `training/module3/`)

| Material                                                     | Priority            |
| ------------------------------------------------------------ | ------------------- |
| `dswd_asset` at the repo root, test-first, tags `m3-step-0` to `m3-step-6`, `auto_install: False` | Essential |
| `runbook.md`: commands per block, the planted fault with its real log line, cut-offs, drop order  | Essential |
| `slides.md`: Marp, 26 slides, screenshots from the real stack                                      | Essential |
| `handout-anatomy.md`: fill-in file map, the field-type table, the loop, the mistakes, the code per step, the side-by-side table on the back | Essential |
| `command-card.md`: half a page: `start`, `install dswd_asset`, `test dswd_asset`, `resetassets`, `logs` | Essential |
| `quiz.md` and `quiz-answers.md`: not built; no Module 3 quiz, no pre-test or post-test             | Dropped   |
| `README.md`: index and demo-machine preparation                                                   | Essential |
| Screen recording; one stretch card ("add a `location` Char and a list column")                     | Nice to have        |

No broken copy for Module 3: Module 4's drill already covers diagnosis.

## 9. Repo fixes folded into this round

From the Odoo review, verified: the development guide's scaffold access rows reference officer and manager groups
that the scaffold manifest never defines; two notes claim `spp_security` provides cross-project officer and manager
groups (it provides only `group_spp_admin` and a self-restriction group); the scaffold manifest shows an
`external_dependencies` line with a placeholder library that aborts install if copied; the scaffold test lacks the
`@tagged` decorator the testing rule requires. Plus the two-line loop correction in the Module 4 handout.

## 10. Risks

| Risk                                                   | Mitigation                                                                                               |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| First session of the day: stacks down, late arrivals   | Door slide; twenty laptop-free minutes; checkpoint at 9:10, not 8:47                                     |
| 87 installs at once                                    | Installs are local, so failures are individual: helpers per row, pair rule, lunch triage; a failed install costs nothing, the module is in the repo for Day 3 |
| `install` wall time on Windows laptops unknown         | Measured 6 s plus restart on a Mac; measure on the Windows machine during Edwin's rehearsal; the fourteen-minute demo block after it absorbs the wait |
| First `test` run slow (fresh database)                 | Started at 9:34, read at 9:54; lunch task if needed                                                      |
| Overrun into the break and Module 4 (10:10), same trainer | Cut-offs per block, fixed drop order, the hand-off never dropped                                          |
| Demo machine fails                                     | Tags per step, warm database, the recording                                                              |

## 11. Sample quiz items (not built)

1. (Obj 1) `views/dswd_asset_views.xml` exists and `update` is clean, but the menu never appears. Most likely cause?
   a) missing `_description` b) the file is not in the manifest `data` c) missing `tests/__init__.py` d) wrong
   `view_mode`. Answer: b.
2. (Obj 2) A new office needs an asset type "tablet". With today's `fields.Selection`, what has to happen? Expected:
   edit the Python, release, `update` on every server. Follow-up: what does OpenSPP use instead?
3. (Obj 3) A user clicks a menu and sees a list. Put in order: model, action, menu, view. Answer: menu, action, view,
   model.
4. (Obj 4) The `update` output shows `The models ['dswd.asset'] have no access rules in module dswd_asset` and admin
   gets `AccessError`. Which file, which
   row? Expected: `security/ir.model.access.csv`, a `base.group_system` row with 1,1,1,1 first.
5. (Obj 5) Write the command that runs the tests of `dswd_asset` and name the line that says whether they passed.
   Expected: `./odoo-project test dswd_asset`; the summary line with the failure and error counts.

## 12. Decisions for Edwin

1. The subject: IT asset register (recommended) rather than help-desk ticket or attendance sheet.
2. The menu: a top-level app menu with its own icon (the tile appearing is the payoff), rather than a child of the
   Registry menu, which is gated by registry groups.
3. Keep the planted Selection in the shipped module, with the note in its readme, as the before picture.
4. Superseded: no pre-test or post-test on Day 2; the Module 4 quiz is an optional self-check.
5. Superseded: the module ships three groups (viewer, officer, manager) and four access rows.

## 13. Additions decided on 2026-11-08 (evening)

Edwin asked for four additions, all adopted:

1. **What Odoo is**: a three-minute slide at the start of block 2 (platform, licence, release, module system,
   OpenSPP on Odoo). Developers should know the platform they study.
2. **MVC in Odoo terms**: a three-minute slide after it (model = `models.Model` and the ORM; view = XML and QWeb;
   controller = actions, menus and model methods).
3. **The ORM with examples in the demo module**: step 5 adds `action_assign_to_me` (a form button, `write` in one
   line) and `find_warranty_expiring` (`@api.model`, a `search` with a domain), tested, plus a shell session in the
   guide and the deck.
4. **A PDF report**: step 6 adds `report/dswd_asset_report.xml`, an `ir.actions.report` bound to the Print menu and a
   QWeb template, tested by rendering the HTML. The image carries wkhtmltopdf 0.12.6.1, so the PDF opens live.

Run of show after the additions: block 2 grows to fifteen minutes (8:35 to 8:50), blocks 3 and 4 start two to three
minutes later, the test block shrinks to six minutes, a new block 8b (9:40 to 9:48) covers steps 5 and 6, the hand-off
runs 9:48 to 9:56. New drop order: the shell demo first, then the planted AccessError, then the participants' test
run. Tags `m3-step-5` and `m3-step-6` are added after merge. The participant guide gains sections 3.2, 3.3, 3.11 and
3.12.
