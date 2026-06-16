# Finding — 2026-06-16 — keystone-loadout-materialization (Gate-2)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** PASS-WITH-INFO (both halves)
**Target:** Half A `rocket/v-keystone-gear-materialization-1` (code `c4f20f6`, math `54e6304`); Half B `gamora/v-keystone-node-wire-1` (code `85f5c97`, math `76a74a0`)
**Developers:** rocket (Half A), gamora (Half B)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 6 (cross-seam round-trip); Disciplines #1, #2, #4, #11, #12; ADR-004 (MIGRATION), ADR-002 (tiered approval)
**Governing spec:** `~/Games/reincarnated-collaboration/canonical/story/representative-loadout-measurement-contract-2026-06-16.md` (§3, §7.1, §7.2, §7.3, §6 PARK)

---

## Verdict summary

| Half | Verdict | Surface to Matt? |
|---|---|---|
| **A — rocket gear materialization** (contract §7.1 steps 1-2) | **PASS-WITH-INFO** | No |
| **B — gamora node-wire** (contract §7.2 steps 1-2, staged/flag-gated) | **PASS-WITH-INFO** | No |

**Nothing must surface to Matt.** No BLOCK, no failed gate. Both halves are genuinely Tier-1 ADDITIVE, production-inert, and the parked work (set-content §6, live integration §7.2 step 3+, re-measure §7.2 step 5) was correctly NOT performed. Both work items stand.

---

## What I found

Both halves materialize exactly the contract-determined slice and nothing more. I verified additivity, the load-bearing arithmetic, the smokes (re-run from source, not trusted), determinism, the resource gate, and the cross-seam-contract judgment independently — every claim held.

**Half A (rocket).** `keystone_loadout_materializer.py` is a clean sibling of the stopgap: it imports the existing `partition_roller.roll_partition_gear_instance` and `partition_schema`, never `gear_catalog.compute_balance_gear_stats`. I confirmed by grep that the new module has **zero consumers** anywhere in `src/` (only its own AGENT_STATE doc references its functions); the stopgap remains referenced and unmodified at all 5 balance_loop call sites (`:2880, :2939, :3218, :3663, :3810`). No new balance constants are introduced — the only added constant is the `_SEED_SPLAY` mixing value (a deterministic seed-derivation, not a magnitude). Smoke re-run from source: SMOKE PASS (11 slots, all LEGENDARY_T1, identity metadata carried, 9-category coverage, capability + T4 annotation on all slots). I independently confirmed determinism is **seed-real, not constant** (seed 1337 ≠ seed 9999 produce different loadouts) and that the cross-resource gate **actually holds** (rage kit shows only `rage` filter; no mana leak in either direction).

**Half B (gamora).** The flag `apply_max_profile_investment` defaults `False`, and the OFF branch at `combatant.py:560-564` is literally `else player_class.skills` — byte-identical to prior production, no branch taken. Grep confirms **no caller anywhere passes `True`** (only the math-note doc references the signature). The ON path uses `model_copy(update=...)` so originals are never mutated. I verified the load-bearing arithmetic against source: `compute_investment_multiplier_p1(15, m) = m × (0.35 + 0.65·15/15) = m × 1.0` and `pattern_2_passive_multiplier(5) = 0.50 + 0.50·5/5 = 1.0` (`per_skill_emitter.py:225-254, 262-289`; NODE_MAX_ACTIVE=15, NODE_MAX_PASSIVE=5). The Pattern-2 re-bake sets `passive_effect_magnitude = float(base_at_max)` = base_at_max × 1.0 — correct construction property. The smoke OFF≡production check is non-trivially honest (it compares default-call vs explicit-`False` **and** a 30-fight batch win-rate **and** asserts kit-unmutated), and re-ran ALL PASS across 5 generated classes; `pytest test_combat_simulator.py` re-ran 23/23 green. gamora's Discipline-#11 empirical finding (no boolean `t4_unlocked` gate in the fight seam; T4 = capping the tier-4 node + the orthogonal alteration channel) is consistent with the code I read.

---

## Rationale

- **Additivity (Principle 3 / Discipline #12):** confirmed real for BOTH paths — stopgap intact and unreferenced-by-new-code; no balance_loop wire; flag OFF byte-identical (re-read code, not trusted to smoke).
- **Math-before-code (Principle 1 / Discipline #1):** git log confirms both math-notes committed BEFORE their code (`54e6304`→`c4f20f6`; `76a74a0`→`85f5c97`); the load-bearing arithmetic in both notes is cited to code and reproduces exactly.
- **Smoke-gate (Principle 2 / Discipline #2):** both smokes re-run from source and PASS; the gamora OFF≡production claim is true for the right reason (not a trivial tautology).
- **Cross-seam contract (Principle 6 / ADR-004):** correct that **no MIGRATION.md is required now** — there is no downstream consumer of either artifact (materializer has zero callers; flag has zero `True` callers; the GearStats projection is diagnostic-only and not plumbed into any sim call). MIGRATION lands when the §7.2-step-3 integration wires real gear + flips the flag, which is parked. No MIGRATION was touched by either commit; that judgment is right.
- **Out-of-scope respected:** neither agent built the §6 set-pieces, retired the stopgap, consumed real gear cross-seam, re-measured the rogue/gauntlet, made a semantic shift, or pushed. The parks were surfaced, not decided (Discipline #12 "surface, don't decide").

---

## INFO lines (non-blocking; for the record)

- **INFO-1 (Half A, smoke coverage):** the mana-kit smoke's resource-gate assertion ("no rage/stamina") is satisfied *vacuously* for the chosen seed — that kit rolled **zero** resource-filtered modifiers (`resource_filters: []`), so the no-leak check passes without exercising a positive mana roll. The rage kit (`['rage']` only) does demonstrate the filter is real, so the gate is genuinely proven across the pair; but a future smoke seed that produces a non-empty mana filter would make the mana-side assertion load-bearing rather than trivially-true. Not a defect; the gate holds. *Action: optional — pin a smoke seed where the mana kit rolls ≥1 resource modifier when this path is revisited at integration.*
- **INFO-2 (Half A, JC-3 off-hand for 2H):** rocket correctly surfaced (math-note §5 JC-3) that the 11-slot model rolls a `secondary_item` even for a 2H main-hand; whether a 2H weapon should null the secondary at MEASUREMENT is a consumer-side decision. This is a real measurement-semantics question that lands on gamora's §7.2-step-3 wire, not on this materialization. Correctly parked. *Action: gamora to resolve at integration; track as an open measurement-semantics item.*
- **INFO-3 (Half B, passive-branch coverage):** generated kits ship 0 passive nodes, so the Pattern-2 re-bake (3.75→7.5) is exercised via a *synthesized* passive node in the smoke. This is honest and clearly labeled, and the arithmetic is independently correct — but the re-bake has not been exercised on a real generated passive node (none exist to test). Acceptable for a staged/flag-gated additive commit. *Action: none required now; re-confirm if/when generated kits begin shipping passive nodes.*
- **INFO-4 (Half B, smoke environment noise):** the node-wire smoke emits unrelated `derive_spatial_geometry_type: unknown geometry_type=...` warnings and one `DEGRADED mana kit` loud-fail from the generator during kit construction. These are pre-existing generator-side conditions unrelated to the node-wire and do not affect the smoke verdict (ALL PASS). *Action: none — noted so the noise isn't mistaken for a node-wire regression on re-run.*

---

## Action

- [ ] Developer (rocket): no required action. Optional INFO-1 seed-pin and INFO-2 JC-3 carry to the §7.2-step-3 integration.
- [ ] Developer (gamora): no required action. INFO-3 passive-branch re-confirm deferred to when passive nodes ship.
- [ ] Matt: **none.** No BLOCK, no failed gate. Both halves stand under the autonomous-run charter (PASS-WITH-INFO is terminal). The §6 set-content park and the §7.2-step-3 live-integration / re-measure remain Matt-gated as already designed — unchanged by this gate.

## References

- `~/Games/reincarnated-engine/src/reincarnated/generation/keystone_loadout_materializer.py`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/keystone-gear-materialization-2026-06-16.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (`from_player_class` :430; `_apply_max_profile_investment` :389; flag branch :560-565)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/keystone-max-profile-node-wire-2026-06-16.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` (`compute_investment_multiplier_p1` :232; `pattern_2_passive_multiplier` :266; NODE_MAX_ACTIVE=15 :219; NODE_MAX_PASSIVE=5 :53)
- `~/Games/reincarnated-engine/src/reincarnated/generation/gear_catalog.py:173` (`compute_balance_gear_stats` — stopgap, INTACT + unreferenced by new path)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (5 stopgap call sites :2880,:2939,:3218,:3663,:3810 — unchanged)
- `~/Games/reincarnated-engine/scripts/gamora_keystone_node_wire_smoke_2026_06_16.py` (re-run ALL PASS)
- `~/Games/reincarnated-engine/tests/test_combat_simulator.py` (re-run 23/23)
- Governing spec: `~/Games/reincarnated-collaboration/canonical/story/representative-loadout-measurement-contract-2026-06-16.md`
