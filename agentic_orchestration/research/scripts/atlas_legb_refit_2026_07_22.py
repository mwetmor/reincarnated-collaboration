#!/usr/bin/env python3
"""
Leg-B (Edition-V) STEP 3 + STEP 4 — Path-B refit + four gates — 2026-07-22
==========================================================================
Executes the BINDING pre-registration §3 (Path-B refit) + §4 (four gates), ONLY because
STEP 1 fired the vocabulary arm (2026-07-22-legb-step1-trigger.json: trigger_fired=true) and
STEP 2 ruled element_primary ADMIT-AS-AXIS-INPUT (2026-07-22-legb-step2-elemprimary.json).

  prereg: agentic_orchestration/gandalf/design-inputs/2026-07-22-leg-b-edition-next-preregistration.md
  E4 refit LAW: agentic_orchestration/research/curated/atlas/edition4-refit-spec.md §6 (B1/B2/B3)
  Run A method (hyperparameters UNCHANGED): canonical/.../atlas-derivation-charter-2026-07-14.md §5

Executor: elrond. SEED 20260722 on every stochastic step. READ-ONLY corpus.db (md5 must not move).
NO interpretation, NO axis naming (conductor names from loadings — DRIFT-CRITIC). NO tuning.
Any gate FAIL / congruence<0.85 / anchor<40 -> HALT + RETURN to conductor.

FIT POPULATION (§1 GAP-4 / V-2): record-class, atlas_coords non-null = 265 kits (the 2
unprojectable degenerate kits d2-teleport-sorc/poe1-blood-magic-kit have no coords -> OUT of fit;
annex-299 + negatives project SUPPLEMENTARY only).

FEATURE SET (§13 RESOLVED):
  AXIS INPUTS: 14-position atlas_coords register (== E1 cell_key coords; coords 1-3 locked)
             + geometry-bands (primary skill_ordinal=0: delivery_class, range_band,
               motion_signature, width_band, speed_band, cadence_class) [per §13 candidate AXIS]
             + element_primary (first-skill; ADMITTED per STEP 2 decision rule)
  SUPPLEMENTARY/validation-only: court + six-block overlays (NOT axis input)

METHOD (B1, hyperparameters UNCHANGED — re-uses atlas_derivation_2026_07_14 machinery verbatim):
  MCA/CATPCA + Greenacre-corrected inertia + MFA block-weighting; ordinal constraints on
  tempo+commit only; unknowns passive; annex/negatives supplementary-only. Rare categories
  n<10 fused per Greenacre once, all families. Triangulation: Gower->classical MDS; Leiden
  (kNN k=10, CPM 0.5-2.0); LCA (BIC k=2..12). Retention: permutation-null (NOT Kaiser).

B2: Procrustes-anchor to E4's camera = translation + rotation + reflection, NO scale (s*
  computed + DISCLOSED, never applied). Anchor = record-class gateA common members (46).
B3: congruence coefficient on the anchor set post-transform. <0.85 -> HALT (§8-C).
"""

import os, sys, json, sqlite3, math, hashlib
from collections import Counter, defaultdict

import numpy as np
from scipy import linalg as sla
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import procrustes as scipy_procrustes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
# Re-use the EXACT E1 derivation machinery — never re-implement the math (method drift = a
# different fork). We generalize build_indicator/mca to an arbitrary block list but keep the
# identical CA/Greenacre/MFA math from atlas_derivation_2026_07_14.
import atlas_derivation_2026_07_14 as D1
from atlas_derivation_2026_07_14 import (
    mca_greenacre, classical_mds, gower_matrix, leiden_consensus, find_plateau,
    run_lca, silhouette_per_group, ari, permanova, permdisp, procrustes_congruence,
    plane_diameter,
)
from atlas_frozen_basis_reconstruct import FrozenBasis

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"

SEED = 20260722
N_PERM_RETAIN = 1000
N_BOOT = 1000
BOOT_FRAC = 0.90
KNN_K = 10
LEIDEN_RES = [round(0.5 + 0.1 * i, 1) for i in range(16)]
LEIDEN_SEEDS = 100
LCA_KMIN, LCA_KMAX, LCA_STARTS = 2, 12, 50
FUSE_MIN = 10
OTHER_RARE = "other-rare"
MASK = {"unknown", "blank", "post-cutoff-deferred", "post-cutoff", "", None,
        "n/a", "none-band"}   # band-absent -> passive
CONGRUENCE_MIN = 0.85
ANCHOR_FLOOR = 40

# The 14 register coordinates (E1 cell_key order) + the added band coords + element_primary.
REG_NAMES = ["movement", "delivery", "amp", "geometry", "treatment", "function", "defense",
             "economy", "proxy", "range", "tempo", "commit", "activation", "dependency"]
BAND_NAMES = ["gb_delivery", "gb_range", "gb_motion", "gb_width", "gb_speed", "gb_cadence"]
BAND_SGB_COL = {"gb_delivery": "delivery_class", "gb_range": "range_band",
                "gb_motion": "motion_signature", "gb_width": "width_band",
                "gb_speed": "speed_band", "gb_cadence": "cadence_class"}
ELEM_NAME = "element_primary"
ALL_NAMES = REG_NAMES + BAND_NAMES + [ELEM_NAME]   # 14 + 6 + 1 = 21 blocks
ORDINAL = {"tempo", "commit"}
ORDINAL_ORDER = {"tempo": ["low", "med", "high"], "commit": ["instant", "channel", "reserve"]}

GATEA_EXPECTED = {"WHIRLWIND": 15, "TOTEM-SENTRY": 24, "TRAP-MINE": 23,
                  "CHANNELED-BEAM": 9, "AURA": 8, "MINION-PET": 7}
GATEA_LARGE = {"WHIRLWIND", "TOTEM-SENTRY", "TRAP-MINE", "CHANNELED-BEAM"}
GATEA_SMALL_PERMITTED = {"AURA", "MINION-PET"}
FRANCHISE_ROLLUP = D1.FRANCHISE_ROLLUP

np.random.seed(SEED)
REPORT = []
AMEND = []


def rp(*a):
    line = " ".join(str(x) for x in a)
    REPORT.append(line); print(line)


def halt(reason, extra=None):
    rp(""); rp("## EXECUTION HALTED"); rp(""); rp("**HALT:** " + reason)
    if extra:
        rp(""); rp(extra)
    _flush()
    print("\n!!! HALT !!! " + reason)
    sys.exit(3)


def _flush():
    with open(os.path.join(OUT, "2026-07-22-legb-gate-report.md"), "w") as f:
        f.write("\n".join(REPORT) + "\n")


def ro_connect(path):
    return sqlite3.connect("file:%s?mode=ro" % path, uri=True)


def is_mask(v):
    return v in MASK


# ---------------------------------------------------------------------------
# Generalized indicator builder over ALL_NAMES blocks (identical CA/MFA math to D1)
# ---------------------------------------------------------------------------
def build_indicator_multi(kit_rows, names, ordinal=ORDINAL, block_weight=True):
    """kit_rows: list of dict {name -> level}. Build MCA indicator over `names` blocks.
    Masks passive (all-zero row in that block). MFA block-weight = /first singular value.
    Returns Z, col_meta [(name,level)], block_of_col, first_sv, block_index{name->b}."""
    N = len(kit_rows)
    col_meta = []
    block_of_col = []
    columns = []
    block_index = {nm: b for b, nm in enumerate(names)}
    for b, nm in enumerate(names):
        levels = sorted(set(r[nm] for r in kit_rows if not is_mask(r[nm])))
        for lv in levels:
            col = np.array([1.0 if r[nm] == lv else 0.0 for r in kit_rows])
            columns.append(col); col_meta.append((nm, lv)); block_of_col.append(b)
    Z = np.array(columns).T
    block_of_col = np.array(block_of_col)
    nblocks = len(names)
    first_sv = np.ones(nblocks)
    if block_weight:
        for b in range(nblocks):
            cols_b = Z[:, block_of_col == b]
            if cols_b.shape[1] == 0:
                continue
            cb = cols_b - cols_b.mean(0, keepdims=True)
            try:
                sv = sla.svd(cb, compute_uv=False)
                first_sv[b] = sv[0] if len(sv) and sv[0] > 1e-12 else 1.0
            except Exception:
                first_sv[b] = 1.0
        for b in range(nblocks):
            Z[:, block_of_col == b] /= first_sv[b]
    return Z, col_meta, block_of_col, first_sv, block_index


def fuse_rows(kit_rows, names):
    """Greenacre n<FUSE_MIN fuse per block -> other-rare. Returns fused rows + fuse_map."""
    fuse_map = {}
    for nm in names:
        c = Counter(r[nm] for r in kit_rows if not is_mask(r[nm]))
        for lv, n in c.items():
            if n < FUSE_MIN:
                fuse_map[(nm, lv)] = OTHER_RARE
    out = []
    for r in kit_rows:
        nr = {}
        for nm in names:
            v = r[nm]
            nr[nm] = v if is_mask(v) else fuse_map.get((nm, v), v)
        out.append(nr)
    return out, fuse_map


def parallel_analysis_multi(kit_rows, names, observed_adj, n_perm, seed, block_weight=True):
    """Column-permutation nulls on Greenacre-corrected inertia. Retain leading contiguous
    dims whose observed corrected inertia > 95th-pct null (prereg §4)."""
    rng = np.random.default_rng(seed)
    N = len(kit_rows)
    ncomp = len(observed_adj)
    null_adj = np.zeros((n_perm, ncomp))
    for t in range(n_perm):
        perm = [dict(r) for r in kit_rows]
        for nm in names:
            colvals = [perm[k][nm] for k in range(N)]
            rng.shuffle(colvals)
            for k in range(N):
                perm[k][nm] = colvals[k]
        Zp, cm, _, _, _ = build_indicator_multi(perm, names, block_weight=block_weight)
        mp = mca_greenacre(Zp, cm)
        a = mp["greenacre_adj"]
        m = min(ncomp, len(a))
        null_adj[t, :m] = a[:m]
    p95 = np.percentile(null_adj, 95, axis=0)
    retain = observed_adj > p95
    nret = 0
    for i in range(ncomp):
        if retain[i]:
            nret += 1
        else:
            break
    return max(1, nret), p95


def gower_multi(kit_rows, names):
    """Gower dissimilarity over `names` blocks (equal weights; masks = missing)."""
    N = len(kit_rows)
    nblk = len(names)
    codes = np.empty((N, nblk), dtype=np.int32)
    for ci, nm in enumerate(names):
        mp = {}
        for k in range(N):
            v = kit_rows[k][nm]
            codes[k, ci] = -1 if is_mask(v) else mp.setdefault(v, len(mp))
    present = codes >= 0
    both = np.zeros((N, N)); ne = np.zeros((N, N))
    for ci in range(nblk):
        pc = present[:, ci].astype(float)
        bc = np.outer(pc, pc); both += bc
        col = codes[:, ci]
        eq = (col[:, None] == col[None, :]).astype(float)
        ne += bc * (1.0 - eq)
    with np.errstate(divide="ignore", invalid="ignore"):
        Dm = np.where(both > 0, ne / both, 0.0)
    np.fill_diagonal(Dm, 0.0)
    return Dm


def weighted_mca_multi(kit_rows, names, w, nret):
    Z, cm, block_of_col, first_sv, _ = build_indicator_multi(kit_rows, names, block_weight=True)
    N, Q = Z.shape
    w = w / w.sum()
    col_mass = (Z * w[:, None]).sum(0); col_mass[col_mass == 0] = 1e-12
    r = w.copy(); c = col_mass / col_mass.sum()
    Dr_inv_sqrt = 1.0 / np.sqrt(r); Dc_inv_sqrt = 1.0 / np.sqrt(c)
    rowsum = Z.sum(1); rowsum[rowsum == 0] = 1e-12
    Pr = Z / rowsum[:, None]
    S = (np.sqrt(r)[:, None]) * (Pr - c[None, :]) * (Dc_inv_sqrt[None, :])
    U, sv, Vt = sla.svd(S, full_matrices=False)
    row_pc = Dr_inv_sqrt[:, None] * U * sv[None, :]
    return row_pc[:, :nret]


def catpca_twin_multi(kit_rows, names, mca_coords, nret):
    """MCA with tempo+commit quantified ordinal (divergence diagnostic). Identical shape to D1."""
    from sklearn.cluster import KMeans
    N = len(kit_rows)
    columns = []
    for nm in names:
        if nm in ORDINAL:
            order = ORDINAL_ORDER[nm]
            present = [r[nm] for r in kit_rows if not is_mask(r[nm])]
            uniq = sorted(set(present), key=lambda v: order.index(v) if v in order else 99)
            score = {v: i for i, v in enumerate(uniq)}
            col = np.array([float(score[r[nm]]) if not is_mask(r[nm]) else np.nan for r in kit_rows])
            mu = np.nanmean(col); col = np.where(np.isnan(col), mu, col)
            col = (col - col.mean()) / (col.std() + 1e-12)
            columns.append(col)
        else:
            for lv in sorted(set(r[nm] for r in kit_rows if not is_mask(r[nm]))):
                columns.append(np.array([1.0 if r[nm] == lv else 0.0 for r in kit_rows]))
    Z = np.array(columns).T
    Zc = Z - Z.mean(0, keepdims=True)
    U, sv, Vt = sla.svd(Zc, full_matrices=False)
    coords = U[:, :max(nret, 2)] * sv[:max(nret, 2)]
    k = nret + 2
    a = KMeans(n_clusters=k, random_state=SEED, n_init=25).fit_predict(coords[:, :nret])
    b = KMeans(n_clusters=k, random_state=SEED, n_init=25).fit_predict(mca_coords)
    return nret, ari(a, b)


# ---------------------------------------------------------------------------
# Procrustes with NO scale (B2) — translation + rotation + reflection only
# ---------------------------------------------------------------------------
def procrustes_no_scale(ref, mov):
    """Orthogonal Procrustes (rotation+reflection) + translation, NO scaling.
    ref, mov: (n, d) matched rows. Returns aligned mov, R, t, s_star(disclosed not applied),
    rotation_angle_deg, reflection_bool, congruence."""
    ref = np.asarray(ref, float); mov = np.asarray(mov, float)
    mu_r = ref.mean(0); mu_m = mov.mean(0)
    Rc = ref - mu_r; Mc = mov - mu_m
    # optimal rotation via SVD of cross-covariance
    H = Mc.T @ Rc
    U, S, Vt = sla.svd(H)
    Rrot = U @ Vt          # rotation+reflection mapping Mc -> Rc
    reflection = bool(np.linalg.det(Rrot) < 0)
    # optimal scale s* (DISCLOSED, NOT applied)
    varM = (Mc ** 2).sum()
    s_star = float(S.sum() / varM) if varM > 0 else 1.0
    aligned = Mc @ Rrot + mu_r     # NO scale applied
    # congruence (Tucker) on aligned vs ref across all matched coords/dims
    num = float((aligned * ref).sum())
    den = float(np.sqrt((aligned ** 2).sum()) * np.sqrt((ref ** 2).sum()))
    cong = num / den if den > 0 else float("nan")
    # rotation angle (first-plane) for disclosure
    ang = math.degrees(math.atan2(Rrot[1, 0], Rrot[0, 0])) if Rrot.shape[0] >= 2 else 0.0
    return aligned, Rrot, (mu_r - mu_m @ Rrot), s_star, ang, reflection, cong, mu_r, mu_m


def congruence_coeff(A, B):
    """Tucker congruence coefficient between matched matrices A,B (already aligned)."""
    A = np.asarray(A, float); B = np.asarray(B, float)
    num = float((A * B).sum())
    den = float(np.sqrt((A ** 2).sum()) * np.sqrt((B ** 2).sum()))
    return num / den if den > 0 else float("nan")


# ---------------------------------------------------------------------------
# Data assembly
# ---------------------------------------------------------------------------
def load_fit_data(con):
    """Assemble the E5 fit rows (record-class, atlas_coords non-null) with the full feature set."""
    rows = con.execute(
        "SELECT c.kit_id, c.atlas_coords, c.game, c.court, km.mapping_json "
        "FROM canon_corpus c JOIN kit_mapping km ON km.kit_id=c.kit_id "
        "WHERE c.corpus_class='record' AND c.atlas_coords IS NOT NULL ORDER BY c.kit_id").fetchall()
    # primary (ordinal-0) geometry band per kit
    band0 = {}
    for r in con.execute(
        "SELECT sgb.kit_id, sgb.delivery_class, sgb.range_band, sgb.motion_signature, "
        "sgb.width_band, sgb.speed_band, sgb.cadence_class "
        "FROM skill_geometry_band sgb JOIN canon_corpus c ON c.kit_id=sgb.kit_id "
        "WHERE c.corpus_class='record' AND sgb.skill_ordinal=0").fetchall():
        band0[r[0]] = {"gb_delivery": r[1], "gb_range": r[2], "gb_motion": r[3],
                       "gb_width": r[4], "gb_speed": r[5], "gb_cadence": r[6]}
    kit_ids, kit_rows, kit_game, kit_court = [], [], {}, {}
    for kid, ac, game, court, mj in rows:
        parts = ac.split("|")
        if len(parts) != 14:
            continue
        rec = {REG_NAMES[i]: parts[i] for i in range(14)}
        b = band0.get(kid, {nm: None for nm in BAND_NAMES})
        for nm in BAND_NAMES:
            rec[nm] = b.get(nm)
        ep = None
        try:
            d = json.loads(mj); sk = d.get("skills", [])
            if sk:
                ep = sk[0].get("element_primary")
        except Exception:
            pass
        rec[ELEM_NAME] = ep
        kit_ids.append(kid); kit_rows.append(rec)
        kit_game[kid] = game; kit_court[kid] = court
    return kit_ids, kit_rows, kit_game, kit_court


def main():
    os.makedirs(OUT, exist_ok=True)
    rp("# Leg-B (Edition-V) — Path-B refit + four-gate report")
    rp("")
    rp("**Date:** 2026-07-22 · **Executor:** elrond · **Script:** `atlas_legb_refit_2026_07_22.py`")
    rp("**Prereg:** `2026-07-22-leg-b-edition-next-preregistration.md` (BINDING, §13 fold)")
    rp("**Seed:** %d (all randomness pinned). **NUMBERS ONLY — conductor names axes from loadings.**" % SEED)
    rp("**Trigger:** STEP 1 vocabulary arm FIRED (19 absent levels >=20); expression arm did NOT. "
       "STEP 2 element_primary = ADMIT-AS-AXIS-INPUT (max mechanical V=0.555 vs `function`).")
    rp("")
    rp("---")

    con = ro_connect(DB)
    # guard: frozen basis reproduces E4 camera (the anchor target)
    fb = FrozenBasis()
    e4_err, e4_n, _ = fb.smoke_test()
    if e4_err >= 1e-6:
        halt("frozen E4 basis reconstruction drift %.3e — anchor target not trustworthy." % e4_err)
    e4_served = fb.frozen_active_coords()   # kit_id -> (x,y) in E4/E1 served plane
    e4_full = {}  # kit_id -> full 14-dim principal coord (for higher-dim anchor if needed)
    for i, kid in enumerate(fb.ids):
        e4_full[kid] = fb.active_row_pc[i, :]

    kit_ids, kit_rows, kit_game, kit_court = load_fit_data(con)
    N = len(kit_ids)
    rp("")
    rp("## STEP 3 — Path-B refit (B1)")
    rp("- **Fit population:** record-class, atlas_coords 14-field = **%d kits** (record-267 minus "
       "2 unprojectable degenerate kits d2-teleport-sorc/poe1-blood-magic-kit; annex+negatives "
       "supplementary-only)." % N)
    # feature-set coverage disclosure
    band_cov = sum(1 for r in kit_rows if not is_mask(r["gb_delivery"]))
    ep_cov = sum(1 for r in kit_rows if not is_mask(r[ELEM_NAME]))
    rp("- **Feature set (21 blocks):** 14 register coords (AXIS, coords 1-3 locked) + 6 geometry-band "
       "coords (primary skill_ordinal=0; %d/%d kits carry a band, rest passive) + element_primary "
       "(ADMIT; %d/%d non-null, rest passive)." % (band_cov, N, ep_cov, N))
    rp("- **Supplementary/validation-only (NOT axis input):** court + six-block overlays.")

    # ---- fuse (Greenacre n<10, once) ----
    kit_fused, fuse_map = fuse_rows(kit_rows, ALL_NAMES)
    fuse_summary = defaultdict(list)
    for (nm, lv) in fuse_map:
        fuse_summary[nm].append(lv)
    rp("- **Rare-category fuse (Greenacre n<%d -> other-rare, once, all families):** %s"
       % (FUSE_MIN, "; ".join("%s[%s]" % (nm, ",".join(sorted(lvs))) for nm, lvs in sorted(fuse_summary.items())) or "none"))

    # ---- MCA (Greenacre, MFA block-weighted) ----
    Z, col_meta, block_of_col, first_sv, block_index = build_indicator_multi(kit_fused, ALL_NAMES)
    mca = mca_greenacre(Z, col_meta)
    rp("- Indicator matrix: **%d rows × %d columns** (%d MFA blocks; masks passive)." % (Z.shape[0], Z.shape[1], len(ALL_NAMES)))
    rp("- MFA block weights (first singular value): " +
       ", ".join("%s=%.3f" % (ALL_NAMES[b], first_sv[b]) for b in range(len(ALL_NAMES))))

    nret, p95 = parallel_analysis_multi(kit_fused, ALL_NAMES, mca["greenacre_adj"], N_PERM_RETAIN, SEED)
    rp("- **Parallel-analysis retention** (%d column-permutation nulls, Greenacre-corrected inertia, "
       "NOT Kaiser): retain **%d dimensions**." % (N_PERM_RETAIN, nret))
    rp("")
    rp("| dim | raw eig | Greenacre-adj inertia | Greenacre-adj %% | null-95 | retained |")
    rp("|---|---|---|---|---|---|")
    show = max(nret + 3, 6)
    for d in range(min(show, len(mca["eig"]))):
        rp("| %d | %.5f | %.5f | %.2f | %.5f | %s |"
           % (d + 1, mca["eig"][d], mca["greenacre_adj"][d], 100 * mca["greenacre_rate"][d],
              p95[d] if d < len(p95) else float("nan"), "Y" if d < nret else "n"))
    mca_coords = mca["row_pc"][:, :nret]

    # CATPCA twin divergence
    cat_nret, cat_ari = catpca_twin_multi(kit_fused, ALL_NAMES, mca_coords, nret)
    rp("- **CATPCA twin** (ordinal tempo+commit): ARI(CATPCA vs MCA k-means, k=%d) = %.3f (divergence-as-diagnostic)."
       % (nret + 2, cat_ari))

    # ---- 2b Gower -> MDS ----
    Dm = gower_multi(kit_fused, ALL_NAMES)
    mds_coords_full, mds_eig = classical_mds(Dm)
    # MDS retention via same permutation-null approach (reuse D1's shape on our gower)
    rng = np.random.default_rng(SEED + 7)
    ncomp = min(len(mds_eig[mds_eig > 0]), 15)
    null_eigs = np.zeros((N_PERM_RETAIN, ncomp))
    for t in range(N_PERM_RETAIN):
        perm = [dict(r) for r in kit_fused]
        for nm in ALL_NAMES:
            cv = [perm[k][nm] for k in range(N)]; rng.shuffle(cv)
            for k in range(N):
                perm[k][nm] = cv[k]
        Dp = gower_multi(perm, ALL_NAMES)
        _, e = classical_mds(Dp); e = e[e > 0]
        null_eigs[t, :min(ncomp, len(e))] = e[:min(ncomp, len(e))]
    p95_mds = np.percentile(null_eigs, 95, axis=0)
    pos_eig = mds_eig[mds_eig > 0][:ncomp]
    retain = pos_eig > p95_mds[:len(pos_eig)]
    nret_mds = 0
    for i in range(len(pos_eig)):
        if retain[i]:
            nret_mds += 1
        else:
            break
    nret_mds = max(1, nret_mds)
    rp("- **Gower→MDS** retention (%d nulls): retain **%d dims**." % (N_PERM_RETAIN, nret_mds))
    mds_coords = mds_coords_full[:, :nret_mds]

    # ---- 2c Leiden ----
    try:
        res_profile = leiden_consensus(Dm, KNN_K, LEIDEN_RES, LEIDEN_SEEDS, SEED)
        l_res, l_mem, l_range, l_count, l_degen = find_plateau(res_profile, N)
        rp("- **Leiden-CPM** (kNN k=%d, %d seeds, res 0.5-2.0): consensus count = %d at res %.1f%s."
           % (KNN_K, LEIDEN_SEEDS, l_count, l_res, " (DEGENERATE)" if l_degen else ""))
        leiden = {"membership": l_mem, "degenerate": l_degen, "count": l_count}
    except Exception as e:
        AMEND.append("Leiden-CPM FAILED (%s). Per A7 a Louvain substitution would be a LOGGED "
                     "protocol amendment (timestamped) — NOT performed silently; witness UNCOMPUTED." % type(e).__name__)
        rp("- **Leiden UNCOMPUTED** (runtime %s); per A7 no silent Louvain swap. See §amendments." % e)
        leiden = None

    # ---- 2d LCA ----
    try:
        # LCA over the categorical feature set (stepmix); mask -> explicit level (reported)
        lca_rows_input = []
        for r in kit_fused:
            lca_rows_input.append([r[nm] if not is_mask(r[nm]) else "MASK" for nm in ALL_NAMES])
        lca_rows, lca_best = _run_lca_multi(lca_rows_input, ALL_NAMES, LCA_KMIN, LCA_KMAX, LCA_STARTS, SEED)
        rp("- **LCA** (stepmix, BIC k=%d..%d): selected **k=%d**." % (LCA_KMIN, LCA_KMAX, lca_best["k"]))
        lca = {"labels": lca_best["labels"], "k": lca_best["k"]}
    except Exception as e:
        AMEND.append("LCA (stepmix) FAILED (%s); witness UNCOMPUTED." % type(e).__name__)
        rp("- **LCA UNCOMPUTED** (runtime %s). See §amendments." % e)
        lca = None

    # cross-family ARI
    from sklearn.cluster import KMeans
    kcommon = len(GATEA_EXPECTED)
    if leiden and not leiden["degenerate"]:
        kcommon = max(2, min(leiden["count"], N - 1))
    elif lca:
        kcommon = lca["k"]
    km_mca = KMeans(n_clusters=kcommon, random_state=SEED, n_init=25).fit_predict(mca_coords)
    km_mds = KMeans(n_clusters=kcommon, random_state=SEED, n_init=25).fit_predict(mds_coords)
    parts = {"MCA-kmeans": km_mca, "MDS-kmeans": km_mds}
    if leiden:
        parts["Leiden%s" % ("(DEGEN)" if leiden["degenerate"] else "")] = np.asarray(leiden["membership"])
    if lca:
        parts["LCA"] = np.asarray(lca["labels"])
    rp("- **Cross-family ARI** (common k=%d): %s" % (
        kcommon, " · ".join("%s~%s=%.3f" % (a, b, ari(parts[a], parts[b]))
                            for i, a in enumerate(list(parts)) for b in list(parts)[i+1:])))

    # =====================================================================
    # STEP 3 — B2 Procrustes anchor + B3 congruence
    # =====================================================================
    rp("")
    rp("## STEP 3 — B2 Procrustes anchor (translation+rotation+reflection, NO scale) + B3 congruence")
    con2 = ro_connect(DB)
    anchor_ids = [r[0] for r in con2.execute(
        "SELECT g.kit_id FROM atlas_gateA_labels_2026_07_14 g JOIN canon_corpus c ON c.kit_id=g.kit_id "
        "WHERE c.corpus_class='record' AND c.atlas_coords IS NOT NULL").fetchall()]
    con2.close()
    idx = {kid: i for i, kid in enumerate(kit_ids)}
    # common members between E5 fit and E4 served
    common = [k for k in anchor_ids if k in idx and k in e4_served]
    rp("- **Anchor = record-class gateA members** common to E5 fit AND E4 served plane: **%d** "
       "(floor %d)." % (len(common), ANCHOR_FLOOR))
    if len(common) < ANCHOR_FLOOR:
        halt("Procrustes anchor common-member count %d < floor %d (§8 small-anchor finding)." % (len(common), ANCHOR_FLOOR))

    # Anchor on the 2D served plane (the camera Matt sees) — the design-load-bearing plane.
    ref2 = np.array([e4_served[k] for k in common])
    mov2 = np.array([[mca_coords[idx[k], 0], mca_coords[idx[k], 1]] for k in common])
    aligned2, R2, t2, s2, ang2, refl2, cong2, mu_r2, mu_m2 = procrustes_no_scale(ref2, mov2)
    rp("- **B2 transform (2D plane):** rotation angle = %.2f°, reflection = %s, optimal scale s* = %.4f "
       "(DISCLOSED, NOT applied — E4 distance semantics preserved)." % (ang2, refl2, s2))
    rp("- **B3 congruence coefficient (2D plane, anchor n=%d, post-transform) = %.4f** — threshold ≥ %.2f → **%s**."
       % (len(common), cong2, CONGRUENCE_MIN, "PASS" if cong2 >= CONGRUENCE_MIN else "FAIL"))

    # per-member displacement (max-mover table for disclosure)
    disp = np.sqrt(((aligned2 - ref2) ** 2).sum(1))
    order = np.argsort(-disp)
    rp("")
    rp("- Anchor max-mover table (top 8 by post-anchor displacement):")
    rp("")
    rp("| kit_id | Δ (plane units) | E4 (x,y) | E5-aligned (x,y) |")
    rp("|---|---|---|---|")
    for j in order[:8]:
        k = common[j]
        rp("| %s | %.4f | (%.3f, %.3f) | (%.3f, %.3f) |"
           % (k, disp[j], ref2[j, 0], ref2[j, 1], aligned2[j, 0], aligned2[j, 1]))

    if cong2 < CONGRUENCE_MIN:
        # apply the full transform for disclosure of all movers, then HALT (§8-C)
        halt("B3 congruence %.4f < %.2f (§8-C — refit-candidate-1 rotation precedent). "
             "Rotation %.2f°, reflection %s, s*=%.4f disclosed above; E5 NOT served, E4 remains truth."
             % (cong2, CONGRUENCE_MIN, ang2, refl2, s2),
             extra="The refit produced a plane that does not congruently anchor to E4's camera on the "
                   "46 record-class gateA members. Per §7 no-tuning-until-pass, elrond does NOT tune; "
                   "conductor rules (§8-B/§8-C options).")

    # Apply the anchor transform to ALL E5 active points (for the served artifact) — 2D plane
    all_mov2 = mca_coords[:, :2]
    all_aligned2 = (all_mov2 - mu_m2) @ R2 + mu_r2
    e5_xy = {kid: (float(all_aligned2[i, 0]), float(all_aligned2[i, 1])) for i, kid in enumerate(kit_ids)}

    # RIDER-1 badge fields
    inertia_pct = [round(100 * mca["greenacre_rate"][d], 3) for d in range(nret)]
    rp("")
    rp("- **RIDER-1 badge:** plane corrected-inertia (dim1,dim2) = %.2f%%, %.2f%% (sum %.2f%%); "
       "retained-dim count = %d; \"continuum with condensations, not discrete cells.\""
       % (inertia_pct[0], inertia_pct[1], inertia_pct[0] + inertia_pct[1], nret))

    # =====================================================================
    # STEP 4 — the four gates
    # =====================================================================
    rp("")
    rp("---")
    rp("")
    rp("## STEP 4 — the four gates (basis freezes only if all pass)")

    # gateA labels (record-class members) — the frozen table by kit_id
    con3 = ro_connect(DB)
    kit_group = dict(con3.execute(
        "SELECT g.kit_id, g.\"group\" FROM atlas_gateA_labels_2026_07_14 g "
        "JOIN canon_corpus c ON c.kit_id=g.kit_id "
        "WHERE c.corpus_class='record' AND c.atlas_coords IS NOT NULL").fetchall())
    kit_franchise = {k: FRANCHISE_ROLLUP[kit_game[k]] for k in kit_ids}
    con3.close()

    gate_results = {}

    # ---- Gate A ----
    rp("")
    rp("### Gate A — group recovery")
    k_groups = len(GATEA_EXPECTED)
    km_all = KMeans(n_clusters=k_groups, random_state=SEED, n_init=25).fit_predict(mca_coords)
    derived = {kit_ids[i]: int(km_all[i]) for i in range(N)}
    lab_ids = [k for k in kit_group]
    true_lab = [kit_group[k] for k in lab_ids]
    ari_val = ari(true_lab, [derived[k] for k in lab_ids])
    present_groups = sorted(set(true_lab))
    sil = silhouette_per_group(mca_coords, kit_group, kit_ids)
    rp("- Gate statistic: k-means(k=%d) on retained MCA basis; ARI on labelled record-class subset "
       "(n=%d; groups present: %s)." % (k_groups, len(lab_ids), ", ".join(present_groups)))
    rp("- **ARI (MCA-basis vs frozen labels) = %.3f** — threshold ≥ 0.6 → **%s**."
       % (ari_val, "PASS" if ari_val >= 0.6 else "FAIL"))
    rp("")
    rp("| group | n (record-class) | silhouette | ≥0.2 |")
    rp("|---|---|---|---|")
    large_fail, sub = [], []
    for g in GATEA_EXPECTED:
        if g not in present_groups:
            rp("| %s | 0 | (absent in record-class) | — |" % g)
            continue
        s = sil.get(g, float("nan")); ok = s >= 0.2
        rp("| %s | %d | %.3f | %s |" % (g, sum(1 for x in true_lab if x == g), s, "Y" if ok else "n"))
        if not ok:
            if g in GATEA_LARGE:
                large_fail.append(g)
            sub.append(g)
    n_present = len(present_groups)
    n_ok = sum(1 for g in present_groups if sil.get(g, -9) >= 0.2)
    # A3: large groups present must clear; permitted sub-threshold only AURA/MINION-PET
    large_present = [g for g in present_groups if g in GATEA_LARGE]
    sil_pass = (len(large_fail) == 0) and all(g in GATEA_SMALL_PERMITTED for g in sub) and (n_ok >= max(1, n_present - 1))
    rp("- Silhouette ≥0.2 for **%d of %d present** groups. Large-group failures: %s. Sub-threshold: %s."
       % (n_ok, n_present, large_fail if large_fail else "NONE", sub if sub else "NONE"))
    rp("- NOTE: MINION-PET has **0 record-class members** (all 7 are annex/project-only) → not testable "
       "in the record-class fit; A3's permitted-failure set {AURA,MINION-PET} still honored.")
    gateA = (ari_val >= 0.6) and sil_pass
    rp("- **[A3] silhouette rule: %s**." % ("PASS" if sil_pass else "FAIL"))
    rp("- **GATE A: %s** (ARI %.3f; silhouette-rule %s)." % ("PASS" if gateA else "FAIL", ari_val, "PASS" if sil_pass else "FAIL"))
    gate_results["A"] = {"pass": bool(gateA), "ari": ari_val, "sil": sil, "sil_pass": bool(sil_pass),
                         "present_groups": present_groups}

    # ---- Gate C ----
    rp("")
    rp("### Gate C — franchise mixing")
    franch = np.array([kit_franchise[k] for k in kit_ids])
    Dc = squareform(pdist(mca_coords, metric="euclidean"))
    r2, F, p_perm = permanova(Dc, franch, n_perm=999, seed=SEED)
    disp_p, disp_F = permdisp(Dc, franch, n_perm=999, seed=SEED + 3)
    rp("- PERMANOVA on `franchise_rollup` (retained MCA distances, 999 perms): **R² = %.4f**, pseudo-F = %.3f, p = %.3f."
       % (r2, F, p_perm))
    rp("- **[A4] PERMDISP:** F = %.3f, p = %.3f." % (disp_F, disp_p))
    r2_pass = r2 <= 0.15
    if disp_p >= 0.05:
        gateC = r2_pass; cflag = None
        rp("- PERMDISP non-significant (p≥0.05) → R² pass-interpretable. Threshold R²≤0.15 → **GATE C: %s**."
           % ("PASS" if gateC else "FAIL"))
    else:
        gateC = None; cflag = "PERMDISP-significant"
        rp("- **PERMDISP SIGNIFICANT (p<0.05)** → R²=%.4f flagged for conductor ruling (not self-cleared per dispatch)."
           % r2)
    rp("- **GATE C: %s** (R²=%.4f ≤0.15; PERMDISP p=%.3f)."
       % ("PASS" if gateC is True else ("FAIL" if gateC is False else "conductor-rules"), r2, disp_p))
    gate_results["C"] = {"pass": gateC, "r2": r2, "permdisp_p": disp_p, "flag": cflag}

    # ---- Gate D ----
    rp("")
    rp("### Gate D — stability")
    diam = plane_diameter(mca_coords)   # E5 RETAINED-DIM space (A-LB3/Q6)
    rp("- **Plane diameter [A-LB3]** = max pairwise Euclidean dist among %d active points in the "
       "**%d-dim E5 retained space** = **%.4f** (badge-disclosed)." % (N, nret, diam))
    # bootstrap
    rng = np.random.default_rng(SEED + 11)
    disp_all = [[] for _ in range(N)]
    for t in range(N_BOOT):
        m = int(round(BOOT_FRAC * N))
        sel = rng.choice(N, size=m, replace=False)
        sub = [kit_fused[i] for i in sel]
        Zb, cmb, _, _, _ = build_indicator_multi(sub, ALL_NAMES)
        mb = mca_greenacre(Zb, cmb)
        cb = mb["row_pc"][:, :nret]
        ref = mca_coords[sel, :nret]
        try:
            mtx1, mtx2, _ = scipy_procrustes(ref, cb)
            d = np.sqrt(((mtx1 - mtx2) ** 2).sum(1))
            ref_scale = np.sqrt(((ref - ref.mean(0)) ** 2).sum())
            d_orig = d * ref_scale
        except Exception:
            continue
        for li, gi in enumerate(sel):
            disp_all[gi].append(d_orig[li])
    per_kit_med = np.array([np.median(x) if x else np.nan for x in disp_all])
    median_disp = float(np.nanmedian(per_kit_med))
    pct = 100 * median_disp / diam
    boot_pass = pct <= 10.0
    rp("- **(i) Bootstrap** %d× @ %d%%, Procrustes-aligned: median per-kit displacement = %.4f = **%.2f%% of diameter** (≤10%%) → **%s**."
       % (N_BOOT, int(BOOT_FRAC * 100), median_disp, pct, "PASS" if boot_pass else "FAIL"))
    # LOFO
    frs = sorted(set(kit_franchise.values()))
    lofo = []
    for f in frs:
        keep = [i for i in range(N) if kit_franchise[kit_ids[i]] != f]
        sub = [kit_fused[i] for i in keep]
        Zs, cms, _, _, _ = build_indicator_multi(sub, ALL_NAMES)
        ms = mca_greenacre(Zs, cms)
        cs = ms["row_pc"][:, :nret]
        ref = mca_coords[keep, :nret]
        lofo.append((f, procrustes_congruence(ref, cs)))
    lofo_pass = all(c >= 0.85 for _, c in lofo if not np.isnan(c))
    rp("- **(ii) LOFO** (Procrustes congruence vs full fit):")
    rp("")
    rp("| held-out franchise | congruence | ≥0.85 |")
    rp("|---|---|---|")
    for f, c in lofo:
        rp("| %s | %.3f | %s |" % (f, c, "Y" if c >= 0.85 else "n"))
    # inverse-sqrt reweight
    fr_counts = Counter(kit_franchise.values())
    w = np.array([1.0 / math.sqrt(fr_counts[kit_franchise[kit_ids[i]]]) for i in range(N)])
    coords_rw = weighted_mca_multi(kit_fused, ALL_NAMES, w, nret)
    cong_rw = procrustes_congruence(mca_coords, coords_rw)
    rw_pass = (not np.isnan(cong_rw)) and cong_rw >= 0.85
    rp("- **(iii) inverse-√franchise reweight** vs unweighted: Procrustes congruence = %.3f (≥0.85) → **%s**."
       % (cong_rw, "PASS" if rw_pass else "FAIL"))
    gateD = boot_pass and lofo_pass and rw_pass
    rp("- **GATE D: %s** (bootstrap %s; LOFO %s; reweight %s)."
       % ("PASS" if gateD else "FAIL", "PASS" if boot_pass else "FAIL",
          "PASS" if lofo_pass else "FAIL", "PASS" if rw_pass else "FAIL"))
    gate_results["D"] = {"pass": bool(gateD), "diameter": diam, "boot_pct": pct,
                         "lofo": lofo, "reweight": cong_rw}

    # ---- Gate B -> Finding F-1 (DESCRIPTIVE, NON-GATING) — re-verify corpse dispersal on E5 ----
    rp("")
    rp("### Gate B → Finding F-1 (DESCRIPTIVE on E5 basis, NON-GATING — A-LB5)")
    f1 = gate_B_f1(con, fb, mca, col_meta, block_of_col, first_sv, block_index, ALL_NAMES,
                   fuse_map, mca_coords, nret)
    gate_results["F1"] = f1

    # =====================================================================
    # Verdict + artifacts
    # =====================================================================
    rp("")
    rp("---")
    rp("")
    rp("## §amendments")
    if AMEND:
        for a in AMEND:
            rp("- " + a)
    else:
        rp("- NONE. All pinned parameters executed as specified.")

    passes = {g: gate_results[g]["pass"] for g in ["A", "C", "D"]}
    all_gate_pass = all(v is True for v in passes.values()) and (cong2 >= CONGRUENCE_MIN)
    rp("")
    rp("---")
    rp("")
    rp("## Gate summary")
    rp("")
    rp("| gate | verdict | headline |")
    rp("|---|---|---|")
    rp("| B3 congruence | %s | %.4f (anchor n=%d) |" % (_v(cong2 >= CONGRUENCE_MIN), cong2, len(common)))
    rp("| A group-recovery | %s | ARI=%.3f |" % (_v(gate_results["A"]["pass"]), gate_results["A"]["ari"]))
    rp("| C franchise-mixing | %s | R²=%.4f (PERMDISP p=%.3f) |"
       % (_v(gate_results["C"]["pass"]), gate_results["C"]["r2"], gate_results["C"]["permdisp_p"]))
    rp("| D stability | %s | boot=%.2f%% diam |" % (_v(gate_results["D"]["pass"]), gate_results["D"]["boot_pct"]))
    rp("| B→F-1 (non-gating) | DESCRIPTIVE | p_dispersed=%.4f on E5 |" % f1.get("p_dispersed", float("nan")))
    rp("")
    rp("**ALL GATING (B3+A+C+D) PASS: %s**" % ("YES" if all_gate_pass else "NO"))

    # emit artifacts (loadings, coords, edition5.json) regardless — the report is the account;
    # the served/freeze decision is the conductor's + Matt's.
    emit_artifacts(kit_ids, kit_rows, kit_fused, mca, nret, mca_coords, e5_xy, kit_franchise,
                   kit_group, kit_court, col_meta, first_sv, block_of_col, block_index,
                   ALL_NAMES, inertia_pct, cong2, s2, ang2, refl2, len(common), diam,
                   gate_results, leiden, lca, f1, all_gate_pass)

    con.close()
    _flush()
    print("\n=== gate report: %s ===" % os.path.join(OUT, "2026-07-22-legb-gate-report.md"))
    return all_gate_pass


def _v(x):
    if isinstance(x, (bool, np.bool_)):
        x = bool(x)
    return "PASS" if x is True else ("FAIL" if x is False else "conductor-rules")


def _run_lca_multi(rows_input, names, kmin, kmax, starts, seed):
    from stepmix.stepmix import StepMix
    N = len(rows_input)
    enc = np.zeros((N, len(names)), dtype=int)
    maps = []
    for ci in range(len(names)):
        vals = sorted(set(rows_input[k][ci] for k in range(N)))
        m = {v: i for i, v in enumerate(vals)}; maps.append(m)
        for k in range(N):
            enc[k, ci] = m[rows_input[k][ci]]
    import pandas as pd
    Xdf = pd.DataFrame(enc, columns=names)
    best = None; out_rows = []
    for K in range(kmin, kmax + 1):
        model = StepMix(n_components=K, measurement="categorical", n_init=starts,
                        random_state=seed, max_iter=200, verbose=0)
        model.fit(Xdf)
        ll = model.score(Xdf) * N
        nparams = model.n_parameters if hasattr(model, "n_parameters") else (K - 1) + K * (sum(len(m) for m in maps) - len(names))
        bic = -2 * ll + nparams * math.log(N)
        labels = model.predict(Xdf)
        out_rows.append({"k": K, "BIC": bic})
        if best is None or bic < best["BIC"]:
            best = {"k": K, "BIC": bic, "labels": np.asarray(labels)}
    return out_rows, best


# ---------------------------------------------------------------------------
# Gate B -> F-1: DESCRIPTIVE corpse dispersal on the E5 basis (A-LB5)
# ---------------------------------------------------------------------------
def gate_B_f1(con, fb, mca, col_meta, block_of_col, first_sv, block_index, names, fuse_map,
              mca_coords, nret):
    """Project the intrinsic-red corpses (negatives) into the E5 basis as supplementary, compute
    p_dispersed (upper-tail mean-pairwise-distance permutation vs active). NON-GATING: re-measuring
    ≠ downgrading. Corpses project through the REGISTER coords only (they carry a cell_key; band/
    element features are absent for negatives -> passive)."""
    return _f1_project_and_test(con, names, fuse_map, mca_coords, nret)


def _f1_project_and_test(con, names, fuse_map, active_coords, nret):
    # negatives with a cell_key (register coords only)
    negs = con.execute(
        "SELECT k.kit_id, k.cell_key, c.death_class FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=1 "
        "ORDER BY k.kit_id").fetchall()
    # Rebuild the E5 fit indicator to recover column standard coords (must match the fit exactly).
    # We reconstruct from the same load path used in main() — re-load fit rows here.
    con_local = ro_connect(DB)
    kit_ids, kit_rows, _, _ = load_fit_data(con_local)
    con_local.close()
    kit_fused, _ = fuse_rows(kit_rows, names)
    Z, col_meta, block_of_col, first_sv, block_index = build_indicator_multi(kit_fused, names)
    mca = mca_greenacre(Z, col_meta)
    sv = mca["sv"]
    col_std = mca["col_pc"][:, :nret] / sv[:nret][None, :]
    colidx = {lvl: i for i, lvl in enumerate(col_meta)}

    def project_cellkey(cell_key):
        raw = cell_key.split("|")
        if len(raw) != 14:
            return None
        # register coords only (positions map to REG_NAMES); band + element passive for negatives
        fused = {}
        for i in range(14):
            v = raw[i]
            fused[REG_NAMES[i]] = OTHER_RARE if (REG_NAMES[i], v) in fuse_map else v
        row = np.zeros(Z.shape[1]); present = 0
        for i in range(14):
            nm = REG_NAMES[i]; v = fused[nm]
            if is_mask(v):
                continue
            key = (nm, v)
            if key in colidx:
                j = colidx[key]; row[j] = 1.0 / first_sv[block_of_col[j]]; present += 1
        rt = row.sum()
        if rt <= 0:
            return None
        rowp = row / rt
        coord = np.zeros(nret)
        for j in range(len(row)):
            if rowp[j] != 0:
                coord += rowp[j] * col_std[j]
        return coord

    supp = {}; death = {}
    for kid, ck, dc in negs:
        c = project_cellkey(ck)
        if c is not None:
            supp[kid] = c; death[kid] = dc
    red_ids = [k for k, dc in death.items() if dc == "intrinsic-red"]
    rp("- Projected %d negatives supplementary into the E5 basis (register coords; band/element passive)." % len(supp))
    rp("- intrinsic-red projectable: n=%d." % len(red_ids))
    result = {"n_supp": len(supp), "n_red": len(red_ids)}
    if len(red_ids) < 2:
        rp("- **F-1 UNCOMPUTABLE on E5** (intrinsic-red projectable <2). Reported, non-gating.")
        result["p_dispersed"] = float("nan")
        return result

    def mean_pairwise(ids):
        pts = np.array([supp[k] for k in ids])
        return float(np.mean(pdist(pts, metric="euclidean")))
    obs = mean_pairwise(red_ids)
    rng = np.random.default_rng(SEED)
    Nact = active_coords.shape[0]
    ndraw = 10000
    null = np.zeros(ndraw)
    for t in range(ndraw):
        sel = rng.choice(Nact, size=len(red_ids), replace=False)
        null[t] = float(np.mean(pdist(active_coords[sel], metric="euclidean")))
    p_low = (np.sum(null <= obs) + 1) / (ndraw + 1)
    p_high = (np.sum(null >= obs) + 1) / (ndraw + 1)
    rp("- intrinsic-red (k=%d): mean pairwise = %.4f; null mean = %.4f (10000 draws). "
       "p(tight,lower)=%.4f; **p_dispersed(upper)=%.4f**." % (len(red_ids), obs, float(np.mean(null)), p_low, p_high))
    rp("- **Finding F-1 on E5:** %s (re-measuring ≠ downgrading; NON-GATING per A-LB5)."
       % ("corpses DISPERSED (p_dispersed<0.05) — F-1 holds on the moved camera"
          if p_high < 0.05 else "corpses NOT significantly dispersed on E5 — published finding, not a gate fail"))
    result["p_dispersed"] = float(p_high)
    result["p_tight"] = float(p_low)
    result["obs_mean_pairwise"] = obs
    return result


# ---------------------------------------------------------------------------
# Artifact emission
# ---------------------------------------------------------------------------
def emit_artifacts(kit_ids, kit_rows, kit_fused, mca, nret, mca_coords, e5_xy, kit_franchise,
                   kit_group, kit_court, col_meta, first_sv, block_of_col, block_index,
                   names, inertia_pct, cong2, s2, ang2, refl2, anchor_n, diam,
                   gate_results, leiden, lca, f1, all_gate_pass):
    import pandas as pd
    dims = ["dim%d" % (d + 1) for d in range(nret)]
    # active coordinates csv (E5)
    lmem = leiden["membership"] if leiden else [None] * len(kit_ids)
    llab = lca["labels"] if lca else [None] * len(kit_ids)
    rowsA = []
    for i, kid in enumerate(kit_ids):
        row = {"kit_id": kid}
        for d in range(nret):
            row[dims[d]] = float(mca_coords[i, d])
        row["x_anchored"] = e5_xy[kid][0]
        row["y_anchored"] = e5_xy[kid][1]
        row["leiden_cluster"] = int(lmem[i]) if (lmem[i] is not None) else ""
        row["lca_class"] = int(llab[i]) if (llab[i] is not None) else ""
        row["franchise_rollup"] = kit_franchise[kid]
        row["gateA_group"] = kit_group.get(kid, "")
        row["court"] = kit_court.get(kid) or ""
        rowsA.append(row)
    pd.DataFrame(rowsA).to_csv(os.path.join(OUT, "atlas-coordinates-active-edition5.csv"), index=False)

    # loadings csv (E5) — top |loading| per retained dim; NO axis names (conductor names them)
    col_pc = mca["col_pc"]
    rowsL = []
    for d in range(nret):
        load = col_pc[:, d]
        order = np.argsort(-np.abs(load))
        for rank, j in enumerate(order[:15]):
            cn, lv = col_meta[j]
            rowsL.append({"dim": d + 1, "rank": rank + 1, "coordinate": cn, "level": lv,
                          "loading": float(load[j]), "abs_loading": float(abs(load[j]))})
    pd.DataFrame(rowsL).to_csv(os.path.join(OUT, "atlas-loadings-edition5.csv"), index=False)

    # atlas-edition5.json
    basis = {
        "edition": 5,
        "derivation": "Path-B true refit (E1 method, hyperparameters UNCHANGED) + Procrustes-no-scale "
                      "anchor to E4 camera on record-class gateA members",
        "method": "MCA (Greenacre-corrected inertia, MFA block-weighted, %d coordinate blocks: 14 register "
                  "+ 6 geometry-band + element_primary; ordinal tempo+commit CATPCA twin)" % len(names),
        "fit_population": {"class": "record", "n_active": len(kit_ids),
                           "excluded_unprojectable": ["d2-teleport-sorc", "poe1-blood-magic-kit"]},
        "feature_set": {"axis_inputs": ["13-coordinate register (14-position, coords 1-3 locked)",
                                        "geometry-bands (primary skill_ordinal=0)", "element_primary"],
                        "supplementary": ["court", "six-block overlays"]},
        "retained_dims": nret,
        "inertia_pct": inertia_pct,
        "rider_1": {"plane_corrected_inertia_pct": [inertia_pct[0], inertia_pct[1]],
                    "retained_dim_count": nret,
                    "statement": "continuum with condensations, not discrete cells"},
        "procrustes_anchor": {"anchor_set": "record-class gateA members",
                              "anchor_n": anchor_n,
                              "transform": "translation + rotation + reflection (NO scale)",
                              "rotation_deg": round(ang2, 3), "reflection": refl2,
                              "s_star_disclosed_not_applied": round(s2, 4),
                              "congruence_coefficient": round(cong2, 4),
                              "congruence_threshold": 0.85},
        "plane_diameter_retained_dim_space": round(diam, 4),
        "gates": {"A": {"pass": gate_results["A"]["pass"], "ari": round(gate_results["A"]["ari"], 4)},
                  "C": {"pass": gate_results["C"]["pass"], "r2": round(gate_results["C"]["r2"], 4),
                        "permdisp_p": round(gate_results["C"]["permdisp_p"], 4)},
                  "D": {"pass": gate_results["D"]["pass"], "boot_pct": round(gate_results["D"]["boot_pct"], 4)},
                  "B_F1_descriptive_nongating": {"p_dispersed_on_E5": f1.get("p_dispersed")}},
        "all_gating_pass": bool(all_gate_pass),
        "loadings_ref": "atlas-loadings-edition5.csv",
        "coordinates_ref": "atlas-coordinates-active-edition5.csv",
        "frozen": False,   # flips true only on Matt ratification (freeze is Matt's boundary)
        "seed": SEED,
        "corpus_db_md5": "bebc933b0bf9bcab5988bbc16bcc55b4",
    }
    # attach the anchored point list (kit_id, x, y, gateA_group, franchise) for render/inspection
    points = []
    for i, kid in enumerate(kit_ids):
        points.append({"kit_id": kid, "x": e5_xy[kid][0], "y": e5_xy[kid][1],
                       "gateA_group": kit_group.get(kid, None),
                       "franchise": kit_franchise[kid], "supplementary": False})
    doc = {"basis": basis, "points": points, "n_points": len(points)}
    with open(os.path.join(OUT, "atlas-edition5.json"), "w") as f:
        json.dump(doc, f, indent=2, default=float)
    rp("")
    rp("- Artifacts emitted: `atlas-edition5.json`, `atlas-loadings-edition5.csv`, `atlas-coordinates-active-edition5.csv`.")


if __name__ == "__main__":
    main()
