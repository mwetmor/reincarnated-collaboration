# Dispatch — 2026-05-21 — gamora — W0.5: Mana-bug verify (LC-026)

**From:** knight-rider
**To:** gamora
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); Matt activation dispatch § 4 Step 4 W0.5 listed in P0 roster
**Status:** PENDING — ACTIVE (gamora may execute when launched)
**Estimated effort:** ~2 hours (Discipline #11.1 — empirical inspection; trivially actionable)
**Acceptance:** Mana-bug status documented (resolved / still present / partial); decisions-log entry updated; intermediate tag `qd-rebuild/v0.5-mana-bug-verify`.

---

## Context

LC-026 (jack-ryan legacy constraint audit) carries the mana-bug from 2026-05-08 findings. The dimensional refactor Phase 1 was expected to either fix or expose it. This verify is the QD-rebuild P0's empirical inspection of current state — does the mana-bug persist, was it resolved by some intermediate work, or is it partially resolved?

**Why now:** P0 is the constraint-removal phase. Before P1 substrate enrichment expands the mechanic pool, we need to know whether the mana resource pipeline is structurally sound. If the bug persists, P1 substrate creation that touches resource economy (HP-economy substrate, charge-stack substrate, damage-converts substrate) would inherit the bug — much costlier to fix downstream than now.

## What this dispatch does

### Step 0 — Pull jack-ryan's LC-026 entry from constraint inventory

Read `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` for the LC-026 description + cross-references. Identify the specific failure-mode jack-ryan documented.

### Step 1 — Empirical inspection (Discipline #11.1 in action)

Per Discipline #11.1 (state-space conditioning of empirical signals; ratified 2026-05-21): inspect mana resource pipeline at COLD-START equilibrium, not from pipeline-internal warm states. Methodology:

1. Identify mana-class season (e.g., season_001005 if available; otherwise generate a smoke season under cold-start canonical convergence)
2. Inspect telemetry: `resource_over_time` per fight for mana-classes
3. Check for the originally-documented failure-mode (likely: mana not regenerating between fights / mana counter showing wrong values / mana-cost-not-applied to skills)
4. Cross-check against unit tests in `tests/test_balance_loop.py` or `tests/test_class_generation.py` — what's currently exercised?

### Step 2 — Document the verdict

In your AGENT_STATE.md and a math note under `simulation/math/` (or `simulation/`):

- **Status:** RESOLVED / STILL PRESENT / PARTIALLY RESOLVED
- **Evidence:** specific telemetry observations supporting the verdict (file paths + values)
- **If RESOLVED:** what fixed it; when (commit SHA if traceable); does the fix carry forward to QD-rebuild's substrate-agnostic mechanic pool?
- **If STILL PRESENT or PARTIAL:** what's broken; what would fix it (math-before-code per Discipline #1); is the fix in scope for P0 or does it slot into P1 substrate work (Axis 5 resource economy substrate creation)?

### Step 3 — Update LC-026 disposition

Append your verdict to the LC-026 entry in `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (or create a co-located addendum file if you prefer not to modify jack-ryan's audit). Cross-link to your AGENT_STATE.md.

### Step 4 — Tag

If the verdict is RESOLVED and no further work needed → tag `qd-rebuild/v0.5-mana-bug-verify-resolved`.
If STILL PRESENT or PARTIAL → tag `qd-rebuild/v0.5-mana-bug-verify-needs-fix`; surface to knight-rider for follow-on workstream scoping.

## Required reading before starting

- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-026 entry
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/MEMORY.md` linked memory `project_engine_state_findings.md` (2026-05-08 mana-bug "small telemetry write gap" framing)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your prior P0/P1/P2 recompose-hive records)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11.1 (just ratified — apply rigorously)

## Math-before-code (if applicable)

If the verdict is STILL PRESENT and you propose a fix: produce a math note per Discipline #1 BEFORE implementing. State the failure mode, the proposed mechanism, the predicted effect (magnitude + direction + edge cases), then implement + verify. If the verdict is RESOLVED, no math note needed.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — empirical inspection workstream only; no field add/modify/rename/remove. If verdict requires future fix, that fix's own dispatch carries the round-trip clause.**

## Scope

- [ ] LC-026 description re-read from constraint-inventory
- [ ] Cold-start canonical empirical inspection (per Discipline #11.1) of mana resource pipeline
- [ ] Verdict documented in AGENT_STATE.md + math note (if applicable)
- [ ] LC-026 disposition updated in constraint-inventory (or co-located addendum)
- [ ] Intermediate tag fired (`qd-rebuild/v0.5-mana-bug-verify-*`)

## Acceptance criteria

- [ ] Verdict is one of RESOLVED / STILL PRESENT / PARTIAL — backed by specific telemetry evidence
- [ ] If STILL PRESENT or PARTIAL: math-before-code note authored; not yet implemented (knight-rider scopes fix as separate workstream)
- [ ] Round-trip: not applicable — empirical inspection workstream; no cross-seam contract change

## Out of scope

- Implementing any fix for the mana-bug (if found) — that's a separate downstream workstream
- Inspecting any other LCs in passing — focus on LC-026 only
- Broader resource-economy redesign — that's P1 W1.X substrate creation work

## Open questions for the agent to resolve

- If you find the bug is RESOLVED by some intermediate work, is the fix architecturally compatible with substrate-as-cohesion-only (substrate-agnostic mechanic pool; resource economy as Axis 5 BC dimension)? If you have doubts, flag for knight-rider.

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.5
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.5
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-026
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 1 (math-before-code), § 11.1 (state-space conditioning), § 17 (empirical calibration)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-21 QD-rebuild activation entry

---

## Completion record

**Completed:** 2026-05-21
**Verdict:** RESOLVED
**Tags shipped:** `qd-rebuild/v0.5-mana-bug-verify-resolved`
**Smoke results:** 54/54 test_energy_types.py PASS; 75 passed test_balance_loop.py + test_class_generation.py; 23/23 test_combat_simulator.py PASS. No code changes — empirical inspection only.
**MIGRATION.md written:** No — empirical inspection workstream; no cross-seam contract change.
**Math note written:** `reincarnated-engine/src/reincarnated/simulation/math/w0-5-mana-bug-verify.md`
**LC-026 disposition:** Addendum file created at `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/lc-026-mana-bug-verify-addendum-2026-05-21.md` (co-located with constraint-inventory; gamora did not modify jack-ryan's audit file directly).

**Notes for knight-rider / jack-ryan:**
- LC-026 is cleared. No follow-on fix workstream needed. Phase 1 dimensional refactor resolved the structural bug at both layers (pool assignment + skill costing).
- Residual: `base_stamina` column in `classes` telemetry table is never written by `recorder.py`. Out of scope for LC-026 (it is a documentation gap, not a fight-engine bug). Flag to star-lord for telemetry schema awareness if BC axis 5 profiling needs stamina pool data.
- `resource_over_time` per-fight telemetry field referenced in dispatch does not exist in current schema. Empirical inspection used `classes.base_mana`, `classes.int_stat/wis_stat`, and `abilities.energy_cost_pct` as equivalent evidence — sufficient for a RESOLVED verdict.
- QD-rebuild P1 substrate work (HP-economy substrate, charge-stack substrate, damage-converts substrate) can proceed with mana pipeline structurally sound. LC-025 and LC-030 remain open as separate P1 substrate extension requirements.
- No cross-seam or scope-creep concerns surfaced.
