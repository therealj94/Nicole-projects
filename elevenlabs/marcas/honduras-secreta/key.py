# Recorte del fondo liso de los clips de Veo: placa limpia + relleno desde los bordes
import cv2, numpy as np, sys
src, out_prefix = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
F = np.array(frames).astype(np.float32)
h, w = F.shape[1:3]
# placa limpia: color de fondo por fila desde los bordes laterales (fondo con leve degradado)
border = np.concatenate([F[:, :, :24], F[:, :, -24:]], 2)            # n,h,48,3
plate_row = np.median(border.reshape(-1, h, 48, 3).transpose(1, 0, 2, 3).reshape(h, -1, 3), 1)  # h,3
plate = np.repeat(plate_row[:, None, :], w, 1)
def matte(f):
    d = np.sqrt(((f - plate) ** 2).sum(2))
    hsv = cv2.cvtColor(f.astype(np.uint8), cv2.COLOR_BGR2HSV)
    sat = hsv[..., 1].astype(np.float32)
    core = ((d > 26) | (sat > 70)).astype(np.uint8)
    # quedarse con componentes grandes (el ave), quitar ruido
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, 8)
    keep = np.zeros_like(core)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500: keep[lab == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    # rellenar huecos internos (sombrero/pico claros)
    ff = keep.copy(); m = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 1)
    keep = keep | (1 - ff)
    soft = np.clip((d - 14) / 18, 0, 1)
    a = np.where(cv2.dilate(keep, np.ones((5, 5), np.uint8)) > 0, np.maximum(keep * 1.0, soft), 0)
    a = cv2.GaussianBlur(a.astype(np.float32), (5, 5), 0)
    return np.clip(a, 0, 1)
for i, f in enumerate(F):
    a = matte(f)
    rgba = np.dstack([f, a * 255]).astype(np.uint8)
    cv2.imwrite(f"{out_prefix}_{i:04d}.png", rgba)
print(len(F), w, h)
