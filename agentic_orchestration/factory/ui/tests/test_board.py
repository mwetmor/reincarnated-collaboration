"""Smoke tests for the Tier-2 local fleet board (U1-BUILD/B-3, drax).

Run: python3 -m pytest agentic_orchestration/factory/ui/tests/test_board.py -q
(Deliberately OUTSIDE `factory/pytest.ini`'s `testpaths = tests`, so this file never
changes what star-lord's suite collects.)

What these pin, and why each one is load-bearing:
  * THE LAW at the transport layer — every write verb is refused before any handler runs.
  * THE LAW at the disk layer — a full render mutates NOTHING under `flight/`.
  * empty-tape tolerance — a fleet with no rows renders honest zeroes, never a crash.
  * partition — the render's own audit is clean, so no unit is silently dropped.
  * ONE derivation — the board's lane cards come from `flight_report`'s composite, not
    from a second implementation living here.
  * COLOUR HONESTY (B-3b, from galadriel's S7) — green is earned by comparisons that
    happened, never by comparisons that were impossible; the lane chip's colour is
    star-lord's exported predicate; the HEALTH strip carries Tier-1's severity.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys

import pytest

UI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTORY_DIR = os.path.dirname(UI_DIR)
AO_DIR = os.path.dirname(FACTORY_DIR)
REPO_ROOT = os.path.dirname(AO_DIR)
FLIGHT_DIR = os.path.join(AO_DIR, "flight")

if UI_DIR not in sys.path:
    sys.path.insert(0, UI_DIR)

import board  # noqa: E402

NOW = datetime.datetime(2026, 8, 25, 0, 0, 0, tzinfo=datetime.timezone.utc)


def _digest_dir(path):
    """Content digest of every file under a directory — the writes-nothing witness."""
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(files):
            if name.endswith(".pyc"):
                continue
            full = os.path.join(root, name)
            h.update(os.path.relpath(full, path).encode())
            with open(full, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


def test_renders_against_the_live_tape():
    html = board.render_html(FLIGHT_DIR, REPO_ROOT, NOW,
                             run_probes=False, lane_probes=False)
    assert "FLEET BOARD" in html
    assert "SHOP-ONLY" in html and "VIEW ONLY" in html
    assert "THE LAW (U-1)" in html
    assert "RENDER CHECK FAILED" not in html      # the partition audit is clean
    assert "cannot import flight/bin/flight_report" not in html


def test_writes_nothing_under_flight():
    """A full render — probes and all — leaves the recorder's tree byte-identical."""
    before = _digest_dir(FLIGHT_DIR)
    board.render_html(FLIGHT_DIR, REPO_ROOT, NOW, run_probes=True, lane_probes=False)
    assert _digest_dir(FLIGHT_DIR) == before


def test_empty_tape_renders(tmp_path):
    """No tape file at all: honest zeroes, a declared coverage boundary, no crash."""
    html = board.render_html(str(tmp_path), REPO_ROOT, NOW,
                             run_probes=False, lane_probes=False)
    assert "(0 rows on disk; 0 after corrections)" in html
    assert "tape begins (no rows yet)" in html
    assert "IN-FLIGHT" in html and "no unit on the tape has a START" in html
    assert "no sealed units on the tape yet" in html


def test_empty_tape_file_renders(tmp_path):
    """A tape FILE that exists and is empty is a different disk state from no file."""
    (tmp_path / "records-2026-08.jsonl").write_text("", encoding="utf-8")
    html = board.render_html(str(tmp_path), REPO_ROOT, NOW,
                             run_probes=False, lane_probes=False)
    assert "records-2026-08.jsonl" in html
    assert "RENDER CHECK FAILED" not in html


def test_lane_derivation_is_imported_not_reimplemented():
    """The LANES card must render star-lord's composite. If these names move, the board
    should FAIL here rather than quietly grow a second lane derivation."""
    fr = board.load_flight_report()
    for name in ("LANE_CARDS", "lane_answer", "probe_lane_lock", "probe_process_table",
                 "probe_vendor_auth", "probe_runlogs", "PROBE_MODE", "Q62_CAVEAT",
                 # B-3b: the chip COLOUR is his too, exported by B-1c so both tiers
                 # colour one predicate one way (Amendment H).
                 "state_marker", "GREEN", "AMBER", "RED"):
        assert hasattr(fr, name), "flight_report lost %s — the board's one derivation" % name
    assert {c["vendor"] for c in fr.LANE_CARDS} >= {"codex", "grok"}, "AM-1 grok parity"


def test_grok_lane_renders_even_with_no_grok_rows(tmp_path):
    """AM-1 parity: the grok card appears wherever the codex card does, and says
    'no rows on tape' honestly rather than vanishing."""
    html = board.render_html(str(tmp_path), REPO_ROOT, NOW,
                             run_probes=True, lane_probes=True)
    assert "grok" in html and "codex" in html
    assert "grok-serial" in html
    assert board.load_flight_report().PROBE_MODE in html


def test_no_write_verbs_exist_on_the_handler():
    class Args:
        records_dir = FLIGHT_DIR
        repo_root = REPO_ROOT
        no_probes = True
        no_lane_probes = True

    handler = board.make_handler(Args())
    for verb in ("do_POST", "do_PUT", "do_DELETE", "do_PATCH"):
        assert getattr(handler, verb) is handler._refuse, "%s is not refused" % verb
    assert not hasattr(handler, "do_OPTIONS")


def test_error_page_is_red_and_says_why():
    page = board.error_page("headline", "detail", NOW)
    assert "FLEET BOARD — RED" in page and "headline" in page
    assert "second derivation is a second truth" in page


# ------------------------------------------------------------------ B-3b colour honesty
def _tape(tmp_path, *rows):
    """One disposable tape file. Rows are written exactly as the recorder writes them."""
    path = tmp_path / "records-2026-08.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return str(tmp_path)


def _close(unit_id, **extra):
    row = dict(v=1, row_id=unit_id + "-close", ts="2026-08-24T12:00:00Z", event="CLOSE",
               unit_id=unit_id, unit_kind="job", workstream="T", operator="drax",
               provider="xai", lane="grok-serial", rc=0)
    row.update(extra)
    return row


def _pin_drift_cell(html):
    m = re.search(r"<tr><td>pin drift</td><td>(.*?)</td></tr>", html, re.S)
    assert m, "the HEALTH strip lost its `pin drift` row entirely"
    return m.group(1)


def test_pin_drift_zero_comparable_population_renders_null_not_green(tmp_path):
    """THE B-3b REGRESSION (S7/D1, ruled FALSE-GREEN and BLOCKING at L-25).

    A tape where one unit echoes a model and NO unit carries both keys supports ZERO
    comparisons. The old cell rendered `<span class='ok'>none</span>` — green — off a
    comparable population of zero. The absence of a disagreement is not the presence of an
    agreement, and this board renders the second only when the first was actually tested.
    """
    d = _tape(tmp_path, _close("u/echo-no-pin", model_echo="grok-4.6-build"))
    cell = _pin_drift_cell(board.render_html(d, REPO_ROOT, NOW,
                                             run_probes=False, lane_probes=False))
    assert 'class="null"' in cell, "a zero-comparable population must render as a NULL"
    assert "class='ok'" not in cell and "class=\"ok\"" not in cell, "FALSE-GREEN is back"
    assert "NO COMPARISON POSSIBLE" in cell            # Tier-1's words, on Tier-1's finding
    assert "Determinate, not green" in cell
    assert "0/1 comparable" in cell                    # the denominator galadriel asked for


def test_pin_drift_green_needs_a_comparison_that_actually_happened(tmp_path):
    """The other side of the same rule: green is reachable, and only this way."""
    d = _tape(tmp_path, _close("u/pinned", pin="grok-4.6-build", model_echo="grok-4.6-build"))
    cell = _pin_drift_cell(board.render_html(d, REPO_ROOT, NOW,
                                             run_probes=False, lane_probes=False))
    assert "class='ok'>none</span>" in cell
    assert "1/1 unit(s) carry BOTH" in cell


def test_pin_drift_mismatch_is_red_over_its_comparable_denominator(tmp_path):
    d = _tape(tmp_path,
              _close("u/drifted", pin="grok-4.6-build", model_echo="grok-4.7-build"),
              _close("u/echo-only", model_echo="grok-4.6-build"))
    cell = _pin_drift_cell(board.render_html(d, REPO_ROOT, NOW,
                                             run_probes=False, lane_probes=False))
    assert "class='fail'" in cell and "1 of 1 comparable unit(s)" in cell
    assert "NOT COMPARABLE, excluded from the denominator" in cell   # the echo-only unit


def test_pin_drift_no_signal_at_all_is_also_not_green(tmp_path):
    d = _tape(tmp_path, _close("u/silent"))
    cell = _pin_drift_cell(board.render_html(d, REPO_ROOT, NOW,
                                             run_probes=False, lane_probes=False))
    assert 'class="null"' in cell and "NO SIGNAL" in cell
    assert "class='ok'" not in cell


def test_pin_drift_agrees_with_tier1_on_the_live_tape():
    """ONE DERIVATION, two windows: the board's populations and Tier-1's must land in the
    same branch on the same tape. This is the check that catches a silent re-divergence of
    grain (per-unit vs per-row) or of comparison (`pin` vs `pin.split("@")[0]`)."""
    fr = board.load_flight_report()
    tier1 = fr.render(FLIGHT_DIR, REPO_ROOT, NOW, run_probes=False)
    cell = _pin_drift_cell(board.render_html(FLIGHT_DIR, REPO_ROOT, NOW,
                                             run_probes=False, lane_probes=False))
    for phrase in ("NO COMPARISON POSSIBLE", "NO SIGNAL"):
        assert (phrase in tier1) == (phrase in cell), \
            "Tier-1 and the board disagree on the pin-drift branch (%s)" % phrase
    if "NO COMPARISON POSSIBLE" in tier1 or "NO SIGNAL" in tier1:
        assert "class='ok'" not in cell, "Tier-1 refuses green here and so must the board"


def test_lane_chip_colour_is_star_lords_exported_marker():
    """S7/D2 + Amendment H. The board contributes NO colour rule of its own: green is
    `state_marker` GREEN, amber is AMBER, red is RED. Reduced leg coverage rides in the
    chip text so the reduction is legible at a glance, not only in the card body."""
    fr = board.load_flight_report()
    full = dict(state="open", reasons=[], advisories=[], unreachable=[], na=[])
    partial = dict(full, na=["leg 1 — none", "leg 3 — none"])
    queued = dict(full, state="queue-pending")
    dead = dict(full, state="auth-expired")

    assert "s-open" in board.lane_chip(fr, full)
    # grok: fire-safe but 1-of-3 legs — amber, and it SAYS one of three.
    assert "s-warn" in board.lane_chip(fr, partial)
    assert "s-open" not in board.lane_chip(fr, partial)
    assert "1 of 3 legs" in board.lane_chip(fr, partial)
    # Amendment H: backlog is not occupancy. `queue-pending` colours WITH open.
    assert "s-open" in board.lane_chip(fr, queued)
    assert "s-busy" in board.lane_chip(fr, dead)
    # and the mapping is HIS, not a local table
    assert not hasattr(board, "_STATE_CLASS"), "the local state→colour table is back"


def test_health_severity_matches_tier1_thresholds():
    """S7/D3: disk and git carry Tier-1's colour, on Tier-1's thresholds."""
    fr = board.load_flight_report()
    html = board.render_html(FLIGHT_DIR, REPO_ROOT, NOW, run_probes=True, lane_probes=False)
    m = re.search(r"<tr><td>disk</td><td>(.*?)</td></tr>", html, re.S)
    assert m, "the HEALTH strip lost its `disk` row"
    disk = fr.probe_disk(REPO_ROOT)()
    if disk["pct_free"] > board.DISK_RED_PCT_FREE:
        assert "class='ok'" in m.group(1)
    else:
        assert "class='fail'" in m.group(1) and "🔴" in m.group(1), \
            "Tier-1 renders this reading RED; a plain-white Tier-2 cell is the D3 defect"
    for name in fr.SIBLING_REPOS:
        g = fr.probe_git(os.path.join(os.path.dirname(REPO_ROOT), name))()
        cell = re.search(r"<tr><td>git · %s</td><td>(.*?)</td></tr>" % re.escape(name),
                         html, re.S)
        if cell is None:
            continue
        want = "class='ok'" if (g["ahead"] == 0 and g["dirty"] == 0) else "class='degraded'"
        assert want in cell.group(1), "git · %s severity disagrees with Tier-1" % name


@pytest.mark.parametrize("field", ["cost_usd", "grok-sub", "grok-serial"])
def test_v11_fields_are_read_defensively(field):
    """v1.1 tolerance: none of the amendment's additions may be REQUIRED by the render."""
    src = open(os.path.join(UI_DIR, "board.py"), encoding="utf-8").read()
    assert field in src
    # `cost_usd` must never be read with [] on a row that may not carry it.
    assert 'r["cost_usd"]' not in src
