# Scripts

Helper scripts used by the `odoo-project` CLI, pre-commit, and CI. Participants normally do not run these directly; use
the CLI commands listed in `docs/guides/odoo-project-cli.md`.

| Path                    | Used by                         | Purpose                                                    |
| ----------------------- | ------------------------------- | ---------------------------------------------------------- |
| `lint/`                 | pre-commit, Claude Code hook    | Project lint rules (naming, XML ids, ACLs, Odoo 19 syntax) |
| `compliance/`           | pre-commit                      | Validates `compliance.yaml` security specs against modules |
| `test_single_module.sh` | CI, `odoo-project test --local` | Runs one module's tests against a temporary database       |
| `detect_modules.py`     | CI                              | Finds `dswd_*` modules changed by a commit range           |
| `audit-api-auth.py`     | pre-commit                      | Verifies FastAPI endpoints require authentication          |
| `security_audit.py`     | `odoo-project audit-security`   | Static audit of ACLs, groups, and record rules             |
| `audit-security.sh`     | `odoo-project audit-security`   | Wrapper that runs the audit across modules                 |
| `fix-odoo19.sh`         | `odoo-project fix-odoo19`       | Rewrites legacy Command tuples to the Odoo 19 Command API  |
| `setup_test_env.sh`     | Claude Code on the web          | Builds a local Odoo environment when Docker is unavailable |

See `lint/README.md` and `compliance/README.md` for rule details.
