#!/usr/bin/env python3
"""JOIN-1 J4b formulas.json writer (D2 Fire Sorceress). Re-uses gen_j4b's verified functions.

Usage: python3 gen_formulas_j4b.py <out_dir>   (needs ./sources from fetch_sources.py)
"""
import json, os, sys, math
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
import tempfile
sys.argv = [sys.argv[0], tempfile.mkdtemp(prefix="j4b_rows_")]  # gen_j4b writes a throwaway primary_rows.json here
sys.path.insert(0, HERE)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gen_j4b as G

FB, ME = G.FB, G.ME

def fb_hit(slvl, fbolt_blvl, met_blvl, mastery):
    syn = 14 * (fbolt_blvl + met_blvl)
    return (G.skill_elem(FB, slvl, syn, mastery) / 256, G.skill_elem(FB, slvl, syn, mastery, "max") / 256)

def me_hit(slvl, fbolt_blvl, fball_blvl, mastery):
    syn = 5 * (fbolt_blvl + fball_blvl)
    return (G.skill_elem(ME, slvl, syn, mastery) / 256, G.skill_elem(ME, slvl, syn, mastery, "max") / 256)

def pyre(slvl, inferno_blvl, mastery):
    a, b = G.pyre_bitrate(slvl, inferno_blvl, mastery), G.pyre_bitrate(slvl, inferno_blvl, mastery, "max")
    return (round(a * 25 / 256, 3), round(b * 25 / 256, 3))

def fcr(x):
    e = min(120 * x // (120 + x), 75)
    d = 256 * (100 + e) // 100
    return math.ceil(256 * 14 / d - 1), math.ceil(7 * 256 / d)

# Sensitivity cases. Hard points 20/20/20 for Fire Ball / Meteor / Fire Mastery = the kit record's anchor quote.
cases = []
for label, plus, esch, fbolt in [
    ("A-low: Eschuta +1 sor, Fire Bolt blvl 1 (forced minimum)", 11, 10, 1),
    ("A-high: Eschuta +3 sor, +20% fire skill dmg, Fire Bolt blvl 20", 13, 20, 20),
    ("B: Heart of the Oak (+3 all, no +% fire), Fire Bolt blvl 20", 13, 0, 20),
    ("Floor: no +skills, no item +%, Fire Bolt blvl 1", 0, 0, 1),
]:
    sl = 20 + plus
    fm = G.ln12(G.FM, sl) + esch
    cases.append({
        "case": label, "item_plus_skills": plus, "effective_slvl_fire_ball_meteor_fire_mastery": sl,
        "fire_mastery_plus_item_pct": fm, "fire_bolt_blvl": fbolt,
        "fire_ball_hit_points": fb_hit(sl, fbolt, 20, fm),
        "meteor_impact_points": me_hit(sl, fbolt, 20, fm),
        "pyre_hp_per_s_per_missile_inferno_blvl1": pyre(sl, 1, fm),
    })

S = {
    "TXT113": "D2 1.13 txt tables, fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9 (code/d2_113_data/); sha256 per file in primary_rows.json",
    "D2MOO": "ThePhrozenKeep/D2MOO @ 5596f5cb6c5251a0a07c6637d26458b06099d516 (reverse-engineered 1.10f DLLs; many symbols mapped to 1.13c). Same commit as J4a.",
    "ARREAT_SORCFIRE": "The Arreat Summit, Sorceress Fire Spells (Blizzard): https://classic.battle.net/diablo2exp/skills/sorceress-fire.shtml",
    "ARREAT_SKILLBASICS": "The Arreat Summit, Skills Basics ('Items that give bonuses to skills and skill levels will not add to Synergy bonuses'): https://classic.battle.net/diablo2exp/skills/basics.shtml",
    "ARREAT_DELAYS": "The Arreat Summit, Casting Delays ('While you're waiting through the Casting Delay you can switch to another spell'; 'nothing you can do to reduce or eliminate the Casting Delay'; Meteor 1.2 s): https://classic.battle.net/diablo2exp/skills/castingdelays.shtml",
    "ARREAT_CHARS": "The Arreat Summit, Basics: Characters (mana fully replenished in 120 s without Regenerate Mana or Warmth): https://classic.battle.net/diablo2exp/basics/characters.shtml",
    "BASIN": "Basin Wiki, https://www.theamazonbasin.com/wiki/index.php?title=<page>, pages Fire_Ball, Meteor, Fire_Bolt, Fire_Mastery, Warmth, Inferno, Resistance, Immune, Sunder, Mana, Sorceress (class table), Spirit, Heart_of_the_Oak, Chains_of_Honor. Accessed 2026-10-01.",
    "BLIZZ_24": "Blizzard, Diablo II: Resurrected Patch 2.4 Balance PTR notes: https://news.blizzard.com/en-us/article/23765907/diablo-ii-resurrected-patch-2-4-balance-ptr-has-ended",
    "MAXROLL_24": "Maxroll, Patch 2.4 notes: https://maxroll.gg/d2/news/patch-2-4-notes",
    "J4A": "agentic_orchestration/legolas/research/2026-10-01-join1-j4a-d2-ww-barb/formulas.json (shared D2 laws, re-used, not redone)",
    "SISTER": "agentic_orchestration/legolas/research/2026-10-01-join1-d2-animation-timing/packet.json (LAW_SORC_FCR, LAW_SORC_FHR, LAW_SORC_FBR, LAW_FIREBALL, LAW_METEOR, LAW_OPERANDS)",
}

F = []
def add(**k):
    k.setdefault("conflicts", []); k.setdefault("open", [])
    F.append(k)

add(id="H01", name="Fire Ball damage per hit (fire), with synergies and mastery",
    version="LoD 1.13, expansion game", label="MODEL-VERIFIED",
    formula=[
        "base_min_256 = (EMin + LB(slvl, EMinLev1..5)) << HitShift ; EMin 12, EMinLev 13/23/28/33/38 ; EMax 28, EMaxLev 15/25/30/35/40 ; HitShift 7 (row 47).",
        "LB(n, L) = level-bracket sum: L1*(n-1) for n<=8; 7*L1 + L2*(n-8) for 9-16; + L3 per level for 17-22; + L4 for 23-28; + L5 for 29+.",
        "synergy S = 14 * (Fire Bolt.blvl + Meteor.blvl) % (row 47 EDmgSymPerCalc '(skill('Fire Bolt'.blvl)+skill('Meteor'.blvl))*par8', Param8 14). blvl = hard points only.",
        "dmg_256 += dmg_256 * S // 100 (applied on the shifted value, i.e. in 1/256 points).",
        "then dmg_256 += dmg_256 * M // 100, where M = passive_fire_mastery = Fire Mastery % + item '+% to Fire Skill Damage' (H04).",
        "roll uniformly in [min, max] (D2MOO SUNITDMG/MISSMODE roll); then target resist law (H08); no to-hit roll (H07).",
        "Display: points = dmg_256/256 (Basin prints half points; Arreat prints floor)."],
    sources=["TXT113 Skills.txt row 47", "D2MOO D2Common D2Skills.cpp SKILLS_GetMinElemDamage / SKILLS_GetMaxElemDamage / SKILLS_CalculateDamageBonusByLevel / SKILLS_CalculateMasteryBonus",
             "BASIN Fire_Ball (bracket formulas + slvl 1-60 table, raw)", "ARREAT_SORCFIRE (slvl 1-20 with the forced Fire Bolt.blvl 1 synergy, +14%)"],
    cross_check="Raw table == Basin slvl 1-60 exactly (min and max); synergy-applied table == Arreat slvl 1-20 exactly with S = 14 (Fire Bolt.blvl 1, forced by prerequisite). primary_rows.json verification_log.",
    d2r_differs="None found. Patch 2.4 (BLIZZ_24, MAXROLL_24) lists no Fire Ball or Fire Bolt change; Basin's current page (2026) prints one table, no D2R column. Patch 3.0 (Reign of the Warlock) summary lists no Sorceress skill changes (DiabloBytes; single secondary source).",
    sensitivity_examples=cases)

add(id="H02", name="Meteor impact damage, AoE and timing",
    version="LoD 1.13, expansion game", label="MODEL-VERIFIED",
    formula=[
        "Same skill-side law as H01 with row 56: EMin 80, EMinLev 23/39/79/81/83; EMax 100, EMaxLev 25/41/81/83/85; HitShift 8.",
        "synergy S = 5 * (Fire Bolt.blvl + Fire Ball.blvl) % (row 56 EDmgSymPerCalc, Param8 5); then mastery M (H04).",
        "Impact AoE radius = aurarangecalc ln12 = Param1 + (slvl-1)*Param2 = 6 + 0 = 6 subtiles = 4 yards at every slvl (meteorcenter sHitPar1 0 = 'range (0 = skill)'). Centered on the target POINT, not a unit.",
        "Timing: cast at the action frame spawns meteorcenter at the target; impact = action + 60 frames (meteorcenter Range 60, AlwaysExplode 1 -> it explodes even if nothing is there). Casting delay 30 frames (Skills delay 30) starting at the action frame.",
        "Every unit in the radius takes one impact hit (D2MOO MISSMODE_SrvHit14 -> area damage); no to-hit roll (H07). Impact then spawns the pyre (H03)."],
    sources=["TXT113 Skills.txt row 56; Missiles.txt meteorcenter", "D2MOO D2Game MissMode.cpp MISSMODE_SrvHit14_MeteorCenter; D2Skills.cpp elemental functions",
             "BASIN Meteor (brackets, 1-60 table, 'Radius (yards) 4', '2.4 second (60 frame) delay between point of casting (action frame) and impact', delay '1.2, global (LoD) / 1.2, local (D2R)')",
             "ARREAT_SORCFIRE ('Casting Delay: 1.2 Seconds', 'Radius 4 yards', slvl 1-20 with forced +10%)", "SISTER LAW_METEOR (timeline)"],
    cross_check="Raw table == Basin 1-60 exactly; +10% table == Arreat 1-20 in 39 of 40 cells (slvl 17 minimum: Arreat 696, code 695, Basin raw 632 agrees with the code). Radius 4 yd: Basin, Arreat and 6 subtiles x 2/3.",
    d2r_differs="Patch 2.4: Meteor's casting delay no longer shared with other delayed skills (BLIZZ_24, MAXROLL_24; Basin 'local (D2R)'). For THIS kit it changes nothing: Fire Ball has no delay, and in LoD a delay blocks only other delayed skills (ARREAT_DELAYS). Damage law unchanged.",
    conflicts=["Arreat slvl 17 minimum impact 696 vs code/Basin-derived 695 (one cell). Trust the code and Basin."],
    sensitivity_examples=cases)

add(id="H03", name="Meteor fire field (pyre): footprint, tick, duration, damage",
    version="LoD 1.13, expansion game", label="MODEL-VERIFIED (partial)",
    formula=[
        "Spawn: on impact, meteorcenter HitSubMissile1 'meteorfire' x 18 at FIXED subtile offsets from the impact point (primary_rows.json missile_notes; D2MOO MISSMODE_CreateMeteor_MoltenBoulderSubmissiles). Each is a static Size-2 missile.",
        "Bit rate per missile per FRAME (25 frames/s), missile-side law: v = EMin 15 + LB(slvl, MinELev 4/5/6/6/6) (max: Emax 25, MaxELev 4/5/6/6/6); v += v * (3 * Inferno.blvl) // 100 IN WHOLE POINTS (meteorfire EDmgSymPerCalc); v <<= HitShift 3; then v += v * M // 100 (ApplyMastery 1). Unit: 1/256 point.",
        "HP per second per overlapping missile = bit_rate * 25 / 256. A target takes damage from every pyre missile it overlaps, every frame (Basin; D2MOO SrvDo05 -> collision each frame).",
        "How many missiles overlap a target depends on its size and position: stationary size-1 target at the impact centre 0; size-2 3 (up to 6); size-3 5 (up to 7) (Basin). Displayed tooltip assumes 3.",
        "Lifetime (code) = Param3 + (slvl-1)*Param4 = 30 + 15*(slvl-1) frames (D2MOO SrvHit14 sets the submissile range). Basin: 14 + 15*slvl frames (one frame shorter).",
        "Missiles.txt DamageRate 41 (/1024): per D2MOO it is copied to STAT_DAMAGE_FRAMERATE and used to SCALE the defender's flat Damage Reduced / Magic Damage Reduced per frame (MDR x 41/1024), not to scale the damage. dParam1 19 = soft-hit chance 19/128 per hit.",
        "Fire Mastery applies to the pyre (ApplyMastery 1). Synergies from Fire Bolt / Fire Ball do NOT apply to the pyre; only Inferno (row 41, pinned operand from charter v0.5.1) does, at +3% per HARD point, truncated in whole points before the shift."],
    sources=["TXT113 Missiles.txt meteorfire, meteorcenter; Skills.txt row 56 Param3/Param4; SkillDesc meteor (descmissile1 meteorfire; dsc3line4 skillname41 'AFDImm' calc 3)",
             "D2MOO MissMode.cpp (SrvHit14, CreateMeteor_MoltenBoulderSubmissiles, SrvDo05, SrvDmg03, FillDamageParams line ~4753 'dwPiercePct = STAT_DAMAGE_FRAMERATE'); SUnitDmg.cpp (flat DR/MDR scaled by dwPiercePct/1024); Missile.cpp MISSILE_GetMinElemDamage",
             "BASIN Meteor ('bit rate * 3 * 25/256'; 18 static size-2 missiles; size-dependent overlap; '+% Pyre Fire Damage 3 * Inferno.blvl'; 'Frames 14 + (15*slvl)'; 'Damage Rate 41/1024')",
             "ARREAT_SORCFIRE ('Fire Damage per second' slvl 1-20; 'Inferno: +3% Average Fire Damage Per Second Per Level')"],
    cross_check="Displayed fire/s == Basin 1-60 exactly (no synergy) and == Arreat 1-20 exactly with Inferno.blvl 1 (+3%, whole-point truncation before the shift). Basin 'Seconds' == (14+15*slvl)/25 for all 60 levels.",
    d2r_differs="None found for the pyre. (D2R 2.4 changed Inferno's own damage, not its +3%/blvl pyre synergy: BLIZZ_24 lists the Inferno change; Basin's current Meteor page keeps 3 * Inferno.blvl.)",
    conflicts=["Lifetime: code 30+15*(slvl-1) vs Basin 14+15*slvl, one frame (carried from the sister packet Q5).",
               "Sister packet LAW_METEOR wording 'damage rate 41/1024 of bit rate per frame' is contradicted by D2MOO and by Basin's own displayed-DPS formula (bit rate x missiles x 25/256, no 41/1024 factor). CORRIGENDUM: DamageRate scales the defender's flat MDR per frame; it does not scale damage."],
    open=["DamageRate's meaning rests on D2MOO (1.10f) alone; Basin lists the value without stating its use. Settle: 1.13 capture against a monster with flat MDR, or read 1.13 D2Game.",
          "Overlap count per target is geometry-dependent; the adapter must either model the 18 offsets or adopt Basin's '3' as a declared simplification (gamora's call)."])

add(id="H04", name="Fire Mastery and item '+% to Fire Skill Damage'",
    version="LoD 1.13", label="MODEL-VERIFIED",
    formula=[
        "Fire Mastery (row 61) passivestat1 passive_fire_mastery (ItemStatCost id 329) = ln12 = 30 + 7*(slvl-1) %.",
        "Item '+x% to Fire Skill Damage' = Properties 'extra-fire' -> the SAME stat passive_fire_mastery, so it ADDS to Fire Mastery's % (Eschuta's Temper extra-fire 10-20).",
        "Applied AFTER synergy, multiplicatively with it: dmg = base * (1 + S/100) * (1 + M/100) with floors in 1/256 points (D2MOO SKILLS_Get*ElemDamage then SKILLS_CalculateMasteryBonus; Basin 'applies to fire skill damage of user after any synergy bonus').",
        "Applies to Fire Ball, Meteor impact and the pyre (meteorfire ApplyMastery 1). Applied when the missile is CREATED (Basin).",
        "In 1.13 Fire Mastery does NOT lower enemy fire resistance (row 61 has one passive stat; contrast Cold Mastery's pierce)."],
    sources=["TXT113 Skills row 61; ItemStatCost passive_fire_mastery; Properties extra-fire; UniqueItems Eschuta's temper", "D2MOO D2Skills.cpp, Missile.cpp (APPLYMASTERY)",
             "BASIN Fire_Mastery (23+7*slvl; slvl 1-60 table; 'after any synergy bonus')", "ARREAT_SORCFIRE (Fire Mastery 1-20 table)"],
    cross_check="Fire Mastery % == Basin 1-60 and Arreat 1-20 exactly.",
    d2r_differs="None found (not in the 2.4 change list; Basin page unchanged).")

add(id="H05", name="Synergy law and forced minima",
    version="LoD 1.10-1.14d (1.13 data)", label="MODEL-VERIFIED",
    formula=[
        "Synergies read blvl = hard (base) points only; '+skills' items do not add to synergy bonuses.",
        "Fire Ball: +14% per blvl of Fire Bolt and of Meteor. Meteor impact: +5% per blvl of Fire Bolt and of Fire Ball. Pyre: +3% per blvl of Inferno. Fire Bolt (operand only): +16% per blvl of Fire Ball and Meteor.",
        "Prerequisites (verbatim reqskill columns: Meteor <- Fire Ball + Fire Wall; Fire Ball <- Fire Bolt; Fire Wall <- Blaze; Blaze <- Inferno) force Fire Bolt, Fire Ball, Inferno, Blaze and Fire Wall >= 1 hard point for any Meteor caster, so the minimum synergies are Fire Ball +14% (with Meteor >= 1 hard point: +28%), Meteor +10%, pyre +3%.",
        "Synergy sums are additive within a skill (one S per skill)."],
    sources=["TXT113 Skills EDmgSymPerCalc (rows 36, 47, 56) + Missiles meteorfire; reqskill columns", "ARREAT_SKILLBASICS ('Items that give bonuses to skills ... will not add to Synergy bonuses')", "BASIN Fire_Ball / Meteor ('14 * (Fire Bolt.blvl+Meteor.blvl)', '5 * (Fire Bolt.blvl+Fire Ball.blvl)', '3 * Inferno.blvl')"],
    cross_check="Arreat's tables reproduce exactly only with the forced-minimum synergies (H01-H03 checks).",
    d2r_differs="None found for these synergies.")

add(id="H06", name="Fire Ball projectile and explosion",
    version="LoD 1.13", label="MODEL-VERIFIED (partial)",
    formula=[
        "Missile 'fireball': Vel 20 = MaxVel 20 (px/frame), Range 50 frames (2.0 s lifetime), Size 1, CollideType 3, CollideKill 1 (dies on first unit or wall).",
        "On hit, server explosion radius = sHitPar1 4 subtiles = 2 2/3 yards, centred on the MISSILE's position at impact, not on the struck unit's centre (D2MOO MISSMODE_SrvHit01 area damage at the missile's X/Y; Basin). Every unit in radius takes one hit; the struck unit included if inside.",
        "Spawned at the cast's action frame (sister LAW_SORC_FCR); damage per H01; no to-hit (H07)."],
    sources=["TXT113 Missiles fireball", "D2MOO MissMode.cpp MISSMODE_SrvHit01_Fireball", "BASIN Fire_Ball ('Radius (Yards) 2 2/3'; 'Explosion is centered on point of impact rather than target'; same velocity, range and size as Fire Bolt)", "SISTER LAW_FIREBALL"],
    cross_check="Basin 2 2/3 yd == 4 subtiles x 2/3 (sister's conversion).",
    d2r_differs="None found.",
    conflicts=["Arreat prints 'Radius (yards): 1' for Fireball. Data (4 subtiles) and Basin (2 2/3 yd) agree against it; trust data + Basin."],
    open=["Travel distance in yards: Vel*Range/32 = 31.25 (d2mods convention, sister packet) is approximate; yard conventions differ."])

add(id="H07", name="Hit law for her missiles: no to-hit roll, no monster block",
    version="LoD 1.13", label="MODEL-VERIFIED (partial)",
    formula=[
        "fireball, meteorcenter and meteorfire have an EMPTY Missiles.txt 'ToHit' field. D2MOO rolls to-hit for a missile only when that field is set, so these always hit (no AR vs Defense; J4A F04/F05 do not apply).",
        "Block: D2MOO passes bBlock = (physical damage != 0) into the block/dodge check for missile damage; her missiles carry no physical damage, so block is skipped (only the movement-evade path remains, which monsters lack unless they carry passive evade).",
        "Spells cannot be reduced by Defense; mitigation is the resist law (H08) and flat MDR (J4A F06; scaled by DamageRate for the pyre, H03)."],
    sources=["TXT113 Missiles fireball/meteorcenter/meteorfire (ToHit empty)", "D2MOO MissMode.cpp (missile collision: 'if (pMissilesTxtRecord->nToHit) ... SUNITDMG_IsHitSuccessful'; line ~4707 'SUNITDMG_ApplyBlockOrDodge(..., pDamage->dwPhysDamage != 0)')",
             "BASIN Pierce page ('whenever a hit check is successful or skipped (auto-hit)': auto-hit missiles exist; does not name these missiles)"],
    cross_check="The auto-hit clause has data + code; the community statement is generic.",
    d2r_differs="None found.",
    open=["No second source names Fire Ball/Meteor as auto-hit explicitly, and the area-damage callback path (sub_6FCF5DE0) was not traced for block. Settle: read that callback, or a 1.13 test vs a high-block monster."])

add(id="H08", name="Monster fire resistance, immunity, and -enemy fire resist (1.13)",
    version="LoD 1.13, expansion game", label="MODEL-VERIFIED",
    formula=[
        "dmg_after = max(0, dmg - flat MDR) x (100 - res)/100, then absorb (J4A F07 law, unchanged). MONSTER res = MonStats ResFi / ResFi(N) / ResFi(H) (+ curses/auras); floor -100; capped at 100 at application; res >= 100 = IMMUNE (zero fire damage).",
        "Item '-x% to Enemy Fire Resistance' (Properties pierce-fire -> passive_fire_pierce) is subtracted ONLY if the monster's res < 100. Against an immune it applies NOTHING. (D2MOO SUNITDMG_ApplyResistancesAndAbsorb: 'nResValue < 100 || !bDefenderIsMonster'.)",
        "Only skills that apply 'Resist -%' (Lower Resist curse, Conviction aura) reduce an immune's resist, and against an inherent or Unique-bonus immunity their SUM is cut to 1/5 (Basin Immune: -126 total -> -25). Once res < 100, item -% enemy res then applies in full.",
        "THIS KIT carries no -enemy fire resist in 1.13: none of the named items (Eschuta's Temper, Heart of the Oak, Spirit, Chains of Honor, Harlequin Crest, Magefist, Arachnid Mesh, Mara's Kaleidoscope) has pierce-fire, and the kit has no curse or aura. So -fire res = 0 against everything, and 0 against immunes.",
        "No difficulty penalty applies to monster resist (the 0/-40/-100 penalty is players/hirelings only; J4A F07)."],
    sources=["D2MOO SUnitDmg.cpp SUNITDMG_ApplyResistancesAndAbsorb", "TXT113 UniqueItems/Runes/Properties (no pierce-fire on any kit item)", "BASIN Resistance ('Resist > 99% makes a unit immune'; floor -100)", "BASIN Immune (removal: 1/5 rule; '-% Enemy Resistance equipped now applies at full effectiveness' only once immunity is removed)", "J4A F07"],
    cross_check="Code and Basin agree on: items do not pierce immunity; skill -res 1/5 vs immunes; floor -100.",
    d2r_differs="D2R adds Sunder charms (Basin Sunder: 'D2R only'): Flame Rift sets a fire-immune monster's resist to 95 before other -res, after which Lower Resist/Conviction act at 1/5 and items in full. Maxroll S14 lists Flame Rift in this build's charms. NOT available in 1.13: a material home-game difference for a pure-fire kit (see c12b_home_frontier.md).",
    datamined_examples={"uberdiablo ResFi(H)": "110 (immune; the kit cannot damage Uber Diablo in 1.13)", "mephisto ResFi(H)": "75", "diablo ResFi(H)": "50", "baalcrab ResFi(H)": "50", "andariel ResFi(H)": "-50", "ubermephisto / uberbaal ResFi(H)": "75"})

add(id="H09", name="Mana pool, mana regeneration, and Warmth",
    version="LoD 1.13", label="MODEL-VERIFIED",
    formula=[
        "Sorceress mana (CharStats, 'in fourths'): start = Energy 35 -> 35 mana; ManaPerLevel 8 = +2 per clvl; ManaPerMagic 8 = +2 per Energy. max_mana = (35 + 2*(clvl-1) + 2*(Energy-35) + flat item mana) x (1 + item_maxmana_percent/100) (op 11 on maxmana, as J4A F12).",
        "Regeneration per frame (D2MOO EVENTS_ManaRegen): mult = max(1, floor(max_mana_256 / (25 * ManaRegen))) with ManaRegen 120; regen_256 = floor(mult * (100 + manarecoverybonus) / 100) + manarecovery. I.e. full refill in ~120 s at 0% bonus.",
        "manarecoverybonus = Warmth (37: 30 + 12*(slvl-1) %) + item 'Regenerate Mana %' (regen-mana, same stat; Magefist 25). The bonuses ADD.",
        "Costs: Fire Ball (9 + slvl)/2 mana; Meteor (33 + slvl)/2 mana (rows 47/56 mana, lvlmana, manashift 7). Fire Ball needs no delay; Meteor's 30-frame delay is not shortened by FCR (ARREAT_DELAYS)."],
    sources=["TXT113 CharStats Sorceress; Skills rows 37/47/56; ItemStatCost manarecoverybonus/maxmana/energy", "D2MOO PlrModes.cpp EVENTS_ManaRegen",
             "ARREAT_CHARS ('fully replenished in 120 seconds' without Regenerate Mana or Warmth)", "BASIN Warmth ('Adds to Regenerate Mana +% applied by Meditation and items'; 18+12*slvl; 1-60)", "BASIN Sorceress class table (Mana 35, +2/level, +2/Energy; Life 40, +1/level, +2/Vitality)", "ARREAT_SORCFIRE (Warmth 1-20; 'BaseRegenrate*(100%+Warmth)+item')"],
    cross_check="Warmth % == Basin 1-60 and Arreat 1-20; mana costs == Basin 1-60 (both castables) and Arreat 1-20.",
    d2r_differs="None found for Warmth or the regen law (Warmth absent from the 2.4 change list; Basin page unchanged since 2012).",
    open=["The flooring of mult = max_mana_256 / 3000 makes the true refill time slightly longer than 120 s; exact per-frame regen at a pinned max_mana is computable once Energy/clvl/items are pinned."])

add(id="H10", name="Cast cadence, FCR, FHR, FBR (pointer)",
    version="LoD 1.13 (D2R identical)", label="MODEL-VERIFIED",
    formula=["Shield block (Sorceress BL mode; SISTER LAW_SORC_FBR) is EXCLUDED under the pin (charter v0.5.1): a named fidelity cost, not modelled, even though the kit record carries a Spirit Monarch shield.", "See SISTER LAW_SORC_FCR (13/12/11/10/9/8/7 ticks at FCR 0/9/20/37/63/105/200; action tick 7/6/5/4 at 0/20/63/200), LAW_SORC_FHR, LAW_SORC_FBR, LAW_METEOR (cooldown from the action frame; impact action+60).",
             "Pinned-gear cadence: H11 / README section 3 derive FCR 105-115 from the kit record's named items -> 8 ticks per cast (0.32 s), action tick 5 (0.20 s); Meteor re-cast no sooner than action + 30 = 35 frames after the previous Meteor's cast start."],
    sources=["SISTER (reproduced Maxroll + Basin tables exactly)", "ARREAT_DELAYS"],
    cross_check="Re-used, not redone.", d2r_differs="FCR law identical (sister).")

add(id="H11", name="Shared D2 laws re-used from J4a (pointers only)",
    version="LoD 1.13", label="MODEL-VERIFIED",
    formula=["J4A F07 elemental resistance law (player side: difficulty penalty 0/-40/-100, caps, absorb).", "J4A F06 flat DR/MDR (MDR applies to her fire damage; H03 scaling for the pyre).",
             "J4A F12 life/mana op law (op 8/9/11) — Sorceress operands in H09.", "J4A F13 leech: NOT exercised by this kit (no leech on any named item; spell damage does not leech in D2).", "J4A F15 FCR/FHR pointer; sister packet laws."],
    sources=["J4A", "SISTER"], cross_check="Re-used, not redone.", d2r_differs="See J4a.",
    open=["'Spell damage does not leech' is stated from common knowledge, NOT re-sourced here; leech is irrelevant to this kit since no named item carries it. If a profile adds leech, source it first."])

DT = {
    "H01": "FIRE only (Skills#47 EType fire; no MinDam/MaxDam = no physical; no SrcDam = no weapon damage; no ELen = no burn).",
    "H02": "FIRE only (Skills#56 EType fire; no physical columns; no SrcDam; no ELen).",
    "H03": "FIRE only, per frame (Missiles meteorfire EType fire; no physical columns).",
    "H04": "Modifies FIRE only (passive_fire_mastery is read for ELEMTYPE_FIRE).",
    "H05": "Modifies FIRE only (all synergies listed are '+% Fire Damage').",
    "H06": "FIRE only (carries H01's damage).",
    "H07": "n/a (hit law). Her missiles carry zero PHYSICAL, which is why block is skipped.",
    "H08": "FIRE resistance law (the only damage type this kit emits).",
    "H09": "n/a (resource).",
    "H10": "n/a (timing).",
    "H11": "n/a (pointers).",
}
for f in F:
    f["damage_type"] = DT[f["id"]]
summary = [{"id": f["id"], "name": f["name"], "label": f["label"], "version": f["version"]} for f in F]
out = {
    "schema": "join1-j4b-formulas/v1", "date": "2026-10-01", "author": "legolas (UNKNOWN-RESEARCHER)",
    "commissioner": "gandalf, Run JOIN-1 wave J4b (charter J-S3b: 'the D2 formula set (MODEL-VERIFIED)')",
    "game_version": "Diablo II: Lord of Destruction, expansion game, 1.13 txt data (fabd/diablo2 @ 45112569). JOIN-1 law is LoD 1.13 (KP-160 Q10). D2R differences flagged per formula.",
    "tick": "25 frames per second; 1 frame = 0.04 s",
    "labels": {"DATAMINED": "Read directly from the 1.13 txt files, or a structure read directly from D2MOO source.",
               "MODEL-VERIFIED": "Structure from D2MOO AND confirmed by at least one independent community source (Arreat and/or Basin); where a published table exists it was reproduced numerically (primary_rows.json verification_log).",
               "MODEL-VERIFIED (partial)": "Core has two sources; a named sub-clause has one, or sources conflict on it. Flagged inline.",
               "INFERRED": "Derived here from labelled inputs; derivation stated.", "UNKNOWN": "Not established; what would settle it is stated."},
    "scope": "Charter v0.5.1: castable rows 47 Fire Ball, 56 Meteor; operand rows 36 Fire Bolt, 61 Fire Mastery, 37 Warmth, 41 Inferno (added v0.5.1); prerequisite rows 51 Fire Wall, 46 Blaze (floor 1); Teleport 54 excluded; shield block excluded (fidelity cost).", "damage_type_rule": "W1: every formula carries an explicit damage_type. This kit emits FIRE only; no physical, magic, cold, lightning, poison, burn or leech component exists on any castable row or its server missiles.", "sources": S, "formulas": F, "summary_table": summary,
    "sensitivity_note": "sensitivity_examples are INFERRED (computed from the verified laws with the stated assumptions; hard points 20 in Fire Ball/Meteor/Fire Mastery per the kit record's anchor quote; Meteor.blvl 20 / Fire Ball.blvl 20 for synergies). They show which UNPINNED values move her numbers; they are not pins.",
}
json.dump(out, open(os.path.join(OUT, "formulas.json"), "w"), indent=1, ensure_ascii=False)
for c in cases:
    print(c)
print(fcr(105), fcr(115), fcr(0))
print(len(F), [f["label"] for f in F])
