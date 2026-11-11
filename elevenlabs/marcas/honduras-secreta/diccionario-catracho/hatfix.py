# Reemplaza el parche blanco del sombrero (imagen fija) por el logo oficial, conservando la luz y el borde.
import cv2, numpy as np, sys
SHMIN = .6
LOGO = cv2.imread('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png', -1)
def find_quad(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 1] < 45) & (hsv[..., 2] > 170)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    m[im.shape[0] // 2:] = 0  # el parche está en la mitad superior
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    for c in cs:
        a = cv2.contourArea(c)
        if a < 4000: continue
        r = cv2.minAreaRect(c); w, h = r[1]
        if min(w, h) == 0: continue
        ar = max(w, h) / min(w, h); fill = a / (w * h)
        if 1.6 < ar < 3.4 and fill > .8 and (best is None or a > best[0]): best = (a, c)
    if best is None: return None
    c = best[1]; peri = cv2.arcLength(c, True)
    for eps in np.linspace(.01, .08, 15):
        ap = cv2.approxPolyDP(c, eps * peri, True)
        if len(ap) == 4: break
    q = ap.reshape(-1, 2).astype(np.float32) if len(ap) == 4 else cv2.boxPoints(cv2.minAreaRect(c)).astype(np.float32)
    s = q.sum(1); d = np.diff(q, axis=1)[:, 0]
    return np.float32([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]])  # tl tr br bl
def fix(src, out, q=None, inset=-.015):
    im = cv2.imread(src); H, W = im.shape[:2]
    if q is None: q = find_quad(im)
    if q is None: print('sin parche', src); cv2.imwrite(out, im); return None
    q = np.float32(q)
    c = q.mean(0); qi = c + (q - c) * (1 - inset)  # interior, deja el borde cosido de la IA
    pw = int(np.linalg.norm(qi[1] - qi[0])); ph = int(np.linalg.norm(qi[3] - qi[0]))
    # sombreado: luminancia del parche original sin el texto
    M = cv2.getPerspectiveTransform(qi, np.float32([[0, 0], [pw, 0], [pw, ph], [0, ph]]))
    flat = cv2.warpPerspective(im, M, (pw, ph)).astype(np.float32)
    hsv = cv2.cvtColor(flat.astype(np.uint8), cv2.COLOR_BGR2HSV)
    low = (hsv[..., 1] < 50) & (hsv[..., 2] > 120)
    px = flat[low] if low.sum() > 200 else flat.reshape(-1, 3)
    lum = px.mean(1); sel = (lum >= np.percentile(lum, 80)) & (lum <= np.percentile(lum, 97))
    base = px[sel].mean(0)
    g = cv2.cvtColor(flat.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    g[~low] = np.median(g[low]) if low.sum() > 200 else g.mean()
    sh = cv2.GaussianBlur(g, (0, 0), max(pw, ph) / 6); sh = np.clip(sh / np.percentile(sh, 85), SHMIN, 1.05)
    canvas = np.ones((ph, pw, 3), np.float32) * base * .97
    lh, lw = LOGO.shape[:2]; sc = min(pw * .92 / lw, ph * .82 / lh)
    L = cv2.resize(LOGO, (int(lw * sc), int(lh * sc)), interpolation=cv2.INTER_AREA).astype(np.float32)
    x0 = (pw - L.shape[1]) // 2; y0 = (ph - L.shape[0]) // 2
    a = L[..., 3:] / 255
    canvas[y0:y0 + L.shape[0], x0:x0 + L.shape[1]] = canvas[y0:y0 + L.shape[0], x0:x0 + L.shape[1]] * (1 - a) + L[..., :3] * .93 * a
    # borde cosido
    t = max(2, ph // 28); m = max(3, ph // 14)
    bd = np.ones((ph, pw), np.float32); cv2.rectangle(bd, (0, 0), (pw - 1, ph - 1), .78, t)
    for xx in range(m, pw - m, max(4, ph // 18)):
        cv2.line(bd, (xx, m), (xx + max(2, ph // 36), m), .82, 1); cv2.line(bd, (xx, ph - m), (xx + max(2, ph // 36), ph - m), .82, 1)
    bd = cv2.GaussianBlur(bd, (0, 0), .8)
    canvas = canvas * sh[..., None] * bd[..., None]
    canvas += np.random.normal(0, 3, canvas.shape)
    Mi = cv2.getPerspectiveTransform(np.float32([[0, 0], [pw, 0], [pw, ph], [0, ph]]), qi)
    wl = cv2.warpPerspective(canvas, Mi, (W, H)); wm = np.zeros((H, W), np.float32)
    cv2.fillConvexPoly(wm, qi.astype(np.int32), 1); wm = cv2.GaussianBlur(wm, (0, 0), 1.5)
    wl = cv2.GaussianBlur(wl, (0, 0), .6)
    res = im * (1 - wm[..., None]) + wl * wm[..., None]
    cv2.imwrite(out, np.clip(res, 0, 255).astype(np.uint8))
    x, y = q.min(0).astype(int); X, Y = q.max(0).astype(int)
    return (max(0, x - 120), max(0, y - 80), X + 120, Y + 120)
if __name__ == '__main__':
    import os; os.makedirs('fix', exist_ok=True); crops = []
    for n in sys.argv[1:]:
        r = fix(n + '.png', 'fix/' + n + '.png')
        if r:
            a = cv2.imread('fix/' + n + '.png'); b = cv2.imread(n + '.png'); x, y, X, Y = r
            crops.append(cv2.resize(np.hstack([b[y:Y, x:X], a[y:Y, x:X]]), (900, 300)))
    cv2.imwrite('fixcheck.jpg', np.vstack(crops))
