# ADJUDICATION — V1 juiced-Binbun fireball in the CURRENT war_hall (in-context pass test)

**Author:** gandalf (design steward — the in-context PASS/FAIL is my call). **Date:** 2026-06-19. **Type:** design adjudication + rollout recommendation (Matt ratifies the rollout + buy/build).
**Trigger:** Matt — *"add the best output of the test [V1] into the godot game and show me a video... replace the summoning circles with this if it passes there as well."* Plus the mid-flight correction: *"these are very old rooms/clips. Why not use the current rooms/clips?"* (the first integration targeted the stale Jun-15 boss arena; this is the retarget to the CURRENT room).
**Inputs:** drax retarget — `harness_logs/spellfx_v1_warhall.mp4` + 6-beat frame-strip `spellfx_v1_warhall_{01_charge..06_fade}.png` (I viewed all six). V1 byte-identical to the register-test winner (Binbun `fire_ball_01`+`fire_trail`, `blend_add`, `emission_energy=2.0`, +32 `V1_Ember`); no hue-lock pre-applied (judged as-is, per Matt). Room = war_hall (`Zone3_elite_pack`) in `arena_descent.tscn`.

---

## VERDICT: **PASS in context** — and it passes in the chamber that gives it the LEAST help.

V1 reads as a premium, **directed** fire projectile with a legible charge→release→travel→impact→burn→fade arc, occupying real 3D volume, the bloom + cast-light integrating with the chamber. As a replacement for the placeholder summon VFX: **yes.** The one defect (white-hot impact core) is the exact register-test-predicted blowout, is a known cheap in-engine fix, and is **amplified by the worst-possible chamber** — so this is V1 at a disadvantage still reading premium.

---

## 1. Beat-by-beat (my own eye — the dual-gate, not drax's read on faith)

- **charge / release:** fire kindles at the hero's hands and grows — clean cast initiation, the FX_Ring charge-glyph + cast-light present.
- **travel:** the fireball is mid-air between hero (left) and threat (right), moving the **right way** — **directionality fix confirmed on-frame** (this is the backwards-routing bug Matt flagged, now resolved). It occupies real volume with a glowing additive halo.
- **impact / burn:** bursts at the threat, embers fly — the brightest beats, and **where the white-hot core washes toward white** (drax's read confirmed; matches the register test's ~22–26% achromatic-blowout finding).
- **fade:** dissipates with residual embers — clean tail.

## 2. The one cost — and why the war_hall amplifies it

The white-hot impact core is the **single** quality defect (NOT a legibility failure — you unambiguously read "fireball hits, fire burns"). Two compounding causes, both environmental, neither a backbone cap:
1. **Additive-on-bright:** the war_hall is the **brightest/coolest chamber** in the descent (`key_energy 3.4`, cool fill). Additive bloom needs **dark** to glow against; here it has almost none, so the hot core reads as a white blob rather than incandescent fire.
2. **Isolated warm event:** the warm fire sits on a **cool blue-purple floor** with no warm environmental motivation around the impact — the fire doesn't feel *of* the space.

**Corollary (the useful intelligence):** the war_hall told us the FLOOR of V1's quality; a **dark chamber** (oubliette / sanctum / cathedral) would show the CEILING — same V1, dark to bite against, warm fire motivated by dark-fantasy mood.

## 3. Two cheap levers (neither is a harvest)

1. **The deferred hue-locked-core + additive-halo fix** (the V1.1 fix already named in the 2026-06-18 verdict) — additive only the glow halo, preserve the core color; tames the white blowout. In-engine, no new assets.
2. **Deploy hero fire-casts in the darker chambers** — a juice-craft placement rule, free.

## 4. What this means for the buy/build (the Hovl-harvest question)

This **confirms the 2026-06-18 MARGINAL verdict's core call**: the Binbun backbone is **register-viable**, the gap is **in-engine-fixable**, **no Hovl harvest needed**. Seeing V1 in real descent geometry — directed projectile, legible lifecycle, premium read, all in-engine — is the **strongest evidence yet** for defer-harvest. The only open quality lever (hue) is a tuning knob, not a wall.

## 5. Process notes (from drax's run)

- **Parity:** `check_descent_parity.py` PASS, 35/35 spawns / 6 zones (before + after). **Gate B held** (`arena_descent.tscn` + `render_descent_scene.gd` unmodified; only the runtime war_hall HeroVFX rebuilt).
- **§8 hygiene:** both harnesses self-closed (quit-on-complete + 120s watchdog). No orphaned windows.
- **Latent bug caught:** the boss harness instantiated `fire_trail.tscn` (root is `Node3D`) `as GPUParticles3D` → silent null → the **earlier boss V1 clip's trail never rendered**. Fixed in the new war_hall harness only (drax did not touch the boss file). Another mark against the stale boss clip beyond the wrong room.

## 6. RECOMMENDATION (Matt ratifies the rollout)

**Greenlight V1 as the hero-cast fire substrate + apply the hue-lock fix, then roll it into the remaining summon contexts** (`render_arena_room.gd` still runs the old `SummonGlow`+`SummonFireColumn` placeholder; line ~176 of `render_descent_scene.gd` already flagged "roll the proven cast in after the slice goes GREEN" — the slice is now green-in-context). Options for Matt:
- **(A, recommended)** Greenlight + hue-lock + roll out to the other placeholders.
- **(B)** Greenlight + judge once more in a dark chamber (oubliette/cathedral) before committing the rollout.
- **(C)** Apply hue-lock first, re-render the war_hall, then decide.

My call is **A** — it's a clear yes on the substrate, the hue-lock is cheap and unambiguously correct, and the rollout retires the placeholder everywhere. The dark-chamber render (B) is worth doing as the *showcase* frame regardless, but it isn't a gate on the substrate decision.

---

**Signed:** gandalf, 2026-06-19. V1 PASSES in the current war_hall — directionality fixed, lifecycle legible, premium read in the chamber that helps it least. The white-hot core is the one cost: register-predicted, in-engine-fixable (hue-lock), and chamber-amplified. Confirms defer-harvest. Recommend greenlight + hue-lock + roll the V1 cast into the remaining summon placeholders. Matt ratifies.
