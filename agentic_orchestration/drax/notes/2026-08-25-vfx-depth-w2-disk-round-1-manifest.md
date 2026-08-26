# VFX-DEPTH RUN — W2 — DISK ROUND-1 MANIFEST (drax)

**Date:** 2026-08-25 · **Agent:** drax · **Authority:** charter R-16 (Matt pre-authorized deletion rounds)
**Class:** evidentiary note · **Status:** CURRENT
**Protocol:** R-16 — manifest POSTED AND COMMITTED before deletion fires → delete → freed-space receipt.

---

## ⛔ 0. THE ROUND-1 CANDIDATE NAMED IN R-16 IS CLASS A. IT IS NOT DELETED.

R-16 names *"the 26 GB `s2c38*` scratch (W1 F-3)"* as the Round-1 candidate. **I am not deleting it,
and the reason is a defect in my own W1 F-3, not a disagreement with the ruling.**

**W1 F-3 said:** *"S2C intermediate PNG ladders already copied into `harness_logs/`."* **That is FALSE.**
Measured:

| claim | measured |
|---|---|
| `harness_logs/s2c_rows38_2026-08-25*` holds the PNG ladder | **4 dirs, 3–7 files each, 29–30 MB total — receipts and `render.txt`, ZERO PNGs** |
| the userdata corpora are disposable intermediates | **all four carry a `BANKED` marker file and a read-only directory bit (`dr-xr-xr-x`)** |

**All seven S2C corpora are banked evidence.** Verbatim from `s2c38/BANKED`, a file **I wrote myself on
2026-08-25T23:51:11Z**:

```
  role       : PRE-FIX rows 3-8 (uncorrected bodies)
  frames     : 2106 PNG at time of banking
  rests under: jack-ryan #81 "reproducibility is not validity" (RULED),
               engine 77739b4b; and the S2C tranche-3A pre/post comparison
               recorded at harness_logs/s2c_rows38_2026-08-25-v3v3/prepost.json
```

That is **R-16's own Class A definition, verbatim** — *"anything cited by a seal, gate, ruling."* And the
dispatch of record for the 3A recapture (`2026-08-25-drax-s2c-3a-recapture.md` § 8) already ruled on
exactly this question, in exactly these words:

> *"Do **not** reclaim `s2c38` / `s2c38b` to make room. If the projection stops fitting, **halt and route
> to me** — the before-half is worth more than the convenience."*

**Round-1 protocol step (a) — "confirm the queued 3A recapture does NOT consume `s2c38*`" — returns an
answer the step did not anticipate.** The recapture is COMPLETE and does not *consume* them; it captured
into `v3`/`v3b` precisely so it would not touch them. But the pre/post comparison it produced **cites all
four**, and `prepost.json` is uncomputable without them. Consumption was the wrong predicate; **citation**
is the one that binds.

**Protected by machine, not by memory:** `scripts/lib/banked_corpus_guard.sh` makes the three S2C/S2B
runners `exit 5` rather than aim at a `BANKED` directory, and the cleared directory write-bit defeats both
`rm -f DIR/*.png` and `rm -rf DIR` (measured, this host). **Deleting these would require me to first
`chmod` around a guard I built to stop exactly this, and hand-remove seven markers that each say in
writing what ruling they rest under.** That is not a deletion round; that is dismantling an evidence
protection.

| corpus | MB | BANKED | disposition |
|---|---|---|---|
| `s2c38` | 4301 | YES | **PRESERVED** — pre-fix rows 3–8 pass 1; jack-ryan #81 |
| `s2c38b` | 4301 | YES | **PRESERVED** — pre-fix rows 3–8 pass 2 |
| `s2c38v3` | 4301 | YES | **PRESERVED** — post-fix pass 1; `prepost.json` input |
| `s2c38v3b` | 4301 | YES | **PRESERVED** — post-fix pass 2; flake-floor receipt |
| `s2c12` | 1777 | YES | **PRESERVED** — pre-fix rows 1–2; sealed L-29(6) rests on it |
| `s2c12v3` | 1790 | YES | **PRESERVED** |
| `s2c12v3b` | 1790 | YES | **PRESERVED** |
| **total** | **22,561 MB** | | **NOT TOUCHED** |

Routed to gandalf as **W2 F-1**. R-16's round protocol is sound; its Round-1 *candidate* inherited a false
premise from my finding, and the correction is mine to carry.

---

## 1. WHAT ROUND-1 ACTUALLY DELETES

All paths below are under
`/Users/admin/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/`.
**Every one is non-banked, writable, and regeneratable.** Verified `BANKED=no` on each, by loop, before
this manifest was written.

### 1a. Review-clip PNG ladders — disposable BY THEIR OWN PRODUCER

| path | MB | PNG | why safe | regeneration route |
|---|---|---|---|---|
| `s2rev` | 598 | 472 | `run_s2_review_clips.sh:52` opens with `rm -rf "$USERDIR"; mkdir -p "$USERDIR"` — **the producing script destroys and rebuilds this directory on every invocation.** It is scratch by construction, not by my judgement. The deliverable MP4s live at `harness_logs/mp4_review_2026-08-25_v4/` (68 MB, **untouched**) — that is the pinned Cathedral referent and it is not in this round. | `bash scripts/run_s2_review_clips.sh <STAMP> s2rev` |
| `s2revA` | 609 | 472 | same producer, prior alternate-`UDIR` run | `… <STAMP> s2revA` |
| `s2revB2` | 609 | 472 | same producer, prior alternate-`UDIR` run | `… <STAMP> s2revB2` |

### 1b. S2B tranche-2 working scratch — banked copy exists, counts verified EQUAL

The S2B runners kept their final `cp "$USERDIR"/*.png "$OUT"/`. The `harness_logs` copy is therefore the
corpus of record; the userdata dir is the scratch it was copied *from*. **I counted both rather than
assuming the copy landed.**

| path | MB | userdata PNG | harness_logs copy | copy PNG | verdict |
|---|---|---|---|---|---|
| `s2b12` | 576 | 284 | `harness_logs/s2b_rows12_2026-08-24` | **284** | exact match |
| `s2be1` | 308 | 152 | `harness_logs/s2b_e1_2026-08-24` | **152** | exact match |
| `s2b37` | 228 | 112 | `harness_logs/s2b_rows37_2026-08-24` | **606** | copy is a superset (a+b passes) |
| `s2b37smoke` | 248 | 89 | — | — | smoke pass, no consumer, re-runnable |
| `s2bcmp` | 74 | 54 | — | — | ad-hoc comparison scratch |
| `s2barena` | 26 | 9 | — | — | probe scratch |
| `s2bsmoke` | 26 | 11 | — | — | smoke scratch |
| `s2creg2` | 22 | 8 | — | — | register probe scratch |

Regeneration: `bash scripts/run_s2b_rows12.sh` · `run_s2b_rows37.sh` · `run_s2b_e1.sh`.

### 1c. Whirlwind + misc probe scratch

| path | MB | PNG | why safe |
|---|---|---|---|
| `wwdet1` | 29 | 10 | 10-frame determinism probe; `run_wwcr_stage.sh` marks-mode reproduces it in seconds |
| `wwdet2` | 29 | 10 | same |
| `wwtest` | 29 | 10 | same |
| `s2adbg` | 9 | 175 | debug scratch |
| `s2a` | 10 | 156 | superseded S2A scratch; sealed evidence at `harness_logs/s2a_*` |
| `s2btest` | 12 | 9 | probe scratch |
| `s2smoke` | 15 | 12 | smoke scratch |
| `s2csmoke` | 4 | 69 | smoke scratch |
| `s2brc` | 5 | 100 | receipts probe scratch |
| `vfx_register` | 6 | 72 | register probe scratch |

**`wwcr` (28 MB) is NOT in this round** — it is the live W2 stage userdir and this wave writes to it.

### 1d. Round-1 total

**~3,472 MB (3.4 GB) across 21 directories.** Every entry non-banked, writable, and named with a
regeneration route.

---

## 2. DEFECT-EVIDENCE PRESERVATION (protocol step b)

**No frame in the Round-1 set is cited by any finding.** Checked: the defect-evidence frames the S2C
findings rest on are the `s2c38*` / `s2c12*` corpora — **which this round preserves entirely** (§ 0). The
S2B evidence of record is the `harness_logs/s2b_*` copies, which this round does not touch. The three
review ladders produce MP4s, and the MP4s are staying.

---

## 3. WHAT ROUND-1 DOES NOT REACH — named, with cost, for a later round

Honest arithmetic: free space was **~46.9 GB** before this round. **3.4 GB does not clear the 60 GB
tripwire, and I am not going to imply that it does.** The remaining large consumers, none of which I am
deleting unilaterally:

| candidate | size | why not this round |
|---|---|---|
| `reincarnated-godot/.godot/` | **17 GB** | Godot's import cache — regeneratable *by definition*, and the single biggest legitimate Class B target on the host. **But reimporting ~10 GB of Synty assets stalls the render lane for a long unbounded window, and this is a BUILD wave holding the serial godot lane.** Deleting an import cache in the middle of a capture wave is exactly the wrong hour. **Round-2 candidate at lap close, when the lane is free.** |
| `reincarnated-godot/tmp/` non-`br2watch` | ~3.7 GB | `vfxbakeoff` 328M · `wr3acc` 442M · `restage` 512M · `arcclear` 601M · `lap1watch` 189M and others. Older workstreams' scratch. **I do not own their provenance well enough to certify "why-safe" in this round**, and R-16 requires a why-safe per path, not a size per path. Route to their owners. |
| `reincarnated-godot/tmp/br2watch` | 1.0 GB | **Class A — DO NOT DELETE.** Holds `m6/pl_audit.json`, the file my ratified camera pin is verified against (W1 § 1), and `measure/census.json`, under QA review at `qa/pending/2026-08-25-a-23-day-old-uncommitted-ocr-regression-nobody-owns.md`. |
| `harness_logs/s2c_rows12_2026-08-25` | 1.7 GB | **Class A.** Per `run_s2c_rows38.sh`'s own header comment, S2C rows 1–2 **pass 1 exists ONLY here** — the userdata copy is pass 2. Deleting it makes the determinism receipt uncomputable. |

---

## 4. THE DELETION COMMAND, AS IT WILL BE RUN

Scoped to an explicit list. No glob that could widen, and in particular **no `s2c38*` / `s2c12*` glob** —
the glob that R-16's candidate wording invites is precisely the one that would take the banked corpora.

```
cd "/Users/admin/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike"
rm -rf s2rev s2revA s2revB2 s2b12 s2be1 s2b37 s2b37smoke s2bcmp s2barena s2bsmoke \
       s2creg2 wwdet1 wwdet2 wwtest s2adbg s2a s2btest s2smoke s2csmoke s2brc vfx_register
```

**Pre-deletion `df -k /Users/admin` receipt:**

```
/dev/disk3s5   482797652 409578200  49157600    90% 2774579 491576000    1%   /System/Volumes/Data
                                    ^^^^^^^^ 49,157,600 KiB avail = 46.9 GiB
```

Freed-space receipt is appended to this file after the deletion fires.

---

## 5. FREED-SPACE RECEIPT (appended post-deletion)

*(pending — appended below after `rm` returns)*
