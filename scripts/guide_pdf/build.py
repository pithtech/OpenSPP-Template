#!/usr/bin/env python3
# Part of the DSWD 4Ps OpenSPP training template. See LICENSE file for full copyright and licensing details.
"""Build the participant guide as a PDF: training/participant-guide.md -> training/participant-guide.pdf.

Pandoc turns the Markdown into HTML (with a contents list); WeasyPrint lays it out on A4 with a cover, page numbers as
"page/total" and the contents' page numbers. Requires `pandoc` and `weasyprint` on the PATH (macOS:
`brew install pandoc weasyprint`).

    python3 scripts/guide_pdf/build.py
"""

import datetime
import html as html_lib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GUIDE = ROOT / "training" / "participant-guide.md"
OUTPUT = ROOT / "training" / "participant-guide.pdf"
TITLE = "OpenSPP and Odoo Foundations Training: Participant Guide"

# A code block longer than this may break across pages; shorter ones stay whole.
LONG_CODE_LINES = 40

# Code blocks are set at CODE_PT; a block whose longest line is wider than the page gets a smaller size, down to
# MIN_CODE_PT, so its lines do not wrap. CODE_WIDTH_PT is the inside width of a block on A4 with the print margins,
# and MONO_ADVANCE the width of one monospace character in ems.
CODE_PT = 7.4
MIN_CODE_PT = 5.8
CODE_WIDTH_PT = 450
MONO_ADVANCE = 0.602
FIT_CHARS = int(CODE_WIDTH_PT / (CODE_PT * MONO_ADVANCE))


def prepare_markdown(text: str) -> str:
    """Replace the title and the hand-written contents list, which the cover and the generated contents replace."""
    lines = text.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = "\n".join(lines).lstrip("\n")
    # The hand-written list runs from "Contents:" to the first horizontal rule.
    text = re.sub(r"(?ms)^Contents:\n.*?^---\n", "", text, count=1)
    # Chapters start on a new page in print; the rules between them are not needed.
    text = re.sub(r"(?m)^---\n", "", text)
    return "## About this guide\n\n" + text.lstrip("\n")


def mark_long_code_blocks(html: str) -> str:
    """Add the class `long` to code blocks of more than LONG_CODE_LINES lines, so they may break across pages."""

    def mark(match: re.Match) -> str:
        attrs, body = match.group(1), match.group(2)
        if body.count("\n") <= LONG_CODE_LINES:
            return match.group(0)
        classes = re.search(r'class="([^"]*)"', attrs)
        if classes:
            attrs = attrs.replace(classes.group(0), f'class="{classes.group(1)} long"')
        else:
            attrs = attrs + ' class="long"'
        return f"<pre{attrs}>{body}</pre>"

    return re.sub(r"(?s)<pre([^>]*)>(.*?)</pre>", mark, html)


def _visible_length(line: str) -> int:
    """The number of characters a line of escaped HTML shows on the page."""
    return len(html_lib.unescape(re.sub(r"<[^>]+>", "", line)))


def fit_wide_code_blocks(html: str) -> str:
    """Give a code block wider than the page a font size at which its longest line fits."""

    def fit(match: re.Match) -> str:
        attrs, body = match.group(1), match.group(2)
        longest = max((_visible_length(line) for line in body.split("\n")), default=0)
        if longest <= FIT_CHARS:
            return match.group(0)
        size = max(MIN_CODE_PT, round(CODE_WIDTH_PT / (longest * MONO_ADVANCE), 1))
        return f'<pre{attrs} style="font-size: {size}pt">{body}</pre>'

    return re.sub(r"(?s)<pre([^>]*)>(.*?)</pre>", fit, html)


def keep_inline_code_tokens_whole(html: str) -> str:
    """Keep inline-code tokens with a hyphen or backslash on one line (`--profile`, `.\\odoo-project`)."""

    def nobr(match: re.Match) -> str:
        tokens = match.group(2).split(" ")
        tokens = [
            f'<span class="nobr">{tok}</span>' if len(tok) > 1 and ("-" in tok or "\\" in tok) else tok
            for tok in tokens
        ]
        return f"<code{match.group(1)}>{' '.join(tokens)}</code>"

    parts = re.split(r"(?s)(<pre[^>]*>.*?</pre>)", html)
    return "".join(
        part if part.startswith("<pre") else re.sub(r"(?s)<code([^>]*)>(.*?)</code>", nobr, part) for part in parts
    )


def _edition() -> str:
    commit = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False
    ).stdout.strip()
    today = datetime.date.today().strftime("%d %B %Y").lstrip("0")
    return f"Edition of {today}" + (f", from commit {commit}" if commit else "")


def main() -> int:
    for tool in ("pandoc", "weasyprint"):
        if not shutil.which(tool):
            print(f"{tool} not found. Install it (macOS: brew install {tool}).", file=sys.stderr)
            return 1
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        source = tmp_dir / "guide.md"
        source.write_text(prepare_markdown(GUIDE.read_text(encoding="utf-8")), encoding="utf-8")
        html_file = tmp_dir / "guide.html"
        subprocess.run(
            [
                "pandoc",
                str(source),
                "--from=gfm",
                "--to=html5",
                "--standalone",
                "--toc",
                "--toc-depth=3",
                f"--template={HERE / 'template.html'}",
                f"--metadata=title:{TITLE}",
                f"--variable=edition:{_edition()}",
                f"--variable=css:{HERE / 'print.css'}",
                f"--output={html_file}",
            ],
            check=True,
        )
        html = html_file.read_text(encoding="utf-8")
        html = keep_inline_code_tokens_whole(fit_wide_code_blocks(mark_long_code_blocks(html)))
        html_file.write_text(html, encoding="utf-8")
        subprocess.run(["weasyprint", str(html_file), str(OUTPUT)], check=True)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
