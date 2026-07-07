# Dispatch — 2026-07-07 — rocket + gamora — carried_gear shape unification (nesting bug)

**From:** knight-rider
**To:** rocket (emission decl shape) · gamora (combatant read shape) — JOINT, cross-seam
**Approved by:** Matt 2026-07-06/07 (relayed the critique-pair-aligned 5-step sequencing; this is step 2)
**Estimated effort:** small — a shape-unification + round-trip smoke; ~2–3h joint
**Acceptance:** ONE canonical `carried_gear` shape that BOTH the emission-decl path and the gauntlet/pilot builder produce, and that `combatant.py` reads correctly — verified by a round-trip smoke showing a decl-built combatant reads a non-zero `spell_damage_modifier` (currently it gets 0.0).

## Context

gandalf's finding §8.3 (rank-5 defect, commit `9fb3467`) surfaced a latent wiring divergence while closing the caster-ledger bracket:

- The **gauntlet/pilot builder** passes the substrate binding **un-nested**: `carried_gear = {"main_weapon": kit.substrate_weapon_binding}` (`season_generation_pipeline.py:1604-1606`, `_build_real_player_class`), and `combatant.py:893-901` reads `_carried.get("main_weapon").get("spell_damage_modifier", 0.0)` at TOP level → works, the ~90% caster spell pool was live in the pilot.
- The **emission decl path** NESTS it: `gear_representative[main_weapon_key]["substrate_binding"]` (`season_generation_pipeline.py:472`). A combatant built from the DECL carried_gear therefore reads `spell_damage_modifier` at top level and finds nothing → **gets 0.0**.

Today this is masked because the pilot uses the un-nested builder. But gandalf flagged it explicitly: **unify the two shapes BEFORE loot work multiplies carried_gear consumers** — otherwise every future decl-built / loot-built combatant silently loses its weapon spell pool, and the inversion finding (casters depend entirely on this pool for parity) means that's a silent caster nerf to 0 pool.

**This is independent of the bar re-derivation (step 1) and the re-pilot (step 3)** — the pilot path is unaffected by the bug, so step 1 can run in parallel. This dispatch prevents the bug from propagating into loot work.

## Required reading before starting
- `agentic_orchestration/gandalf/notes/2026-07-06-caster-single-target-structural-finding.md` §8.1 (the verified 4-link chain) + §8.3 rank-5 (the two shapes).
- `season_generation_pipeline.py` — `:472` (nested decl shape) AND `:1604-1606` (`_build_real_player_class` un-nested shape).
- `combatant.py:893-901` — the top-level read (`_carried.get("main_weapon")` → `.get("spell_damage_modifier", 0.0)`).
- `substrate_weapon_binding.py:653` — the binding dict carries `spell_damage_modifier` at top level (the canonical source shape).
- `damage_resolver.py:867-874` (spell_pct_pool feed) + `:758-760` (physical pool via gear_set) — so both paths' consumers are understood.

## Math-before-code (Discipline #1)
Not a math dispatch, but document BEFORE editing:
- **(Gate-1 condition 3 — precision) The canonical shape decision, stated precisely so no THIRD shape is minted.** jack-ryan verified the wiring: `combatant.py:893-901` is a **3-key alias or-chain** that resolves the slot dict FIRST, then reads `spell_damage_modifier` off it — the decl bug is NOT a top-level key absence, it is an **extra `substrate_binding` nesting LEVEL** at `season_generation_pipeline.py:472`. **Canonical shape = the binding directly under the slot key** (matching `_build_real_player_class` at `:1604`). Fix the PRODUCER (`:472`) to match the pilot builder; do not touch the reader.
- **(Gate-1 condition 4 — REQUIRED, not optional) Enumerate EVERY consumer of the nested `substrate_binding` wrapper before editing `:472`.** jack-ryan already found TWO beyond the combatant read that read the nested wrapper TODAY and **WILL BREAK if `:472` is un-nested**: the reconstruction reader (`season_generation_pipeline.py:1885-1890`) and the substrate-field validator (`:2308-2322`). These MUST be reconciled to the canonical shape in the same change and round-tripped. Grep for any further `substrate_binding` readers and reconcile all.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**YES.** `carried_gear` is a loadout-boundary dict crossing generation (rocket, `season_generation_pipeline.py`) → simulation (gamora, `combatant.py`). Unifying its shape modifies an inter-seam fixture dict.

**Therefore Acceptance MUST include:** `Round-trip smoke: a decl-path-built player_class → carried_gear → combatant_from_player_class → combatant reads a NON-ZERO spell_damage_modifier for an INT kit (currently 0.0), AND the gauntlet/pilot-path-built combatant STILL reads the same non-zero value (no regression).` **MIGRATION.md REQUIRED** (ADR-004) documenting the shape change at the generation→sim boundary.

## Scope
- [ ] **Decide + document the canonical `carried_gear` shape** (top-level `main_weapon` → binding dict, per the source + reader — confirm).
- [ ] **rocket:** unify the emission-decl producer (`season_generation_pipeline.py:472`) to the canonical shape (un-nest the extra `substrate_binding` level, matching `_build_real_player_class:1604`).
- [ ] **(Gate-1 condition 4) rocket:** reconcile the TWO other nested-wrapper consumers that break on the un-nest — reconstruction reader (`season_generation_pipeline.py:1885-1890`) and substrate-field validator (`:2308-2322`) — to the canonical shape, in the SAME change, and round-trip them. Grep for any further `substrate_binding` readers and reconcile all.
- [ ] **gamora:** confirm `combatant.py:893-901` reads the canonical shape correctly for BOTH producers; the reader is already correct — do NOT touch it (fix producers only).
- [ ] **(Gate-1 condition 5) MIGRATION.md** at the generation→sim boundary (ADR-004) — **UPDATE the EXISTING `substrate_binding` entries in lockstep** (`generation/MIGRATION.md:287`, `simulation/MIGRATION.md:4126-4130`), not just append, or MIGRATION lies about the shape.
- [ ] **Round-trip smoke** (below) — decl-built AND pilot-built combatants both read non-zero spell pool.
- [ ] Emit-side + sim-side smoke GREEN; regression clean (the pilot path must NOT change behavior — it was already correct).
- [ ] AGENT_STATE.md updated (both seams).
- [ ] Tags: `rocket/v-batch2-carried-gear-shape-1` + `gamora/v-batch2-carried-gear-read-1` (or joint per your coordination).

## Acceptance criteria
- [ ] ONE canonical `carried_gear` shape produced by BOTH the decl path and the gauntlet/pilot builder.
- [ ] Decl-built INT combatant reads non-zero `spell_damage_modifier` (was 0.0). Concrete regression proof of the fix.
- [ ] Pilot/gauntlet-built combatant STILL reads the same non-zero value — NO regression on the already-correct path.
- [ ] **(Gate-1 condition 4) Reconstruction reader (`:1885-1890`) + substrate-field validator (`:2308-2322`) reconciled to the canonical shape and round-tripped** — proof they still resolve the binding after the un-nest.
- [ ] Round-trip smoke: decl player_class → carried_gear → combatant → non-zero spell pool for INT; pilot path unchanged; reconstruction + validator paths still resolve. (Principle 6.)
- [ ] MIGRATION.md written + EXISTING `substrate_binding` entries updated in lockstep (`generation/MIGRATION.md:287`, `simulation/MIGRATION.md:4126-4130`) (generation→sim boundary).

## Out of scope (explicit non-goals)
- **NO constant changes** (BASE_SPELL, multipliers, SC-6b values) — this is pure shape unification.
- **NO change to the pilot/gauntlet path behavior** — it is already correct; the fix brings the DECL path up to it. If your canonical-shape decision would change pilot behavior, STOP and flag — that is a regression, not a fix.
- **NO loot-operator work** — this dispatch is the PRE-REQUISITE that makes loot work safe; it does not do loot work.
- **NO caster bar re-derivation or re-pilot** — those are steps 1 and 3 (gamora, separate dispatches). This can run in parallel.
- **NO physical-pool change** — the inversion finding (physical pool fed only by gear_set, empty in pilot) is NOTED but is a design fork for later, not this shape fix.

## Open questions for the agents to resolve
- Are there OTHER carried_gear producers/consumers beyond the two known sites (grep both)? Unify all, or explicitly scope-out with reason.
- Does any decl-built combatant currently exist in a live path (tests, demo, telemetry) that would CHANGE behavior once the pool goes from 0.0 → non-zero? Enumerate and confirm the change is correct-not-breaking.
- Whether the physical `gear_set` path needs any parallel note in MIGRATION.md (it is empty in pilot but the inversion finding makes it design-relevant).

## References
- gandalf finding §8.1/§8.3 (`9fb3467`); gamora ledger `79796e2`
- ADR-004 (MIGRATION), Principle 6 (round-trip smoke), Discipline #1 (math/design-before-code), #11 (attribution)
- Batch-2 build tags (context for the emission/consume shape): `rocket/v-batch2-legB-economy-emit-1` (`9eca04c`), `gamora/v-batch2-legB-economy-consume-1` (`7e1a5d1`)

---

## Completion record
<!-- rocket + gamora append on completion -->

### rocket — 2026-07-07 — STOP-and-FLAG (no in-seam edit; re-scope to star-lord)

**Outcome:** dispatch NOT executed as written. The named fix (`season_generation_pipeline.py:472` un-nest) is founded on a false premise. Flagging per OP §3.1 + the dispatch's own STOP clause. NO code change, NO tag, NO qa/pending submission (nothing to review — there is no correct in-seam edit).

**Canonical-shape finding (Discipline #1 design-before-code, Discipline #11 empirical):** `gear_representative` and `carried_gear` are TWO DISTINCT structures with TWO DISTINCT correct shapes — NOT one dict at different nesting depths:
- `gear_representative.main_weapon` = a full 10-field gear-slot entry (verified against actual phase2 JSON: `gear_instance_id, slot, rarity, partition_modifiers, capability_modifiers, t4_annotation, set_bonus, set_bonus_rank, is_unique, triggered_passive`), with the binding attached as sub-key `substrate_binding` BY DESIGN (to avoid colliding with the 10 slot fields). Nested-on-purpose.
- `carried_gear.main_weapon` = the binding DIRECTLY (canonical, documented in `generation/MIGRATION.md:325` + `simulation/MIGRATION.md:4126-4130`; produced by pilot builder `:1604`; read by `combatant.py:893-901`).

**All consumers enumerated (Gate-1 condition 4):**
- `season_generation_pipeline.py:472` (producer) — CORRECT. Nests binding onto the gear-slot entry by design. Un-nesting would collide binding fields with slot fields and break downstream.
- `season_generation_pipeline.py:1885-1890` (reconstruction reader) — CORRECT. This is the BRIDGE: pulls `substrate_binding` OUT of nested `gear_representative` → `KitCandidate.substrate_weapon_binding` (`:1926`) → `:1604` re-wraps FLAT into `carried_gear`. The JSON-decl → combatant round-trip already produces correct flat carried_gear.
- `season_generation_pipeline.py:2308-2322` (validator) — CORRECT. Validates the nested `gear_representative.main_weapon.substrate_binding` (11+ fields) — the right structure to validate.
- `export/cycle14_unified_bundle_emitters.py:545,571` (weapon-descriptor emitter, STAR-LORD seam) — reads BOTH `.get("substrate_binding")` AND slot-level `.get("gear_instance_id")`. Would BREAK on an un-nest. Not named in the dispatch; found by grep.
- `combatant.py:893-901` (reader, gamora seam) — CORRECT (per dispatch). Untouched.

**The ACTUAL defect (star-lord's `export/` seam):** `export/cycle13_normal_season_export.py:367-378` `_derive_carried_gear(char_data)` returns the whole nested `gear_representative` verbatim as `carried_gear` → persisted to `classes.carried_gear` TEXT (`recorder.py:1211-1222`) → read back (`season_exporter.py:725`) → combatant reads `.get("main_weapon")` = slot dict → `.get("spell_damage_modifier")` = absent → **0.0**. Fix = flatten `main_weapon.substrate_binding` up to `carried_gear["main_weapon"]` in that ONE export function, matching `:1604`.

**MIGRATION:** no lockstep edit needed. `generation/MIGRATION.md:325` + `simulation/MIGRATION.md:4126-4130` already document the two-shape contract accurately (`carried_gear` = flat `{"main_weapon": ...}`; `gear_representative` = nested slot-entry + `substrate_binding` sub-key). If anything, star-lord adds a note that `_derive_carried_gear` must flatten.

**Inversion finding:** unaffected by this shape issue; remains a later design fork (gandalf §8.2/§8.4). Not acted on.

**Artifacts:** design note `agentic_orchestration/rocket/notes/2026-07-07-carried-gear-nesting-STOP-flag.md` (commit `b3e5658`, collaboration repo); AGENT_STATE checkpoint (commit `6811239`, engine repo). Routed to knight-rider for re-scope to star-lord.

**Recommendation to knight-rider:** re-scope the fix to star-lord — `export/cycle13_normal_season_export.py:_derive_carried_gear` transforms nested `gear_representative.main_weapon.substrate_binding` → flat `carried_gear["main_weapon"]`; round-trip smoke: DECL char JSON → `_derive_carried_gear` → combatant reads non-zero `spell_damage_modifier` for INT; pilot path unchanged. gamora's confirm-only role stands (reader is correct).
