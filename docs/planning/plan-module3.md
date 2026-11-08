# Implementation Plan: Module 3 module `dswd_asset` and materials

> **Status**: approved design ([module3-training-design.md](module3-training-design.md)); Edwin's decisions
> 2026-11-08: IT asset register; top-level app menu; keep the planted Selection; no quiz for Module 3 (assessment is
> Module 6); introduce custom groups in Module 3. Branch `feat/module3-dswd-asset`, one PR, one commit per demo step,
> tags `m3-step-0` to `m3-step-4` after merge.

## Steps (each installable, tests pass, test-first)

| Step | Files                                                                                                   | Tests added                                                                                          | Demo shows                                                                 |
| ---- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 0    | `__manifest__.py` (depends `base`, `spp_security`), `__init__.py`, header-only `security/ir.model.access.csv`, readme stub | none                                                                                    | Apps > Update Apps List > Install; `Loading module dswd_asset`             |
| 1    | `models/__init__.py`, `models/dswd_asset.py` (8 fields, computed warranty flag, constraint)             | defaults; computed flag; constraint refuses warranty before purchase                                  | Technical > Models/Fields; log `has no access rules`                        |
| 2    | `views/dswd_asset_views.xml` (list, form, search, action), `views/menus.xml` (top-level app menu)         | action and views resolve                                                                             | app tile appears; click: AccessError even as admin (the planted fault)      |
| 3    | `security/groups.xml` (category, privilege, viewer/officer/manager, admin link into `spp_security.group_spp_admin`), access rows | viewer reads but cannot create; officer creates but cannot delete; manager deletes; admin sees it | the list opens; participants register their own laptop |
| 4    | `readme/DESCRIPTION.md` completed                                                                        | none                                                                                                 | `./odoo-project test dswd_asset` summary line                               |

Conventions: model `dswd.asset`; xml ids `view_dswd_asset_{list,form,search}`, `action_dswd_asset`,
`menu_dswd_asset_root`, `menu_dswd_asset`, `category_dswd_asset`, `privilege_asset_officer`,
`group_asset_{viewer,officer,manager}`; access ids `access_dswd_asset_{system,viewer,officer,manager}`;
`@tagged("post_install", "-at_install")`, `TransactionCase` with `setUp`; users built with `group_ids`.

## Materials (`training/module3/`)

`README.md`, `runbook.md`, `slides.md` (Marp, real-stack screenshots under `images/`), `handout-anatomy.md`,
`command-card.md`. No quiz. Root README and `docs/README.md` link the folder.

## Repo fixes in the same PR

`docs/guides/module-development.md`: scaffold access rows reference undefined groups; two wrong notes about
`spp_security`; placeholder `external_dependencies`; scaffold test without `@tagged`.
`training/module4/handout-anatomy.md`: the loop row for Python edits (dev profile only).

## Verification

`./odoo-project test dswd_asset` at every step; `uv run pytest tests/`; `pre-commit` twice; `audit-security`
0 errors 0 warnings; `install dswd_asset` on the running stack, then the UI as admin; screenshots from the real stack.
