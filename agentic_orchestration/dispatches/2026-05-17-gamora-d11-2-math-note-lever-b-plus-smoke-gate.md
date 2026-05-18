# 2026-05-17 — gamora — D11.2 math note: Lever B (kit-aggregate DPS-density uniform scaling) + Discipline #17 empirical-calibration smoke gate

**Authority:** Matt L3 D11.2 authorization 2026-05-17 + gandalf D11.2 structural-redesign advisory verdict (LEVER B recommended; smoke-gate mandatory Phase A).
**Type:** Pattern B — math note authoring + algorithm spec + smoke-gate procedure; ~1-2 hours.
**Predecessor (now complete):** gandalf D11.2 structural redesign advisory at `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (524 lines).
**Status:** 🟢 **ACTIVE — fire immediately per gandalf handoff.**

---

## Why this matters

D11.0 missed (6% convergence). D11.1 missed worse (0% convergence; dual-mode failure). D11.2 is the structural retry. Gandalf advisory verdict: **Lever B — uniform `scale_factor` on `damage_multiplier` across all damage-bearing skills in hybrid_mage kits, applied at kit finalization, with magnitude deliberately deferred to a smoke gate (Discipline #17 proposed).**

This is the durable correction to the D11 cycle's repeated magnitude-by-analogy failures: instead of projecting "α=0.07 should give 50% convergence" without empirical seed, we run a 3-point sweep at low / mid / high anchor values, measure WR-at-floor against fixed monster gauntlets, pick the smoke-passing value, then full-regen.

Your job: formalize the algorithm + the smoke gate procedure as a math note. Rocket implements; jack-ryan Gate-1's; rocket smoke-runs; full salvage on smoke-pass.

---

## Required reading

1. **Gandalf D11.2 advisory** — `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (524 lines; lever rationale; identity preservation; retire clause; Discipline #17 proposal)
2. **D11.1 math note** — `reincarnated-engine/src/reincarnated/simulation/math/d11-1-ceiling-primary-tuning.md` (your prior; predecessor to D11.2)
3. **D11 math note** — `reincarnated-engine/src/reincarnated/simulation/math/d11-hybrid-mage-tuning.md`
4. **D10 math note** — `reincarnated-engine/src/reincarnated/simulation/math/d10-substrate-coherent-generation.md` (canonical kit-finalization seam)
5. **balance_loop.py** — `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (convergence math; floor-pin behavior; recompose vs full-regen)
6. **B14.5 V1 primary loop architecture** — `engineering-disciplines.md` (recompose-first + hybrid rejection gate + adaptive quick-estimate + smoke-test mode)
7. **D11.0 → D11.1 empirical deltas** — extract from rocket completion records + your prior math notes (WR-elasticity reference: ≈ 0.5-1.0% WR per 1% damage-skill-DPS reduction)

---

## Scope — math note authoring

### Part 1 — Algorithm spec for Lever B

Formalize the algorithm:

1. **Where applied:** at kit finalization in the hybrid_mage substrate-coherent generation pipeline (post-skill-selection, pre-balance-loop). Specific function name + line number target for rocket.
2. **What's scaled:** `damage_multiplier` field on every skill in the kit where `dps_score > 0` (i.e., damage-bearing skills only; non-damage skills like sustain/utility are NOT scaled — they have `dps_score == 0` and scaling them is a no-op anyway; verify the predicate is robust)
3. **Scale factor:** single uniform `scale_factor ∈ [0.55, 0.75]` (per gandalf advisory anchor band). One value applied to all damage-bearing skills in the kit; not per-skill, not per-element, not per-instance — kit-uniform.
4. **Triggering scope:** ONLY `hybrid_mage` archetype. Other archetypes unaffected. Predicate: `archetype == "hybrid_mage"`.
5. **Salvage path:** when re-salvaging the 17 existing hybrid_mage instances (002011-015 staged seasons), the scale_factor is applied at re-salvage time; no full-regen needed if scale-factor is a finalization step.
6. **Idempotency:** if a class is re-salvaged with `scale_factor=X` after already having been salvaged with `scale_factor=Y`, the math should compose cleanly (or be guarded against double-application). Specify the guarantee.
7. **Composite fallback (B+D):** if smoke fails at upper bound (scale=0.75), composite adds a 5% kit-aggregate HP penalty (multiplier on `max_hp`). Specify formula + application point. This is contingent — not applied by default.

### Part 2 — Discipline #17 empirical-calibration smoke gate procedure

Per gandalf: **3 sweep points × 3-5 instances × ~10-15 min sim cost** before full-regen / full-salvage with a new lever. Formalize:

- **Sweep points:** 3 values from the anchor band — e.g., `[0.55, 0.65, 0.75]` (low / mid / high)
- **Instance count per sweep point:** 3-5 (recommend 5 for tighter signal; 3 acceptable if time-constrained)
- **Instance selection:** representative subset of the 17 hybrid_mage instances — recommend 5 spanning the WR-at-floor distribution (low, mid, high). Specify selection criterion.
- **Sim cost:** ~10-15 min per sweep point; total ~30-45 min for full smoke
- **Acceptance criterion:** smoke passes if **≥3/5 instances at chosen scale escape floor-pin** (WR-at-floor < 0.50 after scale applied). Specify exact threshold.
- **Decision rule:**
  - If `[0.55]` passes ≥3/5 → use 0.55 (minimal identity disruption); proceed to full salvage
  - If `[0.55]` fails AND `[0.65]` passes ≥3/5 → use 0.65; proceed to full salvage
  - If `[0.65]` fails AND `[0.75]` passes ≥3/5 → use 0.75; proceed to full salvage
  - If `[0.75]` fails AND composite B+D passes ≥3/5 → use composite; proceed to full salvage
  - If composite B+D fails ≥3/5 → ESCALATE to Matt with RETIRE recommendation (per gandalf clause)

### Part 3 — Math projection (testable predictions)

Per gandalf empirical anchor (WR-elasticity ≈ 0.5-1.0% WR per 1% damage-DPS reduction):

- For a hybrid_mage instance with current WR-at-floor = 0.65 (mid-range example), scale=0.55 (45% DPS reduction) should drop WR-at-floor by 22.5-45 percentage points → final WR-at-floor ∈ [0.20, 0.425] → escapes 0.50 floor-pin
- For an instance with current WR-at-floor = 0.80 (high-end), scale=0.55 should drop by 22.5-45 pts → final ∈ [0.35, 0.575] → MIGHT not escape if upper-elasticity hits; brittle case for composite

State explicit projections for low / mid / high WR-at-floor instances at each sweep point. These become the empirical comparison anchors when smoke runs.

### Part 4 — Identity-preservation argument

Per gandalf: Lever B does NOT change skill composition, geometry distribution, element coverage, or kit shape — only the per-skill damage_multiplier. The "hybrid_mage" identity (multi-element + multi-archetype layered kit) is preserved; only its raw DPS density is dialed back. Author a short paragraph confirming the identity-preservation rationale (or flagging any ways your math could violate it).

### Part 5 — Backward compatibility + telemetry

- Existing per-class metadata: does the scale_factor need to be persisted (so loadout / demo know what was applied)? Recommend YES; specify field name (e.g., `hybrid_mage_dps_scale_factor`)
- Telemetry: star-lord seam — recommend adding a column to ClassBalanceResult (or similar) capturing the scale_factor used per instance. Task #119 already pending; bundle this in.
- MIGRATION.md entry: cross-seam impact (kit finalization adds new field); requires entry per ADR-004

---

## Acceptance criteria

- [ ] Math note authored at `reincarnated-engine/src/reincarnated/simulation/math/d11-2-lever-b-and-smoke-gate.md`
- [ ] Algorithm spec complete (Parts 1-5 above)
- [ ] Discipline #17 smoke-gate procedure formalized (sweep points, instance selection, acceptance criterion, decision rule)
- [ ] Testable predictions stated (low / mid / high WR-at-floor at each sweep point)
- [ ] Identity-preservation argument included
- [ ] MIGRATION.md draft entry for cross-seam impact
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (heavy concurrent writers — jack-ryan #121 + star-lord scout + drax v1.14 all active)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `gamora/v1.8-d11-2-lever-b-math-note-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT implement the algorithm (rocket seam; next-step dispatch)
- ❌ DO NOT pick the magnitude (smoke gate does that; defer)
- ❌ DO NOT modify balance_loop.py (kit-finalization seam, not balance-loop seam)
- ❌ DO NOT touch other archetypes (hybrid_mage only)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT re-open gandalf's lever choice (Matt-authorized via gandalf advisory)

---

## Coordination

- **Triggers downstream:** jack-ryan D11.2 Gate-1 review (math note + smoke procedure soundness) → rocket D11.2 implementation (algorithm + smoke runner + re-salvage on smoke-pass)
- **Parallel-safe with:** gandalf D11.2 (complete); drax v1.14 (in flight); jack-ryan #121 (in flight); star-lord JSON-parity scout (in flight)
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **Discipline #17 proposal**: gandalf advisory proposed; jack-ryan routed for canonicalization; you reference as "(proposed)" in this math note pending jack-ryan acceptance

---

## Why this completes the D11.2 chain

After this math note → jack-ryan Gate-1 → rocket implementation + smoke runner → smoke decides magnitude → full salvage if smoke-pass → final convergence check. If smoke fails at upper bound + composite, ESCALATE-TO-MATT with RETIRE recommendation. Expected path: Lever B at scale ~0.65 lands convergence in [11/17, 14/17] range; smoke-gate prevents another D11.0/D11.1-style magnitude-by-analogy miss.

---

*Dispatched 2026-05-17 by knight-rider per gandalf D11.2 handoff. ~1-2 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** gamora
**Tag:** `gamora/v1.8-d11-2-lever-b-math-note-1` (local; push gated per ADR-006)

### Deliverables

**Math note authored:** `reincarnated-engine/src/reincarnated/simulation/math/d11-2-lever-b-and-smoke-gate.md`

**MIGRATION.md entry:** v1.11 appended to `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — new `ClassBalanceResult` fields (`hybrid_mage_dps_scale_factor: float = 1.0`, `hybrid_mage_composite_d_active: bool = False`) and new `balance_metadata.hybrid_mage_lever_b` dict; star-lord action required.

**AGENT_STATE.md:** updated to D11.2 complete state.

### Acceptance criteria check

- [x] Math note at `simulation/math/d11-2-lever-b-and-smoke-gate.md`
- [x] Algorithm spec (Parts 1-5 per dispatch scope): application site (Site A, after apply_element_coverage_tax()), what's scaled (_is_damage_bearing() predicate), triggering scope (hybrid_mage only), salvage path (idempotency restore-before-apply), composite B+D fallback formula
- [x] Discipline #17 smoke gate procedure: sweep points {0.55, 0.65, 0.75}, 5 instances with selection rationale, ≥3/5 acceptance, sequential decision rule with composite/RETIRE escalation
- [x] Testable predictions: per-instance WR at each sweep point (central elasticity 0.75% WR/1% DPS); expected path scale=0.65 passes ≥3/5; elasticity derivation confirmed from D11.1 data
- [x] Identity-preservation argument: composition/coverage/geometry unchanged; LE Runemaster lineage; 4-damage-skill boundary check
- [x] MIGRATION.md v1.11 entry: cross-seam impact documented; star-lord action required
- [x] AGENT_STATE.md updated
- [x] Tag `gamora/v1.8-d11-2-lever-b-math-note-1` applied
- [ ] PRE-SIGNAL § 14.1.1 (hive-log append pending; heavy concurrent writers active)

### Key math decisions

**Application site:** Site A (kit finalization), after `apply_element_coverage_tax()` in `d10_kit_constraints.py`. Lever B compounds with the existing element-coverage tax. Combined effective multiplier for 3-element hybrid_mage at scale=0.65: `0.92 × 0.65 = 0.598`.

**Idempotency:** provenance field `balance_metadata.hybrid_mage_lever_b.scale_factor` must be written at every salvage pass. Re-salvage: divide out previous scale before applying new scale. Base state is post-element-coverage-tax `damage_multiplier` values.

**Composite B+D:** Lever D (5% HP penalty) applied at combatant creation in `balance_loop.py` — NOT at kit finalization. Activates only if smoke fails at upper bound (scale=0.55 <3/5). Scale in composite is 0.65 (midpoint) + 5% HP.

**Expected operational path:** smoke passes at scale_factor=0.65 (4/5 instances converge at central elasticity: class_0054, class_0007, class_0029, class_0012 converge; class_0031 at WR=0.867 may not). Full Phase B convergence estimate at scale=0.65: 11-14/17.

### Downstream chain

- **jack-ryan D11.2 Gate-1:** math note review (knight-rider fires)
- **rocket D11.2 Phase A:** implement `_apply_dps_density_scale()` + smoke runner (15 instances × 3 points → `d11_2_smoke_summary.json`)
- **rocket D11.2 Phase B:** full salvage at smoke-selected scale_factor (gated on Phase A pass; ≥10/17 gate at scale=0.65 or ≥12/17 at scale=0.55)
- **ESCALATE to Matt:** if composite B+D smoke also fails ≥3/5 → RETIRE recommendation
