#!/usr/bin/env python3
"""Generate N random WOGROK samples for conflict review.

Produces:
  output/samples/run_XXX/
    000.png … 099.png
    manifest.json          # full trait lists + seed
    manifest.csv           # easy spreadsheet review
    contact_sheet.png      # grid of all samples
    REVIEW_NOTES.md        # blank template for conflict findings

Sampling is intentionally permissive so bad combos surface.
Only optional soft rules are applied when --soft-rules is set.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from compose_preview import (
    ORDER,
    SUPPRESS_UNDER_CLOTHING,
    clothing_coverage_mask,
    load_layer,
    suppress_under_clothing,
)
from paths import BASE_PNG, LAYERS, OUTPUT, ROOT, RULES_JSON, TRAITS_JSON


def load_catalog() -> dict:
    return json.loads(TRAITS_JSON.read_text())


def options_for(catalog: dict, category: str) -> list[dict]:
    """Return pickable options including none/normal (source_rel None)."""
    return list(catalog["traits"][category])


def weighted_pick(items: list[dict], rng: random.Random) -> dict:
    weights = [float(t.get("weight", 10.0)) for t in items]
    total = sum(weights) or 1.0
    r = rng.random() * total
    acc = 0.0
    for t, w in zip(items, weights):
        acc += w
        if r <= acc:
            return t
    return items[-1]


def soft_resolve(pick: dict[str, dict], rng: random.Random, catalog: dict) -> dict[str, dict]:
    """Light conflict fixes (optional). Prefer not using during discovery runs."""
    eyes = pick["eyes"]["id"]
    mouth = pick["mouth"]["id"]
    head = pick["headwear"]["id"]

    mouth_covers = {"bandana_mouth", "surgical_mask", "gas_mask"}
    eye_covers = {
        "sunglasses",
        "pixel_sunglasses",
        "vr_goggles",
        "night_vision_goggles",
        "glasses_3d",
        "eye_patch",
    }
    heavy_hats = {
        "astronaut_helmet",
        "samurai_helmet",
        "viking_helmet",
        "military_helmet",
        "racing_helmet",
    }
    facial_hair = {
        "mustache",
        "handlebar_mustache",
        "stubble",
        "short_beard",
        "full_beard",
        "goatee",
        "fu_manchu",
    }
    mouth_props = {
        "cigarette",
        "joint",
        "cigar",
        "pipe",
        "vape",
        "toothpick",
        "lollipop",
        "straw",
        "bubble_gum",
        "coffee_cup",
    }

    # Masks block other mouth stuff → force none if conflict
    if mouth in mouth_covers and False:
        pass  # already a single mouth slot

    # Gas/surgical mask + facial hair is one slot; nothing to do

    # Eye patch + heavy goggles is one eyes slot; nothing to do

    # Heavy helmet + halo/horns etc. is one headwear slot; nothing to do

    # If special is piercings and mouth is gas_mask, keep both for discovery

    return pick


def compose(pick: dict[str, dict], bg=(255, 255, 255, 255)) -> Image.Image:
    base = Image.open(BASE_PNG).convert("RGBA")
    canvas = Image.new("RGBA", base.size, bg)
    canvas.alpha_composite(base)

    clothing_id = pick["clothing"]["id"]
    clothing_img = load_layer("clothing", clothing_id)
    cover = None
    if clothing_img is not None:
        canvas.alpha_composite(clothing_img)
        cover = clothing_coverage_mask(clothing_img)

    for cat in ORDER:
        if cat == "clothing":
            continue
        tid = pick[cat]["id"]
        layer = load_layer(cat, tid)
        if layer is None:
            continue
        if cover is not None and cat in SUPPRESS_UNDER_CLOTHING:
            layer = suppress_under_clothing(layer, cover)
        canvas.alpha_composite(layer)
    return canvas


def make_contact_sheet(images: list[Path], out: Path, cols: int = 10, cell: int = 180) -> None:
    n = len(images)
    rows = (n + cols - 1) // cols
    pad = 4
    sheet = Image.new("RGB", (cols * (cell + pad) + pad, rows * (cell + pad) + pad + 24), (28, 28, 30))
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 4), f"WOGROK samples × {n}", fill=(220, 220, 220))
    for i, path in enumerate(images):
        im = Image.open(path).convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = 24 + pad + r * (cell + pad)
        sheet.paste(im, (x, y))
        # index label
        draw.rectangle([x, y, x + 28, y + 14], fill=(0, 0, 0))
        draw.text((x + 2, y + 1), f"{i:03d}", fill=(255, 255, 0))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)


def coverage_report(rows: list[dict], catalog: dict) -> dict:
    """How many times each trait appeared."""
    report = {}
    for cat in ORDER:
        counts = {t["id"]: 0 for t in catalog["traits"][cat]}
        for row in rows:
            counts[row[cat]] = counts.get(row[cat], 0) + 1
        report[cat] = counts
    return report


def write_review_notes(path: Path, run_id: str, n: int) -> None:
    path.write_text(
        f"""# Sample review notes — {run_id}

Review the {n} images in this folder. Mark conflicts and keepers.

## How to review

1. Open `contact_sheet.png` for a fast scan.
2. Open individual `NNN.png` files for close-ups.
3. Use `manifest.csv` to see exact traits per sample.
4. Log conflicts below — these become rules in `config/rules.json`.

## Conflict log

| Sample | Traits involved | Problem | Suggested rule |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

### Common conflict categories to watch

- **Mouth covers** (gas_mask, surgical_mask, bandana_mouth) + props that need an open mouth
- **Eye covers** (sunglasses, goggles, patch) + pupil/eye effects that disappear under them
- **Heavy headwear** (astronaut, racing, samurai helmets) + tall hats / horns / halo
- **Full beard / facial hair** + masks
- **Special objects** (laptop, ramen, pizza) overlapping clothing silhouette badly
- **Glitch / effects** washing out DNA at thumbnail size
- **Archetype clothing** (astronaut, knight, samurai) + mismatched headwear

## Traits that always look good

-

## Traits that need redraw / tweak

| Trait | Category | Issue | Action |
|---|---|---|---|
|  |  |  |  |

## New trait ideas (from this review)

-

## Rules to implement next

```json
{{
  "conflicts": [
    {{ "when": ["mouth:gas_mask"], "forbid": ["special:cigarette"] }}
  ]
}}
```

(Fill in after review.)
"""
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--count", type=int, default=100)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument(
        "--soft-rules",
        action="store_true",
        help="Apply light known conflicts (default: off, for discovery)",
    )
    ap.add_argument(
        "--run-id",
        default=None,
        help="Folder name under output/samples/ (default: timestamp)",
    )
    ap.add_argument("--bg", default="white", choices=["white", "black"])
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else 1001
    rng = random.Random(seed)
    catalog = load_catalog()
    run_id = args.run_id or datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")
    out_dir = OUTPUT / "samples" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    bg = (255, 255, 255, 255) if args.bg == "white" else (12, 12, 14, 255)
    pools = {cat: options_for(catalog, cat) for cat in ORDER}

    # Build picks with strong coverage: shuffle each pool and cycle so
    # every trait appears before heavy repeats (still randomized overall).
    cycles: dict[str, list[dict]] = {}
    for cat in ORDER:
        bag = pools[cat][:]
        rng.shuffle(bag)
        cycles[cat] = bag

    def next_from_cycle(cat: str) -> dict:
        bag = cycles[cat]
        if not bag:
            bag = pools[cat][:]
            rng.shuffle(bag)
            cycles[cat] = bag
        # 70% take from coverage cycle, 30% pure weighted (variety)
        if rng.random() < 0.70 and bag:
            return bag.pop()
        return weighted_pick(pools[cat], rng)

    rows = []
    paths = []
    for i in range(args.count):
        pick = {cat: next_from_cycle(cat) for cat in ORDER}
        if args.soft_rules:
            pick = soft_resolve(pick, rng, catalog)

        img = compose(pick, bg=bg)
        path = out_dir / f"{i:03d}.png"
        img.save(path)
        paths.append(path)

        row = {
            "index": i,
            "file": path.name,
            **{cat: pick[cat]["id"] for cat in ORDER},
            **{f"{cat}_name": pick[cat]["name"] for cat in ORDER},
        }
        rows.append(row)
        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{args.count}")

    # manifest.json
    manifest = {
        "run_id": run_id,
        "seed": seed,
        "count": args.count,
        "soft_rules": args.soft_rules,
        "stack": ["base"] + ORDER,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "samples": rows,
        "coverage": coverage_report(rows, catalog),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # CSV
    fieldnames = ["index", "file"] + ORDER + [f"{c}_name" for c in ORDER]
    with (out_dir / "manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row[k] for k in fieldnames})

    make_contact_sheet(paths, out_dir / "contact_sheet.png", cols=10, cell=160)
    # larger sheet for screen review
    make_contact_sheet(paths, out_dir / "contact_sheet_large.png", cols=10, cell=220)

    write_review_notes(out_dir / "REVIEW_NOTES.md", run_id, args.count)

    # coverage summary print
    print(f"\nWrote {args.count} samples → {out_dir}")
    print(f"  contact_sheet.png")
    print(f"  manifest.csv / manifest.json")
    print(f"  REVIEW_NOTES.md")
    print("\nTrait coverage (appearances):")
    for cat in ORDER:
        zeros = [tid for tid, n in manifest["coverage"][cat].items() if n == 0]
        print(f"  {cat}: {len(manifest['coverage'][cat]) - len(zeros)}/{len(manifest['coverage'][cat])} traits appeared; {len(zeros)} never sampled")
        if zeros and len(zeros) <= 12:
            print(f"    never: {', '.join(zeros)}")


if __name__ == "__main__":
    main()
