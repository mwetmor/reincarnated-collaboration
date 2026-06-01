# WS1A.Q18 Wave-Close Deferred Commitments

**STATUS:** CURRENT (deferred-commitments record; surfaced at PG-3 ratification + folded into wave-close sub-phase 5e)
**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-01 ratification ("Feel free to draft them. I think that we manually wrote the caster substrate mostly and so we may need to manually author modern variants.")
**Wave:** WS1A.Q18 flavor-pool research-and-lock wave (PG-3 RATIFIED 2026-06-01)
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-synthesis.md` (Phase 5a synthesis)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (wave operational sequence)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 + § 1.8 (WS1A.3/.4 architecture; multi-axis experiential framework)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; substrate measurement coordinate)
- `canonical/00-ground-state.md` § 1 (current truth; weapon substrate Cycle 8 hive-mind lineage)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing 156-entry pool; Q18 lock extension target)

---

## 0. TL;DR

Two deferred-commitments surfaced during Pattern B PG-3 ratification dialogue 2026-06-01. Both compose with WS1A.Q18 wave-close without blocking it; both require deferred work post-wave-close.

| # | Item | Trigger | Owner | Composes with |
|---|---|---|---|---|
| 1 | **WS1A.3 theme-coherence gating** | Q18 lock added 19 modern-caster overlay entries across 7 rotating primaries; WS1A.3 sub-element selection needs theme-axis gating to prevent thematically-incoherent kit compositions (e.g., "Medieval Tesla Knight") | gandalf design + star-lord / rocket implementation | Q16 / Q17 wave scope; hypothesis-flow § 1.8 multi-axis experiential architecture |
| 2 | **Modern-caster substrate-coverage gap** | Modern-caster flavor pool implies modern-caster kit identity; weapon substrate may not back it; caster substrate was historically manually-authored (NOT legolas-crawled) per Matt 2026-06-01 context | gandalf manual authoring + elrond schema/ingest | Existing manually-authored caster substrate lineage; WS1A.3 implementation prerequisite |

Both items captured here as recognition records with explicit empirical-evidence triggers for re-engagement per Discipline #41 substrate-led recognition → validate → commit pattern.

---

## 1. Deferred Item 1 — WS1A.3 theme-coherence gating

### 1.1 The recognition

The WS1A.Q18 lock added **19 modern-scientific overlay entries** distributed across 7 rotating primaries:

| Primary | Modern-caster overlay entries |
|---|---|
| fire | fusion, thermal, combustion (3) |
| water | hydro, hydraulic (2) |
| earth | seismic, tectonic (2) |
| wind | sonic, shockwave (2) |
| lightning | flash, ion, voltage, tesla (4 — plus plasma which is substrate-validated) |
| holy | photon, laser, prismatic (3) |
| shadow | blackhole, singularity, darkmatter (3 — plus soul which is mystical-fantasy overlay) |

These entries carry **thematic asymmetry within their primary's allow-list** — a lightning kit's flavor pool now contains both pre-industrial vocabulary (arc, spark, thunder, bolt) AND modern-scientific vocabulary (tesla, voltage, ion, flash, plasma).

**The structural risk:** WS1A.3 (per-kit sub-element selection) is not yet specified in detail. Without explicit theme-coherence gating, WS1A.3 could pick `tesla` as sub-element for a medieval-period / pre-industrial-cultural-tradition lightning kit, producing identity-incoherent compositions ("Medieval Tesla Knight").

The risk lives at WS1A.3 sub-element selection, NOT WS1A.4 per-skill judgment. WS1A.4 judgment is bounded to whatever WS1A.3 already picked; the upstream selection is where gating must apply.

### 1.2 Why this surfaced at PG-3 (not earlier in the wave)

The modern-caster pattern emerged during PG-3 Pattern B dialogue (post-Phase-5a synthesis). The synthesis draft proposed conservative modern-caster representation (2-3 entries in holy + shadow); Matt's amendments extended modern-caster across all 7 rotating primaries with substantive cardinality (~19 entries total). This wave-scale design move was not in the synthesis-draft scope; therefore the downstream gating concern was not surfaced during Phase 5a.

This is a clean example of the **synthesis-draft Pattern B critique discipline** in action — the critique-pair surfaced both the design opportunity (modern-caster across all primaries) AND the downstream concern (theme-coherence gating) that the synthesis-author alone would not have surfaced.

### 1.3 Five mitigation options

| Option | Mechanism | Cost | Discipline |
|---|---|---|---|
| **G1 — Theme-axis substrate gate** | Kits declare `theme_register` ∈ {medieval / classical / mythological / modern / sci-fi / ...} at substrate-generation; WS1A.3 filters sub-elements by theme-register match | Schema extension at substrate level; substrate-curation pass | Hard filter; substrate-led discipline applied to theme axis |
| **G2 — Lineage-tag filter** | WS1A.3 filters by pool.json `substrate_validation_lineage` field: `designer-curation-modern-scientific-overlay-*` entries fire only for kits flagged as modern-themed via cultural-tradition + period + register triad | Uses existing pool.json fields (post-Q18 schema amendment); clean composition | Hard filter; lineage-transparent |
| **G3 — LLM prompt context-gating** | WS1A.3 LLM prompt provides kit's full identity context (cultural-tradition + period + register + canonical-archetype + form); LLM does coherent selection within the bounded set | No schema change; LLM-judgment-dependent (variance risk) | Soft gate; LLM reasoning-bound |
| **G4 — Probability-weighted selection** | Modern-caster overlay entries have low default probability mass; boosted only when modern theme-flag fires; statistical drift permitted | Probabilistic gating; permits occasional non-thematic drift | Statistical; not hard filter |
| **G5 — Cell-level theme declaration** | Pattern library cells (per hypothesis-flow architecture § 1.8) declare theme; sub-element selection is cell-scoped per theme | Composes with cell-shape framework; pattern library Phase-A work | Architectural; cell-scoped |

### 1.4 Gandalf design-lean — G2 + G3 composition

**G2 (lineage-tag filter) + G3 (LLM prompt context-gating)** composed:

- G2 provides **hard-filter discipline** at the structural layer: modern-caster overlay entries are mechanically excluded from non-modern-themed kits via lineage-tag enforcement
- G3 provides **soft coherence at the judgment layer** within the filtered set: even if both medieval-canonical AND classical-canonical entries are eligible for a kit, the LLM picks coherently per cultural-tradition + register

Both compose naturally with existing pool.json schema (post-Q18 amendments for `substrate_validation_lineage` + `vocabulary_commonness` + `slot_unambiguous`). No additional schema extension required.

**G1 (substrate-level theme-axis) is a heavier alternative** that may compose better with the multi-axis experiential architecture (hypothesis-flow § 1.8) — if `theme_register` becomes a substrate-declared cell-shape axis, G1 becomes the architecturally-cleanest path. Decision deferred to Q16/Q17 wave scope.

**G4 and G5 are NOT recommended** — G4 (statistical) permits identity-incoherent drift; G5 (cell-level) couples to pattern library Phase A which is Cycle 15+ scope.

### 1.5 Empirical-evidence trigger for re-engagement

**Architectural commitment deferred pending:**

- WS1A.3 implementation design surface fires (Q16 or Q17 wave scope) — at which point the gating mechanism becomes load-bearing
- Theme-axis substrate-extension scope decision (does `theme_register` join the substrate-declared cell-shape axes, or stay as derived per cultural-tradition+period+register triad?)
- Manifestation milestone playtest evidence on identity-coherence (if playtest surfaces "Medieval Tesla Knight"-style identity collisions, gating becomes higher priority)

**Specific empirical signals that would re-engage:**

1. WS1A.3 design-call dispatch authored (commits to filter-vs-LLM-vs-cell architecture)
2. Substrate-coverage audit (Item 2 below) returns evidence on theme-distribution of weapon population
3. First manifestation-milestone kit generation surfaces identity-coherence concerns
4. Q16/Q17 hard-blocker wave includes theme-coherence gating as Pattern B surface

### 1.6 Owner + composition

**Owner:** gandalf design-side (Pattern B surface) + star-lord / rocket implementation-side (WS1A.3 logic).

**Composition:**

- With `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.8 multi-axis experiential architecture — theme-axis discussion belongs here naturally
- With pool.json schema amendments at sub-phase 5f (`substrate_validation_lineage` field is the G2 mechanism)
- With existing substrate-library cultural-tradition + period + register fields (used as G3 context-gating inputs)
- With Q16 WS1A.4 LLM prompt design (WS1A.4 inherits WS1A.3 gating decisions)
- With Q17 hybrid pair selection (hybrid kits have 2 primaries; gating composition is multiplicative)

**Does NOT compose with:**

- WS1A.Q18 wave-close (this gating is downstream-of-vocabulary-lock)
- Existing engine architecture canon (engine doesn't need amendment; gating is at generation-time)

---

## 2. Deferred Item 2 — Modern-caster substrate-coverage gap (manual-authoring path)

### 2.1 The recognition

The WS1A.Q18 lock established modern-caster kit identity vocabulary (~19 entries across 7 rotating primaries). For these kit identities to be realizable in generation:

1. Skills with appropriate geometry + tempo + amplitude (engine-side; not weapon-dependent)
2. **Weapons that read as modern-caster** (substrate-side; possibly thin)
3. Cultural-tradition + period + register substrate that backs modern theming

**Item 2 (weapon substrate) is where the coverage gap likely lives.**

### 2.2 Matt's context — caster substrate is manually-authored (NOT legolas-crawled)

Per Matt 2026-06-01 verbatim:

> "I think that we manually wrote the caster substrate mostly and so we may need to manually author modern variants."

This is critical operational context that changes the deferred-work shape:

- **Caster substrate** (staves / wands / tomes / orbs / focuses / etc.) was **manually authored** by Matt/gandalf, NOT extracted via legolas Mode B catalogue crawl
- **Modern-caster weapon variants** would follow the same operational pattern — manual authoring, NOT crawl extraction
- This is **distinct from the 89,839-row weapon substrate hive-mind cycle** (Cycle 8 2026-05-22) which was largely catalogue-crawled for martial/historical/military weapons

The implication: substrate-expansion for modern-caster is a **gandalf-side authoring work-stream**, not an elrond Mode B crawl dispatch. Elrond handles schema + ingest of the manually-authored entries.

### 2.3 Substrate-coverage state — UNKNOWN; audit OR direct-authoring path

The 89,839-row weapon substrate likely has:

| Weapon category | Substrate coverage estimate |
|---|---|
| **Mythological/historical real weapons** (swords, axes, bows, polearms) | Deep (crawled + manually authored) |
| **Modern military hardware** (firearms, rifles, mortars, artillery) | Moderate (crawled; surfaced in marginal-lineage records — S. American military firearms; Arctic Circumpolar 2S1 SPH / RBS-70 / Mistral 3 / ENVOY UAV / AW50; etc.) |
| **Fantasy/ARPG canonical staves/wands** | Moderate (manually authored caster substrate) |
| **JRPG/isekai canonical weapons** | Moderate (some crawl + manual authoring) |
| **Sci-fi caster weapons** (Tesla Coil, energy pistol, plasma rifle, coilgun, railgun, particle beam, prism array) | **THIN-to-ABSENT** |
| **Modern-tech caster implements** (laser device, focusing crystal array, sonic emitter, EMP generator, lab equipment as weapons) | **VERY THIN** |
| **Cyberpunk-style modern casters** (neural interface, augmented gauntlet, energy gloves) | **THIN** |

The substrate has likely deep coverage of CONVENTIONAL caster weapons (medieval-coded) and CONVENTIONAL modern weapons (firearm-coded) but **thin coverage of modern-CASTER weapons** (sci-fi-coded caster implements).

### 2.4 Two operational paths

**Path A — Substrate-coverage audit first, then manual authoring.**

Elrond Mode A dispatch queries the substrate for modern-caster-eligible weapons:

```
Elrond substrate-coverage audit — modern-caster weapon population

Query the 89,839-row substrate for weapons that back modern-caster
kit identity per primary. Surface per-primary count + cluster
coverage + representative reps.

Lightning modern-caster query targets:
  - Tesla Coil / coilgun / railgun / energy-pistol-class
  - Electromagnetic-pulse generator
  - Modern-electrical implements

Fire modern-caster query targets:
  - Thermal Lance / fusion-weapon / modern flamethrower
  - Incendiary devices (thermite charge, napalm)
  - Heat-emission tech

Holy modern-caster query targets:
  - Laser device / prism array / focusing implement
  - Radiant-emitter tech (concentrated light)
  - Optical-physics weaponry

Shadow modern-caster query targets:
  - Singularity-generator / void-weapon / antimatter-cannon
  - Sci-fi cosmic-horror implements

Wind modern-caster query targets:
  - Sonic Emitter / pressure-cannon / acoustic-device
  - Shockwave-generator / supersonic weapon

Water modern-caster query targets:
  - Cryo-weapon / hydro-pressure device
  - Fluid-dynamic implement (cavitation weapon)

Earth modern-caster query targets:
  - Seismic-device / tectonic-shaper
  - Kinetic-impact weapon (mass driver)

Report per-primary count + representative reps + cluster IDs +
gap-identification (which categories have ZERO substrate coverage).
```

Audit informs whether manual authoring is needed AND at what scope per primary.

**Path B — Direct manual authoring (skip audit; author for full coverage).**

Per Matt's context, caster substrate is manually-authored; modern variants would follow same pattern. Skip elrond audit; gandalf authors ~5-15 modern-caster weapons per primary directly (~50-100 total).

**Hybrid Path A+B (gandalf recommendation):**

- **Phase 1 (post-Q18 wave-close):** elrond audit fires — quick discovery query (~0.5 session); surfaces actual coverage state
- **Phase 2 (post-audit):** gandalf authors gap-fill weapons per primary; targets primaries with audit-confirmed thin coverage
- **Phase 3:** elrond ingests gandalf-authored entries; schema + lineage tags applied
- **Phase 4:** substrate-coverage validation pass — confirms modern-caster kit identity is now backed

Estimated horizon: ~3-5 sessions total (1 audit + 1-2 gandalf authoring + 1 elrond ingest + 1 validation).

### 2.5 Per-primary modern-caster weapon authoring scope (proposed)

If Path A+B fires, the manual-authoring work-stream targets:

| Primary | Weapon archetypes to author | Count estimate |
|---|---|---|
| lightning | Tesla coil staff / coilgun pistol / railgun rifle / electromagnetic-pulse gauntlet / energy-pistol / arc-projector / volt-baton | 5-10 |
| fire | Thermal lance / fusion-cell focus / modern flamethrower-class / incendiary projector / heat-emission torch / plasma-cutter staff | 5-10 |
| holy | Laser device / prism focusing array / radiant emitter staff / light-amplification gauntlet / optical-focus orb / photonic projector | 5-10 |
| shadow | Singularity generator / void-projector / antimatter focus / cosmic-horror implement / dark-energy emitter / null-field gauntlet | 5-10 |
| wind | Sonic emitter / pressure-cannon / acoustic-projector staff / shockwave gauntlet / supersonic device / aerodynamic focus | 5-10 |
| water | Cryo-projector / hydro-pressure device / cryogenic gauntlet / fluid-dynamic focus / cavitation-emitter | 5-10 |
| earth | Seismic-device / tectonic-shaper staff / kinetic-impact gauntlet / mass-driver / pressure-focus | 5-10 |

Total scope: ~35-70 weapons authored. Each requires substrate fields per existing weapon schema (cultural_tradition + period + register + form + scoring per Tier-S/A/B/C gates).

### 2.6 Empirical-evidence trigger for re-engagement

**Architectural commitment deferred pending:**

- WS1A.Q18 wave-close (PG-4 PASS) — this item fires as sibling-of-sub-phase-5f operational work
- Path decision (A vs B vs A+B) — gandalf + Matt design call post-wave-close
- Elrond Mode A audit dispatch (if Path A or A+B fires)
- Manual-authoring session(s) for gandalf gap-fill weapons
- Elrond Mode B ingest + schema + lineage application

**Specific empirical signals:**

1. Wave-close PG-4 PASS lands → this item activates as deferred-work
2. Elrond audit query returns → coverage state empirically known
3. Gandalf authoring sessions complete → gap-fill weapons exist in substrate
4. WS1A.3 implementation fires → modern-caster kit identity is realizable in generation
5. First manifestation-milestone modern-caster kit successfully generates with backing weapon substrate

### 2.7 Owner + composition

**Owner:** gandalf (manual authoring; per Matt 2026-06-01 verbatim "we may need to manually author modern variants") + elrond (schema / ingest / lineage tagging).

**Composition:**

- With existing manually-authored caster substrate (same operational pattern)
- With `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` BC axes — modern-caster weapons score per existing 8-axis substrate measurement coordinate
- With `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — Option β caster-attribute-magical composition; modern-caster weapons follow Option β caster pattern
- With `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` post-Q18-amendment schema — `substrate_validation_lineage` field tags modern-caster weapons per their lineage
- With Item 1 above — substrate-coverage informs gating-mechanism design (thin coverage may justify lighter gating since modern-caster representation is intentionally bounded)

**Does NOT compose with:**

- Legolas Mode B catalogue crawl (manual authoring is the path; not crawl extraction per Matt 2026-06-01)
- WS1A.Q18 wave-close (this is sibling-of-sub-phase-5f operational work; not wave-close blocking)
- 89,839-row weapon substrate hive-mind (Cycle 8) — manually-authored modern-caster weapons compose alongside but follow different lineage

---

## 3. Composition with wave-close (sub-phase 5e)

These two deferred-commitments items compose into the WS1A.Q18 wave-close recognition record at sub-phase 5e per operational sequence § 2:

1. **KR wave-close record** at `canonical/story/2026-06-XX-ws1a-q18-flavor-pool-wave-close-record.md` integrates these items in its "Deferred Commitments" section, referencing this artifact
2. **Gandalf design-quality audit** per OP § 4.6 includes A1-A5 verification on the canonical write + cites this artifact in the audit's "Forward Notes" section
3. **00-ground-state.md § 1 update** adds the canonical lock entry + cross-references this deferred-commitments artifact

**KR routing post-wave-close** can author dispatches for Items 1 + 2:

- **Item 1 routing:** queue as Q16/Q17 hard-blocker wave Pattern B surface; no immediate dispatch needed
- **Item 2 routing:** elrond audit dispatch (~0.25-0.5 session) + gandalf manual-authoring session(s) (~2-3 sessions) + elrond ingest dispatch (~0.5 session); all fire post-wave-close as sibling-of-sub-phase-5f operational work

---

## 4. Sign-off

**Authored:** gandalf (story-and-design steward) 2026-06-01 during PG-3 Pattern B with Matt
**Authority:** Matt 2026-06-01 ratification ("Feel free to draft them. I think that we manually wrote the caster substrate mostly and so we may need to manually author modern variants.")
**Status:** CURRENT (deferred-commitments record; integrates into WS1A.Q18 wave-close recognition at sub-phase 5e)

**Recognition-validate-commit discipline (Disc #41):** both items are RECOGNITIONS at this artifact; VALIDATION fires per the empirical-evidence triggers (§ 1.5 + § 2.6); COMMITMENT fires when validation lands. Neither item is pre-committed at architectural-lock; both honor the recognition → validate → commit pattern at the right temporal layer.

**Composition with prior canon:**

- Composes with Cycle 8 hive-mind weapon substrate (preserves; doesn't amend)
- Composes with manually-authored caster substrate lineage (preserves operational pattern)
- Composes with hypothesis-flow architecture § 1.8 multi-axis experiential framework (theme-axis discussion)
- Composes with WS1A.Q18 canonical lock (sibling-deferred; not wave-close blocking)

**End of deferred-commitments record.**
