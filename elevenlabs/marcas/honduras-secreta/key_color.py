# Recorte por color de fondo por cuadro (gris poco saturado), robusto a movimientos de cámara del clip
import cv2, numpy as np, sys
src, out_prefix = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    h, w = f.shape[:2]
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); sat = hsv[..., 1].astype(np.float32); val = hsv[..., 2].astype(np.float32)
    low = sat < 30
    # fondo: gris de baja saturación; modelar brillo del fondo suavizado espacialmente (viñeta)
    bgv = np.where(low, val, np.nan)
    small = cv2.resize(np.nan_to_num(bgv, nan=0), (w // 16, h // 16), interpolation=cv2.INTER_AREA)
    cnt = cv2.resize(low.astype(np.float32), (w // 16, h // 16), interpolation=cv2.INTER_AREA)
    est = np.where(cnt > .2, small / np.maximum(cnt, 1e-3), np.nan)
    med = np.nanmedian(est)
    est = np.where(np.isnan(est), med, est)
    est = cv2.GaussianBlur(cv2.resize(est.astype(np.float32), (w, h)), (0, 0), 25)
    dv = np.abs(val - est)
    score = np.maximum(np.clip((sat - 32) / 20, 0, 1), np.clip((dv - 22) / 16, 0, 1))
    core = (score > .5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, 8)
    keep = np.zeros_like(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] > 900: keep[lab == k] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    ff = np.pad(keep, 1); m = np.zeros((h + 4, w + 4), np.uint8); cv2.floodFill(ff, m, (0, 0), 1); keep = keep | (1 - ff[1:-1, 1:-1])
    a = cv2.GaussianBlur(np.where(cv2.dilate(keep, np.ones((3, 3), np.uint8)) > 0, np.maximum(keep, score), 0).astype(np.float32), (5, 5), 0)
    cv2.imwrite(f"{out_prefix}_{i:04d}.png", np.dstack([f, np.clip(a, 0, 1) * 255]).astype(np.uint8)); i += 1
print(i)
