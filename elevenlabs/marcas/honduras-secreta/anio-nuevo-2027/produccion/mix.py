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
for f,t,g in [('au/silb.mp3',0.2,.25),('au/apagon.mp3',12.35,.7),('au/whoosh.mp3',23.5,.5),('au/polilla.mp3',22.4,.6),('au/maleta.mp3',25.9,.35),
              ('au/escoba.mp3',31.5,.45),('au/silb.mp3',38.7,.2),('au/cohetes.mp3',51.9,.55),('au/fuego.mp3',53.8,.45),('au/cohetes.mp3',56.5,.4),
              ('au/abrazo.mp3',61.9,.6),('au/cohetes.mp3',69.3,.22),('au/cohetes.mp3',75.5,.18)]:
    put(fx,load(f),t,g)
mus=np.zeros((L,2),np.float32); put(mus,load('au/musica.mp3'),1.8)
env=np.abs(dlg).max(1); k=int(.05*SR); env=np.convolve(env,np.ones(k)/k,'same')
act=(env>.01).astype(np.float32); sm=int(.35*SR); act=np.convolve(act,np.ones(sm)/sm,'same'); gain=1-.7*np.clip(act*1.6,0,1)
mix=dlg+fx+mus*.5*gain[:,None]
mix[-int(2*SR):]*=np.linspace(1,0,int(2*SR))[:,None]**.5
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','loudnorm=I=-14:TP=-1.5','-ar',str(SR),'-c:a','pcm_s16le','mix.wav'],input=np.clip(mix,-1,1).astype(np.float32).tobytes(),check=True)
print('ok',TOT)
