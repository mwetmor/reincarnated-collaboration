# b6 `ARCHETYPE_TEMPLATES` Deletion — Prerequisites Brief (for KR to hold + sequence)

**Type:** sequencing brief (gandalf → knight-rider). The closing-gate half of the 2026-06-15 architecture-commit.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"let's go with option 2"* (the architecture-commit path). Decision 1 committed, Decision 2 sequenced.
**Parent:** `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quater (the architecture-commit) — Decision 2 = b6 deletion, SEQUENCED.
**Lineage:** this IS the concrete prerequisite-set for the long-standing **Stage-3b re-open / b6-deletion closing move** (`agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md`). Stage 3 narrow-deletion HELD the physical fallback to Stage 3b; this brief defines what Stage 3b must clear.

---

## 0. One line

The architecture-commit made the **weapon-as-ENVELOPE** path the canonical physical route (Decision 1, FIRED, additive). **Deleting** the legacy b6 `ARCHETYPE_TEMPLATES` fallback (Decision 2) is the **single destructive move** in this workstream and is **NOT yet fired.** KR holds it as a named closing gate behind **two prerequisites that must BOTH pass.**

## 1. What Decision 2 actually is

Delete the legacy b6 `ARCHETYPE_TEMPLATES` builder (`class_generator.py:636–642` path → `classify_archetype` → label → template) so the weapon-as-envelope path is the **only** physical route — no fallback net beneath it. This is the closing move that finishes the label-deletion the BC-cutover began (Pred 2 closed the smuggle; this removes the last template-fallback machinery).

**Why it is destructive (and therefore gated, not auto-fired):** b6 is the live safety net that protects degraded kits *today* under thin/hostile pools. Deleting it removes that net. Decision 1 deliberately KEPT b6 in the tree precisely so the envelope commit is risk-free; Decision 2 is the deliberate, gated removal.

## 2. The two prerequisites (BOTH must PASS — they can run in parallel)

### Prerequisite A — wider / deliberately-thin-pool envelope stress-run  *(rocket seam; design insurance)*

- **What:** re-run the kit_size floor gate (recognition record § 4.1 — geometry-only-distinct, mechanic-pool path AST-disabled) against an **adversarial** pool, NOT the friendly cycle-14 balanced pool the Phase-2 pass used.
- **Adversarial pool =** deliberately thin physical-weapon coverage + wide bc-cell spread — the degraded-kit cases ("the water_mage 1/29 sin in a new form") that b6 was the net for.
- **Pass criterion:** envelope holds the **10–13** kit_size band (100% meets-floor, per-cell median ≥10) under the stressed pool. Same gate definition as Phase-2; hostile input.
- **Owner:** rocket (generation seam owns the envelope path + harness). **jack-ryan Gate-2** on the result.
- **Rationale:** prove the envelope's floor *where the net mattered most* before removing the net. If the envelope degrades here, b6 is exactly what we'd want to keep — and Decision 2 does NOT fire.

### Prerequisite B — G7 HOLD-SIM sim-validation  *(gamora seam; hard cross-seam gate)*

- **What:** envelope-generated kits clear the balance-loop sim-validation on `balance_loop.py` (the existing G7 HOLD-SIM gate the Stage-3b deletion always had to clear).
- **Pass criterion:** envelope kits sim-validate — they don't break the balance loop; they produce viable fights, not floor-test-only artifacts.
- **Owner:** gamora (simulation seam owns `balance_loop.py` + G7).
- **Rationale:** floor-proven ≠ sim-proven. The b6 deletion does not fire until envelope kits are validated in the simulation, not just at the geometry-count floor.

## 3. Sequencing

1. **A and B are independent — run in parallel.** A is a generation-side floor test on a hostile pool; B is a sim-side validation. Neither depends on the other.
2. **BOTH must PASS.** A single fail holds Decision 2; b6 stays.
3. **On both-pass:** gandalf+Matt give the final fire-confirmation (it is a destructive deletion — a deliberate confirm is appropriate, not auto-fire). Then rocket executes the deletion; jack-ryan Gate-2 on the deletion.

## 4. What NOT to do (anti-patterns this brief guards)

- **Do NOT fire b6 deletion off Decision 1.** Decision 1 committed the envelope as the *route*; it explicitly KEPT b6 as the fallback. The deletion is a separate, gated step.
- **Do NOT treat the Phase-2 cycle-14-balanced-pool pass as sufficient for deletion.** That was the friendly case. Prerequisite A (adversarial pool) is the case that actually licenses removing the net.
- **Do NOT bundle other deferrals into this gate.** Literal-weapon-root L1 (as-time-allows) and L2 summon are **orthogonal** separate workstreams — they do NOT gate, and are NOT gated by, the b6 deletion. Caster-faith § 5 is likewise orthogonal (§ 6-quater (c)).

## 5. Status for KR's tracking

- **Decision 1 (envelope = canonical physical route):** COMMITTED 2026-06-15 (§ 6-quater). Downstream artifacts (ground-state, decisions-log) may record the envelope as the canonical physical route.
- **Decision 2 (b6 deletion):** NAMED · SEQUENCED · NOT FIRED. Held by KR behind Prerequisites A + B.
- **Not blocking anything in flight.** This is a closing gate, not a blocker on current work; it fires when A+B clear.

---

**Signed:** gandalf, 2026-06-15
**For:** the sequenced closing gate of the weapon-as-identity architecture-commit — Decision 2 (delete the legacy b6 `ARCHETYPE_TEMPLATES` fallback) fires only after BOTH a deliberately-thin-pool envelope stress-run (rocket; proves the envelope's kit_size floor under the hostile pools b6 was the net for) AND the G7 HOLD-SIM sim-validation (gamora; proves envelope kits sim-validate, not just floor-pass) clear; until both pass, b6 stays as the live fallback and the Decision-1 envelope commit remains risk-free.
