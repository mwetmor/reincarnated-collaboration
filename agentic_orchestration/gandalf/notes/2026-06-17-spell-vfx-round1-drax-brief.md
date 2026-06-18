# Spell-VFX Round-1 SLICE Brief — drax

**STATUS:** GO — fires now (background). **Author:** gandalf (design steward / orchestrator). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-spell-vfx-runtogreen-log.md` (the tracker + full design direction — READ §1, §2, §4 first; they are the authority).
**Directive (Matt):** *"proceed autonomously until the tri-pod gets it right and replaces the summon circles with meaningful spell effects."*

---

## 0. The job in one line

Transform the descent's **placeholder "summon"** (`_build_hero_vfx`: a frozen ground-glow + fire column) into a **character-driven FIRE spell** that emanates from the caster toward the threat — proven as a SLICE (ONE chamber, war_hall/zone2, ONE element, FIRE) under a **time-sequence** capture. Don't roll out all elements yet; prove the approach on one spell.

## 1. Step 1 — ENUMERATE (don't assume; Discipline #10)

Before building, enumerate every flat-ground-circle / glow element the descent draws, per zone, and tag each against the tracker §2.1 policy:
- **Confirm** the zone2 (war_hall) pale floor disc = the `CombatFill` overhead hotspot (`Color(0.74,0.72,0.80)`, 9m up, line 650/657) — i.e. LIGHTING, **KEEP, FORBIDDEN to touch** (it's 6/6 GREEN-locked). If it's something else, FLAG it to gandalf — do not touch until ruled.
- **KEEP, do not touch:** `_ritual_circle` (sanctum), portal glyph (line 1927), `CombatFill`/`ChamberKey`/`_green_ground_glow`.
- **Check the sibling:** `render_arena_room.gd` (the descent hero-VFX "mirrors" it — comment line 173). Note whether it carries the same summon placeholder (for the eventual roll-out; don't fix it this round).
- Report the enumeration table in your return.

## 2. Step 2 — IMPORT the FIRE-slice FX meshes (substrate → Godot)

From `agentic_orchestration/research/curated/` substrate, the Particle FX Pack zip `fbx/POLYGON_-_Particle_FX_Pack__1464114.zip`, members `Source Files/FBX/FX_*.fbx` (has_godot=0 — NOT imported yet). Import the FIRE-slice shapes into Godot and build `GPUParticles3D` prefabs (alongside the existing `Assets/Particle_FX/Prefabs/FX/` environmental library):
- `FX_Ring_01` — the cast-glyph (flares at the caster, then dissipates)
- `FX_Cone_01`/`_02` and/or `FX_Tower_01` — the projection / eruption body
- `FX_Sphere_Spikes_01`/`_02` and/or `FX_Sphere_Puff` — the impact burst
- (optional) `SM_Flame_FX`, `FX_Spark_01` — fire detail layers

**Reality note (don't burn a round rediscovering this):** Synty ships these as Unity/Unreal particle SYSTEMS — non-portable. The FBX gives you the MESH + the pack's VFX TEXTURES only; **you author the particle BEHAVIOR** (emission shape, velocity, lifetime, color ramp, scale curve) as Godot `GPUParticles3D` + `ParticleProcessMaterial` + an emissive `StandardMaterial3D`/shader. Mesh-emit the shapes where a billboard won't sell depth; use textured billboards for sparks/glow.

## 3. Step 3 — BUILD the character-driven FIRE cast

Rework `_build_hero_vfx` (war_hall path) so the spell is a **VERB emanating from the caster**, not a ground-summon. The lifecycle (this is what the time-sequence will capture):
1. **CHARGE** — `FX_Ring` cast-glyph flares at the CASTER (the player_pos / the caster's hands-or-feet, NOT at `marquee_local`). A momentary telegraph — the magic-circle REBORN (tracker §2.2), not a persistent floor decal.
2. **RELEASE / TRAVEL** — the fire projects from the caster ALONG the `away` axis toward `marquee_local` (`FX_Cone` directional blast, or `FX_Tower` if a rising-pillar reads better). Directionality = combat-intent.
3. **IMPACT** — `FX_Sphere_Spikes`/`_Puff` burst at `marquee_local` (the threat) + a brief warm impact light.
4. **FADE** — dissipate.

**Keep the existing `SummonGlow` warm light as the cast's dynamic light SOURCE** (it's fine — a spell throws light), but **move its character** from a static ground-pool to a cast-following accent (flares at charge at the caster, travels/peaks at impact). Do NOT add lights that perturb the chamber rig's LDR/SHF — the cast light is transient + local, additive to the hero anchor only.

**The criteria you're building TO (tracker §2.4):** emanation-from-caster · motion/lifecycle · element-legible FIRE · points-at-the-threat · premium-layered (core+glow+particles+light, not a flat saturated billboard) · readable at descent camera distance.

## 4. Step 4 — CAPTURE a TIME-SEQUENCE (the instrument must fit the motion)

A single still cannot score a spell (a verb). Render a **sequence** across the lifecycle — e.g. N frames (≥5: charge, release, mid-travel, impact, fade) from the war_hall vantage that reads the cast best. Name them so galadriel can walk them in order (e.g. `descent_spellfx_warhall_seq_01..NN.png`). Local + git-ignored (Synty-derivative). Drive the lifecycle by un-freezing the bake (a `t` parameter / a few discrete `t` snapshots is fine for a static harness — you don't need realtime; you need the LIFECYCLE legible across the strip).

## 5. Process + gates

- **Gate B (confirm):** the GREEN chamber rig is UNTOUCHED — parity 35/35 + Gate-B hold (the spell is additive to the hero anchor, not a lighting change). Confirm, note it.
- **Self-assess + eyes-on:** your own read against §2.4 — does it read as a character casting a FIRE spell at the enemy, or still a ground-summon? Name residuals precisely.
- **Auto-commit** the .gd + import work-products with the `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` trailer; **do NOT push** (Matt-gated). Captures git-ignored, local only.

## 6. Output (your return)

1. The enumeration table (step 1) + the zone2-pale-disc confirmation (CombatFill/KEEP, or flagged).
2. The import + build recipe: which FBX shapes imported, the `GPUParticles3D` prefab structure, the `_build_hero_vfx` rework (the lifecycle you authored).
3. The time-sequence captures (paths) + your eyes-on read against §2.4 (emanation / motion / fire-legible / points-at-threat / premium / readable) + named residuals.
4. Gate-B confirm (rig untouched, parity held).
5. One-line: does the war_hall hero now read as a character-driven FIRE spell (→ slice ready for gandalf eyes-on + galadriel motion-score), or is there a named residual.

---

**Signed:** gandalf, 2026-06-17. Round-1 SLICE: enumerate (confirm zone2 pale disc = KEEP lighting), import FIRE FX-shape meshes → Godot `GPUParticles3D`, transform `_build_hero_vfx` war_hall into an emanate-from-caster FIRE cast (Ring charge → Cone/Tower projection toward the threat → Sphere burst → fade), capture a TIME-SEQUENCE. KEEP all environmental circles + the GREEN-locked lighting (forbidden to touch). Slice-first: one fire spell, one chamber. Auto-commit, no push. GO.
