# Ajusta la velocidad del VIDEO de Veo para que el pico siga la voz natural de José (el audio no se toca)
import json, sys, subprocess, numpy as np, math
from score import times, ORDER
veo, veo_json, jose_json, jose_audio, out = sys.argv[1:6]
SHIFT = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0      # retraso del video respecto a la voz (s)
j, jend = times(jose_json); v, _ = times(veo_json)
ks = [k for k in ORDER[1:] if k in j and k in v]                 # sin "ey" (su inicio no es fiable en la transcripción)
J = np.array([j[k] for k in ks]); Vt = np.array([v[k] for k in ks])
m = (Vt[-1] - Vt[0]) / (J[-1] - J[0])                              # velocidad media
adur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', jose_audio]))
T = np.arange(0, adur + .35, 1 / 24)
def mapt(t):
    if t <= J[0]: return Vt[0] - (J[0] - t) * m
    if t >= J[-1]: return Vt[-1] + (t - J[-1]) * 1.0          # tras la última palabra: velocidad normal
    return float(np.interp(t, J, Vt))
src = np.array([max(0.0, mapt(t - SHIFT)) for t in T])
src = np.convolve(np.pad(src, 3, mode='edge'), np.ones(7) / 7, mode='valid')   # suavizar cambios de velocidad
spd = np.diff(src) * 24
print('anclas', list(zip(ks, J.round(2), Vt.round(2))))
print(f'velocidad media {m:.2f}  min {spd.min():.2f}  max {spd.max():.2f}  rango fuente {src[0]:.2f}-{src[-1]:.2f}')
assert src[0] >= -0.05 and src[-1] <= 8.0, 'fuera del clip'
cap = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', veo, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE).stdout
w, h = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', veo]).decode().strip().split(','))
F = np.frombuffer(cap, np.uint8).reshape(-1, h, w, 3); n = len(F)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-',
                        '-i', jose_audio, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', out], stdin=subprocess.PIPE)
for s in src:
    f = min(max(s * 24, 0), n - 1.001); i = int(f); a = f - i
    fr = F[i] if a < .02 else (F[i] * (1 - a) + F[i + 1] * a).astype(np.uint8)   # mezcla de cuadros: movimiento fluido
    enc.stdin.write(np.ascontiguousarray(fr).tobytes())
enc.stdin.close(); enc.wait(); print('ok', out, len(src) / 24)
