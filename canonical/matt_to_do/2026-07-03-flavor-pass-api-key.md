# MATT TO-DO — export ANTHROPIC_API_KEY to run the W3 flavor pass (Beat B halted-loud at 0/35)

> **Parked:** 2026-07-03, by gandalf (invoking session for the star-lord F1+glyph+flavor dispatch).
> **Blocker class:** host/credential-level — only Matt can perform.

## What's parked

Beat B of `agentic_orchestration/dispatches/2026-07-03-star-lord-f1-glyph-flavor.md` — LLM flavor (`name` / `flavor_text` / `title_completion`) for the 35 shortlist finalists in `agentic_orchestration/w3-batch1-flavor-finalists-2026-07-03.md`. Completion: **0/35, $0 spent.**

Beat A (F1 envelope bridge + `identity_glyph` stamp) landed independently and stands — engine tag `star-lord/v-demo-run-f1-glyph-1`, all 5 round-trip smoke asserts PASS. The bundle is Beat-B-ready; no schema work remains, only the LLM fills.

## Why it halted

`ANTHROPIC_API_KEY` was removed from `.zshrc` 2026-06-12 (Max-subscription billing policy; sub-agent key-leakage guard). The engine's flavor path runs python3 subprocesses that need the key in the environment. Star-lord's test call confirmed the auth error and halted Beat B loud per dispatch instruction — correct behavior, not a defect.

## The action (Matt-only)

Export the key **transiently in your shell** (do NOT re-add to `.zshrc` — the removal policy stands) and fire the resume. Two equivalent paths:

1. Run the flavor script directly per star-lord's completion record appended to the dispatch file (collab commit `a23f881`), with `ANTHROPIC_API_KEY` exported in that shell; per-item resumable — a kill loses nothing completed.
2. Or launch `claude --agent star-lord` in a key-exported shell and point it at the dispatch's Beat-B resume point.

## What it unblocks

- The 35 flavored finalists → the **G7a roster-pick session** (final per-seat picks, 1 of 5 per seat)
- Criterion B (flavor leg) completion at shortlist scope — the other 665 kits stay None by ruling
