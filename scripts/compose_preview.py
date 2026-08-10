#!/usr/bin/env python3
"""Compose base + trait layers into a preview PNG."""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image
from paths import BASE_PNG, LAYERS, OUTPUT

ORDER = ["clothing", "mouth", "eyes", "special", "headwear"]

def main():
    ap = argparse.ArgumentParser()
    for cat in ORDER:
        ap.add_argument(f"--{cat}", default=None)
    ap.add_argument("--out", type=Path, default=OUTPUT / "previews" / "manual.png")
    ap.add_argument("--bg", default="white", choices=["white", "black"])
    args = ap.parse_args()
    bg = (255,255,255,255) if args.bg=="white" else (12,12,14,255)
    base = Image.open(BASE_PNG).convert("RGBA")
    canvas = Image.new("RGBA", base.size, bg)
    canvas.alpha_composite(base)
    for cat in ORDER:
        tid = getattr(args, cat)
        if not tid or tid in ("none", "normal"):
            continue
        p = LAYERS / cat / f"{tid}.png"
        if not p.exists():
            raise SystemExit(f"missing layer: {p}")
        canvas.alpha_composite(Image.open(p).convert("RGBA"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out)
    print("wrote", args.out)

if __name__ == "__main__":
    main()
