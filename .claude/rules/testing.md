---
paths:
  - "*/tests/*.py"
---

# Testing Rules

## Coverage Targets

| Module Type         | Target |
| ------------------- | ------ |
| Core domain modules | 85%+   |
| API modules         | 90%+   |
| Utility/helper      | 80%+   |
| UI-only             | 60%+   |

## Test Structure

- Use `TransactionCase` for unit tests (rolled back per test). Tag with `@tagged("post_install", "-at_install")`.
- `setUp()` calls `super().setUp()` then creates test data.
- For registrant fixtures, reuse upstream helpers: `from odoo.addons.spp_registry.tests.common import RegistryCommon`
  (see `upstream/openspp/spp_registry/tests/common.py`); `spp_programs/tests/common.py` has program fixtures.
- Test names: `test_{what_it_tests}` — descriptive, not generic.
- Docstrings explain the expected behavior, not the implementation.

## Rules

- **NEVER remove or weaken existing tests** without explicit approval.
- Tests must run with appropriate user context (officer, manager), not just admin.
- When fixing security issues, update test user context — don't skip tests.
- If tests can't run due to install issues, fix the install — don't mark tests as skipped.
- Test output must be clean: if a test expects an error log, capture it with `self.assertLogs` or `mute_logger`.

## Odoo Testing Quirks

- `assertRaises` does NOT support tuples — use a single exception type.
- Use `with self.assertRaises(ValidationError):` not `(ValueError, UserError)`.
- Use `with_context(tracking_disable=True)` in test setUp to avoid mail side effects.
- Registrants need `is_registrant=True` (and `is_group=True` for households) or upstream domains will not find them.

## Approval Flow Test Data

- `spp.approval.mixin` records: `approval_state='pending'` requires pending `spp.approval.review` records;
  `approval_state='approved'` requires all reviews approved.
- Create the full approval chain — don't just set the state field directly.

## Running Tests

```bash
./odoo-project test <module_name>              # Docker, isolated database, cross-platform
./odoo-project test <module_name> --tags=...   # filter by tag
```

## Deep-Dive References

- `docs/principles/testing.md`
- `docs/guides/testing-guide.md`
- `docs/principles/odoo19-compatibility.md`
- `docs/principles/approval-workflows.md`
