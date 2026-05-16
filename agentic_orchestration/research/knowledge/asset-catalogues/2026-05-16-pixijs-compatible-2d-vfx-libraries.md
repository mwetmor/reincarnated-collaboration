# 2D VFX libraries — PixiJS-compatible sources

**Filed:** 2026-05-16
**Source:** External Claude conversation (researcher unknown to this team; contributed by Matt)
**Purpose:** Initial knowledge base for Legolas's Mode B catalogue crawl scoping. Becomes part of Gandalf's onboarding reading. Style-register decision (see `canonical/story/style-register.md` once Gandalf authors it) will determine which of these sources receive priority.

**Status:** Raw external research. Elrond should curate this into structured catalogue-source tags + scoping notes as part of catalogue-crawl onboarding.

---

## Sources (free or freemium)

### itch.io — largest single repository of indie 2D VFX

Best vendors there for spell/ability VFX:

- **pimen** — fire, water, ice, holy, dark, earth, wind spell effects (handmade animated sprite sheets, very high quality)
- **ansimuz** — Free Magic Pack 9, Magic Pack 4 (general VFX, retro pixel style)
- **Pipoya** — FREE VFX series (Time Magic, Warp Portal, HEX Shield, Light Pillar)
- **Frostwindz** — Pixel Art VFX Lightning (free)
- **Foozle** — Pixel Magic Effects (10 effects: 2 Fire, 2 Earth, 2 Wind, 2 Water, Portal, Explosion)
- **Brackeys' VFX Bundle** — free, broad coverage
- **CreativeKind** — paid hand-drawn pixel spell sets (Water, Earth, Color, Magic Spell Effects)
- **unTied Games** — Five Free Pixel Explosions, 60-FPS pixel particles
- **Elthen's Pixel Art Shop** — paid character + spell sets
- **ppeldo** — 2D Pixel-art game spell/magic FX
- **LuizMelo** — character + effect packs

### OpenGameArt.org — free CC-licensed VFX

Coverage: explosions, lightning, fireballs, auras, shields, charge effects, energy balls, power rings, sparkles, flame particles, runic alphabets, zodiac/planet symbols. Quality variable; licensing permissive.

### CraftPix.net — mostly paid, freebies section

~$5-15/pack. Royalty-free commercial. Notable packs:

- Free Pixel Magic Sprite Effects Pack (free) — healing, blink, roots, damage aura, laser, spark, charm, starfall, petrification, invisible
- Magic Spells Pixel Art Sprite Pack — bamboo wall, summoning, ball lightning, tornado, freeze, spear, attack sphere, arrows, healing, icicle
- Magic Effects Pixel Art Asset Pack 4 — swords, death punch, acid, bubble, fire, poison, implosion
- Fire Magic Effects Pixel Art — 11 fire-specific effects
- Pixel Art Magic Sprite Effects and Icons Pack — water ball, explosion, fire, firewall, lightning (×2), Midas hand, spikes, spiral, sun strike
- Free Water and Fire Magic Sprite Vector Pack — vector format, scales cleanly

---

## Element coverage across sources (consolidated vocabulary)

### Tier 1 — extremely well-covered (multiple full packs from multiple vendors)

Fire, Ice/Frost, Lightning/Electric, Water, Earth/Stone, Wind/Air, Holy/Light, Dark/Shadow, Poison/Acid, Explosions/Impacts

### Tier 2 — solid coverage (at least one full pack)

Healing/Life, Arcane/Generic Magic, Portal/Warp, Shield/Barrier, Slash/Blade, Summon, Time/Temporal (Pipoya Time Magic specifically)

### Tier 3 — niche but available (single packs, often pixel-only)

Implosion/Gravity (useful for "vacuum"), Petrification, Charm/Mind, Starfall/Cosmic, Roots/Nature, Blink/Teleport short-range, Spiral/Vortex (useful for "deep vortex"), Midas/Transmutation, Sun Strike/Pillar

---

## PixiJS workflow notes

- Cleanest workflow: sprite sheets with JSON atlases (TexturePacker, Aseprite, or Free Texture Packer)
- Most vendors above ship PNG sequences or sprite sheets directly
- Pipoya, CreativeKind, pimen, CraftPix packs typically already in sprite sheet format
- Load via `PIXI.Assets.load()` or `PIXI.AnimatedSprite.fromFrames()`

---

## Mapping to engine's novel canonical-element variants

Pre-locked pairings (from external conversation; verify against doc 37 § 6 cipher architecture):

- **Vacuum** → Wind family + Spiral/Vortex assets, palette-shifted dark
- **Pressure** → Earth family + Implosion + impact distortion overlays
- **Plasma** → Fire + Lightning composite
- **Void** → Dark + Implosion + Portal-edge effects
- **Cosmic** → Holy + Starfall + Spiral

All buildable from the libraries above with no custom commissioning needed.

---

## Pragmatic shopping list (external conversation's v1 recommendation)

- Brackeys' VFX Bundle (free baseline)
- ansimuz Free Magic Pack 9 + Magic Pack 4 (~$5)
- pimen's full element spell effect series (~$3-5 each, get all 8 elements — this is the core)
- Pipoya's full FREE VFX series
- CraftPix Magic Effects Pixel Art Asset Pack 4 (composite/unusual effects)
- CraftPix Magic Spells Pixel Art Sprite Pack (vortex, ball lightning, freeze, etc.)

**Total:** 200-400 distinct effects covering all Tier 1 + most Tier 2/3 niches. Under $100. All royalty-free commercial.

---

## Critical style-register observation (verbatim from source)

> *"The libraries above are predominantly pixel art style. If your engine is targeting higher-fidelity 2D (hand-drawn, vector, or HD raster), you'd want to filter more aggressively toward CraftPix's vector packs and CreativeKind's hand-drawn sets, and away from the retro pixel vendors. The style coherence problem we discussed earlier applies: mixing pixel-art VFX with hand-drawn characters reads badly. Pick a style register first, then curate within it."*

This is the load-bearing finding that justifies a project-level style-register decision (Gandalf's domain) and a score-don't-filter catalogue approach (Legolas + Elrond's domain).

---

## Notes for downstream agents

**For Legolas (Mode B):** These are the priority Tier-1 sources to sample first. Crawl broadly across style registers; score/tag style at extraction or curation time. Don't pre-filter by current locked register.

**For Elrond (curation):** Each asset row should carry style-register tags as a curated dimension. Recommended initial registers: `pixel-art`, `hand-drawn`, `vector`, `hd-raster`, `mixed`. Refine as patterns emerge.

**For Gandalf (style-register decision):** The Tier-1/Tier-2/Tier-3 element vocabulary above gives empirical grounding for which elements have asset support across registers. Use this when picking the project's style register and when reviewing whether novel canonical-element variants (vacuum, plasma, void, cosmic) have viable visual representation.

**For Drax (consumption):** When the engine generates a season with locked style register, the loadout / demo pipelines filter the catalogue by that register tag. If the project pivots register later, the same catalogue serves the new register without re-crawl (assuming sufficient coverage).
