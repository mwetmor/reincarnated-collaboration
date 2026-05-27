# Cycle 13 Pre-Launch Design Session — gandalf Session-Start Doc

> **Purpose:** Focused Matt + gandalf design session to unblock every step of Cycle 13. Combines T4 PM1 (with Matt 2026-05-26 Q7 expanded scope: gear details + character sheet stats + per-slot fill rules) WITH the 7 Phase-3 gaps identified during 2026-05-26 roadmap review. Single session OR sequenced sub-sessions per Matt preference.

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-26 — directive to draft session-start doc covering T4 PM1 expanded scope + Phase 3 gap-closure for Cycle 13 unblocking
**Pattern:** Pattern-B Matt + gandalf design call (per `.claude/agents/gandalf.md` Pattern-B)
**Estimated duration:** 2-4 hours (single session) OR 2-3 sub-sessions of 60-90 min each

---

## 0. TL;DR — what this session produces

By end of session, every Cycle 13 step has the design inputs needed to fire. Specifically:

1. **T4 architecture lock** (skill tree + T4 count + skill point economy + respec rules) — Wave 2-3 inputs
2. **T4-attuned gear architectural specifics** — Wave 4 inputs
3. **Full gear details all rarities × all slots + character sheet stats + per-slot fill rules** (Q7 amendment) — Wave 1 inputs
4. **First-pass class chain architecture** — Wave 2 inputs
5. **Power-level targets per progression node** (GAP 1) — Wave 3 + Wave 4 validation inputs
6. **WR-bracket definition per cell + node** (GAP 7) — Wave 4 + Wave 5 validation inputs
7. **Cohort archetype definitions** (GAP 4) — Wave 4 sim methodology inputs
8. **Trait constellation completeness audit** (GAP 5) — Wave 2 input verification
9. **Resource model verification per cell type** (GAP 6) — Wave 2 + Wave 3 input verification

Session output → gandalf updates T4 PM1 prep doc → becomes T4 PM1 ratification artifact → Cycle 13 scope-doc authoring fires (KR or gandalf) → Cycle 13 launches.

---

## 1. Session pre-reads (gandalf)

Re-read in order (≤15 min total):

1. `canonical/00-ground-state.md` (current state oracle)
2. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (Cycle 13 architectural foundation; 86 locked decisions across 5 design blocks)
3. `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (engine workflow + § 0.5 content lifecycle dependency chain)
4. `canonical/02-roadmap.md` (engine build visual-flow tracker — § 3 ASCII flow for visual gap inspection)
5. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` (RATIFIED 2026-05-26; Q1-Q11 + amendments locked)
6. `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` (T4 PM1 prep doc; will be updated by this session's outputs)
7. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8-axis BC operational truth)
8. `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 cell-targeting; Sketch F)
9. `canonical/story/skill-system-2026-05-24.md` (skill composition; resource model context for GAP 6)
10. `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4 architecture defaults; predecessor to doc 40 multi-T4 lock)

Optional deeper reads if specific gap surfaces:
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (composition policy v1 for WR-bracket context)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (convergence math for sim methodology context)

---

## 2. Session agenda (proposed structure; ~2-4 hrs)

### Block A — T4 + skill tree architecture lock (~45-75 min)

Resolves Q7 items 1-4 + 6 (from Cycle 13 framing brief) + NEW T4-failure-handling decision (Matt 2026-05-26 surfaced):

| Decision | Options to consider |
|---|---|
| **Skill tree architecture** (Q7 item 1; D69) | LE-style per-skill mini-trees vs chain-based investment vs hybrid |
| **T4 count per class** (Q7 item 2; D70/D83) | Locked at chain count - 1 per D83; specific chain counts per class need decision (e.g., do all classes have 3 chains, or variable 3-4?) |
| **Skill point economy** (Q7 item 3; D71) | Per-point allocation vs per-chain unlock vs hybrid; total budget per character |
| **Respec rules** (Q7 item 4; D73) | Composes with D65 respec-with-legendary-trigger mechanism; specifics of base respec cost / time / opportunity cost |
| **First-pass class chain architecture** (Q7 item 6) | Which classes have which chains; hybrid/multi-element design (e.g., fire-primary + lightning-secondary class chain structure per D83) |
| **T4-failure-handling** (NEW — Matt 2026-05-26): when expected T4 count fails WR-bracket validation, what happens? | **Recommended Option F (hybrid):** (1) algorithm regenerates failing T4 with alternate strategies from registry (3 attempts, configurable per D62 compute budget); (2) if all regeneration attempts fail, ship character with partial T4 (in-band subset; chain keeps T1-T3 nodes but no functional capstone); (3) minimum threshold = ≥1 T4 in-band for character to ship at all; (4) track regeneration rate as quality metric. Alternatives: Option A (downgrade class to fewer chains), Option B (scrap whole character), Option C (ship with partial T4 without retry), Option D (retry only), Option E (substitute T4 across chains). Architectural fit reasoning per gandalf 2026-05-26 analysis: composes with D1 + D67 + D65 + Q10 + D62. |

**Session output:** lock decisions; capture in updated T4 PM1 prep doc

### Block B — Gear architecture lock (~45-60 min)

Resolves Q7 item 5 + Q7 items 7-9 (from Q7 amendment):

| Decision | Options to consider |
|---|---|
| **T4-attuned gear architectural specifics** (Q7 item 5; D38) | Attunement bonus magnitudes (1.5x match, 0.8x mismatch?); cross-rarity attunement distribution; set bonus structure (2pc/4pc/full); binary vs graduated attunement |
| **Full gear details all rarities × all slots** (Q7 item 7) | Per-rarity per-slot specifications; item categories; base stats; modifier surface availability per rarity; capability toolkit applicability per rarity tier |
| **Character sheet stats — full enumeration** (Q7 item 8) | The 20-40 modifier types the character stat sheet supports (damage / defense / resource / crit / speed / resistance / on-trigger / etc.) |
| **Per-gear-slot fill rules** (Q7 item 9) | Which slots roll which modifier types; probability + magnitude rules per slot per modifier; tier-restricted modifier availability |

**Session output:** lock gear architecture intent; capture detailed enough that Wave 1 partition cycle can operationalize without re-litigating intent

### Block C — Phase 3 validation calibration (~45-60 min)

Resolves GAPS 1 + 4 + 7 from Q2 gap analysis:

| Decision | Options to consider |
|---|---|
| **Power-level targets per progression node** (GAP 1) | Specific numerical targets for early game / mid game / endgame start / endgame [85% target] — what does "in-band" mean numerically per node? |
| **WR-bracket definition per cell + node** (GAP 7) | What does within-rate / within-band mean numerically per BC cell per progression node? |
| **Cohort archetype definitions** (GAP 4) | Specific definitions for DPS-min-maxer / balanced / defensive / hybrid — node investment patterns; gear preferences; play style; KPM expectations per cohort |

**Session output:** lock calibration anchors OR explicit "delegate to gamora methodology consultation with these constraints" decision

**Important framing:** Matt may choose to ANCHOR specific numbers OR delegate to empirical iteration. Both are valid per balance-as-property discipline (D1). If delegating: name the empirical-iteration discipline (e.g., "first-cycle calibration uses gamora's best estimate; cross-season learning per D25 refines").

### Block D — Audit + verification (~30-45 min)

Resolves GAPS 5 + 6 from Q2 gap analysis:

| Item | What to verify |
|---|---|
| **Trait constellation completeness** (GAP 5) | Audit current trait pool against expected coverage; identify gaps; decision whether trait pool needs expansion in Cycle 13 OR is sufficient for first season |
| **Resource model per cell type** (GAP 6) | Verify skill-system canonical covers mana/cooldown/resource mechanics for caster cells; verify martial cells have appropriate resource model (stamina? energy? other?); identify gaps |
| **Test encounter content for gauntlet sim** (GAP 2) | Audit existing test content for 4-node calibration; decision whether existing content is sufficient OR new node-calibrated encounter content needs generation in Cycle 13 |
| **Degenerate-state detection mechanics** (GAP 3) | Decision on whether gauntlet sim implements explicit degenerate-state checks (stunlock / zero-damage / mandatory locks) OR relies on KPM-out-of-band as proxy |

**Session output:** verification report; any audit findings get added to Cycle 13 scope as additional work-units OR explicitly out-of-scope

### Block E — Session close + handoff (~15-30 min)

1. Update `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` with session outputs
2. Update Cycle 13 framing brief Q7 amendment with concrete outputs (if material)
3. Author Cycle 13 scope-doc OR confirm KR can fire scope-doc dispatch with current inputs
4. Update roadmap § 3 visual flow: any items that moved from ❌ to ⏳ (work-unit now defined) or to ✅ (decision landed)
5. Commit + push

---

## 3. Open architectural recognitions to surface during session

Items I want to flag DURING the session for explicit decision (not let drift):

1. **Cycle 14+ partitioning locked Pattern A** (per Q9 amendment) — Cycle 14 = Phase 5; Cycle 15 = Phase 6; Cycle 16 = Phase 7+8 → engine build COMPLETE → REINCARNATED-GAME UNLOCK. Verify Matt still comfortable with this.

2. **Auto-combat correction is canonical** — doc 40 § 1 captures explicitly. No drift expected but worth reconfirming during gear architecture discussion (Block B) since gear flavor decisions could implicitly assume execution model.

3. **Spec-driven gear gen mirrors T4 algorithm pattern** (doc 40 D7) — when designing gear specifics in Block B, ensure the design supports scored-candidate strategy registry pattern (consistency with T4 algorithm).

4. **Heroic Spirit narrative cohesion** (doc 40 D36) — when designing T4 + gear architecture, ensure narrative resonance: T4 paths = aspects of Spirit; T4-attuned gear = evidence of latent aspects.

5. **No revert / commitment-to-consequence discipline** (D79) — applies broadly; surface if any gear decision implies reversibility.

---

## 4. Probable session output artifacts

| Artifact | Path | Purpose |
|---|---|---|
| Updated T4 PM1 prep doc | `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` | Captures all design decisions from session; becomes Cycle 13 scope-doc input |
| Updated Cycle 13 framing brief | `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` | Q7 amendment concrete outputs added; framing brief stays RATIFIED |
| Optional: new canonical doc | `canonical/41-stat-sheet-modifier-partition-INTENT-2026-XX-XX.md` | If gear architecture intent (Block B) is substantial enough to warrant canonical capture before Wave 1 partition cycle operationalizes |
| Optional: Phase 3 calibration anchor doc | `canonical/story/phase-3-calibration-anchors-2026-XX-XX.md` | If GAPS 1+4+7 produce numerical anchors worth canonical capture |
| Updated roadmap | `canonical/02-roadmap.md` § 3 | Status icon updates for decisions that landed during session |
| Cycle 13 scope-doc | `agentic_orchestration/cycles/cycle-13-mechanical-engine-build-scope.md` | If session produces enough inputs for gandalf to author scope-doc; OR defer to post-session KR-fired dispatch |

---

## 5. Session pacing protocol

- **Time-box each block** to prevent drift; if a block exceeds estimate by 50%, escalate the decision (continue OR defer specific item)
- **Empirical-iteration discipline available** for any calibration item (per Block C) — Matt can choose to anchor OR delegate to gamora consultation
- **Substrate-led discipline applies** — don't pre-impose decisions where substrate could vote (e.g., if WR-bracket can emerge from empirical iteration, defer to gamora)
- **Recognition → validate → commit discipline** — recognitions land; commitments fire only when empirical validation criterion is reachable

---

## 6. Composition with knight-rider hive-mind session

Session output feeds knight-rider Cycle 13 launch:

1. Session produces design inputs (this doc § 4 outputs)
2. KR consumes Cycle 13 framing brief (RATIFIED) + scope-doc (post-session) + roadmap (updated)
3. KR fires Wave 0 dispatch per ratified wave structure
4. Cycle 13 launches

If session produces partial outputs (some blocks deferred), KR can still fire Wave 0 with available inputs; subsequent waves gate on deferred blocks' completion.

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Session participants:** Matt + gandalf (Pattern-B)
**Estimated duration:** 2-4 hrs single session OR 2-3 sub-sessions of 60-90 min
**Session output:** all Cycle 13 wave inputs locked OR explicitly delegated to methodology consultation; T4 PM1 prep doc updated; framing brief Q7 concrete outputs added; KR launch-ready

**Signed:** gandalf
**For:** focused Matt + gandalf design session covering T4 PM1 expanded scope (Q7 amendment) + Phase 3 gap-closure (7 gaps from roadmap review). By session end, every Cycle 13 step has design inputs needed to fire. KR consumes outputs and launches Cycle 13.
