# Engine Greenfield Verdict — WRAP-AND-EXTEND (both seams, empirically measured)

**STATUS:** RECOGNITION RECORD — empirical criterion SATISFIED; ready to commit. Decisions-log entry routed to jack-ryan (decisions-log is jack-ryan's territory; gandalf recommends, jack-ryan canonical-writes).
**Date:** 2026-06-10
**Author:** gandalf (Opus 4.8)
**Decision authority:** Matt (this session) — authorized capture.
**Evidence basis (all MEASURED, not asserted — recognition-validate-commit discipline satisfied at recognition time):**
- `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md` (sim throughput consult)
- `agentic_orchestration/gamora/notes/2026-06-10-spatial-fidelity-reprofile.md` (spatial re-profile — the real combat)
- `agentic_orchestration/rocket/notes/2026-06-10-generation-throughput-and-greenfield.md` (generation throughput + greenfield)

---

## 1. The verdict

**The Reincarnated engine does NOT need a greenfield rebuild. The work is WRAP-AND-EXTEND — an orchestration layer on top of preserved, validated assets.** Both seams reached this verdict independently, from measured numbers:

- **Generation seam (rocket):** WRAP. The mechanical generation path is already free (~9 ms/kit, zero LLM). The cost is LLM naming, and naming is *deferrable*. WRAP verdict.
- **Simulation seam (gamora):** WRAP. Even at true spatial fidelity (10.8–52.9× the 1-D duel), pure-Python delivers 4,000-variant sweeps in single-digit hours under a thin parallel runner. No resolver port justified. WRAP verdict.

This answers the existential question that sat under the whole Fable-5 three-prong consult: *can this engine produce ~400 balanced kits/season (~4,000 variants generated along the way) without a rebuild, and without iteration speed or LLM cost killing the project?* **Yes.**

## 2. What is preserved (the crown jewels — do not rebuild)

- **The validated substrate / catalogue** (the scored, curated data layer — elrond's seam)
- **The engine's internal canonical library** (rocket's)
- **Option-C dimensional generation architecture** (the kit-as-dimensional-composition design)
- **S2 overlay machinery** (`build_variant_enumeration_configs` — produces 270 mechanical overlay variants at $0, already in production)
- **The resolver math** (gamora's fight engine — untouched; no port)

The work is NOT a rewrite of *what a kit is* or *how the substrate is curated*. It is an orchestration/throughput/cost layer.

## 3. The forward-architecture numbers (the contract basis)

| Quantity | Number (measured) |
|---|---|
| Mechanical kit-variant (no naming) | **~9 ms + $0** |
| Delta-named variant (element-swap, batched adaptation) | **~9.7 s + $0.015** |
| Cold-named kit (full LLM naming) | **~54 s + $0.051** |
| Standard 4,000→400 cycle (mechanics-first + survivor-only naming + delta fan-out + parallel) | **~10–35 min + ~$12.4** |
| Spatial kit-variant full-tick gauntlet pass | **~9 s warm / ~43 s cold** |
| 4,000-variant spatial sweep (surrogate-search + full-fidelity-gate) | **Mac ~0.7–3.5 h / PC ~0.3–1.3 h** |

**Naive baseline the architecture defeats:** generation cold/sequential ~60 hr + $203; spatial sweep naive sequential ~2.8 days. Both collapse to hours under the recommended stacks. Cloud is not needed.

## 4. The load-bearing design decisions inside the verdict

### 4.1 Combat-fidelity is the dominant cost lever — and must be named in the contract
1-D duel vs spatial is 11–53× — bigger than tick size (4.3×) or parallelism (4.5–12×). **Decision: search = 1-D duel (cheap, find candidates fast); commit = spatial full-tick (the combat the player actually experiences).** Balancing the final 400 against the duel would be balancing the wrong thing — the genre-classic "balanced in the harness, not the playspace" failure (D3 pre-RoS single-target-dummy itemization vs AoE-density reality; PoE lab-DPS vs map-clear gap). The forward-architecture contract MUST name which fidelity is commit-grade.

### 4.2 Naming-as-survivor-reward (design-correct, not just cost-correct)
Run 4,000 candidates through balance *unnamed* (sim has zero LLM in hot loop); name only the ~400 survivors. Thematically safe because the **fantasy lives in the generation axes** (element/archetype chosen up front in Option-C), not in post-hoc text — the LLM dresses a fantasy already mechanically expressed. Aligns naming budget with kits players see → more curation budget per kit → **protects the D7 AI-tell line.** Order-safe: names don't touch mechanics.

### 4.3 Element-delta variant text — endorsed with a guardrail
The batched "swap element-bearing words, keep structure" delta (~$0.015) is the right variant engine. Sibling-recognizability is a genre *positive* (D2 skill runes, PoE support gems, D3 elemental rune variants — players read variant families). **Guardrail:** when a variant's divergence is mechanical (T4 reversal, trait/experience mix), the delta text must *narrate that divergence*, not let "keep structure" flatten genuinely-distinct siblings into word-swaps. The line: readable variant family (good) vs flat reskin (the D3-vanilla-legendary disease).

### 4.4 A3 surrogate guardrail — empirically earned
The reduced-tick search surrogate flipped a mini-boss winrate 0→1 in 1/18 cells. **Empirical proof that search-grade ≠ commit-grade** — the full-fidelity gate on the final 400 is non-negotiable.

## 5. The work this verdict authorizes (the orchestration layer)

- **Generation (rocket):** defer naming behind the sim gate; add the batched element-adaptation call as the variant text path; fix the cache-hygiene bug (process-stateful skill-id counters defeat the disk cache — 50% miss measured); parallelize naming at concurrency ~10.
- **Simulation (gamora):** thin parallel runner; surrogate-search + full-fidelity-gate pipeline; spatial recalibration (`SPATIAL_DAMAGE_SCALE=4.0` is stale vs current kit power — math-note first per Discipline #1) before spatial becomes commit-fidelity; A3 population audit; PC parallel-factor measurement.
- **Infra (star-lord, routed):** rate-limit tier verification (in-code 50 req/min is ASSUMED), cache-key hygiene fix, batching/model-tier options — all `llm/` infra.
- **Design (gandalf):** the generation↔sim↔UE forward-architecture contract naming combat-fidelity + the §3 numbers; the §4.3 element-delta quality guardrail.

## 6. Routing

- **Decisions-log entry → jack-ryan** (decisions-log is jack-ryan's territory; this record is the recommendation basis).
- **star-lord dispatch** for §5 infra items.
- **Forward-architecture contract authoring** (gandalf, next session) — binds the §3 numbers + §4.1 combat-fidelity decision.

## 7. Sign-off

**Author:** gandalf (Opus 4.8), 2026-06-10. Recognition-validate-commit discipline satisfied at recognition time (evidence is measured, not pending). Three Fable-5 consults (gamora ×2, rocket) converge on WRAP. The engine survives; the work is orchestration, not rebuild.
