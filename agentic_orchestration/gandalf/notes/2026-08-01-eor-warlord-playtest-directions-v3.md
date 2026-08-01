# Eye of Reckoning Warlord — play-test directions **v3** (ENDGAME-FIRST: the L100 build-of-record fixture)

**For:** Matt, at the GD **PC** · **Author:** gandalf (SPEC-AUTHOR), 2026-08-01
**Supersedes:** `2026-08-01-eor-warlord-playtest-directions-v2.md` (bannered; its recording rules,
narration rules, and all of Part II survive here — its leveling spine does not)
**Governing ruling:** `canonical/matt_decision_needed/2026-08-01-eor-playtest-v2-forks.md` (top
banner — ENDGAME-FIRST premise + F-V2-1..4 + F-V3-1, all ruled)
**Build-of-record:** V1 "Gutsmasher" EoR Warlord (banana_peel + mad_lee), final tested spec
**`https://www.grimtools.com/calc/b28gD0KN`** · corpus `gd-eor-warlord`, canon_tier=deep
**Probe of record:** `agentic_orchestration/legolas/notes/2026-08-01-eor-endgame-build-of-record.md`
— **every factual claim below is sourced there**; its URLs are not duplicated here except the two
Matt clicks from this page.
**Share copy:** `/Volumes/reincarnated/matt-notes-from-pc/eor-warlord-playtest/DIRECTIONS.md`
(re-sync on any edit; the meta-repo copy is the record).

**Why a v3.** Matt ruled the premise, not a detail: *"Other than a brief werewolf referent, I don't
see any point to making another level 13 build play test.. we need to play test end game."* The v2
spine — Righteous Fervor window, Primordian controlled experiment, EoR arriving ~L15–20 — is dead.
The character exists at **L100 from minute zero**, matched **100% to the build-of-record including
devotions** (F-V3-1, Matt verbatim: *"I will use the build guide 100%, including devotion, and we
will work out how to adapt the mechanic(s) into RDR's mechanic(s)"*). v2's devotion-ZERO rule is
struck. What that costs us, stated plainly: this fixture is **a referent and a distribution oracle,
not a controlled experiment.** Nothing is held constant against the werewolf run. What it buys is
larger — the build the game was balanced around, in the rooms it was built for.

---

# PART I — MATT'S INSTRUCTION SHEET

*Reasons in italics; the **bold lines** are the instructions. Skip the italics freely.*

## 0 · The one big idea — endgame-first, two rooms

**We are not measuring a character growing. We are measuring a finished build at the ceiling.**
Two windows, both endgame:

- **W1 — Steps of Torment, deepest floor, Ultimate.** The densest campaign content in the game;
  floor-5 wave-3 is the measured prize at **24–25 concurrent** (probe § 3.3).
- **W2 — Crucible, Gladiator, 35 minutes.** The canonical endgame benchmark — *both* Top-20
  Softcore editions, four years apart, use waves **150–170** in identically-worded language
  (probe § 3.1).
- **Plus a 10-minute werewolf referent** (§6) — carried from v2 §1.8, ruled MERGE.

*The spin is a pack-clearer. A single boss was always the wrong referent for it; a finished L100
build in a 25-monster ambush and a Gladiator wave arena is the right one. The render exhibit lives
in the Crucible setting (F-V2-1) — that is drax-side and DB-resident; it needs no capture from you.*

**One honesty note to carry into the write-up, not into the play.** This build is **1.1.9.x-era
canon**: #2 in the 2022 Top-20, **absent from both the 1.2.0.5 and 1.2.1.6 editions**, and its
closest-kin author wrote *"the time hasn't been kind to this build"* (probe § 1.1). Patch
**v1.3.0.0 reverses the exact decay he named** — EoR weapon-damage scaling to 39%/50%, and a
monster-armour cut that names Eye of Reckoning in the patch note itself (probe § 1.8). So: a
strong build again, not a current-meta build. *We describe it that way or we mis-sell our own
fixture.*

## 1 · Before the sitting

1. **Check the game version on the main menu and write it down. If Steam patched Grim Dawn after
   2026-07-24, STOP and tell us before playing.**
   *The corpus is pinned to the Edition-II 2026-07-24 fetch (patch 1.3.0.0). A patched client
   poisons every number — the co-pinning rule is the whole basis of joining video to datamine.*
2. **Vanilla client. No Grim Internals, no Rainbow Filter, no GDAutoCaster, no YoloMouse.**
   *Probe § 2.6 names all four: the first two alter what the screen shows (directly in the OCR
   path), the third alters the measured behaviour, the fourth adds cursor occlusion. GD Stash is
   fine — it is a standalone Java desktop app with no in-game component, no injector, no overlay.*
3. **Same screen resolution and UI scale as the 2026-07-26 werewolf session. Do not change them
   mid-run.** *Galadriel's crop geometry is per-resolution.*
4. **Enemy health bars ON, damage/health numerals ON, floating combat text ON.**
5. **Steam Cloud OFF, before anything else touches the save directory.** Steam → right-click Grim
   Dawn → Properties → General → the Steam Cloud checkbox. *Probe § 2.5. Cloud-off puts saves at
   `Documents\My Games\Grim Dawn\save\`. **Confirm that path by searching for a real character
   folder, not by assuming it** — an entire Crate thread exists about OneDrive hijacking
   `Documents`, and it ended in a Windows reinstall. The exact Steam menu label is flagged
   UNVERIFIED in the probe (U-5); the path consequence is confirmed either way.*
6. **Back up `Documents\My Games\Grim Dawn\save\` in full before extracting or editing anything.**
7. **Start the screen recording BEFORE you launch the game; leave it running all session. Mic on.**
   **Confirm disk headroom first** — two windows plus the werewolf referent.
8. **Pilot manually. If you macro multiple skills to one button, say so on the mic before you do.**
   *The build's own author macros Blitz + Vire's Might + medal skill to one key, and Ascension +
   Judgment + War Cry to another (probe § 2.6). If you do that undeclared, the per-skill
   `skill_use_count` series stops distinguishing those skills and we will not know why.*

## 2 · Getting the character

**R-V3-2 — savefile-primary.** *(gandalf in-seam ruling; veto-open to Matt.)*

**Path A (primary) — drop in the author's tested savefile.**

1. Download **`https://forums.crateentertainment.com/uploads/short-url/wu1LwqaU4vrKY0CtVhxCUnwj1Vu.zip`**
   — probe-verified live 2026-08-01 (HTTP 200, `application/zip`, 1.2 MB). The forum post states
   this **is** the `b28gD0KN` character.
2. Extract so the character folder (`_Name\`, containing `player.gdc`) lands in
   **`Documents\My Games\Grim Dawn\save\main\`** — `main`, **not** `user`. See R-V3-1 below.
3. Launch. The character should appear in the **main campaign** list at L100.

*Why savefile-first and not hand-construction: the build's final devotion state is **not reachable
by monotonic allocation.** It needs a temporary pick-then-refund at the spirit guide (probe § 1.5 —
multiple forum readers got stuck at exactly this, unable to meet the 8 yellow affinities for
Scales). A savefile arrives at the terminal state with no sequence at all. That is the difference
between "100% match" as a fact and as an aspiration.*

**Flagged, not buried: forward-compatibility is UNVERIFIED (probe U-2).** The zip is a 1.1.9.x-era
save; the client is 1.3.0.0. GD has historically read forward across format bumps, but nobody
tested this one. **If the character fails to load, fall back to Path B and say so.**

**Path B (fallback) — GD Stash 1.8.2g**, constructed against the grimtools sheet
**`https://www.grimtools.com/calc/b28gD0KN`**. Follow the probe's § 2.2 steps exactly — set the
save location manually (it does not default correctly; a blank dropdown means the path is wrong),
leave the Mod field empty, leave "Total Conversion Mod" unchecked, import the database, and close
GD Stash before launching GD.
*Correction the probe filed against our own prior art: **do NOT use the "grant XP → restart → kill
one mob" method.** Our 07-28 shortlist described that as the accepted path citing thread 125121 —
but 125121 **is a bug report about that method failing** (L100 Warder ending with ~8k health), and
every reply recommends something else. Root cause undiagnosed (probe U-10). Follow the probe's
corrected guidance, not that thread.*
*If you construct by hand: **Veterancy must be allocated before the chest will equip** (1035
physique requirement vs ~920 on the sheet), and **leave 10 attribute points unspent** — the author's
own reserve against exactly these equip failures (probe § 1.4, § 1.7).*

**R-V3-1 — the character lives in `save\main` (vanilla main campaign), NOT the custom game.**
*(gandalf in-seam ruling; veto-open to Matt.)*
*Forced by probe § 2.7: **a custom-game (`save\user`) character cannot enter the Crucible** —
Crucible is itself a mod, in the way the engine perceives mods. The `user`→`main` copy workaround
exists and GD Stash's own author endorses it only *"for mods that only change some data from
vanilla"* — Matt's empty mod changes nothing, so it qualifies, but it sits at the exact edge of the
author's stated limit, and W2 is half the sitting. Don't stand on the edge for no gain. The debug
console was the reason the custom-game container existed (anger-state measurement, 2026-07-25);
**this sitting is a density / TTK / kit-identity capture and does not need it** (probe U-7, routed
to me — ruled). **The werewolf referent stays in its existing custom-game save, untouched.***

**Character name — report it, don't set it.** The savefile carries the author's name. **Write down
exactly what appears in the character list, character-for-character, and put it in your report.**
*v2's "name it exactly `EoR Warlord 01`" rule adapts rather than dies: what we actually need is the
folder name, because that is the save path we pull. Renaming is optional Path-B territory; if you
do rename, report both names.*

**Skeleton Key.** *Measured, not folklore: `levelRequirement = 0`, and it is craftable from a
blueprint (probe § 3.3) — no gate at any level.* **If the imported character already has a key or
the blueprint, use it. If not, grant one via GD Stash. Do not farm for it.**

**Do NOT otherwise alter the build. Not gear, not skills, not devotions, not a "small improvement."**
*The build IS the fixture. A 100% match that is 97% is worse than useless — it is a number we
cannot attribute. If something genuinely will not work (an item won't equip, a devotion node is
missing), **change nothing and tell us**; a documented deviation is data, an undocumented one is
contamination.*

**Contingency — Crucible access (flagged UNVERIFIED; nobody has established this).** An imported
character may or may not arrive with Gladiator difficulty and the wave-150 checkpoint unlocked, and
may or may not arrive with riftgates near Steps of Torment discovered. *v1.3.0.0 made unlocking
cheaper — the next Crucible difficulty now triggers at wave 110 and wave 160 rather than requiring
a full 1–100 clear (probe § 3.1) — and GD Stash can set riftgates and Crucible token points (§ 2.2
feature list). But whether the savefile ships unlocked is not in our notes.* **If Gladiator or the
150 checkpoint is not available: play the highest difficulty and highest checkpoint that IS
available, for the same 35 minutes, and report exactly what you played.** *The 35-minute window is
the invariant; the wave band is the preference.*

## 3 · VERIFICATION CEREMONY — before the first fight, out of combat

*This replaces v2's five creation ceremonies and it is the load-bearing new beat of the whole
sitting. The exact per-slot gear, the devotion node set, and the skill ranks of the build-of-record
**are not in our notes** — deliberately. Legolas is robots-blocked from grimtools and refused to
reconstruct them from memory (probe § 1.4, U-1). **Your camera is where that data enters our
record.** The 100% match becomes a MEASURED fact here, before a single monster dies — or it becomes
a measured deviation, which is equally useful and infinitely better than an assumed match.*

**Stand somewhere safe, out of combat, and capture all of it once:**

1. **Character sheet — both tabs**, every stat legible.
2. **Both mastery windows**, at full rank display, every skill's allocated rank visible.
3. **Every equipped item's tooltip, shown once each** — all slots, including components,
   augments, and the relic.
4. **The FULL devotion screen: every constellation, every proc, and the BINDINGS.**
   *This is the frame that Matt's F-V3-1 ruling created. Which devotion proc is bound to which
   skill is exactly the adaptation-source data — "we will work out how to adapt the mechanic(s)
   into RDR's mechanic(s)" is a design workstream, and it starts from this screenshot. A devotion
   screen without the bindings is half the information.*
5. **Attributes**, including the unspent reserve if any.

**Then, with the grimtools tab open beside you, eyeball the match yourself and say on the mic
whether it matches.** *We cannot check this for you — grimtools is agent-blocked at robots.txt.
You are the only instrument that can compare the two. One sentence is enough: "matches" or "matches
except X."*

## 4 · Window W1 — Steps of Torment descent (Ultimate)

1. **Enter Steps of Torment on Ultimate and descend to the deepest floor you can reach.** The
   floor-5 wave-3 ambush is the prize.
   *Measured, and it is a genuinely good property: SoT floor-5-wave-3 is **density-invariant and
   composition-invariant** across difficulty and player level (probe § 3.3). 24–25 concurrent,
   **zero champions** (`championChance = 0`), same skeleton roster with no `minPlayerLevel` gates,
   monsters resolving to level **100–102**. The room a L100 character walks into is the same room a
   L20 character walks into. Our L20-era opposition ledger and your L100 run measure the same
   encounter shape.*
2. **The 10-hold probe (once, 60 seconds):** on the first real pack, use EoR in **exactly 10
   separate press-and-hold activations**, releasing fully between holds.
   *This decides whether the save's `skill_use_count` counts activations or ticks. The kit spec's
   entire cadence ledger hangs on it. The COUNT is the experiment, not the timing — take as long
   as you like between holds.*
3. **Say "out of energy" on the mic every time the spin cuts out from an empty bar.**
   *Broken channel segments must attribute to energy, not to piloting. At L100 with the full
   build's sustain this may never happen once — **that silence is itself the finding**, and it is
   the endgame answer to a question the L13 fixture could not ask.*
4. **Narrate the load-bearing moments** — one short sentence each: every death, every evade,
   every potion, any moment the build visibly struggles or trivialises a pack.
5. **Deaths are data. Don't reload to erase one.** *Both werewolf boss outcomes became pre-banked
   acceptance fixtures. A death at Ultimate against 25 skeletons is worth more than a clean clear.*
6. **No gear swaps, no respecs, no devotion changes — for the whole sitting.**
   *v2's "batch your equips between fights" rule retires with the leveling run and this replaces
   it. There are no regime windows now; there is one regime, and it must stay one.*
7. **After the clear: one wide screenshot of the cleared room from a corner that shows the corpse
   field.** *Campaign placement is not in the database — `Levels.arc` is a queued several-GB depot
   pull. Until then **your camera is the placement instrument**, and this frame is also the
   composition referent for the lived-in arena (R-BR-33).*
8. **Never screenshot mid-combat. Clear the area first.**

## 5 · Window W2 — Crucible, Gladiator, 35+ minutes

1. **Play the Crucible at Gladiator for at least 35 minutes.** Prefer **waves 150–170**; per §2's
   contingency, take the highest available band if 150 isn't offered and report what you played.
   *Both Top-20 editions, 2022 and 2026, state the same benchmark verbatim: every listed build
   *"finish[es] 151-170 within 4:30 in the best run."* 35 minutes buys roughly **4–6 complete
   150–170 runs** — and several short runs give more engagement segments than one long climb
   (probe § 3.1).*
2. **Quick re-shot of the character sheet + devotion screen between the windows if ANYTHING
   changed** (a level-up is impossible at 100, but blessings, buffs, or a swapped component are
   not). Otherwise skip it. *One ceremony, one regime — confirm it held.*
3. **DECLARED CONFOUND — do not let anyone discover this later.** v1.3.0.0 increased all boss
   health scaling by **~32% at level 100 — and those changes explicitly do NOT apply to the
   Crucible** (probe § 1.8). **So W1 runs against post-buff boss HP and W2 does not. Any TTK
   comparison across the two windows carries this asymmetry by construction.** We name it now
   rather than rediscover it in the analysis.
4. **Second measured fact worth knowing while you play:** Crucible difficulty is **not a density
   dial** — `spawnMinAdj` and `spawnMaxAdj` are **zero on all three difficulties**; what Gladiator
   buys is **monster health** (`characterLifeModifier` +304→344% at waves 150–170, versus
   +108→128% at Aspirant). *Probe § 3.2. Gladiator is a time-per-kill dial, not a
   monsters-on-screen dial. If the room feels the same but slower, that is the data being honest.*
5. **Same narration rules as §4. Same no-mid-combat-screenshot rule. Same deaths-are-data rule.**

## 6 · The werewolf referent (10 minutes, ruled MERGE — v2 §1.8 carried verbatim)

**Load the existing L13 werewolf in its existing custom-game save and play one ordinary encounter
chain on camera.** Same recorder, zero extra setup. *That short clip is the referent for every
"does the sim read right?" parity question WR3 left open.* **T11 (the Veteran `.gdc` pull) rides
with whichever sitting touches the werewolf save** — this one. **Do not move, copy, or edit that
character; it stays in `save\user`.** *R-V3-1 puts the new character in `save\main`; the werewolf
stays where it is. Two save roots, two pulls, no conversion.*

## 7 · Ending the run

1. **Exit to the main menu, then quit the game.** *Forces the final save flush.*
2. **Do NOT play the character again until we confirm the save is copied.**
   *The path has CHANGED from the werewolf pattern: it is now
   `Documents\My Games\Grim Dawn\save\main\_<name>\` — `main`, and `<name>` is whatever the
   savefile's character is actually called. The werewolf's own pull is still under `save\user\`.*
3. **Put the video on the share** (or name its path). T11's SSH pattern applies (PC, F-V2-3).
4. **Report back — one short message:** game version string · difficulty played in each window ·
   **the character name, verbatim** · which Crucible wave band you actually played · whether Path A
   or Path B built the character · whether the verification ceremony matched · any deviation from
   this doc. *Everything else we measure from the save and the video.*

## 8 · What happens on our side (so nothing is mysterious)

Save parse (measured build identity, day one) → **pixel mining** (HP series, tooltips, regime
segmentation; galadriel) → **endgame EoR kit spec**, with **devotion-proc damage as a NAMED
measured layer** rather than an unexplained residual → **dense-room sim + render exhibits** built
from DB-resident rooms with **zero capture needed** (Crucible t13w06 as the deterministic room, SR
Shard-33+ as the ceiling exhibit) → **the devotion→RDR mechanic-adaptation grill**, an ELICITOR
session that fires after the fixture lands. *Read-only on the save throughout.*

---

# PART II — OUR SIDE: carried forward BY REFERENCE

*v2 §§ II.1–II.4 remain governing and are **not** reproduced. Read them there. Only the deltas the
endgame-first ruling creates are listed below.*

| v2 section | Status under v3 | Delta |
|---|---|---|
| **II.1 — pipeline** | GOVERNING | The "we do not need Matt to grind to 100" clause is **struck** — F-V2-4 dissolved; the endgame validation IS the session. Calibration anchors at L100, not L15–20. |
| **II.2 — engine gap table** (8 rows) | GOVERNING, unchanged rows 1–7 | Row 8 **Retaliation — still EXCLUDED** (V1 is the physical-hit spin; V5's bleed-conversion variant was explicitly rejected as a different BC-axis signature). **New row 9: devotion-proc layer — MEASUREMENT TARGET + adaptation source.** Procs bound to skills are an unmodelled damage layer in the sim today; F-V3-1 makes them a named measured quantity and a design workstream, not a gap-register line. |
| **II.3 — drax emission needs** (6 items) | GOVERNING | Item 4 (N-actor trace) now stresses at **Crucible scale**, not SoT scale — the render exhibit moved to the Crucible setting (F-V2-1). Item 5's arena footprint takes the Crucible arena, with SoT's Ceremony frame as the campaign referent. Add: **proc-triggered secondary damage events need their own record class** or they will silently fold into weapon damage — the R-BR-34 census rule applied to a layer that did not exist in v2. |
| **II.4 — probe queue** | UNCHANGED status | P-D1 **LANDED**. **P-E1 / P-E2 / P-E3 / P-E4 all still open** — and P-E1 (`Skill_AttackRadiusSpin` per-rank tick cadence, radius, energy drain) is now needed at **max ultimate rank**, not rank 1–5. **New: P-E5 — devotion constellation → proc template join** (proc damage, trigger conditions, cooldowns, bind rules), consumer = the new gap row 9. |
| **II.5 — open forks** | CLOSED | F-V2-1..4 and F-V3-1 all ruled (see the governing banner). The live forks are now **R-V3-1** and **R-V3-2** above, both gandalf in-seam and both **veto-open to Matt**. |

**One new opposition-side note for whoever builds the Crucible sim room:** the Crucible balancing
records carry a `retaliationTotalDamageModifier` of **74 at Gladiator** versus 53–54 at the lower
difficulties (probe § 3.2). That is monsters retaliating, not the player — an opposition property
the Crucible room needs and the SoT room does not. **And two numbers the probe refuses to give:**
computed Gladiator concurrency (U-9 — the `spawnMinModifier` operator order is unestablished; the
naive computation produced min > max, which is impossible) and the Crucible tier→wave mapping
(U-8). **Do not quote a Gladiator monster-count figure until those close.**

---

*Filed as the KIT-CAL-2 endgame substrate-capture protocol, v3. Desirable-run-pattern fit: the
L100 build-of-record fixture is the bounded substrate; the verification ceremony makes the "100%
match" premise **decidable before play** rather than assumed after it; SoT floor-5-wave-3's measured
density-invariance and the Crucible's four-year-stable 150–170 benchmark make both windows
decidable against fixed referents; the declared boss-HP asymmetry is the honorable-fallback clause
for cross-window TTK. R-V3-1 and R-V3-2 are the ruling ledger, veto-open. P-E1–E5 are the ELICITOR
drain that keeps the eventual KIT-CAL-2 charter's ARCHITECT gate clean. — gandalf, 2026-08-01*
