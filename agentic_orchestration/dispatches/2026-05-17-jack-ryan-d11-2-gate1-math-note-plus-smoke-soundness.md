# 2026-05-17 — jack-ryan — D11.2 Gate-1 review: math note + smoke procedure soundness

**Authority:** Gandalf D11.2 advisory handoff (auto-fire gate without Matt escalation unless answers shift composite-with-D / gate-threshold / smoke-acceptance values).
**Type:** Pattern A — Gate-1 review; ~45-60 min.
**Predecessor (just shipped):** gamora D11.2 math note at `reincarnated-engine/src/reincarnated/simulation/math/d11-2-lever-b-and-smoke-gate.md` (tag `gamora/v1.8-d11-2-lever-b-math-note-1`).
**Status:** 🟢 **ACTIVE — fire immediately.**

---

## Why this matters

D11.0 missed (6%). D11.1 missed worse (0%). D11.2 is the structural retry. Gandalf prescribed **Lever B + Discipline #17 (proposed) empirical-calibration smoke gate** to break the cycle of magnitude-by-analogy failures. Gamora has authored the formal math note. Before rocket implements, Gate-1 must validate soundness — both the algorithm (Lever B) AND the smoke procedure (Discipline #17).

The Discipline #17 proposal is load-bearing: if the smoke procedure has a hole, the project absorbs another D11.0/D11.1-style miss. Your review is the last gate before code lands.

---

## Required reading

1. **Gamora math note (primary review target)** — `reincarnated-engine/src/reincarnated/simulation/math/d11-2-lever-b-and-smoke-gate.md`
2. **Gandalf D11.2 advisory** — `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (524 lines; the verdict context + Discipline #17 proposal origin)
3. **D11.1 math note** — `reincarnated-engine/src/reincarnated/simulation/math/d11-1-ceiling-primary-tuning.md` (predecessor for elasticity reference)
4. **D11.0 → D11.1 empirical observed deltas** — extract from rocket completion records + hive-log STATE entries (you've seen this; cross-check gamora's central-elasticity assumption against the data)
5. **MIGRATION.md v1.11** — `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (gamora appended; verify cross-seam impact statement)
6. **Engineering disciplines** — `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (review #17 proposal for canonical fit + numbering)
7. **balance_loop.py** — for composite-D semantic-split verification (combatant creation seam, not kit finalization)

---

## Scope — seven review dimensions

### 1. Algorithm soundness (Lever B)

- Application site (`d10_kit_constraints.py` Site A; post-element-coverage-tax) — is this the right seam? Any alternative seams that would be cleaner?
- `_apply_dps_density_scale(skills, scale_factor)` predicate — does the `_is_damage_bearing()` predicate correctly map to `dps_score > 0`? (Gamora cited D11.1 INFO-3 as the source — verify.)
- Scope guard (`archetype_tag == "hybrid_mage"`) — robust against future archetype rename or splitting?

### 2. Idempotency

- Provenance field `balance_metadata.hybrid_mage_lever_b.scale_factor`
- Re-salvage divides out previous scale before applying new — is the math sound? Edge cases (scale_factor=0, missing field, partial application)?
- Canonical base state is "post-element-coverage-tax `damage_multiplier`" — verify gamora's claim that this is preserved across re-salvage rounds

### 3. Smoke-gate decision rule

- Sweep points `{0.75, 0.65, 0.55}` (low / mid / high DPS reduction) — anchor band per gandalf advisory; correct?
- Sequential test order (0.75 first → first-passing wins) — does this correctly bias toward minimal identity disruption?
- Acceptance threshold (≥3/5 instances escape floor-pin at WR-at-floor < 0.50) — appropriate signal strength?
- Composite B+D escalation (5% HP penalty applied only if scale=0.55 fails) — operationally clean?
- RETIRE escalation (composite also fails) — what does RETIRE concretely mean in implementation? (Verify gandalf's RETIRE clause is mechanizable.)

### 4. Instance selection adequacy (5 instances)

- class_0054 (WR=0.567) — low band
- class_0007 (WR=0.656) — mid-low
- class_0029 (WR=0.733, 2-element smoking gun)
- class_0012 (WR=0.744, low damage-skill count)
- class_0031 (WR=0.867, worst-case outlier)

Does this spread cover the WR distribution adequately? Does it sample Mode A (n=11-12) and Mode B (n=9-10) sufficiently? Any blind spots?

### 5. Elasticity assumption justification

- Central value: 0.75% WR per 1% DPS reduction (midpoint of empirically-anchored 0.5-1.0% range)
- Gamora cited D11.0→D11.1 marginal comparison (1% α nudge) as "below fight-variance noise floor" — verify; this justifies reading elasticity from D11.0 baseline rather than the D11.0→D11.1 delta
- Per-instance predictions at scale=0.65 central — verify the math; is the 4/5 expected pass claim defensible? class_0031 worst-outlier non-convergence prediction defensible?

### 6. Composite B+D semantic split

- Lever B applies at kit finalization (`d10_kit_constraints.py`)
- Lever D (5% HP penalty) applies at combatant creation (`balance_loop.py`)
- Two seams, two file modifications — gamora's argument: D is a runtime combat-state penalty, not a kit-shape property, so semantically belongs at combatant creation
- Verify this split is correct + that it doesn't create coupling fragility (e.g., what if combatant creation runs in a context where balance_metadata isn't available?)

### 7. Discipline #17 canonicalization recommendation

Gandalf proposed Discipline #17 as "empirical-calibration smoke gate before full-regen/full-salvage with a new lever." Three sub-questions:
- Does the case-study lineage (D11.0/D11.1 magnitude-by-analogy failures) justify a load-bearing engineering discipline?
- Should #17 be **adopted** as-is, **amended** with refinements you suggest, or **deferred** pending more validation cycles?
- If adopted, propose canonical wording for the discipline doc + cross-references (B14.5 V1 primary loop architecture pairs naturally; smoke-test discipline #2 is a precursor)

---

## Acceptance criteria

- [ ] Gate-1 verdict authored: ENDORSE / CONDITIONAL ENDORSE / BLOCK
- [ ] Each of 7 review dimensions explicitly addressed
- [ ] Specific concerns (if any) cited with file/line refs
- [ ] CONDITIONAL ENDORSE requires explicit list of conditions for rocket to satisfy
- [ ] BLOCK requires specific remediation path with owner identified
- [ ] Discipline #17 verdict: adopt / amend / defer (with rationale + canonical wording if adopt)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (heavy concurrent writers — star-lord scope just shipped + drax v1.15 audio still in flight)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `jack-ryan/v1.5-d11-2-gate1-math-note-soundness-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT re-litigate Lever B vs A/C/D/E (gandalf has resolved + Matt-authorized)
- ❌ DO NOT propose magnitude (smoke gate does)
- ❌ DO NOT implement (rocket seam; downstream)
- ❌ DO NOT amend the math note directly (gamora seam; if you need changes, BLOCK with specific list)
- ❌ DO NOT escalate Q1-Q6 to Matt unless your verdict requires answers that would shift composite-with-D, gate-threshold, or smoke-acceptance values (per gandalf handoff)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessor:** gamora D11.2 math note (complete)
- **Triggers downstream:** rocket D11.2 implementation (Phase A: lever code + smoke runner; Phase B: full salvage if smoke passes) — knight-rider will author + fire on your ENDORSE/CONDITIONAL
- **Parallel-safe with:** drax v1.15 audio (in flight); star-lord JSON-parity scope shipped (now awaiting Matt decision)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-17 by knight-rider per gandalf handoff + gamora completion. ~45-60 min. Append verdict + completion record when done.*

---

## Completion record — jack-ryan Gate-1 verdict

**Completed:** 2026-05-17
**Reviewer:** jack-ryan
**Verdict:** CONDITIONAL ENDORSE
**Tag:** `jack-ryan/v1.5-d11-2-gate1-math-note-soundness-1` (local; push gated per ADR-006)
**Time:** ~55 min

### Verdict summary

CONDITIONAL ENDORSE. Math note is structurally sound across 6 of 7 review dimensions. Four conditions to be resolved by rocket at implementation time (not gamora amend time). Discipline #17 is ADOPTED with one acceptance-gate amendment (⌈N/2⌉ not ⌈(N/2)+1⌉). Knight-rider is clear to author and fire rocket D11.2 Phase A dispatch.

### Acceptance criteria status

- [x] Gate-1 verdict authored: CONDITIONAL ENDORSE
- [x] Each of 7 review dimensions explicitly addressed
- [x] Specific concerns cited with file/line refs (combatant.py; balance_loop.py lines 427-432, 776; d10_kit_constraints.py lines 484-493; MIGRATION.md)
- [x] CONDITIONAL ENDORSE — 4 conditions listed, all implementation-layer (rocket/gamora); no math-note revision required
- [x] Discipline #17 verdict: ADOPTED with ⌈N/2⌉ amendment; canonical wording provided
- [x] PRE-SIGNAL § 14.1.1 performed (git fetch; log check; no concurrent writes on target path)
- [x] AGENT_STATE STATE entry (see generation AGENT_STATE.md)
- [x] Tag `jack-ryan/v1.5-d11-2-gate1-math-note-soundness-1`

### Conditions for rocket (Phase A)

1. Externalize archetype guard string to config constant (not inline `"hybrid_mage"` literal)
2. Resolve flat vs nested provenance key: flat `hybrid_mage_dps_scale_factor` for idempotency restore; nested `hybrid_mage_lever_b` dict for provenance audit; both written on every salvage pass
3. Composite B+D `composite_d_active` flag: read once at top of `balance_class()` from incoming class JSON (same pattern as element-coverage tax at line 427-432 of balance_loop.py); not re-read from balance_metadata mid-loop (relevant only if Step 3 smoke fails)
4. Append R11(b) round-trip clause to MIGRATION.md v1.11 before Phase B (acceptable form: deferral clause naming the Phase A smoke as the round-trip exercise point)

### Chain trigger

Knight-rider: fire rocket D11.2 Phase A dispatch. Include: 4 conditions above; INFO-C (dps_score persistence, Discipline #7); INFO-D (Phase B sliding gate spec: ≥10/17 at scale=0.65 OR ≥12/17 at scale=0.55 per gandalf advisory § 7.4).

— jack-ryan
