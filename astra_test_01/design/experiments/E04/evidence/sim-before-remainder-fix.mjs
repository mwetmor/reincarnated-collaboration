// Engine-neutral deterministic JSON boundary. No renderer, browser, camera or asset imports.
import {Chamber,dist} from './chamber.mjs';
function assertJSON(value){if(value===null||typeof value==='string'||typeof value==='boolean')return;if(typeof value==='number'&&Number.isFinite(value))return;if(Array.isArray(value)){value.forEach(assertJSON);return;}if(value&&Object.getPrototypeOf(value)===Object.prototype){Object.values(value).forEach(assertJSON);return;}throw Error('Boundary accepts finite JSON data only');}
export function step(input){assertJSON(input);const {content}=input;if(content.schema_version!==1)throw Error('Unsupported content schema');const restored=input.state??null;const m=new Chamber(content.layout,restored?JSON.stringify(restored.chamber):null);
 const actors=structuredClone(restored?.actors??Object.fromEntries(content.layout.actors.map(a=>[a.id,{point:a.point,radius:a.radius,height:a.height,effects:{}}]))),routes=structuredClone(restored?.routes??{}),outcomes=[];
 for(const command of input.commands??[]){
  if(command.type==='move'){const a=actors[command.entity_id];if(!a)throw Error('Unknown actor');const route=m.path(a.point,command.point,a.radius)??[];if(route.length)route.shift();routes[command.entity_id]=route;outcomes.push({type:'move',accepted:route.length>0});}
  else if(command.type==='authoritative_event'){outcomes.push({type:command.action,accepted:m.action(command.action,Object.values(actors))});}
  else if(command.type==='place_fixture'){if(!content.test_mode)throw Error('Fixture placement unavailable outside test mode');actors[command.entity_id].point=[...command.point];routes[command.entity_id]=[];}
  else if(command.type==='visual_effect'){const e=command.effect;if(!e||!['tint','flash','glow','outline'].includes(e.kind)||typeof e.color!=='string'||!/^#[0-9a-fA-F]{6}$/.test(e.color)||!Number.isFinite(e.ms)||e.ms<0)throw Error('Invalid visual effect declaration');actors[command.entity_id].effects[e.kind]={color:e.color,ms:e.ms,started_at_ms:m.time*1000};}
  else if(command.type==='stop'){routes[command.entity_id]=[];}
  else throw Error('Unknown command '+command.type);
 }
 const dt=(input.dt_ms??0)/1000;if(dt<0||dt>10)throw Error('Invalid step duration');m.tick(dt);
 for(const [id,a]of Object.entries(actors)){
  let budget=dt*content.movement_speed_mps;const route=routes[id]??[];
  while(route.length&&budget>0){const d=dist(a.point,route[0]),to=d<=budget?route[0]:a.point.map((v,i)=>v+(route[0][i]-v)*budget/d),moved=m.move(a.point,to,a.radius);if(dist(a.point,moved)<1e-9&&d>1e-9){route.length=0;break;}a.point=moved;if(d<=budget){budget-=d;route.shift();}else budget=0;}
  routes[id]=route;for(const[k,e]of Object.entries(a.effects))if(e.ms>0&&m.time*1000-e.started_at_ms>=e.ms)delete a.effects[k];
 }
 const state={schema_version:1,chamber:JSON.parse(m.save()),actors,routes};const output={schema_version:1,state,blockers:m.blockers(),outcomes,visual_events:structuredClone(m.state.events)};assertJSON(output);return output;
}
