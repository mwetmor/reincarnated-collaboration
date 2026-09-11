// Diagnostic presentation only; no game state or rules.
const app=new PIXI.Application();await app.init({width:900,height:600,resolution:1,preference:'webgl',antialias:true,autoStart:false,preserveDrawingBuffer:true});document.querySelector('#stage').appendChild(app.canvas);
const backgrounds=[0x141b22,0xe6dfd1,0x1451a3];
for(const [row,id]of ['mage','monster','npc'].entries()){
 const url=new URL('manifests/'+id+'.asset.json',location.href),m=await fetch(url).then(r=>r.json()),texture=await PIXI.Assets.load(new URL(m.frames[0].source_path,new URL(m.path_base,url)).href),s=150/m.registration.source_axis_height;
 for(let col=0;col<3;col++){
  app.stage.addChild(new PIXI.Graphics().rect(col*300,row*200,300,200).fill(backgrounds[col]));
  const c=new PIXI.Container();c.position.set(col*300+150-m.frames[0].pivot[0]*s,row*200+174-m.frames[0].pivot[1]*s);c.scale.set(s);
  const sprite=new PIXI.Sprite(texture),mask=new PIXI.Graphics().poly(m.silhouette_polygon.flat()).fill(0xffffff);c.addChild(sprite,mask);sprite.mask=mask;app.stage.addChild(c);
 }
}
app.render();document.body.dataset.ready='true';
