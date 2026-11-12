# Escena 3: Claudio (fondo azul) sentado en el escritorio a la derecha del laptop.
import cv2, numpy as np, subprocess
PLATE = '../real/t3_1080.mov'; C = 'claudio.mp4'
REF = 110; SEAT_P = np.float32([915, 1560]); SEAT_C = np.float32([600, 1245]); SC = 0.55
def frames(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
P = frames(PLATE); CF = frames(C); n = len(P); H, W = P[0].shape[:2]
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in P]
mask = np.zeros_like(gray[0]); mask[1250:1750, 700:1080] = 255
def chain(d):
    M = {REF: np.eye(3)}; cur = np.eye(3); i = REF; pts = cv2.goodFeaturesToTrack(gray[i], 300, .01, 7, mask=mask)
    while 0 <= i + d < n:
        j = i + d
        p1, st, _ = cv2.calcOpticalFlowPyrLK(gray[i], gray[j], pts, None, winSize=(25, 25), maxLevel=4); ok = st[:, 0] == 1
        A, inl = cv2.estimateAffinePartial2D(pts[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2)
        cur = np.vstack([A, [0, 0, 1]]) @ cur; M[j] = cur.copy(); pts = p1[ok][inl[:, 0] == 1].reshape(-1, 1, 2)
        if len(pts) < 60: pts = cv2.goodFeaturesToTrack(gray[j], 300, .01, 7, mask=cv2.warpAffine(mask, cur[:2], (W, H)))
        i = j
    return M
M = {**chain(-1), **chain(1)}; ks = sorted(M); arr = np.array([M[k] for k in ks]); M = {k: np.mean(arr[max(0, t - 3):t + 4], 0) for t, k in enumerate(ks)}
# corte del bloque: todo lo que queda bajo la línea del borde superior del bloque
cut = np.zeros(CF[0].shape[:2], np.float32); yy, xx = np.mgrid[0:cut.shape[0], 0:cut.shape[1]]
line_y = 1265 + (xx - 215) * (1225 - 1265) / (1000 - 215); cut[yy < line_y] = 1; cut = cv2.GaussianBlur(cut, (0, 0), 2)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', 'v_comp.mp4'], stdin=subprocess.PIPE)
for i in range(n):
    f = P[i].astype(np.float32); k = min(int(round(i / 30 * 24)), len(CF) - 1)
    g = CF[k].astype(np.float32)
    bd = g[..., 0] - np.maximum(g[..., 1], g[..., 2])                      # dominancia del azul
    a = np.clip(1 - (bd - 25) / 80, 0, 1) * cut
    a[:8] = 0; a[:, :8] = 0; a[:, -8:] = 0; a = cv2.GaussianBlur(a, (0, 0), .8)
    g[..., 0] = np.minimum(g[..., 0], (g[..., 1] + g[..., 2]) / 2 + 12)   # quitar derrame azul
    Tm = np.float32([[SC, 0, SEAT_P[0] - SC * SEAT_C[0]], [0, SC, SEAT_P[1] - SC * SEAT_C[1]], [0, 0, 1]])
    A = (M[i] @ Tm)[:2]
    wg = cv2.warpAffine(g, A, (W, H), flags=cv2.INTER_AREA); wa = cv2.warpAffine(a, A, (W, H))
    # sombra de contacto sobre el escritorio
    sh = np.zeros((H, W), np.float32); p = (M[i] @ np.float32([*SEAT_P, 1]))[:2]
    cv2.ellipse(sh, (int(p[0]), int(p[1]) + 6), (190, 22), 0, 0, 360, 1, -1); sh = cv2.GaussianBlur(sh, (0, 0), 14) * .45
    f *= (1 - sh[..., None])
    # luz: cuarto de día, cálido suave
    wg = wg * np.float32([0.97, 0.99, 1.02])
    f = f * (1 - wa[..., None]) + cv2.GaussianBlur(wg, (0, 0), .6) * wa[..., None]
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', n)
