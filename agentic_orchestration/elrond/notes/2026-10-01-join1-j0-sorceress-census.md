# JOIN-1 J0: the D2 Fire Sorceress INTERNAL / BOUNDARY census (J-S3b)

> ⚑ **ADDENDUM 4 2026-10-14 (§ 10; conductor ruling KC2 KP-426, `99d55f74e`): the universal-player-layer sweep admits SIX rows, 22–27 (5 BOUNDARY, 1 INTERNAL). A fourth named finding moves the count 21 → 27 and fraction (b) 13 → 18.** Curses/debuffs received and monster mana drains/cooldown lockout are EXCLUDED with fidelity-cost lines. § 10 governs over § 9.5.
> ⚑ **ADDENDUM 3 2026-10-14 (§ 9; conductor ruling KC2 KP-423, `edf2b88bc`): D2 potions (health, mana, rejuvenation; the belt as the count limit) were an OMISSION and join as ONE row, row 21, BOUNDARY / WIDEN. A third named finding moves the count 20 → 21 and fraction (b) 12 → 13.** § 9 governs over § 8.3.
> ⚑ **ADDENDUM 2 2026-10-14 (§ 8; conductor ruling KC2 KP-421, `145c880aa`): § 7.4's held item is ADMITTED as row 20, the INTAKE HIT LAW, BOUNDARY / WIDEN. A second named finding moves the count 19 → 20 and fraction (b) 11 → 12.** § 8 governs over § 7.4 and § 7.5.
> ⚑ **ADDENDUM 2026-10-14 (§ 7; Matt, KC2 KP-420; JOIN-1 charter v0.8): her shield block JOINS as row 19, BOUNDARY / WIDEN. The count moves 18 → 19 and the fraction-(b) population 10 → 11, as a NAMED FINDING after her J0 anchor.** § 6 C-4 is superseded. One question is held for the conductor (§ 7.4, D-1). § 7 governs over anything above it.

> ⚑ **GATE-2 PASSED WITH WARN (jack-ryan, collab `b48500a4d`; charter v0.5.1; KP-165). The count (18) and every row's class are FROZEN.** Forward corrections asked of this seat are in **§ 6**. The text above § 6 is left exactly as committed (`b4d151a4a`), so where § 6 corrects a line, § 6 governs.
> **STATUS:** CURRENT. J0 deliverable, seat elrond, Run JOIN-1 (charter `gandalf/notes/2026-09-29-join-1-run-charter.md` v0.5, § 1 J-S3b and § 5 J0 elrond row). **Subject of jack-ryan's J0 Gate-2: the COUNT and every row's CLASS freeze there. J3 does not open until that Gate-2 passes.**
> **Date:** 2026-10-01 · **Author:** elrond (data steward) · **Conductor:** gandalf (`RUN-CONDUCTOR`).
> **Method:** the P0 census method unchanged (`elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md`, `78797db4b`, § 1): a row is one distinct kit-internal mechanism or one distinct question the boundary must answer. Each row has a source, the best grade available in its lane, a class, the GD rule it meets (read-only reference) and a verdict. The verdict vocabulary is P0's: INTERNAL · BOUNDARY / AS-IS · BOUNDARY / WIDEN · BOUNDARY / GD-EMPTY · OUT-OF-ARENA.
> **Governing:** architect pass § 8 (Q86: kit-internal mechanisms enter natively; ONE boundary rulebook, GD default, widened by lever).
> **Mode:** read-only on all data and on the GD oracle (`reincarnated-engine/src/reincarnated/simulation/kc2/`). Zero code and no ORACLE behaviour touched. No KC2-run file touched.

---

## 0 · Headline

**The count is 18 rows: 7 INTERNAL, 10 BOUNDARY, 1 OUT-OF-ARENA, 0 HELD.** The 10 BOUNDARY rows split 2 AS-IS, 4 WIDEN and 4 GD-EMPTY.

Four findings, most important first:

1. **The Sorceress cannot "run" (charter § 4.5) on today's rulebook without three player-side DELIVERY builds that GD has no rule for.** These are: a player projectile in flight (row 11, Fire Ball); a remote, delayed, ground-targeted impact (row 12, Meteor); and a player-placed persistent damage zone (row 14, Meteor's burning ground). P0 named **L-14 `player_projectile_model` a "B5 blocker" with PoE2 Bonestorm as its only witness, and Bonestorm is outside JOIN-1.** The Sorceress puts L-14 on JOIN-1's build path, along with two sibling build items P0 did not have. **This changes J4b's cost**: either the three are built, or the kit joins with its delivery reduced to an approximation, which is a fidelity cost printed on the table's face. Choosing between those is the conductor's call, not this seat's.
2. **`crit_model` (L-06) gains a fourth witness, and it is DATAMINED.** D2 spells carry no to-hit term. `ToHit` and `LevToHit` are empty on rows 47 and 56, whereas Whirlwind has `LevToHit=5` and Battle Orders has `ToHit=50`. Spells also do not crit. That is VS's "always hit, never crit" shape, which GD's `resolve_hit` cannot express (row 10).
3. **The damage-family registry is exercised by D2 fire through a family GD already has, BUT the oracle's offense path does not read the operand.** `data/kc2/pm4l_mitigation_by_body.csv` carries a `res_fire` column for every body. `player_offense.Mitigation` reads only `res_physical`, `res_lightning` and `res_bleeding` (I-12), and no module under `kc2/` reads `res_fire` (verified by grep). The form is AS-IS; the operand is on disk and unread. This is a J4b input for gamora (row 15).
4. **The J-S3b pin misses one operand: Inferno (Id 41).** Meteor's burning ground is the sub-missile `meteorfire` (`Missiles.txt`). Its synergy is `EDmgSymPerCalc = skill('Inferno'.blvl)*3`. So row 56 references Inferno as a damage operand, reached through `Missiles.txt`, and J-S3b's operand list does not include it. **Flagged for Gate-2 (A-1), not repaired here.** The pin is the conductor's, and the corpus kit record (which votes) does not name Inferno either. The count and the classes do not depend on this flag. Only the operand list of row 4 does.

---

## 1 · Scope, pinned BY ROW ID (J-S3b; the corpus kit record votes)

| Pinned row | Skills.txt Id | Role in J-S3b | Enters this census as |
|---|---|---|---|
| Fire Ball | **47** | castable | rows 1, 3, 4, 5, 6, 8, 9, 10, 11, 13, 15, 16, 17, 18 |
| Meteor | **56** | castable | rows 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18 |
| Fire Bolt | **36** | operand (synergy blvl of 47 and 56) | row 4 only: its `blvl` is a term in both castables' `EDmgSymPerCalc`. Its own damage, missile and cost never enter |
| Fire Mastery | **61** | operand (fire passive) | row 5 |
| Warmth | **37** | operand (resource economy, "mana-hungry") | row 2 |
| Teleport | **54** | **EXCLUDED** (pinned) | Appears only in the JSON's `motion_frame`, not in its skill list. Excluded per J-S3b; it would be a B7 movement↔engagement row for a later kit |

**Sources, all re-derived this session, digests labelled FILE:**
- `fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9`, D2 1.13 classic, DATAMINED. `Skills.txt` FILE `59601208f3052205c175753038cedb6e338ef9bdc268f4e92a74b9c7b69cdc07`. `Missiles.txt` FILE `9d6794a50e8b1931e476a4d666bfe4048d7d1dada454f19659d74a8825adef53`. **Both git-blob ids match the upstream tree at the pinned commit**, checked through the GitHub contents API: `Skills.txt` `00fff7f9…` and `Missiles.txt` `18d5642c…`.
- `reincarnated-collaboration/agentic_orchestration/research/curated/kits-export/d2-fire-sorc.json` FILE `43eb1e55572da6abf127033d520c614660b120e49a2c269988ae0c62c6bfc6ea` (`grade = EXACT`, MAPPED, 6 dossier rows, 5 verify CONFIRMED, 0 dockets).
- The D2 formula set, MODEL-VERIFIED (community). ⚑ **legolas's J4 formula leg is in flight.** Wherever a row below rests on a community formula rather than on a record field, it says so, and its verdict (not its class) is conditional on that leg.

**Rows that the record references but that do not enter, with the reason (named so they are not mistaken for misses):**
- **Fire Wall (Id 51):** Meteor's `reqskill2`. It is a prerequisite only, so it is build legality and folds into row 18. ⚑ J-S3b says "every other Sorceress row, not referenced". Fire Wall **is** referenced, but as a prerequisite, not as an operand. See A-2.
- **Inferno (Id 41):** a damage operand of row 56 through `meteorfire`. See A-1.
- **Telekinesis:** Teleport's prerequisite. It falls out with Teleport.
- **The variants** (Meteorb, Blizzard/Fireball): `fidelity_notes` scopes them out of core `skills[]`.
- **Client-only fields** (`cltmissile*`, `castoverlay`, sounds, light) are presentation, not mechanism.
- **Defensive gear** (Chains of Honor, Spirit's resistances) is a player-sheet operand of the INTAKE rule, not a kit mechanism. P0 precedent: WW's defensive gear was not censused.

---

## 2 · The census

**Evidence grades:** **DM** = DATAMINED (a field of the pinned record) · **MV** = MODEL-VERIFIED (D2 community formula) · **att** = attested (corpus dossier or verify ledger). A row may carry two grades: `mechanism_grade` / `magnitude_grade`, per J-L4 and P0 § 7.3.

| # | Mechanism | Evidence (mechanism / magnitude) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| 1 | **Per-cast mana spend, refused when mana is short.** 47: `mana=10 lvlmana=1 manashift=7 minmana=1`; 56: `mana=34 lvlmana=1 manashift=7 minmana=1`. There is no `AttackNoMana`, unlike WW | DM / DM (fields) + MV (cost law `(mana+lvlmana·(slvl−1))·2^manashift/256`) | **INTERNAL** | `per_cast_energy` (C-2 fold): a per-cast IMPULSE on top of `energy.EnergyModel`'s channel drain | Enters natively. GD's per-cast impulse already has this form; the D2 cost law is a second setting of the same resource primitive |
| 2 | **Mana income: the D2 regeneration law plus Warmth (37)**, `passivestat1=manarecoverybonus`, `passivecalc1=ln12` (30 + 12/level) | DM (Warmth fields) + MV (base regen law) / **NONE** for the pool: the kit record has no Energy, mana pool or Warmth level | **INTERNAL** | `energy.EnergyModel` income + reservation | Native. ⚑ A value-gap (P0 § 7.3 shape): the mechanism is graded but the magnitude is not. The kit has no character sheet |
| 3 | **Base fire damage by skill level, three sources.** Fire Ball impact (`EMin 12/EMax 28`, `EMinLev1–5`, `HitShift 7`); Meteor impact (`EMin 80/EMax 100`, lines, `HitShift 8`); Meteor burning ground (`meteorfire` `EMin 15/Emax 25`, `MinELev1–5`, `HitShift 3`) | DM / DM | **INTERNAL** | `channel.compose_damage_basis()` (composition) | Native: damage composition (P0 PoE1 row 6 precedent) |
| 4 | **Synergy on base level.** 47: `(skill('Fire Bolt'.blvl)+skill('Meteor'.blvl))*par8`, `Param8=14`; 56: `(skill('Fire Bolt'.blvl)+skill('Fire Ball'.blvl))*par8`, `Param8=5`; `meteorfire`: `skill('Inferno'.blvl)*3` | DM (formula strings, literally `.blvl`) / **att** for 47/56/61 at 20 points (verify CONFIRMED); **NONE** for Fire Bolt's and Inferno's levels | **INTERNAL** | none | Native. ⚑ **A-1:** the Inferno operand is outside the pin. ⚑ The Fire Bolt level is unattested: the JSON says Meteor "synergizes Fire Ball and Fire Bolt" but gives no points |
| 5 | **Additive +% fire damage:** Fire Mastery (61) `passive_fire_mastery` `ln12` (30 + 7/level) plus gear "+fire damage" (Eschuta's +10–20%). `meteorfire` carries `ApplyMastery=1` | DM (61 fields, `ApplyMastery`) + att (gear) / DM + att | **INTERNAL** | `offense` modifier stack (additive, Lap L § 4.1 law) | Native. The composition order (synergy × (1 + mastery + gear)) is MV and pre-boundary |
| 6 | **+skill levels from gear** (Eschuta's +1–3, Spirit +2). They raise `slvl` and therefore the damage lines; they do **not** raise `blvl`, so synergies (row 4) do not move | att (dossier `item_alterations`) + MV (slvl/blvl rule) / att | **INTERNAL** | none | Native. The blvl/slvl split is DATAMINED in row 4's formula strings |
| 7 | **Meteor cooldown** `delay=30` frames | DM / DM (frames) + MV (25 fps → 1.2 s) | **INTERNAL** (a cooldown on a skill) | `channel.cooldown_s` (EoR) · `counterplay` runs actives greedy on cooldown | **AS-IS on the clock** (P0 VS row 2 precedent: a cooldown needs no new boundary primitive) |
| 8 | **Cast cadence by frame breakpoints.** `anim=SC`; the cast time is set by the Sorceress FCR breakpoint table; Spirit gives +35 FCR (att) | DM (`anim`) + att (FCR) / **MV**: the breakpoint table lives in `AnimData`, which is not among the 34 fetched files | **BOUNDARY** (tick clock) | `channel.tick_period_s = 0.16 × (100/AS%)`, continuous and proportional to AS | **WIDEN → L-01 `tick_quantisation`** = `frame-breakpoint-table`. **Second witness** after WW |
| 9 | **A cast roots the caster** for its cast frames (the `SC` sequence; no movement during the cast) | DM (`anim=SC`) / MV (lock rule) | **BOUNDARY** (B7, movement↔engagement during an action) | `channel_policy` measures movement while channelling (`REF_FRAC_MOVING_FIGHT 0.6265`) but has no cast-lock term. `action_permission` decodes GD's 26×26 `CharacterActionPermission` matrix, **read-only, imported by no hot loop** | **WIDEN**, lever attribution OPEN (A-3): L-10 `channel_move_speed_pct` names *channelling*, and this is a discrete cast. Candidate **L-S1 `cast_move_lock`**, or a setting of a wired-in action-permission matrix |
| 10 | **Hit resolution: spells have no hit roll and no crit.** `ToHit`, `LevToHit` and `ToHitCalc` are empty on 47 and 56 (WW: `LevToHit=5`; BO: `ToHit=50`) | DM (field absence, set against populated siblings) / MV (spells bypass AR; D2 crits apply to physical attacks only) | **BOUNDARY** (hit resolution) | `threat.resolve_hit(pth, roll)` derives the crit tier from the **same** PTH and d100 roll as the hit; at PTH ≥ 135 the multiplier is forced to 1.5. ⚑ On REFERENT-v1's board `player_offense.HIT_CHANCE = 1.0` (measured: the player cannot miss) and `CritLimb.LO = 1.0`. That is a coincidence of THIS board's operands, not a rule | **WIDEN → L-06 `crit_model`. Fourth witness** (D2 WW, PoE2, VS, D2 Sorc), the first whose absence of a to-hit term is DATAMINED. Conditional on legolas's formula leg for the MV half |
| 11 | **Fire Ball is a player projectile in flight.** `srvmissile=fireball`: `Vel 20`, `Range 50` (lifetime, frames), `CollideType 3`, `CollideKill 1` (bursts on first collision, not at the cursor) | DM / DM | **BOUNDARY** (B6, target selection) | The GD oracle has **no player projectile in flight.** `discrete_volley` is the monster lane. GD's own player projectile, Soulfire, is reduced in `secondary_streams` to a period proc with a **reach bracket** (`SoulfireReach` 3.0 / 4.0 m, "no reach field of any kind") | **GD-EMPTY → L-14 `player_projectile_model`** (a build item, not a lever). **Second witness** after PoE2 Bonestorm; **first inside JOIN-1.** Headline 1 |
| 12 | **Meteor is a remote, delayed, ground-targeted impact.** It lands at the cursor, not at the caster; `meteorcenter` `Range 60` (lifetime, frames), `AlwaysExplode 1`; 56 has `LineOfSight 4`, `SearchOpenXY 1` | DM / DM (frames) + MV (frames → seconds) | **BOUNDARY** (B6 + tick clock) | Player damage geometry is the **player-centred** moving disc (`disc.py`, family `eor_spin`). The remote `circle` shape plus a telegraph delay exist **only on the monster side** (`disc.py` names the blizzard per-drop scatter) | **GD-EMPTY (player side)**, with a monster-side form precedent. A build item with no P0 L-id: candidate **L-S2 `player_remote_delivery`**, or L-14 widened from "projectile" to "player delivery" (A-3) |
| 13 | **Splash footprint at the impact point.** Fire Ball `sHitPar1=4` (server damage radius); Meteor `Param1=6` radius via `calc1=ln12` (`Param2=0`, so flat across levels) | DM / DM + MV (D2 units → m) | **BOUNDARY** (B6) | The disc predicate in `geometry`/`disc`; multiplicity is `pm4l_target_multiplicity.csv`, a **measured constant per body** around the player | **AS-IS in form, EMPTY in operand** (P0 WW row 4 and finding 5). The disc test is centre-agnostic; the remote centre is row 12's problem, not this row's |
| 14 | **Meteor's burning ground: a player-placed persistent zone** damaging monsters inside it. `meteorfire` `pSrvDoFunc 5`, `pSrvDmgFunc 3`, `DamageRate 41`, `Collision 1`; duration from 56 `Param3=30`, `Param4=15` "Frames of fire" | DM / DM + MV (per-frame rate law) | **BOUNDARY** (placed zone × tick clock × target selection) | No player-side zone exists anywhere in `kc2/` (grep: `ground`, `zone`, `persistent`, `lingering` over the offense, devotion, summon and pet modules). Player DoT on monsters exists only as an **on-hit ledger** (`secondary_streams` bleed); `dot_timeline` is the decoded stacking rule for DoTs keyed `(damage_type, ATTACKER)` | **GD-EMPTY (player side).** A build item: candidate **L-S3 `player_placed_zone`** (A-3) |
| 15 | **Fire family vs monster resistance.** `EType=fire` on 36/37/47/56/61 and on the `fireball`/`meteorfire` missiles. Monsters are GD bodies in the arena | DM / DM (family tag) | **BOUNDARY** (damage type vs resistance + B8 family registry) | `threat.RESIST_PCT` has `Fire` (player intake). For OFFENSE, `player_offense.applied_damage` puts armour on physical only and resistance on every family. ⚑ **`pm4l_mitigation_by_body.csv` carries `res_fire` per body; `Mitigation` reads only physical/lightning/bleeding; no `kc2/` module reads `res_fire`** | **AS-IS** in form: D2 `fire` → GD `Fire`, a family GD already has; elemental damage takes no armour leg, so mitigation ORDER is moot for this kit. ⚑ The operand is on disk and unread (headline 3). The registry prints **D2 fire: EXERCISED**; `KeyError` is preserved |
| 16 | **Hits put monsters into hit recovery.** `GetHit=1` on `fireball` and `meteorcenter`; `meteorfire` has `dParam1=19` "softhit chance (/128)" | DM / DM (flag) + MV (D2 damage-vs-life threshold law) | **BOUNDARY** (CC/status on monsters) | `control_application` is the **player-as-victim** lane only (P0 § 7.1): no monster control model, no monster CC duration | **GD-EMPTY** (P0 § 7.1 item 1). A build item in the monster-CC lane; P0 assigned it no L-id (A-3). ⚑ **A-4:** WW's melee hits trigger hit recovery too, and P0 did not census it |
| 17 | **The player's casts are interruptible by hit recovery.** `interrupt=1` on 47 and 56 (WW: empty, i.e. uninterruptible) | DM / DM (flag) + MV (D2 player FHR law) | **BOUNDARY** (CC/status on the PLAYER; B7) | The GD player-control lane (`control_application`) is triggered by control **families** from monster skills; GD has no damage-threshold stagger. `REF_P_CAST_INTERRUPTS = 0.15` is the player's own cast cutting his channel, not a stagger | **WIDEN**: candidate **L-S4 `player_hit_recovery`** {GD setting \| `d2-damage-threshold`}. ⚑ **A-5:** is GD's setting `off` (GD decides that damage never interrupts) or `NONE — no GD rule`? Census § 7.1 discipline: the registry must be able to say which |
| 18 | **Build legality:** prerequisites (47 `reqskill1` Fire Bolt; 56 `reqskill1` Fire Ball, `reqskill2` Fire Wall), `reqlevel` 12/24/30, `leftskill`, `ItemEffect` | DM / DM | **OUT-OF-ARENA** | none | P0 § 7.2 (PoE1 `weapon_restrictions` precedent): kit-defining at home, with no fight-boundary meaning |

**D2 Fire Sorceress: INTERNAL 7** (1, 2, 3, 4, 5, 6, 7) · **BOUNDARY 10** (8–17; **AS-IS 2**: 13, 15 · **WIDEN 4**: 8, 9, 10, 17 · **GD-EMPTY 4**: 11, 12, 14, 16) · **OUT-OF-ARENA 1** (18) · **HELD 0**. **18 rows.**

**Her § 4.5 fractions, for reference only (the denominators freeze at Gate-2):** (a) rows mapped / **18**; (b) of the **4 WIDEN rows**, how many have their D2 setting implemented and ACTIVE in her `JOIN` profile. ⚑ The 4 GD-EMPTY rows sit outside fraction (b) by its own definition ("BOUNDARY/WIDEN rows"). For this kit they are a fraction-(a) and "runs" question, and that is exactly where headline 1 bites.

---

## 3 · Candidate levers surfaced (charter § 4.4: registered at the J0 Gate-2, not by this seat)

Provisional ids `L-S*` are used so that registry numbering stays the registry's.

| Lever | Concept | Kind | GD-referent value | Witnesses |
|---|---|---|---|---|
| L-01 `tick_quantisation` | existing | settable | `continuous-as-proportional` | WW, **Sorc (row 8)** |
| L-06 `crit_model` | existing | settable | `pth-tiered` | WW, PoE2, VS, **Sorc (row 10)** |
| L-14 `player_projectile_model` | existing | **build item** | NONE: no GD rule | PoE2, **Sorc (row 11)** |
| **L-S1** `cast_move_lock` | movement during a discrete cast | settable (or an L-10 widening; A-3) | NONE wired. GD's decoded `CharacterActionPermission` matrix is read-only | Sorc (row 9) |
| **L-S2** `player_remote_delivery` | remote, delayed, ground-targeted player impact | **build item** (or L-14 widened; A-3) | NONE player-side. Monster-side form exists | Sorc (row 12) |
| **L-S3** `player_placed_zone` | persistent player zone damaging monsters | **build item** | NONE player-side | Sorc (row 14) |
| **L-S4** `player_hit_recovery` | damage-threshold interruption of the player's actions | settable | ⚑ A-5: `off` vs NONE | Sorc (row 17) |
| *(monster-CC lane)* | monster hit recovery | **build item** (P0 § 7.1; no L-id) | NONE | Sorc (row 16), and WW unrecorded (A-4) |

---

## 4 · Ambiguities, for jack-ryan's Gate-2

**None of these changes the count or any row's class.** A-1 and A-2 touch the pin's text, A-3 and A-5 touch lever attribution, and A-4 touches the frozen P0/J-S2 record.

| # | Ambiguity | Why it is not resolved here | What would resolve it |
|---|---|---|---|
| **A-1** | **Inferno (Id 41) is a damage operand of pinned row 56** (`meteorfire` `EDmgSymPerCalc = skill('Inferno'.blvl)*3`) but is absent from J-S3b's operand list | The pin is the conductor's. The corpus kit JSON (which votes) names synergies only as "Meteor synergizes Fire Ball and Fire Bolt". Adding a row id would let this seat amend the scope it is censusing | The conductor either (a) adds Inferno (41) to J-S3b as a fourth operand row, or (b) records its `blvl` as **NONE in the kit record**, carried as a named term with its operand unset. Neither changes row 4's class |
| **A-2** | J-S3b says "every other Sorceress row, not referenced", but **Fire Wall (51) is referenced** (56 `reqskill2`) | It is referenced as a prerequisite, not an operand, so it folds into row 18 (OUT-OF-ARENA). The pin's sentence is imprecise; its effect is right | One word in J-S3b: "not referenced **as an operand**" |
| **A-3** | **Lever attribution for rows 9, 12, 14 and 16.** Does each widen an existing L-id (L-10 for 9, L-14 for 12) or open a new one? | Charter § 4.4 registers census-surfaced levers at Gate-2. Choosing between widening a named lever and opening a new one sets the registry's shape | The Gate-2 registration |
| **A-4** | **P0 consistency.** Row 16 (monster hit recovery) applies equally to WW's melee hits, which P0 did not census. J-S2's 14 rows are frozen at launch, and any WW addition is a named finding | Adding a WW row is not this seat's to make. It is a reclassification of a frozen denominator, owed to the conductor as a finding | The conductor records whether WW gains a row (named finding) or the omission is accepted (one line) |
| **A-5** | **Row 17's GD-referent value:** is "damage never interrupts the player" a GD **rule** (`off`) or GD **silence** (`NONE — no GD rule`)? | P0 § 7.1's law: a registry that cannot tell silence from a setting launders silence into a default. The record does not decide this, so this seat does not | Gate-2 or the J3 registration |

---

## 5 · What this note claims, and what would falsify it

**Claims.** These 18 mechanisms are what the five pinned rows (47, 56, 36, 61, 37) and the kit record depend on, at the grades named. The GD oracle references are as cited, read on disk at engine HEAD this session. `res_fire` is carried on the pinned board and read by no `kc2/` module.

**Does not claim.** That the list is complete beyond what the pinned rows, `Missiles.txt` and the kit record say. That any lever should move. That the Sorceress can run today: headline 1 says she cannot without three delivery builds, or an approximation priced as a fidelity cost.

**Falsifiers.** Row 10: a populated `ToHit`/`LevToHit`/`ToHitCalc` on 47 or 56, or a D2 source showing that spells roll AR. Rows 11/12/14: a player-side projectile-flight, remote-delivery or placed-zone body anywhere in `kc2/`. Row 15's operand finding: any `kc2/` read of `res_fire`. Headline 4: a `meteorfire` synergy other than Inferno in the pinned `Missiles.txt`.

**Signed:** elrond (data steward and archivist), 2026-10-01. Seat J0, Run JOIN-1. Read-only on every store touched.

---

## 6 · Forward corrections after Gate-2 (`b48500a4d`, KP-165). Count, classes and frozen record unchanged

Each item names the line it corrects. The original text above stays visible.

| # | Gate-2 item | Corrects | Correction (governs) |
|---|---|---|---|
| **C-1** | **W1** | Row 15, the GD-rule cell (*"For OFFENSE, `player_offense.applied_damage` puts armour on physical only and resistance on every family"*); headline 3; the § 2 sentence *"`KeyError` is preserved"* | Her damage runs on the **offense** side through `player_offense.applied_damage(raw, armor, absorption_pct, res_physical_pct, crit_mult)` (`player_offense.py:329`). That chain is **physical-only** and has **no damage-type table**. Lightning and bleeding are separate streams hard-wired per family in `secondary_streams`. **`threat.mitigate`'s `KeyError` table (`threat.RESIST_PCT`) is on the player-takes-damage (intake) side**, keyed to the player's own resistances. So the offense side has no family registry and no refuse-loudly guard. A D2 fire packet has no path today, and routed through `applied_damage` it would be silently mis-adjudicated (armour plus physical resistance), not refused. **Class and verdict unchanged**: AS-IS in form (per-stream `× (1 − res/100)`, no armour leg), the family exists, and the `res_fire` operand is on disk but unread. That is the row-13 shape, EMPTY in operand. The registry prints D2 fire as EXERCISED **on offense** only once a family-keyed offense dispatch with the same refuse-loudly discipline exists and reads `res_fire` (conductor and gamora, W1b) |
| **C-2** | **A-2** | § 1, the Fire Wall bullet, and the pin sentence *"every other Sorceress row, not referenced"* | jack-ryan's corrigendum text, verbatim: *"every other Sorceress row is excluded as a mechanism. Rows referenced only as prerequisites (Fire Wall 51 directly, Blaze 46 transitively) fold into the OUT-OF-ARENA legality row. Where a prerequisite forces an operand floor (Inferno ≥ 1, Fire Bolt ≥ 1), row 4 carries the floor."* The chain was re-verified in `Skills.txt` this session: Meteor `reqskill2` Fire Wall → Fire Wall `reqskill1` Blaze → Blaze `reqskill1` Inferno; Fire Ball `reqskill1` Fire Bolt |
| **C-3** | **A-1** | § 1 pin table (five rows) and headline 4 | **A fourth operand row is added to her pin record:** **Inferno, `Skills.txt` Id 41, operand (synergy `blvl` of 56 via `meteorfire`), entering row 4 only.** Its `blvl` enters through `srvmissilea=meteorcenter` → `HitSubMissile1=meteorfire` → `EDmgSymPerCalc = skill('Inferno'.blvl)*3`, and `SkillDesc.txt`'s `meteor` synergy panel names Inferno (`skillname41`). Its own damage, missiles and cost never enter. Magnitude: DM at the legality floor of 1, NONE above it, the same state as Fire Bolt. Points above the floor are a conductor-default operand and an explicit lever, unless legolas's J4b leg sources them. **A-1 in § 4 is RESOLVED: pinned, not left unset. Count 18 and row 4's class are unchanged** |
| **C-4** | **W4** | § 1, the "do not enter" list | **Add: her shield block.** The kit loadout carries a shield (Spirit Monarch), and legolas's timing packet (`b0f9d77fa`) calls her block kit-reachable. Under J-S3b, gear enters only as an operand of a pinned-row mechanism (Spirit's FCR feeds row 8, its +skills row 6, Eschuta's +fire% row 5). **Block feeds no pinned row, so it is excluded and the count stays 18.** It is "censused and excluded", not "not censused" (P0 § 7.2). The fidelity-cost table carries it as a home mechanism not joined. GD's intake already has the slot (`threat.PLAYER_BLOCK_PCT = 0.0`); D2's full negate plus block lock would be a WIDEN if a later pin admits it |
| C-5 | I-1 | Row 8's magnitude grade (*"MV: the breakpoint table lives in `AnimData`, which is not among the 34 fetched files"*) | Superseded by legolas `b0f9d77fa`: `SO SC 14/256/7` is DATAMINED (Basin dump), and the FCR table 0/9/20/37/63/105/200 → 13…7 ticks is community-verified from three sources. The magnitude grade upgrades; the class is unchanged |
| C-6 | I-2 | Row 11's GD-rule cell | Add the monster-side form precedent: `deferred_arrival.py` models **monster** projectile flight (`arrival = cast + ceil((d/v)/period)`). This parallels row 12's `disc.py` citation and is relevant to L-14's build cost. Still GD-EMPTY on the player side |
| C-7 | I-3 | § 5 falsifiers for row 10 | Add: `fireball` and `meteorcenter` carry `HitFlags=2` (undecoded). An AR path through the missile hit flags would falsify the DM half; legolas's J4b leg should confirm there is none. L-06 gains a third value, `no-roll-no-crit` (registered by gamora at J3) |
| C-8 | I-4 | Row 18's verdict (*"no fight-boundary meaning"*) | Reword as: the legality check does not run in the arena, **but it forces operand floors that row 4 carries** (Inferno ≥ 1, Fire Bolt ≥ 1). The class is unchanged |

**Gate-2 rulings recorded here for the reader** (not this seat's to make): **A-3** registers L-17 `cast_move_lock` (row 9), L-18 `player_hit_recovery` (row 17), L-19 `player_remote_delivery` (row 12), L-20 `player_placed_zone` (row 14) and L-21 `monster_hit_recovery` (row 16). This replaces the provisional `L-S1…L-S4` ids in § 3. **A-5** rules GD's referent for row 17 as **`NONE`**, with a DECLARED-INVENTED JOIN default of `off`. **W2** sets her fraction-(b) population to **all 10 BOUNDARY rows**, not the 4 WIDEN rows stated under § 2. **A-4** (the Barbarian's two rows) is recorded against P0, in `2026-09-28-join1-p0-internal-boundary-census.md` § 11.

**Frozen record, restated:** 18 rows: INTERNAL 7 (1–7) · BOUNDARY 10 (AS-IS 13, 15 · WIDEN 8, 9, 10, 17 · GD-EMPTY 11, 12, 14, 16) · OUT-OF-ARENA 1 (18) · HELD 0. Operands for row 4: Fire Bolt (36) and Inferno (41).

*Forward corrections signed:* elrond, 2026-10-01.

---

## 7 · Addendum 2026-10-14: her shield block joins (Matt, KC2 KP-420; charter v0.8). Count 18 → 19, a NAMED FINDING

**Source of the change.** Matt, 2026-10-14, KC2-PLAY ledger **KP-420** (`gandalf/notes/2026-09-20-kc2-play-run-charter.md`), folded as JOIN-1 charter **v0.8**: *"The Sorceress joins with her FULL D2 defensive sheet including shield block … block is a census row, denominator 18→19, recorded as a named finding."* This **supersedes** charter v0.5.1 amendment (8) and jack-ryan's census Gate-2 **W4** (`qa/findings/2026-10-01-join1-j0-sorceress-census-gate2.md`, `b48500a4d`), and with them § 6 **C-4** above. C-4 was right under the pin it was written against, which admitted gear only as an operand of a pinned-row mechanism. KP-420 widens her scope to her whole defensive sheet, so block no longer needs a pinned row to feed.

**What this addendum does not touch.** Rows 1–18, their classes and their verdicts stand exactly as § 2 and § 6 left them. The text above is left as committed (`b4d151a4a`, `3ade1a6a6`); where § 7 corrects a line, § 7 governs.

### 7.1 · Correction to § 1 and § 6 C-4: block leaves the "do not enter" list

- **§ 1, "Rows that the record references but that do not enter":** her shield block is **removed** from this list (it was added there by C-4). It now enters as row 19.
- **§ 1, the "Defensive gear" bullet** (*"Chains of Honor, Spirit's resistances … a player-sheet operand of the INTAKE rule, not a kit mechanism"*): the classification stands for life and resists, but the bullet's scope is now the whole defensive sheet. See § 7.3. Defence is the exception held at § 7.4.
- **The fidelity-cost table** no longer carries block as "a home mechanism not joined". That line goes, because the mechanism is joined.

### 7.2 · Row 19

| # | Mechanism | Evidence (mechanism / magnitude) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| **19** | **Shield block: a blocked monster hit is fully negated, and the block locks her in the BL animation for a time set by her FBR.** The kit loadout carries a Spirit Monarch (the kit record; legolas: "the only effect of the shield is that BL becomes reachable") | **DM** for the lock's frame data: `SO BL 5 · 256`, base 9 ticks (0.36 s) at 0 % FBR (Basin AnimData dump, cross-checked against Maxroll's per-class block base; legolas `b0f9d77fa` § 1, the `d2-fire-sorc` **BL** row, status MISSING "only if the model resolves blocks"). **MV** for the lock duration by FBR: `ticks = ceil(256·5 / floor(256·(50+EFBR)/100) − 1)`, table FBR 0/7/15/27/48/86/200 → 9…3 ticks (legolas § 3.4, COMMUNITY-VERIFIED). **MV, not sourced this session,** for the block-chance law and the full-negate rule. **Magnitude NONE** for her block chance: it depends on the shield's base block, her Dexterity and her character level, and the kit record carries no stat values (legolas Q7) | **BOUNDARY** (intake avoidance × B7: a lock on the player's actions) | `threat.PLAYER_BLOCK_PCT = 0.0` (`threat.py:126`, engine HEAD `f72316b7`), **MEASURED** (sheet 519: *"block / dodge / deflect are ALL ZERO … Carried as a constant so the zero is a measurement on the wire rather than an omission"*). It is emitted in `declared_constants()` (`threat.py:2317`). **No resolve path reads it.** `resolve_attack`'s hit-certainty reasoning (`threat.py:1895`) is conditioned on its being zero. GD itself resolves block as a chance plus a partial **block value** plus a shield **recovery** time; the oracle implements none of these, because the sheet zero makes them unreachable | **WIDEN.** Candidate lever **L-S5 `player_block_model`** {`gd` (referent: chance **0.0, MEASURED**) \| `d2-full-negate-bl-lock`}. Settable. The id is registered by the delta Gate-2, not by this seat |

**Why WIDEN, and why not AS-IS or GD-EMPTY.** I confirm W4's provisional class, and I have checked it against both neighbours.

- **Not AS-IS.** GD's rule cannot express D2 block. GD negates part of a blocked hit (block value) and puts the *shield* on recovery. D2 negates the whole hit and locks the *player*. The lock is a B7 action interruption, the same shape as rows 9 and 17. Nothing in GD's form carries it. Even GD's form is unbuilt in the oracle: a non-zero `PLAYER_BLOCK_PCT` would change nothing today, because no path reads it.
- **Not GD-EMPTY.** P0 § 7.1 reserves GD-EMPTY for a boundary question with **no GD rule at all**, where the registry's referent must read `NONE — no GD rule`. Block has a GD referent value, and it is not silence. It is a **measured zero** on the referent sheet, which P0 § 7.1 tells us to keep distinct from `NONE` ("a GD value that happens to be zero"). Setting the lever to `gd` reproduces REFERENT-v1 exactly. That is the defining property of a WIDEN row's default. The GD-EMPTY rows in this census (11, 12, 14, 16) have no such setting.
- **Precedent inside this census.** Rows 9 and 17 are WIDEN with no wired oracle body either (row 9: "NONE wired"; row 17: GD referent `NONE` with a DECLARED-INVENTED default `off`, A-5). Row 19 is stronger than row 17: its GD default is **measured**, not invented.
- **What WIDEN costs here, named so it is not hidden in the class.** The `d2` setting needs three pieces. First, a block resolve step in the intake path, between the hit and mitigation. Second, a per-attack **block-eligibility** rule: in D2, block applies to some attack kinds (community law: melee and missile attacks), so each GD monster attack slot needs a declared mapping. Third, the BL lock in the player-action lane, where it shares the lock primitive with rows 9 and 17. These are build items *inside* a settable lever. They are not a new GD-EMPTY row. Whether the lock shares L-18's machinery is gamora's design call.
- **Coupling.** The BL lock is an action interruption, and it composes with row 17 (L-18). D2's community rule set also reduces block chance while the player is moving. If legolas's leg sources that rule, it couples row 19 to her movement. These are operand and law details for gamora's addendum, not further rows.

**Falsifiers.** For WIDEN over GD-EMPTY: a reading in which `PLAYER_BLOCK_PCT = 0.0` is an unmeasured placeholder rather than sheet 519's measurement. Under that reading the referent is `NONE` and the row is GD-EMPTY (fraction (b) is unchanged either way, see § 7.5). For WIDEN over AS-IS: any `kc2/` resolve path that reads `PLAYER_BLOCK_PCT`, or that already negates a whole hit and locks the player.

### 7.3 · Her other defensive operands enter as player-sheet operands, not rows

Under KP-420 (b), enemy attacks are anchored against the kit's defences: *"life, resists, defence, block"*. My method (P0 § 1) makes a row only for a distinct mechanism or a distinct boundary question. An operand that drops into an existing GD intake form is not a row (P0 precedent: WW's defensive gear was not censused; § 1 above).

| Operand | Enters GD's intake as | Class here |
|---|---|---|
| **Life** | `PLAYER_HP_MAX`: the same pool form | operand, no row |
| **Elemental and poison resists** | `RESIST_PCT[family]`: the same per-family `× (1 − res/100)` form, guarded by the `KeyError` refusal. D2's cap (75, plus +max) and the Hell penalty (−100) are her sheet's own derivation, which happens before the boundary. They are not a boundary rule | operand, no row |
| **Physical damage reduction** (D2 "Damage Reduced by %", e.g. Chains of Honor) | ⚑ **declared map:** `RESIST_PCT["Physical"]`. D2 has no armour-absorption term, so GD's armour leg takes a declared operand of **0**. That is the P0 WW row-12 shape: AS-IS form with a D2 operand | operand, no row; the map is **declared**, and gamora's addendum states it |
| **Block** | no existing form | **row 19** (§ 7.2) |
| **Defence** | ⚑ **held, see § 7.4** | — |

### 7.4 · ⚑ HELD FOR THE CONDUCTOR (D-1): defence does not enter as a bare operand under my method

**I am stopping on this item. It is not added here.**

D2 **Defence** is not a GD operand. In GD, a monster hits the player through `threat.probability_to_hit(oa, da)` against **DA**, with `PTH_MINIMUM = 55`, and the crit tier comes from the same roll (`resolve_hit`). In D2, a monster hits the player through a different function: AR against Defence, with level terms, clamped to **[5 %, 95 %]**. D2 monsters have no PTH crit tier. Putting her Defence into GD's DA slot would be an **invented mapping**, not an operand.

By my method, "under which hit law does a GD body's attack land on a D2 player?" is a **distinct boundary question**. It is the intake-direction twin of P0 WW row 9 (L-04/L-05, the clamps) and of row 10 here (L-06). jack-ryan's W1 established that boundary rules are stated **per direction**, and the charter already carries an intake L-06 setting (v0.6.7, KP-321). Until KP-420 it did not arise for her, because gamora's M-2 option (I) would have put the referent's sheet in her place. KP-420 retired option (I).

If the conductor admits it, it is **row 20, BOUNDARY / WIDEN** (L-04/L-05 and L-06 in the intake direction, plus a declared Defence ↔ DA disposition). That would be a **second named finding: 19 → 20 and 11 → 12.** If the conductor rules instead that Defence enters as an anchored operand under GD's hit law, that ruling is an E-1 measured cost, and the conductor records it with the map declared. **Either way the choice is above this seat.** KP-420 names block as the row, and adding a further row would let this seat amend the scope it is censusing (the A-1 discipline). Row 19 and the denominators in § 7.5 do not depend on D-1's outcome, except as stated there.

### 7.5 · NAMED FINDING: the Sorceress's denominators after her J0 anchor

**Reason:** Matt, KP-420 (charter v0.8): her full D2 defensive sheet, including shield block, joins. **This is an addition after her J0 Gate-2 anchor** (charter v0.5.1 (1), `b48500a4d`), so it is a named finding (charter § 4.5), printed against that anchor with its reason. It is not a silent re-map. Like the Barbarian's 14 → 16, it makes coverage harder, not easier, and it lands before J4b is graded.

| Fraction | J0 anchor (v0.5.1) | After KP-420 | Why |
|---|---|---|---|
| **(a)** rows mapped / all rows | **18** | **19** | row 19 added |
| **(b)** population = all BOUNDARY rows (Gate-2 W2; v0.5.1 (2)) | **10** | **11** | row 19 is BOUNDARY. Its WIDEN sub-class does not matter for (b), because (b) counts every BOUNDARY row. A GD-EMPTY re-reading (§ 7.2 falsifier) would leave (b) at 11 |

⚑ **Conditional on D-1 (§ 7.4):** if the conductor admits intake hit resolution as a row, a further named finding moves these to **20 and 12**.

**Corrected frozen record (after KP-420): 19 rows.**

| Class | Count | Rows |
|---|---|---|
| INTERNAL | 7 | 1–7 |
| **BOUNDARY** | **11** | **AS-IS 2**: 13, 15 · **WIDEN 5**: 8, 9, 10, 17, **19** · **GD-EMPTY 4**: 11, 12, 14, 16 |
| OUT-OF-ARENA | 1 | 18 |
| HELD | 0 | — |

Operands for row 4: Fire Bolt (36) and Inferno (41), unchanged. Candidate lever surfaced: **L-S5 `player_block_model`** (§ 7.2), for registration at the delta Gate-2. **Owed downstream (not this seat's):** legolas sources the block-chance law, the full-negate rule and the block-eligibility rule with grades. These go with the KP-420 enemy-anchor leg, together with the Q7 gear values (FBR, Dexterity, shield base block). gamora's design addendum carries the row-19 build pieces and the § 7.3 declared physical map. jack-ryan delta-gates the class and the denominators.

*Addendum signed:* elrond (data steward and archivist), 2026-10-14. Run JOIN-1, conductor gandalf. Read-only on every store touched, including the GD oracle at engine HEAD `f72316b7`.

---

## 8 · Addendum 2, 2026-10-14: the intake hit law joins as row 20 (conductor ruling, KC2 KP-421). Count 19 → 20, a second NAMED FINDING

**Source of the change.** Conductor gandalf, KC2-PLAY ledger **KP-421** (`gandalf/notes/2026-09-20-kc2-play-run-charter.md`, collab `145c880aa`), ruling on this seat's held item **D-1** (§ 7.4): *"admit it as row 20, BOUNDARY / WIDEN."* The conductor gave three grounds. (1) KP-420 rules native mechanics on anchored magnitudes in **both** directions. (2) The row matches rows 9, 10 and 19. (3) It makes coverage harder, not easier. § 7.4 is **resolved: admitted**. Rows 1–19 and their classes are unchanged. § 7 is left as committed (`20790cd34`). Where § 8 corrects § 7.4 or § 7.5, § 8 governs.

### 8.1 · Row 20

| # | Mechanism | Evidence (mechanism / magnitude) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| **20** | **Intake hit resolution: a monster's attack lands on her by D2's law, AR against her Defence, with level terms, clamped to [5 %, 95 %]. D2 monster hits on the player have no PTH crit tier.** Her Defence comes from her D2 sheet (KP-420 (b) and (d)) | **MV** (D2 community hit law, the intake twin of the AR formula P0 WW row 9 cites; legolas sources the formula and its grades in the KP-420 enemy-anchor leg) / **NONE** for both operands: her Defence (the kit record has no stat values; legolas Q7) and the anchored monster AR (KP-420 (a), the leg in flight) | **BOUNDARY** (hit resolution, **intake** direction) | `threat.probability_to_hit(oa, da)`: a two-term blend with `PTH_MINIMUM = 55`. `resolve_hit` derives the crit tier from the **same** PTH and roll (`PTH_THRESHOLDS` → `PTH_MULTIPLIERS`). On REFERENT-v1's board every body's PTH lies in 91.41–99.98, so every hit lands at exactly one crit tier (`threat.py:1892–1897`; that is a fact of this board, not a rule) | **WIDEN.** It takes the **intake-direction** settings of **L-04 `pth_floor_pct`** (GD 55; D2 5), **L-05 `pth_ceiling_pct`** (GD unbounded; D2 95) and **L-06 `crit_model`** (GD `pth-tiered`; D2 no tier on intake; cf. the charter's intake L-06 setting, v0.6.7 / KP-321). **GD default:** `probability_to_hit(oa, da)`, minimum 55, with crit tiers. **D2 setting:** AR vs Defence, 5–95 %, no tiers. Magnitudes are anchored per KP-420 |

**Notes on the class.**

- **WIDEN, by P0 WW row 9's own reasoning.** The two *functions* differ. Under E-1, a kit running under GD's function would be a measured cost, not inexpressibility. What GD's form cannot express is the **clamps** and the **untiered** intake. Those are what make the row WIDEN. GD's default reproduces REFERENT-v1, as a WIDEN default must.
- **Defence ↔ DA.** Under the `d2` setting, her Defence is the operand of D2's own law, so it needs no conversion. Under the `gd` setting, she would need a DA, and a Defence → DA map would be an **invented** mapping. **That setting must be labelled DECLARED-INVENTED wherever it runs** (P0 § 7.1 discipline: never launder an invented value into a default).
- **Lever registration.** The registry decides whether the intake-direction settings are per-direction values of L-04/L-05/L-06 or new ids. W1 requires only that they be **stated per direction**. Registration belongs to the delta Gate-2, not to this seat.
- **Coupling.** The row composes with row 19 (D2 checks block on a hit that has landed) and with row 17 (a landed hit can put her into hit recovery). The D2 order is hit, then block, then damage. gamora's addendum fixes that order in the intake resolve step. It is a law detail, not a further row.

**Falsifiers.** For WIDEN over AS-IS: any GD intake path whose floor or ceiling can be set to 5 and 95 and whose crit tier can be separated from the hit roll. P0 found none (`resolve_hit` derives both from one PTH and one roll). For the D2 setting's form: a D2 primary source showing that monster attacks on the player use a law other than AR against Defence with the 5–95 % clamp.

### 8.2 · § 7.3 correction: Defence

Defence's row in the § 7.3 operand table (*"held, see § 7.4"*) now reads: **row 20 (§ 8.1).** Life, resists and physical damage reduction stay operands, exactly as § 7.3 states. With row 20 admitted, every item of KP-420 (b)'s defence list ("life, resists, defence, block") is accounted for: two rows (19 and 20) and three operands.

### 8.3 · SECOND NAMED FINDING: the Sorceress's denominators after KP-421

**Reason:** conductor ruling **KP-421** (collab `145c880aa`), on held item D-1. The ruling follows from Matt's KP-420. **This addition comes after her J0 Gate-2 anchor** (charter v0.5.1 (1), `b48500a4d`), so it is a named finding (charter § 4.5), printed against that anchor with its reason. It is not a silent re-map. It is the second such finding, after § 7.5's (KP-420, block). It makes coverage harder and lands before J4b is graded.

| Fraction | J0 anchor (v0.5.1) | After KP-420 (§ 7.5) | **After KP-421 (this finding)** | Why |
|---|---|---|---|---|
| **(a)** rows mapped / all rows | 18 | 19 | **20** | row 20 added |
| **(b)** population = all BOUNDARY rows (Gate-2 W2; v0.5.1 (2)) | 10 | 11 | **12** | row 20 is BOUNDARY |

§ 7.5's conditional line (*"if the conductor admits intake hit resolution as a row … 20 and 12"*) is hereby **discharged**: admitted.

**Corrected frozen record (after KP-421): 20 rows.**

| Class | Count | Rows |
|---|---|---|
| INTERNAL | 7 | 1–7 |
| **BOUNDARY** | **12** | **AS-IS 2**: 13, 15 · **WIDEN 6**: 8, 9, 10, 17, 19, **20** · **GD-EMPTY 4**: 11, 12, 14, 16 |
| OUT-OF-ARENA | 1 | 18 |
| HELD | 0 | — |

**Restated in one line:** INTERNAL 7 · BOUNDARY 12 · OUT-OF-ARENA 1 · HELD 0 = **20**. Operands for row 4: Fire Bolt (36) and Inferno (41), unchanged. Candidate levers surfaced since the J0 Gate-2: **L-S5 `player_block_model`** (row 19), and the **intake-direction settings of L-04/L-05/L-06** (row 20). Both are for registration at the delta Gate-2.

**Owed downstream (not this seat's):**
- **legolas:** source the D2 intake hit law (AR vs Defence, level terms, clamp) with grades, in the KP-420 enemy-anchor leg, alongside § 7.5's block items.
- **gamora:** carry row 20's intake settings, the hit → block → damage order and the labelling of the DECLARED-INVENTED `gd`-setting Defence → DA map in the design addendum.
- **jack-ryan:** delta-gate rows 19 and 20 and the 20 / 12 denominators.

*Addendum 2 signed:* elrond (data steward and archivist), 2026-10-14. Run JOIN-1, conductor gandalf. Read-only on every store touched.

---

## 9 · Addendum 3, 2026-10-14: D2 potions join as row 21 (conductor ruling, KC2 KP-423). Count 20 → 21, a third NAMED FINDING

**Source of the change.** Conductor gandalf, KC2-PLAY ledger **KP-423** (`gandalf/notes/2026-09-20-kc2-play-run-charter.md`, collab `edf2b88bc`). gamora's J4b ADDENDUM-2 (engine `20ff8684`) found that **neither this census nor P0 mentions potions**, yet the sealed oracle gives the Warlord a health potion. **Ruling:** *"admit D2 potions (health / mana / rejuvenation, with the belt as the count limit) as row 21."* Rows 1–20 and their classes are unchanged. §§ 7–8 are left as committed (`20790cd34`, `9096b2e97`). Where § 9 corrects § 8.3, § 9 governs.

**This was an omission, not an exclusion, and the record should say so plainly.** P0 § 7.2 warns that "not censused" and "censused and excluded" must stay distinguishable. Potions were not censused at all. The census enumerated her pinned `Skills.txt` rows, `Missiles.txt` and the kit record's skills. A potion is none of these: it is a **universal player consumable**, not a skill of her kit. So no record this seat read carried a field for it. This is the same blind spot that § 11 of the P0 note named for B-15: an engine law with no field on the kit's own records. The § 7.3 sweep of her defensive sheet also missed it, because it read the sheet's *stats*, not its *consumables*. The fix is noted as a method lesson in § 9.6.

### 9.1 · The GD referent (read-only, engine HEAD `20ff8684`)

- **Potion law:** `counterplay.Kit` K-4, MEASURED from the consumable CSV. Rows `defaulthealthpotion.dbr` (800 flat + 25 % of max HP instant, 12.0 s cooldown, 1 charge) and `healthpotion_healovertime.dbr` (25 % over time, spread over the potion's own 12 s cooldown) (`counterplay.py:451–465`, `:707–731`).
- **Drink trigger:** a threshold theta on the HP fraction, **IDENTIFIED** from the reference player's 60 fps HP-bar trace (OBS-H2-5, `potion_threshold_frac()`). Under the oracle's split rule it is evaluated at the **end-of-tick sample** it was identified against (`sustain_procs.SPLIT_RULE`). It is driven on the **run-wide** clock (`run.py:3595–3627`).
- **Permission:** the drink is `RequestUseItem`, decoded **PERMITTED in every control state**, so it is deliberately not gated by `refuse_actives` (`counterplay.py:627`, `run.py:3627–3629`).
- **Pool:** **life only.** The oracle has no mana or energy potion anywhere (grep over `counterplay.py`).
- **Supply:** **no count is consumed.** `potion_charges` is read into the Kit and never decremented, so the only supply limit is the 12 s cooldown. The GD referent for a count limit is therefore *"unbounded, cooldown-gated"*. That is an **implicit oracle assumption, not a measurement**, because nothing measured the reference player's stack.

### 9.2 · Row 21

| # | Mechanism | Evidence (mechanism / magnitude) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| **21** | **D2 belt potions: health and mana potions restore their pool over a duration; rejuvenation restores a share of both pools at once; every drink spends one potion from a finite belt.** The kit record's loadout names the belt (**Arachnid Mesh**, `d2-fire-sorc.json` `item_alterations`). Heals land on her anchored life; mana lands on her native mana pool (row 2) | **MV, not sourced this session**, for all the D2 laws: heal and restore amounts and durations by tier, the rejuvenation shares, drink and concurrency rules, belt slots for her belt, and whether the belt refills. legolas adds these to C-13 (KP-423). **NONE** for every magnitude until then. The belt's presence is **att** (kit record) | **BOUNDARY** (the player's consumable-sustain layer × the run-wide clock × agency) | `counterplay` K-4 (§ 9.1): instant flat + %, plus heal-over-time across a 12 s cooldown; life only; trigger = IDENTIFIED theta; permitted under every control state; no count consumed | **WIDEN.** Candidate lever **L-S7 `player_potion_model`** {`gd` (K-4 at its measured values; count unbounded, cooldown-gated, **DECLARED**) \| `d2-belt`}. Settable. The id is registered by the delta Gate-2 |

**Why BOUNDARY rather than INTERNAL.** I considered INTERNAL seriously, because row 2 (mana income) is INTERNAL and a mana potion is a mana income. It does not hold, for two reasons. First, a potion is **not a mechanism of her kit**. It is the game's universal player consumable, the same in every D2 build, just as GD's `defaulthealthpotion` belongs to every GD character, not to the Warlord's kit. Second, in the oracle it is driven by the **world**, not by a kit record: the run's counterplay/sustain layer, a bound player policy, the run-wide clock and a decoded control-state permission. Those are rulebook terms. The precedent is row 17 and P0 B-16: a universal engine law acting on the player is BOUNDARY, even where it touches a native pool.

**Why WIDEN rather than AS-IS.** GD's form cannot express D2's law at any setting of its existing terms:
- **Heal shape.** GD's potion is an instant plus a drip over its own cooldown. D2 health and mana potions restore over a duration with no cooldown. Zeroing GD's instant and cooldown does not reproduce D2's rule, because the drip is spread over the cooldown and D2's concurrency rule (pending legolas) has no GD term.
- **Pools.** The oracle's potion restores life only. It has no mana target and no two-pool instant (rejuvenation).
- **Count.** The oracle consumes no count. D2's belt is a finite supply, spent per drink.

**Why WIDEN rather than GD-EMPTY.** GD has a potion rule with measured values, and the `gd` setting reproduces REFERENT-v1 exactly. That is the WIDEN default property (P0 § 7.1; cf. row 19's measured zero). The mana and rejuvenation pieces have no GD counterpart in the oracle. They are terms the `d2` setting adds inside the lever, the same way row 19's block step and lock are. They are not a GD-silent boundary question of their own. ⚑ **One sub-term carries no GD measurement and must be labelled:** the count limit's `gd` value ("unbounded, cooldown-gated") is DECLARED, not MEASURED (§ 9.1). The registry prints it that way, per P0 § 7.1's rule that silence must not be laundered into a measured default.

**Falsifiers.** For WIDEN over AS-IS: any setting of the K-4 terms that reproduces a D2 duration-based restore with D2's drink rules, a mana target and a consumed count. For BOUNDARY over INTERNAL: a reading in which her potions are records of her kit rather than the game's universal consumable, for example a kit-specific potion skill in her pinned rows (there is none).

### 9.3 · One row, not two: health and mana potions are not separate rows under my method

**My method does not require a split, so I am not stopping.** P0 § 1 makes a row for one distinct mechanism, or one distinct question the boundary must answer.

- **One mechanism.** Health, mana and rejuvenation potions are one law: drink one belt potion, restore pool P by amount X over duration d. Rejuvenation is the same law with d = 0 and two pools. The target pool and the magnitude are **operands** of that law. The precedents are row 1 (two skills' mana spend in one row), row 3 (three damage sources in one row) and row 5 (mastery plus gear in one row).
- **One boundary question, with a shared constraint.** All three are drunk under one policy, on one clock, under one control-state permission, and **from one belt**. The belt is a single count limit across all potion types. Splitting by pool would split that constraint across rows and count the supply question twice.
- **The unit rule is an operand difference, not a mechanism difference.** Under gamora's ADDENDUM-1 unit rule, life restored is a kit-life quantity (× r_DMG) and mana restored is kit-internal (native). Rejuvenation carries both units in one drink. That is a per-pool operand rule, already stated in ADDENDUM-1.
- **The nearest thing to a split, named so it can be checked.** The **mana drink trigger** has no GD referent (§ 9.4). A trigger with no referent is a *setting* of the row's policy term, labelled DECLARED-INVENTED. It is not a separate boundary question. Row 17 is the precedent: its GD referent is `NONE` and its JOIN default is DECLARED-INVENTED, inside one row (A-5). If jack-ryan's delta gate reads the mana trigger as a distinct question instead, the split would be 21 → 22, and I would record it as a further named finding.

### 9.4 · Her drink policy, and the units

- **The drink policy is JUDGED (conductor, KP-423), mirroring the Warlord's threshold law where D2 is silent.** D2 has no drink policy: the player decides.
- **Health potions:** the mirror is GD's IDENTIFIED theta on the HP fraction. ⚑ Under the oracle's split rule, an identified threshold is evaluated at the scalar it was identified against, the **end-of-tick** HP fraction. A mirror that evaluated it on a different scalar (for example the within-tick floor) would be a different law, so gamora's ADDENDUM-3 states which scalar it uses.
- **Mana potions and the mana half of rejuvenation:** the Warlord has no mana potion, so there is **no GD threshold to mirror.** Any mana trigger is **DECLARED-INVENTED** inside the JUDGED policy, and is labelled so wherever it runs (P0 § 7.1). This bears directly on gamora's Meteor-starvation prediction, which KP-423 re-registers after row 21 is built.
- **Control-state permission:** GD's referent is PERMITTED in every control state (§ 9.1). The D2 setting (whether she can drink during hit recovery, the block lock or her cast lock, rows 17, 19 and 9) is part of legolas's sourcing. Until it is sourced, any JOIN setting is labelled.
- **Units:** heal amounts are **D2 units × r_DMG** (kit-life quantities, ADDENDUM-1 unit rule). Mana restored is **native** (kit-internal). Durations are native D2 frames on the WARN-2 integer timeline. The belt count is a native integer.

### 9.5 · THIRD NAMED FINDING: the Sorceress's denominators after KP-423

**Reason:** conductor ruling **KP-423** (collab `edf2b88bc`). Potions were an omission found by gamora (engine `20ff8684`), and the ruling stands on Matt's KP-420. **This addition comes after her J0 Gate-2 anchor** (charter v0.5.1 (1), `b48500a4d`), so it is a named finding (charter § 4.5), printed with its reason. It is not a silent re-map. It is the third such finding, after § 7.5 (KP-420, block) and § 8.3 (KP-421, intake hit law). It makes coverage harder and lands before J4b is graded.

| Fraction | J0 anchor | After KP-420 | After KP-421 | **After KP-423 (this finding)** | Why |
|---|---|---|---|---|---|
| **(a)** all rows | 18 | 19 | 20 | **21** | row 21 added |
| **(b)** all BOUNDARY rows | 10 | 11 | 12 | **13** | row 21 is BOUNDARY |

**Corrected frozen record (after KP-423): 21 rows.**

| Class | Count | Rows |
|---|---|---|
| INTERNAL | 7 | 1–7 |
| **BOUNDARY** | **13** | **AS-IS 2**: 13, 15 · **WIDEN 7**: 8, 9, 10, 17, 19, 20, **21** · **GD-EMPTY 4**: 11, 12, 14, 16 |
| OUT-OF-ARENA | 1 | 18 |
| HELD | 0 | — |

**Restated in one line:** INTERNAL 7 · BOUNDARY 13 · OUT-OF-ARENA 1 · HELD 0 = **21**. Candidate levers surfaced since the J0 Gate-2: L-S5 (row 19), the intake-direction settings of L-04/L-05/L-06 (row 20; gamora calls this L-S6), and **L-S7 `player_potion_model`** (row 21).

### 9.6 · Consequences beyond her census (named, not acted on)

- **⚑ The Barbarian has the same omission.** P0's D2 WW Barbarian record (16 rows after P0 § 11) has no potion row either. Under KP-420 (f), he inherits the enemy-anchored key with both sides anchored, and his comparison against the Warlord carries the same bias KP-423 ground (2) names. **Adding a row to his frozen record is the conductor's call, not this seat's** (the A-4 precedent). If admitted, it is a named finding against J-S2: **16 → 17, his (b) 11 → 12.**
- **Method lesson for every later census.** Enumerating a kit's own records cannot see **universal player laws that carry no field on those records**. This census has now missed three: monster hit recovery from melee (B-15), potions (row 21), and, until KP-420 made it a question, the intake hit law (row 20). Each later census should run one explicit sweep of the universal player layer (consumables, recovery, avoidance, the intake hit law, control-state permissions) against the GD oracle's player-side modules, in addition to the kit-record enumeration.

**Owed downstream (not this seat's):**
- **legolas:** the 1.13 potion laws for C-13: amounts and durations by tier, rejuvenation, drink and concurrency rules, belt slots for Arachnid Mesh, refill, and drinking under control states.
- **gamora:** ADDENDUM-3, covering row 21's form, the drink-policy scalar (§ 9.4), the labelled mana trigger and a negative control.
- **jack-ryan:** a later delta covering row 21, including the § 9.3 one-row reading.
- **The conductor:** the Barbarian disposition (§ 9.6).

*Addendum 3 signed:* elrond (data steward and archivist), 2026-10-14. Run JOIN-1, conductor gandalf. Read-only on every store touched, including the GD oracle at engine HEAD `20ff8684`.

---

## 10 · Addendum 4, 2026-10-14: the universal-player-layer sweep (conductor ruling, KC2 KP-426). Count 21 → 27, a fourth NAMED FINDING

**Source of the change.** Conductor gandalf, KC2-PLAY ledger **KP-426** (collab `99d55f74e`). It rules on this seat's sweep batch, which KP-424 commissioned: *"ONE universal-player-layer sweep for both D2 kits before any J4b build."* That sweep is the method lesson of § 9.6, applied once instead of one omission at a time. **Method:** the oracle's player-side modules under `simulation/kc2/`, read-only at engine HEAD `20ff8684`, checked against every law D2 1.13 applies to any character. **Every D2 law cited in §§ 10.1–10.2 is MV, unsourced this session; legolas sources them in C-13.** Rows 1–21 and their classes are unchanged. §§ 7–9 are left as committed. **Lever ids registered since § 9 (KP-425):** row 19 → **L-23 `player_block_model`**; row 20 → **L-24 `intake_hit_law`** (intake only). These replace the provisional L-S5 and L-S6.

### 10.1 · Rows 22–27

| # | Mechanism | Evidence (mechanism / magnitude) | Class | GD's rule (read-only ref) | Verdict |
|---|---|---|---|---|---|
| **22** | **GD control families landing on a D2 player.** Stun, Sleep, Trap, Immobilize, Knockdown, Freeze and Petrify, delivered by GD monster skills. D2 players have no sleep, trap or petrify state; D2's own stun and freeze run on D2 duration rules. Cannot Be Frozen and Half Freeze Duration are her sheet's operands (none is on her pinned items) | MV / NONE (her D2 control-resistance operands are unset; legolas's leg) | **BOUNDARY** (CC/status on the PLAYER) | `control_application`: one timeline per family on the target, **longest wins**, never additive; exactly **one** involuntary effect acts, chosen by the decoded ladder; per-family resists from sheet 519 (`player_control_resists()`, `None` ≠ 0); `suppression_matrix()` governs what a controlled player may request. ⚑ **`gd` value (settled 2026-10-14, gamora, read-only on the sealed oracle `969fbd8d`): APPLIED** (armed, `ApplicationLimb.RECORD`; `scripts/gamora_kc2_w1w2_lift_build_2026_08_25.py:179-181`, `control_application.py:403-406`), **UNREACHED on the J-S8 board** (the G6 status grain is empty). ⚑ So this row's negative control may be unreachable on this board. It then reports REACHED-INSENSITIVE or needs a forced-landing control; gamora decides which in J4b ADDENDUM-4 | **WIDEN → L-12 `control_family_registry`, receiving direction,** plus a D2 duration law setting. The registry must say how each GD family lands on a D2 player, including the three D2 has no state for, and refuse loudly on an unmapped family (P0 § 7.1) |
| **23** | **DoTs landing on a D2 player** (GD burn, frostburn, poison, bleed, and the rest) | MV (D2 per-type rules, e.g. a new poison replacing a weaker one; poison length reduction) / NONE | **BOUNDARY** (damage over time × tick clock, intake) | `dot_timeline`: decoded (`Game.dll`, D-4c), keyed `(damage_type, ATTACKER)`, 100 ms buckets, same source **MAX**, distinct sources **ADD** | **WIDEN.** The `gd` setting is the decoded rule; the `d2` setting applies D2's per-type rules on the receiver. The magnitude still goes through row 25's family map and her resists |
| **24** | **Chill: in D2, cold damage slows the player.** It is a rider on the damage type, not a control row. Cannot Be Frozen and cold length reduction are operands | MV / NONE | **BOUNDARY** (status on the PLAYER, triggered by damage type) | **None.** GD's slows are `debuff`/`modifier` kinds, which `threat.NON_HEALTH_KINDS` routes off the health path and never applies. No damage-triggered slow on the player exists in `kc2/` | **WIDEN**, GD referent **`NONE`**, with a **DECLARED-INVENTED** JOIN default `off` that reproduces REFERENT-v1. This is the row 17 / A-5 precedent. Kept separate from row 22 by ruling (KP-426): the trigger is a damage type, not a GD control family. ⚑ Whether chill slows casting (and so couples to row 8) is part of legolas's sourcing |
| **25** | **Intake damage-family map:** GD damage families that have no D2 resistance. Pierce, Chaos, Aether, Vitality ("Life"), Acid, Bleeding and the folded "Elemental", plus their DoT forms | DM (GD's family list in `RESIST_PCT`) / **DECLARED** (each map entry is a choice; D2's own resist set is fire, cold, lightning, poison, plus physical and magic reduction) | **BOUNDARY** (damage type vs resistance, intake; B8 registry) | `threat.RESIST_PCT`: per family, form `× (1 − res/100)`; an unmapped family raises `KeyError` (GL-12: "name it in RESIST_PCT … do not guess a resistance") | **AS-IS in form, DECLARED in operand** (the row 13 and 15 shape). This is the intake twin of row 15, stated per direction (W1). The map is gamora's to declare, entry by entry. § 7.3's fire, cold, lightning, poison and physical entries become its first five rows |
| **26** | **World and arena modifiers on the player.** The Vanguard Banner (`offensiveTotalDamageModifier +100 %` within 8 m) and the player-side mutator clauses: Cruel (×0.92 outgoing for 1 s after any monster hit), Resilient (+8 % max poison/acid and bleeding resistance), Ascended (+8 % damage, added into the pool; ×1.08 as the sensitivity). Leeching's use of her leech resistance is an operand (§ 10.3) | DM (`defenses.py`, `mutators.py`; Ed IV `*_u.dbr`, sha-pinned) / DM | **BOUNDARY** (world → kit composition) | `defenses` (the banner multiplier, per tick from the player's position) and `mutators` (hook sites in `resolve_attack` and `run.simulate_wave`). ⚑ **Banner `gd` value (settled 2026-10-14, gamora, read-only on `969fbd8d`): LIVE**, `offensiveTotalDamageModifier +100 %` within the measured 8 m (`kc2/defenses.py:11-19`, `:86`), applied through `PlayerOffense.banner_factor` (`run.py:2939`, `:3070`/`:3072`/`:3127`). Composition per `BANNER_ADDITIVE_OF_RECORD = True`: the +100 % is ADDED into the sheet's own damage modifier, not multiplied onto the result (`player_offense.py:484-491`; engine prereg `kc2-play-v3p2-lift-prereg-2026-09-20.md` § 228ff). MIGRATION records V311-FULL as including the six mutators | **AS-IS.** GD's form (a dimensionless multiplier, or an addend into the damage pool) expresses each clause unchanged. What must be **declared** is where each lands in D2's composition: **the banner's +100 % and Ascended both add into row 5's pool**, following the oracle's additive limbs of record (Ascended has ×1.08 as its sensitivity); Cruel multiplies total outgoing; Resilient's +8 % goes onto her D2 max poison resist (D2 has no bleed resist to raise) |
| **27** | **Stamina.** Running drains stamina; at zero she walks. Battle Orders and Energy do not apply to her; her stamina pool and run drain come from her D2 sheet | MV / NONE | **INTERNAL** (her own resource, gating her speed) | None. GD has no stamina; the referent's movement is MEASURED (`movement`, `player_locomotion`) | Native: a resource primitive on her own state, like mana in rows 1–2. It binds because the JOIN pilot moves her (the referent moves about 63 % of the time, `REF_FRAC_MOVING_FIGHT`). Her run speed and FRW are operands (§ 10.3) |

**Why each class, briefly.**
- **Rows 22–24 are WIDEN, not GD-EMPTY.** Each has a GD setting that reproduces REFERENT-v1: the decoded control law, the decoded DoT rule, and for row 24 the declared-invented `off`. That is the row 17 precedent.
- **Rows 22–24 are not AS-IS.** GD's form cannot express D2's receiver-side laws. D2 has no sleep, trap or petrify; it stacks DoTs per type, not per attacker; and it chills on damage type.
- **Rows 25 and 26 are AS-IS.** GD's form expresses them; only operands and placement are declared.
- **Row 27 is INTERNAL** by the row 1–2 precedent.

**Falsifiers.**
- Row 22 WIDEN → AS-IS: a D2 primary source showing that D2 players have states equivalent to all seven GD families under a longest-wins law.
- Row 23: a D2 source showing that DoTs on the player stack per attacker the way D-4c's rule does.
- Row 24 → no row: a D2 source showing that cold damage does not chill players in 1.13.
- Row 25 → WIDEN: a GD family whose intake needs a form other than `× (1 − res/100)` against her D2 sheet.
- Row 26 → WIDEN: a clause whose placement in D2's composition has no GD-form analogue.

### 10.2 · Excluded, with fidelity-cost lines (KP-426)

| Excluded | Why | Fidelity-cost line |
|---|---|---|
| **Curses and debuffs received** | D2 curses need D2 casters; the arena's monsters are GD bodies. GD's own debuff and modifier kinds are routed off the health path for **both** arms (`threat.NON_HEALTH_KINDS`, a declared under-read). This is a **referent gap**, not a join question | "GD monster debuffs and modifiers on the player are not applied in either arm (referent under-read). A D2 kit's curse-received law (D2 curse durations on players) is therefore moot. Direction: both arms take less than at home; the margin's direction is unknown." |
| **Monster mana drains and cooldown lockout** (`SlowManaLeach`, `ManaBurnDrain`, `Disruption`) | Routed off the health path for **both** arms as declared under-reads (`threat.NON_HEALTH_DAMAGE_TYPES`, `DECODED_NON_HEALTH_TYPES`). Another referent gap | ⚑ **"Monster energy and mana drains and the Disruption cooldown lockout are not applied in either arm (referent under-read). THIS EXCLUSION FAVOURS THE SORCERESS:** she is a mana-bound kit (row 1; the Meteor starvation prediction) with a cooldown on Meteor (row 7), so an unapplied drain or lockout spares her more than it spares the Warlord. Her anchored margin is biased UPWARD by an unknown amount from this line." |

### 10.3 · Operands confirmed by KP-426 (no rows)

- **Life regen and Replenish Life** → `PLAYER_REGEN_HP_PER_S`, D2 units × r_DMG.
- **Run speed and FRW, and body radius** → locomotion and geometry, through the declared D2-units-to-metres conversion that row 13 also needs.
- **Defence against GD's %-current-life attacks** (`intake.PclLimb`'s answering defence) → **0**. D2 has no such stat, so 0 is a D2 fact, not an invented value.
- **Her resistance to monster life leech** (`LEECH_MULTIPLIER`, the Leeching mutator) → **0**, so the multiplier is 1.0. D2 has no such stat.
- **Cannot Be Frozen, Half Freeze Duration, cold and poison length reduction** → operands of rows 22–24.
- **The Hell resist penalty, cap and +max, and physical damage reduction** → as § 7.3, and now as entries in row 25's map.
- **Her own life leech** → 0: D2 spells do not leech.

### 10.4 · FOURTH NAMED FINDING: the Sorceress's denominators after KP-426

**Reason:** conductor ruling **KP-426** (collab `99d55f74e`), the universal-player-layer sweep commissioned at KP-424. **This addition comes after her J0 Gate-2 anchor**, so it is a named finding (charter § 4.5), printed with its reason. It is not a silent re-map. It is the fourth such finding (after KP-420, KP-421 and KP-423). It makes coverage harder and lands before any J4b build.

| Fraction | J0 anchor | KP-420 | KP-421 | KP-423 | **KP-426 (this finding)** |
|---|---|---|---|---|---|
| **(a)** all rows | 18 | 19 | 20 | 21 | **27** (+22…27) |
| **(b)** all BOUNDARY rows | 10 | 11 | 12 | 13 | **18** (+22…26; row 27 is INTERNAL) |

**Corrected frozen record (after KP-426): 27 rows.**

| Class | Count | Rows |
|---|---|---|
| **INTERNAL** | **8** | 1–7, **27** |
| **BOUNDARY** | **18** | **AS-IS 4**: 13, 15, **25**, **26** · **WIDEN 10**: 8, 9, 10, 17, 19, 20, 21, **22**, **23**, **24** · **GD-EMPTY 4**: 11, 12, 14, 16 |
| OUT-OF-ARENA | 1 | 18 |
| HELD | 0 | — |

**Restated in one line:** INTERNAL 8 · BOUNDARY 18 · OUT-OF-ARENA 1 · HELD 0 = **27**.

**Settled 2026-10-14 (gamora, read-only on `969fbd8d`; it replaces this addendum's "pending" text, which is in git at `8fdf4c267`):** row 22's control fold is **APPLIED, UNREACHED on the J-S8 board** (its negative-control form goes to gamora's ADDENDUM-4). Row 26's banner is **LIVE**, composing additively. Neither changes a class or a count.

**Owed downstream (not this seat's):**
- **legolas:** source the D2 laws behind rows 22–24 and 27 (control states and durations for players, the DoT rules on players, chill, stamina) with grades, in C-13.
- **gamora:** declare row 25's map entry by entry and row 26's placements, and settle row 22's negative-control form (REACHED-INSENSITIVE vs a forced landing) in ADDENDUM-4.
- **jack-ryan:** delta-gate rows 21–27 and the 27 / 18 denominators.

*Addendum 4 signed:* elrond (data steward and archivist), 2026-10-14. Run JOIN-1, conductor gandalf. Read-only on every store touched, including the GD oracle at engine HEAD `20ff8684`.

---

## 11 · Corrigendum, 2026-10-14 (jack-ryan census delta Gate-2 INFO-3, collab `1a4bee308`; KC2 KP-427). Text only, no class or count change

**The taxonomy rule, stated once for this census:**
- **BOUNDARY / GD-EMPTY:** the `d2` side needs a **built body or entity** that the oracle does not have. Examples here: rows 11, 12, 14 and 16 (the L-14 and L-19 to L-21 build items).
- **BOUNDARY / WIDEN with GD referent `NONE`:** a **settable switch whose `off` reproduces REFERENT-v1**. Its `off` default is labelled DECLARED-INVENTED. Examples here: rows 17 and 24.

A `NONE` referent can occur in either class. **What decides the class is whether reproducing the referent takes a switch or a build.**

**Correction to § 7.2.** In row 19's reasoning, the bullet "Not GD-EMPTY" opens: *"P0 § 7.1 reserves GD-EMPTY for a boundary question with no GD rule at all, where the registry's referent must read `NONE`."* That definition also describes rows 17 and 24, which are WIDEN. It is **superseded by the rule above**. Row 19's own class is unchanged: its referent is a measured 0.0, and `gd` reproduces REFERENT-v1 by a setting, so it is WIDEN under either wording. P0 § 7.1 carries the same rule (P0 § 14).

*Corrigendum signed:* elrond, 2026-10-14.

---

## 12 · Addendum 5, 2026-10-14: her build file is pinned (Matt, KC2 KP-435 / KP-436); the mercenary is OUT. No row added, count unchanged at 27 / 18

**Source.** Matt, KC2 **KP-435** (her endgame sheet comes from a pinned build file) and **KP-436** (collab `0ac88e6ef`). The build file is legolas C-14, `agentic_orchestration/legolas/research/2026-10-14-join1-c14-sorc-build-file/`: the Maxroll S14 Meteor guide, **Standard** variant, verbatim (planner profile `gca1a0l6`, `build_file_standard_verbatim.json`), resolved in 1.13 (`sorc_build_sheet.json`). Matt's three rulings:
1. the Standard variant, as written;
2. **Battle Orders always on**, as a precast buff held for the run (a sheet operand, checked against fight length);
3. **"Mercenaries are out. Period."**, for every kit.

**What this addendum records.**

- **The mercenary: a home mechanism not joined.** The build file equips an Act 2 mercenary (type 11, level 98): Infinity on an ethereal Giant Thresher (Conviction aura level 12), ethereal Fortitude, ethereal Andariel's Visage. The guide's prose names a Might-aura mercenary and pairs him with Static Field "to take out Immunes". **The mercenary is a separate actor, and he does not join.** Fidelity-cost line: *"Her home mercenary (Infinity Conviction: lowers enemy resists, and in 1.13 can break some fire immunities; Might; his own damage, body and aggro) is not joined. Direction: her offense against high-fire-resist bodies, and her survival (he draws attacks), are both UNDERSTATED relative to her home build."* **By Matt's ruling, no later option to admit a companion actor is held open.**
- **The sheet source changes; the census does not.** Her sheet operands (life, mana, Defence, block, resists, FCR/FHR/FBR, damage reduction, +skills) are now read from the pinned build file instead of the KP-428 defaults. Every one of them is already an operand of an existing row. The sheet is data; it adds no mechanism.
- **The build-file sweep against this census is with the conductor** (one batch, returned 2026-10-14). **No row is added here.** Any row the conductor admits is recorded as its own named finding.

*Addendum 5 signed:* elrond, 2026-10-14. Run JOIN-1, conductor gandalf. Read-only on every store touched.
