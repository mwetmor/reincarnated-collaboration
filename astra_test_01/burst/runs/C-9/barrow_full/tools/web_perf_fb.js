// C-9 (c) -- the Fire Ball's budget on the PAGE: /playtest/barrow-painted/?c=sorceress&perf=fb, in Chrome with its
// GPU at phone size (844 x 390 CSS px at DPR 3). The scene runs its own A/B casts (godot/scripts/perf_fireball.gd)
// and prints one "[perf_fb] {...}" line; this waits for it and writes it out, with the page's load clock and
// any errors. A screenshot is taken during the first burst.
//   PLAYWRIGHT_CORE=<playwright-core> node web_perf_fb.js <url> <outdir> [tag]
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2]; const outdir = process.argv[3]; const tag = process.argv[4] || 'phone';
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false, args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--window-size=900,480', '--window-position=40,40'] });
  const context = await browser.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  await context.addInitScript(() => { window.__raf = []; const f = (t) => { window.__raf.push(t); requestAnimationFrame(f); }; requestAnimationFrame(f);
    window.__lift = 0; const log = console.log.bind(console); console.log = (...a) => { if (!window.__lift && String(a[0]).startsWith('[veil] lifted')) window.__lift = performance.now(); if (!window.__ready && String(a[0]).startsWith('[barrow_painted] web:')) window.__ready = performance.now(); return log(...a); }; });
  const page = await context.newPage();
  const logs = []; let perf = null; let built = 0; let lifted = 0; const t0 = Date.now();
  page.on('console', (m) => { const s = m.text(); logs.push(`[${m.type()}] ${s.slice(0, 400)}`);
    if (s.startsWith('[perf_fb] ')) perf = JSON.parse(s.slice(10));
    if (!built && s.startsWith('[barrow_painted] web:')) built = Date.now() - t0;
    if (!lifted && s.startsWith('[veil] lifted')) lifted = Date.now() - t0; });
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  await page.goto(url, { waitUntil: 'load', timeout: 300000 });
  let shot = false;
  for (let i = 0; i < 400 && !perf && !(process.env.WAIT_S && i * 500 > +process.env.WAIT_S * 1000); i++) {
    await sleep(500);
    if (built && !shot && Date.now() - t0 > built + 3000 + 1250) { await page.screenshot({ path: path.join(outdir, `${tag}_first_burst.png`) }); shot = true; }
  }
  const raf = await page.evaluate(() => ({ raf: window.__raf, lift: window.__lift, ready: window.__ready }));
  const afterReady = []; for (let i = 1; i < raf.raf.length; i++) if (raf.ready && raf.raf[i - 1] >= raf.ready) afterReady.push([Math.round(raf.raf[i - 1] - raf.ready), Math.round((raf.raf[i] - raf.raf[i - 1]) * 10) / 10]);
  const worst_raf_after_ready = afterReady.sort((a, b) => b[1] - a[1]).slice(0, 6);
  const after = []; for (let i = 1; i < raf.raf.length; i++) if (raf.lift && raf.raf[i - 1] >= raf.lift) after.push([Math.round(raf.raf[i - 1] - raf.lift), Math.round((raf.raf[i] - raf.raf[i - 1]) * 10) / 10]);
  const worst_raf_after_veil = after.sort((a, b) => b[1] - a[1]).slice(0, 5);
  fs.writeFileSync(path.join(outdir, `${tag}_perf.json`), JSON.stringify({ url, built_ms: built, veil_lifted_ms: lifted, worst_raf_after_veil_ms_since_lift: worst_raf_after_veil, worst_raf_after_ready_ms_since_ready: worst_raf_after_ready, perf,
    errors: logs.filter((l) => /\[error\]|pageerror|SCRIPT ERROR|SHADER ERROR/i.test(l)).slice(0, 20) }, null, 1));
  fs.writeFileSync(path.join(outdir, `${tag}_console.txt`), logs.join('\n'));
  console.log(JSON.stringify({ built_ms: built, got: !!perf, errors: logs.filter((l) => /error/i.test(l)).length }));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
