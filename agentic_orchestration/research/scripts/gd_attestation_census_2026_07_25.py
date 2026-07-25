#!/usr/bin/env python3
"""
gd_attestation_census_2026_07_25.py — GD two-sided attestation census (ANALYSIS ONLY, read-only).

DISPATCH
    `agentic_orchestration/dispatches/2026-07-25-elrond-gd-attestation-scope-census.md`
    Operationalizes Matt's 2026-07-25 scope principle: remove any GD metric which no corpus build
    exercises AND no GD monster needs.

WHAT THIS DOES
    Reads Edition-II .arz (TRUE SOURCE) + grimtools raw JS (corroborating) + corpus.db (player side).
    Emits the attestation counts backing `elrond/notes/2026-07-25-gd-attestation-scope-census.md`.
    NO WRITES ANYWHERE. corpus.db is opened read-only (SELECT only); .arz files are opened read-only.

REUSES the productionized TQIT .arz parser from `gd_arz_adapter_2026_07_24.py` (ArzArchive).

COMBAT-RELEVANCE FILTER PREDICATE (§2 of the note; stated here so the code IS the audit trail)
    A .arz record R is a COMBAT-RELEVANT MONSTER iff ALL hold:
      F1  R's record-table type == 'Monster'
      F2  NOT R.path.startswith('records/sandbox/')
      F3  NOT R.path.startswith('records/creatures/npcs/')
      F4  NOT R.path.startswith('records/creatures/ambient/')
      F5  'testdummy' not in R.path
      F6  R.hiddenFromCombat is not True
      F7  R.invincible is not True
      F8  R.targetable is not False
      F9  R.defaultTeamMajor != 'TeamMajor_Human'
    Yields N = 3,207 of 4,066 Monster records.

NON-INERT (the "non-default" operationalization; see note §2.3)
    numeric  -> != 0
    bool     -> is True
    string   -> not in {NeverFlee, NeverRoam, NeverUseSkill, None, ''}
    list     -> any element != 0
    absent   -> inert (template default inherited)

USAGE
    python3 gd_attestation_census_2026_07_25.py            # full census to stdout
"""
import sys, pathlib, collections, sqlite3, re, statistics as st

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gd_arz_adapter_2026_07_24 import ArzArchive          # noqa: E402

VENDOR = pathlib.Path("~/Games/vendor/grim-dawn-edition-II-20260724").expanduser()
ARZS = [("base", VENDOR / "database/database.arz"),
        ("gdx1", VENDOR / "gdx1/database/GDX1.arz"),
        ("gdx2", VENDOR / "gdx2/database/GDX2.arz"),
        ("gdx3", VENDOR / "gdx3/database/GDX3.arz")]
DB = HERE.parent / "curated" / "corpus.db"
GRIMTOOLS = HERE.parent / "datamine-acquisition" / "gd" / "raw" / "all_monsters.js"

CTRL_TYPES = {"ControllerMonster", "ControllerStationaryMonster", "ControllerMonsterHidden",
              "ControllerMonsterSynergy", "ControllerGraeae", "ControllerTotem",
              "ControllerSpirit", "ControllerSpiritHost"}
INERT_STRINGS = {"NeverFlee", "NeverRoam", "NeverUseSkill", "None", ""}


def load_arz():
    """Index all four archives. Later archives override earlier for same record path (expansion order)."""
    controllers, monsters, types = {}, {}, {}
    for tag, p in ARZS:
        a = ArzArchive(p)
        for path, v in a.records.items():
            types[path] = (tag, v["rtype"])
        for path, v in a.records.items():
            if v["rtype"] in CTRL_TYPES:
                try:
                    controllers[path] = (tag, v["rtype"], a.read_record(path))
                except Exception:
                    pass
            elif v["rtype"] == "Monster" and not path.startswith("records/sandbox"):
                try:
                    monsters[path] = (tag, a.read_record(path))
                except Exception:
                    pass
        del a
    return controllers, monsters, types


def combat_relevant(path, r):
    """The F1-F9 predicate. F1/F2 are applied at load time."""
    if path.startswith("records/creatures/npcs/"):    return False   # F3
    if path.startswith("records/creatures/ambient/"): return False   # F4
    if "testdummy" in path:                            return False   # F5
    if r.get("hiddenFromCombat") is True:              return False   # F6
    if r.get("invincible") is True:                    return False   # F7
    if r.get("targetable") is False:                   return False   # F8
    if r.get("defaultTeamMajor") == "TeamMajor_Human": return False   # F9
    return True


def non_inert(v):
    if v is None:                 return False
    if isinstance(v, bool):       return v is True
    if isinstance(v, (int, float)): return v != 0
    if isinstance(v, list):       return any(x for x in v if isinstance(x, (int, float)) and x != 0)
    if isinstance(v, str):        return v not in INERT_STRINGS
    return True


def main():
    controllers, monsters, types = load_arz()
    kept = [p for p, (tag, r) in monsters.items() if combat_relevant(p, r)]
    N = len(kept)
    print(f"Monster records (sandbox excluded): {len(monsters)}   combat-relevant N = {N}")

    ctrl_of = {p: controllers.get(monsters[p][1].get("controller"), (None, None, {}))[2] for p in kept}
    unresolved = sum(1 for p in kept if not ctrl_of[p])
    print(f"monster->controller join: {N - unresolved}/{N} resolved directly via the `controller` field "
          f"({unresolved} unresolved)")

    # ---- controller-parameter attestation, monster-weighted ----
    allf = set()
    for p in kept:
        allf |= set(ctrl_of[p].keys())
    print(f"\n=== CONTROLLER PARAMETERS ({len(allf)} fields over kept-monster controllers) ===")
    rows = []
    for f in sorted(allf):
        pr = sum(1 for p in kept if f in ctrl_of[p])
        lv = sum(1 for p in kept if non_inert(ctrl_of[p].get(f)))
        rows.append((f, pr, lv))
    for f, pr, lv in sorted(rows, key=lambda r: -r[2]):
        print(f"  {f:<36} present {pr:5d} ({100*pr/N:5.1f}%)  non-inert {lv:5d} ({100*lv/N:5.1f}%)")
    out = [r for r in rows if 100 * r[2] / N < 1.0]
    print(f"\n  OUT-BY-ATTESTATION at <1% threshold: {len(out)} fields -> "
          + ", ".join(f"{f}({lv})" for f, pr, lv in sorted(out, key=lambda r: r[2])))

    # ---- monster-side skill-class join (Charge / JumpAttack / ally-buff / ground-point / death) ----
    SKILLF = (["attackSkillName", "initialSkillName", "initial2SkillName", "dyingSkillName",
               "healSkillName", "buffSelfSkillName", "buffSelf2SkillName", "buffOtherSkillName",
               "buffOther2SkillName", "berserkSkillName", "nightBuffSkill", "chainInitialSkill",
               "chainNextSkill"]
              + [f"specialAttack{i}SkillName" for i in ["", "2", "3", "4", "5", "6", "7"]]
              + [f"skillName{i}" for i in range(1, 24)])
    srt = {}
    for p in kept:
        s = set()
        for f in SKILLF:
            v = monsters[p][1].get(f)
            if isinstance(v, str) and v in types:
                s.add(types[v][1])
        srt[p] = s
    print("\n=== MONSTER SKILL-CLASS JOIN ===")
    for lab, pred in [("Skill_AttackWeaponCharge (Charge)",  lambda t: t == "Skill_AttackWeaponCharge"),
                      ("Skill_AttackWeaponBlink (JumpAttack)", lambda t: t == "Skill_AttackWeaponBlink"),
                      ("Skill_BuffOther (UseSkillOnAlly)",   lambda t: t == "Skill_BuffOther"),
                      ("Skill_OnDeathSpawnActor (Dying)",    lambda t: t == "Skill_OnDeathSpawnActor"),
                      ("SpawnPet / MonsterGenerator",        lambda t: "SpawnPet" in t or t == "Skill_MonsterGenerator")]:
        n = sum(1 for p in kept if any(pred(t) for t in srt[p]))
        print(f"  {n:5d} ({100*n/N:5.1f}%)  {lab}")

    # ---- monster-field metric families ----
    FAM = {
        "CC-RESIST": ["defensiveStun", "defensiveFreeze", "defensivePetrify", "defensiveTrap",
                      "defensiveSleep", "defensiveKnockdown", "defensiveConfusion", "defensiveFear",
                      "defensiveTaunt", "defensiveConvert", "defensiveDisruption", "stunResistanceInc"],
        "DAMAGE-RESIST": ["defensivePhysical", "defensivePierce", "defensiveFire", "defensiveCold",
                          "defensiveLightning", "defensivePoison", "defensiveAether", "defensiveChaos",
                          "defensiveLife"],
        "OA/DA": ["characterOffensiveAbility", "characterDefensiveAbility", "characterAttributeEquations"],
        "SPEEDS": ["characterRunSpeed", "characterAttackSpeed", "characterSpellCastSpeed", "walkSpeed",
                   "walkDistance", "walkUsesRun"],
        "SPECIAL-ATTACK SLOTS": [f"specialAttack{i}SkillName" for i in ["", "2", "3", "4", "5", "6", "7"]],
        "THREAT/DISTRESS": ["distressCall", "distressCallRange", "maxDistressCalls", "hitThreshold",
                            "angerMultiplier", "numAttackSlots", "numDefenseSlots"],
        "DEATH/LIFECYCLE": ["dyingSkillName", "chanceToSpawnOnDeath", "onDie", "deathFromEnemyDelay"],
        "LOW-HEALTH": ["lowHealthTriggerLevel", "lowHealthResetLevel", "berserkSkillName"],
    }
    print("\n=== MONSTER-FIELD METRIC FAMILIES ===")
    for fam, ks in FAM.items():
        print(f"\n  -- {fam} --")
        for k in ks:
            pr = sum(1 for p in kept if k in monsters[p][1])
            lv = sum(1 for p in kept if non_inert(monsters[p][1].get(k)))
            print(f"     {k:<38} present {pr:5d} ({100*pr/N:5.1f}%)  non-inert {lv:5d} ({100*lv/N:5.1f}%)")

    # ---- TSF6 cited-value vs population check ----
    TSF6 = {"ViewDistance": 15.0, "InnerViewDistance": 4.0, "MaxPursuitDistance": 75.0,
            "PursuitTime": 10000, "SightAngerRate": 3.0, "InnerSightAngerRate": 12.0,
            "fleeDistance": 16.0, "WanderDistance": 4.0}
    print("\n=== TSF6 CITED VALUE vs POPULATION (divergence check) ===")
    print(f"  {'param':<22}{'cited':>9}{'mode':>10}{'%@cited':>10}{'median':>9}")
    for f, cited in TSF6.items():
        vals = [ctrl_of[p].get(f) for p in kept]
        vals = [v for v in vals if isinstance(v, (int, float))]
        c = collections.Counter(round(v, 3) for v in vals)
        mode = c.most_common(1)[0][0]
        at = c.get(round(float(cited), 3), 0)
        print(f"  {f:<22}{cited:>9}{mode:>10}{100*at/len(vals):>9.1f}%{st.median(sorted(vals)):>9}")

    # ---- grimtools corroboration ----
    if GRIMTOOLS.exists():
        s = GRIMTOOLS.read_text(encoding="utf-8", errors="replace")
        body = s[s.find("{"):]
        ids = re.findall(r"[{,](m\d+):\{", body)
        fc = collections.Counter(re.findall(r"[{,]([A-Za-z][A-Za-z0-9_]*):", body))
        print(f"\n=== GRIMTOOLS CORROBORATION (entries counted by regex: {len(ids)}) ===")
        for k in ["ViewDistance", "MaxPursuitDistance", "PursuitTime", "controller", "FleeBehavior",
                  "defensiveStun", "defensiveKnockdown", "defensivePetrify", "defensiveSleep",
                  "defensiveTrap", "defensiveFreeze", "hitThreshold", "numAttackSlots"]:
            print(f"  {('PRESENT ' + str(fc[k])) if fc.get(k) else 'ABSENT':>14}  {k}")

    # ---- player side (P): corpus.db GD-lane, READ-ONLY ----
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    print("\n=== PLAYER-SIDE (P): corpus.db GD-lane, read-only ===")
    print("  GD kits:", cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE game='gd'").fetchone()[0])
    for term in ["stun", "freeze", "trap", "slow", "charge", "blitz", "teleport", "ground", "totem",
                 "reposition", "kite", "petrif", "sleep", "knockdown", "fear", "taunt"]:
        r = cur.execute(
            "SELECT COUNT(DISTINCT kit_id), group_concat(DISTINCT kit_id) FROM kit_dossier "
            "WHERE kit_id LIKE 'gd-%' AND LOWER(payload_json) LIKE ?", (f"%{term}%",)).fetchone()
        print(f"  {term:<12} {r[0]:>3}  {(r[1] or '')[:100]}")
    con.close()


if __name__ == "__main__":
    main()
