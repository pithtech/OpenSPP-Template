# Module 4 Runbook: Developing Custom Modules and Extending Odoo Models

Day 2, 10:10 to 12:00, after the ten-minute break that follows Module 3. Trainer copy. Objectives, strategy and
rationale are in [docs/planning/module4-training-design.md](../../docs/planning/module4-training-design.md); this page
is only what to do and say, with the commands and the real error lines.

**Cut-offs are hard, and there is no buffer.** Drop order if late: the live commit and push in block 8 (show slide 21's
table and go straight to the prepared pull request, 5 minutes), then breakage 4 in block 6. Blocks 9 and 10 are never
dropped. Block numbers follow the design; there is no block 5.

## Before the session

- Demo laptop: the same stack as Module 3, on a database created fresh the evening before, where `dswd_wellbeing` has
  never been installed (see [README.md](README.md)). Block 1 shows the end state from the screenshots in the deck; the
  live build starts from `m4-step-0` with nothing to uninstall. Terminal and editor at 20pt, light theme, the six files
  ready to open in tabs.
- The test database is warm: `./odoo-project test dswd_wellbeing` has run once today (about 20 s per run after).
- Handouts and drill sheets printed; answer keys with you.
- Two volunteer helpers recruited during Module 3 (anyone whose `./odoo-project doctor` is all green).
- Pre-flight on the demo laptop, same as the participants' Day 3 list: `doctor` clean, `start`, log in, page styled
  (otherwise `./odoo-project resetassets`), `test dswd_wellbeing` 5 passed.

## Switch to the live build (in the break, before 10:10)

Slide 1 (title) is up while the room comes back.

The `m4-step-N` tags do not contain `dswd_asset`, so take it out of the database before its folder disappears, and drop
the tablet edit from Module 3's block 9 so git can switch:

```bash
# In Apps: remove the Apps filter, search "Asset", Uninstall the IT Asset Register.
git checkout -- dswd_asset     # discard the live tablet edit
git checkout m4-step-0
./odoo-project update          # nothing to update; shows the loop command once
```

There is nothing else to uninstall: this database has never had `dswd_wellbeing`. (Uninstalling it would not reset the
demo anyway: the vocabulary is a system vocabulary, so its codes and xml ids stay behind and breakages 1 and 2 would not
reproduce.) Developer mode is on (Settings > Activate the developer mode) so Apps > Update Apps List is available.

## Block 1, 10:10 to 10:15: the end state (screenshots)

Slides 2 to 5.

1. Slide 2, the objectives, in one breath (block 10 comes back to it). Slide 3, the requirement; slide 4, "What you will
   see at noon": a household's Profile page with the "4Ps" section and the Well-Being Level dropdown open. Do not show
   it live: the demo database must not have the module before the live build.
2. Say: "Survival, Subsistence, Self-Sufficient: the SWDI levels. Since EO 120 the level decides whether a household
   stays in the program past seven years. By noon you will know every file it took to put that dropdown there, and how
   to find out why it is missing when it is."
3. Slide 5: where this lives in production (`dswd_4ps_registry`, 27 vocabularies, same pattern). The household's level
   is copied from the latest SWDI assessment (guide 4.12, 5.8).

## Block 2, 10:15 to 10:20: module anatomy (paper)

Slides 6 and 7.

1. Slide 6: the file tree, worded as in guide 4.3 (the answer key for handout section 2). "You filled this map for
   `dswd_asset` at 8:50. What is new: a `data/` file, no menu, and an access file with only its header." Section 2 of
   the handout is filled in as the steps go by; do not wait for it.
2. Slide 7: the three rules, read aloud: never edit `upstream/`; inherit, do not redefine; a file not in the manifest
   does not exist.

## Block 3, 10:20 to 10:40: steps 0 and 1, manifest and data (demo, predict)

Slides 8 to 13.

1. Slides 8 and 9. Show `__manifest__.py` and `__init__.py`. "This is an installable module. It does nothing." Apps >
   Update Apps List > remove the **Apps** filter (the module is not an application) > search "Well" > Install.
   `./odoo-project logs` and point at `Loading module dswd_wellbeing` (an install from Apps runs in the server, so
   `logs` shows it). Slide 10, the loop: point at the install row, then the update row; the `noupdate` row comes back
   after breakage 2.
2. Slide 11. `git checkout m4-step-1`, then, before running anything, **plant both breakages**: delete the data line
   from the manifest, and change `social_assistance` to `administrative` in the data file. The order matters: the file
   is `noupdate="1"`, so a bad value is only caught the first time the file loads.
3. Show the data file: one vocabulary, three codes. Ask: "After update, where will I see them?" Run
   `./odoo-project update`. Settings > Vocabularies: nothing. **Breakage 1.** Ask for the cause. Show the manifest. Add
   the line. Do not update yet.
4. **Breakage 2.** Ask: "Will this fail in lint, on update, or never?" `./odoo-project lint` passes.
   `./odoo-project update` fails. Read the lines in the `update` output together, bottom up:
   ```
   ValueError: Wrong value for spp.vocabulary.domain: 'administrative'
   odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/data/vocabulary_well_being_level.xml:10
   ```
   Open `upstream/openspp/spp_vocabulary/models/vocabulary.py` at the `domain` selection. Fix. `update`. Show the
   vocabulary and its three System codes. Say: "A failed update rolls back; a `noupdate` record that did load is never
   reloaded. Fix values before the first load. After that, only a fresh database or a migration changes it: shipped
   codes of a system vocabulary cannot be deleted." Slide 12 is the fallback for the live screen.
5. Say what `get_code("urn:dswd:4ps:well-being-level", "survival")` means; it is what the tests use.
6. Slide 13. Ask: "Why not a Selection with three values?" (32 client statuses, 394 IP groups, deployment profiles, no
   release to change a code.)

## Block 4, 10:40 to 10:55: step 2, the model (demo, predict)

Slides 14 to 16.

1. `git checkout m4-step-2`, but first **delete the import line in `models/__init__.py`** (breakage 3).
2. Slide 14. Show `models/res_partner.py`: `_inherit`, the `dswd_` prefix, `Many2one` to `spp.vocabulary.code`, the
   namespace domain. Ask: "After update, what changes on screen?"
3. Slide 15. `./odoo-project update`. No error. Settings > Technical > Fields, search `dswd_`: nothing. **Breakage 3.**
   Ask. Show `models/__init__.py`. Restore the import. `update`. The field is listed. "No view yet: a field without a
   view is invisible, not broken." Slide 16 is the fallback for the Fields screen.

## Block 6, 10:55 to 11:10: step 3, the view (demo, predict)

Slides 17 to 19.

1. Slide 17. Open the upstream form first: `upstream/openspp/spp_registry/views/individual_views.xml`, search
   `group_tags_section`. "One form serves individuals and households; household sections are `group_*`."
2. `git checkout m4-step-3`. Show the view file: `inherit_id`, one XPath on a named anchor, a "4Ps" group, `no_create`,
   `no_open`. (The finished module also sets `readonly="disabled"`, so the field locks with the rest of a disabled
   household's Profile page; the tag does not have it.) Ask: "Where will it appear?" Do not update yet.
3. **Breakage 4** (drop if late: then just `update` and open a household): change `group_tags_section` to
   `group_tag_section` before the first update. `update`. Read, in the `update` output:

   ```
   Element '<xpath expr="//group[@name=&#39;group_tag_section&#39;]">' cannot be located in parent view

   View error context:
   {'file': '/mnt/extra-addons/custom/dswd_wellbeing/views/res_partner_views.xml',
    ...
    'xmlid': 'view_res_partner_form_wellbeing'}
   ```

   "`&#39;` is a quote: Odoo escapes the attribute values." Fix. `update`. Registry > Browse All (Audit) > All Groups,
   open a household: set a level. Save (slide 18 is the fallback). Developer menu > View Form: show the inherited view
   listed.

4. Slide 19: the two errors of the morning, read bottom up, as a recap. If breakage 4 was dropped, this is where the
   room sees its lines.

## Block 7, 11:10 to 11:25: steps 4 and 5, the tests (demo, predict)

Slide 20.

1. `git checkout m4-step-5`. Open `tests/test_wellbeing.py`. Walk one test: `RegistryCommon` gives a household and the
   vocabulary model; `get_code`; `assertEqual`. "The test says what we want before the code exists."
2. Run `./odoo-project test dswd_wellbeing`. While it runs (about 20 s), show `security/ir.model.access.csv`: header
   only, "no new model, no rows", and `readme/DESCRIPTION.md`.
3. Read the output: `0 failed, 0 error(s) of 5 tests`, `Passed: 5 | Failed: 0 | Errors: 0` and the `Full log:` line.
   "This line is the one you read first when a colleague says the module is broken."
4. If time: flip `"Subsistence"` to `"Survival"` in `test_household_stores_a_level`, run again, read the
   `AssertionError` and the file:line. Restore.

## Block 8, 11:25 to 11:35: from a change to a merge (demo only)

Slides 21 to 23. The change is made by hand; Claude Code is in Module 5 this afternoon.

Prepare the evening before, in a repository of your own created from the template (never the template itself):

- Clone it next to the template clone, run `./odoo-project vendor` and `./odoo-project test dswd_wellbeing` in it once,
  and open it in a second VS Code window. The template clone's `origin` is the template repository, so nothing in this
  block is pushed from it; check `git remote -v` in the clone you push from.
- Write the edit and keep it in a scratch file outside the clone: in `data/vocabulary_well_being_level.xml`, a fourth
  record `code_well_being_graduated` (a copy of the `self_sufficient` record with code `graduated`, display `Graduated`,
  sequence 40), and in `tests/test_wellbeing.py` a test that `self.VocabCode.get_code(NAMESPACE, "graduated")` resolves
  with display `Graduated`. Rehearse it in the clone once (6 tests, all green), then `git restore` the two files. On
  stage the change is one pasted record and one pasted test.
- Open a pull request for the same change on another branch (for example `feat/graduated-rehearsal`) and let its CI
  finish green, so the room does not wait for the image build.
- Leave the clone on an up-to-date `main` (`git switch main`, `git pull`), so the live change starts at 7.4 step 1.

Drop rule: if block 7 ran over, skip item 2's live commit and push. Show slide 21's table, say which row is which, and
go straight to item 3 on the prepared pull request (5 minutes).

1. **The change, by hand** (3 min), slide 21: in the clone, on its up-to-date `main`, `git switch -c feat/graduated`.
   Paste the test into `tests/test_wellbeing.py` and the `graduated` record into the data file. Show the diff
   (`git diff`): the record sits under the well-being vocabulary, the data file is still in the manifest, and the test
   asserts something that could fail. Run `./odoo-project test dswd_wellbeing` in that clone (about 20 s):
   `0 failed, 0 error(s) of 6 tests`.
2. **The path to `main`** (4 min), slide 21: `git add` the two files by name, `git status`,
   `git commit -m "feat(wellbeing): add the graduated level"` (the hooks run on screen; if one reformats a file,
   `git add` it again and commit again), `git push -u origin feat/graduated`. Open the link it prints: the pull request,
   the template headings. Say: "CI starts now; its first run builds the image, so we look at the one I opened
   yesterday."
3. **CI, review, merge** (3 min), slides 22 and 23, on the prepared pull request: the **Checks** tab (pre-commit, build,
   the module's test job), a failed run's **Details** if you have one, then **Files changed**: leave one review comment,
   approve, **Merge pull request**, **Delete branch**. Back in the clone: `git switch main`, `git pull`,
   `git branch -d <the prepared branch>`, and `update` if the merge changed a module on your stack (guide 7.4, step 15).
   "Tomorrow you do steps 1 to 11 yourselves; the review is not required in the exercise."
4. Close the live branch's pull request without merging (the prepared one already carries the change), or keep it as an
   example.

## Block 9, 11:35 to 11:50: troubleshooting drill (pairs, paper)

Slide 24.

1. Slide 24: the five mistakes, four of which the room watched this morning. Hand out [drill.md](drill.md). 12 minutes,
   three excerpts, pairs.
2. Walk the room; note which pairs reach C (the silent one) and start the debrief with one of them.
3. Debrief with [drill-answers.md](drill-answers.md): C first, then A, then B. One pair reports each. Bonus D if a pair
   reached it.

## Block 10, 11:50 to 12:00: recap and handoff

Slide 25 (and slide 2).

1. Go back to slide 2, the objectives: read the five, ask for a thumbs up on each.
2. What moves to Module 5: the production modules read through this morning's parts: the module map, the registry and
   its hierarchical vocabularies, roles and approvals, change requests, compliance, payroll, casework, APIs; and, at the
   end of the afternoon, Claude Code in development.
3. Point to Module 6: "Tomorrow you build three modules of your own, starting from `dswd_asset` and `dswd_wellbeing`.
   Before 8:30: `./odoo-project start` and `./odoo-project test dswd_wellbeing` (`0 failed, 0 error(s) of 5 tests`). If
   your laptop does not run Docker, sit with a pair that has a working one."
4. Back to slide 25. Point to the lunch triage table.

## If the demo machine fails

- Any step: `git checkout m4-step-N` restores a known-good tree; `./odoo-project update` or `install` restores the
  database state.
- Docker gone: switch to the recording for the current block and continue with the handout code on screen.
- Projector gone: the handout has every file; run the session from paper and the drill.

## Commands used in this session

```bash
./odoo-project start --profile dev     # dynamic port when 8069 is busy
./odoo-project install dswd_wellbeing  # first install (update cannot install)
./odoo-project update                  # after manifest, data, security, new field or view changes; prints ParseError
./odoo-project logs                    # the running server: Loading module ... after an install from Apps
./odoo-project test dswd_wellbeing     # fresh database, 5 tests, about 20 s
./odoo-project lint                    # passes on all four breakages; that is the point
git checkout m4-step-N                 # N from 0 to 5
```
