# Architecture Decision Records (ADRs)

An ADR records one significant decision: the context, the options, what was decided, and the consequences. Write one
whenever a choice will be hard to reverse or will shape many modules (naming, security model, integration approach,
data model boundaries).

## ADR Index

| #                                           | Title                             | Status       | Date       | Summary                                              |
| ------------------------------------------- | --------------------------------- | ------------ | ---------- | ---------------------------------------------------- |
| [001](ADR-001-dswd-module-prefix.md)        | `dswd_` module prefix             | **Accepted** | 2026-11-06 | Our modules use `dswd_`; `spp_` stays upstream-only  |

## Status Legend

| Status         | Meaning                                         |
| -------------- | ----------------------------------------------- |
| **Proposed**   | Under discussion, not yet approved              |
| **Accepted**   | Approved, implementation pending or in progress |
| **Implemented**| Fully implemented                               |
| **Deprecated** | No longer recommended                           |
| **Superseded** | Replaced by another ADR                         |

## Creating a New ADR

1. Copy the template below to `ADR-NNN-short-title.md` using the next number
2. Fill in every section; keep it to one or two pages
3. Add a row to the index above
4. Open a pull request so the team can discuss it

### Template

```markdown
# ADR-NNN: Title

**Status**: Proposed
**Date**: YYYY-MM-DD

## Context

What situation or problem forces a decision? Which constraints apply (OpenSPP upgrade path, DSWD policy, data
protection, performance)?

## Options Considered

1. Option A — pros / cons
2. Option B — pros / cons

## Decision

What we will do, stated plainly.

## Consequences

What becomes easier, what becomes harder, what must change elsewhere (modules, docs, tests).
```
