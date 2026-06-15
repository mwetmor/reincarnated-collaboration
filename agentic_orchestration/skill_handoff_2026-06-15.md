# Skill handoff — 2026-06-15 (knight-rider)

## Session focus: rogue-degeneracy → architectural-hypothesis arc — CLOSED on evidence; constraint is kit-composition (boss efficacy). Pushed both repos.

Drove a four-step recognition→validate→commit investigation that converged on a clean, bounded answer to the weapon-as-envelope rogue degeneracy. The architectural single-global-modifier hypothesis is **RULED OUT on evidence**; the real constraint is a **kit-composition deficiency** (the envelope rogue kit lacks boss efficacy the legacy b6 template has). All gates cleared, both repos pushed.

## The arc (recognition → validate → commit, each step gated)

1. **Role-floor fix (rocket).** gandalf diagnosed the envelope composer dropped b6's role-composition floor (no `defensive` emission, no sub-60 `burst`). rocket built a coordinate-derived floor in `compose_physical_kit_envelope`. Gate-1 CLEAR-W/-AMENDMENTS (`c41f909`) → Gate-2 PASS-W/-INFO (`5041949`). Tag `rocket/v2.2-envelope-role-floor` (`52703c9`). The rogue cell now composes `{defensive:1, mobility:2, area:4, burst:1}` vs the audit's 0/0. **Result: NECESSARY but INSUFFICIENT** — gamora's G7 rogue re-fire (`d003f8f`, Gate-2 PASS `aa2b8e7`) showed the floor fires in-sim yet swarm stays pinned at 1.0 → modifier floors to 0.0719 → upper tiers still crater.
2. **Swarm-coverage architectural spike (gamora).** Tested gandalf's located lever: a spatial-arena-derived coverage cost (NOT an AoE-share proxy — the falsified lever). Gate-1 on dispatch (`f96fad4`) + mandatory Gate-1 on mechanic+criterion (`120eb93`, decisive anti-AoE-proxy check held under independent code scrutiny). Flag-gated, OFF-byte-identical. Tag `gamora/v1.0-swarm-coverage-spike` (`0b34432`). **Result: HONEST_FAIL — informative shape.** The mechanic is a *real* encounter lever (ON/OFF deltas bite), but no swept value clears the conjunctive criterion; convergence settles at a feedback equilibrium (swarm 0.833 / modifier 0.1333 / upper tiers 0.0). Gate-2 PASS-W/-INFO (`0793aa2`). **RELOCATED the gap to the upper-tier side** — the crater is NOT solely a swarm-suppression artifact.
3. **Lever C disambiguation (gamora).** Cheap decisive probe: can the floored rogue kit clear upper tiers at a HEALTHY modifier held by fiat (swarm set aside)? Gate-1 re-pivoted the architecture-discriminator from M=1.0 (generous brute-force, false-positive risk) to **M=0.30** (`8d3bb0e`). Tag `gamora/v1.x-lever-c-disambiguation` (`01da930`). **Result: C-2 (KIT-COMPOSITION).** Zero boss kills at BOTH M=0.30 and M=1.0 (n=60, clean zero; jack-ryan independently re-ran to confirm it's not a "fight-never-ran" defect — rogue deals ~192 mean dmg vs a 123,356-HP boss that ends every fight at 100% HP). Elite + mini_boss also 0.0; only magic clears. Gate-2 PASS (`2106e10`). **The single global modifier was NEVER the constraint.**

## Disposition (gandalf, recognition record § 6-octies / § 6-novies / § 6-decies)

- **Architectural single-global-modifier hypothesis: CLOSED — RULED OUT.** Option 2 (per-tier modifiers / second degree of freedom) is OFF the table on evidence.
- **It's a composition DEFICIENCY, not acceptable genre-correct fragility.** Zero-at-M=1.0 (above the engine's 0.65-killable boss calibration) is past the knife's-edge fragility line. b6's 0.967 boss-clear at the SAME archetype + SAME role-floor counts is the genre-CORRECT shape — the envelope is strictly worse than a proven-good baseline at the same role histogram.
- **Count-vs-efficacy located.** The role floor is a role-PRESENCE guarantee, CORRECTLY scoped. Boss EFFICACY is a SEPARATE second composer layer, now isolated for the first time (the envelope filled the burst *slot*; b6 filled it with a burst that *works on boss* — power_tier 58 + geometry selections + kit_size 13). Do NOT bolt efficacy onto the presence floor.
- **Decision 2 (b6 deletion): HELD, b6 stays WHOLE — UPGRADED from "net" to "SPEC."** b6 is the in-tree worked example (answer key) of the boss-efficacy the envelope must match before b6 can go. The deletion gate is now a **bounded composer fix**, not an open architecture conversation.

## Push (Matt authorized "push and wind down")

- ENGINE: `d003f8f..01da930` (role-floor impl + rogue re-fire + swarm-coverage spike + Lever C) + tags `rocket/v2.2-envelope-role-floor`, `gamora/v1.0-swarm-coverage-spike`, `gamora/v1.x-b6-deletion-prereq-B-rogue-refire`, `gamora/v1.x-lever-c-disambiguation`, `gamora/v1.x-b6-reshape-hot-caster-followup`.
- COLLAB: `e431c70..3d363bf` (rogue-arc dispatches + all Gate-1/Gate-2 findings + gandalf's three dispositions + canon § 6-octies/novies/decies; ALSO parallel galadriel/gandalf drax descent-scene + iteration briefs — independent workstream, legitimately committed).
- Both repos verified pushed.

## Deferred / open (carry-forward, with empirical re-open criteria)

- **DECISION IN FRONT OF MATT (the arc's terminus):** two options, his call — (1) **bounded rocket composition investigation** into envelope boss-efficacy vs b6 (gandalf's recommendation; cheap *because b6 is the answer key* — a diff against a worked example, not an open search; this is also the path that eventually retires b6); or (2) **accept the deficiency, routed around by b6, and move on** (honest, *provided* named as a deficiency, not as genre-correct fragility). gandalf authored a follow-on "DoT-as-boss-bridge investigation brief" (`81285d7`) framing the falsifiable form of Option 1. NOT yet authorized — awaiting Matt's pick.
- **b6 deletion (Decision 2): re-open criterion is now CONCRETE** — the envelope composer must achieve b6-parity boss efficacy on the rogue cell (re-pass G7 HOLD-SIM upper tiers). Until then b6 stays whole as the boss-capable spec.
- **Caster-side generalization: STILL-OPEN** (untouched this arc; § 6-septies). The role-floor diagnosis confirmed on the physical side; caster generalization remains located-but-unprobed.
- **Process INFO (jack-ryan, standing):** stash mutable working-tree state (cycle-14 gear/monster JSON, telemetry.db) before any same-seed reproduction-anchored sim run — that dirty tree perturbs determinism at the noise floor (it caused the non-load-bearing magic/b6 jitter in the spike's §5 anchor; ruled non-dispositive).

## Routing notes for next session

- The rogue arc is a model of the prove-then-commit discipline: every step (fix, spike, probe) gated its destructive/architectural conclusion behind a math-note → mandatory Gate-1 on the *criterion/mechanic* (the decisive act) → run → Gate-2. The Gate-1-on-criterion caught two real force-pass surfaces (the AoE-proxy mechanic; the M=1.0 false-architecture verdict). Keep this pattern for any future architectural probe.
- An infra stream-timeout killed an uncommitted gamora math-note mid-arc (recovered: the file survived on disk, gamora re-committed it). Durability-first (commit before long runs) held everywhere else. For long sweeps, instruct incremental/coarse-first commits.
- Parallel non-arc work landed on collab this session: galadriel re-scores + gandalf drax briefs for the dark-fantasy descent scene (iteration 1 → iter2fix; `3d363bf` validates gandalf's §4 gold-over-green prediction). Independent of the rogue arc; drax/galadriel/gandalf loop.
