# Research — D2 as primary engine join key: Q1 verification surface / Q2 edition hygiene / Q3 harvest cost — 2026-07-27

**Mode:** A (analytical, READ-ONLY)
**Commissioner:** gandalf (ELICITOR), for a Matt ruling: Grim Dawn vs Diablo 2 as PRIMARY calibration join key
**Access date:** 2026-07-27 (all web fetches; failures reported inline)
**Scope discipline:** three bounded questions only. No scope expansion. No DB writes. No writes outside this notes directory.

---

## Summary

**Q1 — CONFIRMED NEGATIVE, with one qualification that matters.** D2R has no native behavioral-verification
surface: no kill counter, no per-skill use counts, no damage/healing totals, no session play_time readable
from video. Blizzard has never shipped one and has never replied to the standing player request. The two
routes to manufacturing one are (a) a Windows-only, single-build, memory-scanning overlay (7 stars, created
May 2026), and (b) a data-file mod recipe that is documented as **melee-kills-only** and is a legacy-D2 forum
recipe never verified on D2R. Both are instruments *we would have to build and then trust*, and (b) mutates
the very data files being calibrated. There is no open-source D2 oracle mature enough to substitute:
`pydiablo` is 5 stars / last push 2019-11-09, `OpenDiablo2` is **archived** (2021), and GitHub search for D2
damage calculators returns nothing above 3 stars. Best available evidence grade from a sim-vs-compendium
path is **DERIVED-UNWITNESSED** — strictly weaker than the MEASURED grade the GD lane already produced.

**Q2 — MUCH BETTER THAN ASSUMED, and the drift is asymmetric.** A live, actively-maintained community mirror
of **current** D2R CASC `.txt` data exists as JSON (`blizzhackers/d2data`, 111 stars, last push 2026-05-25,
commit message *"Updated for newest patch."*). No CASC extraction is required at all — it is a `curl` away.
I diffed it against our local 1.13 set: **114 of 209 common player skills (54.5%) moved on damage/cost/synergy
fields**, but only **21 of 733 common monster rows (2.9%)** moved, and those are almost entirely Druid summons
and mercenaries. The numerator moved; the denominator did not. Effort to reach D2R-edition parity: **hours,
not days.**

**Q3 — D2 WINS DECISIVELY, and by a larger margin than expected.** Maxroll's d2planner exposes an **open,
unauthenticated REST JSON API** — `https://planners.maxroll.gg/profiles/d2/<id>` — returning the complete
exact-numeric build: skill IDs → point allocation, stat allocation, level, difficulty, full item list with
resolved stat names, merc, quests. The skill keys **are Skills.txt `Id` values** and the item stat keys **are
ItemStatCost.txt stat names**, so the payload byte-joins to substrate we already hold. Grimtools `/calc/`
by contrast returns a 33 KB JS shell with zero build data at any probed endpoint.

**The genuine surprise:** D2R is not a frozen classic. It shipped an **eighth playable class (Warlock, patch
3.0 "Reign of the Warlock")** — the first new class since 2001 — and is on an active 2026 balance cadence
(3.1.2 April 2026, 3.2 PTR April 2026). The `charclass` enum in the current data is `ama/sor/nec/pal/bar/dru/ass/**war**`.

---

## Q1 — Behavioral-verification surface

### 1a. Native in-game counters — **ABSENT**

**No total kill count.** Blizzard forum thread *"Can we have total kill count and stuff?"*
(https://us.forums.blizzard.com/en/d2r/t/can-we-have-total-kill-count-and-stuff/2235, accessed 2026-07-27).
Verbatim player statement on current state:

> "anything is more than what we currently have - nothing."

Players note the feature regressed from the franchise's own history:

> "That feature was present in Diablo 1"

**No Blizzard reply exists in the thread.** Requested-but-absent metrics enumerated by players: champion /
elite / boss kills, total monster kills, gold and chests opened, PvP statistics.

**No damage numbers.** D2R ships no floating combat text and no toggle for it. Pro Game Guides
(https://progameguides.com/diablo-ii-resurrected/can-you-turn-on-damage-numbers-in-diablo-ii-resurrected-floating-text/,
accessed 2026-07-27):

> "The remastered version of Diablo 2 does not feature damage numbers as an option for players to either turn
> on or off how they wish."

Three separate long-running Blizzard forum feature requests corroborate the absence
(`/turn-on-damage-numbers/35178`, `/option-to-show-damage-numbers/158950`, `/i-want-damage-numbers-on-screen/95302`).

**What D2 *does* count, and why it is useless to us.** The engine tracks per-monster-type kills to unlock the
monster info tooltip — resistances shown at 15 kills, hit points at 30. This is a per-*type* knowledge gate,
not a displayed running counter, and it is not a session ledger. It yields no kills-total, no per-skill use
count, no healed total, no play_time.

**Contrast to the GD lane (per `gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md`):** GD's native
panel yielded `kills`, `deaths`, `play_time`, `life_healed`, and **per-skill use counts**
(`claws / charge / weaponattack / onslaught`) — 13,633 samples at 0.5 s, zero gaps, **every series closing
exactly on independently human-read totals** (882 kills, 74 weaponattack, 54 onslaught, 358 claws, 175 charge,
12468.06 healed). That closure is the thing D2 structurally cannot offer, because the numbers do not exist to
be read.

**Additional hard blocker:** **D2R has no macOS client.** Blizzard support article
https://us.support.blizzard.com/en/article/284798 lists Windows 10 only. Community reporting
(macresearch.org, accessed 2026-07-27) describes CrossOver as "shaky ... triggered by a Rosetta 2 bug."
Our host is Mac.

### 1b. Mod surface — instrumentation is *possible*, but it is DIY, melee-only as documented, and unverified on D2R

**Official posture.** Blizzard supports offline/private-game mods and has explicitly shut down mods it deemed
security risks (D2ROffline, D2RModding — dsogaming.com, accessed 2026-07-27). TCP/IP was removed at launch.
Practical read: mods are **offline single-player only**.

**Toolchain maturity is real.** `olegbl/d2rmm` (D2RMM mod manager) — 175 stars, last push **2026-07-26**.
Notably its README documents a Mac path:

> "## macOS Support (arm64 only, experimental)
> **Note:** macOS support is experimental and not officially supported. Things may not work as expected.
> Pre-built releases are available (.dmg) for Apple Silicon Macs (M1/M2/M3/M4). Intel Macs are not currently
> supported.
> Since Diablo II: Resurrected has no native MacOS version, you'll need to run the game using external tools
> (e.g. CrossOver). Launch D2R with the run options: `-mod D2RMM -txt`"

**Can a mod add a kill counter? Yes in principle — with a documented fatal caveat.** Phrozen Keep thread
*"Saving User made stats (Kill counter example)"* (https://d2mods.info/forum/viewtopic.php?t=19942, accessed
2026-07-27) gives a pure data-file recipe, no ASM/DLL:

- `itemstatcost.txt` — an unused entry `< 255` with `Saved = 1`, `Send Bits = 32`, `CSvBits = 32`, creating a
  savefile-persistent global stat. Verbatim: *"Use an 'unused' entry that's less than 255. This will create a
  'global' stat that can be saved with the characters stats."*
- `skills.txt` — a skill using function 65 (prayer function) to increment
- item property `skill_on_kill` to fire on monster death
- display via `op = 2` + `descfunc = 3`

The killing caveat, verbatim from the thread:

> "kills with my spells didn't appear on the counter! Only melee Dmg is working."

**I verified the mechanism survives into current D2R.** The `kill-skill` property code (the `skill_on_kill`
carrier) is present in **both** our local 1.13 `Properties.txt` and current D2R `properties.json`. So the hook
exists. But two independent problems remain:

1. **Melee-only, per the only documented recipe.** Our corpus is caster-heavy. A counter that cannot see
   spell kills cannot verify a Blizzard sorc, a hammerdin, or a trapsin.
2. **No free stat slots are visibly available.** I checked: **0 rows** with a blank `Stat` field in either
   1.13 (359 rows) or current D2R (368 rows) `itemstatcost`. The recipe's "unused entry" is a 2000s-era
   assumption; whether headroom still exists in D2R 3.x is **UNVERIFIED** and would need a slot-by-slot audit.

**The epistemic objection is the decisive one, and it is not a cost objection.** A mod-built counter is *our
own instrument*, not the game's accounting. It changes the game's `.txt` files — the exact files we are
calibrating against — so the observation contaminates the observed. GD's panel is Crate's own ledger of its
own engine, which is why the GD run could close two independent read paths on one number. A self-authored
counter has one path and no oracle behind it.

**Memory-reading overlay path — real, and unusable for us.** `Fr4nsson/D2RDamageNumbers` (GitHub, accessed
2026-07-27): **7 stars, created 2026-05-15, last push 2026-05-16, C++, Windows-only.** Repo description:

> "a Windows overlay for Diablo II: Resurrected that displays floating damage numbers above monsters and an
> optional DPS readout. It watches monster HP drops from the running game process..."

Its own warnings, verbatim:

> "The project is intended for local experimentation and modding research. It reads game process memory, so
> use it at your own risk."
> "Multiplayer use is at the user's own risk."

Pinned to a single build — `D2R.exe file/product version 3.0.92198` — with the note that *"Other launchers,
editions, regions, multiplayer modes, or game builds may use different memory layouts."* It does log to
`D2RDamageNumbers.log`. **Assessment:** 2-day-old project, one contributor, Windows-only, offset-fragile
against a game patching quarterly, and on the wrong OS. Not a lane.

**Bot-framework path.** `blizzhackers/kolbot` (d2bs + kolbot) — 291 stars, last push **2026-07-27** (today),
JavaScript. This is the most *capable* instrumentation surface in the D2 ecosystem: full scripted game state.
But it targets **legacy D2 LoD 1.13/1.14 via DLL injection**, not D2R, it is a botting framework (Battle.net
ToS violation; ban surface), and it would put us on the 1.13 edition we are trying to move *off*. The D2R
equivalent, `dulingzhi/koolo` (Go), is **10 stars, last push 2023-11-27** — effectively dormant.

### 1c. Oracle maturity — can sim-vs-formula-compendium substitute? **Not at closure grade.**

| Candidate | Stars | Last push | Status |
|---|---|---|---|
| `youbetterdont/pydiablo` | **5** | **2019-11-09** | Dead. PyPI page: *"currently has an accurate monster stats parser and the beginnings of a weapon speed calculator"* / *"The library is still in early stages."* |
| `OpenDiablo2/OpenDiablo2` | 11,075 | 2021-10-21 | **ARCHIVED.** Engine reimplementation, never a balance oracle. |
| `Doudline/pd2-damage-calculator` | 3 | 2024-10-16 | Project Diablo 2 **mod**-specific, not vanilla/D2R |
| `finpingvin/pd2-map-dmg-calculator` | 2 | 2025-11-30 | PD2 mod-specific |
| `jamiethorpe/d2calc` | 1 | 2023-02-11 | Skill point calculator, not a DPS oracle |
| `pastelmind/d2txt` | 7 | 2022-12-08 | TXT↔INI converter only (parser, not oracle) |

GitHub API searches run 2026-07-27 for `diablo 2 damage calculator`, `d2r damage calculator`,
`diablo2 dps calculator`, `d2 skill calculator`: **nothing above 3 stars, and the two above 2 are both
mod-specific.** This directly corroborates the existing coverage matrix's E-grade for D2
(`datamine-coverage-matrix-2026-07-21.md`): *"no single open-source tool computes arbitrary build DPS from
the raw tables end-to-end; requires assembly."*

**Formula compendium status.** The prose compendia are real and good — Maxroll
(https://maxroll.gg/d2/resources/damage-calculation, *"Updated to Patch 2.6"* Feb 2023, reformatted Feb 2026;
gives the layered order *"Base Weapon Damage → Ethereal bonus → Enhanced Damage (On Weapon) → +xx Min/Max →
Damage +xx → +xx% Damage (Off Weapon) → Critical Hit doubling → Elemental additions → Skill Damage modifiers
→ Conversions → Source Penalties → Unit Modifier"*), Phrozen Keep's Xeno/Kingpin Formulae Guide
(d2mods.info/forum/kb/viewarticle?a=371), PureDiablo's Facts & Formulae archive. **FETCH FAILURE, reported
honestly:** targeted searches for a document titled *"Diablo II Formula Compendium"* by Ruvanal returned
nothing across two query formulations. I could not locate it and will not substitute recollection for it.
The Ruvanal-lineage material appears to survive as the Phrozen Keep and PureDiablo archives rather than as a
retrievable single artifact.

**Evidence-grade verdict.** A D2 verification lane would be: raw `.txt` → hand-implemented formula chain →
predicted TTK → compared against *what?* There is no observed-play measurement to compare it to. The loop
does not close; it only checks our arithmetic against a wiki's arithmetic. Per the GD verdict's own standard
— *"Two methods, one number, no shared failure mode"* — a D2 sim path has **one method and no independent
number.** Grade ceiling: **DERIVED-UNWITNESSED**. The GD lane already delivered **MEASURED**.

---

## Q2 — D2R edition hygiene

### 2a. Extraction — **no CASC work needed; a maintained JSON mirror of current D2R data exists**

`blizzhackers/d2data` — **111 stars, last push 2026-05-25, actively maintained.** README, verbatim:

> "# Diablo 2 Data Files
> These files are the data from the .txt files from the d2r casc, as well as a couple of helpful extra files."

Recent commit log (`gh api repos/blizzhackers/d2data/commits`, accessed 2026-07-27):

```
2026-05-23  Bumped version
2026-05-23  Updated to handle desecrated and non-desecrated conditions.
2026-05-23  Updated headers.
2026-05-23  Updated for newest patch.
2026-03-07  Tweaked population numbers again.
```

**112 JSON files** under `json/`, covering the full table set we hold in 1.13 TSV and more:
`skills.json` (482 KB), `monstats.json` (1.4 MB), `monstats2.json`, `monlvl.json`, `monai.json`,
`levels.json` (292 KB), `missiles.json` (517 KB), `itemstatcost.json`, `properties.json`, `uniqueitems.json`,
`setitems.json`, `runes.json`, `magicprefix.json`, `magicsuffix.json`, `treasureclassex.json`,
`allstrings-eng.json`, plus D2R-era additions absent from 1.13 — notably **`desecratedzones.json`** (108 KB;
Terror Zones, a 2.5+ feature) and `monpopulationest.json`.

Fetch verified: `curl https://raw.githubusercontent.com/blizzhackers/d2data/master/json/skills.json`
→ **HTTP 200, 481,917 bytes.** No auth, no tooling, no Windows, no game install.

**If a first-party extraction were ever wanted anyway:** the Mac-viable primitive is
`ladislav-zezula/CascLib` (483 stars, **last push 2026-07-21**, cross-platform C++) — which is exactly what
D2RMM vendors (`yarn build:casclib`) to ship its arm64 macOS build. CascView/CascExplorer are the Windows
GUI route (per d2mods.info KB a477 and diabloclone.org). But given the mirror, **extraction is not on the
critical path.**

### 2b. Empirical 1.13 → D2R drift — I measured it rather than reading patch notes

Method: parsed local `d2/raw/Skills.txt` (357 named rows, fabd/diablo2 commit `45112569…`) and current
`blizzhackers/d2data/json/skills.json` (428 named rows), joined on the `skill` name string, compared ~60
damage / cost / synergy / to-hit fields. Whitespace, `''`↔`0`, and JSON quote-wrapping normalized out.

**Schema drift first (must be handled before any value diff is trusted):**

| Change | Detail |
|---|---|
| Column count | 1.13 = **256** cols → D2R union = **292** keys |
| `delay` **renamed/split** | 1.13 `delay` → D2R **`localdelay`** + `globaldelay`. Verified: Blizzard `delay=45` → `localdelay=45`; Frozen Orb 25→25; Meteor 30→30; Fire Wall 35→35. **A naive diff reports these as "cast delay removed" — they are not.** |
| Param slots | `Param1-8` → **`Param1-12`** |
| Calc slots | `calc1-4` → **`calc1-10`**; `passivecalc` extended to 14 |
| ID column | `Id` → **`*Id`** (asterisk = comment column in D2 txt convention; `lineNumber` added) |
| Dropped from 1.13 | `reqstr/reqdex/reqint/reqvit`, `skpoints`, `general`, `checkfunc`, `passiveevent(func)`, `auratgtevent(func)` |

**Roster drift:** 72 rows exist in D2R that do not exist in 1.13. One row (`Sword Mastery`) was renamed away.
**30 of the 72 are a whole new class** (see 2b-note below). Others are new monster/uber skills
(`Korlic's Bash`, `Madawc's Lightning Pierce`, `Talic's Whirlwind`, `Goatman Frenzy`, `UberAncientsHeal`,
`MonHolyFire/Freeze/Shock`) and UI pseudo-skills (`TownPortal`, `SwapWeapons`, `EmoteWheel`, `ShowItems`, `Loot`).

**Player-skill value drift (artifact-filtered):**

| Class | Skills changed / 30 |
|---|---|
| Assassin | **21** |
| Druid | **20** |
| Amazon | **18** |
| Barbarian | **17** |
| Sorceress | **15** |
| Paladin | **12** |
| Necromancer | **11** |
| **Total** | **114 / 209 common player skills = 54.5 %** |

Most-changed fields: `Param8` (39 skills — the synergy coefficient), `Param1` (37), `Param2` (35),
`calc1` (34), `Param3` (24), `EDmgSymPerCalc` (17 — the synergy *formula string*), `EMinLev1-5` (13–15 each).

**Worked examples — verbatim field deltas:**

```
Fire Ball          EMin/EMax/EMinLev1-5/EMaxLev1-5/mana/Param8/HitShift  ALL IDENTICAL
                   only:  Param1 '' -> 4    calc1 '' -> 'par1'
Lightning Sentry   EDmgSymPerCalc "(skill('Shock Field'.blvl) + skill('Charged Bolt Sentry'.blvl)
                                    + skill('Death Sentry'.blvl))*par8"
                                -> "(skill('Shock Field'.blvl) + skill('Charged Bolt Sentry'.blvl))*par8"
                   Param8  12 -> 18                       [synergy list shrank, coefficient +50%]
Charged Strike     EDmgSymPerCalc lost skill('Lightning Fury'.blvl);  Param8  10 -> 14
Holy Bolt          EDmgSymPerCalc lost skill('Blessed Hammer'.blvl);  Param7  15 -> 20
Nova               mana 15 -> 13;  EDmgSymPerCalc '' -> "(skill('Static Field'.blvl))*par8";  Param8 '' -> 5
Venom              Param2  100 -> 300
Whirlwind          Param1 -50 -> 30;  Param2 8 -> 5;  ToHit '' -> 50
Fury               Param2 100 -> 70;  LevToHit 7 -> 10
Blade Fury         DmgSymPerCalc '' -> "(skill('Blade Sentinel'.blvl)+skill('Blade Shield'.blvl))*par8"
                   Param8 '' -> 10;  ToHitCalc '' -> 'lvl*10'
Bone Spear         Param8  7 -> 8
Raise Skeletal Mage Param2  7 -> 10
Chain Lightning    calc1 'ln34 / 5' -> 'ln34/par5'
Hurricane          localdelay  150 -> (none)              [cast delay genuinely REMOVED]
Blizzard / Frozen Orb / Meteor / Fire Wall   delay preserved via localdelay — NO change
```

This matches the qualitative patch record: 2.4 (2022-04-14, Ladder S1) was a synergy-and-underused-skill pass
across **all seven** classes — Amazon synergies added to Guided Arrow / Strafe / Multiple Shot; Barbarian
Berserk's Shout synergy swapped to Battle Orders; Sorceress cold armors and the lightning tree reworked;
Assassin trap scaling; Druid physical/elemental; Necromancer mages and golems; Paladin auras and Thorns
(maxroll.gg/d2/news/d2r-patch-2-4-final-patch-notes; icy-veins.com/d2/patch-2-4-compendium-for-diablo-ii-resurrected).
2.5 added Terror Zones and Sunder Charms (immunity-breaking — a build-viability shift, not a table shift).

**Monster-side drift — nearly nil, and this is the important asymmetry.** Same method against
`MonStats.txt` (734 rows) vs `monstats.json` (751 rows), comparing HP / AC / damage / resists per difficulty,
`Velocity`, `Run`, `aidel`, `aidist`, `aip1`, `MinGrp`, `MaxGrp`, `Exp`:

> **21 of 733 common monster rows changed = 2.9 %.**

And the changed rows are overwhelmingly **not hostile monsters** — they are player summons and hirelings:

```
spiritwolf    minHP  60 -> 130   maxHP  82 -> 130     [Druid summon buff, 2.4]
fenris        minHP  98 -> 216   maxHP 130 -> 216
druidhawk     minHP  20 -> 26    maxHP  32 -> 26
bloodgolem    A1MinD  6 -> 7     A1MaxD 16 -> 20
roguehire / act2hire / act3hire   aip1 changed
bladecreeper  Velocity 10 -> 12  Run 10 -> 12
```

**Reading:** the monster substrate — the *denominator* of any TTK calibration — is effectively frozen
1.13 → D2R 3.x. The *numerator* (player skill output) moved on half the roster. That is a favorable shape:
it means our existing `MonStats` / `MonLvl` / `Levels` work does **not** need redoing, and only the skill
table does.

### 2b-note — the finding I did not expect: **D2R has an eighth class**

`charclass` enum in current `skills.json`: `ama, sor, nec, pal, bar, dru, ass, **war**` — 30 skills each.

The `war` (Warlock) skill list:
`Summon Goatman, Demonic Mastery, Death Mark, Summon Tainted, Summon Defiler, Blood Oath, Engorge, Blood Boil,
Consume, Bind Demon, Levitate, Eldritch Blast, Hex Bane, Hex Siphon, Psychic Ward, Echoing Strike, Hex Purge,
Blade Warp, Cleave, Mirrored Blades, Sigil Lethargy, Ring of Fire, Miasma Bolt, Sigil Rancor, Enhanced Entropy,
Flame Wave, Miasma Chains, Sigil Death, Apocalypse, Abyss`

Corroborated externally: *"The Warlock is the eighth playable class in Diablo II and the first new class added
since the original Lord of Destruction expansion in 2001"* — patch 3.0, "Reign of the Warlock"
(diablobytes.com/d2-resurrected/news/patch-notes-3-0/; nintendoeverything.com, accessed 2026-07-27). Blizzard
News PTR 3.2 (news.blizzard.com/article/24266710, accessed 2026-07-27) documents an **April 2026** balance
pass across three Warlock subclass trees (Demon / Chaos / Eldritch) plus a Sunder Charm drop-rate change:

> "we have increased the chances for both to address this, while still keeping the charms rarer than
> pre-Reign of the Warlock drop rates."

Steam patch 3.1.2 dated **April 1, 2026**. Maxroll's guide index already carries five Warlock build guides
(`abyss-warlock-build-guide`, `blood-boil-warlock-guide`, `echoing-strike-warlock-guide`, `fire-warlock-guide`,
`abyss-warlock-leveling-build-guide`).

**Consequence for the ruling.** The premise "D2 is the stable classic reference" is **false as of 2026**.
D2R is on an active seasonal cadence (Season 14 at time of writing) with live class additions and quarterly
rebalance. Pinning an edition is therefore *mandatory*, not optional — exactly as it was for GD.

### 2c. Effort to reach D2R-edition-pinned parity with the GD lane

| Step | Cost | Note |
|---|---|---|
| Fetch current D2R JSON (112 files, ~15 MB) | **minutes** | `curl` / `git clone`; no auth, no tooling, no Windows, no game install |
| Freeze provenance (commit SHA + per-file SHA-256, mirroring GD Edition-I discipline) | **~1 h** | our 1.13 set is already pinned to fabd commit `45112569…` in `d2/MANIFEST.md`; same pattern |
| Write a schema-drift adapter (`delay`→`localdelay`, `Id`→`*Id`, Param 8→12, calc 4→10) | **~2 h** | fully enumerated above; small and closed |
| Re-derive the 114 changed player skills | **~half day** | mechanical once the adapter exists |
| Re-anchor the 294 `kit_numeric` rows off rankedboost (1.13-era, post-formula) onto edition-pinned raw | **~1 day** | this is pre-existing debt, not new — see `2026-07-23-join-surface-probe.md` §2a and Gap 1 |
| Decide Warlock posture (in-corpus vs out) | **a ruling, not an effort** | not currently in our 60 kits |

**Total to edition parity on the data side: on the order of two days.** This is genuinely cheap — cheaper
than the GD `.arz` probe was. **It buys nothing on Q1.** Edition hygiene is a solved problem for D2; the
verification surface is the unsolved one, and no amount of Q2 work touches it.

---

## Q3 — Corpus harvest cost: D2 vs GD

### 3a. Maxroll d2planner — **open REST JSON API, exact-numeric, joins to substrate we already hold**

Discovery path (all read-only, 2026-07-27): `curl` on `https://maxroll.gg/d2/d2planner/ev0106nb` (HTTP 200,
178,504 bytes) surfaced, inside the server-rendered page JSON:

```
"apiUrl":"https://backend.maxroll.gg","userBackendUrl":"https://planners.maxroll.gg"
```

and a `"d2planner-by-id"` key containing the **full build payload inline in the SSR HTML**. Probing the
backend directly:

| Endpoint | Result |
|---|---|
| `https://planners.maxroll.gg/profiles/d2/ev0106nb` | **HTTP 200, `application/json`, 19,614 bytes** |
| `https://planners.maxroll.gg/profiles/ev0106nb` | 404 (`Route GET:/profiles/ev0106nb not found`) |
| `https://planners.maxroll.gg/d2/ev0106nb` | 404 |
| `https://backend.maxroll.gg/d2planner-by-id/…` | 302 (nginx) |

No auth. No token. No JS. No rate-limit encountered on 4 sequential fetches.

**Payload anatomy** (`data` is a JSON string; two schema versions observed — v1 with top-level
`profiles`/`items`, v2 nested under `planner`; both trivially handled):

```
top:      id, date, name, class, data, userId, public, folder, accessed, mainset,
          category, game, average_rating, total_ratings, metadata, season, shared, type, tags, user
data:     profiles[], items{}, activeProfile, buffs, summons, active, name, class   (v1)
          planner{items, profiles, activeProfile, buffs, summons, pinnedStats}      (v2)
profile:  name, skills, stats, inventory, cube, class, level, items,
          merc, mercLevel, mercItems, difficulty, weaponSet, quests
```

Verbatim from `ev0106nb`:

```json
"skills": {"36":1,"37":1,"39":5,"42":1,"43":1,"44":1,"45":1,"47":5,"48":1,
           "52":1,"54":1,"55":1,"59":1,"61":20,"62":20,"64":20,"65":20}
"stats":  {"str":80,"dex":0,"int":0,"vit":380}
"level":  90,  "difficulty": 2,  "mercLevel": 87
```

**The skill keys are `Skills.txt` `Id` values.** Resolved against our local raw file:

```
36 Fire Bolt(sor)   37 Warmth   39 Ice Bolt   42 Static Field  43 Telekinesis
44 Frost Nova       45 Ice Blast 47 Fire Ball  48 Nova          52 Enchant
54 Teleport         55 Glacial Spike  59 Blizzard  61 Fire Mastery
62 Hydra            64 Frozen Orb     65 Cold Mastery
```

**Items resolve just as cleanly.** Verbatim item entry:

```json
"1": {"base":"uap","quality":6,"ilvl":99,"unique":"unique248","defense":141,"sockets":1,
      "socketedItems":[33],
      "stats":{"item_allskills":2,"item_hp_perlevel":12,"item_mana_perlevel":12,
               "item_magicbonus":50,"damageresist":10,"strength":2,"dexterity":2,
               "vitality":2,"energy":2}}
"3": {"base":"uit","quality":7,"unique":"runeword155","sockets":4,
      "socketedItems":["r07","r10","r09","r11"],
      "stats":{"item_fastergethitrate":55,"maxmana":112,"armorclass_vs_missile":250,
               "vitality":22,"item_fastercastrate":35,"item_absorbmagic":8,"item_allskills":2}}
```

`base` codes (`uap`, `uit`, `xea`, `obf`, `xhm`, `ci0`) → `Armor.txt` / `Weapons.txt` `code` column.
`unique248` / `runeword155` / `set104` → `UniqueItems.txt` / `Runes.txt` / `SetItems.txt` indices.
Magic-affix refs (`mp575`, `mp330`, `ms175`, `ms286`) → `MagicPrefix.txt` / `MagicSuffix.txt`.
**`stats` keys are `ItemStatCost.txt` stat names** (`item_fastercastrate`, `item_magicbonus`,
`passive_cold_mastery`, `item_addclassskills#1`). Every one of those tables is already in
`d2/raw/`. **No name-bridge is needed anywhere in this chain.**

### 3b. Volume available

`https://maxroll.gg/d2/category/guides` (HTTP 200, 510,022 bytes) → **68 unique curated build-guide slugs**
(`blizzard-sorceress`, `blessed-hammer-paladin`, `bone-spear-necromancer`, `frozen-orb-sorceress`,
`fire-claws-druid`, `dragon-talon-assassin`, `frenzy-barbarian`, `exploding-arrow-amazon`, … plus 5 Warlock).
Each guide page SSR-embeds its planner IDs: the Blizzard Sorceress guide (626,675 bytes) yielded **3 distinct
planner IDs** (`28a5d0op`, `gx0106gp`, `tq77b0oa` — starter / budget / endgame variants), all three
resolving HTTP 200 against the API (44–49 KB each; `gx0106gp` = *"2.4 Blizzard Sorceress Guide"*, class `sor`,
level 99, 15 skills, **93 items**).

**Order-of-magnitude: ~68 guides × ~3 variants ≈ 200 exact-numeric, edition-tagged, fully-itemized build
payloads, each one `curl` away.** That is 3× our current 60-kit D2 corpus, at exact-numeric grade, against a
current corpus with 294 `kit_numeric` rows total across all D2 kits.

**One honest failure to report:** I could not find a bulk *listing* endpoint for community-submitted builds.
`/profiles/d2` → 404, `/community/d2` → 404, `/profiles/d2/community` → `{"error":"Profile not found"}`,
`backend.maxroll.gg/api/planners/d2` → 302. The `community-builds` page is client-rendered and its listing
API was not visible in SSR HTML. **Consequence:** ID discovery for the long tail of user builds is unsolved;
the *curated guide* corpus (~200) is fully solved by scraping guide pages for IDs. Given that curated guides
are precisely the "community canon builds" the commission names, this gap does not bind.

### 3c. Grimtools — the contrast

`https://www.grimtools.com/calc/w26lp5wV` → **HTTP 200, 33,193 bytes.** The response is a JS shell:
`<title>Grim Dawn Build Calculator</title>`, zero build data, zero `__NEXT_DATA__`, zero embedded JSON, no
`b64`/`build_data`/`loadBuild` markers. `/calc/load/<id>` and `/calc/get/<id>` return **the same 33 KB shell**
(HTTP 200 — i.e. the path segment is ignored, confirming client-side routing); `/get_build/<id>` → 404. Build
resolution happens in JS after load. This corroborates the prior-art characterisation of grimtools as
JS-rendered and confirms **no unauthenticated JSON endpoint was reachable.**

Compounding it, from `2026-07-23-join-surface-probe.md` §3: GD's `all_skills.js` carries **no English skill
names at all** — skills are opaque `sk<N>` IDs whose `skillDisplayName` is a localization tag
(`tagCompSkillA014Name`). A GD build-corpus join needs an intermediate
`sk<N> → English name → kit_id` bridge that does not yet exist (this is the standing motivation for
`2026-07-26-gd-displayname-bridge.md`).

### 3d. Head-to-head

| Dimension | D2 (Maxroll d2planner) | GD (grimtools calc) |
|---|---|---|
| Build payload transport | **Open REST JSON, unauthenticated** | JS-rendered shell; no reachable endpoint |
| Also SSR-embedded? | **Yes** (`d2planner-by-id` in page HTML) | No |
| Skill identity | **Numeric ID == `Skills.txt` `Id`** | Opaque `sk<N>`; English name absent |
| Item identity | base code / unique index → our TSVs | separate DBR acquisition path |
| Stat vocabulary | **`ItemStatCost.txt` names, pre-resolved** | GD-engine field names, no bridge |
| Name bridge needed | **None** | **Yes, and not yet built** |
| Curated corpus reachable | ~200 payloads from 68 guide pages | requires JS rendering per build |
| Cost per build | one `curl`, ~45 KB | headless browser session |

**D2's community-build corpus is roughly an order of magnitude cheaper to harvest at exact-numeric grade,
and it lands pre-joined to raw tables we already hold.**

---

## Where this leaves the ruling (factual framing only — the call is Matt's)

The two games fail and succeed on *opposite* axes, cleanly:

|  | D2 / D2R | Grim Dawn |
|---|---|---|
| Raw data ground truth | **A** — flat TSV/JSON, mirrored, free, no extraction | **A** — but required a bespoke LZ4/TQIT parser to obtain |
| Edition pinning | **cheap** (~2 days; monster side already frozen) | **done** (Edition-I SHA-256, Edition-II fetched) |
| Build-corpus harvest | **A** — open JSON API, IDs join to raw | **C** — JS-rendered, no name bridge |
| **Behavioral verification (observed play)** | **X — structurally absent** | **A — proven MEASURED, zero-cost, closure-grade** |
| Oracle / calculator | **B→C** — nothing above 3 stars, best sim dead since 2019 | **A** per coverage matrix |
| Runs on our Mac host | **No native client** | (the play-test rig exists and delivered) |

D2 dominates on *substrate acquisition and corpus harvest*. GD dominates on *the ability to check whether the
sim is right*. The question the ruling turns on is which of those the join key is actually **for** — and per
the commission's own framing ("the game whose community builds become the first representative corpus kit
selection, **augmented with game source data**"), both roles are in play at once.

Worth stating plainly: **these are separable.** Nothing observed in this probe prevents GD serving as the
verification join key while D2's planner API is harvested as the corpus-breadth lane. The two lanes touch
different substrate and neither blocks the other. Whether that split is desirable is a design judgment I do
not make.

---

## Knowledge gaps not resolved

1. **`itemstatcost` free-slot headroom in D2R 3.x.** 0 rows with a blank `Stat` field in either edition;
   whether the mod recipe's "unused entry < 255" assumption still holds requires a slot-by-slot audit I did
   not run. Bears only on Q1b, which fails on other grounds anyway.
2. **Whether the melee-only kill-counter limitation is fixable.** The Phrozen Keep thread reports it as a
   `skill_on_kill` trigger limitation and does not resolve it. A `death-skill`-based variant on the *monster*
   side was not investigated.
3. **"Diablo II Formula Compendium" (Ruvanal) — NOT FOUND.** Two search formulations returned nothing. I did
   not substitute recollection. The lineage appears to survive as Phrozen Keep KB a371 (Xeno/Kingpin) and the
   PureDiablo Facts & Formulae archive.
4. **Maxroll community-build listing API — NOT FOUND.** Four endpoint probes 404/302'd; page is
   client-rendered. Curated-guide ID discovery works; long-tail user-build discovery does not.
5. **Whether the `blizzhackers/d2data` mirror is edition-*labelled*.** Commits say "Updated for newest patch"
   but I found no explicit patch-version stamp inside the JSON. Pinning would be by **commit SHA**, not by a
   self-declared game version — a weaker pin than GD's Edition-I SHA-256-of-payload discipline. This should
   be verified before any edition freeze is declared.
6. **D2R under CrossOver on Apple Silicon — not tested.** D2RMM ships an experimental arm64 `.dmg` and
   community reporting cites a Rosetta 2 bug. Whether a video-telemetry rig could even *run* on our host is
   untested; I did not install anything (read-only discipline).
7. **Warlock corpus posture.** 30 new skills, 5 Maxroll guides, zero corpus kits. Not investigated further —
   out of the three bounded questions.

---

## Source list

### Local (read-only)
| Source | Path | Accessed |
|---|---|---|
| D2 1.13 raw TSV (34 files) | `agentic_orchestration/research/datamine-acquisition/d2/raw/` | 2026-07-27 |
| D2 acquisition manifest | `agentic_orchestration/research/datamine-acquisition/d2/MANIFEST.md` | 2026-07-27 |
| Acquisition log (fabd commit `45112569deb9384738ccafe5c24ebbb71f41c7c9`) | `…/ACQUISITION-LOG-2026-07-21.md` | 2026-07-27 |
| Coverage matrix, D2 row + grade key | `agentic_orchestration/research/datamine-coverage-matrix-2026-07-21.md` | 2026-07-27 |
| Join-surface probe §2a, §3, §5 | `agentic_orchestration/legolas/notes/2026-07-23-join-surface-probe.md` | 2026-07-27 |
| GD play-test v1 efficacy verdict | `agentic_orchestration/gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` | 2026-07-27 |
| GD Mac extraction viability | `agentic_orchestration/legolas/notes/2026-07-23-gd-mac-extraction-viability.md` | 2026-07-27 |

### Web — all accessed 2026-07-27
| Source | URL | Result |
|---|---|---|
| Blizzard forum — kill count request | https://us.forums.blizzard.com/en/d2r/t/can-we-have-total-kill-count-and-stuff/2235 | 200 |
| Pro Game Guides — no damage numbers | https://progameguides.com/diablo-ii-resurrected/can-you-turn-on-damage-numbers-in-diablo-ii-resurrected-floating-text/ | 200 (via search) |
| Fr4nsson/D2RDamageNumbers | https://github.com/Fr4nsson/D2RDamageNumbers | 200 · 7★ · pushed 2026-05-16 |
| Phrozen Keep — kill counter recipe | https://d2mods.info/forum/viewtopic.php?t=19942 | 200 |
| Phrozen Keep — D2R modding KB (2021 alpha; inconclusive) | https://d2mods.info/forum/kb/viewarticle?a=477 | 200 |
| Phrozen Keep — Formulae Guide (Xeno/Kingpin) | https://d2mods.info/forum/kb/viewarticle?a=371 | via search |
| olegbl/d2rmm (README, macOS section) | https://github.com/olegbl/d2rmm | 200 · 175★ · pushed 2026-07-26 |
| blizzhackers/kolbot | https://github.com/blizzhackers/kolbot | 200 · 291★ · pushed 2026-07-27 |
| dulingzhi/koolo | https://github.com/dulingzhi/koolo | 200 · 10★ · pushed 2023-11-27 |
| youbetterdont/pydiablo | https://github.com/youbetterdont/pydiablo · https://pypi.org/project/pydiablo/ | 200 · 5★ · pushed 2019-11-09 |
| OpenDiablo2 | https://github.com/OpenDiablo2/OpenDiablo2 | 200 · 11,075★ · **archived** 2021-10-21 |
| ladislav-zezula/CascLib | https://github.com/ladislav-zezula/CascLib | 200 · 483★ · pushed 2026-07-21 |
| **blizzhackers/d2data** | https://github.com/blizzhackers/d2data | 200 · 111★ · pushed 2026-05-25 |
| D2R skills.json | https://raw.githubusercontent.com/blizzhackers/d2data/master/json/skills.json | **200, 481,917 B** |
| D2R monstats.json | https://raw.githubusercontent.com/blizzhackers/d2data/master/json/monstats.json | **200, 1,434,371 B** |
| D2R properties.json / itemstatcost.json | same host, `/json/` | 200 |
| Maxroll d2planner (example build) | https://maxroll.gg/d2/d2planner/ev0106nb | **200, 178,504 B** |
| **Maxroll planner API** | https://planners.maxroll.gg/profiles/d2/ev0106nb | **200, application/json, 19,614 B** |
| Maxroll planner API (3 guide builds) | `…/profiles/d2/{28a5d0op,gx0106gp,tq77b0oa}` | 200 · 44–49 KB each |
| Maxroll guides index | https://maxroll.gg/d2/category/guides | **200, 510,022 B** · 68 slugs |
| Maxroll Blizzard Sorceress guide | https://maxroll.gg/d2/guides/blizzard-sorceress | **200, 626,675 B** · 3 planner IDs |
| Maxroll damage calculation | https://maxroll.gg/d2/resources/damage-calculation | 200 · "Updated to Patch 2.6" |
| Maxroll 2.4 final patch notes | https://maxroll.gg/d2/news/d2r-patch-2-4-final-patch-notes | via search |
| Icy Veins 2.4 compendium | https://www.icy-veins.com/d2/patch-2-4-compendium-for-diablo-ii-resurrected | via search |
| Blizzard News — PTR 3.2 | https://news.blizzard.com/en-gb/article/24266710/diablo-ii-resurrected-ptr-3-2-now-live | 200 |
| Steam — 3.1.2 "Reign of the Warlock" (2026-04-01) | https://steamcommunity.com/app/2536520/discussions/0/807973228118103547/ | via search |
| DiabloBytes — patch 3.0 notes | https://diablobytes.com/d2-resurrected/news/patch-notes-3-0/ | via search |
| Blizzard — D2R system requirements (no macOS) | https://us.support.blizzard.com/en/article/284798 | via search |
| DSOGaming — D2ROffline / D2RModding shutdown | https://www.dsogaming.com/mods/blizzard-shuts-down-diablo-2-resurrected-offline-d2rmodding-mods/ | via search |
| **grimtools calc (contrast case)** | https://www.grimtools.com/calc/w26lp5wV | **200, 33,193 B — JS shell, no build data** |
| grimtools `/calc/load/`, `/calc/get/`, `/get_build/` | same host | 200 (same shell) / 200 (same shell) / **404** |

### Endpoint probes that FAILED (reported per standing discipline)
```
https://planners.maxroll.gg/profiles/ev0106nb          404  {"message":"Route GET:/profiles/ev0106nb not found"}
https://planners.maxroll.gg/d2/ev0106nb                404  {"message":"Route GET:/d2/ev0106nb not found"}
https://planners.maxroll.gg/profiles/d2                404
https://planners.maxroll.gg/community/d2               404
https://planners.maxroll.gg/profiles/d2/community      404  {"error":"Profile not found"}
https://backend.maxroll.gg/d2planner-by-id/ev0106nb    302  (nginx)
https://backend.maxroll.gg/api/planners/d2             302  (nginx)
https://www.grimtools.com/get_build/w26lp5wV           404
gh search "diablo 2 damage calculator" / "d2r damage calculator" /
   "diablo2 dps calculator" / "d2 skill calculator"    → nothing above 3 stars
WebSearch "Diablo II Formula Compendium" Ruvanal (×2 formulations) → NOT FOUND
```
