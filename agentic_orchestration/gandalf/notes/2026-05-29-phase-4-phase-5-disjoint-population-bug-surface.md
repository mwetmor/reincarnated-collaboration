# Phase 4 → Phase 5 Disjoint Population Bug — Empirical Surface

> **STATUS:** CURRENT — gandalf-authored bug surface 2026-05-29 evening late. Discovered post-A2-1-RE-FIRE-3 close while investigating Phase 5 LLM output anomalies. Routes to KR for parallel-team-redirect (rocket/gamora/jack-ryan investigations underway; this surface provides the SPECIFIC finding to anchor their work).
>
> **Composes with:** Amendment 7a (in-flight; per-chain element wiring); cascade-resumption-3 work program; Cycle 14 Wave 5 season_001 production fire diagnostic.

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward)
**Composition:** Cycle 14 cascade-resumption-3 post-production diagnostic
**Authority:** Matt 2026-05-29 evening late ("if you found the bug, let's surface it to KR and resolve" verbatim)

---

## 0. TL;DR

Phase 4 Pareto-2 archive (34 mixed-sample kits per Amendment 6 Sub-fix 1+2) and Phase 5 PM-1 cluster input (208 unique members, all `_s2`-suffixed) are **~80% disjoint populations** at the kit_id join layer.

| Source | Population | Sample distribution |
|---|---|---|
| Phase 4 archive (kit_archive.db; feeds Phase 7 mechanical gate) | 34 base kits | s0=18, s1=9, s2=7 |
| Phase 5 PM-1 clusters (feeds Phase 7 cohesion gate; produces faction labels + Wave B names) | 208 unique kit_ids | **s0=0, s1=0, s2=208** |
| **Overlap** | **6** | s0=0, s1=0, s2=6 |
| Phase 4 accepted NOT in Phase 5 | 28 | s0=18, s1=9, s2=1 |
| Phase 5 members NOT in Phase 4 | 202 | s0=0, s1=0, s2=202 |

**Empirical chain (all artifacts at `agentic_orchestration/cycle-14-wave-5-season-001/`):**
- `phase2_kit_candidates.json`: 54 kits CORRECT (s0=18, s1=18, s2=18; all 8 elements; 12 hybrid; 5 lineages)
- `phase4_archive_insertion.json`: 34 ACCEPT with mixed samples CORRECT (Amendment 6 working)
- `phase5_faction_clusters.json`: 4 clusters / 208 members ALL `_s2` suffix — disconnect surfaced
- `kit_archive.db`: 34 rows mixed samples (Phase 4 → Phase 7 join)

**Root cause located** at code level: `wave5_season_orchestrator.py:825-836`:
```python
base_kit_datas = [_build_pm1_kit_data(k, k.character_id) for k in passing_kits]
variant_kit_datas = [_build_pm1_kit_data(vr, vr.character_id) for vr in variant_passing_rows]
surviving_kit_datas = base_kit_datas + variant_kit_datas  # PM-1 input
```

Phase 5 PM-1 reads `passing_kits` (Phase 3 mechanical-gate output) + `variant_passing_rows` (S2 variant emission output; all `_s2`-naming). **Phase 4 Pareto-2 archive is NOT consumed.**

---

## 1. Architectural status — parallel-by-design OR sequential-bug?

Two interpretations of the code layout:

### Interpretation A — parallel-by-design
- Phase 4 archive → Phase 7 mechanical gate (kit_archive.db)
- Phase 5 PM-1 → Phase 7 cohesion gate (cluster_id assignment)
- These are PARALLEL workstreams meeting at Phase 7
- Phase 7 joins on kit_id; requires both mechanical_pass AND cohesion_pass

**Observation against this interpretation:** if join is at Phase 7, then only 6 kits can ship (the 6 in both populations). Yet `season_summary.json` reports `phase7_shipped_worthy: 22`. So either Phase 7 doesn't strictly require BOTH gates, OR the 22 count is a different metric, OR there's implicit cluster_id assignment for kits Phase 5 didn't see.

### Interpretation B — sequential-bug
- Phase 4 archive was INTENDED to feed Phase 5 PM-1 input
- The current code path is a pre-Amendment-6 holdover that wasn't updated when Pareto-2 partition was added
- Phase 5 should consume Phase 4 archive output, ensuring cluster population = mechanical-gate population

**Observation against this interpretation:** none of the orchestrator math doc (`cycle-14-wave-5-season-001-orchestrator-math-2026-05-27.md`) explicitly states Phase 4 → Phase 5 pipe. The doc describes Phase 4 archive → Phase 7 bridge. Phase 5 clustering input is described separately.

**Open question to resolve at code investigation:** what does Phase 7's join logic actually require? Does it ship kits that have mechanical_pass but NO cluster_id assignment? Or does cohesion_pass require explicit cluster membership? rocket/gamora resolve.

---

## 2. Three candidate fix paths (rocket+gamora deliberate scope)

### Path X — Phase 5 PM-1 input = Phase 4 archive
- Change `wave5_season_orchestrator.py:825-831` to read from Phase 4 archive output rather than passing_kits + variant_passing_rows
- Phase 5 clusters operate on the 34 mixed-sample Pareto-2 winners
- 100% Phase 4 ∩ Phase 5 overlap at Phase 7 join layer
- **Downside:** Phase 5 PM-1 clusters on 34 kits (smaller); may degenerate to k=2 or k=3 (current k=4); variant-population substrate for cluster boundary inference goes away
- **Upside:** strongest architectural coherence; Pareto-2 selection drives faction labels; minimal s0-blanket missing-from-output issue

### Path Y — S2 variant emission extends to s0/s1/s2 samples
- Change S2 variant emission to generate variants for ALL 3 substrate samples per cell (currently `_s2_` hardcoded in variant naming)
- Phase 5 PM-1 input grows from ~200 members to ~600 (3x variant count)
- Phase 5 cluster members reflect all sample diversity
- Phase 4 archive still feeds Phase 7 mechanical gate separately
- **Downside:** triples variant count + LLM cost (Phase 5 cohesion judge runs on more); doesn't unify Phase 4 → Phase 5 conceptually
- **Upside:** keeps parallel architecture; addresses s2-only-variant naming bug; cheaper code change

### Path Z — Variants enter Phase 4 archive via Pareto-2 insertion
- Currently `variant_accepted_count: 0` — Phase 4 rejects all variants
- Allow variants to enter Phase 4 Pareto-2 archive based on Q-vector dominance
- Phase 7 sees mixed base+variant population in archive
- Phase 5 still operates on passing_kits + variants, joins at Phase 7
- **Downside:** variant accept/reject criterion needs design call (S6a-FIX previously addressed variant wr_bracket_pass inheritance — extending to Pareto-2 archive needs new spec)
- **Upside:** maximizes population at Phase 7; preserves both architectural seams

### Hybrid Path X+Y
- Path X (Phase 5 input = Phase 4 archive) AND Path Y (extend variants to s0/s1/s2)
- Phase 5 clusters on Phase 4 archive output (34 mixed-sample kits) + variant_passing_rows extended to mixed-sample naming
- Strongest coherence; highest implementation cost

---

## 3. Gandalf-lean recommendation

**Lean: Path X (Phase 5 PM-1 input = Phase 4 archive output)** with caveats:

1. Phase 5 cluster member count drops from ~208 to 34. PM-1 GMM may select k=2 or k=3 (currently k=4 with sparsity branch). Verify PM-1 sparsity branch behavior at n=34.

2. Variant Pareto archive insertion (Path Z element) becomes Cycle 15+ canonical-write candidate. For Cycle 14 v1, variants are mechanical-gauntlet noise, not player-facing surface. Phase 5 faction labels + Wave B kit names operate on base kits only.

3. The 4-of-8 element coverage gap I flagged earlier at Phase 5 is RESOLVED by Path X — Phase 4 archive has 34 kits spanning all 8 elements per Amendment 7 verification (rocket smoke confirmed at engine commit 8d5be1b). Phase 5 inherits 8-element coverage.

**Implementation cost estimate:** ~1-2hr rocket (code change at orchestrator + PM-1 sparsity branch verification + ~5-10 new tests).

**Composition with Amendment 7a (in-flight):** Path X is independent of Amendment 7a; both can land in the same rocket dispatch OR sequentially.

---

## 4. Cumulative Disc #42a Instance 6 pattern observation

Revised count after architectural refinement:

1. Wave B phantom-component → CLOSED
2. Variant Pareto-dominance → pre-ratified A3
3. Sub-fix 3 namespace-only → PASS-with-INFO
4. Amendment 7 hybrid metadata-only → Amendment 7a fix-pack
5. **Phase 4 → Phase 5 disjoint population — Path X candidate** (NEW; was provisionally Instance 6 #5 in my prior framing; revised to architectural-parallelism-with-implementation-gap; jack-ryan + gandalf wave-close evaluation determines final classification)

If Path X interpretation B holds (sequential-bug; Phase 4 should feed Phase 5), this is Instance 6 #5. If Path X interpretation A holds (parallel-by-design with implementation gap at variant naming), it's a different pattern class.

**For wave-close canonical-write:** capture this as either Instance 6 sub-case #5 OR as new pattern category "parallel-workstream-population-disjoint-at-join-layer" — jack-ryan + gandalf adjudicate.

---

## 5. KR routing instructions

**Redirect parallel team investigations** to focus on Phase 4 → Phase 5 disjoint population bug:

### Rocket — Path X scope confirmation + implementation
- Read this surface doc + verify Phase 5 PM-1 input code path
- Investigate Phase 7 join logic: does shipped_worthy require BOTH gates strictly, or one-of-two? (explains 22 shipped despite 6 overlap)
- Propose Path X implementation: change `wave5_season_orchestrator.py:825-831` to consume Phase 4 archive output as PM-1 input
- Estimate cost + risks (PM-1 sparsity at n=34; cluster count drop k=4→k=2/3; variant exclusion implications)
- Submit Amendment 7b spec proposal OR confirm Path Y/Z alternative

### Jack-ryan — architectural arbitration
- Read the orchestrator math doc + dispatch artifacts for Phase 4 / Phase 5 design intent
- Resolve interpretation A (parallel-by-design) vs interpretation B (sequential-bug)
- Apply Disc #42a Q1-Q6 to the disconnect
- Document for Cycle 14 wave-close canonical-write: cumulative Instance 6 framing OR new pattern class

### Gamora — Phase 7 join logic + acceptance rate
- How does Phase 7 verdict log compute `shipped_worthy` at the kit_id level when Phase 5 cluster_id assignment is sparse?
- Why is `phase3_passing_kit_count: 13` low (24% mechanical pass rate)?
- Sample distribution within `passing_kits` — are s0/s1/s2 represented OR is mechanical gate skewing to s2?

### Gandalf (me) — design context + canonical-write candidates
- Standing by for team findings
- Will integrate findings + recommend Path X/Y/Z selection
- Cycle 14 wave-close canonical-write candidates accumulating

---

## 6. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening late "let's surface it to KR and resolve" verbatim
**Composition:** Cycle 14 cascade-resumption-3 post-production diagnostic; Amendment 7b candidate scope

**For KR:** redirect parallel team investigations (rocket/jack-ryan/gamora) to anchor on this surface doc; consolidate findings to gandalf for Path X/Y/Z selection + Amendment 7b spec firing decision.

**For all team:** reference this doc as the empirical anchor; do NOT re-investigate Phase 4 archive correctness (verified working) NOR Phase 2 element coverage (verified at all 8) — focus on Phase 5 PM-1 input population vs Phase 4 archive disconnect.
