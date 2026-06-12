# Gate-2 Handoff — Spatial Re-Point Phase 3/4 (gamora → jack-ryan)

**Author:** gamora
**Date:** 2026-06-12
**For:** jack-ryan Gate-2 (DEV-MODE, BLOCK authority) — reviews math note + implementation together
**Dispatch:** `agentic_orchestration/dispatches/2026-06-12-gamora-spatial-repoint-phase-3-4.md`
**Math note (Gate-2 PASS-with-INFO 2026-06-11):** `simulation/math/spatial-repoint-recalibration-2026-06-11.md` (§ 10 + § 11 = Phase 3/4 actuals)
**MIGRATION:** `simulation/MIGRATION.md` v1.65
**Vestigial-ontology register:** `gandalf/notes/2026-06-12-vestigial-ontology-register.md`
**Predecessor handoff:** `gamora/notes/2026-06-11-spatial-repoint-phase-0-1-2-gate-2-handoff.md`

---

## 0. Top-line

Phase 3/4 COMPLETE. Commit-grade spatial player→mob damage re-points from the simplified flat model
to the kernel damage truth (`damage_resolver.resolve_skill`); `SPATIAL_DAMAGE_SCALE` recalibrated
4.0 → 0.6; golden master re-captured as the new commit-grade oracle. All 27 structural tests pass.
All golden-master movement is math-note-predicted; ZERO STOP. Kernel READ-ONLY (Phase 0 v1.64
boundary honored). No cross-seam telemetry schema change. One structural follow-on flagged
(magic_pack HP-scope; out of dispatch scope).

Requesting: Gate-2 review + a decisions-log entry for the Discipline #12 semantic shift + a
disposition routing for the magic_pack structural follow-on (§ 6).

---

## 1. Golden-master harness output — WR distribution before/after

Corpus: 10 season_001010 classes × 6 ArenaScenario = 60 cells, 10 fights/cell, seed 770011 (fixed).
Harness: `scripts/gamora_spatial_golden_master_2026_06_11.py`.

**Overall saturation (WR ≥ 0.9):** 95% (57/60) pre-re-point → **65% (39/60)** at SDS=0.6. De-saturated.

| cell WR movement (vs pre-re-point oracle, at SDS=0.6) | count |
|---|---|
| WR DOWN | 21 |
| WR UP   | 1 |
| WR unchanged | 38 |

**The single UP cell** — `mini_boss::class_0009` 0.0 → 1.0 — is EXPLICITLY predicted in math note
§ 2.1 ("cells already below saturation [mini_boss class_0001/0007/0009 at WR=0.0] may move UP if
armor-vs-boss interactions were previously punishing under the flat model"). class_0009 named.

**Per-scenario shape at SDS=0.6** (spread = max−min WR across 10 classes):

| scenario | sat≥0.9 | spread | floor≤0.1 | disposition |
|---|---|---|---|---|
| open_arena | 8/10 | 1.00 | 2/10 | discriminating ✔ |
| chokepoint_corridor | 8/10 | 0.70 | 0/10 | discriminating ✔ |
| elite_pack | 7/10 | 1.00 | 3/10 | discriminating ✔ |
| mini_boss | 4/10 | 1.00 | 6/10 | discriminating ✔ (the § 3 calibration anchor) |
| boss_with_adds | 2/10 | 1.00 | 7/10 | discriminating but FLOOR-heavy (boss HP dominates; § 2.1-predicted) |
| **magic_pack** | **10/10** | **0.00** | 0/10 | **STRUCTURAL — not DPS-tunable (§ 6)** |

**Determinism:** new oracle self-verify = 0/60 moved (bit-stable). Pre-re-point oracle preserved in
git history (`5a7b079`); the re-captured oracle is the new commit-grade baseline at the same path.

---

## 2. Geometry-hit count comparison (negative contract § 2.3) — HELD

- `dominant_geometry_hist` changed in **4/60** cells. ALL 4 are TTK-explained: each has
  `mean_elapsed_s` increased ≥1.5× (lower DPS → longer fight → different skill-cast mix → different
  accumulated-hit dominant geometry). Examples: chokepoint::class_0006 elapsed 25.4→113.2s
  (line→point); mini_boss::class_0008 elapsed 97.6→240.0s/timeout (point→circle).
- Geometry SELECTION logic (`_select_skill_for_entity`, `_compute_aoe_hits`) is UNTOUCHED. The
  re-point changes per-cast DAMAGE MAGNITUDE only → fight LENGTH → accumulated-hit histogram.
- `mean_total_aoe_hits` rose (median +54.6) — same mechanism (longer fights = more casts).
- This is exactly the § 2.3 sanctioned exception ("except where a fight ends earlier/later"). The
  negative contract — "the re-point changes DAMAGE magnitude, not WHICH targets are hit" — HOLDS.

---

## 3. Per-fight cost measurement (§ 5 re-check)

| measurement | value |
|---|---|
| math-note simplified baseline (warm) | 5.8 ms/fight |
| re-measure trigger (1.5×) | > 8.7 ms/fight |
| resolver path, MATCHED fight-length (SDS=4.0, short fights) | **3.41 ms/fight** (BELOW baseline) |
| resolver path, SDS=0.6 (de-saturated, ~4.5× longer fights) | 27.9 ms/fight (= 4.8× baseline) |
| per-sim-second cost: SDS4.0 vs SDS0.6 | 0.198 vs 0.240 ms/sim-second |

**Diagnosis (Discipline #11):** the raw §5 re-measure trigger FIRES (27.9 > 8.7). BUT the cost
increase is FIGHT-LENGTH driven — de-saturation makes fights ~4.5× longer (more ticks), which is the
recalibration working as designed, NOT resolver per-call overhead. At matched fight-length the
resolver path is BELOW the simplified baseline. Per-sim-second efficiency is essentially flat.
Disposition: the § 4 re-gate model's `C_s` (commit-grade per-fight cost) updates to the longer
fight cost; the 12× PC factor stays ASSUMED + SEPARABLE (§ 7, not banked). No interface degradation.

**For Gate-2:** confirm you accept the fight-length attribution for the §5 trigger, OR flag if you
want a separate cost-budget disposition before commit-grade status is granted.

---

## 4. Vestigial-ontology charge compliance (dispatch § 3 / register a/b/c)

- **(a) No new surface named in legacy ontology vocabulary.** New surfaces: `combatant_state`,
  `resolver_skills` (SpatialEntity fields); `player_class`, `mob_objects`, `monster` (keyword
  params); `resolve_spatial_hit`, `_SingleTargetSkillView`, `_ResolverSkill`, `build_resolver_skills`,
  `combatant_projection_from_*` (adapter module). All substrate-truthful (resolver / combatant /
  damage vocabulary), none are archetype/role/class-style ontology names.
- **(b) No new required-native ontology field added to the kernel input schema.** The kernel
  CombatantState is built via the EXISTING `from_player_class` / `from_monster` factories
  (production path; unchanged) OR a declared, defaulted projection from the export dict (harness /
  smoke; data-projection rule Q3). `simulate_fight` / `resolve_skill` signatures + internals
  UNCHANGED (Phase 0 v1.64 boundary).
- **(c) Each newly-threaded legacy field has a register row + crosses per its disposition:**
  - `archetype` → NAME-ONLY: carried as construction label, NEVER branched on in the adapter.
  - `range_profile` → STRUCTURAL-BENIGN: defaulted projection `"medium"` via `getattr`/`.get`.
  - `energy_type` → STRUCTURAL-CONSTRAINING: crossed as-is; NO new value introduced → no
    kernel-change-protocol + DEFENSIVE_TRADEOFF gate update triggered.

---

## 5. DEFENSIVE_TRADEOFF reinstatement (dispatch § 2 — shadow+holy)

`damage_resolver.py:324`: `if element in ("shadow", "holy") and getattr(defender, "t4_chaos_immune", False)`.
Verified in isolation: vs a `t4_chaos_immune` defender, shadow → 0 (`on_chaos_immune`), holy → 0
(`on_chaos_immune`), fire → full (`on_hit`); non-immune defenders take full from both. No
golden-master delta on season_001010 (pre-T4 corpus carries no `t4_chaos_immune` and no holy
enemies), as the dispatch § 2 predicted. Matt-ratified 2026-06-12.

---

## 6. STRUCTURAL FOLLOW-ON (out of dispatch scope) — magic_pack disposition request

The single-parameter `SPATIAL_DAMAGE_SCALE` sweep CANNOT cure `magic_pack` saturation at ANY value
(WR=1.0 for all 10 classes down to SDS=0.35). Root cause: `magic_pack` is NOT in
`MOB_HP_DIFFICULTY_SCENARIOS` (HP-multiplier scope = open_arena + chokepoint only) and its
4-mob / 120s structure clears comfortably at any tunable player DPS. Curing it requires an
HP-multiplier-SCOPE decision (extend `MOB_HP_DIFFICULTY_SCENARIOS`) — a separate scope change beyond
Discipline #24 single-parameter isolation and beyond this dispatch. I did NOT silently expand the
scope. The 5/6 tunable scenarios reaching a discriminating surface is the deliverable.

**Request:** route a follow-on disposition (KR dispatch or decisions-log entry) for the
HP-multiplier-scope decision. boss_with_adds floor-heaviness is the symmetric structural outlier
(boss HP dominates; § 2.1-predicted) — likely the same scope conversation.

---

## 7. What I need from Gate-2

1. **Semantic-shift decisions-log entry** (Discipline #12 — math note § 9): commit-grade spatial WR
   is no longer the same quantity (R-series recalibration lineage; SDS 4.0→0.6).
2. **Cost-trigger disposition** (§ 3): accept fight-length attribution, or flag a cost-budget gate.
3. **magic_pack follow-on routing** (§ 6).
4. **Commit-grade status grant** (contract § 5) at clean verification — milestone tag pending your
   sign-off (no tag fired yet).

**Test state:** 27/27 spatial structural PASS. 7 pre-existing `test_cycle13_wave5_gauntlet_sim.py`
failures confirmed pre-existing via git-stash on HEAD (eligible_encounters_passed counting —
unrelated subsystem); my change adds ZERO new failures.

**Signed:** gamora, 2026-06-12.
