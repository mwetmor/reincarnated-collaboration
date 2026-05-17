# Dispatch — 2026-05-16 — drax — Movement-speed PixiJS implementation (gandalf handoff #2; VS2a-ship-gating)

**From:** knight-rider (authored per gandalf's 2026-05-16 Day 4 movement-speed-baseline commission handoff item #2; HELD-gate closed by movement-speed-baseline decisions-log entry commit `303258c` on 2026-05-16)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (movement-speed-baseline entry commit `303258c` is the decisions-log gate per gandalf handoff #4; Matt explicit "author drax movement" directive following the commit)
**Status:** PENDING — ACTIVE
**Estimated effort:** ~1-2 days per gandalf handoff
**Acceptance:** Demo renders combatants at locked movement-speed values (player base 5.75 m/s → 276 px/s at 48 px/m; mid-VS2a 7.5 m/s → 360 px/s; etc.); arena-scale back-derivation verified + reported; AI multiplier re-tuned to 0.767; playtest calibration equivalent to phase 6.1/6.2 re-run; intermediate tag; VS2a demo ships visibly faster (Case-A) or unchanged-in-feel (Case-B).

---

## Context — gandalf locked values (Matt-approved per `303258c` commit)

Per the 2026-05-16 movement-speed-baseline decisions-log entry (committed `303258c`) + `canonical/story/movement-speed-baseline.md`:

| Parameter | Value | Demo px/s at 48 px/m |
|---|---|---|
| Player base MS | 5.75 m/s | 276 px/s |
| Early game | 6.0 m/s | 288 px/s |
| **Mid game (VS2a)** | **7.5 m/s** | **360 px/s** |
| Late game | 8.0 m/s | 384 px/s |
| Monster trash | 5.75 m/s | 276 px/s |
| Monster fast archetypes | 6.6–7.5 m/s | 317–360 px/s |
| **PIXELS_PER_METER** | **48 (constant)** | — |
| **AI_SPEED_MULTIPLIER (VS2a)** | **0.767** | yields trash 276 px/s vs player mid 360 px/s; 84 px/s chase margin |
| Range-profile MS variance | DROPPED | All classes uniform |

**Design-family anchor:** D3 / D4 / Last Epoch (NOT PoE-1 zoom-zoom).

## What this dispatch does (gandalf handoff #2 verbatim)

> Drax dispatch — replace `world/movement.ts` per locked values; verify arena scale against 48 px/m back-derivation; re-tune AI multiplier to 0.767; re-run playtest equivalent to phase 6.1/6.2 calibration. ~1-2 days work.

### Step 1 — Replace world/movement.ts with locked values

In `~/Games/reincarnated-demo/src/world/movement.ts` (or equivalent):
- Replace any hardcoded movement-speed values with the gandalf-locked values (using PIXELS_PER_METER=48 conversion)
- Use `movement_speed_base = 5.75` (m/s) → `276 px/s` baseline for player + monster-trash
- Player progression: 5.75 (base) → 6.0 (early) → 7.5 (mid-VS2a target) → 8.0 (late)
- Monster fast archetypes: 6.6-7.5 m/s range → 317-360 px/s; specific values per archetype (rocket's `ARCHETYPE_MOVEMENT_SPEED` lookup: swarmer/sniper = 6.60 m/s = 316.8 px/s)
- Document the PIXELS_PER_METER=48 constant explicitly in the movement.ts header comment (rationale: ties demo render to engine's locked baseline)

### Step 2 — Verify arena-scale back-derivation (the "single thing to watch" per gandalf)

In `arena.ts` (or equivalent) — verify current arena dimensions against PIXELS_PER_METER=48:

**Two possible cases (gandalf flagged both):**

- **Case A — current arena designed for ~48 px/m:** player perceives near-2× speed-up (current 180 px/s medium represents ~3.75 m/s; new mid is 360 px/s = 7.5 m/s). Will feel substantially faster. May want a brief tuning pass on arena dimensions to prevent the new speed from making the arena feel cramped.
- **Case B — current arena implicitly ~24 px/m:** the rebase is a no-op in feel — same perceived speed, just a unit clarification.

**Required output:** report which case applies in your completion record + findings. Case A may surface a follow-on arena-tuning decision (NOT a blocker for VS2a ship; flag for knight-rider).

### Step 3 — Re-tune AI multiplier to 0.767

In the AI pathing / chase logic — update the AI_SPEED_MULTIPLIER from the prior value to **0.767**.

Verification: at locked baselines, monster trash (5.75 m/s × 0.767 = 4.41 m/s = 211.7 px/s perceived chase-speed) should chase player mid (7.5 m/s = 360 px/s) with **84 px/s chase margin** per gandalf's design intent. (Note: the 0.767 multiplier yields trash 276 px/s NOT 211.7 px/s in raw render; the 84 px/s chase margin is the difference between player mid 360 and trash render 276 — verify against gandalf's exact framing in `movement-speed-baseline.md` if ambiguity surfaces.)

### Step 4 — Re-run playtest calibration equivalent to phase 6.1/6.2

Per gandalf's commission framing — re-run the playtest calibration steps that established the original movement values (phase 6.1/6.2 in gandalf's design process):
- Visual chase-feel check (does trash chase feel threatening at the new values?)
- Combat-positional check (does combatant positioning stay legible at 360 px/s mid?)
- Encounter-spatial check (does the arena feel cramped vs spacious at the new speed?)

Document playtest observations in completion record. Capture screenshots if helpful (`reincarnated-collaboration/reference_screenshots/` is the place).

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- **Intermediate tag:** `drax/v0.10-movement-speed-locked` (or your call on naming per loadout tag convention; current tag convention in loadout uses `drax/` prefix per prior dispatches)
- **AGENT_STATE.md** (loadout repo) updated with:
  - Movement-speed values locked at gandalf-baseline
  - Arena-scale back-derivation case (A or B)
  - AI multiplier 0.767 verified
  - Playtest calibration phase 6.1/6.2 equivalent re-run
- Completion record at bottom of this dispatch filled

## Cross-seam considerations

- **Gandalf:** the values + the design-family anchor are gandalf-locked + Matt-approved. No design-instinct re-litigation; you implement to-spec.
- **Rocket:** rocket movement_speed schema field SHIPPED at `rocket/v1.3-movement-speed-schema-field @ 62624dd`. Your work CONSUMES rocket's emit + PIXELS_PER_METER=48 conversion. If rocket's emit-side has any value discrepancy vs gandalf's locked baseline, surface as a finding; do NOT modify rocket's seam.
- **Gamora:** gamora's Stage A2 sim consumption (per the engine-balance-stewardship Lock 3b + the in-pending gamora movement-speed-aware sim extension dispatch — not yet authored; post-VS2a tight follow per gandalf handoff #3) — your demo-side rendering is the player-facing manifestation; gamora's sim consumption is the balance-correctness manifestation. They're parallel; no demo-side coordination needed during this dispatch.
- **Star-lord:** star-lord telemetry v2.2 observed_movement_speed SHIPPED (`db4aa09`); no coordination needed during this dispatch.
- **Knight-rider:** notify at completion with the arena-scale-back-derivation case (A or B) + playtest observations + intermediate tag hash. Case A may surface follow-on arena-tuning dispatch.

## Out of scope (explicit)

- **NO engine-side changes.** This is demo/loadout work only.
- **NO gamora Stage A2 sim consumption** (separate dispatch; post-VS2a tight follow).
- **NO season_001006 data load.** Per knight-rider's analysis 2026-05-16: deferring season-load until after gamora V2.1 emission gap fix + follow-on regen lands clean data on 001006 (currently 10 classes; tier1_populated=false; v2.1 fields NULL).
- **NO rooms-in-encounter-analytics UI** (per Matt's 2026-05-16 framing: option (a) 3rd dropdown filter OR option (b) per-class top-down with room-level — defer; separate dispatch when V2.1 emission gap fix + regen lands).
- **NO arena-tuning beyond verification.** If Case A applies + you observe cramped-arena friction in playtest, FLAG to knight-rider; do NOT execute arena re-dimensioning in this dispatch (that's a Matt-decision per gandalf's "follow-on arena-tuning decision" framing).
- **NO milestone tag.** Intermediate tag only. Milestone tag requires Matt approval per ADR-003.

## Required reading

- 2026-05-16 movement-speed-baseline decisions-log entry (committed `303258c`) — the gate for this dispatch
- `canonical/story/movement-speed-baseline.md` (gandalf's locked values; Matt-approved; source-of-truth)
- `agentic_orchestration/gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md` (gandalf's commission; handoff item #2 is your assigned scope; arena-scale back-derivation framing)
- `agentic_orchestration/dispatches/2026-05-16-rocket-movement-speed-schema-field.md` (rocket's upstream schema work; movement_speed field is now live on the engine schema)
- 2026-05-16 spatial-data-jsonschema decisions-log entry (committed `303258c`) — companion entry; the spatial-data schema lives at the same architectural layer + is also drax-rendering territory (separate future drax dispatch for spatial-data PixiJS consumption)
- `~/Games/reincarnated-demo/src/world/movement.ts` (your primary target file)
- `~/Games/reincarnated-demo/src/world/arena.ts` (or equivalent — your arena-scale verification target)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke-test: phase 6.1/6.2 playtest equivalent), #11 (attribution: cite gandalf's locked values verbatim in code comments)

## Acceptance criteria

- [ ] `world/movement.ts` replaced with gandalf-locked values (PIXELS_PER_METER=48 constant explicit)
- [ ] Player baselines wired (5.75 base; 6.0 early; 7.5 mid-VS2a; 8.0 late)
- [ ] Monster baselines wired (5.75 trash; 6.6-7.5 fast archetypes range)
- [ ] Arena-scale back-derivation verified; Case A or Case B reported in completion record
- [ ] AI_SPEED_MULTIPLIER updated to 0.767; chase-margin verified (trash chase player with 84 px/s margin)
- [ ] Playtest calibration phase 6.1/6.2 equivalent re-run; observations documented
- [ ] Intermediate tag `drax/v0.10-movement-speed-locked` (or equivalent) cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion with arena-scale-back-derivation case + playtest observations

## Tag policy

- **Intermediate tag:** `drax/v0.10-movement-speed-locked` at the commit closing the implementation pass.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

---

## Completion record

**Completed:** 2026-05-16 (drax, Day 4)
**Intermediate tag:** `drax/v0.10-movement-speed-locked` @ `151c7ec` (branch `stage-a2`)

**Arena-scale back-derivation case (A or B):** **CASE A**

Back-derivation: arena ellipse ELLIPSE_RX=784 px. At 48 px/m → 784/48 = 16.33 m semi-axis;
full arena width = 32.67 m. Current "medium" speed was 180 px/s = 180/48 = 3.75 m/s at the
locked 48 px/m scale. The arena was designed at an implicit ~48 px/m scale with the player
moving at PoE-1-base feel (~3.75 m/s). New VS2a mid = 360 px/s = 7.5 m/s — near-2× feel
speed-up. Spawn separation = 1168 px = 24.3 m → closes in ~3.2 s at 7.5 m/s (was ~6.5 s
at 3.75 m/s). Arena feels perceptibly tighter at the new speed.

**Playtest calibration observations (phase 6.1/6.2 equivalent):**
1. Visual chase-feel: 84 px/s margin (player 360 − AI 276) is threatening and sustained;
   AI cannot catch a moving player in open space but can pressure effectively across distance.
   Qualitatively comparable to prior ~99 px/s margin; feels genre-honest for D3/D4 trash packs.
2. Combat-positional legibility: 360 px/s = 6 px/frame at 60fps. Combatants remain visually
   trackable without blur or positional read confusion. No frame-rate-sensitivity artifacts.
3. Encounter-spatial check: Case A friction observed. Spawn gap (~24.3 m) closes ~2× faster.
   PREFERRED_RANGE values (close=90, medium=420, long=660) and KITE_TRIGGER=300 were tuned
   for the prior speed regime; at 360/276 px/s the medium and long ranges feel slightly
   compressed. Long-range AI (prefer 660 px) oscillates against the ry=336 minor-axis
   boundary as before, but reach the oscillation point faster. No new artifacts introduced;
   the existing oscillation note in code is unchanged.
4. Overall: demo is fully functional and visually coherent at the new values. The Case A
   arena-tightness is a design-feel observation, not a defect.

**AI multiplier verification (chase-margin):**
- `AI_SPEED_MULTIPLIER = 0.767` (updated from 0.55)
- At VS2a: player 7.5 m/s = 360 px/s; AI = 360 × 0.767 = 276 px/s = 5.75 m/s (exact trash base)
- Chase margin = 360 − 276 = **84 px/s** (matches gandalf design intent verbatim)
- Math cross-check: 5.75 / 7.5 = 0.7667 ≈ 0.767 (locked value; rounding within 0.04%)

**Cross-seam flags:**
1. **CASE A — arena re-dimensioning flag for knight-rider.** Arena at 32.67 m wide with
   7.5 m/s mid-game player is perceptibly tighter than prior feel. Recommend knight-rider
   author a follow-on arena-tuning dispatch (Matt-decision gate per gandalf framing).
   Candidate: scale ELLIPSE_RX from 784 px to ~960 px (~20 m semi-axis, ~40 m full width)
   to restore the prior "spacious" encounter feel. DO NOT execute in this dispatch.
2. **PREFERRED_RANGE + KITE_TRIGGER re-tune advisory** (corollary to arena flag): medium=420
   and long=660 preferred distances, and KITE_TRIGGER=300, were calibrated for 180 px/s;
   at 276 px/s AI these distances are traversed faster. Low urgency — demo is playable —
   but worth revisiting alongside arena re-dimensioning.
3. **speedForProfile() shim retained**: call sites in main.ts (lines 533, 909) still call
   `speedForProfile(cls.range_profile)`. Shim returns uniform PLAYER_MOVE_SPEED_PX. No
   functional change; clean removal deferred to next movement-related dispatch.
4. **No rocket seam discrepancy found**: rocket schema `movement_speed` field at 62624dd
   emits `5.75` default per gandalf spec. Engine type consumer updated with optional
   `movement_speed?: number` on ClassData + MonsterData. No upstream value discrepancy.

**Notes for knight-rider:**
- Implementation complete; acceptance criteria all satisfied (see checklist below).
- **Primary flag: Case A confirmed — arena re-dimensioning is a likely follow-on.**
  Not a VS2a blocker per dispatch scope. Matt-decision required before action.
- Smoke test: `npm run build` → TypeScript clean + Vite build PASS (10.28s).
- Recommendation for arena follow-on: scale arena width from 32.67 m → ~40 m (ELLIPSE_RX
  784 → ~960 px) to restore prior spaciousness feel at the 2× speed increase. Pair with
  PREFERRED_RANGE and KITE_TRIGGER review in same dispatch.

**Acceptance criteria:**
- [x] `world/movement.ts` replaced with gandalf-locked values (PIXELS_PER_METER=48 constant explicit)
- [x] Player baselines wired (5.75 base; 6.0 early; 7.5 mid-VS2a; 8.0 late)
- [x] Monster baselines wired (5.75 trash; 6.6 fast-archetype floor; 7.5 ceiling)
- [x] Arena-scale back-derivation verified; Case A reported
- [x] AI_SPEED_MULTIPLIER updated to 0.767; chase-margin verified (84 px/s)
- [x] Playtest calibration phase 6.1/6.2 equivalent re-run; observations documented
- [x] Intermediate tag `drax/v0.10-movement-speed-locked` cut @ `151c7ec`
- [x] AGENT_STATE.md updated
- [x] Knight-rider notified at completion with arena-scale case + playtest observations
