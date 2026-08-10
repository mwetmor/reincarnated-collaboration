"""Receipts — Spec A § 6. One data path: gates write here, every surface reads here.

The tests that matter most are the two that keep a later dashboard honest:
`usage_totals` must not fold reasoning into the billable sum, and
`gate_verdict_tuples` must be the stable comparison key the determinism
assertion is built on.
"""

import sqlite3

from factory.envelope import EnvelopeBase
from factory.gates.base import GateReport
from factory.receipts import SCHEMA_VERSION, Receipts
from factory.usage import DOLLARS_HARNESS_IMPUTED, UsageBreakdown

EXPECTED_TABLES = {
    "schema_meta", "sessions", "phases", "events", "envelopes",
    "gate_results", "processes", "agent_sessions",
}


def _db(tmp_path) -> Receipts:
    return Receipts(tmp_path / "receipts.db")


# ---------------------------------------------------------------------------
# schema
# ---------------------------------------------------------------------------
def test_the_seven_tables_plus_schema_meta_exist(tmp_path):
    r = _db(tmp_path)
    names = {
        row["name"]
        for row in r.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert EXPECTED_TABLES <= names
    r.close()


def test_the_schema_version_is_stamped_so_a_consumer_can_refuse_it(tmp_path):
    r = _db(tmp_path)
    row = r.conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()
    assert int(row["value"]) == SCHEMA_VERSION
    r.close()


def test_wal_mode_is_on(tmp_path):
    r = _db(tmp_path)
    mode = r.conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode.lower() == "wal", "concurrent readers depend on WAL"
    r.close()


def test_reopening_an_existing_db_does_not_destroy_it(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    r.close()
    again = _db(tmp_path)
    assert again.session("run1") is not None
    again.close()


# ---------------------------------------------------------------------------
# the write path
# ---------------------------------------------------------------------------
def test_a_full_run_round_trips(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path, workflow_path="/w.yaml",
                    workflow_sha256="deadbeef")
    assert r.session("run1")["status"] == "RUNNING"

    pid = r.start_phase("run1", 0, "digest", None, None)
    assert r.phases("run1")[0]["status"] == "FAILED", "a phase is on record as FAILED first"

    env = EnvelopeBase(status="PASS", summary="pinned", artifacts=["b.tar"],
                       notes_for_next_agent="next")
    r.record_envelope("run1", pid, env, attempt=1, raw_path="/tmp/e.json")
    r.record_gate("run1", pid, GateReport.passed("sha256_matches", "digest matches"))
    r.finish_phase(pid, "PASS", 1, UsageBreakdown.absent("mechanical phase"))
    r.finish_session("run1", "PASS")

    assert r.session("run1")["status"] == "PASS"
    assert r.session("run1")["workflow_sha256"] == "deadbeef"
    assert r.envelope_for_phase(pid)["summary"] == "pinned"
    assert r.gates_for_phase(pid)[0]["status"] == "PASS"
    r.close()


def test_a_parse_failure_is_recorded_as_an_envelope_row_with_no_envelope(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    pid = r.start_phase("run1", 0, "p", "rocket", "claude_code")
    r.record_envelope("run1", pid, None, 1, parse_error="no fenced JSON block found")
    row = r.envelope_for_phase(pid)
    assert row["status"] is None
    assert "no fenced JSON" in row["parse_error"]
    r.close()


def test_gate_evidence_survives_non_serialisable_values(tmp_path):
    """Evidence is written with default=str so a Path never loses a gate's receipt."""
    from pathlib import Path

    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    pid = r.start_phase("run1", 0, "p", None, None)
    r.record_gate("run1", pid, GateReport.failed("g", "boom", where=Path("/x/y")))
    assert "/x/y" in r.gates_for_phase(pid)[0]["evidence_json"]
    r.close()


def test_a_phase_row_cannot_reference_a_session_that_does_not_exist(tmp_path):
    r = _db(tmp_path)
    try:
        r.start_phase("no-such-run", 0, "p", None, None)
    except sqlite3.IntegrityError:
        pass
    else:  # pragma: no cover - only reached if FK enforcement regresses
        raise AssertionError("foreign keys are not being enforced")
    finally:
        r.close()


def test_processes_and_agent_sessions_record_what_actually_ran(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    pid = r.start_phase("run1", 0, "p", "star-lord", "claude_code")
    r.record_process("run1", pid, ["python3", "-m", "pytest"], "/repo", 0, "2026-08-10T00:00:00Z")
    r.record_agent_session("run1", pid, "star-lord", "claude_code", 1, "sess-abc",
                           "claude-fable-5", "/p.txt", "/raw.jsonl", "2026-08-10T00:00:00Z")
    proc = r.conn.execute("SELECT * FROM processes").fetchone()
    assert "pytest" in proc["argv_json"] and proc["exit_code"] == 0
    sess = r.conn.execute("SELECT * FROM agent_sessions").fetchone()
    assert sess["harness_session_id"] == "sess-abc" and sess["model"] == "claude-fable-5"
    r.close()


# ---------------------------------------------------------------------------
# the read path — where a dashboard would get its numbers
# ---------------------------------------------------------------------------
def test_usage_totals_exclude_reasoning_from_the_billable_sum(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    for idx in range(2):
        pid = r.start_phase("run1", idx, f"p{idx}", "rocket", "claude_code")
        r.finish_phase(
            pid, "PASS", 1,
            UsageBreakdown(input_tokens=10, output_tokens=20, cache_read_tokens=30,
                           cache_write_tokens=40, reasoning_tokens=15, dollars=0.5,
                           dollars_source=DOLLARS_HARNESS_IMPUTED),
        )
    totals = r.usage_totals("run1")
    assert totals["billable_token_total"] == 200
    assert totals["reasoning_tokens"] == 30, "reasoning is still reported, just not summed in"
    assert totals["dollars"] == 1.0
    assert totals["dollars_sources"] == [DOLLARS_HARNESS_IMPUTED], (
        "a summed dollar figure carries the provenance of what was summed (D-4)"
    )
    r.close()


def test_dollar_provenance_travels_with_the_total_from_every_lane(tmp_path):
    """Two lanes, two pricing stories, one sum. The total must not be able to
    describe itself with a single lane's caveat."""
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    for idx, source in enumerate([DOLLARS_HARNESS_IMPUTED, "metered_api_billed"]):
        pid = r.start_phase("run1", idx, f"p{idx}", "rocket", "claude_code")
        r.finish_phase(
            pid, "PASS", 1,
            UsageBreakdown(input_tokens=1, output_tokens=1, cache_read_tokens=0,
                           cache_write_tokens=0, dollars=0.25, dollars_source=source),
        )
    totals = r.usage_totals("run1")
    assert totals["dollars"] == 0.5
    assert set(totals["dollars_sources"]) == {DOLLARS_HARNESS_IMPUTED, "metered_api_billed"}
    r.close()


def test_a_priced_phase_with_no_recorded_source_leaves_the_total_unlabelled(tmp_path):
    """The falsification partner: provenance must be ABSENT when nothing recorded it,
    so the renderer says so rather than inheriting a default caveat."""
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    pid = r.start_phase("run1", 0, "p", "rocket", "claude_code")
    r.finish_phase(
        pid, "PASS", 1,
        UsageBreakdown(input_tokens=1, output_tokens=1, cache_read_tokens=0,
                       cache_write_tokens=0, dollars=9.99, dollars_source=None),
    )
    totals = r.usage_totals("run1")
    assert totals["dollars"] == 9.99
    assert [s for s in totals["dollars_sources"] if s] == []
    r.close()


def test_usage_totals_of_a_mechanical_run_are_null_not_zero(tmp_path):
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    pid = r.start_phase("run1", 0, "p", None, None)
    r.finish_phase(pid, "PASS", 1, UsageBreakdown.absent("mechanical phase — no model invoked"))
    totals = r.usage_totals("run1")
    assert totals["billable_token_total"] is None
    assert totals["input_tokens"] is None
    r.close()


def test_gate_verdict_tuples_are_the_determinism_key(tmp_path):
    """Ordered (phase, gate, status) — stable across runs, and the thing compared."""
    r = _db(tmp_path)
    r.start_session("run1", "wf", tmp_path, tmp_path)
    for idx, pname in enumerate(["second_by_name", "aaa_first_by_name"]):
        pid = r.start_phase("run1", idx, pname, None, None)
        r.record_gate("run1", pid, GateReport.passed("artifacts_exist", "ok"))
        r.record_gate("run1", pid, GateReport.failed("files_non_empty", "zero bytes"))
    tuples = r.gate_verdict_tuples("run1")
    assert tuples == [
        ("second_by_name", "artifacts_exist", "PASS"),
        ("second_by_name", "files_non_empty", "FAIL"),
        ("aaa_first_by_name", "artifacts_exist", "PASS"),
        ("aaa_first_by_name", "files_non_empty", "FAIL"),
    ], "ordering must follow phase index then gate order, never alphabetical"
    r.close()


def test_two_runs_with_the_same_verdicts_compare_equal(tmp_path):
    r = _db(tmp_path)
    for run in ("run1", "run2"):
        r.start_session(run, "wf", tmp_path, tmp_path)
        pid = r.start_phase(run, 0, "p", None, None)
        r.record_gate(run, pid, GateReport.passed("artifacts_exist", "ok"))
    assert r.gate_verdict_tuples("run1") == r.gate_verdict_tuples("run2")
    r.close()


def test_sessions_lists_most_recent_first(tmp_path):
    r = _db(tmp_path)
    r.start_session("older", "wf", tmp_path, tmp_path)
    r.conn.execute("UPDATE sessions SET started_at='2020-01-01T00:00:00+00:00'")
    r.start_session("newer", "wf", tmp_path, tmp_path)
    assert [s["run_id"] for s in r.sessions()][0] == "newer"
    r.close()
