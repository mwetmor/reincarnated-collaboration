// web12 production touch check: Tab x9 -> kit index 9 (fire_bolt_e1_B), cast EAST from
// the clearing spawn, six back-to-back screenshots per cast (f2 catches the peak, f3 the
// residue). drax, 2026-09-17.
//
// Phone-landscape 844x390 CSS px, dsf 2, hasTouch + isMobile. The CAST is a genuine CDP
// Input.dispatchTouchEvent and THE MOUSE IS NEVER MOVED, so keeper.gd's touch branch
// (forward aim along facing) is the branch under test. Facing is set with the briefest
// possible keyboard walk tap; the overlay leaves the keyboard alone.
// usage: node touch_cast_firebolt_b.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'tcast';
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
  const touchFlags = await page.evaluate(() => ({
    maxTouchPoints: navigator.maxTouchPoints, ontouchstart: 'ontouchstart' in window,
    TouchEvent: typeof window.TouchEvent, ua: navigator.userAgent }));
  fs.writeFileSync(path.join(outdir, `${label}_touchflags.json`), JSON.stringify(touchFlags, null, 2));
  let n = 0;
  const shot = (tag) => page.screenshot({ path: path.join(outdir, `${label}_${String(++n).padStart(2, '0')}_${tag}.png`) });
  await shot('spawn');
  // Tab x9 -> kit index 9, fire_bolt_e1_B
  for (let i = 0; i < 9; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('kit_label');
  // face EAST with the briefest possible walk tap (~15 px of drift at 247 px/s)
  await page.keyboard.down('KeyD'); await sleep(60); await page.keyboard.up('KeyD');
  await sleep(500);
  await shot('facing_east');          // <- the pre-cast reference frame for the grey measure
  for (let c = 0; c < 3; c++) {
    await touch('touchStart', [{ x: 700, y: 314, id: 2 }]);
    for (let i = 0; i < 6; i++) await shot(`cast${c + 1}_f${i}`);
    await touch('touchEnd', []);
    await sleep(1800);
  }
  await shot('after');
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `touchflags=${JSON.stringify(touchFlags)}`,
     ...responses, '--- console', ...logs].join('\n'));
  console.log(`done booted=${booted} boot_ms=${bootMs}`);
  console.log(logs.filter((l) => /error|warn|fail|invalid/i.test(l)).slice(0, 30).join('\n') || '(no error/warn console lines)');
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
