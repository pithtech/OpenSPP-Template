# odoo-project CLI

Developer CLI for running, testing, and managing OpenSPP and your `dswd_*` modules locally with Docker. It is a
single Python script; on Windows run it as `.\odoo-project <command>` (PowerShell) or `python odoo-project <command>`.
Examples below use the macOS/Linux spelling `./odoo-project`.

## Prerequisites

Run `./odoo-project doctor` to verify your environment:

- **Docker Desktop** with Compose v2 (required), at least 4 GB memory (a running OpenSPP uses about 0.5 GB; the
  rest is headroom for Docker itself and for `build`), WSL 2 backend on Windows
- **Python 3.11+** (required; the CLI itself)
- **Git** (required)
- **pre-commit** and **Node.js** (used by `lint` and the git hooks)
- **argcomplete** (optional, tab completion)

## Quick Start

```bash
./odoo-project doctor          # 1. check prerequisites
./odoo-project pull            # 2. get the Docker image (or: build, 10-25 min)
./odoo-project vendor          # 3. get the OpenSPP source for reading
./odoo-project start           # 4. start; first start installs OpenSPP (several minutes)
# 5. open http://localhost:8069 (admin / admin)
./odoo-project test dswd_x     # 6. run a module's tests
./odoo-project stop            # 7. stop everything
```

## Where the OpenSPP Release Is Pinned

`.env` at the repo root:

```ini
OPENSPP_REF=2026.09
ODOO_IMAGE=openspp-template-dev
ODOO_IMAGE_REMOTE=ghcr.io/pithtech/openspp-template
```

`pull`, `build`, `vendor`, and `doctor` all read it. To move to a newer release: change `OPENSPP_REF`, then
`pull` (or `build`), `vendor --force`, and `stop -v -y` followed by `start`.

## Commands

Every command has a short alias shown in parentheses.

### pull — Get the published image

Downloads `ghcr.io/pithtech/openspp-template:<OPENSPP_REF>` and tags it as the local image, then pulls the
PostgreSQL image (from Docker Hub) so the first `start` downloads nothing. Minutes instead of the 10-25 minutes a
build takes. The image is private: log Docker in once with a GitHub token that has
`read:packages` (`docker login ghcr.io`, see `training/SETUP.md` step 8) before the first pull.

```bash
./odoo-project pull
```

### build (b) — Build the image locally

Needed only when the image is not published, or after you change `requirements.txt`, `docker/requirements.txt`,
or the Dockerfile. `start` and `test` detect such changes and offer to pull the published image again, building locally only if the pull fails.

```bash
./odoo-project build
./odoo-project build --no-cache       # full rebuild
```

### vendor — Fetch the OpenSPP source

Downloads the pinned release into `upstream/openspp/` (gitignored, read-only). Claude Code and you read it to learn
the models, views, groups, and tests you are extending.

```bash
./odoo-project vendor
./odoo-project vendor --force         # re-download (after changing OPENSPP_REF)
```

The folder is `upstream/openspp`, not `vendor/`: the repo root is mounted into the container as an addons root, and
Odoo's stylesheet build resolves Bootstrap's relative SCSS imports against any addons root that holds a folder with
one of these names: `forms`, `helpers`, `mixins`, `utilities`, `vendor`. Such a top-level folder makes every page
lose its styling. `doctor` reports them, `start` refuses to run, and a pre-commit hook blocks them. If you have an
old `vendor/` from an earlier version of this template, move it (`mv vendor upstream`) or delete it, then run
`./odoo-project resetassets`.

### start (s) — Start OpenSPP

Starts the database, Odoo, and the job worker. Defaults to the **ui** profile on port 8069. On a fresh database it
installs the default modules (`spp_starter_sp_mis`) and waits until they are installed.

```bash
./odoo-project start                     # ui profile, port 8069
./odoo-project start --demo=demo         # fresh database with the MIS demo data
./odoo-project start --wipe -y           # delete all data first, then start
./odoo-project start --profile dev       # dynamic port, auto-reload enabled (see note below)
./odoo-project start --no-build          # skip the image freshness check
```

| Option        | Description                                                        |
| ------------- | ------------------------------------------------------------------ |
| `--profile`   | `ui` (fixed port 8069, default) or `dev` (dynamic port)            |
| `--demo`      | Demo profile to install on a fresh database (see Demo Profiles)    |
| `--wipe`      | Delete all data (database + filestore) before starting             |
| `--no-watch`  | Disable auto-reload (dev profile enables it by default)            |
| `--no-build`  | Skip the Docker image freshness check                              |
| `-y, --yes`   | Skip confirmation prompts                                          |

Auto-reload relies on file-change events reaching the container. On Windows with the repository on the `C:` drive
they may not arrive through the bind mount, so Odoo may keep running old code: run `.\odoo-project restart` (Python)
or `.\odoo-project update` (XML, data) as on the ui profile.

### stop — Stop all services

```bash
./odoo-project stop
./odoo-project stop -v -y        # also delete the database and filestore, no prompt
```

### restart (r) — Restart Odoo

```bash
./odoo-project restart
```

### test (t) — Run module tests

Runs a module's tests in a one-off container against a temporary database. Does not touch your running instance.

```bash
./odoo-project test dswd_attendance
./odoo-project t dswd_attendance                         # alias
./odoo-project test dswd_attendance --tags=post_install
```

| Option     | Description                              |
| ---------- | ---------------------------------------- |
| `--tags`   | Odoo test tags filter                    |

The full Odoo log is saved under your temp directory; the path is printed after each run.

### update (u) — Upgrade changed modules

Uses `click-odoo-update` inside the running container to detect and upgrade modules whose files changed.

```bash
./odoo-project update
```

`update` only upgrades modules that are already installed. To add a new module, use `install`.

### install (i) — Install new modules

Runs `odoo -i` inside the running container, then restarts Odoo so the registry picks up the new modules. Equivalent
to Apps > Update Apps List > Install in the UI.

```bash
./odoo-project install dswd_wellbeing
./odoo-project install dswd_wellbeing dswd_id_types   # several at once
```

### resetassets — Rebuild the styling

Odoo keeps a compiled asset bundle as long as its version hash matches, and that hash comes from the source files,
not from whether the compile succeeded. After a broken stylesheet build (pages shown unstyled, with "A css error
occured" at the bottom), fix the cause, then delete the stored bundles and restart:

```bash
./odoo-project resetassets
```

### resetdb — Drop and recreate the database

```bash
./odoo-project resetdb -y
./odoo-project resetdb --demo=demo start     # reset, then start (chained)
```

### logs (l), shell (sh), sql, url, status (st)

```bash
./odoo-project logs -f                       # follow Odoo logs
./odoo-project logs jobworker                # job worker logs
./odoo-project shell                         # Odoo Python shell:  env["res.partner"].search_count([("is_registrant","=",True)])
./odoo-project sql "SELECT count(*) FROM res_partner WHERE is_registrant"
./odoo-project url --open                    # open the running instance in a browser
./odoo-project status                        # container status
```

### lint — Run formatters and linters

```bash
./odoo-project lint                          # changed files
./odoo-project lint dswd_attendance/models/*.py
```

PowerShell does not expand `*.py`: list the files by name, or run `lint` with no arguments for the changed files.

### doctor — Check prerequisites

Checks Docker, Compose, the daemon, backend (WSL 2 on Windows), memory, Python, Node.js, Git, pre-commit,
argcomplete, the pinned release, whether the image is present, whether `upstream/openspp` is current, and port 8069.

### fix-odoo19, audit-security

```bash
./odoo-project fix-odoo19 dswd_attendance --dry-run   # rewrite legacy Command tuples
./odoo-project audit-security dswd_attendance         # static ACL/group audit
./odoo-project audit-security dswd_a dswd_b --json    # several modules, JSON report
```

### activate — Tab completion

```bash
eval "$(./odoo-project activate)"            # add to ~/.zshrc or ~/.bashrc; needs argcomplete
```

## Demo Profiles

| Profile | Modules installed                              | Use                                     |
| ------- | ---------------------------------------------- | --------------------------------------- |
| `base`  | `spp_starter_sp_mis`                           | Default: registry, programs, API, approvals |
| `demo`  | `spp_mis_demo_v2`                              | Generated registrants, programs, cycles |
| `phl`   | `spp_mis_demo_v2,spp_demo_phl_luzon`           | Demo data with Luzon administrative areas |

Any module list also works: `--demo=spp_starter_social_registry`.

## Command Chaining and Dry Run

```bash
./odoo-project resetdb --demo=demo start       # options bind to the command before them
./odoo-project -n stop -v                      # print the docker commands without running them
```

## Configuration

Personal defaults in `~/.odoo-project.toml`. Create it in a text editor and save it as UTF-8. On Windows do not
create it with `echo ... >` in PowerShell 5.1, which writes UTF-16; the CLI then warns and ignores the file.

```toml
default_demo = "base"
default_profile = "ui"
default_db = "odoo"
```

## Troubleshooting

| Symptom                                   | What to do                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------- |
| Port 8069 already in use                  | `./odoo-project stop`; `doctor` says whether it is in use; on Windows `netstat -ano \| findstr 8069` shows the PID |
| "Docker image may be outdated"            | Accept the pull (it is quick when the image is already current); if the pull fails, log in to GHCR or run `./odoo-project build` |
| Module not updating after code changes    | `./odoo-project update`, then `restart` if needed                               |
| New module not found or not installed     | `./odoo-project install <module>`; `update` does not install new modules        |
| Pages unstyled, "A css error occured" | `doctor` names the top-level folder to move; then `./odoo-project resetassets` |
| First start seems stuck                   | Installing `spp_starter_sp_mis` takes 1-8 minutes; `logs -f` shows progress     |
| Tests fail but the UI works               | Tests run on a fresh database; check the log path printed by `test`             |
| Database connection errors                | `doctor`, then `status`, then `logs db`                                         |
| Windows-specific problems                 | See [windows-setup.md](windows-setup.md)                                        |
