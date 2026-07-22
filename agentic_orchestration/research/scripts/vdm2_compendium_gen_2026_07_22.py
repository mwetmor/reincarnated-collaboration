#!/usr/bin/env python3
"""
VDM-2 COMPENDIUM GENERATOR (elrond, W6-data — the final Leg-A render wave).

Regenerates the human/machine compendium FROM the corpus.db `kit_master` VIEW
(574 rows, the ONE per-kit query surface) ENRICHED with the six VDM-2 per-skill
"side-car" blocks + the two global registries — all computed live in the RENDER
LAYER. This is the v2.0 successor to the VDM-1 compendium (v1.1-verified).

MECHANISM — Approach B (freeze-cleanest lean):
  The VDM-1 gen was READ-ONLY on corpus.db. This gen KEEPS it read-only. The
  six-side-car joins happen HERE (query layer), never in the DB. corpus.db is
  NEVER mutated: no view redef, no DDL, no data touch. The file md5 stays
  `bebc933b0bf9bcab5988bbc16bcc55b4`; canon_corpus data columns stay frozen.

ANTI-EXPLOSION LAW (non-negotiable):
  The per-skill side-cars are multi-row-per-kit (skill_geometry_band up to 5
  skills/kit; kit_deviation / recognition_hook / kit_acceptance_assert up to
  2/kit). A naive simultaneous LEFT JOIN would produce the Cartesian product
  per kit (up to 5*2*2*2 = 40 rows for a single kit) and blow the row count.
  Instead every multi-row side-car is aggregated via a CORRELATED SUBQUERY +
  json_group_array (exactly the pattern the kit_master view already uses for
  citations / verify tallies). The surface stays EXACTLY 574 rows. Kits with no
  side-car row keep an empty [] array (annex/system classes) — LEFT-join
  semantics preserved via the subquery returning NULL/empty.

SIDE-CARS surfaced per-kit (record-class kits populate; annex/system stay empty):
  skill_geometry_band (490) · kit_deviation (259) · recognition_hook (441) ·
  kit_acceptance_assert (310) · kit_delta_t4 (267, 1:1 direct LEFT join) ·
  kit_numeric (2)
REGISTRIES surfaced (global reference blocks + per-kit token lists):
  door_registry (28) — resolves each kit's mapping_json.t4_doors tokens
  motion_signature_registry (18) — resolves each skill band's motion_signature
ELEMENT COURT (the W5-corrected field):
  canon_corpus.court (reconciled, enum-checked) is re-joined and surfaced as the
  per-kit `element` field. canon_corpus.original_element carries the RAW
  provenance (reversibility). elem_raw is NOT exposed (provenance-only law from
  VDM-1 held). d2-wl-blood-boil surfaces court=fire (W5 correction).

Outputs (into research/vdm2/compendium/ — NEW dir; v1.1 lineage stays recoverable
in research/vdm1/compendium/):
  - kits-<game>.md        (per-game human render, one per game)
  - vdm2-compendium.jsonl (one machine render, one JSON object per kit + _meta)
  - registries.md         (the two global reference tables)
  - README.md             (index + provenance stamp: corpus.db md5 + v2.0)

READ-ONLY on corpus.db. Stamped with the corpus.db file md5 + v2.0. Does NOT
git-commit.
"""
import sqlite3
import json
import os
import hashlib
from collections import Counter

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm2/compendium"
VERSION = "v2.0"
GEN_UTC = "2026-07-22T09:46:42Z"

# The freeze fingerprints this render was generated against (W6-data brief).
FREEZE_FULL_585 = "38823f2fee619cb856c342f2abd10c15"      # kit_id,elem_raw,court,corpus_class ORDER BY kit_id
FREEZE_584_DIFF = "d5a9a8e04d585a610b214c674830289a"      # same WHERE kit_id != 'd2-wl-blood-boil'
FREEZE_DB_MD5   = "bebc933b0bf9bcab5988bbc16bcc55b4"      # whole-file md5 (Approach B: must hold)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sql_md5(cur, sql):
    """md5 of a query's row text, mimicking the sqlite3 CLI pipe-through-md5 fingerprint."""
    h = hashlib.md5()
    for row in cur.execute(sql):
        line = "|".join("" if v is None else str(v) for v in row)
        h.update((line + "\n").encode("utf-8"))
    return h.hexdigest()


os.makedirs(OUT, exist_ok=True)
db_md5 = md5_of(DB)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# ---- FREEZE PROOF (read-only; asserts the frozen columns are byte-identical) --
live_full_585 = sql_md5(
    cur, "SELECT kit_id,elem_raw,court,corpus_class FROM canon_corpus ORDER BY kit_id")
live_584_diff = sql_md5(
    cur, "SELECT kit_id,elem_raw,court,corpus_class FROM canon_corpus "
         "WHERE kit_id != 'd2-wl-blood-boil' ORDER BY kit_id")
freeze_ok = (live_full_585 == FREEZE_FULL_585 and
             live_584_diff == FREEZE_584_DIFF and
             db_md5 == FREEZE_DB_MD5)

# ---- registries (global reference blocks) -----------------------------------
doors = [dict(r) for r in cur.execute(
    "SELECT door_name, door_status, rfc_ref, description FROM door_registry "
    "ORDER BY door_status, door_name")]
motions = [dict(r) for r in cur.execute(
    "SELECT signature_name, engine_impl_ref, description FROM motion_signature_registry "
    "ORDER BY signature_name")]

# ---- the enriched per-kit surface -------------------------------------------
# Base is kit_master (574). We re-join canon_corpus for the VDM-2 element court
# + original_element + corpus_class, and aggregate the six side-cars via
# correlated subqueries so the surface stays exactly 574 rows.
#
# json_group_array over a correlated subquery returns '[]' (empty array text) for
# kits with no matching side-car rows — LEFT-join semantics without the explosion.
ENRICH_SQL = """
SELECT
    km.*,
    -- VDM-2 element court (reconciled, enum-checked) + raw provenance
    c.court                AS element,
    c.original_element     AS original_element,
    c.corpus_class         AS corpus_class,
    -- kit-level t4_doors tokens (resolved against door_registry) from mapping_json
    (SELECT json_extract(m.mapping_json, '$.t4_doors')
       FROM kit_mapping m WHERE m.kit_id = km.kit_id) AS t4_doors_json,
    -- side-car 1: skill_geometry_band (multi-row per kit -> json array; anti-explosion)
    (SELECT json_group_array(json_object(
                'skill_ordinal',      sgb.skill_ordinal,
                'source_skill',       sgb.source_skill,
                'delivery_class',     sgb.delivery_class,
                'origin',             sgb.origin,
                'width_band',         sgb.width_band,
                'range_band',         sgb.range_band,
                'speed_band',         sgb.speed_band,
                'pierce',             sgb.pierce,
                'chain',              sgb.chain,
                'fork',               sgb.fork,
                'count_per_cast',     sgb.count_per_cast,
                'cadence_class',      sgb.cadence_class,
                'motion_signature',   sgb.motion_signature,
                'band_conf',          sgb.band_conf,
                'derivation',         sgb.derivation))
       FROM (SELECT * FROM skill_geometry_band WHERE kit_id = km.kit_id
             ORDER BY skill_ordinal) sgb) AS geometry_bands_json,
    -- side-car 2: kit_deviation
    (SELECT json_group_array(json_object(
                'missing_expression', kd.missing_expression,
                'deviation_class',    kd.deviation_class,
                'proposed_fix_type',  kd.proposed_fix_type,
                'proposed_fix_target',kd.proposed_fix_target,
                'downgrade_owner',    kd.downgrade_owner,
                'docket_id',          kd.docket_id))
       FROM (SELECT * FROM kit_deviation WHERE kit_id = km.kit_id
             ORDER BY deviation_id) kd) AS deviations_json,
    -- side-car 3: recognition_hook
    (SELECT json_group_array(json_object(
                'hook_id',            rh.hook_id,
                'rank',               rh.rank,
                'hook_type',          rh.hook_type,
                'hook_text',          rh.hook_text,
                'expressed_by',       rh.expressed_by,
                'provenance',         rh.provenance,
                'coverage_status',    rh.coverage_status))
       FROM (SELECT * FROM recognition_hook WHERE kit_id = km.kit_id
             ORDER BY rank) rh) AS recognition_hooks_json,
    -- side-car 4: kit_acceptance_assert
    (SELECT json_group_array(json_object(
                'assert_text',        kaa.assert_text,
                'hook_id',            kaa.hook_id,
                'expected_state',     kaa.expected_state,
                'last_result',        kaa.last_result,
                'routed_docket_id',   kaa.routed_docket_id))
       FROM (SELECT * FROM kit_acceptance_assert WHERE kit_id = km.kit_id
             ORDER BY assert_id) kaa) AS acceptance_asserts_json,
    -- side-car 5: kit_delta_t4 (1:1 per kit -> direct LEFT join, no explosion)
    kdt.shape          AS t4_shape,
    kdt.asserts_json   AS t4_asserts_json,
    kdt.shape_signoff  AS t4_shape_signoff,
    -- side-car 6: kit_numeric
    (SELECT json_group_array(json_object(
                'numeric_key',        kn.numeric_key,
                'source_value',       kn.source_value,
                'source_scale',       kn.source_scale,
                'rdr_value',          kn.rdr_value,
                'rule_id',            kn.rule_id))
       FROM (SELECT * FROM kit_numeric WHERE kit_id = km.kit_id
             ORDER BY numeric_key) kn) AS numerics_json
FROM kit_master km
JOIN canon_corpus c        ON c.kit_id = km.kit_id
LEFT JOIN kit_delta_t4 kdt ON kdt.kit_id = km.kit_id
ORDER BY km.game,
    CASE km.grade WHEN 'EXACT' THEN 1 WHEN 'CLOSE' THEN 2 WHEN 'APPROX' THEN 3
                  WHEN 'GAPPED' THEN 4 ELSE 5 END,
    km.kit_id
"""
rows = [dict(r) for r in cur.execute(ENRICH_SQL).fetchall()]

# ---- iron-law + six-block measured counts (reported in the stamp) -----------
def scalar(sql):
    return cur.execute(sql).fetchone()[0]

counts = {
    "canon_corpus": scalar("SELECT COUNT(*) FROM canon_corpus"),
    "kit_master": scalar("SELECT COUNT(*) FROM kit_master"),
    "is_system": scalar("SELECT COUNT(*) FROM canon_corpus WHERE is_system=1"),
    "skill_geometry_band": scalar("SELECT COUNT(*) FROM skill_geometry_band"),
    "kit_deviation": scalar("SELECT COUNT(*) FROM kit_deviation"),
    "recognition_hook": scalar("SELECT COUNT(*) FROM recognition_hook"),
    "kit_acceptance_assert": scalar("SELECT COUNT(*) FROM kit_acceptance_assert"),
    "kit_delta_t4": scalar("SELECT COUNT(*) FROM kit_delta_t4"),
    "kit_numeric": scalar("SELECT COUNT(*) FROM kit_numeric"),
    "kit_door_arg": scalar("SELECT COUNT(*) FROM kit_door_arg"),
    "verify_ledger": scalar("SELECT COUNT(*) FROM verify_ledger"),
    "door_registry": scalar("SELECT COUNT(*) FROM door_registry"),
    "motion_signature_registry": scalar("SELECT COUNT(*) FROM motion_signature_registry"),
}
conn.close()

total = len(rows)
games = sorted({r["game"] for r in rows})
game_counts = {g: sum(1 for r in rows if r["game"] == g) for g in games}


# ---- helpers ----------------------------------------------------------------
def parse_arr(js):
    if not js:
        return []
    try:
        v = json.loads(js)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def fmt_cites(cj):
    arr = parse_arr(cj)
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


def fmt_bands(js):
    arr = parse_arr(js)
    if not arr:
        return None
    out = []
    for b in arr:
        seg = f"  - `#{b.get('skill_ordinal')}` **{b.get('source_skill') or '—'}**: "
        bits = []
        for k in ("delivery_class", "range_band", "width_band", "speed_band",
                  "cadence_class", "motion_signature"):
            if b.get(k):
                bits.append(f"{k.replace('_band','').replace('_class','')}={b[k]}")
        if b.get("count_per_cast"):
            bits.append(f"count={b['count_per_cast']}")
        if b.get("pierce") and b.get("pierce") != "0":
            bits.append(f"pierce={b['pierce']}")
        if b.get("chain"):
            bits.append(f"chain={b['chain']}")
        if b.get("fork"):
            bits.append(f"fork={b['fork']}")
        seg += ", ".join(bits) if bits else "_(bands silent)_"
        if b.get("band_conf") is not None:
            seg += f" · conf {b['band_conf']}"
        out.append(seg)
    return "\n".join(out)


def fmt_hooks(js):
    arr = parse_arr(js)
    if not arr:
        return None
    out = []
    for h in sorted(arr, key=lambda x: (x.get("rank") or 99)):
        cov = h.get("coverage_status") or "?"
        htype = h.get("hook_type") or "?"
        out.append(f"  - `H{h.get('rank')}` [{htype}/{cov}] {h.get('hook_text') or ''}"
                   + (f" — _expressed by_ `{h['expressed_by']}`" if h.get("expressed_by") else ""))
    return "\n".join(out)


def fmt_deviations(js):
    arr = parse_arr(js)
    if not arr:
        return None
    out = []
    for d in arr:
        seg = f"  - [{d.get('deviation_class')}] {d.get('missing_expression') or ''}"
        if d.get("proposed_fix_type") and d.get("proposed_fix_type") != "none":
            seg += f" → _fix_ `{d.get('proposed_fix_type')}`"
            if d.get("proposed_fix_target"):
                seg += f": {d['proposed_fix_target']}"
        if d.get("downgrade_owner"):
            seg += f" · downgrade-owner `{d['downgrade_owner']}`"
        out.append(seg)
    return "\n".join(out)


def fmt_asserts(js):
    arr = parse_arr(js)
    if not arr:
        return None
    out = []
    for a in arr:
        res = a.get("last_result") or "untested"
        seg = f"  - `{a.get('assert_text') or ''}` [{res}]"
        if a.get("expected_state"):
            seg += f" · expected: {a['expected_state']}"
        out.append(seg)
    return "\n".join(out)


def fmt_t4doors(js):
    arr = parse_arr(js)
    if not arr:
        return None
    return ", ".join(f"`{d}`" for d in arr)


def fmt_numerics(js):
    arr = parse_arr(js)
    if not arr:
        return None
    out = []
    for n in arr:
        seg = f"  - `{n.get('numeric_key')}` = {n.get('source_value')} ({n.get('source_scale')})"
        if n.get("rdr_value") is not None:
            seg += f" → rdr {n['rdr_value']}"
        out.append(seg)
    return "\n".join(out)


# ---- per-game .md renders ----------------------------------------------------
for g in games:
    grows = [r for r in rows if r["game"] == g]
    lines = []
    lines.append(f"# VDM-2 Compendium — {g} ({len(grows)} kits)")
    lines.append("")
    lines.append(f"> **Source:** `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 "
                 f"side-car blocks + two registries (render-layer joins; DB never mutated). "
                 f"**{VERSION}** · db md5 `{db_md5}` · generated {GEN_UTC}.")
    lines.append("> `court` is the reconciled element court (enum-checked); `original_element` carries "
                 "raw provenance. Raw mobile-era descriptors (`elem_raw`) are NOT exposed (provenance-only). "
                 "`kit_citations` is the sole citation authority.")
    lines.append("")
    gh = Counter(r["grade"] for r in grows)
    cited = sum(1 for r in grows if (r["citation_count"] or 0) > 0)
    vc = sum(r["verify_confirmed"] or 0 for r in grows)
    vx = sum(r["verify_contradicted"] or 0 for r in grows)
    vu = sum(r["verify_unsupported"] or 0 for r in grows)
    dr = sum(r["dossier_rows"] or 0 for r in grows)
    n_bands = sum(len(parse_arr(r["geometry_bands_json"])) for r in grows)
    n_hooks = sum(len(parse_arr(r["recognition_hooks_json"])) for r in grows)
    lines.append("| grade | n | verify (C/X/U) | dossier | cited | geom-bands | hooks |")
    lines.append("|---|---|---|---|---|---|---|")
    lines.append(f"| E {gh.get('EXACT',0)} · C {gh.get('CLOSE',0)} · A {gh.get('APPROX',0)} · "
                 f"G {gh.get('GAPPED',0)} | {len(grows)} | {vc}/{vx}/{vu} | {dr} | "
                 f"{cited}/{len(grows)} | {n_bands} | {n_hooks} |")
    lines.append("")
    for r in grows:
        flags = []
        if r["negative"]:
            flags.append("NEGATIVE")
        if r["is_system"]:
            flags.append("is_system")
        if r["corpus_class"]:
            flags.append(f"class:{r['corpus_class']}")
        flag_s = (" `[" + ", ".join(flags) + "]`") if flags else ""
        lines.append(f"## {r['kit_id']} — {r['folk_name'] or ''}{flag_s}")
        lines.append("")
        lines.append(f"- **grade / terminal:** `{r['grade']}` / `{r['terminal_state']}`")
        lines.append(f"- **element (court):** {r['element'] or '_(unassigned)_'}"
                     + (f" · _raw_: {r['original_element']}" if r["original_element"] else ""))
        lines.append(f"- **elements attested:** {r['elements_attested'] or '_(silent)_'}")
        lines.append(f"- **ailments attested:** {r['ailments_attested'] or '_(none)_'}")
        lines.append(f"- **eras:** {r['eras'] or '_(unattested)_'} · "
                     f"**tier:** {r['tier'] or '—'} · **lineage:** {r['lineage'] or '—'}")
        lines.append(f"- **verify (C/X/U):** {r['verify_confirmed'] or 0} / "
                     f"{r['verify_contradicted'] or 0} / {r['verify_unsupported'] or 0} · "
                     f"**dossier rows:** {r['dossier_rows'] or 0}")
        lines.append(f"- **citations ({r['citation_count'] or 0}):** {fmt_cites(r['citations_json'])}")
        td = fmt_t4doors(r["t4_doors_json"])
        if td:
            lines.append(f"- **t4 doors:** {td}")
        if r["t4_shape"]:
            lines.append(f"- **t4 delta:** shape `{r['t4_shape']}` (signoff: {r['t4_shape_signoff']})")
        bands = fmt_bands(r["geometry_bands_json"])
        if bands:
            lines.append("- **skill geometry bands:**")
            lines.append(bands)
        hooks = fmt_hooks(r["recognition_hooks_json"])
        if hooks:
            lines.append("- **recognition hooks:**")
            lines.append(hooks)
        devs = fmt_deviations(r["deviations_json"])
        if devs:
            lines.append("- **deviations:**")
            lines.append(devs)
        asr = fmt_asserts(r["acceptance_asserts_json"])
        if asr:
            lines.append("- **acceptance asserts:**")
            lines.append(asr)
        nums = fmt_numerics(r["numerics_json"])
        if nums:
            lines.append("- **numerics:**")
            lines.append(nums)
        if r["deviation_notes"]:
            lines.append(f"- **mapping deviation notes:** {r['deviation_notes']}")
        lines.append("")
    with open(os.path.join(OUT, f"kits-{g}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

# ---- one .jsonl machine render ----------------------------------------------
JSON_ARRAY_FIELDS = [
    "geometry_bands_json", "deviations_json", "recognition_hooks_json",
    "acceptance_asserts_json", "numerics_json", "t4_doors_json",
    "t4_asserts_json", "citations_json",
]
with open(os.path.join(OUT, "vdm2-compendium.jsonl"), "w") as f:
    f.write(json.dumps({
        "_meta": True, "version": VERSION, "corpus_db_md5": db_md5,
        "generated_utc": GEN_UTC, "kit_count": total, "game_count": len(games),
        "source": "corpus.db kit_master view (574) + 6 side-cars + 2 registries (render-layer joins)",
        "mechanism": "Approach B (read-only): joins in the render/query layer; corpus.db never mutated",
        "supersedes": "vdm1-compendium.jsonl (v1.1-verified)",
        "citation_authority": "kit_citations (non-quarantined)",
        "element_field": "court (reconciled, enum-checked); original_element = raw provenance; elem_raw NOT exposed",
        "freeze": {
            "full_585_fingerprint": live_full_585, "full_585_expected": FREEZE_FULL_585,
            "diff_584_fingerprint": live_584_diff, "diff_584_expected": FREEZE_584_DIFF,
            "corpus_db_md5_expected": FREEZE_DB_MD5, "freeze_held": freeze_ok,
        },
        "invariants": counts,
        "registries": {"door_registry": counts["door_registry"],
                       "motion_signature_registry": counts["motion_signature_registry"]},
        "note": "*_json fields parsed to arrays for machine consumers; side-cars aggregated per-kit "
                "(json_group_array) so membership stays 574 with no per-skill explosion",
    }, ensure_ascii=False, separators=(",", ":")) + "\n")
    for r in rows:
        obj = dict(r)
        for jf in JSON_ARRAY_FIELDS:
            if jf in obj:
                key = jf[:-5] if jf.endswith("_json") else jf  # strip _json suffix for the array key
                obj[key] = parse_arr(obj.pop(jf))
        f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")

# ---- registries.md ----------------------------------------------------------
reg = []
reg.append("# VDM-2 Compendium — Registries (global reference)")
reg.append("")
reg.append(f"> **{VERSION}** · db md5 `{db_md5}` · generated {GEN_UTC}. Read-only render of the two "
           "global registries the per-kit blocks reference. `door_registry` resolves each kit's "
           "`mapping_json.t4_doors` tokens; `motion_signature_registry` resolves each skill band's "
           "`motion_signature`.")
reg.append("")
reg.append(f"## door_registry ({len(doors)})")
reg.append("")
reg.append("| door_name | status | rfc_ref | description |")
reg.append("|---|---|---|---|")
for d in doors:
    reg.append(f"| `{d['door_name']}` | {d['door_status']} | {d.get('rfc_ref') or '—'} | "
               f"{(d.get('description') or '').replace(chr(10), ' ')} |")
reg.append("")
reg.append(f"## motion_signature_registry ({len(motions)})")
reg.append("")
reg.append("| signature_name | engine_impl_ref | description |")
reg.append("|---|---|---|")
for m in motions:
    reg.append(f"| `{m['signature_name']}` | {m.get('engine_impl_ref') or '—'} | "
               f"{(m.get('description') or '').replace(chr(10), ' ')} |")
reg.append("")
with open(os.path.join(OUT, "registries.md"), "w") as f:
    f.write("\n".join(reg) + "\n")

# ---- README index -----------------------------------------------------------
readme = []
readme.append("# VDM-2 COMPENDIUM — the enriched one-representation render")
readme.append("")
readme.append(f"> **STATUS:** CURRENT ({VERSION}). Generated {GEN_UTC} FROM the `corpus.db` `kit_master` "
              f"view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries. "
              f"**db md5 `{db_md5}`.**")
readme.append("")
readme.append("**Authority:** post-VDM-2, `corpus.db` + this compendium GOVERN. This is the v2.0 "
              "successor to the VDM-1 compendium (`research/vdm1/compendium/`, `v1.1-verified`, which "
              "stays recoverable in git + on disk). The VDM-2 lap re-emitted all 267 record-class kits "
              "into six per-kit/per-skill side-car blocks + 2 registries; this render surfaces that "
              "structure per-kit alongside the VDM-1 identity/mapping/citation/verify surface.")
readme.append("")
readme.append("**Mechanism (Approach B — freeze-cleanest):** the six-side-car joins happen in the "
              "RENDER LAYER (this gen script), NOT in the DB. `corpus.db` is never mutated — no view "
              "redef, no DDL, no data touch. The multi-row-per-kit side-cars are aggregated via "
              "correlated subqueries + `json_group_array` (the same pattern `kit_master` already uses "
              "for citations), so the surface stays EXACTLY 574 rows with no per-skill explosion. "
              "canon_corpus data columns stay frozen.")
readme.append("")
readme.append(f"**Freeze proof (measured at gen time):** full-585 fingerprint `{live_full_585}` "
              f"(expected `{FREEZE_FULL_585}`) · 584-differential `{live_584_diff}` "
              f"(expected `{FREEZE_584_DIFF}`) · corpus.db md5 `{db_md5}` "
              f"(expected `{FREEZE_DB_MD5}`) · **freeze held: {freeze_ok}**.")
readme.append("")
readme.append("**Invariants (measured):** "
              f"canon_corpus {counts['canon_corpus']} / kit_master {counts['kit_master']} / "
              f"is_system {counts['is_system']} · "
              f"skill_geometry_band {counts['skill_geometry_band']} / "
              f"kit_deviation {counts['kit_deviation']} / recognition_hook {counts['recognition_hook']} / "
              f"kit_acceptance_assert {counts['kit_acceptance_assert']} / "
              f"kit_delta_t4 {counts['kit_delta_t4']} / kit_numeric {counts['kit_numeric']} · "
              f"kit_door_arg {counts['kit_door_arg']} (carved out — untouched) · "
              f"verify_ledger {counts['verify_ledger']} · "
              f"door_registry {counts['door_registry']} / "
              f"motion_signature_registry {counts['motion_signature_registry']}.")
readme.append("")
readme.append(f"**Contents:** {total} kits · {len(games)} games · per-game `.md` + "
              "`vdm2-compendium.jsonl` (machine render) + `registries.md` (the two global reference tables).")
readme.append("")
readme.append("| game | kits | file |")
readme.append("|---|---|---|")
for g in sorted(games, key=lambda x: (-game_counts[x], x)):
    readme.append(f"| {g} | {game_counts[g]} | [`kits-{g}.md`](kits-{g}.md) |")
readme.append(f"| **TOTAL** | **{total}** | `vdm2-compendium.jsonl` |")
readme.append("")
readme.append("**Regeneration:** `python3 research/scripts/vdm2_compendium_gen_2026_07_22.py` "
              "(read-only on `corpus.db`; re-stamps the md5).")
readme.append("")
readme.append("**Provenance-cleanliness:** `court` (reconciled, enum-checked) is the surfaced element "
              "field; `original_element` carries raw provenance (reversibility). Raw mobile-era "
              "descriptors (`elem_raw`, suffix raws) are NOT exposed (provenance-only, VDM-1 law held). "
              "`kit_citations` is the sole citation authority (`canon_corpus.source_urls` DEPRECATED-frozen).")
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("\n".join(readme) + "\n")

# ---- console report + integrity asserts -------------------------------------
print(f"VDM-2 COMPENDIUM generated: {total} kits, {len(games)} games")
print(f"  mechanism: Approach B (read-only render-layer joins)")
print(f"  db md5: {db_md5} (expected {FREEZE_DB_MD5}, held={db_md5 == FREEZE_DB_MD5})")
print(f"  freeze full-585:  {live_full_585} (expected {FREEZE_FULL_585}, held={live_full_585 == FREEZE_FULL_585})")
print(f"  freeze 584-diff:  {live_584_diff} (expected {FREEZE_584_DIFF}, held={live_584_diff == FREEZE_584_DIFF})")
print(f"  per-game .md: {len(games)} files + registries.md + README.md")
print(f"  jsonl: vdm2-compendium.jsonl ({total} kit lines + 1 meta line)")
print(f"  invariants: {counts}")
print(f"  out dir: {OUT}")

# jsonl line count == total + 1 meta
with open(os.path.join(OUT, "vdm2-compendium.jsonl")) as f:
    n = sum(1 for _ in f)
print(f"  jsonl line count = {n} (expect {total+1})")
assert n == total + 1, f"jsonl line count {n} != {total+1}"
assert total == counts["kit_master"], f"render row count {total} != kit_master {counts['kit_master']}"
assert counts["kit_master"] == 574, f"kit_master {counts['kit_master']} != 574 (membership breach)"
assert counts["kit_door_arg"] == 0, f"kit_door_arg {counts['kit_door_arg']} != 0 (out-of-scope table touched)"
assert freeze_ok, ("FREEZE BREACH: one of full-585 / 584-diff / corpus.db-md5 moved — "
                   f"full585={live_full_585==FREEZE_FULL_585} diff584={live_584_diff==FREEZE_584_DIFF} "
                   f"dbmd5={db_md5==FREEZE_DB_MD5}")
print("  integrity asserts OK (574 membership · jsonl line count · kit_door_arg=0 · freeze held)")
