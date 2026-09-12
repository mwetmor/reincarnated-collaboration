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
from .walk_curves import curves,frame_paths
from .walk_landmarks import figure_mask_row

ROOT=Path(__file__).resolve().parents[1]
OURS_ROOT=ROOT/'runs/C-1/oracle'
LABELS=('plate2_lateral','plate13_lateral','plate13_front','plate13_rear')


def bands(summary,k_vert=2.,k_lat=.5):
    def band(v,k,ceiling=None):
        return dict(floor=v,target=v*k if v is not None else None,ceiling=ceiling)
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
    masks=figure_mask_row(arrays)
    h,w=arrays[0].shape[:2];check=Image.new('RGB',(2*w,h+65),(22,26,35))
    for column,index in enumerate((0,6)):
        a=arrays[index][...,:3].copy();mask=masks[index]
        a[mask]=(a[mask]*.5+np.array([40,220,100])*.5).astype(np.uint8)
        panel=Image.fromarray(a);draw=ImageDraw.Draw(panel);lm=data['landmarks'][index]
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
    plot=Image.new('RGB',(1150,1100),(22,26,35));d=ImageDraw.Draw(plot)
    d.text((20,12),label+' / source-pixel curves / provisional bands',fill='white')
    seq=data['landmarks'];H=data['summary']['H_median']
    panels=[('head image y; red NCC, yellow mask lineage',{'head_top_y':'#ff7777','head_top_mask_y':'#eeee66'},band['W1']),
            ('head x; blue',{'head_cx':'#66bbff'},None),
            ('tracked sole x; L cyan, R green',{'foot_L_x':'cyan','foot_R_x':'#66ee99'},None),
            ('extent at 0.45H; L cyan, R green',{'wrist_ext_L':'cyan','wrist_ext_R':'#66ee99'},None)]
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
    d.text((20,1040),'Shading: W1 floor/target/ceiling about curve center. Missing phases shown ?. Tracks are image-space proxies.',fill='white')
    d.text((20,1060),'Front/rear sole and arm curves are diagnostics only; W5/W6/scroll summary is null.',fill='white')
    path=directory/f'{label}_curves.png';plot.save(path)
    return [str(check_path),str(path)]


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);src=p.add_mutually_exclusive_group(required=True)
    src.add_argument('--ref',type=Path);src.add_argument('--ours',type=Path)
    p.add_argument('--pattern',default='*.png');p.add_argument('--fps',type=float,required=True)
    p.add_argument('--label',required=True);p.add_argument('--out',type=Path,default=Path('oracle/bands_walk.json'))
    p.add_argument('--plot_dir',type=Path);p.add_argument('--k_vert',type=float,default=2.);p.add_argument('--k_lat',type=float,default=.5)
    args=p.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.label): p.error('invalid label')
    if args.ref and args.label not in LABELS:p.error('reference label must name a contracted plate row')
    if any(not np.isfinite(k) or k<=0 for k in (args.k_vert,args.k_lat)):p.error('multipliers must be positive finite')
    if args.plot_dir and args.plot_dir.resolve().is_relative_to(ROOT) and not args.plot_dir.resolve().is_relative_to(OURS_ROOT):p.error('in-repository plots only under runs/C-1/oracle')
    directory=(args.ref or args.ours).resolve();lateral=not args.label.endswith(('_front','_rear'))
    try:data=curves(directory,args.pattern,args.fps,lateral,ours=bool(args.ours))
    except ValueError as exc:p.error(str(exc))
    provenance=dict(plate=args.label.split('_')[0],row=args.label.split('_')[-1],source=str(directory),
                    source_note='Muybridge public domain' if args.ref else 'own registered sprites',
                    frame_names=data['frame_names'],frames=data['frames'],fps=args.fps,pattern=args.pattern,
                    mask_params=data['mask_params'],k_vert=args.k_vert,k_lat=args.k_lat)
    b=bands(data['summary'],args.k_vert,args.k_lat);data['provenance']=provenance
    if args.plot_dir:
        evidence=_plots(args.plot_dir.resolve(),args.label,frame_paths(directory,args.pattern),data,b)
        for r in data['results']:r['evidence']=evidence
    if args.ref:
        out=args.out.resolve();existing=json.loads(out.read_text()) if out.exists() else {}
        existing[args.label]=dict(bands=b,summary=data['summary'],phase_table=data['phase_table'],
                                  provenance=provenance,curves=data,committed=False)
        _write(out,existing)
    else:
        out=OURS_ROOT/f'{args.label}_ours.json';_write(out,data)
    print(json.dumps(dict(label=args.label,out=str(out),summary=data['summary'],phase_table=data['phase_table']),allow_nan=False))


if __name__=='__main__':main()
