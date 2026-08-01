# Research — Trace descriptor census: what the substrate knows and presentation throws away — 2026-08-01

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf
**Scope:** full `kitcal_g5` battery (4,073 traces) + current-generation battery (200 traces) + upstream `.arz` source records (5 DBRs + 10 FX-chain records)
**Access:** read-only. No writes outside this file.

---

## THE ANSWER, FIRST

**Yes, and the gap is larger than the nova.** Three findings, in descending order of what they buy:

1. **The blizzard is the biggest loss, not the nova.** The trace emits **one static circle, r = 8.0 m, one record per cast**. The source says: **24 ice orbs, in 4 volleys 2.0 s apart, falling from 20 m altitude at 24 m/s, over an 8.0 s active window, each with a 1.32 m hit radius, mesh `frostorb01.msh`, under a looping audio cue.** Every one of those 24 drops is *already individually identified in the trace* — inside the `attack_id` string (`…:blizzard:<cast>:<volley 0-3>:<drop 0-5>`, verified: volleys 0-3, drops 0-5) — but **no schema field declares it**, so no consumer can find it without string-parsing.

2. **Two of the three fields needed to fix the wave and the blizzard already exist in the schema and are null.** `projectile_velocity_ms` and `prong_count` are populated on `nova` and null on `wave` and `blizzard`. Populating them (wave: 11.4286 m/s front speed; blizzard: 24.0 m/s, 6 drops) costs two floats and one int per telegraph and buys the wave's *sweep* and the blizzard's *volley* — the two things that currently render as motionless shapes. **This is a fill, not a schema change.**

3. **The entity header's `range_m` is the AI fire range, not the geometric extent — 100 % of the time, on every telegraphing slot in both batteries.** Verified against source: header `range_m` equals `fire_range_m` on 3 of 3 boss AoE slots exactly (10.0 / 9.0 / 15.0). **Render from the event, never the header** is now evidenced, not assumed.

---

## §1 — Field-population census, current-generation battery

**Corpus split, and it matters.** The 4,073-file `kitcal_g5` tree is **pre-schema-growth**: `family`, `prong_count`, `t_launch_s`, `spoke_offset_rad`, `projectile_velocity_ms` are **0 % non-null across all 13,865 telegraphs**, and `rect` / `wave` / `blizzard` do not appear at all. The current-generation set is the 200 traces at `~/Games/reincarnated-godot/tmp/wr3acc/traces/` (schema `g5-replay-trace/v1`). All per-family figures below are from that set: 200 traces, 17,813 events, **1,556 telegraphs**.

### 1a. Telegraph fields by family — (a) populated

| Field | `nova` (470) | `wave` (516) | `blizzard` (570) |
|---|---|---|---|
| `shape` | `circle` | **`rect`** | `circle` |
| `radius_m` | **12.0** | — | **8.0** |
| `range_m` | — | **16.0** | — |
| `width_m` | — | **6.0** | — |
| `orientation_rad` | — | **[-3.118, 3.109]** | — |
| `half_angle_rad` | — | — | — |
| `spoke_offset_rad` | **[0.131, 6.277]** | — | — |
| `t_launch_s` | **= `fire_t_s`** | — | — |
| `projectile_velocity_ms` | **14.0** | — | — |
| `prong_count` | **16** | — | — |
| `wind_up_s` | **0.85** | **0.8519** | **0.8333** |
| `damage_amount` | [19.89, 56.63] | [74.18, 91.37] | [37.27, 45.93] |
| `origin_x_m` / `origin_y_m` | populated | populated | populated |

**One telegraph record per cast**, all three families (verified: `attack_id` has 3 segments, 1 record each). The blizzard's single record therefore represents 8.0 s and 24 projectiles.

**Answering the commission's specific probes, plainly:**
- **True cones:** none. `half_angle_rad` is **0 non-null out of 15,421 telegraph events across both batteries.** No family has ever telegraphed a cone. The schema supports it; nothing uses it.
- **Prong counts other than 16:** none. `prong_count` is 16 on 470/470 nova records, null everywhere else.
- **Travel:** only the nova. `projectile_velocity_ms` + `t_launch_s` are nova-only.
- **Chains / multi-stage:** none in the trace. The blizzard *is* multi-stage upstream (4 volleys) and the trace does not model it as such.
- **`melee` family:** declared in `VALID_FAMILIES`, **never emitted** (0 records). Boss melee produces `damage` events with `geometry:"point"` and no telegraph at all in the current battery.

### 1b. (b) Fields that exist and are ALWAYS null

Clean negatives. These are schema slots with zero occupancy across the whole current battery:

| Record | Field | Non-null |
|---|---|---|
| telegraph (all families) | `half_angle_rad` | 0 / 1,556 |
| damage (all geometries) | `expected` | 0 / 10,157 |
| damage | `expected_premit` | 0 / 10,157 |
| damage | `pct` | 0 / 10,157 |
| damage | `pct_premit` | 0 / 10,157 |
| damage | `pct_received` | 0 / 10,157 |
| header → entity | `element` | 0 / 800 |
| header → entity | `threat_tier` | 0 / 800 |
| header → entity → skill | `element` | 0 / 1,800 |
| header | `boss_focus_entity_id` | 0 / 200 |

`skills[].element` being 0 % populated is the notable one: **the damage events prove the engine knows the element** (`cold` / `physical` / `chaos`, 100 % populated on all 10,157 damage events), but the skill declaration that a renderer would read *at load time to pick a VFX palette* is empty on every row.

### 1c. Damage-event census — the join is broken for boss AoE

| `geometry` | n | `element` | `skill_idx` | `attack_id` |
|---|---|---|---|---|
| `cone` | 3,837 | chaos | 0 | **null** |
| `dot` | 3,726 | chaos | **-1** | **null** |
| `line` | 1,663 | chaos | 1 | **null** |
| `circle` | 426 | cold | **-1** | present (nova + blizzard) |
| `point` | 405 | physical | 0 | **null** |
| `rect` | 100 | cold | **-1** | present (wave) |

**`skill_idx = -1` on every boss AoE damage event.** The only route from a blizzard damage event back to skill 3 is parsing the `attack_id` string. And `attack_id` is **null on 9,631 of 10,157 damage events** — every player skill and every melee hit — so there is no universal join key between a damage event and the telegraph that caused it. A renderer cannot reliably answer "which impact belongs to which telegraph."

### 1d. The per-frame stream — richer than expected, and under-consumed

`tick.entities[]` is 100 % populated on 16 fields:

`entity_id, alive, x_m, y_m, **heading_rad**, hp, max_hp, **commit_state**, **commit_skill_idx**, movement_speed_ms, is_leashing, is_activated, energy, skill_cooldowns, **ailments**, ai_state`

- **`ailments`** — array of `{name, remaining_s, element}`. Observed: `wr3_icearmor` (7,200 frames), `bleed` (10,913), `action_lock` (989), `gd_total_speed_slow` (2,479), `gd_damage_debuff` (974). **This is a complete per-frame status-effect channel with countdowns and elements, and it is exactly what a buff/debuff VFX layer needs.** The boss's ice armour is visible here for 12 s at a time — I initially expected it to be absent and it is not.
- **`commit_state`** — 4-phase animation state machine: `idle` / `windup` / `strike` / `recovery`. **Boss-only, and only for skill 0.** `commit_skill_idx` takes values `{-1, 0}` only. So during a nova/wave/blizzard cast the boss reads `commit_state: "idle"` — **the signature casts have no animation state in the per-frame stream.** That is a real gap: the telegraph event says a cast is happening; the entity stream says the boss is idle.
- **`ai_state`** — `dormant / alert / engage / approach / windup / strike / recover`. Mob-only. `alert` fires 358 frames — a distinct pre-aggro state a renderer could stage.
- **`heading_rad`** — per-frame facing, 100 % populated, and the wave's `orientation_rad` is the only place facing currently matters visually.

### 1e. `g5_header` carries display names the base header does not

The base `header.entities[]` gives a renderer `boss&quest_slith_wightmirecave01_0` and nothing else. The `g5_header.g5.opposition_roster[]` carries, for the same entity:

| Field | Value |
|---|---|
| `label` | **"Primordian, the Forgotten One"** |
| `record` | `boss&quest/slith_wightmirecave01` (the DBR join key) |
| `tier` | **`boss`** / `elite` |
| `char_level` | 18 |
| `hp_grade` / `dmg_grade` | `M` / `M-BAND` |

Escorts: **"Deepmire Vanguard (escort)"**, **"Deepmire Evocator (escort)"**. Boss-vs-elite tiering and human-readable names exist in the trace **but in a sidecar record, not the entity list a renderer reads.**

---

## §2 — The disagreement audit

**Verdict: the header's `range_m` is never the geometric extent. Standing law confirmed.**

### Current battery (1,556 telegraphs, 3 slots)

| Slot | Skill name | Header `geometry` / `range_m` | Telegraph `shape` / extent | Shape | Extent |
|---|---|---|---|---|---|
| 1 | `primordian_frigidring_star_r5` | `circle` / **10.0** | `circle` / radius **12.0** | agree | **DISAGREE** |
| 2 | `primordian_wave_r5` | **`cone`** / **9.0** | **`rect`** / range **16.0**, width **6.0** | **DISAGREE** | **DISAGREE** |
| 3 | `chillbane_blizzard_r5` | `circle` / **15.0** | `circle` / radius **8.0** | agree | **DISAGREE** |

- **Shape agreement: 1,040 / 1,556 (66.8 %).** The wave's 516 records disagree on the geometry *class* — `cone` vs `rect`. A consumer trusting the header draws an unbounded wedge where the source has a bounded 3.0 → 6.0 m lane that stops at 16.0 m.
- **Extent agreement: 0 / 1,556 (0.0 %).**

### Old battery (13,865 telegraphs, 17 slots)

Shape agrees on all 17 slots (16 `point` melee slots, 1 `circle`). Extent: the 13,060 `point` telegraphs carry **no extent field at all** (dimensionless — not a disagreement, an absence); the 805 `primordian_frigidring_r4` records show header 10.0 vs telegraph radius 12.0, the **same disagreement, present since the older schema**.

### Why — and this is the load-bearing part

Cross-checked against the source parameter objects:

| Slot | Header `range_m` | Source field | Source value |
|---|---|---|---|
| nova | 10.0 | `NovaParams.fire_range_m` (creature `mediumRangeMax`) | **10.0** |
| wave | 9.0 | `WaveParams.fire_range_m` (`specialAttackRange` → `moderateRange`) | **9.0** |
| blizzard | 15.0 | `BlizzardParams.fire_range_m` (`'LongRange'` → `longRange`) | **15.0** |

**3 of 3 exact.** `header.range_m` is the **AI trigger distance** — how close the boss must be to cast — and has never been the visual extent. Two vocabularies collided in one field name. This is the same class of defect as the `range_m`/`radius_m` collision that cost R-WR2-19 a ruling.

**Proposed law:** *Telegraph events are the sole authority for danger-zone geometry. `header.entities[].skills[].range_m` is AI fire range and must not be rendered.* If it is to stay in the header it should be renamed `fire_range_m`.

---

## §3 — Upstream: what the source holds and the trace drops

The pinned corpus is at `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (4 `.arz` archives). All five skill/creature records read successfully via the existing adapter. **This is (c) — detail that exists upstream and is lost in translation. It is the largest of the three buckets.**

### 3a. Source record sizes vs what reaches the trace

| Skill | Source DBR fields | Params-object fields | Telegraph fields non-null |
|---|---|---|---|
| `primordian_frigidring` | **304** | 27 | **20** |
| `primordian_wave` | **281** | 21 | **13** |
| `chillbane_blizzard` | **726** | 21 | **11** |
| `primordian_icearmor` | **641** | 11 | **0** (never telegraphs) |
| `slith_wightmirecave01` (creature) | **964** | — | 6 header fields |

### 3b. The descriptive fields — never modelled, never in any params object

**These are the ones Matt is asking about.** Every value below is read verbatim from the `.arz` in this probe and appears **nowhere** in the engine's params objects or the trace.

| Source field | frigidring | wave | blizzard | icearmor |
|---|---|---|---|---|
| **`FileDescription`** | **"Freeze projectile ring"** | **"large cone wave with cold and poison dot"** | **"ice projectiles from air doing cold and slow"** | — |
| `templateName` | `skill_attackprojectilering.tpl` | `skill_attackwave.tpl` | `skill_buffattackradiusdrop.tpl` | `skill_buffselfduration.tpl` |
| **`cameraShakeAmplitude`** | **0.12** | **0.12** | **0.12** | — |
| **`cameraShakeDurationSecs`** | — | **1.0** | — | — |
| `skillSpecialAnimationName` | **`Roar`** | **`TailLashSunder`** | *(absent — no cast anim)* | **`BuffQuick`** |
| `skillProjectileName` | `icebolt_nova_fxprojectile.dbr` | — | `blizzard_projectilefx.dbr` | — |
| `fxPakName` | — | `tidalwavepoison_fxpak01.dbr` | — | — |
| `fxPakExtents` / `fxPakSpawnDistance` / `fxPakRandAngle` / `fxPakRandOffsetX` | — | **1.5 / 0.8 / 15.0° / 1.0** | — | — |
| `charFxPakSelfNames` | — | — | — | `icearmor_chfxpak01.dbr` |
| `ragDollDirection` / `Effect` / `Elevation` | **Push / TakeHit / Downward** | Push / TakeHit / None | — | — |
| Sounds | *(via projectile)* | `waveStartSound`, `waveLoopSound`, `skillHitSound` | `skillSwipeSound` (loop) | `skillActivatedSound` |
| `projectileDamageRange1/2/3Scale` | **50 / 100 / 140** | — | — | — |
| `charBuffFxType` | — | — | `None;Fire;Poison;` | — |

**`FileDescription` is a one-line human-authored intent string on every skill record.** "large cone wave with cold and poison dot" is the designer telling you what the ability *is*. Nothing in our pipeline reads it.

**`cameraShakeAmplitude 0.12` is present on all three offensive skills**, and the wave additionally carries a 1.0 s shake duration. That is free game-feel, in the source, unread.

### 3c. The FX chain — three levels deep, all readable

Following `skillProjectileName` → projectile record → `projectileFlightFX` / `projectileImpactFX` / `projectileWeaponTrail`:

**`icebolt_nova_fxprojectile.dbr`** (the nova's prong — 32 fields):

| Field | Value |
|---|---|
| `Class` | `ProjectileFireballLike` |
| **`mesh`** | **`fx/meshfx/frostorb01.msh`** |
| `scale` | 1.0 |
| `collisionShape` | `Sphere` |
| `actorRadius` | **0.10** (this is the hit-test operand R-WR3-21 adopted) |
| `maxTransparency` | 0.5 |
| `castsShadows` | True |
| `projectileFlightFX` | `pfx_icebolt_flight01.pfx` |
| `projectileImpactFX` | `pfx_icebolt_impact01.pfx` |
| **`projectileWeaponTrail`** | **`swordfrost_fxtrail.dbr`** |
| Sounds | `spak_ice_projectile` (swipe), `spak_damage_freeze_shatter` (hit + explode) |

**`blizzard_projectilefx.dbr`** (the falling orb — 33 fields): **same `frostorb01.msh` mesh**, `scale` **1.2**, `Class` `ProjectileExploding`, `actorRadius` 0.5, impact `pfx_blizzard_impact.pfx`, `projectileDistance` 24.0.

**`swordfrost_fxtrail.dbr`** — the deepest visual data available, and it is fully specified:

| Field | Value |
|---|---|
| `Red256` / `Green256` / `Blue256` / `Alpha256` | **255 / 255 / 255 / 255** |
| `Shader` | **`shaders/effects/trailadditive.ssh`** |
| `Texture` | **`fx/fxtrails/wpntrail_frost01.tex`** |
| `MSFadeTime` | **400 ms** |
| `TrailShrinkSpeed` / `TextureDistance` | 2.0 / 10.0 |
| `FadeAlpha` / `DragUVs` | True / True |

**Clean negative, stated plainly:** the chain bottoms out at `.pfx` / `.msh` / `.tex` asset paths. **The pinned corpus ships only `Text_EN.arc`** — no `Animations.arc`, no asset archives. I checked every `.arc` on disk (8 files, all localization). **The particle-system definitions and meshes are not acquirable from this pin.** We can read *what effect is named and how it is coloured/shaded/faded*; we cannot read the particle system itself. That is the hard floor of this line of enquiry without a larger depot pull.

### 3d. Mechanical detail lost between params object and trace

This detail **is** modelled — it exists in the engine's params objects and drives simulation — but never reaches the replay trace:

| Datum | Source value | In trace? |
|---|---|---|
| **BLIZZARD** — drops per volley | **6** | no |
| — volley interval | **2.0 s** | no |
| — active duration | **8.0 s** | no |
| — number of volleys | **4** (⇒ 24 drops) | only via `attack_id` string |
| — drop height / fall time | **20.0 m / 0.8333 s** | only as `wind_up_s` |
| — drop velocity | **24.0 m/s** | no (`projectile_velocity_ms` null) |
| — per-drop hit radius | **1.32 m** | no |
| — scatter / drop radius / variation | 8.0 / 15.0 / 3.0 m | only scatter, as `radius_m` |
| — retargets | **False** (resolved once, at cast) | no |
| — rider | **30 % total-speed slow, 5.0 s** | in `ailments` as `gd_total_speed_slow` |
| **WAVE** — front speed | **11.4286 m/s** | no (`projectile_velocity_ms` null) |
| — sweep time | **1.4 s** | no |
| — start width → end width | **3.0 → 6.0 m** | only end width (6.0) |
| — depth (band thickness) | **1.0 m** | no |
| — dwell in band | 0.0875 s | no |
| — riders | 91 cold DoT/3 s, 30 % damage debuff/3 s | in `ailments` |
| **NOVA** — spoke spacing | **22.5°** (360/16) | derivable from `prong_count` |
| — splash radius | 1.5 m | no |
| — prong corridor half-width | **0.42 m** | no |
| — distance bands | **[0,2.5) ×0.50, [2.5,9) ×1.00, [9,12] ×1.40** | no |
| — freeze | **1.3–1.8 s** | as `action_lock` in `ailments` |
| — cold DoT | 77 over 2.0 s | in `ailments` |
| **ICEARMOR** — absorb / duration / cooldown | **25 % / 12 s / 32 s** | duration visible via `ailments` |
| — riders | **+35 % attack speed, +28 % cold dmg, slow immunity, cold retaliation** | no |
| — cast time | 1.8116 s | no |

**The blizzard's `wind_up_s = 0.8333` is not a windup.** It is `dropHeight / projectileVelocity` — the orb fall time — used as the windup because the source has **no cast animation for this skill at all** (`skillSpecialAnimationName` absent, confirmed on a 726-field dump). The tell *is* the visible descent of 6 orbs. A renderer drawing a 0.83 s "charge-up glow" on the caster is rendering the wrong thing entirely.

---

## §4 — Presentation-relevant fields nobody is consuming, ranked

Ranked by visual truth bought per unit of work.

| # | Change | Cost | What it buys |
|---|---|---|---|
| **1** | **Populate `projectile_velocity_ms` on `wave` (11.4286) and `blizzard` (24.0)** | Two constants. **Field already exists, already null-tolerant.** | The wave's lane *sweeps* instead of appearing whole; the blizzard's orbs *fall*. Currently both render as motionless shapes. Highest ratio in this table by a wide margin. |
| **2** | **Populate `prong_count` on `blizzard` (= 6, drops per volley)** | One int. **Field already exists.** | Turns one circle into six discrete orbs. The name generalises correctly: it is already documented as "the launched count." |
| **3** | **Add `duration_s` to the telegraph** | One new nullable float. | The single biggest omission. The nova lasts 0.857 s, the wave 1.4 s, the blizzard **8.0 s** — and the schema says nothing. A renderer cannot know how long to hold a danger zone. Blizzard is 9× the nova and reads identically. |
| **4** | **Add `stage_count` + `stage_interval_s`** (blizzard: 4 / 2.0) | Two nullable fields. | Makes the blizzard's rhythm renderable — four pulses, not one wash. This is the "multi-stage behaviour" the commission asked about; it exists upstream and is the only such case found. |
| **5** | **Promote `attack_id` sub-structure into declared fields** (`cast_idx`, `stage_idx`, `element_idx`) | Three nullable ints; **the data is already there**, encoded in a string. | 24 individually addressable orbs with per-drop impact timing, without string-parsing. |
| **6** | **Populate `skills[].element` in the header** | The engine already knows it (100 % on damage events). | Load-time VFX palette selection per skill. Currently 0/1,800. |
| **7** | **Carry `FileDescription` onto the skill row** | One string, straight from the source. | "large cone wave with cold and poison dot" — human-authored design intent, one line, free. Directly serves VFX selection and matching. |
| **8** | **Carry `camera_shake_amplitude` / `camera_shake_duration_s`** | Two floats, in the source (0.12; wave 1.0 s). | Genre-canonical impact weight. Currently zero camera feedback anywhere. |
| **9** | **Emit a telegraph (or a cast event) for `primordian_icearmor`** | New record on a `none`-geometry skill. | The boss gains 25 % absorb + 35 % attack speed for 12 s, 37.5 % of the fight. `ailments` shows the *state*; nothing marks the *moment*. |
| **10** | **Drive `commit_state` for skills 1–3** | Engine change, not schema. | The boss currently reads `idle` while casting its signature abilities. Animation cannot be driven from the entity stream for any AoE. |
| **11** | **Surface `opposition_roster.label` + `tier` into `header.entities[]`** | Copy two fields across records. | Boss nameplate reads "Primordian, the Forgotten One" instead of `boss&quest_slith_wightmirecave01_0`; boss-vs-elite framing becomes available. |
| **12** | **Carry the nova's distance bands** (`[0,2.5) ×0.50, [2.5,9) ×1.00, [9,12] ×1.40`) | One tuple. | The star is *more* dangerous at its rim — reverse falloff, a 2× cliff at 2.5 m. Currently invisible; a uniform-intensity ring actively misinforms the player. |
| **13** | **Carry `wave.start_width_m` (3.0)** | One float. | The lane widens 3.0 → 6.0. Only the end width ships, so the wave renders as a uniform 6.0 m corridor. |

**Not recommended:** carrying `.pfx`/`.msh`/`.tex` paths into the trace. They name assets we do not possess and cannot acquire from the current pin (§3c). They belong in a *static* skill→VFX mapping table read at bake, keyed on skill name — not in a per-cast event stream.

---

## §5 — Knowledge gaps not resolved

- **Particle systems and meshes are unreachable.** `.pfx`, `.msh`, `.tex` referenced by the FX chain are not in the pinned corpus (only `Text_EN.arc` present). Would require a larger depot pull; the viability of that is a separate question I did not open.
- **`.tpl` templates not parsed.** `templates.arc` exists at `vendor/grim-dawn/database/templates.arc` (781 KB). It would give field *semantics* and defaults — including whether `useTargetDir` absence really means "caster facing" (currently a declared-not-sourced reading, flagged CA-3 in the engine source). Not opened here; out of commission scope.
- **Localization tags unresolved.** The creature carries `description = tagSlithBossB02`; the English string is in `Text_EN.arc`, which is on disk and parseable. Not chased — the `g5_header` already supplies "Primordian, the Forgotten One."
- **One fixture only.** Every telegraph in both batteries comes from a single boss. "Families with true cones or other prong counts" cannot be answered for content that does not exist; the finding is *this fixture never casts them*, not *the engine cannot emit them*.

---

## §6 — Source list

**Traces (read-only):**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/**/*.jsonl` — 4,073 files, 2,303,525 records
- `~/Games/reincarnated-godot/tmp/wr3acc/traces/*.jsonl` — 200 files, 90,508 records

**Engine source:**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gd_nova.py` (1,166 lines)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gd_boss_kit.py` (1,476 lines)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` (709 lines)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py`

**Primary source (`.arz`, read-only, via `research/scripts/gd_arz_adapter_2026_07_24.py`):**
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/{database,gdx1,gdx2,gdx3}/**/*.arz`
- Records read: `primordian_frigidring.dbr` (304), `primordian_wave.dbr` (281), `chillbane_blizzard.dbr` (726), `primordian_icearmor.dbr` (641), `slith_wightmirecave01.dbr` (964), `icebolt_nova_fxprojectile.dbr` (32), `blizzard_projectilefx.dbr` (33), `tidalwavepoison_fxpak01.dbr` (6), `icearmor_chfxpak01.dbr` (3), `icebolt_flight_fx.dbr` (8), `icebolt_impact_fx.dbr` (6), `blizzard_impact_fx01.dbr` (8), `tidalwavepoison_fx01.dbr` (8), `icearmor_fx01.dbr` (7), `swordfrost_fxtrail.dbr` (14)

**Census scripts (scratch, not committed):** `/tmp/legolas_census/{census.py,census_godot.py,dump_dbr.py,fx.py,fx2.py}`
