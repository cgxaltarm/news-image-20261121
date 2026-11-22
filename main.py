#!/usr/bin/env python3
"""Publish the pre-rendered front page for news-image-20261121.

The competition entry is a single picture: entry.png, a newspaper front
page for Saturday 21 November 2026 with 33 stories, drawn at build time
by work/frontpage_21nov.py. This program's only job is to hand that
picture to the grader: check it really is a PNG inside the size limits,
then copy it byte for byte into the output folder the grader reads.

Standard library only — nothing is installed before this runs in the
scoring container, so no Pillow here, just raw bytes and shutil.
"""

import os
import shutil
import struct
import sys

# Where the picture lives, and where the grader expects it.
BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")
DEST_FOLDER = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(DEST_FOLDER, "entry.png")

# Competition limits for the picture.
BYTE_LIMIT = 1024 * 1024
SIDE_LIMIT = 1024

# First eight bytes of every PNG file.
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def load_picture(path):
    """Read the picture and confirm it is a PNG within the limits."""
    with open(path, "rb") as handle:
        data = handle.read()

    if data[:8] != SIGNATURE:
        raise SystemExit("entry.png does not start with the PNG signature")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png is missing its IHDR chunk")

    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        raise SystemExit("entry.png has a zero width or height in its IHDR")
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise SystemExit(
            "entry.png is %dx%d, larger than the %dx%d limit"
            % (width, height, SIDE_LIMIT, SIDE_LIMIT)
        )
    if len(data) > BYTE_LIMIT:
        raise SystemExit(
            "entry.png is %d bytes, over the 1 MiB limit" % len(data)
        )
    return data, width, height


def publish(data):
    """Copy the picture into the output folder, checking it matches."""
    os.makedirs(DEST_FOLDER, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    with open(DEST, "rb") as handle:
        copied = handle.read()
    if copied != data:
        raise SystemExit("the copied file differs from entry.png")


def run():
    data, width, height = load_picture(SOURCE)
    print("entry.png: %dx%d, %d bytes" % (width, height, len(data)))
    publish(data)
    print("wrote %s (%d bytes, identical to the source)" % (DEST, len(data)))


if __name__ == "__main__":
    run()
