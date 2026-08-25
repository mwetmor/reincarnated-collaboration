# MD-B4app-2d — hot-bar ground truth from the referent save file

> **CAPTURE NOTE (gandalf RUN-CONDUCTOR, 2026-08-25):** the lap harness blocked legolas's note write; the full findings text was returned in the lap result and is captured here VERBATIM by the conductor. Authority is legolas's; the capture is durable per the Pattern-A-deep capture convention. The lap's 20 code/data artifacts in this directory were swept into knight-rider commit `d7835900` (S2C push-as-you-go posture) before the seat could commit — contents verified intact byte-for-byte by the seat; disposition recorded below and in charter row L-90.

---

## ⚑ First: commit + sweep record

**My 20 lap artifacts were swept into another session's commit before I could commit them.**

- Sweeping commit: **`d7835900`** — `knight-rider(S2C): Matt extended push-as-you-go to godot for this session…` (21 files: my 20 + their `step2-vfx-archetype-mint-wave-record.md`).
- **Contents verified intact:** `git diff HEAD` over my lap directory is empty — every committed blob matches my working tree byte-for-byte. `__pycache__` was not swept.
- ⚑ **Disposition, which the content check does not cover (CLAUDE.md REFINEMENT (b)):** my work now sits under the **S2C wave's push posture**, not mine — and that posture is *push-as-you-go*, so **`d7835900` is already on `origin`** (`git rev-list --count origin/main..HEAD` = 0). My lap artifacts reached the remote under knight-rider's authorization, before this lap finished. Nothing lost; **the release was not mine to make and was made.**
- **I did not push and did not attempt to.** Recording this per the standing repair-by-record convention so the owner-of-record is not silently wrong.

Two mechanical notes worth banking: `git commit --only <paths> -m <msg>` with `-m` *after* the pathspecs fails to match, **and `--only` empties the index on that failure** — which is what made the sweep look at first like a disappearance. `pwd` first (per the standing rule) ruled out the cwd-drift false alarm in one call.

**Files:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-md-b4app-2d/` — `gdc_read.py`, `decode_hotbar.py`, `dump_block.py`, `dbr_probe.py`, `hotbar-decode.json`, `save-copy/` (15 `.gdc` files).

---

**Lap:** KC2 MODEL-COMPLETION, decode lap MD-B4app-2d · **Agent:** legolas · **Conductor:** gandalf
**Authority:** charter rows L-86 / L-87 · **Date:** 2026-08-25
**Access mode:** READ-ONLY against Matt's PC throughout. Files copied out by tar-pipe over SSH; nothing on the PC written, moved, or opened by a tool with a write path. The parsers have no write path.

## Headline

> **Slot L is `records/skills/playerclass01/blitz1.dbr` — BLITZ, the Soldier charge, bound to the LEFT MOUSE BUTTON.** DBR class `Skill_AttackWeaponCharge`, `skillCooldownTime = 3.5 s`, rank 1, cooldown rank-invariant.
>
> **Slot R is `records/skills/playerclass09/eyeofreckoning1.dbr` — the EoR channel itself, bound to the RIGHT MOUSE BUTTON.** Rank 15. It is the only bar skill in the file with **no `skillCooldownTime` field at all** — the format's own signature of a channel.
>
> galadriel's `L` and `R` are not bar positions. They are **the two mouse-button icons at the centre of Grim Dawn's action bar**, and the save binds them. That converts H-MC-2 from "which icon is the culprit" into a **binding** question: the suspected interrupter is the left-click skill and the channel is the right-click skill, **on the same mouse.**

The identification does not rest on the cooldown match. It rests on a **12/12 occupancy census** (§4) that independently refutes five of the six other hot-bar configurations recovered from the save series. The cooldown is corroboration.

## 1 — Character disambiguation

| Save dir | Header name | Level | Size | Crucible | Verdict |
|---|---|---|---|---|---|
| `_EoRWarlGuts` | `EoRWarlGuts` | 100 | 98,096 B | `maps_survivalworld_a…h.map`; `survivalWaveTier=170`, `greatestSurvivalScore=22,568,006` | **THE REFERENT** |
| `_DawnGuard` | `DawnGuard` | 1 | 8,932 B | none | not a candidate |
| `_custom` | `custom` | 1 | 7,394 B | none | not a candidate |

`_EoRWarlGuts` measures out on four independent fields: `header.tag = tagSkillClassName0109` (masteries 01+09); `_classtraining_class09` rank **50** (Oathkeeper) + `_classtraining_class01` rank **46** (Soldier), `masteriesAllowed=2` ⇒ **Warlord**; `eyeofreckoning1` rank **15** (+`eyeofreckoning2` rank 12) ⇒ **EoR build**; `survivalWaveTier=170` ⇒ waves 150–160 inside range. No disambiguation was needed — only one candidate exists.

*(`_DawnGuard` is L1/8.9 KB, **not** the L12 Soldier/werewolf character from KIT-CAL-1. **Queue row T11's target does not appear to survive on this PC.** Noted for the conductor; not my commission, not acted on.)*

### 1.1 — Two save locations; the live one is not the Steam-cloud one

`Documents` is **OneDrive-redirected**, which is why the commission's literal path missed.

| Location | `player.gdc` mtime | size | `playTime` | Status |
|---|---|---|---|---|
| `…\OneDrive\Documents\My Games\Grim Dawn\save\main\_EoRWarlGuts\` | **2026-08-24 22:50** | 98,096 | 595,993 | **LIVE** |
| `…\Steam\userdata\116655798\219990\remote\save\main\_EoRWarlGuts\` | 2026-08-02 00:20 | 87,820 | 591,060 | stale cloud mirror |

Both retrieved. **15 files, SHA-256 verified against remote `certutil`, 3/3 spot-check.**

## 2 — Format: what drifted, and the method that survived it

The community reference is pinned to GD 1.1.9.1; Matt's build is Fangs-of-Asterkarn era. **Four block interiors drifted** and the reference parse throws on first contact — exactly as §4 of my 2026-07-28 lane map predicted.

| Block | Ref | Observed | Drift |
|---|---|---|---|
| `character_info` (1) | 5 | 5 | loot-filter array 39 → **42** bytes, **no version bump** |
| `inventory` (3) | 4 | **11** | not decoded (not needed) |
| `character_skills` (8) | 5 | **8** | **one extra byte after `enabled`** |
| `ui_settings` (14) | 5 | **7** | ~12 B extra preamble; slot array **46 → 47** |
| `play_stats` (16) | 11 | **12** | trailing fields added |

**The method, and it is the transferable part of this lap:**

> The top-level block ID sequence is fixed, and the first word of every block is `read_int()` of that ID. **That is known plaintext, so the key is recoverable at every block boundary independently** — `key = ciphertext XOR block_id`. Walking the declared lengths indexes the entire file **without parsing a single interior**, and a drifted block can be *skipped* rather than guessed at.

The index is self-verifying — it must land exactly on EOF. **It did, on all 15 files** (live save: 15 blocks, final position 98,096 == file size 98,096).

Second consequence: because the key advance is a per-byte fold over consumed ciphertext, **the key state at every offset inside a block is computable from the block start alone**, identically whether preceding bytes were read as ints or bytes. So a drifted block can be dumped in two plaintext views (byte-wise / int-wise) and its real layout *read off* rather than assumed. That is how `ui_settings` v7 and `character_skills` v8 were recovered.

## 3 — Full slot table (LIVE save)

| idx | Screen position | Bound record | Class | Cooldown |
|---|---|---|---|---|
| 0 | key **1** | *(empty)* | — | — |
| 1 | key **2** | `…/playerclass09/viremight1.dbr` | `Skill_AttackPathCharge` | **3.5999999 s** |
| 2 | key **3** | `…/playerclass01/warcry1.dbr` | `Skill_AttackRadius` | 7.5 s |
| 3 | key **4** | `…/playerclass09/ascension1.dbr` | `Skill_BuffSelfDuration` | 24.0 s (duration 10.0 s) |
| 4 | key **5** | *(empty)* | — | — |
| 5 | key **6** | *(empty)* | — | — |
| 6 | key **7** | `…/itemskillsgdx2/runes/rush_d203.dbr` *(item skill ← `…/enchants/runes/d203_rune.dbr`, equipLoc 14)* | `Skill_AttackPathCharge` | 2.5 s |
| 7–9 | keys **8, 9, 0** | *(empty)* | — | — |
| **10** | **weapon-set-1 LEFT click** | **`…/playerclass01/blitz1.dbr`** | **`Skill_AttackWeaponCharge`** | **3.5 s** |
| 11 | weapon-set-2 LEFT click | `…/default/defaultweaponattack.dbr` | — | none |
| **12** | **weapon-set-1 RIGHT click** | **`…/playerclass09/eyeofreckoning1.dbr`** | **`Skill_AttackRadiusSpin`** | **no `skillCooldownTime` field** |
| 13 | weapon-set-2 RIGHT click | `…/playerclass09/eyeofreckoning1.dbr` | as above | — |
| 18 | secondary bar #5 | `…/playerclass09/summon_celestialguardian1.dbr` | `Skill_TargetedSpawnPet` | 20.0 s |
| 19 | secondary bar #6 | `…/itemskillsgdx1/relics/summondeathstalker.dbr` *(item skill ← `…/gearrelic/d114_relic.dbr`, equipLoc 11)* | `Skill_SpawnPet` | 15.0 s |
| 24 / 25 | health / energy potion | *(types 2 / 3)* | — | — |

All other indices empty. **`weaponSwapActive = 0`** ⇒ weapon set 1 is active, so the on-screen mouse icons are indices **10 and 12**, not 11 and 13.

**Ranks** (367/367 skill records parsed): Blitz **1**, Vire's Might **1**, Ascension **1**, War Cry **12**, Eye of Reckoning **15**, Celestial Guardian **1**. `skillCooldownTime` is a **scalar** in every one of these DBRs while damage fields are 26-entry rank arrays — so **cooldown is rank-invariant** and rank 1 vs 15 moves no number above. Cooldowns are **identical in depot editions II (2026-07-24) and III (2026-08-08)** — no patch moved them across the referent window.

### 3.1 — Why the mapping is verified, not assumed

The v7 slot array starts at an unknown offset. Rather than guess, the decoder tries every plausible start and accepts one only if **three independent anchors** hold: (1) the chain lands **exactly** on the trailing `cameraDistance` float; (2) slot **24** decodes as type 2 (health potion); (3) slot **25** as type 3 (energy potion). It accepted start = 67, uniquely. A fourth anchor then falls out unforced and is the one that matters: **indices 10–13 decode as `blitz1` / `defaultweaponattack` / `eyeofreckoning1` / `eyeofreckoning1`** — a left-click attack and a right-click channel, precisely what those indices are documented to be. A wrong alignment does not produce that.

## 4 — Slot L: identification and evidence

galadriel's slot boxes (`galadriel/pipeline/eor_cooldown.py:114`), left to right:

```
"1"  "2"  "3"  "4"  "5"   "L"   "R"   "6"   "7"   "8"   "9"   "0"
701  742  784  827  869   917   962  1007  1049  1092  1134  1177
```

That is Grim Dawn's actual HUD: keys **1–5**, then **the two mouse-button icons**, then keys **6–0**. Her labels map to save indices `1..5 → 0..4`, **`L → 10`**, **`R → 12`**, `6..0 → 5..9`.

**The census test.** Her note records: *"Slots 1, 5, 6, 8, 9 and 0 are EMPTY on this build"* — a 12-position occupancy fingerprint measured **on the footage itself**. Tested against every configuration in the save series:

| State | `playTime` | 1 | 2 | 3 | 4 | 5 | L | R | 6 | 7 | 8 | 9 | 0 | vs census |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g09 | 575,543 | soulscythe1 | viremight1 | ascension1 | · | soultransfer | shadowstrike_d218 | EoR | · | · | · | · | · | **refuted** |
| g07, g08 | 576,551–576,584 | · | viremight1 | ascension1 | · | · | blitz1 | EoR | · | · | · | · | · | **refuted** |
| g04–g06 | 580,838–581,773 | shadowstrike_d218 | viremight1 | warcry1 | ascension1 | · | shadowstrike_d218 | EoR | · | · | · | viremight1 | viremight1 | **refuted** |
| **g00–g03, cloud** | **588,122–591,060** | · | viremight1 | warcry1 | ascension1 | · | **blitz1** | **EoR** | · | rush_d203 | · | · | · | **MATCH 12/12** |
| **bak, LIVE** | **595,826–595,993** | · | viremight1 | warcry1 | ascension1 | · | **blitz1** | **EoR** | · | rush_d203 | · | · | · | **MATCH 12/12** |

Six of twelve states match on all twelve positions, and **all six carry an identical visible bar.** The other six are each refuted by a position she measured empty and the save shows occupied, or the reverse.

**Corroborating signatures, none used to make the identification:**

| galadriel's measurement | Save + DBR | Fit |
|---|---|---|
| slot L "figure mid-stride", **~3.6 s**, 12 casts | **Blitz**, `Skill_AttackWeaponCharge`, **3.5 s** | +0.10 s |
| slot 4 dim run **24.4 s** | **Ascension**, `skillCooldownTime` **24.0 s** | +0.4 s |
| slots **2, 7, R permanently blind** — red icon art | Vire's Might, a **rune** icon, and EoR — all red/orange art | exact set |
| slot R never counted as a cast | EoR **is the channel**; no cooldown field exists | structural |

### 4.1 — What this does to H-MC-2 (stated as fact; interpretation is the conductor's)

1. **Slot L and slot R are the same mouse.** L is left-click; R is right-click and is the channel. In Grim Dawn a left-click activation and a held right-click channel are mutually exclusive character actions. If the 8 Type-B interrupts are slot-L casts, the mechanism on offer is **binding exclusivity, not skill identity** — the Layer-1/engine-behaviour reading L-86 pre-named, and **a rule that transfers to Godot without carrying a Grim Dawn skill with it.**

2. **"Charge skill" does not discriminate on this bar; "left click" does.** There are **three** `…Charge`-class skills bound: Blitz (L, 3.5 s), Vire's Might (slot 2, 3.6 s), Rune of Rush (slot 7, 2.5 s). Slot 2 carries 22 of the 53 casts and is *not* the outlier in the family test. So "charge skills interrupt" is **not** the rule the standing p=0.0090 points at; "the left-click skill interrupts" is.

3. ⚑ **The blind slot is a charge skill, and that bounds the converse test.** Slot 7 is **Rune of Rush**, `Skill_AttackPathCharge`, 2.5 s — and slot 7 is one of the three permanently-blind slots. **Its casts are not in the 53-cast population at all.** So P(interrupt|slot-L) vs P(interrupt|other) is computed over slots 2/3/L only and **cannot see the one other charge skill that is neither slot L nor slot 2.** If H-MC-2 is supported, this is the named residual: the footage cannot separate "left-click interrupts" from "charge interrupts", because slot 7 was never measurable.

**The 53-cast population is now fully named:** slot 2 = **Vire's Might** (22), slot 3 = **War Cry** (19), slot L = **Blitz** (12).

## 5 — Staleness window

**Matt's "~1 month ago" is off by about ten days, and the true date is recoverable.** The referent footage is `/Users/admin/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` — **recorded 2026-08-05 21:37:25**. Corroborated inside the save directory: `maps_survivalworld_b.map` mtime **2026-08-05 21:52**, fifteen minutes into that recording.

**No retrieved save is from the referent session.** The fight sits in a bracket:

| | State | `playTime` | Visible bar |
|---|---|---|---|
| **before** | cloud + `g00`, 2026-08-02 00:20 | 591,060 s | **config A** |
| — | **referent fight, 2026-08-05 21:37** | *(between)* | *(measured 12/12 = config A)* |
| **after** | `player.gdc`, 2026-08-24 22:50 | 595,993 s | **config A** |

Bracket width **4,933 in-game seconds (≈82 min), 19 days wall-clock**. Both ends carry the **identical visible bar**, and the census on the footage matches that same bar and refutes every other configuration. **The staleness window exists but is not load-bearing for this lap's answer.**

Two things changed inside the bracket; neither touches a visible slot:
- **A game patch landed** — `ui_settings` **v5 (46 slots) → v7 (47 slots)**, `character_skills` v5→v8, `play_stats` v11→v12.
- **The non-visible secondary bar was cleared** — indices 14–17 held `fieldcommand1`, `divinemandate1`, `compa_presenceofmight_01`, `presenceofvirtue1` on 08-02 and are empty on 08-24 (index 13 gained a second EoR binding). Indices 14–25 are the **secondary** bar and are **not in galadriel's 12-box strip**. Plausibly patch migration of passive auras rather than a player edit; **not determined here.**

**On Matt's attestation** — *"the hotbar was pre-set from the save file and I did not alter it."* The evidence **supports it for the fight**, and refines it: the bar was **not** static across the character's life — it changed at least four times over `playTime` 575,543 → 591,060. It was static across the fight bracket, which is what the attestation actually claims.

## 6 — Honesty rails

1. **Median dim run is not a cooldown estimator, and two disagreements say so.** Ascension (24.0→24.4) and Blitz (3.5→3.60) land within 0.4 s; Vire's Might (3.6→**3.15**) and War Cry (7.5→**4.55**) do not, War Cry by 2.95 s. **Do not read a cooldown-reduction figure out of these deltas** — they run in *both directions*, which is the tell that they are not measuring one quantity.
2. **Cooldown reduction is NOT MEASURED.** It lives in `inventory` (v11, undecoded) and devotion. `devotionReclamationPointsUsed = 180` and 285 skill entries carry non-zero `devotionLevel` — heavily devotion-invested, almost certainly carrying CDR. Recovering it means decoding `inventory` v11, which this lap did not need and did not attempt.
3. ⚑ **Slot 4 may be a cast, not a buff timer — and if so the cast census is short.** galadriel excluded slot 4 reading its white numeral as buff duration. The DBR says Ascension's **cooldown is 24.0 s** and its **active duration is 10.0 s**; her 24.4 s matches the *cooldown*. Two readings survive: gear `+skills` raises the effective duration above rank-1's 10.0 s, or it is the cooldown and slot-4 dim runs are casts. **Her instrument, her call** — flagged because it bears on the 53.
4. **`itemSkills` is empty (0 entries)** despite two item-granted skills being bar-bound; the bindings carry their own `item` + `equipLocation`, which is where the rune/relic identities come from. Noted so emptiness is not later read as evidence of absence.
5. **`inventory` (v11) was skipped, not guessed** — equipped gear, the poison-DoT item question and CDR remain **NOT RECOVERED**.
6. **`uid` reads as 16 zero bytes** in every file — the `save_identity` join key from my 2026-07-28 probe §5 is **null on this character**, not failed-to-read (the index lands on EOF regardless).
7. **The bar-config-to-file binding is inferential; the bar identity is not.** Six files agree unanimously. If the referent bar were a seventh configuration older than `playTime` 575,543 sharing the same 12-position occupancy pattern with different skills, the census could not tell. No evidence suggests it and six states contradict it — but that is the shape of the residual and it is not zero.
8. **Slot-index→screen-position was DERIVABLE after all** (the commission allowed it might not be), and was verified against three structural anchors plus the independent census. The reconciliation never had to fall back to cooldown+shape.

## 7 — Sources

| # | Source | Class |
|---|---|---|
| S1 | `AaronHutchinson/Grim-Dawn-Save-Decryption` — `decrypt-player.{cpp,h}`, `decrypt-helper.h` | Primary (working implementation), re-fetched 2026-08-25 |
| S2 | Matt's PC `mhwet@192.168.1.133` — the save files | **Primary (the artifact)** |
| S3 | Depot `.arz` corpus, editions II (2026-07-24) + III (2026-08-08) | Primary (shipped game data) |
| L1 | `agentic_orchestration/legolas/notes/2026-07-28-gd-gdc-save-probe.md` — the lane map this lap executed | Internal |
| L2 | `agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2b-energy-release.md` | Internal |
| L3 | `agentic_orchestration/galadriel/pipeline/eor_cooldown.py:114` — slot geometry | Internal |

---

The boat came. The far shore was mapped a month ago and the crossing was short — but the shore had moved, and the thing that carried across was not the map of the rooms; it was knowing which door each one opens onto.
