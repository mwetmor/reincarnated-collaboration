// Verify the WHIRLWIND touch button is a HELD CHANNEL, not a tap.
//
// A screenshot of a spinning character proves nothing: a one-tick flash and a
// sustained channel look identical in a single frame. What separates them is
// how the frame keeps CHANGING while the pointer is down. So this measures
// per-frame churn -- the fraction of pixels that differ between consecutive
// screenshots -- in four phases:
//
//     idle      pointer up, character at rest      -> the noise floor
//     hold      pointer DOWN on WHIRLWIND, 8 samples over ~1.5 s
//     release   pointer up again                   -> must fall back to floor
//     combo     WHIRLWIND held + joystick pushed   -> must TRANSLATE
//
// A one-tick flash would show a single elevated sample at the start of `hold`
// and idle-level churn for the rest; a real channel holds elevated churn for
// every sample. That is the distinction the whole test exists to make, and it
// is why `hold` is sampled repeatedly rather than once.
//
// Also checks: the button is absent in a build with no attack action (pressing
// where it would be does nothing), a finger dragged off it releases the spin
// rather than leaving the player stuck, and the tap target clears 44 CSS px.
//
// usage: node verify_whirlwind_touch.js <base_url> <outdir>
//   env PLAYWRIGHT_CORE=<path to playwright-core>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');

const base = (process.argv[2] || '').replace(/\/$/, '');
const outdir = process.argv[3];
if (!base || !outdir) {
  console.error('usage: node verify_whirlwind_touch.js <base_url> <outdir>');
  process.exit(2);
}
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// The project's design viewport. project.godot declares 1920x1080 with
// canvas_items stretch and the default "keep" aspect, so the Godot viewport
// stays 1920x1080 and is letterboxed inside whatever the canvas is -- which is
// what lets a Godot-space button anchor be converted to a CSS tap point.
const VW = 1920;
const VH = 1080;

// Anchors are measured from the BOTTOM-RIGHT, matching touch_controls.gd.
const WHIRL_ANCHOR = { x: -390, y: -370, radius: 95 };
const JOY_HINT = { x: 260, yFromBottom: 250 };

async function shot(page) {
  return (await page.screenshot()).toString('base64');
}

async function diff(page, a, b) {
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

const median = (xs) => {
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.floor(s.length / 2)];
};

// Consecutive-frame churn over `count` samples at `gap` ms.
async function churn(page, count, gap) {
  const shots = [];
  for (let i = 0; i < count; i++) {
    shots.push(await shot(page));
    await sleep(gap);
  }
  const ds = [];
  for (let i = 1; i < shots.length; i++) ds.push(await diff(page, shots[i - 1], shots[i]));
  return ds;
}

async function boot(context, url) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  for (let i = 0; i < 300; i++) {
    const hidden = await page.evaluate(() => {
      const s = document.getElementById('status');
      return !s || getComputedStyle(s).display === 'none';
    });
    if (hidden) break;
    await sleep(500);
  }
  await sleep(6000);
  return { page, errors };
}

async function geometry(page) {
  const rect = await page.evaluate(() => {
    const c = document.getElementById('canvas');
    const r = c.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  const scale = Math.min(rect.w / VW, rect.h / VH);
  const offX = rect.x + (rect.w - VW * scale) / 2;
  const offY = rect.y + (rect.h - VH * scale) / 2;
  return {
    rect, scale,
    toCss: (vx, vy) => ({ x: offX + vx * scale, y: offY + vy * scale }),
  };
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  const results = [];
  let failures = 0;
  const record = (step, ok, detail) => {
    if (!ok) failures++;
    results.push({ step, ok, ...detail });
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${step}`);
    console.log('   ' + JSON.stringify(detail));
  };

  // ------------------------------------------------ WARLORD: the held channel
  {
    const ctx = await browser.newContext({
      viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    });
    const { page, errors } = await boot(ctx, `${base}/playtest/cliffside/?c=warlord&touch=1`);
    const geo = await geometry(page);
    const whirl = geo.toCss(VW + WHIRL_ANCHOR.x, VH + WHIRL_ANCHOR.y);
    const joy = geo.toCss(JOY_HINT.x, VH - JOY_HINT.yFromBottom);
    const tapPx = WHIRL_ANCHOR.radius * 2 * geo.scale;
    const cdp = await ctx.newCDPSession(page);
    const touch = (type, points) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: points });

    await page.screenshot({ path: path.join(outdir, 'warlord_00_controls.png') });

    const idle = await churn(page, 7, 150);

    // HOLD. One finger down on WHIRLWIND, held across many sampled frames.
    await touch('touchStart', [{ x: whirl.x, y: whirl.y, id: 1 }]);
    await sleep(150);
    const hold = await churn(page, 8, 150);
    await page.screenshot({ path: path.join(outdir, 'warlord_01_hold_late.png') });
    await touch('touchEnd', []);

    await sleep(900);
    const after = await churn(page, 7, 150);
    await page.screenshot({ path: path.join(outdir, 'warlord_02_released.png') });

    const mIdle = median(idle), mHold = median(hold), mAfter = median(after);
    // Every hold sample elevated -- not just the first. This is the clause that
    // a one-tick flash fails: a flash spikes sample 1 and then reads as idle.
    const everySampleElevated = hold.every((d) => d > mIdle * 2);
    record('warlord: WHIRLWIND is a HELD channel',
      mHold > mIdle * 3 && everySampleElevated && mAfter < mHold / 2 && errors.length === 0, {
        idleChurnMedian: +mIdle.toFixed(4),
        holdChurnMedian: +mHold.toFixed(4),
        afterReleaseChurnMedian: +mAfter.toFixed(4),
        holdSamples: hold.map((d) => +d.toFixed(4)),
        everyHoldSampleElevated: everySampleElevated,
        stoppedOnRelease: mAfter < mHold / 2,
        tapTargetCssPx: Math.round(tapPx),
        tapTargetClears44: tapPx >= 44,
        errors,
      });

    // COMBO. Whirlwind held on one finger, joystick pushed on another: must
    // walk AND spin. Measured as translation -- the follow camera repaints the
    // whole view, so this is a large, unambiguous diff versus a stationary spin.
    const beforeCombo = await shot(page);
    await touch('touchStart', [{ x: whirl.x, y: whirl.y, id: 1 }]);
    await sleep(120);
    await touch('touchStart', [
      { x: whirl.x, y: whirl.y, id: 1 },
      { x: joy.x, y: joy.y, id: 2 },
    ]);
    for (let k = 1; k <= 8; k++) {
      await touch('touchMove', [
        { x: whirl.x, y: whirl.y, id: 1 },
        { x: joy.x + k * 7, y: joy.y, id: 2 },
      ]);
      await sleep(30);
    }
    await sleep(1800);
    await page.screenshot({ path: path.join(outdir, 'warlord_03_combo_walk_spin.png') });
    const afterCombo = await shot(page);
    const comboDiff = await diff(page, beforeCombo, afterCombo);
    await touch('touchEnd', []);
    record('warlord: WHIRLWIND + joystick walks AND spins',
      comboDiff > 0.3, { comboTranslationDiff: +comboDiff.toFixed(3) });

    // DRAG-OFF. Press the button, slide the finger well clear, lift. The spin
    // must not survive -- a stuck channel is the failure this guards.
    await sleep(1200);
    await touch('touchStart', [{ x: whirl.x, y: whirl.y, id: 1 }]);
    await sleep(400);
    for (let k = 1; k <= 6; k++) {
      await touch('touchMove', [{ x: whirl.x, y: whirl.y - k * 25, id: 1 }]);
      await sleep(40);
    }
    await sleep(500);
    const draggedOff = await churn(page, 6, 150);
    await touch('touchEnd', []);
    await sleep(800);
    const settled = await churn(page, 6, 150);
    const mDragged = median(draggedOff), mSettled = median(settled);
    record('warlord: finger dragged OFF the button releases the spin',
      mDragged < mHold / 2 && mSettled < mHold / 2, {
        churnWhileDraggedOff: +mDragged.toFixed(4),
        churnAfterLift: +mSettled.toFixed(4),
        holdChurnForReference: +mHold.toFixed(4),
      });

    // Desktop keyboard F must still behave as a held channel.
    await sleep(600);
    const beforeKey = await shot(page);
    await page.keyboard.down('KeyF');
    await sleep(150);
    const keyHold = await churn(page, 6, 150);
    await page.keyboard.up('KeyF');
    const mKey = median(keyHold);
    record('warlord: keyboard F unchanged (still a held channel)',
      mKey > mIdle * 3, { keyboardHoldChurnMedian: +mKey.toFixed(4), idleChurnMedian: +mIdle.toFixed(4) });
    void beforeKey;

    await ctx.close();
  }

  // ------------------------------- KEEPER / NECRO: the button must be ABSENT
  for (const id of ['keeper', 'necro']) {
    const ctx = await browser.newContext({
      viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    });
    const { page, errors } = await boot(ctx, `${base}/playtest/cliffside/?c=${id}&touch=1`);
    const geo = await geometry(page);
    const whirl = geo.toCss(VW + WHIRL_ANCHOR.x, VH + WHIRL_ANCHOR.y);
    const cdp = await ctx.newCDPSession(page);
    await page.screenshot({ path: path.join(outdir, `${id}_00_controls.png`) });

    const idle = await churn(page, 6, 150);
    // Press exactly where the warlord's button lives. Nothing is there, so
    // nothing may happen -- and nothing may break either.
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: whirl.x, y: whirl.y, id: 1 }] });
    await sleep(200);
    const pressed = await churn(page, 6, 150);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await sleep(600);
    await page.screenshot({ path: path.join(outdir, `${id}_01_pressed_empty_spot.png`) });
    const mIdle = median(idle), mPressed = median(pressed);
    record(`${id}: no WHIRLWIND button, and pressing its spot is inert`,
      mPressed < Math.max(0.01, mIdle * 3) && errors.length === 0, {
        idleChurnMedian: +mIdle.toFixed(4),
        churnWhilePressingEmptySpot: +mPressed.toFixed(4),
        errors,
      });
    await ctx.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(outdir, 'whirlwind.json'), JSON.stringify(results, null, 2));
  console.log(failures === 0 ? '\nALL PASS' : `\n${failures} FAILING STEP(S)`);
  process.exit(failures === 0 ? 0 : 1);
})().catch((e) => { console.error('VERIFY_FAILED', e); process.exit(1); });
