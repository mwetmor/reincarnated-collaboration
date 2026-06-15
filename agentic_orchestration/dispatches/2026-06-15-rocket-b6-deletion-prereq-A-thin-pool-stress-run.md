# Dispatch — 2026-06-15 — rocket — b6-deletion Prerequisite A: adversarial/thin-pool envelope kit_size stress-run

**Status:** 🔥 FIRED — Matt authorized the drive toward b6 deletion 2026-06-15 ("Fire"); jack-ryan Gate-1 CLEAR-WITH-AMENDMENTS (finding `2026-06-15-gate1-rocket-b6-prereq-A-thin-pool-stress-run.md`, amendment folded in below).
**From:** knight-rider
**To:** rocket
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires (Pattern-B discipline).
**Estimated effort:** multi-day (Pattern B)
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` § 2 Prerequisite A; `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quater Decision 2.

## What this is

One of TWO independent prerequisites (A + B) that must BOTH pass before the legacy b6 `ARCHETYPE_TEMPLATES` fallback deletion (Decision 2) may fire. **B (gamora G7 HOLD-SIM) runs in parallel — they are independent.** A single fail on either holds Decision 2; b6 stays. This dispatch is Prerequisite **A** only.

## Acceptance — the design-insurance stress-run

Re-run the kit_size floor gate (recognition record § 4.1 — geometry-only-distinct, mechanic-pool path AST-disabled, the SAME gate definition Phase-2 used) against an **adversarial pool**, NOT the friendly cycle-14 balanced pool the Phase-2 PASS used.

- **Adversarial pool =** deliberately thin physical-weapon coverage + wide bc-cell spread — the degraded-kit cases ("the water_mage 1/29 sin in a new form") that b6 was the safety net for. Construct/select the most hostile physical-weapon pool the substrate can present, not the balanced one.
- **Pass criterion:** the weapon-as-envelope path holds the **10–13** kit_size band — **100% meets-floor, per-cell median ≥10** — under the stressed pool. Geometry-only-distinct is the floor test (role/tier do NOT rescue); report it SEPARATELY from the (geo, role, tier_band) triple, exactly as Phase-2 did.
- **HONEST-FAIL clause (load-bearing):** if the envelope DEGRADES under the adversarial pool (geometry-only-distinct < 10 in any central case), that is a VALID, VALUABLE outcome — it means b6 is exactly the net we'd want to keep, and **Decision 2 does NOT fire.** Report the failure clearly; do NOT force a pass; route to gandalf+KR. Proving the envelope's floor where the net mattered most is the whole point.

## Required reading before starting

- The Phase-2 build + math-note: `weapon_envelope_composer.py`; `src/reincarnated/generation/notes/2026-06-15-weapon-as-identity-phase-2-math-note.md` (§8 code-time addendum); the Phase-2 gate harness `scripts/weapon_as_identity_phase2_gate_2026_06_15.py` (re-use/extend it for the adversarial pool).
- Recognition record § 4.1 (THE gate definition) + § 6-quater Decision 2 (why the adversarial pool, not the balanced one, licenses removing the net).
- The b6-deletion prerequisites brief § 2 A + § 4 (anti-patterns: do NOT treat the cycle-14-balanced pass as sufficient).
- The NET-NEW `PHYSICAL_GEOMETRY_PALETTE` (11 melee + 3 ranged-unlock) you authored in Phase-2.
- Disciplines #1 (math-before-code: how the adversarial pool is constructed + why it is genuinely hostile, code-cited), #1.2, #2 / #2.1, #11 (empirical inspection over assumption).

## Scope

- [ ] **Math-note FIRST (Discipline #1)** — define the adversarial-pool construction (what makes it hostile: thin physical-weapon coverage, wide bc-cell spread), code-cited, and the expected floor behavior. **HALT for jack-ryan Gate-1 on the adversarial-pool construction — MANDATORY, not conditional** (jack-ryan Gate-1 amendment: the pool-hostility construction is the load-bearing decision guarding "don't re-run a friendly pool and call it stressed"; it must be validated BEFORE the multi-day run, not only at Gate-2 after). Then HALT for jack-ryan Gate-2 on the result (per brief § 2 A owner line).
- [ ] Construct/select the adversarial physical-weapon pool.
- [ ] Run the § 4.1 floor gate (mechanic-pool path AST-disabled) against it; report geometry-only-distinct separately from the triple.
- [ ] Gate-result artifact (JSON + script) parallel to the Phase-2 one.
- [ ] Report step-3 (coherent-adjacent, NEVER cross-envelope) firing frequency under stress — high frequency here is the elrond pool-growth signal that the physical pool wants expansion before the net is removed.
- [ ] AGENT_STATE.md updated; tag `rocket/v1.x-b6-deletion-prereq-A-stress-run` (seam-prefixed).

## Out of scope

- **NO b6 deletion.** This dispatch PROVES the floor under stress; it does not delete anything. Decision 2 fires only after A AND B pass AND gandalf+Matt give the fire-confirmation.
- **NO L1 changes** (stays proxy-rooted).
- **NO bundling other deferrals** (literal-weapon-root L1, L2 summon, caster-faith § 5 are orthogonal — do not touch).
- **NO push** (Matt-gated).

## Sequence

jack-ryan Gate-1 on this dispatch ✅ CLEAR-WITH-AMENDMENTS → rocket math-note (adversarial-pool construction) → **HALT, jack-ryan Gate-1 on the adversarial-pool construction (MANDATORY)** → rocket stress-run → **jack-ryan Gate-2 on the result** → KR carries A's result toward the Decision-2 both-pass tally. Prerequisite B (gamora) runs independently in parallel.
