#!/usr/bin/env python3
"""Swap the placeholder seal for your real logo.

Usage:
    python3 swap-logo.py /path/to/your-logo.png

Copies your file into assets/ and rewires every page (masthead image and
browser-tab icon) to point at it. Works with .svg, .png, .jpg or .webp.
Safe to run more than once.
"""
import pathlib
import re
import shutil
import struct
import sys

ROOT = pathlib.Path(__file__).parent
TYPES = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def pixel_size(path):
    """Best-effort width/height, so the page reserves the right space."""
    data = path.read_bytes()
    if path.suffix.lower() == ".png" and data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    if path.suffix.lower() == ".svg":
        text = data.decode("utf-8", "ignore")
        box = re.search(r'viewBox="[\d.\s-]*?([\d.]+)[\s,]+([\d.]+)"', text)
        if box:
            return float(box.group(1)), float(box.group(2))
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 swap-logo.py /path/to/your-logo.png")

    source = pathlib.Path(sys.argv[1]).expanduser()
    if not source.is_file():
        sys.exit(f"Can't find that file: {source}")

    ext = source.suffix.lower()
    if ext not in TYPES:
        sys.exit(f"Unsupported file type '{ext}'. Use .svg, .png, .jpg or .webp.")

    target = ROOT / "assets" / f"seal{ext}"
    (ROOT / "assets").mkdir(exist_ok=True)
    shutil.copy(source, target)

    # Display width is fixed at 84px by the stylesheet; scale height to match.
    size = pixel_size(target)
    if size:
        width, height = 84, max(1, round(84 * size[1] / size[0]))
    else:
        width, height = 84, 84

    href = f"assets/seal{ext}"
    mime = TYPES[ext]
    changed = []

    targets = list(ROOT.glob("*.html")) + [ROOT / "build.py"]
    for path in targets:
        if not path.exists():
            continue
        text = original = path.read_text(encoding="utf-8")
        text = re.sub(
            r'<link rel="icon" href="assets/seal\.[a-z]+" type="[^"]+">',
            f'<link rel="icon" href="{href}" type="{mime}">',
            text,
        )
        text = re.sub(
            r'<img class="seal" src="assets/seal\.[a-z]+" alt="" width="\d+" height="\d+">',
            f'<img class="seal" src="{href}" alt="" width="{width}" height="{height}">',
            text,
        )
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path.name)

    # Remove the old placeholder so only one seal file remains.
    for suffix in TYPES:
        stale = ROOT / "assets" / f"seal{suffix}"
        if stale != target and stale.exists():
            stale.unlink()

    print(f"Logo installed as {href} ({width}x{height} on screen).")
    print(f"Updated: {', '.join(sorted(changed))}")
    print("Open index.html in your browser to check it.")


if __name__ == "__main__":
    main()
