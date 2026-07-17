"""
corpus_econ_recrawl_apply_2026_07_16.py — APPLY the Legolas econ re-crawl sheet to corpus.db.

Author: elrond, 2026-07-16 (autonomous atlas-parity run, cycle 2, ECON-RECRAWL-APPLY charge).
Commissioner: gandalf-prime (Matt authorization 2026-07-16).

SHEET (the law for this pass — doc-authority, row-level **disposition** markers are authority):
    ../../legolas/research/econ-recrawl-2026-07-16/application-sheet-2026-07-16.md
    (commit 4abe140f, 20 rows: 17 classify / 3 unverifiable).

WHAT THIS PASS DOES (idempotent):
    1. 16 ECON CLASSIFIES — write economy_model (in cell_key slot 7 + column) + econ_status +
       econ_gaps on 16 kits; clear their econ-audit-ambiguous-2026-07-16 flag (resolved);
       stamp provenance flag econ-recrawl-applied-2026-07-16; merge source_urls from sheet rows.
         spend      x9 : d2-wl-abyss, d2-wl-echoing-strike, d2-wl-fire, poe1-kinetic-fusillade,
                         poe2-spiral-volley, poe2-whirling-assault-ma  (economy_model='spend')
                       + d4-blazing-abyss-warlock, d4-hammerdin-paladin, d4-rabies-lacerate
                         (economy_model='generator-spender' — sub-shape preserved per sheet;
                          still the spend family / native / expressible, still clears UNKNOWN)
         AM (accum) x3 : d4-dread-claws-warlock, poe1-heavy-strike-stun, poe2-walking-calamity
                         (economy_model='finite', econ_status='gap', econ_gaps=['AM'])
         PC         x3 : gd-berserker-wereforms, poe2-shaman-bear, vs-out-of-bounds-freeze
                         (economy_model='free', econ_status='gap', econ_gaps=['PC'])
         RS         x1 : poe2-archmage-totems
                         (economy_model='reserve', econ_status='gap', econ_gaps=['RS'])
       Bin→(economy_model, econ_status, econ_gaps) mapping matches the DB's established convention
       (surveyed pre-run: PC↔free/gap/["PC"] x44, RS↔reserve/gap/["RS"] x42, AM↔finite/gap/["AM"] x15,
        spend↔spend/native/[] x185, generator-spender↔native/[] x38). NO NEW BIN MINTED.
       Sub-shape detail with no schema column → recorded in the econ-recrawl-applied flag note payload.

    2. 1 AILMENT CLASSIFY — di-warlock-launch: ctrl_ailments_mapped -> [bleed,burn,knockback,stun];
       drop GAP-AILMENT:unknown-ailment from ctrl_ailment_gaps (resolved per sheet row 19).
       (di-warlock-launch econ is already cooldown/native — NOT touched.)

    3. 3 UNVERIFIABLE — flag econ-recrawl-unverifiable-2026-07-16:
         d2-wl-void-rift          : econ stays UNKNOWN (no dedicated guide; no editorial basis).
         poe2-snipe-mirage-deadeye: EDITORIAL single-bin call = spend (see ELROND-CALL below);
                                    econ resolves to spend/native/[] AND carries the unverifiable
                                    flag (classification is editorial-inferred, not source-confirmed).
         di-spiritform-druid-pvp  : econ already cooldown/native; ailment unresolved; flag only.

    4. DEDUPE RIDER — vs-gorgeous-moon: ctrl_ailment_gaps carries a duplicated instant-kill token
       (census V8 honesty note). Dedupe to a single GAP-AILMENT:instant-kill; flag dedupe-2026-07-16.
       (instant-kill is Wave-C+ ailment — stays a gap, NOT resolved; only the duplicate is removed.)

ELROND-CALL (poe2-snipe-mirage-deadeye editorial single-bin resolution):
    Row 14 flags this build as a two-mechanism interaction (Snipe channel = spend, mana/second;
    Mirage Deadeye = PC activation-toggle buff) and asks for an editorial single-bin call if the
    evidence supports one. raw_json carries NO captured-primary-mechanism signal (no mech prose /
    core_skills / resource_verbatim — only delivery=projectile, a low-conf geometry, dossier-deferred
    flag). BUT the sheet resolves three structurally-identical in-batch cases the same way:
    poe1-kinetic-fusillade (spend core + RS aura rider -> spend), poe2-whirling-assault-ma
    (spend core + power-charge damage-layer + RS rider -> spend), poe2-spiral-volley
    (spend core + frenzy-charge damage-layer + spirit-reservation -> spend). In every case the
    resource-consuming delivery skill (spend) is primary and the persistent buff/charge layer is
    the rider. Snipe/Mirage is the same shape: Snipe is the damage-delivery skill that carries the
    per-activation operating cost (mana/second channel); Mirage Deadeye is the persistent buff rider
    (10s cadence, no independent operating cost, adds mirage copies == a damage-multiplier layer).
    Under the §5.3 single-bin contract, the primary economy identity is the layer that consumes the
    operating resource => spend. Row 14's own text states "Snipe's own economy is spend (mana/second
    channeled)". CALL: spend. Flagged unverifiable (crawl found no dedicated guide) with this note;
    the classification is honestly recorded as editorial-inferred.

IRON LAWS:
    1. Backup-first (../curated/corpus.db.pre-econ-recrawl-2026-07-16-backup; integrity_check=ok).
    2. Asserts PRE + POST identical: total=585 · engine_key=585 · kit_grain=566 · null_grain=19 ·
       cell_key_resolved=562 · bt_sentinel=1 · orphans 0+0 · dossier_owed=4.
    3. Write scope limited to the 20 sheet rows + vs-gorgeous-moon dedupe. Touch NOTHING else.
    4. NO new schema minted mid-run (spec-amendment candidates instead — enumerated in return/MIGRATION).
    5. Idempotent — re-run yields identical DB state + identical asserts.
    6. HALT on any assert fail. Auto-commit collab repo; NO push (gandalf pushes).

NOTE: writes shift scoreboard buckets (LIKE-match kit-grain positives): PC 44->47, RS 42->43,
    AM 16->19, UNKNOWN 33->16. Census is NOT rerun this pass; V9 fires after Wave-B Gate-2 and
    picks all of it up.
"""

import json
import pathlib
import sqlite3
import sys

BASE = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = BASE / "agentic_orchestration/research/curated/corpus.db"

# Iron-law invariants (identical PRE + POST)
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

APPLIED_FLAG = "econ-recrawl-applied-2026-07-16"
UNVERIFIABLE_FLAG = "econ-recrawl-unverifiable-2026-07-16"
DEDUPE_FLAG = "dedupe-2026-07-16"
AMBIGUITY_FLAG = "econ-audit-ambiguous-2026-07-16"

# cell_key slot map (14 parts, "|"-delimited):
#  0=mob 1=delivery 2=amp 3=geometry 4=ctrl_treatment 5=ctrl_function 6=def_bin
#  7=economy_model 8=proxy 9=range 10=tempo 11=commit 12=activation 13=dependency
ECON_SLOT = 7

# --- The 16 econ classifies: kit_id -> (economy_model, econ_status, econ_gaps_json, urls, note) ---
# note = sub-shape payload recorded in the applied-flag (grain the schema lacks a column for).
ECON_FILLS = {
    # spend x9 -----------------------------------------------------------------
    "d2-wl-abyss": (
        "spend", "native", "[]",
        ["https://maxroll.gg/d2/guides/abyss-warlock-build-guide",
         "https://maxroll.gg/d2/guides/abyss-warlock-leveling-build-guide"],
        "spend/steady-mana; Hex:Siphon kill-return + Insight Meditation sustain; no generator/reserve/meter",
    ),
    "d2-wl-echoing-strike": (
        "spend", "native", "[]",
        ["https://maxroll.gg/d2/guides/echoing-strike-warlock-guide",
         "https://odealo.com/articles/echoing-strike-warlock-build-for-diablo-2-resurrected"],
        "spend/steady-mana+leech; gear mana-stolen + Insight Meditation; no reservation/meter",
    ),
    "d2-wl-fire": (
        "spend", "native", "[]",
        ["https://maxroll.gg/d2/guides/fire-warlock-guide",
         "https://www.icy-veins.com/d2/fire-warlock-build"],
        "spend/starved-mana (High Mana Requirements; early Energy; Insight mandatory); spend family",
    ),
    "poe1-kinetic-fusillade": (
        "spend", "native", "[]",
        ["https://maxroll.gg/poe/build-guides/kinetic-fusillade-ballista-hierophant-league-starter",
         "https://www.pathofexile.com/forum/view-thread/3876136"],
        "spend/steady-mana (cost 4-6/cast); Wrath+Clarity aura reservation is an RS rider, not primary",
    ),
    "poe2-spiral-volley": (
        "spend", "native", "[]",
        ["https://maxroll.gg/poe2/build-guides/spiral-volley-deadeye-build-guide",
         "https://www.poe2wiki.net/wiki/Spiral_Volley"],
        "spend/intensive-mana (cost 6-64; mana-per-kill gear); frenzy charges = damage-layer not cost",
    ),
    "poe2-whirling-assault-ma": (
        "spend", "native", "[]",
        ["https://maxroll.gg/poe2/build-guides/whirling-assault-martial-artist-build-guide",
         "https://boostmatch.gg/blog/poe-2/articles/poe2-martial-artist-monk-whirling-assault-build-guide"],
        "spend/mana-per-activation (Conservative Casting); power charges = damage-layer; spirit-reserve minor RS rider",
    ),
    # spend family, sub-shape = generator-spender (preserved per sheet; native/[]/expressible) ------
    "d4-blazing-abyss-warlock": (
        "generator-spender", "native", "[]",
        ["https://maxroll.gg/d4/build-guides/blazing-scream-warlock-leveling-guide",
         "https://www.icy-veins.com/d4/guides/blazing-abyss-warlock-build/"],
        "spend/generator-spender on Wrath (Command Fallen generates, Blazing Scream spends); Shadowform stealth is secondary",
    ),
    "d4-hammerdin-paladin": (
        "generator-spender", "native", "[]",
        ["https://maxroll.gg/d4/build-guides/blessed-hammer-paladin-guide",
         "https://www.icy-veins.com/d4/guides/blessed-hammer-paladin-build/"],
        "spend/generator-spender on Faith (Rally generates, Blessed Hammer+auras spend); aura upkeep is CD-stacked not reservation",
    ),
    "d4-rabies-lacerate": (
        "generator-spender", "native", "[]",
        ["https://www.icy-veins.com/d4/guides/rabies-lacerate-druid-build/",
         "https://mobalytics.gg/diablo-4/builds/druid-rabies-endgame"],
        "spend/generator-spender on Spirit (Rabies 30/Lacerate 100; Stag/Blood Howl generate); "
        "werewolf form-lock = buff-preservation rider (GX-02 SS docket), not a separate econ bin",
    ),
    # AM (charge-stack/accumulator) x3 -----------------------------------------
    "d4-dread-claws-warlock": (
        "finite", "gap", '["AM"]',
        ["https://maxroll.gg/d4/build-guides/dread-claws-warlock-guide",
         "https://www.icy-veins.com/d4/guides/dread-claws-warlock-build/"],
        "AM/accumulator; Shadowform fill=on-passive-tick (Terror Demon 4 stacks/s), discharge on Dread Claws; "
        "SPEC-AMENDMENT: fill_trigger enum lacks on-passive-tick/on-time-tick",
    ),
    "poe1-heavy-strike-stun": (
        "finite", "gap", '["AM"]',
        ["https://mobalytics.gg/poe/builds/stun-heavy-strike-berserker",
         "https://www.mmoexp.com/News/path-of-exile-the-complete-guide-to-the-sir-bongsalot-stun-build.html"],
        "AM/accumulator; Rage+Trauma fill=on-hit-dealt, discharge on Berserk; endurance-charge secondary rider",
    ),
    "poe2-walking-calamity": (
        "finite", "gap", '["AM"]',
        ["https://maxroll.gg/poe2/build-guides/walking-calamity-shaman-build-guide",
         "https://www.mmoexp.com/News/path-of-exile-2-walking-calamity-druid-build-guide.html"],
        "AM/accumulator; Glory fill=on-resource-overflow (Rage-at-max), 50 Glory discharges Walking Calamity 20s+; "
        "SPEC-AMENDMENT: fill_trigger enum lacks on-resource-overflow",
    ),
    # PC (persistent-condition) x3 ---------------------------------------------
    "gd-berserker-wereforms": (
        "free", "gap", '["PC"]',
        ["https://www.grimdawn.com/guide/character/masteries/berserker/",
         "https://massivelyop.com/2026/06/01/grim-dawns-fangs-of-asterkarn-expansion-adds-a-frosty-new-realm-and-a-shapeshifting-mastery-line-july-23/",
         "https://grimdawn.fandom.com/wiki/Fangs_of_Asterkarn"],
        "PC/activation-toggle; wereform (werewolf/wereraven) persists while active, extendable to permanent; "
        "no per-tick drain; cold-infused weapon attacks state-enabled (ailment GAP freeze UNRESOLVED this pass)",
    ),
    "poe2-shaman-bear": (
        "free", "gap", '["PC"]',
        ["https://maxroll.gg/poe2/build-guides/demon-calamity-bear-shaman-build-guide",
         "https://overgear.com/guides/poe-2/shaman-bear-druid/"],
        "PC/activation-toggle; Bear Form persistent (Furious Wellspring prevents Rage decay); "
        "spirit-reservation (~360) = RS rider, glory-accum = AM rider; PC is the defining identity",
    ),
    "vs-out-of-bounds-freeze": (
        "free", "gap", '["PC"]',
        ["https://vampire.survivors.wiki/w/Out_of_Bounds_(XII)",
         "https://vampire-survivors.fandom.com/wiki/Out_of_Bounds_(XII)"],
        "PC/activation-toggle; arcana slot occupied entire run, no per-tick drain (arcana-slot opportunity cost); "
        "freeze is applied by carry-weapon layer not this arcana (ailment GAP freeze stays weapon-attributed)",
    ),
    # RS (reservation) x1 ------------------------------------------------------
    "poe2-archmage-totems": (
        "reserve", "gap", '["RS"]',
        ["https://maxroll.gg/poe2/build-guides/grim-pillars-spell-totem-oracle-build-guide",
         "https://allthings.how/path-of-exile-2-oracle-spell-totem-build-how-the-spirit-trick-works/"],
        "RS/flat-reservation; 75 Spirit/totem (Ancestral Bond, ->63 via Efficient Inscriptions); "
        "Archmage mana-as-damage is a stat not a spend; SPEC-AMENDMENT: reservation_resource enum lacks 'spirit'",
    ),
}

# --- 1 ailment classify (di-warlock-launch econ untouched — already cooldown/native) ---
# Sheet row 19: burn + bleed + stun + knockback; drop GAP-AILMENT:unknown-ailment.
AILMENT_FILL = {
    "di-warlock-launch": {
        "ailments_mapped": ["bleed", "burn", "knockback", "stun"],  # sorted
        "drop_gaps": ["GAP-AILMENT:unknown-ailment"],
        "urls": ["https://news.blizzard.com/en-us/article/24277443/introducing-diablo-immortals-newest-class-warlock"],
    }
}

# --- 3 unverifiable ---
# d2-wl-void-rift: econ stays UNKNOWN, flag only.
# poe2-snipe-mirage-deadeye: EDITORIAL call = spend (resolves econ) + unverifiable flag + note.
# di-spiritform-druid-pvp: econ already cooldown/native, flag only.
SNIPE_EDITORIAL = {
    "poe2-snipe-mirage-deadeye": (
        "spend", "native", "[]",
        ["https://pathofexile2.wiki.fextralife.com/Mirage+Deadeye+(Meta+Skill)",
         "https://www.poe2wiki.net/wiki/Snipe"],
        "ELROND-CALL spend (editorial-inferred, no dedicated guide): Snipe channel = operating spend "
        "(17-118 mana/s); Mirage Deadeye = PC buff-rider (10s, no independent cost). Structurally == "
        "kinetic-fusillade/whirling-assault/spiral-volley (spend-core + buff-rider -> spend). §5.3 single-bin: "
        "resource-consuming delivery layer is primary. Row-14 evidence: 'Snipe's own economy is spend'.",
    )
}
UNVERIFIABLE_FLAG_ONLY = ["d2-wl-void-rift", "di-spiritform-druid-pvp"]

# --- dedupe rider ---
DEDUPE_TARGET = "vs-gorgeous-moon"


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


def parse_list(s):
    if not s:
        return []
    try:
        v = json.loads(s)
        return v if isinstance(v, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def add_flag(conn, kit_id, flag):
    """Append flag to canon_corpus.flags (comma-sep, idempotent). Return True if added."""
    existing = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    toks = [t for t in (existing.split(",") if existing else []) if t]
    if flag in toks:
        return False
    toks.append(flag)
    conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (",".join(toks), kit_id))
    return True


def remove_flag(conn, kit_id, flag):
    """Remove an exact-match flag token from canon_corpus.flags. Return True if removed."""
    existing = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    toks = [t for t in (existing.split(",") if existing else []) if t]
    if flag not in toks:
        return False
    toks = [t for t in toks if t != flag]
    conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (",".join(toks) if toks else None, kit_id))
    return True


def merge_source_urls(conn, kit_id, urls):
    """Merge urls into canon_corpus.source_urls JSON array (dedup, order-preserving)."""
    existing_raw = conn.execute("SELECT source_urls FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    existing = parse_list(existing_raw)
    merged = list(existing)
    for u in urls:
        if u not in merged:
            merged.append(u)
    if merged != existing:
        conn.execute("UPDATE canon_corpus SET source_urls=? WHERE kit_id=?",
                     (json.dumps(merged), kit_id))
        return True
    return False


def apply_econ(conn, kit_id, model, status, gaps_json):
    """Write economy_model into cell_key slot 7 + the three econ columns. Idempotent."""
    row = conn.execute(
        "SELECT cell_key, economy_model, econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?",
        (kit_id,),
    ).fetchone()
    if not row:
        raise RuntimeError(f"econ target missing: {kit_id}")
    old_ck, old_model, old_status, old_gaps = row

    parts = old_ck.split("|")
    if len(parts) != 14:
        raise RuntimeError(f"{kit_id}: cell_key has {len(parts)} parts, expected 14")
    parts[ECON_SLOT] = model
    new_ck = "|".join(parts)

    conn.execute(
        "UPDATE canon_engine_key SET cell_key=?, economy_model=?, econ_status=?, econ_gaps=? WHERE kit_id=?",
        (new_ck, model, status, gaps_json, kit_id),
    )
    return old_model, model


def apply_ailment(conn, kit_id, mapped, drop_gaps):
    """Set ctrl_ailments_mapped; drop named tokens from ctrl_ailment_gaps. Idempotent."""
    row = conn.execute(
        "SELECT ctrl_ailments_mapped, ctrl_ailment_gaps FROM canon_engine_key WHERE kit_id=?",
        (kit_id,),
    ).fetchone()
    old_mapped, old_gaps = parse_list(row[0]), parse_list(row[1])
    new_gaps = [g for g in old_gaps if g not in drop_gaps]
    conn.execute(
        "UPDATE canon_engine_key SET ctrl_ailments_mapped=?, ctrl_ailment_gaps=? WHERE kit_id=?",
        (json.dumps(mapped), json.dumps(new_gaps), kit_id),
    )
    return old_mapped, mapped, old_gaps, new_gaps


def dedupe_gaps(conn, kit_id):
    """Dedup ctrl_ailment_gaps preserving first-seen order. Return (old, new)."""
    raw = conn.execute("SELECT ctrl_ailment_gaps FROM canon_engine_key WHERE kit_id=?", (kit_id,)).fetchone()[0]
    old = parse_list(raw)
    seen, new = set(), []
    for g in old:
        if g not in seen:
            seen.add(g)
            new.append(g)
    if new != old:
        conn.execute("UPDATE canon_engine_key SET ctrl_ailment_gaps=? WHERE kit_id=?",
                     (json.dumps(new), kit_id))
    return old, new


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        _, pre_breach = run_asserts(conn, "PRE")
        if pre_breach:
            print("HALT: PRE-state assert breach (iron law). No writes.", file=sys.stderr)
            sys.exit(2)

        # Idempotency: if this migration is already in the ledger, verify the post-state
        # invariants and exit 0 as a clean no-op (do not re-apply, do not halt).
        already = conn.execute(
            "SELECT COUNT(*) FROM corpus_schema_meta WHERE version='econ-recrawl-apply-2026-07-16'"
        ).fetchone()[0]
        if already:
            u = conn.execute(
                "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
                "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%'"
            ).fetchone()[0]
            assert u == 16, f"idempotent re-run: expected post-state UNKNOWN=16, got {u}"
            conn.rollback()
            print("\nAlready applied (ledger hit). Post-state verified (UNKNOWN=16). No-op — DB unchanged.")
            return

        pre_unknown = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%'"
        ).fetchone()[0]
        print(f"\n[PRE] econ:UNKNOWN kit-grain positives: {pre_unknown} (expected 33)")
        assert pre_unknown == 33, f"PRE UNKNOWN={pre_unknown}, expected 33"

        # -- 1. 16 econ classifies --
        bin_counts = {"spend": 0, "AM": 0, "PC": 0, "RS": 0}
        print(f"\n[1] 16 econ classifies:")
        for kit_id, (model, status, gaps_json, urls, note) in ECON_FILLS.items():
            old_model, _ = apply_econ(conn, kit_id, model, status, gaps_json)
            remove_flag(conn, kit_id, AMBIGUITY_FLAG)
            add_flag(conn, kit_id, f"{APPLIED_FLAG}:{note}")
            merge_source_urls(conn, kit_id, urls)
            # scoreboard family tally
            if gaps_json == '["AM"]':
                bin_counts["AM"] += 1
            elif gaps_json == '["PC"]':
                bin_counts["PC"] += 1
            elif gaps_json == '["RS"]':
                bin_counts["RS"] += 1
            else:
                bin_counts["spend"] += 1
            print(f"    {kit_id:28s} {old_model!r:>10s} -> {model!r:<18s} status={status} gaps={gaps_json}")
        print(f"    bin family counts: spend={bin_counts['spend']} AM={bin_counts['AM']} "
              f"PC={bin_counts['PC']} RS={bin_counts['RS']}")

        # -- 2. 1 ailment classify --
        print(f"\n[2] 1 ailment classify:")
        for kit_id, spec in AILMENT_FILL.items():
            om, nm, og, ng = apply_ailment(conn, kit_id, spec["ailments_mapped"], spec["drop_gaps"])
            add_flag(conn, kit_id, f"{APPLIED_FLAG}:ailment burn+bleed+stun+knockback per sheet row 19")
            merge_source_urls(conn, kit_id, spec["urls"])
            print(f"    {kit_id}: mapped {om} -> {nm}  gaps {og} -> {ng}")

        # -- 3. 3 unverifiable --
        print(f"\n[3] 3 unverifiable:")
        for kit_id in UNVERIFIABLE_FLAG_ONLY:
            add_flag(conn, kit_id, UNVERIFIABLE_FLAG)
            print(f"    {kit_id}: flagged {UNVERIFIABLE_FLAG} (econ unchanged)")
        for kit_id, (model, status, gaps_json, urls, note) in SNIPE_EDITORIAL.items():
            old_model, _ = apply_econ(conn, kit_id, model, status, gaps_json)
            remove_flag(conn, kit_id, AMBIGUITY_FLAG)
            add_flag(conn, kit_id, UNVERIFIABLE_FLAG)
            add_flag(conn, kit_id, f"{APPLIED_FLAG}:{note}")
            merge_source_urls(conn, kit_id, urls)
            print(f"    {kit_id}: EDITORIAL {old_model!r} -> {model!r} status={status} gaps={gaps_json} "
                  f"+ flagged {UNVERIFIABLE_FLAG}")

        # -- 4. dedupe rider --
        print(f"\n[4] dedupe rider:")
        old_g, new_g = dedupe_gaps(conn, DEDUPE_TARGET)
        if new_g != old_g:
            add_flag(conn, DEDUPE_TARGET, DEDUPE_FLAG)
            print(f"    {DEDUPE_TARGET}: ctrl_ailment_gaps {old_g} -> {new_g}  (flagged {DEDUPE_FLAG})")
        else:
            print(f"    {DEDUPE_TARGET}: already deduped {old_g} (idempotent skip)")

        # -- POST UNKNOWN accounting --
        post_unknown = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%'"
        ).fetchone()[0]
        print(f"\n[POST] econ:UNKNOWN kit-grain positives: {post_unknown} "
              f"(expected 16 = 33 - 16 econ - 1 snipe-editorial)")
        assert post_unknown == 16, f"POST UNKNOWN={post_unknown}, expected 16"

        # only d2-wl-void-rift should remain UNKNOWN among the 20 targets
        remaining = [r[0] for r in conn.execute(
            "SELECT ce.kit_id FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%' "
            "AND ce.kit_id IN ('d2-wl-abyss','d2-wl-echoing-strike','d2-wl-fire','d2-wl-void-rift',"
            "'d4-blazing-abyss-warlock','d4-dread-claws-warlock','d4-hammerdin-paladin','d4-rabies-lacerate',"
            "'gd-berserker-wereforms','poe1-heavy-strike-stun','poe1-kinetic-fusillade','poe2-archmage-totems',"
            "'poe2-shaman-bear','poe2-snipe-mirage-deadeye','poe2-spiral-volley','poe2-walking-calamity',"
            "'poe2-whirling-assault-ma','vs-out-of-bounds-freeze')"
        ).fetchall()]
        assert remaining == ["d2-wl-void-rift"], f"unexpected UNKNOWN residue among targets: {remaining}"

        # scoreboard family verification (kit-grain positives)
        def cnt(tok):
            return conn.execute(
                "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
                f"WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%\"{tok}\"%'"
            ).fetchone()[0]
        pc_n, rs_n, am_n = cnt("PC"), cnt("RS"), cnt("AM")
        # LIKE-match baselines pre-run: PC=44, RS=42, AM=16 (15 exact ["AM"] + 1 ["AM","BT"]).
        # +3 PC, +1 RS, +3 AM => 47 / 43 / 19 (AM=19 matches charge's "~18/19" upper hedge).
        print(f"    scoreboard now: PC={pc_n} (expect 47)  RS={rs_n} (expect 43)  AM={am_n} (expect 19)")
        assert pc_n == 47, f"PC={pc_n}, expected 47"
        assert rs_n == 43, f"RS={rs_n}, expected 43"
        assert am_n == 19, f"AM={am_n}, expected 19 (16 pre-run LIKE-match + 3)"

        _, post_breach = run_asserts(conn, "POST")
        if post_breach:
            print("HALT: POST-state assert breach. Rolling back.", file=sys.stderr)
            conn.rollback()
            sys.exit(3)

        # schema-meta ledger bump
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?, ?, ?)",
            (
                "econ-recrawl-apply-2026-07-16",
                "2026-07-16T00:00:00Z",
                (
                    "Elrond applied Legolas econ re-crawl sheet (application-sheet-2026-07-16.md, "
                    "commit 4abe140f; doc-authority row-level dispositions) to corpus.db. "
                    "16 econ classifies: spend x9 (6 spend + 3 generator-spender sub-shape), "
                    "AM x3 (d4-dread-claws-warlock/poe1-heavy-strike-stun/poe2-walking-calamity -> finite/gap/[AM]), "
                    "PC x3 (gd-berserker-wereforms/poe2-shaman-bear/vs-out-of-bounds-freeze -> free/gap/[PC]), "
                    "RS x1 (poe2-archmage-totems -> reserve/gap/[RS]); ambiguity flag cleared on the 16, "
                    "econ-recrawl-applied-2026-07-16 + source URLs stamped. "
                    "1 ailment classify: di-warlock-launch ctrl_ailments_mapped=[bleed,burn,knockback,stun], "
                    "dropped GAP-AILMENT:unknown-ailment (econ untouched, already cooldown/native). "
                    "3 unverifiable flagged econ-recrawl-unverifiable-2026-07-16: d2-wl-void-rift (econ stays "
                    "UNKNOWN), di-spiritform-druid-pvp (econ already cooldown/native), poe2-snipe-mirage-deadeye "
                    "(EDITORIAL single-bin call -> spend, unverifiable-flagged, editorial-inferred note). "
                    "Dedupe: vs-gorgeous-moon ctrl_ailment_gaps duplicate instant-kill removed (dedupe-2026-07-16). "
                    "Scoreboard shift (LIKE-match kit-grain positives): PC 44->47, RS 42->43, AM 16->19, "
                    "UNKNOWN 33->16. "
                    "Asserts held identical (585/585/566/19/562/1-bt/0-orphans/4-dossier). No new bin/schema "
                    "minted; 3 spec-amendment candidates flagged (AM fill_trigger on-passive-tick + "
                    "on-resource-overflow; RS reservation_resource 'spirit'). Census NOT rerun; V9 picks it up "
                    "after Wave-B Gate-2."
                ),
            ),
        )

        conn.commit()
        print("\nEcon-recrawl APPLY complete. All asserts held; committed.")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
