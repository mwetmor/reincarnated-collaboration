// Re-verify ONLY the mobile clamp fix (item-6 refix) on the new build.
// Items 1-5 already confirmed last round; do NOT redo them.
// Left case = the region where "Galvanic Shards Merc" clipped to "anic Shards Merc" before.
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';

const URL_NEW = 'https://reincarnated-glance-frfn98i8m-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-clamp-refix';
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json', 'utf8'));
const VB = dotJson.viewBox;
const dots = dotJson.dots;

// Scan for the popover card: absolutely/fixed-positioned, mono-font tag row inside, reasonable card size.
function popScan() {
  const cards = [...document.querySelectorAll('*')].filter(el => {
    const cs = getComputedStyle(el);
    const b = el.getBoundingClientRect();
    return (cs.position === 'fixed' || cs.position === 'absolute')
      && b.width > 70 && b.width < 700 && b.height > 20 && b.height < 680
      && (el.textContent || '').trim().length > 6
      && cs.visibility !== 'hidden' && cs.opacity !== '0';
  }).map(el => {
    const b = el.getBoundingClientRect();
    const mono = [...el.querySelectorAll('*')].some(d => /mono/i.test(getComputedStyle(d).fontFamily));
    // tag row = presence of at least one mono descendant chip
    const tagCount = [...el.querySelectorAll('*')].filter(d => /mono/i.test(getComputedStyle(d).fontFamily) && (d.textContent || '').trim().length > 0).length;
    return {
      text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
      x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height),
      right: Math.round(b.right), bottom: Math.round(b.bottom), hasMono: mono, tagCount
    };
  });
  return cards.filter(c => c.hasMono).sort((a, b) => (a.w * a.h) - (b.w * b.h));
}

async function loadAtlas(page, viewport) {
  const base = URL_NEW.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(3000);
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(500);
}

function svgBox(page) {
  return page.evaluate(() => {
    const r = document.querySelector('svg[viewBox]').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
}

// ============ MOBILE 375 ============
console.log('=== MOBILE 375px CLAMP RE-VERIFY (new fixed build) ===\n');
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await loadAtlas(page);

// Find the horizontal-scroll container that holds the plane (plane wider than viewport).
const scroller = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  let el = svg;
  while (el && el !== document.body) {
    const cs = getComputedStyle(el);
    if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 4) {
      return { found: true, scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, tag: el.tagName, cls: (el.className || '').toString().slice(0, 60) };
    }
    el = el.parentElement;
  }
  return { found: false };
});
console.log('scroll container:', JSON.stringify(scroller));

async function hoverTest(label, screenX, screenY, expectSide) {
  await page.mouse.move(2, 2); await page.waitForTimeout(200);
  await page.mouse.move(screenX, screenY); await page.waitForTimeout(750);
  const pops = await page.evaluate(popScan);
  const p = pops[0] || null;
  let verdict;
  if (!p) {
    verdict = { popover: 'NONE' };
  } else {
    const onScreen = p.x >= 0 && p.right <= 375;
    // Title truncation heuristic: card body has a title; check it's not starting mid-word with the known clip signature.
    const clippedSig = /anic Shards Merc|^\w{0,3}[a-z] (Shards|Merc)/.test(p.text) && !/Galvanic/.test(p.text);
    verdict = {
      onScreen, leftEdge: p.x, rightEdge: p.right, w: p.w,
      overflowL: Math.max(0, -p.x), overflowR: Math.max(0, p.right - 375),
      tagRowChips: p.tagCount, titleClippedSig: clippedSig
    };
  }
  console.log(`\n[${label}] hover screen(${screenX},${screenY}) expect=${expectSide}`);
  console.log('  popover:', JSON.stringify(p));
  console.log('  VERDICT:', JSON.stringify(verdict));
  await page.screenshot({ path: `${OUT}/mobile-${label}.png` });
  return { p, verdict };
}

// ---- ITEM 1: LEFT-side dot (the clip region) ----
// Bring the LEFT edge of the plane into view (scroll to 0) then hover a left-column dot.
await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  let el = svg;
  while (el && el !== document.body) {
    const cs = getComputedStyle(el);
    if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 4) { el.scrollLeft = 0; return; }
    el = el.parentElement;
  }
});
await page.waitForTimeout(400);
let sb = await svgBox(page);
let sx = sb.w / VB.w, sy = sb.h / VB.h;
console.log('\nsvg bbox (scrollLeft=0):', JSON.stringify({ x: Math.round(sb.x), y: Math.round(sb.y), w: Math.round(sb.w), h: Math.round(sb.h) }));
// leftmost dots now on-screen
let visL = dots.map(d => ({ d, X: sb.x + d.px * sx, Y: sb.y + d.py * sy })).filter(o => o.X > 2 && o.X < 373 && o.Y > 2 && o.Y < 806);
visL.sort((a, b) => a.X - b.X);
console.log('leftmost visible dots:', visL.slice(0, 4).map(o => `${o.d.display_name.slice(0, 24)}@${Math.round(o.X)},${Math.round(o.Y)}`).join(' | '));
const L1 = await hoverTest('left-1', Math.round(visL[0].X), Math.round(visL[0].Y), 'LEFT');
const L2 = await hoverTest('left-2', Math.round(visL[2].X), Math.round(visL[2].Y), 'LEFT');
// also probe a couple more left-column candidates to try to land the "Galvanic Shards" kit specifically
const gv = dots.map(d => ({ d, X: sb.x + d.px * sx, Y: sb.y + d.py * sy }))
  .filter(o => /galvanic|shard/i.test(o.d.display_name) && o.X > 2 && o.X < 373 && o.Y > 2 && o.Y < 806);
console.log('\nGalvanic/Shard dots on-screen at scrollLeft=0:', gv.map(o => `${o.d.display_name.slice(0,30)}@${Math.round(o.X)},${Math.round(o.Y)}`).join(' | ') || 'none in view');
let L3 = null;
if (gv.length) L3 = await hoverTest('left-galvanic', Math.round(gv[0].X), Math.round(gv[0].Y), 'LEFT');

// ---- ITEM 2: RIGHT-side dot (scroll plane right, then hover) ----
const scrolled = await page.evaluate(() => {
  const svg = document.querySelector('svg[viewBox]');
  let el = svg;
  while (el && el !== document.body) {
    const cs = getComputedStyle(el);
    if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 4) { el.scrollLeft = el.scrollWidth; return { scrollLeft: el.scrollLeft, max: el.scrollWidth - el.clientWidth }; }
    el = el.parentElement;
  }
  return null;
});
console.log('\nscrolled plane fully right:', JSON.stringify(scrolled));
await page.waitForTimeout(400);
sb = await svgBox(page); sx = sb.w / VB.w; sy = sb.h / VB.h;
console.log('svg bbox (scrolled right):', JSON.stringify({ x: Math.round(sb.x), y: Math.round(sb.y), w: Math.round(sb.w), h: Math.round(sb.h) }));
let visR = dots.map(d => ({ d, X: sb.x + d.px * sx, Y: sb.y + d.py * sy })).filter(o => o.X > 2 && o.X < 373 && o.Y > 2 && o.Y < 806);
visR.sort((a, b) => b.X - a.X);
console.log('rightmost visible dots:', visR.slice(0, 4).map(o => `${o.d.display_name.slice(0, 24)}@${Math.round(o.X)},${Math.round(o.Y)}`).join(' | '));
const R1 = visR.length ? await hoverTest('right-1', Math.round(visR[0].X), Math.round(visR[0].Y), 'RIGHT') : null;
const R2 = visR.length > 2 ? await hoverTest('right-2', Math.round(visR[2].X), Math.round(visR[2].Y), 'RIGHT') : null;

await ctx.close();

// ============ DESKTOP SANITY (item 3) ============
console.log('\n=== DESKTOP SANITY (item 3) ===');
const ctxD = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
const pageD = await ctxD.newPage();
await loadAtlas(pageD);
const sbD = await svgBox(pageD);
const sxD = sbD.w / VB.w, syD = sbD.h / VB.h;
// mid-plane dot
const visD = dots.map(d => ({ d, X: sbD.x + d.px * sxD, Y: sbD.y + d.py * syD }))
  .filter(o => o.X > sbD.x + sbD.w * 0.35 && o.X < sbD.x + sbD.w * 0.6 && o.Y > sbD.y + 40 && o.Y < sbD.y + sbD.h - 40);
const mid = visD[Math.floor(visD.length / 2)] || visD[0];
await pageD.mouse.move(4, 4); await pageD.waitForTimeout(200);
await pageD.mouse.move(Math.round(mid.X), Math.round(mid.Y)); await pageD.waitForTimeout(750);
const popsD = await pageD.evaluate(popScan);
const pD = popsD[0] || null;
// count how many distinct popover cards appeared (want exactly ONE single-kit popover)
const cardCount = popsD.length;
const centered = pD ? Math.abs((pD.x + pD.right) / 2 - mid.X) : null;
console.log('mid-plane dot:', mid.d.display_name.slice(0, 40), '@', Math.round(mid.X), Math.round(mid.Y));
console.log('desktop popover:', JSON.stringify(pD));
console.log('desktop verdict:', JSON.stringify({ cardCount, onScreen: pD ? (pD.x >= 0 && pD.right <= 1440) : false, cardCenterVsDotDx: centered != null ? Math.round(centered) : null }));
await pageD.screenshot({ path: `${OUT}/desktop-mid.png` });
await ctxD.close();

await browser.close();
console.log('\nDONE clamp re-verify');
