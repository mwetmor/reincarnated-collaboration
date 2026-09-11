"""Analytical geometry only. Does not generate, deform, or edit painted artwork."""
import json,math,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
P=Path(__file__).resolve().parent
layout={'id':'chamber-e01-draft-v1','units':'metres (diagnostic proposal)','bounds':[-5,-4,5,4],
 'exits':[{'id':'west','point':[-5,0],'width':2.5},{'id':'east','point':[5,0],'width':2.5}],
 'static_blocks':[{'id':'partition-south','rect':[2,-4,2.3,-1.25],'height':2.5},{'id':'partition-north','rect':[2,1.25,2.3,4],'height':2.5},{'id':'pillar','rect':[-2.5,-2,-1.5,-1],'height':3}],
 'objects':[{'id':'door','rect':[2,-1.25,2.3,1.25],'height':2.5,'initial_state':'locked','states':['locked','closed','opening','open','closing'],'approaches':[[1,0],[3.3,0]]},{'id':'crate','rect':[-0.5,2.3,0.5,3.3],'height':0.9,'initial_state':'intact','states':['intact','broken'],'approaches':[[0,1.3]]},{'id':'chest','rect':[-4,1.5,-3,2.3],'height':0.8,'initial_state':'closed','states':['closed','open','looted'],'approaches':[[-3.5,0.5]]}],
 'actors':[{'id':'mage','point':[0,0],'height':2,'radius':0.35},{'id':'monster','point':[3.6,2.7],'height':2.7,'radius':0.65},{'id':'npc','point':[-3.7,-2.7],'height':2,'radius':0.35}],
 'surfaces':[{'id':'stone','rect':[-5,-4,0,4]},{'id':'soil','rect':[0,-4,5,4]}],
 'status':'DRAFT geometry for comparison; no runtime interaction or art pass; exits are boundary approach points, later links require external clearance'}
(P/'chamber-layout.draft.json').write_text(json.dumps(layout,indent=2)+'\n')
W,H=720,405;anchor=np.array([W*0.5010414505,H*0.5509251234]);body=H*.095
profiles=[('A','Low affine / flatter ground',30,47,False),('B','High affine / recommended probe',52.9535411256,47,False),('C','Godot-informed perspective',52.9535411256,47,True)]
fig,axes=plt.subplots(1,3,figsize=(21.6,6),dpi=100);fig.patch.set_facecolor('#171a1e');out=[]
for ax,(id,title,angle,yaw,persp) in zip(axes,profiles):
 t=math.radians(angle);y=math.radians(yaw);ct,st=math.cos(t),math.sin(t);cy,sy=math.cos(y),math.sin(y)
 focal=H/2/math.tan(math.radians(31.7861018306)/2)
 distance=2*st+focal*2*ct/body
 scale=body/(2*ct)
 def project(u,v,h=0):
  right=cy*u-sy*v;depth=sy*u+cy*v
  fac=focal/(distance-ct*depth-st*h) if persp else scale
  return anchor+fac*np.array([right,st*depth-ct*h])
 def inverse(x,y):
  dx,dy=x-anchor[0],y-anchor[1]
  if persp:
   depth=dy*distance/(focal*st+dy*ct);right=dx*(distance-ct*depth)/focal
  else:depth=dy/(scale*st);right=dx/scale
  return np.array([cy*right+sy*depth,-sy*right+cy*depth])
 def poly(points,fc,ec='#6c737c',lw=.7,z=1):ax.add_patch(Polygon([project(*q) for q in points],closed=True,facecolor=fc,edgecolor=ec,linewidth=lw,zorder=z))
 def rect(r,h=0):a,b,c,d=r;return [(a,b,h),(c,b,h),(c,d,h),(a,d,h)]
 for surf in layout['surfaces']:poly(rect(surf['rect']), '#394249' if surf['id']=='stone' else '#514839')
 for u in range(-5,6):a,b=project(u,-4),project(u,4);ax.plot(*zip(a,b),color='#72736d',lw=.35,zorder=2)
 for v in range(-4,5):a,b=project(-5,v),project(5,v);ax.plot(*zip(a,b),color='#72736d',lw=.35,zorder=2)
 def block(o,color):
  r=o['rect'];h=o['height'];a,b,c,d=r
  poly([(a,b,0),(c,b,0),(c,b,h),(a,b,h)],color,z=4)
  poly([(c,b,0),(c,d,0),(c,d,h),(c,b,h)],color,z=4)
  poly(rect(r,h), '#989a93',z=5)
  x,y=project((a+c)/2,(b+d)/2,h);ax.text(x,y-6,o['id'].split('-')[0],color='#e8e9e6',fontsize=7,ha='center',zorder=8)
 for o in layout['static_blocks']:block(o,'#666b6a')
 for o in layout['objects']:
  if o['id']=='door':poly(rect(o['rect']),'#bf9759',ec='#e2c190',lw=2,z=5)
  else:block(o,'#7c694f')
 for actor in layout['actors']:
  u,v=actor['point'];r=actor['radius'];h=actor['height']
  circle=[(u+r*math.cos(a),v+r*math.sin(a),0) for a in np.linspace(0,math.tau,50)]
  poly(circle,'#b0b8b5',z=6)
  # Known-size volumetric proxy: all corners share the selected projection.
  block({'id':actor['id'],'rect':[u-r/2,v-r/2,u+r/2,v+r/2],'height':h},'#5c8491')
  a,b=project(u,v),project(u,v,h);ax.plot(*zip(a,b),color='#d3eced',lw=1,zorder=8)
 for exit in layout['exits']:
  x,y=project(*exit['point']);ax.scatter([x],[y],s=30,c='#d7b87b',zorder=9);ax.text(x,y+13,exit['id']+' exit',ha='center',color='#f0d9ac',fontsize=7,zorder=9)
 circ=[(-.5+1.2*math.cos(a),-.7+1.2*math.sin(a),0) for a in np.linspace(0,math.tau,70)];poly(circ,'none',ec='#d9b572',lw=1.4,z=7)
 # Equal-height stationary probes at three ground depths. Not animation poses.
 heights=[]
 for depth in [-3,0,3]:
  u,v=sy*depth,cy*depth;aa,bb=project(u,v),project(u,v,2);heights.append(float(aa[1]-bb[1]))
 ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_facecolor('#20252a');ax.set_xticks([]);ax.set_yticks([])
 ax.axhspan(H*.91,H,color='#131619',zorder=10);ax.text(14,H-14,'SAME 9% HUD RESERVE • diagnostic only',color='#aaa',fontsize=8,zorder=11)
 ax.set_title(id+'  '+title,color='#ece9e0',fontsize=12,loc='left',pad=12)
 ax.text(0,-.12, f'2 m body at centre: 9.5% H | ground q={st:.3f}\nNear / centre / far: {heights[2]:.1f} / {heights[1]:.1f} / {heights[0]:.1f} px',transform=ax.transAxes,color='#c3c7ca',fontsize=9,va='top')
 errors=[float(np.linalg.norm(inverse(*project(u,v))-[u,v])) for u in np.linspace(-5,5,11) for v in np.linspace(-4,4,9)]
 out.append({'id':id,'title':title,'type':'pinhole' if persp else 'affine','elevation_deg':angle,'yaw_deg':yaw,'q':st,'screen':[W,H],'anchor':anchor.tolist(),'body_height_fraction':.095,'uniform_scale_px_per_m':None if persp else scale,'vertical_fov_deg':31.7861018306 if persp else None,'distance_m':distance if persp else None,'probe_heights_far_center_near_px':heights,'ground_roundtrip_max_m':max(errors),'note':'C matches recovered angle/lens but recalibrates distance to equal body size; not exact recovered Godot camera. Ground field and all volumetric proxies use same projection; no painted asset is tested.'})
fig.suptitle('ONE LAYOUT • ONE BODY SCALE • THREE PROJECTIONS',x=.02,ha='left',color='#e7e2d8',fontsize=18)
fig.subplots_adjust(top=.9,bottom=.23,left=.02,right=.99,wspace=.08)
fig.text(.02,.025,'Geometry/state preparation for the painted chamber. No textures, character animation, hidden-region art, dynamic sorting or runtime collision are qualified here.',color='#bcc2c6',fontsize=10)
fig.savefig(P/'projection-study.png',facecolor=fig.get_facecolor());fig.savefig(P/'projection-study.svg',facecolor=fig.get_facecolor())
(P/'projection-candidates.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

# Matplotlib emits trailing spaces in SVG paths; retain newline separators.
svg_path=P/'projection-study.svg'
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
