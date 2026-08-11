"""Gate-2 H6 — the limits of the measurement, recorded WITH the measurement.

Every other row in this suite asks whether the wall caught something. These ask a
different question: when the wall reports that it caught nothing, what exactly has
been established? Two facts bound that answer, and neither of them is visible from
inside a phase.

**The ground the wall stands on.** H1's root cause was `~/.claude/settings.json`
setting `permissions.defaultMode` to `bypassPermissions` on this host — outside the
tree, outside the workflow, and outside anything the factory sets. J1 then measured
that `--allowedTools` does not restrict in headless `default` mode, so the argv is
not evidence of the grant either. A receipt that records the fence and omits the
ground has recorded the less important half.

**The trees the wall looked at.** `fingerprint` measures `wf.repos`. A phase with
unrestricted `Bash` reaches the whole filesystem. "0 breaches" is therefore a claim
about a bounded region, and the boundary has to be printed next to it.

The failure shape these rows exist to refuse is the one this whole review series
keeps finding: not a wrong answer, but a *narrower* answer wearing the wide one's
clothes. And the specific temptation here has a name — filling an unstated
`defaultMode` with Claude Code's own fallback, `default`. That would be correct on
every host that has not changed it and unfalsifiable on the ones that have, which is
`usage.py`'s zero-filled-token defect moved from cost to containment.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from factory import host
from factory.receipts import SCHEMA_VERSION, Receipts
from factory.report import render_run_report
from factory.runner import Runner
from factory.workflow import load_workflow


# ---------------------------------------------------------------------------
# reading one layer, and saying so
# ---------------------------------------------------------------------------
def _settings(root: Path, payload: object) -> Path:
    path = root / "settings.json"
    path.write_text(json.dumps(payload) if not isinstance(payload, str) else payload,
                    encoding="utf-8")
    return path


def test_H6_a_STATED_host_default_is_read_and_its_source_named(tmp_path):
    path = _settings(tmp_path, {"permissions": {"defaultMode": "bypassPermissions"}})
    result = host.read_host_permission_mode(path)
    assert result.mode == "bypassPermissions"
    assert str(path) in result.source, "a mode with no named source cannot be audited"
    assert "NOT resolved here" in result.source, (
        "one layer reported as though it were the effective mode is the defect this "
        "records, not the one it fixes"
    )


def test_H6_an_UNSTATED_host_default_is_NULL_not_the_fallback(tmp_path):
    """The row that refuses the zero-fill.

    Claude Code's own fallback is `default`. Writing it here would produce a receipt
    that is right on this host and unfalsifiable everywhere — the shape `usage.py`
    refuses for tokens, arriving in containment evidence. Absent is absent.
    """
    path = _settings(tmp_path, {"permissions": {"allow": ["Read"]}})
    result = host.read_host_permission_mode(path)
    assert result.mode is None
    assert "default" not in (result.mode or ""), "an unstated mode must not be invented"
    assert "UNSTATED" in result.source
    assert str(path) in result.source, (
        "'we looked and it was silent' must be distinguishable from 'we never looked'"
    )


def test_H6_an_ABSENT_settings_file_is_UNKNOWN_not_restrictive(tmp_path):
    result = host.read_host_permission_mode(tmp_path / "nope.json")
    assert result.mode is None
    assert "UNREAD" in result.source
    assert "not permissive and not restrictive" in result.source


def test_H6_an_UNPARSEABLE_settings_file_does_not_abort_the_run(tmp_path):
    """A malformed host file is an observation about the host, not a run-stopping
    error. It must still be distinguishable from every other None."""
    path = _settings(tmp_path, "{ not json at all")
    result = host.read_host_permission_mode(path)
    assert result.mode is None
    assert "UNPARSEABLE" in result.source


def test_H6_a_NON_STRING_mode_is_refused_rather_than_stringified(tmp_path):
    """`str(True)` is `'True'`, which would be recorded as a mode nobody set."""
    path = _settings(tmp_path, {"permissions": {"defaultMode": True}})
    assert host.read_host_permission_mode(path).mode is None


# ---------------------------------------------------------------------------
# the ROUTE — the production default, not just the injectable one
# ---------------------------------------------------------------------------
def test_H6_the_PRODUCTION_default_path_resolves_through_the_users_home(tmp_path, monkeypatch):
    """The ROUTE axis, which this review series keeps landing on.

    Every row above passes an explicit path, so all five would stay green if the
    no-argument default pointed somewhere that does not exist. This one moves
    `Path.home()` and watches the real default follow — which is only possible
    because `default_settings_path()` resolves at CALL time rather than at import.
    """
    fake_home = tmp_path / "home"
    (fake_home / ".claude").mkdir(parents=True)
    (fake_home / ".claude" / "settings.json").write_text(
        json.dumps({"permissions": {"defaultMode": "acceptEdits"}}), encoding="utf-8"
    )
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    assert host.default_settings_path() == fake_home / ".claude" / "settings.json"
    assert host.read_host_permission_mode().mode == "acceptEdits"


# ---------------------------------------------------------------------------
# the measurement limit
# ---------------------------------------------------------------------------
def test_H6_the_limit_sentence_names_the_trees_and_refuses_the_wide_reading():
    text = host.describe_measurement_limit([Path("/x/engine"), Path("/x/godot")])
    assert "/x/engine" in text and "/x/godot" in text
    assert "not 'no unauthorised writes'" in text, (
        "the sentence exists to stop 'no breaches' being read as 'no writes'"
    )


def test_H6_measuring_NO_tree_says_nothing_was_looked_at():
    """The falsification partner. A limit sentence that reads the same whether two
    trees or zero trees were fingerprinted is decoration."""
    text = host.describe_measurement_limit([])
    assert "NO tree" in text
    assert "nothing was looked at" in text


# ---------------------------------------------------------------------------
# the WIRING — a run puts both on the receipt
# ---------------------------------------------------------------------------
def _run_a_mechanical_workflow(tmp_path, repo: Path) -> Runner:
    doc = {
        "name": "h6",
        "root": str(repo),
        "repos": [str(repo)],
        # A mechanical cell whose command touches nothing. The run has to be REAL —
        # the wiring under test is `Runner.run()`'s call to `start_session` — and it
        # has to be free, so the cheapest true-returning command is the whole phase.
        "phases": [{
            "name": "noop",
            "gates": [{"gate": "command_succeeds", "args": {"command": "true"}}],
        }],
    }
    path = tmp_path / "wf.json"
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    runner = Runner(load_workflow(path), factory_dir=tmp_path / "fh", verbose=False)
    runner.run()
    return runner


def test_H6_a_RUN_records_the_host_default_it_ran_under(tmp_path, git_repo, monkeypatch):
    """The wiring row. J5's first mutation pass found the column-writing correct and
    the call site absent; nothing certifies a column until something certifies that
    a run fills it."""
    fake_home = tmp_path / "home"
    (fake_home / ".claude").mkdir(parents=True)
    (fake_home / ".claude" / "settings.json").write_text(
        json.dumps({"permissions": {"defaultMode": "bypassPermissions"}}), encoding="utf-8"
    )
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    runner = _run_a_mechanical_workflow(tmp_path, git_repo)
    try:
        row = runner.receipts.session(runner.run_id)
        assert row["host_permission_mode"] == "bypassPermissions"
        assert row["host_permission_source"], "a mode with no provenance is unreadable"
    finally:
        runner.close()


def test_H6_a_RUN_records_the_trees_it_actually_fingerprinted(tmp_path, git_repo):
    runner = _run_a_mechanical_workflow(tmp_path, git_repo)
    try:
        row = runner.receipts.session(runner.run_id)
        assert json.loads(row["measured_trees"]) == [str(git_repo)]
        assert str(git_repo) in row["measurement_limit"]
        assert "not 'no unauthorised writes'" in row["measurement_limit"]
    finally:
        runner.close()


# ---------------------------------------------------------------------------
# the report — on the GREEN path, which is the only path that matters here
# ---------------------------------------------------------------------------
def test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches(tmp_path, git_repo, monkeypatch):
    """The whole point of H6, and the one assertion that cannot be satisfied by
    putting the caveat next to the breach list.

    A green run is where the over-claim happens: "0 breaches" invites "nothing was
    written". A caveat that only prints when something went wrong is a caveat no
    reader of a green report ever sees.
    """
    fake_home = tmp_path / "home"
    (fake_home / ".claude").mkdir(parents=True)
    (fake_home / ".claude" / "settings.json").write_text(
        json.dumps({"permissions": {"defaultMode": "bypassPermissions"}}), encoding="utf-8"
    )
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    runner = _run_a_mechanical_workflow(tmp_path, git_repo)
    try:
        breaches = [
            e for e in runner.receipts.events(runner.run_id)
            if e["kind"] == "permissions_breach"
        ]
        assert not breaches, "this row is about the GREEN path; it must stay green"
        text = render_run_report(runner.receipts, runner.run_id)
    finally:
        runner.close()

    assert "Permissions breaches" not in text, "premise: no breach section to hide behind"
    assert "bypassPermissions" in text
    assert str(git_repo) in text
    assert "not 'no unauthorised writes'" in text


def test_H6_an_UNRECORDED_measurement_reads_as_unrecorded_not_as_clean(tmp_path):
    """A pre-v3 session, migrated forward, carries NULL in all four columns.

    `COALESCE(host_permission_mode, 'default')` in a consumer would convert "we did
    not measure" into "the host was ordinary". The renderer must not do the same
    thing in prose.
    """
    r = Receipts(tmp_path / "receipts.db")
    r.start_session("old", "wf", tmp_path, tmp_path)      # v1/v2-shaped call site
    r.finish_session("old", "PASS")
    try:
        text = render_run_report(r, "old")
    finally:
        r.close()

    assert "UNRECORDED" in text
    assert "not evidence the host was restricted" in text
    assert "bypassPermissions" not in text and "`default`" not in text


# ---------------------------------------------------------------------------
# schema v3
# ---------------------------------------------------------------------------
def _v2_database(path: Path) -> None:
    """A receipts DB in the v2 shape: `sessions` without the four H6 columns.

    Hand-built rather than produced by dropping columns from the current schema —
    a fixture assembled by mutating today's code cannot outlive a change to today's
    code, and this one exists to represent a DB written months ago.
    """
    conn = sqlite3.connect(str(path))
    conn.executescript(
        "CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT);"
        "INSERT INTO schema_meta VALUES('schema_version','2');"
        "CREATE TABLE sessions (run_id TEXT PRIMARY KEY, workflow TEXT NOT NULL,"
        " workflow_path TEXT, workflow_sha256 TEXT, root TEXT NOT NULL,"
        " session_dir TEXT NOT NULL, status TEXT NOT NULL, started_at TEXT NOT NULL,"
        " ended_at TEXT, abort_reason TEXT);"
        "INSERT INTO sessions(run_id, workflow, root, session_dir, status, started_at)"
        " VALUES('before','wf','/tmp/x','/tmp/x/s','PASS','2026-01-01T00:00:00Z');"
    )
    conn.commit()
    conn.close()



def test_H6_a_v2_database_is_MIGRATED_to_v3_and_its_rows_survive(tmp_path):
    """Additive, per MIGRATION.md's standing rule: `ADD COLUMN` cannot destroy a row.

    The pre-existing row must come back with NULLs — never backfilled. The host
    default for a run that predates this measurement was never measured, and must
    read as unmeasured forever.
    """
    db = tmp_path / "receipts.db"
    _v2_database(db)

    again = Receipts(db)
    try:
        cols = {c[1] for c in again.conn.execute("PRAGMA table_info(sessions)")}
        assert {"host_permission_mode", "host_permission_source",
                "measured_trees", "measurement_limit"} <= cols
        stamp = again.conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        assert int(stamp[0]) == SCHEMA_VERSION == 3
        row = again.session("before")
        assert row is not None, "a migration that loses a row is not a migration"
        assert row["host_permission_mode"] is None
        assert row["measurement_limit"] is None
    finally:
        again.close()
