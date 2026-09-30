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

const only = process.argv[4] || 'both';
(async () => {
  // 1. PERF
  if (only !== 'look') {
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
  // 2. THE LOOK: one cast in film mode AT QUARTER SPEED (&slow=1), screenshots through it. The first
  // version shot at play speed and died at a screenshot ("Target page, context or browser has been
  // closed"); each shot is now caught, and the console is written whatever happens.
  if (only !== 'perf') {
    const { browser, page, logs } = await launch();
    await page.goto(base + 'index.html?meteor=film&slow=1', { waitUntil: 'load', timeout: 300000 });
    let trim = null;
    for (let i = 0; i < 2400 && !trim; i++) {
      // (by the key, not the line's start: the JSON's key order put "lit_at_target" first, the first look
      // pass never matched, and every screenshot landed after the cast had ended)
      trim = logs.find((l) => l.includes('[film] {') && l.includes('"trim_frames"'));
      if (!trim) await sleep(50);
    }
    // quarter speed: her release ~6.5 s after the cast, the impact ~9.8 s, the burn to ~21.8 s
    const shots = [6600, 7400, 8200, 9000, 9500, 9900, 10500, 11600, 15000, 20000];
    const tStart = Date.now();
    const got = [];
    try {
      for (const [i, ms] of shots.entries()) {
        const wait = ms - (Date.now() - tStart);
        if (wait > 0) await sleep(wait);
        try {
          await page.screenshot({ path: path.join(outdir, `web_look_${String(i).padStart(2, '0')}_${ms}ms.png`) });
          got.push(ms);
        } catch (e) { logs.push(`[shot-failed ${ms}] ${e.message}`); }
      }
      await sleep(2000);
    } finally {
      fs.writeFileSync(path.join(outdir, 'film_console.txt'), logs.join('\n'));
      console.log(JSON.stringify({ look_shots: got, trim: trim || null }));
      try { await browser.close(); } catch (e) {}
    }
  }
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
