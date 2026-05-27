# Finding — 2026-05-27 — Cycle 13 SC-6 Gate-1 Critique

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (3 WARN, 4 INFO; 0 BLOCK)
**Target:** commit `3ced195`
**Developer:** gamora
**Principles applied:** Principles 1 / 3 / 4 / 5; Disciplines #1.2 / #11 / #18 / #19.1 / #23 / #26

---

## Verdict

**PASS-with-WARN.** Rocket WU-R1 / WU-R2 / WU-R3 dispatch authoring may proceed. Three WARN conditions (W1–W3) must be folded into downstream dispatch acceptance criteria before rocket fires; they are not blocking at Gate-1 but will BLOCK at Gate-2 if unaddressed.

---

## What I found — 7 critique dimensions

### Dimension 1 — Empirical validity (Discipline #11) — 0-encounter baseline

**Verdict: INFO.**

Empirical spot-check performed at three span-covering line numbers (283, 486, 643):

- Line 283: `SCENARIO_OPEN_ARENA = ArenaScenario(scenario_id="open_arena", ...)` — arena geometry + spawn archetype tags (`"swarmer"`); no BC-cell targeting; no L45-50+ mob stat anchoring. Confirmed shell.
- Line 486: `SCENARIO_MAGIC_PACK = ArenaScenario(scenario_id="magic_pack", ...)` — geometry + 4 spawns (`archetype_tag="caster"`, `"swarmer"`); WR contract per `gauntlet_archive.py` notation; no BC-cell targeting. Confirmed shell.
- Line 643: `SCENARIO_MINI_BOSS = ArenaScenario(scenario_id="mini_boss", ...)` — geometry + 3 spawns (`archetype_tag="boss"`, `"brute"`); soft/hard timeout; no BC-cell targeting. Confirmed shell.

Search for `reference_encounter`, `endgame_encounter`, `encounter_catalog`, `L45`, `BC_CELL` returned 0 results in `simulation/`. The 0-encounter baseline finding is empirically valid. The `archetype_tag` field carries only topology hints (`"swarmer"`, `"caster"`, `"brute"`, `"boss"`), not BC-cell identity. gamora's finding is confirmed.

Cite: Discipline #11 empirical inspection over assumption — satisfied.

---

### Dimension 2 — Coverage methodology (Discipline #18) — cell scoping vs BC-axis lock vs v1 22-cell scope

**Verdict: WARN (W1).**

**What exists:** gamora audited against the 5-tuple subspace from `v1-bc-target-intent-2026-05-24.md` Sketch A (range × tempo × amplitude × attribute × proxy-density) and correctly identified 25 enumerated rows. gamora acknowledges the doc's own "~22 distinct cells" language and handles the 3-cell delta cleanly (§ 2.2 post-script Dimension 2).

**The axis-framing tension:** the dispatch specifies critique against `qd-engine-bc-axes-lock-2026-05-20.md` 8-axis operational truth (68,040 cells), but the v1-bc-target-intent doc uses a 5-tuple subspace (324 cells; ~22 v1 cells). gamora explicitly names this mismatch at audit § 2.1 and makes a clean scope decision: "I map encounters against the 5-tuple cells used in the v1-bc-target-intent doc, which is the source document specified in the dispatch." This is the correct scoping choice — the 8-axis lock governs deferred-evaluation policy (proxy-light/heavy axis 2A per `qd-engine-bc-axes-lock-2026-05-20.md:§ 5`), not the coverage target itself.

**WARN condition:** the audit does not explicitly reconcile whether the 25-row enumeration vs "~22 distinct cells" delta originates from (a) proxy-density variants of the same 5-tuple base cell being counted separately, (b) contested-cell cross-attribute overlaps, or (c) a doc-level counting error. The v1-bc-target-intent doc's distribution summary (§ 1.2) says "none ~15 cells / light ~3 cells / heavy ~4 cells" = 22 base cells, which implies the 25-row enumeration counts proxy variants of the same base cell as separate rows (e.g., STR-light Ancestor-Warrior is base cell 5 of the melee cluster, a proxy-density variant of a melee-STR base). This reading makes the 22 vs 25 delta well-characterized, but it is not stated explicitly in the audit.

**W1 — folded into WU-R2 dispatch authoring:** WU-R2 (per-cell mob composition specs) must state explicitly whether cell identity is keyed on the 5-tuple (25 rows) or the 4-tuple base + proxy-density as a deferral discriminator (22 base cells, 18 non-deferred). This affects whether WU-R2 generates 18 encounter definitions or a different count.

Cite: Discipline #18 methodology-before-execution — methodology scoping decision made (5-tuple from v1-bc-target-intent; correct); the 22 vs 25 delta must be resolved in WU-R2 acceptance criteria.

---

### Dimension 3 — Recommendation completeness (Discipline #1.2) — per-encounter specification depth

**Verdict: WARN (W2).**

**What is present:** each of the 18 recommended encounters carries (a) target cell tuple, (b) archetype name, (c) recommended scenario shell, (d) mob composition intent string, (e) WR expectation range. This is solid structural coverage.

**What is missing:** per-encounter difficulty calibration intent is stated at a cohort level (§ 5.3: KPM ~75+, defensive uptime ≥80%, active resource management critical, full rotation depth) but is NOT cited to specific code line references per Discipline #1.2. The audit claims "endgame difficulty (L45-50+ per doc 41 § 3)" as the anchoring authority, and doc 41 § 3 does confirm these targets — but the critical mob-difficulty operationalization gap (identified in audit § 5.3 as "MOB_HP_DIFFICULTY_MULTIPLIER = 1.5 was NOT calibrated against L45-50+ endgame node") is raised as a second-order flag but is not cross-referenced to a specific code location for WU-R1 to target.

**W2 — folded into WU-R1 dispatch authoring:** WU-R1 acceptance criteria must include: (a) cite `arena.py` or `gauntlet_archive.py` line(s) where the current `1.5×` HP multiplier lives, and (b) define whether L45-50+ mob stats are a new multiplier against that constant, a new constant replacing it, or a new per-tier stat profile. Without this, WU-R1 may produce L45-50+ mob profiles that do not plug cleanly into the existing `build_reference_gauntlet()` path.

The 18-encounter recommendation list itself achieves adequate specification depth for gate-passing purposes — gamora correctly limits mob composition to composition intent (archetype + tier + element + WR expectation), leaving specific monster instance authoring to rocket's generation seam. This is the correct seam boundary.

Cite: Discipline #1.2 math-note implementation claims must cite code line references — WU-R1 must resolve this before rocket fires.

---

### Dimension 4 — Playability gate operationalization (Discipline #26) — 6 sub-gates per encounter

**Verdict: INFO.**

gamora's audit §4 assesses the 6 existing arena scenario shells against all 6 Discipline #26 sub-gates (KPM / rotation coherence / resource flow / defensive uptime / non-degenerate / cognitive load) and correctly defers per-encounter per-gate assessment to Wave 1 when encounter content arrives, because there is no content to assess. This is the right call — the audit cannot operationalize #26 against content that doesn't exist.

The audit establishes a threshold policy (§ 4, "THIN-COVERAGE with caveat" for 5/6 sub-gates) for application at Wave 1. This is implementation-ready and can be consumed directly by WU-R2 dispatch acceptance criteria.

The structural capability finding ("geometry shells are capable of exercising all 6 sub-gates IF mob content is properly calibrated") is sound and empirically grounded in the scenario designs verified at lines 283 / 486 / 643.

No finding beyond INFO. Cite: Discipline #26 — forward policy established; Gate-2 will verify at Wave 1 post-implementation.

---

### Dimension 5 — Proxy-deferred 7-cell boundary — alignment with canonical deferred-evaluation policy

**Verdict: INFO.**

gamora identifies 7 cells as proxy-deferred (§ 3): STR-light (1) + DEX-light (1) + DEX-heavy (1) + INT-heavy (2) + WIS-heavy (2) = 7. gamora cites `qd-engine-bc-axes-lock-2026-05-20.md:§ 5` as the deferral authority.

Empirical verification: `qd-engine-bc-axes-lock-2026-05-20.md:§ 5` confirms: "proxy-light and proxy-heavy bins route to deferred-evaluation pool until sim extension lands" and "Profile A excludes proxy-light + proxy-heavy from shippable seasons." The deferral is canonical policy, not gamora's editorial call. The 7-cell deferral is within gamora's seam authority and fully aligned with the locked deferred-evaluation policy.

The post-script Dimension 3 arithmetic is correct: 25 - 7 = 18 non-deferred cells.

WU-R4 (Cycle 14+ scope record) is the appropriate vehicle for the deferred cells. No escalation required.

No finding beyond INFO.

---

### Dimension 6 — Rocket consultation work-unit specifications — WU-R1/R2/R3/R4 readiness

**Verdict: WARN (W3).**

**WU-R1 (L45-50+ mob stat profile):** Substantively described (§ 6.1). The blocking claim is clear: current `1.5× HP multiplier` was not calibrated against L45-50+ node. WARN from Dimension 3 applies here — the WU-R1 dispatch must cite the specific code location of the current multiplier so rocket can target the correct intervention point. Otherwise WU-R1 risk: rocket authors L45-50+ stat profiles that are disconnected from the `build_reference_gauntlet()` selection path.

**WU-R2 (per-cell mob composition specs):** Well-scoped. 18 encounter definitions, 1 per non-deferred cell; format (mob tier + archetype + element + endgame calibration markers) is clear. WARN from Dimension 2 applies — cell identity key (5-tuple vs 4-tuple + proxy discriminator) must be explicit in dispatch.

**WU-R3 (archetype coverage for WR contract alignment):** Adequately described. The ask is: verify or create L45-50+ calibrated monster instances per `archetype_tag` in the bestiary. This is within rocket's generation seam and does not require additional specification depth at Gate-1.

**WU-R4 (proxy-deferred 7-cell record):** Well-scoped as a Cycle 14+ scope record. No additional specification needed.

**W3 — WU-R1 and WU-R2 require code-citation amendment before dispatch authoring:** Knight-rider must include in WU-R1 dispatch acceptance criteria: cite `arena.py` or `balance_loop.py` line for current mob HP multiplier and specify the implementation target (replace vs augment). Knight-rider must include in WU-R2 dispatch acceptance criteria: explicit statement of whether cell identity is keyed on 25-row 5-tuple or 18-cell non-deferred 4-tuple.

---

### Dimension 7 — Framing-audit per Discipline #23 (Pattern A-deep three-question protocol)

**Applied to audit's load-bearing claims.**

**Q1 — What would refute: if 18 encounters were too few/too many vs actual sim coverage need, what evidence would surface?**

The 18-encounter count is anchored to the GAP 2 LOCKED intent range (minimum 8-12 / optimal 15-22 / maximum ~30 per closeout § 5.1). The "too few" refutation would surface at Wave 1 sim execution if multiple cells fail to produce WR signals distinguishable from each other due to scenario shell re-use across multiple cells (e.g., 4 cells using `open_arena` may produce insufficient per-cell discrimination signal). The "too many" refutation is implausible given the pre-existence gap (0 → 18 is well within the locked range). The 18 count is defensible and within the framing authority.

**Q2 — Cheapest refuting test: how cheaply can the 0-encounter baseline be falsified?**

gamora cites the grep: `grep -n "^SCENARIO_"` returning 6 entries at the named lines. This is the cheapest refuting test (Discipline #19.1 — substrate count / coverage claim type; cheapest test = grep/search on production codebase). The secondary search for `reference_encounter`, `endgame_encounter` etc. is the cheapest systematic refutation. Both were performed. The baseline is properly falsified at minimum cost.

**Q3 — Alternative framing: is "encounter as unit" correct, or are encounters better understood as parameterized templates?**

This is a load-bearing framing question. gamora's audit treats "encounter as unit" — 1 encounter definition = (arena scenario + mob composition + BC-cell target + difficulty calibration intent). The alternative "encounters as parameterized templates" framing would mean authoring 6 scenario templates with parameterized mob composition, then binding BC-cell targets at sim-run time.

**Finding:** the "encounter as unit" framing is correct for the current sim architecture. `build_reference_gauntlet()` selects monster objects from the bestiary by tier + element diversity — it already treats the scenario shells as templates. What is missing is the BC-cell-targeted mob composition binding, which is what gamora's recommended 18 encounter definitions would provide. The audit's "encounter as unit" framing is the addition of the binding layer on top of the existing template infrastructure. The alternative framing is NOT better — it would still require 18 binding specifications; it would just call them "template parameters" rather than "encounter definitions." No framing amendment warranted.

Cite: Discipline #23 — three-question protocol applied; no framing amendment required; audit's load-bearing claims survive scrutiny.

---

### Cross-cohort coverage gate (closeout § 3.3 Principle 6 / C_archetype lock)

**Verdict: INFO.**

The audit's 18 recommended encounters implicitly cover the 4 C_archetype cohort identities (DPS-min-maxer / Balanced / Defensive / Hybrid) by distributing across all 4 attribute classes (STR / DEX / INT / WIS) and all WR contract tiers (0.30-0.80). The distribution is implicit rather than explicit — the audit does not cross-tabulate encounter recommendations against the 4 C_archetype identities from Block C Scaffold 2.

This was flagged in the dispatch as "INFO if implicit; WARN if missing." Because the coverage is structurally implicit (attribute × WR range jointly discriminate archetype cohort coverage at a coarse level), and because the C_archetype partition cycle is Wave 1 work per closeout § 3.3, this registers as INFO rather than WARN. Wave 1 partition cycle is the correct vehicle for explicit cohort-coverage verification, not this audit.

---

## Action items

### WARNs (fold into downstream dispatch authoring before rocket fires)

- [ ] **W1 (KR → WU-R2 dispatch):** State explicitly whether WU-R2 encounter definitions are keyed on 25-row 5-tuple enumeration or 18-cell non-deferred 4-tuple. Resolve the 22 vs 25 cell-count delta in WU-R2 acceptance criteria.
- [ ] **W2 (KR → WU-R1 dispatch):** Include in WU-R1 acceptance criteria: cite the specific `arena.py` or `balance_loop.py` line(s) for the current `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` and define the implementation form (new multiplier / new constant / new per-tier profile) rocket must produce.
- [ ] **W3 (KR → WU-R1 + WU-R2 dispatches):** Compose W1 + W2 into the respective dispatch acceptance criteria before KR fires rocket WU-R1 and WU-R2. WU-R3 and WU-R4 are ready to dispatch without amendment.

### INFOs (no action required; record for archaeology)

- [ ] The 6 arena scenario shells are geometry-sound and capable of exercising all 6 Discipline #26 sub-gates with appropriate mob content. Gate-2 verifies at Wave 1.
- [ ] The 7-cell proxy-deferred boundary is canonically grounded in the BC-axes-lock deferred-evaluation policy. WU-R4 records for Cycle 14+.
- [ ] The C_archetype cohort coverage is implicit in the attribute × WR distribution. Explicit verification deferred to Wave 1 partition cycle per closeout § 3.3.
- [ ] The "encounter as unit" framing survives the Discipline #23 three-question audit. No amendment warranted.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md` — audit reviewed
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` — lines 283 / 486 / 643 spot-checked (Discipline #11)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/v1-bc-target-intent-2026-05-24.md` — § 1.1 / § 1.2 (Sketch A cell enumeration vs distribution summary)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — § 5 proxy-deferred-evaluation policy
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — § 4 Block C / § 5 GAP 2 lock / § 5.1 encounter count range
- `/Users/admin/Games/reincarnated-collaboration/canonical/41-progression-framework-2026-05-27.md` — § 3 node identity mapping / endgame L45-50+ definition
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1.2 / #11 / #18 / #19.1 / #23 / #26

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**Gate-1 verdict:** PASS-with-WARN
**Tag intent:** `jack-ryan(gate-1): PASS-with-WARN — Cycle 13 SC-6 reference encounter audit critique`
