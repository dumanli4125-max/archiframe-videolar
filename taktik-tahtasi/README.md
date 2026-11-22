# Taktik Tahtası · takım sistemi video şablonu

Onaylı stil (22 Kasım 2026): koyu yeşil zemin, metalik başlık, turuncu vurgu, perspektifli diziliş tahtası, kelime kelime altyazı.

## Klasörler
- `ornek/` — onaylı örnek videolar (Örnek FK, **temsili veri**; yayın için değil)
  - `taktik-tahtasi-ornek-sistem.mp4` — dikey 1080×1920 → Shorts + Reels
  - `taktik-tahtasi-ornek-sistem-yatay.mp4` — yatay 1920×1080 → YouTube video
- `sablon/` — videoyu üreten kod
  - `scene.html` — tüm sahneler (canvas, `render(t)` ile kare kare). Başlıklar `HEAD`, altyazılar `CAP`, istatistikler `STATS`, oyuncular `OPP` / `US` dizilerinde.
  - `render.js` — Playwright + ffmpeg ile kare kare render
  - `ses.py` — müzik ve ses efektleri (numpy)
  - `fonts/` — Barlow Condensed, IBM Plex Mono (SIL OFL, lisans metinleri yanında)

## Üretim
```bash
cd taktik-tahtasi/sablon
python3 ses.py                       # audio.wav
node render.js full                  # dikey: video_noaudio.mp4
LAND=1 node render.js full           # yatay: video_h_noaudio.mp4
ffmpeg -i video_noaudio.mp4 -i audio.wav -c:v copy -c:a aac -shortest -movflags +faststart dikey.mp4
ffmpeg -i video_h_noaudio.mp4 -i audio.wav -c:v copy -c:a aac -shortest -movflags +faststart yatay.mp4
node render.js stills 4.5 16.5       # kontrol için tek kareler (still_*.jpg)
```

Gerçek videoda: veriler Maçkolik'ten, seslendirme klon sesle; altyazı zamanları (`CAP`) seslendirmenin kelime hizalamasına göre güncellenir, müzik konuşma altında kısılır.

Not: Depo kökündeki video vidIQ aktarımı içindir; bu klasör ona dokunmaz.
