# ADR-002: Counts That Depend on Age Are Computed, Not Stored

**Status**: Accepted\
**Date**: 2026-11-09

## Context

Several 4Ps figures on a household depend on its members' ages: the children aged 0 to 18 for health and education
grants, the school-age children, the elderly members. Odoo can keep such a figure as a **stored** computed field (a
database column, recomputed when a field it depends on is written) or as a **non-stored** one (computed each time the
record is read).

Age changes with no write to the database. A child turns 19 on their birthday, but nothing touches the household or the
member that day, so a stored count is not recomputed and stays wrong until something else changes the household. The
figures are used to explain grants to beneficiaries, so a stale number is worse than a slower one.

## Options Considered

1. **Stored, recomputed when a member or birthdate changes** — searchable and fast to list, but goes stale on every
   birthday; wrong without anyone noticing.
2. **Stored, with a nightly job that recomputes every household** — searchable, current to within a day, but the job
   rewrites millions of households each night (tracking, locks, job worker load) and is wrong for the rest of the day
   after a birthday.
3. **Not stored, computed when read** — always current, no job, no extra column; cannot be searched, filtered, grouped
   or used in a domain without a `search` method, and costs one read of the memberships for each household shown.

## Decision

A figure that depends on age is a non-stored computed field. It computes the age from `birthdate` on today's date, never
from OpenSPP's `age` field, which is text (`"5"`, or `"No Birthdate!"`).

## Consequences

- The number is right whenever it is shown, with no job to run or monitor.
- A list or report that needs to filter or group by it needs a `search` method or a report query of its own; that is
  part of that change's specification, not a reason to store the field.
- Showing the field on a list of many households costs one read of their memberships; acceptable on the form, to be
  measured before adding it to a list view.
- The first use is the specification [dswd_household_children](../../specs/dswd_household_children.md).
