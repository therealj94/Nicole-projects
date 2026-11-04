# Sigue a la chica de camisa amarilla (color) y a la señora del overol (KLT) para ubicar el hueco entre ambas
import cv2, numpy as np, json, sys
V = sys.argv[1]
cap = cv2.VideoCapture(V); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
fps = 30.0; n = len(fr); i0 = int(2.5 * fps)
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
# --- camisa amarilla neón ---
def yellow(f, prev):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] > 26) & (hsv[..., 0] < 42) & (hsv[..., 1] > 130) & (hsv[..., 2] > 140)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    k, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    best, bd = None, 1e9
    for j in range(1, k):
        if st[j, cv2.CC_STAT_AREA] < 40: continue
        d = np.hypot(*(cen[j] - prev)) if prev is not None else 0
        if d < bd: bd, best = d, j
    if best is None or (prev is not None and bd > 120): return None
    x, y, w, h, a = st[best]
    return [float(cen[best][0]), float(y), float(y + h), float(h)]
Y = {}
prev = np.array([605., 560.])
for i in range(i0, n):
    r = yellow(fr[i], prev)
    if r: Y[i] = r; prev = np.array([r[0], (r[1] + r[2]) / 2])
prev = np.array([605., 560.])
for i in range(i0, -1, -1):
    r = yellow(fr[i], prev)
    if r: Y[i] = r; prev = np.array([r[0], (r[1] + r[2]) / 2])
# --- señora del overol: puntos KLT en su torso ---
def klt(direction, box):
    x0, y0, x1, y1 = box; m = np.zeros_like(gray[i0]); m[y0:y1, x0:x1] = 255
    pts = cv2.goodFeaturesToTrack(gray[i0], 80, 0.01, 4, mask=m); out = {i0: np.median(pts.reshape(-1, 2), 0).tolist()}
    rng = range(i0, n - 1) if direction > 0 else range(i0, 0, -1)
    for i in rng:
        j = i + direction
        if pts is None or len(pts) < 6: break
        p1, st, _ = cv2.calcOpticalFlowPyrLK(gray[i], gray[j], pts, None, winSize=(21, 21), maxLevel=3)
        b, _, _ = cv2.calcOpticalFlowPyrLK(gray[j], gray[i], p1, None, winSize=(21, 21), maxLevel=3)
        good = (st[:, 0] == 1) & (np.linalg.norm((b - pts).reshape(-1, 2), axis=1) < .8)
        pts = p1[good].reshape(-1, 1, 2)
        if len(pts) < 6: break
        med = np.median(pts.reshape(-1, 2), 0)
        d = np.linalg.norm(pts.reshape(-1, 2) - med, axis=1); pts = pts[d < max(25, 2.5 * np.median(d))]
        out[j] = med.tolist()
    return out
L = {**klt(-1, (740, 490, 795, 590)), **klt(1, (740, 490, 795, 590))}
json.dump({"yellow": Y, "lady": L}, open('people.json', 'w'))
print(len(Y), len(L), min(L), max(L))
