#!/usr/bin/env python3
"""
2026-07-25-devotion-payload-probe.py — READ-ONLY probe of the GD devotion/constellation lane.

COMMISSION: gandalf, 2026-07-25 (GD program). Follow-on to the player-mechanism census
(`2026-07-25-gd-player-mechanism-census.md` §5.1 — "devotion proc PAYLOADS, the biggest hole").
Answers Q1 (held?) / Q2 (readable?) / Q3 (sizing?).

READ-ONLY GUARANTEE: opens .arz files with Path.read_bytes(); opens corpus.db not at all.
NO WRITES of any kind. Reuses the width-one-proven parser from
`agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (ArzArchive only —
build_rows / DB apply path is NOT imported-and-run).

RUN:  python3 agentic_orchestration/elrond/notes/2026-07-25-devotion-payload-probe.py
"""
import sys, pathlib, collections, re

REPO = pathlib.Path(__file__).resolve().parents[2]          # agentic_orchestration/
sys.path.insert(0, str(REPO / "research" / "scripts"))
from gd_arz_adapter_2026_07_24 import ArzArchive            # noqa: E402

BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCH = ["database/database.arz", "gdx1/database/GDX1.arz",
        "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]

# Boilerplate = engine scaffolding, not devotion behaviour. Excluded from the payload row estimate.
BOILER = {"skillExperienceLevels", "skillTemplates", "skillBlackList", "characterRacialProfile",
          "skillUpBitmapName", "skillDownBitmapName", "skillBaseDescription", "templateName",
          "Class", "skillDisplayName", "bitmapName", "soundNameDown"}
# Payload = what the census asked for: trigger, ICD, damage/effect, pet-vs-self.
PAY = re.compile(r"^(offensive|defensive|retaliation|character|skillCooldown|skillActive|skillTarget|"
                 r"skillProjectile|projectile|weaponDamagePct|skillManaCost|skillMaxLevel|skillUltimate|"
                 r"templateAutoCast|petLimit|spawn|buffSkillName|petSkillName|petBonusName|conversion|"
                 r"racialBonus|targetingMode|distanceProfile|isPet)")

ars = {a: ArzArchive(BASE / a) for a in ARCH}
union = {}                                    # record_path -> archive (later archives override base)
for a in ARCH:
    for r in ars[a].records:
        union[r] = a
read = lambda p: ars[union[p]].read_record(p)


def q1_inventory():
    print("=" * 78, "\nQ1 — HELD? devotion record inventory per archive\n")
    for a in ARCH:
        ar = ars[a]
        dev = [r for r in ar.records if "devotion" in r.lower()]
        print(f"  {a:32s} {len(ar.records):6d} records  {len(dev):5d} devotion-path")
    print(f"  {'UNION (dedup)':32s} {len(union):6d} records  "
          f"{len([r for r in union if 'devotion' in r.lower()]):5d} devotion-path")


def q2_decode():
    print("=" * 78, "\nQ2 — READABLE? one fully-decoded record + its trigger controller\n")
    p = "records/skills/devotion/tier1_01e_skill.dbr"
    rec = read(p)
    print(f"  RECORD {p}  (archive: {union[p]}, rtype: {ars[union[p]].records[p]['rtype']})")
    print(f"  {len(rec)} fields decoded; non-default shown:\n")
    for k, v in sorted(rec.items()):
        keep = isinstance(v, list) or (isinstance(v, str) and v) or \
               (not isinstance(v, bool) and isinstance(v, (int, float)) and v != 0) or v is True
        if keep:
            print(f"    {k} = {v!r}")
    tc = rec["templateAutoCast"]
    print(f"\n  TRIGGER CONTROLLER {tc}")
    for k, v in sorted(read(tc).items()):
        print(f"    {k} = {v!r}")


def q3_sizing():
    print("=" * 78, "\nQ3 — SIZING\n")
    skl = [r for r in union if r.startswith("records/skills/devotion/")]
    rows = hdrs = procs = withcd = petlane = 0
    fieldnames, consts, triggers = collections.Counter(), set(), collections.Counter()
    for r in skl:
        try:
            rec = read(r)
        except Exception:
            continue
        hdrs += 1
        fd = rec.get("FileDescription")
        if isinstance(fd, str) and fd:
            consts.add(fd.split(" - ")[0])
        ta = rec.get("templateAutoCast")
        if isinstance(ta, str) and ta:
            procs += 1; triggers[ta] += 1
        if rec.get("skillCooldownTime"):
            withcd += 1
        if rec.get("isPetDisplayable") is True or "petBonusName" in rec or "/pets/" in r:
            petlane += 1
        for k, v in rec.items():
            if k in BOILER or not PAY.match(k):
                continue
            if isinstance(v, bool):
                if v: rows += 1; fieldnames[k] += 1
            elif isinstance(v, list):
                if [x for x in v if x not in (0, 0.0, False, "")]:
                    rows += len(v); fieldnames[k] += 1
            elif isinstance(v, (int, float)) and v != 0:
                rows += 1; fieldnames[k] += 1
            elif isinstance(v, str) and v:
                rows += 1; fieldnames[k] += 1
    cons = [r for r in union
            if r.startswith("records/ui/skills/devotion/constellations/")
            and "_background" not in r and r.count("/") == 5]
    print(f"  exact_skill HEADER rows (devotion skill records) : {hdrs}")
    print(f"    of which CELESTIAL POWERS (templateAutoCast)   : {procs}")
    print(f"    with explicit ICD (skillCooldownTime)          : {withcd}")
    print(f"    pet-lane flagged                               : {petlane}")
    print(f"  CONSTELLATION records (affinity/point-cost lane)  : {len(cons)}")
    print(f"  distinct constellation names (in-record)         : {len(consts)}")
    print(f"  PAYLOAD exact_skill_field ROWS (boilerplate excl) : {rows}")
    print(f"  distinct payload field names                     : {len(fieldnames)}")
    print(f"  distinct TRIGGER templates (proc vocabulary)      : {len(triggers)}")
    for k, v in triggers.most_common():
        print(f"      {v:4d}  {k}")


if __name__ == "__main__":
    q1_inventory(); q2_decode(); q3_sizing()
