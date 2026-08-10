#!/usr/bin/env python3
"""Extract a transparent trait layer by differencing composite vs base.

Supports "eraser" pixels: where the composite is white but the base had ink
(e.g. replaced pupils), the layer paints opaque white so base ink is covered
when composited on top of the base.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from paths import BASE_PNG


def extract_trait(
    composite_path: Path,
    out_path: Path,
    base_path: Path = BASE_PNG,
    thr: int = 22,
    grow: int = 0,
    allow_white_eraser: bool = True,
) -> dict:
    base = Image.open(base_path).convert("RGBA")
    comp = Image.open(composite_path).convert("RGBA")
    if comp.size != base.size:
        # Center-fit onto white 1000 canvas if needed
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

    out = np.zeros((base.size[1], base.size[0], 4), dtype=np.uint8)

    # Trait color pixels
    out[mask, :3] = np.clip(c[mask, :3], 0, 255).astype(np.uint8)
    out[mask, 3] = 255

    # White eraser: composite is near-white, base has dark ink
    if allow_white_eraser:
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
        out[grow_only, :3] = np.clip(c[grow_only, :3], 0, 255).astype(np.uint8)
        out[..., 3] = np.maximum(out[..., 3], a)

    img = Image.fromarray(out, mode="RGBA")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)

    ink = int((np.asarray(img)[..., 3] > 10).sum())
    return {"out": str(out_path), "ink_pixels": ink, "size": list(img.size)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--composite", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--thr", type=int, default=22)
    args = ap.parse_args()
    print(extract_trait(args.composite, args.out, thr=args.thr))


if __name__ == "__main__":
    main()
