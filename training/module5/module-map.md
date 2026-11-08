# Module 5 Module Map (poster)

Print at A1 for the wall and at A4 on the inside cover of the catalogue. It is the first slide of the map block and
stays up all afternoon. Production commit `ad98dac9` (2026-11-06): 66 modules with a manifest. 26 cards cover 38 of
them; the rest are in the catalogue index.

## The process, top to bottom

```
                         DSWD 4Ps on OpenSPP v2 (Odoo 19)

  WHERE       dswd_4ps_area            PSGC regions to barangays, area scoping
  WHO         dswd_4ps_registry        households, members, client status, grantee
  WHO MAY     dswd_4ps_roles           POO / RPMO / NPMO tiers, local and global roles
              dswd_4ps_approval_multi_group, dswd_4ps_approval_flow_data
  WHEN        dswd_4ps_period          monthly periods, working-day calendar
  ----------------------------------------------------------------------------------
  CHANGE      dswd_4ps_change_request  + supporting_docs_data, field_limit
  VERIFY      dswd_4ps_compliance      + fds_operations
  PAY         dswd_4ps_payroll         + catchup_payroll, retro_payroll, pg_partition
  ASSESS      dswd_4ps_swdi            + swdi_dashboard
  MANAGE      dswd_4ps_cms             + swdi_cms, cms_nas
  ----------------------------------------------------------------------------------
  CONNECT     dswd_4ps_api             + api_change_request, api_compliance, api_fds,
                                         api_field_limit, swdi_api, payroll_api,
                                         retro_api, portal_api_base, portal_api,
                                         portal_api_casework
              dswd_4ps_integration, dswd_4ps_newgrs, dswd_4ps_ods, dswd_4ps_auth
  ----------------------------------------------------------------------------------
  UNDER ALL   OpenSPP: spp_registry, spp_area, spp_vocabulary, spp_security,
              spp_programs, spp_change_request_v2, spp_event_data, spp_case_base, spp_api_v2
```

## Two instances

```
   INSTANCE 1: Registry and operations              INSTANCE 2: Casework
   bundle dswd_4ps_instance1                        bundle dswd_4ps_instance2

   registry, area, roles, period                    registry, area, roles, api, auth
   change requests, field limits                      (as dependencies)
   compliance, FDS                                  swdi, swdi_dashboard, swdi_api
   payroll, catch-up, retro, partitions             cms, cms_nas, swdi_cms
   api and its route modules                        portal_api_casework, bridge_client
   portal_api, integration, newgrs, ods
   bridge_server
          |                                                   |
          +---------- dswd_4ps_bridge_shared (schemas) -------+
            the registry is the master; casework looks up and
            imports households, events flow back through jobs

   Single instance: bundle dswd_4ps_starter installs both sides on one database.
```

## Not on a card today

Registry tools and operations: `registry_import`, `export`, `ecr`, `hazard`, `account_creation`, `theme`,
`attachment_hardening`, `post_sql_repair`, `pg_partition`, `swdi_dashboard`, `cms_nas`. Sample data, demo and test-only
modules: 17, listed in the catalogue index.
