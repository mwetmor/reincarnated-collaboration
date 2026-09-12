TOOLING BURST T0-b — gate library port (SPEC § 3) + lane amendments (charter v1.1). task_id "T0-b".

Read ONLY, in this order:
1. /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/SPEC.md  (§ 0 constraints, § 1 result schema, § 3 — the contract for this burst, § 5)
2. /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/BURST_RULES.md  (the v1.1 caps + the TRANSCRIBE/LABEL rows)
3. the run_02 / run_03 source files named in SPEC § 3 (astra_test_01/run_02/{guides.py,pipeline.py,registration_preflight.py}; astra_test_01/run_03/{turnaround.py,check.py,check_vfx.py,animation.py,package.py,preview_template.html}); astra_test_01/design/experiments/E01/projection-candidates.json; astra_test_01/run_03/evidence/current_checks.json (regression lock); astra_test_01/run_03/character/frames/** (PNG fixtures, read-only)
4. the existing astra_test_01/burst/lane/*.py and tests/ (to amend, not rewrite)
Do not read AGENTS.md, CLAUDE.md, role files, the charter, or anything else. No web. No agents. No image generation. No pip install. Available: stdlib, Pillow, numpy, scipy, scikit-learn. cv2/skimage/torch are ABSENT — do not import them.

BUILD: everything in SPEC § 3 — gates/{common.py, matte.py, register.py, g1_height.py, g2_pivot.py (root anchor AND planted-sole trajectory, two quantities), g3_light.py, g5_drift.py, g6_seam.py (literal G6 AND G6b median, both reported), g9_alpha.py, drift48.py, silhouette64.py, pack.py, run_gates.py}, review/build_review.py, with tests/test_gates_*.py using known-bad fixtures (run_02's seven cases + shifted-mask, repeated-lead, swollen-bag synthetic cases) and a REGRESSION-LOCK test that re-gates astra_test_01/run_03/character/frames and compares to run_03/evidence/current_checks.json to 1e-3 (record any diff in your receipt concerns; do not "fix" the port to hide a diff — report it).
Projection C: read E01/projection-candidates.json; if C is numerically defined, expose it as the guides.py constant set; if not, keep run_02's constants as default and say so in concerns.

AMEND (charter v1.1 caps; keep every existing test green and add tests for each change): lane/run_burst.py validate_task and lane/audit.py — TOOLING bursts: minutes_cap ≤ 40, tool_call_cap ≤ 60; all other types ≤ 15 / ≤ 20. Image calls: GENERATE ≤ 12, LABEL ≤ 2, every other type 0 (audit must treat LABEL like GENERATE for the image-call rule).

WRITE ONLY under /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/ (via --add-dir) and your cwd. Temporary files ONLY under astra_test_01/burst/tests/tmp/ (create it; clean it) — never the system temp dir.

RETURN: a receipt matching the output schema; task_id "T0-b"; every created/modified file with sha256 in "files"; DELIVERED or DELIVERED_WITH_CONCERNS with each concern named precisely; never PASS/FAIL in the receipt.
