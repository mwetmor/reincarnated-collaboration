# Test 4b (R-C9-66): Ludo on the SAME inputs as the Kling test (fal_t4): knight E still + our Meshy carry-walk drive video.
# Uploads via /assets/uploads (free), submits 3 jobs, long-polls, downloads every result URL. Key from env, never printed.
import os, json, time, subprocess, pathlib, urllib.request
K=os.environ['LUDO_API_KEY']; API='https://api.ludo.ai/api'; H=['-H',f'Authorization: ApiKey {K}']
T4=pathlib.Path('../fal_t4')
def call(method,path,body=None,q=''):
    cmd=['curl','-s','--max-time','90','-X',method,*H,f'{API}{path}{q}']
    if body is not None: cmd+=['-H','Content-Type: application/json','-d',json.dumps(body)]
    out=subprocess.run(cmd,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'raw':out[:500]}
def upload(p,mime):
    b=pathlib.Path(p).read_bytes(); r=call('POST','/assets/uploads',{'mime_type':mime,'size':len(b)})
    subprocess.run(['curl','-s','--max-time','120','-X','PUT','-H',f'Content-Type: {mime}','--data-binary',f'@{p}',r['upload_url']],check=True)
    return r['file_url']
img=upload(T4/'knight_E_ref_1024.png','image/png'); vid=upload(T4/'knight_carrywalk_E_drive.mp4','video/mp4')
common=dict(frames=64,frame_size=0,loop=False,gif=True,individual_frames=True,spritesheet_with_background=True)
jobs={
 'tm_hydra':('/assets/sprite/transfer-motion',dict(image=img,video=vid,model='hydra',duration=5,prompt='the pollaxe stays rigid, carried in both hands',request_id='c9-t4b-tm-hydra-1',**common)),
 'tm_forge':('/assets/sprite/transfer-motion',dict(image=img,video=vid,model='forge',duration=5,prompt='the pollaxe stays rigid, carried in both hands',request_id='c9-t4b-tm-forge-1',**common)),
 'anim_hydra':('/assets/sprite/animate',dict(initial_image=img,motion_prompt='walking',model='hydra',duration=3,request_id='c9-t4b-anim-hydra-1',**{**common,'frames':36})),
}
ids={}
for name,(path,body) in jobs.items():
    r=call('POST',path,body); ids[name]=r.get('id'); print(name,'submitted',r.get('id'),r.get('status'),r.get('message',''),flush=True)
    json.dump({'request':{k:v for k,v in body.items()},'submit':r},open(f'{name}_submit.json','w'),indent=1)
for name,jid in ids.items():
    if not jid: continue
    t0=time.time()
    while True:
        j=call('GET',f'/assets/jobs/{jid}',q='?wait=60')
        if j.get('status') in ('succeeded','failed','canceled') or time.time()-t0>1800: break
    json.dump(j,open(f'{name}_job.json','w'),indent=1)
    print(name,j.get('status'),'credits',j.get('credits_charged'),'s=%.0f'%(time.time()-t0),(j.get('error') or ''),flush=True)
    res=j.get('result') or {}
    res=res[0] if isinstance(res,list) and res else res
    d=pathlib.Path(name); d.mkdir(exist_ok=True)
    for k,v in (res.items() if isinstance(res,dict) else []):
        urls=v if isinstance(v,list) else [v]
        for i,u in enumerate(urls):
            if isinstance(u,str) and u.startswith('http'):
                ext=u.split('?')[0].rsplit('.',1)[-1][:5]; fn=d/(f'{k}_{i:03d}.{ext}' if isinstance(v,list) else f'{k}.{ext}')
                try: urllib.request.urlretrieve(u,fn)
                except Exception as e: subprocess.run(['curl','-s','-L','-o',str(fn),u])
    print(name,'downloaded',len(list(d.iterdir())),'files',flush=True)
print('ALL DONE',flush=True)
