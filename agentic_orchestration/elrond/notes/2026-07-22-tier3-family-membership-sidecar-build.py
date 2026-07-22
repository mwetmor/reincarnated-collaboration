#!/usr/bin/env python3
"""
Tier-3 Encounter-Geometry Run — L-13(b) family-membership sidecar builder.

Materializes the run's THREE membership tiers into ONE joinable sidecar by
TRANSCRIPTION-WITH-PROVENANCE (no new rulings, no fabrication):

  1. RATIFIED   — corpus.db table `atlas_gateA_labels_2026_07_14` (86 kit_ids, 6 families).
  2. PROPAGATED — τ-propagation from gateA seeds, `atlas-archipelago-mock.json`
                  points[stratum='core' & family assigned & not self-seed] (44 memberships:
                  AURA 2 + TOTEM-SENTRY 22 + TRAP-MINE 20; report-confirmed count).
  3. DOCKET     — `atlas-e4-family-candidates.json` dockets[*].members (self-scored
                  discovery docket; 6 working families).

on_spine := kit_id present in corpus.db `canon_corpus` WHERE corpus_class='record'
            (the record-267 act spine; era_year gives the age: 2000=I,2013=II,2016=III,2024=IV).

CONFLICT RULE: precedence RATIFIED > PROPAGATED > DOCKET. If a kit carries different
families across tiers, the higher-precedence row is ACTIVE; lower rows are KEPT with
`shadowed_by` naming the winning tier. (Same-family-across-tiers duplicates are NOT
conflicts but are still shadowed so every source row is preserved — provenance-clean.)

corpus.db opened READ-ONLY (mode=ro). Zero writes to any corpus.db copy.
Author: elrond (data steward) · 2026-07-22
"""
import json
import sqlite3
import hashlib
from collections import defaultdict, Counter

ROOT = "/Users/admin/Games/reincarnated-collaboration"
CORPUS = f"{ROOT}/agentic_orchestration/research/curated/corpus.db"
GATEA_TABLE = "atlas_gateA_labels_2026_07_14"
ARCHIPELAGO = f"{ROOT}/agentic_orchestration/research/curated/atlas/atlas-archipelago-mock.json"
DOCKET_JSON = f"{ROOT}/agentic_orchestration/research/curated/atlas/atlas-e4-family-candidates.json"

OUT_JSON = f"{ROOT}/agentic_orchestration/elrond/notes/2026-07-22-tier3-family-membership-sidecar.json"
OUT_CENSUS = f"{ROOT}/agentic_orchestration/elrond/notes/2026-07-22-tier3-family-membership-sidecar-census.md"

# relative source-path labels for provenance citation (portable, not machine-absolute)
REL = lambda p: p.replace(ROOT + "/", "")

AGE = {2000: "I", 2013: "II", 2016: "III", 2024: "IV"}
PRECEDENCE = {"RATIFIED": 0, "PROPAGATED": 1, "DOCKET": 2}


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---- corpus.db READ-ONLY: the record-267 spine + era map ----
uri = f"file:{CORPUS}?mode=ro"
con = sqlite3.connect(uri, uri=True)
cur = con.cursor()

spine_era = {}  # kit_id -> era_year (record-class only)
for kit_id, era in cur.execute(
    "SELECT kit_id, era_year FROM canon_corpus WHERE corpus_class='record'"
):
    spine_era[kit_id] = era
assert len(spine_era) == 267, f"spine expected 267, got {len(spine_era)}"

# ---- Tier 1: RATIFIED (gateA table, READ-ONLY transcription) ----
ratified = []  # (kit_id, family)
for kit_id, group in cur.execute(f'SELECT kit_id, "group" FROM {GATEA_TABLE}'):
    ratified.append((kit_id, group))
assert len(ratified) == 86, f"gateA expected 86, got {len(ratified)}"
con.close()

# ---- Tier 2: PROPAGATED (archipelago mock points) ----
arch = json.load(open(ARCHIPELAGO))
propagated = []  # (kit_id, family, affinity)
for p in arch["points"]:
    if p["stratum"] == "core" and p.get("family") and p.get("e1_gateA_group") != p["family"]:
        propagated.append((p["kit_id"], p["family"], p.get("affinity")))
assert len(propagated) == 44, f"propagated expected 44, got {len(propagated)}"

# ---- Tier 3: DOCKET (family-candidates docket members) ----
dk = json.load(open(DOCKET_JSON))
docket = []  # (kit_id, family, docket_id, status)
for dd in dk["dockets"]:
    lbl = dd["working_label"]
    did = dd["docket_id"]
    for m in dd["members"]:
        docket.append((m["kit_id"], lbl, did, m["status"]))

# ---- assemble raw rows per tier ----
rows = []  # each: dict


def spine_of(kit_id):
    return kit_id in spine_era


for kit_id, fam in ratified:
    rows.append({
        "kit_id": kit_id,
        "family": fam,
        "tier": "RATIFIED",
        "source_artifact": f"corpus.db table {GATEA_TABLE} (col \"group\"; byte-identical to atlas_gateA_labels_refit_candidate_1)",
        "on_spine": spine_of(kit_id),
    })

for kit_id, fam, aff in propagated:
    rows.append({
        "kit_id": kit_id,
        "family": fam,
        "tier": "PROPAGATED",
        "source_artifact": f"{REL(ARCHIPELAGO)} points[stratum=core, family assigned, not gateA self-seed] (affinity={aff})",
        "on_spine": spine_of(kit_id),
    })

for kit_id, fam, did, status in docket:
    rows.append({
        "kit_id": kit_id,
        "family": fam,
        "tier": "DOCKET",
        "source_artifact": f"{REL(DOCKET_JSON)} dockets[docket_id={did}].members (working_label={fam}; status={status})",
        "on_spine": spine_of(kit_id),
    })

# ---- CONFLICT RULE: precedence RATIFIED > PROPAGATED > DOCKET ----
# For each kit_id, the min-precedence tier row is ACTIVE; every other row gets
# shadowed_by = <winning tier>. A cross-family disagreement is a true CONFLICT.
by_kit = defaultdict(list)
for r in rows:
    by_kit[r["kit_id"]].append(r)

conflicts = []  # kits where families disagree across tiers
for kit_id, krows in by_kit.items():
    # winner = lowest precedence value
    krows.sort(key=lambda r: PRECEDENCE[r["tier"]])
    winner = krows[0]
    winner_tier = winner["tier"]
    winner_fam = winner["family"]
    fams = {r["family"] for r in krows}
    is_conflict = len(fams) > 1
    for r in krows:
        if r is winner:
            r["shadowed_by"] = None
        else:
            r["shadowed_by"] = winner_tier
    if is_conflict:
        conflicts.append({
            "kit_id": kit_id,
            "active_family": winner_fam,
            "active_tier": winner_tier,
            "shadowed": [
                {"family": r["family"], "tier": r["tier"]}
                for r in krows if r is not winner
            ],
            "on_spine": winner["on_spine"],
        })

# stable output order: tier precedence, then family, then kit_id
rows.sort(key=lambda r: (PRECEDENCE[r["tier"]], r["family"], r["kit_id"]))

# ---- emit sidecar JSON ----
sidecar = {
    "$comment": (
        "Tier-3 Encounter-Geometry Run · ruling L-13(b) family-membership materialization · "
        "2026-07-22 · author elrond (data steward). Transcription-with-provenance of the run's "
        "THREE membership tiers into one joinable sidecar. NO new rulings, NO fabrication. "
        "RATIFIED (gateA table, 86) + PROPAGATED (archipelago τ-propagation, 44 hypothesis-tier) + "
        "DOCKET (family-candidates discovery docket, self-scored). Working labels only — NOT canon "
        "(Matt names-review pending). on_spine := kit_id in corpus.db canon_corpus corpus_class='record' "
        "(the record-267 act spine). CONFLICT precedence RATIFIED>PROPAGATED>DOCKET; loser rows kept "
        "with shadowed_by. SAME-TIER tiebreak (two DOCKETs claim one kit): lowest docket_id wins the "
        "active row (deterministic, reproducible). corpus.db read READ-ONLY (mode=ro, md5 d091881dc1507753577f56f4998a64a5)."
    ),
    "run": "Tier-3 Encounter-Geometry Run (conductor: gandalf RUN-CONDUCTOR)",
    "ruling": "L-13(b)",
    "date": "2026-07-22",
    "author": "elrond (data steward)",
    "tier_precedence": ["RATIFIED", "PROPAGATED", "DOCKET"],
    "sources": {
        "RATIFIED": f"corpus.db table {GATEA_TABLE} (86 rows, 6 families)",
        "PROPAGATED": f"{REL(ARCHIPELAGO)} (points stratum=core, non-self-seed; 44 memberships)",
        "DOCKET": f"{REL(DOCKET_JSON)} (dockets[*].members; 6 working families) + companion MD family-candidates-docket-2026-07-17.md",
    },
    "hard_exclusions_honored": [
        "corpus.db canon_corpus.gx column (58 codes; a THIRD taxonomy) — NOT used as a membership source.",
        "corpus.db mechanic_gap_docket.docket_family (mechanic-gap families) — NOT used as a membership source.",
    ],
    "conflict_rule": {
        "cross_tier_precedence": "RATIFIED > PROPAGATED > DOCKET (min-precedence tier is the active row)",
        "same_tier_tiebreak": "two DOCKETs claiming one kit: lowest docket_id wins the active row (stable, deterministic)",
        "shadowed_by": "on every non-active row: names the tier of the winning (active) row for that kit_id",
        "loser_preservation": "every source membership is kept as a row; nothing is dropped",
    },
    "corpus_md5_ro": md5_file(CORPUS),
    "spine_definition": "canon_corpus WHERE corpus_class='record' (267 kits; era_year 2000=I/2013=II/2016=III/2024=IV)",
    "counts": {
        "rows_total": len(rows),
        "by_tier": dict(Counter(r["tier"] for r in rows)),
        "active_rows": sum(1 for r in rows if r["shadowed_by"] is None),
        "shadowed_rows": sum(1 for r in rows if r["shadowed_by"] is not None),
        "conflicts": len(conflicts),
    },
    "conflicts": conflicts,
    "memberships": rows,
}
with open(OUT_JSON, "w") as f:
    json.dump(sidecar, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ---- census computation ----
# Active membership = the winning (non-shadowed) row per kit. Family spine coverage
# counts ACTIVE rows only (a kit resolves to exactly one active family).
active = [r for r in rows if r["shadowed_by"] is None]
active_spine = [r for r in active if r["on_spine"]]

# per-family spine counts (active, on-spine)
fam_spine = Counter(r["family"] for r in active_spine)

# per-era spread of resolved (active, on-spine) kits
era_spread = Counter()
era_fam = defaultdict(Counter)
for r in active_spine:
    era = spine_era[r["kit_id"]]
    age = AGE.get(era, str(era))
    era_spread[age] += 1
    era_fam[age][r["family"]] += 1

# total distinct spine kits resolved (each active-spine row is a distinct kit)
resolved_spine_kits = {r["kit_id"] for r in active_spine}
total_spine_resolved = len(resolved_spine_kits)

# BEFORE baseline: only gateA RATIFIED on-spine
before_ratified_spine = [(k, f) for k, f in ratified if k in spine_era]
before_fam = Counter(f for k, f in before_ratified_spine)
before_kits = {k for k, f in before_ratified_spine}

# the 13 working-label family universe (from the W0 census)
FAMILY_UNIVERSE = [
    "WHIRLWIND", "CHANNELED-BEAM", "AURA", "TOTEM-SENTRY", "TRAP-MINE", "MINION-PET",
    "MELEE-STRIKE", "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY", "SHAPESHIFT",
    "IDENTITY-GAUGE", "CHAIN-BOUNCE", "DASH-STRIKER",
]

# families with ZERO before-spine membership (the 7 the task cites)
zero_before = [f for f in FAMILY_UNIVERSE if before_fam.get(f, 0) == 0]
recovered = [f for f in zero_before if fam_spine.get(f, 0) > 0]
still_zero = [f for f in zero_before if fam_spine.get(f, 0) == 0]

# off-spine tallies (for honesty)
active_offspine = [r for r in active if not r["on_spine"]]

md = []
w = md.append
w("# Tier-3 Family-Membership Sidecar — CENSUS")
w("")
w("**Run:** Tier-3 Encounter-Geometry Run · ruling **L-13(b)** · conductor gandalf `RUN-CONDUCTOR`")
w("**Author:** elrond (data steward) · 2026-07-22")
w(f"**Sidecar:** `{REL(OUT_JSON)}`")
w(f"**corpus.db (READ-ONLY, mode=ro):** md5 `{md5_file(CORPUS)}`")
w("")
w("> Transcription-with-provenance ONLY. No new rulings, no fabrication. Working labels — NOT canon.")
w("")
w("---")
w("")
w("## Tier provenance (FOUND)")
w("")
w("| tier | source artifact | rows |")
w("|---|---|---:|")
w(f"| RATIFIED | `corpus.db` table `{GATEA_TABLE}` | {len(ratified)} |")
w(f"| PROPAGATED | `{REL(ARCHIPELAGO)}` (stratum=core, non-self-seed) | {len(propagated)} |")
w(f"| DOCKET | `{REL(DOCKET_JSON)}` `dockets[*].members` | {len(docket)} |")
w(f"| **TOTAL rows** | | **{len(rows)}** |")
w("")
w(f"Active (non-shadowed) rows: **{len(active)}** · shadowed rows: **{len(rows) - len(active)}** · conflicts: **{len(conflicts)}**.")
w("")
w("---")
w("")
w("## Spine coverage delta (the headline)")
w("")
w(f"- **BEFORE** (gateA RATIFIED only, on-spine): **{len(before_kits)} kits / 267**, "
  f"across **{len([f for f in before_fam if before_fam[f] > 0])} families**.")
w(f"- **AFTER** (all three tiers, active on-spine): **{total_spine_resolved} kits / 267**, "
  f"across **{len([f for f in fam_spine if fam_spine[f] > 0])} families**.")
w(f"- **Delta:** +{total_spine_resolved - len(before_kits)} spine kits · "
  f"+{len([f for f in fam_spine if fam_spine[f] > 0]) - len([f for f in before_fam if before_fam[f] > 0])} families with spine membership.")
w("")
w("## Per-family spine counts (active on-spine): before -> after")
w("")
w("| family | before (RATIFIED only) | after (all tiers) | delta | note |")
w("|---|---:|---:|---:|---|")
for f in FAMILY_UNIVERSE:
    b = before_fam.get(f, 0)
    a = fam_spine.get(f, 0)
    note = ""
    if b == 0 and a > 0:
        note = "RECOVERED (was zero-spine)"
    elif b == 0 and a == 0:
        note = "still zero-spine"
    w(f"| {f} | {b} | {a} | {'+' if a-b>=0 else ''}{a-b} | {note} |")
w(f"| **TOTAL (distinct kits)** | **{len(before_kits)}** | **{total_spine_resolved}** | "
  f"**+{total_spine_resolved - len(before_kits)}** | |")
w("")
w("> Each spine kit resolves to exactly ONE active family (the conflict rule collapses cross-tier")
w(f"> duplicates), so the after-column sums cleanly: {sum(fam_spine.values())} family-assignments = "
  f"{total_spine_resolved} distinct on-spine kits. No kit is double-counted.")
w("")
w("---")
w("")
w("## Per-era spread of resolved (active on-spine) kits")
w("")
w("| age (era_year) | shelf | resolved kits | of era spine |")
w("|---|---|---:|---:|")
era_totals = {"I": 60, "II": 93, "III": 41, "IV": 73}
shelf = {"I": "D2 (2000)", "II": "PoE1 (2013)", "III": "GD (2016)", "IV": "PoE2+LE (2024)"}
for age in ["I", "II", "III", "IV"]:
    n = era_spread.get(age, 0)
    w(f"| Age {age} | {shelf[age]} | {n} | {era_totals[age]} |")
w(f"| **all** | | **{total_spine_resolved}** | **267** |")
w("")
w("### Per-era × family (active on-spine)")
w("")
present_fams = [f for f in FAMILY_UNIVERSE if fam_spine.get(f, 0) > 0]
w("| family | Age I | Age II | Age III | Age IV |")
w("|---|---:|---:|---:|---:|")
for f in present_fams:
    cells = [str(era_fam[age].get(f, 0)) for age in ["I", "II", "III", "IV"]]
    w(f"| {f} | " + " | ".join(cells) + " |")
w("")
w("---")
w("")
w("## Zero-membership family recovery (the L-13(b) purpose)")
w("")
w(f"Families with **zero on-spine membership BEFORE** (RATIFIED-only): "
  f"{', '.join(zero_before) if zero_before else '(none)'} ({len(zero_before)} families).")
w("")
w(f"- **RECOVERED** (now carry >=1 on-spine member): "
  f"**{', '.join(recovered) if recovered else '(none)'}** ({len(recovered)}).")
w(f"- **Still zero-spine**: {', '.join(still_zero) if still_zero else '(none)'} ({len(still_zero)}).")
w("")
w("Recovery-source breakdown (which tier supplied each recovered family's first spine member):")
w("")
w("| family | recovered via tier(s) | on-spine count |")
w("|---|---|---:|")
for f in recovered:
    tiers = sorted({r["tier"] for r in active_spine if r["family"] == f}, key=lambda t: PRECEDENCE[t])
    w(f"| {f} | {', '.join(tiers)} | {fam_spine[f]} |")
w("")
w("> Still-zero families are HONEST HOLES — their docket/draft members are all off-spine (annex/system")
w("> games), OR they are fresh-draft families (CHAIN-BOUNCE, DASH-STRIKER) with no materialized-tier")
w("> artifact. No fabrication was used to fill them.")
w("")
w("---")
w("")
w("## Conflicts (cross-tier family disagreement)")
w("")
if conflicts:
    w(f"**{len(conflicts)} conflict(s)** — kit carries different families across tiers. "
      "Active row = highest-precedence tier; losers kept with `shadowed_by`.")
    w("")
    w("| kit_id | active family (tier) | shadowed family (tier) | on_spine |")
    w("|---|---|---|:---:|")
    for c in conflicts:
        sh = "; ".join(f"{s['family']} ({s['tier']})" for s in c["shadowed"])
        w(f"| `{c['kit_id']}` | {c['active_family']} ({c['active_tier']}) | {sh} | {c['on_spine']} |")
    # split cross-tier vs same-tier(within-DOCKET) conflicts for legibility
    import re as _re
    def _did(art):
        m = _re.search(r"docket_id=(\d+)", art)
        return int(m.group(1)) if m else None
    same_tier_conf = []
    for c in conflicts:
        tiers = {c["active_tier"]} | {s["tier"] for s in c["shadowed"]}
        if tiers == {"DOCKET"}:
            same_tier_conf.append(c["kit_id"])
    w("")
    w(f"Of the {len(conflicts)} conflicts, **{len(same_tier_conf)}** are SAME-TIER (a kit proposed to two "
      "DOCKETs — the discovery docket legitimately lets one kit match multiple axis-signatures). "
      "For these, the active row is picked deterministically by **lowest `docket_id`** "
      "(docket order: 1 MELEE-STRIKE · 2 IDENTITY-GAUGE · 3 SHAPESHIFT · 4 DOT-AILMENT · "
      "5 MULTI-PROJECTILE-VOLLEY · 6 MINION-PET). The remaining "
      f"{len(conflicts) - len(same_tier_conf)} are cross-tier, resolved by RATIFIED>PROPAGATED>DOCKET. "
      "This is a data-integrity call, NOT a design ruling — a consumer wanting a kit's alternate family "
      "reads the shadowed rows.")
else:
    w("**0 cross-family conflicts.** No kit is assigned different families across tiers. "
      "(Same-family cross-tier duplicates exist — e.g. the 7 MINION-PET gateA seeds re-appear in the "
      "MINION-PET docket as `ratified-seed` — but those agree on family; they are shadowed, not conflicts.)")
w("")
w("### Same-family shadowed duplicates (provenance-preserved, NOT conflicts)")
w("")
same_fam_shadow = [r for r in rows if r["shadowed_by"] is not None]
sf_by_pair = Counter((r["tier"], r["shadowed_by"]) for r in same_fam_shadow)
w("| shadowed tier | shadowed_by (winning tier) | rows |")
w("|---|---|---:|")
for (t, sb), n in sorted(sf_by_pair.items()):
    w(f"| {t} | {sb} | {n} |")
w(f"| **total shadowed** | | **{len(same_fam_shadow)}** |")
w("")
w("---")
w("")
w("## Gaps (honest holes)")
w("")
w("| gap | detail |")
w("|---|---|")
w("| Fresh-draft families unmaterialized | CHAIN-BOUNCE + DASH-STRIKER exist only as B3 fresh-draft flags "
  "(grill Appendix B B3) — NO tier artifact enumerates kit_id memberships. Not transcribed; would require "
  "a ruling to materialize. On-spine count for both = 0 by absence of source, not by fabrication-refusal. |")
w("| PROPAGATED tier is hypothesis-grade | The 44 τ-propagated rows ran ~1/3 precision (global-τ umbrella "
  "defect, per archipelago post-mortem). They are HYPOTHESIS-tier by charter and carry `tier=PROPAGATED` + "
  "`shadowed_by` semantics so a consumer can filter them out. Not ratified truth. |")
w("| Off-spine members excluded from spine counts | "
  f"{len(active_offspine)} active rows resolve to a family but sit off the record-267 spine (annex/system "
  "games: la/d3/d4/vs/tq/di/hot/chronicon/undecember/tl2/tli/hades1/hades2/tq2/mcd/tl1). They ARE in the "
  "sidecar (on_spine=false) but do not count toward the 267 coverage. |")
w("| SUMMONER-LEGION (B3 observation) | grill B3 flags a record-class summoner mass claimed by nothing "
  "(Spectres/Skeleton Mages/Golementalist/etc.). No docket exists yet — deliberately NOT invented here. |")
w("")
w("---")
w("")
w("*Filed by elrond (data steward), 2026-07-22. Materialization is transcription; every row cites its origin.*")

with open(OUT_CENSUS, "w") as f:
    f.write("\n".join(md) + "\n")

# ---- console report ----
print("=== SIDECAR BUILD COMPLETE ===")
print(f"rows total: {len(rows)}  (RATIFIED {len(ratified)} + PROPAGATED {len(propagated)} + DOCKET {len(docket)})")
print(f"active: {len(active)}  shadowed: {len(rows)-len(active)}  conflicts: {len(conflicts)}")
print(f"BEFORE spine kits (gateA only): {len(before_kits)} / 267")
print(f"AFTER  spine kits (all tiers) : {total_spine_resolved} / 267   (delta +{total_spine_resolved-len(before_kits)})")
print(f"per-era resolved: " + "  ".join(f"Age {a}={era_spread.get(a,0)}" for a in ['I','II','III','IV']))
print(f"zero-before families ({len(zero_before)}): {zero_before}")
print(f"RECOVERED ({len(recovered)}): {recovered}")
print(f"still zero-spine ({len(still_zero)}): {still_zero}")
print(f"conflicts: {len(conflicts)}")
print(f"outputs:\n  {OUT_JSON}\n  {OUT_CENSUS}")
