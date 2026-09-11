// View adapter only. Light-space policy and world geometry arrive as neutral data.
export function createSceneShadow(PIXI, app, policy, profileId) {
  const profile = policy.profiles[profileId];
  if (!profile) throw Error('Unregistered shadow profile');
  const limit = app.renderer.gl.getParameter(app.renderer.gl.MAX_TEXTURE_SIZE);
  if (Math.max(profile.map.width, profile.map.height) > limit) throw Error('Shadow texture exceeds measured device limit');
  const texture = PIXI.RenderTexture.create({ width: profile.map.width, height: profile.map.height, resolution: 1, antialias: false });
  texture.source.style.scaleMode = 'nearest';
  const target = app.renderer.renderTarget.getRenderTarget(texture);
  target.ensureDepthStencilTexture();
  const settings = { enabled: true, diagnostic: false, omit: '', staleOffset: [0, 0], reverse: false };
  const vec = a => 'vec3(' + a.map(x => x.toFixed(10)).join(',') + ')';
  const scalar = x => x.toFixed(10);
  const axes = profile.basis, bounds = profile.bounds;
  const span = name => bounds[name][1] - bounds[name][0];
  const positionGLSL = `vec3 shadowCoordinates(vec3 p){return vec3((dot(p,${vec(axes.right)})-${scalar(bounds.right[0])})/${scalar(span('right'))},(dot(p,${vec(axes.up)})-${scalar(bounds.up[0])})/${scalar(span('up'))},(${scalar(bounds.toward_light[1])}-dot(p,${vec(axes.toward_light)}))/${scalar(span('toward_light'))});}`;
  const glsl = `uniform sampler2D uSceneShadow;uniform float uSceneShadowEnabled;uniform float uSceneDiagnostic;${positionGLSL}
float sceneShadow(vec3 world,vec3 normal){if(uSceneShadowEnabled<0.5)return 0.0;vec3 q=shadowCoordinates(world+normal*${scalar(profile.normal_offset_m)});if(q.x<0.0||q.y<0.0||q.x>1.0||q.y>1.0||q.z<0.0||q.z>1.0)return 0.0;vec3 packed=texture2D(uSceneShadow,q.xy).rgb;float stored=dot(packed,vec3(1.0,1.0/255.0,1.0/65025.0));return q.z-stored>${scalar(profile.compare_bias_m/span('toward_light'))}?1.0:0.0;}`;
  const fragment = 'precision highp float;varying float vDepth;void main(){vec3 p=fract(vDepth*vec3(1.0,255.0,65025.0));p.xy-=p.yz/255.0;gl_FragColor=vec4(p,1.0);}';
  const sceneVertex = `attribute vec3 aWorld;varying float vDepth;${positionGLSL}void main(){vec3 q=shadowCoordinates(aWorld);gl_Position=vec4(q*2.0-1.0,1.0);vDepth=q.z;}`;
  const dot = (a,b) => a.reduce((s,x,i)=>s+x*b[i],0);
  function covered(p) { return Object.entries(axes).every(([name, axis]) => {const q=dot(p,axis);return q>bounds[name][0]&&q<bounds[name][1];}); }
  function state() { const value = new PIXI.State(); value.depthTest=true;value.depthMask=true;value.blend=false;return value; }
  let last = null;
  function update(pilotMeshes, objects) {
    const source = pilotMeshes[0].shader.resources.params.uniforms, matrixCount = source.uBones.length/16;
    const envelope=policy.caster_envelope,scale=source.uBodyScale,root=[source.uWorldPosition[0]+settings.staleOffset[0],-source.uWorldPosition[1]+settings.staleOffset[1],source.uWorldPosition[2]],r=envelope.radius_m*scale;
    for(const x of[root[0]-r,root[0]+r])for(const y of[root[1]-r,root[1]+r])for(const z of[root[2]+envelope.z_min_m*scale,root[2]+envelope.z_max_m*scale])if(!covered([x,y,z]))throw Error('Pilot outside shared shadow domain');
    const positions=[],indices=[];
    for(const object of objects)for(const face of object.faces){for(const p of face)if(!covered(p))throw Error('Scene geometry outside shared shadow domain: '+object.id);if(settings.omit==='scene')continue;const start=positions.length/3;positions.push(...face.flat());indices.push(...[0,1,2,0,2,3].map(i=>i+start));}
    const container=new PIXI.Container(),meshes=[];
    if(indices.length){const geometry=new PIXI.Geometry({attributes:{aWorld:{buffer:new Float32Array(positions),format:'float32x3'}},indexBuffer:new Uint32Array(indices)}),mesh=new PIXI.Mesh({geometry,shader:PIXI.Shader.from({gl:{vertex:sceneVertex,fragment}}),state:state()});mesh.ownedShadowGeometry=true;meshes.push(mesh);}
    const actorVertex=`attribute vec3 aPosition;attribute vec4 aJoints;attribute vec4 aWeights;uniform mat4 uBones[${matrixCount}];uniform float uHeading;uniform vec3 uWorldPosition;uniform float uBodyScale;varying float vDepth;${positionGLSL}
void main(){mat4 skin=uBones[int(aJoints.x)]*aWeights.x+uBones[int(aJoints.y)]*aWeights.y+uBones[int(aJoints.z)]*aWeights.z+uBones[int(aJoints.w)]*aWeights.w;vec3 p=(skin*vec4(aPosition,1.0)).xyz;float c=cos(uHeading),s=sin(uHeading);p=vec3(c*p.x-s*p.y,s*p.x+c*p.y,p.z)*uBodyScale+uWorldPosition;p.y=-p.y;vec3 q=shadowCoordinates(p);gl_Position=vec4(q*2.0-1.0,1.0);vDepth=q.z;}`;
    if(settings.omit!=='pilot')for(const sourceMesh of pilotMeshes){const v=sourceMesh.shader.resources.params.uniforms,at=v.uWorldPosition,params=new PIXI.UniformGroup({uBones:{value:v.uBones,type:'mat4x4<f32>',size:matrixCount},uHeading:{value:v.uHeading,type:'f32'},uWorldPosition:{value:new Float32Array([at[0]+settings.staleOffset[0],at[1]-settings.staleOffset[1],at[2]]),type:'vec3<f32>'},uBodyScale:{value:v.uBodyScale,type:'f32'}});meshes.push(new PIXI.Mesh({geometry:sourceMesh.geometry,shader:PIXI.Shader.from({gl:{vertex:actorVertex,fragment},resources:{params}}),state:state()}));}
    if(settings.reverse)meshes.reverse();for(const mesh of meshes)container.addChild(mesh);
    app.renderer.render({container,target:texture,clear:true,clearColor:[1,1,1,1]});
    last={profile:profileId,dimensions:[profile.map.width,profile.map.height],device_max_texture:limit,draws:meshes.length,scene_triangles:indices.length/3,pilot_palette_matrices:matrixCount,root,settings:structuredClone(settings)};
    for(const mesh of container.removeChildren()){if(mesh.ownedShadowGeometry)mesh.geometry.destroy(true);mesh.shader.destroy();mesh.destroy();}container.destroy();
  }
  function probe(points){const q=app.renderer.extract.pixels({target:texture});return{width:q.width,height:q.height,records:points.map(p=>{const x=p.pixel[0],y=p.pixel[1];if(x<0||x>=q.width||y<0||y>=q.height)throw Error('Shadow probe outside map');const rgba=[...q.pixels.slice((y*q.width+x)*4,(y*q.width+x)*4+4)];return{...p,rgba,decoded:rgba[0]/255+rgba[1]/65025+rgba[2]/16581375};})};}
  return {texture,profile,settings,glsl,update,probe,snapshot:()=>last};
}
