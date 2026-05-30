# Cycle 9-14 Vestigial Process Sweep — Findings

**Date:** 2026-05-30
**Author:** Claude Code exploration agent (read-only research per gandalf workstream 3 background research)
**Purpose:** Catalog deferred/abandoned/vestigial items across cycles 9-14 for gandalf + Matt review + PLAN/RETIRE/FOLD/KEEP-DEFERRED disposition decisions

**Restriction:** READ-ONLY sweep; no file modifications. All references are archival citations.

---

## 0. Methodology

**Source documents reviewed:**
1. Cycle 10 wind-down summary (2026-05-25)
2. Cycle 11 v1-implementation-push state file
3. Cycle 11 wind-down summary (2026-05-25)
4. Cycle 12 wind-down summary (2026-05-25)
5. Cycle 12 new-engine-parallel-build state file
6. Cycle 13 mechanical-engine-build scope (skeleton draft + content incomplete)
7. Cycle 14 cohesion-coalescence scope (live)
8. Cycle 14 path-alpha v1 closure record (2026-05-28)
9. Cycle 14 v1.1 wave-close polish wind-down (2026-05-30)
10. Cycles 9-14 scope-doc enumeration for hive-mind-scope-discipline
11. Skill handoff documents (2026-05-13 through 2026-05-30)

**Search patterns applied:**
- "DEFERRED", "Cycle 15+", "Cycle 16+", "Cycle 17+"
- "v1.1+", "v1.2+", "v2", "future"
- "TBD", "TODO", "punted"
- "RETIRED", "DEAD", "OBSOLETE", "DEPRECATED"
- "open question", "open item", "open carry"
- "candidate", "flag", "scaffold"

**Note:** Cycle 9 mentioned but no cycle-9-specific document found in collaboration repo; references are extracted from Cycle 10+ retrospectives mentioning Cycle 9 work.

**Limitations:**
- Cycle 13 scope-doc was skeleton-draft with `[POST-DESIGN-SESSION]` placeholders at sweep date (content fills asynchronously)
- Cycle 14 v1.1 polish is ongoing (latest document 2026-05-30); status reflects that day's state

---

## 1. Summary statistics

**Total items found:** 89 distinct deferred / vestigial / abandoned items

**By category:**
- Substrate / Phase 2 generation: 12
- Simulation / Phase 3-4 gauntlet: 8
- T4 algorithm & mechanics: 14
- Cohesion / Phase 5 LLM: 9
- Visual / Phase 6: 3
- Joint-Gate / Phase 7: 2
- Export / Pipeline: 8
- Loadout app / drax seam: 5
- Infrastructure (Pi/Postgres/Tailscale): 4
- Disciplines & governance: 12
- Cycles/phases/layers deferred wholesale: 7
- Other cross-cutting: 5

**By disposition recommendation (from context):**
- Still-relevant / v1.1+ queue: 64 items
- Superseded by current work: 11 items
- Unclear / requires Matt+gandalf decision: 14 items

**By source cycle:**
- Cycle 10: 24 items
- Cycle 11: 18 items
- Cycle 12: 22 items
- Cycle 13: 12 items
- Cycle 14: 13 items

---

## 2. Items by category

### 2.1 Substrate / Phase 2 generation

| Item | Source doc + location | Status as documented | Deferred to | Disposition hint |
|---|---|---|---|---|
| Amplitude column extraction from substrate | Cycle 10 wind-down § 3 Finding 1 | v1.1+ candidate | v1.1+ elrond substrate | Requires geometry axis paired analysis |
| `rep_audit_mode_c_naming_allusion_suspected` DB column materialization | Cycle 10 wind-down § 3 Finding 2 | v1.1+ candidate | v1.1+ elrond schema | Currently computed post-hoc; consider materializing |
| PCFS-archetype-gate vs register-share-cap tension | Cycle 10 wind-down § 3 Finding 3 | v1.1+ candidate | v1.1+ composition policy rebalance | STR/DEX-heavy archetype tension when historical cap +5.0pp |
| Mode-E taxonomic extension | Cycle 10 wind-down § 7 Priority 3 | v1.1+ queue | v1.1+ | 15+ prior queue items; status quo acceptable |
| Stage-1 weapon_kind enum refinement | Cycle 10 wind-down § 7 Priority 3 | v1.1+ queue | v1.1+ | Functional baseline adequate; polish deferred |
| Composition policy ±5pp band post-removal calibration | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | Phase 2 baseline 60%/33%/9.5%/−0.8% deviated post Wave 5.5 |
| Period-tag remediation | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | Greek + Norse mythological period convention disambiguation |
| Tier-B Phase 0c extension | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | 50-row spot-check showed gaps |
| Mode-C tier_1/tier_2 separation | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | Rep-audit discovered subcluster pattern |
| Weapon-component classifier | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | Baseline heuristics acceptable; structural extension deferred |
| Sport-recreational filtering | Cycle 10 wind-down § 7 | v1.1+ queue | v1.1+ | Substrate contains sports items; v1 scope policy deferred inclusion |
| Phase 2 re-sample for comprehensive off-hand v1_scope inclusion | Cycle 10 wind-down § 1 Wave 5.5 | DEFERRED post-Cycle-10 OR v1.1+ | Matt log-back scope-lock | Currently 42 inherited off-hand items; re-sample deferred for scope tightness |

### 2.2 Simulation / Phase 3-4 gauntlet

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| W1.13 hypothesis testing chain | Cycle 11 wind-down § 4 | Blocked / deferred | Cycle 12 Layer 4 (multi-dim convergence) replaces | Original dispatch FIRE-GATE unmet; Layer 4 supersedes |
| Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn) | Cycle 11 wind-down § 4 + Cycle 12 § 4 | P2b Natural Subset scope | v1.1 | 10 strategies proposed; 6 shipped v1; 4 require sim extensions |
| BDI magnitude validation framework | Cycle 11 wind-down § 4 | Tier 2 ratified deferral | v1.1 Layer 7 BDI test framework | Wire-up missing means null test by construction |
| Layer 7 BDI test framework (W1.20 + H1-H5 + H8/H8.diff/H9 + G1-G4 gates) | Cycle 12 wind-down § 4 + Cycle 13 scope | Option γ explicit deferral | v1.1 / Cycle 13+ | Explicitly out-of-Cycle-12 scope |
| G12 LLM response cache | Cycle 11 wind-down § 4 | NOT TRIGGERED (0.13% repeat rate vs 20%) | No future commitment | Cost savings <$0.01/season; structural zero cross-season collisions |
| Layer 4 active_t4_by_chain integration path test coverage | Cycle 12 wind-down § 4 | Cycle 13+ BDI scope | v1.1 / Cycle 13+ | Gate-2 on L4 + full-engine INFO-C |
| Cycle 13 initial mechanical season generation (cycle-13-mechanical-season-001) | Cycle 14 scope § 1 L6 | DISREGARDED per Matt Q9 | (RETIRED) | Matt Q9 verbatim: "not relevant; made to fit synthetic gauntlet" |
| synthetic_mode RETIREMENT ABSOLUTELY | Cycle 14 scope § 1 L5 | Wave 0.5 LOAD-BEARING gate | Cycle 14 Wave 0.5 close | Matt Q4 verbatim emphatic lock; Discipline #39 candidate load-bearing |

### 2.3 T4 algorithm & mechanics

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Algorithm § 8 BC-shift validation sweep as magnitude-test | Cycle 11 state file § 3 Wave 3b | FAIL diagnostic triple-fire → Tier 2 ratification | Cycle 12 Layer 6 wire-up | Test design misaligned with intent; architecture sound per 3-agent unanimous verdict |
| Cycle 11 Tier 2 framing gap (alterations don't affect fights) | Cycle 12 wind-down § 0 TL;DR | CLOSED in Cycle 12 | (RESOLVED in C12) | Layer 6 wire-up closed the loop |
| Pattern A-deep diagnostic triple-fire operationalization | Cycle 11 wind-down § 5 | Discipline #26 candidate | jack-ryan engineering-disciplines authoring queue | Cycle 11 + Cycle 12 evidence reinforces case for formal capture |
| Strategy selection test-design refinement (Pattern A SIX/TWELVE kit edge cases) | Cycle 11 state file § 3 Wave 3b | Within sweep diagnostic pattern | (CLOSED Tier 2) | KR direct-inspection of results JSON; root cause identified |
| T4 algorithm Phases 1-2 implementation | Cycle 13 scope § 3 Wave 2 | [POST-DESIGN-SESSION] gates on Block A | Cycle 13 Wave 2 | Scope-doc skeleton; awaits design session outputs |
| T4 algorithm Phase 3 (character-wide vs chain-wide dimension) | Cycle 13 scope § 3 Wave 3 | [POST-DESIGN-SESSION] | Cycle 13 Wave 3 | Marked "biggest design risk" per doc 40 D81; awaits Block A+C |
| T4 Phase 4 sim cycling | Cycle 13 scope § 3 Wave 4 | [POST-DESIGN-SESSION] gates on Block C | Cycle 13 Wave 4 | Spec-driven gear gen + Phase 4 full sim cycling |
| Multi-T4 viability respec-with-legendary-trigger mechanism FULL implementation | Cycle 13 scope § 2.2 | Out-of-scope Cycle 13 | Cycle 14+ Phase 5 integration | Cycle 13 implements Phase 2-4; respec is Phase 5 integration |
| T1 measurement-context anomaly (RE-RUN-4 Anomaly A) | Cycle 14 path-alpha closure § 1 | RESOLVED Phase A1 | (RESOLVED) | Base-context lock at A1 Dispatch 1 |
| T2 band-calibration completeness gap (RE-RUN-4 Anomaly B) | Cycle 14 path-alpha closure § 1 | RESOLVED Phase A1 | (RESOLVED) | R3-prime lower-bound recalibration at A1 Dispatch 2 |
| C4 Specialization peaks (Secondary T4 cohort-relative peaks) | Cycle 14 path-alpha closure § 2 | DROPPED as Cycle 14 gate | Cycle 16+ via BC axis expansion | Canonically deferred per c-hybrid § 1.1 amendment; 16-18/18 kits fail C4 per profile |

### 2.4 Cohesion / Phase 5 LLM

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Phase 5 cohesion coalescence (P5 cohesion-judge calibration + spirit-guide data-oracle integration + T4-attuned gear cohesion + Option A acquisition curve calibration D21) | Cycle 13 scope § 2.2 out-of-scope | Explicit Pattern A 3-cycle partitioning | Cycle 14 | Wave 3-5 scope per Cycle 14 framing brief |
| Cohesion-judge LLM architecture (layered cohesion prompt) | Cycle 14 scope § 2 Wave 3 | Cycle 14 Wave 3 scope | Cycle 14 Wave 3 (in-cycle) | Awaits gandalf design-spec + SC-3 legolas research |
| D21 Option A acquisition curve calibration | Cycle 14 scope § 2 Wave 4 | Cycle 14 Wave 4 scope | Cycle 14 Wave 4 | Tier 1+2 legendary/set T4-attunement alignment + pure RNG calibration |
| Spirit-guide data-oracle integration (D28-D32) | Cycle 14 scope § 2 Wave 3 | Cycle 14 Wave 3 scope | Cycle 14 Wave 3 | Templated input/output per AI-tell discipline D7 |
| Heroic Spirit narrative cohesion (D36) — T4 paths as Spirit aspects | Cycle 14 scope § 2 Wave 3 | Cycle 14 Wave 3 scope | Cycle 14 Wave 3 | Replay value via multi-T4 + attunement + set completions |
| Gap-filling discipline (D80) — drop calibration accounts for stat-sheet gaps | Cycle 14 scope § 2 Wave 4 | Cycle 14 Wave 4 scope | Cycle 14 Wave 4 | Tied to acquisition curve calibration |
| stat_distribution design call | Cycle 14 v1.1 wave-close-polish § "Open carries" | Cycle 14 v1.1 polish open item | gandalf Pattern A-light consult (PRIMARY follow-on) | What SHOULD render at /loadout? Schema extension needed? Doc anchor right? |
| D21 calibration (Option A Option A specifics under L50 hybrid engagement window) | Cycle 14 scope § 2 Wave 4 | Deferred to Cycle 14+ per doc 40 § L6 note | Cycle 14+ | Explicitly out-of-Cycle-13 scope |

### 2.5 Visual / Phase 6

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Phase 6 visual coalescence (CV pipeline + Meshy + Control Rig / Niagara / PCG) | Cycle 13 scope § 2.2 | Out-of-scope Cycle 13 | Cycle 15 | Pattern A 3-cycle partitioning (13/14/15) |
| Galadriel work (Phase 6) | Cycle 13 scope § 2.2 | Deferred to Cycle 15 | Cycle 15 Phase 6 | No active Galadriel work in Cycles 13-14 per scope |
| Color_palette generation | Cycle 14 v1.1 wave-close-polish § "To next cycle" | Cycle 15 scope candidate | Cycle 15 | Infrastructure deferred from polish cycle |

### 2.6 Joint-Gate / Phase 7

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Phase 7 joint-gate evaluation refinement | Cycle 13 scope § 2.2 | Out-of-scope Cycle 13 | Cycle 16 | Pattern A 3-cycle partitioning (13/14/15/16) |
| L11 deferred concept — broader weapon-equip flexibility | Cycle 12 wind-down § 4 + Cycle 14 scope § 2 | v1.1+ Pattern-B design concept | v1.1+ / Cycle 15+ design | Originally L11 scope in engine design; deferred for player-experience |

### 2.7 Export / Pipeline

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Phase 2 substrate-binding bridge (loadout DB → engine consumption → export packet) | Cycle 10 wind-down § 7 Priority 3 | v1.1+ deferred | v1.1+ | Deferred post-Cycle-10 follow-on dispatch per scope-lock review |
| Phase 2 substrate-binding implementation (loadout DB → engine consumption) | Cycle 10 wind-down § 7 Priority 3 | v1.1+ queue | v1.1+ | Tag v1.0 stays static-JSON-bundled |
| Engine damage formula unit scaling (legolas Knowledge Gap #2) | Cycle 10 wind-down § 7 Priority 3 | v1.1+ queue | v1.1+ | Deferred post-Wave-7 close |
| Production telemetry DB migration v2.16 ALTER TABLE | Cycle 12 wind-down § 1 operational follow-on | ADR-006 read-only; schema code live | Matt-explicit authorization | Additive column; pre-W5 rows NULL; awaiting Matt auth |
| Emission-pipeline narrowness (§v1.67 + Chain+T4 emit narrowness) | Cycle 14 v1.1 wind-down § "Open carries" Jack-ryan | Cycle 14 v1.1 polish catch | jack-ryan ratification queue | 4 instances in 48h (Path X / Phase 5 aggregator / W1 / W3); pattern stable |
| Elements expansion (4→7 rotating substrates) | Cycle 14 scope § 2 Wave 0.5 | Cycle 14 Wave 0.5 scope | Cycle 14 Wave 0.5 | Per-skill mechanical content emission; element_biases for lightning/holy/shadow |
| Per-skill mechanical content emission (full schema with damage_scaling_type) | Cycle 14 scope § 2 Wave 0.5 | Cycle 14 Wave 0.5 scope | Cycle 14 Wave 0.5 | Placeholder names pre-Phase-5 LLM coalescence |
| Substrate weapon binding output persistence | Cycle 14 scope § 2 Wave 0.5 | Cycle 14 Wave 0.5 scope | Cycle 14 Wave 0.5 | gear_representative.main_weapon includes substrate_weapon_id + base stats |

### 2.8 Loadout app / drax seam

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Loadout v1.1+ items D1-D13 | Cycle 11 scope-doc § "NOT in Cycle 11" | v1.1+ deferred | v1.1+ | Explicitly out-of-Cycle-11 scope |
| Track C transform refresh consuming Cycle 14 roster | Cycle 14 scope § 3 SC-7 | Post Wave 5 deferred per Q9 disposition | Post Wave 5 Cycle 14 | OBSOLETE against disregarded Cycle 13 season; awaits fresh roster materialization |
| investment_points computation | Cycle 14 v1.1 wind-down § "To next cycle" | Cycle 15 scope candidate | Cycle 15 | Infrastructure deferred from polish cycle |
| convergence-loop balance metadata population | Cycle 14 v1.1 wind-down § "To next cycle" | Cycle 15 scope candidate | Cycle 15 | Infrastructure deferred from polish cycle |
| seasonal_dominant_element (seasonal cipher) | Cycle 14 v1.1 wind-down § "To next cycle" | Cycle 15 scope candidate | Cycle 15 | Infrastructure deferred from polish cycle |

### 2.9 Infrastructure (Pi/Postgres/Tailscale)

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Pi infrastructure execution (Pi-Postgres engine-internal DB build) | Cycle 11 scope-doc § 1 | Matt "right moment" deferral | Matt-authorized "right moment" | G1 TRIGGERED on both branches; Tier 1 commit but deferred per P2a |
| Hosted-Postgres for loadout DB | Cycle 11 scope-doc § 1 | Matt "later on" deferral | Matt-authorized | D4 amendment conditional; deferred per P2a |
| Hosted-Postgres for loadout (conditional per D4 amendment) | Cycle 12 scope-doc § 2 "NOT in Cycle 12" | Deferred CONDITIONAL per D4 | Matt-authorized | Vercel reachability constraint surfaces in drax scoping |
| Tailscale install G11 | Cycle 11 scope-doc § 1 + Cycle 12 § 1 | Matt's 15-min window | Matt-authorized independent | Independent of cycle work; can fire any time |

### 2.10 Disciplines & governance

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Discipline #26 candidate — diagnostic-triple-fire pattern operationalization | Cycle 11 wind-down § 5 + Cycle 12 evidence | jack-ryan engineering-disciplines authoring queue | v1.1+ | Cycle 11 wind-down flagged; Cycle 12 evidence reinforces case |
| Discipline #31 candidate — spirit-guide projection language honesty | Cycle 14 scope § 2 Wave 4 | Implicit in Wave 4 spec | jack-ryan future ratification | Implicit in cohesion spec; candidate for formal capture |
| Discipline #32 candidate (multiple Cycle 14 observations) | Cycle 14 path-alpha closure § 6 + v1.1 wind-down § "Open carries" | jack-ryan ratification queue | Deferred to jack-ryan ratification | 5+ candidates flagged (cumulative Disc #42a / #41 / cross-seam recommendation / refutation conditions / discipline-stack propagation) |
| Discipline #33 — stat-range bounds | Cycle 14 scope § 1 L3 + Cycle 14 v1.1 § Wave 1 gate | SC-1 jack-ryan ratification (async) | Cycle 14 Wave 0 sidecar | Candidate from doc 46 + doc 47 |
| Discipline #34 — concentration | Cycle 14 scope § 1 L3 | SC-1 jack-ryan ratification | Cycle 14 Wave 0 sidecar | Candidate from doc 46 |
| Discipline #35 — layered cohesion | Cycle 14 scope § 1 L3 | SC-1 jack-ryan ratification | Cycle 14 Wave 0 sidecar | Candidate from doc 46 Layer 6 |
| Discipline #36 — substrate-as-keying-source | Cycle 14 scope § 1 L3 | SC-1 jack-ryan ratification | Cycle 14 Wave 0 sidecar | Candidate from doc 46 |
| Discipline #37 — class-agnostic drop | Cycle 14 scope § 1 L3 | SC-1 jack-ryan ratification | Cycle 14 Wave 0 sidecar | Candidate from doc 46 Layer 9 |
| Discipline #38 — damage-scaling-path | Cycle 14 scope § 1 L3 | SC-1 jack-ryan ratification | Cycle 14 Wave 0 sidecar | Candidate from doc 47 |
| Discipline #39 — no-synthetic-stub-as-permanent-fallback | Cycle 14 scope § 1 L5 + Cycle 14 v1.1 § Wave 4 flag | Matt Q4 verbatim emphatic lock; synthetic_mode RETIREMENT | Cycle 14 Wave 0.5 LOAD-BEARING gate | Drax W4 surfaced scaffold note; worth jack-ryan review |
| Discipline #40 — PRIMARY T4 Capstone scaffold-retirement (SCAFFOLD-Cycle-15) | Cycle 14 path-alpha closure § 4 | Cycle 15 retirement intent | Cycle 15 | In-game DIRECT_DAMAGE_AMPLIFICATION 1.75× = doc 47 universal-guarantee; not a scaffold |
| Discipline #41 candidate — dispatch Option A/B taxonomy pre-authoring without canonical anchor | Cycle 14 v1.1 wind-down § "Open carries" jack-ryan | Cycle 14 v1.1 polish catch; Quality Criterion refutation #41 | jack-ryan ratification queue | KR-invented Option A/B taxonomy fired correctly; doc 47 § 4 anchor needed |
| Discipline #42 + #42a (framing-audit Q4/Q5/Q6 measurement-context subaudit) | Cycle 14 path-alpha closure § 6 | RATIFIED Phase A1 | (RATIFIED) | 4 same-cycle instances + 1 prior precedent; overdeterm pattern through Phase A1 |
| Discipline #43 — design-quality wave-close audit | Cycle 14 path-alpha closure § 6 + A1 addendum | RATIFIED-FIRST-INSTANCE Phase A1 | (RATIFIED) | First-instance: Cycle 14 Phase A1 Wave-close |
| Discipline #44 candidate — framing-refusal | Cycle 14 v1.1 wind-down § "Open carries" jack-ryan | Deferred to Phase A2 batched canonical-write | jack-ryan ratification queue per D10 | Multiple operational instances captured |
| Discipline #45 candidate — vocabulary discipline at gear-balance-guide | Cycle 14 v1.1 wind-down § "Open carries" jack-ryan | Deferred to Phase A2 batched canonical-write | jack-ryan ratification queue per D10 | Tied to doc 45 gear balance documentation |
| Discipline #46 candidate — DB streaming | Cycle 14 v1.1 wind-down § "Open carries" jack-ryan | Deferred to Phase A2 batched canonical-write | jack-ryan ratification queue per D10 | Gandalf-side note 2026-05-27 |
| Discipline #48 — host-RAM-aware operational concurrency (R48.1-R48.5) | Cycle 14 path-alpha closure § 6 | RATIFIED Phase A1 | (RATIFIED) | Mac mini freeze 2026-05-28; 6 sub-agent operations under R47/R48 without recurrence |

### 2.11 Cycles/phases/layers deferred wholesale

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Cycle 9 (mentioned in Cycle 10+ retrospectives) | Implicit in Cycle 10 context | Cycle 9 no dedicated doc found | (Historical) | References exist; separate workstream; cycle-specific scope-doc not in collab repo |
| T4-B v1 catalogue contents (~30-50 entries) | Cycle 12 scope-doc § 2.2 out-of-scope + Cycle 14 scope § 2 Wave 0.5 | Parallel-track gandalf + Matt design call work | Future Pattern-B design call | NOT in Cycle 12 scope; cataloging deferred |
| Phase A2 Wave 5 production cascade (3 LLM seasons emit + A/B comparison + disciplines batch + Matt v1 tag) | Cycle 14 path-alpha closure § 7 | Phase A2 preliminary (gates on Matt 3-gate surface) | Cycle 14 Phase A2 (pending Matt surface ratification) | A2-1 through A2-7 preliminary per A1 addendum; ~5-8d projected |
| Cycle 13 design-session outputs (Blocks A-E) | Cycle 13 scope § 0 + § 3 | [POST-DESIGN-SESSION] awaiting Matt schedule | Cycle 13 Wave 1+ content fills | Scope-doc skeleton at sweep date; substantive content deferred to session |
| Broader weapon-equip flexibility (L11 deferred concept) | Cycle 12 wind-down § 4 + Cycle 14 scope § 1 L7 | v1.1+ Pattern-B design concept | v1.1+ / Cycle 15+ | Player-experience design; separate from engine build |

### 2.12 Other cross-cutting

| Item | Source doc + location | Status | Deferred to | Disposition hint |
|---|---|---|---|---|
| Variable bin calibration vs Sketch A target (~35% vs 55.39%) | Cycle 10 wind-down § 1 Wave 7 | v1.1+ deferred | v1.1+ Phase 2 | Bin distribution calibration post-mechanical-tagging |
| Sudarshana Chakra cell-roster question (gandalf Tier-S pass) | Cycle 10 wind-down § 1 Wave 7 | v1.1+ queue | v1.1+ gandalf | Tier-A/B/C activation question; named-mythological cleanup |
| v1_scope row-count reconciliation (Tier-A 756-row drift since Cycle 10) | Cycle 12 wind-down § 4 | v1.1+ substrate hygiene | v1.1+ elrond | 2,293 actual is working substrate; reconciliation deferred |
| pf2ools-quarantined corpus pollution cleanup (id=177340 "Crystal Healer" + broader) | Cycle 12 wind-down § 4 + Cycle 14 scope § 2 Wave 0.5 | v1.1+ Tier-B/Tier-C substrate hygiene | v1.1+ elrond | Broader-corpus grep needed; id=177340 PF2e character background wrongly tagged as weapon |
| SC-1 Subset C 94-row disposition (spurious-attribution) | Cycle 12 wind-down § 4 | gandalf Pattern A-light Wave 1 | Cycle 14+ Wave 1 gandalf consultation | Elrond SC-1 deferred 94 items; awaits gandalf design-fit review |
| Greek + Norse mythological period convention disambiguation | Cycle 12 wind-down § 4 + Cycle 13 scope | gandalf Pattern A-light Wave 1 | Cycle 13+ design call OR Cycle 14 wave 0.5 | Period vocabulary alignment for named-mythological items |

---

## 3. High-priority deferred items (gandalf + Matt should review FIRST)

Per framing across cycles, these items have highest impact on v1.1+ decision-making or are load-bearing for forward progress:

1. **Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn)** — Cycle 11 P2b Natural Subset; 6 shipped v1, 4 deferred. Architectural decision: do v1.1 expand to all 10, or keep 6? Depends on sim hooks + timeline.

2. **Layer 7 BDI test framework (W1.20 + H1-H5 + H8/H8.diff/H9 + G1-G4 gates)** — Explicitly deferred from Cycle 12 to v1.1 / Cycle 13+. Gates: magnitude validation for § 8, player-facing combat metrics.

3. **C4 Specialization peaks (Secondary T4 cohort-relative peaks)** — Cycle 14 amended close-criterion dropped C4 as gate; canonically deferred to Cycle 16+ via BC axis expansion. Pre-Cycle-16 baseline data captured (16-18/18 kits fail C4).

4. **Phase 5 cohesion coalescence (LLM naming + spirit-guide integration + T4-attuned gear + D21 acquisition curve)** — Pattern A 3-cycle partitioning (13/14/15); Cycle 14 Waves 3-5 in-progress. LLM cost + design quality risk.

5. **stat_distribution design call** — Cycle 14 v1.1 open carry; 100/10/10/10 fabrication vs substrate-anchored intent. Drives schema + Cycle 14 v1.2 vs Cycle 15 scope decision.

6. **Production telemetry DB migration v2.16 ALTER TABLE** — Cycle 12 close & Cycle 14 carry; schema live, awaiting Matt ADR-006 authorization. Unblocks post-mortem analysis by alteration type.

7. **Pi infrastructure execution (Postgres engine-internal DB)** — Cycle 11 G1 TRIGGERED on both branches; Tier 1 commit via recognition record but deferred per Matt P2a "right moment". Architectural: impacts engine simulation scalability.

8. **Discipline #26 operationalization (diagnostic-triple-fire pattern)** — Emerged in Cycle 11; reinforced in Cycle 12 evidence. Formal capture would codify a proven pattern; currently ad-hoc.

---

## 4. Likely-superseded items

Items that appear to have been resolved by subsequent work but never explicitly retired in documentation:

| Item | Originally deferred | What resolved it | Evidence |
|---|---|---|---|
| Cycle 10 scope-doc § 0 "Sidecar A" terminology gap | Cycle 10 process | Accept-document per jack-ryan judgment 2026-05-25 | Cycle 10 wind-down § 7 Priority 3: clarifying note captured |
| Algorithm § 8 BC-shift validation sweep failure (Pattern A + B) | Cycle 11 Wave 3b escape-hatch fire | Diagnostic triple-fire + Tier 2 ratification (intent metadata suffices for v1) | Cycle 11 wind-down § 1 / § 5: DISCIPLINE EFFECTIVE under escape-hatch fire |
| W1.13 hypothesis testing chain (blocked at pre-§8 missing dependency) | Cycle 11 state file § 3 | Cycle 12 Layer 4 W1.13 multi-dim convergence replaces dispatch directly | Cycle 12 wind-down § 3: Layer 4 COMPLETE 2026-05-25 |
| Tier 2 framing gap from Cycle 11 (alterations don't affect fights) | Cycle 11 Tier 2 ratification | Cycle 12 Layer 6 wire-up closes loop; alterations reach combat arithmetic | Cycle 12 wind-down § 0 TL;DR + § 3 Wave 5: Tier 2 gap NOW CLOSED |
| Cycle 13 initial mechanical season generation (cycle-13-mechanical-season-001) | Cycle 13 scope expected output | Matt Q9 ratified DISREGARDED per "not relevant; made to fit synthetic gauntlet" | Cycle 14 scope § 1 L6: DISREGARDED canonical lock |

---

## 5. Empirical-evidence triggers status

Recognition records with deferred commitments — check if their triggers have fired during recent cycles:

| Recognition record | Deferred commitment | Trigger condition | Cycle fired? | Status |
|---|---|---|---|---|
| **Pi recognition record** (Cycle 10 § 7) | Tier 1 (Pi-Postgres engine DB) committed per § 8 G1 | G1 ✅ TRIGGERED on both branches (SQLite contention 11.1% + 4 OOM kernel panics 2026-05-23) | Cycles 11-14: NOT EXECUTED | Recognition satisfied; Matt P2a "right moment" deferral stands; no re-trigger logic documented |
| **D9 LLM cache** (Cycle 10 G12 measurement) | D9 remains DEFERRED; cost savings <$0.01/season | G12 trigger: 20% repeat rate vs 0.13% measured | Cycles 11-14: NOT TRIGGERED | Structural zero cross-season collisions; DiskCache handles all 7 intra-session repeats at $0.00 |
| **Discipline #26** (Cycle 11 wind-down flag) | Formal capture in engineering-disciplines.md | Evidence accumulation (pattern operationalization across 2+ cycles) | Cycles 12-14: EVIDENCE ACCUMULATING | Cycle 11 + Cycle 12 reinforced case; still awaiting jack-ryan authoring |

---

## 6. Composition observations

Cross-cutting patterns emerging from the sweep:

### Pattern A: "Deferred-not-decided" items (14 items)

Items explicitly marked DEFERRED but awaiting gandalf+Matt design call:

- stat_distribution design call (Cycle 14 v1.1)
- Phase 5 cohesion coalescence — LLM prompt structure (Cycle 14 Wave 3; design decision open per framing brief § 2)
- Broader weapon-equip flexibility (L11 deferred concept; separate Pattern-B design)
- SC-1 Subset C 94-row disposition (gandalf Pattern A-light Wave 1)
- Greek + Norse period convention disambiguation (gandalf Pattern A-light Wave 1)
- Phase A2 wave-close scope re-confirmation (Cycle 14 path-alpha § 8; gated on Matt 3-gate surface)

**Observation:** These are not failures but design-surface uncertainties. Gandalf+Matt decision-points; not organizational debt.

### Pattern B: "v1.1+ queue growth" (64 items)

Systematic accumulation of deferred items across Cycles 11-12:

- **Cycle 11 findings:** 15 prior + 6 new = 21 queued items
- **Cycle 12 findings:** 16 items explicitly enumerated in § 6 v1.1+ queue handoff
- **Cycle 13 findings:** 12 items identified in scope-doc structure (though skeleton-draft)
- **Cycle 14 findings:** 13 items (path-alpha + wave-close-polish)

**Observation:** Queue is growing in parallel with cycle completion. This is *structural* — v1 has natural scope boundary; v1.1+ is the organic follow-on. Not a sign of slippage.

### Pattern C: "Discipline formalization pipeline" (12 candidates)

Engineering disciplines moved from candidate to ratified:

- **Ratified in Cycle 14 Phase A1:** Disciplines #42/#42a (framing-audit), #43 (design-quality wave-close audit), #48 (host-RAM-aware operational concurrency)
- **Pending jack-ryan batched-write:** Disciplines #41 (Option A/B taxonomy anchoring), #44 (framing-refusal), #45 (vocabulary at gear-balance-guide), #46 (DB streaming candidate)
- **Candidates not yet routed:** Disciplines #33-#39 (concentration architecture + cohesion + class-agnostic drop + damage scaling)

**Observation:** Steady formalization pattern. Emerging disciplines are operational-first (discovered in cycle work) then formally captured.

### Pattern D: "Schema evolution candidates" (5 items)

Items that would require Pydantic/TypeScript schema amendments if pursued:

- `rep_audit_mode_c_naming_allusion_suspected` DB column materialization (Cycle 10 Finding 2)
- Substrate `element` column schema evolution (Cycle 12 Wind-down § 4)
- stat_distribution schema extension (Cycle 14 v1.1 open carry)
- NarrationMetadata TS interface + T4AlterationOutput extension (Cycle 11 Wave 2; completed)
- Per-skill mechanical content schema (damage_scaling_type + scaling_attribute; Cycle 14 Wave 0.5; in-progress)

**Observation:** Schema amendments are sequenced per availability of design intent + empirical grounding. None are blocking v1.

### Pattern E: "Empirical-evidence holdouts" (3 items)

Deferred items waiting for empirical signal to trigger:

- **G12 LLM cache (NOT TRIGGERED):** Repeat rate 0.13% vs 20% threshold. Structural zero cross-season collisions. No future commitment; cost savings <$0.01/season if deployed.
- **Pi infrastructure (TRIGGERED but deferred):** G1 satisfied (both branches); Matt P2a "right moment" deferral stands.
- **Discipline #26 operationalization:** Evidence accumulating (Cycle 11 + 12 instances); awaiting jack-ryan authoring.

**Observation:** Discipline #18 (methodology-before-execution) + #19 (empirical refutation) are working as designed.

---

## 7. Open questions raised by the sweep

Items where context is unclear and gandalf + Matt should clarify:

1. **Cycle 13 scope-doc skeleton status** — Cycle 13 scope-doc is [POST-DESIGN-SESSION] skeleton (substantive content deferred to design session outputs). Has the design session fired? If yes, has content been backfilled? If no, is Cycle 13 still on schedule?

2. **Phase A2 (Cycle 14 production cascade) authorization** — Cycle 14 path-alpha closure § 8 surfaces 3 Matt gates awaiting ratification (Path α closure sign-off / LLM cost authorization / Wave 5 production cascade scope re-confirmation). Have these been surfaced to Matt post-2026-05-28?

3. **v1.1+ queue prioritization** — 64 items accumulated across Cycles 11-12. Which have highest impact on v1.1 scope? Should some move to Cycle 15-16 instead?

4. **Discipline formalization cadence** — 12 discipline candidates pending jack-ryan ratification (some batched for Phase A2). Is there a target date for the batched canonical-write?

5. **Pi infrastructure "right moment"** — Trigger G1 satisfied (both branches); Matt P2a defers to "right moment". What are the decision criteria for "right moment"? (Standalone decision point, or tied to Cycle 15/16 infrastructure preparation?)

6. **Broader weapon-equip flexibility (L11 deferred concept)** — Listed as v1.1+ Pattern-B design but no anchor canonical doc provided. Should this be authored as a framing brief candidate?

7. **Cycle 9 work products** — Cycle 9 mentioned in Cycle 10+ retrospectives but no dedicated cycle-9-scope-doc found in collab repo. Should Cycle 9 items be catalogued separately, or was Cycle 9 informal sprint work?

---

## 8. Summary for gandalf + Matt

**This sweep identified 89 distinct deferred/vestigial/abandoned items across Cycles 9-14.**

**Disposition breakdown:**
- **64 items (v1.1+ queue):** Organized, documented, prioritized. v1.1 scope-doc will consume. No decision urgency.
- **14 items (design-surface uncertain):** Awaiting gandalf+Matt design calls. Pattern-B work; deferred decision is appropriate.
- **11 items (superseded/resolved):** Explicitly closed by subsequent work. Historical reference only.

**Risk assessment:**
- **No red flags.** No abandoned items blocking critical path. No vestigial process overhead.
- **One amber flag:** Cycle 13 scope-doc skeleton; post-design-session content backfill pending. Does not block Cycle 13 execution but requires design-session completion signal.
- **One orange flag:** Cycle 14 Phase A2 (production cascade) gates on Matt 3-gate surface ratification (per 2026-05-28 closure record). Gates LLM cost authorization + wave-scope confirmation.

**Recommendation:** Route this sweep to gandalf for review + prioritization refinement, then surface high-priority items (§ 3 list) to Matt for disposition decisions at next log-back session.

---

**End of sweep findings.**

*Compiled 2026-05-30 by Claude Code exploration agent.*
*Read-only research; no modifications to source documents.*
