#!/usr/bin/env python3
"""Extract a transparent trait layer by differencing composite vs base.

Modes:
  ink_only (default for clothing/mouth/headwear/special):
    Keep only non-white trait ink. Never emit opaque white.
    Safe to stack on top of clothing without punching holes.

  with_eraser (eyes that replace pupils / cover base ink):
    Also emit opaque white where the composite erased base ink
    (e.g. replaced black pupils with $ / hearts).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from paths import BASE_PNG

# Categories that should never paint white (they stack above other traits)
INK_ONLY_CATEGORIES = {"clothing", "mouth", "headwear", "special"}


def extract_trait(
    composite_path: Path,
    out_path: Path,
    base_path: Path = BASE_PNG,
    thr: int = 22,
    grow: int = 0,
    allow_white_eraser: bool | None = None,
    ink_only: bool | None = None,
) -> dict:
    category = out_path.parent.name
    if ink_only is None:
        ink_only = category in INK_ONLY_CATEGORIES
    if allow_white_eraser is None:
        # White eraser only for eye replacements / covers
        allow_white_eraser = (not ink_only) and category == "eyes"

    base = Image.open(base_path).convert("RGBA")
    comp = Image.open(composite_path).convert("RGBA")
    if comp.size != base.size:
        canvas = Image.new("RGBA", base.size, (255, 255, 255, 255))
        tmp = comp.copy()
        tmp.thumbnail(base.size, Image.Resampling.LANCZOS)
        ox = (base.size[0] - tmp.width) // 2
        oy = (base.size[1] - tmp.height) // 2
        canvas.paste(tmp, (ox, oy), tmp)
        comp = canvas

    b = np.asarray(base).astype(np.int16)
    c = np.asarray(comp).astype(np.int16)

    dist = np.abs(c[..., :3] - b[..., :3]).max(axis=2)
    mask = dist >= thr

    if ink_only:
        # Only keep pixels that are actually dark/colored ink — never near-white.
        # Prevents white "holes" when this layer sits above clothing.
        dark = c[..., :3].max(axis=2) < 248
        # Also keep saturated color (lasers, bloodshot red, etc. on mouth rarely)
        sat = (c[..., :3].max(axis=2) - c[..., :3].min(axis=2)) > 30
        mask = mask & (dark | sat)

    out = np.zeros((base.size[1], base.size[0], 4), dtype=np.uint8)
    out[mask, :3] = np.clip(c[mask, :3], 0, 255).astype(np.uint8)
    out[mask, 3] = 255

    if allow_white_eraser and not ink_only:
        base_ink = b[..., :3].min(axis=2) < 200
        comp_white = c[..., :3].min(axis=2) > 245
        eraser = base_ink & comp_white
        out[eraser, :3] = 255
        out[eraser, 3] = 255

    if grow > 0:
        alpha = Image.fromarray(out[..., 3], mode="L")
        for _ in range(grow):
            alpha = alpha.filter(ImageFilter.MaxFilter(3))
        a = np.asarray(alpha)
        grow_only = (a > 0) & (out[..., 3] == 0)
        if ink_only:
            grow_ink = c[..., :3].max(axis=2) < 248
            grow_only = grow_only & grow_ink
        out[grow_only, :3] = np.clip(c[grow_only, :3], 0, 255).astype(np.uint8)
        out[..., 3] = np.maximum(out[..., 3], a if not ink_only else np.where(grow_only | (out[..., 3] > 0), a, 0).astype(np.uint8))

    img = Image.fromarray(out, mode="RGBA")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)

    ink = int((np.asarray(img)[..., 3] > 10).sum())
    return {
        "out": str(out_path),
        "ink_pixels": ink,
        "size": list(img.size),
        "ink_only": ink_only,
        "allow_white_eraser": allow_white_eraser,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--composite", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--thr", type=int, default=22)
    ap.add_argument("--ink-only", action="store_true")
    ap.add_argument("--with-eraser", action="store_true")
    args = ap.parse_args()
    print(
        extract_trait(
            args.composite,
            args.out,
            thr=args.thr,
            ink_only=True if args.ink_only else None,
            allow_white_eraser=True if args.with_eraser else None,
        )
    )


if __name__ == "__main__":
    main()
