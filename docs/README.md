# Project Documentation

Documentation for building DSWD 4Ps extension modules (`dswd_*`) on OpenSPP v2 (Odoo 19).

## Directory Structure

```
docs/
├── architecture/        # How dswd_* modules sit on OpenSPP, and decisions (ADRs)
│   └── decisions/
├── principles/          # Development standards (naming, security, testing, UI, ...)
├── guides/              # How-to guides (CLI, Windows setup, extending OpenSPP, testing, Claude Code)
└── planning/            # Research and plan that shaped this template
```

## Quick Links

| Need to...                                   | Go to...                                                                   |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| Set up Windows for the training              | [guides/windows-setup.md](guides/windows-setup.md)                         |
| Learn what 4Ps is and how it maps to OpenSPP | [../training/4ps-program-reference.md](../training/4ps-program-reference.md) |
| Use the developer CLI                        | [guides/odoo-project-cli.md](guides/odoo-project-cli.md)                   |
| Extend an OpenSPP model, view, or workflow   | [guides/extending-openspp.md](guides/extending-openspp.md)                 |
| Create a new module                          | [guides/module-development.md](guides/module-development.md)              |
| Write and run tests                          | [guides/testing-guide.md](guides/testing-guide.md)                         |
| Use Claude Code effectively                  | [guides/claude-code-for-developers.md](guides/claude-code-for-developers.md) |
| Understand the architecture                  | [architecture/vision.md](architecture/vision.md)                           |
| Read coding principles                       | [principles/](principles/)                                                 |
| Check or write an ADR                        | [architecture/decisions/](architecture/decisions/)                         |

## Getting Started

1. Follow the [README](../README.md) quick start to get OpenSPP running locally
2. Read [Architecture Vision](architecture/vision.md) to see where your modules fit
3. Read [Extending OpenSPP](guides/extending-openspp.md) before writing your first module
4. Keep [Development Principles](principles/README.md) open while coding

## Upstream Documentation

- OpenSPP documentation: <https://docs.openspp.org>
- OpenSPP source (pinned release, read-only): `vendor/openspp/` after `./odoo-project vendor`
- OpenSPP developer conventions: `vendor/openspp/AGENTS.md`
- Odoo 19 developer documentation: <https://www.odoo.com/documentation/19.0/developer.html>
