# UE Character Creation Manifestation Moment — MVP Framing Brief ("Grassy Knoll")

**STATUS:** FRAMING BRIEF (not a fired commission) — groundwork for (a) Radagast UE-feasibility consult, (b) Pattern B scope-lock with Matt, (c) eventual mantis commission via David-H
**Date:** 2026-06-10
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-10 directive — work toward the PC UE Character Creation Manifestation Moment; scope-control constraint "we cannot use the crusader… make one new generic modern day human image gen, pass it to meshy, animate it and then drop it into UE"

**Canonical anchors (read these for the full architecture; this brief scopes the FIRST SLICE):**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (the scene — § 2-§ 12)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 10 (primitive-as-rune-per-group + kit-as-constellation + spherical-shell geometry)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (rune-anchor visual register)
- `canonical/17-...` spirit guide architecture (ambiguous form = spirit-guide-in-becoming)

---

## 0. TL;DR

The canonical creation moment is a SCENE: the player's Earth avatar standing on a hill at night, an ambiguous spirit form beside them, the celestial sphere of constellations overhead — where **the cosmograph IS the night sky** (in-fiction reality, not metaphor). The full architecture layers dual-path creation (Path L lasso / Path I drop-ingredients), a spirit-guide elicitation cascade, cycling-preview UX, and rune-anchor glyphs.

**This brief scopes ONLY the falsifiable-floor first slice: the static scene + atmosphere.** The load-bearing question is experiential, not mechanical:

> *Does standing on the grassy knoll, looking up at the celestial sphere as the night sky, feel like a moment of mythic weight?*

Get the **feeling** right and validated. THEN layer interaction. (Recognition-validate-commit discipline; cosmograph-pivot "substrate landscape engaging from frame one.")

---

## 1. Scene inventory (canonical) vs MVP scope

| # | Scene element | Canonical role | MVP slice | Deferred to later slice |
|---|---|---|---|---|
| 1 | **Grassy knoll / Earth environment** | Player stands on a hill on Earth, night | Ground plane + hill + horizon + night atmosphere | Detailed environment art; biome variation |
| 2 | **Earth avatar** | The Earth Self — persistent player identity; **ordinary modern-day human** (pre-reincarnation) | Single new generic-human asset (pipeline § 2), idle animation, standing on knoll | Customization; multiple avatars; gender/body options |
| 3 | **Ambiguous spirit form** | The spirit-guide-in-becoming; transforms continuously as creation proceeds | Simple ambiguous luminous/ethereal form beside avatar (no transform logic) | Transformation driven by substrate selection; spirit-guide identity reveal |
| 4 | **Celestial sphere (cosmograph)** | The night sky IS the cosmograph; stars = primitives, constellations = kits | Star field on the sphere interior surface, read as a real night sky with depth | Substrate-accurate star positions (kit-cluster mapping); lasso targeting |
| 5 | **3D nebula context** | Volumetric depth beyond the sphere (clouds, distant galactic structures) | Skybox/HDRI + simple atmospheric depth | Niagara volumetric nebula; parallax depth |
| 6 | **Rune anchors** | Primitive-anchor groups as archaic glyphs — large, atmospheric, light-edge brush-stroke, monochromatic (Tal Rasha register) | **DECISION POINT** — include 1-2 placeholder runes to test the visual register in 3D, OR defer entirely | Full per-group rune curation (Pattern B); two-tier selection |
| 7 | **Camera / POV** | Ground level, looking UP at sphere interior; spherical-shell geometry | Fixed or gently controllable look-up framing | Free-look; lasso camera; path-driven framing |
| 8 | **Lighting / mood** | Mythic weight; sky is the dominant element | Dusk-to-night lighting; sky-dominant composition | Dynamic time-of-creation lighting; spirit-glow interplay |

**Explicitly OUT of the MVP first slice:** Path L lasso, Path I drop-ingredients, spirit-guide cascade UI, cycling-preview, kit lookup, spirit-form transformation, finalized rune curation. These are the *interaction* and *substrate-binding* layers — they come after the scene feeling validates.

---

## 2. Earth-avatar asset pipeline (Matt 2026-06-10 — no Crusader)

**Constraint:** do NOT reuse the Crusader GLB. Produce one new generic modern-day human.

**Pipeline:**
1. **Image-gen** — one generic modern-day human. Design intent: *ordinary, contemporary, neutral.* This is the Earth Self before reincarnation — the contrast against the ambiguous spirit form is the visual story (the mundane human vs the becoming). Full-body, front-facing, clear silhouette, neutral pose (A-pose friendly for rigging). Contemporary casual clothing; no fantasy elements.
2. **Meshy** — image → 3D model (image-to-3D; GLB out). This is the substrate-grounded asset pipeline (image-pass-through-to-Meshy = the asset-layer analog of substrate-grounded provenance per gandalf OP § 3.3 / D7).
3. **Animate** — idle/standing animation (Mixamo auto-rig + idle, or Meshy native). MVP needs only a calm idle for "standing on the knoll, looking up."
4. **Drop into UE** — import as the Earth-avatar placeholder in the scene.

**Note:** "placeholder" = correct for MVP. The avatar is a stand-in to validate scene composition + scale + the human-vs-spirit contrast; it is not the final customizable Earth Self.

---

## 3. Falsifiable-floor acceptance criteria (MVP)

The MVP passes if a viewer, dropped into the scene, reads ALL of:
1. "I am standing on Earth, on a hill, at night." (environment + POV)
2. "There is a sky full of stars/constellations above me, and it has depth — it's not a flat backdrop." (celestial sphere reads as cosmograph-night-sky)
3. "There is an ordinary modern person standing here." (avatar reads as Earth Self)
4. "There is an ambiguous, ethereal presence beside them." (spirit form reads as becoming)
5. **The integrative judgment (Matt's call):** "This feels like a meaningful, mythic creation moment." — the load-bearing subjective gate.

If #5 fails, the scene is iterated BEFORE any interaction work is commissioned.

---

## 4. Open questions for Radagast consult + Pattern B scope-lock

**For Radagast (PC design steward — UE feasibility + current asset/scene inventory):**
- Celestial sphere stars: Niagara point-cloud vs static mesh/material on a sphere shell — which gives the night-sky depth read most cheaply?
- Nebula context: skybox/HDRI vs early Niagara volumetric for the MVP?
- Spherical-shell geometry: practical UE setup for "ground POV looking up at sphere interior" (inverted sphere mesh? sky sphere? cubemap?)
- Existing reusable scene/lighting assets in `reincarnated-unreal` that the MVP can build on (post-WS3.1 + Session-3 groundwork)
- Meshy→UE import path already proven for Crusader — does the generic-human GLB follow the same path cleanly?

**For Pattern B with Matt (scope-lock before commission):**
- Rune anchors in the MVP scene (test the Tal Rasha register in 3D early) or defer to post-scene-validation? (Scene-element #6 decision point.)
- Camera: fixed cinematic framing vs player-controllable look-up for the MVP?
- Spirit form: simple luminous placeholder vs an early hint of transformation?
- How "finished" must the environment art be for the #5 mythic-weight judgment to be fair? (Risk: judging the *feeling* against obviously-placeholder art.)

---

## 5. Discipline guards (carry into the commission)

- **Recognition-validate-commit (OP § 3.4):** scene feeling validates BEFORE interaction layers are commissioned. Empirical criterion = Matt's #5 judgment on the assembled scene.
- **D7 AI-tell line (OP § 3.3):** avatar is image-gen → Meshy substrate-grounded pipeline; no raw-LLM player-facing surfaces in this scene.
- **Substrate-led (OP § 3.1):** MVP star positions are SCAFFOLD (placeholder); flag explicitly as scaffold-with-pending-decision (Discipline #40). Substrate-accurate kit-cluster→constellation mapping is a later slice, not faked-as-final in MVP.
- **Scope-control (Matt 2026-06-10):** no Crusader; one generic human; first slice is scene-feeling only. Resist creep into interaction/binding layers (the failure mode for a scene this evocative is building the whole interactive cosmograph at once).
- **Composes with WS2 Niagara commission** (queued, gandalf desk) — the celestial-sphere stars + spirit-form VFX + rune-anchor light-edge brush-stroke register are the Niagara components of this scene. WS2 should be scoped as a component of the manifestation-moment MVP, not a standalone.

---

## 6. Sequencing (recommended)

1. **PC env hardened** (WSL+tmux) — in flight; enables long mantis orchestration without disconnect loss.
2. **Radagast UE-feasibility consult** (§ 4) — once PC env solid.
3. **Pattern B scope-lock with Matt** (§ 4) — resolve rune-in-MVP, camera, spirit-form, art-finish-bar questions.
4. **Avatar pipeline** (§ 2) — image-gen → Meshy → animate → UE (can run in parallel with 2-3).
5. **mantis commission via David-H** — gandalf authors math/spec-first commission absorbing WS2 Niagara components; mantis executes; Sam Gate-2; Radagast critique-pair.
6. **Matt #5 judgment** on assembled scene → validate → THEN commission interaction layers.

---

**End of framing brief.** This is groundwork, not a commission. The commission fires after § 6 steps 2-3.
