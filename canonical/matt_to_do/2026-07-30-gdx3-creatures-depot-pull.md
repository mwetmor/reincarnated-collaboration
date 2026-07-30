# T-row candidate — GDX3 `Creatures.arc` depot pull (Steam-authenticated)

**Parked:** 2026-07-30 · **By:** gandalf (RUN-CONDUCTOR, WR3), from legolas escalation
(`agentic_orchestration/legolas/research/2026-07-30-wr3-stage2-referent-extraction.md` §5 U-1)

## The action (Matt's hands — Steam credentials)

Pull the **GDX3 asset depot's `Creatures.arc`** (~0.5 GB) into the local Grim Dawn asset pin.
`DepotDownloader` is already resident at `~/Games/reincarnated-engine/vendor/depotdownloader/`;
the Edition-II pull (T-row 2026-07-24, DONE) is the working precedent — same tool, same flow,
different depot. Target: `vendor/grim-dawn/` beside the existing base+GDX1+GDX2 pin.

## Why only Matt

Steam-authenticated download — credentials are a Matt-only context (same constraint the
Edition-II fetch row carried).

## What it unblocks

**The werewolf-form player timings** — the ONLY blocking UNKNOWN in the WR3 stage-2 referent
extraction. Matt fought the referent session in werewolf form; `anm_werewolf.dbr` (GDX3-only)
routes every form-specific clip: Evade dodge animation (`hero_werewolf_dodge_a01.anm`), run-anim
base, and **attack cadence** — which also closes the reference envelope's grade-E attack-cadence
row and firms the 310–620 HP/s player-DPS band that stage-2 calibration targets.

Boss timings and speed ratios are NOT blocked (base-game assets, fully measured). The `.anm`
parser is already written; once the file is on disk, every figure re-derives in minutes
(legolas re-fires on notification).

**Blocks:** WR3 stage-2 player-side referent numbers (Evade lock duration in-form, player swing
cadence). **Does not block:** the stage-2 grill itself — boss-side and speed rows are complete.
