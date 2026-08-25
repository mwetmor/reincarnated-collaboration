# flight recorder — MIGRATION (cross-seam handoff, ADR-004)

**Custodian:** star-lord (schema custody per software-factory § 8 — *one schema, one custodian,
many readers*). **Readers of record:** drax (Tier-2 local board + Glance historical fleet card),
jack-ryan (gate re-derivation), gandalf (fold/audit), any lane emitter.

Append-only, like the tape. Newest revision first.

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
