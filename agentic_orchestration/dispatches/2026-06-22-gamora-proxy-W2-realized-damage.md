# Dispatch — 2026-06-22 — gamora — proxy W2 (realized damage + targetability/death)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-22 — proxy-combat BUILD authorized.
**Gate-1 REQUIRED before build** (jack-ryan DESIGN-MODE — sim wave). Pickup fires only on Gate-1 ENDORSE.
**Estimated effort:** ~1 wave. **Depends on:** rocket G1/G2 (`rocket/v-proxy-gen-prereqs-1`, Gate-2 PASS) + gamora W1 (`gamora/v-proxy-W1-allegiance-spawn-1`, Gate-2 PASS) — BOTH landed and cleared. This is the cross proper.

> **Parent MASTER:** `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`. Read it for the full guard set + gate plan.

## Acceptance
A positioned ally-proxy FIGHTS: it deals real spatial damage through the existing target-agnostic damage path, it is TARGETABLE by enemies, and it can DIE — and a fighting army makes a **load-bearing fighting contribution on `boss_with_adds`** (the spike proved the fight WORKS; the fight is production-real in W2). **Solo BYTE-IDENTICAL at `proxy_bin=solo` (empty `proxy_decls`).** Magnitudes stay at rocket SCAFFOLD values — W2 wires the FIGHT, W3 CALIBRATES it.

> **Gate-1 carry-item #1 (jack-ryan, fold):** do NOT claim "kills the boss as a real graded build." The spike §5.1-5.4 FALSIFIED a stable graded WR band — at scaffold magnitudes the win/loss is a knife-edge STEP, and the gradable signal lives on the clear-TIME axis. W2's acceptance is "the fight WORKS and is load-bearing," NOT "the boss is a stable graded outcome." **The stable graded-band shape is the W3 encounter-model call, pre-cleared to gandalf — do NOT back-door it into W2.**

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
- [ ] **Death.** A proxy whose `hp ≤ 0` is removed from the live world set (reuse the existing mob-death path; no special-cased proxy death). **Gate-1 carry-item #3 (find-by-content anchor):** the death pattern is `e.hp <= 0 → is_alive = False` (~`spatial_engine.py:2245-47`, find by content) + the existing `_step_proxy_population` death/fission handling — reuse it, do not add a parallel proxy-death branch.
- [ ] **Gate-1 carry-item #2 (LOAD-BEARING — declare the `aggro_fraction` semantic, W1-style decoupling).** The load-bearing W2 semantic shift is `aggro_fraction` → spatial re-target SHARE (spec §8.1), and the spike left the spatial mob-RETARGET half UNTESTED. You MUST (a) declare the specific `aggro_fraction` shift in your math note, AND (b) state EXPLICITLY whether W2 implements the spatial mob-retarget (enemies actually re-path/re-aim onto proxies) OR keeps the attrition-share model and DEFERS spatial retarget to W3 — the same conscious nav/attack decoupling W1 did. **Either choice is acceptable; it MUST be declared, not left implicit.** Do not let an undeclared retarget model pass into W3's calibration as a hidden assumption.
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
#1 math-before-code (cite code locations), #3 seed hygiene (FRESH disjoint base — prior through 50,000,017; use 51M+ and record it), #11 empirical inspection (prove the army fights + kills via fixture; prove solo byte-identical), #12 semantic-shift (declare the realized-damage semantic shift — proxies go from positionless contribution-only to real fighting entities — AND the specific `aggro_fraction` → spatial re-target SHARE shift per carry-item #2, including the explicit retarget-vs-attrition-share decision).

## Report back to knight-rider
Confirmation the ally-proxy deals realized damage + is targetable + can die (with fixture evidence — a fighting army vs a boss), confirmation G-CONSTRAINT honored (realized path not COUNT-gated), the 6-spawner-field validation result (WARN-1), the G-SOLO byte-identical re-proof, the MIGRATION producer contract for star-lord's field, the seed base, the tag, and any finding that changes W3 calibration or star-lord's telemetry. Flag anything needing Matt or gandalf. This goes through jack-ryan Gate-2 before W3 chains.

---

## Completion record — 2026-06-22 — gamora — DONE (engine commit `a84a395`, tag `gamora/v-proxy-W2-realized-damage-1`, push HELD)

**THE CROSS IS COMPLETE.** A positioned ally-proxy FIGHTS, is TARGETABLE, and DIES — wired as an EXTENSION (no fork). One engine file (`spatial_engine.py`, 254+/42-). Math note FIRST (Discipline #1): `src/reincarnated/simulation/math/proxy-combat-w2-realized-damage-2026-06-22.md`.

**Realized damage + targetable + death (fixture evidence — `scripts/gamora_proxy_w2_realized_damage_SPIKE_THROWAWAY.py`, INJECTED `proxy_decls`, NO bin lifted, NO kit emitted):**
- **REALIZED DAMAGE / fights + kills:** on a 60k `boss_with_adds`, the army WR = **1.000** vs caster-alone WR = **0.000** (same seeds); one-fight `proxy_realized_damage_dealt`(delivered) = **60000.0**, boss_final_hp = **0.0**. The boss dies to ALLY hits where the caster alone times out → the army is **load-bearing** (carry-item #1 acceptance: a load-bearing fighting contribution, NOT a stable graded WR band — that is W3's encounter-model call). Damage routes through the EXISTING target-agnostic `_apply_skill_damage` (`mob.hp` decrements); no new damage engine.
- **TARGETABLE + DIES:** an ally(base_hp=200) interposed against a hard-hitting boss took realized mob damage and DIED — the mob re-pathed (W1) AND now SWINGS (W2) onto the nearest-enemy ally; `ally.hp` decrements through the same `_apply_skill_damage`; death via the EXISTING `hp<=0 → is_alive=False` flip (no parallel proxy-death branch).

**G-CONSTRAINT honored:** the realized step (new ally-attack phase) is gated `if self._positioned_allies:` (W1's `proxy_decls` set), NOT the COUNT instrument's `if self._track_proxy_population and self._proxies:` — that gate is UNTOUCHED. A summon-in-from-empty army fights. (d4 proxy-port COUNT-instrument smoke 6/6 PASS — the COUNT/CONTRIBUTION instrument is undisturbed, G-COUNT≠CONTRIBUTION.)

**6-spawner-field validation (WARN-1) — CLOSED:** all six decl-LEVEL fields round-trip through gamora's real population spawner: `count`×decl bodies CLAMPED to `proxy_max_active` (count=8/max_active=3 → 3 built, the count wall); `geometry` → engine kernel (aura→circle, melee→point, projectile→line); `duration_s`=2.0 expiry removes the ally at wall-clock; `spawn_cadence_s` gates re-summon; `acquisition="capture"` consumed WITHOUT building G3 (treated as owner-ring conjure — Beast-Taming stays deferred). The seam half rocket couldn't test at G1/G2 is now validated.

**G-SOLO byte-identical re-proof — EXACT.** Reused the W1 multi-behavior fixture pattern: captured the pre-W2 oracle at HEAD `ffea0b4` (git worktree), verified on the W2 tree — signal exact + **1800-tick mob position trace exact** across all 6 nav branches AND the mob attack path. The attack-target generalization degenerates to `[self.player]` in solo (the player is the only non-enemy), byte-identical by the math note §4 theorem.

**MIGRATION producer contract (gamora→star-lord, simulation/MIGRATION.md v1.82):** the field `proxy_realized_damage_dealt = Σ over engine._positioned_allies of ally.delivered_damage_dealt` (V2 overkill-clamped; 0.0 in solo). **SEMANTIC SHIFT star-lord must know:** `SpatialFightResult.player_damage_total` is documented as "player + ALL proxies (proxy term structurally 0)" — W2 makes that proxy term NON-ZERO when a fighting `proxy_decls` is present (always `[]` on real kits today, so production rows are unchanged — but the path is live). gamora RECOMMENDS star-lord keep `player_damage_total` player-only + add `proxy_realized_damage_dealt` as the separate army term (mirrors the `delivered_damage_dealt` split; no existing-consumer value shifts); likely INTERNAL-to-seam (not an export column), per the Wave A2 precedent — final call is star-lord's.

**Carry-item #2 — the `aggro_fraction` retarget-vs-attrition DECISION (LOAD-BEARING, DECLARED):** **W2 implements the FULL SPATIAL MOB-RETARGET** — mobs re-path (W1) AND re-aim (W2) onto the nearest-enemy proxy. This is NOT the attrition-share model; the spike's untested mob-retarget half is now BUILT + PROVEN. `aggro_fraction` is demoted from a lifetime-decay coefficient to a POSITIONING-PRIORITY hint. The COUNT instrument's scalar `aggro_fraction × enemy_dps_est` attrition (`_step_proxy_population`) is UNCHANGED (G-COUNT≠CONTRIBUTION). The W2/W3 mob-aggro boundary is crisp: W2 owns WHETHER the retarget happens (done); W3 owns CALIBRATING how strong the tanking is (the encounter-model death channel that evaporates the army — gandalf's pre-cleared shape).

**Seed base:** `BASE_SEED = 51,000,017` (RECORDED; W1 consumed exactly 50,000,017, cleanly disjoint; next free 52M+).

**Tag:** `gamora/v-proxy-W2-realized-damage-1` (engine commit `a84a395`). **Push HELD** (Mac per-cycle Matt-ask).

**Findings for W3 / star-lord:**
- **W3 calibration:** the realized fight is a clean DPS-race against the 240s timeout with NO ally-death-driven loss channel yet (consistent with the spike's STEP-not-band finding §5.1-5.4). The stable graded-band shape needs the W3 encounter-model death channel (gandalf-owned, pre-cleared): a telegraphed signature slam that EVAPORATES THE ARMY AND THREATENS THE CASTER. W3 calibrates the 4 SCAFFOLD magnitudes (`damage_multiplier`/`base_hp`/`proxy_max_active`/`attack_interval_s`) against that shape — the FIGHT works; the difficulty texture is W3's.
- **star-lord:** the `player_damage_total` proxy-term semantic shift above is the only telemetry impact; the field itself is star-lord's lane.

**No Matt/gandalf escalation needed at this wave:** no locked-decisions conflict, no guard violation, all four guards hold, the load-bearing finding matches the spike. W3 (the calibration + the gandalf encounter-model ruling) is the next wave. Goes to jack-ryan Gate-2 (DEV-MODE) before W3 chains.
