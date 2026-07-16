#!/usr/bin/env node
// d6-verify-probe.mjs — headless CDP verification of the §9.6 D6 pass.
//
// v1.12 RE-HOME (drax, Matt-ruled 2026-07-16): ported from reincarnated-loadout with the
// interactive Build-Horizon package and RE-TARGETED at the glance preview. Edition-III
// content MOVES text/dots vs Edition-II, so legend placement RE-verifies here, never carries
// (the acc-67-v2 gate is the binding law). The subtitle now reads "Edition-III lattice · …".
//
// D7 HARDENING + RE-VERIFY (drax, Matt-ruled 2026-07-16; spec §9.7 owed items):
//   - VIEWPORTS now span the WIDE widths this pass exists for — 2560 + 1920 (the /atlas host
//     went FLUID this pass) + the prior 1440 + 1280 + 375. The acc-67-v2 gate binds all 5
//     widths × both skins (10 surfaces); wide widths are HALT-don't-shrink.
//   - SKIN FLIP hardened per §9.7: (1) the flip target is selected by CANVAS LABEL ('Light'
//     capitalized + aria-pressed="false"), NEVER by skin name (the names are inverted:
//     'archive'=dark lead, 'instrument'=light); (2) the flip WAIT polls for a STATE CHANGE
//     (plate fill DIFFERS from the pre-click dark fill), fail-loud on timeout — the old
//     wait-for-existence loop was satisfied instantly by the still-mounted dark svg and
//     silently re-measured dark as the '…-light' cell.
//
// Zero-dependency CDP client (Node 24 global WebSocket + fetch; system Chrome). Drives a
// running `vite preview` of the built bundle (the D4/D5 precedent — the *.vercel.app
// preview hits an SSO wall for headless CDP, so we verify the SAME built bundle locally).
//
// Acceptance (spec §9.6 items 66–68):
//   66 box==zoom: the FRAME rect x/y/w/h == fit box INSET 12u on all sides; ALL rendered
//      content sits INSIDE the drawn frame at mount + after skin flip; the fail-loud
//      frame-identification test is in the unit suite (ambiguous fixture RAISES).
//   67 legend-in-box: the legend node renders INSIDE the chart region (DOM containment);
//      no normal-flow band between header and region; placement bottom-RIGHT; and — per the
//      D6-b OCCLUSION LAW v2 (gandalf verify-gate finding 2026-07-15) — the legend overlay
//      rect intersects the screen-space bbox of ZERO in-artifact `<text>` node (±4px pad).
//      This is a CLASS invariant, not a list: title, poles, condensation key, footer honesty
//      block, points-denominator line, GHOST FIELD + graveyard annotations, and every
//      drill-in dot label — all `<text>` nodes with a nonzero bbox are checked. FAIL-LOUD
//      with the offending text content if any hit. Asserted at BOTH viewports (1440, 375)
//      and BOTH skins (default dark + flipped light). Non-binding (NOT checked): ghost-
//      lattice speckle + dashed boundary curves (blurred backdrop leaves them inferable;
//      text under a panel is information destroyed — that asymmetry is the law's rationale).
//      (galadriel still eyes-verifies the pixels — this probe reports + gates the geometry.)
//   68 subtitle: the header subtitle reads "Edition-III lattice · …" exactly once (no
//      "Edition-Edition"). Verbatim from atlas-interactive.json (no hardcoded edition literal).
//   + no-regression: plate == viewBox == fit box (D5 acc 63); svg width/height absent (64);
//     zero horizontal page overflow; wiring (chart↔table halo) still fires.
//
// Usage: node scripts/atlas/d6-verify-probe.mjs [--url http://localhost:4319] [--out DIR]
//   (glance vite preview defaults to :4173 — pass --url http://localhost:4173.)
//
// Contract: agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md §7.8

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const BASE_URL = getArg('--url', 'http://localhost:4319');
const OUT_DIR = getArg('--out', path.join(os.tmpdir(), 'drax-d6-receipts'));
fs.mkdirSync(OUT_DIR, { recursive: true });

// FRAME_INSET is the spec's ONE legislated number (§9.6 D6-a). The probe asserts against
// it independently of the source (this is the acceptance check, not the implementation).
const FRAME_INSET = 12;

// D7-a re-verify (Matt 2026-07-16): the /atlas host is now FLUID, so the region/legend
// geometry MOVES with viewport width — the whole point of this pass. The v2 occlusion law
// re-runs at the WIDE widths this pass exists for (2560, 1920) plus the prior desktop +
// mobile set (1440, 1280, 375). Wide widths are gated fail-loud; HALT-don't-shrink if a
// wide placement can't satisfy the law.
const VIEWPORTS = [
  { name: '2560', width: 2560, height: 1440 },
  { name: '1920', width: 1920, height: 1080 },
  { name: '1440', width: 1440, height: 900 },
  { name: '1280', width: 1280, height: 800 },
  { name: '375', width: 375, height: 812 },
];

// ---------- minimal CDP client over the DevTools WebSocket ----------
function cdpConnect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  const listeners = [];
  ws.addEventListener('message', (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    } else if (msg.method) {
      for (const l of listeners) l(msg);
    }
  });
  const ready = new Promise((res, rej) => {
    ws.addEventListener('open', () => res());
    ws.addEventListener('error', (e) => rej(new Error('ws error: ' + (e.message || e))));
  });
  const send = (method, params = {}, sessionId) =>
    new Promise((resolve, reject) => {
      const id = nextId++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  return { ws, ready, send, on: (fn) => listeners.push(fn) };
}

async function launchChrome(userDataDir) {
  const port = 9222 + Math.floor(Math.random() * 500);
  const proc = spawn(CHROME, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-gpu',
    'about:blank',
  ]);
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (r.ok) {
        const j = await r.json();
        return { proc, port, wsUrl: j.webSocketDebuggerUrl };
      }
    } catch {
      /* not up yet */
    }
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error('Chrome did not expose the debugging endpoint');
}

async function probeViewport(browser, vp, extras) {
  const { targetId } = await browser.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await browser.send('Target.attachToTarget', { targetId, flatten: true });
  const S = (method, params) => browser.send(method, params, sessionId);

  await S('Page.enable', {});
  await S('Runtime.enable', {});
  await S('Emulation.setDeviceMetricsOverride', {
    width: vp.width,
    height: vp.height,
    deviceScaleFactor: 1,
    mobile: false,
  });

  const evalJs = async (expression) => {
    const r = await S('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) {
      throw new Error(
        'eval exception: ' +
          (r.exceptionDetails.exception?.description || JSON.stringify(r.exceptionDetails))
      );
    }
    return r.result.value;
  };

  // v1.12 ROUTER ADAPTATION (mechanical): glance uses HASH routing (App.tsx parseHash),
  // not BrowserRouter — the atlas page is `#/atlas`, not `/atlas`. (loadout served `/atlas`
  // as a path route; the ported page is unchanged, only the host router differs.)
  await S('Page.navigate', { url: `${BASE_URL}/#/atlas` });
  await S('Page.loadEventFired', {}).catch(() => {});

  const measurement = await evalJs(`(async () => {
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));
    let svg = null;
    for (let i = 0; i < 150; i++) {
      svg = document.querySelector('.atlas-svg-host svg');
      if (svg && !svg.hasAttribute('width') && svg.getAttribute('viewBox') !== '0 0 1600 1200') break;
      await sleep(100);
    }
    if (!svg) return { error: 'no inlined svg' };

    const num = (s) => Number(s);
    const viewBox = svg.getAttribute('viewBox');
    const vbNums = viewBox.trim().split(/\\s+/).map(Number); // [minx,miny,w,h]

    // planeClip rect (D5 acc 63 no-regression).
    const clip = svg.querySelector('#planeClip rect');
    const clipAttrs = clip ? {
      x: clip.getAttribute('x'), y: clip.getAttribute('y'),
      width: clip.getAttribute('width'), height: clip.getAttribute('height'),
    } : null;

    // Direct-child rects: classify PLATE (native-dim originally → now fit box, filled) vs
    // FRAME (fill="none" + stroke). Report both for the receipt.
    const directRects = Array.from(svg.children).filter(el => el.tagName.toLowerCase() === 'rect');
    const rectInfo = directRects.map(el => ({
      x: el.getAttribute('x'), y: el.getAttribute('y'),
      width: el.getAttribute('width'), height: el.getAttribute('height'),
      fill: el.getAttribute('fill'), stroke: el.getAttribute('stroke'),
    }));
    const plate = rectInfo.find(r => r.fill && r.fill.toLowerCase() !== 'none');
    const frame = rectInfo.find(r => r.fill && r.fill.toLowerCase() === 'none' && r.stroke);

    // svg presentation attrs (D5 acc 64: ABSENT).
    const svgWidthAttr = svg.getAttribute('width');
    const svgHeightAttr = svg.getAttribute('height');

    // Page horizontal overflow.
    const de = document.documentElement;

    // ---- LEGEND containment (acc 67) ----
    // The legend is inside the chart region (aria-label). Find the legend by its
    // "Legend" text within the region; report DOM containment + geometry + corner.
    const region = document.querySelector('[aria-label="Build Horizon — full-horizon chart"]');
    const regionRect = region ? region.getBoundingClientRect() : null;
    // The legend wrapper is the absolutely-positioned overlay; find the element whose text
    // starts with "Legend" and that is a descendant of the region.
    let legendEl = null;
    if (region) {
      const candidates = Array.from(region.querySelectorAll('div,button'));
      legendEl = candidates.find(el => {
        const t = (el.textContent || '').trim();
        return /^Legend\\b/.test(t) && el.offsetParent !== null;
      }) || null;
    }
    const legendRect = legendEl ? legendEl.getBoundingClientRect() : null;
    const legendInRegionDom = !!(region && legendEl && region.contains(legendEl));
    // Geometric containment within the region bounds (with a 1px tolerance).
    let legendGeomInside = null, legendCorner = null, legendCoveragePct = null, legendCollapsed = null;
    if (regionRect && legendRect) {
      legendGeomInside =
        legendRect.left >= regionRect.left - 1 && legendRect.right <= regionRect.right + 1 &&
        legendRect.top >= regionRect.top - 1 && legendRect.bottom <= regionRect.bottom + 1;
      const nearLeft = (legendRect.left - regionRect.left) < regionRect.width * 0.25;
      const nearBottom = (regionRect.bottom - legendRect.bottom) < regionRect.height * 0.25;
      legendCorner = (nearLeft ? 'left' : 'right') + '-' + (nearBottom ? 'bottom' : 'top');
      legendCoveragePct = Math.round((legendRect.width / regionRect.width) * 1000) / 10;
      // Collapsed if the legend text is JUST "Legend" (+ maybe "N on") — no entry labels.
      const txt = (legendEl.textContent || '').replace(/\\s+/g, ' ').trim();
      legendCollapsed = !/Live Kits|Ghosts|Condensations|Graveyard/i.test(txt);
    }

    // ---- D6-b v2 TEXT-OCCLUSION (acc 67 v2) ----
    // The BINDING invariant: the legend overlay rect intersects the screen-space bbox of NO
    // in-artifact <text> node (±4px pad). Measure the legend's on-screen rect and EVERY svg
    // <text> node's bbox (getBoundingClientRect handles the viewBox→screen transform + the
    // region's proportional scaling for us), then compute padded intersections. A zero-area
    // text node (e.g. an empty label) is skipped. Report the full hit list with content so a
    // failure is self-describing. PAD is the spec's ±4px. NON-binding nodes (speckle, dashed
    // curves) are <path>/<circle>/<line>, never <text> — so scanning <text> only is exactly
    // the v2 binding set.
    const PAD = 4;
    const rectsIntersect = (a, b) =>
      a.left - PAD < b.right && a.right + PAD > b.left &&
      a.top - PAD < b.bottom && a.bottom + PAD > b.top;
    let textOcclusion = { legendRectPresent: !!legendRect, textNodes: 0, occlusions: [] };
    if (legendRect && svg) {
      const textNodes = Array.from(svg.querySelectorAll('text'));
      let counted = 0;
      const hits = [];
      for (const t of textNodes) {
        const tr = t.getBoundingClientRect();
        // Skip zero-area nodes (nothing rendered → nothing to occlude).
        if (tr.width <= 0 || tr.height <= 0) continue;
        counted++;
        if (rectsIntersect(legendRect, tr)) {
          hits.push({
            text: (t.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 80),
            bbox: { left: Math.round(tr.left), top: Math.round(tr.top), right: Math.round(tr.right), bottom: Math.round(tr.bottom) },
          });
        }
      }
      textOcclusion = {
        legendRectPresent: true,
        legendRect: { left: Math.round(legendRect.left), top: Math.round(legendRect.top), right: Math.round(legendRect.right), bottom: Math.round(legendRect.bottom) },
        textNodes: counted,
        pad: PAD,
        occlusions: hits,
        textOcclusions: hits.length,
      };
    }

    // Is there a normal-flow legend band BETWEEN the header and the region? (must be GONE)
    // Heuristic: any element with "Legend" text that is a SIBLING before the region (not a
    // descendant of it). Walk the region's preceding siblings for legend text.
    let bandBeforeRegion = false;
    if (region) {
      let node = region.previousElementSibling;
      while (node) {
        if (/\\bLegend\\b/.test(node.textContent || '') && /Live Kits|Ghosts|Condensations|Graveyard/i.test(node.textContent||'')) {
          bandBeforeRegion = true; break;
        }
        node = node.previousElementSibling;
      }
    }

    // ---- SUBTITLE (acc 68) ----
    const h1 = document.querySelector('h1');
    // The subtitle is the <p> right after the h1.
    const subtitleEl = h1 ? h1.nextElementSibling : null;
    const subtitleText = subtitleEl ? (subtitleEl.textContent || '').trim() : null;

    return {
      viewBox, vbNums, clipAttrs, rectInfo, plate, frame,
      svgWidthAttr, svgHeightAttr,
      page: { scrollW: de.scrollWidth, clientW: de.clientWidth, innerW: window.innerWidth },
      region: regionRect ? { width: regionRect.width, height: regionRect.height } : null,
      regionBorder: region ? getComputedStyle(region).borderTopColor : null,
      legend: {
        found: !!legendEl, inRegionDom: legendInRegionDom, geomInside: legendGeomInside,
        corner: legendCorner, coveragePct: legendCoveragePct, collapsed: legendCollapsed,
        bandBeforeRegion,
      },
      textOcclusion,
      subtitle: subtitleText,
    };
  })()`);

  const result = { viewport: vp.name, width: vp.width, ...measurement };

  // Frame-vs-fitbox-inset receipt (acc 66): frame attrs == viewBox inset 12u each side.
  if (!measurement.error && measurement.frame && measurement.vbNums) {
    const [minx, miny, w, h] = measurement.vbNums;
    const expected = {
      x: minx + FRAME_INSET,
      y: miny + FRAME_INSET,
      width: w - 2 * FRAME_INSET,
      height: h - 2 * FRAME_INSET,
    };
    const f = measurement.frame;
    const close = (a, b) => Math.abs(Number(a) - b) < 0.01;
    result.frameCheck = {
      frameAttrs: { x: f.x, y: f.y, width: f.width, height: f.height },
      expectedInset12: expected,
      matches:
        close(f.x, expected.x) && close(f.y, expected.y) &&
        close(f.width, expected.width) && close(f.height, expected.height),
      frameStroke: f.stroke,
    };
    // Plate == viewBox (D5 no-regression).
    if (measurement.plate) {
      const p = measurement.plate;
      result.plateCheck = {
        matchesViewBox:
          close(p.x, minx) && close(p.y, miny) && close(p.width, w) && close(p.height, h),
        plateFill: p.fill,
      };
    }
  }

  // Extras. `extras === 'full'` (1440): eyes-ref screenshots + wiring smoke + skin-flip.
  // `extras === 'flip'` (375): skin-flip + post-flip text-occlusion only (no heavy shots).
  // The DEFAULT-skin text-occlusion is already in `measurement` at EVERY viewport; the flip
  // adds the LIGHT-skin check so acc 67 v2 is proven at BOTH viewports × BOTH skins.
  if (extras && !measurement.error) {
    if (extras === 'full') {
      // Full-page screenshot for eyes reference (galadriel judges the pixels).
      const full = await S('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
      const fullPath = path.join(OUT_DIR, `d6-atlas-${vp.name}-full.png`);
      fs.writeFileSync(fullPath, Buffer.from(full.data, 'base64'));
      result.fullScreenshot = fullPath;

      // Corner crops — bottom-RIGHT is where the legend NOW sits (v2 occlusion eyes-ref);
      // bottom-left / top-left / top-right kept so the footer honesty block (now UN-occluded,
      // bottom-left) + title + condensation key are all eyes-checkable.
      const regionBox = await evalJs(`(() => {
        const region = document.querySelector('[aria-label="Build Horizon — full-horizon chart"]');
        const r = region.getBoundingClientRect();
        return { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
      })()`);
      const cropW = Math.min(480, regionBox.w - 2);
      const cropH = Math.min(360, regionBox.h - 2);
      for (const c of [
        { tag: 'bottomright', x: regionBox.x + regionBox.w - cropW - 1, y: regionBox.y + regionBox.h - cropH - 1 },
        { tag: 'bottomleft', x: regionBox.x + 1, y: regionBox.y + regionBox.h - cropH - 1 },
        { tag: 'topleft', x: regionBox.x + 1, y: regionBox.y + 1 },
        { tag: 'topright', x: regionBox.x + regionBox.w - cropW - 1, y: regionBox.y + 1 },
      ]) {
        const shot = await S('Page.captureScreenshot', {
          format: 'png',
          captureBeyondViewport: true,
          clip: { x: c.x, y: c.y, width: cropW, height: cropH, scale: 1 },
        });
        fs.writeFileSync(path.join(OUT_DIR, `d6-atlas-cornercrop-${c.tag}.png`), Buffer.from(shot.data, 'base64'));
      }

      // Wiring smoke: chart mark → selection + halo (chart↔table still fires post-D6).
      result.wiring = await evalJs(`(async () => {
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        const out = {};
        const kitMark = document.querySelector('.atlas-svg-host svg [data-kit]');
        out.markFound = !!kitMark;
        if (kitMark) {
          const kid = kitMark.getAttribute('data-kit');
          kitMark.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          await sleep(160);
          out.selectionShown = /build ·/.test(document.body.textContent || '');
          const styleText = Array.from(document.querySelectorAll('style')).map(s=>s.textContent).join('\\n');
          out.haloRuleForKit = styleText.includes('[data-kit="'+kid+'"]');
          out.markStrokeWidth = getComputedStyle(kitMark).strokeWidth;
        }
        return out;
      })()`);
    }

    // Skin flip re-apply (acc 66 "after skin flip") + LIGHT-skin text-occlusion (acc 67 v2):
    // frame + plate re-written on flip AND the legend still hits ZERO <text> bbox in light.
    //
    // D7-c HARDENING (spec §9.7, ratified 2026-07-15 skin-name inversion; Matt 2026-07-16):
    //   (1) SELECT BY CANVAS LABEL, NEVER BY SKIN NAME. The AtlasSkinToggle renders the
    //       CAPITALIZED canvas word ('Dark'/'Light') as a bare text node + the lowercase
    //       skin name ('archive'/'instrument') in a muted <span>. The names are INVERTED
    //       ('archive'=dark lead, 'instrument'=light), so matching on skin name is a trap.
    //       We target the button carrying the capitalized 'Light' label (case-sensitive
    //       substring — the lowercase skin spans + the legend/filter labels contain no
    //       capital-run 'Light'/'Dark') that is currently aria-pressed="false" (i.e. the
    //       not-yet-active canvas = the flip target).
    //   (2) WAIT FOR A STATE CHANGE, NOT FOR EXISTENCE. The old skin's <svg> stays mounted
    //       through the flip until the new-canvas markup fetches + re-inlines, so a
    //       wait-for-"an svg exists with a non-seed viewBox" loop is satisfied INSTANTLY by
    //       the STILL-DARK svg — that silently re-measured dark as the '…-light' cell in the
    //       v1.12 pass. We snapshot the PRE-CLICK plate fill (the dark canvas hex) and poll
    //       until the mounted svg's plate fill DIFFERS from it. Fail-LOUD on timeout.
    result.skinFlip = await evalJs(`(async () => {
      const sleep = (ms) => new Promise(r => setTimeout(r, ms));

      // Pre-click plate fill — the state we must observe CHANGE (the dark canvas hex).
      const plateFillOf = (svg) => {
        if (!svg) return null;
        const rects = Array.from(svg.children).filter(el => el.tagName.toLowerCase() === 'rect');
        const plate = rects.map(el => el.getAttribute('fill'))
          .find(f => f && f.toLowerCase() !== 'none');
        return plate ? plate.toLowerCase() : null;
      };
      const preSvg = document.querySelector('.atlas-svg-host svg');
      const prePlateFill = plateFillOf(preSvg);

      // (1) SELECT BY CANVAS LABEL + aria-pressed — never by skin name.
      //     The button textContent is the CAPITALIZED canvas word directly concatenated with
      //     the lowercase skin-name span (e.g. "Lightinstrument", "Darkarchive"). A case-
      //     SENSITIVE substring 'Light' matches ONLY the canvas label — the skin names
      //     ('archive'/'instrument') are lowercase and contain no capital 'Light'/'Dark', and
      //     the legend/filter labels ('Live Builds', 'Build Families', 'All', 'DEPLOY · W' …)
      //     contain no capital-run 'Light'/'Dark' either. (A \\bLight\\b word-boundary FAILS
      //     here because 'instrument' abuts 'Light' with no separator — that was the miss.)
      const btns = Array.from(document.querySelectorAll('button[aria-pressed]'));
      const isLightCanvasBtn = (b) => (b.textContent || '').includes('Light'); // capital label only
      const target = btns.find(b => isLightCanvasBtn(b) && b.getAttribute('aria-pressed') === 'false' && !b.disabled);
      if (!target) {
        // Maybe already on light (aria-pressed true) — then there is nothing to flip TO.
        const anyLight = btns.find(isLightCanvasBtn);
        return {
          flipped: false,
          reason: anyLight ? 'light canvas already active (no aria-pressed=false Light button)' : 'no Light-canvas button found',
          ariaButtons: btns.map(b => ({ text: (b.textContent||'').replace(/\\s+/g,' ').trim().slice(0,24), pressed: b.getAttribute('aria-pressed') })).slice(0, 12),
        };
      }
      target.click();

      // (2) WAIT FOR STATE CHANGE — poll until the plate fill DIFFERS from the pre-click
      //     (dark) fill. The still-mounted dark svg keeps prePlateFill until the LIGHT
      //     markup re-inlines; only a real change satisfies this. Fail-loud on timeout.
      let svg = null;
      let postPlateFill = null;
      let changed = false;
      for (let i = 0; i < 200; i++) {
        await sleep(75);
        svg = document.querySelector('.atlas-svg-host svg');
        postPlateFill = plateFillOf(svg);
        if (svg && !svg.hasAttribute('width') && postPlateFill && postPlateFill !== prePlateFill) {
          changed = true;
          break;
        }
      }
      if (!changed) {
        return {
          flipped: false,
          reason: 'plate fill did not change after Light flip (skin did not re-render) — TIMEOUT',
          prePlateFill, postPlateFill,
        };
      }
      const directRects = Array.from(svg.children).filter(el => el.tagName.toLowerCase() === 'rect');
      const info = directRects.map(el => ({
        x: el.getAttribute('x'), y: el.getAttribute('y'),
        width: el.getAttribute('width'), height: el.getAttribute('height'),
        fill: el.getAttribute('fill'), stroke: el.getAttribute('stroke'),
      }));
      // LIGHT-skin text-occlusion (v2): re-find the legend + re-scan every <text> node.
      const PAD = 4;
      const rectsIntersect = (a, b) =>
        a.left - PAD < b.right && a.right + PAD > b.left &&
        a.top - PAD < b.bottom && a.bottom + PAD > b.top;
      const region = document.querySelector('[aria-label="Build Horizon — full-horizon chart"]');
      let legendEl = null;
      if (region) {
        legendEl = Array.from(region.querySelectorAll('div,button')).find(el => {
          const t = (el.textContent || '').trim();
          return /^Legend\\b/.test(t) && el.offsetParent !== null;
        }) || null;
      }
      const legendRect = legendEl ? legendEl.getBoundingClientRect() : null;
      let textOcclusion = { legendRectPresent: !!legendRect, textNodes: 0, occlusions: [], textOcclusions: null };
      if (legendRect) {
        const hits = [];
        let counted = 0;
        for (const t of Array.from(svg.querySelectorAll('text'))) {
          const tr = t.getBoundingClientRect();
          if (tr.width <= 0 || tr.height <= 0) continue;
          counted++;
          if (rectsIntersect(legendRect, tr)) {
            hits.push({ text: (t.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 80),
              bbox: { left: Math.round(tr.left), top: Math.round(tr.top), right: Math.round(tr.right), bottom: Math.round(tr.bottom) } });
          }
        }
        textOcclusion = {
          legendRectPresent: true,
          legendRect: { left: Math.round(legendRect.left), top: Math.round(legendRect.top), right: Math.round(legendRect.right), bottom: Math.round(legendRect.bottom) },
          textNodes: counted, pad: PAD, occlusions: hits, textOcclusions: hits.length,
        };
      }
      return {
        flipped: true,
        // State-change receipt (D7-c): plate fill BEFORE (dark) vs AFTER (light) the flip.
        // These MUST differ — that difference is the proof the light skin actually mounted.
        prePlateFill,
        postPlateFill,
        viewBox: svg.getAttribute('viewBox'),
        plate: info.find(r => r.fill && r.fill.toLowerCase() !== 'none') || null,
        frame: info.find(r => r.fill && r.fill.toLowerCase() === 'none' && r.stroke) || null,
        svgWidthAttr: svg.getAttribute('width'),
        textOcclusion,
      };
    })()`);
  }

  await browser.send('Target.closeTarget', { targetId });
  return result;
}

async function main() {
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'drax-cdp-'));
  const { proc, wsUrl } = await launchChrome(userDataDir);
  const browser = cdpConnect(wsUrl);
  await browser.ready;
  const results = [];
  try {
    for (const vp of VIEWPORTS) {
      // D7-a re-verify allocation: the WIDEST width (2560) gets FULL extras — the fluid-
      // width eyes-ref full-page screenshot + corner crops + wiring smoke + skin flip. EVERY
      // OTHER width runs the skin flip (so acc 67 v2 is proven under BOTH skins at every
      // width the brief lists: 2560, 1920, 1440, 1280, 375). Dark-skin occlusion is measured
      // at every viewport already (in `measurement`); the flip adds the light-skin check.
      const extras = vp.name === '2560' ? 'full' : 'flip';
      const r = await probeViewport(browser, vp, extras);
      results.push(r);
    }
  } finally {
    try { browser.ws.close(); } catch {}
    try { proc.kill('SIGKILL'); } catch {}
  }
  const outJson = path.join(OUT_DIR, 'd6-receipts.json');
  fs.writeFileSync(outJson, JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
  console.log('\nReceipts JSON:', outJson);

  // ---- ACC 67 v2 GATE (fail-loud): zero <text> intersections at EVERY width, both skins ----
  // D7-a re-verify: the FLUID host MOVES the geometry with width, so the binding surfaces are
  // now 2560/1920/1440/1280/375 × {dark, light} = 10. Each carries a textOcclusions count;
  // ANY nonzero → the legend occludes an in-artifact text node → FAIL. The wide widths (2560,
  // 1920) are the whole point of this pass — they are gated, HALT-don't-shrink if unsatisfiable.
  const occChecks = [];
  const flipFailures = [];
  for (const r of results) {
    // Every viewport's DARK-skin occlusion is measured in `measurement`; the flip adds the
    // LIGHT-skin check (run at every width now). A flip that did NOT change state is a HARD
    // failure (the D7-c wait-for-CHANGE guard) — recorded so the -light surface is not
    // silently satisfied by a re-measured dark skin.
    if (r.textOcclusion && typeof r.textOcclusion.textOcclusions === 'number') {
      occChecks.push({ where: `${r.viewport}-dark`, ...r.textOcclusion });
    }
    if (r.skinFlip && r.skinFlip.flipped === false) {
      flipFailures.push({ where: `${r.viewport}-light`, reason: r.skinFlip.reason, prePlateFill: r.skinFlip.prePlateFill, postPlateFill: r.skinFlip.postPlateFill });
    }
    if (r.skinFlip && r.skinFlip.textOcclusion && typeof r.skinFlip.textOcclusion.textOcclusions === 'number') {
      occChecks.push({ where: `${r.viewport}-light`, ...r.skinFlip.textOcclusion });
    }
  }
  console.log('\n==== ACC 67 v2 — legend × in-artifact <text> occlusion (±4px pad) ====');
  const REQUIRED = [
    '2560-dark', '2560-light', '1920-dark', '1920-light',
    '1440-dark', '1440-light', '1280-dark', '1280-light', '375-dark', '375-light',
  ];
  const seen = new Set(occChecks.map((c) => c.where));
  const missing = REQUIRED.filter((k) => !seen.has(k));
  let failed = false;
  for (const c of occChecks) {
    const corner = c.legendRect
      ? `legend[l=${c.legendRect.left},t=${c.legendRect.top},r=${c.legendRect.right},b=${c.legendRect.bottom}]`
      : 'legend[absent]';
    console.log(`  ${c.where}: textOcclusions=${c.textOcclusions} · textNodes=${c.textNodes} · ${corner}`);
    if (c.textOcclusions > 0) {
      failed = true;
      for (const h of c.occlusions) {
        console.log(`      ✗ OCCLUDES <text> "${h.text}"  bbox=[l=${h.bbox.left},t=${h.bbox.top},r=${h.bbox.right},b=${h.bbox.bottom}]`);
      }
    }
    if (c.legendRectPresent === false) {
      failed = true;
      console.log(`      ✗ legend rect NOT FOUND at ${c.where} — cannot prove the law`);
    }
  }
  // D7-c: a flip that did not change state is fail-loud (never silently pass).
  for (const f of flipFailures) {
    failed = true;
    console.log(`      ✗ SKIN FLIP DID NOT CHANGE STATE at ${f.where}: ${f.reason} (prePlateFill=${f.prePlateFill}, postPlateFill=${f.postPlateFill})`);
  }
  if (missing.length) {
    failed = true;
    console.log(`  ✗ MISSING required occlusion checks: ${missing.join(', ')}`);
  }
  if (failed) {
    console.error('\nPROBE FAILED: acc 67 v2 — the legend overlay intersects an in-artifact <text> bbox, a skin flip did not change state, or a required check is missing. See the ✗ lines above.');
    process.exit(1);
  }
  console.log(`  acc 67 v2 PASS — legend intersects ZERO in-artifact <text> bbox at all ${REQUIRED.length} binding surfaces (5 widths × 2 skins).`);
  process.exit(0);
}

main().catch((e) => {
  console.error('PROBE FAILED:', e.stack || e.message);
  process.exit(1);
});
