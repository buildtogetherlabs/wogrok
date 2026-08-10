#!/usr/bin/env python3
"""Print trait catalog counts and draw progress."""
from __future__ import annotations

import json
from pathlib import Path

from paths import LAYERS, TRAITS_JSON


def main() -> None:
    cat = json.loads(TRAITS_JSON.read_text())
    print(f"WOGROK catalog v{cat.get('version')}")
    print(f"Base: {cat['base']['id']} → layers/{cat['base']['source_rel']}")
    print(f"Layer order: {' → '.join(cat['layer_order'])}")
    print()
    total_todo = 0
    total_done = 0
    for name, items in cat["traits"].items():
        done = 0
        todo = 0
        for t in items:
            rel = t.get("source_rel")
            if not rel:
                done += 1
                continue
            path = LAYERS / rel
            if path.exists() and t.get("status") == "done":
                done += 1
            elif path.exists():
                done += 1  # file present
            else:
                todo += 1
        total_done += done
        total_todo += todo
        print(f"  {name:12} {done:3}/{done+todo:<3} done  ({todo} to draw)")
    print()
    print(f"Total options: {total_done + total_todo}  |  remaining art: {total_todo}")
    print(f"Raw combo space (from config): see config/traits_summary.json")


if __name__ == "__main__":
    main()
