// C-9 -- the cliffside fire bolt (fire_bolt_e1_B) on the LIVE /playtest/cliffside/ page, timed in Chrome.
// drax. The diagnosis the coordinator ordered before any port: where the fire bolt spends its time.
//
//   PLAYWRIGHT_CORE=<playwright-core> node web_cliffside_fire_diag.js <url> <outdir> <profile> [casts]
//   profile: desktop (1600 x 900, DPR 1, no touch) | phone (844 x 390 at DPR 3, touch) | phone4x (phone, CPU throttled 4x)
//
// Chrome with its GPU (ANGLE on Metal). The page's own keys: Tab cycles the kit (9 presses from
// frozen_orb to fire_bolt_e1_B), E casts. The mouse sits right of the keeper (the desktop aim).
// The page times itself: every requestAnimationFrame (Godot's web main loop runs on rAF, so the
// interval between two is a frame), every long task (> 50 ms on the main thread), and the moment of
// each cast. A frame's interval is capped below by the display (16.7 ms at 60 Hz); a hitch is one
// frame longer than that.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');

const url = process.argv[2];
const outdir = process.argv[3];
const profile = process.argv[4] || 'desktop';
const casts = parseInt(process.argv[5] || '6', 10);
const tag = process.argv[6] ? process.argv[6] + '_' : '';
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const PHONE = profile.startsWith('phone');
const VW = PHONE ? 844 : 1600, VH = PHONE ? 390 : 900;

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
    args: ['--use-angle=metal', '--ignore-gpu-blocklist', `--window-size=${VW + 60},${VH + 140}`, '--window-position=20,20'],
  });
  const context = await browser.newContext(PHONE
    ? { viewport: { width: VW, height: VH }, deviceScaleFactor: 3, hasTouch: true, isMobile: true }
    : { viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  await context.addInitScript(() => {
    window.__raf = []; window.__lt = []; window.__marks = []; window.__log = [];
    const tick = (t) => { window.__raf.push(t); requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
    try {
      new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__lt.push([Math.round(e.startTime), Math.round(e.duration)]); })
        .observe({ type: 'longtask', buffered: true });
    } catch (e) { window.__lt_error = String(e); }
    const log = console.log.bind(console);
    console.log = (...a) => { const s = String(a[0]); window.__log.push([Math.round(performance.now()), s.slice(0, s.startsWith('[diag') ? 4000 : 200)]); return log(...a); };
  });
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  if (profile === 'phone4x') await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const errors = [];
  page.on('pageerror', (e) => errors.push(`[pageerror] ${e.message}`));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
  await page.goto(url, { waitUntil: 'load', timeout: 300000 });
  for (let i = 0; i < 600; i++) {
    const gone = await page.evaluate(() => {
      const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true;
    });
    if (gone) break;
    await sleep(500);
  }
  await sleep(6000);
  const gl = await page.evaluate(() => {
    const c = document.createElement('canvas').getContext('webgl2');
    const e = c && c.getExtension('WEBGL_debug_renderer_info');
    return c ? (e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER)) : 'no webgl2';
  });
  const canvas = await page.evaluate(() => { const c = document.getElementById('canvas'); return c ? [c.width, c.height] : null; });
  await page.mouse.move(VW * 0.78, VH * 0.52);
  await page.focus('#canvas').catch(() => {});
  for (let i = 0; i < 9; i++) { await page.keyboard.down('Tab'); await sleep(70); await page.keyboard.up('Tab'); await sleep(140); }
  await sleep(800);
  await page.screenshot({ path: path.join(outdir, `${tag}${profile}_kit.png`) });
  await sleep(2500);
  for (let c = 0; c < casts; c++) {
    await page.evaluate((n) => window.__marks.push(['cast' + n, performance.now()]), c + 1);
    await page.keyboard.down('KeyE'); await sleep(90); await page.keyboard.up('KeyE');
    if (c === casts - 1) { await sleep(560); await page.screenshot({ path: path.join(outdir, `${tag}${profile}_impact.png`) }); await sleep(2640); }
    else await sleep(3200);
  }
  const data = await page.evaluate(() => ({ raf: window.__raf, lt: window.__lt, marks: window.__marks, log: window.__log, lt_error: window.__lt_error || null }));
  // ---- analysis
  const raf = data.raf; const dts = [];
  for (let i = 1; i < raf.length; i++) dts.push([raf[i - 1], raf[i] - raf[i - 1]]);
  const castT = data.marks.map((m) => m[1]);
  const idle = dts.filter(([t]) => t > castT[0] - 2500 && t < castT[0] - 50).map(([, d]) => d).sort((a, b) => a - b);
  const med = idle.length ? idle[Math.floor(idle.length / 2)] : 16.7;
  const perCast = castT.map((tc, i) => {
    const w = dts.filter(([t]) => t >= tc && t < tc + 3000);
    const ds = w.map(([, d]) => d);
    const top = [...w].sort((a, b) => b[1] - a[1]).slice(0, 6).map(([t, d]) => [Math.round(t - tc), Math.round(d * 10) / 10]);
    const lt = data.lt.filter(([s]) => s >= tc - 20 && s < tc + 3000).map(([s, d]) => [Math.round(s - tc), d]);
    return { cast: i + 1, frames: w.length, max_ms: Math.round(Math.max(...ds) * 10) / 10,
      over_20: ds.filter((d) => d > 20).length, over_33: ds.filter((d) => d > 33.4).length, over_50: ds.filter((d) => d > 50).length,
      excess_over_idle_ms: Math.round(ds.reduce((a, d) => a + Math.max(0, d - med), 0)), top_frames_ms_after_cast: top, long_tasks: lt };
  });
  const report = { url, profile, viewport: [VW, VH], dpr: PHONE ? 3 : 1, cpu_throttle: profile === 'phone4x' ? 4 : 1,
    webgl_renderer: gl, canvas_px: canvas, idle_frame_median_ms: Math.round(med * 100) / 100,
    idle_frame_p95_ms: idle.length ? Math.round(idle[Math.floor(idle.length * 0.95)] * 100) / 100 : null,
    per_cast: perCast, errors: errors.slice(0, 20), lt_error: data.lt_error,
    diag_lines: data.log.filter(([, l]) => l.startsWith('[diag')).map(([t, l]) => [Math.round(t - (castT[0] || 0)), l]) };
  fs.writeFileSync(path.join(outdir, `${tag}${profile}_report.json`), JSON.stringify(report, null, 1));
  fs.writeFileSync(path.join(outdir, `${tag}${profile}_raw.json`), JSON.stringify(data));
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
