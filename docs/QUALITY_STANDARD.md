# Quality standard (non-negotiable)

The failed “geometry beanie + sticker armor” proof was **not acceptable**.
Trait rebuilds must look like the original Wogrok line art — not Clip Art.

## Gold standard for this project

`work/quality_masters/beanie_knight_beard_chain_moon.png`

That image is the bar: same exhausted Wogrok DNA, cohesive drawing, solid
beanie (no skull bleed-through), continuous chain, readable armor.

## How we rebuild traits (v2, quality-first)

1. **Always start from the full DNA base**  
   `work/legacy_v1_layers/wogrok_base_full_v1.png` (canonical line art).

2. **Generate a cohesive full character** with the trait(s) via image edit  
   Same head, same line weight, same deadpan face. Not a floating sticker.

3. **Then extract the layer** from that master:
   - **Opaque covers** (clothing, headwear, eyes): solid white (or color) fill
     + black lines; **no face/head leftover** in clothing; hats fully hide skull.
   - **Ink overlays** (mouth, chain, moon, tattoos): continuous dark strokes only;
     never sparse dotted garbage.

4. **QA on magenta** for every opaque layer: object only, no ghost face.
5. **QA composited** on base: must still look like Wogrok at 128px.

## What is forbidden

- Flat “open forehead” bases that make him look like a box
- PIL ellipse beanies / primitive shapes as final art
- Transparent outline-only clothing/hats
- Dotted chains from bad diff extraction
- Shipping anything that looks worse than the pre-layer master drawing

## Layer architecture still stands

See `LAYER_ARCHITECTURE.md` for stack order and opaque vs ink.
Architecture is right. **Execution must match the quality master.**
