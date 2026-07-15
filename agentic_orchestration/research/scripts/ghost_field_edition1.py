#!/usr/bin/env python3
"""
ghost_field_edition1.py — build the atlas.json ghost_field block (charter §4).
=============================================================================
The layer the whole ship chain waits on. Enumerates the feasibility-cuts-register
v1.1 meso lattice (10,080 feasible + 1,260 sealed cells), projects every feasible
cell into the FROZEN Edition-I basis via the pipeline's CA supplementary transition
formulas (zero mass; axes cannot move — decoupling law), lights cells from the live
corpus, and stamps depth badges.

Author: elrond (data steward). TOOL script (curation/enumeration), not engine code.
Imported by build_atlas_json_edition1.py (star-lord's emitter) — minimal extension,
logged in research/curated/MIGRATION.md.

FROZEN-BASIS DISCIPLINE (decoupling law — verified, non-negotiable):
  The frozen Edition-I MCA fit was computed on the PRE-C3 active cell_keys. My Task-C
  treatment re-key (9 control->damage) would MOVE dim2 if used for the fit (probe:
  max|dim2| ~1.0). So the FIT (axes) reconstructs from the durable snapshot
  atlas-frozen-fit-cellkeys-edition1.csv (pre-C3; verified to reproduce the frozen
  active dim1/dim2 to 0.00e+00). The LIT-MAPPING uses the LIVE corpus.db keys AT
  EMISSION TIME (post-C3 fixes) — honest post-fix lighting. Frozen frame, versioned
  occupancy (Edition law §6). Two different data states, correctly.

PROJECTION (charter §4 step 2; identical machinery to corpse mask handling):
  A meso tuple populates the 6 core-coordinate indicator blocks (movement, delivery,
  treatment, function, proxy, activation, dependency) in the FIT's column vocabulary
  via the register->fit crosswalk. Non-core blocks (amp, geometry, defense, economy,
  range, tempo, commit) are ABSENT (zero rows). Absent core blocks (MELEE/SUMMON
  delivery, hybrid treatment, silence function -> no fit column level) are also absent,
  handled exactly like corpse partial keys. Transition formula:
      F_sup(d) = sum_j rowp_j * col_std_j(d)
  where rowp is the MFA-weighted, row-normalized indicator profile over present levels.

Register-ref: feasibility-cuts-register-v1.1 (elrond, 2026-07-15).
"""

import os, sys, csv, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_derivation_2026_07_14 as pipe

# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
FROZEN_FIT_CSV = os.path.join(ATLAS_DIR, "atlas-frozen-fit-cellkeys-edition1.csv")

NAMES = pipe.NAMES                 # 14-coord order
MASK = pipe.MASK
FUSE_MIN = pipe.FUSE_MIN
OTHER_RARE = pipe.OTHER_RARE
RETAINED_DIMS = 14                 # frozen Edition-I
GHOST_FIELD_VERSION = "1.0"
REGISTER_REF = "feasibility-cuts-register-v1.1"

# cell_key core-slot indices (14-field cell_key: movement|delivery|amp|geometry|
#   treatment|function|defense|economy|proxy|range|tempo|commit|activation|dependency)
CK_IDX = {"movement": 0, "delivery": 1, "treatment": 4, "function": 5,
          "proxy": 8, "activation": 12, "dependency": 13}
CORE = ["movement", "delivery", "treatment", "function", "proxy", "activation", "dependency"]

# ---- register-meso ABSTRACT vocabulary (what the register enumerates) ----
REG = {
    "movement":   ["FREE-MOVE", "WALK", "ROOTED"],
    "delivery":   ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON"],
    "treatment":  ["damage", "control", "hybrid"],
    "function":   ["none", "hard-stop", "stun", "taunt", "fear", "blind",
                   "knockback", "expose", "hex", "silence"],
    "proxy":      ["solo", "light", "heavy"],
    "activation": ["active", "triggered"],
    "dependency": ["one-shot", "build→spend", "apply→detonate"],
}
MOVE_VERB_DELIVERY = None  # RED-3 is geometry-keyed (non-core) — not a meso predicate

# ---- register -> FIT column crosswalk (for the transition formula projection) ----
#   None = no fit core-level exists -> block ABSENT (masked-like; identical to corpse partial key).
REG2FIT = {
    "movement":   {"FREE-MOVE": "full-move", "WALK": "walk", "ROOTED": "rooted"},
    "delivery":   {"PROJECTILE": "projectile", "ORBITAL": "orbit", "NOVA": "self-origin",
                   "ZONE": "at-target", "BEAM": "beam", "MELEE": None, "SUMMON": None},
    "treatment":  {"damage": "damage", "control": "control", "hybrid": None},
    "function":   {"none": "none", "hard-stop": "hard-stop", "stun": "stun", "taunt": "taunt",
                   "fear": "fear", "blind": "blind", "knockback": "knockback",
                   "expose": "expose", "hex": "hex", "silence": None},
    "proxy":      {"solo": "solo", "light": "light", "heavy": "heavy"},
    "activation": {"active": "active", "triggered": "triggered"},
    "dependency": {"one-shot": "one-shot", "build→spend": "build→spend",
                   "apply→detonate": "apply→detonate"},
}

# ---- corpus FIT-key -> register-meso value crosswalk (for lit-mapping) ----
#   applied to the 6 core coords of a LIVE (post-C3) cell_key. 'unmapped' -> exclude from lighting.
def fit2reg_movement(v):
    return {"full-move": "FREE-MOVE", "walk": "WALK", "rooted": "ROOTED"}.get(v)

def fit2reg_delivery(v, geometry, proxy):
    # SUMMON signature = geometry=totem AND a real proxy (proxy != solo). L2 forbids SUMMON x solo,
    # so a totem-geometry kit at proxy=solo is NOT a summon (it is a ground-planted effect, e.g.
    # poe1-earthquake/earthshatter/heavy-strike where 'totem' geometry is a ground-slam key, not a
    # summoned entity). Falling back to the delivery_value mapping keeps such kits in coherent
    # (non-sealed) ground and never lights a SUMMON x solo cell.
    if geometry == "totem" and proxy in ("light", "heavy"):
        return "SUMMON"
    return {"projectile": "PROJECTILE", "orbit": "ORBITAL", "beam": "BEAM", "line": "BEAM",
            "self-origin": "NOVA", "aura-pulse": "NOVA", "at-target": "ZONE"}.get(v)  # other/blank -> None

def fit2reg_direct(v, coord):
    # treatment/function/proxy/activation/dependency map identity when in register vocab
    if v in REG[coord]:
        return v
    return None


# ===========================================================================
# Feasibility predicates at MESO grain (register v1.1: L1' + L2 only bind here;
# L3/L4"/RED-3' are non-core -> invisible at meso). Must match the register generator.
# ===========================================================================
def meso_feasible(cell):
    t, f = cell["treatment"], cell["function"]
    # L1': {control,hybrid} x none incoherent (damage x function coherent)
    if t in ("control", "hybrid") and f == "none":
        return False
    # L2: SUMMON x solo forbidden
    if cell["delivery"] == "SUMMON" and cell["proxy"] == "solo":
        return False
    return True

def meso_cut_id(cell):
    """Which cut seals a NON-feasible meso cell (composition order L1' then L2)."""
    t, f = cell["treatment"], cell["function"]
    if t in ("control", "hybrid") and f == "none":
        return "L1-treatment-function-coherence"
    if cell["delivery"] == "SUMMON" and cell["proxy"] == "solo":
        return "L2-summon-implies-proxy"
    return None


# ===========================================================================
# Depth badge: exact-grain survivor count within a meso cell (delivery-keyed).
# The non-core coords free within a feasible meso cell = amp(3) geometry(21)
# defense(5) economy(7) range(4) tempo(3) commit(3). Cuts touching non-core:
#   L3: MELEE x ranged  |  L4": PROJECTILE x melee  |  RED-3': move-verb-geom x commit!=instant.
# All are delivery-scoped except RED-3' (geometry x commit, delivery-independent, uniform).
# ===========================================================================
def build_depth_by_delivery():
    NONCORE = ["amp", "geometry", "defense", "economy", "range", "tempo", "commit"]
    NC = {
        "amp": ["FLAT", "SPIKY", "VAR"],
        "geometry": ["g%02d" % i for i in range(21)],
        "defense": ["tank", "mitigate", "evade", "absorb", "glass"],
        "economy": ["spend", "cooldown", "generator-spender", "reserve", "self-cost", "finite", "free"],
        "range": ["melee", "mid", "ranged", "dual"],
        "tempo": ["low", "med", "high"],
        "commit": ["instant", "wind-up", "channel"],
    }
    MOVE_VERB = {"g00", "g01"}
    depth = {}
    for dv in REG["delivery"]:
        cnt = 0
        for combo in itertools.product(*[NC[k] for k in NONCORE]):
            c = dict(zip(NONCORE, combo))
            # L3
            if dv == "MELEE" and c["range"] == "ranged":
                continue
            # L4"
            if dv == "PROJECTILE" and c["range"] == "melee":
                continue
            # RED-3'
            if c["geometry"] in MOVE_VERB and c["commit"] != "instant":
                continue
            cnt += 1
        depth[dv] = cnt
    return depth


# ===========================================================================
# FROZEN FIT reconstruction (axes must not move — from the pre-C3 snapshot).
# ===========================================================================
def load_frozen_fit_keys():
    keys = []
    with open(FROZEN_FIT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            keys.append((row["kit_id"], row["cell_key"].split("|")))
    return keys


def build_frozen_fit():
    keys = load_frozen_fit_keys()
    kit_vals = [k[1] for k in keys]
    from collections import Counter
    fuse_map = {}
    for i in range(14):
        c = Counter(v[i] for v in kit_vals if v[i] not in MASK)
        for lv, n in c.items():
            if n < FUSE_MIN:
                fuse_map[(i, lv)] = OTHER_RARE
    def apply_fuse(vals):
        return [vals[i] if vals[i] in MASK else fuse_map.get((i, vals[i]), vals[i]) for i in range(14)]
    kit_fused = [apply_fuse(v) for v in kit_vals]
    Z, cm, block_of_col, first_sv = pipe.build_indicator(kit_fused, block_weight=True)
    mca = pipe.mca_greenacre(Z, cm)
    sv = mca["sv"]
    nret = RETAINED_DIMS
    # column standard coordinates (CA transition): col_pc / sv
    col_std = mca["col_pc"][:, :nret] / sv[:nret][None, :]
    colidx = {lvl: i for i, lvl in enumerate(cm)}
    return dict(col_std=col_std, colidx=colidx, block_of_col=block_of_col,
                first_sv=first_sv, apply_fuse=apply_fuse, fuse_map=fuse_map, nret=nret,
                ncols=Z.shape[1])


def project_meso_cell(cell, fit):
    """Project a register-meso cell into the frozen basis via the CA supplementary
    transition formula. Populates the 6 core blocks (fit vocabulary); absent core
    levels (MELEE/SUMMON/hybrid/silence -> None) contribute nothing (masked-like).
    Non-core blocks are absent by construction. Returns (x, y)."""
    col_std, colidx, block_of_col, first_sv = (fit["col_std"], fit["colidx"],
                                               fit["block_of_col"], fit["first_sv"])
    row = np.zeros(fit["ncols"])
    present = 0
    for coord in CORE:
        fitlvl = REG2FIT[coord][cell[coord]]
        if fitlvl is None:
            continue  # absent core block (masked-like)
        key = (coord, fitlvl)
        j = colidx.get(key)
        if j is None:
            continue
        # apply the SAME MFA block weight the fit used, then fuse if the fit fused this level
        fj = fit["fuse_map"].get((NAMES.index(coord), fitlvl))
        if fj is not None:
            key = (coord, fj)
            j = colidx.get(key)
            if j is None:
                continue
        row[j] = 1.0 / first_sv[block_of_col[j]]
        present += 1
    rt = row.sum()
    if rt <= 0:
        return None, None, 0
    rowp = row / rt
    coord = np.zeros(fit["nret"])
    for j in range(len(row)):
        if rowp[j] != 0:
            coord += rowp[j] * col_std[j]
    return float(coord[0]), float(coord[1]), present


# ===========================================================================
# LIT-MAPPING — map LIVE (post-C3) corpus kits to register-meso cells.
# ===========================================================================
def lit_map(db_conn):
    rows = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL ORDER BY k.kit_id"
    ).fetchall()
    counts = {}                  # register-meso core-tuple -> lit kit count
    unmapped = []                # kits with any unmapped/ambiguous core slot
    unmapped_would_seal = []     # kits that map to a SEALED cell (must NEVER be lit)
    for kid, ck in rows:
        f = ck.split("|")
        geometry = f[3]
        core = {
            "movement": fit2reg_movement(f[CK_IDX["movement"]]),
            "delivery": fit2reg_delivery(f[CK_IDX["delivery"]], geometry, f[CK_IDX["proxy"]]),
            "treatment": fit2reg_direct(f[CK_IDX["treatment"]], "treatment"),
            "function": fit2reg_direct(f[CK_IDX["function"]], "function"),
            "proxy": fit2reg_direct(f[CK_IDX["proxy"]], "proxy"),
            "activation": fit2reg_direct(f[CK_IDX["activation"]], "activation"),
            "dependency": fit2reg_direct(f[CK_IDX["dependency"]], "dependency"),
        }
        if any(v is None for v in core.values()):
            unmapped.append(kid)
            continue
        if not meso_feasible(core):
            # NEVER light a sealed cell — flag for curation
            unmapped_would_seal.append(kid)
            continue
        key = tuple(core[c] for c in CORE)
        counts[key] = counts.get(key, 0) + 1
    return counts, unmapped, unmapped_would_seal


# ===========================================================================
# BUILD the ghost_field block.
# ===========================================================================
def build_ghost_field(db_conn):
    fit = build_frozen_fit()
    depth_by_delivery = build_depth_by_delivery()
    lit_counts, unmapped, unmapped_would_seal = lit_map(db_conn)

    feasible_cells = []
    sealed_cells = []
    depth_sum = 0
    lit_total = 0
    for combo in itertools.product(*[REG[c] for c in CORE]):
        cell = dict(zip(CORE, combo))
        core_tuple = list(combo)
        if meso_feasible(cell):
            x, y, present = project_meso_cell(cell, fit)
            key = tuple(combo)
            kc = lit_counts.get(key, 0)
            depth = depth_by_delivery[cell["delivery"]]
            depth_sum += depth
            lit = kc >= 1
            if lit:
                lit_total += 1
            feasible_cells.append({
                "core": core_tuple,
                "x": round(x, 8),
                "y": round(y, 8),
                "lit": lit,
                "kit_count": kc,
                "depth": depth,
            })
        else:
            sealed_cells.append({
                "core": core_tuple,
                "cut_id": meso_cut_id(cell),
            })

    # deterministic order (byte-stable): sort by core tuple
    feasible_cells.sort(key=lambda c: c["core"])
    sealed_cells.sort(key=lambda c: c["core"])

    ghost = {
        "version": GHOST_FIELD_VERSION,
        "register_ref": REGISTER_REF,
        "grain": "meso (never-demote core: movement, delivery, treatment, function, proxy, activation, dependency)",
        "core_order": CORE,
        "basis_ref": "Edition-I (frozen; ghosts are zero-mass supplementary — axes cannot move, decoupling law)",
        "frozen_fit_input": "atlas-frozen-fit-cellkeys-edition1.csv (pre-C3 snapshot; reproduces frozen active dim1/dim2 to 0.00)",
        "projection": "CA supplementary transition formula F_sup(d)=sum_j rowp_j*col_std_j(d); 6 core blocks in fit vocab; non-core + absent-core blocks masked-like",
        "denominators": {
            "meso_feasible": len(feasible_cells),
            "meso_sealed": len(sealed_cells),
            "meso_raw": len(feasible_cells) + len(sealed_cells),
            "exact_post_red_law": 693146160,
            "exact_post_logical": 740139120,
            "exact_raw_naive": 900169200,
        },
        "depth_by_delivery": depth_by_delivery,
        "depth_sum_check": depth_sum,
        "lit_cells": lit_total,
        "unmapped_pending_curation": len(unmapped),
        "unmapped_pending_curation_kits": sorted(unmapped),
        "unmapped_would_seal_excluded": len(unmapped_would_seal),
        "unmapped_would_seal_kits": sorted(unmapped_would_seal),
        "red3_note": ("RED-3' seals live at GEOMETRY drill-in, not the meso plane "
                      "(geometry is a demotable non-core coord). Meso SEALED cells are L1' + L2 only. "
                      "Depth badges already net out RED-3' within-cell (geometry x commit!=instant) survivors."),
        "feasible_cells": feasible_cells,
        "sealed_cells": sealed_cells,
    }
    return ghost


if __name__ == "__main__":
    import sqlite3
    DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
    con = sqlite3.connect(DB)
    g = build_ghost_field(con)
    con.close()
    print("feasible:", g["denominators"]["meso_feasible"],
          "sealed:", g["denominators"]["meso_sealed"],
          "raw:", g["denominators"]["meso_raw"])
    print("lit cells:", g["lit_cells"], "unmapped:", g["unmapped_pending_curation"],
          "would-seal-excluded:", g["unmapped_would_seal_excluded"])
    print("depth_sum_check:", g["depth_sum_check"], "(expect 693146160)",
          "MATCH" if g["depth_sum_check"] == 693146160 else "MISMATCH")
    print("depth_by_delivery:", g["depth_by_delivery"])
