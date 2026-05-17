# 2026-05-17 — gandalf + drax-demo (joint) — ARPG map overlay research commission

**Authority:** Matt L3 commissioned 2026-05-17 (~17:00 EDT).
**Type:** Pattern B — joint research commission (two parallel streams, one shared output).
**Estimated effort:** ~1-2 days each stream (gandalf canon ~6-10h; drax engineering plan ~6-10h).
**Sibling commissions in flight:**
- Gandalf mobile-vs-PC pixel sizing & ratios (`2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md`)
- Drax mobile UX research + execution plan (`2026-05-17-drax-demo-mobile-ux-research-and-plan-commission.md`)
**Scope window:** Forward-looking; output feeds future implementation in **VS2b territory or later** — not VS2a-gating. Research now; execute when scheduled.

---

## Why this matters

Matt's frame, verbatim: *"UX/UI on this is paramount to the ARPG genre. In fact, MANY players will only focus their eyes on the mini-map overlay due to the pace of the game. And this has the added benefit of allowing for some of the roughness that we will have from using varied pixel art packs to be brushed under the rug in terms of overall player experience impact if we REALLY nail down the map overlay."*

Two strategic reasons:
1. **Genre primacy** — in fast-paced ARPG combat, the minimap is where the player's eye actually lives. Get it wrong and the game feels chaotic; get it right and the game feels coherent.
2. **Pixel-art-pack heterogeneity mask** — our visual assets come from multiple vendors (CraftPix + Pimen + Frostwindz + CreativeKind + Fellor); a strong minimap reduces the perceptual cost of mixed art registers because the player's primary spatial-awareness organ is the map, not the floor art.

**Matt-named player-preference hypothesis (validate with gandalf):**
- **Group 1** — prefers small minimap in the top-right corner (D2 / D4 / PoE canon)
- **Group 2** — prefers larger, centered, semi-transparent full-screen overlay (Matt's preference; D2 ALT-toggle map; D-Immortal big-map mode)

Gandalf validates whether this two-group split is real and what the dominant variant is per platform (PC vs mobile may differ).

---

## Required reading

### For gandalf (genre canon)

1. Sibling commission outputs (consume when available; placeholder if not):
   - `agentic_orchestration/dispatches/2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md` — your mobile sizing canon
   - `agentic_orchestration/dispatches/2026-05-17-drax-demo-mobile-ux-research-and-plan-commission.md` — drax mobile layout zones
2. ARPG canon: D2, D3, D4, PoE 1/2, Last Epoch, Grim Dawn, Lost Ark, Diablo Immortal, Torchlight Infinite, Eternium, Dungeon of Exile, Path of Exile Mobile (if shipped), Anima ARPG, Oniro ARPG
3. Any prior matt-gandalf canon on map design (search `minimap`, `map overlay`, `mini-map` in canonical/ + decisions-log)

### For drax (engineering reality)

1. `reincarnated-demo/src/` — survey for existing map / minimap rendering (search `minimap`, `map`, `worldMap`, `roomLayout`). Likely nothing exists yet — that itself is the starting fact.
2. `reincarnated-demo/src/world/` — room / floor data structures (whatever drives `clampToZone`, room transitions, monster spawns) — these are the data source the minimap reads
3. `reincarnated-demo/src/main.ts` — render layers; where the minimap RenderTexture or Container would live
4. Pixi.js render-texture patterns + viewport-relative positioning (you've handled this pattern for HUD already; same toolkit)
5. The two sibling commissions (same as gandalf's list)

---

## Scope — two parallel streams, one shared output

### Stream A — Gandalf (genre canon + design principles)

#### A1. Two-group hypothesis validation

Matt asserts two player groups. Validate:
- Is it real? Cite genre evidence (e.g., D2 had ALT-overlay because Blizzard saw both; D4 has minimap+expanded-map toggle; PoE has both; Torchlight Infinite has both)
- What's the dominant default per platform? (PC = corner-mini default with full-overlay-on-key? Mobile = compressed-corner-mini? Tablet = hybrid?)
- Any THIRD group? (e.g., players who use full-screen tactical maps in MMOs; players who turn map off entirely in hardcore mode)
- Recommended Reincarnated default per platform

#### A2. Map content + render decisions

For each platform (PC desktop, mobile portrait, mobile landscape, tablet), specify:

- **What's rendered:** room outlines, doors, monsters (color-coded), player position, NPCs, gear drops, treasure chests, environmental waypoints (altar, vendor, exit), objectives
- **Fog of war vs full reveal:** D-canonical fog (explore-to-reveal) vs PoE-canonical full-reveal at room-enter — recommend
- **Color palette:** background tint, room-outline color, monster dot colors (per-tier? per-substrate?), player dot, important-target dot
- **Opacity:**
  - Corner minimap: opaque background but transparent edges? full opacity?
  - Full-screen overlay: 50-70% transparent over gameplay? darken-the-game-underneath approach?
- **Sizing per platform:** consume sibling pixel-sizing commission; document specific px values
- **Zoom controls:** does the player adjust zoom? auto-zoom on big rooms? Recommend

#### A3. Iconography & symbol vocabulary

What symbols appear on the map? Standard ARPG vocabulary:
- Player dot (color/shape/pulse)
- Monster dots (per-tier: trash, elite, rare, champion, boss)
- NPC indicators (vendor, quest-giver)
- Gear drops (per-rarity: white, magic, rare, unique)
- Chests (small/medium/large)
- Exits / waypoints / altars
- Objectives (active quest goal marker)

For each: shape, color, animation (static / pulse / rotate), legibility rules.

#### A4. Interaction model

- **Open/close gesture:** key (M? Tab?), button click, mobile swipe-down, mobile two-finger?
- **While-open behavior:** does gameplay pause? continue? (recommend per platform)
- **Player-position click:** click-to-move? center-on-player? (PoE-canon)
- **Annotation:** can player mark points? (Last Epoch supports this; D-Immortal does not)
- **Transparency tuning:** does player adjust opacity in settings? (PoE allows; D4 does not)

#### A5. Mobile-specific design

- Mobile minimap typically lives top-right (D-Immortal, Torchlight Infinite); thumb-reach analysis
- Mobile full-overlay: usually full-screen modal; closed on tap-outside (or center-tap-to-dismiss)
- Mobile gestures: pinch-zoom on map; two-finger pan; long-press for annotation if scoped
- Avoid notch / status-bar; safe-area inset; landscape vs portrait variants

#### A6. Aesthetic guidance

Per Matt's "brush roughness under the rug" frame — what design choices specifically improve perceived art quality?
- **Stylized symbols** instead of literal sprite renders (lower bar; recognizable; consistent across substrates)
- **Strong contrast** at small sizes (legibility over realism)
- **Consistent palette** (player+monster colors stable across all maps; substrate-coupling on environment tints only)
- **Smooth fog/reveal animation** sells "polish"
- Document the perception-engineering principles

### Stream B — Drax (engineering plan)

#### B1. Engineering reality audit

- What exists today? (likely no minimap at all; full-greenfield)
- What data is available? Room structure exists (per `clampToZone` work); monster positions exist; player position exists. Catalogue the data sources.
- What rendering pipeline fits? Pixi.js RenderTexture vs DOM/Canvas hybrid vs SVG. Recommend.
- Performance budget: minimap is rendered every frame; what's the ms budget per render? Estimate per-platform.

#### B2. Two-mode rendering plan

For each of the two Matt-flagged modes:

**Mode 1 — Corner minimap (top-right by default; configurable)**
- Pixi Container pinned to viewport corner (same pattern as HUD)
- Render at scale ~5-10% of viewport (per gandalf sizing)
- Updates per frame; cheap render
- File list: new `src/ui/minimap.ts`; integration site in `main.ts`; data feed from world/room structure

**Mode 2 — Full-screen centered overlay (M key / button toggle)**
- Pixi Container pinned to screen center
- Render at ~70-85% of viewport with semi-transparent background
- Updates per frame OR static snapshot at open + delta updates (perf decision)
- File list: same `src/ui/minimap.ts` (toggleable mode) or sibling `src/ui/mapOverlay.ts`
- Pause-gameplay-on-open is a design decision (gandalf A4)

#### B3. Mobile constraints

- Corner minimap on mobile: smaller (per gandalf mobile sizing); thumb-reach avoidance (don't block joystick zone)
- Full-overlay on mobile: full-screen modal; close gesture (tap outside? swipe? center button?)
- Render performance on mobile GPU: budget tighter; benchmark hypothesis

#### B4. Data flow architecture

- Map data source: room-graph from gameplay loop; monster positions per frame; player position per frame; drop positions per frame
- Update frequency: per-frame on visible portions; cached on hidden portions
- Memory: how many rooms cached? Whole-floor cache vs current-room-only?
- Integration with eventual mobile execution dispatch from sibling commission

#### B5. Phasing

Decompose into drax dispatches (~0.5-2 days each):

- **Phase MM1 — Data layer**: room-graph extraction; per-frame position feed; testable in isolation
- **Phase MM2 — Corner minimap MVP**: top-right corner render; player+monster dots; static room outline
- **Phase MM3 — Full-overlay MVP**: M-key toggle; centered render; semi-transparent
- **Phase MM4 — Iconography pass**: gear drops, chests, NPCs, waypoints; per gandalf A3 spec
- **Phase MM5 — Mobile adaptation**: per gandalf A5 + drax mobile UX execution plan
- **Phase MM6 — Polish**: fog reveal animation; zoom controls; opacity settings; annotation if scoped

For each phase: file list, line-count estimate, dependencies, smoke test.

#### B6. Out-of-scope deferrals

- Multi-floor map (D2 act-overview style) — Phase-3 if ever
- Map sharing / streaming — out of scope
- Procedural-room reveal animations beyond simple fog-clear — Phase-3 polish

### Shared output

ONE canonical doc at `canonical/story/arpg-map-overlay-research-2026-05-17.md` (or your chosen path) with both streams' content:

1. Executive summary (gandalf authors; drax reviews)
2. Two-group validation result (gandalf A1)
3. Map content + render decisions (gandalf A2)
4. Iconography & symbol vocabulary (gandalf A3)
5. Interaction model (gandalf A4)
6. Mobile-specific design (gandalf A5)
7. Aesthetic guidance (gandalf A6)
8. Engineering reality audit (drax B1)
9. Two-mode rendering plan (drax B2)
10. Mobile constraints (drax B3)
11. Data flow architecture (drax B4)
12. Phasing — drax dispatches (drax B5)
13. Out-of-scope deferrals (drax B6)
14. Open questions for Matt

### Tags + hive log

- **Gandalf:** STATE entry; tag `gandalf/v1.8-arpg-map-overlay-research-1`
- **Drax:** STATE entry; tag `drax/v1.7-arpg-map-overlay-engineering-plan-1`
- Both append completion records to this dispatch.

---

## Coordination protocol

- **Race condition discipline (§ 14.1.1):** PRE-SIGNAL before any hive-log append; pull-rebase before commits to collab repo. Two parallel agents writing the same hive log is a high-risk pattern — apply discipline rigorously.
- **Shared doc authorship:** gandalf authors sections 1-7; drax authors sections 8-14; section 1 (exec summary) gandalf authors after drax sections land; section 14 (open questions) compiled by whichever ships last
- **Cross-stream dependencies:** none blocking (gandalf can author without drax engineering; drax can plan without gandalf canon, using placeholders). Final shared doc requires both.
- **Sibling commission coordination:** consume their outputs if available; cite placeholders if still in flight. The map overlay commission's "what size is the mobile corner minimap?" answer depends on gandalf's pixel sizing commission landing first — note explicitly.

---

## Out of scope (DO NOT)

- ❌ DO NOT implement any minimap code (research + plan only)
- ❌ DO NOT change desktop UX beyond what the plan documents
- ❌ DO NOT lock specific implementation timing (post-VS2a target)
- ❌ DO NOT change gandalf's pixel sizing commission scope or drax's mobile UX plan scope
- ❌ DO NOT extend scope to map sharing / multi-floor maps / streaming
- ❌ DO NOT recommend art-pack acquisitions; if map iconography needs new assets, surface as OBSERVATION for Phase-2 acquisitions queue

---

## Acceptance criteria

- [ ] Two-group hypothesis validated with genre evidence (gandalf A1)
- [ ] Map content + render decisions per platform (gandalf A2)
- [ ] Iconography & symbol vocabulary table (gandalf A3)
- [ ] Interaction model decisions (gandalf A4)
- [ ] Mobile-specific design (gandalf A5)
- [ ] Aesthetic guidance / perception-engineering principles (gandalf A6)
- [ ] Engineering reality audit (drax B1)
- [ ] Two-mode rendering plan (drax B2)
- [ ] Mobile constraints addressed (drax B3)
- [ ] Data flow architecture (drax B4)
- [ ] Phased drax-dispatch plan (drax B5)
- [ ] Out-of-scope deferrals listed (drax B6)
- [ ] Shared canonical doc filed
- [ ] Gandalf tag `gandalf/v1.8-arpg-map-overlay-research-1`
- [ ] Drax tag `drax/v1.7-arpg-map-overlay-engineering-plan-1`
- [ ] Both completion records appended

---

## Smoke expectation

Matt reads the canonical doc and can decide:
- Which default mode per platform (corner vs overlay)
- What iconography palette to lock
- Approval to proceed with drax phase MM1 when scheduled
- Open-question answers (if any)

---

## Coordination notes

- **No legolas sub-commission anticipated** — gandalf's offline canon should cover; if a niche title needs verification, gandalf may invoke legolas Mode B (pre-authorized).
- **No production code** — research + plan only.
- **Hive log discipline:** PRE-SIGNAL per § 14.1.1 before hive-log appends. CRITICAL with two parallel agents.
- **If sibling commissions still in flight when you finish your stream:** ship your stream's section; cite `<sibling-pending>` for cross-references; the other stream's agent fills in when its sibling lands.

---

*Commissioned 2026-05-17 by knight-rider per Matt L3. Two parallel streams, ~1-2 days each. Append completion records when done.*

---

## Completion record — Stream B (drax)

**Completed:** 2026-05-17
**Tag:** `drax/v1.7-arpg-map-overlay-engineering-plan-1`
**Agent:** drax

### Deliverables

**Canonical doc:** `canonical/story/arpg-map-overlay-research-2026-05-17.md` — sections 8-14 authored. Sections 1-7 left as pending placeholders for gandalf stream.

**Acceptance criteria (Stream B):**
- [x] Engineering reality audit (§ 8): full greenfield confirmed; all data sources catalogued
- [x] Two-mode rendering plan (§ 9): corner minimap + full-overlay; single `src/ui/minimap.ts`; `main.ts` integration map
- [x] Mobile constraints addressed (§ 10): sizing, position, gesture, overlay model, performance budget
- [x] Data flow architecture (§ 11): static/dynamic layer model; update frequency; memory model; NPC/chest/waypoint extension path
- [x] Phased drax-dispatch plan (§ 12): 6 phases (MM1-MM6) with file lists, line-count estimates, smoke tests, dependencies
- [x] Out-of-scope deferrals listed (§ 13): multi-floor, map sharing, procedural reveal, click-to-move, annotations, radar-ping
- [x] Shared canonical doc filed
- [x] Tag `drax/v1.7-arpg-map-overlay-engineering-plan-1`
- [x] Hive-log STATE entry appended (§ 14.1.1 discipline observed)
- [x] AGENT_STATE.md updated

### Key findings

- No minimap exists anywhere. Greenfield.
- `topology.ts` `Dungeon` interface already carries everything needed: room/hallway bounds, doors, aggro states.
- `playerPos`, `pack[].pos`, `gearDropSprites[]` are the three per-frame data feeds.
- Recommended pipeline: Pixi `Graphics` two-layer split (static cached, dynamic per-frame). ~0.1-0.8 ms/frame budget — negligible.
- One new file: `src/ui/minimap.ts`. Six phased dispatches to full polish.

### Cross-stream status

Gandalf sections 1-7 pending. Placeholders in doc at §§ 1-7. Sibling commissions consumed: gandalf v1.7 pixel sizing (shipped), drax v1.6 mobile UX plan (shipped).
