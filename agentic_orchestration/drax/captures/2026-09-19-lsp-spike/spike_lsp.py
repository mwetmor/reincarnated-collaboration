#!/usr/bin/env python3
"""Drive ONE headless Godot LSP instance over a project; collect diagnostics.

Runs entirely inside the caller's heavy_lock hold, so the Godot instance's whole
lifetime is under the lock. Two probes:
  (A) the dispatch's literal command line: `godot-lsp-cli diagnostics --project X --json`
  (B) a didOpen sweep over every .gd (what the LSP can actually answer)
"""
import json, os, socket, subprocess, sys, time, pathlib, urllib.parse

GODOT = "/Applications/Godot.app/Contents/MacOS/Godot"
LSPCLI = os.path.expanduser("~/.npm-global/bin/godot-lsp-cli")

project = os.path.abspath(sys.argv[1])
outdir = pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
tag = sys.argv[3]
port = int(sys.argv[4]) if len(sys.argv) > 4 else 6015
boot_timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 420

log = (outdir / f"{tag}_godot.log").open("w")
t_spawn = time.time()
proc = subprocess.Popen(
    [GODOT, "--headless", "--editor", "--path", project, "--lsp-port", str(port)],
    stdout=log, stderr=subprocess.STDOUT,
)
print(f"[spike] spawned Godot pid={proc.pid} port={port} project={project}", flush=True)


def port_open():
    s = socket.socket()
    s.settimeout(1.0)
    try:
        s.connect(("127.0.0.1", port)); return True
    except Exception:
        return False
    finally:
        s.close()


deadline = time.time() + boot_timeout
while time.time() < deadline and not port_open():
    if proc.poll() is not None:
        print(f"[spike] FATAL Godot exited early rc={proc.returncode}", flush=True); sys.exit(2)
    time.sleep(2)
t_ready = time.time()
if not port_open():
    proc.terminate(); print("[spike] FATAL timed out waiting for LSP", flush=True); sys.exit(3)
print(f"[spike] LSP up after {t_ready - t_spawn:.0f}s", flush=True)

results = {"project": project, "port": port, "boot_seconds": round(t_ready - t_spawn, 1)}

# ---- Probe A: the dispatch's literal command line -------------------------
tA = time.time()
try:
    r = subprocess.run([LSPCLI, "diagnostics", "--project", project, "--port", str(port), "--json"],
                       capture_output=True, text=True, timeout=180)
    results["probeA"] = {"rc": r.returncode, "stdout": r.stdout[:20000],
                         "stderr": r.stderr[:4000], "seconds": round(time.time() - tA, 1)}
except subprocess.TimeoutExpired:
    results["probeA"] = {"rc": "timeout", "seconds": round(time.time() - tA, 1)}
print(f"[spike] probeA done: {results['probeA'].get('stdout','')[:200]!r}", flush=True)


# ---- Probe B: didOpen sweep -----------------------------------------------
class LSP:
    def __init__(self, port):
        self.s = socket.create_connection(("127.0.0.1", port), timeout=30)
        self.buf = b""
        self.n = 0
        self.diags = {}

    def send(self, obj):
        b = json.dumps(obj).encode()
        self.s.sendall(b"Content-Length: %d\r\n\r\n" % len(b) + b)

    def req(self, method, params):
        self.n += 1
        self.send({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params})
        return self.n

    def notify(self, method, params):
        self.send({"jsonrpc": "2.0", "method": method, "params": params})

    def pump(self, seconds):
        end = time.time() + seconds
        self.s.settimeout(0.5)
        while time.time() < end:
            try:
                chunk = self.s.recv(65536)
                if not chunk:
                    break
                self.buf += chunk
            except socket.timeout:
                continue
            while b"\r\n\r\n" in self.buf:
                head, rest = self.buf.split(b"\r\n\r\n", 1)
                ln = int([h for h in head.decode().split("\r\n") if h.lower().startswith("content-length")][0].split(":")[1])
                if len(rest) < ln:
                    break
                body, self.buf = rest[:ln], rest[ln:]
                try:
                    msg = json.loads(body)
                except Exception:
                    continue
                if msg.get("method") == "textDocument/publishDiagnostics":
                    p = msg["params"]
                    self.diags[p["uri"]] = p.get("diagnostics", [])


def to_uri(p):
    return "file://" + urllib.parse.quote(str(p))


c = LSP(port)
c.req("initialize", {"processId": os.getpid(), "rootUri": to_uri(project),
                     "rootPath": project,
                     "capabilities": {"textDocument": {"publishDiagnostics": {},
                                                       "synchronization": {"didSave": True}}}})
c.pump(4)
c.notify("initialized", {})
c.pump(2)

files = sorted(p for p in pathlib.Path(project).rglob("*.gd") if ".godot" not in p.parts)
tB = time.time()
for f in files:
    try:
        text = f.read_text(errors="replace")
    except Exception:
        continue
    c.notify("textDocument/didOpen", {"textDocument": {"uri": to_uri(f), "languageId": "gdscript",
                                                       "version": 1, "text": text}})
    c.pump(0.35)
c.pump(15)
results["probeB"] = {
    "files_opened": len(files),
    "seconds": round(time.time() - tB, 1),
    "files_with_diagnostics": sum(1 for v in c.diags.values() if v),
    "total_diagnostics": sum(len(v) for v in c.diags.values()),
    "by_severity": {},
    "diagnostics": {urllib.parse.unquote(k).replace("file://" + project + "/", ""): v
                    for k, v in c.diags.items() if v},
}
sev = {}
for v in c.diags.values():
    for d in v:
        sev[str(d.get("severity"))] = sev.get(str(d.get("severity")), 0) + 1
results["probeB"]["by_severity"] = sev
print(f"[spike] probeB: opened {len(files)} files, "
      f"{results['probeB']['total_diagnostics']} diagnostics in "
      f"{results['probeB']['files_with_diagnostics']} files", flush=True)

(outdir / f"{tag}_lsp.json").write_text(json.dumps(results, indent=2))

try:
    c.s.close()
except Exception:
    pass
proc.terminate()
try:
    proc.wait(timeout=30)
except subprocess.TimeoutExpired:
    proc.kill()
log.close()
print(f"[spike] godot stopped rc={proc.returncode}; total {time.time() - t_spawn:.0f}s", flush=True)
