// Production touch-emulated cast of the 8th kit (Tab x7 = fire_burst_e0p_v2, now
// burst_v2 lap 3) at the brute training dummy. drax, web11.
//
// Phone-landscape 844x390 CSS px, dsf 2, hasTouch + isMobile. The CAST itself is a
// genuine CDP Input.dispatchTouchEvent and THE MOUSE IS NEVER MOVED, so keeper.gd's
// touch branch (forward aim along facing, range_px * art_scale = 650 * 0.6292 = 409 px)
// is the branch under test. Navigation and facing use the keyboard, which the overlay
// leaves untouched -- that buys positional precision so the 409 px forward point lands
// on dummy_brute_1 at world (4370.5, 494.9): the route parks the Keeper at (3961, 480).
// usage: PLAN='[["NE",0.2],...]' node touch_cast_dummy.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'tcast';
const plan = JSON.parse(process.env.PLAN || '[]');
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const KEYS = { N: ['KeyW'], S: ['KeyS'], E: ['KeyD'], W: ['KeyA'],
  NE: ['KeyW', 'KeyD'], NW: ['KeyW', 'KeyA'], SE: ['KeyS', 'KeyD'], SW: ['KeyS', 'KeyA'] };
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
  console.error('goto...');
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  let booted = false;
  for (let i = 0; i < 200; i++) {
    const hidden = await page.evaluate(() => { const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true; });
    if (hidden) { booted = true; break; } await sleep(1000);
  }
  const bootMs = Date.now() - t0;
  console.error('booted=' + booted + ' ' + bootMs + 'ms');
  await sleep(6000);
  const cdp = await context.newCDPSession(page);
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
  const touchFlags = await page.evaluate(() => ({
    maxTouchPoints: navigator.maxTouchPoints, ontouchstart: 'ontouchstart' in window,
    TouchEvent: typeof window.TouchEvent, ua: navigator.userAgent }));
  fs.writeFileSync(path.join(outdir, `${label}_touchflags.json`), JSON.stringify(touchFlags, null, 2));
  let n = 0;
  const shot = (tag) => page.screenshot({ path: path.join(outdir, `${label}_${String(++n).padStart(2, '0')}_${tag}.png`) });
  await shot('spawn');
  await page.keyboard.down('Shift');
  for (const [dir, secs] of plan) {
    const keys = KEYS[dir];
    for (const k of keys) await page.keyboard.down(k);
    await sleep(Math.round(secs * 1000));
    for (const k of keys) await page.keyboard.up(k);
  }
  await page.keyboard.up('Shift');
  await sleep(600);
  await shot('in_position');
  // Tab x7 -> the 8th kit, fire_burst_e0p_v2
  for (let i = 0; i < 7; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('kit_label');
  // face EAST with the briefest possible walk tap (~15 px of drift at 247 px/s)
  await page.keyboard.down('KeyD'); await sleep(60); await page.keyboard.up('KeyD');
  await sleep(400);
  await shot('facing_east');
  for (let c = 0; c < 3; c++) {
    await touch('touchStart', [{ x: 700, y: 314, id: 2 }]);
    for (let i = 0; i < 6; i++) await shot(`cast${c + 1}_f${i}`);
    await touch('touchEnd', []);
    await sleep(1600);
  }
  await shot('after');
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `touchflags=${JSON.stringify(touchFlags)}`,
     `plan=${JSON.stringify(plan)}`, ...responses, '--- console', ...logs].join('\n'));
  console.log(`done booted=${booted} touchflags=${JSON.stringify(touchFlags)}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
