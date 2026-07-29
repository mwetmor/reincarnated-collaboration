import sys
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz
recs=['records/items/gearhead/a03_head002.dbr','records/items/gearshoulders/a03_shoulder01.dbr',
'records/items/geartorso/a02_torso002.dbr','records/items/gearlegs/a02_legs01.dbr',
'records/items/gearfeet/a02_feet02.dbr','records/items/gearhands/a02_hands01.dbr',
'records/items/gearaccessories/waist/a02_waist001.dbr','records/items/gearaccessories/necklaces/b001_necklace.dbr',
'records/items/gearaccessories/rings/a001_ring02.dbr','records/items/gearweapons/blunt1h/b015b_blunt.dbr',
'records/items/gearweapons/shields/b013a_shield.dbr',
'records/items/lootaffixes/prefix/ad003a_res_cold_01.dbr','records/items/lootaffixes/suffix/b_ar014_arje.dbr',
'records/items/lootaffixes/prefix/b_ar022_ar.dbr','records/items/lootaffixes/suffix/a019b_ch_da_02.dbr',
'records/items/lootaffixes/prefix/b_ar030_ar.dbr','records/items/lootaffixes/suffix/b_ar002_ar.dbr',
'records/items/lootaffixes/prefix/b_ar104_ar_a.dbr','records/items/lootaffixes/suffix/b_ar103_ar_a.dbr',
'records/items/lootaffixes/prefix/ao006b_poison_02.dbr','records/items/lootaffixes/suffix/a032c_off_dmg%acid_01_we.dbr',
'records/items/lootaffixes/suffix/a029e_off_dmg%cold_01_ar.dbr','records/items/lootaffixes/suffix/a019a_ch_da_01.dbr',
'records/items/lootaffixes/prefix/aa007a_lifemod_01.dbr','records/items/lootaffixes/prefix/aa010a_damod_01.dbr',
'records/items/lootaffixes/prefix/ao008a_lifeleech_01.dbr','records/items/lootaffixes/suffix/a001a_ch_att_cun_02.dbr',
'records/items/lootaffixes/prefix/aa006a_spimod_01.dbr','records/items/lootaffixes/prefix/aa006b_spimod_01.dbr',
'records/items/lootaffixes/suffix/a005b_ch_att_cunspi_02.dbr']
for r in recs:
    hits=[p for p,a in _arz if r in a.recs]
    flag='  <<< MULTI' if len(hits)>1 else ''
    print(f'{len(hits)}  {r}  {hits}{flag}')
