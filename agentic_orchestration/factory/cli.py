"""factory CLI — terminal commands, no daemon (Spec A § 1).

    factory run <workflow.yaml>       run a workflow to completion
    factory status                    live/last runs, red gates, token totals
    factory report <run_id>           the generated per-run markdown report
    factory gates                     list registered gates (grep-able inventory)
    factory determinism <workflow>    run twice, compare gate verdicts (R-BR-51)
    factory probe-agent <seam>        one live headless call; verifies the lane

    factory lane                      THE cross-session busy check (read-only)
    factory lane-status <queue-dir>   one queue's auth + serial-lane + backlog screen
    factory lane-enqueue <queue-dir>  add one job (--curator is REQUIRED; U-4 R-B)
    factory lane-drain <queue-dir>    drain the queue serially; safe to re-fire

    factory custody check             THE agent-level seam check (read-only)
    factory custody claim             ATOMIC check-and-append; --release-on REQUIRED
    factory custody release           close a claim, citing its completion evidence
    factory custody override          clear a STALE claim — loud, manual, never a TTL

The `lane-*` commands are the uptime half of U-4: hand-fired scripts were the bridge,
the queue is the uptime. `lane-drain` is idempotent and crash-safe, so the correct
response to "did that finish?" is to run it again.

`factory lane` is the D-2 busy check and it is a DIFFERENT KIND OF COMMAND from the
other three: it acquires nothing, writes nothing, and answers *"is a vendor agent in
use right now?"* across every session on this host. Run it before firing anything at a
vendor lane; run it before opening a vendor TUI. The one predicate every consumer
binds to is `lane_status.SAFE_TO_FIRE_STATES` — see `MIGRATION.md`.

`factory custody` is the SECOND AXIS (spec § 11). The lane lock serialises vendor
INVOCATIONS; custody serialises AGENTS. Run `custody check` before dispatching a
sub-agent into a named seam — occupied seam means DO NOT SPAWN. `custody check` holds
the same emits-nothing discipline as `factory lane`; the other three verbs append to
the ledger under an `flock` on it. The predicate is `custody.SAFE_TO_SPAWN_STATES`,
named separately from the lane's because they answer different questions.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .gates import available_gates
from .receipts import Receipts
from .report import render_run_report, render_status
from .runner import DEFAULT_DB, Runner
from .workflow import WorkflowError, load_workflow

FACTORY_DIR = Path(__file__).parent


def _cmd_run(args: argparse.Namespace) -> int:
    try:
        wf = load_workflow(args.workflow)
    except WorkflowError as exc:
        print(f"workflow rejected at load: {exc}", file=sys.stderr)
        return 2
    runner = Runner(wf, factory_dir=FACTORY_DIR, run_id=args.run_id)
    try:
        result = runner.run()
    finally:
        runner.close()
    print(f"\nreport: {result.session_dir / 'run_report.md'}")
    return 0 if result.is_green else 1


def _cmd_status(args: argparse.Namespace) -> int:
    with Receipts(FACTORY_DIR / DEFAULT_DB) as receipts:
        print(render_status(receipts, limit=args.limit))
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    with Receipts(FACTORY_DIR / DEFAULT_DB) as receipts:
        text = render_run_report(receipts, args.run_id)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


def _cmd_gates(args: argparse.Namespace) -> int:
    for name, fn in sorted(available_gates().items()):
        doc = (fn.__doc__ or "").strip().splitlines()
        print(f"{name:<22} {doc[0] if doc else ''}")
    return 0


def _cmd_determinism(args: argparse.Namespace) -> int:
    """R-BR-51 — an instrument used for measurement must assert its own determinism."""
    try:
        wf = load_workflow(args.workflow)
    except WorkflowError as exc:
        print(f"workflow rejected at load: {exc}", file=sys.stderr)
        return 2
    verdicts = []
    for lap in (1, 2):
        runner = Runner(wf, factory_dir=FACTORY_DIR, verbose=not args.quiet)
        try:
            runner.run()
            verdicts.append(runner.receipts.gate_verdict_tuples(runner.run_id))
            print(f"lap {lap}: {runner.run_id}")
        finally:
            runner.close()
    if verdicts[0] == verdicts[1]:
        print(f"\nDETERMINISM: EXACT — {len(verdicts[0])} gate verdicts identical across two laps")
        for phase, gate, status in verdicts[0]:
            print(f"  {phase:<28} {gate:<22} {status}")
        return 0
    print("\nDETERMINISM: DIFFERS — the instrument is not asserting the same thing twice")
    for a, b in zip(verdicts[0], verdicts[1]):
        if a != b:
            print(f"  lap1 {a}  !=  lap2 {b}")
    only1 = [v for v in verdicts[0] if v not in verdicts[1]]
    only2 = [v for v in verdicts[1] if v not in verdicts[0]]
    if only1 or only2:
        print(f"  lap1-only: {only1}\n  lap2-only: {only2}")
    return 1


def _cmd_probe_agent(args: argparse.Namespace) -> int:
    """One live headless call. Verifies the lane and prints the usage frame's shape."""
    from .harness import get_harness

    harness = get_harness("claude_code")
    out_path = FACTORY_DIR / "sessions" / "probe" / f"{args.seam}.jsonl"
    result = harness.run(
        args.prompt,
        Path(args.cwd or FACTORY_DIR),
        {
            "agent": args.seam,
            "tools": ["Read"],
            "timeout_s": args.timeout_s,
            "raw_output_path": str(out_path),
        },
    )
    print(f"ok={result.ok}  model={result.model}  session={result.harness_session_id}")
    print(result.usage.one_line())
    if result.error:
        print(f"error: {result.error}")
    print(f"raw frames: {out_path}")
    print("---")
    print(result.text[:2000])
    return 0 if result.ok else 1


def _lane_pieces(args: argparse.Namespace):
    from .jobqueue import JobQueue

    lane = getattr(args, "lane", None) or "codex"
    if lane == "grok":
        from .harness.grok import GrokHarness

        return JobQueue(Path(args.queue_dir), lane="grok"), GrokHarness()
    from .harness.codex import CodexHarness

    return JobQueue(Path(args.queue_dir), lane="codex"), CodexHarness()


def _cmd_lane(args: argparse.Namespace) -> int:
    """**D-2 — the cross-session busy check.** Read-only, acquires nothing, emits nothing.

    Three legs (kernel lock · process table · run-log last row), unioned FAIL-CLOSED
    over EXECUTION OCCUPANCY ONLY. Answers WHICH state, never a bare bool:

        open · queue-pending · busy-lock · busy-out-of-band · busy-unknown ·
        auth-expired · cli-missing        (+ the interactive-<vendor>-present advisory)

    Exit codes are per-state and pinned in `MIGRATION.md`; `--safe-to-fire` collapses
    them to 0/1 for a caller whose only question is *"may I fire?"*. THE safe-to-fire
    predicate is `lane_status.SAFE_TO_FIRE_STATES` — one name, one place; consumers
    bind to it and never to a leg's raw reading (Amendment H).
    """
    from . import lane_status as ls

    lanes = list(ls.VENDOR_ORDER) if args.lane_sel == "all" else [args.lane_sel]
    extra = [Path(args.queue_dir) / "_run-log.tsv"] if args.queue_dir else []
    if args.lane_sel == "all":
        statuses = ls.all_lane_status(lanes, check_auth=not args.no_auth)
    else:
        procs, error = None, None
        try:
            procs = ls.scan_process_table()
        except Exception as exc:  # noqa: BLE001 — any failure is "could not look"
            error = f"{type(exc).__name__}: {exc}"
        statuses = [ls.lane_status(
            lanes[0], procs=procs, procs_error=error,
            extra_runlogs=extra, check_auth=not args.no_auth,
        )]

    chosen = ls.select_lane(statuses)

    if args.json:
        import json as _json

        print(_json.dumps({
            "lanes": {s.lane: s.to_dict() for s in statuses},
            "select": chosen.lane if chosen else None,
            "safe_to_fire_states": sorted(ls.SAFE_TO_FIRE_STATES),
            "exit_codes": ls.EXIT_CODES,
        }, indent=2))
    else:
        for status in statuses:
            print(status.one_line())
        if args.lane_sel == "all":
            print(
                f"SELECT   : {chosen.lane if chosen else '(none — enqueue, or Claude only under the R-A ledger note)'}"
                "   [§ 10.3 deterministic order: " + " -> ".join(ls.VENDOR_ORDER) + "]"
            )

    if args.shell_fallback:
        print()
        print(ls.shell_fallback_doc(lanes[0]))

    if args.safe_to_fire:
        # ONE BIT, for the caller whose question is only "may I fire?". For `all` the
        # bit is the SELECTION LAW's answer — is there any vendor lane I may fire —
        # which is the question a dispatcher actually asks at that scope.
        return 0 if (chosen is not None if args.lane_sel == "all" else statuses[0].safe_to_fire) else 1

    if args.lane_sel != "all":
        return statuses[0].exit_code
    # `all` exits FAIL-CLOSED across lanes: the worst state present wins, so a caller
    # who reads only the exit code is never told "open" while a lane is occupied. The
    # per-lane answers are on stdout and in `--json`, and `--safe-to-fire` answers the
    # selection-law question instead.
    rank = {state: i for i, state in enumerate(ls.STATE_PRECEDENCE)}
    worst = min(statuses, key=lambda s: rank.get(s.state, 0))
    return worst.exit_code


def _cmd_lane_status(args: argparse.Namespace) -> int:
    """One QUEUE's view: auth + serial lane + backlog, with the busy check's verdict.

    **AMENDMENT A CHANGED THIS COMMAND'S PREDICATE.** It used to return
    `0 if (state.ok and queue.runlog.is_idle()) else 1`, and `is_idle()` is False
    whenever the last row is an `ENQUEUED` row — so a lane on which NOTHING was
    executing reported *"do not fire"* on backlog alone. Composed with P-9 (an
    ENQUEUED-but-undrained job IS the held state, and a hold may persist for as long
    as its named condition takes), one deliberately HELD job would have rendered the
    lane permanently unusable to every other job and every other session: *uptime is
    not utilization*, re-created through the instrument built to abolish it.

    The predicate is now `lane_status.safe_to_fire`, which is the SAME named predicate
    every other consumer binds to. `is_idle()` is still PRINTED, because an operator
    reading the screen wants the raw leg — but it no longer decides.
    """
    from . import lane_status as ls

    queue, harness = _lane_pieces(args)
    state = harness.availability()
    row = queue.runlog.last_row()
    pending = queue.pending()
    lane = getattr(args, "lane", None) or "codex"
    status = ls.lane_status(
        lane,
        auth_probe=lambda: state,
        extra_runlogs=[queue.runlog.path],
    )
    print(f"lane      : {lane}")
    print(f"auth/lane : {state.state} — {state.reason}")
    print(f"last row  : {'  '.join(row) if row else '(none — nothing has ever run)'}")
    print(f"terminal  : {queue.runlog.is_idle()}   (leg 3 raw; NOT the fire predicate)")
    print(f"pending   : {len(pending)} job(s)" + (
        "  [" + ", ".join(f"{j.job_id}->{j.curator}" for j in pending[:8]) + "]"
        if pending else ""
    ))
    print(f"CHECK     : {status.state} — {status.reason}")
    for advisory in status.advisories:
        print(f"advisory  : {advisory}")
    blocked = queue.root / "AUTH-BLOCKED.md"
    if blocked.exists():
        print(f"\n!! {blocked} exists — an unfiled matt_to_do row is waiting")
    return status.exit_code


def _cmd_lane_enqueue(args: argparse.Namespace) -> int:
    queue, _ = _lane_pieces(args)
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    try:
        job = queue.enqueue(
            job_id=args.job_id,
            prompt=prompt,
            curator=args.curator,
            job_class=args.job_class,
            output_path=args.output,
            sandbox=args.sandbox,
            web_search=args.web_search,
            min_output_bytes=args.min_output_bytes,
            enqueued_by=args.enqueued_by or "",
            router=args.router,
        )
    except ValueError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"enqueued {job.job_id}  curator={job.curator}  sandbox={job.sandbox}")
    return 0


def _cmd_lane_drain(args: argparse.Namespace) -> int:
    queue, harness = _lane_pieces(args)
    report = queue.drain(harness, limit=args.limit)
    print(f"lane {report.lane_state}: fired={report.fired} skipped={report.skipped} "
          f"deferred={report.deferred} handed-to-claude={report.handed_to_claude}")
    for outcome in report.outcomes:
        print(f"  {outcome.job_id:<32} {outcome.marker:<16} curator={outcome.curator}"
              + (f"  {outcome.error[:120]}" if outcome.error else ""))
    if report.stopped_reason:
        print(f"\nSTOPPED: {report.stopped_reason}", file=sys.stderr)
        return 2
    return 0 if report.handed_to_claude == 0 else 1


def _cmd_custody(args: argparse.Namespace) -> int:
    """**D-9 — agent-level seam custody.** `check` is read-only and emits nothing.

    Four verbs, one ledger:

        factory custody check [--seam <name>]   is a sub-agent mid-flight here?
        factory custody claim --seam ... --holder ... --intent ... --release-on ...
        factory custody release --seam ... --holder ... --evidence ...
        factory custody override --seam ... --holder ... --note ...

    `check` answers WHICH state — `free` · `held` · `stale` · `custody-unknown` — with
    exit codes BANDED exactly like `factory lane`'s, so a shell caller can bind to the
    predicate without knowing the vocabulary: **`[ $? -lt 20 ]` is safe to spawn.**
    Pinned in `MIGRATION.md`.

    `check` is a DIFFERENT KIND OF COMMAND from the other three, in the same way
    `factory lane` is: it locks nothing, creates nothing, and writes nothing — not even
    the ledger file, if it does not exist yet.
    """
    from . import custody as cu

    ledger = Path(args.ledger) if args.ledger else None

    if args.custody_cmd == "check":
        answers = cu.custody_check(args.seam, ledger=ledger)
        if args.json:
            import json as _json

            print(_json.dumps({
                "seams": [a.to_dict() for a in answers],
                "safe_to_spawn_states": sorted(cu.SAFE_TO_SPAWN_STATES),
                "exit_codes": cu.CUSTODY_EXIT_CODES,
            }, indent=2))
        elif not answers:
            print("no open CLAIM in the ledger — every seam is free.")
        else:
            for answer in answers:
                print(answer.one_line())
        if args.safe_to_spawn:
            # ONE BIT, for the caller whose question is only "may I spawn here?".
            return 0 if all(a.safe_to_spawn for a in answers) else 1
        return answers[0].exit_code if args.seam else cu.worst_exit_code(answers)

    verbs = {
        "claim": lambda: cu.claim(
            seam=args.seam, holder=args.holder, intent=args.intent,
            release_on=args.release_on, detail=args.detail, ledger=ledger),
        "release": lambda: cu.release(
            seam=args.seam, holder=args.holder, evidence=args.evidence, ledger=ledger),
        "override": lambda: cu.override(
            seam=args.seam, holder=args.holder, note=args.note, ledger=ledger),
    }
    result = verbs[args.custody_cmd]()
    if args.json:
        import json as _json

        print(_json.dumps(result.to_dict(), indent=2))
    else:
        print(("OK      " if result.ok else "REFUSED ") + result.reason)
        if result.row is not None:
            print(f"  row: {result.row.to_line()}")
    return result.exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="factory", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="run a workflow")
    p_run.add_argument("workflow")
    p_run.add_argument("--run-id", default=None)
    p_run.set_defaults(func=_cmd_run)

    p_status = sub.add_parser("status", help="recent runs, red gates, token totals")
    p_status.add_argument("--limit", type=int, default=10)
    p_status.set_defaults(func=_cmd_status)

    p_report = sub.add_parser("report", help="markdown report for a run")
    p_report.add_argument("run_id")
    p_report.add_argument("--out", default=None)
    p_report.set_defaults(func=_cmd_report)

    p_gates = sub.add_parser("gates", help="list registered gates")
    p_gates.set_defaults(func=_cmd_gates)

    p_det = sub.add_parser("determinism", help="run twice; compare gate verdicts (R-BR-51)")
    p_det.add_argument("workflow")
    p_det.add_argument("--quiet", action="store_true")
    p_det.set_defaults(func=_cmd_determinism)

    p_probe = sub.add_parser("probe-agent", help="one live headless call against a seam agent")
    p_probe.add_argument("seam")
    p_probe.add_argument(
        "--prompt", default="Reply with exactly the word OK. Do not use any tools."
    )
    p_probe.add_argument("--cwd", default=None)
    p_probe.add_argument("--timeout-s", dest="timeout_s", type=int, default=300)
    p_probe.set_defaults(func=_cmd_probe_agent)

    p_lane = sub.add_parser(
        "lane", help="THE cross-session busy check (read-only; acquires and writes nothing)")
    p_lane.add_argument("--lane", dest="lane_sel", default="all",
                        choices=["codex", "grok", "all"],
                        help="which vendor lane to answer for (default: all, fail-closed)")
    p_lane.add_argument("--json", action="store_true", help="machine-readable answer")
    p_lane.add_argument("--safe-to-fire", dest="safe_to_fire", action="store_true",
                        help="collapse the exit code to 0 (fire) / 1 (do not)")
    p_lane.add_argument("--queue-dir", dest="queue_dir", default=None,
                        help="also read this queue root's _run-log.tsv as a leg-3 surface")
    p_lane.add_argument("--no-auth", dest="no_auth", action="store_true",
                        help="skip the auth probe (legs 1-3 only; faster, and strictly weaker)")
    p_lane.add_argument("--shell-fallback", dest="shell_fallback", action="store_true",
                        help="print the pure-shell degraded recipe for a python-less session")
    p_lane.set_defaults(func=_cmd_lane)

    p_ls = sub.add_parser("lane-status", help="one queue's auth + serial lane + backlog")
    p_ls.add_argument("queue_dir")
    p_ls.add_argument("--lane", default="codex", choices=["codex", "grok"])
    p_ls.set_defaults(func=_cmd_lane_status)

    p_le = sub.add_parser("lane-enqueue", help="add one job to a vendor-lane queue")
    p_le.add_argument("queue_dir")
    p_le.add_argument("job_id")
    p_le.add_argument("prompt_file")
    p_le.add_argument("--lane", default="codex", choices=["codex", "grok"])
    # D-3. A convention with a door: `router=Q3-NO` in the enqueue row's free-form
    # detail column makes lane contention countable (`grep -c "router=Q3-NO"`) without
    # touching the column count. Optional on purpose — a job enqueued on an OPEN lane
    # has no router verdict to record, and a defaulted token would fabricate one.
    p_le.add_argument("--router", default="",
                      help="router verdict token for the detail column, e.g. Q3-NO")
    # REQUIRED at the argparse layer as well as at the queue layer. U-4 R-B makes an
    # unnamed curator a refusal to fire, and a flag that DEFAULTS is a flag that gets
    # left off — the governance line would then be enforced by whoever typed the
    # command remembering it, which is the state R-B exists to replace.
    p_le.add_argument("--curator", required=True,
                      help="the named Claude agent who owns this output downstream (REQUIRED)")
    p_le.add_argument("--job-class", dest="job_class", default="research")
    p_le.add_argument("--output", default=None)
    p_le.add_argument("--sandbox", default="read-only")
    p_le.add_argument("--web-search", dest="web_search", action="store_true")
    p_le.add_argument("--min-output-bytes", dest="min_output_bytes", type=int, default=0)
    p_le.add_argument("--enqueued-by", dest="enqueued_by", default=None)
    p_le.set_defaults(func=_cmd_lane_enqueue)

    p_ld = sub.add_parser("lane-drain", help="drain a vendor-lane queue serially")
    p_ld.add_argument("queue_dir")
    p_ld.add_argument("--lane", default="codex", choices=["codex", "grok"])
    p_ld.add_argument("--limit", type=int, default=None)
    p_ld.set_defaults(func=_cmd_lane_drain)

    # --- D-9: agent-level seam custody (spec § 11, Amendments K + L) -------
    p_cu = sub.add_parser(
        "custody", help="agent-level SEAM custody: who is mid-flight in this seam?")
    p_cu.add_argument("--ledger", default=None,
                      help="ledger path (default: lanes/agents/_custody.tsv)")
    p_cu.add_argument("--json", action="store_true", help="machine-readable answer")
    p_cu.set_defaults(func=_cmd_custody)
    cu_sub = p_cu.add_subparsers(dest="custody_cmd", required=True)

    p_cu_check = cu_sub.add_parser(
        "check", help="READ-ONLY: is a sub-agent mid-flight in this seam?")
    p_cu_check.add_argument("--seam", default=None,
                            help="one seam by name (default: every seam with an open claim)")
    p_cu_check.add_argument("--safe-to-spawn", dest="safe_to_spawn", action="store_true",
                            help="collapse the exit code to 0 (spawn) / 1 (do not)")

    p_cu_claim = cu_sub.add_parser(
        "claim", help="ATOMIC check-and-append: take the seam, or be told who holds it")
    p_cu_claim.add_argument("--seam", required=True)
    p_cu_claim.add_argument("--holder", required=True,
                            help="the SESSION that must be alive, e.g. gandalf-session-85515")
    p_cu_claim.add_argument("--intent", required=True, help="what the sub-agent is being sent to do")
    # AMENDMENT L, at the argparse layer AND in `custody.refuse_reason_for_claim_arguments`.
    # Required in both places on purpose: a governance line enforced only by the CLI is a
    # governance line an API caller walks straight past, and a flag that DEFAULTS is a
    # flag that gets left off. Same lesson as U-4 R-B's `--curator`.
    p_cu_claim.add_argument("--release-on", dest="release_on", required=True,
                            help="the CONDITION whose satisfaction produces the RELEASE (REQUIRED)")
    p_cu_claim.add_argument("--detail", default="", help="extra `k=v` tokens for the detail column")

    p_cu_release = cu_sub.add_parser("release", help="close a claim, citing its completion evidence")
    p_cu_release.add_argument("--seam", required=True)
    p_cu_release.add_argument("--holder", required=True, help="the session writing the RELEASE")
    p_cu_release.add_argument("--evidence", required=True,
                              help="the completion record / commit this release rests on (REQUIRED)")

    p_cu_override = cu_sub.add_parser(
        "override", help="clear a STALE claim — loud, manual, never a TTL")
    p_cu_override.add_argument("--seam", required=True)
    p_cu_override.add_argument("--holder", required=True, help="the session performing the override")
    p_cu_override.add_argument("--note", required=True,
                               help="WHY the stale claim is being cleared (REQUIRED)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
