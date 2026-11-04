#!/usr/bin/env python3
"""Honduras Secreta · "Copán Ruinas: el secreto naranja" — montaje vertical 1080x1920 @24 fps.

Se ejecuta dentro de la carpeta de trabajo (v3) con: veo_s1.mp4, veo_s5.mp4, ../v2/fly_logo.mp4, ../v2/people.json,
los JSON de tiempos de voz (l*_*.json) y la toma original del dron.
Uso: edit_v3.py DRONE.mp4 FONTS_DIR [segundos para vista previa...]
"""
import subprocess, json, math, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 24
DRONE, FD = sys.argv[1], sys.argv[2].rstrip('/') + '/'
ONLY = [float(x) for x in sys.argv[3:]]
GRADE = "eq=contrast=1.06:brightness=0.015:saturation=1.12:gamma=1.03,colorbalance=rs=0.02:bs=-0.02:rm=0.015:bm=-0.015"

def run(cmd, size):
    b = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    n = len(b) // size; return [b[i * size:(i + 1) * size] for i in range(n)]
def vid(path, ss, t, vf):
    return run(['ffmpeg', '-loglevel', 'error', '-ss', str(ss), '-t', str(t), '-i', path, '-fps_mode', 'passthrough', '-vf', vf,
                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], W * H * 3)
def drone(sel):
    return run(['ffmpeg', '-loglevel', 'error', '-i', DRONE, '-fps_mode', 'passthrough', '-vf', sel + ',' + GRADE,
                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], 1440 * 1080 * 3)

# ---------------- tomas ----------------
GR = f'fps=24,scale={W}:{H},eq=contrast=1.04:saturation=1.06:gamma=1.02'
A = vid('v_macro.mp4', 0.6, 3.0, GR)                                     # flor con rocío y abeja
B = vid('v_perch.mp4', 0.0, 7.4, GR)                                     # guara en la rama, despega
F = vid('v_fly.mp4', 1.2, 5.0, GR)                                       # guara volando hacia cámara
C = drone('select=between(n\\,87\\,206),setpts=N/24/TB')            # gente real saludando (0.8x)
Pt = vid('v_petals.mp4', 0.2, 3.0, 'crop=888:1580:96:170,' + GR)                                   # pétalos al viento
E = vid('v_valley.mp4', 0.0, 8.0, GR)                                    # valle soleado (toma continua)
SEG = [('A', A), ('B', B), ('F', F), ('C', C), ('P', Pt), ('E', E)]
START = {}; acc = 0
for name, fr in SEG: START[name] = acc / FPS; acc += len(fr)
TOTAL = acc
P = json.load(open('../v2/people.json')); Y = {int(k): v for k, v in P['yellow'].items()}; L = {int(k): v for k, v in P['lady'].items()}
cx = []
for i in range(87, 207):
    a = Y.get(i, [None])[0]; b = L.get(i, [None])[0]
    cx.append(((a + b) / 2 + 25) if a and b else np.nan)
cx = np.array(cx); ok = ~np.isnan(cx); cx = np.interp(np.arange(len(cx)), np.arange(len(cx))[ok], cx[ok])
cx = np.convolve(np.pad(cx, 12, mode='edge'), np.ones(25) / 25, mode='valid')

def vcrop(b, center, zoom=1.0):
    im = Image.frombytes('RGB', (1440, 1080), b)
    cw, ch = 607.5 / zoom, 1080 / zoom; x0 = min(max(center - cw / 2, 0), 1440 - cw); y0 = (1080 - ch) / 2
    out = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.UnsharpMask(1.6, 70, 2))
    a = np.array(out).astype(np.int16); a += np.random.normal(0, 2.4, a.shape).astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def zoom_blur(im, center, z, blur):
    w, h = im.size; acc = np.zeros((h, w, 3), np.float32); n = 6 if blur > 0 else 1
    for k in range(n):
        zz = z * (1 + blur * k / max(n - 1, 1)); cw, ch = w / zz, h / zz
        x0 = min(max(center[0] - cw / 2, 0), w - cw); y0 = min(max(center[1] - ch / 2, 0), h - ch)
        acc += np.array(im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32)
    return Image.fromarray((acc / n).astype(np.uint8))
def whip(im, amount):
    if amount <= 0: return im
    a = np.array(im, np.float32); k = int(8 + amount * 90); out = np.zeros_like(a)
    for s in range(0, k, max(1, k // 12)): out += np.roll(a, s - k // 2, axis=1)
    out /= len(range(0, k, max(1, k // 12)))
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

# ---------------- voz (tiempos en la línea de tiempo) ----------------
VO = [('l1_b', 0.35), ('l2_a', START['B'] + .9), ('l3_c', START['C'] + .25), ('l4_c', START['E'] + .5), ('l5_b', START['E'] + 4.4)]
WORDS = []
for f, t0 in VO:
    ws = [w for w in json.load(open(f + '.json'))['words'] if w['type'] == 'word']
    WORDS.append([(w['text'], t0 + w['start'], t0 + w['end']) for w in ws])
json.dump({'vo': VO, 'start': START, 'total': TOTAL / FPS}, open('timeline.json', 'w'))

# ---------------- gráficos ----------------
def font(f, s, w=None):
    ft = ImageFont.truetype(FD + f, s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
F_T, F_S, F_K = font('Montserrat[wght].ttf', 100, 850), font('Montserrat[wght].ttf', 50, 600), font('Montserrat[wght].ttf', 34, 700)
F_CAP, F_CAPB = font('Montserrat[wght].ttf', 54, 600), font('Montserrat[wght].ttf', 54, 800)
F_H, F_SEC, F_TAG = font('Montserrat[wght].ttf', 120, 900), font('GreatVibes-Regular.ttf', 120), font('Montserrat[wght].ttf', 44, 600)
BRAND = [(59, 165, 92), (46, 107, 216), (124, 77, 205), (224, 79, 143), (243, 154, 43), (242, 194, 48), (46, 160, 200), (230, 90, 60)]
def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def mask(txt, ft, track=0):
    ws = [ft.getlength(c) for c in txt]; tw = int(sum(ws) + track * (len(txt) - 1)) + 40
    asc, desc = ft.getmetrics(); m = Image.new('L', (tw, asc + desc + 40)); d = ImageDraw.Draw(m); x = 20; pos = []
    for c, w_ in zip(txt, ws): d.text((x, 20), c, font=ft, fill=255); pos.append((x, w_)); x += w_ + track
    return m, pos
def put(lay, m, cxy, alpha, color=(255, 255, 255), shadow=.55, blur=0):
    if alpha <= 0: return
    if blur > .3: m = m.filter(ImageFilter.GaussianBlur(blur))
    x, y = int(cxy[0] - m.width / 2), int(cxy[1] - m.height / 2)
    if shadow:
        sh = Image.new('RGBA', m.size, (0, 0, 0, 255)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * shadow * alpha)))
        lay.alpha_composite(sh, (x + 3, y + 6))
    fl = Image.new('RGBA', m.size, color + (255,)); fl.putalpha(m.point(lambda v: int(v * alpha))); lay.alpha_composite(fl, (x, y))

TITLE, TPOS = mask('COPÁN RUINAS', F_T, 4); SUBT, _ = mask('HONDURAS', F_K, 14)
CAP_MASKS = {}
def caption(lay, t):
    """Subtítulos de José: palabra por palabra, palabras clave en amarillo de la marca."""
    KEY = {'secreto', 'honduras', 'copán', 'ruinas', 'naranja', 'corazón', 'belleza', 'mundo', 'imaginás'}
    for ws in WORDS:
        if not ws: continue
        a, b = ws[0][1] - .1, ws[-1][2] + .6
        if not (a <= t < b): continue
        fade = 1 - ease((t - (b - .25)) / .25)
        lines, cur = [], []
        for w in ws:
            cur.append(w)
            if sum(len(x[0]) + 1 for x in cur) > 20: lines.append(cur[:-1]); cur = [w]
        lines.append(cur)
        for li, line in enumerate([l for l in lines if l]):
            items = []
            for txt, s, e in line:
                k = txt.lower().strip('¡!¿?,.')
                key = (k in KEY) or (txt.lower().strip('¡!,.') in KEY)
                if (txt, key) not in CAP_MASKS: CAP_MASKS[(txt, key)] = mask(txt, F_CAPB if key else F_CAP)[0]
                items.append((CAP_MASKS[(txt, key)], s, key))
            gap = -40 + 16; tw = sum(m.width for m, _, _ in items) + gap * (len(items) - 1)
            x = W / 2 - tw / 2; y = 1290 + li * 72
            for m, s, key in items:
                p = ease((t - (s - .05)) / .18)
                put(lay, m, (x + m.width / 2, y + (1 - p) * 14), p * fade, (255, 214, 64) if key else (255, 255, 255), .7)
                x += m.width + gap

def title(lay, t):
    t0 = START['B'] + .9 + .98                      # "Copán" en la voz
    out = 1 - ease((t - (START['B'] + 5.6)) / .4)
    if t < t0 - .3 or out <= 0: return
    ty = 330
    put(lay, SUBT, (W / 2, ty - 100), ease((t - t0 + .2) / .5) * out)
    for k, (px, pw) in enumerate(TPOS):
        st = t0 + k * .06; p = ease((t - st) / .32)
        if p <= 0: continue
        ch = TITLE.crop((int(px) - 6, 0, int(px + pw) + 6, TITLE.height))
        put(lay, ch, (W / 2 - TITLE.width / 2 + px + pw / 2, ty + (1 - p) * 40), p * out, blur=(1 - p) * 6)
    u = ease((t - (t0 + .8)) / .6)
    if u > 0:
        uw = int(TITLE.width * .78 * u); seg = Image.new('RGBA', (max(1, uw), 10)); sd = ImageDraw.Draw(seg)
        for k in range(6): sd.rectangle((k * uw / 6, 0, (k + 1) * uw / 6, 10), fill=BRAND[k] + (int(255 * out),))
        lay.alpha_composite(seg, (int(W / 2 - TITLE.width * .39), ty + 72))

HON = [mask(c, F_H)[0] for c in 'HONDURAS']; HON_W = [F_H.getlength(c) for c in 'HONDURAS']
SEC = mask('Secreta', F_SEC)[0]; TAG = mask('más de lo que imaginás', F_TAG, 2)[0]
def endcard(lay, t):
    t0 = START['E'] + 4.4                            # "Honduras" en la voz
    if t < t0 - .2: return
    # velo suave para legibilidad
    v = ease((t - t0 + .2) / .6)
    g = Image.new('L', (W, H)); gd = ImageDraw.Draw(g)
    for yy in range(H): gd.line((0, yy, W, yy), fill=int(120 * v * math.exp(-((yy - 820) / 420) ** 2)))
    veil = Image.new('RGBA', (W, H), (10, 8, 6, 255)); veil.putalpha(g); lay.alpha_composite(veil)
    total = sum(HON_W) + 6 * 7; x = W / 2 - total / 2; y = 760
    for k, (m, w_) in enumerate(zip(HON, HON_W)):
        p = ease((t - (t0 + k * .07)) / .35)
        put(lay, m, (x + w_ / 2, y + (1 - p) * 50), p, BRAND[k], .5)
        x += w_ + 6
    s = ease((t - (t0 + .85)) / .6)
    put(lay, SEC, (W / 2 + 120, y + 105), s, (255, 255, 255), .6, blur=(1 - s) * 5)
    tg = ease((t - (t0 + 2.4)) / .5)
    put(lay, TAG, (W / 2, y + 230 + (1 - tg) * 16), tg)

# ---------------- render ----------------
enc = None if ONLY else subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', 'video_v4.mp4'],
                                         stdin=subprocess.PIPE)
# ---------------- color unificado ----------------
import cv2
def lab_stats(ims):
    L = np.concatenate([cv2.cvtColor(np.asarray(i), cv2.COLOR_RGB2LAB).reshape(-1, 3)[::7].astype(np.float32) for i in ims])
    return L.mean(0), L.std(0)
def seg_sample(name):
    fr = dict(SEG)[name]; idx = np.linspace(0, len(fr) - 1, 5).astype(int)
    if name == 'C': return [vcrop(fr[i], float(cx[min(i, len(cx) - 1)])) for i in idx]
    return [Image.frombytes('RGB', (W, H), fr[i]) for i in idx]
REF = lab_stats(seg_sample('E') + seg_sample('C') + seg_sample('B'))      # referencia: campo real soleado + guara
STATS = {nm: lab_stats(seg_sample(nm)) for nm, _ in SEG}
STRENGTH = {'A': .55, 'P': .7}                                           # planos de detalle: igualar sin aplanar
def match(im, name):
    (m, sd), (rm, rsd) = STATS[name], REF; w = STRENGTH.get(name, .85)
    a = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2LAB).astype(np.float32)
    tm, tsd = m + (rm - m) * w, sd + (rsd - sd) * w
    a = (a - m) / np.maximum(sd, 1e-3) * tsd + tm
    return Image.fromarray(cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB))
# filtro común: curva suave en S, sombras ligeramente frías, altas luces cálidas, viñeta suave
_x = np.arange(256) / 255.0
_S = np.clip(_x + .08 * np.sin(2 * np.pi * (_x - .5)) * (_x * (1 - _x)) * 4, 0, 1)
LUT_R = (np.clip(_S * 1.03 + .01, 0, 1) * 255).astype(np.uint8)
LUT_G = (np.clip(_S * 1.0 + .004, 0, 1) * 255).astype(np.uint8)
LUT_B = (np.clip(_S * .95 + .035 * (1 - _x), 0, 1) * 255).astype(np.uint8)
_yy, _xx = np.mgrid[0:H, 0:W]; VIG = (1 - .22 * (((_xx - W / 2) / (W * .75)) ** 2 + ((_yy - H / 2) / (H * .75)) ** 2)).clip(.7, 1)[..., None].astype(np.float32)
def look(im):
    a = np.asarray(im); a = np.dstack([LUT_R[a[..., 0]], LUT_G[a[..., 1]], LUT_B[a[..., 2]]]).astype(np.float32) * VIG
    hsv = cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32); hsv[..., 1] *= 1.06
    return Image.fromarray(cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB))
def get(name, k): return look(match(_get(name, k), name))
def _get(name, k):
    fr = dict(SEG)[name]
    if name == 'C': return vcrop(fr[k], float(cx[min(k, len(cx) - 1)]))
    return Image.frombytes('RGB', (W, H), fr[k])
ORDER = [n for n, _ in SEG]; XF = 10                                      # fundido cruzado de 10 cuadros
for n in range(TOTAL):
    t = n / FPS
    if ONLY and not any(abs(t - o) < .5 / FPS for o in ONLY): continue
    i = max(j for j, nm in enumerate(ORDER) if START[nm] * FPS <= n + 1e-6); name = ORDER[i]
    k = n - int(round(START[name] * FPS)); fr = dict(SEG)[name]
    im = get(name, k)
    if name == 'E':
        p = k / max(len(fr) - 1, 1); z = 1 + .05 * p
        im = im.resize((W, H), Image.LANCZOS, box=((W - W / z) / 2, (H - H / z) / 2, (W + W / z) / 2, (H + H / z) / 2))
    if name == 'A':
        p = k / max(len(fr) - 1, 1); z = 1.08 - .08 * p
        im = im.resize((W, H), Image.LANCZOS, box=((W - W / z) / 2, (H - H / z) / 2, (W + W / z) / 2, (H + H / z) / 2))
    # transición al siguiente plano
    if i + 1 < len(ORDER) and len(fr) - k <= XF:
        nxt = ORDER[i + 1]; a = (XF - (len(fr) - k) + 1) / (XF + 1)
        if name == 'F':                                                    # la guara vuela a cámara: zoom con desenfoque
            im = zoom_blur(im, (540, 900), 1 + a ** 2 * 1.3, a * .08)
        if (name, nxt) in {('B', 'F'), ('F', 'C'), ('C', 'P')}: im = Image.blend(im, get(nxt, 0), ease(a))
        else: im = Image.blend(im, get(nxt, 0), a)
    if name == 'C' and k < 6: im = zoom_blur(im, (540, 960), 1 + (1 - k / 6) ** 2 * .5, (1 - k / 6) * .06)
    fo = ease((t - (TOTAL / FPS - .8)) / .8)
    if fo > 0: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), fo)
    fi = 1 - ease(t / .6)
    if fi > 0: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), fi)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    title(lay, t); endcard(lay, t)
    if t < START['E'] + 4.3: caption(lay, t)
    im = im.convert('RGBA'); im.alpha_composite(lay); im = im.convert('RGB')
    if ONLY: im.save(f'v4_{t:.2f}.png')
    else: enc.stdin.write(im.tobytes())
if enc: enc.stdin.close(); enc.wait()
print('dur', TOTAL / FPS, START)
