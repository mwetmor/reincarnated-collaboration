# Research: the Crucible's centre spawn (p05). Does GD have it, and is it the ×3.17?

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (KC2 REFERENT-v2 track, KP-193) · **Date:** 2026-10-01
**Posture:** read-only. Pack, oracle and port untouched. The counterfactual in § 4 is an in-process wrap of gamora's own harness, NOT-A-GRADED-RUN.
**Labels:** **DATAMINED** = read out of GD's shipped bytes (DB / level / Lua). **FOOTAGE** = from the referent recordings. **SIM** = measured on our oracle. **INFERRED** = my reasoning, kept separate from the record.

---

## Summary

1. **GD has a centre spawn, and its data says so in every arena.** `spawnpoint05` is a `ProxyAmbush` point between **0.11 and 10.28 m** from the `PatrolPoint_Attack` centroid on **20 of 20** shipped arena maps. All three *Crucible of the Dead* candidates have one: `survivalworld_a` 10.10 m, `_b` 2.45 m, `_e` **0.11 m**. Tier 16 declares p05 bodies on 7 of 10 waves (151, 152, 153, 156, 157, 158 and 159). They arrive as a burst at wave start **+4.0 s**. *(DATAMINED)*
2. **p05 was never estimated from footage.** The pack's coordinate is a **datamine label error**. The 2026-08-08 `Maps.arc` reader started 4 bytes late, so every record carries the *next* record's label. The point shipped as "p05", at (−6.82, 2.17), r 7.16 m, is a **stalagmite** (`stalagmitetop_large02_nofade.dbr`). The real `spawnpoint05` in `sm1/survivalworld_a` is at **(−8.245, −5.824), r 10.10 m**, **8.13 m away**. The defect was found and repaired in Lap U (2026-08-14, `D-I20-1`), but the repair never reached the CSV the oracle vendors. The `ESTIMATED-FOOTAGE ±15deg` grade on the row is a **stale label**: star-lord flagged it on 2026-08-08 (IP-14) and it was never cleared. *(DATAMINED, plus provenance trace)*
3. **Oracle body share at p05: 15.1 %** of bodies over waves 151–160 (26.0 of 172.08, p06 OFF). The share of *landed damage* is **13.0–13.9 %**. *(DATAMINED counts; SIM landed share)*
4. **This is not the ×3.17.** Moving p05 to its true datamined position changes the ratio by **−0.6 %** (×3.243 → ×3.225, 20 salts). Moving it to the nearest candidate (r 0.11 m) changes it by −1.2 %. Pushing it out to the ring (r 33 m, *not* GD behaviour) **raises** lethality by +3.9 %. All three shifts are within salt noise. Even deleting every p05 body, which GD does not do, would cap the change at about −14 % (×3.24 → ≤ ×2.79). *(SIM; the bound is INFERRED)*

---

## Q1: Where are the Crucible's spawn locations in GD's data? Is there one near the centre?

### 1.1 The spawn law (DATAMINED)

- The Crucible's wave scripts read spawn positions from **level-resident entities** at runtime: `waveEvent.coords[id] = entity[id]:GetCoords()` (`survivalevent.lua:398`, Edition-I `Scripts.arc`). The `.dbr` spawn-point records carry **no coordinates**. Source: `legolas/notes/2026-08-08-kc2-citation-microprobe.md` § 4.1.
- The positions live in `survivalworld_a…j.map` inside `Maps.arc`. **Edition II and Edition IV ship no `.arc` files**; I re-enumerated `grim-dawn-edition-IV-20260929/` and it holds `.arz` files and two DLLs only. Level geometry therefore comes from the Edition-I and Edition-III `Maps.arc` decodes that are already on file.
- `records/scriptentities/spawnpoint05.dbr` is a `ScriptEntity` with `onAddToWorld = spawnPoint05OnAddToWorld`, which is the same shape as `spawnpoint02.dbr` (Edition IV, `sm_mod`).

### 1.2 Tier-16 p05 proxies: Edition IV against Edition II (DATAMINED) → `tier16_p05_proxies_edition_IV_vs_II.csv`

The seven declaring waves are **byte-identical across Editions II and IV**, and all resolve last-wins to `survivalmode3`. Every one is `Class = ProxyAmbush` with `alertArea 100`, a 4.0 s delay, group size 30, `spawnThreshold 15` and `placementExtents 8.0`. Pools by wave:

| wave | p05 pool |
|---|---|
| 151, 153 | living plant |
| 152 | aetherial corruption hero |
| 156 | aetherial corruption (fire / ice / lightning) |
| 157 | aetherial imp / corruption / wight heroes |
| 158 | wraith / hypporaven heroes |
| 159 | **boss**: Ekketzul or the Korvaak messenger |

Waves 154, 155 and 160 declare `{nil}` at spawn point 5 (`sm1/game/survival/tier16waves.lua`, Edition I).

Lap V-2 decoded what the ambush does: it is a **one-shot burst at +4.000 s with zero extra bodies**, and `alertArea` covers the whole arena, so the "ambush" never acts as a proximity gate (`legolas/notes/2026-08-15-kc2-pm4-lap-v2-proxyambush-decode/pm4v2_findings.md` F-2 to F-5). **Note on the brief:** tier-16 waves are declared in `survivalmode1`'s Lua and their proxies resolve to `survivalmode3`. `survivalmode2` carries only arenas `h` and `i`.

### 1.3 The true p05 position, all 20 maps (DATAMINED) → `p05_true_location_census_20_maps.csv`

| arena (both archives agree unless noted) | Crucible of the Dead candidate | true p05 r from patrol centroid | nearest spawn beacon |
|---|:-:|---:|---:|
| `survivalworld_a` (sm1 / sm3) | **yes** | **10.10 / 10.28 m** | 30.6 m |
| `survivalworld_b` | **yes** | **2.45 m** | 33.1 m |
| `survivalworld_e` | **yes** | **0.11 m** | 31.2 m |
| c, d, f, g, h, i, j | no | 9.57, 7.05, 8.20, 3.50, 3.50, 4.15, 4.53 m | 24.2–38.5 m |

- **The answer is yes.** Every arena has a near-centre p05, and every arena places its **5 spawn beacons** within 0.25–0.6 m of the **5 ring points** and never within 24 m of p05.
- The beacons are `spawnbeacon_0N.dbr`. Their `onAddToWorld` creates `records/creatures/traps/spawnbeacon.dbr`, which the Lua comments as *"Spawn Beacons accelerate monster movement in their spawn areas"* (`eventcontrol.lua:40–56`). *(DATAMINED)*
- **Arena identity:** the referent's HUD reads *Crucible of the Dead* (89 frames), which narrows the map to a, b or e. The exact file is UNREACHED behind the exe's DRM (`pm4aa_findings.md` § 2). *(FOOTAGE plus DATAMINED)*
- **Independent verification, this lap:** I re-parsed the Edition-I `.map` files with the index-first layout (`tools/reverify.py` → `p05_independent_reparse_edition_I.json`). Under the repaired labels, every GUID-bearing record is a `patrolpoint_01` (11/11 on each map checked). Under the old labels those same records read as an fx emitter, moss and stalagmites, which is physically impossible for a patrol control object. `spawnpoint06_fx` also sits 0.28 m from `spawnpoint06` only under the repaired labels. Lap U's repair holds.

## Q2: How was p05 "estimated from footage", and is it wrong?

**It was not estimated from footage, and it is wrong for a different reason.**

| step | what happened | source |
|---|---|---|
| L-10d / L-21 (≤ 2026-08-08) | Positions were DECLARED. galadriel's minimap survey gave **bearings only** at ±15°: s2 wave 151 two arrivals, wave 160 four. **No p05 bearing was ever measured.** star-lord IP-14: *"only 4 of 6 emitter bearings exist per sitting… `bearing_grade` must then not claim ESTIMATED-FOOTAGE ±15° for a bearing that was never estimated."* | `galadriel/notes/2026-08-08-eor-followup-extraction.md` §§ 1.6, 2 · `star-lord/notes/2026-08-08-kc2-baton-emitter-report.md:173–179` |
| 2026-08-08 microprobe | `Maps.arc` decode → `kc2_crucible_emitter_geometry.csv` (sha `ece0c345…`). Positions became CITED-PER-ARENA (L-46(b)). **The reader was 4 bytes late**, so each label belongs to the next record. | `legolas/notes/2026-08-08-kc2-citation-microprobe.md` § 4 |
| 2026-08-09 baton-v1 | Took the arena block from that CSV: `emitter_radii.p05_m = 7.159`. **The per-point `bearing_grade: ESTIMATED-FOOTAGE` was kept**, although the x/y are decoded and `heading_rad` is just *facing the centroid* (verified: `heading = atan2(−y, −x)` on all six points). | `kc2-baton-v1-E-s09-cp150-20260809_052836.json :: config.arena` |
| 2026-08-14 Lap U `D-I20-1` | Labels repaired (v3). Published: *"spawn → nearest beacon 10.47 → 0.61 m"*. **The repaired geometry was used only as a cross-check and never re-vendored.** | `legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_findings.md` § 4 |
| today | The oracle still loads `data/kc2/kc2_crucible_emitter_geometry.csv` (sha `ece0c345…`, `kc2/locomotion.py:50–51`). The pack's `arena_ref.geometry_sha256` is the same hash. | engine, read-only |

**What the error does to each point in `sm1/survivalworld_a`** (DATAMINED). The error only matters where the preceding record is unrelated: at the ring the preceding record is the beacon, so it is harmless.

| point | pack (= the object one record earlier) | true | Δ |
|---|---|---|---:|
| p01 (tier 16) | tier17spawnpoint01 | (−34.409, 9.575) | 0.04 m |
| p02 / p03 / p04 | spawnbeacon_02 / _05 / _03 | — | 0.30 / 0.32 / 0.46 m |
| **p05** | **stalagmite** (−6.821, 2.175) | **(−8.245, −5.824)**, r 10.10 m, bearing 215° | **8.13 m** |
| p06 | the *real p04* (31.215, 6.805) | (20.810, 17.967), r 27.49 m | **15.26 m**. p06 is OFF in the oracle, but if it is ever enabled it spawns on top of p04. |

The same defect propagated into `locomotion.py` docstrings that are now **false**:
- *"the player spawn is the level ENTRY… tens of metres outside"*. With repaired labels, `playerspawnpoint` sits **8.98 m** from the centroid in a, **1.12 m from the true p05**.
- *"three of the ten arenas carry no p05 (c/d/e)"*. **All ten have one.**

## Q3: What share of bodies does the oracle spawn at p05? → `p05_body_share_by_wave.csv`

Expected bodies (Lap V decode, p06 OFF), confirmed on the oracle:

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 | band |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p05 bodies | 4.5 | 3 | 4.5 | 0 | 0 | 7 | 3 | 3 | 1 (boss) | 0 | **26.0** |
| share of the wave's bodies | 17.0 % | 17.6 % | 19.1 % | 0 | 0 | **44.1 %** | 15.5 % | 9.1 % | 18.2 % | 0 | **15.1 %** |

- **SIM (PW-FOLDED, salts 0–4):** 130 of 865 spawned bodies were at p05 (15.0 %), all spawning at t = +4.0 s around (−6.8, 2.2).
- **p05's share of landed damage over waves 151–159:** **13.0 %** on salts 0–4 and 13.9 % on 0–19. Per wave it is lumpy: 157 → 44–53 % (the hero contingent), 159 → 37 % (the boss), 156 → only 1–3 % (the seven corruption bodies die fast).

## Q4: Lethality impact. Is p05 a contributor to the ×3.17?

**Method (SIM):** `tools/p05_counterfactual.py`. It runs gamora's `gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm("PW-FOLDED")`, which is the v1.8 seat cell and the oracle state behind ×3.17, with one in-process wrap: `CitedArenaGeometry.emitter_xy(5)` returns an override. Nothing on disk changes.

**Control reproduced exactly** on salts 0–4: 5,090.3 HP/s, ×3.17, terminals (156, 7.184 s) (152, 4.408 s) (155, 7.02 s) (152, 7.184 s) (152, 6.122 s).

| arm (salts 0–19) | p05 at | landed HP/s 151–159 | ×referent (1,605.6) | Δ | mean death wave | p05 landed share |
|---|---|---:|---:|---:|---:|---:|
| **PACK** (as shipped) | (−6.82, 2.18), r 7.16 m | 5,207.1 | **3.243** | — | 154.3 | 13.9 % |
| **TRUE-A** (the pack's own arena, corrected) | (−8.25, −5.82), r 10.10 m | 5,178.0 | 3.225 | −0.6 % | 154.35 | 16.5 % |
| TRUE-E (nearest candidate) | (0.11, −0.01), r 0.11 m | 5,142.3 | 3.203 | −1.2 % | 154.4 | 12.8 % |
| RING-33 (**not GD**: Matt's reading) | r 33 m, pack bearing | 5,409.8 | 3.369 | **+3.9 %** | 154.3 | 19.7 % |

**Salt noise** is the same arm moving between ×3.17 (salts 0–4) and ×3.24 (salts 0–19). Moving p05 also perturbs the body draws: 520 against 513 p05 bodies.

**Verdict (INFERRED from the SIM table):**
- **p05's position is not a material contributor.** Correcting it moves the ratio by under 1 %.
- **The intuition that "a centre spawn means more early pressure" runs the wrong way on this oracle.** Near-centre bodies walk into the player's kill disc and die. Bodies placed on the ring survive longer and deal more.
- **Upper bound, as arithmetic:** removing all p05 damage gives ×3.24 × (1 − 0.139) ≈ **×2.79**. That would not be a correction, because GD spawns these bodies.
- **p05 cannot close the ×3.** The commission's mechanism is refuted as a contributor to the gap. The position defect is real and is a fidelity item in its own right.

**Coincidence noted, and not a mechanism:** the five control deaths fall 4.4–7.2 s into the wave, just after the +4.0 s burst. But one death is on wave 155, which has no p05, and the TRUE-E arm keeps the same death timing with p05 at the centre. The timing is the wave's opening volley, not p05.

---

## Why Matt saw a "mouth" in the port and none in GD (INFERRED, with DATAMINED anchors)

- The port draws drax's diagnostic double ring and label at every spawn point, p05 included (KP-193).
- In GD, `spawnpoint05` has **no beacon and no trap entity** (§ 1.3), and ambush bodies are released through `Monster::EnableSpawnAnimation()` (Lap V-2 § 3.3). They emerge on the spot rather than coming out of a marked source.
- So GD does spawn 1–7 bodies near the centre 4 s into 7 of 10 waves, with nothing visible marking where they come from.
- Matt's memory of "no centre spawn" is most likely accurate about **what was visible**. It is contradicted by the data on **where bodies spawned**, given any of the three candidate arenas.
- The "invincibility timer" he reported fits a spawn animation, which GD also plays.

## Knowledge gaps not resolved

| # | gap | what would settle it |
|---|---|---|
| G-1 | **Which of a, b or e the referent used.** True p05 is at 10.1 / 2.45 / 0.11 m respectively. | A save-file level id or a landmark match. The binding is behind the exe's `.bind` DRM. Only bounds the ±1 % effect. |
| G-2 | **FOOTAGE confirmation that p05 bodies appeared near the referent player on waves 151–153 / 157.** The Lap U nameplate-entry series shows no distinguishable +4 s step on p05 waves compared with non-p05 waves. That instrument is noise-dominated (`D-U-3`, 11× re-appearance), so this is UNKNOWN, not a negative. | A frame-level look at t+4.0–5.0 s on those waves for emergence animations or new nameplates within about 11 m of the player. galadriel's s1 "+4 s second group" (waves 4/6/13) confirms the timing **in the other arena only**. |
| G-3 | Whether the ring-point 0.3–0.5 m offsets and the p06 duplication matter anywhere. | Re-vendoring the v3 geometry (§ Hand-off) removes the question. |
| G-4 | **The ×3.17 itself remains unexplained.** This was the seventh mechanism checked (C-10 through C-11d, then this). | KP-135 ruling stands: total-layer composition decode, plus an audit of the referent intake instrument. |

## Hand-off (factual; the recipients decide)

1. **gamora / star-lord:** `data/kc2/kc2_crucible_emitter_geometry.csv` (sha `ece0c345…`) carries the 2026-08-08 off-by-one labels.
   - The corrected positions are in `legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode/pm4u_map_placements_v3.csv`.
   - For `sm1/survivalworld_a`: p05 → (−8.245, −5.824), p06 → (20.810, 17.967), and p02–p04 / p01-tier16 shift by 0.04–0.46 m.
   - Expected lethality effect: about −0.6 % (§ 4). The fix is a fidelity correction, not a calibration lever.
2. **Pack grade:** `spawn_points[].bearing_grade = ESTIMATED-FOOTAGE ±15deg` is stale on all six rows. The coordinates are LEVEL-CITED and the headings are DERIVED (they face the centroid).
3. **Docstrings now false:** `kc2/locomotion.py` § CitedArenaGeometry ("player spawn tens of metres outside"; "c/d/e carry no p05").
4. **Port presentation (drax / Matt):** GD gives p05 no visible source. If the port is to read like GD, the p05 marker is the item to reconsider, not p05's existence.

## Source list (accessed 2026-10-01)

**Vendor**
- `~/Games/vendor/grim-dawn-edition-IV-20260929/` (8-archive `.arz` stack; `SurvivalMode3.arz` sha256 `d5e32852…`)
- `~/Games/vendor/grim-dawn-edition-II-20260724/` (`SurvivalMode3.arz` sha256 `b4aa2d78…`)
- Edition-I `.map` extracts: `legolas/scratch/2026-08-08-kc2-citation/maps/` (sha prefixes: sm1 a `2110cd42`, b `c7728cbd`, e `ce3bc0b2`, sm_mod a `f124a0b5`)
- Lua extracts: `legolas/scratch/2026-08-07-u8-tierwave/lua/`

**Prior findings**
- `legolas/notes/2026-08-08-kc2-citation-microprobe.md`
- `…/2026-08-14-kc2-pm4-lap-u-ramp-decode/` (`pm4u_findings.md`, `pm4u_map_placements_v3.csv`, `pm4u_arrivals.csv`)
- `…/2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv`
- `…/2026-08-15-kc2-pm4-lap-v2-proxyambush-decode/pm4v2_findings.md`
- `…/2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure/pm4aa_findings.md`
- `galadriel/notes/2026-08-08-eor-followup-extraction.md`
- `star-lord/notes/2026-08-08-kc2-baton-emitter-report.md`
- `gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` L-21
- `gandalf/notes/2026-09-20-kc2-play-run-charter.md` KP-110, KP-131, KP-135, KP-193

**Engine (read-only)**
- Pack: `src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/{arena,waves,provenance}.json`
- `src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json`
- `src/reincarnated/simulation/kc2/locomotion.py`
- `simulation/scripts/gamora_kc2_play_c11a_fold_pricing_2026_09_30.py`
- `simulation/output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json` (the control)

## Files in this directory

| file | what |
|---|---|
| `p05_true_location_census_20_maps.csv` | the true p05 on every map, with its old-label counterpart |
| `p05_independent_reparse_edition_I.json` | this lap's re-parse of a / b / e and sm_mod a |
| `tier16_p05_proxies_edition_IV_vs_II.csv` | the seven declaring proxies, both editions |
| `p05_body_share_by_wave.csv` | expected bodies per point and wave |
| `p05_position_counterfactual_PW-FOLDED_salts0-19.json` | the four arms, salts 0–19 and the 0–4 subset |
| `tools/` | `reverify.py`, `p05_counterfactual.py`, `arz_stack_edition_IV.py`; run from `reincarnated-engine/src` |
