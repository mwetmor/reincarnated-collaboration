# Dispatch — Gamora — Cycle 14 Cascade-Resumption-3 T4 Strategy Applicability Research (pre-S2 methodology consultation)

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** gamora (engine simulation + spirit-guide seam — simulation/, spirit_guide/)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendment 2 (parallel sub-agent fan-out enabled)
- gandalf authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Amendment 2 (line 47-65 parallel-enabled trajectory) — gamora T4 strategy applicability research can fire parallel with S7+S5 (light analytical work; <300 MB RSS)
- Hive-mind decision-routing (seam-owner decides per audit evidence; Matt last-resort escalation)

**Pattern:** Pattern A-light analytical work (~2-4h; <300 MB RSS)
**R48.4 status:** RELAXED per Amendment 2 — gamora research fires in parallel with rocket S7 + star-lord S5; light analytical; sweep-resident dispatches still sequential (this is NOT sweep-resident)

---

## 0. TL;DR

**Pre-S2 methodology consultation work**: determine per-BC-cell applicability of 6 Layer 2 T4 strategies (Element Conversion A/B/C + Trade-off Reversed + Geometry Collapse + Resource Conversion per doc 47 § 4.6) to inform S2 gauntlet variant enumeration dispatch authoring.

S2 variant enumeration (post-S7) cycles through (BC × T4_strategy × investment_profile) combinations targeting ≥22 unique kit-variant rows. The per-BC-cell × T4-strategy applicability matrix is the methodology input. Doc 47 § 4.6 spec'd the 6 strategies architecturally; per-BC-cell applicability requires gamora seam analysis (simulation/T4 strategy mechanics + BC tuple applicability rules).

**This is analytical research only — read doc 47 § 4.6, doc 51 § 10.8 (strip-and-ship), existing T4 strategy code (`simulation/t4_sim_cycling.py` + related). Output: per-BC-cell × T4-strategy applicability matrix + methodology notes for S2 dispatch authoring.** No code modification.

---

## 1. Required first reads

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § Stream S2 (line 184-204) + Amendment 2 (line 47-75 parallel fan-out) + Stream S6 acceptance criteria reference
2. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 — Two-Layer T4 architecture + 6 Layer 2 strategies (Element Conversion A/B/C + Trade-off Reversed + Geometry Collapse + Resource Conversion)
3. `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.8 — strip-and-ship disposition for Layer 2 T4 cells (in-band ships as additional T4 capstone; misses band stripped)
4. `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` — existing T4 strategy cycling code (gamora's seam; reference implementation for variant cycling at simulation layer)
5. `reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` — POST-S1 (commit `99d67aa`) substrate-derived encounter IDs + BC 5-tuple fields per encounter (range/tempo/amplitude/attribute/proxy_density)
6. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — recent simulation seam state (Concern #3 P3c fix + tag `gamora/v2.15` recent context)
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11 + #18 + #42a + #45 LOAD-BEARING

---

## 2. Scope (analytical research; no code modification)

### 2.1 Per-BC-cell × T4-strategy applicability matrix

For each of 18 BC cells × 6 Layer 2 T4 strategies = 108 cells:

| BC cell | T4 strategy | Applicable? | Reasoning |
|---|---|---|---|
| (melee, low, spiky, STR, none) | Element Conversion A | YES/NO/PARTIAL | per substrate match + mechanic compatibility |
| (melee, low, spiky, STR, none) | Element Conversion B | ... | ... |
| ... | ... | ... | ... |

**Applicability dimensions to consider:**

| Dimension | What to check |
|---|---|
| Substrate match | Does the BC cell's substrate (per S1 substrate-derived encounter_id; future S7 lineage propagation) support the T4 strategy's mechanic? (e.g., Geometry Collapse may not apply to single-target spiky-amplitude kits) |
| Strip-and-ship disposition (per doc 51 § 10.8) | Per the strip-and-ship principle, Layer 2 T4 cells land if in-band ([1.5×, 2.0×] cohort_median per doc 50 § 4 Target 4); miss-band cells stripped. Per-BC-cell variant attempt vs band-fit prediction informs which strategies should be ENUMERATED at S2 (vs pre-filtered out as known to strip) |
| Investment profile interaction | Does the strategy's effectiveness scale with low/mid/max investment profile per doc 51 Patterns 1+2? (per-investment-profile applicability may differ from base applicability) |
| Cohort_archetype interaction | Does the strategy fit specific cohort_archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid) better than others per doc 50 BVV framework? |

### 2.2 Methodology notes for S2 dispatch authoring

- Variant cycling axes priority per gandalf authorization § 3 line 227 (pre-ratified): T4 strategy first → investment profile second → skill tree variant if architecturally tractable
- Effective variant cardinality estimate: 18 BC × N_applicable_T4 × 3 investment profiles
- Strip-and-ship interaction: which (BC × T4 × invest) cells likely strip vs ship → drives the ENUMERATE-vs-PRE-FILTER decision at gauntlet variant cycling
- Disc #18 hotspot question: if methodology has multiple options (e.g., enumerate-all-and-strip vs pre-filter-and-enumerate-survivors), surface to KR for gandalf design-spec-as-math handoff OR legolas Mode A methodology consultation

### 2.3 Output

Authored at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md`:

- § 1 — Per-BC-cell × T4-strategy applicability matrix (108-cell table)
- § 2 — Methodology notes for S2 dispatch authoring
- § 3 — Strip-and-ship disposition predictions per cell (for ENUMERATE-vs-PRE-FILTER decision)
- § 4 — Variant cardinality estimate (18 BC × N_applicable_T4 × 3 invest)
- § 5 — Disc #18 surface conditions (if methodology multi-option surfaces)
- § 6 — S2 dispatch authoring recommendations to knight-rider

---

## 3. Acceptance criteria (close)

- § 2.3 output document authored at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md`
- 108-cell applicability matrix populated
- Methodology notes + cardinality estimate
- KR consumption-ready (concrete S2 dispatch authoring recommendations)

---

## 4. Out-of-scope

- Code modification of any kind (this is analytical research)
- S2 gauntlet variant enumeration implementation (separate dispatch post-S7)
- T4 architecture modification (doc 47 § 4.6 architecture LOAD-BEARING; preserved)
- BVV framework modification (doc 50 LOAD-BEARING; preserved)
- Investment scaling pattern extension (doc 51 P3-P6 Cycle 15+ candidate)

---

## 5. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Methodology has multi-option choice** | E.g., enumerate-all-and-strip vs pre-filter-and-enumerate-survivors OR variant axis priority alternatives surface | Disc #18 hotspot — surface to KR with methodology options + recommendation; KR routes to gandalf design-spec-as-math OR legolas Mode A consultation |
| **Per-BC-cell applicability surfaces architectural gap** | E.g., BC cell × T4 strategy combination requires architecture-level decision (T4 strategy applicability rules undefined at canon) | Halt + surface to KR; gandalf design call territory |
| **Variant cardinality below ≥22 target** | Even with all 6 T4 strategies applied to all 18 BC cells, projected variants < 22 | Surface to KR — S2 acceptance criterion (≥22 unique kit-variant rows per gandalf authorization line 199) may need methodology adjustment OR investment profile axis becomes load-bearing |
| **R48 RAM degradation** | Mid-execution vm_stat shows free + reclaimable < 1 GB combined | Pause + report (light analytical; should not trigger) |

---

## 6. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | Per-BC-cell applicability verification against doc 47 § 4.6 spec + existing t4_sim_cycling.py code |
| **Disc #18 math hotspot consultation** | Variant cycling methodology — this research IS the consultation per Amendment 2 line 75 ("gamora T4 strategy applicability research can fire parallel with S7") |
| **Disc #42a framing-audit Q1-Q6** | Applied at research authoring — what assumptions about T4 applicability does the matrix depend on? what evidence could refute? |
| **Disc #45 vocabulary lock** | Research output uses locked vocabulary (substrate / kit / BC cell / cohort_archetype); no class/role/archetype non-exempt |
| **Disc #48 RELAXED per Amendment 2** | Parallel fan-out enabled |

---

## 7. Deliverables

1. **Research note** at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md`
2. **Completion record appended to this dispatch file** — captures: (a) matrix population evidence; (b) methodology notes summary; (c) cardinality estimate; (d) any surface-to-KR findings
3. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade work; commit fires without re-asking; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 8. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 2 parallel fan-out + gandalf authorization Amendment 2 parallel-eligible gamora research

**Gamora session-start protocol:**
1. Onboard via § 1 required first reads (especially doc 47 § 4.6 + doc 51 § 10.8 + t4_sim_cycling.py)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption
3. Execute § 2 scope (analytical only; no code modification)
4. Apply § 3 acceptance gate
5. Surface conditions per § 5 if triggered
6. Author § 7 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on close:** consume research output; author S2 dispatch (gauntlet variant enumeration expansion; rocket + gamora) per recommendations + § 6 KR consumption-ready section. S2 fires post-S7 close.

**Parallel-firing companions this batch (Amendment 2 parallel fan-out):**
- **S7 (rocket)** — Phase 2 multi-sample substrate consumption + lineage propagation; ~1-2d
- **S5 (star-lord)** — Wave B FULL implementation per canonical § 5; ~4-6h

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Completed:** 2026-05-29
**Completed by:** gamora
**Status:** CLOSED — all § 3 acceptance criteria met

### (a) Matrix population evidence (sample rows)

108-cell matrix populated at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` §§ 1.3 + 1.4.

Sample rows:
| BC cell | T4 strategy | Applicable? | Reasoning |
|---|---|---|---|
| (melee, low, spiky, STR, none) | ECA | NO | Structural: ECA applies 1.50× to magical damage path; STR kit is physical-primary; near-zero magical output → effective magnitude ~0; structurally unable to produce in-band cell |
| (melee, low, spiky, STR, none) | ECC | YES | Canonical STR/DEX assignment per engine `unified_calibration_loop.py:654`; 0.25 additive elemental on physical base; strip risk low at max invest |
| (melee, low, spiky, STR, none) | TOR | YES | Spiky amplitude favors high-crit variance; frenzy mechanic (hit -30% / crit +30%) produces burst-window KPM aligned with encounter's spiky amplitude profile |
| (ranged, medium, variable, INT, none) | ECA | YES | Canonical INT assignment per engine; 1.50× multiplicative on magical damage path; empirically validated at Phase A1 RE-RUN-5 as in-band at max invest |
| (ranged, medium, variable, INT, none) | ECC | NO | Structural: ECC applies 0.25 additive to physical base; INT kit is magical-primary; near-zero physical output → near-zero absolute bonus |
| (ranged, medium, variable, INT, light) | ECB | YES | Proxy-light cell has broadest kit composition diversity; multi-element substrate sampling (S7) expected to surface dual-element INT kits where ECB is exact fit |
| (mid, low, spiky, INT, none) | GC | YES | Mid-range position + spiky amplitude with multi-mob context; AOE-geometry skills benefit from 1.5× damage_multiplier even at 0.5 radius in chokepoint-style encounter |

### (b) Methodology notes summary

- Variant cycling axes: T4 strategy first → investment profile second → substrate sample variant third (per pre-ratified ordering; skill-tree within-chain cycling is Cycle 15+ scope)
- ENUMERATE-vs-PRE-FILTER: Disc #18 methodology multi-option surfaced (§ 5.1). Gamora recommendation: PARTIAL-enumerate (Option C) — exclude 54 structural NO cells (ECA on BC 1-8 + ECC on BC 9-18); enumerate all remaining 270 cells. Structural NOs are zero-magnitude by damage-path architecture; enumerating them adds no empirical signal.
- TRADE_OFF REVERSED canonical-vs-engine vocabulary gap: doc 47 § 4.6.5 marks as PLACEHOLDER but engine has `trade_off_reversed_frenzy` (hit -30% / crit +30%) Matt-locked. S2 uses engine implementation directly. Gandalf doc amendment flagged as low-priority follow-up.

### (c) Cardinality estimate

- Full enumeration: 18 BC × 6 strategies × 3 invest = 324 cells
- Post structural-NO filter: 270 cells (54 structural NOs excluded)
- Post-strip projected shipped variants: ~102-132 (well above ≥22 target; target structurally satisfied)
- Post-S7 multi-sample (54 kits × 6 strategies × 3 invest): 972 cells — NOT recommended for single gauntlet run; one representative sample per BC cell for T4 × invest sweep recommended; multi-sample diversity feeds PM-1 clustering

### (d) Surface-to-KR findings

1. **Disc #18 hotspot (§ 5.1):** ENUMERATE-vs-PRE-FILTER methodology multi-option choice. KR routes to gandalf or decides per pre-ratified seam-owner authority. Gamora recommendation: PARTIAL-enumerate (270 cells). Does not require Matt escalation unless gandalf raises architectural concern.
2. **TRADE_OFF REVERSED vocabulary gap (§ 5.2):** canonical doc PLACEHOLDER vs engine `trade_off_reversed_frenzy` implementation. Low-priority gandalf doc amendment. Does not block S2.
3. **Cardinality above ≥22 target (§ 4.5):** no escalation required. Target satisfied.

**Research note path:** `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md`
