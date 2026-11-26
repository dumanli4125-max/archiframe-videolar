# syntetic.tr video ofisi

Bu depo, **syntetic.tr** (Instagram) ve **Syntetic** (YouTube, eski adı taktiktahtası) için günde 3 adet ~60 sn'lik
dikey (1080x1920) animasyon videosu üretir. Onaylanmış referans video: `uretim/video01/` (Mesai Bitmiyor).

## Ekip (ajanlar: `.claude/agents/`)

| Ajan | Görev | Çıktı |
|------|-------|-------|
| `senarist` | Konudan senaryo yazar (halk ağzı, kanca, final) | `uretim/videoNN/senaryo.md` |
| `seslendirmen` | Satırları seslendirir, yazıya döker, kelime zamanlarını çıkarır | `seslendirme/lXX.wav`, `zamanlama.json` |
| `animator` | Kiti kullanarak sahneyi ve ses miksini kurar, render alır | `scene.html`, `audio.py`, `videolar/NN-ad.mp4` |
| `kalite-kontrol` | Kareleri ve zamanlamayı denetler, düzeltme listesi verir | rapor |
| `yayinci` | Instagram Reel + YouTube Shorts olarak paylaşır, kaydı tutar | `uretim/YAYIN_LOG.md` |

Tek videoyu baştan sona tek bir ajan da üretebilir (aşağıdaki akış). Ajanlar git commit/push YAPMAZ; ana oturum yapar.

## Üslup kuralları (kullanıcının onayladığı, değiştirme)

1. **Halk ağzı, kahvede anlatır gibi.** "Kim olacak, patron." "Oh be, dünya varmış." "Arkası kesilmedi tabii." "Beleşe mesai."
2. **Mecaz yükleme, kitap dili kullanma.** "Ofis senden çıkmadı" gibi soyut cümleler YASAK. Somut, ilk duyuşta anlaşılır.
3. **Hikâye aktif ilerlesin.** Kenardan yorum ("Hadi canım...") yerine olayı ileri taşıyan cümle ("Derler de... bizim patron öyle demiyor.").
4. **İlk 2 sn soru kancası**, ikinci tekil şahıs: "Mesain kaçta bitiyor? Hadi, düşünmeden söyle."
5. **Duygusal dönüm noktası** (çocuk, anne, yalnızlık vb.) ve **somut final eylemi**: "Git, o masalı oku."
6. Süre **~60 sn** (55–65). 10–12 anlatım satırı, her satır 3–6.5 sn.
7. Saat/sayı söyleniyorsa ses **ayrık ve yavaş** okunmalı ("Akşam... saat altı."), ekrandaki saat tam o kelimede değişmeli.

## Görsel kurallar

- Palet: gece mavisi zemin, kehribar `#ffb547` ışık/vurgu, mercan `#ff6b5b` = **SEN**, krem `#efe4cf` diğer insanlar, teal `#5fd3c6` ekran/sakinlik.
- Karakter: kalın kapsül gövde + yuvarlak kafa + iki göz (`figure()`). SEN her zaman mercan ve üstünde `SEN` etiketi.
- Karakterler **hep hareket etsin**: yürüme, yazma, nefes, göz kırpma (motor otomatik), el kaldırma, baş düşürme.
- Altyazı üstte (y≈240), en fazla 2 satır, 62–74 px, satır başına ≤ 26 karakter. Vurgu kelimesi renkli.
- Sahnede etiketler (`tag()`): OFİS, EV, MESAİ, ÇOCUĞUN gibi kısa büyük harf.
- Son 2–3 sn: karartma + büyük final cümlesi + `endCard()`.
- Diyalektik.tr ya da başka sayfaların karakter/görsellerini birebir kopyalama; fikir benzer, çizim bizim.

## Dosya düzeni

```
uretim/
  kit/engine.js       ortak çizim motoru (figure, POSE, walk, room, sofa, desk, phone, caption, bubble, notif, card, countdown, endCard...)
  kit/audio_kit.py    ses kiti (Mix: vo, pad, note, keyboard, steps, buzz, ping, tick, click, thud, whoosh, ding, tension)
  kit/build.sh        bash uretim/kit/build.sh uretim/videoNN   → videolar/<meta.cikti>
  kit/stills.sh       bash uretim/kit/stills.sh uretim/videoNN 2,10,30 <klasör>  → sheet.png (kontrol kareleri)
  render.js           Playwright ile kare kare render
  sablon/             yeni video için kopyalanacak şablon (scene.html, audio.py, meta.json)
  KONULAR.md          konu listesi + durum
  BIYOGRAFI.md        profil metinleri
  YAYIN_LOG.md        paylaşım kaydı
  videoNN/            her video: senaryo.md, seslendirme/, zamanlama.json, scene.html, audio.py, meta.json
videolar/             çıktı MP4'ler (NN-kisa-ad.mp4)
```

## Üretim akışı (bir video)

1. **Konu seç**: `uretim/KONULAR.md` içinde ⏳ olan, günlük karışıma uyan konu (12:30 test/bilgi, 18:30 ve 21:30 hikâye).
2. **Klasör**: `cp -r uretim/sablon uretim/videoNN` (NN = sıradaki numara, iki hane).
3. **Senaryo** (`senaryo.md`): satır listesi + her satırın sahnede ne olduğu + altyazı metni.
4. **Seslendirme** (Speko MCP, ücretsiz kredi):
   - `mcp__Speko__audio_synthesize` body:
     `{"text": "...", "intent": {"language":"tr","optimizeFor":"accuracy"}, "voice":"39f753ef-b0eb-41cd-aa53-2f3c284f948f", "model":"sonic-3.5", "speed":0.85, "constraints":{"allowedProviders":{"tts":["cartesia"]}}}`
     (ses: Cartesia "Emre"; sayı/saat içeren ya da vurgulu satırlarda `speed` 0.8)
   - Sonuç büyük olduğu için dosyaya kaydedilir. Hata metnindeki dosyayı JSON olarak oku: `d[0].text` içinde
     `saved to <...>.wav` yolu (ses), `d[1].text` JSON'unda `url` (15 dk geçerli). WAV'ı `seslendirme/lXX.wav` olarak kopyala.
   - `mcp__Speko__audio_transcribe` (`audio_url`=url, `language`="tr", `word_timestamps`=true) ile **mutlaka** doğrula:
     kelimeler doğru mu, sayılar doğru okunuyor mu. Önemli kelimelerin ms zamanlarını `zamanlama.json`'a yaz.
   - Telaffuz bozuksa metni değiştirip yeniden üret (noktalama/üç nokta ile duraklama ver).
   - Alternatif (kredi varsa): ElevenLabs `creative_generate_speech`, ses "Demir" `z9fa8b150eX19waPShFp`, model `eleven_v4`, `generations_count: 1`.
5. **Zaman çizelgesi**: satır başlangıçları = önceki satır sonu + 0.2–0.5 sn. Sahne olayları (saat değişimi, el kaldırma, ışık sönmesi,
   bildirim) ilgili kelimenin zamanına oturur. Satır sığmıyorsa `m.vo(..., tempo=1.06)` (perde korunur, en fazla 1.08).
6. **Sahne** (`scene.html`): kitin fonksiyonlarıyla çiz; `video01/scene.html` ve `sablon/scene.html` örnek. `DURATION` = son satır sonu + ~3 sn.
7. **Ses** (`audio.py`): `Mix(D=DURATION)`; `m.vo()` başlangıçları scene ile aynı; efektler olaylara denk.
8. **Kontrol kareleri**: `bash uretim/kit/stills.sh uretim/videoNN <8-10 zaman> <scratch klasör>` → sheet.png'yi Read ile gör.
   Kontrol listesi: yazılar üst üste binmiyor mu, altyazı ekrana sığıyor mu, karakterler objelerin içinden geçmiyor mu,
   SEN etiketi okunuyor mu, final kartı temiz mi.
9. **Render**: `bash uretim/kit/build.sh uretim/videoNN` (≈3 dk / 60 sn). Çıktı `videolar/NN-ad.mp4`, -14 LUFS.
10. **Kayıt**: `meta.json`'a başlık, Instagram açıklaması, hashtag'ler, YouTube başlığı ekle (bkz. yayinci ajanı).

## Yayın

- Instagram: `mcp__vidIQ__vidiq_instagram_publish_reel` (hesap vidIQ'ya bağlı olmalı: `vidiq_social_account_list`).
  Video URL'si için önce `vidiq_video_upload` (public URL: GitHub raw linki
  `https://raw.githubusercontent.com/dumanli4125-max/archiframe-videolar/<dal>/videolar/<dosya>.mp4`).
- YouTube Shorts: vidIQ'ya bağlı kanal üzerinden (Syntetic / eski taktiktahtası).
- Her paylaşım `uretim/YAYIN_LOG.md`'ye tarih, platform, dosya, link olarak yazılır; `KONULAR.md`'de durum ✅ yapılır.
- Şifre/kimlik bilgisi asla depoya, loga ya da zamanlanmış görev metnine yazılmaz.
