#!/usr/bin/env python3
"""C-01 · "El secreto naranja" (reel vertical 1080x1920 @24 fps).
Entrada animada de José + tomas reales + narración de la chica (familia) + voz de José latam.
Ejecutar dentro de la carpeta de trabajo c01. Uso: edit_c01.py FONTS_DIR [segundos de vista previa...]
"""
import subprocess, json, math, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 24
FD = sys.argv[1].rstrip('/') + '/'; ONLY = [float(x) for x in sys.argv[2:]]
UP = '/root/.claude/uploads/dd5b2fc2-184e-5514-b789-f8432119b327/'
DRONE = UP + '1d32b6e3-1103_1.mp4'

def run(cmd, size):
    b = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    return [b[i * size:(i + 1) * size] for i in range(len(b) // size)]
def clip(path, ss, dur, speed=1.0, pre=''):
    """Toma vertical a 24 fps; 'speed' < 1 = cámara lenta (con interpolación de cuadros)."""
    vf = (pre + ',' if pre else '') + f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}'
    if speed != 1.0: vf += f',setpts=PTS/{speed},minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1'
    else: vf += ',fps=24'
    fr = run(['ffmpeg', '-loglevel', 'error', '-ss', str(ss), '-t', str(dur / speed + .2), '-i', path, '-vf', vf,
              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], W * H * 3)
    return fr[:int(round(dur * FPS))]
def drone(n0, n1, speed=1.0, cx=720):
    """Toma del dron 1440x1080 → recorte vertical, seguimiento horizontal 'cx'."""
    x0 = int(min(max(cx - 303, 0), 1440 - 607))
    pre = f"select=between(n\\,{n0}\\,{n1}),setpts=N/{30 * speed}/TB,crop=607:1080:{x0}:0"
    fr = run(['ffmpeg', '-loglevel', 'error', '-i', DRONE, '-vf', pre + f',scale={W}:{H}:flags=lanczos,fps=24,unsharp=5:5:0.5',
              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], W * H * 3)
    return fr

# ---------------- línea de tiempo (segundos) ----------------
CH0 = 20.4                                   # inicio del audio de la chica
SEGS = [  # nombre, frames, real (para igualar color)
    ('intro', run(['ffmpeg', '-loglevel', 'error', '-i', 'intro_sync.mov', '-vf', 'fps=24', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], W * H * 3)[:185], False),
    ('d_low', drone(0, 78, 1.0, 640), True),                                      # vuelo rasante entre hileras
    ('d_group', drone(87, 206, .8, 700), True),                                    # el grupo saluda (0.8x)
    ('flor', clip(UP + 'cdde6f33-10.MOV', 0.0, 5.6), True),                        # flores de cerca
    ('c1', clip(UP + '191bd54c-IMG_1553.MOV', 0.4, 5.5), True),                    # la chica camina con los brazos abiertos
    ('c2', clip('../v4/v_petals.mp4', 0.2, 4.5, 1.0, 'crop=888:1580:96:170'), False),   # pétalos y sol
    ('c3', clip('../v4/v_macro.mp4', 0.3, 5.1), False),                            # rocío
    ('c4', clip(UP + '95d60c70-11.MOV', 0.0, 3.2), True),                          # bandera → campo
    ('c5', clip(UP + '4d76ee01-IMG_1523.MOV', 0.0, 3.5, .86), True),               # el señor de la familia
    ('c6', clip(UP + '85e3191c-IMG_1569.MOV', 0.3, 2.0), True),                    # el perrito
    ('c7', clip(UP + 'c064026d-IMG_1496.MOV', 3.95, 3.6, .5, 'crop=iw*0.68:ih*0.68:iw*0.32:ih*0.16'), True),   # sin el equipo de grabación               # girasoles
    ('c8', clip(UP + '191bd54c-IMG_1553.MOV', 7.5, 4.7), True),                    # hacia la bandera
    ('valle', clip('../v4/v_valley.mp4', 0.0, 7.6), False),                        # valle soleado + cierre
]
START = {}; acc = 0
for nm, fr, _ in SEGS: START[nm] = acc / FPS; acc += len(fr)
TOTAL = acc
print({k: round(v, 2) for k, v in START.items()}, 'total', round(TOTAL / FPS, 2))

# ---------------- voces (para subtítulos) ----------------
def words(f, t0, upto=None):
    ws = [w for w in json.load(open(f))['words'] if w['type'] == 'word']
    if upto is not None: ws = [w for w in ws if w['end'] <= upto]
    return [(w['text'], t0 + w['start'], t0 + w['end']) for w in ws]
VOICE = {'intro': json.load(open('intro_sync.mov.json'))['off'], 'v2b': START['d_low'] + .2, 'v3a': START['flor'] + .1,
         'chica': CH0, 'v4b': START['valle'] + .9}
CAPS = []
def chunk(ws, n):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= n or w[0][-1:] in '.,?!': out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CAPS += chunk(words('v1b.json', VOICE['intro']), 7)
CAPS += chunk(words('v2b.json', VOICE['v2b']), 5)
CAPS += chunk(words('v3a.json', VOICE['v3a'], 5.5), 5)
CAPS += chunk(words('chica.json', VOICE['chica']), 5)
CAPS += chunk(words('v4b.json', VOICE['v4b'], 2.6), 6)            # "Copán, mostrémosle…"; el resto lo dice el logo
json.dump({'start': START, 'total': TOTAL / FPS, 'voice': VOICE}, open('timeline_c01.json', 'w'))

# ---------------- color: tomas reales igualadas entre sí + mismo filtro ----------------
def lab_stats(ims):
    L = np.concatenate([cv2.cvtColor(np.asarray(i), cv2.COLOR_RGB2LAB).reshape(-1, 3)[::9].astype(np.float32) for i in ims]); return L.mean(0), L.std(0)
def sample(fr): return [Image.frombytes('RGB', (W, H), fr[i]) for i in np.linspace(0, len(fr) - 1, 4).astype(int)]
REF = lab_stats(sum([sample(fr) for nm, fr, real in SEGS if nm in ('d_group', 'c1', 'c8')], []))
STATS = {nm: lab_stats(sample(fr)) for nm, fr, real in SEGS}
def match(im, nm, w=.75):
    (m, sd), (rm, rsd) = STATS[nm], REF
    a = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2LAB).astype(np.float32)
    ratio = np.clip((sd + (rsd - sd) * w) / np.maximum(sd, 1e-3), .88, 1.12); a = (a - m) * ratio + m + (rm - m) * w
    return Image.fromarray(cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB))
_x = np.arange(256) / 255.0; _S = np.clip(_x + .07 * np.sin(2 * np.pi * (_x - .5)) * (_x * (1 - _x)) * 4, 0, 1)
LR, LG, LB = [(np.clip(_S * k + b, 0, 1) * 255).astype(np.uint8) for k, b in ((1.03, .01), (1.0, .004), (.95, 0))]
LB = (np.clip(_S * .95 + .03 * (1 - _x), 0, 1) * 255).astype(np.uint8)
_yy, _xx = np.mgrid[0:H, 0:W]; VIG = (1 - .2 * (((_xx - W / 2) / (W * .75)) ** 2 + ((_yy - H / 2) / (H * .75)) ** 2)).clip(.72, 1)[..., None].astype(np.float32)
def look(im, strength=1.0):
    a = np.asarray(im); g = np.dstack([LR[a[..., 0]], LG[a[..., 1]], LB[a[..., 2]]]).astype(np.float32) * VIG
    g = a * (1 - strength) + g * strength
    hsv = cv2.cvtColor(np.clip(g, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32); hsv[..., 1] *= 1.05
    return Image.fromarray(cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB))
def frame(nm, k):
    fr = dict((a, b) for a, b, _ in SEGS)[nm]; real = dict((a, c) for a, _, c in SEGS)[nm]
    im = Image.frombytes('RGB', (W, H), fr[min(k, len(fr) - 1)])
    if nm == 'intro': return look(im, .35)                     # el personaje animado conserva su look
    if real or nm in ('valle',): im = match(im, nm, .75 if real else .5)
    else: im = match(im, nm, .45)
    return look(im)

# ---------------- gráficos ----------------
def font(f, s, w=None):
    ft = ImageFont.truetype(FD + f, s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
F_CAP, F_CAPB = font('Montserrat[wght].ttf', 52, 600), font('Montserrat[wght].ttf', 52, 800)
F_T, F_K = font('Montserrat[wght].ttf', 100, 850), font('Montserrat[wght].ttf', 34, 700)
BRAND = [(59, 165, 92), (46, 107, 216), (124, 77, 205), (224, 79, 143), (243, 154, 43), (242, 194, 48)]
def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def mask(txt, ft, track=0):
    ws = [ft.getlength(c) for c in txt]; tw = int(sum(ws) + track * (len(txt) - 1)) + 40
    asc, desc = ft.getmetrics(); m = Image.new('L', (tw, asc + desc + 40)); d = ImageDraw.Draw(m); x = 20; pos = []
    for c, w_ in zip(txt, ws): d.text((x, 20), c, font=ft, fill=255); pos.append((x, w_)); x += w_ + track
    return m, pos
def put(lay, m, cxy, alpha, color=(255, 255, 255), shadow=.6, blur=0):
    if alpha <= 0: return
    if blur > .3: m = m.filter(ImageFilter.GaussianBlur(blur))
    x, y = int(cxy[0] - m.width / 2), int(cxy[1] - m.height / 2)
    sh = Image.new('RGBA', m.size, (0, 0, 0, 255)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * shadow * alpha)))
    lay.alpha_composite(sh, (x + 3, y + 6))
    fl = Image.new('RGBA', m.size, color + (255,)); fl.putalpha(m.point(lambda v: int(v * alpha))); lay.alpha_composite(fl, (x, y))
KEY = {'secreto', 'mágico', 'honduras', 'copán', 'ruinas', 'naranja', 'corazón', 'náhuatl', 'cempasúchil', 'pétalos', 'sol',
       'almas', 'altar', 'familiar', 'resiliencia', 'esperanza', 'luz', 'mundo', 'belleza'}
MCACHE = {}
def captions(lay, t):
    for bi, blk in enumerate(CAPS):
        a, b = blk[0][1] - .08, blk[-1][2] + .35
        if bi + 1 < len(CAPS): b = min(b, CAPS[bi + 1][0][1] - .12)     # sin encimarse con el siguiente bloque
        if not (a <= t < b): continue
        fade = 1 - ease((t - (b - .2)) / .2)
        items = []
        for txt, s, e in blk:
            key = txt.lower().strip('¡!¿?,.…') in KEY
            if (txt, key) not in MCACHE: MCACHE[(txt, key)] = mask(txt, F_CAPB if key else F_CAP)[0]
            items.append((MCACHE[(txt, key)], s, key))
        gap = -24; tw = sum(m.width for m, _, _ in items) + gap * (len(items) - 1)
        if tw > 980:                                            # dos líneas
            half = len(items) // 2; lines = [items[:half], items[half:]]
        else: lines = [items]
        for li, line in enumerate(lines):
            tw = sum(m.width for m, _, _ in line) + gap * (len(line) - 1); x = W / 2 - tw / 2; y = 1290 + li * 70
            for m, s, key in line:
                p = ease((t - (s - .05)) / .16)
                put(lay, m, (x + m.width / 2, y + (1 - p) * 12), p * fade, (255, 214, 64) if key else (255, 255, 255), .75)
                x += m.width + gap
TITLE, TPOS = mask('COPÁN RUINAS', F_T, 4); SUBT, _ = mask('HONDURAS', F_K, 14)
_v2 = {w[0].lower().strip('¡!,.'): w[1] for w in words('v2b.json', VOICE['v2b'])}
T_COPAN = _v2.get('copán', START['d_low'] + 1.5)
def title(lay, t):
    out = 1 - ease((t - (START['d_group'] + 1.2)) / .4)
    if t < T_COPAN - .3 or out <= 0: return
    ty = 300
    put(lay, SUBT, (W / 2, ty - 100), ease((t - T_COPAN + .2) / .5) * out)
    for k, (px, pw) in enumerate(TPOS):
        p = ease((t - (T_COPAN + k * .05)) / .3)
        if p > 0: put(lay, TITLE.crop((int(px) - 6, 0, int(px + pw) + 6, TITLE.height)), (W / 2 - TITLE.width / 2 + px + pw / 2, ty + (1 - p) * 40), p * out, blur=(1 - p) * 6)
    u = ease((t - (T_COPAN + .7)) / .6)
    if u > 0:
        uw = int(TITLE.width * .78 * u); seg = Image.new('RGBA', (max(1, uw), 10)); sd = ImageDraw.Draw(seg)
        for k in range(6): sd.rectangle((k * uw / 6, 0, (k + 1) * uw / 6, 10), fill=BRAND[k] + (int(255 * out),))
        lay.alpha_composite(seg, (int(W / 2 - TITLE.width * .39), ty + 72))
LOGO = Image.open('../v5/logo_hs_fix.png').convert('RGBA'); LOGO = LOGO.resize((900, int(LOGO.height * 900 / LOGO.width)), Image.LANCZOS)
_v4 = {w[0].lower().strip('¡!,.'): w[1] for w in words('v4b.json', VOICE['v4b'])}
T_LOGO = _v4.get('honduras', START['valle'] + 3.5)
def endcard(lay, t):
    if t < T_LOGO - .2: return
    p = ease((t - T_LOGO) / .7); sc = .86 + .14 * p
    g = Image.new('L', (W, H)); gd = ImageDraw.Draw(g)
    for yy in range(0, H, 2): gd.line((0, yy, W, yy + 1), fill=int(120 * ease((t - T_LOGO + .2) / .6) * math.exp(-((yy - 860) / 430) ** 2)))
    veil = Image.new('RGBA', (W, H), (10, 8, 6, 255)); veil.putalpha(g); lay.alpha_composite(veil)
    lg = LOGO.resize((int(LOGO.width * sc), int(LOGO.height * sc)), Image.LANCZOS)
    sh = Image.new('RGBA', lg.size, (0, 0, 0, 255)); sh.putalpha(lg.getchannel('A').filter(ImageFilter.GaussianBlur(14)).point(lambda q: int(q * .5 * p)))
    x, y = int(W / 2 - lg.width / 2), int(860 - lg.height / 2 + (1 - p) * 40); lay.alpha_composite(sh, (x + 4, y + 10))
    s_ = (t - (T_LOGO + .9)) / 1.1
    if 0 < s_ < 1:
        arr = np.array(lg).astype(np.float32); w_ = arr.shape[1]; xs = np.arange(w_)[None, :] + np.arange(arr.shape[0])[:, None] * .4
        band = np.clip(1 - np.abs(xs - (-200 + s_ * (w_ + 400))) / 70, 0, 1)[..., None] * .55
        arr[..., :3] = arr[..., :3] * (1 - band) + 255 * band; lg = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    lg.putalpha(lg.getchannel('A').point(lambda q: int(q * p))); lay.alpha_composite(lg, (x, y))

# ---------------- render ----------------
ORDER = [nm for nm, _, _ in SEGS]; XF = 8
enc = None if ONLY else subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', 'video_c01.mp4'], stdin=subprocess.PIPE)
for n in range(TOTAL):
    t = n / FPS
    if ONLY and not any(abs(t - o) < .5 / FPS for o in ONLY): continue
    i = max(j for j, nm in enumerate(ORDER) if START[nm] * FPS <= n + 1e-6); nm = ORDER[i]
    k = n - int(round(START[nm] * FPS)); L = len(SEGS[i][1])
    im = frame(nm, k)
    if nm == 'valle':                                            # empuje lento + desenfoque bajo el logo
        z = 1 + .05 * k / max(L - 1, 1); im = im.resize((W, H), Image.LANCZOS, box=((W - W / z) / 2, (H - H / z) / 2, (W + W / z) / 2, (H + H / z) / 2))
        bv = ease((t - (T_LOGO - .2)) / .8)
        if bv > 0: im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(14)), bv)
    if nm == 'flor' or nm == 'c3':                               # respiración lenta en los detalles
        z = 1.0 + .04 * k / max(L - 1, 1); im = im.resize((W, H), Image.LANCZOS, box=((W - W / z) / 2, (H - H / z) / 2, (W + W / z) / 2, (H + H / z) / 2))
    if i + 1 < len(ORDER) and L - k <= XF:                       # fundido cruzado al siguiente plano
        a = (XF - (L - k) + 1) / (XF + 1); im = Image.blend(im, frame(ORDER[i + 1], 0), ease(a))
    fo = ease((t - (TOTAL / FPS - .8)) / .8)
    if fo > 0: im = Image.blend(im, Image.new('RGB', (W, H)), fo)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    title(lay, t); endcard(lay, t)
    if t < T_LOGO - .1: captions(lay, t)
    im = im.convert('RGBA'); im.alpha_composite(lay); im = im.convert('RGB')
    if ONLY: im.save(f'c01_{t:.2f}.png')
    else: enc.stdin.write(im.tobytes())
if enc: enc.stdin.close(); enc.wait()
print('ok', TOTAL / FPS)
