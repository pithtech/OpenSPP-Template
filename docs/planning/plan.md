# Implementation Plan: OpenSPP Developer Training Template

> **Status**: implemented 2026-11-06 (steps 1-8 done locally; step 9, the Windows run-through, is pending).
> **Based on**: `docs/planning/research.md` and Edwin's answers (2026-11-05).
> **Settled**: base on Template-Project; OpenSPP2 `2026.09`; prefix `dswd_`; no example module yet; drop `init`;
> drop the nine eSMIS ADRs and the production compose files; vendor checkout for Claude; adapt only
> `training/SETUP.md`; pin via a single `OPENSPP_REF`.
> **Open**: image visibility default (section 1), and the items in section 9.

---

## 1. Participant onboarding flow (decided 2026-11-05)

**Flow A, verified**: the template repo stays private and is marked as a template. Edwin invites each
participant as a collaborator with **Read** access. The participant opens the repo, clicks
"Use this template" → "Create a new repository", and picks their own account as owner. Verified with
`gonzalesedwin1123`, which created the private repo `OpenSPP-Custom-modules` with
`template_repository = pithtech/OpenSPP-Template` and a single "Initial commit" (no history carried over).

README and `training/SETUP.md` will describe exactly this flow. Participants never need org membership,
and Edwin can be added as a collaborator on each participant repo for the demo sessions.

**Image visibility**: the published image is the `dev` target, which contains only Odoo 19, the OCA/muk-it
addons and OpenSPP. No repo files (docs, `.claude/`, modules) are copied in, because participant code is
volume-mounted. Default for this plan: **public package** on GHCR, so participants pull without a token.
If Edwin prefers a private package, step 5 adds a token section to the setup guide and the package inherits
read access from the repo.

---

## 2. Target layout

```
OpenSPP-Template/
├── odoo-project                  # developer CLI (Python, cross-platform)
├── odoo-project.cmd              # Windows shim so `odoo-project <cmd>` works in PowerShell/CMD
├── .env                          # committed, no secrets: OPENSPP_REF=2026.09 and image name (single pin)
├── docker-compose.yml            # db, odoo-app (ui), odoo-dev (dev), jobworker, test
├── docker/
│   ├── Dockerfile                # builder/runtime/dev targets; downloads OpenSPP at OPENSPP_REF
│   ├── entrypoint.sh
│   ├── odoo.conf.template
│   ├── requirements.txt          # project extras beyond OpenSPP's own (starts near-empty)
│   ├── requirements-dev.txt
│   └── README.md
├── requirements.txt              # generated from dswd_* manifests (empty until modules exist)
├── vendor/                       # gitignored; vendor/openspp = read-only OpenSPP source at OPENSPP_REF
├── CLAUDE.md
├── .claude/
│   ├── settings.json             # permissions + OpenSPP/claude-plugins marketplace (odoo-lsp)
│   ├── hooks.json
│   ├── hooks/post-edit-lint.py   # Python port of the bash hook (Windows-safe)
│   ├── rules/                    # odoo-python, odoo-xml, security, testing, module-setup (dswd_, OpenSPP terms)
│   ├── agents/                   # odoo-developer, code-reviewer, ux-expert, code-simplifier, verify-module
│   └── commands/                 # implement, verify-tests, analyze, expert-review, commit, pr
├── docs/
│   ├── README.md
│   ├── principles/               # from Template-Project, examples re-pointed to OpenSPP/dswd_
│   ├── guides/                   # odoo-project-cli, module-development, testing-guide,
│   │                             # claude-code-for-developers, windows-setup, extending-openspp
│   ├── architecture/
│   │   ├── vision.md             # "extending OpenSPP": layers, where dswd_ modules sit
│   │   └── decisions/README.md + ADR-001-dswd-module-prefix.md
│   └── planning/                 # research.md, plan.md (see 9.2)
├── scripts/                      # pruned: lint/, compliance/, test_single_module.sh, detect_modules.py,
│                                 # audit-api-auth.py, security_audit.py, audit-security.sh, fix-odoo19.sh,
│                                 # setup_test_env.sh, README.md
├── tests/                        # repo-level tests: CLI, docker config, shell scripts
├── training/SETUP.md             # pre-training setup, Windows first
├── .github/
│   ├── workflows/ci.yml          # lint + test changed dswd_* modules + image smoke test
│   ├── workflows/pre-commit.yml
│   ├── workflows/build-image.yml # build and push ghcr.io/pithtech/openspp-template:<OPENSPP_REF>
│   ├── ISSUE_TEMPLATE/, pull_request_template.md, dependabot.yml
├── .pre-commit-config.yaml, .ruff.toml, .pylintrc, .pylintrc-mandatory, .flake8, .isort.cfg,
│   .prettierrc.yml, .eslintrc.yml, .editorconfig, .gitattributes, .gitignore, .gitleaks.toml,
│   .semgrep/, .odoo-lint.yaml, pyproject.toml, odools.toml, tools/readme_template.rst.jinja
├── .devcontainer/                # optional sandbox, unchanged
└── README.md, CONTRIBUTING.md, SECURITY.md, LICENSE (LGPL-3), COPYRIGHT, code_of_conduct.md,
    CONTRIBUTORS.md, license_header.txt, code_owners.py
```

Not carried over: `Makefile`, `tpl_vocabulary/`, `docker/docker-compose.production.yml`,
`docker/.env.production.example`, nine ADRs, `docs/guides/security-audit-guide.md` (depends on dropped
scripts), `.github/workflows/{ci-full,security,code-analysis,ci-local}.yml`, `training/{LAB-GUIDE,REFERENCE,SLIDES}.*`,
`training/*.docx|pptx|py`, the 20 unused scripts listed in the research.

---

## 3. Docker image (step 2)

**Dockerfile** (`docker/Dockerfile`), starting from Template-Project's and taking OpenSPP2's improvements:

1. `ARG OPENSPP_REF=2026.09` declared next to the other `*_REF` args (compose passes it from `.env`).
2. Builder stage downloads `https://github.com/OpenSPP/OpenSPP2/archive/refs/tags/${OPENSPP_REF}.tar.gz`
   (sha fallback as OpenSPP does for the other repos), extracts to `/opt/extra-addons/openspp`.
3. Python install in one `uv pip install`: Odoo 19 `requirements.txt` from OCA/OCB, then OpenSPP's
   `requirements.txt` and `docker/requirements.txt` taken **from the extracted tarball**, then this repo's
   `requirements.txt` and `docker/requirements.txt` as overrides. Dependencies therefore always match the
   pinned release; the project files only add what `dswd_*` manifests need.
4. Odoo installed with `--no-deps` (OpenSPP's PyPDF2 fix). Addon repos: `server-ux`, `server-tools`,
   `server-backend`, `rest-framework`, `muk-it`, **`OpenSPP/odoo-job-worker`** (no `OCA/queue`), all with
   pinnable `*_REF` args and OpenSPP's sha-aware download function.
5. Runtime stage: OpenSPP's geoipupdate 7.1.1 with checksums; `COPY --from=builder /opt/extra-addons /mnt/extra-addons`
   now includes `openspp`. `dev` target unchanged (participant code via volume). Drop the `production` target
   (would bake participant code; not needed for training).
6. Image labels: `org.opencontainers.image.source`, `.version=${OPENSPP_REF}` so GHCR links the package to
   the repo.

**`docker/odoo.conf.template`**: addons path =
`/opt/odoo/odoo/addons,/opt/odoo/odoo/odoo/addons,/mnt/extra-addons/custom,/mnt/extra-addons/openspp,/mnt/extra-addons/server-ux,/mnt/extra-addons/server-tools,/mnt/extra-addons/odoo-job-worker,/mnt/extra-addons/server-backend,/mnt/extra-addons/rest-framework,/mnt/extra-addons/muk-it`.
`custom` precedes `openspp` so a `dswd_` repo can never be shadowed. Add `db_maxconn` from OpenSPP.

**`docker/entrypoint.sh`**: keep Template-Project's hardened version; add `ODOO_DB_MAXCONN`; remove the
`ODOO_QUEUE_JOB_CHANNELS` block (no `queue_job`).

**`docker-compose.yml`**: `image: ${ODOO_IMAGE:-openspp-template-dev}` on every Odoo service, `build.args.OPENSPP_REF: ${OPENSPP_REF}`;
`ODOO_DB_NAME` default `openspp`; `ODOO_INIT_MODULES` default `spp_starter_sp_mis`; add `jobworker` from
OpenSPP's compose (profiles `ui` and `dev`, command `job_worker_runner.py`); keep `test` service; db stays
`postgis/postgis:18-3.6-alpine` with `platform: linux/amd64`.

**`.env`** (committed): `OPENSPP_REF=2026.09`, `ODOO_IMAGE=openspp-template-dev`,
`ODOO_IMAGE_REMOTE=ghcr.io/pithtech/openspp-template`. Compose loads it automatically; the CLI parses it;
CI reads it with one shell line. This is the only place the release is spelled.

Trade-off: build-from-source stays the fallback (10 to 25 min); the pull path is the classroom default.

---

## 4. CLI (step 3)

Changes to `odoo-project` (keep style; no rewrite):

- **Remove** `init` and its helpers; `fix-lint`, `fix-security`, `audit-modules` (AI-agent wrappers that
  need cursor-agent; Claude Code does this interactively). **Keep** `audit-security` (static) and `fix-odoo19`.
- **Config**: read `.env` for `OPENSPP_REF`, `ODOO_IMAGE`, `ODOO_IMAGE_REMOTE`. User config file renamed
  `~/.odoo-project.toml` as is.
- **Constants**: `_DOCKER_ADDONS_PATH` matches `odoo.conf.template` (a test asserts equality);
  `DEMO_PROFILES = {"base": "spp_starter_sp_mis", "demo": "spp_mis_demo_v2", "phl": "spp_mis_demo_v2,spp_demo_phl_luzon"}`;
  module discovery = directories with `__manifest__.py` whose name starts with `dswd_`.
- **New `pull`**: `docker pull ${ODOO_IMAGE_REMOTE}:${OPENSPP_REF}`, tag it as `${ODOO_IMAGE}`, write the
  build-freshness marker. `start`/`test` with no local image print "run `odoo-project pull` (fast) or
  `odoo-project build` (slow)" instead of auto-building.
- **New `vendor`**: download the same tarball to `vendor/openspp/` (gitignored), write `vendor/openspp/.ref`;
  `--force` re-downloads; `doctor` warns when `.ref` differs from `OPENSPP_REF`. Uses `urllib` + `tarfile`
  only (no git, no curl), so it works on Windows.
- **`doctor`** additions: Python ≥ 3.11, Node present (pre-commit prettier), Docker Desktop memory ≥ 4 GB
  (`docker info` MemTotal), WSL 2 backend on Windows (`docker info` OSType/Kernel), `git config core.autocrlf`
  advice, vendor checkout present and current, image present locally.
- **`start`**: `--demo` accepts profile names above; prints the URL and `admin/admin`.
- **Windows shim** `odoo-project.cmd`: `@python "%~dp0odoo-project" %*`. README then shows one spelling.
- **Tests** (`tests/test_cli.py`, pytest, subprocess mocked): addons path equality with the conf template;
  `.env` ref equals Dockerfile `ARG OPENSPP_REF` default; `pull` issues pull+tag; `vendor` extracts a fixture
  tarball and writes `.ref`; `doctor` reports a missing vendor checkout; module discovery filters `dswd_`;
  removed commands are absent from the parser.

---

## 5. Claude configuration (step 4)

Content rewrite, same file set:

- **`CLAUDE.md`**: Template-Project skeleton + OpenSPP2 `AGENTS.md` substance. Sections: what this repo is
  (extension modules for DSWD 4Ps on OpenSPP `2026.09`), where upstream source lives (`vendor/openspp/`,
  read-only, never edit), layers (OpenSPP foundation → capabilities → `dswd_*` extensions), naming
  (`dswd_{domain}`, `dswd.{model}`, `group_dswd_*`), quick checklist, OpenSPP pitfalls (ACLs, demo data,
  Odoo 19 XML, tests never weakened, approval mixin state), running/testing/linting with the CLI,
  verification steps, commands and subagents tables.
- **Rules**: `odoo-python.md` (dswd_ naming, inherit `res.partner`/`spp.*` models, `spp.reg.id` not DB ids,
  job-worker for batch), `odoo-xml.md` (Odoo 19 syntax, extending OpenSPP views by `inherit_id`),
  `security.md` (OpenSPP three-tier groups and how `dswd_` groups attach to them), `testing.md`
  (OpenSPP test base classes, registrant fixtures), `module-setup.md` (manifest template with
  `depends` on `spp_*`, category `DSWD 4Ps/...`).
- **Agents**: same five, prompts updated to OpenSPP vocabulary and to read `vendor/openspp/<module>` before
  extending it.
- **Commands**: unchanged except paths and CLI names.
- **Hooks**: `hooks/post-edit-lint.py` replaces the bash hook (same behaviour: ruff/ruff-format/prettier/
  check_odoo19 on the edited file); `hooks.json` points to `python "$CLAUDE_PROJECT_DIR"/.claude/hooks/post-edit-lint.py`.
- **`settings.json`**: permissions list updated to the new command set (`python odoo-project ...`,
  `odoo-project.cmd ...`); `extraKnownMarketplaces` → `OpenSPP/claude-plugins`, `enabledPlugins` → `odoo-lsp`.

---

## 6. Docs (step 5)

- **`README.md`**: five-minute quick start (prerequisites → get your repo [per section 1] → `doctor` →
  `pull` → `vendor` → `start` → open 8069), then CLI table, Claude Code section, layout, documentation map.
  Windows commands shown first, macOS/Linux second.
- **`docs/guides/windows-setup.md`**: Docker Desktop with WSL 2, clone location advice (inside WSL for speed,
  Windows path supported), PowerShell vs Git Bash, line endings, common errors.
- **`docs/guides/extending-openspp.md`**: how to find the right `spp_*` module in `vendor/openspp/`, inherit
  models/views, add fields to registrants, hook into program enrolment, where OpenSPP docs live
  (docs.openspp.org), what not to do (edit vendor, use `spp_` prefix, expose DB ids).
- **`docs/guides/odoo-project-cli.md`, `module-development.md`, `testing-guide.md`, `claude-code-for-developers.md`**: adapted.
- **`docs/principles/`**: keep all 17; replace `tpl_`/`tpl.` examples with `dswd_`/`dswd.` and
  Odoo-generic examples with OpenSPP ones where the text refers to a module.
- **`docs/architecture/vision.md`** rewritten; `decisions/README.md` kept; **ADR-001** "dswd_ module prefix"
  (context: OpenSPP reserves `spp_`; v1 4Ps modules used `spp_*_dswd`; decision; consequences).
- **`CONTRIBUTING.md`, `SECURITY.md`**: adapted (participants' repos, conventional commits, PR template).
- **`training/SETUP.md`**: keep structure; update tool list (Python 3.11+, Node for pre-commit, Claude Code
  install path), add Docker Desktop memory setting, add "pull the image before the session" step with the
  GHCR instructions matching the section 1 decision.

---

## 7. CI (step 6)

- **`ci.yml`**: on push/PR: pre-commit on changed files; detect changed `dswd_*` modules and run
  `odoo-project test` for each using the image (pulled from GHCR if public, else built); plus an
  **image smoke job**: start `db` + `odoo-app`, wait for `/web/health`, assert `spp_starter_sp_mis` is
  installed. The smoke job is the repo's integration test and runs even when no module changed.
- **`pre-commit.yml`**: unchanged.
- **`build-image.yml`**: on push to `main` touching `docker/**`, `.env`, `requirements.txt`, and on
  `workflow_dispatch`: build `dev` target, push `ghcr.io/pithtech/openspp-template:${OPENSPP_REF}` and
  `:latest`, using `GITHUB_TOKEN` with `packages: write`. Participant repos created from the template get
  this workflow too; it is harmless there (it will push to their own namespace only if they enable it) but
  I will gate it with `if: github.repository == 'pithtech/OpenSPP-Template'`.

---

## 8. Steps and commits

Status after implementation (2026-11-06): steps 1-7 committed on `main`; step 8 verified on macOS (build, vendor,
fresh `start` installing `spp_starter_sp_mis`, `test` on a throwaway `dswd_smoke` module: 1 passed); `pull` can
only be verified once `build-image.yml` has published the image. Step 9 (Windows) is still to do.

Deviations from the plan: `fix-lint`, `fix-security`, `audit-modules` dropped from the CLI as proposed;
`integration-patterns.md` and `security-audit-guide.md` dropped with the ADRs; coverage threshold lowered to 85 to
match the documented target; `start` now also waits on a fresh database without `--wipe`; Claude's lint hook is
Python; `WITHOUT_DEMO` default changed to the Odoo 19 boolean spelling.

| # | Commit | Verification |
| --- | --- | --- |
| 1 | `chore: bootstrap template from Template-Project configs` (lint configs, licence files, `.gitattributes`, `.gitignore` + `vendor/`, `.env`, `pyproject.toml`, `.editorconfig`, `tools/`, `.devcontainer/`) | `pre-commit run -a` clean |
| 2 | `feat(docker): build OpenSPP 2026.09 image with job worker` | `docker build --target dev`; `docker compose config`; `tests/test_docker_config.py` |
| 3 | `feat(cli): adapt odoo-project for OpenSPP, add pull and vendor, drop init` + `odoo-project.cmd` | `uv run pytest tests/`; manual `doctor`, `vendor`, `start`, `stop` on this Mac |
| 4 | `feat(claude): configure Claude Code for dswd_ modules on OpenSPP` | hook runs on an edit; `claude` loads without errors |
| 5 | `docs: write README, guides, principles and ADR-001 for the training template` | links checked by a small script; prettier clean |
| 6 | `ci: add module tests, image smoke test and image publishing` | push to a branch, watch the run |
| 7 | `docs(training): adapt pre-training setup guide` | review |
| 8 | Full local E2E on this Mac: `pull` (after CI publishes) → `vendor` → `start --demo=base` → login → `stop -v -y` | log attached to the PR |
| 9 | Windows E2E (manual, your machine or a participant's before the session): same sequence in PowerShell | checklist in `docs/guides/windows-setup.md` |

Each step is its own commit on `main` (you are the only committer, so no PR flow is needed unless you want one).
Tests are written before the code they cover in steps 2 and 3.

---

## 9. Items I am unsure about

1. **Package visibility** (section 1): drafting for a public GHCR package unless told otherwise; the
   onboarding flow itself is settled.
2. **Keep `docs/planning/` in the template?** Participants would see the research and plan. I suggest moving
   both to a `.planning/` folder that is listed in `.gitignore`… but then they are not versioned for you.
   Alternative: keep them in `docs/planning/` and accept that participants can read them. Your call.
3. **Memory and CPU**: `spp_starter_sp_mis` on a 4 GB Docker Desktop allocation is tight; `doctor` will warn
   below 4 GB and SETUP will recommend 6 GB. I will measure during step 8 and adjust the numbers.
4. **Whether `spp_starter_sp_mis` is the right default** install for the 4Ps lab, versus `spp_base` for a
   faster first start. Default can be changed in `.env` later.
5. **`claude-plugins` odoo-lsp** needs the `odoo-ls` binary; if it prompts participants with install
   questions on first run I will leave it listed but disabled.
6. The Dockerfile keeps `--mount=type=cache` BuildKit directives; Docker Desktop on Windows has BuildKit on
   by default, so this should be fine, but it is one more thing to confirm in step 9.
