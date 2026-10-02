"""READ-ONLY: vtable slots used as evidence (Pursue state; DoT damage attributes; skill setters)."""
import struct, gdx
D = gdx.D
def vt(name, n):
    base = gdx.EX[name]
    print(f"=== {name} @ RVA {base:#x} ===")
    for i in range(n):
        p = struct.unpack('<I', gdx.pe.at(base + 4 * i, 4))[0] - gdx.IB
        print(f"  +{4*i:#05x}  {p:#010x}  {D.nearest(p)}")
vt('??_7ControllerMonsterStatePursue@GAME@@6B@', 0x50)
vt('??_7ControllerMonsterStateAttack@GAME@@6B@', 0x50)
for n in ['Physical','Bleeding','Fire','Cold','Lightning','Poison','Life','Chaos','Aether','LifeLeach']:
    vt(f'??_7DamageAttributeDur_{n}@GAME@@6B@', 12)
for f in ['?GetDefaultSkillId@ControllerMonster@GAME@@QBEIXZ','?GetNormalSkillId@ControllerMonster@GAME@@QBEIXZ',
          '?GetChainInitialSkill@ControllerMonster@GAME@@QBEIXZ','?GetInitialSkillId@ControllerMonster@GAME@@QBEIXZ']:
    print('\n'.join(gdx.bounded(f)[:2]), ' ;', f)
