import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {Chamber,dist} from './sim/chamber.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));const layout=JSON.parse(fs.readFileSync(path.join(here,'../E03/inputs/chamber-layout.json')));const checks={},routes=[];const assert=(id,value)=>checks[id]=Boolean(value);
const start=[0,0];
for(const radius of[.35,.65]){
 const m=new Chamber(layout);const k='radius-'+radius;
 assert(k+':locked-forbidden',m.path(start,[3.3,0],radius)===null);
 assert(k+':locked-fast-sweep',dist(m.move([1,0],[3.3,0],radius),[1,0])===0);
 assert(k+':open-locked-rejected',m.action('open')===false);
 assert(k+':unlock-does-not-open',m.action('unlock')&&m.state.door==='closed'&&m.path(start,[3.3,0],radius)===null);
 m.action('open');m.tick(.49);assert(k+':opening-blocks',m.path(start,[3.3,0],radius)===null);m.tick(.01);
 assert(k+':open-transition',m.state.door==='open');
 const targets=[[-5+radius+.05,0],[5-radius-.05,0],...[...layout.objects].flatMap(o=>o.approaches),[-4.1,-3.1],[4,-3.1],[4,3.1],[-4.1,3.1]];
 for(let i=0;i<targets.length;i++){const route=m.path(start,targets[i],radius);assert(k+':reachable-'+i,route!==null);assert(k+':swept-route-'+i,route&&route.every((pt,j)=>j===0||m.segmentClear(route[j-1],pt,radius)));if(route)routes.push({id:k+'-target-'+i,radius,points:route});}
 for(const direction of[1,-1]){
  const perimeter=[[-4.1,-3.1],[4,-3.1],[4,3.1],[-4.1,3.1]];if(direction<0)perimeter.reverse();let current=start;let valid=true;
  for(const to of[...perimeter,perimeter[0]]){const route=m.path(current,to,radius);valid=valid&&route!==null;if(route)valid=valid&&route.every((pt,j)=>j===0||m.segmentClear(route[j-1],pt,radius));current=to;}assert(k+':perimeter-'+direction,valid);
 }
 const v=m.state.navVersion;assert(k+':occupied-close-rejected',!m.action('close',[{point:[2.15,0],radius}])&&m.state.door==='open'&&m.state.navVersion===v);
 assert(k+':close-start-blocks',m.action('close')&&m.path(start,[3.3,0],radius)===null);m.tick(.5);assert(k+':close-and-replan',m.state.door==='closed'&&m.state.navVersion>v);
 // Independent planted tunnelling/corner-cut segment through the pillar footprint.
 assert(k+':corner-cut-rejected',!m.segmentClear([-3.5,-2.8],[-.5,-.2],radius));
 const before=m.path([-1.3,2.8],[1.3,2.8],radius);m.action('break');const after=m.path([-1.3,2.8],[1.3,2.8],radius);const length=route=>route.slice(1).reduce((n,p,i)=>n+dist(route[i],p),0);
 assert(k+':crate-route-shorter',before&&after&&length(after)<length(before));
 assert(k+':wall-owner-retained',m.blockers().some(b=>b.id==='partition-north')&&!m.blockers().some(b=>b.id==='crate'));
 m.action('chest');m.action('chest');assert(k+':one-reward',m.state.rewards.length===1&&m.state.events.filter(e=>e.type==='reward').length===1);
 m.action('pickup');m.action('pickup');assert(k+':one-pickup',m.state.picked.length===1&&m.state.events.filter(e=>e.type==='pickup').length===1);
 const saved=m.save(),loaded=new Chamber(layout,saved);assert(k+':reload-exact',loaded.save()===saved);loaded.action('chest');loaded.action('pickup');assert(k+':reentry-no-duplicate',loaded.state.rewards.length===1&&loaded.state.picked.length===1);
 const bad=JSON.parse(saved);bad.state.rewards.push('chest:reward:1');let rejected=false;try{new Chamber(layout,JSON.stringify(bad));}catch{rejected=true;}assert(k+':bad-duplicate-rejected',rejected);
 const overlap=structuredClone(layout);overlap.static_blocks.push({id:'overlap-wall',rect:layout.objects.find(o=>o.id==='crate').rect});const owned=new Chamber(overlap);owned.action('break');assert(k+':overlapping-owner-survives',owned.blocked([0,2.8],radius));
 const stale=new Chamber(layout);stale.action('unlock');stale.action('open');stale.tick(.5);const healthy=stale.path(start,[3.3,0],radius)!==null;const original=stale.blockers.bind(stale);stale.blockers=()=>[...original(),layout.objects.find(o=>o.id==='door')];assert(k+':stale-door-control-detected',healthy&&stale.path(start,[3.3,0],radius)===null);
}
const out={experiment:'E04',checks,passed:Object.values(checks).filter(Boolean).length,total:Object.keys(checks).length,routes,scope:'Logical navigation, independent swept movement, ownership/state/reward assertions; not painted art or gait acceptance'};fs.writeFileSync(path.join(here,'evidence/model-validation.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({passed:out.passed,total:out.total,failed:Object.entries(checks).filter(x=>!x[1]).map(x=>x[0])}));if(out.passed!==out.total)process.exitCode=1;
