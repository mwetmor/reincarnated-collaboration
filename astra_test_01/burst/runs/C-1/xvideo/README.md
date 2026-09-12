# X-video probe (Q76) — Grok Imagine image-to-video via the consumer app, HITL step

**Still to upload:** `astra_test_01/burst/runs/C-1/artifacts/K6-male-H1/k6_male_H1_1.png` (H1 man on the #00ff00 plate) — or the re-minted H1 starter woman once C-2 mints her. Upload the PNG as the FIRST FRAME. If the app offers a LAST-frame / loop control, use the SAME still as the last frame (loop closure) and note that it exists.

**Prompt A — relaxed idle (6 s):**
> The character stands still and breathes. Keep the flat solid pure green (#00ff00) background completely unchanged and empty — no scenery, no shadows, no particles. Camera locked, no zoom, no pan. Only the body moves: a slow calm breath — chest and shoulders rise and fall about once every two seconds; the head sways very slightly with the breath; the staff stays planted; both feet stay planted and never slide. Same face, same costume, same colours in every frame. Hand-drawn 2D animation, one continuous shot, no cuts. Loop: the last frame matches the first.

**Prompt B — walk in place (6 s):**
> The character walks in place, facing the camera (toward the viewer), on a flat solid pure green (#00ff00) background that stays completely unchanged and empty. Camera locked. A natural, confident walk cycle: the head bobs up and down twice per stride, the free arm swings opposite the legs, the staff arm swings a little; the feet lift and plant clearly with weight. Same face, same costume, same colours in every frame. Hand-drawn 2D animation, one continuous shot, no cuts. Loop: the last frame matches the first.

**Drop the MP4s here:** `runs/C-1/xvideo/in/` as `idle_A.mp4`, `walk_B.mp4` (plus a screenshot of the UI controls if first/last-frame exists). The T1 instrument then: split at native fps → matte on the plate → G11 identity drift per frame → silhouette-boil score (edge jitter frame to frame) → idle: breath/head bob %H vs the Hades combat band → walk: phase table + W-1…W-6 vs Muybridge → keep/kill on the pre-registered kill criteria (scene cuts; boil that keys to a jittering matte; drift beyond G11). Class: FIRST-PARTY (our character, our plate) — may enter the repo.
