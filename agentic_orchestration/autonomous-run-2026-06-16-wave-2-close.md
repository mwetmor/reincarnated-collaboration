# Autonomous run 2026-06-16 — Wave 2 CLOSE (knight-rider)

**Charter:** `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md`
**Wave 2 scope (per charter):** the representative-loadout KEYSTONE — gandalf contract → rocket gear → gamora node-wire.
**Disposition:** CLOSED on its **determined ~90% slice** (contract §7.3). Both halves Tier-1 ADDITIVE, two-witness gate clean (jack-ryan Gate-2 PASS-WITH-INFO + gandalf ENDORSE), production-inert. The **live integration parks** (gated on the §6 set-bonus magnitude ruling — Matt's single open design call). No Tier-2 deletion fired; no gate FAILED; no Matt surface required on gate grounds.

## Why this is the keystone

Generated kits were entering the balance sim on a STOPGAP loadout: investment_points=0 (≈0.35× damage) + synthetic stopgap gear (`compute_balance_gear_stats`, gear_catalog.py:173). The spec'd identity loadout is max-profile node investment (→1.0×) + Legendary-T1 weapon + Tier-1 legendaries + 4-piece Set. Wave 2 builds the REAL gear + node-investment surfaces ADDITIVELY so kits can eventually be MEASURED on their true loadout — the precondition for "do not let a deletion fire on stopgap-loadout evidence." Both halves stop short of the live wire-in (which parks), so no deletion can have fired on the wrong evidence.

## Items

### Keystone-0 — contract (gandalf) — CLOSED (Wave 1.5)
- `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` (`c7b0de5`). §2 node-selection, §3 gear, §6 set-bonus PARK, §7 hooks + §7.3 sequencing.

### Keystone-A — rocket gear materialization (§7.1 steps 1-2) — CLOSED, ADDITIVE
- **Math-note (Discipline #1, before code):** `54e6304` — `generation/math/keystone-gear-materialization-2026-06-16.md`. No new balance constants (assembly over the calibrated Cycle-13 partition pool).
- **Code:** `c4f20f6` — `generation/keystone_loadout_materializer.py`: `materialize_legendary_t1_weapon` (kit's own `selected_weapon` as Legendary-T1 identity surface, weapon-as-envelope metadata preserved), `materialize_measured_loadout` (11-slot Legendary-T1 on the doc-42 affinity matrix, resource-gated, modifier-surface SUM), diagnostic `project_loadout_to_gearstats` (NOT plumbed into sim).
- **Smoke (Discipline #2):** PASS — 11/11 LEGENDARY_T1, cross-resource gate holds, seed-real determinism. AGENT_STATE `6aee023`. Tag `rocket/v-keystone-gear-materialization-1`.
- **Out-of-scope confirmed:** stopgap intact + unreferenced; no balance_loop wire; zero set pieces; no push; no semantic shift.

### Keystone-B — gamora node-wire (§7.2 steps 1-2, staged/flag-gated) — CLOSED, ADDITIVE
- **Math-note:** `76a74a0` — `simulation/math/keystone-max-profile-node-wire-2026-06-16.md`.
- **Code:** `85f5c97` — `simulation/combatant.py`: new kwarg `from_player_class(apply_max_profile_investment=False)` (default OFF → byte-identical production; OFF branch is literally `else player_class.skills`) + helper `_apply_max_profile_investment`. ON → active nodes investment_points=15 (→1.0×), passive=5 (→1.0×), T4 node capped. `model_copy` — originals unmutated.
- **Empirical finding (Discipline #11):** the fight seam has **no boolean `t4_unlocked` gate**; "T4 unlocked" reduces to capping the tier-4 node. gamora declined to invent a parallel mechanism — gandalf judged this faithful + more honest.
- **Smoke:** ALL PASS (OFF≡production honest-not-tautological; ON→1.0× + T4 cap); pytest `test_combat_simulator.py` 23/23 green. AGENT_STATE `4c9592c`. Tag `gamora/v-keystone-node-wire-1`.

### Gate — two-witness, conclusion-free, parallel
- **jack-ryan Gate-2:** both halves **PASS-WITH-INFO**, no BLOCK (`174f7cb`, findings `qa/findings/2026-06-16-keystone-loadout-materialization-gate2.md`). Independently re-verified: rocket determinism seed-real (1337≠9999); resource-gate holds; gamora OFF branch byte-identical with zero callers passing True; p1(15)=p2(5)=1.0; pytest 23/23 re-run. 4 non-blocking INFO.
- **gandalf conformance:** both halves **ENDORSE** (`0fa3c66`, note `gandalf/notes/2026-06-16-keystone-implementation-conformance.md`). Weapon-as-envelope preserved; T4 reduction faithful; §6 + §7.3 respected. Resolved **JC-3** in-lane (count all 11 slots even for 2H — measure-the-ceiling) and noted **P2** already resolved by §2.3.

## Parking lot updated (Wave 2 contributions)
- **§6 set-bonus magnitude (6a generated-aligned vs 6b fixed-reference)** — the SINGLE open design call; Matt's. Gates: set-piece materialization (rocket §7.1 step 3), the live integration, and BOTH Tier-2 deletions (1D-delete cond.5 + b6-delete parity, since both need real-loadout re-measurement).
- **JC-1** (4 set slots → swap at integration) → rides §6.
- **JC-2** (summed 11-slot power vs doc-50 band) → resolved by the empirical re-measure at integration, not a recalibration now.
- **P1** (alteration-channel completeness under the flag) → the live integration; gandalf recorded the T4-coherence criterion (gear-attuned T4 must equal alteration-firing T4 at live measurement).
- **P3** (flip flag default ON) → the live integration itself; needs a decisions-log semantic-shift declaration.
- RESOLVED (removed from parks): JC-3 (gandalf in-lane), P2 (§2.3).

## Integration-dispatch carry-forward (for when §6 lands)
Per gandalf: (1) Matt's §6 ruling FIRST; (2) T4-variant coherence; (3) JC-3 ruling (all 11 slots); (4) empirical re-measure as the gate validating JC-2 + the contract §8 predictions; then consume real gear + flip the flag + re-measure. THAT integration is where cond.5 / b6-parity get measured on real loadouts — the precondition for any Tier-2 deletion.

## Push
Wave-close push pre-authorized by charter. Pushing engine + collab at Wave 2 close.
