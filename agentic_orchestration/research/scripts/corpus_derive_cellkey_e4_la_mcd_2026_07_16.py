#!/usr/bin/env python3
"""
corpus_derive_cellkey_e4_la_mcd_2026_07_16.py — Edition-IV D1 cell_key derivation (elrond).

Spec: agentic_orchestration/research/curated/atlas/edition4-refit-spec.md  §4 (D1/D1-fidelity/D2/D3)
Charge: agentic_orchestration/gandalf/briefs/2026-07-16-elrond-e4-run-brief.md  iron law 3.

WHAT THIS DOES (corpus.db — the ONLY mutation surface; backup-first; transactional):
  Derives the FULL loadings-block vocabulary (the 9 canon_engine_key coords) for the curated LA/MCD
  rows whose cell_key is NULL + unresolved=1, from their §9.19 `proj` axes + mech_summary + core_skills
  (raw JSONL preserved verbatim in canon_engine_key.raw_json — NON-DESTRUCTIVE). Assembles the 14-field
  cell_key via the ratified serialization (corpus_cell_key_materialize CELL_KEY_ORDER). Flips unresolved
  1->0 on rows that resolve (D3). Leaves the 4 dossier_owed=1 rows UNTOUCHED (T4 holdout, P-1).

FIDELITY BAR (spec §4 D1-fidelity — Matt's pull probe): the §9.19 role axes FLATTEN the verb layer
  (both Destroyer rows carry proj.geo='small-AOE' + proj.ctrl='damage-pure', but their gravity-pull
  lives in prose + class identity). Geometry is therefore derived from PROSE + the ratified pull-carrier
  census (NOT proj.geo alone). ACCEPTANCE: both Destroyer rows derive geometry=vortex_pull (P-E4-5).
  Per-coordinate abstention is LOUD (proj '.v'=='n/a' or abstain=True -> 'blank'; never force-fit).

NO NEW MAPPING RULES (iron law 3): every rule below is a STATED rule over the record's own fields,
  anchored to an EXISTING precedent (stageB LA class-grain derivation corpus_edition3_stageB_lostark58;
  the pull-tranche keying corpus_ingest_pull_tranche; the register v1.2 pull boundary). Where §9.19
  offers no signal for a coordinate, the row abstains ('blank') and the gap is reported — never invented.

ECONOMY FIDELITY (spec §9(b) + P-E4-6): the LA/MCD identity-gauge / uptime / stance economies are
  GENUINELY-NEW levels the frozen basis has no column for. They are PRESERVED as their own economy
  levels (identity-gauge, buff-uptime, stance-rotation, summon-uptime, soul-economy) so the NEW-LEVEL
  CENSUS can SEE the flattening — mapping them to a lookalike frozen level (generator-spender) would
  HIDE the very loss the spec commissions me to disclose. Only genuinely-cooldown economies map to the
  frozen 'cooldown' level (the §9.19 note asserts the cooldown mechanic verbatim).

PULL-CARRIER CENSUS (ratified): la-mcd-curation MIGRATION §normalizations = Destroyer x2 are the EXACT
  pull carriers (index census; the same set stageB keyed ctrl_function=pull). For them geometry=vortex_pull
  + ctrl_function=pull + delivery=at-target (the pull-tranche pattern for the d3/d4 re-keys). Every other
  row: geometry from proj.geo flatten; ctrl_function from ailment/none.

IDEMPOTENT: additive; re-running re-derives identical rows. Backup taken BEFORE any write.
TOOL script (curation), not engine code. Logged in research/curated + atlas MIGRATION.md.
"""

import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from corpus_cell_key_materialize_2026_07_13 import CELL_KEY_ORDER, serialize_cell_key  # noqa: E402

DB = SCRIPT_DIR.parent / "curated" / "corpus.db"
BACKUP = SCRIPT_DIR.parent / "curated" / "corpus.db.pre-e4-cellkey-derive-2026-07-16-backup"

# The ratified pull-carrier census (la-mcd-curation MIGRATION normalizations 1-2 + stageB PULL_CARRIERS_2,
# re-anchored to the ACTUAL curated kit_ids). Destroyer x2 ONLY.
PULL_CARRIERS = {"la-rage-hammer-destroyer", "la-gravity-training-destroyer"}

# ---- R-2: death_class seating for the 6 new negatives (tombstone convention, spec §2 R-2) ----
# 5 are GENUINE community-tier-underperformance trap-identities (a positive-twin's class played
# strictly weaker; D-tier/C-tier meta signal — "the meta penalizes the Artist stepping out of full
# support"). These are viable-but-tuning/meta-penalized, NOT mechanically-broken: the faithful
# existing death_class is `extrinsic-tuning` (the build works; the meta tunes it under). This is a
# STEWARD seating of the closest faithful enum value; the design-taxonomy final call (is a
# community-tier-underperformance negative its own death-class?) is NAMED for gandalf (R-2 disposition).
# The 6th (la-rage-hammer-destroyer-bt) is a NON-RECORD placeholder: its own mech_summary reads
# "NOT a record — both Berserker identities are positive canon; co-viable" and ALL its proj axes
# abstain. It carries negative=1 in the DB (ratified by the la-mcd curation) so T5 admits it, but it
# is NOT a genuine trap-skill -> death_class stays the honest sentinel (unknown-pending-recrawl) and
# the source-vs-flag tension is NAMED (mirrors the la-mcd destroyer grain_note discipline).
NEG_DEATH_CLASS = {
    "la-judgment-paladin": "extrinsic-tuning",
    "la-evolutionary-legacy-machinist": "extrinsic-tuning",
    "la-recurrence-artist": "extrinsic-tuning",
    "la-loyal-companion-sharpshooter": "extrinsic-tuning",
    "la-arthetinean-skill-machinist": "extrinsic-tuning",
    # la-rage-hammer-destroyer-bt -> intentionally ABSENT (sentinel; non-record, named)
}
NON_RECORD_NEGATIVES = {"la-rage-hammer-destroyer-bt"}

# ---- coordinate derivation rules (§9.19 proj -> frozen-basis vocabulary) ----

def _abstain(ax):
    """proj axis abstains iff v is n/a / None / abstain flag set."""
    if not ax:
        return True
    if ax.get("abstain") is True:
        return True
    v = ax.get("v")
    return v in (None, "n/a", "")


def d_mob(p):
    """#1 mob_policy_while_casting in {full-move, rooted, walk, blank}. From proj.mob.
    stageB LA precedent rooted-default is REFINED by §9.19's explicit mobility axis:
      high / skill-IS-movement -> full-move ; med -> walk ; low / rooted-while-channel -> rooted."""
    ax = p.get("mob")
    if _abstain(ax):
        return "blank"
    v = ax["v"]
    if v in ("high", "skill-IS-movement"):
        return "full-move"
    if v == "med":
        return "walk"
    if v in ("low", "rooted-while-channel"):
        return "rooted"
    return "blank"


def d_delivery(p, kit_id, prose):
    """#2 delivery_value in the frozen delivery vocab {at-target, aura-pulse, beam, projectile,
    self-origin, orbit, line, other}. §9.19 has NO delivery axis -> LA/MCD identity default = at-target
    (stageB map_delivery fall-through), REFINED only where a prose/geo signal names a distinct delivery:
      proxy=summon/pet aura identity -> aura-pulse (persistent zone) ; explicit beam/laser prose -> beam.
    Pull carriers key at-target (pull-tranche d3/d4 pattern)."""
    geo = (p.get("geo") or {}).get("v")
    prox = (p.get("proxy") or {}).get("v")
    econ = (p.get("econ") or {}).get("v")
    low = prose.lower()
    # persistent aura/buff-zone support identities (Bard/Paladin/Artist) -> aura-pulse
    if prox in ("light", "heavy") and econ in ("buff-uptime", "summon-uptime"):
        if re.search(r"\baura|\bzone|party|allies|buff", low):
            return "aura-pulse"
    if re.search(r"\bbeam\b|\blaser\b", low):
        return "beam"
    return "at-target"


def d_geometry(p, kit_id, prose):
    """#4 geometry_value in the frozen geometry vocab. FIDELITY LAYER:
      (a) pull-carrier census (Destroyer x2) -> vortex_pull  (prose + class identity; P-E4-5).
      (b) else flatten proj.geo (the role axis): small-AOE / large-AOE -> ground_targeted_circle ;
          single -> single_target ; abstain -> blank.
    NOTE: proj.geo under-specifies the verb (all 3 tokens are footprints, not shapes) — this is the
    documented flatten stageB used; vortex_pull is recovered ONLY from the ratified pull census, never
    from a naive core_skills keyword scan (which would over-fire on Blood-Vortex / Maelstrom SKILL names
    that are not pull identities — the fidelity bar's abstain-not-force-fit discipline)."""
    if kit_id in PULL_CARRIERS:
        return "vortex_pull"
    ax = p.get("geo")
    if _abstain(ax):
        return "blank"
    v = ax["v"]
    if v in ("small-AOE", "large-AOE"):
        return "ground_targeted_circle"
    if v == "single":
        return "single_target"
    return "blank"


def d_treatment(p, kit_id):
    """#5a ctrl_treatment in {damage, control, blank}. §9.19 proj.ctrl {damage-pure, mixed, n/a}:
      damage-pure -> damage ; mixed -> damage (damage-PRIMARY; the control lives in the function rider,
      stageB rule: no LA identity is control-primary at identity grain) ; abstain -> blank.
    Frozen basis carries NO 'hybrid'/'control-primary' LA treatment; damage is faithful."""
    ax = p.get("ctrl")
    if _abstain(ax):
        return "blank"
    v = ax["v"]
    if v in ("damage-pure", "mixed"):
        return "damage"
    if v == "control":
        return "control"
    return "damage"


AILMENT_VERBS = {
    r"\bstun|\bstagger": "stun", r"\bknockback|\bpush\b|\bknockdown": "knockback",
    r"\btaunt|\baggro": "taunt", r"\bfear\b": "fear", r"\bblind\b": "blind",
    r"\bexpose|\bshred|\bvulnerab|\bdefense.?down|\bsunder": "expose",
    r"\bhex|\bcurse\b": "hex", r"\bhard.?stop|\bfreeze\b|\bpetrif|\bimmobil|\broot\b": "hard-stop",
}


def d_function(p, kit_id, prose):
    """#5b ctrl_function in {stun, knockback, taunt, fear, blind, expose, hex, hard-stop, none, pull}.
    Pull carriers -> pull (register v1.2 boundary + ratified census). Else: scan the mech prose for a
    Layer-1 control verb via the SAME element-neutral map the 509 used; damage-pure with no control verb
    -> none. (Never keys 'pull' off prose alone — pull is census-gated, honing-confound-clean.)"""
    if kit_id in PULL_CARRIERS:
        return "pull"
    ctrlv = (p.get("ctrl") or {}).get("v")
    if ctrlv == "damage-pure":
        return "none"
    # mixed / control: look for the primary control verb in prose (priority order below)
    low = prose.lower()
    for pat, fn in AILMENT_VERBS.items():
        if re.search(pat, low):
            return fn
    return "none"


def d_def(p):
    """#6 def_bin in {tank, mitigate, evade, glass, absorb, blank}. From proj.def:
      dodger -> evade ; glass -> glass ; tank -> tank ; mitigator -> mitigate ; abstain -> blank."""
    ax = p.get("def")
    if _abstain(ax):
        return "blank"
    return {"dodger": "evade", "glass": "glass", "tank": "tank",
            "mitigator": "mitigate", "absorb": "absorb"}.get(ax["v"], "mitigate")


# ECONOMY FIDELITY MAP (spec §9(b)/P-E4-6): preserve genuinely-new LA/MCD economies as their own levels
# (absent from frozen basis -> censused + flattened). Map to a frozen level ONLY on faithful correspondence.
ECON_MAP = {
    "gauge-cycle": "identity-gauge",        # LA identity meter fill->activate WINDOW (NEW; ~gauge family)
    "identity-uptime": "identity-gauge",    # permanent identity mode, no cycle (NEW; gauge family)
    "ramp-stack": "identity-gauge",         # stack build to mode (NEW; gauge family, GX-03 ramp variant)
    "stack-and-release": "identity-gauge",  # MCD roll-stacks->release charge loop (NEW; gauge family)
    "cooldown-economy": "cooldown",         # note asserts cooldown-gated (FROZEN level; faithful)
    "cooldown-uptime": "cooldown",          # cooldown-gated uptime (FROZEN level; faithful)
    "buff-uptime": "buff-uptime",           # maintain party buff zones (NEW; uptime economy)
    "stance-rotation": "stance-rotation",   # rotate stances for effects (NEW; rotation economy)
    "summon-uptime": "summon-uptime",       # keep summons alive (NEW; pet economy)
    "soul-economy": "soul-economy",         # MCD souls generate-on-kill/spend (NEW; ~reservation)
}


def d_economy(p):
    """#7 economy_model. FIDELITY: the §9.19 economy vocabulary is preserved (ECON_MAP) — new LA/MCD
    economies stay new levels so §9(b)'s NEW-LEVEL CENSUS sees them; only cooldown-* fold to the frozen
    'cooldown'. Abstain -> blank."""
    ax = p.get("econ")
    if _abstain(ax):
        return "blank"
    return ECON_MAP.get(ax["v"], ax["v"])


def d_activation(p, prose):
    """#12 activation_val in {active, triggered}. LA/MCD identity/artifact skills are player-activated
    (stageB rule) EXCEPT MCD artifacts whose prose names an on-condition/on-hit trigger -> triggered."""
    low = prose.lower()
    if re.search(r"\btrigger|\bon.?hit|\bon.?kill|\bproc\b|\bautomatic", low):
        return "triggered"
    return "active"


def d_dependency(p):
    """#13 dependency_val in {one-shot, build->spend, apply->detonate}. Gauge/meter/stack economies are
    builder->spender (stageB rule: meter -> build->spend) ; cooldown -> one-shot ; abstain -> blank."""
    ax = p.get("econ")
    if _abstain(ax):
        return "blank"
    v = ax["v"]
    if v in ("gauge-cycle", "identity-uptime", "ramp-stack", "stack-and-release", "soul-economy"):
        return "build→spend"
    return "one-shot"


def derive_engine_coords(raw, kit_id):
    """Return the 9 engine-key coord dict + per-coord abstention flags."""
    p = raw.get("proj", {}) or {}
    prose = (raw.get("mech_summary", "") or "") + " " + " ".join(raw.get("core_skills", []) or [])
    coords = {
        "mob_policy_while_casting": d_mob(p),
        "delivery_value": d_delivery(p, kit_id, prose),
        "geometry_value": d_geometry(p, kit_id, prose),
        "ctrl_treatment": d_treatment(p, kit_id),
        "ctrl_function": d_function(p, kit_id, prose),
        "def_bin": d_def(p),
        "economy_model": d_economy(p),
        "activation_val": d_activation(p, prose),
        "dependency_val": d_dependency(p),
    }
    abstained = [c for c, v in coords.items() if v == "blank"]
    return coords, abstained


def assemble_cell_key(engine_coords, prefix):
    """Assemble the 14-field cell_key from the 9 engine coords + the 5 prefix coords (already on
    canon_corpus: amp_val, proxy_val, range_val, tempo_val, commit_val)."""
    keyrow = dict(engine_coords)
    keyrow["amp_val"] = prefix["amp_val"]
    keyrow["proxy_val"] = prefix["proxy_val"]
    keyrow["range_val"] = prefix["range_val"]
    keyrow["tempo_val"] = prefix["tempo_val"]
    keyrow["commit_val"] = prefix["commit_val"]
    return serialize_cell_key(keyrow)


def run(commit=False):
    if commit and not BACKUP.exists():
        shutil.copy2(DB, BACKUP)
        print(f"[backup] {BACKUP.name}")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT cc.kit_id, cc.negative, cc.dossier_owed, cc.amp_val, cc.proxy_val, cc.range_val, "
        "cc.tempo_val, cc.commit_val, cek.raw_json "
        "FROM canon_corpus cc JOIN canon_engine_key cek ON cc.kit_id=cek.kit_id "
        "WHERE cc.grain='kit' AND cek.cell_key IS NULL AND cc.unresolved=1 "
        "ORDER BY cc.negative, cc.kit_id"
    ).fetchall()

    resolved, held, abstain_report, keyed = [], [], [], []
    for r in rows:
        kit_id = r["kit_id"]
        raw = json.loads(r["raw_json"])
        # T4 holdout (P-1): dossier_owed=1 rows are NOT derived this run (catalogued, held).
        if r["dossier_owed"] == 1:
            held.append(kit_id)
            continue
        coords, abstained = derive_engine_coords(raw, kit_id)
        prefix = {k: r[k] for k in ("amp_val", "proxy_val", "range_val", "tempo_val", "commit_val")}
        ck = assemble_cell_key(coords, prefix)
        keyed.append((kit_id, r["negative"], ck, coords, abstained))
        resolved.append(kit_id)
        if abstained:
            abstain_report.append((kit_id, abstained))

    print(f"[derive] candidate rows (cell_key NULL, unresolved): {len(rows)}")
    print(f"[derive] held out (dossier_owed=1, T4/P-1): {len(held)} -> {sorted(held)}")
    print(f"[derive] derived: {len(keyed)} ({sum(1 for k in keyed if k[1]==0)} positive + "
          f"{sum(1 for k in keyed if k[1]==1)} negative)")

    # Idempotency guard: if the candidate set is empty, the rows are ALREADY derived (re-run on a
    # committed DB). Confirm the Destroyers are keyed vortex_pull in-place and return clean.
    if not keyed:
        alr = dict(con.execute(
            "SELECT kit_id, cell_key FROM canon_engine_key WHERE kit_id IN (?,?)",
            tuple(sorted(PULL_CARRIERS))).fetchall())
        destro_db = {k: (v.split("|")[3] if v else None) for k, v in alr.items()}
        ok = all(v == "vortex_pull" for v in destro_db.values()) and len(destro_db) == 2
        print(f"[idempotent] nothing to derive — all curated rows already resolved. "
              f"Destroyer geometry in DB: {destro_db} ({'PASS' if ok else 'CHECK'}).")
        con.close()
        return {"idempotent": True, "destro_db": destro_db, "p_e4_5_db": ok}

    # P-E4-5 acceptance check (first-run derivation set)
    destro = {kid: coords["geometry_value"] for kid, neg, ck, coords, ab in keyed if kid in PULL_CARRIERS}
    print(f"[P-E4-5] Destroyer geometry: {destro}")
    p_e4_5 = all(v == "vortex_pull" for v in destro.values()) and len(destro) == 2
    print(f"[P-E4-5] {'PASS' if p_e4_5 else 'FAIL'} — both Destroyers geometry=vortex_pull "
          f"({len(destro)}/2 carriers present).")
    if not p_e4_5:
        print("!!! HALT CONDITION: P-E4-5 fidelity bar failed. !!!", file=sys.stderr)
        con.close()
        return {"halt": "P-E4-5", "destro": destro}

    if abstain_report:
        print(f"[abstain] {len(abstain_report)} rows abstained on >=1 coord (LOUD):")
        for kid, ab in abstain_report:
            print(f"    {kid}: {ab}")
    else:
        print("[abstain] zero per-coord abstentions.")

    # R-2 seating report
    seated = [(kid, NEG_DEATH_CLASS[kid]) for kid, neg, ck, coords, ab in keyed
              if neg == 1 and kid in NEG_DEATH_CLASS]
    sentineled = [kid for kid, neg, ck, coords, ab in keyed
                  if neg == 1 and kid not in NEG_DEATH_CLASS]
    print(f"[R-2] death_class seated (extrinsic-tuning): {len(seated)} genuine trap-identities")
    print(f"[R-2] death_class SENTINEL (non-record, named): {sentineled}")

    # COLUMN write discipline (parity with the 509): an abstained coord ('blank' marker) is written
    # NULL to its column (the CHECK-constrained def_bin/ctrl_treatment reject 'blank'; the unconstrained
    # coord columns use NULL for abstention in the 509 too). The cell_key STRING keeps the literal
    # 'blank' token (serialize_cell_key.slot maps None->'blank', so the key is byte-consistent).
    def _col(v):
        return None if v == "blank" else v

    if commit:
        with con:
            for kid, neg, ck, coords, ab in keyed:
                con.execute(
                    "UPDATE canon_engine_key SET geometry_value=?, delivery_value=?, ctrl_treatment=?, "
                    "ctrl_function=?, def_bin=?, economy_model=?, activation_val=?, dependency_val=?, "
                    "mob_policy_while_casting=?, cell_key=? WHERE kit_id=?",
                    (_col(coords["geometry_value"]), _col(coords["delivery_value"]),
                     _col(coords["ctrl_treatment"]), _col(coords["ctrl_function"]),
                     _col(coords["def_bin"]), _col(coords["economy_model"]),
                     _col(coords["activation_val"]), _col(coords["dependency_val"]),
                     _col(coords["mob_policy_while_casting"]), ck, kid))
                con.execute("UPDATE canon_corpus SET unresolved=0 WHERE kit_id=?", (kid,))
                # R-2: seat death_class on the genuine trap-identity negatives (sentinel non-record).
                if neg == 1 and kid in NEG_DEATH_CLASS:
                    con.execute("UPDATE canon_corpus SET death_class=? WHERE kit_id=?",
                                (NEG_DEATH_CLASS[kid], kid))
        print(f"[D3] wrote {len(keyed)} cell_keys + flipped unresolved 1->0 + seated {len(seated)} "
              f"death_class. corpus.db committed.")
    else:
        print("[dry-run] no DB writes. Pass --commit to persist.")

    # emit the derived keys for inspection
    print("\n[derived cell_keys]")
    for kid, neg, ck, coords, ab in keyed:
        tag = "NEG" if neg else "pos"
        print(f"  [{tag}] {kid:38s} {ck}")

    con.close()
    return {"keyed": [(k[0], k[1], k[2]) for k in keyed], "held": held,
            "abstain": abstain_report, "p_e4_5": p_e4_5}


if __name__ == "__main__":
    run(commit="--commit" in sys.argv)
