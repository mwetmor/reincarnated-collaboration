#!/usr/bin/env node
// capture.mjs — galadriel headless capture harness
//
// Author: galadriel (visual-perception steward) — agentic_orchestration
// Purpose: drive headless Chromium against the running demo dev server at named states +
// named viewports; produce reproducible PNG captures + metadata sidecars under
// agentic_orchestration/galadriel/captures/<YYYY-MM-DD>/<state>/<viewport>/.
//
// Discipline notes:
//  - Reproducibility-first. Every capture writes a JSON sidecar with state, viewport, demo
//    git SHA, dev-url, console-log tail, timestamp. Another galadriel instance running
//    against the same SHA + dev-url should reproduce the picture within rendering variance.
//  - No silent transformation. Captures are saved as raw PNG full-page; any later crop,
//    histogram, or comparison happens in a separate script with its own provenance.
//  - State-determinism is upstream. The pipeline DOES NOT seed game state. Determinism
//    comes from drax-D11.5 debug-state hook (?debug=true&debug-state=<name>). If the hook
//    is not yet shipped, the `landing` state captures the demo's default load (NOT
//    comparison-grade; useful only as cross-viewport regression baseline).
//  - Smoke-test before full. --smoke runs one state × one viewport (landing × 390×844) to
//    verify headless boots, navigation works, screenshot saves.
//
// Usage:
//   node capture.mjs --smoke
//   node capture.mjs --state landing --viewport mobile-portrait-1290x2796
//   node capture.mjs --state combat-midfight                          # all viewports for state
//   node capture.mjs --all-states                                     # all states × all listed viewports
//   node capture.mjs --state combat-midfight --dev-url http://localhost:5174
//   node capture.mjs --state combat-midfight --out-dir /tmp/galadriel-captures

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const STATES_PATH = path.join(HERE, 'states.json');
const DEMO_REPO = path.resolve(HERE, '../../../../reincarnated-demo');
const DEFAULT_OUT_BASE = path.resolve(HERE, '../captures');
const DEFAULT_DEV_URL = 'http://localhost:5173';
const DEFAULT_WAIT_FOR_TIMEOUT_MS = 15_000;

// ---------- arg parsing ----------
function parseArgs(argv) {
  const args = { state: null, viewport: null, outBase: DEFAULT_OUT_BASE, devUrl: DEFAULT_DEV_URL, allStates: false, smoke: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--state')          args.state    = argv[++i];
    else if (a === '--viewport')  args.viewport = argv[++i];
    else if (a === '--out-dir')   args.outBase  = path.resolve(argv[++i]);
    else if (a === '--dev-url')   args.devUrl   = argv[++i];
    else if (a === '--all-states')args.allStates= true;
    else if (a === '--smoke')     args.smoke    = true;
    else if (a === '--help' || a === '-h') { printHelp(); process.exit(0); }
    else { console.error(`unknown arg: ${a}`); printHelp(); process.exit(2); }
  }
  return args;
}

function printHelp() {
  console.log(`capture.mjs — galadriel headless capture harness
Usage:
  --smoke                       run 1 state × 1 viewport smoke-test (landing × 390×844)
  --state <name>                state name from states.json
  --viewport <name>             viewport name from states.json _viewports (default: all listed for state)
  --out-dir <path>              base output dir (default: ../captures)
  --dev-url <url>               dev server URL (default: http://localhost:5173)
  --all-states                  loop all states × all their listed viewports`);
}

// ---------- utils ----------
function todayISO() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function demoGitSha() {
  try {
    return execSync('git rev-parse HEAD', { cwd: DEMO_REPO }).toString().trim();
  } catch (e) {
    return 'unknown';
  }
}

function demoGitShortSha() {
  try {
    return execSync('git rev-parse --short HEAD', { cwd: DEMO_REPO }).toString().trim();
  } catch (e) {
    return 'unknown';
  }
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function loadStates() {
  return JSON.parse(fs.readFileSync(STATES_PATH, 'utf-8'));
}

// ---------- capture core ----------
async function captureOne(browser, { stateName, stateSpec, viewportName, viewportSpec, devUrl, outBase, todayStr, demoSha, demoShort }) {
  const outDir = path.join(outBase, todayStr, stateName, viewportName);
  ensureDir(outDir);

  const fullUrl = devUrl.replace(/\/$/, '') + stateSpec.url_path;
  const filename = `capture.png`;
  const sidecarName = `capture.json`;
  const outPng = path.join(outDir, filename);
  const outSidecar = path.join(outDir, sidecarName);

  const consoleTail = [];
  const consoleCapacity = 200;

  const context = await browser.newContext({
    viewport:           { width: viewportSpec.width, height: viewportSpec.height },
    deviceScaleFactor:  viewportSpec.deviceScaleFactor ?? 1,
    isMobile:           !!viewportSpec.isMobile,
    hasTouch:           !!viewportSpec.isMobile,
  });
  const page = await context.newPage();

  page.on('console', (msg) => {
    const line = `[${msg.type()}] ${msg.text()}`;
    consoleTail.push(line);
    if (consoleTail.length > consoleCapacity) consoleTail.shift();
  });

  let waitForSatisfied = false;
  if (stateSpec.wait_for) {
    page.on('console', (msg) => {
      if (msg.text().includes(stateSpec.wait_for)) waitForSatisfied = true;
    });
  }

  const result = { ok: false, error: null, frictionNotes: [] };

  try {
    console.log(`[capture] ${stateName} × ${viewportName}  →  ${fullUrl}`);
    await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 30_000 });

    // wait for the signal (if any)
    if (stateSpec.wait_for) {
      const deadline = Date.now() + DEFAULT_WAIT_FOR_TIMEOUT_MS;
      while (!waitForSatisfied && Date.now() < deadline) {
        await page.waitForTimeout(200);
      }
      if (!waitForSatisfied) {
        result.frictionNotes.push(`wait_for signal "${stateSpec.wait_for}" not observed within ${DEFAULT_WAIT_FOR_TIMEOUT_MS}ms — likely drax-D11.5 hook unshipped or different log signature`);
      }
    }

    // warmup for atmospheric layers / animations / pixi tickers
    if (stateSpec.warmup_ms) await page.waitForTimeout(stateSpec.warmup_ms);

    await page.screenshot({ path: outPng, fullPage: false }); // viewport-only capture (NOT full scroll-page; we want what the eye sees at viewport)

    result.ok = true;
  } catch (e) {
    result.error = String(e?.message || e);
  } finally {
    const sidecar = {
      state:              stateName,
      state_purpose:      stateSpec._purpose ?? null,
      viewport:           viewportName,
      viewport_spec:      { width: viewportSpec.width, height: viewportSpec.height, deviceScaleFactor: viewportSpec.deviceScaleFactor ?? 1, isMobile: !!viewportSpec.isMobile },
      dev_url:            devUrl,
      full_url:           fullUrl,
      doe_reference:      stateSpec.doe_reference ?? null,
      demo_git_sha:       demoSha,
      demo_git_short_sha: demoShort,
      captured_at_utc:    new Date().toISOString(),
      ok:                 result.ok,
      error:              result.error,
      wait_for:           stateSpec.wait_for ?? null,
      wait_for_satisfied: stateSpec.wait_for ? waitForSatisfied : null,
      warmup_ms:          stateSpec.warmup_ms ?? null,
      friction_notes:     result.frictionNotes,
      console_log_tail:   consoleTail,
      capture_png:        path.relative(outBase, outPng),
      pipeline_version:   '0.1.0',
    };
    fs.writeFileSync(outSidecar, JSON.stringify(sidecar, null, 2));
    await context.close();
  }

  return result;
}

// ---------- orchestration ----------
function pickStateViewportPairs(states, args) {
  const todo = [];
  const stateNames = args.allStates ? Object.keys(states.states) : (args.state ? [args.state] : []);
  if (stateNames.length === 0) {
    throw new Error('No state selected. Use --state <name> or --all-states or --smoke.');
  }
  for (const sName of stateNames) {
    const sSpec = states.states[sName];
    if (!sSpec) throw new Error(`unknown state: ${sName}`);
    const vList = args.viewport ? [args.viewport] : sSpec.viewports;
    for (const vName of vList) {
      const vSpec = states._viewports[vName];
      if (!vSpec) throw new Error(`unknown viewport: ${vName}`);
      todo.push({ stateName: sName, stateSpec: sSpec, viewportName: vName, viewportSpec: vSpec });
    }
  }
  return todo;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.smoke) {
    args.state = 'landing';
    args.viewport = 'mobile-portrait-390x844';
    args.allStates = false;
    console.log('[smoke] state=landing viewport=mobile-portrait-390x844');
  }

  const states = loadStates();
  const todo = pickStateViewportPairs(states, args);
  const todayStr = todayISO();
  const demoSha = demoGitSha();
  const demoShort = demoGitShortSha();

  console.log(`[capture] demo SHA=${demoShort}  todo=${todo.length}  out-base=${args.outBase}/${todayStr}/`);

  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const t of todo) {
      const r = await captureOne(browser, { ...t, devUrl: args.devUrl, outBase: args.outBase, todayStr, demoSha, demoShort });
      results.push({ state: t.stateName, viewport: t.viewportName, ...r });
    }
  } finally {
    await browser.close();
  }

  const okCount = results.filter(r => r.ok).length;
  const failCount = results.length - okCount;
  console.log(`\n[capture] done. ok=${okCount}/${results.length}  fail=${failCount}`);
  for (const r of results) {
    const tag = r.ok ? 'OK  ' : 'FAIL';
    const notes = (r.frictionNotes && r.frictionNotes.length) ? `  friction: ${r.frictionNotes.join('; ')}` : '';
    const err = r.error ? `  error: ${r.error}` : '';
    console.log(`  [${tag}] ${r.state} × ${r.viewport}${notes}${err}`);
  }
  process.exit(failCount > 0 ? 1 : 0);
}

main().catch((e) => { console.error(e); process.exit(1); });
