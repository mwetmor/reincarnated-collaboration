"""U-1 fleet flight-recorder — tape I/O.

The ONE data path: every emitter appends through `append_row`, every view reads through
`load`. There is no edit verb and no delete verb anywhere in this module, by construction.

Python 3 stdlib only.
"""

from __future__ import annotations

import glob
import json
import os

import schema

TAPE_GLOB = "records-*.jsonl"


def tape_path(records_dir: str, ts: str) -> str:
    """The monthly file an event belongs to, chosen from the event's own UTC ts."""
    return os.path.join(records_dir, "records-%s.jsonl" % schema.month_of(ts))


def tape_files(records_dir: str) -> list:
    return sorted(glob.glob(os.path.join(records_dir, TAPE_GLOB)))


def existing_row_ids(path: str) -> set:
    if not os.path.exists(path):
        return set()
    ids = set()
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(json.loads(line).get("row_id"))
            except Exception:
                continue
    return ids


def append_row(row: dict, records_dir: str, force: bool = False, dry_run: bool = False,
               repo_root: str = None):
    """Append one validated row. Returns (path, 'appended' | 'duplicate').

    Duplicate detection is by content-addressed row_id, which is what makes backfills
    idempotent without any side-car state. `force=True` appends anyway (a genuinely
    repeated identical event); nothing is ever overwritten either way.
    """
    errs = schema.validate(row, repo_root=repo_root)
    if errs:
        raise schema.SchemaError("refusing to append invalid row:\n  - %s" % "\n  - ".join(errs))

    # B-1: a correction must target a row that EXISTS on the tape, with the same unit + event.
    if row.get("corrects"):
        existing = schema.read_tape(tape_files(records_dir))
        errs = schema.correction_errors(existing + [row])
        if errs:
            raise schema.SchemaError("refusing to append correction:\n  - %s"
                                     % "\n  - ".join(errs))

    path = tape_path(records_dir, row["ts"])
    if not force and row["row_id"] in existing_row_ids(path):
        return path, "duplicate"
    if dry_run:
        return path, "appended"
    os.makedirs(records_dir, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(schema.serialize(row) + "\n")
    return path, "appended"


def load(records_dir: str, apply_corrections: bool = True):
    """Read every monthly tape in the directory. Returns (rows, raw_count).

    `raw_count` is the honest on-disk row count (corrections included); `rows` is the
    fold-eligible set after superseded rows are dropped from the VIEW (never from disk).
    """
    files = tape_files(records_dir)
    rows = schema.read_tape(files)
    raw_count = len(rows)
    if apply_corrections:
        rows = schema.apply_corrections(rows)
    return rows, raw_count


def audit(records_dir: str, repo_root: str = None) -> list:
    """Whole-tape check: every row valid under the ONE validator, every correction well-formed.

    Read-only. Used by the tests and available to any gate that wants to re-derive rather
    than accept (WARN-5, derive-don't-hand-list).
    """
    rows = schema.read_tape(tape_files(records_dir))
    errs = []
    for r in rows:
        for e in schema.validate(r, repo_root=repo_root):
            errs.append("%s: %s" % (r.get("row_id"), e))
    errs.extend(schema.correction_errors(rows))
    return errs
