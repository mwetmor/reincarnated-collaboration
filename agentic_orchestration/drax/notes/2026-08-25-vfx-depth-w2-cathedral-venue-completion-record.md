# VFX-DEPTH RUN — WAVE 2 (drax) — CATHEDRAL VENUE — COMPLETION RECORD

**Date:** 2026-08-25 · **Agent:** drax (presentation seam, `reincarnated-godot/`)
**Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** `gandalf/notes/2026-08-25-vfx-depth-run-charter.md`, R-15 + R-16
**Class:** evidentiary note · **Status:** CURRENT
**Commits:** collab `64dfeb4d` · `c663ff67` · godot `27baafc`

**Status: PARTIAL — 4 of 5 tasks COMPLETE, TASK 3 (A-arm) PARKED-NAMED** per charter § 2's honorable
fallback, with its specific deficit and the exact re-host seam recorded in § 4 so it is not re-derived.
**Five findings routed (§ 8). Two of them refuse an instruction, and both refusals are load-bearing.**

---

## 0. THE ARTIFACT PATHS — the deliverable, because the media is gitignored

| # | Arm | Path | Verified |
|---|---|---|---|
| **B** | twin + 4a, Cathedral, ratified camera | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxon.mp4` | h264 yuv420p 1920×1080, 60/1 fps, **210 frames, 3.500 s**, 2,250,003 B · sha256 `19d5e9c29dbc67cb…` |
| **B-ctl** | control, same build, VFX hidden | `…/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxctl.mp4` | same stream params, 2,179,910 B · sha256 `f8434eb643c3e24b…` |
| **A** | HITL re-hosted | ⛔ **NOT RENDERED — PARKED-NAMED, § 4** | — |

| Manifest | Path |
|---|---|
| **B-arm reproduction manifest** | `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-25-vfx-depth-w2-b-arm-reproduction-manifest.md` |
| **A-arm reproduction manifest** | **not written — there is no render to reproduce** |
| **Disk Round-1 manifest + receipt** | `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-25-vfx-depth-w2-disk-round-1-manifest.md` |
| **Raw render log** (8.5 MB, full per-frame census) | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w2-bcath/render.txt` |

---

## 1. TASK 5 — DISK ROUND-1. **THE NAMED CANDIDATE WAS CLASS A AND I DID NOT DELETE IT.**

Full manifest + receipt at the path above. The headline:

**R-16 names the 26 GB `s2c38*` scratch as the Round-1 candidate. That naming inherited a FALSE
PREMISE FROM MY OWN W1 F-3**, which said the corpora were *"S2C intermediate PNG ladders already
copied into `harness_logs/`."* Measured: `harness_logs/s2c_rows38_2026-08-25*` holds **3–7 files each,
~29 MB total, ZERO PNGs.** The ladders exist only in the user dir.

All seven S2C corpora carry a `BANKED` marker **I wrote myself on 2026-08-25T23:51:11Z**, plus a
cleared directory write-bit, plus a runner-level guard (`banked_corpus_guard.sh`) that exits 5 rather
than aim at them. `s2c38/BANKED` names **jack-ryan #81 (RULED)** and `prepost.json` as what rests on
them. **That is R-16's own Class A definition, verbatim.** The 3A recapture dispatch had already ruled
the identical question: *"Do not reclaim `s2c38`/`s2c38b` to make room … halt and route to me."*

⚑ **The protocol's step (a) asks the wrong question, and that is worth more than this round.** It asks
whether the recapture **CONSUMES** them. It does not — it captured into `v3`/`v3b` precisely so it
would not touch them. But the pre/post comparison it produced **CITES all four**, and `prepost.json` is
uncomputable without them. **Consumption was the wrong predicate; citation is the one that binds.**

**What Round-1 actually deleted:** 21 non-banked directories, each with a verified regeneration route
— three review-clip ladders whose *own producing script* `rm -rf`s them on every invocation, S2B
scratch whose `harness_logs` copies were **PNG-counted equal** rather than assumed, and probe/smoke
scratch.

```
BEFORE  49,157,600 KiB avail
AFTER   52,713,480 KiB avail        FREED = 3,555,880 KiB = 3.39 GiB
```

Projection 3,472 MB vs actual 3,556 MB — **agree to 2.4 %.** Banked corpora **re-counted after the
`rm`**, not assumed safe because I did not name them: `2106 / 2106 / 2106 / 2106 / 874 / 874 / 874`,
every count matching its own marker's figure.

**50.3 GiB free is still under the 60 GB tripwire and I am not going to imply otherwise.** The only
Class B mass large enough to clear it is `.godot` (17 GB) — an import cache, regeneratable by
definition, whose deletion stalls the render lane for an unbounded window. **Dropping it while holding
the serial godot lane in a capture wave is the wrong hour.** Round-2 is owed at lap close.

*(Post-render note: the B-arm render then consumed ~2.4 GB, so free space closed the wave at 48 GiB.
See F-3 — the venue itself is the new disk story.)*

---

## 2. TASK 1 — THE CATHEDRAL FIGHT SURFACE. **The fight was never on tile at all.**

`27baafc` · `scripts/s2_stage_env.gd` + `scripts/s2_cathedral_floor_probe.gd`.

Matt's order: *"extend the mountain surface on the bottom so that the tile floor could also be extended
enough to encompass the fight surface."*

**I built a probe before authoring geometry, and it answered a question the order implies but does not
state — WHY there was no floor.** `s2_cathedral_floor_probe.gd` walks the LIVE re-homed scene rather
than the pack's filenames:

```
nearest flat mesh   SM_Env_Ground_Grass_Small_01 (92)   r = 11.82 m
then                SM_Env_Rocks_Small_01 (52)          r = 14.21 m
                    SM_Env_Ground_Dirt_Small_01 (57)    r = 18.09 m
```

**Every flat surface within 22 m of the derived arena centre is TERRAIN. Not one of the pack's 1,063
`SM_Bld_Base_Floor_*` tiles is under the fight.** The ritual circle that `_derive_arena_center` locks
onto sits on a rock outcrop **outside the nave** — exactly the hazard the file's own
`ARENA_CENTER_DECLARED` block had warned E-0 about, firing again on a different camera.

### The build

`_extend_fight_surface()` lays **126 pack floor tiles** over a **16.0 m** disc at the derived fight
plane and builds a **four-flank, 148-rock skirt** under and around it.

**The radius is derived, and the derivation names which demand binds:**

| demand | figure |
|---|---|
| (a) FRAME — ground depth at the judging camera | `18.8840 / tan(68.847°) = 7.31 m` near edge → `18.8840 / tan(37.061°) = 24.98 m` far = **17.68 m** |
| (b) THE CAST — in-channel translation, lock dollying with it | 3.5 m/s × (3.70 − 0.20) s = **12.25 m** |

**(b) binds, and it is the one a still frame cannot show you.** A disc sized only to (a) runs out of
floor under a moving subject halfway through the clip. 16.0 m clears (b) with margin and fits inside
`STAGE_RADIUS_M` = 26 m by construction. **Verified in the delivered frames:** at `08-release-late` the
caster has translated and is still fully on tile.

### Three things I learned by rendering them wrong

Each is fixed at the cause and written down at the fix, not in a note beside it.

1. ⚑ **Tree-order donor selection returned a WOODEN-PLANK floor.** The pack ships one floor mesh and
   its look is carried entirely by which instance's material you clone — so *"which instance"* IS
   *"which floor"*, and tree order is picking a look at random. The extension came out a **32 m wooden
   deck butted against the nave's stone**. It was obvious in one frame and **invisible in the meta**,
   which printed a donor name and a tile count and nothing about colour. `_donor` now takes the
   NEAREST matching instance — which is also the principled choice, because the job is to *continue*
   the floor already adjacent to the fight surface.
2. ⚑ **The z-fight guard tested AABB brackets with no flatness condition, and punched out half the
   fight surface.** A 25 m cliff's box brackets an enormous footprint while its surface sits 15 m
   below the fight plane. Unrestricted: **66 of 129 cells skipped as "already floored"** on the
   strength of boxes belonging to rock. Restricted to flat meshes: **3 skipped, 126 laid. A box is not
   a surface.** *(The probe's own ground-reach column has the identical defect — it reports "none
   within 24 m" on all sixteen bearings — and is relied on nowhere. Named in the file so no later
   reader trusts it.)*
3. ⚑ **A skirt entirely below y = 0 does not hide a disc's rim; it sits under it.** The first frame
   showed a tiled slab hanging in air with a machined straight edge and void beneath. The lip flank
   now crests to **y = +0.35** so rock breaks the plane and occludes the rim from a camera looking down
   at 52.95° — which is also what a mesa actually looks like.

### Two properties I built in rather than hoped for

- **Tiles and rock are the pack's own meshes CLONED off live donors, never authored primitives wearing
  the atlas material.** Synty selects colour BY UV; a `PlaneMesh` carrying
  `PolygonDarkFantasy_01_A_mat` samples whatever atlas cell its default UVs land on. **That is how you
  get a hot pink cliff.** Cloning `mesh` + `material` carries correct UVs by construction.
- **Determinism:** the skirt's jitter is one `RandomNumberGenerator`, `seed = 20260825`, **no other
  consumer.** Two builds place identical rock, so the stage clock pin and the control-arm receipt
  survive the venue change.

---

## 3. TASK 2 — THE CAMERA PORT. **`0.000000000000 m`, IN THE CATHEDRAL.**

**There was no port to make, and finding that out was the work.** `wwcr_stage.gd` has routed `--stage=`
to the shared builder `s2_stage_env.gd::build()` since E-0 — the *same function the S2 review path
calls*. So the venue is a **runner parameter**, and **both arms enter the same builder rather than two
rooms that resemble each other.** Nothing was copied to make this work; `STAGE` was added to
`run_wwcr_stage.sh` (default `bare`, so every prior corpus name and the C-3-albedo-anchored measurement
path are byte-unmoved).

**Verbatim from `harness_logs/wwcr_2026-08-25-w2-bcath/render.txt`:**

```
[wwcr] PL-PIN unscaled offset (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       vs pl_audit.json (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       — |delta| 0.000000000000 m, z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
[wwcr] PL-CAM k=0.665000 — DOLLY only. pitch 52.9535411256029 deg  yaw 47.0 deg
       fov_v 31.7861018306101 deg VERTICAL/KEEP_HEIGHT  z_player 34.8165340347471 m
[wwcr] PL-CAM offset k=0.665000 (THIS RUN) = (9.7929267883301, 18.8840122222900, 9.1654367446899) m
       stand-off 23.1627407073975 m  height 18.8840122222900 m
[wwcr] PL-AUDIT anchor: subject ground projects to frac (0.501041571299, 0.550925191243);
       expected (0.501041450500, 0.550925123427);
       delta (0.000000120799, 0.000000067817) frac = (0.0002, 0.0001) px at 1920 x 1080
```

**Every dispatched parameter met exactly.** W1's bar was `0.000000000000 m`; the Cathedral render
prints the same number.

⚑ **The anchor audit is a REAL test here and not a formality.** The venue change moves the entire world
around the subject, and the fight-surface extension re-tiles the ground the anchor is solved against.
**Had the extension shifted the derived floor plane, the anchor would have moved and convicted the
build.** It moved **two ten-thousandths of a pixel** — single-precision residue, the same figure W1
recorded on the bare stage.

---

## 4. ⛔ TASK 3 — THE A-ARM. **PARKED-NAMED, WITH THE SEAM RECORDED.**

Charter § 2: *"a row that cannot reach the standard within the run is PARKED-NAMED with its specific
deficit as a finding — never silently trimmed."* This is that, and I would rather hand over an honest
gap with a map than a half-landed re-host with no reproduction manifest.

### 4a. THE DEFICIT, precisely

The HITL treatment is **not a portable effect module.** It is `scripts/kc2_player_channel.gd`
(**4,217 lines**), driven by `scripts/kc2_cpb_clip.gd`, and it is coupled to:

- the **Undead Knight FBX + warhammer rig** at `WEAPON_SCALE 1.95`, with head/helmet attachments
- a **recorded trace** played through `kc2_motion.gd` on `Kc2Arena.baton`, with shot windows expressed
  in **ticks** (1570–1700), not seconds
- `kc2_arena.gd`'s own world: actor placement via `_arena._v3(sim_x, sim_y)`, a measured
  `footprint`, named anchors, and a **`camera_ground_gate()` that can REFUSE a pose** before a frame is
  written
- a **60-frame tick-frozen preroll** (CLK-1) that is rendered and then pruned

Re-hosting it is a scene-graph surgery on a live cell, not a `--stage=` flag.

### 4b. THE SEAM, so the next session does not re-derive it

**It is smaller than the file sizes suggest, and I found it.** `kc2_arena.gd` (972 lines) localizes
everything that would have to change:

| what | where | note |
|---|---|---|
| the arena floor | `kc2_arena.gd:545 _build_floor(fp)` | **one `PlaneMesh` named `ArenaFloor`** — deliberately one mesh so the footprint is exact (GL-13) |
| the environment | `kc2_arena.gd:321` | one `WorldEnvironment` + `Environment` — **must be freed, or it fights `_lift_env()`'s** |
| the re-home target | `kc2_arena.gd:585 _build_player_station()` → `report["player_station"]` | the Cathedral must be re-homed **to the player station, not to world origin** — `S2StageEnv.build()` homes the arena centre to the origin, and the kc2 player is NOT at the origin |
| the refusal risk | `kc2_arena.gd camera_ground_gate()` | nine frustum rays must land inside the skirt or beyond fog saturation; **a Cathedral swap can make this REFUSE**, and that is a real gate, not a formality |

**Estimated shape:** ~60–80 lines in `kc2_cpb_clip.gd` after `_arena.build()` — free `ArenaFloor` +
skirt + the arena `WorldEnvironment`, call `S2StageEnv.build(self, "cathedral")`, re-parent
`PackCathedral` + `FightSurface` under a `Node3D` positioned at `report["player_station"]`, then
re-run the ground gate. **Provenance law is unaffected: this touches `kc2_*`, never a `wwcr_*` file.**

**Render cost, projected from measured data:** 658 frames + 60 preroll at the Cathedral's measured
**2.78 MB/PNG** ≈ **2.0 GB** of intermediates for one pass.

### 4c. ⚑ AND THE LABEL MOVED AGAIN — I over-corrected in W1, and I am carrying it rather than leaving it

My W1 record says of the reference clip: *"It is **NOT a whirlwind**."* **That is wrong, and I read the
source rather than my own note this time.** `kc2_cpb_clip.gd:111-112`:

> *"It exists to answer ONE question — does the **whirlwind** read, now that the man has a head, a
> hammer, and a rate Matt chose?"*

The Undead Knight **spins a warhammer and throws cut/spark arcs at `CUT_PER_REV 17`**. **The clip's
subject IS a whirlwind cast.**

**Both things are true, and conflating them is what went wrong twice:** `WW-7` is an **SB-1
run-ledger cell id** and is not a whirlwind label — knight-rider's retraction of that mis-citation
stands. But *"the cell id isn't a whirlwind name"* does not license *"the clip isn't a whirlwind."*
**I turned a correct narrow correction into a wrong broad one, and a wrong correction sitting in the
record is worse than the original error** because it now carries a retraction's authority. This
dispatch's Task 3 wording — *"the HITL whirlwind effect"* — **is right**, and my W1 note is what needs
amending.

---

## 5. TASK 4 — THE B-ARM. **RENDERED, AND THE EFFECT IS BYTE-UNCHANGED FROM W1.**

Full parameters at the reproduction manifest. The receipt that matters:

```
$ git diff --stat fde563c..HEAD -- scripts/wwcr_whirlwind.gd scenes/wwcr_stage.tscn scripts/wwcr_stage.gd
    -> EMPTY
```

**The B-arm is W1's clip-3 article in a new room, and nothing else moved.** Every difference between
W1 clip 3 and this clip is attributable to the venue alone — which is the property R-15 exists to
create, obtained here mechanically rather than on my word.

`FRAME_CENSUS rendered=420 delivered=420`. `tinted_count_is_2: true` — **R-9's assert passed on this
render**, in the new venue. `scuff_is_tinted: false`, `SCUFF_COLOR` byte-untouched.

**W1 F-2 constraint honoured:** `mi.scale` is not used to carry size variation anywhere in this
landing. `billboard_keep_scale` remains unset and 4a's mechanism is position-only.

---

## 6. DEFEAT-CONDITION RECEIPT — pasted mechanically, no eye-curation (#72)

`HEAD = 27baafc`. Instrument: the **corrected** glob from R-11(b) (`scripts/run_wwcr_stage.sh`, not
bare `run_wwcr_stage.sh`).

### [1] Full-history test, audited commit `1692d6e`

```
$ git diff 1692d6e..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'scripts/run_wwcr_stage.sh' | grep '^+' \
    | grep -Ei 'vfxbo|cpb|kc2|a337d30|sb1|etch|claw|cut_|rig_poe1|cyclone|run_ww[0-9]|PAL_|decay_gamma|sheath'

+#   character-for-character from `scripts/kc2_cpb_clip.gd:304-317`, which itself
+#   READ-ONLY, PARAMETERS ONLY. `kc2_cpb_clip.gd` is quarantined-adjacent SB-1
+const PL_PITCH_DEG := 52.95354112560294       # kc2_cpb_clip.gd:304 <- wr2_playback.gd:1806
+	#   Same guard kc2_cpb_clip.gd:509 carries, and for the same reason.

[4 matching lines]
```

**Identical to W1's four lines — the same adjudicated camera-provenance citations, already ruled on at
R-11(b). W2 added none.**

### [2] W2's OWN contribution, isolated (`6184385..HEAD`) — the test that is new information

```
$ git diff --stat 6184385..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'scripts/run_wwcr_stage.sh'
 scripts/run_wwcr_stage.sh | 27 +++++++++++++++++++++++++--
 1 file changed, 25 insertions(+), 2 deletions(-)

$ …same diff… | grep '^+' | grep -Ei '<the token set>'
[hits=0]
```

**ZERO hits.** W2 touched exactly one file in the guarded set — the harness — and added 25 lines.

### [3] Float-literal intersection, W2's own added floats

```
$ git diff 6184385..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'scripts/run_wwcr_stage.sh' \
    | grep '^+' | grep -oE '[0-9]+\.[0-9]+' | sort -u
0.085
```

**One value. `0.085` is `BARE_ALBEDO` — this stage's own C-3 anchor constant**, named in a comment
explaining why the measurement corpora must stay on `bare`. It originates in `wwcr_stage.gd:26` and in
`s2_stage_env.gd::BARE_ALBEDO`, both non-quarantined. **No float crossed from
`kc2_player_channel.gd` or `kc2_etch.gdshader` — the two effect-authoring quarantined files.**

### [4] The certified artifact

```
$ git diff --stat fde563c..HEAD -- scripts/wwcr_whirlwind.gd
    -> EMPTY. Byte-identical to the W1 4a landing.
```

**VERDICT: LINEAGE CLEAN.** W2's entire landing sits in `run_wwcr_stage.sh` (25 lines),
`s2_stage_env.gd` (venue, not an effect file) and a new read-only probe. **The twin effect did not
move.**

---

## 7. SMOKE GATES RUN

| Gate | Result |
|---|---|
| Cathedral builds at the judging camera, marks mode | PIN MATCH · `STAGE_META` complete · no `SCRIPT ERROR` |
| Fight surface, second cut (donor + guard + skirt fixed) | 126 tiles laid · 3 skipped · 148 rocks · 274 nodes |
| Shell syntax, amended runner | `bash -n scripts/run_wwcr_stage.sh` → OK |
| Frozen runner vs in-tree, **before** the run | sha256 `4c06c106…745978`, identical |
| Full B-arm capture | `FRAME_CENSUS rendered=420 delivered=420`, both MP4s ffprobed |
| Default path unmoved | `STAGE` unset ⇒ `--stage=bare`, prefix appends nothing — byte-identical invocation to every W1 run |
| Pre-fire disk projection (#1.1) | measured 2.78 MB/PNG **on this exact stage+camera**; projected 4.47 GB worst case, actual ~2.4 GB, 50 GiB available |

---

## 8. FINDINGS ROUTED — five

**F-1 — ⚑ R-16'S ROUND-1 CANDIDATE IS CLASS A, AND MY OWN W1 F-3 IS WHY.** Route: **gandalf** +
**knight-rider**. Detail in § 1 and the disk manifest. The transferable part is the predicate, not the
directory: **"does anything CONSUME it" is the wrong question; "does anything CITE it" is the one that
binds.** A round protocol that asks only the first will eventually delete a seal's evidence base and
print a clean receipt doing it.

**F-2 — ⚑ MY W1 "IT IS NOT A WHIRLWIND" CORRECTION WAS ITSELF WRONG.** Route: **gandalf** +
**knight-rider**; my W1 note needs amending. Detail in § 4c. `kc2_cpb_clip.gd:111` settles it. The
shape worth carrying: **a narrow correction ("`WW-7` is a cell id, not a whirlwind label") was
generalised into a broad claim ("the clip is not a whirlwind") that the source refutes** — and because
it arrived as a *correction*, it carried more authority than the error it replaced.

**F-3 — ⚑ THE CATHEDRAL VENUE COSTS 42× THE DISK PER FRAME OF THE BARE STAGE, AND R-15 THEREFORE
COLLIDES WITH R-16.** Route: **gandalf** (conductor call). Measured on identical camera and capture
settings:

| stage | mean PNG |
|---|---|
| `bare` (W1) | **66,559 B** |
| `cathedral` (W2) | **2,779,536 B** |

One AB pair costs **~2.4 GB** where W1's cost 30 MB. **R-5 retrofits all 24 T-A rows at this venue**;
at one AB pair per row that is **~58 GB**, against 48 GiB free. **The run cannot retrofit 24 rows at the
Cathedral without either a disk plan or a PNG-retention policy** (the frames are the intermediates —
the MP4s are 2.2 MB). Cheapest lever: prune the PNG ladder after a verified encode, which
`run_ww7_gate2_clip.sh` already does under FG-12 and `run_wwcr_stage.sh` does not.

**F-4 — THE CATHEDRAL AT 16 m OF FIGHT SURFACE IS A COMPOSITION TRADE, AND IT IS MATT'S EYE'S CALL.**
Route: **Matt**, at his next look. The tile disc now fills roughly two-thirds of frame at the judging
camera; the nave reads at frame-right and the mountain at frame-left, but **the diorama drama of the
ratified referent — cathedral perched on a mountain, seen whole — is gone at this stand-off.** That is
the direct consequence of his own order plus the 12.25 m travel requirement, and both are correct
individually. **I am not shrinking the disc to buy the composition back**: a caster who runs off the
tile mid-clip is a functional failure and a worse one. If Matt wants the room to read bigger, the lever
is the **camera** (k), not the floor — and the camera is ratified and not mine to move.

**F-5 — `_playerlock_aim` STILL IGNORES ITS `focus` ARGUMENT.** Route: **gandalf**, carried forward
from W1 unchanged. The two call sites pass different things and agree only because the king starts at
the origin. *Happens to agree* is not a property, and the Cathedral did not change it either way.

---

## 9. WHAT I DID NOT DO, AND WHY

- **Did not delete `s2c38*`.** § 1. Class A, banked, guarded, and already ruled on by a dispatch.
- **Did not delete `.godot` (17 GB).** Regeneratable, and the largest legitimate Class B target — but
  dropping an import cache while holding the serial godot lane in a capture wave is the wrong hour.
  Round-2, at lap close.
- **Did not render the A-arm.** § 4. Parked with the seam mapped rather than half-landed without a
  reproduction manifest.
- **Did not run two heavy captures concurrently.** Charter § 6: one heavy capture at a time.
- **Did not move the Tier-1 element sweep to the Cathedral.** It keeps `--cam=inspect` and `bare`; it
  has no motion question, no AB counterpart, and moving it would break comparability with the landed
  element corpus for free.
- **Did not change the `bare` default anywhere.** Every measurement corpus gated against the C-3
  albedo 0.085 anchor is byte-unmoved.
- **Did not touch `tmp/br2watch/measure/census.json`** — dirty, another workstream's, under QA review.
  Left exactly as found, for the fourth time.

---

## 10. PUSH

Charter § 5 push posture LIVE (*"push as you go"*). Instruments per landing:
`git status --porcelain -- <paths>` before, `git show --stat HEAD` after, `git -C <path>` on every
cross-repo operation. Collab `64dfeb4d`, `c663ff67` pushed; godot `27baafc` pushed.
