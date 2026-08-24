#!/usr/bin/env python3
"""VFX ARCHETYPE-BINDING RUN — P2 dossier curation (elrond, 2026-08-24).

Charter: agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md  (§ 4 P2 tail)
Ledger:  L-14 (P2 launched, 26 jobs, knockback excluded per F-3) · L-15 (lane proven) ·
         L-18 / L-19 (Matt-contributed whirlwind incumbent + confounds) · L-24 (lane closed, curation fired)
P1:      agentic_orchestration/research/curated/MIGRATION-vfx-archetype-vote-2026-08-23.md

METHOD
  Input      26 reference dossiers at research/vfx-p2-dossiers/dossiers/*.md (read-only; never edited).
             Grammar verified uniform before parsing: every body line is a heading, a blank, or
             `- <key>: <value>`. No continuation lines exist, so a line-grammar parse is lossless.
  Grain      CANDIDATE. One row per `## Candidate N:` block.
  Raw-first  Every parsed field is stored beside its VERBATIM source string. URLs are stored raw
             (markdown-link form preserved), extracted, and normalized — three columns, because the
             raw form is the evidence, the extracted form is the join key, and the normalized form is
             the only honest basis for cross-dossier duplicate detection (youtu.be/X and
             youtube.com/watch?v=X are the same video and must collide).
  Findings   FIRST-CLASS ROWS, not prose. Anything that did not verify cleanly lands in
             vfx_curation_finding with status LOGGED or UNRESOLVED. Nothing is folded into a
             clean verdict (G-S5: verify, never rubber-stamp).
  Incumbent  The Matt-contributed whirlwind reference (L-19) is curated as a row with
             provenance='matt-incumbent', validation_status='VALIDATED-INCUMBENT', candidate_rank=0
             (0 = contributed out-of-band; it has no position in any dossier's ordering), and Matt's
             two confounds carried VERBATIM into readability_notes.

Transactional + idempotent (a re-run deletes and rebuilds this curation_run's rows only). Additive DDL:
no P0-a/P1 table, column, index or row is altered. Read-only on the dossiers and on every engine store.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))          # agentic_orchestration/
CUR = os.path.abspath(os.path.join(HERE, "..", "curated"))
DB = os.path.join(CUR, "corpus.db")
DOSSIER_DIR = os.path.abspath(os.path.join(HERE, "..", "vfx-p2-dossiers", "dossiers"))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "vfx-p2-dossiers", "jobs", "_manifest.tsv"))

CURATION_RUN = "vfx-p2-dossier-curation-2026-08-24"
SCHEMA_VERSION = "vfx-p2-dossier-curation-2026-08-24/P2"
VOTE_RUN = "vfx-archetype-vote-2026-08-23"
SOURCE = "codex serialized P2 dossier lane (charter § 4 P2 / ledger L-14..L-24)"
SOURCE_DATE = "2026-08-24"
BACKUP_NAME = "corpus.db.pre-vfx-p2-20260824T130336Z-backup"   # TRUE pre-state (taken pre-DDL)

REQUIRED_FIELDS = [
    "source_game", "skill_or_mtx_name", "primary_url", "secondary_urls",
    "media_type", "temporal_coverage", "why_it_fits", "readability_notes",
]
# secondary_urls is chartered-optional (a candidate may legitimately have exactly one source);
# its absence is a LOGGED finding, never a conformance failure.
HARD_REQUIRED = [f for f in REQUIRED_FIELDS if f != "secondary_urls"]

URL_RE = re.compile(r"https?://[^\s\)\],;]+")
MD_LINK_RE = re.compile(r"^\[(?P<label>.*?)\]\((?P<url>[^\)]+)\)\s*$")
HEAD_RE = re.compile(r"^## Candidate\s+(?P<n>\d+)\s*:\s*(?P<title>.*?)\s*$")
FIELD_RE = re.compile(r"^- (?P<k>[a-z_]+):\s?(?P<v>.*)$")
COVER_RE = re.compile(
    r"windup\s*=\s*(?P<w>[YN])\s*;\s*active\s*=\s*(?P<a>[YN])\s*;\s*impact\s*=\s*(?P<i>[YN])\s*$",
    re.IGNORECASE,
)

DDL = """
CREATE TABLE IF NOT EXISTS vfx_reference_candidate (
    curation_run        TEXT NOT NULL,
    archetype_id        TEXT NOT NULL,          -- joins vfx_archetype(archetype_id, vote_run)
    vote_run            TEXT NOT NULL,
    candidate_rank      INTEGER NOT NULL,       -- position within the source dossier as authored.
                                                -- 0 = contributed out-of-band (no dossier position).
                                                -- RANK IS AUTHORING ORDER, NOT PREFERENCE. P3 selects.
    source_game         TEXT,
    skill_or_mtx_name   TEXT,
    candidate_title_raw TEXT,                   -- verbatim '## Candidate N:' heading text
    primary_url         TEXT,                   -- extracted bare URL (join key)
    primary_url_raw     TEXT,                   -- VERBATIM field value; markdown-link form preserved
    primary_url_label   TEXT,                   -- markdown link label, when the field carried one
    primary_url_norm    TEXT,                   -- normalized dedup key (see MIGRATION § 3.3)
    secondary_urls_json TEXT,                   -- JSON array of extracted URLs (ordered as authored)
    secondary_urls_raw  TEXT,                   -- VERBATIM field value
    secondary_url_count INTEGER NOT NULL DEFAULT 0,
    media_type          TEXT,
    coverage_windup     INTEGER,                -- 1/0; NULL = flag did not parse
    coverage_active     INTEGER,
    coverage_impact     INTEGER,
    coverage_raw        TEXT,                   -- VERBATIM temporal_coverage field value
    full_lifecycle      INTEGER,                -- 1 iff windup+active+impact all Y
    why_it_fits         TEXT,
    readability_notes   TEXT,
    provenance          TEXT NOT NULL CHECK (provenance IN ('codex-p2-dossier','matt-incumbent')),
    validation_status   TEXT,                   -- NULL | 'VALIDATED-INCUMBENT' (owner-approved in field)
    dossier_path        TEXT,                   -- repo-relative; NULL for out-of-band contributions
    conformance         TEXT NOT NULL,          -- 'CONFORMING' | 'CONFORMING-WITH-FINDING'
    curated_at          TEXT NOT NULL,
    source              TEXT NOT NULL,
    source_date         TEXT NOT NULL,
    PRIMARY KEY (curation_run, archetype_id, candidate_rank),
    FOREIGN KEY (archetype_id, vote_run) REFERENCES vfx_archetype(archetype_id, vote_run)
);
CREATE INDEX IF NOT EXISTS idx_vrc_arch ON vfx_reference_candidate(archetype_id);
CREATE INDEX IF NOT EXISTS idx_vrc_norm ON vfx_reference_candidate(primary_url_norm);

CREATE TABLE IF NOT EXISTS vfx_reference_dossier (
    curation_run     TEXT NOT NULL,
    archetype_id     TEXT NOT NULL,
    vote_run         TEXT NOT NULL,
    dossier_path     TEXT NOT NULL,
    dossier_bytes    INTEGER NOT NULL,
    dossier_md5      TEXT NOT NULL,             -- pins the exact input text this curation read
    candidate_count  INTEGER NOT NULL,
    search_log_lines INTEGER NOT NULL,
    archetype_joins  INTEGER NOT NULL,          -- 1 = archetype_id resolves in vfx_archetype
    meets_min_three  INTEGER NOT NULL,          -- 1 = candidate_count >= 3 (charter § 4 P2 floor)
    conformance      TEXT NOT NULL,             -- 'CONFORMING' | 'CONFORMING-WITH-FINDING'
    finding_count    INTEGER NOT NULL DEFAULT 0,
    curated_at       TEXT NOT NULL,
    source           TEXT NOT NULL,
    source_date      TEXT NOT NULL,
    PRIMARY KEY (curation_run, archetype_id)
);

CREATE TABLE IF NOT EXISTS vfx_curation_finding (
    curation_run   TEXT NOT NULL,
    finding_id     TEXT NOT NULL,               -- stable within the run
    kind           TEXT NOT NULL,
    severity       TEXT NOT NULL CHECK (severity IN ('INFO','WARN','UNRESOLVED')),
    archetype_id   TEXT,
    candidate_rank INTEGER,
    subject        TEXT,                        -- the value the finding is about (URL, field, ...)
    detail         TEXT NOT NULL,               -- prose. Every finding states its own cause.
    status         TEXT NOT NULL,               -- 'LOGGED' | 'UNRESOLVED' (needs a downstream decision)
    raised_at      TEXT NOT NULL,
    PRIMARY KEY (curation_run, finding_id)
);
"""


def md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_url(u: str) -> str:
    """Normalized duplicate-detection key. Collapses the same-resource-different-spelling cases
    that would otherwise hide genuine cross-dossier reuse: youtu.be/X == youtube.com/watch?v=X,
    scheme, www., trailing slash, and case in the host."""
    if not u:
        return ""
    p = urlparse(u.strip())
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/")
    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        vid = parse_qs(p.query or "").get("v", [None])[0]
        if vid:
            return f"youtube:{vid}"
        if path.startswith("/embed/") or path.startswith("/shorts/"):
            return f"youtube:{path.split('/')[2]}"
    if host == "youtu.be" and path:
        return f"youtube:{path.lstrip('/')}"
    q = f"?{p.query}" if p.query else ""
    return f"{host}{path}{q}"


def split_md_field(v: str):
    """Return (bare_url, label) from a field value that may or may not be a markdown link."""
    m = MD_LINK_RE.match(v.strip())
    if m:
        return m.group("url").strip(), m.group("label").strip()
    urls = URL_RE.findall(v)
    return (urls[0] if urls else None), None


def url_wellformed(u: str):
    """Structural check only. Network truth is the conductor's oEmbed pass (L-15/L-24)."""
    if not u:
        return False, "no URL present in the field value"
    p = urlparse(u)
    if p.scheme not in ("http", "https"):
        return False, f"scheme is {p.scheme!r}, expected http/https"
    if not p.netloc or "." not in p.netloc:
        return False, f"host {p.netloc!r} is not a dotted hostname"
    if any(ch in u for ch in " \t<>[]{}|\\^`"):
        return False, "URL carries characters that are illegal unescaped"
    if u.endswith((".", ",", ";")):
        return False, "URL ends in punctuation — probable prose-bleed at extraction"
    return True, None


def parse_dossier(path: str):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    cands, cur, search_log, in_log = [], None, 0, False
    for raw in lines:
        s = raw.rstrip()
        hm = HEAD_RE.match(s)
        if hm:
            in_log = False
            cur = {"rank": int(hm.group("n")), "title": hm.group("title"), "fields": {}, "order": []}
            cands.append(cur)
            continue
        if s.startswith("## Search log"):
            in_log = True
            cur = None
            continue
        if in_log:
            if s.strip():
                search_log += 1
            continue
        fm = FIELD_RE.match(s)
        if fm and cur is not None:
            k, v = fm.group("k"), fm.group("v").strip()
            if k in cur["fields"]:
                cur.setdefault("dupe_fields", []).append(k)
            cur["fields"][k] = v
            cur["order"].append(k)
    return cands, search_log, len(text.encode("utf-8"))


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not os.path.exists(DB):
        print(f"FATAL: {DB} missing", file=sys.stderr)
        return 2

    # Backup name is PINNED, not stamped-per-run: the first backup taken is the TRUE pre-state
    # (pre-DDL). Re-running the curation must not shadow it with a post-DDL copy.
    backup = os.path.join(CUR, BACKUP_NAME)
    if not os.path.exists(backup):
        con0 = sqlite3.connect(DB)
        con0.execute("pragma wal_checkpoint(TRUNCATE)")
        con0.close()
        shutil.copy2(DB, backup)
        with open(backup + ".md5.txt", "w") as fh:
            fh.write(md5(backup) + "  " + os.path.basename(backup) + "\n")
    print(f"[backup] {os.path.basename(backup)}  md5={md5(backup)}")

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(DDL)

    known = {r["archetype_id"] for r in con.execute(
        "select archetype_id from vfx_archetype where vote_run = ?", (VOTE_RUN,))}
    print(f"[join] vfx_archetype rows for {VOTE_RUN}: {len(known)}")

    findings, fid = [], [0]

    def finding(kind, severity, detail, archetype_id=None, rank=None, subject=None, status=None):
        fid[0] += 1
        findings.append({
            "finding_id": f"F{fid[0]:03d}", "kind": kind, "severity": severity,
            "archetype_id": archetype_id, "candidate_rank": rank, "subject": subject,
            "detail": detail, "status": status or ("UNRESOLVED" if severity == "UNRESOLVED" else "LOGGED"),
        })

    # ---- manifest cross-check (what the lane was ASKED for vs what is on disk) ----
    manifest_ids = []
    if os.path.exists(MANIFEST):
        for line in open(MANIFEST, encoding="utf-8"):
            if line.strip():
                manifest_ids.append(line.split("\t")[0].strip())
    on_disk = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(DOSSIER_DIR, "*.md")))
    for a in sorted(set(manifest_ids) - set(on_disk)):
        finding("manifest-gap", "UNRESOLVED", f"manifest requested archetype {a!r} but no dossier exists on disk",
                archetype_id=a, subject=a)
    for a in sorted(set(on_disk) - set(manifest_ids)):
        finding("unmanifested-dossier", "WARN", f"dossier {a}.md exists but the manifest never requested it",
                archetype_id=a, subject=a)
    for a in sorted(known - set(on_disk)):
        finding("archetype-uncovered", "INFO",
                f"archetype {a!r} carries zero reference candidates after this curation "
                f"(expected for 'knockback' per charter F-3 / ledger L-14; unexpected otherwise)",
                archetype_id=a, subject=a)

    cand_rows, dossier_rows = [], []
    norm_index = {}          # normalized primary URL -> [(archetype, rank)]
    all_urls_index = {}      # normalized ANY url -> set(archetype)

    for path in sorted(glob.glob(os.path.join(DOSSIER_DIR, "*.md"))):
        arche = os.path.basename(path)[:-3]
        rel = os.path.relpath(path, ROOT)
        cands, log_lines, nbytes = parse_dossier(path)
        joins = 1 if arche in known else 0
        if not joins:
            finding("archetype-join-fail", "UNRESOLVED",
                    f"dossier filename {arche!r} does not resolve to a vfx_archetype row under vote_run "
                    f"{VOTE_RUN!r}; candidate rows are curated with a dangling archetype_id",
                    archetype_id=arche, subject=arche)
        if len(cands) < 3:
            finding("short-dossier", "WARN",
                    f"dossier carries {len(cands)} candidates; charter § 4 P2 floor is >= 3. "
                    f"Curated as-is (a short dossier is a finding, not a failure)",
                    archetype_id=arche, subject=f"{len(cands)} candidates")
        if log_lines == 0:
            finding("no-search-log", "WARN", "dossier carries no '## Search log' content — dead ends unrecorded",
                    archetype_id=arche)
        seen_ranks, d_findings = set(), 0
        before = len(findings)

        for c in cands:
            f, rank = c["fields"], c["rank"]
            if rank in seen_ranks:
                finding("duplicate-rank", "UNRESOLVED",
                        f"two candidate blocks both numbered {rank}; the second is curated at rank "
                        f"{max(seen_ranks) + 1} to keep the key unique",
                        archetype_id=arche, rank=rank)
                rank = max(seen_ranks) + 1
            seen_ranks.add(rank)
            for dk in c.get("dupe_fields", []):
                finding("duplicate-field", "WARN",
                        f"field {dk!r} appears more than once in the block; last value curated",
                        archetype_id=arche, rank=rank, subject=dk)

            missing = [k for k in HARD_REQUIRED if not f.get(k)]
            if missing:
                finding("missing-required-field", "UNRESOLVED",
                        f"required field(s) absent or empty: {', '.join(missing)}",
                        archetype_id=arche, rank=rank, subject=",".join(missing))
            if "secondary_urls" not in f or not f.get("secondary_urls"):
                finding("no-secondary-urls", "INFO",
                        "candidate carries no secondary_urls — single-source reference; corroboration "
                        "rests entirely on the primary URL",
                        archetype_id=arche, rank=rank)

            praw = f.get("primary_url", "")
            purl, plabel = split_md_field(praw) if praw else (None, None)
            ok, why = url_wellformed(purl)
            if not ok:
                finding("malformed-primary-url", "UNRESOLVED",
                        f"primary_url did not verify structurally: {why}. Raw value: {praw!r}",
                        archetype_id=arche, rank=rank, subject=praw)

            sraw = f.get("secondary_urls", "")
            surls = URL_RE.findall(sraw) if sraw else []
            for su in surls:
                ok2, why2 = url_wellformed(su)
                if not ok2:
                    finding("malformed-secondary-url", "WARN",
                            f"secondary URL did not verify structurally: {why2}",
                            archetype_id=arche, rank=rank, subject=su)

            craw = f.get("temporal_coverage", "")
            cm = COVER_RE.search(craw) if craw else None
            if cm:
                w, a, i = (cm.group("w").upper() == "Y", cm.group("a").upper() == "Y",
                           cm.group("i").upper() == "Y")
                cw, ca, ci = int(w), int(a), int(i)
                full = int(w and a and i)
                if not (w or a or i):
                    finding("zero-coverage", "WARN",
                            "all three temporal flags are N — the reference documents no phase of the "
                            "effect; low value to P3 frame-set selection",
                            archetype_id=arche, rank=rank, subject=craw)
            else:
                cw = ca = ci = full = None
                finding("unparseable-coverage", "UNRESOLVED",
                        f"temporal_coverage did not match the chartered grammar "
                        f"'windup=Y/N; active=Y/N; impact=Y/N'. Raw value: {craw!r}",
                        archetype_id=arche, rank=rank, subject=craw)

            mt = (f.get("media_type") or "").strip().lower()
            if mt and mt != "video":
                finding("non-video-media", "INFO",
                        f"media_type is {mt!r}; charter § 4 P2 prefers video over stills. Retained — "
                        f"P3 weighs it, curation does not drop it",
                        archetype_id=arche, rank=rank, subject=mt)

            nurl = norm_url(purl or "")
            norm_index.setdefault(nurl, []).append((arche, rank)) if nurl else None
            for u in ([purl] if purl else []) + surls:
                nu = norm_url(u)
                if nu:
                    all_urls_index.setdefault(nu, set()).add(arche)

            cand_rows.append((
                CURATION_RUN, arche, VOTE_RUN, rank,
                f.get("source_game"), f.get("skill_or_mtx_name"), c["title"],
                purl, praw or None, plabel, nurl or None,
                json.dumps(surls, ensure_ascii=False), sraw or None, len(surls),
                f.get("media_type"), cw, ca, ci, craw or None, full,
                f.get("why_it_fits"), f.get("readability_notes"),
                "codex-p2-dossier", None, rel,
                "PENDING", now, SOURCE, SOURCE_DATE,
            ))
            d_findings += 0

        d_findings = len(findings) - before
        dossier_rows.append((
            CURATION_RUN, arche, VOTE_RUN, rel, nbytes, md5(path), len(cands), log_lines,
            joins, int(len(cands) >= 3),
            "CONFORMING" if d_findings == 0 else "CONFORMING-WITH-FINDING",
            d_findings, now, SOURCE, SOURCE_DATE,
        ))

    # ---- Matt-contributed incumbent (ledger L-18 / L-19) ----
    inc_url = "https://www.youtube.com/watch?v=KaMPoPywM40"
    inc_notes = (
        "Matt-named confounds, carried verbatim from ledger L-19: (i) added cyclones/tornadoes are "
        "Dust-Devil-era BUILD modifications, not base-skill VFX; (ii) cosmetic wings occlude VFX "
        "readability. VALIDATED-INCUMBENT: Matt has produced owner-approved Godot scene work from "
        "this reference (L-18)."
    )
    cand_rows.append((
        CURATION_RUN, "whirlwind", VOTE_RUN, 0,
        "Diablo IV (Season 14)", "Whirlwind Barbarian (base skill; S14 build footage)",
        "Whirlwind Barbarian (base skill; S14 build footage) [Matt-contributed incumbent]",
        inc_url, inc_url, None, norm_url(inc_url),
        json.dumps([], ensure_ascii=False), None, 0,
        "video", None, None, None, None, None,
        "Matt's working reference for the EoR-Warlord Godot scene: described verbally to the scene "
        "team and the resulting work was owner-approved. The § 3.2 selection criterion measured in "
        "the field — describable therefore readable, buildable-from-description therefore "
        "parameterizable, owner eye signed the output (ledger L-18).",
        inc_notes,
        "matt-incumbent", "VALIDATED-INCUMBENT", None,
        "PENDING", now, "Matt (live word, 2026-08-23) — ledger L-18 / L-19; oEmbed-verified by conductor",
        "2026-08-23",
    ))
    norm_index.setdefault(norm_url(inc_url), []).append(("whirlwind", 0))
    all_urls_index.setdefault(norm_url(inc_url), set()).add("whirlwind")
    finding("incumbent-coverage-unrated", "INFO",
            "the Matt-contributed incumbent carries NULL temporal coverage flags: the reference was "
            "contributed as a working referent, not phase-rated by the dossier lane. P3 rates it or "
            "leaves it unrated — curation does not invent flags",
            archetype_id="whirlwind", rank=0, subject=inc_url)

    # ---- cross-dossier duplicate detection ----
    for nurl, holders in sorted(norm_index.items()):
        arches = {a for a, _ in holders}
        if len(holders) > 1 and len(arches) > 1:
            finding("cross-archetype-primary-reuse", "WARN",
                    "the same primary reference is claimed by more than one archetype: "
                    + "; ".join(f"{a}#{r}" for a, r in holders)
                    + ". Not necessarily an error — one clip can legitimately demonstrate two "
                      "archetypes — but P3 must not select it for both without saying why",
                    subject=nurl)
        elif len(holders) > 1:
            finding("intra-dossier-primary-duplicate", "UNRESOLVED",
                    "the same primary reference appears on two candidates in ONE dossier: "
                    + "; ".join(f"{a}#{r}" for a, r in holders)
                    + " — the dossier's candidate count overstates its distinct-source count",
                    archetype_id=holders[0][0], subject=nurl)
    for nurl, arches in sorted(all_urls_index.items()):
        if len(arches) > 1 and nurl not in {n for n, h in norm_index.items()
                                            if len({a for a, _ in h}) > 1}:
            finding("cross-archetype-url-reuse", "INFO",
                    "URL appears (as primary or secondary) under multiple archetypes: "
                    + ", ".join(sorted(arches)),
                    subject=nurl)

    # ---- stamp per-candidate conformance from the findings actually raised ----
    flagged = {(f["archetype_id"], f["candidate_rank"]) for f in findings
               if f["candidate_rank"] is not None and f["severity"] in ("WARN", "UNRESOLVED")}
    cand_rows = [
        r[:25] + (("CONFORMING-WITH-FINDING" if (r[1], r[3]) in flagged else "CONFORMING"),) + r[26:]
        for r in cand_rows
    ]

    with con:
        con.execute("delete from vfx_reference_candidate where curation_run = ?", (CURATION_RUN,))
        con.execute("delete from vfx_reference_dossier  where curation_run = ?", (CURATION_RUN,))
        con.execute("delete from vfx_curation_finding   where curation_run = ?", (CURATION_RUN,))
        con.executemany(
            "insert into vfx_reference_candidate values (" + ",".join(["?"] * 29) + ")", cand_rows)
        con.executemany(
            "insert into vfx_reference_dossier values (" + ",".join(["?"] * 15) + ")", dossier_rows)
        con.executemany(
            "insert into vfx_curation_finding values (?,?,?,?,?,?,?,?,?,?)",
            [(CURATION_RUN, f["finding_id"], f["kind"], f["severity"], f["archetype_id"],
              f["candidate_rank"], f["subject"], f["detail"], f["status"], now) for f in findings])

    ic = con.execute("pragma integrity_check").fetchone()[0]
    fk = con.execute("pragma foreign_key_check").fetchall()
    print(f"[db] integrity_check={ic}  foreign_key_check_violations={len(fk)}")
    print(f"[rows] candidates={len(cand_rows)}  dossiers={len(dossier_rows)}  findings={len(findings)}")

    print("\n--- coverage statistics (P3 input) ---")
    for r in con.execute("""
        select
          count(*) as candidates,
          sum(full_lifecycle = 1) as full_lifecycle,
          sum(coverage_windup = 1) as windup,
          sum(coverage_active = 1) as active,
          sum(coverage_impact = 1) as impact,
          sum(coverage_windup is null) as unrated
        from vfx_reference_candidate where curation_run = ?""", (CURATION_RUN,)):
        print(dict(r))
    print("archetypes with >=1 full-lifecycle video candidate:",
          con.execute("""select count(distinct archetype_id) from vfx_reference_candidate
                         where curation_run = ? and full_lifecycle = 1
                           and lower(media_type) = 'video'""", (CURATION_RUN,)).fetchone()[0])

    print("\n--- findings by severity ---")
    for r in con.execute("""select severity, count(*) n from vfx_curation_finding
                            where curation_run = ? group by 1 order by 1""", (CURATION_RUN,)):
        print(f"  {r['severity']:<11} {r['n']}")
    print("--- findings by kind ---")
    for r in con.execute("""select kind, severity, count(*) n from vfx_curation_finding
                            where curation_run = ? group by 1,2 order by 3 desc""", (CURATION_RUN,)):
        print(f"  {r['kind']:<32} {r['severity']:<11} {r['n']}")

    print("\n--- source_game distribution ---")
    for r in con.execute("""select source_game, count(*) n from vfx_reference_candidate
                            where curation_run = ? group by 1 order by 2 desc, 1""", (CURATION_RUN,)):
        print(f"  {r['source_game']:<30} {r['n']}")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
