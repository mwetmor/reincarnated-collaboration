# Carved Ravine — Revision 3 — Matt Gate Package

**Status:** BUILT + VERIFIED BY EYE — the R2 composition regression is RESOLVED; the R2-B brightness you liked is byte-identical-preserved. My §1/§4 read: **PASS-with-minor-residuals.** Awaiting the Matt Gate. Push HELD.
**Author:** gandalf (design steward), 2026-06-21.
**Build:** `reincarnated-godot 881cf57` (R3 — camera-dominant composition fix), held. Parent R2 = `7cad6fd`. galadriel CV still NOT RUN (dark-first rubric stale vs the bright register; advisory pending re-baseline).
**Parents:** `2026-06-21-ravine-carved-r2-matt-gate-package.md` (the mixed read this resolves); `2026-06-21-ravine-carve-and-sculpt-spec.md` (build contract).

---

## 1. What changed since R2

Your R2 verdict: "yes it is not great. I do like the brightness now though." → keep R2-B brightness, fix the composition. The fix was **camera-dominant** (gandalf design call): anchor the follow-cam + in-scene stations to the proven `03_pool2` framing — lower + closer, looking across-and-down INTO the gorge, so the play surface fills the frame and the rim forest sits as a top-of-frame backdrop band. The recognition: the gorge geometry already delivers the "enchanted forest above" feel for free when you stand inside it; the R2-D pull-back was over-reaching for it and created the green-carpet foreground.

drax R3 (`881cf57`):
- **Camera:** follow-cam pull-back undone (`CAM_BACK 6.5→4.8`, `CAM_UP 7.0→5.8`, `CAM_LOOK_DOWN 2.4→1.0` — look into the gorge, not up at the rim carpet); stations `00`/`01`/reveal/downgorge dropped below the rim; `03_pool2` money shot unchanged.
- **Lighting:** UNTOUCHED — falsifier verified byte-identical to R2 (`git diff 7cad6fd HEAD` over `_build_environment` = empty).
- **Floor break-up (light):** ~167 clustered solid grass/moss/pebble/small-mushroom clumps with dark gaps so bare floor reads as forest texture; sparse on combat islands (AoE clarity), dense at edges + pinches; solid geometry, no cards.
- **Red/magenta artifact:** root-caused (backdrop asset sampling a red atlas region) + taken out of frame by the down-into-gorge reorientation; confirmed clear.

## 2. My §1/§4 verdict (verified the previously-fouled frames)

| Frame | R2 read | R3 read (by eye) |
|---|---|---|
| `01_pool1` (static station) | ~70% green carpet, fight in a small aperture | **FIXED** — goblin ring fills lower frame, gorge + water mid, rim forest backdrop band |
| `walk_beat_00440` (pool1 follow-cam) | green humps dominate, gorge small/distant | **FIXED** — hero + full goblin ring fill frame, clean ARPG approach shot, rim as backdrop |
| `walk_beat_01520` (exit) | red/magenta artifact + flat green | **FIXED** — magenta GONE, hero framed in the exit pinch |
| `00_committed` (entry) | bland flat-green floor | **IMPROVED** — gorge mouth + goblins are the subject; minor green rim band remains |
| `03_pool2` (climax) | the working money shot | **PRESERVED** — unchanged, still strong |

The dominant green-carpet foreground regression is gone; combat reads; the rim forest now does its job as the enchanted backdrop band (the prediction held). Brightness unchanged.

## 3. Residuals (minor / geometric — honest, not regressions)

- `00_committed` + `01_pool1` static stations still show a green rim band on the **wide-shallow** pool1 (floor −5.0, hw 9.5) — geometrically unavoidable for a static oblique short of near-top-down; the fight now dominates, so it reads as backdrop, not foreground.
- Exit-pinch beat (`01520`) has a flat green rim-plateau band across the top ~30% — transient, the hero is cleanly framed.
- Connector pinch (~2 s transient) reads as an enclosed dark gorge pinch — the best the narrow snake-pinch geometry affords (acknowledged hard since the R1 gate).

None block the read. All are camera-angle/geometry tradeoffs of the wide-shallow-pool + sunken-gorge combination, not build defects.

## 4. The gate decision in front of you

- **PASS** → the carve is done through the composition fix; I can re-run galadriel once the bright-register rubric is re-baselined (the proper CV leg), or you accept it on eye. State which.
- **POLISH** → name any residual in §3 (or anything the MP4 shows) you want chased; targeted round.
- The MP4 is the best full read: `/Users/admin/Games/reincarnated-godot/harness_logs/ravine_walkthrough_carved_R3_2026-06-21/ravine_walkthrough_carved_R3.mp4`.

Nothing pushed — R3 held at `881cf57`, awaiting your gate.

## Sign-off
gandalf, 2026-06-21. The composition fix you called for landed: camera anchored to the proven `03` framing, the green-carpet foreground gone, the rim forest now the enchanted backdrop, brightness byte-identical-preserved, magenta cleared. PASS-with-minor-residuals on my eye. The human gate is yours.
