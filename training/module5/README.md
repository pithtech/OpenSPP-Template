# Module 5 Materials: DSWD-specific implementation of OpenSPP

Day 2, 1:00 to 5:00. The design behind these materials is in
[docs/planning/module5-training-design.md](../../docs/planning/module5-training-design.md). The session is a
code-reading discussion of the production DSWD 4Ps modules (`dswd-4ps-dp-openspp-v2-module`), organised by the 4Ps
business process and read through the parts of a module taught in Modules 3 and 4. There is no user-interface
demonstration and nothing runs on participant laptops. Every fact, path and excerpt is checked at production commit
`ad98dac9` (2026-11-06).

| File                                     | For                | Use                                                                                     |
| ---------------------------------------- | ------------------ | --------------------------------------------------------------------------------------- |
| [runbook.md](runbook.md)                 | Trainer            | Run of show, what to say per card, the code moments in tab order, drop order, fallbacks |
| [slides.md](slides.md)                   | Trainer, projected | Marp deck, 34 slides; excerpts are copied from the cards                                |
| [module-cards.md](module-cards.md)       | Everyone, printed  | 26 module cards (A5) in session order, then the index of all 66 modules; bound to keep  |
| [module-map.md](module-map.md)           | Wall, A1           | The poster: the process top to bottom, the two instances, the bridge                    |
| [category-cards.md](category-cards.md)   | Pairs, printed     | Eight coloured cards (M, V, D, S, W, J, A, T) for "where would you look?"               |
| [triage-sheet.md](triage-sheet.md)       | Pairs, printed     | Eight fabricated training tickets for the 4:32 triage                                   |
| [triage-answers.md](triage-answers.md)   | Trainer            | Answer key with the reasoning and every file a full fix touches                         |
| [checkpoint-bank.md](checkpoint-bank.md) | Trainer            | Two standing checkpoints with spares                                                    |

## Preparing (the week before and the evening before)

1. The week before: `git -C <production checkout> log -1 --format=%h` should still be `ad98dac9`. If production has
   moved and you want the newer code on screen, re-check every card's paths, line numbers and counts first; the card
   numbers were counted with the method at the top of the catalogue.
2. The evening before: check out `ad98dac9` in the production checkout and open the files in the runbook's tab list.
3. Render the deck once (`npx @marp-team/marp-cli training/module5/slides.md -o slides.pdf`) and keep the PDF as the
   projector fallback.
4. Print: the catalogue for everyone, the poster at A1, a set of category cards and a triage sheet per pair, and the
   answer key and checkpoint bank for yourself.

## Why the session reads code instead of demonstrating screens

Participants are the developers and technicians who will maintain these modules, and they already have access to the
production repository. Reading the real files through the twelve parts of a module they learned in the morning is the
skill they need on a ticket; a running copy of production on the trainer's laptop would add risk and no learning.
