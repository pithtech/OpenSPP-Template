---
paths:
  - "*/views/*.xml"
  - "*/data/*.xml"
---

# Odoo XML Rules

## Odoo 19 Syntax

- **XPath class matching** — use `hasclass('classname')`, never `@class='classname'`.
- **Search view `<group>`** — no attributes allowed (`expand`, `string` are invalid in Odoo 19).
- **Don't use `@title`** as XPath selector — use `@class`, `@name`, or other valid attributes.
- **Command API in XML** — use `Command.link(ref('...'))` not tuple syntax in `eval=`.
- Use `<list>` not `<tree>` for list views.

## Extending OpenSPP Views

- Find the upstream view in `vendor/openspp/<module>/views/` and inherit it with `inherit_id="<module>.<view_id>"`.
- Target **named** elements (`//group[@name='...']`, `//page[@name='...']`, `//field[@name='...']`), never positional
  paths. OpenSPP registrant and program forms expose named groups and placeholder `<div name="..."/>` sections for
  exactly this purpose.
- Keep one inherited view per upstream view per module; group all your changes in it.
- Prefix your own XML IDs with the module name context in mind: `view_res_partner_form_dswd`,
  `view_dswd_attendance_form`.

## Form Layout

- **Minimal header** — only status bar and action buttons in `<header>`.
- **Content in tabs** — all editable fields in `<notebook>` tabs, not header.
- **Multi-column** — use nested `<group>` pattern: `<group col="2"><group>...</group><group>...</group></group>`.
- **Named groups** — all sections must have `name=` for extensibility.
- **Extension points** — add `<div name="..." invisible="1"/>` or `<group name="..." invisible="1"/>`.

## State Colors & Accessibility

- States must use both **icon AND color** (8% of males are colorblind).
- State colors: draft=`secondary`, pending=`warning`, approved=`success`, rejected=`danger`.
- Icons: draft=`fa-pencil`, pending=`fa-clock-o`, approved=`fa-check`, rejected=`fa-times`.

## Lists

- Use `optional="show"` / `optional="hide"` for optional columns.
- Odoo defaults to `limit="80"` — only set explicitly if you need a different value.

## Widgets

- `statusbar` in form header, `badge` in lists/forms, `web_ribbon` for terminal states.
- `boolean_toggle`, `many2many_tags`, `monetary`, `many2one_avatar_user` — prefer these over defaults.

## Comments

- **Section headers** — use `<!-- Section: Name -->` comments to separate logical groups in view files.
- **Data files** — comment groups of records in data XML.
- **Non-obvious attributes** — comment `domain` or `context` expressions that encode business rules.
- **Do not comment self-evident XML** — `<!-- Name field -->` above `<field name="name"/>` adds noise.

## Menu Structure

- Attach menus under the OpenSPP application menus (Registry, Programs, ...) when the feature belongs there; create a
  top-level menu only for a genuinely new application area.
- **Configuration is app-level** — one shared Configuration menu per app, sequence 90, gated by
  `groups="base.group_system"` or the domain's config-admin group.
- **No abbreviations in XML IDs** — `menu_dswd_configuration`, not `menu_dswd_config`.

## Deep-Dive References

- `docs/principles/odoo19-compatibility.md`
- `docs/principles/ui-design.md`
- `docs/principles/ui-entity-classification.md`
