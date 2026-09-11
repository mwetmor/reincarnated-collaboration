from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;data=[json.loads((p/f'evidence/preflight-{m}.json').read_text())for m in ['a','b']];fig,axes=plt.subplots(2,1,figsize=(12,6.5),layout='constrained')
for r,label in zip(data,['A · world palette linear','B · local quaternion slerp']):
 axes[0].plot([x['max_world_error_m']*1000 for x in r['records']],label=label,linewidth=1)
 axes[1].plot([x['bone_error_m']*1000 for x in r['records']],label=label,linewidth=1)
for ax,title in zip(axes,['Error against Blender fractional source (mm)','Bone length error (mm)']):
 ax.axhline(1,color='#a12b25',linestyle='--',label='1 mm limit');ax.set_title(title);ax.set_xlim(0,311);ax.grid(alpha=.2);ax.axvline(96,color='grey',alpha=.3);ax.axvline(240,color='grey',alpha=.3);ax.legend(loc='upper right')
axes[1].set_xlabel('Sample: 0–95 idle; 96–239 walk; 240–311 cast');fig.savefig(p/'evidence/sampler-comparison.png',dpi=100);plt.close(fig)
