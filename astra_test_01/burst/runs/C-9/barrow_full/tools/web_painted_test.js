// C-9 T10-2 -- the PAINTED Barrow's phone page (/playtest/barrow-painted/), measured at phone size in a desktop browser.
// A copy of cliffside3d/tools/web_barrow_test.js; what differs: the page, and the scene's own
// "[barrow_painted] web:" line as the moment it is built.
//
//   PLAYWRIGHT_CORE=<playwright-core> node web_barrow_test.js <url> <outdir> [wifi_mbps]
//
// Chrome with its GPU (ANGLE on Metal), NOT SwiftShader: a frame-rate from a software
// renderer is a number about the CPU. The page is 844 x 390 CSS px at devicePixelRatio 3, an
// iPhone 14 held landscape (the canvas renders at 2532 x 1170), touch on, ?touch=1&fps=1.
//
// LOAD: the network is throttled to a Wi-Fi link (default 40 Mbit/s down, 20 ms) through CDP,
// the cache disabled, and the clock runs from navigation to (a) the engine's loading overlay
// going away and (b) the scene's own "[barrow_painted] web:" line -- the moment the Barrow is built.
// Serve it brotli-encoded as Vercel does (scratch br_server.js), or the transfer is the raw size.
// FRAME RATE: the scene prints "[fps] N" every 2 s (?fps=1); samples are tagged by what the
// knight was doing -- standing, walking on the thumb stick, striking.
// CONTROLS: the stick, then SLASH, CHOP, BASH, BLOCK (held) and GEAR, each tapped at its own
// centre -- computed from barrow_touch.gd's anchors through the 1920 x 1080 canvas, which the
// [display] stretch fits inside the phone's 844 x 390 with pillarboxes -- and each checked in
// the console (the clip set changing for GEAR) or by a screenshot.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');

const url = process.argv[2];
const outdir = process.argv[3];
const mbps = parseFloat(process.argv[4] || '40');
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const VW = 844, VH = 390;
// barrow_touch.gd BUTTONS: anchor from the canvas's bottom-right corner, 1920 x 1080 base
const BUTTONS = { SLASH: [-205, -225], CHOP: [-445, -150], BASH: [-195, -480], BLOCK: [-430, -385], GEAR: [-120, -960] };
const scale = Math.min(VW / 1920, VH / 1080);
const padX = (VW - 1920 * scale) / 2, padY = (VH - 1080 * scale) / 2;
const at = (a) => ({ x: padX + (1920 + a[0]) * scale, y: padY + (1080 + a[1]) * scale });

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
    args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--window-size=900,480', '--window-position=40,40'],
  });
  const context = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  // IN-PAGE CLOCKS. Polling the overlay from outside reads late -- page.evaluate waits while the
  // engine holds the main thread building the scene -- so the page times itself: when the pck
  // and the wasm finished arriving, when the engine printed its first line, when the loading
  // overlay went away, and when the scene printed "[barrow_painted] web:".
  await context.addInitScript(() => {
    window.__t = {};
    const mark = (k) => { if (!(k in window.__t)) window.__t[k] = Math.round(performance.now()); };
    const log = console.log.bind(console);
    console.log = (...a) => {
      const s = String(a[0]);
      if (s.startsWith('Godot Engine v')) mark('engine_first_line');
      if (s.startsWith('[barrow_painted] web:')) mark('barrow_built');
      return log(...a);
    };
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        const n = e.name.split('/').pop().split('?')[0];
        if (n === 'index.wasm' || n === 'index.pck') mark(n + '_arrived');
      }
    }).observe({ type: 'resource', buffered: true });
    const watch = () => {
      const s = document.getElementById('status');
      // the shell REMOVES the overlay when the engine has started (statusOverlay.remove())
      if (!s || getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden') { mark('overlay_gone'); return; }
      requestAnimationFrame(watch);
    };
    addEventListener('DOMContentLoaded', () => requestAnimationFrame(watch));
  });
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false, latency: 20, downloadThroughput: (mbps * 1e6) / 8, uploadThroughput: (10 * 1e6) / 8,
  });
  const logs = [];
  const fps = [];
  let phase = 'loading';
  let builtAt = 0;
  const t0 = Date.now();
  page.on('console', (m) => {
    const s = m.text();
    logs.push(`[${m.type()}] ${s}`);
    const f = s.match(/^\[fps\] (\d+)/);
    if (f) fps.push({ t: Date.now() - t0, phase, fps: parseInt(f[1], 10) });
    if (!builtAt && s.startsWith('[barrow_painted] web:')) builtAt = Date.now() - t0;
  });
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  const files = {};
  cdp.on('Network.loadingFinished', (e) => { if (files[e.requestId]) files[e.requestId].transferred = e.encodedDataLength; });
  cdp.on('Network.responseReceived', (e) => {
    const u = e.response.url;
    if (/\/playtest\/barrow-painted\//.test(u)) {
      files[e.requestId] = { file: u.split('/').pop().split('?')[0] || 'index.html', status: e.response.status,
        encoding: (e.response.headers['content-encoding'] || e.response.headers['Content-Encoding'] || '-') };
    }
  });
  await page.goto(url, { waitUntil: 'load', timeout: 300000 });
  let overlayGoneAt = 0;
  for (let i = 0; i < 600; i++) {
    const gone = await page.evaluate(() => {
      const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true;
    });
    if (gone) { overlayGoneAt = Date.now() - t0; break; }
    await sleep(500);
  }
  for (let i = 0; i < 240 && !builtAt; i++) await sleep(500);
  const gl = await page.evaluate(() => {
    const c = document.createElement('canvas').getContext('webgl2');
    if (!c) return 'no webgl2';
    const e = c.getExtension('WEBGL_debug_renderer_info');
    return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER);
  });
  const canvas = await page.evaluate(() => { const c = document.getElementById('canvas'); return c ? [c.width, c.height] : null; });
  phase = 'standing';
  await sleep(4000);
  await page.screenshot({ path: path.join(outdir, '01_built.png') });
  await sleep(8000);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  const tap = async (name, holdMs = 150) => {
    const p = at(BUTTONS[name]);
    await touch('touchStart', [{ x: p.x, y: p.y, id: 7 }]); await sleep(holdMs); await touch('touchEnd', []);
  };
  // walk: the stick pushed up-right, past the run threshold for the second half
  phase = 'walking';
  await touch('touchStart', [{ x: 140, y: 300, id: 1 }]);
  for (let k = 1; k <= 10; k++) { await touch('touchMove', [{ x: 140 + k * 3, y: 300 - k * 2.5, id: 1 }]); await sleep(30); }
  await sleep(4000);
  await page.screenshot({ path: path.join(outdir, '02_walking.png') });
  for (let k = 11; k <= 20; k++) { await touch('touchMove', [{ x: 140 + k * 3, y: 300 - k * 2.5, id: 1 }]); await sleep(30); }
  await sleep(4000);
  await page.screenshot({ path: path.join(outdir, '03_running.png') });
  await touch('touchEnd', []);
  await sleep(800);
  phase = 'striking';
  await tap('SLASH'); await sleep(350); await page.screenshot({ path: path.join(outdir, '04_slash.png') }); await sleep(1600);
  await tap('CHOP'); await sleep(450); await page.screenshot({ path: path.join(outdir, '05_chop.png') }); await sleep(1800);
  await tap('BASH'); await sleep(300); await page.screenshot({ path: path.join(outdir, '06_bash.png') }); await sleep(1600);
  { const p = at(BUTTONS.BLOCK); await touch('touchStart', [{ x: p.x, y: p.y, id: 8 }]); await sleep(900);
    await page.screenshot({ path: path.join(outdir, '07_block_held.png') }); await sleep(2000); await touch('touchEnd', []); }
  await sleep(1000);
  const clipLinesBefore = logs.filter((l) => l.includes('clip set ->')).length;
  await tap('GEAR'); await sleep(1500);
  const clipLinesAfter = logs.filter((l) => l.includes('clip set ->')).length;
  await page.screenshot({ path: path.join(outdir, '08_after_gear.png') });
  phase = 'after';
  await sleep(2500);
  const inPage = await page.evaluate(() => window.__t);
  const byPhase = {};
  for (const s of fps) (byPhase[s.phase] = byPhase[s.phase] || []).push(s.fps);
  const report = {
    url, wifi_mbps: mbps, webgl_renderer: gl, canvas_px: canvas, buttons_css_px: Object.fromEntries(Object.entries(BUTTONS).map(([k, a]) => [k, at(a)])),
    in_page_ms_from_navigation: inPage,
    polled_ms_overlay_gone: overlayGoneAt, polled_ms_barrow_built: builtAt,
    fps_by_phase: byPhase, fps_samples: fps,
    gear_tap_changed_clip_set: clipLinesAfter > clipLinesBefore,
    files: Object.values(files),
    webgl_perf_warnings: logs.filter((l) => l.includes('READ-usage buffer')).length,
    errors: logs.filter((l) => /\[error\]|pageerror|SCRIPT ERROR|SHADER ERROR|failed/i.test(l)).slice(0, 40),
  };
  fs.writeFileSync(path.join(outdir, 'report.json'), JSON.stringify(report, null, 1));
  fs.writeFileSync(path.join(outdir, 'console.txt'), logs.join('\n'));
  console.log(JSON.stringify({ ...report, fps_samples: undefined }, null, 1));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
