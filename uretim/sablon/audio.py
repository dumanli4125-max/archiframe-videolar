import sys
from audio_kit import Mix
m = Mix(D=8)
# m.vo('seslendirme/l01.wav', 0.3)      # anlatım satırları (scene.html ile aynı başlangıçlar)
m.pad()
m.steps(1.0, 5.2)
m.buzz(3.0); m.ping(3.2)
m.note(6.3, 392)
m.write(sys.argv[1])
