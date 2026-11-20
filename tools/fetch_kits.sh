#!/bin/bash
# CC0 Kenney kits via the public jam-ready-assets mirror -> game/kenney/<kit>/<model>.glb (+ listing)
set -e
KITS="city-kit-roads city-kit-suburban car-kit furniture-kit nature-kit mini-market mini-skate space-kit coaster-kit pirate-kit"
cd /tmp && rm -rf jra && git clone -q --depth 1 --filter=blob:none --sparse https://github.com/series-ai/jam-ready-assets.git jra && cd jra
git sparse-checkout set $(for k in $KITS; do echo kenney-$k; done)
OUT=$GITHUB_WORKSPACE/game/kenney; L=$GITHUB_WORKSPACE/free/kits_listing.txt; : > $L
for k in $KITS; do
  src=kenney-$k; [ -d $src ] || { echo "missing $k" >> $L; continue; }
  # prefer the GLB export folder
  files=$(find $src -iname '*.glb' | grep -viE 'preview|unity|godot' )
  [ -z "$files" ] && { echo "noglb $k $(find $src -type f | head -5)" >> $L; continue; }
  mkdir -p $OUT/$k
  for f in $files; do cp "$f" "$OUT/$k/$(basename "$f" | tr 'A-Z ' 'a-z_')"; done
  # textures referenced by GLBs are embedded; some kits use a shared colormap png next to the glb
  for p in $(find $src -iname 'colormap*.png' | head -1); do mkdir -p $OUT/$k/Textures; cp "$p" $OUT/$k/Textures/colormap.png; done
  echo "== $k $(ls $OUT/$k | wc -l) files $(du -sh $OUT/$k | cut -f1)" >> $L
  ls $OUT/$k | sed 's/\.glb$//' | tr '\n' ' ' >> $L; echo >> $L
done
cat $L | cut -c1-400
