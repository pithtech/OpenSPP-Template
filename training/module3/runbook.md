# Module 3 Runbook: Introduction to Odoo

Day 2, 8:30 to 10:00. Trainer copy. Objectives and rationale are in
[docs/planning/module3-training-design.md](../../docs/planning/module3-training-design.md); this page is only what to do
and say, with the commands and the real log lines.

**Cut-offs are hard; Module 4 starts at 10:00 with the same trainer.** Drop order if late: the shell demo in block 8b,
then the planted AccessError in block 6 (show the rows and move on), then the participants' test run in block 8 (it
becomes the lunch task). Block 9, the hand-off, is never dropped.

## Before the session

- Demo laptop: stack running, developer mode on, the module uninstalled and the tree at `m3-step-0`; `m3-step-6` is the
  finished module (see [README.md](README.md)). The seven files open in tabs. Terminal and editor at 20pt.
- The test database is warm: `./odoo-project test dswd_asset` has run once today.
- Handout and command card printed for everyone. The Module 4 handout and drill sheets ready for 10:00.
- Door slide up from 8:15: "Run `./odoo-project start`, log in, turn on developer mode. Then wait."

## Block 1, 8:30 to 8:35: objectives and hands up

1. The five objectives, one breath each. "By ten you will have built a module, and at ten you will learn why you will
   almost never build one that way for 4Ps."
2. "Who sees the login page?" Hands up. Pick two green hands near the aisles as the helpers for Module 4; thank them
   now.

## Block 2, 8:35 to 8:50: what Odoo is, MVC, and Odoo in five words (demo only)

1. **What Odoo is** (3 min, one slide): Python on PostgreSQL, Community under LGPL, one release a year, Odoo 19;
   everything is a module; OpenSPP is a hundred modules on Odoo, `dswd_*` sits on top. "You are not learning a product;
   you are learning the platform the product is made of."
2. **MVC** (3 min, one slide): model = `models.Model` and the ORM; view = XML and QWeb; controller = actions, menus and
   model methods. "Keep the controller thin: a button calls a method, the method uses the ORM."
3. **Five concepts, each one screen**, no slide longer than one sentence:

4. **Module = folder.** `./odoo-project logs | grep addons` shows `/mnt/extra-addons/custom` (their repository) in the
   addons path. "Every entry in Apps is a folder with a manifest."
5. **Model = table.** Settings > Technical > Models, search `res.partner`. Open it: fields from `base`, `spp_registry`,
   `spp_vocabulary`... "Many modules add columns to one table. Hold that thought until 10:30."
6. **View = drawing.** Settings > Technical > Views, filter model `res.partner`: list, form, search are three XML
   records. "You will write one by 9:20."
7. **Menu, action, view, model.** Registry > Groups, then developer menu > Edit Action: "a menu points at an action, an
   action names a model and its views."
8. **Developer mode.** The bug icon; the Technical menu. "Turn yours on now; it is the only thing you do with the laptop
   before 8:47."

## Block 3, 8:50 to 8:57: step 0, the manifest (demo, then install)

1. Show `__manifest__.py` and the empty `__init__.py`. "Odoo needs a folder and a manifest, nothing more. The `dswd_`
   prefix is our project's rule, the way `spp_` is OpenSPP's; it says who owns the code, not what it is about."
2. Apps > Update Apps List > search "Asset" > Install. `./odoo-project logs`: point at `Loading module dswd_asset`.
3. **"Install now."** Everyone: `./odoo-project install dswd_asset`. Predict first: "mine is an empty folder, yours is
   the finished module; what will differ in Apps in three minutes?" (Theirs shows the app tile; mine shows nothing.)

## Block 4, 8:57 to 9:10: step 1, the model (demo, predict)

Installs run in the background; nothing here needs a laptop.

1. `git checkout m3-step-1`. Open `models/dswd_asset.py`. One field type per minute: Char and `required`, Selection,
   Many2one to `res.users` with a default, Date twice, Boolean, the computed Boolean with `@api.depends`, the
   constraint. "`_name` makes a table; `_description` is mandatory in Odoo 19."
2. Plant the question at the Selection: "Region IV buys tablets. What do we change?" Take two answers. "Hold that
   thought."
3. `./odoo-project update`. Settings > Technical > Fields, search `dswd.asset`: nine columns. "No view yet: invisible,
   not broken."
4. Read the warning in `logs`, exactly as it will appear on their laptops on Day 3:
   ```
   WARNING ... odoo.modules.loading: The models ['dswd.asset'] have no access rules in module dswd_asset, consider adding some
   ```
   "Remember this line. In fifteen minutes it becomes an error on screen."

## Block 5, 9:10 to 9:14: checkpoint

"Apps, search Asset: installed?" Helpers walk the rows. Anyone red: pair up with a neighbour for the rest of the hour,
lunch triage table.

## Block 6, 9:14 to 9:22: step 2, views, action, menu (demo, predict)

1. `git checkout m3-step-2`. Show the list view ("`<list>`, not `<tree>`, in Odoo 19"), the form (`<sheet>`, named
   groups), the search view (fields, a filter, a group-by), the action (`view_mode` list,form), the two menu items.
   Predict: "where will it appear?"
2. `./odoo-project update`. The app tile "IT Assets" appears. Click it: **AccessError, even as admin**. Read it:
   ```
   You are not allowed to access 'IT Asset' (dswd.asset) records.
   ```
   "The warning from block 4 became this. Which file?"

## Block 7, 9:22 to 9:34: step 3, groups and access rows (demo, then do)

1. `git checkout m3-step-3`. Show `security/groups.xml`: a category, a privilege, viewer, officer, manager, and the last
   record that links the manager tier into `spp_security.group_spp_admin`: "that line is why admin can open it". Show
   the four access rows: "viewer reads; officer reads, writes, creates; manager also deletes; system first, always."
2. `./odoo-project update`. The list opens. Create the demo laptop: tag, make and model, type, today's purchase date.
3. **Everyone:** open IT Assets, register the laptop in front of you. Then group by Type. Then set a warranty end date
   earlier than the purchase date and read the dialog: that sentence is in the Python file you saw at 9:00.

## Block 8, 9:34 to 9:40: step 4, the tests (demo, then start yours)

1. `git checkout m3-step-4`. Open `tests/test_dswd_asset.py`: `setUp` creates one asset; `test_defaults`;
   `test_warranty_before_purchase_is_refused` with `assertRaises`. Open `tests/test_access.py`: three users, three
   groups, "the test proves the rows".
2. Run `./odoo-project test dswd_asset` on the demo machine (about 20 s warm). Read `0 failed, 0 error(s) of 8 tests`
   and the `Full log:` line.
3. **Everyone:** start `./odoo-project test dswd_asset` and leave it running. "Read your summary line at 9:56."

## Block 8b, 9:40 to 9:48: steps 5 and 6, the ORM and a PDF report (demo)

1. `git checkout m3-step-5`. Show the two methods: "no decorator, `self` is the record; `@api.model`, the whole table."
   Show the button in the form header. `./odoo-project update`. Press "Assign to me" on the demo laptop: the custodian
   changes. "That is `write` in one line."
2. `./odoo-project shell`: `env["dswd.asset"].search_count([])`,
   `.search([("asset_type", "=", "laptop")]).mapped("name")`, `.find_warranty_expiring(365)`. "Nothing is saved until
   `env.cr.commit()`; `exit()` without it throws it away."
3. `git checkout m3-step-6`. Show the report file: an action and a template. `update`. On the asset form: Print > Asset
   Sheet. The PDF opens. "HTML with `t-` attributes, then wkhtmltopdf. `docs` is what you printed."
4. If late: show the PDF and the two files, skip the shell.

## Block 9, 9:48 to 9:56: the hand-off (never dropped)

1. **The question.** "4Ps needs a well-being level on every household. Which file do we start with?" Take answers; most
   say a new model. Open Registry > Groups, a household: dozens of columns from several modules, the table from block 2.
   "A new `dswd.household` means two tables, two forms, two access files, and no link to programs. At ten you add one
   column to this table instead."
2. **The Selection, resolved.** Add `("tablet", "Tablet")` to `asset_type` live. `./odoo-project update`. Show it in the
   form. "One word cost a code change, a release, and an update on every server. In OpenSPP a code list is data:
   Settings > Vocabularies. That is the first file you see at ten."
3. **The table.** Last slide, back of the handout: today versus 10:00, row by row. Close: "Same files, same loop, same
   `test`. Three swaps, each one line."

## Block 10, 9:56 to 10:00: close

1. "Read your test summary line." Hands up for `0 failed`.
2. "Leave the stack running; Module 4 needs nothing from it. Ten-minute break; helpers, see me."

## If the demo machine fails

- Any step: `git checkout m3-step-N` restores a known-good tree; `./odoo-project update` or `install` restores the
  database state.
- Docker gone: the recording for the current block, with the handout code on screen.
- Projector gone: the handout has every file; run the session from paper.

## Commands used in this session

```bash
./odoo-project start                   # before the session; --profile dev if 8069 is busy
./odoo-project install dswd_asset      # block 3, everyone
./odoo-project update                  # after each step on the demo machine
./odoo-project logs                    # Loading module ..., have no access rules
./odoo-project test dswd_asset         # block 8, everyone
git checkout m3-step-N                 # N from 0 to 6, demo machine only
```
