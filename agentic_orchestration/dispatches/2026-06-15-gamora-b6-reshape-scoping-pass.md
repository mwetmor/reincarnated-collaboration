> ⛔ **SUPERSEDED 2026-06-16 — DO NOT EXECUTE.** Matt RETIRED the b6 archetype processes and the 1D battle sim outright (relayed via gandalf). b6-reshape is moot — b6 is being DELETED, not reshaped; the prove-then-delete / reshape fork is closed. See `2026-06-16-gamora-1d-sim-b6-deletion.md`. Retained as historical record only.

# Dispatch — 2026-06-15 — gamora — b6-reshape scoping pass (per-tier-shape degeneracy characterization)

**Status:** 🔥 FIRED — Matt-authorized 2026-06-15 ("agreed on both" — push + author the reshape scoping-pass dispatch); jack-ryan Gate-1 CLEAR-WITH-AMENDMENTS (finding `2026-06-15-gate1-gamora-b6-reshape-scoping-pass.md`, commit `fdd8057`; amendments A1/A2/A3 folded below — they target the signature math-note and are re-checked at the MANDATORY signature Gate-1).
**From:** knight-rider
**To:** gamora
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** multi-day (Pattern B)
**Parent:** `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quinquies (f) — the caster-path-generalization question, flagged-not-resolved; the named re-open gate behind Decision 2 HELD.
**Disposition this serves (Matt verbatim 2026-06-15):** "Decision 2 HELD — A pass (tight) / B honest-fail (envelope per-tier-shape degeneracy, CELL-4/rogue upper tiers, invariant across two independent runs); b6 stays as the tier-completeness net; **reshape gated on a scoping pass (friendly-pool + other-cell reproduction; caster-path generalization).**"

## What this is — and what it is NOT

This is the **scoping pass** that gates the reshape. It is **diagnostic / characterization only.** It does NOT build the reshape, does NOT modify `balance_loop.py`'s single-global-modifier design, does NOT touch b6, and does NOT delete anything. Its single job: **determine WHAT the per-tier-shape degeneracy actually is**, so the reshape — if it happens at all — is aimed at the right target.

The decisive scoping question (§ 6-quinquies (f)): is the upper-tier collapse an **envelope-specific bug** (the envelope path produces kits the single global balance modifier cannot shape) — OR is it a **property of the shared resource-gated-vocabulary architecture + the balance loop's single-global-modifier design** (in which case it would also affect CASTER kits, and "reshape" means "the balance architecture needs per-tier shape," not "fix the envelope")? The answer changes the reshape's owner, surface, and scope entirely. **This pass answers it before any reshape is scoped.**

## The signature being characterized (from B's HONEST-FAIL)

B's verdict (`gamora/v1.3-b6-deletion-prereq-B-g7-hold-sim-1`, result `output/g7-hold-sim-b6-prereq-B-20260615.json`): on CELL-4 (rogue), the envelope arm over-performs the swarm tier → the single global balance modifier floors to `MODIFIER_SEARCH_FLOOR=0.01` to suppress swarm → upper tiers (elite/mini_boss/boss) crater to 0.0 kills-only WR, while the b6 arm converges (modifier ~0.61) and CARRIES those upper tiers (elite 0.75 / mini_boss 0.667 / boss 0.967 kills-only / magic 1.0). **The envelope has no per-tier shape that ONE global modifier can resolve.** That is the degeneracy. It was invariant across two independent runs.

## The three reproduction legs (Matt-named)

### Leg 1 — friendly-pool reproduction
Re-run the G7 HOLD-SIM degeneracy probe on the **friendly cycle-14 balanced pool** (and a non-harsh power/seed slice — B's smoke slice was 50-power single-seed-per-cell, deliberately harsh; both arms scored 0/5 aggregate there). **Question:** does the CELL-4/rogue per-tier-shape degeneracy (envelope upper-tiers crater while a converging modifier exists for b6) reproduce under realistic, friendly conditions — or was it an artifact of the harsh slice? Note B's verdict explicitly did NOT rest on the harsh-slice aggregate (both 0/5); it rested on per-cell envelope-only degeneracy, asserted robust to the slice. **This leg TESTS that robustness claim under the friendly pool.**

### Leg 2 — other-cell reproduction
B flagged the degeneracy on CELL-4/rogue ONLY (the cell b6 was masking). **Question:** does the per-tier collapse reproduce on cells BEYOND rogue? Extend cell coverage across the physical archetype set (and, for the caster-generalization leg, caster cells). A degeneracy isolated to one cell is a narrow envelope-composition issue; a degeneracy across many cells is structural.

### Leg 3 — caster-path generalization (the load-bearing leg)
Run **existing caster PLAYER kits** through the SAME single-global-modifier per-tier-shape probe. **Question:** do caster kits ALSO exhibit upper-tier collapse when the single global modifier floors to suppress an over-performing tier? Casters share the resource-gated-vocabulary SHAPE (mana gates the vocabulary; the envelope mirrors this). If casters collapse the same way, the degeneracy is **architectural** (the single-global-modifier balance design cannot shape ANY resource-gated kit per-tier), reframing "envelope bug" → "balance architecture needs per-tier shape." If casters do NOT collapse, the degeneracy is **envelope-specific** (the caster composition has a per-tier shape the envelope lacks — find what differs). **This leg is the decisive discriminator.**

**⚠ Gate-1 amendment A2 (caster-kit source — the existing probe has NO caster PLAYER path):** the B harness (`scripts/g7_hold_sim_b6_prereq_B_2026_06_15.py`) tests `_PHYSICAL_ARCHETYPES` ONLY (`:69`); the `"caster"` token in it (`:241`) is an OPPONENT MONSTER, not a player kit under test. Caster PLAYER kits compose through a structurally different path (`archetype_composer.py`, the `*_caster`/`*_mage` mana-gated route) — NOT the envelope composer. So Leg 3 is **not** a friendly "reuse the existing probe": you MUST extend the harness with a caster-PLAYER-kit loader/source, and that caster kit must enter the **identical `balance_class()` probe** (`balance_loop.py:934`) used for the physical arms, so the comparison is apples-to-apples (same loop, same single-global-modifier design, same per-tier bands). **State the caster-kit source explicitly in the math-note.** This caster-loader extension is IN SCOPE (harness-side) — see Scope.

## Acceptance — characterization, not pass/fail

There is no PASS/FAIL verdict here — this is diagnostic. Acceptance = a **clear, evidence-backed characterization** answering the three legs' questions, sufficient for gandalf+Matt to scope (or decline) the reshape:

- A measurable, pre-registered **per-tier-shape degeneracy SIGNATURE** (Discipline #1, below) so "reproduces / does not reproduce" is not a judgment call.
- Per-leg findings: friendly-pool (reproduces? Y/N + evidence), other-cell (which cells? coverage map), caster-path (do casters collapse? the discriminator result).
- A **scoping recommendation** routed to gandalf+Matt: envelope-specific vs architectural, with the evidence that distinguishes them. **HONEST result either way** — if casters collapse too, say so plainly (it is the more consequential finding); do NOT steer toward the convenient "envelope-only" answer.

## Math-before-code (Discipline #1) — FIRST; HALT for Gate-1

**Define the per-tier-shape degeneracy SIGNATURE as a measurable, code-cited criterion BEFORE running anything.** This is the decisive act (exactly as B's "viable fight" criterion was — a soft signature is the steering vector that lets the pass conclude whatever is convenient). The signature must operationalize:

1. **"The single global modifier floors to suppress an over-performing tier"** — measurable: `result.modifier` at/near `MODIFIER_SEARCH_FLOOR=0.01` (`balance_loop.py:318`) AND a low tier (swarm) at/above its ceiling pre-suppression.
2. **"Upper tiers crater while a converging modifier exists for the comparison arm"** — measurable: envelope arm elite/mini_boss/boss kills-only WR collapse (per-tier `< floor`, cite `TIER_FLOORS` `:532-545`, kills-only `:690`) WHILE the b6 arm on the same cell converges (`result.converged == True`, `:1212`) and clears those tiers.
3. **The discriminator for Leg 3 (⚠ Gate-1 amendment A1 — pre-register this with elements-1-2 rigor, NOT as an open question)** — what caster-kit measurement counts as "casters collapse the same way" vs "casters have a per-tier shape the envelope lacks." This is the DECISIVE leg, so it must be the MOST tightly pre-registered, not the softest. Express it in the SAME `balance_loop.py` terms as elements 1-2: e.g. "caster collapses ⟺ on a caster cell where its swarm/low tier is over-ceiling, `result.modifier` floors at/near `MODIFIER_SEARCH_FLOOR=0.01` AND elite/mini_boss/boss kills-only WR fall `< TIER_FLOORS` (`:532-545`, `:690`) — the SAME signature as elements 1-2, just measured on a caster kit." State the pre-registered threshold and the cell-set before running. **The convenient answer is "envelope-only" (it keeps the problem small); the pre-registered, symmetric signature is the anti-steer mechanism — apply B's lesson here exactly.**

**HALT for MANDATORY jack-ryan Gate-1 on the degeneracy-signature criterion before any run.** No run before clearance. jack-ryan will specifically scrutinize the Leg-3 discriminator definition and the caster-kit source at that Gate-1.

## Cross-seam contract change? (Principle 6 gate — knight-rider completed at authoring time)

**Assessment: NO.** This is pure simulation-side characterization: it RUNS the existing `balance_loop.py` G7 HOLD-SIM probe against existing envelope kits (rocket's `weapon_envelope_composer.py`, tag `rocket/v1.3-weapon-as-identity-phase-2`) and existing caster PLAYER kits (via the harness-side caster loader, A2). It adds/modifies/renames/removes NO field on any telemetry table, fight_log dict, loadout dict, or export packet. It does not modify the balance loop, the composer, or any boundary. **Round-trip: not applicable — no cross-seam contract change in this dispatch** (the probe consumes existing shared-Skill-dict kits, the same boundary B already verified clean at `b85d038`). **⚠ Gate-1 amendment (Principle-6, caster symmetry):** the "consumes existing kits cleanly" claim is verified for the physical/envelope arm at `b85d038` — but it must NOT be inherited-by-analogy for the caster arm. Run the field-presence precondition-assert on the caster PLAYER kits SYMMETRICALLY (Discipline #11 — verify, don't assume), not just the envelope arm. Still no MIGRATION.md (read-side either way), but the caster-arm field check is its own explicit assert.

## Required reading before starting
- B's completion record + result: dispatch `2026-06-15-gamora-b6-deletion-prereq-B-g7-hold-sim.md` § Completion record; `output/g7-hold-sim-b6-prereq-B-20260615.json`; harness `scripts/g7_hold_sim_b6_prereq_B_2026_06_15.py` (RE-USE / extend it — same probe, more legs).
- B's viable-fight criterion math-note `src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md` (§1 the locked tier bands, §2 the conjunctive prongs, §3b the absolute per-tier floor that caught the degeneracy) — the signature here EXTENDS that vocabulary.
- `balance_loop.py` — `TIER_FLOORS`/`TIER_CEILINGS` `:532-545`, kills-only semantic `:690`, `MODIFIER_SEARCH_FLOOR`/`CEILING` `:318-319`, `converged` `:1212`, convergence gate `:3249`.
- The caster composition path (Leg 3 subject): how caster kits compose off element × bc_cell — the resource-gated-vocabulary shape the envelope mirrors.
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quinquies (the Decision 2 HELD disposition + (f) the caster-path-generalization flag this pass resolves).
- Disciplines #1 (signature math-note FIRST), #2/#2.1 (smoke subset → characterize before any full sweep; declare resource bounds), #3 (no parallel same-seed regens), #11 (empirical inspection — measure, do not assume the convenient answer), #12 (introduce NO new semantic shift; reuse locked gates).

## Scope
- [ ] **Math-note FIRST (Discipline #1)** — the per-tier-shape degeneracy signature, code-cited (the 3 elements above). **HALT, MANDATORY jack-ryan Gate-1 on the signature criterion.**
- [ ] Leg 1 — friendly cycle-14 pool + non-harsh slice reproduction probe; report reproduces Y/N + evidence.
- [ ] Leg 2 — extend cell coverage beyond CELL-4/rogue; report which cells exhibit the signature (coverage map).
- [ ] **Caster-PLAYER-kit loader / harness extension (IN SCOPE, A2/A3)** — the existing probe has NO caster-player path; extend the harness so caster player kits (composed via `archetype_composer.py` mana-gated route) enter the IDENTICAL `balance_class()` probe as the physical arms.
- [ ] Leg 3 — run existing caster PLAYER kits through the same single-global-modifier probe; report the discriminator result (do casters collapse the same way?) against the pre-registered A1 signature.
- [ ] Cross-seam precondition-assert: sim-consumed Skill fields present on envelope kits AND caster kits SYMMETRICALLY (verify, don't assume — as B did; the caster-arm check is its own explicit assert, not inherited). No MIGRATION.
- [ ] Scoping recommendation (envelope-specific vs architectural) with distinguishing evidence; route to gandalf+Matt.
- [ ] AGENT_STATE.md updated; tag `gamora/v1.x-b6-reshape-scoping-pass` (seam-prefixed).

## Out of scope (explicit non-goals)
- **NO reshape BUILD.** This pass scopes the reshape; it does not implement a per-tier-shape mechanism. The reshape — if scoped — is a SEPARATE downstream dispatch with its own gates.
- **NO `balance_loop.py` modification.** You MEASURE with the single-global-modifier design; you do not change it in this pass. (Whether the loop needs per-tier modifiers is precisely the question this pass FEEDS — it is not licensed to answer it by editing the loop.)
- **NO b6 deletion / no b6 changes.** b6 STAYS (Decision 2 HELD). It is the comparison arm here, untouched.
- **NO generation-side changes** (envelope path + caster path are rocket's seam; you consume their kits, you don't modify composers). **⚠ A3 clarification — what you MAY add:** a HARNESS-SIDE caster-player-kit loader/probe-extension IS in scope (it consumes existing composer output; it does not modify any composer). "Reuse the existing probe" does NOT fence out the harness extension Leg 3 requires — A2 makes that extension mandatory.
- **NO architecture commit / no decisions-log or canonical writes** (those follow the scoping recommendation, via the critique pair + Matt — not in this dispatch).
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- The exact per-tier-shape signature thresholds (the 3 elements above) — pre-register them.
- The Leg-3 discriminator: what caster measurement cleanly separates "architectural" from "envelope-specific." This is the load-bearing definition.
- Slice sizing for a defensible-but-affordable characterization (Discipline #2.1 — declare peak memory + wall-time projection; B's full smoke slice was ~509s; multi-leg multi-cell will be larger — bound it, smoke-subset first).

## Sequence
jack-ryan Gate-1 on this dispatch → gamora signature math-note → **HALT, MANDATORY jack-ryan Gate-1 on the degeneracy-signature criterion** → gamora 3-leg characterization run → **jack-ryan Gate-2 on the characterization** (diagnostic integrity, not pass/fail — confirm the signature was applied honestly and the caster-leg discriminator was not steered) → KR routes the scoping recommendation to **gandalf design-fit (envelope-bug vs architecture-needs-per-tier-shape reframe) + Matt**. The reshape itself fires (or is declined) only after that design call.
