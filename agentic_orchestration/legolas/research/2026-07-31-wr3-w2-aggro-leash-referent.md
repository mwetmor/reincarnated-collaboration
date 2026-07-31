# Research — WR3 W-2: proximity aggro, social aggro, leash — the GD referent parameters — 2026-07-31

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf, RUN-CONDUCTOR, run WR3-KITE-COMMIT (charter ruling R-WR3-12(W-2))
**Sources:** vendor pin `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (`database.arz` + GDX1–3;
3,735 `Class=Monster` records, 447 controller records, 356 `ControllerMonster`),
`/Users/admin/Games/vendor/grim-dawn/database/templates.arc` (819 templates; `controllerai.tpl`,
`character.tpl`, `characterenemy.tpl`, `monster.tpl`), `/Users/admin/Games/vendor/grim-dawn/resources/Text_EN.arc`,
and `Game.dll` symbol/string table. Web used as **tertiary** corroboration only — see §5 on why.
**Scratch (read-only):** `agentic_orchestration/legolas/scratch/2026-07-31-wr3-w2/` (`w1_fieldcensus.py` … `w10_allfields.py`)

**Provenance grades** (commission scheme):
**[extracted]** = read directly from the shipped data or the binary · **[community]** = documented by a
third party, not verifiable here · **[inferred]** = my reading, stated as such, not attested

---

## 0. VERDICT — read this before the parameter tables

**All three mechanisms exist in the referent and all three are fully parameterised. Two of them do
not work the way the charter assumes.**

1. **Proximity aggro is real and is a two-radius anger-accumulation model, not a boolean radius.**
   `ViewDistance` **15 m** / `InnerViewDistance` **4 m**, with separate anger rates per band.
   **[extracted]**

2. **But Crate shipped `AngerTolerance` at median 1.0 / mode 0.0 against a template default of 10.0** —
   the accumulator's *engagement gate is effectively switched off*. Time-to-aggro at the outer radius
   works out to **0.2 s** (and 0 s for the 447/1,278 Hero controllers that ship tolerance 0.0).
   **The anger system's live job in GD is target *ranking*, not engagement *delay*.** So the lap can
   bind proximity aggro as a hard 15 m trigger and be faithful to the referent. §1.3 **[inferred from extracted]**

3. **Social aggro is NOT a spawn-group link and NOT a plain radius broadcast. It is a
   faction-group-keyed distress call with a probabilistic responder gate and a per-caller cap.**
   Caller side: `distressCallRange` **18 m**, `distressCallTime` **500–2000 ms**, `maxDistressCalls`
   **1–2**. Responder side: `ChanceToRespondToDistressCall` **20–75 %**, gated by
   `DistressResponseBehavior` = `RespondToSameGroup` (85 %). §2 **[extracted]**

4. **The charter's stagger claim is CORROBORATED but its stated *reason* is wrong, and this matters.**
   The charter attributes stagger to "aggro radii and body-blocking approach". The data shows stagger
   is **explicitly engineered** in four independent parameters — a call *delay*, a call *cap*, a
   responder *probability*, and a pre-pursuit *emote state*. Body-blocking is at best a contributor.
   If the lap models stagger as an emergent by-product of radii, it will under-produce it. §2.4

5. **THE HEADLINE — GD HAS NO LEASH-WITH-FULL-HEAL, AND THE CHARTER'S W-2 THIRD MECHANISM IS
   THEREFORE NOT REFERENT-ATTESTED.** The string `leash` occurs **0 times** in `Game.dll`. There is
   **no heal-on-return field anywhere in `controllerai.tpl`**, and no `FullHeal` / `RestoreHealth` /
   `ResetHealth` symbol in the binary. What GD has instead is a **75 m / 10 s disengagement envelope**
   (`MaxPursuitDistance` 75.0, `PursuitTime` 10000 ms) plus a `StateReturn` walk-back. Bosses ship
   `MaxPursuitDistance` **210 m** — larger than most arenas, i.e. functionally un-leashable. §3

6. **Full-heal-on-return is an MMO convention, not an ARPG one.** It is absent from GD, and I found no
   confirmation of it in D2, D3 or PoE either (§4). If Matt wants territory-guard full-heal, that is a
   **deliberate departure from the referent**, and it should be queued to him as such rather than
   landed as "GD's convention". This is the single most important bind-vs-decide item in §6.

---

## 1. Proximity aggro

### 1.1 Where the parameters live

The AI record class is **`ControllerMonster`** (`database/templates/controllermonster.tpl`, deriving from
`controllerai.tpl`). Monsters bind to one via the `Monster` record's **`controller`** field — the join
holds for **3,729 of 3,735** monster records **[extracted]**. There is no `ai*.dbr` naming convention;
the records live under `records/controllers/`.

`controllerai.tpl` organises the surface into named groups. The two that govern acquisition are
**`Senses`** and **`AngerManagement`** **[extracted]**.

### 1.2 The parameter surface, template default vs shipped reality

Template defaults are **Titan Quest lineage** and are *not* what GD ships — the gap is large and
systematic, so quoting the defaults as "GD's values" would be an error.

| Field | Group | Template default | GD shipped (median, all tiers) | Grade |
|---|---|---|---|---|
| `ViewDistance` | Senses | 15.0 | **15.0** (mode 15.0, 1103/1278 Hero) | [extracted] |
| `InnerViewDistance` | Senses | 5.0 | **4.0** (mode 4.0, 1246/1278 Hero) | [extracted] |
| `MaxYViewDistance` | Senses | 0.0 | **10.0** (mode 10.0, 1275/1278 Hero) | [extracted] |
| `enemyTooClose` | Senses | 5.0 | 0.0–3.0 (bimodal) | [extracted] |
| `pathingViewDistance` | Senses | 0.0 | 0.0 (set on only 54 records) | [extracted] |
| `AngerTolerance` | AngerManagement | 10.0 | **1.0** (mode **0.0**) | [extracted] |
| `SightAngerRate` | AngerManagement | 20.0 | **5.0** | [extracted] |
| `InnerSightAngerRate` | AngerManagement | 50.0 | **10.0** | [extracted] |
| `AttackedAnger` | AngerManagement | 100.0 | **12.0** | [extracted] |
| `AllyAttackedAnger` | AngerManagement | 40.0 | **6.0** | [extracted] |
| `ProjectileAnger` | AngerManagement | 20.0 | **2.0–3.0** | [extracted] |
| `ForgiveRate` | AngerManagement | 50.0 | **2.0** | [extracted] |
| `RandomAngerChance` | RandomAnger | 0 | 0 (10 on 319/1278 Hero) | [extracted] |
| `RandomAngerEvaluationTime` | RandomAnger | 3000 | 0 or 3000 | [extracted] |

**Crate rescaled the entire anger economy by roughly 10× downward from the TQ defaults while holding
the ratios.** `SightAngerRate` 20→5, `InnerSightAngerRate` 50→10, `AttackedAnger` 100→12,
`AllyAttackedAnger` 40→6, `ProjectileAnger` 20→2. **[inferred from extracted]**

**But `AngerTolerance` did not scale with them** — it went 10.0 → 1.0/0.0, a ~10× *further* cut on top
of the rate cut. That is the load-bearing observation of §1.

### 1.3 Aggro radius by monster class, in metres

**Unit calibration:** `resources/Text_EN.arc → tags_ui.txt` contains
`SkillDistanceFormat={%.1f0 {^E}Meter %s1}` — the engine prints a raw distance field with `%.1f` and
appends "Meter", with no scale factor in the format string **[extracted]**. World unit = metre. That the
*controller's* distance fields share the skill fields' world unit is **[inferred]** (one engine, one
coordinate system) but not separately attested.

Binned by `monsterClassification` (values: `Common;Champion;Hero;Boss;Quest;SuperBoss`, from
`monster.tpl` **[extracted]**), joined monster→controller:

| Tier | n | `ViewDistance` (m) | `InnerViewDistance` (m) | `MaxPursuitDistance` (m) |
|---|---|---|---|---|
| Common (trash) | 742 | **15.0** (mode 15.0) | 4.0 | **75.0** |
| Champion | 1,030 | **15.0** | 4.0 | **75.0** |
| Hero | 1,279 | **15.0** | 4.0 | **75.0** |
| Quest | 518 | 15.0 | 4.0 | 75.0 |
| **Boss** | 85 | **17.5** (mode 15.0/17.5 split) | 4.0 | **210.0** |
| SuperBoss | 29 | 15.5 | 5.0 | 200.0 |

**Aggro radius barely varies by tier — 15 m from trash to hero, 15–17.5 m for bosses. What varies by
tier is *pursuit*, not *detection*.** **[extracted]**

### 1.4 Time-to-aggro

`AngerManager::Update(int, float, bool, bool)` in `Game.dll` takes an int first argument, consistent
with a delta-time-in-ms accumulator **[extracted]**. Reading the rates as anger-per-second **[inferred]**:

| Condition | Tolerance | Rate | t to engage |
|---|---|---|---|
| Outer band (4–15 m), mode tolerance | 0.0 | 5.0 | **0 s (instant)** |
| Outer band, median tolerance | 1.0 | 5.0 | **0.20 s** |
| Inner band (<4 m), median tolerance | 1.0 | 10.0 | **0.10 s** |
| Outer band, 3rd-mode tolerance | 6.0 | 5.0 | **1.20 s** |

So the referent's engagement latency spans **0 – 1.2 s**, concentrated at the bottom. **A hard-radius
trigger at 15 m is a faithful simplification of GD** for the ~65 % of controllers shipping tolerance
0.0–1.0; the 6.0-tolerance tail (111/1,278 Hero controllers) is the only population where the
accumulator produces a perceptible delay. **[inferred from extracted]**

### 1.5 Corroborating engine symbols

`Game.dll` exports a dedicated `AngerManager` class **[extracted]**: `AddAnger`, `SubtractAnger`,
`GetAnger`, `GetAngerDiff`, `GetMaxAnger` (static), `Clear`, `TransferAnger`, `ShouldRemoveEnemy`,
`GetNewTarget`, **`GetCurrentTargetNotMostHated`**, `DebugRender`, `ShowAngerLevels`. Plus
`ControllerMonster::AngerUpdate`, `ControllerMonster::ClearAnger`, `Monster::ClearAnger`,
`Character::CausesAnger`, `Character::GetAngerMultiplier`.

`GetCurrentTargetNotMostHated` is the tell: **the anger value is a threat-ranking key across multiple
candidate targets, and the AI deliberately allows targeting someone other than the most-hated.**
That is the mechanism's real purpose, and it confirms §1.3's reading. **[extracted]**

A per-character master switch `causesAnger` exists: **True on 5,982 records, False on 3,347**
(the False set is props/pets/non-combatants) **[extracted]**.

---

## 2. Social / pack aggro

**GD runs two independent social-aggro mechanisms.** The lap needs both; modelling only one will miss.

### 2.1 Mechanism A — passive ally-attacked anger

`AllyAttackedAnger` (shipped median **6.0**, modes 4.0/6.0/8.0) **[extracted]**. Any monster that can
perceive an ally being struck accrues this much anger. It is implicit-radius (bounded by the
perceiver's own `ViewDistance`), continuous, and requires no broadcast. With `AngerTolerance` at 0–1,
**a single ally being hit is on its own sufficient to aggro every ally in the 15 m band** — one hit
delivers 6.0 anger against a threshold of ≤1.0. **[inferred from extracted]**

### 2.2 Mechanism B — the distress call (explicit broadcast)

**Caller side** — fields on `character.tpl` / `characterenemy.tpl`, group `Character`, present on the
`Monster` record **[extracted]**:

| Field | Type | Template default | Shipped by tier (median) | Grade |
|---|---|---|---|---|
| `distressCall` | bool | 1 | True: Hero 1273/1279, Common **673/742** | [extracted] |
| `distressCallRange` | real | 15.0 | Hero **15.0**, Champion/Common/Quest/Boss **18.0** | [extracted] |
| `distressCallTime` | int (ms) | 5000 | Hero **500**, Champion/Common **2000**, Quest **3000** | [extracted] |
| `maxDistressCalls` | int | 1 | Champion/Common **1**, Hero/Boss/Quest **2** | [extracted] |
| `distressCallGroup` | string | — | Beast, Aetherial, Chthonic, Undead, Eldritch, … | [extracted] |

**Responder side** — fields on `ControllerMonster`, group `DistressCalls` **[extracted]**:

| Field | Template default | Shipped by tier (median) | Grade |
|---|---|---|---|
| `ChanceToRespondToDistressCall` | 100 | Hero **75**, Champion **75**, Common **50**, Boss **20**, SuperBoss **0** | [extracted] |
| `DistressResponseBehavior` | `RespondToAll;RespondToSameGroup;RespondToSameRace` | **`RespondToSameGroup` ≈ 85 %**, `RespondToSameRace` ≈ 15 %, `RespondToAll` 4 records total | [extracted] |
| `DistressResponseGroup` | (empty) | Beast 49, Eldritch 40, Aetherial 37, Chthonic 34, Undead 26, Groble 12, Celestial 11, Outlaw 9, Zealot 7, BlackLegion 6 | [extracted] |

Engine confirmation **[extracted]**: `Character::DoDistressCall`, `Monster::DoDistressCall`,
`Character::ShouldUseDistressCall`, `Player::ShouldUseDistressCall`, `Character::GetDistressCallGroup`,
`ControllerMonster::GetDistressResponseBehavior`, `ControllerMonster::GetDistressResponseGroup`,
`ControllerMonster::GetChanceToRespondToDistressCall`. Also `distressCallWhenDying` appears as a
literal string in the binary but is not populated in shipped records.

### 2.3 So: which is it — radius, spawn-group, or faction call?

**It is a faction-group-keyed radius broadcast with a probabilistic responder gate.** Precisely:

> A monster in combat emits, at most `maxDistressCalls` (1–2) times, every `distressCallTime`
> (500–2000 ms), a call carrying its `distressCallGroup` tag, reaching `distressCallRange` (15–18 m).
> Each recipient within that radius whose `DistressResponseBehavior` is `RespondToSameGroup` and whose
> `DistressResponseGroup` matches the tag rolls `ChanceToRespondToDistressCall` (20–75 %) to engage.

**It is emphatically not a spawn-group link** — the key is a *faction/race string*, not a spawn
identity, so a call can pull an unrelated same-faction pack that happens to be in range, and cannot
pull a co-spawned different-faction pack. **[extracted]**

**Corroborating design evidence — the Shattered Realm override.** The `EndlessDungeonGenerator` class
(32 records) carries `distressCallGroupOverride` = **`Eldritch`**, `distressResponseGroupOverride` =
**`Eldritch`**, `distressCallRangeOverride` = **15.0**, `viewDistanceOverride` = **19.0**,
`roamBehaviorOverride` = **`NeverRoam`** **[extracted]**. Crate deliberately **collapses every SR
monster into one distress group** so that everything pulls everything, and simultaneously **raises view
distance 15→19 m** and **pins roaming off**. That is a designer explicitly using these four knobs to
turn pack cohesion up for the endless-dungeon mode — strong evidence the knobs do what §2.3 says.

### 2.4 Does pack engagement stagger? — the charter's claim, corroborated and corrected

**Corroborated: yes, real packs stagger.** **Corrected: the charter's stated mechanism is not the
dominant one.** The charter attributes stagger to "aggro radii and body-blocking approach". Aggro
radii barely vary (§1.3 — 15 m flat across trash/champion/hero), so radius spread is a *weak* stagger
source in the referent. The actual stagger machinery is four explicit parameters:

| Stagger source | Parameter | Magnitude | Grade |
|---|---|---|---|
| Call **delay** | `distressCallTime` | 500–3000 ms before the call fires | [extracted] |
| Call **cap** | `maxDistressCalls` | 1–2 — a caller cannot chain-pull a zone | [extracted] |
| Responder **probability** | `ChanceToRespondToDistressCall` | 25–50 % of eligible allies *decline* | [extracted] |
| Pre-pursuit **telegraph** | `EmoteBeforePursuingChance` | mode **20 %** (269/356 controllers) play an emote first | [extracted] |

Plus the engine state `ControllerMonsterStateAlertBeforePursue` **[extracted]** — a first-class AI
state for "alerted but not yet pursuing", which is stagger implemented in the state machine itself.

**Net:** a 5-body pack does not arrive as a wall. Roughly half the non-triggering members respond at
all, those that do respond 0.5–3 s late, one in five plays a telegraph before moving, and the cascade
cannot propagate more than 1–2 hops from the original caller. Body-blocking then shapes the arrival
order of whoever did commit. **[inferred from extracted]**

---

## 3. Leash / reset — the negative finding

### 3.1 The word does not exist

`strings Game.dll | grep -ci leash` → **0** **[extracted]**. GD's engine has no leash concept under
that name, and no equivalent under any other name that I could find. What it has is a **pursuit
envelope**.

### 3.2 What actually exists

Group `Pursuit` in `controllerai.tpl` **[extracted]**:

| Field | Type | Template default | Verbatim description | Shipped |
|---|---|---|---|---|
| `PursuitTime` | int | 10000 | *"Maximum length of time for which to pursue enemies (milliseconds)"* | **10000 ms** — 1258/1278 Hero, 945/1029 Champion, **82/82 Boss (100 %)** |
| `MaxPursuitDistance` | real | 20.0 | (empty) | **75.0 m** trash/champion/hero · **210.0 m** Boss · **200.0 m** SuperBoss |
| `EmoteBeforePursuingChance` | int | — | (empty) | mode 20 |

Engine side **[extracted]**: `ControllerMonster::GetMaxPursuitDistance`,
`ControllerMonster::GetPursuitTime`, `ControllerMonster::GetHomePosition`,
`ControllerMonster::GetResetOriginAfterFleeing`, `Character::GetSpawnPoint`, and the states
`ControllerMonsterStatePursue`, **`ControllerMonsterStateReturn`**, **`ControllerMonsterStateReturnFast`**.

So the return-to-home behaviour is real and has its own state (and a "fast" variant), anchored on a
`HomePosition`.

### 3.3 Do they heal on return?

**No — and this is a proven negative, not an absence of evidence.** Three independent checks:

1. The **complete** field surface of `controllerai.tpl` was enumerated (§ scratch `w10_allfields.py`).
   Groups are: `Senses`, `AngerManagement`, `Fleeing`, `Pursuit`, `SkillUsage`, `Roaming`, `Patrolling`,
   `DistressCalls`, `RandomAnger`, `Dodging`, `Attacking`, `Sleep`, `Emote`, `PetBehaviour`, `Loot`,
   `Dying`, `Movement Control`. **There is no health/heal/restore field in any of them.** **[extracted]**
2. `strings Game.dll | grep -iE "FullHeal|HealOnReset|RestoreHealth|ResetHealth|healToFull"` → **no
   hits** **[extracted]**.
3. The one field whose name invites the wrong inference — **`lowHealthResetLevel`** (present on 378
   `Monster` records) — is defined in `character.tpl` under the group **`Character Sounds`**
   **[extracted]**. It is a *low-health audio cue re-arm threshold*, not a leash heal. **Flagging this
   explicitly because it is exactly the field a faster pass would have mis-bound.**

Returning monsters therefore recover only via ordinary `characterLifeRegen` during the walk back.
**[inferred from extracted]**

### 3.4 Does leash fire mid-combat?

**No.** `MaxPursuitDistance` (75 m) is **five times** `ViewDistance` (15 m) **[extracted]**, so the
disengagement envelope cannot be reached while the target remains detectable. The trigger is
disengagement — the player breaking contact and staying broken for `PursuitTime` = 10 s — not any
combat-state condition. **[inferred from extracted]**

Two conditions that *are* attested to clear aggro, both flee-scoped, both rare in shipped data:
- `ClearAngerWhenFleeing` — **False on 355 of 356** controllers **[extracted]**. Effectively never.
- `ResetOriginAfterFleeing` — False ~80 % (1018/1278 Hero), True ~20 % **[extracted]**. Applies after
  *fleeing*, not after *pursuing*.

### 3.5 The consequence for the charter

The charter's W-2 third mechanism is "leash-in-combat (territory-guard full-heal return armed under
combat conditions)". Against the referent, **every one of those three qualifiers fails**:

| Charter qualifier | GD referent | Grade |
|---|---|---|
| "leash" | no such concept; a 75 m / 10 s **pursuit envelope** instead | [extracted] |
| "full-heal return" | **no heal field exists**; normal regen only | [extracted] |
| "armed under combat conditions" | envelope is 5× view distance — **disengagement-only** | [inferred from extracted] |

Bosses at `MaxPursuitDistance` **210 m** are, for practical arena sizes, **un-leashable** **[extracted]**.

---

## 4. Cross-referent sanity row

**Diablo 2** — aggro is a single flat radius. `monstats.txt` carries **`aidist`** ("monster 'vision'…
aggro distance") and **`aidel`** (AI decision delay in frames; lower = faster reaction) **[community]**.
Distances are in tiles; the community conversion is yards × 1.5 = tiles **[community]**. There is no
documented distress-call or group-response system — pack aggro emerges from co-located monsters sharing
overlapping `aidist`, i.e. **exactly the "aggro radii" mechanism the charter assumed for GD, which is
in fact D2's model rather than GD's**. No leash-and-heal; D2 monsters pursue across the level.

**Diablo 3** — monsters return to their spawn area when the player leaves, and "tethering" is a
recognised concept in Rifts/GRs **[community, weak]**. I looked specifically for confirmation of
full-heal-on-leash and **did not find it**; the one concrete health-restoration case surfaced
(Morlu regaining ~60 % of health) is **time-conditioned, not leash-conditioned** **[community]**.

**Path of Exile** — aggro range is a first-class, modifiable stat: Stealth "reduces the range at which
a monster will aggro a target", and Meat Shield "cuts your minions aggro range in half"
**[community, wiki]**. Leashing is short and aggressive — PoE2 EA players report "run 1m they forget
about you" and complain of having to hunt down disengaged rares **[community, forum]**. Monsters carry
ordinary life regeneration; no full-heal-on-leash is documented **[community]**.

**Genre-wide vs GD-specific:**
- **Genre-wide:** radius-triggered proximity aggro; ordinary life regen rather than reset-heal.
- **GD-specific:** the *two-band* anger accumulator (`ViewDistance` + `InnerViewDistance` at different
  rates), and the faction-keyed distress call with a **per-caller cap** and a **responder probability**.
  I found no D2/D3/PoE equivalent of `maxDistressCalls` or `ChanceToRespondToDistressCall`.
- **Not genre-standard at all:** full-heal-on-leash. It is a **WoW/MMO** convention. It appears in
  none of the four ARPGs surveyed. Importing it would be a genre departure, not a genre borrowing.

---

## 5. Knowledge gaps not resolved

1. **Web sources are effectively empty on GD AI internals.** The official *Grim Dawn Modding Guide*
   PDF does not document the AI/controller surface (fetched; no AI parameter content). Nexus/Crate-forum
   and grimtools results returned nothing on `AngerTolerance`/`SightAngerRate`/`distressCall*`. **The
   extraction in §1–§3 is, as far as I can establish, first-of-kind documentation of these fields** —
   which also means it is unreplicated, and §6 should treat it accordingly.
2. **`MaxPursuitDistance`'s reference point is not resolved.** Distance from *home* or from *target*?
   `GetHomePosition@ControllerMonster` exists alongside it, which leans home **[inferred]**, but the
   application site is not exposed as a symbol. This matters: home-relative vs target-relative give very
   different kiting behaviour. **Open.**
3. **Anger rate units are inferred, not attested.** `AngerManager::Update(int, …)` implies ms
   delta-time, and I read the rates as per-second; per-tick would change §1.4's latencies by the tick
   rate. The *ordering* of §1.4 is safe; the absolute seconds are not.
4. **`GetMaxAnger` is a static** — there is a global anger ceiling I did not resolve. It bounds how far
   threat can accumulate and therefore how "sticky" a target is.
5. **`distressCallWhenDying` and `AlertBeforePursue`** appear as binary strings but are not populated in
   any shipped record. Engine-only, or vestigial.
6. **Metre calibration is one-step-removed** for controller fields (§1.3) — attested for *skill*
   distance fields, carried across by single-world-unit assumption.
7. **Template defaults are Titan Quest heritage.** `characterenemy.tpl`'s `distressCallGroup` picklist
   still ships the TQ race list (`Arachnos;CryptWorm;DuneRaider;Harpy;Ichthian;Jackalman;Maenad;Mantid;
   Minotaur;Neanderthal;Peng;Raptor;Ratman;Reptillian;Satyr;Skeleton;Sprite;Tigerman;Yerren`) while the
   *data* carries GD groups (Beast/Aetherial/Chthonic/…). **Anyone reading the templates for values
   rather than for structure will get TQ's game, not GD's.** Recorded as a lane hazard.

---

## 6. What the W-2 lap should BIND vs what it must DECIDE

### 6.1 BIND — referent-attested, no design judgement required

| # | Bind | Value | Grade |
|---|---|---|---|
| B1 | Proximity aggro radius, all monster tiers | **15 m** | [extracted] |
| B2 | Inner/close band radius | **4 m** | [extracted] |
| B3 | Boss aggro radius | **15–17.5 m** (not larger than trash) | [extracted] |
| B4 | Engagement latency at radius | **0–0.2 s** (tolerance ~0–1) | [inferred from extracted] |
| B5 | Anger from being attacked / ally attacked / projectile | **12 / 6 / 2–3** | [extracted] |
| B6 | Anger decay (`ForgiveRate`) | **2.0 /s** | [extracted] |
| B7 | Social-aggro mechanism shape | faction-group-keyed radius broadcast, **not** spawn-link | [extracted] |
| B8 | Distress call radius | **18 m** (15 m for Hero) | [extracted] |
| B9 | Distress call delay | **500 ms** (Hero) / **2000 ms** (Champion, Common) | [extracted] |
| B10 | Distress calls per caller | **1–2** (hard cap on cascade depth) | [extracted] |
| B11 | Responder probability | **75 %** Hero/Champion · **50 %** Common · **20 %** Boss · **0 %** SuperBoss | [extracted] |
| B12 | Responder gate | same-faction-group (85 %); same-race (15 %) | [extracted] |
| B13 | Pre-pursuit telegraph | **20 %** of monsters emote before pursuing | [extracted] |
| B14 | Pursuit envelope, trash/champion/hero | **75 m** | [extracted] |
| B15 | Pursuit envelope, boss | **210 m** (effectively un-leashable) | [extracted] |
| B16 | Pursuit timeout | **10 000 ms**, uniform (100 % of bosses) | [extracted] |
| B17 | Heal on return | **none** — normal regen only | [extracted] |
| B18 | Leash trigger condition | disengagement only; never mid-combat | [inferred from extracted] |

**B1–B18 are the math-first inputs R-WR3-12(W-2) asked for.** They need no Matt ruling; they are the
referent.

### 6.2 DECIDE — genuinely open, queue for Matt

| # | Open choice | Why it is open | Recommended framing |
|---|---|---|---|
| **D1** | **Does the engine adopt full-heal-on-leash at all?** | **The referent does not have it.** §3.3 is a proven negative. The charter names it as "GD's convention" — that premise is false. | This is now a *departure* decision, not an *implementation* decision. Recommend: default to the referent (no heal), and make full-heal an explicit opt-in only if a design goal demands it. |
| **D2** | Territory-guard as a distinct concept | GD has no territory guard — it has `HomePosition` + a 75 m envelope. Whether Reincarnated wants a *narrower*, guard-flavoured leash is a design call with no referent answer. | If yes, note it will make the game **more** restrictive than GD, not less. |
| **D3** | `MaxPursuitDistance` reference point | Unresolved in the data (§5.2) — home-relative vs target-relative. | Pick one and record it as a stated assumption; it is not recoverable from the referent. |
| **D4** | Whether to model the anger accumulator at all | GD ships it effectively disabled as an *engagement gate* (§1.2) but uses it live as a *threat-ranking* key (§1.5). | Recommend: bind B1/B4 as a hard radius for engagement; adopt anger only if/when multi-target threat ranking is in scope. |
| **D5** | Faction-group taxonomy for distress calls | GD's groups (Beast/Aetherial/Chthonic/Undead/Eldritch/…) are GD's *fiction*. Reincarnated's group keys must come from its own bestiary. | Structural mechanism binds (B7/B12); the group *names* are ours to choose. |
| **D6** | Stagger via explicit parameters vs emergent | §2.4 shows GD engineers stagger deliberately. Whether Reincarnated does the same, or accepts weaker emergent stagger, is a cost/fidelity call. | Recommend explicit — emergent-only will under-produce, since B1 shows radii are flat and cannot carry the spread. |
| **D7** | Anger-rate time base | §5.3 — per-second vs per-tick is inferred. | Low stakes (ordering is safe); resolve by choosing, not by further research. |

### 6.3 One thing the lap should NOT do

Do not read the `.tpl` **defaults** as GD's parameters (§1.2, §5.7). The templates are Titan Quest
heritage and are wrong by ~10× on the entire anger economy and by 3.75× on `MaxPursuitDistance`
(20.0 default vs 75.0 shipped). Every number in §6.1 is taken from **shipped record data**, not from
template defaults.

---

## 7. Source list

**Primary — vendor pin, read-only, accessed 2026-07-31**
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/database/database.arz` + `gdx1/GDX1.arz` +
  `gdx2/GDX2.arz` + `gdx3/GDX3.arz` — 3,735 `Class=Monster`, 447 controller records
- `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` — 819 templates; `controllerai.tpl`
  (2,559 B), `controllermonster.tpl`, `character.tpl`, `characterenemy.tpl`, `monster.tpl`
- `/Users/admin/Games/vendor/grim-dawn/resources/Text_EN.arc` → `tags_ui.txt` (unit calibration)
- `/Users/admin/Games/vendor/grim-dawn/Game.dll` — symbol/string table (`AngerManager`,
  `ControllerMonster*` states, `DoDistressCall`, leash-negative)

**Tooling (existing, reused)**
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`
- `agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py`

**Tertiary — web, accessed 2026-07-31**
- Grim Dawn Modding Guide (official PDF) — https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf — *no AI parameter content*
- "How does 'aggro' work in Diablo 2", PureDiablo forums — https://www.purediablo.com/forums/threads/how-does-aggro-work-in-diablo-2.180517/ (403 on direct fetch; `aidist`/`aidel` via search result summary)
- The Phrozen Keep, Monster Spawn — https://d2mods.info/forum/viewtopic.php?t=3915
- Project Diablo 2 Game Mechanics wiki — https://wiki.projectdiablo2.com/wiki/Game_Mechanics
- "Rare monster health reset", Diablo 3 forums — https://us.forums.blizzard.com/en/d3/t/rare-monster-health-reset/59294
- "mobs leash / aggro range", PoE forums (PoE2 EA) — https://www.pathofexile.com/forum/view-thread/3725157
- PoE Wiki: Stealth — https://pathofexile.fandom.com/wiki/Stealth
- PoE Wiki: Monster — https://pathofexile.fandom.com/wiki/Monster
- Grim Dawn Monster Database (grimtools) — https://www.grimtools.com/monsterdb/
- Official Grim Dawn gameplay guide, Monsters — https://www.grimdawn.com/guide/gameplay/monsters/
