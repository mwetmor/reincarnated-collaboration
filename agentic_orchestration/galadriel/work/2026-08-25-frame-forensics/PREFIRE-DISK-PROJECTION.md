# PRE-FIRE RESOURCE-BOUNDS PROJECTION — Discipline #1.1

**Written BEFORE any decode, fetch or transcode.** Dispatch
`2026-08-25-galadriel-reference-frame-forensics.md` § 3 makes this mandatory and
names the reason: `/System/Volumes/Data` hit 2.7 GiB free (0.6 %) earlier today and
halted a live build wave mid-tranche.

**Agent:** galadriel · **Date:** 2026-08-25 · **Fired after this file was written:** yes

---

## 0. Measured starting state

```
$ df -h /System/Volumes/Data
/dev/disk3s5   460Gi   377Gi    60Gi    87%   /System/Volumes/Data
```

**60 GiB free.** (Matt cleared to 66 GiB; 6 GiB has been consumed since by other
lanes — drax's godot renders landed `mp4_review_2026-08-25_v3/` at 17:23–17:24,
71 MiB, plus its PNG intermediates. **The floor is moving under me while I work
and the projection must budget for that, not for a static 60.**)

**Budget I hold myself to: 1 GiB.** Not because 1 GiB is what I need — it is
~25× what I need — but because a bound only disciplines if it is set below the
headroom. A projection that says "60 GiB free, therefore anything fits" is not a
projection.

---

## 1. THE ARCHITECTURAL DECISION THAT MAKES THIS CHEAP — declared first

**No decoded frame is ever written to disk.** Every clip is decoded by piping
`ffmpeg -f rawvideo -pix_fmt rgb24 - ` to stdout and consumed **frame-by-frame in
Python**, accumulating only per-frame derived statistics. There is no `frames/`
directory in this run and there will not be one.

This is a deliberate departure from the seam's usual practice (`wwcr_*` writes
123 PNGs; FG-12 then prunes them with a receipt). The usual practice is right
when the frames are *evidence*. Here they are *intermediate*, and 374 + 420
frames of RGB PNG at 720p–1080p is **~0.9 GiB written and then deleted** for no
evidentiary gain.

⚑ **Counter-argument recorded, because it cuts against me:** KR's note of
2026-08-25 § 5 says my own run supplied "the strongest evidence yet against the
discard fork" — the `_fxctl_` defect was recoverable **only** because 20
superseded PNGs were still on disk. **Streaming decode forfeits that recovery
path.** I accept the forfeit here on a specific ground: the source media are
**re-derivable at zero information loss** (the `.flv` is on Blizzard's CDN with a
2012 mtime and a pinned sha256; our mp4s are on disk and pinned). What was
unrecoverable in the `_fxctl_` case was a *render*, which costs GPU-minutes and a
serial lane. A decode costs 30 seconds. **The retention argument applies to
renders, not to decodes**, and collapsing the two would over-generalise a good
finding.

---

## 2. Line-item projection

| # | Item | Method | Bytes | Persisted? |
|---|---|---|--:|---|
| 1 | Reference master `whirlwind.flv` | `curl` from Blizzard Akamai | **6,872,672** (measured by RT-4 `Content-Length`, not estimated) | yes — `media/`, **untracked** |
| 2 | Reference decode, 374 fr @ 1280×720 | **stdout pipe** | **0** | no |
| 3 | Ours decode, ≤660 fr @ ≤1920×1080 | **stdout pipe** | **0** | no |
| 4 | Transcode-null `O′` (ours → 1280×720 @ ~4.4 Mbps, see § 4) | `ffmpeg` encode | ~**4.0 MiB** | yes — `media/`, **untracked** |
| 5 | Per-frame series JSON, 3 legs × 4 series | numpy → json | ~**6 MiB** worst case (660 rows × ~200 floats × 3 legs, ASCII) | **yes — committed** |
| 6 | Evidence PNGs (crops, ladders, spectra) | matplotlib / PIL | ~**25 MiB** (≤12 files) | **untracked**, sha-pinned in the note |
| 7 | Instrument code + notes | text | <200 KiB | **yes — committed** |
| | **TOTAL NEW ON DISK** | | **≈ 42 MiB** | |

**42 MiB against 60 GiB free = 0.068 % of headroom. Margin ≈ 1,460×.**
**42 MiB against my self-imposed 1 GiB bound = 4.2 %.**

> **VERDICT: FIRE.** The projection clears both the real headroom and the
> self-imposed bound by more than an order of magnitude, and it clears them
> *because* of the § 1 streaming decision, not in spite of the corpus size. Had I
> written frames to disk the figure would have been **~0.95 GiB** — still safe
> against 60 GiB, but 95 % of my own bound, and I would have wanted to know that
> before firing rather than after.

---

## 3. THE BINDING CONSTRAINT IS RAM, NOT DISK — and the dispatch does not say so

§ 3 of the dispatch projects "frames × resolution × bytes-per-frame against
`df -h`". **That arithmetic is right and it is pointed at the wrong resource.**
Streaming decode drives disk to zero and moves the entire cost into memory:

| leg | frames | raster | naïve full-array RAM (uint8 RGB) |
|---|--:|---|--:|
| reference | 374 | 1280×720 | **1.03 GiB** |
| ours (60 fps) | 420 | 1920×1080 | **2.61 GiB** |
| ours (658 fr, ww7) | 658 | 1920×1080 | **4.09 GiB** |

**A naïve "decode it all into an array" would have cost 4 GiB of RAM on the
largest leg** — invisible to `df`, and the failure mode is a swap storm or an
OOM kill mid-run, not a clean disk-full error.

**Mitigation, adopted:** two-pass streaming.
- **Pass 1** samples **48 evenly-spaced frames** for the background plate and the
  noise-floor derivation. 48 × 1280×720×3 = **132 MiB** peak.
- **Pass 2** streams every frame, holding a **3-frame ring buffer** (~8 MiB) plus
  the accumulating series (~KiB).

**Projected peak RSS: ~200 MiB per leg, legs run sequentially.** 20× under the
naïve figure and ~30× under the largest naïve leg.

---

## 4. Decode parameters chosen, and WHY each is the cheap-but-sufficient choice

The dispatch asks me to say which reduction I chose. I chose **two, on different
axes, for different reasons** — and one *non*-reduction:

**(a) Common working raster = 1280×720 — a downscale of OURS, never an upscale of
the reference.** The reference is natively 1280×720; ours is 1920×1080. Comparing
them on their native rasters is exactly the incomparability KR flagged in § 4 and
that **my own ruling of this morning already measured**: across a 16× pixel-count
range on identical frames, a component *count* moved **+426 %** while a mass
*fraction* moved **+9.4 %** (`notes/2026-08-25-xrow-significant-components-instrument-ruling.md`
§ 5.2). Equalising the raster removes the largest term of that exposure before
any statistic is computed. Downscaling ours destroys real information; upscaling
the reference would *fabricate* it. **Between destroying information and
inventing it, destroy.**

**(b) Common frame rate = 30 fps.** Reference is 30000/1001 ≈ 29.97; ours is 60.
Matt's phenomena — cadence, intermittency, scrape *timing* — are quantities in
**seconds**, so the series must be indexed in time, not in frames. 30 fps is not a
concession on the reference leg: **29.97 fps is a hard Nyquist ceiling of 14.985 Hz
and no decode choice of mine can raise it.**
⚑ **But decimating ours 60 → 30 can ALIAS a real 20 Hz flicker down to 10 Hz and
present it as a finding.** Mitigation, pre-registered here: **ours is decoded at
BOTH 60 and 30**, and any periodicity found at 30 is checked against the 60 fps
series before it is reported. Cost: one extra streaming pass, zero extra disk.

**(c) The NON-reduction: the resolution ladder is NOT collapsed.** Every series is
computed at **320×180 / 640×360 / 960×540 / 1280×720** rather than once at the
primary raster. This quadruples compute (~4 min total, measured below) and adds
nothing to disk. It is the only way to answer KR's § 4 bullet 2 — *is this
operator scale-sensitive enough that the two legs are incomparable?* — **with a
measurement instead of an opinion.** The ladder is not overhead; on this dispatch
it is the primary product.

---

## 5. Compute projection

| stage | est. wall |
|---|--:|
| fetch reference (6.5 MiB) | ~5 s |
| decode reference ×4 ladder rungs | ~60 s |
| decode ours ×4 rungs ×2 fps | ~150 s |
| transcode-null encode + decode | ~40 s |
| series computation (FFT, phase-corr, pyramids) | ~120 s |
| **total** | **~6 min** |

No background process, no `sleep` loop, no lane held. Serial godot lane
**untouched — I render nothing** (§ 5 of the dispatch).

---

## 6. What would make me stop

Pre-registered halt conditions, so that stopping is a rule and not a mood:

1. `df` on `/System/Volumes/Data` drops **below 20 GiB** at any check → halt, do
   not decode further, report what exists.
2. Peak RSS exceeds **1 GiB** → halt the ladder, fall back to the primary raster only.
3. Total new bytes exceed the **1 GiB** self-bound → halt and re-project.

`df` is re-checked after the fetch, after the transcode, and at the end. Those
readings are appended to § 7 as they are taken, so the projection is falsifiable
against its own outcome rather than being a form filled in once.

---

## 7. Post-hoc actuals — TO BE FILLED AFTER THE RUN

**Deliberately empty at fire time.**

⚑ **Recorded because I caught myself doing the thing this dispatch exists to
stop.** My first draft of this file filled this table in *before firing*, with
plausible figures I did not have. They read as measurements. **A projection whose
verification section is written in advance is not a projection with a
verification section; it is a longer projection wearing one** — the same shape as
a gate that "returns cleanly and returns an answer to a different question"
(dispatch § 0), and the fourth instance of that shape in this run had I shipped it.

| item | projected | actual |
|---|--:|--:|
| reference `.flv` | 6,872,672 B | *pending* |
| transcode-null `O′` | ~4.0 MiB | *pending* |
| decoded frames on disk | 0 | *pending* |
| series JSON | ~6 MiB | *pending* |
| evidence PNGs | ~25 MiB | *pending* |
| **total new on disk** | ≈ 42 MiB | *pending* |
| peak RSS | ~200 MiB | *pending* |
| wall | ~6 min | *pending* |
| `df` free, end of run | — | *pending* |
