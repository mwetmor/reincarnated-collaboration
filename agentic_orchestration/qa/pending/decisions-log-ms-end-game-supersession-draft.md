# Draft — decisions-log entry — MS end-game-anchor supersession

**Drafted by:** knight-rider 2026-05-16 (Day 4 close)
**Target file:** `reincarnated-engine/design/decisions/decisions-log.md`
**Status:** PENDING Matt approval; pending jack-ryan Gate 1 review
**Awaiting:** Matt's go-ahead → knight-rider commits to decisions-log.md

---

## Draft entry text (for Matt review)

---

### 2026-05-16: Movement-speed baseline — end-game anchor supersedes mid-game-target framing (Day-4 verdict reversal)

**Status:** ACCEPTED + IN-CASCADE

**Context:** Prior MS baseline decision (locked earlier in B-series) anchored on a mid-game-target player movement speed (5.75 m/s L1 unbuffed; ~7.5 m/s mid-game target with limited gear). Drax demo hardcoded mid-game values and engine schema was effectively decorative for VS2a — sim consumed one set of values, demo rendered another. The "no point playing a game which is not ran through the sim" framing surfaced at Day-4 close when Matt observed end-game movespeed + monster:player ratios weren't reaching the sim.

**Decision:** End-game-anchored MS values supersede the mid-game-target framing. VS2a is reframed as end-game playtest (the gauntlet shows what the player experiences at end-of-progression; sim and demo agree on the same values).

**Locked values:**
- **Player end-game movement_speed:** 8.0 m/s (gear-only end-game; no MS-skill-buffs in palette through Phase 0)
- **Player L1 unbuffed:** 5.75 m/s (unchanged baseline)
- **Monster trash movement_speed:** 5.75 m/s (unchanged)
- **Monster fast-archetype movement_speed:** 7.5 m/s (top of locked range; chase margin 0.5 m/s = 24 px/s = genre-correct end-game kiting feel)
- **Monster named-boss movement_speed:** gamora-design-call per-boss (flagged by rocket schema dispatch)
- **AI_SPEED_MULTIPLIER:** 0.719 (= 5.75 / 8.0)
- **PIXELS_PER_METER:** 48 (unchanged; inlined in `src/world/topology.ts` per drax v0.20.1 circular-import fix)

**Rationale:**
- Prior AI_SPEED_MULTIPLIER 0.605 anchored on 9.5 m/s player assumed D2-style active MS skill buffs (Vigor / Burst of Speed). Phase 0 has no MS-buff geometries in palette and no plan to ship them. End-game-gear-only is 8.0; 0.719 is the operational AI_SPEED_MULTIPLIER.
- 7.5 m/s fast-archetype produces chase margin 24 px/s — genre-correct "fast monsters are practically threatening at endgame" feel per gandalf's Diablo+PoE+D4 reference framework.
- Sim consumption is the math layer making balance-loop output trustworthy for movement-affected encounters (kiting math; pack-encounter convergence; boss-arena traversal).

**Supersedes:**
- Prior MS baseline lock (mid-game-target framing in `canonical/story/movement-speed-baseline.md` pre-verdict-reversal sections)
- Gate 3b "post-VS2a tight follow" framing in `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b line 305 (promoted to VS2a-gating per `arena-room-hallway-system.md` amendments)

**Cascade execution (6 steps, per gandalf MS recommendation table):**

| # | Owner | Change | Status as of 2026-05-16 close |
|---|---|---|---|
| 1 | gandalf | `canonical/story/movement-speed-baseline.md` verdict-reversal + `canonical/16-project-roadmap.md` § VS2a end-game-playtest framing | COMPLETE |
| 2 | rocket | Schema defaults: PlayerClass.movement_speed=8.0; Monster.movement_speed per-archetype | IN-FLIGHT (`rocket/v1.3-ms-schema-defaults-end-game`) |
| 3 | star-lord | Stage B export-DTO fix: ExportClass + ExportMonster ship `movement_speed` field through consolidated JSON | IN-FLIGHT (`star-lord/v1.3-stage-b-export-dto-movement-speed`) |
| 4 | gamora | Gate 3b sim consumption: kiting modeling + 3-band distance state + AI_SPEED_MULTIPLIER consumption (PROMOTED to VS2a-gating) | IN-FLIGHT (`gamora/v1.3-gate-3b-sim-ms-consumption`) |
| 5 | drax | Remove hardcoded MS in `world/movement.ts`; consume engine-emitted MS via JSON; re-derive PIXELS_PER_METER conversions | QUEUED (waits step 2 + step 3) |
| 6 | knight-rider | This decisions-log entry | DRAFTED (this doc) |

**Trade-off named explicitly:**
- VS2a no longer validates early-game progression feel. That validation moves to Playtest Cycle 1 post-Stage-A2-closeout. Documented in `canonical/16-project-roadmap.md` § VS2a "Explicit non-coverage (end-game-anchor framing)" subsection.

**Cross-references:**
- `canonical/story/movement-speed-baseline.md` § Verdict Reversal (authoritative source)
- `canonical/16-project-roadmap.md` § VS2a
- `canonical/story/engine-balance-stewardship.md` § Gate 3 Recommendation 3b (post-amendment)
- `canonical/story/arena-room-hallway-system.md` (post-amendment per gandalf canonical follow-on batch)
- `canonical/story/drift-audit.md` Drift-9 + Drift-11.A (post-amendment per gandalf canonical follow-on batch)

**Discipline notes:**
- Discipline #12 (semantic-shifting) — explicit supersession of prior MS lock with cascade table
- Discipline R11(b) (cross-seam round-trip) — each cascade dispatch carries round-trip smoke discipline at its respective contract boundary; this entry references downstream consumer dispatches rather than asserting round-trip itself

---

## Notes for knight-rider on commit timing

Hold commit until:
1. Matt approves the draft text (any revisions noted)
2. Jack-ryan Gate 1 review passes (typical ~15 min for decisions-log entries; can fire as Pattern A subagent)
3. Cascade items 2-5 all return clean (so the "Status as of" column is accurate; if a cascade item BLOCKs, surface to Matt before committing)

If any cascade item blocks: hold this entry; revise to reflect actual cascade outcome.

---

## Notes for knight-rider on related drafts pending

This is the FIRST decisions-log entry needed for the MS verdict reversal. Two additional follow-on decisions-log entries may be needed depending on outcomes:

- **Wind_controller DPS floor (gandalf Decision 1)** — post rocket DPS-floor dispatch return; if dispatch ships clean, draft separate entry per ADR-002 architectural call standard
- **Chierit scale revision + MONSTER_SCALE_BY_SLUG (Path A operationalization)** — post drax MONSTER_SCALE_BY_SLUG dispatch return; design-asset decision, may be operational rather than architectural — defer judgment until dispatch returns

These are separate entries from this MS supersession; do not bundle.
