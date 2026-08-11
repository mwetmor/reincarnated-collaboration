"""Receipts — SQLite in WAL mode. The run ledger's mechanical shadow.

Spec A § 6. Seven tables: sessions / phases / events / envelopes / gate_results /
processes / agent_sessions. One data path: the gates WRITE here and every surface
(status, report, future dashboard) READS here. A view is never truth.

Schema custody: star-lord (strategy § 8). Schema version is stamped in
`schema_meta` so a Tier-2 consumer can refuse an unknown version rather than
guess at it.

Gate-2 J5b: that sentence was FALSE for the whole of v1, and it is worth leaving the
correction next to the claim rather than quietly editing the claim. `__init__` ran
`CREATE TABLE IF NOT EXISTS` and then stamped the code's own constant unconditionally.
`IF NOT EXISTS` cannot add a column, so opening an old DB with new code left the old
table SHAPE in place and relabelled it with the new version — a stamp its own writer
overwrites on every open can never disagree, and what cannot disagree cannot refuse.
Order is now read -> migrate-or-refuse -> stamp. Migrations are additive only
(`_MIGRATIONS`), a NEWER DB raises `SchemaVersionError` and is deliberately NOT
restamped, and pre-existing rows are never backfilled. See `factory/MIGRATION.md`.

Gate-2 H6 (v3): `sessions` now also carries what the run could NOT see — the host's
own `permissions.defaultMode`, the trees actually fingerprinted, and the sentence
bounding what a green containment verdict means. Those live here rather than in a
log because a receipt read months later is the only place they can still be found,
and because a caveat that is not in the evidence store is not evidence. See
`factory/host.py` for what those values do and do not establish.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .host import HostPermissions
from .usage import UsageBreakdown

SCHEMA_VERSION = 3

#: Ordered, additive migrations from version N to N+1. Index 0 takes v1 -> v2.
#:
#: Gate-2 J5b. `CREATE TABLE IF NOT EXISTS` cannot add a column, so before this existed
#: opening an old DB with new code left the old table shape in place — and then stamped
#: it with the new version anyway (see `_stamp_version`). Additive only, deliberately:
#: `ADD COLUMN` cannot destroy a row, and a receipts DB is evidence. Anything that would
#: rewrite or drop is not a migration this module performs unattended.
_MIGRATIONS: tuple[tuple[str, ...], ...] = (
    (
        "ALTER TABLE agent_sessions ADD COLUMN permission_mode TEXT",
        "ALTER TABLE agent_sessions ADD COLUMN granted_tools TEXT",
        "ALTER TABLE agent_sessions ADD COLUMN denial_count INTEGER",
        "ALTER TABLE agent_sessions ADD COLUMN num_turns INTEGER",
        "ALTER TABLE agent_sessions ADD COLUMN stop_reason TEXT",
    ),
    # v2 -> v3. Gate-2 H6: the limits of the measurement, stored with the measurement.
    (
        "ALTER TABLE sessions ADD COLUMN host_permission_mode TEXT",
        "ALTER TABLE sessions ADD COLUMN host_permission_source TEXT",
        "ALTER TABLE sessions ADD COLUMN measured_trees TEXT",
        "ALTER TABLE sessions ADD COLUMN measurement_limit TEXT",
    ),
)


class SchemaVersionError(RuntimeError):
    """This DB was written by a schema version this code cannot read.

    Raised rather than guessed at. A receipts DB is evidence; reading it with the wrong
    column expectations produces confident wrong answers, which is worse than no answer.
    """

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
    abort_reason  TEXT,
    -- v3 (Gate-2 H6). What the factory could NOT measure, recorded next to what it
    -- could. `host_permission_mode` is NULL whenever the host did not state one —
    -- never filled with Claude Code's fallback, which would be a guess wearing a
    -- measurement's clothes. `measurement_limit` is the sentence that stops a green
    -- containment verdict from reading as "no writes anywhere".
    host_permission_mode   TEXT,
    host_permission_source TEXT,
    measured_trees         TEXT,          -- JSON array of the trees fingerprinted
    measurement_limit      TEXT
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
    ended_at          TEXT,
    -- Gate-2 J5. What the process was actually GRANTED, as the harness reported it in
    -- its init frame. `check_grant` adjudicates these and then they were dropped: on a
    -- FAILING phase the verdict survives in `phases.error`, but on a PASSING phase
    -- nothing durable recorded what the fence had been. The receipt could say the
    -- phase succeeded and could not say what it was allowed to do while succeeding.
    --
    -- Load-bearing because of J1: `--allowedTools` does not restrict in headless
    -- `default` mode (measured twice), so the argv is not evidence of the grant. The
    -- init frame is the only place the real answer appears, and this is the only place
    -- it is kept.
    permission_mode   TEXT,
    granted_tools     TEXT,   -- JSON array, as reported by the harness
    denial_count      INTEGER,
    num_turns         INTEGER,
    stop_reason       TEXT
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
        # Gate-2 J5b. Order matters and it was wrong. The stamp used to be written
        # AFTER `executescript` and UNCONDITIONALLY, from the code's own constant — so
        # opening a v1 database with v2 code left the v1 table shape untouched (`CREATE
        # TABLE IF NOT EXISTS` cannot add a column) and then relabelled it "2". The
        # module docstring says the stamp exists "so a Tier-2 consumer can refuse an
        # unknown version rather than guess at it"; a stamp the writer overwrites on
        # every open can never disagree, so it could never refuse. Measured, not
        # reasoned: a probe opened a v1 DB with SCHEMA_VERSION=2 and a new column, and
        # got stamp=2 with the column absent.
        #
        # That is this module's own failure of Discipline #8 — validation at the
        # boundary — in the one artifact whose whole job is to be trustworthy later.
        # So: READ first, migrate or refuse, stamp last.
        found = self._read_version()
        self.conn.executescript(_SCHEMA)      # creates anything missing entirely
        if found is not None and found != SCHEMA_VERSION:
            self._migrate(found)
        self._stamp_version()
        self.conn.commit()

    def _read_version(self) -> int | None:
        """The version this DB claims, or None if it is brand new."""
        try:
            row = self.conn.execute(
                "SELECT value FROM schema_meta WHERE key='schema_version'"
            ).fetchone()
        except sqlite3.OperationalError:
            return None          # no schema_meta table yet: a fresh file
        if row is None:
            return None
        try:
            return int(row[0])
        except (TypeError, ValueError):
            raise SchemaVersionError(
                f"receipts DB at {self.path} carries an unparseable schema_version "
                f"{row[0]!r}. Refusing to guess at its shape."
            ) from None

    def _migrate(self, found: int) -> None:
        if found > SCHEMA_VERSION:
            raise SchemaVersionError(
                f"receipts DB at {self.path} is schema version {found}; this code "
                f"knows version {SCHEMA_VERSION}. It was written by a NEWER factory. "
                "Refusing to open it — reading evidence with the wrong column "
                "expectations yields confident wrong answers."
            )
        for step in range(found, SCHEMA_VERSION):
            for stmt in _MIGRATIONS[step - 1]:
                try:
                    self.conn.execute(stmt)
                except sqlite3.OperationalError as exc:
                    # A column already present is the one benign case: a DB created
                    # fresh by `_SCHEMA` at the new shape but stamped at an old
                    # version. Anything else is a migration that did not apply, and a
                    # migration that did not apply must not be stamped as though it had.
                    if "duplicate column name" not in str(exc):
                        raise SchemaVersionError(
                            f"migration {found} -> {SCHEMA_VERSION} failed on "
                            f"{stmt!r}: {exc}. The DB is NOT restamped."
                        ) from exc

    def _stamp_version(self) -> None:
        self.conn.execute(
            "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (str(SCHEMA_VERSION),),
        )

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
        host: "HostPermissions | None" = None,
        measured_trees: Iterable[Path | str] | None = None,
        measurement_limit: str | None = None,
    ) -> None:
        """Open the session row — including what this run could NOT see (H6).

        `host` is the ONE layer of host permission configuration this factory reads;
        its `source` sentence travels with it and is the only thing that makes the
        mode readable later. `measurement_limit` is the sentence bounding the
        containment claim.

        `measured_trees` is the DECLARED set — the workflow's `repos`, recorded here at
        session open, BEFORE a single fingerprint has been taken. The v3 wording said
        "the set actually fingerprinted", which is H6's own defect committed inside
        H6's fix: a name and a docstring answering a question about the MEASUREMENT
        while the value answers a question about the DECLARATION (Gate-2 JR-1). The two
        coincide on every run that reaches its first phase and diverge on any run that
        aborts before one — where "fingerprinted" would be a false claim on a receipt.

        Recorded from the declaration deliberately, rather than fixed by writing later.
        A run that aborts at load must still leave behind WHAT IT WAS GOING TO MEASURE;
        the alternative is a session row with no trees, which reads as "nothing was in
        scope" — absent standing in for unmeasured, which is the law this column exists
        to serve.

        All three are optional so that v1/v2 call sites keep working, and all three
        land as NULL when omitted. NULL means UNRECORDED. It does not mean the host
        was unrestricted, and it does not mean nothing was measured — see
        `factory/MIGRATION.md`, which is the contract a query must read first.
        """
        trees = None if measured_trees is None else json.dumps([str(t) for t in measured_trees])
        self.conn.execute(
            "INSERT INTO sessions(run_id, workflow, workflow_path, workflow_sha256, root, "
            "session_dir, status, started_at, host_permission_mode, host_permission_source, "
            "measured_trees, measurement_limit) VALUES(?,?,?,?,?,?,'RUNNING',?,?,?,?,?)",
            (
                run_id,
                workflow,
                workflow_path,
                workflow_sha256,
                str(root),
                str(session_dir),
                utcnow(),
                host.mode if host else None,
                host.source if host else None,
                trees,
                measurement_limit,
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
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Gate-2 J5. `extra` is the harness's init/result evidence, and it is now KEPT.

        `granted_tools` is stored as JSON rather than a joined string because the
        distinction between "no tools key was reported" and "an empty tool list was
        reported" is exactly the distinction `check_grant` turns on, and a joined
        string renders both as "". Absent is absent (`usage.py`'s law), applied to
        containment evidence instead of to tokens.
        """
        extra = extra or {}
        granted = extra.get("granted_tools")
        denials = extra.get("permission_denials")
        self.conn.execute(
            "INSERT INTO agent_sessions(run_id, phase_id, attempt, agent, harness, "
            "harness_session_id, model, prompt_path, raw_output_path, started_at, ended_at, "
            "permission_mode, granted_tools, denial_count, num_turns, stop_reason) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
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
                extra.get("permission_mode"),
                None if granted is None else json.dumps(granted),
                None if denials is None else len(denials),
                extra.get("num_turns"),
                extra.get("stop_reason"),
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
            # A summed figure carries the provenance of everything summed into it. If
            # two lanes priced differently, BOTH labels travel -- the total is never
            # allowed to describe itself with a label the runner hard-coded (D-4).
            "dollars_sources": [
                r["dollars_source"]
                for r in self.conn.execute(
                    "SELECT DISTINCT dollars_source FROM phases "
                    "WHERE run_id=? AND dollars IS NOT NULL ORDER BY dollars_source",
                    (run_id,),
                ).fetchall()
            ],
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
