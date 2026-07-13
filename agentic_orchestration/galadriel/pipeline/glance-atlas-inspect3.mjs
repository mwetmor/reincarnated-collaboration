import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json','utf8')); const VB = dotJson.viewBox;
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1100 } });
const page = await ctx.newPage();
const base = URL.split('#')[0];
await page.goto(base, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(()=>{});
await page.waitForTimeout(3000);

// Inspect overlay svg's 2 rects + any svg <text>, and whether the img alt/src encodes the band.
const meta = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  const rects = [...svg.querySelectorAll('rect')].map(r=>({x:r.getAttribute('x'),y:r.getAttribute('y'),w:r.getAttribute('width'),h:r.getAttribute('height'),fill:r.getAttribute('fill'),cls:r.getAttribute('class')}));
  const texts = [...svg.querySelectorAll('text')].map(t=>({t:(t.textContent||'').slice(0,40)}));
  const img = document.querySelector('img');
  // Is there an html element (not svg) whose text has UNMAPPED, searching innerText segments?
  const bandEl = [...document.querySelectorAll('div,p,section,foreignObject')].find(el=>/UNMAPPED: \d+ corpus/i.test(el.textContent||''));
  const bandInfo = bandEl ? (()=>{const b=bandEl.getBoundingClientRect();return{tag:bandEl.tagName,cls:(bandEl.getAttribute('class')||'').slice(0,80),x:Math.round(b.left),y:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height),cursor:getComputedStyle(bandEl).cursor,textLen:(bandEl.textContent||'').length};})() : null;
  return {
    svgRectCount: rects.length, rects, svgTextCount: texts.length, texts: texts.slice(0,5),
    img: img ? { src:(img.getAttribute('src')||'').slice(0,80), w:Math.round(img.getBoundingClientRect().width), h:Math.round(img.getBoundingClientRect().height) } : null,
    bandInfo,
    // full body innerText search for the band phrase to confirm whether it's live text
    bandTextPresent: /UNMAPPED: \d+ corpus/i.test(document.body.innerText||''),
    bandSnippet: (document.body.innerText.match(/UNMAPPED[^\n]{0,120}/i)||[''])[0],
  };
});
console.log('=== overlay svg rects + text + img + band ===');
console.log(JSON.stringify(meta, null, 2));

// The screenshot showed band text like "UNMAPPED: 7 corpus · 0 mint...". If bandTextPresent true it's live HTML below the svg.
// Find its container and hover it, then look for a LIST popover.
if (meta.bandTextPresent) {
  const target = await page.evaluate(() => {
    // topmost small leaf containing a roster token like "poe2-" or "B10"
    const leaves = [...document.querySelectorAll('*')].filter(el=>el.children.length===0 && /poe2-\w|B1[0-9],|movement=unknown/i.test(el.textContent||''));
    const el = leaves[0] || [...document.querySelectorAll('*')].find(e=>/UNMAPPED: \d+ corpus/i.test(e.textContent||'') && e.children.length<8);
    if(!el)return null; el.scrollIntoView({block:'center'}); const b=el.getBoundingClientRect();
    return {x:Math.round(b.left+Math.min(120,b.width/2)),y:Math.round(b.top+b.height/2),cursor:getComputedStyle(el).cursor,t:(el.textContent||'').slice(0,50)};
  });
  console.log('\nband hover target:', JSON.stringify(target));
  if (target) {
    await page.waitForTimeout(300);
    await page.mouse.move(target.x, target.y); await page.waitForTimeout(800);
    const pop = await page.evaluate(()=>{
      const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>80&&b.width<680&&b.height>24&&b.height<640&&(el.textContent||'').trim().length>10&&cs.visibility!=='hidden'&&cs.opacity!=='0'&&b.top>=-5;}).map(el=>{const b=el.getBoundingClientRect();return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,300),h:Math.round(b.height),w:Math.round(b.width),y:Math.round(b.top),liRows:el.querySelectorAll('li').length,divRows:el.querySelectorAll('div').length};});
      cards.sort((a,b)=>b.h-a.h); return cards.slice(0,5);
    });
    console.log('\npopover(s) after band hover (tallest first):');
    console.log(JSON.stringify(pop, null, 2));
    await page.screenshot({ path: `${OUT}/desktop-unmapped-hover.png` });
    console.log('screenshot: desktop-unmapped-hover.png');
  }
}
await ctx.close();
await browser.close();
console.log('DONE');
