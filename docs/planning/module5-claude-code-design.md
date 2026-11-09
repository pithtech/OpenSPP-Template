# Module 5 Addition: Claude Code in Development (design)

> **Status**: proposal for Edwin's review (2026-11-09). Requested by DSWD on 2026-11-09: a one-hour lecture and demo
> of using Claude Code in development, inside Module 5. Nothing is built until Edwin approves.
> **Edwin's decisions so far**: the hour comes from trimming Module 5's tours; demo only, on the trainer's laptop
> (participants watch); the demo covers reading production code, building with TDD, safe use and review, and commit,
> pull request and CI.

---

## 1. Why it fits Module 5

Module 5 teaches participants to read the production 4Ps modules and to say where a ticket lands. The production
repository is already set up for Claude Code: a root `CLAUDE.md` of 1,768 lines and ten module-level `CLAUDE.md` files
(`dswd_4ps_api`, `dswd_4ps_api_change_request`, `dswd_4ps_api_fds`, `dswd_4ps_api_field_limit`, `dswd_4ps_swdi_api`,
`dswd_4ps_portal_api`, `dswd_4ps_retro_api`, `dswd_4ps_newgrs`, and others). The participants' own repository has the same
kind of setup (`CLAUDE.md`, `.claude/rules/`, five agents, six commands, `settings.json`). So the hour is not about a
new tool in the abstract: it shows how the code they just read is maintained, and how they will maintain it.

The hour comes right after the ticket triage, so its first demo can take a triage ticket the room has just answered by
hand and ask Claude Code the same question.

## 2. Objectives

By 5:00 a participant can:

1. Say what Claude Code reads before it answers (the `CLAUDE.md` files, the rules loaded by path, the agents and
   commands) and where those files are in their repository and in production.
2. Use it to locate and explain code in a large repository, and check its answer against the file before trusting it.
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

Demo only. The trainer's laptop has Claude Code signed in, the production checkout at `ad98dac9`, and a clone of the
trainer's own repository created from the template (as for Module 4 block 8). Live model output differs from run to run:
every demo is rehearsed, and a screen recording of each one is the fallback.

| Time      | Min | Part                                    | What happens                                                                                                                                                                                                                                                                                                                                                                                |
| --------- | --- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3:55      | 5   | What it is, and how 4Ps uses it         | A terminal assistant that reads files, runs commands and edits code, always asking before it acts. The production repository's `CLAUDE.md` and module `CLAUDE.md` files on screen: the team writes down its rules for the assistant.                                                                                                                                                                             |
| 4:00      | 8   | What it reads before it answers         | In the participants' repository: `CLAUDE.md` (project rules, known pitfalls), `.claude/rules/` (loaded when matching files are edited), `.claude/agents/` and `.claude/commands/` (`/implement`, `/verify-tests`, `/commit`, `/pr`), `settings.json` (allowed commands, `upstream/` edits denied, attribution off). Guide 5.13 lists them.                                                                    |
| 4:08      | 12  | Demo A: reading production code         | In the production checkout, the triage ticket the room answered at 3:40 (ticket 7, "a Level 1 assessment was approved but no case was created"): "Which module and file handle this? Explain the event's states." Compare its answer with card 18 and open the file it names. A second question with a deliberate trap (ask for a field that does not exist) to show it must be checked. |
| 4:20      | 15  | Demo B: a change, test first            | In the clone of the trainer's repository: ask for a failing test for a computed `warranty_days_left` on `dswd_asset`, run `./odoo-project test dswd_asset` (red), then ask for the field, run again (green). Read the diff together: is the test meaningful, is anything missing from the manifest or the view, does it follow the rules?                                                   |
| 4:35      | 10  | Safe use and review                     | The review checklist (section 5). Live: ask it to edit a file under `upstream/` and show the `settings.json` deny rule refusing. What never goes into a prompt: beneficiary data, passwords, tokens, production database dumps.                                                                                                                                                                     |
| 4:45      | 8   | Demo C: commit, pull request, CI        | `/commit` on Demo B's change (the hooks run), `/pr` (it writes the PR from the template), then CI on a pull request prepared the evening before (the image build is too slow to wait for). Links back to the workflow of Module 4 block 8 and guide 7.4.                                                                                                                                          |
| 4:53      | 2   | Questions                               |                                                                                                                                                                                                                                                                                                                                                                                                  |

The Demo B change is chosen not to overlap the Module 6 exercises (no unique field, no vocabulary code, no new model)
and not to repeat Module 4 block 8 (the `graduated` level).

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
| Lecture notes for the new slides       | `~/Documents/.../lecture-notes/module5-lecture-notes.md` (outside the repo) | Renumbered                                                                                 |
| Design update                          | `docs/planning/module5-training-design.md`    | Run of show and section 4                                                                   |
| Demo preparation list                  | runbook "Before the session"                  | Claude Code signed in, the two repositories, the prepared pull request, the recordings     |

Before printing, each demo prompt is run on the stack with Claude Code, its output read, and the recording made.

## 7. Risks

| Risk                                                                 | Mitigation                                                                                           |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Live output differs from the rehearsal, or is wrong                  | That is a teaching point (check it against the file); recordings as fallback                         |
| Venue internet slow or down                                          | Recordings of all three demos; the slides carry the prompts and the expected shape of the answer      |
| Sending production code to an external AI service                    | Decision 2 below                                                                                     |
| The project's post-edit lint hook may never run (it is defined in `.claude/hooks.json`, not `settings.json`) | Decision 3 below; the demo does not claim the hook runs until it is verified |
| Time: no buffer left in Module 5                                     | Drop order in section 3                                                                              |

## 8. Decisions for Edwin

1. **The schedule** in section 3, including the extra 5-minute trims to foundation, change requests and compliance,
   the 3 minutes from the triage and the buffer.
2. **Production code and the AI service.** Demo A sends production 4Ps code to Anthropic's API. The production team
   already uses Claude Code on that repository (its `CLAUDE.md` files), but confirm that DSWD's policy allows it in a
   training demo; otherwise Demo A runs on the participants' template repository instead.
3. **The lint hook.** `.claude/hooks.json` may not be loaded by Claude Code; the usual place is `settings.json`
   (`"hooks"`). Verify on the trainer's laptop, and if it does not run, move it before the session (a small change to
   the project's config).
4. **Module 4 block 8** already has a three-minute Claude Code demo. Keep it as a teaser that points to Module 5, or
   shorten it further now that Module 5 has the full hour.
