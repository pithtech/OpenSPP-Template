# Module 5 Addition: Claude Code in Development (design)

> **Status**: proposal for Edwin's review (2026-11-09), revised with Edwin's answers to the four decisions (section 8).
> Requested by DSWD on 2026-11-09: a one-hour lecture and demo of using Claude Code in development, inside Module 5.
> **Edwin's decisions**: the hour comes from trimming Module 5's tours (the schedule in section 3, accepted); demo only,
> on the trainer's laptop; **no production code** in the demos: Claude Code works on a small DSWD 4Ps module in Edwin's
> own repository, created from the template before Day 1 (the template repository is not touched); all Claude Code
> material moves to Module 5 (Module 4 keeps the change-to-merge workflow only); the project's lint hook is fixed now.

---

## 1. Why it fits Module 5

Module 5 teaches participants to read OpenSPP and 4Ps code and to say where a ticket lands. Claude Code does the same
kind of work on request: it reads the repository, explains code, finds where a change belongs, writes the change and its
test, and runs the commands. The participants' repository is already set up for it (`CLAUDE.md`, `.claude/rules/`,
five agents, six commands, `settings.json`), so the hour shows them how to use what they already have. The trainer can
say that the production 4Ps team works the same way, but no production code is shown or sent to the service.

The hour comes right after the ticket triage: the room has just practised finding where a change belongs by hand, and
the first demo asks Claude Code the same kind of question.

## 2. Objectives

By 5:00 a participant can:

1. Say what Claude Code reads before it answers (the `CLAUDE.md` file, the rules loaded by path, the agents and
   commands) and where those files are in their repository.
2. Use it to locate and explain code in a large code base (their modules and OpenSPP's in `upstream/openspp/`), and
   check its answer against the file before trusting it.
3. Describe the test-first loop with Claude Code: a failing test, the change, the module's tests, a reviewed diff.
4. Review what it writes: the checks to make, what never goes into a prompt, and what the repository forbids it to do.
5. Take a change from Claude Code to a merged pull request with the repository's `/commit` and `/pr` commands and CI.

## 3. Run of show: Module 5 with the hour

Edwin's decision: the hour comes from the tours. The triage moves before the hour so the first demo can reuse it.

| Time      | Block                                            | Was            | Now    |
| --------- | ------------------------------------------------ | -------------- | ------ |
| 1:00      | Opener                                           | 5              | 5      |
| 1:05      | The map                                          | 10             | 8      |
| 1:13      | Primer: rules, jobs, migrations, hooks, wizards  | 10             | 5      |
| 1:18      | Foundation (cards 2 to 7)                        | 40             | 35     |
| 1:53      | Checkpoint 1                                     | 5              | 5      |
| 1:58      | Change requests (cards 8 to 10)                  | 40             | 35     |
| 2:33      | Break                                            | 15             | 15     |
| 2:48      | Compliance and FDS (cards 11, 12)                | 30             | 25     |
| 3:13      | Payroll family (cards 13 to 15)                  | 20             | 10     |
| 3:23      | Casework and the bridge (cards 16 to 19)         | 20             | 12     |
| 3:35      | Integration (cards 20 to 26)                     | 12             | 5      |
| (dropped) | Checkpoint 2                                     | 5              | 0      |
| 3:40      | Ticket triage                                    | 18             | 15     |
| 3:55      | **Claude Code in development**                   |                | **60** |
| 4:55      | Closing                                          | 7              | 5      |
| (dropped) | Buffer                                           | 3              | 0      |

Total 300 minutes, 1:00 to 5:00. **What the trims cost**: the primer becomes one slide per concept read aloud; payroll
keeps the point of no return and the sealed snapshot only; casework keeps SWDI levels and the trigger-to-case job;
integration becomes one slide (the API's rules, then "the rest is on cards 21 to 26"); checkpoint 2 goes (its payroll
item moves into the payroll tour as a question). Every cut topic stays on its card and in guide chapter 5. There is no
buffer left: the drop order for running late is the casework block to 6 minutes, then integration to the poster only.

**Note**: Edwin's option described the tours trimmed and the hour at 3:55 to 4:55. Reaching 3:55 also needed 5 minutes
each from foundation, change requests and compliance, 3 from the triage, and the buffer. Flag any of these you want
kept; the hour can then start later and the closing shrinks.

## 4. The hour, 3:55 to 4:55

Demo only, in **Edwin's own repository** created from the template before Day 1, never the template repository. The
trainer's laptop has Claude Code signed in, that repository cloned on an up-to-date `main` with the OpenSPP source in
`upstream/openspp/` and the stack running. **No production code** is opened, shown or sent. Live model output differs
from run to run: every demo is rehearsed, and a screen recording of each one is the fallback.

**The demo subject**: a small DSWD 4Ps module, `dswd_household_children`, that adds to each household the number of
children aged 0 to 18 among its current members (4Ps grants are tied to children in that range). It is chosen because it
reads OpenSPP's real household structure (households, memberships, birthdates), it is a computed field and an inherited
view (Module 3 and 4 skills), and it overlaps none of the Module 6 exercises (no new table, no unique field, no
vocabulary code) or the Module 4 demo. Verified upstream: `res.partner.birthdate` and the computed `age`
(`spp_registry/models/individual.py`), the household's `group_membership_ids` and `spp.group.membership.is_ended`
(`spp_registry/models/group_membership.py`).

| Time      | Min | Part                                    | What happens                                                                                                                                                                                                                                                                                                                                                                                |
| --------- | --- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3:55      | 5   | What it is                              | A terminal assistant that reads files, runs commands and edits code, asking before it acts. What it is good at (reading a large code base, the repetitive parts of a change, running the loop) and what stays with the developer (deciding, reviewing, testing, owning the change).                                                                                                             |
| 4:00      | 8   | What it reads before it answers         | In the repository: `CLAUDE.md` (project rules, known pitfalls), `.claude/rules/` (loaded when matching files are edited), `.claude/agents/` and `.claude/commands/` (`/implement`, `/verify-tests`, `/commit`, `/pr`), `settings.json` (allowed commands, the lint hook after every edit, `upstream/` edits denied, attribution off). Guide 5.13 lists them.                                       |
| 4:08      | 12  | Demo A: reading code                    | "Where does OpenSPP keep a household's members, and how do I get each member's age?" It should name `spp.group.membership`, `group_membership_ids`, `is_ended` and `age`: open `upstream/openspp/spp_registry/models/group_membership.py` and `individual.py` and check. Then a trap: ask about a field that does not exist, and show why every claim is checked against the file. |
| 4:20      | 15  | Demo B: a change, test first            | Ask for the module `dswd_household_children` test first: a failing test (a household with members aged 5, 17 and 30, one of them with an ended membership, expects 2), `./odoo-project test` (red), then the computed field and the household form, `install`, `test` (green). The lint hook runs after each edit. Read the diff together.                                                     |
| 4:35      | 10  | Safe use and review                     | The review checklist (section 5). Live: ask it to edit a file under `upstream/` and show the `settings.json` deny rule refusing. What never goes into a prompt: beneficiary data, passwords, tokens, database dumps, code you may not share.                                                                                                                                                       |
| 4:45      | 8   | Demo C: commit, pull request, CI        | `/commit` on Demo B's module (the pre-commit hooks run), `/pr` (it fills the pull request template), then CI on a pull request prepared the evening before (the image build is too slow to wait for). Links back to the workflow of Module 4 block 8 and guide 7.4.                                                                                                                             |
| 4:53      | 2   | Questions                               |                                                                                                                                                                                                                                                                                                                                                                                                  |

## 5. The review checklist (slide, guide 5.13, lecture notes)

1. Does the test fail without the change and pass with it? Does it test the behaviour, not the implementation?
2. Is every new file in the manifest? Is every new field in a view, if users need it?
3. Is anything changed under `upstream/openspp/`? (It should be blocked; check anyway.)
4. Do names follow guide 7.1 (`dswd_` prefix, model and XML id patterns)?
5. Does it claim something about the code you have not seen in a file? Open the file.
6. Did it run the module's tests, and did you read the summary line yourself?
7. Nothing secret or personal in the prompt or the diff: no beneficiary data, passwords, tokens or keys.
8. Commit messages and pull requests carry no AI attribution in this project (`settings.json` turns it off; `/commit`
   and `/pr` repeat it).

## 6. Materials to build

| Item                                   | Where                                         | Notes                                                                                      |
| -------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| About 9 slides, guide footers          | `training/module5/slides.md`                  | After the triage slides; re-timed run-of-show slides; one integration slide                |
| Runbook: new block, re-timed blocks    | `training/module5/runbook.md`                 | Exact prompts for each demo, what to point at, the fallback recording                       |
| Guide: new section 5.13                | `training/participant-guide.md`               | Presented: what Claude Code reads, the loop, the checklist, safe use; links to `docs/guides/claude-code-for-developers.md`; PDF rebuilt |
| Module 4 without Claude Code           | `training/module4/` slides, runbook, README; guide 4.x if it mentions it | Slide 21 goes; block 8 keeps the change-to-merge workflow with a change the trainer prepares by hand; slide numbers and the Module 4 lecture notes renumbered |
| A reference build of the demo module   | outside the repository, with the Module 6 solutions | Built once with Claude Code during rehearsal; the recording's source and the fallback if the live demo fails |
| Lecture notes for the new slides       | `~/Documents/.../lecture-notes/module5-lecture-notes.md` (outside the repo) | Renumbered                                                                                 |
| Design update                          | `docs/planning/module5-training-design.md`    | Run of show and section 4                                                                   |
| Demo preparation list                  | runbook "Before the session"                  | Claude Code signed in, Edwin's repository, the prepared pull request, the recordings       |

Before printing, each demo prompt is run with Claude Code in a repository created from the template, its output read,
and the recording made.

## 7. Risks

| Risk                                                                 | Mitigation                                                                                           |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Live output differs from the rehearsal, or is wrong                  | That is a teaching point (check it against the file); recordings as fallback                         |
| Venue internet slow or down                                          | Recordings of all three demos; the slides carry the prompts and the expected shape of the answer      |
| Time: no buffer left in Module 5                                     | Drop order in section 3                                                                              |
| The demo module looks like a Module 6 answer                         | It overlaps none of the three exercises (section 4)                                                   |

## 8. Decisions

Taken by Edwin on 2026-11-09:

1. **The schedule** in section 3, accepted as written.
2. **No production code.** The demos run on a small DSWD 4Ps module in Edwin's own repository, created from the
   template before Day 1. The template repository is not touched; after the training Edwin removes the participants as
   collaborators of the template repository.
3. **The lint hook** is fixed now: it moves from `.claude/hooks.json`, which Claude Code does not read, to the `"hooks"`
   key of `.claude/settings.json`, where project hooks are documented (code.claude.com/docs/en/hooks). Separate pull
   request.
4. **All Claude Code material moves to Module 5.** Module 4 block 8 keeps the change-to-merge workflow (branch, commit,
   push, pull request, CI, review, merge) with a change the trainer prepares by hand; its Claude Code slide goes.
