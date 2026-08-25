// Final verify: right-axis band alignment (numeric), modal open+hover+dismiss, at desktop 1280 + mobile 375.
import { chromium } from 'playwright';

const BASE = 'http://localhost:4173/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-planeview-refactor';

async function loadAtlas(page) {
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);
  await page.evaluate(() => {
    const all = [...document.querySelectorAll('*')];
    const hit = all.find(el => /RULED\s*V1\.2\s*Stratified Plane View/i.test(el.textContent || '') &&
      ![...el.children].some(c => /RULED\s*V1\.2\s*Stratified Plane View/i.test(c.textContent || '')));
    if (hit) hit.scrollIntoView({ block: 'start' });
  });
  await page.waitForTimeout(400);
}

function popScan() {
  return [...document.querySelectorAll('*')].filter(el => {
    const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
    return (cs.position === 'fixed' || cs.position === 'absolute')
      && b.width > 60 && b.width < 700 && b.height > 18 && b.height < 400
      && (el.textContent || '').trim().length > 4
      && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none';
  }).map(el => { const b = el.getBoundingClientRect();
    return { text: (el.textContent||'').replace(/\s+/g,' ').trim().slice(0,100), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height) };
  }).sort((a,b)=>a.w*a.h-b.w*b.h);
}

const browser = await chromium.launch();

// ===================== DESKTOP 1280 =====================
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1600 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await loadAtlas(page);

// --- RIGHT-AXIS ALIGNMENT: compare label cy to grid internal band-tag cy ---
// The baked plane draws per-cell band tags (F##/S##/V#). We can't read raster text positions from SVG,
// but the right-axis labels are meant to align to the 3 amp-bands per row. We have the 9 label centers.
// A row's 3 labels should be evenly spaced and their SPAN should match one grid-row's height.
const labelData = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]'); const sr = svg.getBoundingClientRect();
  const ts = [...svg.querySelectorAll('text')].map(t => { const r = t.getBoundingClientRect();
    return { s:(t.textContent||'').trim(), cy: r.top - sr.top + r.height/2, cx: r.left - sr.left + r.width/2 }; });
  const right = ts.filter(t => /^(FLAT|SPIKY|VAR)$/.test(t.s));
  const left = ts.filter(t => /(FREE-MOVE|WALK|ROOTED)/.test(t.s));
  return { right: right.map(t=>({s:t.s, cy:+t.cy.toFixed(1), cx:+t.cx.toFixed(1)})), left: left.map(t=>({s:t.s, cy:+t.cy.toFixed(1), cx:+t.cx.toFixed(1)})) };
});
// group right labels into 3 rows of 3
const R = labelData.right;
console.log('RIGHT labels (9):', JSON.stringify(R));
console.log('LEFT labels (3):', JSON.stringify(labelData.left));
const rows = [R.slice(0,3), R.slice(3,6), R.slice(6,9)];
rows.forEach((row,i) => {
  const gaps = [row[1].cy-row[0].cy, row[2].cy-row[1].cy];
  console.log(`row${i+1}: FLAT@${row[0].cy} SPIKY@${row[1].cy} VAR@${row[2].cy}  band-gaps=[${gaps.map(g=>g.toFixed(1))}] gapDelta=${(gaps[0]-gaps[1]).toFixed(1)} cxSpread=${(Math.max(...row.map(r=>r.cx))-Math.min(...row.map(r=>r.cx))).toFixed(1)}`);
});
// row-band centers: left label cy vs middle(SPIKY) of the right triplet — should match (both = row center)
labelData.left.forEach((l,i)=>{ const mid=rows[i][1].cy; console.log(`row${i+1} center: LEFT(${l.s})@${l.cy} vs RIGHT-SPIKY@${mid}  dy=${(l.cy-mid).toFixed(1)}`); });

// divider line
const line = await page.evaluate(() => { const l=document.querySelector('svg[viewBox] line'); if(!l)return null; const r=l.getBoundingClientRect(); const svg=document.querySelector('svg[viewBox]').getBoundingClientRect(); return {x1:Math.round(r.left-svg.left),y:Math.round(r.top-svg.top),h:Math.round(r.height),w:Math.round(r.width)}; });
console.log('right divider line:', JSON.stringify(line));

// --- MODAL TEST ---
console.log('\n=== MODAL ===');
await page.evaluate(() => { const b=[...document.querySelectorAll('button')].find(x=>/open full-size/i.test(x.textContent||'')); if(b) b.scrollIntoView({block:'center'}); });
await page.waitForTimeout(200);
await page.click('button:has-text("open full-size")').catch(async()=>{ await page.evaluate(()=>{ const b=[...document.querySelectorAll('button')].find(x=>/open full-size/i.test(x.textContent||'')); b&&b.click(); }); });
await page.waitForTimeout(800);
const modal = await page.evaluate(() => {
  // biggest fixed/high-z element covering most of viewport
  const cands = [...document.querySelectorAll('*')].filter(el=>{ const cs=getComputedStyle(el); const b=el.getBoundingClientRect();
    return (cs.position==='fixed') && b.width>window.innerWidth*0.7 && b.height>window.innerHeight*0.6; });
  const m = cands[0]; if(!m) return {open:false};
  const svgIn = m.querySelector('svg[viewBox], img, image');
  const imgIn = m.querySelector('image, img');
  const closeBtn = [...m.querySelectorAll('button, [role=button]')].find(b=>/close|✕|×/i.test(b.textContent||''));
  const r = m.getBoundingClientRect();
  return { open:true, w:Math.round(r.width), h:Math.round(r.height), hasSvg:!!m.querySelector('svg[viewBox]'), hasImage:!!imgIn, hasCloseBtn:!!closeBtn };
});
console.log('modal:', JSON.stringify(modal));
await page.screenshot({ path: `${OUT}/desktop-modal-open.png` });

// hover a dot inside the modal plane
if (modal.open) {
  const msvg = await page.evaluate(() => { const m=[...document.querySelectorAll('*')].find(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return cs.position==='fixed'&&b.width>window.innerWidth*0.7&&b.height>window.innerHeight*0.6;}); const s=m.querySelector('svg[viewBox]')||m.querySelector('image')?.closest('svg')||m.querySelector('img'); const r=(s||m).getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height}; });
  console.log('modal plane rect:', JSON.stringify({x:Math.round(msvg.x),y:Math.round(msvg.y),w:Math.round(msvg.w),h:Math.round(msvg.h)}));
  // sweep interior for a popover
  let hit=null;
  const y0=msvg.y+msvg.h*0.18, y1=msvg.y+msvg.h*0.45;
  outer: for (let yy=y0; yy<=y1; yy+=22) for (let xx=msvg.x+msvg.w*0.12; xx<=msvg.x+msvg.w*0.85; xx+=22) {
    await page.mouse.move(4,4); await page.waitForTimeout(20);
    await page.mouse.move(Math.round(xx),Math.round(yy)); await page.waitForTimeout(90);
    const pops=await page.evaluate(popScan);
    const c=pops.find(p=>p.w<520&&p.h<340&&/[A-Z][a-z]+/.test(p.text)&&/·|projectile|spiky|flat|var|walk|move|vs-|kit|Corridor|Shroud|K\d/i.test(p.text));
    if(c){hit={xx:Math.round(xx),yy:Math.round(yy),card:c};break outer;}
  }
  console.log('MODAL hover hit:', JSON.stringify(hit));
  if(hit){ await page.mouse.move(4,4);await page.waitForTimeout(60);await page.mouse.move(hit.xx,hit.yy);await page.waitForTimeout(400); await page.screenshot({path:`${OUT}/desktop-modal-hover.png`}); }
  // dismiss via Esc
  await page.mouse.move(4,4); await page.keyboard.press('Escape'); await page.waitForTimeout(500);
  const stillOpen = await page.evaluate(()=>[...document.querySelectorAll('*')].some(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return cs.position==='fixed'&&b.width>window.innerWidth*0.7&&b.height>window.innerHeight*0.6&&cs.visibility!=='hidden'&&cs.display!=='none';}));
  console.log('after Esc, modal still open?', stillOpen);
}

await ctx.close();

// ===================== MOBILE 375 =====================
console.log('\n=== MOBILE 375 ===');
const ctxM = await browser.newContext({ viewport: { width: 375, height: 900 }, deviceScaleFactor: 2 });
const pageM = await ctxM.newPage();
await loadAtlas(pageM);
// scroll container?
const scroller = await pageM.evaluate(() => {
  let el=document.querySelector('svg[viewBox]');
  while(el&&el!==document.body){const cs=getComputedStyle(el);if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&el.scrollWidth>el.clientWidth+4)return{found:true,scrollWidth:el.scrollWidth,clientWidth:el.clientWidth};el=el.parentElement;}
  return{found:false};
});
console.log('mobile h-scroll container:', JSON.stringify(scroller));
// left edge (scrollLeft 0) shot
await pageM.evaluate(()=>{let el=document.querySelector('svg[viewBox]');while(el&&el!==document.body){const cs=getComputedStyle(el);if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&el.scrollWidth>el.clientWidth+4){el.scrollLeft=0;return;}el=el.parentElement;}});
await pageM.waitForTimeout(300);
await pageM.screenshot({ path: `${OUT}/mobile-left.png` });
// right edge
await pageM.evaluate(()=>{let el=document.querySelector('svg[viewBox]');while(el&&el!==document.body){const cs=getComputedStyle(el);if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&el.scrollWidth>el.clientWidth+4){el.scrollLeft=el.scrollWidth;return;}el=el.parentElement;}});
await pageM.waitForTimeout(300);
await pageM.screenshot({ path: `${OUT}/mobile-right.png` });
console.log('saved mobile-left.png / mobile-right.png');

await browser.close();
console.log('DONE verify');
