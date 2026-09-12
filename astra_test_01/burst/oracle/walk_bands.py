"""CLI: provisional walk reference bands and Pillow diagnostic plots.

k_vert=2 amplifies vertical motion; k_lat=.5 suppresses lateral motion.
The SPEC supplies no finite sole-scroll ceiling or weapon-arm ceiling; these
remain null. Reference floor may exceed its ceiling and is never clamped.
Reference bands are uncommitted. --ours never overwrites reference rows.
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from .walk_curves import curves,frame_paths,annotation_curves,ANNOTATION_POINTS
from .walk_landmarks import figure_mask_row

ROOT=Path(__file__).resolve().parents[1]
OURS_ROOT=ROOT/'runs/C-1/oracle'
LABELS=('plate2_lateral','plate13_lateral','plate13_front','plate13_rear')


def bands(summary,k_vert=2.,k_lat=.5):
    def band(v,k,ceiling=None):
        return dict(value=v,floor=v,target=v*k if v is not None else None,ceiling=ceiling)
    s=summary;w5=s.get('W5');scroll=s.get('sole_scroll')
    scroll_value=scroll.get('mean_scroll_px_per_frame') if scroll else None
    return {'W1':band(s['W1'],k_vert,.07),'W2':s['W2'],
            'W3a':dict(value=s['W3a'],ceiling=.35),
            'W3b':dict(value=s['W3b'],threshold=None),
            'W3c':dict(value=s['W3c'],floor=2,ceiling=3),
            'W4':dict(value=s['W4'],target=2),
            'W5':{side:band(v,k_lat,.20) for side,v in w5.items()} if w5 else None,
            'W5_role_limits':{'free_arm':{'floor':.08,'ceiling':.20},'weapon_arm':{'floor':.03,'ceiling':None},'assignment':None},
            'W6':dict(value=s['W6'],floor=.75,minimum_opposed_frames=9,total_frames=12),
            'sole_scroll':band(abs(scroll_value) if scroll_value is not None else None,1.) if scroll else None,
            'parameters':dict(k_vert=k_vert,k_lat=k_lat,sole_scroll_multiplier=1.),
            'note':'W5 targets apply k_lat to extents; anatomical free/weapon role is unassigned. Sole floor is absolute mean speed; signed values retained in curves.'}


def _write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n')


def _plots(directory,label,paths,data,band):
    directory.mkdir(parents=True,exist_ok=True)
    arrays=[]
    for path in paths:
        with Image.open(path) as source:
            arrays.append(np.array(source.convert('RGBA') if 'A' in source.getbands() else source.convert('RGB')))
    annotation = data.get('source') == 'annotation'
    if annotation:
        check_path = _annotation_check(directory, label, arrays, data)
    else:
        check_path = _mask_check(directory, label, arrays, data)
    if data.get('reason') == 'unstable_segmentation':
        return [str(check_path)]
    return [str(check_path), str(_curve_plot(directory, label, data, band))]


def _annotation_check(directory, label, arrays, data):
    h, w = arrays[0].shape[:2]
    check = Image.new('RGB', (2*w, h+65), (22,26,35))
    colors = dict(head_top='red', chin='orange', hip='yellow', near_sole='cyan',
                  far_sole='magenta', near_wrist='lime', far_wrist='violet')
    for column, index in enumerate((0, 6)):
        panel = Image.fromarray(arrays[index][...,:3]); draw = ImageDraw.Draw(panel)
        frame = data['annotation']['frames'][index]
        draw.line((0, frame['ground_y'], w-1, frame['ground_y']), fill='yellow', width=2)
        for name in ANNOTATION_POINTS:
            x, y = frame[name]; color = colors[name]
            draw.ellipse((x-5,y-5,x+5,y+5), outline=color, width=2)
            draw.text((max(0,min(w-110,x+7)),y-15), name, fill=color, stroke_width=1, stroke_fill='black')
        check.paste(panel, (column*w,65)); draw = ImageDraw.Draw(check)
        draw.text((column*w+5,5), f'{label} frame {index+1}: annotated points', fill='white')
        draw.text((column*w+5,23), f"ground={frame['ground_y']} H={data['landmarks'][index]['H']:.1f}", fill='white')
        draw.text((column*w+5,41), 'Muybridge, public domain; raw points over source cell', fill='white')
    path = directory/f'{label}_annotation_check.png'; check.save(path)
    return path


def _mask_check(directory, label, arrays, data):
    masks=figure_mask_row(arrays, method=data['mask_params'].get('mask_method', 'A'))
    h,w=arrays[0].shape[:2];check=Image.new('RGB',(2*w,h+65),(22,26,35))
    for column,index in enumerate((0,6)):
        a=arrays[index][...,:3].copy();mask=masks[index]
        a[mask]=(a[mask]*.5+np.array([40,220,100])*.5).astype(np.uint8)
        panel=Image.fromarray(a);draw=ImageDraw.Draw(panel);lm=data['landmarks'][index] if data['landmarks'] else {}
        if lm.get('valid'):
            dx,dy=lm['grid_shift_xy']
            if lm.get('head_box_xyxy'):
                x0,y0,x1,y1=lm['head_box_xyxy'];draw.rectangle((x0-dx,y0-dy,x1-dx,y1-dy),outline='red',width=2)
            draw.line((0,lm['head_top_mask_y']-dy,w-1,lm['head_top_mask_y']-dy),fill='yellow')
            for side,color in (('L','cyan'),('R','magenta')):
                x,y=lm.get('foot_'+side+'_x'),lm.get('foot_'+side+'_y')
                if x is not None:
                    x-=dx;y-=dy;draw.ellipse((x-4,y-4,x+4,y+4),outline=color,width=2)
                    draw.text((max(0,x-30),y-20),side+' planted='+str(lm['planted_'+side]),fill=color,stroke_width=1,stroke_fill='black')
        check.paste(panel,(column*w,65));draw=ImageDraw.Draw(check)
        draw.text((column*w+5,5),f"{label} frame {index+1} mask green; head red",fill='white')
        draw.text((column*w+5,22),f"A={lm.get('mask_area')} H={lm.get('H')} planted={lm.get('planted')}",fill='white')
        draw.text((column*w+5,39),f"grid_leak={data['mask_health'][index].get('grid_leak')} NCC={lm.get('head_ncc')}",fill='white')
    check_path=directory/f'{label}_mask_check.png';check.save(check_path)
    return check_path


def _curve_plot(directory, label, data, band):
    plot=Image.new('RGB',(1150,1100),(22,26,35));d=ImageDraw.Draw(plot)
    d.text((20,12),label+' / source-pixel curves / provisional bands',fill='white')
    seq=data['landmarks'];H=data['summary'].get('H_mean', data['summary'].get('H_median'))
    panels=[('head image y; red NCC, yellow mask lineage',{'head_top_y':'#ff7777','head_top_mask_y':'#eeee66'},band['W1']),
            ('head x; blue',{'head_cx':'#66bbff'},None),
            ('tracked sole x; L cyan, R green',{'foot_L_x':'cyan','foot_R_x':'#66ee99'},None),
            ('extent at 0.45H; L cyan, R green',{'wrist_ext_L':'cyan','wrist_ext_R':'#66ee99'},None)]
    annotation = data.get('source') == 'annotation'
    if annotation:
        panels = [('head height above per-frame ground; px', {'H':'#ff7777'}, band['W1']),
                  ('head x relative to per-frame hip; px', {'head_cx':'#66bbff'}, None),
                  ('sole x relative to hip; near cyan, far green', {'foot_L_x':'cyan','foot_R_x':'#66ee99'}, None),
                  ('wrist x relative to hip; near cyan, far green', {'wrist_ext_L':'cyan','wrist_ext_R':'#66ee99'}, None)]
    for j,(title,keys,b) in enumerate(panels):
        top=70+j*235;bottom=top+165;left=95;right=1110
        rows={key:[v.get(key) for v in seq] for key in keys}
        values=[v for row in rows.values() for v in row if v is not None]
        if not values: continue
        lo=min(values);hi=max(values);mid=(lo+hi)/2
        if b and b['ceiling'] is not None: lo=min(lo,mid-b['ceiling']*H/2);hi=max(hi,mid+b['ceiling']*H/2)
        pad=max(1.,.1*(hi-lo));lo-=pad;hi+=pad
        yy=lambda v:bottom-(v-lo)/(hi-lo)*(bottom-top)
        xx=lambda i:left+i/11*(right-left)
        if b:
            for key,color in [('ceiling','#303840'),('target','#384858'),('floor','#405868')]:
                if b[key] is not None:
                    size=b[key]*H/2;d.rectangle((left,max(top,yy(mid+size)),right,min(bottom,yy(mid-size))),fill=color)
        d.text((left,top-22),title,fill='white')
        for t in np.linspace(lo,hi,4):
            y=yy(t);d.line((left,y,right,y),fill='#454a55');d.text((10,y),f'{t:.2f}',fill='white')
        for key,color in keys.items():
            last=None
            for i,v in enumerate(rows[key]):
                if v is None: last=None;continue
                p=(xx(i),yy(v))
                if last: d.line((*last,*p),fill=color,width=2)
                d.ellipse((p[0]-2,p[1]-2,p[0]+2,p[1]+2),fill=color);last=p
        for i,phase in enumerate(data['phase_table']):
            d.text((xx(i)-10,bottom+6),str(i+1),fill='white')
            d.text((xx(i)-18,bottom+20),(phase['phase'] or '?')[:4],fill='#bbbbbb')
    d.text((20,1040),'Shading: W1 floor/target/ceiling about curve center. Missing phases shown ?.',fill='white')
    d.text((20,1060),'Annotation: ground-relative heights and hip-relative x; near/far anatomical labels.' if annotation else 'Mask tracks are screen-space proxies; front/rear arm/sole summaries are null.',fill='white')
    path=directory/f'{label}_curves.png';plot.save(path)
    return path


def agreement(annotation, mask):
    """20% absolute-relative comparison; absent estimates never agree.

    W2 is categorical: compare extrema frame/phase lists exactly, with no
    invented numerical distance. Mask L/R wrists have no anatomical near/far
    identification, so W5 arm comparisons remain unevaluable even when stable.
    """
    output = {}
    for key in ('W1', 'W2', 'W3a', 'W3b', 'W3c', 'W4', 'W6'):
        a, m = annotation.get(key), mask.get(key) if mask else None
        if key == 'W2':
            same = all(a.get(k) == m.get(k) for k in ('min', 'max')) if a and m else None
            output[key] = dict(annotation=a, mask=m, abs_delta=None, within_20_percent=None,
                               categorical_agrees=same, reason='categorical extrema use exact frame/phase agreement' if m else 'unstable_segmentation')
        else:
            delta = abs(a-m) if a is not None and m is not None else None
            output[key] = dict(annotation=a, mask=m, abs_delta=delta,
                               within_20_percent=bool(delta <= .2*abs(a)) if delta is not None else None,
                               reason=None if delta is not None else 'mask_estimate_unavailable')
    for name in ('near', 'far'):
        output['W5.'+name] = dict(annotation=(annotation.get('W5') or {}).get(name), mask=None,
                                abs_delta=None, within_20_percent=None,
                                reason='mask near/far identity unestablished' if mask else 'unstable_segmentation')
        # Expose both possible screen-track comparisons without assigning anatomy.
        a = (annotation.get('W5') or {}).get(name)
        candidates = {}
        for side, m in ((mask.get('W5') or {}).items() if mask else []):
            delta = abs(a-m) if a is not None and m is not None else None
            candidates[side] = dict(mask=m, abs_delta=delta,
                                    within_20_percent=bool(delta <= .2*abs(a)) if delta is not None else None)
        output['W5.'+name]['screen_track_candidates'] = candidates
    a = (annotation.get('sole_scroll') or {}).get('mean_scroll_px_per_frame')
    m = (mask.get('sole_scroll') or {}).get('mean_scroll_px_per_frame') if mask else None
    delta = abs(a-m) if a is not None and m is not None else None
    output['sole_scroll'] = dict(annotation=a, mask=m, abs_delta=delta,
                                 within_20_percent=bool(delta <= .2*abs(a)) if delta is not None else None,
                                 reason=None if delta is not None else 'mask_estimate_unavailable')
    return output


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ref',type=Path);p.add_argument('--ours',type=Path)
    p.add_argument('--landmarks',type=Path)
    p.add_argument('--mask_method', choices=('A', 'B'), default='A')
    p.add_argument('--pattern',default='*.png');p.add_argument('--fps',type=float,required=True)
    p.add_argument('--label',required=True);p.add_argument('--out',type=Path,default=Path('oracle/bands_walk.json'))
    p.add_argument('--plot_dir',type=Path);p.add_argument('--k_vert',type=float,default=2.);p.add_argument('--k_lat',type=float,default=.5)
    args=p.parse_args(argv)
    if not (args.ref or args.ours or args.landmarks): p.error('provide --landmarks, --ref or --ours')
    if args.ours and (args.ref or args.landmarks): p.error('--ours cannot be combined with reference inputs')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.label): p.error('invalid label')
    if args.ref and args.label not in LABELS:p.error('reference label must name a contracted plate row')
    if any(not np.isfinite(k) or k<=0 for k in (args.k_vert,args.k_lat)):p.error('multipliers must be positive finite')
    if args.plot_dir and args.plot_dir.resolve().is_relative_to(ROOT) and not args.plot_dir.resolve().is_relative_to(OURS_ROOT):p.error('in-repository plots only under runs/C-1/oracle')
    directory=(args.ref or args.ours).resolve() if (args.ref or args.ours) else None
    lateral=not args.label.endswith(('_front','_rear'))
    mask_data = None
    try:
        if directory:
            mask_data=curves(directory,args.pattern,args.fps,lateral,ours=bool(args.ours),mask_method=args.mask_method)
        data=annotation_curves(args.landmarks,args.fps,lateral) if args.landmarks else mask_data
    except (ValueError, OSError) as exc:p.error(str(exc))
    provenance=dict(plate=data.get('annotation',{}).get('plate', args.label.split('_')[0]),
                    row=data.get('annotation',{}).get('row',args.label.split('_')[-1]),
                    source=str(args.landmarks.resolve() if args.landmarks else directory),
                    source_note='own registered sprites' if args.ours else 'Muybridge public domain',
                    frame_names=data['frame_names'],frames=data['frames'],fps=args.fps,pattern=args.pattern,
                    mask_params=data['mask_params'],k_vert=args.k_vert,k_lat=args.k_lat)
    if args.landmarks:
        provenance.update(annotation_path=str(args.landmarks.resolve()),
                          reference_path=str(directory) if directory else None,
                          subject_height_px=data['annotation']['subject_height_px'],
                          stride_notes=data['annotation'].get('stride_notes'),
                          coordinates=data['coordinate_system'])
    b=bands(data['summary'],args.k_vert,args.k_lat);data['provenance']=provenance
    if args.landmarks:
        for key in ('W1','W2','W3a','W3b','W3c','W4','W5','W6','sole_scroll'):
            entry = b[key]
            if key in ('W2', 'W5') or entry is None:
                entry = dict(value=data['summary'][key], bands=entry)
                b[key] = entry
            entry.update(value=data['summary'][key],source='annotation',mean_confidence=data['mean_confidence'])
    comparison = agreement(data['summary'], mask_data['mask_estimate']) if args.landmarks and args.ref else None
    mask_agrees = bool(comparison and all(v.get('within_20_percent') is True or v.get('categorical_agrees') is True for v in comparison.values()))
    if comparison:
        for key in ('W1','W2','W3a','W3b','W3c','W4','W6','sole_scroll'):
            b[key]['mask_agrees'] = comparison[key].get('within_20_percent') is True or comparison[key].get('categorical_agrees') is True
        b['W5']['mask_agrees'] = all(comparison['W5.'+name]['within_20_percent'] is True for name in ('near', 'far'))
    if args.plot_dir:
        plot_source = directory
        pattern = args.pattern
        if args.landmarks and plot_source is None:
            # The ANNOTATE schema names its public-domain plate/row, not image paths.
            ann = data['annotation']; row = f"plate{ann['plate']}_{ann['row']}"
            if row not in LABELS: p.error('annotation plot source requires a contracted plate/row or --ref')
            plot_source = ROOT/'fixtures/muybridge'/row; pattern = 'frame_*.png'
        paths = frame_paths(plot_source,pattern)
        if len(paths) != 12: p.error('plots require 12 source cells')
        evidence=_plots(args.plot_dir.resolve(),args.label,paths,data,b)
        for r in data['results']:r['evidence']=evidence
    if not args.ours:
        out=args.out.resolve();existing=json.loads(out.read_text()) if out.exists() else {}
        row=dict(bands=b,summary=data['summary'],value=data['summary'],phase_table=data['phase_table'],
                 provenance=provenance,curves=data,committed=False)
        if mask_data:
            row.update(mask_estimate=mask_data['mask_estimate'],
                       mask_stability=mask_data['mask_stability'], mask_H_cv=mask_data['mask_H_cv'],
                       mask_diagnostics={k: mask_data[k] for k in ('stable','threshold','mask_area_px','mask_H_px','mask_health','mask_params')},
                       reason=mask_data.get('reason'))
        if comparison:
            row.update(agreement=comparison,mask_agrees=mask_agrees)
        existing[args.label]=row
        _write(out,existing)
    else:
        out=OURS_ROOT/f'{args.label}_ours.json';_write(out,data)
    print(json.dumps(dict(label=args.label,out=str(out),summary=data['summary'],phase_table=data['phase_table'],
                          mask_stability=mask_data['mask_stability'] if mask_data else None,
                          mask_H_cv=mask_data['mask_H_cv'] if mask_data else None,
                          mask_estimate_reported=mask_data['mask_estimate'] is not None if mask_data else False,
                          agreement=comparison,mask_agrees=mask_agrees if comparison else None),allow_nan=False))


if __name__=='__main__':main()
