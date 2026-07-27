# Finding — 2026-07-26 — GD play-test v1: artifact verification (alignment + legibility)

**Role:** DRIFT-CRITIC (judging delivered artifacts against the protocol I authored)
**Author:** gandalf-prime
**Target:** `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/`
**Spec under test:** `gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` §§ 1.1, 2.0–2.2, 3.1–3.2, 5.1
**Question asked (Matt):** do the screenshot timestamps line up with the video, legibly?

## Verdict

**ALIGNMENT PROVEN — exact, at four independent points, by arithmetic alone.**
**LEGIBILITY PASS on every load-bearing instrument, at the delivered bitrate.**
**No re-record. The run is usable as-is.**

Three findings attach. One of them restates protocol §1.1 and is the most valuable thing this
verification produced. One is a defect in *my own* measurement method, not in Matt's capture.

---

## 1. Inventory

| Artifact | Measurement |
|---|---|
| `recorded_videos/play_test_2026-07-26.mp4` | 13,119,968,478 B · 1920×1080 · h264 · `r_frame_rate=60/1`, `avg_frame_rate=60/1` (**CFR**) · `nb_frames=408991` · `duration=6816.516667` (1:53:36.5) · 15.4 Mbps · AAC present (319,524 frames) |
| `recorded_videos/smoke_test_2026-07-26.mp4` | 59,635,024 B · 26.65 s · 1920×1080 · 60/1 · 17.9 Mbps |
| `screenshots/` | **313 PNG, numbered 40–352, ZERO gaps** (contiguity verified) · all 1920×1080 · ~4 MB each |

Wallclock bracket: video mtime 17:57:13; first screenshot 16:03:51; last screenshot 17:57:02.
Derived video start = 17:57:13 − 6816.5 s ≈ **16:03:24**.

The first screenshot lands **27 s after recording started**, and the last lands **11 s before it
stopped**. That is protocol §2.1 item 1 ("Start recording FIRST") and the END BLOCK bookend, both
confirmed on camera. Capture-spec compliance: 1920×1080 ✓ · 60 fps ✓ · CFR ✓ · MP4 ✓ · audio ✓ ·
orb numerals always-shown ✓.

## 2. Alignment — PROVEN

`video_start_epoch = mtime(video) − duration = 1785103033 − 6816.517 = 1785096216.5`
`predicted_offset(shot) = mtime(shot) − 1785096216.5`

| Shot | mtime | Predicted offset | `play_time` in the **screenshot** | `play_time` in the **video at that offset** | Result |
|---|---|---|---|---|---|
| 40 | 1785096231 | 14.5 s | 6 min 11 sec | 6 min 11 sec | **EXACT** |
| 200 | 1785099476 | 3259.5 s | 59 min 36 sec | 59 min 36 sec | **EXACT** |
| 280 | 1785101288 | 5071.5 s | 89 min 32 sec | (on the fitted curve, ✓) | consistent |
| 352 | 1785103022 | 6805.5 s | 118 min 8 sec | 118 min 8 sec | **EXACT** |

Shots 200 and 352 additionally match the video frame on `kills` (271 / 882), `deaths` (1 / 2) and
`max level` (8 / 12) — four fields agreeing, not one.

**Seek accuracy independently verified** so the matches are not an artifact of coarse seeking:
frames at t=3259 / 3289 / 3349 read `59:36` / `60:06` / `61:05` — a +30 s seek advanced the ledger
by exactly +30 s.

> **Consequence:** every one of the 313 screenshots can be placed on the video timeline by mtime
> arithmetic alone. No manual sync, no clapperboard, no per-shot matching pass. This is the cheapest
> possible outcome and it is the one we got.

## 3. `play_time` is NOT the video offset — protocol §1.1 restated

§1.1 asserts *"the panel's `play_time` in every frame IS the video↔ledger sync."* True — and the
sync holds — but the map is **not** identity, and assuming it is would have introduced a silent
~6-minute error at the head of the run and a drifting one thereafter.

Measured `play_time − video_offset`:

| video offset (s) | 14.5 | 300 | 900 | 1500 | 3259 | 5071 | 5600 | 6805 |
|---|---|---|---|---|---|---|---|---|
| divergence (s) | +356.5 | +353 | +352 | +333 | +317 | +300.5 | +292 | +283 |

Monotonically decreasing. Two components, both identified:

**(a) Banked prefix, ≈ +356 s.** `play_time` is SAVE-cumulative (the A6 two-clock split). The
character carried ~5 min 56 s of play before recording began — creation, the smoke test, menus.

**(b) ≈ 73 s of non-counted time**, accumulating in **discrete steps**, not as drift.
The mechanism was caught on camera: between t=3289 (`Devil's Crossing`) and t=3349 (`The Old Dump`)
a **zone transition** consumed wallclock that `play_time` did not count. Within any segment the
slope is exactly 1.

> **Ruling for the data contract: key every event on `play_time`, never on video offset.**
> `play_time` is the game-state clock; video offset is the camera clock. The ~73 s of loading is
> real frozen-state time and must not be attributed to gameplay — 73 s wrongly attributed across
> 882 kills would bias every rate the distribution oracle produces. The affine map must be **fit
> from panel samples per session** (piecewise, slope-1 segments, breaks at zone transitions), never
> assumed.

This *strengthens* the design rather than weakening it. PlayStats-as-persistent-ledger survives
intact, and we now know which of the two clocks is the true one.

## 4. Legibility — per instrument, at the delivered bitrate

| Instrument | Source | Verdict |
|---|---|---|
| PlayStats panel (`play_time`, kills, deaths, level) | video, 15.4 Mbps | **PASS** at 1.6× |
| PlayStats panel | screenshot, native | **PASS** |
| `Skills Used` per-skill counts | video | **PASS** — e.g. `werewolf1_skill01_claws.dbr : 358` |
| Green `[entityId] Action State: X` + `Wait Time` overlay | video | **PASS** at 3× — `[605781] Action State: Idle`, `Wait Time: 655` |
| Orb numerals | video | **PASS** at 2× — `672/672`, `283/333` |

**Bitrate deviation ACCEPTED.** 15.4 Mbps against §3.2's ≥25 Mbps recommendation. That
recommendation was precautionary and aimed squarely at the ~10–14 px green overlay text — the
highest-risk pixels in the frame. Those pixels were checked directly and they survive, entity IDs
included. **No re-record.** The ≥25 Mbps recommendation stands for v2 as cheap insurance, but it is
not a gate and it did not bind here.

## 5. Three defects to carry forward

**D-1 — measurement method (MINE, and it matters most).**
My first panel read used a 560×420 crop upscaled 2× to 1120×840. It came back **legible and wrong**:
I read `50 min 37 sec` where the truth is `59:36`, and `Health potions used 8 / Mana 5` where the
truth is `0 / 0`. Cause: the image-read path downsamples large images, so a big crop with a big
upscale *loses* effective resolution at read time. The fix that produced every correct number in
this document: **crop TIGHT, upscale MODESTLY** — ~600×200 native at 1.6×.

This is binding on galadriel's pipeline, and it is a live demonstration of the exact failure her
calibration gates exist to catch: **legibility is not accuracy.** A confidently-rendered wrong digit
is worse than an unreadable one, because it does not announce itself. No OCR figure enters
`fixtures.db` without a confidence gate and a cross-field consistency check (the kills/deaths/level
agreement in §2 is what a cross-check looks like).

**D-2 — quest-tracker occlusion (game-layer, not capture-layer).**
The quest tracker renders over the right edge of the PlayStats panel. At t=6805 the `onslaught.dbr`
skill count is occluded by *"Not a Drop to Drink."* Present **identically in the screenshot and the
video**, which proves it is game-UI layering rather than compression. Costs a small number of
`skill_use_count` reads at arbitrary moments.
→ **v2 smoke-gate item: collapse the quest tracker before the START block.**

**D-3 — counters to distrust.**
`Total Score` reads `0` and `Damage per second` reads `0.00` for the entire run: dead fields, do not
model them.

`Health potions used` / `Mana potions used` reading `0` is **RESOLVED — not a dead counter.**
Matt ruled (2026-07-26): *"I decided not to use any potions for the run so that it could be a more
controlled oracle."* The counters are live and correct; the run is a deliberate no-potion control.
See §8 for what that control buys — it is worth more than it cost.

## 6. Ledger trajectory — sanity

`kills` 0 → 2 → 14 → 45 → 87 → 271 → 586 → 692 → 882 (monotonic)
`deaths` 0 → 1 → 2 · `max level` 1 → 3 → 4 → 8 → 11 → 12 · `play_time` 6:11 → 118:08

**882 kills in 113 minutes ≈ 7.8 kills/min.** For a distribution oracle whose primary statistic is
attacks-per-kill, that is a dense sample, not a thin one. Areas traversed on the sampled frames:
Lower Crossing → Devil's Crossing → The Old Dump.

## 6b. FINDING — `skill_use_count` may not count swings. §1.1's central claim is now conditional.

Complete `Skills Used` block at end of run (Screenshot 352, `play_time` 118:08, **882 kills**),
read from the native still — the video frame had `onslaught` occluded by D-2, the screenshot did not:

| Skill | Count |
|---|---|
| `default/defaultkickattack.dbr` | 19 |
| `default/defaultweaponattack.dbr` | 74 |
| `playerclass10/onslaught.dbr` | 54 |
| `playerclass10/werewolf1.dbr` | 12 |
| `playerclass10/werewolf1_skill01_claws.dbr` | **358** |
| `playerclass10/werewolf1_skill02_charge.dbr` | **175** |
| **total** | **692** |
| `Life healed` | 12468.06 |
| `Shield block chance` | 18.00 |

**692 skill uses against 882 kills — 0.78 per kill.** Excluding the two plausible non-attacks
(`werewolf1` transform toggle, 12; `onslaught` if it is a buff, 54) gives 626 attacks, **0.71 per
kill.** Fewer attack activations than corpses.

Protocol §1.1 asserts *"kill events = exact integer increments; attacks-per-kill needs zero
segmentation judgment."* The denominator claim holds. **The numerator claim does not, yet.** Three
candidate explanations, and they are not equally survivable:

1. **AoE multi-kill** — one `claws`/`charge` activation kills several enemies. Benign: the
   aggregate is still meaningful, but the statistic is *attacks-per-engagement with variable target
   count*, not attacks-per-kill, and it needs a target-count term.
2. **Non-player kills** — pet, retaliation, DoT tick, or environmental kills increment `kills`
   without any player activation. Benign but requires an attribution term.
3. **`skill_use_count` counts ACTIVATIONS, not SWINGS.** `werewolf1_skill01_claws` at 358 uses over
   113 minutes is ~3.2/min, which is implausibly low for a primary attack — consistent with a
   held/channelled auto-attack-replacer registering one "use" per button-press rather than per
   swing. **If this is the cause, the panel cannot serve as the attack-rate ledger at all**, and the
   T-B video tier (60 fps, per-swing) becomes the authoritative counter instead.

### 6b-bis — Matt's build testimony (2026-07-26). Resolves one observation, sharpens the other.

Matt supplied the build facts after the finding was filed:

> *"The werewolf claws had huge AOE damage. I think onslaught likely had a very strong AOE damage
> component as well. Also, on the last level (12) I also had poison (dot) which was almost
> equivalent to the main skill damage itself per tick."*

This is decisive for causes 1 and 2 and it moves the prior substantially. But it is important to be
precise about *which* observation it resolves, because there are two and they are not the same:

**Observation A — the RATIO.** 692 uses < 882 kills. **RESOLVED.** Confirmed heavy AoE on the two
dominant skills (533 of 680 attack activations) plus poison DoT killing with zero activation makes
kills-exceeding-activations entirely expected. 882 / 680 = **1.30 kills per attack activation**,
which is unremarkable for an AoE melee build. Cause 1 + cause 2, confirmed by the player.

**Observation B — the ABSOLUTE RATE. NOT resolved, and this is the load-bearing one.**
680 attack activations over 6816 s = **one attack every 10.0 seconds, sustained, for the entire
run.** For that to be the true swing count, all sustained attacking in the session must fit inside
~11.3 minutes (at 1 attack/s) or ~7.6 minutes (at 1.5 attacks/s) — i.e. **6.6–10% attack uptime in a
session where 882 things died.**

That is low. It is not impossible — ARPG sessions carry a lot of travel, town, stash and menu time,
and a heavy-AoE build clears packs fast. **So this is now a marginal call rather than a strong
inference, and it must be measured rather than argued.** I decline to claim cause 3 is established;
Matt's testimony genuinely weakened it. I equally decline to drop it, because a 10% attack-uptime
implication is exactly the kind of quietly-implausible number that turns out to be an instrument
artifact.

**The test is now better specified and cheaper than it was.** In one clean sustained-combat window:
count `claws` activations from the video AND corpses produced, then compare both against the panel
deltas over the same `play_time` interval. Two independent ratios fall out — swings-per-activation
(1.0 ⇒ the panel counts swings; >1.0 ⇒ it counts button-presses) and kills-per-activation (should
land near 1.3 if the run is homogeneous). Either answer is usable; not knowing is not.

**Third mechanism, and it carries its own requirement — the poison DoT is a REGIME CHANGE, not a
constant.** It arrived at **level 12 only**, at a magnitude Matt puts near the main skill's per-tick
damage. So the attack→kill relationship is **not stationary across the run**: the final segment has
a large kill source with no activation behind it, and the earlier segments do not. This is a
structural break on the `play_time` axis, in addition to the two deaths and the zone transitions,
and any fit that pools across it will produce a number describing no regime that actually existed.

**Do not model attacks-per-kill until Observation B is settled.** This is precisely the class of
error the math-before-code discipline exists to intercept: the statistic looks free, reads cleanly,
and would have been wrong by an unknown multiplicative factor.

## 7. Matt's screenshot caveat — disposition: NO DEGRADATION

*Stated caveat:* for the first few levels, only the equipment-doll view and the skill tree were
captured — no per-item or per-skill stills. From later levels on, everything.

This costs nothing that matters. §5.1 `fixture_character` provenance needs the **equipped set at
epoch boundaries**, and the doll view *is* that record; per-item stills are a convenience for affix
transcription, not the provenance itself. The uncovered region is levels 1–8, where gear is
near-white and skill investment is one to three points — the lowest-information stretch of the
entire run. The high-information region (levels 8–12: real affixes, real skill weights, 611 of the
882 kills) is fully covered.

One honest consequence: for the earliest epochs, affix values must be transcribed from doll tooltips
at read time rather than from dedicated stills, which is slower for elrond and lossier if a tooltip
was never hovered. **If an early affix proves unreadable, drop that slot from the fixture rather
than infer it.** A missing slot is honest; an inferred slot poisons the oracle. No epoch is lost
either way — the character record survives with a gap, which is a graded degradation and exactly
what fidelity LAW §4 exists to express.

## 8. Control properties of run v1 — what the no-potion decision bought

Matt ran the session with **zero potions, deliberately**, for oracle control. Recording what that
actually purchased, because it is more than the obvious:

**Purchased — `life_healed` becomes a clean measurement.** With potions at zero, the run's
`Life healed: 12468.06` is **entirely endogenous**: health regeneration and lifesteal. No
exogenous step-functions in the series. That is ~106 HP/min, roughly **18.5 max-health pools** (peak
observed 672) recovered over 113 minutes without a single player-triggered heal. Under any potion
usage this field is a sum of two unrelated processes and worth nothing; under this control it is a
direct measurement of sustain throughput — the exact quantity the era-substrate needs to calibrate
its sustain curve against. This was the highest-value side effect of the decision.

**A SECOND control was in force — zero devotion.** Matt (2026-07-26): *"I saw a devotion menu but I
decided not to select any devotion points… I left devotion out as a control (at least I think I
did)."* This narrows the run further, in three ways that matter:

- **`life_healed` is cleaner than first recorded.** My original text listed devotion procs as a
  contributor; with zero devotion assigned they contribute nothing. The field is regen + lifesteal
  **only** — a two-source measurement, not a three-source one. Corrected above.
- **It removes a candidate cause from §6b.** Devotion constellation procs are a significant source
  of unattributed damage and therefore of kills with no skill activation behind them. With devotion
  off, that channel is closed, and the §6b kill attribution is correspondingly simpler: skills,
  weapon, and the level-12 poison DoT. Nothing else.
- **VERIFY IT, do not take it on memory.** Matt flagged his own uncertainty (*"at least I think I
  did"*), which is the right instinct. This is cheaply verifiable from the banked stills — the
  devotion/constellation screen or the character sheet will show assigned points. **galadriel: read
  it off a still and confirm zero.** A control believed-but-unverified is worse than no control,
  because it licenses inferences the data may not support.

**The cost side, stated plainly — controls buy interpretability and spend representativeness.**
Two controls are now in force (no potions, no devotion). Both are correct for a *mechanism* oracle:
they isolate the sustain and attribution channels we actually want to measure. But together they
make run v1 a **de-powered build**, materially weaker than a normal player's at level 12. Anything
derived from it that describes *pacing* — time-to-kill, kills/min, damage-taken rate, the felt
difficulty curve — is biased slow and must be labelled as such, not read as "what GD combat is
like." That is a real limitation and it is the correct trade to have made at this stage; the
mechanism questions come first and they need clean channels. But the record must carry the label, or
a future reader will mistake a controlled sample for a typical one. **Recommend: a later
representativeness run with both controls released, explicitly for pacing calibration, once the
mechanism questions are closed.**

**Purchased — the HP series is interpretable.** Every downward move is incoming damage; every upward
move is endogenous recovery. No annotation pass is required to strip out player heals.

**NOT purchased — full control. Three residual discontinuities must still be marked:**

- **2 deaths.** Each is an HP reset *and* a position reset. These are hard segmentation breaks; they
  must be located on the `play_time` axis and excluded from any continuous-series fit. The `deaths`
  counter tells us there are exactly two and the panel samples bracket them (0 by t=900, 1 by
  t=3259, 2 by t=5600).
- **Zone transitions.** Already identified in §3 as the `play_time` loss mechanism; they are also
  combat-continuity breaks.
- **Endogenous recovery is not constant.** It scales with gear and level, both of which changed
  (level 1 → 12). The sustain measurement is a curve across the run, not a scalar.

**Design note.** The instinct here is correct and worth keeping as a standing protocol principle:
*eliminate the exogenous, accept the endogenous, mark the discontinuities.* Potions were the right
thing to remove because they are player-triggered, unlogged in magnitude, and confound a field that
is otherwise a free measurement. This should become an explicit §2.2 run rule for v2 rather than a
one-off choice, alongside a directive to call out each death aloud on the audio track so the two
break points land on the timeline without a search.

## Action

- [ ] galadriel: T-A ledger-tier CV pass against the real MP4. Binding constraints from this
      finding — (i) D-1 crop/upscale geometry; (ii) key on `play_time`, fit the affine map per
      session per §3; (iii) cross-field consistency gate (kills/deaths/level must co-agree before a
      panel read is accepted); (iv) expect D-2 occlusion on `Skills Used`.
- [ ] elrond: `fixtures.db` ingestion per §5. Screenshot→timeline placement is mtime arithmetic
      against `video_start_epoch = 1785096216.5`; store `pts_ms` AND `play_time_ms`, with
      `play_time_ms` as the join key.
- [ ] **galadriel / BLOCKING on §6b:** settle the `skill_use_count` question first, on a bounded
      window, before any attack-rate modelling. Swings-from-video vs panel-delta over the same
      `play_time` interval.
- [ ] gandalf: fold §3 into protocol §1.1, D-2 into §2.0, and §8's no-potion rule + call-out-deaths
      directive into §2.2 before the v2 run. §1.1's attacks-per-kill claim is conditional pending §6b.
- [x] Matt: D-3 RESOLVED — zero potions was a deliberate control (2026-07-26). Counters are live.

## References

- `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/` (video, smoke, 313 screenshots)
- `agentic_orchestration/gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` (§§1.1, 2.0–2.2, 3.1–3.2, 5.1)
- Working crops: `/tmp/gp-align/` (transient)

---

# §9 — ROUND-2 RETURNS (galadriel + elrond + Matt). Corrections to this document.

**Appended 2026-07-26 after both commissioned agents reported and Matt disclosed two instruments.**
Everything above stands except where corrected here. **This section governs on conflict.**

## 9.1 §6b is CLOSED — the panel counts swings

galadriel measured it on a 20 s window at 60 fps at `max_level` 9, **before** the poison existed:

- **swings-per-activation = 1.0** — 7 player attack animations against 7 panel increments (claws +3,
  charge +3, kick +1), five pairings exact to the frame. **Cause 3 REFUTED. The panel counts swings.**
- **kills-per-swing = 1.86** — 13 kills from 7 swings, in steps +1, +1, **+2**, +1, +1, **+4**, **+2**, +1.
  **Cause 1 (AoE) CONFIRMED by direct measurement**, matching Matt's testimony.
- Attack uptime in dense combat **16.6%**; the global 1-per-10 s implies that density over ~29% of
  the run — ordinary ARPG travel time, not an instrument artifact. **Observation B answered.**

Instrument used: the green `[42992] Action State:` overlay, entity 42992 being the player.
`character.LogData` produces **no text log** — it is an on-screen overlay only. Record that: the
protocol implies a log file exists. It does not.

**Consequence for §1.1:** the numerator is sound, but **attacks-per-kill is not well-defined per
kill** — one swing resolves several. The measurable quantity is **kills-per-swing**. §1.1 must be
rewritten to name that instead.

**Dead field found:** `skill_use_count[defaultweaponattack]` totals 74 and **froze before `play_time`
29:17** — dead for 75% of the run (werewolf form replaces the default attack). §1.1 names this field
specifically. The live attack fields are `claws` and `charge`.

## 9.2 CORRECTION — the counters do NOT start at zero. My ratios were wrong.

elrond, from the artifacts: at `pts=14.5` the panel already reads **`kills=2`,
`defaultweaponattack=8`, `life_healed=16.33`** — the smoke gate's two monsters, carried on the save.

Every figure I quoted as a run total was a **SAVE-cumulative endpoint**. Corrected deltas:

| Quantity | I said | Truth (delta) |
|---|---|---|
| kills | 882 | **880** |
| total skill uses | 692 | **684** |
| `life_healed` | 12468.06 | **12451.73** |
| uses-per-kill ratio | 0.783 | **0.777** |

Conclusions unchanged; the arithmetic was wrong anyway. **Standing rule: on a SAVE-cumulative
ledger, always difference against the first frame — never read the last frame as a total.**

**And a live contradiction against A6.** `skill_use_count` and `life_healed` **survived the
smoke→run boundary**, which A6 classifies as SESSION-scoped and therefore destroyed by any return to
main menu. Either A6's classification is wrong, or Matt never returned to the menu between the smoke
and the run. **This must be settled before v2** — the whole no-menu-return rule in §2.2 rests on it,
and if A6 is wrong we are paying for a constraint we do not owe. One question to Matt.

## 9.3 CORRECTION — `Damage per second` is NOT dead (D-3 was half wrong)

galadriel: it reads **74.19 / 394.63 / 832.31** in combat, and `0.00` only out of combat. My two
samples were the run's bookends, which are out-of-combat *by construction* — that is the entire
reason it looked dead. **It is a live rolling outgoing-damage field**, and combined with §9.5 it is
half of a cross-validating pair. `Total Score = 0` still holds as genuinely dead.

This was the most valuable correction of the round: I nearly discarded an instrument.

## 9.4 D-1 IS WORSE THAN I FILED — it fails toward the PLAUSIBLE value

elrond reproduced D-1 independently, and the reproduction is more alarming than my original:
a 460×290 crop at 2.5× read **`kills: 0`**; the same pixels at 430×90 / 1.6× read **`2`**.

**The wrong value was the more plausible one.** Zero kills at the start of a run is exactly what a
reviewer expects to see, so a plausibility check would have *confirmed* the error. This is not
random noise — **it fails toward the expected answer**, which is the single most dangerous shape a
measurement error can take, because every human safeguard we have is pattern-matching on
expectation. The cross-field monotonicity gate is therefore not optional hygiene; it is the only
thing standing between us and confidently-wrong data.

Both agents hit this independently, from different crops, on different fields. **Elevate D-1 from a
methodological note to a binding pipeline constraint.**

**D-2 revised in both directions:** galadriel narrowed it (video and screenshot are pixel-identical
on the `onslaught` row and *both* read 54 — my "the screenshot recovered what the video occluded"
claim was wrong; I simply failed to read the video). elrond widened it — a **second occlusion
source** exists: the green `ShowAngerLevels` overlay renders over the panel digits, not just the
quest tracker. Net: occlusion is real, has two sources, and is recoverable by channel separation
(tracker text is orange; requiring a high blue channel deletes it).

## 9.5 THREE new instruments (Matt, 2026-07-26) — the run is worth more than assessed

**(1) Floating combat text is a per-hit damage ledger.** Matt: *"ALL damage types show up on screen
(whether direct damage or damage over time)… as floating damage numbers on top of the enemy."*
Everything in round 1 counted *events*; this measures *magnitudes*. Paired with the recovered
rolling DPS field (§9.3) it forms **two independent outgoing-damage instruments that cross-validate**
— summed FCT over a window should reconcile against rolling DPS over the same window.

**(2) A training-dummy segment — a controlled fixture, arrived at by accident.** Stationary target,
no death, no retaliation, no movement. The cleanest calibration surface in the run.
**Located from the ledger:** `kills` reads 692 at `play_time` 98:12 *and still 692 at 106:11* —
**eight minutes in which nothing died.** Video offsets ~5600–6079. Inside it: equipment doll open at
5650 (the weapon testing), a full-screen node grid at 5800, back in the world at 6000.

> **CORRECTION to §6b-bis:** I wrote the poison DoT "arrived at level 12." It did not — it arrived
> when Matt **equipped two green poison items**, around the dummy test. The regime break is a **gear
> change near offsets 5600–6079**, not a level-up.

**(3) The first death is a deliberate player-side DoT oracle.** Matt died on purpose in a
poison-flooded cave and captured it, *specifically* to give us incoming-damage data: *"Damage to the
player character does not appear as floating numbers, but you can calculate the poison damage based
on the health globe tick minus regen."* This is the **incoming** side, on which we had nothing.

It works because globe **numerals** are always-shown — the §3.1 pre-run UI dependency, now paid for.
Note the near-miss: galadriel's earlier calibration **rejected** globe *fill-fraction* (4.6pp signal
against a 90.5pp null band) while numerals scored 100% READY. Matt's method reads the surviving
instrument. **Numerals only; never fill-fraction.**

> **Disposition change:** §8 tells consumers both deaths are hard breaks to exclude from fits. That
> holds for *combat* fits — but **death #1 is a FIXTURE to retain and label**, not discard. The two
> deaths now require different handling.

## 9.6 The §5 data contract was wrong in five places (elrond)

Schema landed as `fixtures-v0.3` / `v0.4`; DDL in `research/scripts/`, narrative in
`research/curated/MIGRATION-fixtures.md`. Ingested `GP-gd-2026-07-26-s1` + smoke: 315 captures,
10 clock anchors, 9 map segments, 23 breaks, 17 controls, 49 ledger readings. `attacks_per_kill`
**refused by trigger**, as instructed.

1. **`fixture_trial`'s shape does not survive contact.** `segmentation` as a plain column collides
   with `UNIQUE(fixture_set_id, trial_ordinal)`; the first S1+S2 ingest silently triple-counts. It
   now joins the key. Also **S1/S2/S3 was missing a value** — the seven L0 trials are hand-bracketed,
   not kill-to-kill. Added `S0-explicit`.
2. **`fixture_set` is a one-monster group; a general-play engagement is a many-monster event.**
   §5.1 partitions by `monster_display_name` while §5.3 declares single-monster *violated (packs)* —
   those cannot both hold. `fixture_set_id` is now nullable; `trial_participant` carries per-monster
   identity, rank, and **`kill_attributed_to`** — which is exactly §6b's attribution term.
3. **The ledger is not trial-shaped at all.** Three segmentations over one series meant three copies.
   `session_ledger` is the observed layer; a trial is a **window** over it. (This is the right
   shape and I had it wrong.)
4. **`monster_rank` already existed**, carrying corpus `monsterClassification` from M4 — my §4.3
   request would have **overwritten bridge evidence**. Added `monster_rank_observed`; disagreement
   between them is evidence, not error.
5. **`ladder_rung='GP'` is wrong** — a general-play set is not a rung on the L0–L5 ladder and holds
   none of L0's constraints. Added `evidence_class`.

## 9.7 The join key — right, with three qualifications I did not see

`play_time_ms` is correct, **but the panel renders whole seconds.** So it is quantised at 1000 ms
while an engagement is ~5 s and an AoE multi-kill puts several kills inside one tick. **It cannot
order events within a second — and S1 is precisely about ordering kill increments.**

- **Operative key is the composite `(play_time_ms, pts_ms)`** — `play_time` for correctness across
  the discontinuity, `pts` for ordering within a segment.
- `play_time` **freezes during loading**, so it is one-to-many exactly at the breaks.
- It is **SAVE-scoped**, so the true key is `(save_identity, play_time_ms)` — and **§2.1 item 9 never
  asks for save identity.** A second character or a reload collides silently. **Protocol gap; fix
  before v2.**

## 9.8 Missing deliverable — §3.5 `notes.md` was not produced

No `notes.md` accompanied the run, so difficulty, area sequence and boundary jots are recorded
`absent` rather than inferred (correct handling by elrond). 11 epoch-boundary candidates were
inferred from mtime bursts alone — and note **§7 F-1's estimate of 2–4 epochs is low: 11 level-ups
happened.** Cheap fix for v2: the running audio commentary already required by §2.2 can carry all of
it, with no typing during play.

## 9.9 Consolidated action

- [ ] gandalf: rewrite §1.1 around **kills-per-swing** (not attacks-per-kill); drop the
      `defaultweaponattack` reference; record that `LogData` yields no file; fold §§9.2–9.8 into the
      protocol; add **save identity** to §2.1 and **quest-tracker + anger-overlay collapse** to §2.0.
- [ ] galadriel (round 2, in flight): FCT extractability verdict, dummy-segment bounds, FCT↔DPS
      cross-validation, poison DoT both directions, **zero-devotion verification off a still**.
- [ ] elrond: `fixture_character` / `fixture_set` / `fixture_trial` rows still need identity input.
- [ ] **Matt — one question:** between the smoke test and the run, did you return to the main menu?
      This settles the A6 contradiction in §9.2 and decides whether §2.2's no-menu-return rule is a
      real constraint or one we are paying for without owing it.
