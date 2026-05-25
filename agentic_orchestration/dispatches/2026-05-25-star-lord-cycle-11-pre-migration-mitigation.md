# Dispatch — 2026-05-25 — star-lord — Cycle 11 pre-migration mitigation (PRAGMA busy_timeout)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-05-25 (P2.5 ratification — "I confirm")
**Estimated effort:** ~10 minutes
**Acceptance:** PRAGMA `busy_timeout = 30000` set at SQLite connection open in `telemetry/db.py` line ~29; smoke verifies SQLite connections inherit the setting

---

## Context

Cycle 10 post-cycle G1 infrastructure measurement (dispatch `2026-05-25-star-lord-g1-infrastructure-measurement.md`) CONFIRMED SQLite contention with 4 kernel panics during sustained workload. The cause-effect chain (G1 finding) is: multi-writer concurrent access against the telemetry SQLite DB exhausts lock retries; failed writes propagate as immediate errors; sustained pressure correlates with Mac mini kernel panic.

Matt P2a decision: hybrid Pi-Postgres / hosted-Postgres path RATIFIED but DEFERRED to "right moment" trigger. Status-quo continues against SQLite until Postgres migration fires. Matt P2.5 decision: apply PRAGMA busy_timeout mitigation NOW to convert lock-busy failures from immediate-fail to wait-and-retry. This does NOT fix the multi-writer architectural problem but eliminates the immediate-failure symptom while we wait for "right moment."

This is Cycle 11 Wave 1, zero-dependency, ~10-minute work — first dispatch fired at Cycle 11 open per scope-doc § 8 sequencing.

## Required reading before starting

- `agentic_orchestration/dispatches/2026-05-25-star-lord-g1-infrastructure-measurement.md` § completion record (G1 findings: SQLite contention + 4 kernel panics confirmed)
- `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 7 D1 + § 8 (Pi infrastructure recognition record + Matt P2a hybrid path)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2.5 (Matt verbatim authorization)
- Current `~/Games/reincarnated-engine/src/reincarnated/telemetry/db.py` around line 29 (connection open site)

## Math-before-code

No math required. Single configuration change:
- `PRAGMA busy_timeout = 30000` (milliseconds = 30 seconds)
- Applied at SQLite connection open via `cursor.execute("PRAGMA busy_timeout = 30000")` immediately after connection is established

Behavior change: SQLite will wait up to 30 seconds for a busy lock to release before raising `OperationalError: database is locked`. Previous behavior: immediate fail.

Rationale for 30-second value: per SQLite docs, busy_timeout should comfortably exceed typical write latencies. Engine writes complete in milliseconds; 30s gives generous headroom for transient multi-writer pressure without masking genuine deadlocks. Matt verbatim "30000" in Q2.5 authorization.

## Cross-seam contract change? (Principle 6 gate)

**No.** PRAGMA busy_timeout is a SQLite connection-level setting; no schema change; no field add/modify/rename; no inter-seam fixture dict touched. Existing fight_log / loadout / export packet contracts unchanged.

Round-trip: not applicable — no cross-seam contract change in this dispatch.

## Scope

- [ ] Add `PRAGMA busy_timeout = 30000` execution immediately after SQLite connection open in `telemetry/db.py` around line 29
- [ ] Verify the PRAGMA is applied per-connection (if `db.py` uses a connection factory pattern, the PRAGMA must execute on every new connection; otherwise once at module-level connection)
- [ ] Smoke test: open a connection, query `PRAGMA busy_timeout;`, verify returned value = 30000
- [ ] Tag: `star-lord/v0.0-cycle-11-pre-migration-mitigation-2026-05-25`
- [ ] AGENT_STATE.md updated at session end

## Acceptance criteria

- [ ] `db.py` modified with PRAGMA busy_timeout set
- [ ] Smoke confirms returned PRAGMA value = 30000 on a fresh connection
- [ ] No regression in existing telemetry write paths (a single fight_log write completes without error)
- [ ] Round-trip: not applicable — no cross-seam contract change in this dispatch

## Out of scope (explicit non-goals)

- DO NOT migrate to Postgres (deferred per Matt P2a "right moment")
- DO NOT install Tailscale (G11 task; independent of Cycle 11)
- DO NOT refactor multi-writer architecture (waiting for Postgres trigger)
- DO NOT change journal mode (WAL, etc.) beyond current default — that's a separate architectural decision
- DO NOT raise the busy_timeout above 30000 (Matt-specified value)

## Open questions for the agent to resolve

- If `db.py` uses connection pooling or per-call connections, ensure PRAGMA fires on every new connection (test by opening multiple connections in smoke and verifying each shows 30000)
- If connection open is in a function called from many sites, prefer a centralized PRAGMA application over per-call duplication

## References

- Matt verbatim: "I confirm" (P2.5 — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2.5)
- G1 completion record: `agentic_orchestration/dispatches/2026-05-25-star-lord-g1-infrastructure-measurement.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 0 + § 1
- Pi recognition record: `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md`
