#!/usr/bin/env python3
"""
corpus_curation_a5_2026_07_14.py

Curation batch A.5 (elrond) — the DATA SNAPSHOT the atlas-derivation pipeline runs against.
Matt-ratified binding (d) of the 2026-07-13 direction analysis; re-confirmed 2026-07-14
under the atlas-derivation charter. Dispatch: autonomous run 2026-07-14 (KR/Matt).

READ FIRST:
  - gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md  §A.2 / §A.3 / §A.5
  - canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md  §5 Stage 0
  - the two prior elrond logs (ingest 07-12, cell-key 07-13) in research/curated/

FIVE ITEMS (all ADDITIVE; no destructive migration; survivor keys untouched):

  1. mech_note 140-char truncation repair.
       HYPOTHESIS (dispatch): raw_json carries verbatim mech_note -> local UPDATE.
       FINDING: raw_json in canon_engine_key has NO mech_note field, AND the v3 CSV
       (rdr-kit-atlas-v3.csv) is ITSELF truncated at 140. The UNtruncated source is the
       legolas megaprobe facts JSONL (mechanics_notes up to 739 chars; negatives use a
       'mech_note' field). Path taken = LOCAL RE-EXTRACTION from the committed megaprobe
       facts JSONL (no external re-crawl). GROW-ONLY (never shrink; a shorter facts note =
       whitespace/em-dash normalization, not real data -> skip).

  2. d2-sacrifice fill-or-quarantine.
       FINDING: d2-sacrifice IS negative=1 (a mint kit) and HAS a real postmortem in the
       mint dossier (mint-dossiers-reexpressed.jsonl). Decision rule -> FILL: set mech_note
       from the dossier, then re-key it by the SAME negative-keying rules as item 3. It is
       excluded from the combat denominator by the negative=0 filter (v_combat_kits amended),
       so the junk-key-in-denominator problem is resolved without a quarantine flag.

  3. Re-key the 37 unkeyed negatives (+ d2-sacrifice = 38 total, deduped) through the
       Layer-3 keying pipeline. Negative facts rows are SPARSE (delivery + footprint +
       postmortem only; NO control/defense/economy/movement/full prefix dicts). Recoverable
       coords land; genuinely-unrecoverable coords are LEFT NULL (passive category per
       charter §5 Stage 0) — NEVER guessed. Recoverability matrix (verified):
         #2  delivery_value          <- facts.delivery.value              (recoverable)
         #3  amp_val                 <- canon_corpus (atlas decode)       (recoverable)
         #4  geometry_value          <- delivery+footprint AMBIGUOUS for ALL 37 -> NULL
         #8  proxy_val               <- canon_corpus                      (recoverable)
         #9  range_val               <- canon_corpus                      (recoverable)
         #10 tempo_val               <- canon_corpus                      (recoverable)
         #11 commit_val              <- canon_corpus                      (recoverable)
         #12 activation_val          <- (repaired) mech_note tells        (recoverable)
         #13 dependency_val          <- (repaired) mech_note tells        (recoverable)
         #1  mob_policy_while_casting <- facts.movement ABSENT            -> NULL (passive)
         #5a ctrl_treatment          <- facts.control ABSENT             -> NULL (passive)
         #5b ctrl_function           <- facts.control ABSENT             -> NULL (passive)
         #6  def_bin                 <- facts.defense ABSENT             -> NULL (passive)
         #7  economy_model           <- facts.economy ABSENT             -> NULL (passive)
       They stay negative=1 (supplementary-only; NEVER shape axes).
       row_class: 'combat-kit' for kit-negatives; 'system-record' for vs-golden-egg-scaling
       (§A.2 pattern 11 — system-level evidence, NOT a kit).

  4. Resolve the 5 no-rule-matched pipeline TODOs (d2-impale-zon, gd-reap-spirit,
       d2-grim-ward-barb, d2-leap-attack-barb, hot-blood-catcher). All carry real
       postmortems (item-1 confirmed) -> they are genre-negatives, keyed by item 3 (dedup
       natural: all 5 are in the 37).

  5. Add death_class provenance (CHECK-constrained enum) per the §A.2 pattern->class map.
       Ambiguous pattern-assignment -> NULL + flags note (gandalf adjudicates), never invented.

  cell_key derivation for the negatives REUSES the exact functions from
  corpus_cell_key_materialize_2026_07_13.py (ctrl_function / economy_model / activation /
  dependency / slot / serialize) — imported, not re-implemented, so the negatives key by the
  identical rules as the survivors.

IDEMPOTENT: additive columns created IF NOT present; negative engine-key rows upserted;
death_class recomputed from the static map each run; survivor rows NEVER touched.
Backup discipline: caller takes corpus.db.pre-A5-*-backup before running (done).

D6 rebuild slot: runs AFTER corpus_cell_key_materialize_2026_07_13.py.
"""

import json
import sqlite3
import sys
from pathlib import Path

# Reuse the survivors' exact keying functions (identical rules).
import importlib.util

BASE = Path("/Users/admin/Games/reincarnated-collaboration")
SCRIPTS = BASE / "agentic_orchestration/research/scripts"
DB = BASE / "agentic_orchestration/research/curated/corpus.db"
MEGAPROBE = BASE / "agentic_orchestration/legolas/research/megaprobe-2026-07-12"
ENGINE_KEY = BASE / "agentic_orchestration/gandalf/views/engine-key/corpus-engine-key-v1.jsonl"

# ---- import the materialize module for its keying functions ----
_spec = importlib.util.spec_from_file_location(
    "cellkey_mat", SCRIPTS / "corpus_cell_key_materialize_2026_07_13.py"
)
_ck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ck)

derive_ctrl_function = _ck.derive_ctrl_function
derive_economy = _ck.derive_economy
derive_activation = _ck.derive_activation
derive_dependency = _ck.derive_dependency
slot = _ck.slot
CELL_KEY_ORDER = _ck.CELL_KEY_ORDER


# ======================================================================================
# §A.2 pattern -> death_class map (verbatim from the analysis).
# death_class enum (CHECK-constrained):
#   extrinsic-tuning / extrinsic-itemization / extrinsic-split-scaling /
#   extrinsic-no-lever / extrinsic-content-mix / intrinsic-red / system-evidence
#
# Assignment rule when a kit carries MULTIPLE §A.2 tags (a corpse can die of two things):
#   The §A.5-5 instruction is "tag per the §A.2 pattern->death-class mapping (each of the 12
#   patterns names its class + its member kits)." Each pattern that HAS an explicit curation
#   `death=` line contributes that class. Where a kit's dominant classification is
#   UNAMBIGUOUS in §A.2, we assign it. Where §A.2 leaves the kit genuinely split between two
#   incompatible classes with NO dominant one, we assign NULL + a flags note for gandalf.
#
# Patterns WITHOUT a `death=` curation line (10, 4-carveout) do NOT emit a class by
# themselves; a kit that is ONLY in such a pattern and no death= pattern -> NULL + note.
# ======================================================================================

# Explicit per-kit death_class, transcribed from §A.2. Value None => leave NULL + flag.
# Multi-tag kits are resolved to their DOMINANT death= class per §A.2 prose; the ambiguous
# ones are set to None with a documented reason (surfaced to gandalf).
DEATH_CLASS = {
    # -- Pattern 1 TUNING-STARVATION -> extrinsic-tuning (§A.2-1: "tag death=extrinsic-tuning")
    "d2-inferno-sorc":        "extrinsic-tuning",
    "d2-blade-sin":           "extrinsic-tuning",
    "tl2-arc-beam":           "extrinsic-tuning",   # analysis 'tl-arc-beam' == corpus 'tl2-arc-beam'
    "d3-shield-bash":         "extrinsic-tuning",
    "poe2-wall-of-shields":   "extrinsic-tuning",   # also pattern 12 (port-context); tuning is the death= line, but dual w/ port -> see note below
    "poe2-chronomancer-01":   "extrinsic-tuning",   # also pattern 12; dual -> note

    # -- Pattern 2 ITEMIZATION-ORPHAN -> extrinsic-itemization (§A.2-2: "death=extrinsic-itemization")
    "d3-firebomb":            "extrinsic-itemization",
    "d3-wave-of-force":       "extrinsic-itemization",
    "d3-spectral-blade":      None,  # dual: pattern 2 (itemization) + pattern 10 (sibling-shadowed, no class) -> itemization dominant per §A.2-2 membership; BUT §A.2-10 also lists it. Ambiguous -> gandalf. (see note)
    "d4-wind-shear":          "extrinsic-itemization",
    "d4-kick":                "extrinsic-itemization",
    "d4-blade-shift":         None,  # dual: pattern 2 (itemization) + pattern 4 (movement-verb-pretense = intrinsic-red carveout). Two INCOMPATIBLE classes (extrinsic vs intrinsic) -> gandalf.
    "le-shield-bash-le":      "extrinsic-itemization",

    # -- Pattern 3 DISPLACED-DAMAGE MOVEMENT FUSION -> intrinsic-red (RED LAW co-location)
    "d2-blaze-sorc":          "intrinsic-red",
    "poe1-charged-dash":      "intrinsic-red",   # also patterns 4 & 5 (dual/dual); pattern 3 red is dominant (co-location law) — §A.2-3 flagship

    # -- Pattern 4 MOVEMENT-VERB-AS-PRETENSE -> intrinsic-red UNLESS instant+spammable
    "d2-leap-attack-barb":    "intrinsic-red",   # §A.2-4: "the movement verb was the payload and the payload never paid" — committal, dies -> red

    # -- Pattern 5 SPLIT-SCALING FUSION -> extrinsic-split-scaling (ambers); poe1-reaper stays red via 6
    "d2-golemancer":          "extrinsic-split-scaling",
    "gd-reap-spirit":         "extrinsic-split-scaling",
    "le-soul-feast":          "extrinsic-split-scaling",
    # poe1-reaper below (pattern 6 red)

    # -- Pattern 6 ANTI-SYNERGY LOOP -> intrinsic-red (RED LAW no-anti-synergy)
    "poe1-reaper":            "intrinsic-red",
    "vs-gatti-amari":         "intrinsic-red",

    # -- Pattern 7 STOCHASTIC-WITHOUT-LEVER -> extrinsic-no-lever
    "poe1-wild-strike":       "extrinsic-no-lever",
    "le-tempest-strike":      "extrinsic-no-lever",
    "gd-stun-jacks":          "extrinsic-no-lever",  # §A.2-7 "partial tag" — but no-lever is its death= line

    # -- Pattern 8 TIMING-TAX OVERPRICED -> structural PRICING LAW (no death= class in §A.2)
    #    Members: poe2-perfect-strike-01, tq-calculated-strike, d2-impale-zon.
    #    §A.2-8 assigns NO death= line (it is a pricing law, not a provenance class).
    #    -> these get their class ONLY if they ALSO sit in a death= pattern; else NULL + note.
    "poe2-perfect-strike-01": None,  # pattern 8 only (pricing law, no death= class) + pattern 12 port -> ambiguous, gandalf
    "tq-calculated-strike":   None,  # pattern 8 only -> NULL + note (pricing law, not a death class)
    "d2-impale-zon":          None,  # patterns 8 + 9 (both structural/pricing, no death= class) -> NULL + note

    # -- Pattern 9 SINGLE-TARGET-NO-BOSS-NICHE -> extrinsic-content-mix
    "gd-blade-trap":          "extrinsic-content-mix",
    "poe1-glacial-hammer":    None,  # patterns 9 + 10 (content-mix + sibling-shadowed). §A.2-9 gives death=extrinsic-content-mix; §A.2-10 no class. content-mix present -> but §A.2-9 members list glacial-hammer w/ content-mix. Assign content-mix. (resolved below via override)
    # d2-impale-zon also pattern 9 but handled above as NULL

    # -- Pattern 10 SIBLING-SHADOWED -> NO law, NO class (isotope validation)
    "poe1-cleave":            None,  # pattern 10 only -> NULL + note (no death= class; isotope loser)
    "poe1-sweep":             None,  # pattern 10 only -> NULL + note
    "tq-flame-surge":         None,  # pattern 10 only -> NULL + note

    # -- Pattern 11 SYSTEM-LEVEL DEGENERACY -> system-evidence
    "hot-blood-catcher":      "system-evidence",
    "vs-golden-egg-scaling":  "system-evidence",

    # -- Pattern 12 PORT-CONTEXT DEATH -> (extrinsic; the amber ledger folds it under AMBER)
    #    §A.2-12 names no explicit death= token. §A.4 tallies pattern 12 under "Extrinsic AMBER".
    #    poe2-concoction is pattern-12-only -> the cleanest port-context exhibit.
    #    We assign extrinsic-content-mix? NO — port-context is not content-mix. §A.2 provides no
    #    matching enum value for pure port-context. -> NULL + note (gandalf: may want an
    #    'extrinsic-port' value; NOT in the ratified enum, so we do NOT invent it).
    "poe2-concoction":        None,  # pattern 12 only; no enum value for port-context -> gandalf
    # poe2-chronomancer-01 & poe2-wall-of-shields: dual (1 + 12) -> assigned extrinsic-tuning above.

    # -- d2-grim-ward-barb: appears in the 5 no-rule-matched TODOs; §A.2 pattern membership?
    #    Not named in any of the 12 pattern member-lists. Its postmortem: "buffed-because-dead
    #    exemplar" (a genre in-joke). No §A.2 class -> NULL + note (gandalf).
    "d2-grim-ward-barb":      None,
    # -- d4-incinerate: named in §A.3 CONTESTED (rooted-channel) + pattern 1 region, but NOT in
    #    any pattern MEMBER list. §A.2-1 members do not include d4-incinerate (it is cited in
    #    §A.3 as a CONTESTED corpse, tuning-death-adjacent). Conservative -> NULL + note.
    "d4-incinerate":          None,
}

# Explicit overrides where the multi-tag prose gives a clear dominant class after all.
DEATH_CLASS_OVERRIDE = {
    # §A.2-9 explicitly lists poe1-glacial-hammer as a content-mix ST-no-niche death member
    # ("entire cultural footprint is jokes"); the pattern-10 dual is a secondary tag.
    "poe1-glacial-hammer": "extrinsic-content-mix",
}

# Per-kit flags note explaining every NULL death_class (surfaced to gandalf).
DEATH_CLASS_NULL_NOTE = {
    "d3-spectral-blade":     "A5-death-ambiguous: §A.2 patterns 2(itemization)+10(sibling-shadowed,no-class); no dominant. gandalf adjudicate.",
    "d4-blade-shift":        "A5-death-ambiguous: §A.2 patterns 2(itemization,extrinsic)+4(movement-pretense,intrinsic-red); incompatible classes. gandalf adjudicate.",
    "poe2-perfect-strike-01":"A5-death-ambiguous: §A.2 patterns 8(pricing-law,no-class)+12(port-context,no-enum-value). gandalf adjudicate.",
    "tq-calculated-strike":  "A5-death-null: §A.2 pattern 8 only (pricing law — no death= provenance class in §A.2). gandalf adjudicate.",
    "d2-impale-zon":         "A5-death-null: §A.2 patterns 8+9 (both structural/pricing — no death= class). gandalf adjudicate.",
    "poe1-cleave":           "A5-death-null: §A.2 pattern 10 only (sibling-shadowed isotope loser — no death= class, validation not corpse).",
    "poe1-sweep":            "A5-death-null: §A.2 pattern 10 only (sibling-shadowed isotope loser — no death= class).",
    "tq-flame-surge":        "A5-death-null: §A.2 pattern 10 only (sibling-shadowed isotope loser — no death= class).",
    "poe2-concoction":       "A5-death-null: §A.2 pattern 12 only (port-context death — §A.2 provides no matching enum value; candidate 'extrinsic-port'). gandalf adjudicate.",
    "d2-grim-ward-barb":     "A5-death-null: not a named member of any §A.2 pattern list (buffed-because-dead in-joke; keying-TODO). gandalf adjudicate.",
    "d4-incinerate":         "A5-death-null: cited in §A.3 CONTESTED (rooted-channel, tuning-adjacent) but not a §A.2 pattern MEMBER. gandalf adjudicate.",
    "d2-sacrifice":          "A5-death-null: §A.1 classes it an 'unfilled record' (leaked mint kit), not a §A.2 failure-pattern member; filled from mint dossier this batch. No death= class applies. gandalf adjudicate if a class is wanted.",
}

DEATH_CLASS_ENUM = {
    "extrinsic-tuning", "extrinsic-itemization", "extrinsic-split-scaling",
    "extrinsic-no-lever", "extrinsic-content-mix", "intrinsic-red", "system-evidence",
}

# system-record negatives (§A.2 pattern 11 — evidence, not a combat kit)
SYSTEM_RECORD_NEGATIVES = {"vs-golden-egg-scaling"}


# ======================================================================================
# helpers
# ======================================================================================
def column_exists(conn, table, col):
    return col in {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def best_note(fact_row):
    """Negatives store the postmortem in 'mech_note'; positives in 'mechanics_notes'.
    Return the longer of the two (grow-only source of truth)."""
    a = fact_row.get("mechanics_notes") or ""
    b = fact_row.get("mech_note") or ""
    return a if len(a) >= len(b) else b


def load_full_notes():
    """kit_id -> untruncated postmortem, from ALL megaprobe facts jsonl + mint dossiers."""
    full = {}
    for fn in sorted(MEGAPROBE.glob("*-facts.jsonl")):
        for line in open(fn):
            r = json.loads(line)
            kid = r.get("kit_id")
            if kid:
                full[kid] = best_note(r)
    mint = MEGAPROBE / "mint-dossiers-reexpressed.jsonl"
    if mint.exists():
        for line in open(mint):
            r = json.loads(line)
            kid = r.get("kit_id")
            if kid:
                note = best_note(r)
                if kid not in full or len(note) > len(full.get(kid, "")):
                    full[kid] = note
    return full


def load_negative_facts():
    """kit_id -> full facts dict, for status=='negative' rows + d2-sacrifice mint dossier."""
    negf = {}
    for fn in sorted(MEGAPROBE.glob("*-facts.jsonl")):
        for line in open(fn):
            r = json.loads(line)
            if r.get("status") == "negative" and r.get("kit_id"):
                negf[r["kit_id"]] = r
    # d2-sacrifice: negative=1 in corpus but its facts live in the mint dossier
    mint = MEGAPROBE / "mint-dossiers-reexpressed.jsonl"
    if mint.exists():
        for line in open(mint):
            r = json.loads(line)
            if r.get("kit_id") == "d2-sacrifice":
                negf["d2-sacrifice"] = r
    return negf


# ======================================================================================
# ITEM 1 + (item-4 note repair) — mech_note truncation repair (grow-only)
# ======================================================================================
def repair_mech_note(conn, full_notes):
    cur = {r[0]: (r[1] or "") for r in conn.execute("SELECT kit_id, mech_note FROM canon_corpus")}
    grown = 0
    grown_neg = 0
    neg_ids = {r[0] for r in conn.execute("SELECT kit_id FROM canon_corpus WHERE negative=1")}
    for kid, cur_note in cur.items():
        full = full_notes.get(kid)
        if full is None:
            continue
        if len(full) > len(cur_note):
            conn.execute("UPDATE canon_corpus SET mech_note=? WHERE kit_id=?", (full, kid))
            grown += 1
            if kid in neg_ids:
                grown_neg += 1
    conn.commit()
    return grown, grown_neg


# ======================================================================================
# ITEM 2 + 3 + 4 — re-key the 38 negatives (37 unkeyed + d2-sacrifice)
# ======================================================================================
def build_negative_engine_keys(conn, neg_facts):
    """Upsert canon_engine_key rows for every negative, with recoverable coords + cell_key;
    genuinely-unrecoverable coords LEFT NULL (passive)."""
    # canon_corpus prefix coords (already decoded from atlas_key at ingest)
    cc = {
        r[0]: dict(zip(
            ["mech_note", "amp_val", "proxy_val", "range_val", "tempo_val", "commit_val", "negative"],
            r[1:]))
        for r in conn.execute(
            "SELECT kit_id, mech_note, amp_val, proxy_val, range_val, tempo_val, commit_val, negative "
            "FROM canon_corpus WHERE negative=1")
    }

    keyed = 0
    coord_fill = {c: 0 for c in ["delivery_value", "amp_val", "proxy_val", "range_val",
                                 "tempo_val", "commit_val", "activation_val", "dependency_val",
                                 "geometry_value", "ctrl_treatment", "ctrl_function",
                                 "def_bin", "economy_model", "mob_policy_while_casting"]}
    per_kit = {}

    for kid, corpus_row in sorted(cc.items()):
        facts = neg_facts.get(kid, {})
        # --- recoverable coords ---
        delivery_value = (facts.get("delivery") or {}).get("value")            # #2
        amp_val = corpus_row["amp_val"]                                        # #3 (cc)
        proxy_val = corpus_row["proxy_val"]                                    # #8 (cc)
        range_val = corpus_row["range_val"]                                    # #9 (cc)
        tempo_val = corpus_row["tempo_val"]                                    # #10 (cc)
        commit_val = corpus_row["commit_val"]                                  # #11 (cc)
        # #12/#13 from the (repaired) mech_note via the survivors' exact functions.
        mech_note = corpus_row["mech_note"]  # already repaired by item 1 (grow-only)
        activation_val = derive_activation(mech_note, None)                    # #12
        dependency_val = derive_dependency(mech_note)                          # #13
        # activation/dependency return 'unknown' (literal) when mech_note empty -> that's a
        # real 'unknown' token, NOT a passive NULL. Keep as-is (matches survivor semantics).

        # --- genuinely-unrecoverable coords -> NULL (passive; negatives' facts lack them) ---
        geometry_value = None            # #4  (delivery+footprint ambiguous for ALL 37 — verified)
        ctrl_treatment = None            # #5a (facts.control absent on negatives)
        ctrl_function = None             # #5b
        def_bin = None                   # #6  (facts.defense absent)
        economy_model = None             # #7  (facts.economy absent)
        mob_policy_while_casting = None  # #1  (facts.movement absent)

        row_class = "system-record" if kid in SYSTEM_RECORD_NEGATIVES else "combat-kit"
        route = "loot-economy/degeneracy-evidence" if kid in SYSTEM_RECORD_NEGATIVES else None

        # cell_key: NULL for system-records (out of combat denominator, matches survivor rule);
        #   for combat-kit negatives, serialize with NULL slots -> literal 'blank' (never-merge).
        if row_class == "system-record":
            cell_key = None
        else:
            keyvals = {
                "mob_policy_while_casting": mob_policy_while_casting,
                "delivery_value": delivery_value,
                "amp_val": amp_val,
                "geometry_value": geometry_value,
                "ctrl_treatment": ctrl_treatment,
                "ctrl_function": ctrl_function,
                "def_bin": def_bin,
                "economy_model": economy_model,
                "proxy_val": proxy_val,
                "range_val": range_val,
                "tempo_val": tempo_val,
                "commit_val": commit_val,
                "activation_val": activation_val,
                "dependency_val": dependency_val,
            }
            cell_key = "|".join(slot(keyvals[c]) for c in CELL_KEY_ORDER)

        # provenance: sparse-negative keying provenance object.
        prov = {
            "keying": "A5-negative-rekey-2026-07-14",
            "source": "megaprobe-facts-jsonl (sparse negative row)",
            "recoverable_coords": [c for c, v in [
                ("delivery_value", delivery_value), ("amp_val", amp_val), ("proxy_val", proxy_val),
                ("range_val", range_val), ("tempo_val", tempo_val), ("commit_val", commit_val),
                ("activation_val", activation_val), ("dependency_val", dependency_val),
            ] if v is not None and v != "unknown"],
            "passive_null_coords": ["geometry_value", "ctrl_treatment", "ctrl_function",
                                    "def_bin", "economy_model", "mob_policy_while_casting"],
            "geometry_null_reason": "delivery+footprint pair AMBIGUOUS across positives (no deterministic geometry); charter §5 passive-category rule",
            "negative": 1,
            "supplementary_only": True,
        }
        flags = ["A5-negative-supplementary"]
        if kid in SYSTEM_RECORD_NEGATIVES:
            flags.append("system-level-evidence-record")

        raw_json = json.dumps({
            "kit_id": kid,
            "game": (facts.get("game") if facts else kid.split("-")[0]),
            "folk_name": (facts.get("folk_name") if facts else None),
            "status": "negative",
            "why_negative": (facts.get("why_negative") if facts else None),
            "delivery": facts.get("delivery") if facts else None,
            "footprint": facts.get("footprint") if facts else None,
            "mech_note": mech_note,
            "keying_provenance": prov,
            "row_class": row_class,
        }, ensure_ascii=False)

        # Upsert (idempotent). d2-sacrifice already has a row -> UPDATE it (overwrites junk key).
        conn.execute("""
            INSERT INTO canon_engine_key
                (kit_id, geometry_value, geometry_rule_fired, geometry_conf,
                 ctrl_treatment, ctrl_ailments_mapped, ctrl_ailment_gaps,
                 def_bin, def_riders, def_conf,
                 econ_status, econ_gaps, econ_meter_type,
                 mob_skill_is_movement, mob_policy_while_casting, mob_verbs,
                 row_class, route, flags, provenance_json, raw_json,
                 delivery_value, ctrl_function, economy_model,
                 activation_val, dependency_val, resource_verbatim, cell_key)
            VALUES (?,?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?,?,?, ?,?,?,?,?,?,?)
            ON CONFLICT(kit_id) DO UPDATE SET
                geometry_value=excluded.geometry_value,
                ctrl_treatment=excluded.ctrl_treatment,
                def_bin=excluded.def_bin,
                mob_policy_while_casting=excluded.mob_policy_while_casting,
                row_class=excluded.row_class,
                route=excluded.route,
                flags=excluded.flags,
                provenance_json=excluded.provenance_json,
                raw_json=excluded.raw_json,
                delivery_value=excluded.delivery_value,
                ctrl_function=excluded.ctrl_function,
                economy_model=excluded.economy_model,
                activation_val=excluded.activation_val,
                dependency_val=excluded.dependency_val,
                cell_key=excluded.cell_key
        """, (
            kid, geometry_value, None, None,
            ctrl_treatment, None, None,
            def_bin, None, None,
            None, None, None,
            None, mob_policy_while_casting, None,
            row_class, route, json.dumps(flags), json.dumps(prov), raw_json,
            delivery_value, ctrl_function, economy_model,
            activation_val, dependency_val, None, cell_key,
        ))
        keyed += 1
        for c, v in [("delivery_value", delivery_value), ("amp_val", amp_val),
                     ("proxy_val", proxy_val), ("range_val", range_val),
                     ("tempo_val", tempo_val), ("commit_val", commit_val),
                     ("activation_val", activation_val), ("dependency_val", dependency_val),
                     ("geometry_value", geometry_value), ("ctrl_treatment", ctrl_treatment),
                     ("ctrl_function", ctrl_function), ("def_bin", def_bin),
                     ("economy_model", economy_model),
                     ("mob_policy_while_casting", mob_policy_while_casting)]:
            if v is not None and v != "unknown":
                coord_fill[c] += 1
        per_kit[kid] = {"row_class": row_class, "cell_key": cell_key,
                        "delivery": delivery_value, "activation": activation_val,
                        "dependency": dependency_val}
    conn.commit()
    return keyed, coord_fill, per_kit


# ======================================================================================
# ITEM 5 — death_class provenance column
# ======================================================================================
def add_death_class(conn):
    if not column_exists(conn, "canon_corpus", "death_class"):
        # SQLite can't add a CHECK constraint via ALTER; enforce via a trigger + document.
        conn.execute("ALTER TABLE canon_corpus ADD COLUMN death_class TEXT")
        print("  + added canon_corpus.death_class TEXT")
        # CHECK-equivalent: a trigger rejecting out-of-enum non-NULL writes.
        enum_list = ",".join(f"'{v}'" for v in sorted(DEATH_CLASS_ENUM))
        conn.execute(f"""
            CREATE TRIGGER IF NOT EXISTS trg_death_class_enum
            BEFORE UPDATE OF death_class ON canon_corpus
            FOR EACH ROW WHEN NEW.death_class IS NOT NULL
              AND NEW.death_class NOT IN ({enum_list})
            BEGIN SELECT RAISE(ABORT, 'death_class not in enum'); END;
        """)
        conn.execute(f"""
            CREATE TRIGGER IF NOT EXISTS trg_death_class_enum_ins
            BEFORE INSERT ON canon_corpus
            FOR EACH ROW WHEN NEW.death_class IS NOT NULL
              AND NEW.death_class NOT IN ({enum_list})
            BEGIN SELECT RAISE(ABORT, 'death_class not in enum'); END;
        """)
        print("  + added CHECK-equivalent enum triggers on death_class")
    else:
        print("  = canon_corpus.death_class already present (idempotent)")

    # Recompute from the static map every run (idempotent).
    conn.execute("UPDATE canon_corpus SET death_class=NULL WHERE negative=1")
    assigned = 0
    nulled = 0
    for kid in {r[0] for r in conn.execute("SELECT kit_id FROM canon_corpus WHERE negative=1")}:
        cls = DEATH_CLASS_OVERRIDE.get(kid, DEATH_CLASS.get(kid, None))
        if cls is not None:
            assert cls in DEATH_CLASS_ENUM, f"{kid}: bad death_class {cls}"
            conn.execute("UPDATE canon_corpus SET death_class=? WHERE kit_id=?", (cls, kid))
            assigned += 1
        else:
            nulled += 1
    conn.commit()

    # Fold the NULL-death flags into canon_engine_key.flags (append; idempotent).
    for kid, note in DEATH_CLASS_NULL_NOTE.items():
        row = conn.execute("SELECT flags FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()
        if row is None:
            continue
        try:
            flags = json.loads(row[0]) if row[0] else []
        except (json.JSONDecodeError, TypeError):
            flags = []
        if note not in flags:
            flags.append(note)
        conn.execute("UPDATE canon_engine_key SET flags=? WHERE kit_id=?", (json.dumps(flags), kid))
    conn.commit()
    return assigned, nulled


# ======================================================================================
# denominator hygiene — amend v_combat_kits so negatives never enter the denominator
# ======================================================================================
def amend_combat_view(conn):
    conn.execute("DROP VIEW IF EXISTS v_combat_kits")
    conn.execute("""
        CREATE VIEW v_combat_kits AS
        SELECT c.*, k.geometry_value, k.geometry_conf, k.ctrl_treatment,
               k.ctrl_ailments_mapped, k.ctrl_ailment_gaps,
               k.def_bin, k.def_riders, k.econ_status, k.econ_gaps,
               k.row_class, k.route, k.flags AS ek_flags
        FROM canon_corpus c
        JOIN canon_engine_key k ON c.kit_id = k.kit_id
        WHERE k.row_class = 'combat-kit' AND c.negative = 0
    """)
    conn.commit()
    print("  ~ v_combat_kits amended: + AND c.negative=0 (negatives excluded from denominator)")


# ======================================================================================
# main
# ======================================================================================
def main():
    if not DB.exists():
        sys.exit(f"corpus.db not found at {DB}")
    conn = sqlite3.connect(str(DB))
    conn.execute("PRAGMA foreign_keys=ON")
    print(f"== corpus_curation_a5 == {DB}\n")

    # ---- ITEM 1 (+ item-4 note repair) ----
    print("[ITEM 1] mech_note truncation repair (grow-only, from megaprobe facts jsonl)")
    full_notes = load_full_notes()
    grown, grown_neg = repair_mech_note(conn, full_notes)
    print(f"  repaired (grown) {grown} rows; of which {grown_neg} are negatives\n")

    # ---- ITEM 5 (add column BEFORE re-key so enum trigger exists) ----
    print("[ITEM 5] death_class provenance column")
    add_death_class(conn)  # add column + triggers (assignment recomputed after re-key too)

    # ---- ITEM 2 + 3 + 4 (re-key the 38 negatives) ----
    print("\n[ITEM 2+3+4] re-key the 38 negatives (37 unkeyed + d2-sacrifice)")
    neg_facts = load_negative_facts()
    keyed, coord_fill, per_kit = build_negative_engine_keys(conn, neg_facts)
    print(f"  keyed {keyed} negative rows")
    print("  recoverable-coord fill counts:")
    for c in ["delivery_value", "amp_val", "proxy_val", "range_val", "tempo_val",
              "commit_val", "activation_val", "dependency_val"]:
        print(f"    {c:26s}: {coord_fill[c]}")
    print("  passive-NULL coords (all 0 by design):")
    for c in ["geometry_value", "ctrl_treatment", "ctrl_function", "def_bin",
              "economy_model", "mob_policy_while_casting"]:
        print(f"    {c:26s}: {coord_fill[c]}")

    # ---- ITEM 5 assignment (after negatives exist) ----
    print("\n[ITEM 5] assign death_class per §A.2 map")
    assigned, nulled = add_death_class(conn)  # idempotent recompute
    print(f"  assigned {assigned} death_class; {nulled} NULL (ambiguous -> gandalf, flagged)")

    # ---- denominator hygiene ----
    print("\n[HYGIENE] denominator view")
    amend_combat_view(conn)

    # ---- schema_meta snapshot marker ----
    conn.execute("DELETE FROM corpus_schema_meta WHERE version='atlas-prereg-2026-07-14'")
    _marker_note = (
        "Curation batch A.5 (elrond) - DATA SNAPSHOT for the atlas-derivation pipeline. "
        "(1) mech_note truncation repaired grow-only from megaprobe facts jsonl (CSV+raw_json were also truncated; facts jsonl is the untruncated source). "
        "(2) d2-sacrifice filled from mint dossier + re-keyed as a negative; exits combat denominator via negative=0 filter. "
        "(3) 38 negatives keyed through the Layer-3 pipeline (survivors keying fns reused): recoverable coords (#2 delivery, #3 amp, #8 proxy, #9 range, #10 tempo, #11 commit, #12 activation, #13 dependency) land; genuinely-unrecoverable (#1 mob, #4 geometry, #5a/#5b ctrl, #6 def, #7 econ) LEFT NULL passive per charter section 5. Negatives stay negative=1, supplementary-only. vs-golden-egg-scaling keyed row_class=system-record (A.2 pattern 11). "
        "(4) 5 no-rule-matched TODOs resolved (all genre-negatives; keyed in item 3). "
        "(5) death_class TEXT added (7-value enum, CHECK-equivalent triggers) per A.2 pattern->class map; ambiguous rows NULL + flags note for gandalf. "
        "ADDITIVE only; the 469 clean survivor cell_keys UNTOUCHED. v_combat_kits amended (+AND negative=0). Backup: corpus.db.pre-A5-2026-07-14-backup."
    )
    conn.execute(
        "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        ("atlas-prereg-2026-07-14", "2026-07-14T00:00:00Z", _marker_note),
    )
    conn.commit()
    print("\n  schema_meta marker written: atlas-prereg-2026-07-14")
    conn.close()
    print("  DONE.")


if __name__ == "__main__":
    main()
