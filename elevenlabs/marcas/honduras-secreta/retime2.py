# Video a velocidad normal hasta que empieza a hablar; durante el habla, el video sigue la voz natural de José.
import json, sys, subprocess, numpy as np
veo, veo_json, jose_json, jose_audio, out, shift = sys.argv[1:7]; shift = float(shift)
norm = lambda s: s.lower().strip('¡!¿?,.…')
vw = [w for w in json.load(open(veo_json))['words'] if w['type'] == 'word']
jw = [w for w in json.load(open(jose_json))['words'] if w['type'] == 'word']
pairs = []; vi = 0
for w in jw:                                   # emparejar palabras en orden
    for k in range(vi, len(vw)):
        if norm(vw[k]['text']) == norm(w['text']): pairs.append((w['start'], vw[k]['start'])); vi = k + 1; break
J = np.array([p[0] for p in pairs]); V = np.array([p[1] for p in pairs])
off = V[0] - J[0]                              # la voz de José empieza en el timeline en 'off'
adur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', jose_audio]))
Jt = J + off                                   # tiempos de palabra en el timeline final
total = off + adur + .5
def mapt(t):
    if t <= Jt[0]: return t                    # guitarra: velocidad 1
    if t >= Jt[-1]: return V[-1] + (t - Jt[-1])
    return float(np.interp(t, Jt, V))
T = np.arange(0, total, 1 / 24); src = np.array([max(0, mapt(t)) for t in T])
src = np.convolve(np.pad(src, 3, mode='edge'), np.ones(7) / 7, mode='valid')
spd = np.diff(src[3:-3]) * 24
print('pares', [(round(a, 2), round(b, 2)) for a, b in pairs]); print(f'voz entra en {off:.2f}s | velocidad video min {spd.min():.2f} max {spd.max():.2f} | fuente hasta {src[-1]:.2f}s')
w, h = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', veo]).decode().strip().split(','))
F = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', veo, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE).stdout, np.uint8).reshape(-1, h, w, 3); n = len(F)
# audio: guitarra original de Veo hasta que José habla + voz natural de José
ao = off - shift; d = int(ao * 1000)                # 'shift' adelanta la voz respecto al pico
fc = f"[1:a]atrim=0:{ao - 0.05:.3f},afade=t=out:st={ao - 0.35:.3f}:d=0.3[g];[2:a]adelay={d}|{d}[j];[g][j]amix=inputs=2:normalize=0:duration=longest,apad[a]"
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'warning', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-i', veo, '-i', jose_audio,
                        '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-t', f'{len(T)/24:.3f}', out], stdin=subprocess.PIPE)
for s in src:
    f = min(max(s * 24, 0), n - 1.001); i = int(f); a = f - i
    enc.stdin.write(np.ascontiguousarray(F[i] if a < .02 else (F[i] * (1 - a) + F[i + 1] * a).astype(np.uint8)).tobytes())
enc.stdin.close(); enc.wait(); json.dump({'off': ao, 'total': total}, open(out + '.json', 'w')); print('ok', out, round(total, 2))
