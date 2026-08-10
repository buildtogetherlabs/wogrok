#!/usr/bin/env python3
"""Compose WOGROK v2 layers.

Stack (bottom → top):
  background → base → eyes → clothing → mouth → special → headwear

Opaque covers (eyes, clothing, headwear): solid fill, hide what's under.
Ink overlays (mouth, special): strokes only, no white paint.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from layer_types import (
    EYES_DEFAULT_ID,
    HEADWEAR_NONE_ID,
    STACK_ORDER,
)
from paths import BASE_PNG, LAYERS, OUTPUT

TRAIT_ORDER = ["eyes", "clothing", "mouth", "special", "headwear"]


def load_layer(category: str, trait_id: str | None) -> Image.Image | None:
    if not trait_id:
        return None
    # defaults
    if category == "headwear" and trait_id in ("none", "Nothing", ""):
        trait_id = HEADWEAR_NONE_ID
    if category == "eyes" and trait_id in ("none", ""):
        trait_id = EYES_DEFAULT_ID
    if trait_id in ("none",) and category in ("mouth", "special"):
        return None
    p = LAYERS / category / f"{trait_id}.png"
    if not p.exists():
        raise SystemExit(f"missing layer: {p}")
    return Image.open(p).convert("RGBA")


def compose(
    *,
    eyes: str = EYES_DEFAULT_ID,
    clothing: str | None = None,
    mouth: str | None = None,
    special: str | None = None,
    headwear: str = HEADWEAR_NONE_ID,
    bg=(255, 255, 255, 255),
) -> Image.Image:
    base = Image.open(BASE_PNG).convert("RGBA")
    canvas = Image.new("RGBA", base.size, bg)
    canvas.alpha_composite(base)

    picks = {
        "eyes": eyes,
        "clothing": clothing,
        "mouth": mouth,
        "special": special,
        "headwear": headwear or HEADWEAR_NONE_ID,
    }
    for cat in TRAIT_ORDER:
        layer = load_layer(cat, picks.get(cat))
        if layer is not None:
            if layer.size != base.size:
                layer = layer.resize(base.size, Image.Resampling.NEAREST)
            canvas.alpha_composite(layer)
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--eyes", default=EYES_DEFAULT_ID)
    ap.add_argument("--clothing", default=None)
    ap.add_argument("--mouth", default=None)
    ap.add_argument("--special", default=None)
    ap.add_argument("--headwear", default=HEADWEAR_NONE_ID)
    ap.add_argument("--out", type=Path, default=OUTPUT / "previews" / "manual.png")
    ap.add_argument("--bg", default="white", choices=["white", "black"])
    args = ap.parse_args()
    bg = (255, 255, 255, 255) if args.bg == "white" else (12, 12, 14, 255)
    img = compose(
        eyes=args.eyes,
        clothing=args.clothing,
        mouth=args.mouth,
        special=args.special,
        headwear=args.headwear,
        bg=bg,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
