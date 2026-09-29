#!/usr/bin/env python3
"""T7-B: minimal World Labs Marble API client.

The key is read from the environment (WORLD_LABS_API_KEY) and is NEVER printed,
logged, or written into any artifact -- including the request logs this writes.

Subcommands
  credits                                    free
  upload  <file>                             free (prepare_upload + PUT)
  gen     --asset <id> --model M --name N [--text T] [--seed S]
  op      <operation_id>
  world   <world_id>
  export  <world_id> --asset splats|mesh --format ply|glb [--resolution R]
  dl      <url> <dest>

Every call that can cost credits prints the credit balance before and after and
appends a JSON line to logs/api_log.jsonl.
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE = "https://api.worldlabs.ai"


def _ssl_ctx():
    """python.org Python ships no CA bundle on this Mac; use certifi or the system store.
    Verification stays ON -- this fixes the trust root, it does not disable checking."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    for p in ("/etc/ssl/cert.pem", "/usr/local/etc/openssl@3/cert.pem",
              "/opt/homebrew/etc/openssl@3/cert.pem"):
        if os.path.exists(p):
            return ssl.create_default_context(cafile=p)
    raise SystemExit("no CA bundle found; refusing to run unverified")


CTX = _ssl_ctx()
ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "api_log.jsonl"


def key():
    k = os.environ.get("WORLD_LABS_API_KEY", "")
    if not k:
        sys.exit("WORLD_LABS_API_KEY not in environment (source ~/.zshrc)")
    return k


def req(method, path, body=None, raw_url=None, extra_headers=None, data=None):
    url = raw_url or (BASE + path)
    hdrs = {"WLT-Api-Key": key()}
    if extra_headers:
        hdrs.update(extra_headers)
    payload = data
    if body is not None:
        payload = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=payload, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(r, timeout=300, context=CTX) as resp:
            b = resp.read()
            return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {method} {path or url}: {e.read().decode()[:2000]}")


def credits():
    return req("GET", "/marble/v1/credits")["remaining_credits"]


def log(event, **kw):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event}
    rec.update(kw)
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def upload(path):
    p = Path(path)
    r = req("POST", "/marble/v1/media-assets:prepare_upload",
            {"file_name": p.name[:64], "kind": "image", "extension": p.suffix.lstrip(".")})
    aid = r["media_asset"]["media_asset_id"]
    up = r["upload_info"]
    hdrs = dict(up.get("required_headers") or {})
    body = p.read_bytes()
    rq = urllib.request.Request(up["upload_url"], data=body, headers=hdrs, method="PUT")
    with urllib.request.urlopen(rq, timeout=600, context=CTX) as resp:
        code = resp.status
    log("upload", file=str(p), bytes=len(body), media_asset_id=aid, http=code)
    return {"media_asset_id": aid, "http": code, "bytes": len(body)}


def generate(asset_id, model, name, text=None, seed=None, is_pano=False):
    # world_prompt is a FLAT discriminated union on `type`; the "image" in a 422's
    # loc path (body.world_prompt.image.image_prompt) is the VARIANT NAME, not a
    # nested field. So image_prompt / is_pano / text_prompt all sit at this level.
    # `is_pano` is a bool or the string "auto".
    wp = {"type": "image",
          "image_prompt": {"source": "media_asset", "media_asset_id": asset_id},
          "is_pano": is_pano}
    if text:
        wp["text_prompt"] = text
    body = {"display_name": name[:64], "model": model, "world_prompt": wp,
            "permission": {"public": False}}
    if seed is not None:
        body["seed"] = seed
    before = credits()
    r = req("POST", "/marble/v1/worlds:generate", body)
    log("generate", model=model, display_name=name, media_asset_id=asset_id,
        text_prompt=text, seed=seed, credits_before=before,
        operation_id=r.get("operation_id"), request_body=body)
    r["_credits_before"] = before
    return r


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("credits")
    u = sub.add_parser("upload"); u.add_argument("file")
    g = sub.add_parser("gen")
    g.add_argument("--asset", required=True); g.add_argument("--model", required=True)
    g.add_argument("--name", required=True); g.add_argument("--text", default=None)
    g.add_argument("--seed", type=int, default=None)
    o = sub.add_parser("op"); o.add_argument("operation_id")
    w = sub.add_parser("world"); w.add_argument("world_id")
    e = sub.add_parser("export")
    e.add_argument("world_id"); e.add_argument("--asset", required=True)
    e.add_argument("--format", required=True); e.add_argument("--resolution", default=None)
    d = sub.add_parser("dl"); d.add_argument("url"); d.add_argument("dest")
    a = ap.parse_args()

    if a.cmd == "credits":
        print(json.dumps({"remaining_credits": credits()}))
    elif a.cmd == "upload":
        print(json.dumps(upload(a.file), indent=1))
    elif a.cmd == "gen":
        print(json.dumps(generate(a.asset, a.model, a.name, a.text, a.seed), indent=1))
    elif a.cmd == "op":
        print(json.dumps(req("GET", f"/marble/v1/operations/{a.operation_id}"), indent=1))
    elif a.cmd == "world":
        print(json.dumps(req("GET", f"/marble/v1/worlds/{a.world_id}"), indent=1))
    elif a.cmd == "export":
        body = {"asset_type": a.asset, "format": a.format}
        if a.resolution:
            body["resolution"] = a.resolution
        before = credits()
        r = req("POST", f"/marble/v1/worlds/{a.world_id}:export", body)
        log("export", world_id=a.world_id, body=body, credits_before=before,
            operation_id=r.get("operation_id"), done=r.get("done"), cost=r.get("cost"))
        print(json.dumps(r, indent=1))
    elif a.cmd == "dl":
        Path(a.dest).parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(a.url, timeout=1800, context=CTX) as resp, open(a.dest, "wb") as f:
            n = 0
            while True:
                b = resp.read(1 << 20)
                if not b:
                    break
                f.write(b); n += len(b)
        log("download", dest=a.dest, bytes=n)
        print(json.dumps({"dest": a.dest, "bytes": n, "MB": round(n / 1e6, 2)}))


if __name__ == "__main__":
    main()
