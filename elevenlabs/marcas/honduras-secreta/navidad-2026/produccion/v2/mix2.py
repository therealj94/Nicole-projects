import json, subprocess, numpy as np
SR = 48000; tl = json.load(open('v2/seg/tl.json')); TOT = tl['total']; L = int(TOT * SR)
def load(f, a=0, d=None):
    cmd = ['ffmpeg', '-loglevel', 'error', '-ss', f'{a:.3f}', '-i', f] + (['-t', f'{d:.3f}'] if d else []) + ['-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, stdout=subprocess.PIPE).stdout, np.float32).reshape(-1, 2).copy()
def put(trk, x, t, g=1.0):
    p = int(t * SR); e = min(L, p + len(x)); trk[p:e] += x[:e - p] * g
dlg = np.zeros((L, 2), np.float32); fx = np.zeros((L, 2), np.float32)
for au, a, t, d in tl['audio']:
    if au: put(dlg, load(au, a, d), t)
put(dlg, load('vo/marta.mp3'), 74.3)
def rms(x): return np.sqrt(np.mean(x ** 2) + 1e-12)
# efectos
for f, t, g in [('au/sfx_wind.mp3', 0, .35), ('au/sfx_coffee.mp3', 21.7, .5), ('au/sfx_flash.mp3', 38.9, .6), ('au/sfx_rope.mp3', 45.2, .35),
                ('au/sfx_plane.mp3', 48.25, .3), ('au/sfx_airport.mp3', 54.29, .22), ('au/sfx_wind.mp3', 61.83, .25), ('au/sfx_box.mp3', 68.0, .5),
                ('au/sfx_fireworks.mp3', 93.3, .3), ('au/sfx_flap.mp3', 97.0, .45), ('au/sfx_fireworks.mp3', 99.5, .3)]:
    put(fx, load(f), t, g)
mus = load('v2/cancion_edit.wav')[:L]; mus = np.pad(mus, ((0, L - len(mus)), (0, 0)))
# ducking por envolvente del diálogo
env = np.abs(dlg).max(1); k = int(.05 * SR)
env = np.convolve(env, np.ones(k) / k, 'same'); env = np.maximum.accumulate(env[::-1])[::-1] * 0 + env
act = (env > .01).astype(np.float32); sm = int(.35 * SR)
act = np.convolve(act, np.ones(sm) / sm, 'same'); gain = 1 - .72 * np.clip(act * 1.6, 0, 1)
mix = dlg * 1.0 + fx + mus * .55 * gain[:, None]
mix[-int(2 * SR):] *= np.linspace(1, 0, int(2 * SR))[:, None] ** .5
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'loudnorm=I=-14:TP=-1.5', '-ar', str(SR), '-c:a', 'pcm_s16le', 'v2/mix.wav'], input=np.clip(mix, -1, 1).astype(np.float32).tobytes(), check=True)
print('ok', TOT)
