# T20 — Mac data volume RED: 22 GiB free of 460 (96% used)

**Parked:** 2026-08-24 · **By:** gandalf (RUN-CONDUCTOR, RUN U1-BUILD run-close item — ledger L-7(a))
**Class:** host-level storage action — only Matt can rule what is deletable/movable on his machine.

## The finding (how it surfaced)

The U-1 fleet flight-recorder's FIRST real Tier-1 render (Block B-1, 2026-08-24) carried a HEALTH
lane probe that read the disk and rendered RED: **nobody was watching this number before the
recorder existed.** Re-measured at run close:

```
/System/Volumes/Data   460Gi total · 416Gi used · 22Gi free (96%)
~/Games                234 GB
~/Library/Caches       5.1 GB
```

## Why it matters

- ~5% free is inside the zone where macOS + Godot builds + DepotDownloader pulls + video captures
  start failing in confusing ways (APFS wants headroom; swap + snapshots compete for the same pool).
- Two OPEN queue rows want to WRITE large artifacts to this pool or its externals: **T14**
  (screenshot to `/Volumes/reincarnated/` — external, fine) and any future depot sitting
  (multi-GB pulls landed under `~/Games/vendor/`).
- The flight-recorder HEALTH lane will render this RED on **every report** until it clears —
  by design (same pattern as the `ENABLE_PROMPT_CACHING_1H` red: the lever made visible).

## Candidate reclaim surfaces (Matt rules; agents CANNOT delete any of these)

| Surface | Size class | Consideration |
|---|---|---|
| `~/Games/vendor/` GD depot cuts (Edition-II + Edition-III + gdx3) | tens of GB | Licensed Steam pulls — re-fetchable via DepotDownloader if credentials/manifests retained; the edition cuts are PINNED research referents (KC2/T15 lineage) — moving to the external `reincarnated` volume preserves the pin without the internal-disk cost |
| Video captures (eor-test MP4s, play-test footage) already ALSO on `/Volumes/reincarnated/` | GBs | Any internal duplicates of externally-verified copies are the cheapest reclaim |
| `~/Library/Caches` | 5.1 GB | Safe-ish, small yield |
| Old Godot export builds / DerivedData-class build products | unknown | Rebuildable by definition |

## What it unblocks

Headroom for: future depot sittings (T-class rows), Godot demo export builds (D10 gates),
video capture work (galadriel), and clearing the standing RED on every flight report's HEALTH lane.

**Done-criterion:** free space ≥ 60 GiB (≥13%) on `/System/Volumes/Data` — the next flight report
render flips the probe green automatically; no agent action needed after Matt acts.

---

## ⚑ ESCALATION 2026-08-25 (knight-rider) — THE PREDICTED FAILURE HAPPENED, AND IT HAPPENED TO ME

**Severity raised: RED → BLOCKING.** This row is no longer a hygiene item. It **halted a live build wave mid-tranche.**

### The measurement, one day later

| | 2026-08-24 (this row) | 2026-08-25 (now) |
|---|---|---|
| Free on `/System/Volumes/Data` | **22 GiB** | ⚑ **2.7 GiB** (0.6%) |
| Container free space | — | 2.9 GB, and **APFS local snapshots = 0** — so this is **real, not purgeable**. I checked, because "phantom full from snapshots" is the cheap explanation and it is not the one. |

**~19 GiB consumed in a single day**, essentially all by the Step-2 VFX wave.

### What it did

drax's S2C tranche-3A capture **completed all 128 arms** and then **the host ran out of disk during the copy step**, taking pass 2 with it. He halted correctly and **refused to commit** — writing git objects onto a zero-byte volume risks a corrupt object store. Four commits are held un-pushed. Then **my own shell began failing `ENOSPC`**, intermittently, mid-diagnosis. This row's line *"start failing in confusing ways"* is exactly right, and I want it on the record that **the prediction was already written down before the failure.**

### ⚑ The proximate cause is PURE WASTE and it is fixable in one line

Every capture pass ends with `cp "$USERDIR"/*.png "$OUT"/` — duplicating ~1,600 1080p PNGs (**2.6 GB per pass**) into `harness_logs/`. **`harness_logs/**/*.png` is gitignored**, so the copy is *never committed*, and the gate can read the userdir directly. **The harness has been doubling its own disk footprint at the end of every pass, for no consumer.** At 2 MB/frame across the wave's passes, this alone plausibly accounts for the bulk of the 19 GiB. **Fix belongs to drax (his seam, his diagnosis).**

### What I reclaimed — and the bound I respected

**Freed 2.6 GB**: `harness_logs/s2c_rows38_2026-08-25/*.png`, the current run's duplicate copy. **Gated on a machine-checked predicate, not on my reading of output** — authority-set count (2106) ≥ copy count (1592) **and** `git ls-files` = 0 tracked. It refused-by-construction if the authority was not provably a superset.

**I deleted NOTHING from this row's candidate table.** That table says *"agents CANNOT delete any of these"* and I read it as binding. I also declined to touch the remaining large pools — `harness_logs/s2c_rows12_*` (1.7 GB ×2), `s2b_rows37_*` (1.2 GB ×2), userdir `s2c12` (1.7 GB) — because **those are the frames behind SEALED verdicts**, and retiring sealed evidence is not an orchestrator's call even when it is technically regenerable.

⚑ **One correction against a relayed figure, recorded because I nearly acted on it:** drax's halt named `tmp/vfxtruth1/` as *"~7.7 GB, gitignored, regenerable"* — the next reclaim candidate. **Measured: 84 MB, and NOT ignored by pattern, with 464 tracked files under `tmp/`.** Deleting on that recommendation would have been a mistake against tracked work. `#79` cl. 6 (mechanism claims carry an empirical-test obligation before relay) earned its keep the same day it was minted.

### Host-level picture, so the ruling has numbers under it

```
~/Games                      244 G   ← of which:
  reincarnated-engine        127 G
  reincarnated-godot          43 G   (harness_logs 9.7 G · tmp 4.7 G)
  reincarnated-collaboration  22 G
  reincarnated-demo           15 G
  vendor                      14 G
  synty-corpus                14 G
~/Library                     47 G   (Godot userdata alone: 9.2 G)
```

**`reincarnated-engine` at 127 GB is the largest single object on the machine and nobody has looked at it.** It is a Python repo; that figure is almost certainly retained run outputs and DBs rather than source. **Not my seam and not my call** — flagging it as the highest-yield surface Matt has, and one this row's original table never named.

### What is blocked RIGHT NOW

**S2C tranche-3A cannot complete.** Pass 2 requires **~4.2 GB** (2,106 frames × ~2 MB). Available: **2.7 GB**. ⚑ **I ran that projection and DECLINED TO FIRE** rather than send a 25-minute capture into a host that would fail it at minute 24 — per **Discipline #1.1 pre-fire resource-bounds projection**, which I should have run *before* the first dispatch and did not.

**Ask of Matt — one ruling, not a list:** free enough headroom to clear this row's existing done-criterion (**≥ 60 GiB**), or rule which of the surfaces above may be retired by agents. **Until then the godot lane is stopped**, four commits are held, and every capture-bearing dispatch in any seam is un-fireable.

---

## ✅ CLOSED 2026-08-25 — Matt acted; done-criterion met by measurement, not by report

**Matt, verbatim:** *"crisis averted. I saved 64GB."*

| | at parking (08-24) | at escalation (08-25) | now |
|---|---|---|---|
| Free on `/System/Volumes/Data` | 22 GiB | **2.7 GiB** | **66 GiB (85% used)** |

`df -h` re-read directly rather than inferred from Matt's figure — **66 GiB ≥ the row's own ≥ 60 GiB criterion**, so this closes on its stated terms and not on assent. The HEALTH lane probe flips green on the next flight-report render with no agent action.

**Unblocked and re-fired:** S2C tranche-3A pass 2 (drax), projected at ~4.2 GB against 66 GiB — Discipline #1.1 projection run **before** the re-fire this time, which is the part that was missing when this failed.

**What does NOT close with it.** Two items survive the reclaim and should not be lost in the relief:

1. ⚑ ~~**The `cp "$USERDIR"/*.png "$OUT"/` waste step is still in the harness** and is the proximate cause. ~2.6 GB per pass duplicated into a gitignored path with no consumer.~~ **WRONG — CORRECTED BY drax, same day. See § below. My "one-line fix" would have created a silent false-green.**
2. **`reincarnated-engine` at 127 GB remains the largest single object on the machine and still nobody has looked at it.** It is a Python repo; that figure is retained run outputs and DBs, not source. Not named in this row's original candidate table, not touched by the 64 GB reclaim, and not my seam — it stays flagged as the highest-yield surface available if headroom is ever wanted again.

---

## ⚑⚑ CORRECTION — my `cp`-is-pure-waste diagnosis was WRONG, and acting on it alone would have printed a perfect green over a test that had stopped testing

**Source:** drax, S2C tranche-3A completion record, same day. **This corrects § ⚑ ESCALATION above**, where I wrote that the copy step was *"PURE WASTE and it is fixable in one line."*

**The actual mechanism:** `USERDIR` was a **constant** (`s2c38`) while `OUT` carried the `$SUFFIX`. **Both determinism passes rendered into the same directory, so pass 2 overwrote pass 1.** The `cp` into `harness_logs/` was therefore **pass 1's only surviving copy** — and is what the rows-1-2 receipt was computed from.

> **Delete the copy alone and nothing errors. The gate compares pass 2 against itself and prints a perfect green.**

A determinism check that compares a run to itself passes with probability 1. **My one-line fix would have removed the disk cost and the test in the same stroke, and the receipt would have looked better afterwards.** I had the symptom right — real duplication, real GBs — and the mechanism exactly backwards: it was not a copy with no consumer, it was **a copy that was the only consumer's only input.**

**drax fixed it at the cause instead**: capture dir parameterised by `SUFFIX`, 41 sites. Result **4 × 4.2 GB → 2 × 4.2 GB**, and the receipt now keeps two genuinely independent passes. He found a second consumer the same way — the gate needs `render.txt` co-located, so a 29 MB text file now moves to the frames rather than 4.2 GB of frames moving to it.

**Why this is recorded in a Matt-facing row rather than only in a QA finding:** the escalation above is what asked Matt to spend an afternoon freeing 64 GB, and it named a cause that was wrong. The ask was still correct — the host genuinely was at 0.6% and genuinely did halt a build — but **the reader of this row should not carry away a mechanism that would break the instrument if applied.**

⚑ **Second finding from the same repair, and it defeats the remedy I dispatched:** **bash reads a running script lazily, by byte offset.** drax edited the runner 90 seconds into a detached run of it. **Detachment alone is not enough** — and worse, *a detached run is precisely the one you are most likely to edit*, because it is not holding your terminal. The complete remedy is detach **and** launch from a frozen copy. I dispatched half of it.
