# Decisions-log entry draft — D1 reconsideration scope resolved as bounded entry-by-entry review (per Flag A AMBIGUOUS verdict + Matt option-a routing)

**Author:** knight-rider
**Date drafted:** 2026-05-16 (Day 4)
**Source:** rocket's 2026-05-16 Flag A D1 rubric screening test findings (verdict AMBIGUOUS; 52.4% quarantine; both CONFIRMED + NEGATED thresholds missed; recommendation NEGATED-routing-with-Q1/Q4-amendments). Matt option-a routing 2026-05-16 Day 4 ("fire fresh star-lord for regen recovery + option a on Flag A") — accept rocket's NEGATED routing + author Q1/Q4 surgical amendment dispatch as 2-step closure.
**Process:** Knight-rider drafts → jack-ryan Gate 1 → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the form-bias 5-entry batch (committed `5d51b5a`) + ailment-deferral (committed `680a3f1`) + cipher-width (committed `1dff66d`).

**Target location:** before the "Recently considered, not yet decided" section, after the 2026-05-16 cipher-width resolution entry (committed `1dff66d`).

**Companion-to:** the 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — specifically Sub-lock 4 conditional. This entry resolves the conditional with the NEGATED branch + the surgical-Q-amendment follow-on path.

---

## Entry — D1 reconsideration scope resolved as bounded entry-by-entry review per Flag A AMBIGUOUS verdict + Matt option-a routing; Q1/Q4 surgical rubric amendments authored as separate follow-on dispatch

### 2026-05-16: D1 reconsideration scope — bounded entry-by-entry review (per Flag A AMBIGUOUS verdict); Q1 process-exception + Q4 syllable-cap surgical amendments queued as separate rocket dispatch

**Decision:** The 4th catalogue-track sub-lock per Entry 3 of the form-bias 5-entry batch (committed `5d51b5a`) — D1 reconsideration scope — is resolved as **bounded entry-by-entry review** per the NEGATED routing in the 2026-05-16 cipher-width resolution entry's Sub-lock 4 conditional (committed `1dff66d`).

**Per the cipher-width entry's Sub-lock 4 conditional:**

> If Flag A negates (rubric scores non-humanoid-cosmology candidates as expected): D1 reconsideration is bounded entry-by-entry review against the Sub-lock-1-determined substrate-width target — likely shrinking allow-list from 81 toward ~30-50 entries that map cleanly to the canonical-element-anchored substrate set + a small reserve for per-season novel-substrate naming.

This entry implements that path with the AMBIGUOUS-verdict-resolved-as-NEGATED routing.

**Empirical basis — rocket's Flag A test findings:**

- 21 candidates across 5 categories (physical-process / biological / information-theoretic / atmospheric / geological-material)
- Quarantine rate: 52.4% (11/21)
- Eligible-or-allow-list rate: 47.6% (10/21)
- Both CONFIRMED thresholds (≥75% quarantine OR ≥50% below eligible) missed
- Both NEGATED thresholds (≤25% quarantine AND ≥50% eligible-or-allow-list) missed
- **Verdict: AMBIGUOUS** with category-specific failure-mode pattern

**The failure-mode is category-specific, not universal** (per rocket's findings):

1. **Q1 structurally penalizes the entire physical-process category.** Q1 asks for "a physical thing — not a process." Every physical-process candidate (pressure, vacuum, friction, momentum, currents, gradient, undertow) fails Q1 by category definition. 6 of 8 → quarantine. The rubric cannot distinguish evocative cosmological processes (pressure, currents) from non-evocative technical ones (friction, gradient).
2. **Q2 and Q4 are humanoid-compound gates.** `{word}-bolt`/`{word}-armor` and `{word}-Knight`/`{word}-Mage` fail for polysyllabic biological candidates (bioluminescence-Knight is 6 syllables and sounds academic) and for abstraction words (signal-Knight reads tech-military). Correctly screen MOST of the word space but break at extremes.

**8 candidates DID correctly score allow-list** (resonance, decay, marrow, echo, haze, vapor, strata, vein) — words genuinely appropriate for fantasy-ARPG cosmology use. The rubric isn't broken; it has category-specific structural blind spots.

**Matt option-a resolution (2026-05-16 Day 4):**

Treat AMBIGUOUS as functionally NEGATED → route to bounded entry-by-entry review WITH 2 surgical Q amendments as a separate follow-on dispatch. Reasoning: (a) rocket's empirical diagnosis is sharp; the surgical Q amendments address the real failure-mode without committing to full structural rebuild; (b) the cipher-width resolution (Outcome 2; substrate width 4-6 tags) means the D1 pool's role is bounded — full structural rebuild is over-engineering for the substrate width; (c) the surgical-Q-amendment path resolves both the AMBIGUOUS verdict's category-specific failure modes AND the bounded entry-by-entry review's pool-shrinking work in a coordinated sequence.

**Two-step closure path:**

**Step 1 — bounded entry-by-entry review (this entry locks):**
- D1 pool 156-entry review against the Sub-lock-1-determined substrate-width target
- Likely shrinking allow-list from 81 toward ~30-50 entries that map cleanly to the canonical-element-anchored substrate set
- Small reserve preserved for per-season novel-substrate naming
- Per-entry decision-records preserved for audit-trail
- Future rocket dispatch authored after Step 2 lands (the Q amendments inform the review's threshold-tuning)

**Step 2 — Q1/Q4 surgical rubric amendments (separately authored dispatch):**

- **Q1 process-exception extension** — Q1's current "a physical thing — not a process" framing reliably screens humanoid-fantasy words but structurally penalizes evocative cosmological processes (pressure, currents) alongside non-evocative technical ones (friction, gradient). The amendment introduces an exception path: process candidates that PASS a "evocative-for-cosmological-naming" sub-check survive Q1. Sub-check criteria designed against the 8-allow-list reference set (resonance, decay, marrow, echo, haze, vapor, strata, vein) + the 6 physical-process candidates that failed (pressure, vacuum, friction, momentum, currents, gradient, undertow).
- **Q4 syllable-cap gate** — Q4's current `{word}-Knight`/`{word}-Mage` humanoid-compound check fails for polysyllabic candidates that wouldn't fit naturally in a compound regardless of cosmological evocativeness. The amendment adds a syllable-cap gate (e.g., words above 4 syllables get an alternative test path rather than failing Q4 by default).

**Step 2 is authored as a separate rocket dispatch at `agentic_orchestration/dispatches/2026-05-16-rocket-d1-rubric-q1-q4-surgical-amendments.md`.** The amendments are small code changes to `element/selector.py:282-296` (the rubric); ~1-2h work; standard rocket dispatch flow.

**Step 1 (bounded entry-by-entry review) is HELD pending Step 2** so the review benefits from the amended rubric's improved scoring at boundary cases.

**Reasoning:** Per rocket's empirical findings + Matt's 2026-05-16 option-a routing. The AMBIGUOUS verdict's specific failure-mode diagnostic + rocket's surgical-Q-amendment recommendation are the strongest evidence for the resolution path. Treating AMBIGUOUS as CONFIRMED (full structural rebuild) would over-architect; treating as pure NEGATED (no amendments, just review) would leave the category-specific blind spots in place for future D1 pool work. The 2-step closure path threads the needle.

**Alternatives considered:**

- **(a) Treat AMBIGUOUS as CONFIRMED → structural rebuild:** rejected per Matt option-a routing. Over-engineering for the cipher-width-locked 4-6-substrate-width target; the rubric has surgical-fixable category-specific issues, not structural failure.
- **(b) Run tiebreaker (expand physical-process candidate set; may flip to CONFIRMED):** rejected per Matt option-a routing. Calendar cost (~+1 session) + risk that tiebreaker still lands AMBIGUOUS; the surgical-amendment path resolves the underlying issue regardless of tiebreaker outcome.
- **(c) Pure NEGATED routing (review without Q amendments):** rejected. Leaves the category-specific structural blind spots (Q1 process-penalty + Q4 polysyllabic-compound-failure) in place; future D1 work would inherit the same boundary-case failures.
- **(d) Defer D1 reconsideration entirely** until additional empirical evidence (e.g., post-cipher-migration LLM behavior data) accumulates: rejected. The cipher-width entry's Sub-lock 4 conditional is locked; D1 reconsideration scope must resolve cleanly; deferring would leave a dangling sub-lock conditional.
- **(e) Partial rebuild — Q1 process-exception only, no Q4 syllable-cap amendment** (implement just the Q1 fix; leave Q4 unchanged): rejected. Rocket's Flag A findings show both Q1 and Q4 produce category-specific failures (Q1 → physical-process category; Q4 → polysyllabic/abstraction words). Implementing only Q1 would leave the Q4 polysyllabic-compound-failure mode in place; the surgical-amendment scope is bounded enough that bundling both in a single dispatch (per the Q1/Q4 dispatch above) is more efficient than two separate dispatches.

**Cross-seam cascades:**

- **Rocket:** Q1/Q4 surgical amendments dispatch authored at `dispatches/2026-05-16-rocket-d1-rubric-q1-q4-surgical-amendments.md` (Status: PENDING — HELD pending this entry committing; rocket fires after entry lands). After Step 2 lands, knight-rider authors the bounded entry-by-entry review dispatch (Step 1 of the 2-step closure).
- **Elrond:** READ-ONLY consumer of D1 reconsideration outcomes (post Step 1 review). The bounded review's output (~30-50 entry allow-list) feeds elrond's eventual per-season-vocabulary-coupling work via the L2-decoupled substrate.
- **Star-lord:** READ-ONLY consumer; per-season vocabulary generation work (form-bias Stage 2 — strategy doc § 9.2 cascade) consumes the reconsidered D1 pool at prompt-construction time.
- **Gandalf:** secondary reviewer of the surgical-Q-amendment design (rocket may surface "evocative-for-cosmological-naming sub-check" framing as gandalf-design-instinct-adjacent; knight-rider routes if rocket flags).
- **Jack-ryan:** Gate 1 reviewer on this entry + on the eventual surgical-amendment outcome (if rocket's amendments warrant their own decisions-log entry — likely small enough to fold into a follow-on knight-rider draft).

**Status:** Active. Closes Sub-lock 4 conditional per the 2026-05-16 cipher-width resolution entry (`1dff66d`).

**Re-litigation guard:** if Step 2 (Q1/Q4 surgical amendments) re-run post-amendment regression check (per rocket's amendment dispatch Step 4) still produces an AMBIGUOUS verdict (i.e., the amendments don't drop the quarantine rate to NEGATED-threshold ≤25% AND ≥50% eligible-or-allow-list), knight-rider re-routes: either author a follow-on tiebreaker dispatch (expand candidate set per rocket's original tiebreaker recommendation) OR escalate to Matt for a fresh routing decision. The current Step-1-bounded-review path assumes the amendments achieve their expected boundary-case fix; if they don't, the bounded-review's threshold-tuning operates against weak empirical footing.

**Implementation cascade:**

- **Step 2 first** (Q1/Q4 surgical amendments; ~1-2h rocket work) — authored at `dispatches/2026-05-16-rocket-d1-rubric-q1-q4-surgical-amendments.md`; HELD pending this entry committing; fires post-commit
- **Step 1 second** (bounded entry-by-entry review; rocket dispatch authored after Step 2 lands) — operates against the amended rubric; output is the reconsidered D1 pool

**Related:**

- `agentic_orchestration/qa/findings/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md` (the empirical basis — Flag A AMBIGUOUS verdict + category-specific failure-mode diagnostic)
- `agentic_orchestration/dispatches/2026-05-16-rocket-flag-a-d1-rubric-screening-test.md` (the test dispatch)
- `agentic_orchestration/dispatches/2026-05-16-rocket-d1-rubric-q1-q4-surgical-amendments.md` (Step 2 dispatch authored alongside this entry; PENDING — HELD)
- 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — Sub-lock 4 conditional this entry resolves
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 3 sub-lock 4 framing (now fully resolved by this entry + the cipher-width entry)
- `canonical/story/form-bias-cadence-strategy.md` § 6.5 (Flag A framing)
- `canonical/story/pre-llm-substrate-inventory.md` § 12 (Flag A original flagging)
- `reincarnated-engine/src/reincarnated/element/selector.py:282-296` (D1 rubric code — Step 2's target)
- Memory note D1-2026-05-12 context (per `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_design_intent.md`)
- **Companion entry:** 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — this entry completes its Sub-lock 4 closure

---

## Knight-rider note (NOT for decisions-log; for jack-ryan Gate 1)

Cross-cutting questions for jack-ryan to test:

1. **2-step closure path justification:** is the Step-2-first / Step-1-second sequencing right? My read: yes — the bounded review operates against the AMENDED rubric, so amending first means the review's threshold-tuning is more accurate. Push back if you'd prefer Step 1 first (review against current rubric; then amend rubric for future work).
2. **AMBIGUOUS-as-functionally-NEGATED framing:** does the entry's framing risk re-litigation? My read: the Matt option-a routing is explicit; the entry captures it cleanly. Confirm.
3. **Discipline #13b attribution:** the entry says "the rubric isn't broken; it has category-specific structural blind spots." Per Discipline #13b, this is an inference from rocket's empirical pattern (8 correct allow-list + 6 category-specific failures). Verify the framing is within narrow legitimate use.
4. **Alternatives section completeness:** four alternatives. Any missing?
5. **Cross-seam cascades:** rocket / elrond / star-lord / gandalf / jack-ryan covered. Anything else cascades I missed?

If all five pass with no BLOCK, this entry is ready for Matt approval and commit.
