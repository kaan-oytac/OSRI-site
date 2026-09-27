#!/usr/bin/env python3
"""Generates the site's ornaments and hero engraving as SVG.

Everything here is drawn from scratch by mathematics — no image is copied from
anywhere — so these carry no copyright and need no attribution. Re-run only to
change the artwork:   python make_ornaments.py
"""
import math
import pathlib
import random

OUT = pathlib.Path(__file__).parent / "assets" / "ornaments"
OUT.mkdir(parents=True, exist_ok=True)

CRIMSON = "#A51C30"
INK = "#1A1A1A"
LAUREL = "#2E6B3F"


def svg(path, w, h, body, extra=""):
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="presentation" aria-hidden="true"{extra}>\n'
        f'{body}\n</svg>\n',
        encoding="utf-8",
    )


# ---------------------------------------------------------------- guilloche --
def guilloche_band(path, width=1200, height=120, lines=26, colour=CRIMSON):
    """Engine-turned ribbon: the interference pattern engraved on share
    certificates and banknotes. Two sine waves of different frequency beat
    against each other; each line is that pair at a shifted phase."""
    mid = height / 2
    strokes = []
    for i in range(lines):
        phase = (i / lines) * 2 * math.pi
        points = []
        for step in range(0, width + 1, 6):
            t = step / width * 2 * math.pi
            y = (mid + height * 0.30 * math.sin(7 * t + phase)
                 + height * 0.16 * math.sin(11 * t - phase * 1.5))
            points.append(f"{step},{y:.1f}")
        strokes.append(
            f'  <polyline points="{" ".join(points)}" fill="none" '
            f'stroke="{colour}" stroke-width="0.6" stroke-opacity="0.5"/>'
        )
    svg(path, width, height, "\n".join(strokes), ' preserveAspectRatio="none"')


# ------------------------------------------------------------------ rosette --
def rosette(path, size=240):
    """Three concentric hypotrochoids. Integer radii keep each curve closed,
    so the line is drawn once rather than retraced into a blot."""
    cx = cy = size / 2
    strokes = []
    for R, r, d, op in ((100, 24, 46, 0.55), (82, 21, 36, 0.42), (64, 15, 28, 0.32)):
        periods = r // math.gcd(R, r)
        scale = (size * 0.46) / (R - r + d)
        points = []
        steps = 1200
        for i in range(steps + 1):
            t = i / steps * 2 * math.pi * periods
            x = cx + scale * ((R - r) * math.cos(t) + d * math.cos((R - r) / r * t))
            y = cy + scale * ((R - r) * math.sin(t) - d * math.sin((R - r) / r * t))
            points.append(f"{x:.1f},{y:.1f}")
        strokes.append(
            f'  <polyline points="{" ".join(points)}" fill="none" stroke="{CRIMSON}" '
            f'stroke-width="0.45" stroke-opacity="{op}"/>'
        )
    svg(path, size, size, "\n".join(strokes))


# ------------------------------------------------------------------- laurel --
def leaf(x, y, angle, length=9.0, width=3.4, colour=LAUREL, opacity=0.92):
    """An almond leaf: two quadratic curves meeting at tip and stem."""
    a = math.radians(angle)
    tx, ty = x + length * math.cos(a), y + length * math.sin(a)
    px, py = -math.sin(a) * width, math.cos(a) * width
    mx, my = x + (tx - x) * 0.45, y + (ty - y) * 0.45
    return (f'  <path d="M{x:.1f},{y:.1f} Q{mx + px:.1f},{my + py:.1f} {tx:.1f},{ty:.1f} '
            f'Q{mx - px:.1f},{my - py:.1f} {x:.1f},{y:.1f} Z" fill="{colour}" '
            f'fill-opacity="{opacity}"/>')


def laurel_divider(path, width=440, height=54):
    """Two laurel sprigs flanking a lozenge. Leaves alternate along each stem
    rather than pairing up, which is what makes it read as a branch."""
    cx, cy = width / 2, height / 2
    parts = []
    for direction in (-1, 1):
        start = cx + direction * 30
        end = cx + direction * (width / 2 - 16)
        span = end - start
        parts.append(
            f'  <path d="M{start},{cy} Q{start + span * 0.5:.1f},{cy - 6} {end},{cy}" '
            f'fill="none" stroke="{LAUREL}" stroke-width="1.2" stroke-linecap="round"/>'
        )
        count = 9
        for i in range(count):
            f = (i + 0.5) / count
            x = start + span * f
            y = cy - 6 * 4 * f * (1 - f) * 0.5
            side = 1 if i % 2 == 0 else -1          # alternate, never paired
            angle = (0 if direction > 0 else 180) + side * 42
            parts.append(leaf(x, y, angle, length=9.5 * (1 - 0.4 * f),
                              width=3.5 * (1 - 0.35 * f)))
    parts.append(
        f'  <path d="M{cx},{cy - 7.5} L{cx + 7.5},{cy} L{cx},{cy + 7.5} L{cx - 7.5},{cy} Z" '
        f'fill="{CRIMSON}"/>'
        f'<line x1="{cx - 21}" y1="{cy}" x2="{cx - 12}" y2="{cy}" stroke="{CRIMSON}" stroke-width="1.1"/>'
        f'<line x1="{cx + 12}" y1="{cy}" x2="{cx + 21}" y2="{cy}" stroke="{CRIMSON}" stroke-width="1.1"/>'
    )
    svg(path, width, height, "\n".join(parts))


# -------------------------------------------------------------- hero valley --
def valley(path, width=1200, height=420, seed=11):
    """A line engraving of a lake valley. Tone comes from hatching, the way a
    real engraving builds shade from line density rather than flat fill. The
    hatch is an SVG pattern, so covering a whole hillside costs a few hundred
    bytes. Deterministic: one seed, one view."""
    rng = random.Random(seed)
    horizon = height * 0.60
    defs, parts = [], []

    def ridge_points(base, amp, rough, step):
        pts, x, y = [], 0.0, base
        while x <= width:
            y += rng.uniform(-rough, rough)
            y = max(base - amp, min(base + amp, y))
            pts.append((x, y))
            x += step
        pts.append((width, horizon + 2))
        pts.append((0.0, horizon + 2))
        return pts

    # Sky: fine horizontal hatching, densest at the top.
    for i in range(52):
        f = i / 52
        y = 6 + f * (horizon - 30)
        op = 0.26 * (1 - f) ** 1.6
        if op > 0.012:
            parts.append(f'  <line x1="0" y1="{y:.1f}" x2="{width}" y2="{y:.1f}" '
                         f'stroke="{INK}" stroke-width="0.45" stroke-opacity="{op:.3f}"/>')

    # Three ridges, far to near: finer hatch spacing and firmer crest as they
    # come forward, which is what reads as distance.
    layers = ((horizon - 148, 34, 14, 7.0, 0.18, -62),
              (horizon - 100, 28, 16, 5.2, 0.26, -70),
              (horizon - 56, 22, 13, 3.6, 0.36, -78))
    for n, (base, amp, rough, gap, op, angle) in enumerate(layers):
        defs.append(
            f'    <pattern id="hatch{n}" width="{gap:.1f}" height="{gap:.1f}" '
            f'patternUnits="userSpaceOnUse" patternTransform="rotate({angle})">'
            f'<line x1="0" y1="0" x2="0" y2="{gap:.1f}" stroke="{INK}" '
            f'stroke-width="0.5" stroke-opacity="{op:.2f}"/></pattern>')
        pts = ridge_points(base, amp, rough, width / 46)
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'  <polygon points="{poly}" fill="url(#hatch{n})"/>')
        crest = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-2])
        parts.append(f'  <polyline points="{crest}" fill="none" stroke="{INK}" '
                     f'stroke-width="{0.8 + n * 0.25:.2f}" stroke-opacity="{0.35 + n * 0.16:.2f}"/>')

    # Shoreline: a soft irregular edge, not a ruled line.
    shore, x, sy = [], 0.0, horizon
    while x <= width:
        sy = max(horizon - 3, min(horizon + 3, sy + rng.uniform(-0.8, 0.8)))
        shore.append(f"{x:.1f},{sy:.1f}")
        x += width / 90
    parts.append(f'  <polyline points="{" ".join(shore)}" fill="none" stroke="{INK}" '
                 f'stroke-width="1" stroke-opacity="0.5"/>')

    # Conifers along the near shore: outlined, varied, with trunks.
    for _ in range(14):
        bx = rng.uniform(10, width - 10)
        bh = rng.uniform(22, 46)
        by = horizon - rng.uniform(0, 4)
        op = rng.uniform(0.45, 0.72)
        for t in range(rng.randint(3, 5)):
            f = t / 4
            w = bh * 0.26 * (1 - f * 0.5)
            parts.append(f'  <path d="M{bx:.1f},{by - bh * (f + 0.34):.1f} '
                         f'L{bx + w:.1f},{by - bh * f:.1f} L{bx - w:.1f},{by - bh * f:.1f} Z" '
                         f'fill="{INK}" fill-opacity="{op * 0.45:.2f}" stroke="{INK}" '
                         f'stroke-width="0.5" stroke-opacity="{op:.2f}"/>')
        parts.append(f'  <line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx:.1f}" y2="{by - 5:.1f}" '
                     f'stroke="{INK}" stroke-width="0.9" stroke-opacity="{op:.2f}"/>')

    # Water: broken horizontal lines, spacing widening toward the viewer.
    y, gap = horizon + 6, 3.2
    while y < height - 3:
        x, depth = 0.0, (y - horizon) / (height - horizon)
        while x < width:
            seg = rng.uniform(20, 160)
            if rng.random() > 0.26:
                parts.append(
                    f'  <line x1="{x:.1f}" y1="{y:.1f}" x2="{min(x + seg, width):.1f}" '
                    f'y2="{y:.1f}" stroke="{INK}" stroke-width="0.55" '
                    f'stroke-opacity="{max(0.30 - 0.20 * depth, 0.06):.3f}"/>')
            x += seg + rng.uniform(8, 44)
        y += gap
        gap *= 1.13

    body = "  <defs>\n" + "\n".join(defs) + "\n  </defs>\n" + "\n".join(parts)
    svg(path, width, height, body, ' preserveAspectRatio="xMidYMid slice"')


guilloche_band(OUT / "guilloche.svg")
guilloche_band(OUT / "guilloche-ink.svg", height=90, lines=20, colour=INK)
rosette(OUT / "rosette.svg")
laurel_divider(OUT / "laurel-divider.svg")
# valley(OUT / "valley.svg")   # not used on the site; uncomment to regenerate
print("Wrote:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
