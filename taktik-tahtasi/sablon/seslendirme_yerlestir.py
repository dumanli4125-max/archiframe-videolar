import json,numpy as np,subprocess,wave
S='ses/'
lines=["Lider kazandı ama on sekiz şut yedi.","Skor iki bir, Galatasaray kazandı.","Lider otuz bir puanda.","Okan Buruk beş değişiklikle çıktı, üçü zorunlu.","Stoperde sürpriz isim: Kaan Ayhan.","Dördüncü dakika: Batrakov'un serbest vuruşu Singo'ya çarptı, Torreira altıpastan attı.","Elli üçüncü dakika: Sara'nın uzun pasında Yunus Akgün kaleciyi aştı.","Dört dakika sonra Joe Mendes'in ortasında Bayo farkı bire indirdi.","Samsunspor on sekiz şut çekti, Galatasaray on bir.","Uğurcan altı kurtarışla maçı tuttu.","Top yine de yüzde elli altı Galatasaray'da.","İç sahada kırk iki maçtır yenilmiyor.","Fatih Terim'in kırk bir maçlık rekoru geçildi.","Sence şans mı, Uğurcan mı, sistem mi?"]
W=json.load(open(S+'words.json'))
idx=[0,6,10,13,20,25,38,48,59,66,70,75,80,87]
vs=[W[i][0] for i in idx];ends=[W[j-1][1] for j in idx[1:]]+[W[-1][1]]
target=[0.2,2.8,4.8,7.2,11.0,15.2,19.7,24.2,29.2,31.8,34.4,37.2,40.1,43.2]
w=wave.open(S+'vo44.wav');sr=w.getframerate();vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
out=np.zeros(47*sr,np.float32);cap=[];prev=0
for i,l in enumerate(lines):
    a=max(vs[i]-0.06,0);b=min(ends[i]+0.15,(vs[i+1]-0.03) if i<13 else len(vo)/sr)
    st=max(target[i],prev+0.12);seg=vo[int(a*sr):int(b*sr)].copy()
    f=int(.02*sr);seg[:f]*=np.linspace(0,1,f);seg[-f:]*=np.linspace(1,0,f)
    out[int(st*sr):int(st*sr)+len(seg)]+=seg
    cs=st+(vs[i]-a);ce=cs+(ends[i]-vs[i]);cap.append([round(cs,2),round(ce+0.3,2),l]);prev=st+len(seg)/sr
    print(i,round(st,2),'->',round(prev,2),'hedef',target[i])
o=wave.open(S+'vo_placed.wav','wb');o.setnchannels(1);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes());o.close()
json.dump(cap,open(S+'cap.json','w'),ensure_ascii=False)
