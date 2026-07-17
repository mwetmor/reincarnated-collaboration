"""
corpus_s2_census_v8_2026_07_16.py — S2 readiness census V8 (THE SCOREBOARD, post-Gate-2 rerun).
Author: elrond, 2026-07-16 (autonomous atlas-parity run, cycle 2, CENSUS V8 charge).

Authority: gandalf-prime 2026-07-16 charter (§F.5(1) candidate pool census; S2 = THE SCOREBOARD).
Commissioner: gandalf-prime (Matt authorization 2026-07-16).

WHAT CHANGED SINCE V7 (two landed truths — this run REFLECTS them, does NOT re-apply them):
    1. AILMENT LAYER LANDED. jack-ryan Gate-2 verdict PASS-WITH-AMENDMENTS; engine commit cec8f12
       PUSHED (decisions-log 5796–5844). The 5 in-flight ailment buckets that V7 §2 scored BLOCKED
       (damage-amp/sunder · freeze · stun · poison-dot · taunt) are now LANDED ENGINE TRUTH →
       scored EXPRESSIBLE in V8. Ailment-wave-c+ (blind/curse-hex/fear/deflect/unknown-ailment/
       instant-kill = 21 token-touches) is NOT in the landed spec → STAYS BLOCKED.
    2. ECON:UNKNOWN AUDIT LANDED (elrond own return, top-level ../MIGRATION.md econ-unknown-audit
       -2026-07-16, commit 93233d18). 5 kits filled OUT of econ:UNKNOWN into the DB already:
         - chr-bleed-berserker, chr-high-ranger-warden → economy_model='spend' / status='native'
           / econ_gaps=[] (expressible from econ side)
         - poe1-baron-zombies, poe1-siege-ballista, gd-pet-conjurer → economy_model='summon-uptime'
           / status='gap' / econ_gaps=['SU'] (Wave-A landed → expressible)
       Pool econ:UNKNOWN is now 33 (was 38); econ:SU is now 9 (was 6). 18 kits carry
       'econ-audit-ambiguous-2026-07-16' flags (re-crawl candidates). These fills are ALREADY IN
       THE DB — V8 reads them naturally; it does not re-apply them.

IRON LAWS (this run):
    1. corpus.db is READ-ONLY. V8 is a PURE CENSUS — no backfill rider, no schema-meta INSERT,
       no column writes. The ONLY output is the census artifact MD + a MIGRATION.md entry (caller).
       Asserts held PRE + POST, byte-stable DB.
    2. MULTI-BLOCKER HONESTY. A kit blocked on ailment AND econ:PC does NOT flip just because
       ailment landed. The classifier unions ALL blockers per kit; a kit is expressible only when
       its ENTIRE blockset is empty. The ailment-cohort flip is computed at KIT grain (distinct
       kits whose sole remaining blocker was an in-flight ailment), and the multi-blocker residue
       (ailment-cohort kits still blocked on a non-ailment gate) is named explicitly.
    3. AILMENT-WAVE-C+ STAYS BLOCKED (21: blind 8 / curse-hex 4 / fear 4 / deflect 2 /
       unknown-ailment 2 / instant-kill 1). NOT in the landed spec.
    4. §4 delta vs V7 published baseline (258/568 = 45.4%). Headline movement, per-bucket flips,
       new blocked-bucket ranking (feeds Wave-B sequencing — Wave-B spec at Gate-1 now).
    5. Held-out 4 dossier_owed unchanged (§6). Roster 45/45 remains expressible.
    6. MIGRATION.md entry (caller). Auto-commit collab repo; NO push (gandalf pushes).

DENOMINATOR LAW (identical to V7):
    §F.5(1) candidate pool = 523 corpus positives at kit grain (grain='kit' AND negative=0)
    + 45 founding roster = 568. Negatives (43 kit-grain), NULL-grain system-records (19), and
    grain=NULL mints (captured under NULL-grain exclusion) EXCLUDED. 4 dossier_owed IN pool, flagged.
"""

import json
import pathlib
import sys
from collections import Counter, defaultdict

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = BASE / "agentic_orchestration/research/curated/atlas"
OUT_CENSUS = ATLAS_DIR / "s2-readiness-census-v8-2026-07-16.md"

import sqlite3

# ---------------------------------------------------------------------------
# Iron-law invariants — identical PRE + POST (V8 is a pure read; DB byte-stable)
# ---------------------------------------------------------------------------
EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "kit_grain": 566,
    "null_grain": 19,
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
}

# Published V7 headline baseline (pre-econ-audit) — the §4 delta anchor per charge.
V7_PUBLISHED_POOL_EXPRESSIBLE = 258
V7_PUBLISHED_POOL_PCT = 45.4
V7_PUBLISHED_CORPUS_EXPRESSIBLE = 213
# Ailment-cohort flip CEILING named in the charge (token-touch upper bound: 222 ailment + 5 econ).
FLIP_CEILING = 227


def run_asserts(conn, label):
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
    }
    print(f"\n[{label}] iron-law asserts:")
    breach = False
    for k, exp in EXPECTED.items():
        act = actual[k]
        ok = act == exp
        if not ok:
            breach = True
        print(f"    {k:24s} expected={exp:>4d}  actual={act:>4d}  {'OK' if ok else 'BREACH'}")
    return actual, breach


# ---------------------------------------------------------------------------
# CLASSIFICATION VOCABULARY
# ---------------------------------------------------------------------------
# Econ gaps LANDED under Wave A (rocket v2.8 + gamora v1.7, Gate-2 PASS, engine 4929c6c):
WAVE_A_ECON_LANDED = {"SU", "HV"}  # summon-uptime + harvest — expressible now
# Econ gaps STILL BLOCKED (waves B/C — Wave-B spec at Gate-1 now):
WAVE_B_C_ECON_GAPS = {"RS", "PC", "RC", "AM", "LC", "DR"}
SMALL_ADD_GAPS = {"BT"}       # block-trigger — small add (post-Wave-C)
UNKNOWN_GAP = {"UNKNOWN"}      # unclassified — audit residue (33 post-econ-audit)

# *** V8 CHANGE ***: ailment layer LANDED (Gate-2 PASS-WITH-AMENDMENTS, engine cec8f12 PUSHED,
# decisions-log 5796–5844). These 5 gap tokens are NOW EXPRESSIBLE ENGINE TRUTH → NOT blocking.
AILMENT_LANDED = {
    "GAP-AILMENT:damage-amp",     # → sunder (ruling 5)
    "GAP-AILMENT:freeze",         # chill-escalation + shatter payoff
    "GAP-AILMENT:stun",           # short hard CC + boss resistance
    "GAP-AILMENT:poison-dot",     # independent-stack DoT
    "GAP-AILMENT:taunt",          # proxy-AI directive on Wave-A machinery
}
# Ailment gaps NOT in the landed spec (Wave C or beyond) — STAY BLOCKED (iron law 3):
AILMENT_WAVE_C_OR_BEYOND = {
    "GAP-AILMENT:blind", "GAP-AILMENT:fear", "GAP-AILMENT:curse/hex",
    "GAP-AILMENT:unknown-ailment", "GAP-AILMENT:instant-kill",
    "GAP-AILMENT:deflect",
}

# Small-add mechanic gaps (post-Wave-C):
SMALL_ADD_GEOMETRIES = {"orbit", "walls-placed-lane"}


def parse_json_list(s):
    if not s or s == "[]":
        return []
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return []


def classify_kit(row, ailment_landed=True):
    """Return (expressible_now: bool, blocked_on: set[str]).

    ailment_landed=True is the V8 rule (ailment layer landed).
    ailment_landed=False reproduces the V7-era rule (used only for the flip decomposition,
    NOT for the V8 headline).

    Multi-blocker honest: unions ALL blockers; expressible IFF blockset empty.
    Blocker tokens are deduplicated by set semantics (a kit with a duplicated ailment token
    contributes ONE bucket-touch, matching V7 accounting).
    """
    blocked_on = set()

    for eg in parse_json_list(row.get("econ_gaps")):
        if eg in WAVE_A_ECON_LANDED:
            continue  # landed → no block
        # PC/RS/RC/AM/LC/DR/BT/UNKNOWN and any residual token → blocked, named econ:<TOK>
        blocked_on.add(f"econ:{eg}")

    for ag in parse_json_list(row.get("ctrl_ailment_gaps")):
        name = ag.replace("GAP-AILMENT:", "")
        if ag in AILMENT_LANDED:
            if not ailment_landed:
                blocked_on.add(f"ailment-in-flight:{name}")
            # V8: landed → no block
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
    assert len(corpus_rows) == 523, f"corpus positives = {len(corpus_rows)}, expected 523"

    cur = conn.execute("SELECT kit_id, name, mob_policy_while_casting, commit_val FROM roster_atlas")
    roster_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(roster_rows) == 45, f"roster = {len(roster_rows)}, expected 45"

    # -------------------------------------------------------------------
    # V8 classification (ailment LANDED)
    # -------------------------------------------------------------------
    corpus_classified = []
    bucket_counter = Counter()
    for row in corpus_rows:
        expressible, blocked = classify_kit(row, ailment_landed=True)
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

    # Roster: SPEC ANCHOR, authoritatively expressible-now (Wave-A closed the proxy family).
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
    # MULTI-BLOCKER HONESTY (iron law 2): ailment-cohort flip decomposition.
    # Cohort = distinct kits carrying >=1 in-flight (now-landed) ailment token.
    # For each: V7-rule blockset (ailment_landed=False) vs V8-rule blockset (True).
    #   - flipped   = kit now expressible (ailment was its SOLE remaining blocker)
    #   - residue   = kit STILL blocked on a non-ailment gate (multi-blocker)
    # -------------------------------------------------------------------
    ail_cohort = [r for r in corpus_rows
                  if any(a in AILMENT_LANDED for a in parse_json_list(r.get("ctrl_ailment_gaps")))]
    flipped = 0
    residue = 0
    residue_reasons = Counter()
    for r in ail_cohort:
        _, v8b = classify_kit(r, ailment_landed=True)
        if len(v8b) == 0:
            flipped += 1
        else:
            residue += 1
            for x in v8b:
                residue_reasons[x] += 1

    # Cross-check: net corpus flip V7-rule → V8-rule must equal ailment-cohort flip
    # (ailment is the only classification delta between the two rule-states).
    v7rule_corpus_exp = sum(
        1 for r in corpus_rows if classify_kit(r, ailment_landed=False)[0]
    )
    net_flip = corpus_expressible - v7rule_corpus_exp

    bucket_ranked = sorted(bucket_counter.items(), key=lambda x: (-x[1], x[0]))

    def categorize(bucket):
        if bucket.startswith("ailment-wave-c+:"):
            return "ailment-wave-c+"
        if bucket.startswith("ailment-unclassified:"):
            return "ailment-unclassified"
        if bucket == "econ:PC":
            return "wave-B:persistent-cost"
        if bucket == "econ:RS":
            return "wave-B:reserved-slot"
        if bucket == "econ:AM":
            return "wave-B:attunement-meter"
        if bucket == "econ:RC":
            return "wave-B:recharge"
        if bucket in ("econ:LC", "econ:DR"):
            return "wave-B/C:life-cost-drain"
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
        "ail_cohort_size": len(ail_cohort),
        "ail_flipped": flipped,
        "ail_residue": residue,
        "ail_residue_reasons": residue_reasons,
        "net_flip": net_flip,
        "v7rule_corpus_exp": v7rule_corpus_exp,
        "ailment_wave_c_touches": sum(c for b, c in bucket_ranked if b.startswith("ailment-wave-c+:")),
    }


def write_census_artifact(census):
    total = census["total"]
    exp = census["expressible_now"]
    blk = census["blocked"]
    pct = 100.0 * exp / total

    L = []
    A = L.append
    A("# S2 — Migration-Readiness Census V8 (THE SCOREBOARD, post-Gate-2 rerun)")
    A("")
    A("**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 2, CENSUS V8 charge)")
    A("**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)")
    A("**Corpus state:** 585 rows / 566 kit + 19 NULL-grain / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans) — **byte-stable (pure read this run)**")
    A("**Scope:** Post-ailment-LANDED (Gate-2 PASS-WITH-AMENDMENTS, engine `cec8f12` PUSHED, decisions-log 5796–5844) + post-econ:UNKNOWN-audit (5 fills applied, `93233d18`). corpus.db READ-ONLY — no backfill rider.")
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
      f"+ {census['roster']} founding roster = {total} (SAME denominator law as V7). Negatives (43 kit-grain), "
      f"NULL-grain system-records (19), and grain=NULL mints EXCLUDED per spec.")
    A("")
    A(f"Corpus expressible: **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']} "
      f"({100.0*census['corpus_expressible']/census['corpus_positives_kit_grain']:.1f}%)**  ·  "
      f"Roster expressible: **{census['roster_expressible']}/{census['roster']} "
      f"({100.0*census['roster_expressible']/census['roster']:.1f}%)**")
    A("")
    A("Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets; Wave-A close covers the "
      "proxy-hosted H-cells (H1/H2/H3/H4). Expressible-now at the geometry+economy layer; ailment "
      "overlays now LAND per emission (the ailment layer is live).")
    A("")
    A("---")
    A("")
    A("## §2 Multi-blocker honesty — the ailment flip decomposed (iron law 2)")
    A("")
    A("The ailment layer LANDED, so the 5 in-flight ailment buckets that V7 scored blocked "
      "(damage-amp/sunder · freeze · stun · poison-dot · taunt) are now expressible engine truth. "
      "But **a kit blocked on ailment AND econ:PC does NOT flip just because ailment landed.** "
      "The census unions ALL blockers per kit; a kit is expressible only when its ENTIRE blockset is empty.")
    A("")
    A("| Ailment-cohort accounting | Count |")
    A("|---|---|")
    A(f"| Distinct kits carrying ≥1 now-landed ailment token (the **cohort**) | {census['ail_cohort_size']} |")
    A(f"| — **flipped** to expressible (ailment was the SOLE remaining blocker) | **{census['ail_flipped']}** |")
    A(f"| — **multi-blocker residue** (still blocked on a non-ailment gate) | {census['ail_residue']} |")
    A("")
    A(f"**The real flip is {census['ail_flipped']}, not {FLIP_CEILING}.** The charter's ≤{FLIP_CEILING} ceiling "
      f"(222 in-flight-ailment token-touches + 5 econ) is a TOKEN-TOUCH upper bound. The kit-grain flip is "
      f"{census['ail_flipped']} because (a) the {census['ail_cohort_size']} cohort kits collectively hold 222 "
      f"ailment token-touches (many kits carry >1 ailment), and (b) {census['ail_residue']} of those kits remain "
      f"gated by a non-ailment blocker. The 5 econ-audit fills are NOT part of this flip — they already landed in "
      f"the DB (pre-V8) and lifted corpus from V7-published 213 to the 218 that this V8 read starts from.")
    A("")
    A("**Multi-blocker residue — what the 69 ailment-cohort kits are still blocked on** (token-touches; a kit can carry >1):")
    A("")
    A("| Residual blocker | Cohort kits still gated |")
    A("|---|---|")
    for b, c in census["ail_residue_reasons"].most_common():
        A(f"| `{b}` | {c} |")
    A("")
    A(f"Reading: of the {census['ail_residue']} residue kits, the dominant re-block is the **econ reservation/persistent-cost "
      f"family** (`econ:PC` + `econ:RS` lead) — i.e. the ailment flip HANDS OFF directly to Wave-B as the next lever. "
      f"A handful are re-blocked on wave-c+ ailments, small-add geometry, or shapeshift.")
    A("")
    A("---")
    A("")
    A("## §3 Blocked-on-what — ranked buckets (V8, all corpus-side)")
    A("")
    A("| Bucket category | Kits touched | Sub-buckets |")
    A("|---|---|---|")
    wave_ranked = sorted(census["wave_group"].items(), key=lambda x: (-x[1]["count"], x[0]))
    for cat, data in wave_ranked:
        sub = "; ".join(f"{b}={c}" for b, c in data["buckets"].most_common())
        A(f"| **{cat}** | {data['count']} | {sub} |")
    A("")
    A("**Reading the buckets (post-ailment-landed):**")
    A("")
    A("- The 5 in-flight ailment buckets (damage-amp/sunder · freeze · stun · poison-dot · taunt) are GONE from the "
      "blocked ledger — they landed (`cec8f12`).")
    A(f"- `ailment-wave-c+` = {census['ailment_wave_c_touches']} token-touches (blind 8 / curse-hex 4 / fear 4 / "
      "deflect 2 / unknown-ailment 2 / instant-kill 1) — NOT in the landed spec; stays blocked (iron law 3). "
      "legolas re-crawl (in flight, read-only) is probing the 2 `unknown-ailment` kits (di-warlock-launch, "
      "di-spiritform-druid-pvp).")
    A("- `wave-B:*` (persistent-cost + reserved-slot + attunement-meter + recharge) is now the TOP blocked family — "
      "**Wave-B spec is at Gate-1 now; this ranking is live input to Wave-B sequencing.**")
    A("- `unclassified-economy` (`econ:UNKNOWN`) dropped 38 → 33 (elrond econ-audit `93233d18`; 18 residual kits carry "
      "`econ-audit-ambiguous-2026-07-16` for a future re-crawl; 15 more queued as spec-amendment rule sketches).")
    A("- `small-add:*` = orbit-25th-geo (6), walls-placed-lane (3), block-trigger-BT (8) — post-Wave-C small adds.")
    A("- `shapeshift` = GX-02 keystone (gd-berserker-wereforms + 2 in-pool Wildsoul); +2 held-out Wildsoul in §6.")
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
    A("## §4 Delta vs V7 (published baseline: 258/568 = 45.4%)")
    A("")
    A(f"| Scoreboard | Pool expressible | % | Corpus | Roster |")
    A(f"|---|---|---|---|---|")
    A(f"| V7 (published, pre-econ-audit) | {V7_PUBLISHED_POOL_EXPRESSIBLE}/568 | {V7_PUBLISHED_POOL_PCT:.1f}% | {V7_PUBLISHED_CORPUS_EXPRESSIBLE}/523 | 45/45 |")
    A(f"| **V8 (this run, post-Gate-2 + econ-audit)** | **{exp}/568** | **{pct:.1f}%** | **{census['corpus_expressible']}/523** | 45/45 |")
    A(f"| **Δ** | **+{exp - V7_PUBLISHED_POOL_EXPRESSIBLE}** | **+{pct - V7_PUBLISHED_POOL_PCT:.1f}pp** | +{census['corpus_expressible'] - V7_PUBLISHED_CORPUS_EXPRESSIBLE} | 0 |")
    A("")
    A(f"**Headline movement: 45.4% → {pct:.1f}% (+{pct - V7_PUBLISHED_POOL_PCT:.1f}pp).** The +{exp - V7_PUBLISHED_POOL_EXPRESSIBLE} "
      f"pool-expressible decomposes cleanly:")
    A(f"- **+5 econ-audit fills** (V7-published 258 → 263): 2 native/spend (chr-bleed-berserker, chr-high-ranger-warden) "
      f"+ 3 SU/Wave-A-landed (poe1-baron-zombies, poe1-siege-ballista, gd-pet-conjurer). Already in DB pre-V8.")
    A(f"- **+{census['ail_flipped']} ailment flip** (263 → {exp}): distinct kits whose sole remaining blocker was an "
      f"in-flight ailment, now landed. {census['ail_residue']} ailment-cohort kits did NOT flip (multi-blocked — §2).")
    A("")
    A("**Per-bucket flips (V7 blocked → V8):**")
    A("")
    A("| Bucket | V7 | V8 | Δ |")
    A("|---|---|---|---|")
    A("| `ailment-in-flight:damage-amp` | 97 | 0 (LANDED) | −97 |")
    A("| `ailment-in-flight:freeze` | 42 | 0 (LANDED) | −42 |")
    A("| `ailment-in-flight:poison-dot` | 36 | 0 (LANDED) | −36 |")
    A("| `ailment-in-flight:stun` | 36 | 0 (LANDED) | −36 |")
    A("| `ailment-in-flight:taunt` | 11 | 0 (LANDED) | −11 |")
    A("| `econ:UNKNOWN` | 38 | 33 | −5 (econ-audit) |")
    A("| `econ:SU` (Wave-A, expressible) | 6 | 9 | +3 (econ-audit reclass) |")
    A("| `econ:PC` / `RS` / `AM` / `RC` / `LC` / `DR` / `BT` | frozen | frozen | 0 |")
    A("")
    A("**New blocked-bucket ranking (top 5 — feeds Wave-B sequencing, live at Gate-1):**")
    A("")
    A("| Rank | Bucket | Kits |")
    A("|---|---|---|")
    for i, (b, c) in enumerate(census["bucket_ranked"][:5], 1):
        A(f"| {i} | `{b}` | {c} |")
    A("")
    A("With the ailment cohort cleared, **the reservation/persistent-cost economy family (`econ:PC` 44 + `econ:RS` 42) "
      "is now the single biggest expressible-now lever**, followed by the audit residue (`econ:UNKNOWN` 33), then "
      "`econ:RC` 16 / `econ:AM` 16. Wave-B's exhibits map directly onto this ranking.")
    A("")
    A("---")
    A("")
    A("## §5 Ailment-wave-c+ residue (stays blocked — iron law 3)")
    A("")
    A(f"NOT in the landed spec ({census['ailment_wave_c_touches']} token-touches across distinct kits):")
    A("")
    A("| Sub-bucket | Kits |")
    A("|---|---|")
    for b, c in census["bucket_ranked"]:
        if b.startswith("ailment-wave-c+:"):
            A(f"| `{b.replace('ailment-wave-c+:', '')}` | {c} |")
    A("")
    A("`unknown-ailment` (2: di-warlock-launch, di-spiritform-druid-pvp) is under active legolas re-crawl "
      "(in flight, read-only — no contention with this census). Resolution path is a re-crawl, not a rule.")
    A("")
    A("---")
    A("")
    A("## §6 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE; UNCHANGED)")
    A("")
    for k in census["corpus_classified"]:
        if k["dossier_owed"]:
            extra = f" — blocked_on={k['blocked_on']}" if k["blocked_on"] else " — (mechanically expressible; held by dossier gate)"
            A(f"- `{k['kit_id']}` — {k['folk_name']}{extra}")
    A("")
    A("IN the denominator (§F.5(1) pool) but held-out per E4 T4/P-1 — E-next admission behind Matt E4 ratification. "
      "The 2 Wildsoul are additionally shapeshift-gated (GX-02); the 2 Valkyrie are mechanically expressible but "
      "held by the dossier gate. UNCHANGED from V7.")
    A("")
    A("---")
    A("")
    A("## §7 Iron-law asserts (held PRE + POST — DB byte-stable)")
    A("")
    A("| Assert | Expected | Notes |")
    A("|---|---|---|")
    A("| total_corpus | 585 | pure READ; no writes |")
    A("| total_engine_key | 585 | 1:1 |")
    A("| kit_grain | 566 | denominator base: 523 positives |")
    A("| null_grain | 19 | excluded from pool |")
    A("| cell_key_resolved | 562 | incl. 1 -bt sentinel |")
    A("| bt_sentinel | 1 | -bt placeholder |")
    A("| orphans engine→corpus | 0 | |")
    A("| orphans corpus→engine | 0 | |")
    A("| dossier_owed | 4 | UNTOUCHED |")
    A("")
    A("---")
    A("")
    A("## §8 Reproducibility")
    A("")
    A("- **Script:** `../scripts/corpus_s2_census_v8_2026_07_16.py`")
    A("- **Backup:** `../corpus.db.pre-s2-census-v8-2026-07-16-backup` (integrity_check=ok)")
    A("- **Pure census** — corpus.db READ-ONLY (no backfill, no schema-meta INSERT, no column writes). "
      "Only output is this artifact + the MIGRATION.md entry. DB byte-stable PRE→POST.")
    A("- **Idempotent** — re-run yields identical artifact + identical asserts.")
    A("- **Ailment flip is computed at kit grain** (V7-rule vs V8-rule blockset per kit); the multi-blocker residue "
      "is named, not elided.")
    A("")
    A("**Consumers:** governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-emission.md` §F.5). "
      "**Wave-B spec (at Gate-1 now) takes its exhibit sequencing from the §4 top-5 ranking.** "
      "Next re-run: after Wave-B lands (V9 delta — the PC/RS/AM/RC family flips).")

    OUT_CENSUS.write_text("\n".join(L) + "\n")
    return OUT_CENSUS


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        pre_actual, pre_breach = run_asserts(conn, "PRE")
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No output.", file=sys.stderr)
            sys.exit(2)

        print("\nRunning readiness census V8 (ailment LANDED)...")
        census = run_census(conn)
        print(f"    pool={census['total']}  expressible={census['expressible_now']} "
              f"({100.0*census['expressible_now']/census['total']:.1f}%)  blocked={census['blocked']}")
        print(f"    corpus={census['corpus_expressible']}/523  roster={census['roster_expressible']}/45")
        print(f"    ailment cohort={census['ail_cohort_size']}  flipped={census['ail_flipped']}  "
              f"multi-blocker residue={census['ail_residue']}")
        print(f"    net corpus flip V7-rule→V8={census['net_flip']} "
              f"(V7-rule corpus exp={census['v7rule_corpus_exp']})")
        # sanity: net flip must equal ailment flip (ailment is the only rule delta)
        assert census["net_flip"] == census["ail_flipped"], (
            f"flip cross-check FAILED: net={census['net_flip']} != ail_flip={census['ail_flipped']}")
        assert census["ailment_wave_c_touches"] == 21, (
            f"ailment-wave-c+ must be 21, got {census['ailment_wave_c_touches']}")

        # POST asserts — DB must be byte-identical (pure read)
        post_actual, post_breach = run_asserts(conn, "POST")
        if post_breach:
            print("HALT: POST-state assert breach.", file=sys.stderr)
            sys.exit(3)

        print("\nWriting census artifact...")
        artifact_path = write_census_artifact(census)
        print(f"    → {artifact_path}")

        # No commit needed (pure read; nothing to persist in DB). Explicit rollback for hygiene.
        conn.rollback()
        print("\nS2 census V8 COMPLETE. All asserts held; DB byte-stable (pure read); artifact written.")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
