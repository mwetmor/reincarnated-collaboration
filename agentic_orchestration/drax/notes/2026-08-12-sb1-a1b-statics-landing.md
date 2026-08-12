# SB-1 Cell A1b — GATE-2 DEBT + ARENA STATICS + ROSTER + CP-A STILL-SET (drax)

**Cell ID:** `SB1-CELL-A1b` · **Date:** 2026-08-12 · **Author:** drax (presentation seam)
**Charter:** `gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md` @ `9b3e7e2b` (+ retention rider)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — A1-3 / A1-4 route the Gate-2
findings here; R-A1-1 and R-A1-LAW bind; PL-5 binds item 3.
**Gate-2 under discharge:** `qa/pending/2026-08-12-jack-ryan-sb1-a1a-gate2.md` @ `555d1b17`
**Godot repo:** `28ea1ba` → `aec38e8`, **19 paths**, local only, **nothing pushed** (PL-7: the
conductor pushes on return).

**VERDICT: ALL FOUR ITEMS LANDED. 0 HALTS.**

---

## 1 · Per-item commit table (CL-2)

| hash | item | what |
|---|---|---|
| `093a19e` | **0** | Gate-2 debt discharge — all six DEBTs + three INFOs |
| `0dd9586` | **0** (cont) | JR-A1a-1: the A1a change-set is **12 paths, not 11**, corrected in `AGENT_STATE.md` with its reproduction command |
| `562b6f4` | **1** | the arena statics — floor, six emitters, the BOXes, the player station, five declared absences, the scene of record |
| `26ab5dd` | **2** | the roster — 344 static bodies at their own `path[0]`, six dresses, the veto-open body table in its own file |
| `f1acfa6` | **3** | the CP-A still-set harness + the three defects the frames caught in items 1–2 |
| `aec38e8` | — | `AGENT_STATE.md` checkpoint |

**Containment.** Godot porcelain **233 lines = the L-0 pin exactly**. Engine-tree porcelain
**2,789 lines = the FG-17 baseline**, unchanged before and after. The baton was never touched: its
digest recomputes to `d7ecd866ac45…` after every harness run in this cell. No PNG is committed.

---

## 2 · Item 0 — the Gate-2 discharge table

| finding | sev | discharge, with its evidence |
|---|---|---|
| **JR-A1a-1** — change-set is 12 paths, not 11 | DEBT | Corrected in `AGENT_STATE.md` (`0dd9586`) **with the command that reproduces it** and the reason it was wrong: five committed `tmp/kc2/` artifacts, not four. My A1a landing note is **not** edited — it is the record of what the cell claimed; this is the correction record. |
| **JR-A1a-2** — the GL-7 UNDEFINED row is a tautology on the godot column | DEBT | The row tested `kc2_loader_smoke.gd`'s own `range(lo, hi+1)` emitter loop, which is true for any loader using it **including one that clamps**. The smoke now emits **688 out-of-span probes** (two per actor, at `lo-1` and `hi+1`) carrying `actor_position()`'s actual return; the differential diffs those against the stub's `None`. **Proven able to go RED** (CL-10, trust-but-verify of my own fix): planting a clamped probe on `w151_a000` moved the run to **21/22 EXACT-MATCH, 1 DELTA** and the row named the actor. Restored, 22/22. |
| **JR-A1a-3** — "22 rows, stub → godot" overstates the independent count | DEBT | Every row now carries a `basis` and the headline carries the sub-counts, in the artifact and on stdout. Measured: **STUB-VS-GODOT 8 · WIRE-VS-GODOT 6 · DIFFSCRIPT-VS-GODOT 5 · STUB-VS-STUB 1 · GODOT-ASSERTION 1 · CONTAINMENT 1 = 22.** The eight are exactly the eight jack-ryan named. `DIFFSCRIPT-VS-GODOT` is **added** to his five rather than folded into `WIRE-VS-GODOT`, because folding "this script re-implements the same rule" into "I read the wire right" would repeat the framing error the finding caught. |
| **JR-A1a-4** — FL-3: 19 refusal paths, 4 falsified; **GL-9 unproven and A1b leans on it** | DEBT | Four mutants added, each asserting **its own** error string so a wrong-reason refusal reads FAIL: `SCATTER-SHAPE-UNDECLARED` (GL-9), `placement_extents_m absent` (GL-9), `TICK-PERIOD-DISAGREEMENT` (GL-10), `INTEGRITY-MISMATCH` (CL-10). Falsification **3 → 7 checks, 0 FAIL**, mutants pruned, directory verified empty. **The GL-10 mutant found a defect in itself — see NOTE-15.** |
| **JR-A1a-5** — four assertions carry a basis the predicate does not test | DEBT | `GL-12 absences` was `>= 6` against a measurement of 7 — a bar *below* the measurement — now **set identity on the seven named ids**. The two 61s were bare counts that pass on any 61 bodies — now **set identity against the p05 spawn-anchor roster**, symmetric difference 0 both ways. `GL-11 one global clock` read endpoints only — now **contiguity + monotonicity on all four tracks** (4 × 3,732) plus non-restarting wave spans, which is what NOTE-4's claim actually rests on. |
| **JR-A1a-6** — the census artifact omits the evidence for its own bin | DEBT | `crosschecked_against_actor_table: 344` now reaches `kc2_event_census.json`. Copied **generically** (every extra key the loader hangs on a census row reaches the artifact), so the next evidence field cannot be lost the same way. FG-16 satisfied. |
| **JR-A1a-7** — the 26-check headline ships no receipt | INFO | `tmp/kc2/kc2_loader_smoke.txt` **committed** (45 lines), with its exact regeneration command in the file header. The differential transcript lands beside it. |
| **JR-A1a-8** — the three 61s are one population | INFO | Folded as an **assertion**, not a remark: `2-knot set == drip set == p05 roster`, and the smoke prints the sentence. |
| **JR-A1a-9** — the FG-13 mutant's stated mechanism is not the operative one | INFO | Comment corrected in place. GATE 5 (FG-13) runs **before** GATE 7 (CL-10), so the census was already the first and only refusal without the `_integrity` bump. What the bump actually buys is that the mutant stays **self-consistent** — a baton with one extra row and an `_integrity` block that agrees, so the only thing wrong with it is the thing under test. |

**Harness state after item 0:** loader smoke **28 checks, 0 FAIL** (was 26) · placement **10/10**,
byte-identical regeneration · falsification **7 checks, 0 FAIL** (was 3) · differential **22/22
EXACT-MATCH, 0 DELTA**.

---

## 3 · Item 1 — the arena statics

**Scene of record:** `reincarnated-godot/scenes/kc2_arena_e_s09_cp150.tscn`. It is **thin on
purpose**: everything is built at load by `scripts/kc2_arena.gd` from the digest-verified baton.
A baked `.tscn` would carry 344 transforms as editable literals, and the moment a literal can be
nudged by hand the scene stops reproducing the run and becomes a copy that happens to agree today.
GL-6 also has to hold every load, and a baked scene cannot verify a digest.

| element | value | basis |
|---|---|---|
| floor footprint | **86.915 × 85.303 m**, one `PlaneMesh` | the MEASURED occupied region (80.915 × 79.303 m over 5,085 positions: every knot, every spawn, the player track, the sweep track, all six anchors) grown by **one sweep radius, 3.000 m = `config.kit.radius_m`**, read from the wire |
| ground | Y = 0 | `axis_convention.ground_elevation = 0.0` |
| emitters | six anchors at their wire `(x, y)`, seeded to `heading_rad` | `config.arena.spawn_points[]` |
| scatter BOX | **16 m square** per anchor, axis-aligned | shape word = token 1 of `scatter_model` (**BOX**); half-extent from the typed `placement_extents_m` = 8.0. **No circle is drawn for scatter anywhere.** |
| crossers | `w162_a001`, `w163_a004` marked in place | `DIV-P01-TIER`; **0 moved** at the 1e-5 m float32 transform floor |
| player station | plinth + **3.0 m sweep disc** + **2.4 m engage ring** | `radius_m` / `d_engage_m`, and the tracks re-measured to be constant (see NOTE-13) |
| dress | `polygon-dark-fortress` stone floor at its authored 1.249996 m module; anchor pillars; braziers | GL-17 — FRAME / LAYOUT / ORNAMENT / PALETTE only |

**GL-17 restated in the file before the cell started, as the law requires.** No vendor `.tscn` is
duplicated, no existing scene file forked, **no PART A constant inlined** — PART A is pointed at.
Synty assets are instanced by resource path, which is asset use, not copying a reference's content.

**The one place K-2's register and the wire could have collided, resolved without a HALT.** The
Crucible is a **walled pit**; this wire declares `arena_bounds.shape = UNBOUNDED`,
`collision_model = OPEN-PLANE`, and `DECLARED-ARENA-UNBOUNDED` says *"the arena HAS no extent…
not a wall."* K-2's own sentence rules it — *geometry is baton-truth; dress is scene-side* — and a
wall is an **extent claim**, which is geometry. So **no wall, no rail, no pillar ring, no perimeter
of any kind**; the floor ends and the edge is open. The prohibition is **tested, not promised**:
the smoke walks all 1,429 nodes of the built graph for wall-class names and finds none.

### GL-12 absence declarations (seven, asserted by name as a set identity)

| id | state | what is absent, and why nothing was filled in |
|---|---|---|
| `ABSENT-ARENA-WALL` | DECLARED-UNBOUNDED | see above. Reproduced in the declaration: the six anchors' own bbox is 65.662 × 63.831 m, identical to the emitted `width_m`/`height_m`. |
| `ABSENT-EMITTER-P06-BODIES` | DECLARED-OFF | p06 is on the wire and carries **0 of 344** bodies; `run_p06_enabled = false`, `fixture_p06_state_grade = RULED-OFF`. Drawn in a declared-off state — **neither omitted** (which would hide a wire fact) **nor dressed as live** (which would assert a fight that never happened). |
| `ABSENT-EMITTER-SEPARATION-P04-P06` | COINCIDENT-ON-THE-WIRE | NOTE-12. |
| `ABSENT-EMITTER-REGION-GEOMETRY` | POLAR-RESTATEMENT-NOT-A-REGION | NOTE-11. |
| `ABSENT-PATROL-NODE-GEOMETRY` | NOT-ON-THE-WIRE | `path_node_assignment_rule = 'nearest-node'` and the arena declaration names patrol nodes as half of what `width_m`/`height_m` bound — but **no patrol-node list is emitted**. The nodes are visible only as the knots bodies turned at. **No node markers are placed**: their positions would be a reconstruction. |
| `ABSENT-ARENA-VERTICALITY` | GROUND-ELEVATION-ONLY | one `ground_elevation` (0.0) and no height field, ramp, step or relief anywhere. The arena is flat because that is all the wire says. |
| `ABSENT-BODY-IDENTITY` | NO-WIRE-BASIS | NOTE-14 (rides item 2). |

**No GL-12 absence in this cell is a HALT.** Every one is a thing the wire declines to say, said
out loud, with the count it was measured from.

---

## 4 · Item 2 — the roster, and the body-mapping table (VETO-OPEN)

344/344 placed, 344 children in the tree, **0 unmapped**. `path[0]` **IS** the spawn on 344/344,
max |Δ| **0.000000000000 m** — verified rather than trusted, because the body is placed *on*
`path[0]`. **0 of 344** stand outside the floor footprint, so GL-13's clip surface holds for every
body and not merely for most. GL-8 is **structural**: this file asks the loader for a position and
for nothing else — `is_on_board`, `may_hit_test` and every geometry-membership question are never
called from it, at any tick. R-A1-1 is **tested**: zero hud-class node names and zero
`Label3D` / `Label` / `RichTextLabel` / `CanvasItem` of any kind across the whole graph.

### The mapping axis is the wire's, not mine

`record_path`'s **pool directory** is a measured six-way split, and the producer's own
`DECLARED-MAPPING-THREAT-TIER` row states that the four-way `threat_tier` is a **declared collapse**
of it (*"DEVOTION → hero + BOUNTY → hero is a DECLARED MAPPING, not a measured class"*). Reproduced
here as an assertion: **hero 36 + devotion 18 + bounty 9 = 63 = the `hero` tier exactly.** So the
class axis is the finer, measured one. Only the **body choice per class** is register precedent.

### The table — every row states its basis; every row stands for conductor + Matt veto

| # | pool (wire, measured) | n | Synty body | height | **basis** |
|---|---|---|---|---|---|
| 1 | `records/creatures/enemies` | 211 | `SK_Chr_Skeleton_01` (polygon-dark-fantasy) | 1.70 | **RIG PRECEDENT** — `scenes/rigs/mobs/rig_mob_d2_skeleton.tscn`, body **and** height verbatim |
| 2 | `…/hero` | 36 | `SK_Chr_Skeleton_HeavyArmor_01` | 1.75 | **RIG PRECEDENT** — `rig_mob_poe2_skeleton.tscn`, verbatim. Same family as trash **on purpose**, so the tier reads as a promotion rather than a species change |
| 3 | `…/devotion` | 18 | `SK_Chr_Demon_01` | 1.65 | **RIG PRECEDENT** — `rig_mob_gd_ghoul.tscn`, verbatim. Given its own silhouette so the wire's **declared** devotion→hero fold stays visible instead of disappearing into row 2 |
| 4 | `…/bounties` | 9 | `SK_Chr_Gravedigger_Male_01` | 1.75 | **RIG PRECEDENT** — `rig_mob_gd_crazed_villager.tscn`, verbatim. The one non-undead humanoid, because a bounty is a **named individual** |
| 5 | `…/boss&quest` | 59 | `SK_Chr_Demon_Male_01` | 1.85 | **RIG PRECEDENT** — `rig_mob_poe2_bone_deacon.tscn`, verbatim |
| 6 | `…/nemesis` | 11 | `SK_Chr_DarkLord_Male_01` | **2.05** | **⚑ NO BASIS AT ALL — flagged loudest.** No rig precedent (first use of this body in the repo), and **2.05 is a presentation choice** picked for one reason: so nemesis reads taller than boss (1.85). `entity_radius_m` is null on 344/344, so nothing on the wire could have set it — **and nothing on the wire contradicts it either.** |
| — | **body texture** | all | `PolygonDarkFantasy_Texture_01_A.png` | — | REGISTER — the atlas every cited rig already uses |
| — | **per-body species** | 344 | **none** | — | **NO WIRE BASIS.** See NOTE-14. |
| — | **per-body size** | 344 | **none** | — | **NO WIRE BASIS.** `entity_radius_m` null 344/344; `body_radius_role` NON-CAUSAL. |

**What I deliberately did NOT use, and why.** `archetype_tag` (167 distinct): the wire **declares**
it *"GROUPS NOTHING"* (M-11) and names a semantic archetype as a downstream extraction that does not
exist yet — grouping by it would invent a taxonomy the producer explicitly refused to assert.
`display_name` (163 distinct): a real name, but a name→body table is that same absent extraction
wearing a different hat. `hp_max`: on the wire, and using it as a size proxy would fabricate a
mapping the wire does not make.

**The read this produces, said before Matt sees it: 344 bodies in six dresses looks like a clone
army. That IS the measurement** — six is every distinction this wire makes about what a body *is*.
The honest fix is a producer-side one (a species / family / radius carrier), not a presentation-side
guess. Routable if wanted.

---

## 5 · Item 3 — the CP-A still-set

**PL-5 floor check, run BEFORE anything was built:** `captures/` = **6.67 G of a 10 G ceiling
(66.7 %)**, **3.33 G headroom → PASS**. The check lives inside the harness, not in my head: `du -sk`
on the captures tree, a named HOUSEKEEPING HALT on breach, and an **unmeasurable** tree is also a
halt — a render cell does not open on an unmeasured floor. After the set: 6.67 G (the 9.2 M set is
inside the rounding).

**Class E — owner-eye. UNTRACKED, never committed.** Directory:
`agentic_orchestration/galadriel/captures/2026-08-12-sb1-cpa/` · 1920×1080 · **9.2 M total** ·
`MANIFEST.json` beside them carries every sha256, subject and camera pose.

> ### Framing sentence (charter § 6 — the sentence Matt reads before looking)
>
> **This is run E-s09-cp150 standing still: an unwalled stone floor cut to the exact ground the
> fight covers, six emitter anchors with the 16 m boxes the sim actually rolled bodies into, and
> all 344 of them frozen on the spot the wire says each one spawned — wearing six dresses, because
> six is every distinction this wire makes about what a body IS.**

| # | file | sha256 | subject |
|---|---|---|---|
| 01 | `01-arena-wide.png` | `a09187a7416a8020d95bbdc002c3c5f5e5c8068fce79d6d4d06c7bae3273d286` | **Arena wide** — the whole measured floor, all six anchors with their BOXes, the player station at the origin, and the open edge |
| 02 | `02-arena-detail.png` | `8dd11398805dce90c0718759ab3cc9dfa40a5dfc1372157d9ddbbcd231bd08a8` | **Arena detail** — the station at eye height: plinth, the 3.0 m sweep disc (blue), the 2.4 m engage ring (violet), on dark-fortress stone at its authored 1.25 m module |
| 03 | `03-roster-overview.png` | `51d3606f49a642a2c5846e3d9752404a7ea2338691eab0d66b5984b0488a8aec` | **Roster overview** — all 344 at once, framed on the **body** bbox rather than the 87 m floor (a frame drawn to the floor makes 344 people into specks). Five live clouds: p04 96 · p01 75 · p03 66 · p05 61 · p02 46 |
| 04 | `04-spawn-box-p01-crossers.png` | `317fe96ebdd83bf18f4f517db42b448e424eaa9e4a588ff75416d726e3d63390` | **Spawn BOX p01 with the two crossers called out** — `w162_a001` and `w163_a004` under red beacons standing on their own feet, outside the gold 16 m box, **where the sim put them** |
| 05 | `05-spawn-box-p05-ambush.png` | `be530f233eac343d68912d80ff001b749b6cee1adf6ef2f6528e7ba45474706f` | **Spawn BOX p05** — the ambush emitter 7.159 m from the origin, 61 bodies in one box almost on top of the player: the two-knot straight walkers and the +48…+306 tick drip, one population |
| 06 | `06-body-dress-parade.png` | `ec619ca0a679324a1fe1d1ee2c48fbb1e5d176be3845e6b851cb876f7fd9ebff` | **Body-dress group shot** — capture-only staging, one body per class, L→R trash · hero/HERO · hero/DEVOTION · hero/BOUNTY · boss · nemesis. **This is the veto surface for § 4's table.** |
| 07 | `07-emitter-p04-p06-coincident.png` | `0d30f898c3be4157b0bdaab782a5758b8bccca60597a54bc615a55d3b8500f6e` | **p04 and p06 — one place, two ids** (NOTE-12). p04 live with 96 bodies in gold; p06 DECLARED-OFF with 0, its grey box underneath. No separation invented |
| 08 | `08-open-edge.png` | `bef3e0ae4993f81700e5fcab4b67fd550c7f8fa385985fba4a2e7ff40cff66e4` | **The open edge** — what "no wall" looks like, and **the still most likely to be vetoed** |

**Callouts are geometry, never text.** No `Label3D`, no `Label`, no canvas node exists anywhere in
the scene or the harness — the beacon over a crosser is a cylinder standing on that body's own feet,
and the words live in the manifest (R-A1-1).

### ⚑ What the frames caught in my own items 1–2, fixed before CP-A shipped

I looked at every still with my own eyes rather than trusting the PASS line, and the frames found
three things the assertions had not:

1. **Double build.** `add_child()` into a live tree runs `_ready()` → `build()`, and the capture
   harness then called `build()` itself: **a second floor z-fighting the first, a second set of
   marks, 688 bodies.** Caught in the log before it reached a still. `build()` is now idempotent and
   the smoke **asserts** it — 6 children before, 6 after, roster still 344.
2. **The rainbow plinth.** The player plinth came back painted with the pack's palette **strip**,
   because the DarkFortress Alts atlas was forced onto a `Generic/Base` mesh whose UVs were authored
   for a different atlas. Dropping the atlas was not the fix either — the FBX imports carry no
   material and rendered flat white. The atlas now applies **only** when the prop lives under the
   subtree that atlas was authored for; a mismatch warns and is refused rather than painted.
3. **p04 and p06 are not two places** — see NOTE-12. The "p06 DECLARED-OFF" frame came back showing
   96 **live** bodies in a **gold** box. This one is the reason the item-3 rule is *look at the
   frames*: no assertion I had written could have caught a still that was true about geometry and
   false about what it claimed to depict.

---

## 6 · NOTES (continuing from NOTE-9)

**NOTE-10 — the wire's `width_m`/`height_m` is the ANCHOR HULL, not the arena floor.**
`config.arena.width_m/height_m` = **65.662 × 63.831 m**, and that reproduces **exactly** as the
bounding box of the six `spawn_points[]` anchors. `DECLARED-ARENA-UNBOUNDED` says so:
*"the emitted width/height are the bounding box of the cited emitters and patrol nodes, not a
wall."* The run's actual occupied region is **80.915 × 79.303 m** — larger on all four sides,
because bodies scatter ±8 m about the anchors and then walk. **A consumer that sizes a floor from
`width_m`/`height_m` puts bodies on nothing,** and under **GL-13** — telegraph-class ground FX clip
at the floor-mesh footprint — it also mis-clips every FX at the perimeter. Not a wire defect; a
prose-shaped consumer hazard of exactly the NOTE-4 class. My floor is measured from every position
and grown by one sweep radius.

**NOTE-11 — `arena_ref.emitter_radii` is a POLAR RESTATEMENT of `spawn_points[]`, not region radii.**
The field reads like six emitter-region radii (7.159 → 35.758 m). Measured: `p0N_m` reproduces
`hypot(spawn_point.x, spawn_point.y)` on **6/6 anchors to 0.376 mm** — the 3-dp position
quantisation. It is the anchors' polar radius about the arena reference frame: the same data in the
other coordinate system. **Six 30-metre "emitter region" discs would have been a fabrication built
on a misread.** Measured, reported, and NOT DRAWN. (Composes with my standing obligation O-3, which
reads `emitter_radii.grade = CITED-PER-ARENA` as permitting emitter rings — the grade permits
drawing what the field *is*, and what it is turns out to be the anchors themselves.)

**NOTE-12 — p04 and p06 are 0.462 m apart: one place, two ids.**
Anchors p04 `(30.905, 7.147)` and p06 `(31.215, 6.805)` are **0.462 m** apart — well inside the
scatter box's own 8.0 m half-extent — so their declared 16 m BOXes are the **same square** to the
eye and their anchor props overlap. p04 is live with 96 bodies; p06 is DECLARED-OFF with 0. All 15
anchor pairs are now measured and any pair inside the half-extent is declared. **No separation is
invented to make them read as two places.** Consequence for later cells: any still or clip framing
p04 is also framing p06, and a per-emitter presentation treatment (colour, label, camera) has to
handle two ids resolving to one location.

**NOTE-13 — the player never moves in this run, and the channel never stops.** ⚑ **The biggest
CP-B fact in this cell.** `tracks.player_path.x` and `.y` take exactly **one distinct value each
across all 3,732 samples — `{0.0}`**. So do `circle_sweep.centre_x/centre_y`. `radius_m` is `{3.0}`
on all 3,732 and `channel_active` is **true on all 3,732**. The "player sweep" of charter § 6's
CP-B is therefore a **spin in place**, not a translation: there is no player locomotion to render in
this run at all, and the 3.0 m sweep disc is a genuine **static** of this scene rather than a motion
artefact. This is what makes K-3 (the channel→heading mapping) the *entire* player-presentation
question for CP-B — heading is the only player channel that varies, and `heading_rad` is
DECLARED-NON-SEMANTIC, so the mapping is wholly conductor-ruled. The builder re-measures the
constancy rather than trusting it: if the track were not constant it declares the station UNDEFINED
instead of drawing a fixed ring.

**NOTE-14 — the wire carries NO body species and NO body size.** `entity_radius_m` is **null on
344/344** and `config.kit.body_radius_role` is `NON-CAUSAL`. `archetype_tag` (167 distinct) is
**declared** to *"GROUP NOTHING"* (M-11), with a semantic archetype named as a downstream extraction
that does not yet exist. `display_name` (163 distinct) is a name, not a class. The **only** measured
grouping this baton carries about what a body *is* is `record_path`'s pool directory — six classes —
and the wire itself declares that `threat_tier` is a collapse of that. Everything above six is
presentation invention, and I did not do it. Filed as `ABSENT-BODY-IDENTITY`.
**Producer-side fix if this matters at CP-C:** a typed species/family carrier and a real
`entity_radius_m`. Not mine to patch — routable to knight-rider for star-lord, riding the NOTE-5 /
NOTE-6 micro-item.

**NOTE-15 — Godot's `JSON.stringify` cannot round-trip a 1-ULP double, and my first GL-10 mutant
died of it.** The mutant perturbed `config.kit.tick_period_s` by one ULP in memory; the difference
**existed in RAM and vanished in the file**, so the mutant reached the loader carrying **no defect
at all** and the check passed as a green — a falsification test proving nothing, dressed as a pass.
The harness now finds its **own instrument floor**: it doubles the perturbation, writes, **reads the
file back**, and stops at the first value that survives the round-trip — measured at **6 doublings
from 1e-18 → 97 × 1e-18 absolute, 1.19 ppq relative** — and asserts at that measured magnitude,
which is printed. This is NOTE-9's law applied to an instrument instead of a count: **a gate whose
threshold is set by its own write path must measure that path, not assume it.** Bears on any future
cell that mutates a float through `JSON.stringify`.

**NOTE-16 — the roster stands in the FBX's imported REST POSE, and no pose is authored.**
A pose is motion, motion is CP-B, and choosing an idle here would be choosing a presentation state
the wire says nothing about — so the 344 bodies stand in the retargeted rest (arms out). It reads as
a placement diagram rather than an arena, and that is the honest zero-choice state of a statics
cell. **The fix exists and is one line if the conductor wants it**: `scripts/mob_rig.gd` already
binds a retargeted idle (`A_MOD_BL_Idle_Standing_Masc`) onto any of these bodies. Cost: 344
`AnimationPlayer`s. Named here so CP-B can take it deliberately rather than acquire it by accident.

---

## 7 · Attack surfaces for the motion phase (CP-B)

Named so the gatekeeper and the conductor do not have to find them:

1. **There is no player locomotion to render** (NOTE-13). CP-B's "player sweep" is a spin at the
   origin. If the cell is scoped as "locomotion watch: paths, dwells, straight walks, spawn drip,
   player sweep", four of those five are **monster** locomotion and the fifth is a rotation whose
   mapping K-3 has not yet ruled. That is a scope fact worth settling before the cell fires.
2. **`strike()` exists, `charge()` does not, and that is load-bearing.** K-1's impact-anchored
   ruling is enforced *structurally* today only because no wind-up driver exists to call. The first
   CP-B cell that adds any anticipation timing re-opens it. There are **zero telegraph rows** in the
   event vocabulary to drive one from.
3. **The 17 dwells vs the named 12** (NOTE-1). Five are Δtick = 1. At watch scale they are
   invisible, but a motion driver that special-cases "dwell" will branch on all 17.
4. **Cross-leg speed is non-uniform on 282 of 283 multi-leg bodies at 1e-6 m/s.** A rig driven by one
   speed per body puts the bodies that clip an arrival step in the wrong place for a whole leg;
   `leg_speed_ms(actor, leg)` exists and there is deliberately **no per-body speed accessor**.
5. **The spawn drip is up to +306 ticks ≈ 25.0 s on 61 bodies** (NOTE-2), and it is entry time, not
   jitter. A per-wave batch spawn destroys the ambush.
6. **`build()` is idempotent now — keep it that way.** Any CP-B node that rebuilds the arena per
   frame or per tick will silently get away with it and cost nothing visible until a still shows
   z-fighting.
7. **p04/p06 coincidence** (NOTE-12) — any per-emitter camera or per-emitter treatment has two ids
   at one location.
8. **The floor footprint is GL-13's clip surface** and it is 86.915 × 85.303 m, centred at sim
   `(-1.819, 0.244)` — **not** at the origin. Telegraph FX clipping must use the measured rectangle,
   not a symmetric assumption about the arena centre.
9. **R-A1-1 has no enforcement outside the smoke's node-name walk.** It catches a node called
   `DamageNumber`; it would not catch a texture with digits baked into it. If CP-B adds any HUD, the
   check needs to grow with it.

---

## 8 · Where to attack this cell

(a) The floor **margin** is one sweep radius — wire-grounded, but the *choice to use the sweep
radius as the margin* is mine, and a different defensible margin would move GL-13's clip surface.
(b) The **six-dress mapping** is the largest presentation-side judgement in the cell and row 6 has
no basis at all. (c) The **dress register pick** (`polygon-dark-fortress`) satisfies "Crucible-
adjacent" by my reading of the F-V2-1 ruling; the ruling names the *setting*, not the pack.
(d) The still-set is **8 poses**, and poses are framing — a different eight would tell a different
story about the same geometry; the manifest carries every camera pose so the framing is auditable.
(e) `emitter_radii` is reported and not drawn (NOTE-11) — if a later reading finds it *is* a region
radius after all, the arena needs six discs it currently refuses to draw.

---

— drax, presentation seam, 2026-08-12. *Four items, five commits, zero halts. Three defects the
assertions missed and the frames caught, fixed before Matt sees them. Nothing pushed.*
