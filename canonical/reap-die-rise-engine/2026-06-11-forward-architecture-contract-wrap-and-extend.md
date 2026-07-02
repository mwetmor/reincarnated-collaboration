# Forward-Architecture Contract — Wrap-and-Extend (Kernel-Freeze + Golden-Master Spine)

> **STATUS:** CURRENT (load-bearing as of 2026-06-11) — Matt-authorized authoring this session ("yes please" to kernel-freeze + golden-master as contract spine). Gate-1 critique-pair review (jack-ryan) QUEUED per Discipline #51. Refutation clause § 8 is LIVE: the gap-register architecture-fit audits (rocket + gamora, fired 2026-06-11 in parallel with this authoring) can amend § 2 kernel boundaries via the module-targeted-greenfield path — this contract pre-commits to honoring that evidence.

**Date:** 2026-06-11
**Author:** gandalf (story-and-design steward)
**Decision authority:** Matt 2026-06-11 (this session), following sustained Pattern-B challenge of the 2026-06-10 WRAP verdict
**Evidence basis (all MEASURED):**
- `canonical/story/2026-06-10-engine-greenfield-verdict-wrap-and-extend.md` (the verdict this contract operationalizes)
- `agentic_orchestration/gamora/notes/2026-06-10-sim-throughput-profile-and-runner-architecture.md`
- `agentic_orchestration/gamora/notes/2026-06-10-spatial-fidelity-reprofile.md`
- `agentic_orchestration/rocket/notes/2026-06-10-generation-throughput-and-greenfield.md`

**Companion docs:** doc 38 (D1-D10 delivery keystone); `canonical/story/2026-06-05-cosmograph-pivot.md` (lookup-not-generation); `canonical/story/2026-06-06-atomic-substrate-registry.md` + `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` (cemented future-state); `canonical/story/2026-06-10-engine-architecture-canonical-synthesis.md` § 9 (gap register — the audit instrument)

---

## 0. TL;DR

The engine work ahead is governed by one structural rule: **validated kernels go read-only; all new work is new code in new files against the interfaces this contract names.** Agents never surgically modify living kernels — the empirically observed failure mode of the first rebuild ("what should change vs what should remain" churn) is retired *by construction*, and the empirically observed failure mode of the second rebuild (silent requirement omission — the lost battle simulator) is retired by preserving the code that IS the complete requirements register. The greenfield development experience (clean spec → clean implementation) is delivered on every line agents actually write, because every line they write is new.

## 1. Provenance — why this contract has the shape it has

Matt's empirical history across three engine builds (2026-06-11 session, verbatim substance):

| Event | Mode | Cost | Failure mode exhibited |
|---|---|---|---|
| First build | Greenfield from small specs | ~2 overnight sessions | None (spec surface was small) |
| First rebuild | Modify-in-place | ~2 sessions + 2 sessions churn | **Change-isolation cost** — "inability to target what should change vs what should remain" |
| Second rebuild | Re-render accumulated requirements | A week+ of sessions | **Silent omission drift** — "wrapped in a puzzle of requirements"; the entire battle simulator was omitted |

This contract is designed to retire BOTH failure modes simultaneously:
- **Change-isolation cost** → retired by the kernel-freeze (§ 2): nothing inside a kernel boundary is modified; agents only write new code against named interfaces.
- **Silent omission drift** → retired by kernel preservation (§ 2) + golden-master protocol (§ 3): existing validated code is the complete requirements register, including every requirement nobody wrote down. Today's canonical spec surface (docs 38-51 + atomic-substrate-registry + hypothesis-flow + BC axes) is ~10× the surface that produced the second rebuild's omission drift; a full re-render is that failure mode at scale.

Genre anchor: D2:Resurrected preserved the 20-year-old game logic as the running simulation kernel and built the new layer around it — because validated behavior IS the product. Warcraft III: Reforged replaced and broke behavior players could feel. GGG forked PoE2 to a separate engine only when *design divergence* exceeded what extension could carry — never because code was old. § 8 names design divergence as this contract's only legitimate refutation axis.

## 2. The kernel boundary — read-only validated assets

The following are **KERNELS: read-only libraries behind named interfaces.** No agent modifies kernel internals as part of wrap-and-extend work. Period.

| Kernel | Seam owner | Why frozen (validation history) |
|---|---|---|
| **Resolver math** (fight engine core: damage resolution, three-path routing per doc 47, ailment/control mechanics, tick loop) | gamora | ~15 seasons of telemetry behind its behavior; the A3 case (tick-size change alone flipped a mini-boss winrate 0→1 in 1/18 cells) proves outcome sensitivity to implementation detail no spec captures |
| **Option-C dimensional generation core** (kit-as-dimensional-composition) | rocket | The validated architecture of *what a kit is*; mechanical path measured at ~9 ms + $0 |
| **S2 overlay machinery** (`build_variant_enumeration_configs`) | rocket | In production; 270 mechanical overlay variants at $0 |
| **The curated substrate / catalogue** (89,839-row library; v1_scope 2,293 LOCKED; 125 clusters at 0.9444 purity) | elrond | The whole of Cycle 10; score-don't-filter insurance preserved |
| **Engine internal canonical library** | rocket | Validated content definitions consumed engine-wide |

**Interface naming obligation:** before any orchestration code consumes a kernel, the consuming seam declares the interface (functions/entry-points + input/output schema) in its MIGRATION.md. The interface declaration IS the wrap boundary. Undeclared kernel entry-points are not consumed.

**What is explicitly NOT kernel** (new code, greenfield-style, agents' clean-implementation zone): the parallel sim runner; the surrogate-search + full-fidelity-gate pipeline; naming orchestration (deferral, batching, delta fan-out); `llm/` infra fixes (cache-key hygiene, rate-limit verification, batching/model tiers); the export packet shaped to UE; pattern-library Phases A-E integration layers; anything the gap-register audits route to module-targeted greenfield per § 8.

## 3. Kernel-change protocol — the only door in

A kernel is changed ONLY when all of the following fire, in order:

1. **Math-note first** (Discipline #1) naming the change, its rationale, and its predicted output deltas.
2. **Golden-master capture BEFORE the change:** a pinned corpus of kernel inputs → outputs (for the resolver: a fixed seed-set of fights across encounter types + kit archetypes; for generation: a fixed seed-set of kit tuples → emitted kits) committed as the oracle.
3. **The change, in isolation** (Discipline #24 single-parameter sweep isolation applies).
4. **Golden-master re-run:** every output delta is either (a) predicted by the math-note, or (b) a STOP — unpredicted deltas mean the change is not understood; revert and re-derive.
5. **Telemetry tag** (Discipline #7) so the kernel-version lineage is queryable.

**First scheduled application:** the spatial recalibration (`SPATIAL_DAMAGE_SCALE=4.0` stale vs current kit power). This is the test case that proves the protocol before anything heavier uses it. Math-note (gamora) → golden-master capture → recalibration → predicted-delta verification. Spatial does not become commit-grade fidelity (§ 5) until this completes.

## 4. The binding numbers (measured 2026-06-10; re-measure triggers below)

| Quantity | Number |
|---|---|
| Mechanical kit-variant (no naming) | ~9 ms + $0 |
| Delta-named variant (element-swap, batched) | ~9.7 s + $0.015 |
| Cold-named kit (full LLM naming) | ~54 s + $0.051 |
| Standard 4,000→400 cycle (mechanics-first + survivor-only naming + delta fan-out + parallel ~10) | ~10–35 min + ~$12.4 |
| Spatial kit-variant full-tick gauntlet pass | ~9 s warm / ~43 s cold |
| 4,000-variant spatial sweep (surrogate-search + full-fidelity-gate) | Mac ~0.7–3.5 h / PC ~0.3–1.3 h |

**Re-measure triggers:** any kernel change per § 3; any orchestration-layer milestone close (the wrap must not silently degrade the measured baseline); rate-limit tier verification landing (the 50 req/min figure is ASSUMED in code — star-lord verifies).

## 5. Combat-fidelity lock

- **Search-grade = 1-D duel.** Cheap candidate discovery only. Never balance-authoritative.
- **Commit-grade = spatial full-tick.** The combat the player experiences. The final ~400 are validated here, no exceptions — empirically earned by the A3 violation (1/18 cells flipped under a reduced-tick surrogate). Balancing against the duel would be the genre-classic harness-not-playspace failure (D3 pre-RoS single-target-dummy itemization vs AoE-density reality).
- **Gate:** spatial recalibration (§ 3 first application) must complete before spatial holds commit-grade status.

## 6. Naming-as-survivor-reward + element-delta guardrail

- 4,000 candidates run the balance pipeline **unnamed** (zero LLM in the hot loop). Only ~400 survivors are named. Design-correct, not merely cost-correct: the fantasy lives in the generation axes (Option-C); the LLM dresses a fantasy already mechanically expressed; naming budget concentrates on kits players see — protecting the D7 AI-tell line.
- **Element-delta guardrail (binding on rocket):** when a variant's divergence is mechanical (T4 reversal, trait/experience mix), the delta text must *narrate that divergence*. "Keep structure" must not flatten genuinely-distinct siblings into word-swaps. The line: readable variant family (D2 skill runes, PoE support gems) vs flat reskin (D3-vanilla-legendary disease).

## 7. UE-fit clause — the export contract is the UE surface

Per the lookup-not-generation lock (cosmograph-pivot 2026-06-05): the engine runs offline and ships a JSON packet; UE consumes the packet at runtime. **"Fit Unreal's necessary inputs" is therefore a requirement on the export contract (star-lord's seam) — the thinnest layer in the system — and on nothing upstream of it.** The generation core and resolver do not bend to UE; the packet schema does. The packet schema is new code (non-kernel, § 2) and is authored greenfield-style against UE-side consumption requirements named by the PC seam (mantis/radagast via david-h). Schema changes are additive per Principle 6 cross-seam contract discipline.

## 8. Refutation clause — the door greenfield legitimately walks through

This contract's verdict basis measured throughput/cost. It did NOT measure design-architecture divergence. Accordingly:

1. **The gap-register architecture-fit audits** (rocket: generation seam; gamora: simulation seam; fired 2026-06-11) classify the synthesis § 9 register + cemented future-state fit as extends-cleanly / extends-with-friction / **fights-the-architecture**.
2. **If FIGHTS dominates a seam's classification,** WRAP is refuted FOR THAT SEAM'S AFFECTED MODULES — and the remedy is **module-targeted greenfield under oracle**: rebuild the offending module(s) one at a time, with the existing implementation kept alive as the golden-master oracle (new module must reproduce old outputs on the pinned corpus before it earns trust, then diverge only via § 3 math-notes). Never a big-bang rebuild.
3. **Vocabulary lock:** "rebuild" is reserved for module-targeted greenfield under oracle per this clause. Wrap-and-extend work is not called rebuild; big-bang engine replacement is not on the menu under any audit outcome — the audit can route *modules* to greenfield, not the validated kernels' behavior history.
4. **Standing re-evaluation:** any future cycle that finds itself writing adapter-on-adapter against a kernel interface (the calcified-wrap smell) files a framing-audit (Discipline #23) naming the friction and re-opens this clause for that module.

## 9. Work this contract governs (initial routing)

| Work item | Seam | Kernel-touching? |
|---|---|---|
| Thin parallel sim runner + surrogate-search/full-fidelity-gate pipeline | gamora | No — new code consuming declared resolver interface |
| Spatial recalibration math-note + golden-master (first § 3 application) | gamora | **Yes — protocol test case** |
| A3 population audit + PC parallel-factor measurement | gamora | No |
| Naming deferral behind sim gate + batched element-adaptation delta path + naming concurrency ~10 | rocket | No — orchestration over generation core |
| Cache-hygiene fix (process-stateful skill-id counters → 50% disk-cache miss) | rocket | **RECLASSIFIED per § 8.1 disposition 1** — not a patch; subsumed by the id-generation-substrate module-targeted greenfield under oracle |
| Rate-limit tier verification + cache-key hygiene + batching/model-tier options | star-lord | No — `llm/` infra |
| Export packet schema shaped to UE consumption | star-lord (+ PC seam consult) | No — § 7 surface |
| Gap-register audits → § 8 disposition | rocket + gamora | Read-only |

## 8.1 AMENDMENT 2026-06-11 — § 8 audit disposition (both audits returned same-session)

**Evidence:** `agentic_orchestration/gamora/notes/2026-06-11-gap-register-architecture-fit-audit-simulation.md` (commit `477dee3`) + `agentic_orchestration/rocket/notes/2026-06-11-gap-register-architecture-fit-audit-generation.md` (commit `8910168`).

**Simulation seam: WRAP-CONFIRMED.** 8 cleanly / 2 friction / 0 fights. Kernel boundary drawable TODAY at `fight_engine.simulate_fight(...) → FightResult` — pure function, zero telemetry/DB/LLM/HTTP coupling across all 7 kernel files; `batch_runner.run_batch` already wraps it. Doc-50 BVV targets + doc-47 two-layer T4 are already implemented (`bounded_viability_validation.py`, `gauntlet_sim.py`) — code and cemented architecture co-evolved; no design divergence.

**Generation seam: WRAP-WITH-TARGETED-REBUILDS.** 5 cleanly / 4 friction / 1 fights. Validated core (substrate-identity YAMLs, data-driven element pool, BC-target cell composition, confined downstream naming) is the exact shape the future-state assumes; primitives are accommodated as data. **The one FIGHTS item: the id-generation substrate** — seven process-stateful `global` ID counters (`_class_counter`, `_skill_counter`, `_gear_instance_counter`, `_monster_counter`, `_trial_counter`, …) make generated IDs a function of process invocation order, not content. Fights three cemented axes: delta-naming/cache reuse, the cosmograph stable-kit-id lookup contract, and variant-overlay lineage.

**Dispositions (binding):**
1. **Id-generation substrate → module-targeted greenfield under oracle** (§ 8.2 path): content-addressed deterministic ids, rebuilt as a module across the 7+ touchpoints, with the existing generators preserved and golden-master id-stability tests on the pinned corpus. § 9's cache-hygiene "boundary case" row is RECLASSIFIED to this disposition — it is not a patch.
2. **CELL_DEFS → pattern-library loader** named by rocket as the second targeted-rebuild candidate (Phase C consumption path); scope at rocket's seam discretion within § 8.2.
3. **Spatial damage surface precision flag (gamora):** two damage paths exist — `spatial_gauntlet/spatial_engine.py` (~L886) uses a simplified model (`damage_multiplier × 500.0 × damage_modifier`) bypassing `damage_resolver.resolve_skill`. Commit-grade fidelity currently runs a less-validated damage model than search-grade. Remedy decision folds into the spatial-recalibration math-note (§ 3 first application): (a) designate spatial damage its own kernel post-recalibration, or (b) re-point spatial at `resolve_skill`. **Gandalf design-lean: (b)** — commit-grade combat should run the most-validated damage math; gamora's math-note argues it with numbers. **RESOLVED → § 8.2: Matt authorized (b) same-session.**
4. **Conjunction re-open criterion (rocket-registered, standing):** if the id-substrate rebuild + race-family landing + pattern-library Phase C + cosmograph stable-ids all fire in one window, combined blast radius approaches a generation-spine rebuild — § 8 re-opens for the generation seam at that conjunction. Today each is bounded local work; do not pre-aggregate.
5. **Gap-register corrections:** entry #19 (`scope_preference`/`is_unique`) already landed in code (`partition_schema.py`, `gear_instance_generator.py`); entry #2 DDA scaffold cleanly module-isolated for Cycle-15 retirement. Synthesis § 9 register stands corrected by these audits as the more-current evidence.

**Net: the § 8 refutation clause is RESOLVED for this cycle.** Big-bang greenfield refuted on both measured axes (throughput 2026-06-10; design divergence 2026-06-11). The audit found the one place clean re-implementation genuinely beats extension — the id substrate — and routed it surgically.

## 8.2 AMENDMENT 2026-06-11 (second same-session) — spatial re-point authorized + cycling-cost-model clause + T4-native recompose requirement

**Authority:** Matt, this session ("fold the re-point into the recalibration math-note and proceed"), plus two Matt-surfaced gaps in the contract's cost model and lever vocabulary.

1. **Spatial damage remedy (b) AUTHORIZED.** Spatial commit-grade combat re-points at `damage_resolver.resolve_skill`; the simplified model (`damage_multiplier × 500.0 × damage_modifier`) is retired as commit-grade math. The re-point and the recalibration are **one work item, not two**: `SPATIAL_DAMAGE_SCALE=4.0` was calibrated against the simplified model, so re-pointing invalidates it by construction. The § 3 first-application math-note (gamora) carries both. Design rationale on record: the simplified model cannot express kernel mechanics (chaos_immune nullification, three-path `damage_scaling_type` routing, ±15% per-hit variance, buff interactions) — a DEFENSIVE_TRADEOFF kit gauntleted under it is graded on combat where its build-defining covenant does not exist.

2. **Cycling-cost-model clause (Matt-caught gap).** The § 4 sweep numbers (~0.7–3.5 h Mac / ~0.3–1.3 h PC) are **per-gauntlet-pass — the convergence-iteration multiplier is explicitly OUT OF MODEL** (gamora re-profile scaffold register S7). The contract now names the regimes:
   - **Filter regime** (one spatial pass per variant; architected generation + band selection): MEASURED — the § 4 numbers hold.
   - **Cycling regime** (per-kit recompose convergence): UNMEASURED at spatial fidelity. NOT authorized for production scheduling until modeled.
   - **Hybrid regime (contract intent):** all recompose cycling runs at **duel fidelity** (real `resolve_skill`, 1/11–1/53 spatial cost); spatial fires once per candidate at the commit gate plus re-gates on recomposed near-misses only. The math-note MUST model and bound the re-gate multiplier (failing-fraction × mean re-gates) before any production sweep is scheduled.
   - The PC 12× parallel factor remains ASSUMED (re-profile S4); the PC-side measurement rides with the math-note work before the combined Mac+PC number is banked.

3. **T4-native recompose-lever requirement (Matt directive).** Current recompose levers are flat (modifier nudge, list-based skill swap, 3 attempts/lever, ordered). The future T4 skill profile/process is chains-within-trees; recompose must become **structure-aware** (substitute along a chain, re-form a branch, respect prerequisite topology) or the balance loop will converge kits into formations the skill system cannot legally express — un-architecting what generation architected. Binding consequences: (a) the recompose-lever vocabulary is declared **T4-profile-native-pending**; the thin parallel runner's interfaces must not harden flat-lever assumptions; (b) the **full T4 skill-profile design is upstream of the cycling regime** (the filter regime is NOT gated on it).

## 10. Routing + sign-off

- **Gate-1 critique-pair review** → jack-ryan (process/technical stress-test of this contract).
- **Decisions-log entry** → jack-ryan (composes with the queued greenfield-verdict entry; one entry covering verdict + contract is acceptable at his discretion).
- **Audit results** → amend § 2/§ 8 dispositions in-place per § 0.1-style amendment record when rocket + gamora return.
- **KR** sequences the § 9 dispatches post-Gate-1.

**Author:** gandalf, 2026-06-11. This contract is the instrument that was missing at the first rebuild: the seams are named, so "what should change vs what should remain" is answered by construction. The second rebuild's ghost — the silently omitted battle simulator — is the first name on the kernel list.
