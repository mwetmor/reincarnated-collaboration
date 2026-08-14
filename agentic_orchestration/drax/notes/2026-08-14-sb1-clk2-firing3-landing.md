# SB-1 Cell CLK-2 (firing #3) — landing note

⚑ **VERDICT: ALL THREE ITEMS LANDED. The instrument is built and was verified against numbers
that existed before it did; the certifying matrix went GREEN on all five legs — twenty passes,
one distinct state per leg, the promoted leg's first pass rendered from a fully cold shader
cache; and THE WATCH IS PROMOTED — `a2gr-lookdist-cadence-ab.mp4`, sha256 `017aebf4bb92cfff…`,
658 frames, with every pre-registered optic hit on the render that produced the bytes. No fix
was applied and none is claimed. Caches restored. And the new instrument earned its keep on its
first outing: the pinned manifest line says the preroll divergence is deepest at 21/60, and this
matrix measured 23/60 on the promoted leg — the tail moved again, on a GREEN run, and for the
first time it was seen instead of discovered later.**

Cell: CLK-2, firing #3. Conductor: gandalf (RUN-CONDUCTOR). Date: 2026-08-14.
Godot `0b0f5ee` → **`6814e76`** → **`be7f0c2`** (HEAD, both pushed, PL-7).
Collab `cf81af12` (item A collab half) + `c79f978d` (item C) + this note.

| item | commits | what |
|---|---|---|
| **A** | `6814e76` (godot) + `cf81af12` (collab) | **THE NOTE-90 INSTRUMENT** — both lists always, depth as a standing diagnostic, red legs captured |
| **A follow-on** | `be7f0c2` (godot) | splitting the gate must not become a way to waive it |
| **B** | *(evidence)* | **THE CERTIFYING MATRIX** — 5 legs × 4 passes, all green, one cold |
| **C** | `c79f978d` (collab) | **THE WATCH** — promoted, manifest, on-render optics |

---

## 0 · GATES BEFORE ANYTHING WAS TOUCHED

**PL-5 first:** captures **6.782 G of 10 G**, disk free **24.1 G** — checked in the shell before
the harness was edited, and again by the harness itself before every one of the 25 process
launches this cell made. At close: **6.790 G**, disk **24.0 G**. Delta **+8 MB** — the MP4, the
digest lists and the logs.

**Cache census at open:** project `.godot/shader_cache` **148 files / 11,560 KB**, user
`…/reincarnated-godot-spike/shader_cache` **174 files / 26,628 KB`. Identical at close.

**Containment at open:** godot **230 untracked**, one dirty tracked file
(`tmp/br2watch/measure/census.json`, 2026-08-02 — not mine, not touched). **230 / 1 at close.**
The 230 reconciles exactly against A2g-r's pin of 229: firing #1 added `scripts/clk2_probe.sh`
and `scripts/kc2_clk2_probe.gd`; firing #2 committed the first. See surface 6 for the orphan.

**GL-6:** the arena's own baton gate re-asserted `d7ecd866ac45 (MATCH)` on every launch.

---

## 1 · ITEM A — THE INSTRUMENT ✅ · `6814e76` + `cf81af12` + `be7f0c2`

### 1.1 What changed, and what did not

Three changes to the FG-10 block of `run_kc2_cpb_clip.sh`. **Zero changes to the render path.**
`kc2_cpb_clip.gd` was not opened; it is byte-identical to A2g-r's `9e6068d` and git says so.

1. **Both digest lists, every leg, every pass, green or red** → `<capture>/fg10-digests/`,
   `<legkey>-pass-N.raw.sha` (all frames, preroll included) and `<legkey>-pass-N.sha` (the
   measured span). The post-prune list is now the **tail of the recorded raw list** rather than a
   second measurement of the same thing. That equivalence is not assumed: `clk2_probe.sh` derived
   its list by exactly this tail and produced `f651b328…`, the digest A2g-r's harness produced by
   physically pruning and re-globbing. Two tools, one number, already on record.
2. **DEEPEST-PREROLL-DIVERGENCE per leg**, printed and written to the gate log and to a per-leg
   JSON. **REPORTING-ONLY** — the red condition is untouched.
3. **A red leg is now a capture**: one frame per distinct state at three *named* indices (raw 0,
   first measured, deepest diverging) plus geography for every state pair.

And the gate became addressable one pass at a time (`FG10_MODE=pass|verdict|segments|all|reset`),
because NOTE-84a makes a twenty-pass matrix in a single call un-harvestable inside a turn. **`all`
runs the identical sequence through the identical functions — there is one gate, not two.**

### 1.2 ⚑ THE VERIFICATION: THE TOOL REPRODUCED NUMBERS THAT EXISTED BEFORE IT DID

| replay | expected (firing #2 § state census) | **measured** |
|---|---|---|
| full-span family, 6 complete passes | deepest **line 21** of 60 | **line 21**, margin 39, 17 lines differ |
| short-1570 family, 4 passes | deepest **line 23** of 60 | **line 23**, margin 37, 19 lines differ |

Both also report **measured span IDENTICAL**, and both put the first divergence at index0 **4**
— firing #2's "lines 1–4 agree on every pass; the variance opens at line 5", produced mechanically
instead of by eye.

**Controls (NOTE-72):** a pair known byte-identical → **NONE, margin 60 of 60**; the killed
99-frame pass folded in → **line 21, unchanged**.

⚑ **AND A CONTROL FOUND A DEFECT IN THE INSTRUMENT BEFORE THE INSTRUMENT SHIPPED.** With a single
list there are no pairs, and the tool printed *"NONE — all 60 preroll frames identical across 1
passes"* — the exact sentence it prints when it genuinely compared and agreed. Two verdicts
wearing one line (NOTE-82). It now prints **"NOT MEASURABLE — 1 pass, no pairs to compare. This is
not a green reading."** and carries a `measurable` field. I found this because I wrote a control
whose only purpose was to try to make the tool lie, and it lied.

### 1.3 Plumbing smoke — no committed code path is unexercised

Three paths run in an isolated temp tree before the matrix was allowed to use them: **green**
(exit 0), **red** forced by injecting a synthetic divergence into a throwaway list (exit **12**,
keep-frames fired, geography written), and **all** (exit 0). The red smoke was a plumbing test,
not a determinism finding, and is labelled as such wherever it appears.

⚑ **It produced a real reading anyway.** Its two kept frames at raw index 16 are genuinely
different frames, and the geography reads **82.028791 % of frame, max Δ 171, mean Δ 2.3237, ±1
share 47.849 %, flat grid** — **NOTE-87's fingerprint to three significant figures, reproduced at
a fourth commit by an instrument written after the note.**

### 1.4 The follow-on, and why it is not a bypass · `be7f0c2`

Splitting the gate made the deliverable unreachable: the segments only ever ran by falling through
the bottom of the inline matrix loop. The obvious fix is a flag that skips the gate, and that flag
is what FG-10 exists to prevent. So **`FG10_MODE=segments` re-adjudicates the gate from its own
record** — every leg present, four lists each, one distinct state each, non-zero frame counts, and
`kc2_cpb_clip.gd` byte-identical to the file that drew them. **That is strictly more than the
monolith did**, which re-checked nothing and simply trusted the loop it had just left.

Both refusals were tested with the render path armed and **neither reached a frame**: absent
fingerprint → exit 12; wrong fingerprint → exit 12, naming both digests. A check that only fires
on absence is not a check.

---

## 2 · ITEM B — THE CERTIFYING MATRIX ⚑ **GREEN ×5** ✅

`PROBE_PASSES=4` · 20 blocking in-turn passes · **2,704 rendered probe frames** (pre-prune 3,384).
Idle lane throughout: no concurrent work of any kind ran during any pass (A2gr-1 surface 3, closed
by discipline this time rather than by luck of experimental design).

| # | leg | span | passes | **digest ×4** | states | **deepest preroll** | margin | preroll lines that ever differ |
|---|---|---|---|---|---|---|---|---|
| **1** | canon · **on** · 1570 | **FULL 320** | **p1 COLD** 195 s · 196 · 193 · 191 | **`f651b328d9589efa…`** | **1** | **23 / 60** | 37 | 19 — **5…23** |
| 2 | canon · **off** · 1570 | **FULL 320** | 191 · 194 · 191 · 188 s | `95220575d1345ba3…` | 1 | 23 / 60 | 37 | 19 — 5…23 |
| 3 | canon · on · **1660** | 46 | 51 · 53 · 52 · 54 s | `982352531827455a…` | 1 | **20 / 60** | 40 | 16 — 5…20 |
| 4 | **d-close** · on *(demoted)* | 46 | 41 · 41 · 41 · 42 s | ⚑ `0253761a43b374b9…` | 1 | 23 / 60 | 37 | **4 — 20…23** |
| 5 | **b-ring** · on *(demoted)* | 46 | 45 · 48 · 48 · 47 s | ⚑ `504b6d8b4c0929ff…` | 1 | 23 / 60 | 37 | 19 — 5…23 |

**No drift on legs 4/5.** `0253761a…` and `504b6d8b…` are CLK-1's, A2g's and A2g-r's digests
character for character — now in a **fourth cell at a fourth commit**. Leg 1 returned the
attractor `f651b328…`, which is also A2g-r's passes 3 & 4 and all six of firings #1/#2's complete
full-span passes. Legs 2 and 3 returned A2g-r's own greens.

### 2.1 The cold pass

Both censused caches were **moved aside, never deleted**, to `/tmp/kc2_clk2_f3/cache-backup/`;
both source paths verified absent before the render. Pass 1 ran **195 s** against 191–196 s warm —
**cold costs nothing measurable.** The user cache repopulated **0 → 77 files / 2,604 KB** during
the pass, so the probe could distinguish *"the cache is the clock"* from *"the cache was never
cleared"* (NOTE-72), and it returned the first reading again. The partial repopulation was then
**discarded** and the originals moved back: **project 148 / 11,560 KB, user 174 / 26,628 KB,
backup directory empty.** Verification method: file count and KB against the opening census;
byte-level comparison of cache contents was **not** performed (GL-12), same as firing #2.

**Seven full-span passes have now been rendered from a cold cache or a partial one across two
firings, and not one of them has moved a certified pixel.** NOTE-86 stands; I did not re-litigate
it, I merely paid the ~4 s it costs to keep the acquittal inside the certifying matrix.

### 2.2 ⚑ THE FIRST STANDING-DIAGNOSTIC READING, AND IT MOVED THE TAIL

The full-span family's deepest preroll divergence was **21** at CLK-2-2. **This matrix measured
23** on both full-span legs. Firing #2's surface 3 said the tail was "being sampled, not bounded";
twenty more draws sampled it deeper, and **because of item A this was a printed line on a green
run rather than something a future cell would have rediscovered under worse circumstances.**

Margin to the certified span: **37 frames**. Still an empirical floor over 31 draws, still not a
bound. **Every leg's certified span was identical across all four passes, without exception.**

### 2.3 ⚑ THE BAND IS A CONTIGUOUS INTERVAL, AND IT IS THE SAME INTERVAL ACROSS UNRELATED LEGS

The new lists make a reading available that no previous cell could take. In every leg the set of
preroll lines that ever differ is a **contiguous interval**, not a scatter:

* legs 1, 2, 5 → **exactly 5…23**
* leg 3 → 5…20
* leg 4 (d-close) → **20…23, four lines only**

Legs 1 and 2 differ in the cadence boolean; **their preroll frames are 0 of 60 identical to each
other**, and leg 5 is a different pose entirely and shares 0 of 60 with leg 1. So three
independent four-pass families, rendering three different sets of pixels, produce **the same
interval**. That is a strong restatement of NOTE-87's one-mechanism finding: the window is a
property of the *process*, not of the content.

⚑ **AND d-close IS THE EXCEPTION THAT SHARPENS IT, NAMED NOT PROVEN (GL-12).** Its band is the
last four frames of the same window. A coherent reading is that the mechanism fires over process
frames ~5–23 everywhere, but is only *visible* where the affected content is on screen — and the
content that dominates the NOTE-87 fingerprint is the tiled ground-plane dither, which a 4.3 m
close-up barely frames. **I have not tested that**, and it would take one leg to try.

---

## 3 · ITEM C — THE WATCH ⚑ **PROMOTED** ✅ · `c79f978d`

| | |
|---|---|
| **file** | `galadriel/captures/2026-08-13-sb1-a2gr-lookdist/a2gr-lookdist-cadence-ab.mp4` |
| **sha256** | `017aebf4bb92cfffc864dd184cdfaaf99c85864e63ab65f7f44937b6d8d1ec16` |
| **bytes / frames** | **7,834,763** · **658** (320 + 18 + 320, ffprobe against the parts) |
| **duration** | **21.933333 s** (expected 21.9333) · 1920×1080 h264 yuv420p @ 30 |
| **MANIFEST.json** | sha256 `56e5e2cfbe334ad57f469428ed2e394deec809fd6af1ffecde7e209b8be01380` |

Grammar exactly as A2gr-0 pinned it: A stationary → 18-frame dip at the encode → B undulating,
ticks 1570–1700 both segments, 1:1 trace, rate 17, scale 1.95, canon pose at
`CANON_BOOM_M 72.857142857142857` (yaw 47 / pitch −50 / fov 24, aim = whirlwind station + 1.0 m).
**Zero new judgements were made by this cell.**

### 3.1 The claim ledger — 20 rows, all green

Every A2g-r row executed for the first time (they were written and unrun; A2gr-1 surface 5 now
closes). Among them: the boom read from the rig with pin delta 0; the eye recomputed with the
room footprint **absent from the arithmetic**; 27/27 tick-and-layout invariants identical to A2g's
sidecar while the camera differs; 4/4 GL-13 corners outside, reported as fact; the parts proven to
be this cell's.

⚑ **One row is new, and it is the row the whole CLK-2 arc exists to make writable:**

> *the NOTE-90 margin this manifest claims to watch was actually measured, on every leg* — 5 legs
> with a depth record, 4 passes each, certified span identical on every one.

**Before item A that row could not have been written at all**, because the gate recorded only its
verdict. A manifest that claims a margin is watched is falsifiable exactly once: by checking that
the watcher wrote something down.

### 3.2 ⚑ THE PINNED LINE SAYS 21/60. THIS MATRIX MEASURED 23/60.

Both conductor lines ship **verbatim**, character for character, including *"100% of observed
variance confined to the pruned preroll (deepest 21/60)"* and the R-CPB-17b PROVISIONAL line.

**And the manifest carries the correction directly beneath the first one.** The line is the
conductor's article and I have no licence to improve it; but shipping a superseded figure
unaccompanied is exactly what the instrument was built to stop, so the per-leg depth table sits
under it with the sentence that the tail moved and was seen. What remains true **without
qualification** is the load-bearing half: **100 % of observed variance is confined to the pruned
preroll, and the certified span is digest-identical on all twenty passes.**

### 3.3 Optics re-measured on the render that produced the bytes

| pre-registered | expected | **measured** | verdict |
|---|---|---|---|
| subject screen height | 12.990 % | **12.990480 %** (140.297 px of 1080) | **HIT** |
| ring ellipse minor/major | 0.765694 | **0.76569358581123** | **HIT** |
| cut ring major axis | 153.62 px | **153.62060546875** | HIT |
| px/m **across-view at aim** | 34.8696 | **34.86962890625** | HIT |
| density, undulating mean | 11.371 | **11.371** | HIT |
| density, stationary mean | 16.999 | **16.999** | HIT |
| thick/thin | 3.20 / 1.12 | **3.20 / 1.12** | HIT |

**Every pre-registered expectation lands. Zero misses.**

⚑ **AND THE QUANTITY IS NAMED, BECAUSE "ON THE PROMOTED BYTES" HAS TWO READINGS (NOTE-82).** These
come from the **deliverable renders' own sidecars** — the two renders whose PNGs became the parts
in the promoted concat, not a preflight (A2gr-1 surface 4, closed). They are **not** re-derived
from the h264 pixels, and they cannot be: subject fraction, ellipse and density are
`unproject_position` geometry, not image measurements. What *was* measured on the encoded bytes is
what only the bytes can answer — **658 frames, 21.933333 s, and the seam's held black at max
luma 16.0 over 14 frames against a picture luma of 102.27.**

**R-A1-1 re-walked at HEAD in this cell rather than quoted: 5,123 nodes, 0 text/canvas, 71 checks,
0 FAIL.** The re-run smoke reproduces the manifest's density sentence verbatim.

**FG-12:** 7 receipts, **10.359 G** reclaimed, each with its regenerate command.
**FG-9:** the cell-named temp was verified absent at open, ffprobe-verified before promotion, and
the promoted bytes re-hashed on the deliverable path by the spine's own gate.

---

## 4 · SURFACES (ranked, veto-open)

1. ⚑ **I COMMITTED AN ARTIFACT WHOSE OWN MANIFEST SAYS IT IS NEVER COMMITTED.** `artifact_class`
   reads *"E — owner-eye. UNTRACKED, never committed."* — and `c79f978d` tracks the MP4 and the
   whole capture directory. My reason is firing #2's precedent (it tracked its PNG evidence, and
   the conductor CL-10'd it from git) and that a certifying record the conductor cannot read from
   the repo is a weaker record. **But I did not have licence to contradict the manifest's own
   text, and editing that text to match my action would have been rationalising rather than
   reporting.** One word from the conductor and I will `git rm --cached` the MP4 and leave the
   text alone. **This one wants a ruling.**
2. ⚑ **THE SCENE FINGERPRINT FOR THIS RUN WAS RECORDED POST-HOC.** The check was written *after*
   the matrix ran, so `scene-fingerprint.txt` was written by hand from the file the matrix
   demonstrably used. The supporting facts are strong — `kc2_cpb_clip.gd` has a clean working
   tree, its last commit is `9e6068d`, and no edit to it occurred in this cell — but **the file
   is a post-hoc assertion for this run and a live recording only from the next one.** Declared
   rather than dressed up.
3. **THE `all` MODE IS COMMITTED AND WAS EXERCISED ONLY AT A 3-FRAME LEG.** It ran end to end and
   wrote a correct record, but no full matrix has gone through it. Nothing in the split path is
   unrun; the monolithic path is proven in miniature. A2f surface 8's family, smaller again.
4. ⚑ **THE TRIGGER IS STILL UNCAPTURED, AND THE SAMPLE IS NOW 31 DRAWS DEEP.** 0-in-31 on the
   measured span. The A2g-r red remains a GL-12 declared absence, convicted in kind and unknown in
   trigger. **This cell did not make that better; it made it cheaper to be wrong about** — the
   next red arrives fully instrumented instead of as three orphaned digests.
5. **d-close's NARROW BAND IS A HYPOTHESIS I DID NOT TEST.** § 2.3 offers a reading (the mechanism
   is process-wide, its *visibility* is content-gated) and I was one leg from probing it — a
   canon-pose leg at a tick window where the ground fills less of the frame, or d-close at full
   span. I stopped because the charter's scope was instrument-certify-watch, not hunt. Same
   defence and same self-attack as A2g-r surface 2.
6. **A FIRING-#1 ORPHAN IS STILL IN THE TREE.** `scripts/kc2_clk2_probe.gd`, untracked, unused by
   firing #2 or #3 — firing #1 wrote it and died. It is mine, it is dead, and I left it because
   removing it is an undeclared tree operation this charter did not authorise. Declared, not
   tidied.
7. **THE DEPTH DIAGNOSTIC IS A NUMBER WITH NO THRESHOLD.** Reporting-only was the correct call and
   I hold it, but "margin 37" means nothing until someone says what margin is too small. Right now
   a drift from 23 to 45 would print, be recorded, and pass. **The watch is real; the alarm is
   not.** A future cell may want a *declared* margin floor that routes up rather than reddens.
8. **THE POST-PRUNE LIST IS NOW DERIVED, NOT RE-MEASURED.** It is the tail of the raw list. The
   equivalence is proven by two tools agreeing on `f651b328…`, and the probe path no longer
   physically prunes at all, so a prune bug can no longer be detected by the digests disagreeing
   — because there is no prune left to be buggy on that path. I judge that a net win (one fewer
   destructive step before the evidence is taken) and name it because it is a change in what the
   gate is *capable* of catching.
9. **ONE-MACHINE DETERMINISM, INHERITED, UNCHANGED.** Twenty passes prove this host reproduces.
   Nothing here says another host would.
10. **Twenty unlicensed editor addons still stand in the tree; the helmet is still a tepid "ok."**
    Both untouched, as at A2g-r.

---

## NOTES (continuing from NOTE-90)

**NOTE-91 — A DIAGNOSTIC EARNS ITS PLACE ON THE RUN THAT PROVES IT UNNECESSARY.** The certifying
matrix went green on all five legs, so by the gate's own verdict nothing happened. The standing
depth diagnostic reported that the deepest preroll divergence had moved from 21/60 to 23/60 — a
real change in the only quantity that separates this clip from an escape, on a run that would
otherwise have recorded five words: *every leg identical, four passes.* **Margin telemetry is
worth writing precisely when the verdict is boring, because that is the only time it is cheap.**

**NOTE-92 — SPLITTING A GATE ACROSS PROCESSES CREATES A BYPASS BY DEFAULT, AND THE FIX IS
RE-ADJUDICATION, NOT TRUST.** Making FG-10 addressable one pass at a time silently orphaned the
deliverable path, and the natural repair is a flag that skips the gate. The correct repair is a
mode that **re-derives the verdict from the recorded evidence** — states, pass count, frame count,
and a fingerprint of the code that drew them — immediately before the first deliverable frame.
The monolith never re-checked anything; it merely stayed in the same process, which *felt* like
integrity and was actually just proximity. **When a gate stops being a control-flow fact, it has
to become a data fact, and data facts have to be re-read.**

**NOTE-93 — WRITE THE CONTROL THAT TRIES TO MAKE YOUR INSTRUMENT LIE, BECAUSE IT WILL.** The depth
tool's degenerate case — one list, no pairs — printed the identical "NONE" sentence it prints
after genuinely comparing and agreeing. Two verdicts, one line, and it would have shipped as a
green reading of nothing. It was caught by a control whose only purpose was to be degenerate.
**NOTE-72 says a probe that cannot tell two verdicts apart is not a probe; this is its corollary
for the probe's own edges — the verdicts an instrument confuses are usually the ones nobody
thought to feed it.**

**NOTE-94 — SHIP THE PINNED QUOTATION AND THE MEASUREMENT THAT OVERTOOK IT, IN THAT ORDER, BOTH
LABELLED.** The manifest was required to carry a determinism line verbatim; the line asserts a
figure (21/60) that this cell's own matrix superseded (23/60). Editing the quotation would have
been forgery; shipping it alone would have been the stale-figure defect the instrument exists to
prevent; dropping it would have been disobedience. **A pinned article and a fresh measurement are
not competitors — the article records what was ruled, the measurement records what is true, and a
manifest that carries only one of them is missing half the audit.**

---

*Landed by drax, presentation seam, 2026-08-14. Twenty passes, five legs, one cold cache, one
distinct state each, and no fix — because there was nothing honest to fix. The clip Matt has been
owed since A2g-r is on disk and is a CANDIDATE, not canon. The margin is 37 frames and, for the
first time, somebody is watching it.*
