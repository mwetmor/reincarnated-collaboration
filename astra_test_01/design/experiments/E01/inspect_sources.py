"""Record human-readable visual observations separately from acquisition metadata."""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
notes={
'D2-01':('combat','HUD-equipped Frozen Orb dungeon: bright detached shards cross dark ground; central bodies overlap; foreground tomb/rock hides floor. Body isolation indeterminate.'),
'D2-02':('excluded-menu','Stash and inventory cover the world. Excluded from projection and character-scale measurement.'),
'D2-03':('interaction-ui','Hire-mercenary dialog over camp grass and wagon. Establishes visible NPC interaction UI, not navigation or normal camera framing.'),
'D2-04':('combat','Cold-blue melee cluster beside path and rock; several bodies overlap. Grass and dirt remain separable away from combat; body bounds indeterminate.'),
'D2-05':('combat-architecture','Diagonal masonry floor, tall wall, foreground sarcophagus and blue spell clusters. Ground edges traceable; no dynamic occlusion or collision proven.'),
'D2-06':('quiet-still','Isolated caster in cave with torches, stalagmites, shadow and open floor. Quiet instant only, not a traversal segment.'),
'GD-01':('combat','1920x1200 HUD scene. Large creatures and rocks occupy near ground; central blue/white effects obscure actor feet and floor.'),
'GD-02':('combat','HUD boss scene: bright central fire overlaps player and giant airborne body; red scenery reduces separation of red effects. Cast pose prevents standing-height comparison.'),
'GD-03':('combat-low-clutter','HUD scene: isolated armored player beside huge beast on pale sand; gold ground effect, contact shadows and exposed rock tops visible. Zoom setting unknown.'),
'GD-04':('interaction-before','Devil’s Crossing: broken bridge behind tall gate arch; repair dialog visible. Guide pairs this with GD-05. Timing/path-cache updates not shown.'),
'GD-05':('interaction-after-quiet','Same viewpoint and actor vicinity as GD-04; bridge visibly spans gap; dialog removed. Supports before/after visible geometry only, not transition correctness.'),
'GD-06':('interactable-no-hud','Gold chest among standing stones and ghostly figures. No ordinary HUD; prop/material/occlusion reference only.'),
'LE-01':('excluded-menu','Class-wheel graphic, not gameplay. Retained as an intake rejection.'),
'LE-02':('excluded-menu','Passive-tree menu covering world. Excluded from camera measurements.'),
'LE-03':('excluded-menu','Ballista skill menu covering world. Excluded from camera measurements.'),
'LE-04':('excluded-menu','Forge/inventory panels and enlarged character view; BETA 0.9.2 label visible. This is not ordinary gameplay framing.'),
'LE-05':('interaction-quiet-no-hud','Bridge clearing with four actors, NPC speech icon and foliage/stone edges. No ordinary HUD; composition reference, not default camera evidence.'),
'LE-06':('interaction-dialog','Elder Gaspar dialog over elevated stone platform; cyan/purple portal and stairs. No standard combat HUD. State persistence not demonstrated.'),
'LE-07':('interactable-no-hud','Opened chest with gold light, monumental circular platform and runic central object. Open state visible; loot event/count and traversability unverified.'),
'LE-08':('quiet-no-hud','Actor beside monumental runic plinth on raised circular stone; visible steps/sidewalls, large foreground architecture. No HUD.'),
'LE-09':('combat-no-hud','Gold/red arc at left, green-lit floor at right, diagonal railing crossing foreground, dense combat bodies. Source-rendered combat promotional still; player isolation indeterminate.'),
'LE-10':('combat-no-hud','Fire patches and winged enemies over grass/soil, cyan attack near central actor. Dense wings/FX overlap; no HUD; no motion claim.'),
'LE-11':('combat-no-hud','Bright purple beam across stony shore; actor feet near edge; reflected water highlights compete with energy. No proof of splash/material response.'),
'POE-01':('combat','PoE1 HUD and circular arena; golden fire, purple energy and central winged actor. Body/gear/effects overlap; ellipse is architecture, not calibrated camera fiducial.'),
'POE-02':('combat-architecture','PoE1 HUD; barrels, tall industrial wall and machine amid melee. Blue line-like arcs retain gaps through which ground is visible; red effects overlap central body.'),
'POE-03':('combat','PoE1 HUD; sand arena, enemies, red trails, fire and blood patches. Exact damaging areas and effect lifecycle cannot be read from one instant.'),
'POE-04':('combat-low-clutter','PoE1 HUD; central actor to right of tall wooden fence, large monster at left, ground ring and fire/blue effects. Equipment obscures true head boundary; body height uncertain.'),
'REPLICA-01':('project-replica','Godot cathedral at source 1.000s (60fps source): circular smoke/trail around player, diagonal tile grid, tall structure upper left, colored lighting. Never source-game evidence.')}
rows=json.loads((P/'sources.json').read_text())
for r in rows:
 r['category'],r['observation']=notes[r['id']];r['inspection']='VISUALLY_INSPECTED_FULL_FRAME';r['inspection_method']='view_image of local original; fit-to-tool display for 1920px files, native-file coordinates used for annotations';r['confidence']='High title/publisher provenance; exact screenshot patch/camera settings unknown';r['motion_verdict']='UNVERIFIED — still only'
 if r['id'].startswith('LE-'):r['camera_eligibility']='EXCLUDED from ordinary gameplay framing: menu/dialog or HUD hidden'
 else:r['camera_eligibility']='Still-image quantities only; default zoom and motion unverified'
# Exact source recovery for previously retained stills.
old=P.parents[3]/'agentic_orchestration/galadriel/reference-images/3d-stylized-arpg-2026-06-14'

for r in rows:
 matches=[]
 for sub in ['last-epoch','fire-spell-exemplars']:
  for f in (old/sub).glob('*.jpg'):
   if hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']:matches.append(str(f))
 r['byte_identical_existing_files']=matches
(P/'sources.json').write_text(json.dumps(rows,indent=2)+'\n')
measurements=[
 {'id':'D2-06','body_bbox':[296,175,334,234],'endpoint_uncertainty_px':4,'foot':[324,232],'foot_uncertainty_px':4,'active_rect':[0,0,640,432],'denominator_note':'D2 continuous bottom bar starts near y432; side orbs intrude into this rectangle. Also report full raster denominator 480.','status':'MANUAL_ESTIMATE','note':'Body excludes diagonal staff and blue motes; standing/idle instant.'},
 {'id':'GD-05','body_bbox':[501,255,525,313],'endpoint_uncertainty_px':3,'foot':[512,311],'foot_uncertainty_px':3,'active_rect':[0,0,1024,576],'denominator_note':'Gameplay extends around central bottom HUD; full raster retained, HUD intrusion separate.','status':'MANUAL_ESTIMATE','note':'Standing actor, native guide file may be publisher downsample; no default zoom inference.'},
 {'id':'GD-03','body_bbox':[921,458,1005,624],'endpoint_uncertainty_px':8,'foot':[953,619],'foot_uncertainty_px':8,'active_rect':[0,0,1920,1080],'denominator_note':'Full raster, central bottom HUD overlays world.','status':'MANUAL_ESTIMATE','note':'Armor included where anatomy is hidden; sword and golden ring excluded. Different scale from GD-05; not a game-wide constant.'},
 {'id':'POE-04','body_bbox':None,'endpoint_uncertainty_px':None,'foot':[964,493],'foot_uncertainty_px':12,'active_rect':[0,0,1920,1080],'denominator_note':'Full raster with large side orbs/action UI overlay.','status':'BODY_INDETERMINATE','note':'Gold equipment/effects obscure head and shoulder support. Coarse visible central actor+gear extent approx y340–505 is NOT tight-body measurement.'},
 {'id':'LE-05','body_bbox':[927,385,997,515],'endpoint_uncertainty_px':8,'foot':[961,511],'foot_uncertainty_px':7,'active_rect':[0,0,1920,1080],'denominator_note':'Full publisher image; ordinary HUD absent.','status':'PROMOTIONAL_COMPOSITION_ONLY','note':'Lower-center actor, player assignment provisional; do not infer ordinary gameplay scale.'},
 {'id':'LE-08','body_bbox':[970,401,1037,546],'endpoint_uncertainty_px':8,'foot':[1007,540],'foot_uncertainty_px':7,'active_rect':[0,0,1920,1080],'denominator_note':'Full publisher image; ordinary HUD absent.','status':'PROMOTIONAL_COMPOSITION_ONLY','note':'Standing actor beside runic plinth; helmet included, sword excluded.'}
]
for m in measurements:
 r=next(r for r in rows if r['id']==m['id']);w,h=r['dimensions'];a=m['active_rect'];m['foot_fraction_active']=[round((m['foot'][0]-a[0])/a[2],3),round((m['foot'][1]-a[1])/a[3],3)]
 if m['body_bbox']:
  bh=m['body_bbox'][3]-m['body_bbox'][1];err=2*m['endpoint_uncertainty_px'];m['body_height_px']=bh;m['body_height_fraction_full']=round(bh/h,3);m['body_height_fraction_active']=round(bh/a[3],3);m['body_fraction_active_interval']=[round((bh-err)/a[3],3),round((bh+err)/a[3],3)]
 m['near_far_scale']='UNIDENTIFIED — no calibrated repeated object positions';m['absolute_camera']='UNIDENTIFIED — no calibrated FOV, metres or elevation estimate';m['ground_edge_measurement']='See source overlays in comparison.html; line direction is an image quantity, not a camera solution'
(P/'measurements.json').write_text(json.dumps(measurements,indent=2)+'\n')
print('Inspected',len(rows),'sources; recovered byte matches',sum(bool(r['byte_identical_existing_files']) for r in rows))
