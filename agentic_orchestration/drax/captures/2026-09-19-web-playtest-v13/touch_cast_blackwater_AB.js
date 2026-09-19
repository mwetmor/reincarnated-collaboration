// web13 A/B touch check: Tab x11 -> kit index 11 (blackwater_cocktail_e3, arm A, picker
// slot 12), cast EAST from the clearing spawn; then Tab x7 more -> kit index 18
// (blackwater_cocktail_e3_V, arm B, picker slot 19, the video-spine flipbook body), cast
// EAST three times ~4 s apart. Six back-to-back screenshots per cast, then a settle series
// after the third B cast so the scorch-persistence and three-coexist verdicts have frames.
// drax, 2026-09-19. Adapted from web12's touch_cast_firebolt_b.js.
//
// Phone-landscape 844x390 CSS px, dsf 2, hasTouch + isMobile. The CAST is a genuine CDP
// Input.dispatchTouchEvent and THE MOUSE IS NEVER MOVED, so keeper.gd's touch branch
// (forward aim along facing) is the branch under test. Facing is set with the briefest
// possible keyboard walk tap; the overlay leaves the keyboard alone.
// usage: node touch_cast_blackwater_AB.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'ab';
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
  const cast = async (tag) => {
    await touch('touchStart', [{ x: 700, y: 314, id: 2 }]);
    for (let i = 0; i < 6; i++) await shot(`${tag}_f${i}`);
    await touch('touchEnd', []);
  };
  await shot('spawn');
  // face EAST with the briefest possible walk tap (~15 px of drift at 247 px/s)
  await page.keyboard.down('KeyD'); await sleep(60); await page.keyboard.up('KeyD');
  await sleep(500);
  await shot('facing_east');   // <- the pre-cast reference frame for the grey measure

  // ---- ARM A: picker slot 12 = kit index 11, blackwater_cocktail_e3 (runtime body) ----
  for (let i = 0; i < 11; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('A_kit_label');
  await cast('A_cast1');
  await sleep(4000);
  await shot('A_settle');

  // ---- ARM B: picker slot 19 = kit index 18, blackwater_cocktail_e3_V (video spine) ----
  for (let i = 0; i < 7; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await shot('B_kit_label');
  for (let c = 0; c < 3; c++) {
    await cast(`B_cast${c + 1}`);
    await sleep(4000);
    await shot(`B_after${c + 1}`);
  }
  // settle series: the pools must die while the scorches stay, and all three must coexist
  for (let i = 0; i < 6; i++) { await sleep(2500); await shot(`B_settle_${i}`); }

  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `touchflags=${JSON.stringify(touchFlags)}`,
     ...responses, '--- console', ...logs].join('\n'));
  console.log(`done booted=${booted} boot_ms=${bootMs}`);
  console.log(logs.filter((l) => /error|warn|fail|invalid/i.test(l)).slice(0, 30).join('\n') || '(no error/warn console lines)');
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
