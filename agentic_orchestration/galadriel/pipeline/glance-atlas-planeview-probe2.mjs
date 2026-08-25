// Probe 2: find real hover-target dots (not <circle>), and grab high-res crops of left gutter + right axis.
import { chromium } from 'playwright';
import sharp from 'sharp';

const BASE = 'http://localhost:4173/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-planeview-refactor';

async function loadAtlas(page) {
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1600 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await loadAtlas(page);

// Scroll section to top
await page.evaluate(() => {
  const all = [...document.querySelectorAll('*')];
  const hit = all.find(el => /RULED\s*V1\.2\s*Stratified Plane View/i.test(el.textContent || '') &&
    ![...el.children].some(c => /RULED\s*V1\.2\s*Stratified Plane View/i.test(c.textContent || '')));
  if (hit) hit.scrollIntoView({ block: 'start' });
});
await page.waitForTimeout(400);

// SVG page-rect
const svgRect = await page.evaluate(() => {
  const s = document.querySelector('svg[viewBox]');
  const r = s.getBoundingClientRect();
  return { x: r.left, y: r.top, w: r.width, h: r.height };
});
console.log('SVG page rect:', JSON.stringify({x:Math.round(svgRect.x),y:Math.round(svgRect.y),w:Math.round(svgRect.w),h:Math.round(svgRect.h)}));

// Enumerate ALL leaf-ish drawable elements in the svg to find dot candidates + count marks.
const marks = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  const sr = svg.getBoundingClientRect();
  const tags = {};
  [...svg.querySelectorAll('*')].forEach(el => { tags[el.tagName] = (tags[el.tagName]||0)+1; });
  // dot candidates: small elements with a title/data attr, or that respond to pointer. Look for elements w/ a <title> child or data-kit.
  const cand = [...svg.querySelectorAll('*')].filter(el => {
    const r = el.getBoundingClientRect();
    const small = r.width > 1 && r.width < 22 && r.height > 1 && r.height < 22;
    const hasTitle = el.querySelector('title') || el.getAttribute('data-kit') || el.getAttribute('data-name');
    const pe = getComputedStyle(el).pointerEvents;
    return small && (hasTitle || el.tagName === 'circle' || el.tagName === 'rect' || el.tagName === 'path' || el.tagName === 'use') && pe !== 'none';
  }).map(el => {
    const r = el.getBoundingClientRect();
    const title = el.querySelector('title')?.textContent || el.getAttribute('data-kit') || el.getAttribute('data-name') || '';
    return { tag: el.tagName, cls: (el.getAttribute('class')||'').slice(0,30),
      pageX: Math.round(r.left + r.width/2), pageY: Math.round(r.top + r.height/2),
      svgX: Math.round(r.left - sr.left + r.width/2), svgY: Math.round(r.top - sr.top + r.height/2),
      w: +r.width.toFixed(1), h: +r.height.toFixed(1), title: title.slice(0,30) };
  });
  return { tagCounts: tags, candCount: cand.length, cands: cand.slice(0, 30) };
});
console.log('\nSVG tag counts:', JSON.stringify(marks.tagCounts));
console.log('dot candidate count:', marks.candCount);
console.log('sample candidates:', JSON.stringify(marks.cands, null, 1));

// Take a fresh full section shot to crop from
const shotPath = `${OUT}/probe2-full.png`;
await page.screenshot({ path: shotPath });

// Crop LEFT gutter: svg x .. x+70, full svg height. deviceScaleFactor=2 so multiply.
const S = 2;
const meta = await sharp(shotPath).metadata();
console.log('\nfull shot dims:', meta.width, meta.height);
const clamp = (v,max) => Math.max(0, Math.min(max, Math.round(v)));
async function crop(name, x, y, w, h) {
  const L = clamp(x*S, meta.width), T = clamp(y*S, meta.height);
  const W = clamp(w*S, meta.width - L), H = clamp(h*S, meta.height - T);
  await sharp(shotPath).extract({ left: L, top: T, width: W, height: H }).toFile(`${OUT}/${name}.png`);
  console.log(`crop ${name}:`, L, T, W, H);
}
// left gutter (a bit of grid too, to check for baked-label bleed)
await crop('crop-left-gutter', svgRect.x - 6, svgRect.y, 130, svgRect.h);
// right axis strip
await crop('crop-right-axis', svgRect.x + svgRect.w - 120, svgRect.y, 130, svgRect.h);

await browser.close();
console.log('DONE probe2');
