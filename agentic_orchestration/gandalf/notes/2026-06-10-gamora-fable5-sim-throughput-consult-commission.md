# Gamora (Fable-5) — Battle-Sim Throughput Profiling + Runner-Architecture Consult

**STATUS:** COMMISSION — paste-ready opener for a fresh Fable-5 Gamora session (battle-sim 4K-kit throughput problem; the empirical criterion gating the battle-sim greenfield decision)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Why Fable-5:** single-agent design+profiling run at the higher tier; gradable output (NOT a handoff eval).

**Launch notes (do NOT paste into the Gamora session):**
- Gamora is **Mac-resident** (simulation seam, in `reincarnated-engine`). Launch Mac-side, not via PC/tmux:
  ```
  cd ~/Games/reincarnated-engine
  claude --agent gamora --model claude-opus-4-8
  ```
- The explicit `--model claude-opus-4-8` flag forces Fable-5 regardless of frontmatter pull state. (Avoid the `[1m]` suffix — glob-errors in some shells.)

---

## PASTE-READY OPENER (everything below the line)

---

You are gamora, the simulation-seam engineer (fight engine, balance loop, damage resolver, batch runner). Read your operating procedure skill (`reincarnated-gamora-operating-procedure`) and execute the session-start protocol per your OP. Then take on the commission below.

**Mission: profile the battle-sim's throughput at scale, then recommend a runner architecture that makes the balance loop iterable for ~400 balanced kits.**

### The problem (why this is existential)
The engine's content target has shifted from ~5–10 kits/season to **~400 balanced kits/season**, and landing those 400 likely requires exploring **~10× variants** along the way (element swaps across caster archetypes, range/movement across physical, T4 reversals/amplifications, racial-trait mix, experience mix) — call it **~4,000 kit-variants run through the simulator** to converge on the final 400. A back-of-envelope fear: if that takes **~3 real days of wall-clock**, the iteration loop is dead — nobody iterates on a system with a 3-day feedback latency. **Iteration speed is the project's metabolism; a 3-day balance loop ends the project.** Your job is to find out how real the 3-day figure is and what architecture kills it.

> The "3 days / ~65 sec per kit" figure is an **unverified back-of-envelope from the design chair, NOT a measurement.** Do not take it as fact — measure the actual current per-kit cost and project from real numbers.

### Required discipline (declare at the top of your deliverable)
1. **Empirical-evidence-first.** MEASURE, don't assert. Instrument the current sim/balance runner and report real numbers. A profile built from reading code without running it is insufficient — run it and time it.
2. **Preserve the resolver math (crown jewel).** The fight resolver + balance loop (recompose-first, ±25% variance, convergence-iteration learnings, the gauntlet, bounded-viability-validation) is the single most empirically validated asset in the engine. This consult is about the **runner/throughput layer, NOT the resolver math.** If you recommend porting the resolver to a faster substrate, it is a **same-math port validated against the current resolver as oracle** — never a math rewrite.
3. **Discipline #18 (math hotspot).** The throughput-vs-fidelity tradeoff (surrogate/quick-estimate methodology) is a math-hotspot decision. Treat the surrogate methodology with the rigor that demands.
4. **Surrogate-for-search / full-fidelity-for-commit guardrail (non-negotiable).** A cheap surrogate may prune the search space, but the **final 400 must pass the full-fidelity sim before they ship.** Never let the surrogate become source-of-truth — that ships a broken meta (the Diablo patch-day "this build does 1000× intended damage" failure). Bake this gate into any architecture you recommend.
5. **Recognition-validate-commit** — flag every scaffold/assumed value (Discipline #40); don't present a guess as a measured fact.

### Scope guard
**Throughput / runner architecture ONLY.** In scope: profiling the current sim, the parallelization story, surrogate-filtering, warm-start, and whether the resolver needs a fast-substrate port. OUT of scope: redesigning what "balanced" means, changing the balance *math*, the generation pipeline (rocket's seam), the spirit-guide gameplay, the meta-loop. Stay on "how do we run the existing balance math ~4,000 times fast enough to iterate."

### Required deliverable contents
1. **Empirical profile (the core deliverable)** — instrument and report ACTUAL numbers:
   - cost per fight; fights per gauntlet; convergence iterations per kit; current wall-clock per kit; projected wall-clock for ~4,000 kit-variants run **sequentially** on the current setup.
   - **Decompose where the time goes:** CPU in the resolver? LLM API calls? I/O / serialization? convergence-loop iteration count? Give the breakdown as percentages of total.
2. **LLM-in-loop audit (likely the dominant cost if present).** Is there ANY LLM call inside the balance hot loop? If so: where, how many per kit, what per-call latency. LLM latency × 4,000 × iterations is a prime 3-day-killer candidate — confirm or rule it out explicitly.
3. **Parallelizability confirmation.** Confirm the balance problem is **O(n) kit-vs-gauntlet (not O(n²) kit-vs-kit)** — the game is solo/PvE, so balance should be independent per kit. Confirm fight-run independence, estimate the parallel speedup ceiling, and name the overhead/coordination costs. (If you find an O(n²) matchup-matrix requirement anywhere in the seasonal balance path, flag it loudly — that changes the algorithm class.)
4. **Recommended runner architecture** — the scale-out design:
   - parallelism (local multiprocess → on-demand cloud cluster at sim time)
   - cheap-surrogate filter (the existing adaptive quick-estimate) to prune ~4,000 → candidate survivors, full-fidelity sim only on survivors — WITH the full-fidelity-gate-on-the-final-400 guardrail
   - warm-start from archetype baselines (the 40-general-kits × 10-variants structure means variants of one archetype are strong warm-start seeds for each other)
   - whether variation axes (element swap / T4 reversal / racial trait / experience mix) can be modeled as a balance **delta** rather than fresh convergence-from-cold
5. **Resolver-port assessment** — AFTER parallelism + de-LLM-ing, is raw per-fight Python cost still the wall? If yes → recommend a fast-substrate port (numpy-batch / numba / compiled), with an explicit old-resolver-as-oracle validation plan. If no → say plainly "do NOT port; leave the resolver alone."
6. **Projected post-architecture wall-clock (the headline number Matt wants).** Estimate the ~4,000-kit-variant balance wall-clock under your recommended stack. From 3 days to *what*?
7. **Scaffold register** — every assumed/placeholder value, and a clear measured-vs-assumed line on every number.

### Authority + cross-cutting
- This is your seam — push back hard if the framing above mis-models the actual balance loop.
- Your runner-architecture recommendation is a **load-bearing input to the Mac-side forward-architecture contract effort** (the sim side of the generation↔sim contract) and to the **battle-sim greenfield decision** — flag anything that bears on whether the sim layer should be rebuilt vs. wrapped.

### Output
Write the deliverable to `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md` (or your seam's standard notes path), STATUS-stamped. Auto-commit authorized. When done, report: the deliverable path, the **dominant current bottleneck** (where the time actually goes), the **projected post-architecture wall-clock for ~4,000 kits**, and **whether a resolver port is needed** (yes/no, and why).
