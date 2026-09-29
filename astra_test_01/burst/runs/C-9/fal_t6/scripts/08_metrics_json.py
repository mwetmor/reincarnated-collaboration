# T6 step 7 -- fold every measurement into compare/metrics.json and write the
# Markdown table. Nothing is computed here that is not already measured
# elsewhere; this is assembly plus the price column.
import json, os, glob
import numpy as np

B = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/'
T6 = B + 'fal_t6/'
GENS = ['meshy', 'hunyuan3d_31_pro', 'rodin_25', 'tripo_h31_mv', 'trellis2', 'hi3d_v3']
LABEL = {'meshy': 'Meshy (baseline)', 'hunyuan3d_31_pro': 'Hunyuan3D 3.1 Pro',
         'rodin_25': 'Rodin v2.5', 'tripo_h31_mv': 'Tripo H3.1 multiview',
         'trellis2': 'TRELLIS 2', 'hi3d_v3': 'Hi3D v3.0'}

# Prices read off each endpoint's own fal model page on 2026-09-28. Where an
# option changes the tier, the option WE SENT is resolved against the
# endpoint's OpenAPI schema and named. Nothing here is estimated; the one
# figure that cannot be quoted -- Meshy's dollars-per-credit, which Meshy does
# not publish -- is marked derived, with its arithmetic shown.
PRICE = {
 'hunyuan3d_31_pro': dict(usd=0.525, published='"Your request will cost $0.375 per generation. ... Enabling PBR materials adds $0.15. Using multi-view images adds $0.15. Custom face count adds $0.15."',
   basis='$0.375 base + $0.15 multi-view (4 images sent). enable_pbr=False = schema default, no adder. face_count NOT sent (see run_bakeoff.py), so no custom-face-count adder.',
   url='https://fal.ai/models/fal-ai/hunyuan-3d/v3.1/pro/image-to-3d'),
 'rodin_25': dict(usd=0.40, published='"Your request will cost $0.4 per generation. If HighPack is added to the addons, it will cost an additional $0.8 per generation."',
   basis='Flat $0.40. addons.high_pack not set. hd_texture=True is a SEPARATE unpriced boolean, not the priced HighPack addon.',
   url='https://fal.ai/models/fal-ai/hyper3d/rodin/v2.5'),
 'tripo_h31_mv': dict(usd=0.40, published='"Your request will cost $0.20 (without textures), $0.30 (with standard textures), or $0.40 (with HD textures), plus an additional $0.20 for detailed geometry and $0.05 for quad mesh if selected."',
   basis='texture=True + texture_quality="detailed" = the HD tier ($0.40). geometry_quality left at default "standard", so no +$0.20. CAVEAT: the page says "HD", the schema enum says "detailed"; the two-value mapping forces it but the page never literally equates them ($0.30 vs $0.40).',
   url='https://fal.ai/models/tripo3d/h3.1/multiview-to-3d'),
 'trellis2': dict(usd=0.30, published='"Your request will cost 0.25 $ for 512p resolution, 0.3 $ for 1024p resolution and 0.35 $ for 1536p resolution."',
   basis='Defaults sent; schema default resolution=1024 -> $0.30. The priced field is `resolution`, NOT `texture_size` (default 2048, unpriced).',
   url='https://fal.ai/models/fal-ai/trellis-2'),
 'hi3d_v3': dict(usd=2.10, published='"Your request is billed at $0.02 per credit. ... On v3.0, your request will cost $2.10 (2048³quality) or $9.10 (2048³master)."',
   basis='$2.10 published verbatim for this configuration: resolution default "2048quality", enable_texture=True. enable_pbr was NOT sent and its default is TRUE, so PBR (5 cr) is billed -- had we sent enable_pbr=False it would be $2.00. = 90 geometry + 10 texture + 5 PBR credits at $0.02.',
   url='https://fal.ai/models/hitem3d/hi3d/v3.0/image-to-3d'),
 'meshy': dict(usd=None, published='30 credits ("Multi-Image to 3D ... Mesh with 2K textures - 30 credits"), confirmed by the task\'s own consumed_credits=30.',
   basis='DERIVED, not published: Meshy publishes NO dollars-per-credit rate anywhere. Plan price / included credits gives $0.60 on Pro ($20 / 1,000 cr), $0.40 on Premium ($40 / 3,000), $0.375 on Ultra ($100 / 8,000). Not like-for-like with fal: fal bills marginally per request, this is a subscription rate amortised over a monthly allotment that does not roll over, so it holds only at full utilisation.',
   url='https://docs.meshy.ai/en/api/pricing + https://help.meshy.ai/en/articles/12062933'),
}
VIEWS_GIVEN = {'meshy': 'front,right,back,left', 'hunyuan3d_31_pro': 'front,left,right,back',
               'rodin_25': 'front,right,back,left', 'tripo_h31_mv': 'front,left,back,right',
               'trellis2': 'knight: front / manticore: right', 'hi3d_v3': 'knight: front / manticore: right'}

io = json.load(open(T6 + 'compare/iou_rig.json'))
orient = json.load(open(T6 + 'compare/orientation.json'))['models']
sha = dict(reversed(l.split()) for l in open(T6 + 'compare/sha256.txt').read().split('\n') if l.strip())

out = {'test': 'C-9 T6 -- 3D generator bake-off on fal.ai, judged against Meshy (Matt R-C9-66)',
       'camera': {'projection': 'orthographic', 'elevation_deg': 52.95354112560294,
                  'authority': 'Matt R-C9-68 -- the world camera’s real angle, NOT the 19.77° sprite convention',
                  'silhouette_pass_elevation_deg': 0.0,
                  'silhouette_pass_reason': 'the painted plates are flat orthographic; an IoU against them must be measured in their own projection. Doubles as the 0° side-on geometry read.'},
       'normalisation': {'frame': 'Z up, character faces +Y, feet on z=0, midline x=0, height 1.0 m',
                         'azimuth_0': 'camera at +Y, sees the face',
                         'mirror_policy': 'a flip is applied only on evidence >= 0.05 margin; no model cleared that bar, so NO model was mirrored. Both Tripo models reject the flip decisively (margin ~0.38); every 180° model is within ~0.006 either way, which is noise on a bilaterally symmetric subject.'},
       'models': {}}

for s in ('knight', 'manticore'):
    for g in GENS:
        name = f'{s}_{g}'
        pr = json.load(open(f'{T6}work/probe/{name}.json'))
        me = json.load(open(f'{T6}work/metrics/{name}.json'))
        rj = json.load(open(f'{T6}work/out/{name}_render.json'))
        h = io['iou'][name]['p0_100']
        t = io['iou'][name]['p1_99']
        if g == 'meshy':
            r = json.load(open(B + ('meshy_t1/res_knight.json' if s == 'knight' else 'meshy_t2/res_manticore.json')))
            elapsed = round((r['finished_at'] - r['started_at']) / 1000, 1)
            src = 'meshy multi-image-to-3d'
        else:
            j = json.load(open(f'{T6}{name.replace(s + "_", s + "_")}.json'))
            elapsed = j['elapsed_s']; src = j['endpoint']
        p = PRICE[g]
        e = out['models'][name] = dict(
            subject=s, generator=g, label=LABEL[g], endpoint=src,
            views_given=VIEWS_GIVEN[g], sha256=sha.get(name + '.glb'),
            glb_mb=round(pr['glb_bytes'] / 1e6, 2),
            elapsed_s=elapsed,
            price_usd_per_generation=p['usd'],
            price_published=p['published'], price_basis=p['basis'], price_source=p['url'],
            triangles=me['tris_welded'], vertices=me['verts_welded'],
            triangles_as_delivered=me['tris_delivered'], vertices_as_delivered=me['verts_delivered'],
            textures=[f"{i['w']}x{i['h']}" for i in pr['images']],
            texture_count=len(pr['images']),
            colour_map_socket=list(rj['colour_source'].values())[0],
            islands=me['islands'], main_island_area_frac=me['main_island_area_frac'],
            floating_fragments_lt1pct=me['floating_fragments_lt1pct'],
            fragment_area_pct=me['fragment_area_pct'],
            island_area_fracs_top8=me['island_area_fracs_top8'],
            detached_islands=me['detached_islands'],
            detached_area_pct_total=me['detached_area_pct_total'],
            largest_detached_pct=(me['detached_islands'][0]['area_pct'] if me['detached_islands'] else 0.0),
            largest_detached_off_body=(me['detached_islands'][0]['outside_main_body_xy'] if me['detached_islands'] else False),
            nonmanifold_edges=me['nonmanifold_edges'], boundary_edges=me['boundary_edges'],
            approx_watertight=me['approx_watertight'],
            euler_characteristic=me['euler_characteristic'],
            surface_area_m2=me['surface_area_m2'],
            yaw_applied_deg=int(orient[name]['yaw_deg']), flip_x_applied=orient[name]['flip_x'],
            yaw_margin_iou=orient[name]['yaw_margin_iou'],
            mirror_argmax=orient[name]['mirror_argmax'], mirror_margin=orient[name]['mirror_margin'],
            silhouette_iou={v: h[v]['iou'] for v in ('front', 'right', 'back', 'left')},
            silhouette_iou_mean=h['mean_iou'],
            silhouette_iou_mean_ex_back=h['mean_iou_ex_back'],
            silhouette_iou_mean_trim1_99=t['mean_iou'],
            plate_colour_agreement={v: h[v]['colour'] for v in ('front', 'right', 'back', 'left')},
        )
        if s == 'knight':
            e['rig_probe'] = io['knight_rig_probe'][name]

out['caveats'] = [
 'MANTICORE back-view IoU (0.225-0.306 for all six) measures the PLATE, not the model: the painted back plate draws the tail as a vertical spike above the skull, so its height box is roughly twice the creature’s. No generator reproduces that. Read the manticore on front/right/left (mean_ex_back).',
 'Silhouette scale and alignment come from the largest blob; the full mask including detached fragments is what is scored. Without the largest-blob guard a 200-pixel flake set the scale for a million-triangle mesh and the orientation fit chose the wrong yaw on an IoU of 0.22.',
 'Triangle and vertex counts are AFTER an exact-position weld. glTF splits vertices at UV seams, so the delivered index buffer reports every seam as a hole; delivered counts are kept alongside as *_as_delivered.',
 'Rodin v2.5 with material="Shaded" delivers a BLACK base colour and routes its map into Emission at strength 1: its "texture" is a LIGHTING BAKE, not an albedo. The unlit pass reads that socket so Rodin is visible at all, but Rodin’s row is not an apples-to-apples base-colour comparison -- it already contains shading that will fight any light you later put on it.',
 'Meshy’s price is derived from plan price / included credits because Meshy publishes no per-credit dollar rate. It is a subscription amortisation, not a marginal per-request price like fal’s.',
 'The brief’s "floating fragments under 1% of surface area" screen MISSES this run’s worst junk geometry, because it lands just the wrong side of the line: Tripo’s manticore ships a detached ribbon at 1.87% of surface area floating 0.54-0.88 m off the body’s flank, and Hunyuan’s manticore ships two off-body shards at 1.82% and 0.92%. Both read as 0 in the <1% column. Read the per-model `detached_islands` list instead.',
 'Those detached pieces are NOT missing limbs. Plotting each island set in top view shows both creatures’ own tails present and ATTACHED to the main body; the floating pieces are spurious duplicates, so they are deletable in one operation rather than a limb that would have to be regenerated. Checked deliberately, because the first reading of the bounding boxes said "the tail came off" and a bounding box cannot tell a duplicate from an amputation.',
]
json.dump(out, open(T6 + 'compare/metrics.json', 'w'), indent=1)

# ---------------- markdown ---------------------------------------------------
def row(e):
    tex = '+'.join(sorted(set(e['textures']))) + (f" x{e['texture_count']}" if e['texture_count'] > 1 else '')
    pr = f"${e['price_usd_per_generation']:.3f}".rstrip('0').rstrip('.') if e['price_usd_per_generation'] else '$0.60*'
    wt = 'yes' if e['approx_watertight'] else 'no'
    big = e['largest_detached_pct']
    dcol = ('-' if big == 0 else f"{big:.2f}%" + (' **off-body**' if e['largest_detached_off_body'] else ' internal'))
    return (f"| {e['label']} | {e['triangles']:,} | {e['vertices']:,} | {tex} | {e['glb_mb']:.1f} | "
            f"{e['islands']} | {e['floating_fragments_lt1pct']} ({e['fragment_area_pct']:.2f}%) | {dcol} | "
            f"{e['nonmanifold_edges']:,} | {wt} | {e['elapsed_s']:.0f} | {pr} | "
            f"{e['silhouette_iou']['front']:.3f} | {e['silhouette_iou']['right']:.3f} | "
            f"{e['silhouette_iou']['back']:.3f} | {e['silhouette_iou']['left']:.3f} | "
            f"**{e['silhouette_iou_mean']:.3f}** | {e['silhouette_iou_mean_ex_back']:.3f} |")

md = ['# C-9 T6 -- 3D generator bake-off, measurements', '',
      'Matt R-C9-66. Six pipelines per subject: the Meshy baseline plus five fal endpoints, all',
      'built from the SAME approved four-view painted plates. Renders at orthographic',
      '52.95354112560294 deg elevation per Matt R-C9-68; the IoU pass is at 0 deg because the',
      'painted plates are flat and an IoU against them has to be measured in their own projection.',
      '', 'Counts are AFTER an exact-position weld (glTF splits vertices at UV seams; the delivered',
      'numbers are in `metrics.json` as `*_as_delivered`). `frag` = islands under 1% of surface',
      'area, with their combined area share. IoU = silhouette agreement with the painted plate,',
      'height-normalised.', '']
for s in ('knight', 'manticore'):
    md += [f'## {s.upper()}', '',
           '| generator | tris | verts | textures | GLB MB | islands | frag <1% | largest detached piece | non-manifold edges | watertight | gen s | $/gen | IoU front | IoU right | IoU back | IoU left | IoU mean | IoU mean ex-back |',
           '|---|---:|---:|---|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for g in GENS:
        md.append(row(out['models'][f'{s}_{g}']))
    md.append('')
md += ['\\* Meshy: 30 credits. Meshy publishes no dollars-per-credit rate; $0.60 is DERIVED as',
       'Pro plan $20 / 1,000 credits per month, and holds only at full monthly utilisation',
       '($0.40 on Premium, $0.375 on Ultra). fal prices are marginal per-request prices; this is not.', '',
       '## Knight rig probe (no Meshy rigging call, no credits spent)', '',
       '| generator | tris | decimate to reach 300k | one humanoid island | floating frags | arm/torso gap rows | arms clear |',
       '|---|---:|---:|---|---:|---:|---|']
for g in GENS:
    r = out['models'][f'knight_{g}']['rig_probe']
    md.append(f"| {LABEL[g]} | {r['tris']:,} | x{r['decimate_ratio_to_300k']:.3f} | "
              f"{'yes' if r['single_humanoid_island'] else 'no'} ({r['main_island_area_frac']:.4f}) | "
              f"{r['floating_fragments']} | {r['arm_gap_rows_in_torso_band']} | "
              f"{'yes' if r['arms_clear_of_torso'] else 'NO'} |")
md += ['', '## Orientation applied (measured, not assumed)', '',
       '| model | yaw applied | yaw margin (IoU) | mirror argmax | mirror margin | mirrored? |',
       '|---|---:|---:|---|---:|---|']
for s in ('knight', 'manticore'):
    for g in GENS:
        e = out['models'][f'{s}_{g}']
        md.append(f"| {s}/{LABEL[g]} | {e['yaw_applied_deg']}° | {e['yaw_margin_iou']:.3f} | "
                  f"{e['mirror_argmax']} | {e['mirror_margin']:.4f} | "
                  f"{'yes' if e['flip_x_applied'] else 'no'} |")
md += ['', 'No model was mirrored. A flip is applied only on a margin >= 0.05 and nothing cleared it:',
       'both Tripo models reject a flip decisively (~0.38), every 180 deg model is within ~0.006',
       'either way, which is noise on a bilaterally symmetric subject.', '']
md += ['## Caveats', ''] + [f'- {c}' for c in out['caveats']] + ['']
open(T6 + 'compare/metrics.md', 'w').write('\n'.join(md))
print('wrote compare/metrics.json and compare/metrics.md')
