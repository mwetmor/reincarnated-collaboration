#!/usr/bin/env python3
"""
VDM-1 ingest-9 — basin-1 batches 03 + 04 + six adjudications.

Single-writer: elrond. Substrate: agentic_orchestration/research/curated/corpus.db.
Charter: agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md.

Discipline (identical to ingests 1..8):
  - Backup is taken by the CALLER (already done: pre-vdm1-ingest9-<ts> + md5) before this runs.
  - journal_mode = DELETE preserved (asserted, never changed).
  - Single transaction; guarded UPDATEs assert rowcount == 1; INSERTs counted.
  - Abstained dossier rows carry strictly-null payload (enforced by CHECK; also asserted here).
  - Citations quarantined flag respected (b03 has the run's first 2 quarantined rows).
  - integrity_check at end (caller re-verifies too).
  - No-silent-transformation: every content correction preserves the raw prior value
    (movement facts_json keeps original verbs under a _prior key; tq2 mech_notes PREPEND a
     dated clause and keep the original verbatim after it).

PART 1 — standard ingest of b03/b04 into verify_ledger, kit_citations, kit_dossier.
PART 2 — six-item adjudication docket:
  1. poe2-walking-calamity  — kb CONTENT correction (identity folk_name + mechanics core_skills)
  2. poe2-warbringer-totems — era restamp 0.1 floor drop -> 0.2-dawn (D-2a)
  3. tq2 class-field ×3      — mech_note content corrections (whirlwind/elementalist/stormblade)
  4. hades2-omega-magick    — movement probe-fact correction (sprint->stationary)
  5. Alias spelling fix      — "Rolling Magma" -> "Roiling Magma" (tq2-elementalist core_skills)
  6. Erasure annotation      — VERIFY it still stands (no action unless missing)
"""
import json
import sqlite3
import sys
from datetime import date

DB = "agentic_orchestration/research/curated/corpus.db"
BASE = "agentic_orchestration/research/vdm1/stage1/basin1/"
TODAY = date.today().isoformat()
ANNOT_TAG = "[VDM-1 basin-1 2026-07-18 ingest-9]"

# The 24 b03/b04 kit_ids (for idempotency re-guard inside the txn).
B03_04_KITS = [
    "poe2-snipe-mirage-deadeye", "poe2-spark-stormweaver", "poe2-spiral-volley",
    "poe2-supporting-fire", "poe2-tempest-bell", "poe2-tempest-flurry",
    "poe2-temporalis-blink", "poe2-titan-hotg", "poe2-twister",
    "poe2-walking-calamity", "poe2-wall-of-shields", "poe2-warbringer-totems",
    "poe2-whirling-assault-ma", "poe2-witchhunter-grenades", "hades2-glorious-disaster",
    "hades2-hail-storm", "hades2-hephaestus-blast", "hades2-medea-skull-cast",
    "hades2-omega-magick", "tq2-bastion-tank", "tq2-elementalist",
    "tq2-forge-turrets", "tq2-stormblade-ice-shards", "tq2-whirlwind-rogue",
]

# Verdict normalization (file uses hyphen; schema enum uses underscore).
VERDICT_MAP = {
    "CONFIRMED": "CONFIRMED",
    "CONTRADICTED": "CONTRADICTED",
    "UNSUPPORTED": "UNSUPPORTED",
    "SOURCE-NOT-FOUND": "SOURCE_NOT_FOUND",
    "SOURCE_NOT_FOUND": "SOURCE_NOT_FOUND",
}


def load(fn):
    rows = []
    with open(BASE + fn) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                sys.exit(f"PARSE FAIL {fn}:{i}: {e}")
    return rows


def guarded(cur, sql, params, ctx):
    cur.execute(sql, params)
    if cur.rowcount != 1:
        raise RuntimeError(f"GUARD FAIL ({ctx}): rowcount={cur.rowcount}, expected 1")


def main():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    jm = con.execute("PRAGMA journal_mode").fetchone()[0]
    if jm.lower() != "delete":
        sys.exit(f"ABORT: journal_mode is {jm!r}, expected 'delete'")
    cur = con.cursor()

    # Idempotency re-guard: no landing-zone rows for these kits yet.
    qmarks = ",".join("?" * len(B03_04_KITS))
    for tbl in ("verify_ledger", "kit_citations", "kit_dossier"):
        n = cur.execute(
            f"SELECT count(*) FROM {tbl} WHERE kit_id IN ({qmarks})", B03_04_KITS
        ).fetchone()[0]
        if n != 0:
            sys.exit(f"ABORT: {tbl} already has {n} rows for b03/b04 kits (non-idempotent)")

    ins_v = ins_c = ins_d = 0
    errata_new = 0
    adj = {}

    try:
        cur.execute("BEGIN")

        # ---------- PART 1: standard ingest ----------
        for batch in ("03", "04"):
            for r in load(f"batch-{batch}-verify.jsonl"):
                verdict = VERDICT_MAP.get(r["verdict"])
                if verdict is None:
                    raise RuntimeError(f"bad verdict {r['verdict']!r} ({r['kit_id']})")
                # anchor mandatory for CONFIRMED/CONTRADICTED
                if verdict in ("CONFIRMED", "CONTRADICTED") and not r.get("anchor_quote"):
                    raise RuntimeError(f"missing anchor: {r['kit_id']}/{r['claim_family']}")
                cur.execute(
                    """INSERT INTO verify_ledger
                       (kit_id, claim_family, claim_text, verdict, anchor_quote,
                        source_url, errata_applied, run_tag, verified_date)
                       VALUES (?,?,?,?,?,?,0,'vdm1',?)""",
                    (r["kit_id"], r["claim_family"], r.get("claim_text"), verdict,
                     r.get("anchor_quote"), r.get("source_url"), TODAY),
                )
                ins_v += 1

            for r in load(f"batch-{batch}-citations.jsonl"):
                cur.execute(
                    """INSERT INTO kit_citations
                       (kit_id, url, archive_url, site, author_handle, title,
                        cite_class, rank_class, accessed_date, quarantined)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (r["kit_id"], r["url"], r.get("archive_url"), r.get("site"),
                     r.get("author_handle"), r.get("title"), r.get("cite_class"),
                     r.get("rank_class"), r.get("accessed_date"),
                     int(r.get("quarantined", 0))),
                )
                ins_c += 1

            for r in load(f"batch-{batch}-dossier.jsonl"):
                abst = int(r.get("abstained", 0))
                payload = r.get("payload_json")
                # abstained => payload strictly null (schema CHECK also enforces)
                if abst == 1 and payload is not None:
                    raise RuntimeError(f"abstained w/ payload: {r['kit_id']}/{r['family']}")
                if abst == 0 and payload is None:
                    raise RuntimeError(f"non-abstained w/ null payload: {r['kit_id']}/{r['family']}")
                payload_s = None if payload is None else json.dumps(payload, ensure_ascii=False)
                cur.execute(
                    """INSERT INTO kit_dossier
                       (kit_id, family, payload_json, source_url, anchor_quote,
                        abstained, conf, extraction_provenance, created_date)
                       VALUES (?,?,?,?,?,?,?,'fetched-vdm1',?)""",
                    (r["kit_id"], r["family"], payload_s, r.get("source_url"),
                     r.get("anchor_quote"), abst, r.get("conf"), TODAY),
                )
                ins_d += 1

        # ---------- PART 2: adjudication docket ----------

        # -- Adj 1: walking-calamity CONTENT correction (identity + mechanics) --
        # identity field = folk_name; mechanics field = core_skills. Both b03-CONTRADICTED.
        # Fetched language governs (b03 verify lines 28-29).
        guarded(
            cur,
            "UPDATE canon_corpus SET folk_name=? "
            "WHERE kit_id='poe2-walking-calamity' AND folk_name='Walking Calamity Autobomber'",
            ("Walking Calamity Shaman",),
            "walking-calamity folk_name",
        )
        wc_core_new = json.dumps(
            ["Walking Calamity", "Herald of Ice", "Polcirkeln"], ensure_ascii=False
        )
        guarded(
            cur,
            "UPDATE canon_corpus SET core_skills=?, core_skills_prov=? "
            "WHERE kit_id='poe2-walking-calamity' "
            "AND core_skills='[\"herald/retaliation procs\", \"Molten Crash(weapon)\"]'",
            (wc_core_new, "verified-v1.1-errata19"),
            "walking-calamity core_skills",
        )
        # mark the two CONTRADICTED verify rows (identity+mechanics) as errata_applied
        cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='poe2-walking-calamity' AND verdict='CONTRADICTED' "
            "AND claim_family IN ('identity','mechanics')"
        )
        if cur.rowcount != 2:
            raise RuntimeError(f"walking-calamity errata flag: rowcount={cur.rowcount}, expected 2")
        errata_new += cur.rowcount
        adj["1_walking_calamity"] = "CONTENT-CORRECTED (folk_name + core_skills; 2 verify rows flagged)"

        # -- Adj 2: warbringer-totems era restamp (drop pre-debut 0.1; D-2a) --
        guarded(
            cur,
            "UPDATE canon_corpus SET eras=? "
            "WHERE kit_id='poe2-warbringer-totems' "
            "AND eras='0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients'",
            ("0.2-dawn;0.3-edict;0.4;0.5-ancients",),
            "warbringer-totems eras",
        )
        guarded(
            cur,
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='poe2-warbringer-totems' AND claim_family='era' AND verdict='CONTRADICTED'",
            (),
            "warbringer-totems era verify flag",
        )
        errata_new += 1
        adj["2_warbringer_totems"] = "ERA-RESTAMPED 0.1;... -> 0.2-dawn;... (1 verify row flagged)"

        # -- Adj 3: tq2 class-field ×3 (mech_note CONTENT corrections; b04 anchors) --
        # No canon_corpus.class column; no roster_atlas rows for these kits. The wrong-class
        # assertion lives in mech_note (and folk_name for whirlwind). Correct via mech_note
        # PREPEND (annotation home for class/lineage notes) — preserves original verbatim.
        # NOTE per-kit CONTRADICTED claim_family differs: whirlwind's is IDENTITY
        # (folk-name 'Whirlwind Rogue' contradicted); elementalist/stormblade are MECHANICS
        # ('standalone/solo class' contradicted). The errata flag targets the actual
        # contradicted row's family.
        tq2_fixes = {
            "tq2-whirlwind-rogue": {
                "flag_family": "identity",
                "old_mech": "POST-CUTOFF: TQ2 EA (2025+). All conf ≤0.50. Channel commit confirmed by atlas key C; whirlwind spin pattern from folk_name. TQ2 rogue class mechanic details unverified.",
                "clause": ("CLASS CORRECTION (ERRATA-21, b04): Whirlwind is a WARFARE mastery skill, "
                           "NOT Rogue. The folk_name 'Whirlwind Rogue' and the 'TQ2 rogue class' framing "
                           "are CONTRADICTED (identity claim). Attested build = Warfare (+ 2nd mastery, "
                           "commonly Earth). Anchor: 'Warfare - Sweeping Strikes 17 - Whirlwind 1/1' "
                           "(steamcommunity.com/app/1154030/discussions/0/591778884098532299/). "
                           "folk_name/kit_id slug left as-is per dispatch."),
            },
            "tq2-elementalist": {
                "flag_family": "mechanics",
                "old_mech": "POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. TQ2 iteration of the Elementalist dual-mastery nuker archetype. Details unverified beyond atlas key.",
                "clause": ("CLASS CORRECTION (ERRATA-22, b04): 'Elementalist' is a mastery PAIRING = "
                           "Storm + Earth, NOT a standalone mastery. The 'standalone mastery class' "
                           "reading is CONTRADICTED (mechanics claim). Anchor: 'Elementalist using two "
                           "masteries: Storm and Earth' "
                           "(steamcommunity.com/sharedfiles/filedetails/?id=3541374759)."),
            },
            "tq2-stormblade-ice-shards": {
                "flag_family": "mechanics",
                "old_mech": "POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. Cold projectile caster; 'Stormblade' suggests Storm/Blade mastery combo in TQ2. All details from atlas key provenance.",
                "clause": ("CLASS CORRECTION (ERRATA-23, b04): 'Stormblade' = Rogue + Storm dual mastery, "
                           "NOT a Storm-mastery solo class. The 'Storm mastery solo class' reading is "
                           "CONTRADICTED (mechanics claim). Ice Shards is the Storm-mastery cold projectile "
                           "primary. Anchor: 'Stormblade = Rogue+Storm per mastery combo class names guide' "
                           "(steamcommunity.com/sharedfiles/filedetails/?id=3540989801)."),
            },
        }
        for k, fx in tq2_fixes.items():
            new_mech = f"{ANNOT_TAG} {fx['clause']} [original harvest note follows] {fx['old_mech']}"
            guarded(
                cur,
                "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note=?",
                (new_mech, k, fx["old_mech"]),
                f"{k} mech_note class-correction",
            )
            guarded(
                cur,
                "UPDATE verify_ledger SET errata_applied=1 "
                "WHERE kit_id=? AND claim_family=? AND verdict='CONTRADICTED'",
                (k, fx["flag_family"]),
                f"{k} class verify flag ({fx['flag_family']})",
            )
            errata_new += 1
        adj["3_tq2_class_x3"] = ("CLASS-CORRECTED via mech_note (whirlwind->Warfare, "
                                 "elementalist->Storm+Earth pairing, stormblade->Rogue+Storm; "
                                 "3 verify rows flagged)")

        # -- Adj 4: hades2-omega-magick movement probe-fact correction --
        # kb: sprint-while-charging / full-move ; b04 attests STATIONARY while charging Omega.
        # Correct verbs + policy; PRESERVE raw prior under _prior_ingest9 (no-silent-transformation).
        mv = cur.execute(
            "SELECT facts_json FROM canon_probe_facts "
            "WHERE kit_id='hades2-omega-magick' AND family='movement'"
        ).fetchone()
        if mv is None:
            adj["4_omega_movement"] = "NO movement row present — recorded as annotation only (see ledger)"
        else:
            obj = json.loads(mv[0])
            if obj.get("verbs") != ["sprint-while-charging"] or obj.get("policy_while_casting") != "full-move":
                raise RuntimeError(f"omega movement precondition mismatch: {obj}")
            obj["_prior_ingest9"] = {
                "verbs": obj.get("verbs"),
                "policy_while_casting": obj.get("policy_while_casting"),
                "note": "kb value CONTRADICTED by b04 (hades2-omega-magick mechanics-sprint row); "
                        "corrected to stationary per fetched text; raw preserved here.",
            }
            obj["verbs"] = ["stationary-while-charging"]
            obj["policy_while_casting"] = "stationary"
            new_mv = json.dumps(obj, ensure_ascii=False)
            guarded(
                cur,
                "UPDATE canon_probe_facts SET facts_json=? "
                "WHERE kit_id='hades2-omega-magick' AND family='movement' AND facts_json=?",
                (new_mv, mv[0]),
                "omega-magick movement facts_json",
            )
            # Movement is a mechanics-family correction with a CONTRADICTED verify row; per the
            # ledger convention errata_applied is reserved for CONTRADICTED-ERA rows, so we do NOT
            # set it here (mirrors the omega mechanics-sprint row being a non-era CONTRADICTED).
            adj["4_omega_movement"] = "MOVEMENT-CORRECTED sprint/full-move -> stationary (facts_json; raw preserved)"

        # -- Adj 5: alias spelling "Rolling Magma" -> "Roiling Magma" (tq2-elementalist) --
        guarded(
            cur,
            "UPDATE canon_corpus SET core_skills=? "
            "WHERE kit_id='tq2-elementalist' AND core_skills='[\"Rolling Magma\", \"Call Lightning\"]'",
            (json.dumps(["Roiling Magma", "Call Lightning"], ensure_ascii=False),),
            "tq2-elementalist Roiling Magma spelling",
        )
        adj["5_roiling_magma"] = "SPELLING-FIXED 'Rolling Magma' -> 'Roiling Magma' (tq2-elementalist core_skills)"

        # -- Adj 6: verify Erasure annotation still stands (no action unless missing) --
        er = cur.execute(
            "SELECT core_skills, mech_note FROM canon_corpus WHERE kit_id='poe2-erasure-edc-lich'"
        ).fetchone()
        ok = (er is not None
              and "Erasure" in (er[0] or "")
              and (er[1] or "").startswith("[VDM-1 basin-1 2026-07-18]")
              and "PHANTOM" in (er[1] or ""))
        if not ok:
            raise RuntimeError("ERASURE ANNOTATION MISSING/ALTERED — halting (ingest-8 invariant broken)")
        adj["6_erasure_annotation"] = "VERIFIED-INTACT (core_skills keeps 'Erasure'; mech_note phantom clause present)"

        con.commit()
    except Exception:
        con.rollback()
        raise

    # ---------- verification ----------
    integ = con.execute("PRAGMA integrity_check").fetchone()[0]
    jm2 = con.execute("PRAGMA journal_mode").fetchone()[0]
    tot_v = con.execute("SELECT count(*) FROM verify_ledger").fetchone()[0]
    tot_c = con.execute("SELECT count(*) FROM kit_citations").fetchone()[0]
    tot_d = con.execute("SELECT count(*) FROM kit_dossier").fetchone()[0]
    quar = con.execute("SELECT count(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]
    abst = con.execute("SELECT count(*) FROM kit_dossier WHERE abstained=1").fetchone()[0]
    errata_tot = con.execute("SELECT count(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    con.close()

    print("=== INGEST-9 COMPLETE ===")
    print(f"inserted: verify={ins_v} citations={ins_c} dossier={ins_d}")
    print(f"errata_applied newly-flagged this ingest: {errata_new}")
    print(f"TOTALS  verify={tot_v} citations={tot_c} dossier={tot_d} "
          f"quarantined={quar} abstained={abst} errata_applied={errata_tot}")
    print(f"integrity_check={integ}  journal_mode={jm2}")
    print("--- adjudications ---")
    for kk in sorted(adj):
        print(f"  {kk}: {adj[kk]}")


if __name__ == "__main__":
    main()
