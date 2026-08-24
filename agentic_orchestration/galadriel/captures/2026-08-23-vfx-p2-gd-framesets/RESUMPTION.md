# GD-kit frameset extraction — RESUMED AND DISCHARGED

> **STATUS 2026-08-23: DISCHARGED. Do not re-fire from this file.**
> The resumption happened and completed. Deliverables landed at commit `a35e92cf`:
> `eye_of_reckoning/` (12 framesets, the `whirlwind` semantics-ground-truth set) and
> `judgment/README-EMPTY.md` (the `circle` archetype — honorable pause held; the identity was
> never confirmed and no frames were placed under that name). Full account in
> `galadriel/notes/2026-08-23-vfx-p2-gd-framesets.md`; conductor report at
> `gandalf/requests/2026-08-23-knight-rider-galadriel-p2-landing.md`.
>
> **One thing below is still live:** the `~/gd-scratch/` inventory. Those local video copies are
> what make `_workbench/` and `eor-test-2/` cheap to regenerate, which is the basis of the ~0.9 G
> PL-5 reclaim offered to the conductor. Do not delete `~/gd-scratch/` without reading that.
>
> Everything else below is the historical record of the interrupted first flight.

---

## Historical record — flight ended mid-run, awaiting resumption orders

**Stopped by:** knight-rider, 2026-08-23, on Matt's order (5-hour window token budget).
**Not a failure, not a HALT, not an honorable pause.** Clean stop at a natural boundary.
**Charter position:** VFX archetype-binding run, §4 P2 GD-kit supplement (ledger L-14b, L-16, L-17).

## Where she stopped

Last reported state, verbatim: *"40 candidates. Before mass extraction I need to verify at native
rate what these events actually are. Extracting one and inspecting closely."*

So: **candidate detection DONE (40 events), per-event verification NOT started, mass extraction NOT
started.** No frameset artifacts were finalized. Nothing is half-written into a deliverable path —
`eye_of_reckoning/` and `judgment/` are empty; `eor-test-2/{circle,whirlwind}/` exist.

## What is already on disk — DO NOT REDO THIS (it is the expensive part)

Local scratch, `~/gd-scratch/` (SMB share reads already paid for):

| artifact | size | what |
|---|---|---|
| `eor-test-1/eor-warlord-2026-08-04 21-09-31.mp4` | 2,246,945,680 B | full local copy of referent 1 |
| `eor-test-2/…mp4` | (copied) | full local copy of referent 2 |
| `eor1-gray-4fps.raw` | 323,773,200 B | decimated 4fps grayscale scan substrate, referent 1 |
| `eor2-gray-4fps.raw` | 134,006,400 B | decimated 4fps grayscale scan substrate, referent 2 |
| `eor1_{cm,d,gm}.npy`, `eor2_{cm,cmax,d,gm}.npy` | small | derived detection series |

Workbench (`_workbench/`, 796 M total in this dir): `hb*` hotbar series, `ev1.npy`, probe stills.

**Copy-to-local held up fine** — the mount never dropped during the flight.

## Partial artifacts that MUST be regenerated, not trusted

`_workbench/q1/` (184 files) and `_workbench/q2/` (86 files) were being written by an ffmpeg that
**survived the agent kill as an orphan and was terminated separately**. `q2` is therefore
**truncated mid-write**. Both were sourced from `/Volumes/...` rather than the local copies. On
resume: delete both and regenerate from `~/gd-scratch/` local copies.

The commands in flight were:
`ffmpeg -ss 826 -i <referent1> -t 46 -vf fps=4,scale=1280:720 q1/f-%04d.png`
`ffmpeg -ss 713 -i <referent2> -t 34 -vf fps=4,scale=1280:720 q2/f-%04d.png`

## THE BRIEFING CORRECTION SHE NEVER RECEIVED — read before resuming

She was briefed BEFORE ledger rows **L-18** and **L-19** existed, and is operating on a stale
understanding of what the whirlwind frames are FOR.

- **She believes:** both sets enrich P3 as first-party ground-truth style candidates.
- **Actually (L-18, Matt's live word):** Matt **rejected the GD EoR whirlwind skill art** — *"a
  generic magical aura that happens to be spinning along with the character."* The Eye of
  Reckoning frameset is **RECLASSIFIED for `whirlwind`**: **excluded from the P3 style-candidate
  pool** (pre-lost at the owner instrument), retained as (i) **semantics ground truth** —
  channel cadence / radius / movement, the §3.4 "same move" layer — and (ii) a **negative style
  anchor** for the P3 judge.
- **`Judgment` → `circle` is UNAFFECTED** — full candidate status.
- **L-19:** the validated `whirlwind` incumbent is a D4 Whirlwind-Barbarian clip,
  `https://www.youtube.com/watch?v=KaMPoPywM40`, with two Matt-named confounds: added
  cyclones/tornadoes are NOT base-skill VFX (S14 Dust-Devil build modification), and cosmetic
  wings occlude readability.
- **P3 scoring lens (Matt verbatim criterion, L-19):** **action-caused vs action-decorating** —
  does the VFX read as physically caused by the move (weapon speed, impact against flesh/bone/
  armor), or as decoration attached to it?

**Consequence for the work itself: none — extraction is unchanged, frames are frames.** The
consequence is for **labeling**. The EoR/whirlwind output must not be indexed as a style candidate.
Label it semantics-ground-truth + negative-anchor, or it enters P3 in the wrong role.

## Run context at time of stop

- **Non-blocking.** The Codex dossier lane covers all 26 archetypes independently.
- **Fold-in point: any time before P4 close.** If it misses, T-A carries a provenance note and the
  supplement rolls to Step 2 (L-16 ruling).
- **P0-b (drax Metal probe) is CLOSED** — ledger L-20, tag `drax/v-godot-vfx-metal-probe-1`.

## Resumption shape

Re-fire the named `galadriel` sub-agent pointed at this file. Brief must carry: the L-16 referent
ruling (eor-test-1/-2 only; play-test-v1 excluded by ruling), the L-18/L-19 reclassification above,
and the local-scratch inventory so she resumes at per-event verification rather than re-copying
2.25 GB. The honorable-pause rule still stands.

*Filed by knight-rider, 2026-08-23.*
