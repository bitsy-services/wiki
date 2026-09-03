#!/usr/bin/env python3
"""Derive the small icon sizes from the source mark.

The source of truth is static/favicon.png, supplied by hand. This script only
resamples it — it never draws anything — so the derivatives cannot disagree
with the original. Replace favicon.png and re-run:

    python3 scripts/gen-icons.py
"""
from PIL import Image

SRC = "static/favicon.png"
ICO_SIZES = [(16, 16), (32, 32), (48, 48)]
APPLE = 180


def load():
    im = Image.open(SRC)
    if im.mode in ("RGBA", "LA", "P"):
        # iOS composites transparency onto black; the mark is drawn on white,
        # so flatten against white rather than letting it invert.
        flat = Image.new("RGB", im.size, "white")
        flat.paste(im, mask=im.convert("RGBA").getchannel("A"))
        return flat
    return im.convert("RGB")


if __name__ == "__main__":
    src = load()
    src.resize((APPLE, APPLE), Image.LANCZOS).save("static/apple-touch-icon.png")
    # Pillow builds every .ico member by resampling the image it is given, so
    # hand it the largest member and let it derive the rest.
    src.resize(ICO_SIZES[-1], Image.LANCZOS).save(
        "static/favicon.ico", sizes=ICO_SIZES)
    print("wrote apple-touch-icon.png favicon.ico from", SRC)
