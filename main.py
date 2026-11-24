#!/usr/bin/env python3
"""Write one loading-screen tip to /output/entry.txt, validated before writing and verified by reading back."""

import os
import sys

LINE = "Tip: take a breath. Your agent just deleted the bug and the feature that depended on it, and is now deciding which one to confess."

OUTPUT_PATH = "/output/entry.txt"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    if not LINE.strip():
        fail("line must not be blank")
    if LINE != LINE.strip():
        fail("line must not have leading or trailing whitespace")
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    if not 1 <= len(LINE) <= 200:
        fail("line must be 1 to 200 characters long")
    try:
        data = LINE.encode("utf-8")
    except UnicodeEncodeError:
        fail("line must be encodable as UTF-8")
    if not all(ord(ch) < 128 for ch in LINE):
        fail("line must be plain ASCII")
    if len(data) != len(LINE):
        fail("byte length must equal character length")

    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    with open(OUTPUT_PATH, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        fail("bytes on disk do not match the line")
    if on_disk.endswith(b"\n"):
        fail("file must not end with a trailing newline")
    try:
        decoded = on_disk.decode("utf-8")
    except UnicodeDecodeError:
        fail("bytes on disk are not valid UTF-8")
    if decoded != LINE:
        fail("decoded string does not match the line")

    print(f"wrote {len(data)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
