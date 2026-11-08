# Module 3 Command Card

Keep this next to the keyboard. Every command runs in your repository folder (`dswd-4ps-modules`). On Windows PowerShell
write `.\odoo-project` instead of `./odoo-project`.

| When                                                | Run                                                                          |
| --------------------------------------------------- | ---------------------------------------------------------------------------- |
| Before the session                                  | `./odoo-project start`                                                       |
| The page is unstyled or `doctor` complains          | `./odoo-project doctor`, fix what it says, then `./odoo-project resetassets` |
| "Install now" (the IT asset register)               | `./odoo-project install dswd_asset`                                          |
| Something changed in a module you already installed | `./odoo-project update`                                                      |
| You changed Python and run the default profile      | `./odoo-project restart`                                                     |
| Odoo said something you did not understand          | `./odoo-project logs`                                                        |
| "Run the tests"                                     | `./odoo-project test dswd_asset`                                             |
| End of the day                                      | `./odoo-project stop`                                                        |

Three lines to recognise in `logs`:

```
Loading module dswd_asset                               the module was found and is being installed
The models ['dswd.asset'] have no access rules          a new model with no row in ir.model.access.csv
odoo.tools.convert.ParseError: while parsing ...        a data or view file is wrong; the path and line follow
```

Login: `admin` / `admin`. Developer mode: Settings > scroll to the bottom > Activate the developer mode.
