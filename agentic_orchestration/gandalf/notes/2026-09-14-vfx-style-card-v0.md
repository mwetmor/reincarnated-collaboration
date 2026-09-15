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

## v0.1 — the nostalgia vector (Matt 2026-09-15, R-C3-113)

Three trailers in one sitting set the poles. **CrossCode** = the fully-retro pole: true pixel grid, chip-tune-era framing; Matt likes its VFX and does *not* want to go that retro. **Chronicon** = particle-grammar density over quiet pixel ground. **Children of Morta** = drawn flipbook effects with hard pixel edges, a dark underlay and a local light layer, legible over a painted-pixel world close to ours (ours carries more detail).

**The thesis, verbatim in intent:** *nostalgic feel without full retro — Earthbound meets Diablo 2 — a unique style that does not merge them but pulls from both, plus its own special flourish (flourish the way Hades and Children of Morta have flourish; not theirs).*

**Correction (Matt, minutes later):** *"my Earthbound reference is only for the comparison of a teenager who goes to the future, which is where our story starts off… also the feel of Secret of Evermore."* So Earthbound is a **story-frame** comparison, not a visual one — an ordinary teenager whose adventure runs into the future; ours *begins* there. And the **feel** to hold is **Secret of Evermore** (Square USA, 1995): a boy thrown out of his small town into a world assembled from eras, wandering it with a companion, strange and lonely and wondrous at once, magic that is craft (alchemy from gathered ingredients), SNES-era painted-looking backgrounds. (An earlier draft of this section read Earthbound as a visual-clarity pole — flat shapes, PSI ornament — that reading is withdrawn; nothing of it is ruled.)

**What each reference contributes (reading, not ruling):**
- **Diablo 2** → the scene: painted, dark, weighty, dense with things; pre-rendered-isometric lineage. This is already the cliffside. Effects bold and few against a dense floor.
- **Earthbound** → **THEME ONLY — none of its style** (Matt, explicit): the teenager-into-the-future comparison for where *Reap. Die. Rise.* opens (story-side: `canonical/reap-die-rise-story/`). Earthbound must never appear as a visual, palette, UI or VFX reference in any brief, register card or style anchor.
- **Secret of Evermore** → the *feel*: displaced-kid wonder and unease; a journey through eras; companionship; magic as gathered craft; melancholy without grimdark. The nostalgia lives in this tone and in SNES-era adventure pacing, not in a pixel grid.
- **Flourish** (Hades / CoM as evidence that it exists, not as source) → a *signature reaction layer* of our own: hit-stop, flash, floor light, shake, and the world answering the spell (embers lifting, ash, ravens). The signature is still to be found; candidate motif: the death-faith frame — effects that *reap* (harvest lines, husks, the swing of a scythe in the dissolve).

**Anti-patterns named:** pixel grid on the scene (retro pole); Chronicon density over our detail (mud); merging the references into a pastel-flat D2 (the SNES-skin failure).

**Gate to fold into `canonical/reap-die-rise-story/style-register.md`:** the Chronicon + CoM measurements (Legolas, in flight) and two more kits from the breadth test judged against this thesis.

## v0.2 — measured corrections from Chronicon / Children of Morta / The Slormancer (Legolas 2026-09-15; `legolas/research/2026-09-15-chronicon-com-slormancer-vfx/findings.md`)

⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC (judging my own v0 hypothesis against the measurements).

**Held:** painted-pixel *shape* sprites on the art grid + a separate real-time light layer is exactly the split Children of Morta and The Slormancer ship (CoM: ~3-px pixel shapes + HD glow/light; Slormancer: ×4-grid banded shapes for the signature skills, soft screen-res particles for fire/novas). Flat 2–4 value bands held (Slormancer wave: 3 flat bands, flat-run share .93).

**Corrected:**
1. **White.** v0 asked for a white core (Hades 13–40 %). The two games that stay legible over painted-pixel ground use **almost no white** (CoM 0.1 % near-white at its densest; Slormancer 0.1 % at 19–24 % effect coverage), and Chronicon's white-out (22 % near-white) is the named failure. → **Cores are the palest saturated band, not white; white only as the 0.1 s flash LAYER, never as a flipbook frame.** (Frozen Orb kit: drop the white disc frame `impact_00`; the flash layer already exists.)
2. **Dark separation.** v0 assumed a Hades-style dark duplicate underlay. CoM has **no dark outline or duplicate** on effects; Slormancer's negative contrast comes from **black void shapes** and dark character outlines, not from a duplicate. Legibility over detailed ground is carried by **brightness separation: a bright soft halo (+.16 to +.41 over the ground) + floor light (ground brightens +.07–.09), saturation high, hue contrast opportunistic.** → dark duplicate demoted to an option for Hades-class strikes; **halo + floor light promoted to the default separation.**
3. **Extent.** These effects span 10–16 body-heights at peak; at our 64–128 px native a character is 64–128 art pixels tall, and that density leaves nothing for a painted contour. → **Cap burst width at 3–6 BH (Hades' range); full-screen ornaments are rare punctuation, never the grammar.**
4. **Resolution mixing.** Chronicon draws effects off its art grid at screen resolution next to pixel characters — the mixed-resolution softness is a named anti-pattern for us. → **Shape sprites on the effect's own pixel grid (pixel_scale), only light/glow/particles at screen resolution.**
5. **Hue rule withdrawn.** Effect-vs-ground hue distance runs 6–165° in CoM and 2–11° in Slormancer's tinted rooms: hue contrast is not what carries legibility. → separation by brightness/halo/void, never by palette rule.

**Oracle consequence (fork for Matt, R-C3-118):** Hades keeps the *timing* bands (strike rise, decay, half-life) — no other reference has measured flipbook timing; CoM + Slormancer supply the *legibility* bands (near-white ≤ 2 %, halo +.16–.41, floor light +.07–.09, extent 3–6 BH, white-free banded cores, S median ≥ .5). A hybrid reference file `oracle/vfx_reference_hybrid.json` would encode both.
