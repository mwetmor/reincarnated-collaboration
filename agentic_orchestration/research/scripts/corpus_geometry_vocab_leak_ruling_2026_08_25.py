#!/usr/bin/env python3
"""Geometry-vocabulary leak ruling — corpus.db kit_mapping.skills[].geometry_value.

Occasioned by: gamora X-1 finding, `simulation/MIGRATION.md` (2026-08-24) — corpus
`kit_mapping` carries `geometry_value` values `mobility` (1) and `knockback` (1) that
exist in NO `_RICH_TO_SPATIAL` site and are absent from `VALID_GEOMETRY_TYPES`;
they silently default to `point` at compile time. Routed to elrond by knight-rider
as a curation judgment call, NOT a patch order.

RULING: (B) CORPUS NOISE, both rows. Neither is legitimate vocabulary the schema
failed to catch up to. Neither is a field SWAP (no second hole in either case).
Detail in `curated/MIGRATION.md` [2026-08-25].

  1. d3-zbarb / skill_ordinal 2 / 'Ancient Spear (Rage Flip rune)'
     'knockback' -> 'vortex_pull'
     AUTHORING TRANSCRIPTION FAILURE. The row's OWN delivery_notes adjudicate the
     contest and terminate in "map per anchor: vortex_pull OR knockback contested;
     dominant loop from skill_loop anchor: 'Ancient Spear Rage Flip pulls enemies'
     -> vortex_pull". The conclusion never reached the field; the LOSING candidate
     was written. Corrected to the value the row itself concluded.

  2. le-frost-wall-rm / skill_ordinal 1 / 'Glacier'
     'mobility' -> NULL (STRUCK)
     MAPPER GLOSS, NOT FETCHED GEOMETRY. The sole anchor is a joint build-utility
     sentence ("Glacier and Frost Wall offer multiple buffs, mobility, and even
     cast Lightning Blast", kit_dossier id 1164) which attests no geometry for
     Glacier at all. No `skill_geometry` dossier section exists for Glacier. Same
     defect class, same convention, and the same correction as the established
     precedent gd-trozan-druid/1 [STEWARD AUDIT 2026-07-18] ("'placed at position'
     was mapper gloss, not fetched" -> struck to null). NULL geometry is an
     ADMITTED, attested state in this corpus (15 skills carry it) and is read as
     Optional[str] by `kit_compiler/kit_reader.py:37`.
     NOT A SWAP: the traversal claim is not displaced or lost — it is already
     correctly housed one grain over at
     `skill_geometry_band(le-frost-wall-rm, 1).delivery_class = 'motion'`.
     geometry_value carried a redundant mis-slotted COPY.

RAW PRESERVED IN-BAND: no destructive edit. Each corrected skill gains a bracketed
`[STEWARD AUDIT 2026-08-25: ...]` block in `delivery_notes` naming the pre-correction
value verbatim (the 34-kit established convention). Reversible from the annotation
alone; also from the timestamped backup.

Idempotent: re-run detects the STEWARD AUDIT marker and no-ops.
Transactional: single commit; asserts PRE and POST.
"""

from __future__ import annotations

import datetime as _dt
import json
import shutil
import sqlite3
import sys
from pathlib import Path

CURATED = Path(__file__).resolve().parent.parent / "curated"
DB = CURATED / "corpus.db"

RUN = "geometry-vocab-leak-ruling-2026-08-25"
STAMP = "STEWARD AUDIT 2026-08-25"
VOTE_RUN = "vfx-archetype-vote-2026-08-23"

# Canonical vocabulary, READ from generation/geometry_derivation.py:43 (rocket's seam,
# read-only). Mirrored here so the sweep is self-contained and the script is a record
# of what the vocabulary WAS at ruling time.
VALID_GEOMETRY_TYPES = frozenset({
    "ground_targeted_circle", "circle", "self_buff", "single_target", "vortex_pull",
    "multi_projectile", "beam_channel", "teleport", "ring", "aura", "line", "cone",
    "melee_strike", "ground_slam", "melee_arc", "chain", "ricochet_bounce",
    "dash_attack", "totem", "defensive_dash", "blink", "fork", "whirlwind",
    "leap_strike", "orbit", "placed_lane",
})

CORRECTIONS = [
    {
        "kit_id": "d3-zbarb",
        "ordinal": 2,
        "from": "knockback",
        "to": "vortex_pull",
        "audit": (
            f"[{STAMP}: geometry_value 'knockback' CORRECTED -> 'vortex_pull'. "
            "Authoring transcription failure at the vdm1 stage-2 lap "
            "(basin3/mapping-batch-09.jsonl, authored 2026-07-18): this note's own "
            "adjudication terminates in '-> vortex_pull' and the field was written with "
            "the losing candidate. No new evidence, no re-crawl; the row is corrected to "
            "the value it already concluded. Raised by gamora X-1 (simulation/MIGRATION.md "
            "2026-08-24) as an out-of-vocabulary geometry_value silently defaulting to "
            "'point'; ruled corpus noise, not a vocabulary extension.]"
        ),
    },
    {
        "kit_id": "le-frost-wall-rm",
        "ordinal": 1,
        "from": "mobility",
        "to": None,
        "audit": (
            f"[{STAMP}: geometry_value 'mobility' STRUCK -> null geometry, per the same "
            "two-lane convention as gd-trozan-druid/1 (STEWARD AUDIT 2026-07-18). "
            "'mobility' is an effect/role noun, never a geometry; it entered the slot as "
            "mapper gloss compressed from the skill_loop SUMMARY. The only fetched anchor "
            "is a JOINT build-utility sentence — 'Glacier and Frost Wall offer multiple "
            "buffs, mobility, and even cast Lightning Blast for additional damage output' "
            "(kit_dossier id 1164) — which attests NO delivery geometry for Glacier, and "
            "no skill_geometry dossier section exists for it. Nothing is lost: the "
            "traversal claim is already housed at skill_geometry_band(le-frost-wall-rm,1)"
            ".delivery_class='motion'. Raised by gamora X-1 (simulation/MIGRATION.md "
            "2026-08-24). NOTE (UNRESOLVED, see vfx_curation_finding F003): that band row's "
            "motion_signature='straight_line' rests on the SAME non-anchor and is not "
            "independently attested; re-band at the next kit-mapping lap.]"
        ),
    },
]

FINDINGS = [
    ("F001", "geometry-vocab-leak-ruled", "INFO", "knockback",
     "kit_mapping.d3-zbarb.skills[2].geometry_value",
     "RULED (B) CORPUS NOISE and CORRECTED to 'vortex_pull'. This discharges the "
     f"disposition proposed by vfx_archetype('knockback', {VOTE_RUN}).fold_note "
     "('re-band the single member at the next kit-mapping lap; if it survives re-banding "
     "it earns a P2 dossier job and a T-A row'). It did NOT survive: the leak is confirmed "
     "at the authoring lap and the row's own notes name the correct value. The archetype "
     "'knockback' therefore has zero remaining members and should NOT be minted as a T-A "
     "row. The vote-run rows (vfx_archetype / vfx_archetype_member) are a SNAPSHOT of the "
     "2026-08-23 measurement and are NOT retro-edited (Law 2); geometry_value_raw preserves "
     "what was measured.", "LOGGED", VOTE_RUN),
    ("F002", "geometry-vocab-leak-ruled", "INFO", None,
     "kit_mapping.le-frost-wall-rm.skills[1].geometry_value",
     "RULED (B) CORPUS NOISE and STRUCK to null geometry. 'mobility' minted no archetype "
     "in the P1 vote because le-frost-wall-rm is one of 49 kit_mapping kits outside the "
     "2026-08-23 vote snapshot (see F004), so no vote-run artifact requires disposition.",
     "LOGGED", VOTE_RUN),
    ("F003", "band-rests-on-non-anchor", "UNRESOLVED", None,
     "skill_geometry_band(le-frost-wall-rm,1).motion_signature",
     "skill_geometry_band(le-frost-wall-rm, ordinal 1, 'Glacier') carries "
     "delivery_class='motion' + motion_signature='straight_line' at band_conf 0.75, "
     "derivation 'dossier-prose', with source_anchor = the SAME prose now struck from "
     "geometry_value. delivery_class='motion' is defensible at low confidence from the "
     "utility sentence; motion_signature='straight_line' is a PATH claim the anchor does "
     "not make. NOT corrected here: correcting it needs a re-band, and re-extraction was "
     "explicitly out of scope for this two-row ruling. Carry to the next kit-mapping lap.",
     "UNRESOLVED", None),
    ("F004", "vote-coverage-delta", "INFO", None,
     "vfx_archetype_member coverage vs kit_mapping",
     "OBSERVED, NOT FIXED, adjacent to this ruling: 49 kits now holding kit_mapping rows "
     "have no vfx_archetype_member row under vote_run "
     f"'{VOTE_RUN}' (kit_mapping 574 kits vs 531 kits in the vote snapshot). Expected for "
     "a snapshot vote, but it means any future census that reads archetype membership as "
     "if it covered the universe will under-count. Named here so it is not rediscovered.",
     "LOGGED", None),
]


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sweep(con: sqlite3.Connection) -> list[tuple[object, int]]:
    """Full out-of-vocabulary census over kit_mapping.skills[].geometry_value."""
    rows = con.execute(
        "SELECT json_extract(s.value,'$.geometry_value') AS gv, COUNT(*) "
        "FROM kit_mapping km, json_each(json_extract(km.mapping_json,'$.skills')) s "
        "GROUP BY gv ORDER BY 2 DESC"
    ).fetchall()
    return [(gv, n) for gv, n in rows]


def report_sweep(label: str, rows) -> None:
    total = sum(n for _, n in rows)
    nulls = sum(n for gv, n in rows if gv is None)
    oov = [(gv, n) for gv, n in rows if gv is not None and gv not in VALID_GEOMETRY_TYPES]
    in_vocab = [(gv, n) for gv, n in rows if gv is not None and gv in VALID_GEOMETRY_TYPES]
    print(f"\n--- {label} SWEEP ---")
    print(f"  kit-skills total          : {total}")
    print(f"  distinct in-vocab values  : {len(in_vocab)} / {len(VALID_GEOMETRY_TYPES)} vocab")
    print(f"  NULL (admitted no-geometry): {nulls}")
    print(f"  OUT-OF-VOCABULARY         : {len(oov)} distinct, {sum(n for _, n in oov)} occurrences")
    for gv, n in oov:
        print(f"      {gv!r}: {n}")
    if not oov:
        print("      (none — exactly zero, sweep clean)")
    return oov


def main() -> int:
    if not DB.exists():
        print(f"FATAL: {DB} not found", file=sys.stderr)
        return 2

    con = sqlite3.connect(DB)
    con.row_factory = None

    # ── Idempotency probe ────────────────────────────────────────────────────
    already = con.execute(
        "SELECT COUNT(*) FROM kit_mapping WHERE kit_id IN ('d3-zbarb','le-frost-wall-rm') "
        "AND mapping_json LIKE ?", (f"%{STAMP}%",)
    ).fetchone()[0]
    if already == len(CORRECTIONS):
        print(f"NO-OP: both rows already carry the '{STAMP}' marker. Re-run is a no-op.")
        report_sweep("CURRENT", sweep(con))
        con.close()
        return 0
    if already != 0:
        print(f"FATAL: partial prior application ({already}/{len(CORRECTIONS)}). Halting.",
              file=sys.stderr)
        con.close()
        return 3

    pre = sweep(con)
    pre_oov = report_sweep("PRE", pre)

    # ── PRE assert: the ruling addresses EXACTLY the leaks the sweep finds ────
    expected = {("mobility", 1), ("knockback", 1)}
    if set(pre_oov) != expected:
        print(f"FATAL: PRE out-of-vocabulary set {set(pre_oov)} != expected {expected}. "
              "The premise changed under the ruling. Halting.", file=sys.stderr)
        con.close()
        return 4

    # ── Backup ───────────────────────────────────────────────────────────────
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = CURATED / f"corpus.db.pre-geomvocab-{ts}-backup"
    con.execute("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(DB, backup)
    print(f"\nBackup: {backup.name}")

    # ── Apply ────────────────────────────────────────────────────────────────
    try:
        con.execute("BEGIN")
        for c in CORRECTIONS:
            raw = con.execute(
                "SELECT mapping_json FROM kit_mapping WHERE kit_id=?", (c["kit_id"],)
            ).fetchone()[0]
            mj = json.loads(raw)
            sk = mj["skills"][c["ordinal"]]
            assert sk["geometry_value"] == c["from"], (
                f"{c['kit_id']}[{c['ordinal']}] geometry_value is "
                f"{sk['geometry_value']!r}, expected {c['from']!r}"
            )
            sk["geometry_value"] = c["to"]
            sk["delivery_notes"] = (sk.get("delivery_notes") or "").rstrip() + " " + c["audit"]
            con.execute(
                "UPDATE kit_mapping SET mapping_json=? WHERE kit_id=?",
                (json.dumps(mj, ensure_ascii=False), c["kit_id"]),
            )
            print(f"  {c['kit_id']}[{c['ordinal']}]: {c['from']!r} -> {c['to']!r}")

        now = _now()
        for fid, kind, sev, arch, subj, detail, status, target in FINDINGS:
            con.execute(
                "INSERT OR REPLACE INTO vfx_curation_finding "
                "(curation_run, finding_id, kind, severity, archetype_id, candidate_rank, "
                " subject, detail, status, raised_at, target_curation_run) "
                "VALUES (?,?,?,?,?,NULL,?,?,?,?,?)",
                (RUN, fid, kind, sev, arch, subj, detail, status, now, target),
            )

        con.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            (RUN, now,
             "Geometry-vocabulary leak ruling (elrond; raised by gamora X-1, routed by "
             "knight-rider). DATA-ONLY, two rows, one field. kit_mapping.skills[]"
             ".geometry_value out-of-vocabulary values RULED (B) CORPUS NOISE: "
             "d3-zbarb[2] 'knockback' -> 'vortex_pull' (the row's own delivery_notes "
             "concluded vortex_pull; the losing candidate was transcribed at the vdm1 "
             "stage-2 lap 2026-07-18); le-frost-wall-rm[1] 'mobility' -> NULL (mapper "
             "gloss off a joint build-utility anchor that attests no geometry; struck per "
             "the gd-trozan-druid/1 two-lane precedent). NEITHER was a field swap: no "
             "second hole. NO vocabulary extension proposed; VALID_GEOMETRY_TYPES (26) and "
             "_RICH_TO_SPATIAL untouched — no ADR-004 cross-seam change owed. Raw values "
             "preserved verbatim in-band via [STEWARD AUDIT 2026-08-25] delivery_notes "
             "blocks. POST sweep: 0 out-of-vocabulary values corpus-wide. Findings logged "
             "to vfx_curation_finding (F001-F004; F003 UNRESOLVED = the frost-wall band's "
             "motion_signature rests on the same non-anchor). Vote-run snapshots NOT "
             "retro-edited. Backup " + backup.name + "."),
        )
        con.commit()
    except Exception:
        con.rollback()
        print("ROLLED BACK", file=sys.stderr)
        raise

    # ── POST assert ──────────────────────────────────────────────────────────
    post_oov = report_sweep("POST", sweep(con))
    ok = len(post_oov) == 0
    zb = con.execute(
        "SELECT json_extract(mapping_json,'$.skills[2].geometry_value') "
        "FROM kit_mapping WHERE kit_id='d3-zbarb'").fetchone()[0]
    fw = con.execute(
        "SELECT json_extract(mapping_json,'$.skills[1].geometry_value') "
        "FROM kit_mapping WHERE kit_id='le-frost-wall-rm'").fetchone()[0]
    print(f"\nPOST asserts: oov_empty={ok} · d3-zbarb[2]={zb!r} · le-frost-wall-rm[1]={fw!r}")
    assert ok and zb == "vortex_pull" and fw is None, "POST assert FAILED"
    print("ALL OK")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
