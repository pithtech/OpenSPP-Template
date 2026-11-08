---
paths:
  - "*/security/*"
---

# Security Rules (OpenSPP three-tier model)

## Three-Tier Architecture

OpenSPP's `spp_security` module defines the categories and the central administrator group; domain modules define their
groups inside those categories. `dswd_*` modules follow the same pattern.

```
Tier 1: ROLES (composite, cross-domain)     — role_dswd_{role}            (optional, via base_user_role)
Tier 2: FUNCTIONAL PRIVILEGES (per domain)  — group_dswd_{domain}_{viewer|officer|manager}
Tier 3: BASE PERMISSIONS (technical)        — group_dswd_{domain}_{read|write|create}
```

Permission levels: `viewer` → `officer` → `manager` → admin (`spp_security.group_spp_admin`).

## Groups XML

- Depend on `spp_security` and put your privileges under an existing category (`spp_security.category_spp_registry`,
  `category_spp_programs`, ...) or define `category_dswd_{domain}` only when no upstream category fits.
- User-facing groups use `privilege_id` ref, not `category_id`.
- Link your manager group into the OpenSPP administrator so admins inherit it:

  ```xml
  <record id="spp_security.group_spp_admin" model="res.groups">
    <field name="implied_ids" eval="[Command.link(ref('group_dswd_attendance_manager'))]"/>
  </record>
  ```

- Use `Command.link()` in `implied_ids`, not tuple syntax. Use `user_ids` not `users`. Use `group_ids` not `groups_id`
  on menus.
- Never modify base Odoo groups (`base.group_user`, `base.group_erp_manager`) or upstream OpenSPP groups other than
  adding `implied_ids` to `group_spp_admin`.

## ACL File (`ir.model.access.csv`)

- Entry IDs: `access_{model}_{group}` (e.g., `access_dswd_attendance_officer`).
- Every new model MUST have ACL entries. Related models (lines, logs, wizards) need ACLs too.
- **Every custom `dswd.*` model MUST include a `base.group_system` row with full CRUD** (1,1,1,1) as the first data row.
- Fields added to upstream models inherit the upstream model's ACLs; add record rules if they need narrower access.
- Reference data must be readable by `base.group_user`.
- When tests fail with `AccessError`, fix the ACL — don't bypass with `sudo()`.

## Record Rules

- **Never use empty domains** — `domain_force=[]` is forbidden with write/create/unlink.
- **"See all" pattern** — use `[(1, '=', 1)]`, not `[]`.
- Always specify `groups` OR set `global="True"`.
- Wrap in `<data noupdate="1">`.
- Multi-company models MUST have a company isolation rule:
  `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`

## Anti-Patterns

- Empty domain with write permissions
- Global rule with write (allows ANY user to write)
- No group specification (applies to everyone)
- Modifying base Odoo or upstream OpenSPP groups

## Deep-Dive References

- `docs/principles/access-rights.md`
- `upstream/openspp/spp_security/readme/DESCRIPTION.md` (categories, admin group, extension pattern)
- `upstream/openspp/spp_registry/security/` (a complete domain example)
