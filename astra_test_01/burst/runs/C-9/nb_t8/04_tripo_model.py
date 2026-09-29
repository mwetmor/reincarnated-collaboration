# T8: the T6 winner (Tripo H3.1 multiview, fal) on the NB-1 views, same arguments as the bake-off; order [front, left, back, right].
import fal_client, json, subprocess, sys, time
v=sys.argv[1] if len(sys.argv)>1 else 'b'
u={n:fal_client.upload_file(f'nb_{v}_{n}.jpg') for n in ('front','left','back','right')}
t0=time.time()
r=fal_client.subscribe('tripo3d/h3.1/multiview-to-3d',arguments={'image_urls':[u['front'],u['left'],u['back'],u['right']],'texture':True,'pbr':False,'texture_quality':'detailed'})
json.dump({'endpoint':'tripo3d/h3.1/multiview-to-3d','elapsed_s':round(time.time()-t0,1),'result':r},open(f'tripo_nb_{v}.json','w'),indent=1)
url=(r.get('model_mesh') or {}).get('url') or next((x.get('url') for x in r.values() if isinstance(x,dict) and str(x.get('url','')).endswith('.glb')),None)
subprocess.run(['curl','-s','-L','-o',f'nb_{v}_tripo.glb',url],check=True); print('done',round(time.time()-t0),'s',url.split('/')[-1])
