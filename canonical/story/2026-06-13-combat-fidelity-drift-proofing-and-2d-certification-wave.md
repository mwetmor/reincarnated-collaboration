# Combat-Fidelity Drift-Proofing + 2D Certification Wave

> **STATUS:** CURRENT (load-bearing as of 2026-06-13) — see `canonical/00-ground-state.md`

**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design-spec-as-architecture; Matt-authorized for authoring 2026-06-13 ("yes please, and then the golden oracle for 2D")
**Authority:** Matt 2026-06-13 — authored from the Pattern-B combat-sim-architecture dialogue (this session); the *architectural change it describes* (1D deletion) is gated on the empirical trigger in § 4.3, NOT committed by this doc's existence.
**Companion docs:**
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` — § 5 combat-fidelity lock (this doc operationalizes § 5 as a *type*, not a sentence); § 2 kernel-freeze; § 8 refutation clause
- `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — the acceptance content the cert wave (§ 5) gates against; sibling deliverable
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the 8-axis definitions (preserved) whose *measurement fidelity* is re-stamped here (§ 3.2)

---

## 0. TL;DR

1. **The trap being closed is recombination-drift, not combat-fidelity.** In a 14-agent system that recombines canonical docs, a *rule in a doc* ("the duel is never balance-authoritative," contract § 5) is the weakest possible control — it is made of the same material as the failure. Proof: the rule's own author drifted off it inside two days (the defensive-bridge acceptance gate was a 1D-duel measurement). You cannot discipline a doc-recombination problem with another doc.
2. **The exact mechanism is a type-collision.** `bc_measured_bins.json` — the 8-axis *behavioral-identity* record (the lock, the orphan inventory, the defensive bridge) — is fed by the **1D** `simulate_fight(measure_bc=True)`. The **spatial** `GauntletArchive.insert()` (the only insertion chokepoint, verified at `gauntlet_archive.py:208`) uses a *placeholder* cell (`swarm_open_arena_{id}`) and never computes the 8-tuple. So the identity authority is 1D-fed and **commit-grade BC does not exist yet.** An agent reading {1D produces a behavioral record} + {the lock blesses the 8 axes} pairs them into {1D measurement = kit identity} — exactly the § 5 violation.
3. **The fix is a structural control at the chokepoint, applied in two acts:**
   - **TODAY — eliminate the attractor (§ 3):** type-wall the single archive chokepoint so behavioral identity can only be minted by the spatial path (`CommitGradeVerdict` vs `SearchGradeEstimate`); fidelity-stamp every 1D-measured artifact; rename `fight_engine` → `search_estimator`. This ends the recombination *the moment it lands*, regardless of how many stale docs exist or get written — the chokepoint does not care how many blessing-docs there are; it rejects the *type*.
   - **AT THE TRIGGER — eliminate the existence (§ 4):** delete the 1D engine as the **final gated item of the 2D-certification wave**, bundled so 2D is not certified until 1D is gone. Empirical trigger: golden-master pass (§ companion doc) + throughput proof.
4. **1D dies in every branch (§ 4.2),** so this is not a reprieve for 1D. The only refinement over "delete it now" is *sequencing* — deleting before 2D is proven would strand the pipeline with **zero working combat engines** (2D has never produced a successful run), which is a new way to lose weeks, not an escape from the trap.

---

## 1. The trap being closed

Matt's framing, verbatim in substance: *"Unless we delete the 1D engine, we risk wasting weeks or months AGAIN as our large team of agents picks up on an old canonical document and pairs them together in just the wrong way."*

This is correct and it is the dominant constraint — over combat fidelity, over throughput, over everything. The deployment environment is not a single careful operator who remembers § 5. It is a **14-agent recombination machine** that pairs canonical docs together, and any latent capability that *can* be misused *will* be, on a cycle count measured in weeks. The empirical base rate is now known: the steward who authored § 5 violated it in two days. A fence that the fence-builder climbs in two days is decorative.

The control that failed (§ 5, a sentence in a doc) failed for a structural reason: **it is the same medium as the failure.** Docs are exactly what the agents recombine wrongly. You cannot constrain a doc-recombination hazard with another doc — you can only move the constraint into a medium the agents *cannot* recombine around: a **type**, enforced at a **chokepoint**.

### 1.1 The mechanism, precisely (verified in-engine 2026-06-13)

| Artifact | Fed by | Carries | Today's authority |
|---|---|---|---|
| `bc_measured_bins.json` | **1D** `simulate_fight(measure_bc=True)` via `run_bc_measurement_over_corpus` | the 8-axis behavioral identity (Axis-1…5) — the lock's characterization | **de-facto identity-authoritative** (the lock, orphan inventory, defensive bridge all read it) |
| spatial `GauntletArchive` | **2D** `run_spatial_fight` via `_run_spatial_slot` | per-tier win-rate; `bc_cell` is a **placeholder** string (`swarm_open_arena_{id}`), not the 8-tuple | swarm-only, no 8-axis identity |

The drift is the diagonal: the **identity** lives in the 1D-fed file; the **commit-grade engine** computes no identity. § 5 says the 1D figure is "never balance-authoritative," but nothing *structural* stops an agent from treating it as identity — and the file is literally named `bc_measured_bins`, which *invites* the reading.

---

## 2. Control hierarchy — why type beats doc

Standard safety engineering ranks controls: **elimination > substitution > engineering controls > administrative controls > PPE.** § 5 is an *administrative control* (a rule humans/agents must remember). Matt is reaching for *elimination*, the top tier, and he is right that it is the strongest. This doc places the control at two tiers at once:

- **Engineering control (TODAY):** the type-wall makes the misuse *throw* rather than *silently mis-pair*. An agent that feeds a 1D result into the identity authority gets a **type error at the chokepoint**, not a subtly-wrong architecture three weeks later.
- **Elimination (AT THE TRIGGER):** the 1D engine ceases to exist once its replacement is proven.

The reason both, and in this order: elimination *now* is impossible without stranding the pipeline (§ 4). The engineering control *now* ends the trap immediately while the contained primitive lives out its last wave.

---

## 3. TODAY — eliminate the attractor

These three moves fire immediately on Matt's go. They do **not** depend on 2D succeeding; they close the recombination on the current codebase. Owners are the seam specialists; this doc is the design spec they execute.

### 3.1 Type-wall the chokepoint (gamora + star-lord)

**Intent:** behavioral identity may be minted **only** by the commit-grade (spatial) path. The 1D path may produce a *search-grade estimate* that is structurally un-feedable to the identity authority.

**Mechanism (design intent; gamora owns the simulation-side type, star-lord the export-side type):**

- Introduce two distinct types at the measurement boundary:
  - `CommitGradeVerdict` — minted **only** by the spatial path (the function that runs `run_spatial_fight` across the certified scenario set and computes the 8-axis bin from *spatial* telemetry). Carries a non-forgeable provenance marker (e.g., `fidelity="commit"`, `engine="spatial"`, scenario-set hash).
  - `SearchGradeEstimate` — minted by the 1D `search_estimator` (renamed `fight_engine`, § 3.3). Carries `fidelity="search"`.
- The **identity-authority consumer** — whatever decides a kit's behavioral cell / culls behavioral duplicates (today the MAP-Elites BC archive; the spatial `GauntletArchive.insert()` once it computes the real 8-tuple) — accepts **only** `CommitGradeVerdict` in its insert signature. Feeding a `SearchGradeEstimate` is a **type error**, not a runtime mis-pairing.
- `bc_measured_bins.json` as emitted from the 1D path is re-typed/renamed to advertise search-grade (`bc_search_estimate_bins.json` or an in-file `fidelity: "search"` field that the consumer asserts on). The commit-grade BC file is a *different* artifact minted by the spatial path.

**Why the chokepoint is guaranteeable:** there is exactly **one** archive insertion method (`GauntletArchive.insert(entry: GauntletArchiveEntry)`, verified). You do not have to find every stale blessing-doc — an impossible task in a 14-agent system, which is Matt's whole point. You guard the **one** door the identity must pass through, and the type makes the guard un-bypassable. A stale doc that *says* "use the 1D number" cannot make the 1D number *type-check* at the insert.

**Acceptance:** a deliberate test that constructs a `SearchGradeEstimate` and attempts `GauntletArchive.insert()` (or the BC-identity insert) **fails to compile / raises at the boundary**. jack-ryan gates this test exists and passes.

### 3.2 Fidelity-stamp the 1D-measured artifacts (gandalf + jack-ryan)

The 8-axis *definitions* in the lock are good and stay. What gets stamped is the *measurement fidelity* of everything produced against the 1D engine. Each of the following receives an explicit **`SEARCH-GRADE — commit-grade re-validation pending`** stamp (NOT a HISTORICAL demotion — the work is valid as discovery, pending certification):

| Artifact | Stamp |
|---|---|
| `bc_measured_bins.json` (1D run, season `kse_20260613_002`) | search-grade; superseded by spatial commit-grade BC once it exists |
| `qd-engine-bc-axes-lock-2026-05-20.md` | axes **definitions** CURRENT; add fidelity note: "measured-bin assignments are commit-grade in 2D; any 1D `bc_measured_bins` figures are search-grade scaffolding" |
| BC orphan-lever inventory + sizing ruling (2026-06-13) | search-grade-valid; the defensive bridge's 25/22/23/26 is a **search-grade** result on the 1D boss-duel panel |
| BC Bucket-B unaxised rulings (2026-06-13) | conclusion (zero new axes) holds; the measurement premise is search-grade |

This is surgical: it preserves the design reasoning (which is sound) and marks only the fidelity claim (which was over-stated). The type-wall (§ 3.1) makes the stamp *structural* rather than advisory — even an agent who never reads the stamp hits the type error.

### 3.3 Rename `fight_engine` → `search_estimator` (gamora)

The word "fight engine" *invites* an agent to read its output as the fight. Nothing fights in it — it estimates. Rename the module and its public entry (`simulate_fight` → `estimate_search_grade` or equivalent) so the *name* strips the affordance. This is vocabulary-as-control: half the recombination risk is the noun.

---

## 4. AT THE TRIGGER — eliminate the existence

### 4.1 1D deletion is the final gated item of the 2D-certification wave

The 1D engine's *code* is deleted as the **last step of the wave that certifies 2D** — bundled so the two cannot decouple. The failure mode of "delete at trigger" is that the trigger orphans and 1D lives forever; bundling defeats that: **2D is not declared certified until 1D is deleted and its callsites are gone.** jack-ryan gates that the deletion actually happened as a wave-exit criterion.

### 4.2 1D dies in every branch (this is not a reprieve)

The sequencing is the *only* refinement over "delete now." 1D's destination is deletion regardless of how the throughput question resolves:

- **If 2D throughput is affordable for the commit-grade batch** (§ 4.3 measures this): 1D has zero remaining function. Delete it.
- **If 2D throughput is NOT affordable** and the recompose inner loop needs a cheap evaluator: the cheap evaluator is built as a **spatially-aware reduced mode** (fewer ticks / fewer entities / same geometry), **not** the range-scalar 1D engine — because (per this session's Scenario-3 / C1 analysis) 1D hill-climbing biases every kit toward single-target optima during convergence. A cheap evaluator that lies about AOE is poison even as a non-gating substrate.

There is **no branch** where the range-scalar 1D engine survives. The architecture's destination is single-engine.

### 4.3 The empirical trigger

Deletion fires when **both** resolve:

1. **Golden-master pass** — the spatial engine reproduces the hand-authored known-correct results across the certified scenario set (companion doc `2026-06-13-2d-spatial-golden-oracle-spec.md`). This is the milestone that **has never happened** — 2D has never produced a single successful, ground-truthed run.
2. **Throughput proof** — gamora bounds the commit-grade per-candidate fight budget against the measured datum (`~5 hrs / 30 kits` full gauntlet; `GAUNTLET_COMPUTE_BUDGET_MAX_FIGHTS = 104,000`). The number that must be proven: the commit-grade pass over the season's surviving-candidate set fits a tolerable wall-clock. (This datum already *confirms* the inner loop cannot be 2D — hence a non-gating search substrate survives per § 4.2 — and makes the commit-grade-of-survivors cost *boundable*, not speculative.)

Recognition → validate → commit: the **recognition** is committed now (this doc). The **validation** is the trigger above. The **commit** (1D deletion) fires only when validation resolves. No time-passage gate — empirical only.

---

## 5. The 2D-certification wave (structure)

The wave that the deletion rides. Phases sequence; owners in brackets; jack-ryan gates each phase exit.

| Phase | Work | Owner | Exit gate |
|---|---|---|---|
| **W-A** | Author the golden oracle (the known-correct scenarios + reference kits + tolerances) | gandalf (design authority) | companion doc ratified; reference-kit expected results pinned |
| **W-B** | Type-wall + fidelity-stamp + rename (§ 3, the TODAY moves) | gamora + star-lord + gandalf | § 3.1 type-error test passes |
| **W-C** | Bring the spatial engine to **first successful run** against the golden master, module-by-module (keep what passes the golden master, rebuild only modules that fail it — the golden master votes, no ideological keep-vs-rewrite) | gamora | each of the 6 scenarios reproduces its golden result within tolerance |
| **W-D** | Wire **commit-grade BC**: compute the 8-axis bin from *spatial* telemetry, replacing the placeholder `bc_cell`; mint `CommitGradeVerdict` | gamora + star-lord | spatial path emits the 8-tuple; identity authority consumes only commit-grade |
| **W-E** | Throughput proof (§ 4.3 #2) | gamora | commit-grade batch cost bounded + tolerable |
| **W-F** | **Delete the 1D engine + callsites; re-validate the defensive bridge commit-grade in the boss room** | gamora | 1D gone (jack-ryan verifies); bridge's tank/mitigator/dodger/glass separation holds in `boss_with_adds` at commit-grade |

**W-C is the validate-then-extend core.** It is neither greenfield (don't re-render the captured requirements: 6 scenarios, arena physics, AOE taxonomy, aggro/leash — re-rendering is the silent-omission mechanism that deleted the battle simulator last cycle) nor naive wrap-and-trust (you cannot freeze-and-build on an oracle never seen to be correct). The golden master resolves keep-vs-rewrite **per module, by evidence**, which is the substrate-led discipline applied to the engine itself.

---

## 6. Out of scope — what this doc does NOT do

- **Does not re-render the 6 scenarios.** They exist (`arena.py`); they are captured requirements. The golden oracle *certifies* them; it does not rebuild them.
- **Does not touch the frozen kernel.** `damage_resolver.resolve_skill` is the shared, frozen, gamora-owned resolver both engines already call (post-2026-06-11 repoint). The type-wall and the cert wave are *above* the kernel; the resolver math is untouched (contract § 2).
- **Does not delete 1D before W-F.** Immediate deletion strands the pipeline with zero engines. The TODAY moves (§ 3) end the *trap*; W-F ends the *existence*.
- **Does not re-open greenfield-vs-brownfield as a strategic choice.** That dichotomy is the wrong axis for an unvalidated-but-built artifact (§ 5 W-C). The axis is unvalidated→validated.

---

## 7. Cross-references

- Forward-architecture contract § 5 (fidelity lock), § 2 (kernel-freeze), § 8 (refutation clause): `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md`
- Golden oracle (companion; the acceptance content): `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`
- BC axes lock (fidelity-stamped, § 3.2): `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Verified code anchors (2026-06-13): `GauntletArchive.insert` (`spatial_gauntlet/gauntlet_archive.py:208`); 1D BC feed (`bc_measurement.py` `run_bc_measurement_over_corpus` → `simulate_fight(measure_bc=True)`); placeholder cell (`balance_loop.py:2827`); KPM bands (`gauntlet_sim.py:206-311`); throughput (`gauntlet_sim.py:318-322`)
- ground-state oracle registration: `canonical/00-ground-state.md` § 1 (this doc + the companion added as CURRENT)

---

**Signed:** gandalf, 2026-06-13
**For:** closing the recombination-drift trap structurally — a type-wall at the single archive chokepoint (TODAY) so 1D-measured numbers cannot mint behavioral identity, plus 1D-engine deletion bundled as the final gated item of the 2D-certification wave (AT THE TRIGGER: golden-master pass + throughput proof). Operationalizes contract § 5 as a type rather than a sentence, because in a 14-agent doc-recombination environment a sentence is the weakest control and a type at the chokepoint is the strongest guaranteeable one.
