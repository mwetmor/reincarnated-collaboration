"""Conductor glue: clip T3k walkable polygons to a rect inset from the canvas so the complement leaves a solid frame
(Godot drops sub-pixel sliver collision pieces, which would open exits off-canvas). usage: clip_walkable.py in.json out.json inset"""
import json, sys
w=json.load(open(sys.argv[1])); m=float(sys.argv[3]); W,H=w['canvas_size']
def clip(poly, inside, inter):
    out=[]
    for i in range(len(poly)):
        a=poly[i-1]; b=poly[i]
        if inside(b):
            if not inside(a): out.append(inter(a,b))
            out.append(b)
        elif inside(a): out.append(inter(a,b))
    return out
def lx(x0):
    return (lambda p,s: s*(p[0]-x0)>=0, lambda a,b: [x0, a[1]+(b[1]-a[1])*(x0-a[0])/(b[0]-a[0])])
def ly(y0):
    return (lambda p,s: s*(p[1]-y0)>=0, lambda a,b: [a[0]+(b[0]-a[0])*(y0-a[1])/(b[1]-a[1]), y0])
def clean(p):
    q=[]
    for v in p:
        v=[round(v[0],2),round(v[1],2)]
        if not q or v!=q[-1]: q.append(v)
    if len(q)>1 and q[0]==q[-1]: q.pop()
    changed=True
    while changed and len(q)>=3:
        changed=False
        for i in range(len(q)):
            a,b,c=q[i-1],q[i],q[(i+1)%len(q)]
            cr=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
            if abs(cr)<1e-6:
                q.pop(i); changed=True; break
    return q
res=[]
for p in w['walkable']:
    for f,s in ((lx(m),1),(lx(W-m),-1)):
        ins,itr=f; p=clip(p,lambda v,ins=ins,s=s: ins(v,s),itr)
    for f,s in ((ly(m),1),(ly(H-m),-1)):
        ins,itr=f; p=clip(p,lambda v,ins=ins,s=s: ins(v,s),itr)
    p=clean(p)
    if len(p)>=3: res.append(p)
w['walkable']=res
json.dump(w,open(sys.argv[2],'w')); print(len(res),[len(p) for p in res])
