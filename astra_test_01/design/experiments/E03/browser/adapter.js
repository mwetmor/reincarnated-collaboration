const engine=new URLSearchParams(location.search).get('engine')??'pixi';
const data=await fetch('../scenes.json').then(r=>r.json());
const script=document.createElement('script');script.src=engine==='pixi'?'../../E02/pixi/vendor/pixi-8.20.1.min.js':'../../E02P/vendor/phaser-4.2.1.min.js';document.head.appendChild(script);await new Promise((res,rej)=>{script.onload=res;script.onerror=rej;});
let app,scene,objects=[],index=0;
const textures={};
function draw(i){index=i;objects=[];const frame=data.scenes[i];
 if(engine==='pixi')for(const c of app.stage.removeChildren())c.destroy({children:true});else scene.children.removeAll(true);
 for(const c of frame.commands){let o;
  if(c.type==='image'){
   if(engine==='pixi'){o=new PIXI.Sprite(textures[c.asset]);o.position.set(c.x,c.y);o.scale.set(c.scale);app.stage.addChild(o);}
   else o=scene.add.image(c.x,c.y,c.asset).setOrigin(0,0).setScale(c.scale);
   const mask=data.assets[c.asset].mask;
   if(mask){
    if(engine==='pixi'){const m=new PIXI.Graphics().poly(mask.flat()).fill(0xffffff);m.position.set(c.x,c.y);m.scale.set(c.scale);app.stage.addChild(m);o.mask=m;}
    else{const m=scene.make.graphics({x:c.x,y:c.y});m.setScale(c.scale);m.fillStyle(0xffffff).beginPath().moveTo(...mask[0]);for(const pt of mask.slice(1))m.lineTo(...pt);m.closePath().fillPath();o.enableFilters().filters.external.addMask(m,false,scene.cameras.main);}
   }
   objects.push({id:c.id,node:o,expected:c});
  }else if(c.type==='rect'){
   if(engine==='pixi'){o=new PIXI.Graphics().rect(c.x,c.y,c.w,c.h).fill(c.color);app.stage.addChild(o);}else scene.add.graphics().fillStyle(c.color).fillRect(c.x,c.y,c.w,c.h);
  }else if(c.type==='line'){
   if(engine==='pixi'){o=new PIXI.Graphics().moveTo(...c.points[0]);for(const pt of c.points.slice(1))o.lineTo(...pt);o.stroke({color:c.color,width:c.width});app.stage.addChild(o);}
   else{const g=scene.add.graphics().lineStyle(c.width,c.color).beginPath().moveTo(...c.points[0]);for(const pt of c.points.slice(1))g.lineTo(...pt);g.strokePath();}
  }
 }
 if(engine==='pixi')app.render();document.querySelector('#scene').value=String(i);document.querySelector('#status').textContent=frame.label;
}
function results(){const gl=engine==='pixi'?app.renderer.gl:scene.game.renderer.gl,ext=gl.getExtension('WEBGL_debug_renderer_info');
 return{engine,version:engine==='pixi'?PIXI.VERSION:Phaser.VERSION,scene:data.scenes[index].id,backend:gl.getParameter(gl.VERSION),renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),images:objects.map(o=>({id:o.id,x:o.node.x,y:o.node.y,scale:engine==='pixi'?o.node.scale.x:o.node.scaleX})),order:objects.map(o=>o.id)};
}
function ready(){const s=document.querySelector('#scene');data.scenes.forEach((f,i)=>s.add(new Option(f.label,i)));s.onchange=()=>draw(Number(s.value));document.querySelector('#next').onclick=()=>draw((index+1)%data.scenes.length);document.querySelector('#title').textContent=engine+' · painted chamber · projection C';window.E03={set:draw,results,scenes:data.scenes};draw(0);document.body.dataset.ready='true';}
if(engine==='pixi'){
 for(const [id,a]of Object.entries(data.assets))textures[id]=await PIXI.Assets.load('../'+a.path);
 app=new PIXI.Application();await app.init({width:960,height:640,resolution:1,preference:'webgl',antialias:true,background:0x1c2125,autoStart:false,preserveDrawingBuffer:true});document.querySelector('#stage').appendChild(app.canvas);ready();
}else{
 class Probe extends Phaser.Scene{preload(){for(const [id,a]of Object.entries(data.assets))this.load.image(id,'../'+a.path);}create(){scene=this;ready();}}
 new Phaser.Game({type:Phaser.WEBGL,width:960,height:640,parent:'stage',scene:Probe,render:{antialias:true,roundPixels:false,preserveDrawingBuffer:true},audio:{noAudio:true}});
}
