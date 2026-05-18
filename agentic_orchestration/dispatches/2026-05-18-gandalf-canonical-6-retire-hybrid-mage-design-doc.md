# 2026-05-18 — gandalf — Canonical-6 transition: RETIRE hybrid_mage design doc

**Authority:** Matt L3 verdict 2026-05-18 (early morning) — RETIRE hybrid_mage from canonical-7 after D11.0/D11.1/D11.2 cycle of failures (6% → 0% → 0% convergence). Cleanest path to Matt's stated milestone: "develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it."
**Type:** Pattern A — design canon documentation; ~1-1.5 hours.
**Status:** 🟢 **ACTIVE — fire immediately. Matt-authorized.**

---

## Why this matters

Hybrid_mage was the multi-element + multi-archetype layered identity in canonical-7. Three sprint cycles (D11.0 with α tax recalibration; D11.1 ceiling-primary; D11.2 Lever B DPS density scale) all failed to drive convergence above 6% for this archetype. With gear_catalog environment fidelity, even Lever B at scale=0.75 produced 0/17 interior convergence.

Matt's verdict: rather than D12+ structural redesign of the archetype, **RETIRE hybrid_mage from canonical-7**. Move to **canonical-6**. Fresh new-season regen at canonical-6 unblocks the project. This dispatch authors the design-canon transition: what changes, what stays, what's lost, what alternatives exist.

---

## Required reading

1. **D11.2 advisory (your prior; identity preservation rationale)** — `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (524 lines; § identity preservation argument is now retracted material; § RETIRE clause is activated)
2. **D11.2 Phase B failure** — `agentic_orchestration/dispatches/2026-05-17-rocket-d11-2-phase-b-full-salvage-scale-0-75.md` § completion (PHASE_B_FAILED 0/17; gear-environment fidelity bug surfaced)
3. **Canonical-7 originating context** — wherever the 7-archetype list is canonical (likely canonical/AGENTS.md or canonical-32 progression doc); hybrid_mage was added when?
4. **Spirit Guide canon** — `canonical-XX-gear-and-spirit-guide-design.md` (mentions of hybrid_mage in spirit-guide context; cross-reference clean-up needed)
5. **Earth-Self meta-layer** — `canonical/story/earth-self-meta-layer-*.md` (cross-reference clean-up needed if hybrid_mage was named)
6. **Trait architecture** — Matt's MEMORY mentions `project_trait_architecture.md` — hybrid_mage trait pool? Verify cross-reference cleanup
7. **Hybrid_mage thematic origin** — your prior gandalf authoring of the "wide and modest, not narrow and sharp" framing; LE Runemaster lineage citation

---

## Scope — five deliverables

### Deliverable 1 — Canonical-6 transition design doc

Author `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md`. Sections:

- **Decision context**: D11.0/D11.1/D11.2 failure pattern; environment-fidelity bug; Matt L3 retire verdict; framing as design simplification rather than design failure
- **What was hybrid_mage**: thematic identity ("wide and modest"; multi-element + multi-archetype layered kit); LE Runemaster lineage reference; what it was trying to express
- **Why it didn't survive contact with the balance loop**: structural reason — multi-element kits compound the DPS-density problem; gear Monte Carlo over-buffs hybrid kits; no clean lever
- **Canonical-6 archetype list**: enumerate the 6 archetypes that remain; brief identity reaffirmation for each
- **What's lost**: thematic variety; specific player-fantasy paths (multi-element flex builds)
- **Where the lost identity-DNA lives now**: which archetypes absorb the "wide" feeling? (controllers? hunters?)  Any redistributions needed in trait pools / element coverage / kit shapes for other archetypes to fill the gap?
- **Alternative resurrection paths (for future seasons / experimental tier)**: could hybrid identity return as an unlockable experimental archetype with separate balance treatment? As a Spirit Guide bonus form? As an Earth-Self meta-layer perk? Note paths but don't commit
- **Cross-canon cleanup list**: docs that mention hybrid_mage and need amendments (your audit; pass to jack-ryan for doc-strip pass)

### Deliverable 2 — Hive-log STATE entry

Append to `agentic_orchestration/hive-mind/phase-1-p1-log.md`: gandalf canonical-6 design doc shipped; cross-canon cleanup list handed to jack-ryan; thematic alternative-resurrection paths parked.

### Deliverable 3 — Cross-canon cleanup list (hand-off to jack-ryan)

Enumerate every canon doc that mentions hybrid_mage with line/section refs. Jack-ryan will execute the strip pass as a separate dispatch (knight-rider will fire it post-yours). Expected docs include:
- canonical-32 progression
- canonical-17 gear-and-spirit-guide
- canonical-XX trait architecture
- earth-self meta-layer doc
- AGENTS.md or wherever canonical-7 archetype enumeration lives
- D11.2 advisory (retracted)

### Deliverable 4 — Identity-DNA preservation recommendation

Brief design recommendation (1 page) for which of the 6 remaining archetypes could absorb thematic remnants:
- Multi-element flex builds → ?
- "Wide and modest" tactical positioning → ?
- Layered identity → ?

Optional but useful — informs future archetype refinement.

### Deliverable 5 — Decisions-log handoff prep

Brief jack-ryan on what your decisions-log entry should capture (jack-ryan authors; you brief). Key items:
- Decision: RETIRE hybrid_mage from canonical-7
- Authority: Matt L3 2026-05-18
- Context: D11.0/D11.1/D11.2 cycle of failures
- Alternative considered: D12+ structural redesign — rejected as multi-day cycle with uncertain payoff
- Discipline #17 amendment: smoke environment fidelity clause (jack-ryan separately authors)

---

## Acceptance criteria

- [ ] Canonical-6 transition design doc authored
- [ ] Hive-log STATE entry appended (PRE-SIGNAL § 14.1.1)
- [ ] Cross-canon cleanup list complete (with file/section refs)
- [ ] Identity-DNA preservation recommendation included
- [ ] Decisions-log handoff brief drafted for jack-ryan
- [ ] AGENT_STATE STATE entry
- [ ] Tag `gandalf/v1.11-canonical-6-retire-hybrid-mage-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT amend the cross-canon docs yourself (jack-ryan handles strip pass; you provide the list)
- ❌ DO NOT re-litigate RETIRE (Matt-authorized)
- ❌ DO NOT commit to alternative-resurrection paths (note them; defer to future design)
- ❌ DO NOT touch generation code (rocket seam)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** jack-ryan decisions-log + Discipline #17 amendment (he waits for your handoff brief; can author Discipline #17 portion immediately); rocket archetype-list removal (independent code seam); drax v1.16.2 audio (separate seam); elrond dungeon-objects audit (separate seam)
- **Triggers downstream:** jack-ryan cross-canon strip pass dispatch (knight-rider fires post-your-list)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 RETIRE verdict. ~1-1.5h. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-18
**Agent:** gandalf
**Tag:** `gandalf/v1.11-canonical-6-retire-hybrid-mage-1` (local; push gated per ADR-006)
**Verdict:** SHIPPED CLEAN — all five dispatch deliverables landed within single canonical-6 doc + parallel jack-ryan completion + hive-log STATE + this completion record.
**Total time:** ~1.5h (within dispatch target).

### Deliverables shipped

1. **Canonical-6 transition design doc** — `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` (~11 sections; ~600 lines)
   - § 1 Decision context (D11.0/D11.1/D11.2 three-attempt failure cycle; Matt L3 verdict framed as simplification not failure)
   - § 2 What was hybrid_mage (generative shape; thematic identity; three intertwined design intents; 17 staged instances)
   - § 3 Why it didn't survive contact with the balance loop (multi-element DPS compounding; gear over-buffing; no clean lever at identity-preserving magnitude)
   - § 4 Canonical-6 archetype list (six substrate-coherent integrator slots reaffirmed; terminology clarification + jack-ryan handoff)
   - § 5 Where the lost identity-DNA lives now (Spirit Guide / form library; lightning + controllers; player-built composition)
   - § 6 Alternative resurrection paths (experimental tier; Spirit-Guide bonus; Phase-2 substrate expansion) — flagged not committed
   - § 7 What's lost (honest accounting: in-season variety; player-fantasy paths; genre vocabulary; future-design constraint)
   - § 8 Cross-canon cleanup list with per-doc strategy (~14 docs across canonical/ + canonical/story/ + engine code + consume-time surfaces)
   - § 9 Decisions-log handoff brief (structured input for jack-ryan)
   - § 10 Closing
   - § 11 Acceptance criteria checklist

2. **Hive-log STATE entry** — appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md` with PRE-SIGNAL § 14.1.1 honored.

3. **Cross-canon cleanup list** — § 8 of the canonical-6 doc; hands to jack-ryan for strip pass (knight-rider fires post-this completion). Recommended annotation pattern at § 8.6.

4. **Identity-DNA preservation recommendation** — § 5 of the canonical-6 doc; three threads redistributed (multi-element flex → meta-layer; "wide and modest" → lightning + controllers; layered identity → player composition).

5. **Decisions-log handoff brief** — § 9 of the canonical-6 doc; **note:** jack-ryan already shipped the decisions-log entry per their hive-log STATE (parallel firing per dispatch heads-up); my § 9 confirms structural alignment + ensures my doc's cross-reference path is captured.

### Acceptance criteria from dispatch

- [x] Canonical-6 transition design doc authored
- [x] Hive-log STATE entry appended (PRE-SIGNAL § 14.1.1 honored)
- [x] Cross-canon cleanup list complete (with file/section refs)
- [x] Identity-DNA preservation recommendation included
- [x] Decisions-log handoff brief drafted for jack-ryan
- [x] AGENT_STATE-equivalent visible in hive-log STATE (gandalf seam has hive-log-as-state-of-record per agentic orchestration norms; no separate AGENT_STATE.md in gandalf-territory paths)
- [x] Tag `gandalf/v1.11-canonical-6-retire-hybrid-mage-1` (local)

### Out-of-scope honored

- DID NOT amend cross-canon docs myself (jack-ryan strip pass deferred dispatch handles)
- DID NOT re-litigate RETIRE (Matt-authorized; design rationale captured at § 1 of canonical-6 doc)
- DID NOT commit to alternative-resurrection paths (§ 6 flagged not committed)
- DID NOT touch generation code (rocket seam; rocket dispatch in-flight)
- DID NOT push tag (ADR-006)

### Adjacent findings (flagged, not actioned)

1. **`canonical/story/archetype-coupling-archaeology-2026-05-17.md` Coupling #3 follow-up.** The stat_allocator fallback to hybrid_mage stats target archetype no longer exists post-canonical-6. Recommend ValueError on unrecognized archetype rather than silent fallback. Real engineering follow-up (rocket's territory); may warrant separate dispatch. Captured at § 8.2 item #12 of canonical-6 doc.
2. **Lightning archetype secondary-element-bias review (post-canonical-6 polish; § 5.4 of canonical-6 doc).** If playtest data shows players reaching for hybrid identity space and not finding it satisfied through lightning, consider biasing lightning's kit composition pipeline toward secondary-element skill inclusion. Tunable; small generative-pipeline cost; not blocking.
3. **Form-library narrative integrator-form emphasis (post-canonical-6 polish; § 5.4 of canonical-6 doc).** Player-facing strings + spirit-guide dialogue could explicitly call out the "integrator who walks many forms" archetype as a player journey-identity. Doc work; not engine work; lives in player-facing copy locations.

### Verdict on dispatch

DISPATCH CLOSED. Fresh new-season regen at canonical-6 unblocks per Matt's stated milestone ("develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it"). Cross-canon strip pass downstream-triggered to jack-ryan dispatch. Rocket archetype-list removal dispatch in flight in parallel. Drax + loadout consume-time filter downstream of rocket's `is_retired: true` flag emission.

— gandalf
