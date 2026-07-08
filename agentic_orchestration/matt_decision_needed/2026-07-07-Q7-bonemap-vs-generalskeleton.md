# Q7 — Skeleton-retargeting approach for the v2 Godot demo: BoneMap vs GeneralSkeleton

> **STATUS:** ✓ RULED 2026-07-07 (Matt) — **Option A as recommended** (authored per-variant BoneMaps → GeneralSkeleton; superset nuance adopted: author a `.tres` ONLY where a rig needs one). Decisions-log entry: engine `design/decisions/decisions-log.md` "2026-07-07 — Q7 RULED (Option A)". **Author:** drax (presentation seam). **Date:** 2026-07-07.
> **Scope:** ONLY the Synty POLYGON rig → animation retargeting path in `reincarnated-godot/`. Q8 Camera B is APPROVED and fixed (FOV 40 / pitch −55° / yaw 47°) — not re-litigated here. *(Dist superseded post-ruling: 34 m → **20 m** per the Camera B′ dist-only revision, engine `a0bf7fd` — all capture configs fire at dist 20.)*
> **This fire = the brief only.** On Matt's ruling, drax executes the chosen path immediately (D6/D5/D8 render/capture layers, currently rig-gated).

---

## 0. Framing correction (load-bearing — read first)

"BoneMap" and "GeneralSkeleton" are **not two competing systems.** In Godot 4.x they are two halves of one mechanism:

- **`GeneralSkeleton`** is the *target*: Godot's built-in humanoid reference skeleton (`SkeletonProfileHumanoid` — the 56-bone Hips/Spine/…/Head/LeftUpperArm/… profile). Every retargeted rig in this project already normalizes to a skeleton literally named `GeneralSkeleton`. It is the destination, not an alternative path.
- **`BoneMap`** is the *mapping resource* (`.tres`) that tells the importer which of a source rig's raw bones correspond to each GeneralSkeleton profile slot (e.g. `Hips→pelvis`, `LeftUpperArm→upperarm_l`).

So the real Q7 fork is **how we produce the source→GeneralSkeleton mapping for each Synty rig variant**:

- **Option A — Authored per-variant BoneMaps** (hand-authored `.tres` per rig family, injected at import). **This is the pipeline already built and proven in-repo.**
- **Option B — Auto-mapped GeneralSkeleton** (rely on Godot's import-time `SkeletonProfileHumanoid` auto-detection to guess the mapping; no bespoke per-variant `.tres`).

The decision is A vs B. Both land on `GeneralSkeleton`.

---

## Option A — Authored per-variant BoneMaps → GeneralSkeleton

### (a) What it is / how it works in Godot 4.x
A hand-authored `BoneMap` resource per Synty rig family. At FBX import, `retarget/bone_map` points the importer at the `.tres`; `retarget/bone_renamer` renames the source rig's raw bones to GeneralSkeleton profile names; `retarget/rest_fixer` (with `fix_silhouette/enable=true`) rotates the retargeted **rest** so arms hang at the sides matching the source A-pose. Output: a skeleton named `GeneralSkeleton` carrying humanoid bone names, on which any already-GeneralSkeleton clip binds. This is exactly `scripts/apply_hero_retarget.py` today: `sidekick_bone_map.tres` (UE-mannequin lowercase source: King, Wizard) + `goblin_bone_map.tres` (PascalCase source: goblins), both → GeneralSkeleton.

### (b) Tradeoffs
- **Fidelity:** HIGHEST proven. The King binds all load-bearing locomotion bones (Hips/Spine/Chest/UpperChest/Neck/Head + both arm & leg chains); goblins bind 39/124 with every load-bearing bone driven. Misses are IK/twist/proc/attach helpers with no visible deformation impact. Empirically eye-verified upright walk + idle, sockets (crown/cape/sword/pauldrons) ride the cycle without detach.
- **Per-model setup cost:** HIGHER *per rig family, once.* Authoring a new `.tres` is a bounded one-time task per novel raw-bone convention — NOT per model. All King-family (`SK_Chr_*` Unreal_Characters) heroes reuse `sidekick_bone_map.tres`; all goblin-pack characters reuse `goblin_bone_map.tres`. Today's variant landscape is ~2–3 conventions (UE-mannequin lowercase, PascalCase, and the base-locomotion clips already on GeneralSkeleton).
- **Robustness across Synty variants:** HIGHEST. The `fix_silhouette` rest-fix is the one lever that resolved the Z-up-vs-Y-up bind-orientation mismatch that a plain name-match could NOT fix (the 2026-06-20 reclined-80° failure). A hand-authored map + rest_fixer is the only path that has *actually stood the hero upright* in this repo. New Synty packs with a new convention need one new `.tres`, then bind cleanly.
- **Runtime cost:** ZERO marginal. Retarget is an *import-time* bake; at runtime it is a plain skinned `GeneralSkeleton` — identical cost to any other. No per-frame correction node.
- **Maintenance:** the `.tres` files + `apply_hero_retarget.py` FILES list are the maintenance surface. Because the Synty `Assets/` tree is gitignored (license + size), the `.import` retarget blocks are NOT version-controlled — `apply_hero_retarget.py` re-injects them idempotently on any fresh checkout. That script IS the durable, committed artifact. Adding a rig = one FILES entry + (if new convention) one `.tres`.

---

## Option B — Auto-mapped GeneralSkeleton (no authored BoneMaps)

### (a) What it is / how it works in Godot 4.x
Set the FBX importer to `import/skeleton_profile = SkeletonProfileHumanoid` and let Godot auto-populate the BoneMap by name/heuristic at import, without a hand-authored `.tres`. Idea: one profile, importer guesses the source→profile correspondence, no per-variant authoring.

### (b) Tradeoffs
- **Fidelity:** UNPROVEN-to-LOWER here. Auto-mapping keys off bone-name heuristics. Synty's three conventions (UE-mannequin `pelvis/upperarm_l`, PascalCase `Hips/Clavicle_L`, already-retargeted humanoid) do NOT reliably auto-resolve — King-vs-Wizard *raw* overlap is only 21.6%, and the goblin PascalCase rig hit **0/123** raw-name match against the Sidekick clip before a map was authored. Auto-detection tends to leave gaps or mis-slot exactly where a bespoke map is needed most.
- **Per-model setup cost:** LOWEST *if it works* — no `.tres` authoring. But every mis-mapped bone becomes a per-model manual fix-up, which erases the saving.
- **Robustness across Synty variants:** LOWEST for THIS pack set. Critically, auto-mapping addresses only the *name* correspondence — it does NOT by itself resolve the **rest-orientation mismatch** (Z-up pelvis rest vs Y-up-authored clip rotation) that caused the reclined-walk failure. `fix_silhouette`/rest_fixer still has to run; without a real BoneMap driving it, the rest-fix has nothing coherent to normalize against. Auto-mapping is fragile precisely at the failure mode we already hit.
- **Runtime cost:** ZERO marginal (same as A — import-time bake).
- **Maintenance:** superficially lower (no `.tres`), but shifts cost to per-model manual correction and re-verification on every Synty pack update, with no committed artifact capturing the fix. Non-reproducible on fresh checkout (the gitignored `.import` gaps are silent).

---

## (c) Which best serves the D6 three-beat floor demo under Camera B

The D6 floor demo shows the hero + summoned proxies + goblin-class enemies animating (upright walk/idle + verb realization) across three beats (structure_1 / biome_crossing / structure_2), captured under the fixed Camera B (FOV 40 / pitch −55° / yaw 47° / dist 34m, 34m out, top-down-ish ARPG read).

- Camera B is a **room-scale ~49m-legible-band overhead** shot — it flatters silhouette-and-gait legibility over facial fidelity, but a **reclined-onto-its-back hero** (the exact Option-B-style failure mode) is glaringly wrong from this pitch: at −55° looking down, a figure tipped 80° reads as lying on the floor. Upright-walk correctness is the single most load-bearing animation requirement for this camera, and it is exactly what a plain/auto map fails and what the authored BoneMap + `fix_silhouette` rest-fix is the *only* proven fix for.
- D6 also renders **multiple rig families concurrently** (hero + goblins + summon proxies). Option A already has both required maps (`sidekick_bone_map` + `goblin_bone_map`) proven to bind and hold sockets under render. Option B would require re-de-risking all three families before a single capture, re-opening the 2026-06-20 block.
- The whole point of the D6 camera-ratification beat was "camera ratified late is expensive, caught early." The parallel truth: **rig-retarget correctness is the gate on every render/capture layer** (D5 verb VFX, D5 summon meshes, D6 floor capture, D8 grimoire portraits). Choosing the already-proven path unblocks all of them same-session; choosing the unproven path re-runs the spike.

---

## (d) RECOMMENDATION

**Ratify Option A — Authored per-variant BoneMaps → GeneralSkeleton.** (i.e., keep and formalize the `apply_hero_retarget.py` + per-family `.tres` pipeline as the v2 demo's canonical retargeting path.)

**Reasoning:**
1. **It is the only path that has actually worked in this repo.** The reclined-walk failure (2026-06-20) proved a name-match alone — which is all auto-mapping gives — is *necessary but not sufficient*. The authored BoneMap + `rest_fixer/fix_silhouette` is the empirically-verified fix that stands the hero upright. Choosing B re-opens a block we already closed.
2. **Setup cost is per-convention, not per-model, and already paid.** Both required maps (UE-mannequin + PascalCase) exist and are proven. Marginal cost for a new pack is one `.tres` + one FILES entry — bounded and reproducible.
3. **Zero runtime penalty, fully reproducible** via the committed `apply_hero_retarget.py` despite the gitignored Synty tree — the durable artifact already exists.
4. **It directly unblocks the D6/D5/D8 render+capture layers** under Camera B this session, where upright-gait correctness at −55° pitch is non-negotiable.

**Nuance, not a competing option:** where a *future* Synty pack already ships on a clean humanoid rig that Godot auto-maps correctly (verified by eye-check, not assumed), we can skip authoring a bespoke `.tres` for that pack and let auto-detection populate the GeneralSkeleton map — Option A's mechanism gracefully degrades to "no map needed" when the source is already clean. So A is the superset: author a map where the rig needs one, lean on auto-detect where it doesn't. That is strictly safer than committing to B wholesale.

**On ruling A:** drax immediately (a) formalizes `apply_hero_retarget.py` as the v2 retarget contract, (b) proceeds to the rig-gated D6 three-beat floor authoring + capture, D5 verb VFX/summon-mesh render, and D8 grimoire portrait render under the fixed Camera B — all currently blocked solely on this pick. jack-ryan files the decisions-log entry.
