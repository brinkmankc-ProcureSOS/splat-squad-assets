# Fetch Kenney CC0 kits from their OpenGameArt pages (finds the zip link on the page).
import re, os, io, zipfile, urllib.request, json, sys
UA = {'User-Agent': 'Mozilla/5.0 splat-squad-asset-fetch'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
PAGES = {'cube-pets': 'https://opengameart.org/node/185352'}
for kit, page in PAGES.items():
    html = get(page).decode('utf8', 'ignore'); links = sorted(set(re.findall(r'https?://opengameart\.org/sites/default/files/[^"\']+\.zip', html)))
    print(kit, links)
    for u in links:
        try:
            z = zipfile.ZipFile(io.BytesIO(get(u))); n = 0
            for name in z.namelist():
                low = name.lower()
                if low.endswith('.glb') or (low.endswith('.png') and ('colormap' in low or 'texture' in low)) or low.endswith('license.txt'):
                    out = f'free/kenney/{kit}/' + os.path.basename(name); os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'wb').write(z.read(name)); n += 1
            print(kit, n, 'files'); 
            if n: break
        except Exception as e: print('bad', u, e)
