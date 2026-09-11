from pathlib import Path
import hashlib,json
from PIL import Image
p=Path(__file__).resolve().parent
prior=json.loads((p.parent/'E03/scenes.json').read_text());actors=json.loads((p/'actor-assets.json').read_text());visual=json.loads((p/'visual-data.json').read_text())
def write(name,d):(p/'manifests'/name).write_text(json.dumps(d,indent=2)+'\n')
assets=[]
for id in ['floor','stone','crate','door','chest','mage','monster','npc']:
 if id=='floor':file='../E03/art/floor-v1.png';a={'root':[0,0]};kind='environment'
 elif id=='mage':file='../E03/art/mage-v1.png';a=prior['assets']['mage'];kind='character'
 elif id in actors:file=actors[id]['path'];a=actors[id];kind='character'
 else:file=visual[id]['path'];a={'root':[0,0]};kind='object' if id!='stone' else 'environment'
 im=Image.open(p/file);w,h=im.size
 height={'mage':2,'monster':2.7,'npc':2,'crate':.9,'chest':.8,'door':2.5,'stone':3,'floor':0}[id];radius={'mage':.35,'monster':.65,'npc':.35}.get(id)
 record={'schema_version':1,'id':id,'asset_type':kind,'path_base':'../','projection_id':'C','qualification':'candidate; original pixels preserved','frames':[{'id':id+'-source','source_path':file,'sha256':hashlib.sha256((p/file).read_bytes()).hexdigest(),'atlas_coordinates':{'x':0,'y':0,'width':w,'height':h},'pivot':a['root'],'duration_ms':None}],'fps':None,'timing_mode':'still' if kind=='character' else 'state_or_geometry_driven','direction':'SE-candidate' if kind=='character' else None,'direction_status':'view requested, not an eight-direction qualification' if kind=='character' else 'not applicable','hitbox':{'space':'logical_world_metres','shape':'conservative_square' if radius else 'layout_owned','radius':radius,'height':height},'emissive_mask_path':None,'effects':{},'alpha_policy':'runtime_silhouette_mask' if 'mask' in a else 'opaque_surface','silhouette_polygon':a.get('mask'),'registration':{'source_axis_height':a.get('axis_height'),'physical_height_m':height},'sockets':{'staff_grip':a['socket_source'],'staff_tip':[917,155]} if 'socket_source' in a else {},'face_uv_coordinates':visual.get(id,{}).get('faces')}
 if id=='crate':record['state_regions']=[{'id':'intact','atlas_coordinates':{'x':0,'y':0,'width':w//2,'height':h}},{'id':'broken','atlas_coordinates':{'x':w//2,'y':0,'width':w-w//2,'height':h},'silhouette_polygons':visual['crate']['debris_polygons']}]
 write(id+'.asset.json',record);assets.append(id+'.asset.json')
write('catalog.json',{'schema_version':1,'shipping_target':'Godot','test_harness':'Pixi','manifest_files':assets,'contract':'Every source path is relative to path_base resolved from its manifest; no renderer-native types or filter instances.'})
