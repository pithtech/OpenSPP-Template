# Specifications

A specification describes one change: what the 4Ps users need, the rules, and how to tell that it works. Write one
before you ask Claude Code, or anyone, to build a module or change one. It is a file in the repository so that Claude
Code can read it, the team can review it in a pull request, and it stays as the record of what was asked.

A specification says **what** and **why**. It does not choose field names, files or classes: that is the plan's job.

## Where it fits

| File                                  | Holds                                                    |
| ------------------------------------- | -------------------------------------------------------- |
| `CLAUDE.md`, `.claude/rules/`         | The standing rules for every change                      |
| `docs/principles/`                    | The detail behind the rules                              |
| `docs/architecture/decisions/` (ADRs) | One decision that outlives one change                    |
| `docs/specs/<module>.md`              | One change: the need, the rules, the acceptance examples |
| `docs/planning/research-<topic>.md`   | What exists and what is missing, written by Claude Code  |
| `docs/planning/plan-<topic>.md`       | Files, tests first, steps, written by Claude Code        |

## The flow

1. Write the specification here from the template below. Link the GitHub issue, if there is one.
2. Record any decision that outlives the change as an ADR ([decisions/](../architecture/decisions/README.md)) and link
   it from the specification.
3. Ask Claude Code to read the specification and its ADRs, then the OpenSPP code they name, and to write a research
   file. Check it against the files.
4. Ask it to write the plan to a file. Add your notes in the file (`> NOTE: ...`) and ask it to address them.
5. Ask it to carry out the plan, test first. Review the result against the acceptance examples, then `/commit` and
   `/pr`; the pull request links the specification.

The participant guide, section 5.14, gives the prompts. [dswd_household_children.md](dswd_household_children.md) is a
worked specification to try the flow on.

## What to state, by kind of work

| Kind                             | State                                                                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| A new module with a new model    | The model and its fields with types; which are required; who reads and who writes (the three tiers); the menu; unique rules       |
| An extension of an OpenSPP model | The upstream model and view, by their names in `upstream/openspp/` (checked); what to add; where on the view; nothing upstream    |
| A customization through data     | The records to create; the vocabulary namespace and codes; `noupdate` or not; what keeps the codes valid; the test that proves it |

## Template

```markdown
# Specification: <module or change>

**Status**: Draft | Approved | Implemented\
**Issue**: <link, if any>\
**ADRs**: <links>

## The need

What the 4Ps users need, in their words, and why.

## Who uses it

The roles that read it and the roles that change it.

## Rules

Each rule as one numbered line: what counts, what does not, the limits.

## Where it appears

The screen, menu or report, by its name on screen.

## Acceptance examples

A table of inputs and the expected result. Each row becomes a test.

## Out of scope

What this change does not do.

## Upstream models and views it relies on

The OpenSPP names to check in `upstream/openspp/` before planning.
```
