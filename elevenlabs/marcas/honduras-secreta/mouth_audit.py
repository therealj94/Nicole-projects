# Auditoría por apertura de boca: fracción de píxeles oscuros/rosados en la franja central bajo el pico
import cv2, numpy as np, subprocess, sys
vid, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); X0, X1, Y0, Y1 = [int(v) for v in sys.argv[4:8]]
cap = cv2.VideoCapture(vid); fps = cap.get(cv2.CAP_PROP_FPS); o = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps; i += 1
    if t0 <= t <= t1:
        hsv = cv2.cvtColor(f[Y0:Y1, X0:X1], cv2.COLOR_BGR2HSV)
        o.append(((hsv[..., 2] < 60) | ((hsv[..., 0] > 160) & (hsv[..., 1] > 60) & (hsv[..., 2] < 200))).mean())
o = np.array(o)
a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', vid, '-vn', '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], stdout=subprocess.PIPE).stdout, np.int16).astype(float)
spf = int(24000 / fps); env = np.array([np.sqrt((a[k * spf:(k + 1) * spf] ** 2).mean()) if (k + 1) * spf <= len(a) else 0 for k in range(len(o))])
z = lambda v: (v - v.mean()) / (v.std() + 1e-9); b, e = z(o), z(np.convolve(env, np.ones(3) / 3, 'same'))
L = 8; c = {l: np.corrcoef(b[L + l:len(b) - L + l], e[L:len(e) - L])[0, 1] for l in range(-L, L + 1)}; best = max(c, key=c.get)
print(f'corr lag0 {c[0]:.2f} | mejor desfase {best:+d} cuadros ({best / fps * 1000:+.0f} ms; + = el pico va atrasado) corr {c[best]:.2f}')
