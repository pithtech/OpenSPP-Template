---
marp: true
theme: default
paginate: true
size: 16:9
title: "Module 6: Hands-on Activity"
style: |
  section pre { font-size: 0.7em; }
  section table { font-size: 0.8em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 6

## Hands-on Activity: three modules of your own

OpenSPP and Odoo Foundations Training, Day 3, 8:30 to 10:30

Edwin Gonzales, OpenSPP

---

## Before 8:30

Open PowerShell in your repository.

```powershell
.\odoo-project start
.\odoo-project test dswd_wellbeing
```

Log in. Wait for `0 failed`. No working laptop? Sit with a pair that has one.

---

## Three modules, one per skill

| #   | Skill         | Module             | The 4Ps request                            | Copy from        |
| --- | ------------- | ------------------ | ------------------------------------------ | ---------------- |
| 1   | Development   | `dswd_fds_session` | A register of Family Development Sessions  | `dswd_asset`     |
| 2   | Extending     | `dswd_listahanan`  | A unique Listahanan ID on every household  | `dswd_wellbeing` |
| 3   | Customization | `dswd_id_types`    | PhilSys as an ID type, with a format check | `dswd_wellbeing` |

---

## Done means three proofs

1. `.\odoo-project install <module>` ends with `Install complete. Restarting Odoo...`
2. `.\odoo-project test <module>` ends with `0 failed`
3. You can show it on screen

Read every output to the end. If it does not say complete, it failed, and the browser still shows the old screens.

Pairs: one types, one reads. Swap at each exercise. Ask your pair, your row, a helper, then me.

---

## Exercise 1, development: 8:35 to 9:15

`dswd_fds_session`: topic, date, barangay, facilitator, attendees. The number of attendees cannot be negative.

Copy `dswd_asset`, remove what you do not need, rename every `asset`.

Done: install complete, `0 failed, 0 error(s) of 2 tests`, the **FDS Sessions** tile.

---

## Exercise 2, extending: 9:15 to 9:45

`dswd_listahanan`: a Listahanan ID on the household. No two households share one.

Copy `dswd_wellbeing`, remove the vocabulary, keep the parent view and the anchor.

Done: install complete, `0 failed, 0 error(s) of 3 tests`, a duplicate refused on screen.

---

## Exercise 3, customization: 9:45 to 10:00

`dswd_id_types`: PhilSys in OpenSPP's ID Type list, with `^\d{4}-\d{4}-\d{4}-\d{4}$`. No model, no view.

Done: install complete, `0 failed, 0 error(s) of 2 tests`, `12345678` refused on the Identity page.

Finish it afterwards if time runs out: the sheet is complete.

---

## When `test` prints only `CRITICAL`

`Failed to load registry` or `Couldn't load module` is the symptom, not the cause.

Open the full log named on the last lines and search for `Error`.

The first line that names a file in **your** module is where to look.

---

<!-- _class: lead -->

# Discussion

Development, extending, customization: which one is the everyday work for 4Ps?
