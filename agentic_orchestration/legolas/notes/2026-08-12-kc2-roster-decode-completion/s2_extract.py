#!/usr/bin/env python3
"""E-s09-cp150 roster decode-completion lap (gap G2). READ-ONLY on engine + vendor trees.

Schema lineage: 2026-08-08-kc2-threat-grammar-arz-boundary/x1_extract.py
Deltas vs the 08-08 lap:
  (a) roster basis re-pointed t22 band-A (968) -> E-s09-cp150 baton (169)
  (b) NEW mesh/scale/texture decode  -> closes elrond gap G6 (body declared, not inferred)
  (c) NEW damage_types + control_effects rolled off skill records -> A6-equivalent, 100% cov
  (d) ctrl_* widened from 9 fields to the A7 28-field set
  (e) range_band aggregated BOTH modal and chance-weighted -> G7 stays an open design ruling
  (f) baton facts + pool membership joined on every row
"""
import json, csv, re, collections, sys
sys.path.insert(0, "/tmp/leg_s2")
from s2_lib import E3, roster, pool_membership

ANM = json.load(open("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json"))
FPS = 30.0
PFX = ("unarmed", "sHanded", "dHanded", "dualRanged", "staff", "ranged1h",
       "ranged2h", "axe2h", "mace2h", "sword2h", "spear2h")

# --- damage vocabulary (derived by census over this roster's slot skills, not assumed) ---
DIRECT = ["Physical", "Pierce", "Fire", "Cold", "Lightning", "Poison",
          "Aether", "Chaos", "Life", "Elemental"]
DOT = ["SlowPhysical", "SlowBleeding", "SlowFire", "SlowCold", "SlowLightning",
       "SlowPoison", "SlowLife", "SlowLifeLeach"]
CTRLFX = ["Stun", "Freeze", "Petrify", "Confusion", "Convert", "SlowTotalSpeed",
          "SlowRunSpeed", "SlowAttackSpeed", "SlowDefensiveAbility",
          "SlowOffensiveAbility", "SlowDamageMult", "SlowDefensiveReduction",
          "TotalDamageReductionPercent"]
# A7's controller field set (28)
CTRL = ["MaxPursuitDistance", "PursuitTime", "ViewDistance", "InnerViewDistance",
        "MaxYViewDistance", "RoamBehavior", "RoamDistance", "MinRoamDistance",
        "MinTimeBeforeRoam", "MaxTimeBeforeRoam", "ChanceToIdleOnPatrol",
        "MinPatrolIdleTime", "MaxPatrolIdleTime", "WanderDistance", "MinWanderDistance",
        "TeleportToLeaderDistance", "fleeDistance", "FleeBehavior", "FleeChance",
        "DodgeChance", "DodgeDistance", "MinDodgeDistance", "DodgeDelay",
        "enemyTooClose", "EmoteBeforePursuingChance", "ChanceToRespondToDistressCall",
        "minSwingPause", "maxSwingPause", "RepositionChance"]


def nz(v):
    """nonzero on a scalar OR anywhere in a 60-rank array"""
    if isinstance(v, list):
        return any(x for x in v if isinstance(x, (int, float)))
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0


def akey(ref):
    r = (ref or "").lower().replace("\\", "/")
    return r[len("creatures/"):] if r.startswith("creatures/") else r


def frames(ref):
    e = ANM.get(akey(ref))
    return e["frames"] if e else None


def num(v, d=None):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def dmg_axes(s):
    """(direct types, dot types, control effects, n_ranks) present on one skill record."""
    d = [t for t in DIRECT if nz(s.get("offensive%sMin" % t)) or nz(s.get("offensive%sMax" % t))]
    o = [t for t in DOT if nz(s.get("offensive%sMin" % t))]
    c = [t for t in CTRLFX if nz(s.get("offensive%sMin" % t))]
    nr = 0
    for k, v in s.items():
        if k.startswith("offensive") and isinstance(v, list):
            nr = max(nr, len(v))
    return d, o, c, nr


POOLS, POOLKIND = pool_membership()
rows = roster()
mon_rows, slot_rows = [], []
stat = collections.Counter()

for r in rows:
    rp = r["record"]
    rec, own = E3.merged(rp)
    if rec is None:
        stat["record_unresolved"] += 1
        mon_rows.append(dict(r, status="NOT-FOUND-IN-ARZ")); continue
    tblp = rec.get("charAnimationTableName")
    trec, _ = E3.merged(tblp) if tblp else (None, None)
    if trec is None:
        stat["no_anim_table"] += 1
    ctrlp = rec.get("controller")
    crec, _ = E3.merged(ctrlp) if ctrlp else (None, None)
    if crec is None:
        stat["no_controller"] += 1

    # ---- basic (unarmed) attack animation: weighted duration over Anim1..3
    dur, wt, spd, names = [], [], [], []
    if trec:
        for i in (1, 2, 3):
            a = trec.get(f"unarmedAttackAnim{i}")
            if isinstance(a, str) and a.lower().endswith(".anm"):
                f = frames(a)
                s_ = num(rec.get(f"unarmedAttackAnimSpeed{i}"), 1.0) or 1.0
                w = num(rec.get(f"unarmedAttackAnimWeight{i}"), 0.0) or 0.0
                if f:
                    dur.append(f / FPS / s_); wt.append(w); spd.append(s_)
                    names.append(a.rsplit("/", 1)[-1])
    wsum = sum(wt) or 0
    basic_dur = (sum(d * w for d, w in zip(dur, wt)) / wsum) if wsum else \
                (sum(dur) / len(dur) if dur else None)
    cas = num(rec.get("characterAttackSpeed"), 1.0) or 1.0
    swing = basic_dur / cas if basic_dur else None
    stat["basic_anim_measured" if basic_dur else "basic_anim_NOTFOUND"] += 1

    alt = [p for p in PFX if p != "unarmed" and trec and isinstance(trec.get(p + "AttackAnim1"), str)]

    # ---- special anim ref map, per prefix
    refmap = {}
    if trec:
        for k, v in trec.items():
            m = re.match(r'^([A-Za-z0-9]+?)SpecialAnimRef(\d+)$', k)
            if m and isinstance(v, str):
                an = trec.get(f"{m.group(1)}SpecialAnim{m.group(2)}")
                if isinstance(an, str) and an.lower().endswith(".anm"):
                    refmap.setdefault(v, {}).setdefault(m.group(1), an)
        for p in PFX:
            for nm, fld in (("__spell__", p + "SpellAttackAnim"), ("__buffself__", p + "BuffSelfAnim1"),
                            ("__buffother__", p + "BuffOtherAnim1"), ("__channel__", p + "ChannelAnim")):
                an = trec.get(fld)
                if isinstance(an, str):
                    refmap.setdefault(nm, {}).setdefault(p, an)

    # ---- G6: declared body (mesh), not inferred from anim filename
    mesh = rec.get("mesh") if isinstance(rec.get("mesh"), str) else ""
    mparts = mesh.lower().replace("\\", "/").split("/")
    mesh_body = mparts[-2] if len(mparts) >= 2 else ""
    mesh_file = mparts[-1] if mparts else ""
    stat["mesh_declared" if mesh else "mesh_ABSENT"] += 1

    # ---- attack slots
    SLOTS = [("basic", "attackSkillName", None, None, None, None)]
    for n in ("", "2", "3", "4", "5"):
        SLOTS.append((f"special{n or '1'}", f"specialAttack{n}SkillName", f"specialAttack{n}Chance",
                      f"specialAttack{n}Delay", f"specialAttack{n}Timeout", f"specialAttack{n}Range"))
    SLOTS.append(("initial", "initialSkillName", None, None, None, None))
    SLOTS.append(("dying", "dyingSkillName", None, None, None, None))

    m_direct, m_dot, m_ctrl, m_cls = set(), set(), set(), []
    bands = collections.Counter(); bandsw = collections.Counter()
    nslots = 0
    for slot, fs, fc_, fd, ft, fr in SLOTS:
        sp = rec.get(fs)
        if not (isinstance(sp, str) and sp.lower().endswith(".dbr")):
            continue
        s, _ = E3.merged(sp)
        if s is None:
            stat["skill_unresolved"] += 1; s = {}
        nslots += 1
        san = s.get("skillSpecialAnimationName")
        anmref = anmfr = None; grade = ""
        if isinstance(san, str) and san:
            m = refmap.get(san)
            if m:
                anmref = m.get("unarmed") or list(m.values())[0]; anmfr = frames(anmref)
                grade = "DIRECT-REF" if anmfr else "REF-RESOLVED-ANM-MISSING"
            else:
                grade = "REF-UNSATISFIED-BY-TABLE"
        else:
            grade = "NO-REF"
        fbref = None
        if anmfr is None:
            cls = s.get("Class", "")
            fam = "__spell__" if not cls.startswith(("Skill_AttackWeapon", "Skill_WPAttack",
                                                     "Skill_WeaponPool")) else None
            m = refmap.get(fam) if fam else None
            if m:
                fbref = m.get("unarmed") or list(m.values())[0]
        fbfr = frames(fbref) if fbref else None
        pn = s.get("skillProjectileName"); pv = pd = la = None
        if isinstance(pn, str) and pn.lower().endswith(".dbr"):
            pr, _ = E3.merged(pn)
            if pr:
                pv = num(pr.get("projectileVelocity")); pd = num(pr.get("projectileDistance"))
                la = num(pr.get("launchAngle"))
        stat["slot_" + grade] += 1

        dd, do, dc, nrank = dmg_axes(s)
        m_direct |= set(dd); m_dot |= set(do); m_ctrl |= set(dc)
        skcls = s.get("Class", "")
        if skcls:
            m_cls.append(skcls)
        band = rec.get(fr, "") if fr else ""
        ch = num(rec.get(fc_), 0.0) if fc_ else None
        if band:
            bands[band] += 1
            bandsw[band] += (ch if ch else 0.0)

        slot_rows.append(dict(
            record=rp, display_name=r["display_name"], stratum=r["stratum"],
            slot=slot, skill=sp, skill_class=skcls,
            chance_pct=ch if fc_ else None,
            delay_s=num(rec.get(fd)) if fd else None,
            timeout_s=num(rec.get(ft)) if ft else None,
            range_band=band,
            skill_cooldown_s=num(s.get("skillCooldownTime")),
            skill_active_duration_s=num(s.get("skillActiveDuration")),
            skill_charge_duration_s=num(s.get("skillChargeDuration")),
            instant_cast=s.get("instantCast", ""),
            allows_warmup=s.get("skillAllowsWarmUp", ""),
            warmup_effect=s.get("warmUpEffectName", ""),
            wave_time_s=num(s.get("waveTime")), wave_distance=num(s.get("waveDistance")),
            camera_shake_dur_s=num(s.get("cameraShakeDurationSecs")),
            time_between_attacks_ms=num(s.get("timeBetweenAttacks")),
            target_interval_s=num(s.get("skillTargetInterval")),
            distance_profile=s.get("distanceProfile", ""),
            anim_binding_grade=grade,
            special_anim_ref=san if isinstance(san, str) else "",
            fallback_anm=(fbref or "").rsplit("/", 1)[-1],
            fallback_anm_dur_s=round(fbfr / FPS, 4) if fbfr else "",
            special_anm=(anmref or "").rsplit("/", 1)[-1],
            special_anm_frames=anmfr if anmfr else "",
            special_anm_dur_s=round(anmfr / FPS, 4) if anmfr else "",
            projectile=pn if isinstance(pn, str) else "",
            projectile_velocity=pv, projectile_distance=pd, projectile_launch_angle=la,
            # --- NEW in this lap ---
            damage_types_direct="|".join(t for t in DIRECT if t in dd),
            damage_types_dot="|".join(t for t in DOT if t in do),
            control_effects="|".join(t for t in CTRLFX if t in dc),
            n_damage_ranks=nrank or "",
            skill_radius=num(s.get("skillTargetRadius")),
            skill_max_targets=num(s.get("skillTargetNumber")),
            skill_angle=num(s.get("skillTargetAngle")),
        ))

    # G7: BOTH aggregations emitted; neither is ruled canonical here.
    modal = bands.most_common(1)[0][0] if bands else ""
    wmodal = bandsw.most_common(1)[0][0] if bandsw and sum(bandsw.values()) > 0 else ""
    profile = "|".join(f"{k}:{v}" for k, v in sorted(bands.items(), key=lambda t: -t[1]))

    ctrlvals = {("ctrl_" + c): (crec.get(c) if crec else None) for c in CTRL}
    ctrlvals = {k: (v if isinstance(v, (int, float, str)) else "") for k, v in ctrlvals.items()}

    mon_rows.append(dict(
        record=rp, display_name=r["display_name"], archetype_tag=r["archetype_tag"],
        stratum=r["stratum"], status="OK", arz_owners="|".join(own),
        threat_tier=r["threat_tier"], level_min=r["level_min"], level_max=r["level_max"],
        wave_first=r["wave_first"], wave_last=r["wave_last"],
        n_actors=r["n_actors"], n_champion_actors=r["n_champion_actors"],
        life_modifier_pct_min=r["life_modifier_pct_min"],
        life_modifier_pct_max=r["life_modifier_pct_max"],
        # --- G6: declared body ---
        mesh=mesh, mesh_body=mesh_body, mesh_file=mesh_file,
        mesh_scale=num(rec.get("scale")),
        base_texture=rec.get("baseTexture") if isinstance(rec.get("baseTexture"), str) else "",
        # --- rig (08-08 lineage: inferred from anim filename) ---
        anim_table=tblp or "", controller=ctrlp or "",
        controller_class=(crec or {}).get("Class", ""),
        monster_classification=rec.get("monsterClassification", ""),
        character_attack_speed=cas,
        character_attack_speed_tag=rec.get("characterBaseAttackSpeedTag", ""),
        character_spellcast_speed=num(rec.get("characterSpellCastSpeed")),
        character_run_speed=num(rec.get("characterRunSpeed")),
        walk_speed=num(rec.get("walkSpeed")),
        run_speed_jitter=num(rec.get("characterRunSpeedJitter")),
        disable_movement=rec.get("disableMovement", ""),
        min_rotation_speed=num(rec.get("minRotationSpeed")),
        max_rotation_speed=num(rec.get("maxRotationSpeed")),
        num_attack_slots=num(rec.get("numAttackSlots")),
        n_slots_decoded=nslots,
        waiting_anim_delay_ms=num(rec.get("waitingAnimDelay")),
        death_anim_blend_time=num(rec.get("deathAnimBlendTime")),
        basic_attack_anims="|".join(names),
        basic_attack_anim_weights="|".join(str(x) for x in wt),
        basic_attack_anim_speeds="|".join(str(x) for x in spd),
        basic_attack_anim_durs_s="|".join(f"{d:.4f}" for d in dur),
        basic_attack_dur_s=round(basic_dur, 4) if basic_dur else "",
        basic_swing_period_s=round(swing, 4) if swing else "",
        anim_classes_alt="|".join(alt),
        # --- NEW: rolled-up identity axes ---
        skill_classes="|".join(sorted(set(m_cls))),
        n_skill_classes=len(set(m_cls)),
        damage_types="|".join(t for t in DIRECT if t in m_direct),
        damage_types_nonphysical="|".join(t for t in DIRECT if t in m_direct and t != "Physical"),
        damage_types_dot="|".join(t for t in DOT if t in m_dot),
        control_effects="|".join(t for t in CTRLFX if t in m_ctrl),
        n_control_effects=len(m_ctrl),
        range_band_modal=modal, range_band_chanceweighted=wmodal, range_band_profile=profile,
        # --- life/stat inputs ---
        life_equation=rec.get("charLevel") if isinstance(rec.get("charLevel"), str) else "",
        character_life=num(rec.get("characterLife")),
        character_life_modifier=num(rec.get("characterLifeModifier")),
        bio_record=rec.get("bioDescriptionTag", "") if isinstance(rec.get("bioDescriptionTag"), str) else "",
        pools="|".join(sorted(POOLS.get(rp, []))),
        pool_kinds="|".join(sorted(POOLKIND.get(rp, []))),
        **ctrlvals,
    ))


def dump(fn, rws):
    keys = []
    for r in rws:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rws:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in keys})
    print(fn, len(rws), "rows,", len(keys), "cols")


dump("/tmp/leg_s2/tg2_monster_timing.csv", mon_rows)
dump("/tmp/leg_s2/tg2_attack_slots.csv", slot_rows)
print("stats:", dict(sorted(stat.items())))
