# ArchiFrame üretim kuralları (v1)

Amaç: Reels / Shorts'ta izlenme süresini ve tekrar izlenmeyi artırmak.
Her kural ya ölçülebilir (✅ `kontrol.sh` denetler) ya da üretim sırasında uygulanır (✍️).
Eşikler deneyimsel başlangıç değerleridir; 10–15 video sonra izlenme verisine göre güncellenmeli.

Mevcut `kombisiz-site-dikey-yt.mp4` ölçümü (referans): süre 56 sn · ort. parlaklık 27,7/255 ·
ilk saniye 16,8/255 · ses -29,3 LUFS. Aşağıdaki kuralların çoğu bu açıkları kapatmak için.

---

## 1. İlk 1,5 saniye (kanca)
- ✍️ **Kare 0 boş olamaz.** Ana nesne (bina, kombi, depo…) ilk karede tamamen çizilmiş ve görünür olur. "Çizilerek belirme" animasyonu en fazla 0,5 sn.
- ✍️ İlk karede **paradoks başlık**: en fazla 6 kelime, iki satır. Örnek kalıp: "Kombi yok, ev sıcacık" · "Tek alev, iki iş" · "Bu delik neden var?"
- ✅ İlk saniyenin ortalama parlaklığı ≥ 35/255 (siyah açılış kaydırılır).
- ✍️ İlk 1,5 sn içinde hareket başlar (akış oku, dönen parça, su seviyesi vb.).

## 2. Süre ve tempo
- ✅ Süre **25–40 sn**. Daha uzun konu → iki bölüme böl ("Bölüm 1/2").
- ✍️ En fazla **5 sahne**; her sahne 4–8 sn.
- ✍️ Hiçbir an 3 sn'den uzun **durağan** kalmaz: her 2–3 sn'de yeni etiket, kamera kayması, yakınlaşma ya da akış animasyonu.
- ✍️ Her sahne tek bir fikir anlatır; altyazı tek cümle.

## 3. Görünürlük (en büyük açık)
- ✅ Video boyunca ortalama parlaklık ≥ 35/255; hiçbir saniye < 22/255 olamaz.
- ✍️ Arka plan koyu lacivert kalabilir (#0E1A2E – #13213A), ama **sahne çizgileri parlak** olur:
  ana hatlar #9FB6D9 veya daha açık, kalınlık ≥ 3 px (1080p'de), vurgu rengi yalnızca anlatılan parça.
- ✍️ Sahne (bina/oda/cihaz) her karede ekranın **en az %40'ını** kaplar. Etiketler sahnenin yerine geçmez, sahneyi işaret eder.
- ✍️ İzometrik tek kamera açısı tüm seride sabit; sahne geçişi = kamera yakınlaşması, kesme değil.

## 4. Yazı ve güvenli alan
- ✍️ Instagram/YouTube arayüzü alt ~%25'i ve sağ ~%12'yi örter. **Tüm yazılar y = 220–1400 px, x = 60–940 px** aralığında (1080×1920).
  (Mevcut videoda altyazı kutuları y ≈ 1400–1620'de → kısmen arayüz altında kalıyor.)
- ✍️ Altyazı: en fazla 2 satır, satır başına ≤ 38 karakter, ≥ 46 px kalın yazı, yarı saydam kutu.
- ✍️ Etiket (KAZAN DAİRESİ vb.): ≤ 3 kelime, büyük harf, ince işaret çizgisiyle nesneye bağlı.
- ✍️ Rakam varsa büyüt: "≈ 70 °C" gibi tek sayı kartı, sahne başına en fazla bir tane.

## 5. Ses
- ✅ Bütünleşik ses yüksekliği **-14 LUFS (±1,5)**, gerçek tepe ≤ -1 dBTP.
- ✍️ Ses yoksa en azından düşük seviyeli müzik + akışa bağlı efekt (su, alev, tık). Sessiz video kaydırılır.
- ✍️ Seslendirme varsa altyazıyla kelime kelime eşleşir; seslendirme ilk 0,3 sn'de başlar.

## 6. Bitiş ve döngü
- ✍️ Son 2 sn: tek cümlelik "aha" özeti ("Döngü hiç durmaz.") + sonraki konunun teaser'ı ("Sıradaki: Asansör neden düşmez?").
- ✍️ **Son kare ilk kareye geri bağlanır** (aynı kamera açısı, aynı nesne) → otomatik tekrar oynatmada kesintisiz döngü, tekrar izlenme artar.
- ✍️ Açık uçlu soru ile bitir; yorum tetikler ("Sizin binada kazan nerede?").

## 7. Seri kimliği
- ✍️ Sabit şablon: sol üst `NN · KONU`, sağ üst seri adı, aynı font, aynı renk paleti. (Mevcut şablon iyi; korunmalı.)
- ✍️ Konu seçimi: herkesin her gün gördüğü ama içini bilmediği nesneler. Başlık "nasıl çalışır" değil, merak sorusu.
- ✍️ Kapak karesi = kare 0 (başlık + nesne). Ayrıca seçilecekse aynı kurala uyar.

## 8. Teknik çıktı
- ✅ 1080×1920, 30 fps, H.264 + AAC.
- ✍️ Açıklamaya kısa not: "Animasyonlar yapay zeka destekli hazırlanmıştır." (şeffaflık; zorunlu olmasa da güven verir)

---

## Denetim
```bash
./kontrol.sh video.mp4
```
✅ ile işaretli kurallardan biri bile başarısızsa betik 1 ile çıkar; otomasyon (archiframe-bot) bu durumda yüklemeyi durdurmalı.
Ses düzeltmesi için: `ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 out.mp4`
