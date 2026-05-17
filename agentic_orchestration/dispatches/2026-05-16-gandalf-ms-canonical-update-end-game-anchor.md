# Dispatch — 2026-05-16 — gandalf — MS canonical update: end-game anchor verdict reversal

**From:** knight-rider (authored per Matt directive Day-4 close: "authorize all four" — gandalf's direct ask for permission to update canonical MS doc + roadmap)
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4 (verdict reversal direct authorization)
**Status:** PENDING
**Estimated effort:** ~30-45 min (canonical doc revision + roadmap section update)

**Gate-1 bypass rationale:** Matt-directed, single-seam (gandalf canonical only), reversible (doc updates), follows established gandalf canonical-doc authoring pattern.

**Acceptance summary:** `canonical/story/movement-speed-baseline.md` updated with verdict reversal — end-game-anchored values (player 8.0 m/s; fast-monster 7.5 m/s; AI_SPEED_MULTIPLIER 0.719) supersede prior mid-game-target Option-A framing. `canonical/16-project-roadmap.md` § VS2a updated with "end-game playtest" framing supersession + explicit trade-off note (VS2a no longer tests early-game progression feel — that's Playtest Cycle 1 question).

---

## Why this dispatch exists

Matt reversed the mid-game-target stance: "End game Movespeed and Monster vs player ratios for movespeed aren't reaching the sim. Also I changed stance to end game move speed versus mid game."

You filed a recommendation with three matched specific values:
- **Player end-game:** 8.0 m/s (was 7.5)
- **Monster fast-archetype:** 7.5 m/s (was 6.6 mid-range)
- **AI_SPEED_MULTIPLIER:** 0.719 (was 0.767)

These numbers anchor the entire downstream cascade (rocket schema defaults → star-lord Stage B export-DTO → gamora Gate 3b sim consumption → drax JSON consumption → decisions-log supersession). Your canonical update is the head of the cascade.

## Cross-seam contract change?

**Round-trip: not applicable** — canonical doc + roadmap update; no schema or runtime contract change here. The contract change propagates downstream via rocket schema defaults; that dispatch carries its own round-trip discipline. Per R11(b) Principle 6.

## What this dispatch produces

### Track 1 — canonical/story/movement-speed-baseline.md verdict reversal

Update the doc with:
- **Supersession header at top:** "2026-05-16 verdict reversal — end-game-anchored MS values now in effect; prior mid-game-target Option-A framing superseded. See cascade items 2-6 for downstream propagation."
- **Numbers table** matching what you filed (player 5.75 L1 unbuffed / 8.0 end-game gear-only; monster trash 5.75 / fast 7.5; AI_SPEED_MULTIPLIER 0.719; PIXELS_PER_METER 48 unchanged)
- **Rationale section** explaining: 9.5 m/s (original AI_SPEED_MULTIPLIER 0.605 anchor) assumed D2-style active MS skill buffs which Phase 0 has no plan to ship; end-game-gear-only is 8.0; 0.719 is the operational AI_SPEED_MULTIPLIER. Fast-archetype 7.5 m/s = chase margin 0.5 m/s = 24 px/s = genre-correct "fast monsters are practically threatening at endgame" feel.
- **Sim-consumption gating clause:** the "no point playing a game which is not ran through the sim" framing; balance loop kiting math + pack-encounter convergence + boss-arena traversal all depend on sim consuming the same values demo plays.

### Track 2 — canonical/16-project-roadmap.md § VS2a framing update

Update the roadmap VS2a section with:
- **Reframing:** "VS2a is end-game playtest. The gauntlet shows what the player experiences at end-of-progression. Sim and demo agree on the same values; what the player feels IS what the engine balanced for."
- **Explicit trade-off note:** VS2a deliberately does NOT validate early-game progression feel; that's a Playtest Cycle 1 question.
- **Cross-reference** to the canonical/story/movement-speed-baseline.md supersession.

### Optional — cross-reference any other canonical docs

If you find related canonical docs that reference the old mid-game values, surface them in your completion record for knight-rider to route follow-on amendments. Do NOT cascade-amend without explicit scope (avoids scope creep).

## Out of scope (explicit)

- **NO schema edits** — rocket's seam (separate dispatch firing in parallel)
- **NO export-DTO touchpoints** — star-lord's seam (separate dispatch, queued after Stage 3 returns)
- **NO sim-consumption code** — gamora's seam (separate Gate 3b dispatch firing in parallel)
- **NO demo code** — drax's seam (separate dispatch, queued after rocket + star-lord land)
- **NO decisions-log entry** — knight-rider drafts after your canonical update lands + Matt approval
- **NO unilateral cascade-amendment of other canonical docs** — surface for routing only

## Required reading

- Your filed recommendation (the analysis Matt relayed — old/new values table + cascade table + sim-consumption framing)
- Existing `canonical/story/movement-speed-baseline.md` (the doc to update)
- Existing `canonical/16-project-roadmap.md` § VS2a (the section to update)
- `canonical/story/style-register.md` + `canonical/story/enemy-visual-legibility.md` (consistency-check anchors)

## Acceptance criteria

- [ ] `canonical/story/movement-speed-baseline.md` updated with supersession header + numbers + rationale + sim-consumption gating clause
- [ ] `canonical/16-project-roadmap.md` § VS2a updated with end-game-playtest framing + explicit trade-off note
- [ ] Cross-references between the two docs present
- [ ] Knight-rider notified with: doc paths, any other canonical docs flagged for follow-on amendment, any open questions for Matt before the decisions-log supersession can be drafted

## Tag policy

- No git tag (canonical-doc persona convention)

---

## Completion record

**Completed:** 2026-05-16 (Day 4 close, gandalf)
**Status:** COMPLETE

**Updated docs:**
- `canonical/story/movement-speed-baseline.md` — Verdict-reversal section expanded with three new subsections: (1) "Rationale — why 8.0 (not 9.5), why 7.5 fast-monster, why 0.719" naming the D2-style-buffs assumption that 9.5 would have papered over, the 24 px/s chase margin = genre-correct end-game kiting math, and the operational AI_SPEED_MULTIPLIER derivation; (2) "Sim-consumption gating clause" with Matt's "no point playing a game which is not ran through the sim" framing operationalized via three concrete consequences (balance-loop kiting math, pack-encounter convergence, boss-arena traversal) plus the four-seam single-source-of-truth commitment.
- `canonical/16-project-roadmap.md` § VS2a — three updates: (1) "Out of scope" section gained an "Explicit non-coverage (end-game-anchor framing)" subsection naming VS2a as end-game playtest, with the explicit trade-off that VS2a does NOT validate early-game progression (deferred to Playtest Cycle 1 post-Stage-A2-closeout); (2) seam-allocation table row 76 corrected — gamora Gate-3b is now VS2a-gating (was "post-VS2a, not gating"); (3) Ship-trigger row 84 updated with end-game-anchored language + cross-reference to the verdict-reversal section.

**Other canonical docs flagged for follow-on amendment (surface only; NOT amended per dispatch out-of-scope):**

1. **`canonical/story/arena-room-hallway-system.md`** — Lines 74 + 159 + 206 reference the old AI_SPEED_MULTIPLIER 0.767 and "chase margin 84 px/s" values from Option A. Needs amendment to 0.719 + "chase margin per movement-speed-baseline.md § Verdict Reversal" (current concrete number is 24 px/s for fast-archetype:player, not 84 px/s which was the trash:player margin under Option A). Room-sizing implications: 30m default room cross now 3.75s at 8.0 m/s (was 4.0s at 7.5); may want to re-check arena-sizing rationale doesn't need adjustment.

2. **`canonical/story/engine-balance-stewardship.md`** § Gate 3 Recommendation 3b — Line 305 still describes Gate 3b as "tightly-following post-VS2a ticket targeting VS2a+2-4 weeks." This is now stale; per verdict reversal, Gate 3b is VS2a-gating. The 2026-05-16-update note inside Recommendation 3b needs a second update naming the Day-4 verdict reversal.

3. **`reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`** § "Stage A2 movement-speed sim extension (engine-balance-stewardship lock 3b)" — gamora's queued consumer flag — should be re-classified from "Stage A2" to "VS2a-gating." (This is engine repo, not canonical, but it's the gamora-side reference cited from movement-speed-baseline.md companion-docs list. Gamora's seam dispatch carries it.)

4. **`canonical/story/drift-audit.md`** Drift-9 + Drift-11.A — Drift-9 currently described as resolved by movement-speed-baseline.md authorship; that resolution stands but the resolution state now includes the Day-4 verdict reversal. Worth a one-line amendment naming Option B as the operative resolution. Drift-11.A description ("baseline subset in VS2a scope") similarly stands but is now sharper (full Gate 3b is also in VS2a scope, not just baseline subset).

**Open questions for Matt before knight-rider drafts the decisions-log supersession:**

- **None blocking.** The values are locked per gandalf's recommendation that Matt accepted without revision. The decisions-log entry can be drafted as a supersession against the Option-A entry committed earlier today, locking the Option-B values + sim-consumption-as-VS2a-gating framing.
- **Possible Matt confirmation worth gathering** (not blocking): the four follow-on amendments listed above can be cascade-routed as a single knight-rider sequencing batch (light-touch amendments to arena-room-hallway-system + engine-balance-stewardship + drift-audit + the engine AGENT_STATE.md flag). Matt may want to know these amendments are pending before the decisions-log entry lands, so the decisions-log supersession can reference the full cascade rather than just the two doc updates this dispatch produced.

**Notes for knight-rider:**
- Cross-references between the two updated docs are in place (movement-speed-baseline.md → roadmap entry; roadmap → movement-speed-baseline.md § "Verdict Reversal" — both directions).
- Cascade items 2-6 (rocket schema, star-lord export DTO, gamora Gate 3b, drax demo, decisions-log supersession) are unblocked by this canonical-doc update. The four follow-on canonical amendments listed above are light-touch and do not block downstream cascade execution; they can be batched after the decisions-log supersession lands.
- No git tag per canonical-doc persona convention.
