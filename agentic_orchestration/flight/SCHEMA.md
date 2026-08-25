# U-1 fleet flight-recorder — record schema **v1.1**

**Status:** **v1 FROZEN 2026-08-24** at `a4f7a569` (RUN U1-BUILD, block B-1), carrying jack-ryan's
six G-1 amendments B-1…B-6, **G-2 PASS-WITH-FINDINGS**. **Revision 1.1 landed 2026-08-24** (block
B-1b) under **AMENDMENT AM-1** — a versioned custodian amendment outside G-2's v1-stability claim,
verified by micro-gate **G-2b** (jack-ryan). This document + `flight/schema.py` are the schema of
record; gandalf's spec § 3 is thereafter a historical record.
**Custodian:** star-lord (custody transferred on G-1 ratification — software-factory § 8:
*one schema, one custodian, many readers*).
**Founding version:** spec § 3
(`agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`)
**+ amendments** from `agentic_orchestration/qa/findings/2026-08-24-u1-schema-law-ratification.md`.
**Implementation:** `flight/schema.py` (enums, matrix, validator) · `flight/tape.py` (append/read/audit)
· `flight/bin/flight_record` (appender) · `flight/bin/normalize_vfx_corpus` (founding backfill)
· `flight/bin/flight_report` (Tier-1 view) · `flight/bin/check_append_only` (WARN-6 gate)
· `flight/tests/test_flight.py` (70 tests).
**Cross-seam handoff:** `flight/MIGRATION.md` (what a reader of the tape or an importer of
`flight_report` must change, and what is safe to ignore).

---

## 0.0 · Revision lineage (append-only, like the tape it governs)

| revision | date | custodian | what changed |
|---|---|---|---|
| **1.0** | 2026-08-24 | star-lord | FREEZE at `a4f7a569` — spec § 3 + G-1 amendments B-1…B-6. G-2 **PASS** (T1/T2/T3/T7 HARD all pass) |
| **1.1** | 2026-08-24 | star-lord | **AM-1**: lane `grok-judge` → `grok-serial` (tape-safe) · currency `grok-sub` added · field `cost_usd` added, CLOSE-only optional, vendor-REPORTED primitive |

### Two version markers, and why they are not the same number

| marker | value | moves when |
|---|---|---|
| `schema.SCHEMA_VERSION` — the **row-format** version stamped in every row's `v` | `1` | a row written under it stops being valid: a REMOVAL, a TYPE CHANGE, or a tightened requirement |
| `schema.SCHEMA_REVISION` — the **custodian-amendment** marker | `"1.1"` | any additive amendment: new field, new enum value, new rule |

**Custodian ruling — RATIFIED at G-2b (jack-ryan, 2026-08-24; overrule declined).** jack-ryan's
B-4 says *"adding a field is a version bump (`v:2`) with a custodian-signed note"*; gandalf's AM-1
says *"versioned custodian amendment (v1.1)"*. Both are satisfied in **substance** — there is a
version bump, a signed note, and a red test unless the literal is amended deliberately — with the
marker placed where it does not break the tape. Stamping `v:2` on new rows would force the
validator to branch per version to keep the 67 pre-amendment rows legal, and **"ONE validator,
zero exceptions" (G2-T3) is a HARD gate property I will not trade for a stamp.** Which revision a
given row *needs* stays **derivable from the row itself** (`schema.row_min_revision`) and is never
stored — a per-row revision stamp would be a hand-written summary of the row's own contents, which
is the R-L47-2 defect the derived-not-stored rule exists to prevent.

**The ruling stood; the two sentences defending it did not** (G-2b BLOCK-1 + BLOCK-2, both proven
by mutation, both discharged inside revision 1.1 on the G-1 precedent that gate amendments ship as
part of the version they gate). Recorded here rather than quietly repaired, because a document of
record that once stated a false property should say so:

| the claim as written | what was true | discharge |
|---|---|---|
| *"a red test unless the literal is amended deliberately"* | **FALSE.** No literal was pinned at the field-set level. Adding `cost_estimate` to `COST_FIELDS` — one line, reaching `ALL_FIELDS` and `FIELD_MATRIX` together — validated CLEAN, owed no `derived_from` (an estimate names no source), left `SCHEMA_REVISION` untouched and kept the suite 70/70 green. An **estimate primitive**, admitted silently, past HARD RULE 2. | `FIELD_ORDER` is now pinned **by equality** in `test_B4` — the FINDING-C pattern applied one level up. Add / remove / rename any field ⇒ RED (all three mutation classes verified). The red test exists now. |
| *"derivable from its own **key set**"* | **FALSE for 2 of AM-1's 3 amendments.** The 1.1-a lane rename and the 1.1-b currency introduce no key — they live in **values** — and a genuine v1.0 validator REJECTS both rows while `row_min_revision` called them 1.0-readable. The live grok row answered `"1.1"` only by luck: it happens to carry `cost_usd`. | `VALUE_SINCE` added; `row_min_revision` asks **keys AND values**. A `grok-serial` START row (which cannot carry a cost — CLOSE-only) now correctly reports `"1.1"`. |

A mechanism is not a claim about a mechanism. Both are now mechanisms.

**Backward compatibility:** every pre-1.1 row remains valid, unedited, under the 1.1 validator
(`tape.audit()` returns 0 errors across all 73 on-disk rows). AM-1 removes nothing, retypes
nothing, and tightens nothing.

---

## 0 · The four hard rules (compiled into `schema.py`, not just written here)

1. **Append-only.** No tool in `flight/bin/` has an edit verb or a delete verb. A wrong row is
   corrected by a **new** row carrying `corrects: <row_id>`; the superseded row stays on disk and
   leaves only the *fold*. `check_append_only` makes this a commit gate, not a hope.
2. **Never estimate.** Absent is absent. `make_row()` drops `None` rather than storing a null,
   and there is no zero default anywhere. *A null is a fact; an estimate in a truth-of-record
   stream is a fabrication.*
3. **A verdict never self-reports.** Non-null `verdict` requires a named `gatekeeper` **and** a
   `derived_from` source. `rc` is a mechanical exit code and is never promoted to a judgement.
4. **Telemetry, not content.** Identifiers, counts, timestamps, enums, artifact paths. Never a
   work-product body, never session prose, never an authored status claim.

## 1 · Storage

`agentic_orchestration/flight/records-YYYY-MM.jsonl` — one JSON object per line, monthly files,
**committed to git** (F-8). The month comes from the **event's own `ts`**, not from wall-clock at
append time, so a back-dated row files itself correctly. Raw vendor streams stay beside their runs
and are never copied; rows point at them via `derived_from`.

## 2 · Event types

| `event` | When | Terminal? |
|---|---|---|
| `ENQUEUE` | unit queued (dispatch authored, job queued) | no |
| `START` | execution begins | no |
| `GATE` | a gate fires with a verdict, gatekeeper named | no |
| `HALT` | commitment-boundary halt to Matt; veto window open | no |
| `CURATION` | a named downstream verifier files a WARN count / fabrication-check result | no |
| `SNAPSHOT` | subscription-meter reading; **not unit-bound** (`unit_id` explicit `null`) | no |
| `CLOSE` | terminal; carries cost primitives + artifact refs | **yes** |

## 3 · The normative field matrix (amendment **B-3**)

**R** = required non-null · **O** = optional · **F** = forbidden. Machine-checked in
`schema.FIELD_MATRIX`; the validator enforces **both directions** (a missing R and a present F are
each an error). This table and the code are generated from the same source of truth — if they ever
disagree, the code is the schema and this table is the bug.

| field | ENQUEUE | START | GATE | HALT | CURATION | SNAPSHOT | CLOSE |
|---|---|---|---|---|---|---|---|
| `v` `row_id` `ts` `event` | R | R | R | R | R | R | R |
| `unit_id` | R | R | R | R | R | **null** | R |
| `unit_kind` | R | R | R | R | R | F | R |
| `parent_id` | O | O | O | O | O | F | O |
| `workstream` `operator` `seam` `repo` `backfill` `corrects` `derived_from` | O | O | O | O | O | O | O |
| `provider` `lane` `pin` `model_echo` `harness` `harness_version` `curator` | O | O | F | F | F | F | **O** |
| `currency` | O | O | F | F | F | **R** | O |
| `verdict` | F | F | **R** | F | O | F | O |
| `gate_id` | F | F | **R** | F | F | F | F |
| `gatekeeper` | F | F | **R** | F | **R** | F | O |
| `warn_count` `fabrication_check` | F | F | F | F | O | F | F |
| `tokens_*` `cost_usd` `rc` `attempt` `retry_of` `artifacts` | F | F | F | F | F | F | O |
| `meter_raw` | F | F | F | F | F | **R** | F |

**Ruling on B-3's lean — ADOPTED, explicitly.** Identity is **denormalized onto `CLOSE`**. A CLOSE
row must be self-describing, because every § 3.6 payoff query is keyed on identity and a join-back
to `START` silently drops units whose START was never emitted — which the F-7 partial-coverage
design *expects to happen*. The cost is a few duplicated strings per row; the alternative is a
silently short denominator, which is the more expensive kind of wrong.

**Ruling on identity at `ENQUEUE` — ALLOWED (optional).** B-6 requires a `curator` at ENQUEUE
*for vendor lanes*, which is undecidable unless `lane` may ride an ENQUEUE row. Widened here,
before the freeze, for that reason and no other.

### Field semantics

| Field | Notes |
|---|---|
| `row_id` | **B-1.** `sha256(canonical_json(row − row_id))[:16]`, canonical = `sort_keys, separators=(",",":")` |
| `corrects` | **B-1.** MUST reference a `row_id` present on the tape, with the **same `unit_id` and `event`**. Enforced in `tape.append_row` and `schema.correction_errors` |
| `provider` `pin` `harness` `operator` `curator` `seam` `repo` `workstream` | open strings — a closed enum here would make the recorder refuse to record reality |
| `lane` | enum: `claude-agent · claude-subagent · codex-serial · grok-serial · cross-vendor-judge` (**AM-1 1.1-a** renamed `grok-judge` → `grok-serial`). U-8 adds an enum **value**, never a schema |
| `currency` | enum: `anthropic-max · chatgpt-sub · api-metered · grok-sub` (**AM-1 1.1-b**) |
| `verdict` | `PASS · PASS-WITH-FINDINGS · BLOCK · REFUSAL · HALT · FALLBACK-TAKEN · FAILED · SKIP` |
| `curator` | **B-6** (U-4 R-B). REQUIRED non-null on `ENQUEUE` when `lane` ∈ {`codex-serial`, `grok-serial`, `cross-vendor-judge`}. *A job whose curator field is empty is a refusal to fire.* |
| `tokens_input · tokens_cached_input · tokens_cache_write · tokens_output · tokens_reasoning` | copied verbatim from the vendor stream (Codex `turn.completed.usage` maps 1:1). Reasoning is a **share of output**, never a fifth addend |
| `cost_usd` | **AM-1 1.1-c.** CLOSE-only, optional, non-negative number. The **vendor's own reported** dollar cost, copied verbatim (Grok emits `costUSD` per call; Codex's stream reports none, so the field is simply absent on that lane). A **reported primitive**, not a derivation — it is measured by the vendor and transcribed, exactly like a token count, and it owes a `derived_from` for the same reason. **Never computed here** from tokens × a price list: a computed cost is a derivation wearing a primitive's clothes, and the derived-not-stored rule would catch it one release later, wrong |
| `artifacts` | `[{path, bytes}]` — bytes MEASURED from disk or copied from the harness's own measurement; paths validated to exist |
| `derived_from` | **B-5.** A **LIST** of artifact paths. `path#anchor` is legal (`workflow-upgrades.md#§ U-4`); the anchor is stripped for the disk check |
| `meter_raw` | object, in the meter's **own** vocabulary, unnormalized |
| `seam` / `repo` | **two separate fields** (INFO-5). `seam` = the seam touched; `repo` = the repo, and also the root that `artifacts[].path` and `derived_from` resolve against |

## 4 · Sourcing rules (amendment **B-5**)

- `derived_from` is a **list**, so an identity claim can name its own source independently of a
  cost claim.
- A row carrying **any token primitive**, **any vendor-reported cost** (`cost_usd`, AM-1) or
  **any verdict** MUST carry a non-empty `derived_from`, and **every named path must exist on
  disk**. Validator-enforced.
- **A lane DECLARED to report no dollar cost may not carry one** (G-2b WARN-1). `derived_from`
  proves a path *exists*; it never proves the path *contains* the number, so "reported, never
  computed" was prose with no parse-time consequence. It is decidable wherever a lane's stream has
  been measured, and `schema.LANE_REPORTS_COST` declares exactly those: `codex-serial: False`
  (§ 3, banked — the stream reports none), `grok-serial: True` (spec § 9.1, measured `costUSD`).
  A `codex-serial` CLOSE carrying `cost_usd` is now a **validation error**, because by the
  schema's own documented fact that number can only have been computed. **A lane absent from the
  map is UNDECLARED, not "reports none"** — honest-null discipline applied to the map itself; no
  probe of the Claude lanes' streams has been banked, so nothing is asserted about them.
- **Any identity field with no nameable source on a backfill row is `null`.** This is why the
  founding rows carry no `harness_version`: zero `model*`, `version`, `cli_version` or
  `rate_limit*` keys exist across all 30 VFX streams, so a version on those rows would be an
  unsourced claim about the past.
- **Paths are repo-root-relative** within the repo named by `repo` (default
  `reincarnated-collaboration`; sibling repos resolve under `~/Games/<repo>`).

## 5 · Closed field set (amendment **B-4**)

- The v1 field set is **CLOSED**. The validator **rejects unknown keys**. Adding a field is a
  `v:2` bump with a custodian-signed note.
- **No field may be named for a metric** — `rate · pct · percent · avg · mean · median · total ·
  count · duration · sum · ratio`. Checked at import time in `schema._assert_no_metric_names()`,
  so a violation is a crash, not a review miss.
- **One grandfathered exception, ruled explicitly rather than allowed silently: `warn_count`.**
  It is spec § 3.5 vocabulary and is a **primitive the curator reported** — copied verbatim like a
  token count, never computed from other rows. Renaming a spec field would have broken the
  fork-fidelity mapping jack-ryan verified at G-1; declaring the exception keeps G2-T6 greppable
  and the deviation visible. It lives in `schema.METRIC_NAME_EXCEPTIONS` — one line, one name.
- **The exception list is PINNED BY EQUALITY, not iterated around** (jack-ryan's G-2
  ACCEPT-WITH-CONDITION, FINDING-C): `test_B4` asserts
  `schema.METRIC_NAME_EXCEPTIONS == ("warn_count",)` exactly. Before this, a future custodian
  could discharge a B-4 failure by appending one identifier and keeping the suite green — which
  relocated accretion-by-one-reasonable-field from the field list to the exception list. Adding
  a second exception now costs what adding a field costs: a red suite, a revision bump, and a
  signed note. **AM-1 did not spend it** — `cost_usd` carries no metric token and needed no
  exception.
- **The FIELD SET ITSELF is PINNED BY EQUALITY too** (jack-ryan's G-2b BLOCK-1): `test_B4` asserts
  `schema.FIELD_ORDER == (<the 38-name literal>)`. FINDING-C closed the *inner* door (the
  exception list) and left the *outer* one open — the field list was never pinned by anything, so
  accretion-by-one-reasonable-field simply moved up a level. Proven live: adding `cost_estimate`
  to `COST_FIELDS` reached `ALL_FIELDS` **and** `FIELD_MATRIX` in one line and the row validated
  clean at 70/70 green — an **estimate** primitive walking past HARD RULE 2. Adding, removing OR
  renaming any field now turns the suite red (all three mutation classes verified). `ALL_FIELDS`
  is held equal to `FIELD_ORDER` in the same test, and the lengths are compared, so a duplicated
  name cannot hide inside the frozenset.

**Derived-not-stored.** Cache hit-rate, wall-time, time-to-seal, first-pass rate, rework-chain
length, per-model scorecards, window burn: all are queries over rows, computed by `flight_report`
at render time and written back nowhere.

## 6 · Staleness class key (WARN-1)

Declared **in schema**, not invented at render time — the board performs no derivation beyond
fold-of-events:

- `schema.SLA_CLASS_KEY = ("lane", "unit_kind")`
- `schema.SLA_MIN_N = 5` — below this n, a class median *is* the unit and the SLA is vacuously
  green, so the lane renders `no SLA — n=k` instead of a colour.

## 7 · v1 implementation notes (where the spec was silent, and what I chose)

| # | Choice | Rationale |
|---|---|---|
| **D-1** | Paths are **repo-root-relative**, not `agentic_orchestration/`-relative as in the spec's illustrative § 11.2 rows | the tape is fleet-wide across five repos; a path is resolvable only if it is rooted at a repo named on the row |
| **D-2** | `None` is **dropped**, not stored as JSON `null` | a stored null looks like a measurement of nothing. Sole exception: `unit_id: null` on SNAPSHOT, which spec § 3.2 mandates |
| **D-3** | `row_id` is a **content hash**, not a ULID | backfills become idempotent for free — a re-run regenerates identical ids and every row is refused as a duplicate, with no side-car state file. Trade-off: a byte-identical repeat event inside one second is deduped by default; `flight_record --force` appends it anyway |
| **D-4** | `derived_from` is legal on **every** event type | the per-landing law applies to lifecycle rows too — a backfilled `START` ts must cite the log it came from |
| **D-5** | `attempt` / `retry_of` are `CLOSE`-only | § 3.4 lists them under cost axes; rework-chain length stays a query over CLOSE rows |
| **D-6** | Interactive-lane `pin` is **absent, not guessed** | a Claude Code agent session does not surface the model string it runs under in any form the shell can read. Unknown is the honest state; F-7's revisit is the place to fix it |
| **D-7** | Report ages derive from **one** captured `now`, printed on the header line | makes the render a pure function of (disk state, `now`); `--now` pins it for tests |
| **D-8** | The tape's **raw** on-disk row count and the post-correction fold count are **both** printed | a reader can never mistake "rows we count" for "rows on disk" |
| **D-9** | `verdict` requires `derived_from` as well as `gatekeeper` | B-2 asks for the gatekeeper; requiring the artifact too costs nothing and makes the judgement auditable years later. **Stricter than the amendment, deliberately** |

### Known v1 limitation, carried openly

**Per-model WARN rate (spec § 3.6-1) is only partially derivable.** A `CURATION` row binds to a
`unit_id` and carries no identity axes, so its `provider`/`pin` come from that unit's own
START/CLOSE rows. When curation is filed against a **run** — as the VFX P2 curation is — the run
has no lane identity and the WARN count cannot be attributed to a model. Options for v2: (a) allow
identity axes on CURATION, (b) require curation to bind to the verdict-bearing unit, (c) accept the
gap. **Not ruled unilaterally** — flagged for jack-ryan/gandalf. `flight_report` omits the column
and says why, rather than printing a zero.

## 8 · Founding rows (backfill, 2026-08-24)

30 VFX P2 jobs → **30 `START` + 30 `CLOSE`**, all `backfill: true`, plus **1 `CURATION`** row on
`run:VFX-AB`. Measured aggregate over the 30 `turn.completed.usage` objects — re-derived
mechanically from the raw streams, never copied from a report:

| primitive | measured |
|---|---|
| `tokens_input` | 72,375,471 |
| `tokens_cached_input` | 67,431,424 (93.17 % of input) |
| `tokens_cache_write` | 0 (a measured zero — the key is present and reads 0) |
| `tokens_output` | 259,471 |
| `tokens_reasoning` | 154,000 |

What the founding rows deliberately do **not** contain:

- **No `verdict` on any job row (B-2).** No gatekeeper judged those 30 jobs at job grain. The
  corpus proves the gap: job 01 exited `rc=0` while `01-ground_targeted_circle.err` logged an
  `AuthRequired` transport failure. The report renders `30/30 rc=0`, never `30 PASS`. Ledger S2's
  instruction "verdicts from `_run-log.tsv` rc only" is retracted by this amendment.
- **No `ENQUEUE` rows (INFO-3).** `_run-log.tsv` carries `start`/`end` only; an ENQUEUE at
  `ts=start` would be a fabricated event. `enqueue→seal` is therefore **not derivable** for
  VFX-AB, and the report's rollup column is labelled `first-start→last-close` (a run duration).
- **No `harness_version` / `model_echo` (B-5c).** Neither has a source in the streams.
- **No `GATE` row.** galadriel's P3 selection gate records per-item merge/distinct rulings, not a
  run-level verdict in the § 3.5 enum. Inventing one is the exact fabrication class this recorder
  exists to make impossible.

The one `CURATION` row (`verdict: PASS`, `gatekeeper: elrond`, `warn_count: 6`,
`derived_from: [elrond/notes/2026-08-24-vfx-p2-dossier-curation.md]`) is the only VFX artifact
carrying a run-level verdict in the § 3.5 vocabulary, filed by a named verifier.

Each CLOSE row's `derived_from` lists the raw usage stream, **its `.err` sidecar** (INFO-7 — free
evidence, and what keeps B-2's argument auditable), the run log, and the identity sources.

### 8.1 · The U1-BUILD rows are backfill too, and now say so (G-2 FINDING-1)

Workflow #2 — this run's own six rows, written at `49d717d5` — carry event timestamps that
**predate the appender's existence** and derive from **authored artifacts** (the request doc, the
run ledger, the dispatch file, jack-ryan's finding), not from an instrumented stream. That is
reconstruction, which is exactly what `backfill: true` exists to declare, and `--backfill` was not
passed. jack-ryan caught it at G-2.

**Discharged by CORRECTION, never by rewrite.** Five superseding rows (`corrects: <row_id>`,
`backfill: true`) were appended for the five rows still live in the fold; the sixth was already
superseded by an earlier correction and needed none. The undeclared originals **remain on disk,
byte for byte** — the flight-recorder property is that the tape does not lie about what was
believed at the time. `backfill` is OPTIONAL on every event, so this touched no schema and could
not have tripped G2-T2.

Consequence to read honestly: **the tape currently contains no forward-captured workflow at all.**
Both workflows are backfill. Forward capture begins when the codex durable queue emits its own
rows (FINDING-4's first live `curator` is the same milestone).

### 8.2 · The founding Grok row (AM-1, 2026-08-24)

One `CLOSE` row, `backfill: true`, lane `grok-serial`, unit `grok-probe/2026-08-24-capability`,
sourced **only** to the lane spec's § 9.1 measurement record
(`gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md#§ 9.1`). It is real
credential spend and the first `cost_usd` on the tape.

| on the row | value | why |
|---|---|---|
| `cost_usd` | `0.00286` | § 9.1, vendor-reported (`costUSD`) |
| `harness` / `harness_version` | `grok-cli` / `1.0.5` | § 9.1 measured the binary |
| `model_echo` | `grok-4.6-build` | § 9.1: headless RESOLVES to this — a vendor-side resolution, which is what `model_echo` is for |
| `provider` / `currency` | `xai` / `grok-sub` | § 9.1 |

What is **deliberately absent**, each because § 9.1 does not record it:

- **`verdict`** — `PROBE-OK` is the string the probe's own output returned. That is the executing
  lane's **self-assessment**, and a verdict never self-reports (B-2); it is also not in the § 3.5
  enum. `rc` is absent for the same reason in reverse: § 9.1 records `rc=0` for the *auth* check
  (`grok models`), never for the headless probe.
- **All five token primitives** — § 9.1 records that the envelope *carries* a `usage` object; it
  records no numbers from it. A null is a fact.
- **`pin`** — the probe took the vendor default; nothing was said on the argv. The provisional
  pin `grok-4.6` lives in the lane spec § 9.3 as protocol, and a protocol constant is not a
  measurement of this call.
- **The ~4.3 s wall time** — duration is DERIVED from `START`→`CLOSE`, and § 9.1 records no
  absolute start clock. Emitting a `START` four seconds before the `CLOSE` would assert two
  timestamps nobody measured in order to encode one that was. The measurement stays in the spec;
  the tape stays honest. (Closing this needs a `START` row at fire time — which the lane gets for
  free the day a harness fires it.)
- **`curator`** — B-6 binds at ENQUEUE on vendor lanes; there is no ENQUEUE row, and no curator
  was named for a probe.

**One declared imprecision, flagged rather than smoothed:** § 9.1 records the probe's **date**
but no clock time. The row's `ts` (`2026-08-24T23:24:56Z`) is the commit that banked the
measurement record (`368f7a70`) — a **sourced upper bound**, not a measured event time. Every
other number on the row is § 9.1's own.

**Scope guard (AM-1 § 13.3):** this row is fleet-management parity only. No `GrokHarness` was
built (D-6 stays gated behind U-8 judge-pilot authorisation), `factory/harness/` was not touched,
and Grok workload admission is unchanged.

## 9 · Amendment traceability (for the G-1 discharge read)

| Amendment | Where it lives | Test that fails without it |
|---|---|---|
| **B-1** `row_id` + constrained `corrects` | `schema.compute_row_id`, `schema.correction_errors`, `tape.append_row` | `test_B1_…`, `test_correction_must_target_an_existing_row_with_same_unit_and_event` |
| **B-2** verdict never from `rc` | `schema.validate` (verdict ⇒ gatekeeper), normalizer emits no verdict | `test_B2_verdict_requires_a_named_gatekeeper`, `test_B2_no_founding_row_carries_a_verdict_derived_from_rc`, `test_B2_rc_alone_never_becomes_a_verdict_on_the_founding_tape` |
| **B-3** normative event matrix | `schema.FIELD_MATRIX` | `test_B3_field_matrix_is_normative_in_both_directions` |
| **B-4** closed field set, no metric names | `schema.ALL_FIELDS`, `schema._assert_no_metric_names` | `test_B4_…`, `test_live_tape_stores_no_unknown_and_no_metric_named_key` |
| **B-5** `derived_from` list + disk check | `schema.validate`, `schema.resolve_path` | `test_B5_derived_from_is_a_list_whose_paths_must_exist`, `test_B5c_harness_version_is_null_…`, `test_INFO7_err_sidecar_rides_along_as_evidence` |
| **B-6** `curator` at vendor-lane ENQUEUE | `schema.VENDOR_LANES`, `schema.validate` | `test_B6_vendor_lane_enqueue_requires_a_named_curator` |
| **WARN-1** class key + min-n | `schema.SLA_CLASS_KEY`, `schema.SLA_MIN_N`, `flight_report.staleness` | `test_WARN1_…` |
| **WARN-5** coverage declaration | `schema.coverage`, report header + IN-FLIGHT lane | rendered `COVERAGE:` line |
| **WARN-6** append-only gate | `flight/bin/check_append_only` | run it against a staged rewrite |
| **INFO-3** relabel `enqueue→seal` | report SEALED table column | rendered `first-start→last-close` |
| **INFO-4** denominators on every cell | report SEALED + scorecard tables | rendered `30/30 rc=0`, `93.2% of 72.4M` |
| **INFO-5** `seam` / `repo` named as two fields | § 3 table above | schema field list |
| **FINDING-C** (G-2) exception list pinned by equality | `test_B4` | `test_B4_…` (asserts the literal `("warn_count",)`) |
| **FINDING-1** (G-2) U1-BUILD backfill declared | 5 correction rows on the tape; § 8.1 | `test_FINDING1_every_u1_build_row_in_the_fold_declares_itself_backfill` |
| **FINDING-2** (G-2) lanes partition the tape | `flight_report.partition_audit`, UNBOUND lane, in-band `PARTITION ✓` line | `test_FINDING2_rendered_lanes_partition_the_tape` |
| **FINDING-3** (G-2) owner ≠ last actor | `flight_report.unit_identity` (ENQUEUE/START only), `last_actor` | `test_FINDING3_owner_comes_from_enqueue_start_never_from_a_later_gate`, `…_holds_on_the_live_tape_…` |
| **AM-1 1.1-a** `grok-serial` | `schema.LANES`, `schema.VENDOR_LANES` | `test_11a_…` ×3 (incl. the tape-safety re-check) |
| **AM-1 1.1-b** `grok-sub` | `schema.CURRENCIES` | `test_11b_grok_sub_currency` |
| **AM-1 1.1-c** `cost_usd` | `schema.COST_FIELDS`, `REPORTED_COST_FIELDS`, `FIELD_SINCE` | `test_11c_…` ×3, `test_row_min_revision_…` |
| **AM-1 § 13.1** LANE CARDS | `flight_report.LANE_CARDS` / `lane_answer` / the three leg probes | `TestLanesSection` (10 tests, incl. `test_the_lane_probes_write_NOTHING`) |
| **BLOCK-1** (G-2b) field set pinned by equality | `test_B4` (the 38-name literal) + `ALL_FIELDS` equality + length check | `test_B4_…` (verified red on add / rename / remove) |
| **BLOCK-2** (G-2b) revision derived from keys **and values** | `schema.VALUE_SINCE`, `schema.row_min_revision` | `test_BLOCK2_row_min_revision_asks_VALUES_not_only_keys` (verified red pre-fix), `test_BLOCK2_no_pre_amendment_row_on_the_live_tape_is_over_reported` |
| **WARN-1** (G-2b) a lane declared to report no cost may not carry one | `schema.LANE_REPORTS_COST`, `schema.validate` | `test_WARN1_a_lane_declared_to_report_no_cost_may_not_carry_one` |
| **WARN-2** (G-2b) Amendment H — `queue-pending` is OPEN; predicate rendered | `flight_report.SAFE_TO_FIRE_STATES` / `safe_to_fire` / `state_marker` / `safe_to_fire_line` | `test_WARN2_…` ×3 |
| **WARN-3** (G-2b) D-2 migration named | `lane_answer` docstring · `MIGRATION.md` § *"The busy-check derivation is on loan"* | (documentary — enforced at D-2's DoD) |

---

## 10 · Integration point for the Step-2 codex queue (L-1: `factory/harness/` untouched)

The Step-2 codex adapter (`factory/harness/codex.py`, foreign in-flight at the time of this build)
should emit U-1 rows **natively** so the wave retrofits nothing. It needs **one** function, called
three times per job:

```python
# factory/harness/codex.py — add near the top
import sys, os
FLIGHT_DIR = os.path.join(REPO_ROOT, "agentic_orchestration", "flight")
sys.path.insert(0, FLIGHT_DIR)
import schema, tape

def flight(event, ts, **fields):
    """One line. ENQUEUE at queue-admit, START before `codex exec`, CLOSE after rc.
    Never raises into the queue: a recorder that can stop the work is a middleman."""
    try:
        tape.append_row(schema.make_row(event, ts, **fields), FLIGHT_DIR)
    except Exception as exc:
        sys.stderr.write("flight: row dropped (%s) — work continues\n" % exc)
```

Call sites and the fields each owes:

| Call site | Event | Fields |
|---|---|---|
| job admitted to the queue | `ENQUEUE` | `unit_id`, `unit_kind="job"`, `parent_id`, `workstream`, `operator`, `seam`, `repo`, `lane="codex-serial"`, **`curator=<named agent>` — REQUIRED, B-6; an empty curator is a refusal to fire** |
| immediately before `codex exec` | `START` | the above **plus** `provider="openai"`, `pin`, `harness="codex-cli"`, `harness_version` (read from `codex --version` — **not** hardcoded), `currency="chatgpt-sub"`, `model_echo` if the stream echoes one, `derived_from=[<the config/pin source>]` |
| after the process exits | `CLOSE` | the above **plus** `rc`, `attempt`, the five token primitives **copied from `turn.completed.usage`** (omit any the stream did not carry), `artifacts=[{path, bytes}]`, and `derived_from=[<usage jsonl>, <err sidecar>, <run log>]`. **No `verdict`** — that arrives later as a `GATE` row from a named gatekeeper |

Four properties the integration must preserve:

1. **The recorder never carries traffic and never blocks work** — hence swallow-and-warn above.
   A dropped row is a gap in the tape; a raised exception is a lost job.
2. **`harness_version` is read from the tool, not typed into the source.** A silent CLI update is
   the same class of confound as a silent model change, and hardcoding it hides exactly that.
   This also closes INFO-2: today the pin-drift tripwire has **no signal** on the Codex lane.
3. **`rc` is the exit code; `verdict` is a judgement.** They may correlate on a mechanical lane,
   but the queue must never write one from the other (B-2).
4. **`curator` is captured once, at the source** — enqueue time, not close time (U-4 R-B). This is
   what makes "zero governance leaks" falsifiable by query instead of by memory.

Shell lanes that would rather not import Python call the CLI instead — same tape, same schema:

```bash
FR=agentic_orchestration/flight/bin/flight_record
"$FR" ENQUEUE --unit-id "codexq/$job" --unit-kind job --parent-id "run:$RUN" \
      --workstream "$WS" --operator star-lord --lane codex-serial --curator "$CURATOR"
"$FR" START   --unit-id "codexq/$job" --unit-kind job --lane codex-serial --provider openai \
      --pin "$PIN" --harness codex-cli --harness-version "$(codex --version | awk '{print $NF}')" \
      --currency chatgpt-sub
```
