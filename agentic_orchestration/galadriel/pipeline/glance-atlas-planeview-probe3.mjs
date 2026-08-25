// Probe 3: locate the interactive hover layer (dots live in a baked <image>, so hit targets are elsewhere),
// the "open full-size" button, and measure right-axis label vs grid-band alignment.
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

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1600 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await loadAtlas(page);

// The 3 rects inside svg — what are they?
const rects = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  const sr = svg.getBoundingClientRect();
  return [...svg.querySelectorAll('rect')].map(rc => {
    const r = rc.getBoundingClientRect();
    return { fill: getComputedStyle(rc).fill, x: Math.round(r.left-sr.left), y: Math.round(r.top-sr.top), w: Math.round(r.width), h: Math.round(r.height) };
  });
});
console.log('SVG rects:', JSON.stringify(rects, null, 1));

// The <image> baked plane
const img = await page.evaluate(() => {
  const im = document.querySelector('svg[viewBox] image');
  if (!im) return null;
  const r = im.getBoundingClientRect();
  const href = im.getAttribute('href') || im.getAttribute('xlink:href') || '';
  return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), hrefHead: href.slice(0,40), hrefLen: href.length };
});
console.log('baked plane image:', JSON.stringify(img));

// Buttons / interactive controls anywhere in the atlas section
const buttons = await page.evaluate(() => {
  const scope = document;
  return [...scope.querySelectorAll('button, a[role=button], [role=button], a')].map(b => {
    const r = b.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return null;
    return { tag: b.tagName, text: (b.textContent||'').replace(/\s+/g,' ').trim().slice(0,40),
      pageX: Math.round(r.left+r.width/2), pageY: Math.round(r.top+r.height/2), y: Math.round(r.top) };
  }).filter(Boolean).filter(b => /full|expand|open|↗|maximize|zoom/i.test(b.text) || /↗/.test(b.text));
});
console.log('\nfull-size-ish buttons:', JSON.stringify(buttons, null, 1));

// Broader: any element that toggles pointer / has a title tooltip layer OVER the image region.
const svgRect = await page.evaluate(() => { const r = document.querySelector('svg[viewBox]').getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height}; });

// Hover-hit probe: move mouse across grid interior in a coarse grid, watch for any popover appearing.
function popScan() {
  const cards = [...document.querySelectorAll('*')].filter(el => {
    const cs = getComputedStyle(el);
    const b = el.getBoundingClientRect();
    return (cs.position === 'fixed' || cs.position === 'absolute')
      && b.width > 60 && b.width < 700 && b.height > 18 && b.height < 680
      && (el.textContent || '').trim().length > 4
      && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none';
  }).map(el => {
    const b = el.getBoundingClientRect();
    return { text: (el.textContent||'').replace(/\s+/g,' ').trim().slice(0,90), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height) };
  });
  return cards;
}

// Grid interior spans roughly svg.x+90 .. svg.x+svg.w-130 ; y bands per row.
const gx0 = svgRect.x + 95, gx1 = svgRect.x + svgRect.w - 135;
const rowYs = [svgRect.y + 150, svgRect.y + 275, svgRect.y + 400]; // approx first-band centers per row
let firstHit = null;
outer:
for (const ry of rowYs) {
  for (let gx = gx0; gx <= gx1; gx += 18) {
    await page.mouse.move(4,4); await page.waitForTimeout(30);
    await page.mouse.move(Math.round(gx), Math.round(ry)); await page.waitForTimeout(120);
    const pops = await page.evaluate(popScan);
    // popover heuristic: a small card that is NOT the big legend/paragraph. Look for one whose text names a kit-like token (K\d or capitalized short).
    const card = pops.find(p => p.w < 460 && p.h < 320 && /K\d|kit|·|—|▸|›/.test(p.text) === true || (p.w<420 && p.h<260 && p.text.length<80 && /[A-Z][a-z]+/.test(p.text)));
    if (card) { firstHit = { gx: Math.round(gx), ry: Math.round(ry), card, allPops: pops.length }; break outer; }
  }
}
console.log('\nHOVER SWEEP first popover-ish hit:', JSON.stringify(firstHit, null, 1));
if (firstHit) {
  await page.mouse.move(4,4); await page.waitForTimeout(80);
  await page.mouse.move(firstHit.gx, firstHit.ry); await page.waitForTimeout(400);
  await page.screenshot({ path: `${OUT}/desktop-hover.png` });
  console.log('saved desktop-hover.png');
} else {
  // dump what popScan sees at a central point for diagnosis
  await page.mouse.move(Math.round((gx0+gx1)/2), Math.round(rowYs[0])); await page.waitForTimeout(400);
  console.log('popScan dump at center-row1:', JSON.stringify(await page.evaluate(popScan), null, 1));
  await page.screenshot({ path: `${OUT}/desktop-hover-nohit.png` });
}

await browser.close();
console.log('DONE probe3');
