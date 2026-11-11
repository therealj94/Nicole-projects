# Escena 1: guara (fondo verde) aterriza en el escritorio de Nicole. Sigue la cámara en mano.
import cv2, numpy as np, subprocess, json, sys
PLATE = '../real/t1_1080.mov'; G = 'land_fix.mp4'
T0 = float(sys.argv[1]) if len(sys.argv) > 1 else 3.3     # segundo de la toma en que entra la guara
REF = 150                                              # cuadro de referencia donde medí el escritorio
LAND_PLATE = np.float32([190, 1585])                   # punto del escritorio (en cuadro REF)
LAND_G = np.float32([540, 1335]); SC = 0.45
PERSON = np.load('person.npy')[..., 0]            # pies de la guara en el clip verde y escala
def frames(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
P = frames(PLATE); GF = frames(G); n = len(P)
# --- seguimiento de cámara: transformación de cada cuadro respecto a REF (región izquierda: laptop, pared, escritorio)
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in P]
mask = np.zeros_like(gray[0]); mask[800:1500, 0:400] = 255
def chain(direction):
    M = {REF: np.eye(3)}; cur = np.eye(3); i = REF
    pts = cv2.goodFeaturesToTrack(gray[i], 400, .01, 7, mask=mask)
    while 0 <= i + direction < n:
        j = i + direction
        p1, st, _ = cv2.calcOpticalFlowPyrLK(gray[i], gray[j], pts, None, winSize=(25, 25), maxLevel=4)
        ok = st[:, 0] == 1
        A, inl = cv2.estimateAffinePartial2D(pts[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2)
        A3 = np.vstack([A, [0, 0, 1]]); cur = A3 @ cur; M[j] = cur.copy()
        pts = p1[ok][inl[:, 0] == 1].reshape(-1, 1, 2)
        if len(pts) < 80:
            m2 = cv2.warpAffine(mask, cur[:2], mask.shape[::-1]); pts = cv2.goodFeaturesToTrack(gray[j], 400, .01, 7, mask=m2)
        i = j
    return M
M = {**chain(-1), **chain(1)}
# suavizar levemente la trayectoria
keys = sorted(M); arr = np.array([M[k] for k in keys])
M = {k: np.mean(arr[max(0, t - 2):t + 3], 0) for t, k in enumerate(keys)}
# --- tiempo de la guara (24 fps -> 30 fps); el vuelo inicial (cuadros 0-13) se alarga a 0.9 s
FLY = 0.9
def gsrc(tp):
    t = tp - T0
    if t < 0: return None
    if t < FLY: return t / FLY * 13
    k = 13 + (t - FLY) * 24
    return k if k < len(GF) - 1 else None
def entry_offset(tp):                                   # desplazamiento extra: entra desde arriba a la derecha
    t = tp - T0
    if t >= FLY: return np.zeros(2)
    e = 1 - t / FLY; return np.float32([620, -900]) * e ** 2
plate_h, plate_w = P[0].shape[:2]
lum_plate = None
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{plate_w}x{plate_h}', '-r', '30', '-i', '-',
                        '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', 'v_comp.mp4'], stdin=subprocess.PIPE)
BLK = (110, 1290, 500, 1600)
for i in range(n):
    f = P[i].astype(np.float32); tp = i / 30; k = gsrc(tp)
    if k is not None:
        g = GF[int(round(k))].astype(np.float32)
        # alfa por dominancia del verde + quitar el bloque negro
        gd = g[..., 1] - np.maximum(g[..., 0], g[..., 2])
        a = np.clip(1 - (gd - 15) / 70, 0, 1)
        hsv = cv2.cvtColor(g.astype(np.uint8), cv2.COLOR_BGR2HSV)
        x0, y0, x1, y1 = BLK; blk = np.zeros_like(a, bool); blk[y0:y1, x0:x1] = True
        a[blk & (hsv[..., 2] < 85) & (hsv[..., 1] < 90)] = 0
        edge = np.zeros_like(a, bool); edge[1280:1620, 100:385] = True; a[edge & (hsv[..., 1] < 80)] = 0
        if k < 14: a[1270:1630, 100:500] = 0
        a[:10] = 0; a[-10:] = 0; a[:, :10] = 0; a[:, -10:] = 0
        a = cv2.GaussianBlur(a, (0, 0), .8)
        # quitar derrame verde
        g[..., 1] = np.minimum(g[..., 1], (g[..., 0] + g[..., 2]) / 2 + 10)
        # igualar luz al cuarto (día suave): bajar contraste y saturación un poco
        g = cv2.addWeighted(g, .9, np.full_like(g, g[a > .5].mean() if (a > .5).any() else 128), .1, 0)
        # transformación: escala + posición en la referencia + movimiento de cámara
        off = entry_offset(tp)
        S = np.float32([[SC, 0, 0], [0, SC, 0], [0, 0, 1]])
        Tm = np.float32([[1, 0, LAND_PLATE[0] - SC * LAND_G[0] + off[0]], [0, 1, LAND_PLATE[1] - SC * LAND_G[1] + off[1]], [0, 0, 1]])
        A = (M[i] @ Tm @ S)[:2]
        wg = cv2.warpAffine(g, A, (plate_w, plate_h), flags=cv2.INTER_AREA if SC < 1 else cv2.INTER_LINEAR)
        wa = cv2.warpAffine(a, A, (plate_w, plate_h))
        # sombra de contacto en el escritorio cuando ya aterrizó
        if tp - T0 > FLY * .8:
            sh = np.zeros((plate_h, plate_w), np.float32)
            p = (M[i] @ np.float32([*LAND_PLATE, 1]))[:2]
            cv2.ellipse(sh, (int(p[0]) + 5, int(p[1]) + 4), (80, 14), 0, 0, 360, 1, -1)
            sh = cv2.GaussianBlur(sh, (0, 0), 9) * .45 * min(1, (tp - T0 - FLY * .8) / .2)
            f *= (1 - sh[..., None])
        wg = cv2.GaussianBlur(wg, (0, 0), .5)
        pm = cv2.GaussianBlur(PERSON[i].astype(np.float32) / 255, (0, 0), 1.5); wa = wa * (1 - pm)
        f = f * (1 - wa[..., None]) + wg * wa[..., None]
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', n)
