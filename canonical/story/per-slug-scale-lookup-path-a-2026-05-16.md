# Per-Slug Scale Lookup Table — Path A (re-anchored to chierit player baseline)

**Status:** **Canonical recommendation.** Authored 2026-05-16 by gandalf per knight-rider dispatch (`agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-table-path-a.md`), Matt-approved at Day 4 close: *"Path A — scale down to the common chierit player sprite. Scaling that up would just look awkward."*

**Purpose:** Operationalize the Day-4 Path A lock into a per-slug scale recommendation usable by the drax `MONSTER_SCALE_BY_SLUG` refactor + the per-character chierit scale revision. Re-anchors the Diablo-lineage tier-size hierarchy proportionally downward against actual chierit player figure-content. Resolves the four math-impossibility cases (per `sprite-scale-math-impossibility-rulings-2026-05-16.md`) into Path A-anchored operational scales.

**Path B (upscale chierit ~1.85× to reach 80 px HD-2D reference) was rejected by Matt at Day-4 close** on player-experience + viewport-pressure grounds.

**Consumes:**
- `agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-table-path-a.md` (this dispatch)
- `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (my prior canonical rulings)
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` (drax v0.20.4 PIL measurements)
- `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md` (drax v0.20.2 composite)
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` (legolas Section 4 synthesis)

**Feeds:**
- knight-rider's forthcoming drax `MONSTER_SCALE_BY_SLUG` refactor dispatch
- knight-rider's forthcoming drax per-character chierit-scale revision dispatch
- Matt-decision queue (god-of-lightning resolution; D14/D15 discipline authoring)

**Companion canonical:**
- `style-register.md` — HD-2D-pixel register lock (the consumption-time filter this table honors); the "80–100 px HD-2D target" referenced there now reads as **aspirational reference, not operational constraint** in the Path A world — see § "Style-register reconciliation" below
- `enemy-visual-legibility.md` — tier-coded silhouette / aura / banner hierarchy (the perceptual architecture this table serves)
- `gandalf-design-lineage.md` Layer 2 — Diablo size-hierarchy lineage

---

## TL;DR

- **Chierit operational scale: Option (i).** Default scale `1.0×` for all chierit characters; natural figure content 34–57 px rendered (Group A 53–57 / B 42–44 / C 34–39); player baseline midpoint **≈ 44 px** with Group-specific variance preserved as design feature.
- **Path A tier ranges (re-anchored to ~44 px player baseline):** trash 26–37 px / elite 44–57 px / mini-boss 66–88 px / boss 110–176 px. **(Magic tier 35–44 px reserved for future; engine doesn't emit this tier currently.)**
- **All 11 ENEMY_TIER monsters: scale recommendations land cleanly inside tier ranges** with the exception of two flagged cases (fire-elemental tier-coherence violation accepted at VS2a per swap-queue for VS2b; god-of-lightning blocked on Matt-decision, palette-shift `Fire_Lord_Creativkind` is the recommended zero-cost resolution).
- **Schema additions for drax refactor:** `width_or_height_priority` per-slug flag (for fire-elemental width-dominant case); `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` enforcement for all monster textures (hard requirement for upscales > 1.0×; forward-discipline for all).
- **Two open Matt-decisions surfaced:** god-of-lightning resolution path (recommend `Fire_Lord_Creativkind` palette-shift); sword-warrior transparent-padding inspection (drax bbox confirmation hygiene; non-blocking).

---

## Part 1 — Chierit operational scale recommendation

### The three options framed

The dispatch frames three options:

- **Option (i):** chierit default `1.0×` → natural figure content 34–57 px → player baseline ~44 px midpoint, Group A/B/C variance preserved
- **Option (ii):** chierit default keeps at `0.35` → ~12–20 px player baseline (figure content × 0.35) → monsters re-anchor to *micro* absolute sizes (swarm becomes essentially invisible at typical mobile viewport)
- **Option (iii):** per-character chierit scale lookup → normalize all chierit figure-content to a single target (e.g., scale each character so figure-content renders at ~50 px uniformly)

### Selection: **Option (i)** — default `1.0×` for all chierit characters

### Rationale

**Three converging reasons:**

#### (a) Option (ii) is operationally infeasible at any reasonable viewport

At `0.35`, the chierit player body renders at 12–20 px (per my PIL-corrected math; the prior "31 px at 0.35" figure was canvas-height × scale, not figure-content × scale). Re-anchoring monster tiers proportionally against a 12–20 px player gives **trash 7–17 px / elite 12–26 px / mini-boss 18–40 px / boss 30–80 px.** A 7 px trash mob is *not a silhouette* — it is a *pixel cluster*. The genre's tier-coded silhouette architecture (`enemy-visual-legibility.md` S1) requires that trash mobs be at minimum *parseable as creature shapes* at 200ms recognition; below ~25 px figure-content, parseable creature-shape recognition fails for everything but the simplest single-color silhouettes. Option (ii) collapses the entire perceptual hierarchy. Rejected.

#### (b) Option (iii) homogenizes characters and loses chierit's intrinsic design distinction

The chierit Elementals set is **deliberately not uniform.** Per drax v0.20.4 PIL measurements:

- Group A (Shadow Stalker, Light Valkyrie): tall figures, 53–57 px
- Group B (Fire Knight, Lightning Ronin, Metal Bladekeeper, Leaf Ranger): mid-figures, 42–44 px
- Group C (Water Priestess, Wind Hashashin, Crystal Mauler, Ground Monk, also Crystal Mauler at 39 px): compact figures, 34–39 px

This variance is **the asset author's design choice**: Shadow Stalker is *meant* to read as a tall, cape-extended silhouette (its dark register requires height to carry visual presence); Ground Monk is *meant* to read as a compact, grounded squat (his earth-anchored class fantasy is *low to the ground*); Water Priestess is *meant* to read as light-on-her-feet (figure shorter because her stance is lifted from the ground). **Normalizing all 10 characters to a uniform ~50 px figure-content erases these intentional silhouette differences.** A "Tall Shadow Stalker" reduced to the same rendered height as a "Squat Ground Monk" reads as *the silhouettes are identical to the renderer* — which is exactly the kind of within-class flattening that the form-bias work (`canonical/37-form-bias-diagnosis-and-recovery.md`) pushes against. The intra-class variance is a feature.

Genre lineage: D2's Druid (caster, normal-stature) vs Barbarian (brute, tall-stature) vs Amazon (sniper, slim-stature) are NOT pixel-normalized to a uniform body height; the player reads class from silhouette before reading from gear or aura. The chierit set ships with this discipline already in place. Option (iii) would undo it.

Rejected — but with one carve-out: **if at a later milestone the variance becomes a player-feel problem (Ground Monk reads as "too small" against Group A teammates in a hypothetical co-op or split-screen view), per-character scale lookup becomes the answer.** That is a deferred decision; the variance is design-intent at VS2a.

#### (c) Option (i) lands the player baseline at the empirical midpoint of the chierit author's own design

At `1.0×`, figure-content renders at 34–57 px natural pixel size. Midpoint ≈ 44 px. This is **what the chierit author drew.** No interpolation, no upscale artifacts, no pixel art quality loss. The 288×128 frame canvas's transparent padding is *intentional* — it leaves room for animation extension (Fire Knight's flame trails, Shadow Stalker's cape sweep, attack-frame extension into the surrounding canvas). Rendering at `1.0×` preserves the author's drawn pixel size as the source-of-truth.

The Path A monster tier hierarchy below re-anchors against this 44 px midpoint, which carries two clean properties:

1. **All monster scales become downscales** (with the two flagged exceptions): pixel art downscales cleanly with nearest-neighbor; no quality loss; matches the asset's intrinsic design.
2. **Viewport pressure dissolves.** The drax v0.20.4 notes flagged a 1152–1440 px combat-view viewport pressure at 2.0–2.5× chierit scale. At 1.0× chierit the full 288 px canvas width fits in any standard viewport (mobile 414 px portrait, desktop 800–1920 px) with room to spare.

### Implementation note for drax chierit-scale revision

- **Default `CHIERIT_DEFAULT_SCALE = 1.0`** (per-character override structurally identical to `MONSTER_SCALE_BY_SLUG` if the deferred Option (iii) ever activates).
- **No per-character override at VS2a** — all 10 characters render at 1.0×, intrinsic figure variance preserved.
- **Ground Monk anchor offset note:** per drax v0.20.4 notes anomaly #3, Ground Monk's figure content bottom lands at row 121 (not 127) — 6 px gap to frame bottom. At 1.0× this becomes a 6 px visible float. Hygiene item: drax should apply a per-character `y_anchor_offset` of +6 px for Ground Monk to ground-anchor cleanly. Out of scope for the scale refactor itself; flag as separate anchor-tuning follow-on.
- **Samurai (GandalfHardcore portrait, 640×640) remains out of scope** — portrait-only asset, no animation sheet; do not include in the chierit scale path.

---

## Part 2 — Path A monster tier ranges (re-anchored)

Anchored against chierit player figure-content midpoint **≈ 44 px** at scale 1.0×.

| Tier | Player-relative scale | Rendered figure-content height | Anchor character (genre lineage) |
|---|---|---|---|
| **Swarm** | 0.40–0.60× player | 18–26 px | D2 Quill Rat / PoE Skitter — sub-trash pack-creatures; **engine does not currently emit this tier** but reserved for future VS2c+ expansion |
| **Trash** | 0.60–0.85× player | **26–37 px** | D2 Fallen / PoE white-rarity zombies — parseable silhouette, smaller-than-player by design |
| **Magic** | 0.80–1.00× player | 35–44 px | D2 magic-blue affixed white mobs — engine doesn't emit this tier currently; **reserved** for future |
| **Elite** | 1.00–1.30× player | **44–57 px** | D2 champion-yellow elite packs / D3 elite-pack-leader; visibly *more* than the player |
| **Mini-boss** | 1.50–2.00× player | **66–88 px** | D2 super-unique-purple (Bishibosh, Coldcrow); D3 yellow-elite-cap; readable as "stop and engage" |
| **Boss** | 2.50–4.00× player | **110–176 px** | D2 act-bosses (Andariel, Duriel scaled); D3 launch-cinematic boss-tier; PoE conqueror-tier presence |
| **Act-boss / Trial-encounter** | 4.00–6.00× player (cinematic) | 176–264 px | D2 final-act bosses (Diablo, Baal); D3 culmination renders; reserved for Trial-encounter cinematic frames per `enemy-visual-legibility.md` S4 |

**Notes on the ranges:**

- **Tier midpoints** (the operational target for each per-slug scale calc): trash 32 px / elite 51 px / mini-boss 77 px / boss 143 px.
- **Range width** is intentionally wider at higher tiers — boss-tier variance is *aesthetic asset* (one boss reads as humanoid-tall, another as bulky-bipedal, another as quadruped-wide); the range absorbs intrinsic silhouette differences.
- **Tier-coherence floor and ceiling:** if a monster lands *above* its tier ceiling, it visually mis-reads as the tier above; if *below*, it mis-reads as the tier below. Tier-coherence violations are explicit flags in the lookup table.
- **Path A vs original framing:** the original Diablo-lineage table I authored Day-4 used 55–75 / 90–115 / 130–180 / 225–360 px — those numbers were anchored to a Sea of Stars-class 80 px player body. Path A halves those proportionally to match chierit's actual ~44 px player body. Rulings (which case, which option) remain unchanged from the math-impossibility doc; only the specific scale factors recalibrate.

---

## Part 3 — Per-monster scale recommendation (all 11 ENEMY_TIER monsters)

Schema for each row: `slug | tier | intrinsic frame W×H | content bbox H (PIL) | recommended scale | rendered figure-content H | tier band | quality-loss flag | notes`.

The "content bbox H" column is the actual character-art height inside the frame (where PIL `getbbox()` measurements are available from my prior rulings doc). For monsters where I have not yet PIL-measured the bbox, the frame_h is used as denominator with a `bbox_unmeasured` flag.

### The table

| Slug | Tier | Frame W×H | Content bbox H | Scale | Rendered H | Tier band | Flag | Notes |
|---|---|---|---|---|---|---|---|---|
| **goblin-mage** | trash | 96×96 | ~80 (est, bbox_unmeasured) | **0.40×** | 32 px | in-band (26–37) | none | Clean downscale; sits at trash midpoint |
| **mutant-skeleton** | trash | 120×120 | ~100 (est, bbox_unmeasured) | **0.32×** | 32 px | in-band (26–37) | none | Clean downscale; sits at trash midpoint |
| **evil-eye** | trash | 64×64 | ~52 (est, bbox_unmeasured; floating-eye circular) | **0.60×** | 31 px | in-band (26–37) | none | Near-1:1 (no upscale); sits at trash midpoint |
| **sword-warrior** | trash | 280×280 | 258 (PIL, from rulings doc) | **0.13×** | 34 px | in-band (26–37) | clean_downscale_extreme | Heavy downscale (~7.7× factor); pixel art tolerates; runtime memory-efficiency follow-on flagged in rulings doc § Case 3; see § Part 5 hygiene note |
| **crystal-golem** | elite | 168×141 | ~120 (est, bbox_unmeasured; compact body) | **0.42×** | 50 px | in-band (44–57) | none | Clean downscale; sits at elite midpoint |
| **fire-elemental** | elite | 192×68 | 55 (PIL, from rulings doc; width-dominant 151×55) | **0.85× (width-priority)** | 47 px H / 128 px W | in-band height; **width-flag** | tier_coherence_violation_accepted + width_or_height_priority_REQUIRED | See § Case A below — Per rulings doc Case 1, this is a (c)+queue-for-VS2b-swap case; render at scale that lands height in elite band, accept the 128 px rendered width as the wide-flat aesthetic intent; planned VS2b swap to `Fire_Lord_Creativkind` |
| **demon-mage** | elite | 192×128 | ~108 (est, bbox_unmeasured; row_index missing) | **0.48×** | 52 px (if bbox holds) | in-band (44–57) | row_index_metadata_missing | Frame extraction defaults to row_index=0; may not be true idle row; see § Part 5 routing note; recommend legolas/drax confirm idle row_index in metadata sweep |
| **lich** | mini_boss | 176×128 | ~115 (est, bbox_unmeasured; clean idle sheet available) | **0.70×** | 81 px | in-band (66–88) | none | Clean downscale; sits at mini-boss midpoint; lich has clean per-anim grid layout |
| **hellfire-rhino** | mini_boss | 234×112 | ~95 (est, bbox_unmeasured; quadruped, wide) | **0.78×** | 74 px H / 183 px W | in-band height | width_dominant_quadruped | Quadruped silhouette; height-anchor undersells horizontal presence; recommend drax confirms 183 px rendered width is acceptable for combat-view layout |
| **angel-guardian** | boss | 256×192 | 173 (PIL, from rulings doc) | **0.75×** | 130 px | in-band (110–176) | none | Per rulings doc Case 2, original was 1.30× UPSCALE against SoS-class 80px reference; under Path A this becomes a clean **downscale** to 130 px (mid-boss-band) — the upscale-quality concern dissolves; pixel art downscales cleanly with nearest-neighbor; nearest-neighbor still REQUIRED (forward discipline) |
| **god-of-lightning** | boss | 256×256 (1-frame) | 212 (PIL, from rulings doc) | **0.65× [BLOCKED at VS2a]** | 138 px (technically viable) | in-band (110–176) | ANIMATION_PACK_INCOMPLETE — DO NOT USE IN COMBAT | Scale is feasible; blocker is single-frame animation pack; **recommended Matt-decision: palette-shift `Fire_Lord_Creativkind` to thunder palette** per rulings doc Case 4 + `enemy-visual-legibility.md` S2; zero acquisition cost; see § Part 5 routing |

### Case A — fire-elemental width_or_height_priority detail

The fire-elemental's intrinsic geometry is **width-dominant**: 192×68 frame, 151×55 content bbox. Height-priority scaling (target the elite band 44–57 px) gives scale 0.85× → 47 px tall × 128 px wide. Width-priority scaling (target some max-width budget) would invert this.

**Recommendation:** **height-priority** at scale 0.85× → 47 px rendered figure-height, 128 px rendered figure-width. Rationale:

1. The elite tier's *vertical presence* is the load-bearing tier signal (taller-than-trash is the genre's silhouette grammar).
2. 128 px rendered width is acceptable in a typical combat viewport (mobile portrait 414 px allows three fire-elementals side-by-side; desktop 800 px allows six).
3. The wide-flat aesthetic is intentional per CreativeKind's design; preserving width-by-side-effect-of-height-priority maintains the asset's character.

**Schema requirement:** `width_or_height_priority` per-slug flag. Default `height` for all monsters. Override to `width` only if a specific monster's silhouette grammar requires width-anchored scaling (none currently in the VS2a roster — fire-elemental is height-priority despite being width-dominant). The flag is forward-protection for future acquisitions (e.g., a "wave" elemental, a "horizon" boss with extreme aspect ratio) where width-priority scaling becomes necessary.

### Case B — angel-guardian Path A downscale dissolves the upscale-quality concern

Under the original tier-hierarchy (boss midpoint 292 px against 80 px SoS player), angel-guardian required 1.52× upscale and the rulings doc Case 2 carefully argued for "(a) accept quality loss" — relying on nearest-neighbor + boss-tier aesthetic intent to convert "upscale blur" into "carved presence."

**Under Path A, angel-guardian becomes a clean downscale at 0.75×** to render at 130 px (mid-boss-band against 44 px chierit player). The quality-loss concern dissolves entirely. Pixel art downscales cleanly at 0.75× with nearest-neighbor enforcement. The "nearest-neighbor required" flag persists (forward discipline; bilinear at 0.75× still produces softening), but the *aesthetic-intent rationalization* is no longer load-bearing — the asset simply downscales correctly.

This is one of the cleanest Path A benefits: the boss-tier upscale-quality cases all dissolve into clean downscales, eliminating the prior "carved presence vs blur" judgment call.

### Case C — sword-warrior 0.13× downscale is large but clean

Path A drives sword-warrior to **scale 0.13×** (the rulings doc projected 0.13–0.17× for Path A). At 0.13×:
- Content bbox 258 × 0.13 = ~34 px rendered figure-height (in trash band)
- Frame 280 × 0.13 = ~36 px rendered total canvas (effectively the bbox dominates)
- Downscale factor 7.7× — large but pixel-art handles this cleanly with nearest-neighbor

The "extreme downscale = animation-frame information loss" concern remains valid: at this size, sword-warrior's swing arcs and posture transitions will read as silhouette-motion rather than as fine-grained animation. Per rulings doc Case 3, this is the **correct trash-tier behavior** — trash mobs are silhouette-readable, not detail-readable, by genre convention. Not a defect; design feature.

**Runtime memory note:** sword-warrior carries a 280×280 source texture even at 0.13× render scale. If many sword-warriors spawn (swarm-mode scenarios), each instance's GPU texture is substantial. Pre-downsample-at-load is the optimization (drax/star-lord engineering call; out of scope here). Flagged in rulings doc and re-flagged here for the drax refactor dispatch as P2 follow-on.

### Case D — demon-mage row_index metadata missing

Per drax v0.20.2 notes: demon-mage's metadata `row_per_anim` layout has no `row_index` set on the single "combined" animation entry. Frame extraction defaults to row_index=0, which may not be the idle animation row. The composite shows what may be an attack frame rather than an idle.

**Impact on scale recommendation:** scale 0.48× is computed against frame_h=128, which is consistent across all rows of a row_per_anim sheet. The *scale* is unaffected by row_index ambiguity. The *displayed sprite identity* (which animation frame plays as the idle reference) is the actual question.

**Recommended routing:** legolas (or drax in the MONSTER_SCALE_BY_SLUG refactor) sweeps the metadata.json for monsters with row_per_anim layouts and confirms idle-animation row_index. Demon-mage is the worked case; check if any other row_per_anim assets exist in the VS2a roster (per legolas Section 2 table, only demon-mage uses row_per_anim — single confirmation needed). Non-blocking for the scale refactor; hygiene for the integration notes.

---

## Part 4 — Schema-side recommendations for drax MONSTER_SCALE_BY_SLUG refactor

Two schema additions recommended for inclusion in knight-rider's drax refactor dispatch:

### Schema addition 1 — `width_or_height_priority` per-slug flag

**Field:** `width_or_height_priority: "width" | "height"` (default `"height"`)

**Purpose:** allow per-slug scale calculation to anchor against rendered-width budget instead of rendered-height budget when a monster's silhouette grammar is width-dominant.

**Usage:** the renderer reads this flag alongside the scale factor; if `"width"`, the scale is interpreted as "target rendered width = scale × source width" and the height-band is logged as informational only. If `"height"` (default), scale is interpreted as "target rendered height = scale × source height" and width is the dependent dimension.

**VS2a application:** none — all 11 monsters use `"height"` (default), including fire-elemental despite its width-dominant geometry (per § Case A rationale).

**Forward protection:** future acquisitions where width-priority scaling is required (e.g., a "wave" boss, a "horizon" elemental) can be flagged at integration time without touching the scaling architecture. The flag is **forward-discipline protection**, not a VS2a-active concern.

### Schema addition 2 — `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` enforcement

**Field:** **enforced at renderer-init time for all monster textures, not a per-slug field.**

**Purpose:** lock nearest-neighbor scaling on all monster sprites. Bilinear (Pixi.js default) scaling at any non-1.0× scale produces visible blur on pixel art; this is the dominant pixel-art quality-loss vector across the entire monster roster, not specific to any single slug.

**Hard requirements:**
- **Angel-guardian at Path A 0.75× downscale:** without nearest-neighbor, the downscale produces visible softening. Marked HARD REQ for VS2a per the rulings doc.
- **Forward discipline for all monsters:** all VS2a downscales (range 0.13×–0.85×) are degraded by bilinear filtering. Nearest-neighbor is the genre-correct default for pixel art at any scale.

**Implementation note for drax:** Pixi.js v7 syntax is `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` set at texture-creation time, OR via `baseTexture.style.scaleMode = 'nearest'` on the renderer setting. The legolas knowledge gap #5 ("Pixi.js nearest-neighbor confirmation") remains unresolved — drax should confirm during the refactor whether the current pipeline applies this and either (a) confirm it's already active and document, or (b) add it as part of the refactor's scope.

**Documentation requirement:** the refactor commit message and AGENT_STATE.md completion record should explicitly call out nearest-neighbor enforcement and confirm it's active in the rendered output. This closes legolas knowledge-gap #5.

### Schema addition 3 (recommended but lower priority) — `tier_coherence_violation` flag per-slug

**Field:** `tier_coherence_violation: boolean` (default `false`)

**Purpose:** explicit flag for monsters whose recommended scale lands them OUT of their canonical tier band (the fire-elemental case). Renderer behavior unchanged; this is a metadata/integration-notes hygiene flag for downstream consumers (LLM call signatures, telemetry, future tier-coherence audits).

**VS2a applications:**
- `fire-elemental: tier_coherence_violation: true, planned_resolution: "vs2b_swap_fire_lord_creativkind"`
- `god-of-lightning: tier_coherence_violation: false, but: animation_pack_incomplete: true, planned_resolution: "matt_decision_palette_shift_fire_lord_or_acquire"`

Priority is lower than Schema 1+2 because it's documentation-grade rather than rendering-correctness-grade. Knight-rider's call whether to include in the drax refactor or carry as a follow-on schema-extension dispatch.

---

## Part 5 — Open Matt-decisions surfaced for routing

### Decision 1 — god-of-lightning resolution path

**Question for Matt:** which path resolves god-of-lightning's animation_pack_incomplete blocker for VS2a thunder-boss coverage?

**Options:**

- **(A) Recommended — palette-shift `Fire_Lord_Creativkind` to thunder palette per `enemy-visual-legibility.md` S2.** Zero acquisition cost; the in-house Fire_Lord asset is already in the deferred-pack pool (drax MONSTER_TRACK_INTEGRATION_NOTES.md line 75). Palette-shift (fire-orange → thunder-blue/yellow) is a single texture-tint operation in Pixi.js. Element is communicated via palette per S2, not via base sprite morphology; this is a clean register-coherent solution.
- **(B) Investigate `God_of_Lightning_Dark_Version` (drax MONSTER_TRACK_INTEGRATION_NOTES.md line 76) frame count.** If the dark-variant pack has full animation frames, swap to it (becomes a (b)-swap, no acquisition). Low-cost research (drax inspection of one asset). If it's also single-frame, fall back to (A) or (C).
- **(C) Acquire alternate vendor pack** — Pixogen Full thunder pack (MONSTER_TRACK_INTEGRATION_NOTES.md line 91; gated on Matt's PayPal availability; ~$5–15). Fallback only if (A) and (B) both fail.

**Recommendation:** **(A) palette-shift Fire_Lord_Creativkind to thunder.** Zero cost, fastest, register-coherent.

**Note on VS2a interim state:** until Matt decides, **mark god-of-lightning as NOT-CANONICAL for VS2a combat rendering** (do not use in trial-encounters or act-boss slots). If a thunder boss is needed for VS2a element coverage now, route to Fire_Lord_Creativkind with thunder palette as the temporary stand-in (which is also the recommended permanent path).

### Decision 2 — sword-warrior transparent-padding bbox confirmation

**Question for Matt:** is this routing hygiene-only, or does it warrant a dedicated inspection dispatch?

**My read:** **hygiene-only.** The PIL measurement (content bbox 258×280 inside 280×280 frame) is from my rulings-doc empirical pass and is robust. The downscale to 0.13× under Path A is large but pixel-art-clean. No tier-coherence violation; sword-warrior lands in-band at 34 px rendered.

**Recommendation:** drax confirms bbox in the MONSTER_SCALE_BY_SLUG refactor completion record (single-line confirmation: "sword-warrior content bbox 258×280 of 280×280 frame confirmed at refactor time, scale 0.13× lands at 34 px rendered figure-height"). No separate inspection dispatch needed.

### Decision 3 (carryforward from rulings doc, surfaced again for completeness) — D14 + D15 discipline authoring

**Question for Matt:** authorize gandalf-and-jack-ryan co-authoring of D14 (vendor intrinsic-size pre-acquisition check) and D15 (per-vendor animation-completeness gate) into `reincarnated-engine/design/working-agreement/engineering-disciplines.md`?

**Recommendation:** authorize. Both disciplines emerged from the math-impossibility rulings work; both would have caught the fire-elemental tier mismatch and the god-of-lightning animation gap before integration time; both have low authoring cost and substantial forward-cost-savings.

Knight-rider to sequence per the design-track-quality-track pairing pattern.

### Decision 4 (lower-priority observation) — viewport / camera architecture decision

**Observation, not blocking:** even at Path A's restrained scale ranges, a combat scenario with the player + a boss-tier monster (140 px figure on a 288 px canvas frame at 1.0× chierit = 288 px wide chierit canvas + 256 × 0.75 = 192 px wide boss canvas = ~480 px combined horizontal canvas footprint) plus multiple trash mobs may push against a mobile portrait viewport's horizontal budget (414 px typical).

**This is a deferred architecture concern**, not a scale-refactor concern. Drax's v0.20.4 notes mention "render the content bbox region only, not the full 288×128 frame" as a future optimization — that would dissolve the canvas-padding contribution and tighten the viewport budget. Out of scope for the per-slug scale lookup table; flag for future camera/viewport architecture call when drax tackles combat-view layout.

---

## Style-register reconciliation

The `style-register.md` doc references an "80–100 px HD-2D target" rendered character height as the empirical anchor for the HD-2D-shaped register lock. The Section 3 amendment in legolas's pixel-scale research grounded this in Octopath Traveler's 80–90 px overworld and 120–130 px battle camera measurements.

**Under Path A, the chierit player renders at ~44 px figure-content height, not 80 px.** This is a deliberate departure from the OT-anchored reference, justified by:

1. **Source-asset budget.** The chierit Elementals pack ships at 34–57 px figure-content per frame. Upscaling to 80 px requires ~1.85× — itself a pixel-art quality concern at the 1.5× threshold. Matt's "scaling that up would just look awkward" Day-4 framing is the player-experience-grounded version of this same constraint.
2. **HD-2D register != HD-2D pixel count.** The HD-2D *aesthetic* — pixel-resolution sprites in a hand-drawn-illustration register, paired with detailed environmental art — is preserved at 44 px chierit baseline. The *pixel count* is what differs from OT's 80–90 px. The register is *the rendering aesthetic and asset register*, not a literal pixel measurement.
3. **Viewport coherence.** Path A keeps the full chierit canvas (288 px wide) inside any standard mobile viewport at 1.0×. Path B at 1.85× upscale would push canvas width to 533 px — beyond mobile portrait 414 px without horizontal clipping.

**Action item for style-register.md:** add a clarification note that the "80–100 px HD-2D target" is a *register reference anchor* (the visual aesthetic and register comparison) not an *operational pixel-count constraint* on the project's specific assets. The locked register survives Path A intact; the per-asset pixel count is determined by the source-asset author's intrinsic frame-content sizes. Knight-rider to route this clarification as a small follow-on (gandalf authoring; minor; non-blocking). **2026-05-16 Day-4 close — LANDED:** `canonical/story/style-register.md` § "Path A reconciliation — '80–100 px HD-2D target' is register aesthetic reference, not operational pixel-count constraint" added per knight-rider canonical-followon-amendments-batch dispatch. Bidirectional cross-reference complete.

---

## Cross-references

- `agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-table-path-a.md` — this dispatch
- `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` — prior canonical rulings (this doc operationalizes them at Path A)
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` — drax v0.20.4 PIL measurements (chierit figure-content 34–57 px)
- `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md` — drax v0.20.2 monster composite + 4 sizing concerns
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — legolas Section 4 synthesis + intrinsic source-sheet sizes + Section 3 OT/SoS measurements
- `canonical/story/style-register.md` — HD-2D-pixel register lock; see § "Style-register reconciliation" above for the Path A clarification
- `canonical/story/enemy-visual-legibility.md` — tier-coded silhouette/aura/banner architecture (S1–S6); the perceptual hierarchy this lookup table serves
- `canonical/story/gandalf-design-lineage.md` Layer 2 — Diablo I/II/III/IV/Immortal size-hierarchy lineage
- `reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md` — deferred-pack roster for option-(b) candidates and palette-shift swap targets
- `reincarnated-demo/src/visuals/monsterSprites.ts:73` — ENEMY_TIER_CHARACTER_MAP (drax refactor target)

---

## Maintenance protocol

When the drax `MONSTER_SCALE_BY_SLUG` refactor lands with the per-slug scale values from this table:
- This doc remains the **rationale-of-record** for each per-slug scale.
- The drax `MONSTER_SCALE_BY_SLUG` constant becomes the operational source-of-truth.
- Any scale change at the constant level should reference this doc + the rulings doc; downstream consumers (LLM call signatures, telemetry) consume the constant.

When Matt resolves the god-of-lightning decision:
- Replace the `[BLOCKED at VS2a]` flag with the resolution path (palette-shift / dark-version-swap / acquire).
- If palette-shift `Fire_Lord_Creativkind`: scale 0.65× applies to Fire_Lord's intrinsic frame (likely different from god-of-lightning's 256×256; re-compute against Fire_Lord's actual frame size when integrated).

When VS2b roster expansion happens:
- fire-elemental's planned swap to `Fire_Lord_Creativkind` (or `Elemental_mage`) becomes the operational move.
- This table extends with new slugs; the tier ranges in § Part 2 remain stable unless Path A re-anchor decision changes.

When future Path A vs Path B reopen happens (unlikely given Matt's Day-4 lock, but possible if VS2c+ asset acquisition introduces native-80-px-author content):
- The scale factors here recalibrate proportionally; the tier-band schema and the rulings remain valid.

---

## Part 6 — Path A-prime amendment (added 2026-05-16 Day 4 evening)

**Authority:** Matt, 2026-05-16 Day 4 evening — direct authorization "all authorized" following gandalf surfacing the ARPG-vs-JRPG pixel-scale reframing per Legolas Section 4d ground-truth resolution.

**What this amendment does.** Re-anchors the entire Path A operational table against the **corrected ARPG-genre chierit baseline (~115 px midpoint of 100-130 px ARPG band at 1080p displayed resolution)**, replacing the prior ~44 px chierit baseline that was anchored against JRPG-overworld 80-100 px conventions. Matt-locked Diablo genre ratios (swarm 0.6-0.85×, magic 0.8-1.0×, elite 1.0-1.3×, mini-boss 1.5-2.0×, boss 2.5-4.0×) are PRESERVED; only the absolute baseline shifts.

**What this amendment does NOT do.** Does not re-open Path A vs Path B framing. Does not re-litigate Matt-locked Diablo ratios. Does not invalidate the rulings doc cases A/B/C/D structurally (only the specific scale numerics shift). Does not re-author Parts 1-5 of this doc (preserved as historical record of the Day-4 mid-day Path A authoring).

**Cross-references this amendment consumes:**
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` § Section 4d — the semantic resolution (battle camera vs overworld; ARPG single-camera = 100-130 px at 1080p)
- `canonical/story/embodiment-display-loadout.md` § 1.1 — ARPG-anchored pixel-scale framing (committed `85ce42f`)
- `canonical/story/style-register.md` § "Path A reconciliation" — register aesthetic vs operational pixel-count framing (in-flight gandalf-instance amendment + this evening's follow-on)
- `canonical/story/arena-room-hallway-system.md` — Diablo/PoE single-camera framing commits to ARPG genre signal

---

### 6.1 Why ~44 px was the wrong baseline

Path A (Parts 1-5 above) anchored against ~44 px chierit player figure-content because:
- The Section 4d semantic resolution had not yet returned when Path A authored
- The prior 80-100 px target referenced JRPG-overworld conventions (Octopath overworld 80-90 px; Sea of Stars overworld ~80 px)
- A chierit "1.0× native scale" was operationally pragmatic ("ship with what's in front of us")

Three structural problems with that baseline:

1. **JRPG-overworld is not the right reference for Reincarnated.** Reincarnated has ONE camera (drax shipped Diablo/PoE room/hallway topology Day 4 morning); JRPG dual-camera architecture (overworld 80-100 px + battle camera 75-130 px) doesn't apply. ARPG single-camera convention sits at 100-130 px at 1080p.

2. **44 px chierit reads as undersized against ARPG genre canon.** Diablo IV characters at 1080p sit at 110-130 px; PoE at 100-120 px; Last Epoch at 100-110 px. A 44-px Reincarnated character against a 30m room (1440 px wide at PIXELS_PER_METER=48) is ~3% of room width — well below the ARPG single-camera ~8-9% standard.

3. **Path A's "downscale dissolves upscale concern" benefit was a baseline-specific artifact.** angel-guardian Path A 0.75× downscale (Case B in Part 3) became a clean downscale only because the boss target was 143 px against the 44 px chierit baseline. At Path A-prime, boss target is 374 px (3.25× of 115 px), and angel-guardian's 173 px bbox requires 2.16× upscale — restoring the original rulings-doc Case 2 logic ("accept quality loss with nearest-neighbor"). Boss-tier upscale concern returns.

### 6.2 Path A-prime chierit baseline — 115 px ARPG midpoint

**Operational chierit baseline at scale 1.0× = 88 px figure content** (per Legolas Section 1 measurement; canvas 288×128, character art ~80-96 px range, midpoint 88 px).

**Operational chierit scale = 1.31×** (115 / 88 = 1.30682) → renders at ARPG midpoint 115 px. Acceptable range **~1.14-1.48×** corresponding to ARPG band 100-130 px.

**Why 1.31× midpoint:**
- Aligns to ARPG band midpoint (100-130 px → 115 px) without privileging either D4 (~120 px) or D3 (~105 px) as the anchor
- Modest upscale (1.31× < 2×); pixel-art renders cleanly with nearest-neighbor; no quality concerns
- Conservatively positioned relative to viewport — 115 px player in 1440 px room = 8% of room width, matching Diablo III/IV positional combat readability
- Drax's room/hallway topology designed today targets this scale band (per knight-rider intuition; verified empirically below)

**Required nearest-neighbor enforcement:** chierit at 1.31× requires Pixi.js `SCALE_MODES.NEAREST` for pixel-coherent upscale rendering. Without enforcement, bilinear interpolation softens the chunky-pixel aesthetic into "blurry retro-pixel-art." Drax confirms enforcement in `MONSTER_SCALE_BY_SLUG` refactor dispatch.

### 6.3 Path A-prime tier midpoints

Recomputed against 115 px chierit player baseline using Matt-locked Diablo ratios:

| Tier | Player-relative scale | Rendered figure-content height (Path A-prime midpoint) | Anchor character (genre lineage) |
|---|---|---|---|
| **Swarm** | 0.40-0.60× player | 46-69 px (~58 px midpoint) | D2 Quill Rat / PoE Skitter — reserved for VS2c+ |
| **Trash** | 0.60-0.85× player | **69-98 px (~83 px midpoint)** | D2 Fallen / PoE white-rarity zombies |
| **Magic** | 0.80-1.00× player | 92-115 px | reserved for VS2c+ |
| **Elite** | 1.00-1.30× player | **115-150 px (~132 px midpoint)** | D2 champion-yellow / D3 elite-pack-leader |
| **Mini-boss** | 1.50-2.00× player | **173-230 px (~201 px midpoint)** | D2 super-unique-purple / D3 yellow-elite-cap |
| **Boss** | 2.50-4.00× player | **287-460 px (~374 px midpoint)** | D2 act-bosses / D3 cinematic boss-tier |
| **Act-boss / Trial-encounter** | 4.00-6.00× player (cinematic) | 460-690 px | D2 final-act bosses; reserved for Trial cinematic frames |

**Tier-coherence rationale preserved** — same genre logic as Part 2; only the absolute pixel values shift.

### 6.4 Path A-prime per-slug scale recommendations

Recomputed for all 11 ENEMY_TIER monsters (same source-of-truth bbox data from Part 3 + Legolas Section 2):

| Slug | Tier | Frame W×H | Content bbox H | **Path A-prime scale** | **Rendered H** | Path A (old) scale | Tier band | Quality flag |
|---|---|---|---|---|---|---|---|---|
| **goblin-mage** | trash | 96×96 | ~80 | **1.04×** | 83 px | 0.40× | in-band (69-98) | clean near-1:1 |
| **mutant-skeleton** | trash | 120×120 | ~100 | **0.83×** | 83 px | 0.32× | in-band (69-98) | clean downscale |
| **evil-eye** | trash | 64×64 | ~52 | **1.60×** | 83 px | 0.60× | in-band (69-98) | upscale; nearest-neighbor critical |
| **sword-warrior** | trash | 280×280 | 258 (PIL) | **0.32×** | 83 px | 0.13× | in-band (69-98) | clean downscale |
| **crystal-golem** | elite | 168×141 | ~120 | **1.10×** | 132 px | 0.42× | in-band (115-150) | near-1:1; nearest-neighbor critical |
| **fire-elemental** | elite | 192×68 | 55 (PIL; width-dominant) | **2.40× (height-priority)** | 132 px H / 363 px W | 0.85× | in-band height; **width-flag** | high upscale; nearest-neighbor critical; width-priority concern returns (363 px renders is very wide; recommend VS2b swap to Fire_Lord) |
| **demon-mage** | elite | 192×128 | ~108 | **1.22×** | 132 px | 0.48× | in-band (115-150) | clean upscale; nearest-neighbor critical |
| **lich** | mini_boss | 176×128 | ~115 | **1.75×** | 201 px | 0.70× | in-band (173-230) | clean upscale; nearest-neighbor critical |
| **hellfire-rhino** | mini_boss | 234×112 | ~95 | **2.12×** | 201 px H / 497 px W | 0.78× | in-band height; **width_dominant** | high upscale; nearest-neighbor critical; 497 px rendered width is very wide for combat-view |
| **angel-guardian** | boss | 256×192 | 173 (PIL) | **2.16×** | 374 px | 0.75× | in-band (287-460) | high upscale; rulings-doc Case 2 logic RESTORED — accept quality loss with nearest-neighbor enforcement |
| **god-of-lightning** | boss | 256×256 (1-frame) | 212 (PIL) | **1.76× [STILL BLOCKED at VS2a]** | 374 px | 0.65× | in-band (287-460) | animation-pack-incomplete (independent of scale); recommended Matt-decision: palette-shift Fire_Lord_Creativkind to thunder per Part 5 Decision 1 |

### 6.5 What Cases A/B/C/D become under Path A-prime

#### Case A — fire-elemental width_or_height_priority

**Still applicable; the width concern intensifies.** At Path A-prime 2.40× height-priority scale, fire-elemental renders at 132 px tall × 363 px wide. At desktop 800-px combat view, that's 45% of viewport width per fire-elemental. The original Path A 128 px rendered width was tolerable; Path A-prime 363 px rendered width is intrusive.

**Updated recommendation:** **expedite the VS2b swap to Fire_Lord_Creativkind** rather than accept 363 px wide fire-elementals at VS2a. The Fire_Lord asset has standard humanoid silhouette; height-priority scaling produces width-coherent rendering. Defer fire-elemental to post-VS2a/VS2b roster cleanup OR sub-tier explicitly as "wide elite slot."

Alternative: ship VS2a with fire-elemental at Path A-prime scale 2.40× and accept the wide-flat presence as deliberate; revisit if playtest signal demands. Less recommended.

#### Case B — angel-guardian Path A downscale-dissolves benefit LOST under Path A-prime

**The original rulings-doc Case 2 logic ("accept quality loss with nearest-neighbor") is RESTORED.** Path A-prime 2.16× upscale on angel-guardian reverts the "carved presence vs blur" judgment call. With strict nearest-neighbor enforcement, 2.16× lands cleanly as "intentional carved-up pixel-art upscaling, ARPG genre-appropriate at boss tier." Without nearest-neighbor, the upscale blurs.

**Required:** Pixi.js `SCALE_MODES.NEAREST` enforcement for angel-guardian specifically (and recommended globally for all monsters; tracked as Part 4 Schema Addition 2).

The Path-A "upscale concern dissolves" was specific to the ~44 px baseline. Path A-prime returns to the original framing; no surprise.

#### Case C — sword-warrior 0.13× → 0.32× under Path A-prime

**Downscale eases substantially.** 0.32× is a ~3× downscale (vs Path A's ~7.7×). Still a downscale; still pixel-art-clean. The runtime memory note remains valid (280×280 texture still oversized for 83 px rendered output; pre-downsample-at-load remains the optimization).

**No structural change to Case C ruling.** Just easier on quality.

#### Case D — demon-mage row_index metadata missing

**Unchanged.** The scale recommendation is unaffected by row_index ambiguity (frame_h is row-consistent for row_per_anim layouts). Demon-mage scale shifts from 0.48× to 1.22×; the metadata-sweep recommendation (legolas or drax confirms idle-anim row_index) persists.

### 6.6 Drax MONSTER_SCALE_BY_SLUG values for Path A-prime refactor

**Operational lookup table for drax to implement** (replaces Path A values from Part 3):

```typescript
// MONSTER_SCALE_BY_SLUG (Path A-prime; chierit baseline 1.31× → 115 px ARPG midpoint)
const CHIERIT_PLAYER_SCALE = 1.31; // ARPG midpoint of 100-130 px target
const MONSTER_SCALE_BY_SLUG: Record<string, number> = {
  // Trash tier (rendered ~69-98 px; midpoint 83)
  'goblin-mage': 1.04,
  'mutant-skeleton': 0.83,
  'evil-eye': 1.60,
  'sword-warrior': 0.32,

  // Elite tier (rendered ~115-150 px; midpoint 132)
  'crystal-golem': 1.10,
  'fire-elemental': 2.40, // width-priority concern; recommend VS2b swap to Fire_Lord
  'demon-mage': 1.22,

  // Mini-boss tier (rendered ~173-230 px; midpoint 201)
  'lich': 1.75,
  'hellfire-rhino': 2.12,

  // Boss tier (rendered ~287-460 px; midpoint 374)
  'angel-guardian': 2.16,
  // 'god-of-lightning': 1.76, // BLOCKED at VS2a; animation pack incomplete; pending Matt decision per Part 5 Decision 1
};
```

**Nearest-neighbor enforcement (universal):** `texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST` for all chierit + monster sprites per Part 4 Schema Addition 2. Critical under Path A-prime because most monsters are upscaled (vs Path A where most were downscaled); upscale-without-nearest-neighbor produces visible bilinear blur.

### 6.7 Drax v0.20.6 verification composite recommendation

Knight-rider's intuition (surfaced in evening check-in): at Path A-prime sprite scales, sprites may FIT drax's room/hallway topology cleanly without arena re-dimensioning — but verification before refactor lands is cheap insurance.

**Recommended composite spec:**
- 1 image OR strip showing: chierit player at 1.31× + 1 trash + 1 elite + 1 mini-boss + 1 boss positioned in a single rendered 30m-default room (per drax `arena-room-hallway-system.md` topology)
- All sprites at Path A-prime scales from § 6.6 lookup
- Composited against actual room/hallway background art (or solid floor tint if backgrounds aren't ready)
- Side-by-side OR sequential: same composition at the prior Path A 0.45-chierit-scale baseline for direct pre-vs-post visual comparison

**Estimated drax effort:** ~1-2h (extends v0.20.2/v0.20.3 Python/PIL composite tooling drax has now established as reusable methodology).

**Decision criterion for gate-pass:** does the composite read as ARPG-genre-correct (player + boss + trash mob coherently legible; positional combat readability preserved; no obvious viewport-pressure failures)?
- **If clean:** drax MONSTER_SCALE_BY_SLUG refactor dispatch fires with § 6.6 values
- **If viewport-pressure problems surface:** revisit Path A-prime baseline (consider 105-110 px instead of 115 px) OR re-open Path B framing

### 6.8 What this amendment unblocks

- Drax MONSTER_SCALE_BY_SLUG refactor dispatch (held since this evening per Decision 4 of knight-rider check-in) — Path A-prime values per § 6.6 are the operational target
- Drax v0.20.6 verification composite dispatch (knight-rider authors with § 6.7 spec)
- Chierit-track ingest pipeline dispatch (in flight) — chierit operational scale 1.31× becomes the canonical default for character rendering
- Style-register reconciliation follow-on amendment (separate; in this batch) — adds ARPG-anchored operational target alongside the in-flight 80-100 px aesthetic-reference framing

### 6.9 What persists from Path A (unchanged)

- Matt-locked Diablo genre ratios (swarm/trash/magic/elite/mini-boss/boss/act-boss)
- Schema-side recommendations (width_or_height_priority flag; nearest-neighbor enforcement; tier_coherence_violation flag)
- Open Matt-decisions surfaced in Part 5 (god-of-lightning resolution path; sword-warrior bbox confirmation; D14+D15 discipline authoring; viewport architecture decision)
- Cases A/B/C/D ruling-logic (only specific scale numerics shift)
- Maintenance protocol per Part 6 above (now refers to Path A-prime values as operational; Path A values preserved as historical record of mid-day baseline)

---

— gandalf, 2026-05-16 (Day 4 evening; Path A-prime amendment authored per Matt direct authorization following Legolas Section 4d return)

— gandalf, 2026-05-16
