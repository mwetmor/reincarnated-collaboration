"""MD-B4app-9 step 4 — (a) read GetLifeStateAsText's jump table BYTE-EXACTLY so the
Character_LifeState ordinals are decoded, not assumed sequential; (b) census the callers of the
two RTTI downcast helpers so 'helper-A == as-Player' is corroborated by caller context, not by the
RTTI constant alone.  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
import r3_xref as X   # noqa  (import only for blob reuse below)
pe=D.pe; IB=pe.image_base

print('=== (a) GetLifeStateAsText jump table @ RVA 0x00046f58, 6 entries (cmp eax,5; ja default) ===')
NAMES={0x46ea2:'Life: Unknown',0x46eb9:'Life: Initializing',0x46ed0:'Life: Alive',
       0x46ee7:'Life: Dying',0x46efe:'Life: Dead',0x46f15:'Life: Respawning'}
b=pe.at(0x46f58, 6*4)
for i in range(6):
    t=struct.unpack_from('<I',b,i*4)[0]-IB
    print(f'  index {i} -> {t:#010x}   {NAMES.get(t,"<UNMAPPED — HALT>")}')
print('  default (>5) -> 0x00046f2c   "Life: Illegal"')
