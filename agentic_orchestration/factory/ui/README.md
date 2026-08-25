# factory/ui — the local fleet board (Tier-2)

**Owner:** drax · **Spec:** `gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`
§ 11.4 (render sketch) + § 13.1 (AM-1 vendor LANE CARDS) · Spec B lineage:
`gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md` (F-1: ONE local board, the Spec B
factory surface extended to fleet scope — not a second dashboard).

## Run it

```bash
# serve (the normal way to look at it)
python3 agentic_orchestration/factory/ui/board.py            # → http://127.0.0.1:8787/
python3 agentic_orchestration/factory/ui/board.py --port 9000

# one static snapshot (galadriel's screenshot path; identical render, no server)
python3 agentic_orchestration/factory/ui/board.py --render-to /tmp/fleet-board.html --once

# fast/offline variants
python3 agentic_orchestration/factory/ui/board.py --no-lane-probes   # no vendor CLI auth calls
python3 agentic_orchestration/factory/ui/board.py --no-probes        # tape-only render
python3 agentic_orchestration/factory/ui/board.py --now 2026-08-25T00:00:00Z --render-to …

# tests
python3 -m pytest agentic_orchestration/factory/ui/tests/test_board.py -q
```

Python 3 stdlib only — no npm, no build step, no node_modules, nothing to install.

## What it is

A VIEW over the U-1 tape (`flight/records-*.jsonl`) plus read-only disk probes, rendered as
the § 11.4 columns: **AWAITING MATT · IN-FLIGHT · AT GATE · SEALED**, then the **LANES** card
(codex · grok · claude summarised), then **HEALTH**, then the sealed rollups + per-model
scorecard, then UNBOUND.

**THE LAW (engineering Discipline #74) binds every line of it:** zero authority, zero write
verbs, never in the data path, no LLM in the render path, honest nulls, one data path. The
HTTP server answers GET/HEAD and refuses every other method with 405 before any handler runs.

## One derivation, two windows

The board owns no fold and no probe of its own. It imports `flight/bin/flight_report` and
reuses star-lord's helpers verbatim — `schema.fold`, `unit_identity` (owner from ENQUEUE/START,
never from the latest row), `last_actor`, `sla_class` / `class_medians` / `staleness`,
`partition_audit`, every `probe_*`, and the whole AM-1 lane composite (`LANE_CARDS`,
`probe_lane_lock` / `probe_process_table` / `probe_vendor_auth` / `probe_runlogs`,
`lane_answer`, `PROBE_MODE`, `Q62_CAVEAT`). If that import fails the board renders RED and
renders nothing else: a view that cannot reach its one derivation must not show a partial
green. `flight/` is star-lord's seam and is read/imported only — never modified.

Consequence you can check by eye: for the same tape, this board and `flight/report.md` carry
the same counts. AT GATE and the tape-side HALT list are **overlays**, not partition lanes —
exactly as Tier-1 renders them — so IN-FLIGHT never disagrees between the two windows.

## No auto-refresh, deliberately

Leg 1 of the ratified busy check (`lane_is_free()`) acquires the serial lock and releases it
in the same breath. A self-refreshing board would therefore periodically take the serial lane,
and a concurrent `lane-drain` could see `LaneBusy` and refuse — a view walking into the data
path through its own instrument. So there is no meta-refresh and no poller: a render happens
when a human asks for one. The card shows whether a kernel object was touched.

## Q62 — the pre-TUI glance

The LANES card renders the busy check's output so Matt can glance before opening a codex or
grok TUI. It carries the ruling's caveat verbatim: *liveness-NOW is the § 3 CLI check's
answer; the board is a VIEW (THE LAW) and may lag its refresh.* While the D-2
`factory lane --json` subcommand is unbuilt, every card is labelled
`probe: degraded — D-2 CLI pending` and each leg says what it saw.

## Not here

No New Run form, no launch verb, no annotate verb (Spec B § 5's write verbs are
factory-receipts-side and stay unbuilt until the F1 spine lands). No GrokHarness, no admission
logic, nothing under `factory/harness/` touched.
