TOOLING BURST T0-a — Astra burst lane, Run C-1 (bootstrap; hand-invoked by the conductor)

You are building software to a spec. Read ONLY these files, in this order:
1. /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/SPEC.md  (the build contract — § 0, § 1, § 2, § 5 apply to you)
2. /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md  (§ 2 register card, § 4 burst rules, § 6 rubric — extract these three VERBATIM into REGISTER_CARD.md, BURST_RULES.md, JUDGE_RUBRIC.md under astra_test_01/burst/)
Do not read AGENTS.md, CLAUDE.md, role files, or anything else in the repository. Do not use web tools. Do not spawn agents. Do not generate images. Do not pip install anything.

BUILD (SPEC § 2, all of it): lane/render_brief.py, lane/run_burst.py, lane/audit.py, lane/ledger.py, lane/schema_check.py, receipt.schema.json, tests/test_lane.py (+ synthetic event fixtures under tests/fixtures/). Python 3 stdlib only for this burst. Run the tests; they must pass; include their output in your receipt concerns if anything is skipped.
Also create runs/C-1/ledger.json with the empty structure from SPEC § 2 (images_cap 250).

WRITE ONLY under /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/ (writable via --add-dir) and your own cwd. Nothing else.

RETURN: a receipt matching the output schema. task_id "T0-a". List every file you created with its sha256 in "files". status DELIVERED or DELIVERED_WITH_CONCERNS (name each concern precisely: what you could not verify, what you assumed). Never use the words PASS or FAIL in the receipt.
