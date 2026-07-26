// gd-gp-calib-locate.mjs — REGION LOCATION ONLY. Emits downscaled LOCATOR-* renders.
// Nothing is ever read from these; see METHOD LAW in gd-gp-calib-lib.mjs.
import path from 'node:path';
import { STILLS_V3, TRIAL_FRAMES, SHEET_FRAMES, ensureDirs, locator } from './gd-gp-calib-lib.mjs';
await ensureDirs();
const want = process.argv.slice(2);
const all = { ...TRIAL_FRAMES, ...SHEET_FRAMES };
for (const [k, f] of Object.entries(all)) {
  if (want.length && !want.includes(k)) continue;
  const p = await locator(path.join(STILLS_V3, f), `${k}.png`);
  console.log(k, '->', p);
}
