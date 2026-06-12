# Dispatch — Gamora: Spatial Re-Point Phase 3/4

**STATUS:** READY TO FIRE — Gate-2 PASS-with-INFO on math-note (jack-ryan, 2026-06-11); vestigial-ontology register complete (2026-06-12)
**Authored by:** knight-rider (gandalf Pattern-B session, 2026-06-12, Matt-authorized; KR acting author per mobile-session constraint)
**Target agent:** gamora
**Seam:** simulation/ (fight engine, damage resolver, spatial gauntlet)
**Does NOT touch:** generation, output, telemetry, demo, loadout

---

## 0. Context

The forward-architecture contract (§ 8.2) authorized spatial combat re-point remedy (b): commit-grade spatial combat must re-point at `damage_resolver.resolve_skill` rather than the retired simplified model. The math-note (`simulation/math/spatial-repoint-recalibration-2026-06-11.md`) designed the recalibration and has received Gate-2 PASS-with-INFO. The Phase 0/1/2 proving run is complete (oracle captured, determinism proven, saturation symptom reproduced + pinned). Phase 3/4 is the implementation phase.

The golden-master oracle: `simulation/spatial_gauntlet/golden_master/spatial_golden_master_season_001010_2026_06_11.json`
Harness: `scripts/gamora_spatial_golden_master_2026_06_11.py`
27/27 spatial tests pass at baseline.

---

## 1. Phase 3 — Spatial re-point adapter

**Scope:** Thread `PlayerClass`/`Monster` objects through `entity_from_class_dict` / `entity_from_monster_dict` across the full spatial call path. This is a caller-side change confirmed clean (`balance_loop._run_spatial_slot:2625` already holds full objects). No kernel modification required.

**Work items:**
1. Identify all spatial call-path sites that currently pass simplified damage parameters instead of full PlayerClass/Monster objects
2. Thread full objects through `entity_from_class_dict` / `entity_from_monster_dict` at each site
3. Verify no new kernel parameters introduced — caller-side change only

**Expected outcome (math-note predictions — verify against oracle):**
- WR DECREASES from 57/60 (95%) saturated baseline — de-saturation
- Variance WIDENS
- Geometry-hit counts UNCHANGED (negative contract — geometry is independent of damage path)

**Golden-master gate:** after Phase 3 changes, run the harness. Every delta must be either math-note-predicted (WR decrease / de-saturation / variance widening) or a STOP. Zero unexplained deltas. All 27 structural tests must pass.

---

## 2. Phase 3 immediate item — shadow+holy extension

**Scope:** `damage_resolver.py:324` — extend shadow-only immunity check to shadow+holy.

**Current code:**
```python
if element == "shadow" and getattr(defender, "t4_chaos_immune", False):
```

**Change to:**
```python
if element in ("shadow", "holy") and getattr(defender, "t4_chaos_immune", False):
```

**Authorization:** Matt-ratified 2026-06-12 per DEFENSIVE_TRADEOFF reinstatement ruling. Shadow+holy = 2/7 damage types (~29% coverage), comparable to PoE CI's coverage ratio. Shadow-only (1/7 ≈ 14%) too thin to justify the tradeoff cost.

**No golden-master delta expected** from this change unless Season 001010 kits include DEFENSIVE_TRADEOFF kits AND the gauntlet enemy set includes holy-damage enemies. Confirm empirically.

---

## 3. Vestigial-ontology charge (gandalf, Matt-ratified 2026-06-12)

> The Phase 3 adapter (threading PlayerClass/Monster through `entity_from_class_dict` / `entity_from_monster_dict` across the spatial call path) MUST NOT propagate `PlayerClass`/archetype ontology into any **new** interface surface it authors. New parameters/returns use substrate-truthful vocabulary; legacy fields cross only as declared, defaulted projections (data-projection rule Q3). jack-ryan Gate-2 verifies: (a) no new surface named in legacy ontology vocabulary; (b) no new required-native ontology field added to the kernel input schema; (c) any field the adapter newly threads gets a register row in the vestigial-ontology register (`gandalf/notes/2026-06-12-vestigial-ontology-register.md` § register section).

**Register reference:** `agentic_orchestration/gandalf/notes/2026-06-12-vestigial-ontology-register.md`
- `archetype` → NAME-ONLY (never branch on it; pass as telemetry label only)
- `range_profile` → STRUCTURAL-BENIGN (derivable-with-default `"medium"`; physical question; keep)
- `energy_type` → STRUCTURAL-CONSTRAINING (closed enum; thread as-is; any new energy_type addition requires kernel-change protocol + DEFENSIVE_TRADEOFF gate update)

---

## 4. Phase 4 — Validation

**Work items:**
1. Run golden-master harness post-Phase-3 implementation
2. Confirm all math-note predictions hold
3. Confirm 27/27 structural tests pass
4. Measure per-fight cost delta — re-measure trigger iff >1.5× baseline

**Gate-2 handoff:** after Phase 4 validation, author gate-2 handoff note for jack-ryan. Include:
- Golden-master harness output (WR distribution before/after)
- Geometry-hit count comparison (must be unchanged)
- Per-fight cost measurement
- Vestigial-ontology charge compliance confirmation (a/b/c above)

---

## 5. What this dispatch does NOT include (separate items)

- **Enemy elemental distribution algorithm** — guaranteeing meaningful coverage across all 7 damage types in encounter pools. Separate dispatch; does not block Phase 3/4.
- **T4-aware gear equipping algorithm** — kit construction reading T4 strategy assignment and deriving gear priorities. Separate dispatch; gated on T4 architecture session.
- **Mana shield combat mechanic** — DEFENSIVE_TRADEOFF full implementation gated on T4 architecture session.
- **DEFENSIVE_TRADEOFF gate condition in kit construction** — mana energy_type + mana shield skill required. Gated on T4 architecture session.
- **Combo/focus pool max level-scaling** — hardcoded maxes (combo=5, focus=100) are implementation-time crutches to be replaced with level-derived scaling. Gated on T4 architecture session.

---

## 6. Session note

KR authored this dispatch in the same Pattern-B session as the vestigial-ontology register and kernel field/value audit (2026-06-12). Matt could not open new sessions on mobile. The gamora Phase 3/4 dispatch was listed as the immediate next operational item in the 2026-06-11 session-close handoff.

**Author:** knight-rider (acting), 2026-06-12. Gamora: fire when you next engage.

---

## Completion record (gamora, 2026-06-12)

**STATUS:** COMPLETE — implementation + recalibration + golden-master validation done; routed to jack-ryan Gate-2. Milestone tag pending Gate-2 sign-off.

**Item 1 (shadow+holy, § 2):** `damage_resolver.py:324` shadow-only chaos-immunity extended to shadow+holy. Verified in isolation (shadow+holy→0 vs immune defender; fire passes). No season_001010 golden-master delta (pre-T4 corpus). DONE.

**Item 2 (Phase 3 adapter, § 1):** NEW module `spatial_gauntlet/spatial_resolver_adapter.py` (kernel READ-ONLY caller-side re-point — builds resolver inputs, consumes the damage FLOAT, geometry neutralized to single_target per hit so spatial targets_hit is the sole multi-target model). `SpatialEntity` gains `combatant_state`+`resolver_skills`; `entity_from_class_dict(...,*,player_class=None)` / `entity_from_monster_dict(...,*,monster=None)` thread full objects (production) or build a defaulted projection from the export dict (harness/smoke — export corpus does NOT round-trip `PlayerClass.model_validate`, verified empirically). `_apply_skill_damage` + `run_spatial_fight` + `ConvergenceUsageMode.run_slot` + `_run_spatial_slot` threaded. `SPATIAL_DAMAGE_SCALE` 4.0→**0.6** (Disc #24 single-param sweep; empirical correction Disc #11 — measured r_eff>1, opposite the note's first-order sign because the ×500→magnitude base swap dominates mitigation). DONE.

**Item 3 (vestigial-ontology charge, § 3):** (a) new surface names substrate-truthful, not legacy ontology; (b) NO new required-native kernel-schema field; (c) threaded fields (archetype NAME-ONLY / range_profile BENIGN-default / energy_type as-is, no new value) match register rows. Compliance documented in MIGRATION.md v1.65 + Gate-2 handoff § 4. DONE.

**Item 4 (Phase 4 validation, § 4):** 27/27 spatial structural tests PASS. Golden master re-captured at SDS=0.6 (new commit-grade oracle; self-verify 0/60 — bit-stable; pre-re-point oracle preserved git `5a7b079`). Saturation 95%→65%. 21 WR DOWN + 1 UP (mini_boss::class_0009, § 2.1-predicted) + 38 same; ZERO STOP. Geometry negative-contract HELD (4/60 dominant_geometry changes all TTK-explained). Cost re-check: matched-fight-length 3.41ms (below baseline); raw SDS=0.6 27.9ms=4.8× is fight-length driven; §5 re-measure trigger fires on raw, driver documented. DONE.

**Artifacts:** math note §10/§11 actuals; MIGRATION.md v1.65 (NO cross-seam telemetry schema change); AGENT_STATE.md updated; Gate-2 handoff `gamora/notes/2026-06-12-spatial-repoint-phase-3-4-gate-2-handoff.md`.

**Structural follow-on (out of scope, flagged jack-ryan/KR):** magic_pack saturation is HP-scope (not in MOB_HP_DIFFICULTY_SCENARIOS), not DPS-tunable — separate HP-multiplier-scope decision.

**Smoke-line:** 27/27 spatial structural tests PASS; golden-master self-verify 0/60 (deterministic); 7 pre-existing test_cycle13_wave5_gauntlet_sim.py failures confirmed pre-existing via git-stash (unrelated subsystem; zero new failures).
