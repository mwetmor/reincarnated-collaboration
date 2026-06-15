# drax BRIEF — bake the parametric room to EDITABLE scenes + close open_arena's VFX gate + flag the summoning-circle placeholder

**Type:** direct gandalf → drax design brief. **Hand-delivered to drax's session — NOT a KR dispatch.** (Matt directive 2026-06-15: *"yes please author the full Drax brief. I'll personally re-fire Galadriel once the scene is updated."*)
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B). Three load-bearing Matt statements this brief executes:
1. *"When I open Godot, I have to hit play scene, and then I only see a movie play … I thought that we would be moving to actual baked assets which I can see in the scene and interact with/edit."* → **Change 1 (priority).**
2. Galadriel failed one room (`open_arena`) and flagged reservations on two others. → **Change 2.**
3. *"The summoning circle is a placeholder for VFX and we will need to remove it later on as it is not sensible within many rooms."* → **Change 3.**
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-parametric-arenaroom-refactor.md` — the parametric refactor you already shipped (`scripts/render_arena_room.gd`, committed). This brief extends that work; it does **not** overturn it.
- `reincarnated-godot/scripts/render_arena_room.gd` — the script all three changes touch (line cites below are from the committed version).
- The A-holds ruling + extension (`canonical/story/...a-holds...`) — register-2 is carried by lighting + VFX; that bet is what Change 2 + 3 must protect.

---

## 0. One line

Your parametric room is correct and parity-clean — but it only exists at **runtime** (`_ready()` builds it, `_process()` captures it → the "movie" Matt saw). Add a **bake path** so the same spec-driven builder also writes persistent, **editable** `.tscn` scenes Matt can open/select/edit (the playability on-ramp), **fix open_arena's camera** so its bloom clears the VFX gate (closing Galadriel 6/6), and **decouple the register-bearing VFX from the literal summoning-circle skin** Matt flagged as a placeholder. One builder, two outputs (capture + bake); the spec stays the single authority for both.

## 1. The three changes (priority order)

| # | Change | Why | Gates |
|---|---|---|---|
| **1** | **Bake-to-`.tscn`** — same builder, second output: persistent editable scenes | Matt's actual flag: he wants editable/interactable assets in the editor, not a play-mode movie | the playability on-ramp |
| **2** | **open_arena camera + bloom fix** | open_arena FAILS the VFX gate (composite 3.50, VFX 3, HLF peak only 1.26× thr) | closes Galadriel **6/6** → the multi-footprint A-holds canon extension |
| **3** | **Summoning-circle placeholder** — make removable/conditional + flag for replacement | Matt: the ritual circle "is not sensible within many rooms" | genre coherence; unblocks the durable VFX answer |

All three are **additive to** `render_arena_room.gd`. None touch `arena.py` (engine authority), the spec JSON shape, or the spawn-position parity contract.

---

## 2. Change 1 — bake the parametric room to EDITABLE scenes (the on-ramp Matt flagged)

### 2.1 What's actually true today (code-cited — this is the gap, not a defect)

`render_arena_room.gd` is `extends Node3D` (not `@tool`). It builds the entire room **at runtime**: `_ready()` (`:107`) calls `_build_floor … _build_atmosphere_vfx … _frame_camera` (`:112-121`), each instantiating prefabs and `add_child`-ing them live; `_process()` (`:549`) saves 100 frames to `user://`. So:

- **Nothing persists in the editor.** `scenes/arena_room.tscn` contains only the rig (Node3D root + WorldEnvironment + Camera3D + 3 lights). All geometry, combatants, and VFX exist only while the scene is *running*. Open it in the editor → empty rig. Hit Play → it assembles + captures → "a movie." **That is exactly what Matt described, and it is working as written — it's a capture harness, not an authoring surface.**
- The built nodes are `add_child`-ed with **no `.owner` set** (every `_build_*` does `add_child(x)` and stops). This is the single fact that makes baking a small change.

### 2.2 The change — a bake path that reuses the builder verbatim

Add a mode that runs the **same** `_build_*` assembly, then serializes the assembled tree to a real scene file:

1. **Extract the build sequence.** Pull `_build_floor()…_frame_camera()` (the body of `:111-121`) into a `_build_all()` you can call from either `_ready()` (capture mode, unchanged) **or** the bake path. Zero behavior change to capture mode.
2. **Set `.owner` on every built descendant** — *this is the classic `PackedScene.pack()` gotcha and the whole reason baking looks like nothing happens if you skip it.* Nodes whose `owner` is unset are **silently dropped** from the packed scene. After `_build_all()`, walk the tree and set `owner = scene_root` on all descendants (NOT the root itself):
   ```gdscript
   func _set_owner_recursive(node: Node, root: Node) -> void:
       for child in node.get_children():
           if child != root:
               child.owner = root
           _set_owner_recursive(child, root)
   ```
   The rig nodes from `arena_room.tscn` already carry owner (that's how they were saved); only the runtime-built subtree (Floor, Walls, ChokeZones, combatants, the FX `GPUParticles3D` subtrees) needs it. The recursion must reach **inside** the FX instances or their particle children get dropped.
3. **Pack + save per scenario:**
   ```gdscript
   var packed := PackedScene.new()
   packed.pack(self)                       # self == ArenaRoomRender root (rig + built tree)
   ResourceSaver.save(packed, "res://scenes/arena_%s.tscn" % _scenario_id)
   ```
4. **Trigger — your call, but I recommend the headless-CLI flag** (consistent with the existing `--scenario` arg pattern at `:133-138`, and it loops all six cleanly):
   ```
   godot --headless scenes/arena_room.tscn -- --scenario open_arena --bake
   ```
   → writes `scenes/arena_open_arena.tscn`, then quits. A 6-line shell loop bakes all six. (Alternatives if you prefer in-editor: a `@tool` + exported `bake_now: bool` setter, or a `@tool extends EditorScript` run via *File > Run*. Pick what's cleanest in your seam — the load-bearing content is steps 2–3, not the trigger.)

### 2.3 The gotcha that will bite if unflagged — don't let the baked scene rebuild itself

The packed root carries the script. If you bake with `@tool` + auto-build-in-`_ready` live, **re-opening the baked scene will re-run `_build_all()` on top of the already-baked geometry → duplication.** Guard against it: strip/replace the script at bake time, OR guard the build (`if has_node("Floor"): return`), OR give baked scenes a stripped "viewer" script with no builder. Your call — just make the baked scene **inert geometry**, not a re-builder.

### 2.4 Parity discipline survives the bake — and this is the important part

The baked `.tscn` is a **generated artifact**, exactly like `data/arena_scenarios.json`: it descends from `arena.py → arena_scenarios.json → builder → baked scene`. The parity-critical layer (footprint walls, spawn positions) is **regenerated from the spec**; a spawn move in `arena.py` re-bakes to a new scene, never a hand-patch. So:

- **What you regenerate from spec:** the parity-critical geometry (shell, choke geometry, combatant spawn positions). Never hand-edit these on the baked scene — re-bake.
- **What you hand-author *on top of* the baked scene (Layer 2, deferred per Matt):** dressing, the eventual player-controller, decorative props, lighting polish. The bake gives you a stable, parity-true **starting surface** to build forward from — which is precisely the editable/interactable scene Matt asked for. To keep hand-authored Layer-2 work from being clobbered by a re-bake, isolate it (a separate child node the re-bake leaves alone, or a dressing scene instanced into the baked one). That's a Layer-2 mechanism — note it, don't build it yet.

**Keep the capture harness intact.** Galadriel still scores off the runtime capture path (Matt re-fires her). Bake is a *second* consumer of the same builder, not a replacement. One builder → {capture for galadriel, bake for Matt}. That duality is the clean architecture; preserve it.

---

## 3. Change 2 — fix open_arena's camera + bloom so it clears the VFX gate (closes 6/6)

### 3.1 The diagnosis (code-cited — it's camera distance, and it's proven camera-isolated)

`open_arena` is 50×50, aspect 1.0 → it takes the **near-square** camera branch (`:537-543`). That branch scales camera distance with `max(W,H)`: for 50×50 it puts the camera at **z≈70, height≈31, fov 42, look_at z≈26** — i.e., it pulls *all the way back to frame the entire 50 m footprint*. Two coupled consequences sink the VFX axis:

1. **The whole room is framed → everything subtends few pixels, the bloom included.** HLF (highlight-fraction — the bright-VFX pixel share the rubric's VFX axis reads) collapses to **1.26× threshold** (vs the cathedral's 6.2×, and vs chokepoint passing). Composite **3.50**, VFX **3** < the mandatory **4** → FAIL.
2. **The all-swarm bloom sits in *empty space*.** `_resolve_marquee()` (`:170-184`) gives all-swarm rooms a **room-center** bloom → `_arena_center` = (25, 0, 25). But open_arena's swarm clusters at y∈[8,18] (`:53` table) and the player is at (25,40). So (25,25) is **between** the fight and the player, in empty floor — the brightest VFX event is placed where nothing is happening, *and* far from camera.

**This is camera-isolated, and chokepoint proves it.** chokepoint_corridor is *also* all-swarm with a *room-center* bloom — and it **passes**, because the corridor branch (`:523-530`) frames the tight **engagement band** (player + choke + mobs), so its bloom subtends real pixels. Identical bloom rule, different camera → pass vs fail. The bloom recipe is fine; the **large-near-square camera is the bug.**

### 3.2 The fix (proven-direction — frame the fight, don't fit the footprint)

The near-square branch's "fit the whole footprint" rule is correct for 28–30 m rooms and wrong for a 50 m one. Two moves, either or both (pick the minimal combination that clears VFX ≥ 4):

- **(a) Frame the engagement band for LARGE near-square rooms.** Add a guard: when `max(W,H)` exceeds ~35 m, stop fitting the whole footprint — frame the player↔fight band the way the corridor branch already does for its long axis. Concretely, pull the look-at toward the swarm cluster and bring the camera in so the band (player + mobs + bloom) fills the frame. This is the *same philosophy* the corridor branch uses; you're extending an existing, proven rule to "large near-square," not inventing one.
- **(b) Anchor the all-swarm bloom at the swarm-cluster centroid, not geometric center.** In `_resolve_marquee()` (`:170-184`), for the no-marquee case return the **mean of the swarm spawn positions** instead of `_arena_center`. For open_arena that lands the bloom at ~(25,12) — *where the fight is* — instead of (25,25) empty floor. This raises HLF (bloom now sits in the framed engagement band) **and** is more genre-sensible (the VFX tracks the action), which dovetails with Change 3.

I lean **(b) as the primary fix** (it's one line of intent, helps every all-swarm room, and is the genre-correct "VFX at the fight" move), with **(a)** if (b) alone doesn't clear the gate. Don't over-tune: the bar is VFX ≥ 4 with margin, not maximizing the score.

### 3.3 The "two others" Galadriel had reservations on

Re-score will tell, but if the two flagged rooms are the other large/odd footprints, the **same** large-near-square framing + engagement-centroid bloom should lift them. Apply the fix as a *rule keyed off footprint*, not a per-room patch — that's the whole parametric thesis. If a room still reads thin after the rule fix, **that's a finding, not a failure** — capture it and we look at it; don't hand-hack a single scene to force a pass.

---

## 4. Change 3 — the summoning circle is a placeholder; decouple it from the durable VFX

### 4.1 Matt is right, and this is a genre point worth stating plainly

The `HeroSummonSigil` — the `SM_Prop_Ritual_Circle_01` ritual-circle decal with red emission, built at `:447-461` — is the literal "summoning circle." Matt: *"not sensible within many rooms."* He's correct. A ritual/summoning circle is **scene-appropriate set-dressing for a ritual space** (it earned its place in the cathedral). Stamping one on the floor *under a skeleton in an open field* is a graybox-era expedient, not a design. In Diablo III/IV and PoE, the bright VFX in a combat frame is **a skill firing** — a Blizzard, a Meteor impact, a channel charging — not a decorative floor sigil. The eye tracks the *ability*, and the ability is sensible in every room because abilities happen wherever the fight is.

### 4.2 The decouple — separate the DURABLE need from the PLACEHOLDER skin

There are two things tangled in `_build_hero_vfx()` (`:436-488`), and they must be split:

- **DURABLE (keep — this is the A-holds bet):** the **VFX *presence*** — the `SummonFireColumn` GPUParticles (`:472-480`), the `SummonGlow` OmniLight (`:463-470`), and the charge→erupt→burn→collapse lifecycle (`_process`, `:552-568`). This is ~30% of the premium read and *is what HLF measures*. It stays. Do not weaken it.
- **PLACEHOLDER (make conditional + flag):** the **ritual-circle floor decal** itself (`HeroSummonSigil`, `:447-461`). Gate it behind a flag (e.g., `const USE_RITUAL_CIRCLE_PLACEHOLDER := true`) with a clear comment: *"PLACEHOLDER — stands in for body-anchored skill-cast VFX until skill VFX exist; a ritual circle is only sensible in ritual rooms (cathedral), NOT open fields/corridors. Remove/replace per gandalf brief 2026-06-15."* When the flag is off, the fire column + light + lifecycle still fire — the room keeps its register-bearing VFX **without** the nonsensical floor sigil.

### 4.3 The interaction with Change 2 — and why removing the skin doesn't hurt the gate

This matters: **dropping the ritual-circle decal does NOT cost you the VFX gate.** HLF reads the *bright* VFX pixels — the fire column + glow light. The ritual circle is a low-luminance dark-red emissive decal (`albedo (0.14,0.015,0.015)`, `emission_energy SIGIL_EMBER=0.9`, `:454-458`); it contributes almost nothing to HLF. So: Change 2 (camera + centroid bloom) is what lifts open_arena's VFX score; Change 3 (drop the placeholder skin) is genre-cleanup that's HLF-neutral. They compose cleanly — you can do both without trading one against the other.

### 4.4 What the placeholder is a placeholder *for* (so you know the durable target)

Flag it, don't build it: the durable replacement is **body-anchored skill-cast VFX** — the marquee enemy's signature ability charging/firing (or the player's), which is sensible in every room *and* genre-correct. The fire-column-from-a-sigil is the stand-in for "a bright body-anchored VFX event" until skill VFX exist. That's a separate, later track (it rides on the same GPUParticles lever you've already proven). Naming it here so the placeholder's removal has somewhere to land.

---

## 5. Scope honesty — what this delivers and what it explicitly does NOT

**Delivers:** (1) persistent **editable** arena scenes Matt can open/select/edit — the playability on-ramp; (2) open_arena clearing the VFX gate → Galadriel **6/6** → the multi-footprint A-holds canon extension becomes available (on the re-score, per § 7); (3) a genre-coherent VFX that no longer stamps a ritual circle on a battlefield.

**Does NOT deliver (unchanged, separately gated — keep these explicit in your capture notes so we don't over-claim):**
- **The live combat loop.** Baked scenes are an editable *stage*; figures still stand where the sim spawns them. Input-driven multi-form combat is the separately-gated milestone it always was — the bake just makes the stage approachable to build it on.
- **The real combatant.** Figures stay placeholder Synty kitbashes. The generative-self / character-creator combatant is a separate track.
- **Layer-2 dressing.** Matt is fine waiting (his words). The bake gives the surface; dressing comes later.
- **The skill-cast VFX** that eventually replaces the summon placeholder (§ 4.4).

---

## 6. Roles / acceptance

- **drax:** implement all three changes on `render_arena_room.gd`; bake all six to `scenes/arena_<scenario>.tscn`; re-run the **capture** path for the updated scenes so Matt has fresh frames to score. **Do NOT self-score.**
- **Matt:** opens the baked scenes to confirm they're editable/interactable (Change 1 acceptance); **personally re-fires Galadriel** on the updated capture (his stated plan).
- **galadriel:** lifecycle-scores the re-captured corpus against the register-2 rubric — the gating question is whether **open_arena now clears VFX ≥ 4** (and the two flagged rooms hold).
- **gandalf:** on the re-score, interpret it for the canon call — **if 6/6 at register-2, the multi-footprint A-holds extension fires** (I author the ruling then, not before).

**Acceptance bar:**
1. The six `scenes/arena_*.tscn` open in the editor as **selectable, editable geometry** (not an empty rig, not a play-mode movie).
2. The baked scenes reproduce spawn-position parity with the spec (re-bake = spec-faithful; no hand-edits to parity geometry).
3. Capture mode still works (Galadriel's path intact).
4. open_arena's bloom sits in the engagement band; the summon ritual-circle is behind a flag and off by default in non-ritual rooms (fire column + glow retained).

## 7. Sequence + the recognition→validate→commit line

1. drax: Change 1 (bake) — the priority on-ramp; verify a baked scene opens editable.
2. drax: Change 2 (open_arena camera/bloom) + Change 3 (placeholder flag) — re-capture all six.
3. Matt: confirm editability + re-fire Galadriel.
4. galadriel: re-score → 6/6 question.
5. gandalf: **on the 6/6 re-score**, author the multi-footprint A-holds canon extension.

**The canon does not fire on this brief.** Recognition → validate → **commit**: the recognition is "the parametric room carries register-2 across footprints"; the validation is Galadriel's measured 6/6 re-score on the **fixed** open_arena; the commit is the canon extension. The empirical gate is the re-score, not the authoring of this brief — exactly the discipline that held for the cathedral (canon fired on the 5.00, not the asset drop). Build to the rubric + the proven lift recipe, not to pixel-matching any marketing frame (standing A-holds discipline).

---

**Signed:** gandalf, 2026-06-15
**For:** the three-change drax brief — (1) add a **bake path** so the same spec-driven builder writes persistent, editable `scenes/arena_<scenario>.tscn` (extract `_build_all()`, set `.owner` recursively on every built descendant — the `PackedScene.pack()` gotcha — pack + `ResourceSaver.save()`, recommend a headless `--bake` flag, and don't let the baked scene re-run its own builder), giving Matt the editable/interactable assets he flagged instead of the play-mode movie, while keeping the capture harness intact and the spec as the single parity authority; (2) **fix open_arena's VFX-gate failure** (composite 3.50, VFX 3, HLF 1.26× thr) — a camera-isolated bug where the large near-square footprint pulls the camera back to fit all 50 m so the room-center bloom subtends too few pixels, proven camera-isolated since chokepoint passes on the identical bloom rule — by framing the engagement band for large near-square rooms and anchoring the all-swarm bloom at the swarm-cluster centroid instead of empty geometric center, closing Galadriel 6/6; (3) **decouple the durable register-bearing VFX** (fire column + glow + lifecycle — the A-holds bet, kept) **from the literal summoning-circle skin** Matt correctly flagged as not-sensible-in-many-rooms — gate the ritual-circle decal behind a placeholder flag (HLF-neutral, so it doesn't cost the gate) and name its durable replacement (body-anchored skill-cast VFX). Scope stays honest (editable stage + on-ramp delivered; live combat, real combatant, Layer-2 dressing, skill-cast VFX all still separately gated), and the multi-footprint A-holds canon extension fires on Galadriel's 6/6 re-score, not on this brief.
