#!/usr/bin/env python3
"""Refuse top-level folders that hijack Odoo's stylesheet build.

The repo root is mounted into the container as an addons root. Odoo's SCSS importer
resolves a relative ``@import "<dir>/..."`` against *any* addons root that contains a
``<dir>`` folder, so a top-level folder with one of Bootstrap's import-root names makes
every stylesheet bundle compile to an error stub ("A css error occured, using an old
style to render this page").

The list below is the set of relative import roots found in Odoo 19 and the add-ons
shipped in the image. Keep it in sync with RESERVED_ROOT_DIRS in ``odoo-project``.
"""

import argparse
import sys
from pathlib import Path

RESERVED_ROOT_DIRS = ("forms", "helpers", "mixins", "utilities", "vendor")


def reserved_dirs(root: Path) -> list[str]:
    return sorted(name for name in RESERVED_ROOT_DIRS if (root / name).is_dir())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".", help="Repository root to check (default: current directory)")
    args = parser.parse_args()
    found = reserved_dirs(Path(args.root))
    if not found:
        return 0
    print("Top-level folder(s) that break Odoo's stylesheet build: " + ", ".join(found))
    print("Odoo resolves Bootstrap's SCSS imports against any addons root holding a folder with these names:")
    print("  " + ", ".join(RESERVED_ROOT_DIRS))
    print("Rename or move the folder. A stale OpenSPP checkout goes to upstream/: mv vendor upstream")
    return 1


if __name__ == "__main__":
    sys.exit(main())
