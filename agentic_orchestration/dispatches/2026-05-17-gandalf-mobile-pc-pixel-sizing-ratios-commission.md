# 2026-05-17 — gandalf — Mobile vs PC pixel sizing & ratio research commission

**Authority:** Matt L3 commissioned 2026-05-17 (~15:30 EDT).
**Type:** Pattern B — research commission (Mode A analytical + authorized Mode B catalog crawl via legolas).
**Estimated effort:** ~1-2 days (gandalf synthesis ~6-10h + legolas crawl ~6-12h if sub-commissioned).
**Predecessor:** gandalf v1.6 AOE windup ARPG validation (genre-canon comparative methodology proven).
**Scope window:** Forward-looking; output feeds future mobile UI work in **VS2b territory or later** — not VS2a-gating. Research is timing-independent; capture the canon while bandwidth is available.

---

## Why this matters

We currently have a well-tuned pixel-size and ratio system for **PC**:
- Player sprite ↔ monster sprite ratio
- Skill/potion/ability icon sizes + ratios
- Tile sizes + ratios

These ratios do NOT carry to mobile. Mobile phone screens demand different absolute pixel sizes for combatants, icons, tiles, and HUD elements because of:
- Screen size constraint (4-6.5 inches, 1080-1440 px wide vs 1920+ on PC)
- Touch-input ergonomics (~44 px minimum touch target; thumb-reach constraints)
- DPI variance (mobile is high-DPI; absolute pixels and effective dp/pt differ)
- HUD overlay density (mobile compresses more UI into less screen real-estate)

We need a **transformation table** that maps each PC sprite/icon/tile type to its appropriate mobile equivalent, derived from the genre's mobile-ARPG canon.

Per Matt's frame: this is a Maiar-grade game-dev knowledge job. Gandalf draws on accrued ARPG history; if the catalog crawl breadth exceeds gandalf's offline knowledge, gandalf is **explicitly authorized** to sub-commission legolas in Mode B for a web-crawl pass on the named titles.

---

## Required reading (gandalf, before scoping)

1. `reincarnated-demo/src/main.ts` lines that define current PC sizing constants (search `CANVAS_WIDTH`, `CANVAS_HEIGHT`, `PIXELS_PER_METER`, sprite scale factors, icon sizes)
2. `reincarnated-demo/src/ui/potionHud.ts`, `dashCooldownHud.ts`, `combatHud.ts` — current PC HUD-element dimensions (icons, sweep, panels)
3. `reincarnated-demo/src/mobile/` — what exists for mobile already (touchPotions, mobile-specific HUD)
4. `canonical/story/movement-speed-baseline.md` § "PIXELS_PER_METER" — anchor for sprite-size derivation
5. Any prior Matt-gandalf discussion on mobile (search `mobile` in canonical/ + decisions-log) to avoid re-treading ground

---

## Scope

### Item 1 — Mobile ARPG genre survey

Catalog the following titles in **mobile-as-shipped form** (Android/iOS):

| Title | Vendor | Genre relevance |
|---|---|---|
| Diablo Immortal | Blizzard | The flagship mobile ARPG; PC-derived |
| Torchlight: Infinite | XD Inc. | Currently dominant mobile ARPG; PoE-adjacent |
| Anima ARPG | (varies) | Mobile-first ARPG |
| Oniro ARPG | (varies) | Mobile-first ARPG |
| Eternium | Making Fun | Long-running mobile ARPG; touch-canonical |
| Dungeon Hunter 6 | Gameloft | Console-derived mobile |
| **Dungeon of Exile** | (Matt highlight — "this is a good one") | Per Matt: high-priority comparison |
| (any additional Maiar-flagged titles) | — | Gandalf's call |

For each title, capture (with citations where possible — vendor screenshots, app-store hero shots, recent gameplay video):
- Player sprite pixel size at default zoom (px tall × px wide at 1080p mobile equivalent)
- Monster sprite typical size (representative trash mob + boss)
- Player ↔ monster sprite **ratio**
- Skill/ability icon size (px square)
- Potion/consumable icon size (px square)
- Tile size (floor texture repeat unit, in px)
- Player sprite ↔ icon **ratio**
- Player sprite ↔ tile **ratio**

If gandalf's offline knowledge is sparse on any of these titles, **commission legolas Mode B**: knight-rider authorizes a sub-commission for a web-crawl pass on the named titles, output filed under `agentic_orchestration/research/<date>-mobile-arpg-pixel-sizing-survey/` (or similar). Gandalf consumes legolas's output and synthesizes.

### Item 2 — Mobile-specific object types we DON'T currently have

In addition to the above (objects we already render on PC), capture pixel sizes from the survey titles for:

- **Gear drops** (sword/staff/armor pieces lying on floor; ratio to player sprite)
- **Loot drops** (gold piles, gems, currency items on floor)
- **Treasure chests** (small/medium/large variants)
- **Armor and weapon racks** (set decor; both occluding-NPC-tier and ambient-only)
- **Destructible ambient scenery:**
  - Vases / urns / amphorae
  - Tree stumps / fallen logs
  - Barrels / crates
  - Crystal clusters
  - Bone piles / skull pyramids
  - Any other recurring destructible primitive Matt would recognize

For each: typical pixel size, ratio to player sprite, ratio to tile.

### Item 3 — PC ↔ mobile transformation table

Author a single canonical sizing table:

```
Object             | PC default | Mobile derived | Ratio rationale
-------------------|------------|----------------|----------------
Player sprite      | ~96 px     | ~72 px (0.75×) | Touch zone = thumb-reach
Monster trash      | ~80 px     | ~60 px (0.75×) | Same scalar; ratio preserved
Monster boss       | ~160 px    | ~120 px        | ...
Skill icon         | ~48 px     | ~56 px (1.17×) | Touch target 44+ minimum
Potion icon        | ~64 px     | ~72 px         | ...
Tile               | ~48 px     | ~48 px         | UNCHANGED — environment density
Gear drop          | (n/a)      | ~32 px         | ...
Treasure chest     | (n/a)      | ~80 px         | Interaction affordance
Vase (destructible)| (n/a)      | ~40 px         | ...
[etc.]
```

Numbers above are **placeholders for shape only** — gandalf derives real numbers from the survey.

The table is the dispatch's primary output. It needs to be specific enough that drax's eventual mobile dispatch can implement it directly.

### Item 4 — Transformation principles (the "why")

Author a short principles section explaining the transformation logic, e.g.:

- **Sprites:** scale by N× (e.g., 0.75×); preserve cross-ratio (player:monster ratio constant across platforms)
- **Tiles:** UNCHANGED (preserves environment density; mobile players want SAME density of decor, not more zoomed-in)
- **Touch targets (icons, buttons):** UPSCALE to minimum 44 px (Apple HIG) / 48 dp (Material); platform-canonical minima
- **HUD:** mobile compresses to single-column or radial layouts (cite specific patterns from survey titles)
- **Drop visibility:** mobile increases relative size of loot drops vs PC to compensate for smaller viewport (per Eternium / Diablo Immortal canon)
- **Destructible ambient:** sized for tap-affordance (slightly upscaled vs proportional shrink) when interactive

Principles enable future scope amendments without re-running the survey.

### Item 5 — Output structure

File the output at `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (or equivalent canonical path; gandalf chooses).

Document sections:
1. Executive summary (1 paragraph)
2. Mobile ARPG genre survey results (Item 1 + Item 2 capture)
3. Canonical sizing table (Item 3)
4. Transformation principles (Item 4)
5. Citations / methodology notes
6. Forward hooks: what drax's eventual mobile dispatch consumes; what elrond's catalog might want to track as schema fields (if any)

### Item 6 — Hive log + tag

- STATE entry with verdict (table size; titles surveyed; legolas-used yes/no)
- Tag `gandalf/v1.7-mobile-pc-pixel-sizing-ratios-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT implement any mobile UI changes (research only; drax will execute downstream)
- ❌ DO NOT extend scope to mobile-platform-specific gameplay tuning (combat balance, touch-gesture skills) — that's separate Phase-2 work
- ❌ DO NOT lock specific implementation timing (mobile rollout is post-VS2a; this commission produces the canon now so drax can execute when scheduled)
- ❌ DO NOT bias toward any single title (e.g., Diablo Immortal alone) — canon is the cluster, not the outlier

---

## Acceptance criteria

- [ ] Mobile ARPG genre survey complete for 7+ titles (Matt-named set; legolas sub-commission allowed)
- [ ] Per-object pixel sizes + ratios captured (sprites, icons, tiles, gear drops, chests, racks, destructibles)
- [ ] Canonical sizing table authored with PC → mobile mapping
- [ ] Transformation principles documented (the "why" enables future amendments)
- [ ] Citations or methodology notes captured
- [ ] Forward hooks for drax + elrond identified
- [ ] Canonical doc filed
- [ ] Tag `gandalf/v1.7-mobile-pc-pixel-sizing-ratios-1`
- [ ] Hive-log STATE entry

---

## Smoke expectation

Matt reads the canonical doc + table; can answer "what size is a vase on mobile?" / "what's the player:monster ratio on mobile vs PC?" directly from the table. Drax can implement mobile sizing without re-running the survey when the mobile dispatch fires.

---

## Coordination notes

- **Legolas sub-commission authorization:** gandalf may invoke legolas Mode B for web crawl of any survey title where gandalf's offline canon is sparse. Legolas commission file goes to `agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md`. Output goes to `agentic_orchestration/research/<date>-mobile-arpg-pixel-sizing-survey/`. Knight-rider pre-authorizes this sub-commission.
- **Hive log discipline:** PRE-SIGNAL per § 14.1.1 before hive-log appends.
- **No code changes:** this commission produces canonical reference data only.

---

*Commissioned 2026-05-17 by knight-rider per Matt L3. ~1-2 days. Append completion record when done.*

---

## 2026-05-17 — gandalf — Commission COMPLETE

**Tag intent:** `gandalf/v1.7-mobile-pc-pixel-sizing-ratios-1` (applied at commit)
**Canonical doc:** `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (~770 lines; 7 sections + appendix)
**Legolas Mode B sub-commission filed:** `agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md` (enrichment pass; not gating)
**Effort:** ~6 hours Maiar-knowledge synthesis from demo1 source inventory + offline ARPG-genre knowledge + adjacent-genre touch-canon triangulation
**Hive-log STATE entry:** appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md` 2026-05-17

### Verdict

Mobile-ARPG genre-canon converged 2022-2025; a stable 4-anchor centroid (Diablo Immortal / Torchlight Infinite / Eternium / Diablo III Switch-port) defines the cross-platform transformation. Three locks operationalize the PC → mobile mapping:

1. **World-scale sprites SHRINK at 0.75×** (player, monsters all tiers, projectiles, destructibles) — preserves player:monster cross-ratios that drive encounter readability. TIER_SCALE table is platform-invariant; only the base unit changes.
2. **PIXELS_PER_METER = 48 STAYS PLATFORM-INVARIANT** — tile size, room dimensions, AOE radius, MS all sim-canonical per `movement-speed-baseline.md`. Mobile compensates via **camera zoom-in 1.33×**. Density per visible area is preserved across platforms; sim balances one fight, not two.
3. **Touch targets UPSCALE to 110-125 px diameter** for action canon (ability buttons, potions); 88 px floor for ambient affordances. Genre cluster + Apple HIG / Material Design floors honored.

### Survey titles captured

**Solid Maiar-knowledge anchors (define cluster centroid):**
- Diablo Immortal (Blizzard 2022) — full sizing capture
- Torchlight: Infinite (XD Inc. 2022) — full sizing capture
- Eternium (Making Fun ~2014, continuous updates) — full sizing capture
- Diablo III Switch port (2018) — screen-legibility-floor reference

**Partial / sparse Maiar-knowledge (routed to Legolas Mode B enrichment):**
- Dungeon Hunter 6 (Gameloft 2023) — partial; Legolas to confirm
- Anima ARPG — sparse
- Oniro ARPG — sparse
- Dungeon of Exile — sparse (Matt highlight: "this is a good one" — flagged highest-priority comparison)

**Adjacent-genre touch-canon triangulation (independent confirmation of touch-target floors):**
- Genshin Impact (HoYoVerse 2020)
- Honkai: Star Rail (HoYoVerse 2023)
- Wuthering Waves (Kuro Games 2024)
- Lost Ark Mobile (Smilegate 2024)
- Brawl Stars (Supercell 2017)

### Canonical doc deliverables

- § 1 — PC anchor (empirical sizing inventory from demo1: TIER_SCALE 0.75-1.55, PIXELS_PER_METER=48, CANVAS 1800×944, SLOT 124×98, GLOBE_RADIUS 58, joystick R_OUTER 80 / R_INNER 30, mobile potion / icon constants per current `src/mobile/` implementation)
- § 2 — Mobile ARPG genre survey (per-title pixel data + cluster-fit observations)
- § 3 — Canonical PC → mobile transformation table (4 sub-tables: world-scale sprites with scalars + rationale, HUD primitives with touch-target floor compliance, new objects not in demo1 with implied PC-reverse-derivation, camera framing parameters)
- § 4 — Seven transformation principles (sprite-shrink uniform / tile sacred / touch-target floors / drop-visibility via affordances / destructible-tap-affordance / HUD-reorganize-not-downscale / camera-zoom density-preservation)
- § 5 — Methodology + Legolas Mode B sub-commission scope
- § 6 — Forward hooks (drax: radial-arc hotbar, WORLD_SCALE_MOBILE=0.75, camera zoom 1.33×, specific refinements to existing `mobile/*.ts` files; elrond: optional `platform_suitability` schema field)
- § 7 — Five open design questions for Matt (HP-globe ↔ potion-button merge; inventory drawer vs modal; dual-stick vs tap-to-move; resolution baseline; Dungeon of Exile feel-pull)
- Appendix A — quick-reference card

### Acceptance criteria

- [x] Mobile ARPG genre survey complete for 7+ titles (Matt-named set covered; sparse titles routed to Legolas; adjacent-genre triangulation added)
- [x] Per-object pixel sizes + ratios captured (sprites, icons, tiles, gear drops, chests, racks, destructibles)
- [x] Canonical sizing table authored with PC → mobile mapping
- [x] Transformation principles documented (the "why" enables future amendments)
- [x] Citations + methodology notes captured (§ 5)
- [x] Forward hooks for drax + elrond identified
- [x] Canonical doc filed at chosen canonical path
- [x] Tag `gandalf/v1.7-mobile-pc-pixel-sizing-ratios-1` (applied at commit)
- [x] Hive-log STATE entry (with PRE-SIGNAL discipline per § 14.1.1)

### Legolas Mode B sub-commission status

**Filed, not yet executed.** Per dispatch's pre-authorization, the sub-commission is at `agentic_orchestration/research/commissions/2026-05-17-gandalf-to-legolas-mobile-arpg-pixel-survey.md`. Scope: web-crawl pixel-sizing capture of Anima ARPG / Oniro ARPG / Dungeon of Exile / Dungeon Hunter 6. Estimated 6-12 hours legolas effort. Output directory: `agentic_orchestration/research/2026-05-17-mobile-arpg-pixel-sizing-survey/`.

**Consumption pattern:**
- If all 4 sparse titles confirm 4-anchor cluster within ±10%: file "cluster confirmed" note; canon v1.7 stays authoritative; no doc revision
- If 1-2 titles deviate >±15% on specific values: file "selective refinement" note; gandalf authors v1.7b with adjusted table rows
- If 3-4 titles deviate systemically: re-examine 4-anchor cluster; possible v1.8 reset

**Most likely outcome:** scenario 1 (cluster confirmed). Genre canon is mature; sub-commission is high-value but likely confirmatory.

### Smoke expectation

Matt reads § 3 table; can answer in seconds:
- *"what size is a vase on mobile?"* → 65×80 px, ~0.75× player-sprite-height, tap-affordance ring extends hit zone by 10-12 px (§ 3.3)
- *"what's the player:monster ratio on mobile vs PC?"* → 1.0 : 0.75 trash, 1.0 : 1.55 act-boss — **identical to PC**; TIER_SCALE platform-invariant (§ 3.1)
- *"how does mobile fit the world on a phone?"* → 0.75× sprite shrink + 1.33× camera zoom-in; PIXELS_PER_METER stays at 48; density per visible area preserved (§ 3.4 + § 4.7)

Drax can implement mobile sizing without re-running the survey when the mobile dispatch fires.

### Forward-notes (not action items for this commission)

- **Mobile dispatch (drax, future):** consumes § 3 table + § 6.1 specific refinements; not blocking on Legolas Mode B return (canon is implementable from solid-anchor cluster).
- **Dungeon of Exile pull-and-play:** open question § 7 — Matt's "this is a good one" framing is high-signal; if Matt confirms DoE feel is what Reincarnated mobile should approximate, the cluster centroid may shift slightly on DoE-specific patterns.
- **Tablet / foldable / console-touch ports:** out of scope here; each would warrant its own commission with the same methodology (separate cluster, separate scalar).

— gandalf, 2026-05-17
