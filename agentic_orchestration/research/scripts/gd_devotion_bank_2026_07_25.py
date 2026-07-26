#!/usr/bin/env python3
"""
gd_devotion_bank_2026_07_25.py — the GD devotion payload extraction + banking run.

Commissioned by gandalf (GD program, 2026-07-25) off elrond's own probe
`agentic_orchestration/elrond/notes/2026-07-25-devotion-payload-probe.md`.
Migration doc: `agentic_orchestration/research/curated/MIGRATION-devotion-payloads-2026-07-25.md`

GATES (all must pass before rows land):
  G0  RANK AXIS RESOLVED   — `gd_devotion_rank_axis_probe{,2}_2026_07_25.py`. Never bank an
                             unlabelled rank. Every header row carries `rank_axis`.
  G1  FIELD POLICY         — `gd_devotion_field_policy_2026_07_25.py`, zero unclassified residual.
  G2  BACKUP               — pre-DDL byte copy + md5 (Discipline #8/#11).
  G3  EDITION PIN          — sha256 of every .arz read is verified against the recorded freeze
                             fingerprint BEFORE parsing. A silent edition drift is a poisoned bank.
  G4  IN-PIPE ASSERTS      — non-null, PK-collision, direction-aware monotonicity, axis bounds.
  G5  READ-BACK VERIFY     — float32-canonical byte-match of tier-1 anchors from SQLite.

USAGE
    python3 gd_devotion_bank_2026_07_25.py --verify-only   # parse + build + asserts, NO DB writes
    python3 gd_devotion_bank_2026_07_25.py --dry-run       # + row plan, NO DB writes
    python3 gd_devotion_bank_2026_07_25.py                 # apply
"""
import sys, re, json, pathlib, sqlite3, hashlib, shutil, struct, datetime, collections

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gd_arz_adapter_2026_07_24 import ArzArchive          # noqa: E402
import gd_devotion_field_policy_2026_07_25 as POLICY      # noqa: E402

DB = HERE.parent / "curated" / "corpus.db"
BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
SCHEMA_VERSION = "gd-devotion-payloads-2026-07-25"
ADAPTER = "gd_devotion_bank_2026_07_25.py"
GAME = "gd"
LANE = "gd-devotion"

# ---- G3: edition pin. sha256 recorded in the Edition-I freeze fingerprint §3 (base/gdx1/gdx2)
#      and the Edition-II cut record §3 (gdx3). Depot/manifest from freeze §4 + cut §2.
ARCHIVES = {
    "database/database.arz": dict(
        file="database.arz", depot=219991, name="base",
        manifest="8006922163969537169",
        sha256="8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f"),
    "gdx1/database/GDX1.arz": dict(
        file="GDX1.arz", depot=642280, name="gdx1/AshesOfMalmouth",
        manifest="2275863479823292335",
        sha256="e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539"),
    "gdx2/database/GDX2.arz": dict(
        file="GDX2.arz", depot=897670, name="gdx2/ForgottenGods",
        manifest="4804720554373426689",
        sha256="f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985"),
    "gdx3/database/GDX3.arz": dict(
        file="GDX3.arz", depot=2699230, name="gdx3/FangsOfAsterkarn",
        manifest="1575323658468418166",
        sha256="1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0"),
}
EDITION = "gd-edition-II-20260724"

# ---- fidelity grade, era-substrate LAW §4 (canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md)
FIDELITY_GRADE = "MEASURED"
FIDELITY_BASIS = "primary-source-datamine"   # vs 'live-oracle-fixture'; see MIGRATION doc §7

# ---- G5 tier-1 anchors: Twin Fangs (`records/skills/devotion/tier1_01e_skill.dbr`).
#
# CORRECTED 2026-07-25 against the .arz. The first run FAILED 3/17 here and the HALT-diagnosis
# named the layer: **the ORACLE, not the parse.** The probe note's §2.2 "VERBATIM PROOF" block
# truncated Twin Fangs' 25-element arrays to 20 elements when transcribing, and annotated
# `skillExperienceLevels` as "20 entries" when it holds 25. The values below are read from the
# archive, not from the note. Consequence for the probe's headline spec sentence: Twin Fangs is
# 128-221 vitality + 165 pierce + 22% weapon damage at level 25 of 25 -- NOT "108-186 vitality
# + 140 pierce + 20% weapon damage at rank 20 of 20". Life leech is the one short array (20
# levels authored against a 25-level axis) and does max at 40%.
ANCHORS_FIELD = {   # (record_path, raw_field, rank) -> expected value
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeMin", 1): 28.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeMin", 20): 104.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeMin", 25): 128.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeMax", 1): 46.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeMax", 25): 221.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensivePierceMin", 1): 40.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensivePierceMin", 25): 165.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "offensiveLifeLeechMin", 20): 40.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "weaponDamagePct", 1): 10.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "weaponDamagePct", 25): 22.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "skillCooldownTime", None): 0.6,
    ("records/skills/devotion/tier1_01e_skill.dbr", "projectileLaunchNumber", None): 2.0,
    ("records/skills/devotion/tier1_01e_skill.dbr", "projectilePiercingChance", None): 100.0,
}
ANCHORS_POWER = {   # power_record -> expected devotion_power columns
    "records/skills/devotion/tier1_01e_skill.dbr": dict(
        power_name="Twin Fangs", constellation_name="Bat",
        trigger_event="AttackEnemy", target_frame="Enemy",
        proc_chance_pct=20.0, auto_target_radius=22.0, icd_sec=0.6),
}


def f32(x):
    """Canonicalize through single precision — the source's native float width (GD-SLICE G3 law)."""
    return None if x is None else struct.unpack("<f", struct.pack("<f", float(x)))[0]


# ============================================================ G3 edition verify
def verify_edition():
    print("G3 — EDITION PIN verification (sha256 of every .arz read)")
    ok = True
    for rel, meta in ARCHIVES.items():
        p = BASE / rel
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        good = (h == meta["sha256"])
        ok &= good
        print(f"    {'OK  ' if good else 'FAIL'} {rel:26s} {h[:16]}…  depot={meta['depot']} "
              f"manifest={meta['manifest']}")
    if not ok:
        raise SystemExit("HALT — .arz bytes do not match the recorded edition pin. "
                         "Do NOT bank: the edition drifted or the freeze record is wrong.")
    print(f"    edition = {EDITION}  (4/4 archives byte-verified)\n")


def pin_for(rel):
    m = ARCHIVES[rel]
    return (f"{EDITION}; depot={m['depot']}({m['name']}); manifest={m['manifest']}; "
            f"arz_sha256={m['sha256']}")


# ============================================================ load
def load_union():
    ars = {a: ArzArchive(BASE / a) for a in ARCHIVES}
    union = {}
    for a in ARCHIVES:                      # later archives override base (probe §3.2)
        for r in ars[a].records:
            union[r] = a
    return ars, union


# ============================================================ rank-axis resolution (G0)
def resolve_axes(ars, union, dev_records):
    """
    G0 OUTPUT. Per in-scope record, return (rank_axis, rank_axis_max, rank_axis_source).

    RESOLVED EMPIRICALLY (see MIGRATION §3 for the full evidence chain):
      - `skillExperienceLevels` present  -> axis = SKILL-XP LEVEL, cardinality = len(table).
        60/65 celestial powers have EVERY numeric payload array exactly that long.
      - arrays but no XP table           -> axis INHERITED from the parent that references this
        record via buffSkillName/petBonusName/petSkillName (4 records, all pet-bonus riders).
      - no arrays                        -> axis = NONE (flat scalars; 605 star-node passives
        and pet-bonus records).
    """
    parent_of = {}
    for r in dev_records:
        rec = ars[union[r]].read_record(r)
        for k in ("buffSkillName", "petBonusName", "petSkillName", "skillSecondaryName"):
            v = rec.get(k)
            if isinstance(v, str) and v and v not in parent_of:
                parent_of[v] = r

    xp_len, has_arr = {}, {}
    for r in dev_records:
        rec = ars[union[r]].read_record(r)
        xp = rec.get("skillExperienceLevels")
        if isinstance(xp, list) and xp:
            xp_len[r] = len(xp)
        has_arr[r] = any(isinstance(v, list) and len(v) > 1 and not POLICY.field_denied(k)
                         and POLICY.payload_family(k) and not isinstance(v[0], str)
                         for k, v in rec.items())

    out = {}
    for r in dev_records:
        if r in xp_len:
            out[r] = ("skill_xp_level", xp_len[r], "skillExperienceLevels (in-record, len=%d)" % xp_len[r])
            continue
        if has_arr[r]:
            p, hops = parent_of.get(r), 0
            while p is not None and p not in xp_len and hops < 4:
                p, hops = parent_of.get(p), hops + 1
            if p in xp_len:
                out[r] = ("skill_xp_level", xp_len[p],
                          f"inherited from parent {p} (len={xp_len[p]})")
            else:
                out[r] = ("UNRESOLVED", None, "arrays present, no XP table, no XP-bearing parent")
            continue
        out[r] = ("none", None, "no rank arrays — flat scalar record")
    return out


# ============================================================ build rows
def build(ars, union):
    dev = sorted(r for r in union if r.startswith(POLICY.LANE_PREFIX))
    in_scope, scope_reasons = [], collections.Counter()
    for r in dev:
        try:
            rec = ars[union[r]].read_record(r)
        except Exception:
            scope_reasons["unreadable"] += 1
            continue
        ok, why = POLICY.record_in_scope(r, rec)
        scope_reasons[why] += 1
        if ok:
            in_scope.append(r)

    axes = resolve_axes(ars, union, in_scope)
    unresolved = [r for r, (a, _, _) in axes.items() if a == "UNRESOLVED"]
    if unresolved:
        raise SystemExit(f"HALT (G0) — {len(unresolved)} records carry rank arrays on an "
                         f"UNRESOLVED axis; banking them would poison every payload number. "
                         f"e.g. {unresolved[:5]}")

    headers, fields = [], []
    for r in in_scope:
        rel = union[r]
        rec = ars[rel].read_record(r)
        axis, axis_max, axis_src = axes[r]
        fd = rec.get("FileDescription") or ""
        ext = dict(skill_max_level=rec.get("skillMaxLevel"),
                   skill_ultimate_level=rec.get("skillUltimateLevel"),
                   template_name=rec.get("templateName"),
                   skill_display_tag=rec.get("skillDisplayName"),
                   skill_desc_tag=rec.get("skillBaseDescription"),
                   file_description=fd or None,
                   rank_axis_table_len=axis_max,
                   string_valued_payload={})

        seen = {}
        for raw_field, v in sorted(rec.items()):
            vals = v if isinstance(v, list) else [v]
            if not [x for x in vals if x not in (0, 0.0, False, "", None)]:
                continue
            if POLICY.field_denied(raw_field):
                continue
            fam = POLICY.payload_family(raw_field)
            if fam is None:
                raise SystemExit(f"HALT (G1) — unclassified payload field '{raw_field}' on {r}. "
                                 f"Extend the field policy explicitly; never bank blind.")
            if isinstance(vals[0], str):
                ext["string_valued_payload"][raw_field] = v      # routed, not dropped
                continue
            ck, ckp = POLICY.canon_key_for(raw_field)
            is_core = 1 if fam in POLICY.CORE_FAMILIES else 0
            unit = POLICY.unit_for(raw_field)
            nums = [1.0 if x is True else (0.0 if x is False else float(x)) for x in vals]
            if isinstance(v, list) and len(vals) > 1:
                mdir = POLICY.monotonic_dir(nums)
                for i, val in enumerate(nums, start=1):
                    key = (ck, i)
                    if key in seen:
                        raise SystemExit(f"HALT (G4) — canon_key collision on {r}: "
                                         f"'{seen[key]}' and '{raw_field}' -> '{ck}' rank {i}")
                    seen[key] = raw_field
                    fields.append(dict(entity_id=r, canon_key=ck, rank=i, canon_value=val,
                                       canon_unit=unit, raw_field=raw_field, raw_value=val,
                                       field_kind="rank_array", field_family=fam,
                                       is_core=is_core, canon_key_provenance=ckp,
                                       monotonic_class=1 if mdir in ("up", "down") else 0,
                                       monotonic_dir=mdir,
                                       source_file=ARCHIVES[rel]["file"], record_path=r))
            else:
                key = (ck, None)
                if key in seen:
                    raise SystemExit(f"HALT (G4) — canon_key collision on {r}: "
                                     f"'{seen[key]}' and '{raw_field}' -> '{ck}' (static)")
                seen[key] = raw_field
                fields.append(dict(entity_id=r, canon_key=ck, rank=None, canon_value=nums[0],
                                   canon_unit=unit, raw_field=raw_field, raw_value=nums[0],
                                   field_kind="static", field_family=fam,
                                   is_core=is_core, canon_key_provenance=ckp,
                                   monotonic_class=0, monotonic_dir="none",
                                   source_file=ARCHIVES[rel]["file"], record_path=r))

        headers.append(dict(
            entity_id=r, entity_kind="game_skill", kit_id=None, game=GAME,
            display_name=fd or None,
            record_type=rec.get("Class") or ars[rel].record_type(r) or None,
            rank_count=axis_max or 1, rank_axis=axis, rank_axis_source=axis_src,
            source_file=ARCHIVES[rel]["file"], source_version=pin_for(rel), record_path=r,
            ext_json=json.dumps(ext, sort_keys=True),
            name_provenance="in-record FileDescription '<Constellation> - <Power>'; "
                            ".arc tag-bridge NOT required for this lane (probe §1.4)",
            fidelity_grade=FIDELITY_GRADE, fidelity_basis=FIDELITY_BASIS, lane=LANE,
            adapter=ADAPTER, schema_version=SCHEMA_VERSION))

    powers, vocab = build_powers(ars, union, in_scope, axes)
    constellations = build_constellations(ars, union)
    link_powers_to_constellations(ars, union, powers, constellations)
    return headers, fields, powers, constellations, vocab, scope_reasons


# ============================================================ devotion_power + trigger vocab
def build_powers(ars, union, in_scope, axes):
    """
    The probe reported "65 celestial powers" = 65 records carrying `templateAutoCast`. That is
    a count of RECORDS. The records are three populations, and the distinction is banked as
    `power_role` because the trigger is not always carried by the tree node itself:

      52  tree_node    — the devotion tree node carries the autocast directly. Reachable from a
                        constellation's devotionButton -> UI node -> skillName, AND registered
                        in `_devotiontree.dbr`.
      11  buff_half    — the tree node carries NO autocast; it delegates via `buffSkillName` to
                        a buff record which carries it. The PAIR is one celestial power. The
                        tree node is banked in `devotion_node_record`.
       2  unreferenced — `tier3_01f_skill_old` ("Aeon's Hourglass - Time Stop") and
                        `tier3_01f_skill_cooldownreduction` ("Time Dilation"). Verified by a
                        scan of ALL 82,131 union records: ZERO inbound references to either.
                        Retired design iterations left in the database. The live Aeon's
                        Hourglass power is `tier3_01f_skill.dbr` (Skill_RefreshCooldown).

    So the live celestial-power count is 52 + 11 = **63**, and the honest query is
    `COUNT(DISTINCT devotion_node_record) WHERE power_role <> 'unreferenced'` -- never
    `COUNT(*)`, which would read 65 and silently include two dead records.
    """
    tree = ars[union["records/skills/devotion/_devotiontree.dbr"]].read_record(
        "records/skills/devotion/_devotiontree.dbr")
    tree_skills = {v for k, v in tree.items() if k.startswith("skillName") and isinstance(v, str) and v}
    parent_of = {}
    for r in in_scope:
        rec = ars[union[r]].read_record(r)
        for k in ("buffSkillName", "petBonusName", "petSkillName", "skillSecondaryName"):
            v = rec.get(k)
            if isinstance(v, str) and v:
                parent_of.setdefault(v, r)

    powers, vocab = [], {}
    for r in in_scope:
        rel = union[r]
        rec = ars[rel].read_record(r)
        ta = rec.get("templateAutoCast")
        if not (isinstance(ta, str) and ta):
            continue
        ctrl = ars[union[ta]].read_record(ta) if ta in union else {}
        fd = rec.get("FileDescription") or ""
        cons_name, _, pow_name = fd.partition(" - ")
        cd = rec.get("skillCooldownTime")
        cd_is_arr = isinstance(cd, list) and len(cd) > 1
        icd = (cd[0] if isinstance(cd, list) else cd)
        axis, axis_max, _ = axes[r]
        key = ta
        if key not in vocab:
            vocab[key] = dict(autocast_record=ta,
                              trigger_event=ctrl.get("triggerType"),
                              target_frame=ctrl.get("targetType"),
                              proc_chance_pct=float(ctrl["chanceToRun"]) if ctrl.get("chanceToRun") is not None else None,
                              trigger_param=float(ctrl["triggerParam"]) if ctrl.get("triggerParam") else None,
                              auto_target_radius=float(ctrl["autoTargetRadius"]) if ctrl.get("autoTargetRadius") else None,
                              power_count=0, live_power_count=0,
                              source_file=ARCHIVES[union[ta]]["file"] if ta in union else None,
                              source_version=pin_for(union[ta]) if ta in union else None)
        if r in tree_skills:
            role, node = "tree_node", r
        elif r in parent_of and parent_of[r] in tree_skills:
            role, node = "buff_half", parent_of[r]
        else:
            role, node = "unreferenced", None
        vocab[key]["power_count"] += 1
        if role != "unreferenced":
            vocab[key]["live_power_count"] += 1
        powers.append(dict(
            power_record=r, entity_id=r, power_role=role, devotion_node_record=node,
            power_name=pow_name or None, constellation_name=cons_name or None,
            constellation_record=None,                       # filled by the join below
            record_class=rec.get("Class"),
            trigger_event=ctrl.get("triggerType"), target_frame=ctrl.get("targetType"),
            proc_chance_pct=float(ctrl["chanceToRun"]) if ctrl.get("chanceToRun") is not None else None,
            trigger_param=float(ctrl["triggerParam"]) if ctrl.get("triggerParam") else None,
            auto_target_radius=float(ctrl["autoTargetRadius"]) if ctrl.get("autoTargetRadius") else None,
            icd_sec=float(icd) if icd else None,
            icd_is_rank_array=1 if cd_is_arr else 0,
            rank_axis=axis, rank_axis_max=axis_max,
            is_pet_power=1 if (rec.get("isPetDisplayable") is True or rec.get("petBonusName")) else 0,
            autocast_record=ta,
            source_file=ARCHIVES[rel]["file"], source_version=pin_for(rel),
            fidelity_grade=FIDELITY_GRADE, fidelity_basis=FIDELITY_BASIS,
            schema_version=SCHEMA_VERSION))
    return powers, list(vocab.values())


# ============================================================ devotion_constellation
CONS_PREFIX = "records/ui/skills/devotion/constellations/"


def build_constellations(ars, union):
    recs = [r for r in union if r.startswith(CONS_PREFIX)
            and "_background" not in r and r.count("/") == 5]
    out = []
    for r in sorted(recs):
        rel = union[r]
        rec = ars[rel].read_record(r)
        buttons = {k: rec[k] for k in sorted(rec) if k.startswith("devotionButton") and rec[k]}
        links = {k: rec[k] for k in sorted(rec) if k.startswith("devotionLinks") and rec[k] not in (None, "")}
        tier = None
        for b in buttons.values():
            stem = b.rsplit("/", 1)[-1]
            if stem.startswith("tier") and stem[4:5].isdigit():
                tier = int(stem[4:5]); break
        ag = [rec.get(f"affinityGiven{i}") or 0 for i in (1, 2, 3)]
        ar = [rec.get(f"affinityRequired{i}") or 0 for i in (1, 2, 3)]
        out.append(dict(
            constellation_record=r, constellation_name=rec.get("FileDescription"),
            display_tag=rec.get("constellationDisplayTag"), info_tag=rec.get("constellationInfoTag"),
            tier=tier, star_count=len(buttons), celestial_power_count=0,
            affinity_given_1=ag[0], affinity_given_2=ag[1], affinity_given_3=ag[2],
            affinity_given_name_1=rec.get("affinityGivenName1"),
            affinity_given_name_2=rec.get("affinityGivenName2"),
            affinity_given_name_3=rec.get("affinityGivenName3"),
            affinity_required_1=ar[0], affinity_required_2=ar[1], affinity_required_3=ar[2],
            affinity_required_name_1=rec.get("affinityRequiredName1"),
            affinity_required_name_2=rec.get("affinityRequiredName2"),
            affinity_required_name_3=rec.get("affinityRequiredName3"),
            affinity_given_total=sum(ag), affinity_required_total=sum(ar),
            buttons_json=json.dumps(buttons, sort_keys=True),
            links_json=json.dumps(links, sort_keys=True),
            source_file=ARCHIVES[rel]["file"], source_version=pin_for(rel),
            fidelity_grade=FIDELITY_GRADE, fidelity_basis=FIDELITY_BASIS,
            schema_version=SCHEMA_VERSION))
    return out


def link_powers_to_constellations(ars, union, powers, constellations):
    """
    EXACT join, not a name match: constellation.devotionButtonN -> UI node -> `skillName`
    -> behaviour record. The corpus's own prose conflates constellations with powers
    (probe §2.3, 'Bonds of Bysmiel'); a name join would inherit that conflation.
    """
    skill_to_cons = {}
    for c in constellations:
        for btn in json.loads(c["buttons_json"]).values():
            if btn not in union:
                continue
            ui = ars[union[btn]].read_record(btn)
            sn = ui.get("skillName")
            if isinstance(sn, str) and sn:
                skill_to_cons[sn] = c["constellation_record"]
    by_rec = {c["constellation_record"]: c for c in constellations}
    for p in powers:
        # Join on the TREE NODE, not on the record: a buff_half is not itself a tree node,
        # but the power it is half of is. One rule covers both roles.
        cr = skill_to_cons.get(p["devotion_node_record"]) if p["devotion_node_record"] else None
        p["constellation_record"] = cr
        if cr and p["power_role"] != "unreferenced":
            by_rec[cr]["celestial_power_count"] += 1
    return skill_to_cons


# ============================================================ G4 in-pipe asserts
def asserts(headers, fields, powers, constellations, vocab):
    probs = []
    hdr = {h["entity_id"]: h for h in headers}
    for f in fields:
        if f["canon_value"] is None or f["raw_value"] is None:
            probs.append(f"NULL value {f['entity_id']} {f['raw_field']}")
        if f["entity_id"] not in hdr:
            probs.append(f"orphan field row {f['entity_id']}")
        h = hdr.get(f["entity_id"])
        if h and f["rank"] is not None and h["rank_axis"] == "none":
            probs.append(f"ranked row on a rank_axis='none' header: {f['entity_id']} {f['raw_field']}")
    over = [f for f in fields if f["rank"] is not None
            and hdr[f["entity_id"]]["rank_count"] and f["rank"] > hdr[f["entity_id"]]["rank_count"]]
    for p in powers:
        if p["trigger_event"] is None or p["target_frame"] is None or p["proc_chance_pct"] is None:
            probs.append(f"power with incomplete trigger surface: {p['power_record']}")
        if p["constellation_record"] is None and p["power_role"] != "unreferenced":
            probs.append(f"live power with no constellation join: {p['power_record']}")
        if p["constellation_record"] is not None and p["power_role"] == "unreferenced":
            probs.append(f"unreferenced record unexpectedly joined: {p['power_record']}")
        if p["rank_axis"] == "UNRESOLVED":
            probs.append(f"power with unresolved rank axis: {p['power_record']}")
    for c in constellations:
        if not c["constellation_name"]:
            probs.append(f"unnamed constellation {c['constellation_record']}")
    return probs, over


# ============================================================ DDL + apply
DDL = """
CREATE TABLE exact_skill_v2 (
    entity_id          TEXT PRIMARY KEY,           -- corpus kit_id, or the .dbr record_path
    entity_kind        TEXT NOT NULL CHECK (entity_kind IN ('corpus_kit','game_skill')),
    kit_id             TEXT REFERENCES canon_corpus(kit_id),   -- iff entity_kind='corpus_kit'
    game               TEXT NOT NULL,
    display_name       TEXT,
    record_type        TEXT,
    rank_count         INTEGER NOT NULL,
    rank_axis          TEXT NOT NULL CHECK (rank_axis IN ('bought_rank','skill_xp_level','none')),
    rank_axis_source   TEXT,                       -- the EVIDENCE for the axis label
    source_file        TEXT NOT NULL,
    source_version     TEXT,                       -- composite edition pin
    record_path        TEXT NOT NULL,
    ext_json           TEXT,
    name_provenance    TEXT,
    fidelity_grade     TEXT,                       -- era-substrate LAW §4
    fidelity_basis     TEXT,                       -- primary-source-datamine | live-oracle-fixture
    lane               TEXT,
    adapter            TEXT NOT NULL,
    schema_version     TEXT NOT NULL,
    created_date       TEXT NOT NULL DEFAULT (date('now')),
    CHECK (entity_kind <> 'corpus_kit' OR kit_id IS NOT NULL)
);

CREATE TABLE exact_skill_field_v2 (
    entity_id          TEXT NOT NULL REFERENCES exact_skill_v2(entity_id),
    canon_key          TEXT NOT NULL,
    rank               INTEGER,
    canon_value        REAL NOT NULL,
    canon_unit         TEXT,
    raw_field          TEXT NOT NULL,
    raw_value          REAL NOT NULL,
    field_kind         TEXT NOT NULL CHECK (field_kind IN ('rank_array','static')),
    field_family       TEXT,
    is_core            INTEGER NOT NULL DEFAULT 1,
    canon_key_provenance TEXT NOT NULL DEFAULT 'curated'
                         CHECK (canon_key_provenance IN ('curated','mechanical')),
    monotonic_class    INTEGER NOT NULL DEFAULT 0,
    monotonic_dir      TEXT CHECK (monotonic_dir IN ('up','down','flat','none')),
    source_file        TEXT NOT NULL,
    record_path        TEXT NOT NULL,
    schema_version     TEXT NOT NULL,
    created_date       TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (entity_id, canon_key, rank)
);

CREATE TABLE devotion_constellation (
    constellation_record   TEXT PRIMARY KEY,
    constellation_name     TEXT,
    display_tag            TEXT,
    info_tag               TEXT,
    tier                   INTEGER,
    star_count             INTEGER,
    celestial_power_count  INTEGER,
    affinity_given_1 INTEGER, affinity_given_2 INTEGER, affinity_given_3 INTEGER,
    affinity_given_name_1 TEXT, affinity_given_name_2 TEXT, affinity_given_name_3 TEXT,
    affinity_required_1 INTEGER, affinity_required_2 INTEGER, affinity_required_3 INTEGER,
    affinity_required_name_1 TEXT, affinity_required_name_2 TEXT, affinity_required_name_3 TEXT,
    affinity_given_total    INTEGER,
    affinity_required_total INTEGER,
    buttons_json           TEXT,      -- raw devotionButton1..N  (reversibility)
    links_json             TEXT,      -- raw devotionLinks2..N   (tree topology, preserved raw)
    source_file TEXT, source_version TEXT,
    fidelity_grade TEXT, fidelity_basis TEXT,
    schema_version TEXT, created_date TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE devotion_power (
    power_record        TEXT PRIMARY KEY,
    entity_id           TEXT NOT NULL REFERENCES exact_skill_v2(entity_id),
    power_role          TEXT NOT NULL
                          CHECK (power_role IN ('tree_node','buff_half','unreferenced')),
    -- the devotion TREE NODE this power is (tree_node) or belongs to (buff_half). The honest
    -- power count is COUNT(DISTINCT devotion_node_record) WHERE power_role<>'unreferenced'.
    -- FK targets exact_skill: a delegating tree node is a skill record, not a devotion_power row.
    devotion_node_record TEXT REFERENCES exact_skill_v2(entity_id),
    power_name          TEXT,
    constellation_name  TEXT,
    constellation_record TEXT REFERENCES devotion_constellation(constellation_record),
    record_class        TEXT,
    trigger_event       TEXT,      -- triggerType, verbatim
    target_frame        TEXT,      -- targetType, verbatim
    proc_chance_pct     REAL,      -- chanceToRun
    trigger_param       REAL,      -- LowHealth threshold %, else NULL
    auto_target_radius  REAL,
    icd_sec             REAL,      -- skillCooldownTime (level-1 entry when level-scaled)
    icd_is_rank_array   INTEGER,
    rank_axis           TEXT,
    rank_axis_max       INTEGER,
    is_pet_power        INTEGER,
    autocast_record     TEXT,      -- RAW provenance: the controller .dbr, verbatim
    source_file TEXT, source_version TEXT,
    fidelity_grade TEXT, fidelity_basis TEXT,
    schema_version TEXT, created_date TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE devotion_trigger_vocab (
    autocast_record     TEXT PRIMARY KEY,
    trigger_event       TEXT NOT NULL,
    target_frame        TEXT NOT NULL,
    proc_chance_pct     REAL NOT NULL,
    trigger_param       REAL,
    auto_target_radius  REAL,
    power_count         INTEGER NOT NULL,   -- all autocast-bearing records
    live_power_count    INTEGER NOT NULL,   -- power_role='celestial_power' only (the real 52)
    source_file TEXT, source_version TEXT,
    schema_version TEXT, created_date TEXT NOT NULL DEFAULT (date('now'))
);

CREATE INDEX idx_esf2_entity   ON exact_skill_field_v2(entity_id);
CREATE INDEX idx_esf2_canon    ON exact_skill_field_v2(canon_key);
CREATE INDEX idx_esf2_rawfield ON exact_skill_field_v2(raw_field);
CREATE INDEX idx_esf2_family   ON exact_skill_field_v2(field_family);
CREATE INDEX idx_es2_lane      ON exact_skill_v2(lane);
CREATE INDEX idx_es2_kit       ON exact_skill_v2(kit_id);
CREATE INDEX idx_dp_cons       ON devotion_power(constellation_record);
CREATE INDEX idx_dp_trigger    ON devotion_power(trigger_event, target_frame);
"""

VIEWS = """
DROP VIEW IF EXISTS v_exact_skill_by_kit;
DROP VIEW IF EXISTS v_exact_skill_field_by_kit;
CREATE VIEW v_exact_skill_by_kit AS
  SELECT kit_id, game, display_name, record_type, rank_count, source_file, source_version,
         record_path, ext_json, name_provenance, adapter, schema_version, created_date
  FROM exact_skill WHERE entity_kind='corpus_kit';
CREATE VIEW v_exact_skill_field_by_kit AS
  SELECT s.kit_id, f.canon_key, f.rank, f.canon_value, f.canon_unit, f.raw_field, f.raw_value,
         f.field_kind, f.is_core, f.monotonic_class, f.source_file, f.record_path,
         f.schema_version, f.created_date
  FROM exact_skill_field f JOIN exact_skill s ON s.entity_id = f.entity_id
  WHERE s.entity_kind='corpus_kit';
CREATE VIEW v_devotion_proc_spec AS
  SELECT p.power_role, p.constellation_name, p.power_name, p.trigger_event, p.target_frame,
         p.proc_chance_pct, p.trigger_param, p.icd_sec, p.rank_axis_max,
         c.tier, c.affinity_required_total, c.affinity_given_total, p.power_record
  FROM devotion_power p LEFT JOIN devotion_constellation c
    ON c.constellation_record = p.constellation_record;
"""


def apply(headers, fields, powers, constellations, vocab):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak = DB.with_name(DB.name + f".pre-devotion-{ts}-backup")
    shutil.copy2(DB, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    (bak.with_suffix(bak.suffix + ".md5.txt")).write_text(f"{md5}  {bak.name}\n")
    print(f"G2 — BACKUP {bak.name}  md5={md5}")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=OFF")
    cur = con.cursor()

    # IDEMPOTENCY. Re-running against an already-banked DB must reproduce the same rows, not
    # duplicate them or crash on existing DDL. Reverse the prior swap first: drop this run's
    # tables and restore the pre-run `exact_skill*` from the preserved originals.
    have = {r[0] for r in cur.execute("SELECT name FROM sqlite_master").fetchall()}
    if "exact_skill_pre_devotion_20260725" in have:
        print("     prior run detected — reversing its swap before re-landing (idempotent)")
        cur.executescript("""
            DROP VIEW  IF EXISTS v_devotion_proc_spec;
            DROP VIEW  IF EXISTS v_exact_skill_by_kit;
            DROP VIEW  IF EXISTS v_exact_skill_field_by_kit;
            DROP TABLE IF EXISTS devotion_trigger_vocab;
            DROP TABLE IF EXISTS devotion_power;
            DROP TABLE IF EXISTS devotion_constellation;
            DROP TABLE IF EXISTS exact_skill_field;
            DROP TABLE IF EXISTS exact_skill;
            ALTER TABLE exact_skill_pre_devotion_20260725       RENAME TO exact_skill;
            ALTER TABLE exact_skill_field_pre_devotion_20260725 RENAME TO exact_skill_field;
        """)
        cur.execute("DELETE FROM corpus_schema_meta WHERE version=?", (SCHEMA_VERSION,))
    cur.executescript(DDL)

    # --- migrate the existing FoI slice into the v2 shape (entity identity + labelled axis) ---
    cur.execute("""
        INSERT INTO exact_skill_v2
          (entity_id, entity_kind, kit_id, game, display_name, record_type, rank_count,
           rank_axis, rank_axis_source, source_file, source_version, record_path, ext_json,
           name_provenance, fidelity_grade, fidelity_basis, lane, adapter, schema_version, created_date)
        SELECT kit_id, 'corpus_kit', kit_id, game, display_name, record_type, rank_count,
               'bought_rank',
               'skillMaxLevel=16 + skillUltimateLevel=26; no skillExperienceLevels '
               '(verified: 0 of 694 player-class skill records carry one)',
               source_file, source_version, record_path, ext_json, name_provenance,
               'MEASURED', 'primary-source-datamine', 'gd-class-skill', adapter,
               schema_version, created_date
        FROM exact_skill""")
    cur.execute("""
        INSERT INTO exact_skill_field_v2
          (entity_id, canon_key, rank, canon_value, canon_unit, raw_field, raw_value, field_kind,
           field_family, is_core, canon_key_provenance, monotonic_class, monotonic_dir,
           source_file, record_path, schema_version, created_date)
        SELECT kit_id, canon_key, rank, canon_value, canon_unit, raw_field, raw_value, field_kind,
               NULL, is_core, 'curated', monotonic_class,
               CASE WHEN monotonic_class=1 THEN 'up' ELSE 'none' END,
               source_file, record_path, schema_version, created_date
        FROM exact_skill_field""")
    mig_h = cur.execute("SELECT count(*) FROM exact_skill_v2").fetchone()[0]
    mig_f = cur.execute("SELECT count(*) FROM exact_skill_field_v2").fetchone()[0]
    print(f"     migrated prior slice: {mig_h} header / {mig_f} field rows")

    cur.executemany(
        "INSERT INTO exact_skill_v2 (entity_id,entity_kind,kit_id,game,display_name,record_type,"
        "rank_count,rank_axis,rank_axis_source,source_file,source_version,record_path,ext_json,"
        "name_provenance,fidelity_grade,fidelity_basis,lane,adapter,schema_version) VALUES "
        "(:entity_id,:entity_kind,:kit_id,:game,:display_name,:record_type,:rank_count,:rank_axis,"
        ":rank_axis_source,:source_file,:source_version,:record_path,:ext_json,:name_provenance,"
        ":fidelity_grade,:fidelity_basis,:lane,:adapter,:schema_version)", headers)
    cur.executemany(
        "INSERT INTO exact_skill_field_v2 (entity_id,canon_key,rank,canon_value,canon_unit,"
        "raw_field,raw_value,field_kind,field_family,is_core,canon_key_provenance,monotonic_class,"
        "monotonic_dir,source_file,record_path,schema_version) VALUES (:entity_id,:canon_key,:rank,"
        ":canon_value,:canon_unit,:raw_field,:raw_value,:field_kind,:field_family,:is_core,"
        ":canon_key_provenance,:monotonic_class,:monotonic_dir,:source_file,:record_path,"
        f"'{SCHEMA_VERSION}')", fields)

    cur.executemany(
        "INSERT INTO devotion_constellation (constellation_record,constellation_name,display_tag,"
        "info_tag,tier,star_count,celestial_power_count,affinity_given_1,affinity_given_2,"
        "affinity_given_3,affinity_given_name_1,affinity_given_name_2,affinity_given_name_3,"
        "affinity_required_1,affinity_required_2,affinity_required_3,affinity_required_name_1,"
        "affinity_required_name_2,affinity_required_name_3,affinity_given_total,"
        "affinity_required_total,buttons_json,links_json,source_file,source_version,"
        "fidelity_grade,fidelity_basis,schema_version) VALUES (:constellation_record,"
        ":constellation_name,:display_tag,:info_tag,:tier,:star_count,:celestial_power_count,"
        ":affinity_given_1,:affinity_given_2,:affinity_given_3,:affinity_given_name_1,"
        ":affinity_given_name_2,:affinity_given_name_3,:affinity_required_1,:affinity_required_2,"
        ":affinity_required_3,:affinity_required_name_1,:affinity_required_name_2,"
        ":affinity_required_name_3,:affinity_given_total,:affinity_required_total,:buttons_json,"
        ":links_json,:source_file,:source_version,:fidelity_grade,:fidelity_basis,:schema_version)",
        constellations)
    cur.executemany(
        "INSERT INTO devotion_power (power_record,entity_id,power_role,devotion_node_record,"
        "power_name,constellation_name,"
        "constellation_record,record_class,trigger_event,target_frame,proc_chance_pct,"
        "trigger_param,auto_target_radius,icd_sec,icd_is_rank_array,rank_axis,rank_axis_max,"
        "is_pet_power,autocast_record,source_file,source_version,fidelity_grade,fidelity_basis,"
        "schema_version) VALUES (:power_record,:entity_id,:power_role,:devotion_node_record,"
        ":power_name,:constellation_name,"
        ":constellation_record,:record_class,:trigger_event,:target_frame,:proc_chance_pct,"
        ":trigger_param,:auto_target_radius,:icd_sec,:icd_is_rank_array,:rank_axis,:rank_axis_max,"
        ":is_pet_power,:autocast_record,:source_file,:source_version,:fidelity_grade,"
        ":fidelity_basis,:schema_version)", powers)
    for v in vocab:
        v["schema_version"] = SCHEMA_VERSION
    cur.executemany(
        "INSERT INTO devotion_trigger_vocab (autocast_record,trigger_event,target_frame,"
        "proc_chance_pct,trigger_param,auto_target_radius,power_count,live_power_count,source_file,"
        "source_version,schema_version) VALUES (:autocast_record,:trigger_event,:target_frame,"
        ":proc_chance_pct,:trigger_param,:auto_target_radius,:power_count,:live_power_count,"
        ":source_file,:source_version,:schema_version)", vocab)

    # --- swap v2 into place; the old tables are RENAMED, not dropped (reversibility) ---
    cur.executescript("""
        ALTER TABLE exact_skill        RENAME TO exact_skill_pre_devotion_20260725;
        ALTER TABLE exact_skill_field  RENAME TO exact_skill_field_pre_devotion_20260725;
        ALTER TABLE exact_skill_v2       RENAME TO exact_skill;
        ALTER TABLE exact_skill_field_v2 RENAME TO exact_skill_field;
    """)
    cur.executescript(VIEWS)
    cur.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                (SCHEMA_VERSION, datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "GD devotion payload bank (elrond, gandalf GD-program commission). "
                 "exact_skill/exact_skill_field re-identified on entity_id+entity_kind with a "
                 "MANDATORY rank_axis label; new devotion_power / devotion_constellation / "
                 "devotion_trigger_vocab. Prior tables preserved as *_pre_devotion_20260725. "
                 f"Fidelity {FIDELITY_GRADE}/{FIDELITY_BASIS}; edition {EDITION}."))
    con.commit()
    return con, bak, md5


# ============================================================ G5 read-back verify
def verify_readback(con):
    cur = con.cursor()
    print("\nG5 — READ-BACK BYTE-MATCH (float32-canonical; never tolerance-fudged)")
    bad = 0
    for (rp, rf, rank), exp in sorted(ANCHORS_FIELD.items()):
        if rank is None:
            row = cur.execute("SELECT raw_value FROM exact_skill_field WHERE entity_id=? AND "
                              "raw_field=? AND rank IS NULL", (rp, rf)).fetchone()
        else:
            row = cur.execute("SELECT raw_value FROM exact_skill_field WHERE entity_id=? AND "
                              "raw_field=? AND rank=?", (rp, rf, rank)).fetchone()
        got = row[0] if row else None
        ok = row is not None and f32(got) == f32(exp)
        bad += 0 if ok else 1
        print(f"    {'PASS' if ok else 'FAIL'} {rf:26s} rank={str(rank):4s} exp={exp} got={got}")
    for pr, exp in ANCHORS_POWER.items():
        row = cur.execute("SELECT power_name,constellation_name,trigger_event,target_frame,"
                          "proc_chance_pct,auto_target_radius,icd_sec FROM devotion_power "
                          "WHERE power_record=?", (pr,)).fetchone()
        got = dict(zip(["power_name", "constellation_name", "trigger_event", "target_frame",
                        "proc_chance_pct", "auto_target_radius", "icd_sec"], row or []))
        for k, v in exp.items():
            g = got.get(k)
            ok = (f32(g) == f32(v)) if isinstance(v, float) else (g == v)
            bad += 0 if ok else 1
            print(f"    {'PASS' if ok else 'FAIL'} devotion_power.{k:20s} exp={v} got={g}")
    print(f"    integrity_check    : {cur.execute('PRAGMA integrity_check').fetchone()[0]}")
    fk = cur.execute("PRAGMA foreign_key_check").fetchall()
    print(f"    foreign_key_check  : {'clean' if not fk else fk[:5]}")
    return bad


# ============================================================ post-bank census refinement
def census_refinement(con):
    """
    Probe §4.2 obligation, now discharged: how many corpus kits mention a devotion CONSTELLATION
    vs a celestial POWER. The census's 18-kit 'devotion proc' count was soft because kit prose
    conflates the two. This makes the split reproducible from banked structure.
    """
    cur = con.cursor()
    powers = {r[0]: r[1] for r in cur.execute(
        "SELECT power_name, constellation_name FROM devotion_power "
        "WHERE power_name IS NOT NULL AND power_role <> 'unreferenced'")}
    cons = [r[0] for r in cur.execute(
        "SELECT constellation_name FROM devotion_constellation WHERE constellation_name IS NOT NULL")]
    # SCOPE GUARD, found the hard way on the first run. Many GD constellation names are generic
    # ARPG nouns -- Assassin, Berserker, Hammer, Tempest, Spider, Viper, Widow, Huntress, Anvil.
    # An unscoped substring scan matched 48 POE/TL/TQ kits that have nothing to do with devotions.
    # The census population is the GD lane, so the scan is scoped to GD kits and the ambiguity is
    # recorded rather than silently absorbed.
    gd_kits = {r[0] for r in cur.execute("SELECT kit_id FROM canon_corpus WHERE game='gd'")}
    generic = sorted(n for n in cons if n and " " not in n and "'" not in n)
    # `canon_corpus` is INCLUDED. The first pass scanned only kit_* tables and missed
    # `canon_corpus.fidelity_notes`, which is where the probe's own worked example lives
    # ("Twin Fangs devotion proc named ... but payload behavior unfetched").
    # NOTE: the table list is MATERIALIZED before the PRAGMA loop. Iterating a cursor while
    # re-executing on the SAME cursor silently truncates the outer iteration -- a bug inherited
    # from the first draft that made this scan miss most tables and under-report the counts.
    table_names = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND "
        "(name LIKE 'kit_%' OR name='canon_corpus')").fetchall()]
    tables = {}
    for t in table_names:
        info = cur.execute(f"PRAGMA table_info({t})").fetchall()
        if "kit_id" not in [c[1] for c in info]:
            continue
        tables[t] = [c[1] for c in info if c[2].upper().startswith("TEXT") or c[2] == ""]

    # WORD-BOUNDARY matching, not substring. The first pass credited
    # `gd-ravenous-earth-oppressor` with the constellation "Raven" -- because "Raven" is a
    # substring of "Ravenous". A naive `in` test manufactures devotion mentions out of ordinary
    # English, which is exactly the kind of soft count this refinement exists to retire.
    def rx(name):
        return re.compile(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z'\u2019])")
    pow_rx = {pn: rx(pn) for pn in powers if len(pn) > 3}
    con_rx = {cn: rx(cn) for cn in cons if cn and len(cn) > 3}

    hits_power, hits_cons = collections.defaultdict(set), collections.defaultdict(set)
    for t, cols in tables.items():
        for c in cols:
            if c == "kit_id":
                continue
            try:
                rows = cur.execute(f"SELECT kit_id, {c} FROM {t} WHERE {c} IS NOT NULL").fetchall()
            except sqlite3.Error:
                continue
            for kit, val in rows:
                if kit not in gd_kits or not isinstance(val, str) or len(val) < 3:
                    continue
                for pn, r in pow_rx.items():
                    if r.search(val):
                        hits_power[kit].add(pn)
                for cn, r in con_rx.items():
                    if r.search(val):
                        hits_cons[kit].add(cn)
    both = set(hits_power) | set(hits_cons)
    print("\nCENSUS REFINEMENT (probe §4.2 — 'any kit-count over devotion procs is soft')")
    print(f"    scan scoped to {len(gd_kits)} GD kits (see scope-guard note in source)")
    print(f"    single-word constellation names, ambiguous outside the GD lane: {generic}")
    print(f"    kits naming a CELESTIAL POWER      : {len(hits_power)}")
    print(f"    kits naming a CONSTELLATION        : {len(hits_cons)}")
    print(f"    kits naming EITHER (union)         : {len(both)}")
    print(f"    kits naming ONLY a constellation   : {len(set(hits_cons) - set(hits_power))}")
    for k in sorted(hits_power):
        print(f"      POWER  {k:38s} {sorted(hits_power[k])}")
    for k in sorted(set(hits_cons) - set(hits_power)):
        print(f"      CONS*  {k:38s} {sorted(hits_cons[k])}   <- constellation-only mention")
    return len(hits_power), len(hits_cons), len(both)


# ============================================================ main
def main():
    mode = "apply"
    if "--verify-only" in sys.argv:
        mode = "verify"
    elif "--dry-run" in sys.argv:
        mode = "dry"
    print("=" * 78)
    print(f"GD DEVOTION PAYLOAD BANK — {SCHEMA_VERSION}   mode={mode}")
    print("=" * 78)
    verify_edition()
    ars, union = load_union()
    headers, fields, powers, constellations, vocab, scope = build(ars, union)

    print("L1 RECORD SCOPE :", dict(scope))
    axis_hist = collections.Counter(h["rank_axis"] for h in headers)
    print("RANK AXIS       :", dict(axis_hist))
    print(f"ROWS            : header={len(headers)}  field={len(fields)}  "
          f"power={len(powers)}  constellation={len(constellations)}  trigger_vocab={len(vocab)}")
    print(f"                  is_core 1/0 = {sum(f['is_core'] for f in fields)}/"
          f"{len(fields)-sum(f['is_core'] for f in fields)}; "
          f"canon_key curated/mechanical = "
          f"{sum(1 for f in fields if f['canon_key_provenance']=='curated')}/"
          f"{sum(1 for f in fields if f['canon_key_provenance']=='mechanical')}")
    roles = collections.Counter(p["power_role"] for p in powers)
    live = [p for p in powers if p["power_role"] != "unreferenced"]
    n_live = len({p["devotion_node_record"] for p in live})
    print("POWER ROLE      :", dict(roles),
          f"  <- the probe's '65 celestial powers' is 65 RECORDS; "
          f"distinct live tree nodes = {n_live}")
    for label, pop in (("ALL 65 records", powers), (f"LIVE {n_live} powers", live)):
        ev = collections.Counter(p["trigger_event"] for p in pop)
        tf = collections.Counter(p["target_frame"] for p in pop)
        ch = collections.Counter(p["proc_chance_pct"] for p in pop)
        print(f"TRIGGER ENUM [{label}] : {len(ev)}x{len(tf)}x{len(ch)} "
              f"(events x frames x chances)")
        print(f"    events  {dict(ev)}")
        print(f"    frames  {dict(tf)}")
        print(f"    chances {dict(sorted(ch.items()))}")
        print(f"    realized combos {len({(p['trigger_event'],p['target_frame'],p['proc_chance_pct']) for p in pop})}"
              f" of {len(ev)*len(tf)*len(ch)} theoretical; "
              f"ICD present on {sum(1 for p in pop if p['icd_sec'])}/{len(pop)}")

    probs, over = asserts(headers, fields, powers, constellations, vocab)
    print(f"\nG4 IN-PIPE ASSERTS: {'GREEN' if not probs else str(len(probs)) + ' PROBLEMS'}")
    for p in probs[:20]:
        print("    ", p)
    if over:
        print(f"    NOTE {len(over)} rows have rank > rank_count (authored arrays longer than the "
              f"power's own XP table). Banked verbatim per reversibility; listed:")
        for f in over[:10]:
            print(f"      {f['entity_id']} {f['raw_field']} rank={f['rank']}")
    if probs:
        raise SystemExit("HALT — in-pipe asserts failed. Nothing banked.")
    if mode != "apply":
        print("\nNO WRITES (mode=%s)." % mode)
        return

    con, bak, md5 = apply(headers, fields, powers, constellations, vocab)
    bad = verify_readback(con)
    if bad:
        raise SystemExit(f"HALT — {bad} read-back anchors FAILED. Restore from {bak.name}.")
    census_refinement(con)
    con.close()
    print(f"\nAPPLIED. backup={bak.name} md5={md5}")


if __name__ == "__main__":
    main()
