# Baja a 1080, recorta las tomas partidas (02 y 05) y desplaza sus transcripciones.
import subprocess, json, os
os.makedirs('hd', exist_ok=True)
def R(*a): subprocess.run(a, check=True)
src = lambda n: f'fix/{n}.mp4' if n in ('01','05','07') else f'vid/{n}.mp4'
SPL = {'02a': ('02', 0, 2.7, 1.0), '02b': ('02', 5.55, 8.0, 1.12), '05a': ('05', 0, 1.15, 1.0), '05b': ('05', 4.0, 6.0, 1.18)}
for n in ['01','03','04','06','07','08','09','10','11','12']:
    R('ffmpeg','-loglevel','error','-y','-i',src(n),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-crf','12','-pix_fmt','yuv420p','-an',f'hd/{n}.mp4')
for k, (n, a, b, z) in SPL.items():
    vf = f'scale=1080:1920:flags=lanczos' + (f',scale=iw*{z}:ih*{z},crop=1080:1920:(iw-1080)/2:(ih-1920)*0.4' if z > 1 else '')
    R('ffmpeg','-loglevel','error','-y','-ss',str(a),'-to',str(b),'-i',src(n),'-vf',vf,'-c:v','libx264','-crf','12','-pix_fmt','yuv420p','-an',f'hd/{k}.mp4')
    R('ffmpeg','-loglevel','error','-y','-ss',str(a),'-to',str(b),'-i',f'tr/{n}.wav',f'tr/{k}.wav')
    d = json.load(open(f'tr/{n}.json')); ws = []
    for w in d['words']:
        if a <= w['start'] < b: w = dict(w); w['start'] -= a; w['end'] -= a; ws.append(w)
    json.dump({'words': ws}, open(f'tr/{k}.json', 'w'))
print('ok')
