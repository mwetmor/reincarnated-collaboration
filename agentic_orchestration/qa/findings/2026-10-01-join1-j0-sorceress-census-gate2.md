# Finding — 2026-10-01 — JOIN-1 J0 Gate-2: the D2 Fire Sorceress INTERNAL/BOUNDARY census (J-S3b)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, Run JOIN-1; conductor gandalf)
**Severity:** ⚑ **WARN, i.e. PASS WITH WARN.** 0 BLOCK · 4 WARN · 9 INFO. **The count and every row's class FREEZE here. J3 may open.**
**Target:** elrond census `agentic_orchestration/elrond/notes/2026-10-01-join1-j0-sorceress-census.md` (collab `b4d151a4a`), and conductor ruling KC2-PLAY ledger **KP-162** (`d6065093a`)
**Developer:** elrond (census) · gandalf (KP-162 ruling)
**Principles applied:** REVIEW_PROCESS #1 (math/evidence before code), #3 (cross-seam impact), #4 (decisions-log/charter as truth), #5 (severity matters). Disciplines #10 (empirical inspection over assumption), #12 (semantic shift named), #75 cl. 6 (a remedy does not inherit its predecessor's instrument). ADR-002 (tiered approval), ADR-004 (cross-seam).

---

## 0 · Frozen result

| | Value |
|---|---|
| **Fraction (a) denominator** | **18 rows**, unchanged from the census |
| **Per-row classes** | **INTERNAL 7** (rows 1–7) · **BOUNDARY 10** (rows 8–17: **AS-IS 2** = 13, 15 · **WIDEN 4** = 8, 9, 10, 17 · **GD-EMPTY 4** = 11, 12, 14, 16) · **OUT-OF-ARENA 1** (row 18) · **HELD 0** |
| **Fraction (b) population** | ⚑ **10 rows, all BOUNDARY rows (8–17)**, not the census's 4. See W2: this follows J-S2's convention for the Barbarian and is the only reading under which KP-162's four builds can be seen by (b) |
| **Reclassification anchor** | This gate (charter § 4.5, RC3-W1(c)). Any later addition, removal or reclassification is a named finding |
| **Operand list (row 4)** | Fire Bolt (36), ⚑ **plus Inferno (41)** per the A-1 ruling. Neither adds a row |

**Re-derivation.** I did not take the classes on trust. Every row was re-read from the pinned sources this session. The three FILE digests the census cites reproduce exactly: `Skills.txt` `59601208…`, `Missiles.txt` `9d6794a5…`, `d2-fire-sorc.json` `43eb1e55…`. Every field value quoted in rows 1–18 matches its source, including the ones a misreading would most likely get wrong: `mana/lvlmana/manashift/minmana` on 47 and 56; `delay=30`; `Param1=6`/`Param2=0`; `Param3=30`/`Param4=15`; `fireball` `Vel 20 / Range 50 / CollideType 3 / CollideKill 1 / sHitPar1 4 / GetHit 1`; `meteorcenter` `Range 60 / AlwaysExplode 1 / GetHit 1 / HitSubMissile1 meteorfire`; `meteorfire` `pSrvDoFunc 5 / pSrvDmgFunc 3 / DamageRate 41 / dParam1 19 / ApplyMastery 1 / EDmgSymPerCalc skill('Inferno'.blvl)*3`; `interrupt=1` on 47 and 56 and empty on WW; `ToHit`/`LevToHit`/`ToHitCalc` empty on 47 and 56, against WW `LevToHit=5` and BO `ToHit=50`. The census's oracle claims also reproduce at engine HEAD `22cd2288`: no `kc2/` module reads `res_fire`; no player-side zone exists; `action_permission` is imported by nothing.

**Method fidelity to P0** (`78797db4b` § 1). Each row is one mechanism or one boundary question. Row 7 (cooldown, INTERNAL with an AS-IS-on-the-clock verdict) follows P0 VS row 2. Row 13 (AS-IS in form, EMPTY in operand) follows P0 WW row 4. Rows 11/12/14/16 (no oracle body to parameterise) follow P0 § 7.1 and L-14. Rows 9 and 17 (an existing oracle mechanism lacking a term) follow P0 L-10. Row 18 follows P0 § 7.2. **I found no row whose class is wrong, and no in-scope mechanism that is missing.** One out-of-scope mechanism is unnamed (W4).

---

## 1 · What I found

The census is sound. Its count reproduces from source, and each of its 18 classes follows P0's method. Its four headline findings hold. Headline 3 is right about the operand but **mis-states the rule around it**: the offense path has no family registry at all (W1). That correction reaches back into the charter's § 4.5 `KeyError` clause, and into my own RC3-W2, which carried the same conflation. The five ambiguities rule cleanly; none of them changes her count or any class. **A-4 does change the Barbarian's count**, by two rows rather than one, because P0 also missed his player-side hit recovery: Battle Orders carries `interrupt=1` (DATAMINED). KP-162's "build, don't approximate" ruling is consistent with § 4.5, on four conditions (§ 3). The most important condition is that fraction (b) must count GD-EMPTY rows. Otherwise the four bodies the ruling builds are invisible to the one fraction that "says whether a kit joined or merely compiled".

---

## 2 · The five ambiguities, ruled

### A-1 · Inferno (41): **PIN IT as a fourth operand row.** Do not record it as unset.

- **The pin's own operand clause admits it.** J-S3b: operand rows *"enter ONLY as the operands those two rows … reference"*. Row 56 references Inferno through its own data chain: `srvmissilea=meteorcenter` → `HitSubMissile1=meteorfire` → `EDmgSymPerCalc = skill('Inferno'.blvl)*3`. That is DATAMINED and verified. The enumerated list is an under-inclusive instance of the rule, and the rule governs.
- **The game itself names Inferno as a Meteor synergy.** In `SkillDesc.txt` (same raw directory, FILE sha256 `1d5994c58e1965f4900b839e88a9f10fec15b1497728005b85f98954e103df0f`), the `meteor` row's synergy panel has four lines: Fire Bolt (`Firedplev`, `par8`), Fire Ball (`Firedplev`, `par8`) and **Inferno** (`dsc3line4`, `skillname41`, `AFDImm`, calc `3`). The census did not consult it, and it settles the question.
- **What the kit record says: nothing about Inferno.** Its traits line and capstone `synergies` read *"Meteor synergizes Fire Ball and Fire Bolt; Fire Mastery amplifies all fire skills."* That silence is not a vote against. The record also never names **Warmth**, which J-S3b pins on an inference from "mana-hungry". The record's vote under RC3-W1 is over **castable** scope, and it names exactly two castables. I authored RC3-W1, and its intent was to stop the conductor from *choosing* castables in-run. Applying the operand clause's own rule is not a choice.
- **"Unset" would be false.** Inferno's `blvl` is **not unknown at its floor**. Build legality forces it to at least 1: Meteor `reqskill2` Fire Wall → Fire Wall `reqskill1` Blaze → Blaze `reqskill1` Inferno, all DATAMINED. By the same logic, Fire Bolt ≥ 1 (Fire Ball `reqskill1`).
- **Magnitude:** `mechanism_grade` DM. `magnitude_grade` is DM for the floor of 1 and NONE above it, which is the same state as Fire Bolt. Points above the floor are a kit-definition operand. Following KP-161, they are a **conductor default operand, each an explicit lever, not a fact**, unless legolas's J4b leg sources an allocation.
- **Not a count or class change, and not post-anchor.** Her anchor is this freeze.
- **Action (conductor):** fold a one-line J-S3b corrigendum: *"Inferno (41): operand, its `blvl` only, via `meteorfire`; its own damage, missiles and cost never enter."* ⚑ **Tell legolas now.** His J4b leg is in flight, and it needs the `meteorfire` synergy and Inferno's level in scope.

### A-2 · The Fire Wall prerequisite: **the pin's effect is right; correct its sentence.** It reaches one row further than the census says.

Fire Wall (51) is referenced directly, as Meteor's `reqskill2`. **Blaze (46) is referenced transitively** (Fire Wall `reqskill1`), and the census does not name it. Both are build legality and fold into row 18. **Corrigendum text (conductor, with A-1):** *"every other Sorceress row is excluded as a mechanism. Rows referenced only as prerequisites (Fire Wall 51 directly, Blaze 46 transitively) fold into the OUT-OF-ARENA legality row. Where a prerequisite forces an operand floor (Inferno ≥ 1, Fire Bolt ≥ 1), row 4 carries the floor."* See I-4 for row 18's wording.

### A-3 · Rows 9, 12, 14 and 16: **each opens its own id. None widens an existing one.**

**The test I applied:** an existing lever widens when the new witness is another setting of **the same primitive**, against **the same GD referent**. A new id opens when either differs. For build items there is one more condition: **one id per separately buildable, separately testable body.** Otherwise a single id can read "built" while one of its bodies is missing, which is coverage laundering.

| Row | Ruling | Id registered at this gate | Kind | GD referent value | Why not the existing id |
|---|---|---|---|---|---|
| 8 | widens | **L-01** `tick_quantisation` (2nd witness) | settable | `continuous-as-proportional` | same primitive |
| 10 | widens | **L-06** `crit_model` (4th witness) | settable | `pth-tiered` | same primitive. ⚑ The value set must gain **`no-roll-no-crit`** (I-3) |
| 11 | widens | **L-14** `player_projectile_model` (2nd witness) | build | `NONE — no GD rule` | same body |
| **9** | **new** | **L-17** `cast_move_lock` | settable | `NONE — not wired`. Decoded-partial evidence: in GD's `CharacterActionPermission` (FILE `ad305866…`), MoveTo during Attack = DEFER and Walk during Attack = REPLACE; DEFER's semantics are undecoded, and so is the mapping from player skill to action class. **DECLARED-INVENTED default `no-lock`** reproduces REFERENT-v1 as built (§ 4.7) | L-10 is a continuous speed scalar on a sustained channel, GD value `100`, measured. A cast lock is a discrete lock whose duration is the L-01 cast clock, and its GD referent sits in the permission decode, not in `channel_policy` |
| **17** | **new** | **L-18** `player_hit_recovery` | settable | **`NONE`**, per A-5. **DECLARED-INVENTED default `off`** | no P0 lever exists |
| **12** | **new** | **L-19** `player_remote_delivery` | build | `NONE — no GD rule` (player side). Monster-side form: `disc.py` circle plus telegraph | a remote, delayed point detonation is a different body from a moving collider that bursts on first collision |
| **14** | **new** | **L-20** `player_placed_zone` | build | `NONE — no GD rule` (player side). ⚑ Its damage application defaults to GD's **decoded** DoT stacking rule (I-5) | a persistent area with a per-frame rate is a third body |
| **16** | **new** | **L-21** `monster_hit_recovery` | build | `NONE — no GD rule`. GD's engine has `TakeHitAction` (enum type 11), but the oracle has no monster control body to apply it to | L-15 `monster_debuff_lane` is a damage-taken modifier on monsters (Impale). Hit recovery is a monster **control state**. Merging them would leave L-15 half-built in JOIN-1 |

**Registry after this gate:** 21 ids = **16 settable + 5 build items** (it was 14 + 2). Build status by item: L-14, L-19, L-20 and L-21 are **BUILD-IN-J4b** (KP-162); L-15 is **REGISTERED-UNBUILT**. Docket sweep M-3's trigger-chain depth is **not** registered, because no JOIN-1 kit witnesses it. Negative controls owed under § 4.4: L-17 and L-18 when their D2 settings are implemented, and **each build item once built** (§ 3, condition 5).

### A-4 · The Barbarian's stagger: **yes, a named finding, and yes, his denominator changes: 14 → 16, not 15.**

- **Row B-15, monster hit recovery from his hits.** WW's melee hits put D2 monsters into hit recovery by engine law. WW carries no Skills.txt field for it, unlike the Sorceress's `GetHit=1` missiles, so the grade is MV (legolas). Class: BOUNDARY, verdict **GD-EMPTY → L-21**.
- **Row B-16, player hit recovery. P0 missed this one too, and the census did not flag it.** Battle Orders (149, pinned in J-S3) carries **`interrupt=1`**, DATAMINED (verified this session). Whirlwind's `interrupt` is empty, so the spin itself is uninterruptible, but his buff cast is not. legolas's timing packet (`b0f9d77fa`) already tables his FHR (`BA GH 5/256`). Class: BOUNDARY, verdict **WIDEN → L-18**.
- **Why add rather than accept the omission.** KP-162 builds monster hit recovery into the **one** rulebook, and L-18 is registered. His `JOIN` profile will therefore either activate both, which would put active mechanisms outside his denominator, or leave both at GD's default, which would be a fidelity cost no fraction can see. Either way an accepted omission makes his fractions blind to rulebook behaviour that runs in his own fights. The denominator freeze (my Gate-1 BLOCK-E) exists to stop a kit's coverage from being made **easier**. These additions make it harder, which is the opposite of gaming.
- **His frozen record after the finding:** **16 rows**: INTERNAL 3 · **BOUNDARY 11** (AS-IS 3 · WIDEN 7 · GD-EMPTY 1) · OUT-OF-ARENA 2. **Fraction-(b) population: 11.** Printed against the launch anchor with this reason. **Conductor records it before J4a is graded. Not a Matt item:** § 4.5 provides for exactly this.
- *Paper-only note:* the same universal hit consequence (PoE stun on hit) is likely missing from P0's Cyclone and Bonestorm rows. No JOIN-1 action; it is recorded for whichever run joins them.

### A-5 · "Damage interrupts the player": **GD's default is SILENCE (`NONE`), not a rule (`off`).**

- The oracle never consults damage to interrupt the player. `control_application` is triggered by control **families**, and `REF_P_CAST_INTERRUPTS = 0.15` is the player cutting his own channel. That is an **omission of the extracted rulebook**, not a decoded rule.
- **The only GD evidence in the tree points the other way from `off`.** GD's decoded action enum has **`TakeHitAction` (type 11)**. In the decoded permission grid (`data/kc2/resid_d1_2_action_permission_matrix.json`, FILE `ad3058664b87945a5c9f8180e5dde36e5a287df0ec36071e3df72b1c5d7766b3`), **TakeHit arriving during an Attack = REPLACE**, and **Attack arriving during a TakeHit = REJECT** (read by index through `action_permission.regime`). So GD's engine *does* let a take-hit interrupt an action. What our substrate lacks is GD's **trigger** law, i.e. when a TakeHit fires.
- Registering `off` as "GD's rule" would launder an oracle omission into a GD setting. P0 § 7.1 names that exact failure.
- **Registry row (L-18):** `gd_referent_value = NONE — trigger undecoded (permission decoded: TakeHit REPLACEs Attack, matrix ad305866…)`. **JOIN default = DECLARED-INVENTED `off`**, author the J3 registrant (gamora), reason "reproduces REFERENT-v1 as built, so § 4.7 holds". D2 setting: `d2-damage-threshold` (FHR law; legolas, MV). L-17 takes the same pattern, as in the A-3 table.

---

## 3 · The conductor's ruling KP-162 (build the four GD-EMPTY rows; do not approximate) against § 4.5 and the denominator

**Consistent, on these conditions.** None of them is a reason to reverse the ruling.

1. **Fraction (b) must count GD-EMPTY rows (W2).** Under the census's WIDEN-only reading, (b) never sees whether Fire Ball flies, whether Meteor lands remotely, whether the fire field persists, or whether monsters stagger. A built body and an approximation would print the same (b).
2. **Building does not reclassify.** A class records **GD's rulebook state at the freeze**. Rows 11, 12, 14 and 16 stay **GD-EMPTY** after their bodies are built. Build status lives in the registry and in (b). Re-labelling a built row WIDEN would be a post-anchor reclassification and a named finding for no reason.
3. **The denominator is unchanged by the build:** (a) = 18, (b) = 10.
4. **The built bodies are JOIN-only.** `ORACLE`/`PLAY` stay byte-identical (§ 4.7). ⚑ **Soulfire stays on its sealed `secondary_streams` reduction**, a period proc with a `SoulfireReach` bracket. Migrating GD's own player projectile onto the new L-14 body would change `ORACLE` behaviour, and that is a **HALT to Matt**, not a lever.
5. **Once built, each body is settable.** The GD side is `NONE` with a DECLARED-INVENTED default of `absent`; the D2 side is the D2 law. Each owes a § 4.4 negative control: flipping it moves a named metric, in the predicted direction, by a recorded magnitude.
6. **Charter counts are stale.** § 2.3 ("two build items") and § 4.4 ("14 settable + 2 build items") should read 16 + 5, with per-item build status (A-3).
7. *Citation, INFO:* KP-162 grounds the ruling on Q86, but Q86 is the **kit-internal** clause and these rows are **BOUNDARY**. The correct ground is P0 § 7.1 (GD-EMPTY means the one rulebook is *extended*, not widened), plus J-L2 and § 4.5's "runs". The ruling stands; its citation should point there.
8. **Cost.** J4b now carries four boundary builds, three of which P0 never had. This needs no new Matt decision. It should appear on the **J3→J4 owner-eye checkpoint** sheet so Matt sees the enlarged J4b before it builds.

---

## 4 · WARN items

**W1 · Row 15's GD-rule cell mis-states the offense path. The § 4.5 `KeyError` guard sits on the intake side, while her damage flows on the offense side.**
- **What exists:** `player_offense.applied_damage(raw, armor, absorption_pct, res_physical_pct, crit_mult)` (`player_offense.py:329`) is a **physical-only** chain. It does not apply *"resistance on every family"*, as the census says. Lightning and bleeding are separate streams hard-wired per family in `secondary_streams` (`:272`, `:289`). The family registry with teeth, `threat.mitigate` over `threat.RESIST_PCT` (`KeyError` on an unmapped family), is the **player's intake** path, keyed to the player's own resistances.
- **Consequence:** the offense side has **no family registry and no refuse-loudly guard**. A D2 fire packet has no path. Routed through `applied_damage` it would take armour plus physical resistance, a **silent** mis-adjudication rather than a `KeyError`. So the § 4.5 RC3-W2 clause (*"a `KeyError` in a joined kit is a runs FAIL"*) is **vacuous for her primary damage**. My own RC3-W2 (`2026-09-29-run-JOIN-1-charter-gate1-recheck.md`, re-check 3) made the same conflation (I-7).
- **Row 15's class and verdict hold.** The form exists (per-stream `× (1 − res/100)`, no armour leg), the family exists, and the `res_fire` operand is on disk. It is AS-IS in form with an EMPTY operand reader, the row-13 shape.
- **Fix:** (a) elrond: a corrigendum line on row 15's GD-rule cell. (b) conductor: § 4.5 states the registry **per direction**: offense needs a family-keyed resistance dispatch with the **same** refuse-loudly discipline, built at **J2** (the FORM/OPERAND split) or J4b, JOIN-only. The registry prints D2 fire as EXERCISED **on offense** only once that dispatch exists and reads `res_fire`. Fold before J2 opens.

**W2 · The fraction-(b) population is defined three ways. Ruled: all BOUNDARY rows.**
- J-S2 says the Barbarian's (b) population is *"9 BOUNDARY"*, i.e. all three verdicts. § 4.5 says *"of the D2 BOUNDARY/WIDEN rows"*. The census reads WIDEN only (4).
- **The ruling is all BOUNDARY rows**, so **her (b) = /10** and his (b) = /11 after A-4. Three reasons:
  - J-S2 is the frozen launch text for the parallel kit, so one definition per charter.
  - AS-IS-in-form rows carry an operand-level "D2 setting active vs REFERENT default" question. Row 13 uses Meteor's radius rather than REFERENT-v1's measured multiplicity; row 15 actually reads `res_fire`. That is P0 finding 5's welded-operand problem, and exactly the "joined vs compiled" signal.
  - GD-EMPTY rows under KP-162 carry a built D2 body (§ 3, condition 1).
- **Uniform definition:** (b)_k = |BOUNDARY rows of kit k whose D2 setting (lever value, operand or built body) is implemented and ACTIVE in k's `JOIN` profile| / |BOUNDARY rows of k|.
- **Fix (conductor):** a § 4.5 text corrigendum, "BOUNDARY/WIDEN" → "BOUNDARY (AS-IS, WIDEN and GD-EMPTY)". Mine to approve under ADR-002 when it lands. Fold before J4a is graded.

**W3 · A-4's two Barbarian rows must be recorded before J4a is graded** (§ 2 A-4). Conductor; a named finding against the launch anchor.

**W4 · Her block is unnamed.** The kit record's loadout carries a shield (Spirit Monarch). legolas's timing packet (`b0f9d77fa`, committed 62 minutes before the census) calls her **block** *"kit-reachable"* and *"MISSING"*. Under J-S3b, gear enters only as an operand of a pinned-row mechanism: Spirit's FCR feeds row 8, its +skills feed row 6, Eschuta's +fire% feeds row 5. Block feeds no pinned row, so **it is excluded and the count stays 18.** But "not censused" and "censused and excluded" must stay distinguishable (P0 § 7.2). **Fix:** elrond adds block to the § 1 "do not enter" list with this reason. The fidelity-cost table carries it as a home mechanism not joined. GD's intake already has the slot (`threat.PLAYER_BLOCK_PCT = 0.0`); D2's full-negate-plus-BL-lock would be a WIDEN if a later pin admits it.

---

## 5 · INFO

- **I-1 · Row 8's magnitude grade is stale at commit time.** The census says the breakpoint table lives in AnimData, *"not among the 34 fetched files"*. legolas `b0f9d77fa` carries `SO SC 14/256/7` (DATAMINED, Basin dump) and reproduces the FCR table 0/9/20/37/63/105/200 → 13…7 ticks (COMMUNITY-VERIFIED, three sources). It also gives Meteor's impact at +60 ticks and its field at `30 + 15·(slvl−1)` ticks. The magnitude grade upgrades from MV. The class is unchanged.
- **I-2 · Row 11 omits a monster-side form precedent.** `deferred_arrival.py` models monster projectile flight (`arrival = cast + ceil((d/v)/period)`), just as row 12 cites `disc.py`'s monster circle. This is relevant to L-14's build cost.
- **I-3 · Row 10's DM half rests on the absence of Skills.txt fields.** `fireball` and `meteorcenter` carry `HitFlags=2`, which is undecoded. Add it to the falsifiers; legolas's J4b leg should confirm there is no AR path through the missile hit flags. Separately, L-06's value set `{pth-tiered | independent-proc}` cannot express VS's shape or hers, so register **`no-roll-no-crit`** as a third value. The interplay with L-04 (a floor at 100 means always hit) is J3's to settle.
- **I-4 · Row 18's verdict text** (*"no fight-boundary meaning"*) is slightly too strong. The legality check does not run in the arena, but it **forces operand floors** that row 4 carries (A-1, A-2). The class is unchanged.
- **I-5 · Row 14's stacking sub-question is ruled now, so it cannot reclassify later.** GD's **decoded** DoT stacking rule (`dot_timeline`: `(damage_type, ATTACKER)` timelines, same-source MAX per 100 ms bucket, `Game.dll` decode D-4c) is the default for the built zone's damage application. If J4b sources a D2 stacking law that differs, it attaches to row 14 as a lever. No new row.
- **I-6 · Fraction (a) and OUT-OF-ARENA rows.** State one convention for both kits. I recommend counting an OUT-OF-ARENA row as mapped when its exclusion disposition is recorded. Otherwise her (a) ceiling is 17/18 and his 14/16.
- **I-7 · Reflexive.** My RC3-W2 said the D2→GD mapping *"lives in the D2 adapter … not as new keys in the sealed `threat.RESIST_PCT`"* and made a `KeyError` her "runs" FAIL. `RESIST_PCT` is the **player's intake** table. The gate that should have caught the intake/offense split wrote it into the charter, and two seats then built on it. W1 corrects it. *A guard that is real in one direction was quoted as covering both.*
- **I-8 · Every census line pin I checked is accurate**, except the two wordings W1 and I-1 correct.
- **I-9 · The J4b research packet has not landed** (`legolas/research/2026-10-01-join1-j4b-d2-fire-sorc/` is absent). The census's MV halves stay conditional, as it says. No verdict here depends on them.

---

## Rationale

- **The count and classes PASS** under P0's method (REVIEW_PROCESS #1 and #4). Every row was re-derived from pinned DATAMINED sources (Discipline #10), and the charter's freeze rule (§ 4.5, RC3-W1(c)) is met.
- **WARN, not BLOCK.** None of the defects is in a count or a class. W1 is a mis-cited rule with downstream consequences at J2. W2 is a charter definition that the freeze must state, and it is stated here. W3 and W4 are records owed. None blocks J3.
- **No ADR-004 cross-seam artifact is owed by this gate.** The registrations in A-3 are charter § 4.4's route, seeded at J3 after the docket sweep applies (RC-I5).

## Action

- [ ] **gandalf (conductor):** J-S3b corrigendum adding Inferno (41) and the prerequisite sentence (A-1, A-2). ⚑ **Notify legolas's in-flight J4b leg** that the Inferno operand and the `meteorfire` synergy are in scope.
- [ ] **gandalf:** record A-4 as a named finding. Barbarian 14 → 16, BOUNDARY 9 → 11, (b) population 11 (W3).
- [ ] **gandalf:** § 4.5 (b) corrigendum (W2) · per-direction registry clause (W1b) · § 2.3/§ 4.4 counts 16 + 5 with build status · KP-162 citation (§ 3.7) · KP-162 conditions 4 and 5 stated in the charter.
- [ ] **gandalf:** put KP-162's enlarged J4b on the J3→J4 owner-eye checkpoint sheet (§ 3.8).
- [ ] **elrond:** census corrigendum lines for row 15's GD-rule cell (W1a), row 8's grade (I-1), row 11's precedent (I-2), the row 10 falsifier (I-3), row 18's wording (I-4) and block in the "do not enter" list (W4). This is an addendum. The count, the classes and the frozen record do not change.
- [ ] **gamora (J3):** register L-17…L-21 under the § 2 lever schema with the A-3/A-5 referent values and DECLARED-INVENTED defaults. L-06 gains `no-roll-no-crit`.
- [ ] **gamora (J2/J4b):** the offense-side family dispatch with refuse-loudly discipline, JOIN-only (W1b). Soulfire is untouched (§ 3.4).
- [ ] **Matt:** **nothing to rule.** There is no BLOCK, no HALT and no conflict with a locked decision. He sees KP-162's scope and the A-4 denominator change at the J3→J4 owner-eye checkpoint.

## References

- `agentic_orchestration/elrond/notes/2026-10-01-join1-j0-sorceress-census.md` (`b4d151a4a`)
- `agentic_orchestration/elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` (`78797db4b`)
- `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.5: J-S2, J-S3b, § 2.3, § 4.4, § 4.5, § 4.7, § 9.3)
- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`, KP-157 to KP-162
- `agentic_orchestration/research/datamine-acquisition/d2/raw/Skills.txt` (FILE `59601208…`), `Missiles.txt` (FILE `9d6794a5…`), `SkillDesc.txt` (FILE `1d5994c5…`)
- `agentic_orchestration/research/curated/kits-export/d2-fire-sorc.json` (FILE `43eb1e55…`)
- `agentic_orchestration/legolas/research/2026-10-01-join1-d2-animation-timing/README.md` (`b0f9d77fa`)
- `reincarnated-engine` @ `22cd2288`: `src/reincarnated/simulation/kc2/player_offense.py:329,350`, `secondary_streams.py:71,272,289`, `threat.py:126,132,267`, `action_permission.py`, `deferred_arrival.py`, `dot_timeline.py`, `disc.py`, `channel_policy.py:79,83`; `data/kc2/resid_d1_2_action_permission_matrix.json` (FILE `ad305866…`), `data/kc2/resid_d1_2_action_type_enum.json` (FILE `c976f36d…`), `data/kc2/pm4l_mitigation_by_body.csv` (header carries `res_fire`)
- `agentic_orchestration/qa/findings/2026-09-29-run-JOIN-1-charter-gate1-recheck.md` (RC3-W1/W2/W3)
- Read-only throughout. `corpus.db` was not opened. No KC2 file was touched.

**Signed:** jack-ryan, 2026-10-01. JOIN-1 J0 Gate-2 (Sorceress census).
