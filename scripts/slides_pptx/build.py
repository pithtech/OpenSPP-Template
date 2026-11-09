#!/usr/bin/env python3
# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
"""Build the training decks as PowerPoint: training/moduleN/slides.md -> training/moduleN/slides.pptx.

The Marp Markdown stays the source. This script reads it (front matter, `---` slides, the `_class: lead`, `_footer` and
`_paginate` directives, headings, paragraphs, lists, tables, code and images) and lays each slide out in the colours of
the participant guide's PDF. `<style scoped>` blocks are ignored: sizes are set here.

Fit is checked, not hoped for: a code block over MAX_CODE_LINES lines, a code line too wide at MIN_CODE_PT, or a slide
whose content is taller than the body area fails the build with the slide number. The fix belongs in slides.md.

    uv run python scripts/slides_pptx/build.py                 # all four decks, into training/moduleN/slides.pptx
    uv run python scripts/slides_pptx/build.py 4               # Module 4 only
    uv run python scripts/slides_pptx/build.py --lenient       # report fit problems instead of failing
    uv run python scripts/slides_pptx/build.py --notes DIR --out DIR
        # the trainer's copies: DIR/moduleN-lecture-notes.md as speaker notes, written to the --out folder
"""

import argparse
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from markdown_it import MarkdownIt
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
MODULES = (3, 4, 5, 6)

# Colours of the guide PDF (scripts/guide_pdf/print.css), from the DSWD and 4Ps logos.
DSWD_BLUE = RGBColor(0x19, 0x49, 0x98)
NAVY = RGBColor(0x00, 0x37, 0x61)
RED = RGBColor(0xEC, 0x20, 0x2B)
YELLOW = RGBColor(0xFD, 0xC2, 0x2D)
TEXT = RGBColor(0x1F, 0x2A, 0x37)
MUTED = RGBColor(0x5F, 0x6B, 0x7A)
CODE_INK = RGBColor(0x0F, 0x5F, 0xA8)
CODE_BG = RGBColor(0xF6, 0xF8, 0xFB)
RULE = RGBColor(0xD5, 0xDD, 0xE8)
ZEBRA = RGBColor(0xF6, 0xF8, 0xFB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xC9, 0xD8, 0xEA)

TEXT_FONT = "Arial"
CODE_FONT = "Consolas"

# Slide geometry, in inches (16:9).
SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN_X = 0.6
TITLE_TOP = 0.35
TITLE_H = 0.85
BODY_TOP = 1.35
BODY_BOTTOM = 6.8
BODY_W = SLIDE_W - 2 * MARGIN_X
GAP = 0.14
FOOTER_TOP = 6.95

TITLE_PT = 32
BODY_SIZES = (20, 18, 16)  # tried in turn until the slide fits
CODE_PT = 16
MIN_CODE_PT = 14
MAX_CODE_LINES = 14
FOOTER_PT = 12

# Average advance per character, in ems. Mono is the widest common monospace (Courier New, Menlo), so code that fits
# here fits in Consolas and wherever Consolas is replaced.
TEXT_ADVANCE = 0.5
MONO_ADVANCE = 0.6
LINE = 1.2
CODE_LINE = 1.2
CODE_PAD = 0.12
LIST_INDENT = 0.4
CELL_PAD = 0.08
WRAP_SLACK = 1.08  # lines break at word boundaries, so a line holds a little less than its full width

MARP_IMAGE_PX_PER_INCH = 96  # a Marp slide is 1280 x 720 px on 13.333 x 7.5 in


class FitError(Exception):
    """A slide's content does not fit at a readable size."""


class NotesError(Exception):
    """The lecture notes do not match the deck."""


# --- Parsing ------------------------------------------------------------------------------------------------------


@dataclass
class Run:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False


@dataclass
class Paragraph:
    runs: list


@dataclass
class Heading:
    level: int
    runs: list


@dataclass
class ListItem:
    runs: list
    children: list = field(default_factory=list)


@dataclass
class ListBlock:
    ordered: bool
    start: int
    items: list


@dataclass
class CodeBlock:
    language: str
    text: str


@dataclass
class TableBlock:
    header: list
    rows: list


@dataclass
class ImageBlock:
    path: str
    height_px: int


@dataclass
class Slide:
    number: int
    kind: str  # cover, section or content
    footer: str
    paginate: bool
    title: str
    title_runs: list
    blocks: list


@dataclass
class Deck:
    title: str
    slides: list


DIRECTIVE = re.compile(r"<!--\s*(_?)(class|footer|paginate)\s*:\s*(.*?)\s*-->")
STYLE = re.compile(r"<style[^>]*>.*?</style>", re.S)
FRONT_KEY = re.compile(r'^(\w+):\s*"?(.*?)"?\s*$')


def plain(runs):
    return "".join(run.text for run in runs)


def _split(text):
    """Front matter and the slides' source, split at `---` lines outside code fences."""
    lines = text.splitlines()
    front = {}
    if lines and lines[0].strip() == "---":
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        for line in lines[1:end]:
            match = FRONT_KEY.match(line)
            if match:
                front[match.group(1)] = match.group(2)
        lines = lines[end + 1 :]
    slides, current, fence = [], [], None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else (fence or marker)
        if stripped == "---" and fence is None:
            slides.append("\n".join(current))
            current = []
        else:
            current.append(line)
    slides.append("\n".join(current))
    return front, [s for s in slides if s.strip()]


def _inline(token):
    runs, bold, italic = [], 0, 0
    for child in token.children or []:
        kind = child.type
        if kind == "text":
            runs.append(Run(child.content, bold > 0, italic > 0))
        elif kind == "code_inline":
            runs.append(Run(child.content, bold > 0, italic > 0, code=True))
        elif kind == "strong_open":
            bold += 1
        elif kind == "strong_close":
            bold -= 1
        elif kind == "em_open":
            italic += 1
        elif kind == "em_close":
            italic -= 1
        elif kind in ("softbreak",):
            runs.append(Run(" ", bold > 0, italic > 0))
        elif kind == "hardbreak":
            runs.append(Run("\n", bold > 0, italic > 0))
        elif kind == "html_inline" and child.content.lower().startswith("<br"):
            runs.append(Run("\n"))
    merged = []
    for run in runs:
        if merged and (merged[-1].bold, merged[-1].italic, merged[-1].code) == (run.bold, run.italic, run.code):
            merged[-1].text += run.text
        else:
            merged.append(run)
    return merged


def _image(token):
    """A paragraph holding only an image, as an ImageBlock; None otherwise."""
    children = [c for c in token.children or [] if not (c.type == "text" and not c.content.strip())]
    if len(children) == 1 and children[0].type == "image":
        image = children[0]
        alt = image.content or "".join(c.content for c in image.children or [])
        match = re.search(r"h:(\d+)", alt)
        return ImageBlock(image.attrGet("src"), int(match.group(1)) if match else 470)
    return None


def _blocks(tokens, start, stop_type=None):
    """Blocks from tokens[start:], until a token of stop_type; returns (blocks, next index)."""
    blocks, i = [], start
    while i < len(tokens):
        token = tokens[i]
        if stop_type and token.type == stop_type:
            return blocks, i
        if token.type == "heading_open":
            blocks.append(Heading(int(token.tag[1]), _inline(tokens[i + 1])))
            i += 3
        elif token.type == "paragraph_open":
            image = _image(tokens[i + 1])
            blocks.append(image or Paragraph(_inline(tokens[i + 1])))
            i += 3
        elif token.type in ("bullet_list_open", "ordered_list_open"):
            block, i = _list(tokens, i)
            blocks.append(block)
        elif token.type in ("fence", "code_block"):
            blocks.append(CodeBlock((token.info or "").strip(), token.content.rstrip("\n")))
            i += 1
        elif token.type == "table_open":
            block, i = _table(tokens, i)
            blocks.append(block)
        elif token.type == "blockquote_open":
            inner, i = _blocks(tokens, i + 1, "blockquote_close")
            blocks.extend(inner)
            i += 1
        else:
            i += 1  # html blocks (directives, styles), rules
    return blocks, i


def _list(tokens, i):
    open_token = tokens[i]
    ordered = open_token.type == "ordered_list_open"
    close = "ordered_list_close" if ordered else "bullet_list_close"
    start = int(open_token.attrGet("start") or 1)
    items, i = [], i + 1
    while tokens[i].type != close:
        if tokens[i].type == "list_item_open":
            inner, i = _blocks(tokens, i + 1, "list_item_close")
            runs, children = [], []
            for block in inner:
                if isinstance(block, Paragraph) and not runs:
                    runs = block.runs
                elif isinstance(block, Paragraph):
                    runs = runs + [Run(" ")] + block.runs
                elif isinstance(block, ListBlock):
                    children.append(block)
                elif isinstance(block, CodeBlock):
                    runs = runs + [Run(" " + block.text, code=True)]
            items.append(ListItem(runs, children))
        i += 1
    return ListBlock(ordered, start, items), i + 1


def _table(tokens, i):
    header, rows, row, in_head = [], [], None, False
    while tokens[i].type != "table_close":
        kind = tokens[i].type
        if kind == "thead_open":
            in_head = True
        elif kind == "thead_close":
            in_head = False
        elif kind == "tr_open":
            row = []
        elif kind == "tr_close":
            (header if in_head else rows).append(row)
        elif kind == "inline":
            row.append(_inline(tokens[i]))
        i += 1
    return TableBlock(header[0] if header else [], rows), i + 1


def parse_deck(text):
    front, sources = _split(text)
    md = MarkdownIt("commonmark").enable("table")
    deck_paginate = front.get("paginate", "false") == "true"
    slides = []
    for number, source in enumerate(sources, start=1):
        directives = {name: value.strip('"') for _, name, value in DIRECTIVE.findall(source)}
        body = STYLE.sub("", DIRECTIVE.sub("", source))
        blocks, _ = _blocks(md.parse(body), 0)
        title_runs = []
        if blocks and isinstance(blocks[0], Heading):
            title_runs = blocks.pop(0).runs
        lead = directives.get("class") == "lead"
        kind = "content" if not lead else ("cover" if number == 1 else "section")
        paginate = deck_paginate and directives.get("paginate", "true") != "false"
        slides.append(
            Slide(number, kind, directives.get("footer", ""), paginate, plain(title_runs), title_runs, blocks)
        )
    return Deck(front.get("title", ""), slides)


# --- Lecture notes ------------------------------------------------------------------------------------------------

NOTE_HEADING = re.compile(r"^### Slide (\d+): (.*)$", re.M)


def parse_notes(text):
    """{slide number: (title, notes text)} from a lecture-notes file's `### Slide N: Title` entries."""
    entries = {}
    matches = list(NOTE_HEADING.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        body = re.split(r"^(?:---|## )", body, flags=re.M)[0]
        entries[int(match.group(1))] = (match.group(2).strip(), _notes_text(body))
    return entries


def _notes_text(body):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", body)
    text = text.replace("`", "")
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def _normal(title):
    return re.sub(r"\s+", " ", title.replace("`", "").replace("*", "")).strip().lower()


# --- Measuring ----------------------------------------------------------------------------------------------------


def _text_width(runs, pt):
    """Width in inches of runs set on one line at pt."""
    width = 0.0
    for run in runs:
        advance = MONO_ADVANCE if run.code else TEXT_ADVANCE
        width += len(run.text) * advance * pt / 72
    return width


def _lines(runs, pt, width):
    pieces = plain(runs).split("\n")
    total = 0
    for index, _ in enumerate(pieces):
        part = [Run(p) for p in pieces[index : index + 1]] if len(pieces) > 1 else runs
        total += max(1, math.ceil(_text_width(part, pt) * WRAP_SLACK / width))
    return total


def _text_height(runs, pt, width):
    return _lines(runs, pt, width) * pt * LINE / 72


def _code_size(block, slide_number):
    lines = block.text.splitlines() or [""]
    if len(lines) > MAX_CODE_LINES:
        raise FitError(f"slide {slide_number}: code block has {len(lines)} lines (at most {MAX_CODE_LINES})")
    longest = max(len(line) for line in lines)
    for pt in range(CODE_PT, MIN_CODE_PT - 1, -1):
        if longest * MONO_ADVANCE * pt / 72 + 2 * CODE_PAD <= BODY_W:
            return pt
    raise FitError(
        f"slide {slide_number}: a code line of {longest} characters does not fit at {MIN_CODE_PT}pt; wrap or trim it"
    )


def _code_height(block, pt):
    return len(block.text.splitlines() or [""]) * pt * CODE_LINE / 72 + 2 * CODE_PAD


def _table_size(block, pt):
    return max(14, pt - 4)


def _column_widths(block, pt):
    rows = [block.header] + block.rows
    columns = max(len(row) for row in rows)
    needs, floors = [], []
    for col in range(columns):
        cells = [row[col] for row in rows if col < len(row)]
        needs.append(max(_text_width(cell, pt) for cell in cells) + 2 * CELL_PAD + 0.05)
        words = [Run(w, code=r.code) for cell in cells for r in cell for w in r.text.split()]
        floors.append(max((_text_width([w], pt) for w in words), default=0.3) + 2 * CELL_PAD + 0.05)
    total = sum(needs)
    if total <= BODY_W:
        # Tables span the body width; the spare width is shared in proportion to need.
        return [w * BODY_W / total for w in needs]
    # Too wide: every column keeps its longest word, the rest of the width goes in proportion to what is left over.
    spare = BODY_W - sum(floors)
    extra = [n - f for n, f in zip(needs, floors, strict=False)]
    if spare <= 0 or sum(extra) <= 0:
        return [f * BODY_W / sum(floors) for f in floors]
    return [f + spare * e / sum(extra) for f, e in zip(floors, extra, strict=False)]


def _table_height(block, pt):
    widths = _column_widths(block, pt)
    height = 0.0
    for row in [block.header] + block.rows:
        lines = max(_lines(cell, pt, max(widths[c] - 2 * CELL_PAD, 0.3)) for c, cell in enumerate(row))
        height += lines * pt * LINE / 72 + 2 * CELL_PAD
    return height


def _list_height(block, pt, width, depth=0):
    height = 0.0
    for item in block.items:
        height += _text_height(item.runs, pt, width - LIST_INDENT * (depth + 1)) + pt * 0.35 / 72
        for child in item.children:
            height += _list_height(child, pt, width, depth + 1)
    return height


def _image_size(block, base):
    from PIL import Image

    with Image.open(base / block.path) as img:
        w, h = img.size
    height = block.height_px / MARP_IMAGE_PX_PER_INCH
    return height * w / h, height


def _block_height(block, pt, base, slide_number):
    if isinstance(block, Paragraph):
        return _text_height(block.runs, pt, BODY_W) + pt * 0.3 / 72
    if isinstance(block, Heading):
        return _text_height(block.runs, pt + 2, BODY_W) + pt * 0.3 / 72
    if isinstance(block, ListBlock):
        return _list_height(block, pt, BODY_W)
    if isinstance(block, CodeBlock):
        return _code_height(block, _code_size(block, slide_number))
    if isinstance(block, TableBlock):
        return _table_height(block, _table_size(block, pt))
    if isinstance(block, ImageBlock):
        return _image_size(block, base)[1]
    return 0.0


# --- Drawing ------------------------------------------------------------------------------------------------------


def _font(run_font, *, size, color, name=TEXT_FONT, bold=False, italic=False):
    run_font.name = name
    run_font.size = Pt(size)
    run_font.bold = bold
    run_font.italic = italic
    run_font.color.rgb = color


def _write_runs(paragraph, runs, size, color, bold=False):
    for run in runs:
        out = paragraph.add_run()
        out.text = run.text
        if run.code:
            _font(out.font, size=size, color=CODE_INK, name=CODE_FONT, bold=bold or run.bold)
        else:
            _font(out.font, size=size, color=color, bold=bold or run.bold, italic=run.italic)


def _text_box(slide, left, top, width, height, name):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    box.name = name
    frame = box.text_frame
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    return box, frame


def _bullet(paragraph, ordered, number, depth):
    """A hanging indent with a bullet or a number, written into the paragraph's properties."""
    p_pr = paragraph._p.get_or_add_pPr()
    indent = Emu(Inches(LIST_INDENT))
    p_pr.set("marL", str(int(indent * (depth + 1))))
    p_pr.set("indent", str(-int(indent)))
    for tag in ("a:buClr", "a:buNone", "a:buChar", "a:buAutoNum", "a:buFont"):
        for old in p_pr.findall(qn(tag)):
            p_pr.remove(old)
    # The bullet's own colour and font, so an item that starts with code keeps a plain bullet or number.
    colour = p_pr.makeelement(qn("a:buClr"), {})
    colour.append(colour.makeelement(qn("a:srgbClr"), {"val": str(TEXT)}))
    p_pr.append(colour)
    p_pr.append(p_pr.makeelement(qn("a:buFont"), {"typeface": TEXT_FONT}))
    if ordered:
        p_pr.append(p_pr.makeelement(qn("a:buAutoNum"), {"type": "arabicPeriod", "startAt": str(number)}))
    else:
        p_pr.append(p_pr.makeelement(qn("a:buChar"), {"char": "•" if depth == 0 else "–"}))


def _space_after(paragraph, pt):
    paragraph.space_after = Pt(pt)


def _exact(paragraph, pt, factor=LINE):
    """Exact line spacing, so the heights measured here are the heights drawn."""
    paragraph.line_spacing = Pt(pt * factor)


def _draw_list(frame, block, size, first, depth=0):
    for index, item in enumerate(block.items):
        paragraph = frame.paragraphs[0] if first and index == 0 and depth == 0 else frame.add_paragraph()
        _bullet(paragraph, block.ordered, block.start + index, depth)
        _exact(paragraph, size)
        _write_runs(paragraph, item.runs, size, TEXT)
        _space_after(paragraph, size * 0.35)
        for child in item.children:
            _draw_list(frame, child, size, False, depth + 1)


def _draw_code(slide, block, top, slide_number):
    pt = _code_size(block, slide_number)
    height = _code_height(block, pt)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(MARGIN_X), Inches(top), Inches(BODY_W), Inches(height))
    shape.name = "Code"
    shape.fill.solid()
    shape.fill.fore_color.rgb = CODE_BG
    shape.line.color.rgb = RULE
    shape.line.width = Pt(0.75)
    shape.shadow.inherit = False
    frame = shape.text_frame
    frame.word_wrap = False
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = Inches(CODE_PAD)
    for index, line in enumerate(block.text.splitlines() or [""]):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = PP_ALIGN.LEFT
        _exact(paragraph, pt, CODE_LINE)
        run = paragraph.add_run()
        run.text = line
        _font(run.font, size=pt, color=TEXT, name=CODE_FONT)
    return height


def _draw_table(slide, block, top, pt):
    size = _table_size(block, pt)
    widths = _column_widths(block, size)
    rows = [block.header] + block.rows
    height = _table_height(block, size)
    graphic = slide.shapes.add_table(
        len(rows), len(widths), Inches(MARGIN_X), Inches(top), Inches(sum(widths)), Inches(height)
    )
    graphic.name = "Table"
    table = graphic.table
    table.first_row = True
    tbl_pr = graphic._element.graphic.graphicData.tbl.tblPr
    style = tbl_pr.find(qn("a:tableStyleId"))
    if style is not None:
        tbl_pr.remove(style)
    for col, width in enumerate(widths):
        table.columns[col].width = Inches(width)
    for r, row in enumerate(rows):
        lines = max(_lines(cell, size, max(widths[c] - 2 * CELL_PAD, 0.3)) for c, cell in enumerate(row))
        table.rows[r].height = Inches(lines * size * LINE / 72 + 2 * CELL_PAD)
        for c in range(len(widths)):
            cell = table.cell(r, c)
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(CELL_PAD)
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = DSWD_BLUE
            else:
                cell.fill.fore_color.rgb = ZEBRA if r % 2 == 0 else WHITE
            frame = cell.text_frame
            frame.word_wrap = True
            paragraph = frame.paragraphs[0]
            _exact(paragraph, size)
            runs = row[c] if c < len(row) else []
            if r == 0:
                _write_runs(paragraph, [Run(plain(runs), bold=True)], size, WHITE, bold=True)
            else:
                _write_runs(paragraph, runs, size, TEXT)
    return height


def _draw_image(slide, block, top, base, room):
    width, height = _image_size(block, base)
    if height > room:
        width, height = width * room / height, room
    if width > BODY_W:
        width, height = BODY_W, height * BODY_W / width
    left = (SLIDE_W - width) / 2
    picture = slide.shapes.add_picture(str(base / block.path), Inches(left), Inches(top), Inches(width), Inches(height))
    picture.name = "Picture"
    return height


def _background(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _footer(prs_slide, slide, dark):
    color = PALE if dark else MUTED
    if slide.footer:
        _, frame = _text_box(prs_slide, MARGIN_X, FOOTER_TOP, 9, 0.35, "Footer")
        _write_runs(frame.paragraphs[0], [Run(slide.footer)], FOOTER_PT, color)
    if slide.paginate:
        _, frame = _text_box(prs_slide, SLIDE_W - MARGIN_X - 1.5, FOOTER_TOP, 1.5, 0.35, "Slide number")
        frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        _write_runs(frame.paragraphs[0], [Run(str(slide.number))], FOOTER_PT, color)


def _draw_lead(prs_slide, slide, cover):
    _background(prs_slide, NAVY if cover else DSWD_BLUE)
    paragraphs = [b for b in slide.blocks if isinstance(b, Paragraph | Heading)]
    _, frame = _text_box(prs_slide, 1.0, 1.4, SLIDE_W - 2.0, 4.8, "Title")
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    first = frame.paragraphs[0]
    if cover:
        _write_runs(first, slide.title_runs, 28, YELLOW, bold=True)
    else:
        _write_runs(first, slide.title_runs, 40, WHITE, bold=True)
    first.space_after = Pt(14)
    for block in paragraphs:
        paragraph = frame.add_paragraph()
        if isinstance(block, Heading):
            _write_runs(paragraph, block.runs, 40 if cover else 28, WHITE, bold=True)
            paragraph.space_after = Pt(18)
        else:
            _write_runs(paragraph, block.runs, 20, PALE if cover else WHITE)
            paragraph.space_after = Pt(8)
    if cover:
        rule = prs_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(6.2), Inches(1.6), Inches(0.08))
        rule.name = "Rule"
        rule.fill.solid()
        rule.fill.fore_color.rgb = RED
        rule.line.fill.background()
    _footer(prs_slide, slide, dark=True)


def _layout(slide, base, problems):
    """The body size at which the slide fits; FitError, or a problem noted, when none does."""
    room = BODY_BOTTOM - BODY_TOP
    for block in slide.blocks:
        if isinstance(block, CodeBlock):
            try:
                _code_size(block, slide.number)
            except FitError as error:
                if problems is None:
                    raise
                problems.append(str(error))
    images = [b for b in slide.blocks if isinstance(b, ImageBlock)]
    for pt in BODY_SIZES:
        try:
            fixed = sum(_block_height(b, pt, base, slide.number) for b in slide.blocks if not isinstance(b, ImageBlock))
        except FitError:
            fixed = sum(_safe_height(b, pt, base) for b in slide.blocks if not isinstance(b, ImageBlock))
        gaps = GAP * max(len(slide.blocks) - 1, 0)
        image_room = room - fixed - gaps
        if not images and fixed + gaps <= room:
            return pt
        if images and image_room >= 0.5 * sum(_image_size(b, base)[1] for b in images):
            return pt
    message = f"slide {slide.number} ({slide.title}): content does not fit at {BODY_SIZES[-1]}pt; trim or split it"
    if problems is None:
        raise FitError(message)
    problems.append(message)
    return BODY_SIZES[-1]


def _safe_height(block, pt, base):
    if isinstance(block, CodeBlock):
        lines = block.text.splitlines() or [""]
        return len(lines) * MIN_CODE_PT * CODE_LINE / 72 + 2 * CODE_PAD
    return _block_height(block, pt, base, 0)


def _draw_content(prs_slide, slide, base, problems):
    pt = _layout(slide, base, problems)
    _, frame = _text_box(prs_slide, MARGIN_X, TITLE_TOP, BODY_W, TITLE_H, "Title")
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    _write_runs(frame.paragraphs[0], slide.title_runs, TITLE_PT, DSWD_BLUE, bold=True)
    top = BODY_TOP
    images = [b for b in slide.blocks if isinstance(b, ImageBlock)]
    for block in slide.blocks:
        room = BODY_BOTTOM - top
        if isinstance(block, CodeBlock):
            try:
                top += _draw_code(prs_slide, block, top, slide.number)
            except FitError:
                top += _draw_code_lenient(prs_slide, block, top)
        elif isinstance(block, TableBlock):
            top += _draw_table(prs_slide, block, top, pt)
        elif isinstance(block, ImageBlock):
            rest = sum(
                _safe_height(b, pt, base)
                for b in slide.blocks[slide.blocks.index(block) + 1 :]
                if not isinstance(b, ImageBlock)
            )
            share = (room - rest) / max(
                len([b for b in images if slide.blocks.index(b) >= slide.blocks.index(block)]), 1
            )
            top += _draw_image(prs_slide, block, top, base, max(share, 1.0))
        else:
            height = _block_height(block, pt, base, slide.number)
            _, frame = _text_box(prs_slide, MARGIN_X, top, BODY_W, height, "Text")
            paragraph = frame.paragraphs[0]
            if isinstance(block, ListBlock):
                _draw_list(frame, block, pt, True)
            elif isinstance(block, Heading):
                _exact(paragraph, pt + 2)
                _write_runs(paragraph, block.runs, pt + 2, NAVY, bold=True)
            else:
                _exact(paragraph, pt)
                _write_runs(paragraph, block.runs, pt, TEXT)
            top += height
        top += GAP
    _footer(prs_slide, slide, dark=False)


def _draw_code_lenient(prs_slide, block, top):
    """A code block that broke the limits, drawn at the smallest size so the lenient build still shows it."""
    shrunk = CodeBlock(block.language, block.text)
    lines = shrunk.text.splitlines()
    pt = MIN_CODE_PT
    height = len(lines) * pt * CODE_LINE / 72 + 2 * CODE_PAD
    shape = prs_slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(MARGIN_X), Inches(top), Inches(BODY_W), Inches(height)
    )
    shape.name = "Code"
    shape.fill.solid()
    shape.fill.fore_color.rgb = CODE_BG
    shape.line.color.rgb = RED
    frame = shape.text_frame
    frame.word_wrap = False
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = Inches(CODE_PAD)
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.vertical_anchor = MSO_ANCHOR.TOP
    for index, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = PP_ALIGN.LEFT
        _exact(paragraph, pt, CODE_LINE)
        run = paragraph.add_run()
        run.text = line
        _font(run.font, size=pt, color=TEXT, name=CODE_FONT)
    return height


def build_deck(deck, base, notes=None, problems=None):
    """A Presentation for the deck; images are read relative to base. With notes, each slide gets its entry."""
    if notes is not None:
        for slide in deck.slides:
            if slide.number not in notes:
                raise NotesError(f"slide {slide.number} ({slide.title}) has no lecture-notes entry")
            title, _ = notes[slide.number]
            if _normal(title) != _normal(slide.title):
                raise NotesError(f"slide {slide.number}: the notes say {title!r}, the deck says {slide.title!r}")
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    prs.core_properties.title = deck.title
    prs.core_properties.author = "Edwin Gonzales, Head of Engineering, OpenSPP"
    blank = prs.slide_layouts[6]
    for slide in deck.slides:
        prs_slide = prs.slides.add_slide(blank)
        if slide.kind in ("cover", "section"):
            _draw_lead(prs_slide, slide, slide.kind == "cover")
        else:
            _draw_content(prs_slide, slide, base, problems)
        if notes is not None:
            prs_slide.notes_slide.notes_text_frame.text = notes[slide.number][1]
    return prs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("modules", nargs="*", type=int, default=list(MODULES))
    parser.add_argument("--lenient", action="store_true", help="report fit problems instead of failing")
    parser.add_argument("--notes", type=Path, help="folder with moduleN-lecture-notes.md, for the trainer's copies")
    parser.add_argument("--out", type=Path, help="folder for the output (default: next to each slides.md)")
    args = parser.parse_args(argv)
    if args.notes and not args.out:
        parser.error("--notes needs --out: the copies with notes never go into the repository")
    failed = False
    for module in args.modules:
        source = ROOT / "training" / f"module{module}" / "slides.md"
        deck = parse_deck(source.read_text(encoding="utf-8"))
        notes = None
        if args.notes:
            notes = parse_notes((args.notes / f"module{module}-lecture-notes.md").read_text(encoding="utf-8"))
        problems = [] if args.lenient else None
        try:
            prs = build_deck(deck, source.parent, notes=notes, problems=problems)
        except (FitError, NotesError) as error:
            print(f"Module {module}: {error}", file=sys.stderr)
            failed = True
            continue
        for problem in problems or []:
            print(f"Module {module}: {problem}", file=sys.stderr)
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            name = f"module{module}-slides-with-notes.pptx" if notes else f"module{module}-slides.pptx"
            target = args.out / name
        else:
            target = source.with_suffix(".pptx")
        prs.save(target)
        print(f"Wrote {target} ({len(deck.slides)} slides)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
