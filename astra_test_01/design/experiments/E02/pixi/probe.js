const {Application, Container, Graphics, Sprite, Assets, Text, Point, RenderTexture} = PIXI;
const [profiles, layout, analysis] = await Promise.all([
  fetch('../inputs/projection-candidates.json').then(r=>r.json()),
  fetch('../inputs/chamber-layout.json').then(r=>r.json()),
  fetch('../evidence/analysis.json').then(r=>r.json()),
]);
const texture = await Assets.load('../inputs/legacy-idle-S.png');
texture.source.scaleMode = 'linear';
const app = new Application();
await app.init({width:1440,height:1000,resolution:1,preference:'webgl',antialias:true,
  background:0x11151a,autoStart:false,preserveDrawingBuffer:true});
document.querySelector('#stage').appendChild(app.canvas);
let state = {sample:0, tracking:false, bad:false, point:null};
const rootSource = [256.25,399.5], sourceHeight=223.5;
const t = profiles[2].elevation_deg*Math.PI/180, yaw=profiles[2].yaw_deg*Math.PI/180;
const st=Math.sin(t),ct=Math.cos(t),sy=Math.sin(yaw),cy=Math.cos(yaw);
const f=405/2/Math.tan(profiles[2].vertical_fov_deg*Math.PI/360);
function project(world,h=0,perspective=true){
  const actor=state.point??analysis.samples[state.sample].world;
  const u=world[0]-(state.tracking?actor[0]:0),v=world[1]-(state.tracking?actor[1]:0);
  const right=cy*u-sy*v,depth=sy*u+cy*v;
  const scale=perspective?f/(profiles[2].distance_m-ct*depth-st*h):profiles[1].uniform_scale_px_per_m;
  return [profiles[2].anchor[0]+scale*right,profiles[2].anchor[1]+scale*(st*depth-ct*h)];
}
function text(parent,value,x,y,size=13,color=0xc8cbd0){
  const item=new Text({text:value,style:{fontFamily:'Arial',fontSize:size,fill:color}});
  item.position.set(x,y-size);parent.addChild(item);return item;
}
function world(perspective){
  const parent=new Container(),g=new Graphics();parent.addChild(g);
  g.rect(0,0,720,405).fill(0x20262c);
  const pr=(w,h=0)=>project(w,h,perspective);
  function line(a,b,color=0x71736d,width=.7){g.moveTo(...a).lineTo(...b).stroke({color,width});}
  for(const surface of layout.surfaces){const [a,b,c,d]=surface.rect;
    g.poly([[a,b],[c,b],[c,d],[a,d]].flatMap(w=>pr(w))).fill(surface.id==='stone'?0x3d464e:0x514737);
  }
  for(let u=-5;u<=5;u++)line(pr([u,-4]),pr([u,4]));
  for(let v=-4;v<=4;v++)line(pr([-5,v]),pr([5,v]));
  for(const obj of [...layout.static_blocks,...layout.objects]){const [a,b,c,d]=obj.rect;
    g.poly([[a,b],[c,b],[c,d],[a,d]].flatMap(w=>pr(w))).stroke({color:0xa49a82,width:1});}
  for(const exit of layout.exits){const p=pr(exit.point);g.circle(...p,3).fill(0xd8b87b);text(parent,exit.id,p[0]+5,p[1]+4,11);}
  const actor=state.point??analysis.samples[state.sample].world;
  const ring=[];for(let i=0;i<=64;i++){const a=Math.PI*2*i/64;ring.push(...pr([actor[0]+.7*Math.cos(a),actor[1]+.7*Math.sin(a)]));}
  g.poly(ring).stroke({color:0xc9ac6c,width:1});
  const root=pr(actor),top=pr(actor,2),scale=(root[1]-top[1])/sourceHeight*(state.bad&&perspective?1.25:1);
  g.circle(...root,2).fill(0xf5dfab);
  for(const offset of [-1.1,1.1]){const w=[actor[0]+cy*offset,actor[1]-sy*offset];const a=pr(w),b=pr(w,2);line(a,b,0x91a5b5,1);g.circle(...b,2).fill(0x91a5b5);}
  const actorNode=new Container();actorNode.position.set(...root);actorNode.scale.set(scale);
  const sprite=new Sprite(texture);sprite.position.set(-rootSource[0],-rootSource[1]);actorNode.addChild(sprite);
  const socket=new Container();socket.position.set(203-rootSource[0],187-rootSource[1]);actorNode.addChild(socket);
  parent.addChild(actorNode);
  const hud=new Graphics().rect(0,369,720,36).fill(0x13171b);parent.addChild(hud);
  text(parent,'DIAGNOSTIC FLOOR / footprints only / frozen pose / no collision',12,390,12);
  const mask=new Graphics().rect(0,0,720,405).fill(0xffffff);parent.addChild(mask);parent.mask=mask;
  return {parent,actorNode,sprite,socket,root,top,scale};
}
let visible=[];
let detailTextures=[];
function render(){
  for(const child of app.stage.removeChildren())child.destroy({children:true});
  for(const texture of detailTextures)texture.destroy(true);
  detailTextures=[];
  text(app.stage,'E02 / C PERSPECTIVE / PAINTED SPRITE TRANSFER',20,30,23,0xe2e0db);
  text(app.stage,state.tracking?'Following camera':'Fixed room camera',20,59,17);
  text(app.stage,'Position: '+(state.point?'continuous translation':analysis.samples[state.sample].id)+' | same painted source in both views',340,59,16);
  visible=[];
  for(let i=0;i<2;i++){
    text(app.stage,i===0?'B / affine diagnostic control':'C / chosen perspective candidate',i*720+15,85,18);
    const w=world(i===1);
    const rendered=RenderTexture.create({width:720,height:405,resolution:1});
    rendered.source.scaleMode='linear';
    app.renderer.render({container:w.parent,target:rendered,clear:true});
    detailTextures.push(rendered);
    w.parent.position.set(i*720,95);app.stage.addChild(w.parent);visible.push(w);
    text(app.stage,'3x diagnostic enlargement / judge normal size above',i*720+60,539,14);
    const box=new Container();box.position.set(i*720+60,555);app.stage.addChild(box);
    const detail=new Sprite(rendered);detail.scale.set(3);detail.position.set(-(w.root[0]-85)*3,-(w.root[1]-105)*3);box.addChild(detail);
    const clip=new Graphics().rect(0,0,510,405).fill(0xffffff);box.addChild(clip);box.mask=clip;
  }
  if(state.bad)text(app.stage,'BAD CONTROL: 25% oversized',970,59,17,0xffaf80);
  app.render();
}
function results(){
  const w=visible[1];const origin=w.parent.toGlobal(new Point(0,0));
  const actualRoot=w.actorNode.toGlobal(new Point(0,0));
  const actualSocket=w.socket.toGlobal(new Point(0,0));
  const expectedSocket=[w.root[0]+(203-rootSource[0])*w.scale,w.root[1]+(187-rootSource[1])*w.scale];
  const gl=app.renderer.gl,ext=gl.getExtension('WEBGL_debug_renderer_info');
  return {pixi:PIXI.VERSION,tracking:state.tracking,sample:analysis.samples[state.sample].id,
    root_px:[actualRoot.x-origin.x,actualRoot.y-origin.y],top_px:w.top,
    source_scale:w.scale,root_error_px:Math.hypot(actualRoot.x-origin.x-w.root[0],actualRoot.y-origin.y-w.root[1]),
    socket_error_px:Math.hypot(actualSocket.x-origin.x-expectedSocket[0],actualSocket.y-origin.y-expectedSocket[1]),
    backend:gl.getParameter(gl.VERSION),renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)};
}
function negativeControls(){
  const w=visible[1],root=w.root,oldX=w.actorNode.x;
  w.actorNode.x+=8;const actual=w.parent.toLocal(w.actorNode.toGlobal(new Point(0,0)));
  const rootRejected=Math.hypot(actual.x-root[0],actual.y-root[1])>.5;w.actorNode.x=oldX;
  const oldSocket=w.socket.x;w.socket.x+=8/w.scale;
  const wrong=w.parent.toLocal(w.socket.toGlobal(new Point(0,0)));
  const expected=[root[0]+(203-rootSource[0])*w.scale,root[1]+(187-rootSource[1])*w.scale];
  const socketRejected=Math.hypot(wrong.x-expected[0],wrong.y-expected[1])>.5;w.socket.x=oldSocket;
  return {runtime_shifted_root_rejected:rootRejected,runtime_shifted_socket_rejected:socketRejected};
}
const select=document.querySelector('#position');analysis.samples.forEach((s,i)=>select.add(new Option(s.id,i)));
select.onchange=()=>{state.sample=Number(select.value);state.point=null;render();};
document.querySelector('#tracking').onclick=()=>{state.tracking=!state.tracking;document.querySelector('#tracking').textContent='Following camera: '+(state.tracking?'on':'off');render();};
document.querySelector('#bad').onclick=()=>{state.bad=!state.bad;document.querySelector('#bad').textContent='Bad scale control: '+(state.bad?'on':'off');render();};
let playing=false,start=0;
function tick(time){if(!playing)return;const phase=(time-start)/2000%8,index=Math.floor(phase),blend=phase-index;
  const a=analysis.samples[index].world,b=analysis.samples[index+1].world;
  state.point=[a[0]+(b[0]-a[0])*blend,a[1]+(b[1]-a[1])*blend];render();requestAnimationFrame(tick);}
document.querySelector('#motion').onclick=()=>{playing=!playing;document.querySelector('#motion').textContent=playing?'Pause translation probe':'Play translation probe';if(playing){start=performance.now();requestAnimationFrame(tick);}};
window.E02={set(value){Object.assign(state,value);render();return results();},results,negativeControls,
  frame(){return app.canvas.toDataURL('image/png');},samples:analysis.samples};
render();document.body.dataset.ready='true';
