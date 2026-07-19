#!/usr/bin/env python3
"""
VDM-1 COMPENDIUM GENERATOR (elrond, D-11a).

Regenerates the human/machine compendium FROM the corpus.db `kit_master` VIEW
(the ONE query surface, computed live). This SUPERSEDES the four review rosters
(REVIEW-BOOK-ROSTER-{EXACT,CLOSE,APPROX,GAPPED}.md), which carry no citations.

Outputs (into research/vdm1/compendium/):
  - kits-<game>.md   (per-game, 21 files) — human render
  - vdm1-compendium.jsonl  (one machine render, one JSON object per kit)
  - README.md        (index + provenance stamp: corpus.db md5 + v1.1)

READ-ONLY on corpus.db. Stamped with the post-migration file md5 + v1.1.
Does NOT git-commit.
"""
import sqlite3
import json
import os
import hashlib

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/compendium"
VERSION = "v1.1-verified"
GEN_UTC = "2026-07-19T20:04:46Z"

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

os.makedirs(OUT, exist_ok=True)
db_md5 = md5_of(DB)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cols = [r[1] for r in cur.execute("PRAGMA table_info(kit_master)").fetchall()]
rows = [dict(r) for r in cur.execute(
    "SELECT * FROM kit_master ORDER BY game, "
    "CASE grade WHEN 'EXACT' THEN 1 WHEN 'CLOSE' THEN 2 WHEN 'APPROX' THEN 3 "
    "WHEN 'GAPPED' THEN 4 ELSE 5 END, kit_id").fetchall()]
conn.close()

total = len(rows)
games = sorted({r["game"] for r in rows})

# ---- per-game .md renders --------------------------------------------------
def fmt_cites(cj):
    if not cj:
        return "_(no live citations)_"
    try:
        arr = json.loads(cj)
    except Exception:
        return "_(citation parse error)_"
    if not arr:
        return "_(no live citations)_"
    parts = []
    for c in arr:
        u = c.get("url") or ""
        site = c.get("site") or ""
        auth = c.get("author_handle") or ""
        cc = c.get("cite_class") or ""
        arch = c.get("archive_url") or ""
        seg = f"[{cc}] {site}"
        if auth:
            seg += f" · @{auth}"
        seg += f" · {u}"
        if arch:
            seg += f" (archive: {arch})"
        parts.append(seg)
    return "; ".join(parts)

game_counts = {}
for g in games:
    grows = [r for r in rows if r["game"] == g]
    game_counts[g] = len(grows)
    lines = []
    lines.append(f"# VDM-1 Compendium — {g} ({len(grows)} kits)")
    lines.append("")
    lines.append(f"> **Source:** `corpus.db` `kit_master` view (live-computed; cannot drift). "
                 f"**{VERSION}** · db md5 `{db_md5}` · generated {GEN_UTC}.")
    lines.append("> Supersedes the four review rosters (which carry no citations). "
                 "`kit_citations` is the sole citation authority; raw mobile-era descriptors are "
                 "NOT exposed (provenance-only).")
    lines.append("")
    # grade histogram for this game
    from collections import Counter
    gh = Counter(r["grade"] for r in grows)
    lines.append("| grade | n | | verify (C/X/U total) | dossier rows | cited kits |")
    lines.append("|---|---|---|---|---|---|")
    cited = sum(1 for r in grows if (r["citation_count"] or 0) > 0)
    vc = sum(r["verify_confirmed"] or 0 for r in grows)
    vx = sum(r["verify_contradicted"] or 0 for r in grows)
    vu = sum(r["verify_unsupported"] or 0 for r in grows)
    dr = sum(r["dossier_rows"] or 0 for r in grows)
    lines.append(f"| E {gh.get('EXACT',0)} · C {gh.get('CLOSE',0)} · A {gh.get('APPROX',0)} · "
                 f"G {gh.get('GAPPED',0)} | {len(grows)} | | {vc}/{vx}/{vu} | {dr} | {cited}/{len(grows)} |")
    lines.append("")
    for r in grows:
        flags = []
        if r["negative"]:
            flags.append("NEGATIVE")
        if r["is_system"]:
            flags.append("is_system")
        flag_s = (" `[" + ", ".join(flags) + "]`") if flags else ""
        lines.append(f"## {r['kit_id']} — {r['folk_name'] or ''}{flag_s}")
        lines.append("")
        lines.append(f"- **grade / terminal:** `{r['grade']}` / `{r['terminal_state']}`")
        lines.append(f"- **elements attested:** {r['elements_attested'] or '_(silent)_'}")
        lines.append(f"- **ailments attested:** {r['ailments_attested'] or '_(none)_'}")
        lines.append(f"- **eras:** {r['eras'] or '_(unattested)_'} · "
                     f"**tier:** {r['tier'] or '—'} · **lineage:** {r['lineage'] or '—'}")
        lines.append(f"- **verify (C/X/U):** {r['verify_confirmed'] or 0} / "
                     f"{r['verify_contradicted'] or 0} / {r['verify_unsupported'] or 0} · "
                     f"**dossier rows:** {r['dossier_rows'] or 0}")
        lines.append(f"- **citations ({r['citation_count'] or 0}):** {fmt_cites(r['citations_json'])}")
        if r["deviation_notes"]:
            lines.append(f"- **deviations:** {r['deviation_notes']}")
        lines.append("")
    with open(os.path.join(OUT, f"kits-{g}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

# ---- one .jsonl machine render ---------------------------------------------
with open(os.path.join(OUT, "vdm1-compendium.jsonl"), "w") as f:
    # header line as a metadata object
    f.write(json.dumps({
        "_meta": True, "version": VERSION, "corpus_db_md5": db_md5,
        "generated_utc": GEN_UTC, "kit_count": total, "game_count": len(games),
        "source": "corpus.db kit_master view", "supersedes": "REVIEW-BOOK-ROSTER-{EXACT,CLOSE,APPROX,GAPPED}.md",
        "citation_authority": "kit_citations (non-quarantined)",
        "note": "citations_json parsed to array; raw mobile-era descriptors not exposed (provenance-only)",
    }, ensure_ascii=False, separators=(",", ":")) + "\n")
    for r in rows:
        obj = dict(r)
        # parse citations_json into a proper array for machine consumers
        cj = obj.pop("citations_json", None)
        try:
            obj["citations"] = json.loads(cj) if cj else []
        except Exception:
            obj["citations"] = []
        f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")

# ---- README index ----------------------------------------------------------
readme = []
readme.append("# VDM-1 COMPENDIUM — the one-representation render")
readme.append("")
readme.append(f"> **STATUS:** CURRENT ({VERSION}). Generated {GEN_UTC} FROM the `corpus.db` "
              f"`kit_master` view. **db md5 `{db_md5}`.**")
readme.append("")
readme.append("**Authority (D-11a / D-11f inversion):** post-v1.1, `corpus.db` + this compendium "
              "GOVERN. This compendium is the ONE-per-kit representation Matt asked for — the most "
              "complete version with URL + authorship citations attached — assembled live from the "
              "`kit_master` view (identity ⋈ mapping ⋈ citation-aggregate ⋈ verify-tally ⋈ "
              "dossier-count). It **supersedes** the four review rosters "
              "(`REVIEW-BOOK-ROSTER-{EXACT,CLOSE,APPROX,GAPPED}.md`), which carry no citations; "
              "those retire to git as the review artifact.")
readme.append("")
readme.append(f"**Contents:** {total} kits · {len(games)} games · per-game `.md` + one "
              "`vdm1-compendium.jsonl` (machine render).")
readme.append("")
readme.append("| game | kits | file |")
readme.append("|---|---|---|")
for g in sorted(games, key=lambda x: (-game_counts[x], x)):
    readme.append(f"| {g} | {game_counts[g]} | [`kits-{g}.md`](kits-{g}.md) |")
readme.append(f"| **TOTAL** | **{total}** | `vdm1-compendium.jsonl` |")
readme.append("")
readme.append("**Regeneration:** `python3 research/scripts/vdm1_compendium_gen_2026_07_19.py` "
              "(read-only on `corpus.db`; re-stamps the md5). Cheap to re-run if a trailing citation "
              "lands (e.g. the `ud-snowstorm-frost` citation-pending residue closing 573→574).")
readme.append("")
readme.append("**Provenance-cleanliness:** the `kit_master` view exposes NO mobile-era raw descriptors "
              "(`elem_raw`, suffix raws); those remain provenance-only in `canon_corpus`. `kit_citations` "
              "is the sole citation authority (`canon_corpus.source_urls` is DEPRECATED-frozen per D-11c).")
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("\n".join(readme) + "\n")

print(f"COMPENDIUM generated: {total} kits, {len(games)} games")
print(f"  per-game .md: {len(games)} files")
print(f"  jsonl: vdm1-compendium.jsonl ({total} kit lines + 1 meta line)")
print(f"  README.md + provenance stamp (db md5 {db_md5}, {VERSION})")
print(f"  out dir: {OUT}")
# integrity: jsonl line count == total + 1 meta
with open(os.path.join(OUT, "vdm1-compendium.jsonl")) as f:
    n = sum(1 for _ in f)
print(f"  jsonl line count = {n} (expect {total+1})")
assert n == total + 1, f"jsonl line count {n} != {total+1}"
print("  jsonl line-count assert OK")
