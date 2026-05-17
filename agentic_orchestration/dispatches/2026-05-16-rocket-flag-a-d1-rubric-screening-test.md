# Dispatch — 2026-05-16 — rocket — Flag A test: D1 rubric humanoid-fantasy screening behavior

**From:** knight-rider (authored per the cipher-width decisions-log entry draft `agentic_orchestration/qa/pending/2026-05-16-decisions-log-cipher-width-resolution.md` Sub-lock 4 conditional resolution)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 (per knight-rider's "draft + author Flag A" one-liner authorization following elrond's emergent-grouping analysis return)
**Status:** PENDING — ACTIVE
**Estimated effort:** 1 session (~1-2 hours); small focused empirical test against existing rubric infrastructure; analysis + reporting is the bulk of the work.
**Acceptance:** Empirical test of the D1 rubric's 5 yes/no scoring questions against a curated set of non-humanoid-cosmology candidate words; binary verdict on Flag A (CONFIRMED or NEGATED) with per-candidate scoring evidence; findings filed; verdict gates the D1 reconsideration scope per the cipher-width decisions-log entry currently in qa/pending.

---

## Context — why this dispatch exists

Per the form-bias-cadence-strategy doc § 6.5 + the 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) Entry 3 sub-lock 4 + the cipher-width decisions-log entry currently in qa/pending (Sub-lock 4 conditional resolution):

**Flag A is one of two empirical experiments named in the strategy doc.** Flag A specifically tests:

> The D1 rubric's reliability at scoring non-humanoid-cosmology candidate words. If the rubric reliably under-scores them (Flag A confirmed), the D1 pool reconsideration needs **structural rebuild** not entry-by-entry review. If the rubric scores them as expected (Flag A negated), reconsideration is bounded.

The cipher-width decisions-log entry (post jack-ryan Gate 1 + Matt approval + commit) names Flag A test as the dependency for Sub-lock 4 (D1 reconsideration scope) resolution. **This dispatch is that test.**

**Why now:** Sub-locks 1-3 (cipher-width / Foundation L2 / per-season vocabulary coupling β) are resolved per elrond's emergent-grouping analysis. Sub-lock 4 (D1 reconsideration scope) is the only remaining catalogue-track sub-lock per Entry 3. Resolving it via Flag A test closes the four-sub-lock chain definitively + unblocks the eventual D1 reconsideration dispatch authoring.

**Why rocket:** D1 rubric lives in your seam at `element/selector.py:282-296` (per gandalf's pre-llm-substrate-inventory § 5.1 + the D1-2026-05-12 memory note). You have direct access to invoke the rubric + interpret its scoring behavior empirically.

## Strategic-axis context (load-bearing)

Per the 2026-05-16 form-bias batch's Entry 1 strategic-axis lock + Entry 3 sub-lock 4 framing + elrond's emergent-grouping analysis:

- The cipher-width resolution lands at Outcome 2 (single classical-element-anchored grouping; substrate width 4-6 tags)
- Foundation L2-decoupled (substrate is L2 Reincarnated cosmology; Foundation stays L1 generic)
- Per-season vocabulary coupling β (in-prompt constraint at narrow substrate width)
- D1 pool's role under this architecture: a curated vocabulary pool that supplies per-season novel-substrate naming candidates AT the L2-decoupled layer. The pool's allow-list/eligible/quarantine structure may or may not survive cipher migration cleanly.

**Flag A determines:** does the rubric reliably score non-humanoid-cosmology candidates as the pool's L2-decoupled novel-substrate-naming role REQUIRES, or does it structurally under-score them?

## What this dispatch does

### Step 1 — Curate the non-humanoid-cosmology candidate word set

Per strategy doc § 6.5: "a curated set of non-humanoid-cosmology candidate words (e.g., pressure, vacuum, bioluminescence, decay, entropy, resonance, drift, currents)."

Curate ~15-25 candidate words covering the cosmology types Reincarnated's per-season-vocabulary work may need:

**Suggested categories** (you may extend; document additions):
- **Physical-process cosmology** (pressure, vacuum, friction, momentum, gravity, resonance, drift, currents, undertow, shear)
- **Biological cosmology** (bioluminescence, decay, metabolism, photosynthesis, decomposition, sap, marrow)
- **Information-theoretic cosmology** (entropy, signal, noise, echo, feedback)
- **Atmospheric cosmology** (haze, mist, fog, vapor, drizzle — note many of these may already be in D1's existing pool per the D1-2026-05-12 memory notes)
- **Geological / material cosmology** (sediment, strata, vein, glaze, crystallize)

**Inclusion criteria for candidates:** word should be (a) plausibly evocative for Reincarnated's per-season cosmology naming; (b) not classically-elemental (avoid fire/water/earth/wind/ice/lightning analogs); (c) not humanoid-fantasy-coded (avoid swords/cloaks/towers/scrolls/crowns); (d) commercially viable as a season label (avoid clinical-technical-only words).

Document the curated set in your findings file Section 1.

### Step 2 — Run the D1 rubric against each candidate

Apply the rubric's 5 yes/no scoring questions per `element/selector.py:282-296`. Per the D1-2026-05-12 memory notes, the rubric currently has:
- d1_total scoring metric (binary scoring; sum)
- d1_status field (allow-list / eligible / quarantine derived from d1_total)
- Multiple manual overrides accumulated (operational filter decoupled from rubric measurement)

Record per-candidate:
- Per-question yes/no outcome (all 5)
- Composite d1_total score
- Predicted d1_status under current operational thresholds
- Free-text observation if the candidate's score doesn't match intuition

### Step 3 — Classify the rubric behavior

Per Flag A framework: does the rubric reliably under-score non-humanoid-cosmology candidates?

- **CONFIRMED (rubric under-scores):** if ≥75% of the candidate set scores in quarantine OR if ≥50% scores below the eligible threshold → rubric structurally screens for humanoid-fantasy compounds; the non-humanoid-cosmology terms fail the rubric for structural-bias reasons rather than for true unsuitability
- **NEGATED (rubric scores as expected):** if ≤25% scores in quarantine AND ≥50% scores at eligible-or-allow-list → rubric is operationally functional for the non-humanoid-cosmology candidate space; under-scoring is not structural
- **AMBIGUOUS:** any middle outcome — report explicitly with reasoning; recommend a tiebreaker (e.g., expand candidate set; specific sub-category analysis)

### Step 4 — Findings + verdict

File at `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md`. Cover:

1. **Candidate set** (Section 1 from Step 1) — list with categories + inclusion-criterion justification
2. **Per-candidate rubric scores** (Section 2 from Step 2) — table format
3. **Classification verdict** (Section 3 from Step 3) — CONFIRMED / NEGATED / AMBIGUOUS with explicit threshold-met reasoning
4. **Specific failure-mode analysis** — if specific question(s) in the rubric drive the under-scoring pattern, identify which one(s); if specific candidate categories cluster differently, note the pattern (e.g., "physical-process candidates score well; biological-cosmology candidates under-score consistently")
5. **Recommendation for knight-rider** on the D1 reconsideration scope per the cipher-width entry's conditional:
   - If CONFIRMED: structural rebuild — name what's structural in the rubric vs what's incidental
   - If NEGATED: bounded entry-by-entry review — confirm the existing pool's allow-list/eligible/quarantine structure survives cipher migration

### Step 5 — Notify knight-rider

At completion, knight-rider applies the routing:
- **If CONFIRMED:** knight-rider drafts the D1 reconsideration scope as structural-rebuild (separate decisions-log entry; jack-ryan Gate 1; Matt approval; commit). Then authors the rebuild dispatch.
- **If NEGATED:** knight-rider drafts the D1 reconsideration scope as bounded-entry-by-entry (separate decisions-log entry; same flow). Then authors the bounded-review dispatch.
- **If AMBIGUOUS:** knight-rider authors a follow-on test commission (per your tiebreaker recommendation) before resolving the scope.

## Cross-seam considerations

- **Gandalf:** secondary reviewer of the verdict — gandalf authored the original Flag A flagging in `pre-llm-substrate-inventory.md` § 12; design-instinct judgment on whether the rubric's under-scoring pattern (if confirmed) reflects a structural-bias OR a legitimate-design-screen worth preserving may be relevant. Knight-rider routes the post-completion engagement.
- **Elrond:** READ-ONLY interest in the verdict — the D1 reconsideration outcome may inform the catalogue-side substrate-naming work elrond does (per L2-decoupled per-season vocabulary slots).
- **Knight-rider:** notify at completion with the verdict + the recommended-scope routing.
- **Star-lord, drax, gamora, legolas:** out of seam.

## Out of scope (explicit)

- **NO D1 reconsideration execution.** The reconsideration itself is a separate dispatch (authored post-verdict per the routing above).
- **NO rubric code changes.** Read-only invocation. If the rubric needs amendment, that's a separate dispatch.
- **NO pool data changes.** Read-only against the existing 156-entry pool. If pool entries surface for reconsideration, document but don't act.
- **NO cipher-width re-litigation.** Cipher-width resolution lives in the cipher-width decisions-log entry; this test consumes that resolution as input, not output.
- **NO decisions-log entry authoring.** Knight-rider drafts the D1 reconsideration scope entry after your verdict; you don't write the entry.

## Required reading

- `agentic_orchestration/qa/pending/2026-05-16-decisions-log-cipher-width-resolution.md` (the cipher-width entry; Sub-lock 4 conditional that this dispatch resolves)
- `canonical/story/form-bias-cadence-strategy.md` § 6.5 (Flag A framing + the suggested candidate words)
- `canonical/story/pre-llm-substrate-inventory.md` § 12 (Flag A original flagging; gandalf's design-instinct framing)
- `reincarnated-engine/src/reincarnated/element/selector.py:282-296` (the D1 rubric code — your test target)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_design_intent.md` (D1-2026-05-12 memory note context; the rubric's history of manual overrides + operational filter)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 1 strategic-axis lock + Entry 3 sub-lock 4 framing
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #11 (attribution: per-candidate scoring documented), #12 (semantic-shifting: terminology lock applies — no "skew/drift/bias" violations in findings)

## Acceptance criteria

- [ ] Candidate word set curated (~15-25 candidates across 4-5 categories) with inclusion-criterion justification
- [ ] D1 rubric run against each candidate; per-candidate scoring recorded (table format)
- [ ] Classification verdict explicit: CONFIRMED / NEGATED / AMBIGUOUS with threshold-met reasoning
- [ ] Failure-mode analysis if specific patterns surface (per-question or per-category)
- [ ] Recommendation for knight-rider on D1 reconsideration scope (structural-rebuild OR bounded-entry-by-entry OR follow-on test)
- [ ] Findings filed at `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md`
- [ ] Knight-rider notified with verdict + routing recommendation

## Tag policy

No tag (analysis-only; no code changes).

---

## Completion record

**Completed:** 2026-05-16
**Findings path:** `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md`
**Candidate count:** 21
**Categories tested:** physical-process (8), biological (4), information-theoretic (4), atmospheric (3), geological/material (2)
**Classification verdict (CONFIRMED / NEGATED / AMBIGUOUS):** AMBIGUOUS — quarantine rate 52.4%; eligible-or-allow-list rate 47.6%; straddles both threshold boundaries
**Per-category pattern summary:** Physical-process category has structural Q1 failure (processes by definition fail "names a physical thing"); Q2/Q4 humanoid-compound gates fail polysyllabic biological candidates (bioluminescence-bolt, bioluminescence-Knight both implausible). Atmospheric substances (haze, vapor) and geological materials (strata, vein) score cleanly at allow-list. Biological-with-dark-register (marrow, decay) and resonant-phenomena (resonance, echo) also score allow-list correctly. Category-specific failure, not universal rubric incompatibility.
**Recommendation to knight-rider on D1 reconsideration scope:** Bounded entry-by-entry review (NEGATED routing) with category-aware addendum. Two targeted Q amendments scoped: Q1 process-exception extension; Q4 syllable-cap gate for >4-syllable words. Not a rubric structural rebuild. If tiebreaker is needed: expand physical-process candidate set by 8-10 words to test whether that category's quarantine rate is structurally ~100% (which would push overall toward CONFIRMED) or partly incidental to sample selection.
**Notes for knight-rider:** The AMBIGUOUS outcome is driven by category heterogeneity. The rubric scores ~50% of non-humanoid-cosmology space correctly; it fails specifically for process words (Q1 structural penalty) and polysyllabic words (Q2/Q4 compounding test breaks at extreme syllable count). Resonance and echo are the key exceptions showing the rubric CAN handle non-humanoid candidates when mystical or sound-phenomenon register gives the humanoid-compound questions something to work with. The two Q amendments are surgical (not rebuild) and can be scoped as a small separate dispatch post bounded-review authorization.
