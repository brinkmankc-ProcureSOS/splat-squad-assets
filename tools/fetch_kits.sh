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
  n=$(find $src -iname '*.glb' | grep -viE 'preview|unity|godot' | wc -l)
  [ "$n" = "0" ] && { echo "noglb $k" >> $L; continue; }
  mkdir -p $OUT/$k
  find $src -iname '*.glb' | grep -viE 'preview|unity|godot' | while IFS= read -r f; do b=$(basename "$f" | tr 'A-Z ' 'a-z_'); cp "$f" "$OUT/$k/$b"; done
  p=$(find $src -iname 'colormap*.png' | head -1); if [ -n "$p" ]; then mkdir -p $OUT/$k/Textures; cp "$p" $OUT/$k/Textures/colormap.png; fi
  echo "== $k $(ls $OUT/$k | wc -l) files $(du -sh $OUT/$k | cut -f1)" >> $L
  ls $OUT/$k | sed 's/\.glb$//' | tr '\n' ' ' >> $L; echo >> $L
done
cat $L | cut -c1-400
