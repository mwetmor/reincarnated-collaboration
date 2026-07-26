# Dispatch — 2026-07-12 — gamora — element `water` → `ice` (Unit 3 / Wave 2, SIMULATION sub-scope)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt ruling 2026-07-12 (elem-prep §6 EL2); relayed via gandalf KR brief
**Pattern:** B (multi-hour; own session memory)
**Serialization:** **BEHIND the rocket LEAD config pivot.** Do NOT start until `rocket/v2.7-water-to-ice-element-1` has landed the `config/elements.yaml` rename + the shared read-compat normalizer contract in `element/MIGRATION.md`. Read that normalizer contract FIRST and mirror it — do not author a divergent normalizer.
**Estimated effort:** half-day
**Acceptance:** live simulation code speaks `ice`; reads the rocket-authored normalizer (`water`→`ice`) at load; historical artifacts untouched; simulation tests green; `simulation/MIGRATION.md` entry. Tag `gamora/v1.6-water-to-ice-simulation-1`.

## Context

Part of the Matt-ruled `water`→`ice` element rename + cold/frost register (EL2). rocket owns the config pivot, the element load-boundary normalizer, and the generation literals. **You own the simulation-seam literals only.** The mechanic is UNCHANGED — `chill` (soft_control slow) already is the cold/frost ailment; this is a string + register pass, zero behavioral change.

## Binding laws

1. **Census-first** — grep `"water"` across `simulation/` before editing.
2. **Historical artifacts immutable** — telemetry/fight-log rows keep `water`; normalize on read, emit `ice` forward. NEVER retro-edit.
3. **MIGRATION.md** (`simulation/MIGRATION.md`).
4. **Gate-2 (jack-ryan)** before tag.
5. **Auto-commit, no push.**
6. **No scope creep:** NO resistance-value change, NO ailment-parameter change. String + register only.

## Path note

All live code is under `src/reincarnated/simulation/...`. A decoy top-level `./simulation` (`output/` only) exists — ignore it.

## ⚠ Discipline #14 layer exclusion (Gate-1 finding)

`water` lives in two layers. You rename the SUBSTRATE-element layer only (the `resistance_matrix` element KEY, combatant/damage_resolver element literals). If any simulation code references the canonical-four slot-routing tokens (`water_slot`/`VALID_SLOTS` — rocket's `element/selector.py`+`schema.py` seam), LEAVE THEM — they are Discipline #14 internal routing keys and structural emitted-kit keys, not the display element. If ambiguous, flag to KR.

## Known surfaces (anchors — verify against census; brief: simulation 8 literals)

- `resistance_matrix` (⚠ rename the KEY string `water`→`ice`; VALUES/coefficients UNCHANGED — Law 6)
- `combatant`
- `damage_resolver.py`
- `spatial_gauntlet/` (spatial resolver element references)
- simulation test files in the census

## ⚠ E4 overlap note

HEAD `785956c` carries live E4 PHASE-2 cast-state work in `spatial_engine.py` with **Gate-2 pending/held**. Touch ONLY `water` string sites; do not disturb E4 cast-state logic. If the `water` sites are entangled with held E4 code, flag to KR before editing rather than risk contaminating the held E4 build.

## Read-compat normalizer

Do NOT author your own. Read the shared contract from `element/MIGRATION.md` (rocket-authored) and consume it. If simulation reads element strings from persisted fight-logs/telemetry, normalize `water`→`ice` at that read boundary using the same rule.

## Required reading before starting

- This dispatch + the rocket LEAD dispatch (`2026-07-12-rocket-water-to-ice-element-LEAD.md`)
- `element/MIGRATION.md` (the shared normalizer contract — MUST exist before you start)
- KR brief §Unit 3

## Math-before-code

N/A — no numeric change. Smoke: run a simulation smoke proving a fight resolves byte-identically pre/post rename (resistance coefficients unchanged; only the element key string differs).

## Cross-seam contract change? (Principle 6 gate)

The `water`→`ice` element key crosses simulation → telemetry/export (star-lord). MIGRATION.md required. Coordinate the key rename so star-lord's telemetry read side normalizes identically. No new schema field.

## Out of scope

- resistance-value / ailment-parameter changes
- E4 cast-state logic
- generation/config/llm/export literals (other seams)

## Completion record
_(append: census result, normalizer-consumption confirmation, E4-overlap resolution, smoke result, MIGRATION.md path, tag, notes for jack-ryan Gate-2)_

**Completed 2026-07-12 (gamora).** Commit `9b105f6`, tag `gamora/v1.6-water-to-ice-simulation-1` (LOCAL, no push — KR owns wave push). 15 files, +332/−53.

### Census result (substrate-vs-label-vs-slot classification)
Grepped `water` across `src/reincarnated/simulation/`. Live `.py` sites classified into THREE layers (rocket's own `2ae665b` diff is the ground-truth precedent — it renamed substrate-element `dominant_element` literals but LEFT the archetype-label + slot-routing layers):
- **SUBSTRATE-ELEMENT → RENAMED `water`→`ice`:** `resistance_matrix.KNOWN_SUBSTRATES` KEY (+ 2 comments); `phase7_bridge._BC_ATTRIBUTE_TO_ELEMENT["WIS"]` value; `wave5_season_orchestrator._ELEMENT_TO_SCALING` KEY; `balance_loop` element-diversity list; `t4_sim_cycling.ROTATING_ELEMENTS` tuple (+ comment/docstring); `armor_resist_symmetry_phase4_harness` set; comment examples in `damage_resolver.py`/`combatant.py`/`spatial_telemetry.py`; substrate-element values in `notes/leg2_primary_t4_consume_smoke` + `generation/notes/typed_resistance_roundtrip_smoke` (lockstep).
- **ARCHETYPE-LABEL layer → LEFT `water` (lockstep w/ rocket's untouched gen-side labels):** `ai_strategies.py` `ARCHETYPE_ROLE_PRIORITY["water_mage"/"water_controller"]` + `_PLAYER_CONTROLLER_ARCHETYPES`. Opaque archetype keys matched by exact string against the generator-emitted tag (`ai_strategies.py` §2.5: "NEVER reads element/substrate"); renaming sim-side while gen emits `water_mage` = runtime KeyError. Rocket left `water_mage`/`water_controller`/`water_caster` in `mechanic_alteration.py` + `d10_kit_constraints.py` (confirmed via `git show 2ae665b`).
- **Discipline-#14 SLOT-ROUTING layer → LEFT `water` (out of scope):** `test_d2_substrate_coupling.py` `water_slot`/`VALID_SLOTS`/`primary_slot`/`slots["water"]` — rocket's `element/selector.py`+`schema.py` seam.
- Historical rows in `MIGRATION.md` / `AGENT_STATE.md` / `math/*` / `output/*` — immutable (Law 2), NOT retro-edited.

### Normalizer-consumption confirmation
Consumed rocket's shared RULE `elem_rekey_water_to_ice` (`element/MIGRATION.md` [2026-07-12]) — did NOT author a divergent normalizer. Added ONE sim-seam applicator `normalize_substrate()` in `resistance_matrix.py` (`{"water":"ice"}`, else pass-through; display VALUES only, never slot keys). Applied at: `combatant.py` 4 `dominant_element` reads; `damage_resolver.py` substrate guard; `wave5_season_orchestrator.py` 2 `kit.element` reads (2nd = emit path → ice forward); `balance_loop.py` element-diversity match.

### E4-overlap resolution
RESOLVED — no entanglement. `spatial_gauntlet/spatial_engine.py` (Gate-2-held E4 PHASE-2 cast-state) has ZERO `water` sites (grep-verified). NOT touched. Only spatial_gauntlet site is a comment example in `spatial_telemetry.py`.

### resistance_matrix KEY rename + roundtrip-smoke lockstep
`KNOWN_SUBSTRATES` `water`→`ice`; `_MATRIX_OVERRIDES` byte-UNCHANGED (0 water/ice cells; only the 4 luminance holy↔shadow cells non-1.0, untouched); `_LUMINANCE_VALENCE_MAGNITUDE` unchanged. `typed_resistance_roundtrip_smoke` (rocket lockstep flag) rekeyed → 23/23 GREEN. `test_resistance_matrix.py` 21 matrix-KEY assertions rekeyed → 229/229. `test_phase7_bridge.py` WIS→ice → GREEN.

### Smoke result (byte-identity — the load-bearing guard)
NEW `simulation/notes/water_to_ice_byte_identity_smoke_2026_07_12.py`: **7/7 PASS.** F.b proves `dmg_A(ice)==dmg_B(water)==4112.500000` — a fight resolves BYTE-IDENTICALLY whether the ice defender is addressed by the live `ice` key or a historical `water` value the normalizer folds. Also: ice trivial 1.0× row/col; fire→ice==pre-rekey fire→water==1.0; luminance axis untouched.

### MIGRATION.md
`src/reincarnated/simulation/MIGRATION.md` [2026-07-12] — full entry (Discipline #12 declared, two-layer table, normalizer boundaries, star-lord ADR-004 cross-ref, byte-identity guard).

### Notes for jack-ryan Gate-2
1. **PRE-EXISTING rocket-seam breakage (git-stash-CONFIRMED NOT introduced by this wave):** (a) `test_d2_substrate_coupling.py::test_get_valid_slots_with_foundation_returns_registry` — foundation registry now yields `ice` but test expected `water`; rocket's config-pivot gap (NOTE: appears ALREADY fixed in an uncommitted/concurrent rocket edit to that file in the working tree — verify at Gate-2). (b) `test_cycle13_wave5_season_generation.py` 21 ERRORS — `season_generation_pipeline._build_legendary_config` cell-grain byte-identity violation, unrelated to substrate rekey. Both rocket/generation-seam.
2. **Semantic-shift (Disc #12) to ratify:** raw `"water"` is no longer in `KNOWN_SUBSTRATES` → Pattern-P7 fail-loud RAISES unless normalized. Intentional; the normalizer is applied at all sim read boundaries.
3. **Archetype-label + slot layers deliberately LEFT `water`** (lockstep w/ rocket) — verify this mirrors rocket's gen-side exactly; a future full label-layer rename would be a separate cross-seam wave.
4. **star-lord ADR-004 round-trip** (telemetry/export read side, same shared RULE, no new schema field) is the sibling half — verify identical normalization at that boundary.
5. Working tree carries concurrent OTHER-SEAM edits (export/llm/telemetry/output = star-lord); this commit staged ONLY the 15 gamora-seam files by explicit name (no `git add -A`).
