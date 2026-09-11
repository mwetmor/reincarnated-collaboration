export class Chamber {
 constructor(layout,saved=null){this.layout=layout;this.time=0;this.state={door:'locked',crate:'intact',chest:'closed',loot:'absent',rewards:[],picked:[],events:[],navVersion:0};this.pending=null;if(saved)this.restore(saved);}
 emit(type,id){this.state.events.push({time:this.time,type,id});}
 blockers(){const out=this.layout.static_blocks.map(b=>({id:b.id,rect:b.rect}));for(const o of this.layout.objects)if((o.id==='door'&&this.state.door!=='open')||(o.id==='crate'&&this.state.crate==='intact')||o.id==='chest')out.push({id:o.id,rect:o.rect});return out;}
 blocked(p,r){const[a,b,c,d]=this.layout.bounds;if(p[0]<a+r-1e-8||p[0]>c-r+1e-8||p[1]<b+r-1e-8||p[1]>d-r+1e-8)return true;return this.blockers().some(o=>inside(p,expand(o.rect,r)));}
 segmentClear(a,b,r){if(this.blocked(a,r)||this.blocked(b,r))return false;return !this.blockers().some(o=>intersects(a,b,expand(o.rect,r)));}
 move(a,b,r){return this.segmentClear(a,b,r)?[...b]:[...a];}
 action(name,actors=[]){
  if(name==='unlock'&&this.state.door==='locked'){this.state.door='closed';this.emit('unlocked','door');return true;}
  if(name==='open'&&this.state.door==='closed'){this.state.door='opening';this.pending={at:this.time+.5,state:'open'};this.emit('opening','door');return true;}
  if(name==='close'&&this.state.door==='open'){
   const rect=this.layout.objects.find(o=>o.id==='door').rect;if(actors.some(a=>inside(a.point,expand(rect,a.radius)))){this.emit('close-rejected-occupied','door');return false;}
   this.state.door='closing';this.pending={at:this.time+.5,state:'closed'};this.state.navVersion++;this.emit('closing','door');return true;
  }
  if(name==='break'&&this.state.crate==='intact'){this.state.crate='broken';this.state.navVersion++;this.emit('broken','crate');return true;}
  if(name==='chest'&&this.state.chest==='closed'){this.state.chest='open';if(!this.state.rewards.includes('chest:reward:1')){this.state.rewards.push('chest:reward:1');this.state.loot='ground';this.emit('reward','chest:reward:1');}return true;}
  if(name==='pickup'&&this.state.loot==='ground'){this.state.loot='picked';this.state.chest='looted';if(!this.state.picked.includes('chest:reward:1')){this.state.picked.push('chest:reward:1');this.emit('pickup','chest:reward:1');}return true;}
  return false;
 }
 tick(dt){this.time+=dt;if(this.pending&&this.time+1e-8>=this.pending.at){this.state.door=this.pending.state;this.pending=null;this.state.navVersion++;this.emit(this.state.door,'door');}}
 save(){return JSON.stringify({schema:1,state:this.state,time:this.time,pending:this.pending});}
 restore(s){const d=JSON.parse(s);if(d.schema!==1||!d.state||!['locked','closed','opening','open','closing'].includes(d.state.door)||new Set(d.state.rewards).size!==d.state.rewards.length||new Set(d.state.picked).size!==d.state.picked.length)throw Error('Invalid/duplicate state');this.state=structuredClone(d.state);this.time=d.time;this.pending=d.pending;}
 path(start,target,r){
  const step=.1,key=p=>Math.round(p[0]/step)+','+Math.round(p[1]/step),snap=p=>p.map(x=>Math.round(x/step)*step);
  const s=snap(start),goal=snap(target);if(!this.segmentClear(start,s,r)||!this.segmentClear(goal,target,r))return null;
  const open=new Heap(),cost=new Map([[key(s),0]]),from=new Map(),points=new Map([[key(s),s]]),closed=new Set();open.push([dist(s,goal),key(s)]);let count=0;
  while(open.length&&count++<15000){const[,k]=open.pop();if(closed.has(k))continue;closed.add(k);const at=points.get(k);
   if(k===key(goal)){let route=[target],cur=k;while(cur){route.push(points.get(cur));cur=from.get(cur);}route.push(start);return route.reverse().filter((p,i,a)=>i===0||dist(p,a[i-1])>1e-8);}
   for(const dx of[-1,0,1])for(const dy of[-1,0,1]){if(!dx&&!dy)continue;const n=[Math.round((at[0]+dx*step)*10)/10,Math.round((at[1]+dy*step)*10)/10],nk=key(n);if(closed.has(nk)||!this.segmentClear(at,n,r))continue;if(dx&&dy&&(!this.segmentClear(at,[n[0],at[1]],r)||!this.segmentClear(at,[at[0],n[1]],r)))continue;const v=cost.get(k)+dist(at,n);if(v<(cost.get(nk)??Infinity)){cost.set(nk,v);from.set(nk,k);points.set(nk,n);open.push([v+dist(n,goal),nk]);}}
  }return null;
 }
}
export const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
export const expand=(r,n)=>[r[0]-n,r[1]-n,r[2]+n,r[3]+n];
export const inside=(p,r)=>p[0]>r[0]+1e-8&&p[0]<r[2]-1e-8&&p[1]>r[1]+1e-8&&p[1]<r[3]-1e-8;
export function intersects(a,b,r){let low=0,high=1;for(let i=0;i<2;i++){const d=b[i]-a[i];if(Math.abs(d)<1e-12){if(a[i]<=r[i]||a[i]>=r[i+2])return false;}else{let x=(r[i]-a[i])/d,y=(r[i+2]-a[i])/d;if(x>y)[x,y]=[y,x];low=Math.max(low,x);high=Math.min(high,y);if(low>=high-1e-10)return false;}}return high>0&&low<1;}
class Heap{constructor(){this.a=[];}get length(){return this.a.length;}push(v){let i=this.a.push(v)-1;while(i){const p=(i-1)>>1;if(this.a[p][0]<=v[0])break;this.a[i]=this.a[p];i=p;}this.a[i]=v;}pop(){const first=this.a[0],v=this.a.pop();if(this.a.length){let i=0;while(i*2+1<this.a.length){let c=i*2+1;if(c+1<this.a.length&&this.a[c+1][0]<this.a[c][0])c++;if(this.a[c][0]>=v[0])break;this.a[i]=this.a[c];i=c;}this.a[i]=v;}return first;}}
