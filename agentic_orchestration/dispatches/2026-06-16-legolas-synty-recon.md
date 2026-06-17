# Dispatch — 2026-06-16 — legolas — Synty subscription recon (Mode B)

**From:** knight-rider
**To:** legolas
**Approved by:** Matt — new-workstream brief 2026-06-16 (Synty corpus acquisition)
**Estimated effort:** recon ≤ half a session; staged deliverables D1→D3
**Acceptance:** D1+D2 land a recon report under `research/` that resolves the variant-format and throttle questions; D3 (conditional) lands a representative slice on the Mac for elrond to catalogue.

## Context

Matt owns the full Synty Pass (all packs). We are building a **gear-catalogue substrate** for the gear-spec generator gandalf is designing — the same "select + adapt, not mass-generate" pattern the existing `research/curated/catalogue.db` + `research/catalogue/` vendor tree uses, now extended to **3D armor + weapon meshes** from Synty.

Synty-Hub is already checked: **no first-party bulk downloader exists** (only manual My Account → My Downloads, plus a Unity-only importer that runs on already-downloaded files). Download automation is therefore custom — which is why we recon before committing to a bulk format or a host.

**This recon is the gate** on two downstream Pattern-B dispatches (the Pi-side resumable downloader, and elrond's catalogue/extraction pipeline). Both bake load-bearing assumptions about the variant format. Do not let us build those on a guess.

**Lead discipline — slice first.** The paused gear-spec design session resumes the moment a representative slice is catalogued. Your D3 deliverable (a small slice pulled to the Mac) is what unblocks it. The full multi-day corpus pull is a *separate, later* dispatch and must not gate anything here.

## Required reading before starting
- This dispatch.
- `research/curated/catalogue.db` schema + a couple of `research/catalogue/<vendor>/` folders (e.g. `pimen/`, `craftpix/`) — to understand the existing "select + adapt" substrate pattern and metadata shape you're feeding into. You produce read-only findings; **elrond** curates.
- `research/commissions/2026-05-16-legolas-pimen-mode-b-sample.md` — prior Mode B crawl shape.

## Authorization / read-only posture
- Matt-authorized, read-only against Matt's own subscription. ADR-006 posture holds: you **download** Matt's licensed assets (read from Synty), you do **not** write to any Synty-side state.
- Subscription URL (Matt-authorized): `https://syntystore.com/apps/downloads/subscriptions/mhwetmore@gmail.com/530884`

## Staged deliverables

### D1 — Authenticate + enumerate (gating; report immediately if blocked)
- [ ] Establish an authenticated session against the subscription URL. **This is the single practical unknown.** Determine the mechanism (browser-cookie reuse, login form, session token, etc.). **If you cannot authenticate, STOP and report exactly what you need from Matt** (e.g., a logged-in cookie export, credentials, a session token). Do not burn the session guessing — a precise "here's what I need" is a successful D1.
- [ ] Enumerate every pack download link available on the subscription. Output a machine-readable manifest (JSONL preferred, matching the substrate-inventory shape) under `research/catalogue/synty-recon-2026-06-16/`.

### D2 — Characterize variants + diagnose throttle (the architecture-gating findings)
- [ ] For a representative sample of packs (and ideally all), characterize **what download variants each pack offers**: source/FBX vs `.unitypackage` vs other. Note per-pack which are available — they may not be uniform.
- [ ] **Prefer source/FBX.** If a pack offers *only* `.unitypackage`, flag it: a `.unitypackage` is a gzipped tar; FBX + textures are extractable, but extraction is compute (and runs Mac/PC-side, never on the Pi). Quantify roughly how many packs are FBX-available vs unitypackage-only — this sizes the extraction-pipeline scope for elrond.
- [ ] **Throttle-vs-local diagnosis** (recon open question (a)): time a few downloads and determine whether the slowness Matt observed is **local bandwidth** or a **Synty per-account throttle**. This decides host strategy: if it's an account-side throttle, host choice is irrelevant and the answer is simply "sequential + resumable, let it run for days on the always-on Pi." Report your evidence, not just a verdict (per-file rate, concurrency behavior if you can probe it safely without hammering the account).

### D3 — Representative slice to Mac (conditional on D1+D2 clean; unblocks the design session)
- [ ] If auth works and variants are understood, pull a **small representative slice to the Mac** (not the Pi — Mac is the working subset): a few armor packs spanning **chest / legs / boots**, plus **one weapon pack**. Prefer FBX variants. Land bytes on the filesystem under a clear path and report it.
- [ ] This slice is what elrond catalogues next to unblock gandalf's gear-spec session. Optimize the slice for **slot coverage and distinctiveness spread**, not volume.
- [ ] If D1/D2 surface a blocker (auth gap, unitypackage-only, severe throttle), **do D1+D2 reporting and stop** — recommend slice composition rather than pulling it, and we resolve the blocker with Matt first.

## Cross-seam contract change? (Principle 6 gate)
Round-trip: **not applicable** — this is read-only recon producing research artifacts; no inter-seam fixture/schema change. (The downstream catalogue dispatch to elrond WILL touch schema; that's gated separately.)

## Out of scope (explicit non-goals)
- **Do NOT** build the full resumable Pi-side downloader — that's a separate Pattern-B dispatch authored after this recon, with the variant format known.
- **Do NOT** download the full corpus. Slice only.
- **Do NOT** set up the Pi / USB-SSD infra — that's separate host-infra work, not on the slice critical path.
- **Do NOT** design the catalogue schema or run extraction/thumbnail/distinctiveness rendering — that's elrond's seam.
- **Do NOT** write to any Synty-side state.

## Open questions for the agent to resolve + document
- (a) Local-bandwidth vs Synty per-account throttle (D2). **Drives the host decision.**
- (b) Variant inventory per pack — FBX-available vs unitypackage-only ratio (D2). **Drives the extraction-pipeline scope.**
- The auth mechanism (D1). If it requires something only Matt can provide, name it precisely.

## References
- New-workstream brief 2026-06-16 (Synty corpus acquisition), knight-rider session.
- Existing substrate precedent: `research/curated/catalogue.db`, `research/catalogue/`.
- EULA (recon open question (c)) is **Matt's to confirm** at `syntystore.com/pages/licences-overview` — it feeds the incorporation_status ledger semantics in elrond's later dispatch, NOT this recon.
