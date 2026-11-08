An IT asset register built from scratch in Module 3 of the training: a new model, its views, its menu, its groups and
its tests, in plain Odoo. Nothing here is specific to 4Ps; the `dswd_` prefix is this project's naming rule.

The asset type is a hard-coded `Selection` on purpose, against this project's own checklist ("vocabulary over static
selections"): it is the before picture. Module 4 shows the OpenSPP way, a vocabulary edited under Settings.

## Key Capabilities

- Register an asset: tag, make and model, type, custodian, purchase and warranty dates, in use or not
- Compute whether an asset is still under warranty from its warranty end date
- Refuse a warranty end date earlier than the purchase date
- Three-tier access: viewer reads, officer creates and edits, manager also deletes; the manager tier is linked into
  the OpenSPP admin group so the `admin` user sees the app

## Key Models

- `dswd.asset` — one row per asset; `custodian_id` points at `res.users`

## Configuration

None. Assign users to the groups under Settings > Users & Companies > Users, section "DSWD Training: IT Assets".

## UI Location

IT Assets > Assets (top-level menu `menu_dswd_asset_root`, action `action_dswd_asset`; list, form and search views).

## Security

- `dswd_asset.group_asset_viewer` — read
- `dswd_asset.group_asset_officer` — read, write, create
- `dswd_asset.group_asset_manager` — read, write, create, delete; implied by `spp_security.group_spp_admin`
- `base.group_system` — full access (first row of `security/ir.model.access.csv`)

## Dependencies

- `base` — the ORM, `res.users`
- `spp_security` — the OpenSPP admin group the manager tier links into
