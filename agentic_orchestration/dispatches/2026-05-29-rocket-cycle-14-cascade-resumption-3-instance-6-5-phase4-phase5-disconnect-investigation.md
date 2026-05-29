# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 Instance 6 #5 Investigation: Phase 4 → Phase 5 Disconnect (Code-Level)

**Date:** 2026-05-29 evening late
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam)
**Authority:** Matt 2026-05-29 evening late "why not also fire jack ryan? and rocket?" verbatim + gandalf parallel fan-out directive (Disc #42a Instance 6 #5)

**Pattern:** Pattern A-light code-level investigation (~30-60min; NO code modification — analytical only; output: Amendment 7b spec proposal OR decorative-by-design confirmation)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Parallel-firing companions this batch:** jack-ryan (framing audit + Instance 6 canonical record) + gamora (Phase 3 mechanical gate analysis)

---

## 0. TL;DR

**Investigate Phase 4 → Phase 5 disconnect surfaced by gandalf:** Phase 5 PM-1 cluster input bypasses Phase 4 Pareto-2 archive entirely. Phase 5 operates on `passing_kits` (Phase 3 mechanical gate) + `variant_passing_rows` (s2-only naming convention). Amendment 6 Sub-fix 2 Pareto-2 work is DECORATIVE for player-facing output.

**Empirical chain at `cycle-14-wave-5-season-001/`:**
- Phase 4: archive=34 with s0=18, s1=9, s2=7 (CORRECT per Amendment 6 spec)
- Phase 5: 208 unique members, ALL _s2 suffix; only 6 of 34 P4-accepted survive
- Phase 5 input code: `wave5_season_orchestrator.py:825-836`

**Investigation goal:** Determine root cause + propose Amendment 7b spec OR confirm decorative-by-design.

---

## 1. Required first reads

1. gandalf parallel fan-out directive (this dispatch authority)
2. `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:825-836` — Phase 5 input code
3. `agentic_orchestration/cycle-14-wave-5-season-001/phase4_archive_insertion.json` (34 archive with s0=18, s1=9, s2=7 distribution)
4. `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (208 unique members; all _s2)
5. `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` lines 479+ `_build_variant_kit_rows()` (VariantKitRow construction; s2-only naming convention)
6. Amendment 6 commit `6f9843c` (Sub-fix 2 Pareto-2 partition implementation)
7. Your AGENT_STATE.md at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`

---

## 2. Investigation scope (analytical only; NO code modification)

### 2.1 passing_kits composition analysis

At Phase 3 mechanical gate output, what is the sample distribution per cell in `passing_kits`?
- Per BC cell, which sample_idx values produced passing kits?
- Total passing_kits count (gandalf reports 13/54 base + 585 variants = 598 PM-1 input pre-current-investigation)
- Distribution across cohort_archetype (DPS-min-maxer / Balanced / Defensive / Hybrid)
- Distribution across cultural_lineage_canonical

### 2.2 variant_passing_rows _s2_ hardcoding location

Trace the `_s2_` naming convention through:
- `_build_variant_kit_rows()` in `season_generation_pipeline.py` (legendary_id construction)
- VariantKitRow.character_id field
- Phase 5 input code `wave5_season_orchestrator.py:825-836` filter or selection logic
- Determine WHERE the `_s2_` filtering originates (intentional spec OR accidental hardcoding)
- Extension cost: what would it take to include _s0 + _s1 + _s2 variants?

### 2.3 Phase 4 Pareto-2 archive consumption analysis

Determine whether the Phase 4 Pareto-2 archive (34 kits) is:
- **Dead-code:** never consumed by any downstream stage
- **Decorative-by-design:** intentionally surfaced for player-facing output but not for Phase 5 LLM/PM-1
- **Consumed elsewhere:** Phase 7 mechanical gate? telemetry? export pipeline (drax)?
- **Should be consumed by Phase 5 but isn't:** intent gap (Amendment 7b candidate)

Trace `kit_archive` table reads/writes engine-wide via grep:
- `grep -rnE 'kit_archive' src/reincarnated/` — locate all consumers
- Identify what each consumer reads (which kits / which fields / which Pareto state)

### 2.4 Output recommendation

Author findings note at `agentic_orchestration/rocket/notes/2026-05-29-cascade-r3-instance-6-5-phase4-phase5-disconnect-investigation.md`:

- § 1 — passing_kits composition findings
- § 2 — _s2_ hardcoding location + trace
- § 3 — Phase 4 Pareto-2 consumption analysis
- § 4 — **Verdict: Amendment 7b spec proposal OR decorative-by-design confirmation**
- § 5 — If Amendment 7b: scope estimate (code changes + tests + smoke effort)
- § 6 — Surface-to-KR conditions if architectural concern beyond current scope

---

## 3. Acceptance criteria

- Findings note authored at § 2.4 location
- All 4 investigation areas (§ 2.1-2.3) addressed empirically
- Verdict explicit (Amendment 7b spec OR decorative-by-design)
- KR consumption-ready findings (informs gandalf Path decision)

---

## 4. Out-of-scope

- ANY code modification (analytical only)
- Implementation of Amendment 7b (if proposed; separate dispatch post-gandalf Path decision)
- Re-firing cascade
- Other architectural changes
- Cycle 14 wave-close canonical-write (jack-ryan parallel dispatch)
- Phase 3 mechanical gate analysis (gamora parallel dispatch)

---

## 5. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Discovery of additional Instance 6 surfaces** | Code-level investigation surfaces 6th+ pattern instance beyond current finding | Document at findings; surface to KR for gandalf design-context analysis |
| **Investigation reveals architectural impossibility** | Phase 4 Pareto-2 cannot reasonably be threaded to Phase 5 OR _s2_ filter is structurally locked | Document + surface to KR — gandalf Path decision impact |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces ADDITIONAL pre-imposed assumption | Halt + surface to KR |
| **Effort exceeds ~2h** | Investigation significantly beyond ~30-60min | Surface to KR — scope reconsideration |

---

## 6. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | All 4 investigation areas grounded in code grep + JSON inspection |
| **Disc #41 substrate-led discipline** | Substrate-led promise per Amendment 6+7 must be empirically verified at Phase 5 input layer |
| **Disc #42a framing-audit Q1-Q6** | LOAD-BEARING — Instance 6 #5 surface; verify Amendment 6 Sub-fix 2 (Pareto-2) claim matches Phase 5 empirical consumption |
| **Disc #45 vocabulary lock** | Substrate-led vocabulary used in findings |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |

---

## 7. Deliverables

1. **Findings note** at `agentic_orchestration/rocket/notes/2026-05-29-cascade-r3-instance-6-5-phase4-phase5-disconnect-investigation.md`
2. **Completion record appended to this dispatch file** — captures: (a) passing_kits composition; (b) _s2_ hardcoding trace; (c) Pareto-2 consumption; (d) verdict; (e) Amendment 7b scope estimate (if applicable); (f) any surface-to-KR findings
3. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-r3 investigation work; do NOT push

---

## 8. Sign-off

**Authored:** knight-rider per gandalf parallel fan-out directive + Matt 2026-05-29 evening late authority ("why not also fire jack ryan? and rocket?" verbatim)

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption
3. Execute § 2 scope (analytical only; NO code modification)
4. Apply § 3 acceptance gates
5. Surface per § 5 if triggered
6. Author § 7 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on rocket close:** consolidate findings to gandalf for Path decision (Amendment 7b fire-now / Cycle 14 v1 PASS-with-INFO / cascade-resumption-4).

**Parallel-firing companions:** jack-ryan (framing audit + Instance 6 canonical record) + gamora (Phase 3 mechanical gate analysis).

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-29 evening late
**Findings note:** `agentic_orchestration/rocket/notes/2026-05-29-cascade-r3-instance-6-5-phase4-phase5-disconnect-investigation.md`

### (a) passing_kits composition

- Total: 13 kits, all `sample_idx=2` (`_s2` suffix)
- 0 kits at sample_idx=0 or 1 — structural consequence of config_to_kit collision (see § c below)
- Per-lineage: fantasy_generic=7, east_asian=3, european=2, southeast_asian=1
- Per-cohort: balanced=10, dps_min_maxer=3 (defensive=0, hybrid=0 — no dense-proxy cells in this run)
- Per-BC-range: melee=6, ranged=6, mid=1
- Per-BC-attribute: wis=5, int=3, str=3, dex=2
- Element distribution: earth=6, physical=3, fire=1, wind=1, lightning=1, water=1; hybrid=3, mono=10
- 5 cells produce zero passing kits (their s2 kit failed WR bracket)

### (b) _s2_ hardcoding location + trace

**No hardcoded filter exists in Phase 5 input code (lines 825-836).** The _s2_ exclusivity is a structural consequence of `config_to_kit` dict collision in `w5r2_gauntlet_sim_integration()` (`generation/season_generation_pipeline.py:1424-1428`). The gauntlet uses `legendary_id = f"{bc_cell_id}_{chain_id}"` (not `character_id`). All 3 samples for the same cell emit the same `legendary_id`. The loop `config_to_kit[cfg["legendary_id"]] = kit` overwrites s0 with s1 then s2. Only s2 KitCandidates receive `wr_bracket_pass=True`. The `_s2_` in variant IDs is intentional Amendment 6 S2 naming convention — not a filter.

### (c) Phase 4 Pareto-2 consumption analysis

- Phase 4 archive: 34 rows (s0=18, s1=9, s2=7); 0 variant rows (all 585 rejected: `inferior_duplicate` — variant quality_vectors identical to parent base kit; MG-3 flags them)
- Phase 4 Pareto-2 archive is **consumed by Phase 7** — `phase7_bridge.py` reads ALL 34 ACTIVE rows, evaluates mechanical viability, emits verdict. Result: 22 shipped-worthy, 12 held-mechanical
- Phase 4 is NOT dead-code. NOT decorative-by-design. Phase 7 is the intended Phase 4 consumer
- Phase 5 PM-1 input operates on a SEPARATE population (WR-bracket-passing) — parallel downstream branch from Phase 3, not a Phase 4 → Phase 5 sequential chain
- Overlap between Phase 4 archive and PM-1: 6 kits (s2 base kits that passed both gates)
- 28 Phase 4 accepted kits (s0/s1) are absent from PM-1 due to config_to_kit collision

### (d) Verdict

**Architectural bypass — NOT Amendment 7b; NOT decorative-by-design.**

Phase 4 → Phase 5 bypass is the intended architecture. Phase 4 populates kit_archive for Phase 7. Phase 5 operates on PM-1 (WR-bracket) population. Both are valid downstream paths from Phase 3.

Gandalf finding ("Amendment 6 Sub-fix 2 Pareto-2 work is DECORATIVE for player-facing output") is partially correct in that Pareto-2 archive members don't feed Phase 5 faction clustering. But they DO feed Phase 7 mechanical gate, which determines shipped-worthy output. The claim that it is "decorative" does not hold at the Phase 7 level.

**NEW surface (§ e):** The config_to_kit collision is the structural root cause of all-_s2_ Phase 5 input. This may be a separate Instance 6 candidate.

### (e) Amendment 7b scope estimate

Amendment 7b not recommended — bypass is architectural. However, **config_to_kit collision fix** is a candidate:

- Modify `w5r2_gauntlet_sim_integration()` to accumulate all samples per `legendary_id`, mark all `wr_bracket_pass=True` — ~13 lines
- PM-1 input would grow from 598 to ~624 (s0/s1 survivors added)
- Effort estimate: 45-90 min code + smoke
- DESIGN QUESTION prerequisite: should all 3 Amendment-7 distinct-element samples per cell enter PM-1?

### (f) Surface-to-KR findings

**§ 5 row 1 triggered (additional Instance 6 surface):**

`config_to_kit` dict collision in `w5r2_gauntlet_sim_integration()` (`season_generation_pipeline.py:1424-1428`) silently drops s0/s1 kits from WR bracket across all 18 cells. Disc #42a pattern: pre-imposed structural constraint shaping all downstream WR bracket, PM-1, Phase 5 outputs invisibly. This may be Instance 6 #6. Surfaced to KR for gandalf design-context analysis.

**Corollary gap:** 22 Phase 7 shipped-worthy kits include s0/s1 kits without faction cluster assignment (cohesion_data only covers 13 s2 base kits from Wave B). Export/drax downstream gap — not a new Instance 6 surface by itself.

**Collab commit:** `764e732`
