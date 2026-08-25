#!/usr/bin/env python3
"""board — the Tier-2 LOCAL FLEET BOARD (U-1 § 11.4, F-1: ONE local board).

Renders the same fold as `flight/bin/flight_report`, as columns, in a browser, plus the
AM-1 § 13.1 vendor LANES card. Serves on 127.0.0.1 only. Stdlib only — no npm, no build
step, no node_modules, nothing to install.

THE LAW (U-1 / engineering Discipline #74), enforced by construction here:
  * ZERO WRITE VERBS. The HTTP server answers GET/HEAD and nothing else; every other
    method is 405 before any handler runs. No form, no button, no endpoint mutates
    anything. `--render-to` writes one disposable HTML snapshot and is the only write
    this file can perform (same class as `flight_report` writing `report.md`).
  * NEVER IN THE DATA PATH. Every probe is a read. The lane probe is NON-ACQUIRING by
    deliberate deviation (see `lane_probe.py`) precisely so a refresh cannot steal the
    serial lane from a live drain.
  * ONE DATA PATH. The tape is read through star-lord's `flight/tape.py` + `schema.py`,
    and every fold helper (identity-from-ENQUEUE/START, SLA class medians, staleness,
    the lane-partition audit, the probes) AND THE WHOLE AM-1 § 13.1 LANE COMPOSITE
    (`LANE_CARDS`, the three legs, `lane_answer`, `state_marker` — the chip COLOUR,
    Amendment H's predicate included — `PROBE_MODE`, `Q62_CAVEAT`) is
    IMPORTED from `flight/bin/flight_report` — not reimplemented. If that import fails,
    this board renders RED and renders nothing else: a view that cannot reach its one
    derivation must not show a partial green.

NO AUTO-REFRESH, DELIBERATELY (drax, declared): leg 1 of the ratified busy check is
`lane_is_free()`, which ACQUIRES the serial lock and releases it in the same breath. A
self-refreshing board would therefore be a view that periodically takes the serial lane,
and a concurrent `lane-drain` could see `LaneBusy` and refuse — a view walking into the
data path through its own instrument. So this page carries no meta-refresh and no poller:
a render happens when a human asks for one, exactly like running the CLI check. The card
shows `acquired: yes/no` so the reader knows when a kernel object was touched.
  * NO LLM anywhere. No network except the vendor CLIs' own auth checks.
  * Rebuilt from disk on EVERY request. No board-side state, no cache that can disagree.
  * Honest nulls. A failed probe is loud; a null is declared, never dressed as a zero.

SCHEMA-VERSION TOLERANCE (v1 and v1.1 both): the lane vocabulary rename
(`grok-judge` → `grok-serial`), the `grok-sub` currency and the CLOSE-only `cost_usd`
field are read defensively — `cost_usd` renders only where rows carry it, and both grok
lane spellings map to the one grok vendor lane. The board never validates the tape (that
is the custodian's job); it renders what is there and says what is missing.

USAGE
  python3 agentic_orchestration/factory/ui/board.py                 # serve 127.0.0.1:8787
  python3 agentic_orchestration/factory/ui/board.py --port 9000
  python3 agentic_orchestration/factory/ui/board.py --render-to /tmp/fleet.html --once
  open http://127.0.0.1:8787/
"""

from __future__ import annotations

import argparse
import datetime
import html
import importlib.machinery
import importlib.util
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
FACTORY_DIR = os.path.dirname(HERE)
AO_DIR = os.path.dirname(FACTORY_DIR)
REPO_ROOT = os.path.dirname(AO_DIR)
FLIGHT_DIR = os.path.join(AO_DIR, "flight")

sys.path.insert(0, HERE)
sys.path.insert(0, FLIGHT_DIR)

BOARD_VERSION = "u1-b3b-1"


def load_flight_report():
    """Import star-lord's Tier-1 renderer AS A MODULE (it is `flight/bin/flight_report`,
    a script with no `.py` suffix and a `__main__` guard). This is the one-data-path
    move: his fold helpers, his SLA, his probes, his partition audit."""
    path = os.path.join(FLIGHT_DIR, "bin", "flight_report")
    spec = importlib.util.spec_from_loader(
        "flight_report", importlib.machinery.SourceFileLoader("flight_report", path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- html helpers
def E(s):
    return html.escape("" if s is None else str(s), quote=True)


def NULL(label="null"):
    """A declared null. Never a zero, never an empty cell."""
    return '<span class="null">— %s</span>' % E(label)


CSS = """
:root{--bg:#0b1017;--panel:#121a24;--edge:#243244;--ink:#d7e2ee;--dim:#8fa3b8;
--amber:#e5a83a;--red:#e2544c;--green:#4bb372;--accent:#7fb2e5;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:13px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
a{color:var(--accent)}
header{padding:14px 18px 10px;border-bottom:1px solid var(--edge);background:#0e141d;}
h1{font-size:15px;margin:0 0 4px;letter-spacing:.06em}
.tag{display:inline-block;border:1px solid var(--edge);border-radius:3px;padding:1px 6px;
margin-left:6px;font-size:10px;color:var(--dim);letter-spacing:.08em}
.sub{color:var(--dim);font-size:11.5px;margin-top:3px}
.law{color:var(--dim);font-size:11.5px;margin-top:6px;border-left:2px solid var(--edge);
padding-left:8px}
.coverage{margin:12px 18px 0;padding:8px 10px;border:1px solid var(--edge);
border-left:3px solid var(--amber);background:#141c26;color:#cbd8e6;font-size:11.5px}
.cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;padding:12px 18px}
@media(max-width:1200px){.cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:720px){.cols{grid-template-columns:minmax(0,1fr)}}
.lane{background:var(--panel);border:1px solid var(--edge);border-radius:4px;
display:flex;flex-direction:column;min-height:120px}
.lane>h2{font-size:12px;margin:0;padding:8px 10px;border-bottom:1px solid var(--edge);
letter-spacing:.05em;color:#e8f0f8;background:#16202c;border-radius:4px 4px 0 0}
.lane>h2 .n{color:var(--dim);font-weight:400}
.cards{padding:8px;display:flex;flex-direction:column;gap:7px}
.card{border:1px solid var(--edge);border-radius:3px;padding:6px 8px;background:#0f1720}
.card .t{color:#eaf2fa;word-break:break-all}
.card .m{color:var(--dim);font-size:11px;margin-top:2px}
.empty{padding:10px;color:var(--dim);font-size:11.5px}
.null{color:#6f8296;font-style:italic}
section{margin:12px 18px;background:var(--panel);border:1px solid var(--edge);border-radius:4px}
section>h2{font-size:12px;margin:0;padding:8px 10px;border-bottom:1px solid var(--edge);
background:#16202c;letter-spacing:.05em}
.body{padding:10px}
table{border-collapse:collapse;width:100%;font-size:11.5px}
th,td{border:1px solid var(--edge);padding:4px 6px;text-align:left;vertical-align:top}
th{background:#16202c;color:#cfe0f0;font-weight:600}
.lanes{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:10px}
.vcard{border:1px solid var(--edge);border-radius:3px;background:#0f1720}
.vcard h3{margin:0;padding:6px 8px;font-size:12px;border-bottom:1px solid var(--edge);
background:#141d28}
.vcard .rows{padding:6px 8px}
.kv{display:grid;grid-template-columns:104px 1fr;gap:2px 8px;font-size:11.5px}
.kv .k{color:var(--dim)}
.state{display:inline-block;padding:0 6px;border-radius:3px;font-weight:700;font-size:11px}
.s-open{background:#123020;color:#79d79b;border:1px solid #1f6b41}
.s-busy{background:#3a1f1c;color:#ffa79f;border:1px solid #7d3a34}
.s-warn{background:#332714;color:#ecc06a;border:1px solid #7a5a20}
.s-unknown{background:#20262e;color:#9fb2c6;border:1px solid #39465a}
.degraded{color:var(--amber)}
.fail{color:var(--red)}
.ok{color:var(--green)}
.note{color:var(--dim);font-size:11px;margin-top:6px}
footer{color:var(--dim);font-size:11px;padding:8px 18px 22px}
.err{margin:18px;padding:14px;border:2px solid var(--red);background:#25161a;color:#ffd7d2;
white-space:pre-wrap;font-size:12px}
"""


# ---------------------------------------------------------------- rollups
# The formulas below are the SAME ones `flight_report` renders in its SEALED table and
# per-model scorecard, expressed over the same imported primitives (`unit_event`,
# `unit_identity`, `unit_duration`, `human_n`, `fmt_span`, `median`). They are re-expressed
# rather than imported because star-lord computes them inline inside `render()`; the
# CONVERGENCE POINT is his exposing them as functions, at which point these three
# helpers delete. Any divergence is a render bug and shows up as a number that disagrees
# with `flight/report.md` for the same tape — which is the check galadriel can run.
def sealed_by_workstream(fr, rows, sealed):
    out = []
    groups = {}
    for u in sealed:
        groups.setdefault(fr.unit_identity(u).get("workstream") or "(no workstream)",
                          []).append(u)
    for ws, us in sorted(groups.items()):
        closes = [fr.unit_event(u, "CLOSE") for u in us]
        n = len(us)
        rcs = [c.get("rc") for c in closes if c.get("rc") is not None]
        vcount = {}
        for c in closes:
            if c.get("verdict"):
                vcount[c["verdict"]] = vcount.get(c["verdict"], 0) + 1
        cur_rows = [r for r in rows if r["event"] == "CURATION" and r.get("workstream") == ws]
        tin = sum(c.get("tokens_input") or 0 for c in closes)
        tcache = sum(c.get("tokens_cached_input") or 0 for c in closes)
        tout = sum(c.get("tokens_output") or 0 for c in closes)
        n_tok = len([c for c in closes if c.get("tokens_input") is not None])
        # v1.1 tolerance: `cost_usd` is CLOSE-only + optional. Sum only over rows that
        # carry it, and ALWAYS report the denominator, so a partial sum can never read
        # as a run total.
        usd_rows = [c for c in closes if c.get("cost_usd") is not None]
        firsts = [fr.parse_ts(u["rows"][0]["ts"]) for u in us]
        lasts = [fr.parse_ts(fr.unit_event(u, "CLOSE")["ts"]) for u in us]
        out.append(dict(
            ws=ws, n=n, rcs=rcs, verdicts=vcount,
            curation_rows=len(cur_rows),
            warns=sum(r.get("warn_count") or 0 for r in cur_rows),
            tin=tin, tcache=tcache, tout=tout, n_tok=n_tok,
            usd=sum(c["cost_usd"] for c in usd_rows), n_usd=len(usd_rows),
            currencies=sorted({c.get("currency") for c in closes if c.get("currency")}),
            span=(max(lasts) - min(firsts)).total_seconds()))
    return out


def scorecard(fr, sealed):
    groups = {}
    for u in sealed:
        ident = fr.unit_identity(u)
        groups.setdefault((ident.get("provider") or "—",
                           ident.get("pin") or "(no pin recorded)"), []).append(u)
    out = []
    for (prov, pin), us in sorted(groups.items()):
        closes = [fr.unit_event(u, "CLOSE") for u in us]
        rcs = [c.get("rc") for c in closes if c.get("rc") is not None]
        tin = sum(c.get("tokens_input") or 0 for c in closes)
        usd_rows = [c for c in closes if c.get("cost_usd") is not None]
        out.append(dict(
            provider=prov, pin=pin, n=len(us),
            have_tokens=any(c.get("tokens_input") is not None for c in closes),
            rcs=rcs, tin=tin,
            tcache=sum(c.get("tokens_cached_input") or 0 for c in closes),
            tout=sum(c.get("tokens_output") or 0 for c in closes),
            artifacts=sum(len(c.get("artifacts") or []) for c in closes),
            durs=[d for d in (fr.unit_duration(u) for u in us) if d is not None],
            usd=sum(c["cost_usd"] for c in usd_rows), n_usd=len(usd_rows)))
    return out


def latest_snapshots(rows):
    """Latest SNAPSHOT per currency — the window meters, as the meter reported them."""
    out = {}
    for r in rows:
        if r.get("event") != "SNAPSHOT":
            continue
        cur = r.get("currency") or "(no currency)"
        if cur not in out or r["ts"] > out[cur]["ts"]:
            out[cur] = r
    return out


def pin_drift(fr, units):
    """The `model_echo` ≠ `pin` tripwire, as THREE COUNTED POPULATIONS: mismatching,
    comparable-and-matching, and echo-without-pin.

    A unit that echoes a model but pinned nothing is NOT COMPARABLE — not a match and not a
    miss. Folding it into "none disagree" manufactures a green out of a unit that pinned
    nothing, which is exactly what S7/D1 caught this cell doing (galadriel; ruled FALSE-GREEN
    and BLOCKING at L-25). The absence of a disagreement is not the presence of an agreement,
    and on a board read at a glance, green is read faster than the sentence beside it.

    GRAIN AND COMPARISON ARE TIER-1'S, verbatim — per UNIT via `unit_identity` rather than per
    raw row, and `model_echo != pin` whole rather than `pin.split("@")[0] != echo`. Both were
    board-local divergences before this fix: two windows comparing two different things under
    one name is the desync class the Tier-2 gate exists to prevent.

    RE-EXPRESSED rather than imported for the same reason as the rollup helpers above —
    star-lord computes it inline inside `flight_report.render()`. The CONVERGENCE POINT is his
    exposing it as a function (as B-1c just did for `state_marker`), at which point this helper
    deletes. Any divergence shows up as a `pin drift` cell that disagrees with
    `flight/report.md` on the same tape, which is the check galadriel can run.
    """
    drift, comparable, echo_only = [], 0, 0
    for u in units.values():
        ident = fr.unit_identity(u)
        if not ident.get("model_echo"):
            continue
        if not ident.get("pin"):
            echo_only += 1
            continue
        comparable += 1
        if ident["model_echo"] != ident["pin"]:
            drift.append(dict(unit=u["latest"]["unit_id"], pin=ident["pin"],
                              echo=ident["model_echo"]))
    return dict(drift=drift, comparable=comparable, echo_only=echo_only, total=len(units))


# ---------------------------------------------------------------- the render
def render_html(records_dir, repo_root, now, run_probes=True, lane_probes=True):
    try:
        fr = load_flight_report()
    except Exception:                                               # noqa: BLE001
        return error_page("cannot import flight/bin/flight_report — the board's ONE "
                          "derivation is unreachable, so nothing is rendered",
                          traceback.format_exc(), now)

    import schema
    import tape as tapemod

    rows, raw_count = tapemod.load(records_dir)
    units = schema.fold(rows)
    tape_names = [os.path.basename(p) for p in tapemod.tape_files(records_dir)]

    # ---- lanes: the PARTITION is star-lord's, verbatim (flight_report FINDING-2) —
    # IN-FLIGHT / QUEUED / SEALED / UNBOUND, from `fold()`'s own vocabulary. AT-GATE and
    # the tape-side HALT list are OVERLAYS, not lanes: every unit they show also appears in
    # exactly one partition lane, and the columns say so loudly. The § 11.4 sketch draws
    # four columns; drawing AT GATE as a fifth PARTITION would have made this board's
    # IN-FLIGHT count disagree with `flight/report.md` for the same tape — two windows, two
    # numbers, which is the desync class the Tier-2 gate exists to prevent. Same fold, same
    # counts, one truth.
    by_state = {}
    for u in units.values():
        by_state.setdefault(u["state"], []).append(u)
    inflight = sorted(by_state.get("IN-FLIGHT", []), key=lambda u: u["latest"]["ts"])
    queued = sorted(by_state.get("QUEUED", []), key=lambda u: u["latest"]["ts"])
    sealed = by_state.get("SEALED", [])
    unbound = sorted([u for st, us in by_state.items()
                      if st not in ("IN-FLIGHT", "QUEUED", "SEALED") for u in us],
                     key=lambda u: u["latest"]["ts"])

    # OVERLAY 1 — open HALTs (star-lord's derivation, verbatim): a non-sealed unit with any
    # HALT row. OVERLAY 2 — open gates: the unit's LAST GATE row with no CLOSE at or after it.
    halts = sorted([u for u in units.values()
                    if u["state"] != "SEALED" and any(r["event"] == "HALT" for r in u["rows"])],
                   key=lambda u: u["latest"]["ts"])
    open_gates = []
    for u in units.values():
        gates = [r for r in u["rows"] if r["event"] == "GATE"]
        if not gates:
            continue
        g = gates[-1]
        if not [r for r in u["rows"] if r["event"] == "CLOSE" and r["ts"] >= g["ts"]]:
            open_gates.append(g)
    open_gates.sort(key=lambda r: r["ts"])

    membership = {
        "IN-FLIGHT": [u["latest"]["unit_id"] for u in inflight],
        "QUEUED": [u["latest"]["unit_id"] for u in queued],
        "SEALED": [u["latest"]["unit_id"] for u in sealed],
        "UNBOUND": [u["latest"]["unit_id"] for u in unbound],
    }
    partition_problems = fr.partition_audit(units, membership)

    # ---- probes (all reads; failures are surfaced, never swallowed)
    p = fr.Probes(repo_root)
    if run_probes:
        games = os.path.dirname(repo_root)
        for name in fr.SIBLING_REPOS:
            path = os.path.join(games, name)
            if os.path.isdir(os.path.join(path, ".git")):
                p.run("git:" + name, fr.probe_git(path))
        p.run("env:ENABLE_PROMPT_CACHING_1H", fr.probe_env_cache1h())
        p.run("matt_decision_needed", fr.probe_matt_queue(
            os.path.join(repo_root, "canonical/matt_decision_needed/README.md")))
        p.run("matt_to_do", fr.probe_matt_queue(
            os.path.join(repo_root, "canonical/matt_to_do/README.md")))
        p.run("requests-dirs", fr.probe_requests(os.path.join(repo_root,
                                                              "agentic_orchestration")))
        p.run("disk", fr.probe_disk(repo_root))
        # AM-1 § 13.1 lane legs — probe names IDENTICAL to `flight_report.render()`'s, so
        # the two windows read the same legs under the same keys. `lane-lock` + `proc-scan`
        # are shared across cards; auth + run-log are per-lane so one vendor's failure
        # never masks the other's state.
        if lane_probes:
            p.run("lane-lock", fr.probe_lane_lock())
            p.run("proc-scan", fr.probe_process_table())
            for cfg in fr.LANE_CARDS:
                p.run("auth:" + cfg["key"], fr.probe_vendor_auth(cfg))
                if cfg["runlogs"]:
                    p.run("runlog:" + cfg["key"], fr.probe_runlogs(cfg, repo_root))

    medians = fr.class_medians(units)
    cov = schema.coverage(rows)

    L = []
    A = L.append
    A("<!doctype html><html><head><meta charset='utf-8'>")
    A("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    A("<title>FLEET BOARD — %s</title><style>%s</style></head><body>"
      % (E(now.strftime("%Y-%m-%dT%H:%M:%SZ")), CSS))

    # ---- header
    A("<header><h1>FLEET BOARD"
      "<span class='tag'>SHOP-ONLY</span><span class='tag'>VIEW ONLY</span>"
      "<span class='tag'>TIER-2</span></h1>")
    # v1/v1.1 tolerance: SCHEMA_REVISION is the custodian-amendment marker and only exists
    # post-amendment; the row FORMAT version is SCHEMA_VERSION and is what rows are stamped
    # with. Read both defensively so the board renders against either tape state.
    revision = getattr(schema, "SCHEMA_REVISION", None)
    A("<div class='sub'>rendered %s · tape: %s (%d rows on disk; %d after corrections) · "
      "schema v%s (rows stamped <code>v:%d</code>) · probes %d/%d ran · board %s</div>"
      % (E(now.strftime("%Y-%m-%dT%H:%M:%SZ")), E(", ".join(tape_names) or "(none)"),
         raw_count, len(rows), E(revision or schema.SCHEMA_VERSION), schema.SCHEMA_VERSION,
         p.ran, p.total, BOARD_VERSION))
    A("<div class='law'>THE LAW (U-1): this board is a VIEW. Zero authority, zero write "
      "verbs, never in the data path. Every figure is derived from rows at render time and "
      "stored nowhere; every probe is a read. Rule from the ledgers, dispatches and queues "
      "— never from this page. Refresh re-folds the tape and re-runs the probes; closing "
      "the window loses nothing, because the board owns nothing.</div></header>")

    A("<div class='coverage'><b>COVERAGE:</b> tape begins %s. Every unit that started "
      "before the recorder existed is structurally invisible here — including the six "
      "2026-07-22 engine-seam dispatches this lane was created for. A lane count is a "
      "count of RECORDED units, never a census of the fleet.</div>"
      % E(cov["first_ts"] or "(no rows yet)"))

    if partition_problems:
        A("<div class='err'><b>RENDER CHECK FAILED — lane partition (%d)</b>\n%s</div>"
          % (len(partition_problems), E("\n".join(partition_problems))))

    # ---- the four columns
    A("<div class='cols'>")
    A(col_awaiting(p, halts, fr, now))
    A(col_inflight(inflight, queued, fr, now, medians, len(units)))
    A(col_atgate(open_gates, fr, now))
    A(col_sealed(fr, rows, sealed))
    A("</div>")

    # ---- LANES card (AM-1 § 13.1)
    A(section_lanes(p, fr, rows, units))

    # ---- HEALTH
    A(section_health(p, fr, rows, units, now))

    # ---- SEALED rollups + scorecards
    A(section_rollups(fr, rows, sealed))

    # ---- UNBOUND + probe failures
    A(section_residue(fr, unbound, p, now))

    A("<footer>`agentic_orchestration/factory/ui/board.py` · Tier-2 · SHOP-ONLY · "
      "F-1 ONE local board (the Spec B factory surface, extended to fleet scope). "
      "This page is disposable: close it and it rebuilds identically from the tape. "
      "Tier-1 sibling: <code>flight/report.md</code> (same fold, same helpers, "
      "regenerated by <code>flight/bin/flight_report</code>).</footer>")
    A("</body></html>")
    return "\n".join(L)


def error_page(headline, detail, now):
    return ("<!doctype html><html><head><meta charset='utf-8'><title>FLEET BOARD — RED"
            "</title><style>%s</style></head><body><header><h1>FLEET BOARD — RED</h1>"
            "<div class='sub'>%s</div></header><div class='err'><b>%s</b>\n\n%s</div>"
            "<footer>A view that cannot reach its one derivation renders red and renders "
            "nothing else. It does not fall back to a second derivation, because a second "
            "derivation is a second truth.</footer></body></html>"
            % (CSS, E(now.strftime("%Y-%m-%dT%H:%M:%SZ")), E(headline), E(detail)))


# ---------------------------------------------------------------- columns
def col_awaiting(p, halts, fr, now):
    dec = p.get("matt_decision_needed")
    act = p.get("matt_to_do")
    n_dec = len([r for r in (dec or {}).get("rows", []) if not r["struck"]]) if dec else None
    n_act = len([r for r in (act or {}).get("rows", []) if not r["struck"]]) if act else None
    total = (n_dec or 0) + (n_act or 0) + len(halts)
    L = ["<div class='lane'><h2>⏸ AWAITING MATT <span class='n'>(%s)</span></h2><div class='cards'>"
         % (total if dec and act else "?")]

    def queue_cards(probe_name, probe, label, path):
        out = []
        if probe is None:
            out.append("<div class='card'><div class='t'>%s</div><div class='m'>%s</div></div>"
                       % (E(label), p.line(probe_name, lambda _: "")))
            return out
        open_rows = [r for r in probe["rows"] if not r["struck"]]
        out.append("<div class='card'><div class='t'>%s — <b>%d open</b> / %d struck</div>"
                   "<div class='m'>%s · strike rule is mechanical: a row counts CLOSED only "
                   "when its <code>#</code> cell is struck</div></div>"
                   % (E(label), len(open_rows), probe["struck"], E(path)))
        for r in open_rows[:8]:
            out.append("<div class='card'><div class='t'>%s</div><div class='m'>%s</div></div>"
                       % (E(r["id"] or "(no id)"), E((r["title"] or "")[:110])))
        if len(open_rows) > 8:
            out.append("<div class='card'><div class='m'>… %d more open in %s</div></div>"
                       % (len(open_rows) - 8, E(path)))
        return out

    L += queue_cards("matt_decision_needed", p.get("matt_decision_needed"),
                     "DECISIONS", "canonical/matt_decision_needed/README.md")
    L += queue_cards("matt_to_do", p.get("matt_to_do"),
                     "ACTIONS", "canonical/matt_to_do/README.md")
    L.append("<div class='card'><div class='t'>HALTS / OPEN VETO WINDOWS (from tape)</div>"
             "<div class='m'>%s%s</div></div>"
             % ("none" if not halts else "%d open" % len(halts),
                "" if not halts else " · OVERLAY — each also appears in its partition lane"))
    for u in halts:
        h = [r for r in u["rows"] if r["event"] == "HALT"][-1]
        age = (now - fr.parse_ts(h["ts"])).total_seconds()
        L.append("<div class='card'><div class='t'>%s</div><div class='m'>HALT · %s · "
                 "waiting %s</div></div>"
                 % (E(h["unit_id"]), E(h.get("operator") or "operator —"),
                    E(fr.fmt_age(age))))
    L.append("</div><div class='empty'>The board RENDERS the two queue files; it never "
             "becomes them. The markdown stays the truth you rule in.</div></div>")
    return "".join(L)


def _sla_cell(fr, u, now, medians):
    age = (now - fr.parse_ts(u["latest"]["ts"])).total_seconds()
    ident = fr.unit_identity(u)
    lane = ident.get("lane") or u["latest"].get("lane")
    marker, rule = fr.staleness(age, lane, medians.get(fr.sla_class(u)))
    return age, marker, rule, ident, lane


def col_inflight(inflight, queued, fr, now, medians, n_units):
    L = ["<div class='lane'><h2>▶ IN-FLIGHT <span class='n'>(%d of %d units on tape)</span>"
         "</h2><div class='cards'>" % (len(inflight), n_units)]
    if not inflight:
        L.append("<div class='empty'>no unit on the tape has a START without a terminal "
                 "event</div>")
    for u in inflight:
        age, marker, rule, ident, lane = _sla_cell(fr, u, now, medians)
        L.append("<div class='card'><div class='t'>%s</div>"
                 "<div class='m'>%s · %s · owner %s · last actor %s</div>"
                 "<div class='m'>%s %s · last event %s · %s</div></div>"
                 % (E(u["latest"]["unit_id"]), E(ident.get("unit_kind")
                                                 or u["latest"].get("unit_kind") or "—"),
                    E(lane or "—"), E(ident.get("operator") or "—"),
                    E(fr.last_actor(u) or "—"),
                    marker, E(fr.fmt_age(age)), E(u["latest"]["event"]), E(rule)))
    L.append("</div><div class='empty'>queued (ENQUEUE seen, no START yet): %d%s</div></div>"
             % (len(queued),
                "" if not queued else " — " + ", ".join(E(u["latest"]["unit_id"])
                                                        for u in queued[:4])))
    return "".join(L)


def col_atgate(open_gates, fr, now):
    L = ["<div class='lane'><h2>🚧 AT GATE <span class='n'>(%d · overlay)</span></h2>"
         "<div class='cards'>" % len(open_gates)]
    if not open_gates:
        L.append("<div class='empty'>no GATE row without a CLOSE at or after it</div>")
    for g in open_gates:
        age = (now - fr.parse_ts(g["ts"])).total_seconds()
        L.append("<div class='card'><div class='t'>%s</div>"
                 "<div class='m'>%s · gatekeeper %s · verdict so far %s</div>"
                 "<div class='m'>waiting %s</div></div>"
                 % (E(g["unit_id"]), E(g.get("gate_id") or "(no gate_id)"),
                    E(g.get("gatekeeper") or "—"), E(g.get("verdict") or "(none filed)"),
                    E(fr.fmt_age(age))))
    L.append("</div><div class='empty'>An OVERLAY, not a partition lane: every unit here also "
             "appears in exactly one of IN-FLIGHT / QUEUED / SEALED / UNBOUND. Do not add this "
             "count to those.</div></div>")
    return "".join(L)


def col_sealed(fr, rows, sealed):
    L = ["<div class='lane'><h2>✓ SEALED <span class='n'>(%d)</span></h2><div class='cards'>"
         % len(sealed)]
    if not sealed:
        L.append("<div class='empty'>no terminal unit on the tape yet</div>")
    for g in sealed_by_workstream(fr, rows, sealed):
        rc_cell = ("%d/%d rc=0" % (len([r for r in g["rcs"] if r == 0]), len(g["rcs"]))
                   if g["rcs"] else "no rc on %d/%d units" % (g["n"], g["n"]))
        verdicts = (" · ".join("%d %s" % (v, k) for k, v in
                               sorted(g["verdicts"].items(), key=lambda kv: -kv[1]))
                    if g["verdicts"] else "0/%d judged" % g["n"])
        tok = ("%s in · %.1f%% cache · %s out" % (fr.human_n(g["tin"]),
                                                  100.0 * g["tcache"] / g["tin"],
                                                  fr.human_n(g["tout"]))
               if g["n_tok"] and g["tin"] else "tokens null on %d/%d units" % (g["n"], g["n"]))
        usd = ("$%.5f over %d/%d CLOSE rows" % (g["usd"], g["n_usd"], g["n"])
               if g["n_usd"] else "no cost_usd on any CLOSE row")
        L.append("<div class='card'><div class='t'>▣ %s</div>"
                 "<div class='m'>%d unit(s) · %s · %s</div>"
                 "<div class='m'>%s</div><div class='m'>%s · %s · %s</div></div>"
                 % (E(g["ws"]), g["n"], E(rc_cell), E(verdicts), E(tok), E(usd),
                    E("/".join(g["currencies"]) or "no currency recorded"),
                    E(fr.fmt_span(g["span"]))))
    L.append("</div><div class='empty'>rollups + scorecards render in full below</div></div>")
    return "".join(L)


# ---------------------------------------------------------------- LANES card
# AM-1 § 13.1. Every fact on these cards comes from `flight_report`'s composite —
# `LANE_CARDS` (the vendor descriptors), the three leg probes, and `lane_answer()` (the
# fail-closed union). This board CONTRIBUTES NO LANE DERIVATION OF ITS OWN: it renders
# the check's output as a card, which is exactly what Q62 ruled the board may do.
#
# THE CHIP COLOUR IS NOT THE BOARD'S RULE. It is star-lord's exported `state_marker()`, which
# B-1c made a function precisely so both tiers colour one predicate one way. The board maps his
# three markers onto its three chip classes and contributes no rule of its own — no string
# equality with `"open"`, no local severity table.
#
# What that buys, in the two directions the run ruled on:
#   * Amendment H (jack-ryan): `queue-pending` is SAFE-TO-FIRE — backlog is not occupancy — so
#     it colours WITH `open`, not against it. The retired local table hardcoded it amber, which
#     told Matt to look elsewhere at a lane he should have fired into.
#   * S7/D2 (galadriel): fire-safe on REDUCED LEG COVERAGE is amber, never green. grok wore the
#     same full-green chip as codex while its own card body declared 1-of-3-leg coverage — the
#     distinction Tier-1 drew in 🟡 vs 🟢 and this board lost at a glance, on a surface whose
#     stated use is "glance HERE before opening a vendor TUI". The leg count now rides inside
#     the chip so the reduction is legible without reading the card body.
_MARKER_CLASS_BY_SEVERITY = ("s-open", "s-warn", "s-busy")   # GREEN, AMBER, RED


def lane_chip(fr, ans):
    """The lane-state chip: star-lord's marker, this board's CSS, nothing in between."""
    cls = dict(zip((fr.GREEN, fr.AMBER, fr.RED),
                   _MARKER_CLASS_BY_SEVERITY)).get(fr.state_marker(ans), "s-unknown")
    legs = "" if not ans["na"] else " · %d of 3 legs" % (3 - len(ans["na"]))
    return "<span class='state %s'>%s%s</span>" % (cls, E(ans["state"]), E(legs))


def _lane_tape_activity(fr, rows, units, lane_key):
    """Last CLOSE on this vendor lane + the lane's pins, DERIVED from the lane's own rows.

    Lane membership is taken from the unit's folded identity (the same derivation
    `flight_report.lane_units()` uses), so a CLOSE row that does not itself repeat `lane`
    still lands on the right card.

    v1.1 tolerance: the grok stream is `grok-serial` post-amendment and `grok-judge` in the
    frozen v1 enum. Both spellings map to the grok card, so this renders correctly against
    a pre-amendment tape, a post-amendment tape, and a tape carrying both.
    """
    aliases = {lane_key}
    if lane_key in ("grok-serial", "grok-judge"):
        aliases = {"grok-serial", "grok-judge"}
    lane_us = [u for u in units.values() if fr.unit_identity(u).get("lane") in aliases]
    closes = [c for c in (fr.unit_event(u, "CLOSE") for u in lane_us) if c is not None]
    closes.sort(key=lambda r: r["ts"])
    pins = sorted({fr.unit_identity(u).get("pin") for u in lane_us
                   if fr.unit_identity(u).get("pin")})
    return (closes[-1] if closes else None), len(closes), len(lane_us), pins


def section_lanes(p, fr, rows, units):
    L = ["<section><h2>🛣 LANES — vendor lane cards, per vendor (AM-1 § 13.1) · "
         "glance HERE before opening a vendor TUI</h2><div class='body'>"]
    if p.status("proc-scan") == "not-run" and p.status("lane-lock") == "not-run":
        L.append("<div class='note'>%s</div></div></section>"
                 % NULL("lane probes skipped (--no-lane-probes) — no lane state is claimed"))
        return "".join(L)
    L.append("<div class='note degraded'><b>probe: %s</b> — the D-2 <code>factory lane</code> "
             "subcommand, which will answer all three legs under one pinned contract, does not "
             "exist yet (other workstream). Until it lands each card is a DEGRADED composite of "
             "the legs reachable today, and every leg says what it saw. Union rule: <b>busy if "
             "ANY leg says busy</b>; ambiguity renders busy, never open.</div>" % E(fr.PROBE_MODE))
    L.append("<div class='note'><b>Q62 instrument caveat, verbatim:</b> “%s”</div>"
             % E(fr.Q62_CAVEAT))
    L.append("<div class='lanes' style='margin-top:10px'>")
    for cfg in fr.LANE_CARDS:
        L.append(vendor_card(p, fr, rows, units, cfg))
    L.append(claude_card(fr, rows, units))
    L.append("</div></div></section>")
    return "".join(L)


def vendor_card(p, fr, rows, units, cfg):
    key, vendor = cfg["key"], cfg["vendor"]
    lock = p.results.get("lane-lock") if cfg["has_lane_lock"] else None
    procs = p.results.get("proc-scan")
    rls = p.results.get("runlog:" + key)
    auth = p.results.get("auth:" + key)
    ans = fr.lane_answer(cfg, lock, procs, rls, auth)

    L = ["<div class='vcard'><h3>%s %s "
         "<span class='null'>lane <code>%s</code> · provider <code>%s</code></span></h3>"
         "<div class='rows'>" % (E(vendor), lane_chip(fr, ans), E(key), E(cfg["provider"]))]
    kv = []
    kv.append(("why", "<br>".join(E(w) for w in ans["reasons"])))
    if ans["advisories"]:
        kv.append(("advisory", "<br>".join("<span class='degraded'>%s</span>" % E(a)
                                           for a in ans["advisories"])))
    if ans["unreachable"]:
        kv.append(("unreachable", "<span class='degraded'>%s</span>"
                   % E(" + ".join(ans["unreachable"]))))

    kv.append(("auth", E(p.line("auth:" + key, lambda a: "%s — %s"
                                % ("ok" if a["state"] == "ok" else a["state"], a["text"])))))
    kv.append(("CLI", E(p.line("auth:" + key, lambda a: (
        "not found — %s" % a["text"] if a["state"] == "cli-missing"
        else "%s%s" % (a["cli"], "" if a["on_path"]
                       else "  (installed, NOT on PATH — invoke by absolute path)"))))))

    if cfg["has_lane_lock"]:
        kv.append(("leg 1 · lock", E(p.line("lane-lock", lambda lk: "%s — %s"
                                            % ("FREE" if lk["free"] else "HELD",
                                               lk["why"] or ("%s; acquired: %s"
                                                             % (os.path.basename(lk["path"]),
                                                                "yes" if lk["acquired"]
                                                                else "no")))))))
    else:
        kv.append(("leg 1 · lock",
                   NULL("not applicable — no lane lock exists for this vendor. `GrokHarness` "
                        "is build-delta D-6 and stays gated behind U-8 judge-pilot "
                        "authorisation, so nothing takes a Grok lock today. Declared "
                        "unreachable, not green")))
    kv.append(("leg 2 · procs", E(p.line("proc-scan", lambda ps:
                                         "scanned %d process(es); argv[0]-anchored match on "
                                         "`%s`" % (len(ps), vendor)))))
    if cfg["runlogs"]:
        kv.append(("leg 3 · run-log", E(p.line("runlog:" + key, lambda rl: " · ".join(
            ("%s absent" % os.path.basename(r["path"])) if not r["present"]
            else "%s: %d rows, last `%s` %s (%s)"
            % (os.path.basename(r["path"]), r["rows"], r["marker"],
               "terminal" if r["terminal"] else "NON-TERMINAL",
               "backlog %d ENQUEUED" % r["enqueued"] if r["backlog_derivable"]
               else "backlog NOT derivable: %d-column pre-queue format carries no ENQUEUE "
                    "marker" % r["cols"])
            for r in rl)))))
    else:
        kv.append(("leg 3 · run-log",
                   NULL("none exists for this lane — a Grok run-log is build-delta D-8 and is "
                        "born with the queue. Backlog is UNMEASURED, which is not zero")))

    last, n_closes, n_units, pins = _lane_tape_activity(fr, rows, units, key)
    kv.append(("pin", (E(" · ".join(pins)) + " <span class='null'>(derived from this lane's "
                       "own rows, never asserted here)</span>") if pins
               else NULL("no row on this lane carries a pin — the pin of record lives in the "
                         "harness/lane-spec, not on the tape yet")))
    if last is None:
        kv.append(("last tape activity",
                   NULL("no rows on tape for lane `%s` (%d unit(s) folded to this lane)"
                        % (key, n_units))))
    else:
        bits = ["unit <b>%s</b>" % E(last.get("unit_id")),
                "rc %s" % (E(last["rc"]) if last.get("rc") is not None else "null"),
                ("%s in / %s out" % (fr.human_n(last.get("tokens_input")),
                                     fr.human_n(last.get("tokens_output")))
                 if last.get("tokens_input") is not None else "tokens null"),
                # v1.1: `cost_usd` is CLOSE-only + optional. Absent is stated, not zeroed.
                ("$%.5f" % last["cost_usd"]) if last.get("cost_usd") is not None
                else "cost_usd absent on this row",
                E(last["ts"])]
        kv.append(("last tape activity", " · ".join(bits)
                   + "<br><span class='null'>%d CLOSE row(s) across %d unit(s) on this lane"
                     "</span>" % (n_closes, n_units)))
    kv.append(("lane note", E(cfg.get("note"))))

    L.append("<div class='kv'>")
    for k, val in kv:
        L.append("<div class='k'>%s</div><div>%s</div>" % (E(k), val))
    L.append("</div></div></div>")
    return "".join(L)


def claude_card(fr, rows, units):
    """The Claude lanes, SUMMARISED per § 13.1 — they have no serial lock, no vendor CLI
    busy state, and (F-7) lifecycle rows only. Rendering them with the same five legs
    would dress a structural null as a measurement."""
    lanes = ("claude-agent", "claude-subagent")
    closes = [r for r in rows if r.get("event") == "CLOSE" and r.get("lane") in lanes]
    starts = [r for r in rows if r.get("event") in ("START", "ENQUEUE")
              and r.get("lane") in lanes]
    L = ["<div class='vcard'><h3>claude <span class='state s-unknown'>summarised</span></h3>"
         "<div class='rows'><div class='kv'>"]
    L.append("<div class='k'>state</div><div>%s</div>"
             % NULL("no serial lock and no vendor busy-CLI for this lane — liveness is not "
                    "derivable the way it is for codex/grok"))
    L.append("<div class='k'>auth</div><div>%s</div>"
             % NULL("Claude Code auth is session-held, not probe-readable from here"))
    L.append("<div class='k'>tape rows</div><div>%d lifecycle row(s) · %d CLOSE</div>"
             % (len(starts) + len(closes), len(closes)))
    L.append("<div class='k'>tokens</div><div>%s</div>"
             % NULL("F-7: interactive sessions surface no per-turn usage; token fields stay "
                    "null until hooks + SNAPSHOT brackets deepen. A null is a fact; an "
                    "estimate in a truth-of-record stream is a fabrication"))
    L.append("</div></div></div>")
    return "".join(L)


# ---------------------------------------------------------------- HEALTH
# Tier-1 severity thresholds, RE-EXPRESSED (star-lord evaluates them inline inside
# `flight_report.render()` — same convergence point as the rollup helpers above: when he
# exposes them, these two constants import instead).
#
# S7/D3: the board rendered `23 GB free of 494 GB (5%)` in plain white while Tier-1 rendered
# the identical reading 🔴 — and while the board's own AWAITING MATT column carried T20 saying
# RED. A health strip calmer than the queue printed beside it is an instrument nobody reads
# twice. The five `git ·` rows dropped Tier-1's 🟡 the same way.
DISK_RED_PCT_FREE = 5.0                 # Tier-1: `GREEN if d["pct_free"] > 5 else RED`
# Tier-1: `GREEN if (g["ahead"] == 0 and g["dirty"] == 0) else AMBER` — `behind` is reported
# but deliberately does not raise severity (a behind-remote checkout is not local risk).


def SEV(level, text):
    """A severity-marked health cell. Glyph AND colour on the loud states, so a Tier-1 🔴/🟡
    and a Tier-2 red/amber are the same claim. Green carries colour only, matching the cells
    already on this strip (`<span class='ok'>none</span>`) — the glyph is reserved for the
    states that want the eye."""
    if level == "red":
        return "<span class='fail'>🔴 %s</span>" % text
    if level == "amber":
        return "<span class='degraded'>🟡 %s</span>" % text
    return "<span class='ok'>%s</span>" % text


def section_health(p, fr, rows, units, now):
    L = ["<section><h2>⚙ HEALTH — read-only probes, run at render time</h2><div class='body'>"]
    L.append("<table><tr><th>probe</th><th>reading</th></tr>")

    def row(name, cell):
        L.append("<tr><td>%s</td><td>%s</td></tr>" % (E(name), cell))

    row("vendor auth", "see the LANES cards above — <code>codex login status</code> · "
                       "<code>grok models</code>, each vendor's own check of record, probed "
                       "once per render and rendered on its own card")
    env = p.get("env:ENABLE_PROMPT_CACHING_1H")
    if env is None:
        row("ENABLE_PROMPT_CACHING_1H", E(p.line("env:ENABLE_PROMPT_CACHING_1H", lambda _: "")))
    elif env["present"]:
        row("ENABLE_PROMPT_CACHING_1H",
            "<span class='ok'>SET</span> = <code>%s</code>" % E(env["value"]))
    else:
        row("ENABLE_PROMPT_CACHING_1H",
            "<span class='fail'>🔴 NOT SET</span> — the U-3 lever is off in this render's "
            "environment. (An env var is per-process: this reads the board process's own "
            "environment, which is the shell that launched it.)")
    for name in fr.SIBLING_REPOS:
        key = "git:" + name
        if p.status(key) == "not-run":
            continue
        g = p.get(key)
        if g is None:                       # probe FAILED — loud, and never coloured green
            row("git · " + name, E(p.line(key, lambda r: "")))
            continue
        row("git · " + name,
            SEV("green" if (g["ahead"] == 0 and g["dirty"] == 0) else "amber",
                E("%s · ahead %d · behind %d · dirty %d"
                  % (g["branch"], g["ahead"], g["behind"], g["dirty"]))))
    dk = p.get("disk")
    if dk is None:
        row("disk", E(p.line("disk", lambda r: "")))
    else:
        row("disk", SEV("green" if dk["pct_free"] > DISK_RED_PCT_FREE else "red",
                        E("%.0f GB free of %.0f GB (%.0f%%)"
                          % (dk["free_gb"], dk["total_gb"], dk["pct_free"]))))
    reqs = p.get("requests-dirs")
    if reqs is None:
        row("unswept requests/", E(p.line("requests-dirs", lambda _: "")))
    else:
        open_dirs = {k: v for k, v in reqs.items() if v}
        row("unswept requests/",
            (", ".join("%s %d" % (E(k), len(v)) for k, v in sorted(open_dirs.items()))
             if open_dirs else "<span class='ok'>none</span>"))
    snaps = latest_snapshots(rows)
    if snaps:
        for cur, r in sorted(snaps.items()):
            row("window · " + cur, "%s <span class='null'>(meter vocabulary preserved raw, "
                                   "snapshot %s)</span>" % (E(r.get("meter_raw")), E(r["ts"])))
    else:
        row("window meters", NULL("no SNAPSHOT row on the tape — window burn is not "
                                  "derivable yet"))
    # pin drift — the tripwire, with its DENOMINATOR. Green is earned by comparisons that
    # happened, never by comparisons that were impossible (S7/D1, BLOCKING at L-25).
    d = pin_drift(fr, units)
    echo_note = ("; %d unit(s) echo a model but pinned none — NOT COMPARABLE, excluded from "
                 "the denominator" % d["echo_only"]) if d["echo_only"] else ""
    if d["drift"]:
        row("pin drift", "<span class='fail'>🔴 %d of %d comparable unit(s)</span> where "
                         "<code>model_echo</code> ≠ <code>pin</code>%s: %s"
            % (len(d["drift"]), d["comparable"], E(echo_note),
               E("; ".join("%s %s≠%s" % (x["unit"], x["pin"], x["echo"])
                           for x in d["drift"][:5]))))
    elif d["comparable"]:
        row("pin drift", "<span class='ok'>none</span> — %d/%d unit(s) carry BOTH a "
                         "<code>pin</code> and a <code>model_echo</code>, and all match%s"
            % (d["comparable"], d["total"], E(echo_note)))
    elif d["echo_only"]:
        row("pin drift", NULL(
            "NO COMPARISON POSSIBLE — %d/%d unit(s) carry a `model_echo` but none of them "
            "carries a `pin`, so nothing can be compared. Determinate, not green "
            "(%d/%d model_echo · 0/%d comparable)"
            % (d["echo_only"], d["total"], d["echo_only"], d["total"], d["total"])))
    else:
        row("pin drift", NULL(
            "NO SIGNAL — `model_echo` is null on %d/%d unit(s), so the tripwire cannot fire "
            "on any lane currently captured. A determinate answer, not a clean bill of health"
            % (d["total"], d["total"])))
    L.append("</table>")
    L.append("<div class='note'>Everything on this strip is a LOCAL, pre-push fact — which "
             "is exactly what Glance can never see (§ 12.1). The rear-view half of this "
             "board lives on Glance; the windshield stays here.</div>")
    L.append("</div></section>")
    return "".join(L)


# ---------------------------------------------------------------- rollups + residue
def section_rollups(fr, rows, sealed):
    L = ["<section><h2>✓ SEALED — rollups + per-model scorecard (derived at render time, "
         "stored nowhere)</h2><div class='body'>"]
    groups = sealed_by_workstream(fr, rows, sealed)
    if not groups:
        L.append("<div class='empty'>no sealed units on the tape yet</div>")
    else:
        L.append("<table><tr><th>workstream</th><th>units</th><th>rc</th>"
                 "<th>judged verdicts</th><th>curation</th><th>tok-in</th><th>cache</th>"
                 "<th>tok-out</th><th>reported cost</th><th>currency</th>"
                 "<th>first-start→last-close</th></tr>")
        for g in groups:
            L.append("<tr><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
                     "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (E(g["ws"]), g["n"],
                        E("%d/%d rc=0" % (len([r for r in g["rcs"] if r == 0]), len(g["rcs"])))
                        if g["rcs"] else NULL("no rc on %d/%d units" % (g["n"], g["n"])),
                        E(" · ".join("%d %s" % (v, k) for k, v in
                                     sorted(g["verdicts"].items(), key=lambda kv: -kv[1])))
                        if g["verdicts"] else NULL("0/%d judged — no gatekeeper at this grain"
                                                   % g["n"]),
                        E("%d WARN across %d curation row(s)" % (g["warns"], g["curation_rows"]))
                        if g["curation_rows"] else NULL("no curation row"),
                        E("%s (%d/%d units)" % (fr.human_n(g["tin"]), g["n_tok"], g["n"]))
                        if g["n_tok"] else NULL("null on %d/%d units" % (g["n"], g["n"])),
                        E("%.1f%%" % (100.0 * g["tcache"] / g["tin"]))
                        if g["n_tok"] and g["tin"] else NULL("no denominator"),
                        E(fr.human_n(g["tout"])) if g["n_tok"] else NULL("null"),
                        E("$%.5f (%d/%d CLOSE rows carry cost_usd)"
                          % (g["usd"], g["n_usd"], g["n"])) if g["n_usd"]
                        else NULL("no cost_usd on this workstream's CLOSE rows"),
                        E("/".join(g["currencies"])) if g["currencies"] else NULL("none"),
                        E(fr.fmt_span(g["span"]))))
        L.append("</table>")
        L.append("<div class='note'><code>first-start→last-close</code> is a RUN DURATION, "
                 "not <code>enqueue→seal</code>: the founding corpus records no ENQUEUE "
                 "events, so enqueue→seal is not derivable for it.</div>")

    sc = scorecard(fr, sealed)
    L.append("<h3 style='font-size:12px;margin:14px 0 6px'>Per-model scorecard — one row per "
             "(provider, pin)</h3>")
    if not sc:
        L.append("<div class='empty'>no sealed units to score</div>")
    else:
        L.append("<table><tr><th>provider / pin</th><th>units</th><th>first-pass rc=0</th>"
                 "<th>tok-in</th><th>cache</th><th>tok-out</th><th>tok-in/artifact</th>"
                 "<th>reported cost</th><th>med wall</th></tr>")
        for g in sc:
            rcs = g["rcs"]
            L.append("<tr><td>%s / %s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td>"
                     "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (E(g["provider"]), E(g["pin"]), g["n"],
                        E("%.0f%% (%d/%d rc=0)"
                          % (100.0 * len([r for r in rcs if r == 0]) / len(rcs),
                             len([r for r in rcs if r == 0]), len(rcs))) if rcs
                        else NULL("no rc recorded"),
                        E(fr.human_n(g["tin"])) if g["have_tokens"]
                        else NULL("null, declared"),
                        E("%.1f%%" % (100.0 * g["tcache"] / g["tin"]))
                        if g["have_tokens"] and g["tin"] else NULL("no denominator"),
                        E(fr.human_n(g["tout"])) if g["have_tokens"] else NULL("null"),
                        E(fr.human_n(int(g["tin"] / g["artifacts"])))
                        if g["have_tokens"] and g["artifacts"] else NULL("no artifact rows"),
                        E("$%.5f (%d/%d)" % (g["usd"], g["n_usd"], g["n"])) if g["n_usd"]
                        else NULL("no cost_usd"),
                        E(fr.fmt_age(fr.median(g["durs"]))) if g["durs"]
                        else NULL("no START→CLOSE pair")))
        L.append("</table>")
        L.append("<div class='note'>WARN / fabrication-check columns are OMITTED rather than "
                 "zero-filled: a CURATION row binds to a <code>unit_id</code>, so a per-model "
                 "WARN rate is derivable only when the curated unit is itself a lane unit.</div>")
    L.append("</div></section>")
    return "".join(L)


def section_residue(fr, unbound, p, now):
    L = ["<section><h2>◻ UNBOUND + probe residue — the parts that make the lanes add up"
         "</h2><div class='body'>"]
    L.append("<div class='note'>A unit folds here when the tape carries a judgement or a note "
             "about it but no ENQUEUE/START/CLOSE of its own: never flown under the recorder, "
             "so not IN-FLIGHT, and never closed under it, so not SEALED. It is rendered "
             "rather than dropped — the lanes must partition the tape.</div>")
    if not unbound:
        L.append("<div class='empty'>none — every unit on the tape has a live lane</div>")
    else:
        L.append("<table><tr><th>unit</th><th>state</th><th>latest event</th><th>age</th></tr>")
        for u in unbound:
            age = (now - fr.parse_ts(u["latest"]["ts"])).total_seconds()
            L.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (E(u["latest"]["unit_id"]), E(u["state"]), E(u["latest"]["event"]),
                        E(fr.fmt_age(age))))
        L.append("</table>")
    if p.failures:
        L.append("<div class='note fail'><b>probe failures (%d)</b><br>%s</div>"
                 % (len(p.failures),
                    "<br>".join("%s — %s" % (E(k), E(v)) for k, v in p.failures.items())))
    else:
        L.append("<div class='note ok'>all %d probes ran</div>" % p.ran)
    L.append("</div></section>")
    return "".join(L)


# ---------------------------------------------------------------- server
def make_handler(args):
    from http.server import BaseHTTPRequestHandler

    class Handler(BaseHTTPRequestHandler):
        server_version = "fleet-board/" + BOARD_VERSION

        def _render(self):
            now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            try:
                return render_html(args.records_dir, args.repo_root, now,
                                   run_probes=not args.no_probes,
                                   lane_probes=not args.no_lane_probes)
            except Exception:                                       # noqa: BLE001
                return error_page("render raised", traceback.format_exc(), now)

        def do_GET(self):                                           # noqa: N802
            if self.path.split("?")[0] not in ("/", "/index.html"):
                self.send_error(404, "the board serves exactly one page")
                return
            body = self._render().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_HEAD(self):                                          # noqa: N802
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

        # THE LAW, at the transport layer: there is no write verb to reach. (The reason
        # string stays ASCII: an HTTP status line is latin-1, and a non-ASCII dash there
        # crashes the handler instead of refusing the request.)
        def _refuse(self):
            self.send_error(405, "Method Not Allowed",
                            "The fleet board is a VIEW. It has no write verbs: no endpoint "
                            "on this server mutates anything, so there is nothing for a "
                            "POST/PUT/PATCH/DELETE to reach.")

        do_POST = do_PUT = do_DELETE = do_PATCH = _refuse            # noqa: N815

        def log_message(self, fmt, *a):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % a))

    return Handler


def main(argv=None):
    ap = argparse.ArgumentParser(prog="board", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records-dir", default=FLIGHT_DIR)
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--render-to", default=None,
                    help="write ONE disposable HTML snapshot and exit (screenshot path)")
    ap.add_argument("--once", action="store_true", help="with --render-to: do not serve")
    ap.add_argument("--now", default=None, help="pin the clock (ISO-8601 UTC) for tests")
    ap.add_argument("--no-probes", action="store_true", help="tape-only render")
    ap.add_argument("--no-lane-probes", action="store_true",
                    help="skip the vendor-lane composite (no CLI auth calls)")
    args = ap.parse_args(argv)

    if args.render_to:
        import re as _re
        now = (datetime.datetime.strptime(args.now, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc) if args.now
            else datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
        html_text = render_html(args.records_dir, args.repo_root, now,
                                run_probes=not args.no_probes,
                                lane_probes=not args.no_lane_probes)
        with open(args.render_to, "w", encoding="utf-8") as fh:
            fh.write(html_text)
        sys.stdout.write("wrote %s (%d bytes)\n"
                         % (args.render_to, len(html_text.encode("utf-8"))))
        if _re.search(r"RENDER CHECK FAILED", html_text):
            sys.stderr.write("WARNING: the render's own partition audit failed — see page\n")
        if args.once:
            return 0

    from http.server import ThreadingHTTPServer
    httpd = ThreadingHTTPServer((args.host, args.port), make_handler(args))
    sys.stdout.write("FLEET BOARD (VIEW ONLY, zero write verbs) → http://%s:%d/\n"
                     "tape: %s · repo: %s\nCtrl-C to stop; the board owns nothing.\n"
                     % (args.host, args.port, args.records_dir, args.repo_root))
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stdout.write("\nstopped\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
