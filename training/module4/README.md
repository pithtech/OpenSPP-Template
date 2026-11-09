# Module 4 Materials: Developing Custom Modules and Extending Odoo Models

Day 2, 10:10 to 12:00, after Module 3 and a ten-minute break. The design behind these materials is in
[docs/planning/module4-training-design.md](../../docs/planning/module4-training-design.md); the module itself is
[`dswd_wellbeing`](../../dswd_wellbeing/) at the repo root, built in six tagged steps (`m4-step-0` to `m4-step-5`). The
tags exist only in a clone of the template repository (yours); a participant's repository is a template copy with one
commit, no history and no tags, and already holds the finished module.

| File                                             | For                | Use                                                                                                                                                                                                                           |
| ------------------------------------------------ | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [runbook.md](runbook.md)                         | Trainer            | Run of show with commands, the four planted faults and their real log lines, cut-offs, fallbacks                                                                                                                              |
| [slides.pptx](slides.pptx)                       | Trainer, projected | The deck to present: PowerPoint, built from `slides.md` with `uv run python scripts/slides_pptx/build.py`; edit `slides.md` and rebuild, never the `.pptx`                                                                    |
| [slides.md](slides.md)                           | Source of the deck | Marp deck, 24 slides (20 content, 4 screenshots) one per block or step, with the change-to-merge workflow in block 8; render with the VS Code Marp extension or `npx @marp-team/marp-cli slides.md -o slides.pdf`             |
| [handout-anatomy.md](handout-anatomy.md)         | Everyone, printed  | Fill-in file map, the three rules, the loop, the five mistakes, the code of every step                                                                                                                                        |
| [drill.md](drill.md)                             | Pairs, printed     | Three real log excerpts to diagnose in block 9                                                                                                                                                                                |
| [drill-answers.md](drill-answers.md)             | Trainer            | Answer key for the drill                                                                                                                                                                                                      |
| [quiz.md](quiz.md)                               | Participants       | Ten items, an optional self-check; not scheduled in the session                                                                                                                                                               |
| [quiz-answers.md](quiz-answers.md)               | Trainer            | Answer key with the accepted variants                                                                                                                                                                                         |
| [dswd_wellbeing_broken/](dswd_wellbeing_broken/) | Pairs, block 9     | The module with three planted faults; lint passes, Odoo does not. They show one at a time: excerpt B first, then A once the manifest lists the data file; C needs the tests of `dswd_wellbeing`, which the copy does not have |

## Preparing the demo machine (the evening before)

1. On the laptop you present from, start from a fresh database: `git fetch --tags`, then `./odoo-project stop -v -y` and
   `./odoo-project start` (it creates the database and installs the base modules again). Do this before preparing Module
   3, which shares the stack. Log in once so the first demo screen is instant.
2. Never install `dswd_wellbeing` on this stack before the session. Block 1 shows the end state from the screenshots in
   the deck, and the live build installs the module from `m4-step-0` with nothing to uninstall. An uninstall does not
   reset the database: the vocabulary is a system vocabulary, so its codes and xml ids stay behind, and breakages 1 and
   2 would not reproduce. In the break after Module 3 you uninstall `dswd_asset` and switch the tree to `m4-step-0`
   (runbook, "Switch to the live build"); rehearse that switch once. Turn on developer mode so Apps > Update Apps List
   is available.
3. Terminal and editor at 20pt, light theme, at most 25 lines per screen. Hide the dock and notifications.
4. Open these files in editor tabs in order: `__manifest__.py`, `data/vocabulary_well_being_level.xml`,
   `models/res_partner.py`, `views/res_partner_views.xml`, `tests/test_wellbeing.py`, and the upstream
   `upstream/openspp/spp_registry/views/individual_views.xml` at the `group_tags_section` line.
5. Run `./odoo-project test dswd_wellbeing` once so the image and the test database are warm (about 20 s after that).
6. Print the handout and the drill for every participant, the answer keys for yourself.
7. For block 8: clone a repository of your own created from the template (never push from the template clone: its
   `origin` is the template), run `./odoo-project vendor` and `./odoo-project test dswd_wellbeing` in it once. Write the
   `graduated` level by hand (one record in the data file, one test) and keep it in a scratch file, so on stage it is a
   paste; rehearse it once in the clone, then restore the two files. Open a small pull request for the same change on a
   rehearsal branch and let its CI finish green, so the demo shows CI, a review and a merge without waiting for the
   image build. Leave the clone on an up-to-date `main`. Claude Code is not used in Module 4; it is in Module 5.
8. Render the deck once (`npx @marp-team/marp-cli training/module4/slides.md -o slides.pdf`) and keep the PDF on the
   laptop as the projector fallback.

## Why the session is demo-led

About 87 participants, one trainer, mixed skills and a share of laptops that will not run Docker. Nothing in Module 4
requires a participant laptop: participants read, predict and diagnose. Keyboard time is Module 6 on Day 3.

## Participants without a working environment

They follow the **Read** track: the handout has every file and the drill needs only paper. Send them to the lunch triage
table on Day 2 so they are ready for Day 3, where every exercise needs a working stack (or a pair with one).
