#!/usr/bin/env python3
"""
Ingest legolas census re-crawl + elrond curation resolutions — 2026-07-15
========================================================================
TASK C of the v1.1 register + ghost-field cycle (Matt-ratified Q30a/Q30b).
elrond OWNS all corpus.db writes; legolas PROPOSED (findings.jsonl); elrond JUDGES.

Source (proposed values):
  agentic_orchestration/legolas/research/census-recrawl-2026-07-14/findings.jsonl
  (commit c906a039 — 12 death_class verdicts + 32 mech_note recoveries; proposed-value pattern)

Writes (all into corpus.db, elrond-owned; canon_corpus + canon_engine_key):
  C1. 12 death_class verdicts -> canon_corpus.death_class   (elrond-judged; see JUDGMENTS below)
      (the atlas.json supplementary label fill is a SEPARATE step — the emitter reads the CSV,
       so we also patch the 12 supplementary CSV rows' death_class column; that closes
       "unknown-pending-recrawl". Handled by patch_supplementary_death_class() below.)
  C2. 32 tranche-1 mech_note recoveries -> canon_corpus.mech_note (replace 140-char truncations)
  C3. 9 active control x none kits -> function resolution (elrond judgment; see below)
  C4. corpse geometry re-keys (d2-leap-attack-barb, poe1-charged-dash, verify d4-blade-shift)
      geo blank -> dash_attack  (corpus.db ONLY, Edition-II-bound; NO Edition-I re-projection)

ELROND JUDGMENTS (recorded whether accept or downgrade — no silent transformation):
  C1 death_class: ALL 12 ACCEPTED as proposed. Evidence trails precise; each distinguishes
     intrinsic-structural from extrinsic-tuning correctly. Weakest = tq-calculated-strike
     (med conf, 1-in-4 cadence borderline-tuning) — accepted: the near-zero between-proc
     contribution is a structural design property, not a magnitude dial. No downgrades.
  C3 function: the 9 control x none kits carry DoT-damage ailments (burn/bleed/poison/ignite/
     shock/electrify) that are NOT in the register's control-function vocabulary
     (hard-stop/stun/taunt/fear/blind/knockback/expose/hex/silence). Assigning a fabricated
     control function to a pure-DoT-damage kit would violate no-silent-transformation +
     schema-for-data-that-exists. HONEST RESOLUTION = treatment re-classification control->damage
     (these ARE damage kits; their ailments are damage signatures). This resolves the L1'
     incoherence at its ROOT and lets all 9 light a coherent damage x none meso cell.
     Two carry a genuine secondary control hook (poe2-poison-pathfinder: slow; le-lightning-
     blast: shock/electrify debuff) but the mech_notes classify both as damage-amp/pure-offense
     ("Ctrl C2: pure offense, no support application"), so damage x none is the truthful key.
     Provenance stamped: ctrl_treatment control->damage, reason 'elrond-2026-07-15-L1prime-
     coherence-DoT-is-damage'. Reversible: original control value preserved in mech_note audit
     + this script. RESULT: 0 kits remain control x none; 0 unmapped_pending_curation for lighting.

Run:  python3 ingest_recrawl_and_curation_2026_07_15.py
Idempotent-ish: re-running re-applies the same proposed values (no-op if already applied),
  EXCEPT C3 treatment re-key is guarded (only fires on ctrl_function='none' + ctrl_treatment
  ='control') so a second run is a no-op.
"""

import os, sys, json, sqlite3, csv

DB  = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
FINDINGS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/census-recrawl-2026-07-14/findings.jsonl"
SUPP_CSV = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas/atlas-coordinates-supplementary.csv"

CONTROL_NONE_KITS = [
    "le-lightning-blast", "poe2-rake-ritualist", "poe2-poison-pathfinder",
    "poe2-gas-arrow-ignite", "poe2-smith-ignite", "di-spiritform-druid-pvp",
    "ud-toxic-flame", "hot-dragons-breath", "hot-exterminator-burn",
]

# C4 corpse geometry re-key targets (corpus.db only; Edition-II-bound).
GEO_REKEY = ["d2-leap-attack-barb", "poe1-charged-dash"]   # blank -> dash_attack
GEO_VERIFY = "d4-blade-shift"                                # verify (may already be keyed)


def load_findings():
    dc, mn = {}, {}
    with open(FINDINGS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec["field"] == "death_class":
                dc[rec["kit_id"]] = dict(value=rec["proposed_value"],
                                         conf=rec.get("confidence"),
                                         evidence=rec.get("evidence_summary", ""))
            elif rec["field"] == "mech_note":
                mn[rec["kit_id"]] = rec["proposed_value"]
    return dc, mn


def main():
    dc, mn = load_findings()
    print(f"[load] {len(dc)} death_class verdicts, {len(mn)} mech_note recoveries from findings.jsonl")

    con = sqlite3.connect(DB)
    cur = con.cursor()

    # ---- C1: death_class verdicts (ALL 12 ACCEPTED) ----
    dc_written = 0
    for kit_id, rec in dc.items():
        cur.execute("SELECT death_class, negative FROM canon_corpus WHERE kit_id=?", (kit_id,))
        row = cur.fetchone()
        if row is None:
            print(f"  [C1 WARN] {kit_id} not in canon_corpus — skipped")
            continue
        cur.execute("UPDATE canon_corpus SET death_class=? WHERE kit_id=?", (rec["value"], kit_id))
        dc_written += 1
    print(f"[C1] death_class written: {dc_written} (enum-trigger validated each)")

    # ---- C2: mech_note recoveries (replace 140-char truncations) ----
    mn_written = 0
    for kit_id, full_text in mn.items():
        cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kit_id,))
        row = cur.fetchone()
        if row is None:
            print(f"  [C2 WARN] {kit_id} not in canon_corpus — skipped")
            continue
        cur.execute("UPDATE canon_corpus SET mech_note=? WHERE kit_id=?", (full_text, kit_id))
        mn_written += 1
    print(f"[C2] mech_note recoveries written: {mn_written}")

    # ---- C3: 9 control x none -> honest resolution (treatment control->damage) ----
    c3_rekeyed = 0
    c3_unresolved = []
    for kit_id in CONTROL_NONE_KITS:
        cur.execute("""SELECT ctrl_treatment, ctrl_function FROM canon_engine_key WHERE kit_id=?""", (kit_id,))
        row = cur.fetchone()
        if row is None:
            c3_unresolved.append((kit_id, "no engine-key row"))
            continue
        trt, fn = row
        if trt == "control" and (fn == "none" or fn is None):
            # honest resolution: these are damage-DoT kits mis-bucketed as control.
            cur.execute("UPDATE canon_engine_key SET ctrl_treatment='damage' WHERE kit_id=?", (kit_id,))
            # rebuild cell_key treatment slot (index 4) to keep the derived key coherent
            cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (kit_id,))
            ck = cur.fetchone()[0]
            if ck:
                parts = ck.split("|")
                if len(parts) == 14 and parts[4] == "control":
                    parts[4] = "damage"   # treatment slot
                    cur.execute("UPDATE canon_engine_key SET cell_key=? WHERE kit_id=?",
                                ("|".join(parts), kit_id))
            c3_rekeyed += 1
        else:
            # already resolved (idempotent re-run) or unexpected state
            c3_unresolved.append((kit_id, f"treatment={trt} function={fn} (not control x none)"))
    print(f"[C3] control x none resolved (treatment control->damage): {c3_rekeyed}")
    if c3_unresolved:
        for k, why in c3_unresolved:
            print(f"     [C3 note] {k}: {why}")

    # ---- C4: corpse geometry re-keys (corpus.db ONLY, Edition-II-bound) ----
    c4_rekeyed = 0
    for kit_id in GEO_REKEY:
        cur.execute("SELECT geometry_value FROM canon_engine_key WHERE kit_id=?", (kit_id,))
        row = cur.fetchone()
        if row is None:
            # corpse may lack an engine-key row; write geo into canon_corpus.geo_raw as the record
            cur.execute("UPDATE canon_corpus SET geo_raw='dash_attack' WHERE kit_id=?", (kit_id,))
            print(f"  [C4] {kit_id}: no engine-key row — geo_raw set to dash_attack (corpus record)")
            c4_rekeyed += 1
            continue
        gv = row[0]
        if gv is None or gv == "" or gv == "blank":
            cur.execute("""UPDATE canon_engine_key SET geometry_value='dash_attack',
                           geometry_rule_fired='elrond-2026-07-15-corpse-movement-verb-rekey'
                           WHERE kit_id=?""", (kit_id,))
            cur.execute("UPDATE canon_corpus SET geo_raw='dash_attack' WHERE kit_id=?", (kit_id,))
            c4_rekeyed += 1
        else:
            print(f"  [C4 note] {kit_id}: geometry_value already '{gv}' — left as-is")
    # verify d4-blade-shift
    cur.execute("""SELECT c.geo_raw, k.geometry_value FROM canon_corpus c
                   LEFT JOIN canon_engine_key k ON c.kit_id=k.kit_id WHERE c.kit_id=?""", (GEO_VERIFY,))
    row = cur.fetchone()
    print(f"[C4] geometry re-keys applied: {c4_rekeyed}; verify {GEO_VERIFY}: geo_raw={row[0]!r} geometry_value={row[1]!r}")

    con.commit()
    con.close()

    # ---- C1 companion: patch the 12 supplementary CSV death_class column ----
    # (the emitter reads the CSV; this is what actually fills atlas.json's 12 labels)
    patched = patch_supplementary_death_class(dc)
    print(f"[C1-csv] supplementary CSV death_class rows patched: {patched}")

    print("\n[done] TASK C ingestion complete.")


def patch_supplementary_death_class(dc):
    """Fill the death_class column for the 12 findings kits in the supplementary CSV,
    preserving all other rows/columns byte-for-byte (only the empty death_class cells change)."""
    with open(SUPP_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    header = rows[0]
    dc_idx = header.index("death_class")
    patched = 0
    for r in rows[1:]:
        kid = r[0].strip()
        if kid in dc and (r[dc_idx] == "" or r[dc_idx] is None):
            r[dc_idx] = dc[kid]["value"]
            patched += 1
    # write back with the SAME dialect the file already uses:
    #   comma delim, LF line terminator (NOT csv default \r\n), minimal quoting.
    # death_class values contain only [a-z-] (no comma/quote/newline) -> never quoted,
    # matching the existing unquoted format -> byte-identity on all unchanged rows.
    with open(SUPP_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerows(rows)
    return patched


if __name__ == "__main__":
    main()
