# Dispatch — 2026-05-16 — gandalf — Canonical follow-on amendments batch (4 docs)

**From:** knight-rider (authored per Matt directive Day-4 close: "fire all and palette-shift on god-of-lightning" — authorizes the gandalf canonical-amendments batch)
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Mode:** Design-track analytical (canonical-doc amendments)
**Estimated effort:** 1 session (~45-60 min); 4 small canonical-doc amendments + 1 style-register reconciliation note

**Gate-1 bypass rationale:** Matt-directed batch; single-seam (gandalf canonical only); reversible (doc amendments); small scope per individual amendment. Per CHANGELOG rubric.

**Acceptance summary:** Four canonical docs amended per the carryforward items from your MS canonical update + per-slug Path A returns. (1) `arena-room-hallway-system.md` — AI_SPEED_MULTIPLIER + chase-margin + room-cross-time amendments; (2) `engine-balance-stewardship.md` § Gate 3b line 305 — VS2a-gating update; (3) `drift-audit.md` — Drift-9 + Drift-11.A one-line amendments; (4) `style-register.md` — reconciliation note that 80-100 px is *register aesthetic reference* not *operational pixel-count constraint*. Knight-rider notified.

---

## Why this dispatch exists

Two of your earlier Day-4 returns surfaced carryforward amendments:

**From MS canonical update return** (gandalf MS canonical dispatch completion record):
- `arena-room-hallway-system.md` lines 74, 159, 206 reference old AI_SPEED_MULTIPLIER 0.767 + chase margin 84 px/s; need update to 0.719 + 24 px/s + room-cross time re-check (3.75s at 8.0 m/s vs 4.0s at 7.5 m/s)
- `engine-balance-stewardship.md` § Gate 3 Recommendation 3b line 305 — "tightly-following post-VS2a ticket" is stale; per verdict reversal, Gate 3b is VS2a-gating
- `drift-audit.md` Drift-9 + Drift-11.A — one-line amendments naming Option B as the operative resolution; Drift-11.A description sharpens

**From per-slug Path A lookup table return** (gandalf per-slug dispatch completion record):
- `style-register.md` references "80-100 px HD-2D target"; Path A renders chierit at ~44 px (Option (i) chosen). Recommend clarification note that 80-100 px is *register aesthetic reference* not *operational pixel-count constraint* on the project's specific source assets. Non-blocking; small.

Note: `simulation/AGENT_STATE.md` gamora-flag re-classification (also flagged) is engine-repo (out of your lane); knight-rider routes via gamora-seam carryforward, NOT included in this batch.

## Cross-seam contract change?

**Round-trip: not applicable** — canonical-doc amendments only; no schema or runtime contract change. Per R11(b) Principle 6.

## What this dispatch produces

### Amendment 1 — arena-room-hallway-system.md

Lines 74, 159, 206 (per your earlier note):
- AI_SPEED_MULTIPLIER: 0.767 → **0.719**
- Chase margin: 84 px/s (trash:player under Option A) → **24 px/s (fast-archetype:player under verdict-reversal end-game anchor)** OR reference "per movement-speed-baseline.md § Verdict Reversal" if cleaner
- Room-cross time check: 30m default room cross now **3.75s at 8.0 m/s** (was 4.0s at 7.5 m/s); confirm room-sizing rationale doesn't need adjustment

### Amendment 2 — engine-balance-stewardship.md § Gate 3 Rec 3b

Line 305 — update the "tightly-following post-VS2a ticket targeting VS2a+2-4 weeks" framing. Per verdict reversal, Gate 3b is **VS2a-gating**. Append a Day-4 update note naming the verdict reversal + cross-reference to `movement-speed-baseline.md` § Verdict Reversal.

### Amendment 3 — drift-audit.md (Drift-9 + Drift-11.A)

Per your earlier note:
- Drift-9: one-line amendment naming Option B as operative resolution
- Drift-11.A: description sharpens (full Gate 3b also in VS2a scope, not just baseline subset)

### Amendment 4 — style-register.md reconciliation note

Add a clarification note (small section addition; do NOT rewrite the doc):
- The "80-100 px HD-2D target" cited in the doc refers to the **register aesthetic reference** (Sea of Stars / Octopath overworld camera precedent at displayed 1080p resolution per legolas ground-truth)
- It is NOT an **operational pixel-count constraint** on the project's specific source assets
- Path A operationalization: chierit at native 1.0× scale → ~44 px player baseline; monsters scaled to Path A tier ranges (per `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md`)
- The register commitment is preserved; the operational pixel-count is derived per-asset rather than asserted as a universal floor

### Cross-references — add bidirectional links

Each amendment should add cross-reference link to:
- `canonical/story/movement-speed-baseline.md` § Verdict Reversal (for amendments 1-2)
- `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md` (for amendment 4)
- `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (for amendment 4)

## Out of scope (explicit)

- **NO simulation/AGENT_STATE.md amendment** (engine-repo; gamora-seam carryforward; knight-rider routes via gamora dispatch)
- **NO new canonical authoring beyond the 4 amendments** (style-register reconciliation note is a small addition, not a rewrite)
- **NO decisions-log entry** (knight-rider drafts MS supersession in qa/pending separately)
- **NO unilateral cascade-amendment of additional canonical docs** beyond the 4 listed (surface for routing)
- **NO Path A re-anchor re-justification** (locked by Matt; lookup table is the authoritative operationalization)

## Required reading

- Your MS canonical update completion record (carryforward list)
- Your per-slug Path A lookup table doc: `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md`
- Existing `canonical/story/arena-room-hallway-system.md`
- Existing `canonical/story/engine-balance-stewardship.md` § Gate 3
- Existing `canonical/story/drift-audit.md`
- Existing `canonical/story/style-register.md`

## Acceptance criteria

- [ ] arena-room-hallway-system.md amended (lines 74/159/206; AI_SPEED_MULTIPLIER + chase margin + room-cross time)
- [ ] engine-balance-stewardship.md § Gate 3 Rec 3b line 305 amended (VS2a-gating update + cross-reference)
- [ ] drift-audit.md Drift-9 + Drift-11.A amendments
- [ ] style-register.md reconciliation note added (Path A operationalization clarification)
- [ ] Cross-references between amended docs and the source-of-truth canonical docs
- [ ] Knight-rider notified with: doc paths, any additional canonical docs flagged for follow-on (surface only)

## Tag policy

- No git tag (canonical-doc persona convention)

---

## Completion record

**Completed:** 2026-05-16 Day-4 close (gandalf)
**Status:** COMPLETE

**Docs amended (4 per dispatch + 1 bidirectional back-link):**

1. `canonical/story/arena-room-hallway-system.md` — three line-level amendments + companion-doc cross-reference header:
   - § "Aggro state machine" (was line 74): AI_SPEED_MULTIPLIER 0.767 → **0.719** (= 5.75 / 8.0); cited Verdict Reversal section as source-of-truth; noted Option A → Option B supersession
   - § "Re-validation needed" (was line 159): chase margin 84 px/s → **24 px/s** (fast-archetype 7.5 m/s vs player end-game 8.0 m/s; differential 0.5 m/s × 48 px/m); explained the shift in chase-margin signal (trash:player under Option A → fast-archetype:player under Option B); noted trash now lag end-game player by 108 px/s (the "outrunnable trash" feel)
   - § "Room geometry" (was line 206 area; updated default-size annotation): room-cross time 4.0s at 7.5 m/s → **3.75s at 8.0 m/s**; confirmed **room-sizing rationale does not require adjustment** — geometry (30m × 30m at 48 px/m = 1440 × 1440 px) preserved; only the time-per-traversal and AI-speed ratio recalibrate; 3.75s end-game cross-time still produces D2/PoE clear-room-rhythm feel
   - Added Day-4 amendment header note at top of doc + updated companion-doc cross-reference to specifically cite `movement-speed-baseline.md` § "Verdict Reversal 2026-05-16" as source-of-truth

2. `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b line 305:
   - Added a Day-4 close update block that **supersedes** the morning's "schedule, now / tightly-following post-VS2a ticket targeting VS2a+2-4 weeks" framing
   - Gate-3b sim consumption is now **VS2a-gating** (not post-VS2a) — engine consumes end-game-anchored MS values (player 8.0, trash 5.75, fast 7.5, AI_SPEED_MULTIPLIER 0.719) + emits in convergence-loop telemetry packet before VS2a ships
   - Cross-reference to `movement-speed-baseline.md` § "Verdict Reversal" as source-of-truth + noted Gate-3b body below is preserved for design-rationale archaeology only
   - Quoted Matt's framing: *"No point playing a game which is not ran through the sim."*

3. `canonical/story/drift-audit.md` (Drift-9 + Drift-11.A):
   - **Drift-9 (Q2 movement empirically unknown)**: Day-4 amendment names **Option B (end-game-anchored: player 8.0, trash 5.75, fast 7.5, AI_SPEED_MULTIPLIER 0.719) as operative resolution**; both baseline-anchor portion AND full Gate-3b sim-consumption portion VS2a-gating; Option A (mid-game 7.5, multiplier 0.767) superseded
   - **Drift-11 Instance A (Movement-speed baseline)**: description sharpens — not only baseline-anchor subset but **full Gate-3b sim-consumption portion is also in VS2a scope**, not "tightly-following post-VS2a ticket"; surfaces the lesson that the implicit-deferral pattern bit twice on this same instance (caught earlier for baseline; caught at Day-4 close for sim-consumption); recommends: when a deferred milestone surfaces ONE upstream-of-near-term-ship dependency, **sweep the rest of the deferred milestone for sibling dependencies in the same session** — they tend to cluster

4. `canonical/story/style-register.md` reconciliation note (NEW small section, not rewrite):
   - Added § "Path A reconciliation — '80–100 px HD-2D target' is register aesthetic reference, not operational pixel-count constraint (added 2026-05-16 Day 4)"
   - Clarifies: 80–100 px is **register aesthetic reference** (Sea of Stars / Octopath Traveler overworld camera precedent at displayed 1080p per legolas ground-truth) — NOT an operational pixel-count constraint on Reincarnated's specific source assets
   - Path A operationalization: chierit native 1.0× → ~44 px player baseline; monsters scaled to Path A tier ranges (trash 26–37 / elite 44–57 / mini-boss 66–88 / boss 110–176)
   - Path B (upscale to 80 px) rejected by Matt on player-experience + viewport-pressure grounds
   - HD-2D aesthetic preserved at 44 px chierit baseline (register lock survives Path A intact)
   - Cross-references per-slug-scale-lookup-path-a + sprite-scale-math-impossibility-rulings + legolas pixel-scale research § 3
   - Updated end-of-doc Cross-references section to include the two new Path A canonical docs
   - Q1 open question ("specific fidelity target") partially-resolved to: per-source-asset-derived, not universal-target-asserted

**Bidirectional back-link (small):**

5. `canonical/story/per-slug-scale-lookup-path-a-2026-05-16.md` § "Style-register reconciliation" — appended one-line "LANDED" note to the existing "Action item for style-register.md" paragraph completing the bidirectional cross-reference loop

**Additional canonical docs flagged for follow-on routing (surface only, NOT amended per hard out-of-scope):**

- `canonical/16a-roadmap-shipped-log.md` line 152 — shipped-log entry naming AI_SPEED_MULTIPLIER=0.767 + mid-VS2a 7.5 m/s. Stale per Option B verdict reversal. **Shipped-log is knight-rider-owned historical log** — knight-rider's call whether to amend an already-shipped-log entry in-place (correction) vs append a supersession entry. Surface only; no gandalf action.
- `canonical/story/embodiment-display-loadout.md` line 68 — references "JRPGs have TWO cameras (overworld 80-100 px / battle 75-130 px..." in comparative-genre context. **Probably does NOT need amendment** — reference is about JRPG-genre architecture (comparative anchor), not about Reincarnated's pixel-count operational floor. Surface only; non-blocking. Knight-rider's call if a small forward-reference to the new Path A reconciliation section would aid future readers.

**Notes for knight-rider:**

- All 4 amendments are reversible doc edits; no schema or runtime contract change touched; R11(b) Principle 6 round-trip not applicable.
- Source-of-truth concentration preserved: all operational values for player MS / trash MS / fast-archetype MS / AI_SPEED_MULTIPLIER / chase-margin / room-cross-time continue to live at `movement-speed-baseline.md` § "Verdict Reversal 2026-05-16"; the four amended docs cross-reference that section rather than duplicating the derivations.
- The Drift-11 sharpening (sibling-cluster lesson) is a genuine pattern-extension worth surfacing to engineering-disciplines.md authoring (jack-ryan lane) if knight-rider sees value — recommend NOT a separate amendment, but as input to the next discipline pass.
- No git tag (canonical-doc persona convention; gandalf-seam).
