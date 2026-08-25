"""U-1 fleet flight-recorder — record schema v1.1 (v1 FROZEN + AM-1 custodian amendment).

Truth-of-record: append-only JSONL at `agentic_orchestration/flight/records-YYYY-MM.jsonl`.

Founding version = spec § 3
(`agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`)
**plus the six binding amendments B-1…B-6** from jack-ryan's G-1 ratification
(`agentic_orchestration/qa/findings/2026-08-24-u1-schema-law-ratification.md`).
Custodian: star-lord. Field tables are the machine-readable twin of `SCHEMA.md`.

THE SIX AMENDMENTS, and where each lives in this file:
  B-1  `row_id` defined; `corrects` must reference an existing row_id carrying the SAME
       `unit_id` and `event`.                          -> compute_row_id / validate / tape.audit
  B-2  `verdict` never comes from `rc`. Non-null `verdict` REQUIRES a named `gatekeeper`
       (and, here, a `derived_from` — stricter, deliberately).            -> FIELD_MATRIX
  B-3  REQUIRED / OPTIONAL / FORBIDDEN matrix keyed by event type, machine-checked.
       Identity is DENORMALIZED onto CLOSE (the lean, ADOPTED — see SCHEMA.md § 8 D-3).
                                                                          -> FIELD_MATRIX
  B-4  Field set CLOSED; unknown keys REJECTED; no field named for a metric.
                                                       -> ALL_FIELDS / _assert_no_metric_names
  B-5  `derived_from` is a LIST; any row carrying a token primitive or a verdict MUST name a
       source, and every named path MUST exist on disk.                   -> validate
  B-6  `curator` exists and is REQUIRED on ENQUEUE for vendor lanes.      -> FIELD_MATRIX

AMENDMENT AM-1 (revision 1.1, 2026-08-24) — Matt mid-run directive, spec § 13.2, custodian
star-lord, micro-gate G-2b (jack-ryan). Three changes, ALL ADDITIVE-OR-RENAME, no field removed,
no type changed, no rule weakened:
  1.1-a  lane `grok-judge` -> `grok-serial` (workload-class vs execution-stream conflation;
         mirrors `codex-serial`). TAPE-SAFE: verified zero `grok` rows on the tape before the
         rename (`grep -c grok records-2026-08.jsonl` = 0).
  1.1-b  currency `grok-sub` ADDED (grok.com subscription — the third economy).
  1.1-c  field `cost_usd` ADDED, CLOSE-only, OPTIONAL — the vendor's OWN reported dollar cost,
         copied verbatim (Grok emits `costUSD` per call). A REPORTED PRIMITIVE, not a
         derivation: derived-not-stored is untouched, and it owes `derived_from` exactly like a
         token count does.

HARD RULES:
  * a row is NEVER rewritten — corrections are new rows carrying `corrects: <row_id>`
  * a token count is NEVER estimated — absent is absent (no zero-filling, no defaults)
  * a cost is NEVER computed here — only a vendor-reported dollar figure is stored
  * a verdict NEVER self-reports — it names its judge and its artifact
  * telemetry only — identifiers, counts, timestamps, enums, paths. Never work-product bodies.

Python 3 stdlib only. No network. No LLM. Ever.
"""

from __future__ import annotations

import hashlib
import json
import os
import re

# --- versioning -------------------------------------------------------------
# TWO markers, deliberately, and the distinction is the custodian's AM-1 ruling:
#
#   SCHEMA_VERSION   the ROW-FORMAT version stamped in every row's `v`. It changes only when a
#                    row written under it stops being readable/valid under the validator — i.e.
#                    on a REMOVAL, a TYPE CHANGE, or a tightened requirement. AM-1 does none of
#                    those, so it stays 1 and all 67 pre-AM-1 rows remain valid untouched.
#   SCHEMA_REVISION  the CUSTODIAN-AMENDMENT marker (`"1.1"`). It changes on any additive
#                    amendment — new field, new enum value, new rule — and it is what SCHEMA.md,
#                    the report header, and a reader's "which revision do I need" question
#                    resolve against.
#
# WHY NOT `v:2` on new rows, which is the letter of jack-ryan's B-4 ("adding a field is a
# version bump (v:2) with a custodian-signed note"): stamping v:2 would fork the validator into
# per-version branches to keep the 67 existing rows legal, and "ONE validator, zero exceptions"
# (G2-T3) is a HARD gate property I will not trade for a stamp. The substance B-4 asked for is
# delivered in full — a version bump, a custodian-signed note, a red test unless the literal is
# amended deliberately — with the marker placed where it does not break the tape. Which revision
# a given row NEEDS stays DERIVABLE from its own key set (`row_min_revision`), never stored:
# a stamp would be a hand-written summary of the row's own contents, which is the R-L47-2 defect.
# Declared for G-2b; jack-ryan rules. If he prefers `v:2`, the cost is the validator fork and I
# will say so again before building it.
SCHEMA_VERSION = 1
SCHEMA_REVISION = "1.1"

#: Custodian amendment lineage — append-only, like the tape it governs.
SCHEMA_REVISIONS = (
    ("1.0", "2026-08-24", "star-lord",
     "FREEZE at a4f7a569 — spec § 3 + jack-ryan's G-1 amendments B-1…B-6 (G-2 PASS)"),
    ("1.1", "2026-08-24", "star-lord",
     "AM-1 (Matt directive, spec § 13.2): lane grok-judge->grok-serial (tape-safe, 0 grok rows); "
     "currency grok-sub added; cost_usd added CLOSE-only optional as a vendor-REPORTED primitive"),
)

#: Which revision a field was introduced in. A row's minimum revision is DERIVED from its keys.
FIELD_SINCE = {"cost_usd": "1.1"}

_HERE = os.path.dirname(os.path.abspath(__file__))
META_REPO_ROOT = os.path.dirname(os.path.dirname(_HERE))   # …/reincarnated-collaboration
_SIBLING_ROOT = os.path.dirname(META_REPO_ROOT)            # …/Games

# --- § 3.1 event types -------------------------------------------------------
EVENTS = ("ENQUEUE", "START", "GATE", "HALT", "CURATION", "SNAPSHOT", "CLOSE")
TERMINAL_EVENTS = ("CLOSE",)

# --- enums -------------------------------------------------------------------
UNIT_KINDS = ("job", "dispatch", "run", "wave", "session")

VERDICTS = ("PASS", "PASS-WITH-FINDINGS", "BLOCK", "REFUSAL", "HALT",
            "FALLBACK-TAKEN", "FAILED", "SKIP")

# AM-1 1.1-a: `grok-serial` mirrors `codex-serial`. The v1 name `grok-judge` named a WORKLOAD
# CLASS (the U-8 judge door) in a field whose job is to name an EXECUTION STREAM — the two are
# orthogonal, and a lane enum that encodes admission policy cannot survive the policy changing.
LANES = ("claude-agent", "claude-subagent", "codex-serial",
         "grok-serial", "cross-vendor-judge")

# B-6: lanes that spend a vendor's economy and therefore owe a named curator at enqueue.
VENDOR_LANES = ("codex-serial", "grok-serial", "cross-vendor-judge")

# AM-1 1.1-b: `grok-sub` is the grok.com subscription — the third economy.
CURRENCIES = ("anthropic-max", "chatgpt-sub", "api-metered", "grok-sub")

FABRICATION_CHECKS = ("pass", "fail", "not-run")

# `provider`, `pin`, `harness`, `operator`, `curator`, `seam`, `repo`, `workstream` are OPEN
# strings: a closed enum there would make the recorder refuse to record reality.

# --- WARN-1: the staleness class key is DECLARED IN SCHEMA, not invented at render time ----
SLA_CLASS_KEY = ("lane", "unit_kind")
SLA_MIN_N = 5   # below this n a class has no median worth colouring; the lane says so

# --- field groups ------------------------------------------------------------
COMMON_FIELDS = ("v", "row_id", "ts", "event", "unit_id", "unit_kind", "parent_id",
                 "workstream", "operator", "seam", "repo", "backfill", "corrects",
                 "derived_from")

IDENTITY_FIELDS = ("provider", "lane", "pin", "model_echo", "harness", "harness_version",
                   "currency", "curator")

COST_FIELDS = ("tokens_input", "tokens_cached_input", "tokens_cache_write",
               "tokens_output", "tokens_reasoning", "cost_usd",
               "rc", "attempt", "retry_of", "artifacts")

OUTCOME_FIELDS = ("verdict", "gate_id", "gatekeeper", "warn_count", "fabrication_check")

SNAPSHOT_FIELDS = ("meter_raw",)

TOKEN_FIELDS = ("tokens_input", "tokens_cached_input", "tokens_cache_write",
                "tokens_output", "tokens_reasoning")

# AM-1 1.1-c: numbers the VENDOR reported about what a call cost, copied verbatim. They join the
# token primitives in owing a `derived_from` — a dollar figure with no named artifact is exactly
# the unsourced claim B-5 exists to refuse.
REPORTED_COST_FIELDS = ("cost_usd",)

# Serialization order — readability only; hashing always uses sorted keys.
FIELD_ORDER = COMMON_FIELDS + IDENTITY_FIELDS + OUTCOME_FIELDS + COST_FIELDS + SNAPSHOT_FIELDS
ALL_FIELDS = frozenset(FIELD_ORDER)

# --- B-4: no field may be named for a metric ---------------------------------
METRIC_NAME_TOKENS = ("rate", "pct", "percent", "avg", "mean", "median", "total",
                      "count", "duration", "sum", "ratio")

# The single grandfathered exception, ruled explicitly by the custodian rather than
# silently allowed. `warn_count` is spec § 3.5 vocabulary and is a PRIMITIVE the curator
# reported — copied verbatim like a token count, never computed from other rows. Renaming a
# spec field would have broken jack-ryan's verified fork-fidelity mapping; declaring the
# exception keeps the rule greppable (G2-T6) and the deviation visible.
METRIC_NAME_EXCEPTIONS = ("warn_count",)


def _assert_no_metric_names():
    bad = []
    for f in FIELD_ORDER:
        if f in METRIC_NAME_EXCEPTIONS:
            continue
        for tokname in METRIC_NAME_TOKENS:
            if tokname in f.lower():
                bad.append((f, tokname))
    if bad:
        raise AssertionError(
            "B-4 violation — field named for a metric: %r. Metrics are DERIVED at render "
            "time and stored nowhere." % (bad,))


_assert_no_metric_names()

# --- B-3: the normative per-event field matrix -------------------------------
# R = required non-null · O = optional · F = forbidden (absent, or null where the spec
# mandates an explicit null). Any field/event pair not listed defaults to F.
R, O, F = "R", "O", "F"


def _matrix():
    m = {e: {} for e in EVENTS}

    def put(fields, spec):
        for e in EVENTS:
            for fl in fields:
                m[e][fl] = spec[e]

    # always required
    put(("v", "row_id", "ts", "event"), {e: R for e in EVENTS})
    # unit binding
    put(("unit_id",), dict.fromkeys(EVENTS, R) | {"SNAPSHOT": F})
    put(("unit_kind",), dict.fromkeys(EVENTS, R) | {"SNAPSHOT": F})
    put(("parent_id",), dict.fromkeys(EVENTS, O) | {"SNAPSHOT": F})
    # free-form context, legal everywhere
    put(("workstream", "operator", "seam", "repo", "backfill", "corrects", "derived_from"),
        dict.fromkeys(EVENTS, O))
    # identity axes — ENQUEUE included so B-6's curator rule has a lane to test against;
    # DENORMALIZED onto CLOSE (B-3 lean ADOPTED: a CLOSE must be self-describing).
    put(("provider", "lane", "pin", "model_echo", "harness", "harness_version", "curator"),
        dict.fromkeys(EVENTS, F) | {"ENQUEUE": O, "START": O, "CLOSE": O})
    put(("currency",),
        dict.fromkeys(EVENTS, F) | {"ENQUEUE": O, "START": O, "CLOSE": O, "SNAPSHOT": R})
    # outcome axes
    put(("verdict",), dict.fromkeys(EVENTS, F) | {"GATE": R, "CURATION": O, "CLOSE": O})
    put(("gate_id",), dict.fromkeys(EVENTS, F) | {"GATE": R})
    put(("gatekeeper",), dict.fromkeys(EVENTS, F) | {"GATE": R, "CURATION": R, "CLOSE": O})
    put(("warn_count", "fabrication_check"), dict.fromkeys(EVENTS, F) | {"CURATION": O})
    # cost axes — CLOSE only
    put(COST_FIELDS, dict.fromkeys(EVENTS, F) | {"CLOSE": O})
    # snapshot
    put(("meter_raw",), dict.fromkeys(EVENTS, F) | {"SNAPSHOT": R})
    return m


FIELD_MATRIX = _matrix()

TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
MONTH_RE = re.compile(r"^(\d{4}-\d{2})")


class SchemaError(ValueError):
    """Raised when a row cannot legally join the tape."""


def month_of(ts: str) -> str:
    m = MONTH_RE.match(ts or "")
    if not m:
        raise SchemaError("ts %r has no parseable YYYY-MM" % (ts,))
    return m.group(1)


def canonical_json(row: dict) -> str:
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_row_id(row: dict) -> str:
    """B-1: content address of a row (row_id excluded from its own hash).

    Deterministic rather than random, so a re-run backfill produces byte-identical ids —
    which is what makes normalization idempotent with no side-car state file.
    """
    payload = {k: v for k, v in row.items() if k != "row_id"}
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()[:16]


def row_min_revision(row: dict) -> str:
    """The lowest custodian revision that can READ this row — DERIVED from its own key set.

    Nothing is stamped: a per-row revision string would be a hand-written summary of the row's
    own contents, and a hand-written summary is a defect waiting to disagree with the thing it
    summarises (R-L47-2). Ask the keys instead.
    """
    best = "1.0"
    for k in row:
        since = FIELD_SINCE.get(k)
        if since and _revision_tuple(since) > _revision_tuple(best):
            best = since
    return best


def _revision_tuple(rev: str):
    return tuple(int(x) for x in rev.split("."))


def serialize(row: dict) -> str:
    ordered = {}
    for k in FIELD_ORDER:
        if k in row:
            ordered[k] = row[k]
    for k in row:
        if k not in ALL_FIELDS:
            ordered[k] = row[k]
    return json.dumps(ordered, separators=(",", ":"), ensure_ascii=False)


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def resolve_path(rel: str, repo: str = None, repo_root: str = None) -> str:
    """Resolve a `derived_from` / artifact path.

    Paths are repo-root-relative within the repo named on the row. A `#anchor` suffix
    (`workflow-upgrades.md#§ U-4`) points at a section and is stripped before the disk check.
    """
    rel = (rel or "").split("#", 1)[0]
    if repo_root is None:
        repo_root = META_REPO_ROOT
        if repo and repo != os.path.basename(META_REPO_ROOT):
            cand = os.path.join(_SIBLING_ROOT, repo)
            if os.path.isdir(cand):
                repo_root = cand
    return os.path.join(repo_root, rel)


def validate(row: dict, repo_root: str = None, check_paths: bool = True) -> list:
    """Return a list of human-readable problems. Empty list == the row may join the tape.

    ONE validator, no per-workflow branch, no skip list (G2-T3).
    """
    errs = []

    # --- B-4: closed field set ----------------------------------------------
    for k in row:
        if k not in ALL_FIELDS:
            errs.append("B-4: unknown field %r — schema v1's field set is CLOSED; adding a "
                        "field is a v:2 bump with a custodian-signed note" % k)

    if row.get("v") != SCHEMA_VERSION:
        errs.append("v must be %d, got %r" % (SCHEMA_VERSION, row.get("v")))

    ts = row.get("ts")
    if not isinstance(ts, str) or not TS_RE.match(ts):
        errs.append("ts must be ISO-8601 UTC 'YYYY-MM-DDTHH:MM:SSZ', got %r" % (ts,))

    event = row.get("event")
    if event not in EVENTS:
        errs.append("event must be one of %s, got %r" % (list(EVENTS), event))
        return errs

    if not isinstance(row.get("row_id"), str) or not row.get("row_id"):
        errs.append("B-1: row_id must be a non-empty string")

    # --- B-3: the normative per-event matrix --------------------------------
    matrix = FIELD_MATRIX[event]
    for field in FIELD_ORDER:
        rule = matrix.get(field, F)
        present = field in row and row[field] is not None
        if rule == R and not present:
            if field == "unit_id" and event == "SNAPSHOT":
                continue
            errs.append("B-3: %s is REQUIRED on %s" % (field, event))
        if rule == F and present:
            errs.append("B-3: %s is FORBIDDEN on %s" % (field, event))
    if event == "SNAPSHOT":
        if "unit_id" not in row or row["unit_id"] is not None:
            errs.append("B-3: SNAPSHOT is not unit-bound; unit_id must be an explicit null")

    # --- enums ---------------------------------------------------------------
    if row.get("unit_kind") is not None and row["unit_kind"] not in UNIT_KINDS:
        errs.append("unit_kind must be one of %s, got %r" % (list(UNIT_KINDS), row["unit_kind"]))
    if row.get("lane") is not None and row["lane"] not in LANES:
        errs.append("lane must be one of %s (U-8 adds an enum VALUE, not a schema), got %r"
                    % (list(LANES), row["lane"]))
    if row.get("currency") is not None and row["currency"] not in CURRENCIES:
        errs.append("currency must be one of %s, got %r" % (list(CURRENCIES), row["currency"]))
    if row.get("verdict") is not None and row["verdict"] not in VERDICTS:
        errs.append("verdict must be one of %s, got %r" % (list(VERDICTS), row["verdict"]))
    if (row.get("fabrication_check") is not None
            and row["fabrication_check"] not in FABRICATION_CHECKS):
        errs.append("fabrication_check must be one of %s" % (list(FABRICATION_CHECKS),))
    if "backfill" in row and not isinstance(row["backfill"], bool):
        errs.append("backfill must be a bool")

    # --- types ---------------------------------------------------------------
    for f in TOKEN_FIELDS:
        if row.get(f) is not None and (not _is_int(row[f]) or row[f] < 0):
            errs.append("%s must be a non-negative int copied from a vendor stream "
                        "(absent when unknown — NEVER estimated), got %r" % (f, row[f]))
    for f in ("rc", "attempt", "warn_count"):
        if row.get(f) is not None and not _is_int(row[f]):
            errs.append("%s must be an int, got %r" % (f, row[f]))
    for f in REPORTED_COST_FIELDS:
        v = row.get(f)
        if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0):
            errs.append("%s must be a non-negative number the VENDOR reported, copied verbatim "
                        "(absent when the stream did not report one — NEVER computed from a "
                        "token count and a price list), got %r" % (f, v))
    if row.get("meter_raw") is not None and not isinstance(row["meter_raw"], dict):
        errs.append("meter_raw must be an object carrying the meter's own vocabulary")
    if row.get("corrects") is not None and not isinstance(row["corrects"], str):
        errs.append("corrects must be a row_id string")

    artifacts = row.get("artifacts")
    if artifacts is not None:
        if not isinstance(artifacts, list):
            errs.append("artifacts must be a list of {path, bytes}")
        else:
            for a in artifacts:
                if not isinstance(a, dict) or not a.get("path"):
                    errs.append("artifact entries need a 'path'; got %r" % (a,))
                    continue
                if a.get("bytes") is not None and not _is_int(a["bytes"]):
                    errs.append("artifact bytes must be an int measured from disk")
                if check_paths and not os.path.exists(
                        resolve_path(a["path"], row.get("repo"), repo_root)):
                    errs.append("artifact path does not resolve on disk: %s" % a["path"])

    # --- B-5: sources are a LIST, and they must exist ------------------------
    df = row.get("derived_from")
    if df is not None:
        if not isinstance(df, list) or not df or not all(isinstance(x, str) and x for x in df):
            errs.append("B-5: derived_from must be a non-empty LIST of artifact paths")
        elif check_paths:
            for src in df:
                if not os.path.exists(resolve_path(src, row.get("repo"), repo_root)):
                    errs.append("B-5: derived_from path does not resolve on disk: %s" % src)

    needs_source = []
    if any(row.get(f) is not None for f in TOKEN_FIELDS):
        needs_source.append("a token primitive")
    if any(row.get(f) is not None for f in REPORTED_COST_FIELDS):
        needs_source.append("a vendor-reported cost")
    if row.get("verdict") is not None:
        needs_source.append("a verdict")
    if needs_source and not df:
        errs.append("B-5: this row carries %s and MUST name its source in derived_from — "
                    "every number and every judgement is reproducible from a named artifact"
                    % " and ".join(needs_source))

    # --- B-2: a verdict never self-reports -----------------------------------
    if row.get("verdict") is not None and not row.get("gatekeeper"):
        errs.append("B-2: verdict %r requires a named gatekeeper. An exit code is a mechanical "
                    "fact about a process (`rc`), not a judgement about a work-product."
                    % row["verdict"])

    # --- B-6: vendor lanes owe a named curator at enqueue --------------------
    if event == "ENQUEUE" and row.get("lane") in VENDOR_LANES and not row.get("curator"):
        errs.append("B-6: lane %r is a vendor lane; `curator` is REQUIRED at ENQUEUE "
                    "(U-4 R-B: a job whose curator field is empty is a refusal to fire)"
                    % row["lane"])

    return errs


def make_row(event: str, ts: str, repo_root: str = None, check_paths: bool = True,
             **fields) -> dict:
    """Build + validate a row, stamping `v` and the deterministic `row_id`.

    `None` values are DROPPED, not stored: an absent field is an honest unknown, and a stored
    null would make the tape look like it measured something it did not. Sole exception:
    `unit_id` on SNAPSHOT, which spec § 3.2 mandates as an explicit null.
    """
    row = {"v": SCHEMA_VERSION, "ts": ts, "event": event}
    for k, val in fields.items():
        if val is None:
            continue
        row[k] = val
    if event == "SNAPSHOT":
        row["unit_id"] = None
    row["row_id"] = compute_row_id(row)

    errs = validate(row, repo_root=repo_root, check_paths=check_paths)
    if errs:
        raise SchemaError("invalid %s row:\n  - %s" % (event, "\n  - ".join(errs)))
    return row


def parse_line(line: str) -> dict:
    return json.loads(line)


def read_tape(paths) -> list:
    rows = []
    for p in paths:
        with open(p, "r", encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(parse_line(line))
                except Exception as exc:  # a corrupt tape must be loud, never skipped
                    raise SchemaError("%s:%d not valid JSON: %s" % (p, n, exc))
    return rows


def correction_errors(rows) -> list:
    """B-1: a correction must target an existing row_id with the SAME unit_id and event."""
    by_id = {r.get("row_id"): r for r in rows}
    errs = []
    for r in rows:
        tgt_id = r.get("corrects")
        if not tgt_id:
            continue
        tgt = by_id.get(tgt_id)
        if tgt is None:
            errs.append("B-1: row %s corrects %s, which is not on the tape"
                        % (r.get("row_id"), tgt_id))
            continue
        if tgt.get("unit_id") != r.get("unit_id") or tgt.get("event") != r.get("event"):
            errs.append("B-1: row %s corrects %s but differs in unit_id/event (%s/%s vs %s/%s)"
                        % (r.get("row_id"), tgt_id, r.get("unit_id"), r.get("event"),
                           tgt.get("unit_id"), tgt.get("event")))
    return errs


def apply_corrections(rows):
    """Drop rows superseded by a later row carrying `corrects`. Disk is untouched."""
    corrected = {r["corrects"] for r in rows if r.get("corrects")}
    return [r for r in rows if r.get("row_id") not in corrected]


def fold(rows):
    """Group rows by unit_id. State is DERIVED, never stored.

      SEALED    — a terminal event is present
      IN-FLIGHT — START seen, no terminal event
      QUEUED    — ENQUEUE seen, no START
      OPEN      — anything else (a bare GATE/HALT on a unit never started under the recorder)
    """
    units = {}
    for r in rows:
        uid = r.get("unit_id")
        if uid is None:
            continue
        units.setdefault(uid, []).append(r)

    out = {}
    for uid, rs in units.items():
        rs = sorted(rs, key=lambda r: (r.get("ts", ""),
                                       EVENTS.index(r["event"]) if r.get("event") in EVENTS
                                       else 99))
        kinds = {r["event"] for r in rs}
        if kinds & set(TERMINAL_EVENTS):
            state = "SEALED"
        elif "START" in kinds:
            state = "IN-FLIGHT"
        elif "ENQUEUE" in kinds:
            state = "QUEUED"
        else:
            state = "OPEN"
        out[uid] = {"rows": rs, "latest": rs[-1], "state": state}
    return out


def coverage(rows):
    """WARN-5: the population the tape does NOT cover, so no lane reads as a census."""
    ts = sorted(r["ts"] for r in rows if r.get("ts"))
    return {"first_ts": ts[0] if ts else None,
            "last_ts": ts[-1] if ts else None,
            "rows": len(rows)}
