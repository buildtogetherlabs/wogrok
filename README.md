# WOGROK

One exhausted Wogrok who has lived a thousand crypto lives.

Not 25 different Wojaks — **one immutable character**. Traits tell the story.

## The pitch

You should recognize a tiny 128×128 Wogrok silhouette **before** you know which traits you're looking at.

- Same head, same deadpan energy, same asymmetric eyes
- Eyes / mouth / headwear / clothing / special stack on top
- Every mint is a different life Wogrok has lived in crypto

## Immutable DNA (never redraw these)

| Feature | Rule |
|---|---|
| Head shape | Fixed oval / bald |
| Line style | Black line, same weight |
| Hair | **None** — no wigs, no hair traits |
| Eyebrows | **None** |
| Nose | Tiny, same geometry |
| Mouth base | Same horizontal deadpan |
| Left eye | Flatter / squashed |
| Right eye | Rounder |
| Left pupil | Smaller |
| Right pupil | Larger |
| Under-eye | Tired bag under left eye |
| Energy | Blank / deadpan |

Full write-up: [`docs/BASE_DNA.md`](docs/BASE_DNA.md)

## Trait categories

| # | Category | Role |
|---|---|---|
| 1 | **Eyes** | Additions *on* Wogrok eyes — never change the asymmetry |
| 2 | **Mouth** | Props / facial hair / gore *around* the same mouth |
| 3 | **Headwear** | Things on his head only (no hair) |
| 4 | **Clothing** | Largest set — keep silhouette simple |
| 5 | **Special** | Tattoos, jewelry, crypto objects, meme effects |

Catalog: [`config/traits.json`](config/traits.json) · Queue: [`template/TRAIT_QUEUE.md`](template/TRAIT_QUEUE.md)

## Layer stack (bottom → top)

```
background
  + base          ← immutable full Wogrok (face DNA locked)
  + clothing      ← simplified, fitted to shoulders/neck
  + mouth         ← cigarette, beard, mask, etc.
  + eyes          ← overlays / glasses / pupil swaps
  + special       ← tattoos, chains, props, effects
  + headwear      ← hats, horns, halo
```

## Layout

```
layers/
  base/wogrok_base.png     # canonical DNA
  background/              # solid fills
  eyes/ mouth/ headwear/ clothing/ special/
style_ref/base/            # original source art (do not mint as-is)
template/                  # production docs + references
config/                    # traits, rules, canvas
scripts/                   # generate / preview (coming next)
```

## Open these first

| File | Why |
|---|---|
| `layers/base/wogrok_base.png` | The only base — lock alignment to this |
| `docs/BASE_DNA.md` | What must never change |
| `docs/PRODUCTION.md` | How to draw trait layers |
| `template/TRAIT_QUEUE.md` | Checklist of every trait to draw |
| `config/traits.json` | Machine-readable catalog |

## Status

- [x] Repo + design DNA
- [x] Trait catalog (eyes / mouth / headwear / clothing / special)
- [x] Base character locked in
- [x] All individual trait layers drawn (201)
- [x] Contact sheets + combo previews
- [x] Compose preview script
- [ ] Transparent base isolation for non-white backgrounds
- [ ] Collection generator + metadata
- [ ] Collection size + rarity weights finalized

## Related

Sibling project: LEL (`wojak-collection`) — multi-face white Wojak PFPs.  
Wogrok is the opposite model: **one face, many lives**.
