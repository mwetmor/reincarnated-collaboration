// Verify the three-pck cliffside trio ACTUALLY RUNS before it is deployed.
//
// "It imported cleanly" and "it exported without error" are not "it plays".
// This drives a real Chrome against a real server and checks, per character:
//
//   1. the correct .pck was fetched and the OTHER TWO were not (the whole point
//      of the pre-boot select is that you download one character, so if all
//      three packs were fetched the architecture has silently failed);
//   2. Godot booted (the status overlay went away) with no page errors;
//   3. the scene is actually DRAWN, not a black canvas -- measured as the
//      fraction of non-background pixels in the rendered frame;
//   4. holding a movement key CHANGES the frame (the camera follows the
//      character, so a moving character repaints most of the view);
//   5. F behaves: for the warlord it changes the frame (attack + whirlwind);
//      for the other two it does NOTHING and throws NOTHING -- and the page is
//      still responsive to movement afterwards, which is the real proof that
//      "F does nothing" means degraded, not broken;
//   6. the "Change character" chip is present and points at /play.
//
// For the necromancer it additionally captures Godot's own
// "Missing animation <x>; using <y>" console line, which is the engine
// reporting its nearest-direction fallback in its own words.
//
// usage: node verify_trio.js <base_url> <outdir>
//   env PLAYWRIGHT_CORE=<path to playwright-core>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');

const base = (process.argv[2] || '').replace(/\/$/, '');
const outdir = process.argv[3];
if (!base || !outdir) {
  console.error('usage: node verify_trio.js <base_url> <outdir>');
  process.exit(2);
}
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const CHARS = [
  { id: 'warlord', label: 'Warlord', attacks: true },
  { id: 'keeper', label: 'Keeper', attacks: false },
  { id: 'necro', label: 'Necromancer', attacks: false },
];

// Fraction of pixels differing by more than a small threshold, between two PNG
// screenshots. Decoded via the browser itself so no image library is needed.
async function frameDiff(page, a, b) {
  return page.evaluate(async ([pa, pb]) => {
    const load = (d) => new Promise((res) => {
      const i = new Image();
      i.onload = () => res(i);
      i.src = 'data:image/png;base64,' + d;
    });
    const [ia, ib] = await Promise.all([load(pa), load(pb)]);
    const w = Math.min(ia.width, ib.width);
    const h = Math.min(ia.height, ib.height);
    const grab = (img) => {
      const c = document.createElement('canvas');
      c.width = w; c.height = h;
      c.getContext('2d').drawImage(img, 0, 0);
      return c.getContext('2d').getImageData(0, 0, w, h).data;
    };
    const da = grab(ia), db = grab(ib);
    let n = 0;
    for (let i = 0; i < da.length; i += 4) {
      if (Math.abs(da[i] - db[i]) + Math.abs(da[i + 1] - db[i + 1]) + Math.abs(da[i + 2] - db[i + 2]) > 24) n++;
    }
    return n / (w * h);
  }, [a, b]);
}

// Fraction of pixels that are not the near-black clear colour -- a black canvas
// would pass a "booted" check while drawing nothing at all.
async function drawnFraction(page, shot) {
  return page.evaluate(async (d) => {
    const img = await new Promise((res) => {
      const i = new Image();
      i.onload = () => res(i);
      i.src = 'data:image/png;base64,' + d;
    });
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    c.getContext('2d').drawImage(img, 0, 0);
    const px = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 0; i < px.length; i += 4) {
      if (px[i] + px[i + 1] + px[i + 2] > 60) n++;
    }
    return n / (c.width * c.height);
  }, shot);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  const results = [];
  let failures = 0;

  // ---- the React select screen -----------------------------------------
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(`${base}/play`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(800);
    const cards = await page.$$eval('a[href^="/playtest/cliffside/?c="]', (as) => as.map((a) => a.getAttribute('href')));
    const necroCaveat = await page.evaluate(() => document.body.innerText.includes('north-east and north-west were never drawn'));
    // Portraits live at /characters/, deliberately NOT /play/ -- a public/play/
    // directory sitting next to the /play SPA route is exactly the collision a
    // static host can resolve the wrong way (directory before rewrite).
    const portraits = await page.$$eval('img[src^="/characters/"]', (imgs) => imgs.map((i) => `${i.getAttribute('src')}:${i.naturalWidth}x${i.naturalHeight}`));
    await page.screenshot({ path: path.join(outdir, 'select_mobile_390.png'), fullPage: true });
    const ok = cards.length === 3 && necroCaveat && portraits.every((p) => !p.endsWith(':0x0')) && errors.length === 0;
    if (!ok) failures++;
    results.push({ step: '/play select screen', ok, cards, necroCaveat, portraits, errors });
    await ctx.close();
  }

  // ---- each character ---------------------------------------------------
  for (const ch of CHARS) {
    const ctx = await browser.newContext({ viewport: { width: 1024, height: 640 }, hasTouch: true });
    const page = await ctx.newPage();
    const errors = [];
    const consoleLines = [];
    const packs = [];
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => consoleLines.push(`[${m.type()}] ${m.text()}`));
    page.on('response', (r) => {
      const m = r.url().match(/\/([a-z]+)\.pck$/);
      if (m) packs.push(`${m[1]}:${r.status()}`);
    });

    const t0 = Date.now();
    await page.goto(`${base}/playtest/cliffside/?c=${ch.id}`, { waitUntil: 'load', timeout: 180000 });
    let booted = false;
    for (let i = 0; i < 240; i++) {
      booted = await page.evaluate(() => {
        const s = document.getElementById('status');
        return !s || getComputedStyle(s).display === 'none';
      });
      if (booted) break;
      await sleep(500);
    }
    const bootMs = Date.now() - t0;
    await sleep(5000);

    const shotIdle = (await page.screenshot({ path: path.join(outdir, `${ch.id}_01_idle.png`) })).toString('base64');
    const drawn = await drawnFraction(page, shotIdle);

    // Movement: hold left (west) -- the camera follows, so the frame repaints.
    await page.keyboard.down('KeyA');
    await sleep(1800);
    const shotMove = (await page.screenshot({ path: path.join(outdir, `${ch.id}_02_move_west.png`) })).toString('base64');
    await page.keyboard.up('KeyA');
    const moveDiff = await frameDiff(page, shotIdle, shotMove);

    await sleep(1200);

    // --- the F check, and a note on why it is shaped like this -------------
    // The warlord's attack is a HELD channel, not a tap: keeper.gd drops back
    // to idle the moment `Input.is_action_pressed("attack")` goes false, which
    // is a Cyclone/Whirlwind-style trade, deliberately. A `keyboard.press()`
    // is down+up inside one frame, so it reads as "released" on the very next
    // physics tick and NOTHING happens -- the first version of this test
    // reported the warlord's attack broken when it was the probe that was.
    // So: hold it.
    //
    // It also needs a noise floor. The idle animation alone repaints ~0.3% of
    // the frame, so a bare "> 1%" threshold cannot tell "attack fired" from
    // "character breathed". Measure the idle churn first and judge against it.
    const shotRestA = (await page.screenshot()).toString('base64');
    await sleep(700);
    const shotRestB = (await page.screenshot()).toString('base64');
    const idleNoise = await frameDiff(page, shotRestA, shotRestB);

    const shotRest = (await page.screenshot()).toString('base64');
    await page.keyboard.down('KeyF');
    await sleep(700);
    const shotF = (await page.screenshot({ path: path.join(outdir, `${ch.id}_03_F_held.png`) })).toString('base64');
    await sleep(500);
    await page.screenshot({ path: path.join(outdir, `${ch.id}_03b_F_held_late.png`) });
    await page.keyboard.up('KeyF');
    const fDiff = await frameDiff(page, shotRest, shotF);
    const errorsAfterF = errors.length;

    // Still alive after F? Move again -- this is what "degrades gracefully"
    // has to mean: not merely "no exception", but "the game kept working".
    await sleep(600);
    const shotBeforeMove2 = (await page.screenshot()).toString('base64');
    await page.keyboard.down('KeyD');
    await sleep(1500);
    const shotMove2 = (await page.screenshot({ path: path.join(outdir, `${ch.id}_04_move_east_after_F.png`) })).toString('base64');
    await page.keyboard.up('KeyD');
    const move2Diff = await frameDiff(page, shotBeforeMove2, shotMove2);

    // North: for the necromancer this is the missing-direction fallback.
    await page.keyboard.down('KeyW');
    await sleep(1500);
    await page.screenshot({ path: path.join(outdir, `${ch.id}_05_move_north.png`) });
    await page.keyboard.up('KeyW');
    await sleep(400);

    const chip = await page.evaluate(() => {
      const a = document.querySelector('#char-chip a');
      const who = document.querySelector('#char-chip .who');
      return a ? { href: a.getAttribute('href'), text: a.textContent.trim(), who: who ? who.textContent.trim() : null } : null;
    });

    const missingAnim = consoleLines.filter((l) => /Missing animation/.test(l));
    const wrongPacks = packs.filter((p) => !p.startsWith(ch.id));

    const checks = {
      booted,
      onlyItsOwnPack: packs.length > 0 && wrongPacks.length === 0,
      sceneDrawn: drawn > 0.25,
      movementChangedFrame: moveDiff > 0.05,
      // Warlord: the held channel must move the view well clear of idle churn
      // (the whirlwind travels at walk pace, so the follow camera repaints a
      // lot). Keeper/necro: F is an UNMAPPED key in their builds -- no attack
      // action exists at all -- so the frame must stay within idle churn.
      // The absolute floor is deliberately SMALL. The figure is ~95 px tall in
      // a 1024x640 view, so even a whirlwind that repaints everything around
      // the character touches only ~1-2% of the frame; a "surely 2%" floor
      // rejected a working attack on the first run. The load-bearing test is
      // the RATIO to that character's own idle churn, which separates cleanly:
      // warlord ~10x noise, keeper/necro ~2-3x (i.e. idle churn and nothing
      // else, which is exactly right -- F is not even a mapped action there).
      fBehaved: ch.attacks
        ? fDiff > Math.max(0.006, idleNoise * 4)
        : fDiff <= Math.max(0.01, idleNoise * 3),
      noNewErrorsOnF: errorsAfterF === 0,
      aliveAfterF: move2Diff > 0.05,
      chipPresent: !!chip && chip.href === '/play' && chip.who === ch.label,
      noPageErrors: errors.length === 0,
    };
    const ok = Object.values(checks).every(Boolean);
    if (!ok) failures++;
    results.push({
      step: `character ${ch.id}`, ok, checks,
      bootMs, packs, drawn: +drawn.toFixed(3),
      moveDiff: +moveDiff.toFixed(3), idleNoise: +idleNoise.toFixed(4),
      fDiff: +fDiff.toFixed(3), move2Diff: +move2Diff.toFixed(3),
      chip, missingAnimationLines: missingAnim.slice(0, 6), errors,
    });
    fs.writeFileSync(path.join(outdir, `${ch.id}_console.txt`), consoleLines.join('\n'));
    await ctx.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(outdir, 'verify.json'), JSON.stringify(results, null, 2));
  for (const r of results) {
    console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.step}`);
    console.log('   ' + JSON.stringify(r.checks || { cards: r.cards, necroCaveat: r.necroCaveat, portraits: r.portraits }));
    if (r.bootMs) console.log(`   bootMs=${r.bootMs} packs=${JSON.stringify(r.packs)} drawn=${r.drawn} moveDiff=${r.moveDiff} idleNoise=${r.idleNoise} fDiff=${r.fDiff} move2Diff=${r.move2Diff}`);
    if (r.missingAnimationLines && r.missingAnimationLines.length) console.log('   fallback: ' + r.missingAnimationLines.join(' | '));
    if (r.errors && r.errors.length) console.log('   ERRORS: ' + r.errors.join(' | '));
  }
  console.log(failures === 0 ? '\nALL PASS' : `\n${failures} FAILING STEP(S)`);
  process.exit(failures === 0 ? 0 : 1);
})().catch((e) => { console.error('VERIFY_FAILED', e); process.exit(1); });
