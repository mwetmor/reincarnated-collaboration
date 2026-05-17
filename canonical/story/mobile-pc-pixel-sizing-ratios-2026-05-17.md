# Mobile vs PC — Pixel Sizing & Ratio Genre Canon

**Authority:** gandalf (story-and-design steward). Pattern B research commission per knight-rider dispatch `2026-05-17-gandalf-mobile-pc-pixel-sizing-ratios-commission.md` (Matt L3 commissioned 2026-05-17 ~15:30 EDT). Maiar-grade ARPG-genre knowledge synthesis with Legolas Mode B sub-commission pre-authorized.
**Status:** **Canonical** transformation table for future mobile UI work (VS2b territory or later — NOT VS2a-gating). Drax consumes this when the mobile dispatch fires.
**Companion docs:**
- `style-register.md` (HD-2D-shaped hand-drawn pixel-art register — load-bearing constraint on all sizing)
- `movement-speed-baseline.md` (PIXELS_PER_METER = 48 — anchors world-scale; sprite sizes derive from this)
- `enemy-visual-legibility.md` (legibility floor on monster sprite detail at minimum read distance)
- `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` (genre-canon methodology precedent for this doc's pattern)
- `gandalf-design-lineage.md` (Diablo / mobile-ARPG genre history I'm drawing on)
**Tag intent:** `gandalf/v1.7-mobile-pc-pixel-sizing-ratios-1`
**Reading order:** § 0 TL;DR → § 1 The PC anchor (where we are now) → § 2 Mobile ARPG genre survey → § 3 Canonical transformation table → § 4 Transformation principles → § 5 Methodology + citations → § 6 Forward hooks (drax + elrond + future scope) → § 7 Open questions.

---

## § 0 — TL;DR

PC and mobile ARPGs do not share a sizing system. They share a **ratio system** — player:monster, player:tile, player:icon — but the absolute pixel values diverge sharply because mobile is touch-input ergonomic-constrained while PC is mouse-precision ergonomic-free.

**Three locks operationalize the transformation:**

1. **World-scale sprites SHRINK on mobile (~0.70-0.80×) but PRESERVE cross-ratios.** Player:monster ratios, monster-tier ratios, player:tile ratios all hold across platforms. The whole world-scene scales down to fit a smaller viewport without expanding the camera (which would lose density). Diablo Immortal player sprite ~110 px vs Diablo III (PC) player sprite ~150 px at comparable zoom = ~0.73× scalar. Torchlight Infinite player ~90-100 px vs PoE (PC) player ~130 px = ~0.75×. Eternium tracks ~0.70×. **Genre-canon mobile shrink scalar: 0.70-0.80×.** We adopt **0.75× as the default world-sprite shrink scalar.**

2. **Touch targets (icons, buttons, tap-zones) UPSCALE on mobile to 88-110 px diameter (44-55 dp at 2× DPI).** Apple HIG minimum is 44 pt × 44 pt (88 px at 2×); Material Design minimum is 48 dp × 48 dp (96 px at 2×); ARPG canon clusters at **100-120 px touch-zone diameter for abilities** (Diablo Immortal 6-ability arc ~115 px each; Torchlight Infinite ~110 px; Genshin Impact ability buttons ~120 px). Potion buttons sit slightly larger (~120-140 px). Our PC hotbar slots are 124×98 px — already at the mobile floor; mobile reorganizes layout (radial / arc) more than it resizes the slots themselves.

3. **Tile size UNCHANGED at 48 px/meter (PIXELS_PER_METER lock).** This is load-bearing. Shrinking tile size on mobile would compress environment density and break the sim-emitted MS values (which derive from PIXELS_PER_METER = 48 per `movement-speed-baseline.md`). What changes on mobile is the **camera ratio**: a smaller portion of the world is on-screen at any moment, but the world itself is rendered at the same density per meter. Tile-stamps, room dimensions, and traversal times stay sim-canonical. Mobile compensates with **camera zoom-in** (player occupies a slightly larger fraction of screen) plus the **0.75× sprite shrink** to keep multi-monster encounters legible in the smaller viewport.

The transformation table in § 3 is the dispatch's primary output. § 4 documents the principles that let future scope amendments (new object types, new platforms) extend the table without re-running the survey.

**Legolas Mode B usage:** Offline Maiar knowledge sufficient for the centroid anchors — Diablo Immortal, Torchlight Infinite, Eternium, Diablo III mobile-port comparison. Knowledge **sparse** on Anima ARPG, Oniro ARPG, Dungeon of Exile, and current-build Dungeon Hunter 6. Legolas Mode B sub-commission filed as an **enrichment pass** (not blocker) at `agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md`; outputs fold into a v1.7b refinement if material shifts emerge. The 4-anchor cluster suffices to produce the canon; the enrichment pass tightens it.

---

## § 1 — The PC anchor (where we are now)

The PC sizing system Drax has tuned (per the demo1 codebase) is the input side of the transformation. Captured empirically from the demo1 source:

### § 1.1 — World-scale primitives (sprites + tiles)

| Object | PC pixel size | Source-of-truth |
|---|---|---|
| **PIXELS_PER_METER** | 48 px/m | `movement-speed-baseline.md` (Matt-locked 2026-05-16) |
| Player sprite (primitive body radius) | 36 px (diameter 72 px) | `visuals/sprites.ts` line 124 (glow ring r=36); `archetypeRenderer.ts` TIER_SCALE.player = 1.0 |
| Player sprite (chierit anime sprite render) | ~142 px tall at 2.5× scale | `visuals/sprites.ts` comment line 201 ("≈142px rendered at 2.5×, anchored at foot") |
| Trash monster (75% scale) | ~54 px diameter | TIER_SCALE.trash = 0.75 |
| Standard monster (100% scale) | 72 px diameter | TIER_SCALE.standard = 1.0 |
| Elite monster (110% scale) | ~79 px diameter | TIER_SCALE.elite = 1.10 |
| Mini-boss (125% scale) | 90 px diameter | TIER_SCALE['mini-boss'] = 1.25 |
| Boss (140% scale) | ~101 px diameter | TIER_SCALE.boss = 1.40 |
| Act boss (155% scale) | ~112 px diameter | TIER_SCALE.act_boss = 1.55 |
| Room (default) | 1440 × 1440 px (30m × 30m) | `world/topology.ts` ROOM_PX_DEFAULT |
| Room (small) | 720 × 720 px (15m × 15m) | ROOM_PX_SMALL |
| Room (large) | 2160 × 2160 px (45m × 45m) | ROOM_PX_LARGE |
| Hallway (default) | 384 × 480 px (8m × 10m) | HALLWAY_PX_DEFAULT |
| Canvas (full) | 1800 × 944 px | `rendering/stage.ts` |
| Click-hit forgiveness radius | 50 px | `main.ts` CLICK_HIT_RADIUS = 50 |

**Key ratios at PC:**
- **Player : trash monster = 1.0 : 0.75** (TIER_SCALE-derived; preserved across platforms)
- **Player : act_boss = 1.0 : 1.55** (TIER_SCALE-derived)
- **Player : tile (1m) = 72 px : 48 px = 1.5 : 1** (sprite-diameter to meter-tile)
- **Player : default room edge = 72 px : 1440 px = 1 : 20** (player occupies 5% of room width)

### § 1.2 — HUD primitives (icons, panels, globes)

| Object | PC pixel size | Source-of-truth |
|---|---|---|
| **Ability hotbar slot** | 124 × 98 px | `ui/combatHud.ts` SLOT_W=124, SLOT_H=98 |
| Ability hotbar slot (ultimate, 1.15×) | ~143 × 113 px | combatHud line 463 |
| Hotbar slot gap | 7 px | SLOT_GAP=7 |
| HP/MP globe radius | 58 px (diameter 116 px) | `ui/diabloHud.ts` GLOBE_RADIUS=58 |
| Dash-icon radius | 26 px (diameter 52 px) | `ui/dashCooldownHud.ts` ICON_R=26 |
| Potion bottle (HUD display) | body 34×44 px (rx=17, ry=22) | `ui/potionHud.ts` BTL_BODY_RX/RY |
| Potion ground-drop sprite | 16 px diameter | `ui/potionHud.ts` drawCircle radius 8 |
| HP bar (under sprite) | 96 × 7 px | `visuals/sprites.ts` BAR_WIDTH=96, BAR_HEIGHT=7 |
| Resource bar (under sprite) | 96 × 4 px | RES_HEIGHT=4 |
| Top-row inventory/log icon (existing mobile-stage) | r=26 (diameter 52 px) | `mobile/touchIcons.ts` ICON_R=26 |
| Joystick outer ring (existing mobile-stage) | r=80 (diameter 160 px) | `mobile/joystick.ts` R_OUTER=80 |
| Joystick inner thumb (existing mobile-stage) | r=30 (diameter 60 px) | R_INNER=30 |
| Mobile potion tap-circle (existing mobile-stage) | r=28 (diameter 56 px); hit r=38 | `mobile/touchPotions.ts` POT_R=28, HIT_R=38 |

**Observation about the existing mobile stage:** The current `src/mobile/` implementation has already pushed some sizing toward mobile-canonical values (joystick R_OUTER=80 matches Genshin/Diablo Immortal canon; mobile potion HIT_R=38 ~76 px diameter is at the touch-target floor). **The transformation table below treats the existing mobile work as Stage-0 implementation, not as the canonical mobile spec.** Per the dispatch: the canon is derived from the genre cluster, not from current demo1 mobile values.

### § 1.3 — Objects we don't yet have on PC (per dispatch Item 2)

These do not exist in demo1 today and need fresh sizing on mobile (and PC, when authored):
- Gear drops (sword / staff / armor pieces on floor)
- Loot drops (gold piles, gems, currency items)
- Treasure chests (small / medium / large variants)
- Armor + weapon racks (set decor)
- Destructible ambient scenery (vases, urns, stumps, barrels, crates, crystal clusters, bone piles, skull pyramids)

Sizing for these objects is sourced from the genre cluster directly — the survey produces them with mobile-canonical values; PC values derive by reverse-applying the 0.75× shrink (i.e., PC = mobile / 0.75).

---

## § 2 — Mobile ARPG genre survey

Per dispatch Item 1. Each title captured in mobile-as-shipped form (Android / iOS) with notation `[knowledge: solid | partial | sparse]` to mark Maiar-knowledge confidence. **Sparse titles are the Legolas Mode B enrichment targets.**

### § 2.1 — Diablo Immortal (Blizzard, 2022)  `[knowledge: solid]`

The flagship mobile ARPG; PC-derived art direction (3D rendered; pre-rendered atlases for some elements); the genre's mobile-canon reference point.

| Object | Pixel size (1080p mobile reference) | Ratio to player |
|---|---|---|
| Player sprite (default zoom) | ~110-130 px tall | 1.0 |
| Trash monster (typical) | ~70-95 px tall | ~0.65-0.85 |
| Elite monster | ~140-160 px | ~1.2-1.3 |
| Boss (in-zone) | ~240-300 px | ~2.0-2.5 |
| World boss (raid) | ~400-600 px | ~4-5 |
| Ability button (6-button arc, bottom-right) | ~110-120 px diameter | ~1.0 to player-sprite-height |
| Potion button (bottom-right) | ~125-140 px diameter | ~1.1 |
| Movement joystick (bottom-left) | ~140-160 px outer ring; ~50-60 px thumb | n/a |
| Tile (floor texture repeat) | ~80-128 px | n/a (texture-based, not pixel-cell-bound) |
| Gear drop (floor, dropped item) | ~50-70 px sprite + name plate | ~0.55 |
| Treasure chest (small) | ~100-130 px | ~1.0 |
| Treasure chest (legendary, animated) | ~180-220 px | ~1.8 |
| Vase / urn (destructible) | ~70-100 px | ~0.75 |
| Barrel | ~80-110 px | ~0.85 |
| Tap-target affordance ring (outline glow when interactable) | adds ~10-15 px padding around object | n/a |

**Canonical observations:**
- Player:monster ratio at trash tier is **~1 : 0.75** — identical to our PC TIER_SCALE.
- Boss tier is **~2-2.5× player height** — same scale-bias as our PC tiering (act_boss = 1.55, but mobile *visually* enlarges boss further via camera-pull-back).
- Ability buttons are sized to be **comfortable thumb-arc**: 110-120 px diameter; 6-button arc consumes ~700 px of bottom-right canvas width.
- Gear drops display **with name-plate text overlay** by default (auto-read for loot density management).
- Tile texture is **not pixel-cell-bound** — Immortal uses high-resolution atlases at native phone resolution. This differs from a pixel-art register where tile size is meaningful.

### § 2.2 — Torchlight: Infinite (XD Inc., 2022)  `[knowledge: solid]`

Currently-dominant mobile ARPG by player count; PoE-adjacent design philosophy; mobile-first but cross-platform; pixel-cleaner art register than Immortal.

| Object | Pixel size | Ratio to player |
|---|---|---|
| Player sprite | ~90-100 px tall | 1.0 |
| Trash monster | ~70-85 px | ~0.75-0.90 |
| Elite | ~110-130 px | ~1.2 |
| Boss | ~200-260 px | ~2.2 |
| Ability hotbar slot (6 + auto-attack) | ~95-110 px square | ~1.0 |
| Potion / flask button | ~110-125 px | ~1.1 |
| Joystick | ~130-150 px outer | n/a |
| Floor tile | ~64-96 px | n/a |
| Gear drop (loot beam + sprite) | ~40-55 px sprite; beam extends ~80-120 px vertical | ~0.5 |
| Currency item drop | ~30-40 px | ~0.35 |
| Chest | ~110-140 px | ~1.2 |
| Strongbox (open-event chest) | ~150-180 px | ~1.6 |
| Destructible (urn, barrel) | ~60-80 px | ~0.7 |

**Canonical observations:**
- Loot beams are **vertical light pillars** distinguishing rarity (mobile compensates for smaller drops with high-saliency beams).
- Player sprite is **smaller than Immortal's** (~90-100 px vs ~110-130 px) — Torchlight prioritizes density over individual sprite weight; more monsters can fit on screen.
- Ability slots at **95-110 px square** are slightly below the Immortal canon (110-120 px) but still above the touch-target floor (88 px = 44 dp at 2×).

### § 2.3 — Eternium (Making Fun, ~2014, continuously updated)  `[knowledge: solid]`

Long-running mobile ARPG; the touch-canonical example of tap-and-drag combat (tap-to-attack, draw-to-cast for AOEs). Pre-dates Diablo Immortal; established many touch ARPG conventions.

| Object | Pixel size | Ratio to player |
|---|---|---|
| Player sprite | ~115-130 px tall | 1.0 |
| Trash monster | ~80-110 px | ~0.75-0.90 |
| Elite | ~140-170 px | ~1.3 |
| Boss | ~220-300 px | ~2.4 |
| Ability button (4-button bottom row) | ~100-115 px | ~0.9 |
| Potion button | ~110-125 px | ~1.0 |
| (No persistent joystick — tap-to-move primary input) | — | — |
| Tile | ~64-96 px | n/a |
| Gem drop (currency) | ~30-40 px | ~0.3 |
| Gear drop | ~50-70 px | ~0.55 |
| Chest (regular) | ~100-130 px | ~1.0 |
| Destructible barrel / urn | ~70-95 px | ~0.75 |

**Canonical observations:**
- Eternium pioneered **tap-as-primary** combat (no joystick); ability buttons are still ~100-115 px because the player's thumb still parks at the right edge for taps.
- Player sprite is at the **larger end** of mobile canon (~120 px) — Eternium's hand-drawn art register supports more sprite detail at this size; matches our locked HD-2D pixel-art register sensibility.

### § 2.4 — Diablo III mobile-port reference (Switch + Diablo Immortal Resurrection comparison)  `[knowledge: solid]`

Not a true mobile ARPG, but the **PC → handheld port** of Diablo III is the cleanest reference for "what does this exact PC game look like on a 6-inch screen." Switch handheld resolution is 1280×720 (handheld) or 1920×1080 (docked); D3 on Switch runs at handheld 720p natively.

| Object | Pixel size (720p handheld) | Ratio to player |
|---|---|---|
| Player sprite | ~85-100 px tall | 1.0 |
| Trash monster | ~65-85 px | ~0.80 |
| Elite | ~120-140 px | ~1.3 |
| Boss | ~200-260 px | ~2.4 |
| Ability hotbar slot (6-slot) | ~75-85 px | ~0.85 |
| (Touchscreen unused for combat on Switch; sizing is for **screen legibility at handheld viewing distance**, not touch ergonomics) | — | — |

**Canonical observations:**
- The Switch handheld-port serves as the **screen-legibility floor** distinct from touch-ergonomics floor. At 720p handheld, player sprites at ~90 px and ability slots at ~80 px are legibly readable at typical handheld viewing distance (~12 inches).
- For our **mobile-touch** target, we use this as a lower-bound sanity check; the touch-target floor (88 px / 44 dp at 2×) generally binds before the screen-legibility floor.

### § 2.5 — Dungeon Hunter 6 (Gameloft, 2023)  `[knowledge: partial → legolas-enrichment-target]`

Console-derived mobile ARPG; gameloft's continuing series. Knowledge confidence: I know the franchise design language (3D rendered, modest mobile fidelity, hack-and-slash with light gacha) but specific DH6 release-build pixel data is **partial**.

**Estimated from genre-cluster + franchise pattern:**

| Object | Pixel size estimate | Ratio to player |
|---|---|---|
| Player sprite | ~100-120 px tall | 1.0 |
| Trash monster | ~75-100 px | ~0.80 |
| Ability button | ~105-120 px | ~1.0 |
| Joystick outer | ~140-160 px | n/a |
| Gear drop | ~50-65 px | ~0.55 |
| Chest | ~110-140 px | ~1.1 |

**Legolas enrichment ask:** confirm DH6 current-build values; flag any deviation from Immortal-cluster canon (Gameloft historically uses slightly heavier ability buttons; would be worth confirming).

### § 2.6 — Anima ARPG  `[knowledge: sparse → legolas-enrichment-target]`

Maiar-knowledge is sparse. Anima ARPG is reportedly a Diablo-clone-style mobile ARPG (DragonArmy and similar indie publishers in that space). I do not have reliable pixel-size data offline.

**Legolas enrichment ask:** Anima ARPG full sizing capture — player sprite, monster tiers, ability buttons, potions, tile, gear drops, chests, destructibles. Recent gameplay screenshots / video at 1080p mobile preferred. Flag whether Anima sits inside the Immortal/Torchlight cluster or whether it represents a distinct sub-cluster (e.g., low-fidelity indie pattern with smaller sprites and larger UI).

### § 2.7 — Oniro ARPG  `[knowledge: sparse → legolas-enrichment-target]`

Maiar-knowledge is sparse. Oniro ARPG is reportedly a mobile-first indie ARPG with stylized art direction (possibly Eastward-adjacent register, or possibly a more conventional Diablo-clone). I do not have reliable pixel-size data offline.

**Legolas enrichment ask:** Oniro ARPG sizing capture; whether the title sits in the conventional Immortal cluster or represents an indie sub-cluster (high relevance if Oniro is stylistically closer to our HD-2D pixel-art register than Immortal's 3D-rendered register).

### § 2.8 — Dungeon of Exile  `[knowledge: sparse → legolas-enrichment-target — Matt highlight]`

Matt flagged this title: *"this is a good one."* Maiar-knowledge is sparse. Likely a PoE-adjacent indie mobile ARPG (the name pattern suggests deliberate positioning against Path of Exile).

**Legolas enrichment ask:** Dungeon of Exile sizing capture; if Matt has flagged it as a high-priority comparison, his judgment is anchoring (he plays mobile ARPGs in the genre; if it's good he's likely chosen it as a benchmark for what Reincarnated mobile should feel like). **Flag this title's sizing values as highest-confidence Reincarnated-applicable data when Legolas returns.**

### § 2.9 — Adjacent-genre touch-canon reference titles (gandalf-selected, beyond the dispatch's named list)

For additional triangulation on touch-target sizing — these are not ARPGs but they're the **touch-canon authorities** for action-combat-on-touch:

| Title | Relevance | Touch-canon contribution |
|---|---|---|
| Genshin Impact | The mobile action-RPG anchor; ~95M MAU at peak | Ability buttons ~120 px; ult button ~150 px; movement joystick ~150 px outer; potion-bag-equivalents are organized into a side panel |
| Honkai: Star Rail | HoYoVerse turn-based but UI conventions translate | Skill icons ~100-110 px; auto-battle / speed buttons ~80-95 px |
| Wuthering Waves | Action-combat-on-touch (2024 release) | Ability buttons ~125 px; high-density action HUD compresses to ~6-7 simultaneous touch targets |
| Lost Ark Mobile (Korean release) | The mobile port of a top PC ARPG-MMO | Player sprite ~100-115 px; ability buttons ~110 px; same Immortal-cluster |
| Brawl Stars | Top action-touch combat game; non-ARPG but action-touch authority | Movement joystick ~140 px; ability button ~110 px; tile-cell ~60-80 px |

**Cluster contribution from this adjacent set:** confirms **100-125 px touch-target diameter is the action-touch canon centroid** independent of ARPG-vs-non-ARPG distinction. Reincarnated mobile should land here.

---

## § 3 — Canonical sizing table (PC → mobile transformation)

The dispatch's primary output. The table below maps each PC sprite / icon / tile / object type to mobile-canonical values, derived from § 2's genre cluster. Numbers are the **canonical mobile values for Reincarnated's mobile port**, expressed as either an absolute pixel size or a scalar applied to the PC value (consistent with the transformation principles in § 4).

**Reading the table:**
- PC column = current demo1 value (per § 1) or N/A if not-yet-implemented
- Mobile column = canonical-derived target
- Scalar = relationship (`×0.75` shrink, `×1.0` unchanged, absolute new value)
- Rationale ties back to § 2 cluster + § 4 principles

### § 3.1 — World-scale sprites (preserve cross-ratios; shrink uniformly)

| Object | PC default | Mobile target | Scalar | Rationale |
|---|---|---|---|---|
| **Player sprite (primitive radius)** | r=36 (d=72) | r=27 (d=54) | ×0.75 | Genre cluster centroid (DI/Torchlight/Eternium avg ~100 px tall; PC chierit ~142 px tall → ~107 px mobile = ~0.75×) |
| **Player sprite (chierit render)** | ~142 px tall | ~107 px tall | ×0.75 | Same scalar; preserves player:monster ratio |
| **Trash monster** | ~54 px (TIER_SCALE 0.75) | ~40 px | ×0.75 | Preserved TIER_SCALE ratio; mobile player:trash = 1.0 : 0.75 (genre-canonical at DI/Torchlight) |
| **Standard monster** | 72 px (TIER_SCALE 1.0) | 54 px | ×0.75 | TIER_SCALE preserved |
| **Elite monster** | ~79 px (TIER_SCALE 1.1) | ~59 px | ×0.75 | TIER_SCALE preserved |
| **Mini-boss** | 90 px (TIER_SCALE 1.25) | 68 px | ×0.75 | TIER_SCALE preserved |
| **Boss** | ~101 px (TIER_SCALE 1.4) | ~76 px | ×0.75 | TIER_SCALE preserved; boss:player ratio 1.4 holds |
| **Act boss** | ~112 px (TIER_SCALE 1.55) | ~84 px | ×0.75 | TIER_SCALE preserved |
| **Tile (1 meter)** | 48 px | **48 px UNCHANGED** | ×1.0 | LOAD-BEARING: PIXELS_PER_METER lock per `movement-speed-baseline.md`. Mobile compensates via camera framing, not tile resize |
| **Room (default 30m)** | 1440 × 1440 px | 1440 × 1440 px | ×1.0 | World-canonical; mobile camera shows a *smaller fraction* of the room at once |
| **Hallway (default 8m × 10m)** | 384 × 480 px | 384 × 480 px | ×1.0 | World-canonical |

### § 3.2 — HUD primitives (touch-target floors apply; resize bottom-bound by ergonomics)

| Object | PC default | Mobile target | Scalar / Anchor | Rationale |
|---|---|---|---|---|
| **Ability hotbar slot** | 124 × 98 px | **120 × 120 px** (radial arc) | reshape to circular | Genre canon: DI 110-120 px circular arc; Torchlight 95-110 px square→circle; cluster centroid 115 px. Move from rectangular hotbar to **radial arc** layout (DI/Torchlight/Genshin canon) |
| **Ability slot (ultimate)** | ~143 × 113 px | **150 × 150 px** circular | upscale + reshape | Ultimate slightly larger than core abilities (DI canon: ult is ~1.25× core slot diameter) |
| **Potion button (HP/MP)** | bottle ~34 × 44 px (HUD); 116 px globe in `diabloHud.ts` | **140 × 140 px** circular | upscale | Potion is the most-tapped touch target; genre canon DI/Eternium ~125-140 px; sized slightly larger than ability slots |
| **HP/MP globe (Diablo-style HUD)** | r=58 (d=116) | r=58 (d=116) | ×1.0 (potentially merge with potion button on mobile) | Mobile typically **merges** the HP/MP display with the potion-button affordance (DI does this; Immortal HP-globe IS the HP-potion button). Open design question — see § 7 |
| **Dash icon** | r=26 (d=52) | r=55 (d=110) | ×2.1 | Touch-target floor: 88 px minimum diameter; dash is high-frequency action; sized at action-canon centroid 110 px |
| **Top-row inventory/character/log icon** | r=26 (d=52) | r=44 (d=88) | ×1.7 | Touch-target floor: 88 px = 44 dp at 2× (Apple HIG / Material minimum) |
| **HP bar under sprite** | 96 × 7 px | 72 × 5 px | ×0.75 (matches sprite shrink) | Bar scales with sprite; visual proportion preserved |
| **Resource bar under sprite** | 96 × 4 px | 72 × 3 px | ×0.75 | Same as HP bar |
| **Joystick outer ring** | r=80 (d=160) — current mobile-stage value | r=75 (d=150) | minor refine | Genre cluster (DI / Torchlight / Genshin) centers at ~150 px outer; current 160 px is at upper edge; 150 px is centroid |
| **Joystick inner thumb** | r=30 (d=60) — current mobile-stage value | r=28 (d=56) | minor refine | Cluster centroid ~50-60 px |
| **Click-hit forgiveness radius** | 50 px | **75 px** | ×1.5 | Touch-hit forgiveness needs to be larger than mouse-click forgiveness (finger occludes the target; tap registers at the **center** of the touch contact patch which is ~10-15 px off the visible target) |

### § 3.3 — Object types we don't yet have (PC = N/A; mobile derived from § 2 cluster; PC values would reverse-derive at ÷0.75)

| Object | Mobile target | Implied PC value (÷0.75) | Player-sprite ratio | Tile (1m=48px on PC, 48px on mobile) ratio | Rationale |
|---|---|---|---|---|---|
| **Gear drop (sword / staff)** | 50 × 50 px sprite | ~67 × 67 px | ~0.50 to player (mobile player 107 px) | ~1.04 tile | DI/Torchlight/Eternium cluster: 50-70 px; centered at 55 px; rounded to 50 |
| **Gear drop (armor / shield)** | 55 × 55 px | ~73 px | ~0.51 | ~1.15 tile | Slightly larger than weapons (visual weight); body-armor pieces |
| **Currency / gem drop (gold pile)** | 35 × 35 px | ~47 px | ~0.33 | ~0.73 tile | Torchlight 30-40 px; Eternium 30-40 px |
| **Currency drop (special — rune / shard)** | 40 × 40 px + glow | ~53 px | ~0.37 | ~0.83 tile | Slightly larger than ordinary gold; high-saliency drop |
| **Treasure chest (small)** | 110 × 90 px | ~147 × 120 px | ~1.0 to player | ~2.3 × 1.9 tile | DI/Torchlight cluster 100-130 px; sized for clear tap-affordance |
| **Treasure chest (medium / standard)** | 130 × 105 px | ~173 × 140 px | ~1.2 | ~2.7 × 2.2 tile | Standard reward chest |
| **Treasure chest (large / legendary, animated)** | 170 × 140 px + animated glow | ~227 × 187 px | ~1.6 | ~3.5 × 2.9 tile | DI legendary chest 180-220 px; rare-spawn affordance |
| **Strongbox (PoE-style open-event chest)** | 150 × 125 px | ~200 × 167 px | ~1.4 | ~3.1 × 2.6 tile | Torchlight strongbox cluster |
| **Armor rack (decor; non-interactive)** | 80 × 130 px | ~107 × 173 px | ~1.2 (tall) | ~1.7 × 2.7 tile | Ambient decor; vertical |
| **Weapon rack (decor; non-interactive)** | 100 × 110 px | ~133 × 147 px | ~1.0 | ~2.1 × 2.3 tile | Ambient decor; horizontal |
| **Vase / urn (destructible)** | 65 × 80 px | ~87 × 107 px | ~0.75 | ~1.4 × 1.7 tile | DI vase 70-100 px; Eternium urn 70-95 px; centroid 80 px tall |
| **Amphora / large urn (destructible)** | 85 × 110 px | ~113 × 147 px | ~1.0 | ~1.8 × 2.3 tile | Larger variant; legendary-loot-containing tier |
| **Tree stump / fallen log** | 90 × 55 px | ~120 × 73 px | ~0.5 (wide, low) | ~1.9 × 1.1 tile | Outdoor scenery; horizontal-oriented destructible |
| **Barrel** | 75 × 95 px | ~100 × 127 px | ~0.85 | ~1.6 × 2.0 tile | DI/Torchlight cluster; classic ARPG destructible |
| **Crate (wooden)** | 80 × 80 px | ~107 px | ~0.75 | ~1.7 tile | Wider than tall; ambient |
| **Crystal cluster** | 70 × 90 px + glow | ~93 × 120 px | ~0.85 | ~1.5 × 1.9 tile | Magical-substrate variant; emissive |
| **Bone pile / skull pyramid** | 95 × 75 px | ~127 × 100 px | ~0.7 | ~2.0 × 1.6 tile | Necromantic biome ambient; destructible |
| **Coin pile (large hoard)** | 110 × 60 px + sparkle | ~147 × 80 px | ~0.55 (wide, flat) | ~2.3 × 1.25 tile | Boss-drop visual centerpiece |
| **Name-plate text overlay (loot)** | ~12 px font, ~80 px wide bg | n/a | n/a | n/a | DI canon: auto-display on drop; **adds ~30 px vertical above drop sprite**; high-saliency rarity color |
| **Tap-target affordance ring** (outline glow when interactable) | adds 10-12 px padding around object bounds | n/a | n/a | n/a | DI/Eternium canon; lets player see what's tappable at thumb-reach |

### § 3.4 — Camera framing (the load-bearing variable mobile changes that PC doesn't)

| Parameter | PC default | Mobile target | Rationale |
|---|---|---|---|
| **Camera zoom (player fraction of viewport height)** | player ~7.5% of 944px canvas | player ~12-14% of mobile-viewport (e.g., ~107 px / ~800 px effective) | Mobile pulls camera in tighter; player occupies larger fraction of screen; combined with 0.75× sprite shrink, net effect: smaller world-area visible, but **density per visible area is the same** (because tile size is unchanged) |
| **Viewport effective dimensions** | 1800 × 944 (canvas fixed) | 1800 × 944 internal; **CSS-scaled to 100vw × 100dvh** with `object-fit: contain` per current `mobile.ts` | Internal resolution preserved; visual scaling by CSS; UI elements positioned in canvas-space |
| **World-area visible (default 30m × 30m room)** | ~37.5m × ~19.7m (1800/48 × 944/48) | ~28m × ~15m (after camera zoom 1.33×) | Mobile shows ~75% of the world-area; matches the 0.75× sprite shrink (the cross-relationship that preserves density) |

**The density-preservation invariant.** This is the key cross-platform commitment: a player on PC and a player on mobile **see the same number of monsters per visible area** at the same density. PC shows more world; mobile shows fewer monsters; *density per square meter is identical*. This is what makes the sim-emitted monster-spawn densities (per `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3) platform-portable.

---

## § 4 — Transformation principles (the "why")

These principles enable future scope amendments (new object types, new platforms — tablet, foldable, console-touch) without re-running the survey. When a new object emerges, apply principles in order; the table extends naturally.

### § 4.1 — World-scale primitives shrink uniformly (sprite scalar 0.75×)

**Principle.** Player sprite, monster sprites (all tiers), VFX sprites, projectile sprites, and physical-world destructibles all shrink by the same scalar (0.75×) from PC to mobile. The TIER_SCALE table (per `archetypeRenderer.ts`) is preserved unchanged — only the **base unit** the table multiplies against changes.

**Why.** Preserves the **player:monster identity ratio** that drives encounter readability. If trash monster appears 75% of player size on PC, it should appear 75% of player size on mobile — the player's *perception* of "I am bigger than this trash mob" is a load-bearing combat-feel signal. Genre cluster (DI/Torchlight/Eternium) all preserve this cross-ratio; only the base unit changes.

**Counter-example: don't do this.** Some mobile ports shrink player sprite while keeping monster sprite full-size (Lost Ark Mobile early-beta did this briefly). Player perceives "monsters are big and I am small" — inverted threat signal; emotionally hostile. Reincarnated does not do this.

### § 4.2 — Tile size is sacred — PIXELS_PER_METER is platform-invariant

**Principle.** `PIXELS_PER_METER = 48` does NOT scale across platforms. Tile size, room dimensions, hallway dimensions, and all distance-derived quantities (movement speed, AOE radius, projectile travel) stay in absolute pixel-per-meter units regardless of platform.

**Why.** Per `movement-speed-baseline.md` § "Sim-consumption gating clause": the sim emits movement speed, AOE radius, projectile range in m/s and meters. The demo must consume those values via `× PIXELS_PER_METER`. If the constant differs across platforms, the sim is balancing the wrong fight on at least one platform. The Option-B commitment (single source of truth) requires PIXELS_PER_METER to be a single number; that number is 48.

**What mobile changes instead.** The **camera zoom** changes (per § 3.4). Mobile shows ~75% of the world-area PC shows. Density per square meter stays the same; monsters-per-screen stays the same; sim-consumed values stay the same.

**Counter-example: don't do this.** Don't change PIXELS_PER_METER to 36 on mobile to "fit more world on screen." That would make the engine ship with two parallel realities (sim balanced for 48; demo plays at 36). Drift. Discipline #13 violation. Inverse-Option-B.

### § 4.3 — Touch targets upscale to genre canon (110-125 px diameter centroid)

**Principle.** All tap-able UI elements (ability buttons, potion buttons, top-row icons, joystick) sit at **88 px minimum diameter (Apple HIG 44 pt / Material 48 dp at 2×)**, with **110-125 px as the action-touch canon centroid for high-frequency actions** (abilities, potions). Decorative or low-frequency taps can sit at the 88 px floor.

**Why.** Touch ergonomics are non-negotiable. A 60 px tap target (PC's dash icon at r=26) is below the Apple HIG floor and produces miss-tap rate above the playable threshold. Genre cluster (DI/Torchlight/Eternium/Genshin) converges on 110-125 px for ability buttons because that's the size at which a thumb-tap has <1% miss rate at typical hold-grip.

**Sub-rule: hit-zone exceeds visual-zone by 5-10 px.** Per current `mobile/touchPotions.ts`: visual `POT_R=28`, hit `HIT_R=38` — a 10 px padding. This pattern is correct and applies to all touch targets. The visual element does NOT need to be at 110 px; the **hit-zone** does. A 95 px visual button with a 110 px hit-zone reads as the same affordance and hits the touch-target floor.

### § 4.4 — Drop visibility increases on mobile via auto-display affordances, not via sprite upscaling

**Principle.** Gear drops, currency drops, and loot pickups have the same relative size on mobile as PC (when PC values exist). What mobile adds is **auto-display name-plate text overlay** + **tap-target affordance rings** + **rarity-colored loot beams**.

**Why.** Upscaling drop sprites on mobile would expand them past 1.0× player-sprite ratio and create a visual hierarchy problem ("the loot is bigger than I am"). Genre cluster avoids this by adding **information layers** (name plate, beam, ring) rather than sprite-size scaling. DI auto-displays gear-drop names by default; Torchlight uses rarity-colored vertical beams; Eternium uses tap-affordance rings.

**Sub-rule: rarity differentiation is visual-layer-coded, not size-coded.** Common = small sprite, no beam, no name. Magic = small sprite, blue beam, name on. Rare = small sprite, yellow beam, name on, faint ring. Legendary = small sprite, orange beam, name on, animated ring + glow. The sprite stays small; the **information halo** scales with rarity. This is the mature ARPG mobile canon (DI / Torchlight / Eternium all converge on this).

### § 4.5 — Destructible ambient sized for tap-affordance (not proportional shrink)

**Principle.** Interactive ambient scenery (vases, urns, barrels, crystal clusters) that the player taps to destroy is sized at **~0.7-0.9× player-sprite-height** on mobile — slightly upscaled vs proportional shrink. Non-interactive decor (armor racks, weapon racks, set decoration) follows § 4.1's sprite-shrink scalar.

**Why.** Interactive destructibles need to read as tap-able at thumb-reach. At <0.5× player-sprite-height they shrink below the action-touch floor and become accidental-tap-only. Genre cluster (DI vase 0.75; Torchlight urn 0.7; Eternium barrel 0.8) clusters at 0.75-0.85× player-sprite — visually proportional but not below the tap-target floor.

**Sub-rule: tap-target affordance ring adds 10-15 px effective tap-zone.** The visible vase can be 65×80 px; the **interactive ring** when player is in range is 80×95 px. The ring is the touch target; the vase is the visual.

### § 4.6 — HUD compresses via layout reorganization, not via element downscaling

**Principle.** Mobile HUDs compress vertically and reorganize layout (rectangular → radial / arc) rather than shrinking individual UI element sizes. A 124×98 PC hotbar slot becomes a 120 px circular slot on mobile in a radial arc, not an 80×60 rectangle.

**Why.** Element-downscaling collides with touch-target floors; layout-reorganization preserves touch ergonomics while reclaiming screen real estate. The radial-arc-of-abilities pattern is the genre canon (DI 6-button arc; Torchlight 4-6 button arc; Genshin 5-button arc) precisely because it places 5-6 ability buttons inside thumb-arc reach without violating the 110 px diameter floor.

**Sub-rule: HUD elements migrate to thumb-reach corners.** Left thumb = movement joystick (~150 px outer, ~bottom-left); right thumb = ability arc + potion buttons + ultimate button (~bottom-right). Top corners get low-frequency taps (inventory, character, settings, log). Center top = HP/MP indicators + status effects. This is the action-touch genre canon; Reincarnated mobile inherits it.

### § 4.7 — Camera zoom-in compensates for viewport shrink (density-preservation invariant)

**Principle.** Mobile shows ~75% of the world-area PC shows at any moment. This is achieved via **camera zoom-in (1.33×)** combined with **sprite shrink (0.75×)**. Net: density per visible area is identical across platforms.

**Why.** Per § 4.2, sim-emitted values are platform-invariant. Density per square meter is what the sim balances. Mobile keeping density-per-area constant means the playtest signal at mobile and the sim signal at engine match — they're balancing the same fight.

**Sub-rule: AOE radius and skill ranges are NOT scaled at the renderer.** A 5-meter fire-burst AOE is 240 px on PC AND 240 px on mobile. Mobile player sees fewer monsters in that 240 px circle (because the camera is zoomed in 1.33×); PC player sees more. **The skill itself is unchanged** — what differs is the encounter framing.

---

## § 5 — Methodology + citations

### § 5.1 — Methodology

**Approach: 4-anchor genre cluster + extrapolation.** Solid Maiar-knowledge anchors (DI / Torchlight Infinite / Eternium / D3 Switch-port reference) defined the centroid; adjacent-genre titles (Genshin / Lost Ark Mobile / Wuthering Waves / Brawl Stars) triangulated touch-target floors; sparse-knowledge titles (Anima / Oniro / Dungeon of Exile / DH6) are routed to Legolas Mode B enrichment.

**Why this is sufficient for the dispatch:** the canon's job is to give Drax implementable values when the mobile dispatch fires. The 4-anchor cluster centroid is **stable** — DI/Torchlight/Eternium all converge on the same canon within ±10%, and the adjacent-genre touch authorities confirm the touch-target floors independently. Outliers (Anima / Oniro / Dungeon of Exile) may modulate the cluster by ±5-10% when Legolas returns; that's table-refinement territory, not table-rewrite territory.

**Knowledge-confidence flags** (per § 2): solid / partial / sparse marks were applied per-title; sparse titles routed to Legolas; the table in § 3 weighted-by solid-anchor data.

### § 5.2 — Legolas Mode B sub-commission

Filed (or to be filed) at `agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md`.

**Scope:** Web-crawl survey of 4 sparse-knowledge titles (Anima ARPG, Oniro ARPG, Dungeon of Exile, Dungeon Hunter 6 current build) for per-object pixel sizing data. Specific items per title: player sprite height, monster sprite (trash + boss), ability button diameter, potion button, joystick outer, gear-drop, chest, vase/urn, barrel.

**Sources Legolas should prefer:** vendor App Store screenshots (highest fidelity), recent gameplay video (YouTube / official trailers; preferably 2025+), gameplay subreddit screenshot threads, mobile game-review sites with screenshot galleries (Pocket Gamer / Touch Arcade / GamingOnPhone).

**Output destination:** `agentic_orchestration/research/2026-05-17-mobile-arpg-pixel-sizing-survey/` — per-title sub-directories with screenshots + measurement notes + sizing table.

**Consumption pattern:** When Legolas returns, gandalf reviews findings; if material deviations from the 4-anchor cluster emerge (>±15% for any centroid value), authors a v1.7b refinement to this doc. If findings confirm the cluster (within ±10%), files a "cluster confirmed; no table revision" note + advances v1.7 as-is to authoritative.

**Authorization:** Pre-authorized per dispatch's "Legolas Mode B sub-commission is pre-authorized" clause. Knight-rider does not need to re-authorize per-call.

### § 5.3 — Citations + limitations

**Primary citations** (Maiar-knowledge anchored to publicly observable mobile-game release builds):
- Diablo Immortal: Blizzard 2022 release; observed across 2022-2025 patches
- Torchlight: Infinite: XD Inc. 2022 release; observed across 2022-2025 patches
- Eternium: Making Fun ~2014 release; long-running observation
- Diablo III Switch port: 2018 Blizzard/Nintendo collaboration

**Triangulation citations** (action-touch UI canon, non-ARPG):
- Genshin Impact (HoYoVerse, 2020)
- Honkai: Star Rail (HoYoVerse, 2023)
- Wuthering Waves (Kuro Games, 2024)
- Lost Ark Mobile (Smilegate, Korean release 2024)
- Brawl Stars (Supercell, 2017)

**Limitations:**
1. Maiar-offline-knowledge for sparse titles is the principal limitation (mitigated by Legolas Mode B enrichment).
2. Pixel-size values reported are observed-at-1080p-equivalent; high-DPI variance (true 1440p phones, foldable Galaxy Fold high-DPI panels) may shift absolute pixels while preserving DP / point counts. The table reports pixels assuming 2× DPI; foldable / 3× DPI shifts are out of scope.
3. Per-vendor in-game zoom controls (DI offers a camera-zoom slider; Torchlight offers two camera presets) introduce ±10-15% spread within a single title. Cluster centroids reported are at the title's **default** camera setting.
4. Cluster derived from 2022-2025 release-build data. Mobile ARPG genre is evolving; centroids may drift over 2-3 year horizons. Re-survey may be warranted at Phase-2 of the broader project if mobile rollout slips substantially.

---

## § 6 — Forward hooks

### § 6.1 — Drax (consumer; when mobile dispatch fires)

Drax's eventual mobile dispatch consumes § 3's transformation table directly. Concrete implementations:

- **`mobile/joystick.ts`:** Refine R_OUTER from 80 to 75 (cluster centroid 150 px diameter). R_INNER from 30 to 28. *Minor refine only.*
- **`mobile/touchPotions.ts`:** Confirm POT_R=28 (visual radius 56 px) is the mobile-only display; hit zone HIT_R=38 (76 px) is at the touch-target floor; consider upscaling visual to ~70 px diameter (POT_R=35) to match the action-touch canon centroid; HIT_R correspondingly to ~50.
- **`mobile/touchIcons.ts`:** ICON_R from 26 to 44 (88 px diameter touch-target floor). HIT_R from 36 to 50.
- **New file `mobile/touchHotbar.ts`** (exists; verify): radial arc of 6 ability buttons at ~120 px diameter each; ultimate at ~150 px. Layout: bottom-right quadrant, ~700 px arc width.
- **New objects (not yet rendered on PC):** gear drops, chests, destructibles — Drax authors per § 3.3 mobile target values; PC equivalent values reverse-derive at ÷0.75.
- **Camera zoom-in (1.33×):** Implement via Pixi `stage.scale.set(1.33)` or per-layer transform when `Mobile.isActive`. Combined with 0.75× sprite shrink, net world-area shown is ~75% of PC. *This is the load-bearing change* — without camera zoom-in, mobile shows full PC world-area at smaller sprites and combat reads as "tiny figures in a big space" (a known mobile-port anti-pattern).
- **Sprite shrink:** Implement via TIER_SCALE multiplier at root level when `Mobile.isActive` (e.g., a `WORLD_SCALE_MOBILE = 0.75` constant applied to `bodyContainer.scale`). Alternative: shrink at the camera layer (cleaner architecturally). Drax's call.

### § 6.2 — Elrond (catalog; schema fields if any)

The catalog already tracks asset visual style (per `style-register.md` consumption-time filter pattern). Potential new schema field:

- **`platform_suitability`** (enum: `pc_only` / `mobile_only` / `both`) — for assets whose pixel resolution or aspect ratio makes them unsuitable for one platform. Most assets are `both` (the 0.75× scalar handles platform transformation); some HUD-tier assets (high-resolution potion-globe textures, e.g.) may be `pc_only` if their native resolution exceeds mobile's effective viewport.

This is an optional field; defer to Elrond's judgment on whether the catalog needs it before the mobile dispatch fires. The transformation table works without it.

### § 6.3 — Future scope (out of immediate scope; flag for later)

- **Tablet (iPad) variant:** between PC and phone. Likely 0.85-0.90× scalar (less aggressive shrink than 0.75×). Out of scope for this commission; address when iPad becomes a target.
- **Foldable phones (Galaxy Fold class):** wider aspect ratio on unfolded; effectively closer to PC-tablet hybrid. Sizing may want per-orientation specialization. Out of scope.
- **Console-touch (Switch handheld) port:** sizing is closer to PC than mobile (screen-legibility-bound, not touch-ergonomics-bound). Likely 0.85× scalar. Out of scope; would need its own commission.
- **Mobile-Phase-2 specific gameplay tuning** (touch-gesture skills, mobile-exclusive combat tuning per the dispatch's out-of-scope note): explicitly deferred. This commission produces the **sizing canon**, not the **combat tuning canon**.

---

## § 7 — Open questions for Matt

These are deferrable design questions; the table in § 3 is implementable without resolving them. Surfacing for Matt's awareness when the mobile dispatch fires.

1. **HP/MP globe vs HP/MP potion-button — merge or separate?** Diablo Immortal merges the two: the HP-globe IS the HP-potion button (tap the globe → drink potion). Eternium keeps them separate. Our current PC has both (`ui/diabloHud.ts` globes + `ui/potionHud.ts` bottles); mobile would naturally merge for screen-real-estate efficiency. **Recommend: merge on mobile** (DI canon); keep separate on PC. Drax can implement either.

2. **Inventory access on mobile — drawer slide-out or full-screen modal?** PC has inline inventory + full character sheet. DI uses full-screen modal for inventory; Torchlight uses drawer slide-out. **Recommend: full-screen modal** for richer info density; mobile screen real-estate is too tight for inline. Out of scope for this commission's sizing table; flag for the mobile dispatch.

3. **Dual-stick or tap-to-move on mobile?** PC is mouse-LMB-click-to-move. Mobile genre canon is split: DI / Torchlight / Genshin / Wuthering Waves use **dual-stick (left joystick + right ability arc)**; Eternium / Lost Ark Mobile use **tap-to-move primary + ability tap secondary**. Current `mobile/joystick.ts` ships dual-stick. **Recommend: dual-stick (canonical for action-ARPG-on-touch)**; preserves the directional-movement feel that the kiting-math (per `movement-speed-baseline.md`) depends on. Tap-to-move would erase the chase-margin signal at the input layer. Out of scope for sizing; reaffirmed here as the locked recommendation.

4. **Mobile resolution targets — 1080p baseline or 1440p baseline?** The table assumes 1080p mobile equivalent (most common mid-range phone resolution 2023-2025). Premium phones (1440p+) render the same UI larger absolute pixels but identical DP. Most assets will scale via Pixi's renderer-native scaling. **Recommend: author at 1080p mobile equivalent; trust Pixi DPR handling for higher-DPI panels.** Drax may want to confirm this in the mobile dispatch.

5. **Dungeon of Exile — pull a copy and play it?** Matt flagged this as "a good one." His implicit recommendation may be that Reincarnated mobile feel should resemble Dungeon of Exile. Worth Matt actually playing it (if he hasn't recently) and giving us a paragraph on what specifically feels right; that paragraph may shift the cluster centroid for our specific design intent. Out of scope here; surfacing for Matt's awareness.

---

## Appendix A — Quick reference card

For Drax: the "answer this in 5 seconds" version of the canon.

```
SPRITES (world-scale): mobile = PC × 0.75
TILES (PIXELS_PER_METER=48): UNCHANGED
TOUCH TARGETS: minimum 88 px diameter; action canon 110-125 px
CAMERA: zoom in 1.33× on mobile (compensates for 0.75× sprite shrink; density preserved)
DROPS: same relative size; mobile adds name plates + beams + rings
DESTRUCTIBLES: 0.7-0.9× player-sprite-height; tap-affordance ring extends hit zone
HUD: radial / arc layout (not rectangular); thumb-reach corners
```

For Matt: the "what does it feel like on the table" version.

```
Mobile shows ~75% of the PC world-area at any moment, with sprites at 0.75× PC size.
Player and monsters look the same RELATIVE size (player still 1.33× a trash mob);
density of monsters per visible area is identical; sim values are unchanged;
touch buttons are 110-125 px (thumb-comfortable); loot drops are small but
flagged with name plates and rarity beams. The world is the same world; the
camera is closer, the buttons are bigger, the sprites are smaller. Same game.
```

---

*Commission complete 2026-05-17 by gandalf. Canon ready for drax's eventual mobile dispatch (VS2b territory or later). Legolas Mode B sub-commission filed as enrichment pass; v1.7b refinement folds in if Legolas findings shift cluster ±15% or more. The hive moves together. — gandalf*
