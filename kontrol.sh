#!/usr/bin/env bash
# ArchiFrame video kalite denetimi — URETIM_KURALLARI.md içindeki ✅ kurallar.
# Kullanım: ./kontrol.sh video.mp4   (başarısızlıkta çıkış kodu 1)
set -uo pipefail
V="${1:?Kullanım: $0 video.mp4}"
[ -f "$V" ] || { echo "Dosya yok: $V"; exit 2; }

FAIL=0
ok()   { printf '  ✅ %s\n' "$1"; }
bad()  { printf '  ❌ %s\n' "$1"; FAIL=1; }
chk()  { if awk "BEGIN{exit !($2)}"; then ok "$1"; else bad "$1"; fi; }

probe() { ffprobe -v error -select_streams "$1" -show_entries "$2" -of csv=p=0 "$V" | head -1; }
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
W=$(probe v:0 stream=width); H=$(probe v:0 stream=height)
FPS=$(probe v:0 stream=r_frame_rate); VC=$(probe v:0 stream=codec_name); AC=$(probe a:0 stream=codec_name)

# Saniye başına ortalama parlaklık (0–255)
mapfile -t Y < <(ffmpeg -hide_banner -i "$V" -an \
  -vf "fps=1,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null - 2>/dev/null \
  | grep YAVG | cut -d= -f2)
YAVG=$(printf '%s\n' "${Y[@]}" | awk '{s+=$1} END{printf "%.1f", s/NR}')
YMIN=$(printf '%s\n' "${Y[@]}" | sort -n | head -1)
Y0=${Y[0]:-0}

# Ses yüksekliği
LOUD=$(ffmpeg -hide_banner -i "$V" -vn -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p')
LUFS=$(echo "$LOUD" | awk '/ I:/{print $2; exit}')
TP=$(echo "$LOUD"   | awk '/Peak:/{print $2; exit}')

echo "Denetim: $V"
chk "Süre 25–40 sn (ölçülen ${DUR%.*} sn)"                      "$DUR>=25 && $DUR<=40"
chk "Çözünürlük 1080x1920 (ölçülen ${W}x${H})"                    "$W==1080 && $H==1920"
chk "30 fps (ölçülen $FPS)"                                       "\"$FPS\"==\"30/1\""
chk "H.264 + AAC (ölçülen $VC + ${AC:-yok})"                      "\"$VC\"==\"h264\" && \"$AC\"==\"aac\""
chk "İlk saniye parlaklığı ≥ 35 (ölçülen $Y0)"                    "$Y0>=35"
chk "Ortalama parlaklık ≥ 35 (ölçülen $YAVG)"                     "$YAVG>=35"
chk "En karanlık saniye ≥ 22 (ölçülen $YMIN)"                     "$YMIN>=22"
chk "Ses -14 LUFS ±1,5 (ölçülen ${LUFS:-?} LUFS)"                 "${LUFS:--99}>=-15.5 && ${LUFS:--99}<=-12.5"
chk "Gerçek tepe ≤ -1 dBTP (ölçülen ${TP:-?} dBFS)"               "${TP:-0}<=-1"

if [ $FAIL -eq 0 ]; then echo "SONUÇ: GEÇTİ"; else echo "SONUÇ: KALDI — yüklemeden önce düzelt"; fi
exit $FAIL
