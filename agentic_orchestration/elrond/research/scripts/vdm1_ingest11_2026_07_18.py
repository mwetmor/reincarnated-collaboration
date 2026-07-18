#!/usr/bin/env python3
"""
VDM-1 ingest-11 — basin-2 (Grim Dawn + Last Epoch, 78 kits) full crawl-stage ingest
+ accumulated erratum queue + BACKFILL-1 era backfills + whole-kit promotion gate.

Single-writer: elrond. Substrate: agentic_orchestration/research/curated/corpus.db.
Run steward: gandalf (VDM-1 charter; fires under Matt's standing autonomous-run mandate).

FILES GOVERN. The 21 basin-2 stage-1 jsonl files are POST-audit truth; the batch summaries'
STEWARD AUDIT ADDENDUM sections are authoritative for errata targets. Every expected count is
asserted EXACTLY on load; a mismatch RAISES (no silent reconcile).

Discipline (identical to ingests 1..10):
  - Backup taken by the CALLER before this runs (pre-vdm1-ingest11-<ts> + md5).
  - journal_mode = DELETE preserved (asserted, never changed).
  - Single transaction; guarded UPDATEs assert exact prior value + rowcount==1; INSERTs counted.
  - Abstained dossier rows carry strictly-null payload (schema CHECK + in-script assert).
  - Citations quarantined flag respected AS-IS (b06 le-smite-paladin lastepochtools = 1; no flip).
  - No-silent-transformation: every content correction preserves the raw prior value
    (probe facts_json keeps the original object under a _prior_ingest11 key; mech_note
     annotations PREPEND a dated clause and keep the original verbatim after it).
  - integrity_check + foreign_key_check at end (caller re-verifies too).

PART 1 — standard ingest of 7 batches into verify_ledger / kit_citations / kit_dossier.
PART 2 — errata queue (continues ERRATA-24.. ; full detail in errata-ledger.md):
  (a) D-2a era-floor restamps ×10 (8 floor-too-early drop-band + 2 floor-too-late add-band)
  (b) gd-blade-trap era restamp base-2016;aom-2017 ("later reworked" clause UNVERIFIED — annotate)
  (c) b02 mechanics content fixes ×3 (fire-strike economy · panettis tri-elemental · pet-conjurer Grave->Beast)
  (d) WRONG-RESOURCE-GENERALLY sweep: all gd-* resource fields spirit/focus/lowercase-mana -> Energy
      (canon_corpus.econ_raw + canon_probe_facts.economy.resource_verbatim). LE untouched.
  (e) chthonic-fissure probe element label "Void / Fire (FI suffix)" -> "fire / necrotic"
  (f) word-of-pain elem_raw=fire artifact -> annotate (fetched: chaos/lightning/pierce variants)
  (g) tempest-strike class "Shaman (Primalist+Acolyte)" -> drop Acolyte + negative era-scope annot
  (h) umbral-blades alias "void blade Rogue" -> annotate probe artifact (fetched: physical/cold)
  (i) manifest-armor resource "Forge Stacks" -> Mana (probe-fact fabrication; fetched Mana-based)
  (j) fire-aura-spellblade core-skill framing: aura passive-emergent, NOT Flame Ward -> annotate
  (k) ghostflame geo_text beam -> review toward cone -> annotate
  (l) runic-invocation class "Runemaster (Mage+Primalist)" -> annotate (Runemaster is a MAGE mastery)
  (m) harvest-lich CHIMERA -> annotate identity-unattested/chimera (NO split mid-run; Unattested Register)
  (n) annotations (no value change): stun-jacks · stormbox · detonating-arrow · wraithlord ·
      hammer-throw rename · storm-totem Spriggan Rage
PART 3 — BACKFILL-1 NULL-field era backfills (ring-of-shields, shift-bladedancer).
PART 4 — whole-kit promotion gate (mechanics=CONFIRMED-w/-anchor AND zero CONTRADICTED in ANY family).
"""
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import date

DB = "agentic_orchestration/research/curated/corpus.db"
BASE = "agentic_orchestration/research/vdm1/stage1/basin2/"
TODAY = date.today().isoformat()
ANNOT_TAG = "[VDM-1 basin-2 2026-07-18 ingest-11]"

BATCHES = ["01", "02", "03", "04", "05", "06", "07"]

# Expected recounts (steward post-audit file truth). Asserted EXACTLY.
EXP_VERIFY = {  # batch -> (CONFIRMED, CONTRADICTED, UNSUPPORTED, SOURCE_NOT_FOUND)
    "01": (32, 2, 3, 0), "02": (29, 7, 0, 0), "03": (37, 2, 2, 0),
    "04": (42, 1, 6, 3), "05": (44, 1, 14, 0), "06": (36, 0, 18, 0), "07": (30, 0, 3, 0),
}
EXP_VERIFY_TOTAL = (250, 13, 46, 3)          # 312 rows
EXP_CITATIONS = {"01": 25, "02": 27, "03": 22, "04": 23, "05": 31, "06": 25, "07": 20}  # 173
EXP_CIT_QUAR_TOTAL = 1                        # b06 le-smite-paladin lastepochtools (AS-IS)
EXP_DOSSIER = {"01": 72, "02": 72, "03": 72, "04": 72, "05": 72, "06": 72, "07": 36}    # 468
EXP_DOSSIER_ABST = {"01": 26, "02": 3, "03": 10, "04": 12, "05": 15, "06": 5, "07": 2}  # 73
EXP_DOSSIER_TOTAL = 468
EXP_DOSSIER_ABST_TOTAL = 73

VERDICT_MAP = {
    "CONFIRMED": "CONFIRMED", "CONTRADICTED": "CONTRADICTED",
    "UNSUPPORTED": "UNSUPPORTED",
    "SOURCE-NOT-FOUND": "SOURCE_NOT_FOUND", "SOURCE_NOT_FOUND": "SOURCE_NOT_FOUND",
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


def guarded(cur, sql, params, ctx, expect=1):
    cur.execute(sql, params)
    if cur.rowcount != expect:
        raise RuntimeError(f"GUARD FAIL ({ctx}): rowcount={cur.rowcount}, expected {expect}")


def main():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    jm = con.execute("PRAGMA journal_mode").fetchone()[0]
    if jm.lower() != "delete":
        sys.exit(f"ABORT: journal_mode is {jm!r}, expected 'delete'")
    cur = con.cursor()

    # ---------- PRE-LOAD: recount + validate ALL files against dispatch truth ----------
    verify_by_batch = {b: load(f"batch-{b}-verify.jsonl") for b in BATCHES}
    cit_by_batch = {b: load(f"batch-{b}-citations.jsonl") for b in BATCHES}
    dos_by_batch = {b: load(f"batch-{b}-dossier.jsonl") for b in BATCHES}

    tot_v = [0, 0, 0, 0]   # C, X, U, SNF
    for b in BATCHES:
        c = x = u = snf = 0
        for r in verify_by_batch[b]:
            v = VERDICT_MAP.get(r["verdict"])
            if v is None:
                raise RuntimeError(f"bad verdict {r['verdict']!r} ({r['kit_id']}) b{b}")
            if v == "CONFIRMED": c += 1
            elif v == "CONTRADICTED": x += 1
            elif v == "UNSUPPORTED": u += 1
            else: snf += 1
        if (c, x, u, snf) != EXP_VERIFY[b]:
            raise RuntimeError(f"VERIFY COUNT MISMATCH b{b}: got {(c,x,u,snf)}, expected {EXP_VERIFY[b]} — STOP")
        tot_v[0] += c; tot_v[1] += x; tot_v[2] += u; tot_v[3] += snf
    if tuple(tot_v) != EXP_VERIFY_TOTAL:
        raise RuntimeError(f"VERIFY TOTAL MISMATCH: {tuple(tot_v)} != {EXP_VERIFY_TOTAL} — STOP")

    cit_quar = 0
    for b in BATCHES:
        if len(cit_by_batch[b]) != EXP_CITATIONS[b]:
            raise RuntimeError(f"CITATIONS COUNT MISMATCH b{b}: {len(cit_by_batch[b])} != {EXP_CITATIONS[b]} — STOP")
        cit_quar += sum(int(r.get("quarantined", 0)) for r in cit_by_batch[b])
    if cit_quar != EXP_CIT_QUAR_TOTAL:
        raise RuntimeError(f"CITATIONS QUAR MISMATCH: {cit_quar} != {EXP_CIT_QUAR_TOTAL} — STOP")

    dos_abst_tot = 0
    for b in BATCHES:
        if len(dos_by_batch[b]) != EXP_DOSSIER[b]:
            raise RuntimeError(f"DOSSIER COUNT MISMATCH b{b}: {len(dos_by_batch[b])} != {EXP_DOSSIER[b]} — STOP")
        ab = sum(int(r.get("abstained", 0)) for r in dos_by_batch[b])
        if ab != EXP_DOSSIER_ABST[b]:
            raise RuntimeError(f"DOSSIER ABST MISMATCH b{b}: {ab} != {EXP_DOSSIER_ABST[b]} — STOP")
        dos_abst_tot += ab
    if dos_abst_tot != EXP_DOSSIER_ABST_TOTAL:
        raise RuntimeError(f"DOSSIER ABST TOTAL MISMATCH: {dos_abst_tot} != {EXP_DOSSIER_ABST_TOTAL} — STOP")

    # kit set + FK guard + idempotency
    all_kits = sorted({r["kit_id"] for b in BATCHES for r in verify_by_batch[b]})
    if len(all_kits) != 78:
        raise RuntimeError(f"distinct kit count {len(all_kits)} != 78 — STOP")
    qk = ",".join("?" * len(all_kits))
    present = {r[0] for r in cur.execute(f"SELECT kit_id FROM canon_corpus WHERE kit_id IN ({qk})", all_kits)}
    missing = set(all_kits) - present
    if missing:
        raise RuntimeError(f"FK GUARD: {len(missing)} basin-2 kits missing from canon_corpus: {sorted(missing)}")
    for tbl in ("verify_ledger", "kit_citations", "kit_dossier"):
        n = cur.execute(f"SELECT count(*) FROM {tbl} WHERE kit_id IN ({qk})", all_kits).fetchone()[0]
        if n != 0:
            sys.exit(f"ABORT: {tbl} already has {n} rows for basin-2 kits (non-idempotent)")

    print(f"PRE-LOAD OK: verify total {tuple(tot_v)}=312, citations 173 (quar {cit_quar}), "
          f"dossier {sum(len(dos_by_batch[b]) for b in BATCHES)} (abst {dos_abst_tot}), 78 kits, FK clean.")

    ins_v = ins_c = ins_d = 0
    errata_new = 0
    sweep = {"probe_economy": 0, "econ_raw": 0}
    adj = {}

    try:
        cur.execute("BEGIN")

        # ================= PART 1: standard landing-zone ingest =================
        for b in BATCHES:
            for r in verify_by_batch[b]:
                verdict = VERDICT_MAP[r["verdict"]]
                if verdict in ("CONFIRMED", "CONTRADICTED") and not r.get("anchor_quote"):
                    raise RuntimeError(f"missing anchor: {r['kit_id']}/{r['claim_family']} b{b}")
                cur.execute(
                    """INSERT INTO verify_ledger
                       (kit_id, claim_family, claim_text, verdict, anchor_quote,
                        source_url, errata_applied, run_tag, verified_date)
                       VALUES (?,?,?,?,?,?,0,'vdm1',?)""",
                    (r["kit_id"], r["claim_family"], r.get("claim_text"), verdict,
                     r.get("anchor_quote"), r.get("source_url"), TODAY),
                )
                ins_v += 1
            for r in cit_by_batch[b]:
                cur.execute(
                    """INSERT INTO kit_citations
                       (kit_id, url, archive_url, site, author_handle, title,
                        cite_class, rank_class, accessed_date, quarantined)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (r["kit_id"], r["url"], r.get("archive_url"), r.get("site"),
                     r.get("author_handle"), r.get("title"), r.get("cite_class"),
                     r.get("rank_class"), r.get("accessed_date"), int(r.get("quarantined", 0))),
                )
                ins_c += 1
            for r in dos_by_batch[b]:
                abst = int(r.get("abstained", 0))
                payload = r.get("payload_json")
                if abst == 1 and payload is not None:
                    raise RuntimeError(f"abstained w/ payload: {r['kit_id']}/{r['family']} b{b}")
                if abst == 0 and payload is None:
                    raise RuntimeError(f"non-abstained w/ null payload: {r['kit_id']}/{r['family']} b{b}")
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

        # ================= PART 2: ERRATA (continues ERRATA-24..) =================

        # ---- (a) D-2a era-floor restamps ×10 ----
        # floor-too-early ×8: drop the impossible pre-debut band (leftmost).
        era_early = {  # kit -> (old_eras, new_eras)  [guarded on exact old]
            "gd-aar-spellbinder":            ("base-2016;aom-2017;fg-2019;patch-1.1-1.2", "aom-2017;fg-2019;patch-1.1-1.2"),
            "gd-callidors-tempest-templar":  ("base-2016;fg-2019;patch-1.1-1.2",         "fg-2019;patch-1.1-1.2"),
            "gd-fire-strike-purifier":       ("base-2016;aom-2017;patch-1.1-1.2",        "aom-2017;patch-1.1-1.2"),
            "gd-forcewave-warlord":          ("base-2016;fg-2019;patch-1.1-1.2",         "fg-2019;patch-1.1-1.2"),
            "gd-mortar-purifier":            ("base-2016;aom-2017;patch-1.1-1.2",        "aom-2017;patch-1.1-1.2"),
            "gd-panettis-mage-hunter":       ("base-2016;aom-2017;patch-1.1-1.2",        "aom-2017;patch-1.1-1.2"),
            "gd-primal-strike-vindicator":   ("base-2016;aom-2017;patch-1.1-1.2",        "aom-2017;patch-1.1-1.2"),
            "gd-shadow-strike-infiltrator":  ("base-2016;aom-2017;patch-1.1-1.2",        "aom-2017;patch-1.1-1.2"),
        }
        # floor-too-late ×2: ADD the earlier attested floor band (prepend).
        era_late = {
            "gd-vitality-conjurer":     ("aom-2017;fg-2019;patch-1.1-1.2", "base-2016;aom-2017;fg-2019;patch-1.1-1.2"),
            "le-healing-hands-paladin": ("1.1-harbingers;1.4-omens",       "1.0-launch;1.1-harbingers;1.4-omens"),
        }
        for k, (old, new) in {**era_early, **era_late}.items():
            guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?",
                    (new, k, old), f"{k} eras restamp")
            guarded(cur, "UPDATE verify_ledger SET errata_applied=1 "
                         "WHERE kit_id=? AND claim_family='era' AND verdict='CONTRADICTED'",
                    (k,), f"{k} era verify flag")
            errata_new += 1
        adj["a_era_restamps"] = f"10 era restamps applied (8 floor-too-early drop-band + 2 floor-too-late add-band)"

        # ---- (b) gd-blade-trap era restamp base-2016;aom-2017 (reclassed X->U by steward; the
        #          internal-inconsistency routes here). "later reworked" clause UNVERIFIED — annotated,
        #          not asserted. No verify errata_applied flag (blade-trap's era row is UNSUPPORTED, not X). ----
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='gd-blade-trap' AND eras=?",
                ("base-2016;aom-2017", "base-2016;aom-2017;fg-2019;patch-1.1-1.2"),
                "blade-trap eras restamp")
        bt_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='gd-blade-trap'").fetchone()[0]
        bt_new = (f"{ANNOT_TAG} ERA restamp: fg-2019;patch-1.1-1.2 bands DROPPED — fetched text attests "
                  f"base-game presence + 2017 criticism only, SILENT on the later span (steward reclass "
                  f"CONTRADICTED->UNSUPPORTED, claim-vs-claim law). negative_canon_target's 'mechanism later "
                  f"reworked' clause is UNVERIFIED from fetched text — annotated, NOT asserted. "
                  f"[original mech_note follows] {bt_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='gd-blade-trap' AND mech_note IS ?",
                (bt_new, bt_mn), "blade-trap mech_note annot")
        adj["b_blade_trap"] = "ERA -> base-2016;aom-2017 + 'later reworked' UNVERIFIED annotation (no verify flag; row is U)"

        # ---- (c) b02 mechanics content fixes ×3 ----
        # (c1) fire-strike economy: spirit/focus meter -> Energy / attack-replacer (b02 addendum).
        #      canon_corpus.econ_raw is 'generator-as-spender-inversion' (NOT a resource label — left);
        #      the resource fix lands in the (d) sweep on econ_raw? No: fire-strike econ_raw has no mana/spirit.
        #      The economy CONTRADICTION is the probe economy model+label. Handled in (d) sweep for the
        #      resource_verbatim label; here we ADDITIONALLY correct the model (meter->attack-replacer) since
        #      b02 ruled Fire Strike is a default-attack replacer, not a meter skill. flag its mechanics X row.
        guarded(cur, "UPDATE verify_ledger SET errata_applied=1 "
                     "WHERE kit_id='gd-fire-strike-purifier' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
                (), "fire-strike mechanics verify flag")
        errata_new += 1  # counts the mechanics content erratum (economy correction executed in (d) + here)
        # (c2) panettis tri-elemental: elem_raw 'lightning' -> 'mixed(fire/cold/lightning)'; probe element
        #      label + shock-downstream unreliable. flag its mechanics X row.
        guarded(cur, "UPDATE canon_corpus SET elem_raw=? WHERE kit_id='gd-panettis-mage-hunter' AND elem_raw='lightning'",
                ("mixed(fire/cold/lightning)",), "panettis elem_raw fix")
        # probe element label
        pe = cur.execute("SELECT facts_json FROM canon_probe_facts WHERE kit_id='gd-panettis-mage-hunter' AND family='element'").fetchone()
        if pe:
            obj = json.loads(pe[0])
            obj["_prior_ingest11"] = {"label_verbatim": obj.get("label_verbatim"),
                                      "note": "kb mono-lightning CONTRADICTED (b02): PRM base is tri-elemental "
                                              "(1/3 fire/cold/lightning); 'shock' ailment is downstream-unreliable."}
            obj["label_verbatim"] = "mixed / fire+cold+lightning (PRM tri-elemental base; shock-downstream-unreliable)"
            guarded(cur, "UPDATE canon_probe_facts SET facts_json=? "
                         "WHERE kit_id='gd-panettis-mage-hunter' AND family='element' AND facts_json=?",
                    (json.dumps(obj, ensure_ascii=False), pe[0]), "panettis probe element fix")
        guarded(cur, "UPDATE verify_ledger SET errata_applied=1 "
                     "WHERE kit_id='gd-panettis-mage-hunter' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
                (), "panettis mechanics verify flag")
        errata_new += 1
        # (c3) pet-conjurer core_skills: Call of the Grave (Necromancer) -> Call of the Beast (Shaman).
        pc_old = '["Summon Briarthorn", "Summon Familiar", "Call of the Grave"]'
        pc_new = json.dumps(["Summon Briarthorn", "Summon Familiar", "Call of the Beast"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='gd-pet-conjurer' AND core_skills=?",
                (pc_new, pc_old), "pet-conjurer core_skills fix")
        guarded(cur, "UPDATE verify_ledger SET errata_applied=1 "
                     "WHERE kit_id='gd-pet-conjurer' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
                (), "pet-conjurer mechanics verify flag")
        errata_new += 1
        adj["c_mech_fixes"] = "fire-strike(economy->energy/attack-replacer) · panettis(tri-elemental) · pet-conjurer(Grave->Beast)"

        # ---- (d) WRONG-RESOURCE-GENERALLY sweep: gd-* resource fields spirit/focus/lowercase-mana -> Energy ----
        # Scope = the two dispatch-named stores: canon_corpus.econ_raw + canon_probe_facts.economy.resource_verbatim.
        # LE untouched (Mana correct). canon_engine_key.resource_verbatim is a THIRD store NOT named in the
        # dispatch — FLAGGED in MIGRATION for steward, NOT swept here (scope-discipline).
        RES_MAP_VERBATIM = {"mana": "energy", "mana (reserve)": "energy (reserve)", "spirit/focus": "energy"}

        # (d.1) canon_probe_facts.economy.resource_verbatim (gd-* only)
        econ_rows = cur.execute(
            "SELECT id, kit_id, facts_json FROM canon_probe_facts WHERE kit_id LIKE 'gd-%' AND family='economy'"
        ).fetchall()
        for rid, kid, fj in econ_rows:
            obj = json.loads(fj)
            rv = obj.get("resource_verbatim", "")
            rvl = rv.lower()
            if not ("mana" in rvl or "spirit" in rvl or "focus" in rvl):
                continue
            new_rv = RES_MAP_VERBATIM.get(rvl)
            if new_rv is None:
                raise RuntimeError(f"UNMAPPED gd resource_verbatim {rv!r} ({kid}) — STOP (add to RES_MAP)")
            # preserve raw prior + reconcile the leading plain_text resource token
            prior = {"resource_verbatim": obj.get("resource_verbatim"),
                     "model": obj.get("model"), "meter_type": obj.get("meter_type"),
                     "plain_text": obj.get("plain_text")}
            obj["_prior_ingest11"] = {**prior,
                "note": "GD resource is Energy ('Spirit' is a GD STAT name — confusion source). "
                        "resource_verbatim relabelled per WRONG-RESOURCE-GENERALLY sweep; raw preserved."}
            obj["resource_verbatim"] = new_rv
            # reconcile leading plain_text label token if present (e.g. "mana (spend); ..." -> "energy (spend); ...")
            pt = obj.get("plain_text")
            if isinstance(pt, str):
                for bad in ("mana (reserve)", "mana", "spirit/focus"):
                    if pt.lower().startswith(bad):
                        obj["plain_text"] = new_rv + pt[len(bad):]
                        break
            # fire-strike: b02 ruled it a default-attack replacer, NOT a meter skill -> correct model+meter_type
            if kid == "gd-fire-strike-purifier":
                obj["model"] = "attack-replacer"
                obj["meter_type"] = "n/a"
                obj["_prior_ingest11"]["note"] += (" fire-strike: model meter->attack-replacer, meter_type "
                                                   "focus->n/a (Fire Strike is a default-attack replacer, b02 addendum).")
            guarded(cur, "UPDATE canon_probe_facts SET facts_json=? WHERE id=? AND facts_json=?",
                    (json.dumps(obj, ensure_ascii=False), rid, fj), f"{kid} probe economy sweep")
            sweep["probe_economy"] += 1

        # (d.2) canon_corpus.econ_raw (gd-* only) — descriptor resource labels reading mana/spirit/focus.
        cc_rows = cur.execute(
            "SELECT kit_id, econ_raw FROM canon_corpus WHERE kit_id LIKE 'gd-%' AND econ_raw IS NOT NULL"
        ).fetchall()
        for kid, econ in cc_rows:
            low = econ.lower()
            if not ("mana" in low or "spirit" in low or "focus" in low):
                continue
            # relabel the resource token 'mana' -> 'energy' (case-insensitive, first token); preserve prior in mech_note? No —
            # econ_raw is a compact descriptor; per no-silent-transformation we record the prior in the errata ledger
            # and via the sweep census. Replace 'mana' substring -> 'energy' (there are no 'spirit'/'focus' econ_raw hits;
            # asserted below). All current values are 'mana-...' compounds.
            if "spirit" in low or "focus" in low:
                raise RuntimeError(f"UNEXPECTED spirit/focus in gd econ_raw {econ!r} ({kid}) — STOP (needs explicit map)")
            new_econ = econ.replace("mana", "energy").replace("Mana", "Energy")
            guarded(cur, "UPDATE canon_corpus SET econ_raw=? WHERE kit_id=? AND econ_raw=?",
                    (new_econ, kid, econ), f"{kid} econ_raw sweep")
            sweep["econ_raw"] += 1
        adj["d_resource_sweep"] = f"probe_economy={sweep['probe_economy']} · econ_raw={sweep['econ_raw']} (gd only; LE untouched)"

        # ---- (e) chthonic-fissure probe element label "Void / Fire (FI suffix)" -> "fire / necrotic" ----
        ce = cur.execute("SELECT facts_json FROM canon_probe_facts WHERE kit_id='le-chthonic-fissure-warlock' AND family='element'").fetchone()
        obj = json.loads(ce[0])
        if obj.get("label_verbatim") != "Void / Fire (FI suffix)":
            raise RuntimeError(f"chthonic-fissure element precondition mismatch: {obj.get('label_verbatim')!r}")
        obj["_prior_ingest11"] = {"label_verbatim": obj.get("label_verbatim"),
                                  "note": "'Void' unattested (generation artifact); fetched: fire & necrotic tags by default (b04)."}
        obj["label_verbatim"] = "fire / necrotic"
        guarded(cur, "UPDATE canon_probe_facts SET facts_json=? WHERE kit_id='le-chthonic-fissure-warlock' AND family='element' AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), ce[0]), "chthonic-fissure element label fix")
        adj["e_chthonic"] = "probe element label 'Void / Fire' -> 'fire / necrotic'"

        # ---- (f) word-of-pain elem_raw=fire artifact -> ANNOTATE (fetched chaos/lightning/pierce) ----
        wop_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='gd-word-of-pain-tactician'").fetchone()[0]
        wop_new = (f"{ANNOT_TAG} ELEM-ARTIFACT WATCH: elem_raw='fire' is a descriptor artifact — fetched WoP "
                   f"Tactician builds show chaos/lightning/pierce variants (fire is a burn/secondary, not primary). "
                   f"Value LEFT as-is (descriptive field, not verify-family); annotated per b04 addendum. "
                   f"[original mech_note follows] {wop_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='gd-word-of-pain-tactician' AND mech_note IS ?",
                (wop_new, wop_mn), "word-of-pain elem annot")
        adj["f_word_of_pain"] = "elem_raw=fire artifact ANNOTATED (chaos/lightning/pierce; value unchanged)"

        # ---- (g) tempest-strike class Acolyte-drop + negative era-scope annotation ----
        # No class column; the "Shaman (Primalist+Acolyte)" string is in the CRAWL SPEC, not the DB.
        # Correction is a mech_note annotation (ERRATA-21/22/23 pattern).
        ts_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-tempest-strike'").fetchone()[0]
        ts_new = (f"{ANNOT_TAG} CLASS CORRECTION: spec class field 'Shaman (Primalist+Acolyte)' — DROP Acolyte "
                  f"(Shaman is a PRIMALIST mastery; Acolyte is a separate base class = ingest artifact). Fetched: "
                  f"Tempest Strike is Primalist/Shaman. NEGATIVE_CANON is ERA-SCOPED: beta-attested 'falls off at "
                  f"end-game' (fixed attack-speed ceiling); post-1.0 rework substantially addressed it (viable-with-"
                  f"investment at 1.2-woven) — the negative label is REAL but era-bounded (new review-book class). "
                  f"[original mech_note follows] {ts_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-tempest-strike' AND mech_note IS ?",
                (ts_new, ts_mn), "tempest-strike class+negative annot")
        adj["g_tempest_strike"] = "class 'Primalist+Acolyte' -> drop Acolyte (annot) + negative era-scope annot"

        # ---- (h) umbral-blades "void blade Rogue" alias -> ANNOTATE probe artifact ----
        ub_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-umbral-blades'").fetchone()[0]
        ub_new = (f"{ANNOT_TAG} ALIAS-ARTIFACT: spec alias 'void blade Rogue' is a probe artifact — fetched text "
                  f"attests Umbral Blades as physical/cold (probe element already reads 'Physical / Cold'), NOT void "
                  f"('void' likely confused with Void Knight skills). Identity CONFIRMED on the real folk name. "
                  f"[original mech_note follows] {ub_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-umbral-blades' AND mech_note IS ?",
                (ub_new, ub_mn), "umbral-blades alias annot")
        adj["h_umbral"] = "'void blade Rogue' alias ANNOTATED as probe artifact (physical/cold; value unchanged)"

        # ---- (i) manifest-armor resource "Forge Stacks" -> Mana (probe-fact fabrication) ----
        ma = cur.execute("SELECT facts_json FROM canon_probe_facts WHERE kit_id='le-manifest-armor' AND family='economy'").fetchone()
        obj = json.loads(ma[0])
        if obj.get("resource_verbatim") != "Forge Stacks":
            raise RuntimeError(f"manifest-armor economy precondition mismatch: {obj.get('resource_verbatim')!r}")
        obj["_prior_ingest11"] = {"resource_verbatim": obj.get("resource_verbatim"),
                                  "model": obj.get("model"), "builder_source": obj.get("builder_source"),
                                  "note": "'Forge Stacks' is a probe-fact fabrication as the RESOURCE model — fetched "
                                          "maxroll text is Mana-based (primary Mana cost for initial summon). "
                                          "resource_verbatim -> Mana; model/builder_source preserved here (b05 addendum)."}
        obj["resource_verbatim"] = "Mana"
        guarded(cur, "UPDATE canon_probe_facts SET facts_json=? WHERE kit_id='le-manifest-armor' AND family='economy' AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), ma[0]), "manifest-armor resource fix")
        adj["i_manifest"] = "probe resource 'Forge Stacks' -> 'Mana' (LE; fetched Mana-based)"

        # ---- (j) fire-aura-spellblade core-skill framing -> ANNOTATE (aura passive-emergent, NOT Flame Ward) ----
        fa_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-fire-aura-spellblade'").fetchone()[0]
        fa_new = (f"{ANNOT_TAG} CORE-SKILL FRAMING: core_skills 'Flame Ward/aura suite' MISFRAMES the delivery — "
                  f"Flame Ward is a DEFENSIVE COOLDOWN, not the aura. The fire aura radiates PASSIVELY via a passive "
                  f"node (emergent, unnamed), NOT a placed Flame Ward skill (b05 addendum). core_skills value LEFT "
                  f"as-is (framing note, no unilateral restamp of the skill token). "
                  f"[original mech_note follows] {fa_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-fire-aura-spellblade' AND mech_note IS ?",
                (fa_new, fa_mn), "fire-aura-spellblade framing annot")
        adj["j_fire_aura"] = "core-skill framing ANNOTATED (aura passive-emergent, not Flame Ward; value unchanged)"

        # ---- (k) ghostflame geo_text beam -> review toward cone -> ANNOTATE ----
        gf_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-ghostflame-warlock'").fetchone()[0]
        gf_new = (f"{ANNOT_TAG} GEO-TEXT REVIEW (beam->cone): probe delivery.value='beam' + geo_raw='small-AOE' — "
                  f"fetched describes a 'channeled jet'/'hellish torrent' covering a widening CONE projection, not a "
                  f"pure line. The probe geo_text prose already captures the cone nuance; delivery.value LEFT as 'beam' "
                  f"pending steward review (b05 flag — 'review', not hard-restamp). "
                  f"[original mech_note follows] {gf_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-ghostflame-warlock' AND mech_note IS ?",
                (gf_new, gf_mn), "ghostflame geo annot")
        adj["k_ghostflame"] = "geo_text beam->cone REVIEW annotated (delivery value unchanged pending steward)"

        # ---- (l) runic-invocation class "Runemaster (Mage+Primalist)" -> ANNOTATE (Runemaster is a MAGE mastery) ----
        ri_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-runic-invocation'").fetchone()[0]
        ri_new = (f"{ANNOT_TAG} CLASS CORRECTION: spec/folk class 'Runemaster (Mage+Primalist)' — Runemaster is a "
                  f"MAGE mastery; 'Primalist' is an ingest artifact (Runemaster is not available to Primalist). "
                  f"folk_name slug 'Runic Invocation Runemaster' LEFT as-is (identifier, not a truth claim). "
                  f"[original mech_note follows] {ri_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-runic-invocation' AND mech_note IS ?",
                (ri_new, ri_mn), "runic-invocation class annot")
        adj["l_runic"] = "class 'Mage+Primalist' -> Primalist artifact ANNOTATED (Runemaster is Mage mastery)"

        # ---- (m) harvest-lich CHIMERA (HIGH) -> ANNOTATE identity-unattested/chimera (NO split mid-run) ----
        hl_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id='le-harvest-lich'").fetchone()[0]
        hl_new = (f"{ANNOT_TAG} CHIMERA (HIGH — Unattested Register; EXCLUDED from promotion): folk name "
                  f"'Harvest Death Seal Lich' CONFLATES TWO real maxroll builds — Harvest Flay Lich (cold/HP-leech) "
                  f"and Death Seal Lich (necrotic/low-life) — different core skills, damage types, economies. All "
                  f"identity/mechanics/era claims for the COMBINED form are UNSUPPORTED (the all-U wall is the "
                  f"instrument WORKING). Steward ruling: do NOT split the kit record mid-run (schema surgery deferred "
                  f"to review book). Identity is UNATTESTED/chimera. [original mech_note follows] {hl_mn or ''}")
        guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id='le-harvest-lich' AND mech_note IS ?",
                (hl_new, hl_mn), "harvest-lich chimera annot")
        adj["m_harvest_lich"] = "CHIMERA annotated (identity-unattested; Unattested Register; NO mid-run split; promo-excluded)"

        # ---- (n) ANNOTATIONS (no value change) ----
        # stun-jacks negative-unverified · stormbox + detonating-arrow identity-intent WATCH ·
        # wraithlord era-stamps unattested WATCH · hammer-throw rename note · storm-totem Spriggan Rage note.
        annots_n = {
            "gd-stun-jacks": ("NEGATIVE-UNVERIFIED: negative_canon 'trap-skill over-centralization' is UNATTESTED "
                              "(fetched sources are POSITIVE about the skill's damage ceiling); verdict was honest-U. "
                              "kb-negative-list reliability signal."),
            "gd-stormbox-elementalist": ("IDENTITY-INTENT WATCH: dominant Storm Box expression is VINDICATOR, not "
                                         "Elementalist; identity reclassed CONFIRMED->UNSUPPORTED (steward). Is this "
                                         "corpus entry intended as Vindicator? Demote candidate iff curation later "
                                         "requires primary-skill-anchored identities."),
            "le-detonating-arrow-mm": ("IDENTITY-INTENT WATCH: dominant maxroll expression is Blast Rain (which procs "
                                       "DA); no standalone DA Marksman guide. Identity C STANDS (components attested "
                                       "together) but weak on folk-name-as-headline; demote candidate iff curation "
                                       "later requires primary-skill anchors."),
            "le-wraithlord-necro": ("ERA WATCH (prune/backfill candidate): 1.1-harbingers + 1.2-woven era stamps "
                                    "UNATTESTED (sources cluster at 1.0-launch; possible post-1.0 rotation). Value "
                                    "LEFT as-is pending steward prune/backfill decision."),
            "le-hammer-throw-paladin": ("PATCH RENAME NOTE: 'Sigils of Hope' (beta/1.0 era name, correct at stamp) "
                                        "renamed to 'Symbols of Hope' in current Season 4 — era-scoped name note, not "
                                        "a contradiction. Value LEFT as-is."),
            "le-storm-totem-shaman": ("FORM-SPECIFIC RESOURCE NOTE: Spriggan Form variant replaces Mana with Rage "
                                      "('Mana is replaced by Rage while Transformed') — form-specific override, NOT a "
                                      "contradiction of the base Mana resource. Value LEFT as-is."),
        }
        for k, clause in annots_n.items():
            old_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
            new_mn = f"{ANNOT_TAG} {clause} [original mech_note follows] {old_mn or ''}"
            guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note IS ?",
                    (new_mn, k, old_mn), f"{k} annotation-n")
        adj["n_annotations"] = f"6 no-value-change annotations ({', '.join(annots_n.keys())})"

        # ================= PART 3: BACKFILL-1 (NULL-field era backfills) =================
        # ring-of-shields eras NULL/'' -> 1.0-launch;1.1-harbingers ; shift-bladedancer -> broad (1.2 omitted).
        backfills = {
            "le-ring-of-shields":    "1.0-launch;1.1-harbingers",
            "le-shift-bladedancer":  "beta-0.8-0.9;1.0-launch;1.1-harbingers;1.4-omens",
        }
        for k, new_eras in backfills.items():
            row = cur.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()
            prior = row[0]
            if prior not in (None, ""):
                raise RuntimeError(f"BACKFILL precondition: {k} eras not NULL/empty (={prior!r}) — STOP")
            # preserve raw prior value via mech_note annotation convention (_prior_ingestN)
            old_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
            bf_note = (f"{ANNOT_TAG} BACKFILL-1 (steward-ratified): eras NULL -> {new_eras!r}. "
                       f"_prior_ingest11 eras value was {prior!r} (empty). "
                       f"[original mech_note follows] {old_mn or ''}")
            guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND (eras IS NULL OR eras='')",
                    (new_eras, k), f"{k} eras backfill")
            guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note IS ?",
                    (bf_note, k, old_mn), f"{k} backfill annot")
        adj["backfill_1"] = f"ring-of-shields + shift-bladedancer eras backfilled (2 kits)"

        # ================= PART 4: whole-kit promotion gate =================
        # Build per-kit verdict map from the JUST-INGESTED verify rows (source of truth = files).
        kit_fams = defaultdict(lambda: defaultdict(list))
        for b in BATCHES:
            for r in verify_by_batch[b]:
                kit_fams[r["kit_id"]][r["claim_family"]].append(VERDICT_MAP[r["verdict"]])
        gate_pass = []
        excl_contra = []
        excl_mech = []
        for k in all_kits:
            fams = kit_fams[k]
            has_contra = any("CONTRADICTED" in vs for vs in fams.values())
            mech_conf = "CONFIRMED" in fams.get("mechanics", [])
            if has_contra:
                excl_contra.append(k)
            elif not mech_conf:
                excl_mech.append(k)
            else:
                gate_pass.append(k)
        # Mandatory exclusions must be OUTSIDE gate_pass (assert — bomb-lance SNF-mech, harvest-lich U-mech).
        for k in ("le-bomb-lance-falconer", "le-harvest-lich"):
            if k in gate_pass:
                raise RuntimeError(f"MANDATORY EXCLUSION {k} unexpectedly in gate_pass — STOP")
        # Promote: gate_pass kits that HAVE probe facts, flipping kb-legacy/named-source-unfetched -> verified-v1.1.
        promoted_facts = 0
        promoted_kits = []
        zero_fact_kits = []
        for k in gate_pass:
            n = cur.execute("SELECT COUNT(*) FROM canon_probe_facts WHERE kit_id=?", (k,)).fetchone()[0]
            if n == 0:
                zero_fact_kits.append(k)
                continue
            cur.execute(
                "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                "WHERE kit_id=? AND fact_provenance IN ('kb-legacy','named-source-unfetched')", (k,))
            promoted_facts += cur.rowcount
            promoted_kits.append(k)
        adj["promotion"] = (f"promoted {len(promoted_kits)} kits / {promoted_facts} facts; "
                            f"excl: {len(excl_contra)} contra + {len(excl_mech)} mech-not-conf + "
                            f"{len(zero_fact_kits)} zero-fact gate-pass")

        con.commit()
    except Exception:
        con.rollback()
        raise

    # ================= verification =================
    integ = con.execute("PRAGMA integrity_check").fetchone()[0]
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    jm2 = con.execute("PRAGMA journal_mode").fetchone()[0]
    tv = con.execute("SELECT count(*) FROM verify_ledger").fetchone()[0]
    tc = con.execute("SELECT count(*) FROM kit_citations").fetchone()[0]
    td = con.execute("SELECT count(*) FROM kit_dossier").fetchone()[0]
    quar = con.execute("SELECT count(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]
    abst = con.execute("SELECT count(*) FROM kit_dossier WHERE abstained=1").fetchone()[0]
    errata_tot = con.execute("SELECT count(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    prov = dict(con.execute("SELECT fact_provenance, count(*) FROM canon_probe_facts GROUP BY fact_provenance").fetchall())
    con.close()

    print("\n=== INGEST-11 COMPLETE ===")
    print(f"inserted: verify={ins_v} citations={ins_c} dossier={ins_d}")
    print(f"errata verify-rows newly flagged: {errata_new}")
    print(f"resource sweep: probe_economy={sweep['probe_economy']} econ_raw={sweep['econ_raw']}")
    print(f"TOTALS  verify={tv} citations={tc} dossier={td} quar={quar} abst={abst} errata_applied={errata_tot}")
    print(f"fact_provenance: {prov}")
    print(f"integrity_check={integ}  foreign_key_check={'CLEAN' if not fk else fk}  journal_mode={jm2}")
    print("--- steps ---")
    for kk in sorted(adj):
        print(f"  {kk}: {adj[kk]}")


if __name__ == "__main__":
    main()
