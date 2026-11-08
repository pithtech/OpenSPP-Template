# Module 6 Runbook: Hands-on Activity

Day 3, 8:30 to 10:30. Trainer copy. Rationale in
[docs/planning/module6-training-design.md](../../docs/planning/module6-training-design.md); the answer key and the
reference solutions are outside the repository, in `~/Documents/DSWD-4PS-Training-11-2026/module6/`.

**The shape.** Three modules, one per skill, each built by the pair on its own stack. 90 minutes of work, then 30
minutes of discussion. The trainer walks the room; the sheets carry the steps.

## Before the session

- Demo laptop: stack running, logged in, developer mode on. The three solutions ready to copy into the repository root
  for the discussion (not committed).
- The sheets printed. The deck open on the door slide from 8:00.
- Helpers (anyone whose stack worked on Day 2) told their rows.

## 8:00 to 8:30: at the door

Door slide: "Open PowerShell in your repository. `.\odoo-project start`, log in, then
`.\odoo-project test dswd_wellbeing` and wait for `0 failed`." The first test of the day is the slowest; it must not
happen inside the exercises. Laptops that cannot start: their owners pair with a working laptop now.

## Block 1, 8:30 to 8:35: launch

1. "Three modules this morning, one per skill: development, extending, customization. Each is a 4Ps request."
2. "Done means three proofs: the install line, the test line with `0 failed`, and the screen. That is what we discuss at
   ten."
3. Rules: pairs at one laptop, one types and one reads; swap at each exercise. Ask your pair, then your row, then a
   helper, then me. "Read every command's output to the end: if it does not say complete, it failed."

## Block 2, 8:35 to 9:15: exercise 1, development (`dswd_fds_session`)

- Walk the room from the back. The first ten minutes are copying, renaming and the manifest; most questions are leftover
  `dswd_asset` names.
- At 8:55, ask: "Who has installed?" Expect few. Whoever is stuck on a `CRITICAL` line: open the full log, search for
  `Error`.
- **Checkpoint 9:15**: hands up for "install complete", then for "0 failed". Pairs not there at 9:25 move to exercise 2
  and finish 1 later.
- Watch for, and note the pair for the discussion: a pair that met the hidden-menu lesson (no access rows), a pair whose
  manifest listed a deleted file.

## Block 3, 9:15 to 9:45: exercise 2, extending (`dswd_listahanan`)

- The hint on the sheet carries the uniqueness test; the usual mistakes are a wrong anchor (copy it exactly) and the
  data file still in the manifest.
- **Checkpoint 9:45**: hands up for "the Listahanan section on a household", then for "a duplicate refused".
- Note a pair that can show the duplicate message on screen.

## Block 4, 9:45 to 10:00: exercise 3, customization (`dswd_id_types`)

- Say at 9:45: "Exercise 3 is the smallest. Finish it here if you can; the sheet is complete for afterwards."
- The usual mistakes: the module's `__init__.py` still importing `models`; a manual PhilSys code added in the UI.
- Note a pair that reached the refusal on the Identity page.

## 10:00 to 10:30: discussion

The pair narrates from its laptop or sheet; you reproduce on the demo laptop (copy the solution in, `install`, show). Do
not switch laptops on the projector.

| Time        | Segment                                                                                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10:00-10:10 | Exercise 1: one pair shows its register. "Which error did you meet first?" The hidden menu without access rows; the manifest listing a deleted file.                                                 |
| 10:10-10:18 | Exercise 2: the section on a household, absent on an individual (why, without an `invisible`); the duplicate message. Why a database constraint and not a Python check.                              |
| 10:18-10:26 | Exercise 3: the refusal on the Identity page. OpenSPP checked the number with no Python from them: customization through data. Production does the same for PhilSys, the 4Ps ID card and PhilHealth. |
| 10:26-10:30 | Close: development, extending, customization. For 4Ps, extending and data are the everyday work; a new model is rare.                                                                                |

## If something fails

- A pair's stack dies mid-exercise: they join the next pair and continue on its laptop.
- Many laptops slow: announce exercise 3 as the take-home; exercises 1 and 2 get 45 minutes each.
- Demo laptop down: the discussion runs from the pairs' laptops at their tables, you walking with a microphone.

## Commands used in this session

```powershell
.\odoo-project start
.\odoo-project test dswd_wellbeing          # at the door
.\odoo-project install <module>             # once per exercise
.\odoo-project test <module>                # after each install
.\odoo-project update                       # after changing an installed module
```
