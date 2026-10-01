# C-12b — the D2 Fire Sorceress's home frontier point — 2026-10-01

**Mode:** A (analytical; open-question search)
**Commissioner:** gandalf, Run JOIN-1 wave J4b (charter § 4.5, J-S7, commission C-12b; same standard as C-12)
**Question:** what is the hardest content this kit is known to clear in its home game, and how fast? The answer has to be a sourced **LoD 1.13** point that the arena margin can be measured against.
**Law:** JOIN-1's law is LoD 1.13 (KP-160, Q10). D2R figures are context only.

---

## Verdict

**C-12b returns SEARCHED-UNLOCATED: there is no home margin.** Under the charter, the home margin is **`DEFERRED`**. The re-entry criterion below goes on the fidelity-cost table, as it did for C-12.

The search found three things.

1. **No timed LoD 1.13 clear exists for this kit in any source I could reach.**
   - Every Fire Ball/Meteor timing found is either from D2R, or from before D2R with no date, gear or clock definition.
   - The pre-D2R reports found are not even this kit. One is a Frozen Orb + Fire Ball hybrid (2005). The other is a level-96 "FB/Meteor" Uber run of unknown gear (§ Candidates).
2. **A sourced 1.13 capability anchor exists only in negative form, and it is DATAMINED.**
   - In 1.13 this kit **cannot damage Uber Diablo**. `uberdiablo` ResFi(H) = **110**, which makes him immune.
   - 1.13 items cannot lower an immune's resistance (`formulas.json` H08).
   - The kit carries no Lower Resist and no Conviction.
   - So **Uber Tristram (Levels Id 136) is not a 1.13 home point for this kit.** It is not merely unsourced; it is infeasible.
3. **D2R points do not transfer**, even though the skill laws are the same. See the next section.

---

## Did Meteor and Fire Ball change in D2R?

**Skill laws: essentially no.**

| Law | LoD 1.13 | D2R | Source |
|---|---|---|---|
| Fire Ball damage, synergies (+14%/blvl Fire Bolt, Meteor) | as `primary_rows.json` | **unchanged** | Blizzard 2.4 notes and Maxroll 2.4 notes list no Fire Ball change; Basin's current page has one table |
| Meteor impact, radius 4 yd, impact action+60, pyre law, +3%/blvl Inferno | as `primary_rows.json` | **unchanged** | as above; Basin's current Meteor page keeps one table |
| Meteor casting delay 1.2 s | **global** (shared with other delayed skills) | **local** (per-skill), from 2.4 | Blizzard 2.4; Maxroll 2.4; Basin "1.2, global (LoD) / 1.2, local (D2R)" |
| Fire Mastery, Warmth, Fire Bolt | — | **unchanged** | not in the 2.4 change list; Basin pages |
| FCR breakpoints | 13/12/11/10/9/8/7 | **identical** | sister packet |

**For this kit, the delay change has no effect on cadence.** Fire Ball has no delay, and in LoD a casting delay blocks only other delayed skills (Arreat, Casting Delays).

One limit on this: the Patch 3.0 (Reign of the Warlock) check rests on a single secondary summary (DiabloBytes: "no Sorceress skill balance changes").

**What did change in D2R is how the world meets a pure-fire kit.** Each of these moves clear speed:

1. **Sunder charms (D2R only).** Flame Rift sets every fire-immune monster's resistance to 95 (Basin, Sunder). Maxroll's Season 14 guide for this build lists Flame Rift in its charms.
   - In 1.13, fire immunes are untouchable for this kit.
   - D2R therefore opens content (for example, Uber Diablo) and whole packs that 1.13 closes.
2. **Flickering Flame (D2R only).** The kit record names it as a helm. It has no row in 1.13 `UniqueItems.txt`, and Basin marks it "D2R only". The 1.13 profile must take the record's alternative, Harlequin Crest.
3. **Terror Zones (D2R 2.5)** change area levels, so a D2R "Chaos" or "Pit" time may not be at the J-S7 area level.

**Conclusion:** a D2R time measures a different immunity regime, and that cannot be corrected without a model. It does not transfer.

---

## Candidate points found, with source quality

Area references are DATAMINED from J-S7 (`Levels.txt` sha256 `3163b66e…`, `MonStats.txt` sha256 `973eedac…`, `fabd/diablo2 @ 45112569`):
- Chaos Sanctum Id 108, Hell area level 85.
- Durance of Hate Level 3 Id 102, Hell area level 83.
- Pit Level 1 / 2: Id 12 / 16, Hell 85.
- Throne of Destruction Id 131, Hell 85.
- Pandemonium Finale "Tristram" Id 136, Hell 83.

Boss fire resists in Hell (`ResFi(H)`): mephisto 75 · diablo 50 · baalcrab 50 · andariel −50 · ubermephisto 75 · uberbaal 75 · **uberdiablo 110 (immune)**.

| # | Content | Claimed result | Version | Gear vs kit | Source and quality |
|---|---|---|---|---|---|
| Q1 | Uber Tristram, "all three" | "5+ minutes", with 2 deaths, no prebuff, no Fade | pre-D2R (diablo2.io tags the post "pre-Resurrected"); patch and date unrecoverable from the page | **Unknown** (level-96 "FB/Meteor sorc") | diablo2.io poll thread, user "vued". **TERTIARY, single, untimed ("5+"), no gear, no /players.** ⚑ **It conflicts with the DATAMINED immunity:** a pure-fire 1.13 kit cannot damage Uber Diablo (ResFi(H) 110). So the run used something outside this kit (a merc, or non-fire damage). Not admissible. |
| Q2 | Hell Baal runs (full run including waves) | "average runtime is 5 minutes in a 6-8 player game and 3 minutes in a 1 player game" | 2005-07-16. The patch is not stated; CoH, Spirit and Facets imply ≥ 1.10 | **Not this kit:** a Frozen Orb + Fire Ball hybrid with Death's Fathom, a faceted Nightwing's Veil and 8 cold-skill grand charms. Cold primary | Tom's Hardware forums, "Fastest Hell Baal Killer", Alex Holtz. **TERTIARY, single self-report, no video.** Wrong kit. |
| Q3 | Capability: Andariel, Mephisto, Stony Tombs, The Pit, Mausoleum, Lower Kurast, Eldritch/Shenk, Cows, Ancient Tunnels, Maggot Lair | No times | **D2R Season 14** (updated 2026-05-22) | Kit-record gear family; **Flame Rift sunder charm included** | Maxroll, Teo1904. This is the kit record's own citation. **SECONDARY, authored, D2R.** These are mostly fire-immune-light areas. That is consistent with the immunity problem, but it is a D2R list. |
| Q4 | "Fireball/Meteor … fastest Baal / boss farming" | Baal "around 2 minutes" (wave delays) | Unstated; search-summary snippets only | Unstated | Search-engine summaries of PureDiablo and other threads. PureDiablo returned 403 to a direct read, so these were **not verified**. Not admissible. |

Searched without a usable result:
- d2jsp topics 76839004 ("Fire Ball/meteor Sorceress") and 86566158 ("Chaos Sanctuary As Meteorb"). d2jsp returns 403 to read-only fetches.
- speedrun.com d2lod. Its categories time full-game races (same finding as C-12).
- YouTube searches for 1.13 Fire Ball sorc clear videos found only D2R-season titles.
- Icy Veins, the kit record's other citation, returned 403. Its anchor quote in the kit record names skill points only.

---

## What is defensible

- **A negative capability anchor, HIGH confidence (DATAMINED + MODEL-VERIFIED):** in 1.13 the kit cannot damage `uberdiablo`, and it deals zero damage to any monster whose `ResFi` at that difficulty is ≥ 100. Any home point must therefore be chosen **per area, against J-S7's fire-immune census**. That census is elrond's or gamora's to compute; it is not tabulated here.
- **A positive 1.13 capability anchor: none sourced.** Maxroll's farming list is D2R and assumes Flame Rift.
- **A timed anchor: none.**

---

## Re-entry criterion (for the fidelity-cost table's face)

Home margin moves from `DEFERRED` to measured when a timed clear exists that meets **all** of the following (the same four tests as C-12):

1. **Version:**
   - **either** LoD 1.13 (1.10–1.14d mechanics, expansion game, no sunder);
   - **or** the conductor rules a D2R point admissible. That ruling must record as named fidelity costs: (a) Sunder/Flame Rift, (b) Flickering Flame, (c) Terror Zone area levels.
2. **Gear** matches the JOIN profile's pinned loadout. At minimum: weapon (Eschuta's Temper or Heart of the Oak), shield (Spirit Monarch), helm, armour, and **no sunder charm** if the point claims 1.13.
3. **Content is stated:** `Levels.txt` Id, difficulty, /players, merc yes/no, and what the clock spans. The area must contain **no monster the kit cannot damage**, or the report must say how those monsters were handled.
4. **Corroboration:** two independent reports, or one video with a frame-countable timer.

**The cheaper path C-12 named applies here too.** A home point computed in home rules (the kit through a 1.13-faithful replay of a J-S7 area) would meet criteria 1–3 by construction and lack only criterion 4. Whether to adopt it is the conductor's decision. KP-160 declined it for the Barbarian.

---

## Sources (accessed 2026-10-01)

**Primary**
- J-S7 tables, `fabd/diablo2 @ 45112569`: `Levels.txt`, `MonStats.txt`, `UniqueItems.txt`.
- D2MOO @ `5596f5cb`, `SUnitDmg.cpp` (the immunity gate on item pierce).

**D2R change record**
- Blizzard, Patch 2.4 Balance PTR notes: https://news.blizzard.com/en-us/article/23765907/diablo-ii-resurrected-patch-2-4-balance-ptr-has-ended
- Maxroll, Patch 2.4 notes: https://maxroll.gg/d2/news/patch-2-4-notes
- DiabloBytes, Patch 3.0 notes: https://diablobytes.com/d2-resurrected/news/patch-notes-3-0/

**Basin Wiki**
- Meteor: https://www.theamazonbasin.com/wiki/index.php?title=Meteor
- Fire_Ball: https://www.theamazonbasin.com/wiki/index.php?title=Fire_Ball
- Sunder: https://www.theamazonbasin.com/wiki/index.php?title=Sunder
- Immune: https://www.theamazonbasin.com/wiki/index.php?title=Immune
- Mana (Flickering Flame "D2R only"): https://www.theamazonbasin.com/wiki/index.php?title=Mana

**Arreat Summit**
- Casting Delays: https://classic.battle.net/diablo2exp/skills/castingdelays.shtml

**Build guides and forums**
- Maxroll, Teo1904, Fire Ball Meteor Sorceress (S14, updated 2026-05-22): https://maxroll.gg/d2/guides/meteor-sorceress
- diablo2.io, "Poll: Uber Tristram Prime Evil Killers": https://diablo2.io/post4498184.html
- Tom's Hardware forums, "Fastest Hell Baal Killer" (2005-07): https://forums.tomshardware.com/threads/fastest-hell-baal-killer.132878/

**Blocked (403) and not read**
- https://forums.d2jsp.org/topic.php?t=76839004&f=87
- https://www.purediablo.com/forums/threads/sorceress-fast-safe-baal-runs.175859/
- https://www.icy-veins.com/d2/fireball-sorceress-build
