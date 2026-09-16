// Walk from spawn (2285.6, 2407.3) toward the bridge and photograph the
// necromancer FINAL master on the sand path at world (2650, 1950). drax, web10.
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
  const logs = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  for (let i = 0; i < 200; i++) {
    const hidden = await page.evaluate(() => { const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true; });
    if (hidden) break; await sleep(1000);
  }
  await sleep(6000);
  await page.screenshot({ path: path.join(outdir, `${label}_10_spawn.png`) });
  const hold = async (keys, ms, extra) => {
    if (extra) await page.keyboard.down(extra);
    for (const k of keys) await page.keyboard.down(k);
    await sleep(ms);
    for (const k of keys) await page.keyboard.up(k);
    if (extra) await page.keyboard.up(extra);
    await sleep(500);
  };
  for (let step = 1; step <= 5; step++) {
    await hold(['KeyD', 'KeyW'], 700, 'Shift');
    await page.screenshot({ path: path.join(outdir, `${label}_1${step}_walk_ne_${step}.png`) });
  }
  fs.writeFileSync(path.join(outdir, `${label}_necro_console.txt`), logs.join('\n'));
  console.log('done');
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
