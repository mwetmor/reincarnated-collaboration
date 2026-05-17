# Per-Slug Scale Lookup Table — Path A-prime (ARPG ~100–130 px chierit baseline)

**Status:** **Canonical recommendation v2.** Authored 2026-05-16 by gandalf per knight-rider dispatch (`agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-path-a-prime-v2.md`), Matt-approved at Day-4 close 2026-05-16: Path A-prime locked per ARPG-vs-JRPG reframing.

**Supersedes:** `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md` (v1, Path A). v1 is preserved as historical record. All per-slug scale recommendations, tier ranges, and the chierit operational scale **change** in this v2. The schema additions (`width_or_height_priority`, nearest-neighbor enforcement, `tier_coherence_violation`) carry forward unchanged with strengthened criticality (more monsters now upscale at Path A-prime).

**Purpose:** Operationalize Matt's Path A-prime lock (Day-4 close, 2026-05-16) into per-slug scale recommendations usable by the drax `MONSTER_SCALE_BY_SLUG` refactor + the per-character chierit-scale revision. Preserves Path A's tier-ratio architecture (Diablo-genre 0.6–0.85× swarm / 1.0–1.3× elite / etc.) but re-anchors the absolute baseline against ARPG single-camera convention (~100–130 px at 1080p displayed resolution) rather than the prior Path A's ~44 px chierit-native baseline.

**Why the re-anchor — ARPG-vs-JRPG reframing.** Path A anchored chierit at native 1.0× → ~44 px player figure-content. The implicit reference was JRPG/HD-2D overworld camera (Octopath ~80–90 px overworld; Sea of Stars ~75–90 px battle). Reincarnated is a **single-camera ARPG** — exploration and combat happen in the same view per the room/hallway arena topology (`canonical/story/arena-room-hallway-system.md`). The genre-convention pixel band for single-camera ARPGs at 1080p is ~100–130 px (Diablo IV ~110–130; Diablo III ~100–110; Path of Exile ~100–120; Last Epoch ~100–110; Grim Dawn ~90–110). This band gives characters enough screen-presence for positional combat readability against pack encounters. The HD-2D-shaped pixel-art register (`style-register.md`) is preserved — register is a visual-style commitment (chunky pixel edges, limited palette, hand-drawn-illustration sensibility), not an absolute pixel scale. **Path A-prime is a SCALE adjustment within the register, not a register change.**

**Consumes:**
- knight-rider dispatch `agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-path-a-prime-v2.md`
- v1 Path A lookup table (this doc supersedes): `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md`
- `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` — prior canonical rulings (still valid; scale factors recalibrate proportionally per the rulings doc's own maintenance protocol)
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` — drax v0.20.4 PIL measurements
- `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md` — drax v0.20.2 monster composite
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — legolas Section 1+2 intrinsic sizes + Section 3 ARPG-vs-JRPG ground truth
- `canonical/story/arena-room-hallway-system.md` — room/hallway topology (load-bearing for the viewport-pressure analysis)
- `canonical/story/embodiment-display-loadout.md` § 1.1 — ARPG-anchored pixel-scale framing (gandalf commit 85ce42f)

**Feeds:**
- knight-rider's drax `MONSTER_SCALE_BY_SLUG` refactor dispatch (currently held; unblock-trigger updated to "v2 lookup table return")
- knight-rider's drax chierit-scale-revision dispatch (per-character or uniform scale; this doc recommends uniform 2.5×)
- knight-rider's bbox-tightened sprite rendering follow-on dispatch (NEW at Path A-prime — see § "Viewport pressure analysis")

**Companion canonical:**
- `style-register.md` — HD-2D-pixel register lock (preserved at Path A-prime); see the § "Path A reconciliation" amendment landing concurrently with this v2 doc for ARPG operational target framing
- `enemy-visual-legibility.md` — tier-coded silhouette / aura / banner hierarchy (perceptual architecture this table serves)
- `gandalf-design-lineage.md` Layer 2 — Diablo size-hierarchy lineage; the ARPG genre convention this table anchors against
- `embodiment-display-loadout.md` § 1.1 — ARPG-anchored pixel-scale framing (gandalf commit 85ce42f); this v2 doc is the operational complement

---

## TL;DR

- **Chierit operational scale: sub-option (i-prime).** Default scale `2.5×` for all chierit characters. Group A (Shadow Stalker, Light Valkyrie) overshoots ARPG band ceiling by 3–13% (133–143 px vs 130 px ceiling); Group B (Fire Knight cluster) lands mid-band (105–110 px); Group C (Ground Monk cluster) undershoots band floor by 5–15% (85–98 px vs 100 px floor). Intra-class variance preserved as design feature — within ARPG genre tolerance (D4 Druid 130 px / D4 Necromancer 110 px is ~18% spread).
- **Path A-prime tier ranges** (anchored to chierit ~115 px midpoint at 2.5×): trash 70–98 px / elite 115–150 px / mini-boss 173–230 px / boss 287–460 px / act-boss 460–690 px (cinematic).
- **All 10 active monsters: per-slug scales land in tier band** with three operational flags. Several monsters become upscales (evil-eye, lich, hellfire-rhino, angel-guardian, fire-elemental height-priority) — **nearest-neighbor HARD REQ across the roster**, not just for one slug.
- **Roster change:** god-of-lightning REMOVED (palette-shift Fire_Lord_Creativkind to thunder palette, Matt-locked). `Fire_Lord_Creativkind` thunder-shift added as boss-tier thunder slot. (Total: 10 active monsters at Path A-prime, was 11 at Path A.)
- **Schema additions for drax refactor:** carry forward from v1 unchanged in shape; criticality strengthened. `width_or_height_priority` per-slug; nearest-neighbor enforcement (now applies to upscale roster, not just angel-guardian); `tier_coherence_violation` per-slug.
- **Viewport pressure analysis (NEW at Path A-prime):** drax v0.20.4 viewport concern returns in modified form. Pre-existing arena dimensions (default 30m room = 1440 px; small 15m = 720 px; large 45m = 2160 px) **accommodate Path A-prime figure-content footprints** without arena re-dimensioning. BUT: two follow-on engineering items become load-bearing — (1) bbox-tightened sprite rendering (drax v0.20.4 "evaluate" item) becomes priority; (2) default-room camera-follow re-validation. Both are drax/star-lord engineering calls, not arena topology calls.
- **Two open Matt-decisions surfaced beyond viewport** carried forward from v1 + math-impossibility rulings; D14 + D15 discipline authoring authorization remains the main forward-process item.

---

## Part 1 — Chierit operational scale recommendation (Path A-prime)

### The two sub-options framed (per dispatch)

- **Sub-option (i-prime):** uniform chierit default ~2.5× → most characters land in or near 100–130 px ARPG band; Group A slightly over, Group C slightly under. Preserves intra-class silhouette variance as design feature.
- **Sub-option (ii-prime):** per-character lookup normalizing all chierit to 110–120 px midpoint → Group A ~1.9–2.1×, Group B ~2.6–2.7×, Group C ~3.0–3.4×. Homogenizes intra-class silhouette.

### Selection: **sub-option (i-prime)** — uniform `2.5×` for all chierit characters

### Rationale

**Three converging reasons** (parallel to v1's Option-(i) rationale, recalibrated):

#### (a) Intra-class silhouette variance is a feature, not a defect

The chierit Elementals set is **deliberately not uniform.** Per drax v0.20.4 PIL measurements (confirmed):

- Group A (Shadow Stalker, Light Valkyrie): tall figures, 53–57 px content
- Group B (Fire Knight, Lightning Ronin, Metal Bladekeeper, Leaf Ranger): mid-figures, 42–44 px content
- Group C (Water Priestess, Wind Hashashin, Crystal Mauler, Ground Monk): compact figures, 34–39 px content

Sub-option (ii-prime) normalizes all 10 characters to a uniform ~115 px rendered figure. **This erases the asset author's intentional silhouette differences.** Shadow Stalker is meant to read as a tall, cape-extended silhouette (the dark register requires height to carry visual presence); Ground Monk is meant to read as a compact, grounded squat (his earth-anchored class fantasy is *low to the ground*); Water Priestess is meant to read as light-on-her-feet. Normalizing flattens these.

**Diablo lineage check:** D2's Druid (caster, normal-stature) vs Barbarian (brute, tall-stature) vs Amazon (sniper, slim-stature) are NOT pixel-normalized to a uniform body height. **D4 is even more explicit:** Druid renders ~130 px tall; Rogue ~110 px; Necromancer ~110 px; Barbarian ~125 px; Sorceress ~115 px. ~18% spread across the class roster, all within ARPG band. **Reincarnated at Path A-prime sub-option (i-prime) lands in the same intra-class-spread genre tradition.**

Group A overshoots ceiling by 3–13% (Shadow Stalker 142 px / Light Valkyrie 133 px vs 130 px ceiling). Group C undershoots floor by 5–15% (Ground Monk 85 px / Water Priestess 92 px / Wind Hashashin 92 px / Crystal Mauler 98 px vs 100 px floor). These deltas are **within ARPG-genre tolerance** — the band is convention not floor/ceiling-strict. Diablo IV Druid exceeds 130 px in idle stance frames; Path of Exile Marauder is shorter than band-floor in some stances. The band names the genre's center-of-gravity, not its edges.

#### (b) Sub-option (ii-prime) collides with the form-bias structural realignment work

Per `canonical/37-form-bias-diagnosis-and-recovery.md`, the project's form-bias work pushes against silhouette flattening. Normalizing 10 chierit characters to identical rendered heights is exactly the kind of within-class flattening the form-bias structural-realignment recommends against. The intra-class variance carried by the chierit asset set is a **substrate the form-bias work assumes is present** — flattening it at the rendering layer would require re-establishing variance later via embodiment-axis differentiation at a higher cost.

Sub-option (i-prime) preserves the substrate. Sub-option (ii-prime) erases it.

#### (c) Path A-prime tier hierarchy stays coherent against the ~115 px Group-B midpoint

The Group B cluster (Fire Knight, Lightning Ronin, Leaf Ranger, Metal Bladekeeper) lands at ~105–110 px at 2.5×. This is the **operational midpoint** for monster-tier ratio calculations (treating Group B as "player typical" for ratio anchoring). Tier ranges re-anchor against ~115 px (between Group B mid and ARPG-band center 115 px); Group A characters reading slightly larger than Group B is read as **class-fantasy weight** (Shadow Stalker = ominous tall presence; Light Valkyrie = winged uplift), not as tier-coherence violation; Group C characters reading slightly smaller is read as **class-fantasy compactness** (Ground Monk = grounded squat; Water Priestess = light dancer), again not as tier-coherence violation.

The "is the player taller or shorter than this monster" reading remains stable across the chierit roster because the **tier ratios** (the player-relative scales) are what carry the perceptual tier-coherence signal, not the absolute pixel counts.

### Why not sub-option (ii-prime)

- **Erases author intent.** The asset author drew variance; the renderer would un-draw it.
- **Erases form-bias substrate.** The structural realignment assumes intra-class variance exists in the asset layer.
- **Genre-deviation.** D2/D3/D4 all ship intra-class height variance; sub-option (ii-prime) would deviate from genre convention.
- **Higher per-character scaling produces more pixel-art quality stress.** Group C at 3.0–3.4× pushes upscale further from native than the 2.5× uniform. Pixel art tolerates 2.5× cleanly with nearest-neighbor; 3.4× is at the threshold.

### Per-character rendered figure-content heights at uniform 2.5×

| Character | Content_h | @ 2.5× | ARPG band fit |
|---|---|---|---|
| Shadow Stalker | 57 px | **142 px** | above (10% over 130 ceiling) |
| Light Valkyrie | 53 px | **133 px** | above (2% over 130 ceiling) |
| Leaf Ranger | 44 px | **110 px** | in-band (mid) |
| Fire Knight | 44 px | **110 px** | in-band (mid) |
| Lightning Ronin | 43 px | **108 px** | in-band (mid) |
| Metal Bladekeeper | 42 px | **105 px** | in-band (mid) |
| Crystal Mauler | 39 px | **98 px** | below (2% under 100 floor) |
| Water Priestess | 37 px | **92 px** | below (8% under 100 floor) |
| Wind Hashashin | 37 px | **92 px** | below (8% under 100 floor) |
| Ground Monk | 34 px | **85 px** | below (15% under 100 floor) |

**Mean rendered height: ~108 px.** Band-center for ARPG convention is ~115 px; the chierit set's natural author-drawn mean lands slightly under band-center, consistent with the asset family being more compact than the upper end of the ARPG band. Acceptable; no further re-anchoring needed.

### Implementation note for drax chierit-scale revision

- **Default `CHIERIT_DEFAULT_SCALE = 2.5`** (replacing v1's `1.0`; replacing prior `0.35` long ago).
- **No per-character override at VS2a** — all 10 characters render at 2.5×, intrinsic figure variance preserved.
- **Ground Monk anchor offset note** (carry forward from v1): per drax v0.20.4 notes anomaly #3, Ground Monk's figure content bottom lands at row 121 (not 127) — 6 px gap to frame bottom × 2.5× = **15 px visible float** at Path A-prime (vs 6 px at v1 Path A). The float is now load-bearing (15 px gap is visible at HD-2D fidelity); drax should apply a per-character `y_anchor_offset` of +6 px (in source pixels, applied before scale) for Ground Monk. **Priority bumped from hygiene to P1** at Path A-prime due to amplified visibility.
- **Samurai (GandalfHardcore portrait, 640×640) remains out of scope** — portrait-only asset; not in chierit scale path.
- **Forward-compat:** if a later milestone wants to migrate to sub-option (ii-prime), the per-character override structure mirrors `MONSTER_SCALE_BY_SLUG` and is a one-doc-amendment + one-constant-change away.

---

## Part 2 — Path A-prime monster tier ranges (re-anchored)

Anchored against chierit operational midpoint **~115 px** at uniform 2.5× (between Group B mean 108 px and ARPG band center 115 px; matches Sub-option (i-prime) mean of 108 px rounded to band-center).

| Tier | Player-relative scale | Rendered figure-content height | Anchor character (genre lineage) |
|---|---|---|---|
| **Swarm** | 0.40–0.60× player | 46–69 px | D2 Quill Rat / PoE Skitter — sub-trash pack-creatures; engine doesn't emit at VS2a; reserved |
| **Trash** | 0.60–0.85× player | **70–98 px** | D2 Fallen / PoE white-rarity zombies — parseable silhouette, smaller-than-player |
| **Magic** | 0.80–1.00× player | 92–115 px | D2 magic-blue affixed mobs — engine doesn't emit; reserved |
| **Elite** | 1.00–1.30× player | **115–150 px** | D2 champion-yellow elite / D3 elite-pack-leader — visibly *more* than the player |
| **Mini-boss** | 1.50–2.00× player | **173–230 px** | D2 super-unique-purple (Bishibosh, Coldcrow); D3 yellow-elite-cap |
| **Boss** | 2.50–4.00× player | **287–460 px** | D2 act-bosses (Andariel, Duriel); D3 launch-cinematic boss-tier; PoE conqueror-tier |
| **Act-boss / Trial-encounter** | 4.00–6.00× player (cinematic) | 460–690 px | D2 final-act bosses (Diablo, Baal); D3 culmination renders |

**Notes:**

- **Tier midpoints** (operational target for per-slug scale calc): trash 84 px / elite 132 px / mini-boss 200 px / boss 370 px / act-boss 575 px.
- **Comparison to v1 Path A:** v1 ranges (trash 26–37; elite 44–57; mini-boss 66–88; boss 110–176) recalibrate ~2.65× upward at Path A-prime — consistent with the chierit scale-up factor (44 px → 115 px = 2.61×).
- **Tier-coherence semantics unchanged.** If a monster renders above its tier ceiling, mis-reads as the tier above; below floor, mis-reads as tier below. `tier_coherence_violation` flag persists.
- **Boss-tier ceiling (460 px) is large.** A 460 px boss in a default 30m room (1440 px) occupies 32% of room width — visually appropriate for an act-boss culmination moment but viewport-load-bearing (see § Viewport pressure analysis).

---

## Part 3 — Per-monster scale recommendation (10 active monsters at Path A-prime)

Schema: `slug | tier | intrinsic frame W×H | content bbox H (PIL or est) | recommended scale | rendered figure-content H | tier band | width_or_height_priority | quality-loss flag | notes`.

### The table

| Slug | Tier | Frame W×H | Content bbox H | Scale | Rendered H | Tier band | W/H priority | Quality flag | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **goblin-mage** | trash | 96×96 | ~80 (est) | **1.05×** | 84 px | in-band (70–98) | height | minor_upscale_nearest_neighbor_REQ | Sits at trash midpoint; 1.05× is at native; minimal upscale artifacts |
| **mutant-skeleton** | trash | 120×120 | ~100 (est) | **0.84×** | 84 px | in-band (70–98) | height | clean_downscale | Sits at trash midpoint |
| **evil-eye** | trash | 64×64 | ~52 (est, floating-eye circular) | **1.62×** | 84 px | in-band (70–98) | height | **upscale_nearest_neighbor_HARD_REQ** | Upscales 1.62× — circular-eye morphology tolerates better than humanoid silhouettes; aesthetic intent is iconic-large-pixels |
| **sword-warrior** | trash | 280×280 | 258 (PIL) | **0.33×** | 85 px | in-band (70–98) | height | clean_downscale_extreme | Heavy 3× downscale; pixel art tolerates with nearest-neighbor; runtime memory P2 follow-on flagged in v1 (carry forward) |
| **crystal-golem** | elite | 168×141 | ~120 (est, compact body) | **1.05×** | 126 px | in-band (115–150) | height | minor_upscale_nearest_neighbor_REQ | Sits at elite mid-floor; near-native; minimal upscale artifacts |
| **fire-elemental** | elite | 192×68 | 55 (PIL, width-dominant 151×55) | **2.29× (height-priority)** | 126 px H / 346 px W | in-band height; **width-flag** | height | **tier_coherence_violation_accepted + upscale_nearest_neighbor_HARD_REQ + WIDE_FOOTPRINT** | Per v1 Case A logic + Path A-prime amplification: height-priority lands in elite band; rendered width 346 px is substantial (1/4 of default 30m room width); planned VS2b swap to `Fire_Lord_Creativkind` becomes higher-priority at Path A-prime; the 2.29× upscale is at the threshold |
| **demon-mage** | elite | 192×128 | ~108 (est, row_index missing) | **1.17×** | 126 px | in-band (115–150) | height | minor_upscale_nearest_neighbor_REQ + row_index_metadata_missing | Frame extraction defaults to row_index=0; per v1 carry forward; recommend legolas/drax confirm idle row_index |
| **lich** | mini_boss | 176×128 | ~115 (est) | **1.67×** | 192 px | in-band (173–230) | height | **upscale_nearest_neighbor_HARD_REQ** | Lich has clean per-anim grid layout; sits at mini-boss midpoint; 1.67× is below the 2× soft-ceiling; aesthetic intent is presence-via-pixel-size |
| **hellfire-rhino** | mini_boss | 234×112 | ~95 (est, quadruped wide) | **2.02×** | 192 px H / 473 px W | in-band height; width_dominant | height | **upscale_nearest_neighbor_HARD_REQ + WIDE_FOOTPRINT** | Quadruped silhouette; 473 px rendered width is wide (one-third of default 30m room); 2.02× upscale at the threshold |
| **angel-guardian** | boss | 256×192 | 173 (PIL) | **2.06×** | 356 px | in-band (287–460) | height | **upscale_nearest_neighbor_HARD_REQ** | Per v1 Case B logic: at Path A v1 this dissolved to clean downscale (0.75×); **at Path A-prime it returns to upscale (2.06×) — Case B's prior framing inverts back.** Nearest-neighbor + cinematic-aura compensate; same as math-impossibility rulings Case 2 logic resurfaces. See § Case B-prime |
| **Fire_Lord_Creativkind (thunder palette-shift)** | boss | (TBD; flagged) | (TBD; flagged) | **TBD (recommend ~2.0×)** | ~370 px target (boss midpoint) | in-band (287–460) target | height | **upscale_nearest_neighbor_HARD_REQ; INTRINSIC_SIZE_UNMEASURED** | Newly active at Path A-prime per Matt-decision palette-shift; intrinsic frame measurement needed (legolas or drax inspection at integration time); scale derived once measurement returns; placeholder 2.0× targets boss midpoint pending measurement |

### Case A-prime — fire-elemental width_or_height_priority detail (amplified at Path A-prime)

Per v1 Case A, fire-elemental's intrinsic width-dominant geometry (192×68 frame, 151×55 content bbox) yields height-priority scaling at 2.29× → 126 px tall × 346 px wide.

**What changes at Path A-prime:**

- **Rendered width 346 px** (vs v1's 128 px) is now substantial against the room. Default 30m room = 1440 px; 346 px = 24% of room width. A single fire-elemental is one-quarter of the room's horizontal real estate. **Two fire-elementals side-by-side consume half the room.**
- **Upscale 2.29× crosses the 2.0× soft-threshold** for pixel-art quality. Nearest-neighbor remains REQ; aesthetic tolerance is more strained than at v1's 0.85× downscale.
- **VS2b swap priority bumped.** The planned swap to `Fire_Lord_Creativkind` (or `Elemental_mage`) was a "VS2b queued" item at Path A v1; at Path A-prime, the rendered-width + upscale-threshold concerns make the swap **earlier-priority** — recommend knight-rider sequence the VS2b roster expansion sooner if room-cluttering becomes an empirical playtest finding.

**Recommendation persists:** **height-priority** at scale 2.29× → 126 px rendered figure-height, 346 px rendered figure-width. Rationale:

1. Elite tier's vertical presence is the load-bearing tier signal (taller-than-trash is genre silhouette grammar).
2. 346 px rendered width is acceptable in default 30m room with one fire-elemental at a time; multi-fire-elemental encounters need to be encounter-design-aware.
3. Wide-flat aesthetic per CreativeKind's design intent is preserved.

**Schema requirement (carry forward):** `width_or_height_priority` per-slug; default `"height"` for all; fire-elemental documented as height-priority despite width-dominant geometry per the rationale.

### Case B-prime — angel-guardian Path A-prime upscale returns

Under v1 Path A, angel-guardian dissolved to a clean downscale (0.75× → 130 px rendered) — the upscale-quality concern from math-impossibility rulings Case 2 dissolved entirely.

**At Path A-prime, the upscale returns.** Angel-guardian at boss midpoint 370 px requires 2.06× upscale from 173 px content bbox. The math-impossibility rulings Case 2 framing (boss-tier-as-aesthetic-choice; large pixels read as "carved presence" with nearest-neighbor; cinematic-tier aura compensates) **resurfaces as load-bearing rationale.**

This is the same architectural logic as in the original rulings doc: boss-tier visual stakes are highest; large pixels with nearest-neighbor read as "carved presence" not "low resolution"; the cinematic-tier aura + name-banner stack per `enemy-visual-legibility.md` S3/S5 carries the perceptual weight; HD-2D pattern specifically supports boss-pixel-size as a tier signal (Octopath Traveler boss sprites are visibly larger-pixel than field-explore characters by deliberate design).

**Hard requirement:** nearest-neighbor filtering must be active. The legolas knowledge-gap #5 ("Pixi.js nearest-neighbor confirmation") is now **operationally-critical at Path A-prime** — multiple monsters upscale; bilinear filtering would degrade the rendered output across the roster, not just at one slug.

### Case C-prime — sword-warrior downscale persists, severity reduced

Path A v1: sword-warrior at 0.13× (7.7× downscale). Path A-prime: sword-warrior at 0.33× (3.0× downscale).

The "extreme downscale → animation-frame information loss" concern (per v1 Case C) reduces. At 0.33× a 258 px body renders at 85 px — readable as silhouette-with-sword AND with visible animation detail (sword swing arcs more legible at 85 px than at 34 px).

**This is a Path A-prime benefit:** sword-warrior is more readable; trash-tier silhouette grammar preserved; animation detail more parseable. **Runtime memory note (carry forward):** sword-warrior still carries a 280×280 source texture; pre-downsample optimization remains a P2 follow-on for drax/star-lord.

### Case D-prime — demon-mage row_index metadata (carry forward unchanged)

Same as v1 Case D: row_per_anim layout has no row_index set; frame extraction defaults to row_index=0; may not be idle row. Scale recommendation (1.17×) is unaffected by row_index ambiguity. Non-blocking hygiene item for drax MONSTER_SCALE_BY_SLUG refactor or legolas metadata sweep.

### Case E — Fire_Lord_Creativkind thunder palette-shift (NEW at Path A-prime)

Per Matt-locked decision (`sprite-scale-math-impossibility-rulings-2026-05-16.md` Case 4 § "Operational specifics" + Day-4 close confirmation), god-of-lightning is removed from VS2a active roster and `Fire_Lord_Creativkind` is palette-shifted to thunder palette (fire-orange → thunder-blue/yellow) per `enemy-visual-legibility.md` S2 (element communicated via palette, not via base sprite morphology).

**Intrinsic-size measurement gap:** `Fire_Lord_Creativkind` frame dimensions are not yet PIL-measured (the deferred-pack roster at `reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md` line 75 tagged this as "humanoid fire boss; strong VS2b boss-tier candidate" without intrinsic-size capture). **Action required before drax MONSTER_SCALE_BY_SLUG refactor lands this slug:** legolas or drax inspection of Fire_Lord_Creativkind metadata + content bbox.

**Placeholder recommendation:** scale ~2.0× targeting boss midpoint (370 px), pending measurement. Once measurement returns, scale recalibrates against actual content bbox to land in boss tier (287–460 px). If Fire_Lord intrinsic frame is ~256×256 (matching god-of-lightning's frame footprint) with ~200 px content, scale ~1.85× lands at 370 px — clean upscale at the threshold; aesthetic-intent rationalization applies same as angel-guardian.

**Quality-loss flag:** `upscale_nearest_neighbor_HARD_REQ; INTRINSIC_SIZE_UNMEASURED; palette_shift_required_pre_render`. The palette-shift is a Pixi.js texture-tint operation — drax integration time.

---

## Part 4 — Schema additions for drax MONSTER_SCALE_BY_SLUG refactor (carry forward; criticality strengthened)

The three schema additions from v1 carry forward unchanged in shape. Criticality changes at Path A-prime:

### Schema 1 — `width_or_height_priority` per-slug flag (unchanged)

- **Field:** `width_or_height_priority: "width" | "height"` (default `"height"`)
- **Usage:** per v1; fire-elemental documented as height-priority despite width-dominant geometry
- **VS2a applications at Path A-prime:** none active; all 10 monsters use `"height"` (default)
- **Forward-protection:** future acquisitions where width-priority scaling required

### Schema 2 — nearest-neighbor enforcement (`texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST`) — **CRITICALITY ESCALATED**

- **Field:** enforced at renderer-init time for all monster textures (not per-slug field)
- **Path A-prime change:** v1 marked nearest-neighbor as HARD REQ for angel-guardian only (the lone upscale). At Path A-prime, **five active monsters upscale** (evil-eye 1.62×, fire-elemental 2.29× height-priority, lich 1.67×, hellfire-rhino 2.02×, angel-guardian 2.06×, Fire_Lord_Creativkind ~2.0×) plus three near-native (goblin-mage 1.05×, crystal-golem 1.05×, demon-mage 1.17×). **HARD REQ across the entire monster roster, not per-slug.**
- **Legolas knowledge-gap #5 closure becomes operationally-critical** before MONSTER_SCALE_BY_SLUG refactor ships. Drax should confirm nearest-neighbor active or add it as part of the refactor's scope; the documentation requirement (refactor commit + AGENT_STATE.md call-out) persists.
- **Bilinear-filter failure mode at Path A-prime:** without nearest-neighbor, the entire monster roster renders with bilinear-blur softening at upscale (>1.0×). This is not aesthetic; it is **visible degradation of the HD-2D pixel-art register lock** across the roster. Style-register coherence depends on this enforcement.

### Schema 3 — `tier_coherence_violation` flag per-slug (unchanged)

- **Field:** `tier_coherence_violation: boolean` (default `false`)
- **VS2a applications at Path A-prime:**
  - `fire-elemental: tier_coherence_violation: true, planned_resolution: "vs2b_swap_fire_lord_creativkind_or_elemental_mage"` (carry forward + escalated)
  - `Fire_Lord_Creativkind: tier_coherence_violation: false (pending intrinsic measurement); operational_flag: "intrinsic_size_unmeasured"; palette_shift: "thunder"`
  - All other 8 monsters: `tier_coherence_violation: false`

---

## Part 5 — Viewport pressure analysis (NEW at Path A-prime; load-bearing)

Path A-prime brings sprites to ARPG-genre absolute size. This re-introduces the viewport-pressure concern drax v0.20.4 flagged at the corrected-chierit-composite analysis — a concern that **dissolved** under Path A (because the chierit canvas fit any standard viewport at 1.0×) and **returns** under Path A-prime (because the canvas at 2.5× is 720 × 320 px).

### The chierit canvas at Path A-prime

- Full canvas: 288×128 × 2.5× = **720 × 320 px**
- Figure-content: ~80–140 px wide × ~85–142 px tall (per Group A/B/C variance at 2.5×)
- **Canvas is ~5–9× wider than figure-content.** Most canvas footprint is transparent padding (intentional per chierit author for animation-frame extension — flame trails, cape sweep, attack arcs).

### The pre-existing arena dimensions (drax-shipped per `arena-room-hallway-system.md`)

- Default room: 30m × 48 px/m = **1440 × 1440 px** (square; fits 1920×1080 viewport with margin)
- Small variant: 15m × 15m = **720 × 720 px**
- Large variant: 45m × 45m = **2160 × 2160 px** (camera-follow within bounds; full room not visible at once)
- Hallway width: 6–10m = **288–480 px**

### Viewport pressure at canvas-rendering (current drax render path)

At current drax render path (full 288×128 canvas × scale, transparent padding included):

| Scenario | Canvas footprint | Default room (1440 px) fit | Small room (720 px) fit |
|---|---|---|---|
| Single player (chierit canvas @ 2.5×) | 720 px wide | 50% of room | 100% of room (entire room is one canvas!) |
| Player + boss (boss canvas @ 2.06× = 527 px) | 1247 px combined | 87% of room (tight) | overflows room |
| Player + 4 trash (goblin-mage canvas @ 1.05× = ~100 px each) | 720 + 4×100 + spacing = ~1300 px | 90% of room (tight) | overflows room |
| Player + boss + 4 trash (full-encounter) | 720 + 527 + 400 + spacing = ~1850 px | overflows by 28% | overflows by 157% |

**Canvas-rendering at Path A-prime hits viewport pressure for full-encounter scenarios.** Small room (15m) becomes infeasible for any multi-actor scene; default room (30m) is tight for player+boss+pack encounters.

### Viewport pressure at bbox-tightened rendering (drax v0.20.4 "evaluate" follow-on)

Per drax v0.20.4 notes: *"Recommended design path (for gandalf to evaluate): per-character scale lookup with tighter bounding-box-anchored rendering (render the content bbox region only, not the full 288×128 frame) would allow higher effective scale while keeping the rendered footprint manageable in the viewport."*

At bbox-tightened rendering (figure-content footprint only, transparent canvas padding clipped at render time):

| Scenario | Figure footprint | Default room (1440 px) fit | Small room (720 px) fit |
|---|---|---|---|
| Single player (figure-content ~80–140 px wide) | ~110 px (mid) | 8% of room (comfortable) | 15% of room (comfortable) |
| Player + boss (boss figure ~250 px wide) | ~110 + ~250 + 60 spacing = 420 px | 29% of room | 58% of room |
| Player + 4 trash (figure ~60 px each) | 110 + 4×60 + 5×60 spacing = ~650 px | 45% of room | 90% of room (tight) |
| Player + boss + 4 trash | ~250 + 110 + 4×60 + spacing = ~750 px | 52% of room (comfortable) | 104% of small room (overflows) |

**Bbox-rendering at Path A-prime is comfortable for default 30m room across all scenarios; small 15m room is tight for full-encounter scenes but accommodates player+trash or player+boss pairings.**

### Recommendation — viewport pressure

**No arena re-dimensioning needed.** Drax-shipped 30m default room (1440 × 1440 px) accommodates Path A-prime figure-content footprints comfortably *under bbox-tightened rendering*. Pre-existing arena topology stands.

**Two follow-on engineering items become load-bearing at Path A-prime:**

1. **Bbox-tightened sprite rendering (drax)** — was a v0.20.4 "evaluate" item; **becomes Matt-decision priority at Path A-prime.** Without bbox-tightening, full-canvas rendering hits viewport pressure on default room encounters. With bbox-tightening, viewport pressure dissolves. Recommend knight-rider author a drax dispatch for bbox-rendering implementation, sequenced after MONSTER_SCALE_BY_SLUG refactor lands.
2. **Default-room camera-follow re-validation** — per `arena-room-hallway-system.md` § "Camera/viewport behavior", default 30m room frames player with room bounds visible; camera may pan if player approaches room edge. At Path A-prime, the player canvas at 2.5× occupies more screen real estate; pan thresholds may need re-tuning. Drax/star-lord engineering call after Path A-prime renders are in playtesting.

**Neither item is arena topology re-dimensioning.** The arena topology (room sizes, hallway widths, aggro state machine, door mechanic) stands as Matt-locked. Drax's prior arena work consumed for nothing — it remains the operational topology.

**Forwarded analysis prediction confirmed.** My pre-dispatch prediction was: "Path A-prime is recoverable without arena re-dimensioning (drax already designed for ARPG framing)." This analysis confirms — **the room/hallway topology drax shipped is genre-correct for ARPG single-camera framing**, the chierit canvas footprint is the load-bearing variable (not arena dimensions), and bbox-rendering optimization dissolves the canvas-overhead pressure.

### Edge case — small 15m room at Path A-prime

The 15m room (720 × 720 px) is **tight at Path A-prime even with bbox-rendering** for full-encounter scenarios. Recommendation: per-encounter design discipline at content-authoring time — small rooms reserved for player+boss or player+trash-pack encounters, not full elite+trash compositions. This is encounter-design discipline (knight-rider can route as a content-authoring guideline if needed), not arena re-dimensioning.

### Edge case — large 45m room at Path A-prime

The 45m room (2160 × 2160 px) was already designed for camera-follow within bounds (not full-room visible at once). At Path A-prime this stands — camera-follow accommodates any reasonable Path A-prime encounter composition; full room visibility is intentionally not the design goal at this room size.

---

## Part 6 — Open Matt-decisions surfaced for routing

### Decision 1 — Bbox-tightened sprite rendering authorization (NEW at Path A-prime)

**Question for Matt:** authorize drax bbox-tightened sprite rendering follow-on dispatch?

**Recommendation:** **authorize.** Was v0.20.4 "evaluate" item; becomes operationally-load-bearing at Path A-prime per § Viewport pressure analysis. Without it, Path A-prime hits viewport pressure on default-room full-encounter scenes. With it, viewport pressure dissolves. Knight-rider to sequence after MONSTER_SCALE_BY_SLUG refactor lands.

### Decision 2 — Fire_Lord_Creativkind intrinsic-size measurement (NEW at Path A-prime)

**Question for Matt:** authorize legolas or drax inspection of Fire_Lord_Creativkind metadata + content bbox before MONSTER_SCALE_BY_SLUG refactor lands?

**Recommendation:** **authorize legolas Mode A research (low-cost; single-asset inspection).** Drax can also do this at MONSTER_SCALE_BY_SLUG refactor time if integration timing permits. Either path closes the placeholder scale (~2.0×) into a measured scale. Required before Fire_Lord_Creativkind ships as the thunder boss-tier slot.

### Decision 3 — D14 + D15 discipline authoring (carry forward from v1 + math-impossibility rulings)

**Question for Matt:** authorize gandalf-and-jack-ryan co-authoring of D14 (vendor intrinsic-size pre-acquisition check) and D15 (per-vendor animation-completeness gate) into `reincarnated-engine/design/working-agreement/engineering-disciplines.md`?

**Recommendation:** **authorize.** Carries forward from v1 and math-impossibility rulings. Both disciplines would have caught Fire_Lord_Creativkind's intrinsic-size measurement gap before integration time.

### Decision 4 — Ground Monk anchor-offset priority bump (UPGRADED at Path A-prime)

**Question for Matt:** authorize drax to apply per-character `y_anchor_offset` of +6 px (source pixels) for Ground Monk as part of MONSTER_SCALE_BY_SLUG refactor (not separate dispatch)?

**Recommendation:** **authorize as part of MONSTER_SCALE_BY_SLUG refactor scope.** Was v1 hygiene-priority (6 px visible float at Path A); at Path A-prime becomes 15 px visible float — operationally-visible. Adding to refactor scope avoids a separate dispatch cycle.

### Decision 5 — Sword-warrior transparent-padding bbox confirmation (carry forward from v1; priority unchanged)

**Recommendation:** **hygiene-only**; drax confirms in MONSTER_SCALE_BY_SLUG refactor completion record. No separate inspection dispatch. (Path A-prime change: sword-warrior at 0.33× downscale is less severe than v1's 0.13× — single-line confirmation suffices.)

---

## Cross-references

- knight-rider dispatch `agentic_orchestration/dispatches/2026-05-16-gandalf-per-slug-scale-lookup-path-a-prime-v2.md` — this v2
- v1 `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md` — superseded; preserved as historical record (Path A baseline; v2 supersedes per Matt Day-4 close lock)
- `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` — math-impossibility rulings (still valid; Case 1/2 rationale resurfaces at Path A-prime per Cases A-prime/B-prime above)
- `canonical/story/style-register.md` — HD-2D-pixel register lock; see § "Path A reconciliation" amendment landing concurrently with this v2 doc (ARPG operational target framing added)
- `canonical/story/embodiment-display-loadout.md` § 1.1 — ARPG-anchored pixel-scale framing (gandalf 85ce42f); this v2 doc is the operational complement
- `canonical/story/enemy-visual-legibility.md` § S1–S6 — tier-coded perceptual architecture
- `canonical/story/arena-room-hallway-system.md` — room/hallway topology (load-bearing for viewport-pressure analysis)
- `canonical/story/gandalf-design-lineage.md` Layer 2 — Diablo size-hierarchy lineage; ARPG genre convention
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md` — drax v0.20.4 PIL measurements
- `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md` — drax v0.20.2 monster composite
- `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — legolas Section 3 ARPG-vs-JRPG ground truth + Section 4d semantic implications
- `reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md` — deferred-pack roster; Fire_Lord_Creativkind palette-shift target (line 75)
- `reincarnated-demo/src/visuals/monsterSprites.ts:73` — ENEMY_TIER_CHARACTER_MAP (drax refactor target)

---

## Maintenance protocol

When the drax `MONSTER_SCALE_BY_SLUG` refactor lands with the per-slug scale values from this v2 table:
- This v2 doc remains **rationale-of-record** for each per-slug scale at Path A-prime.
- Drax `MONSTER_SCALE_BY_SLUG` constant becomes operational source-of-truth.
- Any scale change references this doc + math-impossibility rulings; downstream consumers (LLM call signatures, telemetry) consume the constant.

When Fire_Lord_Creativkind intrinsic-size measurement returns:
- Replace placeholder `~2.0×` with measured scale targeting boss midpoint (370 px).
- Recompute against actual content bbox; verify in-band; flag if tier-coherence violation surfaces.

When bbox-tightened sprite rendering ships (drax follow-on dispatch):
- Re-validate viewport-pressure analysis empirically (this doc's bbox-vs-canvas table is calculated; playtest confirms).
- If small-room (15m) full-encounter scenes still feel tight, surface as encounter-design guideline (not arena re-dimensioning).

When VS2b roster expansion happens:
- fire-elemental's planned swap to `Fire_Lord_Creativkind` (or `Elemental_mage`) becomes operational; this table extends.
- Fire_Lord_Creativkind already active at VS2a as thunder boss; the VS2b expansion adds the fire-elite slot replacement.

When future Path A-prime vs alternate-path reopen happens:
- The Path A-prime ratios (Diablo genre-convention) are stable; the baseline (~115 px chierit) is the variable. Recalibration follows the same architecture.

When playtests on VS2a Path A-prime render return signal:
- "Characters feel too big / too small" → first check chierit `CHIERIT_DEFAULT_SCALE` against intended ARPG band; sub-option (i-prime) at 2.5× lands Group B in band; if signal points to sub-option (ii-prime) becoming the answer, the per-character override structure is already in place.
- "Multi-actor encounters feel cluttered" → verify bbox-tightened rendering is active (Decision 1 above); if cluttered persists with bbox-rendering active, encounter-design discipline (Part 5 Edge case — small 15m room) is the answer, not scale revision.

— gandalf, 2026-05-16 (Path A-prime; supersedes v1 Path A; Matt Day-4 close lock)
