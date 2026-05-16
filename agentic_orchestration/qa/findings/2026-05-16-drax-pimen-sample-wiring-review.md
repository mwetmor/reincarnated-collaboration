# Finding — 2026-05-16 — drax wiring-track Pimen sample review

**Reviewer:** drax
**Severity:** PASS WITH FLAGS
**Target:** Legolas Pimen sample (20 rows, `research/catalogue/pimen/sample-2026-05-16.json`)
**Track:** wiring (viability-gate, one of three)

---

## Verdict (one line)

Pimen assets are wirable with a mandatory RAR-unpack step in the ingest pipeline, acceptable frame-layout variance, and no character/enemy decomposition blocker for the demo's current rendering approach — full crawl is greenlit on the wiring track with the flags documented below.

---

## Per-criterion assessment

### 1. Pixi.js consumption viability (PNG vs RAR-archive vs sprite-sheet vs Aseprite)

**RAR is the dominant delivery format: 15 of 20 rows (75%) include a RAR archive.** The remaining 5 rows (holy-spell-effect, dark-spell-effect, acid-spell-effect, mega-pack-elemental-spell-effects, battle-vfx-hit-spark) ship PNG directly with no RAR container.

Pixi.js cannot consume RAR at load time. This is not a hard blocker — it is a pipeline-stage requirement. The RAR must be unpacked during or after download, before the PNG files reach the loader. The PNG payload inside every RAR is standard PNG (rows 1–17, 19 all confirm PNG content). Once unpacked, Pixi.js `Assets.load()` handles them without modification.

RAR usage appears consistent and Pimen-wide, not asset-specific. The free packs and paid packs both use RAR. The no-RAR packs (rows 7, 8, 15, 18, 20) are the higher-cost tier-04+ packs and the mega-bundle — this may reflect a Pimen packaging convention where the premium tier ships without archive wrapping, but the sample is too small to confirm. **Do not assume RAR is absent for paid packs — rows 2, 4, 6, 10, 12, 14 are paid and RAR-packaged.**

**FLAG 1 (must-have): RAR-unpack step required in ingest pipeline.** This is a pipeline adaptation, not a demo-side code change. The demo's loader.ts operates on pre-ingested assets (fetches via `/seasons/<id>/` path). The unpack step belongs in elrond's curation pipeline or in a separate asset-prep script that runs at catalogue-ingest time. Estimated cost: see Operational cost section.

**Pixi.js loader compatibility for the PNG payload:** confirmed compatible. The demo's current `fetchJson` / static-asset pattern in loader.ts targets JSON engine output, not sprite assets directly. Sprite assets will be consumed by Pixi.js `Assets.load()` in the demo's rendering layer when VFX playback is integrated. PNG is fully supported.

---

### 2. Sprite-sheet shape consistency

**Three distinct frame-delivery modes are present in the sample:**

- **Pre-baked spritesheet only:** rows 3 (magical-water-effect), 19 (buff-n-debuff). Spritesheet ships; no individual frames.
- **Spritesheet + individual frames:** rows 6 (ice-spell-effect-02), 7 (holy), 8 (dark), 15 (acid), 18 (mega-pack), 20 (battle-vfx-hit-spark). Both included — consumer can choose the form that fits the loader.
- **Individual frames only (no spritesheet):** row 5 (ice-spell-effect-01). Confirmed in extraction_notes: "distributed as individual PNG frames rather than spritesheet — implies consumer must assemble spritesheet." No spritesheet included.
- **Format ambiguous (PNG only, RAR-packaged, no explicit sheet/frame distinction):** rows 1, 2, 4, 9, 10, 11, 12, 13, 14, 16, 17. The RAR contents could be a spritesheet, individual frames, or both. Visual inspection post-download is required to confirm layout.

**Canvas size variance — non-square shapes present:**
- dark-spell-effect: 32x48, 72x32 (non-square; these require canvas-padding when loading into a Pixi.js texture atlas that assumes uniform cell dimensions)
- buff-n-debuff-vfx-pack-01: 48x64 (portrait-oriented; taller than wide)
- holy-spell-effect VFX3: 64x80 (tall-canvas)
- acid-spell-effect: ranges 16x16 to 72x80
- water-spell-effect-03: Water Mine 96x64, Water Beam 96x48 (narrative-pixel outliers within a hd2d-pixel pack)
- wind-spell-effect-03: Spin Attack 64x48 within a primarily 32x32 pack

**Mixed canvas sizes within a single pack are the norm, not the exception.** Most packs have a primary canvas size with outliers (e.g., fire-spell-effect-3 is primarily 32x32 with 64x64 large effects and 16x16 small effects). This is standard VFX practice — impact effects are smaller, screen effects are larger.

**FLAG 2 (nice-to-have): Animation loader must handle non-uniform cell sizes per animation, not per pack.** A per-pack single-cell-size assumption will break on dark-spell-effect and others. The loader needs per-animation canvas metadata (which the sample's `frame_count_notes` field provides for the paid tier packs, but is `unknown` or inferred for the free packs). Elrond's curation should surface explicit canvas dimensions per animation where available; the sample already does this well for paid packs.

The individual-frames-only case (ice-spell-effect-01) requires an additional build step: frame PNGs must be assembled into a spritesheet before Pixi.js texture atlas loading. The Pixi.js `Assets.load()` API does not accept a directory of sequentially numbered PNGs as an animation — it expects either a spritesheet JSON descriptor or a `TextureAtlas`. This is a one-time asset-prep step per pack.

**FLAG 3 (must-have for individual-frame-only packs): Frame-assembly step needed for packs that ship individual frames without a spritesheet.** In this sample, only ice-spell-effect-01 is confirmed individual-frames-only; the ambiguous-format packs may contribute more at full crawl.

---

### 3. Decomposition sufficiency

**Category distribution in the 20-row sample:**
- `vfx`: 17 rows — decomposition `not-applicable` for all (correct; VFX sprites don't have body/head/weapon layers)
- `enemy`: 1 row (fantasy-skeleton-enemies) — decomposition `monolithic`
- `character`: 1 row (fantasy-platformer-character) — decomposition `monolithic` (inferred)
- `vfx` with bundled enemy character: 1 row (earth-spell-effect-03) — decomposition `unknown` for the bundled Earth Elemental enemy

**VFX decomposition: clean.** Not-applicable is the correct tag for VFX sprites. No rigging concern — VFX run as baked animation sequences, not articulated rigs.

**Character/enemy decomposition: monolithic confirmed for the two explicit character/enemy rows.** Per the skeleton-enemies extraction_notes: "body/head/weapon are baked together. Not separable without manual slicing." The platformer character is also monolithic (inferred from listing format).

**Monolithic character sprites are compatible with the demo's current rendering approach** — the Pixi.js demo does not currently implement layer-separated character rigs. Enemy and character sprites play as baked texture sequences. Monolithic is the expected format for this integration level. If the demo later needs layer-separated rendering (e.g., weapon-swap on character sprites), Aseprite source files would be needed — none are included with the character packs in this sample.

**Projection to full crawl:** If the 17:3 VFX-to-character ratio holds (85% VFX), decomposition concerns are negligible at scale. Pimen's catalogue appears heavily VFX-dominant. The monolithic character/enemy assets are usable as-is for the demo's baked-animation renderer.

**FLAG 4 (informational — no action required now): The one `unknown` decomposition row (earth-spell-effect-03) bundles an enemy character inside a VFX pack.** The Earth Elemental enemy's decomposition is unknown. Elrond's curation should resolve this during the manual-review pass. Given Pimen's consistent monolithic pattern across other character assets, `monolithic` is the working assumption, but visual inspection of the actual sprite file is needed to confirm.

---

### 4. Format compatibility — Aseprite + other non-standard formats

**Aseprite source files present in 2 of 20 rows:**

- **mega-pack-elemental-spell-effects** (row 18): "PNG spritesheet + individual frames + Aseprite source files, elemental icons included." This is the $12.75 bundle of 9 element packs. Aseprite files are included in addition to PNG.
- **battle-vfx-hit-spark** (row 20): "PNG spritesheet + Aseprite source files (.aseprite)." The extraction_notes flag this as a wiring advantage — Aseprite layers enable per-layer color tint / palette variant swap without re-exporting the full spritesheet.

**Aseprite (.aseprite) files cannot be loaded directly by Pixi.js or served by the React/Vite loadout app.** They require export-to-PNG (via Aseprite CLI `--export` or batch export) before consumption. However, both Aseprite-containing rows also ship PNG spritesheets. The demo and loadout app can ignore the Aseprite files and consume the PNG directly. The Aseprite files are an optional enhancement path (layer-editing, palette variants) — not a requirement for basic display.

**No other non-standard formats observed in the sample.** No SVG, no GIF, no MP4, no WebP. The format surface is PNG (in various delivery modes) + RAR archive container + Aseprite source (in 2 rows). This is a narrow, manageable format set.

**FLAG 5 (nice-to-have): Aseprite source files should be preserved in the curation pipeline's asset storage even if the demo doesn't consume them now.** When palette-swap or layer-editing capability is needed in the demo (future VFX customization work), the Aseprite files are the correct source. Elrond should ensure curation does not discard the .aseprite files during asset-prep.

---

### 5. Loadout app consumption

The React/Vite loadout app's current architecture (`useSeasonData.ts`) consumes engine-generated JSON files via Vite's `import.meta.glob` at build time. It does not currently have a VFX preview pipeline, tooltip asset rendering, or gear-card sprite display. The loadout app's immediate consumption of Pimen assets is therefore limited to:

- **Static display of PNG thumbnails** (preview images, card art) — supported natively in React/Vite via `<img>` elements or CSS background.
- **Animated VFX tooltip previews** — not currently implemented. Would require either a Canvas/WebGL element (Pixi.js integrated into React, or plain Canvas2D) or an animated GIF/WebP export of the animation sequence. The raw PNG spritesheets are not natively playable in a React `<img>` tag.

**For the loadout app's current feature set**, Pimen assets are passively compatible. PNG thumbnails display fine. No loadout-side code change is required to display static previews if Legolas or elrond's pipeline produces a static preview thumbnail per asset.

**For future animated preview tooltips (not currently scoped)**, the loadout app would need either:
1. A pre-exported animated GIF or WebP per animation (can be produced from Pixi.js or ffmpeg during asset-prep), OR
2. A Pixi.js/Canvas integration component inside React (more complex; adds the Pixi.js dependency to the loadout stack)

**FLAG 6 (nice-to-have, future scope): Animated VFX previews in the loadout app require an asset-prep step to produce animated GIF or WebP thumbnails from the PNG spritesheet sequences.** The spritesheet → animated thumbnail conversion is a pipeline concern, not a loadout app code concern in the short term. Out of scope for full-crawl-release timing.

**React/Vite build compatibility:** PNG files served from Vite's public directory or imported as static assets are fully compatible. No compatibility issue with the React/Vite/Tailwind stack.

---

## Adaptation patches required

### Must-have (blocks full-crawl asset ingest)

**M1 — RAR-unpack step in ingest pipeline.** Before any Pimen asset can be loaded by Pixi.js or served to the loadout app, the RAR archive must be unpacked to extract the PNG payload. This step does not belong in the demo or loadout codebase — it belongs in elrond's curation pipeline or a standalone asset-prep script. The unpack step must be part of the Pimen ingest pipeline before the full crawl's asset files enter the demo's static asset directory or the loadout app's public folder.

**Ownership:** elrond (curation pipeline author). Drax is not the implementing agent for this step. Raising as a must-have because without it, the wiring from RAR-packaged Pimen assets to the demo is broken.

**M2 — Frame-assembly step for individual-frame-only packs.** Ice-spell-effect-01 ships individual PNG frames with no pre-baked spritesheet. Before these can be loaded by Pixi.js as an animation sequence, the frames must be assembled into a spritesheet + JSON descriptor (e.g., via TexturePacker or a script using Pixi.js CLI tools). Confirmed 1 of 20 rows in this sample; full crawl may surface more.

**Ownership:** elrond's ingest pipeline. Drax would configure the Pixi.js `Assets.load()` call to point at the assembled spritesheet once it exists.

### Nice-to-have (do not block full crawl)

**N1 — Per-animation canvas metadata in curated rows.** Non-uniform canvas sizes within packs (dark-spell-effect, holy-spell-effect, acid-spell-effect, etc.) mean the demo's animation loader needs per-animation dimensions, not per-pack dimensions. Elrond's curation should surface explicit canvas dimensions from `frame_count_notes` into structured fields where available. Currently the sample captures this in free-text; structured fields would allow programmatic loader config.

**N2 — Aseprite source file preservation.** Elrond's asset-prep pipeline should retain .aseprite files alongside the PNG exports (at minimum in cold storage). Do not discard them during prep.

**N3 — Animated thumbnail generation (future VFX previews in loadout).** Not needed for full-crawl-release. Document in `AGENT_STATE.md` as a deferred adaptation when animated VFX previews are scoped for the loadout app.

---

## Operational cost projections

**RAR-unpack step:** 75% of Pimen catalogue will require unpack. Unpack is mechanically trivial (`unrar e` or Python `rarfile` library). The cost is pipeline implementation, not per-asset execution time. Estimated implementation cost: 2–4 hours of elrond pipeline work (add a `rar_unpack` pre-processing stage to `curate_catalogue.py` or a standalone `prep_assets.py` script). Per-asset execution is negligible (RAR archives in this sample range 3.9 kB to 265 kB; unpack is milliseconds per file).

If the full Pimen catalogue is ~200 packs (rough extrapolation; Legolas can confirm), ~150 packs will need unpack. At <1s each, total unpack time for a full crawl's asset set is under 5 minutes.

**Frame-assembly step:** In this sample, 1 of 20 rows (5%) confirmed individual-frames-only. If this holds at full-crawl scale (~10 packs of 200), frame assembly is a moderate pipeline task. Using a script (e.g., `PIL`/`Pillow` to tile frames into a spritesheet + generate a Pixi.js-compatible JSON descriptor) is ~4–8 hours of elrond implementation, then automated for all matching packs. Elrond should add a `delivery_mode` field to curated rows: `spritesheet`, `individual-frames`, `both` — so the asset-prep script knows which packs need assembly.

**Per-animation canvas metadata structuring:** Low cost. Elrond's curation step 4 field normalization can extract canvas dimensions from `frame_count_notes` using a simple regex pattern (most paid packs state dimensions explicitly as `NxN`). Free pack rows with `unknown` canvas sizes will remain `unknown` until visual inspection.

---

## What this unblocks (full crawl greenlit on wiring track)

Full Pimen crawl release is viable from the wiring track's perspective, conditional on M1 (RAR-unpack) and M2 (frame-assembly) being implemented in elrond's pipeline before Pimen assets are ingested into the demo's static asset directory. The conditions do not block the crawl itself — Legolas can run the full crawl now. They block the asset-consumption step downstream of the crawl.

Specifically: the Pixi.js demo can consume Pimen VFX assets after the ingest pipeline unpacks RAR and assembles any individual-frame-only packs. The loadout app can display static PNG thumbnails without any additional work. Character/enemy assets (monolithic) are compatible with the demo's current baked-animation rendering approach.

---

## What this blocks (if conditions not met)

If the RAR-unpack step (M1) is not implemented, Pimen assets cannot enter the demo's rendering pipeline. The demo's Pixi.js `Assets.load()` call does not handle RAR. This is a hard block on demo consumption.

If M1 is deferred past full-crawl-release, the crawl data lands in the catalogue but cannot reach the demo until the pipeline catches up. The crawl and the demo ingest can be decoupled — Legolas crawls, elrond curates, and demo consumption waits for M1. This is acceptable staging.

---

## Cross-track notes (informational, not wiring-track findings)

The earth-spell-effect-03 pack bundles a full enemy sprite (Earth Elemental) inside a VFX pack with `category: "vfx"`. Gandalf's design track and elrond's structural track should both note this category-conflation. From the wiring perspective, the enemy sprite is wirable (monolithic assumption, PNG delivery), but the category mismatch may affect how elrond's curation pipeline handles embodiment tagging for this row.

The mega-pack (row 18) includes elemental icons — these are UI/HUD assets, distinct from VFX. The loadout app's HUD or gear-card visualization could consume these as `<img>` elements directly. No wiring concern; flagging for loadout-side awareness.

---

**Reviewer:** drax
**Date:** 2026-05-16
**Verdict file location:** `agentic_orchestration/qa/findings/2026-05-16-drax-pimen-sample-wiring-review.md`
