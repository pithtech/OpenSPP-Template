# Module 3 Runbook: Introduction to Odoo

Day 2, 8:30 to 10:00. Trainer copy. Objectives and rationale are in
[docs/planning/module3-training-design.md](../../docs/planning/module3-training-design.md); this page is only what to do
and say, with the commands and the real log lines.

**Cut-offs are hard; the session ends at 10:00, a ten-minute break follows, and Module 4 starts at 10:10 with the same
trainer.** Drop order if late: the shell demo in block 8b, then step 6 reduced to opening the PDF (one minute, no code),
then the participants' test run in block 8 (it becomes the lunch task). The planted AccessError in block 6 costs two
minutes and is never dropped, nor is block 9, the hand-off.

## Before the session

- Demo laptop: stack running, developer mode on, the module uninstalled and the tree at `m3-step-0`; `m3-step-6` is the
  finished module (see [README.md](README.md)). The eight files open in tabs. Terminal and editor at 20pt.
- The test database is warm: `./odoo-project test dswd_asset` has run once today.
- Handout and command card printed for everyone. The Module 4 handout and drill sheets ready for 10:10.
- Slide 1 (title) ready; door slide (slide 2) up from 8:15: "Run `./odoo-project start`, log in, turn on developer mode.
  Then wait."

## Block 1, 8:30 to 8:35: objectives and hands up

Slide 3.

1. The eight objectives, one breath each. "By ten you will have built a module, and after the break you will learn why
   you will almost never build one that way for 4Ps."
2. "Who sees the login page?" Hands up. Pick two green hands near the aisles as the helpers for Module 4; thank them
   now.

## Block 2, 8:35 to 8:50: what Odoo is, MVC, and Odoo in five words (demo only)

Slides 4 to 6.

1. **What Odoo is** (3 min, slide 4): Python on PostgreSQL, Community under LGPL, one release a year, Odoo 19;
   everything is a module; OpenSPP is a hundred modules on Odoo, `dswd_*` sits on top. "You are not learning a product;
   you are learning the platform the product is made of."
2. **MVC** (3 min, slide 5): model = `models.Model` and the ORM; view = XML and QWeb; controller = actions, menus and
   model methods. "Keep the controller thin: a button calls a method, the method uses the ORM."
3. **Five words, each one screen** (slide 6, one table slide; one screen per row, in the table's order):
   - **Module = folder.** `./odoo-project logs | grep addons` shows `/mnt/extra-addons/custom` (their repository) in the
     addons path. "Every entry in Apps is a folder with a manifest."
   - **Model = table.** Settings > Technical > Models, search `res.partner`. Open it: fields from `base`,
     `spp_registry`, `spp_vocabulary`... "Many modules add columns to one table. Hold that thought until 10:40."
   - **Field = column.** Settings > Technical > Fields, filter model `res.partner`: each row is a column with a type.
   - **View = drawing.** Settings > Technical > Views, filter model `res.partner`: list, form, search are three XML
     records. "You will write one by 9:20."
   - **Menu, action, view, model.** Registry > Browse All (Audit) > All Groups, then developer menu > Edit Action: "a
     menu points at an action, an action names a model and its views."
4. Not one of the five, but it is what made those screens visible: developer mode, the bug icon and the Technical menu.
   "If yours is not on yet, turn it on now (slide 2); it is the only thing you do with the laptop before 8:50."

## Block 3, 8:50 to 8:57: step 0, the manifest (demo, then install)

Slides 7 to 9.

1. Slide 7, under a minute: the finished form. "This is the screen you will have at 9:30. Fill in the file map on your
   handout, section 3, as we go."
2. Show `__manifest__.py` and the empty `__init__.py`. "Odoo needs a folder and a manifest, nothing more. The `dswd_`
   prefix is our project's rule, the way `spp_` is OpenSPP's; it says who owns the code, not what it is about." Point at
   `data`: "a file not listed here does not exist to Odoo: no error, it is simply ignored."
3. Apps > Update Apps List > remove the **Apps** filter (the x on the facet; the module is not an application) > search
   "Asset" > Install. `./odoo-project logs`: point at `Loading module dswd_asset` (an install from Apps runs in the
   server, so `logs` shows it).
4. **"Install now."** Everyone: `./odoo-project install dswd_asset`. Predict first: "mine is an empty folder, yours is
   the finished module; what will differ in Apps in three minutes?" (Theirs shows the app tile; mine shows nothing.)

## Block 4, 8:57 to 9:10: step 1, the model (demo, predict)

Slides 10 to 14. Installs run in the background; nothing here needs a laptop.

1. `git checkout m3-step-1`. Open `models/dswd_asset.py`. One field type per minute: Char and `required`, Selection,
   Many2one to `res.users` with a default, Date twice, Boolean, the computed Boolean with `@api.depends`, the
   constraint. "`_name` makes a table; `_description` is required by our lint, and Odoo warns without it." Show the two
   import lines (`models/__init__.py`, `__init__.py`): "forget either and the model is silently absent."
2. Plant the question at the Selection: "Region IV buys tablets. What do we change?" Take two answers. "Hold that
   thought."
3. `./odoo-project update`. Settings > Technical > Fields, search `dswd.asset`: fourteen rows, the eight fields you
   wrote and the six Odoo adds to every table (`id`, `display_name`, who and when created and last updated). "No view
   yet: invisible, not broken."
4. Read the warning in the `update` output (it prints in the terminal where `update` ran, not in `logs`), exactly as it
   will appear on their laptops on Day 3:
   ```
   WARNING ... odoo.modules.loading: The models ['dswd.asset'] have no access rules in module dswd_asset, consider adding some, like:
   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   dswd_asset.access_dswd_asset,access_dswd_asset,dswd_asset.model_dswd_asset,base.group_user,1,0,0,0
   ```
   "Odoo even suggests a row; ours will have four, with the system row first. Remember this warning. In fifteen minutes
   it becomes an error on screen."

## Block 5, 9:10 to 9:14: checkpoint

Slide 14 stays up.

"Is there an IT Assets tile on your home screen?" (Their copy is the finished module, so the tile shows once the install
is done.) Helpers walk the rows. Anyone red: pair up with a neighbour for the rest of the hour, lunch triage table.

## Block 6, 9:14 to 9:22: step 2, views, action, menu (demo, predict)

Slides 15 to 17.

1. `git checkout m3-step-2`. Show the list view ("`<list>`, not `<tree>`, in Odoo 19"; slide 15), the form (`<sheet>`,
   named groups), the search view (fields, a filter, a group-by), then the action (`view_mode` list,form) and the two
   menu items (slide 16). Predict: "where will it appear?"
2. Predict while slide 16 is still up (slide 17's title gives the answer away): "will the tile appear?" Then
   `./odoo-project update` and slide 17. Look: **no tile appears, even for admin.** "Odoo hides a menu whose model you
   cannot read." Open the action by its URL, `http://localhost:8069/odoo/action-dswd_asset.action_dswd_asset` (with the
   dev profile, the port `start` printed): **AccessError, even as admin**. Read it:
   ```
   You are not allowed to access 'IT Asset' (dswd.asset) records.
   No group currently allows this operation.
   Contact your administrator to request access if necessary.
   ```
   "The warning from block 4 became this. Which file?"

## Block 7, 9:22 to 9:34: step 3, groups and access rows (demo, then do)

Slides 18 to 20.

1. `git checkout m3-step-3`. Show `security/groups.xml`: a category, a privilege, viewer, officer, manager, and the last
   record that links the manager tier into `spp_security.group_spp_admin`: "every OpenSPP admin is now an asset
   manager." (`admin` opens the app through the first access row, `base.group_system`; the link is what makes it a
   manager, which is why it sees the officer-only button at step 5.) Show the four access rows: "viewer reads; officer
   reads, writes, creates; manager also deletes; system first, always."
2. `./odoo-project update` (slide 20). The IT Assets tile appears and the list opens. Create the demo laptop: tag
   `LT-0001`, make and model, type Laptop, today's purchase date, a warranty end date about six months ahead. Then a
   second asset, `PR-0001`, type Printer. (The shell demo in block 8b reads exactly these two records; if you show the
   bad-warranty dialog on the demo laptop, discard that change.)
3. **Everyone:** open IT Assets, register the laptop in front of you. Then group by Type. Then set a warranty end date
   earlier than the purchase date and read the dialog: that sentence is in the Python file you saw at 9:00.

## Block 8, 9:34 to 9:40: step 4, the tests (demo, then start yours)

Slide 21.

1. `git checkout m3-step-4`. "The tests were written with each step since step 1; step 4 completes the module
   description, so this is where we read them." Open `tests/test_dswd_asset.py`: `setUp` creates one asset;
   `test_defaults`; `test_warranty_before_purchase_is_refused` with `assertRaises`. Open `tests/test_access.py`: three
   users, three groups, "the test proves the rows". The tag shows `(6, 0, [...])` on line 23; the finished module and
   the handout use `Command.set([...])`, the Odoo 19 form.
2. Run `./odoo-project test dswd_asset` on the demo machine (about 20 s warm). Read `0 failed, 0 error(s) of 8 tests`
   and the `Full log:` line. "Yours will say 12: your copy also has steps 5 and 6."
3. **Everyone:** start `./odoo-project test dswd_asset` and leave it running. "Read your summary line at 9:56."

## Block 8b, 9:40 to 9:48: steps 5 and 6, the ORM and a PDF report (demo)

Slides 22 to 26.

1. `git checkout m3-step-5`. Show the two methods: "no decorator, `self` is the record; `@api.model`, the whole table."
   Show the button in the form header (the finished module also gives it `groups="dswd_asset.group_asset_officer"`, so
   viewers do not see it). `./odoo-project update`. Press "Assign to me" on the demo laptop: the custodian changes.
   "That is `write` in one line."
2. `./odoo-project shell` (slide 23): `Asset = env["dswd.asset"]`, `Asset.search_count([])` (2),
   `Asset.search([("asset_type", "=", "laptop")]).mapped("name")` (`['LT-0001']`), create `LT-0099`, `write` (prints
   `True`), `a.custodian_id.name` (`'OdooBot'`: the shell runs as the superuser),
   `Asset.find_warranty_expiring(365).mapped("name")` (`['LT-0001']`), `a.unlink()` (`True`). "Nothing is saved until
   `env.cr.commit()`; `exit()` without it throws it away. That line belongs in the shell only, never in module code."
3. `git checkout m3-step-6`. Show the report file: an action and a template (the tag prints the date and user with
   `t-esc`; the finished module uses `t-out`, the Odoo 19 form). `update`. On the asset form: Print > Asset Sheet. The
   PDF opens. "HTML with `t-` attributes, then wkhtmltopdf. `docs` is what you printed."
4. Slide 26, one minute: the four mistakes; you saw the first today (the warning at 9:08, the error at 9:20). If late,
   skip it and point to Guide 3.19.
5. If late: show the PDF and the two files, skip the shell.

## Block 9, 9:48 to 9:56: the hand-off (never dropped)

Slides 27 to 30.

1. **The question.** "4Ps needs a well-being level on every household. Which file do we start with?" Take answers; most
   say a new model. Open Registry > Browse All (Audit) > All Groups, a household: the form shows dozens of fields, and
   the table behind it has hundreds of columns from several modules, the table from block 2. "A new `dswd.household`
   means two tables, two forms, two access files, and no link to programs. After the break you add one column to this
   table instead."
2. **The Selection, resolved.** Add `("tablet", "Tablet")` to `asset_type` live (the list only; `required` and `default`
   stay). `./odoo-project update`. Show it in the form. "One word cost a code change, a release, and an update on every
   server. In OpenSPP a code list is data: Settings > Vocabularies. That is the first file you see after the break."
3. **The table.** Last slide, back of the handout: today versus Module 4, row by row. Close: "Same files, same loop,
   same `test`. Three swaps matter most: `_inherit`, a vocabulary instead of a Selection, an inherited view."

## Block 10, 9:56 to 10:00: close

Slide 30 stays up.

1. "Read your test summary line." Hands up for `0 failed`.
2. "Leave the stack running; Module 4 needs nothing from it. Break until 10:10; helpers, see me." Then switch the demo
   machine to Module 4 (Module 4 runbook, "Switch to the live build").

## If the demo machine fails

- Any step: `git checkout m3-step-N` restores a known-good tree; `./odoo-project update` or `install` restores the
  database state.
- Docker gone: the recording for the current block, with the handout code on screen.
- Projector gone: the handout has every file; run the session from paper.

## Commands used in this session

```bash
./odoo-project start                   # before the session; --profile dev if 8069 is busy
./odoo-project install dswd_asset      # block 3, everyone
./odoo-project update                  # after each step on the demo machine; prints have no access rules
./odoo-project logs                    # the running server: Loading module ... after an install from Apps
./odoo-project test dswd_asset         # block 8, everyone
git checkout m3-step-N                 # N from 0 to 6, demo machine only
```
