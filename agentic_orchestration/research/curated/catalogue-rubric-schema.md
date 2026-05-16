# Catalogue Rubric — Six-Axis Visual Style Register Schema

**Status:** **Locked v1.0** as of 2026-05-16, post-dialogue with gandalf (Pattern-A subagent, per Matt's direct-dialogue directive). See § 9 for the dialogue record.
**Author:** elrond, in dialogue with gandalf.
**Companion:** `catalogue-schema.md` (the broader DB schema); `curator-tagging-guide.md` (per-axis tagging instructions); `MIGRATION.md` (v1.0 schema migration record).
**Implements:** `canonical/story/style-register.md` § "Operational precision — deferred to Elrond's rubric design." Operationalizes the locked HD-2D-pixel hand-drawn register into curator-checkable axes.

---

## 0. What this doc is, in one sentence

Six axes, five mechanically-checkable + one derivable, that two different curators looking at the same asset arrive at the same value-set for — converting the locked-but-vague style-register decision into a tag schema the catalogue can ship against.

---

## 1. Design principles

**Score-don't-filter (AGENTS.md § "Score-don't-filter principle").** Every asset gets *all six axis values*. The locked HD-2D-pixel register becomes a **multi-axis query** at consumption time, not a filter at crawl time. Other-register assets stay in the catalogue with their own axis tags. A register pivot is a *re-filter* operation, not a re-crawl.

**Two-curator convergence.** Each axis has a closed value set. For each value, the curator-tagging guide describes a deterministic test the curator applies. If two different curators tag the same asset and disagree on more than one axis, that's a rubric bug, not a tagging bug — surface it for refinement.

**Source-anchored.** The rubric assigns values per-asset, not per-vendor and not per-pack. A vendor that ships across registers (CraftPix has both pixel AND vector packs; CreativeKind has both retro-leaning AND hand-drawn-leaning sets) gets per-asset axis values that reflect each individual asset's properties.

**Reversible.** The full Legolas raw extraction (`asset_metadata_raw` JSON) is preserved alongside the curated axis values. If the rubric is refined, the catalogue can be re-tagged from the raw evidence without re-crawl.

**Tagged, not encoded.** Axis values live in named columns. The derived stylistic register (axis 6) is **stored as its own column**, not encoded by joining the other five — this allows curator overrides (manual judgment when the deterministic rule mis-classifies a known case) without losing the underlying axis-1-5 truth.

---

## 2. The six axes — schema-side definitions

Each axis is implemented as a column on `catalogue_assets` with a constrained enum value set.

### Axis 1 — `resolution_band` (sprite resolution range)

Enum (TEXT) with these allowed values:

| Value | Range (pixels per asset character body / single-sprite frame) | Examples |
|---|---|---|
| `tiny` | ≤ 16 px | 8-bit micro-sprites; some Pipoya tile-mode assets |
| `retro` | 17 – 32 px | Classic 16-bit register; ansimuz, most Pipoya free packs, lower-tier Foozle |
| `hd2d-pixel` | 33 – 64 px | Hand-drawn pixel register: CreativeKind, Elthen, mid-tier pimen, higher-tier Foozle |
| `narrative-pixel` | 65 – 128 px | Larger hand-drawn pixel: CreativeKind portrait packs, ppeldo character sets, LuizMelo character + effect |
| `cinematic-pixel` | 129 – 256 px | Narrative-moment-tier: large-canvas hand-drawn pixel; some CraftPix high-tier packs |
| `raster` | ≥ 257 px or pixel-grid-free | Painterly raster; HD raster textures; non-pixel art |
| `vector` | resolution-independent vector format (SVG, scalable) | CraftPix vector packs; vector indie packs |
| `unknown` | not determinable from source metadata | Last resort; flagged for manual review |

**Why a band, not a numeric range:** Vendors ship inconsistent canvas sizes per pack. A "32x32" pack may contain individual sprites at 28x32, 32x32, and 32x40. The band absorbs that variance. Curators record the **typical character-body size** for the asset; outliers within a pack take the same band.

**Special-case rule for VFX assets:** for spell/effect assets (no humanoid body), use the effect-frame canvas size as the resolution proxy. A 64x64 spell-effect frame is `hd2d-pixel`-band; a 128x128 is `narrative-pixel`-band.

### Axis 2 — `palette_size` (color palette breadth)

Enum (TEXT):

| Value | Distinct-color count | Examples |
|---|---|---|
| `16-color` | ≤ 16 distinct colors | Classic NES/SMS register; rare in modern indie packs |
| `restricted` | 17 – 64 | Retro pixel-art: Pipoya, ansimuz, classic-leaning Foozle |
| `expansive` | 65 – 256 | Hand-drawn pixel-art with dithering: CreativeKind, Elthen, pimen, CraftPix Magic-pack tier |
| `truecolor` | ≥ 257 (effectively photo-class) | Raster painterly, HD raster, untreated vector |
| `unknown` | not determinable | Manual-review flag |

**Curator-checkable test:** Open the sprite/sample in an image tool. Count unique colors. Most asset listings include this. If not, eyeball: ≤16 colors looks "retro-blocky;" 17-64 looks "classic-pixel;" 65-256 supports gradient ramps and dithering; ≥257 is photo-class.

### Axis 3 — `shading_technique`

Enum (TEXT):

| Value | What it looks like | Examples |
|---|---|---|
| `flat-fill` | One color per region; no shading at all | Some Pipoya minimal-mode; UI-pixel work |
| `single-step` | Base + one darker step; banded shadows | ansimuz, classic Pipoya, lower-tier Foozle |
| `dithered` | Pixel-noise patterns approximate gradients | Classic hand-drawn pixel: CreativeKind, Elthen, higher Foozle |
| `gradient-ramp` | Smooth multi-step color ramps; pixel-coherent | pimen, CreativeKind, higher-tier CraftPix pixel packs |
| `painterly` | Brush-stroke-coded shading; not pixel-grid-coherent | Raster painterly; some hand-drawn vector |
| `vector-flat` | Vector regions, flat or gradient-vector fills | CraftPix vector packs |
| `unknown` | not determinable | Manual-review flag |

**Curator-checkable test:** Inspect the sprite at 4x zoom. How does it handle a curved or shaded surface? Flat color = `flat-fill`; one banded step = `single-step`; pixel-noise approximating shadow = `dithered`; smooth ramped pixels = `gradient-ramp`; brush-stroke evidence = `painterly`; SVG/clean curves = `vector-flat`.

### Axis 4 — `linework_style`

Enum (TEXT):

| Value | What it looks like | Examples |
|---|---|---|
| `hard-1px-outline` | Uniform 1-pixel black or dark outline around every shape | Pipoya, ansimuz, classic Foozle, classic retro register |
| `soft-outline` | Outline present but anti-aliased or color-modulated | Some CreativeKind, higher-tier hand-drawn pixel |
| `variable-width` | Outlines vary in thickness to convey depth/illustration sensibility | CreativeKind hand-drawn packs; some pimen narrative work |
| `no-outline` | Sprite is shaded without explicit border | Some hand-drawn pixel; most painterly raster |
| `vector-clean` | Hard clean lines characteristic of vector packs | CraftPix vector packs |
| `unknown` | not determinable | Manual-review flag |

**Curator-checkable test:** Zoom in on any sprite edge. Is there a 1-pixel uniform dark border? `hard-1px-outline`. Anti-aliased or color-shifted border? `soft-outline`. Outline width varies along the sprite? `variable-width`. No discernible outline; shaded directly? `no-outline`. Vector-clean curves? `vector-clean`.

### Axis 5 — `animation_frame_density`

Enum (TEXT):

| Value | Frames per typical cycle | Examples |
|---|---|---|
| `static` | Single frame; no animation | Portrait assets, some Court-tier pieces |
| `low` | 2 – 4 frames per cycle | Classic Pipoya, minimal-pixel VFX |
| `mid` | 5 – 8 frames per cycle | Hand-drawn pixel game-pace: most CreativeKind, lower pimen, mid Foozle |
| `high` | 9 – 12 frames per cycle | pimen animation-rich packs, CreativeKind higher-tier |
| `cinematic` | ≥ 13 frames per cycle | unTied Games 60-FPS particle packs, painterly cinematic |
| `unknown` | not determinable | Manual-review flag |

**Curator-checkable test:** Check vendor listing for per-cycle frame count. If listed, use it. If not listed but sprite-sheet is provided, count rows in a single animation cycle. If sprite is static (portrait, environment), `static`.

### Axis 6 — `derived_register` (the qualitative aesthetic tag)

Enum (TEXT):

| Value | Description |
|---|---|
| `retro-16bit` | Classic 16-bit register; restricted palette + flat/single-step shading + hard outline + low animation |
| `hand-drawn-pixel` | The locked Reincarnated register. Expansive palette + dithered/gradient-ramp shading + variable-width or no outline + mid-to-high animation |
| `clean-vector` | Vector register; vector-flat shading + vector-clean linework + scale-invariant resolution |
| `painterly-raster` | Raster painterly; truecolor + painterly shading + no/soft outline + cinematic-or-static |
| `anime-cel` | Cel-shading register (rare in asset libraries; mostly commissioned/LLM territory) |
| `manual-review` | Axes 1-5 don't combine into any of the above clean clusters; curator-or-design-lead judgment required |

**Derivation rule:** see § 3 below. Stored as its own column; curator overrides allowed (with `derived_register_source` flag — `'rule'` or `'override'` — preserving the audit trail).

---

## 3. Deterministic classification rule for axis 6

Given values on axes 1-5, the rule produces an axis-6 value. The rule is a decision table, evaluated in priority order (first match wins). `*` means "any value." `manual-review` is the fallback.

| Rule | Axis 1 resolution | Axis 2 palette | Axis 3 shading | Axis 4 linework | Axis 5 animation | → Axis 6 derived |
|---|---|---|---|---|---|---|
| R1 | `vector` | `truecolor` OR `expansive` | `vector-flat` | `vector-clean` | `*` | `clean-vector` |
| R2 | `raster` | `truecolor` | `painterly` | `no-outline` OR `soft-outline` | `*` | `painterly-raster` |
| R3 | `tiny` OR `retro` | `16-color` OR `restricted` | `flat-fill` OR `single-step` | `hard-1px-outline` | `static` OR `low` | `retro-16bit` |
| R4 | `tiny` OR `retro` | `16-color` OR `restricted` | `flat-fill` OR `single-step` | `hard-1px-outline` | `mid` | `retro-16bit` (motion doesn't change register) |
| R5 | `hd2d-pixel` OR `narrative-pixel` OR `cinematic-pixel` | `expansive` | `dithered` OR `gradient-ramp` | `variable-width` OR `no-outline` OR `soft-outline` | `mid` OR `high` OR `static` | **`hand-drawn-pixel`** ← the Reincarnated lock |
| R6 | `hd2d-pixel` OR `narrative-pixel` OR `cinematic-pixel` | `expansive` | `dithered` OR `gradient-ramp` | `hard-1px-outline` | `*` | `hand-drawn-pixel` **with mandatory `outline-profile:hard-1px` secondary tag** — see § 3.1 below. Per gandalf dialogue: hard-outline + expansive palette + dithered/ramp reads as hand-drawn-pixel and clears the consumption filter, but does NOT composite cleanly in the same scene as soft/variable-outlined hand-drawn-pixel assets (Octopath HD-2D precedent). Drax constrains scene-level filters by outline-profile. CreativeKind / ppeldo land here. |
| R7 | `hd2d-pixel` OR `narrative-pixel` | `restricted` | `dithered` | `hard-1px-outline` OR `soft-outline` | `mid` | `hand-drawn-pixel` **with default `quality_flag = 'borderline'`** until curator-confirmed — see § 3.1 below. Per gandalf dialogue: Foozle higher-tier sits genuinely between retro and hand-drawn-pixel; the rule admits the asset but flags it for explicit eyeball pass to prevent silent absorption of clashing assets. |
| R8 | `cinematic-pixel` | `expansive` OR `truecolor` | `gradient-ramp` OR `painterly` | `no-outline` | `static` | `hand-drawn-pixel` (narrative-moment-tier portraits; locked register's portrait fidelity) |
| R-default | anything else | | | | | `manual-review` |

**Why R6 exists separately:** without R6, R3 captures CreativeKind/ppeldo hard-outlined hand-drawn-pixel assets and mis-classifies them as `retro-16bit`. The dialogue with gandalf surfaced this — hand-drawn-pixel CAN have hard 1-px outlines; the differentiator from retro is palette breadth and shading technique, not linework alone.

**Why R7 exists:** Foozle's higher-tier packs (Pixel Magic Effects) sit between retro and hand-drawn-pixel. They have restricted-to-mid palette but use real dithering. The rubric admits them to `hand-drawn-pixel` rather than `manual-review` to avoid a curation traffic-jam on a known boundary cluster. Documented explicitly so future refinement can revisit.

### 3.1 — Side effects of R6 and R7 (per gandalf dialogue, 2026-05-16)

R6 and R7 admit assets to `hand-drawn-pixel` that need additional metadata to be consumed cleanly. Two side effects of the rule:

**R6 side effect — mandatory `outline-profile` secondary tag.**

When R6 produces `hand-drawn-pixel` with `linework_style = 'hard-1px-outline'`, the curation pipeline **must** add a secondary tag `outline-profile:hard-1px` to `asset_style_tags` for that asset. Conversely, when the asset's linework is `soft-outline / variable-width / no-outline`, the pipeline adds `outline-profile:soft-or-variable`.

This protects scene-level coherence at consumption time: **two assets in the same scene must share an outline-profile tag.** Drax's default consumption query for a scene constrains to one outline-profile. The Octopath / Trials of Mana / HD-2D shipped precedents do not mix outline profiles in the same frame; the rubric preserves that capability without rejecting hard-outlined assets from the catalogue.

The tag is **not part of the deterministic rule for axis 6** — it's a curation-pipeline side effect. The pipeline applies it automatically based on `linework_style`. Curators do not separately reason about outline-profile.

**R7 side effect — default `quality_flag = 'borderline'`.**

When R7 produces `hand-drawn-pixel` (Foozle higher-tier boundary cluster), the curation pipeline **must** set `quality_flag = 'borderline'` on insert, forcing an explicit eyeball pass before the asset is treated as ship-ready. Curator either confirms (`quality_flag = 'pass'` with rationale) or rejects (`quality_flag = 'fail'` with rationale).

This protects against R7 becoming a silent pass-through that absorbs assets which read as clashing when composited. R7 is a documented exception with intentional friction.

**Curator override.** If a curator looks at the rule output and disagrees on a specific asset (e.g., a CreativeKind pack that scores `hand-drawn-pixel` by rule but visually reads as `retro-16bit` due to non-canonical color choices), they can override. The DB records the override with `derived_register_source = 'override'` and a free-text `derived_register_override_rationale`. Overrides are audit-trail-preserved; the rule's output is still derivable from axes 1-5 if needed.

**Curator-override review threshold (per gandalf dialogue).** Curator overrides are sufficient with audit-trail; gandalf-approval is **not** required for routine cases. But: if a single curator's overrides exceed **10% of their tagged corpus**, OR if overrides on the same rule clause cluster above **5 instances**, the override pattern is surfaced as a rule-bug to elrond. The rule isn't carrying its weight at that point and needs refinement.

**Manual-review escalation.** When the rule produces `manual-review`, the asset goes to a `manual-review-queue` (a curator workflow). Two outcomes: (a) curator looks at axes 1-5 and assigns a register value with override (recorded as `derived_register_source = 'manual-review-resolved'`); (b) curator escalates to gandalf for senior-design call (recorded as `derived_register_source = 'gandalf-call'`).

**Important distinction (per gandalf dialogue):** `gandalf-call` is reserved for **register-genuinely-ambiguous cases** — the asset belongs to a register the rubric doesn't yet name, requiring senior-design judgment. It is **not** an escape hatch for routine curator-vs-rule disagreements; those are handled by `override` with audit-trail. The curator-tagging guide documents this distinction so curators don't reach for `gandalf-call` when `override` is the right tool.

---

## 4. Cross-axis structural constraints (the negative-space rules)

These are pre-tagging validity checks. If a curator records a combination that violates them, the rubric prompts re-inspection rather than accepting the tag set.

- **C1 — `vector` resolution requires `vector-flat` shading.** Vector assets do not have dithering or painterly shading. If a curator records `resolution_band = vector` with `shading_technique = dithered`, that's a category error; re-inspect.
- **C2 — `16-color` palette is incompatible with `gradient-ramp` shading.** Gradient ramps require ≥17 colors to register as ramps.
- **C3 — `painterly` shading is incompatible with `hard-1px-outline`.** Painterly assets don't use uniform 1-pixel outlines.
- **C4 — `tiny` resolution is incompatible with `high` or `cinematic` animation.** Sub-16px sprites do not sustain 9+ frames meaningfully.
- **C5 — `static` animation is compatible with all other axes.** Portraits and environment-pieces span every register.

These are encoded as `CHECK` constraints in the DB schema where unambiguous (C1 specifically); softer constraints (C2-C4) are documented warnings the curator script surfaces but does not block.

---

## 5. What the rubric does NOT cover (and where it intentionally stops)

**Content axis.** What the asset *depicts* (humanoid sprite, slime, swarm, vfx-spell, environment-tile, UI-icon) is a separate dimension from style register. It lives on `catalogue_assets.category` (Legolas Mode B field) and, for character/enemy assets specifically, on `catalogue_assets.embodiment_tag` (per gandalf's commission item 4 + dialogue topic 4). The style rubric applies uniformly to a humanoid sprite and a slime sprite — both can be retro, both can be hand-drawn-pixel. **Style is style; content is content; they're orthogonal.**

**Quality / aesthetic-merit.** "Is this a good asset?" is not in the rubric. The catalogue scores style register; senior-design (gandalf) viability-gates whether the asset's quality clears the bar for inclusion in the Reincarnated register's consumption-time filter.

**Animation framerate.** Axis 5 captures *frame density per cycle*, not playback FPS. A 60-FPS pack with 12 frames per cycle is `high`; a 8-FPS pack with 12 frames per cycle is also `high`. Playback FPS is a Pixi.js-side rendering concern handled by drax, not a catalogue-rubric concern.

**Per-season palette modulation.** Per `enemy-visual-legibility.md` Q2 + `style-register.md` § "Per-embodiment register awareness," seasons modulate element palettes (Yomi shifts wind toward heavier compressed signature). This is a runtime tint operation, not a per-asset rubric concern. The catalogue's `palette_size` axis captures the asset's *intrinsic* palette breadth; seasonal modulation is downstream.

**License / cost.** Distinct from style. Lives on `catalogue_assets.license` + `cost_usd` + `cost_model` columns (see `catalogue-schema.md` § 3.5).

---

## 6. Versioning policy

This rubric is **v1.0** as of 2026-05-16 lock. Future refinements come in two forms:

- **v1.x — additive refinement.** New value added to an axis enum; new constraint added; the deterministic rule gains a new clause. Forward-compatible: previously-tagged assets remain valid; no re-tagging required. Recorded in `MIGRATION.md`.
- **v2.0 — breaking refinement.** Existing enum values change meaning; an axis is added or removed; the deterministic rule changes outcome on existing assets. Requires re-tagging pass. Senior-design decision (Matt + gandalf + elrond) per ADR-002. Recorded in `MIGRATION.md` with re-tagging script in `research/scripts/`.

The rubric version is stored alongside each `catalogue_assets` row as `rubric_version` (default `'1.0'`). This makes mixed-rubric-version rows discoverable when v2.0 lands.

---

## 7. What this rubric locks operationally

**For Legolas (Mode B crawl).** Legolas's per-asset extraction populates the source-anchored fields (asset_id, source, url, name, category, dimensionality, file_format, license, cost, crawl_date) AND attempts the five mechanical axis values (resolution_band, palette_size, shading_technique, linework_style, animation_frame_density) from vendor metadata where possible. Where axes can't be determined from metadata alone, Legolas sets `unknown` and the curator (Elrond) fills in during curation pass.

**For Elrond (curation).** Each asset row passes through curator-axis-tagging: any `unknown` values get filled in by visual inspection; the deterministic rule (§ 3) produces `derived_register`; curator overrides recorded with rationale. Quality-flag / license-clarity / decomposition-signal checks happen in the same curation pass (per dispatch § Curator-tagging guidance + curation pipeline doc).

**For Gandalf (design-track viability gate).** Sample-time review consumes the curated axis values directly. Sample passes design track if: (a) sufficient assets in `hand-drawn-pixel` derived register to clear the locked-register consumption filter; (b) the axis distribution is consistent with pivot-insurance (other registers represented for re-filter capability); (c) sample-classification by rule matches gandalf's visual read on a sub-sample.

**For Drax (consumption filter).** Drax queries the catalogue with `derived_register = 'hand-drawn-pixel'` as the default filter for Reincarnated demo / loadout asset selection. Compound queries (e.g., `derived_register = 'hand-drawn-pixel' AND category = 'enemy' AND embodiment_tag = 'slime'`) are the normal pattern. Filter behavior under a register pivot is a re-query, not a re-build.

**For Star-lord (LLM visual prompts).** Style-register prompt language is consumed from `style-register.md` § "Maintenance protocol → When LLM image generation work needs the register." The catalogue's axis tags are not directly consumed by LLM prompts; they're consumed by drax to source style-reference images that *anchor* the LLM prompt.

---

## 8. Failure modes the rubric protects against

1. **Curator-tagging variance.** Two curators looking at Pipoya pack X tagging it as `retro-16bit` vs `hand-drawn-pixel`. Axes 1-5 are checkable (resolution count, palette count, shading inspection); they converge. Axis 6 is deterministic from the rule.
2. **Vendor-level tagging.** Tagging CraftPix as "vector" when the vendor also ships pixel packs. The rubric tags **per-asset**, not per-vendor. CraftPix-vector-pack-A and CraftPix-pixel-pack-B get different axis values.
3. **Style-coherence drift.** Selecting a `retro-16bit` asset for a `hand-drawn-pixel` scene because the asset's vendor listing didn't make the distinction visible. The locked-register filter (`derived_register = 'hand-drawn-pixel'`) excludes retro at the SQL level.
4. **Register-pivot lock-in.** Throwing away the catalogue's other-register coverage during the Reincarnated lock. The score-don't-filter principle is enforced in the schema: all six axes are tagged for every asset; the filter is consumption-time.
5. **Hidden boundary clusters.** Foozle's higher-tier packs are between retro and hand-drawn-pixel. R7 captures this case explicitly so each Foozle asset gets the same value rather than rotating between curator judgments.

---

## 9. Dialogue summary — gandalf, 2026-05-16

Per Matt's 2026-05-16 directive (Option B direct gandalf-elrond dialogue), this rubric was developed via Pattern-A subagent dialogue. Elrond presented draft proposals on the five topics from gandalf's commission + the schema sketch; gandalf returned terse-where-accepted, specific-where-refined responses; outcomes folded back into this doc + the companion schema doc.

**Topic 1 — Axis 6 determinism. REFINED.**
- Operationally deterministic for the known landscape is acceptable.
- **R6:** keep producing `hand-drawn-pixel`; do **not** fork the enum. But the rule is doing too much work without a sub-tag — CreativeKind hard-outlined hand-drawn-pixel does **not** composite cleanly with Octopath-style soft/variable-outlined hand-drawn-pixel in the same frame. Genre precedent: Octopath Traveler, Trials of Mana remake, Diablo III's character-painting backlash.
- **Resolution:** R6 admits the asset to `hand-drawn-pixel` AND adds a mandatory `outline-profile:hard-1px` vs `outline-profile:soft-or-variable` secondary tag on `asset_style_tags`. Scene-level consumption filters constrain to one outline-profile. See § 3.1.
- **R7:** Foozle higher-tier admission is the right call but risks silent absorption. Mitigation: default `quality_flag = 'borderline'` on R7-derived assets, forcing explicit eyeball pass. See § 3.1.

**Topic 2 — Per-asset granularity. ACCEPTED, with one addition.**
- Per-asset (not per-pack, not per-vendor) tagging is canonical.
- Addition: `catalogue_packs.pack_register_consistency` advisory column (`consistent | mixed | unknown`) populated post-curation. Drives curator suspicion on future packs from the same vendor and informs gandalf's viability-gate read.

**Topic 3 — Three-step ladder for between-categories assets. REFINED.**
- Ladder shape is right.
- Curator-override is sufficient with audit-trail; no gandalf-approval needed for routine cases.
- Threshold: if a curator's overrides exceed **10% of their tagged corpus** OR cluster on a single rule clause **>5 instances**, surface as rule-bug to elrond (the rule isn't carrying its weight).
- `gandalf-call` enum value reserved for **register-genuinely-ambiguous** cases (asset belongs to a register the rubric doesn't yet name), not for routine curator-vs-rule disagreements (those use `override`). Documented in § 3.1.

**Topic 4 — Embodiment expansion-protocol slots. PARTIALLY REJECTED.**
- Including all expansion-protocol slots (mecha/undead/demon/vampire/merfolk/deity/other-form) in the v1.0 enum breaks the narrative-layer amendment protocol locked in `embodiment-narrative-layer.md`. Catalogue convenience would pre-empt narrative-layer canonicity.
- **Resolution:** v1.0 enum = the eight starter embodiments + `not-applicable` + `unknown` + a single holding value `pending-amendment`. New `pending_amendment_hint` TEXT column captures curator's read ("looks like undead", "mecha-form"). Asset still tagged on all other dimensions (style axes, license, decomposition); only blocks embodiment-specific filtering until amendment lands.
- When N assets accumulate with the same hint, that pressures formal amendment. Amendment promotes the value to a real enum entry in a v1.x rubric migration; curator backfills.
- Cross-reference required in `embodiment-narrative-layer.md` so the narrative-layer doc and the catalogue agree on amendment-gated promotion. (NOTE: that doc is gandalf's; elrond surfaces this back to knight-rider for gandalf to amend.)

**Topic 5 — License enum. REFINED.**
- Split `commercial-license` into four narrower values:
  - `commercial-royalty-free` (CraftPix-style; pay once, ship any number of projects; the indie-pack default)
  - `commercial-per-project` (license is per-game-title)
  - `commercial-royalty-bearing` (per-copy or revenue-share; rare in asset libraries; may surface in music/SFX catalogue later)
  - `commercial-license` (commercial terms apply, specifics-not-yet-parsed; narrower escape valve than `unknown`; default `quality_flag = 'borderline'`)
- **Drop `itch-standard`** — meaningless category; itch creators ship every variety. Forcing curators to record the real license prevents shortcut-tagging.
- `unknown` license treatment strengthened: at viability-gate sample-time, if >20% of a sample carries `license = 'unknown'`, the sample fails the design track on data-hygiene grounds (catalogue's job is to know what we can use).

**Topic 6 (gandalf-added) — Pivot-insurance ledger.**
- Score-don't-filter is only honored if pivot-insurance is **actively monitored as the catalogue grows**, not just queryable on demand.
- Curation pipeline emits a small summary appended to `agentic_orchestration/research/curated/pivot-insurance-ledger.md` at every curation pass. Records: per-`derived_register` asset counts; per-embodiment coverage in `hand-drawn-pixel` AND next-most-populated register; embodiments where pivot-insurance is near-zero.
- Coverage erosion (e.g., 200 hand-drawn-pixel slimes but 3 retro-16bit slimes) is the signal that a register pivot cannot preserve that embodiment without a fresh crawl. The ledger watches the asymmetric-stewardship analogue of Discipline #13 implicit-pillar drift at the catalogue layer.

---

### Files touched by this dialogue lock

- `catalogue-rubric-schema.md` (this doc) — § 3 rule-table revisions on R6/R7; new § 3.1; § 9 dialogue record
- `catalogue-schema.md` — § 3.4 embodiment_tag enum revision + `pending_amendment_hint` column; § 3.5 license enum revision; § 3.6 `pack_register_consistency` advisory; § 4 license taxonomy revision
- `pivot-insurance-ledger.md` — new file; curation-pipeline output target
- `embodiment-narrative-layer.md` — cross-reference of `pending-amendment` holding pattern (owned by gandalf; elrond surfaces request via knight-rider, not direct edit)

---

## 10. Cross-references

- `catalogue-schema.md` — the DB schema implementing these axes as columns
- `curator-tagging-guide.md` — per-axis curator-tagging instructions with worked examples
- `catalogue-rubric-validation-2026-05-16.md` — validation pass against the empirical asset landscape
- `MIGRATION.md` — v1.0 schema migration entry
- `canonical/story/style-register.md` — the locked register this rubric operationalizes
- `canonical/story/embodiment-narrative-layer.md` — the embodiment-tag value set (separate dimension from style)
- `canonical/story/enemy-visual-legibility.md` — the monster-sprite registry requirements informing per-archetype tagging
- `agentic_orchestration/research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` — empirical landscape the rubric was validated against
- `AGENTS.md` § "Viability-gate workflow (catalogue work)" + § "Score-don't-filter principle"

---

## 11. Maintenance protocol

When new asset sources are crawled and surface cases the rubric doesn't cover cleanly:
1. Curator flags the case in `manual-review` queue with rationale.
2. Elrond reviews the queue at curation passes. Patterns of similar cases → propose axis refinement (additive v1.x or breaking v2.0).
3. For v1.x: add value or rule clause; update MIGRATION.md; backfill is optional (existing rows remain valid).
4. For v2.0: senior-design review (Matt + gandalf + elrond); breaking change with re-tagging script.

When the locked style register pivots:
- Rubric is **unchanged.** Other-register assets are already tagged. Consumption-time filter changes from `derived_register = 'hand-drawn-pixel'` to whatever the new lock specifies. No re-tagging.

When a curator override pattern emerges (many overrides on the same rule clause):
- Surface as a rule-bug, not a curation-bug. Refine the rule clause in next rubric version.

---

— elrond, post-dialogue with gandalf, 2026-05-16
