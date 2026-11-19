# Download realistic CC0 props from Poly Haven (glTF, 1k textures) into free/ph/<id>/
import json, os, urllib.request
UA = {'User-Agent': 'splat-squad-asset-fetch/1.0'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
def js(u): return json.loads(get(u))
assets = js('https://api.polyhaven.com/assets?t=models'); ids = sorted(assets)
KW = ['potted_plant', 'planter', 'fern', 'bush', 'tree', 'bench', 'sofa', 'armchair', 'chair', 'table', 'lamp', 'street_lamp', 'barrel', 'crate', 'pallet', 'cone', 'hydrant', 'trash', 'bin', 'vending', 'shelf', 'speaker', 'boombox', 'tire', 'tyre', 'rock', 'boulder', 'statue', 'fountain', 'sign', 'neon', 'skate', 'basketball', 'bicycle', 'scooter', 'mannequin', 'cart']
picked, man = [], {}
for kw in KW:
    c = [i for i in ids if kw in i and i not in picked]
    c.sort(key=lambda i: -assets[i].get('download_count', 0))
    picked += c[:2]
picked = [i for i in picked if (assets[i].get('polycount') or 0) < 400000][:44]
os.makedirs('free/ph', exist_ok=True)
for mid in picked:
    try:
        f = js('https://api.polyhaven.com/files/' + mid); g = f['gltf']['1k']['gltf']; d = f'free/ph/{mid}'; os.makedirs(d, exist_ok=True)
        open(f'{d}/{mid}.gltf', 'wb').write(get(g['url']))
        for rel, info in g.get('include', {}).items():
            p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(get(info['url']))
        man[mid] = {'name': assets[mid].get('name'), 'tags': assets[mid].get('tags', []), 'polycount': assets[mid].get('polycount')}; print('ok', mid, man[mid]['polycount'])
    except Exception as e: print('miss', mid, e)
json.dump(man, open('free/ph/manifest.json', 'w'), indent=1)
