# Spell-VFX Run-to-Green — Tracker + Design Direction

**STATUS:** 🟡 OPEN — Round-1 cast LANDED (PASS-with-residual); substrate head-to-head RESOLVED on Matt's eyes-on (2D-as-thrown-projectile DIRECTIONAL fail, 3D-particle won the projectile role, neither hit PoE/D2 register); LAYERED-COMBO slice BUILDING (drax). Governing directive (Matt 2026-06-17): *"proceed autonomously until the tri-pod gets it right and replaces the summon circles with meaningful spell effects."*
**Orchestrator / design steward:** gandalf. **Builder:** drax (Godot). **Scorer:** galadriel (CV / perception).
**Parent run (CLOSED GREEN, the model for this one):** `2026-06-17-descent-runtogreen-log.md`.
**Substrate ruling:** `2026-06-17-synty-acquisition-run-ruling.md` (Particle FX Pack = POLYGON-line cross-cutting KEEP).

---

## 0. The ask + scope ruling

Matt: *"KR finished the synty asset run. Do we have any character-driven VFX (i.e. spells) that can replace the summon circles?"* → *"please proceed autonomously until the tri-pod gets it right and replaces the summon circles with meaningful spell effects."*

**Answer to the literal question:** yes — substrate exists (POLYGON Particle FX Pack, 58 effect-MESH assets + VFX textures), but it is a MESH+texture substrate, NOT turnkey particle systems. Synty ships behavior as Unity/Unreal particle systems (non-portable); the **spell behavior must be AUTHORED as Godot `GPUParticles3D` + shaders** from the mesh/texture parts. drax builds that.

**Scope ruling (the tripod's lane):** "summon circles" = a **design category**, not one mesh — *any flat ground-anchored magic-circle/glow standing in as the placeholder representation of the character's combat spellcasting.* This run operates on the **Godot descent surface** (the tripod's domain). Cross-surface summon-circle placeholders in `reincarnated-demo` (2D Pixi) are OUT of this run's scope (different surface, different tripod) — noted for a follow-on.

---

## 1. What EXISTS (survey-mode — what IS, before any "should")

**`render_descent_scene.gd` `_build_hero_vfx` (line 777) — THE summon, the target:**
- `SummonGlow` — OmniLight3D, warm red `Color(1.0,0.18,0.08)`, energy `SIGIL_LIGHT_CHARGE=6.0`, range 8.0, at `anchor+(0,0.6,0)`. A warm pool on the ground.
- `SummonFireColumn` — `FX_Fire_Large_01` GPUParticles3D, at `anchor + away*1.8 + (0,0.1,0)`, scale `(0.55,0.7,0.55)`. **Frozen at erupt** (`SIGIL_LIGHT_CHARGE`, "frozen erupted for bake" — comment line 776).
- `anchor = marquee_local` (the highest-threat-tier mob position; the combat focus). The summon sits at the THREAT, offset from the player by `away*1.8`.
- Comment line 1882: *"the 6/6 ruling keeps the hero disc out"* — a prior hero DISC was already removed; this glow+column is its replacement. It still reads as a ground-summon, not a cast.
- The hero-VFX **"mirrors `render_arena_room.gd`"** (comment line 173) — a SIBLING arena render shares this pattern. drax enumerates whether it carries the same summon placeholder.

**KEEP-set (do NOT touch — ruled environmental / GREEN-locked):**
- `_ritual_circle` (line 1884) — dark-red emissive `SM_Prop_Ritual_Circle_01.tscn`, sanctum cathedral set-dressing. Diegetic. KEEP.
- Portal threshold glyph (line 1927) — faint violet `SM_Prop_Ritual_Circle_01.tscn` @ emission 0.45. Gateway decal. KEEP.
- **Chamber lighting pools** — `CombatFill` (line 650), `_build_chamber_key` (line 672), `_green_ground_glow` (line 1674). These are the **6/6 GREEN-locked lighting rig.** The pale flat disc in the zone2 (war_hall) still is the `CombatFill` hotspot directly under the 9m-overhead pale `Color(0.74,0.72,0.80)` light — it is LIGHTING, not a placeholder prop (`_dress_warhall` has no disc mesh). **Touching it re-opens the closed chamber gate. Forbidden.**

**Substrate (Particle FX Pack — `fbx/POLYGON_-_Particle_FX_Pack__1464114.zip`, `Source Files/FBX/FX_*.fbx`, has_godot=0, NOT imported):**
shapes available — Ring, Cone(×2), Cylinder(×2), Sphere/_Spikes/_Puff/_Pivot, Tower, Shard_Rock(×4)/_Small, Vine(×3), Crystal(×4)/CrystalShard, Star/_Pivot, Arrow(×2), Bullet_Trail, Spark, Cloud_Placement, LightRayCube/Round, SunShafts, Flame_FX, Smoke. **Existing Godot FX prefab library is ENVIRONMENTAL-only** (Fire/Fog/Smoke/Dust/Rain/Snow/Leaves/Candle/SunBeam) — NO spell-shape prefab exists yet; the shapes above must be imported + authored into `GPUParticles3D`.

---

## 2. DESIGN DIRECTION (gandalf — the seam I own)

### 2.1 Keep / Replace / Transform policy

| element | policy | why |
|---|---|---|
| `_build_hero_vfx` (SummonGlow + frozen SummonFireColumn) | **TRANSFORM** | the literal placeholder summon → character-driven spell |
| `_ritual_circle` (sanctum), portal glyph | **KEEP** | diegetic environmental dressing, already ruled |
| `CombatFill` / `ChamberKey` / `_green_ground_glow` | **KEEP — FORBIDDEN to touch** | 6/6 GREEN-locked lighting; the zone2 pale disc IS this |
| any flat ground-circle drax finds NOT in the above | **FLAG to gandalf** | enumerate, do not assume; I rule keep/replace |

### 2.2 The reframe — the magic-circle is REBORN, not deleted

Do NOT simply delete the ground glyph. The elegant move (and the isekai-native one): the magic-circle becomes a **momentary cast-telegraph** — `FX_Ring` flares at the caster's hands/feet at cast-START, then EMANATES the spell and dissipates. The circle stops being a persistent placeholder decal and becomes the **first beat of a spell verb.** (Mushoku Tensei / Frieren cast-glyphs flare and fire; they don't sit on the floor as furniture.)

### 2.3 Element × geometry mapping (the substrate → spell vocabulary)

- **FIRE** → `FX_Ring` cast-glyph → `FX_Cone`/`FX_Tower` projection → `FX_Sphere_Puff`/`_Spikes` burst + `SM_Flame_FX`
- **ICE/WATER** → `FX_Crystal` + `FX_CrystalShard` + `FX_Cone` (frost cone)
- **EARTH** → `FX_Shard_Rock` + `FX_Vine` + `FX_Tower` (stone pillar)
- **WIND** → `FX_Cone` + `FX_Ring` (vortex) + `FX_Cloud_Placement`
- **ARCANE/LIGHTNING** → `FX_Star` + `FX_Spark` + `FX_Ring` + `LightRay`
- **HOLY/LIGHT** → `SM_LightRayRound`/`Cube` + `SunShafts` + `FX_Star`
- **RANGED (phys)** → `FX_Arrow` + `FX_Bullet_Trail`

### 2.4 "Meaningful spell effect" — acceptance criteria (genre-anchored)

A spell PASSES as character-driven (vs summon-circle) iff ALL hold:
1. **Emanation-from-caster** — originates at the character's body/hands, travels/projects. (Diablo Sorceress Firebolt emanates from her hands; PoE spells originate at the character. Ground-spawn-glyph = the anti-pattern we kill.)
2. **Motion / lifecycle** — charge → release → travel → impact → fade. A spell is a VERB. (This is why the gate is a TIME-SEQUENCE, not a still.)
3. **Element-legibility** — reads as its element at a glance, no label (fire = orange/red billow + sparks; ice = cyan/white crystalline shards). Diablo/PoE element-tells.
4. **Directionality / combat-intent** — points at the threat (the marquee). The eye reads "the character is doing THIS to THAT enemy," not ambient decoration.
5. **Premium register** — punchy against the dark, layered (core + glow + particles + light), matching the chambers' dark-fantasy register. NOT a flat saturated billboard.
6. **Readability (mobile-first)** — silhouette + color legible at descent camera distance + thumbnail scale.

**ANTI-patterns (a FAIL looks like):** persistent flat ground glyph w/ no emanation · a frozen column that doesn't read as motion · a flat saturated billboard (the portal-square anti-pattern the rework killed) · element-ambiguous mush · decoration that doesn't point at the enemy.

---

## 3. THE DUAL GATE (same discipline that held the descent four directions)

- **Gate A — perception (galadriel):** scores the **TIME-SEQUENCE** (charge→release→travel→impact→fade), not a frozen frame. Instrument must measure: motion-presence (frame-to-frame change along the cast axis), element-hue legibility, emanation-origin (energy starts at caster, not at ground-center), premium register (layered, punchy-in-dark, not flat-saturated). New instrument — the static register-2 scorer does NOT fit motion VFX (this is why descent VFX was "inherited PASS": a frozen-charge still can't score a spell).
- **Gate B — composition + load-path (gandalf rules / drax builds):** builds clean + deterministic; the GREEN chamber rig is UNTOUCHED (parity + Gate-B hold trivially — VFX is additive to the hero anchor, not a lighting change — but CONFIRM); the spell reads as a character-driven cast per §2.4 on my eye.
- **Anti-confirmation-bias (descent Round-2 lesson):** gandalf eyes-on recorded BEFORE galadriel's numbers; rule on CONVERGENCE, not either eye alone.

---

## 4. SLICE-FIRST (the disciplined Round-1)

Per slice-first discipline (and the Synty downloader gate KR just applied): Round-1 proves **ONE character-driven spell in ONE chamber** reads as a meaningful spell under the time-sequence instrument, BEFORE rolling out all elements/chambers. De-risks the `GPUParticles3D`-from-Synty-mesh approach on one spell, not six.

- **Slice chamber:** war_hall (zone2) — the arbiter chamber, the most-prominent placeholder read, a pure combat chamber (not the sanctum).
- **Slice element:** FIRE — matches the current placeholder (minimal variable change; we test summon-circle→cast, NOT an element swap). `FX_Ring` cast-glyph at caster → `FX_Cone`/`FX_Tower` projecting toward marquee → `FX_Sphere_Spikes` burst at impact.
- **Slice capture:** a TIME-SEQUENCE strip (N frames across the lifecycle), local + git-ignored (Synty-derivative).

---

## 5. ROUND LOG

### Round-1 — drax RETURNED (godot `3b1daa2`); galadriel FIRING
- **drax:** ✅ returned. Enumeration confirms zone2 pale disc = `CombatFill` lighting = KEEP (untouched); no stray circle flagged. Imported 8 FIRE FX-shape FBX → authored `_build_spell_lifecycle` + reworked `_build_hero_vfx` war_hall as a CODE-authored cast (license discipline: builder code, not git-ignored `.tscn`). 7-frame time-sequence rendered. Gate-B PASS (parity 35/35; diff = 2 hunks only, zero lines in any KEEP-locked lighting/circle fn). **Crux banked:** Godot silently ignores FBX under a nested `project.godot` subtree — import OUTSIDE `polygon-starter/`. **Sibling:** `render_arena_room.gd` carries the SAME summon placeholder (roll-out target, untouched this slice).
- **gandalf eyes-on (recorded BEFORE galadriel):** transformation LANDED — emanation-from-caster ✅, motion/lifecycle ✅ (energy travels caster→threat, reads as a verb), fire-legible ✅(mostly; charge-ring red leans slightly magenta), readable ✅. **Two convergent residuals (gandalf eye + drax self-assess AGREE):** (a) mid-travel bolt (frames 04–05) reads SOFT — fire-bloom not crisp aimed projectile; (b) directionality reads as "fire migrates rightward," not a bolt aimed at a specific marquee target. Approach is PROVEN; residual is crispness/polish, not a fundamental failure.
- **galadriel:** ▶ FIRING (background) — motion-score request patched + live (`2026-06-17-spell-vfx-round1-galadriel-motionscore-request.md`). NEW 5-metric time-sequence instrument; headline = energy-travel caster→threat. Tasked to CONFIRM-or-REFUTE the two named residuals (metrics 1/4/5).
- **gate / next:** rule on CONVERGENCE — if galadriel confirms the soft-bolt + weak-directionality residuals → targeted drax Round-2; if clean → slice-GREEN → roll out.

### ⚠ SUBSTRATE INTERRUPT (2026-06-17) — pixel-VFX proposal → register-conflict ruling
Matt (via a Gemini consult) surfaced the demo's purchased VFX catalogue (`reincarnated-demo/public/assets`) + a Gemini spec to route 2D flipbook VFX through Godot's 3D billboard pipeline, as a candidate to replace the soft Round-1 mesh-spell. **Inspected (Discipline #10):** the catalogue is the demo's PIXEL-ART substrate — metadata `derived_register: "hand-drawn-pixel"`, 32–160 px/frame, Holy sheets on un-keyed white bg. **Ruling (`pushback/2026-06-17-pixel-vfx-into-godot-register-conflict.md`):** routing pixel flipbooks into the smooth-Synty-3D descent REVERSES the LOCKED register (`style-register.md`, 2026-06-14 Matt/Pattern-B; A-locks 4.50→5.00/5; 2D-pixel SUPERSEDED) and downgrades a 3D-native VFX strategy already scored **VFX-presence 5/5** (`FX_Fire_Large_01` bloom) to a retired register. Gemini's flipbook TECHNIQUE is sound but mis-sourced (PoE/Diablo flipbooks are smooth-HDR, not pixel). **The soft-mesh residual's correct fix = the register-lock's OWN lever: S-tier `GPUParticles3D` particle juice, NOT geometric Synty meshes, NOT pixel flipbooks.** → **Round-2 redirect PENDING Matt's call:** (rec) particle-juice redirect, register stays locked; (only-if-intended) re-open register to pixel-hybrid = whole-art-direction pivot discarding the Synty-3D descent. Escalated to Matt (above tripod authority). Pixel catalogue retained for the 2D demo (pivot-insurance).

### Round-1 motion-score — galadriel RETURNED (`82a3ac4`): PASS-with-residual, CONVERGES
galadriel's NEW 5-metric time-sequence instrument (`galadriel/pipeline/spell-motion-score.mjs`) scored the war_hall fire cast **PASS-with-residual**, INDEPENDENT of gandalf's eye, and CONFIRMED both named residuals (cross-check working, not anchoring):
- **Metric 1 ★ energy-travel PASS** — +1.012 caster→threat axis-march (F02 at-caster → F06 at-threat); +19.6% frame-width. Textbook emanation. Metric 2 motion-presence PASS; Metric 3 fire-hue PASS (deep-red→amber lifecycle, R>G>B); backdrop-invariance PASS (rig untouched, additive cast).
- **Residual (a) soft mid-travel CONFIRMED** — metric 4: F04 layering 8.55 AT the 9.0 flat-cardboard line vs impact 10.4–11.8 (~25% structure deficit). The soft beat is the GEOMETRIC-MESH travel-bolt — corroborates that the fix is particle-juice, not mesh.
- **Residual (b) aim-drift CONFIRMED** — metric 5: principal axis horizontal (8–20°) vs threat-line −22.5°, alignment loosens cos 0.86→0.74. Shaped but not threat-locked.
The transformation LANDED (summon-glyph genuinely replaced by a cast verb); residuals are crispness/aim polish, not fundamental failure.

### SUBSTRATE HEAD-TO-HEAD (2026-06-17) — RESOLVED on Matt's eyes-on
Rather than adjudicate the register conflict on paper, Matt called for a controlled head-to-head VIDEO: same war_hall + 2.5D cam + fire beat, two substrates (drax commit `824a5d9`, both LOCAL/git-ignored mp4):
- **Video A** = juiced Synty/`GPUParticles3D` particle fire (`_build_spell_lifecycle_juiced`).
- **Video B** = pimen "Fire bite" 2D flipbook (64px native) wired into 3D as a thrown projectile (full 3-phase technique — NO strawman; drax gave the 2D path its strongest fair shot).
gandalf independent eyes-on (frames pulled from each) + drax self-assess CONVERGED with Matt's read.

**Matt's verdict:**
- **2D flipbook FAILS as a THROWN PROJECTILE** — root cause is a MOTION-ROLE mismatch, NOT resolution: the flame's internal animation licks UPWARD (stationary-burn convection) but it was propelled FORWARD, so internal motion fights travel — reads as "a stationary fire oddly sliding sideways." Genre corroboration: D2 authors fire TWICE — Fire Bolt streaks forward (projectile), Meteor leaves upward-licking ground fire (stationary); PoE same (Fireball streaks; Ignite/Burning-ground licks up). pimen is a stationary-burn asset in the wrong role.
- **Synty 3D particle WON the projectile role** (occupies volume + travels correctly).
- **Matt LIKED the 2D flame's stylized look** + observed it would PASS as STATIONARY fire (upward animation correct when anchored).
- **Neither video hit the PoE / D2 register.** A "won" the substrate question but is below the genre bar — gap NAMED: missing AAA techniques (alpha-erosion-via-noise, flowmap churn, smooth-HDR layer textures) + the bright war_hall starving the fire of dark-mood contrast.

**Design distinction (the load-bearing read):** TWO separable tells — (1) resolution mismatch (asset-specific, partly fixable with higher-res) vs (2) DIMENSIONAL mismatch (a flat billboard vs effects that occupy volume — STRUCTURAL to any flipbook-in-3D, NOT fixed by resolution; a flipbook is paint on a card, particles occupy depth). The pixel question is SETTLED; the SMOOTH-flipbook-vs-particle question (tell 2 alone) is NOT yet tested.

### FINDING — 2D-as-projectile: DIRECTIONAL recommendation (NOT absolute; door OPEN, per Matt)
Recorded per Matt's explicit instruction — directionally recommend, do NOT close the door:
- **Directional default:** 2D flipbook VFX default to STATIONARY-fire roles (impact flames, burning ground, torches/ambient) — NOT traveling projectiles. Motion-role discipline: **2D = stationary, 3D = travel/volume.**
- **Why DIRECTIONAL not ABSOLUTE (scope of the evidence):** the observed failure was a STATIONARY-BURN asset (pimen Fire-bite) used as a projectile. We have NOT tested a 2D flipbook AUTHORED with forward-STREAKING directional motion (comet/meteor-style — internal motion along the travel axis).
- **Door left OPEN — future test:** "directional 2D" — a forward-streaking-authored 2D flipbook as a projectile — remains an OPEN question to test at a later date. The recommendation is a default LEAN pending that test, NOT a prohibition. Do NOT record it as "all 2D VFX must never be projectiles."

### DIRECTION SET (Matt) + ROUND-2 = LAYERED COMBO (BUILDING NOW)
- **Combo slice (drax FIRING, background):** Synty 3D fireball TRAVEL → on IMPACT, 2D stationary fire (pimen flame, anchored, burning-in-place where its upward animation is correct) + lingering ground-fire, LAYERED with the existing particle burst. Proves the **LAYERING principle** (AAA spell VFX = stacked layers, never one effect) + validates 2D-as-stationary in its right motion-role. war_hall, same vantage (comparable to the head-to-head). Video + time-sequence; galadriel motion-score to follow.
- **The REAL target (recognition — deferred design doc, gandalf-owned):** the **COMBINATORIAL VFX-LAYER SYSTEM** for **400 kits** at genre register. Can't hand-author 400; the genre doesn't — PoE runs hundreds of skills off a shared PARAMETERIZED layer library (recolor by element, rescale by tier, compose by rule); Last Epoch specialization trees add/swap composable layers; D4 tints a base. Answer to 400-kits AND to quality is the SAME: **author quality once per composable LAYER** (core/trail/impact/ground-fire/ember/light — each 2D-stationary or 3D-volume per role) × element-parameterization × the §2.3 element×geometry mapping; compose per kit, not bespoke. Quality lives in the layers, not per-kit.
- **Quality spike (deferred):** prototype alpha-erosion + flowmap + smooth-HDR layer texture on the particle layers in a DARK chamber → tests reaching PoE/D2 register + re-opens the smooth-texture-SOURCE question on real evidence. (The UE-Marketplace-VFX option, opined this session: techniques sound + register-correct SMOOTH source, but per-asset licensing is NOT blanket engine-portable [FAB restructured it] + premature vs the proven lever → adopt the TECHNIQUES, defer the pipeline; cleanest smooth-HDR source = EmberGen [royalty-free, engine-agnostic] first.)

---

**Signed:** gandalf, 2026-06-17. Spell-VFX run-to-green opened. Target = `_build_hero_vfx` (the placeholder summon); KEEP = environmental ritual circles + GREEN-locked lighting (incl. the zone2 pale CombatFill disc — forbidden to touch). The magic-circle is REBORN as a cast-telegraph, not deleted. Gate is a TIME-SEQUENCE (a spell is a verb). Slice-first: ONE fire spell, ONE chamber, then roll out.
