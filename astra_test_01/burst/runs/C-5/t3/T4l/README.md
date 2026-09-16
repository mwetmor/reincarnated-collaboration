T4l — outside-in implementation with unresolved acceptance requirements

V2 now erodes the whole-body distance field from tips toward the core. Dissolve stays zero during expansion/erosion, then removes white, orange, and finally dark/red together at release. Tongue stretch is seeded 2.0–2.5 along and 0.85 across; root drift remains unchanged. The opt-in screen_px kit field bypasses character art_scale for cast/travel/impact layers, including piece roots, duplicates, flash, halo and floor radius; the G1 socket position is unchanged. Legacy shader exports strip the optional outside-in branch and all 488 authored exports for six kits plus v1 match pre-change hashes.

CPU extent at effect age 15 is 1.91318× hold extent; at expansion end it is 1.93248×. Expansion/erosion minimum component fraction is 0.95137. Residue initially retains 8403/41951 = 20.0305% of maximum HOLD-frame body coverage (not the larger temporal maximum during expansion). Its centroid stays within 0.06518× peak extent throughout erosion and residue.

The prescribed final band removals do not satisfy the compactness/hold requirements on these masks. White removal leaves 5425 pixels (12.9318%); orange removal leaves 1650 (3.9332%) with largest component 67.2121%. Only 23 of the 36 residue frames remain within 15–25% coverage. A diagnostic sweep over every 8-bit radial cutoff in the allowed initial coverage interval gives at most 80.8738% final-ember connectivity. The candidate threshold was not changed. The conductor must resolve this conflict; do not treat this implementation as accepted.

The new headless import and actual uniform trace exit 0 with no script/parse errors. Caller scale 0.608 yields Art scale 1 and floor scale (7.5,4.5), corresponding to authored radius 120. Godot emitted sandbox user-data/editor-setting permission errors and a certificate error; these are recorded, not hidden. No rendered bake was produced; rendered acceptance is UNEVALUABLE.

51 relevant unittests ran: 45 without failure, six failures, no test errors. Two failures expose the current candidate's connectivity and literal residue-duration shortfalls. Four retained failures assert superseded lap-2 behavior. Existing tests are byte-preserved prefixes; only appended tests were added. The replay-importing test was omitted because export/replay.py is excluded from this task. A repository-wide suite was not run.

Procedure deviation: the first SPEC excerpt included unrequested sections 2–6 and other section-7 rows. Full invariant compliance is not claimed.

Evidence archive: extract evidence.tar.gz into this directory to restore project/, before-source snapshots, legacy_before/, legacy_after/, raw logs, diffs and drivers. From burst root, with PYTHONPATH=.:tests and PYTHONDONTWRITEBYTECODE=1, run python3 -B runs/C-5/t3/T4l/check.py, then headless.py, then run_checks.py. The two extra residue tests are available as test_effect_kit.BurnBackResidueHoldTests via unittest. CPU diagnostic is test_effect_kit.burn_back_cpu(project_path). All test temporary files must remain redirected to this directory as in run_checks.py.

The appended CPU and clock tests can also read project evidence directly from evidence.tar.gz; extraction is only needed to rebuild or rerun Godot.
