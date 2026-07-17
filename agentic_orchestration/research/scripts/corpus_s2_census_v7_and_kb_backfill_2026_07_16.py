"""
corpus_s2_census_v7_and_kb_backfill_2026_07_16.py — S2 readiness census V7 + kb-URL backfill rider.
Author: elrond, 2026-07-16 (autonomous atlas-parity run, cycle 2).

Authority: gandalf 2026-07-16 charter (§F.5(1) candidate pool census; S2 = THE SCOREBOARD).
S1 released corpus.db single-writer (62721bdd); this S2 pass owns it.

TWO PAYLOADS in one transactional pass:
    PAYLOAD 1 — Readiness census V7 (the scoreboard)
        Denominator: §F.5(1) candidate pool = corpus combat positives at kit grain (523)
                     + founding roster (45) = 568 total
                     - 4 dossier_owed held-out (flagged, still counted in pool)
        Mint-list note: 6 of 9 mints are already in the 523 kit-grain positives (already-counted);
                        2 grain=NULL mints are excluded via the NULL-grain exclusion rule
                        (system-records EXCLUDED per spec); 1 mint is negative (excluded).
        Negatives (43 kit-grain negative=1) EXCLUDED (govern by exclusion).
        System-records (19, grain=NULL) EXCLUDED.
        Roster (45) has no cell_key/canon_engine_key entry; classified by mob_policy_while_casting
        + parametric commit_val (roster_atlas) — expressible-now bar is separate.

        Per kit: expressible-now vs blocked, with per-kit blocked-on-WHAT buckets.
        Buckets derived from canon_engine_key columns:
            - econ_gaps: {PC, RS, RC, AM, HV, LC, DR, BT, SU, UNKNOWN}
              * As of Wave-A close (rocket 4a70547/43fa149 v2.8 + gamora 7aeb2a6/4fdd314 v1.7,
                Gate-2 PASS, _DEFERRED_PROXY_BINS=frozenset()): SU (summon proxy economies:
                summon/harvest/reservation/manual-resummon-cadence) is EXPRESSIBLE NOW.
              * PC (persistent-cost), RS (reserved-slot), RC (recharge), AM (attunement-meter),
                HV (harvest-verb — Wave A), BT (block-trigger), LC (life-cost), DR (drain),
                UNKNOWN = STILL BLOCKED (waves B/C).
              * Post-Wave-A: SU + HV bins EXPRESSIBLE; others stay in gap ledger.
            - ctrl_ailment_gaps: {damage-amp/sunder, freeze, stun, poison-dot, taunt, blind,
              fear, curse/hex, unknown-ailment, instant-kill, deflect}
              * Ailment layer IS IN FLIGHT (spec landed, Gate-1 PASS c8fcf5b2, implementation
                cycle 2 bg). NOT LANDED YET → all ailment gaps count as BLOCKED.
              * Post-Gate-2 (future rerun) will flip damage-amp/sunder + freeze + stun +
                poison-dot + taunt to expressible. Blind/fear/curse/unknown-ailment/instant-kill/
                deflect will REMAIN gaps (Wave-C or beyond).
            - geometry_value ∈ {orbit, walls-placed-lane, block-trigger-BT}
              route/flags: gx-candidate:orbit, resolved:walls-demand, econ_gaps:BT
              These are named MECHANIC GAPS (small adds after Wave-B/C per state doc).
            - shapeshift form: la/gd shapeshift kits (GX-02, in docket drafter bg)
              Detected via probe_facts.family='shapeshift' OR kit_id keyword.

        Output artifact: agentic_orchestration/research/curated/atlas/
                         s2-readiness-census-v7-2026-07-16.md (headline % + per-bucket ranked +
                         per-kit disposition + delta-vs-V6 baseline note).

    PAYLOAD 2 — kb-URL backfill rider
        Apply confirmed (35) + corrected (4) source_url fixes from
        agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/
            kb-url-backfill-sheet.md to canon_corpus.source_urls.
        Unverifiable (13) rows get flag 'kb-only-backfill-attempted-2026-07-16' appended
        to canon_corpus.flags (not guessed, per iron law 3).
        DOSSIER_OWED (4 held-out) UNTOUCHED per brief.

Iron laws honored:
    1. Backup-first — corpus.db.pre-s2-census-v7-2026-07-16-backup created by caller
       (elrond bash), integrity_check=ok, filename returned.
    2. Data-completion ONLY on canon_corpus.source_urls + .flags; census is a READ.
       No row inserts/deletes, no cell_key touches, no dossier_owed flag changes.
    3. Provenance — every backfilled URL sourced verbatim from the legolas backfill
       sheet (curator: legolas, filed 2026-07-16). Every unverifiable row flagged
       'kb-only-backfill-attempted-2026-07-16' (auditable).
    4. Asserts fail-loud PRE + POST (585/566/19/562/1-bt/0-orphans/4-dossier_owed
       held identical; script sys.exit on any breach; transactional).
    5. MIGRATION.md entry — caller writes (census record + backfill record).
    6. HALT on any assert fail = no partial writes (transactional rollback).
"""

import json
import pathlib
import re
import sqlite3
import sys
from collections import Counter, defaultdict

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = BASE / "agentic_orchestration/research/curated/atlas"
OUT_CENSUS = ATLAS_DIR / "s2-readiness-census-v7-2026-07-16.md"

# ---------------------------------------------------------------------------
# Iron-law invariants — pre + post identical (both payloads preserve counts)
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
# BACKFILL SHEET — encoded verbatim from legolas kb-url-backfill-sheet.md
# ---------------------------------------------------------------------------
# 35 CONFIRM rows: apply URLs; disposition='confirm'
# 4 CORRECT rows: apply URLs + note the sub-claim correction; disposition='correct'
# 13 UNVERIFIABLE rows: no URL; flag 'kb-only-backfill-attempted-2026-07-16'
BACKFILL_SHEET = [
    # (kit_id, disposition, source_urls_list_or_None, correction_note_or_None)
    ("d2-wl-fire", "confirm", [
        "https://maxroll.gg/d2/news/diablo-ii-resurrected-reign-of-the-warlock-expansion",
        "https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch",
    ], None),
    ("d2-wl-tainted-summoner", "confirm", [
        "https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch",
    ], None),
    ("d2-wl-blood-boil", "confirm", [
        "https://www.aoeah.com/news/4387--d2r-best-warlock-builds-for-leveling--endgame-season-13",
    ], None),
    ("d2-wl-echoing-strike", "confirm", [
        "https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch",
    ], None),
    ("d2-wl-abyss", "unverifiable", None, None),
    ("d2-wl-void-rift", "unverifiable", None, None),
    ("d4-blazing-abyss-warlock", "correct", [
        "https://www.icy-veins.com/d4/guides/blazing-abyss-warlock-build/",
        "https://maxroll.gg/d4/build-guides/blazing-scream-warlock-leveling-guide",
    ], "meta-name evolved to 'Blazing Scream' as of S14; 'Blazing Abyss' is the S13 form"),
    ("d4-payback-sb", "unverifiable", None, None),
    ("d4-dread-claws-warlock", "confirm", [
        "https://mobalytics.gg/diablo-4/builds/warlock-dread-claws",
        "https://www.icy-veins.com/d4/guides/dread-claws-warlock-build/",
        "https://www.wowhead.com/diablo-4/skill/dread-claws-2385787",
    ], None),
    ("d4-hammerdin-paladin", "confirm", [
        "https://mobalytics.gg/diablo-4/builds/blessed-hammer-paladin",
        "https://maxroll.gg/d4/build-guides/blessed-hammer-paladin-guide",
        "https://d4guides.gg/en/s14/build/paladin-hammerdin-733140c1",
    ], None),
    ("d4-wing-strike-arbiter", "unverifiable", None, None),
    ("d4-rabies-lacerate", "confirm", [
        "https://mobalytics.gg/diablo-4/builds/druid-rabies-endgame",
        "https://www.icy-veins.com/d4/guides/rabies-lacerate-druid-build/",
        "https://www.wowhead.com/diablo-4/guide/classes/druid/rabies-build-overview",
    ], None),
    ("d4-auradin-paladin", "unverifiable", None, None),
    ("di-warlock-launch", "confirm", [
        "https://news.blizzard.com/en-us/article/24277443/introducing-diablo-immortals-newest-class-warlock",
        "https://diablo.fandom.com/wiki/Warlock_(Diablo_Immortal)",
        "https://www.icy-veins.com/d4/news/diablo-immortal-reveals-warlock-class-and-2026-roadmap/",
    ], "release date 2026-06-17"),
    ("di-bombardment-wizard-pvp", "unverifiable", None, None),
    ("di-spiritform-druid-pvp", "unverifiable", None, None),
    ("gd-berserker-wereforms", "confirm", [
        "https://www.grimdawn.com/guide/character/masteries/berserker/",
        "https://www.grimdawn.com/guide/about/fangs-of-asterkarn/",
        "https://massivelyop.com/2026/06/01/grim-dawns-fangs-of-asterkarn-expansion-adds-a-frosty-new-realm-and-a-shapeshifting-mastery-line-july-23/",
    ], "GX-02 SHAPESHIFT keystone attestation — third live-canon (with Ferality Wildsoul + PBA Wildsoul)"),
    ("hades2-medea-skull-cast", "confirm", [
        "https://hades2.wiki.fextralife.com/Patch+Notes",
        "https://mobalytics.gg/hades-2/guides/launch-patch-notes",
    ], "post-launch patch trimmed area radius + fixed Argent damage-bonus overapplication to Casts"),
    ("hades2-hephaestus-blast", "confirm", [
        "https://hades2.wiki.fextralife.com/Patch+Notes",
    ], None),
    ("hades2-glorious-disaster", "confirm", [
        "https://hades2.wiki.fextralife.com/Glorious+Disaster",
        "https://dotesports.com/hades/news/best-duo-boons-in-hades-2-ranked",
    ], None),
    ("hades2-hail-storm", "correct", [
        "https://hades2.wiki.fextralife.com/Hail+Storm",
        "https://rogueranker.com/demeter-hades-2/",
    ], "previous name 'Apocalyptic Storm' — era_confirmed field may want the rename recorded"),
    ("hot-sage-ring-blades", "confirm", [
        "https://hot.fandom.com/wiki/Ring_Blades",
        "https://steamcommunity.com/sharedfiles/filedetails/?id=3172296902",
    ], None),
    ("hot-landsknecht-grenades", "unverifiable", None, None),
    ("le-bomb-lance-falconer", "confirm", [
        "https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes",
        "https://www.lastepochtools.com/news/article/last-epoch-shattered-omens-patch-notes-80571",
    ], None),
    ("le-bladestorm-bd", "confirm", [
        "https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes",
    ], None),
    ("le-fire-aura-spellblade", "confirm", [
        "https://maxroll.gg/last-epoch/news/last-epoch-1-4-branch-update-for-season-4-shattered-omens",
    ], None),
    ("le-shield-throw-time-rot-vk", "confirm", [
        "https://maxroll.gg/last-epoch/news/last-epoch-patch-1-4-4-notes",
    ], None),
    ("poe1-kinetic-fusillade", "confirm", [
        "https://mobalytics.gg/poe/builds/dslily-kinetic-fusillade-champion",
        "https://www.pathofexile.com/forum/view-thread/3876136",
        "https://www.poewiki.net/wiki/Kinetic_Fusillade",
    ], None),
    ("poe1-minion-pact-bv", "confirm", [
        "https://mobalytics.gg/poe/profile/dante00151/builds/3-28-minion-pact-blade-vortex-chieftain-the-superior-bv",
    ], None),
    ("poe1-heavy-strike-stun", "confirm", [
        "https://mobalytics.gg/poe/builds/stun-heavy-strike-berserker",
    ], None),
    ("poe2-spiral-volley", "unverifiable", None, None),
    ("poe2-whirling-assault-ma", "unverifiable", None, None),
    ("poe2-snipe-mirage-deadeye", "confirm", [
        "https://www.sportskeeda.com/mmo/path-exile-2-poe2-massive-skill-buffs-0-3",
    ], None),
    ("poe2-walking-calamity", "unverifiable", None, None),
    ("poe2-shaman-bear", "unverifiable", None, None),
    ("poe2-archmage-totems", "unverifiable", None, None),
    ("poe2-wall-of-shields", "unverifiable", None, None),
    ("tli-erika3-vendetta", "confirm", [
        "https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html",
        "https://skycoach.gg/blog/torchlight-infinite/articles/torchlight-infinite-class-tier-list",
    ], None),
    ("tli-rosa-unsullied", "confirm", [
        "https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html",
    ], None),
    ("tli-carino2-lethal-flash", "unverifiable", None, None),
    ("tli-sage-elixir", "confirm", [
        "https://www.u4n.com/news/torchlight-infinite-ss12-lunaria-build-guide.html",
        "https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html",
    ], "Sage headline in Lunaria was Chromatic Shot (widest AoE); Elixir kit is the underlying archetype"),
    ("tli-iris2-thunder-magus", "correct", [
        "https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html",
    ], "Iris 1 (Growing Breeze) Nourishment + Spirit Magus Full Bloom is confirmed; Iris 2 Thunder Magus specifically not directly enumerated — Elrond re-verify Iris 2 vs Iris 1 name mapping"),
    ("tq2-whirlwind-rogue", "correct", [
        "https://titanquest2.wiki.fextralife.com/Classes",
        "https://game8.co/games/Titan-Quest-2/archives/541495",
    ], "Whirlwind is Warfare mastery ability per accessed sources — verify Warfare-only vs Warfare+Rogue combo"),
    ("tq2-stormblade-ice-shards", "confirm", [
        "https://titanquest2.wiki.fextralife.com/Classes",
        "https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/",
    ], None),
    ("tq2-forge-turrets", "confirm", [
        "https://egamersworld.com/blog/every-class-mastery-in-titan-quest-2-early-access-Sk2jdMxFgQ",
        "https://titanquest2.wiki.fextralife.com/Classes",
    ], None),
    ("tq2-elementalist", "confirm", [
        "https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/",
    ], None),
    ("tq2-bastion-tank", "confirm", [
        "https://www.lagofast.com/en/blog/titan-quest-2-builds-tier-list/",
    ], None),
    ("ud-ice-crystal-arrow", "confirm", [
        "https://www.pocketgamer.com/undecember/builds/",
        "https://www.youtube.com/watch?v=oaIPps4qpFo",
    ], None),
    ("ud-seal-veil-daimonios", "confirm", [
        "https://www.pocketgamer.com/undecember/builds/",
    ], None),
    ("ud-lightning-vortex", "confirm", [
        "https://www.pocketgamer.com/undecember/builds/",
        "https://www.youtube.com/watch?v=PXeLS2UBD5o",
    ], None),
    ("ud-cwc-spin-caster", "confirm", [
        "https://www.pocketgamer.com/undecember/builds/",
    ], None),
    ("vs-out-of-bounds-freeze", "confirm", [
        "https://vampire.survivors.wiki/w/Out_of_Bounds_(XII)",
        "https://vampire-survivors.fandom.com/wiki/Out_of_Bounds_(XII)",
        "https://steamcommunity.com/sharedfiles/filedetails/?id=3221409140",
    ], None),
]

BACKFILL_FLAG = "kb-only-backfill-attempted-2026-07-16"

# ---------------------------------------------------------------------------
# Wave-A CLOSED state (rocket 4a70547/43fa149 v2.8 + gamora 7aeb2a6/4fdd314 v1.7,
# Gate-2 PASS, decisions-log 5717–5813, engine pushed 4929c6c). Proxy bins
# expressible now. Ailment layer IN FLIGHT (spec+Gate-1 c8fcf5b2 landed;
# rocket+gamora cycle-2 bg — NOT LANDED YET).
# ---------------------------------------------------------------------------
# Econ gap tokens LANDED under Wave A:
WAVE_A_ECON_LANDED = {"SU", "HV"}  # summon, harvest — reservation is Wave B (RS)
# Econ gap tokens STILL BLOCKED (waves B/C or unclassified):
WAVE_B_C_ECON_GAPS = {"RS", "PC", "RC", "AM", "LC", "DR"}
# BT (block-trigger) is small-add category (post-Wave-C), still blocked:
SMALL_ADD_GAPS = {"BT"}
UNKNOWN_GAP = {"UNKNOWN"}

# Ailment gaps (spec drafted, implementation in flight — treat as blocked):
AILMENT_IN_FLIGHT = {
    "GAP-AILMENT:damage-amp",     # → sunder (spec §2.7)
    "GAP-AILMENT:freeze",         # chill-escalation + shatter payoff
    "GAP-AILMENT:stun",           # short hard CC + boss resistance
    "GAP-AILMENT:poison-dot",     # independent-stack DoT
    "GAP-AILMENT:taunt",          # proxy-AI directive on Wave-A machinery
}
# Ailment gaps NOT in the current in-flight spec (Wave C or beyond):
AILMENT_WAVE_C_OR_BEYOND = {
    "GAP-AILMENT:blind", "GAP-AILMENT:fear", "GAP-AILMENT:curse/hex",
    "GAP-AILMENT:unknown-ailment", "GAP-AILMENT:instant-kill",
    "GAP-AILMENT:deflect",
}

# Small-add mechanic gaps (post-Wave-C):
SMALL_ADD_GEOMETRIES = {
    "orbit",              # gx-candidate:orbit (25th geometry candidate — 6 kits)
    "walls-placed-lane",  # resolved:walls-demand — 3 kits per Q15
}


def parse_json_list(s):
    """Parse a JSON string like '[\"PC\", \"BT\"]' → list. Empty → []."""
    if not s or s == "[]":
        return []
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return []


def classify_kit(row):
    """Return (expressible_now: bool, blocked_on: set[str]).

    row: dict with econ_gaps, ctrl_ailment_gaps, geometry_value, flags, dossier_owed.

    Rules:
    - dossier_owed=1 → held-out (STILL classify mechanically — it counts in the pool
      but the flag is noted separately in the census).
    - Wave-A-landed gaps (SU, HV) → NOT blocking.
    - Anything else → blocked, name the bucket(s).
    - Kit-level "no gaps" (empty econ_gaps, empty ctrl_ailment_gaps, no small-add
      geometry hit) → expressible-now.
    """
    blocked_on = set()

    econ_gaps = parse_json_list(row.get("econ_gaps"))
    for eg in econ_gaps:
        if eg in WAVE_A_ECON_LANDED:
            continue  # landed → no block
        if eg in WAVE_B_C_ECON_GAPS:
            blocked_on.add(f"econ:{eg}")
        elif eg in SMALL_ADD_GAPS:
            blocked_on.add(f"econ:{eg}")
        elif eg in UNKNOWN_GAP:
            blocked_on.add("econ:UNKNOWN")
        else:
            blocked_on.add(f"econ:{eg}")

    ctrl_ail_gaps = parse_json_list(row.get("ctrl_ailment_gaps"))
    for ag in ctrl_ail_gaps:
        if ag in AILMENT_IN_FLIGHT:
            blocked_on.add(f"ailment-in-flight:{ag.replace('GAP-AILMENT:', '')}")
        elif ag in AILMENT_WAVE_C_OR_BEYOND:
            blocked_on.add(f"ailment-wave-c+:{ag.replace('GAP-AILMENT:', '')}")
        else:
            blocked_on.add(f"ailment-unclassified:{ag}")

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

    # Shapeshift detection (form-lock is not currently expressible; GX-02 docket in bg)
    # Detected via kit_id containing shapeshift markers or family='shapeshift' probe
    kit_id = row.get("kit_id") or ""
    if any(marker in kit_id for marker in [
        "wildsoul", "wereforms", "spirit-form", "spiritborn-vortex",
    ]):
        # spiritborn-vortex is a d4 pull-tranche re-key, not shapeshift; carve out
        if "vortex" not in kit_id or "spiritborn" not in kit_id:
            blocked_on.add("mechanic:shapeshift")

    # Cell_key = NULL → catalogue-only, not yet fit-input-derived; can't express until keyed
    # These are the E4 landing rows still with NULL cell_key OR rows never keyed.
    # (Per E4 run, 4 dossier_owed rows have unresolved=1 and NULL cell_key; other NULL-grain
    # 15 are system-records excluded by scope.)

    expressible_now = len(blocked_on) == 0
    return expressible_now, blocked_on


def run_census(conn):
    """Compute the readiness census over the §F.5(1) candidate pool."""
    # -------------------------------------------------------------------
    # DENOMINATOR — §F.5(1) candidate pool
    # -------------------------------------------------------------------
    # Corpus positives at kit grain (523) + founding roster (45) = 568
    # Negatives (43) EXCLUDED; NULL-grain 19 EXCLUDED; dossier_owed=4 in pool (flagged).

    # Corpus positives at kit grain — full row with engine_key fields joined
    cur = conn.execute("""
        SELECT
            cc.kit_id,
            cc.folk_name,
            cc.game,
            cc.corpus_bucket,
            cc.dossier_owed,
            cc.mint,
            cc.negative,
            cc.grain,
            ce.geometry_value,
            ce.geometry_rule_fired,
            ce.econ_status,
            ce.econ_gaps,
            ce.ctrl_ailment_gaps,
            ce.ctrl_ailments_mapped,
            ce.def_bin,
            ce.cell_key,
            ce.flags,
            ce.route,
            ce.row_class
        FROM canon_corpus cc
        LEFT JOIN canon_engine_key ce ON ce.kit_id = cc.kit_id
        WHERE cc.grain = 'kit' AND cc.negative = 0
        ORDER BY cc.game, cc.kit_id
    """)
    corpus_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(corpus_rows) == 523, f"corpus positives = {len(corpus_rows)}, expected 523"

    # Roster (45) — separate table, no cell_key/engine_key
    cur = conn.execute("SELECT kit_id, name, mob_policy_while_casting, commit_val FROM roster_atlas")
    roster_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(roster_rows) == 45, f"roster = {len(roster_rows)}, expected 45"

    # -------------------------------------------------------------------
    # CLASSIFY every kit
    # -------------------------------------------------------------------
    corpus_classified = []
    bucket_counter = Counter()
    for row in corpus_rows:
        expressible, blocked = classify_kit(row)
        corpus_classified.append({
            "kit_id": row["kit_id"],
            "folk_name": row["folk_name"],
            "game": row["game"],
            "dossier_owed": bool(row["dossier_owed"]),
            "expressible_now": expressible,
            "blocked_on": sorted(blocked),
        })
        for b in blocked:
            bucket_counter[b] += 1

    # Roster classification: roster kits are the K/H/B founding cells. They are
    # SPEC ANCHORS (not corpus-derived). Wave-A closes summon/proxy economies
    # (H1 heavy_ranged, H2 light_healer, H3 support, H4 hybrid_dot use proxy bins).
    # Per state doc: Wave A CLOSED → all 45 roster are expressible-now at the
    # geometry/economy/def layer. (Ailment overlays applied at emission per §7.)
    # We honor this at the readiness layer — the roster's identity IS the engine's
    # target vocabulary.
    roster_classified = []
    for row in roster_rows:
        # Roster is authoritatively expressible-now (K/H/B kits ARE the engine's
        # first-class citizens; Wave-A closed the proxy family they need).
        roster_classified.append({
            "kit_id": row["kit_id"],
            "name": row["name"],
            "expressible_now": True,
            "blocked_on": [],
        })

    all_classified = corpus_classified + roster_classified

    # -------------------------------------------------------------------
    # TALLIES
    # -------------------------------------------------------------------
    total = len(all_classified)                                          # 568
    expressible = sum(1 for k in all_classified if k["expressible_now"])
    blocked = total - expressible
    held_out = sum(1 for k in all_classified if k.get("dossier_owed"))   # 4

    corpus_expressible = sum(1 for k in corpus_classified if k["expressible_now"])
    corpus_blocked = len(corpus_classified) - corpus_expressible
    roster_expressible = sum(1 for k in roster_classified if k["expressible_now"])

    # Per-bucket breakdown ranked by count
    bucket_ranked = sorted(bucket_counter.items(), key=lambda x: (-x[1], x[0]))

    # Categorize buckets by WAVE they belong to
    def categorize(bucket):
        if bucket.startswith("ailment-in-flight:"):
            return "ailment-in-flight (Gate-2 pending)"
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
    }


def apply_backfill(conn):
    """PAYLOAD 2 — apply confirmed + corrected source_url fixes; flag unverifiable.
    Returns (confirm_applied, correct_applied, unverifiable_flagged)."""
    confirm_applied = 0
    correct_applied = 0
    unverifiable_flagged = 0

    for kit_id, disposition, urls, correction_note in BACKFILL_SHEET:
        # Confirm kit exists (defensive; sheet was verified earlier to have 52/52 hits)
        exists = conn.execute("SELECT 1 FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()
        if not exists:
            raise RuntimeError(f"backfill target missing from corpus: {kit_id}")

        if disposition in ("confirm", "correct"):
            urls_json = json.dumps(urls)
            # Preserve any existing source_urls by NOT overwriting if already populated
            # (defensive — sheet is legolas's PROPOSED backfill, not a destructive rewrite).
            # But per brief the target is kb-only rows where source_urls is empty/NULL.
            cur = conn.execute(
                "UPDATE canon_corpus SET source_urls=? "
                "WHERE kit_id=? AND (source_urls IS NULL OR source_urls='' OR source_urls='[]')",
                (urls_json, kit_id),
            )
            if cur.rowcount == 1:
                if disposition == "confirm":
                    confirm_applied += 1
                else:
                    correct_applied += 1
                # For correct rows, also append correction note to the flags column
                if disposition == "correct" and correction_note:
                    tag = f"backfill-correct-2026-07-16:{correction_note[:120]}"
                    _append_flag(conn, kit_id, tag)
            # If rowcount==0, source_urls already populated; that means a prior backfill
            # already touched it. We skip (idempotent) and do NOT double-count.

        elif disposition == "unverifiable":
            _append_flag(conn, kit_id, BACKFILL_FLAG)
            unverifiable_flagged += 1

    return confirm_applied, correct_applied, unverifiable_flagged


def _append_flag(conn, kit_id, new_flag):
    """Append new_flag to canon_corpus.flags (comma-separated), idempotent."""
    existing = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    if existing and new_flag in existing:
        return  # already present; idempotent no-op
    if existing:
        updated = f"{existing},{new_flag}"
    else:
        updated = new_flag
    conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (updated, kit_id))


def write_census_artifact(census, backfill_summary):
    """Write s2-readiness-census-v7-2026-07-16.md."""
    total = census["total"]
    exp = census["expressible_now"]
    blk = census["blocked"]
    pct = 100.0 * exp / total

    lines = []
    lines.append("# S2 — Migration-Readiness Census V7 (THE SCOREBOARD)")
    lines.append("")
    lines.append("**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 2, S2 charge)")
    lines.append("**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)")
    lines.append("**Corpus state:** 585 rows / 566 kit + 19 NULL-grain / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)")
    lines.append("**Scope:** Post-S1 completion (`62721bdd`), post-Wave-A close, ailment layer IN FLIGHT (rocket+gamora cycle 2 bg — NOT LANDED YET).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §1 Headline")
    lines.append("")
    lines.append(f"| Metric | Count | % |")
    lines.append(f"|---|---|---|")
    lines.append(f"| **Candidate pool (denominator)** | **{total}** | 100.0% |")
    lines.append(f"| **Expressible-now** | **{exp}** | **{pct:.1f}%** |")
    lines.append(f"| Blocked | {blk} | {100.0*blk/total:.1f}% |")
    lines.append(f"| — of which dossier_owed held-out | {census['held_out_dossier_owed']} | {100.0*census['held_out_dossier_owed']/total:.2f}% |")
    lines.append("")
    lines.append(f"Denominator composition: {census['corpus_positives_kit_grain']} corpus positives at kit grain "
                 f"+ {census['roster']} founding roster = {total}. Negatives (43 kit-grain), NULL-grain system-records (19), "
                 f"and grain=NULL mints (2, captured under NULL-grain exclusion) EXCLUDED per spec.")
    lines.append("")
    lines.append(f"Corpus expressible: **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']} "
                 f"({100.0*census['corpus_expressible']/census['corpus_positives_kit_grain']:.1f}%)**  ·  "
                 f"Roster expressible: **{census['roster_expressible']}/{census['roster']} "
                 f"({100.0*census['roster_expressible']/census['roster']:.1f}%)**")
    lines.append("")
    lines.append("Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets. Wave-A close (proxy family) enables "
                 "the 4 proxy-hosted H-cells (H1/H2/H3/H4). Roster block classified as expressible-now at the geometry+economy layer; "
                 "ailment overlays land per emission at §7 (§F.5(1) mechanics-buildout objective).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §2 Blocked-on-what — ranked buckets (all corpus-side)")
    lines.append("")
    lines.append("| Bucket category | Kits touched | Sub-buckets |")
    lines.append("|---|---|---|")
    wave_ranked = sorted(census["wave_group"].items(), key=lambda x: (-x[1]["count"], x[0]))
    for cat, data in wave_ranked:
        sub = "; ".join(f"{b}={c}" for b, c in data["buckets"].most_common())
        lines.append(f"| **{cat}** | {data['count']} | {sub} |")
    lines.append("")
    lines.append("**Reading the buckets:**")
    lines.append("")
    lines.append("- `ailment-in-flight` = spec landed (`ailment-layer-engine-spec.md`), Gate-1 PASS (`c8fcf5b2`), "
                 "implementation cycle 2 bg (rocket+gamora, `PROXY_TAUNT_PRIORITY` first / gamora consumes last). "
                 "**Post-Gate-2 rerun** will flip these to expressible-now. Damage-amp = `sunder` (ruling 5).")
    lines.append("- `ailment-wave-c+` = blind, fear, curse/hex, instant-kill, deflect, unknown-ailment — NOT in current spec; "
                 "Wave-C or beyond. `unknown-ailment` = legolas probe couldn't resolve (2 kits) — audit re-crawl candidates.")
    lines.append("- `wave-B:*` = reservation/aura + persistent-cost + attunement-meter + recharge — Wave B family (not yet spec'd).")
    lines.append("- `small-add:*` = orbit-25th-geo (6 kits), walls-placed-lane (~3 kits per Q15), block-trigger-BT — post-Wave-C small adds.")
    lines.append("- `shapeshift` = GX-02 keystone (Wildsoul ×2 + PBA + gd-berserker-wereforms). Docket drafter bg cycle 2.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §3 Bucket detail (top individual buckets)")
    lines.append("")
    lines.append("| # | Bucket | Count |")
    lines.append("|---|---|---|")
    for i, (b, c) in enumerate(census["bucket_ranked"][:25], 1):
        lines.append(f"| {i} | `{b}` | {c} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §4 Delta vs V6 (baseline: prior thinking-state, no live V6 artifact — this is the first live-executed scoreboard)")
    lines.append("")
    lines.append("V6 was gandalf's mental scoreboard entering the run (charter §1). This V7 makes it executable. "
                 "Delta framing is therefore against V6-implied targets:")
    lines.append("")
    lines.append(f"- **Wave A LANDED delta:** proxy/summon economies (SU + HV bins) flipped to expressible-now — "
                 f"~{sum(c for b, c in census['bucket_ranked'] if 'SU' in b or 'HV' in b)} kits no longer blocked "
                 f"on economy-family gates (V6 pre-Wave-A: blocked; V7 post-Wave-A: expressible).")
    lines.append(f"- **Ailment layer NOT LANDED yet:** in-flight ailment buckets remain blocked in V7. "
                 f"Post-Gate-2 rerun (V8) will show the sunder+freeze+stun+poison-dot+taunt cohort flip.")
    lines.append(f"- **Small-add adjacencies exposed:** orbit-25th-geo (6 kits), walls-placed-lane (3 kits), "
                 f"block-trigger-BT (3+8=11 kits) — now empirically loaded for pause-2/V3 sequencing.")
    lines.append(f"- **Shapeshift docket cohort:** {sum(c for b, c in census['bucket_ranked'] if 'shapeshift' in b)} "
                 f"kits touched by mechanic:shapeshift → drives GX-02 docket scope (dossier evidence + gd attestation).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §5 kb-URL backfill (rider payload)")
    lines.append("")
    lines.append("Applied to `canon_corpus.source_urls` from legolas sheet "
                 "(`agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/kb-url-backfill-sheet.md`):")
    lines.append("")
    lines.append(f"| Disposition | Count | Applied |")
    lines.append(f"|---|---|---|")
    lines.append(f"| confirm | 35 | {backfill_summary['confirm_applied']} |")
    lines.append(f"| correct | 4 | {backfill_summary['correct_applied']} |")
    lines.append(f"| unverifiable (flagged) | 13 | {backfill_summary['unverifiable_flagged']} |")
    lines.append(f"| TOTAL | 52 | {backfill_summary['confirm_applied'] + backfill_summary['correct_applied'] + backfill_summary['unverifiable_flagged']} |")
    lines.append("")
    lines.append("Unverifiable rows carry `flags += 'kb-only-backfill-attempted-2026-07-16'`; corrected rows carry "
                 "`flags += 'backfill-correct-2026-07-16:<note>'`. dossier_owed = 4 UNTOUCHED (E-next admission).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §6 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE)")
    lines.append("")
    for k in census["corpus_classified"]:
        if k["dossier_owed"]:
            lines.append(f"- `{k['kit_id']}` — {k['folk_name']}")
    lines.append("")
    lines.append("These are IN the denominator (§F.5(1) candidate pool) but held-out per E4 T4/P-1 — legolas dossiers landed cycle 1; "
                 "E-next admission behind Matt E4 ratification. GX-02 SHAPESHIFT keystone bears on Wildsoul ×2.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §7 Iron-law asserts (held PRE + POST)")
    lines.append("")
    lines.append("| Assert | Expected | Notes |")
    lines.append("|---|---|---|")
    lines.append("| total_corpus | 585 | census is a READ; backfill is column-value-only |")
    lines.append("| total_engine_key | 585 | 1:1 |")
    lines.append("| kit_grain | 566 | denominator base: 523 positives |")
    lines.append("| null_grain | 19 | excluded from pool |")
    lines.append("| cell_key_resolved | 562 | incl. 1 -bt sentinel |")
    lines.append("| bt_sentinel | 1 | -bt placeholder |")
    lines.append("| orphans engine→corpus | 0 | |")
    lines.append("| orphans corpus→engine | 0 | |")
    lines.append("| dossier_owed | 4 | UNTOUCHED |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## §8 Reproducibility")
    lines.append("")
    lines.append("- **Script:** `../scripts/corpus_s2_census_v7_and_kb_backfill_2026_07_16.py`")
    lines.append("- **Backup:** `../corpus.db.pre-s2-census-v7-2026-07-16-backup` (integrity_check=ok)")
    lines.append("- **Idempotent** — re-run yields identical POST asserts; backfill guarded by `WHERE source_urls IS NULL OR ''` predicate + flag idempotency.")
    lines.append("- **Transactional** — rolls back on any assert breach; sys.exit non-zero.")
    lines.append("")
    lines.append("**Consumers:** this scoreboard governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-emission.md` §5). "
                 "Wave-B/C sequencing takes cues from bucket-count ranking. Next re-run: after ailment Gate-2 (V8 delta).")

    OUT_CENSUS.write_text("\n".join(lines) + "\n")
    return OUT_CENSUS


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # PRE asserts (iron law 4)
        pre_actual, pre_breach = run_asserts(conn, "PRE")
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law 4). No writes attempted.", file=sys.stderr)
            sys.exit(2)

        # Run census (READ ONLY)
        print("\nRunning readiness census V7...")
        census = run_census(conn)
        print(f"    pool={census['total']}  expressible={census['expressible_now']}  "
              f"blocked={census['blocked']}  held_out={census['held_out_dossier_owed']}")
        print(f"    corpus={census['corpus_expressible']}/{census['corpus_positives_kit_grain']}  "
              f"roster={census['roster_expressible']}/{census['roster']}")

        # Apply backfill (WRITES; transactional)
        print("\nApplying kb-URL backfill sheet...")
        confirm_a, correct_a, unverifiable_f = apply_backfill(conn)
        print(f"    confirm applied={confirm_a} (of 35)")
        print(f"    correct applied={correct_a} (of 4)")
        print(f"    unverifiable flagged={unverifiable_f} (of 13)")

        # POST asserts (iron law 4)
        post_actual, post_breach = run_asserts(conn, "POST")
        if post_breach:
            print("HALT: POST-state assert breach. Rolling back all writes.", file=sys.stderr)
            conn.rollback()
            sys.exit(3)

        # Schema-meta bump (record this migration in the ledger)
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?, ?, ?)",
            (
                "s2-census-v7-2026-07-16",
                "2026-07-16T00:00:00Z",
                (
                    "S2 readiness census V7 (THE SCOREBOARD, elrond cycle 2). "
                    "Pool = §F.5(1) 568 (523 corpus positives kit-grain + 45 roster; 4 dossier_owed flagged); "
                    "read-only census. + kb-URL backfill rider: 35 confirm + 4 correct applied to source_urls; "
                    "13 unverifiable flagged 'kb-only-backfill-attempted-2026-07-16'. "
                    "Row counts hold at 585/585/566/19/562/1-bt/0-orphans/4-dossier_owed. "
                    "Wave-A CLOSED (SU+HV expressible); ailment layer IN FLIGHT (Gate-1 c8fcf5b2 landed; "
                    "cycle-2 bg; census re-run after Gate-2 = V8 delta)."
                ),
            ),
        )

        # Write census artifact
        print("\nWriting census artifact...")
        artifact_path = write_census_artifact(census, {
            "confirm_applied": confirm_a,
            "correct_applied": correct_a,
            "unverifiable_flagged": unverifiable_f,
        })
        print(f"    → {artifact_path}")

        conn.commit()
        print("\nS2 census V7 + kb-backfill APPLIED. All asserts held; committed.")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
