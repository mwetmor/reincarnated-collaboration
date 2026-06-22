# Dispatch — 2026-06-22 — gamora — proxy W2 (realized damage + targetability/death)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-22 — proxy-combat BUILD authorized.
**Gate-1 REQUIRED before build** (jack-ryan DESIGN-MODE — sim wave). Pickup fires only on Gate-1 ENDORSE.
**Estimated effort:** ~1 wave. **Depends on:** rocket G1/G2 (`rocket/v-proxy-gen-prereqs-1`, Gate-2 PASS) + gamora W1 (`gamora/v-proxy-W1-allegiance-spawn-1`, Gate-2 PASS) — BOTH landed and cleared. This is the cross proper.

> **Parent MASTER:** `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`. Read it for the full guard set + gate plan.

## Acceptance
A positioned ally-proxy FIGHTS: it deals real spatial damage through the existing target-agnostic damage path, it is TARGETABLE by enemies, and it can DIE — and a fighting army kills the boss as a real graded build (the de-risk spike proved YES; W2 makes it production-real). **Solo BYTE-IDENTICAL at `proxy_bin=solo` (empty `proxy_decls`).** Magnitudes stay at rocket SCAFFOLD values — W2 wires the FIGHT, W3 CALIBRATES it.

## Required reading before starting
1. Sim build spec (THE cross design): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-2026-06-21.md`
2. T2.3 de-risk spike (the cross wired as `_step_proxy_population` replacement; what's proven): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/proxy-combat-derisk-spike-2026-06-21.md`
3. Your W1 math note (the nav/attack decoupling you declared — W2 now does the attack half): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/proxy-combat-w1-allegiance-spawn-2026-06-22.md` §5
4. rocket G1/G2 Gate-2 (the `proxies` surface contract + WARN-1): `agentic_orchestration/qa/findings/2026-06-22-proxy-gen-prereqs-G1-G2-gate2.md`
5. rocket's gen MIGRATION (the decl shape you consume): `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (2026-06-22)
6. Parent MASTER (guards + not-unlocked fences): `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`

## Scope
- [ ] **Realized damage.** A positioned ally-proxy deals real spatial damage via the existing target-agnostic `_apply_skill_damage` (decrements `target.hp`). Wire the ally-proxy attack step (the `_step_proxy_population` realized path the spike prototyped — promote it from throwaway to production, reusing `_compute_*_hits` + the damage path; no new damage engine).
- [ ] **Targetability — generalize the ATTACK-target (the site W1 left for you).** The enemy ATTACK target is hard-wired to `[self.player]` at `:2073` (`_select_skill_for_entity`) + `:2082` (`_compute_aoe_hits`) — find by CONTENT (lines shift). Generalize to allegiance-filtered targets so enemies can hit ally-proxies, reusing W1's allegiance helpers. Keep it minimal (extension-not-fork; no aggro-AI fork — nearest-enemy / existing target-selection logic).
- [ ] **Death.** A proxy whose `hp ≤ 0` is removed from the live world set (reuse the existing mob-death path; no special-cased proxy death).
- [ ] **G-CONSTRAINT (packet §5 — LOAD-BEARING).** The realized-damage step MUST NOT be gated behind the COUNT instrument's non-empty check (`if self._track_proxy_population and self._proxies:`, ~`spatial_engine.py:2066` — find by content). A summon-in-from-empty army must fight. W1 already put the solo gate on `proxy_decls`, NOT `_track_proxy_population` — keep that decoupling; do not re-entangle the realized path with the COUNT instrument.
- [ ] **WARN-1 (rocket Gate-2) — validate YOUR half of the seam.** The six decl-LEVEL spawner fields (`geometry`, `proxy_max_active`, `count`, `duration_s`, `spawn_cadence_s`, `acquisition`) are carried by rocket's surface but NOT yet validated against a real consumer (the population spawner is YOUR code, didn't exist at G1/G2). Validate them in W2.
- [ ] **G-SOLO — solo byte-identical at `proxy_bin=solo`** (empty `proxy_decls`). Re-prove (your W1 multi-behavior fixture pattern) that the realized-damage wiring is inert when no proxy is declared.
- [ ] **MIGRATION.md** (gamora↔star-lord, ADR-004) — W2 wires proxy realized-damage; the telemetry field `proxy_realized_damage_dealt` (star-lord, alongside) reads this path. Document the producer contract.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-proxy-W2-realized-damage-N`

## How to TEST a fighting proxy WITHOUT emitting content (critical)
`proxies` is ALWAYS `[]` on real kits (content emission deferred, bin un-lifted). So you CANNOT test the fighting path via a real emitted kit. Test it the way the de-risk spike did: an INJECTED / FIXTURE `proxy_decls` (a populated decl built in the harness, or via `entity_from_proxy_dict` directly). **Do NOT lift `_DEFERRED_PROXY_BINS`. Do NOT emit a proxy kit into a season.** The fixture proves the production CODE PATH works; the content stays gated.

## Cross-seam contract change (Principle 6 — YES, MIGRATION required)
W2 introduces proxy realized-damage that star-lord's additive telemetry field reads, AND consumes rocket's `proxies` surface (round-trip the 6 spawner fields against your real consumer). MIGRATION.md required (gamora→star-lord producer contract + confirming the rocket→gamora consumer round-trip).

## NON-NEGOTIABLE GUARDS (from MASTER)
- **G-SOLO byte-identical** — the shipped solo instrument must not move (empty `proxy_decls` → realized path inert).
- **G-CONSTRAINT** — realized path not gated behind the COUNT non-empty check (above). Load-bearing.
- **G-EXTENSION-NOT-FORK** — reuse `_apply_skill_damage` / `_compute_*_hits` / existing target-selection / existing death path. The allegiance filter is W1's; W2 adds the attack-target generalization + realized step. NO autonomous-AI aggro fork.
- **G-COUNT≠CONTRIBUTION** — the realized fight and the cancelled contribution-selector stay TWO DISTINCT instruments; do not conflate.
- **G-PLAYER-RELEVANT** — `0 < s_baseline < 1` stays enforced; the player is not a spectator.
- **No content emission** — bin stays deferred, no kit emitted (test via fixture).
- **Push HELD** — auto-commit; do NOT push.

## Out of scope (explicit non-goals)
- **CALIBRATION** (boss-grading, magnitude tuning of the 4 SCAFFOLD fields, the encounter-model shape) — that is **W3** (gamora + gandalf). W2 uses scaffold magnitudes as-is and confirms the fight WORKS; it does NOT tune for difficulty.
- **The encounter-model SHAPE** (telegraphed signature slam, build-floor + dodge-ceiling) — design-pre-cleared, **gandalf owns the W3 ruling**. Not W2.
- **The golden-master re-pin** — the pre-existing `season_001010` drift (confirmed NOT W1) is a SEPARATE gamora-owned housekeeping item. Keep it OUT of W2 to preserve the boundary (jack-ryan Gate-2 directive).
- **G3 (Beast-Taming)** — separable, not built.
- The `proxy_realized_damage_dealt` telemetry FIELD itself — star-lord's lane (you document the producer contract; star-lord adds the field).

## Disciplines
#1 math-before-code (cite code locations), #3 seed hygiene (FRESH disjoint base — prior through 50,000,017; use 51M+ and record it), #11 empirical inspection (prove the army fights + kills via fixture; prove solo byte-identical), #12 semantic-shift (declare the realized-damage semantic shift — proxies go from positionless contribution-only to real fighting entities).

## Report back to knight-rider
Confirmation the ally-proxy deals realized damage + is targetable + can die (with fixture evidence — a fighting army vs a boss), confirmation G-CONSTRAINT honored (realized path not COUNT-gated), the 6-spawner-field validation result (WARN-1), the G-SOLO byte-identical re-proof, the MIGRATION producer contract for star-lord's field, the seed base, the tag, and any finding that changes W3 calibration or star-lord's telemetry. Flag anything needing Matt or gandalf. This goes through jack-ryan Gate-2 before W3 chains.
