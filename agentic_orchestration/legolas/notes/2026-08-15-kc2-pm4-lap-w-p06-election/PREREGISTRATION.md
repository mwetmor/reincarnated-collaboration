# RUN KC2-PM4 · LAP W — THE p06 ELECTION READ (the `R-V-1` video route) · PREREGISTRATION

**Agent** legolas (UNKNOWN-RESEARCHER) · **Conductor** gandalf (RUN-CONDUCTOR)
**Fired under** `R-PM4-58 part 1` (Matt 2026-08-15, Q-a verbatim: *"I don't remember"*)
**Date** 2026-08-15 · **Discipline** GL-12 decode-never-estimate · full-64-hex digests (`R-PM4-55 part 2`)
**This file commits ALONE, FIRST, in its own commit** (`L-46` git-attested-priority discipline; second use).

> **AT THE MOMENT THIS FILE IS COMMITTED, ZERO FRAMES OF THE REFERENT VIDEO HAVE BEEN DECODED,
> EXTRACTED, OR VIEWED IN THIS LAP.** Everything below rests on (i) container metadata read via
> `ffprobe` (duration / frame count / geometry — no pixel decoded), (ii) prior-lap legolas notes,
> (iii) records-side reads of pinned game data and pinned prior-lap CSV/JSON artefacts.

---

## § 0 — THE QUESTION, STATED SO IT CAN FAIL

`bonusSpawnStatus` gates spawn point 6 (`p06`) in the Crucible wave loop. Lap V decoded it to a
**player election made at the start of the run** (`pm4v_findings.md` § 1.2), worth **+25.000
expected bodies** across waves 150–160 (§ 1.5), declared on 8 of 10 band waves **including wave
160** (§ 1.4). No record and no binary can say what Matt elected. Matt does not remember.

**Lap W asks exactly one question:** *in the recorded fight, was the p06 election ON or OFF?*

**The permitted answers are ON, OFF, and UNREACHED.** UNREACHED is not a failure of the lap; it is
the honest landing when no pre-registered discriminator fires, and `R-PM4-58 part 1` already states
its consequence (I-22 folds both limbs as arms and the election stays a fixture bracket).

---

## § 1 — THE REFERENT, AND WHAT IS KNOWN OF IT BEFORE ANY FRAME IS GRADED

| item | value | basis |
|---|---|---|
| referent | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | Lap H-2 README; Lap N § A.2 |
| container | 1920×1080, h264, **60/1 fps**, **1034.100 s**, **62 046 frames** | `ffprobe` this lap (metadata only) |
| **fought band 151–160 occupies** | **683.0 – 866.0 s** | Lap H-2 (in-frame bracket; 339 tracks, 10 waves) |
| FCT (combat text) present | 690–800 s and 830–860 s | Lap N § A.2 pre-scan |
| **pre-band span available** | **t ∈ [0, 683) s ≈ 11 min 23 s — contents UNKNOWN to this lap** | arithmetic on the two rows above |
| camera | rigidly player-locked; screen coords ARE player-relative; **player's absolute arena position is NOT known** | Lap H-2 "the enabling find" |
| nameplate primitive proven | red 3-scanline bar + white `(cur/max)` string; **monster NAME strings were never part of any prior instrument** | Lap H-2 instrument section |
| OCR instrument proven | Apple Vision `VNRecognizeTextRequest`, `.accurate`, language correction OFF (`ocr.swift`) | Lap N § A.2 |

**⚑ The pre-band span is the reason discriminator D-A is registered first and the reason this lap
is worth running at all.** Whether it contains the Crucible run-start sequence is *unknown at
preregistration time* and is the first thing the instrument will determine — by a scan whose cadence
and extent are fixed below, before it is run.

---

## § 2 — RECORDS-SIDE FINDS MADE BEFORE PREREGISTRATION (they shape D-B; they are not grades)

Two reads were performed against pinned records artefacts *before* this file was written. Both are
declared here so that nothing in D-B is a post-hoc construction.

**W-R1 — the election leaves a WORLD-VISIBLE MARK.** Lap V captured the `bonusChest` setter body
verbatim (`pm4v_bonusspawn.json`). On activation it does more than set a flag:

```lua
if Server && not bonusChest then
    LuaGlobalEvent("bonusChestTokenGlobalMP")
    bonusChest = true
    local spawn = Entity.Get(spawnPoint06FxId)
    local coords = spawn:GetCoords()
    local fx = Entity.Create("records/fx/ambient/fx_eldritchrift_medium01.dbr")
    if (fx != nil) then fx:NetworkEnable(); fx:SetCoords(coords) end
end
```

**An eldritch-rift FX entity is created at the 6th spawn point's coordinates, and only then.**

**W-R2 — the static rift census, and the resulting 4-vs-5 signature.** Census of
`pm4u_map_placements_v3.csv` (pinned below): `records/fx/ambient/fx_eldritchrift_medium01.dbr`
appears **80 times** across the ten `survivalworld_[a–j].map` files = **8 rows per map**. Both that
file and `pm4u_geometry_v3.csv` carry an exact 2× row duplication (12 spawn rows per map resolve to
**6 unique** spawn points; 8 rift rows resolve to **4 unique** rifts). Distance test on
`survivalworld_a.map`, xz-plane:

| static rift (x,z) | nearest unique spawn point | distance |
|---|---|---|
| (112.4, 71.2) | sp idx 4 | **0.09 m** |
| (90.6, 32.6) | sp idx 0 | **0.15 m** |
| (46.7, 73.9) | sp idx 2 | **0.11 m** |
| (89.6, 96.6) | sp idx 3 | **0.22 m** |

**Four of the six unique spawn points carry a statically-placed rift; two — (73.0, 58.5) and
(102.1, 82.3) — carry none.** Therefore the arena's rift count at spawn points is **4 when the
election is OFF and 5 when it is ON**, and the 5th appears at a spawn point that has no static
placement. This is a *countable, records-derived, in-arena signature that contains no body count*.

**Stated as a limitation, before it is tested:** the mapping from geometry row index to Lua
`entity[1..6]` index is **NOT established** by any prior lap, so "which rift-less point is p06" is
open; and Lap H-2 established there is **no world→screen registration** (the camera gives
player-relative coordinates only). D-B is therefore registered with an explicit NOT-USABLE branch.

---

## § 3 — THE DISCRIMINATORS, PRE-REGISTERED

Registered in priority order. They are **independent**: D-A reads UI, D-B reads world VFX geometry,
D-C reads monster identity. Any one may fire alone. Nothing below may be substituted, widened,
weakened, or supplemented once frame grading begins.

### D-A — START-OF-RUN UI READ *(directness: DIRECT)*

The shipped text `tagTutorialTip64TextB` ("…any additional bonuses you activated **at the start**")
and `achS007Desc` ("…with the 6th Spawn Point active") both establish that the election is expressed
in a start-of-run interface. If the recording reaches back to it, the election is **read, not
inferred**.

**Instrument (cadence fixed now):**
1. Contact-sheet scan of `t ∈ [0, 690] s` at **1 frame / 5 s** (139 frames), each frame classified
   into `{menu-or-UI-panel, loading, arena-no-combat, arena-combat, other}`.
2. If any `menu-or-UI-panel` frame is found, **refine at 2 fps over ±20 s** around each such frame
   and read every panel with Vision OCR (`.accurate`, correction OFF) plus direct crop inspection.
3. If step 1 finds no panel, D-A returns **NOT-PRESENT** and the lap moves to D-B/D-C. **No
   additional scan budget may be spent on D-A after that** (anti-fishing).

**Decision rule.**
- **DIRECT-ON** — a start-of-run bonus/spawn-point control is legible at some `t < 683 s` in an
  ACTIVE state (checked / purchased / lit / "active" wording), and no later toggle-off is observed.
- **DIRECT-OFF** — the same control is legible in an INACTIVE state and no activation occurs before
  the band begins.
- **NOT-PRESENT / ILLEGIBLE** — otherwise. Not evidence either way.

**Expected failure modes.** Recording begins after the election. The election is a click-through
never held on screen. Panel text below OCR resolution at 1080p. The election may live in an NPC
dialogue or a pre-arena lobby that was not captured. A rift-creation *event* (W-R1) occurring in the
pre-band span would also count as DIRECT-ON, but only if the FX is seen to *appear* — a rift already
standing is D-B evidence, not D-A evidence.

### D-B — THE p06 RIFT MARKER *(directness: INDIRECT, records-anchored)*

Per W-R1/W-R2: ON ⇒ 5 rifts at spawn points, one of them at a statically rift-less point; OFF ⇒ 4.

**Instrument.**
1. Establish arena identity: match the fight footage's visible terrain/layout against the ten
   `survivalworld_*` spawn-geometry fingerprints (inter-spawn distance signature) **only if** a
   registration anchor exists. If arena identity cannot be established, D-B returns **NOT-USABLE**.
2. Scan for rift FX in the frame set already committed to under D-A step 1, plus a **1 frame / 2 s**
   sweep of the band `683–866 s` (92 frames), by colour/shape signature of the eldritch-rift VFX.
3. A rift is only counted if a raw crop is published for it.

**Decision rule.**
- **ON** — a rift is observed at a spawn point that carries no static placement, with the spawn
  point's identity established (not assumed).
- **OFF** — all six spawn points are observed across the fight and exactly the four static rifts are
  present.
- **NOT-USABLE** — arena identity, or the geometry-row → `entity[i]` index mapping, or world→screen
  registration cannot be established. **This is the expected outcome and is declared as such now**:
  Lap H-2 says the camera gives no absolute position, so D-B is registered as a long shot, honestly.

**Expected failure modes.** No world→screen registration (near-certain). Rift VFX confusable with
the arena's other aether/chthonic ambient VFX and with skill VFX. Occlusion by bodies and bloom.
Spawn points off-camera for the whole fight. Row-index → `entity[i]` mapping unproven.

### D-C — p06-DISTINCT ROSTER CENSUS *(directness: INDIRECT; the Lap N OCR class)*

Lap V's per-wave p06 pools (`pm4v_roster_arithmetic.csv`, pinned) are **hero/champion pools** on six
of the seven contributing waves:

| wave | p06 pool(s) | usable for D-C? |
|---|---|---|
| 152 | `poolsdevotion/devotion_heroes01…06` | yes |
| 153 | `poolshero/chthoniandreadguard_hero`, `poolsherogdx3/giant_hero` | yes |
| 155 | `poolsbounty/bounty_heroes01…03`, `poolsbountygdx1/bounty_heroes01…02` | yes |
| 156 | `poolsbasicgdx1/humanwendigo_t3` (basic trash, 7 bodies) | **no — excluded, not identity-distinct** |
| 157 | `poolsherogdx1/aetherialcolossus_hero` | yes |
| 158 | `poolsherogdx1/aetherialfleshshaper_hero`, `poolsherogdx3/dranghoul_hero` | yes |
| 160 | `poolsherogdx1/wendigocannibal_hero` | yes |

**Instrument.**
1. From the pinned `.arz` set, census the member entries and their **display names** for every pool
   declared at **every** spawn point on each band wave (not just p06).
2. Per wave `w`, form `S_w` = { display names reachable **only** through that wave's p06 pool }.
   Waves with `S_w = ∅` are dropped from D-C before any OCR is run.
3. Wave-boundary timestamps from Lap H-2 `OBS-H2-6` (wave-counter digit crop, ±0.25 s).
4. OCR monster nameplate text over each surviving wave's span at **1 frame / 1 s**, Vision
   `.accurate`, correction OFF; every candidate hit re-read in a raw crop before it counts.

**Decision rule.**
- **ON** — ≥1 name in `S_w` is read on its own wave at OCR confidence ≥ 0.90 **and** confirmed in a
  published raw crop.
- **OFF** — requires **ROBUST absence**: full coverage of every surviving declaring wave, **plus a
  POSITIVE CONTROL** — ≥1 display name drawn from a **non-p06** pool of the same wave, read by the
  same instrument at a comparable rate. **Without the positive control, absence is UNINFORMATIVE and
  must be reported as such, never as OFF.** (Lap H-2 measured plates as bar + `(cur/max)`; whether
  GD draws a persistent *name* string on hero plates is unproven and is exactly what the positive
  control tests.)
- **UNINFORMATIVE** — otherwise.

**Expected failure modes.** GD may draw monster names only on hover/target, in which case D-C dies at
the positive control (the honest outcome). Nameplate density fusing OCR lines — Lap N observed a
single OCR line fusing two overlapping strings. Confusion pairs among similar hero names
(`aetherialcolossus` / `aetherialfleshshaper` share a long prefix in their *record* names; display
names may or may not). Heroes killed or engaged off-camera. Hero display names may be shared across
pools, collapsing `S_w` to ∅ — checked in step 2 **before** OCR.

### D-D — INADMISSIBLE EVIDENCE (declared, so it cannot be smuggled in)

- **Aggregate body counts of any kind** — living bodies on screen, total nameplates, crowd size,
  arrival counts — are **NOT admissible**, alone or as a tie-breaker. The count is the quantity under
  test; grading the election by it would grade the answer by the target (`R-PM4-27 part 3`).
- **The referent's 19–36 crowd number is never an input to this lap.**
- **"ON grades better" is not evidence.** Lap V already named that temptation out loud and refused
  it; Lap W inherits the refusal.

---

## § 4 — THE GLOBAL DECISION RULE

1. **ON** iff D-A returns DIRECT-ON, **or** D-B returns ON, **or** D-C returns ON — with the
   supporting crop / frame numbers published.
2. **OFF** iff D-A returns DIRECT-OFF, **or** D-B returns OFF, **or** D-C returns OFF (robust
   absence *with* its positive control).
3. **If two admissible discriminators disagree, the verdict is UNREACHED** and the conflict is
   published in full. Conflicting evidence is never averaged, and the more convenient limb is never
   preferred.
4. **Otherwise: UNREACHED.** The honest landing. I-22 then folds both limbs as arms per
   `R-PM4-58 part 1`.
5. **Confidence is reported on every verdict** (DECISIVE / STRONG / MODERATE), together with the
   discriminator that carried it. A verdict at MODERATE-or-below must say plainly what would
   overturn it.
6. **Scan budgets in § 3 are caps.** If a budget is exhausted without a fire, the discriminator
   returns its null outcome. Extending a budget after seeing results is forbidden; if a budget is
   extended for a *pre-stated structural reason* (e.g. D-A step 1 finds a panel and step 2's ±20 s
   window clips it), the extension and its reason are recorded in the defect table.

---

## § 5 — HALT CONDITIONS

- **Fourth-mechanism find** (`R-PM4-56 part 4`, standing per `R-PM4-58 part 4`): any spawn/count
  mechanism surfacing in this lap that is unmodelled by the sim, the wave-pools CSV, and Lap V —
  **NAME IT, DO NOT DECODE IT**, and HALT the decode of it. `F-3M-1` (`ProxyAmbush` at p05) is Lap
  V-2's, not Lap W's; if it is encountered here it is named and left alone.
- **Input digest mismatch** on any pinned artefact at instrument start → HALT.
- **Any temptation to resolve the election by body count** → HALT and report UNREACHED.

---

## § 6 — INPUTS, PINNED AT PREREGISTRATION (HALT on mismatch at instrument start)

| input | sha256 (full 64) |
|---|---|
| referent video `eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` |
| `…/lap-u-ramp-decode/pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| `…/lap-u-ramp-decode/pm4u_map_placements_v3.csv` | `08308eb408f7f630c9bd310c4b5ba36ce1869bb4338caaa4028fd4c609f08a57` |
| `…/lap-v-roster-decode/pm4v_findings.md` | `5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895` |
| `…/lap-v-roster-decode/pm4v_bonusspawn.json` | `7c8d0b732d947c60c1a9344f3130482513195486f20ff49f6173ecd33fb84aa4` |
| `…/lap-v-roster-decode/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |

The three `pm4v_*` digests are **byte-identical to the values Lap V published in its own § 8.1**, so
Lap W decodes against the same artefacts the conductor verified at `L-48`.

Game-data inputs (`edition-III` `.arz`/`.arc` set, `Game.dll`, `Engine.dll`) are re-verified at
instrument start against **Lap V § 8.2's published digests**; any mismatch HALTs.

---

## § 7 — SCOPE FENCE

- **Read-only outside** `agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-w-p06-election/`
  (and `agentic_orchestration/research/scripts/` for this lap's instrument, per prior-lap practice).
- **Read-only on** `/Volumes/reincarnated/` and on all game data.
- This lap does **not** fold anything, does **not** touch the sim, and does **not** re-open Lap V's
  arithmetic. It answers one fixture question.
- Lap V's § 7.2 DO-NOTs remain binding and are carried forward into this lap's hand-off.
