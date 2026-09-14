# Cliffside exploration scene — HITL plan (painted 2D, blockout-first)

> **STATUS:** CURRENT — HITL plan v1.0, Matt present at every checkpoint. Author: gandalf (ELICITOR → ARCHITECT → RUN-CONDUCTOR), 2026-09-13. Rulings: C-3 ledger `astra_test_01/burst/runs/C-3/ledger.json` **R-C3-42** (Matt forks 1–6). Predecessor: the tower scene (R-C3-29…40). Not an autonomous run: every checkpoint stops for Matt's eye.

## 0. What we are making
An **LE-05-like outdoor cliffside path** for the novice Keeper (starter set), drawn in the **H1 line register with more zany Hades flavour in the environment** (saturated jewel tones, bold graphic shadows, exaggerated shapes; the Keeper sprite itself is unchanged). A **follow camera** stays on the character. Beyond and below the cliff edge, a **separately scrolling, extremely detailed background** tells a story: **the ruins of a recently destroyed temple and a charred, burnt forest against a sunset sky**. Foreground first **bare**, then a **cluttered** variant; clutter as **individual 2D assets**, including **breakables/interactives**: boxes, vines, a bridge piece that falls out.

## 1. Rulings in force (R-C3-42)
| # | Ruling |
|---|---|
| 1 | Camera: D2/LE-like, Keeper at **12–13 %** of screen height (aim 12.5 %) |
| 2 | Style: H1 register |
| 3 | Outdoor LE-05-like exploration; add zany Hades flavour; follow camera; parallax sky/background below and beyond the cliff; background story = destroyed temple ruins + charred forest + sunset |
| 4 | Bare foreground first, cluttered variant later; background extremely detailed from the start |
| 5 | Clutter as individual 2D assets; add breakables/interactives (boxes, vines, falling bridge piece) |
| 6 | drax renders the blockout; Matt sees it at the start |

## 2. ARCHITECT pass — decisions the build will hit
| Decision | Class | Disposition |
|---|---|---|
| Exact camera numbers for "D2/LE" | GATED — Matt's eye at checkpoint 1 | Start from the ratified GD `player_lock` angles (yaw 47°, pitch 52.95°, vertical FOV 31.79°), dolly until a 1.75 m figure reads 12.5 % at 1080p; render beside LE-05 and D2-06. No absolute D2/LE camera is recoverable from stills (E01: camera UNIDENTIFIED), so the look is ratified, not a number. |
| Keeper perspective vs camera | GATED — checkpoint 1 | Our sprites were drawn from a shallow ~25–30° view; at 12.5 % the upright look is more visible than at 9.9 %. Checkpoint 1 composites real Keeper frames onto the blockout render so Matt can judge before any painting. |
| Level size with a follow camera | RESOLVED (R-C3-43) | Nothing is projected onto 3D: all art is flat screen-space painting at the fixed camera. The paint guide is an ORTHOGRAPHIC canvas at the player_lock yaw/pitch (a perspective follow camera cannot align with flat paintings). The canvas is cut into overlapping 1536×1024 chunks with canvas origins; props are single-view sprites; background layers are flat panoramas. Fidelity is measured against blockout masks and across seams. |
| Parallax layers | RESOLVED (conductor, veto-open) | Four layers: sunset sky (slowest) → far temple ruins → charred forest and valley → cliff face and foreground path (1.0). Each background layer is a wide panorama painted from the blockout's far planes. Factors are tuned at checkpoint 3. |
| Hades flavour boundary | RESOLVED (conductor, veto-open) | Environment only; the Keeper sprite stays as passed. |
| Breakable / interactive behaviour | GATED — checkpoint 5 | Art: per-asset intact / broken frames. Logic: the Godot scene kit. Designed after the bare scene plays. |
| Frost bolt / own VFX | QUEUED | R-C3-31 fast follow, after this scene. |

## 3. Checkpoints (each stops for Matt)
1. **Blockout look (drax).** Greybox cliff path, bridge gap and far planes rendered at the candidate camera, with the Keeper composited at 12.5 % beside LE-05 and D2-06. Matt rules camera and perspective.
1b. **Proof step (R-C3-43, Matt "Agreed").** Two adjacent foreground chunks painted over the ORTHOGRAPHIC blockout canvas (each 1536×1024 with its canvas-pixel origin and the neighbour's overlap strip) + one background panorama; measured against the blockout masks and across the seam. Fallback if chunks do not hold together: fewer, larger paintings upscaled (sharpness trade). ≈ 3–5 Astra images, 0 Grok.
2. **Background panorama (Astra).** Sunset sky, destroyed temple ruins and charred forest painted to the blockout's far planes, at full detail. Matt rules story and style.
3. **Bare foreground + parallax in Godot.** Path chunks painted over the blockout; parallax scrolling with the follow camera; the Keeper walking. First playable.
4. **Cluttered variant.** The same blockout with props, painted as a look target.
5. **Props as assets + breakables/interactives.** Individual 2D assets placed from layout data; boxes, vines and the falling bridge piece wired in.

**Progress (R-C3-43…58):** checkpoints 1, 1b, 2 and **3 COMPLETE** — first playable delivered (`astra_test_01/burst/runs/C-3/cliffside_final/`). Geometry went v3 → v4.1 on Matt's review (strip removed; organic rock; boulders out → props at checkpoint 5); walkable = all flat tops, 0.5 m rim margin; image cap lifted (R-C3-55). Next: checkpoint 4.

**Clutter method (R-C3-61/62, Matt):** Astra composes clutter by EDITING the bare painted crops; the before/after diff locates every object; extraction by diff only where the pre-registered gate passes (ground drift ≤ 6 in a 16-px ring, one clean mask with ≤ 3-px halo, shadow separates), otherwise Astra repaints that object alone on green, matched to the edit, registered back to the diff position. Every object becomes a catalogued reusable asset. Deferred test for procedural maps: give Astra the asset base and ask it to recommend placement on a new bare map.

**Budget posture:** Grok not needed through checkpoint 5 (existing clips). Astra images per checkpoint are named before it fires. Nothing moves past a checkpoint without Matt's word.

Tracker-delta: game tracker SESSION-DELTA owed at checkpoint 3 (first playable).

— gandalf, 2026-09-13
