// C-9 -- the base page's ~4.5 s hitch, traced: Chrome's trace over 2.5-7 s after the level's ready line (V8 GC,
// GPU service, loading, timeline), plus requestAnimationFrame intervals, so a run can be kept only if it CAUGHT
// the long frame.  PLAYWRIGHT_CORE=<pc> node web_trace_4s.js <url> <out.json>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const url = process.argv[2]; const out = process.argv[3]; const mode = process.argv[4] || 'window';
const CATS = mode === 'gc' ? ['v8', 'disabled-by-default-v8.gc', 'toplevel'] : ['devtools.timeline', 'v8', 'disabled-by-default-v8.gc', 'gpu', 'disabled-by-default-gpu.service', 'loading', 'toplevel', 'blink.console'];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false, args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--window-size=900,480'] });
  const context = await browser.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  await context.addInitScript(() => { window.__raf = []; const f = (t) => { window.__raf.push(t); requestAnimationFrame(f); }; requestAnimationFrame(f);
    window.__ready = 0; const log = console.log.bind(console); console.log = (...a) => { if (!window.__ready && String(a[0]).startsWith('[barrow_painted] web:')) window.__ready = performance.now(); return log(...a); }; });
  const page = await context.newPage();
  if (mode !== 'window') await browser.startTracing(page, { path: out, screenshots: false, categories: CATS });
  await page.goto(url, { waitUntil: 'load', timeout: 300000 });
  for (let i = 0; i < 400; i++) { if (await page.evaluate(() => window.__ready)) break; await sleep(100); }
  await sleep(2500);
  if (mode === 'window') await browser.startTracing(page, { path: out, screenshots: false, categories: CATS });
  const tStart = await page.evaluate(() => performance.now());
  await sleep(4500);
  await browser.stopTracing();
  const r = await page.evaluate(() => ({ raf: window.__raf, ready: window.__ready }));
  let worst = [0, 0];
  for (let i = 1; i < r.raf.length; i++) { const d = r.raf[i] - r.raf[i - 1]; if (r.raf[i - 1] >= r.ready && d > worst[1]) worst = [Math.round(r.raf[i - 1] - r.ready), Math.round(d)]; }
  console.log(JSON.stringify({ worst_after_ready: worst, trace_from_s_after_ready: Math.round(tStart - r.ready) / 1000 }));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
