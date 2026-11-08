# OpenSPP Developer Training Template (DSWD 4Ps)

A ready-to-use repository for building **DSWD 4Ps extension modules on OpenSPP v2** (Odoo 19). It gives you a local
OpenSPP in Docker, a developer CLI, Claude Code configured for OpenSPP work, and the standards we follow.

| What you get                   | Where                                                    |
| ------------------------------ | -------------------------------------------------------- |
| OpenSPP `2026.09` in Docker     | `docker/`, `docker-compose.yml`, pinned in `.env`         |
| Developer CLI                  | `odoo-project` (`.\odoo-project` on Windows)              |
| Claude Code setup              | `CLAUDE.md`, `.claude/`                                   |
| Standards and guides           | `docs/`                                                   |
| Your modules                   | `dswd_*/` folders you create at the repo root             |

## Before the Training

Install the tools listed in [training/SETUP.md](training/SETUP.md): Docker Desktop, Git, Python 3.11+, Node.js,
pre-commit, Claude Code. Windows users: read [docs/guides/windows-setup.md](docs/guides/windows-setup.md).

## Get Your Own Repository

1. Open this repository on GitHub and click **Use this template > Create a new repository**.
2. Choose your own account as **Owner**, name it (for example `dswd-4ps-modules`), keep it **Private**, and create it.
3. Clone it:

   ```bash
   git clone https://github.com/<your-account>/dswd-4ps-modules.git
   cd dswd-4ps-modules
   ```

## Quick Start

Windows (PowerShell):

```powershell
.\odoo-project doctor      # check Docker, Python, memory, WSL 2
.\odoo-project pull        # download the OpenSPP image (minutes)
.\odoo-project vendor      # download the OpenSPP source for reading
.\odoo-project start       # first start installs OpenSPP: 1-8 minutes
```

macOS / Linux:

```bash
./odoo-project doctor
./odoo-project pull
./odoo-project vendor
./odoo-project start
```

Then open <http://localhost:8069> and log in with `admin` / `admin`. Stop with `odoo-project stop`.

The image is private. Before the first `pull`, log Docker in to GitHub once with a token that has
`read:packages` (steps in [training/SETUP.md](training/SETUP.md), step 8). If `pull` still fails, run
`odoo-project build` instead; it takes 10 to 25 minutes.

## Daily Workflow

```bash
./odoo-project start                 # start (fast once installed)
# ... edit dswd_* modules ...
./odoo-project install dswd_wellbeing # install a new module into the running instance
./odoo-project update                # upgrade changed modules in the running instance
./odoo-project test dswd_wellbeing   # run one module's tests on a clean database
./odoo-project lint                  # ruff, ruff-format, prettier on changed files
git commit                           # pre-commit hooks run the full lint set
```

Full command reference: [docs/guides/odoo-project-cli.md](docs/guides/odoo-project-cli.md).

## Working with Claude Code

Run `claude` from the repo root. It loads `CLAUDE.md`, the path-scoped rules in `.claude/rules/`, and can read the
OpenSPP source in `vendor/openspp/` (it is blocked from editing it).

1. Start in **Plan mode** (shift+tab twice) and describe the feature
2. `/implement` runs the TDD workflow with subagents and expert review
3. `/verify-tests` confirms no tests were removed or weakened
4. `/commit` writes a conventional commit, `/pr` opens the pull request

| Command          | Purpose                                                 |
| ---------------- | ------------------------------------------------------- |
| `/implement`     | Full TDD workflow with subagents and expert review      |
| `/verify-tests`  | Check test integrity after subagent work                |
| `/analyze`       | Deep analysis mode — understand before implementing     |
| `/expert-review` | Parallel code review from multiple perspectives         |
| `/commit`        | Conventional commit (feat/fix/chore/docs/refactor/test) |
| `/pr`            | GitHub PR creation                                      |

See [docs/guides/claude-code-for-developers.md](docs/guides/claude-code-for-developers.md).

## Writing Modules

- Prefix: `dswd_` for modules, `dswd.` for models, `dswd_` for fields added to OpenSPP models
  ([ADR-001](docs/architecture/decisions/ADR-001-dswd-module-prefix.md))
- Extend OpenSPP with `_inherit`, inherited views, and hooks; never edit `vendor/openspp/`
  ([Extending OpenSPP](docs/guides/extending-openspp.md))
- Every module ships security groups under OpenSPP's categories, an ACL file, and tests
  ([Module Development](docs/guides/module-development.md), [Testing](docs/guides/testing-guide.md))

## Project Structure

```
├── odoo-project, odoo-project.cmd   # Developer CLI (+ Windows shim)
├── .env                             # OPENSPP_REF and image names (the single pin)
├── docker/                          # Dockerfile, entrypoint, Odoo config template
├── docker-compose.yml               # db, odoo-app, odoo-dev, jobworker, test
├── vendor/openspp/                  # OpenSPP source, read-only, gitignored (odoo-project vendor)
├── dswd_*/                          # Your modules
├── dswd_wellbeing/                  # Training module (Module 4): well-being level on households
├── docs/                            # Guides, principles, architecture, ADRs
├── scripts/                         # Lint, compliance, and test helpers used by the CLI and CI
├── tests/                           # Tests for the CLI and repo configuration
├── training/                        # Pre-training setup guide and 4Ps program reference
├── .claude/                         # Claude Code rules, agents, commands, hooks, settings
├── .github/                         # CI workflows and issue/PR templates
└── CLAUDE.md                        # Claude Code project instructions
```

## Updating to a Newer OpenSPP Release

Change `OPENSPP_REF` in `.env`, then `odoo-project pull` (or `build`), `odoo-project vendor --force`, and
`odoo-project stop -v -y` followed by `odoo-project start`.

## Documentation Map

| Area                       | Location                                                                     |
| -------------------------- | ---------------------------------------------------------------------------- |
| Pre-training setup         | [training/SETUP.md](training/SETUP.md)                                       |
| 4Ps program reference      | [training/4ps-program-reference.md](training/4ps-program-reference.md)       |
| Windows notes              | [docs/guides/windows-setup.md](docs/guides/windows-setup.md)                 |
| CLI reference              | [docs/guides/odoo-project-cli.md](docs/guides/odoo-project-cli.md)           |
| Extending OpenSPP          | [docs/guides/extending-openspp.md](docs/guides/extending-openspp.md)         |
| Module development         | [docs/guides/module-development.md](docs/guides/module-development.md)       |
| Testing                    | [docs/guides/testing-guide.md](docs/guides/testing-guide.md)                 |
| Claude Code                | [docs/guides/claude-code-for-developers.md](docs/guides/claude-code-for-developers.md) |
| Architecture and ADRs      | [docs/architecture/](docs/architecture/)                                     |
| Principles                 | [docs/principles/](docs/principles/)                                         |
| Docker details             | [docker/README.md](docker/README.md)                                         |
| OpenSPP documentation      | <https://docs.openspp.org>                                                   |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). This template repository accepts changes from its maintainer only;
participants work in their own repositories created from it.
