# Module 5 Module Catalogue

Day 2, 1:00 to 5:00. One card per production module or module family, in the order of the session, then the index of all
66 modules. Printed as A5 cards for the session and bound as a catalogue participants keep. Facts are counted at
production commit `ad98dac9` (2026-11-06) of `dswd-4ps-dp-openspp-v2-module`; paths on a card are inside that module
unless they name another one.

## How to read a card

- **The table**: the 4Ps process the module serves (with the section of
  [4ps-program-reference.md](../4ps-program-reference.md)), the instance it installs on, what it depends on, how many
  modules depend on it, and its size: Python lines without tests and migrations (manifest included, rounded to two
  significant figures) and the number of `def test_` in its `tests/` folder.
- **Key models**: **new table** is a model with its own `_name`; **extends** is an `_inherit` on an existing model
  (sections 3.7 and 4.6 of the participant guide).
- **The Module 3/4 strip**: twelve boxes, one per part of a module you met in Modules 3 and 4, each with its guide
  section. A shaded box (■) means the module uses that part in a way worth knowing; the word says how. Read a module as
  "which boxes are shaded": that is where its tickets land.
- **Important points**: what changes how a maintainer works on the module. Read these before changing it.
- **A ticket usually lands in**: files, each with a symptom in user words.
- **Code moment** and **code excerpt**: the file the trainer opens on screen, and the lines shown.

## Part 1: The map

### Card 1. `dswd_4ps_starter`, `dswd_4ps_instance1`, `dswd_4ps_instance2`: install bundles, one or two databases

**Purpose.** Install bundles: `dswd_4ps_starter` puts everything in one database; `dswd_4ps_instance1` and
`dswd_4ps_instance2` build the split registry and casework databases joined by the bridge.

| 4Ps process | Instance                                    | Depends on (dswd and spp only)                                                 | Used by | Size                                                   |
| ----------- | ------------------------------------------- | ------------------------------------------------------------------------------ | ------- | ------------------------------------------------------ |
| Deployment  | starter: single; instance1: 1; instance2: 2 | starter 38, instance1 34, instance2 10 direct dependencies (see the manifests) | none    | about 290, 270 and 210 Python lines; 28, 9 and 7 tests |

**Key models**

- No models. Each bundle is a manifest, a `post_init_hook` and an Apps-list filter view.
- Starter has, and instance1 lacks: `dswd_4ps_cms`, `dswd_4ps_cms_nas`, `dswd_4ps_portal_api_casework`, `dswd_4ps_swdi`,
  `dswd_4ps_swdi_api`, `dswd_4ps_swdi_dashboard`. Instance1 has, and starter lacks: `dswd_4ps_bridge_shared`,
  `dswd_4ps_bridge_server`.
- Instance2 lists `dswd_4ps_bridge_shared`, `dswd_4ps_bridge_client`, `spp_studio`, `dswd_4ps_swdi_api`,
  `dswd_4ps_swdi_dashboard`, `dswd_4ps_cms_nas`, `dswd_4ps_portal_api_casework`, `dswd_4ps_theme`, `spp_branding_kit`,
  `dswd_4ps_attachment_hardening`. Counting what they pull in: starter 42, instance1 37, instance2 17 `dswd_4ps_*`
  modules.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ depends    |                |            |                   |              |                        | ■ 44            |          |           |              |                  | ■ 3             |

**Important points**

1. The split is chosen by which bundle is installed. Installing `dswd_4ps_bridge_client` (through instance2) turns a
   database into the casework side; instance1 ships `dswd_4ps_bridge_server` and stays the master registry.
2. `excludes` enforce it: 26 manifests exclude `dswd_4ps_bridge_client` (change requests, compliance, payroll, FDS,
   approval flow data, most APIs, and the bridge server) and 8 exclude `dswd_4ps_bridge_server` (SWDI, CMS and their
   APIs, and the bridge client).
3. Area, registry and roles install on both instances, because the bridge client depends on them. Period and the two
   approval modules install only with starter or instance1.
4. The three `hooks.py` files are copies: each sets the Philippines and PHP on every company, and keeps the currency
   when posted entries exist in another one. A fix to one belongs in all three; starter's migration 19.0.1.2.0 applies
   it to existing databases.
5. `dswd_4ps_swdi_cms` is not in any bundle's own list; it arrives by `auto_install` once SWDI and CMS are both
   installed. Nine modules in the repository are `auto_install`.

**A ticket usually lands in**

- `dswd_4ps_instance2/__manifest__.py`: "The casework server will not install: a module is excluded."
- `dswd_4ps_starter/hooks.py`: "The company currency is still USD."

**Code moment.** `dswd_4ps_instance1/__manifest__.py`: the `depends` list, grouped by layer with comments, and the
description's "Single- vs split-instance" section. A manifest as the map of a deployment (section 3.6).

## Part 2: Foundation

### Card 2. `dswd_4ps_area`: PSGC geography and who sees which area

**Purpose.** Loads the Philippine PSGC geography (region to barangay) into `spp.area` and limits what each user sees to
their assigned areas.

| 4Ps process                                                                 | Instance | Depends on (dswd and spp only)                          | Used by          | Size                                |
| --------------------------------------------------------------------------- | -------- | ------------------------------------------------------- | ---------------- | ----------------------------------- |
| Where they are: geography and area scoping (reference section 5, hierarchy) | both     | `spp_area`, `spp_registry`, `spp_vocabulary`, `spp_gis` | about 22 modules | about 2,200 Python lines, 230 tests |

**Key models**

- `spp.area` (extends): PSGC ids and codes per level (`region_id`, `province_id`, `city_id`, `barangay_id`, `geocode`,
  `psa_code`), `legis_district`, `is_gida`, `is_4ps_area`.
- `res.partner` (extends): stored `area_region_id`, `area_province_id`, `area_city_id`, `area_display`; the computed
  `area_scope_ids` with its own search method; `area_id` relabelled "Barangay" and indexed.
- `res.users` (extends): raw identity-provider areas (`idp_regions`, `idp_provinces`, `idp_cities`, `idp_barangays`),
  stored `region_assignment_ids` (and province, city, barangay), computed `sees_all_areas`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      | ■ stored   | ■ inherits        |              | ■ fail-closed          | ■ 230           | ■ search | ■ queue   |              | ■ 4              | ■ 10            |

**Important points**

1. `hooks.py`: the `post_init_hook` creates regions, provinces and cities at install and queues the barangays (about
   42,000) as job-worker batches of 2,000 on the `psgc_load` channel. It runs only on install, so every later data fix
   ships as a migration (10 so far).
2. Fail-closed for areas: the global rule in `security/area_record_rules.xml` and `_prepare_domain` in `models/area.py`
   show a user with no center areas no areas at all. Only `sees_all_areas` (System Administrator, or the country root as
   a center area) bypasses. Households are filtered by upstream's `spp_area.rule_res_partner_area_filter`, whose
   no-center-area branch is still upstream's `[]`, so that rule does not narrow a user with no center areas.
3. That upstream rule is `noupdate`. The hook rewrites its text in code (adds the `sees_all_areas` bypass, swaps
   `child_of` for `area_scope_ids`), and migrations 19.0.1.6.0, 19.0.1.7.0 and 19.0.1.12.0 repeat it on installed
   databases. Both helpers leave a hand-tuned domain alone and log a warning.
4. `area_scope_ids` in `models/registrant.py` is a performance fix: its comment records 15 to 20 seconds per dashboard
   tile at 7.4 million households, and 99 ms after. Do not "simplify" it back to `child_of`.
5. `_fail_open_area_rules.py` is a shared migration helper that removes the `area_id = False` branch from other modules'
   rules. Four modules are fixed; `dswd_4ps_swdi` keeps the branch on purpose (#2342).

**A ticket usually lands in**

- `models/registrant.py`: "A provincial officer cannot see households in one barangay."
- `models/res_users.py`: "A new user sees no municipalities in the area dropdown."
- `psgc_corrections.py`: "This barangay is listed under the wrong municipality."
- `hooks.py`: "After install there are no barangays" (the `psgc_load` jobs failed or are still waiting).

**Code moment.** `security/area_record_rules.xml`: the global rule's domain, with the `sees_all_areas` bypass and the
`[('id', '=', False)]` branch for users without areas (a follow-up to section 3.12), and the header note that the record
is `noupdate` and changed by migrations. Then `_enqueue_barangay_batch` at the end of `hooks.py` (a job queued with
`with_delay`).

**Code excerpt** (`dswd_4ps_area/security/area_record_rules.xml`, lines 41 to 52 at ad98dac9):

```xml
    <record id="rule_spp_area_center_area_filter" model="ir.rule">
        <field name="name">Areas: visible only within user's center areas</field>
        <field name="model_id" ref="spp_area.model_spp_area" />
        <field
            name="domain_force"
        >[] if user.sees_all_areas else (['|', ('id', 'child_of', user.center_area_ids.ids), ('id', 'parent_of', user.center_area_ids.ids)] if user.center_area_ids else [('id', '=', False)])</field>
        <field name="global" eval="True" />
        <field name="perm_read" eval="True" />
        <field name="perm_write" eval="False" />
        <field name="perm_create" eval="False" />
        <field name="perm_unlink" eval="False" />
    </record>
```

### Card 3. `dswd_4ps_registry`: the 4Ps household and member record

**Purpose.** Holds the 4Ps household and member record: identifiers, client status, grantee, and the vocabularies behind
them.

| 4Ps process                                                              | Instance | Depends on (dswd and spp only)                                                                                                                                                                                                                              | Used by          | Size                                |
| ------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| Who they are: households, members, statuses (reference sections 5 and 6) | both     | `dswd_4ps_area`, `spp_base_common`, `spp_registry`, `spp_vocabulary`, `spp_area`, `spp_banking`, `spp_dms`, `spp_audit`, `spp_service_points`, `spp_registry_search`, `spp_cel_registry_search`, `spp_hide_menus_base`, `spp_studio`, `spp_source_tracking` | about 30 modules | about 6,500 Python lines, 629 tests |

**Key models**

- `res.partner` (extends): household `listahanan_id`, `client_status_id`, `previous_client_status_id`, `set_group_id`,
  `grantee_id`, stored `client_status_category_id` and `is_delisted`; member `member_id_4ps`, `member_status_id`,
  `pregnancy_status_id`, stored `gestation_week`.
- `spp.group.membership` (extends): member fields shown on the roster; clears the household grantee when the Capable
  Grantee role is removed.
- `dswd.4ps.grantee.change`, `dswd.4ps.head.change` (new tables): grantee and head-of-household history.
- `dswd.4ps.grade.level.config`, `dswd.4ps.payroll.account.config` (new tables): grade-level and payroll account
  configuration.
- `spp.health.facility`, `spp.education.facility`, `spp.employment.history` (new tables, `spp.` names): facility
  registries and employment history.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      | ■ stored   | ■ OWL             | ■ 2          | ■ groups               | ■ 629           | ■ SQL    | ■ cron    |              | ■ 27             | ■ 30            |

**Important points**

1. `data/vocabulary_client_status.xml`: 32 statuses (codes 1 to 33, no 27), each with a `parent_id` in one of 9
   categories kept in a separate vocabulary; `client_status_category_id` is computed from that parent. The file is
   `noupdate`, so a new or renamed status needs a migration. The field's `domain` only filters the dropdown; the module
   has no namespace constraint.
2. Writes go through `_4ps_write_hook` in `models/res_partner.py`, which `_register_hook` wires into `spp_audit`'s write
   decorator. The plain `write()` override runs only when that decorator is absent. The hook stamps
   `previous_client_status_id` with raw SQL to avoid a recursive write, and requires a reason and writes a history row
   when the grantee changes.
3. Permanent-exit lock (`_assert_client_status_move_allowed`): a write that does not run as superuser may not move a
   household out of status 3 (system parameter `dswd_4ps_registry.permanent_exit_codes`, default "3"). Any server-side
   `sudo()` path passes, which is how an approved change request or CMS changes it.
4. Three field-name styles on `res.partner`: no prefix (`listahanan_id`), `x_4ps_` (13 fields, such as
   `x_4ps_validation_num` and `x_4ps_employment_status`) and `dswd_export_*`. Some new models carry `spp.` names. Search
   all of them before adding a field.
5. `data/ir_cron.xml` has three crons: daily pregnancy update, daily post-delivery reset, and a monthly aging delist
   (statuses 11, 12, 15 and 26 held for six months become 29, one write per household). Index choices in
   `res_partner.py` are sized for about 53 million partner rows.

**A ticket usually lands in**

- `models/res_partner.py`: "A household at status 3 cannot be reinstated" or "The grantee cannot be changed without a
  reason."
- `models/group_membership.py`: "The grantee disappeared after I edited the member's roles."
- `data/vocabulary_*.xml`: "A new set group is missing from the list."
- `static/src/js/household_search.js`: "Household search ignores the area I picked."

**Code moment.** `data/vocabulary_client_status.xml`: status 3 points to the Delisted category through `parent_id`
(Module 4's hierarchical vocabularies at scale). Then the `client_status_id` and `client_status_category_id` fields in
`models/res_partner.py` (lines 401 to 407 and 533 to 539).

**Code excerpt** (`dswd_4ps_registry/data/vocabulary_client_status.xml`, lines 95 to 101 at ad98dac9):

```xml
    <record id="client_status_3" model="spp.vocabulary.code">
        <field name="vocabulary_id" ref="vocab_client_status" />
        <field name="code">3</field>
        <field name="display">3 - Graduated Due to Improved Level of Well-Being</field>
        <field name="parent_id" ref="client_status_category_delisted" />
        <field name="sequence">3</field>
    </record>
```

### Card 4. `dswd_4ps_roles`: the 4Ps organisation chart as security

**Purpose.** Turns the 4Ps organisation (POO, RPMO, NPMO, field positions and payroll units) into Odoo groups and user
roles, scoped by area where the role is local.

| 4Ps process                                   | Instance | Depends on (dswd and spp only)                                                                                                                                                                                                                          | Used by          | Size                                |
| --------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| Who may see and approve (reference section 5) | both     | `dswd_4ps_area`, `dswd_4ps_registry`, `spp_change_request_v2`, `spp_security`, `spp_user_roles`, `spp_area`, `spp_hazard`, `spp_dms`, `spp_registry`, `spp_programs`, `spp_session_tracking`, `spp_vocabulary`, `spp_api_v2`, `spp_cel_registry_search` | about 20 modules | about 1,200 Python lines, 202 tests |

**Key models**

- `res.users` (extends): office fields (`dswd_4ps_office_name`, `dswd_4ps_office_address`, `dswd_4ps_contact_number`),
  `center_areas_locked`; syncs local role areas from the identity provider; protects the built-in admin.
- `res.users.role.line` (extends): `auto_synced`.
- `dswd.4ps.remove.admin.workaround` (new table, wizard): removes the System Admin workaround from C/ML users.
- Data, not models: 54 groups (`security/groups.xml`), 48 roles (29 local, 19 global, one of which edits upstream's
  System Admin role), 5 record rules.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      |            | ■ inherits        | ■ 1          | ■ groups               | ■ 202           |          |           |              |                  | ■ 20            |

**Important points**

1. `security/groups.xml`: three umbrella groups, `group_4ps_poo`, `group_4ps_rpmo` and `group_4ps_npmo`, are the
   approval-tier targets. Sub-roles (MSWDO, SWO III, ProvLink, RGO, RCVO and others) imply them. POO implies
   `group_cr_validator`, RPMO `group_cr_validator_hq`, NPMO `group_cr_manager`.
2. Every group, role and rule file is `noupdate`; the header of `groups.xml` says any change needs a migration script.
   20 migration folders so far.
3. Local roles (`data/local_roles.xml`) are area-scoped. `models/res_users.py` rewrites their areas from the
   identity-provider assignment on create and on write, unless RITO has set `center_areas_locked`.
4. Safeguards in `models/res_users.py`: the built-in admin always keeps System Administrator and the System Admin role,
   and `set_groups_from_roles` never drops the last system administrator. The context flags `_syncing_role_areas` and
   `_ensuring_admin_role` stop recursion; keep them.
5. `hooks.py` rewrites two upstream `noupdate` change-request rules: the validator rule is scoped to the user's center
   areas, and the global CR area rule gets the `sees_all_areas` bypass. `security/rito_rules.xml` lets RITO manage users
   in its own areas and hides the System Admin role from it.

**A ticket usually lands in**

- `models/res_users.py`: "A user lost access after a role change" or "My areas reset every time I log in."
- `security/groups.xml`: "A SWO III cannot open the household form."
- `hooks.py`: "A validator sees change requests from another province."

**Code moment.** `security/groups.xml`: an umbrella group and a sub-role whose `implied_ids` link to it, the same
pattern as the Module 3 tiers. Then the `migrations/` folder listing: 20 versions, because `noupdate` groups need a
migration for every change.

**Code excerpt** (`dswd_4ps_roles/security/groups.xml`, lines 103 to 110 at ad98dac9):

```xml
    <record id="group_4ps_poo_mswdo" model="res.groups">
        <field name="name">4Ps POO: MSWDO</field>
        <field name="comment">Municipal Social Welfare and Development Officer at provincial level.</field>
        <field name="implied_ids" eval="[
            Command.link(ref('group_4ps_poo')),
            Command.link(ref('spp_registry.group_registry_officer')),
        ]"/>
    </record>
```

### Card 5. `dswd_4ps_approval_multi_group`: several approver groups per step

**Purpose.** Lets one approval definition or tier name several groups, and any member of any of them may approve.

| 4Ps process                                       | Instance | Depends on (dswd and spp only) | Used by         | Size                             |
| ------------------------------------------------- | -------- | ------------------------------ | --------------- | -------------------------------- |
| Who may approve BUS updates (reference section 6) | 1        | `spp_approval`                 | about 2 modules | about 180 Python lines, 13 tests |

**Key models**

- `spp.approval.tier` (extends): `approval_group_ids`.
- `spp.approval.definition` (extends): `approval_group_ids`; computed `all_approval_group_ids` for the list view.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ overrides    | ■ M2M      | ■ inherits        |              |                        | ■ 13            |          |           |              |                  |                 |

**Important points**

1. `_check_approval_config` in `models/approval_definition.py` and `_check_approver_config` in `models/approval_tier.py`
   replace the upstream constraints without calling `super()`. If upstream adds a check to either, it does not run here
   until this module copies it.
2. `get_approvers` returns the active users of every listed group (OR). It falls back to `super()` when only upstream's
   single `approval_group_id` is set.
3. The definition-level `get_approvers` does not remove the submitter; self-approval is left to the mixin's
   `auto_approve_same_user`.
4. Only `dswd_4ps_approval_flow_data` and `dswd_4ps_account_creation` depend on it. It adds fields to upstream models
   and no new model, so it has no `ir.model.access.csv`.

**A ticket usually lands in**

- `models/approval_tier.py`: "RCVO is listed on the tier but no RCVO is offered the approval."
- `models/approval_definition.py`: "Saving a definition says: Please select at least one approval group."
- `views/approval_tier_views.xml`: "The tier form shows only one approver group."

**Code moment.** `models/approval_definition.py`: the docstring of `_check_approval_config` says it replaces the base
constraint entirely. An override without `super()`, against the `_inherit` pattern from section 3.7.

**Code excerpt** (`dswd_4ps_approval_multi_group/models/approval_definition.py`, lines 65 to 71 at ad98dac9):

```python
    def _check_approval_config(self):
        """Override to accept approval_group_ids as alternative to approval_group_id.

        This replaces the base constraint entirely (same method name wins in
        MRO). If another module also overrides _check_approval_config, it must
        account for approval_group_ids or be loaded before this module.
        """
```

### Card 6. `dswd_4ps_approval_flow_data`: who approves each change-request type

**Purpose.** A data-only module that says who approves each 4Ps change-request type, chosen by CEL conditions on the
status transition.

| 4Ps process                                       | Instance | Depends on (dswd and spp only)                                                                        | Used by         | Size                            |
| ------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------- | --------------- | ------------------------------- |
| Who may approve BUS updates (reference section 6) | 1        | `dswd_4ps_approval_multi_group`, `dswd_4ps_change_request`, `dswd_4ps_roles`, `spp_change_request_v2` | about 3 modules | about 51 Python lines, 57 tests |

**Key models**

- No new models. Records of `spp.approval.definition` (21) and `spp.approval.tier` (8) in 8 files.
- `spp.change.request.type` (records it writes): candidate definitions or a fixed definition per type, in
  `data/cr_type_approval_config.xml`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ auto       |                |            |                   |              |                        | ■ 57            |          |           |              |                  | ■ 6             |

**Important points**

1. 21 definitions in 8 files; `data/cr_type_approval_config.xml` links 19 of them to 6 change-request types. The
   manifest description still says 20 definitions across 7 types.
2. Update Household Info, Update Individual 4Ps and Reinstate Household list candidate definitions: lowest sequence
   first, the first matching CEL wins, and a transition no definition matches auto-approves (the catch-all RGO
   definition was removed; migration 19.0.1.3.0 deletes it).
3. The Change Address and Update Transfer Account definitions ship dormant (not linked), so those types auto-approve on
   submit. Update Pregnancy has only an exception definition.
4. All files are `noupdate`: a new approver or transition needs a migration (6 so far), and the migrations check the
   original value first so admin edits survive. The `<function>` calls that switch on multi-tier run only on first
   install.
5. Manifest: `auto_install` is true and it `excludes` `dswd_4ps_bridge_client`, so it installs by itself on the registry
   side and never on the casework instance.

**A ticket usually lands in**

- `data/approval_defs_update_hh_info.xml`: "Nobody can approve a client-status change from 24 to 3."
- `data/cr_type_approval_config.xml`: "Change Address requests are approved with no review."
- `migrations/`: "We changed the approver in the XML but production still routes to the old group."

**Code moment.** `data/approval_defs_update_hh_info.xml`, definition 4 (24 to 3): a CEL condition on `old_value.code`
and `new_value.code`, two tiers (SWO III, then RGO) and `noupdate="1"` at the top. Data as configuration, and why it
needs a migration to change.

**Code excerpt** (`dswd_4ps_approval_flow_data/data/approval_defs_update_hh_info.xml`, lines 81 to 91 at ad98dac9):

```xml
    <record id="approval_def_hh_info_poo_rpmo" model="spp.approval.definition">
        <field name="name">Family - Update Family Info - CS (24 → 3)</field>
        <field name="model_id" ref="spp_change_request_v2.model_spp_change_request" />
        <field name="approval_type">group</field>
        <field name="approval_group_ids" eval="[Command.link(ref('dswd_4ps_roles.group_4ps_swo_iii'))]" />
        <field name="sequence">10</field>
        <field name="use_cel_condition" eval="True" />
        <field name="cel_condition">record.selected_field_name == "client_status_id" and old_value.code == "24" and new_value.code == "3"</field>
        <field name="sla_days">10</field>
        <field name="is_require_comment" eval="True" />
    </record>
```

### Card 7. `dswd_4ps_period`: compliance months and the working-day calendar

**Purpose.** Provides one compliance period per calendar month and the Philippine holiday calendar used to count
statutory working-day deadlines.

| 4Ps process                                                  | Instance | Depends on (dswd and spp only) | Used by         | Size                             |
| ------------------------------------------------------------ | -------- | ------------------------------ | --------------- | -------------------------------- |
| When: compliance periods (reference section 4) and deadlines | 1        | none (`base` only)             | about 4 modules | about 590 Python lines, 69 tests |

**Key models**

- `spp.compliance.period` (new table, `spp.` name): one row per month, `code` such as `2026-03`, `date_start`,
  `date_end`; `get_or_create()`.
- `dswd.4ps.holiday.year` (new table): one row per year, state Draft or Seeded, `has_pending_proclamations`.
- `dswd.4ps.holiday` (new table): one holiday per date; hosts `is_working_day`, `add_working_days`,
  `count_working_days`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8    | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15    | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ------------- | ----------------- | ------------ | ---------------------- | --------------- | ----------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ new          | ■ constraints | ■ settings        |              |                        | ■ 69            | ■ savepoint |           |              |                  | ■ 1             |

**Important points**

1. Fail-loud: `_assert_year_seeded` in `models/holiday.py` raises an error for any year that is not Seeded, instead of
   counting weekends alone and giving a deadline that is too early.
2. `data/ph_holidays_2027.xml` ships 2027 as an empty Draft year on purpose. Each December an administrator enters the
   next year's proclamation under Settings > DSWD 4Ps > Holiday Calendar and marks it Seeded. Do not add a 2028 file: a
   year already entered in the UI would stop the upgrade on `UNIQUE(year)`.
3. `data/ph_holidays_2026.xml` nests its 18 holidays inside the year record, because a `<function>` in a `noupdate` file
   runs only on install; migration 19.0.1.1.0 repairs databases left with a Draft 2026. Eid'l Fitr and Eid'l Adha are
   missing until proclaimed (`has_pending_proclamations`).
4. `_as_date` refuses a datetime (a UTC value would fall on the previous Manila day after 16:00 UTC) and an empty value.
   Pass dates.
5. `get_or_create` in `models/compliance_period.py` uses `sudo()` and a savepoint, so two field users creating the same
   month at once do not fail on `UNIQUE(month, year)`.

**A ticket usually lands in**

- `data/ph_holidays_2027.xml`: "The 2027 working-day deadline raises an error."
- `models/holiday.py`: "The processing deadline is one day early" (a proclaimed holiday not entered).
- `models/compliance_period.py`: "Error: a period already exists for this month and year."

**Code moment.** `models/holiday_year.py`: the Draft and Seeded `state` field and the constraint that a Seeded year must
have holidays. A selection field and `@api.constrains` used as a guard (section 3.8).

**Code excerpt** (`dswd_4ps_period/models/holiday_year.py`, lines 34 to 44 at ad98dac9):

```python
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("seeded", "Seeded"),
        ],
        string="Status",
        required=True,
        default="draft",
        help="Deadlines are only computed across years marked Seeded. A Draft "
        "year is treated as unmaintained and refused.",
    )
```

## Part 3: Change requests

### Card 8. `dswd_4ps_change_request`: the Beneficiary Update System on OpenSPP change requests

**Purpose.** Defines the 4Ps change request types that field officers file to update a household or member record, and
adds batching, cancellation, document rules, update limits and access control around them.

| 4Ps process             | Instance | Depends on (dswd and spp only)                                                                                                                                                                                                                         | Used by          | Size                                 |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- | ------------------------------------ |
| BUS updates (section 8) | 1        | `spp_change_request_v2`, `spp_dms`, `spp_cr_types_base`, `spp_cr_types_advanced`, `spp_approval`, `spp_registry`, `spp_area`, `dswd_4ps_area`, `dswd_4ps_registry`, `dswd_4ps_compliance`, `dswd_4ps_field_limit`, `dswd_4ps_roles`, `dswd_4ps_period` | about 10 modules | about 12,000 Python lines, 826 tests |

**Key models**

- `spp.change.request` (extends): `batch_id`, document validation by conditions and groups at submit, frequency and
  field-limit checks, a job that copies documents to the registrant on apply.
- `spp.approval.mixin` (extends): adds `cancelled` to `approval_state`, with `cancelled_by_id`, `cancelled_date` and
  `cancellation_reason`.
- `spp.cr.detail.change_address` and 30 more detail models and lines (new tables): the proposed values, one model per
  type, such as `spp.cr.detail.update_member_info`.
- `spp.cr.batch` (new table): groups change requests under a `ticket_number`, with stored counts per state.
- `dswd.cr.parent.access.mixin` (new, abstract): detail rows, lines and CR documents follow the access of their parent
  change request.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15    | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | ----------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ detail       | ■ related  | ■ forms           | ■ cancel     | ■ mixin                | ■ 826           | ■ overrides | ■ queue   |              |                  | ■ 27            |

**Important points**

1. A type plugs into upstream `spp_change_request_v2` as data: `data/cr_type_*.xml` (22 files: 20 new 4Ps types, two
   upstream types reused; nine generic upstream types are archived in `data/deactivate_generic_cr_types.xml`). Each
   record names a detail model and an apply strategy: 9 types use `field_mapping`, 11 use `custom` with an
   `spp.cr.apply.*` model. Approval comes from `spp.approval.mixin`, routed by `dswd_4ps_approval_flow_data`. The type
   files are `noupdate="1"`, so a change to a shipped type needs a post-migrate script; most of the 27 migrations exist
   for this reason.
2. `models/approval_mixin.py` adds `cancelled` to the upstream approval mixin itself, so every model that uses
   `spp.approval.mixin` on the database gets the state; cancelling also cancels the pending reviews.
   `models/cr_batch.py` groups requests under one ticket number, and `change_request.py` refuses to move a request from
   one batch to another.
3. Derived requests: when a newborn's Add Member is applied, `models/cr_apply_add_member_4ps.py` creates an Update
   Pregnancy request for each pregnant parent and an Update Member Additional Information request for each parent whose
   solo-parent flag changes. They apply at once only because no approval definition matches them, and they skip document
   validation. Do not add an approval definition that matches them.
4. Access without record rules: `models/cr_parent_access.py` overrides `_search`, `_check_access` and `write` so a
   detail row, a detail line or a CR document is visible only when its parent change request is. A record rule cannot do
   this, because Odoo evaluates rule domains as superuser. A new detail line model needs a class in
   `models/cr_child_access.py`; `tests/test_2830_cr_child_scoping.py` fails without one.
5. The module uses 14 context keys of its own; 11 of them skip or override a check (`skip_doc_validation`,
   `skip_field_update_limit`, `dup_override`, `skip_cr_notification`, `skip_dup_autoscan`, and others). Some are set
   here and read in `dswd_4ps_registry`. Search the whole repository before removing or renaming one.

**A ticket usually lands in**

- `models/cr_detail_<type>.py` and `views/detail_<type>_views.xml`: "The request form has no field for the new value."
- `models/change_request.py`: "I cannot submit: it says documents are missing" or "the maximum number of requests for
  this year is reached."
- `models/cr_apply_add_member_4ps.py`: "We added the newborn but the mother still shows as pregnant."
- `data/cr_type_*.xml` with a migration: "The renamed request type still shows the old name on production."

**Code moment.** `data/cr_type_change_address.xml`: point at `detail_model`, `apply_strategy` and `noupdate="1"`; a
change request type is a data record (Module 4 data files), and the mapping records below it copy `new_area_id` and
`new_address` to the household. Then open `models/cr_detail_change_address.py`
(`_inherit = ["spp.cr.detail.base", ...]`) and `models/cr_parent_access.py` (the docstring says why there is no record
rule).

**Code excerpt** (`data/cr_type_change_address.xml`, lines 13 to 23 at ad98dac9):

```xml
    <record id="cr_type_change_address" model="spp.change.request.type">
        <field name="name">Change Address</field>
        <field name="code">change_address</field>
        <field name="description">Change the geographic area and address for a household</field>
        <field name="target_type">group</field>
        <field name="detail_model">spp.cr.detail.change_address</field>
        <field name="detail_form_view_id" ref="dswd_4ps_change_request.spp_cr_detail_change_address_form" />
        <field name="apply_strategy">field_mapping</field>
        <field name="auto_apply_on_approve">True</field>
        <field name="icon">fa-map-marker</field>
        <field name="sequence">50</field>
```

### Card 9. `dswd_4ps_supporting_docs_data`: which documents each request type needs

**Purpose.** Sets, as data, the supporting documents each 4Ps change request type accepts or requires, using one list of
22 canonical document types.

| 4Ps process             | Instance | Depends on (dswd and spp only)                                       | Used by        | Size                             |
| ----------------------- | -------- | -------------------------------------------------------------------- | -------------- | -------------------------------- |
| BUS updates (section 8) | 1        | `dswd_4ps_change_request`, `spp_vocabulary`, `spp_cr_types_advanced` | about 1 module | about 260 Python lines, 10 tests |

**Key models**

- `spp.change.request.type` (extends): adds `trigger_api_paths`, the API payload paths that create each type; the data
  files also set `document_validation_mode` and `available_document_ids`.
- `spp.cr.type.document.group` (records only; the model is in `dswd_4ps_change_request`): "any N of these documents",
  such as any one of seven for Add Member.
- `spp.cr.type.document.condition` (records only): a document required when a field changes, such as a Medical
  Certificate when sex changes.
- `spp.vocabulary.code` (records only): the 22 canonical document types in `urn:openspp:vocab:cr_document_type`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      |            |                   |              |                        | ■ 10            |          |           |              | ■ 22             | ■ 3             |

**Important points**

1. A data module with `auto_install: True`: it installs itself with `dswd_4ps_change_request`. Every data file is
   `noupdate="1"`, so a change reaches existing databases only through a post-migrate script; all three migrations exist
   for that reason.
2. `hooks.py` (`pre_init_hook`) runs before the data loads: it archives the legacy per-type document codes, reuses four
   of them by giving them the canonical XML ids (so existing DMS files keep a valid document type), and wipes every
   type's document bindings, conditions and groups.
3. Three rule kinds, checked at submit by `dswd_4ps_change_request` (`_validate_documents`): the available list, groups
   ("any N of"), and conditions ("required when this field changes"). `document_validation_mode` is `required`,
   `warning` or `none`; `data/cr_type_opt_out.xml` sets `none` on the types DSWD has no list for yet.
4. `trigger_api_paths` feed the mobile app's `$required_documents` endpoint in `dswd_4ps_api_change_request`.
   `tests/test_trigger_paths_match_submission.py` guards drift, but its member-field test always skips: it looks for a
   `MEMBER_API_ALIAS` table that no longer exists in the submission service.
5. Document pools differ per type: a Barangay Certificate is valid for Add Member but not for Update Pregnancy. That is
   why derived requests skip document validation; test data with one shared document hides this kind of bug.

**A ticket usually lands in**

- `data/cr_type_<type>.xml`: "Add Member now needs one more document" or "this document should also be accepted."
- `data/vocabulary_canonical_docs.xml`: "The document type we need is not in the dropdown."
- `migrations/<version>/post-migrate.py`: "The document change works on a fresh install but not on production."

**Code moment.** `data/cr_type_add_member_4ps.xml`: point at `noupdate="1"`, the record id that names a record of
another module (`dswd_4ps_change_request.cr_type_add_member_4ps`), and the group with `min_required` 1. Data files can
extend a record another module created (Module 4 data files and vocabularies).

**Code excerpt** (`data/cr_type_add_member_4ps.xml`, lines 13 to 17 at ad98dac9):

```xml
<odoo noupdate="1">

    <record id="dswd_4ps_change_request.cr_type_add_member_4ps" model="spp.change.request.type">
        <field name="document_validation_mode">required</field>
        <field name="trigger_api_paths">addMembers[]</field>
```

### Card 10. `dswd_4ps_field_limit`: how often a registry field may change

**Purpose.** Limits how many times a registrant's name, sex, birthdate and contact number may be changed after
registration, as the BDMD Field Operations Manual requires, and keeps a count per registrant.

| 4Ps process                                     | Instance | Depends on (dswd and spp only) | Used by         | Size                             |
| ----------------------------------------------- | -------- | ------------------------------ | --------------- | -------------------------------- |
| BUS updates, one-time update fields (section 8) | 1        | `spp_registry`, `spp_security` | about 4 modules | about 440 Python lines, 48 tests |

**Key models**

- `spp.field.update.limit` (new table): `field_id`, `model_scope` (`res.partner` or `spp.group.membership`),
  `maximum_updates`, `code`.
- `spp.field.update.log` (new table): `limit_id`, `partner_id`, `update_count`, `last_update_date`; one row per limit
  and registrant.
- `res.partner` (extends): no new fields; `write` checks and counts the limited fields.
- `spp.group.membership` (extends): the same check on membership fields, counted per individual.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ overrides    |            |                   |              | ■ admin                | ■ 48            | ■ lock   |           |              |                  | ■ 2             |

**Important points**

1. `models/res_partner.py` and `models/spp_group_membership.py` override `write`. Every write that changes a limited
   field counts, whoever makes it: an applied change request, an import or an administrator. Only the
   `skip_field_update_limit` context key bypasses the check, and it is logged.
2. `models/spp_field_update_limit.py` reads the log rows with raw SQL `SELECT ... FOR UPDATE`, so two writes for the
   same registrant cannot both pass the limit. Do not replace it with a plain ORM search.
3. The six one-time limits are seeded in `data/field_limit_one_time_fields.xml` (`noupdate="1"`). The
   relationship-to-head limit is seeded by `dswd_4ps_change_request/data/field_limit_membership_fields.xml`. A change to
   a seeded value needs a migration; a value an administrator changed survives upgrades.
4. `dswd_4ps_change_request` repeats the check at submit (`_check_field_update_limits` in `models/change_request.py`),
   so the officer learns before approval. A rule change has to keep both checks in step.
5. Only `base.group_system` can create or change limits and logs; every internal user can read them.

**A ticket usually lands in**

- `data/field_limit_one_time_fields.xml` and a migration: "Birthdate should be correctable twice, not once."
- `models/spp_field_update_limit.py`: "It says the name was already changed, but we never changed it."
- `dswd_4ps_change_request/models/change_request.py`: "The request was approved but failed when it was applied."

**Code moment.** `models/res_partner.py`: a `write` override on an inherited model (`_inherit = "res.partner"`, Module 3
models and ORM), with the context key that bypasses it at the top.

**Code excerpt** (`models/res_partner.py`, lines 16 to 24 at ad98dac9):

```python
    def write(self, vals):
        """Override write to enforce Registry-scoped field update limits."""
        if self.env.context.get("skip_field_update_limit"):
            _logger.info(
                "Field update limits bypassed for partner IDs: %s by user %s",
                self.ids,
                self.env.user.login,
            )
            return super().write(vals)
```

## Part 4: Compliance and FDS

### Card 11. `dswd_4ps_compliance`: the Compliance Verification System

**Purpose.** Turns school attendance, health visit, deworming and FDS attendance reports into monthly compliance status
rows per member and household, which payroll reads.

| 4Ps process                                 | Instance | Depends on (dswd and spp only)                                                                                                                                                         | Used by          | Size                                |
| ------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| Conditionalities and compliance (section 4) | 1        | `spp_registry`, `dswd_4ps_registry`, `dswd_4ps_period`, `spp_programs`, `spp_event_data`, `spp_session_tracking`, `spp_hazard_programs`, `spp_area`, `dswd_4ps_area`, `dswd_4ps_roles` | about 17 modules | about 8,400 Python lines, 693 tests |

**Key models**

- `spp.event.data` (extends): `flag_reason`, `x_cv_note`; `create` and `write` queue a compliance job for each active
  `cv_health`, `cv_school` or `cv_deworming` event.
- `spp.cv.compliance.pipeline` (new, abstract): the computation, called as `self.env["spp.cv.compliance.pipeline"]`.
- `spp.education.compliance.status`, `spp.health.compliance.status`, `spp.fds.compliance.status`,
  `spp.deworming.compliance.status` (new tables): one row per member (or grantee) and period, with a `waived` status for
  hazards.
- `res.partner` (extends): `x_4ps_cv_needs_reconcile`, `x_4ps_school_compliance_status`,
  `x_4ps_health_compliance_status`, `x_4ps_fds_compliance_status`, `x_4ps_education_grant`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      | ■ `x_4ps_` | ■ OWL             | ■ grant      | ■ rules                | ■ 693           | ■ SQL    | ■ locks   |              | ■ 6              | ■ 24            |

**Important points**

1. Reconcile later, not on every write. `models/event_data.py` queues one job per event; the job writes the member's
   status row and sets `x_4ps_cv_needs_reconcile` on the household. The daily cron "4Ps CV: Reconcile Compliance"
   reconciles the flagged households in parallel jobs. FDS attendance arrives as `spp.session.attendance`, not as an
   event, and flags the household the same way.
2. Per-household PostgreSQL advisory locks: the event job takes `pg_try_advisory_xact_lock` and requeues itself when the
   lock is busy; the reconcile takes the blocking lock. The comments explain why a blocking wait in the job would fail
   under REPEATABLE READ; do not "simplify" this.
3. The school status uses the constant `SCHOOL_ATTENDANCE_THRESHOLD = 85.0` in `models/compliance_pipeline.py`. The
   system parameter `dswd_4ps.education_attendance_threshold` only feeds the display fields in
   `models/education_compliance_status.py`, so changing it does not change any status.
4. Hazards (force majeure) set a row to `waived`, which pays like `compliant`; the computed value is kept in
   `pre_exemption_status`. The client-status 21 and 28 exemptions and the per-pillar household rules for payment are
   applied in `dswd_4ps_payroll` (`cv_entitlement_manager.py`), not here.
5. The status rows are a cache rebuilt from events and attendance. A fix to a rule needs a test that creates
   `spp.event.data` events, not one that writes status rows directly.

**A ticket usually lands in**

- `models/event_data.py`: "The school form was submitted but nothing changed for the child."
- `models/compliance_pipeline.py`: "The child attended 86% but is marked non-compliant."
- `data/vocabulary_compliance_reasons.xml` with a migration: "We need a new reason for non-attendance."

**Code moment.** `models/event_data.py`: `_inherit = "spp.event.data"`, then `create` queuing `_cv_process_compliance`
with `with_delay` (Module 3 jobs), then the job's lock, retry and household flag. Then the top of
`models/compliance_pipeline.py` (the constants and the lock namespace), read for its structure only.

**Code excerpt** (`models/event_data.py`, lines 160 to 171 at ad98dac9):

```python
            self.with_delay(
                channel="cv_events",
                description="CV: Process compliance event (retry)",
                eta=5,
            )._cv_process_compliance()
            return

        self._cv_compute_from_event(self.env["spp.cv.compliance.pipeline"])

        # Mark household for deferred aggregation by the reconciliation cron
        if household:
            household.write({"x_4ps_cv_needs_reconcile": True})
```

### Card 12. `dswd_4ps_fds_operations`: Family Development Sessions in the field

**Purpose.** Runs Family Development Sessions: parent groups, the session library, quarterly plans with approval,
sessions and attendance, equivalencies, outcome (TPP) assessments and the FDS Accomplishment Report.

| 4Ps process                          | Instance | Depends on (dswd and spp only)                                                                                                                                                          | Used by         | Size                                   |
| ------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------- |
| Monthly FDS, a condition (section 4) | 1        | `dswd_4ps_area`, `dswd_4ps_compliance`, `dswd_4ps_registry`, `dswd_4ps_roles`, `spp_approval`, `spp_registry_group_hierarchy`, `spp_session_tracking`, `spp_registry`, `spp_vocabulary` | about 8 modules | about 12,000 Python lines, 1,115 tests |

**Key models**

- `spp.session` (extends): `on_hold` added to `state`, `session_topic_id`, `parent_group_id`, `plan_id`,
  `session_subtype_id`.
- `res.partner` (extends): a parent group is a group with type code `parent_group`; adds `pg_status`, `pg_max_members`,
  `pg_curriculum_track_id`, `pg_parent_leader_id`.
- `dswd.fds.plan` (new table): the quarterly plan of a municipality, on `spp.approval.mixin`.
- `dswd.fds.equivalency` (new table): credit for an FDS attended another way; validating it creates attendance.
- `dswd.fds.tpp.assessment` (new table): the TPP competency assessment of a household.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ new          | ■ stored   | ■ OWL             | ■ 10         | ■ global               | ■ 1,115         | ■ SQL    | ■ cron    | ■ QWeb       | ■ 15             | ■ 21            |

**Important points**

1. `models/spp_session.py` adds `on_hold` to the upstream session state with `selection_add` and
   `ondelete={"on_hold": "set default"}`, and keeps its own table of allowed transitions; state changes go through
   `write`.
2. `models/fds_equivalency.py`: a validated equivalency creates a synthetic FDS session and an attended row per
   household, then walks the session to Completed. Compliance and the reports count it like any session, so they need no
   special case. Resetting the equivalency deletes them; do not "clean up" these sessions by hand.
3. Parent groups: `pg_max_members` defaults to 30 and is checked in `models/res_partner.py` and the assign, merge and
   transfer wizards; `models/spp_group_membership.py` allows one Parent Leader and one Assistant Parent Leader per
   group. The curriculum track is computed by majority of member households' registration dates (before or after 1
   January 2026, ties to TLP-NB); NPMO can set an override field protected by `groups=`.
4. `security/ir_rule.xml` (`noupdate="1"`) has 14 record rules, 13 of them global (no `groups`), AND-ed with the
   upstream group rules. A user with no center area sees no FDS sessions. A rule change needs a post-migrate script.
5. The household screens are separate `res.partner` form views at priority 99 opened by the FDS actions, not inherited
   upstream forms; the module inherits only one view.

**A ticket usually lands in**

- `models/spp_session.py`: "I cannot put a session back to scheduled."
- `models/fds_equivalency.py`: "The equivalency was validated but the household is still non-compliant for FDS."
- `security/ir_rule.xml` and a migration: "The C/ML cannot see the sessions of their own barangay."

**Code moment.** `models/fds_equivalency.py`, `_create_credited_attendance`: the session values dated to
`date_completed`, with the FDS session type that the compliance pipeline looks for. Data built in code so a downstream
module needs no special case (Module 3 models and ORM `create`).

**Code excerpt** (`models/fds_equivalency.py`, lines 439 to 446 at ad98dac9):

```python
        session_vals = {
            "name": _("Equivalency: %(ref)s", ref=self.name),
            "session_type_id": fds_type.id,
            "date": self.date_completed,
            "facilitator_id": self.env.user.id,
            "session_topic_id": self.substitute_session_id.id or False,
            "session_subtype_id": special_fds_code.id if special_fds_code else False,
        }
```

## Part 5: Payroll

### Card 13. `dswd_4ps_payroll`: the monthly cash-grant payroll run

**Purpose.** Turns enrolment, compliance and grant rates into the sealed household list, the approvals, the Land Bank
files and the payment results for each regular 4Ps payroll cycle.

| 4Ps process                        | Instance | Depends on (dswd and spp only)                                                                                                                                                                                             | Used by          | Size                                   |
| ---------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- |
| Paying the cash grants (section 3) | 1        | `spp_programs`, `spp_approval`, `spp_cel_domain`, `spp_audit_programs`, `dswd_4ps_registry`, `dswd_4ps_compliance`, `dswd_4ps_period`, `dswd_4ps_approval_flow_data`, `dswd_4ps_hazard`, `dswd_4ps_roles`, `dswd_4ps_area` | about 10 modules | about 50,000 Python lines, 2,252 tests |

**Key models**

- `dswd.4ps.payroll.cycle.run` (new table): one run of a cycle. Its `state` field is the pipeline: 17 steps from `draft`
  to `done`, plus `rejected` and `cancelled`. A rejected run stays for audit and a new run is created.
- `dswd.4ps.payroll.snapshot.beneficiary` (new table): one sealed row per household per run, the snapshot (the code
  calls it NAPA). Everything after it reads this row, not the live registry.
- `dswd.4ps.payroll.cv.grant.rate` (new table): the amount per grant component (health, three education tiers, F1KD,
  rice) per date range.
- `spp.cycle` (extends): `payroll_run_ids`, `program_archetype`, `payroll_health_period_id`,
  `payroll_education_period_ids`.
- `spp.payment` (extends): `delivery_status`, `lbp_batch_number`, `snapshot_beneficiary_id`, `run_id`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8  | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17  | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ----------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | ---------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ states       | ■ selection | ■ inherited       | ■ 12         | ■ roles                | ■ 2,252         | ■ SQL    | ■ channels | ■ PDF        | ■ 3              | ■ 24            |

**Important points**

1. The point of no return. `models/payroll_cycle_run.py` sets `POINT_OF_NO_RETURN_STATES` to `instructions_generated`,
   `lbp_uploaded` and `done`. From Credit Instructions on, `action_cancel` refuses, and
   `wizard/rejection_rewind_wizard.py` offers no rewind. Before it, a rewind sets the old files to `active=False` and
   creates a new run; nothing is deleted. Keep it that way.
2. The snapshot cannot be edited. `write()` in `models/snapshot_beneficiary.py` refuses every field except `active`,
   `invalidated_at`, `write_date` and `write_uid`. Rows are sealed when they are created. To correct a snapshot, rewind
   the run; do not widen the allowlist.
3. Grant rates are never deleted. `models/cv_grant_rate.py` refuses every delete and says to archive instead. A rate
   change is a new row with a later Effective From. Two active rows for one component may not share a start date. The
   docstring warns not to "finish" ticket #1879 by banning overlaps.
4. Five job channels in `data/queue_data.xml`: `payroll_enrollment`, `payroll_run`, `payroll_pdf`, `payroll_lbp` and
   `payroll_entitlement`. Large steps fan out into chunk jobs, and a barrier job finishes the step. The file is
   `noupdate`, so operations can tune the limits. A new heavy step goes on a channel, not on the root channel.
5. Raw SQL: about 110 `cr.execute` calls outside tests. The snapshot is written by one `INSERT ... SELECT`, so the ORM
   never validates it. A new snapshot field needs the SQL changed too, and a test checks that the SQL and the selection
   lists still match.

**A ticket usually lands in**

- `wizard/rejection_rewind_wizard.py`: "We need to cancel the run, but credit instructions were already generated."
- `models/snapshot_beneficiary.py`: "We updated the grantee's name but the payroll list still shows the old one."
- `data/queue_data.xml` and the job queue: "The run has been on Running Entitlement for hours."

**Code moment.** `models/payroll_cycle_run.py`: `STATE_SELECTION` (line 122) and the frozensets under it, then
`action_cancel`; then the `write()` guard in `models/snapshot_beneficiary.py`. A selection field used as a state machine
(3.8), and a model that refuses writes (3.15).

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_payroll/models/payroll_cycle_run.py`, lines 147 to 152 at ad98dac9):

```python
# States from Step 8b onward — Credit Instructions is the point of no return.
# Cancel is disabled from these states.
POINT_OF_NO_RETURN_STATES = frozenset({"instructions_generated", "lbp_uploaded", "done"})

# Terminal states: run is closed, no further action allowed.
TERMINAL_STATES = frozenset({"rejected", "cancelled", "done"})
```

### Card 14. `dswd_4ps_catchup_payroll`: paying households a regular cycle left out

**Purpose.** Pays households that a regular cycle could not pay (for example, no bank account at DV time), in separate
catch-up cycles under one catch-up program.

| 4Ps process                        | Instance | Depends on (dswd and spp only)                                                              | Used by         | Size                                 |
| ---------------------------------- | -------- | ------------------------------------------------------------------------------------------- | --------------- | ------------------------------------ |
| Paying the cash grants (section 3) | 1        | `spp_programs`, `spp_approval`, `dswd_4ps_roles`, `dswd_4ps_compliance`, `dswd_4ps_payroll` | about 3 modules | about 12,000 Python lines, 587 tests |

**Key models**

- `dswd.4ps.catchup.source.record` (new table): the ledger of households left out of a regular cycle, with the reason.
  `dswd_4ps_payroll` writes it, but only when this module is installed.
- `dswd.4ps.catchup.transaction` (new table): one row per household, catch-up cycle and payroll type.
- `dswd.4ps.catchup.cycle.run` (new table): the catch-up pipeline, seven steps from `draft` to
  `transaction_status_updated`, plus `cancelled`.
- `spp.program`, `spp.cycle` (extends): the single catch-up program and its cycles.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ states       |            |                   | ■ 7          |                        | ■ 587           | ■ locks  | ■ cron    | ■ PDF        |                  | ■ 13            |

**Important points**

1. Its own state machine, not the regular one. `models/catchup_cycle_run.py` has no snapshot step, and its
   `POINT_OF_NO_RETURN_STATES` starts at `credit_instructions_generated` and includes `cancelled`. At most two active
   runs per program (`MAX_ACTIVE_RUNS_PER_PROGRAM`); a run waiting for Land Bank results does not count.
2. Row locks. `_lock_run_for_advance` runs `SELECT ... FOR UPDATE` on the run before a step changes its state, so a
   double click gets a clean error instead of a unique-constraint crash. Do not replace it with an ORM read.
3. Program locks. Verify and Import set `is_locked` on the program (`models/spp_program.py`). The cron "4Ps Catch-up:
   Release Stale Locks" (every 30 minutes) frees locks left by a failed job.
4. Two modules share the ledger. The regular DV step (`dswd_4ps_payroll/models/disbursement_voucher.py`) writes source
   records only if `env.registry.get("dswd.4ps.catchup.source.record")` finds the model. A unique key on household,
   source cycle and reason makes a replay harmless. A ledger change touches both modules.

**A ticket usually lands in**

- `models/catchup_eligibility.py`: "A household left out in May is not in the catch-up import."
- `models/catchup_cycle_run.py`: "The system will not let us create a third catch-up cycle."
- `models/spp_program.py`: "The catch-up program says it is locked."

**Code moment.** `models/catchup_cycle_run.py`: `STATE_SELECTION` and `POINT_OF_NO_RETURN_STATES` at the top, next to
the regular run's. The same pattern in a second module, with different states (3.8).

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_catchup_payroll/models/catchup_cycle_run.py`, lines 73 to 84 at ad98dac9):

```python
# Past the point of no return for Cancel / Reject + Rewind (spec §5.4 / §5.5).
POINT_OF_NO_RETURN_STATES = frozenset(
    {
        "credit_instructions_generated",
        "lbp_result_files_uploaded",
        "transaction_status_updated",
        "cancelled",
    }
)

# Terminal states (no further action).
TERMINAL_STATES = frozenset({"transaction_status_updated", "cancelled"})
```

### Card 15. `dswd_4ps_retro_payroll`: correcting past payments

**Purpose.** Recovers overpayments through the regular cycle and pays underpayments in a retro cycle that reuses the
regular payroll run.

| 4Ps process                        | Instance | Depends on (dswd and spp only)                                                                                                                                              | Used by         | Size                                   |
| ---------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------- |
| Paying the cash grants (section 3) | 1        | `spp_programs`, `spp_approval`, `spp_hide_menus_base`, `dswd_4ps_roles`, `dswd_4ps_compliance`, `dswd_4ps_period`, `dswd_4ps_payroll`, `dswd_4ps_registry`, `dswd_4ps_area` | about 7 modules | about 21,000 Python lines, 1,522 tests |

**Key models**

- `dswd.4ps.retro.overpayment` and `dswd.4ps.retro.overpayment.line` (new tables): a per-household balance and its
  recovery lines from regular cycles.
- `dswd.4ps.retro.underpayment` (new table): a retro payment request. The amount is computed once, then validated and
  approved.
- `dswd.4ps.payroll.cycle.run` (extends): a retro run is a regular run with retro files added.
- `dswd.4ps.retro.entitlement.manager` (new table): takes each household's amount from the approved requests.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17  | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | ---------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ extends      |            |                   | ■ 9          | ■ rules                | ■ 1,522         | ■ locks  | ■ channels | ■ PDF        |                  | ■ 21            |

**Important points**

1. The retro run is the regular run. `models/payroll_cycle_run.py` here has `_inherit = "dswd.4ps.payroll.cycle.run"`. A
   change to the regular pipeline changes retro too, so run the retro tests after any payroll change.
2. Ledgers cannot be edited. `write()` in `models/overpayment.py` refuses the `_FROZEN_AFTER_CREATE` fields (partner,
   amount, source and others); only `status` may change. A correction is a cancel and a new import.
3. Recovery follows the payroll point of no return. The regular cycle proposes a deduction through a hook in
   `dswd_4ps_payroll/models/cv_entitlement_manager.py` that runs only if the retro model exists. The balance drops only
   when the run passes Credit Instructions; a reject, rewind or cancel reverses the proposal.
4. Locks and jobs. Bulk Validate fans out on the `retro_validate` channel, serialised by `pg_advisory_xact_lock`
   (`models/underpayment.py`). Program Based Adjustment runs on `retro_bulk_diff`. An hourly cron finishes abandoned
   Validate batches.

**A ticket usually lands in**

- `models/underpayment.py`: "Bulk validate of the retro requests stopped halfway."
- `models/overpayment.py`: "We cannot correct the amount on an overpayment."
- `models/retro_entitlement_manager.py`: "The retro cycle pays a different amount from the approved request."

**Code moment.** `models/overpayment.py`: the module docstring (two-phase recovery, tied to the payroll point of no
return), then `_FROZEN_AFTER_CREATE` and `write()` (line 383). A model that decides which fields its ACL write bit
covers (3.11, 3.15).

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_retro_payroll/models/overpayment.py`, lines 10 to 19 at ad98dac9):

```python
Recovery is two-phase so it survives the payroll cycle's reject-and-rewind:

    _compute_proposed_recovery(partner, run, gross)   # PROPOSED line(s)
        → cycle reaches its point of no return (Step 8b)
    _commit_recovery_for_run(run)                     # PROPOSED → APPLIED
        → balance drops only now
    _reverse_recovery_for_run(run)                    # on reject/rewind/cancel
        → PROPOSED/APPLIED → REVERSED, balance restored
    _reverse_recovery_for_run(run, partner_ids)       # retro done, credit rejected (#2914)
        → those households' lines only
```

## Part 6: Casework

### Card 16. `dswd_4ps_swdi`: the yearly well-being assessment

**Purpose.** Receives SWDI and FRVA assessments from the mobile app, scores them, and runs review, return, approval and
archiving, with household assignment to C/MLs.

| 4Ps process                            | Instance | Depends on (dswd and spp only)                                                                                    | Used by          | Size                                   |
| -------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- |
| SWDI well-being assessment (section 5) | 2        | `spp_scoring`, `spp_approval`, `spp_area`, `spp_registry`, `dswd_4ps_area`, `dswd_4ps_registry`, `dswd_4ps_roles` | about 11 modules | about 16,000 Python lines, 1,125 tests |

**Key models**

- `dswd.swdi.assessment` (new table): one assessment per household per period. States: `not_assessed`, `draft`,
  `submitted`, `returned`, `approved`, `locked`, `archived`. Holds `lowb_level`. Uses `spp.approval.mixin`.
- `dswd.swdi.frva` (new table): the Family Risk and Vulnerability Assessment, reviewed on its own.
- `dswd.swdi.assignment` (new table): which C/ML assesses which household.
- `dswd.swdi.return.flag` (new table): a field the reviewer returned for correction. The mobile app locks every field
  without a flag.
- `res.partner` (extends): `swdi_assessment_ids`, `swdi_assignment_ids`, `swdi_needs_assignment`, `swdi_in_programme`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ approval     | ■ computed |                   | ■ 8          | ■ rules                | ■ 1,125         |          | ■ cron    | ■ PDF        |                  | ■ 30            |

**Important points**

1. The level comes from the total score only. `_classify_lowb` in `models/assessment.py` uses `LOWB_LEVEL_3_MIN_SCORE`
   (2.83) and `LOWB_LEVEL_2_MIN_SCORE` (1.83) from `constants/states.py`. Economic sufficiency and social adequacy are
   reported, not used as gates. The same numbers are in `data/scoring_model_swdi.xml` (`noupdate`) and in the mobile
   app; change all three together.
2. Move an assessment through its actions, never by writing `state`. `action_approve` finishes the scoring before it
   writes the state. Bulk approve calls `action_approve` row by row, so audit notes and CMS triggers still fire.
3. Two-person archiving. One person requests, another approves. `models/archive_log.py` holds the proof: its author and
   step fields cannot be edited, and rows cannot be deleted except as superuser.
4. Security. Five SWDI groups (`security/groups.xml`) are linked into the `dswd_4ps_roles` groups. The 11 record rules
   in `security/ir_rule.xml` are `noupdate`, so a rule change needs a migration.
5. `__manifest__.py` excludes `dswd_4ps_bridge_server`: this module never runs on the registry instance of a split
   install.

**A ticket usually lands in**

- `models/assessment.py`: "A household with a score of 2.85 shows Level 2."
- `models/return_flag.py`: "The mobile app lets the C/ML change fields the reviewer did not return."
- `models/assignment.py`: "A household is missing from the C/ML's assignment list."

**Code moment.** `models/assessment.py`: `_classify_lowb` (line 1226) and the two constants in `constants/states.py`
(lines 252 and 253). The well-being level from Module 4, as production computes it (3.8 computed fields).

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_swdi/models/assessment.py`, lines 1230 to 1241 at ad98dac9):

```python
        classification is total-score-range-only; the earlier ES/SA dimensional
        gates were dropped. ES and SA are retained as reported sub-scores, not
        as gates. Mirrors the mobile engine (swdi-mobile #280/#281):
        - Level 3: score >= 2.83
        - Level 2: score >= 1.83
        - Level 1: otherwise
        """
        if score >= LOWB_LEVEL_3_MIN_SCORE:
            return "3"
        if score >= LOWB_LEVEL_2_MIN_SCORE:
            return "2"
        return "1"
```

### Card 17. `dswd_4ps_cms`: Kilos-Unlad case management

**Purpose.** Runs 4Ps case management on the upstream `spp.case`: case study reports, intervention plans, Purple Tag,
transition and exit, each with its own approval chain.

| 4Ps process                             | Instance | Depends on (dswd and spp only)                                                                                                                                                                                            | Used by          | Size                                   |
| --------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- |
| Kilos-Unlad case management (section 6) | 2        | `spp_case_base`, `spp_case_programs`, `spp_case_entitlements`, `spp_approval`, `spp_audit`, `spp_area`, `spp_registry`, `dswd_4ps_registry`, `dswd_4ps_roles`, `dswd_4ps_area`, `dswd_4ps_swdi`, `dswd_4ps_bridge_shared` | about 10 modules | about 20,000 Python lines, 1,913 tests |

**Key models**

- `spp.case` (extends): `case_source` (ten values in `constants.py`, such as `swdi_l1`, `frva_high`, `manual`,
  `auto_attrition`), `exit_type`, `case_status`, `swdi_assessment_id`, `purple_tag_id`.
- `dswd.cms.scsr` (new table): the Social Case Study Report and its approval chain.
- `dswd.cms.case.summary` (new table): the exit report, approved by the Provincial Link.
- `dswd.cms.purple.tag` (new table): the Purple Tag recommendation and its expiry.
- `dswd.cms.household.transition.plan` (new table): the transition plan for a graduating household.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17  | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | ---------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ extends      |            | ■ inherited       | ■ 6          | ■ 117 rules            | ■ 1,913         | ■ sudo   | ■ 25 crons | ■ PDF        | ■ 15             | ■ 38            |

**Important points**

1. Record rules. `security/ir_rule.xml` holds 117 rules for the six CMS groups (user, worker, reviewer, authorizer,
   director, manager). A rule scopes on the household's area `child_of` the user's center areas, so the level follows
   the user's area. The file is `noupdate`: a rule change needs a migration.
2. Do not split the archive filter into its own rule. Rules for one group combine with OR, so the "hide executed
   archives" condition is joined into each area rule with AND. The comment at the top of the file explains why.
3. A state cannot be written directly. `models/state_tier_gate_mixin.py` checks every `state` write against
   `_state_tier_map`, so an RPC write cannot skip a supervisor's action. `models/scsr.py` has its own copy of the guard:
   a change must be made in both places.
4. Twenty-five crons, all daily or weekly. Two auto-approve SCSRs and Case Summaries after 30 days
   (`data/cron_auto_approval.xml`); they call `sudo()` themselves because the cron user is not reliable on a `noupdate`
   record. Others detect natural attrition and seven-year residency and create exit cases.

**A ticket usually lands in**

- `security/ir_rule.xml`: "A Provincial Link cannot see a case in their province."
- `models/scsr.py` and `data/cron_auto_approval.xml`: "An SCSR was approved although nobody approved it."
- `models/spp_case.py`: "A natural-attrition case was created for a household that still has a child in school."

**Code moment.** `security/ir_rule.xml`: the comment block, then `rule_cms_case_director` (line 48). A record rule at
production scale, a direct follow-up to section 3.12.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_cms/security/ir_rule.xml`, lines 48 to 59 at ad98dac9):

```xml
    <record id="rule_cms_case_director" model="ir.rule">
        <field name="name">CMS Case: Director (regional scope)</field>
        <field name="model_id" ref="spp_case_base.model_spp_case"/>
        <field name="groups" eval="[Command.link(ref('group_cms_director'))]"/>
        <field name="perm_unlink" eval="True"/>
        <field name="domain_force">[
            '&amp;',
            '|',
            ('archive_request_status', '!=', 'executed'),
            ('archived_by_id', '=', user.id),
            ('partner_id.area_id', 'child_of', user.center_area_ids.ids),
        ]</field>
```

### Card 18. `dswd_4ps_swdi_cms`: assessment results become cases

**Purpose.** When an SWDI or FRVA assessment is approved, or a household is tagged Not Assessed, creates the CMS case in
a queued job, with retries and a dead-letter state.

| 4Ps process                                   | Instance | Depends on (dswd and spp only)                                        | Used by         | Size                                |
| --------------------------------------------- | -------- | --------------------------------------------------------------------- | --------------- | ----------------------------------- |
| SWDI results into case management (section 5) | 2        | `dswd_4ps_swdi`, `dswd_4ps_registry`, `dswd_4ps_cms`, `spp_case_base` | about 4 modules | about 2,000 Python lines, 144 tests |

**Key models**

- `dswd.swdi.cms.trigger.config` (new table): one row per trigger: case type, priority, intensity, `max_retries`,
  `is_active`. Seven rows in `data/trigger_config_data.xml` (`noupdate`).
- `dswd.swdi.cms.event` (new table): one dispatch per trigger and source record. States: `pending`, `processing`,
  `done`, `failed` (the dead letter), `deferred`.
- `dswd.swdi.assessment` (extends): `action_approve` and `action_mark_not_assessed` call the dispatcher.
- `dswd.swdi.frva` (extends): high overall, child-protection and safety risk call the dispatcher.
- `spp.case` (extends): `response_due_at`, `is_response_overdue`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ auto       | ■ extends      |            |                   |              | ■ rules                | ■ 144           | ■ sudo   | ■ retries |              |                  | ■ 4             |

**Important points**

1. Approval does not wait for the case. `_create_and_dispatch` in `models/cms_event.py` creates the event inside the
   approval and queues `_dispatch_cms_case`; the case is created in the job. If the trigger config is inactive, no event
   is created and only a warning goes to the log.
2. The module owns the retries. Jobs are queued with `max_retries=0`. On failure, `_handle_dispatch_failure` retries
   after 5 minutes, 15 minutes and 1 hour (`BACKOFF_SCHEDULE` in `constants.py`), then sets `failed`. Do not add
   job-engine retries on top.
3. Duplicates are blocked twice. A partial unique index on trigger, source model and source record stops a second event;
   a per-household advisory lock (`CMS_LOCK_NS`) serialises dispatch. A busy lock re-queues the job after 5 seconds.
4. A Level 3 graduation is `deferred` when the household has a blocking client status. The cron "CMS Events: Re-check
   Deferred Level-3 Graduations" re-fires it. Another daily cron alerts when failed events pile up.
5. `auto_install` is `True`: the module installs itself once SWDI and CMS are both installed.

**A ticket usually lands in**

- `models/cms_event.py`: "A Level 1 assessment was approved but no case was created."
- `data/trigger_config_data.xml`: "FRVA high-risk households should get urgent cases, not high."
- `models/assessment.py`: "A Level 3 household was not sent to graduation."

**Code moment.** `models/cms_trigger_config.py`, then the seven records in `data/trigger_config_data.xml`. A trigger is
a data record, so switching one off or changing its priority is configuration, not code (4.4 data, 3.7 models).

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_swdi_cms/models/cms_trigger_config.py`, lines 41 to 50 at ad98dac9):

```python
    trigger_type = fields.Char(
        string="Trigger Type",
        required=True,
        help=("One of: PRIORITY_CASE, GRADUATION, FRVA_HIGH_RISK, CHILD_PROTECTION, MISBEHAVIOR, WAIVE_EXIT."),
    )

    is_active = fields.Boolean(
        string="Active",
        default=True,
    )
```

### Card 19. The bridge family: `dswd_4ps_bridge_shared`, `dswd_4ps_bridge_server`, `dswd_4ps_bridge_client`

**Purpose.** Lets casework run on its own instance: the CMS instance looks up and imports households from the registry
instance, and sends case events back.

| 4Ps process                                              | Instance                                        | Depends on (dswd and spp only)                                                                                                                                                                                  | Used by            | Size                                |
| -------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------------------------- |
| Splitting the registry and casework across two instances | both (shared on both, server on 1, client on 2) | shared: none; server: `dswd_4ps_api`, `dswd_4ps_registry`, `dswd_4ps_bridge_shared`, `dswd_4ps_compliance`; client: `dswd_4ps_cms`, `dswd_4ps_swdi_cms`, `dswd_4ps_bridge_shared`, `dswd_4ps_auth`, `spp_audit` | 5, 2 and 1 modules | about 5,000 Python lines, 296 tests |

**Key models**

- `dswd_4ps_bridge_shared` (no models): Pydantic schemas for households, case events and lookups, constants such as
  `PERMANENT_EXIT_CODES`, and error codes.
- `res.partner` (extends, server): `registry_uuid`, the key that links one household across the two instances.
- `dswd.4ps.bridge.sync.log` (new table, server and client): an audit log of bridge requests.
- `res.partner` (extends, client): `is_imported_from_registry`, `registry_uuid`, and a write and delete guard.
- `spp.case` (extends, client): looks up and imports the household when a case is created, and queues case events.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15  | Jobs 3.17  | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | --------- | ---------- | ------------ | ---------------- | --------------- |
| ■ excludes   | ■ extends      |            |                   | ■ 2          | ■ hook                 | ■ 296           | ■ context | ■ pushback |              |                  |                 |

**Important points**

1. The installed modules choose the mode. `dswd_4ps_bridge_client` and `dswd_4ps_bridge_server` exclude each other in
   their manifests. Payroll, change requests, compliance and the other registry-side modules exclude the client; SWDI,
   CMS and the other casework modules exclude the server. `dswd_4ps_starter` installs everything on one instance with
   neither bridge module.
2. The registry instance owns household data. On the CMS instance, `_4ps_write_hook` in
   `dswd_4ps_bridge_client/models/res_partner.py` refuses writes to imported partners except SWDI and CMS fields, and
   `unlink` refuses deletes. Only the bridge itself bypasses this, with `bridge_internal_write` in the context.
3. Lookups are synchronous; events are queued. A lookup at case creation waits at most 5 seconds
   (`DEFAULT_LOOKUP_TIMEOUT_SECONDS`) and fails with a timeout error. `case_created`, `case_closed` and `swdi_level_set`
   go back through `with_delay` jobs (`services/pushback.py`).
4. Configuration after install. The client needs `registry_base_url`, `client_id` and `client_secret` in system
   parameters. The server's `post_init_hook` adds `group_bridge_service` to the API service role. Two daily crons on the
   client refresh households with open cases and sync the registry user list.

**A ticket usually lands in**

- `dswd_4ps_bridge_client/services/bridge_client.py`: "Creating a case says the registry timed out."
- `dswd_4ps_bridge_client/models/res_partner.py`: "On the CMS instance I cannot correct a member's birthdate."
- `dswd_4ps_bridge_server/services/case_event.py`: "The case was closed in CMS but the registry still shows it open."

**Code moment.** `dswd_4ps_bridge_client/__manifest__.py`: `excludes` and `depends`, then the same two keys in
`dswd_4ps_bridge_server/__manifest__.py`. How the manifest (section 3.6) decides which instance a module can live on.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_bridge_client/__manifest__.py`, lines 37 to 45 at ad98dac9):

```python
    "excludes": ["dswd_4ps_bridge_server"],
    "depends": [
        "dswd_4ps_cms",
        "dswd_4ps_swdi_cms",
        "dswd_4ps_bridge_shared",
        # The cross-instance user sync writes oauth_uid / oauth_provider_id and
        # overrides the _post_oauth_login hook — both from dswd_4ps_auth (the CMS
        # split instance authenticates against Keycloak via this module).
        "dswd_4ps_auth",
```

## Part 7: Integration

### Card 20. `dswd_4ps_api`: the 4Ps API on the OpenSPP API application

**Purpose.** Serves 4Ps household, member, reference, area and document endpoints to the mobile app and the beneficiary
portal, and decides who the caller is and what it may read.

| 4Ps process                                                                      | Instance | Depends on (dswd and spp only)                                                                     | Used by          | Size                                |
| -------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| Connecting the mobile app and the beneficiary portal to the registry (section 8) | both     | `spp_api_v2`, `spp_oauth`, `dswd_4ps_registry`, `dswd_4ps_area`, `dswd_4ps_auth`, `dswd_4ps_roles` | about 16 modules | about 9,900 Python lines, 556 tests |

**Key models**

- `spp.api.client` (extends): adds the Keycloak auth type, `keycloak_client_identifier` (the token's `azp`) and
  `scope_grant_log`.
- `spp.api.client.scope` (extends): adds 4Ps scope resources (`area`, `cv`, `dms`, `fds`, `facility`, `hazard`,
  `reference`, and others) and the `write` action.
- `fastapi.endpoint` (extends): `_get_fastapi_routers()` adds eleven 4Ps routers to the `api_v2` application.
- `spp.beneficiary.device_key` (new table): a beneficiary device's public key, used to verify signed change requests.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      |            |                   |              | ■ RBAC                 | ■ 556           | ■ env    |           |              |                  | ■ 11            |

**Important points**

1. `middleware/rs256_auth.py` reads the token's `alg` header first. HS256 tokens are machine clients checked by upstream
   `spp_api_v2`. RS256 tokens come from Keycloak and are checked against its JWKS keys. If the `azp` claim matches an
   API client, the caller is that client. If not, the caller is the matching Odoo user.
2. `dependencies.py` `authenticated_env` runs every request as the caller: as the Keycloak user, or as the
   `4Ps API Service` user for client tokens. Record rules and ACLs therefore apply to API traffic. Routers and services
   do not call `sudo()` (ADR-0004). The `dswd_4ps_api.enforce_rbac` system parameter must stay `True`. When it is
   `False`, the code runs the request as superuser.
3. Scopes are checked in the router (`has_scope("group", "read")`). The `cssp-bff` portal client is seeded here
   (`data/api_client_cssp_bff.xml`). Each module grants its own scopes to it from a `post_init_hook`, which runs once,
   at install. A scope added later needs a migration or the "Re-grant Missing Scopes" button.
4. Records are found by identifiers, not database ids: `{system}|{value}` looked up in `spp.registry.id`
   (`services/household_service.py`), or the Listahanan ID.
5. The mobile app depends on every path and field alias. The module's maintainer notes say: read the repository's
   `docs/api-contract.md` before changing a router, schema or service, and update the mobile repository's copy at the
   same time.

**A ticket usually lands in**

- `middleware/rs256_auth.py`: "The app gets 401 Authentication failed after the Keycloak change."
- `routers/household.py` and `services/household_service.py`: "The app shows a household as not found, but it is in the
  registry."
- `data/service_user_role.xml`: "Since the last release one endpoint returns 403 for the mobile client" (the API service
  user lacks a group).

**Code moment.** `routers/household.py`: open `read_grantee_history`. Point at `Depends(authenticated_env)` (the request
runs as the caller, so the record rules from Module 3 apply), `_check_read_access` (the scope check), `parse_identifier`
(an identifier, never a database id), and the call into the service layer.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_api/routers/household.py`, lines 96 to 107 at ad98dac9):

```python
async def read_grantee_history(
    identifier: Annotated[str, Path(description="Format: {system}|{value}")],
    env: Annotated[Environment, Depends(authenticated_env)],
    auth: Annotated[dict, Depends(get_auth_with_rate_limit)],
):
    """Grantee change audit trail."""
    _check_read_access(auth)

    system, value = parse_identifier(identifier)
    service = HouseholdService(env)
    household = service.find_by_identifier(system, value)
```

### Card 21. The split API modules: domain endpoints on the same application

**Purpose.** Each module adds one domain's endpoints to the same `api_v2` application, so an instance installs only the
endpoints for the data it holds (ADR-0009).

Members: `dswd_4ps_api_change_request` (about 6,000 lines, 269 tests), `dswd_4ps_api_compliance` (about 2,900 lines, 301
tests), `dswd_4ps_api_fds` (about 1,000 lines, 81 tests), `dswd_4ps_api_field_limit` (about 910 lines, 63 tests),
`dswd_4ps_retro_api` (about 390 lines, 31 tests), `dswd_4ps_swdi_api` (about 5,900 lines, 369 tests).

| 4Ps process                                                                                                             | Instance | Depends on (dswd and spp only)                                                                                                                                                                                                                      | Used by             | Size                                   |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------------------------- |
| Change requests, compliance verification (section 4), FDS, field limits, retro status for NEWGRS (section 7), SWDI sync | both     | `dswd_4ps_api` plus the domain module: `dswd_4ps_change_request`, `spp_api_v2_change_request`, `dswd_4ps_supporting_docs_data`, `dswd_4ps_compliance`, `dswd_4ps_fds_operations`, `dswd_4ps_field_limit`, `dswd_4ps_retro_payroll`, `dswd_4ps_swdi` | 2 or 3 modules each | about 17,000 Python lines, 1,114 tests |

**Key models**

- `fastapi.endpoint` (extends, in every member): `_get_fastapi_routers()` appends the module's routers when
  `self.app == "api_v2"`.
- `spp.api.client.scope` (extends, in `retro_api` and `swdi_api`): adds the `retro` and `swdi` scope resources.
- `dswd.cv.submission.proof` (new table, `api_compliance`): proof records for compliance forms sent from the app.
- `dswd.swdi.sync.rejection` (new table, `swdi_api`): SWDI assessments the mobile sync refused, and why.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ auto       | ■ extends      |            |                   |              | ■ scopes               | ■ 1,114         |          |           |              |                  | ■ 9             |

**Important points**

1. Paths do not change when routes move between modules. `dswd_4ps_api_fds` says so in
   `models/fastapi_endpoint_registry.py`: the FDS routers moved out of `dswd_4ps_api` and kept their paths.
2. Five members set `auto_install: True` (change request, compliance, FDS, field limit, SWDI). They install by
   themselves once `dswd_4ps_api` and their domain module are present. `retro_api` does not auto-install; the bundles
   list it.
3. A grant forgotten in a split module shows up as a 403 or an `AccessError`, not as an install error. Check the
   module's `data/service_user_role.xml` and its `hooks.py` scope list.
4. Every router still imports `authenticated_env` and the rate-limit dependency from `dswd_4ps_api`. The rules on the
   `dswd_4ps_api` card apply here too.

**A ticket usually lands in**

- `dswd_4ps_api_change_request/routers/changes_submission.py`: "Updates sent from the app never become change requests."
- `dswd_4ps_api_compliance/routers/cv_router.py`: "A school attendance form sent from the app was refused."
- `dswd_4ps_swdi_api/services/submission_service.py`: "An SWDI assessment synced from the tablet was rejected."

**Code moment.** `dswd_4ps_api_fds/models/fastapi_endpoint_registry.py`: the whole file is twelve lines of method.
`_inherit = "fastapi.endpoint"`, `super()`, then one `routers.append`. This is Module 3's `_inherit` and `super()`
pattern used to add API routes, and it is the same in every split module.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_api_fds/models/fastapi_endpoint_registry.py`, lines 25 to 36 at ad98dac9):

```python
    def _get_fastapi_routers(self) -> list[APIRouter]:
        """Add the FDS API routers to the API V2 app."""
        routers = super()._get_fastapi_routers()

        if self.app == "api_v2":
            # Import here to avoid circular imports at module load.
            from ..routers.fds import fds_router

            routers.append(fds_router)
            _logger.debug("Added FDS API routers to API V2")

        return routers
```

### Card 22. The portal APIs: what the beneficiary portal reads

**Purpose.** Serves the CSSP beneficiary portal, through its backend client `cssp-bff`. A household reads its own FDS,
compliance, payroll, SWDI and case data, and uploads compliance and FDS evidence.

Members: `dswd_4ps_portal_api_base` (about 300 lines, 12 tests), `dswd_4ps_portal_api` (about 2,300 lines, 109 tests),
`dswd_4ps_portal_api_casework` (about 1,400 lines, 46 tests), `dswd_4ps_payroll_api` (about 1,700 lines, 108 tests).

| 4Ps process                                                                                         | Instance | Depends on (dswd and spp only)                                                                                                                                            | Used by             | Size                                |
| --------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ----------------------------------- |
| Beneficiary self-service: grants (section 3), compliance (section 4), FDS, SWDI and case management | both     | `dswd_4ps_api`, `dswd_4ps_portal_api_base`, `dswd_4ps_fds_operations`, `dswd_4ps_swdi`, `dswd_4ps_swdi_api`, `dswd_4ps_cms`, `dswd_4ps_payroll`, `dswd_4ps_retro_payroll` | 2 to 4 modules each | about 5,700 Python lines, 275 tests |

**Key models**

- `spp.api.client.scope` (extends, `portal_api_base`): adds the `portal` and `cms` resources and the `cases_read`
  action.
- `spp.api.client.scope` (extends, `payroll_api`): adds the `payroll` resource.
- `fastapi.endpoint` (extends): adds the `/portal` routers (`portal_api`, `portal_api_casework`) and the `/payroll`
  router (`payroll_api`).
- `spp.payment` (read, from `dswd_4ps_payroll`): the payroll router reads payments and the snapshot row each one points
  at.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      |            |                   |              | ■ header               | ■ 275           |          |           |              |                  |                 |

**Important points**

1. Two checks on every call (`dswd_4ps_portal_api_base/portal_auth.py`). The client needs the scope. The
   `Authorization-Beneficiary` header must equal the Listahanan ID in the path. A missing header is refused unless
   `dswd_4ps_portal_api.require_beneficiary_header` is the literal `false`.
2. The split follows the two instances. `portal_api` (FDS, compliance) runs on instance 1. `portal_api_casework` (SWDI,
   FRVA, CMS) runs on instance 2. `payroll_api` does not depend on the portal base, so it has its own copy of the header
   check. Tests in both modules keep the two copies the same.
3. "No data" is not an error. Empty sections return HTTP 200 with null or empty values. 404 means the household was not
   found. `payroll_api` also returns `payrollAvailable=false` when the caller may not read payroll, so the portal can
   tell "never paid" from "not allowed to see".
4. `payroll_api/services/payroll_service.py` reads `spp.payment`, not the snapshot alone. A snapshot row exists for
   every household in the run, paid or not. Catch-up payouts come from a second ledger, `dswd.4ps.catchup.transaction`.
   The last grant counts only payments the bank confirmed (`delivery_status` `success`).
5. One path carries a record number: `/payroll/Household/{listahanan_id}/payout/{snapshot_id}` takes the reference that
   the payout history returned. It is checked against the household and answers 404 for any other household.

**A ticket usually lands in**

- `dswd_4ps_payroll_api/services/payroll_service.py`: "The portal shows no payroll for a household that was paid."
- `dswd_4ps_portal_api_base/portal_auth.py`: "Every portal page returns 403 since the portal update."
- `dswd_4ps_portal_api/routers/portal_router.py`: "A beneficiary cannot upload a school certificate in the portal."

**Code moment.** `dswd_4ps_portal_api_casework/routers/portal_casework_router.py`: `read_swdi_history`. Four lines show
the whole portal pattern: scope check, beneficiary header check, household by Listahanan ID, then the service. The same
four lines open every portal and payroll endpoint.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_portal_api_casework/routers/portal_casework_router.py`, lines 79 to 86 at ad98dac9):

```python
    env: Annotated[Environment, Depends(authenticated_env)],
    auth: Annotated[dict, Depends(get_auth_with_rate_limit)],
    authorization_beneficiary: Annotated[str | None, Header(alias="Authorization-Beneficiary")] = None,
) -> dict:
    _check_swdi_read_scope(auth)
    _check_beneficiary_identity(listahanan_id, authorization_beneficiary, auth)
    household = _resolve_household(env, listahanan_id)
    return {"swdiHistory": portal_service.get_swdi_history(env, household)}
```

### Card 23. `dswd_4ps_integration`: outbound events the portal polls

**Purpose.** Keeps a log of notices for the beneficiary portal (CSSP), such as retro payment status and case updates.
The portal polls the log and confirms what it received.

| 4Ps process               | Instance | Depends on (dswd and spp only)                        | Used by         | Size                             |
| ------------------------- | -------- | ----------------------------------------------------- | --------------- | -------------------------------- |
| Beneficiary notifications | 1        | `dswd_4ps_api`, `dswd_4ps_registry`, `dswd_4ps_roles` | about 2 modules | about 990 Python lines, 21 tests |

**Key models**

- `dswd.outbound.event` (new table): one notice per occurrence and destination. It holds `event_code`, the household's
  Listahanan ID, the grantee's 4Ps member ID, a small `payload`, `status` (queued, sent, failed, dead letter, cancelled)
  and a poll cursor.
- `spp.api.client.scope` (extends): adds the `cssp` resource (`events_read`, `events_ack`).
- `fastapi.endpoint` (extends): adds `GET /cssp/events` and `POST /cssp/events/ack`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ new          |            |                   |              | ■ group                |                 | ■ SQL    | ■ cron    |              |                  |                 |

**Important points**

1. Producers call `emit()` on `dswd.outbound.event`. Today they are `dswd_4ps_retro_payroll` (underpayment status) and
   `dswd_4ps_cms` (notification types marked for CSSP). Both check `"dswd.outbound.event" in self.env` first, so they
   work without this module.
2. `emit()` is idempotent. The event id is a UUID made from the event code, destination and a dedup key, so a repeated
   trigger reuses the row. A unique constraint on `(event_id, destination)` covers the race.
3. Only identifiers go on the wire. `_assert_no_forbidden_keys` refuses forbidden payload keys, and
   `internal_only_hints` is never serialised. Keep notices small: no scores, codes or notes.
4. A poll does not mark a row sent; only an ack does. Two crons escalate rows served but not acknowledged (every 6
   hours) and alert on dead letters (daily). The cursor comes from its own PostgreSQL sequence, created in `_auto_init`.

**A ticket usually lands in**

- `models/outbound_event.py`: "The portal never showed the notice that a retro payment was released."
- `routers/events_router.py` and `services/cursor_service.py`: "The portal keeps receiving the same notices."
- `hooks.py`: "Every portal poll returns 403" (`cssp-bff` lacks the `cssp` scope).

**Code moment.** `models/outbound_event.py`: the `emit()` method. Point at the deterministic `event_id` and the search
before create (idempotency), and the forbidden-key check before anything is written.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_integration/models/outbound_event.py`, lines 213 to 224 at ad98dac9):

```python
        event_id = str(uuid.uuid5(EVENT_ID_NAMESPACE, f"{event_code}|{destination}|{dedup_key}"))
        existing = self.search([("event_id", "=", event_id), ("destination", "=", destination)], limit=1)
        if existing:
            _logger.debug("Outbound emit idempotency hit: id=%s reused for %s", existing.id, event_code)
            return existing

        self._assert_no_forbidden_keys(payload)
        vals = {
            "event_id": event_id,
            "event_code": event_code,
            "destination": destination,
            "subject_household_id": subject_household_id or False,
```

### Card 24. `dswd_4ps_newgrs`: grievance status in, profile updates out

**Purpose.** Connects the registry to NEWGRS, the grievance system. It receives grievance status pushes, tells NEWGRS
when an approved change request updates a household, and serves the household profile to NEWGRS.

| 4Ps process                          | Instance | Depends on (dswd and spp only)                                                                               | Used by         | Size                                |
| ------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------ | --------------- | ----------------------------------- |
| Grievance Redress System (section 7) | 1        | `dswd_4ps_api`, `dswd_4ps_registry`, `dswd_4ps_area`, `dswd_4ps_change_request`, `spp_api_v2`, `spp_consent` | about 2 modules | about 2,100 Python lines, 170 tests |

**Key models**

- `dswd.4ps.grievance` (new table): the local copy of a NEWGRS grievance: `grievance_no`, `household_id`, `partner_id`,
  `current_status`, `status_reason`.
- `dswd.4ps.grievance.status.history` (new table): one row per status push.
- `spp.change.request` (extends): `_on_approve` queues the NEWGRS notification.
- `res.partner` (extends): adds `grievance_ids`.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ extends      |            | ■ inherited       |              | ■ rules                | ■ 170           |          | ■ queue   |              |                  |                 |

**Important points**

1. Three features, each off by default behind its own system parameter: `dswd_4ps_newgrs.enabled` (the status receiver
   returns 404 until it is `True`), `dswd_4ps_newgrs.notify_enabled` (the outbound notice) and
   `dswd_4ps_newgrs.profile_read_enabled` (the profile endpoint).
2. The outbound notice runs as a job on the `newgrs_notify` channel. Only the change request types in `NOTIFY_CR_CODES`
   (`constants.py`) trigger it. A job marked done does not mean NEWGRS received the notice: look for the note on the
   change request or the job result.
3. NEWGRS credentials come from the server configuration or environment, never from the database.
4. NEWGRS authenticates through the `dswd_4ps_api` middleware and needs `newgrs:write` (push) or `newgrs:read`
   (profile). `security/grievance_area_rules.xml` limits grievance records to the user's areas.

**A ticket usually lands in**

- `models/change_request.py`: "NEWGRS did not get the update after we approved a change of grantee."
- `routers/newgrs.py` and `services/grievance_service.py`: "Grievance statuses stopped updating in the system."
- `security/grievance_area_rules.xml`: "A regional officer cannot see grievances for her region."

**Code moment.** `models/change_request.py`: `_on_approve` calls `super()` first, then `_newgrs_dispatch_profile_update`
returns early when the flag is off or the type is out of scope, and ends in `with_delay(...)` with a channel and an
`identity_key`. This is Module 3's job worker: work handed to a queue, deduplicated, retried.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_newgrs/models/change_request.py`, lines 80 to 91 at ad98dac9):

```python
        updated_at_iso = iso_utc_z(self.approved_date)
        # identity_key dedupes a double-fire of the same approval while letting a
        # later re-approval (distinct approved_date) through. Engine retry — not an
        # app-level loop — provides the AC4 replay window; max_retries sizes that
        # window to ~22h (see NOTIFY_MAX_RETRIES) instead of the engine default's
        # ~5 minutes.
        self.with_delay(
            channel=NOTIFY_CHANNEL,
            identity_key=f"newgrs_profile_notify_{listahanan_id}_{updated_at_iso}",
            description=f"NEWGRS: notify HH profile update (CR {self.name})",
            max_retries=NOTIFY_MAX_RETRIES,
        )._newgrs_notify_profile_update(listahanan_id, updated_at_iso)
```

### Card 25. `dswd_4ps_ods`: read-only lookups in the old Pantawid ODS

**Purpose.** Shows a household's historical data from the Pantawid ODS API gateway (payroll, compliance, SWDI, cases,
grievances and more) in tabs on the household form. It only reads.

| 4Ps process                               | Instance | Depends on (dswd and spp only) | Used by         | Size                             |
| ----------------------------------------- | -------- | ------------------------------ | --------------- | -------------------------------- |
| Household history from the earlier system | 1        | `dswd_4ps_registry`            | about 2 modules | about 880 Python lines, 91 tests |

**Key models**

- `dswd_4ps_ods.api_client` (new, abstract model, no table): the HTTP client. It handles the token and has one
  `ods_fetch_*` method per ODS endpoint.
- `dswd_4ps_ods.data.cache` (new table): cached responses by Listahanan ID, endpoint and parameter hash, with
  `fetched_at`.
- `res.partner` (extends): adds no fields. It adds `ods_ui_fetch_*` methods that the OWL tabs call.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
|              | ■ abstract     |            | ■ OWL             |              | ■ admin                | ■ 91            |          | ■ cron    |              |                  |                 |

**Important points**

1. ODS is a client, not an API: nothing in this module adds a route. The OWL widgets in `static/src/js/` call
   `res.partner` methods, which call the client.
2. `res.partner._ods_safe_call` never raises to the screen. A failure returns `{"error": ..., "data": []}` with a plain
   message. When ODS is down the widget can ask for cached data only.
3. The cache table has one ACL row, for `base.group_system`. Other users reach it through `sudo()` in `_ods_cache()`. A
   daily cron deletes entries older than `dswd_4ps_ods.cache_ttl_days` (15 by default).
4. The gateway address, login and cached token are system parameters (`data/ir_config_parameter.xml` ships them empty).
   Set them per environment.

**A ticket usually lands in**

- `models/ods_api_client.py`: "The ODS tabs say ODS is not configured" or "ODS returned an error".
- `models/res_partner.py`: "The ODS tab shows last month's data" (the cache).
- `views/household_ods_tabs.xml`: "The ODS tabs do not appear on an individual's form" (they show for households only).

**Code moment.** `models/res_partner.py`: `_ods_safe_call`. Point at the cache check before the HTTP call and the
`except` branches that turn errors into messages. A model extended with no fields, only methods for the UI.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_ods/models/res_partner.py`, lines 71 to 78 at ad98dac9):

```python
        # Check cache (unless force-refreshing).
        if not force_refresh and endpoint:
            cached_data, fetched_at = cache_model._get_cached(lid, endpoint, params_hash)
            if cached_data is not None:
                return {
                    "data": cached_data,
                    "cached_at": (fetched_at.isoformat() + "+00:00") if fetched_at else "",
                }
```

### Card 26. `dswd_4ps_auth`: Keycloak single sign-on for staff

**Purpose.** Lets DSWD staff sign in to the web application through Keycloak (OpenID Connect). It creates or links the
user on first sign-in and copies the area claims from the token.

| 4Ps process                                   | Instance | Depends on (dswd and spp only) | Used by         | Size                                |
| --------------------------------------------- | -------- | ------------------------------ | --------------- | ----------------------------------- |
| Staff sign-in and area assignment (section 5) | both     | `dswd_4ps_area`                | about 2 modules | about 1,200 Python lines, 127 tests |

**Key models**

- `auth.oauth.provider` (extends): adds `flow`, `token_endpoint`, `jwks_uri`, `allow_signup`, `signup_default_groups`
  and `sync_user_groups`.
- `res.users` (extends): signs users in, links users created beforehand by login, and copies the `regions`, `provinces`,
  `cities` and `barangays` claims into `idp_regions` and the other area fields.
- `ir.http` (extends): removes technical error details from responses unless the user is in
  `group_technical_error_details`.
- `dswd.4ps.auth.openid.config.wizard` (new, wizard): fetches a provider's OpenID configuration.

**The Module 3/4 strip**

| Manifest 3.6 | Models 3.7/4.6 | Fields 3.8 | Views 3.9/4.7-4.8 | Wizards 3.10 | Security 3.11-3.12/4.9 | Tests 3.13/4.10 | ORM 3.15 | Jobs 3.17 | Reports 3.18 | Vocabularies 4.4 | Migrations 4.13 |
| ------------ | -------------- | ---------- | ----------------- | ------------ | ---------------------- | --------------- | -------- | --------- | ------------ | ---------------- | --------------- |
| ■ hook       | ■ extends      |            |                   | ■ OpenID     | ■ group                | ■ 127           |          |           |              |                  |                 |

**Important points**

1. `res.users._auth_oauth_signin` creates new users with `create()`, not Odoo's signup, because the portal template user
   conflicts with the role groups. A user created beforehand (by an administrator or the bridge) is linked by login on
   first sign-in, not duplicated.
2. Keycloak is the source of truth for a user's areas (ADR-0012). The claim map in `models/res_users.py` writes them to
   the user. `dswd_4ps_area` turns them into area access.
3. `data/security_defaults.xml` is not `noupdate`: the hardening values (for example `dswd_4ps_auth.sso_only_login`) are
   set again on every upgrade.
4. The API uses the same Keycloak: `dswd_4ps_api` depends on this module, and `dswd_4ps_bridge_client` does too.

**A ticket usually lands in**

- `models/res_users.py`: "A new MSWDO signed in with Keycloak but sees no households" (the area claims).
- `controllers/main.py`: "The login page no longer shows the username and password form" (SSO-only login).
- `models/auth_oauth_provider.py` and its views: "Sign-in fails after Keycloak was moved to a new address."

**Code moment.** `models/res_users.py`: the `_IDP_CLAIM_FIELD_MAP` at the top, then `_auth_oauth_signin`. A plain
`_inherit = "res.users"` that decides how a Keycloak identity becomes an Odoo user with areas.

<!-- Not printed on the card: for the slide deck. -->

**Code excerpt** (`dswd_4ps_auth/models/res_users.py`, lines 35 to 41 at ad98dac9):

```python
# Mapping from OIDC claim keys to res.users field names (B4 multi-level attributes).
_IDP_CLAIM_FIELD_MAP = [
    ("regions", "idp_regions"),
    ("provinces", "idp_provinces"),
    ("cities", "idp_cities"),
    ("barangays", "idp_barangays"),
]
```

## Index: all 66 modules

The Card column gives the card that covers the module. Instance: 1 is registry and operations, 2 is casework, "1 and 2"
installs on both; "not in a bundle" is sample data, demo or test-only. Summaries are the modules' own manifest
summaries.

### Foundation

| Module                          | What it is for                                                             | Instance | Card |
| ------------------------------- | -------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_area`                 | Philippine Standard Geographic Code (PSGC) extensions for area management  | 1 and 2  | 2    |
| `dswd_4ps_registry`             | DSWD 4Ps program registry extensions for households and individuals        | 1 and 2  | 3    |
| `dswd_4ps_roles`                | DSWD 4Ps program security roles and multi-tier approval configuration      | 1 and 2  | 4    |
| `dswd_4ps_approval_multi_group` | Adds OR support for multiple approval groups per tier                      | 1        | 5    |
| `dswd_4ps_approval_flow_data`   | Pre-configured approval definitions for DSWD 4Ps change requests           | 1        | 6    |
| `dswd_4ps_period`               | Monthly compliance periods and the Philippine working-day calendar for 4Ps | 1        | 7    |

### Bundles

| Module               | What it is for                                                                                                                  | Instance | Card |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_starter`   | Complete single-instance DSWD 4Ps bundle — registry, compliance, change requests, payroll, SWDI/CMS, FDS, API, roles, and theme | bundle   | 1    |
| `dswd_4ps_instance1` | Split-instance Registry bundle — registry, compliance, change requests, payroll, FDS, API, and the Registry-side bridge server  | bundle   | 1    |
| `dswd_4ps_instance2` | Split-instance CMS bundle — SWDI, Kilos-Unlad case management, beneficiary portal API, and the CMS-side bridge client           | bundle   | 1    |

### Change requests

| Module                          | What it is for                                                                        | Instance | Card |
| ------------------------------- | ------------------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_change_request`       | 4Ps-specific change request extensions including batching and cancellation            | 1        | 8    |
| `dswd_4ps_supporting_docs_data` | Canonical supporting-document configuration for 4Ps change requests                   | 1        | 9    |
| `dswd_4ps_field_limit`          | Enforce configurable limits on how many times specific registry fields can be updated | 1        | 10   |

### Compliance and FDS

| Module                    | What it is for                                                                                                                        | Instance | Card |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_compliance`     | DSWD 4Ps program compliance tracking for education, health, FDS, and HCDI                                                             | 1        | 11   |
| `dswd_4ps_fds_operations` | Family Development Sessions: session library, parent groups, plans, attendance capture, equivalency, TPP storage, and FDSAR reporting | 1        | 12   |

### Payroll

| Module                     | What it is for                                                                                                                                                                                                     | Instance | Card |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ---- |
| `dswd_4ps_payroll`         | 13-step payroll lifecycle for 4Ps cash grants                                                                                                                                                                      | 1        | 13   |
| `dswd_4ps_catchup_payroll` | Foundation for the catch-up payroll program: data model, cycle/run state machine, singleton program, sequences, and admin scaffolding. Action bodies for DV / Top-Up / PS / CI / LBP land in sub-tickets #397-#404 | 1        | 14   |
| `dswd_4ps_retro_payroll`   | Retroactive payroll: overpayment recovery ledger consumed by the regular CV cycle, underpayment (retro payment) ledger, and a ledger-driven retro disbursement cycle                                               | 1        | 15   |
| `dswd_4ps_pg_partition`    | PostgreSQL LIST partitioning helper for 4Ps payroll snapshot tables                                                                                                                                                | 1        |      |

### Casework

| Module                    | What it is for                                                               | Instance | Card |
| ------------------------- | ---------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_swdi`           | SWDI assessment workflow, review, approval, and household assignment for 4Ps | 2        | 16   |
| `dswd_4ps_swdi_cms`       | SWDI/FRVA triggers for CMS case creation via job worker queue                | 2        | 18   |
| `dswd_4ps_cms`            | Case Management System for the DSWD 4Ps programme (Kilos-Unlad lifecycle)    | 2        | 17   |
| `dswd_4ps_swdi_dashboard` | SWDI dashboards, analytics, reports, and historical comparison views         | 2        |      |
| `dswd_4ps_cms_nas`        | NAS non-attendance candidate dashboard card and list for the CMS             | 2        |      |

### Bridge

| Module                   | What it is for                                                             | Instance | Card |
| ------------------------ | -------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_bridge_shared` | Shared Pydantic schemas and constants for the Registry/CMS bridge          | 1 and 2  | 19   |
| `dswd_4ps_bridge_server` | Registry-side endpoints for the split-instance Registry/CMS bridge         | 1        | 19   |
| `dswd_4ps_bridge_client` | CMS-side bridge: lookup, import, read-only enforcement, push-back, refresh | 2        | 19   |

### Integration

| Module                         | What it is for                                                                     | Instance | Card |
| ------------------------------ | ---------------------------------------------------------------------------------- | -------- | ---- |
| `dswd_4ps_api`                 | 4Ps API Extensions - JWKS endpoint, RS256 authentication, and 4Ps field extensions | 1 and 2  | 20   |
| `dswd_4ps_api_change_request`  | Change-request API endpoints for the 4Ps mobile/external clients                   | 1        | 21   |
| `dswd_4ps_api_compliance`      | Compliance-verification (CV) API endpoints for the 4Ps mobile client               | 1        | 21   |
| `dswd_4ps_api_fds`             | FDS (Family Development Session) API endpoints for the 4Ps mobile/external clients | 1        | 21   |
| `dswd_4ps_api_field_limit`     | Field-update-limit API endpoints for the 4Ps mobile client                         | 1        | 21   |
| `dswd_4ps_swdi_api`            | Mobile sync API endpoint for SWDI assessments                                      | 2        | 21   |
| `dswd_4ps_payroll_api`         | CSSP beneficiary portal read API — payroll / financial status                      | 1        | 22   |
| `dswd_4ps_retro_api`           | NewGRS-facing read API — retro underpayment transaction status                     | 1        | 21   |
| `dswd_4ps_portal_api_base`     | Shared base for the CSSP portal API modules (auth helpers + scopes)                | 1 and 2  | 22   |
| `dswd_4ps_portal_api`          | CSSP beneficiary portal API — FDS + compliance (operations instance)               | 1        | 22   |
| `dswd_4ps_portal_api_casework` | CSSP portal read API — SWDI / FRVA / CMS (casework instance)                       | 2        | 22   |
| `dswd_4ps_integration`         | Producer-side outbound event log + CSSP poll transport (#826)                      | 1        | 23   |
| `dswd_4ps_newgrs`              | NEWGRS grievance-status push receiver + household profile-update notifier          | 1        | 24   |
| `dswd_4ps_ods`                 | HTTP client and UI for the Pantawid ODS API Gateway                                | 1        | 25   |
| `dswd_4ps_auth`                | Auth module for DSWD 4PS system                                                    | 1 and 2  | 26   |

### Registry tools and operations

| Module                          | What it is for                                                                                                                                                                                                                                     | Instance        | Card |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---- |
| `dswd_4ps_registry_import`      | CSV import for 4Ps households and members with household linking, member ID generation, and registry templates                                                                                                                                     | 1               |      |
| `dswd_4ps_export`               | Curated Family and Member data export with DSWD-aligned columns and filters                                                                                                                                                                        | 1               |      |
| `dswd_4ps_ecr`                  | Automated eligibility check for 4Ps program based on poverty, education, and health criteria                                                                                                                                                       | 1               |      |
| `dswd_4ps_hazard`               | Links hazard incidents to 4Ps registrants via area-based auto-assignment                                                                                                                                                                           | 1               |      |
| `dswd_4ps_account_creation`     | Bank account creation workflow for 4Ps grantees                                                                                                                                                                                                    | 1               |      |
| `dswd_4ps_theme`                | DSWD branding colors, login page, and UX overrides for 4Ps                                                                                                                                                                                         | 1 and 2         |      |
| `dswd_4ps_attachment_hardening` | Platform-wide attachment type allowlist, forced download, and AV scan (VA #000278 / #1503)                                                                                                                                                         | 1 and 2         |      |
| `dswd_4ps_post_sql_repair`      | NULL-aware backfill that recomputes stored fields, rebuilds parent_path trees, and advances sequences after a SQL-only data migration that bypassed the Odoo ORM. Operator-driven, optionally area-scoped, with a throttled background full-repair | not in a bundle |      |

### Sample data, demo and test-only

| Module                                 | What it is for                                                                                                                                                                                                                                                                                                          | Instance        | Card |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---- |
| `dswd_4ps_sample_data`                 | Generates deterministic households across 19 real PSGC barangays (referenced by geocode, never created) with a fixed 16-member template covering all member type combinations. Compliance-free base for other sample data modules                                                                                       | not in a bundle |      |
| `dswd_4ps_demo`                        | Generates realistic Filipino 4Ps household and individual demo data for the DSWD Pantawid Pamilyang Pilipino Program modules                                                                                                                                                                                            | not in a bundle |      |
| `dswd_4ps_fds_sample_data`             | Generates realistic FDS demo data on top of the 250 sample households: parent groups, PL/APL, FDS plans, sessions, attendance, TPP assessments, and equivalency records                                                                                                                                                 | not in a bundle |      |
| `dswd_4ps_payroll_sample_data`         | Self-service, queue-based generator for a rich, payroll-ready 4Ps sample dataset: balanced compliance across all four pillars, varied account groups (TAGs), SWDI levels, and F1KD cohorts. Installable from the UI                                                                                                     | not in a bundle |      |
| `dswd_4ps_retro_payroll_sample_data`   | Self-service, queue-based generator for the retro + CV payroll test dataset: 25 real-looking households for every case in the retro payroll test plan, on their own dedicated CV program, with pre-created CV cycles and seeded overpayment/underpayment ledger state. Installable from the UI                          | not in a bundle |      |
| `dswd_4ps_swdi_sample_data`            | Generates 5 years of SWDI and FRVA sample assessments on UAT households                                                                                                                                                                                                                                                 | not in a bundle |      |
| `dswd_4ps_cms_sample_data`             | Seeds a CMS casework chain on the SWDI sample households so the CSSP portal returns data                                                                                                                                                                                                                                | not in a bundle |      |
| `dswd_4ps_cms_demo`                    | Seeds the named users and households used by the CMS manual regression testing guide                                                                                                                                                                                                                                    | not in a bundle |      |
| `dswd_4ps_cms_prototype_demo`          | Seeds the 10 `HH-TEST-*` households + family members + pre-loaded cases used by CMS prototype/UAT demos                                                                                                                                                                                                                 | not in a bundle |      |
| `dswd_4ps_cms_prototype_demo_registry` | Seeds the 10 `HH-TEST-*` households + members on the Registry side of a split-mode UAT deployment                                                                                                                                                                                                                       | not in a bundle |      |
| `dswd_4ps_cms_prototype_demo_shared`   | CSV seed dataset shared by the Registry-side and CMS-side prototype-demo seeders                                                                                                                                                                                                                                        | not in a bundle |      |
| `dswd_4ps_cssp_sample_data_cms`        | Finishes the `HH-TEST-*` prototype demo so the CSSP Kilos Unlad screen renders (Instance 2: CMS/SWDI)                                                                                                                                                                                                                   | not in a bundle |      |
| `dswd_4ps_cssp_sample_data_registry`   | Finishes the `HH-TEST-*` prototype demo so the CSSP Family Development screen renders (Instance 1: registry/FDS)                                                                                                                                                                                                        | not in a bundle |      |
| `dswd_4ps_test_household`              | One obviously-named test household with 18 months of history, populating every field the CSSP beneficiary portal reads                                                                                                                                                                                                  | not in a bundle |      |
| `dswd_4ps_e2e`                         | Year-long simulation test (Jan-Dec 2025, 50 households, 3 areas) exercising CV + catch-up + retro payroll programs end-to-end through compliance, entitlement, NAPA, ORS/DV, top-up files, credit instructions, and the LBP CCTUF result-upload round-trip                                                              | not in a bundle |      |
| `dswd_4ps_security_tests`              | Verification-first access-control harness (issue #1248, UAT pentest T2-11/T4-01): proves per role whether the server-side data layer (ir.model.access + ir.rule) denies direct action/URL reachability of privileged records across CMS, registry, payroll, change-request, compliance, FDS, and the FastAPI RBAC layer | not in a bundle |      |
| `dswd_4ps_cms_nas_direct_tests`        | Integration tests for dswd_4ps_cms_nas direct mode (requires dswd_4ps_compliance)                                                                                                                                                                                                                                       | not in a bundle |      |
