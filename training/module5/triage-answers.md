# Module 5 Ticket Triage: Answer Key

Trainer copy. The tickets are fabricated training scenarios, checked against production commit `ad98dac9` (2026-11-06).
Two were reworded from the design's draft because the draft did not fit the code (tickets 2 and 5; the reason is under
each). Re-check every answer against production the week before the session.

| #   | Module                          | Category | First file                                                            | Card |
| --- | ------------------------------- | -------- | --------------------------------------------------------------------- | ---- |
| 1   | `dswd_4ps_area`                 | S        | `dswd_4ps_area/hooks.py` (the household rule), `models/registrant.py` | 2    |
| 2   | `dswd_4ps_change_request`       | M        | `models/cr_detail_update_member_info.py`                              | 8    |
| 3   | `dswd_4ps_approval_flow_data`   | D        | `data/approval_defs_update_hh_info.xml`                               | 6    |
| 4   | `dswd_4ps_compliance`           | J        | `models/event_data.py`                                                | 11   |
| 5   | `dswd_4ps_supporting_docs_data` | D        | `data/cr_type_add_member_4ps.xml`                                     | 9    |
| 6   | `dswd_4ps_period`               | D        | `data/ph_holidays_2027.xml`                                           | 7    |
| 7   | `dswd_4ps_swdi_cms`             | J        | `models/cms_event.py`                                                 | 18   |
| 8   | `dswd_4ps_payroll_api`          | A        | `services/payroll_service.py`                                         | 22   |

How to score at the report-back: the module is the main answer; a pair that names the module and the right card has done
the job. The first file is the stretch. Ask one pair per ticket, then "who had something different?"

Points to draw out:

- Tickets 2, 3 and 5 all end in a `noupdate` data file, so each fix ships a migration (section 4.13).
- Tickets 4 and 7 are jobs: the user's action succeeded, the work happened later, or did not. Look at the job and its
  state before the code.
- Ticket 6 needs no code at all: an administrator seeds the year.

## Details

### T1

**Ticket as printed.** "A provincial officer cannot see households in one barangay."

The wording fits the code; keep it.

- **Module**: `dswd_4ps_area` (with `dswd_4ps_roles` for the officer's role areas).
- **Category**: security.
- **First file**: `dswd_4ps_area/hooks.py`, where the household record rule is rewritten; then
  `dswd_4ps_area/models/registrant.py` for `area_scope_ids`. Accept M (model) if the pair names `registrant.py` and
  explains the rule.
- **Why**: Households are filtered by upstream's global rule `spp_area.rule_res_partner_area_filter`, which
  `dswd_4ps_area/hooks.py` rewrites to `('area_scope_ids', 'in', user.center_area_ids.ids)`; `area_scope_ids` is the
  household's barangay and every area above it. If the officer sees the rest of the province but not one barangay, check
  that barangay's parent chain (`psgc_corrections.py`, migration 19.0.1.13.0) and the households' `area_id`. Then check
  the officer's center areas: the POO local role areas synced from the identity provider in
  `dswd_4ps_roles/models/res_users.py`, and whether RITO set `center_areas_locked`.

### T2

**Original ticket.** "Add the mother's maiden name to the Update Member Info request."

**Why it was rewritten.** The mother's maiden name is already captured, as three fields (first, middle and last), by the
request type now called "Update Member Additional Information" (code `update_individual_4ps`; migration `19.0.1.32.0`
split the mapping). "Update Member Info" was renamed "Update Member Personal Information" (code `update_member_info`,
migration `19.0.1.31.0`) and holds the name, suffix, birthdate and sex. The place of birth (`birth_place` on
`res.partner`, from upstream `spp_registry`) is in neither.

**Ticket as printed.** "Add the place of birth to the Update Member Personal Information request."

**Answer.** Module: `dswd_4ps_change_request`. Category: model. First file:
`dswd_4ps_change_request/models/cr_detail_update_member_info.py`. Add `current_birth_place` (related to
`registrant_id.birth_place`) and `birth_place` to the detail model, show both in
`views/detail_update_member_info_views.xml`, and add a mapping record `birth_place` to `birth_place` in
`data/cr_type_update_member_info.xml`. That file is `noupdate="1"`, so a full fix also adds
`migrations/<next version>/post-migrate.py` that creates the mapping on existing databases and bumps the manifest
version. If the mobile app sends the field: `dswd_4ps_api_change_request/schemas/change_request_detail.py`
(`UpdateMemberInfoDetail`), `schemas/changes_submission.py` and `_extract_member_info` in
`services/changes_submission_service.py`, plus the trigger path in
`dswd_4ps_supporting_docs_data/data/cr_type_update_member_info.xml` (also `noupdate="1"`, so a migration there too).
Tests: `dswd_4ps_change_request/tests/test_cr_update_member_info.py` and the API module's tests.

### T3

**Ticket as printed.** "Nobody can approve a client-status change from 24 to 3."

The wording fits the code; keep it. Code 24 is "GRS: Suspended grants due to misbehavior of HH" (Active category) and
code 3 is "Graduated Due to Improved Level of Well-Being" (Delisted category). A definition matches exactly 24 to 3.

- **Module**: `dswd_4ps_approval_flow_data`.
- **Category**: data or vocabulary.
- **First file**: `dswd_4ps_approval_flow_data/data/approval_defs_update_hh_info.xml`.
- **Why**: Definition `approval_def_hh_info_poo_rpmo` (sequence 10, its CEL matches old code 24 and new code 3) on the
  Update Household Info type has two blocking tiers: POO Review (SWO III), then RPMO Review (RGO). Check that someone
  holds `group_4ps_swo_iii` (local role `local_role_swo_iii`) and, for tier 2, `group_4ps_rgo`, with the household's
  area in their center areas, since `dswd_4ps_roles/hooks.py` scopes validators by area. The records are `noupdate`, so
  also compare the production record with the XML (an admin edit, or `use_multitier` missing because the `<function>`
  that sets it runs only on first install).

### T4

**Ticket as printed.** "A child's school attendance was submitted but the household is still non-compliant." (Fits the
code; kept.)

**Answer.** Module: `dswd_4ps_compliance`. Category: job. First file: `dswd_4ps_compliance/models/event_data.py`. The
maintainer checks, in order: whether the event is `active` or was left `draft` with a `flag_reason` because the member
or household id did not match (`dswd_4ps_api_compliance/routers/cv_router.py`); whether the `cv_events` job ran or is
still queued or requeued behind the household lock; and, in `models/compliance_pipeline.py`
(`compute_school_compliance_inner`), whether the child has `x_4ps_education_grant` (without it the event is skipped
silently), which period `attendance_month` put the row in, and the 85% constant. Then whether the household still has
`x_4ps_cv_needs_reconcile` set, waiting for the daily reconcile (`_cv_reconcile_id_range` in `models/res_partner.py`).
The household shows compliant only when every active member is compliant on every pillar that applies
(`_is_household_compliant`), so another member's health or FDS row may be the cause. A fix touches
`models/compliance_pipeline.py` (or `models/event_data.py`) and a test under `dswd_4ps_compliance/tests/` that creates
`spp.event.data` events, such as `test_school_attendance_month.py`.

### T5

**Original ticket.** "Add Member now needs one more required document."

**Why it was reworded.** Add Member does not have a list of required documents: it requires any one of seven (a document
group with `min_required` 1 in `dswd_4ps_supporting_docs_data/data/cr_type_add_member_4ps.xml`). "One more required
document" could mean adding an eighth option or demanding a document every time; the printed ticket names the second.

**Ticket as printed.** "Add Member must now always include the Household Head Declaration, not just any one of the usual
documents."

**Answer.** Module: `dswd_4ps_supporting_docs_data`. Category: data or vocabulary. First file:
`dswd_4ps_supporting_docs_data/data/cr_type_add_member_4ps.xml`. Add a second `spp.cr.type.document.group` with only
`dswd_4ps_hh_head_declaration` and `min_required` 1 (or set `required_document_ids`), and decide with the business
whether it stays in the any-one pool. The file is `noupdate="1"`, so a full fix adds
`migrations/19.0.1.3.0/post-migrate.py`, bumps the manifest version, and adds an assertion to
`tests/test_canonical_doc_bindings.py`. If the document is a new type, it also goes in
`data/vocabulary_canonical_docs.xml` and the test's `CANONICAL_DOC_CODES`. The mobile app's `$required_documents`
endpoint already reads groups and required documents, so no API change; derived requests skip document validation and
are not affected.

### T6

**Ticket as printed.** "The 2027 working-day deadline raises an error."

The scenario fits the code: 2027 ships as an empty Draft year on purpose. Optional wording closer to a user report:
"Saving an underpayment grievance received in December shows: No holiday calendar has been seeded for 2027."

- **Module**: `dswd_4ps_period`.
- **Category**: data or vocabulary.
- **First file**: `dswd_4ps_period/data/ph_holidays_2027.xml`.
- **Why**: `_assert_year_seeded` in `dswd_4ps_period/models/holiday.py` refuses any working-day count that touches a
  year not marked Seeded. The production caller is the retro underpayment deadline
  (`dswd_4ps_retro_payroll/models/underpayment.py`: 7 and 20 working days from the Certificate of Compliance receipt
  date, grievance origin only), so receipts from about early December 2026 reach into 2027. The fix is not code: a
  System Administrator enters the 2027 proclamation under Settings > DSWD 4Ps > Holiday Calendar and marks the year
  Seeded; no 2028 data file should be added.

### T7

**Ticket as printed.** "A Level 1 assessment was approved but no case was created."

- **Module**: `dswd_4ps_swdi_cms`
- **Category**: job
- **First file**: `dswd_4ps_swdi_cms/models/cms_event.py`
- **Why**: approving the assessment calls `_trigger_cms_if_needed`, which creates a `dswd.swdi.cms.event` for the
  `swdi_level_1` trigger and queues `_dispatch_cms_case`; the case itself is created in that job. The maintainer first
  checks the trigger configuration: if `swdi_level_1` is not active, no event exists and the only trace is a warning in
  the log. If an event exists, its state says the rest: `pending` or `processing` means the job is waiting or will retry
  (see `retry_count` and `next_retry_at`); `failed` means the three retries (5 minutes, 15 minutes, 1 hour) were used up
  and the event is in the dead letter, with `error_message` showing why. After fixing the cause, the Retry action
  re-queues it.

The ticket fits the code as written; the wording is unchanged.

### T8

**Ticket as printed.** "The beneficiary portal shows no payroll for a household that was paid."

- **Module**: `dswd_4ps_payroll_api`
- **Category**: API
- **First file**: `dswd_4ps_payroll_api/services/payroll_service.py`
- **Why**: the portal's Finance tab calls `/payroll/Household/{listahanan_id}/financial-status` and `/payout-history`.
  An empty answer with HTTP 200 comes from the service. A refused scope or a missing `Authorization-Beneficiary` header
  would be a 403 from `routers/payroll_router.py`. The maintainer checks the following. Does the household have an
  active `spp.payment`? The service reads payments, not the snapshot: a snapshot row exists even for households not
  paid. Did the bank confirm the payment? The last grant counts only `delivery_status` `success`, while a payment still
  pending shows only in the history. Was the household paid by catch-up? That ledger is read only when
  `dswd_4ps_catchup_payroll` is installed and the caller can read it. Is `payrollAvailable` `false`? Then the API user
  lacks the payroll groups: check `dswd_4ps_api/data/service_user_role.xml` and the record rules that apply to that
  user.
- **Wording**: the ticket fits the code as written. The draft answer in the design ("snapshot") needs correcting: the
  service reads `spp.payment` and uses the snapshot only for amounts and periods.
