#!/usr/bin/env python3
"""Preview immutable base on a background."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from paths import BASE_PNG, CANVAS_JSON, LAYERS, OUTPUT


def main() -> None:
    p = argparse.ArgumentParser(description="Preview WOGROK base on a background")
    p.add_argument("--background", default="paper_white", help="background trait id")
    p.add_argument(
        "--out",
        type=Path,
        default=OUTPUT / "previews" / "base_preview.png",
        help="output path",
    )
    args = p.parse_args()

    canvas = json.loads(CANVAS_JSON.read_text())
    w, h = canvas["width"], canvas["height"]

    bg_path = LAYERS / "background" / f"{args.background}.png"
    if bg_path.exists():
        img = Image.open(bg_path).convert("RGBA").resize((w, h), Image.Resampling.NEAREST)
    else:
        img = Image.new("RGBA", (w, h), (245, 243, 238, 255))

    base = Image.open(BASE_PNG).convert("RGBA")
    if base.size != (w, h):
        base = base.resize((w, h), Image.Resampling.LANCZOS)
    img.alpha_composite(base)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
