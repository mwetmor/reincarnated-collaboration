# Research — EoR Warlord endgame build-of-record, GD Stash construction protocol, endgame difficulty axis — 2026-08-01

**Mode:** A (analytical + primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** knight-rider, relaying Matt's ENDGAME-FIRST ruling for the C2 `gd-eor-warlord` playtest
**Access:** read-only. Web = Crate Entertainment forum (Discourse `/raw/` + `/t/*.json`; `/t/` is robots-allowed), GitHub API, ModDB/Nexus (both 403'd — see § 6). **grimtools.com was NOT fetched** — its `robots.txt` disallows `ClaudeBot`/`Claude-User`. Every grimtools URL below is a link **for Matt to click**, never a page I read.
**Local:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` via `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`
**Scripts:** `agentic_orchestration/legolas/scratch/2026-08-01-eor-endgame/` — `q_diff.py`, `q_diff2.py`, `q_diff3.py`, `q_diff4.py`, `q_diff5.py`, `q_sot.py`, plus fetched forum sources (`t*.txt`, `*.json`)
**Discipline:** R-BR-34 — every claim below names its evidence. Anything I could not evidence is stamped **UNVERIFIED** and is not asserted.

---

## SUMMARY

1. **Build-of-record: `https://www.grimtools.com/calc/b28gD0KN`** — the *final tested* Gutsmasher EoR Warlord from Top-20-SC #2 (banana_peel + mad_lee). The published link `a2E7zk3Z` is superseded by the author's own edit.
2. **A tested savefile exists and is downloadable — this beats every construction method.** `https://forums.crateentertainment.com/uploads/short-url/wu1LwqaU4vrKY0CtVhxCUnwj1Vu.zip` (HTTP 200, `application/zip`, 1.2 MB, "Gutsmasher EoR Warlord.zip"). It **is** the `b28gD0KN` character.
3. **Canon-window ruling (material, and it changes the framing):** the Gutsmasher EoR Warlord is **1.1.9.x canon**. It was #2 in the 2022 list, **absent from the 1.2.0.5 list, and absent from the 1.2.1.6 list**. Nery's own 1.2.1.6 verdict: *"the time hasn't been kind to this build."*
4. **v1.3.0.0 reverses the specific decay Nery named.** EoR weapon-damage scaling up (39% / 50% ult rank) + CC-resist while channelling; and **monster armour −17% / armour-absorption −20%, with EoR named in the patch note** as a beneficiary.
5. **Verdict (a) custom game:** GD Stash CAN see custom-game saves (`save\user`) — but **the Crucible CANNOT.** See 7.
6. **Verdict (b) Steam cloud:** must be OFF. Steam → right-click Grim Dawn → Properties → General → Steam Cloud checkbox. Cloud-off root = `Documents\My Games\Grim Dawn\save\`. **Watch for OneDrive hijacking `Documents`.**
7. **THE COLLISION — read this before planning the sitting.** A custom-game (`save\user`) character **cannot enter the Crucible**; Crucible is itself a mod. Workaround, endorsed by GD Stash's author mamba: copy the character folder `save\user\` → `save\main\`, valid *"only for mods that only change some data from vanilla"* — **Matt's empty mod changes nothing, so it qualifies.** Recommendation: build in `save\main\`, keep a `save\user\` copy only if the console is needed.
8. **Verdict (c) vanilla client:** GD Stash is a standalone offline Java desktop app. No injector, no overlay, no in-game component. **Do NOT install Grim Internals or the Rainbow filter** (both are in thread 124405's tool list; both alter the UI the pixel pipeline reads).
9. **Difficulty picks:** Crucible **Gladiator, waves 150–170** (both Top-20 editions use exactly this as the endgame benchmark). SoT: **Ultimate, floor 5**.
10. **Density does NOT vary much by Crucible difficulty; monster HP does.** Measured: `spawnMinAdj`/`spawnMaxAdj` are **zero on all three difficulties**; `characterLifeModifier` at wave 150–170 is **+108→128% (Aspirant) / +218→240% (Challenger) / +304→344% (Gladiator)**.
11. **SoT at Ultimate/L100 is essentially density-invariant:** floor-5 wave-3 goes 24–24 → **24–25 concurrent** (`spawnMax` +1), still **zero champions** (`championChance = 0`), monsters resolve to **level 100–102**. Skeleton Key: `levelRequirement = 0` — no gate at all.

---

## 1 — The build-of-record

### 1.1 Canon window — the finding that shapes everything else

The corpus citation for `gd-eor-warlord` is thread 124405, which is a **leveling/beginner** guide (title: *"[1.1.9.7] SSF Physical Eye of Reckoning Warlord | leveling and beginner build | HC friendly"*, tqFan). Its § "Endgame builds" is a **four-item link list**, not a build. That list is the map:

| # | Endgame build named by 124405 | Author | Thread |
|---|---|---|---|
| 1 | DW by Fordprefect — *"recommended — has very similar devotion"* | fordprefect | [124885](https://forums.crateentertainment.com/t/1-1-9-7-another-dw-warborn-eor-warlord-sr-90ish-ravager-of-minds/124885) |
| 2 | DW by Nery | Nery | [88245](https://forums.crateentertainment.com/t/1-1-4-1-1-1-9-3-physical-spin2win-eor-warlord-150-170-sr-75-viable-no-greens/88245) |
| 3 | 2H by Fordprefect | fordprefect | [113547](https://forums.crateentertainment.com/t/1-1-9-4-gutsmasher-warlord-2h-physical-eor-sr-90-ravager-of-minds/113547) |
| 4 | **2H by banana_peel + mad_lee** ← *the Gutsmasher* | banana_peel + mad_lee | [122229](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) entry #2 |

**Measured canon decay.** I fetched all three editions of the Top-20 Softcore list and grepped each:

| Edition | Thread | Game version | Posted / last-updated | EoR Warlord present? |
|---|---|---|---|---|
| 1st | [122229](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) | 1.1.9.6 (tested on .9.7) | 2022-10-12 / 2023-07-17 | **YES — #2, score 19** |
| 2nd | [136117](https://forums.crateentertainment.com/t/top-20-softcore-builds-ft-hc-approved-section-from-rektbyprotoss-1-2-0-5-an-onion/136117) | 1.2.0.5 | — | **NO** (0 grep hits for `Eye of Reckoning`/`EoR`/`Gutsmasher`; the two Warlords present are #7 Blitz and #11 Markovian) |
| 3rd | [150895](https://forums.crateentertainment.com/t/top-20-softcore-builds-end-of-forgotten-gods-edition-with-hc-section-by-rektbyprotoss-1-2-1-6/150895) | 1.2.1.6 | upd. 2026-03-04 | **NO** (0 grep hits for any of the four tokens across the whole 37.5 KB post) |

And the build's own most-current author says the same thing in his own words. Nery, thread 88245, **Update 1.2.1.6** (post last edited 2025-10-21):

> *"Long time no see! Unfortunately, the time hasn't been kind to this build. Both Physical damage as a whole and EoR skill aren't in good shape. It's a working build, and it's cheap to assemble, but that's all."*

**Ruling.** "Gutsmasher EoR Warlord" is a **1.1.9.x-era canonical build**. That is not a reason to drop it — the corpus `canon_tier=deep` grade and the §C2 scorecard rest on cross-era recognition, and this note's § 1.5 shows v1.3.0.0 reversed the exact decay Nery diagnosed. But **it is a reason not to describe it as "current meta,"** and it is a fact the playtest write-up should carry.

**No FoA-native EoR build exists.** The FoA theorycraft list ([155952](https://forums.crateentertainment.com/t/fangs-of-asterkarn-builds-theorycraft-calcs-list-for-endgame-and-leveling/155952), 62 posts, 2026-07-21) has **zero** Warlord or EoR entries. The Beginner Compendium ([106137](https://forums.crateentertainment.com/t/beginner-build-compendia-for-fangs-of-asterkarn-forgotten-gods/106137), post #2, updated 2026-07-17) carries "Physical | Eye of Reckoning | Warlord | **1.1.9.7**" by tqFan and by The_Coyote — still 1.1.9.7.

### 1.2 Variant table — decision-shaped

All grimtools links are **for Matt to click**; I did not fetch any of them.

| ID | Build | Author | Patch | Weapon | GrimTools | Savefile? | Source |
|---|---|---|---|---|---|:--:|---|
| **V1** | **Gutsmasher EoR Warlord** (Top-20 SC **#2**) | banana_peel + mad_lee | 1.1.9.6/.7 | 2H mace (Gutsmasher) | published [`a2E7zk3Z`](https://www.grimtools.com/calc/a2E7zk3Z) · **final tested** [`b28gD0KN`](https://www.grimtools.com/calc/b28gD0KN) | **YES** | [122229](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) #2 |
| V2 | Gutsmasher Warlord / 2H Physical EoR, SR 90 | fordprefect | 1.1.9.4 | 2H (Gutsmasher) | defensive [`vNQ6A6E2`](https://www.grimtools.com/calc/vNQ6A6E2) · damage [`r2BegeDN`](https://www.grimtools.com/calc/r2BegeDN) | no | [113547](https://forums.crateentertainment.com/t/1-1-9-4-gutsmasher-warlord-2h-physical-eor-sr-90-ravager-of-minds/113547) |
| V3 | Another DW Warborn EoR Warlord, SR 90ish | fordprefect | 1.1.9.7 | dual wield | [`qNY9lPAN`](https://www.grimtools.com/calc/qNY9lPAN) | no | [124885](https://forums.crateentertainment.com/t/1-1-9-7-another-dw-warborn-eor-warlord-sr-90ish-ravager-of-minds/124885) |
| **V4** | Physical Spin2win DW EoR Warlord | **Nery** | **1.2.1.6** ← most patch-current | dual wield | [`RZR6q69Z`](https://www.grimtools.com/calc/RZR6q69Z) | no | [88245](https://forums.crateentertainment.com/t/1-1-4-1-1-1-9-3-physical-spin2win-eor-warlord-150-170-sr-75-viable-no-greens/88245) |
| V5 | Bleeding Whirlwind (Gutsmasher + Bloodrager) | CheeserYT | 1.1.9.7 | 2H, bleed-conversion | [`8NKvwGjZ`](https://www.grimtools.com/calc/8NKvwGjZ) | no | [126179](https://forums.crateentertainment.com/t/1-1-9-7-bleeding-whirlwind-warlord-build-gutsmasher-eye-of-reckoning-bloodrager-set-sr80/126179) |
| V0 | *(context — the corpus citation)* leveling / beginner | tqFan | 1.1.9.7 | DW | leveling [`1NXxEvON`](https://www.grimtools.com/calc/1NXxEvON) · budget [`aZqpYlMV`](https://www.grimtools.com/calc/aZqpYlMV) | no | [124405](https://forums.crateentertainment.com/t/1-1-9-7-ssf-physical-eye-of-reckoning-warlord-leveling-and-beginner-build-hc-friendly/124405) |

### 1.3 Recommendation — **V1, and specifically `b28gD0KN`**

**Why V1 is the build-of-record.** It is the *only* variant that is the thing the corpus row actually names. `gd-eor-warlord` is graded `canon_tier=deep`; the name "Gutsmasher" and the C2 scorecard's *"#2 in the Top-20 Softcore list… the best channelling skill boosted by all the perks of the best dmg type"* is a **direct quote of the 122229 #2 entry**. V2–V5 are the same archetype by other hands; V1 is the record.

**Why `b28gD0KN` and not `a2E7zk3Z`.** The 122229 post carries its own correction, verbatim:

> *"edit: the last version of the build we tested was this: `https://www.grimtools.com/calc/b28gD0KN` — it proved to be a little better. **it is also the one in the savefile**"*

So `b28gD0KN` is simultaneously (i) the final tested spec and (ii) the spec Matt gets for free by unzipping the attachment. Those two agreeing is what makes a **100% match** achievable rather than approximated.

**Named alternatives, so the pick stays Matt's:**

- **Want patch-currency over canon-rank → V4 (Nery, 1.2.1.6, `RZR6q69Z`).** Three years newer, and its author documents what changed (Chains of Anguish belt for +1 all skills and lifesteal; **Oleron's Rage as the exclusive instead of Divine Mandate**, for OA; crafts for slow resistance). Cost: it is **dual-wield, not Gutsmasher** — a different weapon geometry, and it forfeits the name the corpus row carries. Its author grades it *"working… but that's all."*
- **Want a prose-documented gear rationale → V2 (fordprefect, `vNQ6A6E2`).** The only variant whose forum post explains *why* each slot is what it is (§ 1.4). Same 2H Gutsmasher core. One patch older than V1.
- **Do not pick V5 for this playtest.** It converts the build's damage to **bleed** — a DoT profile. That is a different BC-axis signature from the physical-hit channel the C2 scorecard was written against, and it would silently change what the fixture measures.

### 1.4 Gear — what I can and cannot give you

**Hard boundary, stated plainly.** The 122229 #2 entry contains **no prose gear list** — it is a grimtools link, a savefile, and three video links. `grimtools.com/robots.txt` disallows `ClaudeBot` and `Claude-User`, so I did not open the calculator. **V1's exact per-slot gear is therefore not in this note, and I will not reconstruct it from memory.** Matt gets it two ways, both trivial: click `b28gD0KN`, or unzip the savefile and look at the character.

What I *can* give, because it is written in prose in the forum post, is **V2's slot-by-slot rationale** — same weapon, same set core, one patch earlier. From [113547](https://forums.crateentertainment.com/t/1-1-9-4-gutsmasher-warlord-2h-physical-eor-sr-90-ravager-of-minds/113547) § "Gears", verbatim structure:

| Slot / item | fordprefect's stated reason |
|---|---|
| **Gutsmasher** (2H mace) + **3-piece Warborn set** | *"core of the build"* |
| **Sandreaver** gloves | *"BiS for new EoR mods"* |
| **Sigil of the Bear King** (medal) | *"BiS for good stats and attack speed"* |
| **Black Matriarch** (ring — *Mythical Ring of the Black Matriarch*, per reply #18) | *"BiS for RR"* |
| **Deathstalker** (relic) | *"better than Serenity here since CC resist and AS is important… but since it cost you resistances I had to get them from belt prefix"* |
| **Ugdenbog** belt | *"to get missing resistances and defensive ability"* |
| **Windshear** boots | *"can be replaced with many others… craftable boot with phys resist and good stats… proc provides good defense"* |
| **Hellforged** pants | *"used for phys resist mostly. Build lacks it but for more damage you can use Barbaros as well"* |
| **Lifegiver** ring | *"used to get Lifesteal but resistances also fits the setup"* |
| **Azrakaa** amulet | *"to get defense (since build has low phys resist) and slow resist"* |
| Crafts | *"Helmet and Boots crafted with %4 Armor bonus"* |

Two operational notes from the same thread's replies, both of which will bite during construction:

- **Physique requirement.** The chest requires 1035 physique against ~920 on the sheet. Reply #6/#7: *"%12 reduced physique requirement for armor from **Veterancy** skill allows you wear."* If you construct the character stat-by-stat rather than from the savefile, **Veterancy must be allocated before the chest will equip.**
- **Faction choices are near-free.** fordprefect, reply #23: Kymon's vs Death's Vigil — *"Doesn't matter"*; Cult choice — *"Doesn't matter"*; Barrowholm — *"With Barrowholm if you wanna kill Ravager."*

### 1.5 Devotion

**The V1 devotion map is not in prose either** (same grimtools boundary). Two prose sources cover the archetype:

- **fordprefect, V2:** *"Devotions are quite usual **Bear–Ulzaad–Azrakaa** route. You need **Scales** for energy regen and it also helps for defense."*
- **tqFan, 124405 § Devotion** — a full ordered route with respec markers (`-X` = respec from X):

> Blue → **Bull** (bind Forcewave, later EoR) → −Blue → **Assassin** (bind Guardians, later EoR) → **Lion** → Yellow → **Tip of the Scale** (Ulcama proc) → **Wraith** → **Bear** (bind **Maul** to Judgment, or to Vire's Might with Volcanic Stride) → Purple → **Ulzaad's Decree** (proc only; bind Blitz, later War Cry) → **Crab** proc (bind Divine Mandate) → **Stag** → −Bull → **Turtle** → −Yellow → **Solemn Watcher** → −Lion → complete **Crab** → −Wraith → **Hammer** → **Shifting Sands** → Red → **Ghoulish Hunger** → **Jackal** → −Red → **Azrakaa** free node

**Construction gotcha — devotion manipulation.** Multiple readers of 113547 hit this and could not proceed. Replies #12/#14/#15/#17:

> *"I've completed the devotions in the build but I'm not meeting the 8 required yellow affinities to put points into Scale."* → *"You will need to do what's called 'devotion manipulation'. Basically pick one of… 'Panther', 'Scarab' or 'Stag' for those 2 yellow affinities. Add Scales right after and remove the previous one… Then you will have Scales devotion and you can go further investing into… Azrakaa's sands."* → *"You need to go to the **spirit guide** for that, just like for skill points."*

**Consequence for construction: the final devotion state is not reachable by monotonic allocation.** It requires a temporary pick-then-refund. This is the single strongest argument for the savefile path (§ 2.1), which arrives at the terminal state directly.

### 1.6 Skills

The V1 endgame rank allocation is behind the same boundary. The **ordered acquisition list** from 124405 § "Skills order" is prose and is reproduced here because it names every skill the build touches and their relative priority:

max **Eye of Reckoning** early (from ~L14, after 1pt Vire's Might) → 1pt Tectonic Shift → 1pt Guardians of Empyrion → max **Soulfire** → 1pt Presence of Virtue + 1pt Rebuke → max **Divine Mandate** → max **Celestial Presence** → max **Ascension** + 1pt Clarity of Purpose → 1pt Haven, 1pt Resilience → 1pt Volcanic Stride **or** Judgment (whichever procs Maul; *"I initially played VM but switched to Judgment"*) → 1pt Blitz → 12/12 **Fighting Spirit** → 1pt Veterancy → 1pt War Cry (bind Ulzaad's Decree) + 1pt Field Command → 1pt Decorated Soldier → max **Presence of Virtue** → soft-cap **Squad Tactics** + 1pt Blindside → 1pt Scars of Battle + max **Break Morale** → soft-cap **Military Conditioning** → soft-cap **Field Tactics** → 3 and 5 total into Haven / Clarity of Purpose.

Two author-flagged traps in the same section: *"don't put 1p into **Menhir's Will**… **it doesn't work with dual wield**"* (irrelevant for the 2H V1, relevant for V3/V4), and Divine-Mandate-before-Celestial-Presence (*"[MISTAKE, SHOULD HAVE PUT POINTS INTO DIVINE MANDATE DUE TO LOW %DAMAGE]"*).

**A 1.2.1.6-era amendment worth reading.** V4's author accepted a reader change in 88245 (relayed in 124885 #13, 2025-12-17): *"drop **Scars of Battle** by 1 and put this point somewhere else… +1 to **Military Conditioning** for 20k Health."*

### 1.7 Attributes

tqFan, 124405 § "Tips and info", verbatim:

> *"spend leftover Attributes points in **Cunning** (Physique / Spirit just to meet requirements) but left **10 points in the tank** just in case there's suddenly a high requirement to meet"*

The 10-point reserve is the answer to the physique/spirit equip failures reported in 113547 (#7 chest, #18 Black Matriarch ring). **Do not dump the last 10 points.**

### 1.8 Patch-currency delta — v1.3.0.0 / Fangs of Asterkarn

Extracted verbatim from the official patch notes ([155979](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979), 55.5 KB, accessed 2026-08-01):

**Directly buffs this build:**

- *"**Eye of Reckoning**: increased % Weapon damage scaling with rank to 39%, 50% by max ultimate rank. Added % Crowd Control and % Max Crowd Control resist for the caster while channeling the skill, scaling with rank."*
- *"Reduced Monster Armor by 17% on Champion+ enemies and reduced Monster % Armor Absorption by 20% on all enemies. This reduces monster resistance to Physical damage, **particularly for small fast attacks (ex. dual wielding or Eye of Reckoning)**."* ← **this is the patch note that answers Nery's diagnosis by name.**
- *"Reduced Monster % Life Leech Resist on Ultimate difficulty. This makes % Attack damage Converted to Health roughly 16% more effective against an average boss."*
- *"**Soulfire**: increased % Damage Reduction scaling with rank to 20% by rank 12, 30% by max ultimate rank"*
- *"**Judgment**: increased Internal Trauma damage scaling with rank and increased its Duration to 5s"*
- *"**Warborn Bastion Set**: reduced Cooldown on the skill proc"*

**Slight headwinds:**

- *"**Haven**: reduced % Health scaling with rank to 16% by rank 10, 28% by max ultimate rank"*
- *"**Summon Guardian of Empyrion**: reduced Burn damage scaling with rank"*
- *"**Lifegiver Signet**: reduced Health to 270"* (V2's lifesteal ring)
- *"Increased all Boss Health scaling with level, by ~32% at level 100 (~15% for superbosses). **These changes do not apply to the Crucible.**"* ← relevant to the SoT half of the sitting, **not** the Crucible half.

**Not touched:** Gutsmasher, Sandreaver, Sigil of the Bear King, Black Matriarch, Deathstalker, Beronath Reforged, Celestial Presence, Presence of Virtue, Vire's Might, Ascension, Divine Mandate, Oleron's Rage — **zero grep hits** across the whole patch-notes document. The build's core is untouched; the changes are net-positive.

**For V5 only:** *"Bloodrager's Endless Frenzy Set: replaced % Crit damage bonus with 8% Offensive Ability… Increased Bleed damage modifier for Blade Arc to 240 / 3s."*

---

## 2 — Construction protocol, for Matt's hands

### 2.0 Three paths, ranked — and the ranking is the finding

| Path | 100% match? | Patch-current? | Risk | Verdict |
|---|:--:|:--:|---|---|
| **A — drop in the tested savefile** | **exact, by construction** | save is 1.1.9.x; **game upgrades it on load** (see 2.1 caveat) | lowest | **DO THIS** |
| **B — GD Stash 1.8.2g** | approximate (hand-built) | **yes — author-maintained, FoA-current** | low | **adjustment tool + fallback** |
| **C — gd-edit, GrimTools-URL import** | exact *in principle* | **only via 5-day-old community forks** | **elevated** | **do not lead with this** |

Path A wins for a reason specific to this build: **§ 1.5's devotion state is not reachable by monotonic allocation.** Any hand-construction has to reproduce a pick-then-refund sequence. A savefile arrives at the terminal state with no sequence at all.

### 2.1 Path A — savefile drop-in (recommended)

1. **Turn Steam cloud OFF first** (§ 2.5). Do this before anything else touches the save directory.
2. Download **`https://forums.crateentertainment.com/uploads/short-url/wu1LwqaU4vrKY0CtVhxCUnwj1Vu.zip`** — verified reachable 2026-08-01 (HTTP 200, `content-type: application/zip`). This is the "Gutsmasher EoR Warlord.zip" attachment on [122229](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) post #1, and the post states it is the `b28gD0KN` character.
3. **Back up** `Documents\My Games\Grim Dawn\save\` in full before extracting anything.
4. Extract so the character folder (`_Name\` containing `player.gdc`) lands in **`Documents\My Games\Grim Dawn\save\main\`**. `main` — **not** `user`. See § 2.7 for why.
5. Launch GD. The character should appear in the main-campaign list at L100.
6. Use **GD Stash Char Editor** (Path B) only for adjustments — renaming, topping up unspent points, adding a Skeleton Key.

**Caveats, named rather than buried:**

- **Format upgrade is expected but UNVERIFIED by me.** The zip is a 1.1.9.x-era save; the game is 1.3.0.0. GD has historically read forward across save-format versions (GD Stash's own changelog tracks a long chain of format bumps — 1.0.0.5, 1.0.1.0, 1.0.3.0, 1.0.7.0, FG, 1.2.0, 1.2.0.4, 1.2.1.6, **1.3.0.0** — each additive). I did **not** test it. If the character fails to load, fall back to Path B.
- **A respec may be wanted, not needed.** Between 1.1.9.x and 1.3.0.0 the skills listed in § 1.8 changed magnitudes. The build will *work*; whether it is *optimal* is a separate question. If Matt wants the 1.2.1.6-era corrections, apply the two amendments in § 1.6.
- **Achievement side-effect.** medea_fleecestealer, [125121](https://forums.crateentertainment.com/t/how-to-create-authentic-level-100-character-using-gd-stash/125121) #2, on pre-built L100 characters generally: *"keep in mind this has everything maxed, so if you didn't complete those tasks yourself, lvl 100 ultimate, max reputation etc, those steam achievements will be triggered if you use this blank char."* Harmless for our purposes; stated so it isn't a surprise.

### 2.2 Path B — GD Stash 1.8.2g

**Version and currency.** Current release is **1.8.2g**, per the tool author's own OP on [29036](https://forums.crateentertainment.com/t/tool-gd-stash/29036) (author `mamba`, thread opened 2015-07-08, **OP last edited 2026-07-26**, 8,562 posts, author actively answering FoA questions through 2026-07-26). Changelog, verbatim: *"**Version 1.82** — Support for the GD 1.3.0.0 save file formats"*; *"**Version 1.80** — Support for the Fangs of Asterkarn beta file formats."*

**Runtime requirement.** GD Stash *"is written in Java and stores all items in a database."* Changelog v1.01: *"still requires a **64 bit JVM** (due to a bug in Oracle's 32 bit JVM)"*; v1.05a later added *"32bit Java VM supported."* **The exact minimum Java version is UNVERIFIED** — I could not reach ModDB or Nexus (both 403 to agent fetches, § 6). Read the `readme` inside the download. For reference, the sibling tool gd-edit states *"This thing needs **Java 8** to run… be sure to download the **64bit** version for your platform"* ([35817](https://forums.crateentertainment.com/t/tool-gd-save-file-editor/35817) OP) — a current 64-bit JRE will satisfy both.

**Steps.**

1. **Steam cloud OFF** (§ 2.5). Back up `Documents\My Games\Grim Dawn\save\`.
2. Download 1.8.2g from [ModDB](http://www.moddb.com/mods/gd-stash/downloads/gd-stash) or [Nexus mod 2](https://www.nexusmods.com/grimdawn/mods/2/) (both links from the author's OP). Extract anywhere; it is portable.
3. **Config page — three settings, in this order.**
   - **Grim Dawn install directory** → the game folder.
   - **Save location** → `Documents\My Games\Grim Dawn\save`. It does **not** default here. mamba's own troubleshooting (thread [29036](https://forums.crateentertainment.com/t/tool-gd-stash/29036) #8576): a blank stash/character dropdown *"might indicate that it is not finding any shared stash files."* Community guidance is that GD Stash defaults to the Steam cloud path and must be switched manually.
   - **Mod** → leave **empty**. mamba, #8576: *"The second can be empty, no problem there, that just means you have no mods installed."* Matt's mod folder is empty — it ships **no `database.arz`** — so there is nothing for GD Stash to import for it, and **"Total Conversion Mod" must stay unchecked** (that checkbox restricts item lookup to the mod database only).
4. **Import database.** Config page → Import. This decodes `database.arz` into GD Stash's own tables. Re-run this after every GD patch. Warnings during import are expected — mamba, #8574: *"this is 'expected', I get the same warnings and they are irrelevant, which is why they are warnings and not errors."*
5. Press **Reload** to refresh the character/stash dropdowns.
6. **Char Editor tab.** Per the OP feature list, GD Stash supports *"Editing of some character information"*; changelog entries establish specifically: level + XP with auto-adjusted stat/skill points (v1.07: *"When entering the level and pressing &lt;return&gt;, the XP and available stat and skill points are adjusted"*), **devotion skill levels** (v1.04), attribute points (v0.99b), faction reputation (v0.99d), riftgates (v0.99), shrines (v0.99c), Crucible token points (v1.06), full **mastery refund** (v1.26), and dedicated **skill-editing screens** (v1.60). Community how-to: *"select 'Char Editor' tab, pick a character from a list, clear spent skill points with 'X' (it's near class names), rename if you want, save the changes, close the app and start Grim Dawn."*
7. **Items.** Transfer page moves items between GD Stash's database and the character/shared stash; the Crafting page creates items by selecting base item + prefix + suffix. Grant the § 1.4 list here.
8. **Close GD Stash before launching GD.** Changelog v1.29 / v1.44: GD Stash blocks saving cloud characters and editing the shared stash while Grim Dawn is running, specifically to prevent corruption.

**Do NOT use the XP-grant-then-kill-one-mob method as your primary path.** That is the method our prior note cited from thread 125121 — but 125121 is a **bug report about that method failing**, not a how-to. The original poster, verbatim: *"give yourself enough experience points, then start the game again, kill one mob and the game will level the character to the 100 level. And that's happened, HOWEVER, **the character has way less health and energy than it should. Level 100 Warder has like a little more than 8000 health (with all points distributed).**"* Every reply in that thread recommends a *different* method (download a pre-built L100; copy a finished character; use a save editor). **The root cause is UNVERIFIED** — no one in the thread diagnosed it. Correcting our own prior art: `2026-07-28-gd-iconic-build-shortlist.md` § 3 described this method as the accepted path; on reading the source thread in full, it is the method the thread exists to report as broken.

### 2.3 Path C — gd-edit GrimTools import (real, and currently risky)

This is the tool that does *exactly* what "match the build 100%" asks: **Odie has implemented loading GrimTools URLs directly into the save editor**, and it has a `make-char` command that writes a new character.

**Why it is not the recommendation.** Measured on the GitHub API, 2026-08-01:

| Repo | Last push | Stars | Release assets |
|---|---|:--:|---|
| `Odie/gd-edit` (original) | **2024-07-23** | 20 | — |
| `kirijin/gd-edit` (fork) | 2026-07-30 | 0 | `gd-edit-nix.bin` (v0.2.445, **Linux only**) |
| `c0de-v1k1ng/gd-edit-FoA` (fork) | 2026-07-26 | 0 | none |

The original is **two years stale** and does not support 1.3.0.0/FoA. Its author has been publicly absent through cancer treatment since 2024 (thread [35817](https://forums.crateentertainment.com/t/tool-gd-save-file-editor/35817) #1402–#1424). FoA support exists **only** in forks created 2026-07-25/26 — five days old, zero stars, no code review, and the one Windows binary offered in the thread (#1434, `gd-edit 0.2.447 build dbd121f`) is **hosted on LimeWire**, not on GitHub Releases. Thread quotes: c4ph4lor #1430 — *"Supports FoA / 1.3"*; tito.tarantular #1429 — *"vibe-slopped a patch… Import from grimtools links works now"*; #1431 — *"vibe tool revival started)"*.

**Ruling: do not put an unvetted third-party binary next to Matt's save directory when Path A gets the same character with a `.zip` and Path B is author-maintained.** Revisit if a fork consolidates and a reviewed Windows release appears.

**`getgrimdawn.uc.r.appspot.com`** (named in 125121 #5 as the GrimTools→JSON bridge) is **alive** — HTTP 200, 2026-08-01 — but is a JS app I cannot inspect, and per thread [124379](https://forums.crateentertainment.com/t/tool-get-grim-dawn/124379) it has since been narrowed: *"GetGrimDawn is now just a team buffs calculator, as it was originally intended to be."* **Its build-export capability is UNVERIFIED as of today.**

### 2.4 — VERIFICATION POINT (a): custom-game saves

**Verdict: GD Stash can read and edit `save\user` characters. CONFIRMED, with one setting and one caveat.**

- **Path fact (primary, Crate forum [146160](https://forums.crateentertainment.com/t/where-is-my-character-saved-file/146160), 2025-06-24).** Cloud on → `C:\Program Files (x86)\Steam\userdata\<numbers>\219990\remote`. Cloud off → `Documents\My Games\Grim Dawn\save`. Under that root: **`\main\` = main campaign, `\user\` = custom game.** Custom-game characters are a *separate list* with separate stashes.
- **GD Stash reads them.** Author changelog, thread [29036](https://forums.crateentertainment.com/t/tool-gd-stash/29036) OP: v0.99d — *"**Modded chars and stashes are being read.** Only edit them if you know the mods are compatible with the vanilla game as the mods cannot yet be loaded"*; v1.00 — *"Mod support: A mod can now be specified on the config page"*; v1.60 — *"Improved handling for **mods with a custom campaign** (e.g. Reign of Terror)."*
- **The v0.99d caveat is satisfied for us, exactly.** It says only edit modded characters if the mod is vanilla-compatible. **Matt's mod is an empty folder — it ships no `database.arz`, so it is vanilla by construction.** (This is the same property the 2026-07-25 handoff § 4.7 identified: *"an empty mod has no `database.arz`, so there is nothing to override vanilla with. Contamination is impossible by construction."*) The caveat's condition is met at its strongest.
- **Setting to check:** GD Stash's save-location field must point at the save **root**, and the character dropdown must be **Reload**ed. If the dropdown is empty, the location is wrong (this is the single most common failure in the thread).
- **UNVERIFIED residual:** I found **no post that says in so many words "GD Stash lists `save\user` characters."** The finding is built from the author's own changelog. **60-second test for Matt:** open GD Stash, set the save location, hit Reload, and look for the werewolf character (the one that produced `player.gdc` for the G-7 probe) in the Char Editor dropdown. If it is there, verified end-to-end.

**Independent corroboration that the custom-game path produces ordinary saves:** we already parsed one. `2026-07-28-kitcal1-g7-gdc-save-findings.md` decoded a `.gdc` from a `save\user` custom-game session — level, XP, attributes, equipment, and a real vanilla monster kill (`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr`) all read cleanly. The empty-mod custom game plays the vanilla world and writes a standard save. *(One flagged property carries forward: that save's `uid` was 16 zero bytes, and the note explicitly leaves open whether that is a `save\user` property or format-wide.)*

### 2.5 — VERIFICATION POINT (b): Steam cloud save

**Verdict: cloud must be OFF. CONFIRMED.**

- **Where the toggle is:** Steam → right-click **Grim Dawn** in the library → **Properties** → **General** → the Steam Cloud checkbox (*"Keep game saves in the Steam Cloud"*). Turning it off relocates saves to `Documents\My Games\Grim Dawn\save`. *(Widely-reported community instruction; the **path consequence** is independently confirmed by Crate thread [146160](https://forums.crateentertainment.com/t/where-is-my-character-saved-file/146160) #2, which states both paths explicitly. The exact Steam menu label is **UNVERIFIED** — Steam UI strings change and I could not fetch steamcommunity.)*
- **Why it matters, from the tool author.** GD Stash changelog v1.29: *"No longer allows saving of cloud chars while Grim Dawn is running."* v1.44: *"The shared stash cannot be edited while GD is running when using cloud save to prevent corruption."* The failure mode is the cloud overwriting edited local files with an older snapshot.
- **If Matt insists on keeping cloud on** (not recommended): the community workaround is to use the game's own network options to *"download cloud saves,"* edit locally, then *"Delete cloud saves."* Fragile. Don't.
- **⚠ Windows gotcha worth more than it looks.** Crate thread [146160](https://forums.crateentertainment.com/t/where-is-my-character-saved-file/146160) is an entire thread about a missing save folder, and the cause was **OneDrive redirecting `Documents`**: *"if there is no folder at all in my games it's usually a hint that Onedrive has hijacked the folder and it's somewhere in the onedrive subpath."* The reporter eventually reinstalled Windows to fix it. **Before Matt edits anything, have him confirm the real path by searching for his character's folder name — not by assuming `C:\Users\<name>\Documents\`.**

### 2.6 — VERIFICATION POINT (c): the client stays vanilla

**Verdict: GD Stash has no in-game component. CONFIRMED, with a warning attached.**

GD Stash is a **standalone Java desktop application**. The author's own description: *"written in Java and stores all items in a database… It also reads the information from `database.arz` into its own tables."* Its screenshots are a desktop UI (Config / Im-Export / Transfer / Char Editor / Crafting / Collection / Look-and-Feel tabs). It edits files on disk while the game is closed; the changelog's repeated concern is *avoiding* concurrent access with a running GD. **There is no DLL, no injector, no overlay, no launcher wrapper.** The rendering pipeline sees a stock client.

**⚠ The real threat to the pixel pipeline is elsewhere, and it is in a source we were already reading.** Thread [124405](https://forums.crateentertainment.com/t/1-1-9-7-ssf-physical-eye-of-reckoning-warlord-leveling-and-beginner-build-hc-friendly/124405) § "Mods and tools" recommends five tools. Three of them **change what the screen shows**:

| Tool | What it does | Verdict for our capture |
|---|---|---|
| **Grim Internals** | in-game overlay/injector: debuff icons, potion cooldowns, auto-pickup, **fog removal**, fixed time-of-day | **DO NOT INSTALL.** Injects and alters rendering. Also, per its own release note quoted in thread [94315](https://forums.crateentertainment.com/t/crucible-for-mod-character/94315): *"Steam Cloud Save is not functioning properly when you launch Grim Internals!"* |
| **Rainbow Filter** | *"item highlighting… making item stats more readable"* | **DO NOT INSTALL.** Changes tooltip/label colour — directly in the OCR path. |
| **GDAutoCaster** | automates skill casting | **DO NOT INSTALL.** Changes the measured behaviour, not just the pixels. |
| Grim Dawn Item Assistant | external stash app, out-of-process | harmless, but unnecessary |
| YoloMouse | enlarges the cursor | **avoid** — a bigger cursor is more occlusion in frame |

**Also note the build author's own macro habit**, 124405 § Tips: *"I have Blitz, Vire's Might and Medal movement skill macro'ed to 1 button that spams them; same with Ascension, Judgment and War Cry."* If Matt does this, the per-skill `skill_use_count` series stops distinguishing those skills. **Pilot manually, or declare the macro before recording.**

### 2.7 — THE COLLISION: custom game vs the Crucible

**This is the finding most likely to change the plan, so it gets its own section.**

**A custom-game (`save\user`) character cannot enter the Crucible.** Crate forum thread [94315](https://forums.crateentertainment.com/t/crucible-for-mod-character/94315), *"Crucible for Mod character"*:

> ASYLUM101: *"the reasoning for it is that **crucible itself is a 'mod'**, at least in the way the game perceives mods."*

This is consistent with our own datamine finding (`2026-07-25-gd-custom-game-console-unlock.md` § Q2): Crucible is `mods/survivalmode`, loaded via its own hardcoded code path, and **does not appear in the Custom Game list**. Matt's playtest calls for 35 minutes of Crucible. If the character lives in `save\user`, that half of the sitting does not happen.

**The workaround, and its exact validity condition — from GD Stash's own author.** Same thread, the OP proposes the fix and **mamba** qualifies it:

> Darkwave76: *"I can cheat it taking my saved game in **user** directory and **copy into main** + GD Stash"*
> mamba: *"you cannot really do that in most cases, as **mod specific items and masteries get lost** that way, so **the only mods this would work for are ones that only change some data from vanilla GD**, e.g. increase drop rate or mob density."*

**Matt's empty mod changes *no* data — not drop rates, not density, nothing. It has no `database.arz` at all.** It sits at the strict limit of mamba's condition: there are no mod-specific items to lose and no mod-specific masteries to lose. **The `user` → `main` copy is safe for our case specifically.**

**Recommended plan:**

1. Put the character in **`save\main\`**. Both Steps of Torment (main-campaign content) and the Crucible work from there. This is the default and the simplest sitting.
2. **Only if the debug console is needed** for the endgame sitting: keep a *second copy* of the character folder in `save\user\`, run the SoT portion there, and run the Crucible portion from the `save\main\` copy. Two folders, two copies, no conversion step.
3. **Do not** try to run both from one location. There isn't one.

**Decision Matt should make explicitly:** does the endgame sitting need the console at all? The custom-game container was chosen in the 2026-07-25 work to unlock `character.ShowAngerLevels` / `character.LogData` / `game.Spawn` / `character.WarpCursor` for *anger-state* measurement. If this sitting is an OCR-of-PlayStats density/TTK run, `save\main\` alone is sufficient and simpler. **UNVERIFIED by me:** whether the console is required by the current playtest KPI set — that is gandalf's/knight-rider's call, not a research question.

---

## 3 — The endgame difficulty axis

*(Short by instruction. Measured against the Edition-II `.arz`; scripts `q_diff*.py`.)*

### 3.1 Crucible — which difficulty and wave band

**Gladiator, waves 150–170.** Both Top-20 editions state this as the endgame benchmark in their own performance guidelines, verbatim and unchanged across four years:

> *"every build is capable of finishing **Crucible 151-170** within 4:30 in the best run, safely farm it with correct play, finish 151-170 without buffs and banners with safe play"* — [122229](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) (2022) and [150895](https://forums.crateentertainment.com/t/top-20-softcore-builds-end-of-forgotten-gods-edition-with-hc-section-by-rektbyprotoss-1-2-1-6/150895) (2026), identically worded.

Gladiator is the top of three difficulties (Aspirant / Challenger / Gladiator). **v1.3.0.0 made reaching it much cheaper:** *"Unlocking the next Crucible difficulty now also triggers at **Wave 110 and Wave 160**, rather than requiring clearing the Crucible Waves 1-100."*

**Sizing the 35 minutes.** A top-20-grade build clears 150→170 in ~4:30 and the guideline calls ~4:30 a *best* run. 35 minutes buys roughly **4–6 complete 150-170 runs**, or one full 1→170 climb with time to spare. For a fixture, several short 150-170 runs give more engagement segments than one long climb.

### 3.2 Does Crucible density vary by difficulty? — **barely; monster HP does all the work**

Three measured layers, all from the `.arz`:

**(i) `records/game/gameproxies.dbr` — SurvivalMode override**, arrays indexed `[Aspirant/Normal, Challenger/Elite, Gladiator/Ultimate]`:

```
spawnMin         = [0, 0, 1]        spawnMax    = [0, 1, 1]
championMin      = [0, 0, 1]        championMax = [0, 1, 1]
spawnMinModifier = [0, 112, 120]
```

Note the Crucible override is **weaker** than the campaign base (`championMax = [0, 2, 3]`).

**(ii) `records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`** — 200-element arrays, one record per difficulty (selected by `survivalinfo.dbr`'s `survivalAdjustment{Normal,Elite,Ultimate}`). **The spawn-count arrays are entirely zero on all three difficulties:**

| field | Aspirant | Challenger | Gladiator |
|---|---|---|---|
| `spawnMinAdj` | all 0 | all 0 | all 0 |
| `spawnMaxAdj` | all 0 | all 0 | all 0 |
| `spawnChampionMaxAdj` | 0 → **1 at index 68** | 0 → **1 at index 52** | 0 → **1 at index 52** |
| `spawnChampionMinAdj` | 0 → **1 at index 85** | 0 → **1 at index 68** | 0 → **1 at index 68** |

**(iii) The same records' stat modifiers, at indices 150 / 160 / 170:**

| field | Aspirant | Challenger | Gladiator |
|---|---|---|---|
| `characterLifeModifier` | +108 / +118 / **+128%** | +218 / +229 / **+240%** | +304 / +324 / **+344%** |
| `retaliationTotalDamageModifier` | 54 | 53 | **74** |

**Answer:** Crucible difficulty adds **at most +1 common spawn and +1 champion slot per pool**, and the per-wave arrays add **no** common spawns at all. What difficulty actually buys is **monster health — Gladiator monsters have roughly 2.9× the Aspirant bonus at the same wave.** For a density-focused fixture, difficulty is close to a *time-per-kill* dial, not a *monsters-on-screen* dial.

**Two flags, both mine and both honest:**

- **The 200-element axis is INFERRED to be wave number**, not proven. The reasoning: (a) the campaign's analogous `balancingadjustment_mp+difficulty_*` records use **12**-element arrays (player count 1–12), so 200 is not a shared engine convention; (b) `characterLifeModifier` grows monotonically **through and past index 100**, so it cannot be monster-level-indexed (no monster exceeds ~110); (c) decisively, the champion step points **differ by difficulty** (52 vs 68 vs 85) — coherent as "harder difficulties introduce champions earlier in the wave sequence," incoherent as a level threshold. Indices 171–199 appear to be unreachable padding (Crucible caps at 170).
- **Ultimate/Gladiator concurrency cannot be computed from these scalars with confidence.** My own prior note (`2026-08-01-gd-pack-density-ranking.md`) reported *"tier 14 wave 06 becomes roughly 36 min / 47 max"* on Ultimate by applying `spawnMinModifier` to the total and `spawnMax +1` per point. Applying the same operator order to **tier 13 wave 06** (base 35/35 over 5 active points, since `sm1` zeroes p06) yields **min 42 / max 40** — min above max, which is impossible. **The operator order is therefore not established.** Report the base (Aspirant) figures and the *direction* of the Ultimate adjustment; do not report a computed Gladiator concurrency number until the order is settled.

### 3.3 Steps of Torment — Ultimate, level 100

Measured on `records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` and its pool `boss&questpools/p_areab_stepsoftorment_floor5wave3.dbr`:

| Property | Normal | **Ultimate @ L100** | Source |
|---|---|---|---|
| Ambush concurrency cap | `maxGroupSize = 25`, `minGroupSize = 24` | **unchanged, 25** | ambush record |
| Pool spawn | `spawnMin = spawnMax = 24` | **24–25** (`gameproxies.spawnMax = [0,1,1]`) | base `gameproxies.dbr` |
| Champions | `championChance = 0`, `championMin = championMax = 0` | **still zero** — the difficulty's `championMax = [0,2,3]` has nothing to roll against at 0% chance | pool record |
| Refill | `spawnThreshold = 3`, respawn 0.25–0.5 s | unchanged | ambush record |
| Roster | `skeleton_a01` · `_a02_archer` (limit 8) · `_b04_warlock` (limit 2, `alwaysSpawn`) · `_b01_archer` (limit 1, `alwaysSpawn`) · `_b03_priest` (limit 1, `alwaysSpawn`) | **identical — no `minPlayerLevel` on any entry** | pool record |
| Monster level | `lv3_strong` / `lv4_champion` vs `averagePlayerLevel` | **100–102** (`lv3_strong` → 100–101; `lv4_champion` → 101–102) | `records/proxies/lv{3,4}_*.dbr` |

**Answer:** SoT floor-5 wave-3 is **density-invariant and composition-invariant** across difficulty and player level. The only deltas at Ultimate/L100 are **+1 spawn ceiling** and **monster level 100–102** (plus whatever the campaign's Ultimate stat-scaling applies, which is a different record class). The room a L100 character walks into is the same room a L20 character walks into, populated identically. **That is a genuinely good property for a fixture** — the L20 opposition ledger and the L100 run are measuring the same encounter shape.

**Skeleton Key: MEASURED, no gate.** `records/items/crafting/materials/craft_skeletonkey.dbr` — `Class = QuestItem`, `itemClassification = Quest`, `itemLevel = 1`, **`levelRequirement = 0`**. It is also craftable: `records/items/crafting/blueprints/other/craft_special_skeletonkey.dbr` (`Class = ItemArtifactFormula`). Confirmed trivial at 100 — and grantable directly via GD Stash if Matt doesn't want to farm the blueprint.

**One patch-note interaction worth carrying to the playtest doc:** *"Increased all Boss Health scaling with level, by ~32% at level 100… **These changes do not apply to the Crucible.**"* So the SoT half of the sitting runs against post-buff boss HP and the Crucible half does not. If TTK is compared across the two halves, that asymmetry is a real confound and should be declared, not discovered.

---

## 4 — Corrections to our own prior art

Filed explicitly so the record self-heals rather than accumulating drift.

1. **`2026-07-28-gd-iconic-build-shortlist.md` § 3** presents the GD Stash "grant XP → restart → kill one mob → resolve to L100" flow as *"the accepted endgame-construction path [that] works,"* citing thread 125121. **That thread is a bug report about the method failing** (character ends with ~8k HP at L100), and all four replies recommend other methods. The GD Stash *version* claim in the same section (1.8.2a supports 1.3.0.0 + FoA) **stands and is now upgraded**: current is **1.8.2g**, and the author's changelog splits it as v1.80 = FoA beta formats, v1.82 = 1.3.0.0 save formats.
2. **Same note, § C2** scores canon-fame **5** on the basis of Top-20 #2. That was correct for the source it named (the 2022 list) but **the 2nd and 3rd editions both dropped the build**. § 1.1 above supplies the fuller window. C2's *selection* rationale (channel family, weapon-based isolation, v1.3.0.0 tailwind) is unaffected — but the canon-fame figure should read "5 at 1.1.9.x; unranked at 1.2.0.5 and 1.2.1.6."
3. **`2026-08-01-gd-pack-density-ranking.md`** reported tier-13 wave-06 as *"35 min / 36 max, E = 36.00."* Re-resolving the overlay stack today, spawn point **p06 comes from `sm1` with all five of its pools at `spawnMin = spawnMax = 0`** — i.e. the AoM overlay zeroes that point. Summing the five live points gives **35 / 35**. The difference is aggregation method, not a data disagreement; noting it so the two numbers are not read as a contradiction. The Ultimate-projection arithmetic in that note is separately flagged in § 3.2 above.

---

## 5 — Unverified / open

| # | Item | Why it matters | What closes it |
|---|---|---|---|
| U-1 | **V1's exact per-slot gear, devotion node set, and skill ranks** | the "100% match" requirement | Matt clicks [`b28gD0KN`](https://www.grimtools.com/calc/b28gD0KN), or opens the savefile. **I am blocked by `grimtools.com/robots.txt` and did not fetch it.** |
| U-2 | Whether a 1.1.9.x `.gdc` loads cleanly in 1.3.0.0 | Path A's whole premise | Matt tries it. Path B is the fallback. |
| U-3 | Whether GD Stash's Char Editor dropdown enumerates `save\user` characters | verification point (a) | 60-second test: does the werewolf character appear? |
| U-4 | GD Stash's exact minimum Java version | install step | the `readme` in the download. ModDB + Nexus both 403 agent fetches. |
| U-5 | Exact Steam Cloud checkbox label / menu position in the current Steam client | verification point (b) | Matt looks. The *path consequence* is confirmed either way. |
| U-6 | Whether `getgrimdawn` still exports builds | would make Path C cheap | JS app; not inspectable by fetch. |
| U-7 | Whether the endgame sitting needs the debug console | decides `main` vs `user` (§ 2.7) | gandalf / knight-rider — a scope question, not research |
| U-8 | Crucible **tier index → in-game wave number** mapping | would let the density note's tier figures be quoted as waves | carried unresolved from the density note: the schedule is game script (`gd.survival.tier14Waves.*`), not data. The 20 tiers × 10 waves = 200 slots matching the 200-element balancing arrays is **suggestive but not proof**. |
| U-9 | `spawnMinModifier` operator order (§ 3.2) | blocks any computed Gladiator concurrency figure | a controlled in-game count, or an engine-behaviour source |
| U-10 | Root cause of the 125121 low-HP bug | would rehabilitate the XP-grant method | nobody in that thread diagnosed it |

---

## 6 — Sources

**Primary — official / developer**

| Source | URL | Accessed |
|---|---|---|
| Grim Dawn v1.3.0.0 patch notes (Crate) | https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979 | 2026-08-01 |

**Primary — tool authors (own threads / changelogs)**

| Source | URL | Accessed |
|---|---|---|
| `[Tool] GD Stash` — author `mamba`, OP updated 2026-07-26, v1.8.2g, 8,562 posts | https://forums.crateentertainment.com/t/tool-gd-stash/29036 | 2026-08-01 |
| `[Tool] GD save file editor` — author `Odie`, last post 2026-07-30, 1,435 posts | https://forums.crateentertainment.com/t/tool-gd-save-file-editor/35817 | 2026-08-01 |
| gd-edit docs (Getting Started, FAQ) | https://odie.github.io/gd-edit-docs/ | 2026-08-01 |
| GitHub API — `Odie/gd-edit`, `kirijin/gd-edit`, `c0de-v1k1ng/gd-edit-FoA` | (API) | 2026-08-01 |

**Primary — local datamine (read-only)**

`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — `database/database.arz`, `mods/survivalmode/database/SurvivalMode.arz`, `survivalmode{1,2,3}/database/SurvivalMode{1,2,3}.arz`, via `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`. Records cited: `records/game/gameproxies.dbr`, `records/game/survivalinfo.dbr`, `records/game/balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`, `records/game/balancingadjustment_mp+difficulty_enemies01.dbr`, `records/game/gameengine.dbr`, `records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr`, `records/proxies/boss&questpools/p_areab_stepsoftorment_floor5wave3.dbr`, `records/proxies/lv{3,4}_*.dbr`, `records/proxies/tier{13,14}waves/proxy_w06_p0*a.dbr`, `records/items/crafting/materials/craft_skeletonkey.dbr`, `records/items/crafting/blueprints/other/craft_special_skeletonkey.dbr`.

**Secondary — community canon (authored, attributed, maintained)**

| Source | URL | Accessed |
|---|---|---|
| Top 20 Softcore builds (1st ed., 1.1.9.6) — banana_peel et al. — **entry #2 = the build-of-record** | https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229 | 2026-08-01 |
| Top 20 Softcore (2nd ed., 1.2.0.5) | https://forums.crateentertainment.com/t/top-20-softcore-builds-ft-hc-approved-section-from-rektbyprotoss-1-2-0-5-an-onion/136117 | 2026-08-01 |
| Top 20 Softcore (3rd ed., 1.2.1.6, upd. 2026-03-04) | https://forums.crateentertainment.com/t/top-20-softcore-builds-end-of-forgotten-gods-edition-with-hc-section-by-rektbyprotoss-1-2-1-6/150895 | 2026-08-01 |
| SSF Physical EoR Warlord — leveling/beginner (tqFan) — *the corpus citation* | https://forums.crateentertainment.com/t/1-1-9-7-ssf-physical-eye-of-reckoning-warlord-leveling-and-beginner-build-hc-friendly/124405 | 2026-08-01 |
| Gutsmasher Warlord 2H Physical EoR SR90 (fordprefect) — **prose gear list** | https://forums.crateentertainment.com/t/1-1-9-4-gutsmasher-warlord-2h-physical-eor-sr-90-ravager-of-minds/113547 | 2026-08-01 |
| Another DW Warborn EoR Warlord (fordprefect) | https://forums.crateentertainment.com/t/1-1-9-7-another-dw-warborn-eor-warlord-sr-90ish-ravager-of-minds/124885 | 2026-08-01 |
| Physical Spin2win DW EoR Warlord (Nery) — **1.2.1.6 update** | https://forums.crateentertainment.com/t/1-1-4-1-1-1-9-3-physical-spin2win-eor-warlord-150-170-sr-75-viable-no-greens/88245 | 2026-08-01 |
| Bleeding Whirlwind Warlord, Gutsmasher/Bloodrager (CheeserYT) | https://forums.crateentertainment.com/t/1-1-9-7-bleeding-whirlwind-warlord-build-gutsmasher-eye-of-reckoning-bloodrager-set-sr80/126179 | 2026-08-01 |
| How to create authentic level 100 character using GD stash? — **a bug report, not a how-to** | https://forums.crateentertainment.com/t/how-to-create-authentic-level-100-character-using-gd-stash/125121 | 2026-08-01 |
| Crucible for Mod character — **the `user`→`main` ruling, from mamba** | https://forums.crateentertainment.com/t/crucible-for-mod-character/94315 | 2026-08-01 |
| Where is my character saved file? — **cloud-on/off paths + OneDrive hijack** | https://forums.crateentertainment.com/t/where-is-my-character-saved-file/146160 | 2026-08-01 |
| Beginner Build Compendia for FoA & FG (post #2 updated 2026-07-17) | https://forums.crateentertainment.com/t/beginner-build-compendia-for-fangs-of-asterkarn-forgotten-gods/106137 | 2026-08-01 |
| Fangs of Asterkarn theorycraft calcs list — **contains no Warlord/EoR entry** | https://forums.crateentertainment.com/t/fangs-of-asterkarn-builds-theorycraft-calcs-list-for-endgame-and-leveling/155952 | 2026-08-01 |
| `[Tool] Get Grim Dawn` | https://forums.crateentertainment.com/t/tool-get-grim-dawn/124379 | 2026-08-01 |

**Artifacts (for Matt to click / download)**

| What | URL |
|---|---|
| **Build-of-record calculator** | https://www.grimtools.com/calc/b28gD0KN |
| Published (superseded) version | https://www.grimtools.com/calc/a2E7zk3Z |
| **Tested savefile** (1.2 MB zip, verified HTTP 200 `application/zip`) | https://forums.crateentertainment.com/uploads/short-url/wu1LwqaU4vrKY0CtVhxCUnwj1Vu.zip |
| GD Stash 1.8.2g | http://www.moddb.com/mods/gd-stash/downloads/gd-stash · https://www.nexusmods.com/grimdawn/mods/2/ |
| Warlord + EoR build browser *(Matt only — robots-blocked to agents)* | https://www.grimtools.com/builds/filter/skill=2616&mastery=warlord |
| All 1.3.0.0-era builds *(Matt only)* | https://www.grimtools.com/builds/version/1.3.0.0 |

**Blocked / not fetched**

- `grimtools.com` — `robots.txt` disallows `ClaudeBot` and `Claude-User`. **Zero pages fetched.** All grimtools URLs above are hand-offs.
- `nexusmods.com` — HTTP 403 to both WebFetch and curl.
- `moddb.com` — HTTP 403 (JS/cookie wall).
- `steamcommunity.com` — WebFetch domain-blocked; one page reached by curl and found non-decisive.
- `forums.crateentertainment.com/search` and `/u/` — robots-disallowed; not used. `/t/` and `/raw/` are allowed and were used throughout.

---

**Signed:** legolas, 2026-08-01. The build is 1.1.9-era canon that the newest patch just handed a weapon back to. The savefile makes the construction question mostly disappear — and the one that remains is not "how do I build it" but "which folder does it live in," because the Crucible will not take a custom-game character. That is the sentence to read twice.
