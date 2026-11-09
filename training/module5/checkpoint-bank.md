# Module 5 Checkpoint Bank

Trainer copy. One standing checkpoint of five minutes, after foundation. Read the symptom, count to three, pairs hold up
a category card, then one pair names the module. Three items; the spares replace an item the class has already seen.
Every symptom comes from a card's "a ticket usually lands in" list, checked at production commit `ad98dac9`.

Checkpoint 2 left the run of show to make room for the Claude Code hour. Its payroll item and the follow-up are now
asked in the payroll tour (runbook block 8); the rest of set 2 is kept as spares.

## Set 1: after foundation (1:53)

| Symptom                                                                                   | Card answer | Module and first file                                                     |
| ----------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------- |
| "My areas reset every time I log in."                                                     | M           | `dswd_4ps_roles`, `models/res_users.py` (card 4)                          |
| "This barangay is listed under the wrong municipality."                                   | D           | `dswd_4ps_area`, `psgc_corrections.py` and a migration (card 2)           |
| "Saving a definition says: Please select at least one approval group."                    | M           | `dswd_4ps_approval_multi_group`, `models/approval_definition.py` (card 5) |
| Spare: "A household at status 3 cannot be reinstated."                                    | M           | `dswd_4ps_registry`, `models/res_partner.py` (card 3)                     |
| Spare: "We changed the approver in the XML but production still routes to the old group." | D           | `dswd_4ps_approval_flow_data`, `migrations/` (card 6)                     |

Point to make after set 1: the barangay item (and the spare about the approver, if used) ends in a migration, because
the data is `noupdate`.

## Set 2: spares (no longer a checkpoint)

| Symptom                                                                       | Card answer | Module and first file                                                                             |
| ----------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------- |
| "Birthdate should be correctable twice, not once."                            | D           | `dswd_4ps_field_limit`, `data/field_limit_one_time_fields.xml` and a migration (card 10)          |
| "The school form was submitted but nothing changed for the child."            | J           | `dswd_4ps_compliance`, `models/event_data.py` (card 11)                                           |
| "We updated the grantee's name but the payroll list still shows the old one." | M           | `dswd_4ps_payroll`, `models/snapshot_beneficiary.py`: by design, the snapshot is sealed (card 13) |
| Spare: "The document type we need is not in the dropdown."                    | D           | `dswd_4ps_supporting_docs_data`, `data/vocabulary_canonical_docs.xml` (card 9)                    |
| Spare: "The run has been on Running Entitlement for hours."                   | J           | `dswd_4ps_payroll`, `data/queue_data.xml` and the job queue (card 13)                             |

Point to make with the payroll item (asked in the payroll tour): it is not a bug. "Sometimes the answer to a ticket is:
this is how it must work, and here is why."

Follow-up to the payroll item (objective 4), one pair answers aloud: "A colleague wants to let `write()` change the name
on the snapshot to fix this. What breaks?" Answer: the snapshot is frozen to preserve the audit, and every later
document (the NAPA Summary, the payroll summary, the ORS and DV) reads it; a name changed after the seal would disagree
with documents already produced. The correction is a rewind before the point of no return, not a wider allowlist (card
13).
