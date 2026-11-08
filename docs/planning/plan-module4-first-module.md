# Implementation Plan: Module 4 first module, `install` command, guide fixes

> **Status**: approved design ([module4-training-design.md](module4-training-design.md)), Edwin 2026-11-08: "go with
> the defaults and add the install command". This plan covers the code and doc changes; the training materials
> (runbook, slides, handouts, drill, quiz, broken copy) are a separate round.
> **Branch**: `feat/module4-dswd-wellbeing`, one PR, commits per step so each demo step has a tag.

---

## A. CLI `install` command

**Why**: `./odoo-project update` runs click-odoo-update, which only upgrades modules that are already installed. Nothing
installs a new module into the running database except the Apps UI or a fresh start with `ODOO_INIT_MODULES`.

**Behaviour**: `./odoo-project install <module> [<module> ...] [--db odoo]`

1. Find the running Odoo service (`_find_running_odoo`); exit with the same hint as `update` if none.
2. `docker compose exec <service> odoo -d <db> -i <modules> --stop-after-init --no-http` (the image sets `ODOO_RC`, so
   the rendered config supplies the addons path and database credentials, exactly as `click-odoo-update` relies on).
3. Restart the service and print the URL, as `update` does.
4. Argument completion with `_module_completer`, alias `i`.

**Tests first** (`tests/test_cli.py`, new `TestInstall`): registered in the command set; the exec call contains
`odoo`, `-i`, the joined module list and `--stop-after-init`; a restart follows; no container running exits 1 with the
start hint. **Docs**: command table in `docs/guides/odoo-project-cli.md`, the README quick start, and a sentence in
`docs/guides/extending-openspp.md` where the module is first installed. Check `tests/test_docs.py` for a command list
assertion and extend it.

Commit: `feat(cli): add install for new modules on a running database`.

## B. `dswd_wellbeing` module, six tagged steps

Each step is one commit and one tag `m4-step-N`; every step installs and its tests pass. Tests accompany the step they
cover (TDD), so the demo shows "the test says what we want" before each file; demo step 4 runs the accumulated suite.

| Step | Files | Test added | Shown in the demo |
| --- | --- | --- | --- |
| 0 | `__init__.py`, `__manifest__.py` (name "DSWD 4Ps: Household Well-Being Level", category `DSWD 4Ps/Registry`, depends `spp_registry`, `spp_vocabulary`, empty `data`), `readme/DESCRIPTION.md` stub | none | Apps > Update Apps List > Install; `Loading module dswd_wellbeing` |
| 1 | `data/vocabulary_well_being_level.xml` (vocabulary `urn:dswd:4ps:well-being-level`, `is_system`, domain `social_assistance`; codes `survival`, `subsistence`, `self_sufficient`, SWDI number in `definition`, sequence 10/20/30), manifest `data` entry, `tests/__init__.py`, `tests/test_wellbeing.py` | `get_code` returns the three codes in order; the vocabulary is a system vocabulary | Settings > Vocabularies |
| 2 | `models/__init__.py`, `models/res_partner.py` (`_inherit = "res.partner"`, `dswd_well_being_level_id` Many2one `spp.vocabulary.code`, domain on `namespace_uri`, `help`), root `__init__.py` imports models | household accepts a code and reads it back | Technical > Fields |
| 3 | `views/res_partner_views.xml` (inherit `spp_registry.view_individuals_form`, XPath after `group_tags_section`, group `dswd_4ps_section` "4Ps", field with `no_create`, `no_open`), manifest entry | the inherited view resolves (`get_view` on the form contains the field) | Household Profile page |
| 4 | `security/ir.model.access.csv` header only, manifest entry; `readme/DESCRIPTION.md` completed | none (checklist housekeeping) | `./odoo-project test dswd_wellbeing` summary |
| 5 | `@api.constrains("dswd_well_being_level_id")` rejecting a code outside the namespace | a gender code raises `ValidationError` | Written live with Claude Code, test first |

Conventions: `dswd_` field prefix; xml ids `vocab_well_being_level`, `code_well_being_*`, `view_partner_form_wellbeing`;
`@tagged("post_install", "-at_install")`; `RegistryCommon` as the base class with `tracking_disable`; `pyproject.toml`
per the scaffold if the lint requires it (check `tools/`).

Commits: `feat(dswd_wellbeing): step N, <what>`; tags after the PR merge: `git tag m4-step-N <sha>` and push tags.

### Deviations while building

- The pre-commit hook "Odoo: ACL files exist" fails any installable module without `security/ir.model.access.csv`,
  so the header-only file ships in **step 0**, not step 4. Step 4 is now the readme and the test-run moment only.
- The repo excludes `docs/` and `README.md` from every pre-commit hook (top-level `exclude`), so prettier never runs on
  the guides; `tests/test_docs.py` is the only check on them.
- Step 0 measured: `./odoo-project test dswd_wellbeing` took 2 min 31 s on Edwin's Mac including a cached image
  rebuild (the pull fails without a GHCR login).
- Steps 1 to 3 measured: about 20 s each for `./odoo-project test dswd_wellbeing` once the image exists, including
  the fresh test database. The live test run in the demo therefore fits inside its own block; no second terminal is
  needed on a machine with the image already built.

## C. Guide fixes (`docs/guides/module-development.md`, `extending-openspp.md`)

Confirmed, fix now:

1. Vocabulary example `domain` `administrative` to `social_assistance`.
2. Menu parent `spp_vocabulary.menu_spp_vocabulary_configuration` to `spp_vocabulary.menu_vocabulary_root`.
3. Namespace advice `urn:dswd:vocab:{name}` to `urn:dswd:4ps:{name}` (and the ID type table in the research doc).
4. Menu path "Registry > Configuration > Vocabularies" to "Settings > Vocabularies".

Verify, then fix if true:

5. Layer 0 list (`hr, stock, account, calendar`) versus CLAUDE.md (`base, mail, web`).
6. Scaffold ACL and DESCRIPTION referencing `dswd_attendance.group_dswd_attendance_officer` from a generic
   `dswd_{domain}` scaffold.
7. Scaffold `menus.xml` root under `base.menu_custom` (developer-mode Technical menu?).
8. `extending-openspp.md` Step 3 targets an individual-page anchor; add that households use the `group_*` anchors.
9. Neither guide explains first install; add the `install` command where the module is first run.

Commit: `docs(guides): correct vocabulary domain, menu ids, namespace pattern and first-install steps`.

## D. Verification

- `uv run pytest tests/` (CLI and docs tests).
- `./odoo-project test dswd_wellbeing` at each step (Docker); record the wall time for the runbook.
- `pre-commit run --files <changed>`; `./odoo-project lint`; `./odoo-project audit-security`.
- Manual: `./odoo-project start`, `install dswd_wellbeing`, open a household, set a level; `update` after a view
  change.
- `/verify-tests` after the build.

## E. Out of scope for this PR (next round)

Trainer runbook, slides, anatomy handout, troubleshooting drill sheet and answer key, quiz bank, Day 3 exercise sheet,
`dswd_wellbeing_broken` (kept under `training/`, not at the repo root, so CI does not try to test it), screen
recording.

## F. Unsure

- Whether a second `odoo -i` process against the live database is safe while the server is running. click-odoo-update
  does the same from `update`, so the pattern is already in use, but the restart afterwards is mandatory.
- Whether `get_view` on the inherited form is stable enough as a step 3 test, or whether `env.ref` on the view id
  plus `arch_db` contains the field name is the simpler assertion. Decide when writing the test.
