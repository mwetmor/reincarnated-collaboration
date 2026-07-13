// FINAL: hover the 2 overlay hit-rects directly. Rect2 => LIST (item5). Mobile edge-clamp non-touch (item6).
import { chromium } from 'playwright';
import { mkdirSync, readFileSync } from 'node:fs';
const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
mkdirSync(OUT, { recursive: true });
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json','utf8')); const VB = dotJson.viewBox; const dots = dotJson.dots;

function popScan() {
  const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>70&&b.width<700&&b.height>20&&b.height<680&&(el.textContent||'').trim().length>6&&cs.visibility!=='hidden'&&cs.opacity!=='0'&&b.top>=-5;}).map(el=>{const b=el.getBoundingClientRect();const mono=[...el.querySelectorAll('*')].some(d=>/mono/i.test(getComputedStyle(d).fontFamily));return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,300),x:Math.round(b.left),y:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height),right:Math.round(b.right),hasMono:mono};});
  return cards.sort((a,b)=>(a.w*a.h)-(b.w*b.h));
}

const browser = await chromium.launch();

// ===== DESKTOP: hover rect1 (per-dot) mid, and rect2 (unmapped list) mid =====
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1150 } });
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(()=>{});
  await page.waitForTimeout(3000);
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(400);
  const svgBox = await page.evaluate(() => { const r=document.querySelector('svg[viewBox]').getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height}; });
  const sx = svgBox.w/VB.w, sy = svgBox.h/VB.h;
  const toScr = (px,py)=>({x:svgBox.x+px*sx, y:svgBox.y+py*sy});

  // --- rect2 center (unmapped band) ---
  const r2 = { x: 110.541763, y: 482.279412, w: 725.76, h: 212.7584 };
  const r2c = toScr(r2.x + r2.w/2, r2.y + r2.h*0.25); // upper part of band = the movement=unknown line
  await page.mouse.move(r2c.x, r2c.y); await page.waitForTimeout(800);
  const p2 = await page.evaluate(popScan);
  // list heuristic: tall card OR many separators, and NOT a single-kit (no lone mono+3tags shape)
  const tallest = [...p2].sort((a,b)=>b.h-a.h)[0];
  const listy = tallest ? (tallest.h > 90 || (tallest.text.match(/·|,|poe2|B1[0-9]|K[0-9]|roster|movement=unknown/gi)||[]).length >= 4) : false;
  console.log('===== ITEM 5: UNMAPPED band (rect2) hover =====');
  console.log('hover screen:', Math.round(r2c.x), Math.round(r2c.y));
  console.log('tallest card:', JSON.stringify(tallest));
  console.log('looksLikeList:', listy);
  console.log('all cards:', JSON.stringify(p2.slice(0,4), null, 2));
  await page.screenshot({ path: `${OUT}/desktop-unmapped-list-hover.png` });

  // --- rect1: confirm a mid-plane dense hover still yields single-kit (contrast) ---
  const tl = dots.filter(d=>d.cell.movement==='FREE-MOVE'&&d.cell.delivery==='PROJECTILE');
  const one = tl.reduce((a,b)=>Math.abs(b.px-165)+Math.abs(b.py-220)<Math.abs(a.px-165)+Math.abs(a.py-220)?b:a);
  const oc = toScr(one.px, one.py);
  await page.mouse.move(oc.x, oc.y); await page.waitForTimeout(600);
  const p1 = await page.evaluate(popScan);
  const single = p1.find(c=>c.hasMono) || p1[0];
  console.log('\n===== contrast: rect1 per-dot popover =====');
  console.log('single-kit card:', JSON.stringify(single));
  await ctx.close();
}

// ===== MOBILE 375 non-touch: edge-clamp =====
{
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 }); // NO isMobile/hasTouch so hover fires
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(()=>{});
  await page.waitForTimeout(3000);
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(400);
  const svgBox = await page.evaluate(() => { const r=document.querySelector('svg[viewBox]').getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height}; });
  const sx=svgBox.w/VB.w, sy=svgBox.h/VB.h;
  console.log('\n===== ITEM 6: MOBILE 375 edge-clamp =====');
  console.log('svg bbox:', JSON.stringify({x:Math.round(svgBox.x),y:Math.round(svgBox.y),w:Math.round(svgBox.w),h:Math.round(svgBox.h)}));
  // pick dot whose on-screen X is closest to the right edge (but < 375) to force popover to want to overflow
  const vis = dots.map(d=>({d,X:svgBox.x+d.px*sx,Y:svgBox.y+d.py*sy})).filter(o=>o.X>5&&o.X<374&&o.Y>5&&o.Y<807);
  vis.sort((a,b)=>b.X-a.X);
  const t = vis[0];
  console.log('rightmost-visible dot:', t.d.display_name, 'screenX', Math.round(t.X), 'of 375');
  await page.mouse.move(t.X, t.Y); await page.waitForTimeout(800);
  const p = await page.evaluate(popScan);
  const single = p.find(c=>c.hasMono) || p[0];
  const clamp = single ? { popover: single, viewportW:375, onScreen: single.x>=-1 && single.right<=376, overflowRightPx: Math.max(0,single.right-375), overflowLeftPx: Math.max(0,-single.x) } : {popover:null};
  console.log(JSON.stringify(clamp, null, 2));
  await page.screenshot({ path: `${OUT}/mobile-375-edge-hover.png` });
  if (single) { const c={x:Math.max(0,single.x-8),y:Math.max(0,single.y-8),width:Math.min(375,single.w+30),height:Math.min(812,single.h+30)}; await page.screenshot({path:`${OUT}/mobile-375-popover-crop.png`,clip:c}); }

  // also test a dot near the LEFT edge for completeness
  vis.sort((a,b)=>a.X-b.X); const tl2=vis[0];
  await page.mouse.move(tl2.X, tl2.Y); await page.waitForTimeout(600);
  const pL=await page.evaluate(popScan); const sL=pL.find(c=>c.hasMono)||pL[0];
  console.log('leftmost-visible dot:', tl2.d.display_name,'screenX',Math.round(tl2.X));
  console.log('left popover clamp:', sL?JSON.stringify({x:sL.x,right:sL.right,onScreen:sL.x>=-1&&sL.right<=376}):'none');
  await ctx.close();
}
await browser.close();
console.log('\nDONE final');
