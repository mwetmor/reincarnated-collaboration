# Legolas Mode A — Chronicon VFX: atlas pull + oracle measurement (particle-grammar reference)

> **STATUS:** CURRENT — research commission, gandalf (RUN-CONDUCTOR, Run C-3 → VFX lane). Matt 2026-09-15: *"I just looked at Chronicon's Steam page, and I'm not a fan of the art register/style, but I love the VFX, and that style may be worth looking into for our game."* Chronicon (Subworld, 2016 EA / 1.0 2020, Steam 375480) is NOT in the 54-sample VFX style atlas (`~/Games/vendor/vfx-atlas/`). Add it, measured.

## 1. What to pull (study-only fence — never an image-model reference, never committed; local store only)
6–8 short samples of Chronicon skill VFX from the Steam page trailer / screenshots, the Subworld dev blog, Steam community gifs, YouTube skill showcases — one per family: (a) a projectile with trail (e.g. Warlock bolt / Templar hammer), (b) a screen-filling AoE burst (Mage nova / Berserker whirlwind), (c) a chain/beam (lightning chain), (d) a DoT ground field (poison / fire pool), (e) a summon / pet effect, (f) a late-game "screen full of numbers and particles" clip (the density ceiling). Cut each to a 1–3 s loop of frames at source fps into `~/Games/vendor/vfx-atlas/samples/chronicon-<family>/` with the same layout as the existing samples (`frames/`, `loop.webp`, `meta.json` with source URL, timestamp, fps, crop, body height in px), and append them to `atlas.json` so `atlas.html` shows them. Keep the existing sample schema exactly.

## 2. Measure
Run **our** oracle on each sample: `cd astra_test_01/burst && python3 -m oracle.vfx_measure <frames_dir> --fps <src fps> --plate black --body-h-px <measured> --ref oracle/vfx_reference_hades.json` (read-only use of the repo tooling; write outputs next to the sample as `measure.json`). Also fill the atlas O1–O9 style traits used for the other 54 samples (value bands, additive vs painted, contour, particle count class, extent, hue spread, saturation core/rim, life, rate). Then a **Chronicon vs Hades vs D2R** three-column table on the same measures.

## 3. Process note (short)
What is known about how Subworld makes their VFX: engine (GameMaker), pixel-particle sprites, additive blending, particle counts, screen shake / hit-stop, resolution of the effect grid vs the scene grid, palette rules per element. Cite posts/interviews with URLs and dates; label VERIFIED / PRACTITIONER-REPORT / INFERRED.

## 4. Deliverable (text return; gandalf files it at `agentic_orchestration/legolas/research/2026-09-15-chronicon-vfx/findings.md`)
1. Sample list with sources; 2. measurement table + the three-column comparison; 3. process note; 4. a one-paragraph "what carries to a painted-pixel register at 64–128 px native over painted backgrounds" (state what would break: legibility over painted detail, density vs contour); 5. gaps.

## 4b. Extension (Matt 2026-09-15, sent to the running agent): CHILDREN OF MORTA (Dead Mage, 2019, Steam 330020)
Same pull, same schema (`children-of-morta-<family>/`), same measures; comparison becomes four columns Chronicon / Children of Morta / Hades / D2R. Matt's observation: CoM's painted-pixel world is close to our painted register (ours has more detail) and its VFX read even better than Chronicon's. For CoM also record HOW the effects stay legible over detailed painted ground (dark separation / outline, local light layer, ground darkening during casts, effect pixel grid vs scene grid, palette contrast per element), MEASURED / INFERRED.

## 5. Host guardrails (hard)
Serial only, no sub-agents; **one decode at a time**, ffmpeg/python under 1.5 GB RSS (the watchdog kills > 2 GB); stream, never load a whole video into memory; no model downloads. Do not write into the repo; the atlas store under `~/Games/vendor/` is the only write target.

— gandalf, 2026-09-15
