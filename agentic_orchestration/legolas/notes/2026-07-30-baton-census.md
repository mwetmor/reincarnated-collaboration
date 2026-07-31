# BATON-CENSUS — does the emitted trace schema carry what a SCENE needs? — 2026-07-30

**Mode:** A (analytical, READ-ONLY throughout — no engine writes, no godot-tree writes, nothing regenerated)
**Commissioner:** gandalf (`RUN-CONDUCTOR`), from the LR/presentation session
**Class:** evidentiary note (format probe)
**Method:** parsed REAL emitted `.jsonl` traces (785 files across four batteries), diffed key-sets
three ways, then read the consumer (`reincarnated-godot/scripts/wr2_playback.gd`, 3,636 lines) and the
producer (`simulation/spatial_gauntlet/replica_frame_emitter.py`, `simulation/spatial_gauntlet/spatial_engine.py`)
to explain every gap the data showed.

---

## §0 — WHICH ARTIFACTS THIS IS BUILT ON (and the one that does not exist)

| battery | mtime | traces | role here |
|---|---|---|---|
| `output/kitcal_g5/g5/traces/` | 2026-07-28 21:19 | 165 | **G-5 BASELINE** for the before/after diff |
| `output/kitcal_g5/wr2_battery_after/*/traces/` | 2026-07-30 08:25 | **450** | the largest post-telegraph corpus; **the only one where the nova actually LANDS** |
| `output/kitcal_g5/wr3_battery_after_s11{,_det}/*/traces/` | 2026-07-30 15:33 | 165 each | freshest FULL battery with traces |
| `output/kitcal_g5/wr3_w1_smoke/*/traces/` | 2026-07-30 **16:45** | 5 | **the newest emission in the tree** — the only one carrying the W-1 amendment |
| `output/kitcal_g5/wr3_battery_s2/` | 18:37 | **0** | report JSON only |
| `output/kitcal_g5/wr3_battery_s2b/` | 19:56 | **0** | report JSON only |
| `output/kitcal_g5/wr3_stagesweep_s2b/` | 19:59 | **0** | report JSON only |
| `output/kitcal_g5/wr3_clean_ablation/` | 21:01 | **0** | two summary JSONs |

⚑ **The four freshest Stage-2 / Stage-2b artifacts contain ZERO trace files.**
`find wr3_battery_s2 wr3_battery_s2b wr3_stagesweep_s2b wr3_clean_ablation -name '*.jsonl' | wc -l` → **0**.
The newest emitted trace in the whole tree is 16:45, and Stage-2b's mechanisms landed after it.
This is not a "cannot answer" — it is the answer, and it is §7 below.

Schema strings on the newest emission are UNCHANGED: `replica-frame/v1` (base) + `g5-replay-trace/v1`
(superset). Every wave addition is **additive and key-absent-tolerant**; a pre-amendment trace still parses.

---

## §1 — THE NEEDS-vs-CARRIES TABLE

| # | scene render need | verdict | evidence |
|---|---|---|---|
| 1 | **TELEGRAPH GEOMETRY** | **CARRIES** (shapes exercised: 2 of 4) | §2 |
| 2 | **SKILL FLAVOR** (element + mechanic per event) | **CARRIES-PARTIALLY** | §3 |
| 3 | **STATUS STATES** (freeze/CC/stun per frame) | **CARRIES** — under a different name, and unexercised in the freshest traces | §4 |
| 4 | **PROJECTILE / TRAVEL** | **ABSENT** | §5 |
| 5 | **COMBATANT IDENTITY** | **CARRIES-PARTIALLY** — `is_boss` is a live lie | §6 |
| 6 | **STAGE-2b MECHANICS** (wave / blizzard / icearmor) | **NEVER EMITTED**; one of the three is structurally unrenderable | §7 |
| 7 | what else the wave added (diff vs G-5) | **five additions, all additive** | §8 |

---

## §2 — TELEGRAPH GEOMETRY — **CARRIES**

The `telegraph` event is 19 fields and carries the full geometry set. Real record, the frigidring nova
(`wr3_battery_after_s11/…/traces/boss__B__seed74000808.jsonl`):

```json
{"record_type":"event","tick":7,"t_s":0.7,"event":"telegraph",
 "attack_id":"boss&quest_slith_wightmirecave01_0:nova:1",
 "attacker_id":"boss&quest_slith_wightmirecave01_0","skill_idx":1,
 "fire_tick":30,"fire_t_s":3.0188405797101447,"wind_up_s":2.318840579710145,
 "shape":"circle","origin_x_m":26.15859567407256,"origin_y_m":15.41632345377963,
 "orientation_rad":null,"radius_m":12.0,"range_m":null,
 "half_angle_rad":null,"width_m":null,"damage_amount":218.07587472172813}
```

So: **shape ✓ · origin ✓ · radius ✓ (12.0 m, the 12 m nova) · windup ✓ (2.3188 s) · fire instant ✓
(both tick and seconds) · announced payload ✓.** Orientation, half-angle and width are declared fields
with `null` here because a circle has no orientation.

**Three caveats a scene must carry:**

1. **Only two shapes have ever been emitted.** Across the 165-trace `after_s11` battery: `point` 627,
   `circle` 114. Nothing else. `orientation_rad` / `half_angle_rad` / `width_m` are `null` on **100 %
   of every telegraph ever written**. The fields exist; no exemplar does.
2. **Telegraphs are MOB-SIDE ONLY** — 741 / 741 attackers are mobs. The player's `cone` (`feral_claws_r16`)
   and `line` (`rip_and_tear_r16`) swings emit **no telegraph at all**. A scene that wants a player windup
   tell must drive it off `commit_state` / `ai_state`, not off this channel.
3. **Two known internal disagreements, both already surfaced by drax and neither reconciled:**
   `range_m: 10.0` on the header skill row vs `radius_m: 12.0` on the telegraph (a 2 m gap on the nova);
   and on `point` telegraphs `wind_up_s: 0.5` while `fire_tick == tick` (i.e. `fire_t_s − t_s == 0`).
   The consumer rules `fire_t_s` governs (`wr2_playback.gd:2455-2461`) and warns once. That ruling should
   ride the baton as text, because it is a *convention*, not a field.

---

## §3 — SKILL FLAVOR — **CARRIES-PARTIALLY**

**Element arrives only at impact, never at windup.**

| where | element? |
|---|---|
| `header.entities[].element` | `null` on 100 % of entities, all batteries |
| `header.entities[].skills[].element` | `null` on 100 % of skill rows, all batteries |
| **`telegraph.element`** | **field does not exist** |
| `damage.element` | **populated** — `chaos` 9,157 / `physical` 1,222 / `cold` 202 (after_s11) |
| `death.death_element` | populated |
| `ailments[].element` | populated (`chaos` on bleed/poison; `null` on `action_lock`) |

Consequence: a scene cannot tint a *windup* by element from the trace. It must join
`telegraph.skill_idx` → `header.entities[].skills[skill_idx].name` → a hard-coded lookup. The consumer
already does exactly this and says so (`wr2_playback.gd:2028-2035`: "`element` COLOURS THE HIT AND
NOTHING ELSE").

**Mechanic label is a string-sniff, not a field.** `geometry` is carried on damage events
(`cone` 4,174 / `dot` 4,467 / `point` 1,424 / `line` 516 in after_s11; `circle` 132 in the WR2 battery)
and on header skill rows. Skill *names* are carried (`primordian_frigidring_r4`, `feral_claws_r16`,
`slith_wightmirecave01_attack`) and are joinable by `skill_idx`. But the only "this is a nova" marker is
the substring `:nova:` inside `attack_id` — and the run's own analyser parses it that way
(`wr3_cell_kc_2026_07_30.py:551`). There is no `mechanic` / `family` field.

**One broken join, worth naming.** On the nova's realized hit the damage event reads `skill_idx: -1`
(the emitter coerces the producer's `None`), so the boss's signature mechanic is the ONE damage event
that cannot be joined back to its own skill row:

```json
{"event":"damage","source_id":"boss&quest_slith_wightmirecave01_0","target_id":"gd-werewolf-kitcal-1",
 "amount":414.8,"delivered":414.8,"element":"cold","skill_idx":-1,"geometry":"circle", … }
```

---

## §4 — STATUS STATES — **CARRIES**, under a different name, and cold in the freshest traces

`tick.entities[].ailments` is a list of `{name, remaining_s, element}`, present on every entity block
since the G-5 baseline. Observed vocabulary, whole-corpus:

| name | where seen | count |
|---|---|---|
| `poison` | mob-side, `element: chaos` | 51,280 frames (s11) / 197,733 (WR2) |
| `bleed` | mob-side, `element: chaos` | 5,481 frames (s11) |
| **`action_lock`** | **player-side, `element: null`, `remaining_s` 1.3 → 0.1** | **1,716 frames — WR2 battery ONLY** |

**`action_lock` IS the nova's freeze/CC.** `gd_nova.py:21-26` refuses to emit RDR `freeze` on purpose
(GD's `dmgspecial_freeze_handler.dbr` has no shatter operator; A-FRZ-1 stays armed) and applies
`ACTION_LOCK_NAME = "action_lock"` instead, pinned at `freeze_min_s = 1.3 s`
(`spatial_engine.py:6109`). So the CC channel exists, is per-frame, and is duration-carrying.

**But it is ZERO in every freshest battery.** `after_s11` (165 traces), `after_s11_det` (165) and
`w1_smoke` (5): **0 `action_lock` frames, 0 `circle`-geometry damage events**. The player escaped every
one of the 114 novas. A scene built and validated against the 15:33/16:45 traces would render a
CC mechanic it has never once seen fire. **The exemplar lives in `wr2_battery_after/` (08:25) and
nowhere newer.**

Also absent everywhere: `freeze`, `stun`, `slow`, `chill`, `root` — zero token matches across all
785 traces, although `spatial_engine.py:787` recognises `freeze` and `stun` names.

**Adjacent per-frame state the scene can use as status** (all present, all consumed or consumable):
`commit_state` (idle 136,152 / windup 12,392 / strike 3,096 / recovery 6,192) · `is_leashing`
(False on 100 %, dormant) · `is_activated` · `energy` · `skill_cooldowns[]` · and — new at 16:45 —
`ai_state`.

---

## §5 — PROJECTILE / TRAVEL — **ABSENT**

The producer's entire event API is eight methods: `header · tick · on_hit · dot · deaths_from_diff ·
telegraph · decision · footer` (`replica_frame_emitter.py`). **There is no spawn event, no travel
event, no impact-position event.** Damage events carry no coordinates at all.

The nova makes this concrete. It is a ring front that physically travels at 14.0 m/s and is resolved by
a **sub-tick crossing solve** (`spatial_engine.py:6028-6033` — "the tick is 0.1 s and the ring front
advances 1.4 m per tick against a 1.5 m blast, so a stationary snapshot can step the front straight
past a target"). What the trace emits is **one telegraph at mint** and **one damage event at crossing**.
Everything between — the expanding front, the 16 spokes, the realized spoke count `n` that decides
whether this crossing hits for 0 or 2× — is computed, appended to an in-memory ledger
(`gd_nova_crossings`, a 7-tuple carrying `r_star` and `n`) and **never written to the trace**.

A scene therefore has to *invent* the ring's motion: reconstruct `r(t)` from `(t − fire_t_s) × v`, where
`v` is not in the trace either. That is a fabrication with a plausible shape — the exact class of thing
this census exists to catch.

**Related absence:** the damage event carries **no `attack_id`**, so a hit cannot be joined to the
telegraph that caused it. The only reconstructable join is `(source_id, geometry, t_s window)`.
`attack_id` on the damage/dot events is a **one-field rider** and it is the cheapest thing on this list.

---

## §6 — COMBATANT IDENTITY — **CARRIES-PARTIALLY**

**Carried, per entity** (`header.entities[]`): `entity_id`, `kit_ref`, `side` (`player`/`mob`),
`is_player`, `entity_radius_m`, `spawn_x_m`/`spawn_y_m`, `max_hp`, and — new this wave —
`hp_provenance` (`"M"`/`"D"`) and `movement_speed_ms`. Skills carry `{skill_idx, name, geometry, range_m, element}`.

**Carried, per fight** (`g5_header.g5`): `kit_id` (`"gd-werewolf-kitcal-1"`) and an
`opposition_roster[]` with the human-facing labels a scene actually wants —
`{label: "Primordian, the Forgotten One", record: "boss&quest/slith_wightmirecave01", char_level: 13,
tier: "boss", hp_grade: "M", dmg_grade: "HELD-SWEPT", max_hp: 14812.0}` — plus, new at 16:45,
`commit_reach.by_attacker_m` (`{boss: 2.5, slitha_melee: 2.5, slitha_shaman: 18.5}`).

**⚑ BROKEN: `is_boss` is `false` for the boss.** On 100 % of traces, baseline and current, every entity
including `boss&quest_slith_wightmirecave01_0` writes `is_boss: false`; `threat_tier` is `null` on 100 %;
`header.boss_focus_entity_id` is `null`. The consumer already discovered this and works around it by
`entity_id.begins_with("boss")` cross-checked against largest-`max_hp`, warning loudly on disagreement
(`wr2_playback.gd:2984-3008` — "a `getattr`-style read here returns false forever and the depiction
would silently draw no commit lock at all, with every counter reading a clean 0"). **A field that is
present and always wrong is worse than an absent one**, and it is currently defended only by a
naming convention in the spawner.

**Roster join is a string transform, not a key.** `opposition_roster[].record` is
`"boss&quest/slith_wightmirecave01"`; `entity_id` is `"boss&quest_slith_wightmirecave01_0"` —
`/`→`_` plus a spawn index. No declared key field.

**Hero-slot: NOT APPLICABLE, not absent.** These are 1-player fights; `side: "player"` has exactly one
occupant. There is no party/slot concept in the schema to be missing.

---

## §7 — STAGE-2b: NEVER EMITTED, and one of three is structurally unrenderable

Stage 2b added three boss mechanics (`spatial_engine.py:6153-6157`, R-WR3-22 / R-WR3-23(1) / R-WR3-24):
`primordian_wave`, `chillbane_blizzard`, `primordian_icearmor`. **None has appeared in a single emitted
trace** — the batteries that exercised them (`wr3_battery_s2b`, `wr3_stagesweep_s2b`, 19:56–19:59)
wrote report JSON and no traces. I read what they WOULD emit, from source:

**`primordian_wave` → `shape: "rect"`** (`spatial_engine.py:6245`). A **new shape token that has never
existed in any trace**, and the first telegraph ever to populate `orientation_rad` (the caster heading),
`range_m` (`p.distance_m`) and `width_m` (`p.end_width_m`), with `radius_m: null`.
Consumer status: **accidentally correct.** `_spawn_telegraph`'s `else` branch already builds a
`BoxMesh(width_m, 0.04, range_m)` rotated by `orientation_rad` (`wr2_playback.gd:2501-2508`) — which is
a rect. It works because rect is the fall-through, not because rect was modelled.

**`chillbane_blizzard` → `shape: "circle"`** (`spatial_engine.py:6382`) with
`radius_m = scatter_radius_m`, `origin` = **the storm centre, not the caster**, `wind_up_s` = the orb
**fall** time, and `damage_amount` **per drop, not per storm**.
Consumer status: **SILENT WRONG RENDER.** `wr2_playback.gd:2435` is
`var is_ring := (shape == "circle") and rad_v != null` — an unqualified test. A blizzard telegraph would
be **registered as a nova** (`_wr3_register_nova(ev)`), painted the nova's blue expanding ring, have its
radius written into `_tell_radius_m`, and — worse — **be scored into `_nova_verdicts`**, silently
corrupting the escape-rate statistic the run is being graded on. Nothing warns. This is drax's own D-F4
shape: an exhaustive match with no discriminating arm.

**`primordian_icearmor` → NOTHING.** No telegraph, no event, no per-frame field. Its state lives on
`mob._wr3_icearmor` (`spatial_engine.py:6183, 6443-6471`), a plain attribute — **not** in
`combatant_state.active_effects`, which is the only thing `_ailments()` reads
(`replica_frame_emitter.py:71-84`). So a **25 % damage-absorption buff** (`_wr3_icearmor_factor`,
`:900-908`) plus a **+28 % outgoing cold modifier** (`:6169`) is running on the boss and is **invisible
in the trace by construction**. A scene cannot show that the boss is armored; a grader cannot see why
damage dropped 25 %; and a viewer watching numbers fall would read it as a bug.

---

## §8 — WHAT THE WAVE ADDED (three-way key diff vs the G-5 baseline)

| addition | where | landed in |
|---|---|---|
| **`decision` event** — `{tick, t_s, target_id, intent}` | new event type | after_s11 (92,525) |
| **`telegraph` event** — 19 fields (§2) | new event type | after_s11 (741) |
| `crit` (bool) + `crit_multiplier` (float\|null) | `damage` event | after_s11 — 145 / 10,581 = **1.37 %** player-side; **0 / 1,424** mob-side |
| `hp_provenance`, `movement_speed_ms` | `header.entities[]` | after_s11 |
| **`ai_state`, `max_hp`, `movement_speed_ms`** | **`tick.entities[]`** | **`w1_smoke` ONLY (16:45)** |
| **`commit_reach`** — `{law, against_entity_id, body_separation_v2, by_attacker_m}` | **`g5_header.g5`** | **`w1_smoke` ONLY** |

`decision.intent` vocabulary, measured: `reposition` 38,260 · `advance` 26,809 · `evade:commit` 17,694 ·
`evade:pressure` 6,814 · `hold` 1,916 · `evade:tg` 1,032. **Player-side only.**

`ai_state` vocabulary, measured on `w1_smoke`: `engage` 1,611 · `approach` 654 · `windup` 440 ·
`recover` 220 · `strike` 110 · **`null` 24**. Enemy blocks only — the player block omits the KEY
entirely (950/950). Three-valued presence is deliberate (AI-D3): key absent = out of scope; key present
+ `null` = corpse or no live foe; key present + string = a vocabulary member. **A consumer that treats
absent and null as one branch will silently mis-render death frames.**

⚑ **The W-1 additions exist in exactly FIVE trace files in the entire tree.** Everything else — including
both 165-trace batteries and the 450-trace WR2 battery — predates them.

**Consumer coverage of the new surface** (`grep -c` on `wr2_playback.gd`): `commit_state` 24 · `ai_state` 9 ·
`max_hp` 9 · `movement_speed_ms` 5 · `hp_provenance` 4 · `geometry` 6 · `entity_radius_m` 6 · `width_m` 4 ·
`skill_idx` 3 · `orientation_rad` 1 · **`ailments` 0 · `half_angle_rad` 0 · `skill_cooldowns` 0 ·
`commit_reach` 0 · `opposition_roster` 0 · `kit_ref` 0 · `threat_tier` 0**.
The CC channel (§4) is carried by the producer and **read by nobody**.

---

## §9 — THE SINGLE MOST DANGEROUS GAP

**`primordian_icearmor` has no emission channel at all — and the blizzard telegraph will be
mis-registered as a nova.** One mechanic is invisible; the other is actively mislabelled into a
statistic the run is graded on.

They are one finding because they share a root: **Stage 2b was built without a trace-emission pass, and
its batteries emitted no traces, so nothing forced the question.** The icearmor gap is the worse half —
it is not a missing field on an existing record, it is a state that lives outside the only structure
the emitter reads (`combatant_state.active_effects`), so no amount of consumer cleverness recovers it.
Fixing it after the baton closes means re-emitting, because the buff's up/down schedule cannot be
reconstructed from anything in the file.

**Three riders, in cost order, all additive and all `replica-frame/v1`-compatible:**

1. **Route `_wr3_icearmor` through `combatant_state.active_effects`** (or emit a parallel `buffs: []`
   on the entity block) so a 25 %-absorb window is a per-frame fact. *Cheapest correct fix; nothing
   downstream breaks, because `ailments` is already a list and already tolerates unknown names.*
2. **A `family` (or `mechanic`) string on the telegraph event** — `"nova" | "blizzard" | "wave" | "melee"`
   — so the consumer stops discriminating on `shape == "circle"`. This retires the silent-wrong-render
   **and** retires the `:nova:` substring-sniff in the run's own analyser at the same time.
3. **`attack_id` on `damage` and `dot` events.** One field; makes telegraph→hit joinable; removes the
   `skill_idx: -1` dead end on the nova's own hit.

Two more worth a line in the spec even if not fixed: **`is_boss` should be true for the boss** (a
present-and-always-wrong field, currently defended by a spawner naming convention), and **element on
the telegraph** (flavor currently arrives only at impact).

---

## §10 — IS THE SCHEMA BATON-READY FOR SCENE RENDERING AS-IS?

**Baton-ready for the fight the traces actually contain — NOT baton-ready for the boss the wave now builds.**

For the WR1/WR2-era fight, yes, and demonstrably: telegraph geometry is complete for the 12 m nova,
positions/headings/HP are per-frame at 10 Hz, intent and crit are live, and the consumer already renders
it. Nothing in §2–§6 blocks a scene; §5's projectile gap is the only one that forces the renderer to
invent motion, and even that is bounded to one mechanic.

For the **Stage-2b** boss, no. Two of the three new mechanics are unsafe to render today (one invisible,
one mis-registering), and **all three are unobserved** — I could describe their emission only by reading
the producer, never by parsing a record. **A scene certified against the 15:33/16:45 traces would be
certified against a boss that no longer exists.**

The window is real: all three riders in §9 are additive fields on records the emitter already writes.
Landed before the run banks, they cost a field each. Landed after, they cost a re-emission —
and in icearmor's case they cost the re-emission regardless, because the buff schedule is not
recoverable from any file now on disk.

---

## §11 — WHAT I DID NOT ESTABLISH

- **No Stage-2b trace was parsed** — none exists. Every §7 claim about wave / blizzard / icearmor
  emission is read from `spatial_engine.py` source (line numbers given), not from data. If a Stage-2b
  battery is emitted with traces, §7 should be re-run against it rather than trusted.
- **`action_lock` was observed only in `wr2_battery_after/`** (engine-of-record differs from the 16:45
  emission). I did not verify the lock still emits under the W-1 amendment; the amendment is additive
  and does not touch `_ailments`, so it should, but "should" is not "measured".
- **I did not run anything.** No battery, no smoke, no regeneration. All 785 traces were read as they lay.
