#!/bin/bash
# Quaternius "Ultimate Monsters" (CC0) via a public GitHub mirror
set -e
cd /tmp && git clone -q --depth 1 --filter=blob:none --sparse https://github.com/series-ai/jam-ready-assets.git jra && cd jra
git sparse-checkout set quaternius-ultimate-monsters
find quaternius-ultimate-monsters -maxdepth 3 | head -30
S=quaternius-ultimate-monsters/3D/monster
find $S -type f | sed "s#$S/##" > $GITHUB_WORKSPACE/free/monsters_listing.txt
rm -rf $GITHUB_WORKSPACE/free/monsters_src; mkdir -p $GITHUB_WORKSPACE/free/monsters_src
for d in Big Blob Flying; do mkdir -p $GITHUB_WORKSPACE/free/monsters_src/$d; cp $S/$d/glTF/* $GITHUB_WORKSPACE/free/monsters_src/$d/; done
ls -la $GITHUB_WORKSPACE/free/monsters_src/Blob | head; du -sh $GITHUB_WORKSPACE/free/monsters_src
