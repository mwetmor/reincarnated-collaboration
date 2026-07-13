"""
V1 Plane View — Q19 Plane-Lock Decision Instrument
Renders Plane A (15-cell spec grid) and Plane B (Matt's mock structure) side by side.

Author: synthetic team, 2026-07-12
"""

import sqlite3
import os
import json
import random
import math
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT   = SCRIPT_DIR.parents[3]          # reincarnated-collaboration/
DB_PATH     = REPO_ROOT / "agentic_orchestration" / "research" / "curated" / "corpus.db"
OUT_DIR     = SCRIPT_DIR

# ── 24→5 Rollup Table (Plane A dispersion-v1 families) ─────────────────────
# Ground: substrate-coordinates.md §1 Axis 2 definition
#   single | chain | small-AOE | large-AOE | multi-spawn
#
# 24 geometry_value types from DB:
#   ground_targeted_circle, circle, totem, multi_projectile, single_target,
#   melee_strike, chain, whirlwind, dash_attack, vortex_pull, cone, ring,
#   line, aura, self_buff, teleport, beam_channel, ricochet_bounce, ground_slam,
#   melee_arc, fork, NULL(6 kits)
#
# Rollup discipline: cite Axis 2 definition where unambiguous; FLAG judgment calls.

GEO_ROLLUP = {
    # ── SINGLE: one-point, one-impact, does not hop, does not spread ──
    "single_target":    ("single",      "def",       "Axis 2 def: one impact point"),
    "melee_strike":     ("single",      "def",       "Axis 2 def: one impact, melee geometry; footprint 1"),
    "dash_attack":      ("single",      "def",       "Melee-range single contact; footprint 1, no aoe spread"),
    "ground_slam":      ("single",      "def",       "Footprint 1 impact point despite short cone — classic single in genre (D2 Smite / PoE Leap Slam pattern)"),
    "melee_arc":        ("single",      "judgment",  "Narrow arc; footprint effectively 1 target per swing in corpus use — filed single vs small-AOE; judgment: genre precedent favors single for tight-arc melee"),
    "fork":             ("chain",       "judgment",  "Fork = projectile that splits on hit (2 branches); sequential-hop pattern closer to chain than single; judgment: fork is chain-subtype, not AOE"),
    "ricochet_bounce":  ("chain",       "def",       "Axis 2 def: chain = one moving point, sequential hops; ricochet is the canonical chain exemplar"),
    "chain":            ("chain",       "def",       "Axis 2 def: chain = sequential hops"),
    "multi_projectile": ("chain",       "judgment",  "Multiple simultaneous projectiles = canonical chain-pattern precursor (D2 Multi-Shot, PoE Barrage); footprint = multiple traveling points; dispersion per-hop not per-region; judgment: chain over large_aoe because the volley radiates from one cast-point sequentially/simultaneously — not a contiguous region"),
    # ── SMALL-AOE: compact region, <~50% arena ──
    "cone":             ("small_aoe",   "def",       "Axis 2 def: compact region; cone is bounded forward sweep"),
    "line":             ("small_aoe",   "def",       "Line AoE = narrow compact region (lightning bolt, ice lance)"),
    "vortex_pull":      ("small_aoe",   "judgment",  "Pull vortex draws targets into 1 location; effective footprint compact; judgment: small-aoe vs single — multi-target impact but compact; filed small-aoe"),
    "whirlwind":        ("small_aoe",   "def",       "Spinning melee aura = compact constant region around caster; small-AOE by extent"),
    "beam_channel":     ("small_aoe",   "judgment",  "Beam = sustained linear region; footprint long but narrow; judgment: small-aoe vs single — more than one point but not wide; filed small-aoe over single for multi-target line"),
    # ── LARGE-AOE: wide region, arena-scale ──
    "ground_targeted_circle": ("large_aoe", "def",   "Axis 2 def: wide region; circle at target = arena-covering in genre usage (Blizzard, Meteor, Desecrate)"),
    "circle":           ("large_aoe",   "def",       "Axis 2 def: wide region; circle is the canonical large-aoe shape"),
    "aura":             ("large_aoe",   "judgment",  "Aura = persistent omnidirectional radius = large constant region; judgment: large-aoe vs multi-spawn — no separate entity spawned; filed large-aoe"),
    "ring":             ("large_aoe",   "judgment",  "Ring = expanding/fixed large radial region; judgment: large-aoe vs multi-spawn — ring IS the damage region, not spawns; filed large-aoe"),
    # ── MULTI-SPAWN: many autonomous origins ──
    "totem":            ("multi_spawn", "judgment",  "Totem = persistent autonomous entity that fires independently; judgment: multi-spawn; identical to 'standing army' archetype in spec §2.1"),
    "self_buff":        ("multi_spawn", "judgment",  "Self-buff kits in corpus are companion/minion-empowering passives; judgment: multi-spawn proxy — UNMAPPED-LEANING but best-fit is multi-spawn given proxy dimension. Flagged: 5 kits; if kit has no damage geometry it should be UNMAPPED"),
    # ── UNMAPPED ──
    "teleport":         ("UNMAPPED",    "judgment",  "Teleport is mobility, not damage geometry; cannot be mapped to Axis 2 dispersion without knowing primary damage skill"),
    None:               ("UNMAPPED",    "judgment",  "NULL geometry = geometry not keyed; cannot be placed"),
}

# Plane A grid definition (spec §2.1)
PLANE_A_ROWS    = ["instant", "wind-up", "channel"]
PLANE_A_COLS    = ["single", "chain", "small_aoe", "large_aoe", "multi_spawn"]
PLANE_A_COL_LABELS = ["SINGLE", "CHAIN", "SMALL-AOE", "LARGE-AOE", "MULTI-SPAWN"]
PLANE_A_ROW_LABELS = ["INSTANT", "WIND-UP", "CHANNEL"]

# Plane B structure (parsed from Matt's SVG mock)
# SVG text elements extracted verbatim:
#   Column headers (x-positions 196→1036, 8 columns):
#     "➤ PROJECTILE" | "◎ ORBITAL" | "✳ NOVA" | "▒ ZONE" | "━ BEAM" | "✕ MELEE" | "☍ SUMMON" | "◯ RING"
#   Row headers (3 rows):
#     "SNAP" | "WIND-UP" | "CHANNEL"
PLANE_B_COLS    = ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON", "RING"]
PLANE_B_ROWS    = ["SNAP", "WIND-UP", "CHANNEL"]

# Plane B geometry rollup: SVG delivery-family → Axis 2 types
PLANE_B_ROLLUP = {
    "PROJECTILE": ["single_target", "multi_projectile", "fork", "ricochet_bounce", "chain", "line"],
    "ORBITAL":    ["ring", "vortex_pull", "whirlwind", "aura"],
    "NOVA":       ["circle", "ground_targeted_circle"],
    "ZONE":       ["ground_targeted_circle", "circle", "cone"],
    "BEAM":       ["beam_channel"],
    "MELEE":      ["melee_strike", "melee_arc", "dash_attack", "ground_slam"],
    "SUMMON":     ["totem", "self_buff"],
    "RING":       ["ring"],
}

# Plane B geometry rollup judgment notes
PLANE_B_ROLLUP_NOTES = {
    "PROJECTILE": "Maps to: single_target, multi_projectile, fork, ricochet_bounce, chain (sequential), line — the traveling-entity family",
    "ORBITAL":    "Maps to: ring, vortex_pull, whirlwind, aura — rotating/orbiting persistent region; OVERLAP with RING column",
    "NOVA":       "Maps to: circle, ground_targeted_circle — instant burst; OVERLAP with ZONE (both accept circle types)",
    "ZONE":       "Maps to: ground_targeted_circle, circle, cone — placed ground regions; OVERLAP with NOVA",
    "BEAM":       "Maps to: beam_channel only — narrow sustained linear; clean mapping",
    "MELEE":      "Maps to: melee_strike, melee_arc, dash_attack, ground_slam — contact range",
    "SUMMON":     "Maps to: totem, self_buff — autonomous spawned entities",
    "RING":       "Maps to: ring only; judgment: OVERLAP with ORBITAL (ring appears in both families in mock)",
}

# Plane B row mapping to commit enum
PLANE_B_ROW_TO_COMMIT = {
    "SNAP":      "instant",    # 'SNAP' = SVG mock label for instant commitment
    "WIND-UP":   "wind-up",
    "CHANNEL":   "channel",
}

# ── Invert rollup: geometry_value → Plane A col ────────────────────────────
def geo_to_plane_a(geo_val):
    """Return (family, flag) for a geometry_value. Returns ('UNMAPPED', ...) if unmapped."""
    entry = GEO_ROLLUP.get(geo_val)
    if entry is None:
        # Not in table at all
        return ("UNMAPPED", "judgment", f"geometry_value '{geo_val}' not in rollup table")
    return entry

def geo_to_plane_b_cols(geo_val):
    """Return list of Plane B columns that claim this geometry_value."""
    cols = []
    for col, geos in PLANE_B_ROLLUP.items():
        if geo_val in geos:
            cols.append(col)
    return cols if cols else ["UNMAPPED"]

# ── Load data from DB ───────────────────────────────────────────────────────
def load_data():
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row

    # Corpus combat kits (463)
    corpus_kits = con.execute("""
        SELECT c.kit_id, c.folk_name, c.game, c.commit_val,
               k.geometry_value, c.negative, c.mint
        FROM canon_corpus c
        JOIN canon_engine_key k ON c.kit_id = k.kit_id
        WHERE k.row_class = 'combat-kit'
        ORDER BY c.kit_id
    """).fetchall()

    # Negative kits (no engine key, not combat-kit)
    negative_kits = con.execute("""
        SELECT c.kit_id, c.folk_name, c.commit_val, c.negative
        FROM canon_corpus c
        LEFT JOIN canon_engine_key k ON c.kit_id = k.kit_id
        WHERE c.negative = 1
        ORDER BY c.kit_id
    """).fetchall()

    # Roster kits (45)
    roster_kits = con.execute("""
        SELECT r.kit_id, r.name, r.commit_slot,
               rle.bc6_commit, rle.bc6_attr, rle.folk_name as lineage_name
        FROM roster_atlas r
        LEFT JOIN roster_lineage_enrichment rle ON r.kit_id = rle.kit_id
        ORDER BY r.kit_id
    """).fetchall()

    con.close()
    return corpus_kits, negative_kits, roster_kits

# ── Assign kits to Plane A cells ────────────────────────────────────────────
def assign_plane_a(corpus_kits, negative_kits, roster_kits):
    """Returns dicts keyed by (row, col) containing lists of kit records."""
    cells = {(r, c): {"corpus": [], "mint": [], "negative": [], "unmapped": []}
             for r in PLANE_A_ROWS for c in PLANE_A_COLS}
    cells["UNMAPPED"] = {"corpus": [], "mint": [], "negative": [], "unmapped": []}

    for kit in corpus_kits:
        commit = kit["commit_val"] or "instant"  # 1 NULL → default instant
        geo    = kit["geometry_value"]
        family, flag, _ = geo_to_plane_a(geo)

        if family == "UNMAPPED":
            bucket = "UNMAPPED"
        else:
            if commit not in PLANE_A_ROWS:
                commit = "instant"
            bucket = (commit, family)

        if kit["mint"]:
            cells[bucket]["mint"].append(dict(kit))
        else:
            cells[bucket]["corpus"].append(dict(kit))

    # Negatives: no geometry key; put in UNMAPPED strip
    for kit in negative_kits:
        cells["UNMAPPED"]["negative"].append(dict(kit))

    return cells

# ── Assign kits to Plane B cells ────────────────────────────────────────────
def assign_plane_b(corpus_kits, negative_kits, roster_kits):
    """Returns dicts keyed by (row, col) where row in PLANE_B_ROWS, col in PLANE_B_COLS."""
    cells = {(r, c): {"corpus": [], "mint": [], "negative": [], "unmapped": []}
             for r in PLANE_B_ROWS for c in PLANE_B_COLS}
    cells["UNMAPPED"] = {"corpus": [], "mint": [], "negative": [], "unmapped": []}

    for kit in corpus_kits:
        commit = kit["commit_val"] or "instant"
        geo    = kit["geometry_value"]

        # Map commit to Plane B row
        row_b = None
        for row, cval in PLANE_B_ROW_TO_COMMIT.items():
            if commit == cval:
                row_b = row
                break
        if row_b is None:
            row_b = "SNAP"  # default

        # Map geometry to Plane B col(s)
        b_cols = geo_to_plane_b_cols(geo)

        if b_cols == ["UNMAPPED"]:
            bucket_list = ["UNMAPPED"]
        else:
            bucket_list = [(row_b, c) for c in b_cols]

        # When a kit maps to multiple columns (overlap), place in first-listed
        bucket = bucket_list[0]

        if kit["mint"]:
            cells[bucket]["mint"].append(dict(kit))
        else:
            cells[bucket]["corpus"].append(dict(kit))

    for kit in negative_kits:
        cells["UNMAPPED"]["negative"].append(dict(kit))

    return cells

# ── Roster commitment assignment ─────────────────────────────────────────────
def roster_commit(kit):
    """Return commit string for a roster kit from bc6_commit or commit_slot."""
    c = kit["bc6_commit"] or kit["commit_slot"] or "_"
    mapping = {"I": "instant", "W": "wind-up", "C": "channel",
               "instant": "instant", "wind-up": "wind-up", "channel": "channel"}
    return mapping.get(c, None)

# ── Roster geometry inference ─────────────────────────────────────────────────
# Known geometry associations by kit name pattern (best effort from kit identity)
ROSTER_GEO_HINTS = {
    "K1":  "melee_strike",       # Heavy Barbarian
    "K2":  "melee_strike",       # Light Fighter
    "K3":  "melee_strike",       # Polearm Soldier
    "K4":  "multi_projectile",   # Thrown-Heavy / Atlatl
    "K5":  "totem",              # Ancestor-Warrior (totems)
    "K6":  "melee_strike",       # Dagger Assassin
    "K7":  "single_target",      # Archer
    "K8":  "single_target",      # Crossbow Sniper
    "K9c": "melee_strike",       # Twin-Blade Fencer
    "K9f": "melee_strike",       # Twin-Blade Fencer
    "K10": "single_target",      # Falconer
    "K11": "ground_targeted_circle", # Trap Assassin (area traps)
    "K12": "ground_targeted_circle", # Standard Wizard
    "K13": "ground_targeted_circle", # Artillery Mage
    "K14": "circle",             # Pyromantic Caster (nova/fire)
    "K15": "melee_strike",       # Red Mage / Spellsword
    "K16": "ring",               # Arcane-Familiar Mage (orbital)
    "K17": "totem",              # Necromancer Summoner
    "K18": "totem",              # Totem Hierophant
    "K19": "beam_channel",       # Channeling Cleric
    "K20": "melee_strike",       # Holy Knight / Hammerdin
    "K21": "ground_targeted_circle", # Ritual Mage / Oracle
    "K22": "circle",             # Storm Caller / Druid
    "K23": "melee_strike",       # Monk (quarterstaff)
    "K24": "totem",              # Druid Beastmaster
    "K25": "totem",              # Witch Doctor Petmaster
    "K26": "aura",               # Blood Mage / Martyr (self-harm aura)
    "K27": "aura",               # Thorns / Vengeance Knight
    "K28": "melee_strike",       # Builder-Spender Warrior
    "K29": "totem",              # Necromantic Blood Mage
    "H1":  "ring",               # Orbital Guard
    "H2":  "whirlwind",          # Blade Vortex
    "H3":  "totem",              # Storm Brand caster
    "H4":  "circle",             # Orbital Bombardier
    "H5":  "melee_strike",       # True Battlemage
    "H6":  "ground_targeted_circle", # Charge-up Caster
    "B4":  "line",               # Bone-Wall Necromancer
    "B5":  "teleport",           # Teleport Sorceress (UNMAPPED)
    "B6":  "dash_attack",        # Dash-Weaver Martial
    "B7":  "ring",               # Ring of Shields
    "B8":  "ring",               # Nested-Orbit Epicycle
    "B9":  "circle",             # Collapse-Bomb Caster
    "B10": "whirlwind",          # Vaal Blade Vortex
    "B11": "totem",              # Inversion Summoner
    "B12": "whirlwind",          # Spin-to-Win
}

def assign_roster(roster_kits, plane="A"):
    """Assign roster kits to plane cells. Returns list of (bucket, kit_id, kit_name)."""
    assignments = []
    for kit in roster_kits:
        kid = kit["kit_id"]
        name = kit["name"] or kid
        commit = roster_commit(kit)
        geo = ROSTER_GEO_HINTS.get(kid)

        if plane == "A":
            if geo is None:
                assignments.append(("UNMAPPED", kid, name))
                continue
            family, _, _ = geo_to_plane_a(geo)
            if family == "UNMAPPED":
                assignments.append(("UNMAPPED", kid, name))
                continue
            if commit is None:
                # Place without commit dimension — use all rows or mark TBD
                assignments.append(("COMMIT_UNKNOWN", kid, name))
                continue
            row = commit
            if row not in PLANE_A_ROWS:
                assignments.append(("UNMAPPED", kid, name))
                continue
            assignments.append(((row, family), kid, name))
        else:  # Plane B
            # Map commit to row
            row_b = None
            for r, c in PLANE_B_ROW_TO_COMMIT.items():
                if commit == c:
                    row_b = r
                    break

            if geo is None:
                assignments.append(("UNMAPPED", kid, name))
                continue
            b_cols = geo_to_plane_b_cols(geo)
            if b_cols == ["UNMAPPED"]:
                assignments.append(("UNMAPPED", kid, name))
                continue
            if row_b is None:
                assignments.append(("COMMIT_UNKNOWN", kid, name))
                continue
            bucket = (row_b, b_cols[0])
            assignments.append((bucket, kid, name))

    return assignments

# ── Jitter within cell ────────────────────────────────────────────────────────
def jitter_points(n, cx, cy, cell_w, cell_h, margin=0.12, seed=42):
    """Return (x, y) arrays for n jittered points inside a cell."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(cx - cell_w*(0.5-margin), cx + cell_w*(0.5-margin), n)
    ys = rng.uniform(cy - cell_h*(0.5-margin), cy + cell_h*(0.5-margin), n)
    return xs, ys

# ── Plot one plane ────────────────────────────────────────────────────────────
def plot_plane(ax, rows, cols, col_labels, row_labels, cells,
               roster_assignments, title, nrows, ncols):
    """Draw one plane onto ax."""

    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows + 0.8)  # extra space for col headers
    ax.set_aspect('equal')
    ax.axis('off')

    cell_w = 1.0
    cell_h = 1.0

    COLORS = {
        "corpus_ghost": "#B0B8C4",
        "mint":         "#FFD700",
        "roster_kits":  "#4CA3FF",
        "negative":     "#FF6B6B",
        "cell_bg":      "#1A1F27",
        "cell_border":  "#334055",
        "cell_empty":   "#111520",
        "cell_empty_border": "#223",
    }

    # Title
    ax.text(ncols/2, nrows + 0.65, title, ha='center', va='top',
            fontsize=11, fontweight='bold', color='white',
            transform=ax.transData)

    # Column headers
    for ci, lbl in enumerate(col_labels):
        ax.text(ci + 0.5, nrows + 0.32, lbl, ha='center', va='center',
                fontsize=6.5, color='#9AA3AD', fontweight='bold')

    # Row headers
    for ri, lbl in enumerate(row_labels):
        row_val = rows[ri]
        ax.text(-0.18, nrows - ri - 0.5, lbl, ha='right', va='center',
                fontsize=6.5, color='#9AA3AD', fontweight='bold', rotation=0)

    # Draw cells
    for ri, row_val in enumerate(rows):
        for ci, col_val in enumerate(cols):
            bucket = (row_val, col_val)
            cell_data = cells.get(bucket, {"corpus": [], "mint": [], "negative": [], "unmapped": []})

            corpus_in  = cell_data.get("corpus", [])
            mint_in    = cell_data.get("mint", [])
            total = len(corpus_in) + len(mint_in)

            cx = ci + 0.5
            cy = nrows - ri - 0.5

            # Background
            bg_color = COLORS["cell_bg"] if total > 0 else COLORS["cell_empty"]
            brd_color = COLORS["cell_border"] if total > 0 else COLORS["cell_empty_border"]
            rect = FancyBboxPatch((ci + 0.04, nrows - ri - 0.04 - cell_h + 0.08),
                                   cell_w - 0.08, cell_h - 0.08,
                                   boxstyle="round,pad=0.02",
                                   linewidth=0.8,
                                   edgecolor=brd_color,
                                   facecolor=bg_color)
            ax.add_patch(rect)

            # Corpus ghost dots (jittered)
            if corpus_in:
                xs, ys = jitter_points(len(corpus_in), cx, cy, cell_w*0.78, cell_h*0.55,
                                        seed=ri*100+ci)
                ax.scatter(xs, ys, s=3, color=COLORS["corpus_ghost"], alpha=0.35,
                           linewidths=0, zorder=2)

            # Mint dots (star marker)
            if mint_in:
                mxs, mys = jitter_points(len(mint_in), cx, cy, cell_w*0.6, cell_h*0.4,
                                          seed=ri*100+ci+500)
                ax.scatter(mxs, mys, s=28, marker='*', color=COLORS["mint"],
                           alpha=0.9, linewidths=0, zorder=4)

            # Count annotation
            if total > 0:
                ax.text(ci + cell_w - 0.07, nrows - ri - cell_h + 0.1,
                        str(total), ha='right', va='bottom',
                        fontsize=5.5, color='#6B8099', zorder=5)

    # Roster kit markers (colored dots with K-number labels)
    for bucket, kid, name in roster_assignments:
        if bucket in ("UNMAPPED", "COMMIT_UNKNOWN"):
            continue  # handled below

        # Find col/row index
        if not isinstance(bucket, tuple) or len(bucket) != 2:
            continue
        row_val, col_val = bucket
        if row_val not in rows or col_val not in cols:
            continue
        ri = rows.index(row_val)
        ci = cols.index(col_val)

        cx = ci + 0.5
        cy = nrows - ri - 0.5

        # Deterministic jitter by kid hash
        h = hash(kid) % 10000
        rng = np.random.default_rng(h)
        ox = rng.uniform(-0.3, 0.3)
        oy = rng.uniform(-0.22, 0.22)

        ax.scatter([cx + ox], [cy + oy], s=22, color=COLORS["roster_kits"],
                   alpha=0.95, linewidths=0.5, edgecolors='white', zorder=6)
        ax.text(cx + ox, cy + oy + 0.13, kid,
                ha='center', va='bottom', fontsize=4.2, color='white',
                fontweight='bold', zorder=7)

    # UNMAPPED strip below main grid (if any unmapped kits exist)
    unmapped_corpus = cells.get("UNMAPPED", {}).get("corpus", [])
    unmapped_neg    = cells.get("UNMAPPED", {}).get("negative", [])
    unmapped_roster = [b for b, kid, name in roster_assignments
                       if b in ("UNMAPPED", "COMMIT_UNKNOWN")]

    if unmapped_corpus or unmapped_neg or unmapped_roster:
        strip_y = -0.55
        ax.text(0, strip_y + 0.18,
                f"UNMAPPED: {len(unmapped_corpus)} corpus · {len(unmapped_neg)} negatives · "
                f"{len(unmapped_roster)} roster",
                ha='left', va='center', fontsize=5.5, color='#FF9966', zorder=5)

    # Negative kits: pale X strip note
    if unmapped_neg:
        ax.text(0, strip_y - 0.05,
                f"  Negatives (✗ warning flags, NOT candidates): "
                + ", ".join(k["kit_id"] for k in unmapped_neg[:8])
                + ("..." if len(unmapped_neg) > 8 else ""),
                ha='left', va='center', fontsize=4.5, color='#FF6B6B', zorder=5)


# ── Main render ───────────────────────────────────────────────────────────────
def main():
    random.seed(0)
    np.random.seed(0)

    print("Loading data from DB...")
    corpus_kits, negative_kits, roster_kits = load_data()
    print(f"  corpus combat kits: {len(corpus_kits)}")
    print(f"  negative kits: {len(negative_kits)}")
    print(f"  roster kits: {len(roster_kits)}")

    # Assign cells
    cells_a = assign_plane_a(corpus_kits, negative_kits, roster_kits)
    cells_b = assign_plane_b(corpus_kits, negative_kits, roster_kits)
    roster_a = assign_roster(roster_kits, plane="A")
    roster_b = assign_roster(roster_kits, plane="B")

    # ── Figure ──────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(24, 12), facecolor='#0B0D10')
    fig.patch.set_facecolor('#0B0D10')

    # Main title
    fig.text(0.5, 0.97,
             "V1 PLANE VIEW — Q19 PLANE-LOCK DECISION INSTRUMENT",
             ha='center', fontsize=14, fontweight='bold', color='white')
    fig.text(0.5, 0.945,
             "ARCHIVE-GRAIN · geometry family (Axis 2, BC-MEASURED R-3) × commitment class (ninth archive axis, Q-E4-4b)\n"
             "corpus = projected/keyed (ghost dots) · roster = engine-sourced (solid blue ●) · mint = star ★",
             ha='center', fontsize=8, color='#9AA3AD')

    # Legend
    legend_elements = [
        mpatches.Patch(color='#B0B8C4', alpha=0.5, label='Corpus combat kit (463 total, ghost dot)'),
        plt.Line2D([0],[0], marker='*', color='w', markerfacecolor='#FFD700',
                   markersize=9, linewidth=0, label='Mint kit (9 total, ★)'),
        plt.Line2D([0],[0], marker='o', color='w', markerfacecolor='#4CA3FF',
                   markersize=7, linewidth=0, label='Engine roster kit (45 total, labeled)'),
        mpatches.Patch(color='#FF6B6B', alpha=0.5, label='Negative kit (37 total, ✗ — UNMAPPED strip only)'),
        mpatches.Patch(facecolor='#1A1F27', edgecolor='#334055',
                       label='Occupied cell (has corpus or mint kits)'),
        mpatches.Patch(facecolor='#111520', edgecolor='#111833',
                       label='Empty cell (frontier — gap is the point)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3,
               fontsize=7, facecolor='#11161C', edgecolor='#334055',
               labelcolor='white', framealpha=0.9,
               bbox_to_anchor=(0.5, 0.01))

    # ── PLANE A ─────────────────────────────────────────────────────────────
    ax_a = fig.add_axes([0.04, 0.13, 0.42, 0.78])
    ax_a.set_facecolor('#0B0D10')

    plot_plane(ax_a,
               rows=PLANE_A_ROWS,
               cols=PLANE_A_COLS,
               col_labels=PLANE_A_COL_LABELS,
               row_labels=PLANE_A_ROW_LABELS,
               cells=cells_a,
               roster_assignments=roster_a,
               title="PLANE A — SPEC (15 cells: 3 commitment × 5 dispersion families)",
               nrows=3, ncols=5)

    # ── PLANE B ─────────────────────────────────────────────────────────────
    ax_b = fig.add_axes([0.53, 0.13, 0.46, 0.78])
    ax_b.set_facecolor('#0B0D10')

    plot_plane(ax_b,
               rows=PLANE_B_ROWS,
               cols=PLANE_B_COLS,
               col_labels=PLANE_B_COLS,
               row_labels=PLANE_B_ROWS,
               cells=cells_b,
               roster_assignments=roster_b,
               title="PLANE B — MATT'S MOCK (24 cells: 3 commitment × 8 delivery-family columns)",
               nrows=3, ncols=8)

    # Divider
    fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.95],
                               transform=fig.transFigure,
                               color='#334055', linewidth=1.5, linestyle='--'))

    # Grain legend footer
    fig.text(0.5, 0.072,
             "GRAIN: ~972 L0 coordinates live INSIDE cells as isotope sub-dots — not the plane. "
             "Search space of record: L4 ≈ 1.284×10⁹ = 204,120 × 16 × 393. "
             "Negatives are NOT candidates — rendered in UNMAPPED strip only.",
             ha='center', fontsize=6.5, color='#5A6470')

    # Save PNG
    png_path = OUT_DIR / "plane_view_v1.png"
    fig.savefig(str(png_path), dpi=150, bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"Saved PNG: {png_path}")

    # Save SVG
    svg_path = OUT_DIR / "plane_view_v1.svg"
    fig.savefig(str(svg_path), format='svg', bbox_inches='tight',
                facecolor='#0B0D10', edgecolor='none')
    print(f"Saved SVG: {svg_path}")

    plt.close(fig)

    # ── Return stats for use by stats script ─────────────────────────────────
    return cells_a, cells_b, roster_a, roster_b, corpus_kits, negative_kits, roster_kits

if __name__ == "__main__":
    main()
