// C-9 -- the page's first-strike cold frame, traced: Chrome's own trace (GPU process included) over the
// first strike of a session (?c=sorceress&perf=fbc: the control cast first), then the longest slices.
//   PLAYWRIGHT_CORE=<playwright-core> node web_trace_first_strike.js <url> <outdir>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2]; const outdir = process.argv[3];
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false, args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--window-size=900,480'] });
  const context = await browser.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  const page = await context.newPage();
  let built = 0; const t0 = Date.now();
  page.on('console', (m) => { const s = m.text(); if (!built && s.startsWith('[barrow_painted] web:')) built = Date.now() - t0; });
  await page.goto(url, { waitUntil: 'load', timeout: 300000 });
  for (let i = 0; i < 200 && !built; i++) await sleep(250);
  await browser.startTracing(page, { path: path.join(outdir, 'trace.json'), screenshots: false,
    categories: ['devtools.timeline', 'gpu', 'disabled-by-default-gpu.service', 'disabled-by-default-devtools.timeline', 'toplevel', 'viz'] });
  await sleep(9000);   // the harness casts at +3 s after it starts; the cold frame comes ~2 s later
  await browser.stopTracing();
  console.log('built', built);
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
