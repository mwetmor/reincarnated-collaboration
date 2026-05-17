# 2026-05-17 — gamora — D11.1 ceiling-primary tuning math note (composite lever recalibration)

**Authority:** Matt L3 2026-05-17 evening + Gandalf post-mortem ENDORSE with 3 load-bearing warnings. Option B selected: α=0.07→0.08 (identity-flavor nudge) + skill-count ceiling 12→10 (**PRIMARY structural lever**).
**Type:** Pattern B — gen-math + balance-loop math note recalibration; ~0.5-1 day (smaller than original D11 note; lever delta only).
**Predecessor:** Gandalf D11 post-mortem (`canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md` or wherever he authored it; per dispatch path `2026-05-17-gandalf-d11-postmortem-option-b-veto-authority.md`).

---

## ⚠️ THREE LOAD-BEARING WARNINGS FROM GANDALF (CONSUME BEFORE WRITING)

These supersede the original D11 math note framing where they conflict. Reference: gandalf post-mortem completion verdict.

### WARN 1 — Ceiling 12→10 is PRIMARY; α=0.07→0.08 is IDENTITY-FLAVOR

The empirical miss in v1.13 told us α=0.07 produced Δtax≈7% at n=3, insufficient to bring WR=0.56-0.84 to ≤0.50. Bumping α to 0.08 produces Δtax≈8% at n=3 — **statistically negligible 1-2% delta over v1.13**. α IS NOT the convergence lever in D11.1.

**The convergence lever is the skill-count ceiling 12→10.** This is the Immortal-pattern (4-skill cap as primary breadth-tax) at a softer ratio. -16.7% kit capacity directly reduces resistance-immunity-coverage at the structural source. Your math note must frame the ceiling change as the structural move; the α bump is calibration noise that preserves identity-flavor continuity with v1.13.

**Wrong framing (DO NOT use):** "α=0.08 + ceiling reduction as secondary safety net."
**Correct framing (USE):** "Ceiling 12→10 as primary convergence lever (Immortal-pattern breadth-tax); α nudge to 0.08 as identity-flavor calibration preserving comfortable-mid-tier feel from v1.13."

If rocket/gamora reads this wrong, the D11.1 outcome will be α-tuning chasing convergence and missing. Frame the ceiling as the load-bearer.

### WARN 2 — Time-box: if D11.1 misses, go to D11.2, NOT α-escalation

D11.1 acceptance gate: **≥12/17 hybrid_mage converged at α=0.08, ceiling=10.**

If MISS:
- **DO NOT** escalate α to 0.10, 0.11, 0.12 chasing convergence
- **DO NOT** lower ceiling further (12→9, 12→8) without explicit Matt L3 + gandalf redesign authorization
- **ESCALATE** to D11.2 redesign

D11.2 will be a structural rework framed around **gauntlet resistance-immunity-coverage** as the real convergence mechanism (see WARN 3). Time-boxing here prevents another iteration of "implement → miss → α-chase → miss."

Jack-ryan Gate 1 advisory (queued for your math note) is instructed to HOLD THIS LINE. If you propose α>0.08 OR ceiling<10 in your math note, jack-ryan will pre-flag REQUEST AMENDMENT.

### WARN 3 — Structural learning: gauntlet resistance-immunity-coverage is the real mechanism

Your original D11 math note translated gandalf's α=0.07 advisory grounded in the D2 Sorceress specialist-vs-split DPS-output differential. Empirical reality refuted that anchor: the actual mechanism driving hybrid_mage WR-at-floor pinning is **quadratic resistance-immunity-coverage** (more elements = orthogonal coverage of more gauntlet resistance profiles), NOT DPS magnitude.

Implication for D11.1 math:
- Damage tax α is ORTHOGONAL to coverage; it can scale damage but cannot fix coverage immunity
- Coverage is reduced by limiting skill count (fewer slots → fewer element representations) or by limiting element-breadth (already 4→3 in v1.13)
- The ceiling 12→10 attacks coverage directly; α attacks magnitude

Document this in your D11.1 math note § 1 (Gandalf advisory translation):
- Acknowledge the D2-DPS-race anchor failure from v1.13
- Frame the new mechanism understanding: gauntlet resistance-immunity-coverage
- Use this framing throughout the math note (especially § 7 convergence projection — base projection on coverage-reduction math, NOT pure-damage math)

Gandalf flagged that a canonical/story/ note on this structural learning is worth authoring AFTER D11.1 lands (so the lesson is captured regardless of D11.1 outcome). Knight-rider may queue that as a separate gandalf dispatch.

---

## Why this matters

D11 v1.13 implemented gandalf's original composite lever (α=0.07 + element-breadth 4→3) cleanly. Empirical result: 1/17 hybrid_mage converged (6% vs ≥12/17 target). Gandalf post-mortem ENDORSE-with-warnings: Option B is the right move; misframe risk is large.

This dispatch authors D11.1 math note as a focused recalibration:
- Element-breadth ceiling 4→3 STAYS (from v1.13)
- **NEW: skill-count ceiling 12→10** (PRIMARY lever per WARN 1)
- α=0.07→0.08 (identity-flavor only per WARN 1)
- Acceptance gate ≥12/17 (time-boxed per WARN 2)
- Structural framing shifted from DPS-output to resistance-immunity-coverage (per WARN 3)

---

## Required reading

1. **Gandalf D11 post-mortem** — `canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md` (or appended to `dispatches/2026-05-17-gandalf-d11-postmortem-option-b-veto-authority.md` completion record) — the authoritative source for these 3 warnings
2. **Gandalf D11 advisory** — `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` (your original genre-design source; consume identity intent)
3. **Your own D11 math note (v1.6)** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md` (the v1.13 spec rocket implemented; reuse what's still correct; revise per warnings)
4. **Rocket v1.13 completion record** — empirical data: 1/17 converged; WR 0.56-0.84 at modifier floor; tax 0.93 applied at Site A; per-instance breakdown in `d11_salvage_summary.json`
5. **D11.1 _tax_config.yaml** — `reincarnated-engine/config/_tax_config.yaml` (current α=0.07; bump to 0.08; add ceiling=10 if config-driven)
6. **`src/reincarnated/generation/d10_kit_constraints.py`** — your seam for the ceiling change (12→10 alongside existing element-breadth 4→3)

---

## Scope — D11.1 math note recalibration

Author at: `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11.1-ceiling-primary-tuning-math-note-2026-05-17.md`

Structure (slimmer than v1.13 note; this is a delta):
1. **§ 0 TL;DR** — D11.1 ceiling-primary recalibration; ≥12/17 acceptance gate; D11.2 redesign on miss
2. **§ 1 — Gandalf post-mortem translation** — restate WARN 3 in math-spec terms: gauntlet resistance-immunity-coverage as real mechanism; coverage attacked by ceiling, not damage
3. **§ 2 — Lever delta from v1.13** — what changes, what stays:
   - **NEW: skill-count ceiling for hybrid_mage = 10** (was 12 implicit; D11.1 makes explicit at 10)
   - α: 0.07 → 0.08 (identity-flavor only)
   - element-breadth ceiling 4→3 (unchanged from v1.13)
   - Tax formula unchanged: `tax_multiplier = 1.0 − α × max(0, n_elements − 2)²`
   - Tax application Site A (unchanged from v1.13)
4. **§ 3 — Coverage-reduction projection** — frame convergence projection in terms of coverage reduction (not damage reduction):
   - v1.13 hybrid_mage avg n_skills ≈ 12; n_elements ≈ 3; coverage span = 36 element-slot-events
   - D11.1 hybrid_mage max n_skills = 10; n_elements ≤ 3; coverage span ≤ 30 (-16.7%)
   - Mechanism: fewer skill slots → fewer resistance-profile representations per kit → less gauntlet-coverage immunity → WR closer to convergence band
5. **§ 4 — Convergence projection (resistance-coverage-based)** — project against v1.13 sample; target ≥12/17 (gate); empirical floor for sanity
6. **§ 5 — Generation rules (rocket implements)** — single-line change in `d10_kit_constraints.py`: `_ARCHETYPE_SKILL_COUNT_CEILING["hybrid_mage"] = 10` (or wherever skill-count ceiling lives); α config bump in `_tax_config.yaml`
7. **§ 6 — Salvage strategy** — re-process the 17 hybrid_mage instances from v1.13-curated state (NOT pre-D11; the v1.13 tax already applied). Prune to 10 skills per instance (keep highest-modifier or highest-DPS skills; salvage script decides). Re-run balance loop; report convergence
8. **§ 7 — Cross-seam impact + R11(b)** — none new (carries v1.13 contracts forward)
9. **§ 8 — Acceptance criteria for rocket D11.1 implementation** — ≥12/17 hybrid_mage converged; per-instance WR documented; if MISS document for D11.2 escalation
10. **§ 9 — Out of scope** — D12+ ceremonial 4-element; D11.2 structural rework (separate Matt L3); α escalation beyond 0.08

---

## Out of scope (DO NOT)

- ❌ DO NOT propose α > 0.08 (per WARN 1 + WARN 2; jack-ryan Gate 1 will pre-flag)
- ❌ DO NOT propose ceiling < 10 for hybrid_mage without explicit Matt + gandalf authorization
- ❌ DO NOT re-author the full v1.13 math note (delta-only document)
- ❌ DO NOT pre-empt D11.2 structural rework (your math note's § 9 flags D11.2 trigger; doesn't author D11.2 itself)
- ❌ DO NOT modify generation/ code (rocket's seam; you specify rule, rocket implements)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] D11.1 math note authored (9 sections per structure above)
- [ ] § 1 explicitly translates WARN 3 (resistance-immunity-coverage as real mechanism)
- [ ] § 2 frames ceiling 12→10 as PRIMARY lever (per WARN 1)
- [ ] § 3 + § 4 ground projection in coverage-reduction math, not damage-reduction math
- [ ] Convergence projection has clear acceptance gate ≥12/17
- [ ] § 9 explicitly flags D11.2 as escalation path if MISS (NOT α-escalation; per WARN 2)
- [ ] MIGRATION.md v1.11 entry if any new fields (likely just config; minimal contract change)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log
- [ ] HANDOFF → rocket (D11.1 implementation; queued) + HANDOFF → jack-ryan (D11.1 Gate-1; queued; instructed to hold the α≤0.08 + ceiling≥10 line)
- [ ] Hive-log STATE
- [ ] Tag `gamora/v1.7-d11.1-ceiling-primary-tuning-math-note-1`

---

## Coordination

- **Predecessor:** gandalf D11 post-mortem (shipped 2026-05-17 evening)
- **Triggers:** jack-ryan D11.1 Gate-1 advisory (queued; auto-fires on your completion) → rocket D11.1 implementation (queued; auto-fires on jack-ryan)
- **Parallel-safe with**: drax v1.12.0.1 hotfix (shipped); rocket v1.13.1 backfill (shipped); legolas-4 audio crawl (in flight); elrond CraftPix curation (shipped)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 Option B + Gandalf ENDORSE-with-warnings. ~0.5-1 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 late evening
**Author:** gamora
**Output:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11.1-ceiling-primary-tuning-math-note-2026-05-17.md` (9 sections)
**Tag:** `gamora/v1.7-d11.1-ceiling-primary-tuning-math-note-1` (local; push gated per ADR-006)
**MIGRATION.md:** No new entry. v1.10 from v1.13 carries forward. See § 7.1 of math note.
**AGENT_STATE:** Updated.
**Hive log:** PRE-SIGNAL + STATE appended.
**Wall time:** ~0.5 day (within Pattern B estimate)

### Acceptance criteria check

- [x] D11.1 math note authored (9 sections per dispatch structure)
- [x] § 1 explicitly translates WARN 3 (resistance-immunity-coverage as real mechanism; DPS-race anchor failure named; 2-element smoking gun documented)
- [x] § 2 frames ceiling 12→10 as PRIMARY lever (WARN 1; α nudge framed as identity-flavor; Δtax≈1% explicitly non-convergence)
- [x] § 3 + § 4 grounded in coverage-reduction math, not damage-reduction math (WARN 3; per-group coverage-span analysis; WR threshold crossing analysis)
- [x] Convergence projection has clear acceptance gate ≥12/17 (§ 4.3; honest miss-projection documented)
- [x] § 9 explicitly flags D11.2 as escalation path if MISS — NOT α-escalation (WARN 2)
- [x] MIGRATION.md: no v1.11 entry required (v1.10 carries; confirmed in § 7.1)
- [x] PRE-SIGNAL § 14.1.1 before hive-log (completed)
- [x] HANDOFF → rocket (D11.1 implementation; queued) + HANDOFF → jack-ryan (Gate-1; queued)
- [x] Hive-log STATE appended
- [x] Tag `gamora/v1.7-d11.1-ceiling-primary-tuning-math-note-1` (cut below)

### New empirical finding from Discipline #11

Tax persistence IS working (resolved Gandalf's § 4 concern). Two 2-element instances floor-pin without any tax (smoking gun for structural DPS density failure mode). Conservative convergence projection: 1-2/17. Realistic: 2-4/17. Both below gate. Gate must be run — projection is not measurement.

### Auto-fire trigger

**jack-ryan D11.1 Gate-1:** auto-fire on this completion record per dispatch `2026-05-17-jack-ryan-d11-1-gate1-hold-the-line-queued.md`.
**rocket D11.1 implementation:** auto-fires after jack-ryan Gate-1 verdict per dispatch `2026-05-17-rocket-d11-1-ceiling-primary-implementation-queued.md`.

— gamora
