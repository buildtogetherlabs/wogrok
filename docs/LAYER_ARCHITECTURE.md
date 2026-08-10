# WOGROK layer architecture (v2 — correct stacking)

This replaces the v1 “ink-only diff” approach. v1 leaked head/face into clothing
and hats and used transparent line art, so you could see the skull through hats
and double-heads on hoodies.

## Canvas

Every file is **1000×1000** PNG RGBA, aligned to the same pixel grid.

## Two kinds of trait layers

| Kind | Categories | Pixels | Transparency |
|---|---|---|---|
| **Opaque cover** | clothing, headwear, eyes, bald crown | Solid fill (usually white) + black line art | Transparent *outside* the object only. Fill must hide whatever is underneath. |
| **Ink overlay** | mouth, most special | Black (or colored) strokes only | Transparent everywhere except the strokes. Must **not** paint white. |

## Stack (bottom → top)

```
background          solid color
  + base            body + face DNA, NO eyes, NO crown
  + eyes            opaque eye assemblies (always one, including "normal")
  + clothing        opaque garment only (no head)
  + mouth           ink on face (beard, cigarette, …)
  + special         ink / props (chains, tattoos, objects)
  + headwear        opaque hat OR bald_crown (always one)
```

## Base (`layers/base/wogrok_base.png`)

Provides:

- Shoulders + neck
- Face outline from **forehead cut line** down through chin
- Nose, deadpan mouth, under-eye bag, face DNA
- White fill for skin so clothing/hats can cover cleanly

Must **not** provide:

- Eyes / pupils / eye socket ink (eyes layer fills this)
- Top of skull / crown above the hat line (headwear or `bald_crown` fills this)

## Eyes (opaque cover)

- Every mint picks exactly one eyes trait (including `normal`)
- Layer includes socket outlines + white of eye + pupils/effects
- Opaque enough that nothing from base shows through the sockets
- Asymmetry (flat left / round right, pupil size) is part of identity

## Clothing (opaque cover)

- **Only the garment** — hoodie, suit, robe, etc.
- **No head, no face, no eyes**
- White (or colored) fabric fill + black outlines
- Covers neck/shoulders of the base
- Transparent outside the clothing silhouette

## Mouth (ink overlay)

- Lines/props only: beard, cigarette, mask strokes, etc.
- Transparent background — base face shows through
- Never opaque white
- May hang slightly over collar; clothing fill still owns the fabric

## Headwear (opaque cover)

- Hat / helmet / horns / halo as a solid piece
- **No face**
- Opaque fill so base never shows through the hat
- When no hat: use `headwear/bald_crown.png` (completes the skull)

## Special

- Default: ink overlay (tattoos, chains, piercings, thin props)
- Rare solid props may be opaque; prefer not covering the face DNA

## Why v1 failed

1. Diff extraction kept only “ink vs base” → clothing/hats became **transparent outlines**
2. Composites still contained the full head → clothing files included **face + head lines**
3. Base had full eyes + full crown → hats couldn’t hide the skull outline

## Production rules (non-negotiable)

1. Clothing/headwear/eyes QA: place layer on **magenta** — object solid, no face ghosting
2. Clothing/headwear QA: place on base — no double jaw, no skull through hat
3. Mouth QA: on base — only new strokes, base face still readable
4. Never reintroduce white-eraser pixels into ink overlays
