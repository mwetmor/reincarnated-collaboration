"""Compare my oracle trace to drax's filed one: byte sha, and canonical equality with composition.engine_src blanked."""
import json, sys, hashlib, gzip
mine, filed = sys.argv[1], sys.argv[2]
mb = open(mine,'rb').read(); fb = gzip.open(filed).read() if filed.endswith('.gz') else open(filed,'rb').read()
a = json.loads(mb); b = json.loads(fb)
ea, eb = a['composition'].get('engine_src'), b['composition'].get('engine_src')
a['composition']['engine_src'] = b['composition']['engine_src'] = None
eq = a == b
ca = json.dumps(a, sort_keys=True).encode(); cb = json.dumps(b, sort_keys=True).encode()
print(json.dumps({"mine_sha256": hashlib.sha256(mb).hexdigest(), "filed_sha256": hashlib.sha256(fb).hexdigest(),
  "byte_equal": mb == fb, "equal_modulo_engine_src": eq, "canon_sha256_equal": hashlib.sha256(ca).hexdigest()==hashlib.sha256(cb).hexdigest(),
  "engine_src_mine": ea, "engine_src_filed": eb}))
