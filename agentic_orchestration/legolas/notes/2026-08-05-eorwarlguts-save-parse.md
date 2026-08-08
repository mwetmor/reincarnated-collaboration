# EoRWarlGuts `.gdc` save parse — build identity graduated to MEASURED — 2026-08-05

**Mode:** A (analytical / primary-source measurement)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access mode:** read-only throughout. Every original was copied to scratch and parsed from the copy;
no share original was opened by any tool with a write path, and nothing outside this repo was written.
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/`
**Supersedes for format purposes:** the parse lane mapped in `2026-07-28-gd-gdc-save-probe.md` § 3
(that parser was fitted to 1.3.0.x only; § 1 below generalises it and corrects it in three places).

---

## VERDICT BLOCK

**All four saves parsed 100% clean — every block, every end-of-block checksum, zero trailing bytes,
zero notes.** No block resisted. The `.gdc` cipher and the 1.1.9.x↔1.3.0.5 format gap were both fully
defeated; § 1 records three first-of-kind format corrections produced along the way.

**Build identity: MEASURED, and it did not move.** Across 3,590 build-identity field comparisons
between the as-imported baseline and the post-two-sittings end state, **exactly one changed**
(`character_bio.health`, +12.0, a derived pool) — **99.97% identity retention**. Every skill rank,
every devotion node, every celestial-power binding, every equipped item *including its seed*, and
every attribute is byte-identical to fordprefect's 2022 savefile.

**Regime: MEASURED, and it corroborates Matt's attestation exactly.**
`survival-defense-built` **263 → 267 = +4**, matching "four defense sites purchased."
`survival-powerups-activated` **390 → 390 = +0**, matching "zero celestial blessings."
Devotion **55 → 55**, so zero tributes went to Torralia's devotion unlock.

**Crucible tokens: nothing was minted.** Reaching 150 and dying at 160 added **zero** Crucible tokens.
The next rung is `SURVIVALMODE_TIER18CHECKPOINT` (wave 180) and it is **absent** — and per the 1.2.1.3
patch notes the checkpoint tokens no longer gate anything anyway.

**The 08/03 mystery: the save says a third session happened.** `death-count` rose **+3** where only
**two** deaths are attested, and `maps_survivalworld_h.map` — a directory that **does not exist in the
2022 zip** — was created 2026-08-03 22:05.

**One correction to a live gandalf note:** the 08-04 `v3 §5-AFTERMATH` primer's "no obelisks/beacons,
banner-only convention" is **wrong**. The Crucible ships three named beacons; Matt's video (Inferno
Beacon) and the `.arz` agree against the note. See § 10.

---

## 0 — Sources and integrity

### 0.1 Substrate (SHA-256 verified against the remote `certutil` values in the commission)

| Copy in scratch | Bytes | SHA-256 | Source mtime (PC) | Role |
|---|---:|---|---|---|
| `player.gdc` | 98,101 | `b8e6f510…4bfa5` ✓ | 2026-08-05 21:54 | **end state**, ~2 min after the sitting-two death |
| `player.gdc.bak` | 98,101 | `9901e66d…a7230` | 2026-08-05 21:52 | pre-final-write rotation — **NOT byte-identical to `.gdc`** |
| `player.g00` | 87,820 | `71d0d9b8…0fa5e` ✓ | 2026-08-02 00:20 | **not** the as-constructed baseline — see § 0.2 |
| `player.g01`–`g09` | 84,655–89,149 | (parsed, § 0.2) | 2026-08-02 | fordprefect's own 2022 GD Stash rotation |
| `player.gdc.eor` | 87,820 | `c8738da3…87e0d` | 2026-08-01 15:51 | my pre-construction copy = the zip's `player.gdc` |

Hash-verified provenance chain, byte-exact:

```
gutsmasher.zip → _EoRWarlGuts/player.g00   SHA 71d0d9b8… ≡ the live share's player.g00
gutsmasher.zip → _EoRWarlGuts/player.gdc   SHA c8738da3… ≡ my 2026-08-01 player.gdc.eor
```

### 0.2 **CORRECTION: `player.g00` is not a construction artifact.** (load-bearing)

The commission treats `player.g00` as the "in-situ as-constructed baseline." **It is not.**

1. `player.g00` on the share is **byte-identical** to `_EoRWarlGuts/player.g00` inside `gutsmasher.zip`
   (SHA `71d0d9b8…`). `gutsmasher.zip` ships the **whole** `_EoRWarlGuts` folder including `player.g00`
   through `player.g09` and `player.gdc.bak`, all dated 2022-08-11/13. Its 2026-08-02 00:20 mtime is
   the **unzip** time, not a write.
2. A semantic diff of `player.g00` against `player.gdc.eor` returns **0 differing leaves out of 9,303**.
   They are the same logical state under two encryption seeds (GD randomises the 4-byte seed per write).
3. **Every** one of `g00`–`g09` carries `expansion-character? = 3`, `inventory v4`, `character_skills v5`,
   `play_stats v11` — the pre-1.3 shape. GD 1.3.0.5 *always* writes `7 / 11 / 8 / 12`. **None of the ten
   was written by the current client, and none was written after 2022.**

**Consequences.** (a) The true as-constructed 2026-08-02 state was written straight to `player.gdc`
and has since been overwritten; it is **not recoverable**. (b) The only available baseline is the
*as-imported* state, so the g00→gdc diff spans **import → migration → all sittings**, not just the
sittings. (c) No GD Stash backup was created in this directory after the unzip — consistent with either
a GD-Stash backup-directory setting or with the construction having been a savefile drop-in (Path A).
Since the gear is bit-identical to fordprefect's file (§ 3), **the fixture is his artifact unmodified**,
which is the strongest possible construction outcome and makes (a) harmless.

### 0.3 Corpus and reference sources

| # | Source | Class | Used for |
|---|---|---|---|
| S1 | `c0de-v1k1ng/gd-edit-FoA` `gdc.clj` (banked `scratch/2026-08-04-crucible-ckpt/gdc_foa.clj`) | **Primary** (working impl.) | 1.3/FoA struct deltas |
| S2 | `kirijin/gd-edit` ≡ upstream `odie/gd-edit` `gdc.clj` (banked `…/gdc_kirijin.clj`, `2026-08-01-eor-addendum/gdc.clj`) | **Primary** | base struct + field names |
| S3 | `AaronHutchinson/Grim-Dawn-Save-Decryption` | Primary (older) | cipher; superseded field names |
| S4 | Edition-II corpus `~/Games/vendor/grim-dawn-edition-II-20260724/` (`database.arz`, `GDX1/2/3.arz`, `SurvivalMode*.arz`, `Text_EN.arc` ×4) | Primary (game data) | item/skill/devotion/monster names; Crucible economy |
| S5 | GD 1.2.1.3 patch notes, thread 142410 (banked `raw_142410.txt`) | Primary | checkpoint + tribute rules |
| S6 | Crucible tag dumps (banked `tags_survival{,2,3,ui}.dec.txt`) | Primary (game data) | tribute cap, defense names, checkpoint ladder |
| L1 | `legolas/notes/2026-08-01-eor-endgame-build-of-record.md` | Internal | verification target |
| L2 | `legolas/notes/2026-07-28-gd-gdc-save-probe.md` | Internal | parse lane |
| L3 | `legolas/notes/2026-08-04-gd-crucible-checkpoint-edit-probe.md` | Internal | token structure |

Tooling written for this pass (all in scratch, all read-only): `gdc2.py` (version-aware parser),
`ui_solve.py` (block-14 layout solver), `semdiff.py`, `deepdiff.py`, `allscan.py`, `gear.py`,
`devo.py`, `econ.py`.

---

## 1 — Parse lane: three first-of-kind format corrections

The 2026-07-28 parser hard-coded the 1.3.0.x item and skill shapes and could not read a 1.1.9.x file
(it died at `inventory` offset `0x1e3`). `gdc2.py` gates every drifted field on its **block version**,
so one parser now reads both vintages. Observed versions:

| block | 2022 file (`g00`, `eor`) | 2026 file (`gdc`, `bak`) |
|---|:--:|:--:|
| header `expansion-character?` | 3 | **7** |
| file `data-version` | 8 | 8 |
| character_info / character_bio | 5 / 8 | 5 / 8 |
| **inventory** | **4** | **11** |
| **character_stash** | **6** | **11** |
| **character_skills** | **5** | **8** |
| **ui_settings** | **5** | **7** |
| **play_stats** | **11** | **12** |
| respawn/teleport/marker/shrine/lore/faction/tutorial/tokens | 1/1/1/2/1/5/1/2 | identical |

### 1.1 CORRECTION — `ui_settings` v7 is **count-prefixed**, not 95 hotslots

The FoA fork hard-codes `(>= version 7) → (s/array HotSlot :length 95)`. **That over-runs the block on
a GD 1.3.0.5 save.** Solved by brute force against the block-end + checksum oracle: of nine candidate
extra-int counts, exactly one lands on `end − 4` with a valid checksum and a `camera-distance` of
`48.0` (matching the v5 control byte-for-byte).

The correct v7 layout writes **three int32 after `skill-sets`, and the second of them is the hotslot
count** — observed value **47**, and the greedy read consumed exactly 47. Corrected naming:

```
:14-unk2        :int32      ; observed 1
:hotslot-count  :int32      ; observed 47   <- was mis-modelled as a fixed 95
:14-unk4        :int32      ; observed 0
:hotslots       (s/array HotSlot :length hotslot-count)
:camera-distance :float
```

### 1.2 CORRECTION — the four 1.3/FoA item fields are **2 before + 2 after**, not 4 appended

The FoA fork appends all four `Item-v13-fields` after `stack-count`. Reading it that way silently
**mis-assigns `relic-completion-level` and `stack-count` on every item.**

Proof is value-preservation across the migration, on the *same item instances* (identical seeds).
Reading the six post-`augment-seed` words in the 2026 file gives `0,0,X,1,0,0`; the 2022 file gives
`relic-completion-level=X, stack-count=1`. The pair is at index 2–3, so exactly two words precede it.
The medal is the discriminator — its `relic-completion-level` is **4**, and the 4 survives at index 0
of the new group, which a reset could not produce. Corrected layout:

```
… :augment-seed :int32
   :13-unk1 :int32          ; NEW
   :13-unk2 :int32          ; NEW
   :relic-completion-level :int32
   :stack-count            :int32
   :13-unk3 :int32          ; NEW
   :13-unk4 :int32          ; NEW
```

**Independently confirmed on a second corpus:** all 130 stash items matched by `(basename, seed)` —
**129/129 confirm the hypothesis, 0 violate it.**

### 1.3 REFUTATION — `play_stats.v` is not a per-skill usage counter

The 2026-07-28 probe § 3.4 hypothesised (explicitly flagged UNTESTED) that the unnamed
`(string, uint32)` vector in `play_stats` was the per-skill counter table behind the `game.PlayStats`
overlay. **It is not.** gd-edit names it `skills-map`, and the measured contents are a five-entry
**movement/dash-rune binding map**:

```
records/endlessdungeon/skills/shrines/rattoshveil.dbr      1
records/skills/itemskillsgdx2/runes/rush_c212.dbr         17
records/skills/itemskillsgdx2/runes/rush_d201.dbr         16
records/skills/itemskillsgdx2/runes/rush_d203.dbr         14
records/skills/playerclass09/viremight1.dbr               23
```

**Hypothesis closed, negative.** The OCR series' per-skill counters are not in the `.gdc`.

**Grade — parse lane: MEASURED.** No block resisted; 4/4 files clean.

---

## 2 — TARGET 1: build identity

### 2.1 Bio, attributes, masteries — MEASURED

| Field | Baseline (as-imported) | End state | Δ |
|---|---:|---:|---|
| header level / class tag | 100 / `tagSkillClassName0109` | 100 / same | — |
| hardcore | 0 | 0 | — |
| `level-in-bio` / `experience` | 100 / 28,475,316 | same | — |
| `attribute-points` unspent | **0** | **0** | — |
| `skill-points` unspent | **0** | **0** | — |
| `devotion-points` unspent | **0** | **0** | — |
| `total-devotion-points-unlocked` | **55** | **55** | — |
| physique / cunning / spirit | 74.0 / **858.0** / 74.0 | identical | — |
| health / energy | 1142.0 / 298.0 | **1154.0** / 298.0 | **+12.0** / — |
| `masteries-allowed` | 2 | 2 | — |
| `skill-points-reclaimed` / `devotion-points-reclaimed` | 405 / 180 | identical | — |

Warlord confirmed by mastery bars: `_classtraining_class01` (Soldier) rank **46**,
`_classtraining_class09` (Oathkeeper) rank **50**.

Against **§ 1.7** ("spend leftover Attributes in Cunning… leave 10 points in the tank"): cunning 858
against physique/spirit 74 each is an emphatic **Cunning dump — MATCH**. The "10 in the tank" is
**MISMATCH**: `attribute-points` unspent is 0. That is fordprefect's V1 file, not tqFan's advice, and
the note attributes the 10-point reserve to tqFan (§ 1.7 quotes 124405, a *different* variant).

`health` +12.0 is the **only** build-identity field that moved. It is not an allocation: physique is
unchanged and unspent points are 0 in both. Across fordprefect's own 2022 backup series `health` ranges
1114–1274 while physique ranges 58–162 **non-monotonically**, so this word is a stored derived pool the
client recomputes, not an allocation record. **Cause UNRESOLVED; impact bounded and benign.**

### 2.2 Skills — MEASURED, zero drift

318 skill entries in the baseline, 367 in the end state. Keyed by `skill-name`:

- **Entries only in the end state: 49.** All are 1.3/FoA content additions. Only **4** carry a rank,
  and all four are auto-granted defaults, not allocations:
  `defaultevade`, `defaulthealthpotion`, `defaultmanapotion`,
  `itemskillsgdx3/potionmodifiers/healthpotion_healovertime` (each level 1).
- **Entries only in the baseline: 0.** Nothing was lost in migration.
- **Common entries with any changed field: 0 of 318**, comparing `level`, `devotion-level`, `enabled`,
  `sublevel`, `devotion-experience`, `autocast-skill-name`, `autocast-controller-name`.
  **2,226 field comparisons, 2,226 identical.**

28 player-class skills hold ranks:

| Soldier (playerclass01) | rank | Oathkeeper (playerclass09) | rank |
|---|---:|---|---:|
| `_classtraining_class01` | 46 | `_classtraining_class09` | 50 |
| `warcry1` / `warcry2` | 12 / 12 | `eyeofreckoning1` / `2` | **15** / 12 |
| `fieldcommand1` / `2` | 10 / 8 | `presenceofvirtue1` / `2` / `3` | 12 / 9 / 10 |
| `passive1` (Fighting Spirit line) | 6 | `divinemandate1` | 12 |
| `passive2` | 1 | `summon_celestialguardian1` | 1 |
| `passive3` | 8 | `summon_celestialguardian2_petmodifier` | 12 |
| `passive4` | 1 | `ascension1` / `2` | 1 / 1 |
| `blitz1` / `blitz2` | 1 / 1 | `viremight1` / `2` / `3` | 1 / 1 / 1 |
| `fightingspirit1` | 1 | `passive02` | 2 |
| `willtolive1` | 1 | | |

Against **§ 1.6**'s named acquisition list: **Eye of Reckoning maxed (15) ✓**, 1pt Vire's Might ✓,
1pt Guardians of Empyrion ✓, Divine Mandate maxed (12) ✓, Ascension ✓, 1pt Blitz ✓,
Presence of Virtue maxed (12) ✓, War Cry ✓, Field Command ✓, Fighting Spirit ✓. **10/10 named skills
present at the described relative priority.** `menhirswill` is **absent**, matching the § 1.6 trap
warning ("don't put 1pt into Menhir's Will").

### 2.3 Devotion — MEASURED, zero drift

`total-devotion-points-unlocked = 55`, `devotion-points` unspent `= 0`, and **exactly 55 devotion
node entries carry `level > 0`.** The three-way conjunctive test from the 2026-07-28 probe § 2.1 is
satisfied in the *affirmative* direction: full allocation, nothing unspent, nothing lost in migration.
Resolved to 11 constellations:

| Constellation | nodes | Celestial power taken |
|---|---:|---|
| Assassin's Blade (`tier1_08`) | 5 | **Assassin's Mark** |
| Tortoise (`tier1_29`) | 5 | **Turtle Shell** |
| Jackal (`tier1_38`) | 3 | — |
| Stag (`tier1_39`) | 4 | — |
| Toad (`tier1_42`) | 4 | — |
| Scales of Ulcama (`tier2_02`) | 6 | **Tip the Scales** |
| Dire Bear (`tier2_05`) | 6 | **(Maul)** — `tier2_05f_skill`, display tag unresolved |
| Crab (`tier2_17`) | 5 | **Arcane Barrier** |
| Kraken (`tier2_21`) | 5 | — |
| Ulzaad, Herald of Korvaak (`tier2_37`) | 6 | **Ulzaad's Decree** |
| Azrakaa, the Eternal Sands (`tier3_20`) | 6 | **Shifting Sands** |
| **total** | **55** | 7 powers |

Against **§ 1.5** (fordprefect V2: *"Bear–Ulzaad–Azrakaa route. You need Scales"*):
**Dire Bear ✓ · Ulzaad ✓ · Azrakaa ✓ · Scales of Ulcama ✓ — 4/4 MATCH.**

### 2.4 Celestial-power bindings — MEASURED, and a flagged risk did **not** fire

All seven proc bindings, with their controllers:

| Celestial power | bound to | controller |
|---|---|---|
| Assassin's Mark (`tier1_08e`) | **Eye of Reckoning** | `cast_@enemyonattackcrit_100%` |
| Turtle Shell (`tier1_29e`) | Field Command | `cast_@selfat50%health_100%` |
| Tip the Scales (`tier2_02f`) | Presence of Virtue | `cast_@enemyonanyhit_33%` |
| Maul (`tier2_05f`) | **Vire's Might** | `cast_@selfonattack_20%` |
| Arcane Barrier (`tier2_17c`) | Divine Mandate | `cast_@selfonanyhit_30%` |
| Ulzaad's Decree (`tier2_37d`) | **War Cry** | `cast_@selfonattack_20%` |
| Shifting Sands (`tier3_20e`) | Summon Celestial Guardian | `cast_@enemyonattack_20%` |

Against **§ 1.5**'s tqFan binding list: *Maul→Vire's Might* ✓ (the stated alternative to Judgment),
*Ulzaad's Decree→War Cry* ✓ ("bind Blitz, later War Cry"), *Crab proc→Divine Mandate* ✓,
*Assassin→EoR* ✓ ("bind Guardians, later EoR"). **4/4 MATCH.**

**This refutes a loudly-flagged risk.** § 4C of the build-of-record predicted that the 1.2.1.5 one-time
reset (*"skills granted by two-handed weapons… Celestial Powers have been unassigned from them"*) would
land on this 2H build and require re-binding before recording. **It did not.** All seven bindings and
both controller strings are byte-identical to the 2022 file. The reset applies to *weapon-granted*
skills; every power here is bound to a **mastery** skill, so none was in scope. **§ 4C's warning is
correct in the abstract and inapplicable to this build — recorded so nobody re-binds a fixture that
does not need it.**

The 47 hotslots recovered from `ui_settings` v7 confirm a populated, intact bar: Vire's Might, War Cry,
Ascension, Blitz, default weapon attack, **Eye of Reckoning ×2**, Summon Celestial Guardian, plus two
item skills — `runes/rush_d203` (from `d203_rune`, equip location 14) and `relics/summondeathstalker`
(from `d114_relic`, equip location 11).

### 2.5 CROSS-LANE RECONCILIATION — "EoR 26" vs "EoR 15" is **not** a disagreement

gandalf's parallel ceremony-cross-verification lane (commit `a963a132`, same day) found the grimtools
calculator inside the `eor-test-1` capture set and graded the fixture **MEASURED, 13/13 gear slots
name-identical to `b28gD0KN`, devotion 55/55, EoR rank 26 = 26**. That lane read the *calculator*;
this lane read the *file*. **Two of the three numbers agree outright and the third only looks like a
conflict.** Recorded here so it never hardens into one:

| Surface | ceremony lane (grimtools) | this lane (`.gdc`) | status |
|---|---|---|---|
| Gear slots | 13/13 name-identical | 13 non-empty entries, all matching | **AGREE** |
| Devotion | 55/55 | 55 nodes, 55 unlocked, 0 unspent | **AGREE** |
| **Eye of Reckoning** | **26** | **15** | **RECONCILED — different scales** |

**The `.gdc` stores ALLOCATED rank; grimtools displays TOTAL rank including gear.** Proven from the
skill's own DBR:

```
records/skills/playerclass09/eyeofreckoning1.dbr
    skillMaxLevel      = 16      <- hard cap on points you can spend
    skillUltimateLevel = 26      <- cap WITH gear bonuses
```

The measured **15** sits one below the 16-point hard cap; **26** is the ultimate ceiling, reachable
only through `+skill` gear. The contributing gear is measurable and present:

- **Sandreaver Bracers** — `augmentSkillName4 = …/eyeofreckoning1.dbr`, `augmentSkillLevel4 = 2` →
  **+2 to EoR directly.** This is precisely § 1.4's *"Sandreaver gloves — BiS for new EoR mods."*
- **Gutsmasher** — `augmentMasteryLevel1 = 2`, `augmentMasteryLevel2 = 2` → +2 to **every** Soldier and
  Oathkeeper skill.
- **Warborn Visor** — `augmentMasteryLevel1/2 = 1` → +1 to both masteries.

**Rule for anyone comparing these two lanes again: a `.gdc` skill rank is never directly comparable to
a grimtools rank.** Add gear before comparing, or compare `.gdc`-to-`.gdc`. Every rank in § 2.2 is
allocated-rank; every rank in the ceremony note is total-rank.

### 2.6 Grade

| Surface | vs the fixture's own construction lineage | vs grimtools `b28gD0KN` |
|---|---|---|
| Level / masteries / attributes | **MEASURED — 100%** | PARTIAL (prose targets only) |
| Every skill rank | **MEASURED — 100%, 0/318 drifted** | PARTIAL — 10/10 named skills MATCH |
| Devotion nodes + points | **MEASURED — 100%, 55/55** | PARTIAL — 4/4 named constellations MATCH |
| Celestial-power bindings | **MEASURED — 100%, 7/7 intact** | PARTIAL — 4/4 named bindings MATCH |

**Why the right-hand column is PARTIAL *from this lane*, stated plainly.** `b28gD0KN` was never read
**by this lane**. Build-of-record § 1.4/§ 1.5/§ 1.6 each say so explicitly — `grimtools.com/robots.txt`
disallows `ClaudeBot` and `Claude-User`, so no per-slot, per-node or per-rank target was ever captured
*into that note*. **I did not fabricate one**; the right-hand column is graded only against the prose
targets that genuinely exist there.

**The gap is nonetheless closed — by the other lane, not this one.** gandalf's ceremony
cross-verification (§ 2.5) obtained the calculator from the `eor-test-1` capture set and returned
13/13 gear, 55/55 devotion, EoR 26 = 26, zero MISMATCH. **Composing the two lanes gives the full
grade:** grimtools says the fixture matches the spec; the save says the fixture did not move across
two sittings. Neither statement implies the other, and together they are the complete answer.

What this lane adds independently, and is arguably stronger than either: the fixture is
**byte-identical to the savefile fordprefect posted in the same forum entry as the `b28gD0KN` link**
(§ 0.1 hash chain), down to per-item seeds. The build-of-record's own § 2.1 named that savefile the
recommended construction path precisely because it "arrives at the terminal state directly." It did.

---

## 3 — TARGET 2: gear identity — MEASURED, and unchanged

**16/16 slots identical on all 12 identity fields, seeds included.** A seed is an item-instance
fingerprint, so this is not "equivalent gear" — it is *the same items*.

| Slot | Item | Component | Augment |
|---|---|---|---|
| Head | **Warborn Visor** (`upgraded/gearhead/d028_head`) + craft `ad201_slowresist` | Prismatic Diamond | Bysmiel's Veiltouch |
| Neck | Imposing **Kaisan's Burning Eye** of Alacrity (`b201e_necklace`) | Seal of Annihilation | Arcanum Dust |
| Chest | **Warborn Chestguard** (`upgraded/geartorso/d026_torso`) | Chains of Oleron | Malmouth Soulguard Powder |
| Legs | Devastating **Solael-Sect Legguards** of the Eagle (`b002e_legs`) | Ancient Armor Plate | Mogdrogen's Touch |
| Feet | **Windshear Greaves** (`upgraded/gearfeet/d007_feet`) + craft `ad201_slowresist` | Spellscorched Plating | Spellward Powder |
| Hands | **Sandreaver Bracers** (`gearhands/d206_hands`) | Restless Remains | Spellward Powder |
| Ring 1 | **Combustion Band** (`rings/d110_ring`) | Runebound Topaz | Steelbloom Powder |
| Ring 2 | Aggressive **Gargabol's Ring** of Oleron's Wrath (`b103e_ring`) | Bloodied Crystal | Arcanum Dust |
| Belt | **Gladiator's Distinction** (`waist/d108_waist`) | Spellscorched Plating | Bysmiel's Veiltouch |
| Shoulders | **Warborn Pauldrons** (`upgraded/gearshoulders/d026_shoulder`) + craft `ao14_oa` | Living Armor | Bysmiel's Veiltouch |
| Medal | Imposing **Mark of Harvoul** of Ruin (`medals/b016e_medal`) | Arcane Spark | **Rune of Violent Delights** (`runes/d203_rune`) |
| Relic | **Deathstalker** (`gearrelic/d114_relic`) | — | — |
| **WS1 main** | **Gutsmasher** (`melee2h/d107_blunt2h`) | Seal of Might | Potent Oleron's Fervor |
| WS1 off | *(empty — 2H)* | | |
| **WS2 main / off** | ***(both empty)*** | | |

Every path above is a DBR record that joins directly to the banked Edition-II `.arz`; names were
resolved through it, so this table is a **live join**, not a transcription.

### 3.1 Weapon set II — the load-bearing answer, and a live hazard

**Measured:** `weapon-sets[1]` is **empty in both slots, in both the baseline and the end state**,
with `use-alt-weaponset = 0` and `alt-weapon-set = 0` — **but `alt-weapon-set-enabled = 1`, i.e. the
weapon-swap key is armed.**

**First, the settled part.** The end-state gear is complete (§ 3, 16/16 slots, seeds intact). **Nothing
was permanently lost in either sitting.** Whatever the sitting-one fingerprint was, it did not survive
to the save.

**Second, a correction to my own first reading.** I initially treated the 20,005 → 15,939 fingerprint
as a DPS step and used "an empty set II would be a near-total DPS collapse, not −20%" to rule the swap
out. Per gandalf's ceremony note (commit `a963a132`), **20,005 is sheet HP**, not DPS. On the HP scale
the arithmetic runs the other way and **the set-II swap hypothesis is not ruled out — it is the leading
candidate.** Swapping to an empty set II unequips **Gutsmasher**, and Gutsmasher carries

```
augmentMasteryLevel1 = 2      +2 to EVERY Soldier skill
augmentMasteryLevel2 = 2      +2 to EVERY Oathkeeper skill
augmentSkillLevel1   = 4
```

Losing +2 across both full masteries drops every `%health` source at once — Haven, Military
Conditioning, the Fighting Spirit line — on top of the weapon's own contribution. **A −20.3% sheet-HP
step is exactly the shape that produces**, and it reverts invisibly on swap-back, leaving the save
showing `use-alt-weaponset = 0` and full gear. **HYPOTHESIS, consistent with every measured field;
the save is an endpoint and cannot confirm it.** U7 is re-scoped accordingly.

**Third, the actionable part.** An **armed swap key over an empty set II** is a standing hazard for
every future sitting on this fixture: one stray keypress silently removes the character's weapon and
+4 mastery ranks mid-run, with no on-screen "you are unarmed" affordance beyond the stat sheet.
**Recommend one of: populate set II with a duplicate 2H, or set `alt-weapon-set-enabled = 0`, before
the next recorded sitting.** Cheap, and it removes a confound from the telemetry rather than leaving
it to be diagnosed from frames afterwards.

### 3.2 Gear vs the build-of-record's prose

§ 1.4's slot table is **V2's**, explicitly — the note says V1's per-slot list is behind the grimtools
boundary and that V2 is "same weapon, same set core, one patch earlier." Measured against it:

**MATCH (6):** Gutsmasher · the 3-piece Warborn set (Visor + Chestguard + Pauldrons — exactly three) ·
Sandreaver · Deathstalker · Windshear.
**DIVERGENT (5):** medal is Mark of Harvoul, not Sigil of the Bear King · no Black Matriarch ring ·
belt is Gladiator's Distinction, not Ugdenbog · legs are Solael-Sect, not Hellforged · amulet is
Kaisan's Burning Eye, not Azrakaa; no Lifegiver ring.

**The divergences are the expected signal, not a failure.** They fall exactly on the flex slots the
note predicted would differ between variants, and the shared core is exactly the "same weapon, same set
core" it predicted would not. § 1.4 also flags *"Helmet and Boots crafted with %4 Armor bonus"* — the
measured helmet and boots are the **only** two slots carrying a `lootaffixes/crafting/` modifier
(`ad201_slowresist`), confirming both are crafted. **MATCH.**

**Grade: MEASURED.** 192 equipment identity comparisons, 0 drift; 129 stash items, 0 drift.

---

## 4 — TARGET 3: Crucible token and access state — MEASURED

`trigger_tokens` (block 10), difficulty slot 2, **end state, file order**:

```
SURVIVALMODE_TIER05CHECKPOINT     SURVIVALMODE_DEFENSEBUILT
SURVIVALMODE_TIER10CHECKPOINT     SURVIVALMODE_POWERUPACTIVE
SURVIVALMODE_NORMAL               SURVIVALMODE_4POWERUPS
SURVIVALMODE_CHALLENGER           GD_STASHED
SURVIVALMODE_GLADIATOR            DISMANTLING_UNLOCKED   ← new
SURVIVALMODE_TIER15CHECKPOINT     CONVERTING_UNLOCKED    ← new
```

**Token delta, baseline → end state: exactly +2, and neither is a Crucible token.**
`CONVERTING_UNLOCKED` and `DISMANTLING_UNLOCKED` were added to difficulty slots 0 **and** 2 — these are
the Fangs-of-Asterkarn item conversion/dismantling features, granted on format migration. Slot 1 is
empty in both.

**Did reaching 150 / dying at 160 mint anything past TIER15? No — and the ladder does not stop at 15.**
The full checkpoint ladder in the Edition-II tag corpus is:

| tag | wave | token | present? |
|---|---:|---|---|
| `tagNotification_Checkpoint05` | 50 | `SURVIVALMODE_TIER05CHECKPOINT` | ✓ (2022) |
| `tagNotification_Checkpoint10` | 100 | `SURVIVALMODE_TIER10CHECKPOINT` | ✓ (2022) |
| `tagNotification_Checkpoint15` | 150 | `SURVIVALMODE_TIER15CHECKPOINT` | ✓ (2022) |
| **`tagNotification_Checkpoint18`** (`SurvivalMode3`, FoA-era) | **180** | `SURVIVALMODE_TIER18CHECKPOINT` (name inferred from the 05/10/15 pattern) | **✗ absent** |

Correct reading: the next rung is **wave 180**, it requires *clearing* 180, and dying at 160 does not
approach it. **This also supersedes the 2026-08-04 probe's "TIER15 is the max checkpoint" framing.**

**And the tokens no longer gate access at all.** GD 1.2.1.3 patch notes, verbatim (banked S5, line 122):

> *"The Crucible no longer requires previously unlocking the wave 50/100/150 checkpoints on a character
> to start on them. **They are now immediately available for all characters.**"*

So the TIER tokens in this save are a **legacy 2022 artifact**, not the mechanism that let Matt start
at wave 150. Other measured access state: `greatest-survival-difficulty-completed = 2` (Gladiator),
`greatest-difficulty-completed = 2` (campaign Ultimate) — both unchanged.

`GD_STASHED` was already present in the 2022 file, so it is a fingerprint of **fordprefect's** GD Stash
use, not of any 2026 construction. **This closes caveat (i) of the 08-01 addendum § 2B.**

`character_info.last-difficulty` reads **66** (`0x42` = difficulty 2 + bit 6) in the end state and in
fordprefect's three oldest backups (`g07`–`g09`), and **2** in his seven newest. It is a legitimate
game-written value, and the correlation with Crucible-heavy periods supports reading bit 6 as a
"last session was survival/Crucible" flag — **INFERRED, and consistent with the end state.**

**Grade: MEASURED.**

---

## 5 — TARGET 4: `play_stats` — MEASURED

| Field | Baseline (2022) | End state | Δ |
|---|---:|---:|---:|
| `playtime-seconds` | 591,060 | 595,790 | **+4,730** (78.8 min) |
| `death-count` | 601 | 604 | **+3** |
| `kill-count` | 162,068 | 162,091 | +23 |
| `hits-inflicted` | 4,850,150 | 4,850,319 | +169 |
| `crits-inflicted` | 645,072 | 651,695 | **+6,623** |
| `hits-received` | 1,013,950 | 1,016,551 | +2,601 |
| `crits-received` | 0 | 0 | 0 (always 0 — field appears unwritten by GD) |
| `health-potions-used` / `energy-potions-used` | 4,700 / 2,012 | unchanged | **0 / 0** |
| `max-level` | 100 | 100 | — |
| **`survival-greatest-wave`** | **170** | **170** | **0** |
| **`survival-greatest-score`** | 22,568,006 | 22,568,006 | **0** |
| **`survival-defense-built`** | **263** | **267** | **+4** |
| **`survival-powerups-activated`** | **390** | **390** | **0** |
| `greatest-damage-done` / `-received` | 1,249,739 / 27,777.2 | unchanged | 0 |
| `champion-kills` / `hero-kills` | 24,211 / 17,464 | unchanged | 0 |
| `endless-souls` / `endless-essence` | 3,014 / 12 | unchanged | 0 |
| `boss-kills` | [0, 0, 361] | unchanged | 0 |
| `last-monster-hit-DA` / `-OA` | 2164.66 / 2289.69 | **2577.65 / 2827.80** | changed |

**Forensics on the death.** `greatest-monster-killed[2].last-monster-hitBy` moved from
`tagEnemySkeletonA02` (Skeletal Archer, 2022) to **`tagNemesis_OrderDeathsVigil01` — "Zantarin, the
Immortal"**, the Order of Death's Vigil Nemesis. The last thing the player hit was
`tagEnemySkeletonC04` ("Death Revenant"). Crucible spawns Nemesis bosses in the high wave bands, so
**Zantarin is the measured proximate cause of the wave-160 death**, and the last enemy's
DA 2577.65 / OA 2827.80 are banked.

**Two counter anomalies, reported not explained.** (a) `kill-count` +23 and `hits-inflicted` +169 are
implausibly small for ~100 Crucible waves of channelled Eye of Reckoning — Crucible kills appear largely
not to increment the campaign counters. (b) `crits-inflicted` +6,623 vastly exceeds `hits-inflicted`
+169, which only coheres if `hits-inflicted` counts **non-crit** hits. Both are **UNRESOLVED**;
neither affects any target. `greatest-damage-done` did **not** move, so nothing in these sittings beat
the 2022 peak.

**Grade: MEASURED.**

---

## 6 — TARGET 5: THE DIFF

### 6.1 `player.gdc.bak` → `player.gdc` — **one field**

The `.bak` is **not** byte-identical to the `.gdc` (different SHA at identical size). Semantically it
is nearly so: of **11,509 leaves, exactly one differs** —

```
play_stats.playtime-seconds :  595,776  →  595,790     (+14 s)
```

Nothing else. Tributes, defenses, tokens, gear, skills, deaths — all already final in the `.bak`.
**Reading: the `.bak` is the 21:52 write and the `.gdc` the 21:54 write; the 14 seconds between them
are post-death menu time. The wave-160 death was already committed at 21:52.** The `.bak` therefore
adds no forensic information the `.gdc` lacks — useful as an independent parse control, which it passed.

### 6.2 Baseline → end state — every changed field

Raw leaf diff: 3,693 of 9,303→11,509. Semantically (keyed, format-normalised) the changes are:

**A. Format migration (not gameplay)**
- `expansion-character?` 3 → 7 (AoM+FG → AoM+FG+FoA mask; **the 08-01 note's INFERRED reading is
  confirmed** by the block-version co-movement)
- block versions: inventory 4→11, stash 6→11, skills 5→8, ui 5→7, play_stats 11→12
- `play_stats.16-unk1/2` appear (v12), `character_skills.8-unk1` appears (v≥6), all 0
- +49 skill entries (1.3 content), 4 auto-granted defaults ranked
- factions 27 → 47 entries; `faction[9]` 0 → −1000, `[24][25][26]` 0 → −1 (new-slot defaults)
- +2 trigger tokens (`CONVERTING_UNLOCKED`, `DISMANTLING_UNLOCKED`)
- ui hotslots 46 → 47
- item `relic-completion-level`/`stack-count` field shift (§ 1.2) — **no semantic change**

**B. Gameplay**
- `playtime-seconds` +4,730 · `death-count` +3 · `kill-count` +23 · `hits-inflicted` +169 ·
  `crits-inflicted` +6,623 · `hits-received` +2,601
- **`survival-defense-built` +4** · `survival-powerups-activated` +0
- `tributes` **999 → 128** · `iron` **+88,032**
- `last-difficulty` 2 → 66 · `last-monster-hit-DA/-OA` changed
- inventory sacks: 2 components gained (**Battered Shell**, **Soul Shard** — Crucible drops);
  `craft_aethercrystalcluster`, `potion_healtha01` ×2 stacks and `potion_energya01` gone. The potion
  removals with **zero** change to `health-potions-used`/`energy-potions-used` point to the 1.3 potion
  rework converting the old tiered potions, not to consumption.

**C. Build identity**
- **`character_bio.health` +12.0. That is the entire list.**

**Grade: MEASURED**, with the § 0.2 caveat stated in the header: the baseline is *as-imported*, not
*as-constructed*, so category A is unavoidably folded into the same diff. Category A is fully
separable by inspection (every item is a version-gated field or a 1.3 content addition), and
categories B and C are clean.

---

## 7 — TARGET 6: regime measurement

### 7.1 The counters — MEASURED, and they match the attestation exactly

| Attested regime (Matt + video, sitting two) | Save field | Measured | Verdict |
|---|---|---|---|
| **FOUR** defense sites purchased (1 aura banner + 3 beacons) | `survival-defense-built` | **263 → 267 = +4** | **CONFIRMED** |
| **ZERO** celestial blessings | `survival-powerups-activated` | **390 → 390 = +0** | **CONFIRMED** |
| **ZERO** site upgrades (Matt only *hovered* the dialog) | `iron` | **+88,032 (net gain)** | **CONSISTENT** — upgrades cost Iron Bits; iron only rose |
| (implicit) no tribute→devotion purchases | `total-devotion-points-unlocked` | **55 → 55** | **CONFIRMED** |

`survival-powerups-activated` **is** the blessing counter, not an arena-pickup counter. Proof from the
Crucible achievement tags (S6): `achS010Desc = "Activate a Celestial Blessing"`,
`achS012Desc = "Activate all 4 Celestial Blessings in a single Crucible"` — and the corresponding
tokens are `SURVIVALMODE_POWERUPACTIVE` / `SURVIVALMODE_4POWERUPS`. **Powerup ≡ Celestial Blessing.**
Likewise `achS009Desc = "Construct 50 Defenses"` pins `survival-defense-built` to constructions.

The four defense names Matt described are all real and named in `tags_survival`: **three beacons**
(Inferno / Deathchill / Stormcaller), **two banners** (Stonewall / **Vanguard**), plus Barricade and
Celestial Beacon. "1 aura banner + 3 beacons" is exactly expressible in this vocabulary, and the
on-camera Inferno Beacon is `tagDefense_Turret01`.

**This is the parse-over-frames graduation the commission asked for: the regime record moves from
ATTESTED to MEASURED on three of four claims, and to CONSISTENT on the fourth.**

### 7.2 Tribute arithmetic — PARTIAL

`tributes`: **999 → 128** (net −871). Two facts reframe this.

1. **The cap is 150.** `tagHUDTribute01Info`, verbatim: *"Tributes are a currency that can be spent on
   various Celestial Blessings, Defenses and to resume at various checkpoints. **You cannot have more
   than 150 Tributes at a time.**"* The 999 is over cap by 849 and was **GD-Stash-injected in 2022** —
   fordprefect's own backup series flips between 999 and 100 across `g00`–`g09`, which is the signature
   of repeated editor writes.
2. **Starting at wave 150 was free.** 1.2.1.3, verbatim: *"Tributes are no longer required to start a
   Crucible at higher waves, **but are still required for restarting or retrying** a Crucible run."*

Therefore the 871 is **not** a spend. Spending 871 on four base defenses with zero upgrades, zero
blessings and zero devotion purchases is not credible. The parsimonious reading is **clamp-on-load**:
the 1.3.0.5 client reduced the over-cap 999 to 150 on first load, after which

```
150 (clamped)  −  spend  +  earnings  =  128        ⟹   net burn 22 below cap
```

which is comfortably consistent with four base-tier purchases plus wave earnings.

**Why this stays PARTIAL and not MEASURED.** (a) Clamp-on-load is **UNVERIFIED** — there is no
intermediate save between the 08-02 construction and the 08-05 end state that would show the clamped
value directly (§ 0.2). (b) Per-purchase costs are **UNRESOLVABLE from the corpus**: an exhaustive scan
of all four `SurvivalMode*.arz` archives for any field matching `cost|tribute|price|merit` returned
**nothing but mana costs and UI widget references**. Crucible prices live in `Grim Dawn.exe`, not in
the database. The consistency test the commission asked for can therefore be run on the **counters**
(§ 7.1, and it passes) but **not** on the currency.

**Cheap closure if wanted:** one screenshot of the Crucible defense-purchase dialog showing a price,
or one save write taken immediately after entering the Crucible and before any purchase.

**Grade: PARTIAL** — counters MEASURED, currency UNRESOLVED.

---

## 8 — TARGET 7: the 2026-08-03 verdict

**Verdict: a third, unattested Crucible engagement occurred on 2026-08-03 ~22:05. Two independent
lines of evidence, one of them inside the save.**

**Evidence 1 — the save (positive).** `death-count` **601 → 604 = +3**. Attested deaths across both
recorded sittings: wave 93 (08-04) and wave 160 (08-05) = **2**. **One death is unaccounted for.**

**Evidence 2 — the arena directories (positive).** `gutsmasher.zip` contains
`maps_survivalworld_a` … `_f` — **six**. The live save directory holds **eight**: `_g` and `_h` were
created after import. Directory mtimes (these survived the copy; the files inside did not):

| dir | mtime | in the 2022 zip? | `.bak` files inside? |
|---|---|---|---|
| `_c`, `_e` | 2026-08-02 00:33 | yes | — |
| `_d` | 2026-08-02 00:51 | yes | yes |
| **`_h`** | **2026-08-03 22:05** | **NO — created** | **yes** |
| `_f` | 2026-08-04 20:24 | yes | — |
| `_g` | 2026-08-04 21:00 | **NO — created** | no |
| `_a` | 2026-08-04 21:25 | yes | yes |
| `_b` | 2026-08-05 21:52 | yes | yes |

`_h` was **created** on 08-03 at 22:05, a full day before sitting one, and was **not touched again**.
It carries `.bak` files, which only appear on a second write — so it was written at least twice, i.e.
it saw actual play, not a single menu touch.

**Bound on what that session did.** It built **zero** defenses and activated **zero** blessings: the
`+4 / +0` counters are fully consumed by the video-attested sitting-two regime (§ 7.1), leaving nothing
for 08-03. Total in-game time across *everything* post-import is only **4,730 s (78.8 min)**, of which
sitting two accounts for ~18 min of wall clock — so 08-02's first load, the 08-03 session and sitting
one share roughly an hour. **The 08-03 session was short.**

**One caution against over-reading the map dirs.** Sitting one alone touched three arena directories
(`_f` 20:24, `_g` 21:00, `_a` 21:25), so a single Crucible *run* evidently moves between arenas as the
wave tiers advance. Map-dir count is therefore **not** a session count. What survives that caution is
the pair that matters: `_h`'s **creation date of 08-03** (isolated from every other session by a full
day) and the **+3 vs 2 death discrepancy**. Those agree, and they agree independently.

**Grade: MEASURED (positive).** The save carries affirmative evidence of activity between construction
and sitting one. What that session *was* — a shakedown run, a settings check, an aborted attempt —
is not recorded anywhere in the file. **Only Matt can name it.**

---

## 9 — TARGET 8: `uid` — the join key does not exist

**MEASURED, negative.** The 16 bytes at the position the 2026-07-28 probe § 3.2 labelled `uid` decrypt
to **all zeros** — in the end state, in the `.bak`, in `g00`, and in fordprefect's 2022 original.

Two things follow.

1. **The label was wrong.** gd-edit — the newer and more actively maintained reference — reads the same
   16 bytes and names them **`mystery-field`**, with no claim that they identify anything. The `uid`
   name came from the older AaronHutchinson C++ port. **There is no per-save UID in `player.gdc`.**
   (The `respawn_list` / `teleport_list` / `shrine_list` UID arrays are *world-object* identifiers —
   riftgates, shrines — and are shared across characters. They are not save identity either.)
2. **The `save_identity` component the artifact-verification note § 505 wanted is not obtainable from
   this field**, and the 2026-07-28 probe § 5's instruction to "bank `uid` as the `save_identity`
   component" **cannot be executed as written**. That instruction should be retired.

**Recommended substitute, since one is genuinely needed:** synthesise the key as
`SHA-256(player.gdc)` — already computed and banked in § 0.1 for every artifact — optionally paired
with `(header.character-name, play_stats.playtime-seconds)` as a human-legible secondary. For this
fixture: `EoRWarlGuts` / `595790` / `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`.

---

## 10 — Corrections to our own prior art

1. **`legolas/notes/2026-07-28-gd-gdc-save-probe.md` § 3.4 — hypothesis REFUTED.** `play_stats.v` is
   gd-edit's `skills-map`, a movement/dash-rune binding table, **not** a per-skill usage counter. The
   OCR series' per-skill counts are not in the `.gdc` at all. (§ 1.3)
2. **Same note, § 3.2 and § 5 — `uid` is a misnomer.** It is gd-edit's unidentified `mystery-field`
   and reads all-zero. The "bank `uid` as `save_identity`" instruction is not executable. (§ 9)
3. **Same note, § 3.3 — the item and skill struct tables are 1.3-only.** They silently mis-read a
   1.1.9.x file. `gdc2.py` supersedes them with version gating. (§ 1)
4. **`legolas/notes/2026-08-04-gd-crucible-checkpoint-edit-probe.md` — "TIER15" is not the top rung.**
   `SurvivalMode3.arz` carries `tagNotification_Checkpoint18` (wave 180). More importantly, since
   1.2.1.3 the checkpoint tokens **no longer gate checkpoint access at all** — every character can
   start at 50/100/150 regardless. **The whole token-edit motivation in that probe is moot on 1.3.0.x**,
   which strengthens rather than weakens its "don't edit, just play" verdict. (§ 4)
5. **`legolas/notes/2026-08-01-eor-endgame-build-of-record.md` § 4C — risk did not fire.** The 1.2.1.5
   two-handed Celestial-Power unassignment does **not** affect this build; all 7 bindings survived
   migration byte-identical. Do not re-bind. (§ 2.4)
6. **Same note, § 2B caveat (i) — resolved.** `GD_STASHED` is present in the 2022 original, so it is
   fordprefect's GD Stash fingerprint, not evidence of 2026 construction.
7. **Same note, § 2B caveat (ii) — resolved.** The three blocks that "failed our parser" (inventory,
   stash, skills) now parse clean; it was version drift, exactly as diagnosed.
8. **gandalf, `v3 §5-AFTERMATH` blessings + banner primer (2026-08-04) — CONTRADICTED.** That note
   records a "banner-only convention, no obelisks/beacons." The Edition-II corpus names **three
   beacons** — `tagDefense_Turret01/02/03` = **Inferno / Deathchill / Stormcaller Beacon** — alongside
   two banners (Stonewall, **Vanguard**), a Barricade and a Celestial Beacon. Matt's video (Inferno
   Beacon on camera) and the game data agree **against** the note. **Routing this to gandalf; the
   §5-AFTERMATH field primer needs the beacon line struck.**
9. **Commission premise — `player.g00` is not the as-constructed baseline.** See § 0.2. Everything
   downstream is graded against the *as-imported* baseline, and the note says so wherever it matters.
10. **This note's own first reading of the weapon fingerprint — CORRECTED before publication.** I began
    by ruling the set-II swap out on a DPS reading of 20,005 → 15,939. It is **sheet HP**. On the HP
    scale the swap becomes the *leading* candidate, because Gutsmasher carries `augmentMasteryLevel1/2
    = 2` and unequipping it strips +2 from every Soldier and Oathkeeper skill at once. § 3.1 records
    the corrected reading and a standing hazard (armed swap key over an empty set II).
11. **Cross-lane scale mismatch — `.gdc` ranks are ALLOCATED, grimtools ranks are TOTAL.** EoR reads
    15 here and 26 in the ceremony note; both are right. Never compare the two scales directly. (§ 2.5)

Findings 1–4, 8, 10 and 11 change future behaviour. Items 5–7 close open caveats.

---

## 11 — Open / unresolved

| # | Item | Why it is open | What closes it |
|---|---|---|---|
| U1 | ~~**`b28gD0KN` per-surface comparison**~~ | **CLOSED 2026-08-05 by the ceremony lane** (commit `a963a132`) — the calculator was in the `eor-test-1` capture set; 13/13 gear, 55/55 devotion, EoR 26 = 26, zero MISMATCH. Reconciled against this lane in § 2.5 | — |
| U2 | **Crucible tribute prices** | not in any `SurvivalMode*.arz` — engine-side | one screenshot of the purchase dialog, or a save write taken pre-purchase inside the Crucible |
| U3 | **Clamp-on-load of over-cap tributes** | plausible and near-necessary, but no intermediate save exists to show it | load any over-cap GD-Stash save on 1.3.0.5 and save immediately |
| U4 | **`character_bio.health` +12.0** | derived pool, moves independently of physique in the historical series too | low value; bounded and benign |
| U5 | **What the 08-03 session was** | the save records that it happened, not what it was | Matt's recollection |
| U6 | **`kill-count` +23 / `hits-inflicted` +169** for ~100 waves | Crucible kills appear not to increment campaign counters | compare against a campaign-only session on the same character |
| U7 | **Sitting-one 20,005 → 15,939 sheet-HP fingerprint** | set-II swap is the **leading** candidate, not ruled out (§ 3.1 — Gutsmasher carries +2 to both masteries, so unequipping it collapses every `%health` source at once); the save is an endpoint and holds no history | frame-level re-review for the weapon icon / the swap indicator at the step; or reproduce by pressing the swap key on the fixture and reading the sheet |
| U8 | **`13-unk1..4` semantics** | positions now proven (§ 1.2), meanings unknown; all zero except the two migrated words | a save with a non-trivial value in one of them |
| U9 | **`14-unk2` / `14-unk4`** | observed 1 and 0; `hotslot-count` identified, these two are not | a save with a differently-sized hotbar |

---

## 12 — Grade summary

| # | Target | Grade |
|---|---|---|
| — | Parse lane (all four files, all blocks, all checksums) | **MEASURED** |
| 1 | Build identity vs the fixture's construction lineage | **MEASURED — 3,589/3,590 fields identical (99.97%)** |
| 1′ | Build identity vs grimtools `b28gD0KN` | **PARTIAL from this lane, MEASURED when composed with the ceremony lane.** From the file alone: every prose-level target the build-of-record captured MATCHES — **10/10** named skills, **4/4** constellations, **4/4** proc bindings, **2/2** crafted slots; gear scores **6/11** against § 1.4's list, which is **V2's by the note's own statement** (the 6 are its "same weapon, same set core", the 5 divergences are its flex slots). The grimtools comparison itself was closed same-day by gandalf's ceremony lane — 13/13 gear, 55/55 devotion, EoR 26 = 26 — **reconciled to this lane's allocated-rank scale in § 2.5** |
| 2 | Gear identity, components/augments, weapon set II | **MEASURED** — 16/16 slots, seeds included; set II empty in both |
| 3 | Crucible tokens / tributes / wave / score fields | **MEASURED** — +2 non-Crucible tokens only; nothing minted |
| 4 | `play_stats` | **MEASURED** |
| 5 | THE DIFF (`g00`→`gdc`, and `gdc.bak`→`gdc`) | **MEASURED** (baseline caveat § 0.2; `.bak` diff = 1 field) |
| 6 | Regime measurement | **PARTIAL** — counters MEASURED (+4 / +0 / devotion 55→55), currency UNRESOLVED (U2, U3) |
| 7 | The 2026-08-03 mystery | **MEASURED (positive)** — a third session occurred; its content is unrecorded (U5) |
| 8 | `uid` join key | **MEASURED (negative)** — field is all-zero and misnamed; substitute proposed |

---

**Signed:** legolas, 2026-08-05. The scout went to the far bank this time and brought back the whole
map. The fixture is exactly what it claimed to be — fordprefect's character, unaltered, down to the
item seeds — and the regime the frames attested is now written in the file's own counters. Two things
the save knows that we did not: a Nemesis named **Zantarin, the Immortal** ended the wave-160 run, and
**somebody played this character on the third of August.**

*Note on composition:* this lane and gandalf's ceremony lane ran in parallel against the same fixture
from opposite directions — the calculator and the file. They agree everywhere they overlap once the
allocated-vs-total rank scale is applied (§ 2.5). Reading either note alone will produce a false
contradiction on Eye of Reckoning; read the reconciliation first.

---
---

# POST-COMMIT CORRIGENDA — appended 2026-08-08

> **Read this before using §§ 2.5 or 7.2 above.** These blocks are **appended, not rewritten**: the
> original text is left standing so the lineage of the correction is legible. Where a corrigendum and
> the body disagree, **the corrigendum governs.** Filed by legolas under the KC2-SIM Phase-B micro-probe
> (conductor: gandalf), Task 4. Both items were queued debt from the G-A fold.

## C-1 — § 7.2 / U3 tribute arithmetic — **PARTIAL → CLOSED on camera. The ledger balances exactly.**

**Status change: U3 (clamp-on-load) and U2 (Crucible prices) are both CLOSED.** § 7.2's grade line
*"PARTIAL — counters MEASURED, currency UNRESOLVED"* is **superseded**; the currency is now MEASURED.

galadriel's sitting extraction (`galadriel/notes/2026-08-07-eor-sittings-extraction.md` **§ 1**) read the
Crucible tribute counter directly off both videos at 10 Hz (ROI `x 1360..1440, y 98..124`), localising
every debit to ±0.1 s and naming each purchase from the confirmation dialogue in the preceding frame.
The full ledger:

| step | value | evidence |
|---|---:|---|
| sitting 1, prep + entire 1→93 ramp | **150 flat**, t = 300 → 2240, **zero debits of any size** | `evidence/s1-tribute-ledger-flat-150.png` |
| − 5 · wave-93 checkpoint restart (attempt 2) | **145** from t = 2440 to end of s1 recording | § 1 |
| *(sittings are contiguous — nothing spent between them)* | s2 **opens at 145** at t = 60 | § 1 cross-sitting continuity check |
| − 5 · Deathchill Beacon @ t = 476.8 | 140 | `evidence/s2-defense-ledger-all-four.png` |
| − 5 · Stormcaller Beacon @ t = 484.1 | 135 | ″ |
| − 5 · Inferno Beacon @ t = 502.3 | 130 | ″ |
| − 5 · Vanguard Banner @ t = 509.6 | **125** | `evidence/s2-defense4-VANGUARD-BANNER-t509.4.png` |
| held 125 from t = 512 → 850 — **zero upgrades, zero blessings** | 125 | § 1 |
| + 3 in-run awards | **128** by t = 900 | § 1 |
| **= the save-observed value** | **128** ✔ | § 7.1 / § 5 above |

```
150  −  5 (restart)  −  20 (4 × base defense)  +  3 (in-run awards)  =  128
```

**Three corrections to the body text:**

1. **The clamp-on-load hypothesis is CONFIRMED, and its start value is now observed, not assumed.**
   § 7.2 reasoned from `999 → 128` to a hypothesised clamp at 150. The camera shows the counter
   **pinned at exactly 150** across sitting 1's whole prep phase and 93-wave ramp. The 999 never
   reached the Crucible. § 7.2's *"clamp-on-load is UNVERIFIED"* is retired.
2. **The −5 restart debit was missing from the body's model.** § 7.2 wrote `150 − spend + earnings = 128
   ⟹ net burn 22 below cap` and attributed it to *"four base-tier purchases plus wave earnings."* The
   22 is really **25 spent (20 defenses + 5 restart) less 3 earned.** The restart term is the one the
   file could not see, and it is exactly the term v1.2.1.3 predicts: *"Tributes … are still required for
   restarting or retrying a Crucible run."* **The M1/M2 distinction is now visible in the fixture's own
   currency, not just in the patch notes.**
3. **§ 7.2's premise that prices are unresolvable is wrong and was already corrected once.**
   *"Crucible prices live in `Grim Dawn.exe`, not in the database"* — they do not; they are in
   `Conversations.arc` (`object_defensesite_01.cnv`: *"spend 5 Tributes + 7000 Iron Bits"*;
   `npc_event_03.cnv`: the 5 / 15 / 30 restart ladder). First corrected in
   `legolas/notes/2026-08-07-u8-tier-wave-map.md` § 6.2 / § 7; **now confirmed on camera** — the
   observed debits are 5 apiece, and the fourth purchase's dialogue reads *"Create this defense (spend
   **5 Tributes** + 10000 Iron Bits)"*, matching the `.cnv` exactly.

**The U-8 residual is retired, and it retires in the right direction.** `2026-08-07-u8-tier-wave-map.md`
§ 7 left *"a residual of ~2"* against a 150-clamp model and declined to claim closure. That residual
decomposes cleanly as **−5 (restart, unknown to that pass) + 3 (awards)**. The same note predicted the
failed-checkpoint award from `rewards.lua` as **≈ 2.6 Tributes**; the camera shows **+3**. The formula
was right; the ledger was one term short.

**Grade for § 7.2: MEASURED.** Counters MEASURED (§ 7.1, unchanged); **currency MEASURED**.
**U2 CLOSED · U3 CLOSED.** § 12's row 6 (*"PARTIAL — … currency UNRESOLVED (U2, U3)"*) should be read
as **MEASURED**.

*Also correct in § 7.2's spirit and worth keeping:* the reasoning that "871 is not a spend" was right,
and right for the right reason.

## C-2 — § 2.5 gear attribution — **arithmetic CORRECTED. The § 2.5 CONCLUSION is UNCHANGED.**

Per `legolas/notes/2026-08-07-pe1-eor-spin-parameters.md` §§ 5.1 and 7.1, which read the live item
records rather than inferring from field names.

**§ 2.5 as written is wrong on both named gear sources:**

- *"**Gutsmasher** — `augmentMasteryLevel1 = 2`, `augmentMasteryLevel2 = 2` → +2 to **every** Soldier and
  Oathkeeper skill."* **WRONG.** Gutsmasher's mastery names are
  `augmentMasteryName1 = _classtraining_class01` (**Soldier**) and
  `augmentMasteryName2 = _classtraining_class03` (**Occultist**). Not Oathkeeper.
- *"**Warborn Visor** — `augmentMasteryLevel1/2 = 1` → +1 to both masteries."* **WRONG.** The Visor's
  names are `class01` (**Soldier**) and `class08` (**Necromancer**). Not Oathkeeper.
- **No equipped item on this fixture grants any Oathkeeper mastery rank.** Eye of Reckoning is
  `playerclass09` (Oathkeeper), so **the mastery route contributes ZERO to EoR.** The `+11` comes
  entirely from *direct* `+skill` and `+all-skills` grants.

**The corrected attribution — the real +11, DB-CITED:**

| source | record | field | +EoR |
|---|---|---|---:|
| allocated | `player.gdc :: character_skills` | `eyeofreckoning1.level` | **15** |
| **Gutsmasher** | `items/gearweapons/melee2h/d107_blunt2h` [GDX2] | `augmentSkillName2` / `Level2` | **+4** |
| **Warborn Visor** | `items/upgraded/gearhead/d028_head` [GDX2] | `augmentSkillName1` / `Level1` | **+2** |
| **Warborn Chestguard** | `items/upgraded/geartorso/d026_torso` [GDX2] | `augmentSkillName4` / `Level4` | **+2** |
| **Sandreaver Bracers** | `items/gearhands/d206_hands` [**GDX3**] | `augmentSkillName4` / `Level4` | **+2** |
| **Kaisan's Burning Eye** | `items/gearaccessories/necklaces/b201e_necklace` [GDX2] | **`augmentAllLevel = 1`** | **+1** |
| Warborn set, 4-pc bonus | `items/lootsets/itemset_d025b` | `augmentSkillLevel4 = [0,0,0,3]` | **+0** — only 3 pieces worn |
| | | **TOTAL** | **26** |

**15 + 11 = 26 = `skillUltimateLevel`. Two lanes that never touched each other — the `.gdc` and the
`.arz` — land on the same integer, and it is gandalf's ceremony-lane grimtools reading.**

Two narrower fixes inside § 2.5, both about *which* source carries the grant:

- § 2.5 credits **Sandreaver Bracers** as *"gloves"* with `+2` — the `+2` and the record are right; the
  slot is **hands/bracers**, and it is a **GDX3** record, the only Fangs-of-Asterkarn item in the +11.
- § 2.5 omits **Warborn Chestguard** (`+2`) and **Kaisan's Burning Eye** (`augmentAllLevel = 1`, `+1`)
  entirely. Those three points are why the note could only gesture at 26 rather than reach it.

**What does NOT change.** § 2.5's conclusion, its table, and its rule all stand:

> Gear slots **AGREE** · Devotion 55/55 **AGREE** · **Eye of Reckoning 26 (grimtools, total) vs 15
> (`.gdc`, allocated) — RECONCILED, different scales.** `skillMaxLevel = 16`, `skillUltimateLevel = 26`.
> **"A `.gdc` skill rank is never directly comparable to a grimtools rank."**

Only the arithmetic underneath it was wrong; **cite EoR at TOTAL 26**, unchanged. The correction makes
§ 2.5 *stronger*, because the reconciliation now closes on the exact value instead of pointing at it.

*Related, and already carried in the P-E1 note § 7.2 — not restated here:* § 3.1's weapon-set-II hazard
is sharper than recorded (EoR's `Mace2h = True` / all ranged-and-caster `False` gate means an empty set
II makes the build's only damage skill **uncastable**, not merely weaker).

**Signed:** legolas, 2026-08-08. Two debts paid. The tribute ledger balanced the moment the camera
supplied the one term the file could not hold — a five-Tribute restart — and the `+11` turned out to
come from five items, none of them via the mastery route I had assumed.
