# Module 4 Troubleshooting Drill: Answer Key

Debrief order: C first (the silent one teaches the most), then A, then B, then D if any pair reached it.

## Excerpt A: invalid selection value in a data file

- **File**: `data/vocabulary_well_being_level.xml`, line 10 (the `ParseError` names the file and line; the `ValueError`
  names the field, `spp.vocabulary.domain`, and the bad value).
- **Compare against**: the `domain` field's allowed values in `upstream/openspp/spp_vocabulary/models/vocabulary.py`
  (`core`, `social_assistance`, `social_insurance`, `labor`, `disability`, `agriculture`, `health`, `education`).
- **Fix**: `<field name="domain">social_assistance</field>`.
- Teaching point: read from the bottom of the traceback up; the first line that names a file in your module is where you
  go. Lint cannot catch this: it is a value, not syntax.

## Excerpt B: XPath anchor does not exist in the upstream view

- **File**: `views/res_partner_views.xml`, the `xpath` line. The context block even gives the xml id of your view.
  `&#39;` in the message is a quote: Odoo escapes the attribute values.
- **Compare against**: the named groups in the upstream form: search `name="group_` in
  `upstream/openspp/spp_registry/views/individual_views.xml` (VS Code Ctrl+F, or PowerShell
  `Select-String -Path upstream\openspp\spp_registry\views\individual_views.xml -Pattern 'name="group_'`).
- **Fix**: `group_tag_section` to `group_tags_section`.
- Teaching point: anchors are names, and names live upstream. Always open the upstream view before writing the XPath.

## Excerpt C: data file not listed in the manifest

- **File**: `__manifest__.py`. The module "loaded" but the log shows only two files loading: the access csv and the
  view. `data/vocabulary_well_being_level.xml` never appears.
- **Look for**: the `data` list in `dswd_wellbeing/__manifest__.py`; it has no `vocabulary_` line.
- **Fix**: add `"data/vocabulary_well_being_level.xml",` to `data`, before the view.
- Teaching point: the only reason this was caught is the test. Without tests the vocabulary would simply be absent and
  someone would notice in the UI days later. "A file not listed in the manifest does not exist."

## Bonus D: field defined but never imported

- **File**: `models/__init__.py` (or the root `__init__.py`). The class exists in `models/res_partner.py`, but Python
  never imports the file, so Odoo never registers the field.
- **Look for**: `from . import res_partner` in `models/__init__.py` and `from . import models` in `__init__.py`.
- **Fix**: add the missing import line.
- Why step 2 did not show it: at step 2 there was no view yet. A missing import on its own raises nothing; the field is
  simply absent (Settings > Technical > Fields). The error only appears once a view, a test or a data file refers to the
  field. That is why the handout lists it as a "silent" mistake.
