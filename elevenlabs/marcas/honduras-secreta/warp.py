# Ajusta la voz de José (TTS) a los tiempos de palabra de la toma de Veo, tramo por tramo, sin cambiar el tono
import json, subprocess, numpy as np, sys
src, src_json, ref_wav, ref_json, out = sys.argv[1:6]
sw = [w for w in json.load(open(src_json))['words'] if w['type'] == 'word']
rw = [w for w in json.load(open(ref_json))['words'] if w['type'] == 'word']
# inicio de voz en la referencia (para "¡Ey!" que la transcripción de Veo omitió)
x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', ref_wav, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], stdout=subprocess.PIPE).stdout, np.int16).astype(float)
env = np.convolve(np.abs(x), np.ones(320) / 320, 'same'); onset = np.argmax(env > env.max() * .12) / 16000
norm = lambda s: s.lower().strip('¡!¿?,.')
rmap = {norm(w['text']): w for w in rw}
anch = []
for w in sw:
    k = norm(w['text'])
    if k in ('ey', 'hey') and k not in rmap:
        nxt = sw[sw.index(w) + 1]; tq = rmap[norm(nxt['text'])]['start']
        anch.append((w['start'], max(0.0, tq - (nxt['start'] - w['start'])))); continue
    if k in rmap: anch.append((w['start'], rmap[k]['start']))
anch = sorted(set(anch)); print('anclas', [(round(a, 2), round(b, 2)) for a, b in anch])
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]))
pts = [(0.0, max(0.0, anch[0][1] - anch[0][0]))] + anch + [(dur, anch[-1][1] + (dur - anch[-1][0]))]
parts = []
for (s0, t0), (s1, t1) in zip(pts, pts[1:]):
    if s1 - s0 < .01 or t1 - t0 < .01: continue
    tempo = (s1 - s0) / (t1 - t0); chain = []
    while tempo > 2: chain.append('atempo=2'); tempo /= 2
    while tempo < .5: chain.append('atempo=0.5'); tempo /= .5
    chain.append(f'atempo={tempo:.5f}'); parts.append((s0, s1, ','.join(chain)))
lead = max(0.0, anch[0][1] - anch[0][0]) if anch[0][1] > anch[0][0] else 0
fc = ''; ins = []
for k, (s0, s1, ch) in enumerate(parts):
    fc += f'[0:a]atrim={s0}:{s1},asetpts=N/SR/TB,{ch}[p{k}];'
fc += ''.join(f'[p{k}]' for k in range(len(parts))) + f'concat=n={len(parts)}:v=0:a=1,adelay={int(lead*1000)}|{int(lead*1000)}[a]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-filter_complex', fc, '-map', '[a]', '-ar', '44100', out], check=True)
print('ok', out)
