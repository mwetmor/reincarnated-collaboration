"""
V1.2 Plane View — RULED plane (Matt 2026-07-13)
Renders the ruled 3×7 plane with within-cell amp stratification.

RULINGS APPLIED (vs V1.1 B′):
  1. ROWS change from commitment (SNAP/WIND-UP/CHANNEL, sourced from commit_val)
     to movement-while-casting (FREE-MOVE/WALK/ROOTED, sourced from
     canon_engine_key.mob_policy_while_casting). Values full-move / walk /
     rooted → the three rows; unknown → UNMAPPED strip.
  2. Within each of the 21 cells, kits are stratified into three
     horizontal strata by canon_corpus.amp_val, FIXED ORDER top→bottom:
     FLAT / SPIKY / VAR. Thin separators, small per-stratum counts.
     Empty strata stay visible (design-frontier signal). Because order is
     fixed everywhere, strata form chart-wide scannable bands.
  3. Cone Path 2 applied: geometry `cone` splits by delivery.value from
     canon_probe_facts (family='delivery'). delivery=beam → BEAM (5 kits),
     delivery=projectile → PROJECTILE (6 kits). Derived from DB, not hardcoded.
  4. The one combat kit with amp_val NULL (d2-wl-void-rift) renders as a
     thin visually-distinct "unkeyed" sliver in its cell (walk × ZONE),
     not silently dropped.

CARRY-OVERS from V1.1 (unchanged):
  - Non-cone geometry column mappings.
  - UNMAPPED-9 column assignments (ORBITAL/ZONE/MELEE per addendum §4);
    but ROW derives from actual mob_policy_while_casting, not hardcoded SNAP.
  - Visual conventions (dark bg, ghost dots, mint stars, per-cell counts,
    UNMAPPED strip, legend).
  - Roster kits: no movement column in roster_atlas, so kits with unknown
    movement go to the UNMAPPED strip (honest treatment; roster
    movement/amp backfill is separately queued).

Author: gandalf sub-agent, 2026-07-13
"""

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]  # reincarnated-collaboration/
DB_PATH = REPO_ROOT / "agentic_orchestration" / "research" / "curated" / "corpus.db"
OUT_DIR = SCRIPT_DIR

# ── V1.2 RULED PLANE STRUCTURE ─────────────────────────────────────────────
PLANE_ROWS = ["FREE-MOVE", "WALK", "ROOTED"]
PLANE_COLS = ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON"]

# NEW: movement (not commit) drives rows
ROW_TO_MOV = {"FREE-MOVE": "full-move", "WALK": "walk", "ROOTED": "rooted"}

# NEW: amp strata, FIXED order top→bottom, empty strata stay visible
AMP_STRATA = ["FLAT", "SPIKY", "VAR"]  # top→bottom
STRATUM_TO_AMP = {"FLAT": "flat", "SPIKY": "spiky", "VAR": "var"}

# geometry_value → column (identical to V1.1 for all non-cone geometries)
# cone is handled per-kit via Path 2 (delivery-derived) — see resolve_column()
GEO_TO_COL_BASE = {
    "single_target": "PROJECTILE",
    "multi_projectile": "PROJECTILE",
    "fork": "PROJECTILE",
    "ricochet_bounce": "PROJECTILE",
    "chain": "PROJECTILE",
    "line": "PROJECTILE",
    "ring": "ORBITAL",  # RING merged per addendum §2
    "vortex_pull": "ORBITAL",
    "whirlwind": "ORBITAL",
    "aura": "ORBITAL",
    "circle": "NOVA",  # deterministic NOVA/ZONE rule (addendum §3)
    "ground_targeted_circle": "ZONE",
    # "cone" → resolved per-kit via delivery (Path 2)
    "beam_channel": "BEAM",
    "melee_strike": "MELEE",
    "melee_arc": "MELEE",
    "dash_attack": "MELEE",
    "ground_slam": "MELEE",
    "totem": "SUMMON",
    "self_buff": "SUMMON",
    "teleport": None,  # per-kit reassignment (addendum §4)
    None: None,  # NULL geometry → per-kit reassignment (addendum §4)
}

# UNMAPPED-9 column assignments per addendum §4.
# NOTE (V1.2 change): only COLUMN is fixed here. Rows derive from actual
# mob_policy_while_casting via load_data() — do NOT hardcode row.
UNMAPPED_COL = {
    "d3-inarius-bonestorm": "ORBITAL",
    "d4-ball-lightning": "ORBITAL",
    "d4-bouldercane": "ORBITAL",
    "poe1-poison-bv": "ORBITAL",
    "d2-firewall-sorc": "ZONE",
    "di-bone-wall-necro-pvp": "ZONE",
    "le-frost-wall-rm": "ZONE",  # overrides default SUMMON via walls-demand flag
    "di-monk-sss": "MELEE",
    "tq-phantom-strike-dreamkiller": "MELEE",
    "poe2-temporalis-blink": None,  # UNMAPPED-residual (pure mobility)
}


def load_data():
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row

    # Combat kits with full context including delivery for cone Path-2 split.
    # Movement is the row driver; amp is the stratum driver.
    corpus_kits = con.execute("""
        SELECT c.kit_id, c.folk_name, c.game, c.commit_val, c.amp_val,
               c.era_year, c.stabilization_patch,
               k.geometry_value, k.mob_policy_while_casting AS movement,
               c.negative, c.mint,
               (SELECT json_extract(pf.facts_json, '$.value')
                FROM canon_probe_facts pf
                WHERE pf.kit_id = c.kit_id AND pf.family = 'delivery'
                LIMIT 1) AS delivery_value
        FROM canon_corpus c
        JOIN canon_engine_key k ON c.kit_id = k.kit_id
        WHERE k.row_class = 'combat-kit'
        ORDER BY c.kit_id
    """).fetchall()

    negative_kits = con.execute("""
        SELECT c.kit_id, c.folk_name, c.commit_val, c.negative
        FROM canon_corpus c
        LEFT JOIN canon_engine_key k ON c.kit_id = k.kit_id
        WHERE c.negative = 1
        ORDER BY c.kit_id
    """).fetchall()

    roster_kits = con.execute("""
        SELECT r.kit_id, r.name, r.commit_slot, r.amp,
               rle.bc6_commit, rle.bc6_attr, rle.bc6_amp, rle.folk_name AS lineage_name
        FROM roster_atlas r
        LEFT JOIN roster_lineage_enrichment rle ON r.kit_id = rle.kit_id
        ORDER BY r.kit_id
    """).fetchall()

    con.close()
    return corpus_kits, negative_kits, roster_kits


def resolve_column(kit):
    """Return the B′ column for a corpus kit under V1.2 (cone Path 2 applied).

    Returns column name (str) or None (UNMAPPED).
    Precedence: explicit UNMAPPED-9 override → cone Path 2 → GEO_TO_COL_BASE.
    """
    kid = kit["kit_id"]
    if kid in UNMAPPED_COL:
        return UNMAPPED_COL[kid]

    geo = kit["geometry_value"]
    if geo == "cone":
        dv = kit["delivery_value"]
        if dv == "beam":
            return "BEAM"
        if dv == "projectile":
            return "PROJECTILE"
        # Any other delivery on a cone would be unexpected under Path 2.
        # Surface it rather than silently defaulting.
        return None

    return GEO_TO_COL_BASE.get(geo)


def resolve_row(kit):
    """Return the movement-row for a corpus kit under V1.2.

    Returns row name (str) or None (UNMAPPED strip).
    """
    mov = kit["movement"]
    for row_name, mov_val in ROW_TO_MOV.items():
        if mov == mov_val:
            return row_name
    # 'unknown' or NULL movement → UNMAPPED strip
    return None


def resolve_stratum(kit):
    """Return the amp-stratum for a corpus kit under V1.2.

    Returns stratum name (str) or None (amp NULL → unkeyed sliver in cell).
    """
    amp = kit["amp_val"]
    for stratum, amp_val in STRATUM_TO_AMP.items():
        if amp == amp_val:
            return stratum
    return None  # amp NULL


# ── Public-label derivation (naming law §7.1) ───────────────────────────────
# Contract: atlas-per-dot-json-and-public-label-contract-2026-07-13.md
# public_label = [game_id]-[era_year] (v[patch]) · [mechanical_desc]
# NULL-honest; NEVER renders a trademarked class/skill name (dot_id stays internal).

MOVEMENT_WORD = {"FREE-MOVE": "free-move", "WALK": "walk-cast", "ROOTED": "rooted"}
AMP_WORD = {"FLAT": "flat tempo", "SPIKY": "spiky tempo", "VAR": "variable tempo"}


def mechanical_desc(row, col, stratum):
    """Short human phrase from the cell address + strata. NOT a skill name.

    e.g. "free-move beam, flat tempo" / "rooted summon, variable tempo".
    Omits any axis that is UNMAPPED/None (null-honest).
    """
    delivery = col.lower() if col else None
    move = MOVEMENT_WORD.get(row) if row else None
    tempo = AMP_WORD.get(stratum) if stratum else None

    shape_bits = [b for b in (move, delivery) if b]
    shape = " ".join(shape_bits) if shape_bits else None

    parts = [p for p in (shape, tempo) if p]
    return ", ".join(parts) if parts else None


def build_public_label(game_id, era_year, patch, mech_desc):
    """Assemble the public register string. NULL-honest at every segment."""
    if game_id and era_year is not None:
        head = f"{game_id}-{era_year}"
        if patch:
            head += f" (v{patch})"
        return f"{head} · {mech_desc}" if mech_desc else head
    # No historical game/era (e.g. abstract roster coordinates) — fall back to
    # whatever identity exists + the mechanical phrase.
    if mech_desc:
        return mech_desc
    return game_id or None


def build_dot_records(corpus_kits, roster_kits, roster_assignments):
    """Emit one record per rendered dot, per the per-dot JSON contract.

    Covers the plotted dots: corpus (ghost) + mint (★) from corpus_kits, and
    roster overlay dots. amp-NULL kits carry amp=null; UNMAPPED axes emit null.
    """
    records = []

    for kit in corpus_kits:
        row = resolve_row(kit)
        col = resolve_column(kit)
        stratum = resolve_stratum(kit)
        mech = mechanical_desc(row, col, stratum)
        game_id = kit["game"]
        era_year = kit["era_year"]
        patch = kit["stabilization_patch"]
        records.append({
            "dot_id": kit["kit_id"],
            "source": "mint" if kit["mint"] else "corpus",
            "cell": {"movement": row, "delivery": col, "amp": stratum},
            "cell_confident": (row is not None and col is not None),
            "public_label": build_public_label(game_id, era_year, patch, mech),
            "label_parts": {
                "game_id": game_id,
                "era_year": era_year,
                "stabilization_patch": patch,
                "mechanical_desc": mech,
            },
            "negative_canon": bool(kit["negative"]),
        })

    # Roster overlay: no historical game/era in roster_atlas; movement is
    # S7-emitted so all roster dots are UNMAPPED on the movement axis (cell
    # position pending S7 — names/labels are emitted regardless).
    roster_col = {a[1]: a[4] for a in roster_assignments}  # kid -> resolved col
    for kit in roster_kits:
        kid = kit["kit_id"]
        col = roster_col.get(kid)
        stratum = resolve_stratum({"amp_val": kit["amp"]})
        mech = mechanical_desc(None, col, stratum)  # movement UNMAPPED
        name = kit["lineage_name"] or kit["name"] or kid
        label = mech if mech else name
        records.append({
            "dot_id": kid,
            "source": "roster",
            "cell": {"movement": None, "delivery": col, "amp": stratum},
            "cell_confident": False,  # movement pending S7
            "public_label": label,
            "label_parts": {
                "game_id": None,
                "era_year": None,
                "stabilization_patch": None,
                "mechanical_desc": mech,
            },
            "negative_canon": False,
        })

    return records


def assign_all(corpus_kits, negative_kits):
    """Assign every combat kit to a (row, col, stratum) or UNMAPPED.

    Returns cells dict with structure:
      cells[(row, col)] = {"strata": {"FLAT": [kit,...], "SPIKY": [...], "VAR": [...]},
                            "unkeyed_amp": [kit,...],
                            "mint_by_stratum": {...}}
      cells["UNMAPPED"] = {"corpus": [...], "mint": [...], "negative": [...]}
    """
    def new_cell():
        return {
            "strata": {s: [] for s in AMP_STRATA},
            "unkeyed_amp": [],  # amp NULL sliver
            "mint_by_stratum": {s: [] for s in AMP_STRATA},
            "mint_unkeyed": [],
        }

    cells = {(r, c): new_cell() for r in PLANE_ROWS for c in PLANE_COLS}
    cells["UNMAPPED"] = {"corpus": [], "mint": [], "negative": []}
    audit = []

    for kit in corpus_kits:
        kid = kit["kit_id"]
        row = resolve_row(kit)
        col = resolve_column(kit)
        stratum = resolve_stratum(kit)

        if col is None or row is None:
            # UNMAPPED: either explicit residual, unknown movement, or geo unresolved
            reason = []
            if row is None:
                reason.append(f"movement='{kit['movement']}'")
            if col is None:
                if kid in UNMAPPED_COL and UNMAPPED_COL[kid] is None:
                    reason.append("residual (pure mobility)")
                else:
                    reason.append(f"geometry='{kit['geometry_value']}' delivery='{kit['delivery_value']}'")
            audit.append((kid, "UNMAPPED: " + ", ".join(reason)))
            if kit["mint"]:
                cells["UNMAPPED"]["mint"].append(dict(kit))
            else:
                cells["UNMAPPED"]["corpus"].append(dict(kit))
            continue

        # Placed in grid
        bucket = (row, col)
        if kid in UNMAPPED_COL:
            audit.append((kid, f"{row}×{col} (UNMAPPED-9 override; movement-derived row)"))

        if stratum is None:
            # amp NULL — unkeyed sliver
            if kit["mint"]:
                cells[bucket]["mint_unkeyed"].append(dict(kit))
            else:
                cells[bucket]["unkeyed_amp"].append(dict(kit))
        else:
            if kit["mint"]:
                cells[bucket]["mint_by_stratum"][stratum].append(dict(kit))
            else:
                cells[bucket]["strata"][stratum].append(dict(kit))

    for kit in negative_kits:
        cells["UNMAPPED"]["negative"].append(dict(kit))

    return cells, audit


# Roster geometry hints — inherited from V1/V1.1 render.
ROSTER_GEO_HINTS = {
    "K1":  "melee_strike",  "K2":  "melee_strike",  "K3":  "melee_strike",
    "K4":  "multi_projectile", "K5":  "totem", "K6":  "melee_strike",
    "K7":  "single_target", "K8":  "single_target", "K9c": "melee_strike",
    "K9f": "melee_strike",  "K10": "single_target", "K11": "ground_targeted_circle",
    "K12": "ground_targeted_circle", "K13": "ground_targeted_circle",
    "K14": "circle", "K15": "melee_strike", "K16": "ring",
    "K17": "totem", "K18": "totem", "K19": "beam_channel",
    "K20": "melee_strike", "K21": "ground_targeted_circle",
    "K22": "circle", "K23": "melee_strike", "K24": "totem",
    "K25": "totem", "K26": "aura", "K27": "aura",
    "K28": "melee_strike", "K29": "totem",
    "H1": "ring", "H2": "whirlwind", "H3": "totem",
    "H4": "circle", "H5": "melee_strike", "H6": "ground_targeted_circle",
    "B4": "line", "B5": "teleport", "B6": "dash_attack",
    "B7": "ring", "B8": "ring", "B9": "circle",
    "B10": "whirlwind", "B11": "totem", "B12": "whirlwind",
}


def assign_roster(roster_kits):
    """Roster kits: roster_atlas has no movement column. Per V1.1 honest-treatment
    precedent, roster kits with unknown movement (all of them, since the column
    doesn't exist) go to UNMAPPED-strip. Backfill is separately queued.
    """
    assignments = []
    for kit in roster_kits:
        kid = kit["kit_id"]
        name = kit["name"] or kid
        geo = ROSTER_GEO_HINTS.get(kid)
        col = GEO_TO_COL_BASE.get(geo) if geo else None

        # All roster kits UNMAPPED under V1.2 (no movement column in roster_atlas)
        note = "MOVEMENT_UNKNOWN"
        if kid == "B5":
            note = "UNMAPPED-residual (pure mobility)"
        elif col is None:
            note = "GEOMETRY_UNMAPPED"
        assignments.append(("UNMAPPED", kid, name, note, col, geo))
    return assignments


def jitter_points(n, cx, cy, cell_w, cell_h, margin=0.12, seed=42):
    if n == 0:
        return np.array([]), np.array([])
    rng = np.random.default_rng(seed)
    xs = rng.uniform(cx - cell_w * (0.5 - margin), cx + cell_w * (0.5 - margin), n)
    ys = rng.uniform(cy - cell_h * (0.5 - margin), cy + cell_h * (0.5 - margin), n)
    return xs, ys


def plot_stratified(ax, cells, roster_assignments, nrows, ncols):
    ax.set_xlim(-0.05, ncols + 0.05)
    ax.set_ylim(-1.15, nrows + 0.85)
    ax.set_aspect('equal')
    ax.axis('off')

    cell_w = 1.0
    cell_h = 1.0

    COLORS = {
        "corpus_ghost": "#B0B8C4",
        "mint": "#FFD700",
        "unkeyed_amp": "#FF6B9E",  # pink sliver for amp NULL
        "roster_kits": "#4CA3FF",
        "negative": "#FF6B6B",
        "cell_bg_flat": "#1B1F27",     # subtle top-stratum tint
        "cell_bg_spiky": "#20242D",    # subtle mid-stratum tint
        "cell_bg_var": "#252A34",      # subtle bottom-stratum tint
        "cell_border": "#334055",
        "cell_empty": "#0F1218",
        "cell_empty_border": "#1F2632",
        "stratum_sep": "#2A3746",  # thin separator between strata
        "cell_reassigned_border": "#5A7A9A",
    }

    STRATUM_BG = {
        "FLAT": COLORS["cell_bg_flat"],
        "SPIKY": COLORS["cell_bg_spiky"],
        "VAR": COLORS["cell_bg_var"],
    }

    # Cells receiving UNMAPPED-9 overrides — highlighted borders.
    # Derived: any cell that appears as a target in UNMAPPED_COL's non-None values,
    # crossed with the actual movement of that kit.
    reassign_target_cells = set()
    kit_movements = {
        "d3-inarius-bonestorm": ("WALK", "ORBITAL"),
        "d4-ball-lightning": ("FREE-MOVE", "ORBITAL"),
        "d4-bouldercane": ("WALK", "ORBITAL"),
        "poe1-poison-bv": ("FREE-MOVE", "ORBITAL"),
        "d2-firewall-sorc": ("FREE-MOVE", "ZONE"),
        "di-bone-wall-necro-pvp": ("ROOTED", "ZONE"),
        "le-frost-wall-rm": ("ROOTED", "ZONE"),
        "di-monk-sss": ("ROOTED", "MELEE"),
        "tq-phantom-strike-dreamkiller": ("ROOTED", "MELEE"),
    }
    for row, col in kit_movements.values():
        reassign_target_cells.add((row, col))

    # Column headers
    col_labels = ["➤ PROJECTILE", "◎ ORBITAL", "✳ NOVA", "▒ ZONE", "━ BEAM", "✕ MELEE", "☍ SUMMON"]
    for ci, lbl in enumerate(col_labels):
        ax.text(ci + 0.5, nrows + 0.32, lbl, ha='center', va='center',
                fontsize=9, color='#B8C0CA', fontweight='bold')

    # Row headers (with movement icon hint)
    row_glyphs = {"FREE-MOVE": "⇢⇢", "WALK": "⇢", "ROOTED": "✕"}
    for ri, lbl in enumerate(PLANE_ROWS):
        ax.text(-0.12, nrows - ri - 0.5, f"{row_glyphs[lbl]}  {lbl}",
                ha='right', va='center', fontsize=10, color='#B8C0CA', fontweight='bold')

    # Draw the 21 cells, each stratified into 3 horizontal bands
    for ri, row_val in enumerate(PLANE_ROWS):
        for ci, col_val in enumerate(PLANE_COLS):
            bucket = (row_val, col_val)
            cell_data = cells.get(bucket)
            corpus_flat = cell_data["strata"]["FLAT"]
            corpus_spiky = cell_data["strata"]["SPIKY"]
            corpus_var = cell_data["strata"]["VAR"]
            mint_flat = cell_data["mint_by_stratum"]["FLAT"]
            mint_spiky = cell_data["mint_by_stratum"]["SPIKY"]
            mint_var = cell_data["mint_by_stratum"]["VAR"]
            unkeyed = cell_data["unkeyed_amp"]
            mint_unkeyed = cell_data["mint_unkeyed"]

            per_stratum_totals = {
                "FLAT": len(corpus_flat) + len(mint_flat),
                "SPIKY": len(corpus_spiky) + len(mint_spiky),
                "VAR": len(corpus_var) + len(mint_var),
            }
            total = sum(per_stratum_totals.values()) + len(unkeyed) + len(mint_unkeyed)

            cell_left = ci + 0.04
            cell_bottom = nrows - ri - 1 + 0.04
            cell_width = cell_w - 0.08
            cell_full_height = cell_h - 0.08

            # Reserve a thin sliver at the bottom of the cell for unkeyed-amp
            # kits, iff any exist. Sliver height ~10% of cell.
            has_unkeyed = (len(unkeyed) + len(mint_unkeyed)) > 0
            sliver_h = cell_full_height * 0.10 if has_unkeyed else 0.0
            strata_area_h = cell_full_height - sliver_h
            stratum_h = strata_area_h / 3.0

            if total == 0:
                # Fully-empty cell — subdued render, still show strata separators
                rect = FancyBboxPatch(
                    (cell_left, cell_bottom),
                    cell_width, cell_full_height,
                    boxstyle="round,pad=0.02",
                    linewidth=0.8,
                    edgecolor=COLORS["cell_empty_border"],
                    facecolor=COLORS["cell_empty"],
                )
                ax.add_patch(rect)
            else:
                # Cell border (highlighted if it received an UNMAPPED-9 kit)
                is_reassign_target = bucket in reassign_target_cells
                brd = (COLORS["cell_reassigned_border"] if is_reassign_target
                       else COLORS["cell_border"])
                lw = 1.4 if is_reassign_target else 0.8
                rect = FancyBboxPatch(
                    (cell_left, cell_bottom),
                    cell_width, cell_full_height,
                    boxstyle="round,pad=0.02",
                    linewidth=lw,
                    edgecolor=brd,
                    facecolor=COLORS["cell_empty"],  # base; strata painted on top
                )
                ax.add_patch(rect)

            # Draw the three amp strata (FLAT top, SPIKY mid, VAR bottom)
            # even if a stratum is empty (empty strata stay visible per Matt).
            for si, stratum in enumerate(AMP_STRATA):
                # top→bottom, so FLAT is highest
                stratum_bottom = cell_bottom + sliver_h + (2 - si) * stratum_h
                stratum_top = stratum_bottom + stratum_h

                # Stratum background (visible even when empty; slightly-differentiated tint)
                if total > 0:
                    ax.add_patch(Rectangle(
                        (cell_left + 0.008, stratum_bottom),
                        cell_width - 0.016, stratum_h,
                        facecolor=STRATUM_BG[stratum],
                        edgecolor='none',
                        zorder=1.5,
                    ))

                # Ghost dots for corpus kits in this stratum
                corpus_here = cell_data["strata"][stratum]
                mint_here = cell_data["mint_by_stratum"][stratum]
                stratum_cx = cell_left + cell_width / 2
                stratum_cy = stratum_bottom + stratum_h / 2

                if corpus_here:
                    xs, ys = jitter_points(
                        len(corpus_here),
                        stratum_cx, stratum_cy,
                        cell_width * 0.78, stratum_h * 0.62,
                        seed=ri * 1000 + ci * 10 + si,
                    )
                    ax.scatter(xs, ys, s=3.4, color=COLORS["corpus_ghost"],
                               alpha=0.55, linewidths=0, zorder=2.5)

                if mint_here:
                    mxs, mys = jitter_points(
                        len(mint_here),
                        stratum_cx, stratum_cy,
                        cell_width * 0.55, stratum_h * 0.48,
                        seed=ri * 1000 + ci * 10 + si + 500,
                    )
                    ax.scatter(mxs, mys, s=28, marker='*', color=COLORS["mint"],
                               alpha=0.95, linewidths=0, zorder=4)

                # Per-stratum count (small, right-anchored inside stratum)
                cnt = len(corpus_here) + len(mint_here)
                if total > 0:
                    label_color = '#8AA0BC' if cnt > 0 else '#42505E'
                    ax.text(
                        cell_left + cell_width - 0.03, stratum_bottom + 0.02,
                        f"{stratum[0]}{cnt}",
                        ha='right', va='bottom',
                        fontsize=5.5, color=label_color, zorder=5,
                    )

                # Thin separator ABOVE this stratum (skip topmost)
                if si > 0 and total > 0:
                    ax.plot(
                        [cell_left + 0.02, cell_left + cell_width - 0.02],
                        [stratum_top, stratum_top],
                        color=COLORS["stratum_sep"], linewidth=0.5, zorder=3,
                    )

            # Unkeyed-amp sliver (if any) at the bottom of the cell
            if has_unkeyed:
                sliver_bottom = cell_bottom
                sliver_top = cell_bottom + sliver_h
                ax.add_patch(Rectangle(
                    (cell_left + 0.008, sliver_bottom),
                    cell_width - 0.016, sliver_h,
                    facecolor="#2B1E28",  # dark magenta hint
                    edgecolor=COLORS["unkeyed_amp"],
                    linewidth=0.5,
                    zorder=1.8,
                ))
                sliver_cx = cell_left + cell_width / 2
                sliver_cy = sliver_bottom + sliver_h / 2
                # Draw the unkeyed kit as a distinctive marker
                n_unk = len(unkeyed) + len(mint_unkeyed)
                ax.scatter([sliver_cx], [sliver_cy], s=14,
                           marker='D', color=COLORS["unkeyed_amp"],
                           alpha=0.95, linewidths=0, zorder=4)
                ax.text(cell_left + cell_width - 0.03, sliver_bottom + 0.005,
                        f"?{n_unk}", ha='right', va='bottom',
                        fontsize=5, color=COLORS["unkeyed_amp"], zorder=5)

            # Cell total in top-right corner (matches V1.1 convention)
            if total > 0:
                ax.text(
                    cell_left + cell_width - 0.02,
                    cell_bottom + cell_full_height - 0.03,
                    str(total),
                    ha='right', va='top',
                    fontsize=8, color='#C8D6E8', zorder=6, fontweight='bold',
                )

    # UNMAPPED strip
    unmapped_corpus = cells["UNMAPPED"]["corpus"]
    unmapped_mint = cells["UNMAPPED"]["mint"]
    unmapped_neg = cells["UNMAPPED"]["negative"]
    unmapped_roster = [a for a in roster_assignments if a[0] == "UNMAPPED"]

    strip_y = -0.55
    ax.text(-0.05, strip_y + 0.15,
            f"UNMAPPED: {len(unmapped_corpus)} corpus  ·  {len(unmapped_mint)} mint  ·  "
            f"{len(unmapped_neg)} negatives  ·  {len(unmapped_roster)} roster",
            ha='left', va='center', fontsize=8, color='#FF9966', zorder=5, fontweight='bold')

    # Group UNMAPPED corpus into (a) movement-unknown and (b) pure-mobility residual
    mov_unknown = [k for k in unmapped_corpus if k["movement"] == "unknown"]
    other_residual = [k for k in unmapped_corpus if k["movement"] != "unknown"]

    if mov_unknown:
        names = ", ".join(k["kit_id"] for k in mov_unknown)
        ax.text(-0.05, strip_y - 0.08,
                f"  movement=unknown ({len(mov_unknown)}): {names}",
                ha='left', va='center', fontsize=6, color='#FFB088', zorder=5)

    if other_residual:
        names = ", ".join(k["kit_id"] for k in other_residual)
        ax.text(-0.05, strip_y - 0.25,
                f"  pure-mobility residual ({len(other_residual)}): {names}",
                ha='left', va='center', fontsize=6, color='#FFB088', zorder=5)

    if unmapped_roster:
        rids = ", ".join(a[1] for a in unmapped_roster)
        ax.text(-0.05, strip_y - 0.42,
                f"  roster (movement column missing in roster_atlas; backfill queued): {rids}",
                ha='left', va='center', fontsize=5.5, color='#FFB088', zorder=5)


def main():
    print("Loading corpus DB (READ-ONLY)...")
    corpus_kits, negative_kits, roster_kits = load_data()
    print(f"  corpus combat kits: {len(corpus_kits)}")
    print(f"  negative kits: {len(negative_kits)}")
    print(f"  roster kits: {len(roster_kits)}")

    # Verify cone Path-2 split matches the brief exactly
    cones = [k for k in corpus_kits if k["geometry_value"] == "cone"]
    cone_beam = sorted(k["kit_id"] for k in cones if k["delivery_value"] == "beam")
    cone_proj = sorted(k["kit_id"] for k in cones if k["delivery_value"] == "projectile")
    expected_beam = sorted([
        "ud-flamethrower-channel", "poe1-incinerate",
        "gd-flames-of-ignaffar-purifier", "hot-dragons-breath",
        "hot-exterminator-burn",
    ])
    expected_proj = sorted([
        "tq-ternion-bone-charmer", "poe2-galvanic-shards",
        "di-vengeance-strafe-dh", "di-multishot-dh",
        "le-frost-claw", "tl2-shotgonne-outlander",
    ])
    if cone_beam != expected_beam or cone_proj != expected_proj:
        raise SystemExit(
            f"CONE PATH-2 DERIVATION MISMATCH — stopping.\n"
            f"  BEAM derived:  {cone_beam}\n"
            f"  BEAM expected: {expected_beam}\n"
            f"  PROJ derived:  {cone_proj}\n"
            f"  PROJ expected: {expected_proj}\n"
        )
    print(f"  cone Path-2 verified: {len(cone_beam)} beam + {len(cone_proj)} projectile")

    cells, audit = assign_all(corpus_kits, negative_kits)
    roster_assignments = assign_roster(roster_kits)

    print("\nUNMAPPED-9 + placement audit (V1.2 movement-derived rows):")
    for kid, note in audit:
        print(f"  {kid:35s} → {note}")

    # Figure — single 3×7 stratified plane
    fig = plt.figure(figsize=(18, 10), facecolor='#0B0D10')
    fig.patch.set_facecolor('#0B0D10')

    fig.text(0.5, 0.965,
             "V1.2 PLANE VIEW — RULED PLANE (movement rows × delivery columns × amp strata)",
             ha='center', fontsize=14, fontweight='bold', color='white')
    fig.text(0.5, 0.938,
             "3 movement rows × 7 delivery-family columns = 21 cells; "
             "each cell stratified top→bottom by amp: FLAT / SPIKY / VAR   ·   "
             "cone Path 2 applied (delivery-derived: 5 BEAM + 6 PROJECTILE)",
             ha='center', fontsize=8.5, color='#9AA3AD')
    fig.text(0.5, 0.916,
             "corpus (ghost dots · 463) · mint (★ · 9) · unkeyed-amp sliver (◆ pink · 1: d2-wl-void-rift)   ·   "
             "highlighted borders = cells receiving UNMAPPED-9 kits (rows derived from actual movement)",
             ha='center', fontsize=7.5, color='#9AA3AD')

    legend_elements = [
        mpatches.Patch(color='#B0B8C4', alpha=0.6, label='Corpus combat kit (462 keyed, ghost dot)'),
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FFD700',
                   markersize=10, linewidth=0, label='Mint kit (9, ★)'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#FF6B9E',
                   markersize=6, linewidth=0, label='Amp-NULL sliver (1: d2-wl-void-rift, ◆)'),
        mpatches.Patch(facecolor='#1B1F27', edgecolor='#5A7A9A', linewidth=1.5,
                       label='Cell received UNMAPPED-9 kits (highlighted border)'),
        mpatches.Patch(facecolor='#0F1218', edgecolor='#1F2632',
                       label='Empty cell / empty stratum (frontier)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3,
               fontsize=8, facecolor='#11161C', edgecolor='#334055',
               labelcolor='white', framealpha=0.9,
               bbox_to_anchor=(0.5, 0.015))

    ax = fig.add_axes([0.06, 0.16, 0.88, 0.72])
    ax.set_facecolor('#0B0D10')
    plot_stratified(ax, cells, roster_assignments, nrows=3, ncols=7)

    png_path = OUT_DIR / "plane_view_v1_2_stratified.png"
    fig.savefig(str(png_path), dpi=150, bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"\nSaved PNG: {png_path}")

    svg_path = OUT_DIR / "plane_view_v1_2_stratified.svg"
    fig.savefig(str(svg_path), format='svg', bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"Saved SVG: {svg_path}")

    plt.close(fig)

    # ── Per-dot JSON emission (Drax Phase-2 mouseover contract) ──────────────
    dot_records = build_dot_records(corpus_kits, roster_kits, roster_assignments)
    dots_path = OUT_DIR / "plane_dots_v1_2.json"
    with open(dots_path, "w") as f:
        json.dump({
            "schema": "atlas-plane-dots/v1.2",
            "provenance": "derived from corpus.db by render_v1_2_stratified.py; "
                          "no authored content, no LLM in truth path (D6)",
            "count": len(dot_records),
            "dots": dot_records,
        }, f, indent=2)
    labeled = sum(1 for d in dot_records if d["public_label"])
    confident = sum(1 for d in dot_records if d["cell_confident"])
    print(f"Saved dots JSON: {dots_path} "
          f"({len(dot_records)} dots · {labeled} labeled · {confident} cell-confident)")

    return cells, roster_assignments, audit


if __name__ == "__main__":
    main()
