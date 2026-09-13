"""Offline direction/animation review wheel (plain HTML, canvas and video).

python3 -B -m review.viewer_wheel --cells DIR --out EMPTY_DIR
Raw cut cells and T3d MP4 review packets may be nested below DIR. Optional
DIR/missing.json maps animation_DIRECTION to a reason string (or {reason:…}).
Absent entries display an explicit 'Cell not supplied' reason. No gameplay.
"""
import argparse
import html
import json
from pathlib import Path
import shutil
import time
from urllib.parse import unquote, urlsplit

from export.godot_import import DIRECTIONS, FPS, discover_cells, local_file, _output
from .cell_packet import validate_packet_html


def _json(data):
    return json.dumps(data, ensure_ascii=True, allow_nan=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def validate_viewer(path):
    """Validate both markup references and assets embedded in JSON data."""
    path = Path(path)
    references = validate_packet_html(path)
    document = path.read_text()
    start = document.index('<script id="cell-data" type="application/json">')
    data = json.loads(document[document.index('>', start)+1:document.index('</script>', start)])
    root = path.parent.resolve()
    for entry in data.values():
        for ref in entry.get('frames', []) + [entry[k] for k in ('video', 'numbers_path') if k in entry]:
            decoded = unquote(ref)
            url = urlsplit(decoded)
            if url.scheme or url.netloc or decoded.startswith(('/', '\\')) or '\\' in decoded or url.query or url.fragment:
                raise ValueError('Nonlocal viewer asset: '+ref)
            local_file(root/url.path, root)
            references.append(ref)
    return references


DOCUMENT = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' file:; media-src 'self' file:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'">
<title>Keeper cell review wheel</title>
<style>
body{margin:0;background:#171d27;color:#e7edf5;font:16px/1.5 system-ui}
main{max-width:1100px;margin:auto;padding:24px}button,a{color:#dcecff}
button{background:#29364a;border:1px solid #61718b;padding:10px;cursor:pointer;font:inherit}
button[aria-pressed=true]{background:#526d91;border-color:#c5ddff}
.layout{display:flex;gap:24px;flex-wrap:wrap}.wheel{display:grid;grid-template-columns:repeat(3,64px);gap:5px;margin:18px 0}
.wheel button[data-dir=N]{grid-area:1/2}.wheel button[data-dir=NE]{grid-area:1/3}
.wheel button[data-dir=E]{grid-area:2/3}.wheel button[data-dir=SE]{grid-area:3/3}
.wheel button[data-dir=S]{grid-area:3/2}.wheel button[data-dir=SW]{grid-area:3/1}
.wheel button[data-dir=W]{grid-area:2/1}.wheel button[data-dir=NW]{grid-area:1/1}
canvas,video{width:512px;max-width:100%;height:auto;background:#3a3f4a}
[hidden]{display:none!important}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#202a39;padding:16px}
#reason{color:#ffd79e}#animations{display:flex;gap:6px;flex-wrap:wrap}
</style></head><body><main><h1>Keeper cell review wheel</h1>
<p>Offline cell playback and recorded measurements. No gameplay.</p>
<nav id="animations" aria-label="Animation">@@ANIMATIONS@@</nav>
<div class="layout"><section><div class="wheel" aria-label="Direction">@@DIRECTIONS@@</div>
<button id="play">Pause</button> <button id="restart">Restart</button>
<button id="previous">Previous frame</button> <button id="next">Next frame</button>
<p id="status" aria-live="polite"></p><p id="reason"></p></section>
<section><canvas id="frame" width="512" height="512" aria-label="Selected cell frame"></canvas>
<video id="video" controls muted playsinline preload="metadata" hidden></video></section></div>
<h2>Recorded numbers</h2><pre id="numbers"></pre><p id="numbers-link"></p>
<h2>Available cells</h2><ul>@@LIST@@</ul>
<script id="cell-data" type="application/json">@@DATA@@</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('cell-data').textContent);
const $=id=>document.getElementById(id),ctx=$('frame').getContext('2d');
let anim='@@INITIAL_ANIM@@',direction='@@INITIAL_DIR@@',entry=null,frames=[],frame=0;
let elapsed=0,last=null,playing=true,generation=0;
const isLoop=()=>!['jump','cast'].includes(anim);
function showFrame(){
 ctx.clearRect(0,0,512,512);
 if(frames[frame])ctx.drawImage(frames[frame],0,0);
 $('status').textContent=anim+'_'+direction+(entry&&!entry.reason?' · '+entry.fps+' fps'+
 (entry.video?' · MP4 playback':' · frame '+frame+' / '+(frames.length-1)):' · missing');
}
function select(){
 const token=++generation;entry=data[anim+'_'+direction];frames=[];frame=0;elapsed=0;last=null;
 const video=$('video');video.pause();video.removeAttribute('src');video.load();
 video.hidden=true;$('frame').hidden=false;$('reason').textContent=entry.reason||'';
 $('numbers').textContent=JSON.stringify(entry.numbers??[],null,2);
 $('numbers-link').replaceChildren();
 if(entry.numbers_path){const a=document.createElement('a');a.href=entry.numbers_path;a.textContent='Numbers JSON';$('numbers-link').append(a);}
 document.querySelectorAll('[data-dir]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.dir===direction));
 document.querySelectorAll('[data-anim]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.anim===anim));
 for(const id of ['play','restart','previous','next'])$(id).disabled=Boolean(entry.reason);
 $('play').textContent=playing?'Pause':'Play';showFrame();
 if(entry.reason)return;
 if(entry.video){
  $('frame').hidden=true;video.hidden=false;video.loop=isLoop();video.src=entry.video;
  video.onerror=()=>{$('reason').textContent='Video could not load: '+entry.video;};
  if(playing)video.play().catch(()=>{$('reason').textContent='Use the video Play control to start playback.';});
 }else{
  Promise.all(entry.frames.map(path=>new Promise((resolve,reject)=>{
   const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error(path));im.src=path;
  }))).then(images=>{if(token===generation){frames=images;elapsed=0;last=null;showFrame();}})
  .catch(error=>{if(token===generation)$('reason').textContent='Frame could not load: '+error.message;});
 }
}
document.querySelectorAll('[data-dir]').forEach(b=>b.onclick=()=>{direction=b.dataset.dir;select();});
document.querySelectorAll('[data-anim]').forEach(b=>b.onclick=()=>{anim=b.dataset.anim;select();});
$('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'Pause':'Play';
 if(entry.video){if(playing)$('video').play().catch(()=>{});else $('video').pause();}};
$('restart').onclick=()=>{elapsed=0;frame=0;last=null;if(entry.video)$('video').currentTime=0;showFrame();};
function step(delta){
 playing=false;$('play').textContent='Play';
 if(entry.video){$('video').pause();$('video').currentTime=Math.max(0,$('video').currentTime+delta/entry.fps);}
 else if(frames.length){frame=isLoop()?(frame+delta+frames.length)%frames.length:Math.max(0,Math.min(frames.length-1,frame+delta));elapsed=frame/entry.fps;showFrame();}
}
$('previous').onclick=()=>step(-1);$('next').onclick=()=>step(1);
function tick(ms){
 if(last!==null&&playing&&frames.length){elapsed+=(ms-last)/1000;
  frame=isLoop()?Math.floor(elapsed*entry.fps)%frames.length:Math.min(frames.length-1,Math.floor(elapsed*entry.fps));showFrame();}
 last=ms;requestAnimationFrame(tick);
}
select();requestAnimationFrame(tick);
</script></main></body></html>
'''


def build_viewer(cells, out):
    started = time.monotonic()
    root = Path(cells).resolve()
    entries = discover_cells(root, allow_video=True)
    missing = {}
    if (root/'missing.json').exists():
        missing = json.loads(local_file(root/'missing.json', root).read_text())
        if not isinstance(missing, dict):
            raise ValueError('missing.json must map cell names to reasons')
    for name, reason in missing.items():
        if name not in {a+'_'+d for a in FPS for d in DIRECTIONS}:
            raise ValueError('Unknown missing cell: '+name)
        if isinstance(reason, dict):
            reason = reason.get('reason')
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('Missing cell needs a nonempty reason: '+name)
        if name in entries:
            raise ValueError('Cell is both present and declared missing: '+name)
        missing[name] = reason
    out = _output(out, [root])
    data = {}
    for anim in FPS:
        for direction in DIRECTIONS:
            name = anim+'_'+direction
            entry = entries.get(name)
            if entry is None:
                data[name] = {'reason': missing.get(name, 'Cell not supplied: '+name), 'numbers': []}
                continue
            folder = out/'cells'/name
            folder.mkdir(parents=True)
            item = {'fps': entry['fps'], 'frames': [], 'numbers': entry['numbers']}
            for source in entry['frames']:
                target = folder/source.name
                shutil.copyfile(source, target)
                item['frames'].append(target.relative_to(out).as_posix())
            if 'video' in entry:
                target = folder/entry['video'].name
                shutil.copyfile(entry['video'], target)
                item['video'] = target.relative_to(out).as_posix()
            target = folder/'numbers.json'
            target.write_text(json.dumps(item['numbers'], indent=2, allow_nan=False)+'\n')
            item['numbers_path'] = target.relative_to(out).as_posix()
            data[name] = item
    initial = sorted(entries)[0] if entries else 'idle_S'
    initial_anim, initial_dir = initial.split('_')
    replacements = {
        'ANIMATIONS': ''.join(f'<button data-anim="{a}">{a}</button>' for a in FPS),
        'DIRECTIONS': ''.join(f'<button data-dir="{d}">{d}</button>' for d in DIRECTIONS),
        'LIST': ''.join('<li>'+html.escape(name)+' — '+
                        ('MP4' if 'video' in entry else str(len(entry['frames']))+' numbered PNGs')+
                        f' at {entry["fps"]:g} fps</li>' for name, entry in sorted(entries.items())),
        'INITIAL_ANIM': initial_anim, 'INITIAL_DIR': initial_dir, 'DATA': _json(data)}
    document = DOCUMENT
    for key, value in replacements.items():
        document = document.replace('@@'+key+'@@', value)
    (out/'index.html').write_text(document)
    refs = validate_viewer(out/'index.html')
    return {'cells': sorted(entries), 'missing_cells': 40-len(entries),
            'references': len(refs), 'wall_s': time.monotonic()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cells', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(json.dumps(build_viewer(args.cells, args.out), indent=2))


if __name__ == '__main__':
    main()
