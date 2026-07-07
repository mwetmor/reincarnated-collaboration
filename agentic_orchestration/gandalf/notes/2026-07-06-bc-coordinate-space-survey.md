# BC coordinate-space survey — axis inventory · lattice arithmetic · the 18-vs-25 Gate-1 rider

> **Trigger:** Matt Q (2026-07-06, batch-2 session): *"Is the engine currently missing this entire BC Axis? If so, how many other substrates and axes are missing? How many total of the 64,000 BC coordinates do we currently have represented?"*
> **Method:** Explore-agent engine read + gandalf spot-verification (composer axis block read directly; sampler cell_id count grepped; 64,000 grep = zero hits in src/ + design/). Survey-mode: what-IS first, gaps second.
> **Author:** gandalf (ARCHITECT), 2026-07-06.

---

## 1. What IS — the coordinate system (verified against `bc_target_composer.py:71-99`)

**BcTarget = 8-tuple** `(eng, geo, proxy, ctrl, tempo, var, def, econ)`:

| # | Axis | Bins | Live | Gated | Cite |
|---|---|---|---|---|---|
| 1 | Engagement | close/mid/ranged × fast/slow | 6 | 0 | :75 |
| 2 | Geometry | single-target, small-AOE, large-AOE, chain, multi-spawn | 5 | 0 | :77 |
| 2A | Proxy density | solo · ~~proxy-light · proxy-heavy~~ | 1 | 2 (`_DEFERRED_PROXY_BINS` :97, "solo-only Profile A") | :79 |
| 2B | Control density | damage-pure, mixed, control-pure | 3 | 0 | :81 |
| 3A | Damage tempo | low, medium, high | 3 | 0 | :83 |
| 3B | Damage variance | flat, variable, spiky | 3 | 0 | :85 |
| 4 | Defensive profile | tank, mitigator, dodger, glass (`_DEFERRED_DEF_SUBCASES` = ∅; evasion-dodger ACTIVE) | 4 | 0 | :87, :99 |
| 5 | **Resource economy** | starved, overflow, generator-spender, steady · ~~HP-economy · charge-stack · damage-taken-converts~~ | 4 | 3 (`_DEFERRED_ECON_BINS` :95; HP-economy HARD-INFEASIBLE, LC-030 "zero HP-cost mechanics in pool" ~:326-331) | :89-92 |

**Lattice arithmetic (gandalf-recomputed):** live = 6×5×1×3×3×3×4×4 = **12,960** · fully un-gated = 6×5×3×3×3×3×4×7 = **68,040** · gated fraction = 55,080 (81%).

**Resource substrates LIVE beyond mana:** rage, combo, focus, stamina-as-resource are active cost-types (`resolve_cost_type()` ~:244-272). The martial economies exist; the absence is specifically the three exotic STRUCTURAL types.

**Leg-A state (found landed):** `resource_economy` dict emit-side LANDED (rocket, Route B — `generation/resource_economy.py:50` defaults, `:124` sampler; MIGRATION 2026-07-06): cost_scale, cost_slope{flat,escalating}, regen_shape{flat,on_kill,ramping}+magnitude/frac/ramp, cadence_scale. Sim-consume half = gamora, pending. Mana-default chassis only; the 3 structural bins not fired — consistent with the same-day Axis-5 ruling (batch-2 spec §8 R1).

**Variation axes (pilot-confirmed, distinct layer from BC axes):** T4 per-sample (~8-12/kit), role-split templates (5), element per-sample (8); geometry jitter excluded from pilot by design. Proxy lives at the composition layer today (`PROXY_COMPOSITION_WEIGHT_MULT = 0.25`, `bc_target_cell_sampler.py:492`), not as BC-cell bins.

**Cell granularities — THREE, not one:**
1. **8-axis lattice:** 12,960 live coordinates (descriptive space).
2. **Sampler curated roster:** **25 active cells** (`bc_target_cell_sampler.py` cell_id 1..25; v1 was 22) — verified by direct grep.
3. **Ruled batch-2 partition: 18 cells** — spec-level (faction stack / one-realm), **NOT yet an enumerated subset in code.**

## 2. The 64,000 figure — no derivation exists

Grep of src/ + design/ = zero hits. No axis-cardinality product equals 64,000. Nearest true number: **68,040** (full un-gated lattice) — 64,000 ÷ 68,040 ≈ 0.94. Disposition: treat **68,040 as the number of record** for the full lattice, 12,960 for the live lattice; retire 64,000.

## 3. Coverage — what's represented

- **Cell granularity (the meaningful one):** batch-1 = 700 gauntlet-passed kits over **7 martial cells**; all INT/caster cells at 0 (pilot chain addressing). Against the ruled partition: **7/18**.
- **Lattice granularity:** ≤700/12,960 (≤5.4%) and materially fewer distinct (batch-1 reskin-degenerate). Exact distinct-coordinate count IS parseable (per-kit BC-target arrays exist in `output/d5-reference-kit-coverage-*.json`) — elrond/star-lord query on request, not fired.
- **Frame (design law, substrate-led):** the lattice is **descriptive, not a quota.** The plan tiles the 18-cell partition at ≥100/cell; variation + economy axes provide within-cell spread; the population votes on which fine coordinates are viable and many lattice points are legitimately empty (infeasible combos — the composer's `check_infeasibility()` already says so). Treating 68,040 as a production target would be a category error.

## 4. THE ACTIONABLE RIDER — 18-vs-25 enumeration pin (rides Leg-A Gate-1)

The ruled "full fresh 18-cell emission" (batch-2 spec §4) has **no code-level cell enumeration yet**: the sampler's active roster is 25 cells. Before Leg C fires, rocket pins WHICH cells constitute the ruled 18 (and the 25→18 mapping rationale: merged? retired? Profile-A-infeasible?). **Not a Leg-B blocker** — the pilot names its 2-3 cells explicitly. Paste-ready for the AV2 session:

> **Gate-1 rider (gandalf, `agentic_orchestration/gandalf/notes/2026-07-06-bc-coordinate-space-survey.md`):** the ruled 18-cell partition is not yet an enumerated subset in code — `bc_target_cell_sampler.py` active roster = 25 cells. At Leg-A Gate-1, rocket pins the 18-cell enumeration (which sampler cells = the ruled partition, and why the other 7 are out) so Leg C's "full fresh 18-cell emission" has a code-level definition. Leg B unaffected.

## 5. Ruling-closure observation (registry honesty, guard 1)

The composer **already registers** the three structural bins as deferred (`_DEFERRED_ECON_BINS`) with HP-economy hard-infeasible citing LC-030. Under build-to-spec discipline (OP §3.7) a bare "deferred" flag is a gap-to-close; **the 2026-07-06 Axis-5 ruling converts these from drift-suspect deferrals into RULED reserved bins** (`reserved, empty-by-ruling`, batch-2 spec §8 R1 + derivation-stack F5 re-entry). The code flag and the canon row now agree — the un-drift is the point.

---

**Signed:** gandalf, 2026-07-06 (ARCHITECT). The lattice describes; the partition prescribes; the population votes.
