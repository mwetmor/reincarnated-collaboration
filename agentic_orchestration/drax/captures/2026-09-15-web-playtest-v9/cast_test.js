// Route to the practice dummies, Tab x7 to the 8th kit, cast at a dummy. drax, web9.
// usage: node cast_test.js <url> <outdir> <label>    env: AIM="730,327"
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
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const logs = []; const responses = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  page.on('response', (r) => { const u = r.url();
    if (/index\.(wasm|pck|js|html)|cliffside\/?$/.test(u)) responses.push(`${r.status()} ${r.headers()['content-type']} ${r.headers()['content-length'] || ''} ${u}`); });
  const hold = async (keys, ms, extra) => {
    if (extra) await page.keyboard.down(extra);
    for (const k of keys) await page.keyboard.down(k);
    await sleep(ms);
    for (const k of keys) await page.keyboard.up(k);
    if (extra) await page.keyboard.up(extra);
  };
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
  await page.screenshot({ path: path.join(outdir, `${label}_00_spawn.png`) });
  const TABS = Number(process.env.TABS || 7);
  for (let i = 0; i < TABS; i++) { await page.keyboard.press('Tab'); await sleep(250); }
  await page.screenshot({ path: path.join(outdir, `${label}_01_kit_label.png`) });
  await hold(['KeyD'], 6000, 'Shift');
  await hold(['KeyD', 'KeyW'], 16000, 'Shift');
  await hold(['KeyW'], 6000, 'Shift');
  await hold(['KeyD'], 1400, 'Shift');
  await page.screenshot({ path: path.join(outdir, `${label}_02_at_dummies.png`) });
  const aim = (process.env.AIM || '730,327').split(',').map(Number);
  await page.mouse.move(aim[0], aim[1]);
  await sleep(400);
  // Fire and grab a burst of frames back to back (headless readback is slow, so no sleeps).
  for (let shot = 0; shot < 4; shot++) {
    await page.keyboard.down('KeyE');
    for (let i = 0; i < 6; i++) await page.screenshot({ path: path.join(outdir, `${label}_03_cast_s${shot}f${i}.png`) });
    await page.keyboard.up('KeyE');
    await sleep(1200);
  }
  await page.screenshot({ path: path.join(outdir, `${label}_04_after.png`) });
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`),
    [`booted=${booted} boot_ms=${bootMs}`, `aim=${aim}`, ...responses, '--- console', ...logs].join('\n'));
  console.log(`booted=${booted} boot_ms=${bootMs}`);
  console.log(responses.join('\n'));
  console.log(logs.filter((l) => /error|fail/i.test(l)).slice(0, 20).join('\n'));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
