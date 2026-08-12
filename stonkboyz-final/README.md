# Stonkboyz — final trait pack

Artist-final 1000×1000 RGBA layers for the Stonkboyz collection.
This folder is an **add-only drop**. It does not replace the original WOGROK `layers/` set.

## Stack (bottom → top)

```
01-background
  + 02-clothes
  + 03-head
  + 04-mouth
  + 05-eyes
  + 06-headwear
```

`head → clothes` also works; collars are cut to the same neck hole. Previews in `previews/` use `background → clothes → head → mouth → eyes → headwear`.

## Counts

| Layer | Usable files |
|---|---|
| Background | 3 |
| Clothes | 24 |
| Head | 1 (blank oval — no eyes, no mouth) |
| Mouth | 9 |
| Eyes | 17 |
| Headwear | 20 |
| **Raw combo space** | **220,320** |

Plenty of unique DNA for a 3,333–10,000 collection.

## Notes from the 2026-08-12 intake

- Every file is 1000×1000 PNG with alpha. Alignment is good — these composite cleanly.
- Dropped `Green Gainz .png` (0 bytes). The real trait is `04-mouth/Green Gainz_.png`.
- Head is a closed bald oval. Every mint needs a mouth trait (`Standard Deviation` is the deadpan default).
- There is **no Bald / None headwear**. Every random mint currently gets a hat. Add a None option if bald characters (album-cover look) should exist.
- Suggested conflict rules before a full generate:
  - Mouth `Bandana` × Headwear `Bandana`
  - Clothes `Cowboy` (already has a neckerchief) × Mouth `Bandana`
- No dedicated headphones / cigarette-only accessory layer. Album-cover vibe is closest to: PNL Green + Crypto Hoodie + Toothpick + Unimpressed + no hat.

## Status

- [x] Layers received and stored here
- [x] Sample composites (see `previews/`)
- [ ] Collection size + rarity weights
- [ ] None/Bald headwear decision
- [ ] Conflict rules locked
- [ ] Full generate + metadata
