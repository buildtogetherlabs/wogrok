# Design notes

## Why this model works

LEL / classic generative Wojak collections often vary the **face itself** (dozens of expressions as separate bases). That creates variety but dilutes recognition.

Wogrok inverts it:

- **DNA is the product** — exhausted asymmetric blank stare
- **Traits are biography** — which trade, which cope, which delusion

A HODL-cap + laser-eyes + ramen hoodie Wogrok is still obviously the same guy who shows up in a tuxedo with dollar pupils. That's the brand.

## Rarity intuition (not final)

| Category | Common bias | Rare energy |
|---|---|---|
| Eyes | Normal, sleepy | Laser, glitched, fire, rainbow, VR |
| Mouth | None, stubble | Gas mask, diamond teeth, bubble gum |
| Headwear | None, beanie, baseball | King crown, astronaut, devil horns |
| Clothing | Hoodies, tees | Fur coat, king robe, prison, cult |
| Special | None | Tiny Pepe, glitch, diamond hands + rocket |

Weights live in `config/traits.json` and will be tuned after art exists.

## Collection size

`config/rules.json` starts at **5,555** (placeholder). Combo space with current lists is ~170M before rules — size is a product decision, not a technical limit.

## Open decisions

- [ ] Final supply number
- [ ] Background set expansion (colors / subtle textures)
- [ ] Whether clothing is mandatory vs includes `none` (shirtless base)
- [ ] Max specials per mint (0–1 vs 0–2)
- [ ] 1-of-1 super-rares outside normal stack
- [ ] Transparent isolation of base (remove white fill for non-white backgrounds)
