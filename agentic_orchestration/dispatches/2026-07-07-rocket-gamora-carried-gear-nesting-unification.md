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
- The canonical `carried_gear` shape decision (top-level vs nested) and WHY — the binding source (`:653`) is top-level and the combatant reader (`:893-901`) is top-level, so top-level is the lower-churn canonical target. Confirm and record.
- Every current PRODUCER of a `carried_gear` dict (grep) and every CONSUMER (combatant read sites) — so the unification is exhaustive, not just the two known sites.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**YES.** `carried_gear` is a loadout-boundary dict crossing generation (rocket, `season_generation_pipeline.py`) → simulation (gamora, `combatant.py`). Unifying its shape modifies an inter-seam fixture dict.

**Therefore Acceptance MUST include:** `Round-trip smoke: a decl-path-built player_class → carried_gear → combatant_from_player_class → combatant reads a NON-ZERO spell_damage_modifier for an INT kit (currently 0.0), AND the gauntlet/pilot-path-built combatant STILL reads the same non-zero value (no regression).` **MIGRATION.md REQUIRED** (ADR-004) documenting the shape change at the generation→sim boundary.

## Scope
- [ ] **Decide + document the canonical `carried_gear` shape** (top-level `main_weapon` → binding dict, per the source + reader — confirm).
- [ ] **rocket:** unify the emission-decl producer (`season_generation_pipeline.py:472`) to the canonical shape (un-nest, matching `_build_real_player_class`).
- [ ] **gamora:** confirm `combatant.py:893-901` reads the canonical shape correctly for BOTH producers; adjust the reader ONLY if the canonical shape decision requires it (prefer fixing the producer, not the reader, to match the already-correct pilot path).
- [ ] **MIGRATION.md** at the generation→sim boundary (ADR-004).
- [ ] **Round-trip smoke** (below) — decl-built AND pilot-built combatants both read non-zero spell pool.
- [ ] Emit-side + sim-side smoke GREEN; regression clean (the pilot path must NOT change behavior — it was already correct).
- [ ] AGENT_STATE.md updated (both seams).
- [ ] Tags: `rocket/v-batch2-carried-gear-shape-1` + `gamora/v-batch2-carried-gear-read-1` (or joint per your coordination).

## Acceptance criteria
- [ ] ONE canonical `carried_gear` shape produced by BOTH the decl path and the gauntlet/pilot builder.
- [ ] Decl-built INT combatant reads non-zero `spell_damage_modifier` (was 0.0). Concrete regression proof of the fix.
- [ ] Pilot/gauntlet-built combatant STILL reads the same non-zero value — NO regression on the already-correct path.
- [ ] Round-trip smoke: decl player_class → carried_gear → combatant → non-zero spell pool for INT; pilot path unchanged. (Principle 6.)
- [ ] MIGRATION.md written (generation→sim boundary).

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
