// Render preview stills without re-bundling for every frame.
// usage: node scripts/stills.mjs scene:seg:frac [scene:seg:frac ...]
//   e.g. node scripts/stills.mjs intro:0:0.5 rahmen:3:0.9 credits:-:300
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const script = JSON.parse(fs.readFileSync(path.join(root, 'src/data/script.json'), 'utf8'));
const timing = JSON.parse(fs.readFileSync(path.join(root, 'src/data/timing.json'), 'utf8'));
const FPS = 30;
const CARD = Math.round(2.6 * FPS);
const LEAD = Math.round(0.5 * FPS);
const GAP = Math.round(0.55 * FPS);

function segFrame(id, seg, frac) {
  const scene = script.scenes.find((s) => s.id === id);
  let t = (scene.chapter ? CARD : 0) + LEAD;
  const secs = timing[id];
  for (let i = 0; i < seg; i++) t += Math.ceil(secs[i] * FPS) + GAP;
  return Math.round(t + frac * Math.ceil(secs[seg] * FPS));
}

const browserExecutable = process.env.REMOTION_BROWSER ?? '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const serveUrl = await bundle({ entryPoint: path.join(root, 'src/index.ts') });
fs.mkdirSync(path.join(root, 'out/stills'), { recursive: true });

for (const spec of process.argv.slice(2)) {
  const [id, seg, frac] = spec.split(':');
  const frame = seg === '-' ? Number(frac) : segFrame(id, Number(seg), Number(frac));
  const composition = await selectComposition({ serveUrl, id: `S-${id}`, browserExecutable, inputProps: { id } });
  const output = path.join(root, `out/stills/${id}-${seg}-${frac}.png`);
  await renderStill({ composition, serveUrl, output, frame, browserExecutable, inputProps: { id } });
  console.log(output);
}
