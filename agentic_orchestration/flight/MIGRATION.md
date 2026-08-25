# flight recorder — MIGRATION (cross-seam handoff, ADR-004)

**Custodian:** star-lord (schema custody per software-factory § 8 — *one schema, one custodian,
many readers*). **Readers of record:** drax (Tier-2 local board + Glance historical fleet card),
jack-ryan (gate re-derivation), gandalf (fold/audit), any lane emitter.

Append-only, like the tape. Newest revision first.

---

## Revision 1.1a — U-11 GATE REPAIR — 2026-08-25 (RUN U11-BUILD, block B-2)

**Still no schema change.** `SCHEMA_VERSION` 1, `SCHEMA_REVISION` "1.1", field set untouched,
`row_min_revision` still "1.0" for every U-11 row. Corrections use the existing `corrects:`
mechanics. This entry exists because **a published number moved by 163 %**, a fold-level
CONTRACT was clarified, and two normative SCHEMA.md clauses now say something they did not.

Discharges jack-ryan's G-U11 BLOCK ×3 + WARN-1/2/3/4 + INFO-5
(`qa/findings/2026-08-25-u11-gate.md`), under conductor ruling R-8 (run ledger L-4).

### 1 · `tokens_output` on the Claude lane was 62 % LOW. 16 correction rows are on the tape.

The B-1 ingester deduped a message's transcript lines by `message.id` and kept the **first**.
Anthropic writes `output_tokens` **progressively** — a placeholder on each non-terminal content
block, the complete count only on the line carrying a non-null `stop_reason`. The three INPUT
axes do repeat identically; output does not.

| axis | shipped (B-1) | corrected (B-2) | moved? |
|---|---|---|---|
| `tokens_input` | 8,442,547,650 | 8,442,547,650 | **no — byte-exact** |
| `tokens_cached_input` | 8,238,067,996 | 8,238,067,996 | **no — byte-exact** |
| `tokens_cache_write` | 204,120,185 | 204,120,185 | **no — byte-exact** |
| `tokens_output` | 19,327,247 | **50,878,369** | **+31,551,122 (+163 %)** |

**Cache-hit 97.578 % is unchanged and was always correct**, so anything baselined on the cache
criterion is unaffected. **Anything that quoted `19.3M`, or a cost/efficiency figure derived from
it, is stale** — re-derive, do not adjust.

**What to do as a reader:** nothing, if you fold corrections (you must — see § 2). The tape now
carries **118 raw rows / 95 after supersession**; the U-11 population is still **27 current rows,
one per session**. If you cached a raw row count, re-derive it.

**16, not 27.** The gate's discharge condition read "emit correction rows for all 27". Re-derived
per row from each row's own `derived_from`, **the two selectors disagree on 16 rows and agree
byte-for-byte on 11** — the agreeing 11 are sessions with no multi-block message (the four
synthetic-probe zero rows among them). The 62 % is a LANE-grain fact stated at row grain in the
finding. A `corrects:` row restating identical values would assert an amendment that did not
happen, on an append-only tape, and inflate any later count of the defect's blast radius. Both
populations are reported by the pass, and `--correct-unchanged` emits all 27 if the conductor
rules that way. **Flagged for jack-ryan at re-gate.**

### 2 · CORRECTION-SUPERSESSION IS NOW FOLD-LEVEL LAW — `schema.fold` applies it (**R-8**)

**This is the change most likely to affect you.** Before: supersession lived only in
`tape.load()`. A consumer holding raw rows — `schema.read_tape` and `tape.audit` both hand you
those — and folding them saw the **superseded original** as current. jack-ryan proved it live: a
valid, accepted, on-tape correction was **invisible** to `unit_event` under both ts orderings
while `correction_errors` returned `[]`.

- `schema.fold(rows)` now calls `apply_corrections` **first**, by default.
- New kwarg `fold(rows, corrections_applied=False)` — an assertion that the caller already
  applied them, **not** a switch that turns the law off. Leaving it alone is always safe;
  `apply_corrections` is idempotent, so `tape.load` → `fold` double-applies harmlessly.
- Semantics are **identical to Glance's `applyCorrections`** (`glance/parser/fleet.mjs`), which
  R-8 names the reference consumer: drop every `row_id` named by a `corrects` edge.
  Latest-in-chain wins, chains included, with no ordering pass.
- **Action for any Python consumer that folds raw rows: none — you inherit it.** Action for a
  consumer that hand-rolled its own supersession: delete it and use `fold`.

### 3 · Two normative SCHEMA.md clauses changed meaning

- **§ 3 line 141 said the token fields are "copied verbatim from the vendor stream". That was
  false as a general instruction** and is replaced by **new § 3.1**: the token fields are
  **semantic axes**, `tokens_input` means *total input presented, cached portion included*, a
  vendor reporting disjoint components sums them exactly, and fresh input is a derivation
  (`tokens_input − tokens_cached_input − tokens_cache_write`). Ratified as **R-G-U11-1**.
  **A third-lane emitter that followed the old wording on the Anthropic stream would publish a
  cache-hit rate of several thousand percent.** Read § 3.1 before mapping any new vendor.
- **§ 4 now DECLARES host-local absolute `derived_from`** (F-4). 27 rows name transcripts under
  `~/.claude/projects/`, which live in no repo. They validated by accident of
  `os.path.join(root, "/abs")`; the behaviour is now declared and pinned by a test.
  **Consequence: those rows are NOT reproducible off this host**, and on them `repo` is
  identity-only — it resolves nothing.

### 4 · Render contract — `flight_report` exports, and `board.py`'s duplicate is DELETED

The Tier-2 board kept its **own copy** of the SEALED-table and scorecard arithmetic, under a
comment naming the convergence point as *"star-lord exposing them as functions"*. Both copies
carried the same defect. That convergence has happened.

| new export | contract |
|---|---|
| `axis(closes, field)` | `(total, n_present, n_total)` for one **optional** numeric axis. Absence is COUNTED, never summed as zero |
| `axis_cell(total, n_present, n_total, fmt=human_n, noun="units")` | renders one axis; **an axis nothing carried never renders a numeral** — returns `— null on N/N units` |
| `share_cell(num, n_num, den, n_den)` | a rate; renders `—` over a missing denominator and tags mixed ones |
| `ratio_cell(...)` | quotients whose two sides have different populations (WARN-4: `tok-in/artifact`) |
| `close_rows(units)` · `sealed_by_workstream(rows, sealed)` · `model_scorecard(sealed)` | **the one home** for both tables' arithmetic. Returns per-axis coverage (`n_in`, `n_cache`, `n_cw`, `n_out`, `n_reason`, `n_artifact_rows`, `n_started`) alongside the totals |

- `n_tok` is retained under its old name and still means *"how many units carry `tokens_input`"*
  — **which is precisely the confusion BLOCK-3 was**: it was being used to gate OTHER axes.
  **If you gate a token cell, gate it on that axis's own `n_*`.**
- `sealed_by_workstream(...)["span"]` **may now be `None`** (no START→CLOSE pair). It was
  previously computed unconditionally. Guard it.
- Both tables gained a **`reasoning`** column, and every token cell now names its denominator.
- `board.NULL(label)` no longer doubles a leading em-dash, so `axis_cell` output flows through it.

### 5 · Behaviour changes inside the ingester

- `claude_usage.aggregate_session` selects the **terminal** usage payload per message
  (`stop_reason` non-null, falling back to last-seen). New key `progressive_messages` reports how
  many messages disagreed with themselves.
- New: `claude_usage.correct(records_dir, ...)` and `bin/ingest_claude_usage --correct`
  (`--correct-unchanged`, `--dry-run`, `--json`). **Append-only, idempotent twice over**: a row
  already named by a `corrects` edge is skipped, and a row whose re-derivation agrees produces
  nothing.
- New helpers: `u11_rows`, `superseded_ids`, `files_for_row`, `measured_axes`,
  `build_correction_row`, `terminal_rank`.
- The module docstring's stale literal is corrected (WARN-3): **42,595 repeated lines of 92,185
  usage-bearing lines (46.2 %)**, denominators named, re-derived — not `51,842 / "roughly a
  third"`.

### 6 · What did NOT change

- **Schema v1.1 is UNAMENDED.** No field, no enum value, no validation rule.
- **No row was edited or deleted.** `check_append_only`: 16 appended, 0 deleted or modified.
- The Claude lane's **cache-hit criterion (T3)** and every input/cache figure. Untouched, and
  verified byte-exact under the new selector before the correction was written.
- Attribution (R-3) — still honest-null on 27/27. F-5 remains a governance candidate.

**Suite:** 130 passed (flight) + 18 passed (factory board). Whole-tape validator CLEAN (118 rows),
`correction_errors` `[]`, `retrospection_audit` 0 violations, `check_append_only` 16/0.

---

## Revision 1.1 — U-11 CLAUDE-LANE INGESTER — 2026-08-25 (RUN U11-BUILD, block B-1)

**No schema change. `SCHEMA_VERSION` 1, `SCHEMA_REVISION` "1.1", both untouched** — no field
added, no enum widened, no rule altered, and `row_min_revision` reports **1.0** for every row
this emitter writes. A v1.0 reader can read them. This entry exists because the tape's
POPULATION changed in ways a consumer can be surprised by, which ADR-004 covers even when the
schema does not move.

**What landed:** `flight/claude_usage.py` + `flight/bin/ingest_claude_usage` fold Claude Code
session-transcript usage onto the tape. 27 rows for the quiescent 2026-08 sessions.

### What readers will see that was not there before

| change | consequence for a reader |
|---|---|
| **A new unit namespace `claude-session/<uuid>`**, `unit_kind: "session"` (an enum value v1 always had, now used for the first time) | Anything keyed on `unit_kind ∈ {job, run}` now has a third population. `session` units are **CLOSE-only** — no ENQUEUE, no START. |
| **CLOSE-only units** — 27 of them | Any derivation that assumes a SEALED unit has a START gets a null. `flight_report` already says so per-cell ("no START row on 27/27 units"); a consumer that instead computes `close − start` will divide by nothing. |
| **The `anthropic` lane now carries token primitives.** Before: `— (null, declared)`. After: 8.44 B input / 97.6 % cache-hit. | This is the point of U-11 and the thing to re-baseline against. Any dashboard copy that says the Claude lane reports no tokens is now **stale, not wrong-in-future** — fix the copy. |
| **Tape coverage moved backwards** — `coverage.first_ts` was `2026-08-24T03:29:39Z`, is now `2026-08-01T05:01:30Z` | Anything that pinned the coverage boundary as a literal is now stale. Derive it. |
| **A `(no workstream)` group of 27 units** in the SEALED-by-workstream table | Honest-null attribution (R-3), not a gap in the row. See the attribution note below before treating it as a defect. |
| **`derived_from` carries ABSOLUTE paths** on these rows | The transcripts live at `~/.claude/projects/**`, which is inside **no repo**, so a repo-relative path cannot name them. `schema.resolve_path` handles this correctly (`os.path.join(root, "/abs")` → `/abs`) and the validator's existence check passes. **Consequence: these rows are host-local.** A reader on another machine cannot re-derive them — the same property the substrate itself has. |

### The token-axis mapping — the one thing to read before querying these rows

    anthropic output_tokens               -> tokens_output        (1:1)
    anthropic cache_read_input_tokens     -> tokens_cached_input  (1:1)
    anthropic cache_creation_input_tokens -> tokens_cache_write   (1:1)
    anthropic input_tokens
      + cache_creation_input_tokens
      + cache_read_input_tokens           -> tokens_input         (the SUM)
    (no anthropic axis)                   -> tokens_reasoning     ABSENT

`tokens_input` is the **total input presented, cached portion included** — the same axis Codex's
stream reports directly (`input_tokens: 845782` alongside `cached_input_tokens: 750336` on one
turn: a subset, not an addend). Anthropic reports that same whole as three disjoint components,
so the row stores their exact sum. **A reader wanting fresh (uncached) input computes
`tokens_input − tokens_cached_input − tokens_cache_write`** — nothing is lost, but it is not
`tokens_input`. Storing `input_tokens` alone would have rendered a "cache-hit rate" of several
thousand percent. `tokens_reasoning` is **absent, not 0**: no anthropic axis reports it, and a
measured zero is a different fact from an unmeasured one.

### Attribution: honest-null is the finding, not the failure

`workstream` and `operator` are null on **27/27** rows. The mechanical index (R-3) works — it is
proved against a fixture, and it resolves `gandalf-session-53631d11` correctly — but the custody
ledger holds exactly **one** holder token that is a real session-id fragment, and it belongs to a
session that is still live and therefore not yet emitted. **Nothing durable in the repo records
which session did which work.** That is a fleet-level gap worth closing at the source (record the
session id in run ledgers / custody claims), not by guessing here.

### Re-running

Idempotent by `unit_id`: a session gets exactly one row, ever. Re-running appends nothing for
sessions already on the tape and picks up any session that has since gone quiet (60 min with no
transcript mtime change). Live sessions are skipped by design — the conductor's own session
lands on a later run. A quiescent session that later resumes is a `corrects:` chain, the only
amendment path, and expected to be rare.

---

## Revision 1.1 — G-2b DISCHARGE — 2026-08-24 (block B-1c)

Still **revision 1.1**, deliberately: gate amendments ship *as part of* the version they gate
(the G-1 precedent — B-1…B-6 shipped as part of v1.0). No row on the tape was written or edited
by this block; no frozen v1 rule was touched; the validator stays single-path.

### The SAFE-TO-FIRE predicate — **pinned here, by state name** (Amendment H · WARN-2)

Lane spec § 3 requires this predicate to be pinned in MIGRATION.md, and § 10.3 clause 6 requires
consumers — **router Q3 included** — to bind to it and **never to a leg's raw reading**. It is
pinned here and exported from `flight/bin/flight_report`:

| class | states | means |
|---|---|---|
| **OPEN — fire** | `open` · `queue-pending` | **Backlog is not occupancy.** A P-9 HELD job never closes a lane; the next drain takes it. `queue-pending` is a *first-choice* lane. |
| **OCCUPIED — enqueue** | `busy-lock` · `busy-out-of-band` · `busy-unknown` | The lane exists and works. ENQUEUE behind it. Occupied is **not** closed and never routes Claude-ward on its own. |
| **CLOSED — Matt** | `auth-expired` · `cli-missing` | Closes on a Matt-only action; a retry is not the fix (P-4). |

```python
flight_report.SAFE_TO_FIRE_STATES   # ("open", "queue-pending")
flight_report.safe_to_fire(ans)     # the predicate — bind to THIS
flight_report.state_marker(ans)     # the glance colour, derived from the predicate
flight_report.safe_to_fire_line(ans)  # the predicate rendered in words
```

**What changed for a reader:** `queue-pending` used to render **amber** in the Tier-1 card. It now
renders **green** (fire-safe) with the backlog still named in the `why` list, and every card
carries a `safe to fire:` line it previously did not render at all. `STATE_PRECEDENCE` is
**unchanged** — `queue-pending` still outranks `open`, because the backlog is the more specific
fact and deserves to be the one named. Only the *colour* moved, and it now derives from the
predicate instead of from string equality with `"open"`.

> **⚠ drax — cross-seam (ADR-004).** As of this block's HEAD, `factory/ui/board.py` holds its
> **own** `_STATE_CLASS` map (`"queue-pending": "s-warn"`). It does **not** import this
> derivation, so it did **not** inherit the correction and still paints a fire-safe lane as a
> warning. Two colour maps for one predicate is the WARN-2 defect wearing a second hat.
> `factory/` was deliberately **untouched** by this block (out of seam) — the fix is drax's.
> Shape: import `state_marker` / `safe_to_fire` and derive the CSS class from the returned
> severity, rather than keying a literal per state name.
>
> *Measured at write time, not assumed:* an uncommitted working-tree change in a **concurrent**
> drax session already replaces `_STATE_CLASS` with a map keyed off `fr.state_marker(ans)`. If
> that lands, this item is discharged board-side and the derivation has exactly one home. Stated
> as an observation of a working tree, not as a claim that it shipped.

### `row_min_revision` now asks KEYS **and** VALUES (BLOCK-2)

Correction to a statement this document and `SCHEMA.md § 0.0` both made: *"which revision a row
needs is derived from its own **key set**"*. That was true for **1 of AM-1's 3 amendments**. The
lane rename (1.1-a) and the currency (1.1-b) introduce no key — they live in **values** — and a
genuine v1.0 validator REJECTS both rows while the function reported `"1.0"`. If you consult
`row_min_revision`, re-read it: it now returns `"1.1"` for any row carrying `lane: "grok-serial"`
or `currency: "grok-sub"`, as well as for `cost_usd`. `schema.VALUE_SINCE` is the declared map.
No row on the tape changed classification except by becoming *correct*: exactly one row
(`dfbe28b17c2520f0`) needs 1.1, and it needs it on all three axes.

### `cost_usd` now refused on a lane declared to report none (WARN-1)

`schema.LANE_REPORTS_COST` — `codex-serial: False` (SCHEMA.md § 3, banked), `grok-serial: True`
(spec § 9.1, measured). **A writer emitting `cost_usd` on a `codex-serial` CLOSE now gets a
validation refusal**, because by the schema's own documented fact that number can only have been
computed from tokens × a price list. A lane **absent** from the map is UNDECLARED, not
"reports none" — nothing is asserted about the Claude lanes, whose streams have not been probed.
Zero existing rows affected (the only `cost_usd` on the tape is the `grok-serial` row).

### The busy-check derivation is **ON LOAN** to a renderer — D-2 must take it back (WARN-3)

Q62 ruled the card **renders the check's output**: *"a view of the derivation, never a second
truth source."* D-2 (`factory lane`) is unbuilt, so `flight_report.lane_answer` performs the
derivation itself and declares it (`probe: degraded — D-2 CLI pending`, sanctioned by spec
§ 13.1). **That sanction expires the day D-2 lands.**

The semantics invented in this renderer are **derivation logic**, not presentation: `busy-unknown`,
the UNREACHABLE/NOT-APPLICABLE split, the fail-closed union, the coverage clause, and the
Amendment-H predicate above. WARN-2 is the proof of what happens when two consumers hold their own
copies: one diverged from ratified law within the hour.

**Therefore, entered into D-2's DEFINITION OF DONE — D-2 is not done while two copies exist:**

1. D-2 owns the answer states, the coverage semantics and the safe-to-fire predicate, behind its
   pinned `--json` contract (exit codes pinned here, `0` = fire-safe);
2. `lane_answer` / `state_marker` / `safe_to_fire` / `safe_to_fire_line` in `flight_report` are
   **deleted** or reduced to thin adapters over that JSON — **deletion is part of D-2's DoD**, not
   a follow-up;
3. `factory/ui/board.py` renders the same `--json`;
4. `PROBE_MODE` stops saying `degraded`.

---

## Revision 1.1 — AMENDMENT AM-1 — 2026-08-24 (block B-1b)

**Authority:** Matt mid-run directive → spec § 13.2 (`gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`)
· lane spec § 9 (`gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`, ratified
`aed7dd43`). **Gate:** micro-gate **G-2b**, jack-ryan, pre-seal.

### TL;DR for a reader of the tape

**Nothing you already parse breaks.** AM-1 removes nothing, retypes nothing, tightens nothing.
Every pre-1.1 row is valid unedited under the 1.1 validator. If you only read the tape and never
write it, the two things you may now see that you could not before are `lane: "grok-serial"` and
`cost_usd` on a CLOSE row.

### The three changes

| # | change | breaking? | what a reader must do |
|---|---|---|---|
| **1.1-a** | lane enum `grok-judge` → **`grok-serial`** | **only for a WRITER that hardcoded the old string** | The rename is **tape-safe**: verified zero `grok` rows existed before it (`grep -c grok records-2026-08.jsonl` = `0`, re-checked mechanically by `test_11a_the_rename_was_TAPE_SAFE`). No historical row carries the old value, so no reader can encounter it. A writer passing `grok-judge` now gets a validation refusal — **loud, at the boundary, by design**. |
| **1.1-b** | currency enum gains **`grok-sub`** | no (pure addition) | A reader that switches exhaustively on `currency` needs a `grok-sub` arm. A reader that renders whatever string it finds needs nothing. |
| **1.1-c** | new field **`cost_usd`** — CLOSE-only, OPTIONAL | no (pure addition) | A reader with a closed field allow-list of its own must add it. **Semantics matter:** it is the VENDOR's reported dollar cost, copied verbatim (Grok emits `costUSD`; Codex reports none). It is a *reported primitive*, not a derivation — do not synthesise it from tokens × a price list, and do not treat its absence as `$0`. Absence means "this vendor's stream reports no dollar figure", which is not the same fact. |

### Version markers — read this before you assert a version

Two markers, and they are not the same number:

- `schema.SCHEMA_VERSION == 1` — the **row-format** version stamped in every row's `v`. It did
  **not** move: AM-1 is purely additive, so every existing row stays valid and the validator stays
  single-path (G2-T3, a HARD gate property).
- `schema.SCHEMA_REVISION == "1.1"` — the **custodian-amendment** marker. Render this when you
  display "schema vX"; the Tier-1 report does.

Which revision a row *needs* is **derived, never stamped**: `schema.row_min_revision(row)` returns
`"1.1"` for a row carrying `cost_usd`, `"1.0"` otherwise. Full reasoning + the declared deviation
from B-4's literal `v:2` wording is in `SCHEMA.md § 0.0` (custodian ruling, open for G-2b).

### `flight_report` module API — new exports (drax, Tier-2 board)

The Tier-2 board imports `flight/bin/flight_report` as a module and renders the **same** fold from
the **same** helpers, per THE LAW's one-data-path discipline. AM-1 adds the lane-card surface as
importable symbols so the board renders the busy check's output rather than deriving a second
answer (Q62: *a view of the derivation, never a second truth source*):

| symbol | contract |
|---|---|
| `LANE_CARDS` | tuple of per-vendor descriptors (`key`, `vendor`, `provider`, argv regexes, `has_lane_lock`, `runlogs`, `note`) |
| `probe_lane_lock()` · `probe_process_table()` · `probe_vendor_auth(cfg)` · `probe_runlogs(cfg, repo_root)` | leg probes, each a `Probes.run`-compatible thunk. **Probe names in `Probes` must match `render()`'s** (`lane-lock`, `proc-scan`, `auth:<key>`, `runlog:<key>`) or `lane_answer` sees `None` and correctly renders `busy-unknown` |
| `lane_answer(cfg, lock, procs, runlogs, auth)` | the union derivation. Returns `dict(state, reasons, advisories, unreachable, na)`. `na` is **new in 1.1** — legs that structurally do not exist (Grok has no lock, no run-log) as distinct from legs that failed |
| `lane_units(units, lane_key)` | lane membership from folded identity — **module-level as of 1.1** (was a closure) so both renderers share one derivation |
| `PROBE_MODE` · `Q62_CAVEAT` | the degraded-probe tag and the instrument caveat, rendered verbatim by both tiers |
| `unit_identity(unit)` · `last_actor(unit)` | **behaviour changed in B-1b** (G-2 FINDING-3): `unit_identity` now folds owner/seam/repo/workstream from **ENQUEUE/START only**, with CLOSE filling gaps. A later GATE row no longer overwrites the owner. If your board rendered `operator` off `unit["latest"]`, switch to `unit_identity(u)["operator"]` and put `last_actor(u)` in its own column |
| `partition_audit(units, membership)` | **required** if you render lanes: returns the list of units that fall in no lane / two lanes / no unit. An empty list is the only passing state (G-2 FINDING-2) |

**Removed:** `probe_codex_login()`. Vendor auth is probed once, per lane, via
`probe_vendor_auth(cfg)` — a read-only view that spawns the same vendor binary twice per render is
a view with a footprint. Nothing in-tree referenced it.

### What did NOT change, and must not be assumed to have

- No `GrokHarness`. D-6 stays gated behind U-8 judge-pilot authorisation. `factory/harness/` was
  not touched by this block.
- No change to Grok workload admission (U-8 judge door only). The lane card honestly renders
  `grok-serial` activity from the tape; it admits nothing.
- No D-1 (process-scan leg *in `factory/`*) and no D-2 (`factory lane` CLI subcommand). Those are
  another workstream. The report's leg-2 scan is a **render-time read** inside the view, and when
  D-2 lands the card should switch to rendering its `--json` output — at which point `PROBE_MODE`
  stops saying `degraded`.

---

## Revision 1.0 — FREEZE — 2026-08-24 (block B-1, `a4f7a569`)

Founding version = spec § 3 + jack-ryan's six G-1 amendments B-1…B-6. Full field matrix, sourcing
rules, closed field set and implementation deviations D-1…D-9 are in `SCHEMA.md`. G-2 ruled
**PASS-WITH-FINDINGS** (`qa/findings/2026-08-24-u1-schema-law-ratification.md`).

New readers start at `SCHEMA.md § 0` (the four hard rules) and `§ 10` (how a lane emits rows).
