# Module 4 Quiz Bank

Ten items mapped to the five Module 4 objectives. Items 1 to 5 are the paired pre-test and post-test set (ask the same
five before Day 2 and after Module 4); items 6 to 10 are spares for the post-test or for Module 6. Answers are in
`quiz-answers.md`.

Objectives: (1) module anatomy and the manifest rule, (2) the extension pattern, (3) view inheritance and its error, (4)
reading a log excerpt, (5) running tests and reading the summary.

---

**1.** (Objective 1) A new file `data/vocabulary_well_being_level.xml` exists, the module installs without any error,
but the vocabulary is not in Settings > Vocabularies. What is the most likely cause?

- a) A row is missing in `security/ir.model.access.csv`
- b) The file is not listed under `data` in `__manifest__.py`
- c) The model uses `_name` instead of `_inherit`
- d) `tests/__init__.py` is missing

**2.** (Objective 2) 4Ps needs a well-being level on every household. Which approach is correct?

- a) A new model with `_name = "res.partner"`
- b) `_inherit = "res.partner"` and a field named `dswd_well_being_level_id`
- c) A new model `dswd.household` with the field, linked to the registrant
- d) Add the field to `vendor/openspp/spp_registry/models/res_partner.py`

**3.** (Objective 2) In one sentence: why does the field point to `spp.vocabulary.code` instead of being a
`fields.Selection` with three fixed values?

**4.** (Objectives 3 and 4) An update fails with:

```
odoo.exceptions.ValidationError: Element '<xpath expr="//group[@name='group_tag_section']">' cannot be located in parent view
```

Which file in your module do you open, and what do you compare it against?

**5.** (Objective 5) Write the command that runs the tests of `dswd_wellbeing`, and name the line in its output that
tells you whether the tests passed.

**6.** (Objective 1) Put these files in the order Odoo needs them to make a vocabulary code appear in a dropdown on the
household form: `views/res_partner_views.xml`, `data/vocabulary_well_being_level.xml`, `models/res_partner.py`,
`__manifest__.py`.

**7.** (Objective 1) `models/res_partner.py` defines the field correctly, the module installs cleanly, but Settings >
Technical > Fields does not list `dswd_well_being_level_id`. Which one-line file is the usual culprit?

**8.** (Objective 4) After editing a code's `display` text in `data/vocabulary_well_being_level.xml` and running
`./odoo-project update`, the old text still shows. Why, and what are the two ways to see the new text?

**9.** (Objective 2) The dropdown on the form only offers well-being codes, yet a script writes a gender code into the
field and it is saved. What is missing, and why does the field's `domain` not prevent it?

**10.** (Objective 5) `./odoo-project update` finishes cleanly but your brand-new module is still "uninstalled". Which
command installs it, and what does `update` actually do?
