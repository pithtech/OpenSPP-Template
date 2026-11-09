# Plan: Modules 3 to 6 as PowerPoint decks, in sync with the guide

> **Status**: approved by Edwin (2026-11-09, "OK let's proceed"), with the recommended answer to each decision in
> section 5 (recorded there).
> **Edwin's decisions so far**: PowerPoint (`.pptx`, which also imports into Google Slides); the Markdown decks
> (`training/moduleN/slides.md`) stay the source and a build script generates the `.pptx`; the lecture notes go into the
> speaker notes of a **private copy** written outside the repository, and the copy in the repository has no notes.
> **Research**: four expert audits, one per deck, against the guide, the runbook and the lecture notes. They quote the
> lecture notes, so they are kept outside the repository:
> `~/Documents/DSWD-4PS-Training-11-2026/slides-audit/slides-audit-m3.md` to `-m6.md` (every finding, with file and
> line).

---

## 1. What the audits found

| Deck     | Slides now | Proposed | Guide sync                                                                    | Readability                                                                  |
| -------- | ---------- | -------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Module 3 | 27         | 26       | Good: right order, right footers; 18 rows, 5 that matter                       | Code at 14 to 18px on 9 slides (slide 12, the access warning, worst at 14px)  |
| Module 4 | 25         | 24       | 9 real fixes (excerpts that differ from the guide, one footer, order of 6/7)  | Slide 20 at 12.9px; slides 11 and 17 at 17.9px with 16 to 19 code lines      |
| Module 5 | 48         | 43       | 18 rows: slide 42 misses acceptance example 4; slide 39 has 4 steps, guide 5  | Code at 17.4px on all 14 code slides; 5 slides already overflow the frame    |
| Module 6 | 11         | 11       | Slide 2 has no footer; slide 4 has a rule that is in no guide section         | Code fine; slides 4 and 9 and the tables on 3 and 11 are too full            |

Target for every code block: **at least 20px equivalent** (16pt on a 13.33-inch PowerPoint slide), **at most 14
lines**, no line wider than the slide (about 85 characters at 16pt). Every excerpt longer than that is trimmed to the
lines the notes discuss, dedented, or split; the guide keeps the full file.

## 2. Content changes, per deck

All changes are made in `slides.md`, then the runbook's and the lecture notes' slide numbers are renumbered. No
runbook block timing changes. Each merge below was checked against the notes: nothing Edwin says, demos or asks is lost
(the audit files cite the note entry for each).

**Module 3 (27 to 26)**

- Split slide 13 (24 code lines) into the list view, and the action and menus.
- Merge 14 into 15 (the missing tile and its error screenshot), and 17 into 18 (the tile screenshot and "Your turn").
- **Not taken**: merging the title slide into the door slide. The audit proposes it (the title slide's note is "Say:
  nothing"), but in PowerPoint the title slide is the branded cover on screen while the room settles. My
  recommendation: keep it.
- Sync: footer "Guide 0.3" on slide 2; mark the manifest (8) and groups file (16) excerpts "abridged"; the dev-profile
  port note on slide 14's URL; slide 22's report template made to match the guide (`o_main_table`, `<tbody>`); slide 18
  and the runbook agree on the "group by Type" step.
- Readability: rewrap or trim slides 9, 10, 12, 19, 20, 22 and 26; drop the scoped styles that shrink code.

**Module 4 (25 to 24)**

- Split slide 20 (the test, 12.9px) into "Step 4: the test" and "Step 5: run the tests".
- Merge 15 and 16 (the silent failure and its Fields-screen fallback), and 22 and 23 ("CI, review, merge").
- Swap 6 and 7 to follow the guide's order. Slide 21 keeps its number (the runbook's drop rule cites it).
- Sync: slide 19's second error excerpt from the guide (lines 1709 to 1710); slide 10's last line as guide 0.4;
  `help=` back on slide 14 (the guide and the `m4-step-2` tag have it); slide 9's footer to 4.3; slide 2's objective
  wording as the guide; slide 21's "`0 failed, 0 error(s)`"; slide 24's pointer to 4.4.
- Readability: trim slides 11 and 17 to the lines that matter; wrap the long lines on 6, 13, 19 and 25; fit the slide 24
  table.

**Module 5 (48 to 43)**

- Merge the five one-minute primer slides (7 to 11) into one table slide: record rules, jobs, migrations and `noupdate`,
  hooks, wizards, each with its guide section and one line.
- Merge the Claude Code title slide (35) into "What Claude Code is" (36).
- Slide 42: add acceptance example 4 ("no members: 0"). Slide 39: the guide's five steps.
- Sync: the missing guide facts on slides 24 (5.5), 29 (5.7), 30 and 31 (5.8), 42 and 44 (5.13); footers on 31 and 46;
  slide 1 says "about 5:08", as the runbook; slide 44 shows only the `upstream/**` deny rules (`settings.json` also denies
  `vendor/**`, a guard against the old folder name; the slide need not show it).
- Readability: dedent every excerpt (all have 4 to 8 leading spaces); trim slides 13, 16, 18, 19, 22, 28, 29, 30 and 31
  to the lines the notes point at.
- Outside the deck: the notes' slide 42 entry contradicts guide 5.13 on `/implement` (fix the notes); the runbook's stray
  `")` at line 358; `module5-training-design.md` still says 45 slides.

**Module 6 (11, unchanged)**

- Footer "Guide 6.2" on slide 2. Slide 4: footer "Guide 6.2, 6.4, 7.4", and the escalation order ("your pair, your row,
  a helper, then me") added to guide 6.2, so the slide says nothing the guide does not.
- Trim the wording on slides 4 and 9 (no item dropped: the notes read them out) and the table cells on 3 and 11.
- Outside the deck: the notes' stale branch name and "edits pending" lines; `module6-training-design.md` "about 8
  slides".

**Guide changes**: Module 6's escalation sentence in 6.2, and Module 4's "why a vocabulary" moved before the XML in 4.4
(the audit recommends changing the guide here, not the slide). PDF rebuilt.

## 3. The PowerPoint build

**`scripts/slides_pptx/build.py`**, beside `scripts/guide_pdf/`, run as `python3 scripts/slides_pptx/build.py` (all
four decks) or with a module number. It uses `python-pptx` (added as a dev dependency with `uv add --dev python-pptx`, so
the tests run in CI) and parses the Marp Markdown: front matter, `---` slides, `_class: lead`, `_footer`, headings,
paragraphs, bullet and numbered lists, tables, fenced code, images with `h:`, bold, italics and inline code. `<style
scoped>` blocks are ignored: the builder sizes everything itself.

**Look**: the guide PDF's colours (`scripts/guide_pdf/print.css`, from the DSWD and 4Ps logos):

| Element                    | Style                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| Title slide (`lead`)       | Navy `#003761` background, white title, module subtitle in 4Ps yellow `#fdc22d`, a DSWD red `#ec202b` rule as on the PDF cover |
| Section slide (`lead` mid-deck) | DSWD blue `#194998` background, white text                                         |
| Content slide              | White; title in DSWD blue `#194998`, 32pt bold; body `#1f2a37`, 20pt                      |
| Tables                     | Header row DSWD blue with white bold text; zebra rows `#f6f8fb`; lines `#d5dde8`; 16pt     |
| Code                       | Box `#f6f8fb` with a `#d5dde8` border; monospace 16pt (smaller only to 14pt, never below) |
| Inline code                | Monospace in `#0f5fa8`                                                                    |
| Footer                     | "Guide x.y" bottom left and the slide number bottom right, in `#5f6b7a`, 12pt              |

Fonts: Arial for text (on every Windows and Mac machine). For code: see decision 1.

**Fit is checked, not hoped for.** The builder estimates each block's height and width; a slide whose content does not
fit, a code block over 14 lines, or a code line that would need less than 14pt **fails the build** with the slide
number and the reason. The fix is always in `slides.md` (trim or split), never a smaller font. After each build every
slide is rendered to an image (Keynote's PDF export on this Mac) and inspected.

**Outputs**

- `training/moduleN/slides.pptx`, committed beside `slides.md` (as the guide PDF is), with no speaker notes.
- Edwin's copies with notes: `~/Documents/DSWD-4PS-Training-11-2026/slides/moduleN-slides-with-notes.pptx`, built with
  `--notes ~/Documents/DSWD-4PS-Training-11-2026/lecture-notes`. Each `### Slide N: Title` entry becomes slide N's
  notes; the build fails if an entry's title does not match its slide's title, or a slide has no entry, so the notes and
  the deck cannot drift apart.

**Tests first** (`tests/test_slides_pptx.py`): the parser on small Markdown samples (each element kind, footers, `lead`,
images); a built deck has as many slides as `slides.md`, each footer as written, every code run at 14pt or more; the
fit check rejects an over-long code block; the notes mapping rejects a title mismatch; the repository's `.pptx` files
have no notes and are up to date with their `slides.md` (as `tests/test_guide_pdf.py` checks the PDF).

**Docs**: `scripts/README.md`, each module's `README.md` (the `.pptx` is what Edwin presents; `slides.md` is the
source), and the runbooks' "Before the session".

## 4. Order of work

Two pull requests, so the build can be reviewed before the content moves:

1. **The builder**: tests, `scripts/slides_pptx/`, the four decks built as they are now. You open them in PowerPoint
   and judge the look before any content changes.
2. **The content**: the section 2 changes deck by deck (one commit per deck), the runbooks and the lecture notes
   renumbered, the guide edits and the PDF rebuilt, the decks rebuilt and checked slide by slide, then your copies with
   notes.

## 5. Decisions

Edwin approved the plan as written on 2026-11-09, so each decision takes the recommendation:

1. **Code font**: Consolas (PowerPoint on Windows or Mac). Fit is computed at 0.6em per character, the widest common
   monospace, so code also fits where Consolas is replaced (Keynote, Google Slides).
2. **Module 3's title slide**: kept as the branded cover.
3. **Module 5's primer**: one table slide.
4. **Module 4's slide 16** (the Fields-screen screenshot): merged into slide 15, as the audit proposes.
5. **The Marp decks**: `slides.md` stays valid Marp, so the HTML rendering remains a fallback.
