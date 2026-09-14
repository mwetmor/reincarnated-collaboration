# Legolas — VFX style atlas: feasibility + first sample pull (retro-to-modern VFX corpus)

> **STATUS:** CURRENT — commission by gandalf (ELICITOR → RUN-CONDUCTOR), Matt-agreed 2026-09-14 (ledger `astra_test_01/burst/runs/C-3/ledger.json` R-C3-90/91/92). Purpose: find OUR VFX style by mixing traits from past games (retro 1990s–2000s RPG/ARPG/adventure + modern retro + our ARPG set), and give every sample the O1–O9 measurements from `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md`. **Pixel-art register is an open option — never eliminate it** (tag every sample painted / pixel / 3D).

## 1. Sources (first pass)
- **Retro, data-rich:** Baldur's Gate II + Icewind Dale (Infinity Engine: BAM spell sprites, VVC/VEF timing; IESDP, Near Infinity) · Diablo I (DevilutionX-documented missile CL2 sprites) · Diablo II (DC6 missile/overlay sprites + `Missiles.txt`/`Overlay.txt`) · Ragnarok Online (effect .str + sprites; emulator-community docs) · RPG Maker 2003 / XP / MV standard (RTP) battle animations (cell frames + timing + flash/shake) · SNES/GBA spell rips (Final Fantasy VI, Chrono Trigger, Secret of Mana, Golden Sun; The Spriters Resource + technique write-ups: palette cycling, dithered transparency, screen flash).
- **Modern retro:** Sea of Stars · Octopath Traveler (HD-2D) · CrossCode (effect JSON) · Hyper Light Drifter.
- **Our set:** Hades flipbooks (from a local install — confirm what is needed) · LoL and Dota 2 wiki ability clips · frames from D2R, Grim Dawn (install already at `~/Games/vendor/grim-dawn-edition-III-20260808`), Last Epoch, PoE.

## 2. Effect types (6)
projectile · impact/explosion · ground area (circle/nova) · aura/buff · beam/lightning · elemental burst (fire / ice / holy). Target ≈ 100–150 samples total; this pass pulls **one sample per effect type per source where obtainable without Matt's accounts or installs** (≈ 60–90).

## 3. Per source, return (feasibility table)
format(s) and extraction tool that works on macOS (arm64) or in pure Python · whether timing/layer data exists (frame counts, fps, blend, transparency method) · obtainability: free public download / fan-site rip / needs purchase or install / needs Matt's account · licence / terms position for PRIVATE STUDY (no redistribution, no image-model reference) · expected disk for (a) the raw source and (b) the extracted effect subset · go / no-go and effort.

## 4. Sample pull (only no-account sources)
For each pulled sample store: a short loop (≤ 2 s) as a lossless or near-lossless animated WebP/APNG or a PNG frame folder cropped to the effect, **native resolution, native frame timing kept** (per-frame durations), and a JSON record: `{id, game, year, source_url, effect_type, element, register: painted|pixel|3D, native_res, frames, fps_or_durations, blend_or_transparency, measures: {O1..O9 where computable}, traits: {outline, palette_colors, value_bands, transparency_method, dither, shape_language, smear, dissolve, ground_component, flash_shake, core_body_edge}}`. Pixel traits (native resolution, palette size, dithering, sub-pixel motion) on every pixel sample.

## 5. Constraints
- **Disk:** the Mac has ≈ 25 GB free. Hard cap for this pass: **≤ 6 GB peak, ≤ 2 GB kept.** No game installs. Delete source footage and archives after cropping.
- Measurement and private study only; never an image-model reference; nothing from the samples is committed to the repo (JSON records and a summary are returned to gandalf).
- Store samples in the session scratchpad under `vfx-atlas/` (gandalf moves them to persistent local storage); report the folder size.
- Evidence classes as before: VERIFIED / MEASURED / DERIVED / PRACTITIONER-REPORT; blocked routes stated, never substituted.

## 6. Deliverable
Feasibility table (§3) · list of pulled samples with folder paths and sizes · the JSON records (or the path to one `atlas.json`) · what needs Matt (installs, accounts, purchases) with the disk each would cost · gaps.

— gandalf, 2026-09-14
