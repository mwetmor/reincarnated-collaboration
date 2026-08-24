#!/usr/bin/env python3
"""D-9 emit -- the three deliverable CSVs.  READ-ONLY on every source.

  d9_summon_bodies.csv        MD-B3-1  one row per measured body parameter, both summons
  d9_call_site_xrefs.csv      MD-B3-2  the two call-site verdicts, instruction by instruction
  d9_pet_control_routing.csv  MD-B3-3  the pet-side control routing matrix

Grades: MEASURED (read off a record / an instruction), DECODED (read off an instruction body
whose semantics were resolved), INFERRED-WITH-EVIDENCE, UNDERIVABLE-WITH-PATH-NAMED.
"""
import sys, csv, json, hashlib, pathlib, re
NOTES = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-12-kc2-roster-decode-completion")
sys.path.insert(0, NOTES)
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from s2_lib import E3

HERE = pathlib.Path(__file__).parent
ANM = json.load(open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json"))
FPS = 30.0

# ---- the ONE declared input that is not read off a record on this lap -----------------------
# player level, MEASURED, from data/kc2/pm2_measured_player_sheet.csv row `level` (three-way
# agreement: screenshot 495 + screenshot 508 + gdc header).  Parsed, never typed.
_PS = pathlib.Path("/Users/admin/Games/reincarnated-engine/data/kc2/pm2_measured_player_sheet.csv")
PLAYER_LEVEL = None
for r in csv.DictReader(_PS.open()):
    if r["stat"] == "level":
        PLAYER_LEVEL = int(r["value"]); PLAYER_LEVEL_SRC = r["source_screenshot_or_gdc"]
assert PLAYER_LEVEL is not None


def evaleq(eq, charLevel):
    if isinstance(eq, (int, float)) and not isinstance(eq, bool):
        return float(eq)
    if not isinstance(eq, str) or not eq.strip():
        return None
    e = eq.replace("^", "**")
    if re.search(r"[A-Za-z_]+", e.replace("charLevel", "")):
        return None
    try:
        return float(eval(e, {"__builtins__": {}}, {"charLevel": float(charLevel)}))
    except Exception:
        return None


def num(v, d=None):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def frames(ref):
    r = (ref or "").lower().replace("\\", "/")
    k = r[len("creatures/"):] if r.startswith("creatures/") else r
    e = ANM.get(k)
    return e["frames"] if e else None


def swing_period(c):
    tbl = c.get("charAnimationTableName")
    t, _ = E3.merged(tbl) if isinstance(tbl, str) else (None, None)
    if not t:
        return None, None, tbl
    dur, wt = [], []
    for i in (1, 2, 3):
        an = t.get("unarmedAttackAnim%d" % i)
        if not (isinstance(an, str) and an.lower().endswith(".anm")):
            continue
        f = frames(an)
        sp = num(c.get("unarmedAttackAnimSpeed%d" % i), 1.0) or 1.0
        w = num(c.get("unarmedAttackAnimWeight%d" % i), 0.0) or 0.0
        if f:
            dur.append(f / FPS / sp); wt.append(w)
    if not dur:
        return None, None, tbl
    tw = sum(wt)
    base = sum(d * w for d, w in zip(dur, wt)) / tw if tw else sum(dur) / len(dur)
    ats = num(c.get("characterAttackSpeed"), 1.0) or 1.0
    return base, base / ats, tbl


def arr_at(v, lvl):
    """rank-array read at 1-based rank `lvl`; scalar passes through."""
    if isinstance(v, list):
        i = int(lvl) - 1
        return v[i] if 0 <= i < len(v) else ("<rank %d beyond len %d>" % (lvl, len(v)))
    return v


# ---------------------------------------------------------------- the two summons
SUMMONS = [
    dict(summon="Guardian of Empyrion",
         skill="records/skills/playerclass09/summon_celestialguardian1.dbr",
         rank_eff=2, body_from="spawnObjects[rank_eff-1]"),
    dict(summon="Deathstalker",
         skill="records/skills/itemskillsgdx1/relics/summondeathstalker.dbr",
         rank_eff=1, body_from="spawnObjects (scalar)"),
]

rows = []


def add(summon, group, field, value, grade, source, method):
    rows.append(dict(summon=summon, group=group, field=field, value=value,
                     grade=grade, source_record_or_rva=source, extraction_method=method))


for s in SUMMONS:
    nm = s["summon"]
    sk, sk_owners = E3.merged(s["skill"])
    spawn = sk.get("spawnObjects")
    body_path = spawn[s["rank_eff"] - 1] if isinstance(spawn, list) else spawn
    body, body_owners = E3.merged(body_path)

    add(nm, "chain", "spawn_skill_record", s["skill"], "MEASURED",
        s["skill"], "E3.merged, archives=%s" % "|".join(sk_owners))
    add(nm, "chain", "spawn_skill_class", sk.get("Class"), "MEASURED", s["skill"], "field read")
    add(nm, "chain", "spawnObjects_len", len(spawn) if isinstance(spawn, list) else 1,
        "MEASURED", s["skill"], "field read")
    add(nm, "chain", "rank_eff_used", s["rank_eff"], "MEASURED",
        "pm4g_defensive_actives.csv (B-3 § 0.1)", "inherited registered value")
    add(nm, "chain", "body_record", body_path, "DECODED", s["skill"],
        "spawnObjects indexed by GetCurrentLevel@Skill via GetSpawnObject@Skill "
        "(SpawnPet@Skill_SpawnPet 0x0041c884/0x0041c8ae); %s" % s["body_from"])
    add(nm, "chain", "body_archives", "|".join(body_owners), "MEASURED", body_path, "arz index")
    add(nm, "body", "Class", body.get("Class"), "MEASURED", body_path, "field read")
    add(nm, "body", "templateName", body.get("templateName"), "MEASURED", body_path, "field read")
    add(nm, "body", "monsterClassification", body.get("monsterClassification"), "MEASURED",
        body_path, "field read")
    add(nm, "body", "invincible", body.get("invincible"), "MEASURED", body_path, "field read")
    add(nm, "body", "invincible_SEMANTICS",
        "Load@Character (0x00043d0a/0x00043d17) writes this field to BOTH Character+0x1845 and +0x1844. "
        "IsInvincible@Character (0x00059c80) = read of +0x1844, Character vtable slot 262 (+0x418), "
        "inherited unchanged by Monster/Pet/PetPlayerScaling. FIVE gates early-return on it: "
        "SubtractLife@Character 0x000542b4, SubtractLife@SkillManager 0x004405f1, "
        "AddDamage@DurationDamageManager 0x00208a53, AddFixedDamage@DurationDamageManager 0x00208d46, "
        "DebufTarget@Character 0x0005302f. IsTargetable@Monster (0x002dc783) deliberately BYPASSES the "
        "runtime test for an invincible-in-DBR body, so it stays targetable.",
        "DECODED", "Game.dll 0x00043d0a / 0x00059c80 / 0x00043d17 / 0x002dc783",
        "byte-exact disp32 scans for 0x1844, 0x1845 and 0x418 over .text; every hit decoded")
    add(nm, "body", "factions", body.get("factions"), "MEASURED", body_path, "field read")
    add(nm, "body", "charLevel_equation", body.get("charLevel"), "MEASURED", body_path, "field read")
    add(nm, "body", "controller", body.get("controller"), "MEASURED", body_path, "field read")
    add(nm, "body", "controllerAggressive", body.get("controllerAggressive"), "MEASURED",
        body_path, "field read")
    add(nm, "body", "controllerDefensive", body.get("controllerDefensive"), "MEASURED",
        body_path, "field read")
    add(nm, "body", "causesAnger", body.get("causesAnger"), "MEASURED", body_path, "field read")
    add(nm, "body", "angerMultiplier", body.get("angerMultiplier"), "MEASURED", body_path, "field read")
    add(nm, "body", "actorHeight", body.get("actorHeight"), "MEASURED", body_path, "field read")

    # --- bio ---------------------------------------------------------------------------
    bio_path = body.get("characterAttributeEquations")
    bio, bio_owners = E3.merged(bio_path)
    add(nm, "bio", "bio_record", bio_path, "MEASURED", body_path, "field read")
    for k in ("characterLife", "characterOffensiveAbility", "characterDefensiveAbility",
              "characterMana", "characterLifeRegen", "characterStrength",
              "characterDexterity", "characterIntelligence"):
        add(nm, "bio", k + "_equation", bio.get(k), "MEASURED", bio_path, "field read")
    for k, lab in (("characterLife", "life"), ("characterOffensiveAbility", "OA"),
                   ("characterDefensiveAbility", "DA"), ("characterMana", "mana")):
        v = evaleq(bio.get(k), PLAYER_LEVEL)
        add(nm, "bio", "%s_base_at_charLevel_%d" % (lab, PLAYER_LEVEL),
            None if v is None else round(v, 6), "INFERRED-WITH-EVIDENCE", bio_path,
            "equation evaluated at charLevel=player level %d (%s). Level BINDING is inferred, "
            "not measured: Class=PetPlayerScaling + GetCharLevelGapFixer@Pet (0x00009470) is "
            "`xor eax,eax; ret 4` + Lap E Q3 MEASURED owner-level binding for the Class=Monster "
            "sibling. See UNDERIVABLE row `pet_charLevel_binding`."
            % (PLAYER_LEVEL, PLAYER_LEVEL_SRC))

    # --- attack surface ---------------------------------------------------------------
    slots = [("attackSkillName", "basic"), ("specialAttackSkillName", "special1"),
             ("specialAttack2SkillName", "special2"), ("specialAttack3SkillName", "special3"),
             ("specialAttack4SkillName", "special4"), ("buffSelfSkillName", "buff_self")]
    n_att = 0
    for fld, lab in slots:
        p = body.get(fld)
        if not isinstance(p, str) or not p:
            continue
        r, _o = E3.merged(p)
        cls = r.get("Class") if r else None
        if lab != "buff_self":
            n_att += 1
        add(nm, "attack_slot", "%s.record" % lab, p, "MEASURED", body_path, "field read")
        add(nm, "attack_slot", "%s.class" % lab, cls, "MEASURED", p, "field read")
        if not r:
            continue
        # rank used by this slot = the skillLevel<i> that names this record on the body
        lvl = 1
        for i in range(1, 64):
            if str(body.get("skillName%d" % i, "")).lower() == p.lower():
                eq = body.get("skillLevel%d" % i)
                ev = evaleq(eq, PLAYER_LEVEL)
                lvl = int(ev) if ev is not None else 1
                add(nm, "attack_slot", "%s.rank_equation" % lab, eq, "MEASURED", body_path,
                    "skillLevel%d beside skillName%d" % (i, i))
                break
        add(nm, "attack_slot", "%s.rank_used" % lab, lvl, "DECODED", body_path,
            "skillLevel equation evaluated at charLevel=%d" % PLAYER_LEVEL)
        for f in sorted(r):
            if not f.startswith("offensive"):
                continue
            v = r[f]
            if isinstance(v, list):
                if not any(x != 0 for x in v):
                    continue
                add(nm, "attack_slot", "%s.%s" % (lab, f), arr_at(v, lvl), "MEASURED", p,
                    "rank-array[%d] of %d ranks" % (lvl, len(v)))
            elif isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0:
                add(nm, "attack_slot", "%s.%s" % (lab, f), v, "MEASURED", p, "scalar field")
        for f in ("skillTargetNumber", "skillTargetAngle", "skillTargetRadius",
                  "skillMaxLevel", "skillUltimateLevel", "distanceProfile",
                  "skillSpecialAnimationName", "skillCooldownTime"):
            if f in r and r[f] not in (0, 0.0, False, "", None):
                add(nm, "attack_slot", "%s.%s" % (lab, f), r[f], "MEASURED", p, "field read")
    add(nm, "attack_slot", "n_attack_slots", n_att, "MEASURED", body_path,
        "count of populated attack/specialAttack* slots")

    # --- swing period ------------------------------------------------------------------
    base, per, tbl = swing_period(body)
    add(nm, "swing", "charAnimationTableName", tbl, "MEASURED", body_path, "field read")
    add(nm, "swing", "characterAttackSpeed", body.get("characterAttackSpeed"), "MEASURED",
        body_path, "field read")
    add(nm, "swing", "characterSpellCastSpeed", body.get("characterSpellCastSpeed"), "MEASURED",
        body_path, "field read")
    add(nm, "swing", "characterRunSpeed", body.get("characterRunSpeed"), "MEASURED",
        body_path, "field read")
    add(nm, "swing", "unarmed_anim_weighted_base_s", None if base is None else round(base, 6),
        "MEASURED", tbl, "anm_index frames/%.0f fps, weighted by unarmedAttackAnimWeight" % FPS)
    add(nm, "swing", "basic_swing_period_s", None if per is None else round(per, 6),
        "MEASURED", body_path, "weighted base / characterAttackSpeed (pm2b_petchain method)")

    # --- passive / armour skill ---------------------------------------------------------
    for i in range(1, 64):
        p = body.get("skillName%d" % i)
        if not isinstance(p, str) or "armorpets" not in p:
            continue
        r, _ = E3.merged(p)
        eq = body.get("skillLevel%d" % i)
        lvl = int(evaleq(eq, PLAYER_LEVEL) or 1)
        add(nm, "passive", "armour_skill_record", p, "MEASURED", body_path, "skillName%d" % i)
        add(nm, "passive", "armour_skill_rank_equation", eq, "MEASURED", body_path,
            "skillLevel%d" % i)
        add(nm, "passive", "armour_skill_rank_used", lvl, "DECODED", body_path,
            "evaluated at charLevel=%d" % PLAYER_LEVEL)
        add(nm, "passive", "defensiveProtection", arr_at(r.get("defensiveProtection"), lvl),
            "MEASURED", p, "rank-array[%d] of %d" % (lvl, len(r.get("defensiveProtection", []))))
        for f in ("defensiveSlowLifeLeach", "defensiveSlowManaLeach", "offensiveTauntMin"):
            if f in r:
                add(nm, "passive", f, arr_at(r[f], lvl), "MEASURED", p, "field read")
        add(nm, "passive", "offensiveCritDamageModifier",
            arr_at(r.get("offensiveCritDamageModifier"), lvl), "MEASURED", p,
            "rank-array[%d]" % lvl)
        break

    # --- innate control-resistance passive ---------------------------------------------
    for i in range(1, 64):
        p = body.get("skillName%d" % i)
        if not isinstance(p, str):
            continue
        if not ("passiveproperties" in p or "_innate01" in p):
            continue
        r, _ = E3.merged(p)
        add(nm, "resist", "innate_passive_record", p, "MEASURED", body_path, "skillName%d" % i)
        for f in sorted(r):
            if f.startswith("defensive") and isinstance(r[f], (int, float)) \
                    and not isinstance(r[f], bool) and r[f] != 0:
                add(nm, "resist", f, r[f], "MEASURED", p, "field read")
        break

    # --- what could NOT be derived ------------------------------------------------------
    add(nm, "UNDERIVABLE", "pet_charLevel_binding",
        "UNDERIVABLE-WITH-PATH-NAMED", "UNDERIVABLE-WITH-PATH-NAMED", body_path,
        "SpawnPet@Skill_SpawnPet (0x0041c850) contains NO SetLevel call; the pet is Load()ed from "
        "its record then JoinMe@Monster (Character vtable +0x30c, called at 0x0041ca9d) binds it "
        "to the caster. PATH TO CLOSE: decode JoinMe@Monster (0x002d5200) and the leader-level "
        "read it performs, OR read a live Guardian's level off a save/GDC block (NOT a tooltip - "
        "display-layer guard).")
    add(nm, "UNDERIVABLE", "difficulty_pak_cell_index",
        "UNDERIVABLE-WITH-PATH-NAMED", "UNDERIVABLE-WITH-PATH-NAMED",
        "records/game/balancingadjustment_mp+difficulty_pets01.dbr",
        "THE PAK IS DECODED (ContributeGameBalanceCharAttributes@Pet 0x00315f90 reads "
        "gGameEngine+0x19f0 = petAttributePak, and does NOT fold GetChallengeAdjustment). The "
        "12-cell index for Crucible-Ultimate-solo was not re-derived on THIS lap. PATH TO CLOSE: "
        "Lap E pm4e_dispatch_evidence.csv already publishes cell 8 = 15.0 for the pet pak; "
        "re-derive the index selection in GameEngine before folding it.")


# ------------------------------------------------------------------ write CSV 1
p1 = HERE / "d9_summon_bodies.csv"
with p1.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["summon", "group", "field", "value", "grade",
                                      "source_record_or_rva", "extraction_method"])
    w.writeheader()
    for r in rows:
        w.writerow(r)
print("wrote %s : %d rows" % (p1.name, len(rows)))


# ------------------------------------------------------------------ CSV 2 : call-site xrefs
X = [
    # MD-B3-2 (a)
    dict(target="MD-B3-2a", question="does ControllerPlayerStateIdle::RequestReleasePet call SkillManager::StopCurrentSkill?",
         link=1, rva="0x0011ff60", symbol="RequestReleasePet@ControllerPlayerStateIdle",
         instruction="jmp 0x0011f0d0", resolves_to="DefaultRequestReleasePetAction@ControllerPlayerState",
         verdict="forwarder", grade="DECODED", method="bounded disasm (d8_lib.bounded)"),
    dict(target="MD-B3-2a", question="", link=2, rva="0x0011f0d0",
         symbol="DefaultRequestReleasePetAction@ControllerPlayerState",
         instruction="push 0x14; call operator new; mov [edi], 0x1058e0f4",
         resolves_to="??_7ReleasePetConfigCmd@GAME@@6B@ (VA 0x1058e0f4 = RVA 0x0058e0f4)",
         verdict="allocates a ReleasePetConfigCmd", grade="DECODED",
         method="vtable VA resolved against export table"),
    dict(target="MD-B3-2a", question="", link=3, rva="0x0011f170",
         symbol="DefaultRequestReleasePetAction+0xa0", instruction="call dword ptr [eax+0x1a4]",
         resolves_to="controller config-cmd queue", verdict="queues the cmd; returns al=1 unconditionally",
         grade="DECODED", method="bounded disasm"),
    dict(target="MD-B3-2a", question="", link=4, rva="0x000a9580", symbol="Execute@ReleasePetConfigCmd",
         instruction="ObjectManager::Get<Character>([ebx+0xc]) -> esi; Get<ControllerCombat>([esi+0x1120]) -> edi",
         resolves_to="classInfo@Character (VA 0x107ff618) / classInfo@ControllerCombat (VA 0x107ff510)",
         verdict="resolves THE PET, not the player", grade="DECODED",
         method="RTTI_ClassInfo statics resolved by export name"),
    dict(target="MD-B3-2a", question="", link=5, rva="0x000a9614",
         symbol="Execute@ReleasePetConfigCmd+0x94", instruction="call dword ptr [eax+0x88]",
         resolves_to="KillMe@ControllerCombat 0x000eeab0 (controller vtable +0x88, IDENTICAL on ControllerPlayer/ControllerMonster/ControllerPet/ControllerAlly)",
         verdict="kills the pet", grade="DECODED", method="controller vtable +0x88 resolved on 4 classes"),
    dict(target="MD-B3-2a", question="", link=6, rva="0x0043ea00",
         symbol="StopCurrentSkill@SkillManager",
         instruction="E8/E9 rel32 xref scan over .text + image-wide 4-byte VA scan",
         resolves_to="7 call sites, 0 address-takes",
         verdict="Execute@{MoveToAction,JumpAttackAction,EvadeAction,TakeStunAction,TakeKnockdownAction,TakeSleepAction,ImmobilizeAction}",
         grade="DECODED", method="two independent techniques (D-7 § 6 standard)"),
    dict(target="MD-B3-2a", question="", link=7, rva="n/a", symbol="VERDICT",
         instruction="n/a", resolves_to="n/a",
         verdict="NO. Releasing a pet does NOT call StopCurrentSkill and does NOT break the channel. K-11 ANSWERED.",
         grade="DECODED", method="call-target audit of all four lane bodies + the 7-caller census"),
    # MD-B3-2 (b)
    dict(target="MD-B3-2b", question="what is slot 76's UseSkill IMPL occupant's verdict?",
         link=1, rva="0x005c0c04+0x130", symbol="ControllerPlayerStateUseSkill vftable slot 76",
         instruction="dword @ vftable+0x130", resolves_to="0x00122f50 RequestSkillAction@ControllerPlayerStateUseSkill",
         verdict="the IMPL occupant", grade="MEASURED", method="vtable slot read"),
    dict(target="MD-B3-2b", question="", link=2, rva="0x00122f56",
         symbol="RequestSkillAction@ControllerPlayerStateUseSkill",
         instruction="mov ecx,[esi+4]; call GetCurrentStateData@ControllerAI; push [eax+8]",
         resolves_to="the state-data's actor id",
         verdict="reads the CHANNELLED SKILL's id", grade="DECODED", method="bounded disasm"),
    dict(target="MD-B3-2b", question="", link=3, rva="0x00122f69",
         symbol="RequestSkillAction@ControllerPlayerStateUseSkill+0x19",
         instruction="call 0x0000d4f0", resolves_to="ObjectManager::Get<Skill> (classInfo@Skill VA 0x107ff570)",
         verdict="cast target class = Skill", grade="DECODED",
         method="RTTI_ClassInfo static resolved by export name"),
    dict(target="MD-B3-2b", question="", link=4, rva="0x00122f76",
         symbol="RequestSkillAction@ControllerPlayerStateUseSkill+0x26",
         instruction="mov eax,[eax+0x2b0]; call eax; test al,al; je DEFAULT; xor al,al; ret 0x14",
         resolves_to="Skill vtable +0x2b0 (slot 172)",
         verdict="REFUSE iff the predicate returns true, else fall through", grade="DECODED",
         method="bounded disasm"),
    dict(target="MD-B3-2b", question="", link=5, rva="0x003e96f0",
         symbol="Skill_AttackRadiusSpin vtable +0x2b0 = GetWarmUpWasActive@Skill_AttackRadiusGrow",
         instruction="cmp dword ptr [ecx+0x44c], 1 ; sete al ; ret",
         resolves_to="Skill+0x44c == 1 (the WARM-UP phase; D-8 R-D8-3 named this field: 0/1/2 = idle/warm-up/running)",
         verdict="TRUE only during warm-up", grade="DECODED",
         method="bounded disasm + Skill* vtable census (118/141 classes carry IsActive@Skill = `xor al,al` here)"),
    dict(target="MD-B3-2b", question="", link=6, rva="0x00122f9a",
         symbol="RequestSkillAction@ControllerPlayerStateUseSkill+0x4a",
         instruction="tail-forward to DefaultRequestSkillAction@ControllerPlayerState (0x0011e1d0)",
         resolves_to="THE IDLE OCCUPANT",
         verdict="identical to PERMITTED once the warm-up gate passes", grade="DECODED",
         method="the Idle slot-76 occupant 0x0011ff30 jmps to the same 0x0011e1d0"),
    dict(target="MD-B3-2b", question="", link=7, rva="n/a", symbol="VERDICT", instruction="n/a",
         resolves_to="n/a",
         verdict="PERMITTED-EXCEPT-WARM-UP. Slot 76 mid-channel is NOT a refusal: it refuses only while the channelled skill's Skill+0x44c == 1 (warm-up). With EoR spinning (+0x44c == 2) the Guardian of Empyrion IS castable.",
         grade="DECODED", method="six-link chain, every link an instruction"),
]
p2 = HERE / "d9_call_site_xrefs.csv"
with p2.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["target", "question", "link", "rva", "symbol",
                                      "instruction", "resolves_to", "verdict", "grade", "method"])
    w.writeheader()
    for r in X:
        w.writerow(r)
print("wrote %s : %d rows" % (p2.name, len(X)))


# ------------------------------------------------------------------ CSV 3 : pet control routing
P = []


def pr(layer, family, subject, occupant, rva, verdict, grade, method):
    P.append(dict(layer=layer, family=family, subject=subject, occupant=occupant, rva=rva,
                  verdict=verdict, grade=grade, method=method))


# controller class, from the records
for path, who in [("records/controllers/pets/controller_hellhound_normal.dbr", "Deathstalker (normal)"),
                  ("records/controllers/pets/controller_hellhound_aggressive.dbr", "Deathstalker (aggressive)"),
                  ("records/controllers/pets/controller_hellhound_defensive.dbr", "Deathstalker (defensive)"),
                  ("records/controllers/pets/controller_celestialguardian_aggressive.dbr", "Guardian of Empyrion")]:
    r, _ = E3.merged(path)
    pr("record", "controller_class", who, r.get("Class"), path,
       "the pet's controller record declares Class = %s" % r.get("Class"), "MEASURED", "field read")
    for f in ("FleeBehavior", "ViewDistance", "MaxPursuitDistance", "TeleportToLeaderDistance",
              "DodgeChance", "minSwingPause", "maxSwingPause", "ignorePetsChance",
              "petAngerTransference"):
        if f in r:
            pr("record", "controller_param", who, r[f], path, f, "MEASURED", "field read")

# C++ hierarchy
for a, b, off, note in [("classInfo@Pet", "classInfo@Monster", "0x107ff5b8+0x08",
                         "Pet DERIVES FROM Monster"),
                        ("classInfo@ControllerPet", "classInfo@ControllerMonster", "0x007fd308+0x08",
                         "ControllerPet DERIVES FROM ControllerMonster"),
                        ("classInfo@Player", "classInfo@Character", "0x107ff5a0+0x08",
                         "Player DERIVES FROM Character")]:
    pr("rtti", "hierarchy", a, b, off, note, "DECODED",
       "RTTI_ClassInfo base pointer at +0x08, both ends exported by name")

pr("binary", "state_machine", "RegisterStates@ControllerPet", "jmp RegisterStates@ControllerMonster",
   "0x000e8e90", "a pet registers EXACTLY the ControllerMonster state set - no additions, no removals",
   "DECODED", "bounded disasm: a bare jmp")
pr("binary", "state_machine", "RegisterTemporaryStates@ControllerPet",
   "jmp RegisterTemporaryStates@ControllerMonster", "0x000e8ef0",
   "same", "DECODED", "bounded disasm: a bare jmp")
pr("binary", "state_machine", "ControllerMonster registered states",
   "Startup|Idle|Pursue|Attack|JumpAttack|RepositionForAttack|Flee|Roam|Wander|WanderPause|Return|"
   "Dying|Dead|FollowLeader|DefendLeader|NavigateObstacle|Move|Charge|DodgeAttack|Panic|Paralyze|"
   "Confused|Immobile|Trapped|Stunned|KnockedDown|Sleeping|Scared|Patrol|WaitToAttack|QuestMove|"
   "QuestWalk|QuestPlayAnimation|QuestUseSkill|GettingUp|TakeHit",
   "0x000f87c0", "36 state names, string-literal exact", "MEASURED",
   "push-literal scan over the bounded body")

# the three families, body layer then controller layer
FAM = [
    ("Confusion", "Character vtable +0x3c8", "0x000084d0 (ret 4 stub)",
     "0x002d9670 CombatExertInfluenceConfusion@Monster",
     "0x002d9670 CombatExertInfluenceConfusion@Monster"),
    ("Fear", "Character vtable +0x3c4", "0x00054690 CombatExertInfluenceFear@Character",
     "0x00054690 (same)", "0x00054690 (same)"),
    ("Taunt", "Character vtable +0x3cc", "0x000546d0 CombatExertInfluenceTaunt@Character",
     "0x000546d0 (same)", "0x000546d0 (same)"),
]
for fam, slot, pl, pet, mon in FAM:
    pr("body_vtable", fam, "Player", pl, slot, "player-side occupant", "MEASURED", "vtable slot read")
    pr("body_vtable", fam, "Pet / PetPlayerScaling", pet, slot,
       "PET-SIDE OCCUPANT - PetPlayerScaling inherits Pet's vftable at this slot", "MEASURED",
       "vtable slot read on ??_7Pet@GAME@@6BObject@1@@ and ??_7PetPlayerScaling@GAME@@6BObject@1@@")
    pr("body_vtable", fam, "Monster", mon, slot, "monster-side occupant", "MEASURED", "vtable slot read")

pr("controller_vtable", "Fear", "ControllerPlayer +0x84", "0x0000f100 (`ret 8` stub)", "+0x84",
   "NO-OP on the player (D-7 § 3.4, RE-DERIVED here)", "DECODED", "bounded disasm of the occupant")
pr("controller_vtable", "Fear", "ControllerMonster / ControllerPet / ControllerAlly +0x84",
   "0x000f6c50 ScareMe@ControllerMonster", "+0x84",
   "REAL: latches a scared-until value at Controller+0x530 if the new one is larger, then drives the "
   "current AI state via state vtable +0xd0", "DECODED", "bounded disasm of the occupant")
pr("controller_vtable", "Taunt", "ControllerPlayer +0x8c", "0x0000f100 (`ret 8` stub)", "+0x8c",
   "NO-OP on the player", "DECODED", "bounded disasm of the occupant")
pr("controller_vtable", "Taunt", "ControllerMonster / ControllerPet / ControllerAlly +0x8c",
   "0x000f9c80 TauntMe@ControllerMonster", "+0x8c",
   "REAL: if InPursuitRange@ControllerMonster(id) [0x000fb7a0] then AddAnger@AngerManager(id, amount, forced=true)", "DECODED",
   "bounded disasm of the occupant")
pr("controller_vtable", "Confusion", "the pet's controller", "state vtable +0x9c (`Confused`)",
   "+0x9c", "CombatExertInfluenceConfusion@Monster tail-jumps into the CURRENT AI STATE's +0x9c; "
   "the ControllerMonster state set registers a `Confused` state", "DECODED", "bounded disasm")

for off, lab in [(0x90, "BeginStun"), (0x94, "EndStun"), (0xa8, "BeginSleep"), (0xac, "EndSleep"),
                 (0xb0, "BeginImmobilize (Freeze 0x2d / Petrify 0x2e / Immobilize 0x2f)"),
                 (0xb4, "EndImmobilize"), (0xb8, "BeginTrap"), (0xbc, "EndTrap")]:
    pr("controller_vtable", "involuntary-effect ladder", lab,
       "BYTE-IDENTICAL across ControllerPlayer / ControllerMonster / ControllerPet / ControllerAlly",
       "+%#05x" % off,
       "the shared forwarder (ICF-folded); it dispatches to the CURRENT AI STATE's slot 40 - which "
       "for a pet is a ControllerMonsterState*, not a ControllerPlayerState*", "MEASURED",
       "vtable slot read on all four classes")

# the DBR-side resistances that make the live route land at zero on THESE two summons
for who, path in [("Deathstalker", "records/skills/itemskillsgdx1/pets/petskill_deathstalker_passiveproperties.dbr"),
                  ("Guardian of Empyrion", "records/skills/playerclass09/pets/petskill_celestialguardian_innate01.dbr")]:
    r, _ = E3.merged(path)
    for f in ("defensiveConfusion", "defensiveFear", "defensiveConvert", "defensiveTotalSpeedResistance",
              "defensiveStun", "defensiveFreeze", "defensivePetrify", "defensiveSleep",
              "defensiveTrap", "defensiveKnockdown", "defensiveLifeLeach", "defensiveBleeding",
              "defensivePercentCurrentLife", "defensivePercentReflectionResistance"):
        pr("record", "innate_resistance", "%s :: %s" % (who, f),
           r.get(f, "<ABSENT => 0>"), path,
           "the route is live at the binary layer; THIS body resists it by %s" % r.get(f, "<absent>"),
           "MEASURED", "field read on the body's innate passive")

# ---- THE INVINCIBLE GATE: the third kind of zero, upstream of both routing and resistance ----
pr("binary", "invincible", "DBR field -> live flag",
   "Load@Character reads \"invincible\" (literal VA 0x104f4b9c) with LoadTable::GetBool(default=0) "
   "and writes al to BOTH Character+0x1845 (IsInvincibleInDbr) AND Character+0x1844 (IsInvincible)",
   "0x00043d0a / 0x00043d17",
   "the DBR flag IS the live flag at spawn - no runtime step needed", "DECODED",
   "byte-exact disp32 scan for 0x1844 (16 sites) and 0x1845 (9 sites) over .text, every site decoded")
pr("binary", "invincible", "IsInvincible@Character", "mov al, byte ptr [ecx+0x1844]; ret",
   "0x00059c80", "Character vtable slot 262 (+0x418); Monster/Pet/PetPlayerScaling all inherit it; "
   "Player overrides it (0x0031b090) to OR in IsPlayingVideo", "DECODED", "bounded disasm + vtable read")
for lbl, at, eff in [
        ("SubtractLife@Character", "0x000542b4",
         "early-return: NO LIFE LOSS. Guarded by a force-bool at [ebp+0x10]; a second immunity byte "
         "at Character+0x1846 refuses immediately after"),
        ("SubtractLife@SkillManager", "0x004405f1", "early-return: NO LIFE LOSS"),
        ("AddDamage@DurationDamageManager", "0x00208a53", "early-return: NO DoT IS ENROLLED"),
        ("AddFixedDamage@DurationDamageManager", "0x00208d46",
         "early-return: NO CONTROL BUCKET IS ENROLLED - this is the function that fills the fixed-damage "
         "buckets UpdateFxAndInfluence elects from (D-8 § 3.1)"),
        ("DebufTarget@Character", "0x0005302f", "early-return: NO DEBUFF TRANSFER")]:
    pr("binary", "invincible", lbl, "mov eax,[vtable+0x418]; call eax; test al,al; jne <return>", at,
       eff, "DECODED", "byte-exact disp32 0x418 scan over .text (66 instructions, 5 are this gate)")
pr("binary", "invincible", "IsTargetable@Monster", "cmp byte [esi+0x1845],0", "0x002dc783",
   "an invincible-IN-DBR body SKIPS the runtime IsInvincible test and stays TARGETABLE "
   "(targetable <=> [+0x182e] != 0 AND the tested byte == 0). Invincible-by-declaration therefore "
   "means DRAWS ATTACKS BUT TAKES NONE - the shipped aggro-sink shape", "DECODED", "bounded disasm")
pr("binary", "influence-driver", "Fear (Character +0x3c4)", "call dword ptr [esi+0x3c4]", "0x0020a19f",
   "sole driver = UpdateFxAndInfluence@DurationDamageManager - the SAME function D-8 pinned; it reads "
   "the fixed-damage buckets, so the invincible gate on AddFixedDamage forecloses it", "DECODED",
   "byte-exact disp32 0x3c4 scan (25 instructions, 1 is a call)")
pr("binary", "influence-driver", "Confusion (Character +0x3c8)", "call dword ptr [esi+0x3c8]", "0x0020a15b",
   "same driver, same foreclosure", "DECODED",
   "byte-exact disp32 0x3c8 scan (26 instructions, 1 is a call)")
pr("binary", "influence-driver", "Taunt (Character +0x3cc)", "call dword ptr [eax+0x3cc]", "0x000dcf4c",
   "DIFFERENT DRIVER: Execute@CombatAttributeInfluenceDamage_Taunt - hit-resolution side, NOT the "
   "duration-damage ladder. Whether the invincible gate covers this path was NOT decoded on this lap",
   "UNDERIVABLE-WITH-PATH-NAMED",
   "byte-exact disp32 0x3cc scan (17 instructions, 1 is a call). PATH TO CLOSE: decode the caller of "
   "Execute@CombatAttributeInfluenceDamage_Taunt (0x000dcf30) and test it for the +0x418 gate")

p3 = HERE / "d9_pet_control_routing.csv"
with p3.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["layer", "family", "subject", "occupant", "rva",
                                      "verdict", "grade", "method"])
    w.writeheader()
    for r in P:
        w.writerow(r)
print("wrote %s : %d rows" % (p3.name, len(P)))

# ------------------------------------------------------------------ digests
dig = {}
for p in (p1, p2, p3):
    dig[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
for src in ["/Users/admin/Games/vendor/grim-dawn/Game.dll",
            "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/database/database.arz",
            "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx1/database/GDX1.arz",
            "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx2/database/GDX2.arz",
            "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/gdx3/database/GDX3.arz"]:
    h = hashlib.sha256()
    with open(src, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    dig[src] = h.hexdigest()
dig["player_level_input"] = dict(value=PLAYER_LEVEL, source=PLAYER_LEVEL_SRC,
                                 file=str(_PS))
(HERE / "d9_digests.json").write_text(json.dumps(dig, indent=2))
print("wrote d9_digests.json")
