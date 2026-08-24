"""factory CLI — terminal commands, no daemon (Spec A § 1).

    factory run <workflow.yaml>       run a workflow to completion
    factory status                    live/last runs, red gates, token totals
    factory report <run_id>           the generated per-run markdown report
    factory gates                     list registered gates (grep-able inventory)
    factory determinism <workflow>    run twice, compare gate verdicts (R-BR-51)
    factory probe-agent <seam>        one live headless call; verifies the lane

    factory lane-status <queue-dir>   auth + serial-lane + last-row liveness, one screen
    factory lane-enqueue <queue-dir>  add one job (--curator is REQUIRED; U-4 R-B)
    factory lane-drain <queue-dir>    drain the queue serially; safe to re-fire

The three `lane-*` commands are the uptime half of U-4: hand-fired scripts were the
bridge, the queue is the uptime. `lane-drain` is idempotent and crash-safe, so the
correct response to "did that finish?" is to run it again.
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
    from .harness.codex import CodexHarness
    from .jobqueue import JobQueue

    return JobQueue(Path(args.queue_dir)), CodexHarness()


def _cmd_lane_status(args: argparse.Namespace) -> int:
    """The U-4 router's question (3), answered in one place instead of two habits.

    *"Lane open?"* is `last _run-log.tsv row terminal` AND `auth valid`, and until now
    those were a `tail -1` and a `codex login status` that a dispatcher had to remember
    to run in the right order. Exit code is the answer: 0 = fire, 1 = do not.
    """
    queue, harness = _lane_pieces(args)
    state = harness.availability()
    row = queue.runlog.last_row()
    pending = queue.pending()
    print(f"auth/lane : {state.state} — {state.reason}")
    print(f"last row  : {'  '.join(row) if row else '(none — nothing has ever run)'}")
    print(f"terminal  : {queue.runlog.is_idle()}")
    print(f"pending   : {len(pending)} job(s)" + (
        "  [" + ", ".join(f"{j.job_id}->{j.curator}" for j in pending[:8]) + "]"
        if pending else ""
    ))
    blocked = queue.root / "AUTH-BLOCKED.md"
    if blocked.exists():
        print(f"\n!! {blocked} exists — an unfiled matt_to_do row is waiting")
    return 0 if (state.ok and queue.runlog.is_idle()) else 1


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

    p_ls = sub.add_parser("lane-status", help="auth + serial lane + last-row liveness")
    p_ls.add_argument("queue_dir")
    p_ls.set_defaults(func=_cmd_lane_status)

    p_le = sub.add_parser("lane-enqueue", help="add one job to a vendor-lane queue")
    p_le.add_argument("queue_dir")
    p_le.add_argument("job_id")
    p_le.add_argument("prompt_file")
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
    p_ld.add_argument("--limit", type=int, default=None)
    p_ld.set_defaults(func=_cmd_lane_drain)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
