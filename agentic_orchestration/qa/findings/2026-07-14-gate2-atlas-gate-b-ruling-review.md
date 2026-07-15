# Finding — 2026-07-14 — Gate-2 post-results protocol review of the Gate-B ruling (atlas derivation)

**Reviewer:** jack-ryan
**Mode:** DEV-MODE (Gate-2, BLOCK authority) — post-results protocol-amendment review
**Severity:** RATIFY-WITH-AMENDMENTS (R1 ratified with one binding rider; R2 ratified; R3 ratified with one clarification)
**Target:** `agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-b-diagnosis-and-proposed-ruling.md` (commit 69594f4c)
**Author under review:** gandalf (SPEC-AUTHOR proposing a ruling on his own gate — conflict declared by author)
**Executor of pipeline:** elrond (gate report `agentic_orchestration/research/curated/atlas/2026-07-14-gate-report.md`)
**Principles applied:** Review-Principle #1 (math-before-code — here, math-before-ruling), #2 (smoke/diagnostics-before-freeze), #4 (decisions-log/register as truth), #5 (severity matters); Discipline #11 (empirical-over-assumption), #12 (semantic-shift declaration), #8 (schema-validation at boundaries); ADR-002 (tiered approval — this ruling exceeds my tier at the freeze step → Matt ratifies), ADR-006 (read-only external systems — SELECT/CSV-read only, honored)

---

## Verdict

**RATIFY-WITH-AMENDMENTS** on the proposed ruling.

- **R1 (reclassify Gate B → Finding F-1; freeze criterion becomes A+C+D; zero recomputation):** **RATIFY** with one binding rider (RIDER-1 below). This is a legitimate use of the one-amendment-cycle power, not gate-deletion-after-failure. The Edition-I freeze decision itself remains Matt's per charter §9 and ADR-002 — my ratification clears the *ruling*, not the freeze.
- **R2 (retire danger-zone overlay vocabulary; GRAVEYARD renders as per-corpse tombstones):** **RATIFY.** Follows necessarily from F-1 and improves charter honesty.
- **R3 (Edition-II replacement negative-validity criterion, per-law, powered, fresh v2 prereg with my review):** **RATIFY** with one clarification (CLARIFY-1 below).

The package proceeds to Matt for the Edition-I freeze decision.

---

## What I independently verified vs took on trust

**Independently reproduced (read-only, from the committed CSVs `atlas-coordinates-active.csv` + `atlas-coordinates-supplementary.csv`, 14-D retained space):**

1. **The §3.2 neighbor-identity table — byte-for-byte.** I recomputed the 5 nearest active neighbors for all five intrinsic-red corpses. **Every corpse, every neighbor, every WHIRLWIND tag, in the same rank order gandalf reported.** Confirmed load-bearing specifics: `poe2-walking-calamity` is genuinely the 4th-nearest active kit to `d2-blaze-sorc` (dist 0.724); `gd-eor-warlord` and `d2-ww-sin` (both frozen-label WHIRLWIND) are genuinely among `poe1-charged-dash`'s five nearest. The evidence is real and regenerates from the committed artifacts. It was not embellished.
2. **The Gate-B pooled statistic.** Observed mean pairwise (k=5) = **2.4404 exact**; my null mean 1.8499 vs report 1.8549; my p_dispersed 0.0369 vs report 0.0363; my p_tight 0.9631 vs report 0.9638. Matches within Monte-Carlo tolerance (seed/RNG-order deltas only).
3. **The extrinsic-tuning secondary (k=6).** Observed 2.0944 exact; p_lower 0.818 vs report 0.814. Matches.
4. **Stage-0 reconciliation (37 vs 38).** The supplementary CSV has 38 rows; exactly 37 carry a `death_class` + coordinates; the 5 intrinsic-red ids are exactly `{d2-blaze-sorc, d2-leap-attack-barb, poe1-charged-dash, poe1-reaper, vs-gatti-amari}`. The 38th is the non-combat system record. **This is documented data-state, not a silent denominator change** — confirmed against my own Gate-1 A6 note and elrond's Stage-0 §.
5. **Falsifiability-in-reverse of the pooled gate (my own adversarial probe, NOT in the proposal).** The "tight" pass line was the null 5th percentile ≈ 1.389. Genuinely co-located single-family sets sit well below it (AURA 0.86, WHIRLWIND 1.02, MINION-PET 0.98, TRAP-MINE 1.37). The five red corpses sit at 2.44 — **33% above the null median**, with inter-corpse distances up to 3.69 (leap-barb↔vs-gatti). So the gate was *passable in principle* by a co-located corpse set — it was **not** literally unfalsifiable — but passing was conditional on a substantive territory fact (that the distinct red laws co-locate) that no prior artifact asserted.
6. **The neighbor test is genuinely post-hoc.** The prereg contains no pre-registered nearest-neighbor test (only the boilerplate phrase "nearest neighbor of the pinned choice"). Confirmed by grep of the pinned v1.1.
7. **The operationalization gap is textual, not retrofitted.** Charter §5 Gate B: corpses "cluster where the map says **danger** lives." Prereg §5 Gate B: operationalized purely as mean-pairwise-tighter-than-random, lower-tail p<0.05 — **no danger-zone coordinates were ever specified.** The gap gandalf diagnoses exists in the charter-vs-prereg text and predates the results.
8. **No decisions-log conflict.** Grepped the log for atlas/edition/gate-b/negative-geography — no locked entry commits a prior Edition or a danger-zone finding that freeze-on-A/C/D would contradict.

**Taken on trust (not re-run — execution fidelity was elrond's, already clean per the gate report):** the MCA basis derivation itself (14-dim retention, Greenacre correction, MFA weights), Gates A/C/D internal statistics, the bootstrap/LOFO battery. I re-derived nothing upstream of the coordinates; I verified that *given* the committed coordinates, the Gate-B numbers and the neighbor evidence are correct. That is the correct scope for a ruling review — the coordinates are the frozen object under v1.1, and elrond ran zero amendments.

---

## Reasoning per question

### (a) Is the §3 diagnosis a legitimate "pinnable cause," or motivated reasoning?

**Legitimate.** Three independent tests, all passed:

- **The cause is textually locatable, not invented.** The charter chartered "danger geography"; the prereg operationalized it as undirected tightness with a directional (lower-tail) threshold. That is a specification-side mismatch present in the documents before any result existed. The prereg's own example of a pinnable cause ("a fusing error") is execution-side; gandalf is honest that his cause is a different *kind* — specification-side — but "pinnable" in the decision rule means *identifiable and non-arbitrary*, not *execution-side only*. A wrong operationalization of a correct intent is exactly as pinnable as a fusing error, and arguably more so because it is legible in the frozen text.
- **The evidence survives adversarial reproduction.** I recomputed the neighbor table from scratch; it is exact. The corpses genuinely sit among their mechanical siblings — the same projection machinery Gate A validated (ARI 0.668) and Gate D validated (bootstrap 3.6%, LOFO min 0.968). "Corpses among siblings" *does* establish projection fidelity here, because the siblings are frozen-label living kits whose placement Gate A independently certified. The dispersion is therefore a property of the *corpses being 5 different kits*, not of the map mislocating them. I could construct no reading under which 2.44 (33% above null median, with 3.69-scale inter-corpse gaps) indicates map *invalidity* rather than territory *heterogeneity* — the map places each corpse correctly; the corpses simply don't share a neighborhood.
- **The motivated-reasoning guard is satisfied by the direction of the error.** Motivated reasoning would explain away a failure to rescue a favored conclusion. Here the "favored conclusion" (a passing map) is rescued on A/C/D regardless; the diagnosis does not soften Gate B's *result* (FAIL stands, published verbatim as F-1) — it re-files the result's *meaning*. gandalf gains nothing self-serving: F-1 is a published negative finding on *either* ruling branch. That is the opposite of motivated reasoning.

**Post-hoc-evidence legitimacy (in-scope check):** the §3.2 neighbor analysis is diagnostic, not a substitute passing criterion. It is used to *explain* the failure (why dispersion is expected), never to *convert* the failure to a pass. Gate B remains FAIL. That is the legitimate use of post-hoc evidence — a permitted-and-expected part of failure diagnosis under the one-amendment-cycle clause, which explicitly contemplates a "failure diagnosis." Illegitimate use would be inventing a new nearest-neighbor *gate* post-hoc and declaring it passed; the proposal does not do that (R1 says "No new gate is invented post-hoc to replace it in this edition") — and R3 correctly defers the *replacement* criterion to a fresh v2 prereg with my review.

### (b) Does reclassification-without-re-run fit the one-amendment-cycle power, or is it gate-deletion-after-failure?

**It fits — with a rider.** The decision rule permits "one protocol-amendment cycle … IF the failure diagnosis identifies a pinnable cause." A reclassification that (i) leaves every number exactly as computed, (ii) publishes the FAIL verbatim, and (iii) invents no replacement gate for this edition, is the *minimal* amendment — strictly less invasive than a re-run, which would spend the cycle recomputing. The prereg's spirit forbids *tuning-until-pass* and *deleting a failed gate to manufacture a pass*. This does neither: A/C/D passed on their own merits with margins (ARI 0.668, R² 0.076, bootstrap 3.6%) **before** Gate B's disposition was known, so the freeze does not *depend* on removing B — it survives B's removal because the other three independently cleared.

The one hazard is precedent: "author diagnoses own gate as mis-specified, reclassifies to non-gating finding" is a template that, unguarded, could excuse any future failed gate. That is precisely why this came to me with BLOCK authority, and it is handled by the conflict-declaration + independent-review structure already in place. **RIDER-1 makes the guard explicit** (below) so the precedent is bounded, not open.

**On whether this "forces the fallback":** it does not. The fallback fires only if *no diagnosis identifies a pinnable cause*. A pinnable cause is identified (a). Therefore the amendment cycle is available and the fallback is not compelled. (Note, correctly captured in R2's tail: F-1 publishes on *either* branch; the branches differ only in whether the derived basis freezes as Edition I.)

### (c) Is freezing Edition I on A/C/D+F-1 sound given the §2 structural findings?

**Sound, conditional on the badge telling the truth — which the charter already mandates and RIDER-1 hardens.** The §2 findings (14-D diffuse space; dims 1–2 = 8.36% corrected inertia; Leiden shatter / no meso-communities; LCA k=3; cross-family ARI ≤0.23) are not *disqualifying* — they are a description of the territory: a continuum with archetype condensations, not a periodic table of boxes. Gate A proves the condensations are real where genre history predicts them; Gate D proves the whole configuration is stable (LOFO holds even dropping all 156 Diablo kits). A low dims-1–2 inertia is not a validity failure for a genuinely high-dimensional categorical space — it is the honest number, and the charter §6 already *requires* it on every render ("this plane explains X% of corrected inertia"). The soundness condition is that the badge is not cosmetic: a reader must not mistake an 8.36% two-dim view for a faithful summary. RIDER-1 binds the badge to also disclose the retained-dimension count and the "continuum, not boxes" finding, so no render implies discreteness the data denies.

This is a Discipline #12 (semantic-shift) moment and gandalf handles it correctly: the map ships as *what it is* (a stable low-dim navigation projection of a high-dim continuum), not as *what it was originally imagined to be* (a grid of discrete cells). The Q19-grid rejection is retroactively vindicated by the Leiden shatter — even derived discrete partitions don't exist at meso-scale.

### (d) Is R3 correctly placed per the second-attempt clause?

**Yes, with a clarification.** The decision rule states "A second full re-derivation attempt requires a fresh pre-registration (v2) with jack-ryan review." R3 designs the *replacement negative-validity criterion* (per-law, powered) inside that v2 prereg, after the graveyard census grows — this is exactly the right placement: it does not smuggle a new gate into Edition I, it queues it behind fresh pre-registration and fresh review, and it correctly identifies that the *reason* Gate B could not be per-law this edition (n<5/law, my A6) is a power problem that only a larger census cures. CLARIFY-1 pins the one thing R3 leaves loose (below).

---

## The A6 self-critique (in-scope; my own amendment under honest scrutiny)

gandalf asks me to consider honestly whether my A6 pooling made Gate B unfalsifiable-in-reverse, and what that means for the prereg-spirit weight the gate should now carry. My finding, having run the probe:

- **A6 did not create the reversal, and did not make the gate unfalsifiable.** The falsifiability probe (verification #5) shows a co-located corpse set *would* have cleared the pass line (1.389); the gate was falsifiable in both directions. What A6 changed was the *unit* (per-law → pooled) and the null's frame — not the *direction*. The directional, lower-tail "cluster where danger lives" framing is the **charter's**, authored before A6. So the operationalization error gandalf diagnoses is his charter-level prior; my A6 inherited that direction and applied it to a pooled set.
- **What A6 *did* do is make the directional prior more likely to fail** — because pooling five kits drawn from three distinct structural laws into one "tightness" test asks whether distinct laws co-locate, which the 38-negative taxonomy never claimed. In hindsight, the more revealing A6 form would have been to state explicitly that the pooled test is only interpretable as danger-geography *if* the red laws are a priori expected to share a region — and to flag at pin-time that the taxonomy predicts they do not. I did not write that caveat. That is a real, if modest, miss in my Gate-1 review, and I record it here rather than let it pass silently: **A6 pinned the unit and the null correctly but did not surface that the pooled directional test encoded an unstated territory assumption.** It was still a legitimate pre-registered test (falsifiable both ways); it was just testing a hypothesis the taxonomy already leaned against.
- **Consequence for prereg-spirit weight:** Gate B was a *validly pre-registered* gate (so its FAIL is real and must be published — F-1), but it was a *weak* gate in the sense that its pass condition required an unstated and taxonomy-disfavored territory fact. That is the correct amount of weight for the reclassification to carry: enough that the FAIL is honest and published, not so much that a reclassification-to-finding is treated as gate-deletion. This *strengthens* the case for R1 rather than undermining it — the gate was measuring the wrong thing, both the author (charter direction) and the reviewer (A6 unit, uncaveated) contributed to that, and the honest remedy is to publish the result as the substantive finding it actually is and design a real per-law locality gate for Edition II (R3).

---

## Amendments (binding on RATIFY)

**RIDER-1 (binds R1 + R2, and the charter render) — the badge and the F-1 publication must jointly prevent the map from over-claiming.** Two specific requirements, both within gandalf's authorship tier (doc-tier, ADR-002):
1. The inertia badge (charter §6) must disclose, on every render, not only "X% of corrected inertia" but also **the retained-dimension count (14)** and a one-line "continuum with condensations, not discrete cells" statement — so no reader mistakes the 2-D view (8.36%) for a faithful summary of a 14-D space. (Discipline #12 — the semantic shift from "grid" to "continuum projection" must be visible, not buried.)
2. F-1's published text must retain the phrase that its *consequence* is "the unexplored ghost field contains **no forbidden zones** derived from corpse-geography" — i.e., F-1 must not be quietly downgradable later into a soft danger-heuristic. The finding is a *negative* result about geography; it must be published as one so that a future Edition cannot cite "we always knew death was geographic."

Rationale: this is the precedent-guard for (b). It makes the reclassification honest-in-perpetuity — the map ships with its limits on its face, and the failed gate is preserved as a published negative finding, not memory-holed.

**CLARIFY-1 (binds R3) — pin the second-attempt trigger and the power target.** R3 says the replacement criterion is designed "once the graveyard census grows." Before Edition-II derivation runs, the v2 prereg must state (for my review) **the minimum per-law corpse count that makes a per-law locality test powered** (a stated n-per-law and the power calculation behind it), and **the census-growth trigger** (which Legolas re-crawl deliverable, and what count, unlocks it). Rationale: "grows" is unpinned; without a pre-committed power target and trigger, Edition-II Gate B risks the same n<5 under-power that forced A6's pooling this round. This is Review-Principle #1 (the math justifying the threshold must exist before the code runs) applied to the *next* edition, pre-emptively.

Both amendments are specification-tightening within gandalf's doc-tier authority; neither requires Matt escalation to *apply* (Matt's ratification is owed at the Edition-I freeze, not at these edits).

---

## What I did NOT flag (so gandalf can trust the silence)

- **Execution fidelity.** Not re-audited — elrond ran v1.1 with zero amendments, seed pinned, N=469 exact, label table byte-verified, Leiden confirmed true CPM (A7 honored). I re-derived nothing upstream of the coordinates because nothing upstream is in dispute; the ruling concerns the *interpretation* of frozen numbers, and the numbers reproduce.
- **A/C/D thresholds.** All passed with genuine margins (ARI 0.668 vs 0.6; R² 0.076 vs 0.15 with PERMDISP p=0.066 → interpretable; bootstrap 3.6% vs 10%; worst LOFO 0.968 vs 0.85). These are non-vacuous bars clearing non-vacuously. No re-litigation.
- **The 37-vs-38 reconciliation.** Correct documented data-state, matches my Gate-1 A6 note; `vs-golden-egg-scaling` is legitimately outside the combat denominator. No denominator drift.
- **The conflict declaration itself.** gandalf declared the COI in the header and routed to me with BLOCK authority before Matt. That is exactly the pre-registration guard working as designed; I note it approvingly rather than treating self-diagnosis as automatically suspect — the safeguard is *independent review*, which is what this is, not *prohibition of self-diagnosis*.
- **The fallback branch.** Correctly specified (exact lattice at meso-grain as census dashboard + F-1) and correctly made available only on a BLOCK. Not triggered here.
- **Naming/axis work.** Out of scope for this ruling; happens at freeze under Matt, from loadings, placeholder-names-banned per charter §6. No comment owed now.

---

## Action

- [ ] gandalf (SPEC-AUTHOR): apply RIDER-1 (badge discloses 14-dim + continuum statement; F-1 published as a negative-geography finding, non-downgradable) and CLARIFY-1 (v2 prereg pins per-law power target + census-growth trigger) — both doc-tier, no Matt escalation to apply. Then the package goes to Matt.
- [ ] Matt (ratification owed — this is the freeze decision, my tier ends here per ADR-002 + charter §9): ratify (or decline) the **Edition-I freeze on A/C/D+F-1**. The *ruling* is cleared by this review; the *freeze* is yours. If you decline the freeze, the fallback surface (exact lattice at meso-grain + F-1) is the alternative — F-1 publishes either way.
- [ ] KR: on Matt's freeze ratification, the decisions-log entry owed by the charter (`2026-07-14: Atlas derivation charter adopted`) should be extended with a Gate-B-ruling row — I draft it per standing protocol once Matt rules.

## References

- `agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-b-diagnosis-and-proposed-ruling.md` (69594f4c) — review object
- `agentic_orchestration/research/curated/atlas/2026-07-14-gate-report.md` — elrond numbers (reproduced: neighbor table, Gate-B stat, secondary, 37-vs-38)
- `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (v1.1, 63f32817) — the pinned contract; §5 Gate B operationalization; decision rule
- `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` — charter §5 Gate B ("danger"), §6 inertia badge, §10 fallback clause
- `agentic_orchestration/research/curated/atlas/atlas-coordinates-active.csv` + `atlas-coordinates-supplementary.csv` — the frozen coordinates I recomputed against (14-D, gateA_group, death_class)
- `agentic_orchestration/qa/findings/2026-07-14-gate1-atlas-derivation-prereg.md` — my prior Gate-1 (A1–A7); A6 self-critique grounded here
- Verification scripts run this session (read-only, transient `/tmp`): neighbor-identity reproduction; Gate-B pooled permutation reproduction; falsifiability-in-reverse probe. Every number regenerates from the two committed CSVs.
