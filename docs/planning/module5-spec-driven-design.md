# Module 5 Addition: From a Specification to a Module with Claude Code (design)

> **Status**: approved by Edwin (2026-11-09), with the four decisions of section 9. **As built**: Demo B is four
> slides (the flow, what a specification states, the specification with research and plan, then test first), so the
> deck has 48 slides; the objectives slide gained objectives 6 and 7 to match guide 5.1; the reference build has five
> tests, one per acceptance example plus the form, all passing. Builds on the approved
> [module5-claude-code-design.md](module5-claude-code-design.md).
> **Edwin's answers (2026-11-09)**: the hour may run past 4:55 (it is the end of Module 5); the specification is a file,
> and a pre-written one for the demo module goes into the template repository now, so participants can try it after the
> training; a specification template goes into the template repository; the guide gets a new section 5.14.

---

## 1. The gap

Guide 5.13 shows Claude Code answering a question and writing a change from a one-line prompt. Real work does not start
from a prompt: it starts from a written request and the project's decisions. The template already has the places for
them (`docs/architecture/decisions/` with an ADR template and ADR-001, `docs/principles/`, `docs/planning/`, the feature
request issue template, `/implement`, which carries out "the plan discussed above"), but neither the guide nor the demo
shows how they feed Claude Code.

What participants should leave with: **the specification and the decisions are files in the repository; Claude Code
reads them, writes its research and its plan as files, you review each one, and only then does it write the test and
the code.** That is how the template itself was built.

## 2. What goes where

| File                                         | Holds                                                         | Written by                     | Lifetime            |
| -------------------------------------------- | ------------------------------------------------------------- | ------------------------------ | ------------------- |
| `CLAUDE.md`, `.claude/rules/`                | The standing rules for every change                            | The team                       | The project         |
| `docs/principles/`                           | The detail behind the rules (security, naming, testing, UI)   | The team                       | The project         |
| `docs/architecture/decisions/ADR-NNN-*.md`   | One decision that outlives one change, with its consequences  | The developer, reviewed in a PR | Until superseded    |
| `docs/specs/<module>.md` (**new folder**)    | One change: the need, the rules, acceptance examples, scope   | The developer or the analyst   | Until the change merges, then the record |
| `docs/planning/research-<topic>.md`          | What exists, what is missing, open questions                  | Claude Code, reviewed by you   | The change          |
| `docs/planning/plan-<topic>.md`              | Files, tests first, steps, risks                              | Claude Code, annotated by you  | The change          |

## 3. The flow (guide 5.14, Demo B)

1. **Write the specification** in `docs/specs/<module>.md` from the template (section 5). Link the GitHub issue, if any.
2. **Record any lasting decision** as an ADR (the template in `docs/architecture/decisions/README.md`), and link it from
   the specification.
3. **Research**: "Read `docs/specs/<module>.md` and the ADRs it links, then the OpenSPP models they name in
   `upstream/openspp/`. Write `docs/planning/research-<topic>.md`: what exists, what is missing, your questions. Do
   not write code." Review it against the files (5.13's "ask it to read, then check").
4. **Plan**: "Write the plan to `docs/planning/plan-<topic>.md`: the files, the tests first, the steps." Annotate it
   in the file (a line starting `> NOTE:`), then "Address my notes in the plan."
5. **Implement, test first**: "Carry out the plan, test first: write the failing test, run it, then the code." For a
   larger change, `/implement` does the same with its agents and an expert review (say "test first": 5.13).
6. **Review** with 5.13's checklist, plus one point: does the code do what the specification's acceptance examples say?
7. **`/commit`, `/pr`**: the pull request body links the specification and the ADR.

## 4. What a specification states, by kind of work

The three skills of Day 2 and Module 6. The guide gives what to state, not the content, so it hands out no Module 6
answer.

| Kind                                   | The specification states                                                                                                   |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Developing a new module (a new model)  | The model and its fields with types; required fields; who reads and who writes (the three tiers); the menu; the list and form; unique rules |
| Extending an OpenSPP model             | The upstream model and view, by their names in `upstream/openspp/` (checked); the `dswd_` fields; where on the view; what must not change upstream |
| Customizing through data               | The records to create; vocabulary namespace and codes; `noupdate` or not; the constraint that keeps codes valid; the test that proves the data |
| All three                              | The 4Ps need in the users' words; the rules; acceptance examples as a table; out of scope; the ADRs it relies on           |

## 5. New files in the template repository

1. **`docs/specs/README.md`**: what a specification is, when to write one, the flow (section 3) in five lines, and the
   template:

   ```markdown
   # Specification: <module or change>

   **Status**: Draft | Approved | Implemented
   **Issue**: <link, if any>
   **ADRs**: <links>

   ## The need
   ## Who uses it
   ## Rules
   ## Where it appears
   ## Acceptance examples
   ## Out of scope
   ## Upstream models and views it relies on
   ```

2. **`docs/specs/dswd_household_children.md`**: the demo module's specification, status Approved, written from the
   approved design: the 4Ps need (grants tied to children aged 0 to 18), who uses it (municipal links reading a
   household), the rules (current members only, `is_ended` false; age from `birthdate`, 0 to 18 inclusive; no
   birthdate, not counted), where it appears (the household Profile page), the acceptance examples (members aged 5, 12,
   17 with an ended membership, and 30 give 2; members aged 18 and 19 give 1; a member with no birthdate is not
   counted), out of scope (searching or grouping by the count; storing it), and the upstream names to verify
   (`res.partner`, `group_membership_ids`, `spp.group.membership`, `birthdate`, `spp_registry.view_individuals_form`).
   It names no field or file to write: choosing them is the plan's job.
3. **`docs/architecture/decisions/ADR-002-computed-counts-not-stored.md`**, status Accepted: counts that depend on age
   are computed when read, not stored. Context: a child turns 19 with no write to the database, so a stored count goes
   stale on each birthday until something else touches the household. Options: stored with a nightly recompute job;
   stored with `depends` (stale); not stored. Decision: not stored. Consequences: always current; cannot be searched,
   grouped or used in a domain without a `search` method; costs one read of the memberships per household shown. Row in
   the ADR index.
4. **Pointers**: `docs/README.md` (the tree and a "Write a specification" quick link), `CLAUDE.md` "Where Things Are"
   (a `docs/specs/` row, so Claude Code knows to read it), `docs/guides/claude-code-for-developers.md` "Recommended
   Workflow" (the flow of section 3).

**What stays out of the repository**: the reference build (outside, as now), and the rehearsal's research and plan
files (they live in Edwin's own repository, made by the rehearsal).

**Not a Module 6 answer**: the demo module extends `res.partner` with a computed field; Module 6's exercises are a new
model, a unique field on an extension and vocabulary codes. No overlap (checked against the three sheets).

## 6. Guide section 5.14 "From a specification to a module"

About one and a half pages, after 5.13:

- Why files, not prompts: Claude Code reads them, the team reviews them in a pull request, and they outlast the session.
- The table of section 2 (what goes where).
- The flow of section 3, with the four prompts as code blocks.
- The table of section 4 (what a specification states, by kind of work).
- **Try it after the training**: in your own repository, on a branch, from `docs/specs/dswd_household_children.md` and
  ADR-002, run the flow. Compare your plan with the one shown in the session.
- 5.1 gets objective 7: "Give Claude Code a specification and the project's decisions as files, and take a module from
  them through research, a plan, a test and the code (5.14)."

## 7. The hour, re-timed

Edwin's answer: the hour may run over. Demo B grows from 15 to about 23 minutes; nothing else is cut.

| Time  | Min | Part                                     | Change                                                                 |
| ----- | --- | ---------------------------------------- | ---------------------------------------------------------------------- |
| 3:55  | 5   | What it is                               | None                                                                   |
| 4:00  | 8   | What it reads                            | Add `docs/specs/` and the ADRs to the files shown                      |
| 4:08  | 12  | Demo A: reading code                     | None                                                                   |
| 4:20  | 23  | **Demo B: from a specification to a module** | The flow (2), spec and ADR-002 (2), research (4), plan with one note (4), test first (11) |
| 4:43  | 10  | Safe use and review                      | One checklist point added (the acceptance examples)                    |
| 4:53  | 8   | Demo C: commit, pull request, CI         | The PR body links the spec and ADR-002                                  |
| 5:01  | 2   | Questions                                |                                                                        |
| 5:03  | 5   | Closing                                  | Ends 5:08                                                              |

**Live or prepared**: the research and the plan are generated live; the rehearsal's two files are open in background
tabs and replace the live ones if generation takes over three minutes. The note Edwin adds to the plan live: "Add a
test for a member with no birthdate" (it is in the specification's examples; a plan that missed it shows why you read
the plan). Demo B uses a plain prompt, not `/implement`: `/implement` runs its agents and an expert review, too slow
to show live. The slide says when to use it.

## 8. Materials to change

| Item                                  | Where                                          | Change                                                                       |
| ------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------- |
| New files (section 5)                 | `docs/specs/`, `docs/architecture/decisions/`  | Two specs files, ADR-002, index row                                           |
| Pointers                              | `docs/README.md`, `CLAUDE.md`, `docs/guides/claude-code-for-developers.md` | Section 5, item 4                                  |
| Guide                                 | `training/participant-guide.md`, PDF           | 5.14, objective 7, 5.13's checklist point; PDF rebuilt                         |
| Slides                                | `training/module5/slides.md`                   | Slide 39 becomes three: the flow, what a spec states, Demo B's prompts (footer "Guide 5.14"); 45 slides become 47; run of show re-timed |
| Runbook                               | `training/module5/runbook.md`                  | Block 12 re-timed; Demo B rewritten with the four prompts; "Before the session": the rehearsal's research and plan files open; block 13 at 5:03 |
| Module 5 README and design            | `training/module5/README.md`, `docs/planning/module5-training-design.md` | Times, the guide section                         |
| Lecture notes                         | outside the repository                         | Three slides' notes, renumbered                                               |
| Tests                                 | `tests/test_docs.py`                           | First: the specs template has its sections; the demo spec links an existing ADR; ADR-002 is in the index |

Order: tests first, then the template files, then the guide and the PDF, then the slides, runbook and notes. One pull
request. The decks measured in Chrome as before.

## 9. Decisions

Taken by Edwin on 2026-11-09:

1. **ADR-002 status**: Accepted.
2. **The note added to the plan live**: "Add a test for a member with no birthdate."
3. **The closing at 5:03 to 5:08**: all three points kept.
4. **Demo C's prepared pull request**: it includes the rehearsal's research and plan files, and its body links the
   specification and ADR-002.
