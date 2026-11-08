# Module 5 Ticket Triage: Answer Key

Trainer copy. The tickets are fabricated training scenarios, checked against production commit `ad98dac9` (2026-11-06).
Ticket 5 was reworded from the design's draft because the draft did not fit the code (the reason is under it). Tickets
2, 4 and 6 replace three earlier tickets whose symptoms the trainer says aloud earlier in the afternoon, so that the
triage asks for transfer, not recall; none of the three is spoken in the runbook or copied from a card. Re-check every
answer against production the week before the session.

| #   | Module                          | Category | First file                                                   | Card |
| --- | ------------------------------- | -------- | ------------------------------------------------------------ | ---- |
| 1   | `dswd_4ps_area`                 | M or S   | `models/registrant.py`, then `hooks.py` (the household rule) | 2    |
| 2   | `dswd_4ps_change_request`       | V        | `views/change_request_views.xml` (the search view)           | 8    |
| 3   | `dswd_4ps_approval_flow_data`   | D        | `data/approval_defs_update_hh_info.xml`                      | 6    |
| 4   | `dswd_4ps_fds_operations`       | W        | `wizards/fds_parent_group_transfer.py`                       | 12   |
| 5   | `dswd_4ps_supporting_docs_data` | D        | `data/cr_type_add_member_4ps.xml`                            | 9    |
| 6   | `dswd_4ps_export`               | J        | `models/dswd_export_batch.py`                                | none |
| 7   | `dswd_4ps_swdi_cms`             | J        | `models/cms_event.py`                                        | 18   |
| 8   | `dswd_4ps_payroll_api`          | A        | `services/payroll_service.py`                                | 22   |

How to score at the report-back: the module is the main answer; a pair that names the module and the right card has done
the job. The first file is the stretch. There is time for four tickets aloud: 1, 2, 4 and 6 (four different categories,
and ticket 6 is the one with no card). Ask one pair per ticket, then "who had something different?" Then show the
answers slide with all eight.

Stretch answers (objective 2): ticket 2 builds on `spp_change_request_v2` (the search view it extends is
`spp_change_request_v2.spp_change_request_search`); ticket 7 builds on `spp_case_base` (the job creates an `spp.case`).

Points to draw out:

- Ticket 5 ends in a `noupdate` data file, so its fix ships a migration (section 4.13). Ticket 3 starts in a `noupdate`
  file, but the cause is usually who holds the group and their areas; only a change to the definition itself needs a
  migration.
- Tickets 6 and 7 are jobs: the user's action succeeded, the work happens later, or did not. Look at the record's state
  and the job before the code.
- Tickets 2 and 4 need no model change: in 2 the field exists and the screen does not search it (V); in 4 the limit is a
  field on the parent group that a user can raise, so there may be no code change at all.

## Details

### T1

**Ticket as printed.** "A provincial officer cannot see households in one barangay."

The wording fits the code; keep it.

- **Module**: `dswd_4ps_area` (with `dswd_4ps_roles` for the officer's role areas).
- **Category**: model or security; accept either. Card 2 sends this symptom to `models/registrant.py`, and the rule that
  uses it is security.
- **First file**: `dswd_4ps_area/models/registrant.py` for `area_scope_ids`, the card's answer; then
  `dswd_4ps_area/hooks.py`, where upstream's household record rule is rewritten to use it.
- **Why**: Households are filtered by upstream's global rule `spp_area.rule_res_partner_area_filter`, which
  `dswd_4ps_area/hooks.py` rewrites to `('area_scope_ids', 'in', user.center_area_ids.ids)`; `area_scope_ids` is the
  household's barangay and every area above it. If the officer sees the rest of the province but not one barangay, check
  that barangay's parent chain (`psgc_corrections.py`, migration 19.0.1.13.0) and the households' `area_id`. Then check
  the officer's center areas: the POO local role areas synced from the identity provider in
  `dswd_4ps_roles/models/res_users.py`, and whether RITO set `center_areas_locked`.

### T2

**Ticket as printed.** "A field worker gave us the ticket number the app showed after an update. Typing it in the Change
Requests search finds nothing."

It replaces "Add the place of birth to the Update Member Personal Information request.", which the runbook uses as the
change-request category prompt (block 5).

- **Module**: `dswd_4ps_change_request`.
- **Category**: view.
- **First file**: `dswd_4ps_change_request/views/change_request_views.xml`, the inherited search view
  `spp_change_request_view_search_4ps`.
- **Why**: The app gets `ticketNumber` back from `POST /ChangesSubmission`
  (`dswd_4ps_api_change_request/routers/changes_submission.py`). The ticket number belongs to the `spp.cr.batch` that
  groups the submission's requests (`models/cr_batch.py` generates it as the date, a sequence and the time), not to the
  request. The search view adds `batch_id`, and searching a Many2one matches the batch's name, which is the Batch
  Reference (`name`), not `ticket_number`. The field exists, so the answer is V, not M. Today the user can find it under
  Change Requests > CR Batches, whose search view (`views/cr_batch_views.xml`) has Ticket Number.
- **Every file a full fix touches**: `views/change_request_views.xml`, a search field such as
  `<field name="batch_id" string="Ticket Number" filter_domain="[('batch_id.ticket_number', 'ilike', self)]"/>` in
  `spp_change_request_view_search_4ps`; views are not `noupdate`, so a module update carries it and no migration is
  needed. A test under `dswd_4ps_change_request/tests/` (next to `test_cr_batch.py`) that searches requests by their
  batch's ticket number.

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

**Ticket as printed.** "The C/ML cannot transfer five households into another parent group: it says the group would go
over its max."

It replaces "A child's school attendance was submitted but the household is still non-compliant.", which the runbook
uses as the compliance category prompt (block 7).

- **Module**: `dswd_4ps_fds_operations`.
- **Category**: wizard.
- **First file**: `dswd_4ps_fds_operations/wizards/fds_parent_group_transfer.py`, the action behind the Transfer
  Households button on the parent group form.
- **Why**: The wizard refuses when the target group's member count (`pg_member_count`, live memberships) plus the
  households being moved is above the target's `pg_max_members` (Max Members on the parent group form, default 30;
  #1349). The message says so: "Raise the group's Max Members or transfer fewer households." This is the rule working,
  not a bug: a user who may edit the target group raises its Max Members, or the C/ML moves fewer households. The same
  cap is checked in the merge wizard (`wizards/fds_parent_group_merge.py`), the assign wizard
  (`wizards/fds_household_assign_pg.py`) and Add Households (`models/res_partner.py`).
- **Every file a full fix touches**: none if the group's Max Members is raised. If the business wants a different
  default for new groups: the field default in `models/res_partner.py` and `default_pg_max_members` in the parent group
  action's context in `views/res_partner_views.xml`; existing groups keep their own value unless a migration changes
  them. The cap tests are in `tests/test_1349_1350_membership_guards.py`.

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

**Ticket as printed.** "I exported 3,000 families with Export (DSWD) after lunch. The export batch still says Running
and there is no file."

It replaces "The 2027 working-day deadline raises an error.", which the runbook uses as the period category prompt
(block 3). The module has no card: pairs find it in the catalogue index ("Curated Family and Member data export"), which
checks objective 5.

- **Module**: `dswd_4ps_export`.
- **Category**: job.
- **First file**: `dswd_4ps_export/models/dswd_export_batch.py`: `action_run`, `_dispatch_async`, `_job_build_chunk` and
  `_try_assemble`.
- **Why**: An export larger than `dswd_4ps_export.sync_threshold` (seeded 200; the code never lets it go above 500) runs
  in the background. The batch is split into chunks of about 200 records, about 15 here, each built by its own job on
  the `dswd_export` channel (four at a time, `data/queue_data.xml`). The chunk that completes the set assembles the
  file, sets the batch to Done and posts "Export ready" in its chatter. The maintainer opens the batch under Registry >
  Data Export > Export Batches and compares the chunk count with the chunks done, then looks at the jobs on the
  `dswd_export` channel: still queued behind other work, or a job that never finished. A chunk that raises an error sets
  the batch to Failed with the error text, so a batch still Running means a chunk job has not run or did not complete.
- **Every file a full fix touches**: none if the jobs were only waiting. If a chunk job fails on a bug, the fix is in
  `models/dswd_export_batch.py` (or the columns in `catalog.py`), with a test in `tests/test_export_async.py`. More
  workers for the channel is the queue limit record in `data/queue_data.xml`, which is `noupdate`: an administrator
  changes it on the record, or a migration does.

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
