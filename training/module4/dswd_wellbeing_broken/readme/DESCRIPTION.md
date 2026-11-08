Adds the SWDI well-being level (Survival, Subsistence, Self-Sufficient) to 4Ps households.

This is the first training module. It is the smallest complete `dswd_*` module that extends OpenSPP by data (a
vocabulary) and by model and view (a field on the household form), the same shape as the production `dswd_4ps_*`
modules.

## Key Capabilities

- Ships the "4Ps Well-Being Level" vocabulary (`urn:dswd:4ps:well-being-level`) as a system vocabulary with three
  codes in SWDI order
- Adds a well-being level field to households and shows it in a "4Ps" section of the household Profile page
- Refuses codes from any other vocabulary, so writes from code or the API are guarded, not only the dropdown

## Key Models

- `res.partner` (extended) — `dswd_well_being_level_id`, a Many2one to `spp.vocabulary.code` limited to the
  well-being namespace
- `spp.vocabulary` / `spp.vocabulary.code` (data only) — the vocabulary and its codes `survival`, `subsistence`,
  `self_sufficient`

## Configuration

None. The vocabulary is a system vocabulary; add local codes through Settings > Vocabularies > Manage Vocabularies >
Add Manual Code if a deployment needs more levels.

## UI Location

Registry > Groups > open a household > Profile tab > "4Ps" section (menu root `spp_registry.spp_main_menu_root`).
The vocabulary itself is under Settings > Vocabularies (`spp_vocabulary.menu_vocabulary_root`).

## Security

No new model, so `security/ir.model.access.csv` holds only the header. Access to the field follows the upstream
`res.partner` rules from `spp_registry`.

## Dependencies

- `spp_registry` — households (`res.partner` with `is_registrant` and `is_group`) and the form being extended
- `spp_vocabulary` — vocabulary models and the Settings menu
