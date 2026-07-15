#!/usr/bin/env python3
"""
Atlas Derivation Pipeline — 2026-07-14
=======================================
Executes the pinned pre-registration:
  agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md (v1.1)

Executor: elrond (data steward). EXECUTE WITH NO INTERPRETATION.
Numbers return; gandalf reads them as DRIFT-CRITIC.

Single entrypoint, pinned seeds, self-contained. Lineage/style:
  family-discovery-poc-rerank.py (same DB constant, NAMES, MASK, MINSUP conventions).

Stages:
  0  hygiene + verification (snapshot marker, N=469, label table, franchise rollup, fusing map)
  1  diagnostics (per-coord entropy; Cramer's V + MI; BH-FDR q=0.05; freq tables post-fuse)
  2  four method families:
       2a MCA (indicator SVD, Greenacre-corrected inertia, MFA block weighting,
              CATPCA-twin ordinal on tempo+commit; parallel-analysis retention vs 1000 nulls)
       2b Gower dissimilarity -> classical (Torgerson) MDS (same permutation-null retention)
       2c Leiden on kNN graph k=10, CPM, resolution sweep 0.5-2.0 step 0.1, 100 seeds, consensus
       2d LCA k=2..12, 50 starts, BIC selection (stepmix)
  3  four gates (numbers + PASS/FAIL vs pinned thresholds, nothing else):
       A group recovery   B negative geography   C franchise mixing   D stability

Run:  python3 atlas_derivation_2026_07_14.py
Everything regenerates from this one command. All randomness pinned to SEED.
"""

import os, sys, json, math, sqlite3, hashlib, itertools
from collections import defaultdict, Counter

import numpy as np
import pandas as pd
from scipy import linalg as sla
from scipy.stats import chi2_contingency
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import procrustes as scipy_procrustes

# ----------------------------------------------------------------------------
# CONSTANTS (pinned) — lineage: family-discovery-poc-rerank.py
# ----------------------------------------------------------------------------
DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
LABEL_CSV = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-a-group-labels.csv"

NAMES = ["movement", "delivery", "amp", "geometry", "treatment", "function", "defense",
         "economy", "proxy", "range", "tempo", "commit", "activation", "dependency"]
MASK = {"unknown", "blank", "post-cutoff-deferred", "post-cutoff"}
FUSE_MIN = 10           # coordinate levels with n<10 (active) fuse per Greenacre
OTHER_RARE = "other-rare"
ORDINAL = {"tempo", "commit"}   # ordinal treatment for CATPCA twin only
ORDINAL_ORDER = {                # register order (low->high); used for CATPCA spline scoring
    "tempo": ["low", "med", "high"],
    "commit": ["instant", "channel", "reserve"],  # placeholder-safe: rank by observed if mismatch
}
SEED = 20260714
N_PERM_RETAIN = 1000    # parallel-analysis column-permutation nulls (Stage 2 dim retention)
N_PERM_GATEB = 10000    # Gate B permutation null draws
N_BOOT_GATED = 1000     # Gate D bootstrap iterations
BOOT_FRAC = 0.90        # Gate D subsample fraction
KNN_K = 10              # Leiden kNN
LEIDEN_RES = [round(0.5 + 0.1 * i, 1) for i in range(16)]  # 0.5..2.0 step 0.1
LEIDEN_SEEDS = 100
LCA_KMIN, LCA_KMAX, LCA_STARTS = 2, 12, 50

# Franchise rollup [A2] — 11 franchises. Keys are DB `game` codes.
FRANCHISE_ROLLUP = {
    "poe1": "PoE", "poe2": "PoE",
    "d2": "Diablo", "d3": "Diablo", "d4": "Diablo", "di": "Diablo",
    "tq": "TitanQuest", "tq2": "TitanQuest",
    "hades1": "Hades", "hades2": "Hades",
    "tl1": "Torchlight", "tl2": "Torchlight", "tli": "Torchlight",
    "gd": "gd", "le": "le", "vs": "vs",
    "chronicon": "chronicon", "hot": "hot", "undecember": "undecember",
}

# Gate-A expected group counts (from prereg §1 [A1])
GATEA_EXPECTED = {"WHIRLWIND": 15, "TOTEM-SENTRY": 24, "TRAP-MINE": 23,
                  "CHANNELED-BEAM": 9, "AURA": 8, "MINION-PET": 7}
GATEA_LARGE = {"WHIRLWIND", "TOTEM-SENTRY", "TRAP-MINE", "CHANNELED-BEAM"}
GATEA_SMALL_PERMITTED = {"AURA", "MINION-PET"}

np.random.seed(SEED)

REPORT = []   # accumulates gate-report markdown lines
AMEND = []    # protocol-amendment log lines


def rp(*a):
    line = " ".join(str(x) for x in a)
    REPORT.append(line)
    print(line)


def stop(reason):
    print("\n!!! STOP !!! " + reason)
    rp("\n## EXECUTION HALTED\n\n**STOP:** " + reason)
    _flush_report()
    sys.exit(2)


def _flush_report():
    with open(os.path.join(OUT, "2026-07-14-gate-report.md"), "w") as f:
        f.write("\n".join(REPORT) + "\n")


# ============================================================================
# STAGE 0 — hygiene + verification
# ============================================================================
def stage0(con):
    rp("# Atlas Derivation — Gate Report")
    rp("")
    rp("**Date:** 2026-07-14 · **Executor:** elrond · **Script:** `agentic_orchestration/research/scripts/atlas_derivation_2026_07_14.py`")
    rp("**Prereg:** `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (v1.1, PINNED)")
    rp("**Seed:** %d (all randomness pinned). **NUMBERS ONLY — interpretation is gandalf's.**" % SEED)
    rp("")
    rp("---")
    rp("")
    rp("## Stage 0 — verification")
    rp("")

    # snapshot marker
    meta = con.execute("SELECT version FROM corpus_schema_meta").fetchall()
    versions = [m[0] for m in meta]
    if "atlas-prereg-2026-07-14" not in versions:
        stop("snapshot marker 'atlas-prereg-2026-07-14' absent from corpus_schema_meta.")
    rp("- **Snapshot marker:** `atlas-prereg-2026-07-14` PRESENT in `corpus_schema_meta`. OK.")

    # active set
    rows = con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0 "
        "ORDER BY k.kit_id").fetchall()
    N = len(rows)
    if N != 469:
        stop("Active set N=%d, expected 469." % N)
    rp("- **Active set N = %d** (combat-kit, cell_key NOT NULL, negative=0). OK (== 469)." % N)

    # negatives accounting
    neg_all = con.execute("SELECT COUNT(*) FROM canon_corpus WHERE negative=1").fetchone()[0]
    neg_combat = con.execute(
        "SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=1").fetchone()[0]
    neg_sys = con.execute(
        "SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='system-record' AND c.negative=1").fetchone()[0]
    rp("- **Negatives:** %d total `negative=1` in canon_corpus; %d are combat-kit with cell_key "
       "(projectable supplementary set for Gate B); %d is a system-record "
       "(`vs-golden-egg-scaling`, per A.5 note — outside combat denominator, not projectable). "
       "Reconciliation: charter's \"38 graveyard\" = corpus count; fit-relevant projectable-negative count = %d."
       % (neg_all, neg_combat, neg_sys, neg_combat))

    # hard-constraint: survivor-key hash (proof snapshot is the byte-frozen state)
    concat = "\n".join("%s|%s" % (kid, ck) for kid, ck in rows)
    h = hashlib.sha256(concat.encode()).hexdigest()
    rp("- **Survivor-key SHA256** (469 rows, ordered by kit_id): `%s`" % h)

    # 14-field structural check
    bad = [kid for kid, ck in rows if len(ck.split("|")) != 14]
    if bad:
        stop("%d active rows not 14-field: %s" % (len(bad), bad[:5]))
    rp("- **Structural:** all %d active rows are exactly 14 pipe-delimited positions. OK." % N)

    kit_ids = [kid for kid, _ in rows]
    kit_vals = [ck.split("|") for _, ck in rows]

    # ---- Gate-A label table load (byte-verbatim) ----
    rp("")
    rp("### Stage 0a — Gate-A label table")
    lab_df = pd.read_csv(LABEL_CSV, dtype=str, keep_default_na=False)
    if list(lab_df.columns) != ["kit_id", "group", "group_intent_rationale"]:
        stop("Gate-A label CSV columns = %s, expected [kit_id, group, group_intent_rationale]" % list(lab_df.columns))
    if len(lab_df) != 86:
        stop("Gate-A label CSV has %d rows, expected 86." % len(lab_df))
    gc = Counter(lab_df["group"])
    for g, exp in GATEA_EXPECTED.items():
        if gc.get(g, 0) != exp:
            stop("Gate-A group %s count %d, expected %d." % (g, gc.get(g, 0), exp))
    rp("- Loaded **86 rows** byte-verbatim into `atlas_gateA_labels_2026_07_14`. Group counts: "
       + " · ".join("%s %d" % (g, gc[g]) for g in GATEA_EXPECTED) + ". OK.")
    con.execute("DROP TABLE IF EXISTS atlas_gateA_labels_2026_07_14")
    con.execute("CREATE TABLE atlas_gateA_labels_2026_07_14 "
                "(kit_id TEXT PRIMARY KEY, \"group\" TEXT, group_intent_rationale TEXT)")
    con.executemany("INSERT INTO atlas_gateA_labels_2026_07_14 VALUES (?,?,?)",
                    list(lab_df.itertuples(index=False, name=None)))
    con.commit()
    # verify every labelled kit is in the active set
    active_set = set(kit_ids)
    miss = [k for k in lab_df["kit_id"] if k not in active_set]
    if miss:
        stop("%d Gate-A labelled kits not in active set: %s" % (len(miss), miss[:5]))
    rp("- All 86 labelled kits present in the active set. OK.")
    kit_group = dict(zip(lab_df["kit_id"], lab_df["group"]))

    # ---- franchise rollup ----
    rp("")
    rp("### Stage 0b — franchise rollup [A2]")
    games = con.execute(
        "SELECT DISTINCT c.game FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0").fetchall()
    game_codes = sorted(g[0] for g in games)
    orphans = [g for g in game_codes if g not in FRANCHISE_ROLLUP]
    if orphans:
        stop("game codes outside the franchise rollup map: %s" % orphans)
    rp("- **%d distinct game codes** in active set, all in-map. No orphans. OK." % len(game_codes))
    # build kit->franchise
    kit_game = dict(con.execute(
        "SELECT k.kit_id, c.game FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0").fetchall())
    kit_franchise = {k: FRANCHISE_ROLLUP[g] for k, g in kit_game.items()}
    fr_counts = Counter(kit_franchise.values())
    if len(fr_counts) != 11:
        stop("franchise_rollup yielded %d franchises, expected 11." % len(fr_counts))
    rp("- **franchise_rollup materialized as lookup dict (kit_id -> franchise); 11 franchises**: "
       + " · ".join("%s %d" % (f, n) for f, n in fr_counts.most_common()) + ".")
    rp("- Rollup map (game -> franchise): "
       + " · ".join("%s->%s" % (g, FRANCHISE_ROLLUP[g]) for g in game_codes))
    # also persist to DB as a table for reproducibility
    con.execute("DROP TABLE IF EXISTS atlas_franchise_rollup")
    con.execute("CREATE TABLE atlas_franchise_rollup (kit_id TEXT PRIMARY KEY, game TEXT, franchise_rollup TEXT)")
    con.executemany("INSERT INTO atlas_franchise_rollup VALUES (?,?,?)",
                    [(k, kit_game[k], kit_franchise[k]) for k in kit_ids])
    con.commit()

    # ---- rare-category fusing (Greenacre, once, identical across families) ----
    rp("")
    rp("### Stage 0c — rare-category fusing (Greenacre, n<%d)" % FUSE_MIN)
    fuse_map = {}   # (coord_idx, raw_level) -> fused_level ; only for levels that fuse
    fuse_report = []
    for i, nm in enumerate(NAMES):
        c = Counter(v[i] for v in kit_vals if v[i] not in MASK)
        rare = {lv: n for lv, n in c.items() if n < FUSE_MIN}
        if rare:
            for lv in rare:
                fuse_map[(i, lv)] = OTHER_RARE
            fuse_report.append((nm, sorted(rare.items(), key=lambda x: x[1])))
    if fuse_report:
        rp("- The prereg (§1) fuses n<10 levels into a register-parent bucket; the prereg names no "
           "per-level parent, so per brief the fused level is **\"other-rare\"** per coordinate. "
           "Map computed ONCE, applied identically across all four families:")
        for nm, items in fuse_report:
            rp("  - **%s** -> other-rare: %s" % (nm, ", ".join("%s(%d)" % (lv, n) for lv, n in items)))
    else:
        rp("- No levels below n<%d after masking. No fusing applied." % FUSE_MIN)
    rp("- **Note:** fusing applies to MCA/MDS/Leiden/LCA *input levels* (stability measure). "
       "Gate-A labels come from the frozen CSV by kit_id, independent of fused levels — fusing "
       "does not alter group membership (e.g. geometry=aura fuses in the MCA input, but the AURA "
       "group is defined by kit_id in the label table).")

    def apply_fuse(vals):
        """Return fused categorical value list (masks preserved as-is)."""
        out = []
        for i in range(14):
            v = vals[i]
            if v in MASK:
                out.append(v)
            else:
                out.append(fuse_map.get((i, v), v))
        return out

    kit_fused = [apply_fuse(v) for v in kit_vals]

    return {
        "N": N, "kit_ids": kit_ids, "kit_vals": kit_vals, "kit_fused": kit_fused,
        "kit_group": kit_group, "kit_franchise": kit_franchise, "kit_game": kit_game,
        "fuse_map": fuse_map, "apply_fuse": apply_fuse,
    }


# ============================================================================
# STAGE 1 — diagnostics
# ============================================================================
def norm_entropy(values):
    c = Counter(v for v in values if v not in MASK)
    tot = sum(c.values())
    if tot == 0 or len(c) <= 1:
        return 0.0
    H = -sum((n / tot) * math.log(n / tot) for n in c.values())
    return H / math.log(len(c)) if len(c) > 1 else 0.0


def cramers_v(a, b):
    """Bias-corrected Cramer's V on two aligned categorical lists (masks dropped pairwise)."""
    pairs = [(x, y) for x, y in zip(a, b) if x not in MASK and y not in MASK]
    if len(pairs) < 3:
        return np.nan, np.nan
    ax = [p[0] for p in pairs]; bx = [p[1] for p in pairs]
    ca = sorted(set(ax)); cb = sorted(set(bx))
    if len(ca) < 2 or len(cb) < 2:
        return 0.0, 1.0
    ia = {v: i for i, v in enumerate(ca)}; ib = {v: i for i, v in enumerate(cb)}
    tbl = np.zeros((len(ca), len(cb)))
    for x, y in pairs:
        tbl[ia[x], ib[y]] += 1
    chi2, p, _, _ = chi2_contingency(tbl, correction=False)
    n = tbl.sum()
    phi2 = chi2 / n
    r, k = tbl.shape
    phi2corr = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rcorr = r - (r - 1) ** 2 / (n - 1)
    kcorr = k - (k - 1) ** 2 / (n - 1)
    denom = min(kcorr - 1, rcorr - 1)
    v = math.sqrt(phi2corr / denom) if denom > 0 else 0.0
    return v, p


def mutual_info(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x not in MASK and y not in MASK]
    if len(pairs) < 3:
        return np.nan
    n = len(pairs)
    ca = Counter(p[0] for p in pairs); cb = Counter(p[1] for p in pairs)
    cab = Counter(pairs)
    mi = 0.0
    for (x, y), nxy in cab.items():
        pxy = nxy / n; px = ca[x] / n; py = cb[y] / n
        mi += pxy * math.log(pxy / (px * py))
    # normalize by min marginal entropy -> [0,1]
    Ha = -sum((n_ / n) * math.log(n_ / n) for n_ in ca.values())
    Hb = -sum((n_ / n) * math.log(n_ / n) for n_ in cb.values())
    denom = min(Ha, Hb)
    return mi / denom if denom > 0 else 0.0


def bh_fdr(pvals, q=0.05):
    """Benjamini-Hochberg. Returns boolean reject array aligned to input order."""
    p = np.asarray(pvals, float)
    ok = ~np.isnan(p)
    idx = np.where(ok)[0]
    m = len(idx)
    reject = np.zeros(len(p), bool)
    if m == 0:
        return reject
    order = idx[np.argsort(p[idx])]
    thresh = q * (np.arange(1, m + 1)) / m
    passed = p[order] <= thresh
    if passed.any():
        kmax = np.max(np.where(passed)[0])
        reject[order[:kmax + 1]] = True
    return reject


def stage1(st):
    rp("")
    rp("---")
    rp("")
    rp("## Stage 1 — diagnostics (pre-decomposition)")
    kit_fused = st["kit_fused"]
    cols = [[row[i] for row in kit_fused] for i in range(14)]

    rp("")
    rp("### 1.1 Per-coordinate normalized entropy (0–1; <0.1 flagged, NOT dropped)")
    rp("")
    rp("| coord | levels (post-fuse, non-mask) | mask n | entropy |")
    rp("|---|---|---|---|")
    ent = {}
    for i, nm in enumerate(NAMES):
        e = norm_entropy(cols[i])
        ent[nm] = e
        lv = len(set(v for v in cols[i] if v not in MASK))
        mk = sum(1 for v in cols[i] if v in MASK)
        flag = " ⚠<0.1" if e < 0.1 else ""
        rp("| %s | %d | %d | %.3f%s |" % (nm, lv, mk, e, flag))

    rp("")
    rp("### 1.2 Pairwise association — Cramér's V + normalized MI, BH-FDR q=0.05 (78 pairs)")
    pairs = list(itertools.combinations(range(14), 2))
    recs = []
    for i, j in pairs:
        v, p = cramers_v(cols[i], cols[j])
        mi = mutual_info(cols[i], cols[j])
        recs.append({"a": NAMES[i], "b": NAMES[j], "cramers_v": v, "mi_norm": mi, "p": p})
    pvec = [r["p"] for r in recs]
    rej = bh_fdr(pvec, 0.05)
    for r, rj in zip(recs, rej):
        r["fdr_sig"] = bool(rj)
    nsig = sum(1 for r in recs if r["fdr_sig"])
    dup = [r for r in recs if r["fdr_sig"] and (not np.isnan(r["cramers_v"])) and r["cramers_v"] > 0.8]
    rp("")
    rp("- **%d of 78 pairs FDR-significant** (q=0.05)." % nsig)
    rp("- **Near-duplicate candidates (V>0.8 AND FDR-sig):** %s (retained for v1 per prereg §3.2; demotion is Edition-II)."
       % (", ".join("%s~%s(V=%.2f)" % (r["a"], r["b"], r["cramers_v"]) for r in dup) if dup else "NONE"))
    rp("")
    rp("Top 15 pairs by Cramér's V:")
    rp("")
    rp("| a | b | Cramér's V | MI(norm) | p | FDR-sig |")
    rp("|---|---|---|---|---|---|")
    for r in sorted(recs, key=lambda x: -(x["cramers_v"] if not np.isnan(x["cramers_v"]) else -1))[:15]:
        rp("| %s | %s | %.3f | %.3f | %.2e | %s |"
           % (r["a"], r["b"], r["cramers_v"], r["mi_norm"], r["p"], "Y" if r["fdr_sig"] else "n"))

    rp("")
    rp("### 1.3 Category frequency tables post-fuse (the exact input the decomposition sees)")
    rp("")
    for i, nm in enumerate(NAMES):
        c = Counter(cols[i])
        parts = ", ".join("%s=%d" % (lv, n) for lv, n in c.most_common())
        rp("- **%s:** %s" % (nm, parts))

    st["entropy"] = ent
    st["assoc"] = recs
    return st


# ============================================================================
# Indicator matrix + MCA (Greenacre) + MFA block weighting
# ============================================================================
def build_indicator(kit_fused, block_weight=True, ordinal_split=False):
    """
    Build MCA indicator matrix over the 14 coordinates -> 14 MFA blocks.
    Masks are PASSIVE: a masked cell contributes 0 to every indicator column of
    that coordinate (row is all-zero for that block) -> zero inertia contribution.
    Returns (Z, col_meta, block_of_col, block_first_sv).
      block_weight: divide each block by its first singular value (MFA).
      ordinal_split: unused here (CATPCA twin handled separately).
    """
    N = len(kit_fused)
    col_meta = []      # (coord_name, level)
    block_of_col = []  # block id per column (0..13)
    columns = []
    for i, nm in enumerate(NAMES):
        levels = sorted(set(row[i] for row in kit_fused if row[i] not in MASK))
        for lv in levels:
            col = np.array([1.0 if row[i] == lv else 0.0 for row in kit_fused])
            columns.append(col)
            col_meta.append((nm, lv))
            block_of_col.append(i)
    Z = np.array(columns).T   # N x Q
    block_of_col = np.array(block_of_col)
    # MFA block weighting: each block's first singular value from its own SVD
    first_sv = np.ones(14)
    if block_weight:
        for b in range(14):
            cols_b = Z[:, block_of_col == b]
            if cols_b.shape[1] == 0:
                continue
            # center block then first singular value
            cb = cols_b - cols_b.mean(0, keepdims=True)
            try:
                sv = sla.svd(cb, compute_uv=False)
                first_sv[b] = sv[0] if len(sv) and sv[0] > 1e-12 else 1.0
            except Exception:
                first_sv[b] = 1.0
        for b in range(14):
            Z[:, block_of_col == b] /= first_sv[b]
    return Z, col_meta, block_of_col, first_sv


def mca_greenacre(Z, col_meta, n_coords=14):
    """
    Classic CA on the (weighted) indicator matrix Z.
    Greenacre-adjusted inertia: only eigenvalues > 1/K contribute; adjusted rates
    per Greenacre (1993). Returns dict with coords (row principal), loadings, inertia.
    """
    N, Q = Z.shape
    grand = Z.sum()
    P = Z / grand
    r = P.sum(1)          # row masses
    c = P.sum(0)          # col masses
    r[r == 0] = 1e-12
    c[c == 0] = 1e-12
    Dr_inv_sqrt = 1.0 / np.sqrt(r)
    Dc_inv_sqrt = 1.0 / np.sqrt(c)
    S = (Dr_inv_sqrt[:, None]) * (P - np.outer(r, c)) * (Dc_inv_sqrt[None, :])
    U, sv, Vt = sla.svd(S, full_matrices=False)
    eig = sv ** 2                       # principal inertias (eigenvalues)
    # standard row principal coordinates
    row_pc = (Dr_inv_sqrt[:, None]) * U * sv[None, :]
    col_pc = (Dc_inv_sqrt[:, None]) * Vt.T * sv[None, :]

    K = n_coords
    total_raw = eig.sum()
    # Greenacre adjustment: keep dims with sqrt(eig) > 1/K
    mask = np.sqrt(eig) > (1.0 / K)
    adj = np.where(mask, (K / (K - 1.0)) ** 2 * (np.sqrt(eig) - 1.0 / K) ** 2, 0.0)
    greenacre_total = ((K / (K - 1.0)) *
                       (np.sum(eig[np.sqrt(eig) > 1.0 / K]) - (Q - K) / (K ** 2)))
    if greenacre_total <= 0:
        greenacre_total = adj.sum() if adj.sum() > 0 else total_raw
    adj_rate = adj / greenacre_total
    return {
        "eig": eig, "sv": sv, "row_pc": row_pc, "col_pc": col_pc,
        "col_meta": col_meta, "total_raw": total_raw,
        "greenacre_adj": adj, "greenacre_total": greenacre_total,
        "greenacre_rate": adj_rate, "U": U, "Vt": Vt,
    }


def parallel_analysis_mca(kit_fused, observed_adj, n_perm, seed, block_weight=True):
    """Column-permutation nulls: permute each coordinate independently, rebuild
    indicator, take GREENACRE-CORRECTED inertia (prereg §4: 'retain dimensions whose
    CORRECTED inertia exceeds the 95th percentile of the null'). Retain leading
    contiguous dims whose observed corrected inertia > 95th-pct null."""
    rng = np.random.default_rng(seed)
    N = len(kit_fused)
    ncomp = len(observed_adj)
    null_adj = np.zeros((n_perm, ncomp))
    base = [list(row) for row in kit_fused]
    for t in range(n_perm):
        perm = [row[:] for row in base]
        for i in range(14):
            colvals = [perm[k][i] for k in range(N)]
            rng.shuffle(colvals)
            for k in range(N):
                perm[k][i] = colvals[k]
        Zp, cm, _, _ = build_indicator(perm, block_weight=block_weight)
        mp = mca_greenacre(Zp, cm)
        a = mp["greenacre_adj"]
        null_adj[t, :min(ncomp, len(a))] = a[:min(ncomp, len(a))]
    p95 = np.percentile(null_adj, 95, axis=0)
    retain = observed_adj > p95
    # retain contiguous leading dims
    nret = 0
    for i in range(ncomp):
        if retain[i]:
            nret += 1
        else:
            break
    return max(1, nret), p95, null_adj


# ============================================================================
# Gower distance + classical MDS
# ============================================================================
def gower_matrix(kit_fused):
    """Gower dissimilarity for all-categorical data with missing (mask) handling.
    d(i,j) = mean over coords present in both of [x_i != x_j]. Equal weights.
    Vectorized: integer-encode each coordinate (masks -> -1), broadcast per-coord."""
    N = len(kit_fused)
    codes = np.empty((N, 14), dtype=np.int32)
    for c in range(14):
        vals = [row[c] for row in kit_fused]
        mp = {}
        for k, v in enumerate(vals):
            if v in MASK:
                codes[k, c] = -1
            else:
                codes[k, c] = mp.setdefault(v, len(mp))
    present = codes >= 0                       # N x 14 bool
    both = np.zeros((N, N), dtype=np.float64)   # count of coords present in both
    ne = np.zeros((N, N), dtype=np.float64)     # count of coords differing (present in both)
    for c in range(14):
        pc = present[:, c].astype(np.float64)
        bc = np.outer(pc, pc)                    # 1 where both present
        both += bc
        col = codes[:, c]
        eq = (col[:, None] == col[None, :]).astype(np.float64)
        ne += bc * (1.0 - eq)                    # differ AND both present
    with np.errstate(divide="ignore", invalid="ignore"):
        D = np.where(both > 0, ne / both, 0.0)
    np.fill_diagonal(D, 0.0)
    return D


def classical_mds(D, ndim=None):
    N = D.shape[0]
    D2 = D ** 2
    J = np.eye(N) - np.ones((N, N)) / N
    B = -0.5 * J @ D2 @ J
    B = (B + B.T) / 2
    w, V = sla.eigh(B)
    order = np.argsort(w)[::-1]
    w = w[order]; V = V[:, order]
    pos = w > 1e-9
    coords = V[:, pos] * np.sqrt(w[pos])
    eig = w.copy()
    if ndim is not None:
        coords = coords[:, :ndim]
    return coords, eig


def parallel_analysis_mds(kit_fused, observed_eig, n_perm, seed):
    rng = np.random.default_rng(seed + 7)
    N = len(kit_fused)
    ncomp = min(len(observed_eig), 15)
    null_eigs = np.zeros((n_perm, ncomp))
    base = [list(row) for row in kit_fused]
    for t in range(n_perm):
        perm = [row[:] for row in base]
        for i in range(14):
            colvals = [perm[k][i] for k in range(N)]
            rng.shuffle(colvals)
            for k in range(N):
                perm[k][i] = colvals[k]
        Dp = gower_matrix(perm)
        _, e = classical_mds(Dp)
        e = e[e > 0]
        null_eigs[t, :min(ncomp, len(e))] = e[:min(ncomp, len(e))]
    p95 = np.percentile(null_eigs, 95, axis=0)
    obs = observed_eig[observed_eig > 0][:ncomp]
    retain = obs > p95[:len(obs)]
    nret = 0
    for i in range(len(obs)):
        if retain[i]:
            nret += 1
        else:
            break
    return max(1, nret), p95


# ============================================================================
# Leiden (CPM) on kNN graph
# ============================================================================
def leiden_consensus(D, k, resolutions, n_seeds, seed):
    import igraph as ig
    import leidenalg
    N = D.shape[0]
    # kNN graph (mutual-or edges), weight = 1 - dist (similarity)
    edges = set()
    for i in range(N):
        order = np.argsort(D[i])
        cnt = 0
        for j in order:
            if j == i:
                continue
            edges.add((min(i, j), max(i, j)))
            cnt += 1
            if cnt >= k:
                break
    elist = sorted(edges)
    weights = [1.0 - D[i, j] for (i, j) in elist]
    g = ig.Graph(n=N, edges=elist)
    g.es["weight"] = weights

    res_profile = []   # (resolution, median_nclusters, consensus_partition_membership)
    for res in resolutions:
        memberships = []
        ncl = []
        for s in range(n_seeds):
            part = leidenalg.find_partition(
                g, leidenalg.CPMVertexPartition,
                weights="weight", resolution_parameter=res, seed=seed + s, n_iterations=-1)
            m = np.array(part.membership)
            memberships.append(m)
            ncl.append(len(set(m)))
        # consensus via co-association -> single Leiden pass on co-assoc graph
        co = np.zeros((N, N))
        for m in memberships:
            same = (m[:, None] == m[None, :]).astype(float)
            co += same
        co /= n_seeds
        # consensus membership: threshold co-assoc at 0.5, connected components via Leiden CPM res=0.05
        cg = ig.Graph.Weighted_Adjacency((co * (co >= 0.5)).tolist(), mode="undirected", loops=False)
        cpart = leidenalg.find_partition(
            cg, leidenalg.CPMVertexPartition, weights="weight",
            resolution_parameter=0.05, seed=seed, n_iterations=-1)
        cons = np.array(cpart.membership)
        res_profile.append((res, int(np.median(ncl)), len(set(cons)), cons))
    return res_profile


def find_plateau(res_profile, N):
    """Return the resolution whose consensus-cluster-count is stable across >=3
    consecutive resolution steps (the plateau). A partition of N singletons or 1
    giant cluster is DEGENERATE and is not selected as the usable partition (it is
    still reported in the profile). Returns (res, membership, plateau_range,
    cluster_count, degenerate_flag)."""
    counts = [rp_[2] for rp_ in res_profile]

    def nondegenerate(c):
        return 1 < c < N

    # first pass: >=3-step plateau at a NON-degenerate cluster count
    i = 0
    while i < len(counts):
        j = i
        while j + 1 < len(counts) and counts[j + 1] == counts[i]:
            j += 1
        if (j - i + 1) >= 3 and nondegenerate(counts[i]):
            mid = (i + j) // 2
            return (res_profile[mid][0], res_profile[mid][3],
                    (res_profile[i][0], res_profile[j][0]), counts[i], False)
        i = j + 1
    # second pass: modal NON-degenerate cluster count, middle resolution of its run
    nd_idx = [k for k, c in enumerate(counts) if nondegenerate(c)]
    if nd_idx:
        from collections import Counter as C
        modal = C(counts[k] for k in nd_idx).most_common(1)[0][0]
        idxs = [k for k in nd_idx if counts[k] == modal]
        mid = idxs[len(idxs) // 2]
        return res_profile[mid][0], res_profile[mid][3], None, modal, False
    # everything degenerate: return the least-degenerate (smallest resolution) but flag it
    idx = int(np.argmin(counts)) if max(counts) == N else int(np.argmax(counts))
    return res_profile[idx][0], res_profile[idx][3], None, counts[idx], True


# ============================================================================
# LCA via stepmix
# ============================================================================
def run_lca(kit_fused, kmin, kmax, starts, seed):
    from stepmix.stepmix import StepMix
    N = len(kit_fused)
    # encode each coordinate as integer categories; masks -> their own category (passive-ish;
    # stepmix has no passive, so mask becomes an explicit level — reported)
    enc = np.zeros((N, 14), dtype=int)
    maps = []
    for i in range(14):
        vals = sorted(set(row[i] for row in kit_fused))
        m = {v: idx for idx, v in enumerate(vals)}
        maps.append(m)
        for k in range(N):
            enc[k, i] = m[kit_fused[k][i]]
    X = pd.DataFrame(enc, columns=NAMES)
    rows = []
    best = None
    for K in range(kmin, kmax + 1):
        model = StepMix(n_components=K, measurement="categorical",
                        n_init=starts, random_state=seed, max_iter=200, verbose=0)
        model.fit(X)
        ll = model.score(X) * N          # score = avg log-lik per sample
        n_params = model.n_parameters if hasattr(model, "n_parameters") else _lca_nparams(K, maps)
        bic = -2 * ll + n_params * math.log(N)
        aic = -2 * ll + 2 * n_params
        # sample-size-adjusted BIC
        sabic = -2 * ll + n_params * math.log((N + 2) / 24.0)
        # entropy of classification
        post = model.predict_proba(X)
        with np.errstate(divide="ignore", invalid="ignore"):
            ent = -np.nansum(post * np.log(post + 1e-12))
        rel_ent = 1.0 - ent / (N * math.log(K)) if K > 1 else 1.0
        labels = model.predict(X)
        rows.append({"k": K, "loglik": ll, "nparams": n_params, "BIC": bic,
                     "AIC": aic, "sABIC": sabic, "entropy_R2": rel_ent})
        if best is None or bic < best["BIC"]:
            best = {"k": K, "BIC": bic, "labels": np.asarray(labels), "model": model}
    return rows, best


def _lca_nparams(K, maps):
    ncat = sum(len(m) for m in maps)
    return (K - 1) + K * (ncat - 14)


# ============================================================================
# Clustering helpers for gates
# ============================================================================
def silhouette_per_group(coords, labels_dict, kit_ids):
    """Silhouette per named group using euclidean on coords, only over labelled points."""
    idx = {kid: i for i, kid in enumerate(kit_ids)}
    lab_ids = [k for k in labels_dict if k in idx]
    pts = np.array([coords[idx[k]] for k in lab_ids])
    labs = np.array([labels_dict[k] for k in lab_ids])
    from sklearn.metrics import silhouette_samples
    if len(set(labs)) < 2:
        return {}
    s = silhouette_samples(pts, labs)
    out = {}
    for g in sorted(set(labs)):
        out[g] = float(np.mean(s[labs == g]))
    return out


def ari(a, b):
    from sklearn.metrics import adjusted_rand_score
    return adjusted_rand_score(a, b)


# ============================================================================
# STAGE 2 — the four families
# ============================================================================
def stage2(st):
    rp("")
    rp("---")
    rp("")
    rp("## Stage 2 — four method families")
    kit_fused = st["kit_fused"]
    kit_ids = st["kit_ids"]
    N = st["N"]

    # ---- 2a MCA ----
    rp("")
    rp("### 2a — MCA (Greenacre-corrected, MFA block-weighted)")
    Z, col_meta, block_of_col, first_sv = build_indicator(kit_fused, block_weight=True)
    mca = mca_greenacre(Z, col_meta)
    rp("- Indicator matrix: %d rows × %d columns (14 MFA blocks; masks passive = zero-inertia rows within block)."
       % Z.shape)
    rp("- MFA block first-singular-values (weights): "
       + ", ".join("%s=%.3f" % (NAMES[b], first_sv[b]) for b in range(14)))
    # parallel analysis retention — on GREENACRE-CORRECTED inertia per prereg §4
    nret_mca, p95_mca, _ = parallel_analysis_mca(kit_fused, mca["greenacre_adj"], N_PERM_RETAIN, SEED)
    rp("- **Parallel analysis** (%d column-permutation nulls): retain **%d dimensions** (leading dims whose "
       "**Greenacre-corrected inertia** exceeds the 95th-pct null, per prereg §4)." % (N_PERM_RETAIN, nret_mca))
    rp("")
    rp("| dim | raw eig | Greenacre-adj inertia | Greenacre-adj %% | null-95 (corrected) | retained |")
    rp("|---|---|---|---|---|---|")
    show = max(nret_mca + 3, 6)
    for d in range(min(show, len(mca["eig"]))):
        rp("| %d | %.5f | %.5f | %.2f | %.5f | %s |"
           % (d + 1, mca["eig"][d], mca["greenacre_adj"][d],
              100 * mca["greenacre_rate"][d], p95_mca[d] if d < len(p95_mca) else float("nan"),
              "Y" if d < nret_mca else "n"))
    mca_coords = mca["row_pc"][:, :nret_mca]
    st["mca"] = {"coords": mca_coords, "nret": nret_mca, "col_pc": mca["col_pc"],
                 "col_meta": col_meta, "eig": mca["eig"], "greenacre_rate": mca["greenacre_rate"],
                 "greenacre_total": mca["greenacre_total"], "total_raw": mca["total_raw"]}

    # CATPCA twin (ordinal on tempo+commit) — divergence diagnostic
    rp("")
    rp("- **CATPCA twin** (ordinal spline on tempo+commit only): implemented as MCA with tempo/commit "
       "replaced by their register-ordinal integer score (single quantified column each), other coords nominal.")
    catpca_coords, catpca_nret, catpca_ari = catpca_twin(kit_fused, kit_ids, mca_coords, nret_mca)
    rp("  - CATPCA retained **%d dims**; ARI(CATPCA k-means vs MCA k-means, k=%d) = **%.3f** "
       "(divergence-as-diagnostic per prereg §2)." % (catpca_nret, nret_mca + 2, catpca_ari))

    # ---- 2b Gower -> MDS ----
    rp("")
    rp("### 2b — Gower dissimilarity → classical (Torgerson) MDS")
    D = gower_matrix(kit_fused)
    st["gower"] = D
    mds_coords_full, mds_eig = classical_mds(D)
    nret_mds, p95_mds = parallel_analysis_mds(kit_fused, mds_eig, N_PERM_RETAIN, SEED)
    rp("- Gower matrix %d×%d (equal coordinate weights; masks = missing per Gower). "
       "Classical MDS eigen-scree below." % D.shape)
    rp("- **Parallel analysis** (%d nulls): retain **%d dimensions**." % (N_PERM_RETAIN, nret_mds))
    rp("")
    rp("| dim | eigenvalue | inertia %% | null-95 | retained |")
    rp("|---|---|---|---|---|")
    pos_eig = mds_eig[mds_eig > 0]
    tot_pos = pos_eig.sum()
    show = max(nret_mds + 3, 6)
    for d in range(min(show, len(pos_eig))):
        rp("| %d | %.5f | %.2f | %.5f | %s |"
           % (d + 1, pos_eig[d], 100 * pos_eig[d] / tot_pos,
              p95_mds[d] if d < len(p95_mds) else float("nan"), "Y" if d < nret_mds else "n"))
    mds_coords = mds_coords_full[:, :nret_mds]
    st["mds"] = {"coords": mds_coords, "nret": nret_mds, "eig": mds_eig}

    # ---- 2c Leiden ----
    rp("")
    rp("### 2c — Leiden communities (CPM, kNN k=%d)" % KNN_K)
    try:
        res_profile = leiden_consensus(D, KNN_K, LEIDEN_RES, LEIDEN_SEEDS, SEED)
        leiden_res, leiden_mem, plateau_range, plateau_count, degen = find_plateau(res_profile, N)
        rp("- Leiden-CPM available (leidenalg + python-igraph). kNN k=%d, %d seeds/resolution, "
           "resolution sweep %.1f–%.1f step 0.1. Edge weight = 1−Gower (similarity)."
           % (KNN_K, LEIDEN_SEEDS, LEIDEN_RES[0], LEIDEN_RES[-1]))
        rp("")
        rp("| resolution | median #clusters (per-seed) | consensus #clusters |")
        rp("|---|---|---|")
        for res, medncl, consncl, _ in res_profile:
            rp("| %.1f | %d | %d |" % (res, medncl, consncl))
        if degen:
            rp("- **All resolutions in the pinned sweep 0.5–2.0 yield DEGENERATE partitions** "
               "(either N=%d singletons or 1 giant cluster) under CPM on this similarity graph. "
               "Consensus witness has NO usable non-degenerate partition. Reported at resolution %.1f "
               "(least-degenerate). This is a numeric result of the pinned parameters, NOT a substitution."
               % (N, leiden_res))
        elif plateau_range:
            rp("- **Plateau:** consensus cluster count = %d stable across resolutions %.1f–%.1f. "
               "Consensus partition taken at resolution %.1f."
               % (plateau_count, plateau_range[0], plateau_range[1], leiden_res))
        else:
            rp("- **No ≥3-step non-degenerate plateau;** modal non-degenerate consensus count = %d; "
               "consensus taken at resolution %.1f." % (plateau_count, leiden_res))
        st["leiden"] = {"membership": leiden_mem, "resolution": leiden_res,
                        "profile": res_profile, "degenerate": degen, "ncons": plateau_count}
    except Exception as e:
        # A7 clause: Leiden failure is an AMENDMENT, never a silent Louvain swap.
        AMEND.append("Leiden-CPM FAILED at runtime (%s). Per A7 this requires a logged protocol "
                     "amendment + jack-ryan visibility BEFORE substitution. NO silent Louvain swap performed. "
                     "Clustering-witness 2c is MARKED UNCOMPUTED." % type(e).__name__)
        rp("- **Leiden UNCOMPUTED — runtime failure: %s.** Per A7, NOT silently substituted. See §amendments." % e)
        st["leiden"] = None

    # ---- 2d LCA ----
    rp("")
    rp("### 2d — Latent Class Analysis (BIC-selected, k=%d..%d)" % (LCA_KMIN, LCA_KMAX))
    try:
        lca_rows, lca_best = run_lca(kit_fused, LCA_KMIN, LCA_KMAX, LCA_STARTS, SEED)
        rp("- stepmix categorical LCA, %d starts/k. Masks enter as explicit levels (stepmix has no passive "
           "category — reported deviation from MCA's passive treatment; noted, not silent)." % LCA_STARTS)
        rp("")
        rp("| k | loglik | #params | BIC | AIC | sABIC | entropy R² |")
        rp("|---|---|---|---|---|---|---|")
        for r in lca_rows:
            star = " ⭐" if r["k"] == lca_best["k"] else ""
            rp("| %d | %.1f | %d | %.1f | %.1f | %.1f | %.3f%s |"
               % (r["k"], r["loglik"], r["nparams"], r["BIC"], r["AIC"], r["sABIC"], r["entropy_R2"], star))
        rp("- **BIC-selected k = %d** (⭐)." % lca_best["k"])
        st["lca"] = {"labels": lca_best["labels"], "k": lca_best["k"], "rows": lca_rows}
    except Exception as e:
        AMEND.append("LCA (stepmix) FAILED at runtime (%s). LCA witness 2d marked UNCOMPUTED." % type(e).__name__)
        rp("- **LCA UNCOMPUTED — runtime failure: %s.** See §amendments." % e)
        st["lca"] = None

    # ---- cross-family agreement (ARI matrix) ----
    rp("")
    rp("### 2e — cross-family agreement (ARI)")
    from sklearn.cluster import KMeans
    # k-means on retained MCA dims and MDS dims at a common k. Use non-degenerate Leiden
    # consensus count if available, else LCA-BIC k, else the 6 Gate-A groups.
    kcommon = None
    if st.get("leiden") and not st["leiden"].get("degenerate"):
        kcommon = len(set(st["leiden"]["membership"]))
    if not kcommon or kcommon < 2 or kcommon >= mca_coords.shape[0]:
        kcommon = st["lca"]["k"] if st.get("lca") else len(GATEA_EXPECTED)
    km_mca = KMeans(n_clusters=kcommon, random_state=SEED, n_init=25).fit_predict(mca_coords)
    km_mds = KMeans(n_clusters=kcommon, random_state=SEED, n_init=25).fit_predict(mds_coords)
    parts = {"MCA-kmeans": km_mca, "MDS-kmeans": km_mds}
    if st.get("leiden"):
        tag = "Leiden(DEGEN)" if st["leiden"].get("degenerate") else "Leiden"
        parts[tag] = st["leiden"]["membership"]
    if st.get("lca"):
        parts["LCA"] = st["lca"]["labels"]
    names = list(parts.keys())
    rp("- Common k = %d for k-means witnesses (non-degenerate Leiden consensus count if available, "
       "else LCA-BIC k, else 6). ARI matrix (note: a degenerate Leiden partition scores ~0 vs all "
       "others by construction — reported for transparency):" % kcommon)
    rp("")
    rp("| | " + " | ".join(names) + " |")
    rp("|" + "---|" * (len(names) + 1))
    for a in names:
        cells = []
        for b in names:
            cells.append("%.3f" % ari(parts[a], parts[b]))
        rp("| %s | %s |" % (a, " | ".join(cells)))
    st["parts"] = parts
    st["kcommon"] = kcommon
    st["km_mca"] = km_mca
    return st


def catpca_twin(kit_fused, kit_ids, mca_coords, nret):
    """MCA with tempo+commit quantified to ordinal integer scores (single numeric col each)."""
    N = len(kit_fused)
    # build modified indicator: nominal coords as indicators, tempo/commit as one standardized numeric col
    col_meta = []
    columns = []
    block_of_col = []
    for i, nm in enumerate(NAMES):
        if nm in ORDINAL:
            # ordinal score by register order; unknown/mask -> mean (passive-ish -> 0 after centering)
            order = ORDINAL_ORDER[nm]
            present = [row[i] for row in kit_fused if row[i] not in MASK]
            uniq = sorted(set(present), key=lambda v: order.index(v) if v in order else 99)
            score_map = {v: rank for rank, v in enumerate(uniq)}
            col = []
            for row in kit_fused:
                v = row[i]
                col.append(float(score_map[v]) if v not in MASK else np.nan)
            col = np.array(col)
            mu = np.nanmean(col)
            col = np.where(np.isnan(col), mu, col)
            col = (col - col.mean()) / (col.std() + 1e-12)
            columns.append(col); col_meta.append((nm, "ordinal")); block_of_col.append(i)
        else:
            levels = sorted(set(row[i] for row in kit_fused if row[i] not in MASK))
            for lv in levels:
                columns.append(np.array([1.0 if row[i] == lv else 0.0 for row in kit_fused]))
                col_meta.append((nm, lv)); block_of_col.append(i)
    Z = np.array(columns).T
    # simple PCA (center + SVD) on this mixed matrix
    Zc = Z - Z.mean(0, keepdims=True)
    U, sv, Vt = sla.svd(Zc, full_matrices=False)
    coords = U[:, :max(nret, 2)] * sv[:max(nret, 2)]
    from sklearn.cluster import KMeans
    k = nret + 2
    a = KMeans(n_clusters=k, random_state=SEED, n_init=25).fit_predict(coords[:, :nret])
    b = KMeans(n_clusters=k, random_state=SEED, n_init=25).fit_predict(mca_coords)
    return coords, nret, ari(a, b)


# ============================================================================
# STAGE 3 — the four gates
# ============================================================================
def plane_diameter(coords):
    d = pdist(coords, metric="euclidean")
    return float(d.max())


def project_supplementary(con, st):
    """Project the 37 projectable negatives into the MCA retained space (supplementary,
    zero mass). Partial keys -> passive (mask) per Stage 0. Returns dict kit_id->coord."""
    negs = con.execute(
        "SELECT k.kit_id, k.cell_key, c.death_class FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=1 "
        "ORDER BY k.kit_id").fetchall()
    apply_fuse = st["apply_fuse"]
    mca = st["mca"]
    col_meta = mca["col_meta"]
    # rebuild the column index map + block weights from the ACTIVE fit
    # supplementary row profile projected via column standard coordinates
    # Reconstruct col standard coordinates: col_pc / sqrt(col mass)... we use transition formula:
    # f_supp = (1/row_total) * sum over present levels of (indicator * col_standard_coord)
    # Build active indicator meta to recover column standard coords consistent with fit.
    kit_fused = st["kit_fused"]
    Z, cm, block_of_col, first_sv = build_indicator(kit_fused, block_weight=True)
    mca2 = mca_greenacre(Z, cm)
    # column standard coordinates = col_pc / sv  (CA transition: row_std = col_profile weighted)
    sv = mca2["sv"]
    nret = mca["nret"]
    col_std = mca2["col_pc"][:, :nret] / sv[:nret][None, :]
    colidx = {lvl: i for i, lvl in enumerate(cm)}
    # column masses from the active fit
    grand = Z.sum()
    c_mass = Z.sum(0) / grand

    out = {}
    death = {}
    for kid, ck, dc in negs:
        raw = ck.split("|")
        fused = apply_fuse(raw)
        # build supplementary row indicator in the SAME weighted column space
        row = np.zeros(Z.shape[1])
        present_levels = 0
        for i in range(14):
            v = fused[i]
            if v in MASK:
                continue
            key = (NAMES[i], v)
            if key in colidx:
                row[colidx[key]] = 1.0 / first_sv[block_of_col[colidx[key]]]  # apply same MFA weight
                present_levels += 1
        rt = row.sum()
        if rt <= 0:
            continue
        rowp = row / rt
        # supplementary principal coord: sum_j (rowp_j / sqrt(c_mass_j)) * ... use transition:
        # F_sup(d) = sum_j rowp_j * colstd_j(d)   (standard CA supplementary row formula, weighted profile)
        coord = np.zeros(nret)
        for j in range(len(row)):
            if rowp[j] != 0 and c_mass[j] > 0:
                coord += rowp[j] * col_std[j]
        out[kid] = coord
        death[kid] = dc
    return out, death


def gate_A(st):
    rp("")
    rp("---")
    rp("")
    rp("## Stage 3 — the four gates")
    rp("")
    rp("### Gate A — group recovery")
    from sklearn.cluster import KMeans
    kit_ids = st["kit_ids"]
    kit_group = st["kit_group"]
    mca_coords = st["mca"]["coords"]
    idx = {kid: i for i, kid in enumerate(kit_ids)}

    # GATE STATISTIC: derived clustering on the retained MCA BASIS (the map itself, per
    # prereg §4 — the candidate basis is 2a; Leiden/LCA are witnesses). k-means at k=6
    # (the number of Gate-A groups). ARI computed on the labelled subset only.
    k_groups = len(GATEA_EXPECTED)
    km_all = KMeans(n_clusters=k_groups, random_state=SEED, n_init=25).fit_predict(mca_coords)
    derived = {kit_ids[i]: int(km_all[i]) for i in range(len(kit_ids))}
    lab_ids = [k for k in kit_group]
    true_lab = [kit_group[k] for k in lab_ids]
    ari_basis = ari(true_lab, [derived[k] for k in lab_ids])

    # SECONDARY WITNESSES: Leiden + LCA partitions vs labels (reported, not the gate stat)
    witness = {}
    if st.get("leiden") and not st["leiden"].get("degenerate"):
        lm = st["leiden"]["membership"]
        witness["Leiden(consensus)"] = ari(true_lab, [int(lm[idx[k]]) for k in lab_ids])
    elif st.get("leiden") and st["leiden"].get("degenerate"):
        witness["Leiden(DEGENERATE)"] = float("nan")
    if st.get("lca"):
        ll = st["lca"]["labels"]
        witness["LCA(BIC-k=%d)" % st["lca"]["k"]] = ari(true_lab, [int(ll[idx[k]]) for k in lab_ids])

    ari_val = ari_basis   # the gate statistic
    sil = silhouette_per_group(mca_coords, kit_group, kit_ids)
    rp("- **Gate statistic:** derived clustering = k-means(k=%d) on the retained MCA basis "
       "(the candidate map per prereg §4). ARI computed on the labelled subset (n=%d)." % (k_groups, len(lab_ids)))
    rp("- **ARI (MCA-basis k-means vs frozen labels) = %.3f** — threshold ≥ 0.6 → **%s**."
       % (ari_val, "PASS" if ari_val >= 0.6 else "FAIL"))
    if witness:
        rp("- Secondary witness ARIs (reported, non-gating): "
           + " · ".join("%s=%.3f" % (k, v) for k, v in witness.items()) + ".")
    rp("")
    rp("| group | n | silhouette (retained MCA space) | ≥0.2 |")
    rp("|---|---|---|---|")
    large_fail = []
    sub = []
    for g in GATEA_EXPECTED:
        s = sil.get(g, float("nan"))
        ok = s >= 0.2
        rp("| %s | %d | %.3f | %s |" % (g, GATEA_EXPECTED[g], s, "Y" if ok else "n"))
        if not ok:
            if g in GATEA_LARGE:
                large_fail.append(g)
            sub.append(g)
    n_ok = sum(1 for g in GATEA_EXPECTED if sil.get(g, -9) >= 0.2)
    # A3 rule
    sil_pass = (n_ok >= 5) and (len(large_fail) == 0) and all(g in GATEA_SMALL_PERMITTED for g in sub)
    rp("- Silhouette ≥0.2 for **%d of 6** groups. Large-group failures: %s. Sub-threshold groups: %s."
       % (n_ok, large_fail if large_fail else "NONE", sub if sub else "NONE"))
    rp("- **[A3] silhouette rule** (≥5/6 AND all four large clear AND permitted-failure∈{AURA,MINION-PET}): **%s**."
       % ("PASS" if sil_pass else "FAIL"))
    gateA = (ari_val >= 0.6) and sil_pass
    rp("")
    rp("**GATE A: %s** (ARI %.3f; silhouette-rule %s)."
       % ("PASS" if gateA else "FAIL", ari_val, "PASS" if sil_pass else "FAIL"))
    st["gateA"] = {"pass": gateA, "ari": ari_val, "sil": sil, "sil_pass": sil_pass,
                   "derived": derived, "witness": witness}
    return st


def gate_B(st, supp_coords, supp_death):
    rp("")
    rp("### Gate B — negative geography")
    active_coords = st["mca"]["coords"]
    kit_ids = st["kit_ids"]

    # supplementary points are in the same retained space; test set = pooled intrinsic-red
    red_ids = [k for k, dc in supp_death.items() if dc == "intrinsic-red" and k in supp_coords]
    amber_ids = [k for k, dc in supp_death.items() if dc == "extrinsic-tuning" and k in supp_coords]
    rp("- Projected %d negatives (supplementary, zero mass). intrinsic-red pooled k=%d; extrinsic-tuning k=%d."
       % (len(supp_coords), len(red_ids), len(amber_ids)))

    def mean_pairwise(ids):
        pts = np.array([supp_coords[k] for k in ids])
        if len(pts) < 2:
            return float("nan")
        return float(np.mean(pdist(pts, metric="euclidean")))

    def perm_test(test_ids, n_perm, seed):
        """Null = draws of k kits from ACTIVE projected set; stat = mean pairwise dist."""
        k = len(test_ids)
        obs = mean_pairwise(test_ids)
        rng = np.random.default_rng(seed)
        Nact = active_coords.shape[0]
        null = np.zeros(n_perm)
        for t in range(n_perm):
            sel = rng.choice(Nact, size=k, replace=False)
            null[t] = float(np.mean(pdist(active_coords[sel], metric="euclidean")))
        # small mean pairwise distance = tight clustering = "danger zone"; test lower tail
        p_low = (np.sum(null <= obs) + 1) / (n_perm + 1)
        p_high = (np.sum(null >= obs) + 1) / (n_perm + 1)
        return obs, float(np.mean(null)), p_low, p_high

    # POOLED intrinsic-red — the gate
    if len(red_ids) >= 2:
        obs, nullmean, plow, phigh = perm_test(red_ids, N_PERM_GATEB, SEED)
        p = min(plow, phigh) * 1  # report tighter-than-random (lower tail) as the danger signal
        rp("- **POOLED intrinsic-red (k=%d):** mean pairwise dist = %.4f; null mean = %.4f "
           "(%d draws from active). p(tight, lower-tail) = %.4f; p(dispersed, upper-tail) = %.4f."
           % (len(red_ids), obs, nullmean, N_PERM_GATEB, plow, phigh))
        gateB = plow < 0.05
        rp("- Threshold p<0.05 (clustered tighter than random). **GATE B: %s** (p_lower=%.4f)."
           % ("PASS" if gateB else "FAIL", plow))
    else:
        gateB = None
        rp("- **GATE B UNCOMPUTABLE:** intrinsic-red projectable k=%d (<2). Halting this gate per prereg." % len(red_ids))

    # secondary NON-gating: extrinsic-tuning
    if len(amber_ids) >= 2:
        obs2, nm2, pl2, ph2 = perm_test(amber_ids, N_PERM_GATEB, SEED + 1)
        rp("- **[secondary, NON-gating] extrinsic-tuning (k=%d):** mean pairwise = %.4f; null mean = %.4f; "
           "p_lower = %.4f; p_upper = %.4f." % (len(amber_ids), obs2, nm2, pl2, ph2))
    else:
        rp("- [secondary] extrinsic-tuning k=%d (<2) — not evaluated." % len(amber_ids))

    # per-law descriptive
    rp("- Per-law breakdown DESCRIPTIVE ONLY (all underpowered; not gating):")
    bylaw = Counter(dc for dc in supp_death.values())
    for dc, n in sorted(bylaw.items(), key=lambda x: -x[1]):
        rp("  - %s: n=%d projectable" % (dc if dc else "<NULL>", n))
    st["gateB"] = {"pass": gateB, "red_k": len(red_ids)}
    return st


def gate_C(st):
    rp("")
    rp("### Gate C — franchise mixing")
    coords = st["mca"]["coords"]
    kit_ids = st["kit_ids"]
    franch = np.array([st["kit_franchise"][k] for k in kit_ids])

    # PERMANOVA (adonis2-style) on euclidean distances of retained coords
    D = squareform(pdist(coords, metric="euclidean"))
    r2, F, p_permanova = permanova(D, franch, n_perm=999, seed=SEED)
    rp("- PERMANOVA on `franchise_rollup` (retained MCA distances, 999 perms): "
       "**R² = %.4f**, pseudo-F = %.3f, p = %.3f." % (r2, F, p_permanova))
    # PERMDISP companion
    disp_p, disp_F = permdisp(D, franch, n_perm=999, seed=SEED + 3)
    rp("- **[A4] PERMDISP companion:** F = %.3f, p = %.3f." % (disp_F, disp_p))
    r2_pass = r2 <= 0.15
    if disp_p >= 0.05:
        verdict = "PASS" if r2_pass else "FAIL"
        rp("- PERMDISP non-significant (p≥0.05) → R² is pass-interpretable. Threshold R²≤0.15 → **GATE C: %s**."
           % verdict)
        gateC = r2_pass
        gateC_flag = None
    else:
        rp("- **PERMDISP SIGNIFICANT (p<0.05)** → R² NOT self-interpreting. Reporting both numbers; "
           "**GATE C: gandalf rules** (R²=%.4f vs ≤0.15; dispersion heterogeneity present)." % r2)
        gateC = None
        gateC_flag = "PERMDISP-significant"
    rp("")
    rp("**GATE C: %s** (R²=%.4f, threshold ≤0.15; PERMDISP p=%.3f)."
       % ("PASS" if gateC is True else ("FAIL" if gateC is False else "gandalf rules"), r2, disp_p))
    st["gateC"] = {"pass": gateC, "r2": r2, "permdisp_p": disp_p, "flag": gateC_flag}
    return st


def permanova(D, labels, n_perm, seed):
    """adonis2-style one-way PERMANOVA. Returns (R2, pseudoF, p)."""
    N = D.shape[0]
    D2 = D ** 2
    SST = D2[np.triu_indices(N, 1)].sum() / N
    groups = np.unique(labels)

    def ssw(lab):
        s = 0.0
        for g in groups:
            idx = np.where(lab == g)[0]
            ng = len(idx)
            if ng < 2:
                continue
            sub = D2[np.ix_(idx, idx)]
            s += sub[np.triu_indices(ng, 1)].sum() / ng
        return s
    SSW = ssw(labels)
    SSA = SST - SSW
    a = len(groups)
    dfA = a - 1
    dfW = N - a
    F = (SSA / dfA) / (SSW / dfW) if SSW > 0 and dfW > 0 else float("nan")
    R2 = SSA / SST if SST > 0 else float("nan")
    rng = np.random.default_rng(seed)
    perm = labels.copy()
    ge = 1
    for _ in range(n_perm):
        rng.shuffle(perm)
        ssw_p = ssw(perm)
        ssa_p = SST - ssw_p
        F_p = (ssa_p / dfA) / (ssw_p / dfW) if ssw_p > 0 else -np.inf
        if F_p >= F:
            ge += 1
    p = ge / (n_perm + 1)
    return float(R2), float(F), float(p)


def permdisp(D, labels, n_perm, seed):
    """PERMDISP / betadisper: homogeneity of multivariate dispersions.
    Distance-to-centroid via PCoA embedding; ANOVA F on those distances + permutation p."""
    N = D.shape[0]
    D2 = D ** 2
    J = np.eye(N) - np.ones((N, N)) / N
    B = -0.5 * J @ D2 @ J
    w, V = sla.eigh(B)
    order = np.argsort(w)[::-1]
    w = w[order]; V = V[:, order]
    pos = w > 1e-9
    X = V[:, pos] * np.sqrt(w[pos])
    groups = np.unique(labels)
    dist_to_cent = np.zeros(N)
    for g in groups:
        idx = np.where(labels == g)[0]
        c = X[idx].mean(0)
        dist_to_cent[idx] = np.sqrt(((X[idx] - c) ** 2).sum(1))

    def anova_F(vals, lab):
        grand = vals.mean()
        ssb = 0.0; ssw = 0.0
        for g in groups:
            idx = np.where(lab == g)[0]
            gm = vals[idx].mean()
            ssb += len(idx) * (gm - grand) ** 2
            ssw += ((vals[idx] - gm) ** 2).sum()
        a = len(groups)
        dfb = a - 1; dfw = N - a
        return (ssb / dfb) / (ssw / dfw) if ssw > 0 else float("nan")
    F = anova_F(dist_to_cent, labels)
    rng = np.random.default_rng(seed)
    lab = labels.copy()
    ge = 1
    for _ in range(n_perm):
        rng.shuffle(lab)
        if anova_F(dist_to_cent, lab) >= F:
            ge += 1
    return ge / (n_perm + 1), float(F)


def procrustes_congruence(A, B):
    """Tucker congruence via procrustes: align B to A, return 1 - normalized disparity proxy.
    Use scipy.procrustes standardized disparity -> congruence = sqrt(1 - disparity)."""
    n = min(A.shape[0], B.shape[0])
    d = min(A.shape[1], B.shape[1])
    A2 = A[:n, :d]; B2 = B[:n, :d]
    try:
        _, _, disp = scipy_procrustes(A2, B2)
    except Exception:
        return float("nan")
    return math.sqrt(max(0.0, 1.0 - disp))


def gate_D(st):
    rp("")
    rp("### Gate D — stability")
    kit_fused = st["kit_fused"]
    kit_ids = st["kit_ids"]
    N = st["N"]
    coords_full = st["mca"]["coords"]
    nret = st["mca"]["nret"]
    diam = plane_diameter(coords_full)
    rp("- **Plane diameter [A5]** = max pairwise Euclidean distance among %d active points in the "
       "%d-dim retained space = **%.4f**. All displacement %% use this denominator." % (N, nret, diam))

    # (i) bootstrap 1000x @ 90%
    rng = np.random.default_rng(SEED + 11)
    disp_all = [[] for _ in range(N)]
    base = [list(r) for r in kit_fused]
    for t in range(N_BOOT_GATED):
        m = int(round(BOOT_FRAC * N))
        sel = rng.choice(N, size=m, replace=False)
        sub = [base[i] for i in sel]
        Zb, cmb, _, _ = build_indicator(sub, block_weight=True)
        mb = mca_greenacre(Zb, cmb)
        cb = mb["row_pc"][:, :nret]
        ref = coords_full[sel, :nret]
        # procrustes align cb to ref
        try:
            mtx1, mtx2, _ = scipy_procrustes(ref, cb)
            # scipy standardizes; recover displacement in standardized ref units, rescale to diam fraction
            d = np.sqrt(((mtx1 - mtx2) ** 2).sum(1))
            # scale factor: standardized ref norm -> map back approx via ref scale
            ref_scale = np.sqrt(((ref - ref.mean(0)) ** 2).sum())
            d_orig = d * ref_scale
        except Exception:
            continue
        for local_i, gi in enumerate(sel):
            disp_all[gi].append(d_orig[local_i])
    per_kit_med = np.array([np.median(x) if x else np.nan for x in disp_all])
    median_disp = np.nanmedian(per_kit_med)
    pct = 100 * median_disp / diam
    boot_pass = pct <= 10.0
    rp("- **(i) Bootstrap** %d× at %d%% subsample, Procrustes-aligned: median per-kit displacement = "
       "%.4f = **%.2f%% of plane diameter** (threshold ≤10%%) → **%s**."
       % (N_BOOT_GATED, int(BOOT_FRAC * 100), median_disp, pct, "PASS" if boot_pass else "FAIL"))

    # (ii) LOFO franchise
    franch = {k: st["kit_franchise"][k] for k in kit_ids}
    frs = sorted(set(franch.values()))
    lofo_res = []
    for f in frs:
        keep_idx = [i for i in range(N) if franch[kit_ids[i]] != f]
        sub = [base[i] for i in keep_idx]
        Zs, cms, _, _ = build_indicator(sub, block_weight=True)
        ms = mca_greenacre(Zs, cms)
        cs = ms["row_pc"][:, :nret]
        ref = coords_full[keep_idx, :nret]
        cong = procrustes_congruence(ref, cs)
        lofo_res.append((f, cong))
    lofo_pass = all(c >= 0.85 for _, c in lofo_res if not np.isnan(c))
    rp("- **(ii) Leave-one-franchise-out** (Procrustes congruence vs full fit on retained kits):")
    rp("")
    rp("| held-out franchise | congruence | ≥0.85 |")
    rp("|---|---|---|")
    for f, c in lofo_res:
        rp("| %s | %.3f | %s |" % (f, c, "Y" if c >= 0.85 else "n"))

    # (iii) inverse-sqrt-franchise reweight refit
    fr_counts = Counter(franch.values())
    w = np.array([1.0 / math.sqrt(fr_counts[franch[kit_ids[i]]]) for i in range(N)])
    coords_rw = weighted_mca(kit_fused, w, nret)
    cong_rw = procrustes_congruence(coords_full, coords_rw)
    rw_pass = (not np.isnan(cong_rw)) and cong_rw >= 0.85
    rp("- **(iii) inverse-√franchise-size reweighted refit** vs unweighted: Procrustes congruence = "
       "%.3f (threshold ≥0.85) → **%s**." % (cong_rw, "PASS" if rw_pass else "FAIL"))

    gateD = boot_pass and lofo_pass and rw_pass
    rp("")
    rp("**GATE D: %s** (bootstrap %s; LOFO %s; reweight %s)."
       % ("PASS" if gateD else "FAIL",
          "PASS" if boot_pass else "FAIL",
          "PASS" if lofo_pass else "FAIL",
          "PASS" if rw_pass else "FAIL"))
    st["gateD"] = {"pass": gateD, "diameter": diam, "boot_pct": pct,
                   "lofo": lofo_res, "reweight_cong": cong_rw,
                   "per_kit_med": per_kit_med}
    return st


def weighted_mca(kit_fused, w, nret):
    """MCA with row weights w (masses) — for inverse-sqrt-franchise reweight."""
    Z, cm, block_of_col, first_sv = build_indicator(kit_fused, block_weight=True)
    N, Q = Z.shape
    w = w / w.sum()
    # weighted CA: use row masses = w
    col_mass = (Z * w[:, None]).sum(0)
    col_mass[col_mass == 0] = 1e-12
    P = Z / Z.sum()
    r = w.copy()
    c = col_mass / col_mass.sum()
    Dr_inv_sqrt = 1.0 / np.sqrt(r)
    Dc_inv_sqrt = 1.0 / np.sqrt(c)
    # expected under independence with weighted margins
    rowsum = Z.sum(1); rowsum[rowsum == 0] = 1e-12
    Pr = Z / rowsum[:, None]        # row profiles
    S = (np.sqrt(r)[:, None]) * (Pr - c[None, :]) * (Dc_inv_sqrt[None, :])
    U, sv, Vt = sla.svd(S, full_matrices=False)
    row_pc = Dr_inv_sqrt[:, None] * U * sv[None, :]
    return row_pc[:, :nret]


# ============================================================================
# ARTIFACT EMISSION
# ============================================================================
def emit_artifacts(con, st, supp_coords, supp_death):
    kit_ids = st["kit_ids"]
    mca = st["mca"]
    coords = mca["coords"]
    nret = mca["nret"]
    dims = ["dim%d" % (d + 1) for d in range(nret)]

    # active coordinates
    leiden_mem = st["leiden"]["membership"] if st.get("leiden") else [None] * len(kit_ids)
    lca_lab = st["lca"]["labels"] if st.get("lca") else [None] * len(kit_ids)
    rowsA = []
    for i, kid in enumerate(kit_ids):
        row = {"kit_id": kid}
        for d in range(nret):
            row[dims[d]] = coords[i, d]
        row["leiden_cluster"] = leiden_mem[i] if leiden_mem[i] is not None else ""
        row["lca_class"] = int(lca_lab[i]) if lca_lab[i] is not None else ""
        row["franchise_rollup"] = st["kit_franchise"][kid]
        row["gateA_group"] = st["kit_group"].get(kid, "")
        rowsA.append(row)
    pd.DataFrame(rowsA).to_csv(os.path.join(OUT, "atlas-coordinates-active.csv"), index=False)

    # supplementary
    rowsS = []
    for kid, coord in sorted(supp_coords.items()):
        row = {"kit_id": kid, "death_class": supp_death.get(kid, "")}
        for d in range(nret):
            row[dims[d]] = coord[d] if d < len(coord) else float("nan")
        rowsS.append(row)
    pd.DataFrame(rowsS).to_csv(os.path.join(OUT, "atlas-coordinates-supplementary.csv"), index=False)

    # loadings: top |loading| coord=level per retained dim
    col_pc = mca["col_pc"]
    col_meta = mca["col_meta"]
    rowsL = []
    for d in range(nret):
        load = col_pc[:, d]
        order = np.argsort(-np.abs(load))
        for rank, j in enumerate(order[:12]):
            cn, lv = col_meta[j]
            rowsL.append({"dim": d + 1, "rank": rank + 1, "coordinate": cn,
                          "level": lv, "loading": float(load[j]), "abs_loading": float(abs(load[j]))})
    pd.DataFrame(rowsL).to_csv(os.path.join(OUT, "atlas-loadings.csv"), index=False)

    # bootstrap summary
    if st.get("gateD"):
        pkm = st["gateD"]["per_kit_med"]
        diam = st["gateD"]["diameter"]
        rowsB = [{"kit_id": kit_ids[i], "median_displacement": pkm[i],
                  "pct_of_diameter": 100 * pkm[i] / diam if not np.isnan(pkm[i]) else float("nan")}
                 for i in range(len(kit_ids))]
        pd.DataFrame(rowsB).to_csv(os.path.join(OUT, "atlas-bootstrap-summary.csv"), index=False)

    # basis draft if all gates pass. Coerce numpy bools -> python bool for clean identity.
    def _pybool(x):
        return bool(x) if isinstance(x, (bool, np.bool_)) else x
    gates = [_pybool(st.get("gateA", {}).get("pass")), _pybool(st.get("gateB", {}).get("pass")),
             _pybool(st.get("gateC", {}).get("pass")), _pybool(st.get("gateD", {}).get("pass"))]
    all_pass = all(g is True for g in gates)
    if all_pass:
        inertia_pct = [round(100 * mca["greenacre_rate"][d], 3) for d in range(nret)]
        basis = {
            "edition": 1,
            "method": "MCA (Greenacre-corrected inertia, MFA block-weighted, 14 coordinate blocks; "
                      "ordinal tempo+commit in CATPCA twin)",
            "retained_dims": nret,
            "inertia_pct": inertia_pct,
            "loadings_ref": "atlas-loadings.csv",
            "plane_diameter": st["gateD"]["diameter"],
            "frozen": False,
        }
        with open(os.path.join(OUT, "atlas-basis-edition-1-draft.json"), "w") as f:
            json.dump(basis, f, indent=2)
        rp("")
        rp("- **All four gates PASS** → `atlas-basis-edition-1-draft.json` drafted (frozen=false; flips true on Matt ratification).")
    else:
        rp("")
        rp("- Not all gates PASS (A=%s B=%s C=%s D=%s) → basis draft NOT emitted (per decision rule)."
           % tuple(str(g) for g in gates))
    return all_pass


# ============================================================================
# MAIN
# ============================================================================
def main():
    os.makedirs(OUT, exist_ok=True)
    con = sqlite3.connect(DB)
    st = stage0(con)
    st = stage1(st)
    st = stage2(st)
    # gates
    st = gate_A(st)
    supp_coords, supp_death = project_supplementary(con, st)
    st = gate_B(st, supp_coords, supp_death)
    st = gate_C(st)
    st = gate_D(st)

    rp("")
    rp("---")
    rp("")
    rp("## §amendments")
    if AMEND:
        for a in AMEND:
            rp("- " + a)
    else:
        rp("- NONE. All pinned parameters executed as specified.")

    all_pass = emit_artifacts(con, st, supp_coords, supp_death)

    rp("")
    rp("---")
    rp("")
    rp("## Gate summary")
    rp("")
    rp("| gate | verdict | headline |")
    rp("|---|---|---|")
    ga = st["gateA"]; gb = st["gateB"]; gc = st["gateC"]; gd = st["gateD"]
    rp("| A group-recovery | %s | ARI=%.3f |" % (_v(ga["pass"]), ga["ari"]))
    rp("| B negative-geography | %s | intrinsic-red k=%d |" % (_v(gb["pass"]), gb["red_k"]))
    rp("| C franchise-mixing | %s | R²=%.4f (PERMDISP p=%.3f) |" % (_v(gc["pass"]), gc["r2"], gc["permdisp_p"]))
    rp("| D stability | %s | boot=%.2f%% diam |" % (_v(gd["pass"]), gd["boot_pct"]))
    rp("")
    rp("**ALL FOUR PASS: %s**" % ("YES" if all_pass else "NO"))

    con.commit()
    con.close()
    _flush_report()
    print("\n=== gate report written to %s ===" % os.path.join(OUT, "2026-07-14-gate-report.md"))


def _v(x):
    if isinstance(x, (bool, np.bool_)):
        x = bool(x)
    return "PASS" if x is True else ("FAIL" if x is False else "gandalf-rules/uncomputed")


if __name__ == "__main__":
    main()
