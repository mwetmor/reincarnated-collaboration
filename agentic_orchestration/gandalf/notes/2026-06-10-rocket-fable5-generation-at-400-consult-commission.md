# Rocket (Fable-5) — Generation-Pipeline-at-400 Throughput + Greenfield Consult

**STATUS:** COMMISSION — paste-ready opener for a fresh Fable-5 Rocket session (the generation-side counterpart to the gamora battle-sim throughput consult; closes the greenfield map)
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Why Fable-5:** single-agent design+profiling run at the higher tier; gradable output.
**Companion:** `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md` (the SIM-side throughput consult — this is the GENERATION-side counterpart; together they answer the engine greenfield question)

**Launch notes (do NOT paste into the Rocket session):**
- Rocket is Mac-resident (generation seam, in `reincarnated-engine`). Launch Mac-side:
  ```
  cd ~/Games/reincarnated-engine
  claude --agent rocket --model claude-opus-4-8
  ```
- The explicit `--model claude-opus-4-8` flag forces Fable-5 regardless of frontmatter pull state.

---

## PASTE-READY OPENER (everything below the line)

---

You are rocket, the content-generation-seam engineer (generation/, element/, anchor/, foundation/, and the engine's internal canonical library). Read your operating-procedure skill and execute your session-start protocol. Then take on the commission below.

**Mission: profile the content-generation pipeline's throughput AND LLM-cost at scale, then recommend whether the generation seam should be wrapped-and-extended or greenfield-rebuilt to produce ~400 balanced kits/season — and deliver the generation-side number for the forward-architecture contract.**

### The problem (why this is existential — same metabolism argument as the sim side)
The engine's content target shifted from ~5–10 kits/season to **~400 balanced kits/season.** Landing those 400 likely means generating **~10× variants** along the way → on the order of **~4,000 kit generations.** The sim side just got profiled (gamora; companion deliverable above) — the balance loop is ~12 min parallel for 4,000 variants and has **zero LLM in the hot loop.** But **generation is exactly where the LLM lives.** If generating 4,000 kit-variants is itself a multi-day job or a runaway LLM bill, the iteration loop dies on the generation side even though the sim side is fast. **Iteration speed is the project's metabolism; a slow OR ruinously-expensive generation step ends the project just as surely as a slow sim.** Your job: find out how real that fear is, and what architecture kills it.

### The 40×10 structure (the key lever — read carefully)
The 400 are not 400 independent generations. The structure is **~40 general kits × ~10 variants each.** Variants of one general kit diverge along: element swap (across a caster archetype) OR range/movement (across a physical archetype), then differentiated further by **T4 reversals/amplifications, racial-trait mix, and experience mix.** The design hypothesis (untested) is that variants of one general kit are *perturbations of a shared seed*, not cold-from-scratch generations.

**The load-bearing question this raises for you:** can the 10× fan-out be generated as a **structured DELTA off the general kit** (cheap perturbation: swap element, apply T4 reversal, remix traits) rather than 10 independent cold generations? If yes, generation cost ≈ **40 cold + ~360 cheap deltas**, not 4,000 cold — and the LLM cost collapses proportionally. If no (each variant needs full fresh generation including fresh LLM calls), the cost is ~4,000× the per-kit LLM cost. **This single question likely dominates the whole projection.** Profile it; don't assume it.

### Required discipline (declare at the top of your deliverable)
1. **Empirical-evidence-first.** MEASURE, don't assert. Instrument the current generation pipeline and report real numbers (per-kit wall-clock, per-kit LLM call count + latency + token cost). A profile from reading code without running it is insufficient — run it and time it.
2. **Preserve the validated substrate + canonical library (your crown jewels).** The catalogue/substrate, the canonical library, and the dimensional-generation architecture (Option C) are validated assets. This consult is about the **throughput/cost/orchestration layer and the variant-fan-out strategy, NOT a rewrite of what a kit IS or how the substrate is curated.** If you recommend any port, it is a same-output port validated against current generation as oracle.
3. **D7 / AI-tell line.** Generation is where LLM output reaches player-facing surfaces (names, descriptions, ability text). Any throughput optimization MUST preserve the AI-tell discipline — no shortcut that ships raw/un-curated LLM output to players. Flag where the LLM output passes through human-authored templates vs. where it's free-form.
4. **Recognition-validate-commit** — flag every scaffold/assumed value (Discipline #40); measured-vs-assumed line on every number.

### Scope guard
**Generation throughput + cost + variant-strategy + greenfield-vs-wrap ONLY.** In scope: profiling current generation, the LLM-in-generation audit, the variant-as-delta question, parallelization of generation, and whether the generation seam needs a rebuild. OUT of scope: the balance/sim loop (gamora's seam — already profiled), telemetry/export (star-lord's), the LLM-call *infrastructure* itself (star-lord owns `llm/` — you audit how much generation CALLS it and route infra-optimization findings to star-lord), redesigning what "a kit" is, the runtime lookup boundary (cosmograph-pivot — generation is offline-batch by design; don't touch runtime).

### Required deliverable contents
1. **Empirical generation profile (core deliverable)** — instrument and report ACTUAL numbers for generating one kit today: wall-clock per kit; **LLM call count per kit, per-call latency, per-call token cost (the likely dominant cost — confirm or rule out)**; CPU/substrate-lookup cost; I/O. Give the breakdown as percentages of total time AND total dollar cost. Then project ~4,000-variant generation **cold/sequential** on the current setup — wall-clock AND dollar cost.
2. **LLM-in-generation audit (likely the dominant cost).** Where exactly does generation call the LLM, how many calls per kit, for what (naming? description? ability text? cohesion judging?). This is the generation-side analog of the question that turned out to dominate nothing on the sim side — here it likely dominates everything. Quantify it in both wall-clock and dollars.
3. **The variant-as-delta verdict (the headline architectural question).** Can the 10× fan-out be modeled as a cheap structured perturbation of a general kit's seed (element/T4/trait/experience deltas) rather than cold generation — *specifically, can it reuse or cheaply-adapt the general kit's LLM-generated content rather than re-calling the LLM 10×?* Measure or prototype the delta path if feasible; if not feasible to measure, reason about it explicitly with flagged assumptions. **This is the number that decides whether 4,000 variants costs ~40 cold-generations-worth or ~4,000.**
4. **Parallelizability + recommended generation-runner architecture.** Is generation embarrassingly parallel (per-kit independent)? Estimate the parallel speedup; name coordination/rate-limit costs (LLM API rate limits are a real ceiling — flag it). Recommend the scale-out generation architecture (parallel + delta-fan-out + any caching of shared LLM content).
5. **Greenfield-vs-wrap verdict for the generation seam.** After the variant-delta + parallelism analysis: does the generation pipeline need a rebuild, or wrap-and-extend? Preserve substrate + canonical library + Option-C architecture regardless. Be explicit: wrap or rebuild, and why. (The sim side concluded WRAP; state your independent verdict for generation.)
6. **Projected post-architecture generation wall-clock + dollar cost (the headline numbers).** ~4,000-variant generation under your recommended stack: from *what* to *what*, in both wall-clock and dollars.
7. **Generation↔sim forward-architecture contract.** You emit kits in the shape gamora's sim consumes. State the generation-side contract number ("~X s + ~$Y per kit-variant generated; ~Z min + ~$W per 4,000-variant batch") and flag any shape-mismatch between what generation emits and what the sim/UE-emit layers need (this feeds the Mac-side forward-architecture effort).
8. **Scaffold register** — every assumed/placeholder value; measured-vs-assumed line on every number.

### Authority + cross-cutting
- This is your seam — push back hard if the framing above mis-models the actual generation pipeline (especially the 40×10 / variant-as-delta hypothesis, which is design-chair speculation, NOT a measured property).
- Your verdict is a **load-bearing input to the engine greenfield decision** (the generation half; gamora delivered the sim half) and to the **Mac-side generation↔sim↔UE-emit forward-architecture contract.**
- Route any LLM-*infrastructure* optimization findings (batching, model-tier, caching layer) to star-lord (`llm/` seam) rather than implementing them — you audit the call pattern; star-lord owns the infra.

### Output
Write the deliverable to `agentic_orchestration/rocket/notes/2026-06-10-generation-throughput-and-greenfield.md` (or your seam's standard notes path), STATUS-stamped. Auto-commit authorized. When done, report: the deliverable path, the **dominant current cost** (wall-clock + dollars — likely LLM), the **variant-as-delta verdict** (the lever that decides everything), the **projected post-architecture 4,000-variant cost** (wall-clock + dollars), and **whether the generation seam needs greenfield or wrap.**
