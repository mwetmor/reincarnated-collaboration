# D11 — Hybrid_mage tuning post-mortem (after empirical miss)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

> *[RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for retire verdict and rationale. See `reincarnated-engine/design/decisions/decisions-log.md` for the RETIRE entry.]*

**Authority:** Matt L3 2026-05-17 evening — Option B endorsed; gandalf post-mortem authorized as immediate companion to advisory.
**Author:** gandalf (story-and-design steward).
**Predecessor:** `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` (the pre-empirical design call) + `agentic_orchestration/dispatches/2026-05-17-rocket-d11-hybrid-mage-tuning-implementation-queued.md` § completion record (1/17 convergence; 6%).
**Type:** Pattern B short — post-mortem on my own advisory; cites Disciplines #1 + #11.
**Status:** Companion document. Does NOT supersede the advisory. Captures what the empirical data taught us between advisory completion and Option B authorization.

---

## § 0 — Verdict on Option B (the headline)

**Option B is IN BOUNDS. Fire it. But frame it correctly, or it will miss the same way α=0.07 missed.**

The composite α=0.08–0.09 + skill-count ceiling 12→10 is the right next move because:

1. It honors the original advisory's **composite-lever intent** (§ 4.4 of advisory — primary tax + secondary structural constraint).
2. It adds the genre-canonical capacity reduction that **Diablo Immortal (4-skill cap)** and **D4 (enchantment-slot opportunity cost)** both demonstrate works empirically as a breadth-tax in modern ARPGs.
3. It does NOT abandon the "comfortable mid-tier hybrid" thematic framing in advisory § 5 — a 1–2% α nudge plus a 12→10 skill count is *less harsh* than D2 Sorceress synergy differential (~40–50% damage delta), *less constraining* than Immortal's 4-skill cap, and *less identity-disrupting* than Option A's 15–20% damage tax.
4. It is the **smallest defensible disciplined increment** before Option D redesign — one-shot tuning is correct iterative-engineering discipline before committing to a multi-day redesign pass.

The decision is not stop or pause. It is fire with three load-bearing warnings (§ 3 below).

---

## § 1 — What the advisory predicted vs what shipped

### Advisory projection (pre-empirical)

From advisory § 4.6 — worked example calibration table:

> | 3 elements (general-D11 hybrid ceiling) | 0.93 (7% tax) | pre-modifier WR ≈ 0.95–0.97 from raw 1.000 | balance loop should find converged modifier ~0.06–0.10 (above floor) |

Translation: at α=0.07, the advisory projected 3-element hybrid_mage kits would land just above the modifier floor (0.05) — convergence rate not stated explicitly but the implied projection (gandalf + gamora cross-check) was **50–60% of hybrid_mage instances converging.**

### Empirical result (post-implementation)

From `output/standard-demo-regen-2026-05-17/d11_salvage_summary.json` (via rocket completion record):

- **1/17 hybrid_mage instances converged (6%)**
- WR at modifier floor: **0.56–0.84** (target ≤0.50; the floor is 0.05; the convergence band asks WR-at-floor ≤ 0.50 so the loop can find a non-floor modifier)
- α=0.07 → 7% damage tax produced **no measurable convergence shift** on 16 of 17 kits

### The miss is roughly an order of magnitude

The advisory projected ~50–60%; the engine delivered 6%. That is not a small miscalibration. That is **the wrong mental model for the convergence mechanism.**

---

## § 2 — The structural learning: I anchored on the wrong genre mechanic

This is the post-mortem's load-bearing observation. Document it; carry it forward to D11.2 if needed and to Phase-1 P2 hybrid-composer work.

### What I cited in the advisory

The advisory's calibration anchor (§ 2.2, Diablo II Sorceress) framed the breadth-tax as a **DPS-output differential**:

> The differential between specialist and split is roughly **40-50% of damage output**. This is the genre's empirical magnitude for "what does breadth cost in the most-studied multi-element ARPG class." My recommended α=0.07 quadratic on a 4-element kit produces a 28% tax — *less than* the D2 specialist-vs-split differential, which is the correct calibration.

This anchor was *correct as genre observation* but *incorrectly mapped to Reincarnated's balance loop.*

### What the engine actually does

Reincarnated's convergence test is **not a DPS race against an HP bar.** It is a **WR test against a gauntlet of 6 monsters with element-keyed resistances and a final modifier multiplier.** The hybrid_mage's structural advantage is **multi-element coverage immunity to resistance profiles** — each additional element opens new resistance-piercing combinations, and the advantage is **combinatorial, not additive in damage output.**

A 7% damage tax does almost nothing to a kit that wins because it has a 100% chance of having at least one element a monster is vulnerable to. The fight ends with hits-taken-by-player as the bottleneck, not hits-required-to-kill-monster. The damage tax addresses the wrong variable.

### The better genre analogue I undersold

Advisory § 2.6 (Path of Exile Elementalist) noted:

> **Resistance penalty** (every multi-element build runs against the cap-resistances-everywhere endgame requirement; specialists need only one elemental defense direction; hybrids need three)

This is the better analogue for Reincarnated. PoE's hybrid Elementalist pays for breadth by needing **wider defensive coverage** to survive longer fights, not by losing offensive DPS. The mechanism that closes the gauntlet-convergence gap in Reincarnated is the **same shape**: a hybrid_mage needs to either kill faster (DPS tax — what α tries to do) OR survive less well to take more hits (defensive tax — what would actually work).

I cited this in § 2.6 but did not promote it to the calibration anchor. The D2 Sorceress framing felt more vivid and more directly damage-tax-shaped, so it became the calibration story. The PoE framing is mechanically truer to what Reincarnated's balance loop measures.

### Discipline #1 (math-before-code) verdict

The advisory's math-before-code reasoning was **sound in narrative-canon terms but flawed in engine-mechanic terms.** I reasoned about damage output; the engine reasons about WR-at-floor against gauntlet resistance profiles. These are not the same calibration problem. The empirical miss is the lesson: **genre-canon analogies must map to the specific engine mechanism, not the broadly-similar player feel.**

### Discipline #11 (empirical inspection) verdict

The advisory recommended (§ 4.1 validation discipline) that gamora take a v1.5 hybrid_mage sample and run the tax through the balance loop empirically before committing. **Gamora did this in her D11 math note (§ 7.2 — "rough estimate")** and flagged it as a "rough estimate." Jack-ryan Gate 1 INFO-1 flagged that the projection was an estimate-on-estimate. **The empirical inspection discipline was correctly invoked — and the projection was correctly flagged as uncertain. The miss is on the design-side calibration anchor, not on the engineering-side discipline.**

This is important: the team did not fail iterative-engineering discipline. **I (gandalf) failed the genre-canon mapping.** That's a design-steward responsibility, captured here.

---

## § 3 — Three load-bearing warnings for Option B

### Warning 1 — Ceiling 12→10 is the PRIMARY lever in Option B, not α

The α=0.07→0.08–0.09 nudge is statistically negligible. Tax delta: 0.93 → 0.92 (α=0.08) or 0.91 (α=0.09). On a kit already winning 0.77 WR at floor, a 1–2% damage reduction will move WR by <0.02. The convergence target needs ≥0.27 of WR reduction (from 0.77 → 0.50). Even at α=0.09, the damage-tax math gives at most ~0.04 of WR motion.

**The skill-count ceiling 12→10 is what closes the gap.** A 16.7% reduction in kit density reduces:

- Total damage output (capacity-tax that scales with damage_per_skill × skill_count)
- Coverage breadth within the hybrid (10 skills across 3 elements = 3.3 skills/element vs 4 skills/element at 12)
- Ailment-application slots (fewer DoT/control hooks per kit)

This is the **Immortal pattern** (advisory § 2.5): "Skill-count cap *alone* is sufficient to discourage breadth *if the cap is tight enough*." Immortal's cap is 4; Reincarnated's was 12; 10 is the right next step.

**Action:** gamora's D11.1 math note and rocket's D11.1 implementation should **frame the ceiling change as the primary lever** and the α nudge as identity-flavor calibration. If they treat α as primary, they will over-tune α and miss again.

### Warning 2 — Time-box. If Option B misses, go to D11.2 — DO NOT chase α to 0.10/0.11/0.12

The math-before-code projection failure proves we don't yet understand the WR-vs-α curve well enough to predict it linearly. If Option B at α=0.08 + ceiling=10 misses, the answer is **not** α=0.10 then 0.11 then 0.12. That path is *more empirical guessing without a corrected model.*

The answer if Option B misses is **D11.2 redesign**, framed around the corrected mental model from § 2 above: the breadth-tax must address **resistance-coverage immunity**, not damage output. Concrete D11.2 candidate levers (deferred until needed):

- **Per-monster ailment-slot limit** (advisory § 2.7 — PoE pattern; one ailment per monster; multi-ailment kits compete for slot). This is the elegant breadth-tax that hits multi-element coverage directly.
- **Element-resistance penalty for the hybrid kit's own user** (PoE-shaped; the hybrid pays the cap-resistances-everywhere cost in a Reincarnated-shaped way; e.g., -10% to incoming damage resist per element beyond 2; survivability tax).
- **Coverage-bonus suppression** (engine-mechanic; if the kit's hits cover ≥3 elements during a fight, monster resistance becomes adaptive — the gauntlet detects the breadth and raises a resistance against the most-used element each round). This is the most engine-faithful — it makes breadth-immunity self-limiting.

**Acceptance gate for Option B:** ≥12/17 hybrid_mage convergence. Miss → D11.2 immediately, **not** α=0.10.

**Jack-ryan Gate 1 should hold this line.** The Gate 1 review on Option B's math note should explicitly require: "if this misses, escalation path is redesign, not further α tuning." Capture in dispatch acceptance criteria.

### Warning 3 — Capture the structural learning before D11.2

If Option B succeeds (target ≥12/17 hybrid_mage converged), the structural learning from § 2 still matters for **Phase-1 P2 hybrid-composer** work and any future hybrid_physical / hybrid_caster archetypes. The Phase-1 P2 work will inherit the tax mechanism; without correcting the mental model, the same calibration miss will repeat at scale.

**Action:** when Option B lands (pass or fail), this post-mortem doc is the artifact. Reference it in:

- `canonical/story/gandalf-phase2-bullet-points.md` § 1.4 (form-library / hybrid framing) — append a "lessons from D11" cross-reference
- Phase-1 P2 hybrid-composer dispatch (when authored) — required reading
- Decisions-log entry (Matt + jack-ryan + knight-rider authoring path) — capture the "resistance-coverage is the true mechanism" insight as a project-wide design principle

---

## § 4 — Option B reframed correctly for gamora + rocket

Strict implementation guidance, in tight form for the next dispatch:

### Primary lever (load-bearing)

- **`_ARCHETYPE_SKILL_CEILING["hybrid_mage"]` 12 → 10** (or wherever the kit-size constraint lives; likely `d10_kit_constraints.py` or `b6_kit_builder.py`)
- This is the **structural change** that closes the convergence gap
- Acceptance criteria for this lever alone: 3-element hybrid_mage kits should now have 3-4 skills per element (vs 4-5 before); coverage breadth tightens

### Secondary lever (identity-flavor calibration)

- **α: 0.07 → 0.08** (single-line config change in `config/_tax_config.yaml`)
- Pushes tax to 0.92× on 3-element kits (vs 0.93×)
- Cumulative effect with ceiling change: ~25% effective damage reduction on a 3-element 10-skill kit vs prior 3-element 12-skill kit
- Acceptance criteria: 3-element hybrid_mage converges above floor + FLOOR_EPSILON

### Salvage strategy

- Same as D11.1: post-process the 17 hybrid_mage instances in seasons 002011-015
- Apply both the ceiling reduction (drop lowest-priority 2 skills per kit via re-pruning, **not** re-LLM-naming) AND the new α
- Re-run balance loop; verify convergence
- $0 LLM cost (sim only; D10 + D11 pattern)

### Provenance

- Append `d11_2_post_process: True` to manifests
- Bump `schema_version` to v1.9 on manifest.json (NOT per-class — jack-ryan WARN-2 carry-forward)
- Add `skill_count_ceiling_applied: int` to provenance log on each hybrid_mage class

### Acceptance gate

- **Hard target: ≥12/17 hybrid_mage convergence (≥70% — the original D11 target)**
- **Soft target: 14-15/17 (matches non-hybrid archetypes)**
- **Miss → D11.2 redesign immediately. NOT further α escalation.**

### Time-box

- Phase A (rules in generation/) — same-day; ceiling change is 1-line; α change is 1-config-key
- Phase B (salvage 17 instances) — same-day; ~5 min sim
- Phase C (verify) — same-day; convergence delta reported

Total D11.1 should be **<1 day** of rocket work. If it spills longer, that's signal to pause and check the model.

---

## § 5 — Genre-canon reframing: what I'd write differently now

For the record, and for future reference when authoring multi-element/hybrid design advisories:

### What I'd keep from the advisory

- ARPG-canon survey of 13 titles (§ 2 of advisory): still correct as genre observation
- Identity decision: retain + reshape (§ 3): still correct — hybrid_mage as form-library capstone identity
- Thematic framing in canonical-7 substrate (§ 5): still correct — substrate-commitment-truth-telling is the right narrative shape
- D11 scope tight on hybrid_mage (§ 6): still correct — broader hybrid-family is downstream

### What I'd reframe

- **Calibration anchor (§ 4.6):** Switch from D2 Sorceress synergy-differential (~40-50% DPS) to **PoE Elementalist resistance-cap-coverage cost (~25-30% defensive opportunity cost translated to ~15-20% effective WR-at-floor shift)**. The PoE mapping is engine-faithful; the D2 mapping is feel-faithful but engine-inaccurate.
- **Tax shape (§ 4.1):** Keep quadratic in n_elements (still correct for combinatorial coverage advantage), but anchor magnitude against **WR-shift target**, not damage-multiplier target. The math note should compute α from "what tax produces what WR-shift at floor" empirically, not from "what tax matches D2 Sorceress synergy-differential."
- **Composite lever weighting (§ 4.4):** Promote the **ceiling/capacity reduction** to co-equal with the damage tax (or even primary), not "secondary." Capacity reduction acts on coverage; damage tax acts on DPS. For a coverage-immunity convergence problem, capacity reduction is the load-bearing lever.

### What this means for the form-library narrative

The thematic framing in advisory § 5 (canonical-7 substrate-commitment; form-library accumulation; Earth-Self diversity-via-grace) is **unchanged**. The narrative shape is correct — substrates respond honestly to forms that hold many commitments. The mechanical translation just needs to land on the right engine-mechanism (coverage tax, not DPS tax) for the narrative to feel true at convergence.

A chromatic_mage that has "fewer skills but each one matters more across many elements" feels narratively *truer* than "the same number of skills but each one hits 7% softer." The capacity-tax framing is also **better thematic ground**: the form-library integrator has *focused breadth* (10 skills, 3 elements) not *diffuse breadth* (12 skills, 3 elements with redundancy).

This is good news. The reframing makes the narrative *more* coherent, not less.

---

## § 6 — Open items / Phase-1 P2 implications

### Closes

- **L3 #42 (hybrid_mage retain-or-retire):** Already closed in the advisory as (iii) reshape; this post-mortem does NOT reopen that decision. The reshape is the right call; the mechanical tuning is what needed correction.

### Re-opens (low priority)

- **Optional rename `hybrid_mage` → `chromatic_mage`:** Advisory § 7 listed this as Matt's call. With the capacity-tax framing, the "focused breadth" identity is stronger and the rename has more thematic ground. Matt's call; not blocking; flag for downstream.

### New items (capture for downstream)

- **Phase-1 P2 hybrid-composer:** must inherit the capacity-tax + α-tax composite, not just the α-tax. The Phase-1 P2 design should treat **per-archetype skill-count ceiling** as a first-class composer parameter, not a fixed constant. (Currently `_ARCHETYPE_SKILL_CEILING` is implicit; promote to substrate-identity declaration field?)
- **Future hybrid archetypes (hybrid_physical, hybrid_caster):** when they appear, they inherit both levers automatically via the substrate-identity declaration framework. The α and ceiling per archetype become substrate-derivable.
- **Resistance-coverage adaptive monster rule (D11.2 fallback candidate):** if Option B misses, this is the lever to invoke. Captured here so the design conversation can move quickly if needed.
- **Per-monster ailment-slot limit (D12+ candidate):** the PoE-elegant breadth-tax (§ 2.7 of advisory). Worth a deferred discussion; orthogonal to D11.1 but complements the capacity-tax framing.

---

## § 7 — Handoffs

- **→ knight-rider:** D11.1 dispatch to author. Frame ceiling 12→10 as PRIMARY; α 0.07→0.08 as SECONDARY. Acceptance gate: ≥12/17. Miss → D11.2 redesign, not α escalation.
- **→ gamora:** D11.1 math note. Cap-and-tax composite. Empirical calibration: run the v1.5 Class C sample with ceiling=10 alone first to isolate the capacity-lever contribution; then with α=0.08 added to see composite effect. Surface both contributions in the math note.
- **→ rocket:** D11.1 implementation. ~half-day. Same salvage pattern as D11. Carry forward jack-ryan WARN-1/2/3 fixes (already in place).
- **→ jack-ryan:** Gate 1 on D11.1 math note. Hold the escalation line: if miss, redesign not α-chase. Capture in dispatch acceptance criteria.
- **→ drax:** No surface change required. Demo + loadout continue to consume D10-curated until D11.1 lands; on landing, in-place refresh (no new dispatch needed; pointer already at 002011-015).
- **→ star-lord:** MIGRATION.md v1.10 already documents the 3-column contract. D11.1 may add a 4th column for `skill_count_ceiling_applied` (provenance). Star-lord follow-on if so.

---

## § 8 — Footer

**Lessons captured:**

- Discipline #1 (math-before-code): the genre-canon analogy must map to the specific engine mechanism, not the broadly-similar player feel
- Discipline #11 (empirical inspection over assumption): the team did this correctly; the projection was correctly flagged as uncertain; the lesson is design-side, not engineering-side
- Discipline #13 (implicit-pillar drift): captured the cap-and-tax composite as the design pillar going forward; Phase-1 P2 inherits

**Tone for downstream:**

The advisory was not wrong about *what* hybrid_mage should be. It was wrong about *which lever moves the engine's specific convergence mechanism.* The reshape direction is unchanged. The mechanical translation is corrected here.

This is the kind of miss that happens once and informs everything downstream. The team's iterative discipline kept the miss to a half-day of sim cycles (rocket Phase A + B was clean and cheap). The cost of being wrong was low because the disciplines were working. The cost of the lesson is captured here.

**Fire Option B. Frame the ceiling as primary. Time-box. If it misses, go to D11.2 redesign — not α escalation.**

---

*Authored 2026-05-17 by gandalf as immediate companion to the D11 advisory. ~1 hour. Append completion record from knight-rider when D11.1 lands.*
