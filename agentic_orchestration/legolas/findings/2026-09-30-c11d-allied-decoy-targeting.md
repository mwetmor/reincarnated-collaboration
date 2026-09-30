# C-11d — the four Crucible structures as ALLIED DECOYS: the targeting rule, and why the diversion share is ZERO

**Date:** 2026-09-30 · **Author:** legolas (UNKNOWN-RESEARCHER) · **Commission:** C-11d (KP-134),
issued by the KC2-PLAY conductor (gandalf) on the **REFERENT-v2** track. Does **not** block the
REFERENT-v1 seal.
**Boundary under test:** C-11c found four Crucible structures purchased, 65,000 life each, and
recorded them as *"the largest UNPRICED player-side term"* — allied bodies the oracle's board does
not contain, on the premise that every monster in the oracle targets the player while the referent
had 260,000 HP of decoy soaking attacks. C-11c graded existence **A** and the **diversion share
SOURCE-UNLOCATED**, and declined to estimate it.
**Mode:** read-only. Nothing fitted, nothing reconstructed (Law 3). No sealed cell opened or re-run.
**Surfaces:** Mac Edition-II depot `.arz` (CRUCIBLE precedence KP-79) · the **Edition-IV `Game.dll`**
(`~/Games/vendor/grim-dawn-edition-IV-20260929/`, KP-117) · the D-12 anger-economy decode
(`legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode/`) · galadriel's committed footage
extractions · gamora's committed C-11/C-11a decomposition.
**Tooling:** `legolas/scratch/2026-09-30-c11b-attrlineage/arz.py` (carried, unchanged) + a PE
section/xref walker written for this lap (scratch, not committed).

---

## 0 · VERDICT IN ONE PARAGRAPH

⚑ **The decoys cannot divert, and the term prices to exactly ×1.000 — no change at all.** All four
structures carry **`causesAnger = 0`** and **`targetable = 0`** in the record, against shipped
binary defaults of **TRUE for both** (the immediates are in the DBR-load block, read below). Under
the D-12 decode — re-verified in the Edition-IV binary this lap — `causesAnger = False` makes
`ShouldRemoveEnemy` return TRUE, so **every `AddAnger` against that body writes nothing, the body
never enters the monster's `std::map<entityId, Entry>` threat table, and `FindEnemy`/`GetNewTarget`
can never select it.** ⚑ **This is the identical pattern D-12 already decoded and verified on both
Guardian summons, and it produced the identical ruling then: "the Guardians cannot divert;
`DIVERT_MAX` bounds a non-mechanism."** ⚑ **C-11d is the same finding, one commission later, on a
different body.** Two further record facts kill the attraction reading from the other side: the
structures' `offensiveTauntMin/Max/Chance` are all **0.0** (they emit **no** taunt), and the
`defensiveTaunt = 500` that the commission brief read as an attraction field is a **taunt
RESISTANCE** — it sits in the CC-resistance block beside `defensiveFear`, `defensiveConfusion`,
`defensiveStun`, `defensiveKnockdown`, `defensiveSleep`, all also 500. ⚑ **The field points the
opposite way to the reading it was given.** And an independent MEASURED instrument agrees:
galadriel's minimap actor-detector, which *"renders one icon per tracked actor,"* returns **zero
blobs** at t = 515 and t = 520 — after all four purchases — and her own note already states it:
*"the four purchased defenses do not appear on the minimap."* ⚑ **They are not tracked actors.**
**The landed-intake ratio is unmoved: ×3.175 stands. C-11d is the SIXTH sourced investigation to
fail to close ×3, and the second on the player side.**

| finding | grade |
|---|---|
| `causesAnger = 0` on all four (default TRUE) | **DATAMINED [record + bin]** |
| `targetable = 0` on all four (default TRUE) | **DATAMINED [record + bin]**; consumer site SOURCE-UNLOCATED |
| structures emit zero taunt; `defensiveTaunt` is a resistance | **DATAMINED [record]** |
| four defences absent from the minimap actor track | **MEASURED** (galadriel, independent) |
| **diversion share** | ⚑ **0.000 — DECODED, not bracketed** |
| **priced effect on landed intake** | ⚑ **×1.000 (nil)** |

---

## 1 · WHICH STRUCTURES, AND WHAT THEY ARE

Read from `SurvivalMode.arz` (CRUCIBLE precedence). All four are `Monster` records on
`database/templates/monster.tpl`.

| purchase | record | t (s) | controller |
|---|---|---|---|
| Deathchill Beacon | `records/creatures/defenses/turret_ice.dbr` | 477 | `controllers/defenses/controller_turretice.dbr` |
| Stormcaller Beacon | `…/turret_lightning.dbr` | 484 | `…/controller_turretlightning.dbr` |
| Inferno Beacon | `…/turret_fire.dbr` | 502 | `…/controller_turretfire.dbr` |
| Vanguard Banner | `…/banner_offense.dbr` | 510 | `…/controller_banner.dbr` |

**Identical on all four**, verbatim:

```
causesAnger            0                                   <- default TRUE (see §2.1)
angerMultiplier        0.0                                 <- default 1.0  (see §2.1)
targetable             0                                   <- default TRUE (see §2.2)
invincible             0
lifeTime               0                                   (no expiry)
monsterClassification  Common
defaultTeamMajor       TeamMajor_Human
defaultTeamMinor       TeamMinorMonster_Friendly
factions               records/controllers/factions/faction_survivors.dbr
actorRadius            0.3        actorHeight   1.0        pathingSize  Small
avoidForce             0.0                                 <- exerts NO crowd-avoidance on others
```

**The 65,000 life is DERIVED, and the derivation closes exactly.** The bios
(`bios/bio_defense_turret_01.dbr`, `bio_defense_banner_01.dbr`, both identical) carry
`characterLife = ((charLevel*16)^1.5)+1000`. At **charLevel 100**: `(1600)^1.5 + 1000 = 64,000 +
1,000 = 65,000`. ⚑ **Exact, to the unit** — the record's own `charLevel = charLevel*1`, and the
referent player is level 100. Life regen is `(charLevel*2+100) = 300 hp/s`. C-11c's 65,000 is
confirmed from the equation rather than from the sheet.

**Their own defences** (`passiveproperties_defense.dbr`, tree slot 1): 300–500 in every CC
resistance. ⚑ **Including `defensiveTaunt 500` — a RESISTANCE to being taunted.** Their
`offensiveTauntMin`, `offensiveTauntMax` and `offensiveTauntChance` are **all 0.0**: the structures
project no taunt field of any kind. There is no attraction term on these records.

**Their own attacks** (unchanged from C-11c, restated for completeness): tree slot 3,
`turretfire_fireblast` / `turretice_icebolt` / `turretlightning_chainlightning`; the banner's
`characterAttackSpeed = 0.0` (it does not attack — its 8 m aura is the offensive player buff C-11c
priced). Their **own** controllers give them `ViewDistance 12/10`, `AttackedAnger 3.0`,
`MaxPursuitDistance 15/10` — ⚑ **these govern how the TURRET picks a monster, not how a monster
picks the turret**, and reading them as the latter is the error this commission was issued to avoid.

---

## 2 · THE TARGET-SELECTION RULE, AND ITS GRADE

### 2.1 `causesAnger` — the threat-table entry gate. Grade DATAMINED [bin].

**The mechanism is already decoded and I did not re-derive it** — D-12
(`legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode/findings.md` § 3, commit `96e90a378`):

> `causesAnger = False` on the summon body makes `ShouldRemoveEnemy` (`0xfff0`, `CausesAnger` vslot
> `+0x428`) return TRUE, so **every `AddAnger` writes nothing**; `FindEnemy` is only `GetNewTarget`
> over that table. […] The threat table is `std::map<uint32 entityId, Entry>`.

D-12's offsets were taken against a **vendor tree that no longer exists** (C-7 § 1, KP-79(b)), so I
did not inherit them. ⚑ **I re-verified the structure of the mechanism in the Edition-IV `Game.dll`
independently**, and it holds:

| check | Edition-IV result |
|---|---|
| field-name string live in the binary (the D-3 dead-field test) | `causesAnger` **1 occurrence, referenced from `.text`** at `0x100417da`. *(Contrast `EmoteBeforePursuingChance`: 0 hits in all five binaries — D-3 `F-D3-3`.)* |
| the DBR read and its **shipped default** | `0x100417d7  push 1` · `0x100417d9  push 0x104f4de8 ("causesAnger")` · `call [vtbl+0x2c]` (GetBool) · `0x100417e3  mov byte [edi+0x194c], al` ⚑ **default TRUE** |
| corroborating default at construction | `0x1003ec97  mov byte [edi+0x194c], 1` |
| `angerMultiplier`, same block | `push 0x3f800000` (= 1.0f) · `push 0x104f4df4` · `call [vtbl+0x24]` · `fstp [edi+0x1958]` ⚑ **default 1.0** |
| who reads `+0x194c` | ⚑ **no direct `cmp`/`test` anywhere in `.text`** — only a **virtual accessor** at `0x10059c30` (`mov al, [ecx+0x194c]`) and its setter at `0x10059c56`. **Consumers reach it through the vtable, exactly as D-12's `CausesAnger` vslot `+0x428` describes.** |

⚑ **Two independent builds, two independent analysts, one mechanism.** The four structures set to
`0` a flag whose shipped default is `1` and whose only read path is the virtual accessor that
`ShouldRemoveEnemy` calls. **That is deliberate authoring, not an omission.**

### 2.2 `targetable` — a second, independent gate. Grade DATAMINED [record]; consumer SOURCE-UNLOCATED.

`targetable = 0` on all four, against a shipped default of TRUE:
`0x100440bb  push 1` · `push 0x104f5c58 ("targetable")` · `call [vtbl+0x2c]` · stored to **two**
adjacent bytes, `[edi+0x182f]` and `[edi+0x182e]` (a current/base pair). `.text` holds **four
`cmp byte [reg+0x182e], …` gates** (`0x1000f892`, `0x1000f9d9`, `0x100fb6a4`, `0x102de21a`) plus an
accessor pair and one runtime setter.

⚑ **I did NOT name which of those four gates is the monster-target-selection one, and I will not
guess.** That would require resolving each containing function, which this lap did not do. **The
conclusion does not rest on it**: § 2.1 alone is sufficient, and `targetable` is corroboration.

**What makes the corroboration strong is the record-level census**, over the 1,307 `Monster`
records in `database.arz`:

| `causesAnger` | `targetable` | count |
|---|---|---|
| 1 | absent (template default) | 1,122 |
| 1 | 1 | 127 |
| ⚑ **0** | ⚑ **0** | ⚑ **47** |
| 0 | absent | 7 |
| 0 | 1 | 4 |

⚑ **The two flags co-vary perfectly on the off side: every one of the 47 `targetable = 0` bodies
also has `causesAnger = 0`, with no exceptions.** And that 47-body class has an unmistakable
identity — `rock_01b` · `rock02` · `trap_floorspikes_*` (7 variants) · `trap_chthonicshard_*` (5) ·
`aetheranomaly_01` · `aetherfireflare_01` · `winddevil_poisona01` ·
`loghorean_tentaclecluster01e/02a` · `chthonianabomination_tentacles_a01` ·
`witchgodguardian_sentinel_crystal`. **Scenery, traps, and boss-attached props: the class of body
that is deliberately not a thing you can attack.** The Crucible defences are authored into exactly
that class. (`witchgodguardian_sentinel_crystal` reads `causesAnger 0 / angerMultiplier 0.0 /
targetable 0` — ⚑ **the same triple as the four structures**, and it is a body from D-12's own
verified summon set.)

### 2.3 The footage — an independent MEASURED instrument, already committed

galadriel, `galadriel/notes/2026-08-08-eor-followup-extraction.md` § 0, verbatim:

> *"it renders one icon per tracked actor […] **the four purchased defenses do not appear on the
> minimap.** t = 515 and 520 are *after* all four 5-tribute debits (476.8 / 484.1 / 502.3 / 509.6)
> and return zero. Anything bright on the disc during a wave is a monster, not a beacon or the
> banner."*

⚑ **Three instruments — the record, the binary and the footage — agree, and none of them was built
to answer this question.**

### 2.4 The one reading that could have gone the other way, and why it is inert

D-12 found that `petAngerTransference` (`+0x57c`, one consumer at `UnderAttack@ControllerMonster`
`0xfc3e8`) **splits** one `AttackedAnger` grant between the attacker and its `GetLeader()` —
*"summons slightly **attract** attacks to their owner."* The structures' controllers do carry
`petAngerTransference 32`. ⚑ **It cannot bite here, in either branch.** If the beacons have no
leader, both legs land on the beacon's own id, which `causesAnger = 0` discards entirely — **no
anger is written at all, toward anyone.** If their leader resolves to the player, the transferred
anger lands on a target the oracle **already** has at 100 % of monster attention; you cannot exceed
all. **Both branches give the same answer, so the conclusion is robust to a fact I did not
establish.** I record the branch rather than close it.

---

## 3 · WHETHER AND WHEN THEY DIE — the question is MOOTED, not answered

`invincible = 0` and `lifeTime = 0`: the bodies can in principle take damage and never expire. But
**no monster can select them** (§ 2), so the only path to their death is incidental AoE, and
against 65,000 life with 300 hp/s regen that is not a mechanism anyone should model without a
measurement.

⚑ **For the diversion term the question is moot: a share of zero does not change if the body that
would have absorbed it dies.** The survival question survives **only** as C-11c's caveat 2 on
**Term B** (the beacons' enemy-facing output must be *emitted* to matter), and it is unchanged by
this lap. **I did not view footage frames for structure health bars.** galadriel's minimap
instrument **cannot** answer it — the structures are not on the disc at all — so the surface that
would answer it is a direct frame read at the beacons' arena positions, which are themselves the
D-1 **placement CONVENTION**, not a measurement. **I am leaving it SOURCE-UNLOCATED and flagging
that the placement gap must be closed before the survival gap can be.**

---

## 4 · PRICING, WITHOUT FITTING

**Basis, unchanged from C-11c:** gamora's committed C-11a-fold decomposition — oracle 5,097.8 hp/s
pooled landed over w151–159 against the referent's 1,605.6 hp/s ⇒ **×3.175**. Target ×1; the
required factor is ×0.315.

**Term C — the four decoy bodies.**
Fraction of monster attacks that go to the decoys under the sourced rule: ⚑ **0.000.**
Not a ceiling, not a bracket — the rule *forbids* the body from entering the threat table, so the
share is zero by mechanism, in the same way and for the same reason D-12 ruled the Guardians'
diversion a non-mechanism.

| | landed hp/s | ratio |
|---|---|---|
| oracle, C-11a-corrected (committed) | 5,097.8 | ×3.175 |
| ⚑ **− Term C (decoy diversion), sourced** | ⚑ **5,097.8** | ⚑ **×3.175** |
| C-11c Term A + Term B, both at ceiling (unchanged) | 3,683.0 | ×2.294 |
| referent (target) | 1,605.6 | ×1 |

⚑ **C-11c's arithmetic — *"4 × 65,000 = 260,000 HP of decoy is, at the oracle's 5,098 hp/s,
51 seconds of intake"* — is FALSIFIED by the records. It was correctly marked UNPRICED and
correctly not applied; had it been applied it would have been the largest fitted error in the
REFERENT-v2 track.** The brief's framing — *"they are allied DECOY bodies […] while the oracle's
board has none"* — is true as to existence and **false as to consequence**: the oracle's board
having no allied bodies is **not a departure from the referent**, because the referent's allied
bodies were untargetable too. ⚑ **On this term the oracle was already right.**

**What would settle it against dispute, if anyone wants a second instrument:** a footage count of
monsters attacking a structure over any wave window. **The sourced prediction is zero**, and a
single monster observed swinging at a beacon would falsify § 2. That measurement is cheap for
galadriel *if* the beacons' on-screen positions can be established — which is the same D-1
placement gap named in § 3, and the reason I am not asserting it is available today.

---

## 5 · C-11e — routed, NOT answered, and the reason is a missing column

The commission offered C-11e *"if cheap, using one query on gamora's committed by-source column."*
⚑ **That column does not exist in any committed artifact I can reach, so it is not cheap and I did
not manufacture it.** Searched:

- `simulation/kc2/*.py` — the string `chaos` appears **nowhere** as a damage-type key. The only
  damage-type literals present are `"lightning"` (6), `"physical"` (5), `"bleed"` (2).
- `data/kc2/pm4l_mitigation_by_body.csv` (19,810 rows) **does** carry `res_chaos` — but it is a
  **MONSTER-side** sheet (per record × wave: their armour, DA and resists). It is not the player's
  landed intake by source.
- C-11's own FINDINGS reports killing-burst mass **by SKILL**, not by damage type
  (`chthonianherald_chaosblast` · `aetherialvanguard_arcanemissilenova` ·
  `arcane_elementalaura_buff` · `aetherorbitalretaliation`).

⚑ **I checked the instrument's domain before reporting the absence** — the first grep's silence
could have meant "resists are data-driven, not literals," and it partly did; the sheet that turned
up is the wrong side of the fight. **Reporting the first grep alone would have been a false alarm.**

**The bracket therefore stands exactly where C-11c left it, and the routing is unchanged:** if
`voidmarked` was one of the two drawn player mutators (identities SEARCHED SOURCE-UNLOCATED,
`math.randomseed(Time.Now())` per run), chaos resist and its cap both go 80 → 88 and landed chaos
goes 0.20× → 0.12× of raw, **a ×0.60 on the chaos channel only**. ⚑ **gamora owns the tick trace
and can emit a per-damage-type landed column from it; legolas cannot read one that was never
written.** One emission converts this from a named possibility into a bracket. **C-11e is OWED, not
closed.**

---

## 6 · WHAT gamora WOULD MODEL FOR REFERENT-v2

1. ⚑ **Nothing, for the decoys.** The oracle's board having no allied bodies is **correct** as
   against this referent. **Do not add decoy bodies; do not add a diversion term.** Record
   `defense_structures` as **`SEARCHED — DECODED-FALSE MECHANISM (diversion share 0.000;
   causesAnger=0 + targetable=0; D-12 precedent)`**, not as `EXCLUDED — excluded by charter`.
   ⚑ **The current classification and the new one give the same model and different knowledge**,
   and the difference is the whole point of the Commission Rule.
2. **C-11c's items 1–4 are untouched by this lap** and remain the v2 payload: install
   `LifeMonitorLimb.MONITOR_ON_FLOOR`; admit the three beacons to the timing decode; reclassify
   blessings and tributes to `SEARCHED-ABSENT`; amend the stale `kc2/__init__.py` L18–22 docstring.
3. **Carry forward, newly sharpened:** the **D-1 placement convention** is now blocking *two*
   things, not one — Term B's coverage **and** any footage check of beacon survival. It is the
   cheapest remaining unlock on the structure limb.
4. **Owed:** **C-11e**, as a one-shot emission from gamora (per-damage-type landed column over
   w151–159), not as a research commission on my surfaces.

---

## 7 · THE STANDING READ

⚑ **Six sourced investigations have now failed to close ×3: four monster-side (C-10, C-11, C-11a,
C-11b) and two player-side (C-11c, C-11d).** Three of the six pointed the wrong way. **C-11d is the
cleanest negative of the set** — not a ceiling that fell short, but a **decoded zero**: the
mechanism the term depended on does not exist, and the oracle's supposed departure was not a
departure.

⚑ **And it is the second time this project has priced a diversion term to zero by the same field on
a different body.** D-12 did it for the Guardian summons on 2026-08-25; C-11d does it for the
Crucible structures on 2026-09-30. **The pattern is worth naming, because it will recur: in Grim
Dawn, "an allied body stands on the board" does NOT imply "it takes attacks." `causesAnger` is the
field that decides, its default is TRUE, and Crate turns it off on anything it does not want
fought over.** Any future commission that proposes a body as a damage sink should read that one
field first — it is a five-minute check that would have priced this term before it was written up
as the largest unpriced one.

**This finding therefore strengthens, rather than weakens, C-11c's closing judgement, and I repeat
it unchanged:** the surplus is **not a missing mechanic on either side**. It is more likely a term
that is *present but composed wrongly* — the attribute limb's composition with `M_inst` and the
own-modifier at the total layer, where C-11a's C3 HALTED and R3/R4 were routed, both direction UP.
⚑ **That is a composition question. No further acquisition commission on my surfaces will answer
it, and C-11d is the second consecutive finding to say so.** ⚑ **REFERENT-v2 should not issue a
seventh surface commission of this shape.** The decoys *did* qualify under KP-134's own test — they
priced a mechanism the oracle does not have at all — and the test was met honestly and returned
zero. **The next move belongs to gamora's total-layer composition, not to me.**

**Matt's seal ruling is unaffected and remains correct.** The declared gap should now read:
**"~×3 too lethal; player-side absences SEARCHED and priced at ≤ ×2.29 combined ceiling; the allied
decoys DECODED to a diversion share of ZERO; not the cause."**

---

## 8 · SOURCE LIST

**Primary — game data** (Mac Edition-II depot, CRUCIBLE precedence KP-79):
`SurvivalMode.arz` :: `records/creatures/defenses/{turret_fire, turret_ice, turret_lightning,
banner_offense}.dbr` · `…/defenses/bios/{bio_defense_turret_01, bio_defense_banner_01}.dbr` ·
`records/controllers/defenses/{controller_turretfire, controller_turretice,
controller_turretlightning, controller_banner}.dbr` ·
`records/controllers/factions/faction_survivors.dbr` ·
`records/skills/defenses/passiveproperties_defense.dbr`.
`database.arz` :: full `Monster`-record census, 1,307 records, `causesAnger` × `targetable` joint
distribution · `records/skills/nonplayerskills/bossskills/pets/witchgodguardian_sentinel_crystal.dbr`.

**Primary — binary** (`~/Games/vendor/grim-dawn-edition-IV-20260929/`, KP-117; 32-bit PE,
imagebase `0x10000000`): `Game.dll` — string liveness for `causesAnger` (1), `angerMultiplier` (1),
`targetable` (3), `defensiveTaunt` (1), `offensiveTauntMin` (1), all referenced from `.text`;
DBR-load block `0x100417a2–0x10041816`; default-construct `0x1003ec97`/`0x1003ecb8`; virtual
accessor `0x10059c30`/`0x10059c56`; `targetable` load `0x100440bb`, gates `0x1000f892`,
`0x1000f9d9`, `0x100fb6a4`, `0x102de21a`. `Engine.dll` — zero hits on all of the above (the fields
are Game-side).

**Prior decode relied on, not re-derived:**
`legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode/findings.md` § 2–§ 3 (commit `96e90a378`;
`ShouldRemoveEnemy` `0xfff0`, `CausesAnger` vslot `+0x428`, `UnderAttack@ControllerMonster`
`0xfc3e8`, the `std::map<uint32 entityId, Entry>` threat table) ·
`legolas/findings/2026-09-29-gd-enemy-ai-own-files-inventory.md` (D-1 alert gate, D-12 anger
economy, D-3 `F-D3-3` dead-field test).

**Primary — footage:** `galadriel/notes/2026-08-08-eor-followup-extraction.md` § 0 (minimap
actor-detector; zero blobs at t = 515/520 post-purchase) · `…/2026-08-07-eor-sittings-extraction.md`
§ 1 (the four purchases, timestamps, in-game description lines).

**Oracle substrate (committed, read-only):** `simulation/kc2/*.py` (damage-type key census) ·
`data/kc2/pm4l_mitigation_by_body.csv` ·
`simulation/math/kc2-play-c11-oracle-lethality-decomposition{,-FINDINGS}-2026-09-29.md` ·
`…-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` (×3.175) ·
`legolas/findings/2026-09-30-c11c-player-side-defensive-absences.md` · charter KP-124 → KP-134.

**Nothing in this finding was fitted, reconstructed, or taken from community description.** Where a
value was not recoverable it is marked SOURCE-UNLOCATED and left unpriced. Where a prior lap's
arithmetic is contradicted, both readings are printed and the contradiction is named.
