#!/usr/bin/env python3
"""RDR Kit Atlas v1 generator.
Cell key = OOD-stable axes: delivery(proxy) x geometry(geo) x commitment(commit).
Ranks kits within contested cells (tier > canon depth > lineage > confidence),
marks representatives, maps mechanics gating vs RDR engine surface (DRAFT for Mac pass).
Re-runnable: drop new canon-corpus-*.jsonl files in outputs/ and re-run."""
import json, glob, csv, statistics, re

def code_attr(v):
    v=(v or '').upper()
    return {'STR':'S','DEX':'D','INT':'I','WIS':'W'}.get(v[:3],'_') if v and v!='N/A' else '_'
def code_range(v):
    v=(v or '').lower()
    if 'melee-radius' in v: return 'M'
    if 'melee' in v: return 'M'
    if 'mid' in v: return 'D'
    if 'ranged' in v: return 'R'
    return '_'
def code_tempo(v): return {'low':'L','med':'M','high':'H'}.get((v or '').lower(),'_')
def code_amp(v):
    v=(v or '').lower()
    if 'flat' in v: return 'F'
    if 'spik' in v: return 'S'
    if 'var' in v: return 'V'
    return '_'
def code_proxy(v): return {'SOLO':'S','LIGHT':'L','HEAVY':'H'}.get(v,'_')
def code_commit(v): return {'INST':'I','WIND':'W','CHAN':'C'}.get(v,'_')  # 'E' reserved: deferred arity-gate
def code_mob(v):
    v=(v or '').lower()
    if 'skill-is' in v.replace('_','-') or 'skill-IS' in (v or ''): return 'K'
    if 'player-verb' in v: return 'P'
    if 'rooted' in v: return 'R'
    if 'high' in v: return 'H'
    if 'med' in v: return 'M'
    if 'low' in v: return 'L'
    return '_'
def code_geo(v): return {'SINGLE':'N','CHAIN':'C','SMALL':'S','LARGE':'L','MULTI':'M'}.get(v,'_')
def code_ctrl(v):
    v=(v or '').lower()
    if 'control-pure' in v: return 'C'
    if 'mixed' in v: return 'M'
    if 'damage' in v: return 'D'
    return '_'
def code_def(v):
    v=(v or '').lower()
    if 'tank' in v: return 'T'
    if 'mitig' in v: return 'M'
    if 'dodg' in v: return 'D'
    if 'glass' in v: return 'G'
    return '_'
ECON_CODE={'self-cost':'SC','path-hybrid':'PB','spend':'SP','ammo':'AM','meter':'MT','reserve':'RS','proc':'PC','dot-walk':'DW','cooldown':'CD','summon':'SU','recipe':'RC','draft':'DR','leech':'LC','stat-weapon':'SW','harvest':'HV'}
def code_elem(v):
    v=(v or '').lower()
    if not v or v=='n/a': return '__'
    if v=='var': return 'VR'
    m={'fire':'FI','cold':'CO','frost':'CO','lightning':'LI','physical':'PH','poison':'PO','shadow':'SH','holy':'HO','arcane':'AR','chaos':'CH','vitality':'VI','aether':'AE','bleed':'BL','pierce':'PI','erosion':'ER','ethereal':'ET','unknown':'__'}
    return m.get(v, (v[:2].upper() if v.isalpha() else '__'))

TIER = {'d2':'T1','poe1':'T1','poe2':'T1','d3':'T1','d4':'T1','le':'T1','gd':'T1',
        'tq':'T2','tl':'T2','chronicon':'T2','hades':'T2','di':'T2b','undecember':'T2b',
        'vs':'T3','hot':'T3'}
TIER_W = {'T1':4,'T2':3,'T2b':2.5,'T3':2}
CANON_W = {'deep-iconic':3,'deep':2,'moderate':1,'negative':0}

def norm_proxy(v):
    v=(v or '').lower()
    if 'heavy' in v: return 'HEAVY'
    if 'light' in v: return 'LIGHT'
    if 'solo' in v: return 'SOLO'
    return 'UNSPEC'
def norm_geo(v):
    v=(v or '').lower()
    if 'melee-radius' in v or 'small' in v: return 'SMALL'
    if 'large' in v: return 'LARGE'
    if 'multi' in v: return 'MULTI'
    if 'chain' in v: return 'CHAIN'
    if 'single' in v: return 'SINGLE'
    if 'zone' in v: return 'LARGE'
    return 'UNSPEC'
def norm_commit(v):
    v=(v or '').lower()
    if 'channel' in v: return 'CHAN'
    if 'wind' in v or 'deferred' in v: return 'WIND'
    if 'instant' in v: return 'INST'
    return 'UNSPEC'

# Mechanics gating rules (first match wins). DRAFT mapping vs RDR engine surface:
# battle-sim auto-aim, soul-control troop command, loot-operator framework,
# rotational/orbital substrate addendum, element-application addendum, reap/possession native.
RULES = [
 (lambda r,c: 'GX-13' in r['gx'], 'have-core', 'reap/possession is RDR-native'),
 (lambda r,c: r['is_union'], 'blocked-new', 'union/recipe evolution system (pair-grain authoring)'),
 (lambda r,c: 'GX-21' in r['gx'] or c[2]=='CHAN', 'blocked-new', 'sustained-stream/channel verb + movement-tax tuning'),
 (lambda r,c: 'GX-09' in r['gx'], 'designed-addendum', 'rotational/orbital substrate addendum — build pending'),
 (lambda r,c: 'GX-19' in r['gx'] or c[0]=='HEAVY', 'partial', 'soul-control troop command exists; turret/pet AI variants + summon economy needed'),
 (lambda r,c: 'GX-03' in r['gx'], 'blocked-new', 'mark/tag ledger + consume-trigger operators'),
 (lambda r,c: 'GX-14' in r['gx'] and 'GX-10' in r['gx'], 'blocked-new', 'lodge/retrieve ammo economy + return-path solver'),
 (lambda r,c: 'GX-14' in r['gx'], 'blocked-new', 'finite-ammo/consumable economy'),
 (lambda r,c: 'GX-10' in r['gx'], 'blocked-new', 'return-path/carom projectile solver'),
 (lambda r,c: 'GX-02' in r['gx'], 'blocked-new', 'form-swap stat-block hotswap'),
 (lambda r,c: 'GX-06' in r['gx'], 'blocked-new', 'self-cost contract operators'),
 (lambda r,c: 'GX-04' in r['gx'], 'blocked-new', 'on-kill resource-spawn economy (corpse/soul ammo)'),
 (lambda r,c: 'GX-07' in r['gx'], 'blocked-new', 'thorns/stat-retaliation channel'),
 (lambda r,c: 'GX-18' in r['gx'], 'partial', 'persistent/mobile zone entities — VFX slot model adjacent; follow-zones new'),
 (lambda r,c: 'GX-11' in r['gx'], 'partial', 'echo/clone actors — troop-command adjacent'),
 (lambda r,c: 'GX-05' in r['gx'], 'partial', 'reservation/aura toggles — loot-operator extension'),
 (lambda r,c: 'GX-12' in r['gx'], 'partial', 'stochastic ops in loot-operator framework — per-cast roll verify'),
 (lambda r,c: 'GX-15' in r['gx'], 'partial', 'element-application addendum covers hybrid caps — status-gate ops verify'),
 (lambda r,c: 'GX-01' in r['gx'], 'partial', 'dash/blink verb — sim support verify; deflect riders new'),
 (lambda r,c: 'GX-17' in r['gx'], 'have-core', 'battle-sim auto-aim native'),
 (lambda r,c: 'GX-20' in r['gx'], 'have-core', 'default-attack scaling native to sim'),
 (lambda r,c: c[0]=='SOLO' and c[2]=='INST', 'have-core', 'direct-hit instant verbs native'),
]

ECON_BUCKETS = [
 ('ammo','ammo|flask|consum|retriev|lodge|reload'),
 ('meter','meter|charge|rage|frenzy|spirit|fury|combo|soul-reserv|heat'),
 ('reserve','reserv|aura|toggle|seal'),
 ('proc','proc|cascade|trigger'),
 ('dot-walk','dot|walk|stack-scal|bleed|burn-stack'),
 ('cooldown','cooldown|window'),
 ('summon','summon|uptime-pass|minion'),
 ('recipe','recipe|union|evolution|relic-gated'),
 ('draft','draft|pool|banish|reroll|offer'),
 ('leech','leech|life-feed|sustain|heal-on'),
 ('self-cost','hp-cost|self-cost|blood-cost'),
 ('path-hybrid','path-hybrid'),
 ('stat-weapon','stat-is|threshold|stat-thresh|block'),
 ('harvest','harvest|magnet|pickup|greed'),
]
def econ_bucket(e):
    e=(e or '').lower()
    for name,pat in ECON_BUCKETS:
        if re.search(pat,e): return name
    return 'spend'

rows=[]
for path in sorted(glob.glob('/mnt/user-data/outputs/canon-corpus-*.jsonl')) + ['/mnt/user-data/outputs/rdr-roster-kits.jsonl']:
    m_ = re.search(r'canon-corpus-(.+)\.jsonl', path)
    corpus = m_.group(1) if m_ else 'rdr-roster'
    tier = TIER.get(corpus,'RDR' if corpus=='rdr-roster' else 'T?')
    for line in open(path):
        line=line.strip()
        if not line: continue
        r=json.loads(line)
        p=r.get('proj',{})
        def ax(k):
            a=p.get(k) or {}
            return (a.get('v'), a.get('c') or 0)
        (pv,pc),(gv,gc),(cv,cc)=ax('proxy'),ax('geo'),ax('commit')
        econ=(p.get('econ') or {}).get('v') or ''
        is_sys = 'system' in (r.get('class') or '') or 'mechanic' in (r.get('class') or '')
        is_union = 'union' in (r.get('class') or '') or 'pair-grain' in econ or 'union' in econ
        gx_list = r.get('gap_refs') or []
        gx=' '.join(gx_list)
        if is_sys:
            cell = ('SYS', re.sub(r'[^a-z0-9-]','',econ.lower())[:24] or 'meta','','')
        else:
            fam = gx_list[0] if gx_list else 'econ:'+econ_bucket(econ)
            cell = (norm_proxy(pv), norm_geo(gv), norm_commit(cv), fam)
        flags=r.get('flags') or []
        canon=r.get('canon_tier','moderate')
        ms=r.get('mech_summary','')
        source=r.get('source','canon')
        rec={'kit_id':r.get('id'),'source':source,'folk_name':r.get('folk_name'),'corpus':corpus,
             'game':r.get('game',corpus),'tier':tier,'canon_tier':canon,
             'negative':bool(r.get('negative')),'flags':';'.join(flags),
             'lineage':r.get('lineage',''),'gx':gx,'is_union':is_union,
             'proxy':pv or '','geo':gv or '','commit':cv or '','econ':econ,
             'mob':(p.get('mob') or {}).get('v') or '','elem_p':(p.get('elem_p') or {}).get('v') or '',
             'avg_conf':round(statistics.mean([pc,gc,cc]),2),
             'spend_stratum':(r.get('canonicity') or {}).get('spend_stratum',''),
             'basin':r.get('basin',''),'meta':r.get('meta',''),
             'power_rating':(r.get('canonicity') or {}).get('power_rating',''),
             'eras':';'.join(r.get('eras') or []),'prov':';'.join(r.get('prov') or []),
             'mech_note':ms[:140]}
        # unique atlas key: 6 sampled | 5 measured | identity elem | 2 reserved
        (tv,_),(av_,__)=ax('tempo'),ax('amp')
        atv=(p.get('attr') or {}).get('v'); rgv=(p.get('range') or {}).get('v')
        dfv=(p.get('def') or {}).get('v'); ctv=(p.get('ctrl') or {}).get('v')
        kparts=[code_attr(atv),code_range(rgv),code_tempo(tv),code_amp(av_),code_proxy(norm_proxy(pv)),code_commit(norm_commit(cv)),
                code_mob(rec['mob']),code_geo(norm_geo(gv)),code_ctrl(ctv),code_def(dfv),
                ECON_CODE.get(econ_bucket(econ),'SP'),code_elem(rec['elem_p'])]
        rec['atlas_key']=''.join(kparts[:6])+'-'+''.join(kparts[6:10])+'-'+kparts[10]+'-'+kparts[11]+'-~~'
        rec['key_completeness']=sum(1 for k in kparts if k not in ('_','__'))
        # rep score
        s = TIER_W.get(tier,1)*10 + CANON_W.get(canon,1)*5 + (2 if (rec['lineage'] or gx) else 0) + rec['avg_conf']*3
        if source in ('roster','bench'): s += 100  # incumbents rank first in-group
        if 'placeholder' in rec['flags']: s = -50
        if rec['negative']: s = -100
        if 'narrow-scope' in flags: s -= 3
        if 'SEARCH-DERIVED' in ms: s -= 2
        rec['_score']=round(s,2); rec['_cell']=cell
        # mechanics
        rec['status']=r.get('status','')
        rec['cross_ref']=r.get('cross_ref','')
        st_txt=(rec['status'] or '').upper()
        if is_sys:
            rec['mechanics_status'],rec['blocking_mechanics']='n/a-system','evidence record — see harvest report'
        elif source=='bench':
            if 'PROMOTED' in st_txt: rec['mechanics_status'],rec['blocking_mechanics']='have-core',f"promoted — mechanism rides F5 build ({rec['cross_ref']})"
            elif 'PENDING RE-CERT' in st_txt: rec['mechanics_status'],rec['blocking_mechanics']='partial','pre-migration kit exists; zero-diff audit then channel-bin re-cert'
            elif 'LAUNCH-SCOPE' in st_txt: rec['mechanics_status'],rec['blocking_mechanics']='blocked-new','E9-C enemy-side consumer — launch scope'
            else: rec['mechanics_status'],rec['blocking_mechanics']='blocked-new',ms[:110]
        elif source=='roster' and 'f5-promotion' in rec['flags']:
            rec['mechanics_status'],rec['blocking_mechanics']='have-core','F5 build carries the mechanism (2026-07-11)'
        else:
            rec['mechanics_status'],rec['blocking_mechanics']='verify','no rule matched — Mac pass to classify'
            for cond,st,bl in RULES:
                if cond(rec,cell): rec['mechanics_status'],rec['blocking_mechanics']=st,bl; break
        rows.append(rec)

# group into cells
cells={}
for rec in rows:
    rec['cell_browse']='|'.join([x for x in rec['_cell'][:3] if x]) + ('\u00d7'+rec['_cell'][3] if len(rec['_cell'])>3 and rec['_cell'][3] else '')
    if 'placeholder' in rec['flags']: gkey='UNPLACED'
    elif rec['_cell'][0]=='SYS': gkey='SYS|'+rec['_cell'][1]
    elif rec['key_completeness']<4: gkey='UNRESOLVED'
    else: gkey=rec['atlas_key']
    rec['_g']=gkey
    cells.setdefault(gkey,[]).append(rec)
for cell,members in cells.items():
    members.sort(key=lambda r:-r['_score'])
    rep_done=False
    for i,m in enumerate(members,1):
        m['cell_id']=m['cell_browse']
        m['key_group']=cell if isinstance(cell,str) else str(cell)
        m['cell_members']=len(members)
        m['rank_in_cell']=i
        m['cell_tier_span']=','.join(sorted({x['tier'] for x in members}))
        m['cell_games']=len({x['game'] for x in members})
        m['cell_neg']=sum(1 for x in members if x['negative'])
        m['representative']=False
        if not rep_done and not m['negative'] and not str(cell).startswith(('SYS','UNPLACED','UNRESOLVED')):
            m['representative']=True; rep_done=True

# order: contested kit-cells first (size desc), SYS annex last
def cell_sort(c):
    k=str(c[0])
    kind = 3 if k=='UNPLACED' else (2 if k=='UNRESOLVED' else (1 if k.startswith('SYS') else 0))
    return (kind, -len(c[1]), k)
ordered=[]
for cell,members in sorted(cells.items(), key=cell_sort):
    ordered.extend(members)

cols=['key_group','atlas_key','status','cross_ref','key_completeness','cell_members','cell_tier_span','cell_games','cell_neg','rank_in_cell','representative','source','cell_id','kit_id','folk_name','corpus','game','tier',
      'canon_tier','negative','flags','lineage','gx','proxy','geo','commit','econ','mob','elem_p','avg_conf',
      'spend_stratum','basin','meta','power_rating','eras','prov','mechanics_status','blocking_mechanics','mech_note']
out='/mnt/user-data/outputs/rdr-kit-atlas-v3.csv'
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore')
    w.writeheader()
    for rec in ordered: w.writerow(rec)

kit_cells=[c for c in cells if not str(c).startswith(('SYS','UNPLACED','UNRESOLVED'))]
contested=[c for c in kit_cells if len(cells[c])>1]
mech={}
reps=[]
for rec in rows:
    if rec.get('representative'): reps.append(rec); mech[rec['mechanics_status']]=mech.get(rec['mechanics_status'],0)+1
print(f"records ingested: {len(rows)}")
print(f"kit cells: {len(kit_cells)} | contested (2+): {len(contested)} | SYS annex cells: {len(cells)-len(kit_cells)}")
print(f"representatives: {len(reps)} | rep tier mix: "+str({t:sum(1 for r in reps if r['tier']==t) for t in ['T1','T2','T2b','T3']}))
print(f"rep mechanics_status: {mech}")
print("top convergence groups: "+str([(cells[c][0]['atlas_key'], len(cells[c])) for c in sorted(kit_cells,key=lambda c:-len(cells[c]))[:8]]))
