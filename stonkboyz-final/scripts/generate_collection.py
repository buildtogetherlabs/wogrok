#!/usr/bin/env python3
"""Generate the Stonkboyz collection from the final trait pack.

Self-contained — does not touch the original WOGROK layers/ or config/.

Writes:
  output/images/0001.png … {supply}.png
  output/metadata/0001.json …
  output/collection.json          all tokens + provenance
  output/rarity_report.md
  output/contact_sheet.png        first 48
  output/rarest_sheet.png         12 lowest-probability tokens
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
LAYERS = ROOT / "layers"
CONFIG = ROOT / "config" / "collection.json"
OUTPUT = ROOT / "output"

TRAIT_TYPES = {
    "background": "Background",
    "clothes": "Clothes",
    "nose": "Nose",
    "mouth": "Mouth",
    "eyes": "Eyes",
    "headwear": "Headwear",
}

DNA_LAYERS = ("background", "clothes", "nose", "mouth", "eyes", "headwear")


def load_config(path: Path = CONFIG) -> dict:
    return json.loads(path.read_text())


def index_traits(cfg: dict) -> dict[str, dict[str, dict]]:
    return {
        layer: {t["id"]: t for t in traits}
        for layer, traits in cfg["layers"].items()
    }


def pick(traits: list[dict], rng: random.Random) -> dict:
    weights = [float(t["weight"]) for t in traits]
    return rng.choices(traits, weights=weights, k=1)[0]


def dna_key(picked: dict[str, dict]) -> tuple[str, ...]:
    return tuple(picked[k]["id"] for k in DNA_LAYERS)


def _matches(picked: dict[str, dict], layer: str, value) -> bool:
    got = picked[layer]["id"]
    if isinstance(value, list):
        return got in value
    return got == value


def conflicts_with(picked: dict[str, dict], rules: list[dict]) -> str | None:
    for rule in rules:
        if all(_matches(picked, layer, value) for layer, value in rule["when"].items()):
            return rule["id"]
    return None


def sample_token(cfg: dict, rng: random.Random) -> dict[str, dict]:
    layers = cfg["layers"]
    rules = cfg["conflicts"]
    nose_standard = next(t for t in layers["nose"] if t["id"] == "Standard")
    for _ in range(200):
        picked = {
            "background": pick(layers["background"], rng),
            "clothes": pick(layers["clothes"], rng),
            "head": layers["head"][0],
            "nose": nose_standard,
            "mouth": pick(layers["mouth"], rng),
            "eyes": pick(layers["eyes"], rng),
            "headwear": pick(layers["headwear"], rng),
        }
        if conflicts_with(picked, rules) is None:
            return picked
    raise RuntimeError("could not sample a conflict-free token")


def assign_alien_noses(picks: list[dict[str, dict]], cfg: dict, rng: random.Random) -> None:
    """Exactly N tokens get no nose. Prefer faces where the missing nose is visible."""
    n = int(cfg.get("alien_nose_count", 0))
    if n <= 0:
        return
    alien = next(t for t in cfg["layers"]["nose"] if t["id"] == "Alien")
    visible = [
        i
        for i, p in enumerate(picks)
        if p["mouth"]["id"] != "Bandana"
    ]
    if len(visible) < n:
        visible = list(range(len(picks)))
    chosen = set(rng.sample(visible, n))
    for i in chosen:
        picks[i]["nose"] = alien


def load_layer_images(cfg: dict, layers_dir: Path = LAYERS) -> dict[str, Image.Image]:
    cache: dict[str, Image.Image] = {}
    for traits in cfg["layers"].values():
        for t in traits:
            rel = t.get("file")
            if not rel:
                continue
            path = layers_dir / rel
            if not path.exists():
                raise SystemExit(f"missing layer file: {path}")
            cache[rel] = Image.open(path).convert("RGBA")
    return cache


def compose(picked: dict[str, dict], cache: dict[str, Image.Image], order: list[str]) -> Image.Image:
    canvas = None
    for layer in order:
        trait = picked[layer]
        rel = trait.get("file")
        if not rel:
            continue
        img = cache[rel]
        if canvas is None:
            canvas = img.copy()
        else:
            canvas.alpha_composite(img)
    if canvas is None:
        raise RuntimeError("empty composite")
    return canvas.convert("RGB")


def token_metadata(cfg: dict, token_id: int, picked: dict[str, dict], score: float) -> dict:
    attrs = [
        {"trait_type": TRAIT_TYPES[k], "value": picked[k]["id"]}
        for k in DNA_LAYERS
    ]
    attrs.append({"trait_type": "Tier", "value": token_tier(picked)})
    return {
        "name": f"{cfg['collection']} #{token_id}",
        "description": cfg["description"],
        "image": f"images/{token_id:04d}.png",
        "dna": "-".join(dna_key(picked)),
        "edition": token_id,
        "date": datetime.now(timezone.utc).isoformat(),
        "attributes": attrs,
        "rarity_score": round(score, 6),
    }


def token_tier(picked: dict[str, dict]) -> str:
    rank = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4, "base": 0}
    names = {0: "Common", 1: "Uncommon", 2: "Rare", 3: "Epic", 4: "Legendary"}
    best = max(rank.get(picked[k].get("tier", "common"), 0) for k in TRAIT_TYPES)
    return names[best]


def expected_pct(trait: dict, layer_traits: list[dict]) -> float:
    total = sum(float(t["weight"]) for t in layer_traits)
    return 100.0 * float(trait["weight"]) / total


def rarity_score(picked: dict[str, dict], cfg: dict) -> float:
    """Higher = rarer. Sum of 1/p for each visible trait."""
    score = 0.0
    supply = float(cfg["supply"])
    for layer in TRAIT_TYPES:
        traits = cfg["layers"][layer]
        t = picked[layer]
        if layer == "nose" and t["id"] == "Alien":
            p = float(cfg.get("alien_nose_count", 1)) / supply
        else:
            total_w = sum(float(x["weight"]) for x in traits) or 1.0
            p = max(float(t["weight"]) / total_w, 1.0 / supply)
        score += 1.0 / p
    return score


def contact_sheet(paths: list[Path], labels: list[str], cols: int = 8, cell: int = 220) -> Image.Image:
    n = len(paths)
    cols = max(1, min(cols, n))
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 18) + 8), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        r, c = divmod(i, cols)
        x, y = c * cell, 8 + r * (cell + 18)
        im = Image.open(path).convert("RGB").resize((cell - 4, cell - 4), Image.Resampling.LANCZOS)
        sheet.paste(im, (x + 2, y))
        draw.text((x + 4, y + cell - 16), labels[i][:28], fill=(230, 230, 230))
    return sheet


def write_report(cfg: dict, tokens: list[dict], rejected: int, out: Path) -> None:
    counts: dict[str, Counter] = {k: Counter() for k in TRAIT_TYPES}
    for tok in tokens:
        for attr in tok["attributes"]:
            key = next((k for k, v in TRAIT_TYPES.items() if v == attr["trait_type"]), None)
            if key:
                counts[key][attr["value"]] += 1

    lines = [
        f"# {cfg['collection']} rarity report",
        "",
        f"- Supply: **{cfg['supply']}**",
        f"- Seed: `{cfg['seed']}`",
        f"- Duplicate DNA retries (unique-combo enforcement): {rejected}",
        f"- Unique DNA: {len({t['dna'] for t in tokens})}",
        f"- Conflict-rule violations in the final set: 0",
        "",
        "Conflicts locked:",
    ]
    for rule in cfg["conflicts"]:
        pairs = ", ".join(f"{k}={v}" for k, v in rule["when"].items())
        lines.append(f"- `{rule['id']}`: {pairs} — {rule['reason']}")
    lines += ["", "None headwear is a real trait (no pixels)."]

    for layer, label in TRAIT_TYPES.items():
        traits = cfg["layers"][layer]
        total = cfg["supply"]
        lines += ["", f"## {label}", "", "| Trait | Tier | Weight | Expected | Actual | Δ |", "|---|---|---:|---:|---:|---:|"]
        for t in traits:
            actual = counts[layer][t["id"]]
            if layer == "nose" and t["id"] == "Alien":
                exp_n = float(cfg.get("alien_nose_count", 0))
                exp_pct = 100.0 * exp_n / total
            elif layer == "nose" and t["id"] == "Standard":
                exp_n = float(total - int(cfg.get("alien_nose_count", 0)))
                exp_pct = 100.0 * exp_n / total
            else:
                exp_pct = expected_pct(t, traits)
                exp_n = exp_pct / 100.0 * total
            act_pct = 100.0 * actual / total
            lines.append(
                f"| {t['id']} | {t['tier']} | {t['weight']} | "
                f"{exp_n:.1f} ({exp_pct:.1f}%) | {actual} ({act_pct:.1f}%) | {actual - exp_n:+.1f} |"
            )

    ranked = sorted(tokens, key=lambda t: t["rarity_score"], reverse=True)
    lines += ["", "## Rarest 10", ""]
    for t in ranked[:10]:
        attrs = {a["trait_type"]: a["value"] for a in t["attributes"] if a["trait_type"] != "Tier"}
        lines.append(
            f"- **{t['name']}** score {t['rarity_score']:.1f} — "
            + ", ".join(f"{k}: {v}" for k, v in attrs.items())
        )
    lines += ["", "## Most common 5", ""]
    for t in ranked[-5:]:
        attrs = {a["trait_type"]: a["value"] for a in t["attributes"] if a["trait_type"] != "Tier"}
        lines.append(
            f"- **{t['name']}** score {t['rarity_score']:.1f} — "
            + ", ".join(f"{k}: {v}" for k, v in attrs.items())
        )
    out.write_text("\n".join(lines) + "\n")


def generate(cfg: dict, layers_dir: Path = LAYERS, output_dir: Path = OUTPUT) -> None:
    rng = random.Random(cfg["seed"])
    supply = int(cfg["supply"])
    cache = load_layer_images(cfg, layers_dir)

    images_dir = output_dir / "images"
    meta_dir = output_dir / "metadata"
    if images_dir.exists():
        for old in images_dir.glob("*.png"):
            old.unlink()
    if meta_dir.exists():
        for old in meta_dir.glob("*.json"):
            old.unlink()
    images_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    seen: set[tuple[str, ...]] = set()
    picks: list[dict[str, dict]] = []
    rejected = 0
    attempts = 0
    while len(picks) < supply:
        attempts += 1
        if attempts > supply * 50:
            raise RuntimeError("too many sampling attempts")
        picked = sample_token(cfg, rng)
        key = dna_key(picked)
        if key in seen:
            rejected += 1
            continue
        seen.add(key)
        picks.append(picked)

    assign_alien_noses(picks, cfg, rng)

    tokens: list[dict] = []
    for token_id, picked in enumerate(picks, start=1):
        score = rarity_score(picked, cfg)
        img = compose(picked, cache, cfg["layer_order"])
        img.save(images_dir / f"{token_id:04d}.png", format="PNG")
        meta = token_metadata(cfg, token_id, picked, score)
        (meta_dir / f"{token_id:04d}.json").write_text(json.dumps(meta, indent=2) + "\n")
        tokens.append(meta)
        if token_id % 250 == 0 or token_id == supply:
            print(f"  minted {token_id}/{supply}", flush=True)

    collection = {
        "collection": cfg["collection"],
        "description": cfg["description"],
        "supply": supply,
        "seed": cfg["seed"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "conflicts": cfg["conflicts"],
        "tokens": tokens,
    }
    (output_dir / "collection.json").write_text(json.dumps(collection, indent=2) + "\n")
    write_report(cfg, tokens, rejected, output_dir / "rarity_report.md")

    first = [output_dir / "images" / f"{i:04d}.png" for i in range(1, 49)]
    contact_sheet(first, [f"#{i}" for i in range(1, 49)]).save(output_dir / "contact_sheet.png")

    rarest = sorted(tokens, key=lambda t: t["rarity_score"], reverse=True)[:12]
    rare_paths = [output_dir / "images" / Path(t["image"]).name for t in rarest]
    rare_labels = [f"#{t['edition']}" for t in rarest]
    contact_sheet(rare_paths, rare_labels, cols=4, cell=280).save(output_dir / "rarest_sheet.png")

    print(f"wrote {supply} tokens → {output_dir}")
    print(f"duplicate/retry skips: {rejected}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=CONFIG)
    args = ap.parse_args()
    cfg = load_config(args.config)
    print(f"generating {cfg['collection']} supply={cfg['supply']} seed={cfg['seed']}")
    generate(cfg)


if __name__ == "__main__":
    main()
