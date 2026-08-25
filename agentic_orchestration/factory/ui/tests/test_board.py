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
"""

from __future__ import annotations

import datetime
import hashlib
import os
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
                 "probe_vendor_auth", "probe_runlogs", "PROBE_MODE", "Q62_CAVEAT"):
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


@pytest.mark.parametrize("field", ["cost_usd", "grok-sub", "grok-serial"])
def test_v11_fields_are_read_defensively(field):
    """v1.1 tolerance: none of the amendment's additions may be REQUIRED by the render."""
    src = open(os.path.join(UI_DIR, "board.py"), encoding="utf-8").read()
    assert field in src
    # `cost_usd` must never be read with [] on a row that may not carry it.
    assert 'r["cost_usd"]' not in src
