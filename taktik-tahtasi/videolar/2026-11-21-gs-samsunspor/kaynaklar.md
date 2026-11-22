# Galatasaray 2-1 Samsunspor · 21 Kasım 2026 · Süper Lig 12. hafta

Maçkolik bu oturumdan okunamadığı için kullanıcı onayıyla haber kaynakları kullanıldı. Diziliş tahtası **temsilidir** (kaynaklar formasyon vermiyor; yerleşim ilk 11'den çıkarıldı, numaralar rol numarasıdır).

| Videodaki bilgi | Kaynak |
|---|---|
| 2-1; Torreira 4', Yunus Akgün 53', Bayo 57' | ESPN maç sayfası, Habertürk, beIN Sports özeti |
| 4': Batrakov serbest vuruşu Singo'ya çarptı, Torreira altıpastan | Habertürk, beIN geniş özet |
| 53': Sara'nın uzun pası, Yunus Akgün aşırtma | Habertürk, beIN geniş özet |
| 57': Joe Mendes'in sağdan ortası, Bayo | Habertürk, beIN geniş özet |
| Şut 11-18, topa sahip olma %56 GS | ESPN takım istatistikleri |
| Uğurcan 6 kurtarış | Ajansspor (spor yazarları değerlendirmesi) |
| 5 değişiklik (3 zorunlu), stoperde Kaan Ayhan | Son Dakika, 12punto, Haber7 |
| Galatasaray 31 puan, lider | Milliyet |
| İç sahada 42 maç yenilmezlik, Terim'in 41 maçlık rekoru geçildi | Haber.tr, Gündem Atlas, Fotomaç |

Bağlantılar:
- https://www.espn.co.uk/football/match/_/gameId/401888245
- https://www.espn.co.uk/football/team-stats/_/gameId/401888245/league/tur.1
- https://www.haberturk.com/spor/galatasaray-samsunspor-mac-sonucu-iste-gs-samsunspor-maci-ozeti-ve-golleri-super-lig-3928946
- https://beinsports.com.tr/haber/galatasaray-samsunspor-3
- https://ajansspor.com/haber/spor-yazarlari-galatasaray-samsunspor-macini-degerlendirdi-739124
- https://www.sondakika.com/spor/haber-okan-buruk-samsunspor-macinda-galatasaray-in-11-20449200/
- https://12punto.com.tr/spor/galatasaray-samsunspor-macinin-ilk-11leri-belli-oldu-okan-buruktan-surpriz-tercihler-159860
- https://www.milliyet.com.tr/skorer/live-lider-galatasaray-samsunspora-gecit-vermedi-okan-buruk-fatih-terimin-rekorunu-kirdi-7704839
- https://www.haber.tr/okan-buruk-fatih-terimin-ic-sahadaki-yenilmezlik-rekorunu-kirdi
- https://www.fotomac.com.tr/galatasaray/2026/11/22/okan-buruk-fark-yaratti-yeni-rekor

Üretim: `cd taktik-tahtasi/sablon && python3 ses_gs.py && SCENE=gs-samsun.html OUT=gs_ node render.js full` (yatay için başına `LAND=1`), ardından ses `audio_gs.wav` ile birleştirilir.

## Seslendirme ve görseller (22 Kasım 2026)
- Seslendirme: ElevenLabs, "Cem – Deep documentary narrator" (mimarlık videolarındaki ses), eleven_v4. Ham kayıt: `seslendirme-cem.mp3`; cümleler `sablon/seslendirme_yerlestir.py` ile sahnelere yerleştirildi.
- Seslendirmeli videolar: `gs-samsunspor-dikey-ses.mp4`, `gs-samsunspor-yatay-ses.mp4`.
- Armalar ve oyuncu fotoğrafları: `sablon/img/KAYNAKLAR.md`.
