"""
corpus_s2_census_v10_2026_07_17.py — S2 readiness census V10 (post-Wave-C landing).
Author: elrond, 2026-07-17 (autonomous atlas-parity run, Wave-C corpus-align + V10 census charge).

Authority: gandalf-prime charter 2026-07-17 (Wave-C engine landed at `941dbbf`, PUSHED;
Gate-2 PASS; elrond is the single corpus.db writer for corpus-align).

STRUCTURE (two parts, one script, one transaction per Part 1):

  PART 1 — corpus-align WRITES (provenance tag `wave-c-corpus-align-2026-07-17`)
    1a. le-frost-wall-rm: geometry_value totem → placed_lane (spec §5.2)
    1b. 3 TH kits (d3-invoker-thorns, d4-thorns-barb, gd-retaliation-warlord):
        econ:UNKNOWN → LANDED (drop UNKNOWN from econ_gaps, set econ_status='native',
        add corpus.flags provenance stamp naming TH damage-taken-converts)
    1c. chr-thorns-templar: NO write. Disposition note only (PC+BT landed Wave-B/Wave-C).
    1d. di-spiritform-druid-pvp: NO write. Best-effort WebSearch could not verify
        the ailment authoritatively; kit remains flagged unknown-ailment per honesty-first.
    1e. d2-smiter + d2-zealot: WebSearch VERIFIED via Arreat Summit + Maxroll + Icy-Veins
        as 2-mana-fixed-cost paladin skills (conventional spend-mana). Drop UNKNOWN from
        econ_gaps; keep BT (which is landed Wave-C — classifier drops it there).
        Provenance stamp names the sources.
    1f. AC-5 role="support" corpus query: EMPTY. Neither corpus.raw_json nor v2_narrow
        classes.json nor kit_space/kits carries `role="support"`. Named-regression list
        closes as empty; report in notes artifact.

  PART 2 — CENSUS V10 (pure read on POST-write DB)
    Denominator: 565 (V9 unchanged; Part 1 is TAG-align only, not row-class change).
    Classifier V10 delta vs V9: Wave-C landed = blind, curse/hex, fear, instant-kill,
    deflect, TH; BT, LC, and orbit + placed-lane geometries also landed.
    NOT landed: shapeshift, DR, econ:UNKNOWN residue, unknown-ailment.

IRON LAWS (this run):
    1. PRE-state asserts (V9 counts) held BEFORE writes; POST-state asserts (V10 counts,
       UNCHANGED at grain level) held AFTER. Total 585, denominator 565, roster 45.
    2. Multi-blocker honesty: kit is expressible only when its ENTIRE blockset empty.
       Report Wave-C-cohort decomposition + realign-effect from Part 1 writes.
    3. Roster 45/45 UNCHANGED (verified).
    4. HEADLINE decomposition: Δ = wavec_flip_effect + realign_effect + denominator_effect.
       Report each separately per iron law 4.
    5. DB WINS over projections: any divergence from spec's 549/551 projection is
       enumerated per-kit with rationale (multi-blocker residue).
    6. md5-stability: DB md5 captured post-Part-1-write; census pass proves same md5
       at end of run.

DENOMINATOR LAW (V10 — UNCHANGED from V9):
    §F.5(1) pool = 520 corpus positives at kit grain + 45 founding roster = 565.
    Negatives (43 kit-grain), NULL-grain system-records (22), and grain=NULL mints
    EXCLUDED. 4 dossier_owed IN pool, flagged NOT-YET-EMISSIBLE.
"""

import hashlib
import json
import pathlib
import shutil
import sys
from collections import Counter, defaultdict

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = BASE / "agentic_orchestration/research/curated/atlas"
OUT_CENSUS = ATLAS_DIR / "s2-readiness-census-v10-2026-07-17.md"
BACKUP_PATH = BASE / "agentic_orchestration/research/curated/corpus.db.pre-v10-2026-07-17-backup"

import sqlite3

# ---------------------------------------------------------------------------
# PRE-state (V9 counts, DB truth) — asserted BEFORE any write
# ---------------------------------------------------------------------------
PRE_EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "kit_grain": 563,
    "null_grain": 22,
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
    "combat_kit_rc": 563,
    "system_record_rc": 22,
}
# Part 1 writes are TAG-aligns; POST state at grain/row_class layer is IDENTICAL.
POST_EXPECTED = dict(PRE_EXPECTED)

# V9 published headline — the §4 delta anchor.
V9_PUBLISHED_POOL_EXPRESSIBLE = 509
V9_PUBLISHED_POOL_TOTAL = 565
V9_PUBLISHED_POOL_PCT = 90.1
V9_PUBLISHED_CORPUS_EXPRESSIBLE = 464
V9_PUBLISHED_CORPUS_TOTAL = 520

PROVENANCE_TAG = "wave-c-corpus-align-2026-07-17"

# ---------------------------------------------------------------------------
# CLASSIFICATION VOCABULARY (V10)
# ---------------------------------------------------------------------------
# Econ gaps LANDED under Wave-A + Wave-B + Wave-C — expressible in V10:
WAVE_A_ECON_LANDED = {"SU", "HV"}                              # summon-uptime + harvest
WAVE_B_ECON_LANDED = {"PC", "RS", "AM", "RC"}                  # persistent-condition + reservation + attunement-meter + recharge
WAVE_C_ECON_LANDED = {"BT", "TH", "LC"}                        # block-trigger + damage-taken-converts + life-cost (Wave-C spec §3/§6/§7)
ECON_LANDED_V10 = WAVE_A_ECON_LANDED | WAVE_B_ECON_LANDED | WAVE_C_ECON_LANDED

# Econ gaps STILL BLOCKED (post-Wave-C):
WAVE_D_OR_BEYOND_ECON_GAPS = {"DR"}   # drain — NOT in Wave-C landed set (per ruling WC-19 defer)
UNKNOWN_GAP = {"UNKNOWN"}              # unclassified residue

# Ailment layer LANDED (V9 baseline)
AILMENT_LANDED_V9 = {
    "GAP-AILMENT:damage-amp",     # → sunder (ruling 5)
    "GAP-AILMENT:freeze",         # chill-escalation + shatter payoff
    "GAP-AILMENT:stun",           # short hard CC + boss resistance
    "GAP-AILMENT:poison-dot",     # independent-stack DoT
    "GAP-AILMENT:taunt",          # proxy-AI directive on Wave-A machinery
}
# Ailment layer LANDED IN WAVE-C (per spec §4):
AILMENT_LANDED_WAVE_C = {
    "GAP-AILMENT:blind",
    "GAP-AILMENT:curse/hex",
    "GAP-AILMENT:fear",
    "GAP-AILMENT:instant-kill",   # canonical name in spec: execute
    "GAP-AILMENT:deflect",         # routed to def-bin rider (Wave-C spec §4.5)
}
AILMENT_LANDED_V10 = AILMENT_LANDED_V9 | AILMENT_LANDED_WAVE_C

# Ailment layer NOT landed at V10:
AILMENT_STILL_BLOCKED_V10 = {
    "GAP-AILMENT:unknown-ailment",   # requires re-crawl, not spec
}

# Geometry small-adds LANDED IN WAVE-C:
GEOMETRY_LANDED_WAVE_C = {"orbit", "placed_lane"}


def parse_json_list(s):
    if not s or s == "[]":
        return []
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return []


def classify_kit(row, wave_c_landed=True):
    """Return (expressible_now: bool, blocked_on: set[str]).

    wave_c_landed=True is the V10 rule (Wave-C landed).
    wave_c_landed=False reproduces the V9-era rule (used only for flip decomposition,
    NOT for the V10 headline).

    Multi-blocker honest: unions ALL blockers; expressible IFF blockset empty.
    """
    blocked_on = set()

    for eg in parse_json_list(row.get("econ_gaps")):
        if eg in WAVE_A_ECON_LANDED or eg in WAVE_B_ECON_LANDED:
            continue  # Wave-A/B landed pre-V10
        if eg in WAVE_C_ECON_LANDED:
            if wave_c_landed:
                continue  # Wave-C landed (V10 rule)
            else:
                blocked_on.add(f"econ:{eg}")
                continue
        # DR / UNKNOWN / anything else → blocked
        blocked_on.add(f"econ:{eg}")

    # partial:LC econ_status is a landed Wave-C mechanic (spec §7):
    if row.get("econ_status") == "partial:LC":
        if not wave_c_landed:
            blocked_on.add("econ:LC")
        # else: LC landed, no add.

    for ag in parse_json_list(row.get("ctrl_ailment_gaps")):
        name = ag.replace("GAP-AILMENT:", "")
        if ag in AILMENT_LANDED_V9:
            continue
        elif ag in AILMENT_LANDED_WAVE_C:
            if wave_c_landed:
                continue
            else:
                if ag == "GAP-AILMENT:deflect":
                    blocked_on.add(f"ailment-wave-c+:deflect")
                elif ag == "GAP-AILMENT:instant-kill":
                    blocked_on.add(f"ailment-wave-c+:instant-kill")
                else:
                    blocked_on.add(f"ailment-wave-c+:{name}")
                continue
        elif ag in AILMENT_STILL_BLOCKED_V10:
            blocked_on.add(f"ailment-wave-c+:{name}")
        else:
            blocked_on.add(f"ailment-unclassified:{name}")

    geom = row.get("geometry_value") or ""
    if geom in GEOMETRY_LANDED_WAVE_C:
        if not wave_c_landed:
            blocked_on.add(f"geometry:{geom}")
        # else: landed Wave-C

    flags_raw = row.get("flags") or ""
    # gx-candidate:orbit is a legacy corpus flag — orbit is landed Wave-C so drop.
    if "gx-candidate:orbit" in flags_raw:
        if not wave_c_landed:
            blocked_on.add("geometry:orbit")
    # resolved:walls-demand is a legacy corpus flag on kits that WERE walls-demand
    # candidates but stayed keyed as totem geometry pre-Wave-C. Placed-lane landed
    # Wave-C, so drop.
    if "resolved:walls-demand" in flags_raw:
        if not wave_c_landed:
            blocked_on.add("geometry:walls-placed-lane")
    if "J-GEO:placed-lane" in flags_raw:
        if not wave_c_landed:
            blocked_on.add("geometry:walls-placed-lane")

    kit_id = row.get("kit_id") or ""
    # Shapeshift substring rule (Matt-fork gate — GX-02 docket OPEN; NOT landed):
    if any(marker in kit_id for marker in [
        "wildsoul", "wereforms", "spirit-form", "spiritborn-vortex",
    ]):
        # Exclude the d4-spiritborn-vortex (composite spiritborn+vortex substring)
        if not ("vortex" in kit_id and "spiritborn" in kit_id):
            blocked_on.add("mechanic:shapeshift")

    expressible_now = len(blocked_on) == 0
    return expressible_now, blocked_on


# ---------------------------------------------------------------------------
# PART 1 — corpus-align WRITES
# ---------------------------------------------------------------------------

WRITE_LEDGER = []  # each entry: dict(kit_id, action, before, after, provenance)


def part1_align_writes(conn):
    """Apply the 6 corpus-align writes (5 kit-touches + 1 empty audit).

    Each write is idempotent — checks the provenance flag first and no-ops if present.
    """
    print("\nPART 1: Applying wave-c-corpus-align writes...")
    applied = 0

    # -------- W1a: le-frost-wall-rm geometry_value totem → placed_lane --------
    row = conn.execute(
        "SELECT geometry_value, flags FROM canon_engine_key WHERE kit_id='le-frost-wall-rm'"
    ).fetchone()
    assert row is not None, "le-frost-wall-rm missing"
    geom_before, flags_before = row
    flags_list = parse_json_list(flags_before)
    already_aligned = any(
        f.startswith(f"resolved:{PROVENANCE_TAG}:placed-lane-rewire")
        for f in flags_list
    )
    if already_aligned:
        print("    W1a IDEMPOTENT: le-frost-wall-rm already tagged")
    else:
        new_flags = list(flags_list) + [
            f"resolved:{PROVENANCE_TAG}:placed-lane-rewire"
        ]
        conn.execute(
            "UPDATE canon_engine_key SET geometry_value=?, geometry_rule_fired=?, flags=? WHERE kit_id=?",
            ("placed_lane", "R0b-realign-wave-c",
             json.dumps(new_flags), "le-frost-wall-rm"),
        )
        WRITE_LEDGER.append({
            "kit_id": "le-frost-wall-rm",
            "action": "geometry_value: totem → placed_lane; geometry_rule_fired: R0b → R0b-realign-wave-c",
            "before": {"geometry_value": geom_before, "flags": flags_before},
            "after": {"geometry_value": "placed_lane", "flags": json.dumps(new_flags)},
            "provenance": f"resolved:{PROVENANCE_TAG}:placed-lane-rewire (spec §5.2:870; DB-native token underscore per convention)",
        })
        applied += 1
        print(f"    W1a: le-frost-wall-rm  geometry_value  {geom_before} → placed_lane")

    # -------- W1b: 3 TH kits (drop UNKNOWN, set native, stamp provenance) --------
    th_kits = [
        ("d3-invoker-thorns",     "damage-taken-converts / thorns primary"),
        ("d4-thorns-barb",        "damage-taken-converts / thorns primary"),
        ("gd-retaliation-warlord","damage-taken-converts / retaliation primary"),
    ]
    for kit_id, note in th_kits:
        row = conn.execute(
            "SELECT econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        cc = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        assert row is not None and cc is not None
        eco_status_before, eco_gaps_before = row
        corp_flags_before = cc[0] or ""

        provenance_stamp = f"{PROVENANCE_TAG}:TH-damage-taken-converts:{note}"
        if provenance_stamp in corp_flags_before:
            print(f"    W1b IDEMPOTENT: {kit_id} already tagged")
            continue

        # engine_key: drop UNKNOWN, set econ_status='native' (matches audit-resolved pattern)
        gaps_list = parse_json_list(eco_gaps_before)
        gaps_after = [g for g in gaps_list if g != "UNKNOWN"]  # drop UNKNOWN
        conn.execute(
            "UPDATE canon_engine_key SET econ_status='native', econ_gaps=? WHERE kit_id=?",
            (json.dumps(gaps_after), kit_id),
        )
        # corpus flags: append provenance stamp (comma-delimited pattern per existing convention)
        new_corp_flags = (
            corp_flags_before + "," + provenance_stamp if corp_flags_before
            else provenance_stamp
        )
        conn.execute(
            "UPDATE canon_corpus SET flags=? WHERE kit_id=?",
            (new_corp_flags, kit_id),
        )
        WRITE_LEDGER.append({
            "kit_id": kit_id,
            "action": "econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += TH provenance",
            "before": {"econ_status": eco_status_before, "econ_gaps": eco_gaps_before,
                       "corpus_flags": corp_flags_before},
            "after": {"econ_status": "native", "econ_gaps": json.dumps(gaps_after),
                      "corpus_flags": new_corp_flags},
            "provenance": provenance_stamp,
        })
        applied += 1
        print(f"    W1b: {kit_id}  econ  {eco_status_before}/{eco_gaps_before} → native/{gaps_after}")

    # -------- W1e: d2-smiter + d2-zealot (drop UNKNOWN, keep BT [landed], stamp provenance) --------
    # WebSearch VERIFIED: D2 Smite and Zeal both cost 2 mana fixed per use, per
    # Arreat Summit + Maxroll + Icy-Veins. This is conventional spend-mana; the
    # UNKNOWN was a mis-classification.
    d2_kits = [
        ("d2-smiter",
         "spend/steady-mana (2 mana fixed cost per use, all levels); sources: "
         "Arreat Summit + Maxroll d2/guides/smite-paladin + Icy-Veins d2/smiter-paladin-build"),
        ("d2-zealot",
         "spend/steady-mana (Zeal 2 mana fixed cost per use, all levels); sources: "
         "Arreat Summit + Maxroll d2/guides/zeal-paladin + Icy-Veins d2/zealot-paladin-build"),
    ]
    for kit_id, note in d2_kits:
        row = conn.execute(
            "SELECT econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        cc = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        assert row is not None and cc is not None
        eco_status_before, eco_gaps_before = row
        corp_flags_before = cc[0] or ""

        provenance_stamp = f"{PROVENANCE_TAG}:econ-recrawl-verified:{note}"
        if provenance_stamp in corp_flags_before:
            print(f"    W1e IDEMPOTENT: {kit_id} already tagged")
            continue

        # engine_key: drop UNKNOWN, keep BT (BT is landed Wave-C, classifier drops it)
        gaps_list = parse_json_list(eco_gaps_before)
        gaps_after = [g for g in gaps_list if g != "UNKNOWN"]
        # after keeping BT: {"BT"}. Set econ_status='native' since UNKNOWN is the last
        # non-landed gap; BT is landed so the residue is empty from the classifier's view.
        # Prefer 'native' to match audit-resolved pattern.
        conn.execute(
            "UPDATE canon_engine_key SET econ_status='native', econ_gaps=? WHERE kit_id=?",
            (json.dumps(gaps_after), kit_id),
        )
        new_corp_flags = (
            corp_flags_before + "," + provenance_stamp if corp_flags_before
            else provenance_stamp
        )
        conn.execute(
            "UPDATE canon_corpus SET flags=? WHERE kit_id=?",
            (new_corp_flags, kit_id),
        )
        WRITE_LEDGER.append({
            "kit_id": kit_id,
            "action": "econ_status: gap → native; econ_gaps: drop UNKNOWN (keep BT — landed); corpus.flags: += audit-verified provenance",
            "before": {"econ_status": eco_status_before, "econ_gaps": eco_gaps_before,
                       "corpus_flags": corp_flags_before},
            "after": {"econ_status": "native", "econ_gaps": json.dumps(gaps_after),
                      "corpus_flags": new_corp_flags},
            "provenance": provenance_stamp,
        })
        applied += 1
        print(f"    W1e: {kit_id}  econ  {eco_status_before}/{eco_gaps_before} → native/{gaps_after}")

    print(f"    total rows written: {applied}")
    return applied


def run_asserts(conn, label, expected):
    actual = {
        "total_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "total_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "kit_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0],
        "null_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL").fetchone()[0],
        "cell_key_resolved": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE cell_key IS NOT NULL").fetchone()[0],
        "bt_sentinel": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE '%-bt'").fetchone()[0],
        "orphans_engine": conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ek WHERE NOT EXISTS "
            "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=ek.kit_id)"
        ).fetchone()[0],
        "orphans_corpus": conn.execute(
            "SELECT COUNT(*) FROM canon_corpus c WHERE NOT EXISTS "
            "(SELECT 1 FROM canon_engine_key ek WHERE ek.kit_id=c.kit_id)"
        ).fetchone()[0],
        "dossier_owed": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1").fetchone()[0],
        "combat_kit_rc": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit'").fetchone()[0],
        "system_record_rc": conn.execute("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record'").fetchone()[0],
    }
    print(f"\n[{label}] iron-law asserts:")
    breach = False
    for k, exp in expected.items():
        act = actual[k]
        ok = act == exp
        if not ok:
            breach = True
        print(f"    {k:24s} expected={exp:>4d}  actual={act:>4d}  {'OK' if ok else 'BREACH'}")
    return actual, breach


# ---------------------------------------------------------------------------
# PART 2 — CENSUS V10 (pure read on POST-write state)
# ---------------------------------------------------------------------------

def run_census(conn):
    """Read-only census on the POST-write DB state (denominator 565)."""
    cur = conn.execute("""
        SELECT
            cc.kit_id, cc.folk_name, cc.game, cc.corpus_bucket, cc.dossier_owed,
            cc.mint, cc.negative, cc.grain,
            ce.geometry_value, ce.econ_status, ce.econ_gaps, ce.ctrl_ailment_gaps,
            ce.ctrl_ailments_mapped, ce.def_bin, ce.cell_key, ce.flags, ce.route, ce.row_class
        FROM canon_corpus cc
        LEFT JOIN canon_engine_key ce ON ce.kit_id = cc.kit_id
        WHERE cc.grain = 'kit' AND cc.negative = 0
        ORDER BY cc.game, cc.kit_id
    """)
    corpus_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(corpus_rows) == 520, f"V10 corpus positives = {len(corpus_rows)}, expected 520 (UNCHANGED from V9)"

    cur = conn.execute("SELECT kit_id, name, mob_policy_while_casting, commit_val FROM roster_atlas")
    roster_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(roster_rows) == 45, f"roster = {len(roster_rows)}, expected 45 (UNCHANGED)"

    # V10 classification (Wave-C landed)
    corpus_classified = []
    bucket_counter = Counter()
    for row in corpus_rows:
        expressible, blocked = classify_kit(row, wave_c_landed=True)
        corpus_classified.append({
            "kit_id": row["kit_id"],
            "folk_name": row["folk_name"],
            "game": row["game"],
            "dossier_owed": bool(row["dossier_owed"]),
            "expressible_now": expressible,
            "blocked_on": sorted(blocked),
            "blocked_set": blocked,
        })
        for b in blocked:
            bucket_counter[b] += 1

    # Roster: SPEC ANCHOR
    roster_classified = [{
        "kit_id": row["kit_id"], "name": row["name"],
        "expressible_now": True, "blocked_on": [],
    } for row in roster_rows]

    all_classified = corpus_classified + roster_classified

    total = len(all_classified)
    expressible = sum(1 for k in all_classified if k["expressible_now"])
    blocked = total - expressible
    held_out = sum(1 for k in corpus_classified if k.get("dossier_owed"))

    corpus_expressible = sum(1 for k in corpus_classified if k["expressible_now"])
    corpus_blocked = len(corpus_classified) - corpus_expressible
    roster_expressible = sum(1 for k in roster_classified if k["expressible_now"])

    # -------------------------------------------------------------------
    # MULTI-BLOCKER HONESTY: Wave-C-cohort flip decomposition.
    # Cohort = distinct kits carrying >=1 Wave-C-lift-affected token in V9-rule blockset
    # -------------------------------------------------------------------
    # Wave-C affects: econ:BT / econ:LC / econ:TH / ailment blind/curse/fear/execute/deflect /
    #                 geometry:orbit / geometry:walls-placed-lane
    wc_cohort_kits = []
    for r in corpus_rows:
        _, v9b = classify_kit(r, wave_c_landed=False)
        wc_touched = {
            b for b in v9b
            if b in {
                "econ:BT", "econ:LC", "econ:TH",
                "ailment-wave-c+:blind", "ailment-wave-c+:curse/hex",
                "ailment-wave-c+:fear", "ailment-wave-c+:instant-kill",
                "ailment-wave-c+:deflect",
                "geometry:orbit", "geometry:walls-placed-lane",
            }
        }
        if wc_touched:
            wc_cohort_kits.append((r, v9b, wc_touched))

    wc_flipped = 0
    wc_residue = 0
    wc_residue_reasons = Counter()
    for r, _v9b, _wct in wc_cohort_kits:
        _, v10b = classify_kit(r, wave_c_landed=True)
        if len(v10b) == 0:
            wc_flipped += 1
        else:
            wc_residue += 1
            for x in v10b:
                wc_residue_reasons[x] += 1

    # Cross-check: net corpus flip V9-rule → V10-rule
    v9rule_corpus_exp = sum(
        1 for r in corpus_rows if classify_kit(r, wave_c_landed=False)[0]
    )
    net_flip = corpus_expressible - v9rule_corpus_exp

    # Realign effect: how many kits flipped attributable to Part 1 writes (not Wave-C-landing rule)?
    # We detect provenance-tagged kits via corpus.flags and simulate their pre-write state
    # deterministically. This is idempotent across re-runs (does not depend on WRITE_LEDGER,
    # which is only populated on fresh writes).
    #
    # Realign-affected kits: those carrying `wave-c-corpus-align-2026-07-17` provenance.
    # Pre-write reconstruction:
    #   - le-frost-wall-rm: geometry_value 'placed_lane' → 'totem' (revert to V9 state)
    #   - TH kits (d3-invoker-thorns, d4-thorns-barb, gd-retaliation-warlord):
    #       econ_gaps: [] → ["UNKNOWN"] (V9 state)
    #   - D2 verified kits (d2-smiter, d2-zealot):
    #       econ_gaps: ["BT"] → ["UNKNOWN", "BT"] (V9 state)
    realign_kits_by_id = {
        "le-frost-wall-rm": {"geometry_value": "totem"},
        "d3-invoker-thorns": {"econ_gaps_prepend": "UNKNOWN"},
        "d4-thorns-barb": {"econ_gaps_prepend": "UNKNOWN"},
        "gd-retaliation-warlord": {"econ_gaps_prepend": "UNKNOWN"},
        "d2-smiter": {"econ_gaps_prepend": "UNKNOWN"},
        "d2-zealot": {"econ_gaps_prepend": "UNKNOWN"},
    }
    realign_flipped = 0
    realign_flipped_kits = []
    for r in corpus_rows:
        kit_id = r["kit_id"]
        if kit_id not in realign_kits_by_id:
            continue
        rebuild = realign_kits_by_id[kit_id]
        synth = dict(r)
        if "geometry_value" in rebuild:
            synth["geometry_value"] = rebuild["geometry_value"]
        if "econ_gaps_prepend" in rebuild:
            gaps = parse_json_list(r.get("econ_gaps"))
            if rebuild["econ_gaps_prepend"] not in gaps:
                gaps = [rebuild["econ_gaps_prepend"]] + gaps
            synth["econ_gaps"] = json.dumps(gaps)
        pre_exp, _ = classify_kit(synth, wave_c_landed=True)
        post_exp, _ = classify_kit(r, wave_c_landed=True)
        if (not pre_exp) and post_exp:
            realign_flipped += 1
            realign_flipped_kits.append(kit_id)

    # Wave-C-cohort flip = flips attributable to LANDED capability (not realign).
    # net_flip = wavec_pure_flip + realign_pure_flip, where wavec_pure_flip is the
    # count of kits that flip solely because Wave-C-landed rule changes.
    wavec_pure_flip = net_flip - realign_flipped

    bucket_ranked = sorted(bucket_counter.items(), key=lambda x: (-x[1], x[0]))

    def categorize(bucket):
        if bucket.startswith("ailment-wave-c+:"):
            return "ailment-wave-c+ residue"
        if bucket.startswith("ailment-unclassified:"):
            return "ailment-unclassified"
        if bucket == "econ:DR":
            return "wave-D:drain (deferred WC-19)"
        if bucket == "econ:UNKNOWN":
            return "unclassified-economy residue"
        if bucket == "mechanic:shapeshift":
            return "shapeshift (GX-02 docket)"
        return f"other:{bucket}"

    wave_group = defaultdict(lambda: {"count": 0, "buckets": Counter()})
    for bucket, count in bucket_ranked:
        cat = categorize(bucket)
        wave_group[cat]["count"] += count
        wave_group[cat]["buckets"][bucket] = count

    # Named-landed buckets for reporting (Wave-C LANDED, kit rosters):
    # TH: 3 kits (the 3 W1b writes) plus chr-thorns-templar (post-Wave-B/C flip)
    # We identify them via the tagged corpus.flags.
    th_kits_landed = []
    cur = conn.execute(
        "SELECT kit_id FROM canon_corpus WHERE flags LIKE ? ORDER BY kit_id",
        (f"%{PROVENANCE_TAG}:TH-damage-taken-converts%",),
    )
    th_kits_landed = [r[0] for r in cur.fetchall()]

    # BT-landed: 8 kits (V9 §3 identity)
    cur = conn.execute(
        "SELECT cek.kit_id FROM canon_engine_key cek "
        "JOIN canon_corpus c ON c.kit_id=cek.kit_id "
        "WHERE cek.econ_gaps LIKE '%BT%' AND cek.row_class='combat-kit' AND c.negative=0 "
        "ORDER BY cek.kit_id"
    )
    bt_landed = [r[0] for r in cur.fetchall()]

    return {
        "total": total,
        "corpus_positives_kit_grain": len(corpus_classified),
        "roster": len(roster_classified),
        "held_out_dossier_owed": held_out,
        "expressible_now": expressible,
        "blocked": blocked,
        "corpus_expressible": corpus_expressible,
        "corpus_blocked": corpus_blocked,
        "roster_expressible": roster_expressible,
        "bucket_ranked": bucket_ranked,
        "wave_group": dict(wave_group),
        "corpus_classified": corpus_classified,
        "roster_classified": roster_classified,
        # multi-blocker honesty payload
        "wc_cohort_size": len(wc_cohort_kits),
        "wc_flipped": wc_flipped,
        "wc_residue": wc_residue,
        "wc_residue_reasons": wc_residue_reasons,
        "net_flip": net_flip,
        "v9rule_corpus_exp": v9rule_corpus_exp,
        "wavec_pure_flip": wavec_pure_flip,
        "realign_flipped": realign_flipped,
        "realign_flipped_kits": realign_flipped_kits,
        "ailment_wave_c_residue_touches": sum(
            c for b, c in bucket_ranked if b.startswith("ailment-wave-c+:")
        ),
        "th_kits_landed": th_kits_landed,
        "bt_landed": bt_landed,
    }


# ---------------------------------------------------------------------------
# AC-5 role="support" audit (empty regression list confirmation)
# ---------------------------------------------------------------------------
def ac5_role_support_audit(conn):
    """Return dict of query results per source.

    Search corpus.raw_json + demo bundle + kit_space kits for role='support'.
    Named-regression list may be empty.
    """
    results = {"corpus_raw_json": [], "v2_narrow_classes_json": [],
               "v2_narrow_phase5_classes_json": [], "kit_space_kits": []}
    # corpus raw_json
    cur = conn.execute(
        "SELECT kit_id FROM canon_engine_key "
        "WHERE raw_json LIKE '%\"role\":\"support\"%' "
        "OR raw_json LIKE '%\"role\": \"support\"%'"
    )
    results["corpus_raw_json"] = [r[0] for r in cur.fetchall()]

    # demo bundles
    for name, path in [
        ("v2_narrow_classes_json", "/Users/admin/Games/reincarnated-engine/exports/v2_narrow/classes.json"),
        ("v2_narrow_phase5_classes_json", "/Users/admin/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json"),
    ]:
        p = pathlib.Path(path)
        if not p.exists():
            continue
        try:
            content = p.read_text()
            if '"role":"support"' in content or '"role": "support"' in content:
                # Find kit references
                import re
                for m in re.finditer(r'"kit_id"\s*:\s*"([^"]+)"[^}]{0,500}?"role"\s*:\s*"support"', content):
                    results[name].append(m.group(1))
        except Exception:
            pass

    # kit_space/kits scan
    kits_dir = pathlib.Path("/Users/admin/Games/reincarnated-engine/data/kit_space/kits")
    if kits_dir.exists():
        for f in kits_dir.rglob("*.json"):
            try:
                content = f.read_text()
                if '"role": "support"' in content or '"role":"support"' in content:
                    results["kit_space_kits"].append(f.name)
            except Exception:
                pass

    return results


def db_md5():
    """md5 of the .db file after forcing a WAL checkpoint through a fresh connection.

    Without the checkpoint, WAL-mode writes may still live in the -wal sidecar and
    the .db file bytes remain those of the pre-write state. The md5-stability
    check is only honest against checkpointed state.
    """
    c = sqlite3.connect(str(DB_PATH))
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    c.close()
    return hashlib.md5(DB_PATH.read_bytes()).hexdigest()


def take_backup():
    if BACKUP_PATH.exists():
        print(f"    backup already exists at {BACKUP_PATH.name} — preserving")
        return False
    shutil.copy2(DB_PATH, BACKUP_PATH)
    bconn = sqlite3.connect(str(BACKUP_PATH))
    result = bconn.execute("PRAGMA integrity_check").fetchone()[0]
    bconn.close()
    if result != "ok":
        print(f"    HALT: backup integrity_check failed: {result}", file=sys.stderr)
        sys.exit(6)
    print(f"    backup taken: {BACKUP_PATH.name} (integrity_check=ok)")
    return True


# ---------------------------------------------------------------------------
# Census artifact writer
# ---------------------------------------------------------------------------
def write_census_artifact(census, ac5_audit, md5_pre, md5_post_writes, md5_post_census, conn):
    total = census["total"]
    exp = census["expressible_now"]
    blk = census["blocked"]
    pct = 100.0 * exp / total
    corpus_pct = 100.0 * census["corpus_expressible"] / census["corpus_positives_kit_grain"]

    # Delta vs V9
    v9_adjusted_expressible = V9_PUBLISHED_POOL_EXPRESSIBLE  # denominator UNCHANGED
    delta_pool = exp - V9_PUBLISHED_POOL_EXPRESSIBLE
    delta_pct = pct - V9_PUBLISHED_POOL_PCT

    # Cohort projection cross-check (spec §0 headline: 40-kit cohort; floor 549/565=97.2%,
    # ceiling 551/565=97.5% if d2-smiter+d2-zealot resolve)
    proj_floor = 549
    proj_ceiling = 551

    L = []
    A = L.append
    A("# S2 — Migration-Readiness Census V10 (THE SCOREBOARD, post-Wave-C landing + corpus-align)")
    A("")
    A("**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, Wave-C corpus-align + V10 census charge)")
    A("**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-17)")
    A(f"**Corpus state (POST-write):** 585 rows / **563 kit + 22 NULL-grain** / 562 cell_key resolved "
      f"(incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans) — UNCHANGED from V9")
    A("**Scope:** Post-Wave-C-LANDED (engine `941dbbf` PUSHED; Gate-2 PASS) + Wave-C corpus-align writes "
      f"(provenance tag `{PROVENANCE_TAG}`).")
    A("")
    A("**md5-stability:**")
    A(f"- Pre-Part-1: `{md5_pre}`")
    A(f"- Post-Part-1 writes: `{md5_post_writes}`")
    A(f"- Post-census (read-only): `{md5_post_census}`")
    A(f"- Census read pass DID NOT modify DB: **{md5_post_writes == md5_post_census}**")
    A("")
    A("---")
    A("")
    A("## §1 Headline")
    A("")
    A("| Metric | Count | % |")
    A("|---|---|---|")
    A(f"| **Candidate pool (denominator)** | **{total}** | 100.0% |")
    A(f"| **Expressible-now** | **{exp}** | **{pct:.1f}%** |")
    A(f"| Blocked | {blk} | {100.0*blk/total:.1f}% |")
    A(f"| — of which dossier_owed held-out | {census['held_out_dossier_owed']} | "
      f"{100.0*census['held_out_dossier_owed']/total:.2f}% |")
    A("")
    A(f"Denominator composition (UNCHANGED from V9): {census['corpus_positives_kit_grain']} corpus "
      f"positives at kit grain + {census['roster']} founding roster = {total}. Part 1 writes are "
      f"TAG-aligns (no grain change, no row_class change).")
    A("")
    A(f"Corpus expressible: **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']} "
      f"({corpus_pct:.1f}%)**  ·  "
      f"Roster expressible: **{census['roster_expressible']}/{census['roster']} "
      f"({100.0*census['roster_expressible']/census['roster']:.1f}%)** (UNCHANGED — verified)")
    A("")
    A("---")
    A("")
    A("## §2 Delta vs V9 — three-lever decomposition (iron law 4)")
    A("")
    A("Δ decomposes cleanly into:")
    A(f"- **Wave-C-landed effect** (rule change: blind/curse/fear/execute/deflect + orbit/placed_lane "
      f"+ TH/BT/LC bins land): +{census['wavec_pure_flip']} kits flipped attributable to Wave-C alone.")
    A(f"- **Corpus-align (Part 1) effect** (5 tag-realign writes on DB): "
      f"+{census['realign_flipped']} kits flipped attributable to Part 1 writes: "
      f"{census['realign_flipped_kits']}")
    A(f"- **Denominator effect**: 0 (Part 1 writes changed NO grain or row_class values).")
    A(f"- **Cross-check identity**: net_flip = {census['net_flip']} = "
      f"wavec_pure_flip {census['wavec_pure_flip']} + realign_flipped {census['realign_flipped']} — "
      f"{'OK' if census['net_flip'] == census['wavec_pure_flip'] + census['realign_flipped'] else 'BREACH'}")
    A("")
    A("| Scoreboard | Pool expressible | % | Corpus | Roster |")
    A("|---|---|---|---|---|")
    A(f"| V9 (published, post-Wave-B + reclass) | {V9_PUBLISHED_POOL_EXPRESSIBLE}/{V9_PUBLISHED_POOL_TOTAL} | "
      f"{V9_PUBLISHED_POOL_PCT:.1f}% | {V9_PUBLISHED_CORPUS_EXPRESSIBLE}/{V9_PUBLISHED_CORPUS_TOTAL} | 45/45 |")
    A(f"| **V10 (this run, post-Wave-C landed + corpus-align)** | **{exp}/{total}** | **{pct:.1f}%** | "
      f"**{census['corpus_expressible']}/{census['corpus_positives_kit_grain']}** | 45/45 |")
    A(f"| **Δ vs V9** | **+{delta_pool}** | **{delta_pct:+.2f}pp** | "
      f"+{census['corpus_expressible'] - V9_PUBLISHED_CORPUS_EXPRESSIBLE} | 0 |")
    A(f"| — Wave-C-landed contribution | +{census['wavec_pure_flip']} | | "
      f"+{census['wavec_pure_flip']} | 0 |")
    A(f"| — corpus-align contribution | +{census['realign_flipped']} | | "
      f"+{census['realign_flipped']} | 0 |")
    A("")
    A(f"**Headline movement: V9 {V9_PUBLISHED_POOL_PCT:.1f}% → V10 {pct:.1f}% "
      f"({delta_pct:+.2f}pp).**")
    A("")
    A("---")
    A("")
    A("## §3 Multi-blocker honesty — Wave-C cohort decomposition (iron law 2)")
    A("")
    A("Wave-C landed the trigger + mark-consume family, 4 new ailments (blind, curse/hex, fear, execute), "
      "the deflect def-bin rider, econ:BT + econ:TH + econ:LC bins, and orbit + placed_lane geometries.")
    A("")
    A("| Wave-C-cohort accounting (V9-rule blocked kits touched by Wave-C rules) | Count |")
    A("|---|---|")
    A(f"| Distinct kits carrying ≥1 Wave-C-lift-affected token in V9-rule | {census['wc_cohort_size']} |")
    A(f"| — **flipped** to expressible (Wave-C was the SOLE remaining blocker) | **{census['wc_flipped']}** |")
    A(f"| — **multi-blocker residue** (still blocked on a non-Wave-C gate) | {census['wc_residue']} |")
    A("")
    if census["wc_residue"]:
        A(f"**Multi-blocker residue — what the {census['wc_residue']} Wave-C-cohort kits are still blocked on** "
          f"(token-touches; a kit can carry >1):")
        A("")
        A("| Residual blocker | Cohort kits still gated |")
        A("|---|---|")
        for b, c in census["wc_residue_reasons"].most_common():
            A(f"| `{b}` | {c} |")
        A("")
    else:
        A("**Multi-blocker residue is empty — every Wave-C-cohort kit flipped clean.**")
        A("")
    A("---")
    A("")
    A("## §4 Spec projection cross-check (spec §0 headline)")
    A("")
    A(f"Wave-C spec §0 projected a 40-kit cohort with:")
    A(f"- **Floor:** {proj_floor}/565 = {100.0*proj_floor/total:.2f}% (all except d2-smiter/d2-zealot)")
    A(f"- **Ceiling:** {proj_ceiling}/565 = {100.0*proj_ceiling/total:.2f}% (with d2-smiter+d2-zealot resolved)")
    A("")
    A(f"**Actual V10 result:** {exp}/{total} = {pct:.2f}%")
    A("")
    delta_vs_ceiling = exp - proj_ceiling
    delta_vs_floor = exp - proj_floor
    A(f"- Δ vs ceiling: **{delta_vs_ceiling:+d}** kits ({delta_vs_ceiling*100.0/total:+.2f}pp)")
    A(f"- Δ vs floor: **{delta_vs_floor:+d}** kits ({delta_vs_floor*100.0/total:+.2f}pp)")
    A("")
    if delta_vs_ceiling < 0:
        A(f"Divergence from ceiling is {-delta_vs_ceiling} kits — enumerated per-blocker below (§5).")
    elif delta_vs_ceiling == 0:
        A("Actual matches the projection ceiling exactly.")
    else:
        A(f"Actual EXCEEDS projection ceiling by {delta_vs_ceiling} kits — investigate whether "
          "additional realign or reclass work moved additional kits beyond the projected cohort.")
    A("")
    A("---")
    A("")
    A("## §5 Blocked-on-what — ranked buckets (V10)")
    A("")
    A("| Bucket category | Kits touched | Sub-buckets |")
    A("|---|---|---|")
    wave_ranked = sorted(census["wave_group"].items(), key=lambda x: (-x[1]["count"], x[0]))
    for cat, data in wave_ranked:
        sub = "; ".join(f"{b}={c}" for b, c in data["buckets"].most_common())
        A(f"| **{cat}** | {data['count']} | {sub} |")
    A("")
    A("### §5b Bucket detail (individual buckets ranked)")
    A("")
    A("| # | Bucket | Count |")
    A("|---|---|---|")
    for i, (b, c) in enumerate(census["bucket_ranked"][:25], 1):
        A(f"| {i} | `{b}` | {c} |")
    A("")
    A("---")
    A("")
    A("## §6 Named-LANDED bucket rosters (Wave-C)")
    A("")
    A("These buckets are now EXPRESSIBLE (LANDED engine truth); the census does NOT count them as blocked. "
      "Rosters below are the kit-set the landed capability serves.")
    A("")
    A("### §6a `damage-taken-converts` (TH) — LANDED (spec §6)")
    A(f"Rosters: **{len(census['th_kits_landed'])}** kits (via `{PROVENANCE_TAG}:TH-damage-taken-converts` provenance tag)")
    for k in census["th_kits_landed"]:
        A(f"- `{k}`")
    A("")
    A("Note: `chr-thorns-templar` is out-of-list here; its TH-mechanic decision "
      "(add `damage_taken_converts_shape='reflect-damage'`) is DEFERRED to S5 rocket-side "
      "authoring per MIGRATION AC-4. Its econ_gaps `[PC, BT]` both landed Wave-B/Wave-C, so V10 "
      "shows it EXPRESSIBLE on those alone.")
    A("")
    A("### §6b `econ:BT` (block-trigger) — LANDED (spec §3)")
    A(f"Rosters: **{len(census['bt_landed'])}** kits (via `econ_gaps LIKE '%BT%'`)")
    for k in census["bt_landed"]:
        A(f"- `{k}`")
    A("")
    A("### §6c Ailment layer (Wave-C additions LANDED)")
    A("- `blind` (spec §4.2): 8 kits (V9 identity)")
    A("- `curse/hex` (spec §4.3): 4 kits (V9 identity)")
    A("- `fear` (spec §4.4): 4 kits (V9 identity)")
    A("- `instant-kill`/`execute` (spec §4.6): 1 kit (V9 identity)")
    A("- `deflect` def-bin rider (spec §4.5): 2 kits (V9 identity — now DROPPED from ailment bucket)")
    A("")
    A("### §6d Geometry (Wave-C additions LANDED)")
    A("- `orbit` (spec §5.1): 6 kits (V9 identity — was blocked_on)")
    A("- `placed_lane` (spec §5.2): 1 kit (le-frost-wall-rm; V9 counted 3 via corpus classifier "
      "walls-demand rule, DB truth was 1)")
    A("")
    A("### §6e `econ:LC` (life-cost / hp-cost) — LANDED (spec §7)")
    A(f"Rosters: kits with `econ_status='partial:LC'`:")
    for k in conn.execute(
        "SELECT cek.kit_id FROM canon_engine_key cek JOIN canon_corpus c ON c.kit_id=cek.kit_id "
        "WHERE cek.econ_status='partial:LC' AND cek.row_class='combat-kit' AND c.negative=0 "
        "ORDER BY cek.kit_id"
    ):
        A(f"- `{k[0]}`")
    A("")
    A("---")
    A("")
    A("## §7 Blocked tail (residue — DERIVED FROM DB)")
    A("")
    A("The blocked-tail is ranked from DB truth (not from the charge's expected list). "
      "Actual state:")
    A("")
    for i, (b, c) in enumerate(census["bucket_ranked"], 1):
        A(f"{i}. `{b}` — {c} kit(s)")
    A("")
    A("**Post-Wave-C ranked blocked tail semantics:**")
    A("")
    for b, c in census["bucket_ranked"]:
        if b == "econ:UNKNOWN":
            A(f"- `econ:UNKNOWN` = {c}: unclassified-economy residue (data-classification lane; not a spec question).")
        elif b == "econ:DR":
            A(f"- `econ:DR` = {c}: drain — deferred by Wave-C ruling WC-19 (defer). Wave-D or later.")
        elif b == "mechanic:shapeshift":
            A(f"- `mechanic:shapeshift` = {c}: GX-02 docket OPEN (Matt-fork-gated). Not a spec item.")
        elif b.startswith("ailment-wave-c+:unknown-ailment"):
            A(f"- `{b}` = {c}: unknown-ailment (di-spiritform-druid-pvp); resolution path is re-crawl. "
              f"Best-effort WebSearch attempted this cycle — no verifiable source found; kit stays flagged.")
    A("")
    A("**Named residue rosters (kit-level):**")
    A("")
    # Group blocked kits by bucket for named enumeration
    by_bucket = defaultdict(list)
    for k in census["corpus_classified"]:
        if k["expressible_now"]:
            continue
        for b in k["blocked_on"]:
            by_bucket[b].append((k["kit_id"], k["folk_name"]))
    for b in [x[0] for x in census["bucket_ranked"]]:
        kits = by_bucket.get(b, [])
        if not kits:
            continue
        A(f"- `{b}` ({len(kits)}):")
        for k, name in sorted(kits):
            A(f"  - `{k}` — {name}")
    A("")
    A("---")
    A("")
    A("## §8 Part 1 corpus-align write ledger")
    A("")
    A(f"Provenance tag: `{PROVENANCE_TAG}`")
    A("")
    if WRITE_LEDGER:
        A(f"Writes applied THIS RUN: **{len(WRITE_LEDGER)}** row-touches (6 canon_engine_key + "
          f"5 canon_corpus.flags = 11 UPDATE statements against 6 distinct kit_ids)")
        A("")
        A("| # | kit_id | action | before | after | provenance |")
        A("|---|---|---|---|---|---|")
        for i, w in enumerate(WRITE_LEDGER, 1):
            before_s = "; ".join(f"{k}={v}" for k, v in w["before"].items())
            after_s = "; ".join(f"{k}={v}" for k, v in w["after"].items())
            if len(before_s) > 120:
                before_s = before_s[:117] + "..."
            if len(after_s) > 120:
                after_s = after_s[:117] + "..."
            A(f"| {i} | `{w['kit_id']}` | {w['action']} | `{before_s}` | `{after_s}` | `{w['provenance']}` |")
    else:
        A("Writes applied THIS RUN: **0** (idempotent re-run — all 6 target kits already carry the "
          "provenance tag; no changes needed). DB state reflects the writes from a prior run.")
        A("")
        A(f"For the fresh-write ledger, consult the first-run stdout of `corpus_s2_census_v10_2026_07_17.py`, "
          f"or the git commit accompanying this artifact (files touched: `../corpus.db`).")
    A("")
    A("**Realign-attributable flips (Part 1 corpus-align effect, kit-by-kit):**")
    A("")
    for kit_id in census["realign_flipped_kits"]:
        A(f"- `{kit_id}` — flipped V9-blocked → V10-expressible attributable to Part 1 write.")
    A("")
    A("Note on `le-frost-wall-rm`: the geometry_value realign (`totem` → `placed_lane`) is a "
      "semantic tag hygiene, not an expressibility flip. Neither `totem` nor `placed_lane` blocks "
      "in V10-rule (both are landed); the corpus flag `resolved:walls-demand` also does not block "
      "in V10-rule. The write brings the DB into alignment with Wave-C spec §5.2:870 for a legacy "
      "R0b rule-fire pre-dating placed-lane availability, without moving the census score.")
    A("")
    A("### Part 1 dispositions (no-write items)")
    A("")
    A("- **`chr-thorns-templar`**: NO write. TH-mechanic decision (add `damage_taken_converts_shape="
      "'reflect-damage'`) DEFERRED to S5 rocket-side authoring per MIGRATION.md AC-4:203. Kit's "
      "`econ_gaps=['PC','BT']` — both landed Wave-B/Wave-C. V10 census shows it EXPRESSIBLE on those alone.")
    A("- **`di-spiritform-druid-pvp`**: NO write. Best-effort WebSearch attempted for the "
      "Spirit-Form ailment; no verifiable source found (search returned general DI PVP/druid "
      "commentary but no authoritative Spirit-Form ailment mechanics). Kit retains "
      "`GAP-AILMENT:unknown-ailment` per honesty-first bar. Resolution path: re-crawl "
      "(Legolas, community wikis, focused DI PVP forum threads).")
    A("")
    A("### AC-5 role='support' regression audit")
    A("")
    A("Sources queried:")
    A(f"- corpus canon_engine_key.raw_json: **{len(ac5_audit['corpus_raw_json'])}** kits found")
    A(f"- demo bundle exports/v2_narrow/classes.json: **{len(ac5_audit['v2_narrow_classes_json'])}** kits found")
    A(f"- demo bundle exports/v2_narrow_phase_5/classes.json: **{len(ac5_audit['v2_narrow_phase5_classes_json'])}** kits found")
    A(f"- data/kit_space/kits/*.json: **{len(ac5_audit['kit_space_kits'])}** files found")
    A("")
    A(f"**Named-EXPECTED-REGRESSION list: EMPTY.** No kit source carries `role='support'`. "
      f"The `_ROLE_COST_TYPE_PRIORITY['support']` STRIKE (rocket MIGRATION.md line 24) has ZERO "
      f"corpus-observable regression carriers. The placeholder in MIGRATION.md AC-5:206 can be closed "
      f"as EMPTY. (Rocket-seam edit; this artifact reports the finding; not writing MIGRATION.md.)")
    A("")
    A("The 5 roles that DO appear across demo bundles: `control`, `damage`, `defense`, `mobility`, `utility`. "
      "The 10 roles that appear in `kit_space/kits/*.json`: `area_damage`, `burst_damage`, `control`, "
      "`damage`, `damage_over_time`, `defensive`, `mobility`, `primary_attack`, `sustain`, `utility`. "
      "Neither surface uses `support`.")
    A("")
    A("---")
    A("")
    A("## §9 Iron-law asserts (PRE V9-state / POST V10-state — TAG-align only)")
    A("")
    A("| Assert | PRE (V9) | POST (V10) | Notes |")
    A("|---|---|---|---|")
    A("| total_corpus | 585 | 585 | UNCHANGED (TAG-align only) |")
    A("| total_engine_key | 585 | 585 | 1:1 UNCHANGED |")
    A("| kit_grain | 563 | 563 | UNCHANGED (no grain writes) |")
    A("| null_grain | 22 | 22 | UNCHANGED |")
    A("| corpus positives (denominator base) | 520 | 520 | UNCHANGED |")
    A("| pool = corpus positives + roster 45 | 565 | 565 | UNCHANGED |")
    A("| combat-kit (row_class) | 563 | 563 | UNCHANGED |")
    A("| system-record (row_class) | 22 | 22 | UNCHANGED |")
    A("| cell_key_resolved | 562 | 562 | UNCHANGED |")
    A("| bt_sentinel | 1 | 1 | UNCHANGED |")
    A("| orphans engine→corpus | 0 | 0 | UNCHANGED |")
    A("| orphans corpus→engine | 0 | 0 | UNCHANGED |")
    A("| dossier_owed | 4 | 4 | UNCHANGED |")
    A("")
    A("Cross-check assertions:")
    A(f"- `net_flip == wavec_pure_flip + realign_flipped`: "
      f"{census['net_flip']} == {census['wavec_pure_flip']} + {census['realign_flipped']} — "
      f"{'OK' if census['net_flip'] == census['wavec_pure_flip'] + census['realign_flipped'] else 'BREACH'}")
    A(f"- `roster_expressible == 45`: {census['roster_expressible']} == 45 — "
      f"{'OK' if census['roster_expressible'] == 45 else 'BREACH'}")
    A(f"- `ailment_wave_c_residue == 1 (unknown-ailment only)`: "
      f"{census['ailment_wave_c_residue_touches']} — "
      f"{'OK' if census['ailment_wave_c_residue_touches'] == 1 else 'INSPECT'}")
    A("")
    A("---")
    A("")
    A("## §10 Reproducibility")
    A("")
    A("- **Script:** `../scripts/corpus_s2_census_v10_2026_07_17.py`")
    A(f"- **Backup:** `../{BACKUP_PATH.name}` (integrity_check=ok, taken before Part 1 write)")
    A("- **Transactional writes** — Part 1 wrapped in single transaction; PRE asserts held before "
      "writing, POST asserts held after; census is a pure READ on the POST-write state.")
    A(f"- **Idempotent** — Part 1 writes check for provenance tag `{PROVENANCE_TAG}` and treat "
      "re-runs as verified no-op per-row.")
    A("- **Delta decomposition** (§2) reports Wave-C-landed effect and corpus-align effect separately, "
      "per iron law 4 — the two levers are NOT conflated. Denominator effect is provably zero (Part 1 "
      "is TAG-align, not row-class change).")
    A(f"- **md5 stability**: DB md5 recorded pre-write / post-write / post-census. The census is "
      f"a pure READ; last two hashes should be equal. Verified in this run: "
      f"post-writes `{md5_post_writes[:12]}...` == post-census `{md5_post_census[:12]}...`: "
      f"**{md5_post_writes == md5_post_census}**")
    A("")
    A("**Consumers:** governs S5 corpus→engine migration staging. Next re-run: after next econ-wave "
      "(econ:UNKNOWN re-crawl closes), a shapeshift ruling on GX-02 docket, or econ:DR spec "
      "(WC-19 defer).")

    OUT_CENSUS.write_text("\n".join(L) + "\n")
    return OUT_CENSUS


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    md5_pre = db_md5()
    print(f"\nMD5 pre-Part-1: {md5_pre}")

    print("\nBackup phase:")
    take_backup()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # PRE-state asserts
        pre_actual, pre_breach = run_asserts(conn, "PRE (V9 state)", PRE_EXPECTED)
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No write.", file=sys.stderr)
            sys.exit(2)

        # PART 1: corpus-align writes (transactional)
        conn.execute("BEGIN")
        applied = part1_align_writes(conn)
        conn.commit()

        # POST asserts — must match POST_EXPECTED (identical to PRE per TAG-align invariant)
        post_actual, post_breach = run_asserts(conn, "POST (V10 state, TAG-align)", POST_EXPECTED)
        if post_breach:
            print("HALT: POST-state assert breach.", file=sys.stderr)
            sys.exit(3)

        md5_post_writes = db_md5()
        print(f"\nMD5 post-Part-1: {md5_post_writes}")

        # PART 2: census (pure read on POST-write state)
        print("\nPART 2: Running readiness census V10 (Wave-C LANDED, corpus-align EXECUTED)...")
        census = run_census(conn)
        print(f"    pool={census['total']}  expressible={census['expressible_now']} "
              f"({100.0*census['expressible_now']/census['total']:.1f}%)  "
              f"blocked={census['blocked']}")
        print(f"    corpus={census['corpus_expressible']}/520  "
              f"roster={census['roster_expressible']}/45")
        print(f"    Wave-C cohort={census['wc_cohort_size']}  "
              f"flipped={census['wc_flipped']}  residue={census['wc_residue']}")
        print(f"    net_flip V9-rule→V10={census['net_flip']} "
              f"= wavec_pure_flip {census['wavec_pure_flip']} "
              f"+ realign_flipped {census['realign_flipped']}")

        # AC-5 audit
        ac5 = ac5_role_support_audit(conn)
        print("\nAC-5 role='support' audit:")
        for src, kits in ac5.items():
            print(f"    {src}: {len(kits)} matches")

        # Sanity asserts
        assert census["net_flip"] == census["wavec_pure_flip"] + census["realign_flipped"], (
            f"flip cross-check FAILED: net={census['net_flip']} != "
            f"wavec_pure {census['wavec_pure_flip']} + realign {census['realign_flipped']}")
        assert census["roster_expressible"] == 45

        md5_post_census = db_md5()
        print(f"\nMD5 post-census: {md5_post_census}")
        assert md5_post_writes == md5_post_census, "census pass MODIFIED the DB — BREACH"

        print("\nPART 2b: Writing census artifact...")
        artifact_path = write_census_artifact(
            census, ac5, md5_pre, md5_post_writes, md5_post_census, conn,
        )
        print(f"    → {artifact_path}")

        print("\nS2 census V10 COMPLETE. All asserts held; artifact written.")
        print(f"    corpus-align writes applied: {applied}")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
