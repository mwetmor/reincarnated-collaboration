# Stage 3 Design Call + Engine Architecture Discussion — State Capture 2026-05-24

> **STATUS:** Session-end state capture — preserves D1-D7 decision chain + engine architecture (A/B/C) discussion across Matt's step-away. Next-session pickup: read this doc + `canonical/story/v1-bc-target-intent-2026-05-24.md` § 1 + Cycle 10 dispatch + this state-capture's "Next-action queue" § 7.

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — session-end state capture; preserves two parallel discussion threads
**Authority:** Matt 2026-05-24 — direct instruction at session-end to capture both threads
**Companion docs:**
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription — substrate for D1-D7 decisions)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 dispatch)
- `canonical/story/skill-system-2026-05-24.md` (consumed for Architecture A vs B + Option β decisions)
- `canonical/story/off-hand-items-2026-05-24.md` (consumed for D1 + Architecture amendments)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (engine architecture canonical source-of-truth — has TWO architectural surfaces requiring amendment per this session)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute lock)
- `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md` (knight-rider state file; Cycle 10 status)

---

## 0. TL;DR

**STATE-CAPTURE UPDATED 2026-05-24 evening — Stage 3 design call FULLY CLOSED + Architecture B LOCKED + composition policy landed.**

**Stage 3 Design Call (D1-D7 decision chain) — FULLY CLOSED:**
- D1 LOCKED with Main/Secondary semantic + accessory/armor subdivisions (commit `8446854`)
- D2 LOCKED via smoke-test validation + Option β + Option C cross-attribute permission (commit `8446854`)
- D3 LOCKED (Option A — 4-tuple substrate routing; proxy-density at form-generation per algorithm § 8.6)
- D4 LOCKED (D4a — Stage 4 mythological-NULL rescue)
- D5 LOCKED (all 4 Sketch F anchors → Stage 3.5 gap-fills per Matt amendment)
- D6 LOCKED (composition policy synthesis structure validated)
- D7 LOCKED (Stage 3.5 budget ~25-50 entries; per-entry discipline)
- **Composition policy canonical doc landed at `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`**

**Engine Architecture (A/B/C discussion) — Architecture B LOCKED as production canonical:**
- ✅ Substrate-AGNOSTIC Phase 2 alignment correction landed (commit `8446854`)
- ✅ Role-shape constraint removed (per Pattern 6 retirement)
- ✅ **Architecture B LOCKED as production canonical via Matt 2026-05-24 reversal** (commit `d761fa5`)
- ✅ Substrate-genre-flagging unified-architecture (per Matt refinement; serves all commercial profiles)
- ✅ Architecture A retained as developer-tool / R&D reference (archived to historical/)
- ✅ Empirical-trigger discipline § 4 of new canonical doc

**Both threads CLOSED. Next-session pickup: Stage 3 execution dispatch routing (knight-rider) → Wave 5 execution → Cycle 10 wind-down → post-Cycle-10 canonical authoring queue (Phase 4/5 amendments + loot architecture + element canonical-pair flavor + naming-space partitioning).**

---

## 1. Thread 1 — Stage 3 Design Call (D1-D7 decision chain)

Stage 3 design call locks the **composition policy** for Cycle 10 substrate-curation — what enters v1_scope and at what tier-protection. Output target: canonical doc `canonical/story/weapon-substrate-composition-policy-v1-2026-05-XX.md` consumed by Stage 3 execution (elrond constrained-sampling).

### 1.1 D1 — Tier-S Weapon-Kind Gate — ✅ LOCKED (with refinements)

**Final lock:**

| Gate | Rule | Approximate rows |
|---|---|---|
| **D1a Main weapon auto-promote** | `category = 'handheld_weapon'` | **449** |
| **D1b Secondary auto-promote** (Main/Secondary semantic per Matt 2026-05-24) | (i) `category = 'armor' AND subtype = 'armor_shield'` ~30-50 + (ii) `category = 'accessory' AND subtype = 'accessory_handheld'` ~40-60 (powder flasks/horns + banners + focuses/talismans) + (iii) `category = 'accessory' AND subtype = 'accessory_weapon_integrated'` ~30-50 (tsuba/menuki/grips/magazines/scopes/pommels) | **~100-160** |
| **D1c Excluded** | (i) `category IN ('siege_vehicle', 'art_object', 'other', 'ammo_consumable')` 422 + (ii) `subtype IN ('accessory_horse_or_equipment', 'armor_body_or_head')` ~105-145 — horse-furniture (spurs/shaffrons/bits) excluded per Matt scope-creep discipline; body-armor deferred to v1.1+ when armor-slot system scoped | **~525-565** |

**Total Tier-S auto-promote: ~550-610 rows out of 1,126 Tier-S (~49-54%).**

**Implementation requirement (post-Stage-3 wind-down):**
- Elrond second-pass classifier on 130 accessory + 125 armor rows for subtype subdivision (~30 min)
- Substrate-fit lookup for weapon-integrated-accessory → parent-weapon-kind compatibility (gandalf; ~30 min)
- Off-hand-items canonical doc rename "Off-hand" → "Main/Secondary" semantics (already locked in companion-ref; full doc amendment post-Cycle-10)

### 1.2 D2 — Thin-Cell Action Queue — ✅ LOCKED (via smoke-test validation + Option β + Option C cross-attribute permission)

**Per-cell action locks:**

| Cell | Archetype | Action |
|---|---|---|
| 13 | Artillery Mage `(ranged, low, spiky, INT)` | **FOLD into Cell 12 Standard Wizard via T4 algorithmic alteration** — Cataclysm-tier T4 manifests as Artillery variant per element-canonical-pair flavor (paired "cataclysmic") |
| 14 | Pyromantic Caster `(mid, low, spiky, INT)` | **Stage 3.5 engine-author gap-fill (~5-10 entries)** — contested cell; engine-authored Pan-Fantasy slot |
| 15 | Red Mage/Spellsword `(melee, high, flat, INT)` | **Phase 5 cohesion-judge composes over STR-melee substrate + INT-flavored kit** — no separate gap-fill needed (Option C + Option β) |
| 17 | Necromancer Summoner `(mid, low, spiky, INT, heavy)` | **Sidecar B fantasy-coinage Necro enrichment + algorithm § 8.6 proxy-spawn** |
| 19 | Channeling Cleric `(mid, medium, variable, WIS)` | **Sidecar B WIS-broad enrichment** (Option β downgrades from rescue to optimization) |
| 21 | Ritual Mage/Oracle `(ranged, low, spiky, WIS)` | **ACCEPT low floor** (51 typed; close to 60 floor; single form) |
| 22 | Storm Caller/Druid `(ranged, medium, variable, WIS)` | **Sidecar B Celtic/Druidic enrichment** |
| 23 | Monk-archetype `(melee, high, variable, WIS)` | **Sidecar B East-Asian fist-and-staff + Stage 4 mistagged-rescue** (quarterstaff cross-attribute via Option C) |
| 24 | Druid Beastmaster `(mid, low, variable, WIS, heavy)` | **Sidecar B Celtic/Pacific enrichment** + algorithm proxy-spawn |
| 25 | Witch Doctor Petmaster `(mid, medium, variable, WIS, heavy)` | **Sidecar B Sub-Saharan-African enrichment** + algorithm proxy-spawn (African caster substrate empirically 0; load-bearing for cultural-tradition coverage) |
| 2 | Light Fighter `(melee, high, flat, STR)` | **ACCEPT 0.45-conf pool** + flag for Stage 4 mechanical-tagging priority |
| 9 | Twin-Blade Fencer `(mid, high, flat, DEX)` | **ACCEPT Pan-Fantasy** — per Sketch D § 5.3 |

**Sidecar B scope expansion CONFIRMED: ~1 day legolas Mode B work + worst-case hand-author fallback (Matt earlier: "we can write them ourselves as a fall-back; less desirable").**

**Smoke-test validation:** Matt requested hand-authored examples per thin 4-tuple; I produced 8 4-tuple examples (Cells 13, 14+17, 15, 19+25, 22, 23, 24, 21); ALL viable; no cells mechanically broken.

**Option α / β / C lock (locked as part of D2 architecture):**
- **Option α — Martial cells (STR/DEX primary, physical-element):** weapon-slot requires 5-tuple mechanical-fingerprint match (weapon-attack IS combat delivery)
- **Option β — Caster cells (INT/WIS primary, non-physical-element):** weapon-slot requires ATTRIBUTE-LEVEL match only (skills deliver kit BC-target; weapon scales)
- **Option C — Cross-attribute hybrid (Red Mage / Monk / Holy Knight):** weapon-slot permits cross-attribute wielding with ω-penalty per BDI ω-field resource-dimension (0.0 cross vs 1.0 same-attribute)

### 1.3 D3 — 5-tuple → 3-tuple Cell-Collapse — ✅ LOCKED (Option A)

**Lock:** Substrate routes at 4-tuple level (range × tempo × amplitude × attribute); proxy-density discriminates at form-generation time via algorithm § 8.6 (faction-generated proxies). Each cell-pair shares substrate pool.

**The 5 routing-ambiguous cell pairs:**

| # | Cell A (proxy=none) | Cell B (proxy=light/heavy) | Shared 4-tuple |
|---|---|---|---|
| 1 | Cell 1 Heavy Barbarian | Cell 5 Ancestor-Warrior (light) | `(melee, low, spiky, STR)` |
| 2 | Cell 7 Archer | Cell 10 Falconer (light) | `(ranged, high, flat, DEX)` |
| 3 | Cell 12 Standard Wizard | Cell 16 Arcane-Familiar Mage (light) | `(ranged, medium, variable, INT)` |
| 4 | Cell 14 Pyromantic Caster | Cell 17 Necromancer Summoner (heavy) | `(mid, low, spiky, INT)` |
| 5 | Cell 19 Channeling Cleric | Cell 25 Witch Doctor Petmaster (heavy) | `(mid, medium, variable, WIS)` |

Cohesion-judge at Phase 5 uses cultural-tradition substrate signal to bias form-assignment within shared cell-pair pool. Thin-cell resolution applies to shared pool.

### 1.4 D4 — 30 Mythological-Register NULL-Typed Rows — ⏸️ PROPOSED (D4a) awaiting Matt confirmation

**Proposed lock D4a:** Stage 4 accurate-tag rescue of 30 mythological-register NULL-typed rows; per-row mechanical-tagging at Stage 4 with Discipline #18 legolas Mode A consult + jack-ryan Gate-2; rescued rows enter v1_scope at legendary-tier per Architecture B.

**Rationale:**
- These are HIGH-VALUE (mythological register = Tier-S candidates for Layer-4 legendary loot pool per Architecture B)
- Stage 4 mechanical-tagging at higher rigor (LLM-judge for ambiguous; cultural canon grounding for named items)
- Composes with existing Stage 4 work (~no marginal cost)
- Complementary to D2 (D4 = legendary-tier coverage; D2 = common-through-rare tier coverage for thin cells)

**Matt action needed:** Confirm D4a (or amend).

### 1.5 D5 — 4 Zero-Substrate Sketch F Anchors — ⏸️ PENDING

**Per Stage 1.5 results, 4 Sketch F anchors returned 0 substrate matches:**
- Hattori Hanzō (Tier 2 Japanese real-historical)
- Lu Bu (Tier 2 Chinese real-historical)
- Moctezuma (Tier 2 Mesoamerican real-historical — per Matt's Custer/Moctezuma vision)
- Gilgamesh (Tier 1 Sumerian broadly-fictionalized)

**Three options surfaced:**
- (a) Track M1 future enrichment crawls them in
- (b) Stage 3.5 engine-authored gap-fills
- (c) Drop from Sketch F roster (~12 → ~8)

**Important context per Matt 2026-05-24 universal-archetypal-naming lock:** these are ENGINE-INTERNAL substrate-anchors only — player NEVER sees explicit names. The decision is whether engine-internal substrate-anchor remains for these 4 forms or is dropped. Dropping doesn't lose player-facing content; it loses engine-side design-discipline grounding.

**My earlier preview lean (pre-Stage-3-design-call thinking — not committing):**
- Hattori Hanzō: Stage 3.5 engine-authored gap-fill (East Asian Tier-2 representation matters)
- Lu Bu: Drop OR Track M1 deferral (Chinese Three Kingdoms representation lower-priority for v1)
- Moctezuma: Stage 3.5 engine-authored gap-fill (Matt's vision is load-bearing; cultural-sensitivity discipline + Quetzalcoatl nested-mythology pattern)
- Gilgamesh: Track M1 future enrichment (single iconic anchor worth crawling for)

**Matt action needed:** Per-anchor disposition.

### 1.6 D6 — Composition Policy Lock Synthesis — ⏸️ PENDING

Synthesizes D1+D2+D3+D4+D5 + this-session-locks into composition policy canonical doc. Outputs:
- Target weights per axis (register × period × lineage × mechanical-cell × Tier protection rules)
- v1_scope membership rules
- Constrained-sampling parameters for elrond execution
- Per-form-archetype substrate-coverage targets

Composes:
- Sketch D distribution (substrate-led skew accepted; Pan-Fantasy 20% hefty)
- Architecture B (substrate as base-type templates + tiered instance loot)
- Option α / β / C cell-type matching policies
- Element canonical-pair flavor + named-bearer attribution discipline
- Universal archetypal naming + naming-space partitioning

Becomes canonical doc consumed by Stage 3 execution.

**Matt action needed at D6:** Validate synthesis; lock policy doc; trigger elrond Stage 3 execution.

### 1.7 D7 — Engine-Authored Gap-Fill Quantity Budget — ⏸️ PENDING

**Stage 3.5 scope locks:**
- Total budget (~5-50 entries?)
- Per-cell allocation (Cell 14 Pyromantic confirmed; potentially Cell 15 Red Mage; potentially Cells 17/22/24/25 if Sidecar B doesn't recover)
- Cultural-tradition discipline (gap-fills curated per D7 AI-tell discipline)
- Provenance flag (`source_library='engine_authored_gap_fill_v1'`)
- Research-replacement notes per Stage 3.6 for v1.1+ web-research substitution

**Matt action needed at D7:** Lock budget + per-cell allocation policy.

---

## 2. Thread 2 — Engine Architecture (A/B/C discussion)

### 2.1 The two architectures discussed

**Architecture A — Substrate-AGNOSTIC Phase 2 (current canonical end-to-end-workflow doc):**
```
Phase 2: Compose SUBSTRATE-BLIND mechanical kit (skills + weapon-SLOT mechanical profile + traits)
Phase 3: Sim runs against abstract weapon-slot; measure 8-axis BC coordinates
Phase 4: Pareto/crowding gate on mechanical signature only
Phase 5: LLM cohesion-judge SELECTS specific substrate weapon + assigns cultural-tradition + element-flavor + naming
```

**Architecture B — Substrate-driven Phase 2 (my earlier ULTRA-think diagram — WRONG):**
```
Phase 2: Compose mechanical kit + PULL specific substrate weapon from v1_scope matching cell's mechanical needs
Phase 3: Sim runs with actual substrate weapon's mechanical signature
Phase 4: Pareto gate on kit-and-substrate as unit
Phase 5: Cohesion-judge CONFIRMS identity-narrative coherence + names
```

### 2.2 Architecture A — Verdict: CORRECT (architectural ULTRA-think landed)

Architecture A is the right engine flow for Reincarnated. Reasons:

| Pro of Architecture A | Why it matters for Reincarnated |
|---|---|
| Variant C composition | Engine must be general; substrate-AGNOSTIC Phase 2 lets engine serve multiple substrate libraries (Reincarnated weapons; future sci-fi Profile B; future commercial profiles) |
| Substrate enrichment composes cleanly | Sidecar B / Track M1 / v1.1+ new substrate ATTACHES at Phase 5 to existing archived kits via cohesion-judge re-run — no Phase 2-4 re-fire |
| Mechanical-design space exploration unconstrained | Engine can explore mechanical kits that have NO substrate support yet — surfaces enrichment needs without breaking |
| Substrate-led discipline preserved | Substrate VOTES at Phase 5 cohesion-coalescence; doesn't DICTATE at Phase 2 |
| Pareto optimization is mechanically pure | Phase 4 archive insertion optimizes mechanical-novelty + diversity without substrate-coverage confounding |
| Element canonical-pair flavor + universal archetypal naming compose | Phase 5 LLM-runtime handles flavor + naming with ALL signals available |
| Replay variety per season | Same mechanical kit re-flavored across seasons |

### 2.3 First fix landed — substrate-AGNOSTIC Phase 2 alignment ✅

**Inconsistency Matt caught:** My skill-system § 13 step 7 said "Select weapon from substrate matching kit's mechanical needs" — implied substrate-pulled-at-Phase-2. Inconsistent with canonical end-to-end-workflow Phase 2 (which is substrate-AGNOSTIC).

**Fix landed (commit `8446854`):**
- skill-system § 13 amended: Phase 2 generation flow rewritten to be SUBSTRATE-AGNOSTIC; step 7 changed from "Select weapon from substrate" to "DEFINE WEAPON-SLOT MECHANICAL PROFILE per cell" with Option α/β/C sub-discipline; Phase 5 substrate-attachment workflow added explicitly
- off-hand-items companion-ref amended: Phase 2 DEFINES off-hand SLOT mechanical profile substrate-blind; Phase 5 cohesion-coalescence selects specific substrate-resident off-hand item

**Source of truth confirmed:** `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` was correct; my downstream docs had error.

### 2.4 Second flaw Matt caught — role-shape constraint ⏸️ PENDING amendment

**The flaw:** Canonical end-to-end-workflow Phase 2 box has:

```
│  Action: compose mechanical kit (skills + gear + traits) targeting BC   │
│          ┌─ substrate-AGNOSTIC mechanic pool                            │
│          ├─ role-shape constraints (damage/control/support/hybrid)      │  ← FLAW
│          └─ BC-target as composition objective                          │
```

`role-shape constraints (damage/control/support/hybrid)` is **pre-imposed categorical taxonomy** — exactly the kind of thing Pattern 6 retirement (`canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`) addressed.

**Why it's a flaw:**
- Pattern 6 RETIRED 2026-05-22 (pre-imposed axes replaced by discovered axes from substrate)
- Substrate-led discipline says roles EMERGE from BC-axes, don't get pre-imposed
- BC-axes already capture role implicitly:
  - Axis 2A (proxy density) → summoner/proxy
  - Axis 2B (control density) → control
  - Axis 4 (defensive profile) → tank/support
  - Mixed signatures → hybrid
- Pre-imposing 4-role taxonomy on top is REDUNDANT + introduces categorical bias

**My ULTRA-think earlier had this RIGHT** (no role-shape constraints) even though wrong on substrate-pulled-at-Phase-2. The TRUE correct architecture combines:
- ✅ Substrate-AGNOSTIC Phase 2 (from canonical doc)
- ✅ NO pre-imposed role-shape constraints (from my ULTRA-think + Pattern 6 retirement + substrate-led discipline)
- ✅ BC-target as composition objective
- ✅ ω-field + τ-field + algorithm § 8 as mechanical-coherence constraints
- ✅ Substrate-coalescence at Phase 5

**Amendment proposed for canonical end-to-end-workflow Phase 2 box:**

```
BEFORE:
│  Action: compose mechanical kit (skills + gear + traits) targeting BC   │
│          ┌─ substrate-AGNOSTIC mechanic pool                            │
│          ├─ role-shape constraints (damage/control/support/hybrid)      │
│          └─ BC-target as composition objective                          │

AFTER:
│  Action: compose mechanical kit (skills + gear + traits) targeting BC   │
│          ┌─ substrate-AGNOSTIC mechanic pool                            │
│          ├─ BC-target as composition objective                          │
│          ├─ ω-field + τ-field mechanical-coherence constraints          │
│          └─ algorithm § 8 mechanic-alteration (if T4 cell)              │
│                                                                          │
│  NO pre-imposed role-shape constraints (per Pattern 6 retirement +     │
│  substrate-led discipline). Role-shapes EMERGE from BC-coordinates     │
│  post-generation; they are descriptive measurements not generation     │
│  constraints.                                                           │
```

Plus add amendment header to canonical doc noting Pattern-6-alignment correction.

**Estimated effort:** ~20-30 min amendment + commit.

**Matt action needed:** Confirm amendment; I execute.

### 2.5 Broader canonical end-to-end-workflow amendment (queued post-Stage-3)

The canonical doc was authored 2026-05-21. This session has locked substantial architectural enhancements that aren't reflected. Beyond the role-shape removal (§ 2.4 above), the doc needs amendment to incorporate:

| Enhancement | Where it slots in end-to-end-workflow |
|---|---|
| Architecture B substrate-as-base-type-templates + tiered-instance-loot | Phase 5 cohesion-coalescence selects from tiered loot pool; potential new Phase 6 for loot-drop mechanics |
| Universal archetypal player-facing naming | Phase 5 LLM cohesion-judge applies universal archetypal-naming discipline |
| Bi-modal form library (engine-layer discipline) | Phase 5 cohesion-judge handles named-personage vs engine-named-original assignment |
| Element canonical-pair flavor at LLM-runtime | Phase 5 LLM cohesion-judge maps core element to per-form flavor manifestation |
| Legendary canonical-pair set-bonuses | Phase 6 (or Phase 5 sub-step): loot-drop mechanics; canonical-pair recognition at equip-time |
| Option α (martial 5-tuple) / Option β (caster attribute-level) / Option C (cross-attribute ω-penalty) | Phase 5 substrate-attachment per cell-type matching policy |
| Faction-generated proxies algorithm | Phase 2 algorithm § 8 output extension; proxy-spawn-template per kit's substrate-derived faction-anchor (attaches at Phase 5) |
| Nested mythology naming pattern | Phase 5 per-tier naming discipline at proxy-named-entity level |
| Spirit-guide explainer pattern | Phase 5 templated LLM call for algorithmic mechanic-alteration explainer |
| Naming-space partitioning per engine-anchor | Phase 5 cohesion-judge constraint at archetypal-naming layer |

**Estimated effort:** ~2-3 hours post-Stage-3 closure canonical authoring.

**Queued for post-Stage-3 closure** (doesn't block Stage 3 design call completion).

---

## 3. Locked architectural commitments this session (broader context)

For state-completeness, full list of architectural locks from this entire session:

1. **4-attribute system** (STR/INT/WIS/DEX; DEX added; VIT deferred to v1.1+)
2. **5-tuple BC-target subspace** (range × tempo × amplitude × attribute × proxy-density = 324 cells)
3. **10-15 node skill tree** (small-tree; D3-class-skill scale)
4. **Mechanic-altering passives only** (NO filler stat-bonuses)
5. **Algorithmic mechanic-alteration as architectural advance** (skill-system § 8; per kit's BC-axis space)
6. **8 core elements** (physical / fire / water / earth / wind / lightning / holy / shadow)
7. **Architecture B substrate-as-base-type-templates + tiered-instance-loot** (Layer 1 base types + Layer 2 common + Layer 3 magic/rare + Layer 4 legendary)
8. **Universal archetypal player-facing naming** (engine-internal named-personage attribution; player layer uniform archetypal)
9. **Bi-modal form library as engine-layer discipline** (~32% named-personage / ~68% engine-named-original at engine layer; player experience uniform)
10. **Element canonical-pair flavor at LLM-runtime** (core element stable; per-form paired-element-flavor manifestation at Phase 5 cohesion-judge)
11. **Legendary canonical-pair set-bonuses** (Excalibur + Avalon scabbard pattern; player-choice equip-both triggers set-bonus regime-change)
12. **Option α (martial 5-tuple) / Option β (caster attribute-level) / Option C (cross-attribute ω-penalty)** per cell-type matching policy at Phase 5 substrate-attachment
13. **Caster kit definition** (primary_attribute INT/WIS + skills primary damage source + skills deal non-physical element + weapon scales)
14. **Faction-generated proxies algorithm extension** (skill-system § 8.6)
15. **Nested mythology naming pattern** (skill-system § 12.4; Tier-2 invokes Tier-1 per Moctezuma-summons-Quetzalcoatl)
16. **Spirit-guide explainer pattern** (skill-system § 9; converts cognitive-load risk into story win)
17. **Naming-space partitioning per engine-anchor** (cohesion-judge respects per-anchor reserved patterns)
18. **substrate-AGNOSTIC Phase 2 + substrate-coalesces Phase 5** alignment correction (commit `8446854`)

**Pending architectural locks (this thread):**
- Role-shape constraint removal from canonical end-to-end-workflow Phase 2 (§ 2.4 above) — awaiting Matt confirm
- Canonical end-to-end-workflow doc full amendment incorporating items 7-17 above (~2-3 hours post-Stage-3)

---

## 4. Cycle 10 status (as of this state-capture)

| Stream | Status |
|---|---|
| Wave 1 + Wave 2 | ✅ CLOSED (commit `23db403`) |
| Wave 3 (Stage 2 + Stage 2.5 + pre-Stage-3 classifier) | ✅ EXECUTION COMPLETE in working tree; awaiting Matt commit/tag authorization (Option II two-tags `elrond/v0.0-cycle-10-stage-2-cross-tab` + `elrond/v0.0-cycle-10-stage-2-5-quality-tier-scoring`) |
| Stage 3 design call | 🔥 IN-FLIGHT — D1/D2/D3 LOCKED; D4 proposed; D5/D6/D7 pending |
| Wave 4 (Stage 3 execution) | Gated on Stage 3 design call completion |
| Wave 5 (Stages 3.5 + 4) | Gated on Wave 4 |
| Sidecar A (Meshy comparison) | ✅ Verdict landed (MIXED per knight-rider commit `23db403`) |
| Sidecar B (off-hand items + thin-tradition + WIS-broad enrichment) | Pending; ~1-2 days legolas Mode B + ~1 day cultural-tradition substrate work |

---

## 5. Pending canonical writes (post-Stage-3 closure)

Per this session's architectural locks, the following canonical writes queue up for post-Stage-3 / post-Cycle-10 work:

1. **Composition policy canonical doc** (post-D6 synthesis) — `canonical/story/weapon-substrate-composition-policy-v1-2026-05-XX.md`
2. **Loot architecture canonical doc** (per Implication 1 of Architecture B discussion) — `canonical/story/loot-architecture-v1-2026-05-XX.md`
3. **Element canonical-pair flavor architecture canonical doc** (per Matt 2026-05-24 element-flavor lock) — `canonical/story/element-canonical-pair-flavor-architecture-2026-05-XX.md`
4. **Naming-space partitioning canonical doc** (per per-engine-anchor reserved-naming patterns) — `canonical/story/naming-space-partitioning-2026-05-XX.md`
5. **End-to-end-workflow doc amendment** (incorporating all this session's enhancements per § 2.5) — amend in place + commit
6. **Off-hand items doc full Main/Secondary rename** — amend in place + commit
7. **Skill-system § 12.3 amendment** (clarifying tier-discipline-lives-at-engine-layer + universal-archetypal-player-facing-naming) — amend in place + commit
8. **Pall deletion** — engine data files; routes via knight-rider for rocket/elrond surgical delete

**Estimated total post-Stage-3 canonical authoring: ~6-8 hours gandalf foreground.** Folds into Cycle 10 wind-down.

---

## 6. Pending knight-rider routing requests

1. **Wave 3 commit/tag authorization** — Matt-decision territory; Option II two-tags
2. **Stage 3 design call closure → Stage 3 execution dispatch** — knight-rider authors execution dispatch once D6 locks
3. **Sidecar B substrate-enrichment scope expansion** (+5 thin-cell-enrichment targets per D2) — knight-rider amends Sidecar B dispatch
4. **Algorithm § 8 implementation dispatch** (post-Cycle-10; rocket seam; Discipline #18 legolas Mode A consult first) — per `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md`
5. **Loadout app readiness scoping** (drax + star-lord coordination for T4-B post-mortem) — same dispatch
6. **Pall deletion** — surgical delete of pall entries in `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` + `vfx_coverage_manifest.json` — small dispatch

---

## 7. Next-action queue (for Matt return)

**Immediate decisions awaiting Matt:**

| Priority | Action | Decision needed |
|---|---|---|
| 1 | Wave 3 commit/tag authorization | Option II two-tags (or amend) |
| 2 | Role-shape constraint removal amendment to canonical end-to-end-workflow (§ 2.4) | Confirm amendment + I execute |
| 3 | D4 confirmation | Lock D4a (Stage 4 mythological-NULL rescue) or amend |
| 4 | D5 — 4 zero-substrate Sketch F anchors | Per-anchor disposition (Track M1 / Stage 3.5 / drop) |
| 5 | D6 — Composition policy lock synthesis | Validate synthesis; lock policy doc |
| 6 | D7 — Engine-authored gap-fill quantity budget | Lock budget + per-cell allocation |

**Once Stage 3 design call completes (D1-D7 all locked):**
- Stage 3 execution dispatch authored by knight-rider → fires elrond constrained-sampling
- Wave 5 fires per dispatch § 4.1
- Cycle 10 wind-down sequence
- Post-Stage-3 canonical authoring queue (§ 5)

**Next Matt-required touchpoint after Stage 3 closure** (per prior session estimate): T4-B post-mortem session 1 ~3-5 weeks from now post-engine-form-generation. Window of low Matt-involvement between Stage 3 closure and T4-B post-mortem.

---

## 8. Continuity instructions for next-session pickup

**Read order:**
1. This state-capture doc first (current state of both threads)
2. `canonical/story/v1-bc-target-intent-2026-05-24.md` § 1 (Stage 0 cell roster reference for D2/D3/D5)
3. Cycle 10 dispatch (`agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md`) for execution context
4. `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` for engine architecture canonical reference (with pending role-shape amendment noted in § 2.4 of this state-capture)
5. `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md` for knight-rider state

**To resume Stage 3 design call:** Pick up at D4 confirmation (or D5 if D4 already confirmed). § 1.4-1.7 of this state-capture has the decision-shape for each.

**To resume Engine Architecture discussion:** § 2.4 (role-shape removal amendment) is the immediate pending item. § 2.5 (broader canonical end-to-end-workflow amendment) is post-Stage-3 work.

**Discipline reminders:**
- Workstream-relative framing only (per Discipline #22)
- No sleep recommendations (per Discipline #21)
- Framing-audit (Q1/Q2/Q3) when authoring new architectural diagrams against existing canon (lesson from this session — I propagated an error in skill-system § 13 + ULTRA-think diagram without auditing against canonical doc)

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — direct instruction at session-end to capture both threads
**Status:** ACTIVE — session-end state capture; preserves D1-D7 decision chain + engine architecture (A/B/C) discussion across Matt's step-away
**For:** clean next-session pickup of two parallel discussion threads without loss of context or progress

---

**Signed:** gandalf
