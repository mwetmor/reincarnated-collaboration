#!/usr/bin/env python3
"""KC2 MODEL-COMPLETION RUN · Wave 1 · piece D-2 -- REUSE GATES FOR THE SILENT SPECIAL SLOTS.

READ-ONLY on the vendor corpus and on the sim substrate. Emits the per-slot gate table.

THE SLOT SET is reconstructed by replaying `threat.load_profiles`'s OWN filter chain against
`data/kc2/pm2_tg2_attack_damage.csv` (status == OK, rank_grade == MEASURED, exact-duplicate
dedup), so the enumerated slots are exactly the slots the sim builds -- not a re-derivation.
The suppression predicate is `threat.py:850` verbatim.

THE GATE is chased on the OWNER CREATURE record -- `specialAttack{N}Chance|Delay|Timeout|Range`,
declared by GRIM DAWN'S OWN TEMPLATE `templatebase/monsterskillmanager.tpl` -- and on the SKILL
record (`skillCooldownTime` + the timing family). The `Range` enum is resolved to METRES by the
same creature's `{short|medium|long}Range{Min|Max}`; Lap F closed DB-length-unit == metre with no
conversion factor. Values verbatim; no fitted constants; an absent field is reported ABSENT.

READING: `s2_lib.E3.merged` (last-wins FIELD merge across the eight-archive overlay), which is the
reading `pm2_tg2_attack_slots.csv` was extracted under -- so these rows are drop-in for that CSV.
The alternative whole-record-replacement reading (`gamora ... .E3.winner`) is checked and is INERT
on every one of these slots; the check is emitted in the summary.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import pathlib
import re
import sys

ROSTER_LAP = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
              "notes/2026-08-12-kc2-roster-decode-completion")
sys.path.insert(0, ROSTER_LAP)
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts")
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")

from s2_lib import E3 as MERGED                                       # noqa: E402
from gamora_kc2_c1_closure_ed3_2026_08_08 import E3 as WINNER         # noqa: E402

DATA = pathlib.Path("/Users/admin/Games/reincarnated-engine/data/kc2")
OUT = pathlib.Path(__file__).resolve().parent
ANM = json.load(open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json"))
FPS = 30.0
PFX = ("unarmed", "sHanded", "dHanded", "dualRanged", "staff", "ranged1h",
       "ranged2h", "axe2h", "mace2h", "sword2h", "spear2h")

PREFIX = {"special1": "specialAttack", "special2": "specialAttack2",
          "special3": "specialAttack3", "special4": "specialAttack4",
          "special5": "specialAttack5"}

SKILL_TIMING = ("skillCooldownTime", "skillActiveDuration", "skillChargeDuration",
                "skillChargeLevel", "skillTargetRadius", "skillTargetNumber",
                "skillTargetAngle", "skillMaxLevel")

#: the metre annulus each `specialAttack{N}Range` enum value names, read off the SAME creature.
BAND_FIELDS = {"ShortRange": ("shortRangeMin", "shortRangeMax"),
               "MediumRange": ("mediumRangeMin", "mediumRangeMax"),
               "LongRange": ("longRangeMin", "longRangeMax")}


def _s(v):
    if isinstance(v, list):
        v = v[0] if v else None
    return "" if v is None else v


def _n(v):
    v = _s(v)
    if v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def akey(ref):
    r = (ref or "").lower().replace("\\", "/")
    return r[len("creatures/"):] if r.startswith("creatures/") else r


def frames(ref):
    e = ANM.get(akey(ref))
    return e["frames"] if e else None


# ── 1 · replay the sim loader's filter chain (threat.py:745-760, 845-852) ──────────────────────
def slot_set():
    rows = list(csv.DictReader(open(DATA / "pm2_tg2_attack_damage.csv", newline="")))
    seen, by = set(), {}
    for r in rows:
        if r["status"] != "OK" or r["rank_grade"] != "MEASURED":
            continue
        key = (r["actor_kind"], r["record"], r["surface"], r["slot"], r["tree_index"],
               r["skill"], r["damage_type"], r["kind"], r["min"], r["max"])
        if key in seen:
            continue
        seen.add(key)
        by.setdefault((r["actor_kind"], r["record"]), []).append(r)
    meta = {(r["record"], r["slot"]) for r in
            csv.DictReader(open(DATA / "pm2_tg2_attack_slots.csv", newline=""))}
    out = []
    for (kind, record), rs in sorted(by.items()):
        if kind != "pet":
            continue
        per = {}
        for r in rs:
            if r["surface"] == "slot":
                per.setdefault(r["slot"], []).append(r)
        for slot in ("special1", "special2", "special3", "special4", "special5"):
            grp = per.get(slot)
            if not grp:
                continue
            cd = _n(grp[0].get("skill_cooldown_s"))
            has_meta = (record, slot) in meta
            out.append(dict(pet_body=record, slot=slot, skill=grp[0]["skill"],
                            root_skill=(grp[0].get("root_skill") or grp[0]["skill"]),
                            nest_depth=grp[0].get("nest_depth", ""),
                            skill_class=grp[0]["skill_class"],
                            display_name=grp[0].get("display_name", ""),
                            sim_skill_cooldown_s=cd, sim_has_slot_meta=has_meta,
                            sim_fires=bool(has_meta or cd), n_damage_rows=len(grp)))
    return out


def pet_owners():
    own = collections.defaultdict(set)
    for r in csv.DictReader(open(DATA / "pm2_tg2_pet_chain.csv", newline="")):
        if r.get("is_threat_actor", "").strip() not in ("True", "true", "1"):
            continue
        own[r["pet_record"]].add(r["owner_record"].rsplit("/", 1)[-1])
    return own


# ── 2 · animation binding (lineage: s2_extract.py, unchanged in semantics) ─────────────────────
def anim_refmap(body):
    tblp = body.get("charAnimationTableName")
    trec, _ = MERGED.merged(tblp) if isinstance(tblp, str) else (None, None)
    if not trec:
        return {}, None
    refmap = {}
    for k, v in trec.items():
        m = re.match(r"^([A-Za-z0-9]+?)SpecialAnimRef(\d+)$", k)
        if m and isinstance(v, str):
            an = trec.get(f"{m.group(1)}SpecialAnim{m.group(2)}")
            if isinstance(an, str) and an.lower().endswith(".anm"):
                refmap.setdefault(v, {}).setdefault(m.group(1), an)
    for p in PFX:
        for nm, fld in (("__spell__", p + "SpellAttackAnim"),
                        ("__buffself__", p + "BuffSelfAnim1"),
                        ("__buffother__", p + "BuffOtherAnim1"),
                        ("__channel__", p + "ChannelAnim")):
            an = trec.get(fld)
            if isinstance(an, str):
                refmap.setdefault(nm, {}).setdefault(p, an)
    return refmap, trec


def anim_for(skill, refmap):
    san = skill.get("skillSpecialAnimationName")
    anmref = anmfr = None
    if isinstance(san, str) and san:
        m = refmap.get(san)
        if m:
            anmref = m.get("unarmed") or list(m.values())[0]
            anmfr = frames(anmref)
            grade = "DIRECT-REF" if anmfr else "REF-RESOLVED-ANM-MISSING"
        else:
            grade = "REF-UNSATISFIED-BY-TABLE"
    else:
        grade = "NO-REF"
    fbref = None
    if anmfr is None:
        cls = str(skill.get("Class", "") or "")
        fam = "__spell__" if not cls.startswith(
            ("Skill_AttackWeapon", "Skill_WPAttack", "Skill_WeaponPool")) else None
        m = refmap.get(fam) if fam else None
        if m:
            fbref = m.get("unarmed") or list(m.values())[0]
    fbfr = frames(fbref) if fbref else None
    return dict(anim_binding_grade=grade,
                special_anm=(anmref or "").rsplit("/", 1)[-1],
                special_anm_frames=anmfr or "",
                special_anm_dur_s=round(anmfr / FPS, 4) if anmfr else "",
                fallback_anm=(fbref or "").rsplit("/", 1)[-1],
                fallback_anm_dur_s=round(fbfr / FPS, 4) if fbfr else "")


def main() -> None:
    slots, owners = slot_set(), pet_owners()
    rows, field_census, reading_diffs = [], collections.Counter(), 0
    for s in slots:
        body, _arcs = MERGED.merged(s["pet_body"])
        body = body or {}
        wbody, _w = WINNER.winner(s["pet_body"])
        skill, _sa = MERGED.merged(s["skill"])
        skill = skill or {}
        pre = PREFIX[s["slot"]]
        refmap, _tr = anim_refmap(body)

        for k in body:
            if k.lower().startswith("specialattack") and "sound" not in k.lower():
                field_census[k] += 1
        for f in ("Chance", "Delay", "Timeout", "Range", "SkillName"):
            if str(_s(body.get(pre + f))) != str(_s((wbody or {}).get(pre + f))):
                reading_diffs += 1

        band = str(_s(body.get(pre + "Range")))
        if band in BAND_FIELDS:
            lo = _n(body.get(BAND_FIELDS[band][0]))
            hi = _n(body.get(BAND_FIELDS[band][1]))
        elif band == "AnyRange":
            lo, hi = 0.0, _n(body.get("longRangeMax"))
        else:
            lo = hi = None

        r = dict(
            pet_body=s["pet_body"], slot=s["slot"], display_name=s["display_name"],
            skill=s["skill"], root_skill=s["root_skill"], nest_depth=s["nest_depth"],
            skill_class=s["skill_class"], n_damage_rows=s["n_damage_rows"],
            summoned_by="|".join(sorted(owners.get(s["pet_body"], ()))) or "UNLISTED",
            sim_fires_today="YES" if s["sim_fires"] else "NO",
            sim_basis=("skill_cooldown_s" if s["sim_skill_cooldown_s"] else
                       ("slot_meta" if s["sim_has_slot_meta"] else "SUPPRESSED")),
            # ── the creature-record gate: THE DECODE ──
            slot_field=pre + "SkillName",
            dbr_skill_name=str(_s(body.get(pre + "SkillName"))).lower().replace("\\", "/"),
            chance_pct=_s(body.get(pre + "Chance")),
            delay_s=_s(body.get(pre + "Delay")),
            timeout_s=_s(body.get(pre + "Timeout")),
            range_band=band,
            range_gate_min_m="" if lo is None else lo,
            range_gate_max_m="" if hi is None else hi,
            short_range_min_m=_s(body.get("shortRangeMin")),
            short_range_max_m=_s(body.get("shortRangeMax")),
            medium_range_min_m=_s(body.get("mediumRangeMin")),
            medium_range_max_m=_s(body.get("mediumRangeMax")),
            long_range_min_m=_s(body.get("longRangeMin")),
            long_range_max_m=_s(body.get("longRangeMax")),
            character_attack_speed=_s(body.get("characterAttackSpeed")),
            body_class=_s(body.get("Class")),
        )
        for f in SKILL_TIMING:
            r[f] = _s(skill.get(f))
        r.update(anim_for(skill, refmap))

        # ⚑ the join is against the ROOT skill: on 5 slots the damage-bearing record is a NESTED
        #   `*_buff.dbr` reached via `buffSkillName`, while the slot field names its root. The GATE
        #   belongs to the SLOT, so root is the correct join key; `skill` alone reports 5 false
        #   failures. Both are emitted so the grain is visible.
        joined = (r["dbr_skill_name"] in (s["skill"].lower(), s["root_skill"].lower()))
        r["slot_join_ok"] = "YES" if joined else "NO"
        r["join_key"] = ("skill" if r["dbr_skill_name"] == s["skill"].lower()
                         else ("root_skill" if joined else "NONE"))
        gate_fields = [k for k in ("chance_pct", "delay_s", "timeout_s", "range_band")
                       if r[k] != ""]
        if r["skillCooldownTime"] != "":
            gate_fields.append("skillCooldownTime")
        r["gate_fields_present"] = "|".join(gate_fields)
        if not joined:
            r["verdict"] = "SLOT-JOIN-FAILED"
        elif r["delay_s"] != "":
            r["verdict"] = "DECODED"
        elif gate_fields:
            r["verdict"] = "DECODED-PARTIAL"
        else:
            r["verdict"] = "UNDECODABLE-FROM-SUBSTRATE"
        rows.append(r)

    cols = list(rows[0].keys())
    p = OUT / "d2_special_slot_gates.csv"
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    def cnt(pred):
        return sum(1 for r in rows if pred(r))

    summary = dict(
        slots_total=len(rows),
        distinct_skills=len({r["skill"] for r in rows}),
        distinct_bodies=len({r["pet_body"] for r in rows}),
        sim_fires_today=cnt(lambda r: r["sim_fires_today"] == "YES"),
        sim_suppressed_today=cnt(lambda r: r["sim_fires_today"] == "NO"),
        verdicts=dict(collections.Counter(r["verdict"] for r in rows)),
        verdicts_on_suppressed=dict(collections.Counter(
            r["verdict"] for r in rows if r["sim_fires_today"] == "NO")),
        slot_join_ok=cnt(lambda r: r["slot_join_ok"] == "YES"),
        join_key=dict(collections.Counter(r["join_key"] for r in rows)),
        delay_present=cnt(lambda r: r["delay_s"] != ""),
        chance_present=cnt(lambda r: r["chance_pct"] != ""),
        timeout_present=cnt(lambda r: r["timeout_s"] != ""),
        range_band_present=cnt(lambda r: r["range_band"] != ""),
        range_gate_resolved_to_metres=cnt(lambda r: r["range_gate_max_m"] != ""),
        skillCooldownTime_present=cnt(lambda r: r["skillCooldownTime"] != ""),
        skillActiveDuration_present=cnt(lambda r: r["skillActiveDuration"] != ""),
        skillChargeDuration_present=cnt(lambda r: r["skillChargeDuration"] != ""),
        anim_dur_measured=cnt(lambda r: r["special_anm_dur_s"] != ""),
        anim_fallback_only=cnt(lambda r: r["special_anm_dur_s"] == ""
                               and r["fallback_anm_dur_s"] != ""),
        anim_no_timing=cnt(lambda r: r["special_anm_dur_s"] == ""
                           and r["fallback_anm_dur_s"] == ""),
        delay_vs_skillcooldown_disagree=cnt(
            lambda r: r["skillCooldownTime"] != "" and r["delay_s"] != ""
            and abs(float(r["skillCooldownTime"]) - float(r["delay_s"])) > 1e-6),
        merged_vs_winner_reading_diffs=reading_diffs,
        creature_field_census=dict(sorted(field_census.items())),
        csv_digest=hashlib.sha256(p.read_bytes()).hexdigest(),
    )
    (OUT / "d2_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
