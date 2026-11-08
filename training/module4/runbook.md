# Module 4 Runbook: Developing Custom Modules and Extending Odoo Models

Day 2, 10:00 to 12:00. Trainer copy. Objectives, strategy and rationale are in
[docs/planning/module4-training-design.md](../../docs/planning/module4-training-design.md); this page is only what to do
and say, with the commands and the real error lines.

**Cut-offs are hard.** Drop order if late: block 8 (Claude Code), then breakage 4 in block 6. Blocks 9 and 10 are never
dropped.

## Before the session

- Demo laptop: one running stack with `dswd_wellbeing` installed from `m4-step-5` (block 1 shows it), terminal and
  editor at 20pt, light theme, the six files open in tabs (see [README.md](README.md)).
- The test database is warm: `./odoo-project test dswd_wellbeing` has run once today (about 20 s per run after).
- Handouts and drill sheets printed; answer keys with you.
- Two volunteer helpers recruited during Module 3 (anyone whose `./odoo-project doctor` is all green).

## Block 1, 10:00 to 10:05: the end state (demo)

1. Registry > Groups > open a household > Profile. Point at the "4Ps" section and set Well-Being Level to Subsistence.
   Save.
2. Say: "Survival, Subsistence, Self-Sufficient: the SWDI levels. Since EO 120 the level decides whether a household
   stays in the program past seven years. By noon you will know every file it took to put that dropdown there, and how
   to find out why it is missing when it is."
3. One slide: where this lives in production (`dswd_4ps_registry`, 26 vocabularies, same pattern).

## Block 2, 10:05 to 10:15: module anatomy (paper)

1. Slide: the file tree. One sentence per file, in the order Odoo reads them.
2. Participants fill in section 2 of the handout while you talk. Ask two people to read their line for `__manifest__.py`
   and `views/`.
3. The three rules, read aloud: never edit `vendor/`; inherit, do not redefine; a file not in the manifest does not
   exist.

## Switch to the live build (during block 2, 1 minute)

```bash
# In Apps: search "Well", Uninstall. Say: "uninstall removes the field, the view and the codes cleanly."
git checkout m4-step-0
./odoo-project update          # nothing to update; shows the loop command once
```

Developer mode is on (Settings > Activate the developer mode) so Apps > Update Apps List is available.

## Block 3, 10:15 to 10:35: steps 0 and 1, manifest and data (demo, predict)

1. Show `__manifest__.py` and `__init__.py`. "This is an installable module. It does nothing." Apps > Update Apps List >
   search "Well" > Install. `./odoo-project logs` and point at `Loading module dswd_wellbeing`.
2. `git checkout m4-step-1`, then, before running anything, **plant both breakages**: delete the data line from the
   manifest, and change `social_assistance` to `administrative` in the data file. The order matters: the file is
   `noupdate="1"`, so a bad value is only caught the first time the file loads.
3. Show the data file: one vocabulary, three codes. Ask: "After update, where will I see them?" Run
   `./odoo-project update`. Settings > Vocabularies: nothing. **Breakage 1.** Ask for the cause. Show the manifest. Add
   the line. Do not update yet.
4. **Breakage 2.** Ask: "Will this fail in lint, on update, or never?" `./odoo-project lint` passes.
   `./odoo-project update` fails. Read the lines together, bottom up:
   ```
   ValueError: Wrong value for spp.vocabulary.domain: 'administrative'
   odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/data/vocabulary_well_being_level.xml:10
   ```
   Open `vendor/openspp/spp_vocabulary/models/vocabulary.py` at the `domain` selection. Fix. `update`. Show the
   vocabulary and its three System codes. Say: "A failed update rolls back; a `noupdate` record that did load is never
   reloaded. Fix values before the first load, or delete the record."
5. Say what `get_code("urn:dswd:4ps:well-being-level", "survival")` means; it is what the tests use.

## Block 4, 10:35 to 10:50: step 2, the model (demo, predict)

1. `git checkout m4-step-2`, but first **delete the import line in `models/__init__.py`** (breakage 3).
2. Show `models/res_partner.py`: `_inherit`, the `dswd_` prefix, `Many2one` to `spp.vocabulary.code`, the namespace
   domain. Ask: "Why not a Selection with three values?" (32 client statuses, 2,000 IP groups, deployment profiles, no
   release to change a code.)
3. `./odoo-project update`. No error. Settings > Technical > Fields, search `dswd_`: nothing. **Breakage 3.** Ask. Show
   `models/__init__.py`. Restore the import. `update`. The field is listed. "No view yet: a field without a view is
   invisible, not broken."

## Block 5, 10:50 to 10:55: buffer

Questions, or catch up. If ahead of time, show `Settings > Technical > Fields` columns for the field (model, type,
relation) and where `help=` shows up.

## Block 6, 10:55 to 11:10: step 3, the view (demo, predict)

1. Open the upstream form first: `vendor/openspp/spp_registry/views/individual_views.xml`, search `group_tags_section`.
   "One form serves individuals and households; household sections are `group_*`."
2. `git checkout m4-step-3`. Show the view file: `inherit_id`, one XPath on a named anchor, a "4Ps" group, `no_create`,
   `no_open`. Ask: "Where will it appear?" Do not update yet.
3. **Breakage 4** (drop if late: then just `update` and open a household): change `group_tags_section` to
   `group_tag_section` before the first update. `update`. Read:
   ```
   Element '<xpath expr="//group[@name='group_tag_section']">' cannot be located in parent view
   View error context: {'xmlid': 'view_res_partner_form_wellbeing', ...}
   ```
   Fix. `update`. Open a household: set a level. Save. Developer menu > View Form: show the inherited view listed.

## Block 7, 11:10 to 11:25: steps 4 and 5, the tests (demo, predict)

1. `git checkout m4-step-5`. Open `tests/test_wellbeing.py`. Walk one test: `RegistryCommon` gives a household and the
   vocabulary model; `get_code`; `assertEqual`. "The test says what we want before the code exists."
2. Run `./odoo-project test dswd_wellbeing`. While it runs (about 20 s), show `security/ir.model.access.csv`: header
   only, "no new model, no rows", and `readme/DESCRIPTION.md`.
3. Read the output: `0 failed, 0 error(s) of 5 tests` and the `Full log:` line. "This line is the one you read first
   when a colleague says the module is broken."
4. If time: flip `"Subsistence"` to `"Survival"` in `test_household_stores_a_level`, run again, read the
   `AssertionError` and the file:line. Restore.

## Block 8, 11:25 to 11:35: Claude Code (demo only; first block to drop)

1. In the module folder: ask Claude Code to "add a fourth well-being level, `graduated`, with sequence 40, and a test
   that it resolves". Review the diff on screen: is the file in the manifest? Is the code in the right namespace?
2. Run the tests. Say: "The review is the job. The tool types."
3. `git checkout -- .` to discard, or keep it as a stretch example.

## Block 9, 11:35 to 11:50: troubleshooting drill (pairs, paper)

1. Hand out [drill.md](drill.md). 12 minutes, three excerpts, pairs.
2. Walk the room; note which pairs reach C (the silent one). That is your observation-checklist evidence.
3. Debrief with [drill-answers.md](drill-answers.md): C first, then A, then B. One pair reports each.

## Block 10, 11:50 to 12:00: recap and handoff

1. Objectives slide: read the five, ask for a thumbs up on each.
2. What moves to Module 5: new models and menus, groups and record rules, hierarchical vocabularies, programs and
   cycles, change requests, the production module map.
3. Hand out [exercise-day3.md](exercise-day3.md). "Before Module 6: `git checkout m4-step-5` and `./odoo-project start`.
   If your laptop does not run Docker, Tier 1 needs only the folder and your eyes."
4. Point to the lunch triage table.

## If the demo machine fails

- Any step: `git checkout m4-step-N` restores a known-good tree; `./odoo-project update` or `install` restores the
  database state.
- Docker gone: switch to the recording for the current block and continue with the handout code on screen.
- Projector gone: the handout has every file; run the session from paper and the drill.

## Commands used in this session

```bash
./odoo-project start --profile dev     # dynamic port when 8069 is busy
./odoo-project install dswd_wellbeing  # first install (update cannot install)
./odoo-project update                  # after manifest, data, security, new field or view changes
./odoo-project logs                    # Loading module ..., ParseError, cannot be located in parent view
./odoo-project test dswd_wellbeing     # fresh database, 5 tests, about 20 s
./odoo-project lint                    # passes on all four breakages; that is the point
git checkout m4-step-N                 # N from 0 to 5
```
