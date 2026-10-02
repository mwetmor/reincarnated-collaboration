import json,glob,numpy as np,sys
sys.path.insert(0,'.')
from lfl import summary
for L in ['L2','L3']:
    tot=np.zeros((8,2),int); ntr=0; npl=0; nf=0; pw={}
    for f in sorted(glob.glob(f'out/{L}_*-*.json')):
        if f.endswith('0-19.json'): continue
        d=json.load(open(f)); tot+=np.array(d['counts']); ntr+=d['n_tracks']; npl+=d['n_plate_rows']; nf+=d['n_frames']
        for w,v in d['per_wave'].items(): pw[w]=(np.array(pw.get(w,np.zeros((8,2),int)))+np.array(v)).tolist()
    out=dict(layer=L,salts=[0,19],opts={},counts=tot.tolist(),**summary(tot),n_tracks=ntr,n_plate_rows=npl,n_frames=nf,per_wave=pw)
    json.dump(out,open(f'out/{L}_0-19.json','w'),indent=1); print(L,out['inside_300gpx'],out['band_300_600gpx'],out['still_by_band'])
