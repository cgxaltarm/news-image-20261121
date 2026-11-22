#!/usr/bin/env python3
"""news-image-20261121 — entry program (Python 3, standard library only).

Writes the pre-rendered front page (entry.png, 1024x1024, 33 stories
from Saturday 21 November 2026) to the output directory, after
checking the file is a real PNG inside the competition limits.

The front page itself is drawn at build time by work/frontpage_21nov.py
(Pillow, flat vector-style drawing, no external images). This program
uses only the standard library because nothing is installed before it
runs in the scoring container.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def main():
    with open(SRC, "rb") as fh:
        buf = fh.read()
    if buf[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if buf[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    if len(buf) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(buf)} bytes, over the 1 MiB limit")
    # IHDR: width at bytes 16-19, height at 20-23 (big-endian uint32).
    width, height = struct.unpack(">II", buf[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    print(f"entry.png: {width}x{height}, {len(buf)} bytes")

    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    # Determinism: the written file must be byte-identical to the source.
    with open(OUT, "rb") as fh:
        written = fh.read()
    if written != buf:
        raise SystemExit("output differs from entry.png")
    print(f"wrote {OUT} ({len(written)} bytes, byte-identical)")


if __name__ == "__main__":
    main()
