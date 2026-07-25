# TCP-L5-D — mode (ii) SEAM ARRIVAL, Phase A report

**Cell:** L5-D · **Agent:** drax (presentation seam) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l5d-seam-arrival.md`
**Status:** **PHASE A COMPLETE — STOPPED AT THE OWNER-EYE GATE.** Nothing was built, no wall was
cut, no scene was saved. Awaiting Matt's eye before Phase B.

**Deliverables:** `~/Games/mcp-lab/evidence/l5/l5d/`
`SITING_PLAN.md` · `FIRST_INTENT_BANKED.md` · `PROBE_siting_candidates[_ANNOTATED].png` ·
`PROBE_chosen_siting[_ANNOTATED].png` · `MEASURED_DOOR_MODULES.txt` ·
`CONCURRENT_REPO_BASELINE.txt` · `rigs/`

---

## 1 — The number the cell exists to produce

**Authoring clock: 27.8 minutes (0.46 h), 2026-07-25T20:04:33Z → 20:32:19Z, thinking included.**

**Method: H throughout. No wire was engaged, so none of the clock is swap or transport.**

| activity | approx |
|---|---|
| read substrate, derive all room geometry from the `.tscn` text | ~9 min |
| write + validate the aperture rasteriser; measure 21 kit modules | ~6 min |
| author siting probe, render (twice — see §5), measure the frames | ~7 min |
| removal-set volume query + frame-budget solve | ~3 min |
| author the plan | ~3 min |

Two re-dos are inside that figure and both are declared: a probe double-grab, and a wrong claim
about collision proxies that I corrected against a measurement rather than shipping.

---

## 2 — The answer, in one paragraph

Put the portal in the **north wall (run 0), bay `0_3`** — the room's centre bay on its own axis.
Do not cut anything: drop in `SM_Bld_Base_Wall_Door_Double_01`, a same-family module that already
contains the hole, centred in the 0.45 m wall band. **Clear aperture x [−1.0021, +1.0021] ×
y [0, 1.9663] — 2.0042 wide, 1.9663 tall, sill 8 mm below the floor surface, so no step.** Behind
it, a chamber **5.00 × 3.75**, floored with the crypt's own tile on the crypt's own 1.25 grid at
the crypt's own height, walled with the crypt's own module to the crypt's own height, capped to
one unbroken wall-top plane, and open to the sky exactly as the crypt is. **Removal set: exactly
two nodes.**

---

## 3 — Findings worth carrying out of the cell

### 3.1 The removal set is a volume query, not a name match — and the naming scheme is a trap

The bay is a **three-node group whose members do not share a fate**: `Wall_0_3_inner` and
`Wall_0_3_outer` go, `WallCap_0_3` stays. I targeted by building world AABBs for all 288 geometry
nodes and intersecting with the portal prism; it returns exactly the two skins, and the cap lands
in the *near-miss* list at y [3.0097, 3.1697] — above the prism, sharing the bay index.

Every natural way of expressing the removal takes the cap: `Wall*_0_3*`, "delete bay 0_3", a wire
`node-find` on the bay name. And the cap is not incidental — **an unbroken wall-top plane is the
strongest "one place" cue in the whole design**, and deleting the cap punches a 2.5 m notch through
it. The most natural expression of the subtraction destroys the thing the subtraction is for.

This is the cell's substantive answer to "how you target removals is a finding," and it is worth
generalising: *in a kit-built scene, the addressable unit of authoring (the bay) is not the
addressable unit of subtraction.*

### 3.2 Subtraction exposes an unfloored band that nothing in the scene would catch

The crypt floor stops at |8.75| and the wall band runs |8.75|→|9.2|. There has never been floor
under the band — it has always been under a wall. **Opening the wall opens a 0.45 m hole in the
walking surface.** Invisible in a still frame, fatal in a walk.

And there is **no collision anywhere in the substrate** — 288 `MeshInstance3D`, zero `StaticBody3D`,
zero `CollisionShape3D`. So nothing would have caught it except the geometry query. This also means
Phase B's "orphaned-collision verification" has an **empty answer by construction** (it should be
reported as satisfied *with the reason*, not silently passed), and Phase B's G4 capsule sweep has
nothing to sweep against until collision is generated at build time.

### 3.3 The kit's collision proxy is smaller than the kit's visible hole

| | visual `Wall_Door_Double_01` | proxy `..._Double_01_Collision` |
|---|---|---|
| aperture w | 2.0042 | **1.9553** (−4.9 cm) |
| aperture h | 1.9663 | **1.9336** (−3.3 cm) |

The hole you can walk through is smaller than the hole you can see. Harmless at this size; it is
the class of mismatch a sweep exists for, and walkability must be measured against the proxy, not
the render. Note also the Base family ships only six proxies and **none for the plain wall**.

### 3.4 The door variants carry THREE surfaces — an extension to the ancestry doc

`L4_KIT_CONSTANTS.md` §3 warns in bold that wall and floor carry **2** surfaces and that a
single-slot assignment leaves a surface rendering as the pack's translucent near-white blob. Every
door variant carries **3** (212 verts / 108 tris / 3 surfaces, vs the plain wall's 40 / 20 / 2).
Copying the substrate's own two-override pattern onto the door leaves the architrave untextured,
at eye level, in the centre of the money frame. This is new information, not a restatement.

### 3.5 The substrate's materials encode camera visibility — read them before choosing a wall

The 26 `ShaderMaterial`s are a visibility scheme. Runs 1 (south) and 2 (east) are the camera-near
walls and are deliberately faded (`walltop_void_radial`; `walltop_occlude` with `ghost_floor 0.0`);
the two `+Z` corner pillars carry `south_blackout = true`. Runs 0 and 3 render solid. **That rules
out half the candidate walls before any rendering happens.**

It also yields the plan's most economical move: **every chamber wall has a crypt wall with an
identical normal**, so each inherits an existing, already-tuned material with no new shader
authored — including the chamber's camera-near wall, which inherits run 2's fade treatment because
it has the identical `+X` normal and the identical problem (left solid it occludes 39% of the
chamber). Not imitation; the substrate's own answer applied to the same geometry.

Sub-finding: runs 0 and 3 give each bay its own `ShaderMaterial` instance and **all fourteen are
parameter-identical**. The per-bay split carries no information, so the removal "orphans" a
material that was never distinct — and it is the right material for the chamber's far wall anyway,
so it is relocated rather than orphaned.

### 3.6 Three independent constraints picked the chamber depth

3.75 m is simultaneously (a) the deepest grid-aligned depth that stays inside the standing `__box`
frame, (b) the depth that tiles exactly as `Wall_01` + `Wall_Half_02`, and (c) the depth at which
the chamber's far wall rises above the crypt's cap while its near floor is still visible through
the doorway — **79.5% of the chamber depth visible from the standing camera**, in two bands with a
0.77 m blind strip between them that the continuous floor grid bridges. Constraints agreeing is a
good sign the number is found rather than chosen.

The half-width panel is what makes this possible, and finding it required measuring: the kit's
`Wall_Half_01` is half-**height** (2.5 × 1.5057) and `Wall_Half_02` is half-**width** (1.2500 ×
3.0057). The names do not tell you which; without `Half_02` the only tiling depths are 2.5 (too
shallow to be a room) and 5.0 (out of frame).

### 3.7 The wire *can* subtract — I checked before ruling it out

The installed W-MUR surface (gamedev-mcp-server 9.2.0.0 + godot_mcp 0.19.1, 39 tools / 11 families)
includes `node-delete` alongside `node-create`, `node-modify`, `scene-open`, `scene-save`. **The
lap's novel primitive is not a capability gap for the installed wire.** I ruled H anyway, on
measured grounds: in-editor call latency is mean 8.32 ms, so forty calls is 0.33 s of wire — the
cost of W-MUR here is *composing* forty individually-parameterised calls, not transport. Ruling
R-7 is logged veto-open, and I flagged explicitly that if the program wants a mode-(ii) datum on
how a wire handles subtraction, that must be said **before** Phase B fires — afterwards the
comparison is contaminated.

---

## 4 — Rulings (all veto-open, all with reasoning; full text in `SITING_PLAN.md`)

| # | ruling | primary reason |
|---|---|---|
| R-1 | portal in the **north wall, bay `0_3`** | north clips 30 px vs west's 91 px in the judgment frame; closed-form solve agrees (out by 0.160 vs 0.522). West's 4.1° better face-on angle does not buy back 0.71 m of frame budget. |
| R-2 | **one** door module **centred** in the 0.45 band | two would overlap 0.063 with coplanar jamb faces → z-fighting on the most-looked-at surface. Centred gives a symmetric 0.081 reveal on the pillars' own mid-plane. |
| R-3 | **`Door_Double_01`**, not Single or Large | measured visible chamber floor through the aperture at −50° pitch: 2.26 / 1.58 / 1.13 m². Height buys nothing looking down; width is what lets you see in. |
| R-4 | every chamber wall **inherits an existing substrate material** by matching normal | no new shader authored; the camera-near wall gets run 2's fade, which is the substrate's own solution to the identical problem. |
| R-5 | chamber gets **its own** `OmniLight3D`; substrate's is untouched | chamber centre is 11.03 m from a range-9.0 pool → receives none of it. Widening the substrate's pool would change the crypt and pollute the diff. |
| R-6 | door module takes **three** per-surface overrides | measured 3 surfaces; the 2-override pattern leaves the architrave an untextured blob. |
| R-7 | **H** for Phase A (done) and Phase B | clock is dominated by authoring, not transport; the build is parametric; the 3-surface hazard is a wire hazard specifically. |

---

## 5 — Instrument note: my own probe reproduced the bug TCP-23 documents

The probe's first run silently grabbed **twice** and saved the drifted second frame:
`await RenderingServer.frame_post_draw` inside `_process` yields, and `_process` re-enters before
`get_tree().quit()` takes effect. `l4_shoot.gd` is immune only because its queue index advances
before the await returns — its refusal check does not cover this path. I added an explicit `_done`
latch and re-shot.

**The lesson is the L3 `editor_up.sh` lesson again: one-scene-per-process needs a latch, not
discipline.** A new rig written by someone who has *read the rule and cited it in their own header*
still reproduced the bug. I did not modify `l4_shoot.gd` (forbidden) — its hash is unchanged — but
this is worth a line in the calibration doc, since the next person to write a rig will hit it too.

The annotation overlay carries a **projection self-check**: the crypt's known floor rectangle is
drawn from its measured coordinates and lands exactly on the rendered floor edges, so the projected
portal/removal/visibility annotations on the frame are trustworthy rather than asserted.

---

## 6 — Steer-check: the control the conductor asked me to run on him

Gandalf's signature block asked me to say if reading something he listed felt like being handed an
answer. Banked before work, verdict now.

**Yes, one sentence: §2's "the dais is not in your scene."** It is a negative fact I could not have
derived and it primed me to expect a dais-like prop. It did not change what I did — I found no
dais, and the plan has no dressing because the brief asks for a chamber — but I looked, and had
`l4prep_measure.gd` been on my path I would have opened it.

**The sharper version of his worry is one he did not name.** `L4_KIT_CONSTANTS.md` is genuinely
disciplined about the thing it guards: §2 hands module natives (which I re-measured and confirmed
rather than trusted) and explicitly withholds all scene placements, which is what made deriving
the room real work. But **§6 of that same file pins two braziers as an L4 spec clause.** A cell
reading its ancestry for natives is handed L4's *dressing decision* in the same document. **The
natives file steers by adjacency, not by content.** Recommend §6 be split out before the file is
handed to another arrival cell.

Everything else behaved as ancestry should.

---

## 7 — Exit predicate

| # | requirement | status |
|---|---|---|
| 1 | FIRST_INTENT + clock start banked before any work | **MET** — banked at 20:04:33Z, before the substrate was opened |
| 2 | `SITING_PLAN.md` complete, all four items, measured numbers | **MET** |
| 3 | probe frame(s) banked under `evidence/l5/l5d/` | **MET** — 4 frames (2 raw, 2 annotated) |
| 4 | rulings logged veto-open; read-list declared | **MET** — R-1…R-7 with reasoning and veto conditions; read-list incl. explicit *not-read* list |
| 5 | substrate sha + 0444 verified intact | **MET** — `d45db0f5…8ede8522de1966`, `-r--r--r--` (100444), verified at start **and** end |
| 6 | project dir clean of scratch | **MET** — all four `l5d_*` files relocated to `evidence/l5/l5d/rigs/`; project dir inventory matches cell-start exactly |

**Concurrency (dispatch §3).** `mcp-lab/project/` was mine alone; the harness dispatch never
appeared on my floor. `reincarnated-godot/` was read-only for me and I recorded its state at both
ends. Three commits landed during my cell (`ce1c1af`, `188fd27`, `398609c` — pillar-quilt
dispatch). `kit_replica_level.gd` changed hash `0a722e0a…` → `42935a35…` but is **git-clean**, so
the change is a commit and attributable to that dispatch. The one uncommitted tracked file,
`project.godot`, is **byte-identical to the baseline I banked at cell start** — pre-existing, not
mine. **No HALT condition.** I did not open `kit_replica_level.gd`; I hashed it, which is why I can
say I did not perturb it.

**Rigs untouched:** `l4_shoot.gd`, `l4_shoot.tscn`, `l4_detail_shoot.gd` hashes recorded and
unchanged. The differ was never invoked. `project.godot` in the lab still carries the Murzak addon
line — the installed wire was left exactly as installed.

---

## 8 — What Phase B needs from the owner-eye

Matt's eye gates the wall-cut. The three things most worth his veto, in order:

1. **R-1, the wall** — everything downstream is sited on it, and it was decided by a frame budget.
   If the Phase-B judgment framing is not `__box`, the comparison that chose north dissolves.
2. **R-3, a 2 m double opening rather than a door** — this is the biggest aesthetic call in the
   plan. It reads as an *opening*, which serves "one place"; it is harder to hang a door leaf in
   later if the fiction wants one.
3. **R-7, method** — if the program wants a wire datum on subtraction, it must be said now. I have
   shown W-MUR can express it; after the build the comparison is contaminated.

Phase B is specified end-to-end in `SITING_PLAN.md` §3 and fires only on resume.
