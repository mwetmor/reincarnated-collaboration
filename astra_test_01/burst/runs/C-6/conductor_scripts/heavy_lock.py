# Shared advisory lock for heavy work on the 8 GB Mac (Gate-1 WARN-6, C-6 charter § 7.2): heavy_lock.py <run> -- <cmd...>
# Exclusive fcntl lock on ~/astra-burst/.heavy.lock; the holder writes pid/run/ts into it (a dead pid is stale by definition).
import sys, os, fcntl, subprocess, json, time, pathlib
L = pathlib.Path.home()/'astra-burst'/'.heavy.lock'; L.parent.mkdir(exist_ok=True)
run = sys.argv[1]; cmd = sys.argv[sys.argv.index('--')+1:]
with L.open('a+') as f:
    t0=time.time()
    try: fcntl.flock(f, fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        f.seek(0); print(f'heavy_lock: waiting — held by {f.read().strip()[:120]}', flush=True); fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0); f.truncate(); f.write(json.dumps(dict(pid=os.getpid(), run=run, ts=time.strftime('%FT%TZ', time.gmtime()), cmd=' '.join(cmd)[:200]))); f.flush()
    print(f'heavy_lock: acquired after {time.time()-t0:.0f}s ({run})', flush=True)
    rc = subprocess.call(cmd)
    f.seek(0); f.truncate()
sys.exit(rc)
