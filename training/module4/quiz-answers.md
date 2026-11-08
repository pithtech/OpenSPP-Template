# Module 4 Quiz Answers

**1.** b. A data file Odoo is not told about in the manifest does not exist to Odoo. No error is raised.

**2.** b. Attributes of an existing OpenSPP record go on the upstream model with `_inherit`, with a `dswd_` prefix.
`_name = "res.partner"` would redefine the model; a separate `dswd.household` model duplicates the registrant; editing
`upstream/openspp/` is never allowed (it is overwritten on the next release).

**3.** Codes can be added, renamed, deprecated or limited per deployment through Settings > Vocabularies without a code
change or a new release, and each code has a namespace URI other systems can match. Accept any answer with "without
changing code" or "configurable per deployment".

**4.** Open `views/res_partner_views.xml` in your module and compare the anchor in the XPath against the group names in
the upstream form, `upstream/openspp/spp_registry/views/individual_views.xml` (the household groups are named `group_*`;
here `group_tags_section` was misspelled).

**5.** `./odoo-project test dswd_wellbeing`. The summary line reads like `0 failed, 0 error(s) of 5 tests`; the
`Full log:` line gives the file to open when it is not zero.

**6.** `__manifest__.py` (declares the module and lists the files), `models/res_partner.py` (the field exists),
`data/vocabulary_well_being_level.xml` (the codes exist), `views/res_partner_views.xml` (the field is shown). Odoo loads
the Python models before any data file. Accept data and model in either order; the manifest must be first and the view
last.

**7.** `models/__init__.py` (or the root `__init__.py` that imports `models`). A missing import gives no error, only a
missing field.

**8.** The data file is `noupdate="1"`: records loaded once on install are never rewritten by `update`. To see the new
text: start from a fresh database (`./odoo-project stop -v -y`, then `start` and `install dswd_wellbeing`); on a
database that must keep its data, a migration script writes the new value. Deleting the code is not possible here:
shipped codes of a system vocabulary are protected, and deleting only the External Identifier makes the next `update`
try to create the code again and fail because the code already exists.

**9.** An `@api.constrains` on the field that checks the code's namespace. A Many2one `domain` only filters what the
dropdown shows; writes from code, imports and the API bypass it.

**10.** `./odoo-project install dswd_wellbeing`. `update` runs click-odoo-update, which only upgrades modules that are
already installed and whose files changed.
