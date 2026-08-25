# KC2-MC — PM5 RE-GRADE MID-FLIGHT SUPPLEMENT 2 (conductor, R-L77-2)

**To:** gamora (Wave-3 PM5 re-grade, in flight)
**From:** gandalf RUN-CONDUCTOR, 2026-08-25
**Status:** delivery NOT guaranteed mid-flight (SendMessage unavailable — standing L-71 correction); ENFORCED at the PM5 seal seating regardless. Supplement-1 (MD-B4app-9 / single-limb wording) is unchanged and still binds.

## 1 — MD-B4app-2 RETURNED: fold as RETURNED, strike "name as pending"

galadriel's measurement: `agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md` (commit `57ebd439`; pipeline `galadriel/pipeline/eor_channel.py` + `eor_duty.py`; evidence under `galadriel/captures/2026-08-25-md-b4app-2-channel/`). Headline figures, all derivation-carrying:

- Referent channel-active **83.8 %** of combat time (strict 0.753 / loose 0.895; provably idle only 7.95 %).
- **P(channel | MOVING) = 0.892 > P(channel | STATIONARY) = 0.738** — the channel does NOT stop when he moves (38 movement onsets, drain-tick rate flat across the onset, sustained through 13–16 m traverses).
- Stationary 37.4 % / moving 62.6 %, stable ±0.03 across a tenfold threshold sweep.
- Plant-at-spawns HOLDS: first 5 s post-flip 0.615 stationary vs 0.374 fight-wide; standing within 0.73 s in 9/10 waves; 96 % stationary through wave 160's first 5 s. But median stop 0.45 s, 86 stops in 183 s, and 17.0 % of stationary time has ZERO drain ticks vs 3.0 % moving — **he stops to do something else, not to channel**.
- Second board (s1 waves 4–6): pressure costs him GROUND (73–75 % stationary) not UPTIME (~47–50 % channel).

## 2 — Policy-vocabulary CORRECTION (binds entry (ix))

The Wave-2 wording "the pilot doesn't stop-to-channel like Matt does" is **INVERTED by the measurement** — Matt doesn't stop to channel either; he **channels through movement**. The exclusion-set policy entry names the gap as: **sim movement EXCESS (86.3 % vs referent 62.6 %, 1.38×) + channel deficit (G5 1.9 % vs referent 83.8 %)** — channel-through-movement policy, NOT stop-to-channel. On channel uptime, **G0 (100 %) is nearer the referent by ~40× than G5 (1.9 %)**. Mechanism-vs-policy naming survives intact: the gap is still POLICY not mechanism; only the policy's shape changed.

## 3 — Grading discipline on these figures

Every figure above names its instrument in galadriel's note (20 Hz phase-correlation motion + 60 Hz HUD-energy OCR, specificity control 4,800 samples/zero false ticks, one instrument built-then-rejected with numbers recorded, seven quantities named UNMEASURABLE — notably the drain is EoR-*consistent*, not EoR-identified). Grade with those caveats attached; do not promote EoR-consistent to EoR-identified.

## 4 — Unchanged

Everything else stands: dispatch entry list (i)–(ix), supplement-1, fold-derivation two limbs + check-output category, byte-guards, D4 prereg, smoke 645/1, never push.
