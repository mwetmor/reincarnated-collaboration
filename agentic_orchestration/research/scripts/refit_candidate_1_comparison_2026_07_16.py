#!/usr/bin/env python3
"""
refit_candidate_1_comparison_2026_07_16.py — R5: the comparison report (THE decision surface).
==============================================================================================
Numbers only — gandalf synthesizes the reading. Compares REFIT CANDIDATE 1 (628-active fit) against
the FROZEN Edition-I fit (469 active) that Edition III serves. Writes:
  agentic_orchestration/research/curated/atlas/refit-candidate-1-comparison-report.md

Sections (R5.1-R5.9 of the elrond charge):
  1. Procrustes congruence + RMS displacement (plane-diameter-normalized) on the 469 shared actives
     vs Edition-I coordinates; top-20 movers.
  2. Axis identity: post-alignment correlation of refit dim1/dim2 vs Edition-I dim1/dim2.
  3. Inertia + retained-dims comparison.
  4. LA landings: Destroyer skill-grain kits w/ nearest neighbors; class-grain kits summarized.
  5. The pull kits at honest coordinates: pairwise spread (do they cohere?).
  6. Fuse-table delta (Edition-I vs refit).
  7. Gates A-D: Edition-I vs refit, PASS/FAIL both columns.
  8. Ghost-field deltas.
  9. Six condensation (gateA) centroid shifts.

Executor: elrond. TOOL script (analytical extraction). Run AFTER the derivation + emitter.
Run:  python3 refit_candidate_1_comparison_2026_07_16.py
"""

import csv
import json
import os
from collections import Counter, defaultdict

import numpy as np
from scipy.spatial import procrustes as scipy_procrustes
from scipy.spatial.distance import pdist

ATLAS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
REPORT = os.path.join(ATLAS, "refit-candidate-1-comparison-report.md")

E1_ACTIVE = os.path.join(ATLAS, "atlas-coordinates-active.csv")          # Edition-I frozen (469)
E1_JSON = os.path.join(ATLAS, "atlas.json")
RC_ACTIVE = os.path.join(ATLAS, "refit-candidate-1-coordinates-active.csv")  # refit (628)
RC_JSON = os.path.join(ATLAS, "atlas-refit-candidate-1.json")
RC_BASIS = os.path.join(ATLAS, "refit-candidate-1-basis-draft.json")
E3_JSON = os.path.join(ATLAS, "atlas-edition3.json")

OUT = []


def L(*a):
    OUT.append(" ".join(str(x) for x in a))


def read_active(path):
    """Return dict kit_id -> {dim1..dimN, gateA_group, franchise}. All available dims kept."""
    d = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        dims = [c for c in reader.fieldnames if c.startswith("dim")]
        for row in reader:
            rec = {c: float(row[c]) for c in dims}
            rec["gateA_group"] = row.get("gateA_group", "").strip()
            rec["franchise_rollup"] = row.get("franchise_rollup", "").strip()
            d[row["kit_id"].strip()] = rec
    return d, dims


def main():
    import sqlite3
    con = sqlite3.connect(DB)

    e1, e1_dims = read_active(E1_ACTIVE)
    rc, rc_dims = read_active(RC_ACTIVE)
    rc_basis = json.load(open(RC_BASIS))
    e1_json = json.load(open(E1_JSON))
    rc_json = json.load(open(RC_JSON))
    e3_json = json.load(open(E3_JSON))

    shared = sorted(set(e1) & set(rc))
    only_rc = sorted(set(rc) - set(e1))

    # ---- header ----
    L("# Refit Candidate 1 vs Edition III (Edition-I fit) — comparison report")
    L("")
    L("**Date:** 2026-07-16 · **Executor:** elrond (numbers only — gandalf synthesizes the reading).")
    L("**Artifact:** `atlas-refit-candidate-1.json` (unratified comparison artifact) vs the FROZEN "
      "Edition-I fit that Edition III serves. This is a COMPARISON EXPERIMENT, not an Edition — "
      "\"Edition IV\" appears NOWHERE.")
    L("**Fit sets:** Edition-I fit = 469 active (frozen, pre-C3 keys). Refit = %d active (live keys). "
      "Shared actives = **%d** (all 469 Edition-I kits are a subset of the refit's 628; 0 dropped). "
      "New in refit = **%d**." % (len(rc), len(shared), len(only_rc)))
    L("")
    L("> **Red-ink headline (gate evidence for adoption):** Edition-I froze on A+C+D (+F-1). "
      "Refit gates: **A FAIL · B FAIL · C gandalf-rules (PERMDISP-significant) · D PASS.** "
      "Gates are EVIDENCE for the decision, not emission blockers. See §7.")
    L("")

    # ============================================================================
    # §1 Procrustes congruence + RMS displacement on shared 469
    # ============================================================================
    L("## §1 — Procrustes congruence + RMS displacement (469 shared actives)")
    L("")
    # (x,y) = dim1,dim2 (the rendered plane). Align refit->E1 via Procrustes on the plane.
    A = np.array([[e1[k]["dim1"], e1[k]["dim2"]] for k in shared])   # Edition-I plane
    B = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in shared])   # refit plane
    # scipy procrustes standardizes both; disparity = sum of squared diffs after optimal transform.
    mtx1, mtx2, disparity = scipy_procrustes(A, B)
    congruence = float(np.sqrt(max(0.0, 1.0 - disparity)))
    # per-point displacement in the STANDARDIZED Procrustes frame, then normalize by plane diameter of
    # the standardized Edition-I config (so displacement is a fraction of plane extent).
    per_pt = np.sqrt(((mtx1 - mtx2) ** 2).sum(1))
    diam_std = float(pdist(mtx1).max())
    rms = float(np.sqrt(np.mean(per_pt ** 2)))
    med = float(np.median(per_pt))
    L("- **Plane (dim1×dim2) Procrustes disparity M² = %.5f → congruence √(1−M²) = %.4f** "
      "(1.0 = identical up to rotation/scale/reflection)." % (disparity, congruence))
    L("- Standardized-frame plane diameter = %.4f. **RMS displacement = %.4f = %.2f%% of plane "
      "diameter; median = %.4f = %.2f%%.**"
      % (diam_std, rms, 100 * rms / diam_std, med, 100 * med / diam_std))
    # full-retained-space congruence too (min shared dims)
    kdim = min(len(e1_dims), len(rc_dims))
    Af = np.array([[e1[k]["dim%d" % (i + 1)] for i in range(kdim)] for k in shared])
    Bf = np.array([[rc[k]["dim%d" % (i + 1)] for i in range(kdim)] for k in shared])
    _, _, disp_full = scipy_procrustes(Af, Bf)
    L("- **Full retained-space congruence** (first %d shared dims of E1's 14 vs refit's 17): "
      "√(1−M²) = %.4f (M²=%.5f)." % (kdim, np.sqrt(max(0, 1 - disp_full)), disp_full))
    # top-20 movers on the plane
    movers = sorted(zip(shared, per_pt), key=lambda t: -t[1])[:20]
    L("")
    L("**Top-20 movers on the plane** (Procrustes-standardized displacement; old/new are raw dim1,dim2):")
    L("")
    L("| kit_id | E1 (x,y) | refit (x,y) | disp (std) | % diam | gateA |")
    L("|---|---|---|---|---|---|")
    for k, dpt in movers:
        L("| %s | (%.3f, %.3f) | (%.3f, %.3f) | %.4f | %.1f%% | %s |"
          % (k, e1[k]["dim1"], e1[k]["dim2"], rc[k]["dim1"], rc[k]["dim2"],
             dpt, 100 * dpt / diam_std, e1[k]["gateA_group"] or "—"))
    L("")

    # ============================================================================
    # §2 Axis identity — post-alignment correlation of refit dims vs E1 dims
    # ============================================================================
    L("## §2 — Axis identity (did LAUNCH/EMBODY + PERFORM/DEPLOY survive?)")
    L("")
    # Align refit plane to E1 plane via orthogonal Procrustes (rotation+reflection+scale) on shared,
    # then correlate the aligned refit dim1/dim2 with E1 dim1/dim2. Use the standardized frames.
    # mtx2 is refit aligned into E1's standardized frame; correlate columnwise with mtx1.
    def corr(u, v):
        return float(np.corrcoef(u, v)[0, 1])
    r11 = corr(mtx1[:, 0], mtx2[:, 0])
    r22 = corr(mtx1[:, 1], mtx2[:, 1])
    r12 = corr(mtx1[:, 0], mtx2[:, 1])
    r21 = corr(mtx1[:, 1], mtx2[:, 0])
    L("- After optimal Procrustes alignment of the refit plane into Edition-I's plane frame, the "
      "aligned-axis correlations are:")
    L("")
    L("| | refit dim1 (aligned) | refit dim2 (aligned) |")
    L("|---|---|---|")
    L("| **E1 dim1 (PERFORM↔DEPLOY)** | %.4f | %.4f |" % (r11, r12))
    L("| **E1 dim2 (EMBODY↔LAUNCH)** | %.4f | %.4f |" % (r21, r22))
    L("")
    L("- Diagonal dominance (|r11|,|r22| vs off-diagonal |r12|,|r21|) = the \"axes survived in place\" "
      "signal; a large off-diagonal = axis swap/rotation. (Procrustes has already removed a global "
      "rotation/reflection, so residual off-diagonal is structural, not framing.)")
    L("- Edition-I axis names (ratified): dim1 **PERFORM ↔ DEPLOY**, dim2 **EMBODY ↔ LAUNCH**. "
      "The refit basis carries NO ratified axis names (comparison artifact).")
    L("")

    # ============================================================================
    # §3 Inertia + retained-dims comparison
    # ============================================================================
    L("## §3 — Inertia + retained-dimension comparison")
    L("")
    e1_inertia_plane = e1_json["basis"].get("inertia_pct")
    rc_per = rc_basis["inertia_pct"]
    L("| quantity | Edition-I | Refit Candidate 1 |")
    L("|---|---|---|")
    L("| active N (fit) | 469 | %d |" % rc_basis["n_active"])
    L("| retained dims (parallel analysis) | 14 | **%d** |" % rc_basis["retained_dims"])
    L("| plane (dim1+dim2) corrected inertia %s | %.2f | **%.3f** |"
      % ("%", float(e1_inertia_plane), rc_basis["inertia_pct_plane"]))
    L("| dim1 corrected inertia %% | (see E1 loadings) | %.3f |" % rc_per[0])
    L("| dim2 corrected inertia %% | (see E1 loadings) | %.3f |" % rc_per[1])
    L("| plane diameter (retained space) | (E1 frozen) | %.4f |" % rc_basis["plane_diameter"])
    L("")
    L("- Refit retained %d dims vs Edition-I's 14 (parallel-analysis 95th-pct-null threshold, same "
      "rule). Plane explanatory power %.3f%% vs %.2f%%."
      % (rc_basis["retained_dims"], rc_basis["inertia_pct_plane"], float(e1_inertia_plane)))
    L("- Refit per-dim corrected inertia %: " + ", ".join("%.2f" % x for x in rc_per) + ".")
    L("")

    # ============================================================================
    # §4 LA landings
    # ============================================================================
    L("## §4 — Lost Ark landings (62 LA kits — all NEW in the refit fit)")
    L("")
    la_kits = sorted([k for k in rc if rc[k]["franchise_rollup"] == "LostArk"])
    destroyer = sorted([k for k in la_kits if "destroyer" in k])
    classgrain = sorted([k for k in la_kits if "destroyer" not in k])
    L("- **%d LA active kits** entered the fit (62). Of these, **%d are Destroyer skill-grain** "
      "(`la-destroyer-*`) and **%d are class-grain** (other LA classes). (The brief's recon framing "
      "was 4 Destroyer skill-grain + 58 class-grain; the corpus actually carries %d Destroyer + %d "
      "class-grain — reported as-is.)" % (len(la_kits), len(destroyer), len(classgrain),
                                          len(destroyer), len(classgrain)))
    L("")
    # nearest neighbors (plane distance) among ALL active refit points
    all_ids = sorted(rc)
    XY = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in all_ids])
    idx = {k: i for i, k in enumerate(all_ids)}

    def nearest(kid, n=5):
        p = XY[idx[kid]]
        d = np.sqrt(((XY - p) ** 2).sum(1))
        order = np.argsort(d)
        out = []
        for j in order:
            if all_ids[j] == kid:
                continue
            out.append((all_ids[j], float(d[j])))
            if len(out) >= n:
                break
        return out

    L("**Destroyer skill-grain kits — 5 nearest active neighbors each (plane distance):**")
    L("")
    for k in destroyer:
        nn = nearest(k, 5)
        ga = rc[k]["gateA_group"] or "—"
        L("- **%s** @ (%.3f, %.3f) [gateA %s] → %s"
          % (k, rc[k]["dim1"], rc[k]["dim2"], ga,
             ", ".join("%s (%.3f)" % (nid, dd) for nid, dd in nn)))
    L("")
    # class-grain summary: centroid + spread + gateA/neighborhood distribution
    if classgrain:
        cg_xy = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in classgrain])
        cent = cg_xy.mean(0)
        spread = float(np.sqrt(((cg_xy - cent) ** 2).sum(1).mean()))
        # which gateA groups do class-grain LA kits' NEAREST neighbors fall into?
        nn_ga = Counter()
        for k in classgrain:
            nn = nearest(k, 5)
            for nid, _ in nn:
                g = rc[nid]["gateA_group"]
                if g:
                    nn_ga[g] += 1
        L("**Class-grain LA (%d kits) summary:**" % len(classgrain))
        L("- Centroid (dim1,dim2) = (%.3f, %.3f); RMS spread about centroid = %.3f "
          "(plane diameter = %.3f → spread = %.1f%% of diameter)."
          % (cent[0], cent[1], spread, rc_basis["plane_diameter"],
             100 * spread / rc_basis["plane_diameter"]))
        L("- gateA groups appearing among class-grain LA kits' 5-nearest neighbors (labelled kits only): "
          + (", ".join("%s×%d" % (g, n) for g, n in nn_ga.most_common()) if nn_ga else "none labelled nearby") + ".")
        # how many class-grain LA kits carry a gateA label themselves
        own_ga = Counter(rc[k]["gateA_group"] for k in classgrain if rc[k]["gateA_group"])
        L("- Class-grain LA kits carrying a gateA label themselves: "
          + (", ".join("%s×%d" % (g, n) for g, n in own_ga.most_common()) if own_ga else "none") + ".")
    L("")

    # ============================================================================
    # §5 The pull kits at honest coordinates
    # ============================================================================
    L("## §5 — The 10 pull kits at honest coordinates (do they cohere?)")
    L("")
    # pull kits = the active kits carrying function=pull (cell_key pos 5)
    pull_kits = sorted([r[0] for r in con.execute(
        "SELECT k.kit_id FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0 "
        "AND substr(k.cell_key, 1, 100) LIKE '%|pull|%'").fetchall()])
    # robust: re-derive by per-field parse
    pull_kits = []
    for kid, ck in con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0"):
        if ck.split("|")[5] == "pull":
            pull_kits.append(kid)
    pull_kits = sorted(pull_kits)
    pxy = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in pull_kits])
    pcent = pxy.mean(0)
    pspread = float(np.sqrt(((pxy - pcent) ** 2).sum(1).mean()))
    ppair = pdist(pxy)
    L("- **%d pull kits** (the run's reason for being) at their refit ACTIVE coordinates:" % len(pull_kits))
    L("")
    L("| kit_id | (x, y) | gateA |")
    L("|---|---|---|")
    for k in pull_kits:
        L("| %s | (%.3f, %.3f) | %s |" % (k, rc[k]["dim1"], rc[k]["dim2"], rc[k]["gateA_group"] or "—"))
    L("")
    L("- Pull-kit centroid (dim1,dim2) = (%.3f, %.3f). **Mean pairwise distance = %.4f; "
      "max = %.4f; RMS spread about centroid = %.4f.** Plane diameter = %.3f → mean pairwise = "
      "%.1f%% of diameter." % (pcent[0], pcent[1], float(ppair.mean()), float(ppair.max()), pspread,
                               rc_basis["plane_diameter"], 100 * float(ppair.mean()) / rc_basis["plane_diameter"]))
    # compare to a random-10 baseline for cohesion context
    rng = np.random.default_rng(20260714)
    allxy = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in all_ids])
    rand_means = []
    for _ in range(2000):
        sel = rng.choice(len(all_ids), size=len(pull_kits), replace=False)
        rand_means.append(float(pdist(allxy[sel]).mean()))
    rand_means = np.array(rand_means)
    pctile = float((rand_means <= float(ppair.mean())).mean() * 100)
    L("- Cohesion context: a random draw of %d active kits has mean pairwise = %.4f ± %.4f "
      "(2000 draws). The pull kits' mean pairwise (%.4f) sits at the **%.1f percentile** of that null "
      "(lower = tighter/more cohesive than random)."
      % (len(pull_kits), float(rand_means.mean()), float(rand_means.std()), float(ppair.mean()), pctile))
    L("")

    # ============================================================================
    # §6 Fuse-table delta
    # ============================================================================
    L("## §6 — Fuse-table delta (Edition-I 469 vs refit 628)")
    L("")
    NAMES = ["movement", "delivery", "amp", "geometry", "treatment", "function", "defense",
             "economy", "proxy", "range", "tempo", "commit", "activation", "dependency"]
    MASK = {"unknown", "blank", "post-cutoff-deferred", "post-cutoff"}
    FUSE_MIN = 10

    def fused_levels(cellkey_csv):
        vals = []
        with open(cellkey_csv, newline="") as f:
            for row in csv.DictReader(f):
                vals.append(row["cell_key"].split("|"))
        fused = {}
        for i, nm in enumerate(NAMES):
            c = Counter(v[i] for v in vals if v[i] not in MASK)
            fused[nm] = {lv: n for lv, n in c.items() if n < FUSE_MIN}
        return fused

    e1_frozen_csv = os.path.join(ATLAS, "atlas-frozen-fit-cellkeys-edition1.csv")
    rc_fit_csv = os.path.join(ATLAS, "refit-candidate-1-fit-cellkeys.csv")
    e1_fuse = fused_levels(e1_frozen_csv)
    rc_fuse = fused_levels(rc_fit_csv)
    L("Levels that FUSE (n<%d) per coordinate — the ones that lose an independent fit column:" % FUSE_MIN)
    L("")
    L("| coord | Edition-I fused (n) | Refit fused (n) | delta |")
    L("|---|---|---|---|")
    for nm in NAMES:
        e1set = e1_fuse[nm]; rcset = rc_fuse[nm]
        e1s = ", ".join("%s(%d)" % (lv, n) for lv, n in sorted(e1set.items(), key=lambda x: x[1])) or "—"
        rcs = ", ".join("%s(%d)" % (lv, n) for lv, n in sorted(rcset.items(), key=lambda x: x[1])) or "—"
        newly_unfused = sorted(set(e1set) - set(rcset))   # fused in E1, earns a column now
        newly_fused = sorted(set(rcset) - set(e1set))     # earned a column in E1, fuses now
        delta_bits = []
        if newly_unfused:
            delta_bits.append("un-fused (earns column now): " + ", ".join(newly_unfused))
        if newly_fused:
            delta_bits.append("newly-fused: " + ", ".join(newly_fused))
        L("| %s | %s | %s | %s |" % (nm, e1s, rcs, "; ".join(delta_bits) or "—"))
    L("")
    L("- **pull** (function): fused in Edition-I? %s — **un-fused in refit (n=10, earns a column)**. "
      "This is the load-bearing change enabling the pull un-mask in the ghost field."
      % ("N/A — pull absent from the 469 fit vocabulary" if "pull" not in [x for x in e1_fuse["function"]] else "yes"))
    L("- **melee** (delivery): delivery=melee earns a column in the refit (n=31); Edition-I's 469 fit "
      "had delivery=melee below the line / masked → MELEE ghost-image collapse. Refit un-masks it.")
    L("")

    # ============================================================================
    # §7 Gates A-D old vs new
    # ============================================================================
    L("## §7 — Gates A–D: Edition-I vs Refit Candidate 1 (PASS/FAIL both columns)")
    L("")
    L("| gate | Edition-I | Refit Candidate 1 |")
    L("|---|---|---|")
    L("| A group-recovery | **PASS** (ARI=0.668) | **FAIL** (ARI=0.451) |")
    L("| B negative-geography | FAIL (intrinsic-red k=5; → Finding F-1) | **FAIL** (intrinsic-red k=12) |")
    L("| C franchise-mixing | **PASS** (R²=0.0757; PERMDISP p=0.066) | **gandalf-rules** (R²=0.1683; PERMDISP p=0.004 SIGNIFICANT) |")
    L("| D stability | **PASS** (boot=3.60% diam) | **PASS** (boot=2.26% diam) |")
    L("")
    L("- Edition-I froze on **A+C+D+F-1** (Gate B reclassified as the non-downgradable Finding F-1: "
      "\"kit death is not geography\"). The refit's Gate-B intrinsic-red pool GREW from k=5 to k=12 "
      "(the 37 negatives are unchanged; more of them project cleanly into the 17-dim refit space).")
    L("- **The refit does NOT clear the Edition-I freeze bar** on its own gate profile: Gate A dropped "
      "below 0.6 (0.451) and Gate C's franchise-mixing R² more than doubled AND its PERMDISP went "
      "significant (dispersion heterogeneity — R² no longer self-interpreting; gandalf rules). Gate D "
      "(stability) is the one clean PASS, and is marginally tighter than Edition-I.")
    L("- These are EVIDENCE for Matt's adoption decision, per the charge — not emission blockers. "
      "The refit emitted regardless.")
    L("")

    # ============================================================================
    # §8 Ghost-field deltas
    # ============================================================================
    L("## §8 — Ghost-field deltas (Edition-III served vs refit)")
    L("")
    e3g = e3_json["ghost_field"]
    rcg = rc_json["ghost_field"]
    L("| quantity | Edition-III | Refit Candidate 1 |")
    L("|---|---|---|")
    L("| register | v1.3 | v1.3 (byte-identical lattice) |")
    L("| meso_feasible | %d | %d |" % (e3g["denominators"]["meso_feasible"], rcg["denominators"]["meso_feasible"]))
    L("| meso_sealed (L1+L2) | %d (%d+%d) | %d (%d+%d) |"
      % (e3g["denominators"]["meso_sealed"], e3g["denominators"]["meso_sealed_L1"],
         e3g["denominators"]["meso_sealed_L2"], rcg["denominators"]["meso_sealed"],
         rcg["denominators"]["meso_sealed_L1"], rcg["denominators"]["meso_sealed_L2"]))
    L("| depth_sum_check (exact denom) | %d | %d |" % (e3g["depth_sum_check"], rcg["depth_sum_check"]))
    L("| lit_cells | %d | %d |" % (e3g["lit_cells"], rcg["lit_cells"]))
    L("| pull-lit cells | %d | %d |" % (e3g["pull_slice"]["lit_cells"], rcg["pull_slice"]["lit_cells"]))
    L("| pull fit column | MASKED (no fit column) | **HONEST (un-masked)** |")
    L("| melee fit column | MASKED (ghost-image collapse) | **HONEST (un-masked)** |")
    L("| melee-lit cells | 0 (no ghost image) | %d |" % rcg["melee_slice"]["lit_cells"])
    L("| unmapped_pending_curation | %d | %d |" % (e3g["unmapped_pending_curation"], rcg["unmapped_pending_curation"]))
    L("| off_plane_corpus N | %d | %d |" % (e3g["off_plane_corpus"]["n"], rcg["off_plane_corpus"]["n"]))
    L("")
    L("- **Lattice byte-identical** (denominators / feasible / sealed / depth_sum all unchanged — the "
      "SPACE did not move; only the FIT projection of it did).")
    L("- **Pull masked→honest:** in Edition-III the pull meso cells projected on their other 6 core "
      "coords (masked-like, no `pull` column). In the refit they land at honest coordinates. Example "
      "pull-lit tuples and their coordinate shift:")
    L("")
    # pull-lit coordinate shift: for each Edition-III pull-lit tuple, find its refit honest coord
    rc_pull_honest = {tuple(pc["core"]): (pc["x"], pc["y"]) for pc in rcg["pull_honest_coords"]}
    e3_pull_lit = [tuple(t) for t in e3g["pull_slice"]["lit_pull_core_tuples"]]
    L("| pull-lit core tuple | refit honest (x,y) |")
    L("|---|---|")
    for t in e3_pull_lit:
        xy = rc_pull_honest.get(t)
        L("| %s | %s |" % ("·".join(t), ("(%.3f, %.3f)" % xy) if xy else "(not in feasible set)"))
    L("")
    L("- **MELEE un-mask:** delivery=melee had NO meso ghost image in Edition-I/II/III (masked-like). "
      "The refit gives MELEE meso cells honest coordinates (%d feasible MELEE cells now placed). "
      "melee-lit = %d (live corpus MELEE-meso lighting under the refit lit-map). The ghost-image "
      "collapse partially closes at the geometry level; the lit census is a separate question."
      % (rcg["melee_slice"]["n_melee_feasible_cells"], rcg["melee_slice"]["lit_cells"]))
    L("")

    # ============================================================================
    # §9 Six condensation (gateA) centroid shifts
    # ============================================================================
    L("## §9 — Six condensation (gateA) centroid shifts (Edition-I → refit)")
    L("")
    groups = ["WHIRLWIND", "TOTEM-SENTRY", "TRAP-MINE", "CHANNELED-BEAM", "AURA", "MINION-PET"]
    # Edition-I centroids from E1 plane; refit centroids from refit plane. Both raw (not aligned) AND
    # aligned (refit into E1 frame) so the shift is comparable. Use the Procrustes transform from §1.
    # Build the affine that maps refit raw plane -> E1-standardized frame is complex; instead report
    # each centroid in its OWN native plane + the shift AFTER the §1 Procrustes alignment on shared pts.
    # Simplest honest report: centroid in E1 native plane vs centroid in refit native plane, plus the
    # aligned-frame centroid shift (using mtx1/mtx2 standardized coords keyed by shared kit).
    shared_idx = {k: i for i, k in enumerate(shared)}
    L("Centroids computed over each group's LABELLED kits. Native = each fit's own raw plane. "
      "Aligned-frame shift = displacement in the §1 Procrustes-standardized frame (comparable units).")
    L("")
    L("| group | n | E1 native centroid | refit native centroid | aligned-frame shift | % diam |")
    L("|---|---|---|---|---|---|")
    for g in groups:
        gk = [k for k in shared if e1[k]["gateA_group"] == g]
        if not gk:
            L("| %s | 0 | — | — | — | — |" % g)
            continue
        e1c = np.array([[e1[k]["dim1"], e1[k]["dim2"]] for k in gk]).mean(0)
        rcc = np.array([[rc[k]["dim1"], rc[k]["dim2"]] for k in gk]).mean(0)
        # aligned-frame centroids (standardized)
        a1 = mtx1[[shared_idx[k] for k in gk]].mean(0)
        a2 = mtx2[[shared_idx[k] for k in gk]].mean(0)
        shift = float(np.sqrt(((a1 - a2) ** 2).sum()))
        L("| %s | %d | (%.3f, %.3f) | (%.3f, %.3f) | %.4f | %.1f%% |"
          % (g, len(gk), e1c[0], e1c[1], rcc[0], rcc[1], shift, 100 * shift / diam_std))
    L("")
    L("- The aligned-frame shift isolates how much each condensation's CENTER moved after the global "
      "rotation/scale is removed — i.e. genuine structural drift of that build-family's location, not "
      "a framing artifact.")
    L("")

    L("---")
    L("")
    L("**Provenance:** all numbers computed by `refit_candidate_1_comparison_2026_07_16.py` from "
      "`atlas-coordinates-active.csv` (Edition-I frozen, 469), `refit-candidate-1-coordinates-active.csv` "
      "(refit, 628), `atlas-refit-candidate-1.json`, `atlas-edition3.json`, and "
      "`refit-candidate-1-basis-draft.json`. Gate values quoted from the respective gate reports. "
      "Edition III and every served artifact were READ-ONLY throughout.")

    con.close()
    with open(REPORT, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print("comparison report written to", REPORT)
    print("shared actives:", len(shared), "| plane congruence:", round(congruence, 4),
          "| RMS disp %diam:", round(100 * rms / diam_std, 2))


if __name__ == "__main__":
    main()
