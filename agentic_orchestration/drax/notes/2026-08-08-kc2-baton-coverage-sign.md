# KC2-SIM baton/v1 — CONSUMER COVERAGE SIGN. drax, 2026-08-08.

**Run:** KC2-SIM (conductor gandalf, RUN-CONDUCTOR), Phase B. **Gate:** the charter § 4.3
KIT-FIDELITY inversion — the consumer signs the coverage list **before** the emitter is built.
**Sourced from:** `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`
§§ 1.1–1.4, 2.1–2.3, 6.3, 10.3, 10.5–10.9, 11.1–11.6.
**Consuming seam:** `~/Games/reincarnated-godot/` — `scripts/wr2_playback.gd`,
`scripts/wr2_traceset.gd`, `scripts/wr2_actor_rig.gd`, `scripts/hud_minimap.gd`,
`scripts/run_wr2_playback.sh`.
**This document, not § 11.4, is what AC-11.3's 100 % coverage check runs against.**

No Godot code was written this session. No commit — conductor commits at gate close (§ 4.7).

---

## § A — The build I am signing against

Concretely, next session in `reincarnated-godot/`:

| Stage | What it becomes | Existing surface it lands on |
|---|---|---|
| 1 | `baton_traceset.gd` — loader + schema-version arm + closed-enum arms with a default limb | new sibling of `wr2_traceset.gd` (which already carries `EVADE_LIMBS`, `AI_STATES_W1`, `COMMIT_STATES`, `dir_of()`) |
| 2 | Arena floor + 6 emitter markers + player spawn, built from `config.arena` | `wr1_level.gd` / `kit_replica_level.gd` room builders |
| 3 | Actor pool: spawn on `spawn_time` at `spawn_point`, proxy body at true radius, nameplate from `display_name`/`level`/`tier` | `wr2_actor_rig.gd` (`derive_stride_from_scale()`, proxies at true `entity_radius_m` — the standing posture since WR2) |
| 4 | Approach + engage choreography, animation blend driven by the emitted path's own derivative | `wr2_playback.gd` locomotion block |
| 5 | Player rig + spinning 3.0 m disc, disc centre read from `circle_sweep`, never recomputed | `wr2_playback.gd` telegraph/geometry block (dual-family + shape-boundary match, per § 2.3 / L-16) |
| 6 | HP + energy bars, damage numbers, DoT dressing, death VFX | `wr2_playback.gd` `_ps_build` HUD surfaces (globes, hotbar, boss bar + pips), `hud_minimap.gd` |
| 7 | Wave banner + run clock + end card | `_banner_reflow()`, `cam_identity_line()`, the provenance strip |
| 8 | MP4 at CAM-LOCK (34.83 m / 52.954° / fov_v 31.786 / player-locked, 36.32 px/m), camera identity on frame | `run_wr2_playback.sh` + `OUTBASE` |

**Run size I am budgeting for.** § 10.9's bimodal clear-time means give band A's own arithmetic:
`83 × 14.29 s + 9 × 28.57 s = 1,443 s ≈ 24.1 min`; band B is 943.60 s ≈ 15.7 min. A 25–40 min run
is band A plus margin. At 12.25 Hz that is **17,700–29,400 ticks**, ~**1,600–2,000 actors**
(band A Σ raw E = 1,600.4), and — upper-bounded — ~**120,000 event records**. In compact JSON:
tracks ≈ 3.2 MB, events ≤ 18 MB, actors ≈ 0.4 MB → **≈ 22 MB single document**. That is inside
what the existing loader already does per battery (the WR3-ACC cohort was 200 files / 87 MB).
**No sidecar or NDJSON split is needed at v1.** If a future run exceeds ~100 MB I will ask for one;
I am not asking now.

---

## § B — Per-item coverage verdict

Verdicts: **SUFFICIENT** · **INSUFFICIENT-because …** · **MISSING**.
Amendment IDs `M-n` are collected in § D.

### B.1 — Envelope

| § 11.4 item | Verdict |
|---|---|
| `baton_trace_format: "v1"` | **SUFFICIENT.** Version arm at load; unknown version refuses rather than guesses. |
| `run_id` | **SUFFICIENT.** Goes on the provenance strip verbatim. |
| `emitted_at` | **SUFFICIENT.** Provenance strip. |
| `spec_pin {spec_note, charter_commit, ledger_commit}` | **SUFFICIENT.** Strip; not rendered into geometry. |
| `sim_pin {engine_commit, sim_module_version, seed}` | **SUFFICIENT.** On frame, as camera identity already is. |

### B.2 — `config.fixture`

| Field | Verdict |
|---|---|
| `name: "EoRWarlGuts"` | **SUFFICIENT.** Banner. |
| `build_of_record: "b28gD0KN"` | **SUFFICIENT.** Banner. |
| `eor_rank_total: 26` | **SUFFICIENT.** Banner ("EoR 26"). |
| `identity_grade: "MEASURED"` | **SUFFICIENT.** Banner, with the grade word rendered — same discipline as WR2's `[engine-default-ungraded]` suffix. |
| `identity_envelope: "+3.9%/-0.5%"` | **SUFFICIENT.** Banner. The picture will never say "matches 100 %". |

### B.3 — `config.encounter`

| Field | Verdict |
|---|---|
| `difficulty: "gladiator"` | **SUFFICIENT.** |
| `start_wave_label` / `first_wave_fought` | **SUFFICIENT.** Both drawn; the +1 is visible rather than silently applied. |
| `lives: 1` | **SUFFICIENT.** No rewind UI is built. |
| `bonus_spawn_p06: <bool\|"UNKNOWN">` | **INSUFFICIENT-because** it describes the **fixture**, and I need what **the run did**. `"UNKNOWN"` gives me no answer to "do I light emitter 6". Split it → **M-1**. |
| `defenses: []` | **SUFFICIENT** as a measured empty. I draw no defense structures and the empty array is why. |
| `blessings: []` | **SUFFICIENT** — measured zero, both sittings. |
| `mutators: "OUT-OF-MODEL"` | **SUFFICIENT.** No mutator icons are drawn, and the string is what licenses that absence. It rides onto the NOT-MODELLED strip (§ B.9). |

### B.4 — `config.kit`

| Field | Verdict |
|---|---|
| `drain_unit` | **SUFFICIENT.** Energy-bar label only. |
| `tick_period_s` | **SUFFICIENT.** Drives the spin cadence and the frame↔tick line. |
| `attack_speed_pct` | **SUFFICIENT.** Banner. |
| `radius_m: 3.0` | **SUFFICIENT**, and cross-checked against `circle_sweep[].radius` per frame; a disagreement warns rather than picks. |
| `weapon_damage_pct: 64` | **SUFFICIENT.** Banner only. |
| *(absent)* `rotation_speed_multiplier`, `channel_tail_s`, `soulfire{}`, `hit_test_model` | **MISSING → M-2, M-3, M-4, M-5.** Every one is already a § 1 / § 2 constant of record. Withholding them makes my rig hold a literal the baton could have carried — the exact custody shape that has now bitten this seam **three times** (the nova unit payload pre-R-WR2-15(2); `C_reach` pre-D-F3; the split-declaring roster row with no entity id). I am not taking a fourth. |

### B.5 — `config.arena`

| Field | Verdict |
|---|---|
| `emitter_positions[6]` | **INSUFFICIENT-because** the array is positional and p05/p06 are *not interchangeable with p01–p04*: p05 is the ambush point (staggered 3 s drip from t + 4 s, § 10.6) and p06 is the player-elected bonus point. I must address them by label to give them different portal treatment and different arrival timing. → **M-6**. |
| `player_spawn` | **SUFFICIENT** for run start (the player is continuous across waves and does not respawn). |
| `placement_extents: 8.0` | **INSUFFICIENT-because** it is a scatter *budget* and does not say **who rolls it**. If the sim rolls a spawn position inside the 8.0 m and hit-tests against it, that position is causal and mine to receive, not to invent. → **M-7**. |
| `positions_provenance: "DECLARED"` | **SUFFICIENT.** Renders as a DECLARED tag on the arena in the provenance strip. |
| *(absent)* axis/units/facing convention | **MISSING → M-8.** Blocking. `player_path{x, y}` and `circle_sweep.centre` do not say which Godot axis `y` is, what the units are, the handedness, or the facing zero/sign/wrap range. Getting handedness wrong **mirrors the fight**: the monster taking damage stands on the wrong side of a disc that is drawn correctly. |
| *(absent)* arena bounds | **MISSING → M-9.** `hud_minimap.gd` takes an arena rect as an input — the current build passes `36.0 × 36.0 m`. Deriving bounds from the convex hull of an emitted path makes the floor and the mini-map a different shape per run, and makes § 10.9's ~7.0 s cycle floor (declared to be *a property of the arena's geometry*, AC-10.7) un-auditable from the baton. |
| *(absent)* collision / obstacle model | **MISSING → M-10.** § 10.6 lists traps, chests, defense points and NPCs as *not modelled*. My level kits contain walls. If nothing says the arena is an open plane, I can dress a wall across a path the player walks straight through. |

### B.6 — `actors[]`

| Field | Verdict |
|---|---|
| `actor_id` | **SUFFICIENT** as the join key, provided it is unique run-wide (not per-wave). Pin it → folded into M-13. |
| `record_path` | **SUFFICIENT** for AC-6.4 provenance, and it is what my nameplate cites. **Not sufficient as a mesh selector** — see `family`, M-11. |
| `display_name` | **SUFFICIENT.** Nameplate + death card. |
| `tier (trash\|hero\|boss\|nemesis)` | **INSUFFICIENT-because** "champion" is a second axis, not a tier. § 10.5(4) is explicit that champions **ADD, never convert**, and § 10.5(5) puts three champions on every 151–170 hero placement. If a champion-of-a-trash-pool and a hero-pool hero both arrive as `hero`, I cannot mark them apart. → **M-12** (either `is_champion`, or a one-line declaration that hero ≡ champion in this sim). |
| `spawn_point` | **SUFFICIENT** once M-6 gives it a label space. |
| `spawn_time` | **SUFFICIENT**, and it is what carries the p05 3 s drip without any extra field. |
| `level` | **SUFFICIENT.** Nameplate. |
| `hp_max` | **INSUFFICIENT-because** the semantics are unpinned: wave 160's `characterLifeModifier` is **324**, and F-2 records a 1.58× error from applying the wave-100 slice. A bar drawn against a pre-scaling `hp_max` is wrong by that factor and looks plausible. Pin `hp_max` = final post-scaling value actually used → folded into M-13. |
| `wave` | **SUFFICIENT.** |
| *(absent)* `family` / archetype | **MISSING → M-11 (SHOULD).** Without it my record_path→mesh map is a substring sniff, which is precisely the defect standing open against `TelegraphSpec.family` (rung (a) dead, an `attack_id` substring carrying 47.2 % of a battery's circles). If it does not land I will ship an **explicit checked-in mapping table** in the Godot repo, auditable row by row, and say on frame that the mapping is presentation-owned — but a sim that holds the record already holds the family. |
| *(absent)* `entity_radius_m` | **MISSING → M-5 (paired with `hit_test_model`).** § 2.1 hit-tests point-to-point (`\|e.position − c\| ≤ 3.0`), so a body at 3.4 m with a 0.6 m proxy visually touches a disc it is not in. I must know whether radii are sim-owned or mine. |
| *(absent)* `engage_time` | **MISSING → M-14.** See consult answer 2. |

### B.7 — `waves[]`

| Field | Verdict |
|---|---|
| `wave` | **SUFFICIENT.** Banner headline. |
| `content_tier` / `reward_tier` | **SUFFICIENT**, and I draw both — AC-10.2 explicitly allows them to differ, so a banner showing one would be lying half the time. |
| `t_start` / `t_end` | **SUFFICIENT**, once `t` is pinned to one monotonic run clock (M-13). The inter-wave gap falls out of `t_start(w+1) − t_end(w)`, which is where the banner lives. |
| `outcome` | **INSUFFICIENT-because** the value set is not enumerated. Value-set growth has caught this seam **three runs running** (`reposition` joining `intent`; `evade:` growing a suffix; `AI_STATES` 6 → 9). Enumerate it, including the wave-160 not-a-clear case → **M-15**. |
| `life_modifier_pct` | **SUFFICIENT.** Banner ("life ×3.24" at wave 160) and the F-2 regression guard made visible. |
| `spawn_points_active[]` | **SUFFICIENT** once labelled (M-6). Drives which portals light. |
| `actor_ids[]` | **SUFFICIENT.** Gives me "monsters remaining" as a join against death events — a join, not a re-derivation. |
| *(absent)* `nemesis_wave` | **MISSING → M-16 (SHOULD).** Derivable from `actors[].tier`, but P-E6 already emits the column and wave 160's banner is the showcase. Cheap; if refused I derive it and label the derivation. |

### B.8 — `events[]`

| Field / member | Verdict |
|---|---|
| `event_type` (the 9-member enum) | **INSUFFICIENT-because** three gaps: (a) `channel_end` cannot express the § 1.1 three-state machine `{IDLE, CHANNELLING, TAIL}` — a tick may land **up to 0.25 s after release** (AC-1.3), so a spin that stops on `channel_end` is a picture disagreeing with the damage → **M-3**; (b) no heal/leech/regen member, so an HP track that rises has no author → **M-17**; (c) no telegraph member at all, against § 2.3's own citation of the BR-2 G-1h law → **M-18**. |
| `t` | **INSUFFICIENT-because** unpinned origin. → **M-13**. |
| `fight_tick` | **INSUFFICIENT-because** the `record_fight_events()` spine it inherits is **per-fight**, and this is one continuous 93-wave run. If it resets per wave, my `fight_tick` ↔ `circle_sweep.tick_index` join silently crosses waves. This is the same class as the frame↔tick offset that captions a wind-up frame "STRIKE". → **M-13**. |
| `wave` | **SUFFICIENT.** |
| `source_id` | **SUFFICIENT** for actor-sourced events; **must be non-null on `player_death`** → **M-19**. |
| `target_id` | **SUFFICIENT.** |
| `damage_dealt` | **INSUFFICIENT-because** the semantic is unpinned (payload vs applied-to-HP), and HALT-7 says the mitigation model is not in the read set. The WR3-ACC precedent is measured: summing `delivered` under-read `player_damage_taken` by up to **47.5 %** (max residual 288.96 HP) because the stream carried no over-time channel. `dot_tick` fixes the channel; it does not fix the semantic. → **M-20**. |
| `damage_type` | **SUFFICIENT** as a type label. **Not** sufficient as a skill discriminator (see `source_skill`). |
| `geometry_type` | **SUFFICIENT** for the player's disc, and I will match on the **dual family + shape boundary** per § 2.3 / L-16 — never on `shape` alone, which the `wr2_cell_bat` selector-repair precedent proves blinds silently. |
| `position` | **INSUFFICIENT-because** it does not say **whose**. This single ambiguity is the difference between "I solve monster positions from an annulus predicate" and "I interpolate between known samples". → **M-21**, and it is the highest-value line in this document. |
| *(absent)* `source_skill` / `ability_id` | **MISSING → M-22.** Soulfire is a *second cadence* (§ 1.4, 0.2 s, orbiting, CCW, front-start) that must not be folded into the disc, and Gutsmasher's 100 % Fire→Physical conversion means the disc is all-physical while Soulfire stays Lightning. `damage_type` therefore separates them **for this fixture, by accident of the conversion**. Leaning on that is a substring sniff wearing a different coat. |
| *(absent)* `hp_after` | **MISSING → M-23.** The single most load-bearing absence in § 11.4. See B.10 and consult answers 3 and 5. |
| *(absent)* `is_crit` | **MISSING → M-24 (conditional).** § 1.3 carries `offensiveCritDamageModifier +12 %`, so crits exist in the kit. Emit the flag **only if the sim rolls them**; if it does not, declare `crit_model: NOT_MODELLED` and I draw no crit emphasis. I will not manufacture a crit the sim did not roll. |
| *(absent)* DoT window | **MISSING → M-25 (SHOULD).** Bleed is 540/3 s pre-modifier with Gutsmasher's **+100 % duration**. Inferring the window from first-to-last `dot_tick` stops the VFX early on the last body. One `duration_s` or `expires_at` closes it. |
| `spawn` | **SUFFICIENT** (redundant with `actors[].spawn_time`; redundancy is a cross-check, and I will run it). |
| `tick_damage` | **SUFFICIENT** *only under* **M-26**: emitted **per (tick, target)**, never aggregated per tick or per wave. Aggregation destroys the in/out-of-disc membership predicate that constrains my entire crowd choreography. |
| `dot_tick` | **SUFFICIENT.** This is the WR3-ACC lesson already fixed in the draft, and I note it as such. |
| `death` | **SUFFICIENT** for actor deaths (actor via `target_id`, killer via `source_id`, time via `t`). |
| `channel_start` | **SUFFICIENT.** |
| `channel_end` | **INSUFFICIENT** — see M-3. |
| `energy_dryout` | **SUFFICIENT**, and it is a genuinely good beat: the spin dying for want of energy is readable without any extra field. |
| `wave_start` / `wave_end` | **SUFFICIENT** (redundant with `waves[]`; cross-checked). |
| `player_death` | **INSUFFICIENT** — see M-19 (mandatory non-null killer) and M-23 (HP into the floor). |

### B.9 — `tracks` and `provenance`

| Item | Verdict |
|---|---|
| `player_path[] {t, x, y, facing}` | **INSUFFICIENT-because** of rate and coincidence, not shape. See consult answer 1 → **M-27**. Fields themselves are right. |
| `circle_sweep[] {tick_index, t, centre, radius}` | **SUFFICIENT** — this is the § 2.3 G-1h telegraph payload in the correct form (`{centre, radius, tick_time}` per tick, not a flag plus a duration). `centre` needs the M-8 convention and the M-27 coincidence guarantee; the record shape is exactly what I want. |
| `player_hp[] {t, hp}` | **INSUFFICIENT-because** a uniform-rate HP track cannot hold the death moment. See consult answer 5 → **M-23**. |
| `player_energy[] {t, energy, energy_max, reserved}` | **SUFFICIENT** in shape — `reserved` is what lets the globe draw § 5.2's reservation as a dead band rather than as missing energy. Pin whether `reserved` is absolute or a fraction → folded into M-13. |
| *(absent)* per-actor HP | **MISSING → M-23.** § 11.3 states the sim owns *"HP tracks (player **and every actor**)"* and § 11.4 emits **only** `player_hp`. That is a direct contradiction between the truth-boundary table and the field inventory, and it is the one that stops monster HP bars — the deliverable names them. |
| `provenance` (§ 11.5, whole block) | **SUFFICIENT, and I will render it.** `calibration_grade`, `identity_grade` + envelope, `u8/u9_closure_state`, `drain_fork`, and the `out_of_model` list all go on frame — the list becomes a **NOT-MODELLED strip** (devotion procs · mutators · defenses · retaliation · Ascension · M2 rewind · tributes) so the picture never implies it is showing what it is not. The G-5 and G-2 declarations get named on the wave-160 banner and on the death card respectively. Nothing here is missing. |

### B.10 — The § 11.3 ↔ § 11.4 contradiction, stated on its own

**§ 11.3 promises the sim owns HP tracks for the player and every actor. § 11.4 emits one track,
for the player.** Everything downstream of that gap — monster bars, boss bars, the pip row already
built in `_ps_build`, damage numbers that land on a body whose remaining HP is legible, and the
death card — sits on the wrong side of it. Closing it by summing damage events is exactly the
forbidden re-derivation, and the WR3-ACC measurement is the proof that event sums are a **lower
bound**, one-signed, exact on only 17 of 200 seeds. **M-23 is the amendment I care most about.**

---

## § C — Named consult answers

### C.1 — Sample rates

**`player_path` needs 10 Hz minimum, and I am asking for the tick grid (12.25 Hz) instead —
not for smoothness, but to kill a drift class.**

Interpolation error first. Sagitta of a circular arc sampled at interval `h`, for speed `v` and
turn rate `ω`: `e ≈ v·ω·h²/8`. Taking the fixture's 135 % run speed as ≈ 4.0 m/s and a brisk
un-channelled 180°/s turn (`ω = π`):

| rate | `h` | error | at CAM-LOCK 36.32 px/m | as a fraction of the 3.0 m disc radius |
|---|---|---|---|---|
| 12.25 Hz (tick) | 0.0816 s | **1.05 cm** | 0.38 px | 0.35 % |
| 10 Hz | 0.100 s | **1.57 cm** | 0.57 px | 0.52 % |
| 5 Hz | 0.200 s | **6.28 cm** | 2.3 px | 2.1 % |
| 2 Hz | 0.500 s | **39.3 cm** | 14.3 px | **13.1 %** |

So **a lower uniform rate plus interpolation is acceptable down to 10 Hz and no further.** 5 Hz is
visible motion-smoothing at my lens; 2 Hz moves the player by an eighth of the disc radius between
samples, which can move a body across the disc boundary — a picture disagreeing with the damage.

**But rate is the smaller half of the answer.** § 2.2 rules that *the disc centre IS the emitted
player position*. If `player_path` runs on a 10 Hz wall clock and `circle_sweep` on the 12.25 Hz
tick grid, the two grids are incommensurate, my interpolated body and the emitted disc centre drift
apart by up to ~1.6 cm at every tick, and **AC-2.2 becomes unverifiable inside the baton** — there
is no pair of records to compare. So:

> **M-27.** `player_path` is emitted on a uniform grid of **≥ 10 Hz** covering the whole run,
> **and** carries a sample at **every** tick timestamp, that sample bearing the `tick_index` and
> being **bit-identical** to `circle_sweep[tick].centre`. Simplest conforming emission: put
> `player_path` on the 12.25 Hz tick grid throughout, ticking through IDLE stretches too.

Cost of the simple form over a 40 min run: 29,412 samples ≈ 2.0 MB. That is nothing against a
22 MB document, and it converts AC-2.2 from an assertion into a check I run at load.

**Facing: per-tick is enough, and I do not want turn-rate or turn-event data.** The 0.35×
channelled turn rate makes facing a *slower* signal than the sample grid, so sampled facing
over-samples it; and because I only ever interpolate emitted samples, my render cannot out-turn
the constraint. Two conditions, both cheap:

1. The convention must be declared — units, zero direction, sign, and wrap range (M-8). A naive lerp
   across a 2π wrap spins the character 359° the wrong way, once per crossing.
2. `rotation_speed_multiplier: 0.35` rides in `config.kit` (M-2), so my blend tree reads it and my
   audit can assert rendered angular velocity never exceeds it — rather than my rig holding `0.35`
   as a literal, which is the custody defect this seam has now hit three times.

**`circle_sweep` stays per-tick, unchanged.** Keep `radius` per record even though it is constant
3.0: it is the telegraph payload, and § 2.3 is explicit that a flag-plus-duration is not sufficient.

### C.2 — Monster approach choreography

**`spawn_time` + `spawn_point` + subsequent damage events are *sufficient to constrain me* and
*insufficient to keep me from inventing a number the sim already holds*. I want the explicit
timestamp — `engage_time` per actor (M-14).**

The constraint half works, and I want to be precise about why, because it is the good part of the
design. For any actor the player damages, the first `tick_damage` at `t₁` means the actor was
within 3.0 m of the emitted disc centre at `t₁`; and for every tick in `[channel_start, channel_end]`
where the actor is alive and *absent* from the damage stream, the actor was **outside** 3.0 m. That
is a per-tick boolean annulus membership for every engaged body — a hard, checkable constraint that
my choreography physically cannot violate without the check firing. I will build that check
(`_approach_audit()`, sibling of `_audit_framing()`) and run it every render. **That is the
mechanism that makes "presentation owns approach" safe, and it holds.**

The hole is not in the constraint, it is in the ownership. § 10.9 decomposes the cycle floor as
`spawn_resolution + approach_traversal + engagement_kill_time + advance_tick_latency`, and AC-10.7
requires the ~7.0 s floor to **emerge from spawn-and-traversal geometry rather than be asserted**.
That means the sim computes an arrival time, that arrival time is causal (it gates when the kill can
start, and therefore the wave clock), and under R-KC2-7 causal quantities are sim-owned. If it is
not emitted, I invent an arrival that the sim already decided — and the two can differ by seconds
on early waves without contradicting a single damage event, because a monster that arrives at t=5
and is first hit at t=9 (player not channelling in between) leaves me free to walk it in at t=9.
Nothing breaks; the wave clock quietly becomes fiction.

`engage_time` is one float per actor on a ~2,000-actor list. **Ask: emitted, `null` permitted with a
declared reason.** If it is refused, I choreograph to the damage-bound envelope and say on the
banner that approach timing is presentation-owned — but I would rather have the number.

**Two riders.** (a) `tick_damage` must be per-(tick, target), never aggregated — **M-26**; the
membership predicate is the whole mechanism. (b) The scatter-roll owner must be declared — **M-7**;
if the sim rolls a position inside `placement_extents = 8.0` and hit-tests against it, that position
is causal and belongs in `actors[]`. "Crowd micro-spacing inside the declared scatter" is mine;
the scatter roll itself may not be.

### C.3 — VFX and readability fields

`damage_type` + `geometry_type` is a floor, not a kit. Ranked by what the picture loses:

| Ask | ID | Why |
|---|---|---|
| **`source_skill` / `ability_id`** — MUST | M-22 | Disc, Soulfire, bleed and each monster ability need distinct VFX. § 1.4 forbids folding Soulfire into the disc, and it *happens* to be separable by `damage_type` only because Gutsmasher converts Fire→Physical at 100 %, leaving Soulfire the build's lone Lightning source. That is an incidental property of one fixture. The `TelegraphSpec.family` defect is open in my own state file for the identical reason. |
| **`hp_after`** — MUST | M-23 | Serves three jobs at once: monster bars without re-derivation, exact bar motion at any sample rate, and **kill-blow for free** (an event whose `hp_after` is 0). |
| **kill-blow flag** — only if M-23 is refused | M-23b | With `hp_after` this is a join between two emitted facts, not a derivation. Without it, my death VFX fires on a bare `death` event with no attribution and no impact frame. |
| **`is_crit`** — conditional MUST | M-24 | § 1.3 carries a `+12 %` crit-damage modifier, so crits exist in the kit. Emit **only if rolled**; otherwise declare `crit_model: NOT_MODELLED`. I will not synthesise crit emphasis. |
| **DoT window (`duration_s` / `expires_at`)** — SHOULD | M-25 | Bleed at 540/3 s with **+100 % duration**. First-to-last `dot_tick` under-runs the window and drops the bleed dressing early on the last body of a pack. |
| **`damage_dealt` semantic pinned; `damage_raw` + `damage_applied` if they differ** — MUST | M-20 | HALT-7 puts the mitigation model outside the read set. If the number is a payload and the bar is HP, the numbers on screen will not add up to the bar — and the WR3-ACC measurement (up to **47.5 %** under-read) is what a silent version of this looks like. With `hp_after` present the reconciliation is checkable at load, which is how I want it. |
| **heal / leech / regen author** — MUST (may be a declaration) | M-17 | `leech` has been a stub in my harness since WR2. If the player's HP can rise, name the event; if it cannot, declare `player_hp_increases: NONE` and I will **assert** it, warning on any rising sample rather than smoothing it. |
| **monster attack model declared** | M-18 | See below. |
| DoT-source distinction as such | — | **Already covered.** `dot_tick` as a distinct `event_type` is the right split and I do not need more, once M-22 names the source. |
| crit magnitude, overkill, absorbed/blocked | — | **Not wanted.** Block DISSOLVES (§ 7); overkill buys nothing. |

**On monster attacks (M-18).** § 6.3 gives monster damage as an upper bound with the rank binding
unread, HALT-7 puts mitigation out of model, and § 11.4 carries **no telegraph event of any kind** —
while § 2.3 invokes the BR-2 G-1h law by name for the player's kit. So the wave-160 death arrives as
a player HP drop with nothing on screen that authored it. I am **not** asking the sim to build a
monster telegraph model this lap. I am asking it to **say which world I am in**:
`monster_attack_model: "abstract-schedule"` (I own the wind-ups, origins and shapes entirely, and I
label them presentation-owned on frame) **or** `"geometric"` (then I need `{origin, shape, radius,
wind_up_s}` per attack and I will draw the real thing). Either answer is buildable. Silence is not:
silence is how I end up drawing a meteor at a place the sim never put one and calling it engine
output.

### C.4 — Arena geometry

**`emitter_positions[6]` + `player_spawn` + `placement_extents: 8.0` is NOT a sufficient contract.
Four additions, all free — these are declared parameters, so one more declared parameter costs the
sim nothing.**

1. **`axis_convention` (M-8) — the blocking one.** `{up_axis, handedness, units, facing_units,
   facing_zero, facing_sign, facing_range}`. Without it I cannot place a single node, and the
   failure mode is not a crash: wrong handedness **mirrors the arena**, so the body taking damage
   stands opposite a disc drawn perfectly. This is the same family as the WR2 projection lie, where
   a correct 2.000000 m separation *looked* like interpenetration at 41° — a frame will not tell me
   which of us is wrong.
2. **`arena_bounds` (M-9).** Explicit rect or disc. `hud_minimap.gd` takes an arena rect as input
   (currently `36.0 × 36.0 m`); hull-deriving it from the path makes the floor and the mini-map a
   different shape per run, and makes AC-10.7's "the floor emerges from geometry" un-auditable from
   the baton alone — which is the charter § 0 sentence's whole point. If the sim runs an unbounded
   plane, say `arena_bounds: UNBOUNDED` and I will size the floor from the data plus a declared
   margin and put that on the banner.
3. **`emitter_ids` (M-6).** Labels `p01..p06`, not array slots. p05 is the ambush point with its own
   arrival law; p06 is the elected bonus point. They need different portal treatment and only one of
   them is conditional.
4. **`collision_model` (M-10) + ground plane (folded into M-8).** § 10.6's unmodelled traps, chests,
   NPCs and defense points are exactly the props my level kits want to place. Declare the arena an
   open plane with no blocking geometry and I will dress it so; leave it silent and I will
   eventually put a wall where a path runs.

Plus **M-1**: `bonus_spawn_p06` currently describes the fixture and may read `"UNKNOWN"`. The run is
not unknown to itself. Split into `fixture_p06_state: bool|UNKNOWN` (provenance, keeps the ±8.4 %
branch honest) and `run_p06_enabled: bool` (mandatory, non-null — whether I light emitter 6). This
matters materially at the showcase: § 10.8 puts p06 in wave 160's **hero slot**, so its state is the
difference between 5 raw bodies and 4 on the wave that kills the fixture.

### C.5 — Wave banners, run UI, and the death moment

**Banners: nearly complete.** `wave` + `content_tier` + `reward_tier` + `life_modifier_pct` +
`t_start`/`t_end` give a banner reading *"WAVE 160 · content 16 / reward 16 · monster life ×3.24"* —
and drawing the 324 rather than a wave-100 168 is F-2 made visible on frame. Two gaps: `outcome`
needs its enum (M-15) and `nemesis_wave` should be carried rather than derived (M-16). **I am not
asking for the bonus timer** — § 10.3 records it as not modelled, so no countdown is drawn.

**Run UI (M-28, SHOULD).** Waves cleared, kills, elapsed and final wave are all derivable joins, and
I will build them as joins. I want an emitted `run_summary { waves_cleared, actors_killed,
run_duration_s, final_wave, end_reason }` anyway, **to assert my joins against**. The end card is
precisely where a derived number gets loudest and least checkable — my own `_ai_print_census()`
shipped a hard-coded "92,525 decision records" over every trace it ever opened, and printed it
backwards on a cohort carrying zero. An emitted summary turns that class of defect into a warning
at load.

**The death moment — this is where the baton is thinnest.** The material is
`player_death` + the HP track, and both need work:

- **`player_death.source_id` mandatory non-null (M-19).** The card names the killer. G-5 rules
  that wave 160 is *rolled honestly from pools and never a scripted Zantarin reenactment* — so
  whichever of the ten p01 nemeses, five p02, two p03 or the p04 superboss the sim actually rolled
  is the name I draw, and the baton is the only thing that knows it. The card carries the G-5 and
  G-2 declarations verbatim, so the viewer knows the name is a roll and the damage is a ceiling.
- **`hp_after` on every player-targeted event (M-23).** The death is `104.73 s into wave 160` against
  five champion-tier bodies including three nemeses. A player at ~6,000 HP can go to zero inside a
  handful of ticks. A uniform 10 Hz `player_hp[]` renders that as a bar teleporting to empty; a
  1 Hz track renders it as a bar that is simply already empty. Event-locked HP makes the drain exact
  at any track rate, needs no track rate increase, and gives me the kill-blow frame for free.
- **`t_end` on the death wave = the death time, and `outcome` says not-a-clear (M-15).** Wave 160 was
  not cleared; if its record looks like every other wave's, the end card contradicts the run.
- Survivors at the death — actors alive with no death event — must simply remain standing. That
  falls out of `actors[]` minus death events. **Sufficient**, no field needed.

---

## § D — MISSING fields list (explicit)

**MUST — absent, the build stalls or the picture can disagree with the damage.**

| ID | Field / amendment |
|---|---|
| **M-1** | Split `bonus_spawn_p06` → `fixture_p06_state: bool\|"UNKNOWN"` (provenance) **+** `run_p06_enabled: bool` (mandatory non-null). |
| **M-2** | `config.kit.rotation_speed_multiplier: 0.35`. |
| **M-3** | Channel state completed: distinguish **release** from **tail expiry** — either `channel_release` + `channel_expiry` members, or a `state ∈ {IDLE, CHANNELLING, TAIL}` on `channel_end`. AC-1.3 puts ticks up to 0.25 s past release. |
| **M-4** | `config.kit.channel_tail_s: 0.25` and `config.kit.soulfire { period_s, direction, start, explosion_radius_m }`. |
| **M-5** | `config.kit.hit_test_model: "point"\|"radius"`, **and** `actors[].entity_radius_m` if radii are sim-owned (if point-tested, declare radii presentation-owned and I will size proxies and say so). |
| **M-6** | `config.arena.emitter_ids: ["p01".."p06"]` — a label space, not array slots. |
| **M-7** | Declare the scatter-roll owner: either `actors[].spawn_position` (sim rolls inside the 8.0 m and hit-tests it) or `scatter_model: "emitter-point; scatter presentation-owned"`. |
| **M-8** | `config.arena.axis_convention { up_axis, handedness, units, ground_elevation, facing_units, facing_zero, facing_sign, facing_range }`. **Blocking.** |
| **M-9** | `config.arena.arena_bounds` — explicit rect or disc, or `UNBOUNDED`. |
| **M-10** | `config.arena.collision_model` — declare the open plane / absence of blocking geometry. |
| **M-13** | Clock + identity pins: `t` monotonic from run start; whether `fight_tick` / `tick_index` reset per wave (and if so, a `(wave, tick)` composite); `actor_id` unique run-wide; `hp_max` is the **final post-scaling** value; `player_energy.reserved` absolute or fractional. |
| **M-14** | `actors[].engage_time` (nullable with a declared reason). |
| **M-15** | `waves[].outcome` — closed, versioned enum including the not-a-clear case; `t_end` on the death wave = death time. |
| **M-17** | Heal / leech / regen: an event member, **or** the declaration `player_hp_increases: NONE`. |
| **M-18** | `monster_attack_model: "abstract-schedule" \| "geometric"`; if geometric, `{origin, shape, radius, wind_up_s}` per attack. |
| **M-19** | `player_death.source_id` mandatory non-null. |
| **M-20** | `damage_dealt` semantic pinned (payload vs applied-to-HP); both `damage_raw` and `damage_applied` if they differ. |
| **M-21** | `events[].position` disambiguated → `source_pos` (nullable) + `target_pos`. For damage events `target_pos` is the target's position at the event tick — the number the sim already computed for the hit test. |
| **M-22** | `events[].source_skill` / `ability_id`. |
| **M-23** | **Per-actor HP.** Preferred form: `hp_after` on every damage/DoT event (exact, event-local, gives monster bars, exact player drain, and kill-blow in one field). Acceptable alternative: per-actor sampled HP tracks. **This closes the § 11.3 ↔ § 11.4 contradiction and is the amendment I care most about.** |
| **M-24** | `is_crit` **if crits are rolled**; otherwise `crit_model: NOT_MODELLED`. |
| **M-26** | `tick_damage` emitted per **(tick, target)** — never aggregated per tick or per wave. Stated as a schema obligation, because the whole crowd-choreography constraint rests on it. |
| **M-27** | `player_path` at **≥ 10 Hz uniform** over the whole run, **with** a sample at every tick timestamp bearing `tick_index` and **bit-identical** to `circle_sweep[tick].centre`. Simplest conforming form: put the path on the 12.25 Hz tick grid throughout (≈ 2.0 MB / 40 min). |

**SHOULD — absent, I ship a labelled fallback and the picture is poorer.**

| ID | Field | Fallback if refused |
|---|---|---|
| **M-11** | `actors[].family` / archetype | An explicit checked-in `record_path → mesh` table in the Godot repo, auditable row by row, labelled presentation-owned on frame. **Never a substring sniff.** |
| **M-12** | `actors[].is_champion`, or a declaration that hero ≡ champion | Champions render identically to heroes; § 10.5(5)'s three-heroes-per-placement reads as three of the same thing. |
| **M-16** | `waves[].nemesis_wave` | Derived from `actors[].tier` and labelled DERIVED. |
| **M-25** | DoT `duration_s` / `expires_at` | Window inferred first-tick→last-tick; bleed dressing ends early on the last body of a pack. |
| **M-28** | `run_summary { waves_cleared, actors_killed, run_duration_s, final_wave, end_reason }` | Joined from `waves[]` + events; end card carries no cross-check against the sim's own accounting. |

**Nothing on this list requires the sim to model anything new.** Every MUST item is either a
constant already in §§ 1–2, a quantity the sim must already hold to run § 2.1's hit test or § 10.9's
traversal, a declaration of a modelling choice already made, or a sample-rate/shape decision on data
already being emitted. **M-18 and M-17 are explicitly satisfiable by a one-line declaration.**

---

## § E — What I am NOT asking for

Recorded so the coverage check does not read absence as an oversight.

- **Monster position tracks.** R-KC2-7 gives me approach choreography and I want it. M-21 + M-26 +
  M-14 constrain me tightly enough that my picture cannot disagree with the damage; full monster
  paths would invert the ruling and cost the most bytes in the document.
- **Camera, lighting, VFX selection, animation, audio, crowd micro-spacing, disc rotation phase.**
  Mine. `config.arena.positions_provenance: "DECLARED"` is already the honest label for the arena
  itself.
- **Bonus timer, tributes, score, rewards, mutator identities, defense structures, M2 rewind,
  devotion procs, Ascension, retaliation.** All declared out of model. They appear as a
  **NOT-MODELLED strip** on frame and nowhere else. I will not draw what the sim did not run.
- **A scripted wave 160.** L-11 rules it rolled honestly; I render whatever rolled, name it, and
  carry G-5 on the card.
- **Any sidecar / NDJSON split at v1** — the ≈ 22 MB budget does not need it.

---

## § F — Standing consumer obligations I take on

So the sign is symmetric.

1. **Never re-derive a sim-owned quantity.** Disc centre from `circle_sweep`; player position from
   `player_path`; HP from the HP source; damage from events. Locomotion blend weights are taken from
   the **emitted path's own derivative** — reading the emitted number, not computing a second one.
2. **Default arms on every enum**, matched on prefix where a suffix has grown before, with a
   `push_warning` on an unrecognised value. Three value-set growths in three runs; I plan for a
   fourth.
3. **Every constant the baton carries is read, never held as a literal**, and where a fallback path
   fires it says so on the banner (the C_reach precedent).
4. **Every derived quantity on frame is labelled DERIVED**, and asserted against an emitted
   cross-check wherever one exists.
5. **`_approach_audit()` runs every render** — asserting that every actor absent from a tick's damage
   set was outside 3.0 m of that tick's emitted centre, and every actor present was inside. A
   failure is a render-blocking finding, not a warning.
6. **Load-time reconciliation** of `Σ damage_applied` against the HP tracks, reported as a
   measurement whichever way it lands, never smoothed.
7. **Engine tree read-only.** Any temporary compensation carries a `// TODO(drax)` and an entry in
   `reincarnated-godot/AGENT_STATE.md`, removed cleanly when the emitter catches up.

---

## SIGN

**SIGNED — coverage sufficient as amended by the listed items.**

The § 11.4 draft is the right shape: sibling artifact, `export/` conventions, per-tick telegraph in
the G-1h form rather than a flag-plus-duration, `dot_tick` split out (the WR3-ACC over-time hole
pre-closed), and a provenance block I can render whole without a single synthesised claim. The gaps
are amendments, not architecture — **28 items, of which 23 are MUST and 5 are SHOULD, and every MUST
is a constant, a declaration, a disambiguation, or a rate decision on data the sim already holds.**

Three carry the most weight and I name them so they are not lost in a list of twenty-eight:

- **M-23** — per-actor HP. § 11.3 promises it, § 11.4 omits it, and everything from monster bars to
  the death card sits on the wrong side of the gap.
- **M-21** — whose position `events[].position` is. One word of schema prose is the difference
  between interpolating known samples and solving an annulus predicate.
- **M-8** — the axis and facing convention. Without it I cannot place the first node, and the
  failure mode is a mirrored arena that looks entirely correct.

Amend those twenty-eight and I will build the whole picture from the baton alone.

*— drax, presentation seam, 2026-08-08. No commit; conductor commits at gate close (charter § 4.7).*
