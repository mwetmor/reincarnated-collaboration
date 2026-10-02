"""Dump the Edition-IV Game.dll disassembly that carries Leg 2's composition decode. READ-ONLY."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import gd_dis as G
SITES = [
 ("DamageAttributeAbsMod_TotalDamageModifier::AddModifierToAccumulator (TDM expands into per-type mods)", 0x1801899d0, 0x180189eb5),
 ("DamageAttributeAbsMod::AddModifierToAccumulator (a per-type % modifier: ONE AbsDamageMod of its own type)", 0x180177360, 0x180177451),
 ("CombatAttributeAccumulator::ModifyDamage loop (every modifier but type 0x3d Executes on every row)", 0x1801061df, 0x180106294),
 ("CombatAttributeAbsDamageMod::Execute / CombatAttributeDurDamageMod::Execute", 0x180101d70, 0x180101d8e),
 ("CombatAttributeDurDamageMod::Execute", 0x180101eb0, 0x180101ed3),
 ("CombatAttributeAbsDamage::ModifyAbsoluteDamage (pct += v into +0x2c)", 0x1801007e0, 0x1801007f0),
 ("CombatAttributeDamage_BasePhysical::ModifyAbsoluteDamage (type 2 -> +0x48, 3 -> +0x4c, 4 -> +0x50)", 0x1801042c0, 0x1801042f0),
 ("CombatAttributeDurDamage::ModifyDurationDamage (DoT pct += v into +0x34)", 0x180101240, 0x18010125a),
 ("CombatAttributeAbsDamageElemental::Process head (pct on UNSCALED base, then magical equation, then ADD)", 0x180100a50, 0x180100ba5),
 ("CombatAttributeAbsDamageElemental::Process (add + DamageScaleInfo + attacker DR max-rule)", 0x180100ba5, 0x180100d10),
 ("CombatAttributeDurDamageElemental::Process head (DoT: same additive form, magical-duration equation)", 0x1801015e0, 0x180101760),
 ("Skill::CollectCombatParameters: crit-dmg (type 0x3b) -> ParametersCombat+0xa0; attacker DR read; Process loop", 0x180485bce, 0x180485cb4),
 ("CombatManager::TakeAttack: crit multiplier += ParametersCombat+0xa0 only when crit; DamageMultiplier 0x3d scale only if > 100", 0x18010b92c, 0x18010b9d9),
 ("type ids: CritDamageModifier / TotalDamageModifier / DamageMultiplier GetType", 0x180189ec0, 0x180189ec6),
 ("", 0x180189970, 0x180189976), ("", 0x180189190, 0x180189196),
]
for title, a, b in SITES:
    print(f"\n## {title}\n; fn {G.nm(a) or ''}")
    print("\n".join(l for l in G.dis(a, b) if "int3" not in l))
