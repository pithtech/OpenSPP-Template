# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
{
    "name": "DSWD Training: IT Asset Register",
    "summary": "A plain Odoo module built from scratch in Module 3: an IT asset register",
    "category": "DSWD 4Ps/Training",
    "version": "19.0.1.0.0",
    "author": "DSWD",
    "website": "https://github.com/pithtech/OpenSPP-Template",
    "license": "LGPL-3",
    "development_status": "Alpha",
    "maintainers": [],
    "depends": [
        "base",
        "spp_security",
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/dswd_asset_views.xml",
        "views/menus.xml",
        "report/dswd_asset_report.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
