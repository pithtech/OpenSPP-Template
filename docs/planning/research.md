# Research: OpenSPP Developer Training Template

> **Status**: research phase, awaiting review before planning.
> **Date**: 2026-11-05
> **Purpose**: decide what to base this template on, how to build the OpenSPP Docker image, and what
> must change for Windows participants, before writing the implementation plan.

---

## 1. What this repo must become

A GitHub **template repository** (`pithtech/OpenSPP-Template`) that each DSWD 4Ps IT trainee clones via
"Use this template". Each clone must give a participant, with no prior setup beyond the prerequisites:

1. A **local OpenSPP v2 instance** (latest release) running in Docker, on Windows first, macOS/Linux second.
2. A **developer CLI** to build, start, stop, test, update, and reset that instance.
3. **Claude Code configuration** (CLAUDE.md, rules, agents, commands, hooks, permissions) tuned so Claude
   produces OpenSPP-quality modules: naming, three-tier security, tests, Odoo 19 syntax.
4. **Docs**: principles, guides, module scaffold, and a README that gets them working in minutes.
5. **CI** that runs lint and module tests on their own repo.
6. An **example module** with the `tpl_` placeholder prefix and an `init` command that renames it.

Only Edwin commits here. Participants never push to this repo.

---

## 2. Candidate references compared

| Candidate | Where | Verdict |
| --- | --- | --- |
| **`~/Projects/Template-Project`** (pithtech/Template-Project, March 2026) | local | **Base this repo on it.** Odoo 19, cross-platform Python CLI (`odoo-project`) with `init` + `doctor`, full `.claude/` set, docs, CI, pre-commit, `training/` folder with SETUP/LAB-GUIDE/REFERENCE/SLIDES. Its Dockerfile, compose, entrypoint, CLI, lint scripts, rules, and agents are a direct descendant of OpenSPP2's own tooling, so adapting it back to OpenSPP is a small delta. |
| `~/Projects/Training-Sample` | local | A `Template-Project` clone with two commits ("Add all repo template files"). No extra value; confirms the template-to-participant flow worked once. |
| `~/Projects/eSMIS` | local | Same tooling, plus six real `esmis_*` modules and `docs/research`. Heavier, project-specific. Use only as a reference for how a real project evolved from the template. |
| `OpenSPP/OpenSPP2` tag `2026.09` | GitHub, public | **Source of the Docker image contents and the OpenSPP conventions.** Odoo 19 (OCA/OCB), Python 3.13, PostGIS 18. Ships `docker/Dockerfile`, `docker-compose.yml`, `spp` CLI, `AGENTS.md`, `.pre-commit-config.yaml`. Does **not** ship `.claude/` or `docs/` at the tag. Does **not** publish a container image (CI builds `openspp-test:<sha>` locally only). |
| `OpenSPP/openspp-odoo-addons-repo-template` | GitHub, public | Copier template, last touched 2024, Odoo ≤ 16. Not usable. |
| `OpenSPP/openspp-docker`, `openspp-packaging-docker` | GitHub, public | Doodba / APT-package images for Odoo 17 (OpenSPP v1). Not usable for v2. |
| `OpenSPP/openspp-ph-dswd-4p-modules` | GitHub, private, branch 17.0 | OpenSPP v1 modules for 4Ps: `spp_spmis_dswd4ps`, `spp_attendance_dswd`, `spp_school_grade_level`, `spp_spmis_dswd4ps_dashboard`. Useful only as domain inspiration for lab exercises (attendance compliance, grade levels, household views). |
| `OpenSPP/claude-plugins` | GitHub, public | Marketplace with an `odoo-lsp` plugin. Worth adding to `.claude/settings.json` as an optional plugin. |
| `OpenSPP/si-training` | GitHub, private | HTML course site (module-1..5). Different format; not a code template. |

**Conclusion**: start from `Template-Project`, swap its Docker layer and conventions to OpenSPP2 `2026.09`.

---

## 3. OpenSPP2 `2026.09` facts that drive the design

| Item | Value | Source |
| --- | --- | --- |
| Latest release | `2026.09` (published 2026-09-15), monthly calendar tags; also `2026.08`, `2026.07`, `v19.0.2.0.0` | `gh api .../releases/latest` |
| Default branch | `19.0` | repo metadata |
| Odoo | 19.0 from `OCA/OCB` branch tarball | `docker/Dockerfile` |
| Python | 3.13 (`python:3.13-slim-bookworm`) | `docker/Dockerfile` |
| Database | `postgis/postgis:18-3.6-alpine` | `docker-compose.yml` |
| Third-party addons | OCA `server-ux`, `server-tools`, `server-backend`, `rest-framework`; `muk-it/odoo-modules`; **`OpenSPP/odoo-job-worker`** (replaces OCA/queue) | `docker/Dockerfile`, `EXTERNAL_DEPENDENCIES.md` |
| Addons path | `/opt/odoo/odoo/addons,/opt/odoo/odoo/odoo/addons,/mnt/extra-addons/openspp,/mnt/extra-addons/server-ux,/mnt/extra-addons/server-tools,/mnt/extra-addons/odoo-job-worker,/mnt/extra-addons/server-backend,/mnt/extra-addons/rest-framework,/mnt/extra-addons/muk-it` | `odoo.conf.template` |
| Python deps | `requirements.txt` (generated from manifests) + `docker/requirements.txt` (rlPyCairo, xlrd, boto3, click-odoo-contrib, openupgradelib, geoip2, …) | both files at tag |
| Compose services | `db`, `openspp` (ui profile, 8069), `openspp-dev` (dev profile), **`jobworker`** (dev+ui), `test`, `e2e-runner`, `prism` | `docker-compose.yml` |
| Default init module | `spp_base`; starters: `spp_starter_sp_mis`, `spp_starter_social_registry`, `spp_starter_farmer_registry`, `spp_starter_disability_registry`; demos: `spp_mis_demo_v2`, `spp_demo_phl_luzon` (Philippine Luzon geodata) | manifests |
| Repo size | ~29 MB (API `size`), ~90 `spp_*` modules | repo metadata |
| Dockerfile differences vs Template-Project | `--no-deps` on Odoo install (PyPDF2 fix), pinnable `*_REF` build args for every addon repo, geoipupdate 7.1.1 with checksums, job-worker instead of queue | diff of both files |
| Entrypoint differences vs Template-Project | Template-Project's is slightly hardened (env-var passing to python, `$$`-quoted SQL) and adds `ODOO_QUEUE_JOB_CHANNELS`, `WITHOUT_DEMO`, `SMTP_USER/PASSWORD`; OpenSPP adds `ODOO_DB_MAXCONN` | diff |

---

## 4. Template-Project inventory and what to do with each part

| Path | Size | Keep / Adapt / Drop | Notes |
| --- | --- | --- | --- |
| `odoo-project` (CLI, 2197 lines, pure Python) | — | **Adapt** | Change `_DOCKER_ADDONS_PATH` (add `openspp`, `odoo-job-worker`, drop `queue`), `DEMO_PROFILES`, service names, `init` next-steps, `doctor` (add Windows checks). Keep `init`, `doctor`, `test`, `start`, `stop`, `update`, `resetdb`, `logs`, `shell`, `sql`, `lint`, `status`. |
| `docker/Dockerfile` | — | **Adapt** | Add an OpenSPP download step at `OPENSPP_REF=2026.09` into `/mnt/extra-addons/openspp`; install OpenSPP's `requirements.txt` + `docker/requirements.txt` from that tarball; swap `OCA/queue` for `OpenSPP/odoo-job-worker`; take OpenSPP's `--no-deps`, pinned `*_REF` args, geoip checksums. Participant modules stay volume-mounted at `/mnt/extra-addons/custom`. |
| `docker-compose.yml` | — | **Adapt** | Add `jobworker` service (from OpenSPP compose). Default `ODOO_INIT_MODULES` to the training bundle (see §6.4). |
| `docker/entrypoint.sh`, `odoo.conf.template` | — | **Adapt** | Keep Template-Project's hardened entrypoint; add `ODOO_DB_MAXCONN`; set addons path to the OpenSPP list plus `/mnt/extra-addons/custom`. |
| `docker/docker-compose.production.yml`, `.env.production.example` | — | **Drop** | Training template; production deploy is out of scope and confuses participants. Mention OpenSPP's own production compose in docs instead. |
| `.claude/` (settings, hooks, 5 agents, 5 rules, 6 commands) | 92 K | **Adapt** | Rewrite content for OpenSPP: `spp.*` models, registrant/group/program/cycle/entitlement vocabulary, OpenSPP three-tier security groups, `spp.reg.id` external identifiers, job-worker instead of `queue_job`, OpenSPP AGENTS.md pitfalls. Add `OpenSPP/claude-plugins` marketplace entry. Keep `tpl_` placeholders so `init` renames them. |
| `CLAUDE.md` | — | **Adapt** | Merge Template-Project's structure with OpenSPP2 `AGENTS.md` content (layers, pitfalls, verification workflow). |
| `docs/principles/` (17 files) | — | **Keep, light edit** | These originated from OpenSPP's `docs/principles/`; re-point examples from `tpl_sale`-style to OpenSPP domain examples. |
| `docs/guides/` (6 files) | — | **Adapt** | `odoo-project-cli.md`, `module-development.md`, `testing-guide.md`, `claude-code-for-developers.md` are needed. Add Windows troubleshooting. `claude-code-sandbox.md` (devcontainer) is optional; `security-audit-guide.md` depends on scripts we may drop. |
| `docs/architecture/` (vision, integration patterns, 10 ADRs) | — | **Mostly drop** | The ADRs (API v2, PII encryption, DMS, terminology…) are eSMIS/OpenSPP-internal decisions. Keep `decisions/README.md` as the ADR template plus `vision.md` rewritten for "extending OpenSPP". |
| `scripts/` | 996 K | **Prune hard** | Keep only what the CLI and pre-commit call: `lint/`, `compliance/`, `test_single_module.sh`, `detect_modules.py`, `audit-api-auth.py`, `security_audit.py`, `fix-lint.sh`, `fix-security.sh`, `fix-odoo19.sh`, `audit-security.sh`, `audit-modules.sh`, `setup_test_env.sh` (Claude Code web). Drop: `zap/`, `trivy/`, `gitleaks/`, `translate_*`, `op_task.py`, `sync_issue_to_odoo.py`, `export_to_public.py`, `create_epic_tasks.py`, `workflows-manual/`, `glossary/`, `build_env_cache.sh`, `cleanup_odoo19_environment.sh`, `test_all_migrated_modules.sh`, `test_odoo19_modules.sh`, `requirements-odoo19.txt`. |
| `.github/workflows/` (ci, ci-full, pre-commit, security, code-analysis) | — | **Keep `ci.yml` + `pre-commit.yml`**, drop the rest | `ci.yml` detects changed modules and tests them in the built image. Add a `build-image.yml` (see §6.2). |
| `.github/ISSUE_TEMPLATE`, `pull_request_template.md`, `dependabot.yml` | — | **Keep** | Standard. |
| `.pre-commit-config.yaml`, `.ruff.toml`, `.pylintrc*`, `.flake8`, `.isort.cfg`, `.prettierrc.yml`, `.eslintrc.yml`, `.editorconfig`, `.gitattributes`, `.gitignore`, `.gitleaks.toml`, `.semgrep/`, `pyproject.toml` | — | **Keep** | Same as OpenSPP2. `.gitattributes` already forces LF for all text, which is essential on Windows. |
| `Makefile` | — | **Drop** | Only wraps the security scanners we are dropping. `make` is not on Windows by default. |
| `tpl_vocabulary/` (example module, 35 tests) | 100 K | **Replace** | A generic vocabulary model does not teach OpenSPP. See §6.5. |
| `tests/` (CLI/script unit tests) | 20 K | **Keep, adapt** | `test_shell_scripts.py`, `test_audit_api_auth.py`. Add tests for the CLI changes. |
| `training/` (SETUP, LAB-GUIDE, REFERENCE, SLIDES + .docx/.pptx + build scripts) | 392 K | **Adapt SETUP.md only, for now** | SETUP.md is Windows-first and 90 % reusable. LAB-GUIDE/SLIDES are the SIS course; a 4Ps lab is new content (§7, question 6). |
| `.devcontainer/` | — | **Keep as optional** | Not needed for the training path; harmless. |
| `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `COPYRIGHT`, `code_of_conduct.md`, `CONTRIBUTORS.md`, `license_header.txt`, `code_owners.py` | — | **Keep, edit** | License: Template-Project is LGPL-3; OpenSPP2 is LGPL-3. Keep LGPL-3. |
| `odools.toml`, `tools/readme_template.rst.jinja` | — | **Keep** | OCA readme generation. |

---

## 5. Windows findings

Most participants are on Windows. What already works, and what needs care:

| Concern | Finding |
| --- | --- |
| CLI | `odoo-project` is a Python 3.11+ script with no bash dependency in Docker mode. It enables ANSI colours on Windows. Invocation is `python odoo-project <cmd>` from PowerShell/CMD, or `./odoo-project` from Git Bash. **Gap**: no `odoo-project.cmd` shim, so the README has two spellings for every command. |
| Line endings | `.gitattributes` sets `* text=auto eol=lf` and `*.sh text eol=lf`. Entrypoint and test scripts therefore arrive LF even with `core.autocrlf=true`. Good. |
| Docker Desktop | Requires WSL 2 backend. Bind mounts from the Windows filesystem (`C:\Users\...`) are **slow**; OpenSPP's ~90 modules read through such a mount would make startup and tests painfully slow. **Baking OpenSPP into the image** (not mounting it) sidesteps this; only the participant's small modules are mounted. Cloning inside WSL (`\\wsl$`) is faster still and should be the recommended path, with the plain-Windows path documented as supported. |
| `platform: linux/amd64` on `db` | Harmless on Windows x86-64. Required for Apple Silicon. |
| `:ro,z` mount flags | `z` is an SELinux label; Docker Desktop ignores it. |
| Claude Code hooks | `.claude/hooks/post-edit-lint.sh` is bash. Claude Code on Windows needs Git for Windows and runs hooks through its bash, so it works, but a Python hook would be more robust. Low-cost change. |
| pre-commit | Works on Windows with Python. The `prettier`/`eslint` hooks need Node (`default_language_version.node: 22.9.0`, auto-installed by pre-commit). |
| `make` | Not available on Windows. Dropping the Makefile removes the issue. |
| `doctor` | Should additionally check: WSL 2 backend active, Docker Desktop memory ≥ 4 GB (OpenSPP with SP-MIS starter needs it), port 8069 free, `git config core.autocrlf`. |
| Port | 8069 fixed in `ui` profile; `dev` profile uses a dynamic port. Fixed port is simpler for a classroom. |
| Image build time | Building from scratch downloads Odoo 19 (~200 MB), six addon repos, OpenSPP, and compiles Python deps: 10–25 min on classroom Wi-Fi. A prebuilt image (§6.2) turns this into a `docker pull`. |

---

## 6. Design decisions to confirm

### 6.1 Base and prefix
Base on `Template-Project`; keep the `tpl_` placeholder and `odoo-project init <prefix> "<Name>"`. The
training prefix is the participant's choice (for example `fps_` or `dswd_`). OpenSPP's own naming guidance
reserves `spp_` for upstream modules; the v1 4Ps repo used `spp_*_dswd`, which collides with that guidance.
**Recommendation**: teach a distinct organisational prefix, not `spp_`.

### 6.2 Docker image strategy
**Recommended**: one Dockerfile, three sources, all pinned:
- Odoo 19 from `OCA/OCB` (as today).
- OpenSPP2 from `https://github.com/OpenSPP/OpenSPP2/archive/refs/tags/${OPENSPP_REF}.tar.gz`, `OPENSPP_REF=2026.09`, extracted to `/mnt/extra-addons/openspp` inside the image, with its `requirements.txt` and `docker/requirements.txt` installed from that same tarball (so Python deps always match the release).
- Addon repos pinned via `*_REF` args exactly as OpenSPP2 does.

Plus a **`build-image.yml`** GitHub Actions workflow in this template repo that builds and pushes
`ghcr.io/pithtech/openspp-template:2026.09` (and `:latest`). Compose reads `image: ${ODOO_IMAGE:-openspp-template-dev}`;
the CLI gains `odoo-project pull` so participants can skip the build. Local `build` remains the fallback and the
path for anyone who changes `docker/requirements.txt`.

Rejected: git submodule of OpenSPP2 (slow bind mount on Windows, submodule friction, 29 MB per clone);
volume-mounting a local OpenSPP checkout (same bind-mount problem).

### 6.3 Readable OpenSPP source for Claude and participants
Claude Code cannot extend what it cannot read, and the image's copy is not on the host. **Recommendation**: add
`odoo-project vendor` (name open) that downloads the same `2026.09` tarball into a gitignored `vendor/openspp/`
folder, and reference it from `CLAUDE.md` ("upstream source is in `vendor/openspp/`, read-only"). The tarball
is ~30 MB; no git history. The image and the vendor folder share the one `OPENSPP_REF` constant.

### 6.4 Default modules and demo profiles
- `ODOO_INIT_MODULES` default: `spp_starter_sp_mis` (registry + programs + service points + approval + API v2), which is what 4Ps maps onto.
- `DEMO_PROFILES`: `base` → `spp_starter_sp_mis`; `demo` → `spp_mis_demo_v2`; `phl` → `spp_mis_demo_v2,spp_demo_phl_luzon`.
- Keep `jobworker` running in `ui` profile so queued imports and batch actions work in class.

### 6.5 Example module
Replace `tpl_vocabulary` with an OpenSPP extension module that demonstrates the patterns participants will
use on 4Ps, with full tests and security, small enough to read in ten minutes. Candidate: `tpl_registry_ext`
that inherits `res.partner` (registrant) to add a 4Ps-relevant field set and a list/form view extension, with
ACL, a security group in the three-tier pattern, and tests covering create/read/ACL. Exact content to agree
in the plan.

### 6.6 Claude configuration content
Rewrite, not just rename: rules and agents must speak OpenSPP (registrants, groups, programs, cycles,
entitlements, change requests, `spp.reg.id`, API v2, job-worker, `spp_security` groups) and quote the
OpenSPP2 `AGENTS.md` pitfalls verbatim where they apply. Add `extraKnownMarketplaces` for
`OpenSPP/claude-plugins` with `odoo-lsp` enabled.

### 6.7 Testing for this repo itself
Per our TDD rule: unit tests for CLI changes (`tests/test_cli.py` using the existing pattern), the existing
shell-script tests, and an integration test that builds the image and runs the example module's tests
(this is what `ci.yml` does on push). End-to-end for a template is "a fresh clone goes from `init` to a
passing `test` on Windows and macOS", which must be exercised manually once on a Windows machine before the
training.

---

## 7. Open questions for Edwin

1. **Prebuilt image on GHCR** (§6.2): do you want this repo's CI to publish `ghcr.io/pithtech/openspp-template:2026.09` so participants only pull? It needs the package set to public, or participants logged in to GHCR.
2. **Vendor checkout** (§6.3): agree to a gitignored `vendor/openspp/` fetched by the CLI, so Claude can read upstream source?
3. **Example module** (§6.5): `res.partner` registrant extension as sketched, or something closer to the 4Ps domain (for example attendance compliance, grade level) from the v1 4Ps repo?
4. **Prefix convention** (§6.1): confirm "organisation prefix, never `spp_`" as the taught rule.
5. **Scope of docs**: drop the 10 ADRs and the production compose files as proposed?
6. **Training materials**: adapt only `training/SETUP.md` now, and leave LAB-GUIDE/SLIDES for a later task once the lab content for 4Ps is decided?
7. **Repo access**: `gh` here is logged in as `gonzalesedwin1123` and cannot see `pithtech/OpenSPP-Template` (404), while git pushes go through the `pithtech` SSH alias. Pushing works; GitHub settings (mark as template, branch protection, GHCR visibility) must be done by you in the UI or with a token on the pithtech account.
8. **Pinning**: tag `2026.09` now; when `2026.10` or later ships before the training, bumping is one constant (`OPENSPP_REF`) plus a rebuild. OK?

---

## 8. Sources consulted

- Local: `~/Projects/Template-Project` (README, CLAUDE.md, odoo-project, docker/*, docker-compose.yml, .claude/*, .pre-commit-config.yaml, .gitattributes, scripts/, docs/, training/, .devcontainer/, .github/workflows/ci.yml), `~/Projects/Training-Sample`, `~/Projects/eSMIS`.
- GitHub `OpenSPP/OpenSPP2@2026.09`: release notes, `docker/Dockerfile`, `docker-compose.yml`, `docker/odoo.conf.template`, `docker/entrypoint.sh`, `docker/requirements.txt`, `requirements.txt`, `EXTERNAL_DEPENDENCIES.md`, `AGENTS.md`, `spp` CLI, `scripts/test_single_module.sh`, `.github/workflows/*`, manifests of `spp_starter_sp_mis`, `spp_mis_demo_v2`, `spp_demo_phl_luzon`.
- GitHub `OpenSPP/openspp-ph-dswd-4p-modules@17.0` manifests; `OpenSPP/claude-plugins`; `OpenSPP/openspp-odoo-addons-repo-template`; `OpenSPP/openspp-docker`; `OpenSPP/openspp-packaging-docker`; `OpenSPP/si-training` (tree only).
