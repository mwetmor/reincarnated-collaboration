// Galadriel perception check — Glance /atlas v3 PER-DOT popover + highlight-ring alignment.
// Read-only verification of drax's per-dot interaction change. No target-file modification.
// Probes: plane raster present; overlay <svg>; plane_dot_positions.json (463 dots) load; dot geometry.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();

const netJson = [];
const consoleErrors = [];
page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('requestfailed', r => consoleErrors.push('REQFAIL ' + r.url() + ' ' + (r.failure()?.errorText || '')));
page.on('response', r => {
  const u = r.url();
  if (/plane_dot_positions|state\.json|dot|scatter/i.test(u)) netJson.push({ url: u, status: r.status(), ct: r.headers()['content-type'] });
});

const base = URL.split('#')[0];
await page.goto(base, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(3000);

const authWall = await page.evaluate(() => {
  const t = (document.body.innerText || '').toLowerCase();
  return /log in to vercel|authentication required|sign in to vercel/.test(t)
    && !/stratified plane view|ruled/i.test(document.body.innerText || '');
});
console.log('AUTH WALL:', authWall);
if (authWall) {
  console.log('snippet:', await page.evaluate(() => (document.body.innerText||'').slice(0,300)));
  await browser.close(); process.exit(0);
}

// Structural probe.
const probe = await page.evaluate(() => {
  const txt = document.body.innerText || '';
  // Largest svg/img = plane raster.
  const bigs = [...document.querySelectorAll('img,svg,canvas')]
    .map(el => ({ el, r: el.getBoundingClientRect() }))
    .filter(o => o.r.width > 150 && o.r.height > 100)
    .sort((a, b) => (b.r.width*b.r.height) - (a.r.width*a.r.height));
  const plane = bigs[0]?.el;
  const pr = plane?.getBoundingClientRect();

  // Enumerate ALL svgs and their child circle/dot count (scatter dots likely <circle> in an overlay svg).
  const svgs = [...document.querySelectorAll('svg')].map(s => {
    const r = s.getBoundingClientRect();
    return {
      cls: s.getAttribute('class') || null,
      viewBox: s.getAttribute('viewBox') || null,
      w: Math.round(r.width), h: Math.round(r.height),
      x: Math.round(r.left), y: Math.round(r.top),
      circles: s.querySelectorAll('circle').length,
      paths: s.querySelectorAll('path').length,
      rects: s.querySelectorAll('rect').length,
    };
  });

  // Count all circles anywhere (dots).
  const allCircles = document.querySelectorAll('circle').length;

  // Look for a highlight ring — an element with sky-blue stroke, likely hidden until hover.
  const ringCandidates = [...document.querySelectorAll('circle,[class*="ring"],[class*="highlight"]')].map(el => ({
    tag: el.tagName.toLowerCase(),
    cls: el.getAttribute('class') || null,
    stroke: el.getAttribute('stroke') || null,
    r: el.getAttribute('r') || null,
  })).slice(0, 20);

  return {
    hasRuled: /RULED/i.test(txt),
    hasStratified: /Stratified Plane View/i.test(txt),
    hasV12: /V1\.2/i.test(txt),
    hasUnmapped: /unmapped|movement.?unknown|roster/i.test(txt),
    planeTag: plane?.tagName?.toLowerCase() || null,
    plane: pr ? { x: Math.round(pr.left), y: Math.round(pr.top), w: Math.round(pr.width), h: Math.round(pr.height), right: Math.round(pr.right), bottom: Math.round(pr.bottom) } : null,
    svgCount: svgs.length,
    svgs,
    allCircles,
    ringCandidates,
    bodyTextLen: txt.length,
  };
});
console.log('\n===== STRUCTURAL PROBE =====');
console.log(JSON.stringify(probe, null, 2));
console.log('\n===== JSON/DOT NETWORK =====');
console.log(JSON.stringify(netJson, null, 2));
if (consoleErrors.length) console.log('\nCONSOLE/NET ERRORS:', JSON.stringify(consoleErrors.slice(0,10), null, 2));

await page.screenshot({ path: `${OUT}/desktop-fold.png` });
await page.screenshot({ path: `${OUT}/desktop-full.png`, fullPage: true });
console.log('\nscreenshots written to', OUT);

await browser.close();
console.log('DONE');
