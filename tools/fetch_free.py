# Pulls CC0 assets (Poly Haven textures/HDRIs, Kenney kits) into free/ on the GitHub runner.
import json, os, re, sys, urllib.request, zipfile, io
UA = {'User-Agent': 'splat-squad-asset-fetch/1.0'}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
def js(url): return json.loads(get(url))
os.makedirs('free/tex', exist_ok=True); os.makedirs('free/hdri', exist_ok=True); os.makedirs('free/kenney', exist_ok=True)
man = {'textures': {}, 'hdri': {}, 'kenney': {}, 'log': []}
def log(*a): print(*a); man['log'].append(' '.join(map(str, a)))
# ---------- Poly Haven textures ----------
WANT = {  # role: keyword lists, first match wins
 'marble_floor': ['marble_01', 'marble_tiles', 'marble'], 'polished_concrete': ['polished_concrete', 'concrete_floor_02', 'concrete_floor'],
 'wood_floor': ['wood_floor', 'laminate_floor', 'wood_planks'], 'tiles': ['floor_tiles', 'tiles_0', 'white_tiles'],
 'plaster': ['painted_plaster', 'plaster', 'white_plaster'], 'brushed_metal': ['metal_plate', 'brushed', 'metal_0'],
 'corrugated': ['corrugated_iron', 'rust_coarse', 'container'], 'asphalt': ['asphalt_02', 'asphalt', 'road'],
 'rooftop': ['concrete_tiles', 'roof_tiles', 'gravel_roof', 'concrete_wall'], 'brick': ['red_brick', 'brick_wall', 'brick'],
 'grass': ['grass_path', 'forrest_ground', 'grass'], 'sand': ['coast_sand', 'sand'], 'snow': ['snow_02', 'snow'],
 'wood_planks': ['wood_planks_grey', 'plank_flooring', 'weathered_planks', 'wood_planks'], 'rock': ['rock_face', 'rocks_ground', 'rock'],
 'fabric': ['fabric_pattern', 'denim', 'fabric'], 'leather': ['leather', 'fabric_leather'], 'carpet': ['carpet', 'dirty_carpet'],
 'skatepark_concrete': ['concrete_pavement', 'concrete_slab', 'patterned_concrete'], 'rubber': ['rubber_tiles', 'rubber'],
}
try:
    tex = js('https://api.polyhaven.com/assets?t=textures'); ids = sorted(tex.keys()); log('polyhaven textures', len(ids))
    used = set()
    for role, kws in WANT.items():
        pick = None
        for kw in kws:
            c = [i for i in ids if kw in i and i not in used]
            if c: pick = sorted(c, key=lambda i: -tex[i].get('download_count', 0))[0]; break
        if not pick: log('no texture for', role); continue
        used.add(pick); files = js('https://api.polyhaven.com/files/' + pick); got = {}
        for mapn, key in [('diff', 'Diffuse'), ('nor', 'nor_gl'), ('rough', 'Rough'), ('ao', 'AO'), ('arm', 'arm')]:
            node = files.get(key) or files.get(mapn)
            if not node: continue
            try:
                u = node['1k']['jpg']['url']; d = get(u); fn = f'free/tex/{role}_{mapn}.jpg'; open(fn, 'wb').write(d); got[mapn] = os.path.basename(fn)
            except Exception as e: log('miss', pick, key, e)
        man['textures'][role] = {'id': pick, 'files': got}; log('tex', role, pick, list(got))
except Exception as e: log('polyhaven textures failed', e)
# ---------- Poly Haven HDRIs ----------
try:
    hd = js('https://api.polyhaven.com/assets?t=hdris'); ids = sorted(hd.keys())
    HW = {'mall': ['shopping', 'mall', 'atrium', 'lobby', 'hall', 'museum', 'gallery'], 'night_city': ['night', 'moonlit', 'dikhololo_night', 'city_night'],
          'dusk': ['sunset', 'dusk', 'evening'], 'day': ['day', 'noon', 'sky', 'clear'], 'harbor': ['port', 'harbor', 'dock', 'pier'], 'snow': ['snow', 'winter']}
    used = set()
    for role, kws in HW.items():
        pick = None
        for kw in kws:
            c = [i for i in ids if kw in i and i not in used]
            if c: pick = sorted(c, key=lambda i: -hd[i].get('download_count', 0))[0]; break
        if not pick: log('no hdri', role); continue
        used.add(pick); f = js('https://api.polyhaven.com/files/' + pick)
        try: u = f['hdri']['1k']['hdr']['url']; open(f'free/hdri/{role}.hdr', 'wb').write(get(u)); man['hdri'][role] = pick; log('hdri', role, pick)
        except Exception as e: log('hdri miss', pick, e)
        try: u = f['tonemapped']['url'] if 'tonemapped' in f else None
        except Exception: u = None
except Exception as e: log('polyhaven hdri failed', e)
# ---------- Kenney kits (CC0) ----------
KITS = {'blaster-kit': ['https://opengameart.org/sites/default/files/kenney_blaster-kit_2.1.zip', 'https://opengameart.org/sites/default/files/kenney_blasterkit.zip'],
        'furniture-kit': ['https://opengameart.org/sites/default/files/kenney_furniture-kit.zip', 'https://opengameart.org/sites/default/files/kenney_furniturekit.zip'],
        'city-kit-commercial': ['https://opengameart.org/sites/default/files/kenney_city-kit-commercial_2.1.zip', 'https://opengameart.org/sites/default/files/kenney_city-kit-commercial.zip'],
        'food-kit': ['https://opengameart.org/sites/default/files/kenney_food-kit.zip', 'https://opengameart.org/sites/default/files/kenney_foodkit.zip']}
for kit, urls in KITS.items():
    ok = False
    for u in urls:
        try: d = get(u)
        except Exception as e: log('kit miss', u, e); continue
        try:
            z = zipfile.ZipFile(io.BytesIO(d)); n = 0
            for name in z.namelist():
                low = name.lower()
                if low.endswith('.glb') or (low.endswith('.png') and 'colormap' in low) or low.endswith('license.txt'):
                    out = f'free/kenney/{kit}/' + os.path.basename(name); os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'wb').write(z.read(name)); n += 1
            man['kenney'][kit] = n; log('kit', kit, n, 'files from', u); ok = True; break
        except Exception as e: log('kit bad zip', u, e)
    if not ok: log('kit failed', kit)
json.dump(man, open('free/manifest.json', 'w'), indent=1)
