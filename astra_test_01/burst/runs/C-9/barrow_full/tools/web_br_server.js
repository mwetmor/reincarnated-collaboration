// C-9 (copied from the /playtest/barrow/ measurement's scratch br_server.js, unchanged below this line)
// A static server that behaves like Vercel for the page's two big files: brotli (quality 4,
// calibrated against Vercel's measured transfer of the identical wasm and a cliffside pck) when
// the browser accepts br, cached in memory; everything else as-is. Logs each response.
//   node br_server.js <root> <port>
const http = require('http'); const fs = require('fs'); const path = require('path'); const zlib = require('zlib');
const root = process.argv[2]; const port = parseInt(process.argv[3] || '8792', 10);
const types = { '.html': 'text/html', '.js': 'application/javascript', '.wasm': 'application/wasm', '.pck': 'application/octet-stream', '.png': 'image/png' };
const cache = {};
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  const ae = req.headers['accept-encoding'] || '';
  const ext = path.extname(f);
  const hdr = { 'Content-Type': types[ext] || 'application/octet-stream', 'Cache-Control': 'no-store' };
  let body;
  if (/\bbr\b/.test(ae) && ['.wasm', '.pck', '.js', '.html'].includes(ext)) {
    const st = fs.statSync(f); const key = f + ':' + st.mtimeMs;
    if (!cache[key]) cache[key] = zlib.brotliCompressSync(fs.readFileSync(f), { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 4 } });
    body = cache[key]; hdr['Content-Encoding'] = 'br';
  } else { body = fs.readFileSync(f); }
  hdr['Content-Length'] = body.length;
  res.writeHead(200, hdr); res.end(body);
  console.log(`${new Date().toISOString()} ${p} ae="${ae}" sent=${body.length} ${hdr['Content-Encoding'] || 'identity'}`);
}).listen(port, '127.0.0.1', () => console.log('listening', port));
