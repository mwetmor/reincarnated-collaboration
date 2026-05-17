# Dispatch — 2026-05-17 — drax — Foozle Lucifer Collection viability test (4 packs) for VS2a

**From:** knight-rider (authored per Matt directive 2026-05-17: "I loaded the four foozle tilesets into the tilesets folder for testing." — implicit commission for viability test analogous to prior Reaper dispatch)
**To:** drax
**Approved by:** Matt at 2026-05-17
**Status:** READY-TO-FIRE
**Estimated effort:** 3-4h (4 packs × tileset inventory + viability test fixture + 3-band render + screenshots + per-pack assessment + comparative assessment vs Reaper + tag)

**Gate-1 bypass rationale:** Matt-directed (explicit asset placement + implicit "for testing" commission); single-seam (drax demo render only); reversible (test fixture + screenshots; no production renderer changes); bounded scope (empirical viability test, NOT Track D integration); pattern-aligned with prior Reaper viability dispatch (v0.20.8 reference).

**Per-seam discipline note:** this is drax's fourth dispatch in-session (Case A + Case D + Reaper viability + this). Matt-authorized exception per scope-bounded + post-Reaper-warm-context + tightly-scoped empirical-test framing + Matt-implicit-commission. **Do NOT auto-fire follow-on integration work** after this returns; full Track D integration (per gandalf Drift-15 commission) is a separate downstream dispatch.

**Acceptance summary:** Four Foozle Lucifer Collection packs (Exterior + Dungeon + Desert + Lava; all 32×32 px native; CC0 free; placed at `public/tilesets/foozle/`) inventoried + loaded into minimal Pixi.js test fixture + rendered at three demo room dimension bands (720×720 / 1440×1440 / 2160×2160 px corresponding to 15m/30m/45m at 48 px/m) via 2× nearest-neighbor upscale to 64×64 px per tile (preserves pixel-art integrity; integer-upscale-only). Per-pack assessment + comparative assessment vs Reaper baseline (drax/v0.20.8). Per-pack screenshots produced for gandalf visual inspection. Recommendation per pack: PASS / CONDITIONAL / FAIL + comparative recommendation: Foozle-preferable / Reaper-preferable / use-both (per-season selection).

---

## Why this dispatch exists

Per legolas Mode B environment-tileset sweep return 2026-05-17: Foozle Lucifer Collection was characterized as **MODERATE** environment coverage, **RETRO** register (below HD-2D bar), **CC0 free** license, **strong free baseline candidates** especially Lucifer Dungeon + Lucifer Lava. Per Matt earlier scope-reduction reframe consideration: Reaper alone may be sufficient for VS2a, but Foozle provides 4 thematic ranges (exterior + dungeon + desert + lava) vs Reaper's 1 (death/undead palace) — potentially enabling per-season variety even at VS2a if 2+ Foozle packs are viable.

Reaper viability test (drax/v0.20.8) returned CONDITIONAL = PASS-for-VS2a; HD-2D-ADJACENT register confirmed. Foozle viability test (this dispatch) is the comparison baseline: how does CC0-free RETRO-register Foozle read at the same demo room dimensions? Is Foozle viable as an alternative (cost savings + thematic variety) or as a complement (per-season pack selection)?

## Cross-seam contract change?

**Round-trip: not applicable** — test fixture only; no production renderer changes; no schema changes; no other seam consumes the test fixture output. Screenshots feed gandalf visual inspection + Matt VS2a selection (out-of-band). Per R11(b) Principle 6.

## What's on disk (pre-verified by knight-rider)

`/Users/admin/Games/reincarnated-demo/public/tilesets/foozle/` contains 4 pack subdirectories:

### Pack 1 — Foozle_2DT0002_Lucifer_Exterior_Tileset_Pixel_Art
- `Ase/` — aseprite source files
- `Png/` — PNG tileset exports (USE THIS for Pixi.js)
- `Exterior Tileset Mockup.png` — 600KB vendor mockup (visual reference)
- `Readme.txt` — license + usage notes

### Pack 2 — Foozle_2DT0003_Lucifer_Dungeon_Tileset_Pixel_Art
- `Ase/` — aseprite source files
- `Png/` — PNG tileset exports (USE THIS for Pixi.js)
- `DungeonTileset Mockup.png` — 397KB vendor mockup (visual reference)
- `Readme.txt`

### Pack 3 — Foozle_2DT0010_Lucifer_Desert_Tileset_Pixel_Art
- `Desert Tileset.png` — main tileset PNG (63KB; flat structure, no Png/ subfolder)
- `Desert Tileset.aseprite` — aseprite source
- `Animated Tiles/` — animated tile assets (sand wave, etc.)
- `Readme.txt`

### Pack 4 — Foozle_2DT0011_Lucifer_Lava_Tileset_Pixel_Art
- `LavaDungeonTileset.png` — main tileset PNG (25KB; flat structure)
- `LavaDungeonTileset.aseprite` — aseprite source
- `LavaMockup.png` — 37KB vendor mockup
- `Animated Tiles/` — animated tile assets (lava flow, etc.)
- `Readme.txt`

**License (pre-verified via legolas Mode B):** CC0 (public domain dedication). No restrictions; commit-OK; post-OK; no attribution required (though optional). Verify per Readme.txt during dispatch.

**Native tile size:** 32×32 px per Foozle convention (vs our PIXELS_PER_METER=48 anchor). Render-strategy below.

## Scale-handling strategy

Foozle native is 32×32 px. Our convention is 48 px/m. Three options considered; recommendation locked:

- **Option A (RAW 32×32):** render Foozle at native; 720px room = 22.5 tiles per side (non-integer; awkward). REJECTED.
- **Option B (1.5× to 48×48):** matches PIXELS_PER_METER convention exactly; but 1.5× is non-integer scale = aliased pixels = bad for pixel-art. REJECTED.
- **Option C (2× to 64×64):** integer nearest-neighbor upscale; preserves pixel-art integrity; tiles render at 64 px per tile = 64 px/m effective at room scale. Room dimensions stay in our convention (720/1440/2160 px); per-pixel density is 32 source px per 1m. **CHOSEN.**

Document the scale-shift implication in completion record: if Foozle is adopted for VS2a, room-scale interpretation shifts from "48 px/m for everything" to "48 px/m for chierit + 64 px/m effective for Foozle tiles" — a forward-flag for Track D integration but does not affect viability assessment.

## What this dispatch produces

### Track 1 — Per-pack inventory + license verification

For each of the 4 Foozle packs:
- File structure (which PNG is the authoritative source; presence of mockup PNG for visual reference)
- Tileset PNG dimensions (raw px × px)
- **Unique-tile-variant counts** for floor + wall + props (vendor packs may include duplicates or scenic-only tiles; empirical count is what matters per legolas Mode B tile-variety floor heuristics)
- Animated-tile contents (Desert + Lava packs; static frame inspection only — animation rendering out of scope)
- License confirmation per Readme.txt (CC0 per legolas; verify)
- Mockup PNG inspection (vendor's own composition examples; inspirational reference only — do NOT copy compositions)

### Track 2 — Viability test fixture

Build minimal Pixi.js test fixture at `/Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/` or analogous location:

- Load 4 packs' authoritative PNG tilesets as Pixi.js BaseTextures
- Use `SCALE_MODES.NEAREST` (HARD REQ; pixel-art convention from Case A/D/Reaper)
- Slice native tiles at 32×32 px; render at 2× upscale = 64×64 px per tile
- Render sample compositions filling each of three demo room dimension bands per pack:
  - **Small (720×720 px):** 720/64 = 11.25 tiles per side → 11×11 = 121 tile cells with 16-px residual (display + center)
  - **Default (1440×1440 px):** 1440/64 = 22.5 → 22×22 = 484 cells with 32-px residual
  - **Large (2160×2160 px):** 2160/64 = 33.75 → 33×33 = 1089 cells with 48-px residual
- Each band per pack INDEPENDENT (per gandalf commission Amendment 3 — no multi-room coherence engineering)
- Tile-selection strategy: use reasonable floor + wall variety to avoid obvious-repetition tiling artifact. If variant counts below legolas tile-variety floor heuristics (≥4 / ≥8 / ≥12 for small/default/large), document the gap per pack.
- Wall composition: render at least one full room boundary per pack so seam-behavior is visible.

**Total renders: 4 packs × 3 bands = 12 screenshots minimum** + optional comparison composite.

### Track 3 — Screenshot output for gandalf inspection

Capture screenshots per pack at each room dimension band. Place in `/Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/` or analogous:

- `foozle-exterior-small-720.png` / `foozle-exterior-default-1440.png` / `foozle-exterior-large-2160.png`
- `foozle-dungeon-small-720.png` / `foozle-dungeon-default-1440.png` / `foozle-dungeon-large-2160.png`
- `foozle-desert-small-720.png` / `foozle-desert-default-1440.png` / `foozle-desert-large-2160.png`
- `foozle-lava-small-720.png` / `foozle-lava-default-1440.png` / `foozle-lava-large-2160.png`
- (Optional) `foozle-vs-reaper-default-comparison.png` — side-by-side at default 1440 band: Foozle Dungeon vs Reaper for direct comparative assessment

Screenshots are the load-bearing artifact for gandalf visual inspection — make them clear, well-framed, representative of VS2a player viewport experience.

### Track 4 — Per-pack assessment

For each of 4 packs, document in completion record OR companion notes file:

- **Floor coverage:** does the floor look reasonable without obvious repetition tiling artifact at each band?
- **Wall coverage:** does the wall boundary render credibly as room edge?
- **Visual register:** does it READ as HD-2D-quality OR retro/low-fidelity? **Be honest** — legolas characterized Foozle as RETRO register; quantify visually how retro at demo viewport scale (does it read as "Stardew-class retro" or "acceptable-pixel-art-just-not-HD-2D"?).
- **Seam behavior:** do adjacent tiles compose without visible seams?
- **Thematic distinctness:** does the pack feel like its theme (Exterior reads as exterior; Dungeon reads as dungeon; Desert reads as desert; Lava reads as lava)?
- **Substrate alignment:** which canonical substrate(s) does this pack visually serve? Per gandalf substrate-expansion doc commit `1df535b`:
  - Exterior → wind / earth / generic-outdoor?
  - Dungeon → generic-dark (no substrate-specific) / shadow?
  - Desert → fire / earth?
  - Lava → fire / lightning?
  - Surface canonical-substrate mapping per pack as design-input for Track B framework

### Track 5 — Comparative assessment vs Reaper (drax/v0.20.8)

In completion record:
- **Foozle Lucifer Dungeon vs Reaper as "default dungeon" tileset:** which reads better at default 1440 band? Visual register comparison. Substrate-alignment comparison (Reaper = shadow-substrate-coherent; Foozle Dungeon = generic-dark).
- **Per-season variety advantage:** 4 Foozle packs (4 thematic ranges) vs 1 Reaper (1 theme) — if Foozle viable, Matt could pick per-season pack from 4-pack roster vs Reaper's single-theme constraint
- **Cost comparison:** Reaper $9.99 paid (CONDITIONAL = PASS-for-VS2a) vs Foozle 4 packs $0 CC0 — cost advantage to Foozle
- **License comparison:** Reaper embed-only constraint (Kokoro license) vs Foozle CC0 no-restriction — Foozle wins on flexibility (can commit to public repo; no gitignore needed)

### Track 6 — Recommendation

In completion record:

**Per-pack:**
- PASS / CONDITIONAL / FAIL per Foozle pack with specific rationale

**Comparative:**
- **Foozle-preferable** (use 1+ Foozle packs for VS2a; deprecate Reaper acquisition)
- **Reaper-preferable** (Reaper's HD-2D-adjacent register beats Foozle's retro register; Foozle stays as fallback baseline)
- **Use-both** (per-season pack selection: Reaper for darkness-theme seasons, Foozle packs for other thematic ranges)

Recommendation goes to gandalf (for Track B framework consumption) + Matt (for VS2a selection). Do NOT execute integration; that's downstream Track D.

### Track 7 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.20.9-foozle-lucifer-tilesets-viability-vs2a`
- AGENT_STATE.md updated
- Completion record appended to this dispatch file
- Knight-rider notified with: tag hash, screenshot paths (12+), per-pack recommendations, comparative recommendation, per-pack unique-tile-variant counts, license verification result per pack, scale-shift implication note for Track D

## Out of scope (explicit)

- **NO full room/hallway renderer extension** (Track D per gandalf Drift-15 commission)
- **NO animated tile rendering** (Phase 0 ships static per gandalf commission framing; Desert + Lava packs have animated assets but render static frames only for viability assessment)
- **NO multi-room-coherent tile-family hunting** (per Amendment 3)
- **NO substrate-expansion runtime activation** (Phase-1 P1; VS2a stays canonical-four)
- **NO seasonal-vocabulary pool-composition matching** (separate workstream when VS2a season selection happens)
- **NO new dispatch authoring** for other tilesets / vendors after this returns
- **NO Track B framework authoring** (gandalf-seam; next session)
- **NO Reaper re-test** (already passed at v0.20.8; comparative-only here)

## Required reading

- **Reaper viability dispatch + completion record:** `agentic_orchestration/dispatches/2026-05-17-drax-kokoro-reaper-tileset-viability-vs2a.md` (methodology pattern; comparison baseline; key findings — 141 A1 floor variants + 659 wall variants + CONDITIONAL = PASS-for-VS2a)
- **Legolas Mode B scout doc:** `agentic_orchestration/research/catalogue/environment-tileset-vendor-scout-2026-05-17.md` (Foozle findings; "MODERATE coverage" / "Retro register" / "Free CC0" / "Lucifer Dungeon + Lava Dungeon strong baseline candidates")
- **Legolas Mode B JSONL:** `agentic_orchestration/research/catalogue/environment-substrate-inventory-2026-05-17.jsonl` (per-pack JSONL schema fields)
- **Gandalf environment commission:** `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` (Drift-15 framing; Amendment 3 each-room-independent)
- **Gandalf substrate-expansion design doc:** `canonical/story/substrate-expansion-decision-2026-05-17.md` (commit `1df535b`; lightning/holy/shadow substrate naming; canonical-four-bound runtime for VS2a/VS2b — Foozle substrate-alignment per pack is design-input for Track B framework)
- **Arena topology:** `canonical/story/arena-room-hallway-system.md` (15m/30m/45m room dimensions; PIXELS_PER_METER=48 anchor; note scale-shift implication for Foozle 32px→64px upscale)
- **Style register:** `canonical/story/style-register.md` (HD-2D Candidate B lock — assess honestly whether Foozle clears or fails this register)
- **Foozle Readme.txt files per pack** (license confirmation; usage notes)
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #2 smoke-test, #10 empirical inspection over assumption

## Acceptance criteria

- [ ] All 4 Foozle packs inventoried (file structure + unique-tile-variant counts + license verification)
- [ ] Viability test fixture built at canonical script location with 2× upscale (32→64 px per tile)
- [ ] Pixi.js BaseTexture load + `SCALE_MODES.NEAREST` enforcement applied
- [ ] 12 screenshots produced (4 packs × 3 bands) + optional comparison screenshot
- [ ] Per-pack assessment (floor + wall + register + seam + thematic-distinctness + substrate-alignment)
- [ ] Per-pack recommendation (PASS / CONDITIONAL / FAIL with rationale)
- [ ] Comparative assessment vs Reaper baseline (visual register + variety + cost + license dimensions)
- [ ] Comparative recommendation (Foozle-preferable / Reaper-preferable / use-both with rationale)
- [ ] Scale-shift implication note (Foozle 64 px/m effective vs chierit 48 px/m baseline) for Track D forward-flag
- [ ] Tag `drax/v0.20.9-foozle-lucifer-tilesets-viability-vs2a` cut
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended to this dispatch file
- [ ] Smoke (existing 326/326 tests stay green; `tsc --noEmit` clean; `vite build` clean)
- [ ] Knight-rider notified with: tag hash, screenshot paths, per-pack + comparative recommendations, per-pack tile-variant counts, license verification, scale-shift note, any unanticipated findings

## Tag policy

- **Intermediate tag:** `drax/v0.20.9-foozle-lucifer-tilesets-viability-vs2a`
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-17
**Per-pack unique-tile-variant counts (empirical, from source PNG at 32px cell):**
- Exterior: 226 unique total (165 floor+wall autotile region / 61 props region)
- Dungeon:  81 unique total (6 floor / 22 wall / 46 props)
- Desert:   269 unique total (30 floor / 100 wall+structure / 56 props)
- Lava:     122 unique total (6 floor / 18 wall / 6 lava-fill / ~96 props)

**License verification:** CC0 confirmed all 4 packs. Public domain (CC0 1.0 Universal).
  No restrictions. No attribution required. Authored by Baldur, distributed by Foozle.
  Commit-OK, post-OK, embed-OK, no gitignore needed (contrast: Reaper embed-only restriction).

**Tiles loaded for render (filtered, 64px rendered = 2x upscale):**
- Exterior: 154 floor, 152 wall (note: region overlap — same autotile blocks used for both)
- Dungeon:  6 floor, 7 wall
- Desert:   30 floor, 63 wall
- Lava:     4 floor, 12 wall, 8 lava-fill

**Variety heuristic status (legolas Amendment 2 floors: ≥4/≥8/≥12 small/default/large):**
- Exterior: all bands PASS (floor 154, wall 152 — far exceeds all floors)
- Dungeon:  small PASS/PASS; default floor FAIL (6<8); large floor FAIL (6<12) + wall FAIL (7<8)
- Desert:   all bands PASS (floor 30, wall 63 — exceeds all floors)
- Lava:     small PASS/PASS; default floor FAIL (4<8)/wall PASS; large floor FAIL (4<12)/wall PASS

**Per-pack recommendations:**

- Exterior: CONDITIONAL — Rich autotile variety (226 unique tiles) and earth/wind substrate
  alignment are strong. However: the autotile blocks contain both center-fill tiles and
  transition/edge tiles. The current render pulls all autotile types as floor fill, producing
  a visually chaotic patchwork that reads as incorrect (transition pieces placed as interior
  fill). A Track D autotile-aware renderer must select center-of-block tiles only. If that
  selection logic is implemented, Exterior becomes viable and potentially the strongest Foozle
  pack for outdoor seasons. Deferred to autotile-aware Track D pass.

- Dungeon: CONDITIONAL — Small band (720px) renders cleanly. Six floor variants adequate for
  small rooms; dark brick wall (7 tiles) reads immediately as dungeon boundary. Floor
  repetition artifact visible at default band and worsens at large. The pack IS the
  legolas-highlighted "strong baseline candidate" but its flat tile variety is the limiting
  factor. Supplement floor to 10+ unique tiles (possible via broader brightness filter or
  manual floor region expansion) and it clears for small/default. Shadow / generic-dark
  substrate alignment strong.

- Desert: PASS — Strongest pack in the collection. 30 floor tiles (all heuristics pass), 63
  wall tiles, thematic clarity immediate (sandy floor + dark stone/wood wall structures reads
  as arid dungeon/encampment). Earth / fire (arid desert) substrate alignment clear. The
  floor has visible texture variation (lighter tiles, wind-scratch pattern) that breaks
  repetition. Wall variety at all three bands is credible without obvious repetition. This
  is the one Foozle pack ready for Track D as-is.

- Lava: CONDITIONAL — The wall (12 tiles, charcoal cobbled stone) is the strongest element
  in this pack: renders cleanly at all bands, dark and thematic, fire/lightning aligned. The
  lava-fill tiles (8 unique, yellow-orange lava) are visually compelling and would work as
  hazard accent or floor variant. The floor region (4 tiles) is critically thin and the
  source region overlaps with architectural elements (hatch/gate objects pulled into floor
  fill in the render). Manual tile isolation needed in Track D. The pack's lava-fill
  capability makes it uniquely thematic for fire/lightning seasons — no other Foozle pack
  provides this.

**Comparative recommendation (Foozle vs Reaper): USE-BOTH (per-season pack selection)**

Rationale: Reaper and Foozle serve different thematic ranges with non-overlapping substrate
alignment, different register levels, and different licensing postures.

- Reaper (HD-2D-adjacent, shadow substrate, $9.99 Kokoro, embed-only):
  Use for darkness/shadow/death-themed seasons. Highest visual quality in the current
  tileset roster. Floor variety (19 solid-fill tiles from A1) and wall variety (659 unique)
  exceed all Foozle packs at the HD-2D register. The comparison screenshot makes the quality
  gap concrete: Reaper tiles have sub-tile atmospheric depth; Foozle tiles are clean
  pixel-outlined flat-fill. For VS2a quality bar, Reaper is the primary dungeon tileset.

- Foozle Desert (PASS, earth/fire, CC0):
  Best Foozle pack. Ready for Track D as-is. Thematic range Reaper cannot cover (desert /
  arid outdoor encampment). Per-season selection: fire/earth seasons in open arena setting.

- Foozle Lava (CONDITIONAL, fire/lightning, CC0):
  Unique lava-fill capability. Requires Track D floor isolation fix. When fixed, provides
  per-season variety for fire/lightning lava dungeon seasons that Reaper cannot cover.

- Foozle Dungeon (CONDITIONAL, shadow-lite, CC0):
  Viable as low-cost fallback dungeon tileset if Reaper is not available. Not competitive
  with Reaper on visual register but workable for small rooms.

- Foozle Exterior (CONDITIONAL, earth/wind, CC0):
  Deferred until autotile-aware Track D renderer implemented. High potential once center-only
  tile selection is working; currently produces chaotic renders.

Foozle-preferable is NOT supported: Reaper's HD-2D-adjacent register is clearly superior in
the comparison screenshot. Reaper-preferable is NOT supported: Foozle provides 4 thematic
ranges (outdoor/dungeon/desert/lava) Reaper cannot cover. USE-BOTH is the correct answer.

**Substrate-alignment per pack:**
- Exterior: earth (outdoor grassland stone) / wind (open sky outdoors) / generic-outdoor
- Dungeon:  shadow / generic-dark (no substrate-specific light source; works as canonical-dark)
- Desert:   earth (arid, sandy, dry stone) / fire (hot climate, sun-scorched)
- Lava:     fire (lava flows, heat hazard) / lightning (metallic pipe structures, industrial)

**Visual register assessment (honest, per dispatch requirement):**
Foozle reads as "acceptable pixel-art — not HD-2D". This is above Stardew-class retro:
tiles have clean outlines, intentional color palettes, and contextual texture variety.
But it does not reach HD-2D-adjacent. The visual gap from Reaper is primarily:
(1) Sub-tile texture density — Reaper has 3-5 distinct texture zones per tile; Foozle
    has 1-2 solid-fill regions with pixel outlines.
(2) Atmospheric shadow/depth — Reaper tiles imply a light source via gradient shading;
    Foozle tiles are flat with outline-only depth cues.
(3) Tile border articulation — Reaper seams include subtle transition blending; Foozle
    seams are hard outline-to-outline (visible grid lines at 64px upscale).
The comparison screenshot (foozle-vs-reaper-default-comparison.png) makes this concrete.
At VS2a, Foozle is acceptable as a free baseline. For VS2b or release, Reaper's register
is the target.

**Scale-shift implication note for Track D:**
Foozle native 32px × 2x upscale = 64px rendered per tile = 64 px/m effective.
Chierit (character sprite) operates at 48 px/m baseline (PIXELS_PER_METER=48).
Mixed-scale environment-plus-character compositing requires Track D resolution:
Option A: render Foozle environment at 64px, rescale chierit viewport to 64px/m.
Option B: render Foozle at 48px (non-integer 1.5x — REJECTED; aliased pixels).
Option C: accept mixed-scale (environment at 64px grid, character at 48px origin) with
          explicit viewport offset logic.
This is a forward-flag only; Track D dispatch decides. Do NOT resolve here.

**Screenshot paths (13 total):**
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-exterior-small-720.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-exterior-default-1440.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-exterior-large-2160.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-dungeon-small-720.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-dungeon-default-1440.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-dungeon-large-2160.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-desert-small-720.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-desert-default-1440.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-desert-large-2160.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-lava-small-720.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-lava-default-1440.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-lava-large-2160.png
- /Users/admin/Games/reincarnated-demo/scripts/foozle-viability-test/screenshots/foozle-vs-reaper-default-comparison.png

**Intermediate tag:** drax/v0.20.9-foozle-lucifer-tilesets-viability-vs2a @ 0e4599b
**Tests status:** 326/326 passed (unchanged)
**Build smoke:** tsc --noEmit clean; vite build clean (520 modules)

**Notes for knight-rider:**
- USE-BOTH is the comparative recommendation. Reaper owns the HD-2D-adjacent shadow/dark
  register. Foozle Desert is the strongest free alternative and ready for Track D integration.
  Foozle Lava is the most thematically unique (lava-fill capability) but needs Track D floor
  fix. Foozle Exterior has the most raw variety but needs autotile-aware tile selection.
- The comparison screenshot (13th, side-by-side) makes the register gap concrete. Recommend
  gandalf review that image first when making VS2a selection.
- All 4 Foozle Readme.txt files confirm CC0 explicitly. No gitignore needed for Foozle
  (contrast: Reaper is gitignored per embed-only license constraint).
- Foozle Desert = PASS; no blocker for Track D as-is. Other packs = CONDITIONAL with
  specific documented gaps. Track D dispatch should scope to Desert first if timeline is
  tight, then add Lava/Dungeon with the documented fixes.
- Scale-shift (Foozle 64px/m vs chierit 48px/m) is the load-bearing Track D pre-work item.
  Must be decided before any environment-plus-character composite render in Track D.
