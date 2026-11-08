# Module 4 Materials: Developing Custom Modules and Extending Odoo Models

Day 2, 10:00 to 12:00. The design behind these materials is in
[docs/planning/module4-training-design.md](../../docs/planning/module4-training-design.md); the module itself is
[`dswd_wellbeing`](../../dswd_wellbeing/) at the repo root, built in six tagged steps (`m4-step-0` to `m4-step-5`).

| File                                             | For                 | Use                                                                                                                                                                 |
| ------------------------------------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [runbook.md](runbook.md)                         | Trainer             | Run of show with commands, the four planted faults and their real log lines, cut-offs, fallbacks                                                                    |
| [slides.md](slides.md)                           | Trainer, projected  | Marp deck, 23 slides (18 content, 5 screenshots) one per block or step; render with the VS Code Marp extension or `npx @marp-team/marp-cli slides.md -o slides.pdf` |
| [handout-anatomy.md](handout-anatomy.md)         | Everyone, printed   | Fill-in file map, the three rules, the loop, the five mistakes, the code of every step                                                                              |
| [drill.md](drill.md)                             | Pairs, printed      | Three real log excerpts to diagnose in block 9                                                                                                                      |
| [drill-answers.md](drill-answers.md)             | Trainer             | Answer key for the drill                                                                                                                                            |
| [quiz.md](quiz.md)                               | Participants        | Ten items; 1 to 5 are the paired pre/post set                                                                                                                       |
| [quiz-answers.md](quiz-answers.md)               | Trainer             | Answer key with the accepted variants                                                                                                                               |
| [exercise-day3.md](exercise-day3.md)             | Participants, Day 3 | Three tiers: find the faults, list column, Philippine ID types                                                                                                      |
| [dswd_wellbeing_broken/](dswd_wellbeing_broken/) | Participants, Day 3 | The module with three planted faults; lint passes, Odoo does not                                                                                                    |

## Preparing the demo machine (the evening before)

1. `git fetch --tags && git checkout m4-step-5 && ./odoo-project start` on the laptop you present from. Log in once so
   the first demo screen is instant. Keep this database: it is the "end state" for block 1.
2. The live build uses the same database: after block 1 you uninstall the module in Apps (Odoo removes the field, the
   view and the codes cleanly), `git checkout m4-step-0`, and install again step by step. Rehearse that switch once; it
   takes under a minute. Turn on developer mode so Apps > Update Apps List is available.
3. Terminal and editor at 20pt, light theme, at most 25 lines per screen. Hide the dock and notifications.
4. Open these files in editor tabs in order: `__manifest__.py`, `data/vocabulary_well_being_level.xml`,
   `models/res_partner.py`, `views/res_partner_views.xml`, `tests/test_wellbeing.py`, and the upstream
   `vendor/openspp/spp_registry/views/individual_views.xml` at the `group_tags_section` line.
5. Run `./odoo-project test dswd_wellbeing` once so the image and the test database are warm (about 20 s after that).
6. Print the handout and the drill for every participant, the two answer keys for yourself.
7. Render the deck once (`npx @marp-team/marp-cli training/module4/slides.md -o slides.pdf`) and keep the PDF on the
   laptop as the projector fallback.

## Why the session is demo-led

About 87 participants, one trainer, mixed skills and a share of laptops that will not run Docker. Nothing in Module 4
requires a participant laptop: participants read, predict and diagnose. Keyboard time is Module 6 on Day 3.

## Participants without a working environment

They follow the **Read** track: the handout has every file, the drill needs only paper, and the Day 3 Tier 1 exercise is
read-only. Send them to the lunch triage table on Day 2 so they are ready for Day 3.
