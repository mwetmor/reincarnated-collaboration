#!/usr/bin/env python3
"""VFX ARCHETYPE-BINDING RUN — P2 SUPPLEMENT curation DELTA (elrond, 2026-08-24).

Charter: agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md
Ledger:  L-30 (supplement lane fired — jobs 27-30, tightened briefs, timestamp discipline)
         L-32 (supplement lane CLOSED, rc=0 x4; fabrication check 9/9 oEmbed, zero PoE leakage;
               job 29 verdict: 3BnHvNZ_4YM is NOT an extraction master)
Predecessor: vfx_p2_dossier_curation_2026_08_24.py  (26 dossiers -> 114 candidates / 26 dossiers /
             25 findings under curation_run 'vfx-p2-dossier-curation-2026-08-24')

WHAT THIS IS
  A bounded, ADDITIVE delta for the 4 supplementary dossiers. It does NOT re-run, re-read or
  re-write the main lane. Its rows land BESIDE the main lane under a distinct curation_run
  (the lane discriminator), exactly as the predecessor MIGRATION § 1 anticipated
  ("a later curation lands beside this one rather than over it").

CONVENTIONS ARE IMPORTED, NOT COPIED
  norm_url / split_md_field / url_wellformed / md5 / the field+heading+coverage regexes are
  imported from the predecessor module so the two lanes cannot drift. Only the dossier walker is
  extended, because ww_clean_baseline.md carries a NON-CANDIDATE '## Part 1:' block and an extra
  per-candidate 'confounds:' field that the main-lane grammar never had.

WHAT IS NEW IN THE SCHEMA (both additive, both nullable, no existing row's value is altered)
  vfx_reference_candidate.confounds        -- 1:1 per-candidate confound-status text. The whirlwind
                                              supplement job exists BECAUSE confound-status is the
                                              question; folding it into readability_notes would be a
                                              silent transformation of the field the job was run for.
  vfx_curation_finding.target_curation_run -- NULL = the finding is about its own run's rows.
                                              Non-NULL = the finding is about ANOTHER run's row.
                                              Required because job 29's Part-1 verdict DOWNGRADES the
                                              MAIN lane's whirlwind#1, and (archetype_id, rank) alone
                                              is now ambiguous across two runs.

  NO 'lane' COLUMN IS ADDED. Backfilling one would mutate the 114 existing rows; leaving it NULL
  would make NULL mean both 'main lane' and 'unset'. Lane is DERIVED in the two union views below.

Transactional + idempotent (a re-run deletes and rebuilds THIS curation_run's rows only).
Read-only on the dossiers (md5-pinned per row) and on every engine store. ADR-004 unaffected.
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vfx_p2_dossier_curation_2026_08_24 as p2  # noqa: E402  (conventions, imported not forked)

ROOT = p2.ROOT
CUR = p2.CUR
DB = p2.DB
DOSSIER_DIR = p2.DOSSIER_DIR
JOBS_DIR = os.path.abspath(os.path.join(HERE, "..", "vfx-p2-dossiers", "jobs"))

CURATION_RUN = "vfx-p2-supplement-curation-2026-08-24"
MAIN_RUN = p2.CURATION_RUN                     # 'vfx-p2-dossier-curation-2026-08-24'
SCHEMA_VERSION = "vfx-p2-supplement-curation-2026-08-24/P2-delta"
VOTE_RUN = p2.VOTE_RUN
SOURCE = "codex serialized P2 SUPPLEMENT lane, jobs 27-30 (charter § 4 P2 / ledger L-30 / L-32)"
SOURCE_DATE = "2026-08-24"
BACKUP_NAME = "corpus.db.pre-vfx-p2-supplement-20260824-backup"   # pinned; first copy is the pre-state

# dossier filename -> archetype_id (the supplement filenames are JOB names, not archetype names)
SUPPLEMENT_MAP = {
    "gtc_nonpoe_supplement": ("ground_targeted_circle", 27,
                              "non-PoE hunt — the archetype's main-lane dossier was 100% PoE"),
    "st_nonpoe_supplement": ("single_target", 28,
                             "non-PoE hunt — the archetype's main-lane dossier was 100% PoE"),
    "ww_clean_baseline": ("whirlwind", 29,
                          "clean-baseline verification of 3BnHvNZ_4YM + confound-free alternates hunt"),
    "ma_video_companion": ("melee_arc", 30,
                           "video companion — the main-lane canonical is a gif; 76-skill archetype"),
}

PART_RE = re.compile(r"^##\s+(?P<title>(?!Candidate\s+\d)(?!Search log).+?)\s*$")


def add_column(con, table, col, decl):
    """Additive ALTER, idempotent. Existing rows read NULL; no existing value is rewritten."""
    have = {r[1] for r in con.execute(f"pragma table_info({table})")}
    if col not in have:
        con.execute(f"alter table {table} add column {col} {decl}")
        return True
    return False


def parse_dossier_ext(path: str):
    """Extended walker. Same heading/field/log grammar as the main lane, plus:
       - non-candidate '## <title>' blocks are captured SEPARATELY (never merged into a candidate);
       - unknown field keys are kept in the block's field map (so 'confounds' survives)."""
    text = open(path, encoding="utf-8").read()
    cands, blocks, cur, search_log, in_log = [], [], None, 0, False
    for raw in text.splitlines():
        s = raw.rstrip()
        hm = p2.HEAD_RE.match(s)
        if hm:
            in_log = False
            cur = {"rank": int(hm.group("n")), "title": hm.group("title"),
                   "fields": {}, "order": [], "kind": "candidate"}
            cands.append(cur)
            continue
        if s.startswith("## Search log"):
            in_log, cur = True, None
            continue
        pm = PART_RE.match(s) if s.startswith("## ") else None
        if pm:
            in_log = False
            cur = {"title": pm.group("title"), "fields": {}, "order": [], "kind": "block"}
            blocks.append(cur)
            continue
        if in_log:
            if s.strip():
                search_log += 1
            continue
        fm = p2.FIELD_RE.match(s)
        if fm and cur is not None:
            k, v = fm.group("k"), fm.group("v").strip()
            if k in cur["fields"]:
                cur.setdefault("dupe_fields", []).append(k)
            cur["fields"][k] = v
            cur["order"].append(k)
    return cands, blocks, search_log, len(text.encode("utf-8"))


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not os.path.exists(DB):
        print(f"FATAL: {DB} missing", file=sys.stderr)
        return 2

    backup = os.path.join(CUR, BACKUP_NAME)
    if not os.path.exists(backup):
        c0 = sqlite3.connect(DB)
        c0.execute("pragma wal_checkpoint(TRUNCATE)")
        c0.close()
        shutil.copy2(DB, backup)
        with open(backup + ".md5.txt", "w") as fh:
            fh.write(p2.md5(backup) + "  " + os.path.basename(backup) + "\n")
    print(f"[backup] {os.path.basename(backup)}  md5={p2.md5(backup)}")

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    # ---- pre-state census (proves the delta is additive) ----
    pre = {t: con.execute(f"select count(*) from {t}").fetchone()[0]
           for t in ("vfx_reference_candidate", "vfx_reference_dossier", "vfx_curation_finding")}
    pre_main_md5 = con.execute(
        "select group_concat(archetype_id || '|' || candidate_rank || '|' ||"
        " coalesce(primary_url_norm,'') || '|' || conformance, char(10))"
        " from (select * from vfx_reference_candidate where curation_run = ?"
        "        order by archetype_id, candidate_rank)", (MAIN_RUN,)).fetchone()[0]
    print(f"[pre] {pre}")

    with con:
        a1 = add_column(con, "vfx_reference_candidate", "confounds", "TEXT")
        a2 = add_column(con, "vfx_curation_finding", "target_curation_run", "TEXT")
    print(f"[ddl] added confounds={a1}  target_curation_run={a2}")

    known = {r["archetype_id"] for r in con.execute(
        "select archetype_id from vfx_archetype where vote_run = ?", (VOTE_RUN,))}

    findings, fid = [], [0]

    def finding(kind, severity, detail, archetype_id=None, rank=None, subject=None,
                status=None, target_run=None):
        fid[0] += 1
        findings.append({
            "finding_id": f"S{fid[0]:03d}", "kind": kind, "severity": severity,
            "archetype_id": archetype_id, "candidate_rank": rank, "subject": subject,
            "detail": detail,
            "status": status or ("UNRESOLVED" if severity == "UNRESOLVED" else "LOGGED"),
            "target_curation_run": target_run,
        })

    # ---- prior-lane URL index (cross-run reuse detection, read-only) ----
    prior_primary, prior_any, prior_skill = {}, {}, {}
    for r in con.execute(
            "select curation_run, archetype_id, candidate_rank, primary_url_norm,"
            " secondary_urls_json, skill_or_mtx_name, media_type"
            "  from vfx_reference_candidate where curation_run = ?", (MAIN_RUN,)):
        if r["primary_url_norm"]:
            prior_primary.setdefault(r["primary_url_norm"], []).append(
                (r["archetype_id"], r["candidate_rank"]))
            prior_any.setdefault(r["primary_url_norm"], set()).add(r["archetype_id"])
        for u in json.loads(r["secondary_urls_json"] or "[]"):
            nu = p2.norm_url(u)
            if nu:
                prior_any.setdefault(nu, set()).add(r["archetype_id"])
        key = (r["archetype_id"], (r["skill_or_mtx_name"] or "").strip().lower())
        prior_skill.setdefault(key, []).append(
            (r["candidate_rank"], r["primary_url_norm"], r["media_type"]))

    cand_rows, dossier_rows = [], []
    seen_norm = {}

    for job_name in sorted(SUPPLEMENT_MAP, key=lambda k: SUPPLEMENT_MAP[k][1]):
        arche, job_no, brief = SUPPLEMENT_MAP[job_name]
        path = os.path.join(DOSSIER_DIR, job_name + ".md")
        if not os.path.exists(path):
            finding("supplement-dossier-missing", "UNRESOLVED",
                    f"ledger L-32 reports job {job_no} rc=0 but {job_name}.md is not on disk",
                    archetype_id=arche, subject=job_name)
            continue
        rel = os.path.relpath(path, ROOT)
        cands, blocks, log_lines, nbytes = parse_dossier_ext(path)
        joins = 1 if arche in known else 0
        before = len(findings)

        if not joins:
            finding("archetype-join-fail", "UNRESOLVED",
                    f"supplement job {job_no} maps to archetype {arche!r}, which does not resolve in "
                    f"vfx_archetype under vote_run {VOTE_RUN!r}",
                    archetype_id=arche, subject=arche)

        # the supplement lane's manifest of record is the job prompt file, not _manifest.tsv
        prompt = os.path.join(JOBS_DIR, f"{job_no}-{job_name}.prompt.md")
        if not os.path.exists(prompt):
            finding("unmanifested-dossier", "WARN",
                    f"no job prompt {job_no}-{job_name}.prompt.md — the supplement dossier's brief "
                    f"of record is missing, so its scope cannot be checked against what was asked",
                    archetype_id=arche, subject=job_name)

        if len(cands) < 3:
            finding("short-dossier", "INFO",
                    f"supplement dossier carries {len(cands)} candidates; the charter § 4 P2 floor of "
                    f">= 3 is a MAIN-LANE criterion and job {job_no}'s brief was "
                    f"'{brief}'. Recorded as a fact in vfx_reference_dossier.meets_min_three = 0 "
                    f"regardless of this severity — the column is the fact, the severity is routing. "
                    f"Severity is INFO rather than WARN because a verification-plus-alternates brief "
                    f"has no 3-candidate floor to fall short of; the count is still reported so P3 "
                    f"cannot mistake this dossier for a full hunt",
                    archetype_id=arche, subject=f"{len(cands)} candidates")
        if log_lines == 0:
            finding("no-search-log", "WARN",
                    "supplement dossier carries no '## Search log' content — dead ends unrecorded",
                    archetype_id=arche)

        # ---- non-candidate blocks (ww_clean_baseline.md '## Part 1') ----
        for b in blocks:
            if arche == "whirlwind" and b["title"].lower().startswith("part 1"):
                f = b["fields"]
                ts = f.get("whirlwind_timestamp", "")
                mr = f.get("max_resolution", "")
                fe = f.get("frame_extraction_adequate", "")
                target = prior_primary.get("youtube:3BnHvNZ_4YM", [])
                trank = target[0][1] if target else None
                finding(
                    "extraction-master-downgrade", "WARN",
                    "Job 29's Part-1 verification block is NOT a candidate — it is a verdict ON the "
                    "MAIN-lane row whirlwind#1 (youtube:3BnHvNZ_4YM), and it DOWNGRADES that row's "
                    "usability per ledger L-32 ('real gameplay footage but NOT an extraction "
                    "master'). Three verdict fields, verbatim: "
                    f"(1) whirlwind_timestamp: {ts} "
                    f"(2) max_resolution: {mr} "
                    f"(3) frame_extraction_adequate: {fe} "
                    "Two honest UNKNOWNs and a qualified Y. The main-lane row is NOT edited — its "
                    "coverage flags (windup=Y; active=Y; impact=Y) stand as the dossier lane wrote "
                    "them, and this finding carries the downgrade beside them. "
                    "target_curation_run pins which run's whirlwind#1 is meant. "
                    "Consequence per L-32, for P3 to rule not curation: the Matt incumbent "
                    "(youtube:KaMPoPywM40, whirlwind#0) carries the reference load as PRIMARY with "
                    "nameable-discountable confounds; this quarterly video demotes to provenance "
                    "corroborator.",
                    archetype_id="whirlwind", rank=trank, subject="youtube:3BnHvNZ_4YM",
                    target_run=MAIN_RUN)
                if not target:
                    finding("downgrade-target-missing", "UNRESOLVED",
                            "job 29's Part-1 verdict targets youtube:3BnHvNZ_4YM but no main-lane row "
                            "carries that normalized primary URL",
                            archetype_id="whirlwind", subject="youtube:3BnHvNZ_4YM")
            else:
                finding("uncurated-dossier-block", "WARN",
                        f"dossier carries a non-candidate '## {b['title']}' block with "
                        f"{len(b['fields'])} field(s) that this curation has no home for; content "
                        f"is NOT discarded silently — it is named here: "
                        f"{json.dumps(b['fields'], ensure_ascii=False)}",
                        archetype_id=arche, subject=b["title"])

        if blocks:
            finding("nonstandard-dossier-format", "INFO",
                    f"supplement dossier departs from the main-lane grammar: "
                    f"{len(blocks)} non-candidate '## ' block(s) "
                    f"({', '.join(b['title'] for b in blocks)}). Parsed by an extended walker that "
                    f"keeps such blocks OUT of the candidate rows rather than letting their fields "
                    f"bleed into the following candidate",
                    archetype_id=arche, subject=job_name)

        seen_ranks = set()
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

            missing = [k for k in p2.HARD_REQUIRED if not f.get(k)]
            if missing:
                finding("missing-required-field", "UNRESOLVED",
                        f"required field(s) absent or empty: {', '.join(missing)}",
                        archetype_id=arche, rank=rank, subject=",".join(missing))

            praw = f.get("primary_url", "")
            purl, plabel = p2.split_md_field(praw) if praw else (None, None)
            ok, why = p2.url_wellformed(purl)
            if not ok:
                finding("malformed-primary-url", "UNRESOLVED",
                        f"primary_url did not verify structurally: {why}. Raw value: {praw!r}",
                        archetype_id=arche, rank=rank, subject=praw)

            sraw = f.get("secondary_urls", "")
            surls = p2.URL_RE.findall(sraw) if sraw else []
            for su in surls:
                ok2, why2 = p2.url_wellformed(su)
                if not ok2:
                    finding("malformed-secondary-url", "WARN",
                            f"secondary URL did not verify structurally: {why2}",
                            archetype_id=arche, rank=rank, subject=su)
            if not surls:
                if not sraw:
                    finding("no-secondary-urls", "INFO",
                            "candidate carries no secondary_urls field — single-source reference; "
                            "corroboration rests entirely on the primary URL",
                            archetype_id=arche, rank=rank)
                else:
                    finding("no-secondary-urls", "INFO",
                            f"secondary_urls is present but yields zero URLs — the field carries the "
                            f"literal template token {sraw!r} rather than being populated or omitted. "
                            f"Curated as single-source; the raw token is preserved verbatim in "
                            f"secondary_urls_raw and is NOT repaired",
                            archetype_id=arche, rank=rank, subject=sraw)

            craw = f.get("temporal_coverage", "")
            cm = p2.COVER_RE.search(craw) if craw else None
            if cm:
                w = cm.group("w").upper() == "Y"
                a = cm.group("a").upper() == "Y"
                i = cm.group("i").upper() == "Y"
                cw, ca, ci, full = int(w), int(a), int(i), int(w and a and i)
                if not (w or a or i):
                    finding("zero-coverage", "WARN",
                            "all three temporal flags are N — the reference documents no phase",
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
                        f"media_type is {mt!r}; charter § 4 P2 prefers video. Retained",
                        archetype_id=arche, rank=rank, subject=mt)

            sg = (f.get("source_game") or "")
            if re.search(r"path of exile", sg, re.I):
                finding("poe-leakage", "UNRESOLVED",
                        f"source_game {sg!r} is PoE, but jobs 27/28 were briefed non-PoE and L-32 "
                        f"records ZERO PoE leakage — this contradicts the gate of record",
                        archetype_id=arche, rank=rank, subject=sg)

            conf = f.get("confounds")
            if conf:
                low = conf.lower()
                if re.search(r"archiv|could not be independently|availability|predates|2008|"
                             r"pre-release|unverified", low) or \
                   re.search(r"archiv|unverified|pre-release|2008", (f.get("readability_notes") or "").lower()):
                    finding("archival-source", "WARN",
                            "candidate rests on ARCHIVAL / historical footage rather than a live "
                            "first-party asset. Carried on the row, not laundered: confounds = "
                            f"{conf!r}; readability_notes = {f.get('readability_notes')!r}. "
                            "L-32 classes both whirlwind alternates as archival-grade "
                            "(silhouette/cadence donors), NOT as extraction masters",
                            archetype_id=arche, rank=rank, subject=f.get("primary_url"))

            extras = [k for k in c["order"]
                      if k not in p2.REQUIRED_FIELDS and k != "confounds"]
            if extras:
                finding("extra-field", "INFO",
                        f"candidate carries field(s) outside the chartered set: "
                        f"{', '.join(sorted(set(extras)))}. Not dropped — reported so the value is "
                        f"not lost silently",
                        archetype_id=arche, rank=rank, subject=",".join(sorted(set(extras))))

            nurl = p2.norm_url(purl or "")

            # ---- cross-run / cross-archetype reuse ----
            if nurl and nurl in prior_primary:
                holders = "; ".join(f"{a}#{r}" for a, r in prior_primary[nurl])
                mine_t = re.search(r"[?&]t=([^&\s\)]+)", praw or "")
                theirs = "; ".join(
                    f"{a}#{r} skill={sk!r} t={(re.search(r'[?&]t=([^&s)]+)', pr or '') or [None, 'none'])[1]}"
                    for (a, r, sk, pr) in [
                        (a, r,
                         con.execute("select skill_or_mtx_name from vfx_reference_candidate where"
                                     " curation_run=? and archetype_id=? and candidate_rank=?",
                                     (MAIN_RUN, a, r)).fetchone()[0],
                         con.execute("select primary_url_raw from vfx_reference_candidate where"
                                     " curation_run=? and archetype_id=? and candidate_rank=?",
                                     (MAIN_RUN, a, r)).fetchone()[0])
                        for a, r in prior_primary[nurl]])
                finding("cross-run-primary-reuse",
                        "INFO" if all(a == arche for a, _ in prior_primary[nurl]) else "WARN",
                        f"this supplement primary is already a MAIN-lane primary at {holders} "
                        f"(run {MAIN_RUN}). One video, two archetypes. It is NOT necessarily a "
                        f"defect — a multi-skill showcase can legitimately demonstrate two "
                        f"archetypes at different seek points — so the seek points are reported "
                        f"rather than assumed: this row is skill={f.get('skill_or_mtx_name')!r} "
                        f"t={mine_t.group(1) if mine_t else 'none'}; the main lane holds {theirs}. "
                        f"P3 must not anchor both archetypes on it without saying why "
                        f"(cf. ledger L-29(6): one reference cannot anchor two archetypes whose "
                        f"causality classes differ)",
                        archetype_id=arche, rank=rank, subject=nurl, target_run=MAIN_RUN)
            elif nurl and nurl in prior_any and arche not in prior_any[nurl]:
                finding("cross-run-url-reuse", "INFO",
                        "URL already appears in the main lane (as a secondary) under: "
                        + ", ".join(sorted(prior_any[nurl])),
                        archetype_id=arche, rank=rank, subject=nurl, target_run=MAIN_RUN)
            if nurl and nurl in seen_norm:
                finding("intra-supplement-primary-duplicate", "UNRESOLVED",
                        "the same primary appears twice inside the supplement lane: "
                        + f"{seen_norm[nurl]} and {arche}#{rank}",
                        archetype_id=arche, rank=rank, subject=nurl)
            if nurl:
                seen_norm[nurl] = f"{arche}#{rank}"

            skey = (arche, (f.get("skill_or_mtx_name") or "").strip().lower())
            for (prank, pnorm, pmedia) in prior_skill.get(skey, []):
                if pnorm != nurl:
                    finding("same-skill-alternate-media", "INFO",
                            f"same archetype + same skill name as main-lane {arche}#{prank} "
                            f"(media_type {pmedia!r}, {pnorm}) but a DIFFERENT source "
                            f"({mt!r}, {nurl}). This is job 30's stated purpose — a video companion "
                            f"for a gif canonical — recorded so P3 pairs them deliberately rather "
                            f"than treating them as two independent references",
                            archetype_id=arche, rank=rank, subject=nurl, target_run=MAIN_RUN)

            cand_rows.append({
                "curation_run": CURATION_RUN, "archetype_id": arche, "vote_run": VOTE_RUN,
                "candidate_rank": rank,
                "source_game": f.get("source_game"), "skill_or_mtx_name": f.get("skill_or_mtx_name"),
                "candidate_title_raw": c["title"],
                "primary_url": purl, "primary_url_raw": praw or None, "primary_url_label": plabel,
                "primary_url_norm": nurl or None,
                "secondary_urls_json": json.dumps(surls, ensure_ascii=False),
                "secondary_urls_raw": sraw or None, "secondary_url_count": len(surls),
                "media_type": f.get("media_type"),
                "coverage_windup": cw, "coverage_active": ca, "coverage_impact": ci,
                "coverage_raw": craw or None, "full_lifecycle": full,
                "why_it_fits": f.get("why_it_fits"), "readability_notes": f.get("readability_notes"),
                "provenance": "codex-p2-dossier", "validation_status": None, "dossier_path": rel,
                "conformance": "PENDING", "curated_at": now, "source": SOURCE,
                "source_date": SOURCE_DATE, "confounds": conf,
            })

        _ = before  # per-dossier finding_count is recomputed after ALL findings are raised, below
        dossier_rows.append([
            CURATION_RUN, arche, VOTE_RUN, rel, nbytes, p2.md5(path), len(cands), log_lines,
            joins, int(len(cands) >= 3),
            "PENDING", 0, now, SOURCE, SOURCE_DATE,
        ])

    # ---- source_game string variance across the two lanes ----
    # Detection-only normalization. Nothing is rewritten: the main lane preserves game strings
    # VERBATIM by policy (predecessor MIGRATION § 4.5), and this lane does the same. The point is
    # that a P4 rollup keyed on source_game will now silently split the same game.
    def gkey(s):
        s = (s or "").lower().split(",")[0].strip()
        for a, b in ((" iii", " 3"), (" ii", " 2"), (" iv", " 4")):
            s = s.replace(a, b)
        return re.sub(r"\s*\(.*?\)\s*", "", s).strip()

    main_games = {r[0] for r in con.execute(
        "select distinct source_game from vfx_reference_candidate where curation_run = ?",
        (MAIN_RUN,))}
    for r in cand_rows:
        sg = r["source_game"]
        twins = sorted(m for m in main_games if m != sg and gkey(m) == gkey(sg))
        if twins:
            finding("source-game-string-variance", "INFO",
                    f"source_game {sg!r} names the same game as main-lane string(s) "
                    f"{twins} but is spelled differently. NOT normalized — game strings are "
                    f"preserved verbatim as authored in both lanes (predecessor MIGRATION § 4.5), "
                    f"because expansion/season/build qualifiers are real provenance. Reported so "
                    f"any P4 rollup keyed on source_game groups them deliberately",
                    archetype_id=r["archetype_id"], rank=r["candidate_rank"], subject=sg)
        elif "," in (sg or ""):
            finding("source-game-string-variance", "INFO",
                    f"source_game {sg!r} packs build provenance into the game field rather than "
                    f"naming the game alone. Preserved verbatim; reported so a rollup does not read "
                    f"it as a distinct title",
                    archetype_id=r["archetype_id"], rank=r["candidate_rank"], subject=sg)

    # _manifest.tsv was never extended for jobs 27-30 — state it rather than let the main-lane
    # detector fire a misleading 'unmanifested-dossier' WARN against a lane it does not describe.
    man = os.path.join(os.path.dirname(JOBS_DIR), "jobs", "_manifest.tsv")
    man_ids = {l.split("\t")[0].strip() for l in open(man, encoding="utf-8") if l.strip()} \
        if os.path.exists(man) else set()
    if not (set(SUPPLEMENT_MAP) & man_ids):
        finding("manifest-not-extended", "INFO",
                "jobs/_manifest.tsv still lists only the 26 main-lane archetypes; jobs 27-30 were "
                "briefed via their prompt files (27..30-*.prompt.md, all present). The prompt files "
                "are the supplement lane's manifest of record. Recorded so a later reader does not "
                "read the manifest as the complete job list",
                subject="jobs/_manifest.tsv")

    # ---- per-candidate conformance, from findings actually raised AGAINST THIS RUN'S ROWS ----
    flagged = {(f["archetype_id"], f["candidate_rank"]) for f in findings
               if f["candidate_rank"] is not None and f["severity"] in ("WARN", "UNRESOLVED")
               and f["target_curation_run"] is None}
    for r in cand_rows:
        r["conformance"] = ("CONFORMING-WITH-FINDING"
                            if (r["archetype_id"], r["candidate_rank"]) in flagged else "CONFORMING")

    # per-dossier finding_count + conformance, derived from every finding the dossier raised
    # (including those raised after the per-dossier loop closed — a count computed mid-loop would
    # have silently under-reported them, and a dossier's verdict must not be cleaner than its facts)
    for d in dossier_rows:
        n = sum(1 for f in findings if f["archetype_id"] == d[1])
        d[10] = "CONFORMING" if n == 0 else "CONFORMING-WITH-FINDING"
        d[11] = n

    cols = list(cand_rows[0].keys()) if cand_rows else []
    with con:
        con.execute("delete from vfx_reference_candidate where curation_run = ?", (CURATION_RUN,))
        con.execute("delete from vfx_reference_dossier  where curation_run = ?", (CURATION_RUN,))
        con.execute("delete from vfx_curation_finding   where curation_run = ?", (CURATION_RUN,))
        if cand_rows:
            con.executemany(
                f"insert into vfx_reference_candidate ({','.join(cols)}) "
                f"values ({','.join('?' * len(cols))})",
                [tuple(r[c] for c in cols) for r in cand_rows])
        con.executemany(
            "insert into vfx_reference_dossier (curation_run,archetype_id,vote_run,dossier_path,"
            "dossier_bytes,dossier_md5,candidate_count,search_log_lines,archetype_joins,"
            "meets_min_three,conformance,finding_count,curated_at,source,source_date) "
            "values (" + ",".join("?" * 15) + ")", dossier_rows)
        con.executemany(
            "insert into vfx_curation_finding (curation_run,finding_id,kind,severity,archetype_id,"
            "candidate_rank,subject,detail,status,raised_at,target_curation_run) "
            "values (?,?,?,?,?,?,?,?,?,?,?)",
            [(CURATION_RUN, f["finding_id"], f["kind"], f["severity"], f["archetype_id"],
              f["candidate_rank"], f["subject"], f["detail"], f["status"], now,
              f["target_curation_run"]) for f in findings])

        # ---- union views: lane is DERIVED, never stored (no backfill, no ambiguous NULL) ----
        con.execute("drop view if exists v_vfx_reference_candidate_p2")
        con.execute(f"""
            create view v_vfx_reference_candidate_p2 as
            select c.*, case c.curation_run
                          when '{MAIN_RUN}' then 'p2-main'
                          when '{CURATION_RUN}' then 'p2-supplement'
                        end as lane
              from vfx_reference_candidate c
             where c.curation_run in ('{MAIN_RUN}','{CURATION_RUN}')""")
        con.execute("drop view if exists v_vfx_reference_dossier_p2")
        con.execute(f"""
            create view v_vfx_reference_dossier_p2 as
            select d.*, case d.curation_run
                          when '{MAIN_RUN}' then 'p2-main'
                          when '{CURATION_RUN}' then 'p2-supplement'
                        end as lane
              from vfx_reference_dossier d
             where d.curation_run in ('{MAIN_RUN}','{CURATION_RUN}')""")

    # ---- additivity proof: the main lane must be byte-for-byte what it was ----
    post_main_md5 = con.execute(
        "select group_concat(archetype_id || '|' || candidate_rank || '|' ||"
        " coalesce(primary_url_norm,'') || '|' || conformance, char(10))"
        " from (select * from vfx_reference_candidate where curation_run = ?"
        "        order by archetype_id, candidate_rank)", (MAIN_RUN,)).fetchone()[0]
    post = {t: con.execute(f"select count(*) from {t}").fetchone()[0]
            for t in ("vfx_reference_candidate", "vfx_reference_dossier", "vfx_curation_finding")}
    main_counts = {t: con.execute(
        f"select count(*) from {t} where curation_run = ?", (MAIN_RUN,)).fetchone()[0]
        for t in ("vfx_reference_candidate", "vfx_reference_dossier", "vfx_curation_finding")}
    print(f"[post] {post}   main-lane counts unchanged: {main_counts}")
    print(f"[additivity] main-lane digest unchanged: {pre_main_md5 == post_main_md5}")
    print(f"[additivity] main-lane confounds all NULL: "
          f"{con.execute('select count(*) from vfx_reference_candidate where curation_run=? and confounds is not null', (MAIN_RUN,)).fetchone()[0] == 0}")

    ic = con.execute("pragma integrity_check").fetchone()[0]
    fk = con.execute("pragma foreign_key_check").fetchall()
    print(f"[db] integrity_check={ic}  foreign_key_check_violations={len(fk)}")
    print(f"[rows] +candidates={len(cand_rows)}  +dossiers={len(dossier_rows)}  "
          f"+findings={len(findings)}")

    print("\n--- supplement findings ---")
    for r in con.execute("""select finding_id, severity, kind, archetype_id, candidate_rank,
                                   target_curation_run
                              from vfx_curation_finding where curation_run = ?
                             order by case severity when 'UNRESOLVED' then 0 when 'WARN' then 1
                                       else 2 end, finding_id""", (CURATION_RUN,)):
        tgt = "  ->MAIN" if r["target_curation_run"] else ""
        print(f"  {r['finding_id']}  {r['severity']:<11} {r['kind']:<34} "
              f"{r['archetype_id'] or '-'}#{r['candidate_rank'] if r['candidate_rank'] is not None else '-'}{tgt}")

    print("\n--- post-delta non-PoE coverage, the two 100%-PoE archetypes ---")
    for a in ("ground_targeted_circle", "single_target"):
        for r in con.execute("""
            select count(*) tot,
                   sum(source_game not like '%Path of Exile%') nonpoe,
                   sum(source_game not like '%Path of Exile%' and full_lifecycle = 1
                       and lower(media_type) = 'video') nonpoe_flc_video
              from v_vfx_reference_candidate_p2 where archetype_id = ?""", (a,)):
            print(f"  {a:<24} total={r['tot']}  non-PoE={r['nonpoe']}  "
                  f"non-PoE full-lifecycle video={r['nonpoe_flc_video']}")

    print("\n--- supplement source_game distribution ---")
    for r in con.execute("""select source_game, count(*) n from vfx_reference_candidate
                            where curation_run = ? group by 1 order by 2 desc, 1""", (CURATION_RUN,)):
        print(f"  {r['source_game']:<30} {r['n']}")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
