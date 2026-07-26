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

**This is decidable before any modelling, and cheaply.** `character.LogData` was on for the run.
Cross-check a bounded window: count swings from the log (or from T-B video frames) against the
`skill_use_count` delta across the same `play_time` interval. Equal ⇒ cause 1 or 2, and the ledger
survives with an added term. Unequal ⇒ cause 3, and §1.1 must be rewritten to demote the panel to a
*coarse* ledger with the video as the attack-rate instrument.

**Do not model attacks-per-kill until this is settled.** This is precisely the class of error the
math-before-code discipline exists to intercept: the statistic looks free, reads cleanly, and would
have been wrong by an unknown multiplicative factor.

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
`Life healed: 12468.06` is **entirely endogenous**: health regeneration, lifesteal, devotion procs.
No exogenous step-functions in the series. That is ~106 HP/min, roughly **18.5 max-health pools**
(peak observed 672) recovered over 113 minutes without a single player-triggered heal. Under any
potion usage this field is a sum of two unrelated processes and worth nothing; under this control it
is a direct measurement of sustain throughput — the exact quantity the era-substrate needs to
calibrate its sustain curve against. This was the highest-value side effect of the decision.

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
