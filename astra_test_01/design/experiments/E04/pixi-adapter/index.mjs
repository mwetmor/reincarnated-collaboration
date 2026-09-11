import {step} from '../sim/index.mjs';
const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);import {makeProjection} from './projection.mjs';
const [layout,profiles,visual,catalog]=await Promise.all(['../E03/inputs/chamber-layout.json','../E03/inputs/projection-candidates.json','visual-data.json','manifests/catalog.json'].map(p=>fetch(p).then(r=>r.json())));
const manifestList=await Promise.all(catalog.manifest_files.map(async file=>{const url=new URL('manifests/'+file,location.href);const m=await fetch(url).then(r=>r.json());m.resolvedSource=new URL(m.frames[0].source_path,new URL(m.path_base,url)).href;return m;}));
const manifests=Object.fromEntries(manifestList.map(m=>[m.id,m]));
const decode=m=>({root:m.frames[0].pivot,axis_height:m.registration.source_axis_height,mask:m.silhouette_polygon,height_m:m.registration.physical_height_m});
const actorAssets=Object.fromEntries(manifestList.filter(m=>m.asset_type==='character').map(m=>[m.id,decode(m)]));const prior={assets:{mage:actorAssets.mage}};
const {project,inverse}=makeProjection(profiles[2]);
const resolution=Number(new URLSearchParams(location.search).get("resolution")??1);if(![1,3].includes(resolution))throw Error("Resolution must be 1 or 3 for the registered comparison");
const app=new PIXI.Application();await app.init({width:960,height:640,resolution,autoDensity:true,preference:'webgl',antialias:true,background:0x1c2125,autoStart:false,preserveDrawingBuffer:true});document.querySelector('#stage').appendChild(app.canvas);
const textures={};for(const m of manifestList)textures[m.id]=await PIXI.Assets.load(m.resolvedSource);
let selected='mage',debug=false,route=[],demoTime=null,demoDone=new Set(),paused=false;
const content={schema_version:1,test_mode:true,layout,movement_speed_mps:2};
let sim,actors,model;
function sync(){actors=sim.state.actors;route=sim.state.routes[selected]??[];model={state:sim.state.chamber.state,time:sim.state.chamber.time,pending:sim.state.chamber.pending,blockers:()=>sim.blockers};}
function dispatch(commands=[],dt_ms=0){sim=step(JSON.parse(JSON.stringify({content,state:sim?.state??null,commands,dt_ms})));sync();return sim.outcomes;}
dispatch();
const frameTimes=[];let last=performance.now(),drawCount=0,drawMs=[],lastRenderedState=null;
const quad=(parent,texture,world,source)=>{
 const vertices=[],uvs=[],indices=[],n=4,w=texture.width,h=texture.height;
 const bil=(q,s,t)=>q[0].map((_,k)=>q[0][k]*(1-s)*(1-t)+q[1][k]*s*(1-t)+q[2][k]*s*t+q[3][k]*(1-s)*t);
 for(let j=0;j<=n;j++)for(let i=0;i<=n;i++){const s=i/n,t=j/n,p=bil(world,s,t),uv=bil(source,s,t);vertices.push(...project(p,p[2]));uvs.push(uv[0]/w,uv[1]/h);if(i<n&&j<n){const a=j*(n+1)+i;indices.push(a,a+1,a+n+2,a,a+n+2,a+n+1);}}
 const mesh=new PIXI.MeshSimple({texture,vertices:new Float32Array(vertices),uvs:new Float32Array(uvs),indices:new Uint32Array(indices)});parent.addChild(mesh);return mesh;
};
const full=id=>[[0,0],[textures[id].width,0],[textures[id].width,textures[id].height],[0,textures[id].height]];
function box(parent,rect,height,id,base=0){const[a,b,c,d]=rect,faces=visual[id]?.faces;quad(parent,textures[id],[[a,d,height+base],[c,d,height+base],[c,d,base],[a,d,base]],faces?.left??full(id));quad(parent,textures[id],[[c,d,height+base],[c,b,height+base],[c,b,base],[c,d,base]],faces?.right??full(id));quad(parent,textures[id],[[a,b,height+base],[c,b,height+base],[c,d,height+base],[a,d,height+base]],faces?.top??full(id));}
function masked(parent,id,source,point,height){const root=project(point),top=project(point,height),s=(root[1]-top[1])/source.axis_height;const node=new PIXI.Container();node.position.set(root[0]-source.root[0]*s,root[1]-source.root[1]*s);node.scale.set(s);const sprite=new PIXI.Sprite(textures[id]);node.addChild(sprite);const effects=actors[id]?.effects??{};if(effects.tint)sprite.tint=parseInt(effects.tint.color.slice(1),16);if(effects.flash){const filter=new PIXI.ColorMatrixFilter();const color=parseInt(effects.flash.color.slice(1),16),r=(color>>16&255)/255,g=(color>>8&255)/255,b=(color&255)/255;filter.matrix=[.5,0,0,0,r*.5,0,.5,0,0,g*.5,0,0,.5,0,b*.5,0,0,0,1,0];sprite.filters=[filter];}for(const kind of Object.keys(effects))if(!['tint','flash'].includes(kind))throw Error('Unqualified effect kind '+kind);const mask=new PIXI.Graphics().poly(source.mask.flat()).fill(0xffffff);node.addChild(mask);sprite.mask=mask;parent.addChild(node);return{node,root,scale:s};}
function render(){const started=performance.now();for(const child of app.stage.removeChildren())child.destroy({children:true});const floor=new PIXI.Sprite(textures.floor);floor.scale.set(.625);app.stage.addChild(floor);const entries=[];
 const add=(key,fn)=>entries.push({key,fn});
 for(const block of layout.static_blocks){const[a,b,c,d]=block.rect;if(block.id==='pillar'){add(project([(a+c)/2,(b+d)/2])[1],par=>box(par,block.rect,block.height,'stone'));}else{const count=Math.ceil(d-b);for(let i=0;i<count;i++){const lo=b+(d-b)*i/count,hi=b+(d-b)*(i+1)/count;add(project([(a+c)/2,(lo+hi)/2])[1],par=>box(par,[a,lo,c,hi],block.height,'stone'));}}}
 // Raised lintel is a separate visual occluder, not a ground blocker.
 add(project([2.15,0])[1]+.01,par=>box(par,[2,-1.25,2.3,1.25],.3,'stone',2.5));
 let openness=model.state.door==='open'?1:0;if(model.pending){const progress=1-(model.pending.at-model.time)/.5;openness=model.state.door==='opening'?progress:1-progress;}openness=Math.max(0,Math.min(1,openness));
 if(openness<.999){const low=openness*2.5;add(project([2.15,0])[1],par=>quad(par,textures.door,[[2.31,1.25,2.5],[2.31,-1.25,2.5],[2.31,-1.25,low],[2.31,1.25,low]],[[0,textures.door.height*openness],[textures.door.width,textures.door.height*openness],[textures.door.width,textures.door.height],[0,textures.door.height]]));}
 const crate=layout.objects.find(o=>o.id==='crate');if(model.state.crate==='intact')add(project([0,2.8])[1],par=>box(par,crate.rect,.9,'crate'));else{
  const root=project([0,2.8]),extent=dist(project([-.5,2.3]),project([.5,3.3])),scale=extent/visual.crate.debris_scale_source_width;
  const node=new PIXI.Container();node.position.set(root[0]-visual.crate.debris_root[0]*scale,root[1]-visual.crate.debris_root[1]*scale);node.scale.set(scale);const image=new PIXI.Sprite(textures.crate),mask=new PIXI.Graphics();for(const poly of visual.crate.debris_polygons)mask.poly(poly.flat()).fill(0xffffff);node.addChild(image,mask);image.mask=mask;app.stage.addChild(node);
 }
 const chest=layout.objects.find(o=>o.id==='chest');add(project([-3.5,1.9])[1],par=>{box(par,chest.rect,.65,'chest');if(model.state.chest!=='closed'){
  const[a,b,c,d]=chest.rect;quad(par,textures.chest,[[a,b,1.3],[c,b,1.3],[c,b+.12,.65],[a,b+.12,.65]],full('chest'));
 }else{box(par,chest.rect,.15,'chest',.65);}});
 if(model.state.loot==='ground'){const pt=project([-3.5,.65]);const g=new PIXI.Graphics().circle(...pt,4).fill(0xdfc477);app.stage.addChild(g);}
 for(const [id,a]of Object.entries(actors)){const root=project(a.point);const shadow=new PIXI.Graphics().ellipse(root[0],root[1],a.radius*30,a.radius*14).fill({color:0x101316,alpha:.35});app.stage.addChild(shadow);add(root[1],par=>masked(par,id,id==='mage'?prior.assets.mage:actorAssets[id],a.point,a.height));}
 entries.sort((a,b)=>a.key-b.key);for(const e of entries){const parent=new PIXI.Container();app.stage.addChild(parent);e.fn(parent);}
 if(debug){const g=new PIXI.Graphics();app.stage.addChild(g);for(const b of model.blockers()){const[a,v,c,d]=b.rect;g.poly([[a,v],[c,v],[c,d],[a,d]].flatMap(p=>project(p))).stroke({color:0x60e2d4,width:1});}if(route.length){g.moveTo(...project(actors[selected].point));for(const p of route)g.lineTo(...project(p));g.stroke({color:0xffd775,width:2});}}
 app.render();drawCount++;drawMs.push(performance.now()-started);if(drawMs.length>600)drawMs.shift();lastRenderedState=structuredClone(model.state);
 document.querySelector('#log').textContent='Gate: '+model.state.door+'\nCrate: '+model.state.crate+'\nChest: '+model.state.chest+'\nLoot: '+model.state.loot+'\nNavigation revision: '+model.state.navVersion+'\n\n'+model.state.events.map(e=>e.time.toFixed(2)+' '+e.type+' '+e.id).join('\n');
 document.querySelector('#status').textContent='Selected: '+selected+' · '+(route.length?'moving frozen pose':'idle frozen pose')+' · geometry/state tests; no gait qualification';
}
function action(name){const result=dispatch([{type:'authoritative_event',action:name}]);render();return result[0].accepted;}
function moveTo(point){const result=dispatch([{type:'move',entity_id:selected,point}]);render();return result[0].accepted;}
function reset(){sim=null;dispatch();demoDone=new Set();render();}
function advance(dt){dispatch([],dt*1000);render();}
const demo=[{at:.4,action:'open'},{at:.8,action:'unlock'},{at:1.2,action:'open'},{at:2,move:[3.3,0]},{at:4.2,point:[2.15,0],action:'close'},{at:5,point:[3.3,0],action:'close'},{at:6,action:'open'},{at:7,action:'break'},{at:8,action:'chest'},{at:8.5,action:'chest'},{at:9.5,action:'pickup'},{at:10,action:'pickup'},{at:11,reload:true}];
function tick(now){const dt=(now-last)/1000;last=now;frameTimes.push(dt*1000);if(frameTimes.length>1200)frameTimes.shift();if(!paused){if(demoTime!==null){demoTime+=dt;demo.forEach((e,i)=>{if(demoTime>=e.at&&!demoDone.has(i)){demoDone.add(i);if(e.point)dispatch([{type:'place_fixture',entity_id:'mage',point:e.point}]);if(e.move)moveTo(e.move);if(e.action)action(e.action);if(e.reload){sim=step({content,state:JSON.parse(JSON.stringify(sim.state)),commands:[],dt_ms:0});sync();}}});if(demoTime>12)demoTime=null;}if(Object.values(sim.state.routes).some(r=>r.length)||Object.values(actors).some(a=>Object.keys(a.effects).length)||model.pending||demoTime!==null)advance(dt);}requestAnimationFrame(tick);}
for(const button of document.querySelectorAll('[data-action]'))button.onclick=()=>action(button.dataset.action);
document.querySelector('#actor').onchange=e=>{selected=e.target.value;dispatch([{type:'stop',entity_id:selected}]);render();};document.querySelector('#debug').onclick=()=>{debug=!debug;render();};document.querySelector('#reset').onclick=()=>{demoTime=null;reset();};document.querySelector('#reload').onclick=()=>{sim=step({content,state:JSON.parse(JSON.stringify(sim.state)),commands:[],dt_ms:0});sync();render();};document.querySelector('#demo').onclick=()=>{reset();selected='mage';demoTime=0;};
app.canvas.addEventListener('pointerdown',e=>{const r=app.canvas.getBoundingClientRect();moveTo(inverse([(e.clientX-r.left)*960/r.width,(e.clientY-r.top)*640/r.height]));});
const percentile=(values,p)=>[...values].sort((a,b)=>a-b)[Math.min(values.length-1,Math.floor(values.length*p))]??null;
window.E04={reset,action,moveTo,advance,project,inverse,select(id){selected=id;sync();},setPoint(id,p){dispatch([{type:'place_fixture',entity_id:id,point:p}]);render();},pause(v){paused=v;},reload(){sim=step({content,state:JSON.parse(JSON.stringify(sim.state)),commands:[],dt_ms:0});sync();render();},debug(v){debug=v;render();},effect(id,e){dispatch([{type:'visual_effect',entity_id:id,effect:e}]);render();},snapshot(){const gl=app.renderer.gl,ext=gl.getExtension('WEBGL_debug_renderer_info');return{json_state:structuredClone(sim.state),state:structuredClone(model.state),rendered_state:lastRenderedState,actors:structuredClone(actors),route:structuredClone(route),model_time:model.time,pixi:PIXI.VERSION,backend:gl.getParameter(gl.VERSION),renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),resolution,buffer_size:[app.canvas.width,app.canvas.height],draw_count:drawCount,frame_ms:{p50:percentile(frameTimes,.5),p95:percentile(frameTimes,.95)},composition_cpu_ms:{p50:percentile(drawMs,.5),p95:percentile(drawMs,.95)}};}};
render();document.body.dataset.ready='true';requestAnimationFrame(tick);
