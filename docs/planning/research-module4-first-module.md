# Research: First Training Module (Day 2, Module 4) on `spp_vocabulary`

> **Status**: research, awaiting Edwin's review (2026-11-08). No code written yet.
> **Purpose**: pick the simplest `dswd_*` module that customises `spp_vocabulary` for 4Ps, to be presented as the first
> topic of Module 4 ("Developing Custom Modules and Extending Odoo Models").
> **Sources**: `vendor/openspp/` at `OPENSPP_REF=2026.09`; the production repo
> `~/OpenSPP/dswd-4ps-dp-openspp-v2-module` (Newlogic, proprietary, read for reference only); the DSWD program of
> activities PDF (`~/Documents/DSWD-4PS-Training-11-2026/`).

---

## 1. Training context

From the program of activities:

| When                     | Module                                                              | Speaker |
| ------------------------ | ------------------------------------------------------------------- | ------- |
| Day 2, 8:30 - 10:00      | Module 3: Introduction to Odoo                                      | Edwin   |
| **Day 2, 10:00 - 12:00** | **Module 4: Developing Custom Modules and Extending Odoo Models**   | Edwin   |
| Day 2, 1:00 - 5:00       | Module 5: DSWD Specific / 4Ps Forward implementation of OpenSPP     | Edwin   |
| Day 3, 8:30 - 10:30      | Module 6: Hands-on Activity: Exploring Odoo and OpenSPP             | Edwin + participants |

Audience: 18 Regional IT Officers, 36 Computer Maintenance Technologists, 33 NPMO IT personnel (87 DSWD technical
staff), plus executives and resource persons. Methodology: lectures and demonstrations, hands-on coding workshops,
pre-test and post-test. Level 3 evaluation targets "Tier-2/Tier-3 troubleshooting", so participants should leave able
to read a module and change it, not design one.

Module 4 has two hours and follows directly after "Introduction to Odoo", so participants will have just seen models,
views, and the module concept. The first module must therefore show the **complete anatomy of a module** (manifest,
data, model extension, view extension, security, test) on something they recognise from their own program, in a form
that fits on one or two screens per file.

## 2. What `spp_vocabulary` provides (verified in `vendor/openspp/spp_vocabulary`, 2026.09)

| Model                            | Role                                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `spp.vocabulary`                 | A named code list with a unique `namespace_uri`, a `domain` selection, `is_system`, `is_hierarchical`.     |
| `spp.vocabulary.code`            | One code: `code`, `display`, `definition`, `sequence`, computed `uri` (`namespace#code`), `is_local`, `target_type`, `id_validation` (regex, for ID types), lifecycle (`active`, `deprecated`, `replaced_by_id`). |
| `spp.vocabulary.mapping`         | Code-to-code mapping between vocabularies.                                                                 |
| `spp.vocabulary.concept.group`   | Semantic grouping of codes (e.g. "head of household") used by CEL expressions.                             |
| `spp.deployment.profile` / `spp.vocabulary.selection` | Per-deployment subset of active codes.                                                |

Facts that matter for a small module:

- `domain` is a fixed `Selection`: `core`, `social_assistance`, `social_insurance`, `labor`, `disability`,
  `agriculture`, `health`, `education`. Any other value fails to load.
- `namespace_uri` is unique; the code `uri` is unique and computed as `{namespace_uri}#{code}`.
- `is_system=True` vocabularies lock their shipped codes against UI edits. Module data files still load (the
  `install_xmlid` context bypasses the lock), so a `dswd_*` module **can add codes to an upstream system vocabulary**
  such as ID Type. Admins add further codes through "Add Manual Code" (`is_local=True`).
- Lookups: `self.env["spp.vocabulary.code"].get_code(namespace_uri, code)` and `resolve_by_uri(uri)`, both ORM-cached.
- Menus: root `spp_vocabulary.menu_vocabulary_root` ("Vocabularies") under `base.menu_administration` (Settings), with
  children `menu_vocabulary` ("Manage Vocabularies"), `menu_vocabulary_code` ("All Codes"), mappings, concept groups,
  deployment profiles, selections.
- Shipped vocabularies include gender, relationship, group type, group membership type, marital status, occupation
  (ISCO-08), education level, ethnocultural, housing, economic activity, language, country, currency, religion, ID type
  (`urn:openspp:vocab:id-type`: national_id, passport, tax_id, birth_certificate), change-request document types,
  disability.
- Upstream tests: `odoo.addons.spp_registry.tests.common.RegistryCommon` creates a household (`is_group=True`), two
  individuals, and looks up the `head` membership code; `_make_user(login, group_xmlids)` builds a user with groups.

## 3. How the production 4Ps modules use vocabularies

`dswd_4ps_registry` (Newlogic) depends on `spp_vocabulary` and ships **26 vocabulary data files**: client status (32
statuses in 9 categories, hierarchical), member status, pregnancy status, disability type, IP group (about 2,000
codes), payment mode classification, account type, transaction account group, grantee change reason, change head
reason, no parent reason, set group (batch/cohort, e.g. `1A` to `12V`), poverty status, IP status, well-being level,
marital status, name suffix, education, grade levels, employment and employer types, DOLE occupations, PRC exams.

Patterns worth copying into the training module:

- Vocabularies are declared first in one file (`data/vocabulary_namespaces.xml`), codes in separate files, all
  `noupdate="1"`, all `is_system=True`.
- Namespaces follow `urn:dswd:4ps:{name}` (`urn:dswd:4ps:well-being-level`, `urn:dswd:4ps:set-group`); national
  standards use `urn:ph:{agency}:{name}` (`urn:ph:dole:occupations`, `urn:ph:prc:examinations`).
- Fields on `res.partner` are `Many2one("spp.vocabulary.code")` with a `domain` on `namespace_uri`; code lookups in
  Python use `get_code("urn:dswd:4ps:member-status", "1")`.
- Philippine ID types are added as codes on the upstream ID Type vocabulary with a regex: PhilSys
  `^\d{4}-\d{4}-\d{4}-\d{4}$`, 4Ps ID card `^.{24}$`, PhilHealth `^\d{12}$` (`data/id_types.xml`).
- The household form is extended by inheriting `spp_registry.view_individuals_form` (one form serves individuals and
  groups; the group notebook is `group_detail` with pages `group_profile`, `group_identity`, `group_participation`,
  `group_history`, and named groups such as `group_header_section` and `group_tags_section`).

The well-being vocabulary is shipped by `dswd_4ps_registry` but no model in that module references it (it is used by
the SWDI side), which makes it a clean, uncontested example to re-create in the training.

## 4. Candidate first modules

| Option | What it does | Files | Teaches | Risk |
| --- | --- | --- | --- | --- |
| **A. `dswd_wellbeing`** (recommended) | Adds the "4Ps Well-Being Level" vocabulary (3 codes: Survival, Subsistence, Self-Sufficient) and a `dswd_well_being_level_id` field on households, shown on the household Profile page. | manifest, 1 data XML, 1 model, 1 view, ACL note, 1 test, DESCRIPTION.md | The whole module anatomy: new vocabulary data, `_inherit` of `res.partner`, Many2one with namespace domain, view inheritance by XPath on a named upstream group, `get_code` lookup in a test. | Very low. Three codes keep the data file readable on a slide. |
| B. `dswd_id_types` | Adds PhilSys, 4Ps ID and PhilHealth as codes on the upstream ID Type vocabulary, with regex validation. | manifest, 1 data XML, 1 test, DESCRIPTION.md | Extending an upstream *system* vocabulary from a module; regex validation visible in the registrant ID tab. | Data-only, so no model or view extension; weaker fit for "extending Odoo models". |
| C. `dswd_household_status` | A trimmed client status vocabulary (5 of the 32 statuses) and a status field on households. | same as A | Same as A, plus a glimpse of hierarchical codes if categories are kept. | Picking 5 of 32 invites "why not the real list" questions; the real list is too long to show. |

**Recommendation: A for the live demo, B as the participants' exercise.** A is the smallest module that still touches
model, view, data, security and tests, and the three-level well-being scale (SWDI / Kilos-Unlad) is something every
RITO and CMT has heard of. B is a pure data change that participants can complete in Module 6 in under 30 minutes, and
it reuses what they saw in A. C stays as a possible later lab once programs and statuses are covered in Module 5.

### Proposed shape of `dswd_wellbeing`

```
dswd_wellbeing/
├── __init__.py                       # imports models
├── __manifest__.py                   # depends: spp_registry, spp_vocabulary; data: data + views
├── data/vocabulary_well_being_level.xml   # 1 vocabulary + 3 codes, noupdate, urn:dswd:4ps:well-being-level
├── models/__init__.py
├── models/res_partner.py             # dswd_well_being_level_id = Many2one(spp.vocabulary.code, domain on namespace)
├── views/res_partner_views.xml       # inherit spp_registry.view_individuals_form, add field after group_tags_section
├── security/ir.model.access.csv      # no new model, so header only? -> see open question 2
├── tests/__init__.py
├── tests/test_wellbeing.py           # RegistryCommon: codes exist, field accepts a code; a wrong-vocabulary code needs an @api.constrains (a Many2one domain only filters the UI)
└── readme/DESCRIPTION.md
```

Demo flow for the two hours (indicative):

1. 10 min: what a vocabulary is in OpenSPP; show Settings > Vocabularies > Manage Vocabularies with the shipped lists.
2. 20 min: the data file. Add the vocabulary and three codes; install; show them in the UI.
3. 25 min: the model. Add the Many2one on `res.partner`; explain `_inherit`, `dswd_` prefix, namespace domain.
4. 20 min: the view. XPath into the household Profile page; show the field on a household; set a value.
5. 15 min: the test. Run `./odoo-project test dswd_wellbeing`; read the output together.
6. 15 min: Claude Code. Ask it to add a fourth code or a list-view column, review the diff.
7. 15 min: buffer, questions, hand-out of exercise B.

## 5. Findings that affect existing template docs

These are inaccuracies in `docs/guides/module-development.md` that the first module would otherwise copy:

1. The vocabulary example uses `<field name="domain">administrative</field>`; `administrative` is not a valid value
   of the `domain` selection (section 2). It should be `social_assistance` or `core`.
2. The configuration menu section says to hang menus under `spp_vocabulary.menu_spp_vocabulary_configuration`. That id
   does not exist in 2026.09; the root is `spp_vocabulary.menu_vocabulary_root`.
3. The guide recommends `urn:dswd:vocab:{name}` for new namespaces. The production 4Ps modules use
   `urn:dswd:4ps:{name}`. Using the production pattern in the training makes the code transferable.

Proposed handling: fix all three in the same PR as the module, since the module is the first consumer of that guide.

## 6. Open questions for Edwin

1. **Option A as the first module, B as the exercise?** Or would you rather present B (data only) first and A second?
2. **ACL file**: the module adds no new model, so `ir.model.access.csv` would be empty. The project checklist says the
   file must exist. I suggest shipping it with a header line only and saying so in the demo (shows where ACLs go), or
   omitting it and adding a sentence to the checklist. Your preference?
3. **Module name**: `dswd_wellbeing` (short to type live) versus `dswd_household_wellbeing` (clearer). The naming rule
   allows both.
4. **Codes as `1`, `2`, `3`** (production) or `survival`, `subsistence`, `self_sufficient` (readable)? Production
   uses numeric codes to match the legacy PPIS; readable codes are easier on a slide. I lean readable, with the
   numeric legacy value in `definition`.
5. **Where the field shows**: household Profile page after the tags section (production puts its 4Ps fields there),
   or a new "4Ps" page in the group notebook? The first is one XPath; the second is more visible in the demo.
6. **Should `docs/planning/` stay visible to participants?** Still open from the template plan (section 9, item 2).
