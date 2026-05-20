# Dispatch — 2026-05-21 — multi-seam — W0.6: Drift candidate closures (LC-006, LC-007, LC-014, LC-028)

**From:** knight-rider
**To:** jack-ryan (drift-discipline owner per Discipline #13a) + rocket (LC-006 + LC-007 + LC-014 generation-side) + gamora (LC-028 if sim-side) + star-lord (LC-006 + LC-014 telemetry/export side); gandalf reviews thematic implications
**Approved by:** gandalf attestation 2026-05-21 § 5 (six autonomous workstreams cleared); per activation dispatch § 4 Step 4 W0.6 + protocol § 6.1.2 W0.6
**Status:** PENDING — ACTIVE (multi-seam coordination via this dispatch's shared completion record)
**Estimated effort:** ~3-5 days total across all 4 LCs (each disposition: bring code into compliance with canonical doc OR revise canonical doc to match committed code direction)
**Acceptance:** Per-LC disposition decision documented; closure or formal-deferral filed in `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md`; tag `qd-rebuild/v0.6-drift-closures-complete`.

---

## Context

Per Discipline #13a (Implementation-vs-intent drift): drift candidates are gaps between canonical-doc intent and code state. Jack-ryan's audit surfaced 5 drift candidates: LC-006 / LC-007 / LC-012 / LC-014 / LC-028. **LC-012 (foundation validator) is handled separately in W0.3** per D5 resolution. The remaining 4 close in this W0.6 dispatch.

**Per Discipline #13a, drift closures take one of two forms:**
- **(a) Bring code into compliance** with canonical doc (resolve the drift toward intent)
- **(b) Revise canonical doc** to match committed code direction (acknowledge the drift as a design evolution; update intent to match reality)

The choice (a) vs (b) per LC is a design-judgment call requiring jack-ryan (drift discipline owner) + relevant seam specialist + gandalf (thematic implications) coordination.

## Per-LC scope

### LC-006 — Canonical-four element labels universally exposed to LLM

**Status from audit:** DRIFT-CANDIDATE (documented intent in doc 37 § 6 — canonical-four hidden; code state — universally exposed at `llm/naming.py:26-36, :87, :89`; `element/selector.py:43-47, :394-446`; `canonical/library_generator.py:85`).

**Disposition per protocol § 6.1.5 + activation dispatch § 1.2 D3:** D3 resolution sequenced cohesion-BC POST-cipher migration. LC-006 fix IS the cipher migration (Stage 3 of form-bias work per `canonical/story/form-bias-cadence-strategy.md` Option II).

**W0.6 action:** **DEFER** this LC to cipher migration workstream. Document the deferral in phase-2-code-side-verification.md with explicit cross-ref to D3 + cipher migration roadmap. Do NOT close in W0.6; cipher migration is its own workstream sequenced before cohesion-BC starts.

**Seam owners:** rocket (LLM prompt construction) + star-lord (export/telemetry surfaces).
**Critique-pair:** gandalf reviews thematic implications of contamination during deferred period; jack-ryan reviews drift discipline (documented deferral is acceptable per Discipline #13a if explicit + tracked).

### LC-007 — Humanoid-presupposing gear schema

**Status from audit:** DOCUMENTED (Position C migration locked but not yet shipped; canonical-doc 37 § 4 specifies functional-mechanic labels; code retains weapon/off_hand/armor/accessory humanoid presuppositions).

**Disposition per protocol § 6.1.5:** Sim extensions in P4 enable non-humanoid embodiments. P4 W4.1 (player-side proxy support) and Stage 1 form-bias migration (per cadence strategy) are downstream consumers.

**W0.6 action:** **DEFER** to P4 territory + Stage 1 form-bias migration workstream. Document deferral in phase-2-code-side-verification.md. Do NOT close in W0.6; structural schema migration is multi-seam coordinated work scoped separately.

**Seam owners:** rocket (gear schema + gear_catalog) + star-lord (export packets carrying gear schema fields).
**Critique-pair:** gandalf reviews canonical doc 37 § 4 functional-mechanic-vs-narrative-skin framing; jack-ryan reviews drift discipline.

### LC-014 — (specifics from constraint inventory)

**W0.6 action:** Read LC-014 entry in constraint inventory; apply (a) vs (b) decision logic; document disposition.

**Likely disposition:** depends on LC-014 specifics (jack-ryan inventory contains the full description). Default: if LC-014 is canonical-four-related, DEFER per D3; if structural-schema-related, DEFER per P4; otherwise apply per-LC judgment.

**Seam owners:** TBD per LC-014 specifics.
**Critique-pair:** as above.

### LC-028 — (specifics from constraint inventory)

**W0.6 action:** Read LC-028 entry in constraint inventory; apply (a) vs (b) decision logic; document disposition.

**Likely disposition:** TBD per specifics.

**Seam owners:** TBD per LC-028 specifics.
**Critique-pair:** as above.

## Coordination

This is multi-seam coordination via shared deliverable. Each LC's disposition appended to `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md` (same file as W0.4 specialist code audit deliverable; W0.6 + W0.4 share this file).

**Per-LC disposition format:**

```markdown
### LC-XXX — <name>

**Disposition:** (a) BRING-CODE-INTO-COMPLIANCE / (b) REVISE-CANONICAL-DOC / (c) FORMAL-DEFER-TO-DOWNSTREAM
**Owner seam(s):** <seam>
**Decision rationale:** <2-3 sentences>
**Action items (if a or b):** <specifics>
**Deferral target (if c):** <workstream / phase> + cross-ref
**Critique-pair status:** gandalf reviewed: <yes/no>; jack-ryan reviewed: <yes/no>
**Status:** OPEN / CLOSED
```

**Hive tag (after all 4 LCs dispositioned + critique-pair reviewed):** `qd-rebuild/v0.6-drift-closures-complete`

## Required reading before starting

- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (LC-006, LC-007, LC-014, LC-028 entries)
- `canonical/37-form-bias-diagnosis-and-recovery.md` (canonical-four + functional-mechanic framing)
- `canonical/story/form-bias-cadence-strategy.md` (Stage 1 + Stage 3 form-bias migration roadmap)
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 1.2 D3 (cohesion-BC sequenced post-cipher)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.6
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 13a (drift discipline; the authoritative spec)

## Math-before-code (if applicable)

Not applicable — this dispatch's deliverable is per-LC DISPOSITION decisions, not new code. Any (a) BRING-CODE-INTO-COMPLIANCE work that emerges from a disposition becomes a follow-on workstream with its own math-before-code requirement.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — disposition decisions only; no field add/modify/rename/remove in W0.6 itself. Each downstream (a) compliance-action workstream carries its own round-trip clause.**

## Scope

- [ ] LC-006 disposition documented (likely DEFER per D3 cipher migration)
- [ ] LC-007 disposition documented (likely DEFER per P4 sim extensions + Stage 1 form-bias)
- [ ] LC-014 disposition documented (per inventory specifics)
- [ ] LC-028 disposition documented (per inventory specifics)
- [ ] All 4 dispositions appended to phase-2-code-side-verification.md
- [ ] Critique-pair: gandalf reviewed thematic implications; jack-ryan reviewed drift discipline
- [ ] Tag: `qd-rebuild/v0.6-drift-closures-complete`

## Acceptance criteria

- [ ] Each LC has clear (a) / (b) / (c) disposition + rationale
- [ ] Deferrals (c) have explicit downstream-workstream cross-ref
- [ ] Cross-seam impact noted per ADR-004 if any disposition implies imminent cross-seam contract change
- [ ] Round-trip: not applicable — disposition-decision workstream

## Out of scope

- Implementing any (a) BRING-CODE-INTO-COMPLIANCE work surfaced by dispositions (those are follow-on workstreams)
- Re-litigating LC severity (jack-ryan audit's HIGH/MEDIUM/LOW classifications are LIVE)
- Closing LC-012 (handled separately in W0.3 per D5)
- Sweep for additional drift candidates beyond the 4 listed (those surface via W0.4 specialist code audit if any)

## Open questions for the agent to resolve

- For each LC, evaluate (a) vs (b) vs (c) per the canonical-doc-vs-code gap analysis. Default to (c) DEFER if the closing workstream is already roadmapped per existing canonical docs (e.g., cipher migration for LC-006; Stage 1 form-bias for LC-007).
- If any LC's specifics reveal it's no longer a drift candidate (e.g., shipped intermediate fix closed it): mark as RESOLVED + cite the closing commit/dispatch.

## References

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 4 Step 4 W0.6
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.1.2 W0.6
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (LC-006, LC-007, LC-014, LC-028)
- `canonical/37-form-bias-diagnosis-and-recovery.md`
- `canonical/story/form-bias-cadence-strategy.md`
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 13a
