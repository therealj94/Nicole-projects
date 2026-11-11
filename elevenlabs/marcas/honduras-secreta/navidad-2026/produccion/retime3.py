# Ajusta el VIDEO a la voz natural (sin estirar audio). Conserva la toma completa: antes y después del habla corre a velocidad 1.
import json, sys, subprocess, numpy as np
veo, veo_json, vo_json, out = sys.argv[1:5]; LOOSE = "--loose" in sys.argv
norm = lambda s: s.lower().strip('¡!¿?,.…')
vw = [w for w in json.load(open(veo_json))['words'] if w['type'] == 'word']
jw = [w for w in json.load(open(vo_json))['words'] if w['type'] == 'word']
pairs = []; vi = 0
for w in jw:
    for k in range(vi, len(vw)):
        if norm(vw[k]['text']) == norm(w['text']): pairs.append((w['start'], vw[k]['start'], w['end'], vw[k]['end'])); vi = k + 1; break
J = np.array([p[0] for p in pairs] + [pairs[-1][2]]); V = np.array([p[1] for p in pairs] + [pairs[-1][3]])
if LOOSE: J, V = J[[0, -1]], V[[0, -1]]
off = V[0] - J[0]; Jt = J + off
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', veo]))
total = Jt[-1] + (dur - V[-1])
def mapt(t):
    if t <= Jt[0]: return t
    if t >= Jt[-1]: return V[-1] + (t - Jt[-1])
    return float(np.interp(t, Jt, V))
T = np.arange(0, total - 1 / 48, 1 / 24); src = np.array([mapt(t) for t in T])
src = np.convolve(np.pad(src, 3, mode='edge'), np.ones(7) / 7, mode='valid')
w, h = 1080, 1920
F = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', veo, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE).stdout, np.uint8).reshape(-1, h, w, 3); n = len(F)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'warning', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for s in src:
    f = min(max(s * 24, 0), n - 1.001); i = int(f); a = f - i
    enc.stdin.write(np.ascontiguousarray(F[i] if a < .02 else (F[i] * (1 - a) + F[i + 1] * a).astype(np.uint8)).tobytes())
enc.stdin.close(); enc.wait()
spd = np.diff(src) * 24
json.dump({'vo_start': float(off), 'total': float(len(T) / 24), 'pairs': pairs}, open(out + '.json', 'w'))
print(out, 'voz entra', round(off, 2), 'dur', round(len(T) / 24, 2), 'vel', round(spd.min(), 2), round(spd.max(), 2))
