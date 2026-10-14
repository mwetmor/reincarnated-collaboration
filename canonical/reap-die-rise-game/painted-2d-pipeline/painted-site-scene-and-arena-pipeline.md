# Painted-Site Scene + Arena Pipeline: a painting projected onto 3D, then a fight brought into it

> **STATUS:** CURRENT (load-bearing as of 2026-10-13) — see `canonical/00-ground-state.md`. This is the canonical procedure for building a playable scene the way barrow_v2 was built: a hand-painted plate cut onto real 3D ground, with a fight brought into it and shipped to the web. Workflow canon: it says **what is done, in what order, by whom, behind which gate**. The tools and numbers live in the run artifacts it cites.

**Date:** 2026-10-13
**Author:** gandalf (CANON-STEWARD / SPEC-AUTHOR; RUN-CONDUCTOR of Run C-9 Phase 2, workstream BV2F)
**Status:** v1.0. Canonized from barrow_v2: Phase 0 → M3′ ratified (R-C9-350) → north extension (site_ph4) → the arena (R-C9-345..396) → the public web build.
**Authority:** Matt 2026-10-13 (session close): *"record everything that enabled completion of the barrow_v2 pipeline … as canonical scene/arena generation pipeline procedure."* The method's DEV register was ratified at M3′ (R-C9-350). DEV-30 (the band stager) is still owed on Matt's ratification list.
**Supersession:** **PARTIAL.** This supersedes the *"3D scenes crossed off the plan"* clause of `scene-builder-workflow.md` for **painted-onto-3D sites**. The flat painted-2D workflow there stands unchanged for 2D scenes; this doc is its 3D-site sibling.
**Companion docs:**
- `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md` — the 2D sibling (roles, grey room → PACK → Matt loop)
- `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` + `mechanical-process.md` — the Astra burst lane (bursts, wrapper audit, freeze)
- `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` — the run charter: §16 DEV register, gates, lanes
- `astra_test_01/burst/runs/C-9/ledger.json` — the truth of record (rulings R-C9-150..396, milestones, halts)
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/RESUME_{LV,PT,PH}.md` — the lane notes: exact tools and commands
- `astra_test_01/burst/runs/C-9/barrow_full/tools/WEB_ARENA_NOTES.md` + `WEB_ARENA_BUGS.md` — the web build record
- `agentic_orchestration/gandalf/notes/2026-10-13-c9-arena-astra-completion-review.md` — review of the Codex completion work

---

## FLOW

1. **Frame + control** ← 2. The frame and the positive control
2. **Level** ← 3. Level (LV)
3. **Guide** ← 4. Guide render
4. **Paint** ← 5. Painting (PT)
5. **Take + dress** ← 6. Take, bake and dress
6. **Prove** ← 7. Proof (PH) and the Matt gate
7. **Extend** ← 8. Extending a ratified plate
8. **Fight** ← 9. Bringing the fight into the scene
9. **Ship** ← 10. Shipping to the web

---

## 0. TL;DR

- **The look:** the scene is ONE hand-painted plate seen through ONE fixed orthographic camera (pitch 52.95354°, yaw 47). The plate is cut onto real 3D ground (a "take") and dressed with unlit bakes, heather and reed cards, and animated water and floes. Players and monsters walk real terrain under the painted look.
- **Painting** is Astra guided paint-over in 1280 px chunks with 256 px context strips, painted in wavefront order over a pinned 3D guide render. It is stitched by the DEV register's seam tools, corrected by masked local repaints, and paid for in image tranches with caps.
- **Proof** is a pre-registered parity harness, with fail-first controls and disclosed failures, then a jack-ryan Gate-2, then **Matt walking the scene himself**. His eye is the final gate.
- **The fight comes to the scene:** the existing arena runtime is used unmodified. Only spawn points move; doors and features become player-only blockers. Presentation (art, effects, numbers, interpolation, doorway entry) is added on the scene side.
- **Shipping:** the scene and fight are bundled byte-verified by digest, given a web-only path shim where the sealed runtime expects absolute paths, and deployed to a Vercel playtest route: push once, check once.

---

## 1. Roles

| Lane | Owner | Does |
|---|---|---|
| Conductor | gandalf (RUN-CONDUCTOR) | Rules and records every decision in the ledger. Commits the ledger. Runs build-safe cleanup. Asks Matt only for his calls, one recommendation per question. |
| LV, the level | drax | 3D ground, the frame transform, walk colliders, bounds, extension geometry |
| PT, the painting | drax | guide pins, Astra bursts, stitching, DEV-24 repaints, take/bake/prep, data sets |
| PH, the proof | galadriel | parity harness P1–P11: pre-registration, fail-first controls, calibration doc |
| QA | jack-ryan | Gate-1 on the charter; Gate-2 on each milestone and each delta |
| Arena | drax | the fight-in-scene variant, presentation, the web build |
| Matt | — | walks the scene, gives notes, ratifies the DEV register and FAIL rows, picks looks, grants permissions |

---

## 2. The frame and the positive control

1. Reproduce the reference scene's **recorded** numbers at HEAD before building anything, with the targets written down first (fid/pc). A missed target is a HALT.
2. Freeze the toolchain in two tiers:
   - **Tier-A** is byte-identical (the guided-paint driver, stitch, wave, refs_guard, bakes), checked by `verify.sh` + `SHA256SUMS`.
   - **Tier-B** is flag-gated: flag off must reproduce the reference byte for byte.
3. Fix the frame once: `world = R_y(camera yaw) · sim`. Prove the sign with a two-anchor test.

## 3. Level (LV)

- Build the ground in the camera-aligned frame: terrain heightfield, collider meshes, bounds.
- No gameplay content lives in the level beyond what the scene needs.
- Re-pinning bounds or level geometry is a recorded event that carries its sha.

## 4. Guide render

- Render the unpainted level at plate resolution: the ID render, the class map, and the "guide" art.
- **Pin** each one by digest. Every later stage reads the pins, so a guide change is a re-pin with a ledger row.
- Guide smoothing (DEV-28) and cleanups, such as removed stray posts and arcs, are pin events too.

## 5. Painting (PT)

1. **Bursts.** Each chunk is one Astra burst (1280×768 stride) with:
   - 256 px context from the top and left;
   - wavefront order under the frozen driver's ready rule;
   - refs_guard (no franchise, studio or artist names);
   - keys from `~/.zshrc`, never printed;
   - one service retry;
   - burst records written to the ledger by the driver.
2. **Image tranches.** Every tranche has a cap. Going over is a HALT with a cap ruling (e.g. N1 10 → 12 → 14).
3. **Stitching** (DEV register):
   - tone match (DEV-23) and grain match (DEV-25);
   - min-error cut with a pinned pilot path (DEV-26);
   - Poisson placement (DEV-27);
   - context patch, so new chunks stage from the patched pilot (DEV-29);
   - the **harmonic seam** for extensions (§ 8).
4. **Matt's notes → masked local repaints** (DEV-24): layers with `read_zone` and pinned correction fields. Each note becomes a layer; nothing is repainted wholesale.
5. **Prompt wording is load-bearing.** Describe content, never mood words that leak colour: "pale mere" turned the snow cream (R-C9-257). Keep every negative clause when a brief is revised; geo v7 dropped them and v7.1 had to restore 12.

## 6. Take, bake and dress

- **Take:** cut the painting by the geometry.
- **Bakes:** unlit bakes (t5_06b) per model. Use **projected paint** for meshes with no UVs or overlapping UVs (procedural posts, panels), and carry a UV-overlap check in the export report.
- **Dress:**
  - heather and reed cards from tuft masks;
  - the **water** animated over the painted sea (DEV-5);
  - **loose floes** as 3D slabs carrying their painted pixels, one shared material with an `instance uniform` bob phase;
  - **snow** by the painted-v1 law: the painting is the surface, with an ankle-deep layer for prints and ploughs. On web, use the web density and half-float textures.
- **Protect the build inputs:** every gitignored input goes in `build_inputs_manifest.json`, checked by `build_inputs_check.py`, and is excluded from every cleanup.

## 7. Proof (PH) and the Matt gate

1. **Pre-register before reading.** The calibration doc is append-only, and pre-registration is committed before the data it judges. Instruments are **re-instrumented or discarded, never threshold-tuned**.
2. **Fail-first controls** for every new check: a RED control that must fail, plus a rigid or null control.
3. **Disclose FAIL rows.** Do not hide them; Matt accepts them at ratification (R-C9-350).
4. **Delta re-runs:** after any repaint, compute the changed-pixel mask and re-run only what it touches. Footprint checks decide whether earlier judged crops survive.
5. **jack-ryan Gate-2** on each milestone and delta, then **Matt walks the scene locally**. His walk is the owner-eye half of the milestone.

## 8. Extending a ratified plate

- **Add a band; never touch ratified pixels.**
  - LV extends the ground (north-only edits) and proves the frame.
  - PT paints the band with a band stager (**DEV-30**): context from the plate's top rows and the previous band chunk.
- **Compose** under an **identity proof**: every old pixel is byte-identical at its new offset, with a one-pixel control that must be caught.
- **Two seam checks:**
  - **tone** (step vs controls);
  - **shape** (a straight-line detector along the seam row). A tone metric cannot see a shape cut; the frozen-pool cut slipped past the tone check and was caught in play (R-C9-389).
  - Fix seams **band-side only**: a masked band repaint, or the harmonic Poisson seam that makes the band's last row equal the plate's first.
- **New data set** (site_ph4); the old set (site_ph3) stays untouched. World coordinates do not change.

## 9. Bringing the fight into the scene

**Principle (Matt, R-C9-347/348): bring the fight to the scene; change only what the scene forces.**

1. **The runtime is unmodified.** Reference or vendor it **by digest** (tree digest plus every member, checked at source, in the copy, and at launch).
2. **One hook:** override the session's post-bind, pre-open method to write the spawn points (doors and features), drop the floor hazards, and clear the mouths. Monster-to-point mapping stays as the data has it.
3. **Anti-camping by impassability:**
   - player-only blockers at the doors and solid features;
   - floor hazards only where impassability can't be made;
   - ambush spawns rise from the ground.
4. **Walk map:** a load-time ray grid over the scene's colliders.
   - Step rule: ≤ 40°, ±0.45 m.
   - Keep-outs on hollows.
   - **Slide:** a refused move is redirected along the edge, never dropped.
   - Prove it with a blocker probe from many bearings: 0 trapped.
5. **Presentation is scene-side and drawing-only:**
   - **Interpolation** between sim ticks: the sim steps at about 12 Hz, so draw positions between ticks.
   - **Doorway entry:** hidden in the door's dark, then a fade as the body crosses the threshold. A body inside solid geometry stays hidden until it reaches open ground.
   - **Sun-true character shadows.**
   - **Damage numbers** in the house NUM-POP style, on the targets only.
   - **Generic names:** no source-game names on screen.
   - **Placeholder bodies** for records with no art, scaled to the sim radius.
6. **Characters:** prefer the **live 3D rig** (60 Hz poses, real light) over pre-rendered strips. JOIN-1 strips are baked at 12 frames per clip and read as choppy (R-C9-383). Monsters stay strips until re-rendered or rigged.
7. **Effects: REUSE before authoring** (R-C9-374). 2D flipbook VFX go into a 3D scene as camera-facing billboards with their own frames, timings and colours. Pool them, cap simultaneous explosions, use no per-hit lights, and **measure on/off on the heaviest wave**.
8. **Diagnose before fixing.** Measure layer by layer before turning anything off. The choppiness was clip frame rate and tick stepping, not scenery (R-C9-381..383).

## 10. Shipping to the web

1. **Bundle by digest:** the runtime, the model pack and pinned tables, each verified at bundle time and at launch (the launch refuses on a mismatch).
2. **Absolute paths** that the sealed code expects: a **web-only path shim** writes the byte-identical pinned file where the code looks, and the code still checks its own sha (R-C9-394). A platform-solver fallback is in place pending Matt's ratification; see the review note's WARN-1.
3. **Web data:**
   - a phone-size plate (WebP, about 6 MB, sampled by normalised plate UV);
   - lossless half-size bakes;
   - per-wave art packs loaded concurrently and fail-closed;
   - shader and animation warm-up before play;
   - streamed WebAudio verified by output PCM.
4. **One build, PC and phone:** mouse and keyboard by default, with a touch layer that wakes on the first touch.
5. **Deploy:** stage into a `reincarnated-loadout/public/playtest/<route>/` folder, then push once and check once (R-C9-84). Public routes need no login.

## 11. Operations that kept the run moving

- **Ledger as truth:** every ruling verbatim with Matt's words. The conductor alone commits it (`git commit --only`; `git status --porcelain` before, `git show --stat HEAD` after, `git -C` across repos).
- **Disk:** lanes halt at 21 GiB and the conductor gate is 20 GiB (one-time releases recorded). The conductor runs build-safe **cleanup manifests**: untracked files only, excluding build inputs, ledger- and QA-cited files, and anything touched in the last 30 minutes. A raw `rm` outside the repo is Matt's.
- **Permissions:** a refusal is reported, never routed around. Standing consent lives in configuration Matt sets himself; a relayed ruling is not consent.
- **Shared Mac:** kill only your own PIDs, use small auto-quit test windows, and use the heavy lock for Godot.
- **Reference choice is a decision.** Name the exact build to match ("the snow as the deployed phone build runs it", R-C9-379). Two "v1s" existed, and picking the wrong one cost three snow rounds.
- **Instruments go blind silently.** A check that runs is not a check that passes. Give every new check a control that must fail (tone vs shape, file-format manifests, git `HEAD` vs index).

## 12. Cross-references

- Ledger: `astra_test_01/burst/runs/C-9/ledger.json`. Milestones M-C9-BV2F-PAINTING-COMPLETE, -SITE-BUILT, -M3P-RATIFIED, -SITE-PH4-BUILT, M-C9-ARENA-W151-PLAYABLE, -10W-BUILT.
- QA: `agentic_orchestration/qa/findings/2026-10-09-bv2f-site-build-gate2.md`, `2026-10-09-bv2f-r339-delta-gate2.md`.
- Handoff: `agentic_orchestration/gandalf/notes/2026-10-13-c9-arena-session-handoff.md`.

Tracker-delta: new gap → `canonical/current-to-end-state/current-to-end-state-game.md` (the painted-site scene + arena pipeline is now canon; open items: DEV-30 and the solver-fallback ratification, whirlwind smoke R-C9-396, monsters as live 3D rigs, web download size and phone confirmation).

---

**Signed:** gandalf (CANON-STEWARD; RUN-CONDUCTOR, Run C-9 BV2F)
**For:** the repeatable procedure for building a painted, playable 3D scene and fighting in it, from first frame to public web build.
