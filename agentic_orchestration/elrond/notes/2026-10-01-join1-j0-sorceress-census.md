# JOIN-1 J0: the D2 Fire Sorceress INTERNAL / BOUNDARY census (J-S3b)

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
