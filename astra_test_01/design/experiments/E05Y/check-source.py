from pathlib import Path
import json,numpy as np
p=Path(__file__).resolve().parent;a=json.loads((p/'character.asset.json').read_text());r=json.loads((p/'evidence/source-motion.json').read_text());checks={'rest_geometry_exact':r['rest_geometry_indices_weights_exact'],'source_unchanged':r['source_unchanged'],'all219_source_samples':len(r['source_checks'])==219 and all(x['pass']for x in r['source_checks'])}
for k,c in r['clips'].items():
 checks[k+'_contacts']=c['contact_drift_m']<=(.02 if k=='walk'else .001)
 checks[k+'_penetration']=c['min_sole_z']>=-.001;checks[k+'_book']=c['book_size_variation']<=.01;checks[k+'_bone_length']=c['bone_error_m']<=.001
 checks[k+'_loop_or_return']=(c['end_idle_start_error']if k=='cast'else c['endpoint_matrix_error'])<=1e-5
checks['gear_core_clearance']=all(x['pass']for x in r['fit_checks'])
v=np.fromfile(p/a['vertex_buffer']['path'],dtype='<f4').reshape(-1,16);ix=np.fromfile(p/a['index_buffer']['path'],dtype='<u4');ids=np.unique(np.concatenate([ix[g['index_start']:g['index_start']+g['index_count']]for g in a['parts']if g.get('default_visible',True)]));v=v[ids];pal=np.fromfile(p/a['palette_buffer']['path'],dtype='<f4').reshape(-1,len(a['bones']),4,4).transpose(0,1,3,2);pos=np.c_[v[:,:3],np.ones(len(v))];joints=v[:,8:12].astype(int);weights=v[:,12:16];profile=json.loads((p.parent/'E03/inputs/projection-candidates.json').read_text())[2];e,y=np.deg2rad([profile['elevation_deg'],profile['yaw_deg']]);f=810/np.tan(np.deg2rad(profile['vertical_fov_deg']/2));records=[]
for frame,mats in enumerate(pal):
 world=sum(np.einsum('vij,vj->vi',mats[joints[:,k]],pos)*weights[:,k,None]for k in range(4))[:,:3]
 for i in range(8):
  t=-i*np.pi/4;c,s=np.cos(t),np.sin(t);q=world.copy();q[:,0]=c*world[:,0]-s*world[:,1];q[:,1]=s*world[:,0]+c*world[:,1];along=np.sin(y)*q[:,0]-np.cos(y)*q[:,1];depth=profile['distance_m']-np.cos(e)*along-np.sin(e)*q[:,2];dx=f/depth*(np.cos(y)*q[:,0]+np.sin(y)*q[:,1]);dy=f/depth*(np.sin(e)*along-np.cos(e)*q[:,2])
  for height,rootY,low,high in [(50,100,0,150),(150,360,150,500)]:
   x=150+dx*height/153.89987636063665;yy=rootY+dy*height/153.89987636063665;margin=float(min(x.min(),300-x.max(),yy.min()-low,high-yy.max()));records.append({'pose':a['poses'][frame]['id'],'heading':i*45,'body_axis_px':height,'margin_px':margin,'bounds_px':[float(x.min()),float(yy.min()),float(x.max()),float(yy.max())],'depth_min_m':float(depth.min()),'depth_max_m':float(depth.max()),'pass':bool(margin>=5 and depth.min()>=10 and depth.max()<=40)})
checks['all3456_full_frame_bounds']=len(records)==3456 and all(x['pass']for x in records)
report={'checks':checks,'fit_failures':r['fit_failures'],'fit_min_m':min(x['minimum_signed_core_clearance_m']for x in r['fit_checks']),'fit_by_part':{k:{'failures':sum(not x['pass']for x in r['fit_checks']if x['object']==k),'min_m':min(x['minimum_signed_core_clearance_m']for x in r['fit_checks']if x['object']==k)}for k in sorted({x['object']for x in r['fit_checks']})},'minimum_margin_px':min(x['margin_px']for x in records),'records':records,'scope':'Core paired vertices only; does not prove all gear surface intersections or turns.'};(p/'evidence/source-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='records'})
