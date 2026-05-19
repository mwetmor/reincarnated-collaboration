# Dispatch — 2026-05-19 — gamora — VS2a S3 Gate-3b sim MS extension

**From:** knight-rider
**To:** gamora (simulation seam — sim MS consumption OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when rocket schema-default-update lands + star-lord export-DTO fix lands (both from C1 in-flight work)
**Estimated effort:** ~3–5 days gamora
**Acceptance:** Sim consumes engine-emitted JSON movement-speed values via single source-of-truth path; sim + demo + engine agree on Option-B values. Tag fires: `vs2a/v0.9-sim-ms-gate3b-complete`.
**Hive context:** VS2a hive ACTIVE; gated on C1 sub-tasks (rocket schema-default-update + star-lord export-DTO fix). C1 is in-flight per drax AGENT_STATE; rocket + star-lord pieces are tracked separately.

---

## Context

Per `canonical/story/movement-speed-baseline.md` § "Verdict Reversal" (Matt verdict 2026-05-16 Day-4 close) + `canonical/16-project-roadmap.md` § VS2a:

- Matt verdict reversal: VS2a is ANCHORED TO END-GAME BALANCE STATE
- Option-B values LOCKED: player 8.0 m/s; trash 5.75; fast 7.5; AI_SPEED_MULTIPLIER 0.719
- Sim and demo must AGREE on the same values
- Engine-emitted JSON is the SINGLE SOURCE OF TRUTH

Current state per scope-of-work-vs2a § 2.4:
- Rocket schema-default-update PENDING
- Drax demo MS pending engine-emitted JSON consumption (precondition: Stage B export-DTO fix)
- Star-lord export-DTO fix PENDING
- **Gamora Gate-3b sim MS extension is the LAST consumer in the cascade** — sim must consume the same engine-emitted JSON

**Gate-3b reframing.** Gate-3b was originally post-VS2a tight follow; Matt verdict 2026-05-16 Day-4 close reclassified it as VS2a-GATING. Sim consumption of engine-emitted JSON is the closing handshake for the movement-speed cascade — without it, sim and demo can diverge on MS values without anyone noticing.

---

## Required reading

In order:
1. `canonical/story/movement-speed-baseline.md` § "Verdict Reversal" (Matt verdict)
2. `canonical/16-project-roadmap.md` § VS2a (Gate-3b reclassification)
3. C1 in-flight artifacts: rocket schema-default-update commit + star-lord export-DTO fix commit (both expected; check rocket + star-lord AGENT_STATE)
4. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your last checkpoint)
5. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` + related code paths (current MS consumption — likely hardcoded constants today)
6. `reincarnated-engine/src/reincarnated/export/` (star-lord export-DTO; the JSON shape sim consumes)
7. `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.4 (S3) + § 2.5 (C1 cascade)
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

- [ ] Verify upstream cascade complete: rocket schema-default-update operational + star-lord export-DTO emitting MS values in engine-output JSON
- [ ] Sim consumer extension: balance_loop.py + fight_engine.py + spatial_engine.py (any MS-using code paths) read engine-emitted JSON values instead of hardcoded constants
  - Player MS: 8.0 m/s
  - Trash MS: 5.75 m/s
  - Fast MS: 7.5 m/s
  - AI_SPEED_MULTIPLIER: 0.719 (per Option-B lock)
- [ ] Single source-of-truth path: sim's MS reads come from the same JSON manifest demo reads (per Matt verdict reversal "engine-emitted JSON drives both")
- [ ] Backward compat: legacy seasons without engine-emitted JSON MS values fall back to hardcoded defaults + emit warning (Discipline #13 drift signal; analogous to F1 fallback pattern)
- [ ] Hypothesis test: sim + demo agree on MS values; run smoke fixture comparing sim MS reads vs demo MS reads on shared season; assert equality within tolerance
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (consumer extension)
- [ ] AGENT_STATE.md updated

---

## Cross-seam contract change? (Principle 6 gate)

**Consumer-side; no schema or contract addition.** Rocket schema-default + star-lord export-DTO are the producing-side changes; S3 is the sim consumer.

**MIGRATION.md** at sim seam (additive consumer contract; legacy fallback documented).

**Round-trip smoke REQUIRED** per Principle 6: shared-season fixture exercises engine emit MS → sim consume MS → demo consume MS → assert sim + demo equal MS values. Field-presence + value-equality checks at each boundary.

---

## Acceptance criteria

- [ ] Upstream cascade verified: rocket schema-default + star-lord export-DTO operational
- [ ] Sim consumes engine-emitted JSON MS values (player + trash + fast + AI_SPEED_MULTIPLIER)
- [ ] Legacy fallback + warning operational
- [ ] Hypothesis test: sim + demo agree on MS values via round-trip fixture
- [ ] MIGRATION.md appended at sim seam
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on start + STATE on completion + HANDOFF if demo MS values need re-verification (drax consumer)
- [ ] Tag: `vs2a/v0.9-sim-ms-gate3b-complete`

---

## Out of scope

- Rocket schema-default-update (upstream; rocket's seam in C1)
- Star-lord export-DTO fix (upstream; star-lord's seam in C1)
- Drax demo MS implementation (parallel consumer; drax C1 work)
- Movement-speed VALUES amendment (Option-B values LOCKED per Matt verdict; not in scope to revise)
- Per-class MS variation (B12 territory; post-VS2a)

---

## Open questions for gamora

- **Source-of-truth JSON path** — L1 gamora. The engine-output `manifest.json` per season is likely the canonical path; rocket schema-default + star-lord export-DTO determine exact field shape. Read both to confirm.
- **Fallback behavior** — L1 gamora. Hardcoded Option-B values as fallback for legacy seasons; emit warning per Discipline #13 drift pattern (cross-reference F1 fallback methodology).
- **Tolerance for sim + demo agreement** — L1 gamora. Likely exact equality (these are constants, not derived); document choice.
- **Per-tier MS variation hooks** — out of scope per VS2a, but if sim consumer architecture is being touched, consider preserving the seam for future B12 per-class MS variation extension. L1 gamora.

---

## References

- `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"
- `canonical/16-project-roadmap.md` § VS2a (Gate-3b reclassification)
- C1 cascade dispatches (rocket schema-default + star-lord export-DTO; in-flight per AGENT_STATE)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.4 + § 2.5
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** rocket schema-default-update operational + star-lord export-DTO emitting MS values (both C1 sub-tasks).

**Post-activation:** gamora L1; no Matt-wait. If sim + demo disagree under fixture, surface to knight-rider for cross-seam coordination — may require rocket or star-lord to amend.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. S3 closes the movement-speed cascade. Engine emits; demo consumes; sim consumes; all three agree on what 8.0 m/s means.*
