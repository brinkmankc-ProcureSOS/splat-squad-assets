#!/bin/bash
mkdir -p /tmp/mon && cd /tmp/mon
pip install -q gdown
python3 - <<'PY'
import gdown, json, subprocess, os
items = gdown.download_folder(url='https://drive.google.com/drive/folders/18m4KpzpEzhC9wl7jzr6dUc0N8Jozr79C', skip_download=True, quiet=True)
sel = [i for i in items if '/glTF/' in i.path]
print('total', len(items), 'gltf', len(sel))
os.makedirs('/tmp/mon/x', exist_ok=True)
lst = []
for i in sel:
    sub = i.path.split('/')[0]; name = os.path.basename(i.path); out = f'/tmp/mon/x/{sub}__{name}'
    url = f'https://drive.usercontent.google.com/download?id={i.id}&export=download&confirm=t'
    r = subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', '-o', out, '-w', '%{http_code} %{size_download}', url], capture_output=True, text=True)
    print(i.path, r.stdout); lst.append(i.path + ' ' + r.stdout)
open(os.environ['GITHUB_WORKSPACE'] + '/free/monsters_listing.txt', 'w').write('\n'.join(p.path for p in items))
PY
mkdir -p $GITHUB_WORKSPACE/free/monsters_src
# keep folder prefix in name, but gltf references its bin/png by plain name -> copy per folder
for d in $(ls x | sed 's/__.*//' | sort -u); do mkdir -p $GITHUB_WORKSPACE/free/monsters_src/$d; for f in x/${d}__*; do cp "$f" "$GITHUB_WORKSPACE/free/monsters_src/$d/${f#x/${d}__}"; done; done
find $GITHUB_WORKSPACE/free/monsters_src -type f | head -80; du -sh $GITHUB_WORKSPACE/free/monsters_src
head -c 300 $(find $GITHUB_WORKSPACE/free/monsters_src -name '*.gltf' | head -1)
