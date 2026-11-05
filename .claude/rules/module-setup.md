---
paths:
  - "*/__manifest__.py"
  - "*/readme/*"
---

# Module Setup Rules

## Manifest (`__manifest__.py`)

### Required metadata fields

Every `dswd_*` manifest must include:

```python
"name": "DSWD 4Ps: {Feature}",
"category": "DSWD 4Ps/{Domain}",
"version": "19.0.1.0.0",
"author": "DSWD",
"license": "LGPL-3",
"development_status": "Alpha",
"maintainers": [],
"depends": ["spp_registry"],   # the upstream modules you extend, never more than needed
```

Only include `"external_dependencies": {"python": [...]}` when the module has external Python deps, and add the package
to the root `requirements.txt` as well.

### `application` and `auto_install`

- **`application=False`** for all `dswd_*` modules. A single bundle module (`dswd_starter`) may be `application=True` to
  install everything at once.
- **`auto_install`**: list syntax `["dep1", "dep2"]` for bridge modules (both deps required). `True` only for a
  single-dependency extension that must always accompany its dependency. Default is `False`.
- **Category**: `DSWD 4Ps/{Domain}` (Registry, Programs, Compliance, Attendance, Reports, Integration).

## Module Naming

- Pattern: `dswd_{domain}` or `dswd_{domain}_{feature}`
- Model prefix: `dswd.*` (extensions keep the upstream model name)
- XML ID prefix: `dswd_*`

## Module Structure

```
dswd_example/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
│   ├── ir.model.access.csv
│   └── groups.xml
├── data/
├── demo/
├── tests/
└── readme/
    └── DESCRIPTION.md
```

## DESCRIPTION.md

- 25-60 lines max. If longer, the module may be doing too much.
- Required sections: overview paragraph, Key Capabilities, Key Models, Configuration, UI Location, Security,
  Dependencies.
- Name models by `_name` (e.g., `dswd.school.attendance`), not prose.
- Name menu paths from actual `<menuitem>` XML — trace `parent=` to root.
- Name security groups by XML ID — don't say "authorized users".
- No marketing language ("robust", "comprehensive", "seamless").
- Verify all claims against source code. See `docs/principles/module-descriptions.md`.

## Dependencies

- Flow downward: `dswd_*` extensions → OpenSPP capabilities (`spp_programs`, `spp_change_request_v2`, ...) → OpenSPP
  foundation (`spp_registry`, `spp_security`, `spp_area`) → Odoo.
- Depend on the most specific upstream module that provides what you extend, not on a starter bundle.
- Minimize peer dependencies between `dswd_*` modules. No circular dependencies.

## Deep-Dive References

- `docs/principles/module-visibility.md`
- `docs/principles/module-architecture.md`
- `docs/principles/module-descriptions.md`
