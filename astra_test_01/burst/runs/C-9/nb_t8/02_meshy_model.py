# T8: Meshy multi-image-to-3D from the NB-1 views (front first), A-pose, same settings as the T1 knight (req_knight.json).
import sys, json, base64, subprocess, time, os
v=sys.argv[1] if len(sys.argv)>1 else 'a'; K=os.environ['MESHY_API_KEY']; API='https://api.meshy.ai/openapi/v1/multi-image-to-3d'
uri=lambda p: 'data:image/jpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
req=dict(image_urls=[uri(f'nb_{v}_{n}.jpg') for n in ('front','right','back','left')],ai_model='latest',should_texture=True,enable_pbr=False,pose_mode='a-pose',should_remesh=True,topology='quad',target_polycount=60000)
open(f'req_nb_{v}.json','w').write(json.dumps(req))
def curl(*a): return json.loads(subprocess.run(['curl','-s','--max-time','120',*a,'-H',f'Authorization: Bearer {K}'],capture_output=True,text=True).stdout or '{}')
r=curl('-X','POST',API,'-H','Content-Type: application/json','-d',f'@req_nb_{v}.json'); tid=r.get('result'); print('task',tid,{k:v for k,v in r.items() if k!='result'},flush=True)
t0=time.time()
while tid:
    s=curl(f'{API}/{tid}'); st=s.get('status')
    if st in ('SUCCEEDED','FAILED','CANCELED','EXPIRED') or time.time()-t0>1500: break
    time.sleep(15)
json.dump(s,open(f'res_nb_{v}.json','w'),indent=1)
print(st,'progress',s.get('progress'),'%.0fs'%(time.time()-t0),(s.get('task_error') or {}).get('message',''),flush=True)
g=(s.get('model_urls') or {}).get('glb')
if g: subprocess.run(['curl','-s','-L','-o',f'nb_{v}.glb',g],check=True); print('glb',os.path.getsize(f'nb_{v}.glb'),'bytes')
