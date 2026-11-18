"""Download a free ("name your own price", $0) itch.io pack without an account and extract model files.
Usage: python fetch_itch.py <itch page url> <out dir> [filename substring]"""
import re, sys, json, zipfile, io, os, urllib.request, urllib.parse, http.cookiejar
page, out = sys.argv[1], sys.argv[2]; want = sys.argv[3] if len(sys.argv) > 3 else ''
cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36')]
def get(u, data=None, hdr=None):
    req = urllib.request.Request(u, data=data, headers=hdr or {})
    with op.open(req, timeout=120) as r: return r.read(), r.geturl()
html, _ = get(page); html = html.decode('utf8', 'ignore')
csrf = re.search(r'name="csrf_token" value="([^"]+)"', html) or re.search(r'"csrf_token":"([^"]+)"', html)
csrf = csrf.group(1) if csrf else ''
body, _ = get(page.rstrip('/') + '/download_url', urllib.parse.urlencode({'csrf_token': csrf}).encode(), {'X-Requested-With': 'XMLHttpRequest'})
dl = json.loads(body)['url']; print('download page', dl)
dhtml, _ = get(dl); dhtml = dhtml.decode('utf8', 'ignore')
uploads = re.findall(r'data-upload_id="(\d+)"', dhtml)
names = re.findall(r'class="name"[^>]*title="([^"]+)"', dhtml) or re.findall(r'<strong class="name"[^>]*>([^<]+)<', dhtml)
print('uploads', uploads, names)
key = re.search(r'/download/([^?/#"]+)', dl).group(1)
for m in re.finditer(r'<script[^>]*>(.*?)</script>', dhtml, re.S):
    t = m.group(1)
    if 'key' in t or 'Download' in t: print('SCRIPT', t[:600].replace('\n',' '))
csrf2 = re.search(r'name="csrf_token" value="([^"]+)"', dhtml); csrf2 = csrf2.group(1) if csrf2 else csrf
os.makedirs(out, exist_ok=True)
for i, up in enumerate(uploads):
    nm = names[i] if i < len(names) else up
    if want and want.lower() not in nm.lower(): continue
    fb, _ = get(page.rstrip('/') + f'/file/{up}?source=game_download&key={key}', urllib.parse.urlencode({'csrf_token': csrf2}).encode(), {'X-Requested-With': 'XMLHttpRequest'})
    j = json.loads(fb); print('file resp', str(j)[:300])
    if 'url' not in j:
        fb, _ = get(f'https://itch.io/download/{key}/file/{up}' if False else page.rstrip('/') + f'/file/{up}?source=game_download&key={key}&after_download_lightbox=true', urllib.parse.urlencode({'csrf_token': csrf2}).encode(), {'X-Requested-With': 'XMLHttpRequest', 'Referer': dl})
        j = json.loads(fb); print('file resp2', str(j)[:300])
    furl = j['url']; print('fetching', nm)
    data, _ = get(furl)
    open(os.path.join(out, 'pack.zip'), 'wb').write(data); print('bytes', len(data))
    z = zipfile.ZipFile(io.BytesIO(data))
    for n in z.namelist():
        print(n)
    for n in z.namelist():
        low = n.lower()
        if low.endswith(('.glb', '.gltf', '.bin', '.png', '.jpg', '.txt')) and '__macosx' not in low:
            dst = os.path.join(out, 'files', n); os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(z.read(n))
    os.remove(os.path.join(out, 'pack.zip'))
    break
