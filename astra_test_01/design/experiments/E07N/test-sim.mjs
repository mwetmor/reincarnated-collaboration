import fs from 'node:fs';import assert from 'node:assert/strict';import {createState,step,obstacles,plan,routeValid} from './sim/index.mjs';
const content=JSON.parse(fs.readFileSync(new URL('../E07D/inputs/scene.json',import.meta.url))),checks={},records=[];
function check(name,fn){try{fn();checks[name]=true;}catch(e){checks[name]=false;records.push({name,error:e.stack});}}
for(const faction of ['F01','F02']) for(const id of ['mage','monster']){
 let s=createState(content);const k=faction+'_'+id, apply=c=>(s=step(s,c,content,faction)),accepted=()=>s.outcomes.at(-1).accepted,move=p=>apply({type:'move',id,point:p}),action=a=>apply({type:'internal_door',actor_id:id,action:a}),tick=dt=>apply({type:'tick',dt});
 apply({type:'fixture_place',id,point:[1.3,0]});
 check(k+'_locked_blocks',()=>{action('open');assert(!accepted());move([3.3,0]);assert(!accepted());});
 check(k+'_closed_blocks',()=>{action('unlock');assert(accepted());assert.equal(s.chamber.state.door,'closed');move([3.3,0]);assert(!accepted());});
 check(k+'_closed_no_path',()=>assert.equal(plan(s,content,faction,id,[3.3,0]).points,null));
 check(k+'_opening_blocks',()=>{action('open');assert(accepted());tick(.25);assert.equal(s.chamber.state.door,'opening');move([3.3,0]);assert(!accepted());});
 check(k+'_mid_transition_restore',()=>{const saved=JSON.stringify(s);const restored=createState(content,JSON.parse(saved));assert.equal(JSON.stringify(restored),saved);assert.deepEqual(step(s,{type:'tick',dt:.25},content,faction),step(restored,{type:'tick',dt:.25},content,faction));});
 tick(.25);const route=plan(s,content,faction,id,[3.3,0]);
 check(k+'_open_path_and_traverse',()=>{assert.equal(s.chamber.state.door,'open');assert(route.points?.length);assert(routeValid(route,s,content,faction));move([3.3,0]);assert(accepted());move([2.15,0]);assert(accepted());});
 check(k+'_occupied_close',()=>{action('close');assert(!accepted());assert.equal(s.chamber.state.door,'open');assert.equal(s.chamber.pending,null);});
 move([1.3,0]);const nav=s.chamber.state.navVersion;
 check(k+'_closing_blocks_and_invalidates',()=>{action('close');assert(accepted());assert.equal(s.chamber.state.door,'closing');assert.equal(s.chamber.state.navVersion,nav+1);assert(!routeValid(route,s,content,faction));move([3.3,0]);assert(!accepted());assert.equal(plan(s,content,faction,id,[3.3,0]).points,null);});
 check(k+'_closing_restores_and_commits',()=>{tick(.2);const t=createState(content,JSON.parse(JSON.stringify(s)));assert.deepEqual(step(s,{type:'tick',dt:.3},content,faction),step(t,{type:'tick',dt:.3},content,faction));tick(.3);assert.equal(s.chamber.state.door,'closed');assert.equal(s.chamber.pending,null);});
 check(k+'_reopen_replan',()=>{action('open');tick(.5);assert(plan(s,content,faction,id,[3.3,0]).points?.length);assert(!routeValid(route,s,content,faction));});
 check(k+'_bad_omitted_collision_detected',()=>{action('close');tick(.5);const b=step(s,{type:'move',id,point:[3.3,0]},content,faction,true);assert(b.outcomes.at(-1).accepted);assert(!step(s,{type:'move',id,point:[3.3,0]},content,faction).outcomes.at(-1).accepted);});
 records.push({name:k,state:s});
}
const s=createState(content),before=JSON.stringify(s),c=JSON.stringify(content);
check('immutable_boundary',()=>{step(s,{type:'tick',dt:.2},content,'F01');assert.equal(JSON.stringify(s),before);assert.equal(JSON.stringify(content),c);});
check('out_of_range_rejected',()=>assert.equal(step(s,{type:'internal_door',actor_id:'mage',action:'unlock'},content,'F01').outcomes.at(-1).reason,'out-of-range'));
check('invalid_dt',()=>{for(const dt of[-1,Infinity,NaN,'0.5'])assert.throws(()=>step(s,{type:'tick',dt},content,'F01'));});
check('invalid_saved_transitions',()=>{for(const patch of [{time:-1},{pending:{at:1,state:'open'}},{time:NaN},{state:{...s.chamber.state,door:'opening'},pending:null},{state:{...s.chamber.state,door:'invalid'}}]){const v=structuredClone(s);Object.assign(v.chamber,patch);assert.throws(()=>createState(content,v));}});
check('no_rendering_imports',()=>assert(!/from\s*['"][^'"]*(?:pixi|adapter|renderer)/i.test(fs.readFileSync(new URL('./sim/index.mjs',import.meta.url),'utf8'))));
check('invalid_props_events_faction',()=>{for(const [key,value] of [['crate','missing'],['chest','invalid'],['loot','invalid'],['events',{}],['rewards','abc']]){const v=structuredClone(s);v.chamber.state[key]=value;assert.throws(()=>createState(content,v));}assert.throws(()=>step(s,{type:'tick',dt:.1},content,'unknown'));});
check('prop_rules_survive_door_wrapper',()=>{let v=step(s,{type:'fixture_place',id:'mage',point:[-3.5,.65]},content,'F01');for(const action of ['chest','chest','pickup','pickup'])v=step(v,{type:'prop_action',actor_id:'mage',action},content,'F01');assert.equal(v.chamber.state.rewards.length,1);assert.equal(v.chamber.state.picked.length,1);assert.equal(v.chamber.state.door,'locked');assert(obstacles(v,content,'F01').some(o=>o.id==='internal-leaf'));});
const output={checks,records,pass:Object.values(checks).every(Boolean)};fs.writeFileSync(new URL('./evidence/sim-validation.json',import.meta.url),JSON.stringify(output,null,2));console.log({pass:output.pass,checks:Object.keys(checks).length,failures:Object.entries(checks).filter(x=>!x[1]),errors:records.filter(x=>x.error)});if(!output.pass)process.exitCode=1;
