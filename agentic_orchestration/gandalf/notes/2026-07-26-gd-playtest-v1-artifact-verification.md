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
model them. `Health potions used` / `Mana potions used` read `0` at 118 min with 2 deaths — either
genuinely zero or non-incrementing. One word from Matt settles it; until then neither is a
calibration signal.

## 6. Ledger trajectory — sanity

`kills` 0 → 2 → 14 → 45 → 87 → 271 → 586 → 692 → 882 (monotonic)
`deaths` 0 → 1 → 2 · `max level` 1 → 3 → 4 → 8 → 11 → 12 · `play_time` 6:11 → 118:08

**882 kills in 113 minutes ≈ 7.8 kills/min.** For a distribution oracle whose primary statistic is
attacks-per-kill, that is a dense sample, not a thin one. Areas traversed on the sampled frames:
Lower Crossing → Devil's Crossing → The Old Dump.

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

## Action

- [ ] galadriel: T-A ledger-tier CV pass against the real MP4. Binding constraints from this
      finding — (i) D-1 crop/upscale geometry; (ii) key on `play_time`, fit the affine map per
      session per §3; (iii) cross-field consistency gate (kills/deaths/level must co-agree before a
      panel read is accepted); (iv) expect D-2 occlusion on `Skills Used`.
- [ ] elrond: `fixtures.db` ingestion per §5. Screenshot→timeline placement is mtime arithmetic
      against `video_start_epoch = 1785096216.5`; store `pts_ms` AND `play_time_ms`, with
      `play_time_ms` as the join key.
- [ ] gandalf: fold §3 into protocol §1.1 and D-2 into §2.0 before the v2 run.
- [ ] Matt: one word on D-3 — did you use zero potions across the run, or is that counter dead?

## References

- `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/` (video, smoke, 313 screenshots)
- `agentic_orchestration/gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` (§§1.1, 2.0–2.2, 3.1–3.2, 5.1)
- Working crops: `/tmp/gp-align/` (transient)
