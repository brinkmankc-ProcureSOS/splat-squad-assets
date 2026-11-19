// Shrink Poly Haven props for phones: simplify to ~6k triangles, 512px webp textures, single .glb
import { NodeIO } from '@gltf-transform/core'; import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { simplify, weld, prune, dedup, textureCompress } from '@gltf-transform/functions'; import { MeshoptSimplifier } from 'meshoptimizer'; import sharp from 'sharp'; import fs from 'fs'; import path from 'path';
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS); const man = JSON.parse(fs.readFileSync('free/ph/manifest.json')); fs.mkdirSync('game/ph', { recursive: true }); const out = {};
await MeshoptSimplifier.ready;
for (const [id, info] of Object.entries(man)) {
  try { const src = `free/ph/${id}/${id}.gltf`; if (!fs.existsSync(src)) continue; const doc = await io.read(src);
    const tris = info.polycount || 10000, ratio = Math.min(1, 6000 / tris);
    await doc.transform(weld(), ...(ratio < 1 ? [simplify({ simplifier: MeshoptSimplifier, ratio, error: 0.02 })] : []), prune(), dedup(), textureCompress({ encoder: sharp, targetFormat: 'webp', resize: [512, 512], quality: 80 }));
    const o = `game/ph/${id}.glb`; await io.write(o, doc); out[id] = { ...info, kb: Math.round(fs.statSync(o).size / 1024) }; console.log(id, tris, '->', out[id].kb + 'KB'); }
  catch (e) { console.log('fail', id, e.message); }
}
fs.writeFileSync('game/ph/manifest.json', JSON.stringify(out, null, 1));
