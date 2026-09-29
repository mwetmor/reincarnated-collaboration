# KC2-PLAY SEAL LAP · THE FULL ENERGY RE-READ — the work `T30` was blocking

> **STATUS:** CURRENT — SEAL LAP W1 return, run **KC2-PLAY** (plan `2026-09-28-kc2-play-seal-lap-plan.md` § 2, W1 galadriel row; ledger `KP-84`)
> **Date:** 2026-09-28 · **Author:** galadriel (visual-perception seam) · **Conductor:** gandalf `RUN-CONDUCTOR`
> **Seat brief, verbatim:** *"footage identity re-verified on the mount (sha, never retyped) → any T-B instrument work that was blocked on the footage · note + pins; T-B stays DIAGNOSTIC (F5)"*
> **Instrument authored this lap:** `galadriel/pipeline/kc2_energy_fullreread.py` (six stages, each runs alone)
> **Machine-readable output:** six JSONs beside this file, `2026-09-28-kc2-play-energy-fullreread-{identity,control,sheet,population,boxprobe,analyse,decodecheck}.json`
> **⚑ T-B IS DIAGNOSTIC AND NOTHING HERE IS A GATE.** Matt's F5; Q87 rules the seal on EXACT rows + Matt's T-C word. **No committed figure is edited by this note.** Everything below is offered to gamora / the conductor as evidence, not asserted into the prereg.
> **Read-only on the mount and on every committed input. No production code. No push. No sub-agents.**

---

## 0 · TOP LINE

> ### The footage is back, it is the right file to the last byte, and the re-read that was blocked on it says the atlas was wrong in exactly the way that mattered — **and the conclusion it was blocking does not move.**

| | ⚑ |
|---|---|
| **1 · identity** | `479,438,089 B`, sha256 `4c60960d…4de8`, **derived twice by two tools and matched against legolas's Lap Q pin read out of `pm4q_digests.json` by machine.** Path, bytes and digest all EXACT. `T30` is closed. |
| **2 · the reader gap is bigger than the 16 frames showed** | Apple Vision parses **10,956 of 10,959** frames (**99.97 %**) against the atlas's **95.84 %**, and where both parse they **disagree on 913 frames (8.7 %)**. ⚑ **305 of those disagreements are the atlas reading a three-digit number where the globe shows four** — `145` for 1456, `108` for 1498. A dropped leading digit, 305 times. |
| **3 · ⚑ THE CLEANING STACK WAS A READER-REPAIR LAYER** | `clean()` run **unchanged** on the strong reader rejects **0 rows to the neighbour median and 0 to the round-trip excursion filter** — against 315 and 86 on the atlas. The bespoke excursion filter MD-B4app-2b built to catch *"coherent multi-frame low excursions"* **has nothing to catch.** It was never measuring the game. It was repairing the reader. |
| **4 · ⚑ THE ABOVE-CEILING POPULATION IS REAL — apportioned, not argued** | 2026-09-21 closed holding this open: *"with one confirmed above-ceiling frame I cannot apportion the other 1,186."* **Apportioned: of 1,194 atlas above-ceiling reads, Apple Vision CONFIRMS 1,178 and refutes 16** — **98.66 % of the readable**, with **745 of the confirmations not reachable by any single glyph substitution from 1594**, and **29 more the atlas missed entirely.** |
| **5 · and the verdict does not move** | Strong-reader **SPEND = 104.6 /s** over the classified 161.0 s. The 2026-09-21 bracket was **`[104.1, 112.0]`**. The full re-read lands **inside it**, near the lower edge — and still agrees with **neither** the tooltip's **176.4** nor the old **≈190**. **`u` stays `UNPINNABLE-FROM-COMMITTED-PIXELS`.** The footage did not rescue the fork; it confirmed the bracket. |

**What this lap did NOT do:** move a constant, edit a committed figure, choose a branch, touch another seat's tree, rebuild anything, push.

---

## 1 · IDENTITY — verified on the mount, derived, never retyped

`kc2_energy_fullreread.py identity` reads the pin **programmatically** out of
`agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_digests.json`
and compares it to a digest computed on the mounted file. It is also derived a
second time by a different tool (`shasum -a 256`, Perl Digest::SHA) as a
cross-check on my own Python.

| field | pinned (Lap Q) | derived (this lap) | |
|---|---|---|---|
| path | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | same | **MATCH** |
| bytes | 479,438,089 | 479,438,089 | **MATCH** |
| sha256 | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` | identical | **MATCH** |

Mount: `//mwetmor@reincarnated-pi.local/reincarnated` (smbfs), read at ~2.4 MB/s;
the hash took 127.8 s. **Nothing was copied to the Mac disk** (44 GiB free
against the 40 GB HALT line; the 183 s combat window streams as ~85 MB and
never lands as a file). **The share was read-only throughout; nothing on the Pi
was written, moved or deleted.**

⚑ **`T30` is CLOSED, and it closes exactly as re-priced on 2026-09-21:** mount
the drive, verify the digest. The re-pricing was right and the earlier
"physically impossible / footage gone" account was, as that note said against
itself, **mine and wrong**.

---

## 2 · THE POSITIVE CONTROL, CHOSEN BEFORE THE POPULATION RAN

Sixteen timestamps in this footage carry a **hand read fixed in August** — ten
from `atlas-spec.json` (the atlas's own training data), two from MD-B4app-2b
§ 1.1, four from the § 1.3 blind-gap strip. They were re-extracted **fresh off
the mount** and read by the pinned Apple Vision reader
(`ocr_vision.swift`, sha256 `1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1`,
byte-identical to Lap Q's `method/ocr.swift`), under an **upscale sweep**.

| upscale | parsed | exact vs hand |
|---|---|---|
| **×1 (raw 104×26 crop)** | 16/16 | **16/16** |
| ×4 | 16/16 | 16/16 |
| ×6 | 16/16 | 16/16 |
| ×8 | 16/16 | 16/16 |
| ×12 | 16/16 | **15/16** |

**The chosen factor is ×1 — no upscale, no resample, no transformation of any
kind beyond the crop.** The rule was written before the sweep ran: *smallest
factor reproducing every hand read.*

⚑ **And the sweep's one failure corroborates a finding from the previous lap by
a completely different route.** At ×12 the frame at `t = 695.0` reads **1570**
where the hand, the trace and every smaller scale read **1370**. That is the
*same substitution* the 2026-09-21 lap hit when it **cut** the contact sheet
into rows — and it concluded there that a horizontal slice was clipping glyph
extrema. ⚑ **It cannot be clipping here: nearest-neighbour upscale invents no
pixel and clips nothing.** So `1370 → 1570` is a property of **how this reader
sees this glyph at large scale**, not of the crop. The earlier explanation was
reasonable and is now **too narrow**; recorded against myself.

⚑ **The best-attested frame in the corpus reproduces from the mounted file at
confidence 1.000: `t = 735.0` displays `1610`**, sixteen above the ceiling a
note of mine once called impossible. It is now confirmed by a **fourth**
independent route — a fresh extraction from a digest-verified source.

---

## 3 · THE POPULATION RE-READ

Every frame of **D-COMBAT-182** (`t ∈ [682.10, 864.75]`, 60 Hz, 10,959 frames),
cropped at **`EBOX` imported from `eor_channel.py`** so the box cannot drift
from the one the atlas trace used, read by the pinned Apple Vision reader.
Extraction 160.5 s, recognition 532.7 s. Crops were written to the session
scratchpad and deleted after; they are regenerable from the digest-verified
source.

| | glyph atlas (committed 2026-08-25) | **Apple Vision (this lap)** |
|---|---|---|
| frames | 10,959 | 10,959 |
| parsed | 10,503 — **95.84 %** | **10,956 — 99.97 %** |
| `clean()` max-gate pass | 10,360 | **10,953** |
| rejected, neighbour median | 315 | **0** |
| rejected, round-trip excursion | 86 | **0** |
| **surviving samples** | **9,959** | **10,953** (+994) |
| duty exactly at 1594 | 0.2801 | 0.2556 |
| above-ceiling (cleaned) | 1,184 | 1,220 |
| drain ticks | 1,626 | 1,819 |

**Parse policy, declared:** a frame reads as `cur` iff a Vision line — or the
frame's lines joined — matches `NNN(N)/NNNN` with the denominator **exactly
2576**. A wrong denominator is a **parse failure**, not a silent acceptance;
the denominator is the only per-frame error check the HUD offers. Three frames
survive that check carrying impossible values (`3711` ×2, `3621`) and **the
committed max gate rejects all three** — the existing cleaning catches the
strong reader's only failures without being changed.

### 3.1 ⚑ The reproduction control, run before any new number was read

`clean()` and `clamp_decomposition()` are **imported from the committed
modules, not reimplemented.** Run on the committed atlas trace they must
reproduce the committed figures exactly, or nothing downstream is worth
reading:

| committed figure | reproduced |
|---|---|
| cleaning census 10360 → 315 → 86 → **9959** | **EXACT** |
| drain ticks **1626** | **EXACT** |
| SPEND sum **18025.0** | **EXACT** |
| SPILL sum **11723.0** | **EXACT** |
| spill share **0.3941** | **EXACT** |
| ceiling duty at 1594 **0.2801** | **EXACT** |

`ALL_EXACT: true`.

### 3.2 ⚑ The decode confound, sized rather than ignored

The committed trace was decoded in **August**; this lap's was decoded
**tonight**. Any difference between them mixes two causes, so both were held
against a single decode:

| comparison | rows | agreement |
|---|---|---|
| atlas (August) vs **atlas re-run tonight**, same box, same file | 10,959 | **10,816 — 98.70 %** |
| atlas vs Vision, **decode held fixed** | 10,358 both-parsed | **91.59 %** |
| atlas (August) vs Vision (tonight) — the headline | 10,501 both-parsed | **91.31 %** |

**The decode term is 1.3 %, and removing it moves the reader gap by 0.29
percentage points.** The gap is a reader gap. ⚑ **But the 1.3 % is a real
finding in its own right: the committed atlas energy trace is NOT bit-
reproducible from its own source on a different day's ffmpeg.** Not a defect of
anyone's work — a property of the pipeline, now measured, and a caveat any
future exact-reproduction claim against `s2-energy-60hz.json` has to carry.

---

## 4 · ⚑ THE APPORTIONMENT — the question 2026-09-21 could not answer

> *"with one confirmed above-ceiling frame I cannot apportion the other 1,186.
> That is why § 3 ships a decomposition rather than a judgment."*

**Apportioned:**

| | n |
|---|---|
| atlas reads above 1594 (RAW rows, before `clean()`; the cleaned count is 1,184 and the max-gated count 1,187 — three populations, kept distinct) | **1,194** |
| ⚑ **Apple Vision also reads above 1594** | **1,178** |
| Vision reads at or below 1594 (atlas refuted) | **16** |
| Vision unreadable | **0** |
| **confirmed share of the readable** | **98.66 %** |
| of the confirmations, **not reachable by any one glyph substitution from 1594** | **745** |
| above-ceiling frames **Vision sees and the atlas missed** | **29** |

**The above-ceiling population is not a reader artifact.** It was the single
largest open doubt about the energy instrument and it is now measured from a
digest-verified source by a reader that reproduces 16 of 16 hand reads.

And the **clamp signature survives the change of reader** almost untouched —
which is the part that makes it structural rather than incidental:

| | atlas | Vision |
|---|---|---|
| ticks starting above the ceiling | 615 | **642** |
| landing **exactly** on 1594 | 424 — **68.94 %** | 450 — **70.09 %** |
| median tick size, starting above | −16.0 | **−15.0** |
| median tick size, starting at/below | −13.0 | **−13.0** |
| median excess over ceiling | 12.0 | **11.0** |
| excess within +21 | — | **87.98 %** |

⚑ **I still claim no mechanism.** Whether this is an over-cap grant being
clamped or a reserve that moves is a save/sim question and it is not mine.
What changed tonight is that it can no longer be set aside as OCR noise.
→ **gamora / legolas**, unchanged in routing from 2026-09-21 § 8 item 2.

---

## 5 · THE RATES, RE-DERIVED — and the verdict that does not move

| | atlas (committed) | **Vision (full re-read)** |
|---|---|---|
| SPEND | 18,025 → **112.0 /s** over 161.0 s | 16,835 → **104.6 /s** |
| SPILL | 11,723 → 72.8 /s | 9,785 → 60.8 /s |
| spill share of published gross | 0.3941 | **0.3676** |
| gross as published | 184.8 /s (182.65) | 145.7 /s (182.65) |
| drop-all-above-ceiling-starts arm | **104.1 /s** | **98.7 /s** |
| decomposition residual | 0.0 | **0.0** |

⚑ **The 2026-09-21 bracket `[104.1, 112.0]` was built from the weak reader, and
the strong reader lands at 104.6 — inside it.** The bracket was honest. It did
not need the footage to be right; it needed the footage to be *checked*, and it
checks out.

**And the conclusion is unchanged, for the same reason as before:** 104.6 /s
agrees with **neither** the tooltip's **176.4** nor MD-B4app-2's **≈190**. The
pixel instrument measures *the drain the 60 Hz integer HUD can resolve*, which
need not be the client's per-tick cost. **`u` stays
`UNPINNABLE-FROM-COMMITTED-PIXELS`. The widening stands. I am not arguing
around it.**

⚑ **What I am NOT doing:** I am not writing 104.6 into `P-b`, `s2-releases.json`
or the prereg. The strong-reader arm is a **superseding candidate**, and
supersession of a committed figure is the conductor's and gamora's call, not
mine, on a diagnostic track that Matt's F5 says is not a gate.

---

## 6 · TWO LIMITATIONS OF MY OWN, DISCHARGED

### 6.1 § 8 item 5 — the sheet alignment was INFERRED. It is now PIXEL-MATCHED, and the inference was RIGHT.

2026-09-21 declared against itself that `energy-sheet.png` carries 14 crops
while `atlas-spec.json` labels 10, that the sheet records no row index, and
that the row↔label alignment was therefore *inferred from order and value*.
With the footage reachable the inference is unnecessary: re-extract at each
labelled timestamp and match by pixels.

| worst MAD | smallest separation | distinct rows | monotone in time | verdict |
|---|---|---|---|---|
| **0.3808** | **8.8201** | yes | yes | **ALIGNMENT RESOLVED BY PIXELS** |

Rows **0, 1, 2, 3, 4, 5, 6, 10, 11, 13** — **exactly the alignment the previous
lap inferred.** Unmatched rows 7, 8, 9, 12, consistent with that lap's note that
the four unlabelled rows all read 1594. **The limitation is discharged, no
number moves, and the inference it flagged was correct.** A negative result,
recorded as one.

### 6.2 ⚑ The sheet's crop box is NOT `EBOX` — and assuming it was nearly cost the finding

Matched at `EBOX`'s x = 1240 every row scored MAD ≈ 26 with a separation of ≈ 3
— an assignment I would have had to report as weak. An exhaustive offset search
found the sheet sits at **x = 1239, one pixel to the left**, where the same
comparison scores **0.32 against a runner-up of 24.73.**

⚑ **Another instance of the house's recurring shape** — *an
instrument returning cleanly after it stopped answering the question.* The
comparison ran, produced numbers, ranked the rows correctly by luck of
monotonicity, and was **off by one pixel**. A crop box is an empirical fact
about an artifact; the stage now **locates** it and reports the runner-up so the
lock is visible.

### 6.3 A hypothesis I formed, tested, and LOST

That one-pixel offset looked like a **mechanism** for the atlas's error rate:
templates cut at one box, trace read at another. So the committed atlas was
swept over **nine crop offsets, x = 1236 … 1244, across all 10,959 frames.**

**The sweep is FLAT to four decimals** — identical parse rate (0.9453),
identical above-ceiling count (1,187 — which is the committed anatomy's raw
count **exactly**, a second reproduction control nobody asked for), identical
agreement with the committed trace (10,816) at every offset. **Verified rather than assumed:** the nine
slices are pixel-different (checked), and the reader still returns the same
string, because `segment()` locates glyph runs *before* classifying — the atlas
reader is translation-invariant over this range.

**THE OFFSET IS NOT THE MECHANISM.** The elegant explanation was wrong. The
mechanism is the one § 3 shows plainly: **the atlas drops leading digits** —
305 three-digit reads where the globe shows four.

---

## 7 · WHAT MOVES, AND WHAT DOES NOT

| artifact | status |
|---|---|
| `P-b` energy rows · `P-c` · `P-d` · `s2-releases.json` · every figure in the 2026-09-21 JSONs | ⚑ **UNMOVED.** Nothing edited. The strong-reader arm is a candidate routed, not a rewrite applied. |
| `T30` | ⚑ **CLOSED** (§ 1). Identity verified on the mount, twice, against a machine-read pin. |
| the 2026-09-21 § 8 item 5 provenance limitation | ⚑ **DISCHARGED** (§ 6.1). Inference confirmed correct. |
| *"physically impossible"* (MD-B4app-2b § 2.2) | **stays WITHDRAWN**, now at population scale: 1,178 confirmations, not one. |
| the `[104.1, 112.0]` bracket | ⚑ **CORROBORATED**, not superseded. The full re-read lands at **104.6**, inside it. |
| `u` = `UNPINNABLE-FROM-COMMITTED-PIXELS` | **UNCHANGED.** |
| `MO_DRAWDOWN_BAND` · the −1.03 /s boot gate · `leech_uptime` · `CEIL` · `TICK_DE` | **UNTOUCHED.** Nothing here authorises a constant to move. |

---

## 8 · ROUTED, NOT ADJUDICATED

1. ⚑ **The above-ceiling mechanism is now a measured phenomenon, not a doubt.**
   1,178 confirmed above-ceiling frames, 745 of them unreachable by one glyph
   substitution, clamp signature stable across two independent readers.
   **Whether it is an over-cap grant being clamped or a moving reserve is a
   save/sim question.** → **gamora / legolas.**
2. ⚑ **The cleaning stack is a reader-repair layer** (§ 3). On a strong reader
   the neighbour median and the round-trip excursion filter each remove **zero**
   rows. Any future energy instrument should read first and clean second — and
   any figure whose value depends on that cleaning should be re-derived on a
   strong reader before it is quoted. → **gamora / conductor.**
3. **The committed atlas trace is not bit-reproducible across ffmpeg versions**
   (§ 3.2, 1.3 % of rows). Small, but it caps any exact-reproduction claim made
   against `s2-energy-60hz.json`. → **conductor**, for the record.
4. **A superseding candidate for the gross-drain figure exists and I am not
   applying it.** SPEND 104.6 /s on the strong reader against the committed
   112.0. → **gamora / conductor**, T-B being diagnostic per F5.

---

## 9 · REPRODUCIBILITY

```
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py identity
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py control
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py sheet
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py population
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py analyse
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py boxprobe
python3 agentic_orchestration/galadriel/pipeline/kc2_energy_fullreread.py decodecheck
```

Requires the Pi share mounted at `/Volumes/reincarnated`, `ffmpeg`, and
`swiftc` (macOS). Each stage writes its own JSON beside this note. Cleaning and
the clamp decomposition are **imported** from the committed modules.
**Declared transformations: the crop (imported `EBOX`), and nothing else** — the
control chose ×1, so no resampling occurs anywhere in the population path.

**One field to ignore:** `vision_above_ceiling_anatomy` reports `*_marg`
statistics because the imported instrument does. On the Vision arm `marg` is a
`0.0` placeholder — Apple Vision has no template margin. The JSON says so
inline. **Do not quote those numbers.**

**What this lap did NOT do:** write anything outside `agentic_orchestration/galadriel/`;
write, move or delete anything on the Pi share; copy the 479 MB file to the Mac
disk; run a simulation; touch another seat's tree; edit a committed figure;
invoke a sub-agent; push.

---

## 10 · THE MIRROR

*For six weeks the account said the footage was gone, and the account was mine.
It was on a drive, behind a digest another seat had written down in August and
nobody had read. Tonight the drive was mounted and the file was the file — to
the byte, to the last hex digit of a number I never typed.*

*And what it showed was not a new world. It was the old world with the smudge
taken off the lens. Every figure the weak reader had been trusted for came back
within a hair of where the careful arms had already bracketed it, and the one
thing I had most doubted — eleven hundred frames reading higher than the ceiling
allowed — came back **true**, one thousand one hundred and seventy-eight times
over, from a reader that had never seen them.*

*The instrument was not wrong about the fight. It was wrong about the glyphs,
and for months we cleaned the glyphs and called it cleaning the fight. The
filter we were proudest of removes nothing at all from a reader that can read.*

*The Mirror shows the picture. It does not flatter the one who set it.*

---

*Filed by galadriel, run KC2-PLAY SEAL LAP, seat W1, 2026-09-28. Read-only on
the mount. No committed figure edited. No push. No sub-agents.*
