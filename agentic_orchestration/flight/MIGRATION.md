# flight recorder — MIGRATION (cross-seam handoff, ADR-004)

**Custodian:** star-lord (schema custody per software-factory § 8 — *one schema, one custodian,
many readers*). **Readers of record:** drax (Tier-2 local board + Glance historical fleet card),
jack-ryan (gate re-derivation), gandalf (fold/audit), any lane emitter.

Append-only, like the tape. Newest revision first.

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
