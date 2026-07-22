# Finding — 2026-07-22 — tier3-encounter-geometry-run (Gate-1 launch)

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1 launch gate; peer review, pre-fire)
**Severity:** PASS-WITH-CONCERNS
**Target:** Charter v1.1 — `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log/committed-truth as truth); Disciplines #1, #18, #46; desirable-run-pattern §3 fit-test / §4 halt-taxonomy / §5 standing-safeties.

## Verdict

**PASS-WITH-CONCERNS.** The run may FIRE. Charter v1.1 fits the desirable-run-pattern honestly: decision-space genuinely pre-drained (all forks + second ruling batch ruled same-day; Appendix B verified against `canon_corpus` read-only), codomain count-checkable, RD-1 conditional respects the §8 honorable fallback rather than fighting it. Three concerns, **all processable in-run** by gates already present in the charter — none is a launch BLOCK.

## Concerns (each processable in-run)

**C1 — WARN — prereg Y-basis (processable at PREREG BEAT, my check before W3).** T3-F4/§4 pin X (effect-size) AND Y (direction-consistency %) "from gamora baseline variance." Variance data grounds X cleanly under Discipline #18 (methodology chosen against real variance, not guessed — #18.2 pre-execution timing honored). It does not obviously ground Y, a consistency percentage. The prereg doc must state Y's derivation basis separately, or Y is the one un-pinned goalpost. Caught at my prereg gate.

**C2 — INFO — freeze/derivation boundary (processable at W0 census, my Gate-2 on W0 close).** §4 W0 done-predicate includes "SUBSTRATE FREEZE + census published," but the freeze/derivation boundary lives only inside the done-predicate, not as a hard handoff gate. Recommend the census publication BE the W0→W1 handoff artifact so no derivation can race the freeze (Discipline #46 / pattern §1 frozen-at-launch). Enforced at my W0 Gate-2.

**C3 — INFO — kin-guarantee × guest-family edge (processable in-run; out of W0-W4 scope).** §1 parks IDENTITY-GAUGE + MINION-PET catalogue-only, but R-b3's kin-guarantee could surface a become->guest-family case (guest family has no native act presence AND no traveling-kin ruling for guests). Not W0-W4 scope; flag for the story fold, not the run.

## One-line findings (a)-(g)

- **(a) Fit-test 4/4 — HONEST.** F1 enumerable (record-267 spine countable; quota [15,30] bounds harvest; family tables finite/diffable — Appendix B IS the diff). F2 decidable (§4 predicates are counts + schema-asserts + runs-without-error; zero quality-feelings). Cite: pattern §3, Discipline #1.
- **(b) Prereg — un-gameable on X, thin on Y.** X-after-baseline correct per #18/#18.2. Y-derivation the soft spot (C1).
- **(c) Commitment-boundaries §5 — COMPLETE.** Naming / ratification / act-order / island build-out / amendments / taste / atlas+Edition all reserved. Only silent-inference risk is the guest-family kin edge (C3), out of run scope.
- **(d) RD-1 conditionality T3-V6 — RESPECTS the fallback.** "Fires ONLY on W3 PASS, VOID on FAIL" is the §8-C honorable fallback in conditional-leg clothes. No forced march; a FAIL ships grammar-as-scaffolding. Clean.
- **(e) T3-V1..V7 ledger — COHERENT.** No internal contradiction. V4 (kin exempt / hostile era-pure) composes with V6 (RD-1 roster under V2); V7 one-way coupling consistent with V6's no-star-lord-code. V3 over-quota-logs-as-admission enforces substrate-votes.
- **(f) W0 freeze — SOUND, one seam to tighten.** Quota + freeze-before-derivation + census is right; only leak is boundary-as-done-predicate not hard-gate (C2). Cite: pattern §1, Discipline #46.
- **(g) Braid coupling T3-V7 + brief §4 — GENUINELY one-way.** No shared files (distinct namespaces; no-push sub-agent briefs), no shared schema MUTATION (Lane-1 reads frozen W1 schema; Tier-3 never reads the emission tracker), no ordering dependency (Tier-3 never blocks on either lane; RD-1 is Lane-1's future fixture, not blocker). `encounters`-key reservation is Lane-1's to honor, one-way. Clean.

## Action

- [x] jack-ryan: Gate-1 PASS-WITH-CONCERNS returned inline to conductor; run cleared to fire.
- [ ] Conductor (gandalf): at PREREG BEAT, state Y's derivation basis separately in the prereg doc (C1) before routing to my prereg check.
- [ ] Conductor (gandalf): make the W0 census file the explicit W0->W1 handoff artifact (C2).
- [ ] jack-ryan (in-run): prereg check before W3 (verifies C1 resolved); Gate-2 on W0 close (verifies C2 freeze integrity); Gate-2 on in-run reclassifications + T3-F4 gate rulings per charter §8.
- [ ] Story fold (future): kin-guarantee × guest-family edge (C3) — not this run.

## References

- `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` (v1.1 — review object)
- `agentic_orchestration/operating-procedures/desirable-run-pattern.md` (§3/§4/§5)
- `canonical/matt_decision_needed/2026-07-22-tier3-encounter-geometry-charter-grill.md` (consumed elicitation; Appendix A/B)
- `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` (§4 braid mirror)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #18 line 455; #46; #18.2)
- Lineage precedent: `agentic_orchestration/qa/findings/2026-07-14-gate1-atlas-derivation-prereg.md` (Run A launch gate)

**Signed:** jack-ryan, 2026-07-22.
