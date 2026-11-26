import sys
from audio_kit import Mix
D = 52.4
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
for n, st in [('l01',0.3),('l02',3.9),('l03',7.3),('l04',27.8),('l05',33.0),('l06',37.8),('l07',41.9),('l08',46.0)]:
    m.vo(f'seslendirme_en/{n}.wav', st)
m.pad(gain=0.045, swell_from=38)
m.note(0.3, 440, g=0.06)                       # kanca
m.steps(3.9, 7.0, rate=0.39, gain=0.18)        # SEN odaya yürüyor
m.thud(7.6, f=55, gain=0.12)                   # kanepeye oturuş
m.ping(11.5, gain=0.10)                        # Başlıyoruz
m.tension(12.5, 27.5, gain=0.05)               # 15 sn tik-tak
for k in range(13, 28): m.tick(k, gain=0.05)   # saniye vuruşları (geri sayım tam sayıları)
m.buzz(27.5, dur=0.6, gain=0.08); m.thud(27.5, gain=0.25)   # süre doldu
m.ping(30.3, gain=0.10)                        # yorum kutusu
m.whoosh(33.1, dur=1.4, gain=0.16)             # başa sar
m.click(34.5)
m.whoosh(35.4, dur=1.8, gain=0.12)             # hızlı oynat
m.ding(37.2, gain=0.17)                        # cevap
m.note(43.0, 329.6, g=0.06); m.note(44.6, 392, g=0.07)   # beklenen
m.note(46.1, 261.6, g=0.07); m.note(47.9, 329.6, g=0.07); m.note(49.6, 392, g=0.08)
m.write(sys.argv[1])
