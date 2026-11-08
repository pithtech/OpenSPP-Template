# Module 4 Troubleshooting Drill

Work in pairs. For each excerpt, write down (1) which file in `dswd_wellbeing` you open, (2) what you compare it against
or look for, and (3) the one-line fix. You have 12 minutes for the three. These are real log lines from
`./odoo-project test dswd_wellbeing`.

---

## Excerpt A

```
ERROR odoo.registry: Failed to load registry
CRITICAL odoo.service.server: Failed to initialize database `test_dswd_wellbeing_8059428`.
Traceback (most recent call last):
  File "/opt/odoo/odoo/odoo/orm/fields_selection.py", line 235, in convert_to_cache
    raise ValueError("Wrong value for %s: %r" % (self, value))
ValueError: Wrong value for spp.vocabulary.domain: 'administrative'

odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/data/vocabulary_well_being_level.xml:10, somewhere inside
<record id="vocab_well_being_level" model="spp.vocabulary">
        <field name="name">4Ps Well-Being Level</field>
        <field name="namespace_uri">urn:dswd:4ps:well-being-level</field>
        <field name="is_system" eval="True"/>
        <field name="domain">administrative</field>
    </record>
```

|                            |     |
| -------------------------- | --- |
| File to open               |     |
| Compare against / look for |     |
| Fix                        |     |

## Excerpt B

```
INFO odoo.modules.loading: loading dswd_wellbeing/views/res_partner_views.xml
ERROR odoo.registry: Failed to load registry
odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/views/res_partner_views.xml:8
Error while parsing or validating view:

Element '<xpath expr="//group[@name='group_tag_section']">' cannot be located in parent view

View error context:
{'file': '/mnt/extra-addons/custom/dswd_wellbeing/views/res_partner_views.xml',
 'name': 'res.partner.form.dswd.wellbeing',
 'view.model': 'res.partner',
 'xmlid': 'view_res_partner_form_wellbeing'}
```

|                            |     |
| -------------------------- | --- |
| File to open               |     |
| Compare against / look for |     |
| Fix                        |     |

## Excerpt C

```
INFO odoo.modules.loading: Loading module dswd_wellbeing (40/44)
INFO odoo.modules.loading: loading dswd_wellbeing/security/ir.model.access.csv
INFO odoo.modules.loading: loading dswd_wellbeing/views/res_partner_views.xml
INFO odoo.modules.loading: Module dswd_wellbeing loaded in 0.07s, 120 queries (+120 other)
ERROR odoo.addons.dswd_wellbeing.tests.test_wellbeing: FAIL: TestWellBeingVocabulary.test_three_levels_in_swdi_order
  File "/mnt/extra-addons/custom/dswd_wellbeing/tests/test_wellbeing.py", line 23, in test_three_levels_in_swdi_order
    self.assertTrue(all(codes), "every level must resolve by namespace and code")
AssertionError: False is not true : every level must resolve by namespace and code
ERROR odoo.tests.result: 3 failed, 0 error(s) of 5 tests when loading database 'test_dswd_wellbeing_8427324'
```

Hint: the module loaded "cleanly". Count the files it loaded.

|                            |     |
| -------------------------- | --- |
| File to open               |     |
| Compare against / look for |     |
| Fix                        |     |

## Bonus excerpt D (if your pair finishes early)

```
INFO odoo.modules.loading: loading dswd_wellbeing/views/res_partner_views.xml
ERROR odoo.registry: Failed to load registry
odoo.tools.convert.ParseError: while parsing /mnt/extra-addons/custom/dswd_wellbeing/views/res_partner_views.xml:8
Field "dswd_well_being_level_id" does not exist in model "res.partner"
```

`models/res_partner.py` defines the field, spelled exactly like that. What is wrong, and why did Module 4 step 2 not
show this error?
