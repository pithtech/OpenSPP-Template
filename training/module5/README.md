# Module 5 Materials: DSWD-specific implementation of OpenSPP

Day 2, 1:00 to 5:00. The design behind these materials is in
[docs/planning/module5-training-design.md](../../docs/planning/module5-training-design.md). The session is a
code-reading discussion of the production DSWD 4Ps modules (`dswd-4ps-dp-openspp-v2-module`), organised by the 4Ps
business process and read through the parts of a module taught in Modules 3 and 4. There is no user-interface
demonstration and nothing runs on participant laptops. Every fact, path and excerpt is checked at production commit
`ad98dac9` (2026-11-06).

The last hour, 3:55 to 4:55, is **Claude Code in development**: a demo on the trainer's laptop, in Edwin's own
repository created from the template (never the template repository, and no production code), of reading code, a
test-first change, review and safe use, and commit to pull request. Its design is in
[docs/planning/module5-claude-code-design.md](../../docs/planning/module5-claude-code-design.md); guide section 5.13 is
the participants' text.

| File                                     | For                | Use                                                                                     |
| ---------------------------------------- | ------------------ | --------------------------------------------------------------------------------------- |
| [runbook.md](runbook.md)                 | Trainer            | Run of show, what to say per card, the code moments in tab order, drop order, fallbacks |
| [slides.md](slides.md)                   | Trainer, projected | Marp deck, 45 slides (35 to 43: Claude Code); excerpts are copied from the cards        |
| [module-cards.md](module-cards.md)       | Everyone, printed  | 26 module cards in session order, then the index of all 66 modules; A4, bound to keep   |
| [module-map.md](module-map.md)           | Wall, A1           | The poster: the process top to bottom, the two instances, the bridge                    |
| [category-cards.md](category-cards.md)   | Pairs, printed     | Eight lettered cards (M, V, D, S, W, J, A, T) for "where would you look?"               |
| [triage-sheet.md](triage-sheet.md)       | Pairs, printed     | Eight fabricated training tickets for the 3:40 triage                                   |
| [triage-answers.md](triage-answers.md)   | Trainer            | Answer key with the reasoning and every file a full fix touches                         |
| [checkpoint-bank.md](checkpoint-bank.md) | Trainer            | One standing checkpoint (set 1) with spares; set 2 is kept as spares                    |

## Preparing (the week before and the evening before)

1. The week before: `git -C <production checkout> log -1 --format=%h` should still be `ad98dac9`. If production has
   moved and you want the newer code on screen, re-check every card's paths, line numbers and counts first; the card
   numbers were counted with the method at the top of the catalogue.
2. The evening before: check out `ad98dac9` in the production checkout and open the files in the runbook's tab list.
3. Render the deck once (`npx @marp-team/marp-cli training/module5/slides.md -o slides.pdf`) and keep the PDF as the
   projector fallback.
4. Print the catalogue on A4, one card per sheet (front and back), bound as a booklet. Render it to PDF once with a
   single tool (for example VS Code's Markdown PDF extension or pandoc) and check that the wide strip tables are not
   clipped; use landscape if they are. Test-print card 8, the longest, before ordering about 87 copies, and leave the
   print shop enough time. If time or budget is short, print one catalogue per pair (pairs work together all afternoon)
   and share the PDF.
5. Print the rest: the poster at A1, a set of category cards and a triage sheet per pair, and the answer key and
   checkpoint bank for yourself.
6. The Claude Code hour, the day before: in Edwin's repository, rehearse each demo prompt, make the screen recordings of
   demos A, B and C, and open the pull request whose CI the hour shows; the full list is in the runbook's "Before the
   session".

## Why the session reads code instead of demonstrating screens

Participants are the developers and technicians who will maintain these modules, and they already have access to the
production repository. Reading the real files through the twelve parts of a module they learned in the morning is the
skill they need on a ticket; a running copy of production on the trainer's laptop would add risk and no learning.
