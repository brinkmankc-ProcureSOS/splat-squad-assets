// Quaternius monsters -> single small .glb each (webp 512 textures), plus a manifest of bones/animations
import { NodeIO } from '@gltf-transform/core'; import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { prune, dedup, textureCompress, weld } from '@gltf-transform/functions'; import sharp from 'sharp'; import fs from 'fs'; import path from 'path';
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS); const src = 'free/monsters_src'; fs.mkdirSync('game/mon', { recursive: true }); const man = {};
for (const f of fs.readdirSync(src, { recursive: true }).filter(f => /\.(gltf|glb)$/i.test(f))) {
  try { const doc = await io.read(path.join(src, f)); await doc.transform(weld(), prune(), dedup(), textureCompress({ encoder: sharp, targetFormat: 'webp', resize: [512, 512], quality: 82 }));
    const id = f.replace(/\.(gltf|glb)$/i, '').replace('/', '_').toLowerCase().replace(/[^a-z0-9]+/g, '_'); const o = `game/mon/${id}.glb`; await io.write(o, doc);
    const R = doc.getRoot(); const tris = R.listMeshes().reduce((a, m) => a + m.listPrimitives().reduce((b, p) => b + (p.getIndices() ? p.getIndices().getCount() / 3 : 0), 0), 0);
    man[id] = { file: f, kb: Math.round(fs.statSync(o).size / 1024), tris, anims: R.listAnimations().map(a => a.getName()), bones: R.listNodes().filter(n => !n.getMesh()).map(n => n.getName()).slice(0, 60), mats: R.listMaterials().map(m => m.getName()) };
    console.log(id, man[id].kb + 'KB', tris, man[id].anims.join(','));
  } catch (e) { console.log('fail', f, e.message); }
}
fs.writeFileSync('game/mon/manifest.json', JSON.stringify(man, null, 1));
