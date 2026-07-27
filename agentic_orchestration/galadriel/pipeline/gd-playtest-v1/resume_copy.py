#!/usr/bin/env python3
"""
Resume a byte-exact copy of the run video from the SMB share.

The share is a Raspberry Pi over SMB at ~3 MB/s and a plain `cp` of the 13 GB
file was reaped mid-transfer twice. This appends from wherever the local file
already ends and retries on transient I/O errors, so a dropped mount costs
seconds rather than a restart.

Verifies size on completion. Does not verify content hash -- that would cost a
second full read of the share, which is the exact resource under contention.
Sequential append plus an exact size match is the affordable check.
"""

import argparse
import os
import sys
import time

CHUNK = 4 * 1024 * 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--retries", type=int, default=50)
    args = ap.parse_args()

    total = os.path.getsize(args.src)
    done = os.path.getsize(args.dst) if os.path.exists(args.dst) else 0
    print(f"src={total} dst={done} remaining={total-done} "
          f"({100.0*done/total:.1f}% already present)", flush=True)

    attempt = 0
    last_report = time.time()
    while done < total:
        try:
            with open(args.src, "rb") as fi, open(args.dst, "r+b" if done else "wb") as fo:
                fi.seek(done)
                fo.seek(done)
                while done < total:
                    buf = fi.read(CHUNK)
                    if not buf:
                        break
                    fo.write(buf)
                    done += len(buf)
                    if time.time() - last_report > 30:
                        print(f"  {done/1e9:.2f}/{total/1e9:.2f} GB "
                              f"({100.0*done/total:.1f}%)", flush=True)
                        last_report = time.time()
                fo.flush()
                os.fsync(fo.fileno())
        except OSError as e:
            attempt += 1
            if attempt > args.retries:
                sys.exit(f"giving up after {attempt} retries: {e}")
            print(f"  I/O error at {done} ({e}); retry {attempt}", flush=True)
            time.sleep(5)
            done = os.path.getsize(args.dst)

    final = os.path.getsize(args.dst)
    if final != total:
        sys.exit(f"SIZE MISMATCH: {final} != {total}")
    print(f"COPY COMPLETE {final} bytes", flush=True)


if __name__ == "__main__":
    main()
