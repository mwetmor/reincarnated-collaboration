# KR session-opener — DoT-as-boss-bridge Phase-1 diagnostic routing

**Type:** gandalf-authored session-opener prompt for a NEW knight-rider session (Matt-chosen "new session" path over injecting into the live role-floor-validation run).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-15 — *"please write the prompt for the new KR session."*
**Routes:** `agentic_orchestration/gandalf/notes/2026-06-15-dot-as-boss-bridge-investigation-brief.md` (the falsifiable Option-1 diagnostic).

---

## How to use

Paste everything in the fenced block below as the FIRST message to a fresh `knight-rider` session
(`cd ~/Games/reincarnated-collaboration && claude --agent knight-rider`). It is self-contained.

---

```
Run session-start per your OP § 1 (ground-state → roadmap → in-flight dispatches → own latest notes). Then route the work below. Do NOT inject this into the live role-floor-validation run — it is its own scoped read-only investigation (rationale in the sequencing section).

== CONTEXT (WS1 — rogue boss-efficacy arc) ==
The rogue-degeneracy architectural arc CLOSED on evidence: the constraint is KIT COMPOSITION, not architecture and not genre-correct fragility. Lever C verdict: the envelope rogue lands ZERO boss/elite/mini_boss kills even at M=1.0 (above the 0.65-killable calibration), while b6 clears the boss at 0.967 with the SAME role histogram {def:1, mob:2, area:4, burst:1} — by cranking power_tier to 58. So b6 "solves" the boss with a power-stat brute-force, not a composition insight. Matt's prompt: "Could it be that we have not yet included physical ailments?" Engine read (gandalf grep): bleed EXISTS as the physical DoT (config/ailments.yaml; element_biases.py:70 physical→bleed; gear affix magnitude 0.12; ticks every second at 35% base application); poison does NOT exist (P2 candidate, not added). DoT family today = burn/bleed/drain.

== THE HYPOTHESIS ==
DoT DPS scales with single-target fight DURATION (swarm dies in ~2s → bleed barely ticks → swarm damage is hits; boss runs 30s+ → bleed stacks accumulate → boss damage is the DoT). So ONE rogue kit could be swarm-strong-via-hits AND boss-strong-via-DoT with no per-tier modifiers — the genre-correct rogue identity (PoE poison/bleed assassins, Last Epoch DoT-rogues bridge exactly this trash→pinnacle gap). This COMPLEMENTS the role-floor work (role floor guarantees the burst SLOT exists = count; DoT is the EFFICACY mechanism that makes the slot actually kill bosses). It does NOT compete with it.

== THE TASK — route the Phase-1 diagnostic (READ-ONLY) ==
Brief: agentic_orchestration/gandalf/notes/2026-06-15-dot-as-boss-bridge-investigation-brief.md (read it; route per its §6).
Three questions, one pass, falsifiable:
- Q1 (gamora, sim read): does b6 kill the boss via DoT TICKS or via brute-force DIRECT HITS at power_tier 58?  [gandalf bet: brute-force]
- Q2 (rocket, composition read): does the envelope rogue's kit even SELECT bleed/DoT skills+affixes?  [bet: likely not / weakly]
- Q3 (rocket read + gandalf design-judgment): is bleed magnitude 0.12 FLAVOR-tier (small bonus on top of hits) or PRIMARY-tier (can carry a boss fight as the main damage source)?  [bet: flavor-tier]
gandalf owns the design-judgment on the "primary-tier" target + which decision-tree branch we land in + whether a re-scope is warranted. rocket/gamora own the engine read (what the code actually does) — do NOT pre-impose the fix; read first.

== SEQUENCING (load-bearing — clean attribution) ==
- The DIAGNOSTIC is read-only: it changes nothing in the sim or generation, so it shifts NO win-rate and is SAFE TO RUN CONCURRENTLY with the in-flight b6/rogue role-floor chain. It does NOT confound the G7 HOLD-SIM WR re-pass. Fire it as its own scoped read.
- Any RESULTING BALANCE CHANGE (DoT-selection re-bias and/or bleed-magnitude scale) sequences AFTER the in-flight role-floor chain + its G7 WR re-pass CLOSES — same one-variable-at-a-time discipline; we do not land a WR-shifting bleed change mid-validation or we can't attribute the result.
- Bleed-magnitude is a gandalf-locked tuning constant (Discipline #16): any eventual re-scope needs sign-off — out of scope for the diagnostic; in scope only if the read warrants it AND it sequences as above.

== ACCEPTANCE ==
The three questions answered with code/sim EVIDENCE + the decision-tree branch named. This is NOT a balance change — that's a separate, sequenced follow-on gated on the read.
FALSIFIER (keep it honest): if the rogue ALREADY selects DoT AND it's already primary-magnitude AND it still lands zero boss kills → the hypothesis is FALSIFIED, DoT is NOT the lever, and Option 2 (b6-as-net / power-composition writ large) strengthens. Report that plainly; do not force the DoT narrative.

Report back the branch + the evidence when the read returns; hold any balance change for post-role-floor clean attribution.
```

---

**Signed:** gandalf, 2026-06-15
**For:** the paste-able session-opener that stands up a fresh KR session to route the read-only DoT-as-boss-bridge Phase-1 diagnostic (Q1 gamora b6 kill-mechanism, Q2 rocket rogue-DoT-selection, Q3 rocket+gandalf bleed flavor-vs-primary), with the load-bearing sequencing constraint (read-only = concurrent-safe, no G7 WR confound; any balance change sequences after the role-floor re-pass) and the real falsifier (DoT already selected+primary+still failing → not the lever → Option 2 strengthens).
