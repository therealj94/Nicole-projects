# Reemplazo robusto del parche del sombrero:
# 1) busca el cuadro donde el parche se ve mejor (ancla), 2) sigue el sombrero hacia adelante y atrás (KLT + afín),
# 3) verifica cada cuadro comparando con la apariencia del parche en el ancla; si falla, el logo se desvanece.
import cv2, numpy as np, sys, subprocess, json
args = sys.argv[1:]; ANCHS = []; ROI = None
if '--roi' in args:
    k = args.index('--roi'); ROI = [float(a) for a in args[k + 1:k + 5]]; del args[k:k + 5]   # x0 y0 x1 y1 en fracción del cuadro
while '--anchor' in args:      # --anchor CUADRO x1 y1 x2 y2 x3 y3 x4 y4   (coordenadas a media resolución)
    k = args.index('--anchor'); v = [float(a) for a in args[k + 1:k + 10]]; ANCHS.append((int(v[0]), np.float32(v[1:]).reshape(4, 2))); del args[k:k + 10]
src, out = args[0], args[1]; PREVIEW = [int(x) for x in args[2:]]
W4, H4 = [int(v) for v in subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height','-of','csv=p=0',src]).decode().strip().split(',')]; DS = 2; w, h = W4 // DS, H4 // DS
ref = cv2.imread('/tmp/claude-0/-home-user-Nicole-projects/dd5b2fc2-184e-5514-b789-f8432119b327/scratchpad/hs/guaca_zip/shot_13_close-up.jpg')
P = ref[100:223, 398:651].astype(np.float32); ph, pw = P.shape[:2]
Pg = cv2.cvtColor(P.astype(np.uint8), cv2.COLOR_BGR2GRAY)
pm = np.zeros((ph, pw), np.float32); cv2.rectangle(pm, (3, 3), (pw - 4, ph - 4), 1, -1); pm = cv2.GaussianBlur(pm, (0, 0), 2.0)
# pasada 1: cuadros en gris a media resolución
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE).stdout
G = np.frombuffer(raw, np.uint8).reshape(-1, h, w); n = len(G)
def find(g, scales=np.linspace(.2, 2.6, 40)):
    best = (-1, None)
    gs = cv2.resize(g, (w // 2, h // 2))
    for sc in scales:
        t = cv2.resize(Pg, None, fx=sc, fy=sc)
        if t.shape[1] < 18 or t.shape[0] >= gs.shape[0] or t.shape[1] >= gs.shape[1]: continue
        r = cv2.matchTemplate(gs, t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
        if mv > best[0]: best = (mv, (ml[0] * 2, ml[1] * 2, t.shape[1] * 2, t.shape[0] * 2))
    return best
_rawc = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f"select='not(mod(n\\,6))',scale={w}:{h}", '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE).stdout
COL = np.frombuffer(_rawc, np.uint8).reshape(-1, h, w, 3)
def on_hat(g, box, idx=None):                       # el parche debe estar rodeado de tela beige (no pelo blanco, piel ni cartón)
    x, y, tw, th = box; H_, W_ = g.shape
    if ROI and not (ROI[0] * W_ <= x + tw / 2 <= ROI[2] * W_ and ROI[1] * H_ <= y + th / 2 <= ROI[3] * H_): return False
    xa, ya, xb, yb = max(0, x - tw // 3), max(0, y - th // 2), min(W_, x + tw + tw // 3), min(H_, y + th + th // 2)
    m = np.ones((yb - ya, xb - xa), bool); m[max(0, y - ya):y - ya + th, max(0, x - xa):x - xa + tw] = False
    if idx is None or idx // 6 >= len(COL): return False
    hsv = cv2.cvtColor(COL[idx // 6][ya:yb, xa:xb], cv2.COLOR_BGR2HSV)[m]
    if hsv.shape[0] < 50: return False
    hh, ss, vv = np.median(hsv[:, 0]), np.median(hsv[:, 1]), np.median(hsv[:, 2])
    return 8 <= hh <= 32 and 25 <= ss <= 100 and vv >= 140
if not ANCHS:
    cands = [(find(G[i]), i) for i in range(0, n, 6)]
    for w0 in range(0, n, 36):                     # un ancla por ventana de 1.5 s si el parche se reconoce
        win = [c for c in cands if w0 <= c[1] < w0 + 36 and c[0][1] is not None]
        if not win: continue
        win = [c for c in win if on_hat(G[c[1]], c[0][1], c[1])]
        if not win: continue
        (score, (x, y, tw, th)), A0 = max(win, key=lambda c: c[0][0])
        if score > .5: ANCHS.append((A0, np.float32([[x, y], [x + tw, y], [x + tw, y + th], [x, y + th]])))
    if not ANCHS:
        (score, (x, y, tw, th)), A0 = max([c for c in cands if c[0][1] is not None and on_hat(G[c[1]], c[0][1], c[1])] or cands, key=lambda c: c[0][0])
        ANCHS = [(A0, np.float32([[x, y], [x + tw, y], [x + tw, y + th], [x, y + th]]))]
print('anclas', [a for a, _ in ANCHS], file=sys.stderr)
def crop_warp(g, q, size=(128, 64)):
    M = cv2.getPerspectiveTransform(q.astype(np.float32), np.float32([[0, 0], [size[0], 0], [size[0], size[1]], [0, size[1]]]))
    return cv2.warpPerspective(g, M, size).astype(np.float32)
def ncc(a, b): a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))
def seed(g, q):
    c = q.mean(0); m = np.zeros_like(g); cv2.fillConvexPoly(m, ((q - c) * 1.8 + c).astype(np.int32), 255)
    return cv2.goodFeaturesToTrack(g, 300, 0.01, 5, mask=m)
def track(A0, q0, direction):
    Q = {A0: q0.copy()}; q = q0.copy(); pts = seed(G[A0], q); i = A0
    while 0 <= i + direction < n:
        j = i + direction; okf = False
        if pts is not None and len(pts) >= 8:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(G[i], G[j], pts, None, winSize=(21, 21), maxLevel=4)
            b_, _, _ = cv2.calcOpticalFlowPyrLK(G[j], G[i], p1, None, winSize=(21, 21), maxLevel=4)
            ok = (st[:, 0] == 1) & (np.linalg.norm((b_ - pts).reshape(-1, 2), axis=1) < 1.0)
            if ok.sum() >= 8:
                A, inl = cv2.estimateAffine2D(pts[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
                if A is not None:
                    q = cv2.transform(q[None], A)[0]; keep = ok.copy(); keep[ok] = inl[:, 0].astype(bool); pts = p1[keep].reshape(-1, 1, 2); okf = True
        if not okf: break
        if len(pts) < 60: pts = seed(G[j], q)
        Q[j] = q.copy(); i = j
    return Q
best = {}
for A0, q0 in ANCHS:
    app = crop_warp(G[A0], q0)
    for d in (-1, 1):
        for i, q in track(A0, q0, d).items():
            if np.linalg.norm(q[1] - q[0]) < 20: continue
            c = ncc(crop_warp(G[i], q), app)
            if c > best.get(i, (-9, None))[0]: best[i] = (c, q)
Q = {i: q for i, (c, q) in best.items() if c > .40}
# validación por cuadro: anillo de tela beige alrededor + parche claro adentro (a 1/4 de resolución)
_rq = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f'scale={w//2}:{h//2}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE).stdout
CQ = np.frombuffer(_rq, np.uint8).reshape(-1, h // 2, w // 2, 3)
def valid(i, q):
    if i >= len(CQ): return False
    qq = (q / 2).astype(np.float32); c = qq.mean(0)
    hsv = cv2.cvtColor(CQ[i], cv2.COLOR_BGR2HSV)
    inner = np.zeros(hsv.shape[:2], np.uint8); cv2.fillConvexPoly(inner, qq.astype(np.int32), 1)
    outer = np.zeros_like(inner); cv2.fillConvexPoly(outer, ((qq - c) * 1.9 + c).astype(np.int32), 1)
    ring = (outer > 0) & (inner == 0)
    if inner.sum() < 30 or ring.sum() < 50: return False
    r = hsv[ring]; beige = (r[:, 0] >= 6) & (r[:, 0] <= 34) & (r[:, 1] >= 20) & (r[:, 1] <= 120) & (r[:, 2] >= 120)
    p = hsv[inner > 0]; light = np.mean(p[:, 2] > 150)
    return np.mean(beige) > .45 and light > .45
bad = [i for i, q in Q.items() if not valid(i, q)]
for i in bad: del Q[i]
print('descartados por validación', len(bad), file=sys.stderr)
vis = np.array([1.0 if i in Q else 0.0 for i in range(n)])
v = np.convolve(vis, np.ones(3) / 3, 'same') > .5
vis = np.convolve(v.astype(float), np.ones(5) / 5, 'same'); score = 0
print(f'visibles {int((vis > .5).sum())}/{n} cuadros', file=sys.stderr)
keys = sorted(Q); arr = np.array([Q[k] for k in keys])
sm = np.array([np.mean(arr[max(0, i - 2):i + 3], 0) for i in range(len(arr))]); Qs = {k: sm[t] * DS for t, k in enumerate(keys)}
print(f'visibles {int((vis > .5).sum())}/{n} cuadros', file=sys.stderr)
# pasada 2: componer en 4K
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
enc = None if PREVIEW else subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W4}x{H4}', '-r', '24', '-i', '-', '-i', src,
                       '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '13', '-pix_fmt', 'yuv420p', '-c:a', 'copy', out], stdin=subprocess.PIPE)
refbeige = np.median(P[pm > .9][P[pm > .9].sum(1) > 500], 0)
for i in range(n):
    b = dec.stdout.read(W4 * H4 * 3)
    if len(b) < W4 * H4 * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H4, W4, 3)
    if i in Qs and vis[i] > .01:
        qs = Qs[i]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [pw, 0], [pw, ph], [0, ph]]), qs.astype(np.float32))
        x0, y0 = np.maximum(qs.min(0).astype(int) - 40, 0); x1, y1 = np.minimum(qs.max(0).astype(int) + 40, [W4, H4])
        if x1 > x0 + 10 and y1 > y0 + 10:
            T = np.float32([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]]) @ M
            wl = cv2.warpPerspective(P, T, (x1 - x0, y1 - y0)); wm = cv2.warpPerspective(pm, T, (x1 - x0, y1 - y0)) * vis[i]
            roi = f[y0:y1, x0:x1].astype(np.float32)
            ring = (cv2.dilate((wm > .02).astype(np.uint8), np.ones((31, 31), np.uint8)) > 0) & (wm < .02)
            gain = np.clip(np.median(roi[ring], 0) / np.maximum(refbeige, 1), .35, 1.3) if ring.sum() > 50 else np.ones(3)
            scale = np.linalg.norm(qs[1] - qs[0]) / pw
            lw = cv2.GaussianBlur(wl * gain, (0, 0), max(.5, .8 / max(scale, .3))) + np.random.normal(0, 2.5, wl.shape)
            roi = roi * (1 - wm[..., None]) + lw * wm[..., None]
            f = f.copy(); f[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)
            if PREVIEW and i in PREVIEW: cv2.imwrite(f'patch_{i}.png', f[max(0, y0 - 250):y1 + 450, max(0, x0 - 350):x1 + 350])
    elif PREVIEW and i in PREVIEW: cv2.imwrite(f'patch_{i}.png', cv2.resize(f, (960, 540)))
    if enc: enc.stdin.write(f.tobytes())
    if PREVIEW and i >= max(PREVIEW): break
dec.terminate()
if enc: enc.stdin.close(); enc.wait()
if not PREVIEW: json.dump({'anchors': [a for a, _ in ANCHS], 'visible': int((vis > .5).sum()), 'frames': n}, open(out + '.json', 'w'))
print('ok', out, file=sys.stderr)
