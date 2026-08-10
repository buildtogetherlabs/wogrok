# Production guide

> **See [LAYER_ARCHITECTURE.md](LAYER_ARCHITECTURE.md) for v2 opaque vs ink rules.**

# Production guide

## Layer model

Stack **bottom → top** (clothing always lands cleanly on the base before face props):

```
background
  → base          (immutable DNA)
  → clothing      (hoodie / shirt — solid fills win over lower face props)
  → mouth         (beard, cigarette, mask — ink only, no white)
  → eyes
  → special
  → headwear
```

| Layer | Path | Notes |
|---|---|---|
| Background | `layers/background/*.png` | Solid (or simple) fills |
| **Base** | `layers/base/wogrok_base.png` | Immutable DNA — never regenerate casually |
| Clothing | `layers/clothing/*.png` | Fit collar + shoulders; leave face clear |
| Mouth | `layers/mouth/*.png` | Props / hair / masks around base mouth |
| Eyes | `layers/eyes/*.png` | Overlays on locked sockets |
| Special | `layers/special/*.png` | Tattoos, chains, props, effects |
| Headwear | `layers/headwear/*.png` | On skull; clear of face features unless intentional brim |

**Critical compositing rules**
1. Clothing is drawn **before** mouth (base → clothing → mouth).
2. Clothing / mouth / headwear / special layers are **ink-only** (no opaque white). White “erasers” punch holes through layers underneath — only eyes may use erasers for pupil swaps.
3. When clothing has a solid fill (black hood interior, etc.), mouth/special pixels under that fill are suppressed so clothing still looks like the solo-trait version.

Stack order is also in `config/traits.json` / `config/canvas.json` → `layer_order`.

## Canvas

- **1000×1000** PNG, RGBA
- Transparent background on trait layers (only the trait pixels)
- Align every trait to `layers/base/wogrok_base.png`

## Drawing a trait

1. Open `layers/base/wogrok_base.png` locked underneath (or workbench when available).
2. Draw **only the trait** — do not redraw head, nose, base eyes, or base mouth lines unless the trait explicitly covers them (mask, sunglasses).
3. Match black line weight to the base.
4. Keep clothing extremely simplified — Wogrok must still read as Wogrok.
5. Export transparent PNG → `layers/{category}/{id}.png`
6. Check off the row in `template/TRAIT_QUEUE.md`
7. Mark `"status": "done"` in `config/traits.json` when the file is final

## Eyes rules (critical)

- Sockets stay: left flatter, right rounder
- Pupils stay size-asymmetric unless the trait *replaces* pupil content ($, ₿, hearts, spirals) **inside** the same sockets
- Glasses / goggles / patches sit on top of the anatomy
- No "fixing" the asymmetry for aesthetics

## Mouth rules

- Deadpan mouth line remains unless covered (bandana, gas mask)
- Comedy comes from **dead face + ridiculous prop** (joint, lollipop, bubble gum)
- Facial hair grows *around* the mouth geometry

## Headwear rules

- No hair / wigs
- Sit on the bald skull; brim height consistent across caps
- Crypto text hats (HODL / DEGEN / NGMI / WAGMI) should be instantly readable

## Clothing rules

- Largest category — still the most simplified drawing
- Collar joins neck cleanly; no floating shoulders
- Text hoodies/shirts: bold, few words (HODL, WAGMI, REKT, ALL IN)

## Special rules

- Face tattoos follow head curvature; don't look stamped-on flat
- Chains/jewelry hang on neck/chest above clothing
- Held objects (phone, ledger, pizza) sit in lower corners without crushing silhouette
- Effects (glitch, flames, lightning) must not erase DNA at thumbnail size

## QA checklist

- [ ] Recognizable as Wogrok at 128×128
- [ ] Left eye still flatter than right
- [ ] No accidental eyebrows or hair
- [ ] Line weight matches base
- [ ] No shoulder gaps / floating clothes
- [ ] Transparent PNG, 1000×1000
- [ ] File id matches `config/traits.json`
