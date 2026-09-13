"""Conductor preview: simulate the follow camera + parallax at sample feet positions. python3 sim_view.py DIR out.png"""
import json,sys
from PIL import Image
D=sys.argv[1]; OUT=sys.argv[2]
P=json.load(open(D+'/parallax.json')); W=json.load(open(D+'/walkable.json'))
fg=Image.open(D+'/foreground.png'); cw,ch=fg.size
L=[(l,Image.open(D+'/'+l['file']).convert('RGBA')) for l in sorted(P['layers'],key=lambda l:l['z'])]
K=Image.open('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/cells/idle_S/frames/idle/S/idle_S_00.png').convert('RGBA')
sc=130/240; K=K.resize((round(512*sc),round(512*sc)),Image.LANCZOS)
ax,ay=P['camera']['anchor']
feet=[tuple(W['spawn']),(1000,2880),(3000,1200),(3800,520),(1800,2700),(2600,1900)]
if len(sys.argv)>3: feet=[tuple(map(float,s.split(','))) for s in sys.argv[3:]]
views=[]
for fx,fy in feet:
    cx=min(max(fx-ax,0),cw-1920); cy=min(max(fy-ay,0),ch-1080)
    v=Image.new('RGBA',(1920,1080),(255,0,255,255))
    for l,im in L:
        s=l['scroll_scale']; px,py=l['position']
        v.alpha_composite(im,(round(px-s*cx),round(py-s*cy))) if True else None
    v.alpha_composite(fg,(round(-cx),round(-cy)))
    v.alpha_composite(K,(round(fx-cx-255.5*sc),round(fy-cy-399*sc)))
    views.append(v.convert('RGB').resize((960,540)))
n=len(views); cols=2; rows=(n+1)//2
sheet=Image.new('RGB',(960*cols,540*rows))
for i,v in enumerate(views): sheet.paste(v,((i%cols)*960,(i//cols)*540))
sheet.save(OUT); print(OUT, feet)
