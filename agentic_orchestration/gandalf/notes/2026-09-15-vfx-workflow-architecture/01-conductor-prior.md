# Conductor prior — pre-registered before Astra session 1 and the Legolas probes returned

> **STATUS:** WORKING — gandalf (ARCHITECT), 2026-09-15, written with S1 and L1 in flight and unread. Purpose: a falsifiable prior, so the synthesis (`03-architecture.md`) can say what the consultation *changed*. Not a recommendation to Matt.

## P0 — The one-sentence thesis
**Grammar lives in the runtime; primitives live in sheets; the anchor is a still; time is never drawn.** (Dossier § 5 corollary.)

## P1 — The architecture I expect to be right (the "primitive alphabet + grammar templates" model)

| Layer | Owner | What it is |
|---|---|---|
| **Skill spec** (per skill) | engine emission → conductor glue | `geometry` (26-type palette) → **grammar template id**; `canonical_element` → **element palette**; `aoe_radius` / range / count / duration / `cooldown` → template parameters; `role` (primary / burst / …) → loudness tier (P11) |
| **Grammar templates** (≈ 10–15, one per motion shape) | Godot scenes, drax builds against a gandalf spec | projectile (single / multi / fork / pierce) · orbit-emitter · thrown-arc → ground field · chain-with-jump · instant strike · beam / channel · nova / ring · cone · melee arc / whirlwind · dash / leap · ground slam / shockwave · aura / self-buff loop · totem / summon spawn · trap / mine. Each = a timeline of **slots** (telegraph → onset → peak → decay → residue) with the Hades timing bands as defaults and per-grammar motion (orbit radius/ω; arc apex/time; chain hop delay; beam length/sweep) |
| **Primitive alphabet** (per element, ≈ 8–12 painted sprites) | Astra paints; oracle measures; Matt approves once per element | tongue · shard · ring · arc segment · mote · pool tile · chain link · wisp · puff · spark · core · streak — each isolated, on its own pixel grid, drawn in the scene's light, anchored by ONE per-element anchor still ("VFX chunk_A") that was itself painted *on top of the scene anchor chunk* |
| **Layer stack** (fixed) | exists (T3t/T3u/T3v) | body · additive halo · floor light · flash 0.1 s · decal · hit-stop · shake · tinted particles — dark duplicate optional (v0.2) |
| **Blockout** (per skill, before any painting) | conductor glue + drax; **Matt sees it** | grey-shape timeline in the live scene with dummies + targeting: size (BH), speed, phases, durations, aim rule. This is the VFX grey room. Hand-off step 2(b). |

**Time source:** the grammar template (engine tweens/particles/curves) — never a drawn row. The image model contributes stills only: primitives, and (maybe) 2–3 key silhouettes per burst for erosion-based dissolve.

## P2 — Predictions Astra's answer will confirm or refute
- A-1: Astra will say EDIT-along-time drifts after 3–5 steps and recommends stills + runtime motion. (Confidence 0.7.)
- A-2: Astra will say the black-void rule cannot be prompted away for emissive subjects and will recommend a key plate + EDIT strip, or drawing the emitter *inside* a scene crop and isolating (the props method). (0.75)
- A-3: Astra will recommend coloured-per-element primitives over greyscale-tint for anything with an object body (flask) and keep greyscale-tint for pure light. (0.6)
- A-4: Astra will recommend a per-element anchor still painted over the scene chunk as the coherence mechanism. (0.5)
- A-5: Astra will rank the image model's motion contribution as "key silhouettes for shader erosion" above "frames". (0.6)
- A-6: Astra will name the briefs' prohibition-heavy prose as harmful and ask for a reference image + a positive description + a plate. (0.85)

## P3 — Predictions Legolas will confirm or refute
- L-1: ≤ 12 grammar templates cover ≥ 80 % of the corpus's key skills. (0.6)
- L-2: Children of Morta / Slormancer / Hades all author effects as *shared painted primitives moved by the runtime* far more than as unique flipbooks; the flipbook is the burst core only. (0.65)
- L-3: Godot native procedural (particles + shaders over painted masks) is the only motion source that is free, host-feasible, and timing-exact; sim → sheet tools are either Windows-only (EmberGen) or too heavy for 8 GB. (0.7)
- L-4: No video model produces a usable alpha effect loop today; video stays glow-only or reference-only for VFX. (0.7)

## P4 — Where I expect to be wrong
- The alphabet may need to be *per grammar* as well as per element (a chain link is not a flame tongue recoloured) — the count could be 20+, not 8–12.
- Bursts (impact cores) may genuinely need a drawn 3–5-frame flipbook to read as *painted*; pure erosion of one silhouette may read as "tech".
- The Hades bands may be wrong for field grammars (pools) and aura loops — the strike bands were already flagged as not applying to CAST (R-C3-106).

## P5 — The first experiment I expect to propose
One grammar (thrown-arc → ground field, Blackwater Cocktail) built the P1 way: blockout with a dummy → Matt sees size/timing → 6 fire primitives painted against a per-element anchor → template composes them → oracle measures → Matt judges beside the Frozen Orb v3. If it beats v3 by eye and hits the bands, the second grammar is orbit-emitter (Frozen Orb re-done the new way) as the coherence test: two grammars, two elements, one language.

— gandalf, 2026-09-15
