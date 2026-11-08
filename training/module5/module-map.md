# Module 5 Module Map (poster)

Print at A1 for the wall and at A4 on the inside cover of the catalogue. It is the first slide of the map block and
stays up all afternoon. Production commit `ad98dac9` (2026-11-06): 66 modules with a manifest. 26 cards cover 38 of
them; the rest are in the catalogue index.

## The process, top to bottom

```
                         DSWD 4Ps on OpenSPP v2 (Odoo 19)             (n) = card number

  WHERE       dswd_4ps_area (2)            PSGC regions to barangays, area scoping
  WHO         dswd_4ps_registry (3)        households, members, client status, grantee
  WHO MAY     dswd_4ps_roles (4)           POO / RPMO / NPMO tiers, local and global roles
              dswd_4ps_approval_multi_group (5), dswd_4ps_approval_flow_data (6)
  WHEN        dswd_4ps_period (7)          monthly periods, working-day calendar
  ----------------------------------------------------------------------------------
  CHANGE      dswd_4ps_change_request (8)  + supporting_docs_data (9), field_limit (10)
  VERIFY      dswd_4ps_compliance (11)     + fds_operations (12)
  PAY         dswd_4ps_payroll (13)        + catchup_payroll (14), retro_payroll (15)
  ASSESS      dswd_4ps_swdi (16)
  MANAGE      dswd_4ps_cms (17)            + swdi_cms (18)
              no card: pg_partition, swdi_dashboard, cms_nas
  ----------------------------------------------------------------------------------
  CONNECT     the bridge (19)              bridge_shared, bridge_server, bridge_client
              dswd_4ps_api (20)            + route modules (21): api_change_request,
                                             api_compliance, api_fds, api_field_limit,
                                             swdi_api, retro_api
                                           + portal APIs (22): portal_api_base,
                                             portal_api, portal_api_casework, payroll_api
              dswd_4ps_integration (23), dswd_4ps_newgrs (24), dswd_4ps_ods (25),
              dswd_4ps_auth (26)
  ----------------------------------------------------------------------------------
  UNDER ALL   OpenSPP: spp_registry, spp_area, spp_vocabulary, spp_security,
              spp_programs, spp_change_request_v2, spp_event_data, spp_case_base, spp_api_v2
```

## Two instances

```
   INSTANCE 1: Registry and operations              INSTANCE 2: Casework
   bundle dswd_4ps_instance1 (1)                    bundle dswd_4ps_instance2 (1)

   registry, area, roles, period                    registry, area, roles, api, auth
   change requests, field limits                      (as dependencies)
   compliance, FDS                                  swdi, swdi_dashboard, swdi_api
   payroll, catch-up, retro, partitions             cms, cms_nas, swdi_cms
   api and its route modules                        portal_api_casework, bridge_client
   portal_api, integration, newgrs, ods
   bridge_server
          |                                                   |
          +---- dswd_4ps_bridge_shared (schemas), card 19 ----+
            the registry is the master; casework looks up and
            imports households, events flow back through jobs

   Single instance: bundle dswd_4ps_starter (1) installs both sides on one database.
```

## Not on a card today

Registry tools and operations: `registry_import`, `export`, `ecr`, `hazard`, `account_creation`, `theme`,
`attachment_hardening`, `post_sql_repair`, `pg_partition`, `swdi_dashboard`, `cms_nas`. Sample data, demo and test-only
modules: 17, listed in the catalogue index.
