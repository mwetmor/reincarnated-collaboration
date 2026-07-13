// Focused mobile 375 clamp test — hover left-edge and right-edge dots, capture each immediately.
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json','utf8')); const VB=dotJson.viewBox; const dots=dotJson.dots;

function popScan(){
  const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>70&&b.width<700&&b.height>20&&b.height<680&&(el.textContent||'').trim().length>6&&cs.visibility!=='hidden'&&cs.opacity!=='0';}).map(el=>{const b=el.getBoundingClientRect();const mono=[...el.querySelectorAll('*')].some(d=>/mono/i.test(getComputedStyle(d).fontFamily));return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,120),x:Math.round(b.left),y:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height),right:Math.round(b.right),hasMono:mono};});
  return cards.filter(c=>c.hasMono).sort((a,b)=>(a.w*a.h)-(b.w*b.h));
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport:{width:375,height:812}, deviceScaleFactor:2 });
const page = await ctx.newPage();
const base = URL.split('#')[0];
await page.goto(base,{waitUntil:'domcontentloaded'});
await page.evaluate(()=>{window.location.hash='#/atlas';});
await page.waitForLoadState('networkidle').catch(()=>{});
await page.waitForTimeout(3000);
await page.evaluate(()=>document.querySelector('svg[viewBox]').scrollIntoView({block:'center'}));
await page.waitForTimeout(400);
const svgBox = await page.evaluate(()=>{const r=document.querySelector('svg[viewBox]').getBoundingClientRect();return{x:r.left,y:r.top,w:r.width,h:r.height};});
const sx=svgBox.w/VB.w, sy=svgBox.h/VB.h;
console.log('svg bbox:', JSON.stringify({x:Math.round(svgBox.x),y:Math.round(svgBox.y),w:Math.round(svgBox.w),h:Math.round(svgBox.h)}),'| viewport 375');
const vis = dots.map(d=>({d,X:svgBox.x+d.px*sx,Y:svgBox.y+d.py*sy})).filter(o=>o.X>3&&o.X<372&&o.Y>3&&o.Y<805);

async function test(label, o) {
  await page.mouse.move(2,2); await page.waitForTimeout(200); // reset
  await page.mouse.move(o.X, o.Y); await page.waitForTimeout(700);
  const pops = await page.evaluate(popScan);
  const p = pops[0] || null;
  const verdict = p ? { onScreen: p.x>=-1 && p.right<=376, x:p.x, right:p.right, w:p.w, overflowR:Math.max(0,p.right-375), overflowL:Math.max(0,-p.x) } : {popover:'NONE'};
  console.log(`\n[${label}] dot="${o.d.display_name}" screenX=${Math.round(o.X)} screenY=${Math.round(o.Y)}`);
  console.log('  popover:', JSON.stringify(p));
  console.log('  clamp verdict:', JSON.stringify(verdict));
  await page.screenshot({ path: `${OUT}/mobile-clamp-${label}.png` });
  return { p, verdict };
}

// Rightmost dot (want popover to appear near right edge)
vis.sort((a,b)=>b.X-a.X);
await test('right-edge', vis[0]);
await test('right-edge-2', vis[3] || vis[0]);
// Leftmost
vis.sort((a,b)=>a.X-b.X);
await test('left-edge', vis[0]);

await ctx.close();
await browser.close();
console.log('\nDONE mobile clamp');
