#!/bin/bash
# Download Quaternius "Ultimate Monsters" (CC0) and list it
set -x
mkdir -p /tmp/mon && cd /tmp/mon
curl -sL -A "Mozilla/5.0" https://quaternius.com/packs/ultimatemonsters.html -o page.html; ls -la page.html
grep -oE 'https?://[^"'"'"' ]+' page.html | grep -iE 'drive|download|zip|itch' | sort -u | tee links.txt
pip install -q gdown
for u in $(grep -i drive links.txt); do gdown --folder "$u" -O dl --remaining-ok || gdown --folder "$u" -O dl; done
find dl -type f | head -50
for z in $(find dl -iname '*.zip'); do echo "== $z"; unzip -l "$z" | tail -3; done
mkdir -p x; for z in $(find dl -iname '*.zip' | grep -iE 'gltf|glb'); do unzip -q -o "$z" -d x; done
[ -z "$(ls x)" ] && for z in $(find dl -iname '*.zip'); do unzip -q -o "$z" -d x; done
cp -r dl/* x/ 2>/dev/null
ls -la
find x -type f | head -300 > $GITHUB_WORKSPACE/free/monsters_listing.txt
find x -iname '*.gltf' -o -iname '*.glb' | head -80
mkdir -p $GITHUB_WORKSPACE/free/monsters_src
find x \( -iname '*.gltf' -o -iname '*.glb' -o -iname '*.bin' -o -iname '*.png' -o -iname '*.jpg' \) -exec cp {} $GITHUB_WORKSPACE/free/monsters_src/ \;
ls $GITHUB_WORKSPACE/free/monsters_src | head -100; du -sh $GITHUB_WORKSPACE/free/monsters_src
