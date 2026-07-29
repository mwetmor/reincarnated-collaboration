import sys,collections
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7')
from lib_corpus import _arz, get
c=collections.Counter(); dc=collections.Counter(); ex=[]
for p,a in _arz:
    for n in a.recs:
        try: rt,f=a.fields(n)
        except: continue
        if f.get('conversionPercentage'):
            seg='/'.join(n.split('/')[1:3])
            c[seg]+=1
        if f.get('defensiveConvert'):
            dc['/'.join(n.split('/')[1:3])]+=1
            if len(ex)<6: ex.append((n,f.get('defensiveConvert'),rt))
print('conversionPercentage carriers by path segment:')
for k,v in c.most_common(20): print(f'   {v:6d}  {k}')
print('\ndefensiveConvert carriers:')
for k,v in dc.most_common(20): print(f'   {v:6d}  {k}')
print('\nexamples:',ex)
# does any ARMOR slot carry conversion?
arm=[ (p,n) for p,a in _arz for n in a.recs
      if n.startswith(('records/items/gearhead','records/items/geartorso','records/items/gearlegs','records/items/gearfeet','records/items/gearhands','records/items/gearshoulders','records/items/gearaccessories'))
      and (a.fields(n)[1].get('conversionPercentage') or 0) ]
print('\narmour/accessory records with conversionPercentage:',len(arm))
for p,n in arm[:10]:
    _,rt,f=get(n); print('   ',n,f['conversionInType'],'->',f['conversionOutType'],f['conversionPercentage'])
