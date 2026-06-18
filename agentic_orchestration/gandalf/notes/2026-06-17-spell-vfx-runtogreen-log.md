# Spell-VFX Run-to-Green — Tracker + Design Direction

**STATUS:** 🟡 OPEN — Round-1 SLICE staged (drax). Governing directive (Matt 2026-06-17): *"proceed autonomously until the tri-pod gets it right and replaces the summon circles with meaningful spell effects."*
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

### Round-1 — STAGED (drax brief: `2026-06-17-spell-vfx-round1-drax-brief.md`)
- drax: enumerate all flat-ground-circle elements per zone (confirm zone2 pale disc = CombatFill = KEEP; flag any stray); import the FIRE-slice FX-shape meshes from the Particle FX Pack zip → Godot `GPUParticles3D` spell prefabs; transform `_build_hero_vfx` war_hall into the character-driven FIRE cast; render the time-sequence; self-assess + eyes-on; auto-commit, NO push.
- gandalf: rule eyes-on (BEFORE galadriel) on §2.4 criteria.
- galadriel: build the motion-scoring instrument + score the sequence.
- **gate:** §2.4 all-hold + Gate-B parity/rig-untouched + galadriel motion-score PASS → slice GREEN → roll out remaining elements/chambers.

---

**Signed:** gandalf, 2026-06-17. Spell-VFX run-to-green opened. Target = `_build_hero_vfx` (the placeholder summon); KEEP = environmental ritual circles + GREEN-locked lighting (incl. the zone2 pale CombatFill disc — forbidden to touch). The magic-circle is REBORN as a cast-telegraph, not deleted. Gate is a TIME-SEQUENCE (a spell is a verb). Slice-first: ONE fire spell, ONE chamber, then roll out.
