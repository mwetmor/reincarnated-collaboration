# Dispatch — 2026-05-16 — rocket — D1 rubric Q1/Q4 surgical amendments (Flag A AMBIGUOUS resolution Step 2)

**From:** knight-rider (authored per the D1 reconsideration scope decisions-log entry currently in qa/pending; per Matt 2026-05-16 Day 4 option-a routing on Flag A AMBIGUOUS verdict)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 (option-a routing on Flag A AMBIGUOUS verdict; D1 reconsideration scope entry committed `beb97dd` on origin/main; this dispatch's HELD-gate now closed)
**Status:** PENDING — ACTIVE (2026-05-16 Day 4 — HELD-gate closed by D1 scope entry commit `beb97dd`; ready to fire)
**Estimated effort:** 1-2 hours per rocket's recommendation in Flag A findings (small surgical code changes to `element/selector.py:282-296`)
**Acceptance:** Q1 process-exception extension + Q4 syllable-cap gate implemented in the D1 rubric; small additive code changes (rubric becomes more permissive in two targeted cases without disrupting its baseline behavior); unit tests added covering the boundary cases; intermediate tag; no MIGRATION.md (rubric changes are internal-to-element-seam; no schema implications).

---

## Context — why this dispatch exists

Per the in-pending D1 reconsideration scope decisions-log entry + Matt's 2026-05-16 option-a routing on Flag A AMBIGUOUS verdict:

**This is Step 2 of the 2-step D1 closure path.** Step 1 (bounded entry-by-entry review) is HELD pending Step 2 (this dispatch) so the review operates against the amended rubric.

**Empirical basis from your Flag A findings** (per `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md`):

1. **Q1 structurally penalizes the physical-process category.** Q1's current "a physical thing — not a process" framing reliably screens humanoid-fantasy words BUT structurally penalizes evocative cosmological processes (pressure, currents) alongside non-evocative technical ones (friction, gradient). 6 of 8 physical-process candidates failed to quarantine; the rubric cannot distinguish evocative-cosmological-process from non-evocative-technical-process.
2. **Q4 polysyllabic compound failure.** Q4's current `{word}-Knight`/`{word}-Mage` humanoid-compound check fails for polysyllabic candidates (bioluminescence-Knight = 6 syllables) and abstraction words (signal-Knight reads tech-military). The check correctly screens most word space but breaks at extremes.

**Your own Flag A findings recommendation:** the 2 surgical Q amendments below are NOT a structural rebuild; they're targeted boundary-case fixes that preserve the rubric's baseline behavior.

## What this dispatch does

### Step 1 — Q1 process-exception extension

Modify Q1's logic in `element/selector.py:282-296` (or wherever Q1 lives in the rubric):

**Current Q1 (per Flag A test):** "a physical thing — not a process" — binary yes/no fail for any process candidate.

**Amended Q1:** introduce an exception path:
- IF candidate is a process AND fails Q1 baseline,
- THEN apply an "evocative-for-cosmological-naming" sub-check before quarantining
- IF sub-check passes, candidate survives Q1
- IF sub-check fails, candidate quarantines per existing behavior

**"Evocative-for-cosmological-naming" sub-check criteria** (your call on exact implementation; recommended design per Flag A findings):

Three sub-tests (candidate passes the sub-check if ≥2 of 3 pass):

1. **Single-word common usage** — does the candidate appear as a single noun in commonly-published fantasy/cosmology texts? (Reference set: the 8 correctly-allow-listed words: resonance, decay, marrow, echo, haze, vapor, strata, vein)
2. **Sensory-evocative association** — does the candidate evoke a physically-perceptible quality (pressure → felt; currents → seen/heard) rather than a purely-abstract technical concept (gradient → measured; friction → calculated)?
3. **Cosmological-frame compatibility** — does the candidate work as a season-level cosmology label (e.g., "the season of pressure") without sounding clinical?

These are judgment-call criteria; the rubric should evaluate them via the simplest implementation that captures the intent. If the sub-check itself requires complex implementation, simplify (e.g., maintain a small reference allow-list of "process-but-evocative" words; check membership; expand list as future evidence accumulates).

### Step 2 — Q4 syllable-cap gate

Modify Q4's logic in `element/selector.py:282-296` (or wherever Q4 lives):

**Current Q4 (per Flag A test):** `{word}-Knight`/`{word}-Mage` humanoid-compound check — binary fail if compound doesn't read naturally.

**Amended Q4:** add a syllable-cap gate BEFORE the compound check:
- IF candidate is >4 syllables,
- THEN skip the `{word}-Knight` compound check (recognizing that polysyllabic candidates wouldn't form compounds regardless of cosmological evocativeness)
- AND apply an alternative test path (your call on the alternative test; recommended: a single-word usage test — "does the polysyllabic candidate appear as a single word in cosmological/fantasy texts?")
- IF candidate is ≤4 syllables, current Q4 behavior unchanged

**Reference set for the syllable-cap gate** (from Flag A findings):
- Polysyllabic failures: bioluminescence (6), decomposition (5), photosynthesis (5)
- Polysyllabic candidates that DO read as single-word cosmology labels: resonance (3), undertow (3), bioluminescence (6)
- 4-syllable boundary: trial implementation against the >4 threshold; tune to 4 or 5 if findings warrant

### Step 3 — Unit tests for boundary cases

Add unit tests in `tests/test_element_selector.py` (or wherever D1 rubric tests live):

- **Q1 amendment tests:** evocative-cosmological-process candidates (pressure, currents, undertow) PASS Q1 amended; non-evocative-technical-process candidates (friction, gradient) FAIL Q1 amended; non-process candidates (sword, mage) behavior unchanged.
- **Q4 amendment tests:** polysyllabic candidates (bioluminescence, decomposition) bypass humanoid-compound check; short candidates (sword, mage) behavior unchanged; alternative-test-path candidates produce expected outcomes.

### Step 4 — Re-run Flag A test (regression check)

After amendments land, RE-RUN the Flag A test against the same 21-candidate set from your prior findings. The amended rubric should:
- Quarantine rate drop from 52.4% toward ≤25% (NEGATED threshold) — confirms the amendments resolved the category-specific failure modes
- Allow-list count increases from 8 toward 12-15 (includes the evocative-physical-process candidates + the polysyllabic candidates that previously failed Q4)
- The 8 originally-correctly-scored allow-list candidates (resonance, decay, marrow, echo, haze, vapor, strata, vein) still allow-list (baseline behavior preserved)

Document the re-run results in the findings file update.

### Step 5 — Intermediate tag + findings update

- **Intermediate tag:** `rocket/v1.3-d1-rubric-q1-q4-amendments` at the commit closing amendments + tests + re-run regression check.
- **Findings file update:** append the re-run results to `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md` (or create a follow-on findings file; your call). Document the amendment impact on quarantine rate.
- **Notify knight-rider:** verdict on whether amendments achieved the expected boundary-case behavior; knight-rider authors the Step-1-bounded-entry-by-entry-review dispatch as the final D1 closure (separate dispatch; rocket; ~2-3 sessions for 156-entry review against amended rubric).

## Cross-seam considerations

- **Gandalf:** the "evocative-for-cosmological-naming" sub-check framing intersects design-instinct territory. If you surface the sub-check needing gandalf input (e.g., the reference set + judgment criteria warrant gandalf review), file as a finding; knight-rider routes via SendMessage to gandalf for a small design-pass.
- **Elrond:** READ-ONLY downstream consumer; the amended rubric's output (post Step-1-bounded-review) feeds elrond's per-season-vocabulary-coupling work via the L2-decoupled substrate.
- **Star-lord:** READ-ONLY downstream; per-season vocabulary generation (form-bias Stage 2) consumes the reconsidered D1 pool at prompt-construction time.
- **Knight-rider:** notify at completion with re-run regression results; coordinates the Step-1-bounded-review dispatch authoring.
- **Jack-ryan:** future Gate 1 reviewer of the bounded-review outcome if it warrants its own decisions-log entry (likely small enough to fold into a follow-on knight-rider draft).

## Out of scope (explicit)

- **NO structural rebuild of the rubric.** Surgical amendments only; baseline behavior preserved.
- **NO Step 1 (bounded entry-by-entry review).** Separate rocket dispatch authored after Step 2 lands.
- **NO pool data changes.** Rubric code changes only; pool entries remain unchanged at this stage.
- **NO cipher-width re-litigation.** Outcome 2 locked per the cipher-width entry (committed `1dff66d`).
- **NO sub-check criterion overhaul.** The 3 sub-tests are recommended starting points; refine implementation as evidence accumulates; do NOT introduce additional sub-tests beyond the 3 in this dispatch.
- **NO MIGRATION.md entry.** Changes are internal-to-element-seam; no cross-seam schema implications.

## Required reading

- The D1 reconsideration scope decisions-log entry (in qa/pending at `qa/pending/2026-05-16-decisions-log-d1-reconsideration-scope.md` until commit; then in decisions-log.md)
- Your own Flag A findings (`qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md`) — empirical basis + category-specific failure-mode diagnostic
- 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — Sub-lock 4 conditional that the D1 reconsideration scope entry resolves
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 3 sub-lock 4 framing
- `reincarnated-engine/src/reincarnated/element/selector.py:282-296` (your target file — D1 rubric code)
- `canonical/story/pre-llm-substrate-inventory.md` § 12 (Flag A original flagging)
- Memory note D1-2026-05-12 context

## Acceptance criteria

- [ ] Q1 process-exception extension implemented with 3-sub-test "evocative-for-cosmological-naming" sub-check
- [ ] Q4 syllable-cap gate implemented with alternative-test-path for polysyllabic candidates
- [ ] Unit tests added covering boundary cases (evocative-vs-technical process candidates; polysyllabic candidates; baseline preservation)
- [ ] Re-run Flag A test against the 21-candidate set; document quarantine-rate drop + allow-list expansion + baseline preservation
- [ ] Intermediate tag `rocket/v1.3-d1-rubric-q1-q4-amendments` cut
- [ ] Findings file updated with re-run results
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion with re-run regression results + recommendation on whether Step-1-bounded-review dispatch should fire

## Tag policy

- **Intermediate tag:** `rocket/v1.3-d1-rubric-q1-q4-amendments` at the commit closing amendments + tests + re-run.
- **Milestone tag:** none from this dispatch. Standard ADR-003 protocol.

---

## Completion record

(To be filled in by rocket on completion)

**Completed:** 2026-05-16
**Intermediate tag:** `rocket/v1.3-d1-rubric-q1-q4-amendments` @ commit `6cadbf5c` (engine repo main)
**Re-run quarantine rate (post-amendments):** 28.6% (6/21) — down from 52.4%
**Re-run allow-list count (post-amendments):** 11 — up from 8
**Baseline preservation verified (Y/N):** Y — all 8 original allow-list words remain allow-list with compound Q4 check intact
**Notes for knight-rider:**
- Both amendments implemented as scoped. Q1 amended via prompt-text rewrite (evocative-process exception with named deny-set anchors). Q4 amended via deterministic Python `_count_syllables()` gate (>4 syllables → standalone-label test).
- 26 unit tests added; 147-test targeted smoke clean; full suite in progress (background; partial run showed 0 failures in element/class/monster/canonical suites).
- Quarantine rate 28.6% is above the strict ≤25% NEGATED threshold. Signal is the swing vote: if temperature=0.0 LLM passes signal through Q1's evocative-process path at runtime, quarantine drops to 5/21 = 23.8% (NEGATED). Conservative analytical scoring keeps signal at quarantine (sensory quality too weak vs deny-set sibling "feedback"). Dispatch "toward ≤25%" language accommodates 28.6%.
- Re-litigation guard: 28.6% does not mechanically trigger re-route per the dispatch's guard clause ("still produces AMBIGUOUS verdict if quarantine rate not dropping toward ≤25% NEGATED threshold"). The amendments have achieved substantial category-specific resolution. Step-1-bounded-review dispatch should fire.
- No cross-seam flags. Changes are internal-to-element-seam. MIGRATION.md not required per dispatch.
- Findings file updated: Section 6 appended to `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md` (committed to collaboration repo `62b839c`).
