# Research — C-7: insufficient-energy behaviour (activation and held channel) — 2026-09-28

**Mode:** A (analytical / primary-source probe)
**Commission:** **C-7**, issued under *The Commission Rule* (`gandalf/notes/2026-09-21-the-commission-rule.md` § 4), Run KC2-PLAY, SEAL LAP **W1b**; charter ledger **KP-89**
**Commissioner / conductor:** gandalf (RUN-CONDUCTOR)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Boundary of record:** gamora, `reincarnated-engine/src/reincarnated/simulation/math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md` **§ 5** — *"DECLARED ABSENT (Law 3). I ISSUE NOTHING."*
**Access:** read-only. No save, archive, template, footage, pack or oracle modified. Footage read in place on the mount; never copied.
**Precedence:** every DBR value below re-checked under **KP-79 CRUCIBLE order** (`database < GDX1 < GDX2 < GDX3 < SurvivalMode < SM1 < SM2 < SM3`). Winners named per row. **No value differs between CAMPAIGN and CRUCIBLE** except `hud_mastertable.dbr`, whose CRUCIBLE winner is `SurvivalMode3.arz` and carries the identical figure.

---

## HEADLINE

**The branch is answerable, and it was answerable from disk. Three of the four sub-questions close; the fourth is a searched `SOURCE-UNLOCATED`.**

| # | question | verdict | grade |
|---|---|---|---|
| **(a)** | bound skill pressed with `energy < cost` | ⚑ **REFUSED.** The activation does not occur. Not cast-anyway, not clamped-to-zero, not queued. **A signal fires: a player vocalization** (`notEnoughManaSound` → 4 wav variants). **No text/error string exists.** | **`TEMPLATE-CITED`** + **`OFFICIAL-GUIDE-VERBATIM`** |
| **(b1)** | is the EoR channel a *different* mechanism? | ⚑ **NO — and this is the finding gamora correctly refused to assume.** `SkillChanneled.tpl` **includes `Skill_Activated.tpl`.** A channel *is* an activated skill re-activated every `duration`. A starved channel tick **is** case (a). | **`TEMPLATE-CITED`** |
| **(b2)** | resume timing after a starved tick, button still held | ❌ **SEARCHED `SOURCE-UNLOCATED`.** The engine binary is not on disk (§ 0). The structural reading is carried in its own column and graded, never folded. | **`STRUCTURAL-INFERRED`** (reading) / **`SOURCE-UNLOCATED`** (fact) |
| **(c)** | does regen continue during a held-but-starved channel? | ⚑ **YES, unconditionally — and the *authoring surface cannot express a gate*.** `manaRegenEquation` is a pure function of `elapsedTime` and character stats, and `healthmanaregen.tpl` exposes **no variable** naming cast, channel or activity state. | **`TEMPLATE-CITED`** (see the caveat, § 4.2) |
| **REFERENT** | does the footage ever reach the branch? | ⚑ **NO. Not once, and not close.** `min(energy) = 1110 / 1594 = 69.6 %` over **10,956 parsed frames**. **Zero** frames below the max single cast cost (106.2), below a four-button burst (236.7), **or below the HUD's own low-energy flash threshold (318.8).** | **`MEASURED-EXACT`** |

⚑ **The sharpest single artefact is a template ORDERING, not a value.** In `charactersounds.tpl`, `notEnoughManaSound` sits inside an unbroken run of **refusal** sounds and nowhere near the **threshold** sounds — § 2.2. That is Crate's own authoring schema classifying the event for us.

⚑ **And the engine has NO `lowManaSound`.** It has `lowHealthSound` (populated on the PC with `spak_malewarninglowhealth`). Exhaustive string-table search across all 8 archives: **no `lowManaSound`, no `outOfManaSound`, no `lowEnergySound` field exists.** The low-energy *warning* channel in Grim Dawn is **visual only**; the audio channel is reserved for the *refusal*. § 2.3.

---

## 0 · Surfaces — what was searched, and what is not there

| Surface | Status |
|---|---|
| **Game on disk — DBRs / ARZ** | ✅ **LIVE.** 8 archives under `/Users/admin/depots/`. Record counts unchanged from C-2/S-1 (34,114 / 18,447 / 16,451 / 24,178 / 3,147 + 3 SM). |
| **Game on disk — AUTHORING TEMPLATES** | ✅ ⚑ **LIVE, AND THIS IS THE SURFACE THAT ANSWERED THE COMMISSION.** 808 `.tpl` files at `legolas/scratch/2026-08-08-kc2-halt-bundle/tpl/`, recovered by an earlier probe and **never used for a semantics question until now.** They are Crate-authored: field rosters, per-field descriptions, include chains. C-2 § 4 and gamora § 5 both concluded from the DBRs alone; **the DBRs say what a field's VALUE is, the template says what the field MEANS.** |
| **Localization (`Text_EN.arc` ×7)** | ✅ 20,394 tags. Searched for every insufficient-resource phrasing. § 2.4 |
| **Client binary — `Game.dll` / `Engine.dll`** | ❌ **NOT ON DISK, ANYWHERE.** The depots hold **only** `database/*.arz` and `resources/Text_EN.arc` — no binary depot was ever pulled. `find` over `~/Games`, `~/depots`, Steam and both mounted volumes: zero hits. ⚑ **The `Character+0x1844` precedent (Commission Rule § 3) ran against a vendor tree that no longer exists** (KP-79 (b)). **This is the single reason (b2) does not close.** |
| **Save (`player.gdc`)** | ⚪ **NOT PROBED — and deliberately.** A save records state, not engine policy. There is no field a save could carry that would answer *"what happens when you press a starved button."* Named so the negative is a decision, not an omission. |
| **Footage** | ✅ read in place, `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`. Used via galadriel's 10,959-row 60 Hz trace. § 3 |
| **Official guide (grimdawn.com, Crate's own site)** | ✅ fetched. One verbatim sentence, load-bearing for (a). § 1.3 |
| **Community (Steam / Crate forums / wiki)** | ⚪ surveyed; **contributes nothing that is not already sourced from disk**, and is cited for nothing. The one Crate-forum thread on exactly this topic contains no statement of the mechanic. Fandom returns HTTP 402. **Recorded so the negative is on the record.** |

---

## 1 · (a) — a bound skill activated with insufficient energy

### 1.1 · The engine has a first-class field for the event

`records/creatures/pc/malepc01.dbr` — **CRUCIBLE winner `GDX3.arz`**, identical in all four main archives:

```
notEnoughManaSound = 'records/sounds/human/vocals/spak_malelowmana.dbr'
```

and that SoundPak, `database.arz`, type `SoundPak`:

```
soundName1..4 = sound/human/vocals/pcmale_outofmana01.wav … 04.wav
weight1..4    = 25 / 25 / 25 / 25
volume        = 0.85      volumeSet = 'Dialog'
```

**Four equal-weight variants of a spoken player line, in the Dialog bus.** Games do not author four voice-acted variants for a state that never occurs; they author them for an event a player will trigger repeatedly. The equivalent female record `femalepc01.dbr` carries `spak_femalelowmana.dbr`; `werewolf`, `wereraven`, `fangs` and `wendigo` character-sound records each carry their own. **The referent's PC sex is not pinned** (the save's `ui_settings` parsed empty, C-2 § 0) — **and it does not matter: both PC records carry the field.**

⚑ **One dissonance, reported rather than smoothed.** The field is `notEnoughMana`, the wavs are `outofmana`, and the intervening DBR is named `lowmana`. **Two of three name the refusal event; the SoundPak's own filename is the outlier.** It is the only thread anywhere in this probe that would support a "threshold warning" reading, and § 2.2 and § 2.3 outvote it decisively. Named because a finding that reports only the agreeing evidence is not a finding.

### 1.2 · The template places the field among REFUSALS

`charactersounds.tpl`, authored ordering, contiguous:

```
inventoryFullSound        <- pickup refused
lockedChestSound          <- interaction refused
lockedShrineSound         <- interaction refused
lockedDoorSound           <- interaction refused
lockedQuestObjectSound    <- interaction refused
notEnoughManaSound        <- ⚑
skillCooldownSound        <- activation refused
itemCooldownSound         <- use refused
---- the run ends ----
lowHealthSound            <- a THRESHOLD, and it is on the far side
deathSound1 / deathSound2
```

**Every neighbour on both sides is "you attempted an action and the game declined it."** The threshold sound is outside the run.

⚑ **And the correspondence is tighter than adjacency.** `skill_activated.tpl`'s *"Skill Config"* group lists, in order, **`skillCooldownTime` then `skillManaCost`** — the two preconditions on an activation. `charactersounds.tpl` lists **`notEnoughManaSound` then `skillCooldownSound`** — one refusal cue per precondition. **Two gates, two cues, and cooldown-refusal is not in dispute.** The mana gate is the same kind of gate.

All four PC cues are populated on `malepc01.dbr`: `lockedChestSound`, `itemCooldownSound = spak_maleitemcooldown`, `skillCooldownSound = spak_maleskillcooldown`, `notEnoughManaSound = spak_malelowmana`. **Live fields, not schema residue.**

### 1.3 · Crate says it in one sentence

`https://www.grimdawn.com/guide/character/character-basics/`, official Crate site, accessed 2026-09-28, **verbatim**:

> **"If you run out of energy, you will not be able to cast skills that require energy."**

**"Will not be able to cast"** — refusal, not a degraded cast. This is the only sentence on the open web that states the mechanic, and it is on the developer's own domain. The official *Combat* guide is silent; `/guide/gameplay/skills/` 404s.

### 1.4 · What (a) does NOT establish

- **No partial-charge or partial-effect behaviour is excluded by direct evidence** — it is excluded by *"will not be able to cast"* plus the refusal-cue placement, which is strong but is not a code read.
- **Whether the refusal consumes the input** (press swallowed vs press re-evaluated next frame) is **not sourced.** It matters only for (b2).

---

## 2 · The negative results, stated as results

### 2.1 · `skillActiveManaCost` is NOT a channel field — exhaustively

A full decompression pass over all 8 archives (~96,000 records) returns **71 records** carrying `skillActiveManaCost`. Every one is a **toggle, aura, buff or shapeshift**: `Skill_BuffSelfToggled`, `Skill_BuffAttackRadiusToggled`, `SkillBuff_Debuf`, `SkillBuff_Passive`, `Skill_BuffSelfDuration`, `Skill_BuffSelfColossus`, `Skill_Shapeshift`.

**Not one channelled attack skill uses it.** Checked by name and by record: **Eye of Reckoning** (`Skill_AttackRadiusSpin`), **Albrecht's Aether Ray** (`playerclass05/aetherray1.dbr`, `Skill_AttackSpellBeam`), Flames of Ignaffar, Drain Essence, `relic_conflagration.dbr` — **all carry flat `skillManaCost` arrays and no `skillActiveManaCost`.**

> ⚑ **The sustained-drain mechanism in Grim Dawn is the TOGGLE/AURA. The channel is not a drain at all — it is a repeated purchase.** The client's *"Energy Cost per Second"* on a beam skill is a **derived display**, and the tag inventory shows the client keeps three distinct labels for the three distinct things: `ManaCost = "{^E}Energy Cost"` · `ManaCostPerSecond = "{^E}Energy Cost per Second"` · `ActiveManaCost = "{^E}Active Energy Cost per Second"`. **Which tag binds to which field is not sourced** and nothing here depends on it.

### 2.2 · The include chain — the answer to gamora § 5's F-8 worry

`records/skills/playerclass09/eyeofreckoning1.dbr` → `templateName = database/templates/skill_attackradiusspin.tpl`, whose **first include** is:

```
database\Templates\SkillChanneled.tpl
```

and `skillchanneled.tpl`'s includes are:

```
Skill_Base.tpl · Skill_Activated.tpl · Skill_Attack.tpl · Skill_Spell.tpl
```

**`Skill_Activated.tpl` is where `skillManaCost` and `skillCooldownTime` live** (`skillManaCost` description, verbatim: *"Activated Skills Only"*).

`skillchanneled.tpl`'s own "Skill Config" group contains **exactly three fields and no resource field of any kind**:

| field | default | EoR's value (CRUCIBLE winner `GDX2.arz`) |
|---|---|---|
| `duration` | 0.2 | **0.25** |
| `canUseWhileMoving` | 0 | **1** |
| `useResetsDuration` | 1 | **1** |

> ⚑ **VERDICT (b1): in Grim Dawn's own schema a CHANNELLED skill IS an ACTIVATED skill, re-activated every `duration` while held.** A starved channel tick is a **refused activation** — case (a) — **not a distinct channel-termination mechanism.**
>
> ⚑ **gamora § 5 was right to refuse, and is now supplied.** Her words: *"a channel that cannot afford its next tick and a button that cannot afford its activation are two different mechanisms, and reading one off the other is exactly the fusion F-8 was retired for."* **The refusal was correct on the evidence she had. The identity is not an inference — it is an include directive in Crate's template.** The distinction that survives is hers in shape: I am not claiming the two *behave* alike because they *seem* alike; I am reporting that the schema gives them **one** cost field, reached through **one** include.

### 2.3 · There is no low-energy audio warning

Exhaustive regex over all 8 archive string tables for `lowManaSound` / `lowEnergySound` / `outOfManaSound` / `manaEmptySound`: **NONE.** `lowHealthSound` exists in `charactersounds.tpl`, `character.tpl` and `characterenemy.tpl`, and is populated on the PC (`spak_malewarninglowhealth` — *"warning"* in the asset's own name). **Its energy twin was never authored.**

The low-energy warning is **visual**: `hudManaBarStartFlashingAtRatio = 0.20` on `hud_mastertable.dbr` and `hud_orbmastertable.dbr` — present in all 8 archives, **CRUCIBLE winner `SurvivalMode3.arz`, same value.** (An orphan `records/ui/hud/temp/hud.dbr` carries 0.15; a `temp/` record referenced by nothing.)

### 2.4 · No insufficient-energy string exists in the client

Searched 20,394 tags on values, not just keys. The client ships **`MarketCostTooExpensive` / `MarketCostReputationTooLow` / `tagMarketError02` / `tagItemInsufficientStatus` / `tagReclaimNoAether` / `tagReclaimNoGold`** — six distinct *"you cannot afford this"* strings, **all for economy transactions, none for a skill activation.** The `{^r}` red-error style is used freely for the economy cases.

> ⚑ **So the absence is not an absence of the CAPABILITY — it is a design choice.** Grim Dawn tells you in text when you cannot afford an *item*; when you cannot afford a *skill* it makes your character grunt. **A port that raises a visible error on this branch would be less faithful than one that is silent.**

---

## 3 · Does the referent exercise the branch? — NO, measured

Recomputed **independently, on the RAW population**, from galadriel `2026-09-28-kc2-play-energy-fullreread-population.json` (video sha-pinned; `t0 = 682.1`, `t1 = 864.75`, 60 Hz, `n = 10,959`, `parsed = 10,956`):

| quantity | value |
|---|---:|
| ceiling (E1, her control) | **1594** |
| **minimum energy over the window** | **1110** |
| min as % of ceiling | **69.6 %** |
| p001 / p01 / p05 / median | 1163 / 1222 / 1359 / 1580 |
| frames below **318.8** (the HUD's own 20 % flash) | **0** |
| frames below **236.7** (four-button burst, C-2) | **0** |
| frames below **106.2** (max single cast, War Cry) | **0** |

⚑ **`min = 1110` on the raw population reproduces gamora § 5's 1110 exactly**, which she derived from galadriel's *cleaned* positive-depth max of 484 (`1594 − 484`). **The cleaning does not move the floor.** Two populations, one number — and the cleaning was never tuned against it.

⚑ **A second, independent instrument agrees, and it is the game's own:** the referent **never once triggered the energy globe's low-energy flash.** The character was 791 energy — **half the usable bar** — above the threshold at which Grim Dawn starts *warning* about energy, across 182.65 s of wave-150–160 Crucible.

> ⚑ **What that means for fidelity, stated plainly: this is a PLAY-ONLY branch with no referent.** Grading a run against the footage **cannot discriminate any insufficient-energy policy from any other**, because the footage never enters the region where they differ. **A policy chosen to "match the footage" would be fitting to zero observations.** That is precisely the situation the Commission Rule exists for: the branch must be decided on **sourced** grounds, and § 1–§ 2 now supply them. **The port must still handle it without crashing** — a player who plays worse than Matt, or a kit with a thinner pool, will reach it on day one.

---

## 4 · (c) — regeneration during a held, starved channel

`records/game/playerresourcebehavior.dbr` — **`database.arz`, the ONLY archive holding it**, so CAMPAIGN and CRUCIBLE agree trivially:

```
manaRegenEquation  = '(((manaRegen*((intelligence/384)+1))+((intelligence-50)/100))+6.5) * elapsedTime'
lifeRegenEquation  = '(lifeRegen + ((physique-50)/25))  * elapsedTime'
manaDrainRate         = 1.0
manaFeedRate          = 10.0     manaOverStorageLimit   = 1.0
healthFeedRate        = 10.0     healthOverStorageLimit = 1.0
templateName = 'database/templates/healthmanaregen.tpl'
```

### 4.1 · The template's variable roster is the evidence

`healthmanaregen.tpl` declares the **complete** set of `eqnVariable`s available to those two equations:

```
elapsedTime · lifeRegen · lifeRegenMod · lifeTotal
manaRegen   · manaRegenMod · manaTotal · intelligence · charLevel
```

> ⚑ **There is no variable for cast state, channel state, combat state, or current energy.** The claim is therefore not the weak one (*"the equation happens to have no such term"*) but the strong one: **the authoring surface cannot express a gate on channelling.** Regeneration is a pure function of elapsed time and character stats, and it ticks while the channel is held and starved exactly as it ticks at rest.

Author's own verbatim descriptions, from the same template's *"Config"* group:

| field | Crate's description |
|---|---|
| `manaOverStorageLimit` | *"Amount of potion above limit to allow"* |
| `manaFeedRate` | *"Add over time rate"* |
| `manaDrainRate` | ⚑ *"Decrease rate of mana used"* |

**`manaFeedRate` and `*OverStorageLimit` are POTION mechanics** — the author says so. **`manaDrainRate = 1.0` is the only field in the game describing how spent energy is deducted**, and it has **no health twin** (`healthDrainRate` does not exist). Reported as a value with an author-verbatim gloss; **I do not claim to know whether 1.0 is a multiplier, a per-second interpolation rate, or a flag.** `SEMANTICS-THIN`.

### 4.2 · The caveat that must travel with (c)

**This rules out a gate *in the regen record*. It does not exclude a suppression applied by the engine outside the equation** — and the binary is not on disk to check. The evidence is strong (the equation is the documented mechanism, and it has no expressive room for a gate) and it is **not a code read.** Carry it as `TEMPLATE-CITED`, not as `BINARY-VERIFIED`.

---

## 5 · What did NOT close — (b2), and what may be said about it

**The fact:** after a channel tick is refused for cost, with the button still held — does the next tick fire the instant `energy ≥ cost` again, or does the channel *end* and require a re-press? **`SOURCE-UNLOCATED`, searched.** Searched: all 8 archives by field and by string; the 808-file template corpus; the 20,394-tag client corpus; the official guide; the Crate forum thread on exactly this subject; the referent footage (which never reaches the branch). **The engine binary is the only surface that could carry it and it is not on this machine.**

**The structural reading, carried in its own column and folded by nobody:** `useResetsDuration = 1` with `duration = 0.25` means a held channel re-activates on a 0.25 s cadence; a refused activation is not a state change to the channel in any field the schema exposes; therefore the *expected* behaviour is **a stutter at the tick cadence, not a termination** — the channel resumes as soon as a tick is affordable, while held. Grade **`STRUCTURAL-INFERRED`**. ⚑ **It is not sourced and must not be emitted as though it were.**

**The nearest MEASURED analogue, named and NOT fused:** KP-1/KP-2 — *Type-B AUTO-RESUMES while RMB is held; Type-A resumes on input only.* That was measured on a **cast-interrupt** cause, not a **starvation** cause. The input state is identical (button held); the cause is not. ⚑ **Reading starvation-resume off cast-interrupt-resume would be the same move gamora refused at § 5, and the include chain that licensed § 2.2 licenses nothing here** — it makes the starved tick a refused *activation*, and says nothing about what the held input does next. **Named as the obvious next hypothesis; asserted as nothing.**

**What would close it, cheapest first:** (1) a `Game.dll` on disk — one depot pull, and the `Character+0x1844` precedent says this surface yields; (2) **30 seconds of deliberate footage** — any character, any channel, drained to zero with the button held. **(2) is a Matt-to-do, not a research task**, and it would close (b2) outright.

---

## 6 · Grades, as rows a consumer can take

| row | value | grade | cite |
|---|---|---|---|
| insufficient-energy policy, discrete activation | **REFUSE** (no cast, no clamp, no queue) | `TEMPLATE-CITED` + `OFFICIAL-GUIDE-VERBATIM` | § 1.2, § 1.3 |
| refusal signal — audio | player vocalization, 4 variants, Dialog bus | `DB-CITED` | § 1.1 |
| refusal signal — text | ⚑ **none exists** | `DB-CITED` (exhaustive absence) | § 2.4 |
| low-energy warning — audio | ⚑ **none exists** (`lowManaSound` never authored) | `DB-CITED` (exhaustive absence) | § 2.3 |
| low-energy warning — visual | energy globe flashes at **ratio ≤ 0.20** | `DB-CITED` (CRUCIBLE winner `SurvivalMode3.arz`) | § 2.3 |
| channel cost mechanism | **repeated activation** of flat `skillManaCost`; **not** a per-second drain | `TEMPLATE-CITED` | § 2.1, § 2.2 |
| starved channel tick | **is** a refused activation (same branch as the discrete case) | `TEMPLATE-CITED` | § 2.2 |
| channel resume timing after a starved tick | ❌ **not recoverable** | **searched `SOURCE-UNLOCATED`** | § 5 |
| — its structural reading | stutter at `duration` cadence; resumes while held | `STRUCTURAL-INFERRED` | § 5 |
| regen during held, starved channel | **continues, ungated** | `TEMPLATE-CITED` (caveat § 4.2) | § 4.1 |
| `manaDrainRate` | **1.0**, *"Decrease rate of mana used"* | `DB-CITED` / `SEMANTICS-THIN` | § 4.1 |
| referent exercises the branch? | **NO.** `min = 1110/1594 = 69.6 %`; 0/10,956 frames below any threshold | `MEASURED-EXACT` | § 3 |

---

## 7 · Operational notes

- **Free disk 42 GiB at close** (44 GiB at lap launch; C-9 rendering concurrently). **Above the 40 GB HALT floor, and closing.** This probe wrote ~30 KB. Flagged for the conductor, not acted on.
- **Tooling:** `legolas/scratch/2026-09-28-c7-insufficient-energy/` — `scan_fields.py` (precedence-aware full-archive field locator), `scan1.json` (engine mana fields), `scan2.json` (71 `skillActiveManaCost` bearers). Readers symlinked from the S-1/C-2 lane (`arz.py`, `arcread.py`, `tags.py`) — **unmodified.**
- ⚑ **Method note worth keeping: the 808-file template corpus has been on disk since 2026-08-08 and was pulled for a different question.** Two prior commissions concluded *"no record field states the behaviour"* from the DBRs alone and were right — **the DBRs never state behaviour; that is not what they are for.** The templates are the semantics layer and they are cheap to grep. **Reach for them first on any future *"what does this field MEAN"* question.**

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-09-28, KC2-PLAY SEAL LAP W1b. Read-only throughout. Committed with an explicit file list; **did not push — the conductor releases.**
