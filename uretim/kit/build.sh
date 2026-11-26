#!/usr/bin/env bash
# Kullanım: bash uretim/kit/build.sh uretim/videoNN  →  videolar/NN-<ad>.mp4
# Klasörde: scene.html, audio.py, meta.json ({"cikti":"02-dikkat-testi.mp4", ...})
set -euo pipefail
DIR=$(cd "$1" && pwd); ROOT=$(cd "$(dirname "$0")/../.." && pwd)
OUT=$(python3 -c "import json;print(json.load(open('$DIR/meta.json'))['cikti'])")
TMP=$(mktemp -d)
( cd "$DIR" && PYTHONPATH="$ROOT/uretim/kit" python3 audio.py "$TMP/a.wav" )
node "$ROOT/uretim/render.js" "$DIR/scene.html" "$TMP/v.mp4" 30
mkdir -p "$ROOT/videolar"
ffmpeg -y -loglevel error -i "$TMP/v.mp4" -i "$TMP/a.wav" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest "$ROOT/videolar/$OUT"
rm -rf "$TMP"
echo "OK $ROOT/videolar/$OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/videolar/$OUT") sn"
