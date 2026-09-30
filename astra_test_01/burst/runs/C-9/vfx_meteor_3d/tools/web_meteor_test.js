// C-9 VFX BAKE-OFF, LANE B -- the Meteor test scene's web export, measured at PHONE SIZE in Chrome.
// From barrow_full/tools/web_painted_test.js: Chrome with its GPU (ANGLE on Metal), NOT SwiftShader;
// 844 x 390 CSS px at devicePixelRatio 3 (an iPhone 14 held landscape: the canvas renders 2532 x 1170),
// touch on. A FRESH browser profile per launch, so every shader is compiled cold.
//   PLAYWRIGHT_CORE=<playwright-core> node web_meteor_test.js <url-base> <outdir>
// Runs the scene's own perf harness (?meteor=perf: idle, the cold first cast, 20 casts with the effect,
// the same 20 without) and waits for its "[meteor_perf]" line; then, in a second fresh browser, the
// film mode (?meteor=film) once, with screenshots through the cast for the look.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');
const base = process.argv[2];
const outdir = process.argv[3];
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const VW = 844, VH = 390;

async function launch() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
    args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--window-size=900,480', '--window-position=40,40'],
  });
  const context = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  const page = await context.newPage();
  const logs = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  return { browser, page, logs };
}

(async () => {
  // 1. PERF
  {
    const { browser, page, logs } = await launch();
    const t0 = Date.now();
    await page.goto(base + 'index.html?meteor=perf', { waitUntil: 'load', timeout: 300000 });
    let line = null;
    for (let i = 0; i < 900 && !line; i++) {
      line = logs.find((l) => l.includes('[meteor_perf] '));
      if (!line) await sleep(500);
    }
    const gl = await page.evaluate(() => {
      const c = document.createElement('canvas').getContext('webgl2');
      if (!c) return 'no webgl2';
      const e = c.getExtension('WEBGL_debug_renderer_info');
      return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER);
    });
    const canvas = await page.evaluate(() => { const c = document.getElementById('canvas'); return c ? [c.width, c.height] : null; });
    const perf = line ? JSON.parse(line.slice(line.indexOf('[meteor_perf] ') + 14)) : null;
    const ready = logs.find((l) => l.includes('[meteor_b] ready')) || null;
    fs.writeFileSync(path.join(outdir, 'perf.json'), JSON.stringify({ webgl_renderer: gl, canvas_px: canvas, wall_s: (Date.now() - t0) / 1000, ready, perf }, null, 1));
    fs.writeFileSync(path.join(outdir, 'perf_console.txt'), logs.join('\n'));
    console.log(JSON.stringify({ webgl_renderer: gl, canvas_px: canvas, got_perf: !!perf,
      errors: logs.filter((l) => /\[error\]|pageerror|SCRIPT ERROR|SHADER ERROR/i.test(l)).slice(0, 20) }, null, 1));
    await browser.close();
  }
  // 2. THE LOOK: one cast in film mode, screenshots through it
  {
    const { browser, page, logs } = await launch();
    await page.goto(base + 'index.html?meteor=film', { waitUntil: 'load', timeout: 300000 });
    let trim = null;
    for (let i = 0; i < 600 && !trim; i++) {
      trim = logs.find((l) => l.includes('[film] {"trim_frames"'));
      if (!trim) await sleep(250);
    }
    // the cast starts ~8 frames after the trim line; her release is 1.625 s into the clip
    const shots = [1500, 1850, 2150, 2350, 2500, 2650, 2900, 3600, 5000];
    const tStart = Date.now();
    for (const [i, ms] of shots.entries()) {
      const wait = ms - (Date.now() - tStart);
      if (wait > 0) await sleep(wait);
      await page.screenshot({ path: path.join(outdir, `web_look_${String(i).padStart(2, '0')}_${ms}ms.png`) });
    }
    await sleep(3000);
    fs.writeFileSync(path.join(outdir, 'film_console.txt'), logs.join('\n'));
    await browser.close();
  }
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
