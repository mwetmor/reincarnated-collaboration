#!/usr/bin/env python3
"""
R4 mint execution — the E-1 admission FOLD under Path-A mechanics.
=================================================================

RULED: Matt 2026-07-22 (three-run consolidated ruling sheet §5 R4=FOLD,
sequenced behind R1). R1 ruled PATH A -> mint UN-GATED, fires under Path-A
mechanics (E4 supplementary mint + served-artifact re-key). Conductor: gandalf.

EXACT SCOPE (nothing more):
  A. 5 new canon_corpus rows (corpus_class='annex'). Conservation 585 -> 590.
     - 4 Lost Ark skill-grain Destroyer pull-kits (pull-intrinsic tranche +
       Stage-A pull-7 docket §2, cell_keys VERBATIM):
         la-destroyer-vortex-gravity     (function=pull)
         la-destroyer-gravity-impact     (function=pull)
         la-destroyer-gravity-force      (function=pull)
         la-destroyer-gravity-compression(function=none  -- pull INFERRED per source)
     - di-druid-pvp-cc-stack-2026 (di-spiritform ruling §"Admission candidate").
  B. 1 re-key: d2-ghost-pvp -> d2-ghost-assassin-pvp. PK rename cascaded through
     EVERY in-DB base table that references the kit_id, PLUS the current served
     artifact atlas-edition4.json (points[40].kit_id). Frozen historical editions
     (E1/E2/E3, refit-candidate-1, e5-exhibit) PRESERVED as provenance (NOT touched)
     -- their d2-ghost-pvp string is the correct historical record of the key at
     that edition; mutating them would break the byte-frozen READ-ONLY law
     (atlas/MIGRATION.md line 340/394).
  C. mint_ledger audit entries for all six operations (build_authorized=0 --
     these are catalogue-admission / re-key events of ALREADY-attested mechanics,
     NOT mechanism-mints; status='r4-admission-fold' distinguishes them from the
     12 mechanism-mints).

MULTI-PROJECTILE-VOLLEY: docket/naming INPUT only -- explicitly NOT a mint row.
Never touched.

Store: agentic_orchestration/research/curated/corpus.db (the 10.7MB live store).
Backup: corpus.db.pre-r4-mint-2026-07-22-backup (pre-write; md5 pinned in log).
Discipline: fail-loud, transactional (single BEGIN; rollback-on-mismatch),
            idempotent (re-run to byte-identical state), source-anchored,
            raw preserved. Discipline #11 (empirical pre/post asserts).

NO FABRICATION: every field traces to a locatable source (pull-intrinsic tranche
2026-07-15-pull-intrinsic-classkit-tranche.md | pull-7 docket §2 | di-spiritform
ruling di-spiritform-phantom-2026-07-17.md §"Admission candidate" | mh-v3 recrawl
application-sheet-2026-07-17.md §4).
"""
import sqlite3
import json
import sys
import hashlib
import os

CURATED = os.path.join(os.path.dirname(__file__), "..", "curated")
DB = os.path.abspath(os.path.join(CURATED, "corpus.db"))
BACKUP = os.path.abspath(os.path.join(CURATED, "corpus.db.pre-r4-mint-2026-07-22-backup"))
E4_JSON = os.path.abspath(os.path.join(CURATED, "atlas", "atlas-edition4.json"))

REKEY_OLD = "d2-ghost-pvp"
REKEY_NEW = "d2-ghost-assassin-pvp"

# ---------------------------------------------------------------------------
# PRE-STATE (Discipline #11 empirical assert -- fail-loud if store moved)
# ---------------------------------------------------------------------------
EXPECT_PRE = {
    "corpus_total": 585,
    "corpus_record": 267,
    "corpus_annex": 299,
    "corpus_system": 19,
    "engine_key_total": 585,
    "orphans": 0,
    "mint_ledger_max": 12,
    "ghost_old_exists": 1,
    "ghost_new_exists": 0,
    "la_dvg_exists": 0,   # none of the 4 LA rows nor di-druid present pre-write
    "didruid_exists": 0,
}

# ---------------------------------------------------------------------------
# THE 4 LOST ARK DESTROYER SKILL-GRAIN PULL-KITS
#   canon_corpus fields mirror exact-batch peer d4-spiritborn-vortex
#   (provenance_tag='pull-tranche-edition2-2026-07-15', source_date='2026-07-15',
#    corpus_class='annex', canon_tier='deep', key_completeness=6, grain='kit').
#   court=NULL (abstain-not-force: the surviving pull-7 Diablo peers carry court=NULL;
#    Destroyer element is Physical/Gravity -- a court is not forced on skill-grain rows).
#   cell_key VERBATIM from pull-7 docket §2. source_url + mech_note from the tranche.
# ---------------------------------------------------------------------------
TRANCHE_URL = {
    "la-destroyer-vortex-gravity": "https://lostarkcodex.com/us/skill/18011/",
    "la-destroyer-gravity-impact": "https://lostark.wiki.fextralife.com/Gravity+Impact",
    "la-destroyer-gravity-force": "https://lostark.wiki.fextralife.com/Gravity+Force",
    "la-destroyer-gravity-compression": "https://lostark.wiki.fextralife.com/Gravity+Compression",
}

LA_ROWS = [
    {
        "kit_id": "la-destroyer-vortex-gravity",
        "folk_name": "Destroyer - Vortex Gravity",
        "cell_key": "rooted|melee|spiky|vortex_pull|damage|pull|tank|cooldown|solo|melee|high|instant|active|one-shot",
        "ctrl_function": "pull",
        "def_bin": "tank",
        "geometry_value": "vortex_pull",
        "delivery_value": "melee",
        "economy_model": "cooldown",
        "activation_val": "active",
        "dependency_val": "one-shot",
        "mech_note": ("[R4-mint 2026-07-22 :: Path-A supplementary admission] "
                      "Destroyer identity skill (Vortex Gravity). Hammer slam inflicts physical damage + "
                      "gravitational explosion pulling foes within 6m; High Stagger; Armor Destruction 12%% "
                      "debuff ~180s. In Hypergravity Mode all other skills disabled (only basic attack + VG). "
                      "The pull is the core identity mechanic. Assessment: closest to treatment=hybrid of any "
                      "intrinsic kit found (pull + damage co-fire, no configurable separation) -> keyed "
                      "ctrl_treatment=damage + ctrl_function=pull per hybrid-assignment-criteria-2026-07-15 §4 "
                      "(gandalf-adopted; corpus stays hybrid-EMPTY). STR / Physical-Gravity; 20s CD; "
                      "Hypergravity-Mode gate. Source: pull-intrinsic tranche 2026-07-15."),
        "mob_verbs": ["rooted"],
        "mob_skill_is_movement": 0,
    },
    {
        "kit_id": "la-destroyer-gravity-impact",
        "folk_name": "Destroyer - Gravity Impact",
        "cell_key": "rooted|melee|flat|vortex_pull|damage|pull|tank|generator-spender|solo|melee|med|channel|active|build→spend",
        "ctrl_function": "pull",
        "def_bin": "tank",
        "geometry_value": "vortex_pull",
        "delivery_value": "melee",
        "economy_model": "generator-spender",
        "activation_val": "active",
        "dependency_val": "build→spend",
        "mech_note": ("[R4-mint 2026-07-22 :: Path-A supplementary admission] "
                      "Concentration skill (Gravity Impact). Caster stationary; gravitational field forms at "
                      "caster location; enemies pulled in 8x (195.2 dmg) then explosion pulls remaining foes "
                      "(+63 dmg). Generates 2 Gravity Cores. Pull as density mechanic for multi-hit damage -> "
                      "damage-primary, pull-rider (function=pull). Paralysis Immunity during cast (rooted). "
                      "STR / Physical-Gravity; 12s CD. Source: pull-intrinsic tranche 2026-07-15."),
        "mob_verbs": ["rooted"],
        "mob_skill_is_movement": 0,
    },
    {
        "kit_id": "la-destroyer-gravity-force",
        "folk_name": "Destroyer - Gravity Force",
        "cell_key": "walk|melee|flat|line|damage|pull|mitigate|generator-spender|solo|melee|med|wind-up|active|build→spend",
        "ctrl_function": "pull",
        "def_bin": "mitigate",
        "geometry_value": "line",
        "delivery_value": "melee",
        "economy_model": "generator-spender",
        "activation_val": "active",
        "dependency_val": "build→spend",
        "mech_note": ("[R4-mint 2026-07-22 :: Path-A supplementary admission] "
                      "Concentration skill (Gravity Force). Frontal swing releases gravitational energy along "
                      "a straight LINE 7x (206.4 dmg total), pulling enemies close along the axis (pull-to-point "
                      "along a line, NOT radial). Two-phase: hammer swing (35) + gravity chain (206.4). Generates "
                      "2 Gravity Cores. damage-primary, pull-rider (function=pull); geometry=line. Paralysis "
                      "Immunity; walk (free to reposition between phases). STR / Physical-Gravity; 14s CD. "
                      "Source: pull-intrinsic tranche 2026-07-15."),
        "mob_verbs": ["walk"],
        "mob_skill_is_movement": 0,
    },
    {
        "kit_id": "la-destroyer-gravity-compression",
        "folk_name": "Destroyer - Gravity Compression",
        "cell_key": "rooted|melee|spiky|ground_targeted_circle|damage|none|mitigate|generator-spender|solo|melee|med|channel|active|build→spend",
        "ctrl_function": "none",   # pull INFERRED per source -> never-invent -> function=none (docket flag a)
        "def_bin": "mitigate",
        "geometry_value": "ground_targeted_circle",
        "delivery_value": "melee",
        "economy_model": "generator-spender",
        "activation_val": "active",
        "dependency_val": "build→spend",
        "mech_note": ("[R4-mint 2026-07-22 :: Path-A supplementary admission] "
                      "Gravity Release skill (spender; Gravity Compression). Thrust hammer into ground, release "
                      "gravitational wave (29 dmg), hold 2s to release a black hole (265.4 dmg over up to 9 hits). "
                      "Highest stagger of the Destroyer set. FLAG(a): the pull is IMPLICIT (9 hits at the black-hole "
                      "location suggest sustained magnetism) rather than an explicit 'enemies moved toward caster' "
                      "description -> never-invent governs -> function=none, pull_pending_vocab=0 "
                      "(RE-VERIFIED vs tranche source line 24). STR / Physical-Gravity; 24s CD. "
                      "Source: pull-intrinsic tranche 2026-07-15."),
        "mob_verbs": ["rooted"],
        "mob_skill_is_movement": 0,
    },
]

# ---------------------------------------------------------------------------
# di-druid-pvp-cc-stack-2026  (di-spiritform ruling §"Admission candidate", verbatim spec)
#   game=di, era_year=2025, skill_debut_year=2025, corpus_class='annex'.
#   All-landed CC vocab -> catalogue-only, cell_key NULL (E-derivation owed; NO fit input).
#   negative=0 (this is the REAL clean-shape row behind the di-spiritform phantom name;
#   the phantom row di-spiritform-druid-pvp stays negative=1, untouched).
# ---------------------------------------------------------------------------
DIDRUID = {
    "kit_id": "di-druid-pvp-cc-stack-2026",
    "folk_name": "DI Druid PvP CC stack",
    "game": "di",
    "corpus_class": "annex",
    "era_year": 2025,
    "skill_debut_year": 2025,
    "eras": "di-2026-era",
    "ctrl_raw": "stun-multi-source, slow, root/immobilize, knockback, damage-amp/marking, self-cc-immunity",
    "elem_raw": "physical, fire, earth",
    "source_urls": json.dumps([
        "https://news.blizzard.com/en-us/article/24216435",
        "https://blizzardwatch.com/2025/06/26/diablo-immortal-druid-class",
        "https://diabloimmortal.fandom.com/wiki/Druid",
    ]),
    "provenance_tag": "legolas-recrawl-v1-2026-07-17",
    "source_date": "2026-07-17",
    "mech_note": ("[R4-mint 2026-07-22 :: Path-A supplementary admission] "
                  "DI Druid PvP CC-stack archetype -- the REAL clean-shape row behind the di-spiritform "
                  "phantom NAME (phantom row di-spiritform-druid-pvp retains negative=1, untouched). DI Druid "
                  "class launched 2025-07-03 (Blizzard official). CC-dense objective-denial build; ALL vocab "
                  "landed: Werebear roar/Mangle/Summon-Grizzly stun, Oak Sage immobilize 4s, Stag Charge / "
                  "Thorn Armor slow 40%%, Earthquake knockup, Werewolf Howl damage-amp-marking, Werebear "
                  "Crush+Bound knockback, Fire Tornado DoT-burn, Rabid Might self-CC-immunity. elem mixed "
                  "(Fire Tornado fire; Earthquake/Landslide/Surging-Stone earth; most CC physical). "
                  "Catalogue-only: cell_key NULL (E-derivation owed; NO fit input). Conf capped <=0.50 "
                  "(post-cutoff di-2026-era). Source: di-spiritform ruling §'Admission candidate' + legolas "
                  "re-crawl di-spiritform-recrawl-2026-07-17."),
    "flags": "r4-admission-2026-07-22:matt-ruled-fold,di-druid-cc-stack-clean-row,conf-cap-0.50-post-cutoff",
}

# tables that carry a kit_id column and must cascade the re-key (BASE tables only;
# views v_canon_corpus_rekeyed / v_combat_kits / v_corpus_substrate / kit_master auto-reflect).
# Enumerated empirically (Discipline #11) from the live store, NOT assumed.
REKEY_TABLES = [
    "canon_corpus",                              # PK
    "canon_engine_key",                          # FK -> canon_corpus(kit_id)
    "canon_probe_facts",
    "kit_acceptance_assert",
    "kit_citations",
    "kit_delta_t4",
    "kit_deviation",
    "kit_dossier",
    "kit_mapping",
    "recognition_hook",
    "skill_geometry_band",
    "verify_ledger",
    "atlas_franchise_rollup",
    "atlas_franchise_rollup_refit_candidate_1",
]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg):
    print(f"HALT (no partial write): {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not os.path.exists(BACKUP):
        fail(f"backup missing: {BACKUP} (take backup before running)")
    print(f"DB       : {DB}")
    print(f"backup   : {BACKUP}  (md5 {md5(BACKUP)})")
    print(f"DB md5   : {md5(DB)}  [pre-write]")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=OFF;")  # PK rename cascade done manually across all tables
    cur = con.cursor()

    # ---- PRE-STATE asserts (fail-loud) --------------------------------------
    def scalar(q, *a):
        return cur.execute(q, a).fetchone()[0]

    pre = {
        "corpus_total": scalar("SELECT COUNT(*) FROM canon_corpus"),
        "corpus_record": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='record'"),
        "corpus_annex": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='annex'"),
        "corpus_system": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='system'"),
        "engine_key_total": scalar("SELECT COUNT(*) FROM canon_engine_key"),
        "orphans": scalar("SELECT COUNT(*) FROM canon_engine_key ek LEFT JOIN canon_corpus cc ON ek.kit_id=cc.kit_id WHERE cc.kit_id IS NULL"),
        "mint_ledger_max": scalar("SELECT COALESCE(MAX(mint_id),0) FROM mint_ledger"),
        "ghost_old_exists": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", REKEY_OLD),
        "ghost_new_exists": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", REKEY_NEW),
        "la_dvg_exists": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id='la-destroyer-vortex-gravity'"),
        "didruid_exists": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", DIDRUID["kit_id"]),
    }
    for k, v in EXPECT_PRE.items():
        if pre[k] != v:
            fail(f"PRE-STATE mismatch {k}: expected {v}, got {pre[k]}")
    print("PRE-STATE asserts: PASS", pre)

    try:
        cur.execute("BEGIN")

        # =================================================================
        # A. 5 NEW ROWS
        # =================================================================
        def insert_corpus(**f):
            cols = ", ".join(f.keys())
            ph = ", ".join(["?"] * len(f))
            cur.execute(f"INSERT INTO canon_corpus ({cols}) VALUES ({ph})", tuple(f.values()))

        def insert_engine_key(**f):
            cols = ", ".join(f.keys())
            ph = ", ".join(["?"] * len(f))
            cur.execute(f"INSERT INTO canon_engine_key ({cols}) VALUES ({ph})", tuple(f.values()))

        # --- 4 LA Destroyer skill-grain rows ---
        for r in LA_ROWS:
            insert_corpus(
                kit_id=r["kit_id"], folk_name=r["folk_name"], game="la",
                corpus_class="annex", source="canon",
                provenance_tag="pull-tranche-edition2-2026-07-15",
                source_date="2026-07-15", era_year=2018, eras="la-global-2026",
                canon_tier="deep", key_completeness=6, grain="kit",
                negative=0, mint=0, dossier_owed=0, unresolved=0, is_system=0,
                pull_pending_vocab=0,
                source_urls=json.dumps([TRANCHE_URL[r["kit_id"]]]),
                mech_note=r["mech_note"],
                flags="r4-admission-2026-07-22:matt-ruled-fold,la-destroyer-skill-grain,pull-7-docket",
            )
            raw = {
                "kit_id": r["kit_id"], "source": "pull-intrinsic-tranche-2026-07-15",
                "class": "Destroyer (Warrior/Heavy)", "element": "Physical/Gravity",
                "cell_key": r["cell_key"], "function": r["ctrl_function"],
            }
            insert_engine_key(
                kit_id=r["kit_id"],
                ctrl_treatment="damage", ctrl_function=r["ctrl_function"],
                def_bin=r["def_bin"], geometry_value=r["geometry_value"],
                delivery_value=r["delivery_value"], economy_model=r["economy_model"],
                activation_val=r["activation_val"], dependency_val=r["dependency_val"],
                cell_key=r["cell_key"], row_class="combat-kit",
                mob_skill_is_movement=r["mob_skill_is_movement"],
                mob_verbs=json.dumps(r["mob_verbs"]),
                ctrl_ailments_mapped=json.dumps([]), ctrl_ailment_gaps=json.dumps([]),
                def_riders=json.dumps([]), econ_gaps=json.dumps([]),
                flags=json.dumps(["r4-admission-2026-07-22"]),
                provenance_json=json.dumps({"mint": "r4-2026-07-22", "ruled_by": "matt-fold",
                                            "src": "pull-intrinsic-tranche-2026-07-15 + pull-7-docket-§2"}),
                raw_json=json.dumps(raw),
            )

        # --- di-druid-pvp-cc-stack-2026 (catalogue-only; cell_key NULL) ---
        insert_corpus(
            kit_id=DIDRUID["kit_id"], folk_name=DIDRUID["folk_name"], game="di",
            corpus_class="annex", source="canon",
            provenance_tag=DIDRUID["provenance_tag"], source_date=DIDRUID["source_date"],
            era_year=DIDRUID["era_year"], skill_debut_year=DIDRUID["skill_debut_year"],
            eras=DIDRUID["eras"], canon_tier="deep",
            negative=0, mint=0, dossier_owed=0, unresolved=1, is_system=0,
            pull_pending_vocab=0,
            ctrl_raw=DIDRUID["ctrl_raw"], elem_raw=DIDRUID["elem_raw"],
            source_urls=DIDRUID["source_urls"], mech_note=DIDRUID["mech_note"],
            flags=DIDRUID["flags"],
        )
        raw_di = {
            "kit_id": DIDRUID["kit_id"], "source": "legolas-recrawl-v1-2026-07-17",
            "game": "di", "ctrl_raw": DIDRUID["ctrl_raw"], "elem_raw": DIDRUID["elem_raw"],
            "note": "catalogue-only; cell_key derivation owed to E-lane; all-landed CC vocab",
        }
        insert_engine_key(
            kit_id=DIDRUID["kit_id"], row_class="combat-kit", cell_key=None,
            ctrl_ailments_mapped=json.dumps(["stun", "slow", "immobilize", "knockback", "damage-amp"]),
            ctrl_ailment_gaps=json.dumps([]),
            def_riders=json.dumps(["self-cc-immunity"]), econ_gaps=json.dumps([]),
            mob_verbs=json.dumps([]),
            flags=json.dumps(["r4-admission-2026-07-22", "catalogue-only-no-fit-input"]),
            provenance_json=json.dumps({"mint": "r4-2026-07-22", "ruled_by": "matt-fold",
                                        "src": "di-spiritform-ruling §Admission-candidate + legolas-recrawl-2026-07-17"}),
            raw_json=json.dumps(raw_di),
        )

        # =================================================================
        # B. RE-KEY  d2-ghost-pvp -> d2-ghost-assassin-pvp
        #    Cascade across every in-DB base table; add audit flag on the corpus row;
        #    update folk_name + source_urls; then the on-disk served artifact (E4).
        # =================================================================
        # enumerate per-table pre-counts for the report
        rekey_touch = {}
        for t in REKEY_TABLES:
            n = cur.execute(f"SELECT COUNT(*) FROM {t} WHERE kit_id=?", (REKEY_OLD,)).fetchone()[0]
            rekey_touch[t] = n

        # canon_corpus FIRST (PK) -- then children (FK off, manual cascade)
        cur.execute("UPDATE canon_corpus SET kit_id=? WHERE kit_id=?", (REKEY_NEW, REKEY_OLD))
        for t in REKEY_TABLES:
            if t == "canon_corpus":
                continue
            cur.execute(f"UPDATE {t} SET kit_id=? WHERE kit_id=?", (REKEY_NEW, REKEY_OLD))

        # folk_name already 'Ghost Assassin (WW/Trap)'; ensure it + stamp audit flag + source_urls
        rekey_urls = json.dumps([
            "https://www.purediablo.com/forums/threads/pvp-ww-ghost-assassin-guide-v2-0-by-tienje.1070/",
            "https://diablo2.diablowiki.net/Guide:PvP_C/C_WW_Shadow_Assassin_v1.10,_by_Voide",
            "https://www.items7.com/blog/how-to-build-a-ghost-sin-by-skibum/",
            "https://www.icy-veins.com/d2/whirlwind-assassin-whirlwindsin-build",
            "https://maxroll.gg/d2/guides/whirlwind-assassin",
        ])
        cur.execute(
            "UPDATE canon_corpus SET folk_name='Ghost Assassin (WW/Trap)', "
            "source_urls=?, "
            "flags=CASE WHEN flags IS NULL OR flags='' "
            "THEN 're-key-2026-07-22:d2-ghost-pvp->d2-ghost-assassin-pvp:matt-ruled-fold:legolas-mh-v3-recrawl' "
            "ELSE flags||',re-key-2026-07-22:d2-ghost-pvp->d2-ghost-assassin-pvp:matt-ruled-fold' END "
            "WHERE kit_id=?",
            (rekey_urls, REKEY_NEW),
        )

        # =================================================================
        # C. mint_ledger audit entries -- 6 operations.
        #    build_authorized=0 (admission/re-key of already-attested mechanics,
        #    NOT mechanism-mints). status='r4-admission-fold'. Distinguishable from
        #    the 12 mechanism-mints by status + build_authorized.
        # =================================================================
        ledger = []
        for r in LA_ROWS:
            ledger.append((
                "qualitative",
                f"R4 ROW-ADMISSION (Path-A supplementary mint into E4): {r['kit_id']} -- "
                f"Lost Ark Destroyer skill-grain pull-kit, function={r['ctrl_function']}, "
                f"cell_key VERBATIM from pull-7 docket §2. Already-attested vocabulary "
                f"(function=pull is a post-E1 census level; no NEW mechanism). corpus_class=annex.",
                json.dumps([r["kit_id"]]),
                "R4-FOLD :: Matt-ruled 2026-07-22 (three-run sheet §5). Source: pull-intrinsic "
                "tranche 2026-07-15 + pull-7 docket §2. NOT a mechanism-mint (build_authorized=0).",
                "r4-admission-fold", "A-attested", 0,
            ))
        ledger.append((
            "qualitative",
            f"R4 ROW-ADMISSION (catalogue-only): {DIDRUID['kit_id']} -- DI Druid PvP CC-stack, "
            "the real clean-shape row behind the di-spiritform phantom name. ALL-landed CC vocab "
            "(stun/slow/immobilize/knockback/damage-amp/self-cc-immunity); no NEW mechanism. "
            "cell_key NULL (E-derivation owed). corpus_class=annex. phantom row di-spiritform-druid-pvp untouched.",
            json.dumps([DIDRUID["kit_id"]]),
            "R4-FOLD :: Matt-ruled 2026-07-22. Source: di-spiritform ruling §Admission-candidate + "
            "legolas re-crawl 2026-07-17. NOT a mechanism-mint (build_authorized=0).",
            "r4-admission-fold", "A-attested", 0,
        ))
        ledger.append((
            "qualitative",
            f"R4 RE-KEY: {REKEY_OLD} -> {REKEY_NEW} (folk_name -> 'Ghost Assassin (WW/Trap)'). "
            "D2 PvP 'Ghost' is authoritatively the Assassin WW/Trap archetype (NOT Barb; docket "
            "speculation corrected). PK rename cascaded across 14 in-DB base tables + served "
            "artifact atlas-edition4.json points[40]. 585-conservation preserved (rename, not add/del). "
            "Frozen historical editions preserved as provenance.",
            json.dumps([REKEY_NEW]),
            "R4-FOLD :: Matt-ruled 2026-07-22. Path-A mechanics (E4 served re-key). Source: mh-v3 "
            "recrawl application-sheet §4. NOT a mechanism-mint (build_authorized=0).",
            "r4-admission-fold", "A-attested", 0,
        ))
        first_new_mint = pre["mint_ledger_max"] + 1
        for row in ledger:
            cur.execute(
                "INSERT INTO mint_ledger (mint_class, description, forced_by_kits, "
                "ladder_step_audit, status, evidence_tier, build_authorized, created_date) "
                "VALUES (?,?,?,?,?,?,?, '2026-07-22')", row,
            )
        last_new_mint = cur.execute("SELECT MAX(mint_id) FROM mint_ledger").fetchone()[0]

        # =================================================================
        # POST asserts (in-transaction, fail-loud -> rollback on any mismatch)
        # =================================================================
        post = {
            "corpus_total": scalar("SELECT COUNT(*) FROM canon_corpus"),
            "corpus_record": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='record'"),
            "corpus_annex": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='annex'"),
            "corpus_system": scalar("SELECT COUNT(*) FROM canon_corpus WHERE corpus_class='system'"),
            "engine_key_total": scalar("SELECT COUNT(*) FROM canon_engine_key"),
            "orphans_fwd": scalar("SELECT COUNT(*) FROM canon_engine_key ek LEFT JOIN canon_corpus cc ON ek.kit_id=cc.kit_id WHERE cc.kit_id IS NULL"),
            "orphans_rev": scalar("SELECT COUNT(*) FROM canon_corpus cc LEFT JOIN canon_engine_key ek ON cc.kit_id=ek.kit_id WHERE ek.kit_id IS NULL"),
            "ghost_old_left": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", REKEY_OLD),
            "ghost_new": scalar("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", REKEY_NEW),
            "ghost_old_anytable": sum(
                cur.execute(f"SELECT COUNT(*) FROM {t} WHERE kit_id=?", (REKEY_OLD,)).fetchone()[0]
                for t in REKEY_TABLES
            ),
            "new_mint_rows": scalar("SELECT COUNT(*) FROM mint_ledger WHERE status='r4-admission-fold'"),
            "la_cellkeys_present": scalar(
                "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE 'la-destroyer-%' AND cell_key IS NOT NULL"),
            "didruid_cellkey_null": scalar(
                "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id=? AND cell_key IS NULL", DIDRUID["kit_id"]),
        }
        checks = [
            ("corpus_total", 590), ("corpus_record", 267), ("corpus_annex", 304),
            ("corpus_system", 19), ("engine_key_total", 590),
            ("orphans_fwd", 0), ("orphans_rev", 0),
            ("ghost_old_left", 0), ("ghost_new", 1), ("ghost_old_anytable", 0),
            ("new_mint_rows", 6), ("la_cellkeys_present", 4), ("didruid_cellkey_null", 1),
        ]
        for k, want in checks:
            if post[k] != want:
                fail(f"POST assert {k}: expected {want}, got {post[k]} -- ROLLING BACK")

        # verify the 4 LA cell_keys are byte-exact to the docket
        for r in LA_ROWS:
            got = cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (r["kit_id"],)).fetchone()[0]
            if got != r["cell_key"]:
                fail(f"cell_key mismatch {r['kit_id']}:\n  want {r['cell_key']}\n  got  {got}")

        con.commit()
        print("COMMIT OK")
        print("POST-STATE:", json.dumps(post, indent=0))
        print(f"mint_ledger new ids: {first_new_mint}..{last_new_mint}")

    except Exception as e:
        con.rollback()
        fail(f"exception -> rolled back: {e}")

    # WAL checkpoint + integrity
    con.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    ic = con.execute("PRAGMA integrity_check;").fetchone()[0]
    con.close()
    if ic != "ok":
        fail(f"integrity_check = {ic}")
    print(f"integrity_check: {ic}")

    # =====================================================================
    # ON-DISK served artifact: atlas-edition4.json points[40].kit_id
    # (the CURRENT served / armed-E4 truth; frozen historical editions untouched)
    # =====================================================================
    with open(E4_JSON) as f:
        e4 = json.load(f)
    touched = 0
    for p in e4.get("points", []):
        if p.get("kit_id") == REKEY_OLD:
            p["kit_id"] = REKEY_NEW
            touched += 1
    if touched != 1:
        fail(f"atlas-edition4.json: expected exactly 1 point to re-key, found {touched}")
    with open(E4_JSON, "w") as f:
        json.dump(e4, f, ensure_ascii=False, indent=2)
    # verify no stray old key remains in E4
    with open(E4_JSON) as f:
        if REKEY_OLD in f.read():
            fail("atlas-edition4.json still contains old key after re-key")
    print(f"atlas-edition4.json: re-keyed {touched} point (points[40].kit_id)")

    print(f"DB md5   : {md5(DB)}  [post-write]")
    print("R4 MINT: DONE")


if __name__ == "__main__":
    main()
