import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createState,step,validate} from './sim/index.mjs';
const asset=JSON.parse(fs.readFileSync(new URL('./character.asset.json',import.meta.url))),checks={};
for(const heading of [0,45,90,135,180,225,270,315])for(const direction of ['left','right']){
 const initial=createState([2.5,-1.25],heading),before=JSON.stringify(initial);let s=step(initial,{type:'turn',direction},asset);
 assert.equal(JSON.stringify(initial),before);assert.equal(s.heading_deg,heading);assert.throws(()=>step(s,{type:'turn',direction},asset));
 s=step(s,{type:'advance',dt:.59},asset);assert.equal(s.action,'turn_'+direction);assert.equal(s.events.length,0);assert.equal(s.heading_deg,heading);
 const restored=JSON.parse(JSON.stringify(s));assert.deepEqual(validate(restored),s);s=step(s,{type:'advance',dt:.01},asset);assert.equal(s.action,'idle');assert.equal(s.events.length,1);assert.equal(s.heading_deg,(heading+(direction==='left'?45:315))%360);assert.deepEqual(s.root,initial.root);
 assert.deepEqual(step(restored,{type:'advance',dt:.01},asset),s);const id=s.events[0].id;s=step(s,{type:'advance',dt:1},asset);assert.equal(s.events.length,0);s=step(s,{type:'turn',direction:direction==='left'?'right':'left'},asset);s=step(s,{type:'advance',dt:2},asset);assert.equal(s.heading_deg,heading);assert.equal(s.events.length,1);assert.notEqual(s.events[0].id,id);checks[heading+'_'+direction]=true;
}
for(const dt of [-1,NaN,Infinity,11])assert.throws(()=>step(createState(),{type:'advance',dt},asset));checks.bad_dt=true;
assert.throws(()=>step(createState(),{type:'turn',direction:'up'},asset));checks.bad_direction=true;
for(const change of [{root:[NaN,0]},{heading_deg:360},{elapsed_s:.2},{action:'walk'},{turn_id:-1}])assert.throws(()=>validate({...createState(),...change}));checks.bad_state=true;
const bad=structuredClone(asset);bad.clips.turn_left.heading_delta_deg=90;assert.throws(()=>step(createState(),{type:'turn',direction:'left'},bad));checks.bad_content=true;
assert.throws(()=>validate({...createState(),events:[()=>0]}));checks.non_json_event=true;let forged=step(createState(),{type:'turn',direction:'left'},asset);forged.duration_s=.3;assert.throws(()=>step(forged,{type:'advance',dt:.1},asset));checks.forged_duration=true;
const source=fs.readFileSync(new URL('./sim/index.mjs',import.meta.url),'utf8');assert.ok(!/\bimport\b|PIXI|document\.|window\./.test(source));checks.no_render_imports=true;
fs.writeFileSync(new URL('./evidence/sim-validation.json',import.meta.url),JSON.stringify({checks},null,2)+'\n');console.log(Object.keys(checks).length,'checks PASS');
