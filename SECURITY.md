# Security Policy

## Reporting a Vulnerability

Do not open a public issue for security problems.

- **In your own `dswd_*` modules**: fix on a branch, add a test that proves the fix, and merge through review.
- **In this template** (CLI, Docker image, workflows): email the maintainer listed in `CONTRIBUTORS.md`.
- **In OpenSPP itself**: follow OpenSPP's policy at <https://github.com/OpenSPP/OpenSPP2/security>.

## Supported Versions

| Component | Supported                                    |
| --------- | -------------------------------------------- |
| OpenSPP   | The release pinned in `.env` (`OPENSPP_REF`) |
| Odoo      | 19.0                                         |

## Practices Enforced Here

- pre-commit runs gitleaks (secrets), bandit (Python security), semgrep (Odoo security rules), and the project ACL
  checks on every commit
- `./odoo-project audit-security` audits groups, ACLs, and record rules
- No PII in logs, comments, or test data; see [Error Handling](docs/principles/error-handling.md)
- Access rights follow [docs/principles/access-rights.md](docs/principles/access-rights.md)
