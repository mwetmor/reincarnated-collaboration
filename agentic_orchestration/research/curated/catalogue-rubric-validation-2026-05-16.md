# Catalogue Rubric Validation — Empirical Asset Landscape Pass

**Filed:** 2026-05-16
**Author:** elrond
**Rubric version:** v1.0 (locked 2026-05-16 post-gandalf-dialogue)
**Companion:** `catalogue-rubric-schema.md` (rubric definition); `curator-tagging-guide.md` (per-axis tagging guidance); `catalogue-schema.md` (DB schema)
**Status:** Validation pass complete. Rubric admits the empirical vendor landscape with the documented R6 + R7 exception rules. Five boundary/unstable cases surfaced; resolutions captured below. No further refinement required before locking v1.0.

---

## 0. What this validation does

Re-classifies every vendor / asset pattern named in `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` against the six-axis rubric. Verifies the deterministic rule (rubric § 3) produces a coherent answer for each. Surfaces unstable categorizations and resolves them in-rubric (additional exception rule) or out-of-rubric (curator override per-asset).

The dispatch (§ Deliverable 4) requires this pass before locking v1.0. The work documented here demonstrates the rubric clears the empirical landscape it must immediately serve.

---

## 1. Validation methodology

For each named vendor / pack pattern:

1. Tag all six axes from publicly-available vendor description + sample screenshots / preview images.
2. Apply rule (§ 3 of rubric-schema.md) to derive axis 6.
3. Compare derived register against gandalf's design-track intuition for the same asset (where it sits in the "retro / hand-drawn-pixel / vector / etc." vocabulary).
4. Where the rule and the intuition diverge, surface as a finding. Either: (a) refine the rule with an exception, or (b) record as a curator-override case for documentation.

The validation is **structural** (does the rubric produce consistent answers) not **aesthetic** (is the asset good for Reincarnated). Aesthetic / quality judgment is gandalf's track at viability-gate time.

---

## 2. Per-vendor validation

Each subsection: axis values, rule output, finding (`stable` / `boundary` / `unstable`), resolution.

### 2.1 — Pipoya (Free RPG Character Pack series)

| Axis | Value | Note |
|---|---|---|
| `category` | `character` | |
| `embodiment_tag` | `humanoid` | |
| `resolution_band` | `retro` | 32x32 canvas |
| `palette_size` | `restricted` | ~30-50 colors per pack |
| `shading_technique` | `single-step` | one shadow tone per region |
| `linework_style` | `hard-1px-outline` | |
| `animation_frame_density` | `low` | 3-4 frames per cycle |
| **Rule output (R3)** | `retro-16bit` | Matches gandalf intuition |
| Finding | **stable** | rubric admits cleanly |

### 2.2 — Pipoya (Time Magic / Warp Portal / HEX Shield / Light Pillar — VFX series)

| Axis | Value | Note |
|---|---|---|
| `category` | `vfx` | |
| `resolution_band` | `retro` | 32x32 typical |
| `palette_size` | `restricted` | |
| `shading_technique` | `single-step` to `dithered` (boundary) | Light Pillar has dithered shading; HEX Shield is mostly single-step |
| `linework_style` | `hard-1px-outline` | |
| `animation_frame_density` | `mid` | 6-8 frames |
| **Rule output** | varies — `retro-16bit` (R3 for single-step) OR `hand-drawn-pixel` (R7 for dithered) | |
| Finding | **boundary** | Per-asset tagging differentiates within the pack |
| Resolution | Curator tags each Pipoya VFX asset individually. Light Pillar lands `hand-drawn-pixel` with `quality_flag = 'borderline'` (R7 default); HEX Shield lands `retro-16bit`. Pack-level `pack_register_consistency = 'mixed'`. |

### 2.3 — ansimuz (Free Magic Pack 9, Magic Pack 4)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `retro` |
| `palette_size` | `restricted` |
| `shading_technique` | `single-step` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `low` to `mid` |
| **Rule output (R3 or R4)** | `retro-16bit` |
| Finding | **stable** |

### 2.4 — ansimuz (character + environment packs — Sunny Land etc.)

| Axis | Value |
|---|---|
| `category` | `environment` or `character` |
| `resolution_band` | `retro` to `hd2d-pixel` (boundary) |
| `palette_size` | `restricted` |
| `shading_technique` | `single-step` to `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `low` |
| **Rule output** | varies — most assets `retro-16bit`; some Sunny Land tile assets reach R7 territory |
| Finding | **stable with per-asset variance** | Per-asset tagging absorbs the variance |

### 2.5 — Foozle (Pixel Magic Effects)

| Axis | Value | Note |
|---|---|---|
| `category` | `vfx` | |
| `resolution_band` | `hd2d-pixel` | 48x48 / 64x64 |
| `palette_size` | `restricted` | ~50-60 colors — restricted-leaning |
| `shading_technique` | `dithered` | |
| `linework_style` | `hard-1px-outline` | |
| `animation_frame_density` | `mid` | 6-8 frames |
| **Rule output (R7)** | `hand-drawn-pixel` with `quality_flag = 'borderline'` | The R7 boundary cluster — gandalf dialogue specifically validated this |
| Finding | **boundary (R7)** | Resolved by R7 with curator-confirms-after-eyeball discipline |

### 2.6 — Foozle (2 Fire / 2 Earth / 2 Wind / 2 Water / Portal / Explosion — lower-tier packs)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `retro` |
| `palette_size` | `restricted` |
| `shading_technique` | `single-step` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `low` |
| **Rule output (R3)** | `retro-16bit` |
| Finding | **stable** | Lower-tier Foozle is straightforwardly retro |

### 2.7 — pimen (Fire / Water / Ice / Holy / Dark / Earth / Wind / Air spell effect series)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` | 64x64 to 96x96 |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `variable-width` (most) or `no-outline` (some) |
| `animation_frame_density` | `high` | 10-12 frames |
| **Rule output (R5)** | `hand-drawn-pixel` |
| Finding | **stable** | The reference case for R5 |

### 2.8 — CreativeKind (paid hand-drawn pixel spell sets — Water / Earth / Color / Magic)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` to `narrative-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `high` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable (R6 the validating case)** | The R6 motivating example — without R6, this would mis-route to `retro-16bit` via R3 |

### 2.9 — CreativeKind (Portrait packs — narrative-moment tier)

| Axis | Value |
|---|---|
| `category` | `portrait` |
| `resolution_band` | `narrative-pixel` to `cinematic-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` or `painterly` (some portraits) |
| `linework_style` | `hard-1px-outline` to `soft-outline` |
| `animation_frame_density` | `static` |
| **Rule output (R6 or R8)** | `hand-drawn-pixel` |
| Finding | **stable** | Narrative-moment-tier portraits land cleanly |

### 2.10 — unTied Games (Five Free Pixel Explosions, 60-FPS pixel particles)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `no-outline` |
| `animation_frame_density` | `cinematic` (60-FPS particle = many frames per cycle) |
| **Rule output (R5)** | `hand-drawn-pixel` |
| Finding | **stable** | Cinematic frame density doesn't change register |

### 2.11 — Elthen (Pixel Art Shop — character + spell sets)

| Axis | Value |
|---|---|
| `category` | `character` or `vfx` per pack |
| `embodiment_tag` | `humanoid` (typical character pack) |
| `resolution_band` | `hd2d-pixel` | 48x48 - 64x64 |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` to `gradient-ramp` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` to `high` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable** | Sibling cluster to CreativeKind |
| Note | Elthen character packs typically ship as `decomposed` (modular character parts) — valuable for embodiment-variance work |

### 2.12 — ppeldo (2D Pixel-art game spell/magic FX)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable** | Same R6 cluster as CreativeKind / Elthen |

### 2.13 — LuizMelo (character + effect packs)

| Axis | Value |
|---|---|
| `category` | `character` or `enemy` per pack |
| `embodiment_tag` | varies — `humanoid` (Adventurer, Wizard, Knight, Huntress), `beast` (Werewolf), **`pending-amendment` (Skeleton)** with hint `'undead-skeleton'` |
| `resolution_band` | `narrative-pixel` | 80x80 - 100x100 (LuizMelo is large-canvas) |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `high` | 10-12 frames |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable structurally; embodiment unblocks via `pending-amendment` for Skeleton pack** |
| Note | Skeleton pack is the canonical first `pending-amendment` case in v1.0 catalogue — drives evidence pressure for an `undead` amendment to `embodiment-narrative-layer.md` if more skeleton/undead assets accumulate |

### 2.14 — Frostwindz (Pixel Art VFX Lightning)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `no-outline` (lightning sprites tend to be linework-free) |
| `animation_frame_density` | `mid` |
| **Rule output (R5)** | `hand-drawn-pixel` |
| Finding | **stable** |

### 2.15 — Brackeys VFX Bundle

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` (mixed) |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` to `gradient-ramp` |
| `linework_style` | varies per asset |
| `animation_frame_density` | `mid` |
| **Rule output** | mostly R5 (`hand-drawn-pixel`); some R6 if hard-outlined |
| Finding | **stable per-asset; pack-level `pack_register_consistency = 'consistent'`** |

### 2.16 — CraftPix (Free Pixel Magic Sprite Effects Pack — pixel)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable** |

### 2.17 — CraftPix (Magic Effects Pixel Art Asset Pack 4 — composite/unusual effects)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `gradient-ramp` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` to `high` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable** |

### 2.18 — CraftPix (Magic Spells Pixel Art Sprite Pack)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `hd2d-pixel` |
| `palette_size` | `expansive` |
| `shading_technique` | `dithered` |
| `linework_style` | `hard-1px-outline` |
| `animation_frame_density` | `mid` |
| **Rule output (R6)** | `hand-drawn-pixel`, auto-tag `outline-profile:hard-1px` |
| Finding | **stable** |

### 2.19 — CraftPix (Free Water and Fire Magic Sprite Vector Pack — VECTOR)

| Axis | Value |
|---|---|
| `category` | `vfx` |
| `resolution_band` | `vector` |
| `palette_size` | `expansive` |
| `shading_technique` | `vector-flat` |
| `linework_style` | `vector-clean` |
| `animation_frame_density` | `mid` |
| **Rule output (R1)** | `clean-vector` |
| Finding | **stable** | Validates per-asset granularity within CraftPix: same vendor, different register per pack |

### 2.20 — CraftPix (Pixel Art Magic Sprite Effects and Icons Pack)

| Axis | Value |
|---|---|
| `category` | `vfx` + `icon` (mixed in same pack) |
| `resolution_band` | `hd2d-pixel` (vfx) and `tiny` to `retro` (icons) |
| `palette_size` | `expansive` (vfx); `restricted` (icons) |
| **Rule output** | per-asset; vfx assets land `hand-drawn-pixel`; icons may land `retro-16bit` |
| Finding | **stable per-asset; pack-level `pack_register_consistency = 'mixed'`** |
| Note | This is a multi-category pack — the schema's per-asset tagging absorbs this cleanly |

### 2.21 — CraftPix (Fire Magic Effects Pixel Art — 11 fire-specific effects)

Same pattern as CraftPix Magic Effects pixel packs (§ 2.17). Stable; R6.

### 2.22 — OpenGameArt.org (CC-licensed; variable register)

Per-asset tagging mandatory. OpenGameArt is the catalogue's canonical heterogeneous source:
- Some assets are `retro-16bit` (classic pixel pack contributions)
- Some are `hand-drawn-pixel` (higher-fidelity submissions)
- Some are `clean-vector` (vector contributions)
- Some are `painterly-raster` (rare; raster painterly submissions)

Finding: **stable per-asset; pack-level coherence is `mixed` for the overall OpenGameArt source**. Per-asset tagging is the only viable approach here.

---

## 3. Unstable cases surfaced — and their resolutions

Five cases where validation surfaced issues. All resolved within v1.0 rubric.

### 3.1 — Pipoya VFX series (§ 2.2)

**Issue:** Light Pillar shading is dithered; HEX Shield is single-step. Same vendor pack but different shading technique = different rule output.

**Resolution:** per-asset tagging absorbs the variance (gandalf dialogue Topic 2). Curator tags each asset individually. `pack_register_consistency = 'mixed'`. No rubric refinement needed.

### 3.2 — Foozle higher-tier vs lower-tier (§ 2.5 vs 2.6)

**Issue:** Foozle ships across registers. Pixel Magic Effects (higher-tier) is `hand-drawn-pixel` boundary; the 2x2 element packs are straightforward retro.

**Resolution:** per-asset granularity + R7 with default-borderline-flag handles cleanly. Per gandalf dialogue Topic 1.

### 3.3 — CraftPix cross-register (§ 2.19 vs 2.16-2.18 and 2.20)

**Issue:** Same vendor, vastly different registers (vector vs pixel).

**Resolution:** per-asset tagging is canonical (gandalf dialogue Topic 2). `pack_register_consistency` on each pack is `consistent`; vendor-level catalogue is `mixed`. The schema admits this cleanly.

### 3.4 — LuizMelo Skeleton pack (§ 2.13)

**Issue:** Skeleton depicts undead form, which is not in the v1.0 embodiment-narrative-layer taxonomy starter set.

**Resolution:** `embodiment_tag = 'pending-amendment'`, hint `'undead-skeleton'`. Per gandalf dialogue Topic 4. Asset still fully tagged on all other dimensions; only embodiment-specific filtering is blocked until amendment lands. When N skeleton/undead assets accumulate, the hint clustering pressures formal amendment.

**Note:** the catalogue's first `pending-amendment` asset cluster will likely be undead. This is consistent with gandalf's design intuition (per dialogue: "Pipoya's skeleton pack" was the example he named).

### 3.5 — OpenGameArt.org overall heterogeneity (§ 2.22)

**Issue:** No vendor-level register characterization possible.

**Resolution:** by design, per-asset tagging handles. Pack/vendor-level fields are advisory, not authoritative.

---

## 4. Coverage report — per-register, per-category

What the locked-Reincarnated-register consumption filter will return, post-curation of the named vendors:

### 4.1 — `derived_register = 'hand-drawn-pixel'` (the locked register)

| Vendor | Categories | Approximate asset count |
|---|---|---|
| pimen (full element series) | vfx | 8 element packs × ~20 assets each ≈ 160 |
| CreativeKind (spell sets) | vfx | ~40 across Water/Earth/Color/Magic |
| CreativeKind (portrait) | portrait | ~20 portraits |
| Elthen (character + spell sets) | character + vfx | ~50 across packs |
| ppeldo | vfx | ~30 |
| LuizMelo (character packs) | character + enemy | ~40 (excluding pending-amendment skeletons) |
| Frostwindz Lightning | vfx | ~10 |
| unTied Games | vfx | ~20 |
| Brackeys Bundle | vfx | ~30 |
| CraftPix (pixel packs) | vfx + icon | ~80 across named pixel packs |
| Foozle higher-tier (R7 borderline) | vfx | ~10 (post-eyeball-confirm subset) |
| OpenGameArt (filtered for hand-drawn-pixel contributions) | mixed | ~50-100 (curator effort-dependent) |
| **Total estimated** | | **~500-600 hand-drawn-pixel assets** in initial curation pass |

### 4.2 — `derived_register = 'retro-16bit'` (pivot-insurance pool)

| Vendor | Categories | Approximate asset count |
|---|---|---|
| Pipoya (Free RPG Character + tile + VFX) | character + tile + vfx | ~150-200 across free packs |
| ansimuz (Free Magic, Sunny Land) | vfx + environment + character | ~80 |
| Foozle lower-tier (2x element packs) | vfx | ~40 |
| OpenGameArt (filtered for retro-16bit) | mixed | ~50-100 |
| **Total estimated** | | **~300-400 retro-16bit assets** for pivot-insurance |

### 4.3 — `derived_register = 'clean-vector'`

| Vendor | Categories | Approximate asset count |
|---|---|---|
| CraftPix vector packs | vfx + tile + ui | ~30-50 |
| **Total estimated** | | **~30-50 vector assets** |

### 4.4 — Coverage by category × embodiment (for character/enemy only)

In the `hand-drawn-pixel` register, the per-embodiment coverage at validation time:

| Embodiment | Approximate coverage | Sourcing |
|---|---|---|
| `humanoid` | strong (~60+ assets) | LuizMelo / Elthen / CreativeKind |
| `slime` | thin (~5-10 assets) | various; gap to flag |
| `beast` | moderate (~15-20) | LuizMelo Werewolf; various |
| `dragonling` | moderate (~10-15) | CreativeKind Dragon |
| `swarm` | very thin (~3-5) | gap |
| `construct` | thin (~5-10) | Pipoya Golem ports; various |
| `spirit` | thin (~5-10) | various ghost / wraith packs |
| `plant` | very thin (~3-5) | gap |
| `pending-amendment` | TBD — accumulates as curation proceeds | LuizMelo Skeleton clusters undead |

**Gap signal:** swarm, plant, slime, dragonling, construct, spirit are all thin or near-empty at `hand-drawn-pixel`. The form-bias work per doc 37 § 4 (Position C non-humanoid embodiment work) will need either: (a) catalogue gap-filling (Legolas commission targeting these embodiments specifically), (b) LLM image generation for the underserved embodiments, or (c) deferred non-humanoid coverage until pipe expands. **This validation surfaces the gap as a known input to form-bias-work sequencing.**

---

## 5. Findings summary

1. **Rubric admits the empirical landscape cleanly.** All 22 vendor / pack patterns map to deterministic axis-6 outputs via rules R1-R8.
2. **R6 and R7 carry their weight.** Without R6, CreativeKind / Elthen / ppeldo / CraftPix pixel-packs mis-route to `retro-16bit`. Without R7, Foozle higher-tier routes to `manual-review` (curation traffic jam). Both rules earned their place in the dialogue.
3. **Per-asset granularity is essential.** Pipoya VFX, Foozle, CraftPix all ship cross-register or cross-shading within their catalogue. Per-vendor or per-pack-level tagging would mis-classify. The schema's per-asset model handles cleanly.
4. **`pending-amendment` embodiment slot proves immediately useful.** LuizMelo Skeleton pack is the first canonical `pending-amendment` case (undead). The amendment-gated pattern (gandalf dialogue Topic 4) prevents catalogue-data from defining narrative canonicity prematurely.
5. **Embodiment coverage gaps in `hand-drawn-pixel` are real.** Slime, swarm, plant, dragonling, construct, spirit are all thin. Form-bias work per doc 37 § 4 needs to plan around this — either catalogue gap-fill, LLM-image generation, or sequenced non-humanoid focus.
6. **License coverage clear-but-mixed.** Most named vendors are `commercial-royalty-free` or vendor-specific commercial. OpenGameArt is CC0/CC-BY heavy. Free + permissive coverage in `hand-drawn-pixel` is strong; commercial-only coverage in retro is also strong. License-filter at consumption time will not strongly constrain the locked-register asset pool.

---

## 6. No rubric refinement needed pre-lock

The validation pass surfaces no cases the rubric's v1.0 design fails to handle. Lock v1.0 as specified in `catalogue-rubric-schema.md`.

**Future refinement triggers (recorded for forward awareness):**
- If Legolas crawls expose vendors / clusters that consistently route to `manual-review` (>10% of a sample) — refine rule to add an exception R-clause.
- If curator-override rates exceed 10% of corpus on a single rule clause — same trigger.
- If `pending-amendment` hints cluster on a recurring form (e.g., 20+ undead-skeleton hints accumulate) — pressure narrative-layer amendment.
- If `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` proves insufficient for scene-coherence at drax's consumption pass — refine tagging to capture additional outline gradations.

---

## 7. Cross-references

- `catalogue-rubric-schema.md` — the rubric this validates
- `curator-tagging-guide.md` — per-axis tagging instructions used in this validation
- `catalogue-schema.md` — DB schema accepting the validated taxonomy
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical landscape source
- `canonical/story/style-register.md` — locked register
- `canonical/story/embodiment-narrative-layer.md` — embodiment taxonomy + amendment protocol
- `canonical/story/enemy-visual-legibility.md` — downstream consumer

---

— elrond, 2026-05-16
