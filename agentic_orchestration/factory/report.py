"""Tier-0 surface — `factory status` and the per-run markdown report.

Strategy § 7. Three disciplines hold here:
  (1) ONE DATA PATH — everything below reads the same SQLite the gates write. A
      view is never truth.
  (2) READ-MOSTLY — nothing in this module writes to the receipts DB.
  (3) NO DASHBOARD BEFORE RECEIPTS — this is the terminal surface that ships with
      the spine; Tier 2 waits for two compiled workflows' worth of receipts.

The generated report is the run's mechanical shadow of a wind-down note. It is
git-ignored working state unless a human deliberately promotes it.
"""

from __future__ import annotations

import json
from typing import Any

from .receipts import Receipts


def _tok(value: Any) -> str:
    return "NULL" if value is None else f"{int(value):,}"


def _usage_line(row: Any) -> str:
    addends = [
        row["input_tokens"],
        row["output_tokens"],
        row["cache_read_tokens"],
        row["cache_write_tokens"],
    ]
    present = [a for a in addends if a is not None]
    if not present:
        return f"NULL ({row['usage_absent_reason'] or 'no reason recorded'})"
    total = sum(present)
    line = (
        f"in {_tok(row['input_tokens'])} · out {_tok(row['output_tokens'])} · "
        f"cache_r {_tok(row['cache_read_tokens'])} · cache_w {_tok(row['cache_write_tokens'])} "
        f"· **{total:,} billable**"
    )
    if row["reasoning_tokens"] is not None:
        line += f" (reasoning {_tok(row['reasoning_tokens'])}, a share of output)"
    if row["dollars"] is not None:
        line += f" · ${row['dollars']:.4f} [{row['dollars_source'] or 'source unrecorded'}]"
    return line


# How each recorded `dollars_source` reads to a human. A source with no gloss is
# rendered raw rather than guessed at — an unlabelled number is the failure mode
# this whole mechanism exists to prevent.
_DOLLARS_GLOSS = {
    "harness_reported_imputed": (
        "harness-reported list-price imputation, NOT a billed amount on a "
        "subscription lane"
    ),
}


def _dollars_line(totals: dict[str, Any]) -> str:
    """Render the summed dollars WITH the provenance recorded alongside it.

    The v1 build hard-coded the subscription-lane caveat into this string. That is
    the same defect as dropping the label: the number and its meaning were joined by
    the renderer's assumption rather than by the receipt (DRIFT-CRITIC D-4). If a
    future lane records a different source, this reads it out and the caveat changes
    with the data. If a source is recorded that nothing here recognises, the raw
    token is printed — never silently dressed as something familiar.
    """
    dollars = totals["dollars"]
    if dollars is None:
        return "NULL (no lane priced this run)"
    sources = [s for s in totals.get("dollars_sources") or [] if s]
    if not sources:
        return (
            f"${dollars:.4f} — **provenance unrecorded**; this figure cannot be read "
            "as money spent"
        )
    label = " + ".join(_DOLLARS_GLOSS.get(s, f"source `{s}` (no gloss registered)") for s in sources)
    return f"${dollars:.4f} — {label}"


def render_run_report(receipts: Receipts, run_id: str) -> str:
    session = receipts.session(run_id)
    if session is None:
        return f"# run {run_id}\n\nNo such run in receipts.\n"
    phases = receipts.phases(run_id)
    totals = receipts.usage_totals(run_id)

    out: list[str] = []
    out.append(f"# Run report — `{run_id}`\n")
    out.append(f"**Workflow:** {session['workflow']} (`{(session['workflow_sha256'] or '')[:12]}…`)")
    out.append(f"**Status:** **{session['status']}**")
    out.append(f"**Started:** {session['started_at']} · **Ended:** {session['ended_at'] or '—'}")
    out.append(f"**Root:** `{session['root']}`")
    if session["abort_reason"]:
        out.append(f"\n> **ABORTED —** {session['abort_reason']}")
    out.append("")

    greens = sum(1 for p in phases if p["status"] == "PASS")
    out.append(f"## Phases — {greens}/{len(phases)} green\n")
    out.append("| # | phase | agent | verdict | attempts | usage |")
    out.append("|---|---|---|---|---|---|")
    for p in phases:
        mark = "PASS" if p["status"] == "PASS" else f"**{p['status']}**"
        out.append(
            f"| {p['idx'] + 1} | {p['name']} | {p['agent'] or '_mechanical_'} | {mark} "
            f"| {p['attempts']} | {_usage_line(p)} |"
        )
    out.append("")

    out.append("## Gate verdicts\n")
    for p in phases:
        gates = receipts.gates_for_phase(p["id"])
        out.append(f"### {p['name']} — {p['status']}")
        if not gates:
            out.append("_no gate results recorded_\n")
            continue
        for g in gates:
            mark = "OK " if g["status"] == "PASS" else "RED"
            out.append(f"- `{mark}` **{g['gate']}** — {g['status']} — {g['detail']}")
            if g["status"] != "PASS":
                try:
                    evidence = json.loads(g["evidence_json"] or "{}")
                except json.JSONDecodeError:
                    evidence = {}
                for key in ("missing", "empty", "absent", "broken", "unclaimed", "problems",
                            "failures"):
                    if evidence.get(key):
                        out.append(f"    - {key}: `{evidence[key]}`")
        if p["error"]:
            out.append(f"- phase error: `{p['error'][:400]}`")
        out.append("")

    out.append("## Totals\n")
    out.append(
        f"- tokens: in {_tok(totals['input_tokens'])} · out {_tok(totals['output_tokens'])} · "
        f"cache_r {_tok(totals['cache_read_tokens'])} · cache_w {_tok(totals['cache_write_tokens'])}"
    )
    out.append(f"- billable token total: **{_tok(totals['billable_token_total'])}** "
               "(reasoning excluded by law — it is a share of output)")
    out.append(f"- dollars: {_dollars_line(totals)}")
    out.append("")

    breaches = [e for e in receipts.events(run_id) if e["kind"] == "permissions_breach"]
    if breaches:
        out.append("## Permissions breaches\n")
        for e in breaches:
            out.append(f"- {e['ts']}: `{e['detail']}`")
        out.append("")

    out.append(f"_Generated from `{receipts.path}` — one data path; this report is a view._\n")
    return "\n".join(out)


def render_status(receipts: Receipts, limit: int = 10) -> str:
    sessions = receipts.sessions(limit)
    if not sessions:
        return "No runs in receipts yet.\n"
    out = [f"factory status — {receipts.path}", ""]
    for s in sessions:
        phases = receipts.phases(s["run_id"])
        greens = sum(1 for p in phases if p["status"] == "PASS")
        totals = receipts.usage_totals(s["run_id"])
        tokens = totals["billable_token_total"]
        out.append(
            f"{s['status']:<8} {s['run_id']:<52} {greens}/{len(phases)} phases green"
            f"   tokens={'NULL' if tokens is None else f'{tokens:,}'}"
        )
        for p in phases:
            if p["status"] != "PASS":
                reds = [
                    g["gate"]
                    for g in receipts.gates_for_phase(p["id"])
                    if g["status"] != "PASS"
                ]
                out.append(
                    f"         └─ {p['name']}: {p['status']}"
                    + (f"  red gates: {', '.join(reds)}" if reds else "")
                )
        if s["abort_reason"]:
            out.append(f"         └─ ABORT: {s['abort_reason']}")
    out.append("")
    return "\n".join(out)
