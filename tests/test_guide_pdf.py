"""The participant guide's PDF build: the Markdown and HTML transformations around pandoc and WeasyPrint."""

import importlib.util
from pathlib import Path

BUILD = Path(__file__).parent.parent / "scripts" / "guide_pdf" / "build.py"


def _load():
    spec = importlib.util.spec_from_file_location("guide_pdf_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUIDE = """# OpenSPP and Odoo Foundations Training: Participant Guide

The guide's introduction.

Contents:

- [0. Before you start](#0-before-you-start)
- [7. Reference](#7-reference)

---

## 0. Before you start

Text.

---

## 7. Reference
"""


def test_title_and_hand_written_contents_are_replaced():
    """The cover replaces the title, the generated contents replace the list, the introduction gets a heading."""
    md = _load().prepare_markdown(GUIDE)
    assert "# OpenSPP and Odoo Foundations Training: Participant Guide" not in md
    assert "Contents:" not in md
    assert "(#0-before-you-start)" not in md
    assert md.startswith("## About this guide\n\nThe guide's introduction.")
    assert "## 0. Before you start" in md
    assert "## 7. Reference" in md


def test_chapter_separators_are_dropped():
    """Chapters start on a new page in print, so the horizontal rules between them go."""
    md = _load().prepare_markdown(GUIDE)
    assert "\n---\n" not in md


def test_only_long_code_blocks_may_break_across_pages():
    """A short block stays on one page; a block longer than the limit is marked so it may break."""
    build = _load()
    short = "<pre><code>a\nb\n</code></pre>"
    long_block = "<pre><code>" + "line\n" * (build.LONG_CODE_LINES + 1) + "</code></pre>"
    html = build.mark_long_code_blocks(short + long_block)
    assert html.count('<pre class="long">') == 1
    assert html.startswith("<pre><code>a")


def test_pandoc_class_attributes_are_kept_when_marking():
    """Pandoc writes language classes on some blocks; marking a long one keeps them."""
    build = _load()
    block = '<pre class="sourceCode python"><code>' + "x\n" * (build.LONG_CODE_LINES + 1) + "</code></pre>"
    html = build.mark_long_code_blocks(block)
    assert '<pre class="sourceCode python long">' in html


def test_wide_code_blocks_get_a_font_size_that_fits_their_longest_line():
    """A block wider than the page gets a smaller font so its lines do not wrap; a narrow one keeps the default."""
    build = _load()
    narrow = "<pre><code>short line\n</code></pre>"
    wide_line = "x" * (build.FIT_CHARS + 20)
    wide = f'<pre class="long"><code>{wide_line}\n</code></pre>'
    html = build.fit_wide_code_blocks(narrow + wide)
    assert html.startswith("<pre><code>short line")
    sized = html[len(narrow) :]
    assert sized.startswith('<pre class="long" style="font-size: ')
    size = float(sized.split("font-size: ")[1].split("pt")[0])
    assert build.MIN_CODE_PT <= size < build.CODE_PT


def test_wide_code_counts_characters_not_html_entities():
    """`&lt;` is one character on the page, so a line of entities is measured as the text it shows."""
    build = _load()
    line = "&lt;" * (build.FIT_CHARS - 5)
    assert build.fit_wide_code_blocks(f"<pre><code>{line}</code></pre>") == f"<pre><code>{line}</code></pre>"


def test_inline_code_does_not_break_at_a_hyphen_or_backslash():
    """`--profile` and `.\\odoo-project` stay whole; code inside a block is left alone."""
    build = _load()
    html = build.keep_inline_code_tokens_whole(
        "<p><code>start --profile dev</code> and <code>.\\odoo-project update</code></p>"
        "<pre><code>a --b</code></pre>"
    )
    assert '<span class="nobr">--profile</span>' in html
    assert '<span class="nobr">.\\odoo-project</span>' in html
    assert "<code>start " in html and " dev</code>" in html
    assert "<pre><code>a --b</code></pre>" in html
