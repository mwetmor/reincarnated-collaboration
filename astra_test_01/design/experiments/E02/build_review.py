"""Package unmodified engine captures into HTML and a Canvas. No art editing."""
from pathlib import Path
import base64
import json

P=Path(__file__).resolve().parent
samples=['center','far','near','left','right','far-left','far-right','near-left','near-right']
rows=[]
for policy in ['fixed','tracking']:
    for sample in samples:
        rows.append({'key':f'{policy}:{sample}','sample':sample,'policy':policy,
                     'Godot':f'evidence/{policy}-v2-{sample}.png',
                     'Pixi.js':f'evidence/pixi-v2-{policy}-{sample}.png'})
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>E02 — C in Godot and Pixi.js</title><style>
body{margin:0;background:#15191e;color:#e4e2dc;font:16px/1.5 system-ui}main{padding:24px}h1{font-size:26px;margin:0}h2{font-size:20px}a{color:#dfc087}select{padding:8px;background:#29313a;color:inherit;font:inherit}nav{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}.pair{display:grid;grid-template-columns:720px 720px;gap:20px;overflow:auto}.native{width:720px;height:405px;overflow:hidden;position:relative}.native img{position:absolute;width:1440px;max-width:none;left:-720px;top:-95px}.detail{width:510px;height:405px;overflow:hidden;position:relative}.detail img{position:absolute;width:1440px;max-width:none;left:-780px;top:-555px}p{max-width:1100px}.quiet{color:#b8bdc5}button{font:inherit}table{border-collapse:collapse}td,th{padding:10px;text-align:left;border-bottom:1px solid #434a51}</style>
<main><h1>Projection C, two renderers</h1><p>Godot and Pixi.js render the same painted source and logical chamber. C remains the test candidate. This is a static-pose transfer probe on diagnostic geometry; painted floors, motion, gear and VFX are still unqualified.</p>
<nav><label>Camera <select id="policy"><option value="fixed">Fixed room camera</option><option value="tracking">Following actor</option></select></label><label>Position <select id="sample"></select></label><a href="pixi/">Run Pixi.js probe (local server)</a><a href="RENDERER_RESEARCH.md">Alternatives research</a><a href="REPORT.md">Results and limits</a></nav>
<p class="quiet">Native scene regions below are 720×405, without rescaling. Scroll horizontally on narrow screens. The lower views enlarge each engine's rendered pixels 3×.</p>
<div class="pair"><section><h2>C / Godot 4.6.3</h2><div class="native"><img id="godot" alt="C projection in Godot"></div><p><a id="godot-link">Open full Godot capture</a></p><div class="detail"><img id="godot-detail" alt="Godot three times diagnostic enlargement"></div></section><section><h2>C / Pixi.js 8.20.1</h2><div class="native"><img id="pixi" alt="C projection in Pixi.js"></div><p><a id="pixi-link">Open full Pixi capture</a></p><div class="detail"><img id="pixi-detail" alt="Pixi three times diagnostic enlargement"></div></section></div>
<h2>What this establishes</h2><p>95 component checks passed. Runtime projection agrees with independent references within 0.000020 pixels. A fixed-view cuboid proxy diverges by up to 6.93 pixels from true perspective at lateral sample positions; that flags an approximation, not a painted-character rejection. Following the actor removes its position-dependent viewpoint change.</p>
<p>In the inspected frames, the stronger disagreement is visible beside vertical guides away from center. The small legacy sprite does not establish whether it would be objectionable in a fully painted scene. Continue C; test a C-conditioned source and painted props next.</p>
<h2>Renderer shortlist</h2><p><strong>Godot + Pixi.js: tested foundation. Phaser 4: recommended third test.</strong> Defold and Cocos are reserves; Three.js is a separate representation experiment if painted planes or depth become necessary. No production winner yet.</p>
<p><a href="RENDERER_BENCHMARK.md">Shared composition benchmark</a> · <a href="RECEIPT.json">Receipt</a> · <a href="evidence/validation.json">Validation</a> · <a href="../../START_HERE.md">Restart handoff</a></p></main>
<script>const rows=ROWS;const sel=document.querySelector('#sample');for(const s of SAMPLES)sel.add(new Option(s,s));sel.value='right';function show(){const row=rows.find(r=>r.sample===sel.value&&r.policy===document.querySelector('#policy').value);for(const [id,key] of [['godot','Godot'],['pixi','Pixi.js']]){document.querySelector('#'+id).src=row[key];document.querySelector('#'+id+'-detail').src=row[key];document.querySelector('#'+id+'-link').href=row[key];}}sel.onchange=show;document.querySelector('#policy').onchange=show;show();</script></html>
'''.replace('ROWS',json.dumps(rows)).replace('SAMPLES',json.dumps(samples))
(P/'review.html').write_text(html)

# Canvas embeds original screenshots. Only CSS selects the native scene region.
canvas_rows=[]
for r in rows:
    if r['sample'] not in ['center','right','near','far']:
        continue
    item={k:r[k] for k in ['key','sample','policy']}
    for engine in ['Godot','Pixi.js']:
        item[engine]='data:image/png;base64,'+base64.b64encode((P/r[engine]).read_bytes()).decode()
    canvas_rows.append(item)
canvas="""import { Stack, Grid, H1, H2, Text, Divider, Select, Table, useCanvasState, useHostTheme } from 'cursor/canvas';
const captures = DATA;
export default function E02Comparison(){
 const theme=useHostTheme();
 const [sample,setSample]=useCanvasState('E02-position','right');
 const [policy,setPolicy]=useCanvasState('E02-camera','fixed');
 const row=captures.find(r=>r.sample===sample&&r.policy===policy)??captures[0];
 return <Stack gap={20}>
 <H1>Projection C in Godot and Pixi.js</H1>
 <Text>C is selected for testing. Both renderers run the same painted source, layout and transforms. This is a frozen-pose probe on diagnostic geometry.</Text>
 <Grid columns={2} gap={16}><div><Text>Camera</Text><Select value={policy} onChange={setPolicy} options={[{value:'fixed',label:'Fixed room camera'},{value:'tracking',label:'Following actor'}]}/></div><div><Text>Position</Text><Select value={sample} onChange={setSample} options={['center','right','near','far'].map(v=>({value:v,label:v}))}/></div></Grid>
 <Grid columns={2} gap={16}>{(['Godot','Pixi.js'] as const).map(engine=><Stack key={engine} gap={8}><H2>{engine}</H2><div style={{width:'100%',aspectRatio:'720 / 405',overflow:'hidden',position:'relative',background:theme.bg.editor}}><img alt={engine+' native scene capture'} src={row[engine]} style={{position:'absolute',width:'200%',maxWidth:'none',left:'-100%',top:'-23.45679%'}}/></div><Text tone="secondary" size="small">Native 720×405 scene; fitted to this panel. Open the HTML review for native-size inspection.</Text></Stack>)}</Grid>
 <H2>Result</H2><Text>95 component checks pass. Maximum runtime/reference error: 0.000020px. Lateral samples show a geometric upright-sprite approximation up to 6.93px on the known-volume proxy. That does not establish an objectionable painted-character defect.</Text>
 <Text>The following camera removes the centered actor’s position-dependent view change. Continue C into a painted chamber test. Legacy source viewpoint, gear, animation, VFX and final floor cohesion remain unqualified.</Text>
 <Divider/><H2>Renderer research</H2>
 <Table headers={['Renderer','Evidence now','Next use']} rows={[
 ['Godot 4.6.3','GPU render + attachment checks','Full chamber comparator'],
 ['Pixi.js 8.20.1','GPU render + browser controls','Full chamber comparator'],
 ['Phaser 4','Primary documentation only','Recommended third test'],
 ['Defold / Cocos','Primary documentation only','Reserve alternate workflows'],
 ['Three.js','Primary documentation only','Separate painted-plane/depth experiment']
 ]}/>
 <Text>No production winner. Compare the same masked prop, gear attachment, timed VFX and requested edits; keep combat JSON fixed.</Text>
 <a style={{color:theme.text.link}} href="REPORTPATH">Report, sources and restart commands</a>
 </Stack>;
}
""".replace('DATA',json.dumps(canvas_rows)).replace('REPORTPATH',str(P/'REPORT.md'))
(P/'renderer-comparison.canvas.tsx').write_text(canvas)
Path('/Users/admin/.cursor/projects/Users-admin-Games/canvases/astra-E02-renderer-comparison.canvas.tsx').write_text(canvas)
print('Wrote review.html and both byte-identical Canvas copies')
