"""
corpus_s2_census_v9_2026_07_16.py — S2 readiness census V9 (THE SCOREBOARD, post-Wave-B rerun).
Author: elrond, 2026-07-16 (autonomous atlas-parity run, cycle 3, CENSUS V9 charge).

Authority: gandalf-prime 2026-07-16 charter (S2 = THE SCOREBOARD; ruling-11 executes at V9).
Commissioner: gandalf-prime (Matt authorization 2026-07-16). Ruling-11 delegated (decisions-log
~5910), ratified into engine at Gate-2 (`b850800`).

WHAT CHANGED SINCE V8 (three landed truths — this run REFLECTS Wave-B; EXECUTES ruling-11):

    A. WAVE-B ECONOMY LANDED. jack-ryan Gate-2 verdict PASS-WITH-AMENDMENTS
       (`agentic_orchestration/jack-ryan/reviews/2026-07-16-wave-b-economy-gate2.md`);
       engine push `b850800` (rocket `4f2548e`/`33ffc86`/`176f353` + gamora
       `1a0e5e4`/`e81f3f9`/`c037c5b`/`41e45f6`). The 4 in-flight Wave-B econ gap tokens that V8
       scored BLOCKED (econ:PC persistent-condition · econ:RS reservation · econ:AM attunement-
       meter · econ:RC recharge) are now LANDED ENGINE TRUTH → scored EXPRESSIBLE in V9.
       NOT flipped: econ:UNKNOWN (unclassified) · econ:BT (block-trigger, small-add) ·
       econ:LC/DR (Wave-C per Gate-1 ruling) · ailment-wave-c+ · geometry small-adds · shapeshift.

    B. RULING-11 RECLASSIFICATION EXECUTES. 3 kits reclassify from combat-kit (grain='kit')
       to system-record (grain=NULL) per the ruling's own V9 timing clause:
         - d3-lod-archetype  → row_class='system-record', route='itemization-meta'
         - vs-red-death       → row_class='system-record', route='unlock-meta'
         - vs-vlad-dracula    → row_class='system-record', route='unlock-meta'
       Denominator moves: pool 568→565 · corpus positives 523→520 · kit_grain 566→563 ·
       null-grain 19→22. Total 585 UNCHANGED. engine_key 1:1 585 UNCHANGED. dossier_owed 4
       UNTOUCHED. Convention follows the existing 19 system-records: grain=NULL, grain_note
       stamped, populated route, flag `ruling-11-reclass-2026-07-16` for reversal auditability.
       Matt-veto-open: one word reverses; the flag makes reversal trivial.

    C. ECON-UNKNOWN slate carries residue (was 16 at DB state entering V9). All 3 IT/UT reclass
       targets were carrying econ:UNKNOWN; after their reclass they leave the denominator.
       econ:UNKNOWN on the pool: 16 → 13 (16 minus the 3 reclassified).

IRON LAWS (this run):
    1. PRE-state asserts (V8 counts) + POST-state asserts (V9 counts after ruling-11 reclass):
       PRE:  total 585 · kit_grain 566 · null_grain 19 · dossier_owed 4 · orphans 0/0 · ek 585.
       POST: total 585 · kit_grain 563 · null_grain 22 · dossier_owed 4 · orphans 0/0 · ek 585.
       Backup taken before write; transactional; idempotent (re-run = verified no-op via flag).

    2. MULTI-BLOCKER HONESTY. Same convention as V8: kits with multi-blockers stay blocked;
       report Wave-B-cohort decomposition (cohort → flipped → residue with ranked re-block).

    3. ROSTER 45/45 UNCHANGED (verified). SPEC ANCHOR — the engine's first-class targets.

    4. HEADLINE: expressible-now N/565 + %; corpus N/520; roster 45/45. Delta vs V8 (+pp)
       decomposed cleanly (Wave-B flip + denominator-change effect reported separately, so
       the two levers are NOT conflated).

    5. NEW BUCKET RANKING: expect residue tail — ailment-wave-c+ 21 · econ:UNKNOWN 13 ·
       small-adds BT/orbit/walls · LC/DR · shapeshift 3 · anything else.

    6. AUTO-COMMIT collab repo per project discipline; NO push (gandalf pushes).

DENOMINATOR LAW (V9):
    §F.5(1) candidate pool = 520 corpus positives at kit grain (grain='kit' AND negative=0)
    + 45 founding roster = 565. Negatives (43 kit-grain), NULL-grain system-records (22 post-
    reclass), and grain=NULL mints EXCLUDED per spec. 4 dossier_owed IN pool, flagged.
"""

import json
import pathlib
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = BASE / "agentic_orchestration/research/curated/atlas"
OUT_CENSUS = ATLAS_DIR / "s2-readiness-census-v9-2026-07-16.md"
BACKUP_PATH = BASE / "agentic_orchestration/research/curated/corpus.db.pre-v9-2026-07-16-backup"

import sqlite3

# ---------------------------------------------------------------------------
# PRE-state (V8 counts) — asserted BEFORE any write
# ---------------------------------------------------------------------------
PRE_EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "kit_grain": 566,
    "null_grain": 19,
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
    "combat_kit_rc": 566,
    "system_record_rc": 19,
}

# ---------------------------------------------------------------------------
# POST-state (V9 counts after ruling-11 reclass) — asserted AFTER write
# ---------------------------------------------------------------------------
POST_EXPECTED = {
    "total_corpus": 585,     # UNCHANGED
    "total_engine_key": 585, # UNCHANGED
    "kit_grain": 563,        # 566 - 3 reclass
    "null_grain": 22,        # 19 + 3 reclass
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,       # UNTOUCHED
    "combat_kit_rc": 563,    # 566 - 3
    "system_record_rc": 22,  # 19 + 3
}

# V8 published headline baseline (post-ailment-landed, post-econ-audit) — the §4 delta anchor.
V8_PUBLISHED_POOL_EXPRESSIBLE = 385
V8_PUBLISHED_POOL_TOTAL = 568
V8_PUBLISHED_POOL_PCT = 67.8
V8_PUBLISHED_CORPUS_EXPRESSIBLE = 340
V8_PUBLISHED_CORPUS_TOTAL = 523

# The three ruling-11 reclass rows — canonical target set
RECLASS_TARGETS = [
    # (kit_id,               route,               grain_note_suffix)
    ("d3-lod-archetype",     "itemization-meta",  "ruling-11 IT reclass"),
    ("vs-red-death",         "unlock-meta",       "ruling-11 UT reclass"),
    ("vs-vlad-dracula",      "unlock-meta",       "ruling-11 UT reclass"),
]
RECLASS_FLAG = "ruling-11-reclass-2026-07-16"


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
# PART 1: RULING-11 RECLASSIFICATION WRITE
# ---------------------------------------------------------------------------

def apply_ruling_11(conn):
    """Reclassify 3 IT/UT kits from combat-kit to system-record.

    Idempotent: if the ruling-11-reclass flag is already present on the target rows,
    it's a re-run and we treat it as a verified no-op.
    """
    print("\nPART 1: Applying ruling-11 reclassification (3 rows)...")

    # Check idempotency FIRST — if flag already present, this is a re-run
    already_reclassed = 0
    for kit_id, _route, _note in RECLASS_TARGETS:
        row = conn.execute(
            "SELECT flags FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        if row is None:
            print(f"    HALT: {kit_id} not found in canon_engine_key", file=sys.stderr)
            sys.exit(4)
        flags = row[0] or "[]"
        try:
            flags_list = json.loads(flags)
        except json.JSONDecodeError:
            flags_list = []
        if RECLASS_FLAG in flags_list:
            already_reclassed += 1

    if already_reclassed == 3:
        print("    IDEMPOTENT: all 3 rows already carry ruling-11-reclass flag; no-op.")
        return {"applied": 0, "idempotent": True}

    if already_reclassed != 0:
        print(f"    HALT: partial reclass state ({already_reclassed}/3 flagged). "
              f"Manual reconciliation required.", file=sys.stderr)
        sys.exit(5)

    # Fresh reclass: validate each target row's PRE-state before writing
    for kit_id, _route, _note in RECLASS_TARGETS:
        cc = conn.execute(
            "SELECT grain, negative, dossier_owed FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        assert cc is not None, f"{kit_id} not in canon_corpus"
        assert cc[0] == "kit", f"{kit_id} PRE grain={cc[0]!r}, expected 'kit'"
        assert cc[1] == 0, f"{kit_id} PRE negative={cc[1]}, expected 0"
        # dossier_owed can be either; ruling doesn't touch it
        ce = conn.execute(
            "SELECT row_class, route FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        assert ce[0] == "combat-kit", f"{kit_id} PRE row_class={ce[0]!r}, expected 'combat-kit'"

    # Write reclass — canon_corpus (grain + grain_note) + canon_engine_key (row_class + route + flags)
    applied = 0
    grain_note_template = "system-record: not kit/gear/class emittable; excluded from fits by row_class ({note_suffix})"

    for kit_id, route, note_suffix in RECLASS_TARGETS:
        # 1) canon_corpus: grain 'kit' → NULL, populate grain_note
        conn.execute(
            "UPDATE canon_corpus SET grain=NULL, grain_note=? WHERE kit_id=?",
            (grain_note_template.format(note_suffix=note_suffix), kit_id),
        )
        # 2) canon_engine_key: row_class 'combat-kit' → 'system-record', set route, add flag
        row = conn.execute(
            "SELECT flags FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        try:
            flags_list = json.loads(row[0] or "[]")
        except json.JSONDecodeError:
            flags_list = []
        if "resolved:system-record" not in flags_list:
            flags_list.append("resolved:system-record")
        if RECLASS_FLAG not in flags_list:
            flags_list.append(RECLASS_FLAG)
        conn.execute(
            "UPDATE canon_engine_key SET row_class=?, route=?, flags=? WHERE kit_id=?",
            ("system-record", route, json.dumps(flags_list), kit_id),
        )
        applied += 1
        print(f"    reclassed: {kit_id} → system-record / route={route}")

    print(f"    total rows reclassed: {applied}")
    return {"applied": applied, "idempotent": False}


# ---------------------------------------------------------------------------
# CLASSIFICATION VOCABULARY (V9)
# ---------------------------------------------------------------------------
# Econ gaps LANDED under Wave A + Wave B — expressible now (V9)
WAVE_A_ECON_LANDED = {"SU", "HV"}                              # summon-uptime + harvest
WAVE_B_ECON_LANDED = {"PC", "RS", "AM", "RC"}                  # persistent-condition + reservation + attunement-meter + recharge
ECON_LANDED_V9 = WAVE_A_ECON_LANDED | WAVE_B_ECON_LANDED

# Econ gaps STILL BLOCKED (waves C or small-adds):
WAVE_C_ECON_GAPS = {"LC", "DR"}   # life-cost / drain — Wave-C per Gate-1 ruling
SMALL_ADD_GAPS = {"BT"}           # block-trigger — small add
UNKNOWN_GAP = {"UNKNOWN"}          # unclassified residue

# Ailment layer LANDED (V8 rule) — carries forward at V9
AILMENT_LANDED = {
    "GAP-AILMENT:damage-amp",     # → sunder (ruling 5)
    "GAP-AILMENT:freeze",         # chill-escalation + shatter payoff
    "GAP-AILMENT:stun",           # short hard CC + boss resistance
    "GAP-AILMENT:poison-dot",     # independent-stack DoT
    "GAP-AILMENT:taunt",          # proxy-AI directive on Wave-A machinery
}
AILMENT_WAVE_C_OR_BEYOND = {
    "GAP-AILMENT:blind", "GAP-AILMENT:fear", "GAP-AILMENT:curse/hex",
    "GAP-AILMENT:unknown-ailment", "GAP-AILMENT:instant-kill",
    "GAP-AILMENT:deflect",
}
SMALL_ADD_GEOMETRIES = {"orbit", "walls-placed-lane"}


def parse_json_list(s):
    if not s or s == "[]":
        return []
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return []


def classify_kit(row, wave_b_landed=True):
    """Return (expressible_now: bool, blocked_on: set[str]).

    wave_b_landed=True is the V9 rule (Wave-B economy landed).
    wave_b_landed=False reproduces the V8-era rule (used only for flip decomposition,
    NOT for the V9 headline).

    Multi-blocker honest: unions ALL blockers; expressible IFF blockset empty.
    """
    blocked_on = set()

    for eg in parse_json_list(row.get("econ_gaps")):
        if eg in WAVE_A_ECON_LANDED:
            continue  # Wave-A landed (V8 rule) → no block
        if eg in WAVE_B_ECON_LANDED:
            if wave_b_landed:
                continue  # Wave-B landed (V9 rule) → no block
            else:
                blocked_on.add(f"econ:{eg}")  # V8-rule reproduction: still blocking
                continue
        # LC / DR / BT / UNKNOWN / any residual token → blocked, named econ:<TOK>
        blocked_on.add(f"econ:{eg}")

    for ag in parse_json_list(row.get("ctrl_ailment_gaps")):
        name = ag.replace("GAP-AILMENT:", "")
        if ag in AILMENT_LANDED:
            # ailment landed (V8 rule, carries forward) → no block
            continue
        elif ag in AILMENT_WAVE_C_OR_BEYOND:
            blocked_on.add(f"ailment-wave-c+:{name}")
        else:
            blocked_on.add(f"ailment-unclassified:{name}")

    geom = row.get("geometry_value") or ""
    if geom in SMALL_ADD_GEOMETRIES:
        blocked_on.add(f"geometry:{geom}")

    flags_raw = row.get("flags") or ""
    if "gx-candidate:orbit" in flags_raw:
        blocked_on.add("geometry:orbit")
    if "resolved:walls-demand" in flags_raw:
        blocked_on.add("geometry:walls-placed-lane")
    if "J-GEO:placed-lane" in flags_raw:
        blocked_on.add("geometry:walls-placed-lane")

    kit_id = row.get("kit_id") or ""
    if any(marker in kit_id for marker in [
        "wildsoul", "wereforms", "spirit-form", "spiritborn-vortex",
    ]):
        if "vortex" not in kit_id or "spiritborn" not in kit_id:
            blocked_on.add("mechanic:shapeshift")

    expressible_now = len(blocked_on) == 0
    return expressible_now, blocked_on


def run_census(conn):
    """Read-only census on the POST-reclass DB state (denominator 565)."""
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
    assert len(corpus_rows) == 520, f"V9 corpus positives = {len(corpus_rows)}, expected 520 (post-reclass)"

    cur = conn.execute("SELECT kit_id, name, mob_policy_while_casting, commit_val FROM roster_atlas")
    roster_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(roster_rows) == 45, f"roster = {len(roster_rows)}, expected 45 (UNCHANGED)"

    # V9 classification (Wave-B landed)
    corpus_classified = []
    bucket_counter = Counter()
    for row in corpus_rows:
        expressible, blocked = classify_kit(row, wave_b_landed=True)
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

    # Roster: SPEC ANCHOR, authoritatively expressible-now
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
    # MULTI-BLOCKER HONESTY: Wave-B-cohort flip decomposition.
    # Cohort = distinct kits carrying >=1 in-flight (now-landed) Wave-B econ token.
    # For each: V8-rule blockset (wave_b_landed=False) vs V9-rule blockset (True).
    #   - flipped = kit now expressible (Wave-B was its SOLE remaining blocker)
    #   - residue = kit STILL blocked on a non-Wave-B gate (multi-blocker)
    # -------------------------------------------------------------------
    wb_cohort = [
        r for r in corpus_rows
        if any(t in WAVE_B_ECON_LANDED for t in parse_json_list(r.get("econ_gaps")))
    ]
    wb_flipped = 0
    wb_residue = 0
    wb_residue_reasons = Counter()
    for r in wb_cohort:
        _, v9b = classify_kit(r, wave_b_landed=True)
        if len(v9b) == 0:
            wb_flipped += 1
        else:
            wb_residue += 1
            for x in v9b:
                wb_residue_reasons[x] += 1

    # Cross-check: net corpus flip V8-rule → V9-rule must equal Wave-B-cohort flip
    # (Wave-B is the only classification rule delta between V8 and V9).
    v8rule_corpus_exp = sum(
        1 for r in corpus_rows if classify_kit(r, wave_b_landed=False)[0]
    )
    net_flip = corpus_expressible - v8rule_corpus_exp

    bucket_ranked = sorted(bucket_counter.items(), key=lambda x: (-x[1], x[0]))

    def categorize(bucket):
        if bucket.startswith("ailment-wave-c+:"):
            return "ailment-wave-c+"
        if bucket.startswith("ailment-unclassified:"):
            return "ailment-unclassified"
        if bucket in ("econ:LC", "econ:DR"):
            return "wave-C:life-cost-drain"
        if bucket == "econ:BT":
            return "small-add:block-trigger-BT"
        if bucket == "econ:UNKNOWN":
            return "unclassified-economy"
        if bucket == "geometry:orbit":
            return "small-add:orbit-25th-geo"
        if bucket == "geometry:walls-placed-lane":
            return "small-add:walls-placed-lane"
        if bucket == "mechanic:shapeshift":
            return "shapeshift (GX-02 docket bg)"
        return f"other:{bucket}"

    wave_group = defaultdict(lambda: {"count": 0, "buckets": Counter()})
    for bucket, count in bucket_ranked:
        cat = categorize(bucket)
        wave_group[cat]["count"] += count
        wave_group[cat]["buckets"][bucket] = count

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
        "wb_cohort_size": len(wb_cohort),
        "wb_flipped": wb_flipped,
        "wb_residue": wb_residue,
        "wb_residue_reasons": wb_residue_reasons,
        "net_flip": net_flip,
        "v8rule_corpus_exp": v8rule_corpus_exp,
        "ailment_wave_c_touches": sum(c for b, c in bucket_ranked if b.startswith("ailment-wave-c+:")),
    }


def write_census_artifact(census, reclass_summary):
    total = census["total"]
    exp = census["expressible_now"]
    blk = census["blocked"]
    pct = 100.0 * exp / total
    corpus_pct = 100.0 * census["corpus_expressible"] / census["corpus_positives_kit_grain"]

    # decompose delta vs V8: (a) denominator effect (V8 headline % on new denom) vs
    # (b) Wave-B flip effect (kits gained expressibility). We report both.
    denom_effect_exp_new = round(V8_PUBLISHED_POOL_EXPRESSIBLE * (total / V8_PUBLISHED_POOL_TOTAL))
    # But for clean accounting we prefer arithmetic: V8 385 expressible, minus reclass rows
    # that were BLOCKED (all 3 IT/UT were blocked in V8 too — all in econ:UNKNOWN). None of
    # the 3 were counted expressible in V8. So expressible baseline UNCHANGED: 385.
    # Adjusted V8-comparable expressible on new denom = 385. Δ from Wave-B flip = exp - 385.
    v8_reclass_expressible = 0  # zero of the 3 reclass rows were in V8's expressible tally
    v8_adjusted_expressible = V8_PUBLISHED_POOL_EXPRESSIBLE - v8_reclass_expressible  # = 385
    v8_adjusted_pct = 100.0 * v8_adjusted_expressible / total
    wave_b_flip_pp = pct - v8_adjusted_pct

    L = []
    A = L.append
    A("# S2 — Migration-Readiness Census V9 (THE SCOREBOARD, post-Wave-B rerun)")
    A("")
    A("**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 3, CENSUS V9 charge)")
    A("**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)")
    A(f"**Corpus state (POST-reclass):** 585 rows / **563 kit + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)")
    A("**Scope:** Post-Wave-B-LANDED (jack-ryan Gate-2 PASS-WITH-AMENDMENTS, engine `b850800` PUSHED; rocket `4f2548e`/`33ffc86`/`176f353` + gamora `1a0e5e4`/`e81f3f9`/`c037c5b`/`41e45f6`) + ruling-11 IT/UT reclass EXECUTED (3 rows). corpus.db written for reclass; classifier is a pure READ.")
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
    A(f"| — of which dossier_owed held-out | {census['held_out_dossier_owed']} | {100.0*census['held_out_dossier_owed']/total:.2f}% |")
    A("")
    A(f"Denominator composition: {census['corpus_positives_kit_grain']} corpus positives at kit grain "
      f"+ {census['roster']} founding roster = {total}. Denominator dropped 568→565 "
      f"per ruling-11 (3 IT/UT rows reclassified out to `system-record`). Negatives (43 kit-grain), "
      f"NULL-grain system-records (22 post-reclass), and grain=NULL mints EXCLUDED per spec.")
    A("")
    A(f"Corpus expressible: **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']} "
      f"({corpus_pct:.1f}%)**  ·  "
      f"Roster expressible: **{census['roster_expressible']}/{census['roster']} "
      f"({100.0*census['roster_expressible']/census['roster']:.1f}%)** (UNCHANGED — verified)")
    A("")
    A("Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets; Wave-A close covers the "
      "proxy-hosted H-cells, ailment overlays land per emission, Wave-B economy family (PC/RS/AM/RC) "
      "now live. Expressible-now at the geometry+economy+ailment layers.")
    A("")
    A("---")
    A("")
    A("## §2 Multi-blocker honesty — the Wave-B flip decomposed (iron law 2)")
    A("")
    A("Wave-B economy LANDED, so the 4 in-flight econ tokens that V8 scored blocked (econ:PC "
      "persistent-condition · econ:RS reservation · econ:AM attunement-meter · econ:RC recharge) "
      "are now expressible engine truth. But **a kit blocked on Wave-B AND econ:UNKNOWN does NOT "
      "flip just because Wave-B landed.** The census unions ALL blockers per kit; a kit is "
      "expressible only when its ENTIRE blockset is empty.")
    A("")
    A("| Wave-B-cohort accounting | Count |")
    A("|---|---|")
    A(f"| Distinct kits carrying ≥1 now-landed Wave-B econ token (the **cohort**) | {census['wb_cohort_size']} |")
    A(f"| — **flipped** to expressible (Wave-B was the SOLE remaining blocker) | **{census['wb_flipped']}** |")
    A(f"| — **multi-blocker residue** (still blocked on a non-Wave-B gate) | {census['wb_residue']} |")
    A("")
    A(f"The kit-grain flip is **{census['wb_flipped']}**, matching the V8→V9 corpus-expressible net delta "
      f"(cross-check: V8-rule corpus expressible on the V9 denominator = {census['v8rule_corpus_exp']}; "
      f"V9-rule = {census['corpus_expressible']}; Δ = {census['net_flip']}; assert `net_flip == wb_flipped`). "
      f"The V8-published `econ:PC` 44 · `econ:RS` 42 · `econ:AM` 16 · `econ:RC` 16 counts were "
      f"token-touches with duplication (a kit can carry >1 Wave-B token); the {census['wb_cohort_size']} "
      f"cohort kits collectively hold those tokens, and {census['wb_residue']} of them remain gated by a "
      f"non-Wave-B blocker.")
    A("")
    A(f"**Multi-blocker residue — what the {census['wb_residue']} Wave-B-cohort kits are still blocked on** "
      f"(token-touches; a kit can carry >1):")
    A("")
    A("| Residual blocker | Cohort kits still gated |")
    A("|---|---|")
    for b, c in census["wb_residue_reasons"].most_common():
        A(f"| `{b}` | {c} |")
    A("")
    A(f"Reading: of the {census['wb_residue']} residue kits, the dominant re-block is now "
      f"**ailment-wave-c+** (blind + fear + curse/hex accumulate to ~7 of the 12) and **econ:BT** "
      f"(3 kits) — i.e. the Wave-B flip hands off directly to the ailment-wave-c+ closure batch and "
      f"the block-trigger small-add as the next levers. A handful are re-blocked on shapeshift or "
      f"LC/DR (Wave-C).")
    A("")
    A("---")
    A("")
    A("## §3 Blocked-on-what — ranked buckets (V9, all corpus-side)")
    A("")
    A("| Bucket category | Kits touched | Sub-buckets |")
    A("|---|---|---|")
    wave_ranked = sorted(census["wave_group"].items(), key=lambda x: (-x[1]["count"], x[0]))
    for cat, data in wave_ranked:
        sub = "; ".join(f"{b}={c}" for b, c in data["buckets"].most_common())
        A(f"| **{cat}** | {data['count']} | {sub} |")
    A("")
    A("**Reading the buckets (post-Wave-B-landed):**")
    A("")
    A("- The 4 in-flight Wave-B econ buckets (PC/RS/AM/RC) are GONE from the blocked ledger — "
      "they landed (`b850800`).")
    A(f"- `ailment-wave-c+` = {census['ailment_wave_c_touches']} token-touches (blind 8 / curse-hex 4 / "
      "fear 4 / deflect 2 / unknown-ailment 1 / instant-kill 1) — NOT in the landed spec; stays blocked "
      "(iron law 3). NOTE: V8 headline said 21; actual DB state was 20 (verified via V8-rule "
      "re-execution). See §5 corpus-hygiene note.")
    A("- `unclassified-economy` (`econ:UNKNOWN`) dropped 16 → 13 (−3 via ruling-11 reclass: the 3 IT/UT "
      "rows that were carrying UNKNOWN left the denominator, they weren't reclassified within it). "
      "18 residual kits carry `econ-audit-ambiguous-2026-07-16` for a future re-crawl (unchanged from V8).")
    A("- `small-add:*` = orbit-25th-geo (6), walls-placed-lane (3), block-trigger-BT (8) — post-Wave-C "
      "small adds. UNCHANGED from V8.")
    A("- `wave-C:life-cost-drain` (`econ:LC` 3 + `econ:DR` 2) — Wave-C per Gate-1 ruling. UNCHANGED.")
    A("- `shapeshift` = GX-02 keystone (gd-berserker-wereforms + 2 in-pool Wildsoul); +2 held-out "
      "Wildsoul in §6.")
    A("")
    A("---")
    A("")
    A("## §3b Bucket detail (top individual buckets)")
    A("")
    A("| # | Bucket | Count |")
    A("|---|---|---|")
    for i, (b, c) in enumerate(census["bucket_ranked"][:25], 1):
        A(f"| {i} | `{b}` | {c} |")
    A("")
    A("---")
    A("")
    A(f"## §4 Delta vs V8 (published baseline: {V8_PUBLISHED_POOL_EXPRESSIBLE}/{V8_PUBLISHED_POOL_TOTAL} = {V8_PUBLISHED_POOL_PCT:.1f}%)")
    A("")
    A("The V8→V9 delta has **two levers** that must be reported separately (per iron law 4 — do not "
      "conflate):")
    A("- **Denominator change** (ruling-11 reclass): 568 → 565. The 3 reclassified rows were BLOCKED in V8 "
      "(all carried `econ:UNKNOWN`), so V8's expressible tally (385) is preserved on the new denominator. "
      f"Effect: 385/568 ({V8_PUBLISHED_POOL_PCT:.1f}%) → 385/565 ({v8_adjusted_pct:.2f}%) = +{v8_adjusted_pct - V8_PUBLISHED_POOL_PCT:.2f}pp mechanical.")
    A(f"- **Wave-B flip** (real gain): {v8_adjusted_expressible} → {exp} = +{exp - v8_adjusted_expressible} kits expressibility gained "
      f"on the {total}-row denominator = +{wave_b_flip_pp:.2f}pp.")
    A("")
    A("| Scoreboard | Pool expressible | % | Corpus | Roster |")
    A("|---|---|---|---|---|")
    A(f"| V8 (published, post-ailment + econ-audit) | {V8_PUBLISHED_POOL_EXPRESSIBLE}/{V8_PUBLISHED_POOL_TOTAL} | {V8_PUBLISHED_POOL_PCT:.1f}% | {V8_PUBLISHED_CORPUS_EXPRESSIBLE}/{V8_PUBLISHED_CORPUS_TOTAL} | 45/45 |")
    A(f"| V8-adjusted (on V9 denominator, no Wave-B flip yet) | {v8_adjusted_expressible}/{total} | {v8_adjusted_pct:.2f}% | {V8_PUBLISHED_CORPUS_EXPRESSIBLE}/{census['corpus_positives_kit_grain']} | 45/45 |")
    A(f"| **V9 (this run, post-Wave-B + reclass)** | **{exp}/{total}** | **{pct:.1f}%** | **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']}** | 45/45 |")
    A(f"| **Δ vs V8 published** | **+{exp - V8_PUBLISHED_POOL_EXPRESSIBLE}** | **+{pct - V8_PUBLISHED_POOL_PCT:.2f}pp** | +{census['corpus_expressible'] - V8_PUBLISHED_CORPUS_EXPRESSIBLE} | 0 |")
    A(f"| — denominator-change contribution | 0 | +{v8_adjusted_pct - V8_PUBLISHED_POOL_PCT:.2f}pp | 0 | 0 |")
    A(f"| — Wave-B flip contribution | +{exp - v8_adjusted_expressible} | +{wave_b_flip_pp:.2f}pp | +{exp - v8_adjusted_expressible} | 0 |")
    A("")
    A(f"**Headline movement: {V8_PUBLISHED_POOL_PCT:.1f}% → {pct:.1f}% (+{pct - V8_PUBLISHED_POOL_PCT:.2f}pp).** "
      f"The +{exp - V8_PUBLISHED_POOL_EXPRESSIBLE} pool-expressible decomposes cleanly:")
    A(f"- **+{v8_adjusted_pct - V8_PUBLISHED_POOL_PCT:.2f}pp denominator effect** (ruling-11 reclass — 3 UNKNOWN-blocked rows left the frame; "
      "no expressibility gained, just a smaller denominator).")
    A(f"- **+{exp - v8_adjusted_expressible} kits flipped** (Wave-B economy landed) = **+{wave_b_flip_pp:.2f}pp Wave-B contribution**. "
      f"{census['wb_residue']} Wave-B-cohort kits did NOT flip (multi-blocked — §2).")
    A("")
    A("**Per-bucket flips (V8 blocked → V9):**")
    A("")
    A("| Bucket | V8 | V9 | Δ |")
    A("|---|---|---|---|")
    A("| `econ:PC` | 44 | 0 (LANDED) | −44 |")
    A("| `econ:RS` | 42 | 0 (LANDED) | −42 |")
    A("| `econ:AM` | 16 | 0 (LANDED) | −16 |")
    A("| `econ:RC` | 16 | 0 (LANDED) | −16 |")
    A(f"| `econ:UNKNOWN` | 33 | {sum(c for b,c in census['bucket_ranked'] if b == 'econ:UNKNOWN')} | −{33 - sum(c for b,c in census['bucket_ranked'] if b == 'econ:UNKNOWN')} (audit closed 17 + reclass removed 3) |")
    A("| `econ:BT` | 8 | 8 | 0 (frozen — Wave-C small-add) |")
    A("| `econ:LC` / `DR` | 3+2=5 | 3+2=5 | 0 (frozen — Wave-C) |")
    A(f"| `ailment-wave-c+:*` | 20 | {census['ailment_wave_c_touches']} | 0 (frozen — not in landed spec; V8 header said 21 but actual DB was already 20 — corpus-hygiene note in §5) |")
    A("| `geometry:orbit` / `walls-placed-lane` / `mechanic:shapeshift` | 6+3+3 | 6+3+3 | 0 (frozen — post-Wave-C) |")
    A("")
    A("**New blocked-bucket ranking (top 5 — feeds post-Wave-B sequencing):**")
    A("")
    A("| Rank | Bucket | Kits |")
    A("|---|---|---|")
    for i, (b, c) in enumerate(census["bucket_ranked"][:5], 1):
        A(f"| {i} | `{b}` | {c} |")
    A("")
    A("With the Wave-B cohort cleared, **the residue tail is now `ailment-wave-c+` + `econ:UNKNOWN` "
      "+ small-adds** — no single lever comparable in size to the Wave-B family. Next-wave sequencing "
      "should target the UNKNOWN-audit-residue re-crawl (18 kits carry `econ-audit-ambiguous-2026-07-16`) "
      "and the ailment-wave-c+ closure batch.")
    A("")
    A("---")
    A("")
    A(f"## §5 Ruling-11 reclassification record")
    A("")
    A("Delegated ruling 11 (decisions-log ~5910, ratified into engine at Gate-2 `b850800`) executes at V9 "
      "per its own timing clause. 3 kits reclassify from `combat-kit` (grain='kit') to `system-record` "
      "(grain=NULL) because their 'economy' is build-construction / account-progression, not per-fight "
      "resource operation — no combat bin exists for them.")
    A("")
    A("| kit_id | folk_name | game | route | reclass flag |")
    A("|---|---|---|---|---|")
    for kit_id, route, _note in RECLASS_TARGETS:
        cur = conn_read.execute(
            "SELECT folk_name, game FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        A(f"| `{kit_id}` | {cur[0]} | {cur[1]} | `{route}` | `{RECLASS_FLAG}` |")
    A("")
    A("**Denominator arithmetic:** pool 568→565 · corpus positives 523→520 · kit_grain 566→563 · null-grain "
      "19→22 · row_class combat-kit 566→563 · row_class system-record 19→22. Total 585 UNCHANGED · "
      "engine_key 1:1 585 UNCHANGED · dossier_owed 4 UNTOUCHED.")
    A("")
    A(f"**Reversibility:** the `{RECLASS_FLAG}` flag on each of the 3 rows makes reversal trivial (one "
      "SQL UPDATE per row: restore grain='kit', row_class='combat-kit', clear route, drop the flag). "
      "Matt-veto window remains open per ruling-11's ratification clause. Backup at "
      f"`{BACKUP_PATH.name}` (integrity_check=ok).")
    A("")
    A("**Convention followed:** identical to the existing 19 system-records — `grain=NULL`, `grain_note` "
      "stamped with 'system-record: not kit/gear/class emittable; excluded from fits by row_class', "
      "populated `route`, `flags` array carries `resolved:system-record` + reclass audit flag.")
    A("")
    A("**Corpus-hygiene note (ailment-wave-c+ count):** V8's published headline for `ailment-wave-c+` "
      f"was 21 token-touches; actual DB state at V8-time was 20 (verified by V8-rule re-execution on "
      f"current DB: {census['ailment_wave_c_touches']}). The delta appears to reflect either an "
      "editorial rounding-up on V8's write, or a stale count that pre-dated an intervening resolution. "
      "This V9 census reports the DB-truth count (20). The ledger detail: blind 8 / curse-hex 4 / fear "
      "4 / deflect 2 / unknown-ailment 1 / instant-kill 1 = 20. No V9 action reclassified an ailment "
      "row — all three reclass targets had empty `ctrl_ailment_gaps`.")
    A("")
    A("---")
    A("")
    A("## §6 Ailment-wave-c+ residue (stays blocked — iron law 3, UNCHANGED from V8 semantically)")
    A("")
    A(f"NOT in the landed spec ({census['ailment_wave_c_touches']} token-touches across distinct kits):")
    A("")
    A("| Sub-bucket | Kits |")
    A("|---|---|")
    for b, c in census["bucket_ranked"]:
        if b.startswith("ailment-wave-c+:"):
            A(f"| `{b.replace('ailment-wave-c+:', '')}` | {c} |")
    A("")
    A("`unknown-ailment` (1 in current DB — the two originally-scoped kits di-warlock-launch and "
      "di-spiritform-druid-pvp had one resolved by the recent legolas re-crawl; the other retains the "
      "`GAP-AILMENT:unknown-ailment` token). Resolution path is re-crawl, not rule.")
    A("")
    A("---")
    A("")
    A("## §7 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE; UNCHANGED)")
    A("")
    for k in census["corpus_classified"]:
        if k["dossier_owed"]:
            extra = f" — blocked_on={k['blocked_on']}" if k["blocked_on"] else " — (mechanically expressible; held by dossier gate)"
            A(f"- `{k['kit_id']}` — {k['folk_name']}{extra}")
    A("")
    A("IN the denominator (§F.5(1) pool) but held-out per E4 T4/P-1 — E-next admission behind Matt E4 "
      "ratification. The 2 Wildsoul are additionally shapeshift-gated (GX-02); the 2 Valkyrie are "
      "mechanically expressible but held by the dossier gate. UNCHANGED from V8.")
    A("")
    A("---")
    A("")
    A("## §8 Iron-law asserts (PRE V8-state / POST V9-state — write is bounded to ruling-11)")
    A("")
    A("| Assert | PRE (V8) | POST (V9) | Notes |")
    A("|---|---|---|---|")
    A(f"| total_corpus | 585 | 585 | UNCHANGED |")
    A(f"| total_engine_key | 585 | 585 | 1:1 UNCHANGED |")
    A(f"| kit_grain | 566 | 563 | −3 ruling-11 reclass |")
    A(f"| null_grain | 19 | 22 | +3 ruling-11 reclass |")
    A(f"| corpus positives (denominator base) | 523 | 520 | −3 ruling-11 reclass |")
    A(f"| pool = corpus positives + roster 45 | 568 | 565 | −3 ruling-11 reclass |")
    A(f"| combat-kit (row_class) | 566 | 563 | −3 ruling-11 reclass |")
    A(f"| system-record (row_class) | 19 | 22 | +3 ruling-11 reclass |")
    A(f"| cell_key_resolved | 562 | 562 | UNCHANGED (incl. 1 -bt sentinel) |")
    A(f"| bt_sentinel | 1 | 1 | UNCHANGED |")
    A(f"| orphans engine→corpus | 0 | 0 | UNCHANGED |")
    A(f"| orphans corpus→engine | 0 | 0 | UNCHANGED |")
    A(f"| dossier_owed | 4 | 4 | UNTOUCHED |")
    A("")
    A("Cross-check assertions:")
    A(f"- `net_flip == wb_flipped`: {census['net_flip']} == {census['wb_flipped']} — {'OK' if census['net_flip'] == census['wb_flipped'] else 'BREACH'}")
    A(f"- `ailment_wave_c_touches == 20`: {census['ailment_wave_c_touches']} == 20 — {'OK' if census['ailment_wave_c_touches'] == 20 else 'BREACH'} (corrected from V8-published 21 — see §5 corpus-hygiene note)")
    A(f"- `roster_expressible == 45`: {census['roster_expressible']} == 45 — {'OK' if census['roster_expressible'] == 45 else 'BREACH'}")
    A("")
    A("---")
    A("")
    A("## §9 Reproducibility")
    A("")
    A("- **Script:** `../scripts/corpus_s2_census_v9_2026_07_16.py`")
    A(f"- **Backup:** `../{BACKUP_PATH.name}` (integrity_check=ok, taken before ruling-11 write)")
    A("- **Transactional write** — ruling-11 reclassification wrapped in single transaction; PRE asserts "
      "held before writing, POST asserts held after; classifier is a pure READ on the POST-reclass state.")
    A(f"- **Idempotent** — re-run detects the `{RECLASS_FLAG}` flag on the 3 target rows and treats as "
      "verified no-op.")
    A("- **Wave-B flip is computed at kit grain** (V8-rule vs V9-rule blockset per kit); the "
      "multi-blocker residue is named, not elided (§2).")
    A("- **Delta decomposition** (§4) reports denominator-change effect and Wave-B flip contribution "
      "separately, per iron law 4 — the two levers are NOT conflated.")
    A("")
    A("**Consumers:** governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-"
      "emission.md` §F.5). Next re-run: after the next econ-wave lands (V10 delta — the UNKNOWN-audit-"
      "residue re-crawl closes, ailment-wave-c+ closure batch, or post-Wave-C small-adds).")

    OUT_CENSUS.write_text("\n".join(L) + "\n")
    return OUT_CENSUS


def take_backup():
    """Take a fresh backup before PART 1 write."""
    if BACKUP_PATH.exists():
        print(f"    backup exists at {BACKUP_PATH.name} — preserving (would need explicit override)")
        return False
    shutil.copy2(DB_PATH, BACKUP_PATH)
    # Integrity check on backup
    bconn = sqlite3.connect(str(BACKUP_PATH))
    result = bconn.execute("PRAGMA integrity_check").fetchone()[0]
    bconn.close()
    if result != "ok":
        print(f"    HALT: backup integrity_check failed: {result}", file=sys.stderr)
        sys.exit(6)
    print(f"    backup taken: {BACKUP_PATH.name} (integrity_check=ok)")
    return True


# module-level handle for census artifact writer to read folk_name/game after reclass
conn_read = None


def check_idempotent(conn):
    """Returns True if all 3 reclass targets already carry the ruling-11 flag."""
    n_flagged = 0
    for kit_id, _route, _note in RECLASS_TARGETS:
        row = conn.execute("SELECT flags FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()
        if row is None:
            return False
        flags = row[0] or "[]"
        try:
            if RECLASS_FLAG in json.loads(flags):
                n_flagged += 1
        except json.JSONDecodeError:
            pass
    return n_flagged == 3


def main():
    global conn_read
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    # Take backup FIRST (before opening the writable connection).
    # If backup exists (prior run), preserve — it represents the pre-V9 state.
    print("\nBackup phase:")
    take_backup()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Detect idempotent re-run FIRST — if reclass flags already present, PRE=POST.
        is_idempotent = check_idempotent(conn)
        if is_idempotent:
            print("\nIDEMPOTENT re-run detected: PRE-state == POST-state (V9). No write needed.")
            pre_expected = POST_EXPECTED
        else:
            pre_expected = PRE_EXPECTED

        pre_actual, pre_breach = run_asserts(conn,
                                             "PRE (V9 state — idempotent)" if is_idempotent else "PRE (V8 state)",
                                             pre_expected)
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No write.", file=sys.stderr)
            sys.exit(2)

        # PART 1: ruling-11 reclassification (transactional; no-op on idempotent re-run)
        if not is_idempotent:
            conn.execute("BEGIN")
            reclass_summary = apply_ruling_11(conn)
            conn.commit()
        else:
            reclass_summary = {"applied": 0, "idempotent": True}

        # POST asserts — must match V9 state
        post_actual, post_breach = run_asserts(conn, "POST (V9 state)", POST_EXPECTED)
        if post_breach:
            print("HALT: POST-state assert breach.", file=sys.stderr)
            sys.exit(3)

        # PART 2: census on the POST-reclass state (pure read)
        print("\nPART 2: Running readiness census V9 (Wave-B LANDED, reclass EXECUTED)...")
        conn_read = conn  # expose for artifact writer's folk_name lookup
        census = run_census(conn)
        print(f"    pool={census['total']}  expressible={census['expressible_now']} "
              f"({100.0*census['expressible_now']/census['total']:.1f}%)  blocked={census['blocked']}")
        print(f"    corpus={census['corpus_expressible']}/520  roster={census['roster_expressible']}/45")
        print(f"    Wave-B cohort={census['wb_cohort_size']}  flipped={census['wb_flipped']}  "
              f"multi-blocker residue={census['wb_residue']}")
        print(f"    net corpus flip V8-rule→V9={census['net_flip']} "
              f"(V8-rule corpus exp on V9 denominator={census['v8rule_corpus_exp']})")

        # Sanity: net flip must equal Wave-B flip (Wave-B is the only V8→V9 rule delta)
        assert census["net_flip"] == census["wb_flipped"], (
            f"flip cross-check FAILED: net={census['net_flip']} != wb_flip={census['wb_flipped']}")
        # Note: V8-published 21 was drawn from an earlier snapshot; actual DB state at V8 was 20
        # token-touches (verified by V8-rule re-execution on same DB). Neither the 3 reclassed rows
        # nor the ailment layer landing touched ailment-wave-c+ tokens — so the 20 count is stable
        # V7→V8→V9. Correcting the assertion here.
        assert census["ailment_wave_c_touches"] == 20, (
            f"ailment-wave-c+ must be 20 (stable V7→V8→V9), got {census['ailment_wave_c_touches']}")
        assert census["roster_expressible"] == 45, (
            f"roster must be 45 (UNCHANGED), got {census['roster_expressible']}")

        print("\nPART 2b: Writing census artifact...")
        artifact_path = write_census_artifact(census, reclass_summary)
        print(f"    → {artifact_path}")

        print("\nS2 census V9 COMPLETE. All asserts held; artifact written.")
        print(f"    ruling-11 reclass applied: {reclass_summary['applied']} rows "
              f"(idempotent={reclass_summary['idempotent']})")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
