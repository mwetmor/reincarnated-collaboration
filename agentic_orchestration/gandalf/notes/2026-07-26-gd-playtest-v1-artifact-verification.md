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

**The apparent A6 contradiction — RESOLVED, but read the resolution carefully.**
Matt (2026-07-26): *"I never went back to the main menu after the smoke run."* So the smoke and the
run are **one A6 session**, the counters carrying over is exactly what A6 predicts, and there is no
contradiction. elrond's differencing against the first frame was the correct handling.

**But A6 is now confirmed UNVIOLATED, not confirmed TRUE.** We have evidence that we never tested
the rule — a different epistemic state from evidence that the rule holds. The no-menu-return
constraint in §2.2 is currently carried on trust.

**That constraint is expensive and it is cheap to test.** It forces a general-play run to be a
single unbroken sitting; v1 was 113 minutes. If A6 is wrong, runs may be **split across sittings**,
which makes longer runs feasible and v2 far easier to schedule. The experiment takes ~60 seconds and
does not belong inside a run: note `skill_use_count`, return to the main menu, reload, re-read.
Zeroed ⇒ A6 holds and the rule is real. Unchanged ⇒ **drop the constraint.** Either answer is worth
more than the minute it costs.

**Better — make the rule AUDITABLE rather than obeyed (recommended, lands regardless of the
experiment).** `skill_use_count` and `life_healed` are strictly non-decreasing *within* a session.
Add them to the cross-field monotonicity gate: **a drop in either is a menu-return detector.**

Note the existing gate would NOT have caught this by itself — `play_time` and `kills` are
SAVE-cumulative and survive a menu return untouched, so **only the session-scoped fields carry the
signal.** The gate as specified is blind to precisely the event it most needs to see.

With that gate in place the run self-reports the break: if the rule is broken in a future run we
learn exactly where and segment around it, instead of silently losing two fields and never knowing.
**A rule a human must remember is a rule that will eventually be broken unobserved; a rule the data
enforces is not.**

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
- [x] **galadriel (round 2) — RETURNED 2026-07-26.** FCT verdict, dummy bounds, dps-integral
      substitute for the failed cross-validation, player-side poison DoT, T-A close. Devotion still
      OPEN; dummy-side DoT NOT MEASURED. **See §9.11 — it governs over §9.10 and §5 on conflict.**
- [ ] elrond: `fixture_character` / `fixture_set` / `fixture_trial` rows still need identity input.
- [x] **Matt — ANSWERED 2026-07-26:** no menu return after the smoke. A6 is unviolated, not
      verified; smoke + run are one session. See §9.2.
- [ ] gandalf/galadriel: add `skill_use_count` + `life_healed` to the monotonicity gate as a
      **menu-return detector** — the gate is currently blind to the one event it must catch.
- [ ] Matt (~60 s, OUTSIDE any run): note `skill_use_count`, return to main menu, reload, re-read.
      Decides whether §2.2's single-unbroken-sitting constraint is real or can be dropped — and
      dropping it would let v2 runs span multiple sittings.

## 9.10 THREE regimes, not two — and a correction back to galadriel

**galadriel, round-1 follow-up:** at `play_time` **29:17** both `defaultweaponattack` (74) and
`onslaught` (54) **froze and never moved again.** From that point the run is essentially **two
skills** — `claws` and `charge`.

This is a **build-identity transition**, not a data artifact: it is almost certainly the point at
which the werewolf transform became the character's operating mode, taking the default attack and
`onslaught` off the table. It is the moment the character became its build.

**So any pooled fit spans at least THREE regimes:**

| Regime | Bounds (`play_time`) | Attack surface |
|---|---|---|
| R1 | 6:11 → 29:17 | weapon attack + `onslaught` + `claws` + `charge` |
| R2 | 29:17 → poison-gear equip (~video 5600–6079) | `claws` + `charge` |
| R3 | poison-gear equip → 118:08 | `claws` + `charge` + poison DoT |

My non-stationarity caution in §6b-bis is therefore **doubly** load-bearing: the DoT break sits on
top of a build-shape break 90 minutes earlier. Pooling across all three produces a number describing
no regime that ever existed.

**Open question for the data (do not assume):** `werewolf1` shows **12 transforms**, yet no
non-transformed attack is recorded after 29:17. Does R2/R3 contain any out-of-form combat at all? If
not, the 12 are re-casts after deaths and zone changes, and the transform is effectively permanent
from 29:17 — which makes R2/R3 a *cleaner* fixture than expected.

### Correction back to galadriel — refinement 1 double-subtracts

She writes: *"You compute 882/680… That denominator includes `onslaught` (54) and `werewolf1` (12).
Excluding it gives 668."*

**680 already excludes the transform toggle.** 19 + 74 + 54 + 358 + 175 = **680**; adding
`werewolf1`'s 12 is what makes the panel total **692**. Subtracting 12 from 680 removes it twice.

Her substantive point is right and was already applied. Authoritative arithmetic, with elrond's
smoke-prefix correction (§9.2) folded in:

| Quantity | Value |
|---|---|
| panel total, all rows | 692 |
| attack activations (excl. transform toggle) | 680 |
| less smoke prefix (8 `defaultweaponattack`) | **672** |
| kills delta | **880** |
| **kills per attack activation, whole run** | **1.31** |

Against her **1.86 measured in a dense-pack window at `max_level` 9**. Both are correct and the gap
is the point: dense-pack combat clears ~1.9 per swing, the run averages ~1.3 because it also
contains single-target fights and travel. **Two numbers, two different questions** — do not let the
run-average silently stand in for the engagement figure.

Her refinement 2 stands and is load-bearing: **1.86 was measured pre-DoT**, so AoE alone carries the
ratio. The DoT makes R3 higher still; it does not explain R1/R2.

**Discipline note.** Both of us have now been caught in arithmetic by the other inside one cycle, on
top of two independent D-1 reproductions. That is the review structure working as designed, and it
is a standing argument against accepting any single-source figure into `fixtures.db` — including
mine.

---

# 9.11 ROUND-2 RETURNS — galadriel (2026-07-26)

> **Governs over §5, §9.10 and my own §6b-bis on any conflict.** Two corrections to me are recorded
> in-line. One correction back to galadriel is recorded in §9.11.4 — the closure residual is a
> denominator artifact, not physics, and the number is *better* than she reported.

## 9.11.1 FCT — READY as a sampler, NOT-READY as a ledger, and we built the confound ourselves

Matt's description is exactly right and is now verified on both instruments: near-white,
low-saturation, dark-outlined numerals over the target, legible at native. Glyph height **9–24 px**;
a number spawns small, *grows* to peak over ~0.5 s, then fades. It is per-**target** and per damage
**component** — at pts 6001.3 two numbers (384, 372) land on one dummy inside 0.2 s.

**Verdict split.** READY as an **assisted magnitude sampler** (a human or a targeted read pulls
individual magnitudes). NOT-READY as an **automated per-hit ledger**, for three measured reasons:

| Failure | Measurement |
|---|---|
| Detector has no discriminating feature | bright+achromatic detector returns **298 candidate tracks in a 10 s window** against a true count of order 10–30; wet-rock specular and torchlight share FCT's colour, size and transience |
| Self-inflicted occlusion | the green `character.LogData` overlay renders **in the same region at the same glyph height** as FCT spawns |
| Overlap and no colour channel | at pts 6046.60 three numbers land together, only the topmost (`449`) survives; a saturated-pixel census over the whole dummy window found green, red, **8 yellow pixels**, nothing else — **no colour coding, so direct and DoT cannot be separated** |

The second row is the one that stings: the overlay we turned on to instrument the run is the thing
occluding the instrument we most wanted. This is the **third** distinct occlusion finding of the
cycle (D-2 skill-panel, elrond's anger-overlay-over-digits, now this), and all three share one cause
— *debug overlays are additive to the frame, and the frame is the instrument.*

**The third-row consequence is the design-relevant one.** Grim Dawn's FCT does **not** colour-code
damage type. Any Reincarnated-side design that assumes "read the numbers to attribute damage type"
inherits that limitation from the oracle, not from the game we are building. If we want type
attribution out of a future oracle it must come from the log/panel layer, never from the pixels.

## 9.11.2 The cross-validation died — and its replacement is worth more than it was

The planned FCT↔DPS cross-validation **could not run as posed** (no census ⇒ no per-hit sum). What
survived is better:

> **`Damage per second` is a rolling-window mean, ~6 s wide.** A 1 s burst at pts 6046 produces a
> **6.5 s non-zero plateau** and then drops to 0.00 in a single step.

Therefore **∫ dps dt over a bout = total damage dealt**, and it needs **no per-hit census at all.**

| Dummy bout | Total damage (∫dps dt) |
|---|---|
| pts 5990–6013 | **18554** |
| pts 6026–6042 | **18051** |
| pts 6046–6052 | **2939** |

This is the single most load-bearing methodological result of round 2. The instrument I twice nearly
discarded — first by declaring `Damage per second` dead off two out-of-combat bookend samples
(§5 D-3, corrected in §9.3), now by treating FCT as its only route to total damage — is the **primary**
total-damage instrument, and the FCT census was never on the critical path. **Standing rule: before
declaring a field dead, sample it inside the condition it measures.** I have now violated that rule
once and been rescued from it twice.

**Qualification I attach (not in her return).** A ~6 s boxcar means the integral is only exact when
the integration bounds sit in dps≡0 on both sides. Bouts 1 and 2 satisfy that; **bout 3's window
(6 s) is the same order as the kernel width**, so its 2939 is the least trustworthy of the three and
should not anchor anything alone. Bounds must be taken at the *plateau edges*, not the contact edges.

## 9.11.3 Dummy segment — confirmed, widened, and two corrections to me

`kills` sits frozen at **692** from `play_time` **96:48 → 107:55** (**667 s**), not the 98:12–106:11
I bracketed. Damage lands in **exactly three bouts, 46 s of contact total.** Gear change brackets to
pts **5760–5990** (two green tooltips side by side at 5760).

**Correction 1 — the test is at level 11, not "just before 12."** 10→11 fires at pts 5515.0, at the
*start* of the window. My §6b-bis phrasing put the dummy test at the top of the level-12 shelf; it
sits at the bottom of the level-11 one.

**Correction 2 — the node grid at offset ~5800 is the MASTERY TREE, not devotion.** I read it as
devotion evidence. It is not evidence of anything about devotion.

Correction 2 matters more than it looks: it removes the only *positive* frame I had for the devotion
question and leaves that question resting entirely on absence-of-evidence. See §9.11.5.

## 9.11.4 Player-side poison DoT — the cleanest number in the run, and cleaner than reported

Matt's deliberate death was the right instinct and it produced the best-conditioned measurement in
the artifact set. Globe **numerals** at 60 fps, **98.2% coverage over 58 s**:

| Quantity | Value | Basis |
|---|---|---|
| **Tick magnitude** | **−10 HP exactly** | 57 consecutive ticks |
| **Tick period** | **1.000 s exactly** | sd **0.072 s** across 57 ticks |
| Max HP implied | **≈490** | from 10 HP = 2.04% of max |
| Time-to-kill from full, unresisted | **59.8 s** | |
| **Regen** | **1.580 HP/s — MEASURED, not modelled** | `life_healed` 3351.78 → 3445.00 (Δ **93.22**) with potions **0** and dps **0.00** ⇒ no exogenous term, no lifesteal |

The out-of-combat matched-gear regen stretch I had planned to ask for is **not needed**. The death
window contains its own regen control, because the two confounds that would have polluted it
(potions, lifesteal) are both pinned to zero by fields already in the panel. That is Matt's
no-potion control paying off in a place nobody designed it for.

### The closure residual is a denominator artifact — the physics closes ~30× tighter than reported

galadriel reports **8.42 expected vs 8.21 measured** and correctly flags that she has *not*
double-subtracted. But the three rates are computed over **three different windows**:

- 10.00 HP/s = 570 HP / **57.0 s** (tick coverage)
- 1.580 HP/s = 93.22 HP / **59.0 s** (`life_healed` endpoints)
- 8.21 HP/s = net drop / **≈58 s** (globe endpoints)

Put all three over one common window **W = 58.0 s**:

```
raw DoT   570.00 / 58.0 = 9.828 HP/s
regen      93.22 / 58.0 = 1.607 HP/s
net                      = 8.221 HP/s      vs measured 8.21   →  0.13% closure
```

The 2.5% gap is arithmetic, not biology. **The closure is essentially exact.**

**And the durable quantity is the TICK, not the rate.** "10.0 HP/s" is window-dependent (over a
58 s window with 98.2% coverage the *effective* raw rate is 9.83). "**−10 HP per tick, period
1.000 s, sd 0.072 s**" is exact and window-independent. Only the tick form goes into the oracle.

**One more thing the uniformity buys us, which neither of us said.** 57 ticks of *identical*
magnitude is itself the evidence that this is a **single DoT instance continuously refreshed**, not
overlapping stacks from a flooded cave — stacking would produce a stepped or varying magnitude. That
is what makes it oracle-grade rather than merely large. A stacked reading would have been useless.

**Design-relevant figure for Reincarnated (not GD trivia):** an environmental hazard that kills an
unresisting player in **~60 s at ~2% max-HP per second**, ticking on a **flat 1 s cadence**, against
a regen of ~0.32% max-HP/s — i.e. the hazard runs **~6.3× regen**. That ratio is the hazard-tempo
number, and it is far more transferable than the raw 10.

**Flagged and unexplained:** HP restores to **full** at pts ~2769 and ~2775 with potions at **zero**.
The measurement stretch is downstream of both, so the number is unaffected — but an unexplained
full-heal on a run whose whole value is its controls is a **live thread**, not a footnote. Candidate
causes to test, cheapest first: (a) a level-up (GD full-heals on level-up) — check `max_level` at
those pts; (b) a shrine/rift/town transition; (c) a death not yet in the deaths series. If (a), it is
fully explained and should be written into §2.2 as a known control-exempt event.

## 9.11.5 Two honest gaps, held open

**Dummy-side poison DoT — NOT MEASURED.** Blocked on the census; the dps field cannot separate DoT
from direct damage. Recorded as an honest gap rather than an estimate. **This is the one deliverable
Matt specifically set up gear for, and it did not land** — through no fault of his setup. The v2 fix
(§9.11.7) recovers it.

**Devotion — still OPEN, and galadriel declined to claim it.** No constellation screen exists
anywhere in pts 5700–6080. The best indirect evidence is that **no `devotion/` path appears in
`Skills Used` across all 313 stills** — which proves **no devotion proc ever fired**, and therefore
closes the kill-attribution channel that actually threatened the oracle. It does **not** prove zero
points assigned, because stat-only nodes leave no trace in that list.

**My disposition:** the control that matters for this fixture is *"no unmodelled damage source
contributed to kills"*, and that is **PROVEN** by the absent `devotion/` path. The stronger claim
*"zero devotion points assigned"* is **UNVERIFIED and should be recorded as such rather than
searched for further** — a stat-only node would perturb the damage magnitudes we are calibrating,
but it perturbs them *inside* the character sheet, and the character sheet is screenshotted. Route
it to the gear/stat reconciliation pass, not to another video search. Matt's own hedge ("at least I
think I did") is the correct confidence level and should survive into the fixture metadata verbatim.

## 9.11.6 T-A screenshot arm — CLOSES

**313/313 stills, zero missing fields, zero monotonicity violations across six series.** The arm that
began with my D-1 misread ends clean. Both independent D-1 reproductions (mine on `play_time`,
elrond's on `kills`) are now behind a gate that catches them.

## 9.11.7 The v2 change that buys the most for the least

> **Record one dummy segment with the debug overlay OFF.**

One toggle, one segment. It removes the self-inflicted occlusion, makes the FCT census tractable, and
recovers the dummy-side DoT measurement that is the only thing round 2 failed to deliver. Everything
else about v2 can stay as it is.

**Protocol form (§2.2 amendment, owed):** the dummy-test segment runs in **two passes over the same
gear state** — pass 1 overlay ON (panel fields, dps, `life_healed`), pass 2 overlay OFF (FCT census).
Gear must not change between them, and the pass boundary is called out on the audio track.

## 9.11.8 Consolidated action from round 2

- [ ] gandalf: §2.2 amendment — **two-pass dummy segment** (overlay ON, then OFF, same gear).
- [ ] gandalf: §5 amendment — FCT is an **assisted sampler**, not a ledger; **`∫dps dt` is the
      primary total-damage instrument**; integration bounds at plateau edges, never contact edges.
- [ ] gandalf: §5 amendment — **no colour coding in FCT**; damage-type attribution can never come
      from the pixel layer.
- [ ] gandalf/elrond: record the poison DoT as **tick-form** (−10 HP / 1.000 s / sd 0.072), never as
      a rate; carry the ~6.3× hazard-to-regen ratio as the transferable figure.
- [ ] galadriel or elrond (~5 min): check `max_level` at pts **2769** and **2775**. Level-up would
      fully explain the unexplained full-heals; anything else is a live control breach.
- [ ] elrond: fixture metadata records devotion as **"no proc fired — PROVEN; zero points assigned —
      UNVERIFIED (player-reported, self-hedged)"**. Do not collapse those two into one flag.
- [ ] gandalf: correction of record — dummy test is at **level 11**; the ~5800 node grid is the
      **mastery tree**. §6b-bis and §9.10 amended by this section.
- [x] galadriel: T-A screenshot arm CLOSED, 313/313.

---

# 9.12 ROUND-3 — the unexplained full-heal, closed (galadriel, 2026-07-26)

**Verdict: BENIGN, not a control breach — and there was only ONE event, not two.**

## 9.12.1 The second event does not exist — D-1 reproduced a FOURTH time, at a new scale

The 60 fps globe trace reads **491 continuously from 2769.317 to 2775.017**, is **unreadable
2775.033–2777.717**, and reads **491 again at 2777.733**. Full HP on both sides. `life_healed` is
**flat at 3351.78** across pts 2770 / 2772 / 2774 / 2778 — no healing of any kind occurred there.

galadriel's round-2 "~330 → 491" was **a read taken across an occlusion.** Her own words: *"my own
D-1 failure mode at window scale instead of glyph scale."*

> ### The D-1 generalisation, now forced by a fourth instance
>
> D-1 is **not** about crop geometry. Four instances, three distinct mechanisms:
>
> | # | Who | Mechanism | Wrong value returned |
> |---|---|---|---|
> | 1 | gandalf | large crop + large upscale ⇒ downsample at read time | `50:37` for `59:36` |
> | 2 | elrond | same, different field | `kills: 0` for `kills: 2` |
> | 3 | galadriel (r2) | **read spanning a data gap** — interpolation across an occluded window | a 161 HP drop that never happened |
> | 4 | — | (D-2/anger-overlay occlusion is the same family, caught early) | — |
>
> **The invariant across all of them: the reader returned a PLAUSIBLE value and did not announce
> that it had guessed.** Instance 2 is the sharpest — the wrong value was the *more* plausible one,
> so a sanity check would have confirmed the error.
>
> **Binding rule, promoted from method-note to pipeline constraint: every reader must emit COVERAGE,
> not just values.** A reader that cannot report its own coverage is not an instrument. This is
> precisely why instance 3 was catchable at all — the globe reader reports coverage (98.2%), so the
> gap was visible once looked at. The panel readers that produced instances 1 and 2 did not.

## 9.12.2 The one real event — a level/map transition, and both mechanisms are eliminated on two fields each

pts **2766.500 → 2769.317** (2.82 s) is a Grim Dawn **loading-screen splash**; the maps either side
differ (green poison cavern → dry rock passage). **HP 342 → 491** (Δ +149). A second loading screen
at 2775.033–2777.717 returns him to the poison cavern at full — he stepped out the door and back in,
then rode the poison down to the death that produced the oracle.

| Candidate cause | Eliminated by |
|---|---|
| level-up full-heal | `max_level` = **8** throughout (7→8 fired at pts ~2728) |
| unlogged death | `deaths` = **0** until 2838.2 |
| potion | counter **0** (Matt's control, holding) |
| lifesteal | `dps` = **0.00**, `kills` pinned at 271 |

The game booked it as healing: **`life_healed` +149.36 against a globe delta of +149.**

## 9.12.3 The honest gap she held open — and why it does not touch the oracle

She cannot separate **flat restore-on-load** from **out-of-combat / Constitution regen released when
the DoT stopped**: the whole restore sits inside a 2.82 s HUD-less window, and both predict identical
observables. Correct refusal to claim.

**My addition — the mechanism question cannot reach the number, and here is why.** `life_healed` is
**mechanism-agnostic**: it books *all* healing regardless of source. Over the measurement stretch it
moved **93.22** total. Whatever restored 149 HP at the transition, it contributed nothing unbooked
during 2778.0–2836.6. The DoT figure is safe under either resolution.

**But one LABEL must change.** 1.580 HP/s is *"total healing from all sources while under DoT"* — an
**in-combat** figure, not base regen. If GD's Constitution pool is suppressed in combat (the likely
reading, given a 149 HP restore in 2.82 s is ~94 s of work at 1.58 HP/s), then the two are different
quantities and must not be conflated. **For the hazard-tempo ratio we want the in-combat one anyway**,
so the transferable ~6.3× stands — but it is now labelled correctly.

Her v2 settlement is 30 seconds of work: drop to ~50% in a non-DoT area, stand out of combat 10 s
with **no transition**, read the globe.

## 9.12.4 A protocol rule that closes an open item in §3 for free

> **A loading screen is a segment boundary.** No measurement stretch may span one; the first sample
> after one is a **fresh full-HP initial condition**, not a continuation.

The rule holds identically under either mechanism, so it can be adopted **without** settling 9.12.3.

**And the detector is free from the existing globe reader:** a contiguous unreadable run **> 2 s** is
a transition; ~1 s runs are ordinary HUD occlusion.

**This is the convergence worth noticing.** §3 ruled that `play_time` freezes during loading and that
the affine video↔ledger map is piecewise slope-1 with **breaks at zone transitions** — and left those
breaks to be *fitted from panel samples.* §9.12's detector finds the same boundaries **independently,
from the globe channel, at 60 fps.** One physical event, two consequences (clock discontinuity **and**
state discontinuity), now detectable by two independent instruments that can cross-check each other.
**Adopt the detector as the break-finder for the §3 clock fit.**

## 9.12.5 The measurement stretch is clear

2778.0–2836.6: **3453 / 3517 frames read, zero transitions**, longest unreadable run **1.0 s** at 2785
(433 → 415, a continuous two-tick decline — not a gap that hides anything). **The −10 HP / 1.000 s
tick and the 1.580 HP/s in-combat healing figure both stand.**

Artifacts: `galadriel/captures/2026-07-26-gd-playtest-v1-r3/` (`r3-evidence.json`,
`globe-hp-2750-2782-60fps.jsonl`, `panel-2750-2792.jsonl`, `frames/`). Commit `23e3e25f`.

## 9.12.6 Action

- [x] full-heal anomaly — **CLOSED, benign.** No control breach. Oracle unaffected.
- [ ] gandalf: §2.2 amendment — **a loading screen is a segment boundary**; measurement stretches
      may not span one.
- [ ] gandalf/galadriel: adopt the **>2 s unreadable-run transition detector** as the independent
      break-finder for the §3 piecewise clock fit.
- [ ] gandalf/elrond: **every reader emits coverage.** A reader that cannot report its own coverage
      does not write to `fixtures.db`. Retrofit the panel readers (D-1 instances 1 and 2 were
      undetectable precisely because they could not).
- [ ] elrond: label the healing figure **"in-combat healing, all sources"**, never "regen."
- [ ] v2 (~30 s): non-DoT 50%-HP out-of-combat stand, no transition — settles restore-on-load vs
      Constitution regen.

---

# 10. Design recognition — form identity, and the transform Matt made for no reason

▶ **ROLE: STORYWRIGHT** — trigger: an unprompted player behaviour in the substrate that speaks to a
locked Reincarnated design thesis.

**The observation.** Matt transformed into the werewolf **in town**, where it bought him nothing —
no combat, no threat, no mechanical benefit. His own account: *"for no specific reason other than to
preserve the role-play experience."*

**Why this is evidence and not anecdote.** It is an *unprompted, mechanically-worthless* action taken
by a player who was at that moment operating as an instrument-runner under a controlled protocol —
i.e. the one condition under which he had every reason **not** to add unnecessary actions. He did it
anyway. Behaviour that survives an incentive to suppress it is the strongest kind of preference
signal there is.

**What it is evidence OF.** That the form is not experienced as an ability with an uptime. It is
experienced as **who the character is**. The player wants to *be* the thing, and only tolerates being
the other thing when the game makes him.

This is precisely the thesis the Reincarnated **form library** is built on — forms as accumulated
identities, not as cooldowns. We now have a player, under experimental discipline, spending actions
to hold an identity that pays zero.

**Genre precedent, and the trap sitting inside it.**

- **Diablo II Druid** — shapeshift is duration-based and must be re-cast. Identity is *present* (the
  Werewolf/Werebear player thinks of himself as the animal), but it is **taxed**: every re-cast is
  the game reminding you that the form is temporary and you are really the human underneath.
- **Diablo IV Druid** — per-skill momentary shifting removed that friction entirely, and dissolved
  the identity with it. The community complaint that followed was never about power; it was
  literally ***"I can't stay a werewolf."*** D4 optimised away the tax and destroyed the thing the
  tax was protecting.

**The trap:** the friction and the identity look like separate variables and are not. D2 has both.
D4 removed the friction and lost the identity. **Nobody in the lineage has shipped identity without
friction** — and that is the space Reincarnated's form library is actually aiming at.

## 10.1 AMENDMENT (same session, Matt's challenge) — the frame above is borrowed from the wrong game

**Matt asked: *"are we just talking about shapeshift forms here?"* The answer is no, and the D2/D4
framing above is mis-transposed. It is corrected here rather than deleted, because the mis-transposition
is instructive.**

Grim Dawn's werewolf is a **removable** identity — and it is the *only* removable identity GD has,
which is why the principle surfaced there wearing a shapeshift costume. In *Reap. Die. Rise.* the body
**cannot be taken off**: possession destroys the old body (`story-keystone.md` §§118–122, "mechanically
legible irreversibility"), bodies are vessels and the self is the controller (§159). There is no
duration, no re-cast, no toggle.

**Therefore protections 1 and 2 above are MOOT for this game as written.** Strike them in that form.

**What actually generalises is one sentence:**

> **Any identity the player chose, that the game can make cheaper to abandon than to keep.**

Shapeshift is merely the surface on which that is most visible in the source game.

### 10.1.a Already ruled — this is EVIDENCE FOR a locked decision, not a new proposal

`canonical/reap-die-rise-story/gameplay-loop-design.md` §8:

> *"Besting a lieutenant **offers** reincarnation… It is **opt-in, always.** Declining keeps your
> current kit. (Forcing a swap would gut the kit identity the whole project is built on; the player
> who loves their bone-spear-necromancer must never be made to abandon it.)"*

That is protection 1, correctly translated into this game's terms, and it was **already locked on
instinct.** The town-transform observation does not propose it; it **corroborates** it empirically —
a bone-spear-necromancer player caught in the wild, in a game that is not even ours, under
experimental discipline that gave him every incentive not to.

### 10.1.b What survives unprotected — LEGIBILITY (protection 3 stands, alone)

`gameplay-loop-design.md` §306 establishes the hub as *"the **daily** relationship that replaces the
old guide's ever-present voice."* Nothing currently says the hub reacts to **which body you came home
in.** That is the cheapest unbought thing on this board, and it is the one that converts a *tolerated*
attachment into a *rewarded* one. Protection 3 stands unmodified and is now the whole of the
recommendation.

### 10.1.c The live fork — DOES THE POWER CURVE RIDE THE KIT? *(open; Matt rules)*

§8 says declining is free. **It is only free if power does not ride the kit.**

`gameplay-loop-design.md` §206: *"You **must best one lieutenant to descend** (the gate is preserved —
power injection happens on schedule, sawtooth intact)… **Whether** you reincarnate is optional."* The
gate is **besting**, not **becoming** — good. But if lieutenant kits scale with depth, a player who
declines twice carries an early kit into late content, and the game has made loyalty expensive
**without ever forcing a swap.** That is D2's re-cast tax in a different costume: the identity is
permitted, and then billed for.

| Option | Consequence | Cost |
|---|---|---|
| **A — power rides the kit** | ascension is felt directly; taking a stronger body *is* stronger; the "ascending conqueror" ladder is literal | declining is a real power sacrifice ⇒ §8's protection is **nominal**, and the attachment player pays rent |
| **B — power rides gear + soul level** (the axes that already cross runs per `agnostic-loot-story-spec.md` §32); kits near-flat in magnitude, differing in **expressiveness** — more operators, different geometry, different matchups | declining costs *variety* and *situational fit*, never *viability* | the becoming stops reading as ascension; the ladder must be carried entirely by soul level |
| **C — split** (LEAN): magnitude near-flat, **complexity/expressiveness escalating**, ascension banked in soul level | keeps the ladder without taxing loyalty | requires kit power to be authored to a band, which constrains the generator |

**Lean: C.** Precedent is **Diablo II class design** — not power-equal, but all *viable*, each
distinctly itself. It is the only shipped model in the lineage where identity survived alongside a
real power curve. **This is a keystone-adjacent economic ruling and is Matt's, not mine.**

### 10.1.d Flagged tension — a record you spend is a currency, not a record

`gameplay-loop-design.md` §1: *"your collection of conquered spirits **is** the record of who you have
become."* But §240: grimoire pages are **spent** on summoning. The depletion economy is good design —
§244 is right that the forfeit branch is what gives it weight — but it is in tension with the
collection-as-identity line. **One of the two framings will have to yield, and it is cheaper to know
which before any marketing copy is written.** Not ruled here; flagged.

### 10.1.e Player consequence, restated for THIS game

Under option A with no hub legibility: the player takes every offered body because declining is
taxed, arrives in the hub as an interchangeable vessel nobody comments on, and the grimoire becomes a
power ledger. Under option C with hub legibility: the player *chooses* which lives to keep, walks into
the hub wearing that choice, someone speaks to **that** body — and the collection becomes the record
§1 says it already is. That is the difference between the loop feeling like an economy and feeling
like reincarnation, which is the game's name.

**Cross-reference owed:** `canonical/reap-die-rise-story/gameplay-loop-design.md` §§1, 8, 206, 233–246,
306; `canonical/current-to-end-state/current-to-end-state-story.md` open-question queue (the 10.1.c
fork and the 10.1.d tension both belong there as rows). Recorded here first because the evidence is
here.
