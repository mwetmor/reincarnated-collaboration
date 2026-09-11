const [profiles,layout,analysis]=await Promise.all([
  fetch('../E02/inputs/projection-candidates.json').then(r=>r.json()),
  fetch('../E02/inputs/chamber-layout.json').then(r=>r.json()),
  fetch('../E02/evidence/analysis.json').then(r=>r.json()),
]);
const profile=profiles[2], rootSource=[256.25,399.5],sourceHeight=223.5;
const t=profile.elevation_deg*Math.PI/180,yaw=profile.yaw_deg*Math.PI/180;
const st=Math.sin(t),ct=Math.cos(t),sy=Math.sin(yaw),cy=Math.cos(yaw);
const f=405/2/Math.tan(profile.vertical_fov_deg*Math.PI/360);
const state={sample:0,tracking:false,bad:false,point:null};
let scene,visible,playing=false,start=0;
function project(world,h=0){
  const actor=state.point??analysis.samples[state.sample].world;
  const u=world[0]-(state.tracking?actor[0]:0),v=world[1]-(state.tracking?actor[1]:0);
  const right=cy*u-sy*v,depth=sy*u+cy*v,scale=f/(profile.distance_m-ct*depth-st*h);
  return [profile.anchor[0]+scale*right,profile.anchor[1]+scale*(st*depth-ct*h)];
}
function render(){
  scene.children.removeAll(true);
  const g=scene.add.graphics();
  g.fillStyle(0x20262c).fillRect(0,0,720,405);
  const polygon=(points,fill,color)=>{g.beginPath();g.moveTo(...points[0]);for(const p of points.slice(1))g.lineTo(...p);g.closePath();if(fill)g.fillStyle(color).fillPath();else g.lineStyle(1,color).strokePath();};
  const line=(a,b,color=0x71736d,width=.7)=>{g.lineStyle(width,color).beginPath().moveTo(...a).lineTo(...b).strokePath();};
  const text=(value,x,y,size=13)=>scene.add.text(x,y-size,value,{fontFamily:'Arial',fontSize:size+'px',color:'#c8cbd0'});
  for(const surface of layout.surfaces){const[a,b,c,d]=surface.rect;polygon([[a,b],[c,b],[c,d],[a,d]].map(w=>project(w)),true,surface.id==='stone'?0x3d464e:0x514737);}
  for(let u=-5;u<=5;u++)line(project([u,-4]),project([u,4]));
  for(let v=-4;v<=4;v++)line(project([-5,v]),project([5,v]));
  for(const obj of [...layout.static_blocks,...layout.objects]){const[a,b,c,d]=obj.rect;polygon([[a,b],[c,b],[c,d],[a,d]].map(w=>project(w)),false,0xa49a82);}
  for(const exit of layout.exits){const p=project(exit.point);g.fillStyle(0xd8b87b).fillCircle(...p,3);text(exit.id,p[0]+5,p[1]+4,11);}
  const actor=state.point??analysis.samples[state.sample].world;
  const ring=[];for(let i=0;i<64;i++){const a=Math.PI*2*i/64;ring.push(project([actor[0]+.7*Math.cos(a),actor[1]+.7*Math.sin(a)]));}polygon(ring,false,0xc9ac6c);
  const root=project(actor),top=project(actor,2),scale=(root[1]-top[1])/sourceHeight*(state.bad?1.25:1);
  g.fillStyle(0xf5dfab).fillCircle(...root,2);
  for(const offset of[-1.1,1.1]){const w=[actor[0]+cy*offset,actor[1]-sy*offset],a=project(w),b=project(w,2);line(a,b,0x91a5b5,1);g.fillStyle(0x91a5b5).fillCircle(...b,2);}
  const sprite=scene.add.image(-rootSource[0],-rootSource[1],'mage').setOrigin(0,0);
  const socket=scene.add.container(203-rootSource[0],187-rootSource[1]);
  const actorNode=scene.add.container(root[0],root[1],[sprite,socket]).setScale(scale);
  scene.add.graphics().fillStyle(0x13171b).fillRect(0,369,720,36);
  text('DIAGNOSTIC FLOOR / footprints only / frozen pose / no collision',12,390,12);
  visible={actorNode,sprite,socket,root,top,scale};
  document.querySelector('#position').value=String(state.sample);
  document.querySelector('#tracking').textContent='Following camera: '+(state.tracking?'on':'off');
  document.querySelector('#bad').textContent='Bad scale control: '+(state.bad?'on':'off');
  document.querySelector('#motion').textContent=playing?'Pause translation probe':'Play translation probe';
  document.querySelector('#status').textContent=(state.tracking?'Following':'Fixed')+' camera · '+(state.point?'continuous translation':analysis.samples[state.sample].id)+(state.bad?' · BAD: 25% oversized':'');
}
function results(){
  const w=visible,r=w.actorNode.getWorldTransformMatrix().transformPoint(0,0),s=w.socket.getWorldTransformMatrix().transformPoint(0,0);
  const expected=[w.root[0]+(203-rootSource[0])*w.scale,w.root[1]+(187-rootSource[1])*w.scale];
  const gl=scene.game.renderer.gl,ext=gl.getExtension('WEBGL_debug_renderer_info');
  return{phaser:Phaser.VERSION,tracking:state.tracking,sample:analysis.samples[state.sample].id,world:state.point??analysis.samples[state.sample].world,
    root_px:[r.x,r.y],top_px:w.top,source_scale:w.actorNode.scaleX,
    root_error_px:Math.hypot(r.x-w.root[0],r.y-w.root[1]),socket_error_px:Math.hypot(s.x-expected[0],s.y-expected[1]),
    backend:gl.getParameter(gl.VERSION),renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)};
}
function negativeControls(){
  const w=visible;w.actorNode.x+=8;const rootError=results().root_error_px;w.actorNode.x-=8;
  w.socket.x+=8/w.scale;const socketError=results().socket_error_px;w.socket.x-=8/w.scale;
  return{root_error_px:rootError,socket_error_px:socketError,runtime_shifted_root_rejected:rootError>.5,runtime_shifted_socket_rejected:socketError>.5};
}
class Probe extends Phaser.Scene{
  preload(){this.load.image('mage','../E02/inputs/legacy-idle-S.png');}
  create(){scene=this;render();
    const select=document.querySelector('#position');analysis.samples.forEach((s,i)=>select.add(new Option(s.id,i)));
    select.onchange=()=>{playing=false;state.sample=Number(select.value);state.point=null;render();};
    document.querySelector('#tracking').onclick=()=>{state.tracking=!state.tracking;document.querySelector('#tracking').textContent='Following camera: '+(state.tracking?'on':'off');render();};
    document.querySelector('#bad').onclick=()=>{state.bad=!state.bad;document.querySelector('#bad').textContent='Bad scale control: '+(state.bad?'on':'off');render();};
    document.querySelector('#motion').onclick=()=>{playing=!playing;document.querySelector('#motion').textContent=playing?'Pause translation probe':'Play translation probe';if(playing)start=performance.now();};
    window.E02P={set(value){playing=false;Object.assign(state,value);render();return results();},results,negativeControls,samples:analysis.samples};
    document.body.dataset.ready='true';
  }
  update(){if(!playing)return;const phase=(performance.now()-start)/2000%8,index=Math.floor(phase),blend=phase-index;
    const a=analysis.samples[index].world,b=analysis.samples[index+1].world;state.point=[a[0]+(b[0]-a[0])*blend,a[1]+(b[1]-a[1])*blend];render();}
}
new Phaser.Game({type:Phaser.WEBGL,width:720,height:405,parent:'stage',backgroundColor:'#20262c',
  render:{antialias:true,roundPixels:false,preserveDrawingBuffer:true},scene:Probe,audio:{noAudio:true}});
