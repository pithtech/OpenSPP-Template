# DSWD 4Ps Program Reference

Background on the Pantawid Pamilyang Pilipino Program (4Ps) for the OpenSPP and Odoo Foundations Training. Use it to
pick examples, name fields and vocabularies the way the program does, and answer "where does this live in the system"
questions. Bracketed numbers point to the sources in section 10. Every figure carries its as-of date; later numbers
quoted in the press are marked as such.

Compiled 2026-11-08 from online sources and from the production 4Ps module source code (`dswd-4ps-dp-openspp-v2-module`,
Newlogic). Verify any number before putting it on a slide.

---

## 1. Program overview

- **Purpose**: the national poverty reduction strategy and human capital investment program. Conditional cash transfers
  (CCT) to poor households to improve health, nutrition and education and break the intergenerational cycle of poverty
  [1].
- **History**: pilot in Q4 2007 (PHP 50M, 4,589 households); named Pantawid Pamilya by DSWD AO 16 s.2008; launched
  January 2008 in Ozamiz City [1]. Institutionalised by law in 2019 [5].
- **Legal basis**: Republic Act 11310, the 4Ps Act, approved 17 April 2019; IRR approved December 2019 [2][3]. Executive
  Order 120 (13 July 2026) extends participation beyond the 7-year cap for households still at SWDI level 1 or 2
  [19][20].
- **Implementing agency**: DSWD (RA 11310 sec. 14), advised by a National Advisory Council (DSWD, DOH, DepEd, DA, DOLE,
  DTI, DAR, DOST, TESDA plus two NGOs, sec. 15) and Independent Monitoring Committees (sec. 16); PIDS runs an impact
  assessment every three years (sec. 10) [2].
- **Scale**: 4,076,035 active households as of 30 September 2024 against an annual target of 4.4M, in 41,676 barangays;
  86.07% of grantees are women [6]. Press, August 2026: more than 2.8M enrolled, with 400,000 to 500,000 validated
  households waitlisted [21]. Cumulative exits: 1,981,543 households as of September 2024 [6].
- **Budget**: PHP 106.3B in the 2024 GAA [7]; PHP 114.2B proposed for 2025 [8]; 2024 adjusted allotment PHP 96.2B
  (health 37.6B, education 28B, rice 30.1B) [6]; PHP 113B in the 2026 GAA [9].

## 2. Eligibility and targeting

- **Targeting**: the Standardized Targeting System (STS), today Listahanan / NHTS-PR, run by the National Household
  Targeting Office and revalidated every three years (RA 11310 sec. 5) [2][1]. EO 867 (2010) directs all agencies to use
  NHTS-PR [10].
- **Method**: Listahanan uses a Proxy Means Test that estimates income from non-income indicators; a household is poor
  when the estimate is below the PSA provincial poverty threshold [4][11]. Listahanan 1 (2009) found about 5.25M poor
  households [11]; Listahanan 3 (released 2022) found 5,599,091 [10].
- **Who qualifies** (sec. 6): poor or near-poor per the STS and the PSA threshold; a member aged 0 to 18 and/or a
  pregnant member at registration; willing to comply with the conditions. Farmers, fisherfolk, homeless, indigenous
  peoples, informal settlers and GIDA residents are automatically included in targeting [2][4].
- **Pipeline**: NPMO runs the Eligibility Check Routine (ECR) on NHTO data; the list is posted locally for at least a
  week; validation by community assembly or house to house; encoding in CARS; registration [1].
- **Household and member**: the household is the unit of entitlement and payment; members are tracked individually
  (children 0 to 18 for education and health monitoring, pregnant women, the grantee). "Children" are sons, daughters or
  grandchildren of the household head [6]; education grants cover only children or grandchildren of the head or spouse
  [1].
- **Duration**: at most seven years (sec. 4), counted from the year the IRR took effect for households registered
  earlier [1]. About 1.8M households were expected to reach the cap in 2026 (DSWD MC 021 s.2026) [19]; EO 120 extends
  level 1 and 2 households subject to annual reassessment [20].
- **Exit and graduation**: the Kilos-Unlad "Graduation to Exit" stage starts in year 5. A household may exit with at
  least two of: SWDI level 3 in the current cycle, level 3 in the preceding cycle, non-poor in the latest STS, a
  case-manager transition assessment. Transition plan of 6 to 12 months; graduates get client status 03 "Graduated Due
  to Improved Level of Well-being" [1].

## 3. Grants and amounts

Current amounts per RA 11310 and the Operations Manual, 5th edition (2021), unless dated otherwise.

| Grant                                 | Amount                                                                        | Notes                                                                                                        |
| ------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Health and nutrition                  | PHP 750 per household per month, 12 months a year                             | Fixed regardless of household size [2][1]                                                                    |
| Education, day care/kinder/elementary | PHP 300 per child per month, up to 10 months a school year                    | Maximum 3 children per household until lifted by NAC resolution [1][5]                                       |
| Education, junior high                | PHP 500 per child per month                                                   |                                                                                                              |
| Education, senior high                | PHP 700 per child per month                                                   | ALS learners paid by assigned grade level [1][2]                                                             |
| Rice subsidy                          | PHP 600 per household per month                                               | Needs compliance with a health or education condition; from SONA 2016 and MC 6 s.2017, not in the Act [1][4] |
| First 1,000 Days (F1KD)               | PHP 350 per month from February 2025; PHP 750 from 9 July 2026 (MC 10 s.2026) | Pregnant women and children to age 2; 180,000+ expected in 2026 [12][13]                                     |

- **Other benefits**: automatic PhilHealth coverage (sec. 8); priority in the Sustainable Livelihood Program (sec. 13)
  [2]. MCCT households may get an Alternative Family Home rent subsidy of up to PHP 6,500 a month [1].
- **Schedule**: six bi-monthly periods. Example: period 1 monitors February to March, is processed in April and paid in
  May [1]; grants are "released every two months" [5].
- **Channels**: digital transaction account, EMV cash card (ATM or POS), or over the counter through the Authorized
  Government Depository Bank (Land Bank) or a conduit (rural bank, cooperative, remittance firm); sec. 9 allows
  BSP-regulated conduits in underserved areas [1][2]. 92.6% were paid by cash card as of Q2 2021 [14]; later splits not
  found.

## 4. Conditionalities and compliance

RA 11310 sec. 11 [2], as detailed in the Operations Manual [1] and DSWD field office pages [5]:

| Who                    | Condition                                                                |
| ---------------------- | ------------------------------------------------------------------------ |
| Pregnant women         | Prenatal check-ups, skilled facility birth, post-partum and newborn care |
| Children 0 to 5        | Check-ups and vaccination: monthly under 2, every two months from 2 to 5 |
| Children 1 to 14       | Deworming twice a year                                                   |
| Children 3 to 4        | Day care or pre-school, at least 85% attendance                          |
| Children 5 to 18       | School, at least 85% attendance                                          |
| One responsible person | Monthly Family Development Session (FDS)                                 |

- **Compliance Verification System (CVS)**: CVF 1 masterlist (C/ML), CVF 2 education (school head), CVF 3 health (health
  facility), CVF 4 FDS (C/ML). Results feed the Payroll Generation System, which computes grants per period. Initial
  grants are paid without verification on registration [1].
- **Q3 2024 compliance**: health 98.38%, FDS 94.65% (3,844,277 of 4,054,976 monitored) [6].
- **Sanctions** (sec. 12, IRR sec. 20): written notice and grants stop for the non-compliant month or period; four
  consecutive months leads to case management; persistent non-compliance for a year after notice leads to removal with
  notice [2][1]. Only 743 households were delisted as persistently non-compliant cumulatively to September 2024 [6].
- **Exemptions**: "purple tagging" (client status 28) suspends conditions for households in difficult circumstances; the
  NAC or the Secretary may suspend conditions in calamities for up to three consecutive CVS periods [1][2].

## 5. Program structure and roles

- **Grantee**: the mother by default, else the father, then a grandparent; one per household; a minor only in
  exceptional cases [1]. The "responsible person" is the parent or guardian who must attend FDS [2].
- **Household head**: the reference member for defining children and the roster [6].
- **Parent Leader (PL)**: each parent group elects a Parent Leader and an assistant for at most three years, one term;
  volunteers who relay information, handle logistics and attest absences [1].
- **City/Municipal Link (C/ML)**: the DSWD case manager who works with households from registration to exit; facilitates
  referrals, FDS, BUS updates and over-the-counter payouts; supported by Social Welfare Assistants [1].
- **Hierarchy**: NPMO (central) to RPMO (regional, under the Regional Director) to Provincial Operations Office to
  Cluster Operations Offices to City/Municipal Operations Office [1]. Workforce 17,661 of 18,729 positions as of
  September 2024 [6]. The training audience (RITOs, CMTs, NPMO IT staff) sits in the RPMO and NPMO layers.
- **SWDI**: Social Welfare and Development Indicators, a case-management tool administered yearly that measures economic
  sufficiency and social adequacy. Levels: 1 Survival, 2 Subsistence, 3 Self-sufficiency [1][20].
- **PPIS**: the Pantawid Pamilya Information System, the web systems on the 4Ps database run by DSWD ICTMS: ECR, CARS,
  BUS, CVS, PGS, GRS, Case Management System, Retroactive Payment System, Payment Reconciliation System [1].

## 6. Status vocabularies and categories

- **Household status** (Operations Manual table 5): Active (registered, eligible subject to compliance); Inactive
  (temporarily deactivated: duplicate, waiver, no eligible child; can be reactivated); Delisted (no longer eligible:
  waiver, failed criteria, misconduct). Member status mirrors it: active, moved out, no longer part of the household
  [1].
- **Client status codes**: the production module `dswd_4ps_registry` ships 32 client statuses in 9 categories (active,
  inactive, appealable, delisted, pool of qualified households, graduated, reactivated, deactivated, reinstatement) in
  `data/vocabulary_client_status.xml`. Codes seen in public sources: 03 graduated, 19 under validation, 28 purple-tagged
  [1][6].
- **Delisting reasons**: no eligible member; misdemeanour; waiver; non-poor per the STS; consistent non-compliance;
  seven-year stay used up [1]. Exits to September 2024: no more eligible children 980,713; misbehaviour (pawning,
  gambling) 59,139; voluntarily waived 50,999; delisted due to inactivity 432,881; persistently non-compliant 743;
  graduated 457,068 [6].
- **Modalities**: Regular CCT; Modified CCT (MCCT) for homeless street families including itinerant indigenous peoples,
  IPs in GIDA, families in need of special protection (disaster-affected) and hazardous-work groups. MCCT households are
  mainstreamed into regular CCT per MC 08 s.2016 [1]. Regional example: 250,617 regular versus 27,283 MCCT [23].
- **Sets**: registration rounds numbered per year (Set 11B in 2022, Set 12 in 2023) used to fill vacated slots [15][16].
  The production module's set group vocabulary runs from `1A` to `12V`, with definitions such as "Listahanan 2 Poor
  Households" (11B) and "MCCT Mainstreaming" (10A).
- **BUS update types**: transfer of residence, change of grantee, add or remove member, correction, filed on BUS forms 5
  and 6 and approved by the Regional Director [1][17].
- **ESGP-PA / TES**: CHED and DSWD tertiary grant for 4Ps children (2012, expanded 2014); continuing grantees were
  absorbed into the Tertiary Education Subsidy under RA 10931. 4Ps membership alone does not qualify for TES [18].
- **Kilos-Unlad**: the seven-year social case management framework, ten components from registration to exit, moving
  households from survival to subsistence to self-sufficiency [1].

## 7. Grievance Redress System (GRS)

- Captures complaints from beneficiaries, stakeholders and the public at all levels; a social accountability measure
  against error, fraud and leakage; the NAC is mandated to establish it (sec. 15d) [2][24].
- **Channels**: walk-in, payout grievance desk, SMS, phone hotline, mail, email, social media [1][4].
- **Types** (Operations Manual table 13): 1 payment issue; 2 card issue; 3 inclusion request; 4 disqualification
  (regular income, high-value property, relatives abroad); 5 misbehaviour (pawning, gambling, misrepresentation, fraud,
  collection, persuasion, disinformation); 6 appeal for reinstatement; 7 facility issue; 8 implementer issue; plus
  "request and inquiry" in reporting [1][6].
- **Q3 2024**: 58,706 grievances, 92.30% resolved; request and inquiry 71.25%, inclusion 10.29%, payment 8.29% [6]. PIDS
  (2010 to 2022 data): payment issues dominate and resolution rates fell in 2021 and 2022 [24].

## 8. Where each concept lives in OpenSPP

This is the bridge between the program and the code. Upstream models are in `upstream/openspp/`; the production
`dswd_4ps_*` modules are the Newlogic implementation that the training examples simplify.

| 4Ps concept                                                 | OpenSPP model or module                                             | Production 4Ps module                                                    |
| ----------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Household, member                                           | `res.partner` (`is_registrant`, `is_group`), `spp.group.membership` | `dswd_4ps_registry`                                                      |
| Grantee, household head                                     | `spp.group.membership` type codes (`head`), grantee flag            | `dswd_4ps_registry` (grantee change, head change)                        |
| Client and member status, sets, well-being level, IP groups | `spp.vocabulary` / `spp.vocabulary.code`                            | `dswd_4ps_registry` (26 vocabulary data files)                           |
| PhilSys, 4Ps ID, PhilHealth numbers                         | `spp.registry.id`, ID type codes with regex                         | `dswd_4ps_registry/data/id_types.xml`                                    |
| Region, province, city, barangay                            | `spp.area`                                                          | `dswd_4ps_area`                                                          |
| Bi-monthly periods                                          | `spp.cycle`                                                         | `dswd_4ps_period`                                                        |
| Program, enrolment                                          | `spp.program`, `spp.program.membership`                             | `dswd_4ps_starter`                                                       |
| Conditions, CVS forms 2 to 4                                | `spp_event_data`, compliance criteria                               | `dswd_4ps_compliance`, `dswd_4ps_api_compliance`                         |
| Family Development Sessions                                 | event data                                                          | `dswd_4ps_fds_operations`, `dswd_4ps_api_fds`                            |
| Grants, payroll, retroactive payments                       | `spp.entitlement`, cycles                                           | `dswd_4ps_payroll`, `dswd_4ps_retro_payroll`, `dswd_4ps_catchup_payroll` |
| Cash card, account type                                     | `spp_banking`, `res.partner.bank`                                   | `dswd_4ps_registry` (account types), `dswd_4ps_account_creation`         |
| BUS updates                                                 | `spp.change.request` (`spp_change_request_v2`)                      | `dswd_4ps_change_request`, `dswd_4ps_api_change_request`                 |
| ECR                                                         | eligibility managers on `spp.program`                               | `dswd_4ps_ecr`                                                           |
| GRS                                                         | `spp_grm`                                                           | `dswd_4ps_newgrs`                                                        |
| SWDI                                                        | assessment events                                                   | `dswd_4ps_swdi`, `dswd_4ps_swdi_cms`, `dswd_4ps_swdi_api`                |
| Roles (RITO, C/ML, RPMO)                                    | `spp_security` three-tier groups, `base_user_role`                  | `dswd_4ps_roles`                                                         |

## 9. Glossary

| Term                  | Meaning                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| Pantawid Pamilya, 4Ps | "Bridging the family"; the DSWD conditional cash transfer program [1]                             |
| Listahanan, NHTS-PR   | National Household Targeting System for Poverty Reduction; PMT-based poor-household database [11] |
| STS                   | Standardized Targeting System, the legal term for Listahanan [2]                                  |
| Kilos-Unlad (KU)      | Seven-year case-management framework toward self-sufficiency [1]                                  |
| SWDI                  | Social Welfare and Development Indicators; yearly well-being assessment, levels 1 to 3 [1]        |
| FDS                   | Family Development Session; monthly, one responsible person per household [2]                     |
| CVS, CVF              | Compliance Verification System and its forms 1 to 4 [1]                                           |
| C/ML                  | City/Municipal Link; the DSWD field case manager [1]                                              |
| PL                    | Parent Leader; elected volunteer of a parent group [1]                                            |
| MCCT                  | Modified CCT for homeless, GIDA indigenous and special-protection families [1]                    |
| GRS                   | Grievance Redress System [1]                                                                      |
| BUS                   | Beneficiary Update System, household roster and profile changes [1]                               |
| BDM, BDMS             | Beneficiary Data Management (System) [17]. "BAS" was not found in DSWD sources.                   |
| PPIS                  | Pantawid Pamilya Information System [1]                                                           |
| PGS                   | Payroll Generation System [1]                                                                     |
| ECR, CARS             | Eligibility Check Routine; Community Assembly Registration System [1]                             |
| NPMO, RPMO, POO       | National and Regional Program Management Office; Provincial Operations Office [1]                 |
| NAC                   | National Advisory Council [2]                                                                     |
| GIDA                  | Geographically isolated and disadvantaged area [1]                                                |
| HSF, FNSP             | Homeless street families; families in need of special protection [1]                              |
| F1KD                  | First 1,000 Days grant [12]                                                                       |
| ESGP-PA, TES          | Expanded Students' Grants-in-Aid Program; Tertiary Education Subsidy [18]                         |
| AGDB                  | Authorized Government Depository Bank (Land Bank) [1][2]                                          |
| CCTG                  | Conditional Cash Transfer Group, the DSWD office that owns 4Ps (training organiser)               |

## 10. Sources

1. DSWD 4Ps Operations Manual, 5th edition (2021):
   <https://pantawid.dswd.gov.ph/wp-content/uploads/2022/08/08152022_4ps_OM_print.pdf>
2. RA 11310 full text: <https://lawphil.net/statutes/repacts/ra2019/ra_11310_2019.html>
3. Senate issuances library, RA 11310: <https://issuances-library.senate.gov.ph/node/17784>
4. DSWD 4Ps FAQ: <https://pantawidnew.dswd.gov.ph/faq>
5. DSWD-CAR 4Ps page: <https://car.dswd.gov.ph/programs-services/core-programs/pantawid-pamilyang-pilipino-program-4ps/>
6. 4Ps 2024 3rd Quarter Report: <https://pantawid.dswd.gov.ph/wp-content/uploads/2024/12/2024-3rd-Quarter-Report.pdf>
7. Inquirer, 2024 budget: <https://newsinfo.inquirer.net/1910625/dbm-4ps-budget-for-2024-is-p106-3-billion>
8. Manila Bulletin, 2025 budget: <https://mb.com.ph/2024/8/27/government-boosts-4-ps-budget-to-p114-billion-for-2025>
9. PIA, 2026 DSWD budget: <https://pia-ncr.blogspot.com/2026/01/gatchalian-says-dswd-budget-to-hit.html>
10. Manila Bulletin, Listahanan 3:
    <https://mb.com.ph/2022/8/1/dswds-3rd-listahanan-identifies-close-to-5-6-million-poor-households>
11. DSWD Social Registry (Listahanan): <https://socialregistry.dswd.gov.ph/?p=207>
12. GMA, F1KD raised to PHP 750 (July 2026):
    <http://www.gmanetwork.com/news/topstories/nation/994883/dswd-expands-first-1-000-days-cash-grants-for-qualified-4ps-beneficiaries/story>
13. Manila Bulletin, F1KD launch (January 2025):
    <https://mb.com.ph/2025/1/13/additional-4-ps-grants-for-pregnant-women-young-children>
14. PIDS payment system study:
    <https://pids.gov.ph/details/pids-study-provides-recommendations-for-a-more-effective-responsive-4ps-payment-system>
15. DSWD-CAR, Set 11B registration:
    <https://car.dswd.gov.ph/2022/03/dswd-car-registers-6068-new-sets-of-4ps-households-for-replacement/>
16. DSWD FO9, Set 12 registration: <https://fo9.dswd.gov.ph/2023/02/4ps-registration-for-new-members-starts-february>
17. DSWD Quezon BDM page: <https://sites.google.com/dswd.gov.ph/quezonpantawidpamilya/core-systems/bdm>
18. CHED, ESGP-PA and TES:
    <https://legacy.ched.gov.ph/esgp-pa-grantees-automatically-qualified-under-the-tertiary-education-subsidy/>
19. EO 120 (2026) text: <https://www.lawphil.net/executive/execord/eo2026/eo_120_2026.html>
20. DSWD release on EO 120:
    <https://pantawid.dswd.gov.ph/2026/07/dswd-welcomes-pbbms-eo-extending-participation-period-for-4ps-grantees-to-help-them-reach-self-sufficiency-level-before-program-exit/>
21. Daily Tribune, August 2026 enrolment and waitlist:
    <https://tribune.net.ph/2026/08/01/up-to-500000-families-await-enrollment-in-4ps-dswd>
22. Manila Bulletin, May 2026 exits:
    <https://mb.com.ph/2026/05/11/over-16-million-households-exit-4ps-since-2008-car-records-most-graduates>
23. DSWD FO7, regular versus MCCT: <https://fo7.dswd.gov.ph/?p=5405>
24. PIDS RPS 2024-08, GRS study:
    <https://pids.gov.ph/publication/research-paper-series/from-complaints-to-opportunities-analyzing-grievance-trends-and-responsiveness-in-the-4ps>
25. PhilSys use-case annex (BUS, CVS, GRS, CARS):
    <https://procurement.psa.gov.ph/sites/default/files/ANNEX%20A_%20USE_CASES_FOR_PHILSYS.pdf>
26. PIDS third-wave impact evaluation:
    <https://pids.gov.ph/publication/discussion-papers/reassessing-the-impact-of-the-pantawid-pamilyang-pilipino-program-results-of-the-third-wave-impact-evaluation>

**Not found or unverified**: an official 2025 or 2026 national quarterly report (the latest official count is September
2024; the August 2026 figure is press-quoted); the May 2026 press figure of "over 1.6M exits since 2008" does not
reconcile with the 1.98M in the September 2024 report; a current cash-card versus over-the-counter split; a definition
of "BAS"; the IRR itself could not be fetched directly, so IRR provisions are cited through the Operations Manual.
