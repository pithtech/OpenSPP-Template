# Specification: children aged 0 to 18 in each household

**Status**: Approved\
**Issue**: none (training example)\
**ADRs**: [ADR-002: counts that depend on age are computed, not stored](../architecture/decisions/ADR-002-computed-counts-not-stored.md)

## The need

4Ps health and education grants are tied to the children of the household aged 0 to 18. When a household's grants are
questioned, the City/Municipal Link (C/ML) has to count those children by hand from the member list. Each household
should show the number directly.

## Who uses it

City/Municipal Links and provincial and regional staff read it on the household. Nobody types it: it follows from the
members and their birthdates.

## Rules

1. Count the household's **current** members only: a member whose membership has ended is not counted.
2. A member is a child when their age, from their **birthdate**, is 0 to 18 inclusive on today's date. A member who is
   18 counts; a member who is 19 does not.
3. A member with no birthdate is not counted.
4. The number is always current: a child who turns 19 stops counting on that day, with no other change to the household
   (ADR-002).

## Where it appears

On the household form, Profile page, labelled "Children (0 to 18)", read-only. Households are under Registry > Browse
All (Audit) > All Groups.

## Acceptance examples

| Household members                                              | Children (0 to 18) |
| -------------------------------------------------------------- | ------------------ |
| Aged 5, 12 and 30, plus one aged 17 whose membership has ended | 2                  |
| Aged 18 and 19                                                 | 1                  |
| Aged 7, plus one member with no birthdate                      | 1                  |
| No members                                                     | 0                  |

## Out of scope

- Searching, filtering or grouping households by the number (ADR-002 explains why it is not stored).
- Changing how OpenSPP computes or shows a member's age.
- Any rule about grant amounts.

## Upstream models and views it relies on

Check each name in `upstream/openspp/` before planning:

- `res.partner`: a household has `is_group` set; an individual has `birthdate`.
- The household's memberships and the membership model, with whatever marks a membership as ended.
- The household form's view in `spp_registry`, and a named element on its Profile page to place the number after.
