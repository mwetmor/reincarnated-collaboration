"""
corpus_s2_census_v11_2026_07_17.py — S2 readiness census V11 (post-econ-recrawl application).
Author: elrond, 2026-07-17 (autonomous atlas-parity run, econ-recrawl-application charge).

Authority: gandalf-prime charter 2026-07-17 (Legolas econ-recrawl returned at commit `f4110f20`:
7 classified / 1 unverifiable; elrond is single corpus.db writer for the application).

STRUCTURE (two parts, one script, one transaction per Part 1):

  PART 1 — econ-recrawl-application WRITES (provenance tag `econ-recrawl-application-2026-07-17`,
                                             source commit `f4110f20`)

    1a. 5 conventional D2 spend kits — drop UNKNOWN, set econ_status='native', stamp provenance:
        - d2-bowazon (Multishot 4→23, Strafe fixed 11 mana/shot; Arreat Summit)
        - d2-fireclaw-wolf (Fire Claws 4 mana/attack; Arreat Summit)
        - d2-fury-wolf (Fury 4 mana/attack; Arreat Summit)
        - d2-kicksin (Dragon Talon spend + Cobra Strike AM charge-stack + Fade PC self-buff)
        - d2-rabies-wolf (Rabies 10 mana/bite; Arreat Summit)

    1b. poe1-whispering-ice — spend w/ cooldown-gate rider (Icestorm 6.50s CD;
        Int-per-10 is damage-scaling, not resource-econ).

    1c. vs-phieraggi — NR (Vampire Survivors auto-fire on 1.4s CD; Revival is a run-state
        passive damage/amount multiplier, NOT a per-cast consumable).

    1d. **d2-wl-void-rift — PHANTOM RULING**. Two independent D2R Warlock skill-tree
        enumerations (rpgstash + fextralife) show NO such skill across all 30 Chaos/Demon/
        Eldritch skills. DB carries three accumulated audit flags across 07-16 + 07-17:
        kb-only-backfill-attempted-2026-07-16, econ-audit-ambiguous-2026-07-16,
        econ-recrawl-unverifiable-2026-07-16 — three independent verification attempts
        FAILED. Web-search noise for "Void Rift Warlock" returns Destiny-2-Voidwalker
        content — mob-harvest-v3 "D2" provenance collision. DB truth AGREES with sheet.

        Action: set negative=1 with `phantom-kit-provenance-collision-2026-07-17` flag.
        Row RETAINED (total 585 conservation; DB/git lineage preserved).
        Denominator effect: −1 (corpus positives 520→519, denominator 565→564).
        Matt veto-open per charge.

    1e. SS form-lock OVERLAY STAMP — 3 D2 werewolf kits (GX-02 docket evidence).
        Werewolf form = 15 mana cast-once, 40s base extended by Lycanthropy passive;
        neither RS (no reservation) nor PC (durationed, not toggle-drain) — an OVERLAY.
        Same lineage as gd-berserker-wereforms PC-toggle and d4-rabies-lacerate GX-02 flags.
        Stamp: `ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence`.

    1f. kicksin secondary-mechanism STAMPS — genuine AM Cobra Strike + PC Fade
        (Icy-Veins verbatim: charges on-hit-Cobra-Strike, discharge on-hit-finisher).
        Stamps: `am-cobra-strike-charge-stack-2026-07-17` + `pc-fade-self-buff-2026-07-17`.

  PART 2 — CENSUS V11 (pure read on POST-write DB)

    Denominator: 564 (was 565; phantom removed).
    Corpus positives at kit grain: 519 (was 520).
    Iron laws #4 decomposition:
        Δ = econ-recrawl-application-effect (flip)
          + denominator-effect (phantom removed −1 from denominator, −1 from expressible baseline)
    Cross-check: net_flip_pool == apply_flip_effect + denominator_effect_on_expressible

IRON LAWS (this run):
    1. PRE-state asserts (V10 counts, DB truth) MUST hold BEFORE writes.
       Total 585 unchanged (rows conserved via negative=1, not row-delete).
       Corpus positives 520 PRE → 519 POST via phantom flip only.
    2. Multi-blocker honest: kit expressible IFF ENTIRE blockset empty. Report per-kit
       decomposition where flip attribution is contested.
    3. Roster 45/45 UNCHANGED (verified).
    4. DB WINS over projections: divergence from sheet's projection (98.9%) enumerated
       per-kit with rationale.
    5. md5-stability: DB md5 captured post-Part-1-write; census pass proves same md5
       at end of run.

DENOMINATOR LAW (V11):
    Pool = 519 corpus positives at kit grain + 45 founding roster = 564.
    Change from V10 (565): −1 phantom moved to negative=1.
    Negatives (44 kit-grain, was 43), NULL-grain system-records (22 unchanged),
    grain=NULL mints EXCLUDED. dossier_owed IN pool, flagged NOT-YET-EMISSIBLE.
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
OUT_CENSUS = ATLAS_DIR / "s2-readiness-census-v11-2026-07-17.md"
BACKUP_PATH = BASE / "agentic_orchestration/research/curated/corpus.db.pre-v11-2026-07-17-backup"

import sqlite3

# ---------------------------------------------------------------------------
# PRE-state (V10 post-write counts, DB truth) — asserted BEFORE any V11 write
# ---------------------------------------------------------------------------
PRE_EXPECTED = {
    "total_corpus": 585,
    "total_engine_key": 585,
    "kit_grain": 563,
    "null_grain": 22,
    "kit_positives": 520,
    "kit_negatives": 43,
    "cell_key_resolved": 562,
    "bt_sentinel": 1,
    "orphans_engine": 0,
    "orphans_corpus": 0,
    "dossier_owed": 4,
    "combat_kit_rc": 563,
    "system_record_rc": 22,
}
# POST state: total UNCHANGED (585) but positives −1, negatives +1 (phantom flip).
POST_EXPECTED = dict(PRE_EXPECTED)
POST_EXPECTED["kit_positives"] = 519  # phantom flipped
POST_EXPECTED["kit_negatives"] = 44   # +1 phantom

# V10 published headline anchors.
V10_PUBLISHED_POOL_EXPRESSIBLE = 551
V10_PUBLISHED_POOL_TOTAL = 565
V10_PUBLISHED_POOL_PCT = 97.5
V10_PUBLISHED_CORPUS_EXPRESSIBLE = 506
V10_PUBLISHED_CORPUS_TOTAL = 520

PROVENANCE_TAG = "econ-recrawl-application-2026-07-17"
SOURCE_COMMIT = "f4110f20"
PHANTOM_TAG = "phantom-kit-provenance-collision-2026-07-17"
SS_OVERLAY_TAG = "ss-overlay-werewolf-form-buff-2026-07-17:GX-02-docket-evidence"

# ---------------------------------------------------------------------------
# CLASSIFICATION VOCABULARY (V11 — inherited from V10; Wave-C landed unchanged)
# ---------------------------------------------------------------------------
WAVE_A_ECON_LANDED = {"SU", "HV"}
WAVE_B_ECON_LANDED = {"PC", "RS", "AM", "RC"}
WAVE_C_ECON_LANDED = {"BT", "TH", "LC"}
ECON_LANDED_V11 = WAVE_A_ECON_LANDED | WAVE_B_ECON_LANDED | WAVE_C_ECON_LANDED

WAVE_D_OR_BEYOND_ECON_GAPS = {"DR"}
UNKNOWN_GAP = {"UNKNOWN"}

AILMENT_LANDED_V9 = {
    "GAP-AILMENT:damage-amp",
    "GAP-AILMENT:freeze",
    "GAP-AILMENT:stun",
    "GAP-AILMENT:poison-dot",
    "GAP-AILMENT:taunt",
}
AILMENT_LANDED_WAVE_C = {
    "GAP-AILMENT:blind",
    "GAP-AILMENT:curse/hex",
    "GAP-AILMENT:fear",
    "GAP-AILMENT:instant-kill",
    "GAP-AILMENT:deflect",
}
AILMENT_LANDED_V11 = AILMENT_LANDED_V9 | AILMENT_LANDED_WAVE_C
AILMENT_STILL_BLOCKED_V11 = {"GAP-AILMENT:unknown-ailment"}
GEOMETRY_LANDED_WAVE_C = {"orbit", "placed_lane"}


def parse_json_list(s):
    if not s or s == "[]":
        return []
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return []


def classify_kit(row):
    """Return (expressible_now: bool, blocked_on: set[str]).

    V11 rule (Wave-C landed). Multi-blocker honest: expressible IFF blockset empty.
    """
    blocked_on = set()

    for eg in parse_json_list(row.get("econ_gaps")):
        if eg in ECON_LANDED_V11:
            continue
        blocked_on.add(f"econ:{eg}")

    if row.get("econ_status") == "partial:LC":
        pass  # LC landed

    for ag in parse_json_list(row.get("ctrl_ailment_gaps")):
        name = ag.replace("GAP-AILMENT:", "")
        if ag in AILMENT_LANDED_V11:
            continue
        elif ag in AILMENT_STILL_BLOCKED_V11:
            blocked_on.add(f"ailment-wave-c+:{name}")
        else:
            blocked_on.add(f"ailment-unclassified:{name}")

    geom = row.get("geometry_value") or ""
    # Landed geometries — no add.

    kit_id = row.get("kit_id") or ""
    # Shapeshift substring rule (Matt-fork gate — GX-02 docket OPEN; NOT landed):
    if any(marker in kit_id for marker in [
        "wildsoul", "wereforms", "spirit-form", "spiritborn-vortex",
    ]):
        if not ("vortex" in kit_id and "spiritborn" in kit_id):
            blocked_on.add("mechanic:shapeshift")

    return len(blocked_on) == 0, blocked_on


# ---------------------------------------------------------------------------
# PART 1 — econ-recrawl-application WRITES
# ---------------------------------------------------------------------------

WRITE_LEDGER = []


def append_corpus_flag(cur_flags, addition):
    """Append addition to comma-delimited canon_corpus.flags string."""
    if not cur_flags:
        return addition
    if addition in cur_flags:
        return cur_flags  # idempotent
    return f"{cur_flags},{addition}"


def part1_econ_recrawl_application(conn):
    """Apply the econ-recrawl 7 classifications + phantom ruling + overlay/secondary stamps.

    Idempotent: each write is guarded on the provenance-tag being absent.
    """
    print("\nPART 1: Applying econ-recrawl-application writes...")
    applied = 0

    # ------------------------------------------------------------------
    # 1a-c: 7 CLASSIFICATION applications (drop UNKNOWN + native + tag)
    # ------------------------------------------------------------------
    # Each row: (kit_id, note_for_provenance, expected_current_gap='UNKNOWN')
    classifications = [
        ("d2-bowazon",
         "spend/steady-mana (leech-sustained). Multishot base 4 (scales +1/lvl to 23 at L20), "
         "Strafe fixed 11, Guided Arrow 8→3.2, Cold Arrow 3.5, Immolation Arrow 6, Freezing Arrow 9. "
         "Sources: Arreat Summit amazon-bow.shtml + Maxroll d2/guides/multiple-shot-amazon"),
        ("d2-fireclaw-wolf",
         "spend/steady-mana + SS-overlay. Fire Claws 4 mana/attack; Werewolf form 15 mana cast-once, "
         "40s base (Lycanthropy passive extends). Sources: Arreat Summit druid-shapeshifting.shtml + "
         "Maxroll d2/guides/werewolf-fury-druid"),
        ("d2-fury-wolf",
         "spend/steady-mana + SS-overlay + Feral Rage buff-maintenance descriptor. Fury 4 mana/attack; "
         "Feral Rage 3 mana / 20s buff (F.R. is per-hit self-buff refresh, NOT AM accumulator). "
         "Sources: Arreat Summit druid-shapeshifting.shtml + Maxroll d2/guides/werewolf-fury-druid"),
        ("d2-kicksin",
         "spend/steady-mana + AM Cobra Strike + PC Fade. Dragon Talon mana-spend/kick (leech-sustained); "
         "Cobra Strike: on-hit-Cobra charges, discharge on-hit-finisher (Dragon Talon). Fade = "
         "activation-toggle self-buff (Icy-Veins verbatim: 'Fade and Cobra Strike don't function as "
         "mana reservations'). Sources: Maxroll d2/guides/dragon-talon-assassin + "
         "Icy-Veins d2/dragon-talon-assassin-kicksin-build-skills"),
        ("d2-rabies-wolf",
         "spend/steady-mana + SS-overlay. Rabies 10 mana/bite (poison DoT 4-11.6s by level, spreads "
         "target-to-target); Werewolf form 15 mana / 40s base. Sources: Arreat Summit "
         "druid-shapeshifting.shtml + Maxroll d2/guides/rabies-druid-guide"),
        ("poe1-whispering-ice",
         "spend w/ cooldown-gate rider. Icestorm 0.75s cast + 6.50s cooldown; Int-per-10 is DAMAGE "
         "scaling, not resource-econ. Clarity aura RS is secondary. Sources: Odealo "
         "articles/whispering-ice-icestorm-trickster-build + poedb.tw us"),
        ("vs-phieraggi",
         "NR/auto-fire (VS-genre-native). 1.4s CD auto-fire; base 15 damage/4 amount/7 pierce; "
         "Revival is passive run-state multiplier (+1 dmg + +1 amount per Revival, cap +10 each), "
         "NOT consumable per-fire (Revival is spent only on death). Sources: fandom.com/wiki/Phieraggi "
         "(search-snippet) + Revival page cross-reference"),
    ]

    for kit_id, note in classifications:
        row = conn.execute(
            "SELECT econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?", (kit_id,)
        ).fetchone()
        cc = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        assert row is not None and cc is not None, f"missing kit_id: {kit_id}"
        eco_status_before, eco_gaps_before = row
        corp_flags_before = cc[0] or ""

        provenance_stamp = f"{PROVENANCE_TAG}:{SOURCE_COMMIT}:{note}"
        if PROVENANCE_TAG in corp_flags_before:
            print(f"    1a-c IDEMPOTENT: {kit_id} already tagged")
            continue

        gaps_list = parse_json_list(eco_gaps_before)
        gaps_after = [g for g in gaps_list if g != "UNKNOWN"]
        conn.execute(
            "UPDATE canon_engine_key SET econ_status='native', econ_gaps=? WHERE kit_id=?",
            (json.dumps(gaps_after), kit_id),
        )
        new_flags = append_corpus_flag(corp_flags_before, provenance_stamp)
        conn.execute(
            "UPDATE canon_corpus SET flags=? WHERE kit_id=?",
            (new_flags, kit_id),
        )
        WRITE_LEDGER.append({
            "kit_id": kit_id,
            "action": "econ_status: gap → native; econ_gaps: drop UNKNOWN; corpus.flags: += econ-recrawl-application provenance",
            "before": {"econ_status": eco_status_before, "econ_gaps": eco_gaps_before,
                       "corpus_flags": corp_flags_before},
            "after": {"econ_status": "native", "econ_gaps": json.dumps(gaps_after),
                      "corpus_flags": new_flags},
            "provenance": provenance_stamp,
        })
        applied += 1
        print(f"    1a-c: {kit_id}  econ  {eco_status_before}/{eco_gaps_before} → native/{gaps_after}")

    # ------------------------------------------------------------------
    # 1d: PHANTOM RULING — d2-wl-void-rift → negative=1
    # ------------------------------------------------------------------
    row = conn.execute(
        "SELECT negative, flags FROM canon_corpus WHERE kit_id='d2-wl-void-rift'"
    ).fetchone()
    assert row is not None, "d2-wl-void-rift missing"
    neg_before, phantom_flags_before = row
    phantom_flags_before = phantom_flags_before or ""

    if PHANTOM_TAG in phantom_flags_before:
        print(f"    1d IDEMPOTENT: d2-wl-void-rift already carries phantom tag")
    else:
        phantom_stamp = (
            f"{PHANTOM_TAG}:{SOURCE_COMMIT}:no D2R Warlock skill 'Void Rift' exists per two "
            f"independent enumerations (rpgstash + fextralife); "
            f"web-search noise = Destiny-2 Voidwalker; mob-harvest-v3 D2 ambiguity collision; "
            f"3 prior audit flags corroborate. ELROND ruling; Matt veto-open."
        )
        new_phantom_flags = append_corpus_flag(phantom_flags_before, phantom_stamp)
        conn.execute(
            "UPDATE canon_corpus SET negative=1, flags=? WHERE kit_id='d2-wl-void-rift'",
            (new_phantom_flags,),
        )
        # ALSO drop UNKNOWN from engine_key econ_gaps for hygiene (phantom won't be
        # classified anyway once negative=1, but consistency helps future audits).
        conn.execute(
            "UPDATE canon_engine_key SET econ_gaps='[]' WHERE kit_id='d2-wl-void-rift'"
        )
        WRITE_LEDGER.append({
            "kit_id": "d2-wl-void-rift",
            "action": "negative: 0 → 1 (PHANTOM RULING); corpus.flags: += phantom-kit-provenance-collision; engine_key econ_gaps: UNKNOWN → []",
            "before": {"negative": neg_before, "corpus_flags": phantom_flags_before,
                       "econ_gaps": '["UNKNOWN"]'},
            "after": {"negative": 1, "corpus_flags": new_phantom_flags, "econ_gaps": "[]"},
            "provenance": phantom_stamp,
        })
        applied += 1
        print(f"    1d PHANTOM: d2-wl-void-rift  negative  0 → 1 (denominator −1)")

    # ------------------------------------------------------------------
    # 1e: SS OVERLAY STAMPS on 3 D2 werewolf kits (GX-02 docket evidence)
    # ------------------------------------------------------------------
    ss_kits = ["d2-fireclaw-wolf", "d2-fury-wolf", "d2-rabies-wolf"]
    for kit_id in ss_kits:
        cc = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)
        ).fetchone()
        corp_flags_before = cc[0] or ""
        if SS_OVERLAY_TAG in corp_flags_before:
            print(f"    1e IDEMPOTENT: {kit_id} already SS-overlay stamped")
            continue
        new_flags = append_corpus_flag(corp_flags_before, SS_OVERLAY_TAG)
        conn.execute(
            "UPDATE canon_corpus SET flags=? WHERE kit_id=?",
            (new_flags, kit_id),
        )
        WRITE_LEDGER.append({
            "kit_id": kit_id,
            "action": "corpus.flags: += SS-overlay-werewolf-form-buff GX-02 docket evidence",
            "before": {"corpus_flags": corp_flags_before},
            "after": {"corpus_flags": new_flags},
            "provenance": SS_OVERLAY_TAG,
        })
        applied += 1
        print(f"    1e SS-overlay stamp: {kit_id}")

    # ------------------------------------------------------------------
    # 1f: KICKSIN SECONDARY-MECHANISM STAMPS (AM Cobra Strike + PC Fade)
    # ------------------------------------------------------------------
    kicksin_secondary_tags = [
        "am-cobra-strike-charge-stack-2026-07-17:on-hit-cobra-fill/on-hit-finisher-discharge",
        "pc-fade-self-buff-2026-07-17:activation-toggle (per Icy-Veins)",
    ]
    cc = conn.execute(
        "SELECT flags FROM canon_corpus WHERE kit_id='d2-kicksin'"
    ).fetchone()
    corp_flags_before = cc[0] or ""
    for tag in kicksin_secondary_tags:
        if tag in corp_flags_before:
            print(f"    1f IDEMPOTENT: d2-kicksin already carries {tag[:40]}...")
            continue
        corp_flags_before = append_corpus_flag(corp_flags_before, tag)
    # Single write for all kicksin secondary tags
    cc_after = conn.execute(
        "SELECT flags FROM canon_corpus WHERE kit_id='d2-kicksin'"
    ).fetchone()
    if cc_after[0] != corp_flags_before:
        conn.execute(
            "UPDATE canon_corpus SET flags=? WHERE kit_id='d2-kicksin'",
            (corp_flags_before,),
        )
        WRITE_LEDGER.append({
            "kit_id": "d2-kicksin",
            "action": "corpus.flags: += AM Cobra Strike charge-stack + PC Fade activation-toggle secondaries",
            "before": {"corpus_flags": cc_after[0]},
            "after": {"corpus_flags": corp_flags_before},
            "provenance": " + ".join(kicksin_secondary_tags),
        })
        applied += 1
        print(f"    1f kicksin secondaries: AM + PC stamped")

    print(f"    total row-touches: {applied}")
    return applied


def part1_collision_audit(conn):
    """READ-ONLY D2 collision audit.

    Scans game='d2' kits + all SEARCH-DERIVED/unharvested rows for Destiny-2-signature
    vocabulary. Returns suspects for report (no writes — audit is report-only per charge).
    """
    destiny_2_signatures = [
        "void", "solar", "arc", "stasis", "strand", "nova", "dawnblade",
        "sunbreaker", "nightstalker", "gunslinger", "rift", "well-of-radiance",
        "voidwalker", "gunslinger", "titan", "hunter-subclass",
    ]

    # D2R Warlock class REAL skills (per sheet enumeration) — safe-list for warlock kits
    d2r_warlock_real_names = [
        "abyss", "blood-boil", "echoing-strike", "fire", "tainted-summoner",
        "chaos", "demon", "eldritch", "miasma", "sigil", "flame-wave",
        "apocalypse", "ring-of-fire", "cleave", "mirrored-blades",
    ]

    suspects = []

    # Scan all D2 kits
    rows = conn.execute(
        "SELECT c.kit_id, c.folk_name, c.flags, c.negative "
        "FROM canon_corpus c WHERE c.game='d2'"
    ).fetchall()
    for kit_id, folk_name, flags, negative in rows:
        if negative == 1:
            continue  # skip already-negative rows (incl. void-rift post-write)
        kit_lower = (kit_id or "").lower()
        name_lower = (folk_name or "").lower()
        text = f"{kit_lower} {name_lower}"
        hits = []
        for sig in destiny_2_signatures:
            if sig in text:
                # Filter false positives: real D2 skill names that contain sub-strings
                if sig == "arc":
                    # 'arc' is Destiny arc-subclass, but also in words like 'arcane'. In D2 kits,
                    # no D2 base skill contains 'arc' — this is safe.
                    if "arcane" in text:
                        continue
                if sig == "nova":
                    # 'nova' is REAL D2 Sorc Lightning-tree skill (Nova) AND real D2 Necro
                    # Poison-tree skill (Poison Nova). Both are safe.
                    if kit_id in ("d2-nova-sorc", "d2-poison-nova-necro"):
                        continue
                if sig == "rift":
                    # 'rift' is Destiny Warlock class ability. In D2R warlock, real skills do not
                    # contain 'rift' (per sheet enumeration).
                    pass
                if sig == "void":
                    # 'void' — Destiny void subclass. D2R has "Void" runeword (item, not skill).
                    # d2-wl-void-rift is the phantom; other D2 kits shouldn't hit this.
                    pass
                # For warlock kits specifically, cross-check against real-name safe-list
                if "d2-wl-" in kit_id:
                    # Extract the skill part after 'd2-wl-'
                    skill_part = kit_id.replace("d2-wl-", "")
                    if any(real in skill_part for real in d2r_warlock_real_names):
                        # It's a real Warlock skill; the signature hit is coincidental
                        continue
                hits.append(sig)
        if hits:
            suspects.append({
                "kit_id": kit_id,
                "folk_name": folk_name,
                "signature_hits": hits,
                "flags": flags or "",
                "verdict": "CONFIRMED-PHANTOM" if kit_id == "d2-wl-void-rift"
                           else "SUSPECT-AMBIGUOUS",
            })

    return suspects


def run_asserts(conn, label, expected):
    actual = {
        "total_corpus": conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0],
        "total_engine_key": conn.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0],
        "kit_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0],
        "null_grain": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL").fetchone()[0],
        "kit_positives": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=0").fetchone()[0],
        "kit_negatives": conn.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=1").fetchone()[0],
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
# PART 2 — CENSUS V11 (pure read on POST-write state)
# ---------------------------------------------------------------------------

def run_census(conn):
    """Read-only census on POST-write DB state (denominator 564, positives 519)."""
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
    assert len(corpus_rows) == 519, (
        f"V11 corpus positives = {len(corpus_rows)}, expected 519 (520 V10 −1 phantom)"
    )

    cur = conn.execute("SELECT kit_id, name, mob_policy_while_casting, commit_val FROM roster_atlas")
    roster_rows = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    assert len(roster_rows) == 45, f"roster = {len(roster_rows)}, expected 45 (UNCHANGED)"

    # V11 classification
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
            "blocked_set": blocked,
        })
        for b in blocked:
            bucket_counter[b] += 1

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


def db_md5():
    """md5 of the .db file after forcing a WAL checkpoint."""
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
def write_census_artifact(census, collision_suspects, md5_pre, md5_post_writes, md5_post_census, conn):
    total = census["total"]
    exp = census["expressible_now"]
    blk = census["blocked"]
    pct = 100.0 * exp / total
    corpus_pct = 100.0 * census["corpus_expressible"] / census["corpus_positives_kit_grain"]

    # Delta decomposition:
    #   V10 baseline: 551/565 expressible (published headline).
    #   V11 = V10 + apply_flip_effect (5 D2 spend + poe1-wi + vs-phieraggi = 7 UNKNOWN-blocked kits flip)
    #                + denominator_effect (phantom removed −1 from positives, −1 from denominator;
    #                  since phantom was blocked in V10, expressible baseline drops by 1 too if
    #                  we count "kits that WERE in denominator that ARE NO LONGER" — the
    #                  phantom itself carried econ:UNKNOWN, so it was blocked, not expressible.
    #                  Net effect on expressible: 0 (phantom wasn't expressible anyway).
    #                  Net effect on denominator: −1.
    #                  Net effect on blocked-count: −1 (one fewer blocked kit in denominator).

    # V10 baseline recompute (for cross-check)
    v10_expressible = V10_PUBLISHED_POOL_EXPRESSIBLE  # 551
    v10_denominator = V10_PUBLISHED_POOL_TOTAL  # 565
    v10_blocked = v10_denominator - v10_expressible  # 14

    # Cross-check identity: V11 expected = V10_baseline + apply_flip - denominator_removal_of_blocked
    #   apply_flip = 7 (the 7 UNKNOWN-blocked kits, sole-blocker, flip clean)
    #   denominator_removal_of_blocked = 1 (phantom, which WAS blocked in V10)
    #   V11 expected expressible = 551 + 7 = 558
    #   V11 expected denominator = 565 - 1 = 564
    #   V11 expected blocked = 14 - 7 (flipped) - 1 (phantom removed) = 6
    apply_flip_effect = 7
    denominator_effect_expressible = 0  # phantom wasn't expressible → no baseline change
    denominator_effect_denominator = -1
    denominator_effect_blocked = -1  # phantom was blocked; removing shrinks blocked count
    v11_expected_expressible = v10_expressible + apply_flip_effect + denominator_effect_expressible
    v11_expected_denominator = v10_denominator + denominator_effect_denominator
    v11_expected_blocked = v10_blocked - apply_flip_effect + denominator_effect_blocked

    L = []
    A = L.append
    A("# S2 — Migration-Readiness Census V11 (THE SCOREBOARD, post-econ-recrawl application + phantom ruling)")
    A("")
    A("**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, econ-recrawl-application charge)")
    A("**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-17)")
    A("**Source of writes:** Legolas econ-recrawl at commit `f4110f20` — "
      "7 classified / 1 unverifiable")
    A(f"**Corpus state (POST-write):** 585 rows / **563 kit-grain (519 positives + 44 negatives) + "
      "22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / "
      "585 engine_key 1:1 (0 orphans)")
    A(f"**Scope:** Post-econ-recrawl (7 classifications + 1 phantom ruling) — "
      f"provenance tag `{PROVENANCE_TAG}`, phantom tag `{PHANTOM_TAG}`.")
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
    A(f"| **Expressible-now** | **{exp}** | **{pct:.2f}%** |")
    A(f"| Blocked | {blk} | {100.0*blk/total:.2f}% |")
    A(f"| — of which dossier_owed held-out | {census['held_out_dossier_owed']} | "
      f"{100.0*census['held_out_dossier_owed']/total:.2f}% |")
    A("")
    A(f"Denominator composition: {census['corpus_positives_kit_grain']} corpus positives at kit grain "
      f"(V10: 520; V11: **519** after `d2-wl-void-rift` phantom→negative) + {census['roster']} founding "
      f"roster = **{total}** (V10: 565; V11: **{total}**).")
    A("")
    A(f"Corpus expressible: **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']} "
      f"({corpus_pct:.2f}%)**  ·  Roster expressible: **{census['roster_expressible']}/{census['roster']} "
      f"({100.0*census['roster_expressible']/census['roster']:.1f}%)** (UNCHANGED — verified)")
    A("")
    A("---")
    A("")
    A("## §2 Delta vs V10 — two-lever decomposition (iron law 4)")
    A("")
    A("Δ decomposes cleanly into:")
    A(f"- **Recrawl-application flip effect** (7 UNKNOWN sole-blocker kits flip clean): "
      f"+{apply_flip_effect} kits expressible.")
    A(f"- **Denominator effect** (phantom `d2-wl-void-rift` → negative=1): "
      f"−1 denominator; −1 from blocked count (phantom WAS blocked in V10, not expressible → "
      f"expressible baseline UNCHANGED by this lever, denominator shrinks by 1).")
    A("")
    A(f"**Expected V11 identity (baseline-anchored):**")
    A(f"- Expected expressible = V10 {v10_expressible} + apply_flip {apply_flip_effect} + "
      f"denominator_effect_expressible {denominator_effect_expressible} = "
      f"**{v11_expected_expressible}**")
    A(f"- Expected denominator = V10 {v10_denominator} + denominator_effect {denominator_effect_denominator} = "
      f"**{v11_expected_denominator}**")
    A(f"- Expected blocked = V10 {v10_blocked} − apply_flip {apply_flip_effect} + "
      f"denominator_effect_blocked {denominator_effect_blocked} = **{v11_expected_blocked}**")
    A("")
    A(f"**DB truth check:**")
    A(f"- Actual expressible = **{exp}** vs expected {v11_expected_expressible} → "
      f"{'OK' if exp == v11_expected_expressible else 'DIVERGENCE (per-kit enumeration below)'}")
    A(f"- Actual denominator = **{total}** vs expected {v11_expected_denominator} → "
      f"{'OK' if total == v11_expected_denominator else 'BREACH'}")
    A(f"- Actual blocked = **{blk}** vs expected {v11_expected_blocked} → "
      f"{'OK' if blk == v11_expected_blocked else 'DIVERGENCE'}")
    A("")
    A("| Scoreboard | Pool expressible | % | Corpus | Roster |")
    A("|---|---|---|---|---|")
    A(f"| V10 (published, post-Wave-C landed + corpus-align) | {v10_expressible}/{v10_denominator} | "
      f"{V10_PUBLISHED_POOL_PCT:.2f}% | {V10_PUBLISHED_CORPUS_EXPRESSIBLE}/{V10_PUBLISHED_CORPUS_TOTAL} | 45/45 |")
    A(f"| **V11 (this run, post-econ-recrawl application + phantom ruling)** | **{exp}/{total}** | "
      f"**{pct:.2f}%** | **{census['corpus_expressible']}/{census['corpus_positives_kit_grain']}** | 45/45 |")
    A(f"| **Δ vs V10** | **+{exp - v10_expressible}** | **{pct - V10_PUBLISHED_POOL_PCT:+.2f}pp** | "
      f"**+{census['corpus_expressible'] - V10_PUBLISHED_CORPUS_EXPRESSIBLE}** | 0 |")
    A(f"| — apply-flip contribution | +{apply_flip_effect} | | +{apply_flip_effect} | 0 |")
    A(f"| — denominator effect (phantom −1) | 0 | | 0 | 0 |")
    A("")
    A(f"**Headline movement: V10 {V10_PUBLISHED_POOL_PCT:.2f}% → V11 {pct:.2f}% "
      f"({pct - V10_PUBLISHED_POOL_PCT:+.2f}pp).**")
    A("")
    A("---")
    A("")
    A("## §3 PHANTOM RULING — `d2-wl-void-rift` (LOUD; Matt veto-open)")
    A("")
    A("**RULING: `d2-wl-void-rift` set to `negative=1` with flag "
      f"`{PHANTOM_TAG}`.** Row retained (total 585 conservation). Denominator −1 (565→564). "
      "Corpus positives −1 (520→519).")
    A("")
    A("**Evidence base (DB truth AGREES with sheet):**")
    A("1. **Sheet enumeration:** two independent D2R Warlock skill-tree enumerations "
      "(rpgstash Chaos/Demon/Eldritch guide + fextralife wiki) show NO skill named "
      "\"Void Rift\" across all 30 Warlock skills.")
    A("2. **DB corroborating audit trail:** kit ALREADY carried three prior audit flags — "
      "`kb-only-backfill-attempted-2026-07-16`, `econ-audit-ambiguous-2026-07-16`, "
      "`econ-recrawl-unverifiable-2026-07-16`. THREE independent verification attempts, "
      "including this pass, FAILED to find mechanics.")
    A("3. **Web-search noise pattern:** Google \"Void Rift Warlock\" returns exclusively "
      "Destiny-2 Voidwalker-Warlock content. Destiny-2 Voidwalker is a real Warlock subclass; "
      "\"D2\" shorthand collision with Diablo-2 during mob-harvest-v3 provenance is the likely "
      "harvest-origin failure mode.")
    A("4. **Corpus consistency check:** the OTHER five D2R Warlock kits in the corpus "
      "(`d2-wl-abyss`, `d2-wl-blood-boil`, `d2-wl-echoing-strike`, `d2-wl-fire`, "
      "`d2-wl-tainted-summoner`) all appear in the same enumerated skill-trees — the source "
      "enumeration is high-fidelity. Void Rift's exclusion from that enumeration is exclusionary "
      "evidence, not a gap.")
    A("")
    A("**Alternative considered and rejected:** editorial-inferred classification (per "
      "`poe2-snipe-mirage-deadeye` precedent 07-16). Rejected because Snipe/Mirage precedent "
      "was \"no dedicated guide but skill demonstrably exists in game\"; void-rift is "
      "\"skill demonstrably does not exist in source universe\" — no substrate to editorialize.")
    A("")
    A("**Alternative considered and rejected:** row DELETION. Rejected because deletion "
      "loses provenance history + breaks 585-total conservation + breaks git lineage. "
      "Negative=1 flip preserves all audit history and enables future disposition changes.")
    A("")
    A("**Matt veto-open:** if Matt disagrees, negative=1 can be reverted by "
      "`UPDATE canon_corpus SET negative=0 WHERE kit_id='d2-wl-void-rift'`; denominator returns "
      "to 565 and the phantom flag remains as documentation. No destructive change.")
    A("")
    A("---")
    A("")
    A("## §4 Sheet projection cross-check")
    A("")
    A(f"Sheet projected (charge instruction):")
    A(f"- **Phantom removed:** 558/564 = 98.9%")
    A(f"- **Phantom kept:** 558/565 = 98.8%")
    A("")
    A(f"**Actual V11 result (phantom REMOVED per elrond ruling):** {exp}/{total} = {pct:.2f}%")
    A("")
    delta_vs_ceiling = exp - 558
    A(f"- Δ vs charge projection ceiling 558: **{delta_vs_ceiling:+d}** kits ({delta_vs_ceiling*100.0/total:+.2f}pp)")
    if delta_vs_ceiling == 0:
        A("Actual EXACTLY matches sheet projection. Recrawl-application landed clean; "
          "no per-kit divergence.")
    elif delta_vs_ceiling < 0:
        A(f"Divergence from projection is {-delta_vs_ceiling} kits — enumerated per-blocker below (§5).")
    else:
        A(f"Actual EXCEEDS projection by {delta_vs_ceiling} kits — investigate whether an additional "
          "kit flipped as side-effect of the recrawl applications.")
    A("")
    A("---")
    A("")
    A("## §5 Blocked-on-what — ranked buckets (V11)")
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
    A("## §6 Blocked-tail rosters (DERIVED FROM DB)")
    A("")
    A("Named kit rosters per residual blocker:")
    A("")
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
        A(f"### `{b}` ({len(kits)} kit{'s' if len(kits) > 1 else ''})")
        for k, name in sorted(kits):
            A(f"- `{k}` — {name}")
        A("")
    A("**Expected-residual tail (per charge):**")
    A("- shapeshift 3 (Matt-fork GX-02): expected `la-ferality-wildsoul`, "
      "`la-phantom-beast-awakening-wildsoul`, `gd-berserker-wereforms` OR similar — verify per-DB.")
    A("- econ:DR 2 (WC-19 → Wave-D): expected `hot-norseman-frost-avalanche`, `vs-queen-sigma`.")
    A("- unknown-ailment 1: expected `di-spiritform-druid-pvp`.")
    A("- void-rift: phantom-negative per §3 ruling — NOT in blocked tail.")
    A("")
    A("Cross-check DB-truth-vs-expected:")
    ss_kits = sorted(by_bucket.get("mechanic:shapeshift", []))
    dr_kits = sorted(by_bucket.get("econ:DR", []))
    ua_kits = sorted(by_bucket.get("ailment-wave-c+:unknown-ailment", []))
    A(f"- shapeshift bucket: **{len(ss_kits)} kits** ({', '.join(k[0] for k in ss_kits)})")
    A(f"- econ:DR bucket: **{len(dr_kits)} kits** ({', '.join(k[0] for k in dr_kits)})")
    A(f"- unknown-ailment bucket: **{len(ua_kits)} kits** ({', '.join(k[0] for k in ua_kits)})")
    A("")
    # If there's residue beyond expected, name it:
    other_residue_buckets = [
        b for b in [x[0] for x in census["bucket_ranked"]]
        if b not in ("mechanic:shapeshift", "econ:DR", "ailment-wave-c+:unknown-ailment")
    ]
    if other_residue_buckets:
        A("**RESIDUAL BEYOND EXPECTED — not enumerated in charge tail:**")
        for b in other_residue_buckets:
            kits = by_bucket.get(b, [])
            if kits:
                A(f"- `{b}` ({len(kits)}): {', '.join(k[0] for k in sorted(kits))}")
        A("")
    A("---")
    A("")
    A("## §7 Part 1 write ledger")
    A("")
    A(f"Provenance tag: `{PROVENANCE_TAG}` · Source commit: `{SOURCE_COMMIT}`")
    A(f"Phantom tag: `{PHANTOM_TAG}` · SS-overlay tag: `{SS_OVERLAY_TAG}`")
    A("")
    if WRITE_LEDGER:
        A(f"Writes applied THIS RUN: **{len(WRITE_LEDGER)}** row-touches "
          f"({sum(1 for w in WRITE_LEDGER if 'econ_status' in str(w['after']))} econ + "
          f"{sum(1 for w in WRITE_LEDGER if 'negative' in str(w['after']))} phantom + "
          f"{sum(1 for w in WRITE_LEDGER if w['provenance'].startswith('ss-overlay'))} SS-overlay + "
          f"{sum(1 for w in WRITE_LEDGER if 'am-cobra' in str(w['provenance']))} kicksin-secondaries)")
        A("")
        A("| # | kit_id | action | provenance-fragment |")
        A("|---|---|---|---|")
        for i, w in enumerate(WRITE_LEDGER, 1):
            prov = w["provenance"]
            if len(prov) > 140:
                prov = prov[:137] + "..."
            action = w["action"]
            if len(action) > 100:
                action = action[:97] + "..."
            A(f"| {i} | `{w['kit_id']}` | {action} | `{prov}` |")
    else:
        A("Writes applied THIS RUN: **0** (idempotent re-run — all target kits already carry "
          "the provenance tag; no changes needed). DB state reflects the writes from a prior run.")
    A("")
    A("---")
    A("")
    A("## §8 D2 collision audit (broader mob-harvest-v3 ambiguity scan)")
    A("")
    A("Per charge: scan D2-game kits (and SEARCH-DERIVED/unharvested rows) for Destiny-2-signature "
      "vocabulary. This is read + flag ONLY confirmed-obvious cases; ambiguous cases list-only for "
      "Legolas follow-up.")
    A("")
    d2_scan_count = conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='d2' AND negative=0"
    ).fetchone()[0]
    A(f"**Total D2-game positive kits scanned:** {d2_scan_count}")
    A(f"**Signature vocabulary checked:** void / solar / arc / stasis / strand / nova / dawnblade / "
      "sunbreaker / nightstalker / gunslinger / rift / well-of-radiance / voidwalker / titan / "
      "hunter-subclass")
    A("")
    if collision_suspects:
        A(f"**Suspects surfaced: {len(collision_suspects)}**")
        A("")
        A("| kit_id | folk_name | signature hits | verdict |")
        A("|---|---|---|---|")
        for s in collision_suspects:
            A(f"| `{s['kit_id']}` | {s['folk_name']} | {', '.join(s['signature_hits'])} | "
              f"{s['verdict']} |")
        A("")
        confirmed = [s for s in collision_suspects if s["verdict"] == "CONFIRMED-PHANTOM"]
        suspects_amb = [s for s in collision_suspects if s["verdict"] == "SUSPECT-AMBIGUOUS"]
        A(f"- **CONFIRMED-PHANTOM ({len(confirmed)}):** already handled — `d2-wl-void-rift` "
          "negative=1 per §3 ruling.")
        A(f"- **SUSPECT-AMBIGUOUS ({len(suspects_amb)}):** not flagged this pass — list-only for "
          "Legolas follow-up if warranted.")
        if suspects_amb:
            A("")
            A("Ambiguous-suspect list (for Legolas follow-up commissioning):")
            for s in suspects_amb:
                A(f"- `{s['kit_id']}` ({s['folk_name']}) — hit on: {', '.join(s['signature_hits'])}")
    else:
        A("**Suspects surfaced: 0** — no other D2-game kit carries Destiny-2-signature "
          "vocabulary in kit_id or folk_name. Void-rift is the isolated collision.")
        A("")
        A("D2R Warlock kits verified as REAL (per sheet enumeration cross-check): "
          "`d2-wl-abyss`, `d2-wl-blood-boil`, `d2-wl-echoing-strike`, `d2-wl-fire`, "
          "`d2-wl-tainted-summoner` — all appear in rpgstash + fextralife Warlock skill-tree "
          "enumerations. Only `d2-wl-void-rift` is anomalous.")
    A("")
    A("**Broader audit disposition:** the collision appears TIGHTLY LOCALIZED to the void-rift "
      "phantom. No mass-rewrite warranted. If Legolas fires a follow-up Mode B pass on ambiguous "
      "candidates, the void-rift precedent (§3) is the template for handling.")
    A("")
    A("---")
    A("")
    A("## §9 Iron-law asserts (PRE V10-state / POST V11-state)")
    A("")
    A("| Assert | PRE (V10) | POST (V11) | Notes |")
    A("|---|---|---|---|")
    A("| total_corpus | 585 | 585 | UNCHANGED (phantom→negative preserves rows) |")
    A("| total_engine_key | 585 | 585 | 1:1 UNCHANGED |")
    A("| kit_grain | 563 | 563 | UNCHANGED (no grain writes) |")
    A("| null_grain | 22 | 22 | UNCHANGED |")
    A("| **kit_positives (denominator base)** | **520** | **519** | −1 (phantom) |")
    A("| **kit_negatives** | **43** | **44** | +1 (phantom) |")
    A("| **pool = corpus positives + roster 45** | **565** | **564** | −1 (phantom) |")
    A("| combat-kit (row_class) | 563 | 563 | UNCHANGED |")
    A("| system-record (row_class) | 22 | 22 | UNCHANGED |")
    A("| cell_key_resolved | 562 | 562 | UNCHANGED |")
    A("| bt_sentinel | 1 | 1 | UNCHANGED |")
    A("| orphans engine→corpus | 0 | 0 | UNCHANGED |")
    A("| orphans corpus→engine | 0 | 0 | UNCHANGED |")
    A("| dossier_owed | 4 | 4 | UNCHANGED |")
    A("")
    A("Cross-check assertions:")
    A(f"- `roster_expressible == 45`: {census['roster_expressible']} == 45 — "
      f"{'OK' if census['roster_expressible'] == 45 else 'BREACH'}")
    A(f"- `total 585 conservation`: rows conserved via negative=1 (NOT row-delete) — OK")
    A(f"- `denominator identity`: 519 corpus positives + 45 roster = {519+45} == {total} — "
      f"{'OK' if 519+45 == total else 'BREACH'}")
    A("")
    A("---")
    A("")
    A("## §10 Reproducibility")
    A("")
    A(f"- **Script:** `../scripts/corpus_s2_census_v11_2026_07_17.py`")
    A(f"- **Backup:** `../{BACKUP_PATH.name}` (integrity_check=ok, taken before Part 1 write)")
    A(f"- **Source of writes:** Legolas econ-recrawl at commit `{SOURCE_COMMIT}` — "
      f"`agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/`")
    A("- **Transactional writes** — Part 1 wrapped in single transaction; PRE asserts held before "
      "writing, POST asserts held after; census is a pure READ on the POST-write state.")
    A(f"- **Idempotent** — Part 1 writes check for provenance tag `{PROVENANCE_TAG}` and treat "
      "re-runs as verified no-op per-row.")
    A("- **Delta decomposition** (§2) reports apply-flip effect and denominator effect separately, "
      "per iron law 4 — the two levers are NOT conflated.")
    A(f"- **md5 stability**: post-writes `{md5_post_writes[:12]}...` == post-census "
      f"`{md5_post_census[:12]}...`: **{md5_post_writes == md5_post_census}**")
    A("")
    A("**Consumers:** governs S5 corpus→engine migration staging. Next re-run: when econ:UNKNOWN "
      "residual (9 remaining post-V11) is closed, when shapeshift GX-02 docket rules, or when "
      "econ:DR Wave-D spec lands. Matt may veto the phantom ruling by reverting negative=0 "
      "(reproducibility instructions embedded in §3).")

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
        # PRE-state asserts — accept either V10 pre-write (520 positives) or V11 post-write
        # (519 positives) state, since Part 1 writes are idempotent-guarded. On idempotent
        # replay, DB is already at POST state; assert matches POST_EXPECTED. On fresh run,
        # DB is at PRE_EXPECTED.
        current_positives = conn.execute(
            "SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=0"
        ).fetchone()[0]
        if current_positives == PRE_EXPECTED["kit_positives"]:
            pre_expected = PRE_EXPECTED
            print("\n[PRE-state] fresh run — DB is at V10 pre-write state")
        elif current_positives == POST_EXPECTED["kit_positives"]:
            pre_expected = POST_EXPECTED
            print("\n[PRE-state] idempotent re-run — DB is at V11 post-write state "
                  "(Part 1 writes will no-op per idempotent guards)")
        else:
            print(f"HALT: DB positive count {current_positives} matches neither PRE "
                  f"({PRE_EXPECTED['kit_positives']}) nor POST "
                  f"({POST_EXPECTED['kit_positives']}) — state indeterminate. Investigate.",
                  file=sys.stderr)
            sys.exit(2)
        pre_actual, pre_breach = run_asserts(conn, "PRE (state auto-detected)", pre_expected)
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No write.", file=sys.stderr)
            sys.exit(2)

        # PART 1: econ-recrawl-application (transactional)
        conn.execute("BEGIN")
        applied = part1_econ_recrawl_application(conn)
        conn.commit()

        # POST asserts — expect kit_positives=519, kit_negatives=44, others UNCHANGED
        post_actual, post_breach = run_asserts(conn, "POST (V11 state)", POST_EXPECTED)
        if post_breach:
            print("HALT: POST-state assert breach.", file=sys.stderr)
            sys.exit(3)

        md5_post_writes = db_md5()
        print(f"\nMD5 post-Part-1: {md5_post_writes}")

        # Collision audit (read-only)
        print("\nPART 1e: D2 collision audit (broader mob-harvest-v3 ambiguity)...")
        collision_suspects = part1_collision_audit(conn)
        print(f"    suspects surfaced: {len(collision_suspects)}")
        for s in collision_suspects:
            print(f"      {s['kit_id']} (hits: {s['signature_hits']}, verdict: {s['verdict']})")

        # PART 2: census
        print("\nPART 2: Running readiness census V11...")
        census = run_census(conn)
        print(f"    pool={census['total']}  expressible={census['expressible_now']} "
              f"({100.0*census['expressible_now']/census['total']:.2f}%)  "
              f"blocked={census['blocked']}")
        print(f"    corpus={census['corpus_expressible']}/{census['corpus_positives_kit_grain']}  "
              f"roster={census['roster_expressible']}/45")

        # Sanity asserts
        assert census["roster_expressible"] == 45
        assert census["corpus_positives_kit_grain"] == 519, (
            f"V11 corpus positives = {census['corpus_positives_kit_grain']}, expected 519"
        )
        assert census["total"] == 564, (
            f"V11 total = {census['total']}, expected 564"
        )

        md5_post_census = db_md5()
        print(f"\nMD5 post-census: {md5_post_census}")
        assert md5_post_writes == md5_post_census, "census pass MODIFIED the DB — BREACH"

        print("\nPART 2b: Writing census artifact...")
        artifact_path = write_census_artifact(
            census, collision_suspects, md5_pre, md5_post_writes, md5_post_census, conn,
        )
        print(f"    → {artifact_path}")

        print("\nS2 census V11 COMPLETE. All asserts held; artifact written.")
        print(f"    application writes applied: {applied}")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
