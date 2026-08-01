#!/usr/bin/env python3
"""P17 - Q1 aggregation by area-path token. READ-ONLY."""
import json, collections, re
camp=json.load(open("campaign_rows.json"))
def area(r):
    p=r['path'].replace("records/proxies/","")
    seg=p.split("/")[0]
    m=re.search(r"_(area[a-z])_",p)
    if m: return f"{seg}:{m.group(1)}"
    return seg
agg=collections.defaultdict(list)
for r in camp: agg[area(r)].append(r)
print(f"{'area token':26s} {'n':>4} {'nProxy':>6} {'nAmb':>5} {'maxCeil':>7} {'maxGrp':>6} {'meanE':>7} {'p90E':>6}")
rows=[]
for k,v in agg.items():
    pr=[r for r in v if r['cls']=='Proxy']; am=[r for r in v if r['cls']=='ProxyAmbush']
    mc=max((r['ceiling'] for r in pr),default=0)
    mg=max((r['ambush']['maxGroupSize'] for r in am),default=0)
    es=sorted(r['expTotal'] for r in pr)
    me=sum(es)/len(es) if es else 0
    p90=es[int(0.9*(len(es)-1))] if es else 0
    rows.append((k,len(v),len(pr),len(am),mc,mg,me,p90))
for k,n,np_,na,mc,mg,me,p90 in sorted(rows,key=lambda x:-max(x[4],x[5])):
    print(f"{k:26s} {n:4d} {np_:6d} {na:5d} {mc:7.0f} {mg:6.0f} {me:7.2f} {p90:6.2f}")
print("\n### grand totals")
pr=[r for r in camp if r['cls']=='Proxy']
print(f" Proxy n={len(pr)}  ceiling: max={max(r['ceiling'] for r in pr):.0f} "
      f"mean={sum(r['ceiling'] for r in pr)/len(pr):.2f}")
import statistics as st
print(f" Proxy E[total]: median={st.median(r['expTotal'] for r in pr):.2f} mean={sum(r['expTotal'] for r in pr)/len(pr):.2f}")
am=[r for r in camp if r['cls']=='ProxyAmbush']
print(f" ProxyAmbush n={len(am)} maxGroupSize: max={max(r['ambush']['maxGroupSize'] for r in am):.0f} "
      f"median={st.median(r['ambush']['maxGroupSize'] for r in am):.0f}")
