#!/usr/bin/env bash
# Kontrol kareleri: bash uretim/kit/stills.sh uretim/videoNN 2,10,25,40 <çıktı_klasörü> [en]  → <çıktı>/sheet.png
set -euo pipefail
DIR=$(cd "$1" && pwd); ROOT=$(cd "$(dirname "$0")/../.." && pwd); OUTD=$3; mkdir -p "$OUTD"; rm -f "$OUTD"/s_*.png
node "$ROOT/uretim/render.js" "$DIR/scene.html${4:+?lang=$4}" --stills "$2" "$OUTD"
python3 - "$OUTD" <<'PY'
import sys,glob
from PIL import Image
d=sys.argv[1];fs=sorted(glob.glob(d+'/s_*.png'),key=lambda f:float(f.split('s_')[-1][:-4]))
ims=[Image.open(f).resize((270,480)) for f in fs];cols=min(5,len(ims));rows=(len(ims)+cols-1)//cols
c=Image.new('RGB',(270*cols,480*rows));[c.paste(im,((i%cols)*270,(i//cols)*480)) for i,im in enumerate(ims)];c.save(d+'/sheet.png');print(d+'/sheet.png')
PY
