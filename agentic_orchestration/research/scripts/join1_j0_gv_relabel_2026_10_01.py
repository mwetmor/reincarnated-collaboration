#!/usr/bin/env python3
"""JOIN-1 J0 GV remedy (elrond, 2026-10-01): FoI edition-pin restore + fidelity_grade MEASURED -> DATAMINED.

Finding:  agentic_orchestration/qa/findings/2026-10-01-join1-j0-gv-exact-skill-grading.md (jack-ryan,
          collab 795334bea, KC2-PLAY ledger KP-159). Approved under ADR-002 as a within-seam DATA-ONLY
          correction: no DDL, and nothing reads fidelity_grade.
Row list: ...gv-exact-skill-grading.rows.json (FILE sha256 96a483ea96894cde33e476770193793b634b006e6ea3f0e4f1c6731a083929c5,
          checked at run time; the run refuses if the sidecar's bytes differ).
MIGRATION: research/curated/MIGRATION-join1-j0-gv-relabel-2026-10-01.md (forward addendum closing
          MIGRATION-devotion-payloads-2026-07-25.md section 7).

Step 1  restore exact_skill.source_version on gd-flames-of-ignaffar-purifier. The value is DERIVED from
        MIGRATION-gd-edition-pin-2026-07-24.md line 30 (read from the file, never retyped), then checked:
        its arz_sha256 must equal (a) the devotion banker's own gdx1 pin and (b) the sha256 of the GDX1.arz
        bytes on disk under ~/depots/642280/24346246/.
Step 2  fidelity_grade MEASURED -> DATAMINED where fidelity_basis='primary-source-datamine', in exact_skill
        (675), devotion_power (65), devotion_constellation (110) = 850. The UPDATE's row set must equal
        the sidecar's row list exactly, table by table, or the run aborts before writing.
Step 3  assert: MEASURED = 0 and DATAMINED = 675/65/110 on those tables; row counts unchanged; every other
        column of the three tables unchanged; exact_skill_field untouched (7,250, content hash);
        integrity_check ok. Add one corpus_schema_meta row.

Modes: --mode dry-run (default; in-memory copy, zero bytes written) | --mode apply (refuses while free disk
       < 40 GiB, the JOIN-1 charter section 6 HALT boundary; writes a file backup first).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                         # agentic_orchestration/research
AO = ROOT.parent                                                   # agentic_orchestration
DB = ROOT / "curated" / "corpus.db"
PIN_DOC = ROOT / "curated" / "MIGRATION-gd-edition-pin-2026-07-24.md"
PIN_LINE = 30
SIDECAR = AO / "qa" / "findings" / "2026-10-01-join1-j0-gv-exact-skill-grading.rows.json"
SIDECAR_SHA = "96a483ea96894cde33e476770193793b634b006e6ea3f0e4f1c6731a083929c5"
GDX1_ON_DISK = Path("/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz")
FOI = "gd-flames-of-ignaffar-purifier"
VERSION = "join1-j0-gv-relabel-2026-10-01"
HALT_FREE_GIB = 40.0
TABLES = {"exact_skill": ("entity_id", 675), "devotion_power": ("power_record", 65),
          "devotion_constellation": ("constellation_record", 110)}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def derive_pin() -> str:
    line = PIN_DOC.read_text().splitlines()[PIN_LINE - 1].strip()
    m = re.fullmatch(r"gd-edition-[A-Z]+-\d{8}; depot=\d+\([^)]+\); manifest=\d+; arz_sha256=([0-9a-f]{64})", line)
    if not m:
        raise SystemExit(f"ABORT: {PIN_DOC.name}:{PIN_LINE} is not a composite edition pin: {line!r}")
    return line


def check_pin(pin: str) -> dict:
    sha_in_pin = pin.rsplit("arz_sha256=", 1)[1]
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    src = (Path(__file__).resolve().parent / "gd_devotion_bank_2026_07_25.py").read_text()
    m = re.search(r'"gdx1/database/GDX1\.arz": dict\(.*?sha256="([0-9a-f]{64})"', src, re.S)
    banker_sha = m.group(1) if m else None
    disk_sha = sha256_file(GDX1_ON_DISK) if GDX1_ON_DISK.exists() else None
    ok = sha_in_pin == banker_sha == disk_sha
    if not ok:
        raise SystemExit(f"ABORT: pin sha {sha_in_pin} / banker sha {banker_sha} / disk sha {disk_sha} disagree")
    return {"pin_sha": sha_in_pin, "banker_sha_equal": True, "disk_sha_equal": True, "disk_path": str(GDX1_ON_DISK)}


def sidecar_sets() -> dict:
    if sha256_file(SIDECAR) != SIDECAR_SHA:
        raise SystemExit("ABORT: GV sidecar bytes differ from the recorded FILE sha256")
    d = json.loads(SIDECAR.read_text())
    sets = {"exact_skill": {r["entity_id"] for r in d["rows"]}}
    for r in d["adjacent_population"]["rows"]:
        sets.setdefault(r["table"], set()).add(r["id"])
    return sets


def table_hash(con, sql):
    h = hashlib.sha256()
    for row in con.execute(sql):
        h.update(repr(row).encode())
    return h.hexdigest()


def other_cols_hash(con, table):
    cols = [r[1] for r in con.execute(f"PRAGMA table_info({table})")]
    keep = [c for c in cols if c != "fidelity_grade" and not (table == "exact_skill" and c == "source_version")]
    return table_hash(con, f"SELECT {', '.join(keep)} FROM {table} ORDER BY {TABLES[table][0]}")


def remedy(con, pin, sets, applied_utc):
    cur = con.cursor()
    pre = {"counts": {t: cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in TABLES},
           "other": {t: other_cols_hash(con, t) for t in TABLES},
           "esf": table_hash(con, "SELECT * FROM exact_skill_field ORDER BY entity_id, canon_key, rank"),
           "esf_n": cur.execute("SELECT count(*) FROM exact_skill_field").fetchone()[0],
           "srcver_others": table_hash(con, f"SELECT entity_id, source_version FROM exact_skill WHERE entity_id<>'{FOI}' ORDER BY 1")}
    foi = cur.execute("SELECT source_version FROM exact_skill WHERE entity_id=?", (FOI,)).fetchone()
    if foi is None or foi[0] is not None:
        raise SystemExit(f"ABORT: FoI source_version is {foi!r}; expected an existing row with NULL")
    for t, (key, n) in TABLES.items():
        target = {r[0] for r in cur.execute(
            f"SELECT {key} FROM {t} WHERE fidelity_grade='MEASURED' AND fidelity_basis='primary-source-datamine'")}
        if target != sets[t] or len(target) != n:
            raise SystemExit(f"ABORT: {t}: UPDATE set ({len(target)}) != sidecar set ({len(sets[t])}) or != {n}")
    cur.execute("BEGIN")
    cur.execute("UPDATE exact_skill SET source_version=? WHERE entity_id=? AND source_version IS NULL", (pin, FOI))
    assert cur.rowcount == 1
    changed = {}
    for t in TABLES:
        cur.execute(f"UPDATE {t} SET fidelity_grade='DATAMINED' "
                    f"WHERE fidelity_grade='MEASURED' AND fidelity_basis='primary-source-datamine'")
        changed[t] = cur.rowcount
    cur.execute("INSERT INTO corpus_schema_meta(version, applied_utc, note) VALUES (?,?,?)", (
        VERSION, applied_utc,
        "GV remedy (elrond; jack-ryan finding 2026-10-01 collab 795334bea, KP-159; ADR-002 within-seam, DATA-ONLY, no DDL). "
        f"(1) exact_skill.source_version restored on {FOI} from MIGRATION-gd-edition-pin-2026-07-24.md:30 (derived, not retyped; "
        "arz_sha256 checked equal to the devotion banker's gdx1 pin and to the GDX1.arz bytes at ~/depots/642280/24346246). "
        "(2) fidelity_grade MEASURED -> DATAMINED where fidelity_basis='primary-source-datamine': exact_skill 675, devotion_power 65, "
        "devotion_constellation 110 (= 850; row sets equal to the GV sidecar, FILE sha256 96a483ea...). Closes "
        "MIGRATION-devotion-payloads-2026-07-25.md section 7 (answered by LAW section 4, 557394ec5; back-filled here)."))
    con.commit()
    return pre, changed


def audit(con, pre, changed, pin):
    cur = con.cursor()
    out = {"rows_changed": changed}
    for t in TABLES:
        out[f"{t}_grades"] = cur.execute(f"SELECT fidelity_grade, count(*) FROM {t} GROUP BY 1 ORDER BY 1").fetchall()
        out[f"{t}_count_unchanged"] = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0] == pre["counts"][t]
        out[f"{t}_other_columns_unchanged"] = other_cols_hash(con, t) == pre["other"][t]
    out["measured_remaining"] = sum(cur.execute(f"SELECT count(*) FROM {t} WHERE fidelity_grade='MEASURED'").fetchone()[0] for t in TABLES)
    out["foi_source_version_equals_pin"] = cur.execute(
        "SELECT source_version FROM exact_skill WHERE entity_id=?", (FOI,)).fetchone()[0] == pin
    out["other_source_versions_unchanged"] = table_hash(
        con, f"SELECT entity_id, source_version FROM exact_skill WHERE entity_id<>'{FOI}' ORDER BY 1") == pre["srcver_others"]
    out["null_source_version_rows"] = cur.execute("SELECT count(*) FROM exact_skill WHERE source_version IS NULL").fetchone()[0]
    out["exact_skill_field_untouched"] = (table_hash(con, "SELECT * FROM exact_skill_field ORDER BY entity_id, canon_key, rank") == pre["esf"]
                                          and cur.execute("SELECT count(*) FROM exact_skill_field").fetchone()[0] == pre["esf_n"] == 7250)
    out["integrity"] = cur.execute("PRAGMA integrity_check").fetchone()[0]
    ok = (changed == {t: n for t, (_, n) in TABLES.items()} and out["measured_remaining"] == 0
          and all(out[f"{t}_count_unchanged"] and out[f"{t}_other_columns_unchanged"] for t in TABLES)
          and out["foi_source_version_equals_pin"] and out["other_source_versions_unchanged"]
          and out["null_source_version_rows"] == 0 and out["exact_skill_field_untouched"] and out["integrity"] == "ok")
    return out, ok


def run(con, applied_utc):
    pin = derive_pin()
    print(f"pin (derived from {PIN_DOC.name}:{PIN_LINE}): {pin}")
    print(f"pin checks: {check_pin(pin)}")
    sets = sidecar_sets()
    pre, changed = remedy(con, pin, sets, applied_utc)
    return audit(con, pre, changed, pin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    a = ap.parse_args()
    applied_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"corpus.db FILE sha256 (before): {sha256_file(DB)}")
    if a.mode == "dry-run":
        src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        con = sqlite3.connect(":memory:", isolation_level=None)
        src.backup(con)
        src.close()
        out, ok = run(con, applied_utc)
        print("MODE: dry-run (in memory; zero bytes written)")
    else:
        st = os.statvfs(DB.parent)
        g = st.f_bavail * st.f_frsize / (1024 ** 3)
        print(f"free disk: {g:.2f} GiB")
        if g < HALT_FREE_GIB:
            raise SystemExit(f"REFUSED: free disk {g:.2f} GiB < {HALT_FREE_GIB} GiB (JOIN-1 charter section 6 HALT boundary)")
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        bak = DB.with_name(f"corpus.db.pre-gv-relabel-{stamp}-backup")
        shutil.copy2(DB, bak)
        print(f"backup: {bak.name} FILE sha256 {sha256_file(bak)}")
        con = sqlite3.connect(DB, isolation_level=None)
        out, ok = run(con, applied_utc)
        con.close()
        print(f"corpus.db FILE sha256 (after): {sha256_file(DB)}")
    for k, v in out.items():
        print(f"{k}: {v}")
    print("VERDICT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
