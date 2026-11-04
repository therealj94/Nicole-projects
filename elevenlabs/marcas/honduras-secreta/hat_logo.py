# Restaura el logo del sombrero: KLT sobre la copa + parche original deformado e iluminado como en cada cuadro
import cv2, numpy as np, sys, json
src, out = sys.argv[1], sys.argv[2]; ONLY = [int(x) for x in sys.argv[3:]]
I0 = 100; C0 = np.array([557.0, 525.0]); PW0, PH0 = 93.0, 45.0
logo = cv2.imread('../guaca_zip/shot_13_close-up.jpg')[100:223, 398:651].astype(np.float32)     # parche original
lh, lw = logo.shape[:2]
pm = np.zeros((lh, lw), np.float32); cv2.rectangle(pm, (4, 4), (lw - 5, lh - 5), 1, -1)
pm = cv2.GaussianBlur(pm, (0, 0), 2.2)
lum_src = cv2.cvtColor(logo.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
cap = cv2.VideoCapture(src); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(f)
G = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in F]; n = len(F)
def run(direction):
    T = {I0: np.array([[1, 0, 0], [0, 1, 0]], float)}       # transformación acumulada desde el cuadro de referencia
    M = np.eye(3); m = np.zeros_like(G[I0]); cv2.rectangle(m, (490, 497), (622, 552), 255, -1)
    pts = cv2.goodFeaturesToTrack(G[I0], 120, 0.01, 4, mask=m)
    cur = pts.copy(); ref = pts.copy()
    rng = range(I0, n - 1) if direction > 0 else range(I0, 0, -1)
    for i in rng:
        j = i + direction
        p1, st, _ = cv2.calcOpticalFlowPyrLK(G[i], G[j], cur, None, winSize=(21, 21), maxLevel=4)
        b, _, _ = cv2.calcOpticalFlowPyrLK(G[j], G[i], p1, None, winSize=(21, 21), maxLevel=4)
        good = (st[:, 0] == 1) & (np.linalg.norm((b - cur).reshape(-1, 2), axis=1) < 1.0)
        if good.sum() < 8: T[j] = T[i]; continue
        A, inl = cv2.estimateAffinePartial2D(ref[good], p1[good], method=cv2.RANSAC, ransacReprojThreshold=2.5)
        if A is None: T[j] = T[i]; continue
        T[j] = A; keep = good.copy(); keep[good] = inl[:, 0].astype(bool)
        cur, ref = p1[keep].reshape(-1, 1, 2), ref[keep].reshape(-1, 1, 2)
        if len(cur) < 25:   # re-sembrar puntos en la zona actual del sombrero, expresados en coordenadas de referencia
            Ainv = cv2.invertAffineTransform(A)
            c = A @ np.array([556, 524, 1.0]); s = np.hypot(A[0, 0], A[1, 0])
            m2 = np.zeros_like(G[j]); cv2.rectangle(m2, (int(c[0] - 66 * s), int(c[1] - 27 * s)), (int(c[0] + 66 * s), int(c[1] + 28 * s)), 255, -1)
            new = cv2.goodFeaturesToTrack(G[j], 120, 0.01, 4, mask=m2)
            if new is not None:
                cur = np.concatenate([cur, new]); ref = np.concatenate([ref, cv2.transform(new, Ainv)])
    return T
T = {**run(-1), **run(1)}
# suavizado temporal de los parámetros
keys = sorted(T); P = np.array([[T[k][0, 2], T[k][1, 2], np.hypot(T[k][0, 0], T[k][1, 0]), np.arctan2(T[k][1, 0], T[k][0, 0])] for k in keys])
Ps = np.array([np.convolve(np.pad(P[:, c], 3, mode='edge'), np.ones(7) / 7, mode='valid') for c in range(4)]).T
def place(i):
    tx, ty, s, a = Ps[keys.index(i)]
    A = np.array([[s * np.cos(a), -s * np.sin(a), tx], [s * np.sin(a), s * np.cos(a), ty]])
    c = A @ np.array([*C0, 1.0]); return c, s, a
fourcc = cv2.VideoWriter_fourcc(*'mp4v'); wr = None if ONLY else cv2.VideoWriter(out, fourcc, 24, (F[0].shape[1], F[0].shape[0]))
for i, f in enumerate(F):
    if ONLY and i not in ONLY: continue
    g = f.astype(np.float32)
    if i in T:
        c, s, a = place(i); pw, ph = PW0 * s, PH0 * s
        sx, sy = pw / lw, ph / lh
        R = np.array([[np.cos(a) * sx, -np.sin(a) * sy], [np.sin(a) * sx, np.cos(a) * sy]])
        A = np.hstack([R, (c - R @ np.array([lw / 2, lh / 2]))[:, None]])
        W_, H_ = f.shape[1], f.shape[0]
        wl = cv2.warpAffine(logo, A, (W_, H_), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
        wm = cv2.warpAffine(pm, A, (W_, H_))
        # iluminación: igualar el brillo del parche al del sombrero alrededor
        x0, y0 = int(c[0] - pw), int(c[1] - ph); x1, y1 = int(c[0] + pw), int(c[1] + ph)
        ring = np.zeros((H_, W_), np.float32); ring[max(0, y0):y1, max(0, x0):x1] = 1; ring *= (wm < .05)
        hat_l = (cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) * ring).sum() / max(ring.sum(), 1)
        gain = np.clip(hat_l / 196.0, .6, 1.25)
        wl = cv2.GaussianBlur(wl * gain, (0, 0), max(.4, .6 / max(s, .3)))
        g = g * (1 - wm[..., None]) + wl * wm[..., None]
    o = np.clip(g, 0, 255).astype(np.uint8)
    if ONLY: cv2.imwrite(f'logo_{i}.png', o)
    else: wr.write(o)
if wr: wr.release()
print('ok', len(T))
