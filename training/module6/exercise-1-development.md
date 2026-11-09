# Module 6, Exercise 1: Development, `dswd_fds_session`

Day 3, about 40 minutes, in pairs: one types, one reads the sheet and the output. Swap at the next exercise.

**The 4Ps request.** Family Development Sessions are a monthly 4Ps condition. A municipal office wants a simple register
of the sessions it held: the topic, the date, the barangay, who facilitated, and how many attended.

**You build** a new module, `dswd_fds_session`, from scratch, the way Module 3 built `dswd_asset`. **You copy from**
`dswd_asset` in your repository: its manifest, model, views, menus, access file and tests are the pattern. Keep both
modules open side by side in VS Code.

**Done when** you can show all three:

1. `.\odoo-project install dswd_fds_session` prints `Install complete. Restarting Odoo...`
2. `.\odoo-project test dswd_fds_session` prints `0 failed, 0 error(s) of 2 tests`
3. The **FDS Sessions** tile opens, a session saves, and a negative attendee count is refused.

Read every command's output to the end. If it does not print the "complete" line, it failed, and the browser still shows
the old screens.

## Step 1: the folder (5 min)

Copy `dswd_asset` and remove what this module does not need. In PowerShell, from your repository folder:

```powershell
Copy-Item -Recurse dswd_asset dswd_fds_session
Remove-Item -Recurse dswd_fds_session\report, dswd_fds_session\security\groups.xml
Remove-Item dswd_fds_session\tests\test_access.py, dswd_fds_session\tests\test_report.py
Rename-Item dswd_fds_session\models\dswd_asset.py dswd_fds_session.py
Rename-Item dswd_fds_session\views\dswd_asset_views.xml dswd_fds_session_views.xml
Rename-Item dswd_fds_session\tests\test_dswd_asset.py test_dswd_fds_session.py
```

(Or copy, delete and rename in the VS Code Explorer.) Every file still says `dswd_asset` or `dswd.asset` inside. Steps 2
to 6 replace all of it; at the end, search the folder for `asset` (VS Code: right-click the folder, Find in Folder) and
nothing should be left.

## Step 2: the manifest (3 min)

| Key       | Value                                                                |
| --------- | -------------------------------------------------------------------- |
| `name`    | DSWD 4Ps: FDS Session Register                                       |
| `summary` | one sentence of your own                                             |
| `depends` | `base`, `spp_area` (the barangay is an OpenSPP area), `spp_registry` |
| `data`    | the access file, the views file, the menus file, in that order       |

Keep `application`, `installable` and `auto_install` as `dswd_asset` has them. Remove the lines for files you deleted.
Rewrite `readme/DESCRIPTION.md` in two sentences of your own.

## Step 3: the model (10 min)

In `models/dswd_fds_session.py` (and fix the import in `models/__init__.py`), one model:

| Name           | Value                                |
| -------------- | ------------------------------------ |
| `_name`        | `dswd.fds.session`                   |
| `_description` | FDS Session                          |
| `_order`       | newest sessions first, then by topic |

| Field            | Type     | Label       | Notes                                        |
| ---------------- | -------- | ----------- | -------------------------------------------- |
| `name`           | Char     | Topic       | required                                     |
| `session_date`   | Date     |             | required; defaults to today                  |
| `area_id`        | Many2one | Barangay    | to `spp.area`                                |
| `facilitator_id` | Many2one | Facilitator | to `res.users`; defaults to the current user |
| `attendee_count` | Integer  | Attendees   |                                              |

One rule: the number of attendees cannot be negative. Raise a `ValidationError` with a sentence the user can read.

Hints:

- `dswd_asset` already has a Many2one to `res.users` with the current user as default, and a constraint with
  `@api.constrains`. Copy their shape.
- A date that defaults to today: `default=fields.Date.context_today`.
- Delete everything from `dswd_asset` you do not need: the Selection, the computed field, the button method, the search
  method.

## Step 4: who may use it (3 min)

`security/ir.model.access.csv` keeps its header and gets three rows, for the model id `model_dswd_fds_session`:

| Group                                 | Read | Write | Create | Delete |
| ------------------------------------- | ---- | ----- | ------ | ------ |
| `base.group_system`                   | 1    | 1     | 1      | 1      |
| `spp_registry.group_registry_viewer`  | 1    | 0     | 0      | 0      |
| `spp_registry.group_registry_officer` | 1    | 1     | 1      | 0      |

This module uses OpenSPP's registry groups instead of creating its own, so there is no `groups.xml`.

## Step 5: views and menus (10 min)

In `views/dswd_fds_session_views.xml`, change every record id, `name`, `model` and field to this module's:

- **List**: date, topic, barangay, facilitator, attendees.
- **Form**: the topic as the title; a group "When and where" (date, barangay) and a group "Who" (facilitator,
  attendees).
- **Search**: search by topic and by barangay; a "Group By" barangay.
- **Action**: name "FDS Sessions", the model `dswd.fds.session`, list and form.

Delete the **Assign to me** button from the form header: its method is gone, and its group belongs to `dswd_asset`.

In `views/menus.xml`: a top-level menu (the tile) named **FDS Sessions** with this module's icon
(`dswd_fds_session,static/description/icon.png`, the file you copied), and under it a menu **Sessions** that opens the
action.

Hint: the action must be defined before a menu that uses it; the manifest loads the views file before the menus file.

## Step 6: the tests (5 min)

`tests/test_dswd_fds_session.py`, one test class with two tests (and fix the import in `tests/__init__.py`):

1. A new session (create it with only a topic) is dated today, has the current user as facilitator, and 0 attendees.
2. Setting the attendee count to -1 raises `ValidationError`.

Hint: `dswd_asset`'s `test_defaults` and `test_warranty_before_purchase_is_refused` are the two shapes. Today, the way
the model computes it: `fields.Date.context_today(record)`.

## Step 7: install, test, look (4 min)

```powershell
.\odoo-project install dswd_fds_session
.\odoo-project test dswd_fds_session
```

Then refresh the browser: the **FDS Sessions** tile is on the home screen. Create a session, save it, then set the
attendees to `-3` and save: the dialog shows your sentence.

## Step 8: commit (1 min)

On the `module6` branch you created before the session (participant guide 6.2):

```powershell
git add dswd_fds_session
git status
git commit -m "feat(fds): register FDS sessions"
```

`git add dswd_fds_session` adds this module's folder only. The pre-commit hooks run; if one changes a file, run
`git add` again and commit again.

At 9:55, whatever step you are on, commit what works, then push and open the pull request: exercise 3, step 7.

## If something goes wrong

`test` may print only `CRITICAL: ... Failed to load registry` or `Couldn't load module`. The cause is in the full log it
names on its last lines: open that file and search for `Error`.

| You see                                                                             | Look at                                                                         |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `install` ends with an error naming a file in `dswd_fds_session`                    | that file and line; the last lines of the output say what is wrong              |
| `FileNotFoundError: [Errno 2] No such file or directory: '.../security/groups.xml'` | the manifest still lists a file you deleted or renamed                          |
| `Field "..." does not exist in model "dswd.fds.session"`                            | a view still uses a field from `dswd_asset`                                     |
| `No matching record found for external id`                                          | an id in the access file or a menu (`model_dswd_fds_session`, the action's id)  |
| Install completes but there is no tile                                              | the access file: a model nobody may read has its menu hidden (Module 3, step 2) |
| `test` says `No tests were executed`                                                | `tests/__init__.py` does not import your test file                              |

## Stretch

- A filter **This month** in the search view.
- A third test: a session without a topic cannot be saved.
- Show the facilitator with the avatar widget, as `dswd_asset` shows the custodian.
