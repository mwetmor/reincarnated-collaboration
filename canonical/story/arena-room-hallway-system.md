# Arena Room/Hallway System — Diablo/PoE Interior Model

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical — Matt-approved 2026-05-16.** Authored 2026-05-16 by gandalf on Matt's direct directive: *"I would like rooms that are more similar to Diablo/PoE and they should connect to one another without enemy combatant aggro prior to entering each room (roughly, or a general aggro range which fits the screen). So I think the genre's style prefer's square rooms and rectangular hallways (when not in open air areas."*

**Gating:** VS2a SHIP gate. Drax's demo arena work scales from "ellipse re-dimensioning" to "room/hallway geometry system" per this doc. Engine sim semantics (B10 V2) are unaffected.

**Supersedes:**
- Drax arena re-dimensioning ELLIPSE_RX 784→960 px (item #6 from 2026-05-16 status report) — the single-ellipse model itself is replaced
- The current `reincarnated-demo/src/world/arena.ts` clampToEllipse-based bounds model — needs replacement with room/hallway bounds system

**2026-05-16 Day-4 amendment:** AI_SPEED_MULTIPLIER, chase-margin, and room-cross time values updated per Matt verdict reversal (Option A mid-game framing → Option B end-game framing). See `movement-speed-baseline.md` § "Verdict Reversal 2026-05-16" for the source-of-truth derivation. Affected lines: room-aggro active-state speed values (§ "Aggro state machine"); chase-margin re-validation (§ "Re-validation needed"); default room-cross time (§ "Room geometry"). Room-sizing rationale **unchanged** — only the time-per-traversal and the AI-speed ratio recalibrate.

**Companion docs:**
- `canonical/story/movement-speed-baseline.md` § "Verdict Reversal 2026-05-16" — source-of-truth for player 8.0 m/s end-game, trash 5.75 m/s, fast-archetype 7.5 m/s, AI_SPEED_MULTIPLIER 0.719, 48 px/m, chase margin 24 px/s — all values consumed here for room sizing
- `canonical/16-project-roadmap.md` § B10 V2 — sequential-room sim semantics this doc gives visual presentation to
- `canonical/story/p6-forward-audit-2026-05-16.md` § B10 V2 row — the WATCH item this directive operationalizes
- `canonical/story/drift-audit.md` Pattern P6 — the drift framing this resolves
- `reincarnated-demo/src/world/movement.ts` — AI engagement distances + chase margin will need re-validation against new arena topology
- `reincarnated-demo/src/world/arena.ts` — current ellipse model being replaced

---

## Headline

Demo VS2a moves from single-elliptical-arena model to **room + hallway interior model.** Square (or near-square) rooms sized to fit on screen; rectangular hallways connecting rooms; aggro activates on room-entry; enemies in unentered rooms remain dormant. Open-air areas are a second register explicitly deferred to Phase 1 / VS2c+.

This is the Diablo/PoE dungeon interior convention. It gives visual presentation to B10 V2's sequential-room sim semantics.

---

## Why this exists (and why now)

B10 V2 is shipping sequential-room semantics in the simulation seam (HP carryover between encounters; class fights N mobs per room). The simulation conceptualizes "room" as an abstract sequencing construct. Until now, the demo has rendered all combat in a single ellipse — i.e., **the engine has a room concept the demo doesn't visually express.**

This is a Pattern P6 instance per the forward audit (B10 V2 row, WATCH severity): *"sequential rooms imply room-to-room transitions; current arena is single-ellipse; needs naming."* Matt's 2026-05-16 directive operationalizes the WATCH item with full design direction before it bites at VS2a integration time.

The decision lands now because (a) B10 V2's first regen will produce sequential-room telemetry that needs matching visual presentation; (b) drax's arena work is already in flight (the now-superseded ellipse re-dimensioning); (c) shipping VS2a with sequential-room sim + single-ellipse visual would undercut the engine's V2 showcase value.

---

## The design — concrete parameters

### Room geometry

- **Shape:** square or near-square (1:1 to 1.5:1 aspect ratio permitted)
- **Default size:** **30m × 30m** at 48 px/m = **1440 × 1440 px** (fits 1920×1080 viewport with margin). Player straight-line room-cross time at end-game baseline (8.0 m/s per `movement-speed-baseline.md` § "Verdict Reversal 2026-05-16"): **30m ÷ 8.0 m/s = 3.75s**. Earlier figure (4.0s at 7.5 m/s mid-game) is superseded. Room-sizing rationale **does not require adjustment** — the ~3.75s cross-time at end-game preserves the "room feels like a discrete combat space, not a hallway" reading; the player still has time to perceive the room geometry before reaching the far wall, and the encounter cadence per-room remains genre-appropriate for D2/PoE-style clear-room rhythm
- **Smaller variant:** 15m × 15m (720 × 720 px) — for tighter encounters; viewport frames player with room headroom
- **Larger variant:** up to 45m × 45m (2160 × 2160 px) — for set-piece encounters; camera follows player within room bounds; full room not visible at once
- **Variance discipline:** room sizes within a single dungeon/season should not vary wildly; per-season vocabulary may bias toward small/medium/large but should stay within the 15–45m envelope

### Hallway geometry

- **Shape:** rectangular
- **Width:** 6–10m (288–480 px) — variable; can vary within a single dungeon for visual interest
- **Length:** variable; typically 10–30m
- **No combat encounters in hallways** per Matt's "no cross-room aggro" directive — hallways are pure traversal corridors
- **Hallway count between rooms:** typically 1; some encounters may include short branching for visual variety, but core sequence is room → hallway → room

### Door / connection mechanic

- **Mode B (free traversal) — locked-in 2026-05-16 per Matt's defaults confirmation.** Doors between rooms and hallways are passable in both directions at all times. Player can retreat to hallway if positionally pressured; enables tactical positioning.
- **Visual door element:** placeholder primitive geometry (rectangular threshold marker) at room ↔ hallway boundaries until art exists. Feedback-layer art per P6.c sub-pattern; not in current sourcing scope.
- **Rejected: Mode A (gated until clear)** — locks the door until room is cleared. D2 dungeon-style. Matt did not select; defaults to Mode B. Mode A remains a per-encounter override option for set-piece designs in future seasons.

### Aggro state machine (per room)

Three states per room:

```
dormant ──(player crosses threshold)──→ active ──(all enemies killed)──→ cleared
                                          │
                                          └─── player exits room (active state persists; enemies don't reset)
```

- **dormant:** all enemies in room are positioned but inactive — no movement, no attacks, no AI tick. Visual: idle pose (or absent if positioned off-screen; drax design call).
- **active:** all enemies in room transition simultaneously when player crosses room threshold. Once active, standard AI behavior per `tickAIMove` with movement-speed values from `canonical/story/movement-speed-baseline.md` § "Verdict Reversal 2026-05-16" (player end-game **8.0 m/s**; trash **5.75 m/s**; **AI_SPEED_MULTIPLIER = 0.719** = 5.75 ÷ 8.0). The earlier 0.767 multiplier (derived from mid-game 7.5 m/s player baseline under the Option A framing) is superseded by Option B end-game anchoring per Matt Day-4 verdict reversal.
- **cleared:** non-reversible state once all enemies dead. Room remains traversable.

**"Screen-fit aggro range" = the room itself** (since rooms are sized to fit on viewport). All visible enemies activate at once when player enters. This matches genre clear-room rhythm — D1/D2 dungeon-clear feel; PoE map-cell entry.

**Enemies do not pursue into hallways** (or do so rarely; "stuck-in-room" pattern is genre-standard for dungeon AI). Implementation: enemies have an implicit room-anchor; AI pursuit caps at the room threshold. If enemy reaches room edge while chasing player into hallway, enemy halts and returns to ambient/wandering behavior within room.

### Camera/viewport behavior

- **In hallway:** tight follow camera (existing `tickPlayerMove` behavior)
- **In room (default 30m × 30m):** frame the player with room bounds visible; camera may pan if player approaches room edge
- **In room (small variant 15m × 15m):** full room visible at once; camera framing fixed at room center with player offset
- **In room (large variant up to 45m × 45m):** camera follows player within room bounds; full room not visible at once; pre-pan optional on entry
- **Room-entry transition:** brief pan to frame room (~0.5s) before AI activates — gives player visual orientation. AI_ENGAGEMENT_WINDUP (current 0.7s in `movement.ts`) covers this and provides reaction time before AI engages.

---

## Genre rationale (briefly)

This is the **Diablo dungeon interior convention** with PoE map-cell influences:

- **D1:** pure tile-based; square rooms + rectangular hallways; iconic dungeon aesthetic
- **D2:** indoor zones (Cathedral, Mausoleum, Sewers) are rooms + hallways; outdoor zones (Cold Plains, Stony Field) are open-air with paths
- **D3:** rooms + hallways dominant in dungeons; outdoor zones (Highlands, Fields of Misery) are wider open
- **D4:** open-world overworld + dungeon interiors that are room-and-hallway; mounts only on overworld
- **PoE:** mixed map content — some maps open ("Strand," "Spider Forest"), most have room-and-hallway structure

The aggro-on-room-entry mechanic is universal across these — D2 Sewers, D3 dungeons, PoE map cells all use room-entry triggers with no cross-room aggro. The player's positional agency to choose engagement timing is part of the genre's core feel.

Reincarnated VS2a/VS2b adopts **interior register only.** Open-air register is the natural second mode and is deferred per § "What's NOT in scope" below.

---

## Implementation guidance for drax

### Code locations

- **Replace `reincarnated-demo/src/world/arena.ts`:** the current `clampToEllipse` model is being retired in favor of room/hallway bounds system. Suggested new module: `reincarnated-demo/src/world/topology.ts` or expand `arena.ts` with new exports
- **Update `reincarnated-demo/src/world/movement.ts`:** `clampToEllipse` calls in `tickPlayerMove` and `tickAIMove` replace with room-or-hallway-aware bounds clamping. AI pursuit cap at room edge needs new logic
- **New module:** `reincarnated-demo/src/world/aggro.ts` (suggested) — per-room aggro state machine; activation trigger on threshold crossing; integration with combatant lifecycle
- **Camera module:** existing camera logic likely lives in `main.ts` or `rendering/`; drax discretion on where the room-aware framing lives

### Suggested data structures

```typescript
interface Room {
  id: string;
  bounds: { x: number; y: number; width: number; height: number }; // px
  variant: 'small' | 'default' | 'large'; // 15m / 30m / 45m
  aggroState: 'dormant' | 'active' | 'cleared';
  enemies: Combatant[];
  doors: Door[];
}

interface Hallway {
  id: string;
  bounds: { x: number; y: number; width: number; height: number };
  connects: [string, string]; // room IDs
}

interface Door {
  position: { x: number; y: number };
  connectsTo: string; // room or hallway ID
}

interface Dungeon {
  rooms: Room[];
  hallways: Hallway[];
  startingRoom: string;
}
```

This is suggested only — drax discretion on actual data model. The constraints from this doc are the semantics, not the types.

### Integration with B10 V2 sequential rooms

Engine sim's "room" concept (HP carryover; N mobs per room) maps 1:1 to demo's visual Room. B10 V2's sequential ordering becomes hallway connectivity in the visual topology. Drax consumes engine's per-room composition data to populate the visual rooms.

For VS2a's single-season regen: a linear dungeon (room1 → hallway → room2 → hallway → room3 → ...) is sufficient. Branching/non-linear dungeons can be Phase 1+ design.

### Re-validation needed

After implementation, re-validate:

- AI engagement distances (`PREFERRED_RANGE` in `movement.ts`) — values were tuned for ellipse model; may need adjustment for room model
- Chase margin in active-room state — should be **24 px/s** (fast-archetype 7.5 m/s vs player end-game 8.0 m/s; differential 0.5 m/s × 48 px/m = 24 px/s) per `movement-speed-baseline.md` § "Verdict Reversal 2026-05-16." Superseded the prior 84 px/s figure (which was trash:player under Option A mid-game framing). At Option B end-game anchoring, the relevant chase-margin signal is fast-archetype:player, not trash:player — trash now lag end-game player by 2.25 m/s = 108 px/s, which is the "outrunnable trash" feel; the 24 px/s fast-archetype margin is the "positionally threatening fast monster" feel preserved as design intent
- Pack movement patterns — `tickAIMove` kiting logic needs to respect room bounds
- Player traversal feel — hallway widths should not feel constraining; rooms should not feel arbitrary

This re-validation is a playtest cycle equivalent to phase 6.1/6.2 movement calibration, but for arena topology.

---

## What's NOT in scope

- **Open-air areas (second register).** Wider freeform paths; proximity-based aggro (~10–15m radius); mount-style traversal possibly. Explicitly deferred to **Phase 1 / VS2c+.** Not in VS2a/VS2b. When open-air enters scope, second design call needed for: aggro mechanic (proximity vs trigger); path widths; visibility / fog-of-war if applicable; encounter density.
- **Branching / non-linear dungeons.** VS2a/VS2b ship linear dungeons (room → hallway → room → ...). Branching topology, multi-path encounters, optional rooms — Phase 1+ design.
- **Door art.** Visible door element is placeholder primitive geometry per P6.c sub-pattern; production-quality door art is part of the feedback-layer art-sourcing track that has no current commission.
- **Room theming / environmental variety.** Walls, floors, decorations, ambient props — Phase 1+. VS2a/VS2b can ship with minimal-style rectangular room presentation.
- **Mode A (gated doors).** Locked-until-clear door mode; explicitly rejected as default by Matt 2026-05-16. Remains available as per-encounter override for set-piece designs in future seasons.
- **Patrolling enemies in hallways.** Genre supports this (D2 wanderers; PoE corridor enemies); Reincarnated VS2a/VS2b ships with empty hallways per "no cross-room aggro" directive. Phase 1+ design call.
- **Camera transitions on room entry beyond a brief pan.** No cinematic camera moves; no entry cutscenes; no boss-room dramatic framing. Simple pan-and-frame.

---

## Cross-references

- **Required reading consumed:**
  - Matt's 2026-05-16 directive (gandalf conversation; this doc's source)
  - `canonical/story/movement-speed-baseline.md` — m/s + 48 px/m + AI_SPEED_MULTIPLIER values for room sizing
  - `canonical/16-project-roadmap.md` § B10 V2 + § VS2a — engine sim semantics; demo gating
  - `canonical/story/p6-forward-audit-2026-05-16.md` § B10 V2 row — the WATCH item this resolves

- **Engine + demo references:**
  - `reincarnated-demo/src/world/arena.ts` — current ellipse model being replaced
  - `reincarnated-demo/src/world/movement.ts` — `clampToEllipse` calls being replaced; AI engagement re-tuning needed
  - `reincarnated-demo/src/main.ts` — camera logic to update

- **Drift-audit instances:**
  - Pattern P6 (load-bearing dimension deferred) — this doc resolves an instance flagged in the forward audit
  - Sub-pattern P6.c (telegraph / feedback / indicator art has no source plan) — door art falls in this gap; named but not resolved

- **Supersedes:**
  - Drax arena re-dimensioning ELLIPSE_RX 784→960 px (item #6 from 2026-05-16 status report) — single-ellipse model replaced
  - Single-arena model in `arena.ts` (`clampToEllipse` paradigm) — replaced by room/hallway topology system

---

## Maintenance protocol

When playtests on VS2a/VS2b return feedback:

1. **"Rooms feel cramped / spacious"** — first check room size variant against intended encounter scale; small variant (15m) is intentional for tight encounters; large variant (45m) for set-pieces. Default 30m should fit most. If feedback recurs across encounter types, consider adjusting movement-speed-baseline or room default size.
2. **"Hallway traversal feels slow / boring"** — hallway widths may need adjustment within 6–10m band; if hallways feel too long, content variation (branching; visual interest) becomes Phase 1+ design.
3. **"Aggro feels surprising / unfair"** — verify room-entry threshold detection; consider if room-entry pan duration needs adjustment; AI_ENGAGEMENT_WINDUP at 0.7s may need tuning if aggro feels too immediate.
4. **"Enemies pursuing into hallways feels wrong / right"** — current design caps pursuit at room edge; if playtest signal flips this, room-anchor cap can be relaxed for specific enemy types. Genre allows either; default is cap-at-edge.

When B10 V2 engine sim returns telemetry:

1. Per-room metrics from sim should map to per-Room visual presentation in demo; verify 1:1 correspondence
2. HP carryover semantics from sim consumed by visual room transitions; verify state persists correctly

When open-air register enters scope (Phase 1 / VS2c+):

1. Author second canonical doc (`arena-open-air-system.md` or similar)
2. Design call needed for: aggro mechanic (proximity vs trigger); path geometry; visibility model; encounter density
3. Cross-reference this doc; preserve interior register as orthogonal first register

When future P6 forward audit re-runs:

1. Verify this doc still names arena topology correctly
2. If new arena sub-dimensions surface (e.g., destructible environment; environmental hazards; dynamic room layouts), surface as new audit finding

— gandalf, 2026-05-16 (Day 4)
