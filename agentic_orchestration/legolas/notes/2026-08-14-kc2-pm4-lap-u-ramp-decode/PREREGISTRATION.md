# KC2-PM4 · LAP U — THE RAMP DECODE · PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-52 part 5`, ledger row `L-43`. **Date:** 2026-08-14.
**Discipline:** GL-6 (full 64-hex on every input and output) · GL-12 (DECODE-NEVER-ESTIMATE;
UNREACHED honest per limb) · NOTE-9 (no repair outside my own seam) · FIT law (self-caught defects
flagged, repaired in-lap with declared scope, and reported).

**This file is written and sha256-hashed BEFORE any instrument of this lap runs.** Its hash and the
UTC instant of hashing are recorded in `pm4u_digests.json`. Every verdict rule below is fixed at
that instant.

---

## § 0 — RECONNAISSANCE PRECEDING THE HASH (declared in full, per CL-10)

I read the following **before** writing this file. Nothing below is a result; all of it is
orientation, and I name it so the reader can discount it.

1. The run charter rows `L-37`, `L-42`, `L-43`, `R-PM4-51`, `R-PM4-52` (verbatim).
2. gamora's I-20 landing note in full — in particular § 2 (`D-I20-1`), § 5.1 `S-2`, § 11 digests.
3. My own Lap S findings §§ 3.1–3.4, 6, 8, 9; my own Lap T findings §§ 5.1–5.3, 6, and the
   UNREACHED/UNDECIDED tables.
4. My own instrument sources `pm4s_video_2026_08_14.py`, `pm4t_map_v2_2026_08_14.py`,
   `pm4t_geom_recompute_2026_08_14.py` — read to recover exact carried constants and the exact
   record layout the v2 reader assumes.
5. **Four facts established by shell reconnaissance before the hash, each of which shapes a
   hypothesis below and is therefore declared rather than presented as a finding:**
   - `survivalworld_a.map` is 4,836,448 bytes; its head carries the group name
     `PatrolPoint_Attack` at offset 0x28.
   - The `.map` references exactly **7** `Maps/Region_Survival_A0NN.lvl` names, at offsets
     0x0f20–0x1196, each preceded by a u32 length and followed by ~48 bytes of numeric metadata
     whose first two u32s (0x1c136b, 0x106d34) are of file-offset/size magnitude. **No standalone
     `.lvl` file exists anywhere in the vendor tree**; `Maps.arc` contains only `.map` entries.
     Limb (c) is therefore an *embedded-region* problem, not a missing-file problem.
   - The last `records/….dbr` string in `survivalworld_a.map` ends at 0x46959e; the file ends at
     0x49cc60.
   - `capstone 5.0.7` and `numpy 2.4.6` are available; `Game.dll` / `Engine.dll` are unprotected
     (Lap S), `Grim Dawn.exe` carries a Steam-DRM `.bind` section (`UNREACHED-S1`).
6. **I have NOT looked at:** any sim-side artifact of I-20 beyond the landing note's prose; any
   arrival-direction, entry-timestamp, player-motion, or follow statistic from the video; any
   disassembly of the Pursue path; any byte of an embedded region blob; any re-parse of the `.map`
   under the alternative record layout of § 5. **Every number this lap reports is unobserved at
   the instant of this hash.**

---

## § 1 — INPUTS, PINNED

Every input is re-hashed at instrument start and the run **HALTS** on any mismatch (GL-6). The
values below are the digests I expect; they are copied from the emitting laps' own digest files and
from gamora's § 11, and are themselves subject to the HALT check.

| input | expected sha256 |
|---|---|
| `lapR/method/plates60_lapH2.npy` | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` |
| `lapH2/method/camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` |
| `lapS/pm4s_video.json` (continuity pin) | `c968041fc1a81f1b6f141e3a0bf0b754d367c8290c368679208312aa8865be07` |
| `lapS/pm4s_findings.md` | `5251e0eaccbfb9097dc6a28fdee76e5a8e6965c034c1a52a4e5fb4af8d538c87` |
| `lapT/pm4t_map_placements_v2.csv` | `96306ed09a08ebd8aad6b5b65f953960cd47ecf78930ce490b013e37aac08820` |
| `lapT/pm4t_geometry_corrected.csv` | `549842a11bf23a2b9733edd8362383b416dfec886dbff44aec92d34148a552fe` |
| `lapT/pm4t_findings.md` | `de80588a3ae922c6ee7b3ccd3ec2bc901da69fba99efc35ac3f52ef1625b2b4b` |
| `vendor/…/survivalmode{1,2,3}/resources/Maps.arc` | re-hashed, compared to Lap S/T `pm4s/pm4t_digests.json` |
| `vendor/grim-dawn/Game.dll`, `Engine.dll` | `4876d6bd…ab02`, `7141b51a…c87c` |

**Carried constants, each with its emitting lap named (NOTE-9), used unchanged and never
re-derived:** `K_GROUND = 0.537` (OBS-H2-8) · `PLAYER_PLATE_ANCHOR = (960.0, 429.0)`,
`PLAYER_GATE = (50.0, 16.0)` (Lap R) · `FIGHT_T0/T1 = 683.0 / 864.0 s` · `WAVE_START` map for waves
151–160 (Lap S) · px→m bracket `[119.0, 125.0]` (`R-PM4-43 part 2`, `U-S-5`; **both edges always,
never a midpoint**) · tracker PRIMARY cell `G_MAX = 60, N_MIN = 6, H_GAP = 6` (Lap S) · decoded
march-speed bracket `3.055412 – 3.209466 m/s` (Lap T, `INFERRED-WITH-EVIDENCE`, `UNREACHED-T1`).

---

## § 2 — BOUND DIRECTIONS AND KNOWN CENSORING (fixed before any measurement)

These are stated first because two of them **kill** discriminators I would otherwise want to run,
and I would rather kill them here than be tempted by them later.

* **B-1.** A nameplate proves a living body; its absence proves nothing. All counts are **LOWER
  bounds**. All *entry* counts are lower bounds on true entries.
* **B-2.** The frustum right-censors at ~11.6 m (`V-B1`, MEASURED). An "entry" in this lap means
  **entry into the observed ~11.6 m window**, never a spawn.
* **B-3. ⚑ THE WORLD-CLUSTERING DISCRIMINATOR IS VACUOUS AND I REFUSE IT IN ADVANCE.** One might
  test targeting by asking whether entry positions, mapped to the world frame, cluster at fixed
  ring nodes or translate with the player. **They translate with the player BY CONSTRUCTION**: the
  camera is player-locked, so every observable entry is within the frustum of the player's
  contemporaneous position. Any regression of entry world-position on player world-position must
  return slope ≈ 1 whatever the game does. **This test is pre-emptively rejected; it will not be
  run and no verdict may rest on it.**
* **B-4.** The player's world *trajectory* is INTEGRATED from per-frame phase correlation and
  accumulates drift (`D-S-1`); the player's world *velocity* is the per-frame translation itself
  and is **not** integrated. **Every primary statistic of limb (a) is built from velocities and
  from player-relative offsets, both drift-free.** Any statistic that needs the integrated
  trajectory is graded **INDICATIVE** and labelled as such in the artifact.
* **B-5.** The sign convention of the camera-translation array is **not** established by any prior
  lap (Lap S ran both and took the conservative one). **Sign-dependent statistics are reported
  under BOTH conventions and a verdict may only be drawn if it holds under BOTH.**
* **B-6.** The greedy tracker can hand an identity from a dying body to a nearby new one. Any
  statistic that follows a body over time carries an explicit anti-swap guard (§ 3.1) and the
  guard's rejection count is published.

---

## § 3 — LIMB (a): VIDEO ARRIVAL DECOMPOSITION (primary limb)

**Instrument:** `pm4u_video_2026_08_14.py`. **Inputs:** the two `.npy` arrays + the Lap S
continuity pin. **No video decode is required** — the plate census and camera translation already
exist as banked arrays.

### 3.0 Continuity pin (D-I20-5's lesson, adopted)

**`P-U-0`.** My per-wave living-plate ramp, recomputed from the arrays, must reproduce **Lap S's
`pm4s_video.json → arrival`** — the **artifact**, field by field, not the sentence about it — with
zero difference on `peak_plates`, `t_to_50pct_peak_s`, `t_to_90pct_peak_s` for all ten waves
151–160. **Any difference HALTS the limb.** F-10's medians (3.27 s / 4.97 s) are recomputed from the
reproduced fields, never quoted.

### 3.1 The primary discriminator — **the FOLLOW test** (`V-a1`)

**Why this one.** It is the only test I can construct that is simultaneously (i) sign-free,
(ii) drift-free, and (iii) not vacuous under B-3.

**Construction.** For each PRIMARY track, take every maximal contiguous window in which the
monster's player-relative ground radius satisfies `|o(t)| ≤ R_hold`. Over that window compute the
player's **NET displacement magnitude** `|Δp|` as the magnitude of the vector sum of the per-frame
camera translations (a magnitude, hence **invariant to the sign convention** of B-5). Then:

> a monster held within `R_hold` of the player at both ends of a window in which the player's net
> displacement was `|Δp|` **must itself have moved at least `|Δp| − 2·R_hold`** in the world frame.

This is a triangle inequality, not a model. A world-static target cannot satisfy it.

**Guards, all pre-registered, all with published rejection counts:**
* **G-1 (dash guard).** Reject any window containing a per-frame player displacement implying
  > 12.0 m/s. Rationale: the MEASURED dash layer (`D-I20-6`: 15.687–15.995 m in one step) would
  otherwise let a tracker artifact masquerade as a 16 m/s monster.
* **G-2 (swap guard).** Reject any window whose implied monster world speed
  `(|Δp| − 2·R_hold)/Δt` exceeds **8.0 m/s** (≈ 2.5× the decoded march bracket). A body that would
  have to outrun the decode is a tracker identity swap, not evidence.
* **G-3 (duration floor).** Reject windows shorter than **1.0 s**.

**PRIMARY cell:** `R_hold = 3.0 m`, proven-displacement threshold `D_min = 3.0 m` (i.e. `|Δp| ≥ 9.0
m`). Reported at **both** px→m edges. **Sweep published:** `R_hold ∈ {2.0, 3.0, 4.0} m` ×
`D_min ∈ {1.0, 2.0, 3.0, 5.0} m`.

**VERDICT RULE `V-a1` — deliberately conservative against my own lean.** My lean, stated so it can
be discounted: I expect the game to target the PLAYER, because that is the hypothesis that would
explain the density gap. Therefore:

| result at the PRIMARY cell, at **both** bracket edges | verdict |
|---|---|
| **≥ 25** surviving tracks with proven monster displacement ≥ `D_min` | **PLAYER-TARGETED — MEASURED** |
| **5 – 24** surviving tracks | **PLAYER-TARGETED — INDICATIVE** (population too small to be a law) |
| **1 – 4** surviving tracks | **NOT SUPPORTED**; reported as anecdote with n |
| **0** surviving tracks | **NOT SUPPORTED**; the limb reports the negative |

If the verdict differs between the two bracket edges, the verdict is the **weaker** of the two.

### 3.2 Corroborating discriminator — the **pursuit cosine** (`V-a2`, secondary)

Monster world velocity `vm = do/dt + vp`; bearing to the player from the monster is `−ô`. Report
`cos = ⟨v̂m, −ô⟩` pooled and per wave, **under both sign conventions of B-5**, restricted to frames
with `|vm|` in a plausible locomotion band. Also report the **frozen-target contrast**: the same
cosine measured against the bearing to the player's position at the track's birth. **`V-a2` may
support but may NEVER establish the § 3.1 verdict**; it is sign-dependent and therefore demoted by
construction. Verdict language permitted: `PURSUIT-CONSISTENT` (median cos > 0 under both
conventions) / `AMBIGUOUS` / `PURSUIT-INCONSISTENT`.

### 3.3 Arrival directions (`V-a3`)

Bearing of each entry (track birth) in the player-relative ground frame. Per wave and pooled:
circular mean, **mean resultant length R**, 12-sector histogram, and a Rayleigh statistic.

* `R < 0.20` ⇒ **OMNIDIRECTIONAL** (entries arrive from all sides — consistent with convergence on
  the player or with the player standing inside a ring).
* `R ≥ 0.40` ⇒ **DIRECTIONAL** (entries arrive from a preferred quarter — consistent with fixed
  doors/packs).
* between ⇒ **WEAKLY DIRECTIONAL**, reported with the number and no adjective beyond it.

### 3.4 The player's own motion (`V-a4`)

Per wave: path length, net displacement, mean and p95 speed, time-moving fraction, and the angle
between the player's net displacement direction and the wave's circular-mean entry bearing.
**Sign-dependent quantities reported under both conventions;** path length and net-displacement
*magnitude* are sign-free and carry the verdict. Question answered: *does Matt close distance
toward packs, and how far does he displace per wave?* Reported as numbers with the drift caveat
(B-4) attached to any statistic that touches the integrated path.

### 3.5 The deliverable the sim will be graded against (`V-a5`)

Emitted **regardless of every verdict above**, as `pm4u_arrivals.csv` + `pm4u_arrival_stats.json`:

* per-wave entry timestamps (seconds since that wave's increment), one row per entry;
* per-wave entry count, entry rate (entries/s over the wave span and over the first 6 s);
* **inter-entry interval distribution**: n, min, p25, median, p75, p90, max, per wave and pooled;
* **burst/density**: maximum entries in a sliding 1.0 s and 2.0 s window;
* per-entry birth radius (gpx and both m edges) and bearing;
* the standing caveat string **"entry = entry into the observed ~11.6 m window; LOWER bound (B-1,
  B-2)"** written into every row's `basis` column.

**No sim number is consulted anywhere in limb (a).** The comparator is emitted; the comparison is
I-21's.

---

## § 4 — LIMB (b): PURSUE-TRIGGER DECODE

**Instrument:** `pm4u_pursue_2026_08_14.py` (capstone, `Game.dll`/`Engine.dll`, read-only) +
`.arz` field census reusing the Lap T reader.

**Routes to be attempted, in this order, each reported pass or fail:**
1. **Export census** — every exported symbol whose name contains `Pursue`, `Aggro`, `Sight`,
   `Perceiv`, `Detect`, `Notice`, `Threat`, `Target`, `SetState`, `StateMachine` in either module.
2. **`ControllerMonsterStatePursue::OnBegin` (`0xff1d0`)** disassembled; its callees named; any
   float/immediate compared against a radius-shaped constant recorded with its address.
3. **The transition** — cross-references to whatever sets the monster state; the `"Pursue"` /
   `"Patrol"` / `"Return"` string literals and their referencing code.
4. **`UNREACHED-T5`** — the *writers* of `this+0x3dc` (`GetRadius`) and `this+0x3e0`
   (`ShouldRunTo`): find the constructor/loader that stores to those offsets and read the immediate
   it stores. This is the route Lap T named and did not walk.
5. **Record route** — census the `.arz` corpus for aggro/sight/perception-radius-family fields on
   monster, controller and proxy records; report field name, value distribution, and whether the
   tier-16 roster carries them.

**VERDICT RULE `V-b1`:**
* **DECODED** — a named code path with an address, whose condition I can read, that changes the
  monster's state to Pursue, *plus* the source of its radius. Nothing less earns the word.
* **PARTIAL** — the radius source is found but the transition is not, or vice versa. Reported with
  exactly what is and is not read.
* **UNREACHED** — neither. **The route that defeated it is named**, and no radius value is
  estimated, inferred from a sibling, or borrowed from another ARPG. GL-12 is absolute here: I
  would rather hand I-21 nothing than hand it a plausible number.

**VERDICT RULE `V-b2` (`UNREACHED-T5`):** same three grades applied to `GetRadius`/`ShouldRunTo`
**values**. A default read from an instruction immediate counts as DECODED **only if** I can show
the store targets `this+0x3dc` / `this+0x3e0`; a constant found near the accessor does not count.

---

## § 5 — LIMB (c): THE `.lvl` ATTEMPT (`UNREACHED-S8`)

**Instrument:** `pm4u_lvl_2026_08_14.py`, read-only over `Maps.arc` members.

Given § 0.5's reconnaissance, the region data is **embedded in the `.map`**, not shipped as a
separate file. The attempt is therefore: parse the 7-entry region table at 0x0f20…, interpret the
u32 pair after each name as (offset, size) or (size, size), and test the interpretation by whether
the implied blobs tile the file without overlap and terminate at the file end.

**VERDICT RULE `V-c1`:**
* **DECODED** — region blobs located AND a structure inside one identified well enough to name
  what it holds (terrain height, pathing/blocker grid, or neither), with the acceptance test that
  produced the identification stated as a constraint the reader enforces.
* **PARTIAL** — blobs located and bounded but contents not identified.
* **UNREACHED** — the table does not resolve. **The failure mode is documented** (compression,
  encryption, a container I cannot bound) and the limb reports the negative. This is an explicitly
  **acceptable** landing per the commission.

**VERDICT RULE `V-c2`:** patrol-point `radius` / `shouldRunTo` **values** recovered from region or
per-entity property data ⇒ closes `UNREACHED-T5` by the data route. Same three grades. **A value
found here must agree with limb (b)'s binary route if both land, and any disagreement is published
as a contradiction, not averaged.**

**Standing refusal:** if the arena wall/collision geometry does not decode, I will **not** offer a
bounding box from entity extents as a substitute. `D-PDEF-2` stays open rather than be closed with
a proxy. (Lap S's `D-S-1` is the precedent: an inflated hull is not a boundary.)

---

## § 6 — LIMB (d): `D-I20-1` REPAIR — MY OWN SEAM

The defect: `pm4t_map_placements_v2.csv`'s `dbr` label column is displaced by one record on
GUID-bearing (72-byte) placements. gamora named two candidate causes and verified neither
(correctly — NOTE-9 forbade her from repairing my artifact).

### 6.1 The two hypotheses, and what each predicts

**`H-d-A` — INDEX-FIRST LAYOUT.** The record is
`[u32 string_index][9×f32 rotation][3×f32 position][u32 has_guid][16 B GUID if has_guid]`, and the
array begins at `arr_off + 4`, **not** `arr_off + 8`. The v2 reader started 4 bytes late, so every
record's rotation/position/GUID is correct but the u32 it reads as *this* record's string index is
in fact the **next** record's index. Displacement is therefore **uniform across all records**, not
special to GUID rows; gamora observed it on the patrol set because that is where she looked.

*Predictions, all falsifiable:*
- **d-A1.** The u32 at `arr_off + 4` — which Lap T's own comment describes as "one further u32
  (observed 0)" — **is record 0's string index**, and is a valid index on all 20 maps.
- **d-A2.** Repair is `true_label[i] = read_label[i−1]`, `true_label[0] = table[u32 @ arr_off+4]`.
- **d-A3.** After repair, **every** row labelled `patrolpoint_01.dbr` is GUID-bearing, its GUID is
  present in the head-section `PatrolPoint_Attack` group, and the count equals `head_count` — on
  **20 of 20** arenas.
- **d-A4.** Positions, GUIDs and record sizes are **byte-identical** to v2. Only labels move.
- **d-A5.** No `playerspawnpoint.dbr` label survives inside the patrol group.
- **d-A6.** The tier-16 **spawn-point** label set also moves. This is a **consequence I must
  report, not suppress**, because Lap T's F-3/F-4/F-5 and the beacon geometry all take their
  *spawn* set from the labelled rows.

**`H-d-B` — PAIRED CONTROLLER/ANCHOR RECORDS.** The level format authors each `patrolpoint_01`
controller as a 56-byte record immediately followed by a distinct GUID-bearing anchor record; the
labels are already correct and nothing should be shifted.

*Prediction:* under `H-d-B`, applying the `H-d-A` repair **breaks** the spawn-point set and leaves
patrol rows non-GUID.

### 6.2 Verdict rules

| test | rule |
|---|---|
| **`V-d1`** | Re-parse under `H-d-A` must reach **exactly `declared` records** on at least the **18 of 20** arenas v2 reached, with the same orthonormality gate, and must not reduce that count. |
| **`V-d2`** | Positions / GUIDs / sizes **identical to v2 on every row** (`H-d-A4`). Any positional change falsifies `H-d-A` outright. |
| **`V-d3`** | `H-d-A3` holds on **20 of 20** arenas. **This is the decisive test.** ≤ 18 of 20 ⇒ `H-d-A` **REJECTED**, no v3 is emitted, and the defect is reported as **UNREACHED-with-cause-narrowed**. |
| **`V-d4`** | The v3 patrol-labelled point set must be **set-identical** to the head-group GUID set — which gamora measured ≡ the sim's 11 nodes at **5.4e-5 m**. Set identity therefore verifies v3 against `geometry_agreement_v2` **transitively and exactly**, without my consuming a sim artifact. |
| **`V-d5`** | F-4 recomputed **three ways** and all three published: (i) v3 patrol × **v2** spawn labels — must reproduce **16.7992** (gamora's GUID-set figure, and Lap T's published 16.80); (ii) v3 patrol × **v3** spawn labels — the honest post-repair figure; (iii) v2 patrol × v2 spawn — must reproduce gamora's **16.7308**. **If (ii) ≠ (i) the difference is a NEW correction to my own Lap T headline and it is reported as one, in the § 0 headline table, not buried.** |

**Emission:** `pm4u_map_placements_v3.csv` — a **NEW artifact**. Lap T's v2 is **not modified,
not deleted, not moved**; the ledger amends, the record stands (the same rule Lap T applied to Lap
S). v3 carries a `label_source` column naming the layout it was parsed under and a `v2_dbr` column
carrying the superseded label, so the displacement is auditable per row rather than asserted.

**If `H-d-A` is rejected:** I emit **no v3**, publish the falsification, and hand `D-I20-1` back
open with the cause narrowed. **A repair I cannot verify is not a repair.**

---

## § 7 — WHAT I WILL REPORT AS UNREACHED WITHOUT APOLOGY

Named now so that a later "we got most of it" cannot be assembled after the fact:

* the Pursue transition, if the state table stays unexported (`UNREACHED-T3`'s cause);
* `GetRadius`/`ShouldRunTo` values, if no store to `this+0x3dc`/`0x3e0` is readable;
* arena walls, if the region blobs do not resolve — and `D-PDEF-2` then **stays open** (§ 5);
* which arena Matt played (`UNREACHED-S3`) — unchanged, and every world-asset number in this lap
  remains a distribution over 20 arenas;
* whether an entry is a genuine new body or a plate re-appearance (`UNREACHED-S4`) — unchanged and
  **load-bearing for limb (a)**: the entry counts of § 3.5 are contaminated upward by re-appearance
  and downward by occlusion, and the artifact says so in every row.

## § 8 — PRE-REGISTERED FALSIFIERS AGAINST MY OWN LEAN

1. If `V-a1` returns **0–4** tracks, I report **"the referent's arrivals do not demonstrably follow
   the player"** in the headline table, in those words, and the conductor's TARGETING suspicion
   goes back to him unsupported by me.
2. If `V-a3` returns **DIRECTIONAL**, that is evidence *for* fixed doors/packs and *against* my
   lean, and it is reported at full size in § 0 rather than as a caveat in a later section.
3. If `V-d3` fails, no v3 exists and I say so first, before anything I did land.
4. If limbs (b) and (c) both return UNREACHED, the lap's headline is that **one** limb landed. I
   will not promote limb (d) — a repair of my own defect — into the lap's headline finding.

---

*Pre-registered by legolas, 2026-08-14, before any instrument of Lap U executed.*
