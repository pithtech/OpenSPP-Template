---
paths:
  - "*/models/*.py"
  - "*/wizard/*.py"
  - "*/wizards/*.py"
---

# Odoo Python Rules (OpenSPP extensions)

## Naming

- Modules: `dswd_{domain}` / `dswd_{domain}_{feature}`. Never `spp_*` (reserved for upstream OpenSPP).
- Models: `dswd.{domain}` / `dswd.{domain}.{entity}` for new models. Extensions of upstream models keep the upstream
  name (`res.partner`, `spp.program`) and live in a file named after the model (`res_partner.py`, `spp_program.py`).
- Fields added to upstream models carry the `dswd_` prefix (`dswd_household_number`, `dswd_is_4ps_beneficiary`) so they
  never collide with upstream or other extensions.
- Fields: `is_*`/`has_*` (bool), `{model}_id` (M2O), `{model}_ids` (O2M/M2M), `{event}_date`.
- No abbreviations (`quantity` not `qty`, `beneficiary` not `ben`). See `docs/principles/naming-conventions.md`.
- States: `draft` → `pending` → `approved`/`rejected` → `cancelled`.
- Views: `view_{model}_form`, `view_{model}_list`, `action_{model}`, `menu_{model}`.

## Extending OpenSPP

- **Read the upstream module first.** The source is in `vendor/openspp/<module>/` (read-only; never edit it). Check the
  upstream model, its hooks, and its tests before adding anything.
- Prefer `_inherit` over new models. Registrants are `res.partner` records with `is_registrant=True`; groups
  (households) also have `is_group=True`. Programs are `spp.program`, membership `spp.program.membership`, cycles
  `spp.cycle`, entitlements `spp.entitlement`, change requests `spp.change.request`, areas `spp.area`.
- Use upstream hooks where they exist (`_pre_enrollment_hook()`, `_post_enrollment_hook()`); add your own
  `_pre_*_hook()` / `_post_*_hook()` pairs on `dswd.*` models for the next extension.
- Never expose database IDs in APIs. Registrant identifiers are `spp.registry.id` records (typed by `spp.id.type`); use
  those or external identifiers.
- Classifications (gender, civil status, relationship, tags) come from `spp.vocabulary` / `spp.vocabulary.code`. Do not
  add `fields.Selection` for values that an external standard or a deployment defines. Static selections are fine for
  internal workflow states only.
- Batch work goes through the job worker (`job_worker` module): `record.with_delay().method()` or
  `env["queue.job"].enqueue(...)`. Never `cr.commit()` in a loop.

## Odoo 19 Compatibility

- **Command API** — use `Command.create(vals)`, `Command.link(id)`, etc. Never tuple syntax `(0, 0, vals)`.
- **`group_expand`** — 2-param signature `(self, stages, domain)`. No `order` param.
- **SQL constraints** — still work; preferred for uniqueness. Use Python constraints for business logic.
- **Translation after unlink** — call `_()` before destructive operations, not after.

## Error Handling

- Use `ValidationError` for data validation, `UserError` for business rules.
- Error messages: state what happened, why, and how to fix.
- Logging: `_logger = logging.getLogger(__name__)`. Use lazy formatting, not f-strings.
- **Never log PII** — use `partner.id`, not names, national IDs, phone numbers, or addresses.
- No bare `except:` — catch specific exceptions.
- No `print()` — use `_logger`.

## Documentation

- **`_description`** — required on every model. Use a human-readable name (e.g., `"School Attendance"`, not
  `"dswd.school.attendance"`).
- **Class docstring** — add on models whose purpose is not obvious from `_name` and `_description` alone. Explain what
  the model represents in the 4Ps domain, not what fields it has.
- **Method docstrings** — required on public methods, overrides of Odoo methods (`create`, `write`, `unlink`,
  `action_*`), constraint methods (`_check_*`), and complex private methods. One-liner is fine for simple methods.
- **Inline comments** — explain _why_, not _what_. Comment non-obvious business rules, programme regulations, and
  workarounds for Odoo quirks.
- **No PII in comments** — do not use real names, IDs, or sensitive data in examples.
- **Field `help=` attribute** — use on fields where the label alone is ambiguous.

## Deep-Dive References

- `docs/guides/extending-openspp.md`
- `docs/principles/naming-conventions.md`
- `docs/principles/odoo19-compatibility.md`
- `docs/principles/error-handling.md`
- `docs/principles/api-design.md`
- `docs/principles/module-architecture.md`
