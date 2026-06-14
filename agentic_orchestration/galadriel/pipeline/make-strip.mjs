// make-strip.mjs — side-by-side comparison strip for benchmark report evidence grid.
// usage: node make-strip.mjs out.png img1.jpg img2.jpg [img3.jpg ...]
import sharp from 'sharp';
const [out, ...imgs] = process.argv.slice(2);
const CELL_W = 480, CELL_H = 270, PAD = 4;
const cells = await Promise.all(imgs.map(p =>
  sharp(p).resize(CELL_W, CELL_H, { fit: 'cover' }).toBuffer()));
const totalW = CELL_W * imgs.length + PAD * (imgs.length + 1);
const totalH = CELL_H + PAD * 2;
const composites = cells.map((buf, i) => ({ input: buf, left: PAD + i * (CELL_W + PAD), top: PAD }));
await sharp({ create: { width: totalW, height: totalH, channels: 3, background: { r: 20, g: 20, b: 24 } } })
  .composite(composites).png().toFile(out);
console.log('wrote', out, `${totalW}x${totalH}`);
