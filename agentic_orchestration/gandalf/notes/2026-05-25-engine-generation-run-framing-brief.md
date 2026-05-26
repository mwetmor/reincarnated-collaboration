# Engine Generation Run Framing Brief — v1 narrow milestone first-use of new engine

> **STATUS:** RATIFIED 2026-05-25 — Matt direction "Should we draft the engine generation for the loadout and special case summaries?" + gandalf affirmative recommendation
> **For:** KR dispatch routing (rocket OR star-lord OR coordinated); gandalf post-generation special case summary work
> **Authority:** Matt 2026-05-25 + Cycle 12 closure (v1.0-new-engine-ready tag at engine commit `7cff770` + loadout `c06bed1`)

**Author:** gandalf (story-and-design steward)
**Purpose:** define scope + coverage + quality criteria for the FIRST USE of the new engine (post-Cycle-12) to produce ~30-40 forms for T4 post-mortem readiness milestone evaluation.

---

## 0. TL;DR

Fire single engine generation run dispatch producing ~30-40 forms via the new BC-target subspace generator (Layer 2) + skill content (Layer 3) + W1.13 multi-dim convergence (Layer 4) + § 8 wire-up with L9 opportunity-scan refactor (Layer 6). Forms upload to loadout app via star-lord export pipeline. Gandalf performs post-generation design-fit pass producing special case summary for Matt + gandalf T4 post-mortem session 1.

**This is the engine v1 narrow milestone Matt has been driving toward.**

---

## 1. Generation run scope

### 1.1 Form count + coverage

| Dimension | Target | Notes |
|---|---|---|
| **Total forms** | ~30-40 | per Matt P2c + T4-B reframe + Cycle 12 wind-down expectation |
| **BC-target cell coverage** | All 25 cells represented OR explicitly accept coverage gap | Per L2 implementation: 25 cells in CELL_DEFINITIONS (25 vs 22 reconciled per gandalf comp-policy verdict § 1.1) |
| **6 v1 § 8 strategies all represented** | At least 2-3 forms per strategy where cell-eligibility allows | RESOURCE_CONVERSION + TRADE_OFF + ELEMENT_CONVERSION + DEFENSIVE_CONVERSION + GEOMETRY_COLLAPSE + 6th strategy (Defensive-tradeoff / Chaos Inoculation) |
| **Provenance mix** | Substrate-pulled main; substrate-pulled off-hand (per Sidecar B); engine-authored gap-fills (per Stage 3.5); mythological-NULL rescue (per Stage 4) | All 4 source_library types should be present |
| **Named-personage anchor forms** | 4 Sketch F anchors expected: Hattori Hanzō + Lu Bu + Moctezuma + Gilgamesh | Per composition policy v1 § 5.2; engine-internal named_bearer field populated |
| **Element coverage** | All 8 core elements represented (physical/fire/water/earth/wind/lightning/holy/shadow) | Wind + lightning critically thin per Cycle 12 elrond pre-Layer-2 prep (8 + 5 rows); expect thin-cell-fallback to fire |
| **Attribute coverage** | All 4 attributes represented (STR/INT/WIS/DEX) | Caster cells (INT/WIS) thin per per-cell substrate distribution; expect Option β attribute-level matching |

### 1.2 Quality criteria

Per Cycle 12 close + Tier 2 ratification path:

- **Algorithm § 8 keystones actually shift fight behavior** (Option γ payoff per gamora cross-seam integration; not Tier 2 intent-metadata-only)
- **All forms have full schema population** per `PlayerClassV2` interface contract (framing brief § 4 LOCKED)
- **Sim-viability flag PASS** per § 8.4 sim-viability check (rocket + jack-ryan Gate-2 already validated layer-wise; full-engine Gate-2 PASS confirmed at Cycle 12 close)
- **engine_version = "v2.0"** on all forms (provenance flag per WARN-A INFO-4 amendment landed)
- **mechanical_substrate_triple populated** per L9 (mechanical only; cultural_tradition/lineage/period as semantic overlay on weapon record)
- **Substrate-binding integrity** — main_weapon's mechanical fields match kit BC-target cell within thin-cell-fallback tolerance per composition policy v1 § 4

### 1.3 Phase coverage during generation

Per QD-engine 8-phase workflow + Cycle 12 Layer mapping:

| Phase | Status during generation run |
|---|---|
| Phase 1 — Archive Inspection | ✅ EXISTS in legacy + v1_scope substrate (2,293 items queryable) |
| Phase 2 — BC-Target Generation | ✅ NEW ENGINE Layer 2 + Layer 3 |
| Phase 3 — Convergence / Measurement | ✅ NEW ENGINE Layer 4 (W1.13 custom multi-dim per math note v1.1 § 4.3) |
| Phase 4 — Insertion | ✅ EXISTS in legacy (verify minor amendment if needed during generation) |
| Phase 5 — Cohesion Coalescence | ⚠️ EXISTS in legacy; calibration spec PENDING (Phase 5 cohesion-judge calibration QUEUED for gandalf canonical authoring; not blocking generation; names + sub-element flavoring will produce but may not be optimally calibrated) |
| Phase 6 — Visual Coalescence | ⚠️ EXISTS-PARTIAL (Sidecar A image-pass-through verdict from Cycle 10; production wire-up not done; expect placeholder visuals OR no visuals at v1 narrow) |
| Phase 7 — Joint-Gate | ⚠️ STATUS UNCLEAR (may exist implicitly via existing acceptance criteria; possible amendment surface) |
| Phase 8 — Profile Assembly | ✅ EXISTS in legacy + Layer 6 wire-up adds T4 alteration application |

### 1.4 What forms will + will NOT have

**Forms WILL have:**
- BC-target cell identity + element + energy + attribute + range/tempo/amplitude
- Main weapon (substrate-bound from v1_scope per L11 strict 4-tuple match with thin-cell-fallback)
- Off-hand item (per SC-3 mechanical contract; if applicable per cell)
- Skill tree (10-15 nodes; 2-4 chains; 3-4 tiers; T4 slots populated; ~3-5 T4 candidates per chain)
- T4 keystone alteration (§ 8 algorithm selected; Layer 6 wire-up means alterations REACH combat arithmetic)
- Multi-dim converged modifier (Layer 4)
- Stat allocation + attribute coupling labels
- mechanical_substrate_triple (per L9)
- engine_version = "v2.0" + source_library provenance
- t4_alteration_output struct (per § 8) — drax + star-lord + gamora consumers all live-supported
- spirit_guide_narration_metadata (drax LIVE-supported per star-lord auto-detect in Wave 5)
- LLM-generated form names (Phase 5; possibly not optimally calibrated — flag at post-mortem)
- LLM-generated skill names + descriptions (Phase 5; same caveat)

**Forms will NOT have (deferred):**
- Generated visuals (Meshy production wire-up partial; placeholders likely)
- Factions (deferred per § 3.4)
- Per-fight combat statistics (Layer 7 BDI test framework deferred v1.1)
- Geospatial fight telemetry (fine-grained spatial; v1.1+ multi-seam work)

---

## 2. Special case summary requirements

Post-generation, gandalf performs design-fit pass producing a special case summary at `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md`. Structure:

### 2.1 Per-form notes (sampling)

NOT exhaustive (~30-40 forms × deep notes would be excessive). Sample by category:

- **All Sketch F anchor forms** (Hattori Hanzō + Lu Bu + Moctezuma + Gilgamesh): full notes — these are the named-personage anchors and warrant individual evaluation
- **One representative form per § 8 strategy** (6 forms): full notes — verify each strategy fires as designed
- **All engine-authored gap-fill forms** (Stage 3.5 provenance): full notes — these are where algorithm assembly matters most
- **All mythological-NULL rescue forms** (Stage 4 provenance): full notes — substrate-context for these is engine-generated
- **Edge case forms surfacing thin-cell-fallback** (e.g., wind/lightning cells with substrate fallback): notes on what fallback produced

### 2.2 Cross-form patterns

- **Substrate-binding integrity**: did substrate-binding produce coherent kit identities? Any obvious mismatches (cultural_tradition × element conflicts the BC-target sampler shouldn't have produced)?
- **§ 8 strategy distribution**: are strategies firing per opportunity-scan triggers as designed? Any patterns where one strategy dominates inappropriately?
- **Calibration parameter behavior**: do the 9 § 10 calibration parameters (per MC-3 surprise) produce reasonable convergence behavior across the form set? Any parameters that look mis-tuned?
- **L9 opportunity-scan refactor outcomes**: now that triggers use mechanical_substrate signals (not cultural_tradition heuristics), do strategy selections feel right per kit identity?
- **Phase 5 naming quality**: are LLM-generated names readable + appropriate for the substrate-bound kit identity? Calibration gaps?
- **Sub-element manifestation**: does Phase 5 cohesion-coalescence produce reasonable sub-element flavoring per substrate-tradition?

### 2.3 Design-fit flags for T4 post-mortem

- **Surprising-but-valid choices**: forms where § 8 algorithm produced unexpected-but-defensible keystones (worth discussing at post-mortem; design learning)
- **Misfits**: forms where § 8 algorithm produced what reads as design-incorrect (worth amending algorithm OR composition policy)
- **Coverage gaps**: cells with no representatives OR cells where only 1-2 forms produced (substrate-distribution constraint)
- **Calibration-tuning candidates**: parameters that read as mis-tuned based on observed form behavior
- **Phase 5/6/7 gap consequences**: where naming / visual / joint-gate gaps materially affected form quality

### 2.4 Format

Markdown doc; tables where appropriate; cross-reference form IDs from generation run output; estimated gandalf effort: ~2-4 hours for the design-fit pass + summary authoring.

---

## 3. Sequencing post-generation

1. **Engine generation run** fires per KR dispatch (rocket OR star-lord; KR's judgment per seam ownership)
2. **~30-60 min later:** ~30-40 forms in loadout via star-lord export pipeline
3. **Gandalf design-fit pass** (~2-4 hours): per § 2 above
4. **Special case summary** authored at `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md`
5. **Matt-touch:** Matt reviews summary; signals readiness for T4 post-mortem session 1
6. **Parked loadout amendments fire** (per `agentic_orchestration/gandalf/notes/2026-05-25-parked-loadout-amendments-post-v1-narrow.md`) — design-mode toggle + cultural/period/quality-tier badges; ~0.5-0.75 day drax work; lands as fast-follow to support post-mortem review with engine-layer field visibility
7. **T4 post-mortem session 1** (Matt + gandalf design call; ~1-2 hours): substantive review of generation output + algorithm-vs-hand-authored comparison authoring (~5-10 alternative T4 entries per T4-B reframe)

---

## 4. What this brief does NOT touch

- **Cycle 13 scope-doc authoring** — gandalf authors AFTER T4 post-mortem session 1 outcomes inform scope (Layer 7 BDI test framework + § 8 v1.1 strategies + Pi infrastructure execution + T4-B v1 catalogue authoring are candidate Cycle 13 scope items; T4 post-mortem may also surface additional items)
- **T4-B v1 catalogue authoring** — parallel-track Matt + gandalf design call work; gated on T4 post-mortem session 1 outcomes
- **Player-game gameplay loop implementation** — far-future v1.1+ wide-scope territory
- **Engine generation run timing pressure** — fire when KR has bandwidth; no urgent timing constraint per Matt direction

---

## 5. Sign-off

**Author:** gandalf 2026-05-25 (Pattern-B framing brief authored same-session as Cycle 12 close)
**Status:** RATIFIED — Matt direction "Should we draft the engine generation..." + gandalf affirmative
**Companion docs:**
- `agentic_orchestration/cycle-12-wind-down-summary-2026-05-25.md` — Cycle 12 closure record
- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — RATIFIED Cycle 12 framing brief (L1-L11 + interface contract § 4)
- `agentic_orchestration/gandalf/notes/2026-05-25-parked-loadout-amendments-post-v1-narrow.md` — parked loadout amendments awaiting Matt signal
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — composition policy v1
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B 8-phase workflow

**For:** the engine v1 narrow milestone first-use of new engine — produces ~30-40 forms with algorithmic T4 keystones that actually shift fight behavior; gandalf design-fit pass surfaces special cases; T4 post-mortem session 1 evaluates algorithm output + authors hand-authored comparison forms.
