// web13 PRODUCTION A/B touch check. drax, 2026-09-19.
//
// Arm A = picker slot 12 = kit index 11 (blackwater_cocktail_e3, runtime body): cast EAST once.
// Arm B = picker slot 19 = kit index 18 (blackwater_cocktail_e3_V, video-spine flipbook body):
// cast EAST three times ~4 s apart.
//
// ⚑ THE KEEPER MOVES BETWEEN THE B CASTS. The local rehearsal cast all three from a standing
// position, so all three landed on the same point and merged into ONE scorch — which would have
// read the "three B scorches coexist" verdict as NO for a reason that has nothing to do with the
// kit. Between casts the Keeper walks NORTH (W) and then re-faces EAST with the briefest possible
// tap, so the three landing points are separated perpendicular to the cast direction.
//
// Phone-landscape 844x390 CSS px, dsf 2, hasTouch + isMobile. The CAST is a genuine CDP
// Input.dispatchTouchEvent and THE MOUSE IS NEVER MOVED, so keeper.gd's forward-aim touch branch
// is the branch under test. The overlay leaves the keyboard alone, so facing/walking by key is safe.
// usage: node touch_cast_blackwater_AB_prod.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'prod';
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
  const faceEast = async () => { await page.keyboard.down('KeyD'); await sleep(60); await page.keyboard.up('KeyD'); await sleep(500); };
  const walkNorth = async (ms) => { await page.keyboard.down('KeyW'); await sleep(ms); await page.keyboard.up('KeyW'); await sleep(400); };
  const cast = async (tag) => {
    await touch('touchStart', [{ x: 700, y: 314, id: 2 }]);
    for (let i = 0; i < 6; i++) await shot(`${tag}_f${i}`);
    await touch('touchEnd', []);
  };
  await shot('spawn');
  await faceEast();
  await shot('facing_east');   // pre-cast reference frame for the grey measure

  // ---- ARM A: slot 12 / index 11, blackwater_cocktail_e3 (runtime body) ----
  for (let i = 0; i < 11; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('A_kit_label');
  await cast('A_cast1');
  await sleep(4000);
  await shot('A_settle');

  // ---- ARM B: slot 19 / index 18, blackwater_cocktail_e3_V (video spine) ----
  for (let i = 0; i < 7; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('B_kit_label');
  for (let c = 0; c < 3; c++) {
    if (c > 0) { await walkNorth(700); await faceEast(); await shot(`B_moved${c + 1}`); }
    await cast(`B_cast${c + 1}`);
    await sleep(4000);
    await shot(`B_after${c + 1}`);
  }
  // Dense settle series: watch the pools die, the scorches persist, and how many coexist.
  for (let i = 0; i < 8; i++) { await sleep(2000); await shot(`B_settle_${i}`); }

  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `touchflags=${JSON.stringify(touchFlags)}`,
     ...responses, '--- console', ...logs].join('\n'));
  console.log(`done booted=${booted} boot_ms=${bootMs}`);
  console.log(logs.filter((l) => /error|warn|fail|invalid/i.test(l)).slice(0, 40).join('\n') || '(no error/warn console lines)');
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
