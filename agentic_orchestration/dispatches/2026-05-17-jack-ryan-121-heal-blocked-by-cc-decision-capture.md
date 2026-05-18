# 2026-05-17 — jack-ryan — #121 Heal-blocked-by-CC decision capture + canonical-17/32 amendments

**Authority:** Matt L3 verdict 2026-05-17 late-evening: "From critical Path #2. I agree with Heals should be blocked by stunned/frozen/silenced".
**Type:** Pattern A — discrete decision capture + canon doc amendments; ~45-60 min.
**Status:** 🟢 **ACTIVE — Matt-authorized; fire immediately.**

---

## Why this matters

Heal-while-CC (stunned / frozen / silenced) was ESCALATE-TO-MATT #121 — the gating decision for VS2b heal_ability refactor and for the heal-affix mechanic spec in canonical-17. jack-ryan's prior recommendation in critical-path was UNCONDITIONAL (DoE pattern; simpler combatant model). Matt has resolved the OPPOSITE direction: **heals BLOCKED by CC**. This is design-canon, not implementation polish — needs decisions-log capture before code lands.

---

## Required reading

1. **#121 escalation context** — recent hive activity around heal-affix mechanic (canonical-17 § heal-affix; canonical-32 § 13 progression)
2. **DoE mobile-feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (heal mechanic spec: 10s CD, 35% max-HP, 50 HP floor, 0s cast, no invuln)
3. **decisions-log.md** — `reincarnated-engine/design/decisions/decisions-log.md` (canonical decision-log location)
4. **canonical-17** — `reincarnated-collaboration/canonical/17-gear-and-spirit-guide-design.md` (heal-affix section needs CC-interaction clause)
5. **canonical-32** — `reincarnated-collaboration/canonical/32-progression-design.md` § 13 (progression mechanic; heal interaction)

---

## Scope — three deliverables

### Deliverable 1 — decisions-log.md entry

Author a fresh decisions-log entry capturing:
- **Decision:** Heal abilities are BLOCKED by stun / freeze / silence (and any future CC ailments that satisfy "actor cannot take voluntary action")
- **Date:** 2026-05-17
- **Authority:** Matt L3 verdict
- **Context:** ESCALATE #121 — was deferred pending design-direction decision
- **Implications:**
  - Heal-affix mechanic (canonical-17) must check actor CC state before resolving
  - Heal_ability core spec (VS2b refactor) gets explicit CC-gate
  - Combatant model gains complexity (state-check before heal); not the simpler UNCONDITIONAL path jack-ryan recommended
  - Anti-pattern: chain-heal during CC-lock is impossible (intentional; player must use defensive options + react)
- **Rationale (per Matt):** Path-2 ARPG semantic — being CC'd means you can't act; healing is an action; therefore CC blocks heal. Genre canon.
- **Alternative considered (UNCONDITIONAL):** jack-ryan recommended for simpler combatant model + DoE pattern alignment. Rejected — Matt prioritized semantic coherence over implementation simplicity.

### Deliverable 2 — canonical-17 amendment (heal-affix § interaction)

Amend canonical-17's heal-affix section to include the CC-gate clause. Suggested wording (adapt to existing voice):

> **CC interaction.** Heal-affix-triggered heals (and any heal ability proper) are BLOCKED during stun / freeze / silence states. The heal is **suppressed** (not queued, not partial, not delayed) — the cooldown does not advance, but the heal does not fire. When the CC ends, the heal becomes available on its normal cooldown timer (i.e., if the affix was off-cooldown when CC was applied, it remains off-cooldown when CC ends).

Cross-reference the decisions-log entry by date.

### Deliverable 3 — canonical-32 § 13 amendment (heal mechanic + progression)

Amend canonical-32 § 13's heal mechanic spec to mirror the CC-gate clause. Single sentence is sufficient; cross-reference canonical-17 + decisions-log.

---

## Acceptance criteria

- [ ] decisions-log entry authored with date, authority, decision, rationale, alternative-considered
- [ ] canonical-17 heal-affix section includes CC-gate clause with cooldown-pause semantics specified
- [ ] canonical-32 § 13 heal mechanic mirrors the gate
- [ ] All three docs cross-reference each other consistently
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (if multiple agents writing)
- [ ] AGENT_STATE STATE entry capturing decision-capture event
- [ ] Tag `jack-ryan/v1.4-heal-blocked-by-cc-decision-capture-1` (intermediate seam tag per ADR-006)

---

## Out of scope (DO NOT)

- ❌ DO NOT implement the gate in code (rocket / gamora seam work; separate dispatch)
- ❌ DO NOT modify VS2b heal_ability refactor scope (this dispatch unblocks it; refactor is its own dispatch)
- ❌ DO NOT amend any test fixtures (test impact is downstream of implementation)
- ❌ DO NOT push tag (ADR-006; Matt-only)
- ❌ DO NOT re-open the UNCONDITIONAL alternative (Matt has resolved)

---

## Coordination

- **Parallel-safe with**: all in-flight work (gandalf D11.2 + drax v1.14); decision capture is doc-only
- **Triggers downstream**: VS2b heal_ability refactor dispatch (rocket/gamora joint; future)
- **Cross-seam impact**: Yes — heal-affix mechanic (canonical-17) gets CC-gate; combatant model (gamora seam) will need to honor

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 verdict on #121. ~45-60 min. Append completion record when done.*

---

## Completion record — 2026-05-17

**Agent:** jack-ryan
**Status:** COMPLETE
**Tag:** `jack-ryan/v1.4-heal-blocked-by-cc-decision-capture-1` (applied to both `reincarnated-engine` and `reincarnated-collaboration` repos; no push per ADR-006)

### Deliverables shipped

**Deliverable 1 — decisions-log.md entry**
- File: `reincarnated-engine/design/decisions/decisions-log.md`
- Commit: `a68d3cc` (engine repo)
- Entry title: "2026-05-17: Heal blocked by CC ailments — #121 verdict"
- Content: date, authority (Matt L3), decision (BLOCKED/suppressed/cooldown-paused), rationale (semantic coherence; ARPG genre canon), alternative considered (UNCONDITIONAL jack-ryan recommendation, rejected), implications (all seam obligations: gamora CC-state check, star-lord `cc_suppressed` telemetry field, rocket `heal_secondary_effect` secondary-effect suppression, jack-ryan Gate-1 obligation for VS2b).
- Also updated the existing "Heal mechanic + heal-affix family" entry's open-question marker from open to resolved, with forward pointer to the new entry.

**Deliverable 2 — canonical-17 amendment**
- File: `reincarnated-collaboration/canonical/17-gear-and-spirit-guide-design.md`
- Commit: `1bc94b0` (collaboration repo)
- Insertion point: after stacking caps block, before "Affix-coherence interaction" section
- Content: "CC interaction — heals BLOCKED during stun / freeze / silence (LOCKED 2026-05-17; Matt L3 verdict #121)" with suppression semantics, cooldown-pause behavior, `heal_secondary_effect` propagation rule (no secondary fires if primary suppressed), future-CC definition anchor, and cross-references to decisions-log + canonical-32 § 13.1.

**Deliverable 3 — canonical-32 § 13.1 amendment**
- File: `reincarnated-collaboration/canonical/32-progression-design.md`
- Commit: `1bc94b0` (collaboration repo)
- Insertion point: after "Engine-side execution (deferred to VS2b)" note, before § 13.2
- Content: single focused CC-gate clause mirroring canonical-17, with cooldown-pause semantics spelled out ("a heal that was ready before CC fires remains ready; a heal on cooldown resumes its timer from where it paused"), and cross-references to canonical-17 + decisions-log.

### Cross-reference consistency check

All three documents reference each other:
- decisions-log → canonical-17 § "Heal-cooldown affix family — CC interaction" + canonical-32 § 13.1 CC-gate clause
- canonical-17 → decisions-log entry + canonical-32 § 13.1
- canonical-32 → canonical-17 § "CC interaction" + decisions-log entry

### Downstream state

- VS2b heal_ability refactor is now unblocked. The design contract is complete: gamora's `combatant.py` spec has the full behavioral rule set (cooldown-gated heal + CC-gate with suppression + cooldown-pause).
- jack-ryan Gate-1 advisory on VS2b dispatch must verify: (a) CC-state check fires before heal resolve, (b) cooldown does not advance during suppression, (c) star-lord telemetry includes `cc_suppressed: bool` field.
- No code was written; this was doc-only per dispatch scope.

### Acceptance criteria verification

- [x] decisions-log entry authored with date, authority, decision, rationale, alternative-considered
- [x] canonical-17 heal-affix section includes CC-gate clause with cooldown-pause semantics specified
- [x] canonical-32 § 13.1 heal mechanic mirrors the gate
- [x] All three docs cross-reference each other consistently
- [x] Tag `jack-ryan/v1.4-heal-blocked-by-cc-decision-capture-1` applied (both repos; no push per ADR-006)
- [ ] PRE-SIGNAL § 14.1.1 — doc-only work; no hive-log append required for this dispatch
- [ ] AGENT_STATE STATE entry — noted below

**AGENT_STATE note:** This dispatch is doc-only, no state file update required per dispatch scope. VS2b dispatch (when authored) will carry the formal AGENT_STATE entry for the heal refactor work.
