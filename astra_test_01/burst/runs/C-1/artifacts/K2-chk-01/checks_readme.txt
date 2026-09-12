K2-chk-01 deterministic diagnostic checks

Sources are read-only. PYTHONDONTWRITEBYTECODE disables cache writes. No registration is performed: source images are 1024x1536 rather than the frozen 512x512 frame canvas, and no reviewed root/registration annotations are supplied. Native diagnostic RGBA mattes preserve dimensions; 64x64 binary silhouettes are the frozen descriptor masks, including its square-resize convention. These are diagnostic outputs, not registered shipping frames.

G1 values are height ratios; passed is copied from the frozen literal deviation gate, retained in notes with the 0.97..1.03 ratio bounds. G2-root remains null without independent reviewed anchors. O7 value is absolute circular deviation from 135 degrees; measured azimuth is in notes.metrics. O3b runs on native matted RGB: raw hollow_min=0, annulus hollow_min=0.5, radii 8..30, vote_thresh=0.50, no masks, no display reduction. All other detector settings are frozen defaults. Plate uniformity uses frozen inferred largest non-key support and tolerance 8, with no acceptance threshold. Matte spill and halo proxies are reported; a distinct bleed-index formula was not supplied. No dark-fringe threshold, silhouette distance threshold, O7 tolerance or plate min_fraction was supplied; their verdicts remain null.

Exact computation command:

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst python3 - <<'PY'
import json
from pathlib import Path
from PIL import Image
from gates import matte, g1_height, g2_pivot, g3_light, silhouette64, plate_uniformity, g9_alpha, matte_quality
from gates.common import DIRS, rgba, measure, result
from oracles import keylight, motif

out = Path('out')
out.mkdir(exist_ok=True)
base = Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
master_source = rgba(base / 'K1-gen-04/k1_master_L.png')
master, master_matte = matte.extract(master_source, alpha_floor=40)
master_measurement = measure(master)
rows = []
for direction in DIRS:
    source_path = base / 'K1-gen-04/k1_master_L.png' if direction == 'S' else base / ('K2-gen-' + direction) / ('k2_' + direction + '.png')
    source = rgba(source_path)
    frame, matte_details = matte.extract(source, alpha_floor=40)
    frame_path = out / ('k2_' + direction + '_rgba.png')
    frame.save(frame_path)
    descriptor = silhouette64.descriptor(frame)
    silhouette_path = out / ('k2_' + direction + '_64.png')
    Image.fromarray(descriptor['mask']).convert('L').save(silhouette_path)
    measurement = measure(frame)
    bbox = measurement['bbox']
    width, height = frame.size
    rows.append(result('source_and_matte', direction, notes=json.dumps({'source':str(source_path),'matte':matte_details,'canvas_px':[width,height],'registration':'none; diagnostic native-size matte; source is not square and no reviewed registration annotations were supplied','required_frame_canvas_px':[512,512],'silhouette':'frozen silhouette64.descriptor: alpha resized to 64x64 with LANCZOS then binarised at 128'},sort_keys=True), evidence=[str(frame_path),str(silhouette_path)]))
    height_gate = g1_height.evaluate(frame, master, subject=direction, tolerance=.03)
    rows.append(result('g1_height', direction, value=measurement['height']/master_measurement['height'], passed=height_gate['passed'], unit='ratio', notes=json.dumps({'literal_gate':height_gate,'ratio_bounds':[.97,1.03],'threshold_semantics':'literal absolute fractional deviation <= 0.03; value reports requested height ratio'},sort_keys=True), evidence=[str(frame_path),'out/k2_S_rgba.png']))
    rows.append(g2_pivot.root_anchor(anchor=None, subject=direction, pivot=(256,400), tolerance=4))
    rows.append(g3_light.evaluate(frame, subject=direction))
    rows.append(silhouette64.evaluate(frame, master, subject=direction, threshold=None))
    rows.append(plate_uniformity.measure(source, tol=8, min_fraction=None, subject=direction))
    rows.extend(g9_alpha.evaluate(frame, subject=direction, dark_threshold=None))
    rows.extend(matte_quality.measure(frame, source, tol=20, halo_width_px=2, subject=direction))
    rows.append(result('bleed_index_definition', direction, notes='No separate bleed-index formula supplied. Frozen matte_quality.spill reports fraction of alpha>0 subject pixels with G-max(R,B)>20; matte_quality.edge_halo reports exterior-band mean positive green excess. Both retained as advisory measurements, without inventing a threshold.'))
    rows.append(keylight.azimuth(frame, frame.getchannel('A'), mask=None, key_azimuth_deg=135, tolerance=None, min_resultant=0, erosion_px=1, display_scale=None, subject=direction))
    raw = motif.count_family(frame, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=0, max_outside=None, subject=direction)
    raw['id'] = 'O3b_raw'
    rows.append(raw)
    annulus = motif.count_family(frame, family='ring', min_radius_px=8, max_radius_px=30, vote_thresh=.50, allowed_masks=None, display_scale=None, hollow_min=.5, max_outside=None, subject=direction)
    annulus['id'] = 'O3b_annulus'
    rows.append(annulus)
    rows.append(result('alpha_bbox_px', direction, value=bbox, unit='xyxy_exclusive_px', notes='Frozen common.measure, alpha >= 128; native source coordinate system.'))
    rows.append(result('alpha_bbox_canvas_fraction', direction, value=[bbox[0]/width,bbox[1]/height,bbox[2]/width,bbox[3]/height], unit='xyxy_fraction', notes=json.dumps({'bbox_width_fraction':(bbox[2]-bbox[0])/width,'bbox_height_fraction':measurement['height']/height,'bbox_area_fraction':(bbox[2]-bbox[0])*measurement['height']/(width*height),'transparent_fraction_alpha_zero':measurement['transparent_fraction']},sort_keys=True)))
    print(json.dumps({'direction':direction,'canvas':[width,height],'bbox':bbox,'height_ratio':measurement['height']/master_measurement['height'],'g3_value': g3_light.evaluate(frame, subject=direction)['value'],'O3b_raw':raw['value'],'O3b_annulus':annulus['value']}),flush=True)
(out / 'checks.json').write_text(json.dumps(rows,indent=2,allow_nan=False)+'\n')
PY

Exact output hash command:

shasum -a 256 out/*
