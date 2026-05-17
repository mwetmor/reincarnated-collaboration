# 2026-05-17 — rocket — D10 implementation + staged-data salvage (QUEUED — auto-fires after gamora D10 math note)

**Authority:** Matt L3 2026-05-17 (~23:00 EDT). Commission queued; auto-fires when gamora D10 math note ships.
**Type:** Pattern B — generation-pipeline implementation + post-process salvage; ~1-2 days.
**Predecessor (gates auto-fire):** gamora D10 substrate-coherent gen-math note (`agentic_orchestration/dispatches/2026-05-17-gamora-d10-substrate-coherent-gen-math-note.md`).
**Status:** 🟢 **ACTIVATED 2026-05-17 ~00:00 EDT.** Gamora math note shipped (commit `92a4691`).

---

## ⚠️ JACK-RYAN GATE-1 ADVISORY — CONDITIONAL ENDORSE — 3 PRE-FLAGS

Tag: `jack-ryan/v1.4-d10-math-note-gate1-review-1`. Verdict: **CONDITIONAL ENDORSE**. Three pre-flags rocket must address at code-time (these supersede the math note where they conflict):

### PRE-FLAG 1 — WARN — `range_profile` is per-CLASS, not per-skill
Math note § 1.3 listed `range_profile` as a per-skill input — **wrong**. Empirical inspection of `season_002011/classes.json` confirms `range_profile` lives on the class object, not on individual skill objects. When you iterate skills in `derive_geometry_type()`, pass `class.range_profile` as a per-class constant — NOT a per-skill lookup. A per-skill lookup will KeyError or silently use the wrong value at salvage-script call-time.

### PRE-FLAG 2 — WARN — Gear backfill seed field is `generation_seed`, not `seed`
Math note § 8.7 specifies `rng = np.random.default_rng(seed + 999)` — **field name wrong**. 002011-015 manifests use `generation_seed` (value 2011/2012/etc.). `manifest.get("seed")` returns None → `default_rng(None + 999)` raises TypeError → deterministic 0-LLM-cost salvage guarantee in § 8.1 breaks. Read `manifest["generation_seed"]` instead.

### PRE-FLAG 3 — INFO — R11(b) round-trip clause required in your acceptance criteria
`gear_pool_staged.json` is a new output path you'll add to `season_writer.py` that the exporter reads at the export boundary. This is a cross-seam contract change per R11(b) trigger table. Your acceptance criteria must include either a round-trip smoke spec (generation → season_writer write → export fallback read → gear_pool.json populated) or an explicit `Round-trip: not applicable because <reason>` clause. Silence is not valid per R11(b).

### Note for gamora (your dependency)
When gamora implements `floor_over_band` + `estimated_gap` on `ClassBalanceResult` in balance_loop.py, she'll need a new MIGRATION.md v1.7 entry at `src/reincarnated/simulation/MIGRATION.md` BEFORE her D10 code tag. Not your concern except: don't proceed with `floor_over_band` consumption until gamora's MIGRATION lands.

---

## Why this matters

Gamora's D10 math note specifies the substrate-coherent gen-math rules + post-process salvage plan for the 5 staged seasons (002011-015) that the pre-D10 shim produced with broken data (geometry_type=null on all skills + empty gear_pool). Your dispatch:

1. **Implements** gamora's rules in `generation/` (so future regens produce clean data)
2. **Post-processes** the 5 staged seasons through the new rules (salvages LLM-expensive content; no re-naming cost)
3. **Fixes** the gear_pool empty-bug per gamora's Item 7 investigation
4. **Outputs** D10-curated 002011-015 ready for drax to point at

---

## Required reading (when activated)

1. Gamora D10 math note (path TBD per gamora's choice; likely at `reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md`)
2. Gamora v1.5 convergence sample analysis (anchor for D10 inputs)
3. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/...015/` — your post-process input
4. `reincarnated-engine/seasons/season_001005/classes.json` — old season geometry_type ground truth
5. `reincarnated-engine/src/reincarnated/generation/` — your implementation target seam

---

## Scope — three phases

### Phase A — Implement D10 rules in generation/

Per gamora's math note:
- geometry_type derivation function (consumes role/element/range_profile/etc.)
- Skill-count ceiling per archetype
- Multi-element breadth gate
- buff_damage stacking limit
- DPS density pre-balance-loop gate
- `floor_over_band` modifier_flag_tier emission

Lands in appropriate `generation/` modules. Standard rocket discipline (tests, MIGRATION.md if cross-seam, hive log).

### Phase B — Salvage the 5 staged seasons (002011-015)

Apply D10 rules as POST-PROCESS to existing staged data:

1. **For each season** (5 total):
   - Load `classes.json`, `manifest.json`, `validation_report.json`
   - **For each class:**
     - Apply skill-count ceiling (drop excess per archetype rule)
     - Apply multi-element breadth gate (trim to allowed canonical elements)
     - Apply buff_damage stacking limit (strip secondaries)
     - Populate `geometry_type` per derivation rules
     - DPS density check (flag or further prune if exceeded)
   - Re-run balance_loop on pruned class (sim only; no LLM)
   - Re-emit class JSON with curated kit + new modifier
   - Update manifest counts + validation_report
   - Rebuild classes.json
2. **For each season's gear_pool.json:**
   - Investigate why empty (per gamora Item 7)
   - Fix root cause AND backfill the 5 staged seasons' pools

Output: updated `reincarnated-engine/output/standard-demo-regen-2026-05-17/` with D10-curated classes + populated gear_pools.

### Phase C — Verify + emit handoff

- Re-run validation on each curated season
- Document per-season verdict: classes_dropped / classes_retained / convergence_rate_pre_vs_post / gear_pool_size
- Hive log STATE entry summarizing salvage outcome
- HANDOFF → drax-demo: D10-curated seasons ready for SEASON_IDS pointer flip (drax v1.11 micro-task: revert v1.10's revert; point at salvaged 002011-015)
- HANDOFF → drax-loadout: loadout's data/ should also refresh to curated versions (drax-loadout v1.2 micro-task)

---

## Out of scope (DO NOT)

- ❌ DO NOT re-run LLM naming (post-process is the path; LLM cost-savings discipline)
- ❌ DO NOT modify gamora's math note (consume only)
- ❌ DO NOT touch simulation/ (gamora's seam; you work in generation/)
- ❌ DO NOT modify drax-demo or drax-loadout directly (your HANDOFF triggers their follow-on dispatches)
- ❌ DO NOT extend beyond D10 (D11+ work is separate)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria (when activated)

- [ ] Phase A: D10 rules implemented in generation/ (with tests)
- [ ] Phase B: 5 staged seasons salvaged + gear_pools populated
- [ ] Phase C: per-season verdict documented; classes_retained > 30; convergence_rate_post > 50%
- [ ] HANDOFF → drax-demo (D10-curated SEASON_IDS unblock)
- [ ] HANDOFF → drax-loadout (data/ refresh follow-on)
- [ ] MIGRATION.md entry if cross-seam contract changes
- [ ] Hive-log STATE
- [ ] Tag `rocket/v1.12-d10-implementation-and-staged-data-salvage-1` (local; push gated per ADR-006)

---

## Coordination

- **AUTO-FIRE TRIGGER:** gamora D10 math note ships completion record. Knight-rider monitors and spawns rocket agent at that time.
- **Parallel-safe with:** drax-demo v1.10 revert (already shipped); other agents writing hive log
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Expected end-state

| State | Demo | Loadout |
|---|---|---|
| Before tonight | season_001001-005 playable | (some seasons present) |
| After drax v1.9 | season_002011-015 BROKEN | season_001001-005 + 002011-015 (broken data surfaced honestly) |
| After drax v1.10 (revert) | season_001001-005 playable again | both sets retained |
| After rocket v1.12 (this dispatch) | season_002011-015 D10-curated + playable | data/ refreshed; analytics shows post-D10 convergence delta |

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 hive-fast D10 plan. ~1-2 days when activated. Append completion record when done.*
