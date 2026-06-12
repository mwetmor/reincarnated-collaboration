# DEFENSIVE_TRADEOFF Reinstatement — Shadow+Holy Immunity + Mana Shield Gate

**STATUS:** DESIGN RULING CAPTURED — Matt-authorized 2026-06-12 (Pattern B session)
**Author:** gandalf
**Routing:** jack-ryan (decisions-log entry; doc 47 amendment); gamora Phase 3/4 dispatch (shadow+holy extension); KR (dispatch authoring); gamora (enemy elemental coverage dispatch, separate); rocket (mana shield skill + gate condition — gated on T4 architecture session)

---

## 1. The ruling (Matt, 2026-06-12)

**DEFENSIVE_TRADEOFF is reinstated** to the T4 strategy catalog with three amendments:

1. **Shadow+holy immunity** — `t4_chaos_immune` grants immunity to BOTH shadow AND holy damage (not shadow-only). Rationale: Reincarnated has 7 damage types (5 elements + shadow + holy); shadow-only = 1/7 ≈ 14% coverage, too thin to justify the tradeoff. Shadow+holy = 2/7 ≈ 29% — comparable to PoE CI's coverage ratio. Paired-luminance symmetry (shadow/holy already treated as a paired axis in the resistance matrix) makes the pairing architecturally coherent.

2. **Gate condition — mana energy type required** — DEFENSIVE_TRADEOFF can only be assigned to kits with `energy_type == "mana"`. Rage, combo, focus, and stamina-as-resource kits cannot take this strategy; their resource pools serve different purposes and there is no mana shield defensive layer to fund.

3. **Gate condition — mana shield skill required** — DEFENSIVE_TRADEOFF can only be assigned to kits that have mana shield in their skill list. Mana shield is the defensive layer: the mana pool absorbs incoming damage, creating a dual-purpose resource tension (offense: cast skills; defense: absorb hits). The tradeoff is this constant mana allocation tension, not a literal HP reduction.

**Mana shield behavior specifics DEFERRED** to the pending T4 architecture session (chains-within-trees design). Implementation of the mana shield skill (rocket seam) and combat mechanic (gamora seam) gates on that session.

---

## 2. Root cause annotation — why Phase 4 removed it

Doc 47 § 4.6.2 marks DEFENSIVE_TRADEOFF as "REMOVED per Matt D3 (no chaos encounter signal)." That removal decision is retained as accurate for the Phase 4 context, but the root cause was measurement contamination, not mechanic invalidity:

**Contamination source 1 — Enemy elemental coverage gap**: gauntlet enemy mobs did not have meaningful representation across all 7 damage types. A kit with shadow+holy immunity was fighting in an environment where the covered damage types never appeared. The immunity fired zero times → zero differential → appeared worthless.

**Contamination source 2 — T4-aware gear equipping absent**: a DEFENSIVE_TRADEOFF kit equipping identically to a non-tradeoff kit pays the opportunity cost (T4 slot) without the compensating upside (mana-optimized gear enabling damage investment). It appeared as a net negative.

**Amendment to doc 47 § 4.6.2 note:** add annotation — "Removed due to contaminated test conditions (enemy elemental coverage gap + T4-aware gear equipping absent), not mechanic invalidity. Reinstated 2026-06-12 with shadow+holy coverage + mana shield gate — see this note."

---

## 3. Two new algorithmic requirements (Matt, 2026-06-12)

These emerged from diagnosing the Phase 4 measurement failure. Both are new dispatch items.

### 3.1 Enemy elemental distribution algorithm (gamora + generation seam)

The gauntlet must guarantee meaningful coverage across all 7 damage types in enemy encounter pools. An evaluation suite that cannot pressure a kit's elemental immunities cannot measure their value. Composition rule needed: minimum representation weight per damage type in the encounter pool for any complete T4 evaluation run.

**Scope:** gauntlet / spatial gauntlet enemy kit construction. Gamora seam for simulation-side enforcement; rocket seam for generation-side skill distribution. Separate dispatch — does not block Phase 3/4.

### 3.2 T4-aware gear equipping algorithm (rocket seam, gamora validation)

Kit construction must read the T4 strategy assignment and derive gear priorities from it:

- **DEFENSIVE_TRADEOFF kits**: mana pool/regen first (fuel the mana shield), HP secondary (total buffer), damage where budget allows
- **Other T4 strategies**: corresponding gear priorities TBD in T4 architecture session

This is a "build optimizer" / "gap-fill equipping" layer that currently doesn't exist at strategy-aware resolution. The absence of this layer means any investment-dependent T4 will underperform in evaluation — the Phase 4 catalog narrowing may have undervalued other strategies too (ELEMENT_CONVERSION, RESOURCE_CONVERSION, GEOMETRY_COLLAPSE) for the same reason.

**Scope:** rocket seam (kit construction, gear assignment). Gamora validation (does the T4-gear combination produce the expected combat differential?). Full design in T4 architecture session; this note names the requirement.

---

## 4. Vestigial-ontology register update — energy_type reinforcement

`energy_type` STRUCTURAL-CONSTRAINING status is reinforced by this ruling. It is no longer just a resource management field — it now gates T4 strategy eligibility. A substrate-emergent resource archetype beyond the current five (mana, rage, combo, focus, stamina-as-resource) would require:
- `_ENERGY_CONFIGS` table edit (existing constraint)
- DEFENSIVE_TRADEOFF gate condition update (new coupling)

Register row for `energy_type` should note both constraints explicitly. The kernel-change protocol (§ 3 of the forward-architecture contract) applies to any energy_type addition.

---

## 5. Implementation routing

| Item | Seam | Blocks on | Priority |
|---|---|---|---|
| `damage_resolver.py:324` shadow → shadow+holy | gamora | nothing — fires in Phase 3/4 dispatch | NOW (Phase 3/4) |
| Mana shield combat mechanic | gamora | T4 architecture session | AFTER session |
| Mana shield skill (pool entry, energy_type gate) | rocket | T4 architecture session | AFTER session |
| DEFENSIVE_TRADEOFF gate condition in kit construction | rocket | mana shield skill + architecture session | AFTER session |
| Enemy elemental distribution algorithm | gamora + rocket | separate dispatch | QUEUE |
| T4-aware gear equipping algorithm | rocket (gamora validation) | T4 architecture session | AFTER session |
| Doc 47 § 4.6.2 annotation + reinstatement | jack-ryan (canonical write) | this note | NOW |
| Decisions-log entry | jack-ryan | this note | NOW |

---

## 6. T4 architecture session scope additions (from this ruling)

The pending T4 skill-profile design session (chains-within-trees) now additionally owns:
- Mana shield behavior: absorption ratio, damage type coverage (all elements? elemental only? shadow+holy excluded since immune?), depletion behavior (spill to HP vs full exposure), passive vs active vs always-on
- Mana shield combat mechanic spec (gamora implementation contract)
- Full T4-aware gear equipping algorithm design
- DEFENSIVE_TRADEOFF downside mechanism confirmation (opportunity cost only, or explicit stat penalty?)

**Author:** gandalf, 2026-06-12. Matt-ratified ruling; mana shield behavior deferred to T4 architecture session per Matt direction.
