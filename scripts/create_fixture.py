#!/usr/bin/env python3
"""Create a tiny, deliberately awkward GeoCities test corpus. Never overwrites."""

import argparse
from pathlib import Path


def create_fixture(root):
    root = Path(root).expanduser().absolute()
    if root.exists() or root.is_symlink():
        raise FileExistsError(f"Refusing to overwrite {root}")
    if not root.parent.is_dir():
        raise FileNotFoundError(f"Parent directory does not exist: {root.parent}")
    root.mkdir()
    (root / "Home").mkdir()
    (root / "home").mkdir()
    (root / "Home" / "INDEX.HTML").write_bytes(b"<h1>Historic page A</h1>\n")
    (root / "home" / "index.html").write_bytes(b"<h1>Historic page B</h1>\n")
    (root / "home" / "music.mid").write_bytes(b"MThd")
    (root / "Home" / "image.GIF").write_bytes(b"GIF89a")
    (root / "Home" / "odd?name.html").write_bytes(b"<p>Question mark filename</p>\n")
    (root / "Home" / "line\nbreak.txt").write_bytes(b"Newline in filename\n")
    (root / "loop").symlink_to(".")
    return root


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", help="New directory (must not already exist)")
    args = parser.parse_args()
    print(f"Created test fixture: {create_fixture(args.destination)}")
