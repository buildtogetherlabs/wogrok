# Stonkboyz — final trait pack + 3,333 generate

Artist-final 1000×1000 RGBA layers and a generated 3,333-supply collection.
This folder is an **add-only drop**. It does not replace the original WOGROK `layers/` set.

## Collection

| | |
|---|---|
| Supply | **3,333** |
| Seed | `33330812` (reproducible) |
| Unique DNA | 3,333 / 3,333 |
| Bald / None hat | **940** (28.2%) |
| Conflict violations | **0** |

Images live locally (not in git — ~627 MB):

```
stonkboyz-final/output/images/0001.png … 3333.png
stonkboyz-final/output/metadata/0001.json …
stonkboyz-final/output/collection.json
```

Regenerate:

```bash
.venv/bin/python stonkboyz-final/scripts/generate_collection.py
```

## Stack (bottom → top)

```
01-background
  + 02-clothes
  + 03-head
  + 04-mouth
  + 05-eyes
  + 06-headwear   ← skipped when Headwear = None
```

## Locked conflicts

- Mouth `Bandana` × Headwear `Bandana`
- Clothes `Cowboy` × Mouth `Bandana`

## Rarity (proposed + used)

Weights are relative inside each layer. Full expected-vs-actual table: [`RARITY.md`](RARITY.md).

Headline odds on 3,333:

| Trait | Tier | Actual |
|---|---|---|
| Headwear None (bald) | common | 940 (28.2%) |
| Standard Deviation mouth | common | 1,171 (35.1%) |
| Unimpressed eyes | common | 602 (18.1%) |
| Cult Robe | legendary | 17 (0.5%) |
| Taco Trade hat | legendary | 27 (0.8%) |
| Laser Eyez | epic | 58 (1.7%) |
| King / Knight / Tuxedo | epic | 37 / 36 / 39 |

Common shirts (Dad / Stonks / All In / Jacket / Business Suit) are ~8% each. Legendary clothes and hats sit under 1%.

## Notes

- `Green Gainz .png` was 0 bytes and was dropped. Display name is **Green Gainz** (`04-mouth/Green Gainz_.png`).
- Beanie is a slouch cut — it covers the eye line. That is in the art, not a compose bug.
- No headphones layer, so the exact album-cover look cannot mint. Closest is Crypto Hoodie + Toothpick + Unimpressed + None.

## Status

- [x] Layers stored here
- [x] None / Bald headwear
- [x] Rarity weights
- [x] Conflicts locked
- [x] 3,333 generate + metadata
- [ ] IPFS / reveal URI
- [ ] On-chain mint
