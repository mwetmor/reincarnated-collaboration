# SB-1 Cell CLK-2 (firing #2) — landing note

⚑ **VERDICT: HALT, chartered. The shader/pipeline disk-cache family is EXONERATED — the cold
probe was run, the cold condition was real and observed, and it produced output BYTE-IDENTICAL
to a warm pass across all 380 frames including the preroll. Item 1's conviction landed outside
the fix families the charter authorised, so items 2, 3 and 4 did not fire. Separately and
independently, the charter's PREFERRED fix is unimplementable on this scene as specified, and
that is measured rather than argued. Caches restored. Nothing was improvised.**

Cell: CLK-2, firing #2. Conductor: gandalf (RUN-CONDUCTOR). Date: 2026-08-14.
Firing #1 died violating NOTE-84a; its salvage was inherited, re-verified and harvested.

---

## Item 0 — SALVAGE HARVESTED ✅

`agentic_orchestration/galadriel/captures/2026-08-13-sb1-clk2/` now holds firing #1's two probe
runs in full: both summaries, all 15 digest lists (`.sha` post-prune and `.raw.sha` pre-prune),
all 8 pass logs, one frame per distinct state, three geography reports, and the prune receipts.
The probe script is committed at `reincarnated-godot/scripts/clk2_probe.sh` — it ran ungoverned
in firing #1, and instruments get committed.

Every salvage claim was re-derived from the raw byte lists before being consumed. All held.
Two things were added that firing #1 did not have:

**The killed fourth pass was completable.** Its digest list was never written, but it had
written 99 frames before the cell died. Hashed: **byte-identical to pass 2 over all 99**. That
is the first evidence that the preroll states *cluster* rather than random-walk.

**The digests were turned into a geography.** `kc2_clk2_geography.py` (new, committed) reports
for a frame pair: differing-pixel count, bounding box, max/mean channel delta, the ±1 share, a
4×4 region grid, and an amplified difference PNG. Its control — the same two passes at the first
*measured* frame — reports **0 differing pixels**, so its non-zero readings mean something
(NOTE-72).

FG-12: 1,239 salvage frames pruned (2.793 G) with a receipt and a regenerate line.

## Item 1 — THE COLD CONVICTION: EXONERATION ⛔

Both censused caches were **moved aside, never deleted**, to
`/tmp/kc2_clk2_fire2/cache-backup/` — project `.godot/shader_cache` (148 files / 11,560 KB) and
user `…/reincarnated-godot-spike/shader_cache` (174 files / 26,628 KB). Both source paths were
verified absent before the render. Three blocking full-span passes followed.

### Pre-registered expectations vs measurement (NOTE-82: one name, one quantity)

| # | Expectation | Result | Measured |
|---|---|---|---|
| E1 | cold `.raw.sha` divergence reaches deeper than line 23, plausibly past 60 | **MISS** | deepest line **17–18** vs warm passes; **0** vs warm p2 |
| E2 | if past 60, post-prune `.sha` ≠ warm attractor ⇒ red reproduced on command | **MISS** | post-prune = `f651b328d9589efa…`, the attractor, exactly |
| E3 | cache census shows files repopulating | **HIT** | user cache **0 → 77 files / 2,604 KB** |
| E4 | warm passes 2/3 return to the attractor post-prune | **HIT** | both `f651b328d9589efa…` |
| E5 | warm preroll divergence depth shrinks back toward ≤ 23 | **HIT (never left)** | full-span family deepest **21** |

### The finding

The cold pass did not merely land on the attractor's post-prune digest. Its **entire 380-frame
pre-prune list is byte-identical to salvage warm pass 2** (`7196394f2f3d8011…`), and to the
killed pass 4. Removing both shader caches changed **nothing** — not one frame, not even inside
the preroll where all the variance lives. Cost: 194 s cold vs 189/190/191 s warm.

E3 is what makes this a conviction rather than a shrug: the caches genuinely were at zero and
genuinely repopulated. The probe could distinguish "the cache is the clock" from "the cache was
never cleared", and it returned the first reading (NOTE-72).

**Six full-span passes, three cache conditions (fully warm / fully cold / partially
repopulated), one post-prune digest.**

### State census — 7 full-span passes, factorised by preroll segment

| run | lines 1–4 | lines 5–17 | line 18 | lines 19–21 | lines 22–60 | measured 61–380 |
|---|---|---|---|---|---|---|
| salvage warm p1 | = | `1715817d` | `94dd2abe` | α | = | `3a4f9317` |
| salvage warm p2 | = | `ef90641b` | `94dd2abe` | α | = | `3a4f9317` |
| salvage warm p3 | = | `1715817d` | `2c6c36f5` | α | = | `3a4f9317` |
| salvage p4 (killed) | = | `ef90641b` | `94dd2abe` | α | = | (killed) |
| **firing2 c1-COLD** | = | `ef90641b` | `94dd2abe` | α | = | `3a4f9317` |
| firing2 c2-warm | = | `1715817d` | `2c6c36f5` | **β** | = | `3a4f9317` |
| firing2 c3-warm | = | `1715817d` | `2c6c36f5` | α | = | `3a4f9317` |

Byte-identical pairs over their shared length: (p2, cold), (p2, p4), (p3, c3-warm), (cold, p4).

**Deepest differing line ever observed, across all 11 passes compared like-with-like:
line 23 of 60** (short leg). Full-span family: **line 21**. Margin to the measured span: **37
frames**. Measured span digest `3a4f9317` on every complete pass, without exception.

### Pixel geography of the states

| pair | % of frame | bbox | max Δ | mean Δ | ±1 share | region grid |
|---|---|---|---|---|---|---|
| state A vs B, idx 010 | 82.017 | full 1920×1080 | 174 | 2.325 | 47.84 % | flat, 5.84–6.66 % |
| state C vs D, idx 017 | 82.026 | full 1920×1080 | 171 | 2.324 | 47.84 % | flat |
| state E vs A, idx 020 (deepest) | 82.038 | full 1920×1080 | 171 | 2.324 | 47.84 % | flat |
| **control**, cold vs warm, idx 060 | **0** | — | **0** | — | — | — |

Every divergent pair carries the **same fingerprint**. The amplified diffs show what the numbers
are: a regular tiled diamond pattern at ±1/±2 across the whole ground plane, plus small bright
clusters on each body and one strong coloured arc at the central subject (the >8 tail, ~29 k px).
A first-use *rendering* difference that heals by line 22 — not a diverged simulation. A diverged
simulation does not reconverge.

### Why the charter's preferred fix cannot be built (measured, before it was attempted)

> "Exit preroll ONLY after K=10 consecutive identical frame hashes."

**All 60 tick-frozen preroll frames are distinct within every pass — 60 distinct of 60, on all
ten passes checked.** The tick is frozen, so the bodies are still; but FX/particles/trails and
whatever drives the ground's per-frame dither advance on *process* time, which the tick freeze
does not touch. Two consecutive identical frames never occur, let alone ten. The gate would
reach its 600-frame cap and abort LOUD on every single run, including green ones.

This is independent of the exoneration above: even had the cold probe convicted, fix (1) as
specified would not have run. A settlement gate remains viable, but its predicate must be
*readiness*-based, not pixel-identity-based.

## Items 2, 3, 4 — NOT EXECUTED (chartered HALT) ⛔

Charter: *"If COLD does NOT push divergence past the preroll (E1/E2 miss): the cache-population
family is NOT the escape mechanism — report what measured, keep the caches restored, and HALT
for conductor ruling (do not improvise new fix families)."* E1 and E2 both missed. No fix was
written, no matrix was run, `a2gr-lookdist-cadence-ab.mp4` was **not** rendered and **not**
promoted. R-CPB-17b remains unissued.

**Caches restored** to their exact opening census: project 148 files / 11,560 KB, user 174 files
/ 26,628 KB; backup directory empty. The 77-file partial repopulation from the cold run was
discarded so the restore is the original state and not a merge. Verification method: file count
and KB compared against the opening census recorded in both probe summaries — byte-level
comparison of cache contents was **not** performed (GL-12).

FG-12: 1,140 firing-2 frames pruned (2.569 G) with a receipt and a cold-regenerate line.
PL-5: captures directory 6.8 G → 6.85 G, under the 10 G ceiling; disk floor checked first
(21 GiB free at open, 24 GiB at close).

---

## Surfaces

1. **The A2g-r red is still unexplained, and the sample is now 11 passes deep with no
   reproduction.** Firing #1 (7 passes) and firing #2 (3 passes, one cold) all land on the same
   measured-span digest. Whatever pushed the transient past frame 60 on 2026-08-13 is not the
   disk-cache state, and it has not recurred once. The mechanism is convicted in *kind* (a
   first-use rendering race in the first ~21 frames) but its *trigger* is uncaptured.
2. **FG-10 is structurally blind to this defect.** It prunes the preroll and *then* compares, so
   it cannot see the region where 100 % of the observed variance lives. It only turns red on the
   day the transient escapes — which is precisely the day it is least useful. The probe's
   dual-list discipline (NOTE-84b) is what makes the variance visible; FG-10 does not have it.
   Cheap remedy available: have the harness digest the pre-prune list too and report preroll
   divergence depth as a standing green-run diagnostic, so the margin is *watched* instead of
   discovered.
3. **The tail is not characterised, and it moved during this cell.** Before firing #2 the
   full-span family's deepest divergence was line 18. c2-warm — a state never previously seen —
   pushed it to 21. Three more passes produced one new state. The distribution over frame index
   is being sampled, not bounded, and 37 frames of margin is an empirical floor over 11 draws,
   not a guarantee.
4. **The divergence is two-or-more independent binary events, not a warmth gradient.** The
   preroll factorises into segments that each take one of two values, and passes are
   combinations of them. A cache-warmth gradient would impose a monotone ordering on passes.
   None exists.
5. **The censused "warm cache" was mostly not being read.** Across three cold/partial passes the
   *project* shader cache never repopulated at all (0 files throughout) and the user cache
   repopulated to 77 of its original 174 files. The run touches ~77 files; the census was
   reporting 322. Any future cache-based reasoning should use the 77.

## NOTEs

- **NOTE-85 — A settlement gate needs a predicate that can fire.** The charter's preferred fix
  (exit preroll after K=10 consecutive identical frame hashes) is unimplementable on this scene:
  all 60 tick-frozen preroll frames are distinct within every one of ten passes measured. The
  tick freeze stops the bodies, not process-time rendering. Pixel identity is not available as a
  settlement predicate here; readiness is the only family left. Measure the predicate's
  reachability before specifying a gate on it.
- **NOTE-86 — The shader/pipeline disk-cache family is exonerated for KC2 CPB.** Both censused
  caches moved aside (project 148→0, user 174→0, both verified absent); the resulting cold pass
  was byte-identical to warm pass 2 across all 380 frames including the preroll; the caches
  demonstrably repopulated (user 0→77). Cold costs ~4 s of wall clock and zero pixels. Do not
  re-litigate without new evidence.
- **NOTE-87 — One fingerprint means one mechanism.** Every divergent preroll pair measured
  carries the same geography to three significant figures: 82.02–82.04 % of the frame, bbox =
  the whole frame, max Δ 171–174, mean Δ 2.324–2.325, ±1 share 47.84 %, flat region grid.
  Distinct mechanisms would print distinct fingerprints. The only free variable is which frame
  index the event lands on.
- **NOTE-88 — Segment-factorised state census beats a distinct-state count.** "3 distinct states
  across 4 passes" (A2g-r) hides the structure that "lines 5–17 take one of two values, line 18
  takes one of two, lines 19–21 take one of two, and passes are combinations" makes obvious. When
  a determinism gate goes red, factorise the frame list into segments before counting states —
  the factorisation is what distinguishes a gradient from independent coin-flips.
- **NOTE-89 — A third Godot cache exists and the census never covered it.**
  `~/Library/Caches/Godot`, 351 M, 83,612 files. Inspected: editor resource thumbnails
  (`resthumb-*`) plus `editor_doc_cache-4.6.res`. Editor-time only; a headless `--write-movie`
  run does not read it. Declared per GL-12 and deliberately not moved — moving it would have
  cost a 351 M restore risk to test a path the render never touches.
- **NOTE-90 — Write the digest lists even when the gate is green.** Firing #1's dual-list
  discipline (NOTE-84b) is the only reason any of this was visible: the post-prune list has been
  green for 11 consecutive passes while the pre-prune list has differed on nearly every one. A
  gate that only records its own verdict records nothing about its margin.
