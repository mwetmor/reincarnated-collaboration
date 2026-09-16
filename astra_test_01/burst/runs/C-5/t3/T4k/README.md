T4k — diagnostic return; production build incomplete

No production source or kit metadata was changed. The two named test files were extended only. Do not ship this as a fix for the conductor’s rendered clipping or dark ring.

The stipulated F-C5-6 cause does not exist in the inspected emitter: the expanded sprites sample original texture UVs, have no outer_distance clip, and have erode=0 and dissolve=0 at age 8. Even a hypothetical clamped distance of 1 cannot satisfy distance < erode for erode<1. The CPU 3x-stretch instrument retains at least 99.9163% of analytic alpha coverage, with zero original-UV boundary discards. Its intentionally world-canvas-clipped control retains only 58.3665% on the most affected piece. That control is an injected defect, not a claim about the existing shader.

At age 30 the actual Godot trace shows all 24 expanding paint/dark pairs and all 24 stationary paint/dark pairs sharing thresholds. PeakDark is hidden. Core erode is 17/27, tongue erode is 11/21, and expanding dissolve is 11/21; stationary erode is 0.04*11/21 and dissolve is 0.5*11/21. Both bands 0 and 1 remain below their shared removal threshold of 5/6. All-four-layer equality is false for every piece, and the instrument reports that separately; it is not weakened to pair equality.

The old exporter predicts 8368/41951 = 19.9471% of original source coverage. Supplied bake rows show residue 8211 px against temporal maximum 72040 px = 11.3978%, which is neither 20% nor the brief’s 12.7%. No threshold was tuned against an unstated denominator.

Actual headless import and trace both exit 0 without script/parse errors. Thirteen focused unittests complete without reds. All 488 exported files for the six legacy kits plus burst_v1 are byte-identical to the pre-T4k snapshot. Full-suite and rendered acceptance are not claimed. acceptance.json names the five standing oracle reds and environment reds from T4j with their provenance.

Evidence: evidence.tar.gz contains the emitted project, exact clock trace, logs, before-source snapshots, before/after legacy export trees, and proof/check drivers. Extract into this directory to reproduce. Commands from burst root after extraction: PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 -B runs/C-5/t3/T4k/run_checks.py; legacy_check.py builds into the archived legacy directories; proof.py accepts a fresh output-directory name and runs import/state tracing only. legacy_hashes.json remains unpacked because the new regression test consumes its pre-change table.

Procedure concern: the initial SPEC excerpt included sections 2–6 outside the requested sections. This deviation is reported; full invariant compliance is not claimed.
