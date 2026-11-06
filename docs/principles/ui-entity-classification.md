# UI Entity Classification

Quick reference for choosing UI patterns based on entity type.

---

## The 6 Entity Classes

| Class | Examples | Record Count | Update Freq | UI Pattern |
|-------|----------|--------------|-------------|------------|
| **Master Data** | Categories, tags, settings, areas | <1k | Rare | Simple 1-2 tab form |
| **Workflow Entities** | Change requests, compliance verifications, grievances, entitlements | <10k | Regular | 4-5 tab form + kanban |
| **Registry Entities** | Registrants, households, schools, health facilities | 100k-10M | Moderate | 4-7 tab form, stat buttons |
| **Transactional** | Attendance records, event data, audit logs | 1M-100M | High | Minimal form, import/export |
| **Relationship (Simple)** | Area assignments, tags | Variable | Follows parent | Embedded only, no standalone view |
| **Relationship (Rich)** | Compliance lines, group membership | Variable | Moderate | Embedded + searchable list view |

---

## Classification Decision Tree

```
Does the entity have a state-based workflow?
├─ No → Is it a lookup/configuration table?
│   └─ Yes → MASTER DATA
│   └─ No → Does it link two other entities?
│       └─ Yes → Is it a log/event created in bulk?
│       │   └─ Yes → TRANSACTIONAL
│       │   └─ No → Does it need searchable list view?
│       │       └─ Yes → RELATIONSHIP (Rich)
│       │       └─ No → RELATIONSHIP (Simple)
│       └─ No → Is it a log/event created in bulk?
│           └─ Yes → TRANSACTIONAL
│           └─ No → REGISTRY ENTITY
└─ Yes → WORKFLOW ENTITY
```

---

## Prescribed Patterns by Class

| Class | Form Tabs | List Limit | Search Panel | Analytics | Kanban | O2M Edit |
|-------|-----------|------------|--------------|-----------|--------|----------|
| Master Data | 1-2 | None | ✅ Yes | ❌ No | ❌ No | Inline |
| Workflow | 4-5 | 80 | ✅ Yes | ✅ Include | ✅ Yes | Wizard |
| Registry | 4-7 | 80 | ⚠️ Selective | ⚠️ Separate | ❌ No | Wizard |
| Transactional | 2-3 | 80 | ❌ No | ❌ Pre-agg | ❌ No | Import |
| Relationship (Simple) | None | Parent | Parent | ❌ No | ❌ No | Parent |
| Relationship (Rich) | 2-3 | 80 | ⚠️ Yes | ⚠️ Separate | ❌ No | Wizard |

**Usage**: Classify your entity first → patterns are automatically prescribed

**Relationship (Simple) vs (Rich)**:
- **Simple**: Pure join table, no additional attributes beyond foreign keys (e.g., `spp.area`)
- **Rich**: Has own attributes, state, dates; needs reconciliation and auditing (e.g., `dswd.compliance.line` with period_date, state, condition_id)

---

## Reference Implementations

| Class | Module | Key Views |
|-------|--------|-----------|
| Master Data | `spp_area` | `views/area.xml` |
| Workflow Entity | `spp_change_request_v2` | `views/change_request_views.xml` |
| Registry Entity | `spp_vocabulary` | `views/vocabulary_code_views.xml` |
| Transactional | `spp_event_data` | `views/event_data_view.xml` |

---

## Examples by Class

### Master Data
- `spp.area` - Geographic areas
- `spp.vocabulary` - Vocabulary definitions (status codes, categories, types)
- `res.country` - Countries

**Characteristics**: Few records, rarely change, simple structure

---

### Workflow Entities
- `spp.change.request` - Registry change requests with approval
- `dswd.compliance` (planned) - Compliance verification per household and period
- `dswd.grievance` (planned) - Grievances raised by beneficiaries

**Characteristics**: State machine, approval workflows, moderate record count

---

### Registry Entities
- `res.partner` (as contact) - Contact records
- `dswd.school` (planned) - Schools attended by 4Ps children

**Characteristics**: Large record count, complex relationships, many tabs

---

### Transactional
- `dswd.log.entry` (planned) - Activity log entries
- `dswd.audit.log` - Audit trail entries

**Characteristics**: Millions of records, created in bulk, import/export heavy

---

### Relationship (Simple)
- `spp.area` - Area assignments (just partner_id + area_id)
- Many2many through tables with no extra fields

**Characteristics**: Pure join table, no additional attributes, embedded only

---

### Relationship (Rich)
- `dswd.compliance.line` (planned) - One condition checked for one beneficiary in a period (has period_date, state, condition_id)
- `spp.registry.id` - Entity identifiers (has type, value, system_uri)

**Characteristics**: Join table with attributes, state, dates; needs searchable list for reconciliation and auditing

---

**Full patterns**: See [ui-design.md](ui-design.md) for templates and [ui-performance.md](ui-performance.md) for scalability rules.
