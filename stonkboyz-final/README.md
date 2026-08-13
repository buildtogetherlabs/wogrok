# Stonkboyz — final trait pack + 2,222 generate

Artist-final 1000×1000 RGBA layers and a generated 2,222-supply collection.
This folder is an **add-only drop**. It does not replace the original WOGROK `layers/` set.

## Collection

| | |
|---|---|
| Supply | **2,222** |
| Seed | `22220812` (reproducible) |
| Unique DNA | 2,222 / 2,222 |
| Canonical nose | **2,200** |
| Alien (no nose) | **22** |
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
  + nose          ← skipped on the 22 Alien tokens
  + 04-mouth
  + 05-eyes
  + 06-headwear   ← skipped when Headwear = None
```

## Locked conflicts

- Mouth `Bandana` × Headwear `Bandana`
- Clothes `Cowboy` × Mouth `Bandana`
- Beanie (stocking cap) × **any eyes** — Eyes is forced to `None`
- Cowboy Hat / Bucket Hat / Military Degen × Pixel Glasses / Aviator / 3D Glasses / VR

Bandage mouth is **out**. File stays in `layers/04-mouth/` but is not minted.

## Rarity (proposed + used)

Weights are relative inside each layer. Full expected-vs-actual table: [`RARITY.md`](RARITY.md).

Headline odds on 3,333:

| Trait | Tier | Actual |
|---|---|---|
| Headwear None (bald) | common | ~30% |
| Standard nose | base | 2,200 |
| Alien (no nose) | legendary | **22** |
| Cult Robe | legendary | ~0.6% |
| Taco Trade hat | legendary | ~0.8% |

Common shirts (Dad / Stonks / All In / Jacket / Business Suit) are ~8% each.

## Notes

- Head file is a blank oval. Canonical wojak hook nose is `layers/03-head/Nose.png`.
- `Green Gainz .png` was 0 bytes and was dropped. Display name is **Green Gainz** (`04-mouth/Green Gainz_.png`).
- Beanie / stocking cap is locked to **no eyes**. The 116 beanie tokens were re-rendered in place.
- No headphones layer, so the exact album-cover look cannot mint. Closest is Crypto Hoodie + Toothpick + Unimpressed + None.

## Status

- [x] Layers stored here
- [x] None / Bald headwear
- [x] Canonical nose + 22 Alien noseless
- [x] Bandage removed
- [x] Hat / glasses conflicts locked
- [x] 2,222 generate + metadata
- [ ] IPFS / reveal URI
- [ ] On-chain mint
