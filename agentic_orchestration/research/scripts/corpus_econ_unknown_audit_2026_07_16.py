"""
corpus_econ_unknown_audit_2026_07_16.py — Audit the econ:UNKNOWN bucket (38 kits) per
gandalf-prime charge 2026-07-16.

BACKGROUND (S2 census V7 SCOREBOARD, gandalf 2026-07-16 dc295719):
    §2/§3 of `../curated/atlas/s2-readiness-census-v7-2026-07-16.md` names 38 kit-grain
    positive rows whose engine-key economy slot is `unknown` (blocked bucket). These 38
    block the parity scoreboard's own measurement — until each is either classified into
    an existing bin or explicitly deferred as ambiguous, the scoreboard can't distinguish
    "genuine unclassified" from "under-derived at rule pass".

CHARGE (verbatim gandalf 2026-07-16):
    For each of the 38 UNKNOWN kits, re-examine raw_json (mech prose + core_skills +
    probe facts) and classify:
        (a) DERIVABLE with EXISTING mapping rules — evidence under-derived at map time
            → fill economy slot in cell_key now (cite rule + evidence phrase per fill)
        (b) NEEDS A NEW MAPPING RULE — economy legible in prose but no existing rule
            covers → do NOT mint the rule (iron law); leave UNKNOWN, add to a
            spec-amendment candidate list with the proposed rule sketch
        (c) GENUINELY AMBIGUOUS / evidence-thin → leave UNKNOWN, flag
            `econ-audit-ambiguous-2026-07-16`, name re-crawl candidate

IRON LAWS:
    1. Backup-first (state filename; integrity_check)
    2. WRITE SCOPE LIMITED to the 38 UNKNOWN rows' cell_key economy slot + flags —
       touch NOTHING else. (Gandalf wave-B spec drafter reads PC/RS/AM/RC/LC/DR rows
       in parallel; those rows are frozen to this charge.)
    3. Asserts PRE+POST (total=585 · kit=566 · NULL-grain=19 · cell_key_resolved=562 ·
       -bt sentinel=1 · engine_key 1:1 · dossier_owed=4)
    4. Every fill carries evidence citation in the report
    5. MIGRATION.md entry required (audit record + per-class counts + amendment-candidate
       list + re-crawl candidate list)
    6. HALT = any assert fail or any temptation to mint a rule → stop + report

CLASSIFICATION RESULTS (this pass):

    Class (a) — 5 fills using EXISTING bin vocabulary (spend, summon-uptime):
        1. chr-bleed-berserker    → economy_model=spend        (native)
        2. chr-high-ranger-warden → economy_model=spend        (native)
        3. poe1-baron-zombies     → economy_model=summon-uptime (gap:[SU])
        4. poe1-siege-ballista    → economy_model=summon-uptime (gap:[SU])
        5. gd-pet-conjurer        → economy_model=summon-uptime (gap:[SU])

        All five map cleanly to bins already present in canon_engine_key.economy_model
        (spend: 183 kits precedent; summon-uptime: 2 kits precedent). SU as gap-ledger
        entry has 6 precedents (1 SU-only + 4 RS+SU + 1 HV+SU). No new bin symbol minted.

    Class (b) — 15 kits, evidence legible but pattern not in existing rule vocabulary.
        Amendment-candidate rule sketches enumerated in report.

    Class (c) — 18 kits, evidence-thin (post-cutoff conf<0.5 / dossier_owed language /
        SEARCH-DERIVED). Flagged econ-audit-ambiguous-2026-07-16; re-crawl candidates
        for a future Legolas batch.

    ALSO listed as re-crawl companions (per charge): 2 unknown-ailment kits from census
        (di-warlock-launch, di-spiritform-druid-pvp) — no action this pass, listed for
        the same future batch.

Author: elrond, 2026-07-16 (autonomous atlas-parity run, cycle 2, econ-audit charge)
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


# Class (a) fills — evidence maps unambiguously to existing rule bin
# Each entry: (kit_id, new_economy_model, new_econ_status, new_econ_gaps_json,
#              rule_cite, evidence_cite)
FILLS_A = [
    (
        "chr-bleed-berserker",
        "spend",
        "native",
        "[]",
        "apply-rules-v1.0.py §4 ECON MAPPING line 444: "
        "`if sub in ('spend', 'cooldown', 'self-cost'): status='native'`",
        "probe.economy.plain_text: 'DW economy = drain-while: bleed drains enemy HP "
        "continuously while stacks are active. Rage spend to activate bleed-strike skills. "
        "Economy is a hybrid: Rage spend to apply bleed, then bleed drains automatically.' "
        "resource_verbatim='Rage'. The plain_text explicitly names 'spend' as the "
        "activation-economy verb; probe encoded model='other', under-derived — spend "
        "is the accepted native token per rule §4."
    ),
    (
        "chr-high-ranger-warden",
        "spend",
        "native",
        "[]",
        "apply-rules-v1.0.py §4 ECON MAPPING line 444: "
        "`if sub in ('spend', 'cooldown', 'self-cost'): status='native'`",
        "probe.economy.plain_text: 'DW old code likely = drain-while: bleed DoT economy "
        "drains enemy HP continuously while active. Focus spent on arrow activation; "
        "bleed sustains between shots. Hybrid spend+drain model.' resource_verbatim='Focus'. "
        "The plain_text explicitly names 'spend' (twice: 'Focus spent' + 'hybrid spend+drain'); "
        "probe encoded model='other', under-derived."
    ),
    (
        "poe1-baron-zombies",
        "summon-uptime",
        "gap",
        '["SU"]',
        "apply-rules-v1.0.py §4 ECON MAPPING line 505: "
        "`if (model_lower == 'summon' or 'minion' in bs_lower or 'summon' in bs_lower or is_jsum): "
        "gaps.append('SU')` + §1 R0b summon_verbs list "
        "(includes 'zombie', 'minion') + army_horde list (includes 'army').",
        "probe.mechanics_notes: 'The Baron helm feeds the caster's stacked STRENGTH into "
        "zombie power and life-leech-per-minion — a gear stat on YOUR sheet becomes the ARMY'. "
        "geo_text same. resource_verbatim='stat->army'. All three rule keywords "
        "(zombie, minion, army) appear in the raw mech prose — this IS an army-summon "
        "economy; probe encoded model='other'/builder_source='n/a', under-derived. "
        "Fill: summon-uptime bin (2 kits precedent) + SU gap-ledger token."
    ),
    (
        "poe1-siege-ballista",
        "summon-uptime",
        "gap",
        '["SU"]',
        "apply-rules-v1.0.py §1 R0b line 620 is_totem_trap includes 'turret' → totem-family "
        "(R0b already fired: geom=totem, conf=0.66); §4 SU-mapping applies via summon-family "
        "spirit (totem/turret-summons = summon economy). Census §5 board 1 counts "
        "'SU mechanics-demand = 48 (totem-keyed + J-SUM-resolved)' — totem-geom kits are "
        "expected to carry SU.",
        "probe.mechanics_notes: 'Iron Commander grants +1 ballista per 200 DEX — the "
        "attribute stack literally COUNTS your turret army; stat-as-army-size.' "
        "geom=totem (R0b fired: 'turret' keyword hit); resource_verbatim='item-count'. "
        "This is a turret-summon economy (ballistas = turret-summon entities); rule R0b "
        "correctly identified the placement but §4 SU-branch missed because builder_source='n/a'. "
        "Under-derived probe."
    ),
    (
        "gd-pet-conjurer",
        "summon-uptime",
        "gap",
        '["SU"]',
        "apply-rules-v1.0.py §4 ECON MAPPING line 505: `if ('summon' in bs_lower ...): "
        "gaps.append('SU')` + §1 R0b summon_verbs list (includes 'summon' verb).",
        "probe.delivery.evidence: 'Full pet menagerie summoned at various positions; "
        "fight independently'. mechanics_notes: 'The full menagerie — Briarthorn, Familiar, "
        "and Bysmiel devotion beasts under pet-scaled gear where YOUR stats mean nothing "
        "and THEIRS mean everything.' resource_verbatim='pet-stat'. The rule keyword 'summon' "
        "(delivery.evidence 'summoned') is present in raw evidence; probe encoded model='other'/"
        "builder_source='n/a', under-derived. Pet-scaled economy = summon-uptime (2 kits precedent)."
    ),
]

# Kits that stay UNKNOWN, flagged econ-audit-ambiguous-2026-07-16
AMBIGUOUS_KITS_C = [
    "d2-wl-abyss",
    "d2-wl-echoing-strike",
    "d2-wl-fire",
    "d2-wl-void-rift",
    "d4-blazing-abyss-warlock",
    "d4-dread-claws-warlock",
    "d4-hammerdin-paladin",
    "d4-rabies-lacerate",
    "gd-berserker-wereforms",
    "poe1-heavy-strike-stun",
    "poe1-kinetic-fusillade",
    "poe2-archmage-totems",
    "poe2-shaman-bear",
    "poe2-snipe-mirage-deadeye",
    "poe2-spiral-volley",
    "poe2-walking-calamity",
    "poe2-whirling-assault-ma",
    "vs-out-of-bounds-freeze",
]

AUDIT_FLAG = "econ-audit-ambiguous-2026-07-16"


def apply_fill(conn, kit_id, new_model, new_status, new_gaps_json):
    """Update economy slot in cell_key + econ columns.
    Cell_key economy_model is at position 7 (0-indexed) between def_bin(6) and proxy_val(8):
      0=mob 1=delivery 2=amp 3=geometry 4=ctrl_treatment 5=ctrl_function 6=def_bin
      7=economy_model 8=proxy_val 9=range_val 10=tempo_val 11=commit_val 12=activation 13=dependency
    """
    cur = conn.execute(
        "SELECT cell_key, economy_model, econ_status, econ_gaps FROM canon_engine_key WHERE kit_id=?",
        (kit_id,),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"fill target missing: {kit_id}")
    old_ck, old_model, old_status, old_gaps = row

    # Sanity: only fill if currently UNKNOWN in gaps
    if "UNKNOWN" not in (old_gaps or ""):
        raise RuntimeError(
            f"{kit_id}: expected UNKNOWN in econ_gaps but got {old_gaps!r}. "
            f"Refusing to touch already-non-UNKNOWN row (write scope guard)."
        )

    # Assemble new cell_key
    parts = old_ck.split("|")
    if len(parts) != 14:
        raise RuntimeError(f"{kit_id}: cell_key has {len(parts)} parts, expected 14")
    old_slot = parts[7]
    parts[7] = new_model
    new_ck = "|".join(parts)

    conn.execute(
        "UPDATE canon_engine_key SET cell_key=?, economy_model=?, econ_status=?, econ_gaps=? "
        "WHERE kit_id=?",
        (new_ck, new_model, new_status, new_gaps_json, kit_id),
    )
    return old_ck, old_slot, new_ck


def apply_ambiguous_flag(conn, kit_id):
    """Append AUDIT_FLAG to canon_corpus.flags (comma-separated, idempotent)."""
    existing = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kit_id,)).fetchone()[0]
    if existing and AUDIT_FLAG in existing:
        return False  # already flagged
    if existing:
        updated = f"{existing},{AUDIT_FLAG}"
    else:
        updated = AUDIT_FLAG
    conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (updated, kit_id))
    return True


def main():
    if not DB_PATH.exists():
        print(f"ERROR: corpus.db not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # PRE asserts
        _, pre_breach = run_asserts(conn, "PRE")
        if pre_breach:
            print("HALT: PRE-state assert breach.", file=sys.stderr)
            sys.exit(2)

        # Pre-count: 38 UNKNOWN kits
        pre_unknown = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%'"
        ).fetchone()[0]
        assert pre_unknown == 38, f"PRE: UNKNOWN count = {pre_unknown}, expected 38"
        print(f"\n[PRE] econ:UNKNOWN kit-grain positives: {pre_unknown} (expected 38)")

        # Apply class (a) fills
        print(f"\nApplying class (a) fills ({len(FILLS_A)}):")
        for kit_id, new_model, new_status, new_gaps, rule, evidence in FILLS_A:
            old_ck, old_slot, new_ck = apply_fill(conn, kit_id, new_model, new_status, new_gaps)
            print(f"  {kit_id}: economy_model {old_slot!r} → {new_model!r}  status={new_status}  gaps={new_gaps}")

        # Flag class (c) ambiguous kits
        print(f"\nFlagging class (c) ambiguous kits ({len(AMBIGUOUS_KITS_C)}) with '{AUDIT_FLAG}':")
        flagged_count = 0
        for kit_id in AMBIGUOUS_KITS_C:
            was_flagged = apply_ambiguous_flag(conn, kit_id)
            if was_flagged:
                flagged_count += 1
        print(f"  Flagged {flagged_count} kits (idempotent skip: {len(AMBIGUOUS_KITS_C) - flagged_count})")

        # Post-count: UNKNOWN kit-grain positives should now be 33 (38 - 5 fills)
        post_unknown = conn.execute(
            "SELECT COUNT(*) FROM canon_engine_key ce JOIN canon_corpus c ON c.kit_id=ce.kit_id "
            "WHERE c.grain='kit' AND c.negative=0 AND ce.econ_gaps LIKE '%UNKNOWN%'"
        ).fetchone()[0]
        assert post_unknown == 33, f"POST: UNKNOWN count = {post_unknown}, expected 33 (38-5)"
        print(f"\n[POST] econ:UNKNOWN kit-grain positives: {post_unknown} (expected 33 = 38 - 5 fills)")

        # POST asserts (iron law invariants must hold identical)
        _, post_breach = run_asserts(conn, "POST")
        if post_breach:
            print("HALT: POST-state assert breach. Rolling back.", file=sys.stderr)
            conn.rollback()
            sys.exit(3)

        # Schema-meta bump — record this migration in the ledger
        conn.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?, ?, ?)",
            (
                "econ-unknown-audit-2026-07-16",
                "2026-07-16T00:00:00Z",
                (
                    "Elrond econ:UNKNOWN bucket audit (S2 census V7 §2-§3 scoreboard input, "
                    "gandalf 2026-07-16 dc295719). 38 kit-grain UNKNOWN rows classified: "
                    "(a) 5 fills using existing bin vocabulary — chr-bleed-berserker + "
                    "chr-high-ranger-warden → spend (native); poe1-baron-zombies + "
                    "poe1-siege-ballista + gd-pet-conjurer → summon-uptime (gap:SU); "
                    "(b) 15 need new mapping rules (amendment-candidate list in report — "
                    "iron law: no new rules minted mid-run); (c) 18 evidence-thin, flagged "
                    "econ-audit-ambiguous-2026-07-16 (re-crawl candidates). All row-count "
                    "asserts hold identical (585/566/19/562/1-bt/0-orphans/4-dossier_owed). "
                    "Write scope limited: 5 cell_key economy-slot updates + 18 canon_corpus.flags "
                    "appends only; no other rows touched. Post-audit econ:UNKNOWN = 33 "
                    "(census bucket count drops 38 → 33 for next V8 rerun)."
                ),
            ),
        )

        conn.commit()
        print("\nEcon-audit APPLIED. All asserts held; committed.")

    except Exception as e:
        conn.rollback()
        print(f"\nHALT: exception during run — rolled back. {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
