# Module 6, Exercise 3: Customization, `dswd_id_types`

Day 3, about 20 minutes, in pairs. Swap who types. If the session ends before you finish, finish it afterwards: the
sheet is complete on its own.

**The 4Ps request.** 4Ps identifies members with PhilSys, the Philippine national ID. Add PhilSys to the ID types
OpenSPP offers on a registrant, with a format check, so a mistyped number is refused.

**You build** a module, `dswd_id_types`, with **no model and no view**: one record of data in a vocabulary OpenSPP
already has. OpenSPP's own code does the format check. **You copy from** `dswd_wellbeing` (Module 4 step 1: a vocabulary
as data) and read one upstream file for the record's shape.

**Done when** you can show all three:

1. `.\odoo-project install dswd_id_types` ends with `Install complete. Restarting Odoo...`
2. `.\odoo-project test dswd_id_types` ends with `0 failed, 0 error(s) of 2 tests`
3. On an individual's **Identity** page, **PhilSys** is in the ID type list, and the number `12345678` is refused.

## Step 1: the folder (3 min)

```powershell
Copy-Item -Recurse dswd_wellbeing dswd_id_types
Remove-Item -Recurse dswd_id_types\models, dswd_id_types\views
Remove-Item dswd_id_types\data\vocabulary_well_being_level.xml
Rename-Item dswd_id_types\tests\test_wellbeing.py test_id_types.py
```

The module's own `__init__.py` must no longer import `models` (the folder is gone): leave only the header comment.
Fix `tests/__init__.py` to import the renamed file.

## Step 2: the manifest (2 min)

| Key       | Value                                                                  |
| --------- | ---------------------------------------------------------------------- |
| `name`    | DSWD 4Ps: Philippine ID Types                                          |
| `depends` | `spp_registry` (registrant IDs), `spp_vocabulary` (the ID Type list)   |
| `data`    | the access file (header only, as before) and `data/id_types.xml`       |

## Step 3: the data (7 min)

Create `data/id_types.xml`. Read the shape of an ID type first:
`upstream\openspp\spp_vocabulary\data\vocabulary_id_type.xml` defines the vocabulary (`vocab_id_type`) and its codes.

Your file has `noupdate="1"`, like `dswd_wellbeing`'s data file, and one `spp.vocabulary.code` record:

| Field           | Value                                                                       |
| --------------- | --------------------------------------------------------------------------- |
| record id       | `code_id_type_philsys`                                                      |
| `vocabulary_id` | a reference to OpenSPP's ID Type vocabulary: `spp_vocabulary.vocab_id_type` |
| `code`          | `philsys`                                                                   |
| `display`       | `PhilSys`                                                                   |
| `definition`    | one sentence: what the ID is                                                |
| `target_type`   | `individual` (households do not have one)                                   |
| `id_validation` | `^\d{4}-\d{4}-\d{4}-\d{4}$` (four groups of four digits)                    |

Hint: the reference goes in a `ref` attribute, because the vocabulary is another module's record.

Why `display` is "PhilSys" and not "PhilSys ID": OpenSPP's error message adds "ID" itself.

## Step 4: the tests (5 min)

`tests/test_id_types.py` keeps `RegistryCommon` (it gives you `self.individual_a`) and has two tests on the model
`spp.registry.id`, whose fields are `partner_id`, `id_type_id` and `value`:

1. An ID with the value `1234-5678-9012-3456` is created and keeps its value.
2. Creating one with the value `12345678` raises `ValidationError`.

Hint: your record is `self.env.ref("dswd_id_types.code_id_type_philsys")`. The `ValidationError` comes from OpenSPP's
constraint on `spp.registry.id`, which checks every value against the type's `id_validation`.

## Step 5: install, test, look (3 min)

```powershell
.\odoo-project install dswd_id_types
.\odoo-project test dswd_id_types
```

In the browser: **Registry > Browse All (Audit) > All Individuals**, open (or create) an individual, **Identity** page,
add a line: ID type **PhilSys**, value `12345678`. The dialog says:

```
The provided PhilSys ID '12345678' is invalid.
```

Change the value to `1234-5678-9012-3456`: it saves.

## If something goes wrong

`test` may print only `CRITICAL: ... Failed to load registry` or `Couldn't load module`. The cause is in the full log
it names on its last lines: open that file and search for `Error`.

| You see                                                                     | Look at                                                                                         |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `ImportError: cannot import name 'models' from partially initialized module 'odoo.addons.dswd_id_types'` (it suggests a circular import; it is not one) | the module's `__init__.py` still imports `models`, and the folder is gone |
| `Code 'philsys' already exists in vocabulary 'ID Type'.`                     | someone added PhilSys by hand in Settings > Vocabularies; remove that manual code, or use a fresh database |
| `test` says `No tests were executed`                                                    | `tests/__init__.py` does not import your test file                                              |
| `External ID not found in the system: dswd_id_types.code_id_type_philsys`   | the record id, or the data file missing from the manifest                                       |
| PhilSys is not in the ID type list                                          | `target_type`; and use the Identity page of an individual, not a household                      |
| You added PhilSys under **Studio > Settings > Registry > ID Types** and it never shows on the Identity page | that screen edits a different model (`spp.id.type`); the Identity page uses the ID Type vocabulary, which is what this module adds to |

## Stretch

- PhilHealth as a second code (its number is twelve digits: `^\d{12}$`), with a test.
- The 4Ps household ID card number, for households (`target_type` `group`), with your own format.
