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

<!-- _footer: "Guide 6.2" -->

## Before 8:30

Open PowerShell in your repository. Log in once the stack is up; wait for `0 failed, 0 error(s) of 5 tests`; then create the morning's branch.

```powershell
.\odoo-project start
.\odoo-project test dswd_wellbeing
git switch main
git pull
git switch -c module6
```

No working laptop? Sit with a pair that has one.

---

<!-- _footer: "Guide 6.3" -->

## Three modules, one per skill

| #   | Skill         | Module             | The 4Ps request                      | Copy from        |
| --- | ------------- | ------------------ | ------------------------------------ | ---------------- |
| 1   | Development   | `dswd_fds_session` | Register of FDS sessions             | `dswd_asset`     |
| 2   | Extending     | `dswd_listahanan`  | Unique Listahanan ID per household   | `dswd_wellbeing` |
| 3   | Customization | `dswd_id_types`    | PhilSys ID type, with a format check | `dswd_wellbeing` |

---

<!-- _footer: "Guide 6.2, 6.4, 7.4" -->

## Done means three proofs

1. `.\odoo-project install <module>` prints `Install complete. Restarting Odoo...`
2. `.\odoo-project test <module>` prints `0 failed`
3. You can show the result on screen

Read every output to the end: no "complete" line means it failed, and the browser still shows the old screens.

After each exercise: `git add <module>` (its folder), `git status`, `git commit`.

Pairs: one types, one reads; swap at each exercise. Ask your pair, your row, a helper, then me.

---

<!-- _footer: "Guide 6.3 · Exercise 1" -->

## Exercise 1, development: 8:35 to 9:15

`dswd_fds_session`: topic, date, barangay, facilitator, attendees. The number of attendees cannot be negative.

Copy `dswd_asset`, remove what you do not need, rename every `asset`.

Done: install complete, `0 failed, 0 error(s) of 2 tests`, the **FDS Sessions** tile, a session saved and `-3` attendees refused.

---

<!-- _footer: "Guide 6.5" -->

## When something goes wrong

Three habits cover most errors; each sheet's last table has the rest.

- **Find the first line that names your module.** Read a traceback from the bottom up (guide 4.11).
- **`CRITICAL` is the symptom.** Open the full log named on the last lines and search for `Error`.
- **A copied module keeps its names.** Search the new folder for the old name (right-click, Find in Folder).

---

<!-- _footer: "Guide 6.3 · Exercise 2" -->

## Exercise 2, extending: 9:15 to 9:45

`dswd_listahanan`: a Listahanan ID on the household. No two households share one.

Copy `dswd_wellbeing`, remove the vocabulary, keep the parent view and the anchor.

Done: install complete, `0 failed, 0 error(s) of 3 tests`, the **Listahanan** section on a household, a duplicate refused on screen.

---

<!-- _footer: "Guide 6.3 · Exercise 3" -->

## Exercise 3, customization: 9:45 to 10:00

`dswd_id_types`: PhilSys in OpenSPP's ID Type list, with `^\d{4}-\d{4}-\d{4}-\d{4}$`. No model, no view.

Done: install complete, `0 failed, 0 error(s) of 2 tests`, `12345678` refused on the Identity page.

Finish it afterwards if time runs out: the sheet is complete.

---

<!-- _footer: "Guide 6.4, 7.4 · Exercise 3, step 7" -->

## 9:55: push and open the pull request

Whatever exercise you are on: commit what works, then

```powershell
git push -u origin module6
```

Open the link it prints, create the pull request, answer the template's headings.

Finish an exercise later? Commit it and `git push` again: the pull request updates itself.

CI builds the image first, so it ends after the session. When green: merge, delete the branch, `git switch main`, `git pull`, `git branch -d module6` (7.4, steps 12 to 15).

---

<!-- _footer: "Guide 6.3" -->
<!-- _class: lead -->

# Discussion

Development, extending, customization: which one is the everyday work for 4Ps?

---

<!-- _footer: "Guide 6.6" -->

## After the training

The three modules are yours: once CI is green, merge the pull request and bring your laptop up to date (7.4, steps 14 and 15).

Each one has a production counterpart you can now read:

| Your module        | In production                                                     |
| ------------------ | ----------------------------------------------------------------- |
| `dswd_fds_session` | FDS operations module (Module 5, card 12)                         |
| `dswd_listahanan`  | Listahanan ID on the registry (card 3)                            |
| `dswd_id_types`    | PhilSys, 4Ps ID card, PhilHealth ID types: registry data (card 3) |
