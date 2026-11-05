# Contributing

## In Your Own Repository

Repositories created from this template belong to you. The workflow we teach:

1. Create a branch from `main`: `git checkout -b feat/attendance-form`
2. Write a failing test, then the code, then make the test pass (`./odoo-project test <module>`)
3. Run `./odoo-project lint` and let the pre-commit hooks pass on commit
4. Commit with a conventional message, open a pull request with the template, and review it (or ask Claude Code's
   `/expert-review`)

### Commit Messages

```
{type}({scope}): {description}
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`. Imperative mood, present tense. The subject says why; the
diff shows what.

### Standards

- [Naming Conventions](docs/principles/naming-conventions.md)
- [Access Rights](docs/principles/access-rights.md)
- [Testing](docs/principles/testing.md)
- [Extending OpenSPP](docs/guides/extending-openspp.md)

## To This Template

Only the maintainer commits to `pithtech/OpenSPP-Template`. Found a problem with the template itself (CLI, Docker image,
docs)? Open an issue on the template repository and describe how to reproduce it.

## Community

- [Code of Conduct](code_of_conduct.md)
- [Security Policy](SECURITY.md)
