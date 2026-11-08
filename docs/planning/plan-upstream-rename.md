# Plan: move the OpenSPP checkout from `upstream/openspp` to `upstream/openspp`

> **Status**: approved by Edwin on 2026-11-08 ("do the vendor rename first"); implemented on
> `fix/upstream-checkout-folder`.

## Why

The repo root is bind-mounted into the container as the first custom addons root. Odoo's SCSS importer
(`odoo/addons/base/models/assetsbundle.py`, `scss_importer`) resolves Bootstrap's `@import "vendor/rfs"` by asking
`file_path("vendor")`, which returns the first addons root that merely contains a directory named `vendor`, and only
falls back to Bootstrap's own folder when none does. With `upstream/openspp` present, every stylesheet bundle compiles
to Odoo's error stub and every page shows "A css error occured, using an old style to render this page". It
surfaces whenever bundles are rebuilt (module install or update, fresh database), so it would hit each participant on
their first module install. Proven on 2026-11-08 with two throwaway containers against the same database: with
`vendor/` the bundle is the error stub, without it the CSS is real.

An empty masking volume does not help (the directory would still exist). The checkout folder has to have another
name. `upstream/openspp` was chosen: descriptive, not an SCSS import root, and the CLI command keeps its name
`vendor`, so the setup instructions participants already have stay valid.

## Changes

1. **Tests first**: `tests/test_cli.py` (checkout path, `_stale_vendor_dir`, `start` warns), `tests/test_claude_config.py`
   (CLAUDE.md wording, settings deny rules, hook skip), `tests/test_docs.py` (skip `upstream/`, guard against
   `upstream/openspp` mentions).
2. **CLI**: `VENDOR_DIR = PROJECT_ROOT / "upstream" / "openspp"`; messages; `_stale_vendor_dir()`; `doctor` and `start`
   warn when a stale `vendor/` still exists at the repo root (stylesheets will break until it is moved or deleted).
3. **Config**: `.gitignore` (`/upstream/`), `.dockerignore`, pre-commit `exclude`, `.claude/settings.json` deny
   rules, `.claude/hooks/post-edit-lint.py` skip.
4. **Docs**: every `upstream/openspp` becomes `upstream/openspp` (guides, rules, agents, README, SETUP, training
   materials, planning records); a Known Pitfalls entry on top-level directory names and the SCSS importer; a note
   in the CLI guide.

## Verification

`uv run pytest tests/`, `pre-commit` on changed files, then on Edwin's machine: move the existing `vendor/` to
`upstream/` (or delete it and run `./odoo-project vendor`), `./odoo-project restart`, `./odoo-project update`, and
confirm no `assetsbundle` error in the log and a styled login page.
