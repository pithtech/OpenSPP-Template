# Module 6 Materials: Hands-on Activity

Day 3, 8:30 to 10:30: 90 minutes in which participants build three modules of their own on their own Docker stack, then
30 minutes in which the trainer discusses the work done. The design is in
[docs/planning/module6-training-design.md](../../docs/planning/module6-training-design.md).

| File                                                       | For                   | Use                                                                         |
| ---------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------- |
| [exercise-1-development.md](exercise-1-development.md)     | Participants, printed | Development: `dswd_fds_session`, a register of FDS sessions (40 min)        |
| [exercise-2-extending.md](exercise-2-extending.md)         | Participants, printed | Extending: `dswd_listahanan`, a unique Listahanan ID on households (30 min) |
| [exercise-3-customization.md](exercise-3-customization.md) | Participants, printed | Customization: `dswd_id_types`, PhilSys as an OpenSPP ID type (20 min)      |
| [runbook.md](runbook.md)                                   | Trainer               | Run of show, checkpoints, the discussion, fallbacks                         |
| [slides.md](slides.md)                                     | Trainer, projected    | Marp deck: door, launch, one slide per exercise, checkpoints, discussion    |

The sheets give a specification, the Day 2 module to copy from (`dswd_asset`, `dswd_wellbeing`), the command after each
step, what the participant should see, and hints for the lines nobody can guess. They never print a complete file.

**The reference solutions and the answer key are not in this repository** and must never be added to it: participants
create their repositories from this template. They are on the trainer's machine, in
`~/Documents/DSWD-4PS-Training-11-2026/module6/` (`solutions/` and `answers.md`).

## Preparing

1. The week before: copy each solution into a scratch checkout of this repository (never commit it) and run
   `./odoo-project test <module>` on each: 2, 3 and 2 tests. Time one `test` and one `install` on a Windows laptop like
   the participants'. If either takes more than about 2 minutes, announce exercise 3 as the take-home at 8:30.
2. The evening before: the demo laptop's stack running, logged in. Keep the three solutions ready to copy into its
   repository root for the discussion; do not commit them.
3. Print the three sheets for every participant (or one set per pair) and the runbook for yourself.
4. Render the deck once (`npx @marp-team/marp-cli training/module6/slides.md -o slides.pdf`) as the projector fallback.
