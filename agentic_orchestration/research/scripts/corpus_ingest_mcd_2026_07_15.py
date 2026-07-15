#!/usr/bin/env python3
"""
corpus_ingest_mcd_2026_07_15.py

Ingest + lattice-key the Minecraft Dungeons (MCD) Mode-B crawl tranche into corpus.db.
Matt INGEST ruling 2026-07-15 ("Regardless, ingest MCD"). legolas crawled; gandalf verified;
elrond OWNS the DB write (this script). Data-curation work in the elrond seam.

READ FIRST:
  - agentic_orchestration/research/knowledge/mcd-pull-mechanic/2026-07-15-mcd-mode-b-crawl-tranche1.md
      (the tranche: Section A melee / B ranged / C artifacts; TABLES ARE GROUND TRUTH)
  - agentic_orchestration/research/knowledge/mcd-pull-mechanic/2026-07-15-mcd-probe-pull-mechanic-census.md
      (Mode-A probe that won INGEST: 3 grains — classless gear-only, unconstrained pull, third-pole curve)
  - prior elrond logs (ingest 07-12, cell-key 07-13, curation a5 07-14, recrawl 07-15)

SOURCE OF TRUTH: the tranche markdown TABLES (parsed directly here; source-anchored + reversible).
  VERIFIED COUNT (gandalf, grep-proven): the tables hold 122 kit rows (28 melee + 30 bows +
  20 crossbows + 44 artifacts). legolas's census summary said 119 (undercounted bows by 2,
  crossbows by 1). We ingest from the TABLES. True pre-drop count = 122.

TWO BOUNDARY DROPS (elrond ruling, fetch-resolved 2026-07-15 against minecraft.wiki):
  - mcd-void-bow        : rarity Common/Rare = BASE-family weapon; unique variant = Call of the Void.
                          Violates the unique-weapon-grain ruling exactly like Wind Bow (excluded;
                          its uniques Burst Gale Bow + Echo of the Valley kept). DROP. (Call of the
                          Void, mcd-call-of-the-void, is unique-rarity -> KEPT.)
  - mcd-twisting-vine-bow: rarity Common/Rare = BASE variant; unique variant = Weeping Vine Bow
                          (mcd-weeping-vine-bow, already in tranche, KEPT). legolas self-flagged the
                          unconfirmed intrinsic; fetch resolves it to base-rarity + Poison-trail
                          intrinsic. Same precedent as Void Bow / Wind Bow. DROP.
  => ingested kit rows = 122 - 2 = 120.

ANNOTATIONS that ride EVERY mcd- row (queryable):
  - canon_tier = 'shallow'          (first-class column; == depth=shallow)
  - flags carries 'depth:shallow' + 'architecture:notable' + (for the 6) 'pull_pending_vocab:true'
  - game='mcd', corpus_bucket='mcd', source='canon', provenance_tag='mcd-mode-b-2026-07-15',
    source_date='2026-07-15', source_urls = the per-item minecraft.wiki URL.
  - prov='legolas-mode-b;elrond-curated'

pull_pending_vocab GATE (frozen-basis; Edition-I lattice FROZEN):
  The 6 pull-primary kits (mcd-hammer-of-gravity, mcd-encrusted-anchor, mcd-echo-of-the-valley,
  mcd-burst-gale-bow, mcd-imploding-crossbow, mcd-voidcaller) are INWARD force. `pull` is NOT a
  function level in Edition-I. They must NOT be force-keyed function=knockback (inward != outward).
  They land UNRESOLVED (unresolved=1, NO canon_engine_key row, pull flag queryable) = the existing
  unmapped-pending-curation mechanism, until the Edition-II vocab pass elevates `pull` to a function.

KEYING PHASE (Gate-A / core-7, same pass):
  MCD rows lack canon_probe_facts (survivors had 10 families each). So MCD keying is a fresh
  derivation from mech_note prose + the prefix coords assigned at ingest, REUSING the survivors'
  serialize_cell_key + enums (imported from corpus_cell_key_materialize_2026_07_13). Weapons with
  clear mech_notes are keyable; thin category-page artifacts are not -> those land unresolved too.
  The 6 pull kits stay unkeyed regardless. Low-confidence -> unresolved (existing mechanism).

IDEMPOTENT: additive. mcd- rows upserted from the static manifest each run; the 469 clean survivor
  cell_keys are NEVER touched (hard-constraint SHA proven in the log). Backup taken by caller
  (corpus.db.pre-mcd-2026-07-15-backup).

D6 rebuild slot: runs AFTER ingest_recrawl_and_curation_2026_07_15.py.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

# reuse the survivors' EXACT serialization + activation/dependency derivation + enums
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_cell_key_materialize_2026_07_13 import (  # noqa: E402
    serialize_cell_key,
    derive_activation,
    derive_dependency,
    ECONOMY_MODEL_PURE_ENUM,
    CTRL_FUNCTION_ENUM,
)

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # -> reincarnated-collaboration
DB = ROOT / "agentic_orchestration/research/curated/corpus.db"
TRANCHE = (ROOT / "agentic_orchestration/research/knowledge/mcd-pull-mechanic"
           / "2026-07-15-mcd-mode-b-crawl-tranche1.md")

PROVENANCE_TAG = "mcd-mode-b-2026-07-15"
SOURCE_DATE = "2026-07-15"
ERAS = "mcd-launch-2020;mcd-dlc-2020-2022"

# The two base-rarity DROPs (fetch-resolved).
DROP = {"mcd-void-bow", "mcd-twisting-vine-bow"}

# The 6 pull-primary kits (pull_pending_vocab:true) — UNRESOLVED, never keyed in Edition-I.
PULL_KITS = {
    "mcd-hammer-of-gravity", "mcd-encrusted-anchor", "mcd-echo-of-the-valley",
    "mcd-burst-gale-bow", "mcd-imploding-crossbow", "mcd-voidcaller",
}


# --------------------------------------------------------------------------------------
# PARSE the tranche tables (source-anchored ground truth).
# --------------------------------------------------------------------------------------
def parse_tranche():
    """Return list of dicts, one per kit row, with section + all table columns."""
    text = TRANCHE.read_text()
    rows = []
    section = None       # 'melee' | 'bow' | 'crossbow' | 'artifact'
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## SECTION A"):
            section = "melee"; continue
        if s.startswith("### Bows"):
            section = "bow"; continue
        if s.startswith("### Crossbows"):
            section = "crossbow"; continue
        if s.startswith("## SECTION C"):
            section = "artifact"; continue
        if s.startswith("## PULL-PRIMARY") or s.startswith("## BOUNDARY") or s.startswith("## SOURCE") or s.startswith("## CRAWL"):
            section = None; continue
        if section is None:
            continue
        if not s.startswith("| mcd-"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        # weapon tables: kit_id | display | family | mech_note | pull_mechanic | pull_pending_vocab | url | depth | arch
        # artifact table: kit_id | display | artifact_type | mech_note | pull_mechanic | pull_pending_vocab | url | depth | arch
        if len(cells) < 9:
            continue
        rows.append({
            "kit_id": cells[0],
            "display_name": cells[1],
            "family": cells[2],
            "mech_note": cells[3],
            "pull_mechanic": cells[4],
            "pull_pending_vocab": cells[5].lower() == "true",
            "source_url": cells[6],
            "depth": cells[7],
            "architecture": cells[8],
            "section": section,
        })
    return rows


# --------------------------------------------------------------------------------------
# PREFIX-COORD derivation (canon_corpus) — from mech_note stats + family. Steward rules.
# Returns dict of the 6 prefix coords; None = genuinely-absent (stays NULL, never guessed).
# --------------------------------------------------------------------------------------
SPEED_RE = re.compile(r"speed\s+([0-9]+(?:\.[0-9]+)?)")


def _speed(note):
    m = SPEED_RE.search(note.lower())
    return float(m.group(1)) if m else None


def derive_prefix(row):
    note = row["mech_note"].lower()
    sec = row["section"]
    coords = {"attr_val": None, "range_val": None, "tempo_val": None,
              "amp_val": None, "proxy_val": None, "commit_val": None}

    # range_val
    if sec == "melee":
        coords["range_val"] = "melee"
    elif sec in ("bow", "crossbow"):
        coords["range_val"] = "ranged"
    # artifacts: range set per-row in ARTIFACT_KEYS override; leave None here.

    # tempo_val from attack speed stat (MCD 'speed' is attacks/sec-ish; higher=faster)
    sp = _speed(note)
    if sp is not None:
        if sp >= 5:
            coords["tempo_val"] = "high"
        elif sp >= 2:
            coords["tempo_val"] = "med"
        else:
            coords["tempo_val"] = "low"

    # amp_val: charged/burst/multiplier -> spiky; steady combo/continuous -> flat
    if any(t in note for t in ["charge multiplier", "charged attack", "supercharge",
                                "charged arrows", "charged shot", "when charged", "wind-up",
                                "roll to charge", "roll charge"]):
        coords["amp_val"] = "spiky"
    elif sec in ("melee", "bow", "crossbow"):
        coords["amp_val"] = "flat"

    # proxy_val: summons/allies -> light (single/few) or heavy; else solo
    if any(t in note for t in ["summons iron golem", "summons wolf", "summons llama",
                                "summons bees", "summons a single", "summons 3", "summon"]):
        coords["proxy_val"] = "light"
    else:
        coords["proxy_val"] = "solo"

    # commit_val: charged/wind-up -> wind-up; continuous-hold -> channel; else instant
    if any(t in note for t in ["continuous-attack", "hold attack", "holds attack",
                                "sustained rapid", "sustained fire", "channel"]):
        coords["commit_val"] = "channel"
    elif any(t in note for t in ["charge multiplier", "when charged", "charged arrows",
                                  "wind-up", "wind up", "roll to charge", "roll charge",
                                  "charge before firing", "charged shot"]):
        coords["commit_val"] = "wind-up"
    elif sec in ("melee", "bow", "crossbow"):
        coords["commit_val"] = "instant"

    return coords


# --------------------------------------------------------------------------------------
# ENGINE-KEY coord derivation (canon_engine_key). Steward rules over mech_note + family.
# Returns dict OR None if the row is too thin to key confidently (-> unresolved).
# --------------------------------------------------------------------------------------
# Layer-1 control tells (element-neutral CC). DoT/elemental = damage (L1' 2026-07-15).
CC_STUN = ["stuns mobs", "stunned effect", "stun ", "stuns ", "shockwave"]
CC_HARDSTOP = ["freeze on impact", "freeze/slow", "immobilizes", "entangles", "root ", "ice blocks"]
CC_TAUNT = []
CC_KNOCKBACK_OUT = ["pushes enemies away", "pushback", "knockback", "punch", "launches",
                    "airborne", "pushes back"]  # OUTWARD only reaches here (6 pull kits excluded)
DEFENSIVE = {
    "mcd-art-iron-hide-amulet": "mitigate",
    "mcd-art-totem-of-shielding": "absorb",
    "mcd-art-ghost-cloak": "evade",
    "mcd-art-shadow-shifter": "evade",
}


def derive_engine_key(row, prefix):
    """Return (ek_dict, confidence_note) or (None, reason) if too thin to key."""
    note = row["mech_note"].lower()
    sec = row["section"]
    kid = row["kit_id"]

    # geometry: MCD delivery is coarse. melee weapons = melee_strike (single-target swing) unless
    # AoE-splash tell; bows/crossbows = single_target unless multishot/ricochet/scatter. Artifacts
    # are too varied + category-thin to key geometry deterministically -> thin artifacts unresolved.
    geometry = None
    if sec == "melee":
        if any(t in note for t in ["area 14", "area 9.2", "360-degree", "aoe", "area damage",
                                    "splash", "spin attack", "180-degree"]):
            geometry = "cone"       # frontal/spin AoE swing family
        else:
            geometry = "melee_strike"
    elif sec in ("bow", "crossbow"):
        if any(t in note for t in ["fires 3", "fires 5", "multishot", "multiple arrows",
                                    "two arrows", "two enemies", "double projectile", "scatter"]):
            geometry = "multi_projectile"
        elif any(t in note for t in ["ricochet", "bounce", "bounces", "chain reaction",
                                      "piercing", "pierce"]):
            geometry = "chain"
        else:
            geometry = "single_target"

    # ctrl_treatment + function (L1' rule: DoT/elemental damage-signature => damage, not control)
    if any(t in note for t in CC_HARDSTOP):
        ctrl_treatment, ctrl_function = "control", "hard-stop"
    elif any(t in note for t in CC_STUN):
        ctrl_treatment, ctrl_function = "control", "stun"
    elif any(t in note for t in ["charms", "enrage", "wild rage"]):
        ctrl_treatment, ctrl_function = "control", "fear"   # charm/enrage = mind-control CC family
    elif any(t in note for t in ["pushes enemies away", "outward push", "outward force", "punch i"]):
        ctrl_treatment, ctrl_function = "control", "knockback"
    else:
        ctrl_treatment, ctrl_function = "damage", "none"

    # def_bin: MCD weapons/utility are pure-offense/utility -> NULL (like the negatives), except
    # the explicit defensive artifacts.
    def_bin = DEFENSIVE.get(kid)  # None for the vast majority (honest NULL, not glass-guess)

    # economy_model: weapon intrinsics carry NO resource -> free; artifacts run on cooldown.
    if sec in ("melee", "bow", "crossbow"):
        economy_model = "free"
    else:
        economy_model = "cooldown"

    # mob_policy_while_casting: MCD has no cast-lock stationary tell in the source -> NULL (passive),
    # matching the negatives' honest-NULL treatment for absent movement facts.
    mob_policy = None

    # activation / dependency via the survivors' exact derivation over mech_note.
    activation = derive_activation(row["mech_note"], None)
    dependency = derive_dependency(row["mech_note"])

    ek = {
        "geometry_value": geometry,
        "geometry_rule_fired": "elrond-mcd-2026-07-15-family-geometry",
        "ctrl_treatment": ctrl_treatment,
        "ctrl_function": ctrl_function,
        "def_bin": def_bin,
        "economy_model": economy_model,
        "mob_policy_while_casting": mob_policy,
        "delivery_value": ("melee" if sec == "melee" else "at-target"),
        "activation_val": activation,
        "dependency_val": dependency,
    }
    return ek, "keyed"


# --------------------------------------------------------------------------------------
# KEYABILITY gate: is a row confident enough to key? Thin category-page artifacts are not.
# --------------------------------------------------------------------------------------
# Artifacts whose mech_note is a category-page one-liner AND whose engine coords can't be
# deterministically assigned. We key artifacts that DO carry a clear CC/summon/defensive
# signal (they map cleanly); the rest land unresolved (thin-note flag) per the tranche caveat.
KEYABLE_ARTIFACTS = {
    # clear control artifacts (stun/freeze/root/charm) — Layer-1 function assignable
    "mcd-art-corrupted-seeds", "mcd-art-fishing-rod", "mcd-art-ice-wand",
    "mcd-art-shock-powder", "mcd-art-love-medallion", "mcd-art-wind-horn",
    # clear defensive artifacts
    "mcd-art-iron-hide-amulet", "mcd-art-totem-of-shielding", "mcd-art-ghost-cloak",
    "mcd-art-shadow-shifter",
    # clear summon artifacts (proxy signal is the whole kit)
    "mcd-art-buzzy-nest", "mcd-art-enchanted-grass", "mcd-art-golem-kit",
    "mcd-art-soul-lantern", "mcd-art-tasty-bone", "mcd-art-vexing-chant",
    "mcd-art-wonderful-wheat",
    # clear damage artifacts with a definite delivery
    "mcd-art-corrupted-beacon", "mcd-art-harvester", "mcd-art-lightning-rod",
    "mcd-art-scatter-mines", "mcd-art-blast-fungus", "mcd-art-spinblade",
    "mcd-art-eye-of-the-guardian",
}


def is_keyable(row):
    """Return (keyable: bool, reason)."""
    kid = row["kit_id"]
    if kid in PULL_KITS:
        return False, "pull_pending_vocab"      # frozen-basis: inward force, no Edition-I function
    sec = row["section"]
    if sec in ("melee", "bow", "crossbow"):
        # all weapons carry a real mech_note -> keyable
        return True, "keyed"
    # artifacts: only the ones with a clear signal
    if kid in KEYABLE_ARTIFACTS:
        return True, "keyed"
    return False, "thin-artifact-note"           # category-page one-liner -> unresolved


# Per-row range/tempo for KEYABLE artifacts (derive_prefix leaves artifact range NULL).
# range: where the effect lands relative to the player. tempo: artifacts fire on cooldown -> low.
ARTIFACT_RANGE = {
    "mcd-art-corrupted-beacon": "ranged", "mcd-art-harvester": "melee",
    "mcd-art-lightning-rod": "ranged", "mcd-art-scatter-mines": "mid",
    "mcd-art-blast-fungus": "ranged", "mcd-art-spinblade": "mid",
    "mcd-art-eye-of-the-guardian": "ranged", "mcd-art-corrupted-seeds": "mid",
    "mcd-art-fishing-rod": "ranged", "mcd-art-ice-wand": "melee",
    "mcd-art-shock-powder": "melee", "mcd-art-love-medallion": "mid",
    "mcd-art-wind-horn": "melee", "mcd-art-buzzy-nest": "melee",
    "mcd-art-enchanted-grass": "melee", "mcd-art-golem-kit": "melee",
    "mcd-art-soul-lantern": "melee", "mcd-art-tasty-bone": "melee",
    "mcd-art-vexing-chant": "melee", "mcd-art-wonderful-wheat": "melee",
    "mcd-art-iron-hide-amulet": "melee", "mcd-art-totem-of-shielding": "melee",
    "mcd-art-ghost-cloak": "melee", "mcd-art-shadow-shifter": "melee",
}


# --------------------------------------------------------------------------------------
# DB WRITE
# --------------------------------------------------------------------------------------
def build_flags(row, keyable, reason):
    tokens = ["depth:shallow", "architecture:notable"]
    if row["pull_pending_vocab"]:
        tokens.append("pull_pending_vocab:true")
    if not keyable:
        tokens.append(f"unmapped_pending_curation:{reason}")
    return json.dumps(tokens)


def upsert_corpus(conn, row, prefix, keyable, reason, key_completeness):
    unresolved = 0 if keyable else 1
    # range for artifacts comes from the override table
    range_val = prefix["range_val"]
    if row["section"] == "artifact" and row["kit_id"] in ARTIFACT_RANGE:
        range_val = ARTIFACT_RANGE[row["kit_id"]]
    tempo_val = prefix["tempo_val"]
    if row["section"] == "artifact" and tempo_val is None and keyable:
        tempo_val = "low"   # artifacts fire on cooldown
    conf = 0.75 if keyable else None   # steward-derived from prose, not mobile-harvest avg
    conn.execute("""
        INSERT INTO canon_corpus
          (kit_id, folk_name, game, corpus_bucket, tier, canon_tier, eras, negative,
           source, is_system, unresolved, mint, dossier_owed,
           provenance_tag, source_date,
           attr_val, range_val, tempo_val, amp_val, proxy_val, commit_val,
           prefix_conf_provenance, avg_conf, key_completeness,
           mech_note, flags, prov, source_urls)
        VALUES (?,?,?,?,?,?,?,?, ?,?,?,?,?, ?,?, ?,?,?,?,?,?, ?,?,?, ?,?,?,?)
        ON CONFLICT(kit_id) DO UPDATE SET
           folk_name=excluded.folk_name, game=excluded.game, corpus_bucket=excluded.corpus_bucket,
           canon_tier=excluded.canon_tier, eras=excluded.eras,
           source=excluded.source, unresolved=excluded.unresolved,
           provenance_tag=excluded.provenance_tag, source_date=excluded.source_date,
           attr_val=excluded.attr_val, range_val=excluded.range_val, tempo_val=excluded.tempo_val,
           amp_val=excluded.amp_val, proxy_val=excluded.proxy_val, commit_val=excluded.commit_val,
           prefix_conf_provenance=excluded.prefix_conf_provenance, avg_conf=excluded.avg_conf,
           key_completeness=excluded.key_completeness,
           mech_note=excluded.mech_note, flags=excluded.flags, prov=excluded.prov,
           source_urls=excluded.source_urls
    """, (
        row["kit_id"], row["display_name"], "mcd", "mcd", None, "shallow", ERAS, 0,
        "canon", 0, unresolved, 0, 0,
        PROVENANCE_TAG, SOURCE_DATE,
        prefix["attr_val"], range_val, tempo_val, prefix["amp_val"],
        prefix["proxy_val"], prefix["commit_val"],
        "mcd-mode-b-steward-derived", conf, key_completeness,
        row["mech_note"], build_flags(row, keyable, reason), "legolas-mode-b;elrond-curated",
        row["source_url"],
    ))


def upsert_engine_key(conn, row, ek):
    provenance = json.dumps({"src": "elrond-mcd-2026-07-15",
                             "basis": "steward-derived-from-mech_note-prose",
                             "note": "MCD lacks canon_probe_facts; coords derived from tranche prose."})
    conn.execute("""
        INSERT INTO canon_engine_key
          (kit_id, geometry_value, geometry_rule_fired, geometry_conf,
           ctrl_treatment, ctrl_function, def_bin, economy_model,
           mob_policy_while_casting, delivery_value, activation_val, dependency_val,
           row_class, flags, provenance_json, raw_json)
        VALUES (?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?)
        ON CONFLICT(kit_id) DO UPDATE SET
           geometry_value=excluded.geometry_value, geometry_rule_fired=excluded.geometry_rule_fired,
           ctrl_treatment=excluded.ctrl_treatment, ctrl_function=excluded.ctrl_function,
           def_bin=excluded.def_bin, economy_model=excluded.economy_model,
           mob_policy_while_casting=excluded.mob_policy_while_casting,
           delivery_value=excluded.delivery_value, activation_val=excluded.activation_val,
           dependency_val=excluded.dependency_val, provenance_json=excluded.provenance_json,
           raw_json=excluded.raw_json
    """, (
        row["kit_id"], ek["geometry_value"], ek["geometry_rule_fired"], 0.7,
        ek["ctrl_treatment"], ek["ctrl_function"], ek["def_bin"], ek["economy_model"],
        ek["mob_policy_while_casting"], ek["delivery_value"], ek["activation_val"],
        ek["dependency_val"],
        "combat-kit", json.dumps(["mcd-mode-b", "depth:shallow"]), provenance,
        json.dumps({k: row[k] for k in ("kit_id", "display_name", "family", "mech_note",
                                         "source_url", "section")}),
    ))


def build_cell_key(conn, kit_id):
    """Serialize the 14-field cell_key via the survivors' EXACT serializer (cross-table join)."""
    r = conn.execute("""
        SELECT k.mob_policy_while_casting, k.delivery_value, k.geometry_value,
               k.ctrl_treatment, k.ctrl_function, k.def_bin, k.economy_model,
               k.activation_val, k.dependency_val,
               cc.amp_val, cc.proxy_val, cc.range_val, cc.tempo_val, cc.commit_val
        FROM canon_engine_key k JOIN canon_corpus cc ON cc.kit_id=k.kit_id
        WHERE k.kit_id=?
    """, (kit_id,)).fetchone()
    ck = serialize_cell_key(r)
    conn.execute("UPDATE canon_engine_key SET cell_key=? WHERE kit_id=?", (ck, kit_id))
    return ck


def main():
    if not DB.exists():
        sys.exit(f"corpus.db not found at {DB}")
    parsed = parse_tranche()

    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    before = conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    # Baseline = the NON-mcd combat-kit survivor keys. Same predicate as surv_after so the
    # invariant holds on first run AND on idempotent re-runs (when mcd rows already exist).
    surv_before = conn.execute("""
        SELECT k.kit_id||'|'||COALESCE(k.cell_key,'')
        FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id
        WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' ORDER BY k.kit_id
    """).fetchall()

    ingested, dropped, keyed, unresolved_rows, pending_vocab = 0, [], [], [], []
    for row in parsed:
        if row["kit_id"] in DROP:
            dropped.append(row["kit_id"])
            continue
        prefix = derive_prefix(row)
        keyable, reason = is_keyable(row)
        # key_completeness: count of the 6 prefix coords that are non-NULL (a real completeness signal)
        kc = sum(1 for v in prefix.values() if v is not None)
        upsert_corpus(conn, row, prefix, keyable, reason, kc)
        ingested += 1
        if keyable:
            ek, _ = derive_engine_key(row, prefix)
            # enum guards (defensive)
            assert ek["ctrl_function"] in CTRL_FUNCTION_ENUM, f"{row['kit_id']} bad fn {ek['ctrl_function']}"
            for part in ek["economy_model"].split("+"):
                assert part in ECONOMY_MODEL_PURE_ENUM, f"{row['kit_id']} bad econ {part}"
            upsert_engine_key(conn, row, ek)
            build_cell_key(conn, row["kit_id"])
            keyed.append(row["kit_id"])
        else:
            # unresolved: NO engine-key row (stays out of the combat denominator + displacement join)
            if reason == "pull_pending_vocab":
                pending_vocab.append(row["kit_id"])
            else:
                unresolved_rows.append(row["kit_id"])
    conn.commit()

    # ---- hard-constraint: survivors untouched ----
    surv_after = conn.execute("""
        SELECT k.kit_id||'|'||COALESCE(k.cell_key,'')
        FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id
        WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' ORDER BY k.kit_id
    """).fetchall()
    # pre-batch had no mcd rows -> the non-mcd predicate == the full pre-batch survivor set.
    assert list(surv_after) == list(surv_before), "SURVIVOR KEYS CHANGED — abort"

    after = conn.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    integ = conn.execute("PRAGMA integrity_check").fetchone()[0]

    # schema_meta marker (idempotent)
    conn.execute("DELETE FROM corpus_schema_meta WHERE version='mcd-ingest-2026-07-15'")
    conn.execute("""
        INSERT INTO corpus_schema_meta (version, applied_utc, note)
        VALUES ('mcd-ingest-2026-07-15', '2026-07-15T00:00:00Z', ?)
    """, (
        f"MCD Mode-B ingest (elrond). {ingested} kit rows ingested (mcd- prefix), "
        f"{len(dropped)} dropped (Void Bow + Twisting Vine Bow = base-rarity, unique-weapon-grain "
        f"ruling, fetch-resolved). Annotations depth:shallow (canon_tier='shallow') + "
        f"architecture:notable ride every row (flags). {len(keyed)} keyed (canon_engine_key "
        f"combat-kit + cell_key); {len(unresolved_rows)} unresolved (thin-artifact-note); "
        f"{len(pending_vocab)} pull_pending_vocab (frozen-basis, inward force, NO Edition-I "
        f"function=knockback, NO engine-key row). Additive; 469 survivor cell_keys byte-identical. "
        f"MCD lacks canon_probe_facts; coords steward-derived from tranche prose. Rebuild = base "
        f"ingest chain + this.",
    ))
    conn.commit()
    conn.close()

    print("== MCD INGEST ==")
    print(f"  canon_corpus: {before} -> {after}  (+{after-before})")
    print(f"  ingested: {ingested} | dropped: {len(dropped)} {dropped}")
    print(f"  keyed (engine-key + cell_key): {len(keyed)}")
    print(f"  unresolved (thin-artifact-note): {len(unresolved_rows)}")
    print(f"  pull_pending_vocab (unkeyed, frozen-basis): {len(pending_vocab)} {sorted(pending_vocab)}")
    print(f"  integrity: {integ}")
    print(f"  survivors untouched: YES (asserted)")


if __name__ == "__main__":
    main()
