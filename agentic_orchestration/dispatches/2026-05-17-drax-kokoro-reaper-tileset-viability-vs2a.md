# Dispatch — 2026-05-17 — drax — Kokoro Reaper tileset viability test for VS2a

**From:** knight-rider (authored per Matt directive 2026-05-17: "I added one sample tileset from Legolas' research into the demo folder here `/Users/admin/Games/reincarnated-demo/public/tilesets/reaper`. Let's dispatch commission to test its viability for the demo VS2a.")
**To:** drax
**Approved by:** Matt at 2026-05-17
**Status:** READY-TO-FIRE
**Estimated effort:** 2-3h (tileset inventory + viability test fixture + 3-band render + screenshots + assessment + tag)

**Gate-1 bypass rationale:** Matt-directed (explicit "dispatch commission to test viability"); single-seam (drax demo render only); reversible (test fixture + screenshots; no production renderer changes); bounded scope (empirical viability test, NOT full Track D integration); pattern-aligned with prior drax v0.20.3-v0.20.4 scale-inspection-strip work.

**Per-seam discipline note:** this is drax's third dispatch in-session (Case A + Case D earlier today + this). Matt-authorized exception per scope-bounded + post-Case-D-warm-context + tightly-scoped empirical-test framing. **Do NOT auto-fire follow-on integration work** after this returns; full Track D integration (per gandalf Drift-15 commission) is a separate downstream dispatch.

**Acceptance summary:** Reaper tileset (Kokoro Reflections; 48px+MVMZ variant) inventoried + loaded into minimal Pixi.js test fixture + rendered at three demo room dimension bands (720×720 / 1440×1440 / 2160×2160 px corresponding to 15m/30m/45m at 48 px/m). Screenshots produced for gandalf visual inspection. Per-band assessment of HD-2D-quality at demo viewport scale + tile-variety adequacy + seam composition behavior + substrate alignment (death/undead/fog theme → shadow substrate per gandalf-locked naming; works as generic dark/somber dungeon for VS2a canonical-four runtime). Recommendation: PASS (use for VS2a) / CONDITIONAL (specify what would clear the bar) / FAIL (specify why; fallback to other Kokoro packs or Foozle CC0 baseline).

---

## Why this dispatch exists

Per legolas Mode B environment-tileset sweep return 2026-05-17 (`agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md`): Kokoro Reflections Reaper Tileset surfaced as **TOP candidate** for VS2a environment closure with HD-2D-ADJACENT register at 48×48 exact-meter-fit. Legolas could not verify HD-2D-quality bar without sample download + visual inspection — that gating step was Matt-action. Matt acquired + placed the sample at `/Users/admin/Games/reincarnated-demo/public/tilesets/reaper/`.

Per gandalf Drift-15 commission (`agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`): VS2a-gating recommendation; demo v1 geometric-placeholder quality drag closure is bounded.

**This dispatch is the EMPIRICAL VIABILITY TEST** — the first concrete render of an acquired tileset in the actual demo pipeline at the actual demo dimensions. It is NOT the full Track D integration (room/hallway renderer extension, prop placement randomization, animated environment tiles); those are separate downstream work.

## Cross-seam contract change?

**Round-trip: not applicable** — test fixture only; no production renderer changes; no schema changes; no other seam consumes the test fixture output. Screenshots feed gandalf visual inspection (out-of-band). Per R11(b) Principle 6.

## What's on disk (pre-verified by knight-rider)

`/Users/admin/Games/reincarnated-demo/public/tilesets/reaper/` contains:
- `48px+MVMZ/` — 48px variant matching PIXELS_PER_METER=48 convention (use THIS variant)
- `32px+VXACE/` — 32px variant (skip; wrong scale for our convention)
- `parallax-fog/` — atmospheric fog overlays (3 files: fogblack.png, fogwhite.png, Parallaxes_3.png)
- `sample maps (RPG Maker MV-MZ)/` — vendor's own composition examples (RPG Maker project files; `Mapshots/` subfolder may contain rendered screenshots for inspirational reference)
- `README non-RPG Maker engine users.txt` — confirms vendor explicitly supports non-RPG-Maker engines (Pixi.js, Tiled, Unity, Unreal). USE the `*-square.png` files (autotile-expanded format).
- `README terms of use.txt` — directs to https://kokororeflections.com/terms-use/ for full license (VERIFY commercial-OK during dispatch)

`48px+MVMZ/` files of immediate interest (non-RM format for Pixi.js):
- `non-rm-a1-square.png` — 2352×912 px (49×19 tile cells; floor autotile expansion)
- `non-rm-a2-square.png` — 1872×1344 px (39×28 tile cells; wall + interior)
- `non-rm-a4-square.png` — 2352×912 px (49×19 tile cells; wall variants)
- `!$Fire_Animation_*.png` (3 variants) + `!$Treasure_Chest_Animations.png` — animated props (animations OUT OF SCOPE for viability test; static frame inspection only if relevant)
- `reaper_A1.png` through `reaper_C_noglow.png` — RPG-Maker autotile format (probably SKIP; vendor README confirms non-RM-square versions are the right choice for Pixi.js)

Vendor README quote: "Yes, they are big. Yes, there are duplicates (they're made on a template). Yes, they waste some tile space." — i.e., the per-cell tile count overcounts unique variants. Drax should empirically measure unique-tile-variant count during inventory.

## What this dispatch produces

### Track 1 — Tileset inventory + license verification

- Document file structure of `48px+MVMZ/` (which non-rm-square files are the authoritative source for floor / wall / props)
- Measure **unique-tile-variant counts** for floor + wall + prop categories (vendor admits autotile expansion produces duplicates; actual unique variant count is what matters per legolas Mode B tile-variety floor heuristic)
- Verify commercial-use license at https://kokororeflections.com/terms-use/ (capture relevant clauses; flag if restrictive)
- Document parallax-fog assets (atmospheric overlay; potential VS2a value-add)
- Cross-reference vendor sample-maps Mapshots screenshots for inspirational composition reference (do NOT copy compositions; just absorb visual intent)

### Track 2 — Viability test fixture

Build minimal Pixi.js test fixture (NOT full room/hallway renderer extension) at `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/` or analogous location:

- Load `non-rm-a1-square.png` (floor) + `non-rm-a2-square.png` (wall/interior) + `non-rm-a4-square.png` (wall variants) as Pixi.js BaseTextures
- Use `SCALE_MODES.NEAREST` (per drax convention from Case A/D; nearest-neighbor enforcement HARD REQ for pixel-art)
- Slice tiles at 48×48 px per tile (matches PIXELS_PER_METER=48 convention)
- Render sample compositions filling each of three demo room dimension bands:
  - **Small (15m × 15m = 720×720 px):** N tiles per side = 720/48 = 15 × 15 = 225 tile cells
  - **Default (30m × 30m = 1440×1440 px):** 1440/48 = 30 × 30 = 900 tile cells
  - **Large (45m × 45m = 2160×2160 px):** 2160/48 = 45 × 45 = 2025 tile cells
- For each band: render a sample room composition (floor + wall boundary + 1-2 sample props if available). DO NOT engineer multi-room coherence; each band is independent (per gandalf commission Amendment 3: "each room can be different").
- Tile-selection strategy: use a reasonable variety of unique floor tiles to AVOID the obvious-repetition tiling artifact. If variant count is below legolas tile-variety floor heuristics (≥4 / ≥8 / ≥12 for small/default/large), document the gap.
- Wall composition: render at least one full room boundary (top + bottom + sides) so seam-behavior at room corners is visible.

### Track 3 — Screenshot output for gandalf inspection

Capture screenshots of the test fixture at each room dimension band. Place in `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/screenshots/` or analogous location:
- `reaper-viability-small-720.png`
- `reaper-viability-default-1440.png`
- `reaper-viability-large-2160.png`
- (Optional) `reaper-viability-with-parallax-fog.png` — sample composition with parallax-fog overlay applied to one of the bands

Screenshots are the load-bearing artifact for gandalf visual inspection — make them clear, well-framed, and representative of what a VS2a player would actually see.

### Track 4 — Per-band assessment

Document in completion record OR companion notes file:

For each of three room dimension bands:
- **Floor coverage:** does the floor look reasonable without obvious repetition tiling artifact?
- **Wall coverage:** does the wall boundary render credibly as room edge?
- **Prop coverage:** if props were placed, do they sit cleanly in the room interior?
- **Visual register:** does it READ as HD-2D-quality at this viewport scale? Or does the pixel-art register feel retro / low-fidelity?
- **Seam behavior:** do adjacent tiles compose without visible seams / abrupt transitions?
- **Substrate alignment:** Reaper theme = death/undead palace/fog; canonically maps to **shadow** substrate (per gandalf-locked naming). For VS2a (canonical-four runtime), does the Reaper aesthetic work as a generic **dark/somber dungeon** environment without requiring shadow substrate to be active? (E.g., works as a generic "graveyard" or "tomb" or "haunted ruin" season-feel?)

### Track 5 — Recommendation

In completion record:
- **PASS** — Reaper tileset clears HD-2D-quality bar at demo dimensions; ready for VS2a integration (Track D); credits attribution path identified
- **CONDITIONAL** — Reaper viable IF [specific gap mitigated, e.g., "supplement with additional floor variants from Kokoro Phoenix/Naga to break repetition" OR "scale-adjust to 96 px/m to reduce tile cell count per band"]
- **FAIL** — Reaper does NOT clear HD-2D bar at demo dimensions; recommend fallback to [Kokoro Phoenix / Kokoro Naga / Foozle Lucifer CC0 baseline / Elthen Cultist Dungeons]; document specific failure mode (register too retro? variety too low? scale wrong?)

Recommendation goes to gandalf (for Track B framework consumption + Matt VS2a selection); do NOT execute integration based on recommendation. Integration is downstream Track D dispatch separately authored.

### Track 6 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.8-reaper-tileset-viability-vs2a`
- AGENT_STATE.md updated
- Completion record appended to this dispatch file
- Knight-rider notified with: tag hash, screenshot paths, recommendation (PASS/CONDITIONAL/FAIL), substrate-alignment assessment, unique-tile-variant counts measured, license verification result

## Out of scope (explicit)

- **NO full room/hallway renderer extension** (Track D per gandalf Drift-15 commission; 3-5 day work; separate dispatch authored later)
- **NO ENEMY_TIER_CHARACTER_MAP changes** (unrelated; that's monster routing)
- **NO MONSTER_SCALE_BY_SLUG changes** (unrelated)
- **NO animated environment tile work** (Phase 0 ships static per gandalf commission "Not animated environments" framing)
- **NO interactive environment work** (destructible / breakable; out of Phase 0)
- **NO prop placement randomization architecture** (Track D)
- **NO attribution credits overlay integration** (cheap follow-on if PASS; separate)
- **NO other Kokoro pack viability tests** (Phoenix + Naga: separate viability tests if/when Matt adds them to the demo folder)
- **NO Foozle Lucifer CC0 viability test** (separate dispatch when needed)
- **NO multi-room-coherent tile-family hunting** (per Amendment 3 from environment-tileset commission: each room independent)
- **NO substrate-expansion runtime activation** (Phase-1 P1; VS2a stays canonical-four)
- **NO VFX-track work** (separate workstreams: CraftPix / Fellor / Frostwindz acquisitions)
- **NO new dispatch authoring** for other tilesets after this returns

## Required reading

- **Legolas Mode B scout doc:** `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md` (Reaper findings; HD-2D-ADJACENT assessment; tile-variety floor heuristics; substrate-mapping notes)
- **Legolas Mode B JSONL:** `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl` (Reaper entry; per-pack JSONL schema fields you'll cross-reference)
- **Gandalf environment commission:** `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` (Drift-15 framing; VS2a-gating context; Track A/B/C/D structure)
- **Gandalf substrate-expansion design doc:** `canonical/story/substrate-expansion-decision-2026-05-17.md` (commit `1df535b`; shadow substrate naming; VS2a/VS2b canonical-four-bound runtime)
- **Arena topology:** `canonical/story/arena-room-hallway-system.md` (15m/30m/45m room dimensions; PIXELS_PER_METER=48 anchor; ARPG-genre framing)
- **Style register:** `canonical/story/style-register.md` (HD-2D Candidate B lock)
- **Prior drax scale-inspection pattern:** `drax/v0.20.3-...` + `drax/v0.20.4-...` completion records (composite scale-strip generator pattern; reference for fixture architecture)
- **Vendor terms:** https://kokororeflections.com/terms-use/ (verify commercial-use during dispatch)
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — especially #2 smoke-test, #10 empirical inspection over assumption

## Acceptance criteria

- [ ] Tileset inventoried (file structure + unique-tile-variant counts for floor/wall/props)
- [ ] License verified at vendor terms URL (commercial-use clause captured)
- [ ] Viability test fixture built at canonical script location
- [ ] Pixi.js BaseTexture load + `SCALE_MODES.NEAREST` enforcement applied
- [ ] Three room dimension band renders (720×720 + 1440×1440 + 2160×2160)
- [ ] Screenshots produced for gandalf inspection (4 PNG files including optional parallax-fog overlay)
- [ ] Per-band assessment (floor + wall + prop + register + seam + substrate alignment)
- [ ] Recommendation (PASS / CONDITIONAL / FAIL with specific rationale)
- [ ] Substrate-alignment notes (Reaper as generic dark/somber dungeon for VS2a canonical-four runtime)
- [ ] Tag `drax/v0.20.8-reaper-tileset-viability-vs2a` cut
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended to this dispatch file
- [ ] Knight-rider notified with: tag hash, screenshot paths, recommendation, substrate-alignment assessment, unique-tile-variant counts, license verification result, any unanticipated findings

## Tag policy

- **Intermediate tag:** `drax/v0.20.8-reaper-tileset-viability-vs2a`
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-17
**Unique-tile-variant counts:** floor 141 total (19 usable as solid fill) / wall 659 combined (A2=420 + A4=239) / props N/A (B tileset not ingested in viability test; vendor RM B shows ~20+ props: tombstones, dead trees, skull pillars, altars, crystal balls, candelabras, archways, pedestals — rich prop inventory confirmed by visual inspection)
**License verification:** Commercial use PERMITTED (no attribution required for purchased tilesets; attribution optional but appreciated). Key restrictions: cannot redistribute assets independently; no AI/NFT/blockchain use; editing for own game is freely permitted. Source: https://kokororeflections.com/terms-use/ verified 2026-05-17.
**Recommendation:** CONDITIONAL
**Recommendation rationale:**
  The Reaper tileset renders a credible dark/somber dungeon interior at all three VS2a room dimension bands. Floor/wall contrast is strong (floor mean ~135, wall mean ~35, ratio ~4:1). Variety floors all PASS. Parallax-fog assets add effective atmospheric depth. The tileset CLEARS the substrate-alignment bar (reads as tomb/cursed sanctum at VS2a canonical-four runtime without shadow substrate). The CONDITIONAL flag is for one specific gap: the A1 floor tile selection produces only 19 usable solid-fill center tiles from 141 unique in the autotile expansion. At the default 30m band (676 floor tiles placed), these 19 tiles cycle and produce a faint repetition pattern that is visible on close inspection, though not jarring at normal gameplay viewport scale. Two paths clear this condition: (a) supplement with a small number of A2 interior tiles as floor accents to break monotony — the A2 sheet has varied floor-compatible tiles; or (b) use the full autotile expansion with proper neighbor-aware tile selection at Track D integration time (the autotile transitions ARE designed for varied floor fill; the viability test used conservative solid-fill-only selection to avoid edge-piece artifacts). Either path is Track D scope. Viability test itself does NOT need re-run before Track D dispatch is authored; the CONDITIONAL is Track D's implementation constraint, not a gate on VS2a selection.
**Substrate alignment:** Works as generic dark/somber dungeon for VS2a canonical-four runtime WITHOUT requiring shadow substrate activation. The Reaper aesthetic (near-black walls, blue-gray stone floor with white geometric ornamental borders, parallax fog) maps cleanly to tomb / death palace / cursed sanctum season framing. DOES NOT require shadow substrate to read correctly. DOES strongly suggest shadow substrate as its canonical Phase-1 P1 home (per substrate-expansion-decision-2026-05-17.md; shadow substrate is exactly this aesthetic). VS2a ships on canonical-four; the Reaper theme works within that constraint as a generic "dark dungeon" season environment.
**Screenshot paths:**
- `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/screenshots/reaper-viability-small-720.png`
- `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/screenshots/reaper-viability-default-1440.png`
- `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/screenshots/reaper-viability-large-2160.png`
- `/Users/admin/Games/reincarnated-demo/scripts/reaper-viability-test/screenshots/reaper-viability-with-parallax-fog.png`
**Intermediate tag:** `drax/v0.20.8-reaper-tileset-viability-vs2a @ 6cd46d8`
**Tests status:** 326/326 passed; tsc --noEmit clean; vite build clean (520 modules)
**Notes for knight-rider:**
  1. LICENSE: Commercial use is fully clear. No attribution required for purchased tilesets (vendor terms explicitly state attribution optional). No redistribution of raw assets; embed-only constraint is standard and non-blocking for game delivery.
  2. UNIQUE TILE COUNTS: The vendor's note about duplicates is accurate. A4 has 239 unique tiles from 931 cells (74% unique). A2 has 420 unique from 1092 cells (62% unique). A1 has 141 unique from 931 cells (15% of cells are unique; 66% of cells are empty/transparent). The non-rm-square format wastes space intentionally for usability (per vendor README). Actual tile variety available for composition is high: 659 wall tiles + 141 floor tiles.
  3. FLOOR TILE SELECTION NUANCE: The A1 autotile expansion's 141 unique tiles break down as: 13-19 solid center-fill tiles (confirmed by quadrant-variance analysis) + 128 edge/transition variants. The viability test used the center-fill tiles conservatively. Track D integration should implement neighbor-aware autotile selection to use the full 141 tiles correctly — this is the standard autotile implementation pattern and will produce markedly better floor variety and natural-looking boundaries.
  4. PROPS: The vendor B tileset (reaper_B.png) contains rich dungeon props — tombstones, dead trees, skull pillars, altars, crystal balls, candelabras, archways, pedestals — visually confirmed from vendor sample map img/tilesets/reaper_B.png. These are NOT ingested in this viability test (out of scope). Track D prop placement work should evaluate these for interior room decoration.
  5. PARALLAX FOG: fogblack.png (1000x1000 RGBA) applies well as atmospheric overlay at 25% opacity. Adds depth without obscuring tile detail. fogwhite.png is the inverted version (white fog for different room atmosphere). Parallaxes_3.png (768x768) is a combined layered fog asset. All three are viable for VS2a atmospheric layering.
  6. ANIMATED TILES: The A1 sheet contains what appears to be a water/liquid autotile section (the vertical stripe pattern in the RM A1 source; mean brightness ~70-100, high vertical regularity). These are out of scope for VS2a (static environments per gandalf commission). Do not use the water animation section for floor fill.
  7. RECOMMENDATION OPERATIVE FRAMING: CONDITIONAL is NOT a soft FAIL. The tileset clears the aesthetic, variety, contrast, substrate-alignment, and license bars. The CONDITIONAL is specifically the autotile-implementation detail that Track D's engineer (drax) needs to handle — use neighbor-aware tile selection for floor fill, not naive center-tile-only selection. Once Track D implements proper autotile, the Reaper tileset should render as a fully credible HD-2D-adjacent dungeon environment.
  8. DO NOT AUTO-FIRE Track D integration. The recommendation feeds gandalf Track B framework + Matt VS2a selection. Integration is downstream Track D dispatch.
