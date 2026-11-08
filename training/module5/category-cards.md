# Module 5 Category Cards

Print one set per pair: eight cards, one colour each, A6 or larger, the letter large enough to read from the front of
the room. Before the back of a module card is shown, the trainer reads a one-line symptom; each pair holds up the card
for the component they would open first. The same letters are used on the triage sheet.

| Card | Colour | Component                     | Open first                                                 | Guide        |
| ---- | ------ | ----------------------------- | ---------------------------------------------------------- | ------------ |
| M    | Blue   | Model                         | `models/*.py`: fields, constraints, overrides              | 3.7, 3.8     |
| V    | Green  | View                          | `views/*.xml`: list, form, search, inherited views, JS     | 3.9, 4.7-4.8 |
| D    | Yellow | Data or vocabulary            | `data/*.xml`: vocabulary codes, types, approval rules      | 4.4, 4.13    |
| S    | Red    | Security                      | `security/*`: groups, access rows, record rules            | 3.11-3.12    |
| W    | Purple | Wizard                        | `wizards/*.py` and their views: multi-step user actions    | 3.10         |
| J    | Orange | Job (cron or background work) | `data/ir_cron.xml`, `with_delay()` callers, queue channels | 3.17         |
| A    | Grey   | API                           | `routers/`, `services/`, `schemas/`, client scopes         | Module 5     |
| T    | White  | Test                          | `tests/*.py`: what the module promises                     | 3.13, 4.10   |

## The front of each card

```
+-------------------------------+
|                               |
|               M               |
|                               |
|             Model             |
|   models/*.py: fields,        |
|   constraints, overrides      |
|                               |
+-------------------------------+
```

## The rule when two cards fit

Hold up the card for the file you would open first, not the file the fix ends in. A missing access is often found in a
model's error message but fixed in `security/`: the answer is S. A field missing from a form may need a model and a
view: if the field exists in the database, the answer is V.
