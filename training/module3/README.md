# Module 3 Materials: Introduction to Odoo

Day 2, 8:30 to 10:00, then a ten-minute break and Module 4 (10:10 to 12:00). The design is in
[docs/planning/module3-training-design.md](../../docs/planning/module3-training-design.md); the demo module is
[`dswd_asset`](../../dswd_asset/) at the repo root, an IT asset register built from scratch in seven tagged steps
(`m3-step-0` to `m3-step-6`, in the trainer's clone of the template; a participant's copy holds the finished module and
no tags).

| File                                     | For                | Use                                                                                                                                                        |
| ---------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [runbook.md](runbook.md)                 | Trainer            | Run of show with commands, the planted fault and its real log line, cut-offs, drop order                                                                   |
| [slides.pptx](slides.pptx)               | Trainer, projected | The deck to present: PowerPoint, built from `slides.md` with `uv run python scripts/slides_pptx/build.py`; edit `slides.md` and rebuild, never the `.pptx` |
| [slides.md](slides.md)                   | Source of the deck | Marp deck, screenshots from a real stack; render with the VS Code Marp extension or `npx @marp-team/marp-cli slides.md -o slides.pdf`                      |
| [handout-anatomy.md](handout-anatomy.md) | Everyone, printed  | Five words, fill-in file map, the loop, field types, the four mistakes, the code per step, the bridge to Module 4 on the back                              |
| [command-card.md](command-card.md)       | Everyone, printed  | The nine commands and the three log lines to recognise                                                                                                     |

No quiz: assessment is Module 6.

## Preparing the demo machine

1. `git fetch --tags && git checkout m3-step-6 && ./odoo-project start`, then `./odoo-project install dswd_asset` once
   so the database knows the module. Before the session, uninstall it in Apps and `git checkout m3-step-0`: the live
   build installs it again step by step. If you also prepare Module 4's fresh database that evening (see the
   [Module 4 README](../module4/README.md)), do that first: `stop -v -y` deletes this database too.
2. Developer mode on. Terminal and editor at 20pt, light theme, at most 25 lines per screen.
3. Editor tabs in order: `__manifest__.py`, `models/dswd_asset.py`, `views/dswd_asset_views.xml`, `views/menus.xml`,
   `security/groups.xml`, `security/ir.model.access.csv`, `report/dswd_asset_report.xml`, `tests/test_dswd_asset.py`.
4. `./odoo-project test dswd_asset` once so the image is warm (about 20 s after that).
5. Print the handout and the command card for every participant.

## The door slide

From 8:15: "Run `./odoo-project start`, log in, turn on developer mode. Then wait." Nothing before 8:50 needs a laptop.
