# Docker

Local Docker setup for the training: Odoo 19 (OCA/OCB) with OpenSPP v2 at the release pinned in `../.env`
(`OPENSPP_REF`), plus the OCA addons OpenSPP depends on and the job worker.

Use the `odoo-project` CLI rather than calling Docker directly; see `../docs/guides/odoo-project-cli.md`.

## Files

| File                   | Purpose                                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| `Dockerfile`           | Multi-stage build: `builder` (pip + downloads), `runtime`, `dev` (what you run)                     |
| `entrypoint.sh`        | Renders `odoo.conf` from environment variables, waits for the database, installs or updates modules |
| `odoo.conf.template`   | Odoo configuration template (addons path lives here)                                                |
| `requirements.txt`     | Extra Python packages for the image, beyond the OpenSPP release                                     |
| `requirements-dev.txt` | Optional debugging tools; not installed in the image                                                |

## What is inside the image

| Component    | Source                                                                        | Location in container               |
| ------------ | ----------------------------------------------------------------------------- | ----------------------------------- |
| Odoo 19      | `OCA/OCB` branch `19.0`                                                       | `/opt/odoo/odoo`                    |
| OpenSPP v2   | `OpenSPP/OpenSPP2` tag `${OPENSPP_REF}`                                       | `/mnt/extra-addons/openspp`         |
| Job worker   | `OpenSPP/odoo-job-worker` branch `19.0`                                       | `/mnt/extra-addons/odoo-job-worker` |
| OCA addons   | `server-ux`, `server-tools`, `server-backend`, `rest-framework` branch `19.0` | `/mnt/extra-addons/<name>`          |
| MuK theme    | `muk-it/odoo-modules` branch `19.0`                                           | `/mnt/extra-addons/muk-it`          |
| Your modules | this repository, volume-mounted read-only                                     | `/mnt/extra-addons/custom`          |

The addons path puts `custom` before `openspp`, so a `dswd_*` module can never be shadowed by an upstream module of the
same name.

## Getting the image

- **Pull** (fast, classroom default): `odoo-project pull` downloads `ghcr.io/pithtech/openspp-template:<OPENSPP_REF>`
  and tags it as the local image name.
- **Build** (10 to 25 minutes, needs a good connection): `odoo-project build`. Needed only when you change
  `requirements.txt`, `docker/requirements.txt`, or the Dockerfile.

## Moving to a newer OpenSPP release

1. Change `OPENSPP_REF` in `../.env`.
2. Run `odoo-project pull` (if the image has been published) or `odoo-project build`.
3. Run `odoo-project vendor --force` to refresh the read-only source checkout.
4. Run `odoo-project stop -v -y` then `odoo-project start` for a fresh database, or `odoo-project update` to upgrade an
   existing one.

## Environment variables

Set in `docker-compose.yml`; the defaults suit local work. The entrypoint validates every value and falls back to a safe
default when one is empty or malformed.

| Variable                | Default              | Purpose                                  |
| ----------------------- | -------------------- | ---------------------------------------- |
| `ODOO_DB_NAME`          | `odoo`               | Database name                            |
| `ODOO_INIT_MODULES`     | `spp_starter_sp_mis` | Modules installed on first start         |
| `ODOO_UPDATE_MODULES`   | empty                | Modules upgraded on every start          |
| `ODOO_WORKERS`          | `0`                  | Worker processes (0 = threaded, for dev) |
| `ODOO_DB_MAXCONN`       | `64`                 | Database connection pool size            |
| `LOG_LEVEL`             | `info`               | Odoo log level                           |
| `QUEUE_JOB_CONCURRENCY` | `2`                  | Parallel jobs in the job worker          |

Production deployment is out of scope for this template. OpenSPP maintains production compose files (Traefik and Nginx
variants) in `docker/` of the OpenSPP2 repository.
