# Eye of Reckoning Warlord — play-test directions (KIT-CAL-2 fixture capture)

**For:** Matt, at the GD PC · **Author:** gandalf, 2026-07-28 · **Build:** C2 "Gutsmasher"
(shortlist top-2; corpus `gd-eor-warlord`, canon_tier=deep; `.arz`-confirmed
`playerclass09/eyeofreckoning1.dbr` → `Skill_AttackRadiusSpin`)
**Share copy:** `/Volumes/reincarnated/matt-notes-from-pc/eor-warlord-playtest/DIRECTIONS.md`
(the two are identical; the meta-repo copy is the record).

Every rule below exists because KIT-CAL-1 paid for it. The one-line reason sits under each
rule in *italics* — skip them freely; the **bold lines** are the instructions.

---

## 0 · The one big idea

**Same arena, new fighter.** Play the SAME campaign setup, same path, same target boss
(Primordian) as the 2026-07-26 werewolf run. The opposition side of that fixture is already
measured and built in the sim — mob rosters, the Primordian proto, the HP tables. If the
opposition stays constant and only the build changes, KIT-CAL-2 becomes a controlled
experiment: every difference between the two fixtures is the KIT.

---

## 1 · Before you create the character (5 minutes)

1. **Check the game version on the main menu and write it down.** If Steam patched Grim Dawn
   any time after 2026-07-24, STOP and tell us before playing.
   *Our datamined corpus is pinned to the 2026-07-24 Edition-II fetch. A patched client
   against an unpatched corpus poisons every number (co-pinning rule).*
2. **Vanilla client — no mods, no Grim Internals, no UI overlays.**
   *The pixel-mining pipeline is calibrated to the stock UI.*
3. **Same screen resolution and UI scale as the 2026-07-26 session. Do not change them
   mid-run.**
   *Galadriel's crop geometry is tuned per-resolution; the werewolf run's one measurement
   residual (armour tooltip) came from a crop misfit. A resolution change invalidates all of it.*
4. **Settings → make sure enemy health bars AND damage/health numerals are ON, floating
   combat text ON** (same as last run).
   *Frame 281 of the werewolf run proved the client renders monster HP numerals — that
   "scoreboard" pinned a composition rule no save file could give us.*
5. **Start the screen recording BEFORE character creation and leave it running the whole
   session.** Same recorder and settings as last time. If you have a mic: enable it (see §3.2).
6. **Same difficulty and same campaign mode as last time** (your custom-game campaign). If
   you change either, that's fine — but say so when you report.
   *Mode decides where the save lives on disk; difficulty changes the opposition we'd have
   to re-measure.*

## 2 · Character creation + build rules

1. **Name the character exactly: `EoR Warlord 01`** — and it's already written here, so it's
   already reported.
   *The werewolf's name was written down nowhere; recovering it cost a ruling, an SSH probe,
   and a ten-path search.*
2. **Masteries: Oathkeeper first (level 2), Soldier second (level 10).**
3. **Play the SPIN build, not the retaliation variant.** Righteous Fervor as the early main
   attack; pump the Oathkeeper mastery bar toward Eye of Reckoning; switch to EoR as your
   main attack the moment it's castable and sustainable.
   *Retaliation appears nowhere in the sim — a retal fixture would be accountable to nothing.
   The spin is the calibration target: sustained channel + melee-radius AoE, two named gap
   families in one kit.*
4. **Devotion: spend ZERO points. Bank them all, the whole run.**
   *Devotion procs are inexpressible in the sim today. The werewolf fixture's devotion-zero
   is what made its join clean — and it took a save parse to prove it after the fact. This
   time it's a rule, not an attestation.*
5. Gear, components, attributes: as the build wants — free choice. **If any item grants an
   active skill you actually use, say so out loud / note it.**

## 3 · During play

1. **Never screenshot mid-combat. Clear the area first.**
   *Werewolf death #1 was you standing in damage taking a screenshot — it cost us a caveat
   on a ratified ruling.*
2. **If the mic is on, narrate the load-bearing moments** — one short sentence each:
   big gear equip ("equipping the new shield now"), each death ("the ground AOE got me"),
   each evade ("dodged the slam"), potion use, and the moment EoR becomes your main attack.
   *Your werewolf testimony had to be reconstructed afterward and ratified as rulings. A
   timestamped sentence on the video replaces a whole adjudication lap.*
3. **Equip big upgrades in a batch, between fights, and call it out.**
   *The werewolf fixture's regime boundary WAS a gear step (759→1600 HP in one equip). Crisp
   steps = crisp windows; piecemeal equipping smears the boundary.*
4. **The 10-hold probe (60 seconds, once):** on the first pack you fight after EoR comes
   online, use EoR in **exactly 10 separate press-and-hold activations** (release fully
   between holds; a few seconds each is fine). Then play normally.
   *This closes the shortlist's one open instrumentation question: whether the save's
   `skill_use_count` counts channel activations or channel ticks. Your 10 holds against the
   parsed counter is the whole experiment.*
5. **Deaths are data. Don't reload to erase one — just say what killed you and keep going.**
   *Both werewolf boss outcomes (the death AND the win) became pre-banked acceptance fixtures
   for sim mechanics. An erased death is an erased fixture.*
6. Otherwise: **play naturally.** Evade, kite, facetank — your real play is the fixture.

## 4 · Screenshot ceremonies (3 total, out of combat)

At each of these three moments, stand somewhere safe and take this set: **character sheet
(both tabs) · both mastery skill windows · inventory open with each equipped item's tooltip
shown once · devotion screen (showing zero spent).**

- **Ceremony 1:** right after taking Soldier at level 10.
- **Ceremony 2:** right before engaging Primordian.
- **Ceremony 3:** immediately after the run ends.

*The werewolf run's tooltips were mined from lucky incidental frames; G-6 ran blind and
still carried the verdict. Three deliberate sets make every kit number first-class.*

## 5 · Ending the run

1. **Endpoint:** kill Primordian (however many attempts it takes), then stop at a natural
   point. **[FORK-1 — see §7]:** if Eye of Reckoning is not yet online by the Primordian
   fight, kill Primordian anyway (that's the werewolf-comparable window), then CONTINUE
   until EoR has been your main attack for a solid stretch (including the 10-hold probe)
   and one more boss-grade fight, then stop.
2. **Exit to the main menu, then quit the game.** *(Forces the final save flush.)*
3. **Do NOT play `EoR Warlord 01` again until we confirm the save is copied.** We'll SSH-copy
   the folder like last time (T11 pattern) — it's `…\save\user\_EoR Warlord 01\` in your
   custom-game layout.
   *The `.gdc` stores only current state. One more session overwrites the end-of-run gear,
   skills, and counters we're trying to measure.*
4. **Put the video file on the share** (`/Volumes/reincarnated/matt-notes-from-pc/`, same as
   your console notes) or leave it where the last one lived and tell us the path.
5. **Report back — one short message:** game version string · difficulty · campaign mode ·
   the level at which EoR became your main attack · any deviations from this doc. Everything
   else (build identity, skill ranks, counters, potions) we measure from the save and video.

## 6 · What happens on our side (so nothing here is mysterious)

Save parse (measured build identity from day one — no attested phase this time) → pixel
mining (HP series, tooltips, regime segmentation) → EoR kit spec → KIT-CAL-2 calibration
battery against the SAME opposition as KIT-CAL-1. The channel mechanic will exercise exactly
what KIT-CAL-1 just repaired and exposed: the DoT delivery ledger, the attack-speed-less
tick model, and the A-statistic coincidence floor. Read-only on our side throughout; nothing
ever writes to your save.

## 7 · FORK-1 — **RESOLVED** (2026-07-28, measured from the `.arz`; legolas
`2026-07-28-eor-unlock-timing.md`)

**EoR rank 1 is castable at character level 10 — the earliest possible.** Two independent
gates land on the same level, by design: tier-6 skills need Oathkeeper mastery bar 25
(27 points = exactly level 10's income), and the game first permits a second mastery at
level 10. So you *can* take EoR right at Ceremony 1.

**But castable ≠ main attack.** Two measured reasons:

1. **Points:** an unrespecced natural build has EoR as the genuine main attack around
   **level ~20** (an efficient split gets there ~15).
2. **Energy:** the channel drains **25 energy/sec at rank 1** against a ~575 pool with ~1/s
   base regen — **≈24 seconds of continuous spin from a full bar**, and it gets shorter as
   you rank it up. Early EoR runs in bursts, not as a hold-the-button style.

**So plan on §5.1's two-window path as the EXPECTED path, not the fallback:** Primordian
(you fought him around level 12 last time) will almost certainly happen in the
Righteous-Fervor window — that IS the werewolf-comparable window. Then keep playing until
EoR is truly your main attack (~15–20), run the 10-hold probe, get one more boss-grade
fight, and stop.

**Empty energy bar is data, not error.** When the spin cuts out because the bar ran dry,
say so on the mic ("out of energy") — broken channel segments will show up in the capture
and we need to attribute them to energy, not to your piloting. If energy runs dry during
the 10-hold probe, pause and regen between holds: the COUNT of activations is the
experiment, not their timing. Spirit attribute points are the energy-sustain lever if the
channel feels starved — still your free choice per §2.5.

---

*Filed as the KIT-CAL-2 substrate-capture protocol. Desirable-run-pattern fit: the fixture
this produces is the bounded substrate; the werewolf fixture + constant opposition make the
target-state decidable. — gandalf*
