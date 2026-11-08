# Day 3 Exercise: Extend `dswd_wellbeing`

Pick the tier that matches your setup. Finish one tier before starting the next. Ask your pair first, then your row,
then the trainer.

Before you start, on a working laptop:

```bash
git checkout m4-step-5            # the finished module from Module 4
./odoo-project start              # or: ./odoo-project start --profile dev
./odoo-project install dswd_wellbeing
```

## Tier 1: Find the faults (no environment needed)

The folder `training/module4/dswd_wellbeing_broken/` is a copy of the module with **three planted faults**. Lint passes
on all three; Odoo does not. The copy has no `tests/` folder on purpose: the real module's tests would give two of the
faults away. For each fault, write down:

1. the file and line,
2. what you would see (a log line, an empty screen, a missing field),
3. the one-line fix.

Use the Module 4 handout: the three rules, the loop, the five mistakes. Do not run anything; read.

Checkpoint: you have three file:line pairs and three expected symptoms. Compare with your pair before the debrief.

Bonus: `./odoo-project lint` (ruff and prettier) passes on all three faults. The repo's pre-commit hooks catch exactly
one of them. Which one, and which hook? (Hint: the OCA module checks compare the files on disk with the manifest.)

## Tier 2: Show the level on the household list (environment needed)

The level shows on the household form but not on the list. Add it as an optional column.

1. Find the upstream list view:
   `grep -n 'record id="view_groups_list' upstream/openspp/spp_registry/views/group_views.xml`. You want
   `view_groups_list_tree_base`; note the field names inside its `<list>`.
2. Add a second record to `dswd_wellbeing/views/res_partner_views.xml` that inherits it and puts
   `<field name="dswd_well_being_level_id" optional="show" />` after `registration_date`.
3. `./odoo-project update`, open Registry > Groups, and show the column.
4. Add a test to `tests/test_wellbeing.py` that the list view's arch contains the field (copy the form test and change
   the view id and view type to `list`). Run `./odoo-project test dswd_wellbeing`.

Checkpoint: 6 tests pass; the column appears.

## Tier 3: Philippine ID types (stretch)

Create a second module, `dswd_id_types`, that adds `philsys` to the upstream ID Type vocabulary with a validation
pattern, and proves the pattern with a test. Step 1 of `dswd_wellbeing` is your template.

1. `__manifest__.py` depending on `spp_registry` and `spp_vocabulary`; header-only `security/ir.model.access.csv`.
2. `data/id_types.xml` with one `spp.vocabulary.code` record: `vocabulary_id` ref `spp_vocabulary.vocab_id_type`, code
   `philsys`, display "PhilSys ID", `target_type` `individual`, `id_validation` `^\d{4}-\d{4}-\d{4}-\d{4}$`.
3. A test on `RegistryCommon`: creating an `spp.registry.id` for `self.individual_a` with that type and the value
   `1234-5678-9012-3456` works; the value `12345678` raises `ValidationError` (upstream validates in a constraint).
4. `./odoo-project test dswd_id_types`, then `./odoo-project install dswd_id_types` and add the ID to a registrant in
   the Identity tab.

Checkpoint: both tests pass; an invalid number is refused in the UI.

Hints: read `upstream/openspp/spp_vocabulary/data/vocabulary_id_type.xml` for the record shape and
`upstream/openspp/spp_registry/models/reg_id.py` for the constraint. The production 4Ps module uses the same pattern for
PhilSys, the 4Ps ID card and PhilHealth.
