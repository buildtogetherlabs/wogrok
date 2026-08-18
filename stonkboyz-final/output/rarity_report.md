# Stonkboyz rarity report

- Supply: **2222**
- Seed: `22220814`
- Duplicate DNA retries (unique-combo enforcement): 189
- Unique DNA: 2222
- Conflict-rule violations in the final set: 0

## Overall token tiers (3)

A boy is **Legendary** if he has Cult Robe, Taco Trade, or Alien nose.
Otherwise the majority look (has a punchy rare/epic trait) is **Common**,
and the all-plain look is **Rare**.

| Overall | Count | Share |
|---|---:|---:|
| Common | 1405 | 63.2% |
| Rare | 757 | 34.1% |
| Legendary | 60 | 2.7% |

Trait-level rows below still use the original five design labels (common / uncommon / rare / epic / legendary). Those are weights inside each layer, not the token's overall tier.

Conflicts locked:
- `double_bandana`: mouth=Bandana, headwear=Bandana — Two bandanas on the same face.
- `cowboy_neckerchief`: clothes=Cowboy, mouth=Bandana — Cowboy already has a neckerchief.
- `beanie_no_drawn_eyes`: headwear=Beanie, eyes=['Unimpressed', 'Impressed', 'Alien', 'Blood Shot', 'Red Eyez', 'Love', 'No Cry', 'Sniper', 'X Eyez', 'Eye Patch', 'Aviator', 'Blacked Out', 'Pixel Glasses', '3D Glasses', 'Monocle', 'VR', 'Laser Eyez', 'Energy'] — Beanie covers the sockets. No eye pixels; metadata stays Standard.
- `hat_bandana`: headwear=Bandana, eyes=['Eye Patch', '3D Glasses'] — Bandana clashes with these eyes.
- `hat_cap_white`: headwear=Baseball Cap White, eyes=['Blacked Out', 'VR', 'Eye Patch'] — White cap clashes with these eyes.
- `hat_cap_green`: headwear=Baseball Cap Green, eyes=['Blacked Out', 'VR', 'Eye Patch'] — Green cap clashes with these eyes.
- `hat_bucket`: headwear=Bucket Hat, eyes=['Blacked Out', 'VR', 'Eye Patch', 'Pixel Glasses'] — Bucket hat clashes with these eyes.
- `hat_cook`: headwear=Let Him Cook, eyes=['Blacked Out', 'Eye Patch'] — Chef hat clashes with these eyes.
- `hat_cowboy`: headwear=Cowboy Hat, eyes=['Blacked Out', 'VR', 'Eye Patch', 'Monocle'] — Cowboy hat clashes with these eyes.
- `hat_band_white`: headwear=Headband White, eyes=['Eye Patch', 'Aviator', '3D Glasses'] — White headband clashes with these eyes.
- `hat_band_green`: headwear=Headband Green, eyes=['Eye Patch', 'Aviator', '3D Glasses'] — Green headband clashes with these eyes.
- `hat_fedora`: headwear=Fedora, eyes=['Eye Patch', 'VR'] — Fedora clashes with these eyes.
- `hat_lil`: headwear=Lil Trader, eyes=['Blacked Out', 'Eye Patch', '3D Glasses'] — Lil Trader clashes with these eyes.
- `hat_taco`: headwear=Taco Trade, eyes=['Blacked Out', 'Eye Patch', 'Aviator', 'Pixel Glasses'] — Taco Trade clashes with these eyes.
- `hat_viking`: headwear=Viking Hodl, eyes=['Blacked Out', 'Eye Patch', '3D Glasses'] — Viking Hodl clashes with these eyes.
- `hat_general`: headwear=Stonks General, eyes=['Blacked Out', 'Eye Patch'] — Stonks General clashes with these eyes.
- `hat_ngmi`: headwear=NGMI Cap, eyes=['Blacked Out', 'VR', 'Eye Patch'] — NGMI cap clashes with these eyes.
- `hat_military`: headwear=Military Degen, eyes=['Blacked Out', 'VR', 'Eye Patch', 'Monocle', 'Aviator', '3D Glasses', 'Pixel Glasses'] — Military Degen clashes with these eyes.
- `hat_santa`: headwear=Santa, eyes=['Blacked Out', 'Eye Patch', '3D Glasses', 'Pixel Glasses'] — Santa clashes with these eyes.
- `energy_eyewear`: eyes=Energy, headwear=['Beanie'] — Energy is an eye layer; beanie already has no drawn eyes.

None headwear is a real trait (no pixels).

## Background

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| PNL Standard | common | 60 | 1333.2 (60.0%) | 1265 (56.9%) | -68.2 |
| PNL Green | uncommon | 25 | 555.5 (25.0%) | 589 (26.5%) | +33.5 |
| PNL Red | rare | 15 | 333.3 (15.0%) | 368 (16.6%) | +34.7 |

## Clothes

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| Dad Shirt | common | 14 | 190.8 (8.6%) | 193 (8.7%) | +2.2 |
| Stonks Shirt | common | 14 | 190.8 (8.6%) | 170 (7.7%) | -20.8 |
| All In | common | 14 | 190.8 (8.6%) | 189 (8.5%) | -1.8 |
| Jacket | common | 14 | 190.8 (8.6%) | 191 (8.6%) | +0.2 |
| Business Suit | common | 14 | 190.8 (8.6%) | 168 (7.6%) | -22.8 |
| Crypto Conference | uncommon | 8 | 109.1 (4.9%) | 115 (5.2%) | +5.9 |
| Crypto Hoodie | uncommon | 8 | 109.1 (4.9%) | 124 (5.6%) | +14.9 |
| Diamond Hands | uncommon | 8 | 109.1 (4.9%) | 120 (5.4%) | +10.9 |
| Track Suit | uncommon | 8 | 109.1 (4.9%) | 100 (4.5%) | -9.1 |
| Jersey | uncommon | 8 | 109.1 (4.9%) | 125 (5.6%) | +15.9 |
| Doctor | uncommon | 8 | 109.1 (4.9%) | 119 (5.4%) | +9.9 |
| Cowboy | uncommon | 8 | 109.1 (4.9%) | 99 (4.5%) | -10.1 |
| Casino Shirt | rare | 4 | 54.5 (2.5%) | 49 (2.2%) | -5.5 |
| Bull Market | rare | 4 | 54.5 (2.5%) | 52 (2.3%) | -2.5 |
| Bathrobe | rare | 4 | 54.5 (2.5%) | 57 (2.6%) | +2.5 |
| Astronaut | rare | 4 | 54.5 (2.5%) | 59 (2.7%) | +4.5 |
| Degen Hoodie | rare | 4 | 54.5 (2.5%) | 51 (2.3%) | -3.5 |
| Puffer Jacket | rare | 4 | 54.5 (2.5%) | 56 (2.5%) | +1.5 |
| Gainz Tech | rare | 4 | 54.5 (2.5%) | 54 (2.4%) | -0.5 |
| Tuxedo | epic | 2 | 27.3 (1.2%) | 30 (1.4%) | +2.7 |
| Luxury Robe | epic | 2 | 27.3 (1.2%) | 25 (1.1%) | -2.3 |
| King | epic | 2 | 27.3 (1.2%) | 28 (1.3%) | +0.7 |
| Knight | epic | 2 | 27.3 (1.2%) | 32 (1.4%) | +4.7 |
| Cult Robe | legendary | 1 | 13.6 (0.6%) | 16 (0.7%) | +2.4 |

## Nose

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| Standard | base | 1 | 2200.0 (99.0%) | 2200 (99.0%) | +0.0 |
| Alien | legendary | 0 | 22.0 (1.0%) | 22 (1.0%) | +0.0 |

## Mouth

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| Standard Deviation | common | 40 | 916.3 (41.2%) | 864 (38.9%) | -52.3 |
| Toothpick | common | 18 | 412.3 (18.6%) | 412 (18.5%) | -0.3 |
| Piercing | common | 14 | 320.7 (14.4%) | 317 (14.3%) | -3.7 |
| Stitches | uncommon | 8 | 183.3 (8.2%) | 209 (9.4%) | +25.7 |
| Pipe | uncommon | 7 | 160.4 (7.2%) | 192 (8.6%) | +31.6 |
| Green Gainz | rare | 4 | 91.6 (4.1%) | 94 (4.2%) | +2.4 |
| Total Loss | rare | 3 | 68.7 (3.1%) | 74 (3.3%) | +5.3 |
| Bandana | rare | 3 | 68.7 (3.1%) | 60 (2.7%) | -8.7 |

## Eyes

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| Standard | common | 0 | 0.0 (0.0%) | 26 (1.2%) | +26.0 |
| Unimpressed | common | 22 | 428.8 (19.3%) | 415 (18.7%) | -13.8 |
| Impressed | common | 16 | 311.9 (14.0%) | 301 (13.5%) | -10.9 |
| Alien | uncommon | 10 | 194.9 (8.8%) | 193 (8.7%) | -1.9 |
| Blood Shot | uncommon | 7 | 136.4 (6.1%) | 141 (6.3%) | +4.6 |
| Red Eyez | uncommon | 6 | 116.9 (5.3%) | 144 (6.5%) | +27.1 |
| Love | uncommon | 6 | 116.9 (5.3%) | 115 (5.2%) | -1.9 |
| No Cry | uncommon | 6 | 116.9 (5.3%) | 113 (5.1%) | -3.9 |
| Sniper | uncommon | 5 | 97.5 (4.4%) | 129 (5.8%) | +31.5 |
| X Eyez | uncommon | 5 | 97.5 (4.4%) | 116 (5.2%) | +18.5 |
| Eye Patch | uncommon | 5 | 97.5 (4.4%) | 45 (2.0%) | -52.5 |
| Aviator | uncommon | 5 | 97.5 (4.4%) | 78 (3.5%) | -19.5 |
| Blacked Out | rare | 4 | 78.0 (3.5%) | 50 (2.3%) | -28.0 |
| Pixel Glasses | rare | 4 | 78.0 (3.5%) | 98 (4.4%) | +20.0 |
| 3D Glasses | rare | 3 | 58.5 (2.6%) | 47 (2.1%) | -11.5 |
| Monocle | rare | 3 | 58.5 (2.6%) | 72 (3.2%) | +13.5 |
| Energy | rare | 3 | 58.5 (2.6%) | 58 (2.6%) | -0.5 |
| VR | epic | 2 | 39.0 (1.8%) | 41 (1.8%) | +2.0 |
| Laser Eyez | epic | 2 | 39.0 (1.8%) | 40 (1.8%) | +1.0 |

## Headwear

| Trait | Tier | Weight | Expected | Actual | Δ |
|---|---|---:|---:|---:|---:|
| None | common | 40 | 734.5 (33.1%) | 707 (31.8%) | -27.5 |
| Headband White | common | 8 | 146.9 (6.6%) | 143 (6.4%) | -3.9 |
| Baseball Cap White | common | 8 | 146.9 (6.6%) | 148 (6.7%) | +1.1 |
| Headband Green | common | 7 | 128.5 (5.8%) | 121 (5.4%) | -7.5 |
| Baseball Cap Green | common | 7 | 128.5 (5.8%) | 118 (5.3%) | -10.5 |
| Beanie | rare | 2 | 36.7 (1.7%) | 26 (1.2%) | -10.7 |
| Bucket Hat | uncommon | 6 | 110.2 (5.0%) | 115 (5.2%) | +4.8 |
| Bandana | uncommon | 5 | 91.8 (4.1%) | 88 (4.0%) | -3.8 |
| Fedora | uncommon | 5 | 91.8 (4.1%) | 109 (4.9%) | +17.2 |
| Cowboy Hat | uncommon | 5 | 91.8 (4.1%) | 91 (4.1%) | -0.8 |
| NGMI Cap | rare | 4 | 73.5 (3.3%) | 71 (3.2%) | -2.5 |
| Lil Trader | rare | 4 | 73.5 (3.3%) | 100 (4.5%) | +26.5 |
| Military Degen | rare | 3 | 55.1 (2.5%) | 41 (1.8%) | -14.1 |
| Santa | rare | 3 | 55.1 (2.5%) | 56 (2.5%) | +0.9 |
| Devil | rare | 3 | 55.1 (2.5%) | 64 (2.9%) | +8.9 |
| Crown | epic | 2 | 36.7 (1.7%) | 32 (1.4%) | -4.7 |
| Fanboy | epic | 2 | 36.7 (1.7%) | 47 (2.1%) | +10.3 |
| Let Him Cook | epic | 2 | 36.7 (1.7%) | 44 (2.0%) | +7.3 |
| Stonks General | epic | 2 | 36.7 (1.7%) | 31 (1.4%) | -5.7 |
| Viking Hodl | epic | 2 | 36.7 (1.7%) | 47 (2.1%) | +10.3 |
| Taco Trade | legendary | 1 | 18.4 (0.8%) | 23 (1.0%) | +4.6 |

## Rarest 10

- **Stonkboyz #109** score 307.8 — Background: PNL Standard, Clothes: Casino Shirt, Nose: Alien, Mouth: Toothpick, Eyes: Monocle, Headwear: Taco Trade
- **Stonkboyz #598** score 263.1 — Background: PNL Green, Clothes: Cult Robe, Nose: Standard, Mouth: Pipe, Eyes: VR, Headwear: Bandana
- **Stonkboyz #1897** score 260.4 — Background: PNL Green, Clothes: Cult Robe, Nose: Standard, Mouth: Total Loss, Eyes: Laser Eyez, Headwear: None
- **Stonkboyz #1912** score 257.5 — Background: PNL Standard, Clothes: Cult Robe, Nose: Standard, Mouth: Green Gainz, Eyes: Impressed, Headwear: Fanboy
- **Stonkboyz #581** score 249.3 — Background: PNL Standard, Clothes: Cult Robe, Nose: Standard, Mouth: Standard Deviation, Eyes: Laser Eyez, Headwear: Fedora
- **Stonkboyz #1805** score 238.9 — Background: PNL Green, Clothes: Tuxedo, Nose: Standard, Mouth: Green Gainz, Eyes: Impressed, Headwear: Taco Trade
- **Stonkboyz #483** score 238.1 — Background: PNL Standard, Clothes: Luxury Robe, Nose: Alien, Mouth: Pipe, Eyes: X Eyez, Headwear: Headband Green
- **Stonkboyz #209** score 235.8 — Background: PNL Red, Clothes: Cult Robe, Nose: Standard, Mouth: Stitches, Eyes: Sniper, Headwear: Lil Trader
- **Stonkboyz #2188** score 233.7 — Background: PNL Standard, Clothes: Jersey, Nose: Alien, Mouth: Stitches, Eyes: Energy, Headwear: Viking Hodl
- **Stonkboyz #586** score 233.6 — Background: PNL Standard, Clothes: Tuxedo, Nose: Alien, Mouth: Standard Deviation, Eyes: X Eyez, Headwear: Cowboy Hat

## Most common 5

- **Stonkboyz #78** score 24.9 — Background: PNL Standard, Clothes: Stonks Shirt, Nose: Standard, Mouth: Standard Deviation, Eyes: Unimpressed, Headwear: None
- **Stonkboyz #80** score 24.9 — Background: PNL Standard, Clothes: All In, Nose: Standard, Mouth: Standard Deviation, Eyes: Unimpressed, Headwear: None
- **Stonkboyz #89** score 24.9 — Background: PNL Standard, Clothes: Business Suit, Nose: Standard, Mouth: Standard Deviation, Eyes: Unimpressed, Headwear: None
- **Stonkboyz #667** score 24.9 — Background: PNL Standard, Clothes: Dad Shirt, Nose: Standard, Mouth: Standard Deviation, Eyes: Unimpressed, Headwear: None
- **Stonkboyz #1121** score 24.9 — Background: PNL Standard, Clothes: Jacket, Nose: Standard, Mouth: Standard Deviation, Eyes: Unimpressed, Headwear: None
