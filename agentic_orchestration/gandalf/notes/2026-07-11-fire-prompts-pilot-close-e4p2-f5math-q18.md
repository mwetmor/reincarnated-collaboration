# Fire prompts — pilot CLOSE · E4 PHASE-2 · F5 math note · Q18 apply

> **STATUS:** RELAY BRIEFS — authored gandalf 2026-07-11 on Matt's "yes write prompts for each."
> Four paste-able prompts, one per lane. Each is self-contained (target session has zero context
> from the gandalf terminal session). **Fire order:** Prompt 1 first (its close record is Prompt
> 2's gate). Prompts 2 and 3 are both gamora-seam — **one gamora unit in flight at a time**; KR's
> slot call which goes first. Prompt 4 is CONDITIONAL — pasting it IS the Q18 ruling (ADR-006);
> hold it until Matt wants the production apply. Same relay pattern as the Glance v1.5/v1.6/v1.9
> briefs: paste the block, or fire the pointer *"Read
> `agentic_orchestration/gandalf/notes/2026-07-11-fire-prompts-pilot-close-e4p2-f5math-q18.md`
> §N and execute it."*

---

## PROMPT 1 — Pilot session CLOSE (paste into the OPEN pilot KR session)

**When:** now. **Target:** the open pilot KR/gamora session (Session 1). Pasting this lifts the
2026-07-11 handoff's "do not close" serialization law — this message is Matt's authorization.

```
KR — Matt authorizes the pilot session CLOSE. Execute the three-item close protocol, then this
session's stewardship ends. Context: the Leg-i completion-build (a63aae2) + Gate-2 PASS (released
via Q13) landed 2026-07-08; the per-axis ladder it gated is four deep on the main line (E1
bfc94eb · C3 e1fe99e · E2 d99635a · E3 chain 2026-07-11) + E4 PHASE-1 co-signed. Nothing this
session stewards remains unexternalized. The three items:

1. RESTORE the overwritten record. Engine tree shows
   src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json MODIFIED: an E3-window
   smoke run (generated_at 2026-07-11T07:35Z, seed 55000000, n=5, 70s, 5/5 pass) OVERWROTE the
   §8-A1 measurement of record (seed 56000000, n=18, 0/18, 2026-07-08) at its on-disk path.
   Verify that provenance in the diff first, then `git restore` the file — the committed version
   (dfbea76) IS the record. Carry a hygiene flag into the close record: smoke/test runs must not
   write to measurement-of-record output paths (star-lord/gamora, fix on next touch,
   non-blocking).

2. CLEAR closed-chain residue (NARROW scope — these two paths only, both verified untracked):
   src/reincarnated/output/variation_pilot_generation_checkpoint.json and
   src/reincarnated/simulation/output/pilot/. The variation chain closed 2026-07-06 (jack-ryan
   light read db2df69); checkpoints for a closed chain are dead weight; the records live in
   simulation/notes/ + the TRACKED output/variation_pilot_measurement_report.json (KEEP — record
   of record). Verify untracked status (git ls-files) before removal. Do NOT touch any other
   untracked output/ residue — general output-tree hygiene is a separate star-lord item, not this
   close.

3. CLOSE-OUT RECORD, dual-write: (a) append a SESSION-CLOSE record to
   agentic_orchestration/dispatches/2026-07-08-gamora-leg-i-pilot-fire.md; (b) prepend a delta to
   canonical/current-to-end-state/current-to-end-state-engine.md stating verbatim: "pilot session
   CLOSED → E4 PHASE-2 unblocked" — gamora's E4 dispatch §0 gate resolves on this exact signal.
   Both records carry the distinction: closing the session ≠ retiring the instrument — the
   two-arm driver + per-axis model + pilot_policy rider persist in code + policy; every future
   axis run fires on the standing instrument from fresh sessions.

Commit per the auto-commit addendum; push per the established pattern. NO content runs, NO new
work in this session after the close record lands.
```

## PROMPT 2 — E4 PHASE-2 sim build (fresh KR session, AFTER Prompt 1's close is visible)

**When:** after the engine-tracker close delta exists. **Target:** a fresh KR session.

```
KR — one job: fire gamora on E4 PHASE-2 (the commitment-axis sim build). Read
agentic_orchestration/dispatches/2026-07-10-gamora-commitment-axis-E4.md in full. PHASE 1
(math-note co-sign, 56e1eb4) is DONE; PHASE 2 is the sim build (cast-state machine · tick
resolution · drain + pay-on-commit · move-while-channel enum · cumulative break threshold ·
ramp + break-reset · interrupt RULE v1). Its §0 gate ("queues behind the pilot completion-build
landing") is RESOLVED: completion-build a63aae2 + Gate-2 (via Q13) landed 2026-07-08, and the
pilot close record in canonical/current-to-end-state/current-to-end-state-engine.md ("pilot
session CLOSED → E4 PHASE-2 unblocked", 2026-07-11) is the explicit signal. VERIFY that close
record exists before firing; if absent, STOP — the close has not landed. Constraints: one gamora
unit in flight at a time (if the F5 math-note unit is out, hold until it returns — KR's slot
call); jack-ryan Gate-2 on the build's return; NO content runs beyond what the dispatch itself
authorizes. Downstream note for the dispatch record: the ninth-axis measurement half (ii) unblocks
when PHASE-2 lands.
```

## PROMPT 3 — F5 cost-TYPE math note (KR session; $0, notes-only, gamora)

**When:** any time; serialize against Prompt 2's gamora unit. **Target:** a KR session.

```
KR — one job: dispatch gamora to author the F5 cost-TYPE math note (notes-only, $0, NO sim code,
NO runs). Context: Matt ruled the F5 forks 2026-07-11 — Q1(a) floor-guarded HP costs · Q2 BOTH
seats (K26 Blood Mage/Martyr at the WIS base seat + K29 Necromantic Blood Mage at INT via the T4
RESOURCE_CONVERSION door) · Q3(a) K-sequential; roster K26–K29; denominator 35; build CLEAR with
the math note FIRST. gamora reads
agentic_orchestration/gandalf/notes/2026-07-11-f5-cost-type-axis-design-note.md (header + §7
roster + §8 + §9 carry the rulings) and authors the math note pinning the four §8 items:
(1) HP-floor semantics at _take_action — cast REFUSED when HP cannot cover the cost, mirroring
the combatant.py:409 mana gate; ONE deduction branch that both doors inherit (K26 base-native +
K29 T4 t4_cost_resource: HP);
(2) damage-taken event grain for the on_damage_taken builder (K27);
(3) charge-pool arity + the active-spender law (K27/K28 — anti-Invoker STRUCTURAL: charges must
be SPENT by an action, never passively drained);
(4) byte-guard scope — existing-population byte-identity when no F5 field is present.
Constraints: one gamora unit in flight at a time (serialize against E4 PHASE-2 — KR's slot call
which goes first). On landing: Gate-1 critique-pair (jack-ryan + gandalf — cost-model semantics
are class-fantasy surface, per the proxy-calibration-note precedent), THEN the F5 build
sequencing returns to KR.
```

## PROMPT 4 — Q18 production apply (CONDITIONAL — pasting this IS the Q18 ruling)

**When:** only when Matt wants the production migration applied (ADR-006 — his paste is the
authorization; Q18 is non-blocking until then). **Target:** a KR session (star-lord dispatch).

```
KR — Matt rules Q18 APPLY; this message is the ADR-006 authorization for ONE production-DB write.
One job: dispatch star-lord to apply the v2.21 telemetry migration to the PRODUCTION telemetry DB
per engine src/reincarnated/telemetry/MIGRATION.md §v2.21 (E3 attribution spine: two additive
NULL-able columns on spatial_fight_results — output_by_element_json + killing_element; landed
brownfield-safe, smoke 10/10, PHASE-4 round-trip drift 0.00e+00; star-lord acb3397 + d702616).
Discipline: (1) snapshot/backup the production DB file BEFORE the apply; (2) run the §v2.21 apply
exactly as documented — no improvisation; (3) post-apply verification per the MIGRATION doc
(pre-v2.21 rows read NULL both columns — zero data loss, zero semantic shift); (4) close the Q18
row in canonical/matt_decision_needed/README.md (ruled + date) and note the apply in the engine
tracker delta. Unblocks: v2.21-consuming production-telemetry runs + the C-5 rate-band cert wave.
NO other production writes under this authorization.
```

---

**Signed:** gandalf, 2026-07-11. Sources verified this session: engine git status (dirty file
diff provenance + untracked paths + tracked report), `telemetry/MIGRATION.md` §v2.21,
`2026-07-10-gamora-commitment-axis-E4.md` §0, `2026-07-08-gamora-leg-i-pilot-fire.md` SESSION-60
record, `variation-pilot-run-state-2026-07-06.md` (chain CLOSED), `batch2-run-state-2026-07-06.md`
(batch-2 rests at Matt's 07-08 lock — not the pilot's).
