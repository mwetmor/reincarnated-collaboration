# Curator Tagging Guide — Six-Axis Style Rubric

**Status:** **Locked v1.0** as of 2026-05-16 (post-gandalf dialogue).
**Author:** elrond.
**Audience:** curators (currently elrond; future: any curator-role agent or human contributor).
**Companion:** `catalogue-rubric-schema.md` (the axis definitions), `catalogue-schema.md` (the DB columns), `curation-pipeline.md` (the operational flow), `catalogue-rubric-validation-2026-05-16.md` (worked validation pass).
**Purpose:** make curator-tagging convergent. Two different curators looking at the same asset should arrive at the same value-set across all six axes.

---

## 0. The standing rule

> **If you and another curator disagree on more than one axis for the same asset, that's a rubric bug. Surface it; don't paper over it.**

The rubric's job is to be checkable. The guide's job is to make the checks concrete. When this guide fails to make a check concrete, refine the guide — or refine the rubric.

---

## 1. The curator's workflow per asset

For each asset Legolas surfaces in raw output:

1. **Open the asset.** Either Legolas captured a preview URL, or you fetch it. You need to *see the sprite at sprite-resolution and at 4x zoom* to tag the axes well.
2. **Note source-anchor info** from Legolas raw: `source`, `source_asset_id`, `source_url`, `name`, `crawl_session_id`. These are unchanged.
3. **Determine `category`** (§ 2 below). What does the asset depict?
4. **Determine `dimensionality`.** Almost always `2d` in our scope. `3d` only for the rare asset.
5. **Determine `embodiment_tag`** if `category IN ('character', 'enemy')`. See § 3.
6. **Tag axes 1-5** (§ 4-8). Each axis: visual inspection produces one value from a closed set.
7. **Apply the deterministic rule for axis 6** (`catalogue-rubric-schema.md` § 3). If output is `manual-review`, queue and stop here for this pass.
8. **Curation pipeline auto-applies side-effects:** `outline-profile` tag (R6); `quality_flag = 'borderline'` (R7); license-default `quality_flag`.
9. **Record license + cost** (§ 9). License is NULL-forbidden.
10. **Record `decomposition`** (§ 10). Critical for drax's wiring track.
11. **Record `quality_flag`** if you're making the call directly. Default `unreviewed` unless rubric or license auto-flags.
12. **Insert the row.** Curation script writes it with `curated_at`, `curated_by`, audit-trail.

If any axis can't be determined from inspection, set the value to `unknown` and move on. The curation-pipeline `manual-review-queue` surfaces all `unknown` values for a follow-up pass.

---

## 2. Determining `category`

What does the asset depict?

| Value | Use for | Examples |
|---|---|---|
| `character` | Player-controllable or playable-class sprites | LuizMelo Adventurer, Elthen Wizard, Pipoya Free RPG Character Pack |
| `enemy` | Non-player enemy / monster sprites | LuizMelo Skeleton, ansimuz Pirate, pimen Skeleton-Boss |
| `vfx` | Spell effects, particle effects, impact effects | pimen Fire Spell Effects, ansimuz Magic Pack, Frostwindz Lightning |
| `environment` | Backgrounds, parallax layers, world tiles (as composite) | ansimuz Sunny Land, Foozle Tropical World |
| `tile` | Individual tileset pieces (terrain, walls, props) | Pipoya RPG tilesets, CraftPix tilesets |
| `ui` | Buttons, HUD frames, menu chrome | CraftPix UI packs |
| `audio` | Music, SFX (catalogue may include later — currently rare) | n/a in current scope |
| `icon` | Item icons, inventory icons | CraftPix Icon Pack series |
| `portrait` | Character portrait illustrations | CreativeKind Portrait packs |
| `other` | None of the above; describe in `notes` | edge cases |

**Decision rule:** what would the asset *most likely be deployed as* in a game? A spell-effect sprite-sheet is `vfx` even if it depicts a character casting a spell. A character-sprite-sheet is `character` or `enemy` even if it includes idle/attack/spell animations. Portraits get their own value because they typically render at narrative-moment-tier rather than combat-tier.

**Special rule:** if uncertain between `character` and `enemy`, default to the vendor's framing. LuizMelo packs labeled "Skeleton" are `enemy`; labeled "Adventurer" are `character`. Both pools may serve either role downstream — Drax's monster-sprite registry consumes from both — but the catalogue records the vendor's intent.

---

## 3. Determining `embodiment_tag`

Required when `category IN ('character', 'enemy')`; leave `not-applicable` otherwise (or `NULL` per schema — `not-applicable` is the explicit value when the row corresponds to a creature-adjacent asset that doesn't have a form, like a creature's spell-effect sprite-sheet).

Compare the sprite to the eight starter embodiments from `embodiment-narrative-layer.md` § 1:

| Embodiment | Look for | Common asset examples |
|---|---|---|
| `humanoid` | Bipedal, two-armed, head-bearing | Most Pipoya / LuizMelo / Elthen character packs |
| `slime` | Amorphous body, no clear bipedal silhouette, core/nucleus | Pipoya Free RPG Monster (slime variants), Foozle slime sprites |
| `beast` | Bipedal-or-quadrupedal animal-form (cat/wolf/fox/bear/etc.); claws, fangs, tail | LuizMelo Werewolf, Pipoya wolf/cat monster sprites |
| `dragonling` | Scaled body, wings often present, fire-breath posture common | CreativeKind Dragon pack, various dragon-kin assets |
| `swarm` | Multiple bodies operating as cluster; insects, rats, ant-swarm | Rare in current asset scope; Foozle bat-swarm |
| `construct` | Stone/crystal/metal/wood body; non-organic | Pipoya Golem, ansimuz Robot |
| `spirit` | Translucent, ethereal, ghost/mist; not anatomically clean | Pipoya Ghost, ansimuz Wraith |
| `plant` | Plant-bodied; vines/leaves/flowers as anatomy | rare; some adventure-pack mushroom-creatures and treefolk |

**If the asset depicts a form NOT in the starter set** (undead-skeleton, mecha, demon, vampire, merfolk, deity-form, etc.):
- Set `embodiment_tag = 'pending-amendment'`.
- Populate `pending_amendment_hint` with a short read: `'undead-skeleton'`, `'mecha-form'`, `'demon-quadrupedal'`, `'aquatic-merfolk'`, etc.
- The asset is still fully tagged on style axes, license, decomposition. It only blocks embodiment-specific filtering until the narrative-layer amendment lands.

**Why not pre-load the enum:** per gandalf dialogue Topic 4, expansion-protocol slots carry narrative-layer implications (what spirit-guide says when player encounters one, how the form integrates with reincarnation lore). Pre-loading the catalogue would let asset-availability define narrative canonicity. The amendment-gated path forces the narrative work to land first.

**If `category IN ('character', 'enemy')` but you genuinely can't tell what form it is** (heavily stylized, abstract, blob-with-features): use `unknown` and surface in curator notes.

---

## 4. Axis 1 — `resolution_band`

**Question:** what's the typical character-body / single-sprite-frame canvas size?

**How to determine:**
- Most vendors list canvas size in the asset description. If listed, use it.
- If the asset is a sprite-sheet, individual frame size is the canvas size.
- For VFX assets (no body), use the effect-frame canvas size.
- For multi-piece decomposed packs (separate head/body/weapon), use the *body* piece's canvas size.

**Value cheat-sheet:**

| If canvas... | Tag as | Vendor cluster |
|---|---|---|
| 16x16 or smaller | `tiny` | rare in our scope |
| 24x24 – 32x32 | `retro` | Pipoya Free RPG packs, ansimuz Free Magic Pack, lower-tier Foozle |
| 32x48 – 48x64 | `hd2d-pixel` | CreativeKind general, Elthen Wizard, mid Foozle, mid pimen |
| 64x64 – 96x128 | `hd2d-pixel` (still) | LuizMelo character packs, pimen spell effects, CraftPix Magic packs |
| 96x96 – 128x128 | `narrative-pixel` | CreativeKind Portrait-tier, higher-tier ppeldo |
| 128x128 – 256x256 | `cinematic-pixel` | CreativeKind narrative-moment-tier, large-canvas hand-drawn pixel |
| 256+ px or non-pixel raster | `raster` | painterly-raster catalogue rare in current scope |
| SVG, vector format | `vector` | CraftPix vector packs |

**Decision rule for ambiguous boundaries:** the cluster boundary at 64px is a soft seam between `hd2d-pixel` and `narrative-pixel`. Use `hd2d-pixel` for combat-action sprite-sheets; `narrative-pixel` for static/illustrative-leaning assets (portraits, narrative moments). If unsure, prefer `hd2d-pixel` — narrative-pixel is the rarer category.

---

## 5. Axis 2 — `palette_size`

**Question:** how many distinct colors does the asset use?

**How to determine:**
- Many vendors list "x-color palette" in asset descriptions. Use if listed.
- If not listed, open the sprite in an image tool (Aseprite, GIMP, Photoshop, even a web-based color-count tool) and count unique colors.
- "Distinct colors" excludes near-duplicates from anti-aliasing IF the palette is restricted. For truecolor assets, count is approximate (≥256 is "truecolor").

**Value cheat-sheet:**

| Count | Tag as |
|---|---|
| 1-16 | `16-color` |
| 17-64 | `restricted` |
| 65-256 | `expansive` |
| 257+ (effectively photo-class) | `truecolor` |

**Visual shorthand if you can't count:**

| Looks like... | Likely... |
|---|---|
| Classic NES / 16-bit register; very limited color choices visible | `16-color` (rare in modern asset packs) |
| Retro pixel-art with banded shadows; small but distinguishable palette | `restricted` (Pipoya, ansimuz, classic Foozle) |
| Hand-drawn pixel-art with dithering and gradient ramps; rich palette but still pixel-discrete | `expansive` (CreativeKind, Elthen, pimen, higher Foozle) |
| Smooth gradients, painted-feel, photo-coded | `truecolor` (raster painterly) |
| Vector with fill regions | `truecolor` or `expansive` per fill richness; usually `expansive` for vector |

**Combining with axis 3:** if shading is `flat-fill` or `single-step`, palette is almost always `16-color` or `restricted`. If shading is `dithered` or `gradient-ramp`, palette is almost always `expansive`. If `painterly`, palette is `truecolor`. Cross-axis incoherence flags a tagging-bug (see catalogue-rubric-schema.md § 4 constraint C1-C5).

---

## 6. Axis 3 — `shading_technique`

**Question:** how does the asset handle shading on a curved or shadowed surface?

**How to determine:**
- Open a sprite (one with a curved body like an arm or torso) at 4x zoom.
- Inspect how the sprite transitions from light to shadow.

**Value cheat-sheet:**

| Looks like... | Tag as | Examples |
|---|---|---|
| One flat color per region; no shadow at all | `flat-fill` | UI-pixel assets, some minimal-mode Pipoya |
| Base color plus one banded darker step | `single-step` | Classic Pipoya, ansimuz, lower Foozle |
| Pixel-noise patterns approximating gradient (checkerboard / Bayer dither) | `dithered` | Classic hand-drawn pixel: CreativeKind, Elthen, higher Foozle |
| Smooth multi-step color ramps, pixel-coherent (each step is its own ramp color, not noise) | `gradient-ramp` | pimen, CreativeKind ramp-style, higher-tier CraftPix pixel |
| Brush-stroke evidence visible; not pixel-grid-coherent | `painterly` | Raster painterly assets |
| Vector regions filled flat or with vector-gradient | `vector-flat` | CraftPix vector packs |

**Combining with axis 4:** if shading is `painterly`, linework is almost always `no-outline` or `soft-outline` — `painterly + hard-1px-outline` is constraint-violation territory.

---

## 7. Axis 4 — `linework_style`

**Question:** how does the asset's edge / outline read?

**How to determine:**
- Zoom in on a sprite edge (silhouette boundary).

**Value cheat-sheet:**

| Looks like... | Tag as | Examples |
|---|---|---|
| Uniform 1-pixel black or dark border around every shape | `hard-1px-outline` | Pipoya, ansimuz, classic Foozle, **CreativeKind hand-drawn**, ppeldo |
| Outline present but anti-aliased / color-modulated (not pure black) | `soft-outline` | Some higher-tier CreativeKind, hand-drawn-leaning packs |
| Outline thickness varies along the sprite (thicker at silhouette, thinner at details) | `variable-width` | Hand-drawn-illustration sensibility: many narrative-moment-tier packs |
| Sprite shaded without explicit border; silhouette is shading-edge | `no-outline` | Some painterly, some hand-drawn pixel |
| Hard clean curves characteristic of vector | `vector-clean` | CraftPix vector packs |

**Important:** `hard-1px-outline` does NOT mean retro. CreativeKind and ppeldo hand-drawn-pixel packs use hard-1px outlines with expansive palette + dithered shading. They land in `hand-drawn-pixel` via rule R6.

**Side effect of R6:** the curation pipeline automatically tags the asset with `outline-profile:hard-1px` (for `hard-1px-outline`) or `outline-profile:soft-or-variable` (for `soft-outline` / `variable-width` / `no-outline`). Drax constrains scene-level filters to one outline-profile. This is automatic; curators don't separately tag outline-profile.

---

## 8. Axis 5 — `animation_frame_density`

**Question:** how many frames per typical animation cycle?

**How to determine:**
- Vendor listings often state frame count per animation. Use if listed.
- If sprite-sheet is provided: count rows in a single animation cycle (idle / walk / attack / etc.); use the highest-frame cycle as the representative density.
- If static (portrait, environment): tag `static`.

**Value cheat-sheet:**

| Frames per cycle | Tag as |
|---|---|
| 1 (no animation) | `static` |
| 2-4 | `low` |
| 5-8 | `mid` |
| 9-12 | `high` |
| 13+ | `cinematic` |

**Decision rule for VFX:** a spell-effect typically has one cycle. Use its frame count. pimen Fire Spell Effects packs are usually 8-12 frames = `mid` or `high`. unTied Games 60-FPS particle packs are `cinematic`.

---

## 9. License + cost

**Required fields:** `license` (NULL-forbidden), `cost_usd`, `cost_model`. `license_url` is required when `license = 'commercial-license'` or `'proprietary'`.

**How to determine `license`:**
- Read the asset's source page. Asset listings on itch.io / OpenGameArt.org / CraftPix / Unity Asset Store all carry an explicit license statement.
- Map to the exact enum value from `catalogue-schema.md` § 4.

**Common cases:**

| Source pattern | License typically |
|---|---|
| OpenGameArt asset marked "CC0" | `CC0` |
| OpenGameArt asset marked "CC-BY 3.0/4.0" | `CC-BY` |
| OpenGameArt asset marked "CC-BY-SA" | `CC-BY-SA` |
| itch.io asset with vendor license statement | Read the actual license — never use `itch-standard` (that value doesn't exist in v1.0). It might be CC0 / CC-BY / commercial-royalty-free / etc. depending on the creator. |
| CraftPix free pack | `commercial-royalty-free` (read terms to confirm) |
| CraftPix paid pack | `commercial-royalty-free` (typical CraftPix terms; verify) |
| Unity Asset Store | `unity-asset-store` |
| Vendor states "license per game title" | `commercial-per-project` |
| Vendor states royalty or revenue-share | `commercial-royalty-bearing` |
| Commercial terms unclear from initial read; needs deeper investigation | `commercial-license` (forces borderline review) |
| Vendor states "all rights reserved" or proprietary terms | `proprietary` |
| You couldn't determine from any source-page read | `unknown` (forces borderline review; do NOT use as a shortcut) |

**Cost:**
- `cost_usd` is the numeric one-time-equivalent. Free is `0.0`. CraftPix $5 pack is `5.0`. Per-asset pricing within a pack — record the asset's allocated share or use the pack price (curator judgment; record in `notes`).
- `cost_model` matches the license: `commercial-royalty-free` → typically `one-time`; `commercial-per-project` → `per-project`; etc.

**Critical rule:** NEVER tag `license = 'unknown'` to clear a backlog. Unknown is for genuinely-undetermined cases after a real read attempt. Per gandalf dialogue Topic 5: at viability-gate sample-time, **>20% unknown-license fails the design track** on data-hygiene grounds.

---

## 10. `decomposition` (the wiring-track signal)

Required for character/enemy assets; `not-applicable` for VFX/environment/UI/audio.

| Value | Look for |
|---|---|
| `monolithic` | Single sprite-sheet with everything baked together; body + head + weapon all on one frame |
| `decomposed` | Separable layers: body sheet, head sheet, weapon sheet shipped as distinct files or distinguishable atlas regions |
| `partial` | Some pieces separable (e.g., weapon overlays available) but not all (body + head still baked) |
| `not-applicable` | Non-character/enemy asset (vfx, tile, ui, audio) |
| `unknown` | Couldn't determine from source page; queue for manual review |

**Why decomposition matters:** drax's pixi.js consumption needs decomposed assets for embodiment-variance work (humanoid + various head/weapon combinations) and for the trial-boss cloak overlay per `enemy-visual-legibility.md`. Monolithic assets are usable but limit variation.

**Quick test:** does the vendor's pack page mention "separable parts" / "modular" / "customizable" / "layered"? Likely `decomposed` or `partial`. Single image with no mention of layers? Likely `monolithic`.

---

## 11. The deterministic rule for axis 6 (recap, with curator-side notes)

After tagging axes 1-5, the curation script applies the rule from `catalogue-rubric-schema.md` § 3 to produce `derived_register`. You do not manually pick axis 6.

**When the rule outputs `manual-review`:**
- Set the row aside in the manual-review queue.
- At the next manual-review pass, eyeball-inspect the asset and decide.
  - If the visual register is clear despite the rule's ambiguity: use `derived_register_source = 'manual-review-resolved'`, fill in the register, fill in `derived_register_override_rationale` with your read.
  - If the register is genuinely ambiguous (asset belongs to a register the rubric doesn't yet name): escalate to gandalf with `derived_register_source = 'gandalf-call'` and a brief description for senior-design review.

**When you disagree with the rule's output on a clearly-tagged asset:**
- Use `derived_register_source = 'override'`, fill in `derived_register_override_rationale` explaining the disagreement.
- This is for routine curator-vs-rule disagreements, NOT for register-genuinely-ambiguous cases. Use `override`, not `gandalf-call`. (Per gandalf dialogue Topic 3.)
- If your overrides accumulate to >10% of your tagged corpus OR cluster >5 on the same rule clause, the curation pipeline surfaces this to elrond as a rule-bug. Trust the threshold.

---

## 12. Worked examples — per-vendor tagging

Tagged worked examples for the major vendors from `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md`. Validation pass details in `catalogue-rubric-validation-2026-05-16.md`.

### 12.1 — Pipoya (Free RPG Character Pack 1-3)

| Axis | Value |
|---|---|
| `category` | `character` |
| `embodiment_tag` | `humanoid` |
| `resolution_band` | `retro` (32x32 canvas) |
| `palette_size` | `restricted` (~30-50 colors per pack) |
| `shading_technique` | `single-step` (one shadow tone per region) |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `low` (3-4 frames per cycle) |
| `derived_register` | `retro-16bit` (rule R3) |
| `decomposition` | `monolithic` (single sheet per character) |
| `license` | depends on Pipoya pack: free packs typically CC-BY / vendor terms |

### 12.2 — CreativeKind (hand-drawn pixel spell sets)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `hd2d-pixel` (64x64 typical) |
| `palette_size` | `expansive` (100+ colors) |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `hard-1px-outline` (THIS IS THE R6 CASE) |
| `animation_frame_density` | `high` (10-12 frames) |
| `derived_register` | `hand-drawn-pixel` (rule R6) |
| Side effect | `outline-profile:hard-1px` auto-tagged |
| `decomposition` | `not-applicable` |
| `license` | `commercial-royalty-free` (typical CreativeKind paid terms) |

### 12.3 — Foozle (Pixel Magic Effects, higher-tier)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `hd2d-pixel` (48x48-64x64) |
| `palette_size` | `restricted` (~50-60 colors — Foozle is restricted-leaning) |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` (6-8 frames) |
| `derived_register` | `hand-drawn-pixel` (rule R7 — boundary cluster) |
| Side effect | `quality_flag = 'borderline'` auto-set; curator confirms after eyeball |
| `decomposition` | `not-applicable` |
| `license` | `commercial-royalty-free` (typical Foozle terms) |

### 12.4 — pimen (Fire Spell Effects series)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `hd2d-pixel` (64x64-96x96) |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `variable-width` (often) or `no-outline` (some sprites) |
| `animation_frame_density` | `high` (10-12 frames) |
| `derived_register` | `hand-drawn-pixel` (rule R5) |
| `decomposition` | `not-applicable` |
| `license` | `commercial-royalty-free` (typical pimen terms; verify per pack) |

### 12.5 — CraftPix (vector pack — e.g., Free Water and Fire Magic Sprite Vector Pack)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `vector` |
| `palette_size` | `expansive` (or `truecolor` if vendor allows truecolor fills) |
| `shading_technique` | `vector-flat` |
| `linework_style` | `vector-clean` |
| `animation_frame_density` | depends; often `mid` |
| `derived_register` | `clean-vector` (rule R1) |
| `decomposition` | `not-applicable` |
| `license` | `commercial-royalty-free` (CraftPix typical) |

### 12.6 — CraftPix (pixel pack — e.g., Magic Effects Pixel Art Asset Pack 4)

Different pack from same vendor — different axis values.

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` to `high` |
| `derived_register` | `hand-drawn-pixel` (rule R6) |
| Side effect | `outline-profile:hard-1px` auto-tagged |
| `decomposition` | `not-applicable` |
| `license` | `commercial-royalty-free` |

**Note the same vendor (CraftPix) lands different axis-6 values on different packs.** This is the per-asset granularity (gandalf dialogue Topic 2). The `pack_register_consistency` field on each pack would be `consistent` here (each pack is internally consistent); CraftPix's broader catalogue is `mixed` at the vendor level.

### 12.7 — ansimuz (Free Magic Pack series, retro register)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `embodiment_tag` | `not-applicable` |
| `resolution_band` | `retro` (32x32) |
| `palette_size` | `restricted` |
| `shading_technique` | `single-step` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `low` (3-4 frames) |
| `derived_register` | `retro-16bit` (rule R3) |
| `decomposition` | `not-applicable` |
| `license` | typically free + vendor terms; read per asset |

### 12.8 — Elthen (Pixel Art Shop — character + spell sets)

| Axis | Value |
|---|---|
| `category` | depends; `character` for character packs, `vfx` for spell sets |
| `embodiment_tag` | `humanoid` (most Elthen character packs) |
| `resolution_band` | `hd2d-pixel` (48x48-64x64) |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` to `gradient-ramp` |
| `linework_style` | `hard-1px-outline` (typical Elthen style) |
| `animation_frame_density` | `mid` to `high` (6-10 frames) |
| `derived_register` | `hand-drawn-pixel` (rule R6) |
| Side effect | `outline-profile:hard-1px` auto-tagged |
| `decomposition` | varies per pack — typically `decomposed` (Elthen ships modular character packs) |
| `license` | `commercial-royalty-free` (typical paid Elthen terms) |

### 12.9 — LuizMelo (character + effect packs)

| Axis | Value |
|---|---|
| `category` | `character` or `enemy` per pack |
| `embodiment_tag` | varies — `humanoid` (Adventurer / Wizard / Knight), `beast` (Werewolf), `pending-amendment` (Skeleton; queue for undead-amendment) |
| `resolution_band` | `narrative-pixel` (LuizMelo is large-canvas; 80x80-100x100 typical) |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `high` (10-12 frames per cycle) |
| `derived_register` | `hand-drawn-pixel` (rule R6) |
| Side effect | `outline-profile:hard-1px` |
| `decomposition` | typically `monolithic` (single sheet per character) |
| `license` | varies per LuizMelo asset; read each |

### 12.10 — ppeldo, Frostwindz, unTied Games

Pattern follows; specifics in `catalogue-rubric-validation-2026-05-16.md`. ppeldo + Frostwindz are usually `hand-drawn-pixel` via R6; unTied Games 60-FPS particle packs are `hand-drawn-pixel` with `animation_frame_density = 'cinematic'`.

---

## 13. Failure modes — what to do when

### 13.1 — "I can't tell what `palette_size` is"

Open the sprite in any image-tool, use "image > image-properties" or color-count. If you genuinely can't, set `unknown` and queue. Don't guess.

### 13.2 — "Asset depicts multiple forms in one sheet (humanoid + beast)"

Tag the dominant form in `embodiment_tag`; note the secondary in `notes`. If genuinely a mixed-form pack (unusual), tag `unknown` and surface for manual review.

### 13.3 — "Vendor description doesn't match what I see"

Trust your eyes. Tag what the asset *looks like*. Note the discrepancy in `notes` so future passes don't repeat the inspection.

### 13.4 — "Asset is on a vendor page I can't access"

Skip; mark in Legolas raw output for re-extraction. Don't tag from secondhand description.

### 13.5 — "Two of my own assets in the same pack are tagging differently"

Possible. Per-asset granularity (gandalf dialogue Topic 2) is canonical. But: if a single Pipoya pack has both `retro` and `hd2d-pixel` resolution-band assets, that's *unusual* — verify your reads. If confirmed, that's a `mixed` `pack_register_consistency` signal worth noting.

### 13.6 — "License is genuinely ambiguous; I read the page and still don't know"

`unknown` license. Queue. Reach out to vendor where possible.

### 13.7 — "Asset depicts a form I've never seen in the starter set"

`embodiment_tag = 'pending-amendment'`; populate `pending_amendment_hint` with your read. Continue tagging the rest. Per gandalf dialogue Topic 4.

---

## 14. Cross-references

- `catalogue-rubric-schema.md` — the axes themselves
- `catalogue-schema.md` — the DB columns implementing them
- `catalogue-rubric-validation-2026-05-16.md` — validation pass on the empirical vendor landscape
- `curation-pipeline.md` — operational flow
- `canonical/story/style-register.md` — the locked register the rubric operationalizes
- `canonical/story/embodiment-narrative-layer.md` — embodiment taxonomy v1.0
- `canonical/story/enemy-visual-legibility.md` — sprite-archetype registry consuming catalogue queries
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical landscape

---

— elrond, 2026-05-16
