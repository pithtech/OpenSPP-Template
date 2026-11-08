# Claude Code for Developers

How Claude Code is configured for this project and how to get the most out of it.

## What Claude Sees Automatically

### Always loaded (every conversation)

- **`CLAUDE.md`** — project overview, architecture, checklist, commands, pitfalls
- **Auto-memory** — persistent notes about patterns discovered across sessions

### Loaded when you edit matching files (`.claude/rules/`)

| Editing | Rule loaded | What it covers |
|---------|-------------|----------------|
| `models/*.py`, `wizard/*.py` | `odoo-python.md` | Naming, extending OpenSPP models, Command API, logging |
| `views/*.xml`, `data/*.xml` | `odoo-xml.md` | Odoo 19 view syntax, form layout, accessibility |
| `security/*` | `security.md` | OpenSPP three-tier groups, ACLs, record rules |
| `tests/*.py` | `testing.md` | Coverage targets, Odoo test quirks, approval flows |
| `__manifest__.py`, `readme/*` | `module-setup.md` | Module visibility, architecture, descriptions |

### NOT loaded automatically (read on demand)

- **`docs/principles/`** — Deep-dive principle files. Claude reads these when it needs detail beyond what the rules provide.
- **`docs/architecture/`** — Architecture vision and ADRs.
- **`upstream/openspp/`** — The OpenSPP source for the pinned release. Claude reads the module it extends before writing code; it is denied edit access to this folder by `.claude/settings.json`.

## Recommended Workflow

1. **Start with Plan mode** (shift+tab twice) for non-trivial features
2. **Use `/implement`** for TDD workflow with subagents
3. **Use `/verify-tests`** after subagent work to catch removed tests
4. **Use `/commit`** for conventional commit format
5. **Use `/pr`** for GitHub PR creation

## Available Subagents

| Agent | Best for |
|-------|----------|
| `@odoo-developer` | Core implementation (models, views, security) |
| `@code-reviewer` | Security, naming, Odoo 19 compliance review |
| `@ux-expert` | UI/UX patterns, form layouts |
| `@code-simplifier` | Reducing complexity after implementation |
| `@verify-module` | Testing module installation and tests |

## Personal Setup

### `settings.local.json` (not committed)

Personal permissions and preferences go in `.claude/settings.local.json`. This file is gitignored
so each developer can customize without affecting others.

```json
{
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "WebSearch"
    ]
  }
}
```

### `settings.json` (committed, team-shared)

Team-wide permissions for project scripts are in `.claude/settings.json`. These apply to everyone.

## Tips

- If Claude isn't following a principle, ask it to read the specific file: "Read `docs/principles/access-rights.md`"
- The rules are concise summaries — for full rationale and examples, point Claude to the source principle doc
- After discovering a recurring mistake, propose an update to the relevant rule or Known Pitfalls in CLAUDE.md

## OpenSPP Plugin

`.claude/settings.json` registers the `OpenSPP/claude-plugins` marketplace, which offers `odoo-lsp`: Odoo-aware
code navigation (model and field lookups) through the `odoo-ls` language server. It is not enabled by default
because the language server needs an Odoo core checkout on your machine, which this template does not ship. If
you have one, run `/plugin install odoo-lsp@openspp-plugins` inside Claude Code and point its `odools.toml`
config at your Odoo path.
