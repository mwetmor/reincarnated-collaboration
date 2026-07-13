// Mobile: does hover work mid-plane? Walk cursor across x to map where popover appears + its clamp behavior.
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const URL='https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
const dotJson=JSON.parse(readFileSync('/tmp/pdp.json','utf8')); const VB=dotJson.viewBox; const dots=dotJson.dots;
function popScan(){const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>70&&b.width<700&&b.height>20&&b.height<680&&(el.textContent||'').trim().length>6&&cs.visibility!=='hidden'&&cs.opacity!=='0';}).map(el=>{const b=el.getBoundingClientRect();const mono=[...el.querySelectorAll('*')].some(d=>/mono/i.test(getComputedStyle(d).fontFamily));return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,70),x:Math.round(b.left),right:Math.round(b.right),w:Math.round(b.width),h:Math.round(b.height),y:Math.round(b.top),hasMono:mono};});return cards.filter(c=>c.hasMono).sort((a,b)=>(a.w*a.h)-(b.w*b.h));}

const browser=await chromium.launch();
const ctx=await browser.newContext({viewport:{width:375,height:812},deviceScaleFactor:2});
const page=await ctx.newPage();
const base=URL.split('#')[0];
await page.goto(base,{waitUntil:'domcontentloaded'});
await page.evaluate(()=>{window.location.hash='#/atlas';});
await page.waitForLoadState('networkidle').catch(()=>{});
await page.waitForTimeout(3000);
await page.evaluate(()=>document.querySelector('svg[viewBox]').scrollIntoView({block:'center'}));
await page.waitForTimeout(400);
const svgBox=await page.evaluate(()=>{const r=document.querySelector('svg[viewBox]').getBoundingClientRect();return{x:r.left,y:r.top,w:r.width,h:r.height};});
const sx=svgBox.w/VB.w, sy=svgBox.h/VB.h;
console.log('svg bbox x',Math.round(svgBox.x),'w',Math.round(svgBox.w),'-> plane spans x',Math.round(svgBox.x),'..',Math.round(svgBox.x+svgBox.w));
// use a fixed Y inside the FREE-MOVE row band; walk X across viewport
const yVB=210; const Y=svgBox.y+yVB*sy;
console.log('walk Y(screen)=',Math.round(Y));
for(const X of [80,140,200,260,320,360]){
  await page.mouse.move(2,2); await page.waitForTimeout(150);
  await page.mouse.move(X,Y); await page.waitForTimeout(600);
  const pops=popScan?await page.evaluate(popScan):[]; const p=pops[0];
  // also read the injected ring so we know a dot resolved
  const ring=await page.evaluate(()=>{const c=document.querySelector('svg[viewBox] circle');return c?{cx:+c.getAttribute('cx'),cy:+c.getAttribute('cy'),stroke:c.getAttribute('stroke')}:null;});
  console.log(`X=${X}: ring=${ring?`(${ring.cx.toFixed(0)},${ring.cy.toFixed(0)})`:'NONE'} popover=${p?`x${p.x}..${p.right} w${p.w} onScreen=${p.x>=-1&&p.right<=376}`:'NONE'}`);
}
// screenshot at X=320 (near right viewport edge, popover should want to overflow right)
await page.mouse.move(2,2); await page.waitForTimeout(150);
await page.mouse.move(330,Y); await page.waitForTimeout(700);
await page.screenshot({path:`${OUT}/mobile-walk-x330.png`});
await ctx.close(); await browser.close(); console.log('DONE walk');
