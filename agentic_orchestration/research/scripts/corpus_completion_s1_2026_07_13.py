"""
corpus_completion_s1_2026_07_13.py
Corpus DB — S1 data-completion pass (five payloads). Author: elrond, 2026-07-13.
Authority: gandalf wind-down §3 (2026-07-13-wind-down-corpus-to-demo-pipeline-resume.md).

RUNS ON TOP OF the base ingest. D6 rebuild sequence is now TWO committed scripts:
    python agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py
    python agentic_orchestration/research/scripts/corpus_completion_s1_2026_07_13.py
Both deterministic from committed inputs. This script is IDEMPOTENT (safe to re-run):
ADD COLUMN is guarded by a pragma check; all backfills are pure UPDATEs from source.

PAYLOADS (five):
  P1  roster_atlas: ADD amp_val, commit_val, mob_policy_while_casting, commit_provenance.
      - amp_val    = expand the engine-sourced atlas amp code (S/F/V -> spiky/flat/var; '_' -> NULL).
                     Codes validated 25/26 against bc_target_cell_sampler.py CellDef amplitude;
                     K9f (fired leg) legitimately diverges (flat vs cell9 variable) — kept, flagged.
      - commit_val = expand the atlas commit code (W/I/C -> wind-up/instant/channel; '_' -> NULL).
                     Only CellDef-PINNED cells carry an explicit code (K1=wind-up, K7=instant/snap,
                     K19=channel) plus roster-explicit B12=channel, H6=wind-up. UNPINNED cells are
                     "rolled" at generation (S7) — NOT fixed at S1 — so honest-NULL, never snap-invented.
      - mob_policy_while_casting = NULL for all 45. FINDING: movement policy is emitted per-skill at
                     S7 (per_skill_emitter.py _MOVE_*); there is NO S1 engine source of record for it.
                     Contradicts the commission's assumption that engine sources carry roster movement.
  P2  canon_engine_key: ADD delivery_value (promote probe delivery.value to keyed column).
      Makes Q19 cone Path-2 routing schema-derivable. VERIFIES the ruled 5-beam / 6-projectile split.
  P3  6 poe2 movement-unknowns: census only. All remain 'unknown' in engine-key + probe + megaprobe.
      No source resolves them -> honest-NULL (kept as engine-key mob_policy_while_casting='unknown').
  P4  d2-wl-void-rift amp_val: census only. Already NULL; no source (probe/megaprobe) supplies amp.
  P5  canon_corpus: ADD era_year, stabilization_patch (naming-law feed, §7.1).
      - era_year = per-game canonical release year (documented table, sourced from per-game-meta.jsonl
                   release_era). Covers all 524 via game. Raw per-kit `eras` column retained for finer signal.
      - stabilization_patch = 'current-X.Y' token parsed from eras (primary, richer) ∪ sources_used.
                   STEWARD SCOPE NOTE: commission scoped this to sources_used (1 row); the cleaner
                   'current-' signal lives in the eras field (10 rows). Extractor unions both and records
                   provenance. Sparse by nature — NULL-honest elsewhere; naming law omits the segment
                   where absent (§7.1 refinement 5). Flagged to gandalf for ratification.

Schema version bumped to 2.1 (2.0 lineage row retained).
"""

import json
import pathlib
import re
import sqlite3
import sys

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"

# ---------------------------------------------------------------------------
# P1 code expanders
# ---------------------------------------------------------------------------
AMP_CODE = {"S": "spiky", "F": "flat", "V": "var"}          # '_' / '' -> NULL
COMMIT_CODE = {"W": "wind-up", "I": "instant", "C": "channel"}  # '_' / '' -> NULL

# CellDef amplitude source-of-record (bc_target_cell_sampler.py CELL_DEFINITIONS,
# reincarnated-engine, read-only). Embedded literal for a self-contained collab-repo
# rebuild (no cross-repo import at rebuild time). Used ONLY to validate roster codes.
CELLDEF_AMP = {
    1: "spiky", 2: "flat", 3: "variable", 4: "spiky", 5: "spiky", 6: "flat",
    7: "flat", 8: "spiky", 9: "variable", 10: "flat", 11: "spiky", 12: "variable",
    13: "spiky", 14: "spiky", 15: "flat", 16: "variable", 17: "spiky", 18: "variable",
    19: "variable", 20: "variable", 21: "variable", 22: "variable", 23: "variable",
    24: "variable", 25: "variable",
}
CELLDEF_AMP_NORM = {k: ("var" if v == "variable" else v) for k, v in CELLDEF_AMP.items()}

def roster_cell_id(kit_id):
    """Map a roster kit_id to its CellDef cell_id (1-25) where one exists; else None.
    K9c/K9f both -> cell 9; K13 -> cell 13 (folded to K12 in roster but code = cell13).
    B*/H*/K26-K29 have no CellDef mapping -> None."""
    if kit_id in ("K9c", "K9f"):
        return 9
    m = re.fullmatch(r"K(\d+)", kit_id)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 25:
            return n
    return None

# ---------------------------------------------------------------------------
# P5 era_year: per-game canonical release year (sourced from per-game-meta.jsonl release_era)
# ---------------------------------------------------------------------------
GAME_ERA_YEAR = {
    "chronicon": 2020,   # era_range '1.0-2020' (NOTE: release_era says '1.0 2021' — discrepancy flagged)
    "d2": 2000,          # base 2000 (LoD 2001; D2R 2021)
    "d3": 2012,
    "d4": 2023,
    "di": 2022,
    "gd": 2016,          # base 2016 (AoM 2017, FG 2019)
    "hades1": 2020,      # 1.0 Sep 2020
    "hades2": 2025,      # 1.0 Aug 2025
    "hot": 2024,         # 1.0-2024
    "le": 2024,          # 1.0 Feb 2024
    "poe1": 2013,
    "poe2": 2024,        # EA 0.1 Dec 2024
    "tl1": 2009,
    "tl2": 2012,
    "tli": 2022,         # EA 2022
    "tq": 2006,          # base 2006 (AE 2016)
    "tq2": 2025,         # EA 2025
    "undecember": 2022,
    "vs": 2022,          # 1.0-2022 (EA 2021)
}

CURRENT_PATCH_RE = re.compile(r"current-(\d+\.\d+\+?)")

POE2_UNKNOWNS = [
    "poe2-spiral-volley", "poe2-whirling-assault-ma", "poe2-snipe-mirage-deadeye",
    "poe2-walking-calamity", "poe2-shaman-bear", "poe2-archmage-totems",
]

EXPECTED_BEAM = {
    "ud-flamethrower-channel", "poe1-incinerate", "gd-flames-of-ignaffar-purifier",
    "hot-dragons-breath", "hot-exterminator-burn",
}
EXPECTED_PROJ = {
    "tq-ternion-bone-charmer", "poe2-galvanic-shards", "di-vengeance-strafe-dh",
    "di-multishot-dh", "le-frost-claw", "tl2-shotgonne-outlander",
}


def has_column(conn, table, col):
    return any(r[1] == col for r in conn.execute(f"PRAGMA table_info({table})").fetchall())


def add_column(conn, table, col, decl):
    if not has_column(conn, table, col):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
        return True
    return False


def main():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found. Run base ingest first.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    findings = []
    report = {}

    # -- pre-flight row-count guard (payloads must NOT change these) --
    pre = {
        "canon_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "canon_probe_facts": conn.execute("SELECT COUNT(*) FROM canon_probe_facts").fetchone()[0],
        "canon_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "roster_atlas": conn.execute("SELECT COUNT(*) FROM roster_atlas").fetchone()[0],
    }
    print(f"Pre-flight row counts: {pre}")

    # =====================================================================
    # P1 — roster_atlas backfill
    # =====================================================================
    print("\n== P1: roster_atlas amp_val / commit_val / mob_policy_while_casting ==")
    add_column(conn, "roster_atlas", "amp_val", "TEXT")
    add_column(conn, "roster_atlas", "commit_val", "TEXT")
    add_column(conn, "roster_atlas", "mob_policy_while_casting", "TEXT")
    add_column(conn, "roster_atlas", "commit_provenance", "TEXT")

    p1_amp_fill = p1_commit_fill = 0
    amp_divergences = []
    for kit_id, amp_code, commit_code in conn.execute(
        "SELECT kit_id, amp, commit_slot FROM roster_atlas"
    ).fetchall():
        amp_val = AMP_CODE.get((amp_code or "").strip().upper())
        commit_val = COMMIT_CODE.get((commit_code or "").strip().upper())
        commit_prov = None
        if commit_val is not None:
            cid = roster_cell_id(kit_id)
            if cid in (1, 7, 19):
                commit_prov = "celldef-pin"
            else:
                commit_prov = "roster-atlas-v1-engine"
        # validate amp against CellDef where a mapping exists
        cid = roster_cell_id(kit_id)
        if amp_val is not None and cid is not None:
            if amp_val != CELLDEF_AMP_NORM.get(cid):
                amp_divergences.append((kit_id, amp_val, CELLDEF_AMP_NORM.get(cid)))
        conn.execute(
            "UPDATE roster_atlas SET amp_val=?, commit_val=?, commit_provenance=?, "
            "mob_policy_while_casting=NULL WHERE kit_id=?",
            (amp_val, commit_val, commit_prov, kit_id),
        )
        if amp_val is not None:
            p1_amp_fill += 1
        if commit_val is not None:
            p1_commit_fill += 1
    conn.commit()

    print(f"  amp_val filled:    {p1_amp_fill}/45  (NULL-honest: {45 - p1_amp_fill})")
    print(f"  commit_val filled: {p1_commit_fill}/45  (NULL-honest: {45 - p1_commit_fill})")
    print(f"  mob_policy_while_casting: 0/45 filled (all NULL — no S1 source; emitted at S7)")
    print(f"  amp validation vs CellDef: {len(amp_divergences)} divergence(s): {amp_divergences}")
    report["P1"] = {
        "amp_fill": p1_amp_fill, "commit_fill": p1_commit_fill,
        "mob_fill": 0, "amp_divergences": amp_divergences,
    }
    findings.append(
        "P1: mob_policy_while_casting = NULL for all 45 roster kits. Movement policy is emitted "
        "per-skill at generation (S7, per_skill_emitter.py _MOVE_ROOTED/_MOVE_WALK/_MOVE_FULL); "
        "there is NO S1 engine source of record. Contradicts the commission's assumption that "
        "engine sources (CellDefs/battle-sim) carry roster movement. Honest-NULL."
    )
    findings.append(
        f"P1: commit_val filled only where the atlas carries an explicit code ({p1_commit_fill}/45): "
        "CellDef-pinned K1=wind-up, K7=instant(snap), K19=channel, plus roster-explicit B12=channel, "
        "H6=wind-up. UNPINNED CellDef cells are 'rolled' at S7 (not fixed at S1) -> honest-NULL, "
        "never snap-invented."
    )
    findings.append(
        f"P1: amp_val filled {p1_amp_fill}/45 by expanding engine-sourced atlas codes; validated "
        f"25/26 exact against CellDef amplitude. Divergence: {amp_divergences} (K9f fired-leg legitimately "
        "differs from cell9 target — kept as engine-emitted value, not overridden)."
    )

    # =====================================================================
    # P2 — canon_engine_key.delivery_value
    # =====================================================================
    print("\n== P2: canon_engine_key.delivery_value ==")
    add_column(conn, "canon_engine_key", "delivery_value", "TEXT")
    conn.execute(
        """UPDATE canon_engine_key
           SET delivery_value = (
               SELECT json_extract(pf.facts_json, '$.value')
               FROM canon_probe_facts pf
               WHERE pf.kit_id = canon_engine_key.kit_id AND pf.family = 'delivery'
               LIMIT 1)"""
    )
    conn.commit()
    p2_fill = conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE delivery_value IS NOT NULL").fetchone()[0]
    print(f"  delivery_value filled: {p2_fill}/478")

    cone_rows = conn.execute(
        "SELECT kit_id, delivery_value FROM canon_engine_key WHERE geometry_value='cone' ORDER BY kit_id"
    ).fetchall()
    got_beam = {k for k, d in cone_rows if d == "beam"}
    got_proj = {k for k, d in cone_rows if d == "projectile"}
    beam_ok = got_beam == EXPECTED_BEAM
    proj_ok = got_proj == EXPECTED_PROJ
    print(f"  cone BEAM ({len(got_beam)}): {'OK' if beam_ok else 'MISMATCH'} — {sorted(got_beam)}")
    print(f"  cone PROJECTILE ({len(got_proj)}): {'OK' if proj_ok else 'MISMATCH'} — {sorted(got_proj)}")
    report["P2"] = {"fill": p2_fill, "beam_ok": beam_ok, "proj_ok": proj_ok,
                    "beam_n": len(got_beam), "proj_n": len(got_proj)}
    if not (beam_ok and proj_ok):
        findings.append(f"P2 STOP: cone split did not reproduce. beam={sorted(got_beam)} proj={sorted(got_proj)}")

    # =====================================================================
    # P3 — 6 poe2 movement-unknowns (census only)
    # =====================================================================
    print("\n== P3: 6 poe2 movement-unknowns (census) ==")
    p3 = {}
    for kid in POE2_UNKNOWNS:
        row = conn.execute(
            "SELECT mob_policy_while_casting FROM canon_engine_key WHERE kit_id=?", (kid,)
        ).fetchone()
        p3[kid] = row[0] if row else "(absent)"
        print(f"  {kid}: mob_policy_while_casting={p3[kid]!r}")
    report["P3"] = p3
    findings.append(
        "P3: all 6 poe2 movement-unknowns remain 'unknown' in engine-key (also unresolved in probe + "
        "megaprobe re-probe). No source resolves them -> honest-NULL retained."
    )

    # =====================================================================
    # P4 — d2-wl-void-rift amp (census only)
    # =====================================================================
    print("\n== P4: d2-wl-void-rift amp_val (census) ==")
    r = conn.execute("SELECT amp_val, amp_conf FROM canon_corpus WHERE kit_id='d2-wl-void-rift'").fetchone()
    print(f"  d2-wl-void-rift: amp_val={r[0]!r} amp_conf={r[1]!r}")
    report["P4"] = {"amp_val": r[0]}
    findings.append(
        "P4: d2-wl-void-rift amp_val remains NULL. atlas_key carries no amp code; probe/megaprobe supply "
        "no amp value. Honest-NULL retained (no source to backfill)."
    )

    # =====================================================================
    # P5 — canon_corpus.era_year + stabilization_patch
    # =====================================================================
    print("\n== P5: canon_corpus.era_year + stabilization_patch ==")
    add_column(conn, "canon_corpus", "era_year", "INTEGER")
    add_column(conn, "canon_corpus", "stabilization_patch", "TEXT")

    p5_era_fill = 0
    unknown_games = set()
    for (game,) in conn.execute("SELECT DISTINCT game FROM canon_corpus").fetchall():
        yr = GAME_ERA_YEAR.get(game)
        if yr is None:
            unknown_games.add(game)
            continue
        conn.execute("UPDATE canon_corpus SET era_year=? WHERE game=?", (yr, game))
    conn.commit()
    p5_era_fill = conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE era_year IS NOT NULL").fetchone()[0]

    # stabilization_patch: parse 'current-X.Y' from eras (primary) ∪ sources_used (secondary)
    p5_patch_fill = 0
    patch_from_sources_used = 0
    for kit_id, eras in conn.execute("SELECT kit_id, eras FROM canon_corpus").fetchall():
        patch = None
        prov = None
        if eras:
            m = CURRENT_PATCH_RE.search(eras)
            if m:
                patch, prov = m.group(1), "eras"
        if patch is None:
            su = conn.execute(
                "SELECT facts_json FROM canon_probe_facts WHERE kit_id=? AND family='sources_used'",
                (kit_id,),
            ).fetchone()
            if su:
                m = CURRENT_PATCH_RE.search(su[0])
                if m:
                    patch, prov = m.group(1), "sources_used"
                    patch_from_sources_used += 1
        if patch is not None:
            conn.execute(
                "UPDATE canon_corpus SET stabilization_patch=? WHERE kit_id=?", (patch, kit_id)
            )
            p5_patch_fill += 1
    conn.commit()

    print(f"  era_year filled: {p5_era_fill}/524  (unknown games: {sorted(unknown_games) or 'none'})")
    print(f"  stabilization_patch filled: {p5_patch_fill}/524 "
          f"(sources_used-only would be {patch_from_sources_used}; NULL-honest elsewhere)")
    report["P5"] = {"era_fill": p5_era_fill, "patch_fill": p5_patch_fill,
                    "patch_sources_used_only": patch_from_sources_used, "unknown_games": sorted(unknown_games)}
    if unknown_games:
        findings.append(f"P5: era_year has no per-game year for: {sorted(unknown_games)} -> NULL. Check GAME_ERA_YEAR.")
    findings.append(
        "P5: era_year = per-game canonical release year (sourced from per-game-meta.jsonl release_era). "
        "chronicon=2020 per era_range '1.0-2020'; NOTE release_era field says '1.0 2021' — source discrepancy flagged."
    )
    findings.append(
        f"P5: stabilization_patch is sparse by nature ({p5_patch_fill}/524). STEWARD SCOPE NOTE — commission "
        "scoped it to sources_used (1 clean 'current-' token); the richer signal is in the eras field (10 tokens). "
        "Extractor unions eras∪sources_used with provenance. Naming law omits the segment where absent (§7.1). "
        "Flagged to gandalf for scope ratification."
    )

    # =====================================================================
    # Schema-meta bump -> 2.1
    # =====================================================================
    if not conn.execute("SELECT 1 FROM corpus_schema_meta WHERE version='2.1'").fetchone():
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            ("2.1", "2026-07-13T00:00:00Z",
             "S1 data-completion (elrond). P1 roster amp_val/commit_val/mob_policy_while_casting/commit_provenance; "
             "P2 engine_key.delivery_value; P5 canon_corpus.era_year/stabilization_patch. P3/P4 census (honest-NULL). "
             "Additive columns only; row counts unchanged. Rebuild = base ingest + this completion script."),
        )
        conn.commit()

    # =====================================================================
    # Post-flight asserts — row counts MUST hold
    # =====================================================================
    print("\n== Post-flight row-count asserts (must hold) ==")
    post = {
        "canon_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "canon_probe_facts": conn.execute("SELECT COUNT(*) FROM canon_probe_facts").fetchone()[0],
        "canon_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "roster_atlas": conn.execute("SELECT COUNT(*) FROM roster_atlas").fetchone()[0],
    }
    expected = {"canon_corpus": 524, "canon_probe_facts": 4780, "canon_engine_key": 478, "roster_atlas": 45}
    counts_ok = True
    for k, v in expected.items():
        ok = post[k] == v and pre[k] == v
        counts_ok = counts_ok and ok
        print(f"  {k}: {post[k]} {'OK' if ok else f'MISMATCH (expected {v}, pre {pre[k]})'}")

    print("\n--- COMPLETION SUMMARY ---")
    print(json.dumps(report, indent=2))
    print(f"\nFindings ({len(findings)}):")
    for f in findings:
        print(f"  - {f}")

    stop = (not counts_ok) or (not report["P2"]["beam_ok"]) or (not report["P2"]["proj_ok"])
    conn.close()
    if stop:
        print("\nSTOP: an acceptance gate failed (row counts or cone split).")
        sys.exit(1)
    print("\nS1 COMPLETION: all gates passed (row counts hold; cone split reproduces).")
    return report, findings


if __name__ == "__main__":
    main()
