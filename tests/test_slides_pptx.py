"""The PowerPoint build of the training decks: training/moduleN/slides.md -> training/moduleN/slides.pptx."""

import importlib.util
from pathlib import Path

import pytest

pptx = pytest.importorskip("pptx")
pytest.importorskip("markdown_it")

ROOT = Path(__file__).parent.parent
BUILD = ROOT / "scripts" / "slides_pptx" / "build.py"


def _load():
    spec = importlib.util.spec_from_file_location("slides_pptx_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DECK = r"""---
marp: true
theme: default
paginate: true
title: "Module 9: Testing"
style: |
  section pre { font-size: 0.7em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Module 9

## A test deck

OpenSPP and Odoo Foundations Training

---

<!-- _footer: "Guide 9.1" -->

<style scoped>ul { font-size: 0.8em; }</style>

## By ten you can

1. Read a **model** and its `_name`.
2. Run _the tests_.

- A bullet
  - A nested bullet

---

<!-- _footer: "Guide 9.2" -->

## Code and a table

```python
class Asset(models.Model):
    _name = "dswd.asset"
```

| Part  | Says        |
| ----- | ----------- |
| `a\|b` | **bold** it |

---

<!-- _class: lead -->
<!-- _footer: "Guide 9.3" -->

# A section

Between topics
"""


def test_slides_are_split_and_directives_read():
    deck = _load().parse_deck(DECK)
    assert deck.title == "Module 9: Testing"
    assert [s.kind for s in deck.slides] == ["cover", "content", "content", "section"]
    assert [s.footer for s in deck.slides] == ["", "Guide 9.1", "Guide 9.2", "Guide 9.3"]
    assert [s.paginate for s in deck.slides] == [False, True, True, True]
    assert [s.title for s in deck.slides] == ["Module 9", "By ten you can", "Code and a table", "A section"]


def test_blocks_lists_and_inline_runs():
    build = _load()
    slide = build.parse_deck(DECK).slides[1]
    numbered, bullets = slide.blocks
    assert isinstance(numbered, build.ListBlock) and numbered.ordered and numbered.start == 1
    first = numbered.items[0].runs
    assert [(r.text, r.bold, r.code) for r in first] == [
        ("Read a ", False, False),
        ("model", True, False),
        (" and its ", False, False),
        ("_name", False, True),
        (".", False, False),
    ]
    assert numbered.items[1].runs[1].italic
    assert not bullets.ordered
    assert bullets.items[0].children[0].items[0].runs[0].text == "A nested bullet"


def test_scoped_styles_and_directives_are_not_content():
    slide = _load().parse_deck(DECK).slides[1]
    text = " ".join(run.text for block in slide.blocks for item in block.items for run in item.runs)
    assert "font-size" not in text and "_footer" not in text


def test_code_and_table_blocks():
    build = _load()
    code, table = build.parse_deck(DECK).slides[2].blocks
    assert isinstance(code, build.CodeBlock)
    assert code.language == "python"
    assert code.text.splitlines() == ["class Asset(models.Model):", '    _name = "dswd.asset"']
    assert isinstance(table, build.TableBlock)
    assert [build.plain(cell) for cell in table.header] == ["Part", "Says"]
    assert [build.plain(cell) for cell in table.rows[0]] == ["a|b", "bold it"]


def test_image_height_comes_from_the_marp_directive(tmp_path):
    build = _load()
    deck = build.parse_deck("---\nmarp: true\n---\n\n## Shot\n\n![h:470](images/shot.png)\n")
    (image,) = deck.slides[0].blocks
    assert isinstance(image, build.ImageBlock)
    assert image.path == "images/shot.png" and image.height_px == 470


def _texts(slide):
    return [shape.text_frame.text for shape in slide.shapes if shape.has_text_frame]


def test_built_deck_has_one_slide_per_source_slide_with_footers(tmp_path):
    build = _load()
    prs = build.build_deck(build.parse_deck(DECK), base=tmp_path)
    assert len(prs.slides) == 4
    assert "Guide 9.1" in _texts(prs.slides[1])
    assert "2" in _texts(prs.slides[1])  # the slide number
    assert not any(t == "1" for t in _texts(prs.slides[0]))  # the cover has no number


def test_code_is_set_in_consolas_at_a_readable_size(tmp_path):
    build = _load()
    prs = build.build_deck(build.parse_deck(DECK), base=tmp_path)
    runs = [
        run
        for shape in prs.slides[2].shapes
        if shape.has_text_frame
        for p in shape.text_frame.paragraphs
        for run in p.runs
        if run.font.name == build.CODE_FONT
    ]
    assert runs, "no code runs on the code slide"
    assert all(run.font.size.pt >= build.MIN_CODE_PT for run in runs)


def test_a_code_block_over_the_line_limit_fails_the_build(tmp_path):
    build = _load()
    code = "\n".join(f"line_{n} = {n}" for n in range(build.MAX_CODE_LINES + 1))
    deck = build.parse_deck(f"---\nmarp: true\n---\n\n## Too long\n\n```python\n{code}\n```\n")
    with pytest.raises(build.FitError, match="slide 1"):
        build.build_deck(deck, base=tmp_path)


def test_a_code_line_too_wide_at_the_smallest_size_fails_the_build(tmp_path):
    build = _load()
    deck = build.parse_deck("---\nmarp: true\n---\n\n## Wide\n\n```\n" + "x" * 140 + "\n```\n")
    with pytest.raises(build.FitError, match="slide 1"):
        build.build_deck(deck, base=tmp_path)


def test_a_slide_with_more_than_fits_fails_the_build(tmp_path):
    build = _load()
    body = "\n".join(f"- Item number {n} with some words to fill the line" for n in range(40))
    deck = build.parse_deck(f"---\nmarp: true\n---\n\n## Crowded\n\n{body}\n")
    with pytest.raises(build.FitError, match="slide 1"):
        build.build_deck(deck, base=tmp_path)


def test_lenient_build_reports_instead_of_failing(tmp_path):
    build = _load()
    code = "\n".join(f"line_{n} = {n}" for n in range(build.MAX_CODE_LINES + 3))
    deck = build.parse_deck(f"---\nmarp: true\n---\n\n## Too long\n\n```python\n{code}\n```\n")
    problems = []
    prs = build.build_deck(deck, base=tmp_path, problems=problems)
    assert len(prs.slides) == 1
    assert problems and "slide 1" in problems[0]


NOTES = """# Lecture notes

Intro.

---

### Slide 1: Module 9

Guide: none

- **Say:** Nothing.

### Slide 2: By ten you can

- **Say:** The `two` objectives.

### Slide 3: Code and a table

- **Do:** Open the file.

### Slide 4: A section

- **Say:** Next topic.
"""


def test_lecture_notes_become_speaker_notes(tmp_path):
    build = _load()
    deck = build.parse_deck(DECK)
    notes = build.parse_notes(NOTES)
    prs = build.build_deck(deck, base=tmp_path, notes=notes)
    text = prs.slides[1].notes_slide.notes_text_frame.text
    assert "Say: The two objectives." in text


def test_notes_whose_titles_do_not_match_the_deck_fail(tmp_path):
    build = _load()
    notes = build.parse_notes(NOTES.replace("Slide 3: Code and a table", "Slide 3: Something else"))
    with pytest.raises(build.NotesError, match="slide 3"):
        build.build_deck(build.parse_deck(DECK), base=tmp_path, notes=notes)


def test_a_slide_without_notes_fails(tmp_path):
    build = _load()
    notes = build.parse_notes(NOTES.split("### Slide 4")[0])
    with pytest.raises(build.NotesError, match="slide 4"):
        build.build_deck(build.parse_deck(DECK), base=tmp_path, notes=notes)


DECKS = [ROOT / "training" / f"module{n}" for n in (3, 4, 5, 6)]


def _all_text(slide):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            texts.append(shape.text_frame.text)
        elif shape.has_table:
            texts.extend(cell.text for row in shape.table.rows for cell in row.cells)
    return texts


def _shape_text(slide, name):
    return next((s.text_frame.text for s in slide.shapes if s.name == name and s.has_text_frame), None)


@pytest.mark.parametrize("folder", DECKS, ids=lambda p: p.name)
class TestRepositoryDecks:
    """The committed PowerPoint decks: built from their slides.md, readable, and without the trainer's notes."""

    def test_source_fits_at_a_readable_size(self, folder):
        build = _load()
        deck = build.parse_deck((folder / "slides.md").read_text(encoding="utf-8"))
        build.build_deck(deck, base=folder)  # raises FitError on a slide that does not fit

    def test_pptx_matches_its_source(self, folder):
        build = _load()
        deck = build.parse_deck((folder / "slides.md").read_text(encoding="utf-8"))
        prs = pptx.Presentation(str(folder / "slides.pptx"))
        assert len(prs.slides) == len(deck.slides), "slides.pptx is out of date: rebuild it"
        fresh = build.build_deck(deck, base=folder)
        for source, built, expected in zip(deck.slides, prs.slides, fresh.slides, strict=False):
            title = _shape_text(built, "Title") or ""
            assert title.startswith(source.title), f"slide {source.number}: {title!r} is not {source.title!r}"
            assert (_shape_text(built, "Footer") or "") == source.footer, f"slide {source.number} footer"
            assert _all_text(built) == _all_text(expected), f"slide {source.number} is out of date: rebuild slides.pptx"

    def test_pptx_has_no_speaker_notes(self, folder):
        prs = pptx.Presentation(str(folder / "slides.pptx"))
        noted = [
            n
            for n, slide in enumerate(prs.slides, 1)
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip()
        ]
        assert noted == [], f"speaker notes belong only in the trainer's private copies: slides {noted}"


def test_a_long_title_takes_two_lines_and_pushes_the_body_down(tmp_path):
    build = _load()
    title = "Compliance: the job retries on a busy lock, then marks the household (3.17)"
    deck = build.parse_deck(f"---\nmarp: true\n---\n\n## {title}\n\nA paragraph.\n\n---\n\n## Short\n\nA paragraph.\n")
    prs = build.build_deck(deck, base=tmp_path)
    tops = []
    for slide in prs.slides:
        heading = next(s for s in slide.shapes if s.name == "Title")
        body = next(s for s in slide.shapes if s.name == "Text")
        assert body.top >= heading.top + heading.height, "the body starts under the title"
        tops.append(body.top)
    assert tops[0] > tops[1]
