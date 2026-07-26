# GD Player-Side Surface-Fit Mapping — the design half of G-5

**Author:** gandalf (named sub-agent, SPEC-AUTHOR piece) · **Commissioned by:** gandalf-prime, 2026-07-25
**Type:** DESIGN MAPPING — research + verdicts. No production code. No corpus writes (read-only `?mode=ro`).
**Input of record:** `agentic_orchestration/elrond/notes/2026-07-25-gd-player-mechanism-census.md`
**Governing rulings (Matt, 2026-07-25):** G-5 fit-or-extend · triage-by-kit-count · G-3 hard-CC built ·
era-substrate architecture (`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md`)
**Status:** DRAFT FOR gandalf-prime. §4 forks are Matt's, not mine — I state leans, I do not rule.

---

## §0 — What this document is, and the law it runs under

G-5 says a GD character **re-instantiates into our engine's native mechanic surfaces.** Smash Bros
does not import Mario's stat deltas; it rebuilds Mario out of one physics engine's verbs. So the
question per mechanism is never "how faithfully can we approximate this" — it is **"which native
surface carries it, and if none does, what surface must exist."** A missing carrier is a BUILD ITEM
on our mechanic surfaces. It is never a fidelity caveat.

Three handling rules I inherited and held:

1. **Delivery reads from the §4.1 CONSOLIDATED table (10 shapes), not the 89 raw rows.** Three
   typed vocabularies (`delivery_class` / `geometry_value` / `motion_signature`) describe the same
   73 skill rows; counting them separately triples a delivery mechanism's apparent weight.
2. **The hard-CC zeros (#88 P-STUN / #89 P-FREEZE) are FIREWALLED.** They are an extraction-policy
   artifact — the curation lane admits a status only when a fetched anchor NAMES it, and build-guide
   prose says "cold shards," not "applies Freeze." GD has stun and freeze; elrond's own monster-side
   `.arz` census found `offensiveStun*` on 19 player-class records. **No triage runs on those zeros.**
   Both are already BUILT engine-side (`config/ailments.yaml` — `freeze`/`stun`, `hard_control`) per
   the ailment-layer wave and today's G-3 control-payload ruling. Annotated, never triaged.
3. **Singleton caution.** Before tagging any kit-count-1 mechanism as re-entry, I checked deviation
   prose and the cross-program `mint_ledger`. This caught two — §2.3 documents both.

**Fidelity-grade discipline on my own verdicts.** Every surface I cite is labeled **BUILT** (code
exists and runs — file cited) or **SPEC-ONLY** (canon-ruled, not in the build). *A FIT against a
spec-only surface is a weaker claim than a FIT against a built one,* and I keep them apart the same
way elrond keeps MEASURED from PROSE. Sources of truth: `canonical/current-to-end-state/mechanical-reality.md`
(the Codex — what the engine can express, with state) plus direct code verification.

---

## §1 — The fit table

Verdicts: **FIT** = a native surface carries the mechanism faithfully · **PARTIAL** = the surface
exists but needs a named change · **GAP** = no surface; name what must exist.

### 1.1 — Delivery (consolidated per census §4.1)

Our delivery vocabulary is the **26-type `VALID_GEOMETRY_TYPES`** (`generation/geometry_derivation.py:44`,
BUILT — 24 pre-Wave-C + `orbit` + `placed_lane`), the 6-type spatial enum it translates into, and the
motion-frame family. This is the census's strongest region: **10 of 10 consolidated delivery shapes FIT.**

| Consolidated mechanism | kits | Native surface | State | Verdict |
|---|---:|---|---|---|
| Ground-placed persistent zone | **19** | `ground_targeted_circle` · `ground_slam` · `circle` · `ring`; zone persistence via `persistent-condition` econ bin; `ZONE_CONTROL` T4 (catalog 26th) | BUILT (`geometry_derivation.py:44`; `bc_target_composer.py:92`; `t4_catalog_v2.py:47`) | **FIT** |
| Projectile (multi / fan / fork / ricochet) | **16** | `multi_projectile` (+ `angle_distribution` ∈ spread/cardinal/diagonal/star), `fork`, `ricochet_bounce`, `line` (+ `collision_mode` pierce_all — carries G-PIERCE, 6 kits) | BUILT (`ability_schema.py:20-29` B11 param expansions) | **FIT** |
| Aura / persistent self-field | **13** | `aura` geometry × `reservation` econ bin (`reservation_percent` ≤0.75 LOCKED, `reservation_flat`, `reservation_resource`) + `persistent-condition` shapes {tick-cost, activation-toggle, proc-loop} | BUILT (Wave-B, engine `cec8f12..b850800`) | **FIT** |
| Placed autonomous proxy (totem/trap/turret) | **9** | `totem` geometry + `proxy-light`/`proxy-heavy` bins (`_DEFERRED_PROXY_BINS` drained to `frozenset()` at Wave-A) + `PROXY_TYPE_TIER` archetypes {STRIKER, BULWARK, BATTERY, TRIGGER, ATTENDANT, ECHO} | BUILT hosting + P1 (`proxy_vocabulary_bridge.py`); **behavior grammar SPEC-ONLY** (mechanical-reality §8: OPEN Matt thread) | **FIT** (placement/emission) · see §2 row for trap-arming |
| Melee strike / arc sweep | **8** | `melee_strike`, `melee_arc` (+ `sweep_shape` pie/crescent), `ground_slam` | BUILT | **FIT** |
| Motion-fused attack (dash/spin/blink/orbit) | **6** | `dash_attack`, `defensive_dash`, `blink`, `teleport`, `leap_strike`, `whirlwind`, `orbit` (+`orbit_anchor` ∈ caster/target/anchor-point, `orbit_projectile_count` ≤8) | BUILT (orbit landed Wave-C/D, engine `8d8bd26`); orbit per-tick WIRING = named Wave-E residue | **FIT** |
| Self-centred nova / burst | **5** | `circle` / `ring` at caster origin; motion-frame `burst_around_self` | BUILT | **FIT** |
| Chain / hop / spread to extra targets | **5** | `chain` geometry + chain-decay parameter (`_CHAIN_DEFAULT_DECAY=0.7`); contagion-on-spread rides `on-defender-death` proc trigger | BUILT for chain/hop; **contagion PARTIAL** (§2 row) | **FIT** (chain) |
| Pets & summons | **4** | delivery=SUMMON × `proxy_bin` × economy model (`reserve` upkeep / `cooldown` / `finite`); `proxy_decl_from_summon()` one-summon-one-decl bridge | BUILT emission + P1 hosting; **P2 nav/command SPEC-ONLY** | **PARTIAL** (§2 row) |
| Channelled beam | **3** | `beam_channel` geometry × commitment bin `channel` × economy `reserve` | geometry BUILT; **commitment emitter BUILT (`e4d682e`), sim consumption PHASE-2 QUEUED = SPEC-ONLY sim-side** | **PARTIAL** (§2 row) |

**Prose-family delivery riders (not folded into the consolidated 10):**

| # | Mechanism | kits | Surface | State | Verdict |
|---|---|---:|---|---|---|
| 25 | Default-attack replacer | 6 | Composition, not a new verb: `economy.model = free` × `cadence = spam` × `commit = instant` × melee/projectile geometry **is** a left-click replacer | BUILT (all four coordinates exist) | **FIT-by-composition** — flag: we have no *named* replacer slot, so the legibility ("this is your attack") is a presentation problem, not a mechanic gap |
| 33 | Movement lock while casting | 5 | Coordinate #1 `mob_policy_while_casting` ∈ FREE-MOVE·WALK·ROOTED (LOCKED, Q19) + E4 move-while-channel enum {rooted, walk, full_move} | key coord BUILT; E4 sim consumption **SPEC-ONLY** (PHASE-2 queued) | **PARTIAL** (rides the E4 row) |
| 46 | Affix that adds targets / projectiles | 3 | **none.** 79-modifier affix pool (`partition_modifier_pool.py`) has dmg/def/res/respen/spd/crit/trig/util families — **no count-modifying operator** | — | **GAP** (§2 build item) |
| 60 | Contagion / proximity spread between enemies | 2 | `on-defender-death` proc trigger + `linked-cast` consequence gets *death*-spread; **proximity**-spread has no trigger condition | trigger BUILT; proximity **GAP** | **PARTIAL** |
| 75 | Enemy-attached tether / beacon | 1 | `orbit_anchor = "target"` is the nearest primitive (an emitter anchored to an enemy) | BUILT | **FIT** (adjacent) |

### 1.2 — Cadence, commitment, ailments, triggers

| # | Mechanism | kits | Native surface | State | Verdict |
|---|---|---:|---|---|---|
| 3 | Cooldown-gated cadence | 17 | `economy.model = cooldown`; `cooldown_seconds` per skill; `cadence_scale` | BUILT | **FIT** |
| 22 | Spam cadence | 6 | `economy.model` spend/free × commit `instant` × high tempo | BUILT | **FIT** |
| 30 | Channel cadence | 5 | commitment bin `channel` | emitter BUILT, **sim SPEC-ONLY** | **PARTIAL** (E4 row) |
| 28 | Sap / weaken curse | 5 | `curse` ailment, sub-mode `sap` — a literal 1:1 name match | BUILT (`config/ailments.yaml:353`, category `debuff`) | **FIT** |
| 36/37/66 | Bleed · Burn · Poison DoT | 4/4/1 | `bleed`, `burn`, `poison` (poison = stack-additive, deliberately distinct from burn) | BUILT (ailment layer, engine `cec8f12`) | **FIT** |
| 52 | Drain (life/resource siphon) | 2 | `drain` ailment (dot, shadow) + `lifesteal` effect | BUILT (`damage_resolver.py:1190`) | **FIT** |
| 65/67 | Blind · Root | 1/1 | `blind` (accuracy-tax 0.20–0.60, soft_control) · `root` (hard_control) | BUILT | **FIT** |
| **88/89** | **Hard CC — stun · freeze** | **0 (POLICY-ZEROED)** | `stun` + `freeze` ailments, `hard_control` category, boss-resistance parameter, freeze→shatter execute-threshold | **BUILT** | **FIT — firewalled.** The census zero is an extraction artifact; G-3 ruled the control payload built. **Do not read "0%" as a GD fact and do not triage on it.** |
| 41/42/86/87 | Proc triggers: on-cast-linked · on-hit-threshold · on-damage-taken · on-defender-death | 4/4/1/1 | `PROC_TRIGGER_CONDITIONS` — all four are literal enum members | BUILT (`resource_economy.py:126`) | **FIT** |
| 27/51/85 | Proc consequences: burst-damage · linked-cast · resource-fill | 6/3/1 | `CONSEQUENCE_TYPES` — all three are literal enum members | BUILT | **FIT** |
| 83 | Swing-count accumulator (every-Nth) | 1 (real reach ≥2) | `charge_stack_sub_shape = accumulator` + `accumulator_fill_trigger = on-hit-dealt` + `accumulator_discharge_threshold` | BUILT (Wave-B) | **FIT** — *but see §2.3: the two-tier version is a ratified Tier-A mint* |
| 84 | Apply-then-consume pair | 1 | `TRIGGER_CHAIN_SHAPES = apply-consume-pair` + `MARK_IDENTITIES` + `mark_apply_event`/`mark_consume_event`/`mark_duration_seconds` (≤10s LOCKED) | BUILT (Wave-C) | **FIT** |
| 63 | Charge / stack accumulator meter | 2 | same accumulator machinery + `per_stack_passive_bonus` | BUILT | **FIT** |
| 82 | Contact-triggered placed trap | 1 | totem/`placed_lane` placement BUILT; **no proximity/contact arming condition** in `PROC_TRIGGER_CONDITIONS` | placement BUILT, arming **GAP** | **PARTIAL** |
| 81 | Explosion-on-death (proxy) | 1 | `on-defender-death` trigger BUILT; proxy-death→payload attribution boundary is a **RULING OWED** (mechanical-reality §8) | **PARTIAL** | **PARTIAL** |
| 2 | **Devotion / constellation proc binding** | **18** | Proc *machinery* exists (triggers + consequences + `trig_*` gear affixes). **The player-directed binding layer does not.** No skill-point / tree / bind surface anywhere in the engine (grep: zero `skill_rank`/`skill_points`/`passive_tree`). No `proc_chance`. No internal-cooldown field. | machinery BUILT, binding **GAP** | **PARTIAL → GAP at the binding layer.** **BUILD-TRIGGERED / SPEC-BLOCKED-ON-DATA** — payload void per census §5.1; elrond's `.arz` devotion probe is the unblock |
| 50 | Weapon-pool proc suite (WPS) | 3 | `on-hit-dealt`-class trigger + `linked-cast` consequence gives ONE deterministic linked cast; **a weighted pool of alternates, chances summing past 100%, is not expressible** (`MAX_CHAIN_DEPTH=1` LOCKED, no chance parameter) | **PARTIAL** | **PARTIAL** (§2 build item) |

### 1.3 — Buff / debuff / defense

| # | Mechanism | kits | Native surface | State | Verdict |
|---|---|---:|---|---|---|
| 5 | Resistance reduction (RR / shred) | 16 | Two carriers: `sunder` ailment (damage-amp `debuff`, ailment-layer §2 — the genre's #1 missing mechanic, now built) + `element_penetration`/`armor_penetration` gear affixes (0.0–0.75) | BUILT (`config/ailments.yaml:203`; `gear_instance_generator.py:68-69`) | **FIT on shape** · **PARTIAL on stacking** — GD's three RR classes (flat / -% / "reduced") have distinct stacking rules; we have single-source magnitudes and no stacking-class enum (§4 fork F4) |
| 16 | Life leech / ADCtH | 7 | `lifesteal` effect + `on_lifesteal` event; TH sub-shape `resource-fill`; LC `hp_cost_scale` for the paying half | BUILT | **FIT** |
| 21 | Healing / sustain zone or totem | 6 | `heal` + `heal_over_time` effects (`damage_resolver.py:1142/1158`) × zone geometry × `consecrate` ailment (`amplification` — a *valenced zone*, the exact primitive) | BUILT | **FIT** — note: in a solo game the ally-benefit half is thin by design (support gated to multi-actor contexts, standing decision) |
| 29 | Timed defensive cooldown / immunity window | 5 | Partial carriers only: `shield`/`absorb_with_shield` BUILT; dodge i-frames `dodge_iframes_seconds` (0.0–2.0) BUILT; **full skill-granted invulnerability window = B13 scope, explicitly not modeled** (`damage_resolver.py:1270`) | **PARTIAL** | **PARTIAL** (§2 build item) |
| 53 | Damage absorption / shield layer | 2 | `shield` ActiveEffect + `get_shield_total()` + `absorb_with_shield()` | BUILT (`combatant.py:434-437`) | **FIT** |
| 68 | Retaliation / damage-return (thorns) | 1 (3 if variant-lane counted) | `damage-taken-converts` econ bin (TH), sub-shapes {reflect-damage, resource-fill, **stack-fill** — the comment literally reads "D2 rage-on-damage / **GD retaliation** stack builder"}, `reflect_damage_fraction` ≤1.00 LOCKED, `reflect_scaling_stat` ∈ {thorns, defense, vitality}; and retaliation keys as a **def-bin rider** per coordinate-register §3A | **BUILT** (Wave-C) | **FIT** — **and this corrects a stale corpus row.** `kit_deviation` still marks `gd-retaliation-warlord` `engine_inexpressible` ("the absence IS the gap", docket 153). Wave-C's §6.3 TH roster names that exact kit. **The docket is stale; the gap closed.** Route to elrond for a deviation re-classify. |

### 1.4 — Gear-borne and resource

| # | Mechanism | kits | Native surface | State | Verdict |
|---|---|---:|---|---|---|
| 4 | Damage-type conversion (item/set/skill-mod granted) | 17 | `ELEMENT_CONVERSION_MONO` / `_HYBRID` / `_PHYSICAL` T4 capstones with LOCKED per-variant magnitudes (1.50 / 1.25 / 0.25) + the `element_application` binder's structure vocabulary | T4 **BUILT** (`t4_catalog_v2.py:31-33`, `damage_resolver.py:738-741`); binder **BUILT** (`db8e47f`, 2 of 7 walkers shipped) | **PARTIAL on carrier.** The *effect* is fully native — the census's own §7 appendix already assigns `ELEMENT_CONVERSION_*` doors to 14 GD kits. What differs is **who grants it**: GD's conversion is an item/set build-choice; ours is a rolled capstone. §4 fork F2. |
| 8 | Item-set threshold bonus as build enabler | 14 | `SetBonusDefinition` + `set_bonus` / `set_bonus_rank` fields, six-profile set architecture, `make_proxy_commander_set_bonus` | BUILT (`export/cycle14_wave5_emitter.py:509`) for stat-grade bonuses; **mechanic-granting thresholds ride the agnostic-loot operator model = SPEC-ONLY** (gates on batch-2) | **PARTIAL** |
| 26 | Cooldown reduction as a scaling lever | 6 | `spd_cooldown_reduction_epic` / `spd_cdr_accessory` affixes | BUILT (`partition_modifier_pool.py`) | **FIT** |
| 61 | Skill-granting item proc | 2 | `trig_on_*` affix family (on-kill / on-hit / on-crit / on-block / on-dodge / on-being-hit) exists and fires effects; **granting a whole named skill** rides the agnostic-loot structural-operator class | affix family BUILT; skill-grant **SPEC-ONLY** | **PARTIAL** — and constrained by the gear law's *import no one's core* clause |
| 20 | Transmuter / skill modifier that changes behaviour | 7 | Nearest carriers: trait pool (55 entries, `ability_modifier_key` — **L1 floor only**, L12/25/38 deferred) + T4 capstone transform declarations `(commitment_bin, amplitude_delta)` | traits BUILT (`config/traits/minimum_viable_pool.yaml`); **player-selected modifier layer GAP** | **PARTIAL** (§2 build item; couples to F1/F3) |
| 15 | Energy / mana economy pressure as build constraint | 8 | 9-value `ECON_BINS` + the 7-value economy-model key coordinate; `cost_scale`/`cost_slope`/`regen_shape` | BUILT (Wave-B) | **FIT** |
| 35 | Attack-speed / cast-speed as scaling lever | 5 | `spd_attack_speed` affixes ×3 | BUILT | **FIT** |
| 64 | Pet-scaling stat lane | 2 | Rides the summoner lane; docket 18 `gear-stat-as-minion-scaling` is a ratified `standing-family-record`, and docket 8 `attribute-value to proxy-count coupling` is `engine-design-intake` | **SPEC-ONLY** | **PARTIAL** (rides §2 pets row) |

### 1.5 — The structural absence that has no census row (census §5.3)

Elrond flagged **mastery-bar / tree topology** as the one place the corpus is not thin but *absent* —
"arguably the single most identity-forming player-side mechanism in the game." It carries no kit-count,
so it cannot be triaged; I record it because a G-5 mapping that ignored it would be dishonest.

**Verdict: NOT A GAP — it is out of the fit domain by construction, and that should be said aloud.**
Our model is a **pre-generated kit addressed by a 13-coordinate identity key** (`coordinate-register-2026-07-13.md`);
the player does not spend points into a mastery bar to *become* the build. GD's two-mastery point spend
is *how a player arrived at* a kit; G-5 converts the arrived-at character, not the arriving. The engine
has zero point-spend surface and, under the current key, wants none — build expression lives in
**soul-bound gear operators** (`agnostic-loot-engine-spec.md`, SPEC-ONLY) under the four-clause gear law.
This is close enough to an unstated assumption that I have surfaced it as confirm-fork **F3**.

---

## §2 — Gap register, triage applied

**The threshold (Matt, 2026-07-25):** kit-count ≥3 → BUILD ITEM · kit-count 1 (after prose check) →
RE-ENTRY TAG · kit-count 2 → judgment call, reasoning stated. Sorted descending.

Size classes: **S** = parameter/field on an existing surface · **M** = new vocabulary member + resolver
branch · **L** = new layer or architecture.

### 2.1 — BUILD ITEMS (kit-count ≥3)

| # | Build item | GD kits | Size | What must exist |
|---|---|---:|---|---|
| **B1** | **Proc CHANCE + INTERNAL COOLDOWN on the trigger surface** | **≥20** (devotion 18 ∪ WPS 3 ∪ item-proc 2, overlapping) | **S–M** | `resource_economy` carries `proc_trigger_condition` and `consequence_type` but **no chance parameter and no ICD** — every proc in our engine is deterministic. The genre is overwhelmingly chance-gated. Add `proc_chance` (0.0–1.0) + `proc_internal_cooldown_seconds` as a *pair*, with an ICD-required-above-a-threshold invariant. **This is the single highest-leverage item in the register** and it unblocks B2 mechanically. |
| **B2** | **Player-directed proc-binding layer (devotion-class)** | **18** | **L** | A surface where the player attaches a proc payload to a chosen skill with a trigger condition. Machinery (triggers, consequences, hook layer design note) is largely in place; the *binding + selection* layer is absent. **BUILD-TRIGGERED / SPEC-BLOCKED-ON-DATA** — kit-count clears any threshold, but the corpus holds ZERO devotion payloads (census §5.1). Do not spec until elrond's `.arz` devotion probe returns. Gated on F1. |
| **B3** | **Conversion as a gear/build-layer operator (beside the T4 capstone)** | **17** | **M** | The conversion *effect* is native and built. The build item is a second **carrier**: a structural gear operator granting conversion as a player build-choice, at capped-garnish potency, with the capstone retained at specialist grade. Rides `agnostic-loot-engine-spec.md`'s transform-operator class (equip-capped 2–3). Gated on F2. |
| **B4** | **Debuff stacking-class discipline (RR family)** | **16** | **S** | We have `sunder` and penetration affixes but no rule for what happens when three sources of resistance reduction land at once. GD's three RR classes stack by distinct rules; PoE's exposure/curse/pen do too. Add a small `stacking_class` enum on debuff-family ailments (e.g. `additive` / `highest-only` / `multiplicative-residual`). Cheap, and it is the difference between build-crafting depth and one flat number. Gated on F4. |
| **B5** | **Set threshold as a MECHANIC-granting operator (not only stat-granting)** | **14** | **M** | Set bonuses exist at stat grade. GD's build-enabling sets *change what a skill does* ("5pc → 50% chaos-to-fire"). Under the agnostic-loot spec this is a structural operator with an equip cap, governed by the gear law's *amplify your own · path texture to anyone · import no one's core · invent nothing.* Composes with B3 (conversion is the most common set payload). Gates on batch-2 close. |
| **B6** | **Player-selectable skill-modifier layer (transmuter-class)** | **7** | **M** | GD transmuters change a skill's behavior as a *choice*. Our trait pool has the right shape (`ability_modifier_key`) but is class-intrinsic and L1-floor-only. Either (a) extend traits to selectable ranks at the deferred L12/25/38 floors, or (b) express transmuters as gear structural operators. Couples tightly to F1 and F3 — if F1 resolves to "gear absorbs everything," B2/B6 collapse into one surface. |
| **B7** | **Timed invulnerability / defensive-cooldown window** | **5** | **S** | Shields and dodge i-frames exist; a *skill-granted timed invulnerability window* is explicitly B13-deferred (`damage_resolver.py:1270`). Five GD kits build around one (Mirror of Ereoctes, Mark of Torment). This is the ARPG "oh-shit button" and its absence is felt, not academic. |
| **B8** | **Weighted proc-POOL consequence (WPS-class)** | **3** | **S** | One deterministic `linked-cast` exists. Needed: a consequence that selects from a **weighted pool** of alternates, with pool chances allowed to exceed 100% (the GD WPS signature — at 100%+ every swing is a special). Rides B1's chance parameter; without B1 this item is not buildable. |
| **B9** | **Count-modifying gear operator (+targets / +projectiles)** | **3** | **S** | The 79-modifier affix pool has no operator that changes a skill's target or projectile *count*. `orbit_projectile_count` proves the sim can carry a count field. Needed: a value-class operator that reads it. |
| **B10** | **Two-tier accumulator** | **1 in GD; ~10 corpus-wide** | **M** | See §2.3 — this is a promoted singleton, already a **ratified Tier-A build-authorized mint** (`mint_ledger`, VDM-1 D-3). Listed here so the GD program does not re-derive it. |

### 2.2 — kit-count 2 — judgment calls

| Mechanism | kits | Ruling | Reasoning |
|---|---:|---|---|
| **P-CONTAGION** (proximity spread) | 2 | **RE-ENTRY TAG, not built now** | Death-spread already works via `on-defender-death`. What is missing is a *proximity* trigger condition — and proximity is the same primitive B8/traps need. Tag it and let it ride whichever of those fires first; building a proximity-trigger for two kits alone is scope leakage. |
| **P-ITEMPROC** (skill-granting item) | 2 | **FOLD into B1/B5** | Not its own item. It is B1's chance parameter plus B5's mechanic-granting operator, wearing an item name. |
| **P-PET-SCALE** | 2 | **FOLD into the pets lane** | Already carried: docket 18 (`gear-stat-as-minion-scaling`, standing-family-record) and docket 8 (`stat-as-army-size`, engine-design-intake). Do not mint a third record for it. |
| **P-ABSORB** / **P-STACKMETER** | 2 / 2 | **FIT — no item** | Both fully built (`shield` layer; accumulator sub-shape). |

### 2.3 — Singletons: the prose check, and what it caught

The census warned that kit-count 1 can mislead. It did — **twice**, in opposite directions.

- **T-ACCUM (swing-count accumulator, count 1).** Elrond's own §6 note flagged the hidden reach:
  `gd-krieg-death-knight` runs the same Cadence skill and asks for the same two-tier accumulator in
  prose without the typed field set — real reach 2. **And it goes further than that:** the
  cross-program `mint_ledger` already carries **two-tier accumulator as a ratified Tier-A
  (≥3-kit-attested) BUILD-AUTHORIZED mint at ~10 kits corpus-wide.** A GD-local reading would have
  tagged this as a singleton re-entry; the correct disposition is **B10, already authorized.**
  *This is the census's own caution paying for itself.*
- **P-RETAL (retaliation, count 1).** The opposite error was already latent in the substrate:
  `kit_deviation` marks `gd-retaliation-warlord` `engine_inexpressible` (docket 153), but Wave-C
  built the TH bin and its roster names that exact kit. **The gap closed; the record did not.**
  Verdict FIT + a re-classify routed to elrond.

**Genuine re-entry tags (build nothing now, named trigger for re-entry):**

| Mechanism | kits | Re-entry trigger |
|---|---:|---|
| P-TRAPTRIG (contact-armed trap) | 1 | PoE lane entry — traps are a whole PoE archetype; the proximity primitive should be designed once, against that population, not against one GD kit |
| P-DEATHNOVA (proxy explode-on-death) | 1 | The proxy behavior-grammar thread (mechanical-reality §8, OPEN Matt design thread) — the emitted-vs-proxy attribution ruling is already owed there |
| P-TETHER (enemy-attached beacon) | 1 | None needed — `orbit_anchor="target"` is close enough that this re-enters only if a future lane shows a real tether population |
| Pets/summons P2 (nav + command) | 4 | Already an OPEN Matt thread, not a GD-program item — the census's five `engine_inexpressible` pet kits resolve there, not here |

### 2.4 — Scoreboard

**Consolidated delivery (10 rows):** 8 FIT · 2 PARTIAL · 0 GAP.
**All rows scored (33 distinct mechanisms after consolidation and firewalling):**
**19 FIT · 13 PARTIAL · 1 GAP** (P-PLUSTARGET is the only outright no-surface row).

That ratio is the headline: **GD's delivery, ailment, cadence, economy, and trigger-shape layers land
almost entirely on surfaces we already built.** Where GD does not fit, it fails in one consistent
place — **the gear/progression layer that lets a PLAYER choose and bind mechanics.** Every large build
item in §2.1 (B1, B2, B3, B5, B6) is a facet of that one absence.

---

## §3 — Cross-era generality per build item

Era-substrate architecture §6 makes G-5's key-domain rulings **the template for D2 and PoE conversion
keys.** So the test on every item is: *does this surface serve other eras and our native game, or is it
GD-shaped?* Prefer the general formulation; a GD-shaped bolt-on is a debt the next key pays.

| Item | Generality | Assessment |
|---|---|---|
| **B1** proc chance + ICD | **UNIVERSAL** | D2 chance-to-cast charms · PoE trigger gems (all ICD-gated) · D4 Lucky Hit · our own `trig_*` affixes. Build it once, generally, and every future key inherits it. **The most general item in the register.** |
| **B2** proc-binding layer | **HIGH** | GD devotions · PoE trigger-gem links · D4 Aspects/Paragon glyphs are the same shape: *a player-chosen payload attached to a chosen trigger.* Design it as "bindable proc payloads," never as "constellations." |
| **B3** conversion operator | **HIGH** | PoE's conversion economy is core identity; D2 has it narrowly. Formulate as *a transform operator over the element axis*, which is exactly the `element_application` binder's existing structure vocabulary. |
| **B4** stacking classes | **HIGH** | PoE needs it more than GD (exposure vs curse vs penetration). Formulate as a general debuff-stacking enum, **not** as "GD's three RR types." |
| **B5** mechanic-granting sets | **HIGH** | D2 runewords + set bonuses, PoE uniques, D4 Aspects — the whole genre's "the item IS the build." The agnostic-loot operator model was *designed* for exactly this (kit-agnostic operators over universal axes) and is the only itemization that scales across ~500 kits from ~15 incompatible source games. |
| **B6** skill-modifier layer | **HIGH** | PoE support gems, D2 synergies, D4 skill upgrade-nodes. Formulate as "modifiers that adjust an owned mechanic," which is the gear law's *amplify your own* clause verbatim. |
| **B7** invulnerability window | **HIGH** | D2 Vigor/Fade-adjacent, PoE guard skills + Immortal Call, D4 defensive cooldowns. Genre-universal. |
| **B8** weighted proc-pool | **MEDIUM** | GD's WPS is the purest case, but PoE multi-link CoC and D4 Lucky Hit pools are the same selection problem. Formulate as *weighted selection from a consequence pool* — general. Avoid the name "WPS." |
| **B9** count operator | **HIGH** | PoE's GMP/LMP is bedrock; D4 has projectile-count aspects. Very general. |
| **B10** two-tier accumulator | **ALREADY GENERAL** | Ratified Tier-A across the corpus; not a GD item. |

**Nothing in the register is GD-shaped.** That is a real finding and worth saying: the GD census
surfaced almost no idiosyncrasy. Every gap it found is a gap the genre has, which is what you would
expect if GD is a good first oracle — and is evidence *for* the era-substrate ruling, not merely
consistent with it.

---

## §4 — Open design forks (Matt rules; I state leans and stop)

### F1 — Does *Reap. Die. Rise.* want a second, player-directed proc-binding progression surface?

18 GD kits (44%) build around devotions. PoE trigger gems and D4 Aspects are the same shape. But we
already have a designated player-expression surface: **soul-bound gear operators** under the four-clause
gear law.

- **(a)** Build a devotion-analogue layer — a second progression tree granting bindable procs.
- **(b)** **Absorb it into soul-bound gear** — proc payloads become structural operators; "binding"
  becomes equipping. No new tree.
- **(c)** Absorb into T4 capstones — procs become capstone payloads, rolled not chosen.

**Lean: (b).** It needs no new progression architecture, it is already the ruled home for
mechanic-adjusting operators, and it holds the gear law's *path texture to anyone* clause without
straining. The cost is honest and should be stated: **(b) makes the payload a purchase rather than a
pilgrimage.** GD's devotion tree is a *journey* — you route through a constellation map, pay affinity,
and the build's identity is the path you walked. Gear-as-absorption keeps the mechanic and drops the
route. If the answer is that the routing itself is the fun, that argues (a) and the answer is worth
more than the saved architecture. **This fork gates B2 and B6 and should be ruled before either is
specced.**

### F2 — Who carries damage conversion: capstone, gear, or both?

Ours is a rolled T4 capstone. GD's is an item/set build-choice — 17 kits, and the corpus's own
appendix already assigns `ELEMENT_CONVERSION_*` doors to 14 of them.

- **(a)** Capstone only — conversion stays a rolled kit property.
- **(b)** Gear only — retire the capstone variants, conversion becomes purely a build choice.
- **(c)** **Both, at different grades** — capstone = specialist scaling; gear operator = capped-garnish.

**Lean: (c).** It is the gear law's *import no one's core* clause applied precisely: core competency
appears on non-owners only as hard-capped garnish, never at the specialist's tier. It also preserves
the capstone's role as identity while giving the player the build-choice GD players expect. Gates B3.

### F3 — Confirm: a converted character is a FIXED kit, not an investable one

Our model has zero point-spend surface. GD's identity comes from two-mastery investment. I read this as
**already settled** by the coordinate register (the kit *is* the built character; expression lives in
gear), but it has never been said in one sentence, and G-5 makes it load-bearing for every future key.

- **(a)** **Confirm** — converted kits are fixed; all build expression is gear-side.
- **(b)** Introduce a bounded investment surface (rank-up / node choice) at the deferred trait floors.

**Lean: (a), stated explicitly in canon.** Not because (b) is wrong but because leaving it implicit is
how a "small progression pass" becomes a second game. If (a) is confirmed, B6 collapses into the gear
lane and the register gets simpler. Cheap ruling, large downstream effect.

### F4 — Do we adopt debuff stacking classes?

Today a debuff has a magnitude and no stacking rule. GD's three RR classes and PoE's
exposure/curse/penetration partitions both exist because *unbounded stacking of the same debuff is the
degenerate case* — it is why RR is the most-nerfed number in GD's history.

- **(a)** **Adopt a small stacking-class enum now** (`additive` / `highest-only` / `multiplicative-residual`).
- **(b)** Defer until a measured stacking problem appears in the gauntlet.

**Lean: (a).** It is an S-size field on a surface we just built, it prevents a class of balance failure
rather than diagnosing one, and every era key will want it. Deferring means re-keying built ailments later.

### F5 — Chance-based procs: do we take the chance, and do we take the guard with it?

Our trigger surface is deterministic by construction. The genre is not. B1 proposes both `proc_chance`
and `proc_internal_cooldown_seconds` — deliberately as a **pair**.

- **(a)** **Both together**, with an invariant that high-frequency triggers require an ICD.
- **(b)** Chance only — simpler, matches GD's raw devotion model.
- **(c)** Neither — keep deterministic triggers and re-express chance as an averaged rate.

**Lean: (a), and the pairing is the whole point.** Chance without an ICD is the documented D3
proc-storm failure and PoE's Cast-on-Crit-loop pathology: a chance-gated payload attached to a
high-frequency trigger stops being a proc and becomes the build's primary damage, at which point the
skill you chose is decoration. The ICD is not a nerf; it is what keeps a proc a *punctuation mark*.
**(c)** deserves a real hearing though — an averaged rate is more simulable and our cert instrument
would thank us for it — but it costs the genre's best texture: the moment where something *unexpectedly*
fires. That texture is load-bearing for loot excitement, and I would not trade it cheaply.

---

## §5 — Honest unknowns

1. **Devotion payloads — inherited, not resolved.** 18 kits, zero behavioral payload. B2 cannot be
   specced past its shape until elrond's `.arz` devotion probe returns. I have marked it
   BUILD-TRIGGERED / SPEC-BLOCKED-ON-DATA rather than sizing it, because sizing it now would be a guess
   wearing a size class.
2. **Magnitudes are unavailable for 40 of 41 kits** (census §5.6 — `kit_composition` / `kit_numeric` /
   `exact_skill*` each cover exactly one kit). **Every verdict in §1 is a SHAPE verdict.** "FIT" means
   the surface can express the mechanism; it never means our number matches GD's. Magnitude-faithful
   re-instantiation is not assessable from held data and I have not implied otherwise anywhere above.
3. **Hard-CC fit is asserted, not measured.** I firewalled the zeros correctly and our `freeze`/`stun`
   are built — but *which* GD kits apply them is unknown until the kit→`.arz` join (elrond's J3) runs.
   The G-3 payload is built; its GD-side attachment points are not attested.
4. **E4 commitment-bin sim consumption.** I labeled channel/cadence PARTIAL on the strength of the
   surface ledger's E4 row (emitter landed `e4d682e`; sim PHASE-2 QUEUED). If PHASE-2 has landed since
   the ledger's last delta, three PARTIAL rows (channel beam, channel cadence, movement-lock) upgrade
   to FIT. **I did not verify PHASE-2's current state in code** — flagged rather than assumed.
5. **Set-bonus mechanic-granting depth.** I verified `SetBonusDefinition` / `set_bonus_rank` exist at
   the export seam but did not read their full payload vocabulary. If a set bonus can already grant a
   mechanic (not just stats), B5 shrinks from M to S.
6. **The stale-docket count is unmeasured.** I found one (`gd-retaliation-warlord`) by accident while
   verifying a surface. The parity waves (ailment / Wave-B / Wave-C / Wave-D) landed *after* most GD
   deviation rows were written, and **there is no reason to believe 153 is the only one.** A systematic
   re-verification of all six GD `engine_inexpressible` rows against post-Wave-D surfaces is worth an
   elrond pass; I did not run it and cannot say how many others closed silently.
7. **Two prose adjudications I would have called differently.** Elrond flagged that a different
   adjudicator could reasonably count the two variant-lane P-RETAL hits, giving 3 instead of 1. It does
   not change my verdict (FIT either way) but it would have changed the *triage class* had retaliation
   been a gap — a reminder that at these counts, one adjudication decides build-vs-tag.

---

**Signed:** gandalf (named sub-agent), 2026-07-25.
Grim Dawn fits our forge better than I expected, and it fails in exactly one place: we built a
magnificent set of verbs and never built the hand that chooses them. Every large item in this register
is that same absence wearing a different name.
