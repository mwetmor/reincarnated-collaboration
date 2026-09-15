# VFX Style Card v0 — hypothesis under test (painted-pixel + real-time light)

> **STATUS:** WORKING — gandalf (SPEC-AUTHOR), 2026-09-14. A hypothesis, not canon: it becomes a `canonical/reap-die-rise-story/` companion to the H1 register only after the six-kit breadth test (R-C3-98/99) corrects it. Sources: Matt's direction ("between painted and pixel, with simple 3D effects — particles / lighting / shaders", R-C3-98); the measured oracle (`legolas/research/2026-09-14-vfx-oracles/findings.md`); the style atlas (`…/2026-09-14-vfx-style-atlas/findings.md`; samples at `~/Games/vendor/vfx-atlas/`); Matt's verdicts R-C3-28/83/88. Every line is a constraint the breadth test can falsify.

## 1. Register (what an effect frame IS)
- **Painted-pixel silhouette.** Each effect phase is a painted shape at a LOW native size — an effect frame 64–128 px on its long side at the Keeper's 130-px scale — then shown crisp (nearest-neighbour), never smoothed or blurred. Edges are hard; interior detail is a few painted planes, not texture. Atlas anchors: CrossCode shock/bomb, Chrono Trigger Flare, RPG Maker MV cells, Hades II splash/pillar (flat planes).
- **Stepped value bands, white core.** 3–4 discrete value bands per effect: white/near-white core (13–40 % of the area at peak), saturated body, darker rim/interior holes. The core is desaturated at peak and saturates as the effect dies (oracle O3/O5). Never a smooth gradient inside the shape.
- **No H1 contour on effects.** Weight comes from a **dark duplicate underlay** (the same frames tinted black, drawn beneath, Mix blend) and dark interior shapes; a thin dark stroke is allowed only on bolts (Hades E1). Ruled R-C3-90 (2).
- **One dominant hue per element** (hue circular SD ≤ ~15–25°, O4), painted once in GREYSCALE and **tinted at runtime** per element/kit (Hades: 112 of 126 god variants share a sheet). Element palettes: ice pale cyan-white / fire orange with yellow core / poison acid green with dark olive rim / lightning white-violet / holy warm gold-white.
- **Dissolve by band-stepping**, not fade: the shape erodes from the centre (E2) or steps down through its bands (CT Flare: white → pink → violet → navy) while hue holds; final frame is a low-value residue at 15–25 % of peak area, then gone.

## 2. Timing (what an effect DOES)
- 60 fps base with **hand-set holds per frame** (Hades: 64 % held 1, 31 % held 2); no animate-on-2s rule (R-C3-90 (3)).
- Anticipation is a separate telegraph layer where the skill has one; the strike itself **peaks within 0–1 frames**, **halves in 2–7 frames**, residue 0.3–1.0 s (O1/O2).
- Projectiles travel **6.5–11.6 body-heights/s** (O7); fast movers streak along their velocity (P17).
- Effects are **rotated at runtime** and squashed onto the ground (Y ≈ 0.5–0.62), never baked per direction (R-C3-28 fix).

## 3. The real-time layer (the "simple 3D effects")
Every effect is one kit of layers; colour and shape mask vary, the stack is constant:
1. body sheet (painted-pixel, tinted) · 2. dark duplicate beneath · 3. **additive glow** on the body (CanvasItemMaterial Add) · 4. **floor light disc** 0.2 s (additive, ground-squashed) · 5. **particles** using the same painted-pixel sprites (embers/sparks/motes; the C-3 ember kit is the precedent) · 6. **flash** 0.1 s at α 0.5, scale 1.2 → 1.0 · 7. **scorch/decal** 1–3 s (Mix) · 8. **hit-stop** 0.04–0.12 s at 0.1×, screen shake small (Hades medians).
Lighting is real-time (2D light or additive disc), never painted into the ground.

## 4. Judge axes (Matt's verdicts, not closed-form)
directionality / facing-lock · frame-to-frame boil ("choppiness on top of smooth") · matte halo ("matte white/glow") · liveness (static embers fail) · "reads as painted planes, not rendered noise" · ground component follows its owner · element identity readable at 130-px scale in a busy fight.

## 5. What the six-kit test must show
One register holding, at once: pale D2 ice (Frozen Orb), smoky GD fire (Blackwater Cocktail), sickly PoE green (Poisonous Concoction), clean LE lightning (Lightning Blast), a painted Hades hit (Zeus chain), warm holy aura (Healing Hands) — each keeping its own identity. Any kit that cannot be made to read under §1–§3 falsifies the line that blocks it; the card is corrected, not the kit.

— gandalf, 2026-09-14
