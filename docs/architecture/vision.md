# Architecture Vision

How DSWD 4Ps extension modules sit on top of OpenSPP, and the rules that keep them upgrade-safe.

## Mission

Extend OpenSPP v2 for the Pantawid Pamilyang Pilipino Program (4Ps) with small, well-tested `dswd_*` modules that
add 4Ps-specific data, rules, workflows, and reports **without modifying OpenSPP itself**. OpenSPP releases monthly;
our modules must survive each upgrade with no more than a version bump.

## Architecture Principles

- **Extend, never fork.** OpenSPP source lives in the Docker image and in the read-only `vendor/openspp/` checkout.
  Changes to upstream behaviour go through `_inherit`, hooks, inherited views, and configuration. Upstream bugs go
  to OpenSPP as pull requests.
- **One concern per module.** `dswd_attendance` does attendance; it does not also do grievances.
- **Depend on the specific capability.** A module depends on `spp_programs`, not on the `spp_starter_sp_mis`
  bundle, so it installs on any OpenSPP deployment that has programs.
- **Security is part of the feature.** Every module ships its groups under OpenSPP's security categories, its ACLs,
  and tests that run as officer and manager users.
- **Odoo-native data.** Use the Odoo ORM and OpenSPP models (`res.partner` registrants, `spp.program`,
  `spp.entitlement`). No parallel database, no raw SQL outside migrations.
- **Identifiers over database ids.** Anything that leaves the system (APIs, exports, QR codes) uses
  `spp.registry.id` identifiers or external ids.

## Layers

```
Layer 3: DSWD 4Ps EXTENSIONS   dswd_registry_ph, dswd_attendance, dswd_compliance, dswd_grievance, dswd_reports
    ↓
Layer 2: OPENSPP CAPABILITIES  spp_programs (programs, cycles, entitlements), spp_change_request_v2, spp_event_data,
                               spp_grm, spp_api_v2, spp_approval, spp_service_points
    ↓
Layer 1: OPENSPP FOUNDATION    spp_registry, spp_security, spp_area, spp_vocabulary, spp_base_common
    ↓
Layer 0: ODOO + OCA            base, mail, web; base_user_role, job_worker, fastapi, extendable
```

Dependencies flow downward only. A Layer 3 module may depend on other Layer 3 modules, but keep that rare and
never circular.

## Module Map (indicative)

| Module                 | Extends                                   | Purpose                                                |
| ---------------------- | ----------------------------------------- | ------------------------------------------------------ |
| `dswd_registry_ph`     | `spp_registry`, `spp_area`                | Philippine identifiers, household fields, PSGC areas   |
| `dswd_attendance`      | `spp_event_data`, `spp_programs`          | School and health attendance records per cycle         |
| `dswd_compliance`      | `spp_programs`                            | Condition verification driving cash grant eligibility  |
| `dswd_grievance`       | `spp_grm`                                 | 4Ps grievance categories and escalation rules          |
| `dswd_reports`         | the above                                 | Programme reports and dashboards                       |
| `dswd_starter`         | the above                                 | One-click install bundle for a 4Ps deployment          |

The lab exercises define the actual modules; this map shows the shape, not a commitment.

## Odoo 19 and OpenSPP Strategy

- Registrants are `res.partner` records (`is_registrant=True`); households are also groups (`is_group=True`).
- Program logic hangs off `spp.program` managers (eligibility, cycle, entitlement) and the enrolment hooks.
- Background work uses the job worker (`with_delay()`); it runs as the `jobworker` compose service.
- Classifications use `spp.vocabulary` codes with namespace URIs, so they interoperate with DCI and other systems.
- Maintain upgrade-safe patterns: `_inherit` extensions, named XPath targets, no core patches.

## Related Documents

- [Extending OpenSPP](../guides/extending-openspp.md)
- [Module Architecture](../principles/module-architecture.md)
- [Access Rights](../principles/access-rights.md)
- [Architecture Decisions](decisions/)
