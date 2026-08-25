// Galadriel perception RE-VERIFY (round 2) — Glance /atlas overlay ALIGNMENT after vertical-offset fix.
// Drax re-anchored hotspots on cell corners read from render cell-background paths (row-0 top → viewBox y=169.239).
// Check TWO cells: (A) free-move × projectile → expect TOP-LEFT. (B) rooted × summon → expect BOTTOM-RIGHT.
// Report per-cell offset in cell-heights (target: ~0), popover real-name check, screenshots desktop + mobile.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const URL = 'https://reincarnated-glance-2ritb9gwh-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-overlay-align-r2';
mkdirSync(OUT, { recursive: true });

const viewports = [{ name: 'desktop', width: 1000, height: 900 }];

const browser = await chromium.launch();
for (const vp of viewports) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('requestfailed', r => consoleErrors.push('REQFAIL ' + r.url() + ' ' + (r.failure()?.errorText || '')));

  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);

  const authWall = await page.evaluate(() => {
    const t = (document.body.innerText || '').toLowerCase();
    return /log in to vercel|authentication required|sign in to vercel|vercel authentication/.test(t)
      && !/stratified plane view|ruled/i.test(document.body.innerText || '');
  });
  if (authWall) {
    console.log(`\n===== ${vp.name} ===== AUTH WALL DETECTED`);
    console.log('textSnippet:', (await page.evaluate(() => (document.body.innerText||'').slice(0,300))));
    await ctx.close();
    continue;
  }

  // Enumerate all overlay rects + plane geometry.
  const geom = await page.evaluate(() => {
    const rects = [...document.querySelectorAll('rect[aria-label], [role="button"][aria-label], [aria-label]')]
      .filter(el => /×/.test(el.getAttribute('aria-label') || ''));
    const info = rects.map(el => {
      const b = el.getBoundingClientRect();
      return { label: el.getAttribute('aria-label'), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height) };
    });
    const planeEls = [...document.querySelectorAll('img,svg')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(o => o.r.width > 150 && o.r.height > 100)
      .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
    const p = planeEls[0]?.el?.getBoundingClientRect();
    return {
      count: info.length,
      plane: p ? { x: Math.round(p.left), y: Math.round(p.top), w: Math.round(p.width), h: Math.round(p.height), right: Math.round(p.right), bottom: Math.round(p.bottom) } : null,
      rects: info,
    };
  });
  console.log(`\n===== ${vp.name} (${vp.width}px) =====`);
  console.log('overlay rects found:', geom.count);
  console.log('plane raster bbox:', JSON.stringify(geom.plane));

  const findRect = (prefix) => geom.rects.find(r => (r.label||'').startsWith(prefix));
  const cells = [
    { key: 'A_topleft', prefix: 'free-move × projectile', expect: 'TOP-LEFT' },
    { key: 'B_botright', prefix: 'rooted × summon', expect: 'BOTTOM-RIGHT' },
  ];

  // Derive grid extent from the full rect set for offset math.
  const xs = geom.rects.map(r => r.x), ys = geom.rects.map(r => r.y);
  const gridMinX = Math.min(...xs), gridMaxX = Math.max(...xs);
  const gridMinY = Math.min(...ys), gridMaxY = Math.max(...ys);
  const cellW = geom.rects[0]?.w || 1, cellH = geom.rects[0]?.h || 1;
  console.log(`grid rect extent: x[${gridMinX}..${gridMaxX}] y[${gridMinY}..${gridMaxY}]  cellW≈${cellW} cellH≈${cellH}`);

  for (const c of cells) {
    const r = findRect(c.prefix);
    if (!r) { console.log(`\n[${c.key}] '${c.prefix}' NOT FOUND`); continue; }
    console.log(`\n[${c.key}] '${r.label}' rect: x=${r.x} y=${r.y} w=${r.w} h=${r.h}  (expect ${c.expect})`);
    // Position within grid, in cell units.
    const colUnits = (r.x - gridMinX) / cellW;
    const rowUnits = (r.y - gridMinY) / cellH;
    console.log(`  grid position: col=${colUnits.toFixed(2)} row=${rowUnits.toFixed(2)}  (top-left→0,0; bottom-right→max)`);
    // Row/col span totals
    const totalCols = Math.round((gridMaxX - gridMinX) / cellW);
    const totalRows = Math.round((gridMaxY - gridMinY) / cellH);
    if (c.key === 'A_topleft') {
      const dyTop = r.y - gridMinY, dxLeft = r.x - gridMinX;
      console.log(`  TOP-LEFT verify: dyTop=${dyTop}px (${(dyTop/cellH).toFixed(2)} cell-h), dxLeft=${dxLeft}px (${(dxLeft/cellW).toFixed(2)} cell-w) — want ~0/~0`);
    }
    if (c.key === 'B_botright') {
      const dyBot = gridMaxY - r.y, dxRight = gridMaxX - r.x;
      console.log(`  BOT-RIGHT verify: dyBot=${dyBot}px (${(dyBot/cellH).toFixed(2)} cell-h), dxRight=${dxRight}px (${(dxRight/cellW).toFixed(2)} cell-w) — want ~0/~0 (rows=${totalRows} cols=${totalCols})`);
    }
  }

  // ---- Hover + screenshot for cell A (top-left) ----
  const doHover = async (prefix, tag) => {
    const el = await page.$(`[aria-label^="${prefix}"]`);
    if (!el) { console.log(`hover: '${prefix}' not found`); return; }
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);
    await el.hover();
    await page.waitForTimeout(600);
    const pop = await page.evaluate(() => {
      const all = [...document.querySelectorAll('*')];
      const cards = all.filter(el => {
        const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && b.width > 60 && b.width < 560 && b.height > 24 && b.height < 420
          && (el.textContent||'').trim().length > 5 && cs.visibility !== 'hidden' && cs.opacity !== '0';
      }).map(el => { const b = el.getBoundingClientRect(); return { text: (el.textContent||'').trim().slice(0,200), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height) }; });
      return cards.slice(0, 8);
    });
    console.log(`\n[popover after hover '${prefix}']:`, JSON.stringify(pop, null, 2));
    const clip = await page.evaluate(() => {
      const planeEls = [...document.querySelectorAll('img,svg')]
        .map(el => ({ el, r: el.getBoundingClientRect() }))
        .filter(o => o.r.width > 150 && o.r.height > 100)
        .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
      const p = planeEls[0]?.el?.getBoundingClientRect();
      if (!p) return null;
      const m = 70;
      const x = Math.max(0, p.left - m), y = Math.max(0, p.top - m);
      return { x, y, width: Math.min(window.innerWidth - x, p.width + 2*m), height: Math.min(window.innerHeight - y, p.height + 2*m + 140) };
    });
    const shotPath = `${OUT}/${vp.name}-${tag}-hover.png`;
    if (clip && clip.width > 0) await page.screenshot({ path: shotPath, clip });
    else await page.screenshot({ path: shotPath });
    console.log('screenshot:', shotPath);
  };

  await doHover('free-move × projectile', 'A-topleft');
  await doHover('rooted × summon', 'B-botright');

  if (consoleErrors.length) console.log('\nCONSOLE/NET ERRORS:', JSON.stringify(consoleErrors.slice(0,8), null, 2));
  await ctx.close();
}
await browser.close();
console.log('\nDONE. Captures in', OUT);
