# RUN U11-BUILD — SEAL REPORT

**Sealed:** 2026-08-25T16:40Z · **Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** Matt 2026-08-25, verbatim: *"yes, let's adopt U-11. Please run it here."*
**Run instrument:** `agentic_orchestration/gandalf/notes/2026-08-25-u11-build-run-ledger.md` (L-1…L-7)
**Spec of record:** `agentic_orchestration/workflow-upgrades.md` § U-11 (ADOPTED at launch; SEALED this fold)
**Gate record:** `agentic_orchestration/qa/findings/2026-08-25-u11-gate.md` (G-U11 BLOCK ×3 · G-U11b PASS-WITH-FINDINGS)
**Seal predicate:** T1–T5 **ALL ✓**. Tape rows of record: START `6947081163daa341` · CLOSE `3a6b27b3a61f4b4e` (`run:U11-BUILD`, verdict PASS-WITH-FINDINGS, gatekeeper jack-ryan).

---

## 1 · The empirical criterion, demonstrated (verbatim from the spec: "Claude lanes render token + cache-hit% beside Codex's on the same board")

From `flight/report.md`, derived from rows, zero prose sources:

| provider / lane | units | tok-in | cache-hit | tok-out |
|---|---|---|---|---|
| **anthropic (claude lanes)** | 29 | **8,442.5M** | **97.6%** | **50.9M** |
| openai / gpt-5.6-sol@xhigh (codex) | 30 | 72.4M | 93.2% | 259K |

**The fleet's primary economy stopped rendering as a null.** August's Claude lanes: 8.44B input tokens across 27 quiescent sessions (49,590 API calls), 97.58% cache-hit, 50.9M output. **U-3's criterion is now a per-lane query** — when Matt sets `ENABLE_PROMPT_CACHING_1H=1` (`matt_to_do/`, still open), the before/after lands on this exact column.

## 2 · What was built (blocks + gates)

- **star-lord B-1** (`7f71ee5b`): read-only ingester `flight/claude_usage.py` + `bin/ingest_claude_usage` — session-grain rows folding each session's `subagents/` tree in (R-1); quiescence-bounded live substrate (R-6, idempotence proven on the live tape); workstream honest-null 27/27 (R-3 fallback, no inference leaked); `backfill:true` throughout (R-4); schema v1.1 untouched (R-5).
- **jack-ryan G-U11** (`cda4a2d8`): **BLOCK ×3** — tokens_output under-reported 62% (placeholder first-lines), Python renders correction-blind, `reasoning | 0` for an absent axis. Plus: F-1 tokens_input-as-sum RATIFIED byte-exact; rev-1.2 provenance trigger NOT FIRED (restated: fires when `backfill:false` would be a *positive claim* of instrumented capture); F-6 synthetic zeros verified measured-not-null.
- **star-lord B-2** (`4ea4f820`): terminal-usage selector (input axes byte-invariant; output 19.3M → **50,878,369**); `schema.fold` applies corrections FIRST (R-8) — board inherits by DELETING its duplicate arithmetic; `or 0` template grep-banned; 16 correction rows (R-9: emitted iff a value moved — the builder HELD for a ruling rather than emit 11 false amendments).
- **jack-ryan G-U11b** (`c3a3ca3c`): all BLOCKs discharged by independent four-selector re-derivation; 5 mutations all bitten; **PASS-WITH-FINDINGS — T4**.
- **star-lord B-3/B-3b** (`57e78e0c`+`e197e03c`): lifecycle rows; **R-8 consumer clause + R-9 emitter clause landed in SCHEMA.md § 0 rule 1** (jack-ryan-verbatim); R-9 falsifier pinned.
- **Suite at seal:** flight 131/131 · board 18 · glance 128/128 · validator 0/120 · retrospection 33/0 · append-only clean all ranges.

## 3 · Run-law findings worth keeping

1. **The gate charged itself and the law held.** G-U11's "under-reported on 27/27 rows" was a lane-grain fact written at row grain (16 differed, 11 identical) — derived-summary defect class, gate layer, second occurrence. jack-ryan's own sentence: *had star-lord complied instead of re-deriving, 11 false amendments would be permanent on an append-only tape.* **Derive-don't-comply (U1 WARN-5) just paid out against the GATE.**
2. **R-8 + R-9 are now the tape's first rule:** consumers fold corrections before deriving (the Glance `buildFleet` path was already the reference); emitters correct iff a measured value moved. Both jack-ryan-worded, SCHEMA.md § 0 — one spelling, no engineering-disciplines copy (R-8's own anti-drift logic applied to itself).
3. **INFO-6:** a grep ban is a tripwire, not a guarantee — single-quote spelling evaded it; the behavioural falsifier bit. Test-design principle for every future template-ban.
4. **INFO-7:** the gatekeeper nearly filed a false finding by feeding the auditor correction-blind inputs — 40 minutes after ruling on correction-blind consumers. The defect class recurses into its own tooling; named and self-charged.
5. **Honest-null's newest face:** measured zeros (synthetic probes) vs nulls-as-zeros vs `or 0` manufacture — three adjacent cases, all now discriminated in code and tests.

## 4 · Governance candidates (Matt rules adoption)

1. **Durable session-attribution (F-5):** 0/27 rows could be workstream-mapped — the mechanical index works, but *nothing durable records which session did which work* (custody rows are the only session-id-bearing artifacts, and only one carried a real fragment). Candidate: session-id in completion records / custody rows as standing discipline. Until adopted, Claude rows stay lane-attributed, workstream honest-null.
2. **R-9 → standing tape law** — ✓ effectively done (SCHEMA.md § 0 clause, gate-ratified); listed here because both R-8 and R-9 were conductor-ruled veto-open: **Matt's veto surface** = the two § 0 clauses + the `--correct-unchanged` lever (emit-all-27 exists if he overrules R-9).
3. **Derived-summary discipline** (U1 candidate #2) gains its **sixth exhibit** (the gate's own "27/27") — the case for engineering-disciplines graduation strengthens.

## 5 · Handoffs out of the run

- **→ drax (post-run backlog):** WARN-6 — Glance's *exported* `fold` is correction-blind by default (live pipeline correct; standalone consumers at hazard); **WARN-7 (deployed-check catch):** prod `state.json` carries `reasoning: 0` where the axis is absent on all units — the BLOCK-3 `or 0` class alive in the Glance DATA layer (Python side now fixed; JS side owes the same honest-null); F-3 mixed scorecard denominators; carried D4–D7+G1 from U1.
- **→ star-lord (standing operation, no dispatch needed):** `bin/ingest_claude_usage` is idempotent and re-runnable — any future run may fold newly-quiescent sessions (this conductor session's own 8-figure row lands on the next ingest). Candidate cadence: at each run-seal.
- **→ Matt (`matt_to_do/`, unchanged + sharpened):** **U-3** `ENABLE_PROMPT_CACHING_1H=1` — the recorder can now MEASURE this lever per-lane; **T20** disk RED still open.
- **→ KR:** Step-2 build wave unchanged (prompt banked at `e765eb32`); F-5 governance candidate for sequencing if Matt adopts.

**The Claude half of factory health is on the board. Every August token the fleet's primary economy spent is now a row, and the row survived two gates that each caught the other's defect.**

**Signed:** gandalf (RUN-CONDUCTOR), 2026-08-25.
