#!/usr/bin/env python3
"""Generate the site icon set from one parametric description of the mark.

The mark is a hexagonal web: six spokes at 30-degree increments, a straight
hexagon threaded onto them, and an outer hexagon whose edges sag inward. Every
output below is drawn from the constants in GEOM, so the SVG and the PNG/ICO
fallbacks cannot drift apart. Re-run with: python3 scripts/gen-icons.py
"""
import math
from PIL import Image, ImageDraw

OUT = "static"

# All lengths are in units of a 1600x1600 design square centred on (800, 800).
UNIT = 1600.0
GEOM = dict(
    W=140.0,    # stroke width
    R1=490.0,   # circumradius of the inner straight hexagon
    R2=800.0,   # radius at which the outer web meets the spokes
    RM=645.0,   # radius the outer web sags to midway between two spokes
)
ANGLES = [30, 90, 150, 210, 270, 330]
INK = "#000000"
PAPER = "#ffffff"


def polar(cx, cy, r, deg, k):
    a = math.radians(deg)
    return (cx + k * r * math.cos(a), cy - k * r * math.sin(a))


def geometry(cx, cy, k, reach):
    """Return (spokes, hexagon, web) in output coordinates.

    `k` scales the design square; `reach` is how far the spokes run, in design
    units, and must exceed the half-diagonal of the canvas so the mark bleeds.
    """
    g = GEOM
    spokes = [(polar(cx, cy, reach, a, k), polar(cx, cy, reach, a + 180, k))
              for a in ANGLES[:3]]                     # three diameters
    hexagon = [polar(cx, cy, g["R1"], a, k) for a in ANGLES]
    # A quadratic Bezier's midpoint is halfway between the chord midpoint and
    # the control point, so place the control point to hit RM exactly.
    chord_r = g["R2"] * math.cos(math.radians(30))
    ctrl_r = 2 * g["RM"] - chord_r
    web = [(polar(cx, cy, g["R2"], a, k),
            polar(cx, cy, ctrl_r, a + 30, k),
            polar(cx, cy, g["R2"], a + 60, k)) for a in ANGLES]
    return spokes, hexagon, web


def svg():
    s, h, w = geometry(UNIT / 2, UNIT / 2, 1.0, 1200)
    n = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    d = [f"M{n(a[0])} {n(a[1])}L{n(b[0])} {n(b[1])}" for a, b in s]
    d.append("M" + "L".join(f"{n(x)} {n(y)}" for x, y in h) + "Z")
    d.append(f"M{n(w[0][0][0])} {n(w[0][0][1])}"
             + "".join(f"Q{n(c[0])} {n(c[1])} {n(e[0])} {n(e[1])}" for _, c, e in w)
             + "Z")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(UNIT)} {n(UNIT)}" '
        f'width="{n(UNIT)}" height="{n(UNIT)}" role="img" '
        f'aria-label="Bitsy Services web mark">\n'
        f'  <rect width="{n(UNIT)}" height="{n(UNIT)}" fill="{PAPER}"/>\n'
        f'  <g fill="none" stroke="{INK}" stroke-width="{n(GEOM["W"])}" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        + "".join(f'    <path d="{p}"/>\n' for p in d)
        + "  </g>\n</svg>\n"
    )


def raster(w, h, k, ss=8):
    """Draw the mark on a w x h canvas, the design square scaled by k."""
    img = Image.new("RGB", (w * ss, h * ss), PAPER)
    d = ImageDraw.Draw(img)
    reach = math.hypot(w, h) / k          # always past the far corner
    spokes, hexagon, web = geometry(w / 2, h / 2, k, reach)
    width = max(1, round(GEOM["W"] * k * ss))

    def stroke(points):
        pts = [(x * ss, y * ss) for x, y in points]
        d.line(pts, fill=INK, width=width, joint="curve")
        for x, y in pts:                  # round caps and joins
            d.ellipse([x - width / 2, y - width / 2,
                       x + width / 2, y + width / 2], fill=INK)

    for a, b in spokes:
        stroke([a, b])
    stroke(hexagon + [hexagon[0]])
    for p0, pc, p2 in web:
        stroke([(
            (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * pc[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * pc[1] + t * t * p2[1],
        ) for t in (i / 96 for i in range(97))])
    return img.resize((w, h), Image.LANCZOS)


def square(px):
    return raster(px, px, px / UNIT)


if __name__ == "__main__":
    with open(f"{OUT}/favicon.svg", "w") as fh:
        fh.write(svg())
    # Each .ico member is drawn at its own size rather than downsampled from
    # one big render, which keeps the 16px strokes from turning to grey mush.
    square(48).save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                    append_images=[square(16), square(32)])
    square(180).save(f"{OUT}/apple-touch-icon.png")
    # Open Graph wants 1.91:1; render natively at that shape so the spokes run
    # off all four edges instead of being cropped to stubs.
    raster(1200, 630, 630 / UNIT).save(f"{OUT}/og-image.png")
    print("wrote favicon.svg favicon.ico apple-touch-icon.png og-image.png")
