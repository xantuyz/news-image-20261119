#!/usr/bin/env python3
"""Publish the pre-rendered front page to the harness output folder.

The newspaper image is drawn ahead of time by render.py (Pillow is
only needed for drawing); this entrypoint uses the standard library
alone, so it runs in the sandbox with nothing installed. It copies
entry.png to the output directory and checks the copy by comparing
SHA-256 digests before reporting success.
"""

import hashlib
import hmac
import os
import sys
from pathlib import Path


def fingerprint(blob):
    return hashlib.sha256(blob).hexdigest()


def publish():
    root = Path(__file__).resolve().parent
    picture = root / "entry.png"
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    payload = picture.read_bytes()
    dest.write_bytes(payload)
    if not hmac.compare_digest(fingerprint(payload),
                               fingerprint(dest.read_bytes())):
        print("digest mismatch after copy", file=sys.stderr)
        sys.exit(1)
    print("published", dest, len(payload), "bytes")


if __name__ == "__main__":
    publish()
