"""
V1.1 Plane View — B' Single-Plane Re-render
Renders the corrected Plane B' (3 commitment × 7 delivery-family = 21 cells).

Derived from render_v1_plane.py conventions (dark bg, ghost dots, mint stars,
labeled roster kits, UNMAPPED strip, count annotations).

B' vs mock B changes:
  1. RING column merged into ORBITAL (see lock addendum §2).
  2. NOVA/ZONE deterministic rule: circle → NOVA, ground_targeted_circle → ZONE,
     cone → ZONE (see lock addendum §3, plus ambiguity census).
  3. UNMAPPED-9 placements: 4 orbit-flagged NULL-geo → SNAP×ORBITAL,
     2 walls-flagged NULL-geo + 1 walls-demand totem → SNAP×ZONE,
     2 teleport-strike (di-monk-sss, tq-phantom-strike) → SNAP×MELEE via dash_attack
     precedent, 1 pure-mobility teleport (poe2-temporalis-blink) → UNMAPPED-residual
     (see lock addendum §4).

Author: gandalf sub-agent, 2026-07-13
"""

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]  # reincarnated-collaboration/
DB_PATH = REPO_ROOT / "agentic_orchestration" / "research" / "curated" / "corpus.db"
OUT_DIR = SCRIPT_DIR

# ── B' PLANE STRUCTURE ─────────────────────────────────────────────────────
PLANE_BP_ROWS = ["SNAP", "WIND-UP", "CHANNEL"]
PLANE_BP_COLS = ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON"]

ROW_TO_COMMIT = {"SNAP": "instant", "WIND-UP": "wind-up", "CHANNEL": "channel"}

# geometry_value → B' column (deterministic; NOVA/ZONE rule per lock addendum §3)
# RING geometry now routes to ORBITAL (merge per addendum §2).
GEO_TO_BP_COL = {
    "single_target": "PROJECTILE",
    "multi_projectile": "PROJECTILE",
    "fork": "PROJECTILE",
    "ricochet_bounce": "PROJECTILE",
    "chain": "PROJECTILE",
    "line": "PROJECTILE",
    "ring": "ORBITAL",  # ← RING merged into ORBITAL
    "vortex_pull": "ORBITAL",
    "whirlwind": "ORBITAL",
    "aura": "ORBITAL",
    "circle": "NOVA",  # ← deterministic NOVA/ZONE rule
    "ground_targeted_circle": "ZONE",
    "cone": "ZONE",  # geometry-grain default; ambiguity flagged (see addendum §3)
    "beam_channel": "BEAM",
    "melee_strike": "MELEE",
    "melee_arc": "MELEE",
    "dash_attack": "MELEE",
    "ground_slam": "MELEE",
    "totem": "SUMMON",
    "self_buff": "SUMMON",
    "teleport": None,  # handled per-kit in reassignment (addendum §4)
    None: None,        # NULL geometry handled per-kit in reassignment (addendum §4)
}

# UNMAPPED-9 explicit reassignments per addendum §4
UNMAPPED_REASSIGN = {
    # 4 orbit-flagged NULL-geo → ORBITAL (SNAP row, all commit=instant)
    "d3-inarius-bonestorm": ("SNAP", "ORBITAL"),
    "d4-ball-lightning": ("SNAP", "ORBITAL"),
    "d4-bouldercane": ("SNAP", "ORBITAL"),
    "poe1-poison-bv": ("SNAP", "ORBITAL"),
    # 2 walls-flagged NULL-geo → ZONE (placed persistent lane) + 1 walls-demand totem
    "d2-firewall-sorc": ("SNAP", "ZONE"),
    "di-bone-wall-necro-pvp": ("SNAP", "ZONE"),
    "le-frost-wall-rm": ("SNAP", "ZONE"),  # overrides default SUMMON routing via totem geo
    # 2 teleport-strike kits → MELEE via dash_attack precedent (probe delivery=at-target melee)
    "di-monk-sss": ("SNAP", "MELEE"),
    "tq-phantom-strike-dreamkiller": ("SNAP", "MELEE"),
    # 1 pure-mobility teleport → UNMAPPED-residual
    "poe2-temporalis-blink": ("UNMAPPED", None),
}


def load_data():
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    corpus_kits = con.execute("""
        SELECT c.kit_id, c.folk_name, c.game, c.commit_val,
               k.geometry_value, c.negative, c.mint
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
        SELECT r.kit_id, r.name, r.commit_slot,
               rle.bc6_commit, rle.bc6_attr, rle.folk_name as lineage_name
        FROM roster_atlas r
        LEFT JOIN roster_lineage_enrichment rle ON r.kit_id = rle.kit_id
        ORDER BY r.kit_id
    """).fetchall()
    con.close()
    return corpus_kits, negative_kits, roster_kits


def assign_bprime(corpus_kits, negative_kits):
    """Assign each combat kit to a B' cell or UNMAPPED. Returns cells dict + reassign audit."""
    cells = {(r, c): {"corpus": [], "mint": []} for r in PLANE_BP_ROWS for c in PLANE_BP_COLS}
    cells["UNMAPPED"] = {"corpus": [], "mint": [], "negative": []}
    reassign_audit = []

    for kit in corpus_kits:
        kid = kit["kit_id"]
        commit = kit["commit_val"] or "instant"
        geo = kit["geometry_value"]

        # UNMAPPED-9 explicit rules take precedence
        if kid in UNMAPPED_REASSIGN:
            row, col = UNMAPPED_REASSIGN[kid]
            if row == "UNMAPPED":
                bucket = "UNMAPPED"
                reassign_audit.append((kid, "UNMAPPED-residual (pure mobility)"))
            else:
                bucket = (row, col)
                prior = "NULL geometry" if geo is None else f"geometry={geo}"
                reassign_audit.append((kid, f"{row}×{col} (prior: {prior})"))
        else:
            # Deterministic geometry → column mapping
            col = GEO_TO_BP_COL.get(geo)
            if col is None:
                bucket = "UNMAPPED"
            else:
                # commit → row
                row = None
                for r, cv in ROW_TO_COMMIT.items():
                    if commit == cv:
                        row = r
                        break
                if row is None:
                    row = "SNAP"  # default (matches V1 render treatment of NULL commit)
                bucket = (row, col)

        if kit["mint"]:
            cells[bucket]["mint"].append(dict(kit))
        else:
            if bucket == "UNMAPPED":
                cells["UNMAPPED"]["corpus"].append(dict(kit))
            else:
                cells[bucket]["corpus"].append(dict(kit))

    for kit in negative_kits:
        cells["UNMAPPED"]["negative"].append(dict(kit))

    return cells, reassign_audit


# Roster geometry hints — inherited from V1 render (docstring conventions match).
ROSTER_GEO_HINTS = {
    "K1":  "melee_strike",
    "K2":  "melee_strike",
    "K3":  "melee_strike",
    "K4":  "multi_projectile",
    "K5":  "totem",
    "K6":  "melee_strike",
    "K7":  "single_target",
    "K8":  "single_target",
    "K9c": "melee_strike",
    "K9f": "melee_strike",
    "K10": "single_target",
    "K11": "ground_targeted_circle",
    "K12": "ground_targeted_circle",
    "K13": "ground_targeted_circle",
    "K14": "circle",
    "K15": "melee_strike",
    "K16": "ring",
    "K17": "totem",
    "K18": "totem",
    "K19": "beam_channel",
    "K20": "melee_strike",
    "K21": "ground_targeted_circle",
    "K22": "circle",
    "K23": "melee_strike",
    "K24": "totem",
    "K25": "totem",
    "K26": "aura",
    "K27": "aura",
    "K28": "melee_strike",
    "K29": "totem",
    "H1":  "ring",
    "H2":  "whirlwind",
    "H3":  "totem",
    "H4":  "circle",
    "H5":  "melee_strike",
    "H6":  "ground_targeted_circle",
    "B4":  "line",
    "B5":  "teleport",
    "B6":  "dash_attack",
    "B7":  "ring",
    "B8":  "ring",
    "B9":  "circle",
    "B10": "whirlwind",
    "B11": "totem",
    "B12": "whirlwind",
}


def roster_commit(kit):
    c = kit["bc6_commit"] or kit["commit_slot"] or "_"
    mapping = {"I": "instant", "W": "wind-up", "C": "channel",
               "instant": "instant", "wind-up": "wind-up", "channel": "channel"}
    return mapping.get(c, None)


def assign_roster_bprime(roster_kits):
    assignments = []
    for kit in roster_kits:
        kid = kit["kit_id"]
        name = kit["name"] or kid
        commit = roster_commit(kit)
        geo = ROSTER_GEO_HINTS.get(kid)
        col = GEO_TO_BP_COL.get(geo) if geo else None

        # Special-case B5 teleport-pure (Teleport Sorceress) → UNMAPPED-residual
        if kid == "B5":
            assignments.append(("UNMAPPED", kid, name))
            continue

        if col is None:
            assignments.append(("UNMAPPED", kid, name))
            continue

        # Map commit → row
        row = None
        if commit:
            for r, cv in ROW_TO_COMMIT.items():
                if commit == cv:
                    row = r
                    break
        if row is None:
            assignments.append(("COMMIT_UNKNOWN", kid, name))
            continue
        assignments.append(((row, col), kid, name))
    return assignments


def jitter_points(n, cx, cy, cell_w, cell_h, margin=0.12, seed=42):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(cx - cell_w * (0.5 - margin), cx + cell_w * (0.5 - margin), n)
    ys = rng.uniform(cy - cell_h * (0.5 - margin), cy + cell_h * (0.5 - margin), n)
    return xs, ys


def plot_bprime(ax, cells, roster_assignments, nrows, ncols):
    ax.set_xlim(0, ncols)
    ax.set_ylim(-0.9, nrows + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')

    cell_w = 1.0
    cell_h = 1.0

    COLORS = {
        "corpus_ghost": "#B0B8C4",
        "mint": "#FFD700",
        "roster_kits": "#4CA3FF",
        "negative": "#FF6B6B",
        "cell_bg": "#1A1F27",
        "cell_border": "#334055",
        "cell_empty": "#111520",
        "cell_empty_border": "#223",
        "cell_reassigned": "#2A3540",  # subtle highlight for cells receiving UNMAPPED-9 kits
        "cell_reassigned_border": "#5A7A9A",
    }

    # Cells that receive UNMAPPED-9 kits (highlight border)
    reassign_target_cells = {(r, c) for (r, c) in [v for v in UNMAPPED_REASSIGN.values() if v[0] != "UNMAPPED"]}

    # Column headers
    col_labels = ["➤ PROJECTILE", "◎ ORBITAL", "✳ NOVA", "▒ ZONE", "━ BEAM", "✕ MELEE", "☍ SUMMON"]
    for ci, lbl in enumerate(col_labels):
        ax.text(ci + 0.5, nrows + 0.32, lbl, ha='center', va='center',
                fontsize=9, color='#B8C0CA', fontweight='bold')

    # Row headers
    for ri, lbl in enumerate(PLANE_BP_ROWS):
        ax.text(-0.15, nrows - ri - 0.5, lbl, ha='right', va='center',
                fontsize=10, color='#B8C0CA', fontweight='bold')

    # Draw cells
    for ri, row_val in enumerate(PLANE_BP_ROWS):
        for ci, col_val in enumerate(PLANE_BP_COLS):
            bucket = (row_val, col_val)
            cell_data = cells.get(bucket, {"corpus": [], "mint": []})
            corpus_in = cell_data.get("corpus", [])
            mint_in = cell_data.get("mint", [])
            total = len(corpus_in) + len(mint_in)

            cx = ci + 0.5
            cy = nrows - ri - 0.5

            if total > 0:
                bg = COLORS["cell_bg"]
                brd = (COLORS["cell_reassigned_border"] if bucket in reassign_target_cells
                       else COLORS["cell_border"])
                lw = 1.4 if bucket in reassign_target_cells else 0.8
            else:
                bg = COLORS["cell_empty"]
                brd = COLORS["cell_empty_border"]
                lw = 0.8

            rect = FancyBboxPatch(
                (ci + 0.04, nrows - ri - 0.04 - cell_h + 0.08),
                cell_w - 0.08, cell_h - 0.08,
                boxstyle="round,pad=0.02",
                linewidth=lw,
                edgecolor=brd,
                facecolor=bg,
            )
            ax.add_patch(rect)

            # Ghost dots
            if corpus_in:
                xs, ys = jitter_points(len(corpus_in), cx, cy, cell_w * 0.78, cell_h * 0.55,
                                       seed=ri * 100 + ci)
                ax.scatter(xs, ys, s=4, color=COLORS["corpus_ghost"], alpha=0.4,
                           linewidths=0, zorder=2)

            # Mint stars
            if mint_in:
                mxs, mys = jitter_points(len(mint_in), cx, cy, cell_w * 0.6, cell_h * 0.4,
                                         seed=ri * 100 + ci + 500)
                ax.scatter(mxs, mys, s=36, marker='*', color=COLORS["mint"],
                           alpha=0.95, linewidths=0, zorder=4)

            # Count
            if total > 0:
                ax.text(ci + cell_w - 0.07, nrows - ri - cell_h + 0.1,
                        str(total), ha='right', va='bottom',
                        fontsize=7.5, color='#8AA0BC', zorder=5, fontweight='bold')

    # Roster markers
    for bucket, kid, name in roster_assignments:
        if bucket in ("UNMAPPED", "COMMIT_UNKNOWN"):
            continue
        row_val, col_val = bucket
        if row_val not in PLANE_BP_ROWS or col_val not in PLANE_BP_COLS:
            continue
        ri = PLANE_BP_ROWS.index(row_val)
        ci = PLANE_BP_COLS.index(col_val)
        cx = ci + 0.5
        cy = nrows - ri - 0.5
        h = hash(kid) % 10000
        rng = np.random.default_rng(h)
        ox = rng.uniform(-0.3, 0.3)
        oy = rng.uniform(-0.22, 0.22)
        ax.scatter([cx + ox], [cy + oy], s=32, color=COLORS["roster_kits"],
                   alpha=0.95, linewidths=0.6, edgecolors='white', zorder=6)
        ax.text(cx + ox, cy + oy + 0.14, kid,
                ha='center', va='bottom', fontsize=5.5, color='white',
                fontweight='bold', zorder=7)

    # UNMAPPED strip
    unmapped_corpus = cells.get("UNMAPPED", {}).get("corpus", [])
    unmapped_neg = cells.get("UNMAPPED", {}).get("negative", [])
    unmapped_roster = [b for b, kid, name in roster_assignments
                       if b in ("UNMAPPED", "COMMIT_UNKNOWN")]

    strip_y = -0.4
    ax.text(0, strip_y + 0.15,
            f"UNMAPPED: {len(unmapped_corpus)} corpus · {len(unmapped_neg)} negatives · "
            f"{len(unmapped_roster)} roster",
            ha='left', va='center', fontsize=8, color='#FF9966', zorder=5, fontweight='bold')

    if unmapped_corpus:
        residual_names = ", ".join(k["kit_id"] for k in unmapped_corpus)
        ax.text(0, strip_y - 0.15,
                f"  Residual corpus (pure mobility, non-damage): {residual_names}",
                ha='left', va='center', fontsize=6.5, color='#FF9966', zorder=5)

    if unmapped_roster:
        residual_roster = ", ".join(kid for _, kid, _ in roster_assignments
                                     if _ in ("UNMAPPED", "COMMIT_UNKNOWN"))
        ax.text(0, strip_y - 0.35,
                f"  Roster (commit-unknown or pure-mobility): {residual_roster}",
                ha='left', va='center', fontsize=6.5, color='#FF9966', zorder=5)


def main():
    print("Loading corpus DB (READ-ONLY)...")
    corpus_kits, negative_kits, roster_kits = load_data()
    print(f"  corpus combat kits: {len(corpus_kits)}")
    print(f"  negative kits: {len(negative_kits)}")
    print(f"  roster kits: {len(roster_kits)}")

    cells_bp, reassign_audit = assign_bprime(corpus_kits, negative_kits)
    roster_bp = assign_roster_bprime(roster_kits)

    print("\nUNMAPPED-9 reassignment audit:")
    for kid, note in reassign_audit:
        print(f"  {kid:35s} → {note}")

    # Figure — single 3×7 plane, generous size for cell readability
    fig = plt.figure(figsize=(16, 9), facecolor='#0B0D10')
    fig.patch.set_facecolor('#0B0D10')

    fig.text(0.5, 0.965,
             "V1.1 PLANE VIEW — PLANE B′ (Q19 CANDIDATE)",
             ha='center', fontsize=14, fontweight='bold', color='white')
    fig.text(0.5, 0.935,
             "3 commitment rows × 7 delivery-family columns = 21 cells   ·   "
             "RING merged into ORBITAL   ·   UNMAPPED-9 placed per lock addendum",
             ha='center', fontsize=8.5, color='#9AA3AD')
    fig.text(0.5, 0.913,
             "corpus (ghost dots · 463) · mint (★ · 9) · roster engine kits (● labeled · 45) · "
             "highlighted borders = cells receiving UNMAPPED-9 kits",
             ha='center', fontsize=7.5, color='#9AA3AD')

    legend_elements = [
        mpatches.Patch(color='#B0B8C4', alpha=0.5, label='Corpus combat kit (463 total, ghost dot)'),
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#FFD700',
                   markersize=10, linewidth=0, label='Mint kit (9 total, ★)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CA3FF',
                   markersize=8, linewidth=0, label='Engine roster kit (45 total, labeled)'),
        mpatches.Patch(facecolor='#1A1F27', edgecolor='#5A7A9A', linewidth=1.5,
                       label='Cell received UNMAPPED-9 kits (highlighted border)'),
        mpatches.Patch(facecolor='#111520', edgecolor='#223',
                       label='Empty cell (frontier)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3,
               fontsize=8, facecolor='#11161C', edgecolor='#334055',
               labelcolor='white', framealpha=0.9,
               bbox_to_anchor=(0.5, 0.015))

    ax = fig.add_axes([0.05, 0.14, 0.9, 0.74])
    ax.set_facecolor('#0B0D10')
    plot_bprime(ax, cells_bp, roster_bp, nrows=3, ncols=7)

    png_path = OUT_DIR / "plane_view_v1_1_bprime.png"
    fig.savefig(str(png_path), dpi=150, bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"\nSaved PNG: {png_path}")

    svg_path = OUT_DIR / "plane_view_v1_1_bprime.svg"
    fig.savefig(str(svg_path), format='svg', bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"Saved SVG: {svg_path}")

    plt.close(fig)

    return cells_bp, roster_bp, reassign_audit


if __name__ == "__main__":
    main()
