#!/usr/bin/env python3
"""
Refit-Candidate-1 fit-relative ledger honesty — VERIFY ONLY (no writes).

Reproduces the refit's actual FIT membership (the 628-active point set from
atlas-refit-candidate-1.json) and cross-checks it against the two carried-over
ghost_field ledgers to confirm gandalf's diagnosis, then DERIVES the honest
values. Purely diagnostic; the emission fix is applied by a separate step after
this confirms the numbers.

Provenance: corpus.db (canon_corpus + canon_engine_key) + atlas-refit-candidate-1.json.
Reuses the EXACT predicates from ghost_field_edition2.off_plane_corpus and
ghost_field_refit_candidate_1.lit_map (imported, not reimplemented) where possible.
"""
import json
import os
import sqlite3
import sys

CUR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
SCRIPTS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts"
REFIT_JSON = os.path.join(CUR, "atlas", "atlas-refit-candidate-1.json")
DB = os.path.join(CUR, "corpus.db")

sys.path.insert(0, SCRIPTS)

# ------------------------------------------------------------------ load emission
with open(REFIT_JSON) as f:
    D = json.load(f)
POINTS = D["points"]
GF = D["ghost_field"]
POINT_KIDS = {p["kit_id"] for p in POINTS if "kit_id" in p}
ACTIVE_KIDS = {p["kit_id"] for p in POINTS if not p.get("supplementary")}
SUPP_KIDS = {p["kit_id"] for p in POINTS if p.get("supplementary")}

print("=" * 70)
print("POINT SET (emitted refit)")
print("=" * 70)
print(f"total points        : {len(POINTS)}")
print(f"active points       : {len(ACTIVE_KIDS)}")
print(f"supplementary points: {len(SUPP_KIDS)}")

conn = sqlite3.connect(DB)

# ------------------------------------------------------------------ reproduce fit membership from DB
# The refit stage predicate (per ghost_field_refit_candidate_1.lit_map + the fit-cellkeys snapshot):
#   combat-kit AND cell_key NOT NULL AND negative=0
fit_rows = conn.execute(
    "SELECT k.kit_id FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
    "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL ORDER BY k.kit_id"
).fetchall()
FIT_KIDS = {r[0] for r in fit_rows}
print(f"\nDB-derived fit membership (combat-kit AND cell_key NOT NULL AND negative=0): {len(FIT_KIDS)}")
print(f"  == active points?  {FIT_KIDS == ACTIVE_KIDS}")
only_db = sorted(FIT_KIDS - ACTIVE_KIDS)
only_pts = sorted(ACTIVE_KIDS - FIT_KIDS)
print(f"  in DB-fit not in active points ({len(only_db)}): {only_db[:8]}")
print(f"  in active points not in DB-fit ({len(only_pts)}): {only_pts[:8]}")

# ------------------------------------------------------------------ CURRENT (stale) ledgers
off = GF["off_plane_corpus"]
cur_off_kits = set(off["kits"])
cur_unmapped_kits = set(GF["unmapped_pending_curation_kits"])
print("\n" + "=" * 70)
print("CURRENT (carried-from-E3) LEDGERS — gandalf's diagnosis")
print("=" * 70)
print(f"off_plane_corpus.n={off['n']} gate_rejected_keyed={off['gate_rejected_keyed']} "
      f"kits={len(off['kits'])} n_mcd_total={off['n_mcd_total']} unresolved_no_key={off['unresolved_no_key']}")
print(f"  off kits ∩ point kit_ids : {len(cur_off_kits & POINT_KIDS)} / {len(cur_off_kits)}  "
      f"(defect => ALL 94 on-plane)")
print(f"unmapped_pending_curation={GF['unmapped_pending_curation']} kits={len(cur_unmapped_kits)}")
print(f"  unmapped kits ∩ point kit_ids : {len(cur_unmapped_kits & POINT_KIDS)} / {len(cur_unmapped_kits)}  "
      f"(defect => ALL 114 on-plane)")
# composition of the 114
comp = {}
for k in cur_unmapped_kits:
    g = k.split("-")[0]
    comp[g] = comp.get(g, 0) + 1
print(f"  114 composition by prefix: {dict(sorted(comp.items(), key=lambda x:-x[1]))}")

# ------------------------------------------------------------------ RE-DERIVE off_plane_corpus honestly
# Honest off-plane = corpus rows that are genuinely NOT in the refit fit point set.
# The 26 unresolved_no_key mcd rows have NO engine-key row => never entered the fit.
# The 94 movement-gate keyed mcd rows DO have cell_key => ADMITTED into the fit (they ARE points).
import ghost_field_edition2 as gf2  # noqa: E402
stale_off = gf2.off_plane_corpus(conn)  # the E2/E3 computation (movement-gate view) — for reference
unresolved = set(stale_off["unresolved_no_key_kits"])
gate94 = set(stale_off["kits"])
n_mcd_total = stale_off["n_mcd_total"]

print("\n" + "=" * 70)
print("RE-DERIVATION — honest fit-relative off_plane_corpus")
print("=" * 70)
print(f"n_mcd_total (corpus-level, carries): {n_mcd_total}")
print(f"unresolved_no_key (corpus-level, carries): {len(unresolved)}")
print(f"  26 unresolved ∩ point kit_ids : {len(unresolved & POINT_KIDS)} / {len(unresolved)}  "
      f"(HONEST off-plane => expect 0 overlap)")
print(f"  94 movement-gate keyed ∩ point kit_ids : {len(gate94 & POINT_KIDS)} / {len(gate94)}  "
      f"(ADMITTED => expect 94 overlap)")
# The honest off-plane N for THIS fit = rows not in the fit. Derive from corpus: mcd negative=0
# rows with NO engine-key row (== the 26). Confirm they equal `unresolved`.
no_key_mcd = {r[0] for r in conn.execute(
    "SELECT c.kit_id FROM canon_corpus c WHERE c.game='mcd' AND c.negative=0 "
    "AND c.kit_id NOT IN (SELECT kit_id FROM canon_engine_key)"
).fetchall()}
print(f"  DB: mcd negative=0 with NO engine-key row: {len(no_key_mcd)}  == unresolved? {no_key_mcd == unresolved}")
# broaden: ANY corpus row (any game) genuinely off the fit that the ledger should name?
# The ledger's schema is mcd-scoped (n_mcd_total). Honest off-plane N under this fit = the 26.
honest_off_kits = sorted(no_key_mcd)
print(f"\nHONEST off_plane_corpus values:")
print(f"  gate_rejected_keyed = 0  (the fit's stage gate rejected none of the keyed 94)")
print(f"  n = kits = {len(honest_off_kits)}  (the {len(honest_off_kits)} no-cell-key mcd rows)")
print(f"  n_mcd_total = {n_mcd_total} ; unresolved_no_key = {len(unresolved)}")
print(f"  honest off kits ∩ points : {len(set(honest_off_kits) & POINT_KIDS)}  (must be 0)")

# ------------------------------------------------------------------ RE-DERIVE unmapped_pending_curation
# Under the refit: unmapped = kits in the fit lit-map whose core coords don't map to REG.
# gandalf's diagnosis: all 114 in the E3 ledger are on-plane points now (admitted). Re-derive the
# TRUE pending-curation-unmapped set under the refit's own lit_map.
import ghost_field_refit_candidate_1 as gfr  # noqa: E402
lit_counts, unmapped, unmapped_would_seal, lit_pull, lit_melee = gfr.lit_map(conn)
unmapped = set(unmapped)
print("\n" + "=" * 70)
print("RE-DERIVATION — honest unmapped_pending_curation (refit lit_map)")
print("=" * 70)
print(f"refit lit_map unmapped N = {len(unmapped)}")
print(f"  unmapped ∩ points : {len(unmapped & POINT_KIDS)}")
if unmapped:
    print(f"  remainder list: {sorted(unmapped)}")
else:
    print("  remainder: [] (all admitted — expected 0)")
print(f"  (cross-check) unmapped_would_seal N = {len(unmapped_would_seal)}  "
      f"kits={sorted(unmapped_would_seal)}")

# ------------------------------------------------------------------ 159-new-actives composition
print("\n" + "=" * 70)
print("159 NEW ACTIVES composition (refit 628 vs Edition-I 469)")
print("=" * 70)
e1_active = set()
with open(os.path.join(CUR, "atlas", "atlas-coordinates-active.csv")) as f:
    import csv
    rd = csv.DictReader(f)
    kid_col = "kit_id" if "kit_id" in rd.fieldnames else rd.fieldnames[0]
    for row in rd:
        e1_active.add(row[kid_col])
print(f"E1 active (csv): {len(e1_active)}")
new_actives = ACTIVE_KIDS - e1_active
dropped = e1_active - ACTIVE_KIDS
print(f"new in refit (active - E1): {len(new_actives)}")
print(f"dropped (E1 - active): {len(dropped)}  {sorted(dropped)[:8]}")
# split new by game (mcd gear-grain vs la class-grain vs other)
new_by_game = {}
for k in new_actives:
    g = conn.execute("SELECT game FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()
    g = g[0] if g else "?"
    new_by_game[g] = new_by_game.get(g, 0) + 1
print(f"new actives by game: {dict(sorted(new_by_game.items(), key=lambda x:-x[1]))}")
# how many of the new are the 94 movement-gate mcd gear kits?
new_mcd = new_actives & gate94
print(f"  of new: gear-grain mcd (movement-gate 94 set) present as new points: {len(new_mcd)}")
# LA class-grain among new
new_la = {k for k in new_actives if k.startswith("la-")}
new_la_destroyer = {k for k in new_la if k.startswith("la-destroyer-")}
print(f"  of new: LA total {len(new_la)} (destroyer skill-grain {len(new_la_destroyer)}, "
      f"class-grain {len(new_la) - len(new_la_destroyer)})")

conn.close()
print("\nDONE (verify-only; no writes).")
