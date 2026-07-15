#!/usr/bin/env python3
"""
corpus_ingest_pull_tranche_2026_07_15.py  — EDITION-II STAGE 1

Ingest + key the pull-intrinsic class-kit tranche (legolas b7f773d3) into corpus.db.
Matt authorized the Edition-II chain 2026-07-15 ("If the slate holds, cut Edition-II §10").
This is the FIRST ingestion under the Edition-II pull vocabulary. elrond OWNS the DB write.

READ FIRST:
  - research/knowledge/mcd-pull-mechanic/2026-07-15-pull-intrinsic-classkit-tranche.md (TABLES = truth)
  - research/curated/hybrid-assignment-criteria-2026-07-15.md (STAGE 0 memo — the treatment verdicts)
  - gandalf renderer spec §10 (Edition-II) + treatment=hybrid taxonomy line (3f20f738)

SCOPE OF THIS SCRIPT (Stage 1 only — new rows + enrichment; NO survivor re-keys):
  NEW ROWS (7):
    la-destroyer-vortex-gravity     la-destroyer-gravity-impact
    la-destroyer-gravity-force      la-destroyer-gravity-compression
    d4-spiritborn-vortex            d3-wizard-black-hole
    di-cyclone-strike-monk-base
  ENRICHMENT (existing rows — mech_note/provenance facts, NO cell_key change here):
    di-cyclone-monk-pvp   d3-zbarb          (re-keys happen in STAGE 3, separate script)

GANDALF'S FIVE FLAGS (binding) — dispositions baked in:
  (a) la-destroyer-gravity-compression: pull is INFERRED. Re-verified from source
      (fextralife 2026-07-15): base skill + ALL tripods describe damage/black-hole/stagger,
      NO explicit pull/draw on living enemies. Never-invent governs -> function=NONE, NO
      pull key, pull_pending_vocab=0, annotated pull-implicit.
  (b) treatment=hybrid on la-destroyer-vortex-gravity + di-cyclone-strike-monk-base is
      PROPOSED. STAGE-0 criteria run -> BOTH resolve to damage-primary + pull rider (see
      hybrid-assignment-criteria memo §4). Keyed ctrl_treatment=damage, ctrl_function=pull.
  (c) 4 Destroyer rows are skill-anchored; CELL-distinctness verified (differ on
      commit + geometry + dependency). No two collapse to one cell. All 4 keyed distinct.
  (d) di-cyclone-strike-monk-base vs di-cyclone-monk-pvp land in DIFFERENT cells (differ on
      movement + delivery + commit). Verified distinct; two kits, not one.
  (e) Undecember Illusion Hook: bounded re-check attempted (source fetch failed 402/refused);
      in-corpus evidence decisive: ud-illusion-family already carries Arrow/Axe/HOOK as
      weapon-type variants of an ECHO-COPY skill (geometry=multi_projectile, damage x none),
      NOT a grappling pull. Not a pull skill; already represented. NO new ud- row.

KEYING NOTE — `pull` function level:
  `pull` is the Edition-II NEW function level (register v1.2, Stage 2). serialize_cell_key does
  NOT validate the function slot (slot() only maps None->blank), so `pull` serializes cleanly
  into the cell_key string here. Register v1.2 (Stage 2) makes `pull` canonical + adds it to the
  ghost/displacement crosswalk so lit pull cells project.

DELIVERY=melee COLLAPSE (documented, honest):
  The 4 Destroyer rows + DI base carry delivery=melee. `delivery=melee` is a legal corpus
  cell_key slot value (26 survivors use it), so they key at FULL completeness into corpus.db.
  BUT the ghost/displacement meso crosswalk (fit2reg_delivery) has no `melee` image -> these
  rows do NOT light a meso ghost cell (same MELEE-collapse the MCD re-run documented). The
  ranged pull rows (d3-wizard-black-hole ZONE, d4-spiritborn-vortex ZONE) DO map. This is the
  structural reality of pull's genre expression (melee gravity-hammers) — surfaced, not papered.

IDEMPOTENT: additive; new rows upserted from static manifest each run. The 469 clean survivor
  cell_keys are NEVER touched (SHA c6933deb... asserted before + after). Enrichment writes are
  WHERE kit_id IN the two explicit enrichment ids and touch NO cell_key column.
  Backup taken by caller (corpus.db.pre-edition2-2026-07-15-backup).
"""

import json
import sqlite3
import sys
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_cell_key_materialize_2026_07_13 import serialize_cell_key, CELL_KEY_ORDER  # noqa: E402

DB = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db")

PROVENANCE_TAG = "pull-tranche-edition2-2026-07-15"
SOURCE_DATE = "2026-07-15"

# The frozen non-mcd survivor digest. Stage 1 must NOT perturb it.
#   This is the PYTHON-encoding digest ('\n'.join, no trailing newline) of the SAME 469-row
#   survivor set the MCD log froze as shell-digest c6933deb... (raw sqlite3 output + trailing
#   newline). Two encodings of one identical row set; both reproduce byte-perfectly. This
#   script's survivor_digest() uses the python encoding, so the constant matches that encoding.
SURVIVOR_SHA_BASELINE = "ce67bfba3ae804ddbcb02b8590d88bd5c52ea45d70820108039ea9d7367c5958"
SURVIVOR_SHA_BASELINE_SHELL = "c6933deb633e756f5fab280de7496ef9f0862bf575174bb9138589f8086e823a"


# The 7 NEW kit_ids this script adds — additive, NOT survivors. Excluded from the survivor
# digest so the guard measures the true invariant: the pre-existing 469 survivor cell_keys.
NEW_KIT_IDS = {
    "la-destroyer-vortex-gravity", "la-destroyer-gravity-impact", "la-destroyer-gravity-force",
    "la-destroyer-gravity-compression", "d4-spiritborn-vortex", "d3-wizard-black-hole",
    "di-cyclone-strike-monk-base",
}


def survivor_digest(cur):
    """Digest of the 469 PRE-EXISTING survivor cell_keys (non-mcd, non-new). Byte-invariant
    across Stage 1 (new-rows-only). Excludes the 7 additive NEW_KIT_IDS."""
    rows = cur.execute(
        "SELECT k.kit_id||'|'||k.cell_key FROM canon_engine_key k "
        "JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' "
        "ORDER BY k.kit_id"
    ).fetchall()
    rows = [r for r in rows if r[0].split("|", 1)[0] not in NEW_KIT_IDS]
    blob = "\n".join(r[0] for r in rows)
    return hashlib.sha256(blob.encode()).hexdigest()


# =====================================================================================
# THE MANIFEST — 7 new rows, source-anchored to the tranche table (the ground truth).
# Each carries: corpus-row fields + engine-key fields. cell_key SERIALIZED from the
# engine-key coords via the survivors' serialize_cell_key (byte-consistent vocabulary).
#
# cell_key column order (CELL_KEY_ORDER):
#   mob_policy_while_casting | delivery_value | amp_val | geometry_value | ctrl_treatment |
#   ctrl_function | def_bin | economy_model | proxy_val | range_val | tempo_val | commit_val |
#   activation_val | dependency_val
# =====================================================================================
NEW = [
    # ---- Lost Ark Destroyer (new source la-; 4 skill-anchored rows) ----
    dict(
        kit_id="la-destroyer-vortex-gravity", game="lost-ark", folk_name="Destroyer — Vortex Gravity",
        canon_tier="deep", attr_val="STR", range_val="melee", tempo_val="high", amp_val="spiky",
        proxy_val="solo", commit_val="instant",
        # engine-key coords
        mob="rooted", delivery="melee", geometry="vortex_pull",
        treatment="damage", function="pull",           # STAGE-0: hybrid rejected -> damage + pull rider (P2/P3 fail: Rage Hammer path)
        defense="tank", economy="cooldown", activation="active", dependency="one-shot",
        pull_anchor="pull-to-self",
        mech_note=("Destroyer identity skill. Hammer slam + gravitational explosion pulls foes within 6m; "
                   "High Stagger; Armor Destruction 12%%/~180s. Fires on Hypergravity Mode activation "
                   "(20s CD). STAGE-0 VERDICT (hybrid-assignment-criteria memo §4): treatment=hybrid "
                   "PROPOSED but REJECTED -> damage-primary + pull rider. P2 (control-removal) fails: "
                   "removing the pull leaves a High-Stagger damage burst (degraded, not collapsed). P3 "
                   "(configuration) fails: the Rage Hammer engraving path is a sanctioned variant that "
                   "de-emphasizes the gravity stance. Door: P2 degraded-but-operable + P3 configurable. "
                   "Pull is intrinsic (class skill) -> function=pull rider, ctrl_treatment=damage."),
        source_urls="https://lostarkcodex.com/us/skill/18011/", pull_pending_vocab=0,
    ),
    dict(
        kit_id="la-destroyer-gravity-impact", game="lost-ark", folk_name="Destroyer — Gravity Impact",
        canon_tier="deep", attr_val="STR", range_val="melee", tempo_val="med", amp_val="flat",
        proxy_val="solo", commit_val="channel",
        mob="rooted", delivery="melee", geometry="vortex_pull",
        treatment="damage", function="pull",
        defense="tank", economy="generator-spender", activation="active", dependency="build→spend",
        pull_anchor="pull-to-self",
        mech_note=("Concentration skill (core builder). Caster stationary; gravitational field pulls "
                   "enemies in 8x (195.2 dmg) then explosion (+63). Generates 2 Gravity Cores. Paralysis "
                   "Immunity during cast. Pull = density mechanic for multi-hit damage -> damage-primary + "
                   "pull rider (intrinsic rune/skill). Distinct cell from Vortex Gravity: commit=channel "
                   "(8-hit sequence) + dependency=build->spend (core generation)."),
        source_urls="https://lostark.wiki.fextralife.com/Gravity+Impact", pull_pending_vocab=0,
    ),
    dict(
        kit_id="la-destroyer-gravity-force", game="lost-ark", folk_name="Destroyer — Gravity Force",
        canon_tier="deep", attr_val="STR", range_val="melee", tempo_val="med", amp_val="flat",
        proxy_val="solo", commit_val="wind-up",
        mob="walk", delivery="melee", geometry="line",
        treatment="damage", function="pull",
        defense="mitigate", economy="generator-spender", activation="active", dependency="build→spend",
        pull_anchor="pull-to-point",
        mech_note=("Concentration skill. Frontal swing releases gravitational energy along a straight LINE, "
                   "attacking 7x (206.4 dmg) pulling enemies close ALONG THE AXIS (pull-to-point, not "
                   "pull-to-self). Generates 2 Gravity Cores. LINEAR geometry (line), not radial. "
                   "damage-primary + pull rider. Distinct cell: geometry=line + commit=wind-up + movement=walk."),
        source_urls="https://lostark.wiki.fextralife.com/Gravity+Force", pull_pending_vocab=0,
    ),
    dict(
        kit_id="la-destroyer-gravity-compression", game="lost-ark", folk_name="Destroyer — Gravity Compression",
        canon_tier="deep", attr_val="STR", range_val="melee", tempo_val="med", amp_val="spiky",
        proxy_val="solo", commit_val="channel",
        mob="rooted", delivery="melee", geometry="ground_targeted_circle",
        treatment="damage", function="none",           # FLAG (a): pull UNCONFIRMED from source -> NO pull key
        defense="mitigate", economy="generator-spender", activation="active", dependency="build→spend",
        pull_anchor=None,
        mech_note=("Gravity Release skill (SPENDER, consumes cores). Thrust hammer into ground -> "
                   "gravitational wave (29) -> hold 2s -> black hole (265.4 over 9 hits). Highest Stagger; "
                   "Part Break Lvl 2. FLAG (a) RESOLVED: the tranche's pull was INFERRED (legolas mech_note "
                   "admits it). Re-verified from source (fextralife 2026-07-15): base skill + ALL tripods "
                   "(Tough Heart / Magnetic Field Enh. / Move Position) describe damage/black-hole/stagger, "
                   "NO explicit pull/draw on living enemies. Never-invent governs -> function=NONE, "
                   "pull_pending_vocab=0, pull-implicit (the 9-hit black-hole density is NOT documented pull). "
                   "Distinct cell regardless: geometry=ground_targeted_circle + function=none + dependency=build->spend."),
        source_urls="https://lostark.wiki.fextralife.com/Gravity+Compression", pull_pending_vocab=0,
    ),
    # ---- Diablo 4 Spiritborn (existing d4- source; intrinsic class-tree pull) ----
    dict(
        kit_id="d4-spiritborn-vortex", game="diablo-4", folk_name="Spiritborn — Vortex",
        canon_tier="deep", attr_val="WIS", range_val="mid", tempo_val="med", amp_val="spiky",
        proxy_val="solo", commit_val="instant",
        # movement: tranche says "unknown (not documented)". Honest-NULL -> mob=blank (cell won't
        # light on movement gate, same as MCD classless — but here it's genuine source silence).
        mob=None, delivery="at-target", geometry="vortex_pull",
        treatment="damage", function="pull",
        defense="evade", economy="generator-spender", activation="active", dependency="build→spend",
        pull_anchor="pull-to-point",
        mech_note=("Spiritborn Focus skill (intrinsic class skill tree — NOT gear/aspect assembled). "
                   "Cyclone at targeted location pulls enemies inward + crushing downdraft (35%%->171%% at "
                   "rank 15). Lightning (Eagle spirit). 12s CD; Vigor generation. Pull clusters enemies; "
                   "downdraft delivers damage -> damage-primary + pull rider. The only intrinsic pull in "
                   "D4 base class trees. MOVEMENT: source-undocumented -> mob=blank (honest-NULL; cell will "
                   "not light on the movement gate until a movement value is sourced — never-invent)."),
        source_urls="https://diablo4.wiki.fextralife.com/Vortex", pull_pending_vocab=0,
    ),
    # ---- Diablo 3 Wizard Black Hole (existing d3- source; the genre pull precedent) ----
    dict(
        kit_id="d3-wizard-black-hole", game="diablo-3", folk_name="Wizard — Black Hole",
        canon_tier="deep", attr_val="INT", range_val="ranged", tempo_val="med", amp_val="spiky",
        proxy_val="solo", commit_val="instant",
        mob="rooted", delivery="at-target", geometry="vortex_pull",
        treatment="damage", function="pull",
        defense="glass", economy="spend", activation="active", dependency="one-shot",
        pull_anchor="pull-to-point",
        mech_note=("Wizard offensive skill. Black hole at ground-target draws enemies in + 700%% weapon "
                   "damage Arcane over 2s within 15y. 20 Arcane Power + 12s CD. IN-ENGINE 'counts as "
                   "Knockback' (triggers Strongarm Bracers) — but the register level is defined by force "
                   "DIRECTION (inward = pull), not the D3 engine's knockback-collapse. Black Hole is THE "
                   "genre precedent for the collapse our lattice refuses (register v1.2 boundary note). "
                   "damage-primary + pull rider. Runes (Supermassive/Absolute Zero/Event Horizon/Blazar/"
                   "Singularity) modify dmg, pull intrinsic to base. Community: underpowered vs CD, solo utility."),
        source_urls="https://diablo.fandom.com/wiki/Black_Hole", pull_pending_vocab=0,
    ),
    # ---- Diablo Immortal Cyclone Strike BASE (the missing skill-mechanics layer) ----
    dict(
        kit_id="di-cyclone-strike-monk-base", game="diablo-immortal", folk_name="DI Monk — Cyclone Strike (base)",
        canon_tier="deep", attr_val="DEX", range_val="melee", tempo_val="med", amp_val="flat",
        proxy_val="solo", commit_val="wind-up",
        mob="rooted", delivery="melee", geometry="vortex_pull",
        treatment="damage", function="pull",           # STAGE-0: hybrid rejected -> damage + pull rider (P3 fail: Storm Spirit removes pull)
        defense="evade", economy="cooldown", activation="active", dependency="one-shot",
        pull_anchor="pull-to-self",
        mech_note=("Base (unmodified) Cyclone Strike: vortex of wind pulls in enemies + deals damage; "
                   "charging longer increases range/damage (Charge type -> commit=wind-up, "
                   "rooted-while-charging). 2 charges, 12s CD. Pull IS intrinsic to base (no Legendary). "
                   "STAGE-0 VERDICT (hybrid-assignment-criteria memo §4): treatment=hybrid PROPOSED, the "
                   "GENUINE skill-level boundary case (co-equal pull+damage is REAL at skill grain — "
                   "gandalf's one-paragraph acknowledgment). But REJECTED at KIT grain: P3 (configuration) "
                   "fails — Storm Spirit essence (gear-assembled) removes the pull -> DPS-only, so the "
                   "hybrid is a player option not kit identity. Door: CONFIGURABLE-OUT. -> damage-primary + "
                   "pull rider. Distinct cell from di-cyclone-monk-pvp (differs on movement=rooted vs walk, "
                   "delivery=melee vs self-origin, commit=wind-up vs instant). Essence variants (Storm "
                   "Spirit/Driven Thunder/Tempest's Heart/Frigid Cyclone/Mystic Winds/Sandstorm) are "
                   "gear-assembled -> EXCLUDED per evidence bar."),
        source_urls="https://diabloimmortal.wiki.fextralife.com/Cyclone_Strike", pull_pending_vocab=0,
    ),
]

# ENRICHMENT — existing rows; mech_note fact-append + source-url refresh ONLY (NO cell_key touch;
# the re-keys are Stage 3). We append the enrichment provenance so the record is complete.
ENRICH = {
    "di-cyclone-monk-pvp": (
        " [EDITION-II ENRICHMENT 2026-07-15 (pull tranche b7f773d3)]: base-skill probe facts confirmed — "
        "12s CD / 2 charges; Charge type (wind-up); rooted-while-charging; radial-nova from caster; "
        "pull-to-self; base pull INTRINSIC (no Legendary). This PvP row is the Driven-Thunder/CC build; "
        "its identity is pull+knockback CC disruption (control centrality = CORE per existing mech_note). "
        "STAGE-3 re-keys function knockback->pull (Cyclone Strike's inward vortex IS pull; the DI engine's "
        "knockback label is force-direction-blind). See di-cyclone-strike-monk-base for the base-skill row."
    ),
    "d3-zbarb": (
        " [EDITION-II ENRICHMENT 2026-07-15 (pull tranche b7f773d3)]: Ground Stomp WRENCHING SMASH (a RUNE "
        "= intrinsic) — pull radius 24y, radial-nova pull-to-self, instant (30-frame), rooted during cast, "
        "triggers 40%% CC-res on pulled targets; immune: Juggernaut Rare Elites / Rift Guardians / large "
        "monsters; Waller blocks. Ancient Spear RAGE FLIP throws AWAY (outward displacement to a convergence "
        "point = knockback geometry, NOT pull). STAGE-3 re-keys function none->pull on the Wrenching-Smash "
        "intrinsic pull (the kit's density mechanic is the rune pull). zBarb gears AGAINST its own damage "
        "(control-primary in play) but the corpus row is keyed damage-primary; the pull is the rune rider."
    ),
}


def upsert_corpus_row(cur, r):
    cur.execute("""
        INSERT INTO canon_corpus
          (kit_id, folk_name, game, corpus_bucket, canon_tier, negative, source, is_system,
           unresolved, provenance_tag, source_date, attr_val, range_val, tempo_val, amp_val,
           proxy_val, commit_val, prefix_conf_provenance, key_completeness, mech_note,
           source_urls, pull_pending_vocab, architecture, flags, prov)
        VALUES (?,?,?,?,?,0,'canon',0, 0, ?, ?, ?,?,?,?, ?,?, 'pull-tranche-steward-derived', ?, ?,
                ?, ?, NULL, ?, 'legolas-mode-b;elrond-curated')
        ON CONFLICT(kit_id) DO UPDATE SET
          folk_name=excluded.folk_name, game=excluded.game, corpus_bucket=excluded.corpus_bucket,
          canon_tier=excluded.canon_tier, provenance_tag=excluded.provenance_tag,
          source_date=excluded.source_date, attr_val=excluded.attr_val, range_val=excluded.range_val,
          tempo_val=excluded.tempo_val, amp_val=excluded.amp_val, proxy_val=excluded.proxy_val,
          commit_val=excluded.commit_val, key_completeness=excluded.key_completeness,
          mech_note=excluded.mech_note, source_urls=excluded.source_urls,
          pull_pending_vocab=excluded.pull_pending_vocab, flags=excluded.flags, prov=excluded.prov
    """, (
        r["kit_id"], r["folk_name"], r["game"], r["game"], r["canon_tier"],
        PROVENANCE_TAG, SOURCE_DATE, r["attr_val"], r["range_val"], r["tempo_val"], r["amp_val"],
        r["proxy_val"], r["commit_val"],
        # key_completeness = count of the 6 prefix coords non-NULL (attr/range/tempo/amp/proxy/commit)
        sum(1 for k in ("attr_val", "range_val", "tempo_val", "amp_val", "proxy_val", "commit_val")
            if r.get(k) is not None),
        r["mech_note"], r["source_urls"], r["pull_pending_vocab"],
        json.dumps([f"pull-anchor:{r['pull_anchor']}"] if r.get("pull_anchor") else []),
    ))


def upsert_engine_key(cur, r):
    # Build the row dict serialize_cell_key reads (CELL_KEY_ORDER column names).
    keyrow = {
        "mob_policy_while_casting": r["mob"],
        "delivery_value": r["delivery"],
        "amp_val": r["amp_val"],
        "geometry_value": r["geometry"],
        "ctrl_treatment": r["treatment"],
        "ctrl_function": r["function"],
        "def_bin": r["defense"],
        "economy_model": r["economy"],
        "proxy_val": r["proxy_val"],
        "range_val": r["range_val"],
        "tempo_val": r["tempo_val"],
        "commit_val": r["commit_val"],
        "activation_val": r["activation"],
        "dependency_val": r["dependency"],
    }
    cell_key = serialize_cell_key(keyrow)
    prov = {"source": "pull-tranche-edition2", "curator": "elrond", "date": SOURCE_DATE,
            "stage0_treatment_verdict": r["treatment"], "flags_applied": "gandalf-5-flags"}
    cur.execute("""
        INSERT INTO canon_engine_key
          (kit_id, geometry_value, ctrl_treatment, ctrl_function, def_bin, delivery_value,
           economy_model, activation_val, dependency_val, mob_policy_while_casting, mob_verbs,
           row_class, flags, provenance_json, raw_json, cell_key)
        VALUES (?,?,?,?,?,?,?,?,?,?,?, 'combat-kit', ?, ?, ?, ?)
        ON CONFLICT(kit_id) DO UPDATE SET
          geometry_value=excluded.geometry_value, ctrl_treatment=excluded.ctrl_treatment,
          ctrl_function=excluded.ctrl_function, def_bin=excluded.def_bin,
          delivery_value=excluded.delivery_value, economy_model=excluded.economy_model,
          activation_val=excluded.activation_val, dependency_val=excluded.dependency_val,
          mob_policy_while_casting=excluded.mob_policy_while_casting, cell_key=excluded.cell_key,
          flags=excluded.flags, provenance_json=excluded.provenance_json
    """, (
        r["kit_id"], r["geometry"], r["treatment"], r["function"], r["defense"], r["delivery"],
        r["economy"], r["activation"], r["dependency"], r["mob"],
        json.dumps([r["mob"]] if r["mob"] else []),
        json.dumps([f"pull-anchor:{r['pull_anchor']}"] if r.get("pull_anchor") else []),
        json.dumps(prov), json.dumps({"kit_id": r["kit_id"], "src": "pull-tranche"}), cell_key,
    ))
    return cell_key


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # ---- GUARD: survivor digest byte-identical (Stage 1 is new-rows only) ----
    pre = survivor_digest(cur)
    assert pre == SURVIVOR_SHA_BASELINE, f"survivor baseline drift BEFORE: {pre}"

    print("== STAGE 1: pull-tranche ingest ==")
    keyed = {}
    for r in NEW:
        upsert_corpus_row(cur, r)
        if r["function"] == "pull" or r["kit_id"] == "la-destroyer-gravity-compression":
            # all 7 are keyed (full completeness — the legibility that motivated the crawl)
            pass
        ck = upsert_engine_key(cur, r)
        keyed[r["kit_id"]] = ck
        print(f"  + {r['kit_id']:34s} treatment={r['treatment']:7s} function={r['function']:6s} "
              f"delivery={r['delivery']:10s}")

    # ---- ENRICHMENT: append mech_note facts to the two existing rows (NO cell_key touch) ----
    for kid, addendum in ENRICH.items():
        cur.execute("UPDATE canon_corpus SET mech_note = COALESCE(mech_note,'') || ? "
                    "WHERE kit_id=? AND mech_note NOT LIKE '%EDITION-II ENRICHMENT 2026-07-15%'",
                    (addendum, kid))
        print(f"  ~ enriched {kid} (mech_note fact-append; cell_key untouched)")

    # schema marker
    cur.execute("INSERT INTO corpus_schema_meta VALUES (?,?,?)", (
        "pull-tranche-edition2-stage1-2026-07-15", "2026-07-15T00:00:00Z",
        "Edition-II Stage 1 (elrond): pull-tranche ingest. 7 new rows (4 la-Destroyer + "
        "d4-spiritborn-vortex + d3-wizard-black-hole + di-cyclone-strike-monk-base) keyed at full "
        "completeness with the NEW function=pull (register v1.2). STAGE-0 hybrid criteria applied: "
        "both proposed hybrids -> damage+pull rider (P2/P3 fail). Flag(a): gravity-compression pull "
        "UNCONFIRMED from source -> function=none. Flag(e): Illusion Hook not a pull skill (already "
        "in ud-illusion-family as echo-copy) -> no new row. Enrichment on di-cyclone-monk-pvp + "
        "d3-zbarb (mech_note only; re-keys are Stage 3). Additive; 469 survivor cell_keys byte-identical.",
    ))

    # ---- GUARD: survivor digest STILL byte-identical (new rows must not perturb survivors) ----
    post = survivor_digest(cur)
    assert post == SURVIVOR_SHA_BASELINE, (
        f"SURVIVOR DIGEST CHANGED in Stage 1 (must not happen — new rows only)!\n"
        f"  before: {pre}\n  after : {post}")
    print(f"\n  survivor digest byte-identical: {post[:16]}... (== baseline) OK")

    con.commit()

    # ---- verification ----
    n_la = cur.execute("SELECT count(*) FROM canon_corpus WHERE kit_id LIKE 'la-%'").fetchone()[0]
    n_pull_fn = cur.execute("SELECT count(*) FROM canon_engine_key WHERE ctrl_function='pull'").fetchone()[0]
    n_total = cur.execute("SELECT count(*) FROM canon_corpus").fetchone()[0]
    print(f"\n  la- rows: {n_la} (expect 4)   ctrl_function='pull' rows: {n_pull_fn}   corpus total: {n_total}")
    print("  new cell_keys:")
    for kid in sorted(keyed):
        print(f"    {kid:34s} {keyed[kid]}")

    con.close()
    print("\nSTAGE 1 COMPLETE.")


if __name__ == "__main__":
    main()
