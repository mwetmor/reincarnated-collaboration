"""Receipts — SQLite in WAL mode. The run ledger's mechanical shadow.

Spec A § 6. Seven tables: sessions / phases / events / envelopes / gate_results /
processes / agent_sessions. One data path: the gates WRITE here and every surface
(status, report, future dashboard) READS here. A view is never truth.

Schema custody: star-lord (strategy § 8). Schema version is stamped in
`schema_meta` so a Tier-2 consumer can refuse an unknown version rather than
guess at it.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .usage import UsageBreakdown

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    run_id        TEXT PRIMARY KEY,
    workflow      TEXT NOT NULL,
    workflow_path TEXT,
    workflow_sha256 TEXT,
    root          TEXT NOT NULL,
    session_dir   TEXT NOT NULL,
    status        TEXT NOT NULL,          -- RUNNING | PASS | FAIL | ABORTED
    started_at    TEXT NOT NULL,
    ended_at      TEXT,
    abort_reason  TEXT
);

CREATE TABLE IF NOT EXISTS phases (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        TEXT NOT NULL REFERENCES sessions(run_id),
    idx           INTEGER NOT NULL,
    name          TEXT NOT NULL,
    agent         TEXT,                   -- NULL = mechanical phase (no model invoked)
    harness       TEXT,
    status        TEXT NOT NULL,          -- FAILED until a finish() collapses it
    attempts      INTEGER NOT NULL DEFAULT 0,
    started_at    TEXT NOT NULL,
    ended_at      TEXT,
    error         TEXT,
    input_tokens        INTEGER,
    output_tokens       INTEGER,
    cache_read_tokens   INTEGER,
    cache_write_tokens  INTEGER,
    reasoning_tokens    INTEGER,          -- share of output_tokens, never a fifth addend
    dollars             REAL,             -- nullable; subscription lanes may not price
    dollars_source      TEXT,
    usage_absent_reason TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id   TEXT NOT NULL REFERENCES sessions(run_id),
    phase_id INTEGER REFERENCES phases(id),
    ts       TEXT NOT NULL,
    kind     TEXT NOT NULL,
    detail   TEXT
);

CREATE TABLE IF NOT EXISTS envelopes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      TEXT NOT NULL REFERENCES sessions(run_id),
    phase_id    INTEGER REFERENCES phases(id),
    attempt     INTEGER NOT NULL DEFAULT 1,
    status      TEXT,
    summary     TEXT,
    artifacts_json TEXT,
    notes_for_next_agent TEXT,
    raw_path    TEXT,
    parse_error TEXT,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gate_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      TEXT NOT NULL REFERENCES sessions(run_id),
    phase_id    INTEGER REFERENCES phases(id),
    attempt     INTEGER NOT NULL DEFAULT 1,
    gate        TEXT NOT NULL,
    args_json   TEXT,
    status      TEXT NOT NULL,            -- PASS | FAIL | NOT_RUNNABLE (only PASS is green)
    detail      TEXT,
    evidence_json TEXT,
    duration_ms INTEGER,
    ts          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      TEXT NOT NULL REFERENCES sessions(run_id),
    phase_id    INTEGER REFERENCES phases(id),
    argv_json   TEXT NOT NULL,
    cwd         TEXT,
    exit_code   INTEGER,
    started_at  TEXT NOT NULL,
    ended_at    TEXT,
    stdout_path TEXT,
    stderr_path TEXT
);

CREATE TABLE IF NOT EXISTS agent_sessions (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id            TEXT NOT NULL REFERENCES sessions(run_id),
    phase_id          INTEGER REFERENCES phases(id),
    attempt           INTEGER NOT NULL DEFAULT 1,
    agent             TEXT NOT NULL,
    harness           TEXT NOT NULL,
    harness_session_id TEXT,
    model             TEXT,
    prompt_path       TEXT,
    raw_output_path   TEXT,
    started_at        TEXT NOT NULL,
    ended_at          TEXT
);

CREATE INDEX IF NOT EXISTS idx_phases_run ON phases(run_id);
CREATE INDEX IF NOT EXISTS idx_gate_results_phase ON gate_results(phase_id);
CREATE INDEX IF NOT EXISTS idx_events_run ON events(run_id);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Receipts:
    """Thin writer/reader over the receipts DB. Not thread-shared; one per run."""

    def __init__(self, db_path: Path | str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.executescript(_SCHEMA)
        self.conn.execute(
            "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (str(SCHEMA_VERSION),),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.commit()
        self.conn.close()

    def __enter__(self) -> "Receipts":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # -- sessions ----------------------------------------------------------
    def start_session(
        self,
        run_id: str,
        workflow: str,
        root: Path,
        session_dir: Path,
        workflow_path: str | None = None,
        workflow_sha256: str | None = None,
    ) -> None:
        self.conn.execute(
            "INSERT INTO sessions(run_id, workflow, workflow_path, workflow_sha256, root, "
            "session_dir, status, started_at) VALUES(?,?,?,?,?,?,'RUNNING',?)",
            (
                run_id,
                workflow,
                workflow_path,
                workflow_sha256,
                str(root),
                str(session_dir),
                utcnow(),
            ),
        )
        self.conn.commit()

    def finish_session(self, run_id: str, status: str, abort_reason: str | None = None) -> None:
        self.conn.execute(
            "UPDATE sessions SET status=?, ended_at=?, abort_reason=? WHERE run_id=?",
            (status, utcnow(), abort_reason, run_id),
        )
        self.conn.commit()

    # -- phases ------------------------------------------------------------
    def start_phase(
        self, run_id: str, idx: int, name: str, agent: str | None, harness: str | None
    ) -> int:
        cur = self.conn.execute(
            "INSERT INTO phases(run_id, idx, name, agent, harness, status, started_at) "
            "VALUES(?,?,?,?,?,'FAILED',?)",
            (run_id, idx, name, agent, harness, utcnow()),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def finish_phase(
        self,
        phase_id: int,
        status: str,
        attempts: int,
        usage: UsageBreakdown,
        error: str | None = None,
    ) -> None:
        self.conn.execute(
            "UPDATE phases SET status=?, attempts=?, ended_at=?, error=?, input_tokens=?, "
            "output_tokens=?, cache_read_tokens=?, cache_write_tokens=?, reasoning_tokens=?, "
            "dollars=?, dollars_source=?, usage_absent_reason=? WHERE id=?",
            (
                status,
                attempts,
                utcnow(),
                error,
                usage.input_tokens,
                usage.output_tokens,
                usage.cache_read_tokens,
                usage.cache_write_tokens,
                usage.reasoning_tokens,
                usage.dollars,
                usage.dollars_source,
                usage.absent_reason,
                phase_id,
            ),
        )
        self.conn.commit()

    # -- narrow writers ----------------------------------------------------
    def event(self, run_id: str, kind: str, detail: str = "", phase_id: int | None = None) -> None:
        self.conn.execute(
            "INSERT INTO events(run_id, phase_id, ts, kind, detail) VALUES(?,?,?,?,?)",
            (run_id, phase_id, utcnow(), kind, detail),
        )
        self.conn.commit()

    def record_envelope(
        self,
        run_id: str,
        phase_id: int,
        envelope: Any | None,
        attempt: int = 1,
        raw_path: str | None = None,
        parse_error: str | None = None,
    ) -> None:
        if envelope is None:
            row = (run_id, phase_id, attempt, None, None, None, None, raw_path, parse_error)
        else:
            row = (
                run_id,
                phase_id,
                attempt,
                envelope.status,
                envelope.summary,
                json.dumps(envelope.artifacts),
                envelope.notes_for_next_agent,
                raw_path,
                parse_error,
            )
        self.conn.execute(
            "INSERT INTO envelopes(run_id, phase_id, attempt, status, summary, artifacts_json, "
            "notes_for_next_agent, raw_path, parse_error, recorded_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
            row + (utcnow(),),
        )
        self.conn.commit()

    def record_gate(self, run_id: str, phase_id: int, report: Any, attempt: int = 1) -> None:
        self.conn.execute(
            "INSERT INTO gate_results(run_id, phase_id, attempt, gate, args_json, status, detail, "
            "evidence_json, duration_ms, ts) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                run_id,
                phase_id,
                attempt,
                report.gate,
                json.dumps(report.args, default=str),
                report.status,
                report.detail,
                json.dumps(report.evidence, default=str),
                report.duration_ms,
                utcnow(),
            ),
        )
        self.conn.commit()

    def record_process(
        self,
        run_id: str,
        phase_id: int | None,
        argv: Iterable[str],
        cwd: str | None,
        exit_code: int | None,
        started_at: str,
        stdout_path: str | None = None,
        stderr_path: str | None = None,
    ) -> None:
        self.conn.execute(
            "INSERT INTO processes(run_id, phase_id, argv_json, cwd, exit_code, started_at, "
            "ended_at, stdout_path, stderr_path) VALUES(?,?,?,?,?,?,?,?,?)",
            (
                run_id,
                phase_id,
                json.dumps(list(argv)),
                cwd,
                exit_code,
                started_at,
                utcnow(),
                stdout_path,
                stderr_path,
            ),
        )
        self.conn.commit()

    def record_agent_session(
        self,
        run_id: str,
        phase_id: int,
        agent: str,
        harness: str,
        attempt: int,
        harness_session_id: str | None,
        model: str | None,
        prompt_path: str | None,
        raw_output_path: str | None,
        started_at: str,
    ) -> None:
        self.conn.execute(
            "INSERT INTO agent_sessions(run_id, phase_id, attempt, agent, harness, "
            "harness_session_id, model, prompt_path, raw_output_path, started_at, ended_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (
                run_id,
                phase_id,
                attempt,
                agent,
                harness,
                harness_session_id,
                model,
                prompt_path,
                raw_output_path,
                started_at,
                utcnow(),
            ),
        )
        self.conn.commit()

    # -- readers -----------------------------------------------------------
    def session(self, run_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM sessions WHERE run_id=?", (run_id,)
        ).fetchone()

    def sessions(self, limit: int = 20) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?", (limit,)
            ).fetchall()
        )

    def phases(self, run_id: str) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT * FROM phases WHERE run_id=? ORDER BY idx ASC", (run_id,)
            ).fetchall()
        )

    def gates_for_phase(self, phase_id: int) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT * FROM gate_results WHERE phase_id=? ORDER BY id ASC", (phase_id,)
            ).fetchall()
        )

    def envelope_for_phase(self, phase_id: int) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM envelopes WHERE phase_id=? ORDER BY id DESC LIMIT 1", (phase_id,)
        ).fetchone()

    def events(self, run_id: str, limit: int = 200) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT * FROM events WHERE run_id=? ORDER BY id ASC LIMIT ?", (run_id, limit)
            ).fetchall()
        )

    def usage_totals(self, run_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT SUM(input_tokens) i, SUM(output_tokens) o, SUM(cache_read_tokens) cr, "
            "SUM(cache_write_tokens) cw, SUM(reasoning_tokens) r, SUM(dollars) d "
            "FROM phases WHERE run_id=?",
            (run_id,),
        ).fetchone()
        totals = {
            "input_tokens": row["i"],
            "output_tokens": row["o"],
            "cache_read_tokens": row["cr"],
            "cache_write_tokens": row["cw"],
            "reasoning_tokens": row["r"],
            "dollars": row["d"],
        }
        addends = [totals["input_tokens"], totals["output_tokens"],
                   totals["cache_read_tokens"], totals["cache_write_tokens"]]
        present = [a for a in addends if a is not None]
        # reasoning is a share of output -- deliberately not summed in
        totals["billable_token_total"] = sum(present) if present else None
        return totals

    def gate_verdict_tuples(self, run_id: str) -> list[tuple[str, str, str]]:
        """(phase_name, gate, status) in order -- the determinism comparison key."""
        rows = self.conn.execute(
            "SELECT p.name AS phase, g.gate AS gate, g.status AS status "
            "FROM gate_results g JOIN phases p ON p.id = g.phase_id "
            "WHERE g.run_id=? ORDER BY p.idx ASC, g.id ASC",
            (run_id,),
        ).fetchall()
        return [(r["phase"], r["gate"], r["status"]) for r in rows]
