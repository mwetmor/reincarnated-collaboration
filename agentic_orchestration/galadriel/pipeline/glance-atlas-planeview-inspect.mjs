// Inspect the refactored /atlas plane-view overlay on the LOCAL preview.
// Goal: understand DOM structure so the verify pass can target axis labels + dots precisely.
import { chromium } from 'playwright';

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

// 1) Find the section titled RULED V1.2 Stratified Plane View
const section = await page.evaluate(() => {
  const all = [...document.querySelectorAll('*')];
  const hit = all.find(el => /RULED\s*V1\.2\s*Stratified Plane View/i.test(el.textContent || '') &&
    ![...el.children].some(c => /RULED\s*V1\.2\s*Stratified Plane View/i.test(c.textContent || '')));
  if (!hit) return { found: false };
  const r = hit.getBoundingClientRect();
  return { found: true, tag: hit.tagName, text: (hit.textContent||'').replace(/\s+/g,' ').trim().slice(0,80), top: Math.round(r.top + window.scrollY) };
});
console.log('SECTION TITLE:', JSON.stringify(section));

// 2) Enumerate SVGs on the page with a viewBox (the plane is SVG-based per prior work)
const svgs = await page.evaluate(() => {
  return [...document.querySelectorAll('svg')].map((s, i) => {
    const r = s.getBoundingClientRect();
    return { i, viewBox: s.getAttribute('viewBox'), x: Math.round(r.left), y: Math.round(r.top + window.scrollY), w: Math.round(r.width), h: Math.round(r.height),
      textNodes: [...s.querySelectorAll('text')].length };
  });
});
console.log('SVGs:', JSON.stringify(svgs, null, 2));

// 3) Dump ALL <text> elements inside the plane SVG (largest text-bearing svg), with content + position + rotation.
const texts = await page.evaluate(() => {
  const svgList = [...document.querySelectorAll('svg')].filter(s => s.querySelectorAll('text').length > 0);
  svgList.sort((a,b) => b.querySelectorAll('text').length - a.querySelectorAll('text').length);
  const svg = svgList[0];
  if (!svg) return { found: false };
  const sr = svg.getBoundingClientRect();
  const out = [...svg.querySelectorAll('text')].map(t => {
    const r = t.getBoundingClientRect();
    const tr = t.getAttribute('transform') || '';
    const cs = getComputedStyle(t);
    return {
      s: (t.textContent||'').trim().slice(0,28),
      x: Math.round(r.left - sr.left), y: Math.round(r.top - sr.top),
      w: Math.round(r.width), h: Math.round(r.height),
      cx: Math.round(r.left - sr.left + r.width/2), cy: Math.round(r.top - sr.top + r.height/2),
      transform: tr.slice(0,40),
      writingMode: cs.writingMode, textAnchor: t.getAttribute('text-anchor') || cs.textAnchor
    };
  });
  return { found: true, svgW: Math.round(sr.width), svgH: Math.round(sr.height), count: out.length, texts: out };
});
console.log('\nPLANE SVG TEXTS:', JSON.stringify(texts, null, 2));

// 4) Enumerate small dots (candidate hover targets) — circles inside the plane svg
const dots = await page.evaluate(() => {
  const svgList = [...document.querySelectorAll('svg')].filter(s => s.querySelectorAll('text').length > 0);
  svgList.sort((a,b) => b.querySelectorAll('text').length - a.querySelectorAll('text').length);
  const svg = svgList[0];
  if (!svg) return { found: false };
  const sr = svg.getBoundingClientRect();
  const circles = [...svg.querySelectorAll('circle')].map(c => {
    const r = c.getBoundingClientRect();
    return { cx: Math.round(r.left - sr.left + r.width/2), cy: Math.round(r.top - sr.top + r.height/2),
      d: Math.round(r.width), fill: getComputedStyle(c).fill.slice(0,24), pageX: Math.round(r.left+r.width/2), pageY: Math.round(r.top+r.height/2+window.scrollY) };
  });
  // stars may be <path> or <polygon>
  const stars = [...svg.querySelectorAll('polygon, path')].length;
  return { found: true, circleCount: circles.length, starLikeCount: stars, circles: circles.slice(0, 12) };
});
console.log('\nPLANE DOTS:', JSON.stringify(dots, null, 2));

// Full-page screenshot of the atlas section for eyeballing
await page.evaluate(() => {
  const all = [...document.querySelectorAll('*')];
  const hit = all.find(el => /RULED\s*V1\.2\s*Stratified Plane View/i.test(el.textContent || '') &&
    ![...el.children].some(c => /RULED\s*V1\.2\s*Stratified Plane View/i.test(c.textContent || '')));
  if (hit) hit.scrollIntoView({ block: 'start' });
});
await page.waitForTimeout(400);
await page.screenshot({ path: `${OUT}/inspect-desktop-section.png` });
console.log('\nsaved inspect-desktop-section.png');

await browser.close();
console.log('DONE inspect');
