// View-only visibility masks. Geometry and per-entity style are supplied as data.
export function createVisibility(PIXI,app,policy){
 const settings={enabled:policy.enabled,variant:policy.selected,diagnostic:false,omitWorld:false,always:false};
 const {width,height}=app.screen,resolution=app.renderer.resolution;
 const targets=[0,1].map(()=>{const t=PIXI.RenderTexture.create({width,height,resolution,antialias:true});t.source.style.scaleMode='nearest';return {texture:t,target:new PIXI.RenderTarget({colorTextures:[t],depth:true,stencil:true})};});
 const state=()=>{const s=new PIXI.State();s.depthTest=true;s.depthMask=true;s.blend=false;return s;};
 const overlayGeometry=new PIXI.Geometry({attributes:{aPosition:{buffer:new Float32Array([-1,-1,1,-1,1,1,-1,1]),format:'float32x2'}},indexBuffer:new Uint32Array([0,1,2,0,2,3])});
 const vertex='attribute vec2 aPosition;varying vec2 vUV;void main(){gl_Position=vec4(aPosition,0.0,1.0);vUV=aPosition*.5+.5;}';
 const fragment=`precision highp float;varying vec2 vUV;uniform sampler2D uFull;uniform sampler2D uVisible;uniform vec3 uColor;uniform float uFill;uniform float uOutline;uniform float uWidth;uniform float uDiagnostic;uniform float uAlways;
 float hidden(vec2 uv){float full=texture2D(uFull,uv).r,visible=texture2D(uVisible,uv).r;return uAlways>0.5?full:max(0.0,full-visible);}
 void main(){float h=hidden(vUV),visible=texture2D(uVisible,vUV).r;if(uDiagnostic>0.5){gl_FragColor=vec4(h,visible,0.0,1.0);return;}
 vec2 stepUV=vec2(uWidth/${width.toFixed(1)},uWidth/${height.toFixed(1)});float surround=0.0;
 for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++)surround=max(surround,hidden(vUV+vec2(float(x),float(y))*stepUV));
 float ring=max(0.0,surround-h),a=h*uFill+ring*uOutline;gl_FragColor=vec4(uColor*a,a);}`;
 const params=new PIXI.UniformGroup({uColor:{value:new Float32Array([1,1,1]),type:'vec3<f32>'},uFill:{value:0,type:'f32'},uOutline:{value:0,type:'f32'},uWidth:{value:0,type:'f32'},uDiagnostic:{value:0,type:'f32'},uAlways:{value:0,type:'f32'}});
 const shader=PIXI.Shader.from({gl:{vertex,fragment},resources:{params,uFull:targets[0].texture.source,uVisible:targets[1].texture.source}});
 let last=null;
 function update(meshes){
  const eligible=meshes.filter(m=>m.geometry&&!m.isVisibilityOverlay),pilots=eligible.filter(m=>m.isPaintedPilot),world=eligible.filter(m=>!m.isPaintedPilot);
  for(let pass=0;pass<2;pass++){
   const container=new PIXI.Container();
   for(const source of (pass===0||settings.omitWorld?pilots:[...world,...pilots])){
    const pilot=!!source.isPaintedPilot,original=source.shader.glProgram.vertex,version3=original.includes('#version 300 es'),fragment=(version3?'#version 300 es\nprecision highp float;out vec4 maskColor;':'precision highp float;')+'void main(){'+(version3?'maskColor':'gl_FragColor')+'=vec4('+ (pilot?'1.0':'0.0') +','+(pilot?'1.0':'0.0')+','+(pilot?'1.0':'0.0')+',1.0);}';
    const clone=new PIXI.Mesh({geometry:source.geometry,shader:PIXI.Shader.from({gl:{vertex:original,fragment},resources:source.shader.resources}),state:state()});container.addChild(clone);
   }
   app.renderer.render({container,target:targets[pass].target,clear:true,clearColor:[0,0,0,0]});
   for(const m of container.removeChildren()){m.shader.destroy();m.destroy();}container.destroy();
  }
  last={pilot_meshes:pilots.length,world_meshes:world.length,dimensions:[width*resolution,height*resolution],settings:structuredClone(settings),allocation_rgba_depth_bytes_arithmetic:width*height*resolution*resolution*16};
 }
 function overlay(){const p=policy.variants[settings.variant];if(!p)throw Error('Unknown visibility variant');Object.assign(params.uniforms,{uColor:new Float32Array(p.color_srgb),uFill:p.fill_opacity,uOutline:p.outline_opacity,uWidth:p.outline_logical_px,uDiagnostic:settings.diagnostic?1:0,uAlways:settings.always?1:0});params.update();const s=new PIXI.State();s.blend=true;s.depthTest=false;s.depthMask=false;const m=new PIXI.Mesh({geometry:overlayGeometry,shader,state:s});m.isVisibilityOverlay=true;return m;}
 return{settings,update,overlay,snapshot:()=>last};
}
