#!/usr/bin/env python3
"""
ghost_field_edition3.py — the atlas.json ghost_field block v3 (EDITION III).
==========================================================================
Edition III is a CENSUS-POPULATION edition: the Edition-III one-batch curated +65 corpus rows
(Stage A pull-7 re-insertion + Stage B Lost Ark 58 at class-engraving grain). Those rows use ONLY
existing coordinate values -> the LATTICE does not move (register v1.3: denominators byte-identical
to v1.2). The FROZEN Edition-I FIT layer is UNTOUCHED (14-dim basis, 506 point coords, tombstones,
axis names, RIDER-1, F-1). This module re-emits the ghost field + drill-in + denominators against
register v1.3, with the LIT census read LIVE from the post-batch corpus.db.

Author: elrond (data steward). TOOL script (curation/enumeration), not engine code.
Imported by build_atlas_json_edition3.py. Logged in research/curated/MIGRATION.md.

WHAT CHANGES vs ghost_field_edition2 (census-only; lattice + basis untouched):
  1. Version/register stamps -> v3 / feasibility-cuts-register-v1.3.
  2. The LIT census grows (read live): occupied meso 193 -> 202 (+9); pull-lit 2 -> 4 (+2). The
     denominators (exact 767,411,820 / meso 11,160 / sealed 1,314 / pull 1,080+54) are IDENTICAL
     to Edition-II (the lattice did not move — denominator law).
  3. off_plane_corpus + unmapped grow by the documented MELEE-collapse (delivery=melee has no meso
     ghost image: 4 skill-grain Destroyer + di-cyclone-strike-monk-base) + 1 honest-NULL movement
     (d4-spiritborn-vortex, source-silent). All documented; none are keying errors.

FROZEN-BASIS DISCIPLINE (unchanged from Edition-I/II): new rows PROJECT into the frozen basis via
  the SAME CA supplementary transition formula (pull/silence/hybrid/MELEE/SUMMON masked-like — no
  fit column, cannot bend an axis). The basis is NOT re-derived at an edition increment (charter
  §6). The fit reconstructs from the durable pre-C3 snapshot atlas-frozen-fit-cellkeys-edition1.csv;
  lighting uses the LIVE (post-Edition-III) corpus.db keys at emission time.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghost_field_edition2 as gf2

# Reuse ALL of Edition-II's lattice machinery verbatim (the lattice is unchanged at Edition-III).
# We re-export the pieces build_atlas_json_edition3 needs, changing only the STAMPS + wrapping
# build_ghost_field to re-stamp the emitted block as Edition-III / register v1.3.

CK_IDX = gf2.CK_IDX
CORE = gf2.CORE
REG = gf2.REG
lit_map = gf2.lit_map
meso_feasible = gf2.meso_feasible
fit2reg_direct2 = gf2.fit2reg_direct2

GHOST_FIELD_VERSION = "3.0"
REGISTER_REF = "feasibility-cuts-register-v1.3"

# Edition-III denominators are IDENTICAL to Edition-II (lattice unchanged). Re-asserted, not
# superseded (register v1.3 §0). We import them from gf2 to keep a single source.
EXACT_POST_RED_LAW = gf2.EXACT_POST_RED_LAW  # 767,411,820


def build_ghost_field(db_conn, atlas_points=None):
    """Edition-III ghost field = Edition-II ghost field re-run against the LIVE post-batch census,
    re-stamped Edition-III / register v1.3. The lattice, projection, drill-in, and denominators are
    Edition-II's (unchanged); only the LIT census (read live from db_conn) grows."""
    ghost = gf2.build_ghost_field(db_conn, atlas_points=atlas_points)
    # re-stamp for Edition-III (the lattice is unchanged; the census is the delta)
    ghost["version"] = GHOST_FIELD_VERSION
    ghost["register_ref"] = REGISTER_REF
    ghost["edition"] = "III"
    ghost["edition3_change"] = (
        "CENSUS-POPULATION edition: +65 corpus rows (Stage A pull-7 re-insertion + Stage B Lost "
        "Ark 58 at class-engraving grain). Lattice UNCHANGED (register v1.3 denominators "
        "byte-identical to v1.2); FIT basis frozen. Lit occupancy grew: occupied meso 193->202, "
        "pull-lit 2->4. New rows PROJECT into the frozen basis (no basis re-derivation).")
    ghost["denominators"]["register_v1_3_note"] = (
        "denominators byte-identical to Edition-II (lattice did not move; LA class-kits add no "
        "coordinate value). v1.2 numbers RE-ASSERTED, not superseded.")
    # carry the register_ref through the pull_slice + denominators sub-blocks for grep-legibility
    return ghost
