#!/usr/bin/env bash
# Kullanım: bash uretim/kit/build.sh uretim/videoNN [en]
#   tr (varsayılan): scene.html + audio.py      → videolar/<meta.cikti>
#   en             : scene.html?lang=en + audio_en.py → videolar/en/<meta.cikti_en>
set -euo pipefail
DIR=$(cd "$1" && pwd); LANGX=${2:-tr}; ROOT=$(cd "$(dirname "$0")/../.." && pwd)
if [ "$LANGX" = "en" ]; then KEY=cikti_en; AUD=audio_en.py; Q="?lang=en"; OUTD="$ROOT/videolar/en"; else KEY=cikti; AUD=audio.py; Q=""; OUTD="$ROOT/videolar"; fi
OUT=$(python3 -c "import json;print(json.load(open('$DIR/meta.json'))['$KEY'])")
TMP=$(mktemp -d); mkdir -p "$OUTD"
( cd "$DIR" && PYTHONPATH="$ROOT/uretim/kit" python3 "$AUD" "$TMP/a.wav" )
node "$ROOT/uretim/render.js" "$DIR/scene.html$Q" "$TMP/v.mp4" 30
bash "$ROOT/uretim/kit/loudnorm.sh" "$TMP/a.wav" "$TMP/a.m4a"
ffmpeg -y -loglevel error -i "$TMP/v.mp4" -i "$TMP/a.m4a" -c copy -shortest "$OUTD/$OUT"
rm -rf "$TMP"
echo "OK $OUTD/$OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUTD/$OUT") sn"
