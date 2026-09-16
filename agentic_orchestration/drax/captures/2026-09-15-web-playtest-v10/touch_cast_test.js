// F-C5-5 verification: does a REAL touch-emulated cast aim FORWARD along facing?
// Phone-landscape 844x390 CSS px, hasTouch + isMobile, CDP touch events only.
// Two casts: facing EAST (as dispatched) and facing WEST (the decisive one --
// the CAST button sits bottom-RIGHT, so an emulated-mouse aim lands right/behind
// while a forward aim lands left). drax, web10.
// usage: node touch_cast_test.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'live';
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  const context = await browser.newContext({
    viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const page = await context.newPage();
  const logs = []; const responses = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  page.on('response', (r) => { const u = r.url();
    if (/index\.(wasm|pck|js|html)|cliffside\/?$/.test(u)) responses.push(`${r.status()} ${r.headers()['content-type']} ${r.headers()['content-length'] || ''} ${u}`); });
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  let booted = false;
  for (let i = 0; i < 200; i++) {
    const hidden = await page.evaluate(() => { const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true; });
    if (hidden) { booted = true; break; } await sleep(1000);
  }
  const bootMs = Date.now() - t0;
  await sleep(6000);
  const cdp = await context.newCDPSession(page);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  // Does the build itself think this is a touchscreen? (what keeper.gd branches on)
  const touchFlags = await page.evaluate(() => ({
    maxTouchPoints: navigator.maxTouchPoints, ontouchstart: 'ontouchstart' in window,
    TouchEvent: typeof window.TouchEvent, ua: navigator.userAgent }));
  fs.writeFileSync(path.join(outdir, `${label}_touchflags.json`), JSON.stringify(touchFlags, null, 2));
  // Never move the mouse. If an emulated mouse exists it is whatever the browser last said.
  const TABS = Number(process.env.TABS || 7);
  for (let i = 0; i < TABS; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await page.screenshot({ path: path.join(outdir, `${label}_00_kit_label.png`) });

  // Drag the floating joystick (left half) to set facing, then release.
  const face = async (dx, dy, ms) => {
    await touch('touchStart', [{ x: 170, y: 250, id: 1 }]);
    for (let k = 1; k <= 10; k++) { await touch('touchMove', [{ x: 170 + dx * k * 9, y: 250 + dy * k * 9, id: 1 }]); await sleep(40); }
    await sleep(ms);
    await touch('touchEnd', []);
    await sleep(300);
  };
  const castBurst = async (tag) => {
    await page.screenshot({ path: path.join(outdir, `${label}_${tag}_pre.png`) });
    for (let shot = 0; shot < 3; shot++) {
      await touch('touchStart', [{ x: 700, y: 314, id: 2 }]);
      for (let i = 0; i < 5; i++) await page.screenshot({ path: path.join(outdir, `${label}_${tag}_cast_s${shot}f${i}.png`) });
      await touch('touchEnd', []);
      await sleep(1400);
    }
  };
  await face(1, 0, 1200);   // east
  await castBurst('01_east');
  await sleep(1500);
  await face(-1, 0, 1200);  // west
  await castBurst('02_west');
  await sleep(1000);
  await page.screenshot({ path: path.join(outdir, `${label}_03_after.png`) });
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `touchflags=${JSON.stringify(touchFlags)}`, ...responses, '--- console', ...logs].join('\n'));
  console.log(`booted=${booted} boot_ms=${bootMs} touchflags=${JSON.stringify(touchFlags)}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
