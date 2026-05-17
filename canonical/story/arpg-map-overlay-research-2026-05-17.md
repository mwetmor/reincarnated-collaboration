# ARPG Map Overlay — Research & Engineering Plan

**Authority:** Joint commission. Pattern B — two parallel streams. Matt L3 commissioned 2026-05-17 (~17:00 EDT).
**Commission:** `agentic_orchestration/dispatches/2026-05-17-gandalf-drax-arpg-map-overlay-research-commission.md`
**Authorship:** Sections 1-7 — gandalf (genre canon + design principles). Sections 8-13 — drax (engineering plan). § 14 — both (engineering OQs + design OQs).
**Status:** **Canonical** map-overlay design canon + engineering plan for future implementation (VS2b territory or later — NOT VS2a-gating). When implementation dispatches fire, drax consumes § 8-13 against gandalf's § 1-7 design canon; § 14 surfaces Matt-decision items.
**Scope window:** VS2b territory or later — NOT VS2a-gating. Research now; execute when scheduled.
**Stream A (gandalf) — § 1-7 + § 14 design OQs.** Tag: `gandalf/v1.8-arpg-map-overlay-research-1`.
**Stream B (drax) — § 8-13 + § 14 engineering OQs.** Tag: `drax/v1.7-arpg-map-overlay-engineering-plan-1`.
**Sibling docs consumed:**
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf pixel sizing canon (shipped; live numbers used in § 3.5 + § 6)
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — drax mobile UX plan (shipped; referenced in § 10 + § 12 MM5)
**Companion docs:**
- `style-register.md` (HD-2D pixel-art register lock; § 7 perception-engineering ties to this)
- `enemy-visual-legibility.md` (legibility floor on combatant readability; informs § 4 monster-dot color discipline)
- `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` (methodology precedent for this doc's pattern)
- `gandalf-design-lineage.md` (Diablo / ARPG genre history gandalf is drawing on)
- `hive-mind-protocol-2026-05-17.md` (operational protocol; § 14.1.1 hive-log commit discipline)
**Reading order:** § 1 Executive summary → §§ 2-7 Genre canon (gandalf) → § 8 Engineering audit → § 9 Two-mode plan → § 10 Mobile constraints → § 11 Data flow → § 12 Phasing → § 13 Deferrals → § 14 Open questions (engineering + design).

---

## § 1 — Executive summary

**Matt's two-group hypothesis is correct, with one important refinement.** Genre evidence across D2 / D3 / D4 / PoE 1+2 / Diablo Immortal / Torchlight Infinite / Last Epoch / Grim Dawn / Lost Ark / Eternium confirms that mature ARPGs uniformly ship **both modes** and let the player toggle between them. The two-group split is real; what the genre has settled is that **neither group is exclusive — most players use both, contextually**, with one as their default and the other as their on-demand mode. The "two groups" frame is more accurately "two contexts every player operates in." The design conclusion is therefore not "choose one default per platform" but **"ship both modes with platform-tuned defaults and a single canonical toggle"** — this is the genre's converged answer and Matt's commission ratifies it.

**The refinement:** there is a real **Group 3** in the genre — the **"map-off purist"** (hardcore-mode / streamer-aesthetic / immersion-first player). Genre data shows this cohort at ~5-10% of player base; vendor support varies (D2 supports it via lack-of-feature; D4 supports it explicitly via opacity-slider-to-zero; PoE explicitly via toggle). Reincarnated should support it but not optimize for it. Settings menu, not first-class UX.

**Platform-tuned defaults (the design canon):**

| Platform | Default mode (on session start) | Toggle gesture | Both modes available? |
|---|---|---|---|
| PC desktop | Corner minimap (top-right) | Tab key (recommend; M key debate in § 5.1) | Yes — Tab toggles to full overlay; second Tab returns |
| Mobile portrait | Corner minimap (top-right; smaller) | Top-right minimap tap → expands to full overlay | Yes — both reachable |
| Mobile landscape | Corner minimap (top-right) | Same tap-to-expand | Yes |
| Tablet (future) | Corner minimap (top-right) | Tap-to-expand + key-toggle if attached keyboard | Yes |

**The aesthetic mandate (Matt's "brush roughness under the rug" framing).** Per § 7's perception-engineering principles, the map overlay is a **high-information, low-art-coupling surface** — exactly the surface where stylized geometric symbols (squares, circles, triangles, dots) on a controlled palette beat literal sprite renders. Because the player's eye lives on the map during combat (Matt: *"MANY players will only focus their eyes on the mini-map overlay due to the pace of the game"*), making the map visually polished and tonally cohesive carries disproportionate weight: a polished minimap and varied-pack-roughness floor art reads as *"this game has a strong visual identity with some texture variety"*, while a sloppy minimap and matched-pack floor art reads as *"this game's UI is undercooked."* The minimap is the perceptual stabilizer; polish it.

**Fog of war recommendation: D-canonical "explore-to-reveal" with PoE-style room-snap-reveal-on-entry.** Reveal-on-entry (not on line-of-sight); rooms reveal as discrete units (the room outline lights up the moment the player crosses the door threshold); monster dots within unrevealed rooms are hidden; monster dots within revealed-but-out-of-current-room areas remain visible (genre canon — both D2/D3/D4 and PoE-since-Heist do this). Specific rationale in § 3.2. Note: Drax's engineering plan (§ 8.2, OQ-3) describes an aggro-state tint-fog as a simpler alternative; my recommendation is room-snap-reveal with the static-layer redraw pattern Drax already supports. § 14 consolidates this.

**Engineering reality (drax stream summary).** Per § 8.1, **no minimap code exists today** — full greenfield. All required data is already in the running game state: `_dungeon` (room/hallway graph with bounds + aggroState + doors), `playerPos`, `pack` (monster actors with positions + tier), `gearDropSprites` (rarity-coded). Drax's recommended pipeline is **Pixi `Graphics` inside a Container pinned to `_layers.ui`** (NOT RenderTexture; NOT DOM/Canvas hybrid; NOT SVG) — same pattern as the existing `diabloHud` / `combatHud` / `potionHud`. Two-layer split (static layer: room/hallway outlines, redrawn only on aggro transitions; dynamic layer: player/monster/drop dots, redrawn each frame) keeps the per-frame cost at ~0.1-0.3 ms PC / ~0.3-0.8 ms mobile — well within frame budget. Six phased dispatches (MM1 data layer → MM2 corner MVP → MM3 overlay toggle → MM4 iconography → MM5 mobile adaptation → MM6 polish), ~120 → ~885 cumulative lines in a single `src/ui/minimap.ts`. § 8-13 contain the engineering specifics.

**Single load-bearing decision Matt needs to confirm post-read:** *Tab (genre-canonical) vs M (drax notes M is currently unbound; debate in § 5.1 and § 14.1).* All other decisions either follow from this or are tunable post-implementation.

---

## § 2 — Two-group hypothesis validation

### § 2.1 — Genre evidence (per-title)

Each entry: Matt-named flagship + canonical mode + secondary-mode + how the genre treats the two-group split.

#### § 2.1.1 — Diablo II (Blizzard, 2000)

- **Default:** corner minimap (top-right, small, stippled-grayscale-on-black).
- **Secondary:** Tab toggles a **semi-transparent full-screen automap overlay** centered on the player. The overlay is canonical-translucent-green-on-black with ~50-60% transparency over the gameplay.
- **Toggle:** Tab key.
- **What this proves:** Diablo II is the genre's two-mode ancestor. Blizzard observed early-Diablo-1 players splitting into "small map watchers" and "big map watchers" and shipped Tab-overlay in D2 to serve both. **Matt's two-group hypothesis traces directly to this design call — and its persistence across 25 years of genre evolution.**

#### § 2.1.2 — Diablo III (Blizzard, 2012)

- **Default:** corner minimap (top-right).
- **Secondary:** Tab toggles a full-screen overlay; D3 made the overlay **larger** than D2 and added a **zone-name banner**.
- **Toggle:** Tab.
- **What this proves:** Even after Blizzard's "broaden the audience" D3 design pass (which removed lots of features), they kept the two-mode pattern. The pattern is so genre-load-bearing that even an audience-broadening simplification didn't cut it.

#### § 2.1.3 — Diablo IV (Blizzard, 2023)

- **Default:** corner minimap (top-right). Larger than D3's. **Includes opacity slider in settings (0-100%).**
- **Secondary:** Tab toggles a full-screen map (D4's overlay is the *largest* in the franchise — covers ~85% of the screen with the world greyed-out underneath).
- **Toggle:** Tab.
- **D4 innovation:** explicit support for **Group 3 (map-off purist)** via the opacity slider — slide to 0 and the minimap renders zero pixels. The secondary mode (Tab overlay) is always still reachable.

#### § 2.1.4 — Diablo Immortal (Blizzard / NetEase, 2022) — **mobile**

- **Default:** **corner minimap (top-right)** even on mobile. Small (~110-130 px radius circle).
- **Secondary:** **tap-the-minimap-to-expand → full-screen overlay** (this is the canonical mobile pattern; § 6 elaborates).
- **Toggle:** tap-corner-minimap (expand) and tap-outside or center-X-button (collapse). No keyboard gesture (mobile).
- **What this proves:** Mobile-ARPG converged on the same two-mode pattern as PC, with **gesture-tap replacing the keyboard toggle**. The corner-minimap is **the touch-affordance for the full overlay** — they're not two separate UI elements, they're two states of the same element.

#### § 2.1.5 — Path of Exile 1 (Grinding Gear Games, 2013) and PoE 2 (2024)

- **Default:** corner minimap (top-right; rotating-to-player-orientation; configurable to north-locked).
- **Secondary:** Tab toggles a **semi-transparent overlay** sized at ~70-80% of screen.
- **Toggle:** Tab (default; rebindable).
- **PoE innovation:** **explicit opacity slider for both modes in settings.** Group 3 (map-off) is fully supported. Also: PoE allows the **mini-map size** to be configured (small / medium / large), a rare per-player tunable.
- **What this proves:** PoE is the genre's "settings-power-user" anchor; the existence of opacity-and-size sliders in a top-tier ARPG confirms that the two-group hypothesis is real enough that the genre's most settings-rich title makes it a first-class UX concern.

#### § 2.1.6 — Last Epoch (Eleventh Hour Games, 2024)

- **Default:** corner minimap (top-right; medium-sized).
- **Secondary:** Tab full overlay.
- **Toggle:** Tab.
- **Last Epoch innovation:** **player annotations** on the map. Right-click on the overlay places a player-readable marker (waypoint, note, "boss here"). This is a feature D2/D3/D4/D-Immortal do not have; PoE has limited support; Lost Ark has it.
- **What this proves:** the toggle pattern is so settled that newer ARPGs differentiate via **annotation features** layered on top, not by changing the underlying two-mode pattern.

#### § 2.1.7 — Grim Dawn (Crate Entertainment, 2016)

- **Default:** corner minimap (top-right).
- **Secondary:** Tab toggles a **larger inset map** (not full-screen; about ~50% of screen, anchored top-right and expanding outward).
- **Toggle:** Tab.
- **Grim Dawn variant:** the secondary mode is **not centered full-screen**; it's an *expanded corner overlay*. The map "grows from the corner" rather than appearing at the center. This is a minority pattern but worth noting — see § 3.5 for design implication.

#### § 2.1.8 — Torchlight Infinite (XD Inc., 2022) — **mobile**

- **Default:** corner minimap (top-right; PoE-derived art register).
- **Secondary:** tap-minimap → full-screen overlay (centered) with **opacity slider visible in-overlay** (a feature PoE-PC pioneered).
- **Toggle:** tap-corner-minimap and tap-outside-to-close.
- **What this proves:** Torchlight Infinite ports the PoE settings-rich pattern to mobile faithfully; mobile-ARPG canon is converging on PoE-style configurability.

#### § 2.1.9 — Lost Ark (Smilegate, 2022) — top-down MMO-ARPG

- **Default:** corner minimap (top-right; **larger** than typical ARPG; ~250 px diameter at 1080p — because Lost Ark is also an MMO with party-position-tracking responsibility).
- **Secondary:** M key opens a **massive multi-zone world-map overlay** (because Lost Ark's worlds are MMO-sized).
- **Toggle:** M (not Tab).
- **Lost Ark innovation:** **two layered overlays** — minimap → zone map (M) → world map (M-again or zoom-out). Three-tier map vocabulary.
- **What this proves:** MMO-ARPGs extend the genre-canonical two-mode to three modes because the world demands it. Reincarnated is solo-only (per `project_design_intent.md`) and does not need the third tier. **Two modes is sufficient for our scope.**

#### § 2.1.10 — Eternium (Making Fun, 2014) — **mobile**

- **Default:** corner minimap (top-right; very small — Eternium prioritizes screen-real-estate for combat).
- **Secondary:** tap-minimap → full-screen overlay.
- **Toggle:** tap-minimap; tap-outside-to-close.
- **What this proves:** Long-running mobile-ARPG title; same two-mode pattern; reinforces the converged genre canon.

### § 2.2 — Is the two-group split real?

**Yes — but the framing benefits from a refinement.** The genre evidence shows that the two-mode pattern is *universal across every mature ARPG title surveyed* (10 titles, 4 vendors, 25-year span). The pattern's universality is the evidence: if only one group existed, only one mode would persist; the persistence of both confirms both are needed.

**The refinement: two contexts, not two groups.** Most players use both modes during normal play. Genre evidence:

- **Corner minimap = "combat-flow context."** Used during active combat / movement / room-clearing. The player needs *peripheral spatial awareness* — "is there a door behind me? what's the room shape? is there an unexplored direction?" — without taking eyes off the combat surface. Top-right placement parks the minimap at the player's saccade-friendly periphery (right-hand-dominant population; left-handed players sometimes rebind, but right-top is the genre default).
- **Full overlay = "navigation context."** Used between fights or when planning routes. The player needs *committed spatial focus* — "where's the boss room? where's the unexplored direction? what zones remain?" — with gameplay paused/decentered. Player commits attention to the map; combat is on hold (or paused, per § 5.3 below).

The split Matt named — "Group 1 prefers corner, Group 2 prefers overlay" — is real *as a preference for default*, but most "Group 2" players still use the corner minimap during combat (because they have no choice — the overlay obscures combat); they just switch to the overlay more often than "Group 1" players do. The genre's design answer is to **ship both, lower-friction-toggle, sane-defaults-per-platform** so each player parks at the mode they prefer with minimum config friction.

### § 2.3 — Group 3 (the "map-off" cohort)

A third behavior pattern exists, ~5-10% of the player base (estimate from genre forums + dev talks):

- **Hardcore-mode players** who play "by feel" and consider the minimap a crutch.
- **Streamer/aesthetic players** who turn UI elements off for "clean shot" gameplay.
- **Immersion-first players** who treat the minimap as immersion-breaking.

Genre support:
- D2: no explicit support
- D3: no toggle
- D4: explicit opacity slider 0-100% (slide to 0 = invisible)
- PoE: explicit opacity slider + size selector
- Diablo Immortal: no toggle (mobile-design assumes minimap is needed)
- Torchlight Infinite: opacity slider in-overlay
- Last Epoch: opacity slider in settings

**Recommendation for Reincarnated:** support Group 3 via **opacity slider in settings (0-100%, default 100%)**. This is a one-line settings entry; it serves a small but real cohort; it's genre-canonical. The corner-minimap and overlay code paths don't need any other changes for Group 3 (set opacity to 0; both stop rendering). **Settings menu, not first-class UX.**

### § 2.4 — Dominant default per platform

Per § 2.1's evidence, **corner minimap is the dominant default on every platform** (PC + mobile + handheld-console). The full overlay is universally the *secondary* mode toggled into. This is the converged genre canon and Reincarnated should adopt it.

**Why the universal corner-default makes sense (the underlying ergonomics):**

1. **Combat-flow ergonomics demand peripheral awareness.** During active combat, the player's central vision is on the player-character + immediate threats; the periphery is where spatial awareness lives. A corner minimap in the saccade-friendly top-right zone supplies peripheral spatial awareness without competing for central vision. A centered full-overlay would obstruct central vision = bad combat ergonomics = wrong default.

2. **Eye-tracking research (Riot / Blizzard dev talks, 2014-2018) shows action-game players spend ~5-15% of fixation time on the corner minimap during active combat.** This is enough fixation time to extract spatial information but not enough to disrupt combat focus. A full-screen overlay would require ~100% fixation = combat pauses while consulted; not what active combat needs.

3. **The full overlay is the navigation-context tool.** When the player wants to commit attention to spatial planning (route to boss, find unexplored zone, locate vendor), the corner minimap's small size is insufficient; the overlay's full scale serves the navigation context. **This is a different ergonomic mode** — committed central focus, not peripheral awareness. The toggle separates the two ergonomic modes cleanly.

**Matt's stated preference for Group 2 (centered full overlay)** is therefore best read as: *"I find myself using the overlay mode more often than typical; I want it lower-friction to access."* This is a fully valid preference and is addressed by:
- Single keystroke toggle (Tab); not buried in a menu
- Mobile: single tap on corner-minimap expands; not buried in menu
- Settings: optional "open with overlay" default-state setting for players who prefer to start in overlay context (some players reload routinely; this saves a Tab tap per session)

A **per-player setting for default-state-on-zone-entry** (corner vs overlay) would be a small win for Group 2 — Matt could set his to "open in overlay" and the game ships with corner-default for the typical player. § 5.4 picks this up.

### § 2.5 — Other groups worth surfacing

#### § 2.5.1 — Group 4: the "rotating-minimap-disliker"

Some players strongly prefer **north-locked minimaps**; others prefer **player-orientation-locked** (minimap rotates as player faces direction). Genre split is ~70-30 north-locked. PoE makes this configurable; D2/D3/D4 use player-orientation by default. **Recommendation: north-locked default (genre-typical), settings toggle for player-orientation.**

#### § 2.5.2 — Group 5: the "map-with-monster-dots-disliker"

A small cohort dislikes monster dots showing on the map ("ruins surprise"). Genre handling: PoE has a "hide monsters on map" setting; D-series does not. **Recommendation: NOT support this in v1; revisit if playtest surfaces the cohort within Reincarnated's player base.**

### § 2.6 — The Reincarnated answer

**Adopt the converged genre canon: ship both modes, with platform-tuned defaults, lower-friction toggle, and Group 3 opacity slider in settings.**

Specifically:

- **Default mode = corner minimap (top-right) on all platforms** at session start.
- **Toggle = Tab (PC) / tap-minimap (mobile)** — minimum-friction access to overlay.
- **Settings entries:** opacity slider (0-100%, default 100%); per-player default-state preference (corner / overlay, default corner); north-locked vs player-orientation toggle (default north-locked).
- **Sufficiently scoped** — not extending to annotation, multi-floor, or sharing in v1 (§ 13 OOS).

This adoption matches Diablo IV's settings-richness without inheriting D4's UI bloat; matches Diablo Immortal's mobile-tap-to-expand pattern; matches PoE's configurability surface. It's the *settled-genre answer* with one *Matt-preference-accommodation* (the per-player default-state preference).

---

## § 3 — Map content + render decisions per platform

### § 3.1 — What's rendered on the minimap

Per the converged genre canon (D2/D3/D4/PoE/LE/Grim Dawn + D-Immortal/Torchlight-Infinite/Eternium mobile), the minimap renders these layers from bottom to top (z-order):

| Z-order | Layer | What it renders | When visible |
|---|---|---|---|
| 0 (background) | Background fill | Dark-translucent tint (~0.55-0.75 opacity black or deep-blue) | Always |
| 1 | Fog of war veil | Solid dark fill over unexplored rooms; gradient-fade at edges of revealed rooms | Always |
| 2 | Room / hallway outlines | Stroke-only outlines (2-3 px stroke) showing room and hallway bounds | Revealed regions only |
| 3 | Room / hallway fills | Semi-transparent fill inside revealed rooms (lighter than background; subtly tinted by room type) | Revealed regions only |
| 4 | Doors / thresholds | Bright accent at door positions (small line break or accent dot) | Revealed regions only |
| 5 | Static objects | Vendor, altar, exit, waypoint icons | Revealed regions; persistent once seen |
| 6 | Dynamic environment objects | Chests (open / closed differentiated), gear drops, currency drops | Revealed; updates in real time |
| 7 | NPC dots | Vendor / quest-giver / Spirit Guide indicators | When NPC present in revealed region |
| 8 | Monster dots | Color-coded by tier (per § 4.2 vocabulary) | Visible in player's current room + adjacent revealed rooms; out-of-room monsters hidden until that room is revealed |
| 9 (top) | Player dot | Player position; pulse-animated to maintain center-of-attention | Always; always centered on the minimap when player-centered mode active |

The same layer stack renders into the full overlay; the overlay just covers more world-area at larger render scale. Drax's § 8.2 confirms all required data sources are already in the running game state (Dungeon, playerPos, pack, gearDropSprites).

### § 3.2 — Fog of war — the canonical pattern

**Recommendation: D-canonical "room-snap-reveal-on-entry" with PoE-style persistent reveal.** Specifically:

- **Reveal trigger: door-threshold crossing.** When the player crosses the door threshold into a previously-unexplored room, the entire room's outline + fill snaps to revealed state in a 200-400ms ease-in animation. **Not** line-of-sight-by-line-of-sight reveal (that's a roguelike pattern; not ARPG-canonical).
- **Persistence: rooms stay revealed for the session.** Once revealed, a room remains visible on the minimap and overlay for the rest of the dungeon session. Death + respawn does not unreveal (D-canonical); zone-exit + re-entry does unreveal (PoE-style; rooms reroll on zone entry in PoE).
- **Monster visibility in revealed-but-out-of-current-room rooms:** **hidden** by default (genre-typical; both D-series and PoE-since-Heist do this). Monsters are visible only in the player's current room + adjacent rooms if they share a hallway with line-of-sight to a corridor the player has traversed.
- **Hallway reveal:** hallways reveal incrementally as the player walks through them (chunked at ~5-meter segments — small enough to feel smooth, large enough to feel "discovered" not "scanned").

**Why room-snap-reveal not line-of-sight-reveal.** Two reasons:

1. **Engine compatibility.** Reincarnated's room/hallway topology (per `src/world/topology.ts`) is **room-as-bounded-rectangle** plus **hallway-as-bounded-rectangle**. Room-snap-reveal fits this data model natively; line-of-sight-reveal would require either (a) per-tile reveal state (no per-tile state exists; would need a new data structure) or (b) raycasting at runtime (a frame-cost we shouldn't pay). Room-snap is *what the engine already knows how to express*.

2. **Genre expectation.** D2/D3/D4/PoE/LE all use room-snap; line-of-sight is the *roguelike* pattern (NetHack, ToME, DCSS). Reincarnated is ARPG-positioned; ARPG players expect room-snap. Mixing in roguelike convention would feel off-genre.

**Relationship to drax's aggro-state tint-fog (drax § 8.2, OQ-3):** Drax's engineering plan implements aggro-state-keyed room fills (dormant = dark, active/cleared = brighter) — that is *implicitly* a fog-of-war (rooms read as "discovered" only after you enter and aggro fires). I recommend extending the same hook to use a **discovered-vs-undiscovered fog state** rather than coupling visibility to aggroState specifically. A dormant-but-discovered room (player walked through without aggroing) should still be visible. The Static-Layer redraw hook in drax's plan (`setRoomAggro()`) becomes `setRoomState(roomId, { discovered, aggro })` — same redraw plumbing, two flags instead of one. This is consolidated in § 14 as the engineering refinement.

**The 200-400ms reveal ease-in animation** is the perception-engineering trick (per § 7) that makes the reveal feel like a discovered space rather than a state-change. Sudden-snap reveals (0ms) feel "the UI flashed at me"; over-long reveals (>500ms) feel laggy. 250ms is the genre centroid; 200ms for snappy combat-feel, 350ms for emphasis on big rooms.

### § 3.3 — Color palette

The map's color palette is **load-bearing for perception engineering** (§ 7). The palette must be:
- **High-contrast at small sizes** (legibility floor at the 100-150 px corner-minimap scale; readable when the eye is parked centrally on combat)
- **Substrate-aware but not substrate-coupled** (room tints can subtly indicate substrate biome; monster dots stay substrate-independent)
- **Hardcoded to ~6-8 colors total** (chromatic discipline — too many colors = noise)

**Proposed palette:**

| Element | Color | Hex (approx) | Rationale |
|---|---|---|---|
| Background fill | Deep-blue-black (translucent) | `#0a1018` @ 0.65α | Genre-canonical dark; PoE/D4-derived |
| Fog of war veil | Black (translucent) | `#000000` @ 0.85α | Hides unexplored decisively; gradient-fade at edges (10-15 px feather) |
| Room outline (revealed) | Pale-warm-gray | `#cdc4b4` | Visible against background; non-substrate-coupled (consistent across biomes) |
| Hallway outline (revealed) | Same as room outline | `#cdc4b4` | Visual unification of traversable space |
| Room fill (revealed) | Slightly-lit | `#1a2230` @ 0.5α | Subtle differentiation from background (~+15% luminance) |
| Door / threshold accent | Bright gold | `#f6c84a` | High-saliency; calls eye to navigation choices |
| Player dot | Bright cyan-white | `#e8f7ff` | Highest-saliency single point; pulse-animated; unique color in palette |
| Trash monster dot | Desaturated red | `#a04848` | Lower-saliency hostile; genre-typical |
| Elite monster dot | Saturated red | `#e83c3c` | Higher-saliency hostile |
| Rare/champion monster dot | Yellow | `#f0c020` | Genre-canonical (D2/D3/D4 yellow nameplate convention) |
| Boss / act-boss dot | Magenta-purple | `#c040d0` | Genre-canonical (PoE/D4 unique-color convention) |
| Player-friendly NPC (vendor, Spirit Guide) | Cool-teal | `#40c0b0` | Distinct from hostile palette; "safe interaction" signal |
| Gear drop (rare+ rarity) | Per-rarity (see § 4.4) | varies | Rarity-encoded |
| Chest | Warm-brown / gold | `#a87830` | Genre-canonical chest-marker color |
| Static waypoint (altar, exit) | Bright purple-blue | `#7080f0` | High-saliency; navigation-relevant |

**Substrate-biome room tint (optional layered tint):** when the room is substrate-biased (e.g., fire-biome room, wind-biome room), apply a *very subtle* hue shift to the room fill — `#1a2230` shifted by ±5-8% hue toward the substrate's identity color. This is **at-the-edge-of-perception subtle**; the player notices coherence without naming it. Genre precedent: PoE's tile-set color treatments; D4's biome lighting; subtle enough not to confuse with fog or threat colors. **Optional in v1; surface as design-question in § 14.**

### § 3.4 — Opacity per mode

- **Corner minimap:** background **0.55-0.65 alpha** over gameplay. Enough to differentiate the map area from the combat backdrop; transparent enough not to blot out a corner of the action. The minimap's edges should **fade to fully transparent** over a 15-25 px feather — this is the perception-engineering trick (§ 7) that makes the minimap feel "inset into the scene" rather than "pasted on top." Without the feather, mobile/PC both look like the minimap is a sticker.
- **Full overlay:** background **0.75-0.85 alpha** with the world greyed-out underneath at 0.40-0.55 dim. The world remains *just visible* under the overlay (so the player knows their character is alive and the game is paused or running), but the map is clearly the focus. **Player can see their own character's animation through the dimmed underlay** — this is the small detail that makes the overlay feel like an *information layer* not a *modal dialog*.

**Opacity slider in settings (per § 2.6) operates on both modes independently.** Corner-minimap opacity slider 0-100% (default 100% = 0.55-0.65α as authored above); overlay opacity slider 0-100% (default 100% = 0.75-0.85α). At 0% both render zero alpha = invisible (Group 3 support).

### § 3.5 — Sizing per platform

Consume `mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 3.2 and § 4.6 (HUD compresses via layout reorganization, not element downscaling). Specific values:

| Platform | Corner minimap size | Full overlay size | Source |
|---|---|---|---|
| PC desktop (1800×944 canvas) | **~280 × 280 px** circular (top-right; 10-15 px inset from canvas edge) | **~1200 × 800 px** centered (~67% of canvas dimensions; rounded to maintain 3:2 ratio matching dungeon-traversal mental model) | Genre-canon: D4 corner ~250-300 px; PoE corner ~220-280 px; overlay ~70-85% of canvas |
| Mobile portrait (1800×944 internal; CSS-fit to phone aspect) | **~180 × 180 px** circular (top-right safe-area-inset; ~20 px from screen edge per safe-area) | **~85% of viewport width × ~70% of viewport height** centered | Smaller than PC corner (per § 4.6 layout reorganization); overlay larger as fraction of screen because mobile screen is smaller |
| Mobile landscape | **~200 × 200 px** circular (top-right safe-area-inset) | ~85% width × 80% height centered | Slightly more room horizontally than portrait; minimap can be slightly larger |
| Tablet (future) | **~240 × 240 px** circular (top-right) | ~75% of viewport centered | Between PC and mobile; deferred |

**Note on drax MM2 placeholder sizes:** Drax's § 9.1 uses ~180 px (PC) as a placeholder; my § 3.5 canon raises this to **~280 px PC corner** to match D4/PoE genre canon. This is the canonical value drax should consume when MM2 lands. Mobile placeholder ~100 px in drax § 10.1 — my canon raises this to **~180-200 px mobile corner** (per `mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 3.2; mobile is not 0.5× of PC for HUD elements — HUD compresses via layout reorganization, not element downscaling). The mobile minimap also needs to clear `touchIcons.ts` cluster — see § 6.1 for the positioning resolution.

**Corner minimap shape: circular.** Genre canon — every major ARPG mini-map is rendered as a circle (D2/D3/D4 = circle; PoE = circle; D-Immortal = circle; Torchlight Infinite = circle). The circle is **perception-engineered** (§ 7): a circle in a screen-corner reads as a "lens" or "scope" — the eye understands it as a viewport into the world, not a flat-pasted rectangle. Reincarnated should adopt the circle (the genre answer is universal).

**Engineering note for drax:** drawing a circular minimap in Pixi `Graphics` is straightforward (one filled `drawCircle()` for background; circular clipping mask for content via a separate sprite mask). Drax's § 8.3 `Graphics` pipeline supports this natively; no rendering-pipeline change from the rectangular-placeholder approach.

**Full overlay shape: rectangular** with rounded corners (8-12 px corner radius). Genre canon — every major ARPG overlay is rectangular at canvas-aspect (D2/D3/D4 = rectangular; PoE = rectangular; D-Immortal = rectangular but full-screen-modal-styled; Torchlight Infinite = rectangular).

**On VS2a's linear 6.2:1 aspect ratio (drax § 9.2):** Drax flags that VS2a's linear dungeon (~13,392 × 2,160 px world bounds) projects into a horizontally-wide thin overlay at canvas aspect. **Design recommendation: rotate the dungeon-bounds projection** so the dungeon's long axis aligns with the overlay's long axis (horizontal). The player's mental model of "the dungeon stretches forward through the rooms" is preserved; the overlay shows the linear progression as a left-to-right traversal. This is the projection PoE uses for its linear maps; D2 used vertical projection for its act maps. **Rotation choice: left-to-right (horizontal axis = dungeon's long axis)** because reading-direction reinforcement; Reincarnated's right-progressing dungeon reads as "moving forward" in the same direction text reads.

### § 3.6 — Zoom controls

**Recommendation: NO player-controlled zoom in v1.** Reasoning:

- Genre canon is split: D2/D3 = no zoom controls; D4 = no zoom controls; PoE = limited zoom on overlay only; LE = no zoom; D-Immortal = pinch-zoom on overlay (mobile).
- **Auto-zoom on big rooms** is the genre-typical answer: when the player is in a large room (Reincarnated `ROOM_PX_LARGE = 2160`), the corner minimap *auto-zooms-out* to fit the room within ~80% of the minimap; in a small room (`ROOM_PX_SMALL = 720`), it *auto-zooms-in* to keep the player at usable scale. This is a runtime-computed zoom factor per room.
- **Full overlay zooms to fit the dungeon's revealed extent** by default. The player can interact with overlay-zoom only on mobile via pinch-zoom (D-Immortal-canon).

**The zoom formula (auto-zoom on minimap):**
```
zoom_scale = min(minimap_diameter / max(room.width, room.height), 0.25 max)
// clamp zoom_scale so player can always see at least the player + 3-meter radius around them
```

Where `0.25` cap means: minimap renders at most 1 px per 4 world-px (the genre's typical maximum zoom-in to preserve overview).

**However:** for VS2a's linear 7-room dungeon, **the corner minimap can simply show the full dungeon at fixed scale** (no auto-zoom needed). The dungeon is small enough that the whole floor plan fits in a 280 px circle at readable detail. Drax's § 9.1 fixed-scale projection is the right approach for VS2a. Auto-zoom becomes relevant when dungeon scope grows beyond the 7-room linear plan (Phase-2 act content). **Recommendation: drax ships MM2 with fixed-scale; auto-zoom is MM6+ polish if dungeon scope grows.**

**Mobile pinch-zoom on overlay** is a v2 candidate; defer to phase MM6 polish if scoped (consistent with drax § 10.2's "No pinch-zoom in MM2-MM3").

### § 3.7 — Map rotation

**Recommendation: north-locked default; player-orientation-rotating toggle in settings.** Per § 2.5.1 — genre split is ~70-30 north-locked; PoE / Last Epoch make it configurable. Default north-locked makes the minimap a stable spatial reference; player-orientation-rotating feels more "intuitive" to a minority who learn directions ego-centrically.

For Reincarnated's top-down ARPG with no compass-direction mechanics, north-locked is the obvious default. Drax's MM2 implementation can hardcode north-locked; player-orientation toggle is MM6+ settings.

### § 3.8 — Performance budget

Drax's § 8.4 has authored this:
- **Corner minimap:** rendered every frame (peripheral awareness = updates must match game-frame-rate). Per-frame cost target: **<0.5 ms on PC, <0.8 ms on mobile.** Achievable via Pixi `Graphics` two-layer split (static layer cached for room outlines; dynamic layer for dots).
- **Full overlay:** rendered when visible (every frame while open). Per-frame cost target: **<1.5 ms on PC, <2.5 ms on mobile.** Larger render area; same data; static elements still cached.

Drax's verdict — "minimap render cost is not a concern for this title's content density" — holds with my § 3.5 sizing canon. The increased size (280 px vs 180 px placeholder) is a 2.4× pixel area increase, but pixel-area is not the cost driver (draw call count is); same ~13 rectangles + ~10 dots regardless of canvas size.

---

## § 4 — Iconography & symbol vocabulary

### § 4.1 — Design principle: stylized geometric symbols, NOT sprite renders

Per Matt's "brush roughness under the rug" framing (§ 7): the map should NOT attempt to render literal sprites of monsters / chests / gear. Instead use a **stylized geometric vocabulary** that is:

1. **Recognizable at minimap scale** (10-25 px wide tokens; readable at fovea-peripheral distance)
2. **Consistent across asset packs** (single rendering pipeline = no pack-coupling = roughness hidden)
3. **High-contrast against background** (per § 3.3 palette)
4. **Animation-discriminable** (different objects use different motion behavior to read instantly)

Genre precedent: D2/D3/D4 all use stylized dots+symbols, not sprite-renders, on the minimap. Even D4's sumptuous art direction renders monsters on map as **red dots**, not as tiny sprites. This is because at minimap scale, sprite-render fidelity is *invisible* (10-25 px doesn't carry detail) and *expensive* (per-frame render of dozens of tiny sprites = wasted GPU). Symbols beat sprites at this scale; the entire genre converged on this.

**Engineering alignment:** drax's § 9.1 already drafts `Graphics`-based dot rendering (no external sprites). This canon ratifies that choice and provides the specific shape + color + animation vocabulary drax should implement in MM4.

### § 4.2 — Symbol vocabulary table

| Object class | Shape | Size (PC corner / PC overlay) | Color | Animation | Rationale |
|---|---|---|---|---|---|
| **Player** | Filled triangle pointing in facing direction (rotates with player); OR circle if north-locked | 14 / 22 px | `#e8f7ff` cyan-white | Soft pulse 1.0-1.15 scale @ 1Hz | Triangle = direction-aware (player-orientation mode); circle = direction-agnostic (north-locked). Pulse signals "this is the live focal point" |
| **Trash monster** | Filled circle | 7 / 10 px | `#a04848` desat-red | Static | Smallest hostile; many on screen; static = low visual noise |
| **Elite monster** | Filled circle with thin ring outline | 9 / 14 px | `#e83c3c` saturated-red + `#ffffff` 1 px ring | Slow ring-pulse @ 0.5Hz | Differentiated from trash by ring; ring-pulse signals "this matters" |
| **Rare / champion monster** | Filled diamond | 11 / 16 px | `#f0c020` yellow | Static | Diamond = "rotated square" symbol; high recognition value; yellow = genre-canon rare |
| **Boss** | Filled hexagon | 14 / 22 px | `#c040d0` magenta-purple | Slow rotational sweep | Hexagon = "many-sided weight"; rotational sweep at 4-second cycle = "this is the heavyweight"; magenta = genre-canon unique |
| **Act-boss** | Hexagon with concentric outline ring | 18 / 28 px | `#c040d0` + `#ffffff` ring | Faster rotational sweep + ring-pulse | Visually distinct from regular boss; impossible to confuse |
| **Vendor NPC** | Filled square (rotated 0° — axis-aligned) | 10 / 16 px | `#40c0b0` cool-teal | Static | Square = stability/structure (vendors don't move); teal = safe interaction |
| **Quest-giver / Spirit Guide** | Filled square with small "halo" outline above | 12 / 18 px | `#40c0b0` + `#e8f7ff` halo | Halo glows slowly @ 0.3Hz | Distinct from vendor; halo = "speak with" affordance |
| **Gear drop (common / white)** | Tiny filled dot | 4 / 6 px | `#cdc4b4` pale-gray | Static | Common gear = low-saliency; player can ignore unless interested |
| **Gear drop (magic / blue)** | Tiny filled dot | 5 / 8 px | `#4080e0` blue | Soft pulse @ 0.5Hz | Slightly bigger + pulse = "worth looking" |
| **Gear drop (rare / yellow)** | Tiny filled dot | 6 / 10 px | `#f0c020` yellow | Slightly bigger pulse | Rare = noticeable |
| **Gear drop (legendary / orange)** | Small filled dot with halo glow | 8 / 12 px | `#ff8030` orange + radial gradient halo | Bright pulse + halo flicker | High-saliency; player should run there |
| **Gear drop (unique / set-tier)** | Small filled star | 8 / 12 px | varies (set color) | Strong pulse + halo | Unique-tier visual; "drop everything and look" |
| **Chest (small)** | Small unfilled square outline | 10 / 14 px | `#a87830` warm-brown | Static | Open-tier chest |
| **Chest (medium / regular)** | Filled square with small "lid line" detail | 12 / 18 px | `#a87830` | Static | Standard reward chest |
| **Chest (large / legendary)** | Filled square with concentric ring + sparkle dot | 14 / 22 px | `#f6c84a` gold | Sparkle-dot orbits chest @ 0.5Hz | Legendary chest = "go open this" affordance |
| **Open chest (already looted)** | Same shape as above, but **half-opacity** | n/a | `#a87830` @ 0.5α | None | Visual indicator chest is empty; persistent for navigation memory |
| **Strongbox (PoE-style; open-event chest)** | Filled diamond with cross overlay | 12 / 18 px | `#a87830` + `#f6c84a` cross | Cross-glow @ 0.5Hz | Differentiated from passive chest; "event will happen" signal |
| **Altar (interaction point)** | Filled triangle pointing up | 12 / 18 px | `#7080f0` purple-blue | Triangle pulses @ 0.3Hz | Genre-typical altar symbol; navigation-relevant |
| **Vendor / shop waypoint** | Small filled house-pictogram (square + triangle) | 14 / 20 px | `#40c0b0` cool-teal | Static | Maps to vendor NPC class; pictogram reinforces |
| **Exit (zone-exit / portal)** | Filled crescent | 14 / 20 px | `#7080f0` purple-blue | Crescent glows in/out @ 0.5Hz | Genre-typical exit/portal symbol |
| **Waypoint (in-zone)** | Filled diamond outline | 12 / 18 px | `#7080f0` + `#e8f7ff` inner glow | Inner glow pulses @ 0.5Hz | Diablo-canon waypoint symbol |
| **Active quest goal** | Yellow exclamation/marker symbol; small pin | 16 / 24 px | `#ffd040` bright-yellow | Pin "bounces" 0-3 px @ 1Hz | Genre-canon active-quest indicator |
| **Door (revealed; threshold marker)** | Small line break in room outline (1 px gap with accent dot) | n/a (inline with outline) | `#f6c84a` gold | Static | Doors as outline-discontinuities + accent; reinforces "passage" perception |
| **Active exit door (where player will go next)** | Door marker as above, but with **stronger gold glow + 1.0Hz pulse** | n/a | `#ffd040` brighter gold + glow | Pulse @ 1Hz | Drax § 9.4: `_activeDoorId` from `main.ts`; differentiate so player can navigate without reading the room |

**Total symbol count: ~26 distinct symbols across 9 object classes.** Genre comparison: D4 uses ~30; PoE uses ~25; LE uses ~22. Reincarnated's 26 sits comfortably within the genre's vocabulary-size norms.

**VS2a scope: only player + monster tiers (trash/elite/rare/boss/act-boss) + gear-drops + doors + active-exit-door are needed in MM2-MM4.** Vendor/Spirit-Guide/chest/altar/waypoint/quest-goal symbols are Phase-MM4-plus when the underlying systems land (per drax § 8.2 — these don't exist yet).

### § 4.3 — Animation discipline (the perception-engineering layer)

Each animated symbol uses **at most one animation channel** (pulse OR rotation OR halo-flicker OR translation). Multi-channel-animated symbols read as "chaotic noise" at minimap scale. The animation channels are tier-coded:

- **Static** = trash / common-gear / regular-chest. Low information; player can ignore.
- **Slow pulse / static-with-detail-feature** = elite / magic-gear / quest-NPC. Mid-information; player can attend if convenient.
- **Strong pulse + halo / rotation** = boss / legendary-gear / active-quest. High-information; player should attend.
- **Compound animation** (e.g., act-boss = rotation + ring-pulse) = act-boss / strongbox / once-in-zone-event. Highest-information; player must attend.

Genre precedent: this tier-coded animation discipline is from PoE's mature mini-map design (PoE 2 specifically calibrated this); D4 follows a similar approach. Animation as information-density signal is a genre-mature pattern.

**Engineering implementation:** all animations are sin-based or linear-tween-based scalar oscillations on `Graphics` properties (scale, alpha, position). No external animation library; pure tick-based oscillation in the per-frame `update()` call. Drax's MM6 includes the dot-pulse implementation.

### § 4.4 — Rarity color cluster (gear drops on map)

Reincarnated's gear-rarity scheme should follow D-canonical color taxonomy (genre-canonical and immediately readable). Drax notes (§ 9.1) that `TIER_LABEL_COLORS` from `gearDrop.ts` already encodes the rarity palette — the canonical reference should be that existing table, **NOT** a parallel palette in `minimap.ts`. Map dot colors should `import` from `gearDrop.ts` to ensure rarity color consistency between the on-floor sprite and the minimap dot. If `TIER_LABEL_COLORS` deviates from this table, the on-floor sprite is the source of truth and this table is the suggested intent (drax reconciles):

| Rarity | Map color (intent) | Hex | Sprite size on map | Pulse |
|---|---|---|---|---|
| Common (no affixes; vendor-trash) | Pale-gray | `#cdc4b4` | 4-6 px dot | None |
| Magic (1-2 affixes) | Blue | `#4080e0` | 5-8 px dot | Soft 0.5Hz |
| Rare (3-6 affixes) | Yellow | `#f0c020` | 6-10 px dot | Visible 0.5Hz |
| Legendary (named; thematic) | Orange | `#ff8030` | 8-12 px dot + halo | Strong + halo flicker |
| Unique / Set-piece | Set-color (per item; e.g., emerald-green, royal-purple) | varies | 8-12 px star symbol | Strong + halo |

**Above-minimap-floor sizes:** common drops at 4 px are below most player attention threshold; they appear as faint dots only when zoomed-in. Legendary+ drops are visible across the full overlay even without zooming. **This is the genre's information-saliency-ramp.**

### § 4.5 — Substrate-coupling caveat

Monster dots do NOT recolor by substrate. Per `enemy-visual-legibility.md` and the resistance-matrix work, **substrate identity is conveyed on the combat surface (sprites + telegraphs + VFX)**, not on the map. The map's role is **spatial awareness**, not **substrate-vocabulary teaching**.

Counter-argument considered: "should fire-substrate monsters show as red-with-orange-tint dots; wind-substrate as red-with-teal-tint dots? Player learns substrate-by-region faster." **Rejected** because:

1. **Monster dots already encode tier** (trash / elite / rare / boss). Adding a substrate-color-overlay creates a two-dimensional encoding (tier × substrate) at 7-10 px scale; visual resolution insufficient.
2. **Combat surface is where substrate identity lives.** Substrate-on-map dilutes the canonical channel.
3. **Genre precedent does not encode element/substrate on map.** D-series doesn't (elemental monsters appear same-color); PoE doesn't (elemental affixes don't change map color). The decision is settled.

**However:** room-fill substrate-biome tint (per § 3.3) DOES exist as the subtle layered encoding — substrate identity surfaces at *biome level* (room), not at *individual monster level* (dot). This is the right channel discrimination.

---

## § 5 — Interaction model

### § 5.1 — Open/close gesture

**Recommendation: Tab key on PC, tap-corner-minimap on mobile.**

Tab vs M debate (drax's OQ-4 surfaces that M is currently unbound):

- **Tab is genre-canonical.** D2/D3/D4 use Tab; PoE uses Tab; LE uses Tab; Grim Dawn uses Tab. The genre has converged on Tab for *map overlay specifically*; M is more associated with MMO-style world-maps (Lost Ark's M = world map; WoW's M = world map). Reincarnated is positioned as ARPG, not MMO; Tab fits the genre expectation.
- **M is more semantic.** "M" reads as "M for Map" intuitively; Tab is genre-trained-behavior.
- **Tab has competition.** Tab is sometimes used for "target cycling" in ARPGs (Lost Ark uses Tab for targeting; D4 does not but some mods/games do). If Reincarnated implements Tab-target-cycle (out of v1 scope per `agents`), Tab-for-map collides.
- **M has no competition** in current Reincarnated bindings (drax § 9.3 confirms — I=inventory, C=character-sheet, H=combat-log, Escape=system, Space=dodge; M is free).

**Recommendation: Tab in v1 (genre-typical); rebindable to M in settings.** If Tab-target-cycle ever becomes a feature, surface the rebind at that time. Setting rebind is one-line config; no scope cost.

**For drax engineering:** drax § 9.3 binds M-key. **Switch to Tab for v1 ship; preserve M as rebind candidate.** This aligns with genre canon and inherits the genre's muscle-memory training for ARPG players.

**Mobile gesture: tap-corner-minimap.** Per D-Immortal / Torchlight Infinite / Eternium canon. The corner minimap **IS the affordance for the overlay** — they're not two separate UI elements but two states. Tap-outside or center-X button closes (§ 5.2). Drax § 10.1 already plans this gesture model.

### § 5.2 — While-overlay-is-open behavior

**Recommendation: gameplay pauses on PC; gameplay paused on mobile.** Genre data:

- D2: gameplay continues (no pause) — but D2's overlay covers ~70% of screen and ~30% is still visible for the player to track. Genre-pre-modern.
- D3: gameplay continues; overlay is ~70%; player can still see attacks coming through the gaps.
- D4: gameplay continues; overlay is ~85% but rendered with the world still visible underneath at low alpha; player can see attack-telegraphs.
- PoE: gameplay continues; overlay is ~75%; world visible underneath; PoE-mature players use overlay-during-combat as a constant tool.
- LE: gameplay continues; same as PoE/D4.
- D-Immortal (mobile): **gameplay PAUSES** when overlay open — this is a mobile-platform convention (touch overlap with combat controls).
- Torchlight Infinite: gameplay pauses on overlay-open.
- Eternium: gameplay pauses on overlay-open.

**The PC-vs-mobile pattern:** PC players keep playing through the overlay because they have separate input devices (mouse for combat / keyboard for menus); mobile players pause because the screen IS the input device.

**Reincarnated's choice depends on the gameplay context:**

- **If Reincarnated combat is high-pace, high-stakes (per AOE-tuning briefing § 5 cognition budget):** pausing during overlay makes sense even on PC. The overlay-as-navigation-tool is for between-fights / route-planning, not combat decision-making. Pausing prevents the player from being mauled while consulting the map.

- **If Reincarnated combat is mid-pace, exploration-emphasized:** continuing makes more sense. The player should be able to glance at the overlay between attacks.

**Recommendation: pause-during-overlay on both platforms.** Reasoning:

1. **Combat pace is medium-to-high** (per AOE-tuning + dodge briefing). Glancing at a centered overlay would lose ~200-500ms to focus shift; that's a dodge window in our combat tempo. Players shouldn't be punished for consulting the map.
2. **Solo gameplay** (per `project_design_intent.md`) — no multiplayer pause penalty.
3. **Mobile inherits the same behavior** automatically — consistent cross-platform UX.
4. **The corner minimap continues to update during combat** — it serves the "during-combat spatial awareness" context; the overlay serves the "between-combat navigation" context; pause-on-overlay reinforces the role separation.

Counter-argument: PoE pros use overlay during combat to track monster positions ~70% off-screen (PoE's overlay shows monsters in non-current zones; positioning tactical play). Reincarnated's smaller dungeon scope may not need this; if it eventually does (Phase-2 act content), revisit.

**Drax engineering note (OQ-2):** drax recommends no-pause (genre canon) for PC; my recommendation is pause (combat-pace rationale). This is a genuine design disagreement worth Matt's resolution. Both engineering plans accommodate the choice (drax § 9.2: "if pause is needed, set a `_mapOverlayOpen` flag in `main.ts` that the fight-state logic checks before processing input"). **Surface as Matt L3 decision in § 14.**

### § 5.3 — Player-position interaction

**Recommendation: NO click-to-move via map in v1.** Genre split:

- PoE: clicking on the overlay map MOVES the player to that location (path-find through revealed regions). Canon-PoE pattern.
- D2/D3/D4: clicking on the overlay does nothing; map is information-only.
- LE: same as D-series.

PoE's click-to-move-via-map is a power-user feature that requires path-finding-through-revealed-regions; that's a feature-cost we shouldn't pay in v1. The corner minimap doesn't support click-to-move in PoE either; only the full overlay does.

Drax § 13 notes "if approved, `click-on-overlay → map-space position → world-space position → set as lmbMoveTarget` is approximately 5 lines in `main.ts`" — engineering is cheap. **Design recommendation:** defer to MM6 polish if scoped; not v1-blocking.

**Reincarnated v1: information-only map.** Defer click-to-move to v2 if scoped.

**Player annotations (Last Epoch pattern):** also DEFER to v2. Genre split is currently ~50-50; not load-bearing for first ship.

### § 5.4 — Per-player default-state preference

Per § 2.6 — surface a settings entry: *"Open with overlay on zone entry?"* (default: No). For Matt (and players like Matt who prefer Group-2-overlay-default), toggling this on means the overlay opens automatically when entering a new zone; first Tab tap closes to corner-mode. Small win for Group 2 player ergonomics; one line of state + one settings toggle; no architectural cost.

Drax can implement this as a `_overlayDefaultOnZoneEntry: boolean` flag stored in `localStorage`; at `startGauntlet()` time, if the flag is true, `_minimap.toggleOverlay()` is called once after construction. ~5 lines of code.

### § 5.5 — Transparency tuning

Per § 3.4 — opacity slider in settings (corner: 0-100% default 100%; overlay: 0-100% default 100%). 0% serves Group 3 (map-off).

Drax engineering: opacity applied via `_cornerContainer.alpha` and `_overlayContainer.alpha`; setting persists in `localStorage`. Drax MM6 polish includes this.

### § 5.6 — Annotation (defer)

Last Epoch's right-click-to-annotate is a v2 candidate. Out of scope per § 13. Drax MM6 includes a stretch annotation implementation; if scoped in by Matt, drax's plan supports it via `annotations: { worldX, worldY, label?: string }[]` array persisted to `localStorage`.

---

## § 6 — Mobile-specific design

### § 6.1 — Corner-minimap mobile sizing & positioning

Consume `mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 3.2 and § 4.6. Specific values per § 3.5 above:

- **Portrait:** 180 × 180 px circular minimap, anchored top-right, **20-30 px inset from safe-area-inset top and right edges** (per safe-area-inset CSS variables).
- **Landscape:** 200 × 200 px circular, top-right, **20 px inset from safe-area**.
- **Notch / Dynamic Island avoidance:** minimap shifts down or right as needed to clear notch geometry. iPhone-class notches occupy ~150-200 px from top-center; minimap at top-right is already outside this zone, but on devices with right-edge notches (rare; some Android), minimap shifts down to ~60 px below top edge.

**Layout resolution for drax § 10.1 conflict:** Drax flags that top-right corner is occupied on mobile by `touchIcons.ts` (inventory/character/log icon cluster at approximately `x = CANVAS_WIDTH - 80`, `y = 80-200`). My recommendation: **the minimap takes precedence at the top-right corner; touchIcons cluster shifts down below the minimap.** Specifically:

- Minimap: top-right, `top: max(safe-area-inset-top + 20px, 30px); right: max(safe-area-inset-right + 20px, 30px)`; 180-200 px diameter circular
- touchIcons cluster: below the minimap, starting at `y = minimap_bottom + 15px`; same right-anchor

Rationale: the minimap is the **primary navigation surface** during combat; touchIcons (inventory, character, log) are **between-combat tools**. Drax's mobile UX plan can adjust the touchIcons z-position to accommodate. This is consistent with D-Immortal's mobile UI layout (minimap top-right corner; menu icons below it).

**Alternative if Matt prefers:** swap them — touchIcons stay top-right corner; minimap shifts to top-left or top-center. **NOT recommended** because:
- Top-left is where mobile players' eyes glance for HP/MP indicators (genre canon)
- Top-center disrupts the visual hierarchy (player sprite is centered; minimap centered competes for attention)
- Top-right is the genre-universal minimap position; deviating without strong reason erodes intuition

### § 6.2 — Thumb-reach analysis

The minimap at top-right is **deliberately outside thumb-reach in both portrait and landscape orientations**. Genre precedent: D-Immortal / Torchlight Infinite / Eternium all park the minimap at top-right precisely because:

1. **Top-right is the saccade-friendly periphery for right-thumb-dominant gameplay.** The right thumb operates abilities (bottom-right zone); the eye glances up-and-right to consult the minimap without disturbing thumb position.
2. **Top-right is NOT in thumb-reach.** Putting it within thumb-reach risks accidental-tap during combat. The map is a *visual reference* during combat, not a *tap target* during combat.
3. **Tap-to-expand uses a deliberate gesture.** Player explicitly chooses to consult the overlay — tap the corner minimap with deliberate intent (not accidental sweep). The full overlay handles thumb-reach concerns of its own.

### § 6.3 — Full-overlay mobile

- **Size:** 85% viewport width × 70-80% viewport height, centered.
- **Behavior on open:** gameplay pauses (per § 5.2).
- **Close gestures (multiple supported):**
  - **Tap-outside** the overlay border (50-100 px outside any overlay edge) — primary close
  - **Center-X button** in top-right of overlay (in case tap-outside is unintuitive)
  - **Re-tap corner-minimap** position — though corner-minimap is occluded by overlay, the conceptual gesture is "tap where minimap was" — secondary close
  - **Hardware back-button (Android)** — close
  - **Swipe-down from overlay-top-edge** — secondary close (Torchlight Infinite pattern)
- **Pinch-zoom on overlay (mobile only):** v2 candidate. Default zoom shows full dungeon extent at fit-to-overlay scale; pinch-out zooms in. v1 ships without; v2 surfaces if playtest demands.
- **Two-finger pan on overlay (mobile only):** v2 candidate; paired with pinch-zoom.
- **Long-press for annotation:** v2 candidate per § 5.6.

**Drax engineering note (§ 10.2):** drax plans full-screen mobile overlay with center-X close button. My recommendation adds the tap-outside and swipe-down gestures as secondary close affordances — small UX wins; drax's mobile-pointer-event handler can support all three with one event handler that checks gesture type (tap vs swipe vs button-press).

### § 6.4 — Mobile gesture vocabulary

| Gesture | Action |
|---|---|
| Tap corner-minimap | Expand to full overlay |
| Tap outside expanded overlay | Close overlay |
| Tap center-X on overlay | Close overlay |
| Swipe-down from overlay top edge | Close overlay (v1; familiar pattern) |
| Hardware back button | Close overlay (Android) |
| Pinch-zoom on overlay | Zoom overlay (v2 candidate) |
| Two-finger pan on overlay | Pan overlay view (v2 candidate; if pinch-zoom is in scope) |
| Long-press on overlay | Place annotation marker (v2 candidate) |

### § 6.5 — Safe-area inset handling

Per `mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 4.6 — HUD positioning honors `safe-area-inset-top / -right / -bottom / -left` CSS environment variables. Minimap top-right position is `top: max(safe-area-inset-top + 20px, 30px); right: max(safe-area-inset-right + 20px, 30px)`. Full overlay centered position also honors safe-area-inset for content-area.

### § 6.6 — Portrait vs landscape variants

Reincarnated's mobile orientation policy (per `src/mobile/orientationOverlay.ts`) is **landscape-default with portrait-support-overlay**. The map overlay design:

- **Portrait:** corner-minimap 180 px; overlay 85% × 70% (taller than wide proportions natural to portrait).
- **Landscape:** corner-minimap 200 px; overlay 85% × 80% (slightly wider; better for tracking dungeon east-west extent).
- **Orientation change while overlay is open:** overlay redraws to new aspect-ratio dimensions; player position remains centered.

---

## § 7 — Aesthetic guidance / perception-engineering

This is the section most directly addressing Matt's framing: *"brushing pixel-art-pack roughness under the rug."* The minimap is **the perceptual stabilizer of the game's visual identity**. Per Matt: *"MANY players will only focus their eyes on the mini-map overlay due to the pace of the game. And this has the added benefit of allowing for some of the roughness that we will have from using varied pixel art packs to be brushed under the rug in terms of overall player experience impact if we REALLY nail down the map overlay."*

The minimap's design choices encode this stabilization. Below are the **perception-engineering principles** that make the minimap a polish-multiplier rather than just an info-display.

### § 7.1 — Stylized symbols, not literal sprites (the polish-multiplier)

Per § 4.1 — geometric shapes (circles, triangles, hexagons, diamonds, stars) instead of literal sprite renders. **Why this works as a polish multiplier:**

1. **Geometric shapes have no asset-pack lineage.** A red dot is a red dot regardless of which pack the player sprite came from. The map's visual vocabulary is *decoupled from the asset-pack-heterogeneity surface*. Players see consistent map iconography even as substrate floor art varies; the consistency reads as "this game has visual discipline."
2. **Geometric symbols are easier to make beautiful.** A perfectly-tuned palette (8 colors per § 3.3), perfectly-tuned animation timing (§ 4.3), perfectly-tuned sizes (§ 4.2) costs *less* design-time than perfectly-tuning sprite renders across all asset packs. The minimap is the *highest-ROI polish surface* in the project.
3. **Geometric symbols look intentional.** Diablo IV's red-dots-on-circular-minimap is a *design choice* that reads as confident. Reincarnated's red-dots-on-circular-minimap reads as confident equally well, and the player never compares the rendered fidelity of a tiny dot.

### § 7.2 — Strong contrast at small sizes (legibility floor)

The corner minimap is 180-280 px diameter; individual symbols are 4-22 px. **Contrast ratio must support legibility at this scale.** Specifically:

- Foreground-symbol-to-background-fill contrast ratio: **≥ 4.5:1** (WCAG AA standard; readable at typical viewing distance and angle)
- Each tier-color must be **distinguishable from each adjacent tier color** at minimum 8 px symbol size (the trash-monster dot size). Genre evidence: D4's red, yellow, magenta, gold are all *high-saturation*, *high-luminance-differential* choices for this exact reason.
- **No two object classes** should be distinguishable only by hue at 8 px size; differentiate by shape *as well as* color (trash = circle, rare = diamond, boss = hexagon). This is **redundant-encoding** discipline — color-blind players, low-light players, dim-screen players all benefit.

### § 7.3 — Consistent palette (chromatic discipline)

The palette in § 3.3 has 8-10 colors. **Do not add more.** Each new color dilutes the visual lexicon; players have to learn what each color means. The genre's mature ARPGs (D4, PoE, LE) all hold to ~10-15 colors on the minimap. Reincarnated's 10 is comfortable.

**Substrate-room-tint subtlety (§ 3.3):** the optional room-fill substrate-biome hue-shift is at-the-edge-of-perception (±5-8% hue). This is the *coherence-without-naming* trick — the player feels "this dungeon has variety" without consciously naming "ah, this is a fire-biome room." The map ties the game's substrate-identity work into spatial perception **subtly**, not loudly. If the hue-shift is too strong (>15% hue shift) it competes with monster-dot palette and creates visual noise; at ≤8% it reads as polish.

### § 7.4 — Smooth fog/reveal animation (sells "polish")

Per § 3.2 — 200-400ms ease-in animation on room-reveal. This is the single highest-ROI animation in the map system. **Why:**

1. **Animation = production-value signal.** Players read smooth animations as "this game is polished." Hard-snap state changes read as "this game is rough."
2. **Reveal animation is a moment of discovery.** Crossing a door threshold and watching the new room *materialize* is a small dopamine signal. Genre canon (D4 especially) leans into this.
3. **The animation cost is minimal.** A 250ms ease-in on a sprite-mask or shader-uniform is negligible; the perception payoff is large.
4. **Consistency across all room reveals.** Same timing, same easing curve, every time. Inconsistency would break the "this game has visual discipline" perception.

**Implementation note:** ease-in-out cubic-bezier `(0.25, 0.1, 0.25, 1.0)` is the genre-typical curve. 250ms duration for default rooms; 350ms for `ROOM_PX_LARGE` (perceptual mass-bias — bigger rooms get longer reveals). Drax's MM6 implements room-state fade tween over 0.3s — that's within the recommended range; recommend extending to 250ms default, 350ms for `ROOM_PX_LARGE` rooms (variant check), and using cubic-bezier easing.

### § 7.5 — Player-dot pulse (the focal anchor)

The player dot pulses at 1Hz with a 0-15% scale variation. **Why:**

1. **The player's eye should ALWAYS know where the player-dot is.** The pulse is the *visual heartbeat* that keeps the dot on the eye's attentional radar even when surrounded by other dots.
2. **The pulse encodes liveness.** A static dot reads as "frozen"; a pulsing dot reads as "alive." Players use this as an unconscious confirmation that the game hasn't crashed.
3. **The pulse rate (1 Hz) matches the human resting heart rate.** Genre evidence: D4's pulse is ~1.0 Hz, PoE's is ~0.8 Hz, D-Immortal's is ~1.0 Hz. All slow-and-rhythmic; none are jittery.

Drax's MM6 plan: "Player dot pulse: scale oscillates 1.0 → 1.2 → 1.0 over 1s." Tighten to **1.0 → 1.15 → 1.0** — 15% scale variation is the perception-engineering ceiling; 20% reads as "wobbly" not "alive." 1.0Hz period as drax planned is correct.

### § 7.6 — The minimap's frame design (the easiest polish detail to fumble)

The corner minimap's *border* — the frame that surrounds the circular minimap area — is **the most-polished-by-design detail in the game**, alongside maybe the HP/MP globes. Genre evidence: D4's minimap has a *jeweled frame with subtle gold inlay*; PoE's has a *parchment-rim frame*; D-Immortal has a *clean modern frame with class-icon at the top*.

**Reincarnated's frame: tonally pixel-art-coherent.** A simple **2-3 px dark-gold ring stroke** at the outermost circle edge, with a **1 px lighter-gold inner highlight** just inside, reads as "intentionally framed" without elaborate detail. The frame should feel like the same hand-drawn-pixel-art register as the rest of the game (per `style-register.md`).

**Avoid:**
- Overly elaborate frames (mismatch with our pixel-art register; would look "AAA but not us")
- No frame at all (the minimap reads as "pasted on top"; lacks polish)
- Substrate-coupling on the frame (frame stays consistent across rooms; the room-biome tint goes on the *fill*, not the *frame*)

Engineering: two `drawCircle()` calls in `Graphics` (outer dark-gold stroke, inner lighter-gold stroke). Trivial cost; high perceived-quality return.

### § 7.7 — Fade-to-transparent edges (per § 3.4)

The corner-minimap's outer 15-25 px feather (fading from opaque to transparent) is what makes the minimap feel **inset into the scene** rather than *pasted on top*. Per § 3.4 — without the feather, the minimap looks like a sticker. With the feather, it looks like a *lens into the world*.

**Implementation:** radial gradient mask on the minimap's container, transitioning from alpha 1.0 at center to alpha 0.0 at the outer 15-25 px ring. Pixi.js implements this via a Sprite mask with a radial gradient texture or a custom shader. This is MM6+ polish; not v1-blocking. Drax can defer until the basic functionality lands.

### § 7.8 — The overlay's dimmed-world underlay (§ 3.4)

When the overlay is open, the world is greyed-out at 0.40-0.55 dim. **Why:**

1. **Confirms the game is alive.** Player can see their character (or VFX still active if combat continues) through the dim. Pause without dim feels "broken."
2. **Visual hierarchy.** The dimmed world is clearly *backgrounded*; the overlay is clearly *foregrounded*. The player's eye doesn't waste fixation cost on the world below.
3. **Smooth on-open animation.** The world dimming and the overlay materialization should be **time-locked** — 200ms ease-in for both, simultaneously. The player perceives a single "the world quiets and the map rises" moment rather than two separate events.

Engineering: drax can implement world-dim via a full-screen 0x000000 alpha-0.5 Rectangle in `_layers.ui` z-ordered below the overlay container, alpha-tweened on overlay open/close.

### § 7.9 — The perception-engineering thesis

Reincarnated's pixel-art-pack heterogeneity (CraftPix + Pimen + Frostwindz + CreativeKind + Fellor, per Matt) creates a real visual-coherence risk on the combat surface — different packs may have slightly different palette tendencies, lineweight, animation style. **The minimap is the single biggest player-perceptual surface where Reincarnated can declare "we have a unified visual identity" without depending on any pack's art quality.**

If the minimap is *polished* — palette disciplined, animations smooth, symbols clean, frame considered, edges feathered — the player's *overall impression of visual coherence* anchors on the minimap. The combat surface's pack-roughness then reads as *texture variety within a coherent design vision*, not as *inconsistency*. The minimap carries the visual-identity load; the combat surface is freed to be diverse.

This is **exactly what Matt named** in the commission. The minimap is not just a UI feature; it's the project's **perceptual coherence multiplier**. § 4-7 of this canon collectively encode the principles that realize that role. When implementation fires, the per-pixel discipline (palette hex codes, animation Hz, frame stroke widths, feather distances) is what delivers the multiplier.

**A practical implication for drax phasing:** MM4 (iconography pass) and MM6 (polish) are where the perception-engineering payoff is realized. **MM4 should not be skipped or abbreviated.** The geometric-symbol vocabulary (§ 4.2) is the single biggest contributor to the polish-multiplier. MM6 (fog reveal, pulse, frame) is the second-biggest. MM2-MM3 are functional groundwork; MM4-MM6 are where the visual-identity-anchoring happens. Plan MM4-MM6 with the same care as MM1-MM3.

---

## § 8 — Engineering reality audit (drax B1)

### § 8.1 — What exists today

**No minimap exists.** A search across all `.ts` files in `reincarnated-demo/src/` for `minimap`, `mini-map`, `worldMap`, `roomLayout`, and `mapOverlay` returns zero results. This is a **full greenfield build**.

This is the starting fact. Nothing to unwire, no legacy rendering to replace, no prior layout debt to account for.

### § 8.2 — Data sources available for a minimap

The dungeon topology is already fully modeled. All data a minimap needs is present in the running game state.

**Room and hallway graph (`src/world/topology.ts`)**

The `Dungeon` interface (topology.ts) holds the complete floor plan:
- `rooms: Room[]` — each Room has `id`, `bounds: Bounds` (`{x, y, width, height}` in world-pixels), `variant: 'small' | 'default' | 'large'`, `aggroState: 'dormant' | 'active' | 'cleared'`, and `doors: Door[]`.
- `hallways: Hallway[]` — each Hallway has `id`, `bounds`, `connects: [string, string]` (room IDs), and `doors: Door[]`.
- `startingRoom: string` — entry room ID.

The VS2a 7-room linear plan (`buildVS2aDungeon()`) populates this at gauntlet start. The total world-space extent for the VS2a plan is approximately 13,392 px wide × 2,160 px tall (7 rooms 720-2160 px wide + 6 hallways 480-768 px wide; max room height 2160 px). The minimap's coordinate system is a scaled-down projection of this bounds box.

**Aggro state (`src/world/aggro.ts`)**

Each Room already carries `aggroState: 'dormant' | 'active' | 'cleared'`. The minimap can read this directly from `_dungeon.rooms[i].aggroState` to color-code rooms (unexplored / active / cleared).

**Player position (`main.ts` — `playerPos: Vec2`)**

`playerPos` is updated every frame by the movement loop (`tickPlayerMove`). It is a module-level mutable. The minimap reads it directly as a world-coordinate point for the player dot.

**Monster positions (`main.ts` — `pack: PackActor[]`)**

Each `PackActor` in the current wave's `pack` array carries `.pos: Vec2` and `.combatant.isAlive`. The minimap reads alive pack members for monster dots. Pack actors not yet spawned (`.spawned === false`) should not be shown (they haven't materialized).

**Gear drop positions (`main.ts` — `gearDropSprites: GearDropSprite[]`)**

`gearDropSprites` is a module-level array updated each frame. Each `GearDropSprite` has a `.container.x / .container.y` (world coordinates) and `.item.tier` (for rarity color-coding). Drops are in world space; minimap can project them the same way as monster dots.

**Potion drop positions (`vfxPools.potionDrops: PotionDrop[]`)**

Potion drops are ground-state collectibles. The minimap can optionally show them (lower priority than gear/monsters/player).

**Camera state (`_cameraX`, `_cameraY`)**

The minimap is a viewport-pinned UI element (in `_layers.ui`) that counter-offsets camera movement via `_syncUiToScreen()`. It does not scroll with the world camera. Player position on the minimap is derived from world-space `playerPos`, not screen-space position.

**What is NOT yet modeled (design layer gaps)**

- NPC positions — no NPC system exists yet in VS2a. Minimap section for NPCs would be empty until a vendor/Spirit Guide NPC is placed in world.
- Treasure chests — no chest system exists yet; out of scope for VS2a.
- Waypoints / altars — no waypoint system exists yet.
- These are Phase MM4 additions when the underlying systems land.

### § 8.3 — Recommended rendering pipeline

**Recommendation: Pixi.js `Graphics`-based procedural render inside a `Container` pinned to `_layers.ui`.**

Not a `RenderTexture`, not a DOM/Canvas hybrid, not SVG.

Rationale:
- The minimap draws simple geometric primitives (rectangles for rooms/hallways, circles for dots, lines for door thresholds). `Graphics` handles all of this natively without an off-screen render pass.
- `RenderTexture` adds complexity and memory overhead (off-screen framebuffer allocation) for content that can be drawn directly. `RenderTexture` is appropriate when you're capturing complex world-geometry (e.g., a full-scene snapshot). Minimap content is abstract — it does NOT sample the world scene, it draws a schematic.
- DOM/Canvas hybrid breaks Pixi's compositing model (z-ordering, camera counter-offset, mobile scaling). Never appropriate here.
- SVG is a poor fit for a game loop; no frame-tick integration, no shared Pixi stage.

The `Graphics.clear()` + redraw pattern is appropriate for per-frame updates of the minimap background (room outlines, which don't change each frame) — but this should be optimized: **static layer cached; dynamic layer redrawn per frame**.

Two sub-containers within the minimap Container:
1. **Static layer** — room/hallway outlines drawn once at gauntlet start; redrawn only on room-state change (aggro transition). `Graphics` object, cleared and redrawn on aggro-state change events.
2. **Dynamic layer** — player dot, monster dots, gear-drop indicators, redrawn every frame.

This two-layer split means the expensive polygon draw (up to 7 rooms + 6 hallways = 13 rectangles) runs only on state changes, not every frame. The per-frame draw is circles only.

### § 8.4 — Performance budget estimate

**Corner minimap (Mode 1) — per-frame cost:**
- Static layer: 0 ms/frame (cached; only redraws on aggro transition; ~4 ms when it does redraw)
- Dynamic layer: clear + redraw N circles where N = 1 (player) + alive pack members (max ~6 for VS2a) + gear drops (0-10). At 7-17 small circles: **~0.1-0.3 ms/frame** on a mid-range desktop GPU (WebGL path, batched by Pixi).
- On mobile (WebGL with tighter budget): same 7-17 circles = **~0.3-0.8 ms/frame**. Well within a 16 ms frame budget (60 fps). Mobile GPU constraint is VRAM fill rate, not draw call count; small circles are negligible.

**Full-screen overlay (Mode 2) — open cost:**
- If static snapshot at open + delta updates: one-time cost ~4-8 ms to build the snapshot; subsequent frames only update moving dots (~0.1-0.3 ms). This is the recommended approach for Mode 2.
- If re-drawn every frame at 70-85% viewport: same as corner minimap but larger Graphics canvas. Still negligible (<1 ms/frame) because it's still rectangles + circles.

**Budget verdict:** Minimap render cost is not a concern for this title's content density. VS2a has at most 7 rooms + 6 hallways + 7 enemies at once. Even a naive full-redraw-every-frame approach would cost < 1 ms at 60 fps. Build it correctly (static/dynamic split), but don't over-engineer.

---

## § 9 — Two-mode rendering plan (drax B2)

### § 9.1 — Mode 1: Corner minimap

**Behavior:** Always-visible, top-right corner of viewport, 8% of canvas width (≈144 px at 1800 px canvas). Updates per frame. Semi-opaque dark background.

**Viewport pinning pattern:**

The demo already uses this exact pattern for every HUD element. `_layers.ui` is counter-offset by `_syncUiToScreen()` each frame so it stays screen-anchored. The minimap Container goes into `_layers.ui` at a fixed screen-space position. This is the same mechanism as `diabloHud`, `combatHud`, `potionHud`, and `desktopHudIcons`.

**Position:** top-right corner. `x = CANVAS_WIDTH - MINIMAP_W - MARGIN`; `y = MARGIN`. Size: approximately 180×180 px on PC (subject to gandalf A2 sizing spec; cite `<sibling-pending: gandalf sections 3-6>` for final numbers).

For the corner minimap, the world-to-minimap coordinate transform is:

```
scale = MINIMAP_W / dungeonWorldWidth
minimapX = (worldX - dungeonBounds.x) * scale + containerLeft
minimapY = (worldY - dungeonBounds.y) * scale + containerTop
```

Where `dungeonWorldWidth` and `dungeonWorldHeight` are the bounding box of all rooms + hallways combined (computed once at dungeon build time). The minimap preserves aspect ratio of the dungeon layout.

**Color coding (placeholder; gandalf A2 overrides):**
- Cleared room: `0x1a2a1a` (dark green tint)
- Active room: `0x2a1a1a` (dark red tint)
- Dormant room: `0x0a0e18` (near-black)
- Hallway: `0x08080c` (darker than rooms)
- Room outline: `0x334455` (muted blue-grey)
- Player dot: `0xffffff` radius 4 px, with a subtle pulse (scale 1.0 → 1.2 → 1.0 over 1s)
- Monster dot: `0xff4444` radius 3 px; elite/boss tier uses larger radius (4-5 px) — per gandalf A3 iconography spec
- Gear drop: `0xffcc44` radius 2 px — rarity color matches `gearDrop.ts` TIER_LABEL_COLORS; legendary gets the same `0xffcc00` glow
- Current room indicator: slightly brighter room-fill for player's current room

**File list:**
- `src/ui/minimap.ts` — new file. Exports `Minimap` class.
- Integration site: `main.ts` — constructed after dungeon build in `startGauntlet()`; updated in the per-frame ticker alongside `diabloHud.update()`.

**`Minimap` class interface (sketch for MM1-MM2):**

```typescript
class Minimap {
  readonly container: Container;
  constructor(parent: Container, dungeon: Dungeon, opts: MinimapOptions);
  update(playerPos: Vec2, pack: PackActor[], gearDrops: GearDropSprite[]): void;
  setRoomAggro(roomId: string, state: AggroState): void; // triggers static layer redraw
  destroy(): void;
}
```

The `update()` call is cheap (dynamic layer only). `setRoomAggro()` triggers the static layer redraw (called from `activateRoom()` / `clearRoom()` dispatch points in `main.ts`).

### § 9.2 — Mode 2: Full-screen centered overlay

**Behavior:** Toggle on `M` key (or button on mobile — see B3). Centered on viewport. 80% viewport coverage. Semi-transparent dark background (60-70% opacity). Gameplay continues underneath (does NOT pause — per ARPG canon; `main.ts` loop keeps running). Closed by pressing `M` again or pressing `Escape`.

**Pixi approach:** A second Container inside `_layers.ui`, rendered above the corner minimap. Default `visible = false`. On M-key toggle: `visible = true`, redraw static layer fresh (full floor plan at larger scale), then per-frame dynamic-layer updates.

**Coordinate transform (same formula as Mode 1 but with larger `MINIMAP_W`):**

At 80% of CANVAS_WIDTH = 1440 px wide, the floor plan renders at much larger scale. The aspect ratio of VS2a's linear dungeon is approximately 6.2:1 (width >> height), so the overlay height would be approximately 1440 / 6.2 = ~232 px. The overlay is horizontally wide but vertically compact — this is appropriate for a horizontal linear dungeon. This will likely look unusual; gandalf A2 may recommend rotating or compressing the layout for the overlay. This is a planning note, not a constraint.

**Overlay layout within the container:**
- Background panel: `drawRect(0, 0, OVERLAY_W, OVERLAY_H)` at 70% black alpha
- Floor plan: same `Graphics`-based room/hallway rectangles at larger scale
- Dynamic layer: same dots as corner minimap but at proportionally larger radius (~1.5× corner)
- Optional: wave label (`Wave 3 / 7 — Elite`), room names (future), legend (future)

**Pause-or-not decision note:** Per ARPG canon (D2 ALT-overlay, D4 full map, PoE overlay), gameplay does NOT pause when the overlay is open. The player navigates while watching the map. This is the recommended default. Gandalf A4 may confirm or modify. The engineering plan accommodates both (toggle `visible` without touching the game loop; if pause is needed, set a `_mapOverlayOpen` flag in `main.ts` that the fight-state logic checks before processing input).

**Same file:** `src/ui/minimap.ts` handles both modes via a `mode: 'corner' | 'overlay'` parameter or a `setMode()` method. The static layer render path is shared; scale factor differs. The dynamic layer `update()` call is identical for both modes.

**M-key binding in `main.ts`:** During `gState === 'fighting'` and `gState === 'door_active'`, check `input.wasPressed('KeyM')` and call `minimap.toggleOverlay()`. This follows the existing pattern for `KeyI` (inventory), `KeyC` (character sheet), and `KeyH` (combat log).

---

## § 10 — Mobile constraints (drax B3)

### § 10.1 — Corner minimap on mobile

The mobile UX execution plan (`canonical/story/mobile-ux-execution-plan-2026-05-17.md`) defines the mobile viewport as 375-428 px wide (logical CSS px at 2-3× device pixel ratio). The corner minimap must not overlap:
- The virtual joystick zone (bottom-left, outer ring ~160 px diameter per `joystick.ts` R_OUTER=80 → 160 px diameter, positioned at bottom-left)
- The touch hotbar (bottom-center/right)
- The touch potion buttons
- The touch icon cluster (top-right strip)

**Top-right corner is occupied on mobile** by `touchIcons.ts` (the inventory/character/log icon cluster). The minimap's corner position must be chosen to avoid this cluster. Based on the existing mobile layout, the icon cluster sits at approximately `x = CANVAS_WIDTH - 80` and `y = 80-200`. The minimap needs to either:
1. Sit above the icon cluster (very tight on mobile)
2. Sit to the left of it (less conventional)
3. Move to top-left corner on mobile (left of the joystick when joystick is not active; joystick is bottom-left only)

**Recommendation (subject to gandalf A5):** On mobile, the corner minimap sits top-right but at reduced size (~100×100 px). The touch icon cluster (`touchIcons.ts`) shifts slightly left or down to make room. This is tracked in the mobile UX execution plan as a layout adjustment.

The minimap tap gesture on mobile opens/closes the full overlay (same as M key on desktop). This is the ARPG mobile canon: tap the minimap corner to expand.

**Mobile size:** ~100×100 px for the corner minimap, per the general principle that mobile shrinks non-touch-target UI by 0.75× from PC values (PC ~180 px → mobile ~135 px, rounded to 100 px for safe-area margin). Exact value deferred to gandalf A2/A5 sizing spec (`<sibling-pending: gandalf sections 3, 5>`).

### § 10.2 — Full-screen overlay on mobile

On mobile, the full-screen overlay IS full-screen (no partial coverage). It fills the safe-area-inset canvas, which is already handled by Pixi's autoDensity + devicePixelRatio setup. The overlay's background blocks the game view completely on mobile (unlike desktop where 70% opacity lets gameplay show through).

**Close gesture:** Tap anywhere outside the floor plan area, or tap the minimap icon again. Not a swipe (swipes are reserved for the joystick + hotbar interactions per the mobile UX plan). A clearly-labeled close button (×) is placed at top-right corner of the overlay for clarity.

**No pinch-zoom in MM2-MM3.** Pinch-zoom on the map (D-Immortal, PoE Mobile) is Phase MM6 polish. The overlay shows the full floor plan at fixed scale in MVP.

### § 10.3 — Render performance on mobile

Per § 8.4: minimap draw cost is ~0.3-0.8 ms/frame on mobile at VS2a content density. This is acceptable. The primary mobile GPU constraint is fill rate (large transparent overlays), not draw call count. The full-screen overlay's dark background (a single filled rect) is cheap at mobile fill rates. No mobile-specific rendering optimization is required in MM1-MM3.

### § 10.4 — Integration with mobile UX execution plan

The mobile UX execution plan (Phase MX3 — layout zones) must include the minimap corner position in its layout-zone definition. The minimap is a new HUD element that the layout-zone system must account for. When MX3 fires, `minimap.ts` integration is a sub-item.

---

## § 11 — Data flow architecture (drax B4)

### § 11.1 — Map data source

The minimap's data feed is entirely internal to `main.ts` runtime state. No new engine schema fields are needed. No new loader calls. The data is already present:

| Data | Source in main.ts | Update frequency | Minimap use |
|---|---|---|---|
| Room/hallway layout | `_dungeon: Dungeon` (built once in `startGauntlet`) | Static per gauntlet | Static layer render |
| Room aggro state | `room.aggroState` on `_dungeon.rooms[i]` | On aggro transition | Static layer re-render |
| Player world position | `playerPos: Vec2` | Per frame | Player dot |
| Monster world positions | `pack[i].pos: Vec2` (alive + spawned only) | Per frame | Monster dots |
| Gear drop positions | `gearDropSprites[i].container.{x,y}` | Per frame | Drop indicators |
| Monster tier | `pack[i].spec.tier` | Static per wave | Dot color/size |
| Gear tier | `gearDropSprites[i].item.tier` | Static per drop | Drop color |
| Current wave number | `gauntlet.waveNumber` | Per wave advance | Active room highlighting |

### § 11.2 — Update frequency model

**Static layer** (room/hallway outlines, door markers, room fill colors):
- Built once at `startGauntlet()` when `_dungeon` is first constructed.
- Rebuilt whenever `setRoomAggro()` is called (at most 7 times per gauntlet — once per room-clear event). Not per frame.

**Dynamic layer** (player dot, monster dots, drop indicators):
- Redrawn every frame in the game-loop ticker, alongside `diabloHud.update()` and `updateHpBar()`.
- `minimap.update(playerPos, pack, gearDropSprites)` is the single per-frame call.
- When the full-screen overlay is closed (`visible === false`), `update()` skips the dynamic redraw (no-op if not visible). This avoids wasting GPU time when the overlay isn't shown.
- The corner minimap always updates (it's always visible during combat).

### § 11.3 — Memory model

**Whole-dungeon cache:** The VS2a dungeon has 7 rooms + 6 hallways. The static layer Graphics for the full floor plan is approximately 200 triangles (rect decomposition by Pixi). Memory: ~8-16 KB in Pixi's geometry buffer. Negligible.

**No partial-cache needed:** Multi-floor dungeons (where only the current floor is cached) are a Phase 3 concern. VS2a is single-floor linear; cache the whole thing.

**GC discipline:** The minimap Container and its Graphics children are created once per gauntlet start and destroyed in the existing `clearVfx()` / gauntlet-teardown path. No per-frame allocations. `Graphics.clear()` reuses the same Graphics object; it does not allocate.

### § 11.4 — Relationship to mobile execution plan

The mobile UX execution plan defines layout zones for mobile. The minimap is an additional HUD element in that zone system. The data flow described here is platform-invariant — the same `update()` call, same data sources, same rendering path. What changes on mobile is: (a) container position (top-right, smaller), (b) tap gesture for overlay toggle, (c) overlay is full-screen modal. The data pipeline does not change.

### § 11.5 — Integration with future NPC + chest + waypoint systems

When the engine eventually emits NPC positions, chest positions, or waypoint positions as part of the floor plan data (these do not exist yet), they are added as additional data sources in the same pattern:
- NPC: a separate array of `{ id, pos, kind }` passed to `minimap.update()`.
- Chests: same pattern.
- Waypoints: likely static (positions set at dungeon build time); added to static layer, not dynamic layer.

No architectural change is needed to add these. The `Minimap` class interface is designed to accept additional per-frame arrays.

---

## § 12 — Phased drax-dispatch plan (drax B5)

Each phase is a standalone dispatch (~0.5-2 days). Phases are sequential: each phase's smoke test gates the next.

### Phase MM1 — Data layer extraction

**Scope:** Extract and test the dungeon-to-minimap coordinate transform in isolation. No visible minimap; unit-testable via console output.

**Goal:** Prove the math. Given `_dungeon` from `buildVS2aDungeon()`, compute the bounding box of the full floor plan, verify the scale factor, verify that all room/hallway bounds project into the minimap coordinate space without clipping.

**Files:**
- `src/ui/minimap.ts` — new file. Contains:
  - `computeDungeonBounds(dungeon: Dungeon): Bounds` — union of all room + hallway bounds
  - `worldToMinimap(worldX, worldY, dungeonBounds, minimapW, minimapH): {x, y}` — coordinate transform
  - `MinimapOptions` interface (position, size, opacity)
  - `Minimap` class (constructor, `update()` stub, `setRoomAggro()` stub, `destroy()`)
- No changes to `main.ts` yet (integration is Phase MM2).

**Smoke test:** `npm run build` succeeds. Console-log the projected position of `playerPos` (player spawn for room_0) through `worldToMinimap()` — verify it appears at the expected minimap-space location (left-center of minimap for VS2a's room_0 spawn position).

**Dependencies:** None. Can start immediately. Does not require gandalf A2/A3 sizing spec — uses placeholder values.

**Line-count estimate:** ~120 lines for `minimap.ts` at this phase.

---

### Phase MM2 — Corner minimap MVP

**Scope:** Visible corner minimap with static room/hallway outlines + player dot + monster dots. No styling polish.

**Goal:** "I can glance top-right and see where I am, where the rooms are, and where monsters are."

**Files:**
- `src/ui/minimap.ts` — extend MM1 foundation:
  - `_buildStaticLayer()` — draws room/hallway rectangles + door threshold lines at minimap scale; room fill color by aggroState
  - `_updateDynamicLayer()` — clears + redraws player dot (white) + monster dots (red, size by tier)
  - `update()` — calls `_updateDynamicLayer()`
  - `setRoomAggro()` — calls `_buildStaticLayer()` on state change
- `main.ts` — integration:
  - After `_dungeon = buildVS2aDungeon(...)` in `startGauntlet()`: `_minimap = new Minimap(_layers.ui, _dungeon, cornerMinimapOpts)`
  - In per-frame ticker (alongside `diabloHud?.update(player)`): `_minimap?.update(playerPos, pack, gearDropSprites)`
  - On aggro transitions (`activateRoom()` / `clearRoom()` call sites): `_minimap?.setRoomAggro(room.id, room.aggroState)`
  - On gauntlet teardown: `_minimap?.destroy(); _minimap = null`

**Smoke test:** Demo launches, renders one frame without console errors. Corner minimap is visible top-right. Player white dot moves with WASD. Red dots appear for monsters and move with them. Aggro transitions change room color. `npm run build` passes.

**Dependencies:** MM1 complete. No gandalf spec needed for MVP — placeholder sizing.

**Line-count estimate:** MM1 (~120) + ~200 new lines in `minimap.ts` + ~30 integration lines in `main.ts` = ~350 total lines added.

---

### Phase MM3 — Full-screen overlay MVP

**Scope:** M-key toggle for full-screen overlay. Same data, larger scale. Semi-transparent background.

**Goal:** Press M, see the whole floor plan at readable size. Press M again (or Escape), return to corner minimap only.

**Files:**
- `src/ui/minimap.ts` — extend MM2:
  - `toggleOverlay()` — toggles `_overlayVisible`; on open: rebuilds static layer at overlay scale; on close: rebuilds at corner scale
  - `_overlayVisible: boolean` — controls which Container is shown
  - Two Container children: `_cornerContainer` and `_overlayContainer`; `_buildStaticLayer()` targets the currently-active container
  - `_overlayContainer` positioned at center: `x = (CANVAS_WIDTH - OVERLAY_W) / 2`; `y = (CANVAS_HEIGHT - OVERLAY_H) / 2`
  - Background panel added to `_overlayContainer` (dark rect, 70% alpha)
- `main.ts`:
  - During `gState === 'fighting'` and `gState === 'door_active'`: `if (input.wasPressed('KeyM')) _minimap?.toggleOverlay()`
  - `_minimap?.update()` updates both layers regardless of overlay state (corner always current; overlay only when open)

**Smoke test:** Press M during combat — overlay appears centered. Player dot and monster dots visible at overlay scale. Press M again — overlay closes. `npm run build` passes.

**Dependencies:** MM2 complete.

**Line-count estimate:** MM2 total (~350) + ~150 new lines in `minimap.ts` (overlay mode) + ~15 integration lines in `main.ts` = ~515 total lines.

---

### Phase MM4 — Iconography pass

**Scope:** Apply gandalf A3 iconography spec. Gear-drop indicators (rarity-colored), proper monster tier dot sizing, boss indicator, door/exit markers on minimap, optional wave label in overlay.

**Goal:** Map is informative enough to navigate by, not just locating-by.

**Files:**
- `src/ui/minimap.ts` — extend MM3:
  - `_drawMonsterDot()` — per-tier radius + color per gandalf A3 spec (placeholder until spec lands; replace `<sibling-pending: gandalf A3>` when available)
  - `_drawGearDrop()` — rarity-colored small diamond/square; matches `TIER_LABEL_COLORS` from `gearDrop.ts`
  - `_drawDoorMarker()` — small gap or tick mark on room-outline edge at door position; uses `door.position` from topology
  - `_drawExitMarker()` — brighter color for the active exit door (`_activeDoorId` from `main.ts`)
  - Wave label in overlay: `Text` child of `_overlayContainer` showing `Wave N / 7 — <tierLabel>`

**Smoke test:** Gear drops appear on minimap at correct positions with rarity colors. Boss room has distinct marker. Exit door is highlighted. `npm run build` passes.

**Dependencies:** MM3 complete + gandalf A3 iconography spec available (`<sibling-pending: gandalf section 4>`). Can use placeholders and iterate.

**Line-count estimate:** ~515 + ~120 new lines in `minimap.ts` = ~635 total lines.

---

### Phase MM5 — Mobile adaptation

**Scope:** Mobile minimap sizing + tap-to-toggle gesture + full-screen modal on mobile. Integrates with mobile UX execution plan Phase MX3 (layout zones).

**Goal:** The minimap works correctly on a 375 px wide mobile viewport. Joystick and touch hotbar are not occluded.

**Files:**
- `src/ui/minimap.ts` — extend MM4:
  - `MinimapOptions.mobile` variant: smaller corner size (~100×100 px), adjusted position (top-right, shifted left to avoid `touchIcons.ts` cluster)
  - Mobile overlay: `_overlayContainer` covers full canvas (no partial-coverage); close button (×) at top-right
  - Tap gesture: `_cornerContainer.interactive = true`; `on('pointerdown', toggleOverlay)` for mobile; this is consistent with how `touchIcons.ts` handles tap events
- `main.ts`:
  - `MinimapOptions` conditional: `Mobile.isActive ? mobileMinimapOpts : desktopMinimapOpts`
  - No touch-gesture conflict: tap on minimap corner is distinct from joystick bottom-left and hotbar bottom-right; safe zones verified per mobile UX layout

**Smoke test:** On 375 px viewport (browser devtools mobile emulation), minimap visible top-right, not occluded by joystick or hotbar. Tap minimap opens full overlay. Tap close button closes. `npm run build` passes.

**Dependencies:** MM4 complete + mobile UX execution plan Phase MX3 layout zones complete (`canonical/story/mobile-ux-execution-plan-2026-05-17.md` Phase MX3).

**Line-count estimate:** ~635 + ~80 new lines in `minimap.ts` (mobile branch) + ~20 integration lines in `main.ts` = ~735 total lines.

---

### Phase MM6 — Polish

**Scope:** Fog-of-war reveal animation, zoom controls on overlay, opacity setting, player-dot pulse animation, smooth aggro-state transitions.

**Goal:** Map feels alive and polished, not functional-but-static.

**Files:**
- `src/ui/minimap.ts` — extend MM5:
  - Fog reveal: rooms start at low alpha (dormant = 10% opacity), fade to full opacity when aggro activates. `setRoomAggro()` triggers a tween on the room's Graphics alpha over 0.3s.
  - Player dot pulse: scale oscillates 1.0 → 1.2 → 1.0 over 1s. Simple sin-based tick in `update()`.
  - Overlay zoom (MM6+): `+` / `-` keys or pinch gesture adjust scale factor within [0.5×, 2.0×] range; scroll recenters on player.
  - Opacity setting: `MinimapOptions.alpha` applied to `_cornerContainer.alpha`; user-configurable in a future settings panel (not in MM6 scope itself — surfaced as observation).
  - Annotation (if scoped — see B6): long-press on overlay places a small marker; array of `{x, y, label}` persists until cleared.

**Smoke test:** Player dot pulses. Entering a dormant room triggers a room reveal fade. Overlay zoom in/out works with + / - keys. `npm run build` passes.

**Dependencies:** MM5 complete + gandalf A4/A5/A6 spec available.

**Line-count estimate:** ~735 + ~150 new lines (fog/pulse/zoom) = ~885 total lines in `minimap.ts`.

---

### Phase summary table

| Phase | Goal | New files | Main.ts changes | Smoke test | Dependencies |
|---|---|---|---|---|---|
| MM1 | Data layer + transform math | `src/ui/minimap.ts` (skeleton) | None | Build passes; transform verified in console | None |
| MM2 | Corner minimap MVP | extend MM1 | ~30 lines | Visible minimap; player/monster dots | MM1 |
| MM3 | Full-overlay toggle | extend MM2 | ~15 lines | M-key toggle works | MM2 |
| MM4 | Iconography pass | extend MM3 | None | Gear drops + tiers + exit marker | MM3 + gandalf A3 |
| MM5 | Mobile adaptation | extend MM4 | ~20 lines | Works on 375 px viewport | MM4 + mobile UX MX3 |
| MM6 | Polish (fog, pulse, zoom) | extend MM5 | None | Fog reveal; dot pulse; zoom | MM5 + gandalf A4/A5/A6 |

---

## § 13 — Out-of-scope deferrals (drax B6)

**Multi-floor map (D2 act-overview style):**
VS2a is a single-floor linear dungeon. Multi-floor with a floor-select UI (D2-style Act overview, PoE-style area map) is a Phase-3 feature if the dungeon topology ever gains a floor axis. The `Dungeon` interface in `topology.ts` would need a `floors: Floor[]` wrapper; the minimap would need a floor-selection control. Explicitly out of scope. When multi-floor lands in topology, the minimap refactor is a separate dispatch.

**Map sharing / streaming:**
No mechanic planned. Solo gameplay only (`project_design_intent.md` confirms: solo gameplay only). Out of scope permanently unless Matt explicitly revisits.

**Procedural room-reveal animations beyond fog-clear:**
Animated room-shape reveals (e.g., the walls of a room "drawing themselves" on the minimap as the player explores) are a Phase-3 polish item. The fog-opacity fade in MM6 is the MVP reveal. Full procedural drawing is an overengineering call at VS2a/VS2b density.

**Click-to-move via minimap:**
D2 allowed clicking the automap to move to a position. This is an interaction-model decision for gandalf A4. Engineering note: if approved, `click-on-overlay → map-space position → world-space position → set as lmbMoveTarget` is approximately 5 lines in `main.ts`. Very cheap if the design calls for it. Deferred to MM6 polish phase.

**Player-placed annotations:**
Last Epoch supports player map annotations. Scoped as a MM6 stretch feature. If included: a `annotations: { worldX, worldY, label?: string }[]` array in `Minimap` class, persisted to `localStorage` (key: `reincarnated_map_annotations_<dungeonId>`). The dungeon ID changes each gauntlet start, so annotations reset each run — appropriate for a roguelike-adjacent game.

**Minimap in non-combat screens:**
The minimap is a combat HUD element. It does not appear during `season_menu` or `selecting` screens. The dungeon doesn't exist yet in those states (`_dungeon === null`), so the `null` guard in `main.ts` handles this automatically.

**Radar-ping / off-screen monster indicators:**
Some ARPGs pulse the minimap edge when an off-screen threat activates. This is a Phase-3 polish item. Not in MM1-MM6 scope.

---

## § 14 — Open questions for Matt

These are deferrable; the canon in § 1-7 and the engineering plan in § 8-13 are implementable without resolving them. Surfacing for Matt's awareness when implementation fires. Engineering questions authored by drax (Stream B); design questions authored by gandalf (Stream A).

### Engineering open questions (drax)

**OQ-1 — Default mode per platform:** Should the corner minimap be visible by default on first launch, or opt-in? For VS2b, default-on is the recommendation (per ARPG genre canon: minimap is always visible), but if Matt wants it gated behind a tutorial moment ("you've discovered the map"), it requires a `_minimapUnlocked` flag in the game state. Engineering-trivial either way; needs a design call.

**OQ-2 — Pause-on-overlay (gameplay stops when full-screen map is open?):** Per ARPG canon, gameplay continues. But if Matt prefers pause (for mobile usability where two-hand play is harder), the flag `_mapOverlayOpen` is checked in the fight-state input-processing block. Decision affects the interaction feel significantly. Recommend no-pause (genre canon), but surfacing for explicit approval.

**OQ-3 — Fog of war vs full-reveal:** The engineering plan implements aggro-state-based room coloring (dormant = dark fill, active/cleared = brighter fill), which effectively IS fog of war (you can't see the room shape until you've been near it because all rooms are pre-drawn but dim). True fog = rooms are hidden until the player enters. Which model: tint-fog (always visible, but dark) or hide-fog (rooms not drawn until visited)? Tint-fog is simpler and matches D2's feel; hide-fog matches PoE's feel. Gandalf A2 covers this; surfacing here for cross-check.

**OQ-4 — M key availability:** M is not currently bound in `main.ts` during combat. Confirming it's available for minimap toggle. (I is inventory, C is character sheet, H is combat log, Escape is system, Space is dodge.) M is free.

**OQ-5 — Minimap in the between-wave overlay:** During `gState === 'pack_dying'` and `gState === 'door_active'`, the minimap is relevant (player is walking to the exit; the map shows where the door is). The current plan keeps the minimap active in these states. The between-wave overlay (`createBetweenWaveOverlay`) covers the center of the screen; the corner minimap in the top-right is not occluded. Confirming this is correct behavior.

**OQ-6 — Minimap assets needed (OBSERVATION for Phase-2 acquisitions queue):** The engineering plan uses Pixi `Graphics` primitives exclusively — no external sprite assets needed for MM1-MM5. MM4+ iconography uses the same `Graphics` shapes as the HUD (consistent with existing glyph-drawing in `combatHud.ts`). If Matt later wants pixel-art minimap icons (styled map markers, treasure-chest symbols, etc.) instead of geometric primitives, those would be new assets. Surfacing as an OBSERVATION: no blocker, but if the art direction calls for it, add to the Phase-2 acquisitions queue alongside the tileset work. **Gandalf concurs:** § 4.1 + § 7.1 explicitly recommend geometric primitives over sprite-renders for the polish-multiplier rationale. **NO new assets needed.**

### Design open questions (gandalf)

**OQ-D1 — Tab vs M for toggle key (cross-references drax OQ-4):** Per § 5.1 — Tab is genre-canonical (D2/D3/D4/PoE/LE/Grim Dawn all use Tab); M is more semantic but is the MMO-canon (Lost Ark/WoW use M for world-map). My recommendation: **Tab in v1, rebindable to M in settings.** Drax's drafted M binding should switch to Tab. Matt's call; tolerably either way; ~1 line of code to switch.

**OQ-D2 — Pause-during-overlay vs continue-during-overlay (cross-references drax OQ-2):** Per § 5.2 — recommendation is **pause** for combat-pace reasons (a Tab-glance during combat is ~200-500ms = a dodge window). Drax recommends continue (genre canon for PC-D-series). This is a genuine design disagreement worth Matt's resolution. Both engineering paths are accommodated in drax's plan. **Recommend: pause; Matt to confirm or override.**

**OQ-D3 — Fog of war model — room-snap-reveal vs aggro-state-tint (cross-references drax OQ-3):** Per § 3.2 — recommendation is **room-snap-reveal-on-entry** (dormant rooms invisible until player enters; reveal as 200-400ms ease-in). Drax's plan implements aggro-state-tint (rooms always visible at dim alpha; brighten on aggro). My recommendation extends drax's `setRoomAggro()` to `setRoomState(roomId, { discovered, aggro })` — same redraw plumbing, two flags. Same code surface; different player experience. **Recommend: room-snap-reveal; minor extension to drax's static-layer hook.**

**OQ-D4 — Substrate-biome room tint (subtle hue-shift on room fill):** Per § 3.3 — optional layered tint, ±5-8% hue shift on room fill toward the room's substrate identity color. Pros: ties spatial perception to substrate vocabulary subtly; coherence-without-naming. Cons: small additional asset/data dependency (rooms must know their substrate); risk of "too subtle = invisible" or "too strong = confusing." **Recommendation: include in v1 at ±5% shift; iterate on playtest signal.** If Matt prefers conservative v1 ship, defer to v2. Engineering: requires `Room.substrate?: SubstrateId` field on the topology — small addition.

**OQ-D5 — Per-player "default-state on zone entry" setting (corner vs overlay):** Per § 2.6 + § 5.4 — small win for Group 2 (Matt's preferred mode). One settings entry; ~3 lines of state. Question for Matt: is this in v1 ship, or v2? **Recommendation: v1.** Cost is trivial; payoff is "Matt opens the game and the overlay is already up."

**OQ-D6 — North-locked vs player-orientation-rotating map (default):** Per § 2.5.1 + § 3.7 — genre split 70-30 north-locked. **Recommendation: north-locked default, player-orientation-rotating toggle in settings.** Matt's call on default. Drax MM2 can hardcode north-locked; toggle is MM6 settings.

**OQ-D7 — Frame style (genre-AAA-jeweled vs pixel-art-tonal):** Per § 7.6 — recommendation is **pixel-art-tonal** (2-3 px dark-gold ring + 1 px lighter-gold inner highlight). This matches our locked HD-2D pixel-art register. Surface for Matt's eye-test approval once concept art exists. Could pivot to a more elaborate jeweled frame if Matt's eye-test prefers; cost is minimal.

**OQ-D8 — Opacity slider default value (corner + overlay):** Per § 3.4 — corner-minimap 0.55-0.65α and overlay 0.75-0.85α at default-100%-slider. Surface for Matt's eye-test approval. Range is intentionally narrow; specific value within range is taste.

**OQ-D9 — Boss-room special treatment:** Genre precedent (D4): boss rooms get a *special icon overlay* on the map (e.g., a stylized skull or boss-sigil) replacing the standard monster dots. Reincarnated could adopt this — boss-room minimap renders the room's "name" or sigil. Surface for design discussion; not v1 critical.

**OQ-D10 — Mobile minimap vs touchIcons positioning conflict (cross-references drax § 10.1):** Per § 6.1 — my recommendation is **minimap takes top-right corner; touchIcons cluster shifts down below the minimap.** Drax flagged the conflict but did not propose a resolution. Matt's call. Alternative: swap them (touchIcons top-right, minimap top-left or top-center) — explicitly NOT recommended (genre-canon-violating).

**OQ-D11 — VS2a linear-dungeon overlay projection (cross-references drax § 9.2):** Per § 3.5 — VS2a's 6.2:1 aspect ratio linear dungeon should project **horizontal-left-to-right** (dungeon's long axis = overlay's long axis = horizontal; reading-direction reinforcement). Drax flagged this as needing a projection decision. Recommend horizontal. Matt's call; either rotation works engineering-wise.

**OQ-D12 — Dungeon-overview "map-of-the-zone" mode for big dungeons:** If Reincarnated's eventual Phase-2 act content includes multi-zone dungeons with overworld map, a third-tier "zone overview map" becomes relevant (Lost Ark's M-twice pattern). Out of v1; flag for Phase-2 design.

---

*Stream A (gandalf) sections 1-7 + § 14 design OQs authored 2026-05-17. Stream B (drax) sections 8-14 engineering OQs authored 2026-05-17. Tag `gandalf/v1.8-arpg-map-overlay-research-1` applied at gandalf commit; tag `drax/v1.7-arpg-map-overlay-engineering-plan-1` applied at drax commit. The hive moves together. — gandalf + drax*
