# DSWD 4Ps OpenSPP Extension Modules

Extension modules for the DSWD Pantawid Pamilyang Pilipino Program (4Ps) on **OpenSPP v2** (Odoo 19). Modules use
`dswd_*` naming and extend upstream `spp_*` modules. The OpenSPP release is pinned in `.env` (`OPENSPP_REF`).

## Where Things Are

| What                             | Where                                                      |
| -------------------------------- | ---------------------------------------------------------- |
| Your modules                     | `dswd_*/` at the repo root                                 |
| OpenSPP source (read-only)       | `upstream/openspp/` — run `./odoo-project vendor` to fetch |
| Upstream conventions             | `upstream/openspp/AGENTS.md`                               |
| Principles                       | `docs/principles/`                                         |
| Guides (CLI, extending, testing) | `docs/guides/`                                             |
| Architecture and decisions       | `docs/architecture/`, `docs/architecture/decisions/`       |
| Specifications, one per change   | `docs/specs/` — read the spec and its ADRs before planning |

**Never edit anything under `upstream/openspp/`.** Read it to learn models, hooks, views, groups, and test helpers
before extending them. Upstream changes belong in a pull request to OpenSPP, not here.

## Auto-Loaded Rules (`.claude/rules/`)

Path-scoped rules load automatically when you edit matching files:

| Rule              | Triggers On                   | Covers                                          |
| ----------------- | ----------------------------- | ----------------------------------------------- |
| `odoo-python.md`  | `models/*.py`, `wizard/*.py`  | Naming, extending OpenSPP models, Odoo 19 API   |
| `odoo-xml.md`     | `views/*.xml`, `data/*.xml`   | View syntax, inheriting OpenSPP views, layout   |
| `security.md`     | `security/*`                  | OpenSPP three-tier groups, ACLs, record rules   |
| `testing.md`      | `tests/*.py`                  | Coverage targets, upstream test helpers, quirks |
| `module-setup.md` | `__manifest__.py`, `readme/*` | Manifest fields, dependencies, descriptions     |

## Architecture

### Layers (dependencies flow downward)

```
Layer 3: DSWD 4Ps EXTENSIONS   (dswd_attendance, dswd_compliance, dswd_reports)
    ↓
Layer 2: OPENSPP CAPABILITIES  (spp_programs, spp_change_request_v2, spp_event_data, spp_grm)
    ↓
Layer 1: OPENSPP FOUNDATION    (spp_registry, spp_security, spp_area, spp_vocabulary, spp_base_common)
    ↓
Layer 0: ODOO CORE + OCA       (base, mail, web; base_user_role, job_worker, fastapi)
```

### Extension Patterns

- **Inherit and extend**: `_inherit = "res.partner"` + fields prefixed `dswd_`
- **Hook methods**: use upstream `_pre_enrollment_hook()` / `_post_enrollment_hook()`; add your own hooks on `dswd.*`
  models
- **Inherit views**: `inherit_id` + XPath on **named** upstream elements
- **Never expose DB IDs** in APIs — use `spp.registry.id` identifiers or external ids
- **Background work**: job worker (`record.with_delay().method()`), never `cr.commit()` in loops

### Key Upstream Models

`res.partner` (registrant: `is_registrant`, household: `is_group`), `spp.group.membership`, `spp.registry.id`,
`spp.id.type`, `spp.program`, `spp.program.membership`, `spp.cycle`, `spp.entitlement`, `spp.change.request`,
`spp.area`, `spp.event.data`, `spp.vocabulary` / `spp.vocabulary.code`, `spp.approval.mixin`.

## Quick Checklist

- [ ] Naming follows `dswd_*` / `dswd.*` conventions; upstream fields prefixed `dswd_`
- [ ] `application=False`, `auto_install` set per [module-visibility](docs/principles/module-visibility.md)
- [ ] `ir.model.access.csv` exists and complete; `base.group_system` row first
- [ ] Manager group linked into `spp_security.group_spp_admin`
- [ ] No `print()` - use `_logger`
- [ ] No bare `except:` clauses
- [ ] No `cr.commit()` in loops - use the job worker
- [ ] No PII in log messages
- [ ] Tests exist for core functionality
- [ ] Nothing under `upstream/openspp/` changed

## Known Pitfalls (from recurring issues)

**Bug fixing**: write a failing test first, then fix at the source (not workarounds).

### Access Rights (Most Common Error)

- **Always check `ir.model.access.csv`** before declaring a module complete
- When tests fail with `AccessError`, fix the ACL, don't bypass with `sudo()`
- Tests must run with appropriate user context (officer, manager), not just admin
- After security changes, **always re-run affected tests** - they often break
- Related models need ACLs too (e.g., if `dswd.attendance` has an ACL, `dswd.attendance.line` likely needs one)

### Extending OpenSPP

- Read the upstream module in `upstream/openspp/` first; do not guess field or method names
- Registrant searches must include `is_registrant=True`; households also `is_group=True`
- Depend on the specific upstream module (`spp_programs`), not a starter bundle (`spp_starter_sp_mis`)
- Do not redefine upstream groups or categories; link into them
- A `Many2one` `domain` only filters the dropdown. A field that must hold codes from one vocabulary needs an
  `@api.constrains` on the namespace, or writes from code, imports and the API will store anything

### Demo Data

- Demo data must create **complete, consistent records** — check all required relations
- Use `with_context(tracking_disable=True)` to avoid sending notifications
- Test demo data generation with dedicated tests

### Views and XML

- XPath must use `hasclass('classname')` not `@class='classname'` (Odoo 19)
- Always use `Command.create()` not `(0, 0, {...})` tuples for relational writes
- When updating views, verify the correct view is being displayed (not a cached old version)
- Search views: check `<filter>` and `<group>` syntax against Odoo 19 docs
- `noupdate="1"` data files are parsed only on first load. A bad value (an invalid selection value, a wrong `ref`) fails
  at install, not on a later `update`; fix values before the first load, or delete the record and update again

### Tests

- **NEVER remove or weaken existing tests** without explicit approval
- After subagent implementations, verify: "Can you confirm no tests were removed or weakened?"
- When fixing security, tests often need user context updates - fix tests, don't skip them
- If tests cannot run due to install issues, fix the install, don't mark tests as skipped

### State Machines and Approvals

- `spp.approval.mixin` records must have consistent state: `approval_state='pending'` requires pending
  `spp.approval.review` records; `approval_state='approved'` requires all reviews approved
- When creating test data for approval flows, create the full approval chain

### GitHub Account

- Everything in this repository happens under the `pithtech` account. Local commits and SSH pushes already use it
  (`~/.gitconfig-projects`, the `pithtech` SSH host), but the `gh` CLI acts as whichever account is active, and a PR
  merged through `gh` gets a merge commit authored by that account. Run `gh` here as
  `GH_TOKEN="$(gh auth token --user pithtech)" gh ...` (or `gh auth switch --user pithtech` first), and check
  `gh api user --jq .login` before creating or merging a PR.
- The CI and pre-commit workflows run only on pull requests against `main`. A PR stacked on a feature branch gets no
  checks until it is retargeted to `main`; `gh run watch` in a pipe reports the pipe's exit status, not the run's.

### Repo Layout

- No top-level directory may be called `forms`, `helpers`, `mixins`, `utilities` or `vendor`. The repo root is mounted
  as an addons root and Odoo's SCSS importer resolves a relative `@import "<dir>/..."` against any addons root that
  contains a `<dir>` folder, which breaks every stylesheet build. The OpenSPP checkout therefore lives in
  `upstream/openspp`; `doctor` reports and `start` refuses such folders, and a pre-commit hook blocks them.
- Odoo keeps a compiled asset bundle while its version hash matches, and the hash comes from the source files, not from
  a successful compile. After any broken stylesheet build, run `./odoo-project resetassets`.

### Docs and Markdown

- Prettier reads a run of underscores in a table cell as emphasis and rewrites it differently on every pass, so the hook
  never settles. Use empty cells for fill-in blanks. `docs/` and `README.md` are excluded from every hook; only
  `tests/test_docs.py` checks them.

### Commits and PRs

- No Claude attribution anywhere: no `Co-Authored-By: Claude`, no "Generated with Claude Code" footer, no mention of
  Claude in commit messages, PR titles or PR bodies. `.claude/settings.json` sets `includeCoAuthoredBy` to false; the
  `/commit` and `/pr` commands repeat the rule. Before `gh pr create`, check the body for "Claude".

After every correction or PR, propose updates to this Known Pitfalls section.

## Running Locally

```bash
./odoo-project doctor                   # Check prerequisites
./odoo-project pull                     # Get the Docker image (or: build, 10-25 min)
./odoo-project vendor                   # Get OpenSPP source into upstream/openspp
./odoo-project start                    # http://localhost:8069 (admin/admin)
./odoo-project stop                     # Stop
./odoo-project stop -v -y               # Clean restart (fresh DB)
```

On Windows PowerShell use `.\odoo-project` (the `.cmd` shim) or `python odoo-project`.

## Running Tests

```bash
./odoo-project test <module_name>                # Docker-based, isolated (cross-platform)
./odoo-project test <module> --tags=post_install # Filter by test tags
```

## Linting and Compliance

```bash
pre-commit run ruff --files <changed_files>         # Lint
pre-commit run ruff-format --files <changed_files>  # Format
pre-commit run prettier --files <changed_files>     # XML/MD/JSON format
./odoo-project lint                                 # All three on changed files
./odoo-project audit-security                       # Security/ACL audit
./odoo-project fix-odoo19                           # Fix Odoo 19 Command API tuples
```

## Verification (before marking any task complete)

1. `./odoo-project test <module>` — run tests
2. `pre-commit run --files <changed_files>` — run linters
3. `/verify-tests` — confirm no tests were removed or weakened
4. If demo data modified: verify records created correctly
5. If UX changes: confirm correct view displays in UI

## Custom Commands

| Command          | When                | Purpose                                                 |
| ---------------- | ------------------- | ------------------------------------------------------- |
| `/implement`     | Implementing        | Carry out the plan with subagents and expert review     |
| `/verify-tests`  | After subagent work | Check test integrity (catch removed tests)              |
| `/analyze`       | Debugging           | Deep analysis mode - understand before implementing     |
| `/expert-review` | Review              | Parallel code review from multiple perspectives         |
| `/commit`        | Before commit       | Conventional commit (feat/fix/chore/docs/refactor/test) |
| `/pr`            | After commit        | GitHub PR creation                                      |

**Starting work**: Enter Plan mode (shift+tab twice) for brainstorming.

## Subagents

| Agent              | Model  | Use For                                |
| ------------------ | ------ | -------------------------------------- |
| `@odoo-developer`  | sonnet | Core implementation work               |
| `@code-reviewer`   | opus   | Security, naming, Odoo 19 compliance   |
| `@ux-expert`       | opus   | UI/UX patterns and form layouts        |
| `@code-simplifier` | sonnet | Reduce complexity, improve readability |
| `@verify-module`   | sonnet | Test module installation and tests     |
