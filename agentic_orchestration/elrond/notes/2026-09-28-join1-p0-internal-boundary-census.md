# JOIN-1 P0 — the INTERNAL / BOUNDARY census (paper, zero code)

> ⚑ **NAMED FINDING, 2026-10-01 (§ 11, forward):** the D2 WW Barbarian's frozen record goes from **14 rows to 16** (BOUNDARY 9 → 11), per jack-ryan's Sorceress-census Gate-2 A-4/W3 (collab `b48500a4d`, KP-165). The text above § 11 is left as committed (`78797db4b`); § 11 governs where it differs.
> **STATUS:** CURRENT — W1 deliverable of the KC2-PLAY **SEAL LAP** (`gandalf/notes/2026-09-28-kc2-play-seal-lap-plan.md` § 2, seat elrond; launch-sheet **L3**, paper-only).
> **Date:** 2026-09-28 · **Author:** elrond (data steward) · **Conductor:** gandalf (`RUN-CONDUCTOR`).
> **Governing text:** `gandalf/notes/2026-09-28-join-key-architect-pass.md` **§ 8 (governs over §§ 1, 3, 5)** — Matt's Q86 ruling: every roster game's **kit-internal** mechanisms enter **natively, as a union**; only the **kit↔world boundary** is shared, as **ONE rulebook**, Grim Dawn's validated rules as default, widened by **lever** only where a foreign kit's interaction cannot be expressed. E-1: joined kits are tuned to **our** balance thresholds; each kit's **home-game margin is measured and recorded**.
> **Also governing:** `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` (three layers; the fidelity-grade LAW § 4; E-1 RULED, E-2 open).
> **Mode:** read-only on `corpus.db` and all data. **No schema change this lap.** Zero code. GD oracle read as reference only.
> **Slate (Q88):** D2 Whirlwind Barbarian (the first real join) · PoE1 Cyclone · PoE2 Bonestorm · one cooldown-only kit, selected in § 4.

---

## 0 · Headline

**Six findings, in the order they matter.**

1. **Matt's boundary list is right but incomplete, and the evidence says so in three places.** Hit resolution · damage-type-vs-resistance · mitigation order · CC/status on monsters · the tick clock are all confirmed boundary. Three more items are boundary by the same test (a foreign kit cannot be adjudicated without them) and **every kit on the slate touches all three**: **target selection / multiplicity**, **movement↔engagement coupling during an action**, and **the damage-family registry itself** (§ 6).
2. **The INTERNAL/BOUNDARY dichotomy needs a third verdict, and it is not a quibble — three boundary items have NO Grim Dawn rule to default to.** Monster-side CC/status, player-side projectiles, and player agency are boundary questions where the GD oracle is **empty**, not merely narrow. "Widen GD's rule" presumes a rule. Verdict class **BOUNDARY / GD-EMPTY** is required (§ 7.1).
3. **GD welds hit chance and critical damage into one scalar, and two independent kits on this slate break on it.** `threat.resolve_hit` derives the crit tier from the *same* PTH value and d100 roll that decides the hit. D2 (independent Deadly Strike / Critical Strike procs) and PoE2 (independent crit chance × crit multi) both need them separable, and Vampire Survivors needs "always hit, never crit", which GD cannot express at all: PTH ≥ 135 forces multiplier 1.5. **Lever `crit_model` is the highest-confidence widening on the slate — three witnesses, two of them DATAMINED.**
4. **Proportional damage (%current-HP / %max-HP dealt BY the player) has no offense-side representation.** GD models it on *intake* only (`intake.PclLimb`, `gd_defensive_percent_current_life`). D2 Crushing Blow and VS Gorgeous Moon both need it. Second-highest-confidence lever.
5. **The "GD rulebook" is, today, one measured character's sheet — not a rulebook.** `threat.RESIST_PCT` is REFERENT-v1's own resistances; `player_offense` carries one kit's 43,691–59,761 raw band; `intake`'s armour table is one build's rolled pieces. The *equations* are general and sound; the *operands* are welded to one character. Every "GD's rule handles this AS-IS" verdict below is a claim about the **form**, never about a number a second kit could use. That is B2's adapter refactor stated as a data fact, and it is Failure Mode 2 measured rather than asserted.
6. **The GD-SLICE `is_core` split does NOT survive the union ruling — and it had already stopped meaning what its MIGRATION note says, before the ruling, by 3,232 rows.** § 8. Recommendation: do not lock the template against the current shape.

**Counts.** 49 mechanisms enumerated across four kits.

| Kit | INTERNAL | BOUNDARY | OUT-OF-ARENA | HELD (evidence) | total |
|---|---|---|---|---|---|
| D2 Whirlwind Barbarian | 3 | 9 | 2 | — | 14 |
| PoE1 Cyclone | 5 | 7 | 1 | — | 13 |
| PoE2 Bonestorm | 4 | 5 | — | 1 | 10 |
| VS Gorgeous Moon (cooldown-only) | 3 | 4 | 2 | — | 9 |
| **Slate** | **15** | **25** | **5** | **1** | **46 rows + 3 cross-cutting misfits (§ 7.3–7.5) = 49** |

Of the 25 BOUNDARY rows: **8 GD-AS-IS**, **14 NEEDS-WIDENING**, **3 GD-EMPTY**. Those yield **16 candidate levers, all OPEN** — of which **14 are settable** and **2 (L-14, L-15) are build items with no mechanism to parameterise** (§ 9).

---

## 1 · Method, and what "evidence" means here

Every row below carries a source and the **best fidelity grade available in that lane**, per the era-substrate LAW § 4. A row is never graded above its lane.

| Lane | Best grade available | Basis | Held where |
|---|---|---|---|
| **GD** (the boundary itself) | **MEASURED** for REFERENT-v1's behaviour · **DATAMINED** for `.arz` records | KC2 live-oracle fixtures; `exact_skill`/`exact_skill_field`, edition `gd-edition-II-20260724` | `reincarnated-engine/src/reincarnated/simulation/kc2/` · `corpus.db` |
| **D2** | **DATAMINED** | `fabd/diablo2` @ `45112569deb9384738ccafe5c24ebbb71f41c7c9`, **D2 1.13 classic** (NOT D2R — a named version skew) | `research/datamine-acquisition/d2/raw/Skills.txt` |
| **PoE1** | **DATAMINED, STALE-FLAGGED** | RePoE @ `8023a1d696dbddc836c05ac3fcedd072da1767d2`, brather1ng **last updated 2022-09-06**; the live fork `repoe-fork/repoe` @ `14e3edc` was **not** fetched | `research/datamine-acquisition/poe1/raw/gems.json` |
| **PoE2** | **attested only** | **There is no `poe2/` tree in `datamine-acquisition/`.** Sources are poe2db.tw + a pathofexile.com forum thread | `corpus.db` `kit_dossier` / `verify_ledger` |
| **VS** | **attested only** | vampire.survivors.wiki | `corpus.db` |

⚑ **The slate's fidelity floor is PoE2, and it is a floor with no upgrade path currently provisioned.** Bonestorm is the only PoE2 kit on the slate and PoE2 has no datamine lane at all. Per era-substrate § 4 it cannot be graded above attested. Every PoE2 row below inherits that ceiling; two of them additionally rest on an anchor the corpus itself marks `UNSUPPORTED` / `ANCHOR_WEAK` (§ 3, row 9).

**Verdict vocabulary used in the tables.**

- **INTERNAL** — enters natively per Q86. No boundary rule needed. May still *read* a boundary output (leech reads applied damage); where it does, the read is named.
- **BOUNDARY / AS-IS** — GD's rule expresses the foreign interaction without change of form.
- **BOUNDARY / WIDEN** — GD's rule cannot express it; a named candidate **lever**, status **OPEN**, GD's setting as default.
- **BOUNDARY / GD-EMPTY** — a real boundary question with **no GD rule at all**. Not a widening. § 7.1.
- **OUT-OF-ARENA** — kit-defining in its home game, no fight-boundary meaning. § 7.2.

---

## 2 · D2 Whirlwind Barbarian — `d2-ww-barb`

**Corpus:** `canon_corpus` T1 / `canon_tier=deep` / eras `classic;lod;d2r;rotw-s14`; `kit_mapping.grade = **EXACT**`, `terminal_state = MAPPED`, no deviation notes; 6 `kit_dossier` rows (1 abstained); `verify_ledger` 1064–1069 + 2209–2210 (7 CONFIRMED, 1 UNSUPPORTED on the `rotw-s14` era claim only); 0 dockets; `kits-export/d2-ww-barb.json`.
**Primary source:** `Skills.txt` rows `Whirlwind` (Id 151) and `Battle Orders` (Id 149), DATAMINED.

| # | Mechanism | Evidence (grade) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| 1 | Moving spin channel; hits everything along the movement path | `Skills.txt` `srvdofunc=76`, `range=none`, `anim=SQ` (DATAMINED) · dossier `skill_geometry` (attested) | BOUNDARY | `channel.ChannelMachine` IDLE/CHANNELLING/TAIL; `channel_policy.MovementWrap`, measured `REF_FRAC_MOVING_FIGHT = 0.6265`, `REF_P_CHANNEL_GIVEN_MOVING = 0.8920` | **AS-IS** — GD's referent *is* a moving channel. Footprint differs (path swath vs radius) → row 4 |
| 2 | Fixed frame cadence — `Param3 = 1` "Attacks per tick"; D2 attack speed resolves to **frame breakpoints**, not a continuous rate | `Skills.txt` `Param3=1`, `*Param3 Description` (DATAMINED) | BOUNDARY (tick clock) | `channel.tick_period_s = 0.16 × (100/AS%)`, `ticks_per_s = AS%/16`; continuous and AS-proportional; `FIRST_TICK_INDEX = 1` | **WIDEN** → **L-01 `tick_quantisation`** {`continuous-as-proportional` (GD default) \| `frame-breakpoint-table`} |
| 3 | Dual-wield alternation — `weapsel = 2`: each swing alternates weapons, so one skill emits **two differently-composed packets** | `Skills.txt` `weapsel=2`, `itypea1=mele` (DATAMINED) | BOUNDARY | `channel.compose_damage_basis()` composes **one** `DamageBasis` per tick | **WIDEN** → **L-02 `packets_per_tick`** {`1` (GD default) \| `n`}. ⚑ Note this is *not* the same as multi-target: it is multiple **source compositions** from one action |
| 4 | Target selection along a path; `TargetableOnly=1`, `SearchEnemyXY=1` | `Skills.txt` (DATAMINED) | BOUNDARY (§ 6 addition) | `player_offense.TARGET_MULTIPLICITY_CSV` (`pm4l_target_multiplicity.csv`) — a **measured constant** for the referent | **AS-IS in form, EMPTY in operand** — the equation exists, the number is REFERENT-v1's. See § 0 finding 5 |
| 5 | Mana cost at initiation — `mana=25`, `lvlmana=1`, `manashift=7` — **and `AttackNoMana=1`: the spin continues at zero mana** | `Skills.txt` (DATAMINED) | **INTERNAL** | `energy.EnergyModel` charges **per tick** and `DryOut` terminates | Enters natively as a second spend law. GD's per-tick drain and D2's charge-at-start-and-never-stop are two settings of a resource primitive the union already needs |
| 6 | Mana leech from gear sustaining the spin | dossier `skill_loop` + `item_alterations` (attested) | **INTERNAL** (Q86 names leech internal) · **reads a boundary output: `damage_applied_to_target`** | `player_sustain.ADCTH_PCT = 21.0`, `offensiveLifeLeechMin`, scope `GLOBAL-WEAPON-ATTACKS` | AS-IS on the read. Same shape both games |
| 7 | Battle Orders: timed self/party buff, `+%` **max** Life / Mana / Stamina; duration `750 + 250/level` frames + Shout/Battle-Command synergy | `Skills.txt` `aurastat1=item_maxmana_percent`, `aurastat2=item_maxhp_percent`, `aurastat3=skill_staminapercent`, `auralencalc`, `Param1/2/3/4/8` (DATAMINED) | **INTERNAL** (the buff) | — | Enters natively. ⚑ Explicitly **not a reservation**: the corpus mapping's "free persistent toggle (no reservation cost)" is confirmed by the record (no reserve field) |
| 8 | …but **raising max HP mid-fight** poses a rule GD has never had to answer: does current HP move with max? | derived from row 7 (DATAMINED input) | BOUNDARY | `intake.ascension_is_flat_positive_control(kit, hp_max)` — GD's only mid-fight HP grant, **Ascension, is FLAT and is asserted to be flat** | **WIDEN** → **L-03 `max_hp_change_policy`** {`preserve-current` \| `preserve-fraction`}. GD has no default because GD never raises max HP; the safe default is `preserve-current` (lower reading) |
| 9 | Hit resolution — D2 AR-vs-DR, clamped **[5 %, 95 %]**; `LevToHit=5`, `HitShift=8` | `Skills.txt` record fields (DATAMINED) + the D2 AR formula (MODEL-VERIFIED, community) | BOUNDARY | `threat.probability_to_hit(oa, da)` — two-term blend; `PTH_MINIMUM = 55.0`; `resolve_hit` d100 | **WIDEN** → **L-04 `pth_floor_pct`** (GD 55; D2 5) and **L-05 `pth_ceiling_pct`** (GD unbounded; D2 95). The *function* differs too, but a foreign kit joining under GD's function is E-1 measured cost, not inexpressibility — the **clamps** are the inexpressible part |
| 10 | Critical damage — D2 Deadly Strike / Critical Strike are **independent proc chances**, orthogonal to whether the swing hit | dossier `item_alterations` runewords (attested) + D2 formulas (MODEL-VERIFIED) | BOUNDARY | `threat.resolve_hit(pth, roll)` derives `crit_tier` from the **same** PTH and the **same** d100 roll: tiers at `PTH_THRESHOLDS (70,90,105,120,130,135)` → `PTH_MULTIPLIERS (1.0 … 1.5)` | **WIDEN** → **L-06 `crit_model`** {`pth-tiered` (GD default) \| `independent-proc`}. ⚑ **Three witnesses on this slate** (D2, PoE2, VS) |
| 11 | Crushing Blow (Grief/runeword rider) — **% of the target's current HP** | dossier `capstone_alterations` / `item_alterations` (attested) | BOUNDARY | GD models proportional damage on **intake only**: `intake.PclLimb` (`multiplicative-1-minus-26pct`), `gd_defensive_percent_current_life`. **No offense-side representation**; `threat.mitigate(damage: float, …)` takes an absolute | **WIDEN** → **L-07 `proportional_damage_offense`** {`off` (GD default) \| `pct-current` \| `pct-max`} + **L-08 `proportional_damage_mitigable`** {`yes` \| `no`} — because a proportional packet entering `mitigate` would still be multiplied by a resistance, and nothing says whether it should be |
| 12 | Physical damage type; monster **physical immunity** is the D2-era wall | `Skills.txt` (no `EType` on WW — weapon carries the type; `SrcDam=128`) (DATAMINED) · `MonStats.txt` resist columns held but not read this lap | BOUNDARY | `threat.RESIST_PCT` Physical = 16.0; armour on **Physical / SlowPhysical only**; `intake.OrderLimb.ARMOUR_THEN_RESIST` (primary by lineage, `R-PM4-62 part 3`); player cap `playerDefenseCap = 80` | **AS-IS.** A 100 %-immune monster is resist = 100 → zero, which the form expresses. ⚑ The immunity **wall** is an E-2 D2-era signature-feel item, not a boundary gap |
| 13 | `durability = 1` — the spin consumes weapon durability | `Skills.txt` (DATAMINED) | **OUT-OF-ARENA** | — | § 7.2 |
| — | Battle Orders projects to **allies** | dossier (attested) | **MISFIT — world-shape** | solo engine | Already ruled: `mechanic_gap_docket` **2** and **12**, both `matt-ratified` / `permanent-gap-record`. Consistent; no new docket owed |

**D2 WW Barb — INTERNAL 3** (5, 6, 7) · **BOUNDARY 9** (1, 2, 3, 4, 8, 9, 10, 11, 12 — of which **AS-IS 3**: 1, 4, 12; **WIDEN 6**: 2, 3, 8, 9, 10, 11) · **OUT-OF-ARENA 2** (13, and the ally-scope row). **14 rows.**

---

## 3 · PoE1 Cyclone — `poe1-cyclone`

**Corpus:** T1 / deep / eras `2.x;3.0-3.6;3.7-3.13;3.20+`; `grade = **EXACT**`, MAPPED, no deviation notes; 6 dossier rows (0 abstained); `verify_ledger` 77–79, 2398 all CONFIRMED; **1 open docket: 176** `poe1_cyclone_base_weapon_dps_build_point_gap`.
**Primary source:** `gems.json` → `Metadata/Items/Gems/SkillGemCyclone`, DATAMINED (stale-flagged).

| # | Mechanism | Evidence (grade) | Class | GD's rule | Verdict |
|---|---|---|---|---|---|
| 1 | Channelled melee attack; skill types `[Attack, Area, Melee, Movement, Channel, Physical]`; `is_manually_casted` | `gems.json` `active_skill.types` (DATAMINED) | INTERNAL (the channel state) + BOUNDARY on its clock | `channel.ChannelMachine`; `tick_period_s` | **AS-IS** — GD's referent is the same shape |
| 2 | **Stage accumulator** — `cyclone_gain_stage_every_x_ms_while_channelling` **330 ms @ L1 → 170 ms @ L20**; `cyclone_max_number_of_stages` **3 → 6**; `cyclone_stage_decay_time_ms = 330` | `gems.json` `per_level` stats (DATAMINED, exact) | **INTERNAL** | — | Enters natively. ⚑ **Positive census result:** the same accumulator primitive serves PoE2 Bonestorm's shard count (§ 4 row 1). One internal primitive, two games |
| 3 | The accumulator **grows the hit footprint**: `cyclone_melee_weapon_range_+_per_stage = 1`, `cyclone_area_of_effect_+%_per_additional_melee_range = 8`, `is_area_damage = 1` | `gems.json` `static.stats` (DATAMINED) | BOUNDARY (target selection) | `player_offense` target multiplicity is a **measured constant per body**, not a function of kit state | **WIDEN** → **L-09 `footprint_source`** {`static-measured` (GD default) \| `kit-state-driven`}. This is the cleanest case on the slate of an *internal* counter that the boundary must read every tick |
| 4 | **Movement penalty while channelling** — `cyclone_movement_speed_+%_final = -30` | `gems.json` (DATAMINED, exact) | BOUNDARY (§ 6 addition) | `channel_policy` **measures** movement (`REF_FRAC_MOVING_AT_RELEASE 0.402`, `REF_P_CHANNEL_GIVEN_STATIONARY 0.7376`) but carries **no move-speed modifier term** on the channel; GD's EoR moves at full speed | **WIDEN** → **L-10 `channel_move_speed_pct`** (GD default `100`; Cyclone `70`). Load-bearing for engagement and therefore for threat intake |
| 5 | `cyclone_first_hit_damage_+%_final = -50` | `gems.json` (DATAMINED) | **INTERNAL** | — | A per-hit damage modifier; native |
| 6 | Damage composition — `damage_effectiveness -56 → -41`, `damage_multiplier -5600 → -4100`, `attack_min/max_added_physical_damage` 5–8 → 28–42 | `gems.json` `per_level` (DATAMINED, exact) | **INTERNAL** | `channel.compose_damage_basis()` | Native. ⚑ **Docket 176 is live against this row:** the *shape* is DATAMINED and the *magnitude* is not — base weapon DPS at the 3.15 build point is un-harvested. See § 7.3 |
| 7 | Mana cost per use (`static.costs`) | `gems.json` (DATAMINED) | **INTERNAL** | `energy.EnergyModel` | Native |
| 8 | Leech / Slayer **overleech** (leech continues at full life) | dossier `capstone_alterations`, overgear (attested) | **INTERNAL** · reads `damage_applied` | `player_sustain` ADCtH | AS-IS on the read |
| 9 | **Fortify** — a flat "% less damage taken" buff maintained by melee hits | dossier `skill_loop` + verify 78 (attested) | BOUNDARY (mitigation order) | `threat.mitigate` exposes **additive** `resist_bonus_pct` / `max_resist_bonus_pct` (Resilience's `defensivePhysical +4 %`, `defensiveAllMaxResist +2 %`) and `intake.PclLimb`. There is **no generic multiplicative damage-taken term** in `physical_applied` (armour branch × resist multiply) | **WIDEN** → **L-11 `generic_damage_taken_mult`**, *and its position in the order*. ⚑ This is exactly the mitigation-order question Matt named, arriving with a foreign operand rather than a GD fork |
| 10 | **Knockback** — quality grants `base_global_chance_to_knockback_%` | `gems.json` `quality_stats` (DATAMINED) | BOUNDARY (status on monsters) | `control_application.control_type_enum()` is a **census parsed from D-7** (Stun, Sleep, Trap, Immobilize, Knockdown, Freeze, Petrify …). `control_states.load_control_rows()` **RAISES `UnknownControlFamilyError`** on a family outside the enum — *"a new member means the table changed… Re-census deliberately — do not bucket."* | **WIDEN** → **L-12 `control_family_registry`** (the enum must become extensible per-game without discarding its GD census). ⚑ And a deeper gap: knockback is **positional displacement**, which GD models nowhere. See § 7.1 |
| 11 | Hit resolution — PoE accuracy-vs-evasion | community model (MODEL-VERIFIED); **not** in RePoE | BOUNDARY | `probability_to_hit(oa, da)` | **AS-IS with measured cost** (see below), floor/ceiling via **L-04/L-05** |
| 12 | Armour — PoE's diminishing curve `armour / (armour + 5 × damage)` | community model (MODEL-VERIFIED) | BOUNDARY (mitigation) | `intake.armour_branch` — GD's two-branch `DLEP` / `DGP` from `combatformulas.dbr`, character for character | **AS-IS with measured cost, NOT a widening.** Cyclone *resolves* under GD's armour curve; what changes is its margin. Per **E-1** that distance is the thing to **measure and record**, not to legislate away. Marking this WIDEN would be Q86 misapplied — the interaction is expressible, the *number* moves |
| 13 | `weapon_restrictions` — 14 legal base types | `gems.json` (DATAMINED) | **OUT-OF-ARENA** | — | § 7.2 — a build-construction legality rule, not a fight rule |

**PoE1 Cyclone — INTERNAL 5** (2, 5, 6, 7, 8) · **BOUNDARY 7** (1, 3, 4, 9, 10, 11, 12 — of which **AS-IS 3**: 1, 11, 12 (12 AS-IS **with measured E-1 cost**); **WIDEN 4**: 3, 4, 9, 10) · **OUT-OF-ARENA 1** (13). **13 rows.**

---

## 4 · PoE2 Bonestorm — `poe2-bonestorm`

**Corpus:** T1 / moderate / eras `0.1;0.2-dawn;0.5-ancients`; `grade = **CLOSE**` with a stated deviation (Bone Cage's shape is "a reasonable-but-thin inference"); 6 dossier rows (1 abstained); `verify_ledger` 355–357 + 2506 CONFIRMED, **2507 UNSUPPORTED / `anchor_lint = ANCHOR_WEAK`**; 0 dockets.
**Fidelity ceiling: attested.** No PoE2 datamine lane exists.

| # | Mechanism | Evidence (grade) | Class | GD's rule | Verdict |
|---|---|---|---|---|---|
| 1 | Channel accumulates a **bone-shard charge count**; release fires the full barrage | poe2db verbatim, verify 356 + 2506 CONFIRMED (attested); mapping `charge_stack_sub_shape: accumulator` | **INTERNAL** | — | Native — and **the same primitive as Cyclone's stages** (§ 3 row 2). Two games, one internal accumulator |
| 2 | **Channel emits nothing until release** — a charge-then-burst channel | same anchor (attested) | BOUNDARY (tick clock) | `channel.ChannelMachine` applies a `DamageTick` **per tick** from `FIRST_TICK_INDEX = 1`; `ChannelRun` has **no release event** | **WIDEN** → **L-13 `channel_emission_mode`** {`per-tick` (GD default) \| `on-release`} |
| 3 | **Multi-point physical projectile barrage**, projectiles explode on impact | verify 2506 CONFIRMED, `geometry_value = multi_projectile` (attested) | BOUNDARY (target selection) | ⚑ **The GD *data* has the fields** — `gd_num_projectiles`, `gd_skill_projectile_number/_maximum_number`, `gd_projectile_explosion_radius`, `gd_projectile_fragments_launch_number_min/_max`, `gd_projectile_period` all live in `exact_skill_field`. ⚑ **The GD *oracle* has no player-side projectile model**: `discrete_volley.py` is the **monster** volley lane | **GD-EMPTY** → **L-14 `player_projectile_model`**. The data/oracle split here is the sharpest single instance of § 0 finding 5 |
| 4 | **Impale** — shrapnel hits cause *subsequent* attack hits on those targets to deal extra damage (mapped `sunder`; a damage-taken amp window, **no DoT**) | poe2db verbatim, verify 356 (attested); mapping `trigger_grammar.mark_identity = "Impale (Shrapnel Impales enemies Hit)"`, `consequence_type = apply-mark` | BOUNDARY (status on monsters) | ⚑ Same split: `gd_offensive_total_resistance_reduction_absolute_min` / `…_percent_min` / `gd_offensive_total_damage_reduction_percent_min` exist **as data**; the oracle applies **no player debuff to any monster** | **GD-EMPTY** → **L-15 `monster_debuff_lane`**. § 7.1 |
| 5 | Crit archetype — independent crit chance × crit multiplier | dossier `skill_geometry` "physical-spell crit archetype… crit scaling for burst" (attested) | BOUNDARY | `resolve_hit` PTH-tiered crit | **WIDEN** → **L-06 `crit_model`** (second witness) |
| 6 | Mana-mid spend per cast | mapping `resource_economy.cost_scale` (attested) | **INTERNAL** | `energy.EnergyModel` | Native |
| 7 | Physical damage, element-neutral | verify 2506 + THE PHYSICAL RULE (attested) | BOUNDARY | `RESIST_PCT["Physical"] = 16.0`, armour applies | **AS-IS** |
| 8 | Physical-crit scalers (traits/affixes lane) | mapping `scaffold.traits_affixes` (attested) | **INTERNAL** | — | Native |
| 9 | **Bone Cage** — "defensive panic button"; mapped `placed_lane` + `root` | ⚑ `verify_ledger` **2507 UNSUPPORTED, `ANCHOR_WEAK`**: *"anchor entails no delivery class incl. assigned 'zone'"*; mapping itself says **LOW confidence** | BOUNDARY (control on monsters) **— but DO NOT CENSUS IT** | `control_type_enum` has no `Root`; nearest is `Immobilize`, whose player-side resist is **`None` by decode** (`D7-N-02`: *no such stat exists*) | **HELD — insufficient evidence.** Censusing a root from an anchor that says only "defensive panic button" would put an invented mechanism into the lever registry. Re-entry criterion: a poe2db skill-page anchor that names the effect. ⚑ This is the correct handling of a thin row, not a gap in the census |
| 10 | Blood Mage variant: **spells cost life instead of mana** | dossier `variants` / `capstone_alterations` (attested) | **INTERNAL** under Q86 — **but collides with a standing ruling** | — | ⚑ `mechanic_gap_docket` **5** (`self-damage cast-cost redirected to a proxy's life pool`) is `matt-ratified` / **`permanent-gap-record`**. Q86 ("add every kit-internal mechanism natively") and that docket's `permanent-gap-record` disposition point opposite ways for the sibling shape. **Flagged for gandalf/knight-rider, not resolved here** — a ruling-vs-ruling question is above this seat |

**PoE2 Bonestorm — INTERNAL 4** (1, 6, 8, 10) · **BOUNDARY 5** (2, 3, 4, 5, 7 — of which **AS-IS 1**: 7; **WIDEN 2**: 2, 5; **GD-EMPTY 2**: 3, 4) · **HELD on insufficient evidence 1** (9). **10 rows**, plus a docket-collision flag carried on row 10 (§ 7.5).

---

## 5 · The cooldown-only kit — selection, with rationale

**Selected: `vs-gorgeous-moon` — Gorgeous Moon (Pentagram evolution), Vampire Survivors.** `grade = APPROX`; 6 dossier rows (3 abstained); `verify_ledger` 1926–1928 all CONFIRMED.

### 5.1 Why, and why not the other two

The slate needs a kit whose economy is cooldown-only **as an attested fact about a game**, not as a curation default about a missing field. Three candidates were surveyed against `corpus.db`; two fail that test on the corpus's own rows.

| Candidate | The cooldown-only claim | Verdict |
|---|---|---|
| `di-cyclone-strike-monk-base` (DI, CLOSE) | `fidelity_notes`: *"Spirit resource: verify_ledger mechanics **UNSUPPORTED**; cooldown used **per §D convention**"* | **Rejected.** The label is a **convention fallback over an absent field**. Censusing it would census a curation rule, not a game |
| `d4-blazing-abyss-warlock` (D4, CLOSE) | `resource_economy`: *"cooldown; Warlock = cooldown-only economy per §C.5 hot-fact"* — **but** its sibling `d4-dread-claws-warlock` records *"variants attests **'Wrath resource confirmed'** but §C.5 governs — cooldown-only framing applied per addendum"* | **Rejected.** The corpus's own rows **contradict** the class-level label. An internally contested row is the worst possible input to a boundary census |
| **`vs-gorgeous-moon` (VS, APPROX)** | `verify_ledger` 1927 **CONFIRMED**, verbatim anchor: *"A hardcoded limit of 15 seconds restricts cooldown reduction effectiveness"*; `item_alterations` states the **exclusion set positively**: *"only Cooldown stat affects weapon; Might/Speed/Area/Amount ignored"* | **Selected.** The only candidate where cooldown-only is a **positive attestation with a named mechanism and a named exclusion set**, uncontradicted elsewhere in the corpus |

Secondary reason, stated so it is not mistaken for the primary one: VS is also the most **structurally alien** kit available, which is what Q88's alien slot is for. Three of the other four kits on the slate are spin/channel melee; the slate needs one kit that shares almost nothing with the referent. Cost, named: the mapping grade is APPROX and the lane ceiling is attested, so **no VS row below may be graded above attested.**

### 5.2 The census

| # | Mechanism | Evidence (grade) | Class | GD's rule | Verdict |
|---|---|---|---|---|---|
| 1 | **Auto-fire; no player cast input at all** | game-structural, wiki (attested) | BOUNDARY (agency) | GD models a **deciding player**: `player_drive.py`, `action_permission.py`, `channel_policy` measures `REF_CAST_RATE_PER_S = 0.290` and `REF_P_CAST_INTERRUPTS = 0.15` | **GD-EMPTY** → **L-16 `agency_model`** {`player-driven` (GD default) \| `autonomous`}. GD's rule is "the player decides"; there is no setting for "nobody decides" |
| 2 | **Hardcoded 15 s cooldown floor**, non-reducible | verify 1927 CONFIRMED, verbatim (attested) | **INTERNAL** (a clamp on a cooldown) | Cooldowns **do** exist GD-side: `channel.cooldown_s` (EoR), `counterplay.py` runs defensive actives **greedy on-cooldown** with measured `cooldown_s` per record | **AS-IS.** ⚑ Useful negative result: a cooldown-only economy needs **no new boundary primitive** — GD already has a cooldown clock. The alien slot's headline risk did not materialise |
| 3 | **Damage equal to the enemy's max HP** (an execute) | dossier `skill_loop` `"damage": "deals damage equal to max health of enemy"` (attested) | BOUNDARY | `threat.mitigate(damage: float, …)` takes an absolute; proportional damage exists only on **intake** (`PclLimb`) | **WIDEN** → **L-07 `proportional_damage_offense`** at `pct-max` (second witness, with D2 Crushing Blow) + **L-08 `proportional_damage_mitigable`** — an execute entering `mitigate` would be multiplied by a resistance, and nothing states whether it should be |
| 4 | **100 % screen coverage**; the Area stat is locked out | dossier `skill_geometry` (attested) | BOUNDARY (target selection) | target multiplicity | **AS-IS** — "all engaged bodies" is the limit case of a multiplicity the form already carries. ⚑ The *consequence* is an **E-1 balance-threshold** matter, not a boundary one: against the arena's `opposition.ENGAGED_WINDOW_EHP_TOTAL = 13,981,477` at wave 160, a screen-clear is wave-terminating. Correctly E-1's problem, and naming it here keeps it out of the lever registry |
| 5 | **No hit roll, no resistances, no armour** — VS has none of these | game-structural (attested) | BOUNDARY (hit resolution) — **by declining it** | `resolve_hit(pth, roll)`: at `PTH ≥ 135` the roll always lands **and the crit multiplier is forced to 1.5** (`PTH_MULTIPLIERS[5]`) | ⚑ **WIDEN → L-06 `crit_model`, third witness, and the sharpest one.** "Always hit" and "never crit" are **not independently settable** in GD's rule, because `resolve_hit` derives both from one PTH and one roll. A kit that simply always hits cannot be expressed. **This is the finding that promotes `crit_model` to the slate's top lever** |
| 6 | On-kill cascade; 0 % item-destruction on erase | dossier (attested); mapping `t4_doors: GEOMETRY_PROPAGATION_cascade` | **INTERNAL** (on-kill trigger) · reads the boundary's `kill` event | `devotion.proc_damage_events()`, `sustain_procs` — trigger/proc machinery exists | **AS-IS** on the read |
| 7 | Simultaneous **gem vacuum** / XP harvest | verify 1926 CONFIRMED (attested) | **OUT-OF-ARENA** | — | § 7.2. Consistent with `mechanic_gap_docket` **13** `loot-economy-identity` → `permanent-out-of-scope` |
| 8 | Evolution recipe: Pentagram + Crown | verify 1926 (attested) | **OUT-OF-ARENA** (build construction) | — | Folded into row 7's class; not counted twice |
| 9 | `+XP gain per level` from the Crown catalyst | dossier `item_alterations` (attested) | **INTERNAL** (a scaler) | — | Native |

**VS Gorgeous Moon — INTERNAL 3** (2, 6, 9) · **BOUNDARY 4** (1, 3, 4, 5 — of which **AS-IS 1**: 4; **WIDEN 2**: 3, 5; **GD-EMPTY 1**: 1) · **OUT-OF-ARENA 2** (7, 8). **9 rows.**

---

## 6 · Refining Matt's boundary list — three additions, on evidence

Matt's list: *hit resolution · damage type vs resistance · mitigation order · CC/status applied to monsters · the tick clock* — **all five confirmed**, each exercised by at least two kits on the slate. The ruling invited refinement "if the evidence says otherwise". It does, in three places. The test used: **a question is boundary if two foreign kits cannot be adjudicated against each other without one shared answer to it.**

| Addition | Why it is boundary, not internal | Witnesses |
|---|---|---|
| **B6 · Target selection / multiplicity** | How many bodies a packet reaches is a property of the **world**, not the kit. Cyclone's footprint is driven by an internal counter (`+1 melee range per stage`, `+8 % AoE per range`); Bonestorm's is a projectile count; VS's is the whole screen; WW's is a path swath. Without one rule they cannot be compared at all — and GD's answer today is a **measured constant** (`pm4l_target_multiplicity.csv`), i.e. an operand, not a rule | all 4 |
| **B7 · Movement ↔ engagement coupling during an action** | Whether you may move while acting, and how fast, decides engagement, which decides threat intake, which decides the fight. Cyclone carries an **exact DATAMINED** `-30 %`; D2 WW and GD EoR move at full speed; Bonestorm's channel is rooted-adjacent. GD **measures** movement (`channel_policy.MovementWrap`, `frac_moving`) but exposes **no modifier term** | 3 of 4 |
| **B8 · The damage-family registry itself** (not only the resistance values) | `threat.mitigate` **raises `KeyError`** on an unmapped family — GL-12, by design: *"a silently-unresisted family is exactly how an invented number gets into a fight model."* So the **enumeration** of families is a shared rule with teeth. GD's set is Physical / Pierce / Fire / Cold / Lightning / Poison / Acid / Aether / Chaos / Life / Bleeding (+ `Slow*` DoT limbs). D2's `EType = mag` (magic damage) and PoE's Chaos-vs-GD-Chaos alignment are unmapped; **the next non-physical foreign kit HALTS the boundary** | structural; all four slate kits are physical, so **none of them triggers it — which is why it must be named now** |

⚑ **The last row is the census's most actionable warning.** The Q88 slate is *four physical kits*. It therefore exercises the damage-family registry not at all, and a reader could conclude the registry is fine. It is not: it is a loaded refusal that the slate happens not to touch. **Recommendation to the conductor: kit #3 in Phase B5 should be non-physical**, so the registry is tested before the adapter is built on the assumption that it passes.

---

## 7 · Mechanisms that do not fit the INTERNAL / BOUNDARY split

Per the dispatch: these are findings, not things to force.

### 7.1 · BOUNDARY / GD-EMPTY — a required third verdict

Q86's sort assumes every boundary item has a GD rule to default to, and that widening means *broadening* one. **Three boundary items have no GD rule at all.**

| Item | The evidence that GD is empty, not narrow | Consequence |
|---|---|---|
| **CC / status applied to monsters** — the item Matt named explicitly | `control_application.py` is entirely the **player-as-victim** lane: `player_control_resists()`, `suppression_matrix()` over `ControllerPlayerState*` vtables, `STATE_OF_FAMILY` mapping five player states. `control_states.player_control_applications()` docstring: **"The player's own control applications… Exactly one."** — a single dash rider. There is **no monster control-resist table, no monster CC-duration model, no diminishing returns** | "GD's rule as default" is **vacuous** for the one boundary item most kits actually use. PoE1 knockback, PoE2 Impale, PoE2 Bone Cage all land here |
| **Player-side projectiles** | `discrete_volley.py` is the **monster** volley lane. GD's `.arz` **data** carries the projectile vocabulary (`gd_num_projectiles`, `gd_projectile_explosion_radius`, `gd_projectile_fragments_launch_number_*`, `gd_projectile_period`) — the **oracle** does not model it, because REFERENT-v1's kit is a cone channel | Bonestorm cannot join at all until this is built. **A B5 blocker, not a lever** |
| **Player agency** | `player_drive.py` / `action_permission.py` presume a deciding player; `channel_policy` measures his cast rate and interrupt rate | An autonomous kit has no representation |

**Recommendation:** the lever-registry schema (architect § 3) should carry `status = OPEN` **plus** a `gd_referent_value` that can be **`NONE — no GD rule`**, distinct from a GD value that happens to be zero. A registry that cannot say "GD is silent here" will launder silence into a default, which is the failure the `RESIST_PCT` `KeyError` already guards against one level down. ⚑ **The oracle's own discipline is the precedent: refuse loudly rather than default quietly.**

### 7.2 · OUT-OF-ARENA — a third bucket, five instances, four kits

D2 weapon durability · PoE1 `weapon_restrictions` · VS gem vacuum · VS evolution recipe · (and D2 Battle Orders' loot-irrelevant stamina term). Each is **kit-defining in its home game** and has **no fight-boundary meaning whatsoever**. They are not INTERNAL (adding them natively adds nothing an arena can observe) and not BOUNDARY (no rule would help). **Four of four kits produced at least one. That is a class, not an accident** — and the corpus already ruled its largest instance out of scope (`mechanic_gap_docket` **13** `loot-economy-identity` → `permanent-out-of-scope`). Proposal: `OUT-OF-ARENA` as an explicit third value wherever the census is eventually materialised, so that "not censused" and "censused and excluded" stay distinguishable.

### 7.3 · Value-gaps are invisible to the sort

`mechanic_gap_docket` **176** (`poe1_cyclone_base_weapon_dps_build_point_gap`, status `open`): Cyclone's per-hit base is `weapon_DPS × 59 % effectiveness × 3.0 attack speed`, and the weapon DPS at the 3.15 build point **is un-harvested**. The mechanism is DATAMINED; the magnitude is missing. **INTERNAL/BOUNDARY cannot see this** — the row sorts cleanly as INTERNAL and is still unusable. A census row needs `mechanism_grade` **and** `magnitude_grade` as separate columns. Same shape, different lane: the whole PoE2 kit (§ 4) has no numbers at all.

### 7.4 · World-shape facts

D2 Battle Orders projects to **allies**; the engine is solo. Not INTERNAL (there is no ally to add it to), not BOUNDARY (no rule helps). It is a fact about the **shape of the world the boundary presumes**. Already ruled — dockets **2** and **12**, `permanent-gap-record`. No new docket owed; named so the census is not read as having missed it.

### 7.5 · A ruling-vs-ruling collision, escalated not resolved

PoE2 Blood Mage's life-for-mana substitution (§ 4 row 10) is INTERNAL under Q86 — *"add all of the mechanisms into the game."* Docket **5**, `matt-ratified`, disposes of the sibling shape as **`permanent-gap-record`**. Both are standing rulings and they point opposite ways. **Routed to gandalf / knight-rider; above this seat.** The same tension will recur for dockets **1, 3, 4, 7, 8** (all `engine-design-intake`) and for the `§5.2` family rows **9–19**: Q86 may have **re-opened a set of docket dispositions that were closed under the pre-union architecture.** ⚑ That is worth a deliberate sweep before B3 seeds the lever registry, because the registry will otherwise inherit whichever answer happens to be read first.

---

## 8 · GD-SLICE template lock — state, and whether `is_core` survives

**Reference:** `research/curated/MIGRATION-gd-slice-exact-fields-2026-07-24.md`. All figures below queried read-only from `corpus.db` this lap.

### 8.1 · State

| | |
|---|---|
| **Template lock** | **NEVER LANDED.** Architect pass § 2 states it; confirmed against the DB — no lock artifact, no `corpus_schema_meta` row naming one. `MIGRATION-gd-slice-exact-fields-2026-07-24.md` remains the last documented word on the shape. Architect § 5 carries it as **TL, GATED+TRACKED**, criterion "B0 + B1 results" |
| **The documented shape is one migration stale** | `gd-devotion-payloads-2026-07-25` (applied 2026-07-26) **re-keyed `exact_skill`**: PK moved `kit_id` → **`entity_id`**, with mandatory **`entity_kind`** ∈ {`corpus_kit`, `game_skill`} and mandatory **`rank_axis`** ∈ {`bought_rank`, `skill_xp_level`, `none`}; added `fidelity_grade`, `fidelity_basis`, `lane`. Pre-devotion snapshots preserved as `exact_skill_pre_devotion_20260725` / `exact_skill_field_pre_devotion_20260725` (park-not-delete, correctly) |
| **Current census** | `exact_skill` **675** headers — **1** `corpus_kit` (FoI, `bought_rank`) + **674** `game_skill` (devotion; 605 `rank_axis=none`, 69 `skill_xp_level`). `exact_skill_field` **7,250** rows (136 at the 07-24 version + 7,114 at the devotion version) |
| ⚑ **A grade-vocabulary defect, 675 rows** | **All 675 headers carry `fidelity_grade = MEASURED` with `fidelity_basis = primary-source-datamine`.** Per the era-substrate LAW § 4, a pinned primary-source extraction is **DATAMINED**; **MEASURED** is reserved for live-oracle behavioural verification — the term was minted on 2026-07-25 precisely because the LAW's original three had no word for this. `.arz` records attest **authored data, not runtime behaviour**. This is the architect pass's **GV** fork with a concrete instance and a row count. **Not fixed this lap** (read-only); recorded so GV opens against evidence rather than against a recollection |

### 8.2 · Does the `is_core` split survive the union ruling? **No — and it had already stopped meaning what the note says, before the ruling.**

**Reason 1 — empirical drift, measured.** The note defines `is_core = 1` as *"game-agnostic core"* and `is_core = 0` as *"per-game extension"*. The 07-24 slice honoured that exactly: **107 core / 29 extension over 11 keys, every one vocabulary-neutral** — core `damage_fire_min/max`, `weapon_damage_pct`, `cast_cadence_ms`, `cooldown_sec`, `cost_resource`, `range_max`; extension `cone_start_width`, `cone_end_width`, `burn_duration_sec`, `damage_fire_burn_dot`.

The devotion lap then landed this:

| schema_version | `is_core` | key vocabulary | distinct keys | rows |
|---|---|---|---|---|
| `gd-slice-exact-fields-2026-07-24` | 1 | neutral | 7 | 107 |
| `gd-slice-exact-fields-2026-07-24` | 0 | neutral | 4 | 29 |
| `gd-devotion-payloads-2026-07-25` | 1 | **`gd_`-prefixed** | **169** | **3,232** |
| `gd-devotion-payloads-2026-07-25` | 1 | neutral | 27 | 2,231 |
| `gd-devotion-payloads-2026-07-25` | 0 | `gd_`-prefixed | 82 | 1,651 |

**169 distinct keys whose names begin `gd_` are flagged `is_core = 1`** — `gd_defensive_petrify`, `gd_wave_start_width`, `gd_offensive_slow_bleeding_modifier`, `gd_projectile_fragments_launch_number_max`. **A key that carries its game in its own name cannot be the game-agnostic core the note defines.** The flag now separates something else — decoded-vs-qualifier, roughly — and **only 27 of 196 core keys are vocabulary-neutral.** The split drifted **before Q86 existed**; the ruling did not break it, it found it broken.

**Reason 2 — the ruling deletes the concept the flag names.** TSR-2's core/extension split exists to define the ONE normalized schema every kit is squeezed through; the first adapter proves it, the next adds its own `is_core = 0` rows. **Q86 rules that no such schema exists at the kit-internal layer:** every game's mechanisms enter **natively, as a union**, and the shared thing is the **boundary rulebook**, not a common field set. `is_core` is the surviving artifact of a retired abstraction. ⚑ Note what *does* survive intact: the note's **`canon_key` ↔ `raw_field` two-column mapping**, which is the reversibility law and is orthogonal to the union ruling. The union costs us the *core/extension* axis, not the provenance axis.

### 8.3 · Steward recommendation (no write this lap)

1. **Do not take the template lock against the current shape.** It would freeze `is_core` at a meaning the data left 3,232 rows ago, and TL's own re-entry criterion is "B0 + B1 results" — B1's paper census is this note, and its result is *the shape is not ready to lock*.
2. **Do not repair `is_core` in place and do not drop it.** Freeze it, documented as a pre-Q86 TSR-2 artifact. The project has two precedents for exactly this and both worked: `le-park-2026-07-24` (park, not delete) and `v1.1-deprecation-source_urls` (*"frozen, 60 rows preserved, NOT dropped… Do not read for truth"*).
3. **At the next schema lap, replace its role with two orthogonal, auditable columns** — neither of which asserts a cross-game abstraction the ruling has retired:
   - **`boundary_class`** ∈ {`internal`, `boundary`, `out_of_arena`} — the **Q86 sort**, per field. This is the column JOIN-1 actually needs and the one this census is the first input to.
   - **`vocab_scope`** ∈ {`neutral`, `game_named`} — **mechanically derivable today** from the key prefix, therefore auditable rather than asserted, and it would have caught the drift in § 8.2 automatically.
4. **Lock after `boundary_class` lands**, so that what is locked is the Q86 sort rather than its predecessor.

This is a recommendation under steward authority within the data domain; it proposes **no write, no DDL, and no ADR-004 cross-seam request** this lap. It requires a ruling from the JOIN-1 charter before any of it fires.

---

## 9 · Candidate levers — the full list, all OPEN, all at their GD-referent setting

Per architect § 3: levers are **discovered, never authored by hand** (Discipline #41). These are discovered from the B1 schema-pressure census — the third of the three legitimate sources, beside the KC2 divergence register and the ablation map. **None is proposed as SET; none has a feel-sensitivity row yet** (that is the ablation map's output), so every `load_class` below is **UNMEASURED**.

| Lever | Concept | GD-referent setting | Witnesses | Status |
|---|---|---|---|---|
| **L-01** `tick_quantisation` | action cadence | `continuous-as-proportional` (`0.16 × 100/AS%`) | D2 | OPEN |
| **L-02** `packets_per_tick` | source compositions per action tick | `1` | D2 | OPEN |
| **L-03** `max_hp_change_policy` | current HP when max HP moves | *no GD rule* — Ascension is flat | D2 | OPEN |
| **L-04** `pth_floor_pct` | hit-chance floor | `55.0` | D2, PoE1 | OPEN |
| **L-05** `pth_ceiling_pct` | hit-chance ceiling | unbounded | D2, PoE1 | OPEN |
| **L-06 ⚑** `crit_model` | crit independent of the hit roll? | `pth-tiered` (welded) | **D2, PoE2, VS** | OPEN — **top of the list** |
| **L-07 ⚑** `proportional_damage_offense` | %current / %max HP dealt by the player | `off` | **D2, VS** | OPEN |
| **L-08** `proportional_damage_mitigable` | does a proportional packet take resistance? | undefined | D2, VS | OPEN |
| **L-09** `footprint_source` | hit footprint from kit state? | `static-measured` | PoE1 | OPEN |
| **L-10** `channel_move_speed_pct` | move speed while channelling | `100` | PoE1 | OPEN |
| **L-11** `generic_damage_taken_mult` | flat % less damage taken, **and its position in the order** | *no generic term* — additive resist hooks only | PoE1 | OPEN |
| **L-12** `control_family_registry` | extensible CC family enum | D-7 census, **raises on unknown** | PoE1 | OPEN |
| **L-13** `channel_emission_mode` | per-tick vs on-release | `per-tick` | PoE2 | OPEN |
| **L-14** `player_projectile_model` | ⚑ **GD-EMPTY** | *none* | PoE2 | OPEN — **B5 blocker** |
| **L-15** `monster_debuff_lane` | ⚑ **GD-EMPTY** | *none* | PoE2 | OPEN — **B5 blocker** |
| **L-16** `agency_model` | ⚑ **GD-EMPTY** | `player-driven` | VS | OPEN |

**Two of these are not levers but build items** (L-14, L-15): a lever parameterises an existing mechanism, and there is no mechanism to parameterise. Recorded in the same table so nothing is lost, flagged so B3 does not seed the registry with two rows that cannot be set.

---

## 10 · What this note does and does not claim

**Claims.** That these 49 mechanisms are what the four kits depend on, at the fidelity grades named per row; that the GD oracle's rules are as cited; that `is_core` has drifted by the row counts in § 8.2; that the fourteen settable levers above are discovered from schema pressure rather than authored.

**Does not claim.** That the list is complete — a paper census over `.txt`/`.json`/attested prose finds what the sources say, and PoE2's sources say very little. That any lever should move. That any GD rule is wrong. That the AS-IS verdicts mean a second kit could *run* today: § 0 finding 5 says the operands are welded to one character, and B0's self-join is the test that will say how much that costs.

**What would falsify the headline findings.** L-06: a reading of `resolve_hit` in which crit tier and hit are separable — they are not, both derive from `p` and `roll`. L-14/L-15 (GD-EMPTY): a player-side projectile or monster-debuff body anywhere in `kc2/` — `grep` over 58 modules found the volley lane on the monster side and the control lane on the player-as-victim side only. § 8.2: a re-reading of `is_core` under which a key named `gd_defensive_petrify` is game-agnostic.

**Deferred, with the criterion that gates re-entry.**
- Materialising this census as a table in `corpus.db` — gated on the JOIN-1 charter and on the `boundary_class` column decision (§ 8.3). **Not this lap; no schema change.**
- PoE2 Bone Cage (§ 4 row 9) — gated on a poe2db anchor that names the effect.
- The docket-disposition sweep against Q86 (§ 7.5) — gated on a gandalf/knight-rider ruling; must land **before B3** seeds the registry.
- The GV grade-vocabulary fix on 675 `exact_skill` rows (§ 8.1) — gated on GV opening at B2, jack-ryan's seam.

**Signed:** elrond (data steward and archivist), 2026-09-28. Seat W1, KC2-PLAY SEAL LAP. Zero code; read-only on every store touched.

---

## 11 · Named finding (forward, 2026-10-01): the D2 WW Barbarian gains two rows, 14 → 16

**Source:** jack-ryan, Sorceress-census Gate-2, A-4 + W3 (`qa/findings/2026-10-01-join1-j0-sorceress-census-gate2.md`, collab `b48500a4d`; charter v0.5.1; KP-165). It was raised by this seat as ambiguity A-4 in `2026-10-01-join1-j0-sorceress-census.md`. **This is an addition after the launch anchor, so it is a named finding (charter § 4.5), printed against J-S2 with its reason. It is not a silent re-map.** It makes his coverage harder, not easier, and it lands before J4a is graded.

**Both rows were omitted by this census (§ 2). Neither changes any existing row's class.**

| # | Mechanism | Evidence (grade) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| **B-15** | **His hits put monsters into hit recovery** (stagger). WW's melee hits trigger D2 monster hit recovery by engine law. WW carries no `Skills.txt` field for it (unlike the Sorceress's `GetHit=1` missiles) | MV (D2 engine law; legolas) | **BOUNDARY** (CC/status on monsters) | `control_application` is the player-as-victim lane only (§ 7.1): no monster control body. GD's engine has `TakeHitAction` (enum type 11), but the oracle has nothing to apply it to | **GD-EMPTY → L-21 `monster_hit_recovery`** (build item, registered at the Sorceress Gate-2; BUILD-IN-J4b under KP-162) |
| **B-16** | **His own hit recovery: the Battle Orders cast is interruptible.** Battle Orders (149, pinned in J-S3) carries **`interrupt=1`**; Whirlwind's `interrupt` is empty, so the spin itself is uninterruptible but the buff cast is not. legolas's timing packet (`b0f9d77fa`) tables his FHR (`BA GH 5/256`) | **DM** (`Skills.txt` `interrupt=1` on 149, re-verified 2026-10-01) / MV (D2 FHR law) | **BOUNDARY** (CC/status on the player; B7) | The player-control lane is triggered by control families, not by damage. `REF_P_CAST_INTERRUPTS = 0.15` is the player cutting his own channel. GD's referent is `NONE` (trigger undecoded; the decoded permission grid has TakeHit REPLACE Attack) | **WIDEN → L-18 `player_hit_recovery`** (settable; GD `NONE`, DECLARED-INVENTED JOIN default `off`) |

**Why the census missed them.** B-16: the § 2 row list read Battle Orders for its buff (row 7) and never read its `interrupt` flag. B-15: the census enumerated the kit's own records, and monster hit recovery from melee is an engine law with no field on WW. The Sorceress census found both shapes from her own `GetHit=1` and `interrupt=1` fields. Paper-only note (Gate-2): the same universal hit consequence (PoE stun on hit) is probably missing from the Cyclone and Bonestorm rows too. No JOIN-1 action follows; it is recorded for whichever run joins them.

**D2 WW Barb, corrected frozen record: 16 rows.**

| Class | Count | Rows |
|---|---|---|
| INTERNAL | 3 | 5, 6, 7 |
| **BOUNDARY** | **11** | **AS-IS 3**: 1, 4, 12 · **WIDEN 7**: 2, 3, 8, 9, 10, 11, B-16 · **GD-EMPTY 1**: B-15 |
| OUT-OF-ARENA | 2 | 13, and the ally-scope row |

**Fraction-(b) population: 11** (all BOUNDARY rows, per Gate-2 W2). **Fraction-(a) denominator: 16.**

**Slate totals, derived (for the record; J-S2 is the conductor's to amend):** 48 classed rows (it was 46) + 3 cross-cutting misfits = 51. INTERNAL 15 · BOUNDARY 27 (AS-IS 8 · WIDEN 15 · GD-EMPTY 4) · OUT-OF-ARENA 5 · HELD 1.

*Named finding signed:* elrond, 2026-10-01.
