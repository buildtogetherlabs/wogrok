#!/usr/bin/env python3
"""Compose base + trait layers into a preview PNG.

Stack (bottom → top):
  background → base → clothing → mouth → eyes → special → headwear

Clothing is drawn before mouth so the hoodie/collar always lands cleanly
on the base. Mouth/special ink never punches white holes through clothing
(layers are ink-only). When clothing has solid fill (e.g. black hood
interior), mouth pixels under that fill are suppressed so the clothing
reads like the solo-trait version.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from paths import BASE_PNG, LAYERS, OUTPUT

# Bottom → top after base
ORDER = ["clothing", "mouth", "eyes", "special", "headwear"]

# Categories that should not paint over solid clothing fill
SUPPRESS_UNDER_CLOTHING = {"mouth", "special"}


def load_layer(category: str, trait_id: str) -> Image.Image | None:
    if not trait_id or trait_id in ("none", "normal"):
        return None
    p = LAYERS / category / f"{trait_id}.png"
    if not p.exists():
        raise SystemExit(f"missing layer: {p}")
    return Image.open(p).convert("RGBA")


def clothing_coverage_mask(clothing: Image.Image) -> np.ndarray:
    """Any opaque clothing pixel — solid fills AND collar/outline ink.

    Mouth/special must not paint here so clothing always reads like the
    solo-trait version (clean hood interior, unbroken collar, etc.).
    """
    c = np.asarray(clothing)
    return c[..., 3] > 30


def suppress_under_clothing(layer: Image.Image, cover: np.ndarray) -> Image.Image:
    arr = np.asarray(layer).copy()
    arr[cover, 3] = 0
    return Image.fromarray(arr, "RGBA")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    for cat in ORDER:
        ap.add_argument(f"--{cat}", default=None)
    ap.add_argument("--out", type=Path, default=OUTPUT / "previews" / "manual.png")
    ap.add_argument("--bg", default="white", choices=["white", "black"])
    ap.add_argument(
        "--no-clothing-mask",
        action="store_true",
        help="Allow mouth/special to paint over solid clothing fill",
    )
    args = ap.parse_args()

    bg = (255, 255, 255, 255) if args.bg == "white" else (12, 12, 14, 255)
    base = Image.open(BASE_PNG).convert("RGBA")
    canvas = Image.new("RGBA", base.size, bg)
    canvas.alpha_composite(base)

    clothing_img = load_layer("clothing", args.clothing)
    cover = None
    if clothing_img is not None:
        # Clothing first so it sits on the base (base → clothing → mouth …)
        canvas.alpha_composite(clothing_img)
        if not args.no_clothing_mask:
            cover = clothing_coverage_mask(clothing_img)

    for cat in ORDER:
        if cat == "clothing":
            continue
        layer = load_layer(cat, getattr(args, cat))
        if layer is None:
            continue
        if cover is not None and cat in SUPPRESS_UNDER_CLOTHING:
            layer = suppress_under_clothing(layer, cover)
        canvas.alpha_composite(layer)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
