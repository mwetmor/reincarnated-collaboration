# Dispatch — 2026-06-15 — gamora — delete the archetype auto-amp; install flag-and-defer

**Status:** ✅ FIRE-READY — jack-ryan Gate-1 (DESIGN-MODE) CLEAR-WITH-AMENDMENTS 2026-06-15 (A1-1, A1-2, CL-1, CL-3-related folded); fire-able on Matt's go.
**From:** knight-rider
**To:** gamora
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** Pattern A→B boundary (likely 1 session; low-risk, sim-internal). Treat as Pattern B if the status touches telemetry/export.
**Parent ruling (STEP 0 — cite throughout):** `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` § 4 (Move 1) + § 7.2 (inert-in-sim discipline).

## What this is — Move 1 of the telegraph/dodge bridge

The balance loop carries a reflex the ruling names as a lie: **tag rogue → detect "underperforms" → inject damage amp to compensate.** It is the automated version of the genre-wrong fix (buff the fragile coordinate with raw stats) and it **masked** the glass-close-ST coordinate's true shape. This dispatch DELETES that auto-compensation and replaces it with **flag-and-defer** — the coordinate is marked `dodge-gated` (viability deferred to the piloted Godot layer), neither auto-compensated nor auto-failed.

This is the move that makes the sim **honest now**, independent of the rest of the bridge. After this lands, the sim should wall glass-close-ST openly and read that walling as "dodge-gated → defer," not "deficient → compensate."

## THE TWO GUARDRAILS (ruling § 4 — non-negotiable)

1. **Delete the AUTO-COMPENSATION only.** Player-chosen damage amp (gear affix, skill choice) is legitimate and STAYS. What dies is the **archetype-tag-triggered, deficiency-detecting, auto-injecting** amp. The trigger is the bug; the mechanic is not. If you cannot cleanly separate the auto-inject path from player-chosen amp, HALT and surface it — do not delete player-amp.
2. **Replace detect→compensate with detect→FLAG-AND-DEFER, NOT detect→fail.** A naive deletion lets the balance loop simply re-fail the coordinate — recreating a dead coordinate by another door. The coordinate needs a **new status**: `dodge-gated` — *viability deferred to the piloted layer; do not auto-compensate, do not fail.* This is a **replacement of a wrong reflex**, not a bare deletion.

## Relationship to in-flight work (KR coordination note — read before scoping)

The **bc-coordinate cutover** (`rocket/v1.3-bc-coordinate-cutover-*`, gamora stage-2) and the **weapon-as-identity** line are actively retiring archetype LABELS from the live path. The auto-amp may already be partially dead or partially routed through the legacy `ARCHETYPE_TEMPLATES` path. **First task: locate the auto-amp and report whether it is live, legacy-only, or already-severed by the cutover.** If already dead, this dispatch collapses to "install the flag-and-defer status + confirm no live amp-injection remains" — report that and proceed to the status work.

## Cross-seam contract change? (Principle 6 gate — KR assessment; gamora resolves)

**Assessment: CONDITIONAL — gamora resolves explicitly (Principle-6 silence = Gate-1 BLOCK).**
- If `dodge-gated` is recorded ONLY in sim-internal balance state (the loop stops compensating/failing, status held in-memory or in a sim-local artifact), **no cross-seam contract change** → state `Round-trip: not applicable because the dodge-gated status is sim-internal and emitted to no shared telemetry/export field.`
- If `dodge-gated` is written to ANY shared boundary — a `fight_log` key, a verdict/season-summary field, a `class_balance_results` column consumed by star-lord export — that IS a cross-seam contract change (ADR-004) → **MIGRATION.md + round-trip smoke** at the gamora→star-lord boundary. Lean: surfacing "viability deferred" in the verdict is *desirable* (the season summary should not report glass-close-ST as a plain failure), so a telemetry field is likely warranted — decide and state.

## Required reading before starting
- STEP-0 ruling `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` (§ 4, § 7.2, § 8) — the spec.
- `agentic_orchestration/gandalf/notes/2026-06-15-rogue-arc-coordinate-confound-reframe.md` (commit b23dce3) — why the auto-amp masked the coordinate; the 40×-stronger-kit-still-walls evidence.
- The auto-amp site: `src/reincarnated/simulation/balance_loop.py` (archetype + amp references) — locate the detect→inject reflex; confirm against the cutover state.
- The cutover context: dispatches `2026-06-14-gamora-bc-coordinate-cutover-stage-2.md`, `2026-06-14-rocket-bc-coordinate-cutover-stage-1.md` — what label machinery is already retired.
- Disciplines #1 (math/decision-note first), #11 (empirical inspection over assumption — verify the auto-amp's actual live path), #12 (semantic-shifting — a status change IS one; document it).

## Math-before-code / decision-note (Discipline #1) — produce FIRST
A balance-loop semantic change (Discipline #12). Before code, document:
1. **The auto-amp's actual live path** — code-cited (file:line): the tag→detect→inject chain, and whether it is live or cutover-severed.
2. **The flag-and-defer state machine** — what `dodge-gated` means operationally: the loop SKIPS auto-compensation AND SKIPS the fail verdict for a dodge-gated coordinate; where the status is set; what reads it.
3. **The Principle-6 resolution** (internal vs telemetry-emitted) — decide + state.

## Scope
- [ ] Decision-note FIRST (Discipline #1); HALT for jack-ryan Gate-1 if the Principle-6 resolution lands on YES (telemetry-emitted) — otherwise proceed.
- [ ] Locate + report the auto-amp's live/legacy/severed state.
- [ ] Delete the auto-compensation path (auto-inject only); preserve player-chosen amp.
- [ ] Install the `dodge-gated` flag-and-defer status (not compensate, not fail).
- [ ] Smoke-test: a glass-close-ST cell run through the loop emerges `dodge-gated` (not amped, not plain-failed); a non-glass cell is unaffected.
- [ ] MIGRATION.md IF Principle-6 resolves YES (else the not-applicable justification).
- [ ] AGENT_STATE.md updated; tag `gamora/v1.x-auto-amp-delete-flag-defer` (seam-prefixed).

## Acceptance criteria
- [ ] No archetype-tag-triggered auto-amp injection remains in the live balance path (code-cited proof).
- [ ] Player-chosen amp (gear/skill) demonstrably unaffected.
- [ ] A glass-close-ST cell resolves to `dodge-gated` — walls honestly, is NOT auto-compensated, is NOT recorded as a plain balance failure.
- [ ] **Deletion-inert guard (A1-2, jack-ryan Gate-1):** a non-glass, never-amped cell produces an IDENTICAL converged result pre/post deletion — the auto-amp deletion is inert for cells it never touched (no perturbation of the loop's iteration/convergence path). This is the §7.2 honesty proof at the deletion site, mirroring dispatch 3's "changes NO existing balance result" guard.
- [ ] Round-trip smoke: <fixture + boundary + field-presence check> OR `Round-trip: not applicable because the dodge-gated status is sim-internal.` — gamora resolves per the Principle-6 gate.

## Out of scope (explicit non-goals)
- **NO telegraph combat-model work** — that is the separate critical-path dispatch (`2026-06-15-gamora-telegraph-combat-model.md`). Do not start it here.
- **NO b6 deletion** (separate downstream move; gated on the role-floor G7 re-pass + gandalf+Matt confirm).
- **NO modeling the dodge in the sim** (§ 7.2) — the sim must STILL wall glass-close-ST. This dispatch only stops the FAKING; it does not add survivability.
- **NO push** (Matt-gated).

## Sequence
jack-ryan Gate-1 on this dispatch → gamora decision-note (→ Gate-1 only if telemetry-emitted) → implement → jack-ryan Gate-2 → lands independently (does not block the critical path; makes the sim honest immediately).

## References
- STEP-0 ruling § 4, § 7.2, § 8; reframe doc b23dce3; battle-room spatial twin `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (the invariant-discipline pattern this chain mirrors).
