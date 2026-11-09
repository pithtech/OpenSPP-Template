# Module 6, Exercise 2: Extending, `dswd_listahanan`

Day 3, about 30 minutes, in pairs. Swap who types.

**The 4Ps request.** 4Ps households are identified from Listahanan, the national household targeting system, and the
production registry keeps a Listahanan ID on every household. Add it to the household in OpenSPP, and make sure no two
households can share one.

**You build** a module, `dswd_listahanan`, that extends OpenSPP's household instead of creating a new table, the way
Module 4 built `dswd_wellbeing`. **You copy from** `dswd_wellbeing` in your repository.

**Done when** you can show all three:

1. `.\odoo-project install dswd_listahanan` prints `Install complete. Restarting Odoo...`
2. `.\odoo-project test dswd_listahanan` prints `0 failed, 0 error(s) of 3 tests`
3. The household's Profile page shows a **Listahanan** section, and a second household with the same ID is refused.

## Step 1: the folder (3 min)

```powershell
Copy-Item -Recurse dswd_wellbeing dswd_listahanan
Remove-Item -Recurse dswd_listahanan\data
Rename-Item dswd_listahanan\tests\test_wellbeing.py test_listahanan.py
```

This module has no vocabulary, so the `data` folder goes. Fix `tests/__init__.py` to import the renamed file.

## Step 2: the manifest (2 min)

| Key       | Value                                                      |
| --------- | ---------------------------------------------------------- |
| `name`    | DSWD 4Ps: Listahanan Household ID                          |
| `depends` | `spp_registry` only: no vocabulary this time               |
| `data`    | the access file and the views file (the data file is gone) |

Rewrite `readme/DESCRIPTION.md` in two sentences of your own. The access file stays as it is: header only. You add a
field to an existing model, not a new model, so there is no new access row.

## Step 3: the field (8 min)

`models/res_partner.py` keeps `_inherit = "res.partner"` and gets one field instead of the well-being level:

| Field                | Type | Label         | Notes                                                  |
| -------------------- | ---- | ------------- | ------------------------------------------------------ |
| `dswd_listahanan_id` | Char | Listahanan ID | `copy=False` (a duplicated household must not keep it) |

Then the rule: no two households may have the same Listahanan ID. Here the right tool is a **database constraint**, not
a Python check: the database refuses the duplicate even if two users save at the same moment. Participant guide 3.8
shows the Odoo 19 form, `models.Constraint("UNIQUE(...)", "message")`, as a class attribute next to the fields. Write a
message the user can read.

Delete the well-being constant, the old field and its `@api.constrains` method.

## Step 4: the view (7 min)

`views/res_partner_views.xml` keeps the same parent view, `spp_registry.view_individuals_form`, and the same anchor,
`//group[@name='group_tags_section']`. Change:

- the record id and the view's `name` to this module's (for example `res.partner.form.dswd.listahanan`);
- the new group's `name` to `dswd_listahanan_section` and its `string` to **Listahanan**;
- the field to `dswd_listahanan_id`, still with `readonly="disabled"` like the fields around it. A Char field needs no
  `options`.

Why the field shows on households only: the anchor sits on the household Profile page, which OpenSPP hides for
individuals. You do not need an `invisible` condition.

## Step 5: the tests (6 min)

`tests/test_listahanan.py` keeps `RegistryCommon` (it gives you `self.group`, a household) and has three tests:

1. A household takes the ID `LH-0001` and reads it back.
2. A second household with the same ID is refused.
3. The household form's arch contains `name="dswd_listahanan_id"` (copy `test_level_shows_on_the_household_form`).

The second test cannot be guessed, because a database constraint raises the database's error, not a `ValidationError`.
The pattern:

```python
from psycopg2 import IntegrityError

from odoo.tools import mute_logger

# inside the test, after creating a second household `other`:
with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError), self.cr.savepoint():
    other.dswd_listahanan_id = "LH-0001"
    other.flush_recordset()
```

`flush_recordset()` sends the write to the database now, so the error happens inside the `with`; the savepoint keeps the
test's transaction usable; `mute_logger` hides the expected error from the log.

## Step 6: install, test, look (4 min)

```powershell
.\odoo-project install dswd_listahanan
.\odoo-project test dswd_listahanan
```

In the browser: **Registry > Browse All (Audit) > All Groups**, open a household, **Profile** page: the **Listahanan**
section. Give it `LH-0001` and save. Open another household, give it the same ID and save. The dialog says:

```
The operation cannot be completed: <your message>
```

Open an individual: no Listahanan section.

## Step 7: commit (1 min)

On the `module6` branch you created before the session (participant guide 6.2):

```powershell
git add dswd_listahanan
git status
git commit -m "feat(listahanan): add the Listahanan household ID"
```

`git add dswd_listahanan` adds this module's folder only. The pre-commit hooks run; if one changes a file, run `git add`
again and commit again.

At 9:55, whatever step you are on, commit what works, then push and open the pull request: exercise 3, step 7.

## If something goes wrong

`test` may print only `CRITICAL: ... Failed to load registry` or `Couldn't load module`. The cause is in the full log it
names on its last lines: open that file and search for `Error`.

| You see                                                            | Look at                                                                 |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `Element '<xpath expr=...>' cannot be located in parent view`      | the anchor: compare it letter by letter with step 4                     |
| `Field "dswd_listahanan_id" does not exist in model "res.partner"` | `models/__init__.py` imports the model file; the field name in the view |
| `install` errors on `data/vocabulary_well_being_level.xml`         | the manifest still lists the data file you deleted                      |
| The second test fails with `IntegrityError not raised`             | the constraint line, or `flush_recordset()` missing inside the `with`   |
| A test still mentions the well-being level                         | delete the tests copied from `dswd_wellbeing` that are not yours        |

## Stretch

- The Listahanan ID as an optional column on the household list: inherit `spp_registry.view_groups_list_tree_base` and
  add the field after `registration_date` with `optional="show"`. A test that the list's arch contains it.
- Make the ID searchable from the household search box.
