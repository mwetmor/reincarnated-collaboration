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
