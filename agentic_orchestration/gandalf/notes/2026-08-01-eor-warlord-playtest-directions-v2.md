# Eye of Reckoning Warlord — play-test directions **v2** (KIT-CAL-2 fixture capture + THE DENSE ROOM)

> **⚠ SUPERSEDED 2026-08-01 by `2026-08-01-eor-warlord-playtest-directions-v3.md`** — Matt's
> ENDGAME-FIRST premise ruling struck this doc's spine (no leveling run; the character exists at
> L100 matched 100% to the build-of-record **including devotions**, so §2.4's devotion-ZERO rule is
> dead and §§0/2/4/5's RF→Primordian→EoR-online structure is dead). v3 carries forward the
> recording rules, the narration rules, the 10-hold probe, the werewolf referent, and **all of Part
> II by reference** (§§ II.2–II.4 remain governing; v3 lists only the deltas). Windows are now SoT
> deepest floor + 35 min Crucible/Gladiator; machine is PC. Do not play from this copy; the share
> copy re-syncs from v3.

**For:** Matt, at the GD machine · **Author:** gandalf (SPEC-AUTHOR), 2026-08-01
**Supersedes:** `2026-07-28-eor-warlord-playtest-directions.md` (bannered; all its rules survive here
unless struck) · **Build:** C2 "Gutsmasher" (corpus `gd-eor-warlord`, canon_tier=deep;
`.arz`-confirmed `playerclass09/eyeofreckoning1.dbr` → `Skill_AttackRadiusSpin`)
**Share copy:** `/Volumes/reincarnated/matt-notes-from-pc/eor-warlord-playtest/DIRECTIONS.md`
(re-sync on any edit; the meta-repo copy is the record).

**Why a v2 (what changed since 07-28):** WR3-KITE-COMMIT closed at target-state (W=1.0 saturated
PASS; wind-down `2026-07-31-wr3-kite-commit-run-wind-down.md`) and BR-2 TRUE-SHAPE is mid-flight —
between them the trace schema grew (`duration_s`, `stage_count`, `hit_radius_m`,
`projectile_velocity_ms`), the arm of record was frozen, and four "one scalar carried two meanings"
defects were caught. Those lessons are baked into Part II. And Matt added a second objective:
**find the most highly dense pack-filled area in Grim Dawn and represent that room in the battle
simulator and the Godot render** — that program is §D, and it changes the shape of the run from
one window to two.

---

# PART I — MATT'S INSTRUCTION SHEET

*Every rule exists because KIT-CAL-1 paid for it. Reasons in italics; the **bold lines** are the
instructions.*

## 0 · The one big idea — TWO windows, TWO fixtures

**Window 1 — Righteous Fervor / Primordian (the controlled experiment).** Same campaign setup, same
path, same target boss (Primordian) as the 2026-07-26 werewolf run. Opposition already measured and
built; only the build changes; every difference between the fixtures is the KIT.

**Window 2 — Eye of Reckoning / THE DENSE ROOM (the spin's natural referent).** EoR is a
pack-clearing spin — a single boss is the wrong referent for it. After EoR becomes your main
attack, the fixture that measures it is a **dense pack room** (§D names it from the datamine). The
werewolf's boss duel calibrated a duelist's kit; the spin needs a crowd. This window is ALSO the
substrate for the standing render goal: a multi-actor pack fight in the Godot scene, blood pools
accumulating per R-BR-33's lived-in-arena ruling.

## 1 · Before you create the character (5 minutes)

1. **Check the game version on the main menu and write it down.** If Steam patched Grim Dawn after
   2026-07-24, STOP and tell us before playing.
   *Corpus pinned to the 2026-07-24 Edition-II fetch; a patched client poisons every number
   (co-pinning rule).*
2. **Vanilla client — no mods, no Grim Internals, no UI overlays.**
3. **Same screen resolution and UI scale as the 2026-07-26 werewolf session. Do not change them
   mid-run.** *Galadriel's crop geometry is per-resolution.*
4. **Enemy health bars ON, damage/health numerals ON, floating combat text ON.**
5. **Start the screen recording BEFORE character creation; leave it running all session. Mic on if
   you have one** (§3.2). **Confirm disk headroom for a multi-hour recording first** — this run is
   longer than the werewolf's (two windows).
6. **Same difficulty and campaign mode as the werewolf run.** If you change either, say so when you
   report.
7. **Which machine?** The 07-28 doc assumed the GD PC; the WR3 wind-down §7.5 planned Mac-side
   recording tooling. **Either is fine — but say which in your report**, because the save-copy path
   and the pull pattern (SSH T11 vs local copy) differ.
8. **Optional 10-minute prelude (merges wind-down §7.5):** before creating the new character, load
   the L13 werewolf and play one ordinary encounter chain on camera. *That short clip is the
   referent for every "does the sim read right?" parity question WR3 left open — same recorder,
   zero extra setup. Skip freely if you'd rather not; it queues separately.* **T11 (the Veteran
   `.gdc` pull) rides with whichever sitting touches the werewolf save.**

## 2 · Character creation + build rules

1. **Name the character exactly: `EoR Warlord 01`.**
2. **Masteries: Oathkeeper first (level 2), Soldier second (level 10).**
3. **Play the SPIN build, not the retaliation variant.** Righteous Fervor as the early main attack;
   pump Oathkeeper toward Eye of Reckoning; switch to EoR as main attack when it is castable AND
   sustainable. *Retaliation appears nowhere in the sim; the spin is the calibration target.*
4. **Devotion: spend ZERO points. Bank them all, the whole run.** *Devotion procs are inexpressible
   in the sim today; devotion-zero is what made the werewolf join clean.*
5. Gear, components, attributes: free choice. **If any item grants an active skill you actually
   use, say so on the mic.** *Spirit points for energy sustain are explicitly allowed — the channel
   drain is real (measured: 25 energy/s at rank 1 vs ~575 pool; ~24 s of spin from a full bar).*

## 3 · During play

1. **Never screenshot mid-combat. Clear the area first.**
2. **Narrate the load-bearing moments** — one short sentence each: big gear equips, each death,
   each evade, potion use, **the moment EoR becomes your main attack**, and **every time the spin
   cuts out from an empty energy bar ("out of energy")**. *Broken channel segments must attribute
   to energy, not to piloting.*
3. **Equip big upgrades in a batch, between fights, and call it out.** *Crisp gear steps = crisp
   regime windows.*
4. **The 10-hold probe (60 seconds, once):** on the first pack after EoR comes online, use EoR in
   **exactly 10 separate press-and-hold activations** (release fully between holds). If energy runs
   dry mid-probe, pause and regen between holds — the COUNT is the experiment, not the timing.
   *This decides whether the save's `skill_use_count` counts activations or ticks — the kit spec's
   cadence ledger hangs on it.*
5. **Deaths are data. Don't reload to erase one.** *Both werewolf boss outcomes became pre-banked
   acceptance fixtures.*
6. Otherwise: **play naturally.** Evade, kite, facetank — your real play is the fixture.

## 4 · The expected path (FORK-1 resolution, carried forward)

EoR rank 1 is castable at level 10 (measured, `2026-07-28-eor-unlock-timing.md`) but is not a
sustainable main attack until roughly **level 15–20** (points + energy, both measured). So:

1. **Window 1:** fight Primordian in the Righteous-Fervor window (~L12, werewolf-comparable). Kill
   him, however many attempts.
2. **Bridge:** keep playing until EoR is genuinely your main attack. Run the **10-hold probe**.
3. **Window 2:** clear **THE DENSE ROOM** (§D below — the named target + fallback) with EoR as the
   main attack. Then one more boss-grade fight if the path offers one, and stop at a natural point.

## 5 · Screenshot ceremonies (5 total, out of combat)

At each moment, stand somewhere safe and take the full set: **character sheet (both tabs) · both
mastery skill windows · inventory open with each equipped item's tooltip shown once · devotion
screen (showing zero spent).**

- **Ceremony 1:** right after taking Soldier at level 10.
- **Ceremony 2:** right before engaging Primordian.
- **Ceremony 3:** right after the Primordian window ends (win banked).
- **Ceremony 4:** the session EoR becomes your main attack — right after the 10-hold probe.
- **Ceremony 5:** immediately before entering THE DENSE ROOM — and after clearing it, one extra
  **wide screenshot of the cleared room** from a corner that shows the corpse field.
  *That frame is the composition referent for the Godot dense-room scene — the lived-in arena,
  photographed from the referent itself.*

## 6 · Ending the run

1. **Exit to the main menu, then quit the game.** *(Forces the final save flush.)*
2. **Do NOT play `EoR Warlord 01` again until we confirm the save is copied.**
3. **Put the video on the share** (or name its path).
4. **Report back — one short message:** game version · machine (PC or Mac) · difficulty · campaign
   mode · the level at which EoR became your main attack · which dense room you cleared (§D target
   or fallback) · any deviations from this doc. Everything else we measure from the save and video.

## D · THE DENSE ROOM — MEASURED (legolas `2026-08-01-gd-pack-density-ranking.md`, probe of record)

**The ranking, from the `.arz` — counts, not folklore:**

| Rank | Where | Density (measured) | DB-resident? | Record |
|---|---|---|---|---|
| 1 | **Shattered Realm, Shard 33+** (GDX2 endgame) | **142.5 / 188.6 / 209.4** monsters per floor (Norm/Elite/Ult); 29 common + 10 hero + 4 boss placements | **FULLY** | `endlessdungeon/rulesets/dungeonset15.dbr` |
| 2 | **Crucible tier 13 wave 06** | **35 min guaranteed** / 36 max, one arena, 6 spawn points (tier 14 w06 peaks 42 but spreads 30–42) | **FULLY** | `proxies/tier13waves/proxy_w06_*.dbr` |
| 3 | **Steps of Torment, floor 5 wave 3** (Act 2 campaign) | **24–25 concurrent, sustained** (`maxGroupSize=25`, pool `spawnMin=spawnMax=24`) | partial (placement needs `Levels.arc`) | `proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr` |

Folklore scored ~50%: SoT / Bastion of Chaos / Port Valbury CONFIRMED as the campaign top-3;
Cronley's Hideout, the Fleshworks, Ancient Grove, Tomb of the Heretic **UNPROBED** (generic pools
in level geometry we don't hold).

**D.1 — Window-2 TARGET (proposed; F-V2-1, your ruling): Steps of Torment, deepest floor you can
reach — the floor-5 wave-3 ambush is the measured 24–25-monster prize.** It is the densest
campaign content in the game, it sits in Act 2 **on the natural leveling path right where EoR
comes online**, and GD has no absolute monster levels — all level equations resolve against
`averagePlayerLevel`, so a ~L20 character faces **full counts** (only the `_c`-tier roster
variants truncate via `minPlayerLevel`; softer composition, same density). *Caution, folklore not
database: the deepest SoT floors may sit behind a Skeleton Key gate. If the gate blocks you at
your level, the fallback fires — don't grind for the key.*

**D.2 — FALLBACK: the deepest ungated Steps of Torment floor, cleared fully on camera.** Same
dungeon family, same measured pool records, smaller waves. (Second fallback if SoT is somehow off
the table: Cronley's Hideout — folklore-dense but UNPROBED; your footage would be its first
measurement.)

**D.3 — THE RENDER EXHIBIT (no play needed — this is "represent that room in the sim + Godot"
at the absolute ceiling):** the SR Shard-33+ floor and/or Crucible tier-13 wave 06 are **fully
database-resident** — generated at runtime from parameters, so their placement counts are in the
`.arz` by necessity. We can build either in the battle simulator and render it with zero capture.
Proposed: **Crucible t13w06 as the deterministic sim room** (highest guaranteed floor in the game,
tight 35–36 band) and **SR Shard-33+ as the ceiling exhibit**. Your Window-2 SoT clear then
supplies the *campaign-referent* fixture — how a real dense room plays — while the DB-resident
rooms supply exact rosters.

**D.4 — Ceremony-5's role, sharpened:** since campaign placement is not in the database, **your
camera is the placement instrument** — the wide shot of the cleared room + the clear footage give
the actor count and room geometry the `.arz` cannot. (`Levels.arc` depot pull queued in
`matt_to_do/` to close this permanently; several-GB fetch, size-check first.)

---

# PART II — OUR SIDE: what KIT-CAL-2 + the dense room need built (so nothing is mysterious)

*This half is for the team, not for the keyboard. It is the pre-charter surface for the KIT-CAL-2
run and the dense-room render; the eventual charters bind at their own gates.*

## II.1 · The werewolf pipeline, mirrored

Save parse (measured build identity from day one) → pixel mining (HP series, tooltips, regime
segmentation; galadriel) → EoR kit spec → KIT-CAL-2 calibration battery vs the SAME Window-1
opposition as KIT-CAL-1 → Window-2 battery vs the dense-room roster → render. Read-only on the
save throughout.

**Endgame note (Matt's framing: "the chosen end game EoR Warlord build"):** the playtest fixture
anchors calibration at ~L15–20; the ENDGAME kit is then built the way the werewolf's rank-16 kit
was — **`.arz`-measured scaling to target ranks + the C2 build-guide gear**, validated against the
fixture's windows. We do not need Matt to grind to 100; we need the fixture + the datamine. If a
later high-level validation session is wanted, it queues separately.

## II.2 · Engine gap table — EoR Warlord kit vs surfaces that exist at HEAD (`28eddef4`)

| # | EoR/Warlord needs | Exists at HEAD? | Gap class |
|---|---|---|---|
| 1 | **Sustained channel delivery** — damage ticks while held, activation start/stop | Partial: attack-speed-less tick model (KIT-CAL-1); `beam_channel` in geometry vocab; FoI is the corpus's width-one `.arz` exemplar | **BUILD** — channel state machine (hold/release/dry-out) on the player arm |
| 2 | **Player-centered moving AoE circle** — spin radius resolves around the player each tick, player keeps moving | Spatial kernel expresses `circle`/`aura`; boss-side circles resolve; no player skill resolves self-centered-while-moving | **BUILD** — the resolver predicate + (per BR-2's G-1h law) telegraph fields that reconstruct it |
| 3 | **Continuous energy drain** — energy/s while held, regen race, Spirit scaling | Energy pools + regen exist (`combatant.py` `_ENERGY_CONFIGS`); per-press `energy_cost` held at canonical values | **EXTEND** — per-second drain + dry-out event; the duty cycle is a design dimension (feeds the discriminating-statistic grill item) |
| 4 | **Shield block** (Soldier) | `block_chance` on combatant + resolver rolls it; WR3 mitigation door forces 0.0 | **PARAMETERIZE + CALIBRATE** — un-force behind a door; block recovery cadence needs a probe |
| 5 | **Righteous Fervor** — default-attack replacer with charge stacks (Window 1 is fought with THIS, not EoR) | Melee default-attack channel exists (composed-value entry, stage-exempt) | **EXTEND** — charge-stack model; Window-1 fixture is accountable to RF |
| 6 | **Aura/passive buffs** (Presence of Virtue etc.) | Boss-side icearmor aura precedent; `aura` in geometry vocab | **EXTEND** — player-side persistent buff surface |
| 7 | **Multi-actor pack opposition** at dense-room scale | EXISTS: boss/champion/trash tiers, full-mix battery, `wr3_encounter_ai_v1` (M1/M2/M3) | **COMPOSE** — roster from the dense room's measured pools; arena footprint from Ceremony-5 footage |
| 8 | Retaliation | Explicitly unwired (fixture channels note) | **EXCLUDED by build rule §2.3** — stays out |

## II.3 · Emission needs — what drax must receive to render Window 2 faithfully

BR-2's standing laws govern: the telegraph describes the resolver's predicate (G-1h); liveness ≠
travel (R-BR-36); one scalar never carries two meanings; the pack supplies material, the trace
supplies geometry (R-BR-35); no field is asserted without a census line (R-BR-34).

1. **Channel records:** activation start/end events, per-tick damage events tied to the activation,
   `duration_s` = liveness of the hold, dry-out reason code (release vs energy-empty). The 10-hold
   probe is the fixture that proves the ledger counts what we say it counts.
2. **Spin geometry:** self-centered radius + tick cadence fields sufficient for an independent
   function to reconstruct hit/no-hit from the telegraph alone (the G-1h bar, applied to the
   player's kit for the first time).
3. **Energy series:** per-tick energy values for HUD binding — the ENERGY orb (R-BR-32) finally
   gets a moving number driven by a mechanic, not a constant.
4. **N-actor trace:** the schema already carries actors; the dense room stresses it — N spawn
   records, N death events (blood pools ×N per R-BR-33 lived-in ruling), champion tier flags.
   G-M4's dead-actor-widget discipline and the HUD target panel need an N-actor answer.
5. **Arena:** a second floor beside the crypt corner, footprint matched to the dense room's
   Ceremony-5 referent; CAM-LOCK + lighting cosmology inherited, not reopened.
6. **VFX material need-9 (the spin):** the 60-effect harvest has no spin-signature family; compose
   from `Aura` + trails or name the gap per G-13 coverage law — a silent substitution is the
   failure mode, not a gap.

## II.4 · Pre-playtest probe queue (fire BEFORE Matt plays; all read-only over the `.arz`/corpus)

| Probe | Question | Consumer |
|---|---|---|
| **P-D1 — LANDED** (`legolas/notes/2026-08-01-gd-pack-density-ranking.md`, commit `148bea76`) | Density ranking: SR Shard-33+ global winner (142.5–209.4/floor); Crucible t13w06 deterministic winner (35 min); SoT floor-5-wave-3 campaign winner (24–25). Two commission premises corrected (pool-vs-proxy fields; endlessdungeon placement recoverable) | §D — folded |
| P-E1 | `Skill_AttackRadiusSpin` template: tick cadence formula, radius, does rotation scale with attack speed, per-rank energy drain | Gap #1/#2/#3 spec |
| P-E2 | Righteous Fervor template: charge-stack mechanics, per-rank values | Gap #5; Window-1 kit spec |
| P-E3 | Soldier block: block chance/amount/recovery values on shields + Overguard | Gap #4 calibration |
| P-E4 | Dense-room pool → monster proto join: HP/damage tables for the chosen room's roster (the Primordian-proto pattern, applied to a crowd) | Gap #7 opposition build |

## II.5 · Open forks for Matt (ELICITOR ledger — rulings land in `matt_decision_needed/` if not
ruled at this doc's review)

- **F-V2-1 — the dense-room pick** (§D): rules when the probe table lands. Reachable target +
  fallback for this run; global-densest as render exhibit.
- **F-V2-2 — werewolf-referent prelude** (§1.8): merge into this sitting, or queue separately.
- **F-V2-3 — machine** (§1.7): PC or Mac — changes T11's pattern, nothing else.
- **F-V2-4 — endgame validation depth** (II.1): fixture+datamine only (lean), or queue a later
  high-level session.

---

*Filed as the KIT-CAL-2 substrate-capture protocol, v2. Desirable-run-pattern fit: the fixture
this produces is the bounded substrate; the werewolf fixture + constant Window-1 opposition make
Window 1 decidable; the measured dense-room roster + Ceremony-5 placement referent make Window 2
decidable. Probes P-D1/P-E1–E4 are the ELICITOR drain that keeps the eventual KIT-CAL-2 charter's
ARCHITECT gate clean. — gandalf, 2026-08-01*
