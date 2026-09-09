"""Deterministic geometry references ONLY; never production character artwork."""
from pathlib import Path
import json
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
DIRS=['S','SW','W','NW','N','NE','E','SE']


def guide(direction):
    theta=DIRS.index(direction)*math.pi/4
    rot=np.array([[math.cos(theta),math.sin(theta),0],[-math.sin(theta),math.cos(theta),0],[0,0,1]])
    faces=[]
    light=np.array([-.6,-.35,.8]);light/=np.linalg.norm(light)
    def project(p):return (512+510*p[0],800+510*(-.5*p[1]-.5*p[2]))
    def mesh(vertices,triangles,color):
        v=np.array(vertices)@rot.T
        for tri in triangles:
            points=v[list(tri)];normal=np.cross(points[1]-points[0],points[2]-points[0]);norm=np.linalg.norm(normal)
            if norm<1e-9:continue
            normal/=norm
            if normal@np.array([0,-1,1]) <= 0:
                continue
            shade=.28+.72*max(0,float(normal@light))
            fill=tuple(int(c*shade) for c in color)
            depth=float(points[:,1].mean()-points[:,2].mean())
            faces.append((depth,[project(p) for p in points],fill))
    def ellipsoid(center,radius,color):
        verts=[];tris=[];nlat=12;nlon=20
        for i in range(nlat+1):
            phi=math.pi*i/nlat
            for j in range(nlon):
                t=2*math.pi*j/nlon
                verts.append(np.array(center)+np.array(radius)*[math.sin(phi)*math.cos(t),math.sin(phi)*math.sin(t),math.cos(phi)])
        for i in range(nlat):
            for j in range(nlon):
                a=i*nlon+j;b=i*nlon+(j+1)%nlon;c=(i+1)*nlon+j;d=(i+1)*nlon+(j+1)%nlon
                tris.extend([(a,c,b),(b,c,d)])
        mesh(verts,tris,color)
    def tube(a,b,r,color):
        a=np.array(a);b=np.array(b);axis=b-a;axis/=np.linalg.norm(axis)
        u=np.cross(axis,[0,0,1] if abs(axis[2])<.95 else [0,1,0]);u/=np.linalg.norm(u);v=np.cross(axis,u)
        verts=[];n=16
        for p in (a,b):
            for j in range(n):verts.append(p+r*(u*math.cos(j*2*math.pi/n)+v*math.sin(j*2*math.pi/n)))
        tris=[]
        for j in range(n):
            k=(j+1)%n;tris.extend([(j,k,n+j),(k,n+k,n+j)])
        mesh(verts,tris,color)
    cloth=(95,103,115);leather=(119,105,89);skin=(166,137,112);iron=(108,116,122)
    # Anatomical RIGHT is local -X; no mirrored images.
    ellipsoid((0,0,1.17),(.255,.15,.38),leather)
    ellipsoid((0,.025,.68),(.27,.19,.34),leather)
    ellipsoid((0,0,1.68),(.17,.17,.20),cloth)
    ellipsoid((0,-.139,1.65),(.10,.07,.13),skin)
    ellipsoid((0,-.205,1.67),(.037,.06,.042),skin)
    # Hood peak makes front/back orientation legible without surface decoration.
    ellipsoid((0,.01,1.82),(.13,.12,.07),cloth)
    for side in (-1,1):
        hip=(side*.125,0,.83);knee=(side*.15,-side*.07,.42);ankle=(side*.15,-side*.10,.10)
        tube(hip,knee,.085,cloth);tube(knee,ankle,.067,cloth)
        ellipsoid((side*.15,-side*.10-.055,.055),(.08,.145,.055),leather)
    shoulder=(-.26,0,1.37);elbow=(-.35,-.08,1.10);hand=(-.43,-.16,1.06)
    tube(shoulder,elbow,.088,leather);tube(elbow,hand,.073,leather);ellipsoid(hand,(.066,.058,.075),skin)
    tube((.26,0,1.37),(.30,-.01,1.0),.084,leather);tube((.30,-.01,1),(.30,-.08,.76),.065,leather)
    ellipsoid((.30,-.08,.76),(.057,.055,.08),skin)
    ellipsoid((.29,-.02,.92),(.11,.11,.16),leather)
    tube((-.43,-.16,.03),(-.43,-.16,1.78),.018,iron)
    tube((-.43,-.16,1.74),(-.49,-.16,1.88),.022,(151,143,120))
    tube((-.43,-.16,1.74),(-.38,-.16,1.87),.022,(151,143,120))
    im=Image.new('RGB',(1024,1024),(30,37,48));draw=ImageDraw.Draw(im)
    # Grid axes at 45 degrees give slopes +/-0.5 after the stated squeeze.
    for k in range(-3,4):
        for axis in (0,1):
            pts=[]
            for v in (-1.3,1.3):
                u=k*.3
                x,y=((v+u)/2**.5,(v-u)/2**.5) if axis==0 else ((u+v)/2**.5,(u-v)/2**.5)
                pts.append(project((x,y,0)))
            draw.line(pts,fill=(51,60,74),width=1)
    for _,poly,color in sorted(faces,key=lambda x:x[0],reverse=True):draw.polygon(poly,fill=color)
    draw.text((30,28),f'{direction} | POSE / CAMERA GUIDE ONLY | NOT PRODUCTION ART',fill=(225,225,225))
    draw.line((500,800,524,800),fill=(240,120,145),width=2)
    draw.line((512,788,512,812),fill=(240,120,145),width=2)
    folder=ROOT/'guides';folder.mkdir(exist_ok=True);im.save(folder/f'{direction}.png')


if __name__=='__main__':
    for d in DIRS:guide(d)
    (ROOT/'guides'/'manifest.json').write_text(json.dumps({
        'purpose':'geometry references only, never deliverable painted frames',
        'directions':DIRS,'camera_elevation_deg':45,'vertical_image_compression':2**-.5,
        'projection':'x=512+510*x; y=800+510*(-0.5*y-0.5*z)',
        'ground_grid_axis_slopes':[-.5,.5],'pivot':[512,800],
        'right_hand_local_x':-.43,'light_world_vector':[-.6,-.35,.8]},indent=2)+'\n')
