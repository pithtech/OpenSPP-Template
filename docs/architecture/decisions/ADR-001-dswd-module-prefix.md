# ADR-001: `dswd_` Module Prefix

**Status**: Accepted
**Date**: 2026-11-06

## Context

OpenSPP reserves the `spp_` prefix for its own modules (about 130 of them in release 2026.09) and the `spp.` namespace
for its models. Earlier DSWD 4Ps modules for OpenSPP v1 (Odoo 17) were named `spp_spmis_dswd4ps`,
`spp_attendance_dswd`, and `spp_school_grade_level`. That naming made our modules look like upstream ones, risked
name collisions with future OpenSPP modules, and hid which code was ours when debugging or upgrading.

We need one prefix that every participant uses during the training and that DSWD can keep afterwards, so that
modules written by different teams fit together and are easy to tell apart from OpenSPP.

## Options Considered

1. **`spp_*_dswd` suffix convention (v1 style)** — familiar, but collides with the upstream namespace, and the lint
   rules that protect upstream naming cannot distinguish ours from theirs.
2. **A per-team or per-participant prefix** — avoids collisions between teams, but produces modules that cannot be
   combined into one deployment without renaming, and gives the training no shared vocabulary.
3. **A single organisational prefix `dswd_` / `dswd.`** — clearly ours, never collides with upstream, works with the
   lint configuration (`.odoo-lint.yaml`), and matches how OpenSPP's own layering document describes country
   extensions.

## Decision

All modules created from this template use the `dswd_` module prefix and the `dswd.` model namespace. Fields added
to upstream models carry a `dswd_` prefix. Security groups are `group_dswd_{domain}_{level}`. The `spp_` prefix is
never used for our code.

## Consequences

- Lint rules (`.odoo-lint.yaml`, `scripts/lint/`) enforce the prefix automatically.
- A participant's module can be installed next to another participant's without renaming.
- Upstream OpenSPP modules remain untouched in the image and in `vendor/openspp/`, which keeps upgrades to newer
  releases a matter of bumping `OPENSPP_REF`.
- When a module turns out to be useful beyond DSWD, contributing it upstream means renaming it to `spp_*` as part of
  the OpenSPP pull request.
