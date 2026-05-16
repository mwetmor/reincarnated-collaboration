# Demo Visual Content R&D — Sprite + Ability + Gear Art Generation/Curation

**Captured:** 2026-05-10
**Library:** Pixi.js (per file 22 + 24's library decision)
**Scope:** companion document to file 24 — describes the iterative approach for generating or curating visual content for combatants, abilities, and gear in the Pixi.js demo. Read alongside file 24 (which is the implementation prompt).

## Why this is its own document

Visual content generation isn't a single phase — it's an iterative concern that runs *across* file 24's six phases. Each phase needs visuals at some level (Phase 1 needs placeholder combatants; Phase 4 needs distinct opponent visuals; Phase 5 needs gear icons; Phase 6 wants polish). The visual approach evolves as the demo matures.

Rather than scoping visuals into a single phase, this document describes the **tiered approach**: start with the cheapest, most-tractable visual pipeline (programmatic procedural), iterate upward as the demo matures (composed atoms → AI-generated → hand-crafted), and let family playtest feedback drive where to invest art effort.

## The metadata available from engine exports

The engine's JSON exports carry rich, structured metadata that drives visual content. Per entity type:

### Class (playable + act-bosses)
- **`name`**: LLM-generated, evocative ("Chalk-Dusted Schoolhouse Arsonist")
- **`archetype_label`**: emergent classification (warrior, mage, hunter, etc.)
- **`energy_type`**: rage / combo / focus / mana / stamina-as-resource
- **`range_profile`**: close / medium / long
- **`role_orientation`**: damage / support / control / hybrid
- **`damage_type`**: physical / fire / wind / water / earth / hybrid
- **`color`**: `{value: int, palette: list[int]}` — sampled from element's color band
- **`stats`**: STR / VIT / INT / WIS / DEX (informs visual proportions — strong = heavier, dexterous = leaner)

### Monster (gauntlet + trial bosses)
- Same dimensional metadata as classes
- **`tier`**: trash / standard / elite / boss (informs visual size and detail level)
- **`dominant_element`**: theme color
- **`name`**: LLM-generated; evokes archetype + element

### Ability (skills)
- **`name`**: LLM-generated ("Chalk Dust Gale", "Inferno Brand")
- **`geometry`**: ranged_physical / fire_blast / frost_nova / melee_strike / etc. (drives the *shape* of the visual effect)
- **`element`**: fire / water / wind / earth / physical (drives the *color* of the effect)
- **`cooldown_seconds`**, **`damage_magnitude`**, etc. (informs particle intensity / duration)
- **`color_value`**: per-skill color sample

### Gear (rare / epic / legendary)
- **`name`**: template (rare) or LLM (epic+) — "Glassworker's Edge", "Sturdy Iron Sword of Hearth"
- **`flavor_text`**: epic+ only, evocative description
- **`visual_prompt`**: epic+ only, LLM-generated *for downstream visual generation* (per file 17 § "Visual prompt field")
- **`base_type`**: sword / staff / robe / etc. (drives icon shape)
- **`tier`**: drives glow / border treatment
- **`color_palette`**: derived from gear's element flavor
- **`color_signature`**: legendary only, hex like `#A8472A`

This is rich, structured data. Visual generation can be driven directly from these fields without needing the LLM to "see" the visual outputs.

## Tiered approach — start cheap, iterate upward

Each tier has different cost, quality, and tractability. Use them in combination: Tier 1 as a baseline for everything; Tier 2 for combatants and gear icons that need more polish; Tier 3 for signature items where uniqueness matters; Tier 4 for the final art pass.

### Tier 1 — Programmatic procedural (baseline)

**Approach:** generate visuals entirely in Pixi.js code from metadata. No external assets.

**For combatants:**
- Body shape from archetype: warrior = heavy/blocky silhouette, mage = slim/tall, hunter = lithe/agile, etc.
- Color: primary body color from `color.value` (mapped to RGB via existing color spectrum); secondary accent from `color.palette[0]`
- Element accents: fire archetype shows ember particles around the sprite; water shows drop particles; earth shows stone fragments; wind shows trailing wisps
- Size: scaled by stat profile (high VIT = larger body; high DEX = leaner)
- Tier scaling (for monsters): trash = small, basic; elite = larger with one signature accent; boss = larger still with multiple particle effects
- Drawn via `PIXI.Graphics` API (rectangles, circles, polygons) plus `PIXI.ParticleContainer` for element effects

**For abilities:**
- Geometry drives shape: ranged_physical = projectile sprite (small elongated shape); fire_blast = expanding circle; melee_strike = swing arc; ground_targeted_circle = ground indicator + AOE animation
- Element drives color: fire = warm gradient (red→orange→yellow); water = cool gradient (blue→cyan); etc.
- Pixi.js particle effects via `@pixi/particle-emitter` library or hand-rolled emitter for element-themed particles
- Cooldown duration informs animation speed; damage magnitude informs particle count/intensity

**For gear (icons in inventory UI):**
- Base type drives shape: sword = vertical blade silhouette; staff = vertical with orb top; robe = trapezoid with arm-holes; etc.
- Color from `color_palette`: primary fill, accent border
- Tier drives glow/border: common = no glow, uncommon = subtle border, rare = thicker border, epic = soft glow, legendary = pulsing glow with `color_signature` hex
- Drawn as `PIXI.Graphics` icons (~64x64 px) for inventory UI

**For ground-state gear (dropped items awaiting pickup):**

When gear drops on boss defeat, the player needs to identify pickup-worthiness at a glance. Tier highlighting on the ground state communicates this without requiring inspection:

| Tier | Ground-state visual treatment |
|---|---|
| Common | Item lays on ground; no glow; small footprint |
| Uncommon | Subtle gray-white outline; mild static glow |
| Rare | Blue outline; gentle pulse |
| Epic | Purple outline; stronger pulse + faint glow halo |
| Legendary | Color from `color_signature` hex; bright pulsing glow + particle aura matching the gear's element |

Implementation in Pixi.js:
- Each ground-state item gets a `PIXI.Graphics` outline + a `PIXI.filters.GlowFilter` (or hand-rolled gradient)
- Pulse animation via Pixi ticker — sine wave over alpha or scale
- Legendary's particle aura uses the element-themed `ParticleContainer` from ability VFX
- The treatment is at-a-glance — a player scanning the ground after a boss kill should immediately see "the legendary is the bright purple-glowing item by the corpse"

**Why this matters:** the smuggling story (per file 17) lives at epic+. If a legendary drop looks indistinguishable from a common on the ground, the discovery moment is lost. Visual tier-grading on the ground is what makes "the third boss dropped THE [legendary name]" land emotionally.

**Pros:** zero external dependencies; deterministic per-seed; fully under our control; ships with demo1 with no asset wrangling
**Cons:** visual quality limited; might look "programmer art" without careful design discipline
**Best for:** placeholder; first-iteration visuals; ability VFX (where procedural is genre-standard regardless of tier); HUD elements

**Tractability for Claude CLI:** HIGH. Claude writes the code; outputs are deterministic; iteration is fast.

### Tier 2 — Composed sprite atoms from open libraries

**Approach:** use existing free/open-source sprite assets (Kenney.nl, OpenGameArt.org, itch.io free packs) as building blocks; composite via Pixi.js sprite layering.

**Source libraries to evaluate:**
- **Kenney.nl** — high-quality permissive (CC0) game asset packs; includes RPG character packs, weapon icons, particle effects. Excellent starting point.
- **OpenGameArt.org** — community-contributed sprites; mixed licenses (check per asset); huge variety of RPG/ARPG sprites
- **itch.io free asset packs** — many ARPG-style sprite packs available for free or pay-what-you-want

**For combatants:**
- Library has body sprites by archetype (warrior, mage, archer, rogue, etc.) — pick by `archetype_label`
- Equipment overlays (helmet, armor, weapon) — pick by gear class_fit_profile or class energy_type
- Element accents added via Tier 1 particle effects on top of the composed sprite
- Composite at runtime: `PIXI.Container` with sprite layers (body → equipment → accents → particles)

**For abilities:**
- Library has spell/attack effect sprites — projectile assets, AOE rings, particle effects
- Pick by geometry; tint by element color (Pixi.js sprites support tint modulation)

**For gear (inventory icons):**
- Library has weapon/armor icons in many tiers — pick by base_type, tint by color, overlay tier-based glow

**Pros:** much higher visual quality than Tier 1; cohesive ARPG aesthetic; existing art is battle-tested
**Cons:** licensing/credit considerations (CC0 ideal; CC-BY requires attribution; some packs have their own terms); style consistency across atoms requires curation; may need to filter to atoms in similar art style
**Best for:** combatants (most user-visible); gear inventory icons; ambient detail

**Tractability for Claude CLI:** MEDIUM. Claude can fetch + integrate sprite atoms but needs the library inventory described/explored first. The agent should download sprite packs, inventory them, and write a mapping function from class metadata → atom selection. Iterate by spot-checking which mappings produce sensible combinations.

### Tier 3 — AI-generated sprites (signature items)

**Approach:** call image generation APIs (Stable Diffusion, DALL-E) with structured prompts derived from LLM metadata. Cache generated sprites per entity.

**Practical pipeline:**
- For legendary gear: combine `name + flavor_text + visual_prompt + color_signature` into a structured prompt:
  > "Pixel art icon, 64x64, isolated on transparent background. Item: [name]. Flavor: [flavor_text]. Visual: [visual_prompt]. Dominant color: #[color_signature]. ARPG game asset style, clean silhouette, single-color background."
- Send to image generation API; receive sprite; cache to `assets/generated/legendary_<id>.png`
- Cache is keyed by gear instance ID (deterministic); only regenerate if missing
- For class portraits (signature image per class): similar approach with class metadata
- For regular abilities: probably skip Tier 3; Tier 1 procedural is good enough

**API options:**
- **Stable Diffusion** via Replicate / Together / local: fastest; cheapest at scale; good for sprites with prompt engineering
- **DALL-E 3** via OpenAI: highest quality; more expensive; better at following structured prompts
- **Midjourney** via Discord: high quality but harder to automate

**Cost estimate:** ~$0.005-0.04 per image depending on model and provider. For demo1: ~80 legendary items × ~10 seasons + ~50 class portraits ≈ ~850 images ≈ $5-30 one-time cost. Cached afterward.

**Pros:** highest visual quality and uniqueness; signature items feel distinct; legendary drops have memorable art
**Cons:** API integration + cost; quality variance (some generations will be unusable; need retry logic); style cohesion requires careful prompt engineering; legal considerations (training data, commercial use clauses)
**Best for:** legendary items (the "this is special" moments); class signature portraits; trial bosses

**Tractability for Claude CLI:** MEDIUM-HIGH. Claude can write the API integration code, prompt engineering logic, and caching pipeline. Quality evaluation needs human-in-the-loop (you/your son spot-check generated images).

### Tier 4 — Hand-crafted (post-MVP)

**Approach:** human artist (or AI-art-curated by your son) creates final-pass art for the demo's signature moments.

**Scope:** likely post-demo1 enhancement. Could be:
- Family collaborator's son does art direction → human artist or family member creates sprites
- AI-generated images (Tier 3) curated and refined by hand
- Sprite atom packs commissioned from itch.io artists

**Best for:** the eventual game ship; demo1 doesn't need this.

## Iterative workflow for the demo CLI agent

The demo CLI agent should approach visual content as **continuous R&D** alongside the six phases of file 24:

1. **Phase 1 (setup):** Tier 1 only. Placeholder colored shapes for combatants; basic Graphics-API ability animations. Goal: prove the rendering pipeline; visual quality is irrelevant.

2. **Phase 2 (one ability end-to-end):** Tier 1 procedural for the chosen ability. Iterate on the ability VFX until it *feels* like the ability's name + element + geometry. This is the visual "voice" of the demo.

3. **Phase 3 (all abilities + statuses):** Extend Tier 1 procedural to cover all geometry types. Status effects (burn, slow, stun) get visible UI indicators.

4. **Phase 4 (gauntlet):** Tier 1 still for combatants. Add Tier 2 evaluation as a side investigation: download Kenney.nl RPG pack; write a sprite atom mapping function; spot-check whether composed sprites look better than procedural shapes. If yes, switch combatant rendering to Tier 2; if no, stay on Tier 1.

5. **Phase 5 (gear drops + inventory):** Tier 1 for gear icons (procedural shapes by base_type + color). Tier 3 evaluation as a side investigation: implement the AI-generation pipeline for legendary items; generate ~5-10 sample legendaries; show family for visual evaluation. If quality is good, integrate; if not, stay on Tier 1.

6. **Phase 6 (polish + multi-season):** Final visual pass. Whichever tier mix produced best results in earlier phases is the demo's final visual approach. Family playtest evaluates which entities feel weakest visually; targeted iteration there.

## Family collaborator role in visuals

The project owner's son contributes most heavily to visual evaluation:
- Phase 4: which combatant sprites feel most/least alive? Procedural vs. composed?
- Phase 5: which gear icons feel most exciting? Are AI-generated legendaries worth the integration cost?
- Phase 6: full-pass visual playtest — what feels weakest, what feels strongest, where to invest art effort

Engage him as the visual judge. He sees the output; he says what looks good. The CLI agent implements; the family validates.

## What to do if a tier doesn't pan out

**Tier 1 too "programmer art":** that's expected; don't fight it. Tier 1's job is to make the rendering pipeline real and the metadata-to-visual mapping concrete. Tier 2 is the upgrade path.

**Tier 2 sprite atoms don't match the engine's element flavors:** look for a different sprite pack or fall back to Tier 1. The engine's elements (fire/water/wind/earth/physical) are common ARPG categories; most RPG sprite packs have coverage. If a specific element (e.g., wind) is underserved, supplement with Tier 1 procedural particles.

**Tier 3 AI generations are inconsistent:** prompt engineering improves results dramatically. Add style anchors ("pixel art, clean silhouette, isolated on transparent background, ARPG game asset"). If still inconsistent after prompt iteration, fall back to Tier 2 + Tier 1.

**Style cohesion across tiers feels off:** pick one tier as the "anchor" style (probably Tier 2 if available, else Tier 1) and constrain other tiers to match. AI-generated sprites can use prompts that reference the anchor style.

## Acceptance criteria for visuals at demo1 ship

By end of demo1, the visual layer should:

1. **Each combatant is visually distinct** — a fire mage looks different from a hunter looks different from a warrior. Distinction comes from any combination of body shape, color, element accent, equipment overlay.
2. **Each ability is visually intelligible** — the player sees an ability fire and immediately understands what's happening (projectile vs AOE vs melee swing) and what element it is (fire vs water vs etc.) without reading the name.
3. **Gear tier is at-a-glance distinguishable** — common items look basic, legendaries look special. Glow / border / color saturation makes tier obvious.
4. **The season's element flavor lands visually** — a "chalk" earth season feels chalky (whitish, dusty); a "hearth" fire season feels warm (orange-red, ember-strewn). Color data + element-themed particles deliver this.
5. **Family collaborator's son can identify content** — if he plays, can he tell which class he's playing, which abilities are doing what, which gear is most valuable?

These don't require Tier 3 or 4 to be hit. Tier 1 + good design discipline can satisfy all five for a demo. Tier 2/3 enhance quality; they don't unlock the criteria.

## What's NOT in scope for visual R&D

- **Animation systems** beyond simple frame-by-frame or tween (no rigged skeletal animation; no full character animation cycles in demo1)
- **Custom shaders** beyond what Pixi.js's built-in filters provide (no GLSL development)
- **Procedural map generation** (demo1 has a single arena; demo2 may add themed maps)
- **Audio/music** (separate concern; not visual)
- **Real-time AI art generation during gameplay** (cache hits only; no on-the-fly generation that affects frame timing)

## Cross-references

- File 22: companion-track scope for the demo + data export
- File 24: demo1 implementation prompt (this doc is its companion for visual scope)
- File 17 § "Color integration": the engine's color system that visual content draws from
- File 17 § "Visual prompt field": how the engine pre-stages content for downstream visual generation
- File 19: LLM call map (no LLM calls happen in the demo; this document references AI image generation, which is separate)

## Status checkpoints

Update as visual R&D progresses:

- [ ] Tier 1 procedural pipeline established (combatants, abilities, gear icons)
- [ ] Tier 2 evaluation completed — decision on whether to integrate composed sprite atoms
- [ ] Tier 3 evaluation completed — decision on whether to integrate AI-generated legendaries
- [ ] Family playtest #1 (visual feedback after Phase 4)
- [ ] Family playtest #2 (visual feedback after Phase 5)
- [ ] Final visual pass + style cohesion check (Phase 6)
- [ ] Demo1 ships with [TIER MIX TBD] as visual approach
