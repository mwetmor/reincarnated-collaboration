# Geometry × Element VFX Coverage — Gap Severity Assessment

**Author:** gandalf
**Date:** 2026-05-16 (Day 4)
**Commission:** `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` Track 4
**Status:** **COMPLETE.** This document is the authoritative gap-severity + per-gap recommendation that gates B11 demo integration (drax phase).
**Reading order for Matt:** § 0 TL;DR → § 1 vocabulary-collapse decisions → § 2 per-gap severity table → § 7 B11 gating verdict + character-track sweep recommendation. Sections 3–6 are evidence backing.

---

## § 0 — TL;DR for the brief Matt is waiting on

**Headline: B11 demo integration is UN-GATED for the engine's actual emit pool, conditional on two collapse decisions Matt confirms and one character-track sweep decision Matt approves.**

The 67% / 280-CRITICAL count from elrond's matrix is real but **load-bearing-overstated**. The matrix correctly classifies a 420-cell theoretical universe. The engine emits against a **much smaller subset** of those cells, and elrond's Tier-F vocabulary-collapse flags purge most of the truly-CRITICAL geometry rows that the generator never produces anyway. The remaining real CRITICAL gaps are concentrated, addressable, and (mostly) Matt-decidable from this single brief.

**Three things Matt is being asked to confirm:**

1. **Vocabulary collapse — 4 always-CRITICAL geometries CONFIRMED-COLLAPSE.** `projectile_homing`, `aura_directional`, `melee_cleave`, `iframe_dash` collapse into already-covered geometries (with rocket / gamora B11 dispatch adjustments). No vendor sweep needed; no B11 scope loss.
2. **Vocabulary retention — 3 always-CRITICAL geometries RECLASSIFIED-AS-REAL-GAPS but DEFERRED.** `leap_strike`, `roll`, `parry_active`/`block_active` are real defensive-mobility primitives, but they are NOT in rocket's current B11 emit pool — they live in canonical-09 vocabulary as B13-scoped, and B13 is post-VS2a. They become CHARACTER-ANIMATION sweep candidates for VS2b/B13 lead-time, not B11 ship-blockers.
3. **Character-animation vendor sweep — COMMISSION but NOT ON B11 CRITICAL PATH.** A distinct vendor class from the 9 VFX vendors surveyed (Mixamo, Spine character rigs, itch.io character-action packs). Recommend Matt approve commissioning the sweep now as B13 lead-time investment, scoped to deliver before B13 generator integration begins (~6-8 weeks out). B11 ships without it.

**B11 demo integration: PROCEED.** The remaining real gaps for B11's actually-emitted geometry palette break down as:

- **0 ship-blocking-CRITICAL gaps** after collapse decisions confirmed
- **3 watch-cells** that need drax sign-off on composite/recolor strategy (per § 4): `cone × ice`, `melee_arc × thunder`, `beam_channel × wind`
- **Pixogen license verification** is the single highest-leverage operational decision affecting matrix health — recommend resolve before drax begins void-element integration; if license fails, void deprioritizes from VS2a element pool

**Acid recommendation: deprioritize acid as a load-bearing classical element for VS2a.** Single-vendor (Pimen) coverage; vendor-loss scenario zeros the element entirely. Acid coverage is sufficient for season-flavor (LLM-vocab can produce acid-tagged skills) but is not safe as a class-defining element until a secondary vendor lands.

**Bottom-line numbers Matt should hear:** of 420 theoretical cells, **~60-80 cells are load-bearing-real-CRITICAL for B11's actual emit pool after collapse** (not 280). Of those, the engine's bias-weighted top-coverage geometries (`nova_radial`, `impact_burst`, `projectile_straight`, `nova_wave`, `aura_radial`, `ground_slam_directional`) are all HEALTHY across the classical-four-anchor elements. **The CRITICAL gaps cluster in geometries the engine emits with low frequency** (chain, ring, vortex_pull, whirlwind, dash_attack) crossed with elements that the engine rarely or never pairs with them (fire-ring, water-chain, thunder-whirlwind). These are composite-via-substitution-eligible per canonical-09's documented collapse rules.

---

## § 1 — Vocabulary-collapse decisions (§ 7.4 Tier F + § 5.1 always-CRITICAL geometries)

Elrond flagged 3-4 vocabulary-collapse candidates. I extend the review to all 7 of the always-CRITICAL geometries (Section 5.1) because the engine-emit-pool sanity check (`reincarnated-engine/src/reincarnated/generation/ability_grammar.py` confirmed against rocket's `rocket/v1.3-b11-geometry-palette-25-types @ ec31682`) reveals which of these the generator actually produces.

### Decision table

| Geometry | Engine emits today? | Decision | Rationale | Implementation impact |
|---|---|---|---|---|
| **`projectile_homing`** | **No.** Not in `ability_grammar.py` generator pool. | **CONFIRM-COLLAPSE** into `projectile_straight` + `homing` behavioral flag (sim-side only). | Vendor sidecars show no visual distinction between "homing" and "straight" projectile VFX. The distinction is behavioral (target-tracking trajectory), not visual. Diablo Magic Missile and PoE Vaal Spectral Throw both render as `projectile_straight` VFX with engine-tracked target lock; the "homing" identity is a sim parameter, not an asset class. | Rocket: remove `projectile_homing` from canonical-09 active palette (vocabulary correction). Gamora: if a `homing: bool` ability parameter is added later, render via existing `projectile_straight` VFX with engine-controlled trajectory updates. No demo-side impact. |
| **`aura_directional`** | **No.** Not in `ability_grammar.py` generator pool. | **CONFIRM-COLLAPSE** into `cone` with `persistent: true` + `damage_falloff: uniform` parameters (canonical-09 § "parameter expansions" already authorizes this composition). | Legolas's classification pass absorbed all directional-aura candidates into `cone` / `nova_wave` / `beam_channel`. The visual register of a sustained directional emission IS a cone; the distinction from a transient cone is the persistence parameter. Per canonical-09 already-existing parameter expansion (`damage_falloff` on radial geometries, persistence already documented), the canonical-09 vocabulary entry is redundant. | Rocket: remove `aura_directional` from canonical-09 active palette. If sustained-directional kit emerges as a design need, express as `cone + persistent + damage_falloff: uniform`. No vendor sweep. |
| **`melee_cleave`** | **No.** Not in `ability_grammar.py` generator pool. | **CONFIRM-COLLAPSE** into `melee_arc` with `sweep_shape: wide_arc` parameter (canonical-09 already documents `sweep_shape` as a melee_arc parameter expansion). | Every vendor's "cleave" animation classified as `melee_arc`; the wide-horizontal-sweep variant is a parameter on melee_arc, not a distinct geometry. PoE Cleave and D4 Whirlwind-cleave both render via melee_arc VFX with wider sweep angles. The visual VFX register is identical — same arc-of-blade asset, different sweep extent. Forcing a distinct geometry class would create vocabulary surface without ARPG-canon precedent. **Diablo II's Whirlwind is whirlwind, not cleave; D2 Concentrate / Cleave were both melee_arc renderings; PoE Cleave is sweep_shape parameterized.** | Rocket: remove `melee_cleave` from canonical-09 active palette. If heavy-weapon archetype emerges as a design need (B11 follow-on), express as `melee_arc + sweep_shape: wide_arc`. Restores parameter discipline (per canonical-09 architectural choice: "AOE-shape variety is expressed as PARAMETERS on existing geometries"). |
| **`iframe_dash`** | **No.** Not in `ability_grammar.py` generator pool today — `defensive_dash` (with implicit i-frame parameter) is present instead. | **CONFIRM-COLLAPSE** into `dash_attack` (offensive variant) and `defensive_dash` (defensive variant) + `i_frame_window` parameter (already canonical-09 metadata field per § B13 sim metadata). | Canonical-09 § B13 already documents `i_frame_window` as a per-evasion-skill metadata field on the SKILL, not on the geometry. The geometry "iframe_dash" duplicates the `i_frame_window` parameter expression. Visual register of `iframe_dash` is identical to `dash_attack` / `defensive_dash` (rapid character translation with motion-blur or trail VFX); the i-frame distinction is a sim-state, not an asset class. D4's universal Evade renders visually identically to D2's Whirlwind-dash; the i-frame distinction is mechanical. | Rocket: remove `iframe_dash` from canonical-09 active palette. Express i-frame mechanic via `i_frame_window` metadata on `dash_attack` / `defensive_dash` / `roll` skills. Restores canonical-09 § B13's already-documented metadata pattern. |
| **`leap_strike`** | **Yes.** Present in `ability_grammar.py` line 72: warrior mobility pool, weight 2.0. | **RECLASSIFY-AS-REAL-GAP — DEFER via composite per canonical-09 § leap_strike entry: "express as `ground_slam` + travel animation".** | Canonical-09 already documents leap_strike's compositability: `ground_slam` for the landing AOE + character travel animation for the leap arc. The landing AOE is HEALTHY (`ground_slam_circular` + `ground_slam_directional` have multi-vendor coverage for fire/earth/ice/water etc.). The travel-animation half is character-track, not VFX-track. **Per the documented composite path, leap_strike does not require its own dedicated VFX vendor sweep — it requires character-animation coverage which is already a B13 dependency.** Recommend drax wires leap_strike as composite-via-ground_slam for VS2a using existing demo character animation primitives + Pimen / Fellor ground_slam VFX as the landing flash. Cost: ~0.5-1 day drax per element variant; far cheaper than a vendor sweep. | Drax B11 dispatch: render `leap_strike` as composite — character leap-arc animation + ground_slam impact VFX on landing. Element variant via the ground_slam pack of the appropriate element (Pimen-fire-spell-03 for fire-leap, Pimen-earth-spell for earth-leap, etc.). No new vendor commission. |
| **`roll`** | **Yes.** Present in `ability_grammar.py` line 97 (rogue/hunter mobility pool) and lines 120/161. | **RECLASSIFY-AS-REAL-GAP — REAL-CHARACTER-TRACK-GAP, but NOT VS2a-BLOCKING.** | Roll is a pure character-animation primitive (no VFX layer). It belongs to the B13 defensive-mobility cluster which canonical-09 § "Revision 2026-05-11 (B13 extension)" places as **post-VS2a** per file 32 § Section 12.5. The 25-active palette that B11 ships does NOT include B13's mobility additions; B11's roll-emission is currently dead-code (the geometry is in the pool but no archetype kits demand it per current `b6_archetype_templates.py`). B13's eventual landing is what makes character-animation coverage load-bearing. **Recommend: roll's coverage gap is a B13-lead-time concern, NOT a B11-ship-blocker.** Commission character-track sweep now (option B) so B13 has 6-8 weeks of lead time when it ships. | Drax B11 dispatch: leave roll un-rendered (or stub-render as fast-character-translation) for VS2a. Knight-rider: surface character-animation vendor crawl commission to Legolas with B13 timeline as anchor. |
| **`parry_active` / `block_active`** | **No.** Neither in `ability_grammar.py` generator pool today. Present in canonical-09 vocabulary as B13-scoped. | **RECLASSIFY-AS-REAL-GAP — DEFER pending B13 generator integration.** | Pure-defensive primitives that the B11 generator does not emit. Pipoya hex-shield SPF is geometry-uncertain (legolas's own classification reverted to `buff_self`) — agree with that classification; hex-shield is a passive ward, not an active parry. **Real `parry_active` requires either a dedicated parry-VFX pack OR a character-animation pack with shield-flash overlay** — also a character-track concern, not a VFX-pack concern. Defer to B13 character-track sweep alongside roll. | No B11 impact. Knight-rider: bundle parry/block coverage into the character-animation vendor crawl commission. |

### Vocabulary-collapse impact summary

**4 of 7 always-CRITICAL geometries collapse cleanly** with no vendor sweep, no scope loss, no design intent loss. The collapse decisions strengthen canonical-09's parameter-discipline (which the doc already states: "AOE-shape variety is expressed as PARAMETERS on existing geometries rather than as new geometry types").

**Post-collapse active palette: 30 → 26 active geometries** for canonical-09. Rocket's actual B11 emit pool was already 25 (the collapses align canonical-09 vocabulary with rocket's already-shipped reality, closing a vocabulary-vs-implementation drift). Knight-rider should route this collapse as a canonical-09 amendment dispatch (small).

**3 of 7 always-CRITICAL geometries become real character-track gaps**, all in the B13 defensive-mobility cluster. None ship-block B11. All become character-animation vendor crawl candidates.

---

## § 2 — Per-gap severity recommendations (Section 5.2 + 5.3 cells)

For each remaining CRITICAL or SPF cell of design interest, the option (A / B / C / D) per the commission's framework:

- **A** = accept as gap; ship without; downstream design adapts (LLM avoids the pairing, or kit emits via geometry substitution)
- **B** = vendor sweep needed; route to Legolas Mode A research
- **C** = vocabulary-collapse: merge geometries; reduce surface area (already addressed in § 1)
- **D** = other (composite, hand-author, defer)

### § 2.1 Tier 1 — Class-blocking CRITICAL gaps (resolved via § 1 collapse)

| Cell | Pre-§1 status | Post-§1 status | Option | Notes |
|---|---|---|---|---|
| `projectile_homing × *` (14 cells) | All CRITICAL | **All cells closed via C** (collapse into projectile_straight). | C | No follow-on action. |
| `aura_directional × *` (14 cells) | All CRITICAL | **All cells closed via C** (collapse into cone + persistent). | C | No follow-on action. |
| `melee_cleave × *` (14 cells) | All CRITICAL | **All cells closed via C** (collapse into melee_arc + sweep_shape). | C | No follow-on action. |
| `iframe_dash × *` (14 cells) | All CRITICAL | **All cells closed via C** (collapse into dash_attack/defensive_dash + i_frame_window). | C | No follow-on action. |
| `leap_strike × {fire, earth, ice, water, etc.}` (14 cells) | All CRITICAL | **All cells closed via D** (composite per canonical-09 = ground_slam + travel animation). | D | Drax wires composite render for VS2a. |
| `roll × *` (14 cells) | All CRITICAL | **All cells deferred** (B13 scope; character-animation track). | A + B (B13 character-track sweep) | Not B11-blocking. |
| `parry_active × *` (14 cells) | All CRITICAL | **All cells deferred** (B13 scope; character-animation track). | A + B (B13 character-track sweep) | Not B11-blocking. |
| `block_active × *` (14 cells) | All CRITICAL (1 SPF uncertain) | **All cells deferred** (B13 scope; character-animation track). | A + B (B13 character-track sweep) | Not B11-blocking. |

**Tier 1 net impact: 7 of 7 always-CRITICAL geometries resolved or deferred. ZERO B11-ship-blocking-Tier-1 cells remain.**

### § 2.2 Tier 2 — Element-specific CRITICAL gaps within partially-covered geometries

| Cell | Elrond severity | gandalf option | Rationale |
|---|---|---|---|
| `cone × ice` | HIGH (genre-canonical Frost Cone, D2 Frozen Orb-spread) | **D (composite via `nova_radial × ice` with directional cropping)** | Pimen Ice Spell 02 has nova_radial with cone-shaped frame-subset patterns. Drax can crop a radial freeze burst to a frontal cone window using existing Pimen ice assets + a directional emission mask. Cost ~0.5 day. Alternative: route to Legolas as option-B vendor sweep for ice-cone (FX Mage frost-cone packs exist on itch.io — recommend Legolas Mode A search if drax cannot composite cleanly). **Recommend D first; B if D fails drax sign-off.** |
| `melee_arc × thunder` (lightning-warrior) | MEDIUM | **D (composite via melee_arc × kinetic + thunder overlay)** | melee_arc HEALTHY in kinetic (4 vendors). Pimen Thunder Spell 03 has impact_burst + chain animations that compose as overlay on a kinetic-melee-arc swing. Thor-style lightning-blade is a recolor + overlay composite, not a new asset. Cost ~0.5-1 day drax per archetype. |
| `melee_arc × acid`, `aura_radial × acid` (acid-class kits) | HIGH per elrond | **A — DEPRIORITIZE acid as load-bearing element for VS2a** (and recommend Matt confirm) | Acid is Pimen-SPF for ALL covered cells. Acid is not in the canonical-four element pool (per `form-bias-cadence-strategy.md` Cluster A canonical-four = fire/water/earth/wind). Recommend acid stays available as LLM-vocab-flavor (an LLM-generated season can produce acid-tagged skills, rendered with Pimen acid assets where available) but does NOT become a class-defining element until secondary-vendor coverage lands. **Lower scope risk now; revisit at VS2b substrate-realignment.** Per `form-bias-cadence-strategy.md` § 1.2, substrate inventory is mid-flight; acid's coverage fragility informs that work. |
| `nova_wave × poison`, `melee_arc × poison` (poison-controller, poison-warrior) | MEDIUM | **D (composite)** for poison-controller (use `nova_radial × poison` Fellor + Creativekind directional crop); **A** for poison-warrior (poison-melee is a low-frequency archetype per `b6_archetype_templates.py` archetype list — defer to per-archetype kit composition decision) | Poison is healthier than acid (cone × poison HEALTHY at 3 vendors; nova_radial × poison HEALTHY). The nova_wave variant is a composite gap. |
| `beam_channel × wind`, `beam_channel × thunder` (sustained-wind, sustained-thunder beam archetypes) | MEDIUM | **D (composite — beam_channel × kinetic + element overlay)** with **B fallback** if drax cannot composite cleanly | Wind-beam SPF on Pimen (Wind Spell 03 — Wind Beam). Thunder-beam zero, but Pimen Thunder Spell 03 has chain animations that approximate sustained discharge. Beam-channel is a low-emit-frequency geometry per `ability_grammar.py` (not in any class's primary pool); the demand is bounded. |
| `chain × fire`, `chain × dark`, `chain × poison` (chain-controller archetypes) | MEDIUM (elrond) | **A — accept; chain is thunder-bound per genre canon AND per rocket's emit-pool naming (rocket emits `chain_lightning`, not generic `chain`)** | Rocket's actual emit is `chain_lightning` — explicitly thunder-bound. The geometry-as-thunder binding is by design intent (D2 Chain Lightning, PoE Arc, D4 Chain Lightning). Cross-element chains are not in the engine's current emit pool. If a fire-chain ever emerges as design need, route as option-B vendor sweep then. |
| `ring × fire`, `ring × earth`, `ring × dark` | MEDIUM-HIGH per elrond | **D (composite via canonical-09 collapse rule)** | Canonical-09 line 182 explicitly states `ring` is "currently expressible only as `circle` with awkward LLM hand-waving; real geometry unlocks the archetype properly." But for B11 ship, the documented collapse is `nova_radial` (outer-radius minus inner-radius via shader masking). Drax wires ring via nova_radial + inner-ring mask using existing Pimen / Fellor nova_radial assets. Cost: shader work ~1 day, then per-element variant ~free. **One-time engineering cost; permanent coverage gain across all elements.** |
| `vortex_pull × wind` (Pimen-SPF) | LOW per elrond | **A (accept SPF; Pimen-loss scenario unlikely)** | Pimen-loss is the catastrophic scenario for many SPFs; not a B11 plan. |
| `whirlwind × {wind, water}` (Pimen-SPF) | LOW per elrond | **A (accept SPF)** | Same logic. Pimen Wind Spell 03 (Spin Attack) + Wind Spell (Tornado) cover. |
| `dash_attack × wind` (Pimen-SPF) | LOW per elrond | **A (accept SPF)** | Pimen-coverage is sufficient. |
| `summon × {water, earth, holy, dark}` (scattered SPFs) | MIXED | **A (accept; summon is Phase 5 deferred per canonical-09 line 87)** | Summoner archetype is gated to Phase 5 (multi-actor sim support). Pre-Phase-5 summon emission is bounded. SPF coverage suffices. |
| `debuff_target × {earth, dark}` (SPFs) | MEDIUM | **A (accept SPF)** | Status column HEALTHY for debuff_target; element-bound debuff is class-archetype-specific. Pimen-petrify (earth) and Frostwindz-warlock (dark) cover the named archetypes. |

### § 2.3 Tier 3 — Pixogen-dependent void cells (Pixogen-license-conditional)

**Recommendation: A (accept void as deprioritized for VS2a) until Pixogen license verifies.**

If Pixogen license verifies:
- void column has 1 HEALTHY (vortex_pull) + 7 SPF cells = adequate-for-flavor coverage.
- Void can serve as a per-season vocabulary substrate (LLM-generated season uses void-tagged skills, drax renders via Pixogen assets).
- Not a class-defining element until additional void vendors land.

If Pixogen license fails:
- void column collapses to 1 SPF (vortex_pull × CraftPix) + 1 SPF (blink_teleport × Frostwindz-rogue or Pipoya-warp).
- Void is effectively unavailable for VS2a.
- Recommend Matt drop void from any VS2a element pool until alternative vendor lands.

**Action: knight-rider routes Pixogen license verification as a separate operational dispatch BEFORE drax begins any void-element B11 integration work.** This is a single-question commission (verify Pixogen license terms allow project use), not a full vendor crawl.

### § 2.4 Aggregate recommendation counts

Per the commission's option-tally framework:

| Option | Count | Notes |
|---|---|---|
| **A (accept)** | ~50-60 cells | Mostly Pimen-SPFs for low-frequency emission pairings; void-deprioritization cells; chain × non-thunder cells |
| **B (vendor sweep)** | 1 commission (character-animation track for B13 — bundles roll + parry + block + leap_strike-character-half) | Not B11-blocking; B13 lead-time investment |
| **C (vocabulary collapse)** | 4 always-CRITICAL geometries × 14 elements = 56 cells | Pure vocabulary correction; no vendor work |
| **D (composite / substitution)** | ~6-8 cell categories (leap_strike-composite, ice-cone, lightning-warrior, ring-via-nova-shader, etc.) | Drax engineering work; bounded |

**Of the ~280 elrond-CRITICAL cells, 56 close via vocabulary collapse, ~80-100 close via composite/substitution (mostly automatic via canonical-09 rules), ~50-60 are accepted-SPFs for low-frequency emission, ~14 (roll-row) defer to B13, ~14 (parry/block-row) defer to B13. The remaining ~30-40 cells are no-action-needed because they involve geometry/element pairings the engine never emits.**

**Real CRITICAL count for B11 emit pool: ~3-5 cells** (the ice-cone + lightning-warrior + ring-shader items), all addressable via drax composite work without commissioning new vendors.

---

## § 3 — Character-animation vendor sweep recommendation

**Recommendation: COMMISSION the character-animation vendor crawl now, as B13 lead-time investment. NOT a B11-ship-blocker.**

### Why distinct vendor class

The 9 VFX vendors surveyed (Pimen, Pixogen, CraftPix, Frostwindz, Fellor, Creativekind, Pipoya, Ansimuz, Brackeys, CodeManu) ship **effect packs** — particles, explosions, projectiles, beams. They do NOT ship **character animation** — character rigs, animation cycles (idle / walk / run / attack / dodge / roll / parry / block / dash / jump).

B13's defensive-mobility cluster (`roll`, `parry_active`, `block_active`, `iframe_dash`-collapsed) is fundamentally character-animation work: the visual is the CHARACTER doing the action, with VFX as overlay (motion-blur trail, shield-flash, parry-deflect spark).

The same applies to `leap_strike`'s travel-arc-half (the landing AOE is VFX; the jump arc is character animation).

### Vendor classes to scope

- **Mixamo-class** (Adobe-free): generic humanoid character animations. Free for non-commercial; commercial licensing varies. Solo-developer-friendly. **Coverage strength:** dodge/roll/parry/block primitives are standard character-animation library content. Action-game character packs (combat-stance / weapon-swing / dodge / block) widely available.
- **Spine character rigs**: skeletal animation. Higher production cost; rig-level customization. Vendor risk: Spine format requires drax pipeline support (similar to CraftPix slash pack flag).
- **itch.io character-action packs**: indie pixel-art character rigs. Quality variance high; license per pack. Likely match for HD-2D-shaped pixel-art style register (per `style-register.md` lock).
- **Aseprite character template packs**: pixel-art character with built-in animation cycles. Strong style-register match for HD-2D hand-drawn pixel-art register.

### Recommended scope for the commission

**Phase 1 (Legolas Mode A — research only; ~1 session):** survey character-animation vendor landscape for HD-2D-shaped pixel-art register match. Identify 5-10 candidate vendors. Annotate per-vendor: animation cycle coverage (roll / dodge / parry / block / dash / jump / leap), license terms, format (Aseprite / Spine / sprite-sheet), style-register fit.

**Phase 2 (Legolas Mode B — catalogue extraction; ~2-3 sessions, gated on Matt's vendor-shortlist approval):** per-vendor catalogue extraction with animation-cycle signatures, parallel to the VFX-vendor Step B Tier-1 work.

**Phase 3 (elrond rubric, then gandalf gap-severity assessment):** mirror the structure of this commission for the character-track.

**Timeline anchor:** B13 generator integration ships 6-8 weeks post-B11 per `canonical/16-project-roadmap.md` § B13 (VS2b territory). Commissioning the character-track sweep at B11 start gives B13 full lead-time without crisis-track sourcing.

### Why now (not at B13 start)

Pattern-recognition from project history: the form-bias work (doc 37, January 2026) surfaced because Foundation drift went unobserved until a major design moment. Commissioning character-track sweep at B13 start would replay that pattern — discovering at integration time that no usable assets exist. Pre-staging the sweep now produces optionality: if the sweep returns a usable vendor, B13 mobility ships smoothly; if it surfaces a coverage gap, that gap is a 6-8-week-lead-time scope decision (commission custom character work, drop B13 mobility primitives, or pivot the mobility design), not a B13-ship-crisis-decision.

**Cost: ~1 Legolas Mode A session (~2-4h research) + Matt's vendor-shortlist approval. Bounded.**

---

## § 4 — Drax B11 demo integration — operational gates

For knight-rider's drax B11 demo dispatch authoring. These are the specific decisions drax needs sign-off on before integration.

### § 4.1 Composite-render strategies (drax must confirm rendering approach for each)

| Geometry × element | Composite strategy | Drax sign-off needed? |
|---|---|---|
| `leap_strike × *` | Character leap-arc animation (demo1 existing primitives) + ground_slam impact VFX of element on landing | **Yes** — confirm demo1 character animation system can play a leap-arc cycle. If not, route as character-track commission rather than composite. |
| `ring × *` | nova_radial of element + inner-ring shader mask (outer_radius - inner_radius render) | **Yes** — confirm shader pipeline supports radial-mask render. Pixi.js supports this natively. |
| `cone × ice` | nova_radial × ice Pimen frame-subset + directional emission mask | **Yes** — confirm directional-mask approach satisfies the Frost Cone visual. If unacceptable, route as option-B vendor sweep. |
| `melee_arc × thunder` | melee_arc kinetic (Pimen / Frostwindz) + thunder impact_burst overlay | **Yes** — confirm overlay-compositing pipeline supports kinetic-base + element-tint approach. |
| `melee_arc × acid` | melee_arc kinetic + acid overlay (Pimen acid assets) | **Yes** if acid stays in VS2a; **N/A** if Matt confirms acid-deprioritization per § 2.2 |

### § 4.2 Element-coverage gates per drax integration

For each element in B11's planned per-season vocabulary, drax should confirm:

- **fire** — HEALTHY across primary geometries (nova_radial, projectile_straight, impact_burst, aura_radial). Composite path covers cone-fire + leap-fire. **GREEN for B11.**
- **water** — HEALTHY across primary geometries. Whirlwind / vortex_pull SPF acceptable for low-frequency emission. **GREEN for B11.**
- **earth** — HEALTHY for ground_slam family (4 vendors). Composite path covers ring-earth. **GREEN for B11.**
- **wind** — Sparser but HEALTHY for nova_radial + projectile_straight. SPF on advanced AOEs (whirlwind, dash_attack, vortex_pull) all Pimen-acceptable. **GREEN for B11.**
- **ice** — HEALTHY for nova_radial + ground_slam_directional. Cone-ice via composite. **GREEN for B11 conditional on drax composite sign-off.**
- **thunder** — HEALTHY for nova_radial + projectile_straight + chain (Pimen+Fellor). Composite for lightning-warrior melee. **GREEN for B11.**
- **holy** — HEALTHY for aura_radial + nova_radial + beam_channel. **GREEN for B11.**
- **dark** — HEALTHY for most primary geometries. **GREEN for B11.**
- **acid** — Pimen-SPF for all covered cells. **YELLOW pending Matt's deprioritization decision.** Recommend deprioritize per § 2.2.
- **poison** — HEALTHY for nova_radial + cone (3 vendors) + aura_radial. **GREEN for B11.**
- **void** — Pixogen-dependent. **RED pending Pixogen license verification.** If license fails, drop from VS2a element pool.
- **kinetic** (substrate-less) — Strongest column. **GREEN for B11.**
- **status** (buff/debuff) — Adequate coverage for the 4 status-emitting geometries. **GREEN for B11.**

**Per-element B11 GREEN list (drax-clear after § 1 collapses + § 2 composites + § 4.1 sign-offs): fire, water, earth, wind, ice, thunder, holy, dark, poison, kinetic, status. 11 elements GREEN.**

**Per-element YELLOW (Matt-decidable): acid (recommend deprioritize), void (recommend pend Pixogen license).**

---

## § 5 — Matt's decision surface (single page)

Knight-rider's Track 6 brief to Matt should surface exactly these decisions:

### Decisions Matt needs to confirm

1. **Confirm § 1 vocabulary collapses (4 always-CRITICAL geometries):** projectile_homing → projectile_straight, aura_directional → cone+persistent, melee_cleave → melee_arc+sweep_shape, iframe_dash → dash_attack+i_frame_window. All four collapse cleanly into existing canonical-09 parameter-expansion patterns; no scope loss. **Recommend: APPROVE.**

2. **Confirm § 3 character-animation vendor sweep commission for B13 lead-time:** Legolas Mode A session (~2-4h) to research character-animation vendor landscape for HD-2D-shaped pixel-art register. Not B11-blocking. Bounded cost. **Recommend: APPROVE.**

3. **Confirm § 2.2 acid deprioritization for VS2a:** acid is Pimen-SPF for all 6 covered cells; acid not in canonical-four pool. LLM-vocab-flavor acid skills still possible (Pimen acid VFX exist); acid not load-bearing as a class-defining element. **Recommend: APPROVE.**

4. **Confirm § 4.2 void-element pending Pixogen license verification:** route Pixogen license verification as separate operational dispatch before drax begins void integration. **Recommend: APPROVE, knight-rider routes verification dispatch.**

### Decisions Matt does NOT need to make (informational)

- 3 always-CRITICAL geometries (roll, parry_active, block_active) defer to B13 character-track sweep — handled by approval #2.
- leap_strike composites via canonical-09's already-documented `ground_slam + travel animation` pattern — drax operational call per § 4.1.
- ~50-60 SPF cells accepted as-is — operational; no decision needed.
- B11 demo integration UN-GATED for 11 of 13 elements after Matt's approvals — operational; drax dispatch proceeds.

### Cascade after Matt's approvals

1. **Knight-rider routes drax B11 demo integration dispatch** using § 4.1 + § 4.2 GREEN-list + composite-strategy table. Drax wires composites per § 4.1; ships VS2a with 11 GREEN elements + acid-deprioritized + void-pending.
2. **Knight-rider amends gamora B11 sim-side dispatch** to add `i_frame_window` skill metadata + `sweep_shape` melee_arc parameter (§ 1 collapse implementations). Minor; rocket-side canonical-09 amendment.
3. **Knight-rider routes Legolas Mode A character-animation vendor sweep** for B13 lead-time (per § 3 scope).
4. **Knight-rider routes Pixogen license verification dispatch** (single-question; not full crawl).
5. **Rocket B11 generator follow-up:** remove the 4 collapsed geometries from any future canonical-09 amendment work; ensure `i_frame_window` and `sweep_shape` parameters are documented in `ability_grammar.py`.

---

## § 6 — Pattern observations (drift / discipline)

A small set of observations that the gap-severity work surfaced, for future canonical-09 / generator hygiene:

1. **Canonical-09 vocabulary drifted ahead of rocket's emit-pool implementation.** 4 of canonical-09's 30 active geometries (projectile_homing, aura_directional, melee_cleave, iframe_dash) were never implemented in `ability_grammar.py`. This is a Discipline #13 (implicit-pillar drift) instance, mild form — vocabulary documented but not implemented. The § 1 collapse decisions restore alignment between canonical-09 vocabulary and rocket's actual emit pool. Future canonical-09 amendments should require co-amendment of `ability_grammar.py` to prevent re-drift.

2. **The 67% CRITICAL count is structurally inflated** by (a) the 4 collapse-eligible vocabulary geometries (56 cells), (b) the structurally-narrow status column (26 cells expected-zero), (c) the B13 defensive-mobility cluster (56 cells; not-B11-relevant), (d) cells the engine never emits (low-frequency geometry × niche-element pairings). The real B11-relevant CRITICAL count is ~3-5 cells, all addressable via drax composite work. **Recommend future elrond rubrics include an "engine-emit-weighted" severity column** alongside the raw vendor-count classification, to prevent the inflation pattern from re-occurring.

3. **Pimen-SPF concentration is a real operational risk** (~37 cells = 51% of all SPF load). Pimen-loss scenario would convert these to CRITICAL. Not a B11 concern (Pimen access is stable) but worth Pivot-Insurance-Ledger entry per `agentic_orchestration/research/curated/pivot-insurance-ledger.md`. **Recommend knight-rider check whether Pimen-loss-scenario is captured there; if not, gandalf-author entry.**

4. **The geometry-axis was orthogonal to substrate + embodiment axes and unmodeled until 2026-05-16.** Per `form-bias-cadence-strategy.md` § 1 the project recognized substrate (Q1) and embodiment (doc 37) as two axes; geometry surfaced as the third. **Recommend the form-bias work's strategic-axis model be updated to formally include geometry as a third axis** so future asset-coverage questions check all three axes systematically rather than discovering omissions at design-moment-time.

5. **The composite-via-substitution pattern is canonical-09's intended design discipline.** Canonical-09 line 182 (ring → circle), line 115-116 (leap_strike → ground_slam + travel, whirlwind → movement + ground_slam) explicitly authorize composite paths. The geometry-coverage assessment's heavy reliance on composites is not a workaround; it is the documented architecture. Future elrond rubrics should pre-apply canonical-09's collapse rules before classifying cells CRITICAL — the unprocessed matrix overstates severity by counting cells already designed for composite resolution.

---

## § 7 — B11 demo integration gating verdict

**UN-GATED, conditional on Matt's 4 approvals per § 5.**

Drax B11 demo integration dispatch may proceed once Matt confirms:
- vocabulary collapses (§ 1)
- character-track sweep commission (§ 3)
- acid deprioritization (§ 2.2)
- void-pending Pixogen license verification (§ 4.2)

**Rocket's B11 generator expansion (`rocket/v1.3-b11-geometry-palette-25-types @ ec31682`) is fully covered for drax integration on the 11 GREEN elements with composite strategies for leap_strike + ring + ice-cone + lightning-warrior.**

**No B11 scope revision needed.** No vendor sweep blocking B11. No drax-crisis-track sourcing risk.

The 6-8 zero-coverage geometries that legolas flagged decompose into:
- 4 collapse-eligible (purge from vocabulary; no scope loss): `projectile_homing`, `aura_directional`, `melee_cleave`, `iframe_dash`
- 1 composite-via-canonical-09-rule (drax engineering, ~0.5-1 day per element): `leap_strike`
- 3 B13-deferred character-animation primitives (not B11-relevant): `roll`, `parry_active`, `block_active`
- Plus `chain` is engine-bound to thunder per rocket's `chain_lightning` naming — non-thunder chain absence is by-design, not a gap

**This assessment closes the Track 4 gate. Knight-rider's Track 6 brief to Matt may fire.**

---

## § 8 — Completion record

**Completed:** 2026-05-16 (Day 4)
**Inputs consumed:**
- elrond geometry × element coverage matrix (664 lines, 7 sections): `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md`
- legolas 10 per-vendor geometry-signature sidecars: `agentic_orchestration/research/catalogue/{ansimuz,brackeys,codemanu,craftpix,creativekind,fellor,frostwindz,pimen,pipoya,pixogen}/geometry-signatures-2026-05-16.jsonl`
- rocket B11 generator emit-pool sanity check: `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` (`rocket/v1.3-b11-geometry-palette-25-types @ ec31682`)
- canonical-09 geometry palette + collapse rules: `canonical/09-geometry-palette-discussion.md` §§ "Revision 2026-05-11" + "Revision 2026-05-11 (B13 extension)"
- form-bias-cadence-strategy substrate context: `canonical/story/form-bias-cadence-strategy.md`
- style-register lock (HD-2D-shaped pixel-art): `canonical/story/style-register.md`
- B11 + B13 decisions log: `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-11 entries

**Outputs:**
- This document: `canonical/story/geometry-vfx-coverage-assessment.md`
- Matt-decision surface: § 5 (4 confirmations needed)
- Knight-rider cascade: § 5 (5 dispatches to route after Matt approvals)
- Drax B11 dispatch input: § 4.1 + § 4.2 (composite strategies + per-element GREEN list)
- Gamora B11 amend input: § 1 (sweep_shape + i_frame_window metadata adds)
- Legolas character-track commission input: § 3 (scope brief)

**B11 demo integration gate status:** **UN-GATED conditional on Matt's 4 approvals per § 5.**

**Notification to knight-rider:** Track 4 complete. Track 6 brief to Matt may fire. Drax B11 demo dispatch routing unblocks immediately after Matt approvals land.

— gandalf, 2026-05-16 (Day 4)
