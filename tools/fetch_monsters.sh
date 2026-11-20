#!/bin/bash
# Download Quaternius "Ultimate Monsters" (CC0) and list it
set -x
mkdir -p /tmp/mon && cd /tmp/mon
curl -sL -A "Mozilla/5.0" https://quaternius.com/packs/ultimatemonsters.html -o page.html; ls -la page.html
grep -oE 'https?://[^"'"'"' ]+' page.html | grep -iE 'drive|download|zip|itch' | sort -u | tee links.txt
pip install -q gdown
for u in $(grep -i drive links.txt); do gdown --fuzzy "$u" -O pack.zip && break; done
ls -la
unzip -l pack.zip | head -150 > $GITHUB_WORKSPACE/free/monsters_listing.txt || true
mkdir -p x && unzip -q -o pack.zip -d x || true
find x -iname '*.gltf' -o -iname '*.glb' | head -80
mkdir -p $GITHUB_WORKSPACE/free/monsters_src
find x \( -iname '*.gltf' -o -iname '*.glb' -o -iname '*.bin' -o -iname '*.png' -o -iname '*.jpg' \) -path '*gl[tT][fF]*' -exec cp {} $GITHUB_WORKSPACE/free/monsters_src/ \;
ls $GITHUB_WORKSPACE/free/monsters_src | head -100; du -sh $GITHUB_WORKSPACE/free/monsters_src
