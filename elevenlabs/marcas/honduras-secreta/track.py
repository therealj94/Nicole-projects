# Seguimiento de un punto del suelo (hueco entre las dos chicas) con KLT + similitud local
import cv2, numpy as np, json, sys
V, T0, P0 = sys.argv[1], float(sys.argv[2]), (float(sys.argv[3]), float(sys.argv[4]))
cap = cv2.VideoCapture(V); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
i0 = int(round(T0 * fps))
def track(direction):
    out = {i0: (P0[0], P0[1], 1.0, 0.0)}
    x, y, s, a = P0[0], P0[1], 1.0, 0.0
    rng = range(i0, len(frames) - 1) if direction > 0 else range(i0, 0, -1)
    pts = None
    for i in rng:
        j = i + direction
        g0, g1 = frames[i], frames[j]
        R = int(260 * s)
        m = np.zeros_like(g0); cv2.circle(m, (int(x), int(y)), max(60, R), 255, -1)
        if pts is None or len(pts) < 40:
            pts = cv2.goodFeaturesToTrack(g0, 300, 0.01, 6, mask=m)
        if pts is None: out[j] = (x, y, s, a); continue
        p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, pts, None, winSize=(25, 25), maxLevel=4)
        b, _, _ = cv2.calcOpticalFlowPyrLK(g1, g0, p1, None, winSize=(25, 25), maxLevel=4)
        good = (st[:, 0] == 1) & (np.linalg.norm((b - pts).reshape(-1, 2), axis=1) < 1.0)
        if good.sum() < 8: out[j] = (x, y, s, a); pts = None; continue
        A, inl = cv2.estimateAffinePartial2D(pts[good], p1[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        if A is None: out[j] = (x, y, s, a); pts = None; continue
        x, y = A @ np.array([x, y, 1.0])
        sc = np.hypot(A[0, 0], A[1, 0]); s *= sc; a += np.degrees(np.arctan2(A[1, 0], A[0, 0]))
        out[j] = (float(x), float(y), float(s), float(a))
        keep = good.copy(); keep[good] = inl[:, 0].astype(bool)
        pts = p1[keep].reshape(-1, 1, 2)
        if not (0 <= x < 1440 and 0 <= y < 1080): break
    return out
tr = {**track(-1), **track(1)}
json.dump({"fps": fps, "track": {int(k): v for k, v in sorted(tr.items())}}, open("track.json", "w"))
print(len(tr), "frames", min(tr), max(tr))
