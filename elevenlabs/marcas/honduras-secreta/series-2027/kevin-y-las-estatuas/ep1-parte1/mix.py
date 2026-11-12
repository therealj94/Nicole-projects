import json, subprocess, numpy as np
SR=48000; tl=json.load(open('seg/tl.json')); TOT=tl['total']; L=int(TOT*SR)
def load(f,a=0,d=None):
    cmd=['ffmpeg','-loglevel','error','-ss',f'{a:.3f}','-i',f]+(['-t',f'{d:.3f}'] if d else [])+['-ac','2','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,stdout=subprocess.PIPE).stdout,np.float32).reshape(-1,2).copy()
def put(trk,x,t,g=1.0):
    p=int(t*SR); e=min(L,p+len(x))
    if e>p: trk[p:e]+=x[:e-p]*g
dlg=np.zeros((L,2),np.float32); fx=np.zeros((L,2),np.float32)
for au,t,d in tl['audio']:
    if au: put(dlg,load(au,0,d),t)
for f,t,g in [('au/aleteo.mp3',6.9,.4),('au/selva.mp3',8.17,.3),('au/aleteo.mp3',8.4,.5),('au/piedra.mp3',14.6,.7),('au/magia.mp3',14.6,.6),('au/pasos.mp3',28.0,.4),('au/magia.mp3',35.0,.4),('au/piedra.mp3',42.96,.5),('au/pelota.mp3',54.4,.6),('au/magia.mp3',61.0,.6),('au/whoosh.mp3',64.9,.5)]:
    put(fx,load(f),t,g)
mus=np.zeros((L,2),np.float32); put(mus,load('au/musica.mp3'),0)
env=np.abs(dlg).max(1); k=int(.05*SR); env=np.convolve(env,np.ones(k)/k,'same')
act=(env>.01).astype(np.float32); sm=int(.35*SR); act=np.convolve(act,np.ones(sm)/sm,'same'); gain=1-.7*np.clip(act*1.6,0,1)
mix=dlg+fx+mus*.5*gain[:,None]
mix[-int(2*SR):]*=np.linspace(1,0,int(2*SR))[:,None]**.5
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','loudnorm=I=-14:TP=-1.5','-ar',str(SR),'-c:a','pcm_s16le','mix.wav'],input=np.clip(mix,-1,1).astype(np.float32).tobytes(),check=True)
print('ok',TOT)
