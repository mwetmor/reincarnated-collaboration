# Dispatch — 2026-05-21 — rocket — W0.3: Foundation validator update (D5 = 7-substrate; LC-012 fix)

**From:** knight-rider
**To:** rocket
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); Matt D5 resolution per activation dispatch § 1.2 (delegated to gandalf; 7-substrate)
**Status:** PENDING — ACTIVE (rocket may execute when launched)
**Estimated effort:** ~1 hour (trivial; single-validator function update)
**Acceptance:** `foundation/foundation.py:39-43` updated to accept 7-substrate; 7-element season generation passes validator; tests pass; tag `qd-rebuild/v0.3-foundation-validator-7-substrate`.

---

## Context

LC-012 (jack-ryan legacy constraint audit) flagged Discipline #13a drift: `foundation/foundation.py:39-43` enforces 4-rotating + 1-physical (canonical-four-element era) but `config/substrate_identities/` declares 7 substrates. D5 was the blocking decision; Matt resolved 2026-05-21 in favor of 7-substrate (matches D2 + substrate identities + Phase-1 P1 commitment).

This dispatch is the trivial-actionable code fix. Under substrate-as-cohesion-only architectural recommitment, the validator becomes a cohesion-layer check (cohesion-judge produces sensible substrate labels), not a substrate-mechanic enforcer — but for backward compatibility + readability + LC-012 drift closure, the 7-substrate count IS the right value.

## What this dispatch does

### Step 1 — Update foundation validator

Target: `reincarnated-engine/src/reincarnated/foundation/foundation.py:39-43` (or whatever lines the current validator occupies).

Change: from enforcing exactly 4-rotating + 1-physical → to enforcing **7-substrate aligned with `config/substrate_identities/`**: fire / water / earth / wind / lightning / holy / shadow. Match the structure `config/substrate_identities/` declares.

### Step 2 — Update any inline literals + tests

Any test or call-site that hard-coded "4 rotating elements" or "canonical four" — update to reflect 7-substrate. Search for these patterns:
- Inline references to 4-element validator behavior
- Test assertions on validator output
- Any other validator-related references in `tests/`

Be selective — don't sweep beyond the validator's own consumers.

### Step 3 — Smoke + tests

Per Discipline #2 (smoke-test mode): run `pytest tests/test_foundation.py` (or equivalent) — confirm 7-element validation passes; no regressions on prior tests. Full test suite confirm: 179/179 PASS preserved (or your current baseline).

### Step 4 — MIGRATION.md (if applicable)

If your foundation validator change affects how downstream seams consume foundation output (e.g., sim or generation code reads from foundation), file a MIGRATION.md entry per ADR-004. Most likely NOT applicable — the validator is a generation-side gatekeeper; sim doesn't consume it directly.

### Step 5 — Tag

Intermediate tag: `qd-rebuild/v0.3-foundation-validator-7-substrate`.

## Required reading before starting

- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-012 entry
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-21 QD-rebuild activation entry (D5 resolution)
- `canonical/story/substrate-design-supplement-2026-05-21.md` (substrate-as-cohesion-only — operative principle; validator is cohesion-layer check)
- `reincarnated-engine/src/reincarnated/foundation/foundation.py` (current state)
- `reincarnated-engine/config/substrate_identities/` (target — 7 substrates)

## Math-before-code (if applicable)

Not applicable — single validator function update with clear before/after spec.

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add/modify/rename/remove any field on cross-seam contracts (telemetry schema, fight_log dict key, loadout dict key, export packet structure, inter-seam fixture dict)?

**Most likely NO** — foundation validator is generation-internal gating; output is "season passes validation" boolean. If you discover during implementation that downstream sim/export DOES read foundation output structurally, surface to knight-rider before proceeding.

Default disposition: **Round-trip: not applicable — validator is generation-internal; no cross-seam contract change.** Confirm during implementation.

## Scope

- [ ] LC-012 description re-read
- [ ] `foundation/foundation.py:39-43` updated from 4-rotating+1-physical → 7-substrate aligned with `config/substrate_identities/`
- [ ] Inline literals + test references updated
- [ ] Smoke + full test suite PASS
- [ ] MIGRATION.md if cross-seam impact discovered (per ADR-004)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `qd-rebuild/v0.3-foundation-validator-7-substrate`

## Acceptance criteria

- [ ] 7-element season generation passes validator (test in smoke OR via `--smoke` regen)
- [ ] Prior 4-element seasons still validate (backward compatibility — verify with existing season fixtures if any)
- [ ] No test regressions
- [ ] Round-trip: not applicable — validator is generation-internal (or, if cross-seam impact discovered: explicit MIGRATION.md round-trip clause)

## Out of scope

- Restructuring substrate identities config (the 7-substrate set is already locked per D2 + `config/substrate_identities/`)
- Refactoring the validator to substrate-AGNOSTIC under substrate-as-cohesion (that's an architectural-question to revisit in P5 cohesion-BC work; this dispatch just closes LC-012 drift at the count-level)
- Any other foundation-layer changes
- Sweep for other LCs (focus on LC-012 only)

## Open questions for the agent to resolve

- If the current validator's structure makes 4→7 a single-line constant change, do it. If it requires structural refactor, surface to knight-rider — keep the LC-012 fix scope minimal
- Whether `physical` is treated as substrate-7 or as separate non-rotating: align with `config/substrate_identities/` actual structure (per D2 the 7 elements are fire/water/earth/wind/lightning/holy/shadow; physical is the cohesion-theme exception per substrate supplement § 2.2 — not a separate substrate in the validator's count)

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.3
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.3
- `canonical/story/substrate-design-supplement-2026-05-21.md` § 5.2 (LC-012 reinterpretation under substrate-as-cohesion)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-012
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-21 QD-rebuild activation entry D5 row
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 13a (drift discipline; this dispatch closes a drift-candidate)
