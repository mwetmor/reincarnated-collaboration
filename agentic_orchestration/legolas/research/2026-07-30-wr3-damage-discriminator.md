# Research — WR3 damage discriminator: were 260.498 / 273.704 Primordian events? — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR, autonomous run WR3-KITE-COMMIT)
**Access mode:** read-only throughout. Writes confined to this note and
`legolas/scratch/2026-07-30-wr3-discriminator/`.

**Companions:**
- `research/2026-07-30-gd-l13-reference-envelope.md` (where 260.498 was first extracted; **its U-5 is
  closed here**)
- `research/2026-07-30-wr3-wave-blizzard-payloads.md` (the ×0.2625 stage)
- `research/2026-07-30-wr3-nova-star-geometry.md` (frigidring rank-5 payload)
- `notes/2026-07-28-kitcal1-g7-gdc-save-findings.md` (the `.gdc` parse)

**Grading key:** **M** = MEASURED (read verbatim from `.arz` / `.gdc` / `Game.dll`) ·
**D** = DERIVED (computed; operator stated) · **E** = bounded ESTIMATE · **U** = UNRESOLVED.

---

## VERDICT

**Three verdicts, and the third is the one that decides the fork.**

### V1 — `lastHitBy` 273.704 is **NOT-PRIMORDIAN**. Firm.

The save format *does* store which entity last hit the player, and it is not Primordian.
`play_stats.perDifficulty[0].lastMonsterHitBy = 'tagEnemyZombieG01'` → **Plague Walker**
(`records/creatures/enemies/zombie_g01.dbr`, `monsterClassification = Common` — a trash zombie) (**M**).
The companion field `lastMonsterHit = 'tagEnemyZombieSoldierA01'` → **Rotting Soldier**, also trash
(**M**). The save was written mid-trash-pack, not in the boss arena.

### V2 — `greatestDamageReceived` 260.498 is **UNRESOLVED, and structurally unresolvable from this save.**

`greatestDamageReceived` is a **bare float with no companion attribution field anywhere in the block**
(**M**, verified against the byte offsets and against `Game.dll`'s own symbol table). Its scope is
**lifetime-of-character, not per-session and not per-encounter** — it is the maximum over the
character's entire history: `playTime` 7,096 s, `kills` 882, `deaths` 2, **`hitsReceived` 500** (**M**).
The Primordian fight is a small minority of those 500 receipt events. No second save exists to diff.
**Exact attribution is impossible.** Bounds are given in §3.

### V3 — **the fork does not turn on attribution, and the commission's stated inference is wrong.**

The commission's third bullet reads: *"If 260.498 / 273.704 were NOT Primordian events … the
constraint dissolves and the mechanical case for S2_FULL stands unopposed."*

**It does not dissolve. It generalises, and it gets stronger.**

The `armorbase0N` outgoing damper is **not a Primordian property**. It is carried by **1,221 of 1,307
Monster records — 93.4 %** (**M**, established in the payloads note and re-confirmed here), and the
**trash-tier records carry it too**: `armorbase01/02` run `offensiveTotalDamageModifier = −56 + rank`
(**M**, newly extracted here — the envelope note had only ever read these records' *life* modifier).
So under S2_FULL *every* candidate source is damped — trash to ×0.4875, champion/hero/boss to
×0.2475–0.2775. Re-attributing the hit away from Primordian moves it from one damped bucket into
another damped bucket.

**Under S2_FULL, nothing the referent character could have met can deliver 260.498 post-mitigation.**
Sweeping all 1,307 base-campaign creature records reachable at player level 13, composing each
monster's best ability at its own resolved `charLevel` and rank, and applying the player's measured
mitigation, the **S2_FULL ceiling is 234.5**. Granting S2 a deliberately unfair best case — the
8 %-chance +35 % physical proc **and** a fabricated +80 raw weapon on **every** entry, and admitting
charLevel-21 heroes a level-13 Act-1 character plausibly never met — lifts it only to **252.9**,
still **2.9 % short** of 260.498 and 7.6 % short of 273.704.

| regime | best-case reachable ceiling (post-mitigation) | 260.498 | 273.704 |
|---|---|---|---|
| S0_NONE | **894.6** | REACHABLE | REACHABLE |
| S1_PAK | **670.9** | REACHABLE | REACHABLE |
| **S2_FULL** | **252.9** | **UNREACHABLE** | **UNREACHABLE** |

**Net: S1_PAK is favoured and S2_FULL is disfavoured — but the margin at the ceiling is 2.9 %, not a
landslide, and §4 names a live hypothesis under which neither number discriminates at all.**

---

## 1. Evidence chain — the save format

### 1.1 What `play_stats` actually contains, and what it does not

Parsed from `player.gdc` (SHA-256 `0be3a99f…ee91`), block version **12**, via G-7's parser. Every
value **M**:

| field | value | attribution field? |
|---|---|---|
| `playTime` | 7,096 s | — |
| `deaths` | 2 | — |
| `kills` | 882 | — |
| `hitsReceived` | **500** | — |
| `hitsInflicted` | 1,606 | — |
| `criticalHitsReceived` | **0** | — |
| `greatestDamageInflicted` | 1,093.807 | — |
| `perDifficulty[0].greatestMonsterKilledName` | `tagSlithBossB02` → **Primordian** | **YES (string)** |
| `perDifficulty[0].greatestMonsterKilledLifeAndMana` | 15,822 | **YES** |
| `perDifficulty[0].lastMonsterHit` | `tagEnemyZombieSoldierA01` → **Rotting Soldier** | **YES (string)** |
| `perDifficulty[0].lastMonsterHitBy` | `tagEnemyZombieG01` → **Plague Walker** | **YES (string)** |
| `championKills` | 7 | — |
| `lastHit` | 312.888 | **NO** |
| `lastHitBy` | **273.704** | **NO** |
| `greatestDamageReceived` | **260.498** | **NO** |
| `heroKills` | 3 | — |
| `bossKills` | [0, 0, 0] | — |

**The asymmetry is the finding.** The format keeps entity *names* inside the per-difficulty struct and
damage *magnitudes* outside it. Only the "last" pair has a name at all; **"greatest" has a name only
for the monster the player killed, never for the monster that hit the player.**

`criticalHitsReceived = 0` (**M**) removes one candidate inflator outright: **260.498 was not a
critical hit.**

### 1.2 The field layout is anchored on both sides — the offsets are not in doubt

Field offsets `0x3b79 / 0x3b7d / 0x3b81` for the three floats, `0x3b85` for `heroKills` (**M**). The
parse **closes cleanly to the block end**: immediately after these fields it reads `bossKills`, four
survival counters, then a length-prefixed vector that resolves to two valid record paths
(`records/skills/playerclass10/werewolf1.dbr`, `…werewolf1_skill02_charge.dbr`) and terminates with a
4-byte zero tail (**M**). Any offset error upstream would garble those string reads. Two further
anchors: `lastHit` 312.888 matches the independently derived Feral Claws ≈ 310 (1 %), and
`greatestDamageInflicted` 1,093.807 matches derived Rip and Tear ≈ 820–1,070.

### 1.3 …but the *labels* on two of them are community convention, not engine truth

`Game.dll` string-table sweep (**M**): `greatestDamageReceived`, `greatestDamageInflicted`,
`numHitsReceived`, `criticalHitsReceived`, `numberOfChampionKills`, `numberOfHeroKills`,
`greatestMonsterKilledName/Level/LifeAndMana` all appear as engine-exposed names. **`lastHit` and
`lastHitBy` appear nowhere in the binary.** Those two labels come from community reverse-engineering
of the save format and carry no first-party backing.

This matters because the measured values **violate an invariant that must hold** if the labels are
right: `greatestDamageReceived` (260.498) **<** `lastHitBy` (273.704). A lifetime maximum cannot be
smaller than a member of the set it maximises over. Three readings survive:

| reading | consequence |
|---|---|
| **(A) labels correct, fields aggregate differently** | one of them is not a single impact — see §4, and §2.2 shows this is *forced* |
| **(B) the 2nd/3rd float labels are swapped** | invariant restored; **`greatestDamageReceived` = 273.704 and the Plague-Walker-attributed last hit = 260.498** |
| **(C) write-cadence lag** | precedent exists in this very block: `maxLevel` reads **12** while `character_bio.level` is **13** (**M**, G-7 §6) |

**Reading (B) is the only one that is self-consistent on its face — and note what it does: it hands
the commission's headline number, 260.498, a positive attribution to a Plague Walker.** I do not
adopt (B) as fact; I report that the fork's headline number is, under the one internally consistent
reading, *named as a trash-zombie event*.

### 1.4 One encounter-history datum, robust under either ranking rule

`greatestMonsterKilled` = Primordian at `lifeAndMana` 15,822, and `warden01.dbr` is
`monsterClassification = 'Quest'` — **the same class as Primordian** (**M**). So `bossKills = 0` proves
nothing about the Warden (Quest kills do not increment it; Primordian was killed and the counter is
still 0). But `greatestMonsterKilled` does: Warden phase 2 (`dp_wardenphase2`, pool **20,940**,
charLevel 19–20) exceeds Primordian on **both** pool and level, so under either ranking rule it would
have displaced Primordian had it died. **Warden Krieg phase 2 was never killed by this character.**
Phase 1 (pool 15,569 < 15,822) could have died without displacing — the fight may have been started
and lost or abandoned. Deaths = 2.

---

## 2. Evidence chain — the arithmetic

### 2.1 The mitigation model reconciles the conductor's own figure to the decimal

Extracted from the equipped set (**M**, per-item, `d7_mitigation.py`): `defensiveProtection` **337**
(+8 % modifier), `defensiveCold` **14**, `defensiveAether` **18**, `defensivePoison` **25**,
`defensiveChaos` **8**, `defensiveLife` **8**, `defensiveBleeding` **10**. **No fire or lightning
resistance at all.**

Applying armor at 70 % absorption on physical (armor 337 exceeds every physical component in range)
and the flat resistances elsewhere:

```
primordian_frigidring r5, far band (r >= 9.0 u, x1.4), S1_PAK:
  physical  148 x 0.75 x 0.30  =  33.30
  cold      247 x 0.75 x 0.86  = 159.31
  sum 192.61  x 1.4            = 269.66
```

**269.66 — the conductor's handed figure, matched exactly** (`d8_final.py` header check). This
independently validates three things at once: the mitigation model, the rank-5 frigidring payload
(148 / 247) from the star note, and the fact that these figures are being compared **post-mitigation**,
which is the correct basis for `greatestDamageReceived`.

### 2.2 Inverse arithmetic — what raw payload each regime needs

| target | regime | trash (armorbase01/02, cl 13, ×0.4875) | boss (armorbase03–06, cl 18, ×0.2625) |
|---|---|---|---|
| 260.498 | S0_NONE | 260.5 raw | 260.5 raw |
| 260.498 | S1_PAK | 347.3 raw | 347.3 raw |
| **260.498** | **S2_FULL** | **534.4 raw** | **992.4 raw** |
| **273.704** | **S2_FULL** | **561.4 raw** | **1,042.7 raw** |

*(Pre-mitigation. Post-mitigation the required raw rises further — the numbers above are floors.)*

For scale: the **entire** `nonplayerskills` corpus at ranks 1–6 has exactly **one** record above
1,042 raw that is not the `mogdrogen_lightning` scripted outlier — `ilgorr_icedoubleclaw` at 1,038 —
and Ilgorr is Act-4 / Ultimate content. **Primordian's whole kit tops out at 425 raw** (`primordian_wave`);
the frigidring prong is 395 raw. **Warden's tops out at 692 raw** (`aethersmash_warden` r5).

### 2.3 The reachable ceiling, swept properly

`d8_final.py` / `d9_s2best.py`: every `records/creatures/enemies/` Monster record whose `charLevel`
formula resolves to ≤ 21 at player level 13, best ability taken at that monster's own resolved rank,
composed under each regime with the §2.1 mitigation and the far-band ×1.4 where a ring/nova exists.

**S2_FULL best case, ranked by S2, with the +35 % physical proc and +80 raw weapon granted to every
entry:**

| S2 | S1 | S0 | class | cL | AB | monster ← ability |
|---|---|---|---|---|---|---|
| **252.9** | 346.5 | 462.0 | Hero | 21 | 2 | `reanimator_lab02` ← `electrified_lightningnova` r6 |
| 248.3 | 670.9 | 894.6 | Boss | 20 | 5 | `nemesis_aetherial_01` ← `valdaran_lightningorbnova` r6 |
| 240.3 | 353.4 | 471.2 | Champion | 16 | 2 | `payingtribute_silas_01` ← `outlaw_grenade` r5 |
| 220.9 | 311.2 | 414.9 | Hero | 19 | 2 | `slith_h08` ← `primordian_frigidring` r5 |
| 212.9 | 313.0 | 417.4 | Hero | 16 | 2 | `dc_bounty06 / dc_bounty15` ← `outlaw_aetherslam_01` r5 |

The two entries that clear 240 under S2 both depend on the player having **zero lightning and zero
fire resistance** (which is measured — §2.1) *and* on late-Act content. The genuinely Act-1,
level-13-plausible sources sit at **≤ 213 under S2**.

Primordian's own numbers under the same model, for the record:

| ability | raw | S0 | S1 | **S2** |
|---|---|---|---|---|
| `primordian_frigidring` far band (×1.4) | 395 | 359.5 | **269.66** | **94.4** |
| `primordian_wave` | 425 | 279.9 | 209.9 | 73.5 |
| `chillbane_blizzard` per drop | 213 | — | — | 55.9 |
| `aethersmash_warden` (ph.2) | 692 | 387.5 | 290.6 | 104.6 |

### 2.4 U-5 is closed: `lastHitBy` **cannot** be a single Plague Walker impact

Plague Walker's instantaneous payload is `damagebase_physical01` r13 = **68–85 raw physical, and
nothing else** (**M**). Its three named abilities — `zombie_barf`, `poisongib_zombie`, `acidpool1` —
carry **`offensivePoisonMin` only** (148 / 133 / 89 at rank 4) with **zero instantaneous damage of any
type** (**M**). They are pure DoT.

| reading | S0_NONE | S1_PAK | S2_FULL |
|---|---|---|---|
| single impact, 85 raw phys, +35 % proc, post-armor | 34.4 (**8.0× short**) | 25.8 (10.6× short) | 16.8 (16.3× short) |
| aggregated poison, 370 raw, post 25 % poison resist | **277.5 (+1.4 %)** | 208.1 (−24 %) | 135.3 (−51 %) |

**The single-impact reading fails by 8–16× under every regime, including the undamped S0.** So
whatever `lastHitBy` measures, **it is not one impact.** The aggregated-poison reading lands within
1.4 % of 273.704 under S0_NONE — I report that as a **coincidence-grade fit and explicitly not as
evidence for S0** (it ignores the pak's −38 % DoT modifier, which would drop it to 172, and the
resist value is a base-record affix rather than a verified roll).

This closes the envelope note's **U-5**: the field aggregates. The direction the envelope guessed
("most likely the field aggregates a poison total") is confirmed by the negative — the impact reading
is arithmetically dead.

---

## 3. Bounding the unattributable — what *could* have produced ~260–274

Per the commission's fallback instruction. Candidate classes for a lifetime-max receipt event on this
character, with what each does to the fork:

| candidate | S0 | S1 | S2 | notes |
|---|---|---|---|---|
| **Primordian frigidring, far band** | 359.5 | **269.66** | 94.4 | S1 sits **3.5 % above** 260.498 — the dodged-far-band lower bound the commission described. Best single fit in the corpus. |
| Warden ph.2 `aethersmash` | 387.5 | 290.6 | 104.6 | requires having fought the Warden; §1.4 says ph.2 was never *killed*, which does not preclude being hit |
| Act-1 outlaw hero (`dc_bounty06/15`, `outlaw_aetherslam_01`) | 417.4 | 313.0 | 212.9 | Devil's Crossing bounty content, level-13 plausible |
| Act-1 outlaw champion (`payingtribute_silas_01`, `outlaw_grenade`) | 471.2 | 353.4 | 240.3 | fire component lands **unresisted** |
| `electrified_lightningnova` hero (`harpy_brokenhills_01`) | 394.8 | 296.1 | 201.3 | lightning lands **unresisted** |
| ordinary trash melee (Plague Walker class) | ≤ 34 | ≤ 26 | ≤ 17 | excluded by two orders of magnitude |
| a trap / environmental hazard | — | — | — | **would bypass the monster damper entirely and constrain nothing** — see §4, U-3 |

**Under S1_PAK the field of candidates is wide and unremarkable** — 260.498 sits at ~39 % of the S1
ceiling, an ordinary bad moment in a 500-hit career with 2 deaths.
**Under S2_FULL there are no candidates at all** — 260.498 sits *above* the best case.

---

## 4. What this does to S1 vs S2

**Ruling: S1_PAK favoured; S2_FULL disfavoured. The attribution question turns out not to be the
lever — the roster-wide reach of the damper is.**

1. **The commission's "if not Primordian, the constraint dissolves" premise is falsified.** The
   damper is on 93.4 % of Monster records including the trash tier. Re-attribution relocates the
   problem, it does not remove it. **This is the single most important line in this note.**
2. **S2_FULL cannot produce either measured number from any reachable source**, even when granted a
   deliberately unfair best case. Shortfall **2.9 %** against 260.498, **7.6 %** against 273.704.
3. **S1_PAK produces both comfortably**, and produces the specific 3.5 %-margin far-band-nova fit at
   269.66 that motivated the fork in the first place — which I have now independently reproduced to
   the decimal from the record payloads and the measured gear.
4. **But the margin is 2.9 %, not a landslide.** I decline to call S2_FULL *falsified*. It is
   *disfavoured on the best evidence available*, and the levers that could flip it are named in §5.
5. **And the whole discriminator may be structurally incapable of discriminating.** §2.4 proves
   `lastHitBy` is not a single impact. If `greatestDamageReceived` shares that semantics — and it sits
   three fields away in a block whose labels are community convention (§1.3) — then it bounds an
   *aggregate*, not an event, and it constrains no single-event ceiling under any regime. **This is
   the largest live threat to the fork and it is not closed.** Recommend the conductor treat the
   S1-vs-S2 ruling as resting primarily on §2.3's ceiling sweep (which is regime arithmetic and does
   not depend on save-field semantics at all) rather than on the 260.498 datum itself.

**One correction the conductor should absorb:** the commission's "under S2_FULL … the entire-kit
single-event ceiling is ~283" does not reproduce here. Primordian's S2 kit ceiling is **94.4**
(frigidring far band) and the *whole reachable roster's* S2 ceiling is **252.9**. If 283 came from
summing simultaneous events it is not comparable to `greatestDamageReceived`, which is a per-event
maximum. Likewise the commission's "~107 worst nova prong" is the **100 %-band** figure (mine: 103.7
pre-mitigation); the far band is the governing case.

---

## 5. Unknowns — flagged, not guessed

| # | item | what would close it |
|---|---|---|
| **U-1** | **Whether `lastHitBy` / `greatestDamageReceived` are correctly labelled, or swapped (§1.3 reading B).** The invariant is violated as labelled. Under the swap, 260.498 becomes the Plague-Walker-attributed last hit — a direct NOT-PRIMORDIAN verdict on the headline number. | A second `.gdc` from any character, diffed. **Cheapest highest-value follow-on by a wide margin.** |
| **U-2** | **Whether either float measures a single event or an aggregate.** §2.4 proves `lastHitBy` is an aggregate. `greatestDamageReceived`'s semantics are untested. If it aggregates, it constrains nothing. | Same: a second save, or a controlled single-hit observation. |
| **U-3** | **Trap / environmental / hazard damage bypasses the monster damper.** 127 trap-named skill records carry instantaneous damage; `trap_floorspikes` is 449 raw Pierce and the player has **no pierce resistance**. If 260.498 was a trap, it is regime-neutral and the whole discriminator is void. | Determine whether GD applies `armorbase`-class dampers to non-Monster damage sources. Not resolved here. |
| **U-4** | **Resistance rolls.** §2.1 uses base-record affix values, not the character's actual rolled magnitudes. The 269.66 reconciliation validates cold = 14 and armor = 70 % specifically; the other resists are unvalidated. | Resolve the affix rolls from the item seeds in `parsed.json`. |
| **U-5** | **Spawn reachability of the two entries that top the S2 table.** `reanimator_lab02` (cl 21) and `nemesis_aetherial_01` are almost certainly *not* reachable by a level-13 Act-1 character; excluding them drops the S2 ceiling to **240.3** and widens the shortfall to 7.8 %. I left them in to be maximally fair to S2. Their proxies returned no `records/proxies/` references in the sweep. | Walk the region/level proxy chains for these records. |
| **U-6** | **`greatestMonsterKilledLevel = 13`** while the envelope's spawn chain resolves Primordian to charLevel **18**. Either the field is the *player's* level at kill, or the charLevel-18 derivation is wrong. The HP anchor (15,822 vs 15,891 predicted at cl 18) strongly favours cl 18 and thus the player-level reading — but it is untested. Would move the S2 boss factor if wrong. | `play_stats` v12 field-semantics reference. |
| **U-7** | Carried forward from the envelope: **weapon-wielder damage floors** (U-2 there). `gear_warden_mace.dbr` was **not found** in any of the four `.arz` pins under that name. §2.3 substitutes a generous +80 raw allowance. | Walk the `lootRightHandItem` master tables. |

---

## 6. Source list

**Primary — game corpus** (read-only, `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`):
`database/database.arz` · `gdx1|gdx2|gdx3/database/GDX*.arz`.
Newly read for this note:
`records/skills/nonplayerskills/passive/{armorbase01…armorbase06, damage_totaladjuster, damagebase_physical01}.dbr` ·
`records/skills/nonplayerskills/path/{zombie_barf, slith_festeringwave}.dbr` ·
`records/skills/nonplayerskills/attackprojectile/poisongib_zombie.dbr` ·
`records/skills/nonplayerskills/aoe/acidpool1.dbr` ·
`records/skills/nonplayerskills/bossskills/{outlaw_aetherslam_01, outlaw_grenade, ilgorr_icedoubleclaw, loghorrean_chomp}.dbr` ·
`records/skills/nonplayerskills/heroskills/archetypes/electrified_lightningnova.dbr` ·
`records/creatures/enemies/zombie_g01.dbr` · `records/creatures/enemies/boss&quest/{warden01, slith_wightmirecave01, payingtribute_silas_01, reanimator_lab02}.dbr` ·
`records/creatures/enemies/bounties/{dc_bounty06, dc_bounty15}.dbr` ·
plus a full sweep of all `records/creatures/enemies/` Monster records and all
`records/skills/nonplayerskills/` skill records.

**Primary — fixture save:** `player.gdc`, SHA-256 `0be3a99f6ead980210a5c06cd12a09bfe51235c09b9da7d41745fa4eacd5ee91`,
via G-7's parse artifacts (`scratch/2026-07-28-gdc-parse-g7/{parsed.json, gdc_parse.py, gear_named.json}`).

**Primary — binary symbol table:** `/Users/admin/Games/vendor/grim-dawn/Game.dll` (string extraction only;
used to establish which play-stat field names are engine-native and which are community convention).

**Scratch artifacts:** `agentic_orchestration/legolas/scratch/2026-07-30-wr3-discriminator/`
(`d1_armorbase.py` · `d2_roster.py` · `d3_ceiling.py` · `d4_pw_traps.py` · `d5_trashceiling.py` ·
`d6_refine.py` · `d7_mitigation.py` · `d8_final.py` — carries the 269.66 reconciliation check ·
`d9_s2best.py` · `d10_pw.py`).

**No tertiary sources used.** No web access was required for this note.

---

## 7. Handoff

**To gandalf (RUN-CONDUCTOR).** In priority order:

1. **Adopt S1_PAK; do not treat S2_FULL as falsified.** The case is a 2.9 % ceiling shortfall, not a
   contradiction.
2. **Discard the "if not Primordian, S2 stands unopposed" branch of the fork.** It rests on a premise
   that is false — the damper is roster-wide (§V3). This is the finding that most changes what
   happens next.
3. **Rest the ruling on §2.3's ceiling sweep, not on 260.498 itself.** The sweep is regime arithmetic
   over the corpus and is independent of save-field semantics; the 260.498 datum is hostage to U-1,
   U-2 and U-3.
4. **`lastHitBy` is closed as NOT-PRIMORDIAN and as NOT-A-SINGLE-IMPACT** (§2.4). The envelope note's
   U-5 can be retired and replaced with the aggregate finding.
5. **One cheap, high-value follow-on:** a second `.gdc` from any character would close U-1 and U-2
   together. Everything ambiguous in this note traces to having exactly one save.

**To jack-ryan**, if ratified: this note **closes envelope U-5** and **corrects envelope §2**, which
read `armorbase01/02`'s *life* modifier but never its *offensive* modifier — a stage that was
therefore missing from every trash-tier damage figure in the L13 ledger.

**No canonical doc amended by this note.**

---

**Signed:** legolas (UNKNOWN-RESEARCHER), 2026-07-30.
