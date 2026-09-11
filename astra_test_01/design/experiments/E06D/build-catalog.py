from pathlib import Path
import re,json,hashlib
here=Path(__file__).resolve().parent
source=here.parents[3]/'agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md'
s=source.read_text();rows=[]
for match in re.finditer(r'^#### 3\.1\.(\d+) · `([^`]+)`.*?\n(.*?)(?=^#### |^### 3\.2)',s,re.M|re.S):
 number,key,block=match.groups();fields={}
 for label in ['Emitter geometry','L-19','Lifecycle','Tier-1 element-param axis (SPEC-ASSERTED)']:
  line=next((x for x in block.splitlines() if x.startswith('- **'+label+':**')),None)
  fields[label]=line.split(':**',1)[1].strip() if line else None
 rows.append({'id':key,'source_section':'3.1.'+number,'source_constraints':fields,'qualification':'NOT_AUTHORED','frames':[]})
assert len(rows)==24 and all(all(x['source_constraints'].values()) for x in rows)
result={'schema_version':1,'source_path':str(source.relative_to(here.parents[3])),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'status':'derived semantic reference; no style or art qualification','active':rows,'aliases':{'ring':{'id':'circle','flags':{'annulus':True}},'defensive_dash':{'id':'dash_attack','flags':{'defensive':True}}},'held':{'knockback':'No selection; source §3.2','aura:delegate_carried':'Do not author as aura; source §3.1.8 L-41'},'aura_anchors':['caster_centred','world_placed'],'element_invariants':['geometry','count','radius','range','spacing','opacity_ceiling','causality_class']}
(here/'binding-catalog.json').write_text(json.dumps(result,indent=2)+'\n')
