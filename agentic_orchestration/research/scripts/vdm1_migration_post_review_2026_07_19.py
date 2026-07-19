#!/usr/bin/env python3
"""
VDM-1 POST-REVIEW MIGRATION (elrond, single writer on corpus.db).

Applies the eleven Matt-ratified rulings D-1..D-11 from
  agentic_orchestration/research/vdm1/MIGRATION-BRIEF-post-review.md
to research/curated/corpus.db, in the brief's "Execution order".

Nothing here re-opens a ruling. Every operation traces to a Matt-ratified ruling.
Runs in a single transaction (BEGIN..COMMIT); any assertion failure => rollback + abort.
Idempotency is NOT assumed: this is a one-shot migration against the post-INGEST-18
chain-head (md5 4a1ae47c...). Guards assert the expected pre-state before writing.

Backup is created OUTSIDE this script (elrond, HARD RULE 1) and md5-verified.
This script does NOT git-commit and does NOT create backups.
"""
import sqlite3
import json
import sys
import hashlib

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
EXPECTED_PRE_MD5 = "4a1ae47c7ded48f6443780602eb7e8ea"
UTC = "2026-07-19T20:04:46Z"

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def die(msg):
    print(f"\n!!! ABORT: {msg}", file=sys.stderr)
    sys.exit(1)

# ---- pre-flight: chain-head md5 guard -------------------------------------
pre_md5 = md5_of(DB)
print(f"[pre] corpus.db md5 = {pre_md5}")
if pre_md5 != EXPECTED_PRE_MD5:
    die(f"pre-migration md5 {pre_md5} != expected chain-head {EXPECTED_PRE_MD5}")

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

def scalar(sql, params=()):
    cur.execute(sql, params)
    r = cur.fetchone()
    return r[0] if r else None

def assert_eq(label, got, want):
    if got != want:
        die(f"{label}: got {got!r}, want {want!r}")
    print(f"  [assert] {label} == {want!r}  OK")

report = {}  # per-item change record for the MIGRATION doc

# ===========================================================================
# NOTE ON journal_mode / transaction: journal_mode is DELETE (house default).
# sqlite3 python driver opens an implicit deferred txn on the first DML; we
# make it explicit. DDL (ALTER/CREATE VIEW/DROP COLUMN) in modern SQLite
# (3.35+, DROP COLUMN support) is transactional and rolls back on abort.
# ===========================================================================
sqlite_ver = scalar("SELECT sqlite_version()")
print(f"[env] sqlite_version = {sqlite_ver}")
maj, minor, *_ = (int(x) for x in sqlite_ver.split("."))
if (maj, minor) < (3, 35):
    die(f"sqlite {sqlite_ver} < 3.35 required for ALTER TABLE DROP COLUMN (D-11b)")

cur.execute("BEGIN")
try:
    # -------------------------------------------------------------------
    # D-1 — Blind-rider errata (4 kits) → attestation-set edits in mapping_json
    # ERRATA-56..59. Element/ailment sets live inside mapping_json.skills[].
    # These are ATTESTATION-SET corrections (union/removal), not identity edits.
    # -------------------------------------------------------------------
    print("\n=== D-1 — blind-rider errata (ERRATA-56..59) ===")

    def load_map(kit):
        s = scalar("SELECT mapping_json FROM kit_mapping WHERE kit_id=?", (kit,))
        if s is None:
            die(f"D-1: kit_mapping row missing for {kit}")
        return json.loads(s)

    def save_map(kit, obj):
        txt = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        cur.execute("UPDATE kit_mapping SET mapping_json=? WHERE kit_id=?", (txt, kit))
        if cur.rowcount != 1:
            die(f"D-1: UPDATE affected {cur.rowcount} rows for {kit} (want 1)")

    def kit_element_set(obj):
        s = set()
        for sk in obj.get("skills", []):
            for f in ("element_primary", "element_secondary"):
                v = sk.get(f)
                if v:
                    s.add(v)
        return s

    def kit_ailment_set(obj):
        s = set()
        for sk in obj.get("skills", []):
            for a in (sk.get("ailments") or []):
                s.add(a)
        return s

    d1_notes = {}

    # ERRATA-56: d2-avenger element +water. cold(tri-element) -> water.
    # The Vengeance skill already carries element_primary=fire, element_secondary=lightning
    # with cold dropped to a delivery_note. Add water as the attested third element.
    # Engine skill objects carry only primary+secondary; a third attested element is
    # recorded via a dedicated attested_elements_errata field on the skill (provenance-
    # preserving; the original primary/secondary are NOT overwritten) so the D-11a view's
    # element aggregate (which unions primary+secondary+this errata field) reads truth.
    kit = "d2-avenger"
    obj = load_map(kit)
    before = kit_element_set(obj)
    veng = next((s for s in obj["skills"] if s.get("source_skill") == "Vengeance"), None)
    if veng is None:
        die("D-1/ERRATA-56: Vengeance skill not found in d2-avenger")
    veng.setdefault("attested_elements_errata", [])
    if "water" not in veng["attested_elements_errata"]:
        veng["attested_elements_errata"].append("water")
    veng["delivery_notes"] = (veng.get("delivery_notes", "") +
        " [ERRATA-56 2026-07-19: cold (the explicit third element of the tri-element "
        "'Fire, lightning and cold' attack) attests engine WATER; added to attested set "
        "via attested_elements_errata (primary/secondary provenance preserved). "
        "Blind-rider anchor, D-1.]")
    save_map(kit, obj)
    after = before | {"water"}
    d1_notes[kit] = (sorted(before), sorted(after))
    print(f"  ERRATA-56 {kit}: element {sorted(before)} -> {sorted(after)}")

    # ERRATA-57: le-runic-invocation element +fire +water. Runic Invocation skill has
    # element_primary=lightning; outputs "fire burst, ice storm, lightning fork" attest
    # all three. Add fire+water via attested_elements_errata.
    kit = "le-runic-invocation"
    obj = load_map(kit)
    before = kit_element_set(obj)
    ri = next((s for s in obj["skills"] if s.get("source_skill") == "Runic Invocation"), None)
    if ri is None:
        die("D-1/ERRATA-57: Runic Invocation skill not found in le-runic-invocation")
    ri.setdefault("attested_elements_errata", [])
    for e in ("fire", "water"):
        if e not in ri["attested_elements_errata"]:
            ri["attested_elements_errata"].append(e)
    ri["delivery_notes"] = (ri.get("delivery_notes", "") +
        " [ERRATA-57 2026-07-19: multi-element outputs 'fire burst, ice storm, lightning "
        "fork' attest engine FIRE + WATER (ice) alongside the lightning primary; added to "
        "attested set via attested_elements_errata. Blind-rider anchor, D-1.]")
    save_map(kit, obj)
    after = before | {"fire", "water"}
    d1_notes[kit] = (sorted(before), sorted(after))
    print(f"  ERRATA-57 {kit}: element {sorted(before)} -> {sorted(after)}")

    # ERRATA-58: d2-ghost-pvp element -shadow. "shadow" was the Shadow Discipline TREE
    # NAME on Mind Blast (name-only over-attest under D4 law). Remove shadow: set Mind
    # Blast element_primary shadow->null; record the strike in delivery_notes.
    kit = "d2-ghost-pvp"
    obj = load_map(kit)
    before = kit_element_set(obj)
    mb = next((s for s in obj["skills"] if s.get("source_skill") == "Mind Blast"), None)
    if mb is None:
        die("D-1/ERRATA-58: Mind Blast skill not found in d2-ghost-pvp")
    if mb.get("element_primary") != "shadow":
        die(f"D-1/ERRATA-58: Mind Blast element_primary is {mb.get('element_primary')!r}, expected 'shadow'")
    mb["element_primary"] = None
    mb["delivery_notes"] = (mb.get("delivery_notes", "") +
        " [ERRATA-58 2026-07-19: 'shadow' element STRUCK — it was the Shadow Discipline "
        "TREE NAME, a name-only over-attestation under the D4 name-only law (moderate "
        "confidence). Mind Blast attests stun (kept), not shadow damage. Blind-rider anchor, D-1.]")
    save_map(kit, obj)
    after = before - {"shadow"}
    d1_notes[kit] = (sorted(before), sorted(after))
    print(f"  ERRATA-58 {kit}: element {sorted(before)} -> {sorted(after)}")

    # ERRATA-59: gd-bwc-demolitionist ailment +burn (union, not replace). Blackwater
    # Cocktail already carries ailments=[blind]; add burn (burning-tar DoT). The kit's
    # full attested ailment set is {blind, curse:sap, burn}; curse:sap is the Thermite RR
    # (recorded in scaffold/fidelity, not on a skill ailments[] list). We add burn to the
    # BWC skill's ailments[] (the skill that carries the burning-tar DoT).
    kit = "gd-bwc-demolitionist"
    obj = load_map(kit)
    before_ail = kit_ailment_set(obj)
    bwc = next((s for s in obj["skills"] if s.get("source_skill") == "Blackwater Cocktail"), None)
    if bwc is None:
        die("D-1/ERRATA-59: Blackwater Cocktail skill not found in gd-bwc-demolitionist")
    bwc.setdefault("ailments", [])
    if "burn" not in bwc["ailments"]:
        bwc["ailments"].append("burn")
    bwc["delivery_notes"] = (bwc.get("delivery_notes", "") +
        " [ERRATA-59 2026-07-19: +burn — the burning-tar ground-DoT is an explicitly "
        "attested engine BURN (union with existing blind; curse:sap from Thermite RR "
        "unchanged). Reverses the mapping-time withhold ('burning tar' now ruled a named "
        "DoT status, not mere zone description). Blind-rider anchor, D-1.]")
    save_map(kit, obj)
    after_ail = before_ail | {"burn"}
    d1_notes[kit] = (sorted(before_ail), sorted(after_ail))
    print(f"  ERRATA-59 {kit}: ailment {sorted(before_ail)} -> {sorted(after_ail)}")

    report["D-1"] = d1_notes

    # errata_applied flag: kit_mapping has no errata_applied column; the flag lives on
    # verify_ledger (per D-8.3 the ledger is authoritative, DB counter subordinate).
    # Per brief D-1 ("set DB errata_applied on the touched rows") we set errata_applied=1
    # on any verify_ledger row for these 4 kits whose claim_family is the corrected axis
    # (identity/mechanics) and whose verdict is not already flagged. These are ATTESTATION
    # corrections; where no driving CONTRADICTED row exists (mirrors ERRATA-53/55 annotation
    # class), we record 0 flips honestly rather than fabricate a flag.
    d1_flag_counts = {}
    for kit in ("d2-avenger", "le-runic-invocation", "d2-ghost-pvp", "gd-bwc-demolitionist"):
        # flag the mechanics/identity CONTRADICTED rows if present (element/ailment ride mechanics)
        cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id=? AND claim_family IN ('identity','mechanics') "
            "AND verdict='CONTRADICTED' AND errata_applied=0", (kit,))
        d1_flag_counts[kit] = cur.rowcount
    report["D-1_verify_flags"] = d1_flag_counts
    print(f"  verify_ledger errata_applied flips (D-1): {d1_flag_counts} "
          f"(0 where no driving CONTRADICTED row — attestation-correction/annotation class)")

    # -------------------------------------------------------------------
    # D-7 — Kit-level annotations (deviation_notes). 7 items. Includes
    # D-7.5 chimera split (two annotation entries, one row) + D-7.6 alias strike.
    # -------------------------------------------------------------------
    print("\n=== D-7 — kit-level annotations (7 items) ===")

    def append_dev(kit, text, expect_exists=True):
        cur.execute("SELECT deviation_notes FROM kit_mapping WHERE kit_id=?", (kit,))
        r = cur.fetchone()
        if r is None:
            die(f"D-7: kit_mapping row missing for {kit}")
        old = r[0] or ""
        new = (old + (" " if old else "") + text).strip()
        cur.execute("UPDATE kit_mapping SET deviation_notes=? WHERE kit_id=?", (new, kit))
        if cur.rowcount != 1:
            die(f"D-7: UPDATE affected {cur.rowcount} rows for {kit} (want 1)")
        return old, new

    d7 = {}

    # D-7.1 d2-wl-void-rift — keep-as-ghost annotation
    k = "d2-wl-void-rift"
    append_dev(k, "[D-7.1 keep-as-ghost 2026-07-19: kb-hallucination-class ghost; harvest "
        "FAILED all four families (honest-negative); retained as a DOCUMENTED NEGATIVE, "
        "not excised (deletion is Matt-tier). Registered ghost, not a live kit.]")
    d7[k] = "keep-as-ghost annotation appended"

    # D-7.2 di-bombardment-wizard-pvp — d3->di misapplication flag; keep
    k = "di-bombardment-wizard-pvp"
    append_dev(k, "[D-7.2 2026-07-19: d3->di misapplication flag. The mapped identity is "
        "the attested DI Bombardment one; kept. (Bombardment absent from icy-veins full DI "
        "Wizard skill list — flag retained, kit not excised.)]")
    d7[k] = "d3->di misapplication flag appended; kept"

    # D-7.3 d4-spiritborn-vortex — component-class annotation; keep mapped
    k = "d4-spiritborn-vortex"
    append_dev(k, "[D-7.3 component-class 2026-07-19: skill, not archetype; Vortex is a "
        "triggered component inside Soar/Quill-Volley builds. Kept mapped as component-class.]")
    d7[k] = "component-class annotation appended; kept"

    # D-7.4 di-spiritform-druid-pvp — relabel the mis-specified-mechanic negative claim; keep
    #   (brief wrote 'd2-spiritform-druid-pvp'; the di-prefixed kit is the one carrying the
    #    negative flag and the mis-specified-mechanic record — anchor resolved to di-.)
    k = "di-spiritform-druid-pvp"
    append_dev(k, "[D-7.4 relabel 2026-07-19: the negative claim is RELABELED to its correct "
        "target — the underlying real DI Druid PvP content is a sustain-denial / CC-stack "
        "mechanic (mis-specified in this census entry), NOT a claim that 'spirit form' is a "
        "named DI skill. Negative flag retained on the corrected target; kit kept.]")
    d7[k] = "mis-specified-mechanic negative relabeled; kept"

    # D-7.5 le-harvest-lich — SPLIT the chimera into TWO deviation_notes entries
    #   (Harvest Flay + Death Seal Lich), each citing the basin-2 dossier anchor.
    #   Kit row stays ONE row (VDM-2 does any true two-kit split on LE re-crawl).
    k = "le-harvest-lich"
    append_dev(k,
        "[D-7.5 chimera-split 2026-07-19 — SUB-KIT 1 of 2 :: HARVEST FLAY :: cold-melee "
        "Reaper Form loop; maps to WATER + melee_arc (per basin-2 LE dossier skill_geometry "
        "anchor). This is the cold variant of the conflated folk name.] "
        "[D-7.5 chimera-split 2026-07-19 — SUB-KIT 2 of 2 :: DEATH SEAL LICH :: necrotic "
        "Low-Life tradeoff loop; maps to DEFENSIVE_TRADEOFF (per basin-2 LE dossier "
        "capstone_alterations anchor). This is the necrotic variant.] "
        "[D-7.5 note: annotation refinement on HELD basin-2 evidence — NO legolas re-fire "
        "(Matt: 'split at migration time, no legolas re-fire'). The kit_id remains one row; "
        "any true two-kit split defers to VDM-2 LE re-crawl.]")
    d7[k] = "chimera SPLIT into 2 sub-kit annotation entries (Harvest Flay + Death Seal Lich); one row"

    # D-7.6 poe1-earthshatter — STRIKE the phantom alias "Foulborn Ghostwrithe zerker(3.28)"
    #   The current deviation_notes says the alias "is correctly ignored"; replace that
    #   sentence with an explicit STRUCK record (REVIEW-1 resolved).
    k = "poe1-earthshatter"
    cur.execute("SELECT deviation_notes FROM kit_mapping WHERE kit_id=?", (k,))
    dev = cur.fetchone()[0]
    old_sentence = "The phantom 'Foulborn Ghostwrithe' alias is correctly ignored (no source fact)."
    new_sentence = ("[D-7.6 / poe1-REVIEW-1 STRUCK 2026-07-19: the phantom alias 'Foulborn "
        "Ghostwrithe zerker(3.28)' is STRICKEN as a confabulated alias (no source fact); "
        "REVIEW-1 resolved.]")
    if old_sentence not in dev:
        die(f"D-7.6: expected earthshatter alias sentence not found; deviation_notes drift")
    dev2 = dev.replace(old_sentence, new_sentence)
    cur.execute("UPDATE kit_mapping SET deviation_notes=? WHERE kit_id=?", (dev2, k))
    if cur.rowcount != 1:
        die("D-7.6: earthshatter UPDATE affected != 1 row")
    d7[k] = "phantom alias 'Foulborn Ghostwrithe zerker(3.28)' STRUCK (poe1-REVIEW-1 resolved)"

    # D-7.7 poe2-erasure-edc-lich — KEEP the possible-phantom annotation; NO deletion.
    #   Also basin-qualify the in-DB REVIEW token to the canonical 'b1-REVIEW-2' form
    #   (D-8.2 collision resolution — the DB carries the basin-1 Erasure REVIEW token in
    #    mech_note as "REVIEW-2, basin-1"; normalize to the machine-consistent 'b1-REVIEW-2').
    k = "poe2-erasure-edc-lich"
    append_dev(k, "[D-7.7 2026-07-19: possible-phantom annotation KEPT; NO deletion "
        "(poe2-REVIEW-2 / b1-REVIEW-2; deletion is Matt-only). 'Erasure' remains "
        "unverified-possible-phantom; Essence Drain + Contagion are CONFIRMED real.]")
    # D-8.2 basin-qualify the mech_note REVIEW token
    cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (k,))
    mn = cur.fetchone()[0]
    if "REVIEW-2, basin-1" in mn:
        mn2 = mn.replace("REVIEW-2, basin-1", "b1-REVIEW-2 (basin-1)")
        # also qualify the referenced peer "REVIEW-1 earthshatter" -> "poe1-REVIEW-1 earthshatter"
        mn2 = mn2.replace("per REVIEW-1 earthshatter", "per poe1-REVIEW-1 earthshatter")
        cur.execute("UPDATE canon_corpus SET mech_note=? WHERE kit_id=?", (mn2, k))
        if cur.rowcount != 1:
            die("D-7.7/D-8.2: erasure mech_note UPDATE affected != 1 row")
        d8_2_applied = True
    else:
        d8_2_applied = False
    d7[k] = ("possible-phantom annotation KEPT, no deletion; "
             + ("mech_note REVIEW token basin-qualified to b1-REVIEW-2" if d8_2_applied
                else "no bare REVIEW token to qualify"))

    report["D-7"] = d7
    print("  D-7 annotations applied to 7 kits (incl. .5 split, .6 strike, .7 keep):")
    for kk, vv in d7.items():
        print(f"    {kk}: {vv}")

    # -------------------------------------------------------------------
    # D-3 — Mint-all + three-tier evidence stamp (mint_ledger).
    #   (1) ADD columns evidence_tier, build_authorized. Set every mint status='matt-ratified'.
    #   (2) Stamp the 6 existing + promote the held accrual families to NEW rows.
    # -------------------------------------------------------------------
    print("\n=== D-3 — mint tier stamp + accrual rows ===")

    # (1) add columns
    cur.execute("ALTER TABLE mint_ledger ADD COLUMN evidence_tier TEXT "
                "CHECK(evidence_tier IN ('A-attested','B-quantitative','C-provisional') OR evidence_tier IS NULL)")
    cur.execute("ALTER TABLE mint_ledger ADD COLUMN build_authorized INTEGER "
                "CHECK(build_authorized IN (0,1) OR build_authorized IS NULL)")
    print("  ADD COLUMN mint_ledger.evidence_tier, mint_ledger.build_authorized")

    # (2a) stamp the 6 existing candidates: tier + build_authorized + status
    existing_tiers = {
        1: ("B-quantitative", 1),  # chain fan-out >1.0 (quant)
        2: ("A-attested",     1),  # stack-parameterizes-geometry (GRADUATED-3)
        3: ("A-attested",     1),  # out-and-return (spectral-throw +5 siblings = 6-kit)
        4: ("B-quantitative", 1),  # temp-minion swarm ~20 (quant)
        5: ("B-quantitative", 1),  # placed-proxy totem count (quant)
        6: ("C-provisional",  0),  # enemy-seeking mobile AoE (1 kit)
    }
    for mid, (tier, ba) in existing_tiers.items():
        cur.execute("UPDATE mint_ledger SET evidence_tier=?, build_authorized=?, "
                    "status='matt-ratified' WHERE mint_id=?", (tier, ba, mid))
        if cur.rowcount != 1:
            die(f"D-3: existing mint_id {mid} stamp affected {cur.rowcount} rows (want 1)")
    print(f"  stamped 6 existing mints with evidence_tier/build_authorized/status='matt-ratified'")

    # (2b) NEW accrual-family rows. mechanism text + forcing-kit list + provenance.
    #   forced_by_kits = JSON array of resolved corpus kit_ids (anchor-resolved).
    #   provenance recorded in ladder_step_audit as 'book§4-accrual' (no provenance col;
    #   ladder_step_audit is the free-text provenance/audit field on mint_ledger).
    accrual_rows = [
        dict(
            mint_class="qualitative",
            description=("two-tier-accumulator: a build-up -> payoff grammar where an "
                "accumulator FILLS on one action-tier (combo-beat / stack / rune-slot / "
                "charge) and DISCHARGES on a second (invoke / spend / release), the two "
                "tiers being distinct mechanics rather than one magnitude scalar. The "
                "genre's dominant 'accumulate-then-unleash' pattern; the run's largest "
                "accrual mass (~10 kits, strengthening every basin). Engine accumulator "
                "scales a single magnitude; this needs a two-tier fill/discharge substrate."),
            forced_by_kits=["poe2-shaman-bear", "poe2-walking-calamity",
                            "gd-cadence-witchblade", "le-tempest-strike",
                            "le-runic-invocation", "d3-raekor-boulder",
                            "d3-raiment-shenlong", "d3-vyr-archon"],
            ladder_step_audit=("book§4-accrual :: ~10 evidence kits (shaman-bear + "
                "walking-calamity = basin-1 WATCH-ITEM; Cadence = krieg+belgothian two-shape "
                "evidence; le-tempest-strike = TWO fetched shapes counted [combo-beat + "
                "stack-spend]; le-runic-invocation = rune-accrue->invoke-spend; d3 family = "
                "raekor/shenlong/vyr archon accumulators). LE Shadow Daggers routes here per "
                "D-6 (stack-payoff, not an ailment). qual-mint forced by >=3 independent kits."),
            evidence_tier="A-attested",
            build_authorized=1,
        ),
        dict(
            mint_class="qualitative",
            description=("roaming-persistent-AoE / twister: a persistent AoE entity that "
                "roams/drifts across the field for its duration (the 27th-geometry "
                "question). Distinct from R-M6 drift-tick (passive travel along cast line) "
                "and from D-3#6 enemy-seeking (active chase) — this is undirected roaming "
                "persistence."),
            forced_by_kits=["poe2-twister"],
            ladder_step_audit=("book§4-accrual :: twister (~1 kit; the 27th-geometry "
                "question). C-provisional: single forcing kit; VDM-2 corroborate-or-drop."),
            evidence_tier="C-provisional",
            build_authorized=0,
        ),
        dict(
            mint_class="qualitative",
            description=("HoWA attribute-total-as-flat-damage: total of a primary attribute "
                "(e.g. Dexterity via Hand of Wisdom and Action) converts directly to flat "
                "added elemental damage on hits — a qualitative stat->damage coupling, not a "
                "numeric range extension of an existing damage source."),
            forced_by_kits=["poe2-howa-invoker", "poe2-gemling-stacker"],
            ladder_step_audit=("book§4-accrual :: HoWA/gemling (~1-2 kits). C-provisional: "
                "thin evidence; VDM-2 corroborate-or-drop watch-list."),
            evidence_tier="C-provisional",
            build_authorized=0,
        ),
        dict(
            mint_class="qualitative",
            description=("GD wandering-emitter: an autonomous emitter entity that WANDERS "
                "the field (undirected patrol), periodically emitting attacks — the Grim "
                "Dawn Wind Devil pattern. Distinct from placed-proxy (static) and enemy-"
                "attached-emitter (bound to a target)."),
            forced_by_kits=[],  # NO discrete corpus kit_id at map-time — see ladder_step_audit
            ladder_step_audit=("book§4-accrual :: GD Wind Devil wandering-emitter (~1). "
                "ANCHOR NOTE: no discrete corpus kit_id carries this pattern as its primary "
                "identity at map-time (the GD Wind Devil / Druid-Elementalist wandering-"
                "emitter was not decomposed into its own corpus row); forcing-kit recorded "
                "as descriptive anchor only, NOT a fabricated kit_id. C-provisional; VDM-2 "
                "corroborate-or-drop (and decompose the anchor kit if it materializes)."),
            evidence_tier="C-provisional",
            build_authorized=0,
        ),
        dict(
            mint_class="qualitative",
            description=("GD enemy-attached-emitter: an emitter entity that ATTACHES to an "
                "enemy and emits from that anchor for its duration — the Grim Dawn Storm Box "
                "of Elgoloth pattern. Distinct from wandering (free) and placed (static-"
                "ground) emitters."),
            forced_by_kits=["gd-stormbox-elementalist"],
            ladder_step_audit=("book§4-accrual :: GD Storm Box enemy-attached-emitter (~1 "
                "kit). C-provisional; VDM-2 corroborate-or-drop."),
            evidence_tier="C-provisional",
            build_authorized=0,
        ),
        dict(
            mint_class="qualitative",
            description=("GD proximity-armed-trigger: a placed device that ARMS on enemy "
                "proximity and detonates when the proximity condition is met — the Grim Dawn "
                "Rune of Hagarrad pattern. A proximity-fused placed proxy, distinct from "
                "cast-detonated or timed placements."),
            forced_by_kits=["gd-roh-infiltrator"],
            ladder_step_audit=("book§4-accrual :: GD Rune of Hagarrad proximity-armed-trigger "
                "(~1 kit). C-provisional; VDM-2 corroborate-or-drop."),
            evidence_tier="C-provisional",
            build_authorized=0,
        ),
    ]

    # guard: all non-empty forcing kit_ids must resolve to canon_corpus rows
    for row in accrual_rows:
        for kid in row["forced_by_kits"]:
            exists = scalar("SELECT 1 FROM canon_corpus WHERE kit_id=?", (kid,))
            if not exists:
                die(f"D-3 accrual: forcing kit_id {kid!r} not in canon_corpus")

    new_mint_ids = []
    for row in accrual_rows:
        cur.execute(
            "INSERT INTO mint_ledger (mint_class, description, forced_by_kits, "
            "ladder_step_audit, status, evidence_tier, build_authorized) "
            "VALUES (?,?,?,?,?,?,?)",
            (row["mint_class"], row["description"],
             json.dumps(row["forced_by_kits"], separators=(",", ":")),
             row["ladder_step_audit"], "matt-ratified",
             row["evidence_tier"], row["build_authorized"]))
        new_mint_ids.append(cur.lastrowid)
    print(f"  inserted {len(new_mint_ids)} NEW accrual-family mint rows: mint_ids {new_mint_ids}")
    report["D-3_new_mint_ids"] = new_mint_ids
    report["D-3_existing_tiers"] = existing_tiers

    # -------------------------------------------------------------------
    # D-4 — Docket ratifications + § 5 family consolidation (mechanic_gap_docket).
    #   1. 8 rows -> status='matt-ratified'
    #   2. four mint-or-declare forks -> disposition='engine-design-intake'
    #   3. two intentional-guard collisions -> disposition='working-as-intended'
    #   4. consolidate 87 held rows -> §5.2 taxonomy (family-tag mechanism; schema call)
    # -------------------------------------------------------------------
    print("\n=== D-4 — docket ratify + §5 consolidation ===")

    # add a disposition column (no such column exists; brief uses disposition='...')
    cur.execute("ALTER TABLE mechanic_gap_docket ADD COLUMN disposition TEXT")
    # add a docket_family column to carry the §5.2 taxonomy family-tag (schema call:
    # family-tag the rows rather than roll to family rows, preserving row identity + member lists)
    cur.execute("ALTER TABLE mechanic_gap_docket ADD COLUMN docket_family TEXT")
    print("  ADD COLUMN mechanic_gap_docket.disposition, mechanic_gap_docket.docket_family")

    # 1 + 2 + 3: status + disposition per row (docket_id -> (disposition))
    #   Row 4 is compound (stun-magnitude-as-damage DECLARE-half + perma-stunlock COLLISION-half).
    #   A single row holds one disposition; primary = engine-design-intake (the mint-or-declare
    #   fork); the working-as-intended collision-half is recorded in the disposition_note. The
    #   RULING (both halves as Matt stated) is preserved; only the single-column mechanism is a
    #   schema call.
    docket_dispositions = {
        1: ("engine-design-intake", "D-4.2 mint-or-declare fork: entity-as-consumable-resource-pool"),
        2: ("permanent-gap-record", "D-4.1 permanent gap record: ally-buff-projection party-support scope (solo-engine boundary; +5 LA siblings). NOT a mint request."),
        3: ("permanent-gap-record", "D-4.1 permanent gap record: RNG-element-pool identity; prunable=build / unprunable=trap distinction must survive future design."),
        4: ("engine-design-intake", "D-4.2 DECLARE-half (stun-magnitude-as-damage) -> engine-design-intake. D-4.3 COLLISION-half (perma-stunlock floor / heavy-strike-stun) -> WORKING-AS-INTENDED: the anti-stunlock floor is a design position, not a gap. Compound row; both halves ruled."),
        5: ("permanent-gap-record", "D-4.1 permanent gap record: self-damage cast-cost redirected to a proxy life-pool (cost-payer redirection primitive absent)."),
        6: ("working-as-intended", "D-4.3 intentional-guard collision: closed-loop self-damage trigger economy vs MAX_CHAIN_DEPTH=1 LOCKED. The guard IS the design."),
        7: ("engine-design-intake", "D-4.2 mint-or-declare fork: world-entity-capture minion pool (spectres); capture-from-world + ability-inheritance lanes absent."),
        8: ("engine-design-intake", "D-4.2 mint-or-declare fork: attribute-value -> proxy-count coupling (siege-ballista); stat-as-army-size."),
    }
    for did, (disp, note) in docket_dispositions.items():
        cur.execute("UPDATE mechanic_gap_docket SET status='matt-ratified', disposition=?, "
                    "docket_family=? WHERE docket_id=?",
                    (disp, "stat-as-damage-substrate" if did == 4 else None, did))
        # note text: append to provenance_json as a disposition_note (preserve existing prov)
        cur.execute("SELECT provenance_json FROM mechanic_gap_docket WHERE docket_id=?", (did,))
        pj = cur.fetchone()[0]
        try:
            pjobj = json.loads(pj) if pj else {}
            if not isinstance(pjobj, dict):
                pjobj = {"_prior": pjobj}
        except Exception:
            pjobj = {"_prior_text": pj}
        pjobj["disposition_note"] = note
        pjobj["disposition_ruling"] = "D-4 (Matt-ratified 2026-07-19)"
        cur.execute("UPDATE mechanic_gap_docket SET provenance_json=? WHERE docket_id=?",
                    (json.dumps(pjobj, separators=(",", ":"), ensure_ascii=False), did))
    print(f"  8 docket rows -> status='matt-ratified' + disposition set "
          f"(4 engine-design-intake, 3 permanent-gap-record, 1 working-as-intended; row 4 compound)")

    # 4. §5.2 taxonomy consolidation. The 87 held rows are NOT in mechanic_gap_docket
    #    (TIER-2 HOLD kept them as static side-files, per INGEST-18 doc). We INGEST the
    #    §5.2 family STRUCTURE as canonical family rows (docket taxonomy), with member
    #    lists + dispositions, and mark them as family/taxonomy rows (destination-tagged).
    #    Side-files freeze as lineage after ingest (D-11f inversion). The stat-as-damage
    #    6-way split is kept intact (DO-NOT-MERGE) inside the stat-as-damage-substrate family.
    #    Schema call: roll the taxonomy to FAMILY rows (mechanism_class = family name,
    #    docket_family = family key, status='matt-ratified', disposition per §5.2 lean),
    #    spec_text_or_path carries the member/DO-NOT-MERGE list. This is the "roll to family
    #    rows with member lists" option the brief authorizes.
    family_rows = [
        dict(family="summoner-deferral",
             disp="engine-design-intake",  # flipped by D-5 below; seeded here as the family row
             members="~23 rows across all basins incl. army-GAP CotA/gargantuan; golemancer, "
                     "zuni-carnevil, rathma, minion-necro, pet-conjurer, skeleton-necro, "
                     "wraithlord, liche-king, petmaster, mechanist, pet-warden, bot-engineer, "
                     "alchemist-summoner, moto-bots, mcd-summoner, master-summoner",
             note="D-5 un-deferral applies to THIS family (see D-5 block): "
                  "deferred/Phase-5/evidence-bank -> matt-ratified / engine-design-intake."),
        dict(family="stat-as-damage-substrate",
             disp="engine-design-intake",
             members="6 DO-NOT-MERGE mechanisms [armour-value | armor-conversion | "
                     "stun-substrate | block-chance | max-Mana->minion | missing-Mana->spell] "
                     "+ accruals [retaliation, thorns x2, reservation-as-scaler, tli-rosa]. "
                     "~12 rows. KEEP 6-WAY SPLIT INTACT (DO-NOT-MERGE).",
             note="D-4 §5.2: keep 6-way split; engine-design intake."),
        dict(family="spatial-consumable-resource-node",
             disp="engine-design-intake",
             members="d2-berserker, grim-ward, trapsin, pestilence, infinimist, shadowblight, "
                     "di-corpse-explosion (7). Sibling of DB row 1 (entity-as-consumable-"
                     "resource-pool) — same intake.",
             note="D-4 §5.2: sibling of DB row 1; same engine-design intake."),
        dict(family="support-party-scope",
             disp="permanent-gap-record",
             members="LA cluster (5 rows: liberator-valkyrie, judgment/blessed-aura paladins, "
                     "desperate-salvation bard, full-bloom artist). Folds into DB row 2 as siblings.",
             note="D-4 §5.2: fold into DB row 2 (ally-buff-projection) as siblings."),
        dict(family="loot-economy-identity",
             disp="permanent-out-of-scope",
             members="berserker Find-Item, horker, throw-barb, firebomb (4). Loot meta != combat kit.",
             note="D-4 §5.2: permanent out-of-scope record (loot meta is not a combat kit)."),
        dict(family="mode-swap-identity",
             disp="hold",
             members="deadeye, peacemaker, iris2 (3). GX-02 form-swap gate adjacents.",
             note="D-4 §5.2: GX-02 form-swap adjacents; hold."),
        dict(family="roguelite-idiom",
             disp="permanent-genre-law-record",
             members="hades1: delayed-detonation Doom, deflect, self-cost-contract, "
                     "duo-boon-pair, finite-ammo-burst, per-arrow-status (6).",
             note="D-4 §5.2: genre-law records; no engine action."),
        dict(family="minion-consumption-harvest",
             disp="standing-family-record",
             members="wraithlord + zero-dogs (2-kit evidence).",
             note="D-4 §5.2: reached 2-kit evidence; named as a standing family."),
        dict(family="recipe-combination-determines-output",
             disp="standing-family-record",
             members="runic-invocation + tli-rosa (2-kit evidence).",
             note="D-4 §5.2: reached 2-kit evidence; named as a standing family."),
        dict(family="gear-stat-as-minion-scaling",
             disp="standing-family-record",
             members="manifest-armor + golemancer (2-kit evidence).",
             note="D-4 §5.2: reached 2-kit evidence; named as a standing family."),
        dict(family="held-singletons",
             disp="hold",
             members="1-each: contact-propagation-DoT rabies | utility-transport teleport-sorc | "
                     "mosaic inverted-spend | item-count-multiplier lod | mobility-gap blade-shift | "
                     "placement-barrier bone-wall | link-rune geometry-modifier | cooldown-reset "
                     "chronomancer | overheal/ES-above-cap [merged 1 class] | density-reactive "
                     "cadence | throw-retrieve reload | ward-from-missing-health | maintenance-"
                     "reservation | pet-death-payload | unshipped-content wereforms | fully-"
                     "unattested snowstorm | element-unresolved moto-bots.",
             note="D-4 §5.2: hold as filed (each a singleton mechanism)."),
    ]
    fam_ids = []
    for fr in family_rows:
        prov = json.dumps({
            "provenance": "book§5.2-consolidation",
            "docket_family_row": True,
            "member_list": fr["members"],
            "disposition_note": fr["note"],
            "disposition_ruling": "D-4 §5.2 (Matt-ratified 2026-07-19)",
        }, separators=(",", ":"), ensure_ascii=False)
        cur.execute(
            "INSERT INTO mechanic_gap_docket (mechanism_class, spec_text_or_path, "
            "evidence_kits, destination, status, disposition, docket_family, provenance_json) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (f"[§5.2 FAMILY] {fr['family']}", fr["members"], None,
             "book-consolidation", "matt-ratified", fr["disp"], fr["family"], prov))
        fam_ids.append(cur.lastrowid)
    print(f"  inserted {len(fam_ids)} §5.2 taxonomy FAMILY rows (docket_id {fam_ids[0]}..{fam_ids[-1]}); "
          f"stat-as-damage 6-way split kept intact")
    report["D-4_family_ids"] = fam_ids
    report["D-4_family_count"] = len(family_rows)

    # -------------------------------------------------------------------
    # D-5 — Summoner un-deferral (disposition flip; NO kit re-mapping).
    #   The summoner-deferral FAMILY row (just created) flips to engine-design-intake +
    #   matt-ratified (already seeded at engine-design-intake above), and is cross-linked
    #   to the resolved matt_decision_needed doc. NO kit re-mapping (the ~21 GAPPED
    #   summoner kits stay mapped-to-deferral in the snapshot).
    # -------------------------------------------------------------------
    print("\n=== D-5 — summoner un-deferral (disposition flip only) ===")
    crosslink = ("canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md "
                 "[RESOLVED 2026-07-06, Matt ruled Option 1 — build the summon-skill GENERATION "
                 "path]. D-5 is the MAPPING-side twin of that EMISSION-side commit; the mapped "
                 "corpus summoners become validation targets for the built gen-path. NO kit "
                 "re-mapping: the ~21 GAPPED summoner kits stay mapped-to-deferral in the VDM-1 "
                 "snapshot (correct — the primitive did not exist at map-time). Only the docket "
                 "DISPOSITION changes: deferred/Phase-5/evidence-bank -> matt-ratified / "
                 "engine-design-intake.")
    cur.execute("SELECT provenance_json FROM mechanic_gap_docket "
                "WHERE docket_family='summoner-deferral' AND mechanism_class LIKE '[§5.2 FAMILY]%'")
    r = cur.fetchone()
    if r is None:
        die("D-5: summoner-deferral family row not found")
    pjobj = json.loads(r[0])
    pjobj["D5_undeferral"] = "deferred/Phase-5/evidence-bank -> matt-ratified / engine-design-intake"
    pjobj["D5_crosslink"] = crosslink
    pjobj["D5_ruling"] = "D-5 (Matt-ratified 2026-07-19; overturns book reaffirm-lean)"
    cur.execute("UPDATE mechanic_gap_docket SET disposition='engine-design-intake', "
                "status='matt-ratified', provenance_json=? "
                "WHERE docket_family='summoner-deferral' AND mechanism_class LIKE '[§5.2 FAMILY]%'",
                (json.dumps(pjobj, separators=(",", ":"), ensure_ascii=False),))
    if cur.rowcount != 1:
        die(f"D-5: summoner-deferral flip affected {cur.rowcount} rows (want 1)")
    print("  summoner-deferral family row FLIPPED to engine-design-intake + matt-ratified; "
          "cross-linked to matt_decision_needed (RESOLVED Option 1); NO kit re-mapping")
    report["D-5"] = "summoner-deferral family: disposition flip only; 0 kit re-maps"

    # -------------------------------------------------------------------
    # D-8 — Normalizations (+ D-11d)
    #   .1 corpus_bucket Diablo tokens -> canonical short form
    #   .2 REVIEW-numbering basin-qualify (handled in D-7.7 for the sole DB token)
    #   .3 errata bookkeeping law (standing; counter reflects it — no numeric change here)
    #   .4 / D-11d suffix_rekey_status 107 'awaiting-rekey' -> 'complete-kit-mapping'
    # -------------------------------------------------------------------
    print("\n=== D-8 — normalizations + D-11d ===")

    # D-8.1 corpus_bucket
    bucket_map = {"diablo-3": "d3", "diablo-4": "d4", "diablo-immortal": "di"}
    d8_1 = {}
    for old, new in bucket_map.items():
        n = scalar("SELECT count(*) FROM canon_corpus WHERE corpus_bucket=?", (old,))
        cur.execute("UPDATE canon_corpus SET corpus_bucket=? WHERE corpus_bucket=?", (new, old))
        d8_1[old] = (n, cur.rowcount, new)
    print(f"  D-8.1 corpus_bucket normalized: "
          + ", ".join(f"{o}->{v[2]} ({v[1]} rows)" for o, v in d8_1.items()))
    report["D-8.1"] = d8_1

    # D-8.2 recorded: sole DB-resident REVIEW token was basin-qualified in D-7.7.
    report["D-8.2"] = ("sole DB REVIEW token (poe2-erasure-edc-lich.mech_note) basin-qualified "
                       "to b1-REVIEW-2 in D-7.7; the poe1-REVIEW-2 (poets-pen-vd) collision "
                       "partner is doc-only [review rosters/errata-ledger], not in the DB")

    # D-8.4 / D-11d suffix_rekey_status: the awaited re-key IS kit_mapping (now complete).
    #   107 'awaiting-rekey' rows -> 'complete-kit-mapping'. mob/elem raws are permanent
    #   'descriptor-final' and are NOT in the 107 (those were never 'awaiting-rekey').
    n_await = scalar("SELECT count(*) FROM canon_corpus WHERE suffix_rekey_status='awaiting-rekey'")
    cur.execute("UPDATE canon_corpus SET suffix_rekey_status='complete-kit-mapping' "
                "WHERE suffix_rekey_status='awaiting-rekey'")
    n_moved = cur.rowcount
    print(f"  D-11d suffix_rekey_status: {n_moved} 'awaiting-rekey' -> 'complete-kit-mapping' "
          f"(the awaited re-key IS kit_mapping, now complete)")
    report["D-11d"] = (n_await, n_moved)

    # -------------------------------------------------------------------
    # D-11b — DROP dead columns (verified 0-populated pre-flight; re-assert here).
    # -------------------------------------------------------------------
    print("\n=== D-11b — drop dead columns ===")
    dead_cols = ["motion_frame", "t4_doors", "option_c_substrate_flags"]
    d11b_counts = {}
    for col in dead_cols:
        pop = scalar(f"SELECT count({col}) FROM canon_corpus")
        d11b_counts[col] = pop
        if pop != 0:
            die(f"D-11b: {col} is {pop}-populated (want 0) — refusing to DROP")
    print(f"  precondition: {d11b_counts} (all 0-populated) — VERIFIED")
    for col in dead_cols:
        cur.execute(f"ALTER TABLE canon_corpus DROP COLUMN {col}")
    print(f"  DROPPED columns: {dead_cols}")
    report["D-11b"] = d11b_counts

    # -------------------------------------------------------------------
    # D-11c — deprecate canon_corpus.source_urls (freeze + comment-deprecate; do NOT drop).
    #   Record the deprecation in corpus_schema_meta (schema meta is the deprecation home);
    #   kit_citations is the sole citation authority. Data preserved (60 rows untouched).
    # -------------------------------------------------------------------
    print("\n=== D-11c — deprecate source_urls (freeze, do not drop) ===")
    n_su = scalar("SELECT count(source_urls) FROM canon_corpus")
    print(f"  source_urls populated rows: {n_su} (FROZEN; not dropped; deprecated via schema_meta). "
          f"kit_citations is sole citation authority.")
    report["D-11c"] = n_su

    # -------------------------------------------------------------------
    # D-11e — citation orphan. legolas micro-fetch ABSENT (checked pre-run). Record honest
    #   573/574 residue. (A trailing one-row fold into kit_citations closes to 574/574 if a
    #   citation lands later.)
    # -------------------------------------------------------------------
    print("\n=== D-11e — citation orphan (ud-snowstorm-frost) ===")
    cite_cov = scalar("SELECT count(DISTINCT kit_id) FROM kit_citations WHERE quarantined=0 "
                      "AND kit_id IN (SELECT kit_id FROM kit_mapping)")
    orphan = scalar("SELECT count(*) FROM kit_mapping WHERE kit_id NOT IN "
                    "(SELECT DISTINCT kit_id FROM kit_citations WHERE quarantined=0)")
    print(f"  citation coverage: {cite_cov}/574 mapped kits with non-quarantined citation; "
          f"{orphan} orphan (ud-snowstorm-frost). legolas micro-fetch ABSENT -> honest 573/574 "
          f"residue recorded (citation-pending).")
    report["D-11e"] = dict(coverage=cite_cov, orphan=orphan, legolas_present=False)

    # -------------------------------------------------------------------
    # D-11a — CREATE kit_master VIEW (identity ⋈ mapping ⋈ citation-agg ⋈ verify-tally ⋈ dossier-count).
    #   Live-computed, cannot drift. Element/ailment sets aggregated from mapping_json.skills[].
    #   Provenance-only: does NOT expose elem_raw / suffix raws.
    #   The compendium regenerates FROM this view (separate step, post-migration, read-only).
    # -------------------------------------------------------------------
    print("\n=== D-11a — create kit_master view ===")
    cur.execute("DROP VIEW IF EXISTS kit_master")
    # element/ailment aggregation: primary+secondary+attested_elements_errata across skills.
    # SQLite JSON aggregation via json_group_array over json_each on the skills array is verbose;
    # we build the aggregates as correlated subqueries producing distinct sorted token lists.
    cur.execute(r"""
    CREATE VIEW kit_master AS
    SELECT
        c.kit_id,
        c.folk_name,
        c.game,
        c.corpus_bucket,
        c.tier,
        c.canon_tier,
        c.eras,
        c.negative,
        c.is_system,
        c.lineage,
        c.gx,
        c.source,
        c.provenance_tag,
        c.source_date,
        -- mapping (grade/terminal/deviation)
        m.grade,
        m.terminal_state,
        m.deviation_notes,
        m.mapping_provenance,
        -- element attested set (primary + secondary + ERRATA-added), distinct, from mapping_json.skills[]
        (SELECT group_concat(el, ',') FROM (
            SELECT DISTINCT el FROM (
                SELECT json_extract(s.value,'$.element_primary')   AS el FROM json_each(m.mapping_json,'$.skills') s
                UNION
                SELECT json_extract(s.value,'$.element_secondary') AS el FROM json_each(m.mapping_json,'$.skills') s
                UNION
                SELECT ee.value AS el FROM json_each(m.mapping_json,'$.skills') s,
                       json_each(COALESCE(json_extract(s.value,'$.attested_elements_errata'),'[]')) ee
            ) WHERE el IS NOT NULL ORDER BY el
        )) AS elements_attested,
        -- ailment attested set, distinct, from mapping_json.skills[].ailments[]
        (SELECT group_concat(al, ',') FROM (
            SELECT DISTINCT al FROM (
                SELECT a.value AS al FROM json_each(m.mapping_json,'$.skills') s,
                       json_each(COALESCE(json_extract(s.value,'$.ailments'),'[]')) a
            ) WHERE al IS NOT NULL ORDER BY al
        )) AS ailments_attested,
        -- citation aggregate (non-quarantined only): count + JSON array of {url,archive_url,site,author_handle,cite_class}
        (SELECT count(*) FROM kit_citations kc WHERE kc.kit_id=c.kit_id AND kc.quarantined=0) AS citation_count,
        (SELECT json_group_array(json_object(
                    'url', kc.url, 'archive_url', kc.archive_url, 'site', kc.site,
                    'author_handle', kc.author_handle, 'cite_class', kc.cite_class))
         FROM kit_citations kc WHERE kc.kit_id=c.kit_id AND kc.quarantined=0) AS citations_json,
        -- verify C/X/U tallies
        (SELECT count(*) FROM verify_ledger v WHERE v.kit_id=c.kit_id AND v.verdict='CONFIRMED')    AS verify_confirmed,
        (SELECT count(*) FROM verify_ledger v WHERE v.kit_id=c.kit_id AND v.verdict='CONTRADICTED')  AS verify_contradicted,
        (SELECT count(*) FROM verify_ledger v WHERE v.kit_id=c.kit_id AND v.verdict='UNSUPPORTED')   AS verify_unsupported,
        -- dossier row-count
        (SELECT count(*) FROM kit_dossier d WHERE d.kit_id=c.kit_id) AS dossier_rows
    FROM canon_corpus c
    JOIN kit_mapping m ON m.kit_id = c.kit_id
    """)
    km_rows = scalar("SELECT count(*) FROM kit_master")
    print(f"  kit_master view CREATED; row count = {km_rows} (expect 574)")
    if km_rows != 574:
        die(f"D-11a: kit_master row count {km_rows} != 574")
    # sanity: element aggregate reflects D-1 errata
    av_el = scalar("SELECT elements_attested FROM kit_master WHERE kit_id='d2-avenger'")
    gh_el = scalar("SELECT elements_attested FROM kit_master WHERE kit_id='d2-ghost-pvp'")
    bwc_al = scalar("SELECT ailments_attested FROM kit_master WHERE kit_id='gd-bwc-demolitionist'")
    print(f"  [sanity] d2-avenger elements = {av_el!r} (expect fire,lightning,water)")
    print(f"  [sanity] d2-ghost-pvp elements = {gh_el!r} (expect lightning only)")
    print(f"  [sanity] gd-bwc-demolitionist ailments = {bwc_al!r} (expect blind,burn or contains burn)")
    if av_el is None or "water" not in av_el:
        die("D-11a: d2-avenger elements aggregate missing water (D-1 errata not reflected)")
    if gh_el is not None and "shadow" in gh_el:
        die("D-11a: d2-ghost-pvp elements aggregate still contains shadow (D-1 errata not reflected)")
    if bwc_al is None or "burn" not in bwc_al:
        die("D-11a: gd-bwc-demolitionist ailments aggregate missing burn (D-1 errata not reflected)")
    report["D-11a_view_rows"] = km_rows

    # -------------------------------------------------------------------
    # D-10 — Corpus v1.1 stamp (corpus_schema_meta). md5 stamped AFTER commit (post-migration
    #   md5 is computed on the closed DB file); we insert the meta row now with a placeholder
    #   and UPDATE the md5 post-commit. To keep it single-pass we insert with md5='PENDING-POST-COMMIT'
    #   and the wrapper updates it. Simpler + honest: insert the v1.1 row now WITHOUT md5, then a
    #   second tiny connection stamps md5 after close (md5 of a file mid-open-txn is meaningless).
    # -------------------------------------------------------------------
    print("\n=== D-10 — corpus v1.1 stamp (pre-md5 row) ===")
    note = ("VDM-1 POST-REVIEW RATIFICATION (elrond). Applies Matt-ratified D-1..D-11 "
            "(REVIEW-BOOK.md §2 + Matt margins 2026-07-19): 4 blind-rider errata (ERRATA-56..59); "
            "mint 3-tier stamp + 6 accrual-family rows; 8 docket ratifications + §5.2 taxonomy "
            "consolidation (11 family rows); summoner un-deferral (D-5 disposition flip); 7 D-7 "
            "kit annotations; corpus_bucket + suffix_rekey normalizations; kit_master view (574); "
            "dropped 3 dead columns; source_urls deprecated (frozen); citation coverage 573/574 "
            "(ud-snowstorm-frost citation-pending). post-md5 stamped post-commit.")
    cur.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                ("v1.1-verified", UTC, note))
    # D-11c deprecation record (schema_meta is the deprecation home)
    cur.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                ("v1.1-deprecation-source_urls", UTC,
                 "D-11c: canon_corpus.source_urls DEPRECATED (frozen, 60 rows preserved, NOT "
                 "dropped). kit_citations is the SOLE citation authority (0 kit-level orphan URLs). "
                 "Do not read source_urls for truth."))
    print("  inserted corpus_schema_meta v1.1-verified + source_urls-deprecation rows (md5 PENDING)")

    # -------------------------------------------------------------------
    # integrity + foreign-key checks BEFORE commit
    # -------------------------------------------------------------------
    print("\n=== pre-commit integrity checks ===")
    ic = scalar("PRAGMA integrity_check")
    assert_eq("integrity_check", ic, "ok")
    cur.execute("PRAGMA foreign_key_check")
    fk = cur.fetchall()
    if fk:
        die(f"foreign_key_check returned {len(fk)} rows: {fk[:5]}")
    print("  foreign_key_check: clean (0 rows)")

    # R-M7 biconditional invariant (unchanged by this migration; assert it held)
    g = scalar("SELECT count(*) FROM kit_mapping WHERE grade='GAPPED'")
    md = scalar("SELECT count(*) FROM kit_mapping WHERE terminal_state='MAPPED_DOCKET'")
    assert_eq("R-M7 GAPPED==MAPPED_DOCKET", (g, md), (86, 86))

    # kit_mapping still 574 (no rows added/removed — errata are in-row edits)
    assert_eq("kit_mapping rows", scalar("SELECT count(*) FROM kit_mapping"), 574)

    conn.execute("COMMIT")
    print("\n=== COMMIT OK ===")
except Exception:
    conn.execute("ROLLBACK")
    conn.close()
    raise

conn.close()

# ---- post-commit: compute post-md5 + stamp it into schema_meta -------------
post_md5 = md5_of(DB)
print(f"\n[post] corpus.db md5 = {post_md5}")
conn2 = sqlite3.connect(DB)
c2 = conn2.cursor()
c2.execute("UPDATE corpus_schema_meta SET note = note || ' [post-md5=' || ? || ']' "
           "WHERE version='v1.1-verified' AND applied_utc=?", (post_md5, UTC))
conn2.commit()
# read back the md5-stamped v1.1 note tail for confirmation
c2.execute("SELECT substr(note, -60) FROM corpus_schema_meta WHERE version='v1.1-verified' AND applied_utc=?", (UTC,))
print(f"[post] v1.1 meta note tail: ...{c2.fetchone()[0]}")
conn2.close()

# emit machine-readable report tail
print("\n=== REPORT (per-item) ===")
print(json.dumps(report, indent=2, default=str))
print(f"\nPRE_MD5={pre_md5}")
print(f"POST_MD5={post_md5}")
