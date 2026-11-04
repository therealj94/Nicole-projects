# Auditoría de sincronía: movimiento del pico (flujo óptico en la zona del pico) vs energía de la voz
import cv2, numpy as np, subprocess, sys
vid = sys.argv[1]
cap = cv2.VideoCapture(vid); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(cv2.cvtColor(cv2.resize(f, (480, 270)), cv2.COLOR_BGR2GRAY))
# localizar el pico: zona de mayor movimiento vertical durante el habla
mot = []
for a, b in zip(fr, fr[1:]):
    fl = cv2.calcOpticalFlowFarneback(a, b, None, .5, 3, 15, 3, 5, 1.2, 0)
    mot.append(np.abs(fl[..., 1]))
M = np.array(mot); heat = M.mean(0); y, x = np.unravel_index(np.argmax(cv2.GaussianBlur(heat, (41, 41), 0)), heat.shape)
reg = M[:, max(0, y - 25):y + 25, max(0, x - 25):x + 25].mean((1, 2))
glob = M.mean((1, 2)); beak = reg - glob * (reg.mean() / max(glob.mean(), 1e-6))   # quitar movimiento de cámara
a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', vid, '-vn', '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], stdout=subprocess.PIPE).stdout, np.int16).astype(float)
env = np.array([np.sqrt((a[i * 1000:(i + 1) * 1000] ** 2).mean()) if (i + 1) * 1000 <= len(a) else 0 for i in range(len(beak))])
def z(v): return (v - v.mean()) / (v.std() + 1e-9)
b, e = z(np.convolve(beak, np.ones(3) / 3, 'same')), z(np.convolve(env, np.ones(3) / 3, 'same'))
lags = range(-12, 13); c = [np.corrcoef(np.roll(b, L)[12:-12], e[12:-12])[0, 1] for L in lags]
best = list(lags)[int(np.argmax(c))]
print(f'correlación en lag 0: {c[12]:.2f} | mejor lag: {best} cuadros ({best/24*1000:+.0f} ms) corr {max(c):.2f}')
