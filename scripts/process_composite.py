#!/usr/bin/env python3
"""
Register a generated composite into:
  - work/composites/{category}/{id}.png  (full preview)
  - layers/{category}/{id}.png           (transparent trait layer)
  - output/previews/traits/{category}_{id}.png  (base + layer check)
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

from extract_layer import extract_trait
from paths import BASE_PNG, LAYERS, OUTPUT, ROOT, TRAITS_JSON

WORK = ROOT / "work"


def composite_preview(layer_path: Path, out_path: Path, bg=(255, 255, 255, 255)) -> None:
    base = Image.open(BASE_PNG).convert("RGBA")
    layer = Image.open(layer_path).convert("RGBA")
    if layer.size != base.size:
        layer = layer.resize(base.size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", base.size, bg)
    canvas.alpha_composite(base)
    canvas.alpha_composite(layer)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)


def mark_done(category: str, trait_id: str) -> None:
    data = json.loads(TRAITS_JSON.read_text())
    for t in data["traits"].get(category, []):
        if t["id"] == trait_id:
            t["status"] = "done"
            break
    TRAITS_JSON.write_text(json.dumps(data, indent=2) + "\n")


def process(category: str, trait_id: str, source: Path, thr: int = 28) -> dict:
    source = Path(source)
    comp_dir = WORK / "composites" / category
    comp_dir.mkdir(parents=True, exist_ok=True)
    comp_path = comp_dir / f"{trait_id}.png"

    # Normalize to 1000x1000 RGBA
    im = Image.open(source).convert("RGBA")
    if im.size != (1000, 1000):
        # fit onto white square
        canvas = Image.new("RGBA", (1000, 1000), (255, 255, 255, 255))
        im_resized = im.copy()
        im_resized.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        ox = (1000 - im_resized.width) // 2
        oy = (1000 - im_resized.height) // 2
        canvas.paste(im_resized, (ox, oy), im_resized)
        im = canvas
    im.save(comp_path)

    layer_path = LAYERS / category / f"{trait_id}.png"
    info = extract_trait(comp_path, layer_path, thr=thr)

    prev = OUTPUT / "previews" / "traits" / f"{category}_{trait_id}.png"
    composite_preview(layer_path, prev)

    # Sanity: if almost no ink, flag
    if info["ink_pixels"] < 80:
        info["warning"] = "very_low_ink"
    if info["ink_pixels"] > 350_000:
        info["warning"] = "very_high_ink_maybe_full_redraw"

    mark_done(category, trait_id)
    info["preview"] = str(prev)
    info["composite"] = str(comp_path)
    return info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--thr", type=int, default=28)
    args = ap.parse_args()
    print(json.dumps(process(args.category, args.id, args.source, thr=args.thr), indent=2))


if __name__ == "__main__":
    main()
