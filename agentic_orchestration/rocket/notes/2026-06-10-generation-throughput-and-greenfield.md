# Generation-Pipeline Throughput + LLM-Cost Profile and Greenfield Verdict (~400 Kits/Season)

**STATUS:** CURRENT — Pattern A-deep verdict (Fable-5 consult); empirical profile measured 2026-06-10
**Author:** rocket (content-generation seam)
**Commission:** `agentic_orchestration/gandalf/notes/2026-06-10-rocket-fable5-generation-at-400-consult-commission.md` (gandalf, commit `c5619c1`)
**Companion:** `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md` (sim-side; together these close the engine greenfield map)
**Harness:** `reincarnated-engine/scripts/rocket_generation_throughput_profile_2026_06_10.py` (committed; reproducible)
**Raw artifacts:** `reincarnated-engine/output/rocket-generation-profile-2026-06-10/report.json` (per-call records included)
**Host measured:** Mac Mini, Apple M2, 8 GB RAM, Python 3.12.0; LLM = claude-sonnet-4-6 via production `llm/` client
**Harness LLM spend this session:** $0.22 (pre-fire projection $0.15–0.25; within guard)

---

## 0. Disciplines declared (per commission § Required discipline)

1. **Empirical-evidence-first (Discipline #11):** every load-bearing number was produced by running the production generation + naming path on this host during this session, or extracted from production telemetry (`data/telemetry.db` llm_calls, 5,618 rows; EAA-5 kit JSONs, 75 kits / 603 skills; cycle-14 wave-5 artifacts). Measured-vs-assumed marked on every number; scaffold register at § 8.
2. **Substrate + canonical library + Option C preserved (crown jewels):** nothing here touches what a kit IS, the substrate-vector machinery, or the canonical library. The recommendation is an orchestration/variant-strategy layer. The greenfield question is answered NO (§ 5).
3. **D7 / AI-tell:** § 2.3 maps exactly which LLM output reaches players and through which curation gate. The delta-adaptation path (§ 3) ships ONLY through the existing cohesion-judge + AI-tell gates; the C3 prototype below deliberately bypassed them and is flagged as such — it is a cost/latency measurement, not shippable output.
4. **Recognition-validate-commit (Discipline #40):** scaffold register § 8; one in-prompt scaffold empirically exposed this session (volatile skill-ids defeating the LLM cache, § 3.4).

---

## 1. Empirical generation profile (core deliverable)

### 1.1 Headline table — all MEASURED unless marked

| Quantity | Value | Provenance |
|---|---|---|
| Mechanical kit generation (wave5 Phase 2 path, `w5r1_generate_kit_candidates`, 54 kits) | **8.7 ms/kit** | MEASURED this session |
| Mechanical kit generation (kit-space `ClassGenerator` path, 8 kits, one per element) | **1.9 ms/kit** mean (0.6–3.2) | MEASURED this session |
| Skills per kit | 11 mean kit-space casters (6–12); 12 wave5 path; 8.04 mean across EAA-5 production (603 skills / 75 kits) | MEASURED |
| LLM calls per kit, current production naming path (non-physical) | **2 per skill** (WS1A.4-lite + Phase 5 cohesion-judged naming) → **22/kit** at 11 skills | MEASURED (44 calls / 2 kits, cold) |
| Per-call: latency / cost / tokens (fresh Sonnet call) | **2.45 s** mean; **$0.0023**; 475 in / 59 out | MEASURED (44 cold calls) |
| **Wall-clock per kit, cold-named, sequential** | **54 s** | MEASURED (2 kits / 107.9 s) |
| **Dollar cost per kit, cold-named** | **$0.051** | MEASURED ($0.1017 / 2 kits) |
| In-season Phase 5 extras per shipped kit (Wave B identity 1 call; T4 narration ~1–2 calls) | ~$0.012/kit | ASSUMED from in-code estimates (`phase5_orchestrator` $0.010/Wave-B call) + measured narration pricing |
| Production cache-hit rate on Phase 5 naming (EAA-5, 75 kits) | **67%** (402/603 skills) | MEASURED (production kit JSONs) |
| Re-roll rate, Phase 5 cohesion judge (EAA-5) | 1.008 attempts/skill | MEASURED |
| All-time LLM spend, entire project, 18 seasons | **$15.09** / 5,618 calls / 3.81 s avg | MEASURED (telemetry.db) |
| **Projected: 4,000 variants, cold + sequential, current path** | **~60 hours wall-clock; ~$203** (88,000 calls) | PROJECTED from measured per-kit cost |

### 1.2 Where time and dollars go (per cold-named kit)

| Component | Wall-clock | % time | Dollars | % dollars |
|---|---|---|---|---|
| **LLM naming calls (22 × 2.45 s sequential)** | ~54 s | **99.98%** | $0.051 | **~100%** |
| Mechanical generation (substrate lookup, chain composition, T4 wire-up, stat allocation) | 2–9 ms | 0.02% | $0 | 0% |
| I/O (kit JSON write) | ~1 ms | ~0% | $0 | 0% |
| DB access during generation | 0 (Phase 2 is pure in-memory; Discipline #46) | 0% | $0 | 0% |

**The commission's hypothesis is confirmed: LLM dominates everything — but only in the naming/identity layer.** Kit *mechanics* (the thing the sim consumes) are LLM-free and cost ~9 ms/kit. The entire generation-side scaling problem is the player-facing text layer.

### 1.3 The fear, sized precisely

Cold/sequential naming of 4,000 variants = ~60 hours and ~$203 — slow enough to kill iteration cadence (not a "runaway bill"; $203 is survivable, 60 hours is not, and 88,000 calls would hit rate-limit ceilings long before latency mattered). The architecture in § 4 reduces this to **minutes and ~$12** (§ 6) — and the largest single lever is not the delta path; it is the observation that **naming does not need to fire before the sim** (§ 3.3).

---

## 2. LLM-in-generation audit

### 2.1 Complete call-site inventory (generation seam + adjacent)

| Call site | Module (seam) | Calls | Purpose | Per-call cost (measured) |
|---|---|---|---|---|
| WS1A.4-lite flavor judgment | `llm/ws1a4_lite_flavor_judgment.py` via `generation/kit_space_skill_naming.py` | 1/skill (non-physical kits; physical opt-out) | flavor-vs-canonical naming decision + name | $0.0023 |
| Phase 5 skill-node naming | `generation/phase5_skill_naming.py` | 1/skill + re-rolls (×1.008 measured) | name + flavor_text + effect_description + tags; programmatic cohesion judge (NOT a second LLM) | $0.0022 |
| Phase 5 T4 narration | `generation/phase5_t4_narration.py` | 1/form | T4 manifestation + rationale prose | ~$0.0025 |
| Wave B per-kit identity | `llm/phase5_orchestrator.py` (star-lord) | 1/shipped kit | kit name + identity narrative | ~$0.010 (in-code estimate) |
| Wave A faction labels / F-C relationships / Wave-S season | `llm/phase5_orchestrator.py` (star-lord) | 3–5 + per-cluster-pair + 1, per SEASON | faction/season identity | amortized ≈ $0.001/kit at 400 kits |
| Legacy season path (cosmological vocab, theme coalescence, element selection, class/monster/gear/trial naming) | `generation/season_orchestrator.py` + `llm/naming.py` | ~310/season measured | legacy full-season naming | $0.88/season measured — **not on the 400-kit forward path** |

**Nothing else in the generation seam calls the LLM.** Phase 2 kit candidate generation (`w5r1_generate_kit_candidates`), the B6 kit builder, BC substrate sampling, T4 wire-up, gear/partition rolling — all LLM-free (verified by import audit: exactly 4 files in `generation/` touch `llm/`).

### 2.2 Per-kit LLM totals (current path, 11-skill caster kit)

- Naming: 22 calls, $0.051, 54 s sequential — **dominant**
- Shipped-kit identity layer (Wave B + T4 narration + amortized faction): ~2–3 calls, ~$0.013
- **All-in per shipped kit: ~$0.065, ~24 calls**

### 2.3 D7 / AI-tell curation map (where LLM text reaches players)

| Surface | Curation gate | Free-form? |
|---|---|---|
| Skill names | WS1A.4-lite binary judgment (template-constrained; Q18 vocabulary pool; canonical deterministic fallback on LLM failure) | No — constrained |
| flavor_text / effect_description | Phase 5 programmatic 5-dimension cohesion judge, threshold 0.70, re-roll on FAIL, placeholder on exhaustion | Free-form prose, GATED |
| T4 manifestation prose | 2-dimension cohesion judge + static-template Path-A fallback | Free-form prose, GATED |
| Kit identity narrative (Wave B) | AI-tell phrase grep (takes precedence) + compliance scoring + regeneration | Free-form prose, GATED |
| Kit mechanics (damage, geometry, cooldowns) | **Never LLM-generated** | n/a |

No surface ships raw un-curated LLM output today. The delta path (§ 3) MUST inherit the same gates — stated as a hard requirement in § 4.3.

---

## 3. The variant-as-delta verdict (headline question)

**VERDICT: YES — and half of it is already implemented in production.** The commission's "untested design hypothesis" is in fact tested on two of the four variant axes; this session measured the remaining (element-swap LLM-content) half.

### 3.1 Mechanical deltas already exist in production (MEASURED — it shipped)

Cascade-R3 S2 (`gauntlet_sim.build_variant_enumeration_configs`) already fans 18 BC cells × 6 T4 strategies × 3 investment profiles → **270 variant configs as pure overlays** of base kits (`_patch_kits_profile` + `_t4_strategy_alteration_fields` + `VariantKitRow`), with **zero LLM calls and zero re-generation** — variants inherit base-kit lineage and even base-kit gauntlet results where semantically justified. The cycle-14 production season ran 54 base kits + 270 variant rows this way. **T4-reversal/amplification and investment/experience-mix variant axes are solved, at ~0 marginal cost.** Racial-trait mix is the same overlay class (trait rank-stacks; `partition_modifier_pool` machinery) — ASSUMED same-cost, same mechanism, unmeasured.

### 3.2 LLM-content deltas — measured this session (the open half)

Three experiments against a cold cache (true API calls; per-call records in report.json):

| Experiment | Result |
|---|---|
| **C1 — identical kit re-named** | 50% cache hit. The misses are a *bug-shaped finding*, not semantic: process-stateful skill-id counters leak into prompts (`skill_000283` → `skill_000327` on rebuild), so identical content misses the cache (§ 3.4). Production cross-run measured 67% hit (EAA-5). With id-hygiene, identical re-runs → ~100% hit, $0. |
| **C2 — element-swap variant via current per-skill path** | 0% cache reuse — 22 fresh calls, $0.050, 62 s. **The current path treats an element variant as a full cold generation.** Confirms the commission's fear for the as-is pipeline. |
| **C3 — delta-adaptation prototype: ONE batched call adapting the whole named fire kit → water** | **1 call, $0.0148, 9.7 s, all 11 skill ids preserved**, quality high ("Flame Dash"→"Tide Dash"; "a mage who stands still is a mage who burns"→"…drowns" — structure, tone, length preserved; element-bearing words swapped). |

**Per-variant LLM cost: $0.051/22 calls/54–62 s (cold) → $0.015/1 call/9.7 s (delta) — 3.4× cheaper in dollars, 22× fewer calls (the rate-limit currency), 6× faster.** And element-swap is the *expensive* variant axis; T4/invest/trait/experience variants reuse base-kit names outright at $0 (§ 3.1).

### 3.3 The bigger lever the commission framing missed (seam pushback, per commission § Authority)

The 10× fan-out exists to feed the **balance loop** — and gamora's companion profile establishes the balance loop consumes *mechanical* kits with **zero LLM in the hot loop**. Therefore: **the 4,000 variants never need naming at all. Only the ~400 shipped survivors do.** Generation of 4,000 sim-ready mechanical variants costs ~35 s and $0. Naming fires once, post-sim, on survivors: 40 general kits cold-named + ~360 shipped variants delta-named. The commission's "40 cold + 360 cheap deltas" arithmetic is right, but it applies to the *post-sim survivor set*, not to the 4,000 — the 4,000-cold-generation fear conflates mechanical generation (free) with content generation (LLM, deferrable).

**Design caveat (flagged, not assumed away):** this requires that no pre-sim surface needs player-facing names for all 4,000 (e.g., a variant-browser UI). If gandalf/Matt later require pre-sim names for all variants, the all-4,000-delta cost is ~$61 / ~1.1–1.6 hr (§ 6 worst-case row) — still survivable.

### 3.4 Cache-hygiene finding (within-seam fix, measured)

LLM prompts embed volatile skill ids; ids are process-stateful; identical semantic content therefore misses the disk cache across rebuilds (C1: 50% miss). Fix: strip/normalize volatile ids out of prompt text (prompt shape = my seam) and/or normalize cache keys (cache infra = star-lord). Cheap, measurable (C1 re-run hits 100%), and it makes regeneration-after-crash and repeat-season fires nearly free.

## 4. Parallelizability + recommended generation-runner architecture

### 4.1 Parallelism facts

- **Mechanical generation:** embarrassingly parallel per kit (pure in-memory, seed-deterministic, no shared state) — but at 8.7 ms/kit it does not even need it; 4,000 sequential ≈ 35 s.
- **LLM naming:** the production naming-batch path (`apply_kit_space_skill_naming_batch`) is **synchronous and sequential** — that is where the 54 s/kit comes from. The codebase **already contains the correct concurrent pattern**: `llm/phase5_orchestrator.py` (star-lord) runs asyncio + AsyncAnthropic + semaphore, DEFAULT_CONCURRENCY=10.
- **Rate limit is the real ceiling, not latency:** in-code comment assumes Sonnet tier-2 = 50 req/min (ASSUMED — unverified against actual org tier; route to star-lord to measure). At 50 RPM, 88,000 cold calls = ~29 hours no matter the concurrency; the delta architecture's 22× call-count reduction is therefore worth more than any concurrency tuning.

### 4.2 Recommended architecture (wrap-layer; nothing inside generators changes)

```
40 general kits (mechanical)             ~0.4 s, $0          [existing generators]
  → fan out ~10× via S2-style overlay deltas                 [extend build_variant_enumeration_configs
    (element swap | range/movement; T4 rev/amp;               with element-swap + range/movement axes;
     racial-trait mix; experience mix)    ~35 s, $0           racial/experience = existing overlay class]
  → 4,000 sim-ready mechanical variants
  → gamora's parallel gauntlet runner     ~12 min             [companion deliverable]
  → ~400 survivors selected
  → NAMING FIRES HERE (post-sim only):
      40 general kits: cold per-skill naming (existing path, made async)   880 calls, $2.03
      ~360 shipped variants: ONE delta-adaptation call each                360 calls, $5.32
      → ALL delta output through existing Phase 5 cohesion judge +
        AI-tell grep gates (same thresholds; re-roll → cold fallback)
      Wave B identity per shipped kit (existing star-lord async path)      400 calls, ~$4
  → emit kit JSONs for shipped 400 (kit-space schema)
```

### 4.3 Hard gates (non-negotiable)

- **D7:** delta-adapted text passes the SAME programmatic cohesion judge + AI-tell grep as cold-named text. A variant that fails the judge twice falls back to cold per-skill naming ($0.05 worst case — bounded). The C3 prototype did NOT run the judge; productionizing the delta call = wiring it through `phase5_skill_naming`'s existing judge entry points. ~1–2 days, my seam.
- **Oracle discipline:** the delta path is validated against current cold generation as oracle on one archetype family (10 variants: cold-name AND delta-name, compare cohesion-judge score distributions) before being relied on. Cheap: ~$0.70, minutes.
- **Discipline #3 analog:** one delta call per (general kit × variant axis) cell; no parallel duplicate adaptation of the same cell.

### 4.4 Routed to star-lord (LLM-infra findings — audit only, per scope guard)

1. Make the naming batch concurrent via the existing phase5 asyncio pattern (the pattern is already in their seam; generation just calls it).
2. Cache-key normalization vs volatile ids (§ 3.4; joint with my prompt-shape fix).
3. Multi-target batched adaptation (adapt 1 kit → up to 9 elements in ONE call; output token-bound; could halve delta cost again).
4. Model-tier experiment: WS1A.4-lite is a binary judgment + short name — Haiku-class model likely sufficient (~3× cheaper on that call class). Needs a quality A/B through the cohesion judge.
5. Measure the actual org rate-limit tier (the 50 RPM in-code figure is a conservative scaffold).

## 5. Greenfield-vs-wrap verdict for the generation seam

**WRAP-AND-EXTEND. Independent of, and agreeing with, the sim-side verdict.**

- The mechanical generators (Option C dimensional generation, BC substrate sampling, B6 kit builder, T4 wire-up, canonical library) are validated, LLM-free, and run at **milliseconds per kit** — throughput provides zero justification for rebuilding them, and they are the most design-validated asset in my seam.
- The variant-fan-out mechanism **already exists** (S2 overlay enumeration, shipped in production); it needs new axes (element swap, range/movement), not a new architecture.
- 100% of the scaling cost lives in the LLM naming/identity layer, which is **confined, cacheable, delta-adaptable, and deferrable to post-sim survivors** — all four properties are wrap-layer properties. A greenfield rebuild would not change a single one of these numbers, because the cost is API latency + call count, not pipeline structure.
- The genuine debt is **two kit shapes** (wave5 Phase-2 candidate dicts vs kit-space export dicts — two generator paths: `BcTargetSubspaceGenerator`/B6 vs `ClassGenerator`). That is a *unification refactor* inside the wrap (MIGRATION.md-gated, ADR-004), not a rebuild: both paths share foundation/canonical/skill-schema substrate; the divergence is at the export-dict assembly layer.

**Re-open criterion (empirical, not time-based):** if a future requirement makes naming load-bearing *inside* the balance loop (LLM-scored cohesion as a selection objective at 4,000-variant scale), the call-count math changes by 10× and the architecture should be re-profiled.

## 6. Projected post-architecture generation cost (headline numbers)

| Scenario | Wall-clock | Dollars | Calls |
|---|---|---|---|
| **Current path, 4,000 cold, sequential (the fear)** | **~60 hr** | **~$203** | 88,000 |
| Current path, 4,000 cold, asyncio concurrency-10 | ~6 hr (latency-bound) / ~29 hr (if 50 RPM binds) | ~$203 | 88,000 |
| **Recommended: 4,000 mechanical + post-sim naming of 400 survivors** | **~35 s generation + ~10 min naming (concurrency-10) / ~33 min (if 50 RPM binds)** | **~$12.4** | ~1,640 |
| Worst-case design demand: all 4,000 variants named (delta) | ~35 s + ~68 min (concurrency-10) / ~1.6 hr (50 RPM) | ~$61 | 4,840 |

From **~60 hours + $203** to **~10–35 minutes + ~$12** for the standard season cycle. Generation is no longer the metabolic constraint; combined with gamora's ~12-minute sim sweep, a full 4,000-variant → 400-shipped season cycle is **under an hour end-to-end** on current hardware.

## 7. Generation↔sim forward-architecture contract (generation-side number)

**Contract statement:**
- **Mechanical kit-variant (sim-ready): ~9 ms + $0 each; 4,000-variant batch ≈ 35 s + $0.** Shape: `KitCandidate.to_character_dict()` + `VariantKitRow` overlay rows — exactly what gamora's gauntlet/runner consumes today; no translation layer needed.
- **Named/shipped kit (player-ready): ~$0.051 + ~5.5 s amortized (cold general kit, concurrency-10) or ~$0.015 + ~1 s amortized (delta variant); 400-survivor naming batch ≈ 10–35 min + ~$12.4.**

**Shape-mismatch flags for the Mac-side forward-architecture effort:**
1. **Two kit export shapes exist** (wave5 Phase-2 candidate dict vs kit-space `kit_*.json` schema). Sim consumes the former; UE-emit (mantis WS1 corpus ingestion) consumes the latter. Unify at the export-assembly layer before the 400-kit ship (MIGRATION.md-gated; my seam + star-lord emit pipeline).
2. **`VariantKitRow` carries no skills payload** (it is an overlay row). A *shipped* variant needs a materialized full kit JSON with adapted names for UE-emit. The delta path must therefore end in a materialization step (overlay → full kit dict → delta-named → emitted). Flag to star-lord (emit) + mantis (ingestion contract).
3. **Naming timing:** the contract above assumes post-sim naming (§ 3.3 caveat). If any pre-sim surface needs names for all 4,000, use the worst-case row in § 6.

## 8. Scaffold register (Discipline #40) — measured vs assumed, every number

| Item | Status |
|---|---|
| 8.7 ms/kit (w5r1, 54 kits), 1.9 ms/kit (ClassGenerator, 8 kits) | **MEASURED** this session (harness in repo) |
| 22 LLM calls/kit; 2.45 s + $0.0023/call; $0.051 + 54 s per cold kit | **MEASURED** this session (44 cold calls, temp cache) |
| C2 element-swap = 0% cache reuse; $0.050/variant via current path | **MEASURED** this session |
| C3 delta adaptation = 1 call, $0.0148, 9.7 s, id-fidelity intact | **MEASURED** this session (n=1 kit, 11 skills — small sample; oracle validation pass required before production reliance, § 4.3) |
| C1 identical re-run 50% cache hit; cause = volatile skill-ids in prompts | **MEASURED** + root-cause verified in call logs |
| 67% Phase 5 cache-hit; 1.008 attempts/skill (production, 75 kits / 603 skills) | **MEASURED** (EAA-5 kit JSONs) |
| $15.09 all-time / 5,618 calls / 3.81 s avg; $0.88 legacy season | **MEASURED** (telemetry.db, read-only) |
| S2 270-variant overlay enumeration, zero LLM | **MEASURED** (production code + cycle-14 artifacts) |
| 60 hr / $203 cold-sequential 4,000 projection | **PROJECTED** from measured per-kit cost (linear; justified — calls are independent) |
| ~$12.4 / 10–35 min post-architecture projection | **PROJECTED** from measured per-call costs; assumes § 3.3 post-sim naming (design caveat flagged) |
| Wave B identity $0.010/call | **ASSUMED** (in-code estimate in `phase5_orchestrator`; actual cost not in telemetry for that path) |
| Sonnet rate limit 50 req/min | **ASSUMED** (in-code scaffold comment; unverified org tier — routed to star-lord to measure) |
| Racial-trait variants = same zero-LLM overlay class as T4/invest | **ASSUMED** (same mechanism family; unmeasured) |
| Delta-adaptation quality at scale (cohesion-judge pass-rate of adapted text) | **ASSUMED pending oracle pass** (§ 4.3; ~$0.70 to measure on one archetype family) |
| 40×10 season structure | **DESIGN-CHAIR** (commission's own flag; profile holds for any cold:delta ratio — § 6 gives both bounds) |
| C2 used same-seed re-generation as the "element swap" proxy, not an in-place mechanical swap | **METHOD NOTE** — conservative (an in-place swap could only cache-hit MORE, not less) |

## 9. Recommended next actions (queued; not executed without authorization)

1. **Within-seam (ADR-002):** oracle validation of the delta-adaptation path on one archetype family (10 variants, cold vs delta, cohesion-score distributions; ~$0.70). The empirical criterion gating production reliance on § 3/§ 4.
2. **Within-seam:** prompt-shape id-hygiene fix (§ 3.4) + wire delta output through existing cohesion/AI-tell gates. ~1–2 days. MIGRATION.md if the variant materialization step lands a new emitted shape.
3. **Within-seam + gamora coordination:** extend `build_variant_enumeration_configs` with element-swap + range/movement axes (the S2 mechanism generalizes; math note first per Discipline #1).
4. **Routed to star-lord:** § 4.4 items 1–5 (async naming batch, cache-key normalization, multi-target batching, Haiku-tier A/B, rate-limit tier measurement).
5. **Design question to gandalf/Matt:** confirm no pre-sim surface needs names for all 4,000 variants (§ 3.3 caveat) — decides between the $12 and $61 rows.
6. **Cross-seam flag to KR:** kit-shape unification (wave5 candidate dict vs kit-space JSON) should be scheduled before 400-kit ship; touches my seam + star-lord emit + mantis ingestion contract.

---

**Sign-off:** rocket. The generation seam's metabolism at 4,000 variants is ~35 seconds of mechanics + ~10–35 minutes of survivor-naming under the recommended wrap, ~$12 a season cycle. Dominant cost is LLM naming latency/call-count — confined to player-facing text, deferrable to post-sim, delta-adaptable at 3.4× cheaper and 22× fewer calls (measured). Variant-as-delta: YES, half already shipped in production. No rebuild. Wrap, extend the overlay axes, gate every adapted word through the existing judges.
