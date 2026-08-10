"""v2 layer types: opaque cover vs ink overlay."""
from __future__ import annotations

# Stack after background (bottom → top)
STACK_ORDER = [
    "base",       # fixed file, not a trait pick
    "eyes",       # opaque — always pick one (incl. normal)
    "clothing",   # opaque cover — garment only
    "mouth",      # ink overlay
    "special",    # ink overlay (default)
    "headwear",   # opaque cover — hat OR bald_crown
]

OPAQUE_CATEGORIES = {"eyes", "clothing", "headwear"}
INK_CATEGORIES = {"mouth", "special"}

# headwear "none" is not empty — it's the bald crown piece
HEADWEAR_NONE_ID = "bald_crown"
EYES_DEFAULT_ID = "normal"
