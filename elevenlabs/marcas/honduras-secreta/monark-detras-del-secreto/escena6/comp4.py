# Escena del rodaje: la guara posa sobre el tapete de la mesa mientras Nicole dirige.
import cv2, numpy as np, subprocess
PLATE = '../real/x4_1080.mov'; G = 'pose_fix.mp4'
REF = 120; FEET_P = np.float32([760, 915]); FEET_G = np.float32([540, 1330]); SC = 0.36; T0 = 0.0
PERSON = np.load('person.npy')[..., 0]
def frames(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
P = frames(PLATE); GF = frames(G); n = len(P); H, W = P[0].shape[:2]
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in P]
mask = np.zeros_like(gray[0]); mask[750:1400, 520:1080] = 255
def chain(d):
    M = {REF: np.eye(3)}; cur = np.eye(3); i = REF; pts = cv2.goodFeaturesToTrack(gray[i], 400, .01, 7, mask=mask)
    while 0 <= i + d < n:
        j = i + d
        p1, st, _ = cv2.calcOpticalFlowPyrLK(gray[i], gray[j], pts, None, winSize=(25, 25), maxLevel=4); ok = st[:, 0] == 1
        A, inl = cv2.estimateAffinePartial2D(pts[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2)
        cur = np.vstack([A, [0, 0, 1]]) @ cur; M[j] = cur.copy(); pts = p1[ok][inl[:, 0] == 1].reshape(-1, 1, 2)
        if len(pts) < 80: pts = cv2.goodFeaturesToTrack(gray[j], 400, .01, 7, mask=cv2.warpAffine(mask, cur[:2], (W, H)))
        i = j
    return M
M = {**chain(-1), **chain(1)}; ks = sorted(M); arr = np.array([M[k] for k in ks]); M = {k: np.mean(arr[max(0, t - 2):t + 3], 0) for t, k in enumerate(ks)}
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', 'v_comp.mp4'], stdin=subprocess.PIPE)
for i in range(n):
    f = P[i].astype(np.float32); k = min(int(round((i / 30 - T0) * 24)), len(GF) - 1)
    if k >= 0:
        g = GF[k].astype(np.float32)
        gd = g[..., 1] - np.maximum(g[..., 0], g[..., 2]); a = np.clip(1 - (gd - 15) / 70, 0, 1)
        hsv = cv2.cvtColor(g.astype(np.uint8), cv2.COLOR_BGR2HSV)
        blk = np.zeros_like(a, bool); blk[1338:1660, 260:820] = True; a[blk & ((hsv[..., 2] < 140) | (hsv[..., 1] < 110))] = 0
        blk2 = np.zeros_like(a, bool); blk2[1312:1340, 260:820] = True; a[blk2 & (hsv[..., 2] < 95)] = 0
        a[:10] = 0; a[-10:] = 0; a[:, :10] = 0; a[:, -10:] = 0; a = cv2.GaussianBlur(a, (0, 0), .8)
        g[..., 1] = np.minimum(g[..., 1], (g[..., 0] + g[..., 2]) / 2 + 10)
        Tm = np.float32([[SC, 0, FEET_P[0] - SC * FEET_G[0]], [0, SC, FEET_P[1] - SC * FEET_G[1]], [0, 0, 1]])
        A = (M[i] @ Tm)[:2]
        wg = cv2.warpAffine(g, A, (W, H), flags=cv2.INTER_AREA); wa = cv2.warpAffine(a, A, (W, H))
        sh = np.zeros((H, W), np.float32); p = (M[i] @ np.float32([*FEET_P, 1]))[:2]
        cv2.ellipse(sh, (int(p[0]), int(p[1]) + 3), (60, 12), -6, 0, 360, 1, -1); sh = cv2.GaussianBlur(sh, (0, 0), 8) * .5
        f *= (1 - sh[..., None])
        pm = cv2.GaussianBlur(PERSON[i].astype(np.float32) / 255, (0, 0), 1.5); wa = wa * (1 - pm)
        f = f * (1 - wa[..., None]) + cv2.GaussianBlur(wg * np.float32([.97, .99, 1.02]), (0, 0), .6) * wa[..., None]
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', n)
