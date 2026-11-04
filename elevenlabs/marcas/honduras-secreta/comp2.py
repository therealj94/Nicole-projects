# Integra a José (clip Veo recortado) en la toma de dron con seguimiento, oclusión de flores y sombra
import cv2, numpy as np, json, glob, math, sys
from PIL import Image, ImageFilter, ImageEnhance
V = sys.argv[1]; OUT = sys.argv[2]; ONLY = [float(x) for x in sys.argv[3:]]
TR = {int(k): v for k, v in json.load(open('track.json'))['track'].items()}
_P = json.load(open('people.json'))
_Y = {int(k): v for k, v in _P['yellow'].items()}; _L = {int(k): v for k, v in _P['lady'].items()}
def _series(fn, n=600):
    xs = np.array([fn(i) if fn(i) is not None else np.nan for i in range(n)], float)
    idx = np.arange(n); ok = ~np.isnan(xs)
    xs = np.interp(idx, idx[ok], xs[ok])
    k = np.ones(11) / 11; return np.convolve(np.pad(xs, 5, mode='edge'), k, mode='valid')
GX = _series(lambda i: (_Y[i][0] + _L[i][0]) / 2 if i in _Y and i in _L else None)
SH = _series(lambda i: _Y[i][3] if i in _Y else None)
GY = _series(lambda i: _Y[i][2] if i in _Y else None)
BIRD = sorted(glob.glob('key_full/*.png')); CFPS = 24.0
FEET = (360, 1182); BIRD_H = 580              # pies y altura del ave en el clip 720x1280
T_IN, T_CUT, T_RESUME = 1.6, 4.55, 4.20       # salto del tramo con "mano" (3.05-4.15 s del clip)
H_SCENE = 100                                  # altura del ave en escena cuando s = 1
A_REF = TR[75][3]
def clip_time(t):
    if t < T_IN: return None
    if t < T_IN + 2.95: return t - T_IN
    return T_RESUME + (t - (T_IN + 2.95))
def bird_rgba(ct):
    i = min(len(BIRD) - 1, int(ct * CFPS)); im = Image.open(BIRD[i]).convert('RGBA')
    a = np.array(im.getchannel('A')).astype(np.float32); h, w = a.shape        # desvanecer bordes del clip
    fx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 40, 0, 1); fy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / 40, 0, 1)
    a *= fx[None, :] * fy[:, None]; im.putalpha(Image.fromarray(a.astype(np.uint8)))
    rgb = ImageEnhance.Color(ImageEnhance.Contrast(im.convert('RGB')).enhance(.94)).enhance(.9)
    r, g, b = rgb.split(); rgb = Image.merge('RGB', (r.point(lambda v: min(255, v * 1.04)), g, b.point(lambda v: v * .95)))
    rgb.putalpha(im.getchannel('A')); return rgb
def compose(frame_bgr, t, fi):
    img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)).convert('RGBA')
    ct = clip_time(t)
    if ct is None or ct > 7.6 or fi not in TR: return img
    _, _, _, a = TR[fi]
    x = float(GX[fi]); sh = float(SH[fi]); y = float(GY[fi]) + .45 * sh                    # pies a la altura de las flores, en el hueco
    s_cam = TR[fi][2] / TR[78][2]                                     # escala estable del seguimiento de cámara
    sh_ref = float(SH[78])
    y = float(GY[fi]) + .45 * sh_ref * s_cam
    s = sh_ref * s_cam / 80.0
    k = 1.55 * sh_ref * s_cam / BIRD_H                                 # la cabeza le llega al pecho de las chicas
    pop = min(1, (t - T_IN) / .25)                                     # aparición suave
    b = bird_rgba(ct)
    if abs(t - (T_IN + 2.95)) < .12:                                   # fundido en el corte
        b2 = bird_rgba(T_RESUME + (t - (T_IN + 2.95)) if t < T_IN + 2.95 else T_IN + 2.95 - T_IN)
        b = Image.blend(b, b2, .5)
    bw, bh = int(b.width * k), int(b.height * k)
    if bw < 4: return img
    b = b.resize((bw, bh), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.9))
    ba = np.array(b).astype(np.float32); ba[..., :3] += np.random.normal(0, 3.2, ba[..., :3].shape)
    b = Image.fromarray(np.clip(ba, 0, 255).astype(np.uint8), 'RGBA')
    fx, fy = FEET[0] * k, FEET[1] * k
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # sombra de contacto (solo mientras está en el suelo)
    ground = max(0, 1 - max(0, ct - 5.2) / .5)
    if ground > 0:
        sh = Image.new('L', (int(110 * k * 3), int(30 * k * 3)), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(sh).ellipse((0, 0, sh.width - 1, sh.height - 1), fill=int(120 * ground))
        sh = sh.filter(ImageFilter.GaussianBlur(6 * k * 3))
        shl = Image.new('RGBA', sh.size, (20, 12, 5, 255)); shl.putalpha(sh)
        layer.alpha_composite(shl, (int(x - sh.width / 2), int(y - sh.height / 2)))
    layer.alpha_composite(b, (int(x - fx), int(y - fy)))
    ang = -(a - A_REF)
    layer = layer.rotate(ang, center=(x, y), resample=Image.BICUBIC)
    if pop < 1: layer.putalpha(layer.getchannel('A').point(lambda v: int(v * pop)))
    img.alpha_composite(layer)
    # oclusión: flores naranjas delante de las patas
    if ground > 0:
        fr = np.array(Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)))
        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        orange = ((hsv[..., 0] >= 5) & (hsv[..., 0] <= 22) & (hsv[..., 1] > 150) & (hsv[..., 2] > 150)).astype(np.float32)
        band = np.zeros_like(orange); y0 = int(y - 26 * s); band[max(0, y0):int(y + 30 * s), int(x - 80 * s):int(x + 80 * s)] = 1
        m = cv2.GaussianBlur(orange * band, (5, 5), 0) * ground
        fl = Image.fromarray(fr).convert('RGBA'); fl.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
        img.alpha_composite(fl)
    return img
cap = cv2.VideoCapture(V); fps = cap.get(cv2.CAP_PROP_FPS); fi = 0
wr = None if ONLY else cv2.VideoWriter(OUT, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1440, 1080))
while True:
    ok, f = cap.read()
    if not ok: break
    t = fi / fps
    if ONLY:
        for o in ONLY:
            if abs(t - o) < .5 / fps: compose(f, t, fi).convert('RGB').save(f'comp_{o:.1f}.png')
    else:
        wr.write(cv2.cvtColor(np.array(compose(f, t, fi).convert('RGB')), cv2.COLOR_RGB2BGR))
    fi += 1
if wr: wr.release()
