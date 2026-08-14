# NOTE-90 instrument — verification by replay against firing #2's kept lists

**Cell:** SB-1 CLK-2, firing #3, item A. **Date:** 2026-08-14. **Author:** drax.
**Tool:** `agentic_orchestration/drax/tools/kc2_preroll_depth.py`
**Harness:** `reincarnated-godot/scripts/run_kc2_cpb_clip.sh` (FG-10 block)

The instrument was not accepted because it ran. It was accepted because it reproduced
numbers that were on record before it existed — the § state census of the firing-#2 landing
note, derived there by paste-arithmetic.

## The two required reproductions

| replay | lists | expected (firing #2 § state census) | **measured by the tool** |
|---|---|---|---|
| full-span family | salvage p1/p2/p3 + firing2 c1-cold/c2-warm/c3-warm (6 × 380 lines) | deepest **line 21** of 60 | **line 21**, margin 39, 17 preroll lines ever differ |
| short-1570 family | short p1–p4 (4 × 105 lines) | deepest **line 23** of 60 | **line 23**, margin 37, 19 preroll lines ever differ |

Both replays also report **measured span IDENTICAL** — the 11-pass green, restated by a
second implementation. First divergence is index0 **4** (= line 5) on both families, which is
the firing-#2 finding that "lines 1–4 agree on every pass; the variance opens at line 5",
now produced mechanically instead of by eye.

## Controls — because a probe that cannot tell two verdicts apart is not a probe (NOTE-72)

| control | question it answers | result |
|---|---|---|
| A — salvage p2 vs firing2 c1-cold, a pair KNOWN byte-identical | can the tool report **zero**? | **NONE, margin 60 of 60** |
| B — one list, no pairs | does "nothing was compared" print the same line as "compared and agreed"? | **defect found and fixed** — see below |
| C — the killed 99-frame p4 folded into the full family | does a truncated list corrupt the maximum? | **line 21, unchanged** |

⚑ **Control B found a defect in the instrument, before the instrument shipped.** With a
single list there are no pairs, yet the tool printed *"NONE — all 60 preroll frames identical
across 1 passes"* — the same sentence it prints when it genuinely compared and found
agreement. Two different verdicts wearing one line (NOTE-82). The tool now carries a
`measurable` field and prints **"NOT MEASURABLE — 1 pass, no pairs to compare. This is not a
green reading."**

## Harness plumbing smoke (isolated temp tree, throwaway)

Three code paths were executed before the matrix was allowed to consume them:

1. **green** — 2 passes of a 3-frame leg, split mode (`FG10_MODE=pass` ×2 then `verdict`):
   1 state, exit **0**. The standing diagnostic printed on a **green** leg: *line 17 of 60,
   13 preroll lines differ* — which is the whole point of NOTE-90.
2. **red** — the same leg with a **synthetic** divergence injected into the throwaway
   post-prune list (a plumbing test, not a determinism finding): 2 states, exit **12**,
   keep-frames fired (3 named indices × 2 states), geography written.
3. **all** — the unsplit path (`FG10_MODE=all PROBE_ONLY=1`), exit **0**, evidence dir and
   gate log written. No committed code path in this amendment is unexercised.

⚑ **The red smoke produced a real reading anyway.** The two kept frames at raw index 16 are
genuinely different frames — the preroll transient, caught in the act at HEAD:

```
n_differing_pixels 1,700,949   pct_of_frame 82.028791   bbox 1920x1080
max_abs_delta 171   mean_abs_delta 2.3237   pm1_share 47.849 %
region grid flat (6.32 - 6.66 %)
```

That is **NOTE-87's fingerprint to three significant figures**, reproduced in a fourth firing
at a fourth commit by an instrument written after the note. One mechanism, still.

## Files

- `depth-REPLAY-full1570-family.json` — the line-21 replay, with the full per-pair table
- `depth-REPLAY-short1570-family.json` — the line-23 replay
- `depth-CONTROL-known-identical.json` — the zero reading
