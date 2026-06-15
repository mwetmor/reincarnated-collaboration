# Dispatch — 2026-06-15 — gamora — b6-deletion Prerequisite B: G7 HOLD-SIM sim-validation of envelope kits

**Status:** 🔥 FIRED — Matt authorized the drive toward b6 deletion 2026-06-15 ("Fire"); jack-ryan Gate-1 CLEAR-WITH-AMENDMENTS (finding `2026-06-15-gate1-gamora-b6-prereq-B-g7-hold-sim.md`, amendments folded in below).
**From:** knight-rider
**To:** gamora
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires (Pattern-B discipline).
**Estimated effort:** multi-day (Pattern B)
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` § 2 Prerequisite B; `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quater Decision 2.

## What this is

One of TWO independent prerequisites (A + B) that must BOTH pass before the legacy b6 `ARCHETYPE_TEMPLATES` fallback deletion (Decision 2) may fire. **A (rocket adversarial-pool stress-run) runs in parallel — they are independent.** A single fail on either holds Decision 2; b6 stays. This dispatch is Prerequisite **B** only — the HARD cross-seam gate.

## Acceptance — the G7 HOLD-SIM sim-validation

Weapon-as-envelope-generated physical kits must clear the balance-loop sim-validation on `balance_loop.py` — the existing G7 HOLD-SIM gate the Stage-3b deletion always had to clear.

- **Pass criterion:** envelope kits **sim-validate** — they don't break the balance loop; they produce **viable fights, not floor-test-only artifacts.** Floor-proven (rocket Phase-2 § 4.1) ≠ sim-proven; this gate proves the latter.
- **The point (brief § 2 B rationale):** the b6 deletion does not fire until envelope kits are validated in the SIMULATION, not just at the geometry-count floor. b6 is the live safety net protecting degraded kits today; removing it requires the replacement be sim-safe.
- **HONEST-FAIL clause:** if envelope kits break the balance loop / produce non-viable fights, that is a VALID outcome — it holds Decision 2 and keeps b6. Report clearly; do NOT force a pass.

## Required reading before starting

- `balance_loop.py` — the G7 HOLD-SIM gate; the ARCHETYPE_TEMPLATES imports at lines ~1884 / 1946 / 2025 / 2176 are the cross-seam consumers that make this gamora's hard gate (these stay UNTOUCHED — you sim-validate, you do not delete).
- The Phase-2 build (rocket): `weapon_envelope_composer.py`; commit `137ed25`, tag `rocket/v1.3-weapon-as-identity-phase-2`; gate artifact `output/weapon-as-identity-phase2-gate-20260615.json` (the floor-proven kits you now sim-validate).
- Recognition record § 6-quater Decision 2 (b) Prerequisite 2 (why sim-validation gates the deletion) + the b6-deletion prerequisites brief § 2 B + § 4.
- The cross-seam handoff: rocket's envelope kits land in the SHARED Skill dict (Principle-6 NO new field per Gate-2 `b85d038`) — so they should consume cleanly at the sim boundary; verify field-presence at the boundary.
- Disciplines #1 (math-before-code: define what "sim-validate / viable fight" means as a measurable criterion BEFORE running), #2 / #2.1, #11.

## Scope

- [ ] **Math-note FIRST (Discipline #1)** — define the measurable sim-validation pass criterion ("viable fight" operationalized: win-rate band? fight-length band? non-degenerate damage resolution?), code-cited against `balance_loop.py`. **HALT for jack-ryan Gate-1 on the "viable fight" criterion — MANDATORY** (jack-ryan Gate-1 amendment: the criterion definition is the decisive act; a soft definition is the force-pass vector, so it is validated BEFORE the run).
- [ ] Run envelope-generated physical kits through the G7 HOLD-SIM balance-loop sim-validation.
- [ ] Report PASS / HONEST-FAIL against the operationalized criterion, with the sim metrics.
- [ ] Confirm the cross-seam boundary is clean (envelope kits' shared-Skill-dict fields present + consumed correctly at the sim boundary; no MIGRATION needed per Gate-2 — verify, don't assume).
- [ ] AGENT_STATE.md updated; tag `gamora/v1.x-b6-deletion-prereq-B-g7-hold-sim` (seam-prefixed).

## Out of scope

- **NO b6 deletion** (that is rocket's, downstream, after BOTH gates + Matt fire-confirmation). You do NOT touch `balance_loop.py`'s ARCHETYPE_TEMPLATES imports — they stay until Decision 2 fires.
- **NO generation-side changes** (the envelope path is rocket's seam; you consume its kits, you don't modify the composer).
- **NO L1 / L2 / caster-faith work** (orthogonal).
- **NO push** (Matt-gated).

## Sequence

jack-ryan Gate-1 on this dispatch ✅ CLEAR-WITH-AMENDMENTS → gamora math-note (sim-validation criterion) → **HALT, jack-ryan Gate-1 on the "viable fight" criterion (MANDATORY)** → gamora G7 HOLD-SIM run → **jack-ryan Gate-2 on the result (UNCONDITIONAL — B is the hard cross-seam gate licensing a destructive deletion)** → KR carries B's result toward the Decision-2 both-pass tally. Prerequisite A (rocket) runs independently in parallel. On BOTH-pass → gandalf+Matt fire-confirmation → rocket executes the b6 deletion → jack-ryan Gate-2 on the deletion.
