// Galadriel perception check — Glance /atlas interactive overlay ALIGNMENT + POPOVER
// One-off probe for drax's transparent-SVG hotspot layer over the matplotlib plane raster.
// Read-only against target. Hover the top-left cell (free-move × projectile), screenshot,
// verify: (a) sky-outline rect lands on top-left grid cell, (b) popover shows real build name,
// (c) no docked panel below plane. Repeat at mobile to check popover clipping.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const URL = 'https://reincarnated-glance-1efbmkjhi-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-overlay-align';
mkdirSync(OUT, { recursive: true });

const viewports = [
  { name: 'desktop', width: 1000, height: 900 },
  { name: 'mobile', width: 375, height: 812 },
];

const browser = await chromium.launch();
for (const vp of viewports) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: vp.name === 'mobile' ? 2 : 1,
  });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('requestfailed', r => consoleErrors.push('REQFAIL ' + r.url() + ' ' + (r.failure()?.errorText || '')));

  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);

  // Detect auth wall
  const authWall = await page.evaluate(() => {
    const t = (document.body.innerText || '').toLowerCase();
    return /log in to vercel|authentication required|sign in to vercel|vercel authentication/.test(t)
      && !/stratified plane view|ruled/i.test(document.body.innerText || '');
  });
  if (authWall) {
    console.log(`\n===== ${vp.name} (${vp.width}px) ===== AUTH WALL DETECTED — cannot load page`);
    console.log('textSnippet:', (await page.evaluate(() => (document.body.innerText||'').slice(0,300))));
    await ctx.close();
    continue;
  }

  // Find the top-left hotspot rect by aria-label prefix.
  const targetSel = '[aria-label^="free-move × projectile"]';
  const target = await page.$(targetSel);

  // Enumerate overlay rects for geometry cross-check.
  const overlayInfo = await page.evaluate((sel) => {
    const rects = [...document.querySelectorAll('rect[aria-label], [role="button"][aria-label]')]
      .filter(el => /×/.test(el.getAttribute('aria-label') || ''));
    const info = rects.map(el => {
      const b = el.getBoundingClientRect();
      return {
        label: el.getAttribute('aria-label'),
        x: Math.round(b.left), y: Math.round(b.top),
        w: Math.round(b.width), h: Math.round(b.height),
      };
    });
    // Largest img/svg raster = the plane image
    const planeEls = [...document.querySelectorAll('img,svg')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(o => o.r.width > 150 && o.r.height > 100)
      .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
    const p = planeEls[0]?.el?.getBoundingClientRect();
    const tgt = document.querySelector(sel);
    const tb = tgt ? tgt.getBoundingClientRect() : null;
    return {
      count: info.length,
      target: tb ? { x: Math.round(tb.left), y: Math.round(tb.top), w: Math.round(tb.width), h: Math.round(tb.height) } : null,
      plane: p ? { x: Math.round(p.left), y: Math.round(p.top), w: Math.round(p.width), h: Math.round(p.height) } : null,
      rects: info.slice(0, 25),
    };
  }, targetSel);

  console.log(`\n===== ${vp.name} (${vp.width}px) =====`);
  console.log('overlay rects found:', overlayInfo.count);
  console.log('target rect (free-move × projectile):', JSON.stringify(overlayInfo.target));
  console.log('plane raster bbox:', JSON.stringify(overlayInfo.plane));
  // Target-vs-plane relative position: for a correct TOP-LEFT cell, target.x ≈ plane.x (leftmost),
  // target.y ≈ plane.y (topmost), each near the plane's left/top inset.
  if (overlayInfo.target && overlayInfo.plane) {
    const dxLeft = overlayInfo.target.x - overlayInfo.plane.x;
    const dyTop = overlayInfo.target.y - overlayInfo.plane.y;
    console.log(`target inset from plane: dxLeft=${dxLeft}px  dyTop=${dyTop}px  (cellW≈${overlayInfo.target.w}, cellH≈${overlayInfo.target.h})`);
    console.log(`  → dxLeft in cell-widths: ${(dxLeft/overlayInfo.target.w).toFixed(2)}  dyTop in cell-heights: ${(dyTop/overlayInfo.target.h).toFixed(2)}`);
  }

  if (target) {
    await target.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await target.hover();
    await page.waitForTimeout(600); // let highlight + popover render/transition
  } else {
    console.log('!! target hotspot NOT FOUND with selector', targetSel);
  }

  // Popover text probe after hover
  const pop = await page.evaluate(() => {
    // Heuristic: a small card recently shown. Look for monospace detail line + proper-noun name.
    const all = [...document.querySelectorAll('*')];
    const monoNodes = all.filter(el => {
      const cs = getComputedStyle(el);
      const fam = (cs.fontFamily || '').toLowerCase();
      return el.children.length === 0 && /mono/.test(fam) && (el.textContent||'').trim().length > 3;
    }).map(el => (el.textContent||'').trim());
    // popover container candidates: fixed/absolute small boxes with visible text
    const cards = all.filter(el => {
      const cs = getComputedStyle(el);
      const b = el.getBoundingClientRect();
      return (cs.position === 'fixed' || cs.position === 'absolute')
        && b.width > 60 && b.width < 520 && b.height > 30 && b.height < 400
        && (el.textContent||'').trim().length > 5
        && cs.visibility !== 'hidden' && cs.opacity !== '0';
    }).map(el => {
      const b = el.getBoundingClientRect();
      return { text: (el.textContent||'').trim().slice(0,200), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height), right: Math.round(b.right) };
    });
    return { monoSample: monoNodes.slice(0,8), cards: cards.slice(0,10), vpW: window.innerWidth };
  });
  console.log('popover mono lines:', JSON.stringify(pop.monoSample));
  console.log('popover card candidates:', JSON.stringify(pop.cards, null, 2));
  // Clipping check: any card extending past right edge?
  const clipped = pop.cards.filter(c => c.right > pop.vpW + 1 || c.x < -1);
  if (clipped.length) console.log('!! CARDS CLIPPED off-viewport:', JSON.stringify(clipped));
  else console.log('no card clipped off-viewport (vpW=' + pop.vpW + ')');

  // Docked-panel check: large table/panel BELOW the plane bottom.
  const dock = await page.evaluate(() => {
    const planeEls = [...document.querySelectorAll('img,svg')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(o => o.r.width > 150 && o.r.height > 100)
      .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
    const p = planeEls[0]?.el?.getBoundingClientRect();
    const planeBottomDoc = p ? p.bottom + window.scrollY : null;
    const bigBelow = [...document.querySelectorAll('table, [role="table"], section, div')]
      .map(el => ({ el, b: el.getBoundingClientRect() }))
      .filter(o => o.b.height > 200 && o.b.width > 300 && (o.b.top + window.scrollY) > (planeBottomDoc ?? 1e9) + 10)
      .map(o => ({ tag: o.el.tagName.toLowerCase(), h: Math.round(o.b.height), w: Math.round(o.b.width), topDoc: Math.round(o.b.top + window.scrollY), snippet: (o.el.innerText||'').trim().slice(0,80) }));
    return { planeBottomDoc: planeBottomDoc ? Math.round(planeBottomDoc) : null, scrollH: document.body.scrollHeight, bigBelow: bigBelow.slice(0,6) };
  });
  console.log('plane bottom (doc y):', dock.planeBottomDoc, ' body scrollHeight:', dock.scrollH);
  console.log('large blocks below plane:', JSON.stringify(dock.bigBelow, null, 2));

  // Screenshot the plane region: clip around plane bbox with margin (fresh bbox post-hover).
  const clip = await page.evaluate(() => {
    const planeEls = [...document.querySelectorAll('img,svg')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(o => o.r.width > 150 && o.r.height > 100)
      .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
    const p = planeEls[0]?.el?.getBoundingClientRect();
    if (!p) return null;
    const m = 60;
    const x = Math.max(0, p.left - m), y = Math.max(0, p.top - m);
    return { x, y, width: Math.min(window.innerWidth - x, p.width + 2*m), height: Math.min(window.innerHeight - y, p.height + 2*m + 120) };
  });
  const shotPath = `${OUT}/${vp.name}-plane-hover.png`;
  if (clip && clip.width > 0 && clip.height > 0) {
    await page.screenshot({ path: shotPath, clip });
  } else {
    await page.screenshot({ path: shotPath });
  }
  console.log('screenshot:', shotPath);
  if (consoleErrors.length) console.log('CONSOLE/NET ERRORS:', JSON.stringify(consoleErrors.slice(0,8), null, 2));
  await ctx.close();
}
await browser.close();
console.log('\nDONE. Captures in', OUT);
