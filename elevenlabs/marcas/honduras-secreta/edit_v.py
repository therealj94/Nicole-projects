# Honduras Secreta · Copán Ruinas (parte 1): secuencia vertical 1080x1920 @24fps
import subprocess, json, math, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 24
DRONE = '/root/.claude/uploads/dd5b2fc2-184e-5514-b789-f8432119b327/1d32b6e3-1103_1.mp4'
FD = '../../lbs/fonts/'
ONLY = [float(x) for x in sys.argv[1:]]
def frames(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); fs = []
    while True:
        b = p.stdout.read(W * H * 3) if 'fly' in cmd[-1] or True else None
        if b is None or len(b) < W * H * 3: break
        fs.append(b)
    return fs
GRADE = ("eq=contrast=1.07:brightness=0.015:saturation=1.14:gamma=1.03,"
         "colorbalance=rs=0.02:bs=-0.02:rm=0.015:bm=-0.015,unsharp=5:5:0.55,noise=alls=3:allf=t")
def raw(path, vf, ss=None, t=None):
    cmd = ['ffmpeg', '-loglevel', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + \
          ['-i', path, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    n = len(p) // (W * H * 3); return [p[i * W * H * 3:(i + 1) * W * H * 3] for i in range(n)]
# --- A: vuelo (Veo + logo restaurado), 0 - 6.6 s
A = raw('fly_logo.mp4', 'fps=24,scale=1080:1920,eq=contrast=1.03:saturation=1.04', 0, 6.625)
# --- B: saludo, original 2.0-6.8 s; todos los cuadros (30 fps) reproducidos a 24 = cámara lenta 0.8x
P = json.load(open('people.json')); Y = {int(k): v for k, v in P['yellow'].items()}; L = {int(k): v for k, v in P['lady'].items()}
cx = []
for i in range(60, 204):
    a = Y.get(i, [None])[0]; b = L.get(i, [None])[0]
    cx.append(((a + b) / 2 - 15) if a and b else np.nan)
cx = np.array(cx); ok = ~np.isnan(cx); cx = np.interp(np.arange(len(cx)), np.arange(len(cx))[ok], cx[ok])
cx = np.convolve(np.pad(cx, 12, mode='edge'), np.ones(25) / 25, mode='valid')
srcB = None and raw(DRONE, 'select=between(n\\,60\\,203),setpts=N/24/TB,' + GRADE.replace(',unsharp=5:5:0.55,noise=alls=3:allf=t', ''), None, None)
def bytes_to_img(b, w=W, h=H): return Image.frombytes('RGB', (w, h), b)
# B y C se recortan del cuadro 1440x1080 -> 607x1080 -> 1080x1920
def raw_full(sel):
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', DRONE, '-fps_mode', 'passthrough', '-vf', sel + ',' + GRADE.replace(',unsharp=5:5:0.55,noise=alls=3:allf=t', ''), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    fs = 1440 * 1080 * 3; return [p[i * fs:(i + 1) * fs] for i in range(len(p) // fs)]
B = raw_full('select=between(n\\,60\\,203),setpts=N/24/TB')
C = raw_full('select=between(n\\,366\\,510),setpts=N/30/TB,fps=24')
def vcrop(b, center, zoom=1.0):
    im = Image.frombytes('RGB', (1440, 1080), b)
    cw, ch = 607.5 / zoom, 1080 / zoom; x0 = min(max(center - cw / 2, 0), 1440 - cw); y0 = (1080 - ch) / 2
    out = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    out = out.filter(ImageFilter.UnsharpMask(1.6, 70, 2))
    a = np.array(out).astype(np.int16); a += np.random.normal(0, 2.6, a.shape).astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
# --- títulos
def font(f, s, w=None):
    ft = ImageFont.truetype(FD + f, s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
F_T, F_S, F_K = font('Montserrat[wght].ttf', 100, 850), font('Montserrat[wght].ttf', 50, 600), font('Montserrat[wght].ttf', 34, 700)
BRAND = [(59, 165, 92), (46, 107, 216), (124, 77, 205), (224, 79, 143), (243, 154, 43), (242, 194, 48)]
def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def text_layer(txt, ft, track=0):
    widths = [ft.getlength(c) for c in txt]; tw = int(sum(widths) + track * (len(txt) - 1)) + 40
    asc, desc = ft.getmetrics(); img = Image.new('L', (tw, asc + desc + 40)); d = ImageDraw.Draw(img); x = 20
    pos = []
    for c, w_ in zip(txt, widths): d.text((x, 20), c, font=ft, fill=255); pos.append((x, w_)); x += w_ + track
    return img, pos
TITLE, TPOS = text_layer('COPÁN RUINAS', F_T, 4)
SUB, _ = text_layer('mostrémosle tu belleza al mundo', F_S, 1)
KICK, _ = text_layer('H O N D U R A S', F_K, 2)
VO = 0.8; W_COPAN, W_RUINAS, W_MOSTR = VO + .12, VO + .46, VO + 1.30
def draw_titles(cv, t):
    out = 1 - ease((t - 5.6) / .45)
    if t < .5 or out <= 0: return cv
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def put(mask, cxy, alpha, color=(255, 255, 255), clip=None, shadow=True):
        m = mask if clip is None else mask.crop((0, 0, max(1, int(mask.width * clip)), mask.height))
        x, y = int(cxy[0] - mask.width / 2), int(cxy[1] - mask.height / 2)
        if shadow:
            sh = Image.new('RGBA', m.size, (0, 0, 0, 255)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * .55 * alpha)))
            lay.alpha_composite(sh, (x + 3, y + 6))
        fl = Image.new('RGBA', m.size, color + (255,)); fl.putalpha(m.point(lambda v: int(v * alpha))); lay.alpha_composite(fl, (x, y))
    ty = 330
    put(KICK, (W / 2, ty - 110), ease((t - .55) / .5) * out)
    # COPÁN RUINAS: cada letra entra con subida + desenfoque al ritmo de la voz
    for k, (px, pw) in enumerate(TPOS):
        st = W_COPAN + k * ((W_RUINAS + .35 - W_COPAN) / len(TPOS))
        p = ease((t - st) / .32)
        if p <= 0: continue
        ch = TITLE.crop((int(px) - 6, 0, int(px + pw) + 6, TITLE.height))
        if p < 1: ch = ch.filter(ImageFilter.GaussianBlur((1 - p) * 6))
        x = W / 2 - TITLE.width / 2 + px + pw / 2; y = ty + (1 - p) * 40
        put(ch, (x, y), p * out)
    # subrayado en colores de la marca
    u = ease((t - (W_RUINAS + .3)) / .6)
    if u > 0:
        uw = int(TITLE.width * .78 * u); seg = Image.new('RGBA', (max(1, uw), 10))
        sd = ImageDraw.Draw(seg)
        for k in range(len(BRAND)): sd.rectangle((k * uw / len(BRAND), 0, (k + 1) * uw / len(BRAND), 10), fill=BRAND[k] + (int(255 * out),))
        lay.alpha_composite(seg, (int(W / 2 - TITLE.width * .39), ty + 72))
    s = ease((t - W_MOSTR) / .5)
    if s > 0: put(SUB, (W / 2, ty + 160 + (1 - s) * 20), s * out)
    cv = cv.convert('RGBA'); cv.alpha_composite(lay); return cv.convert('RGB')
def zoom_blur(im, center, z, blur):
    w, h = im.size; acc = np.zeros((h, w, 3), np.float32); n = 6 if blur > 0 else 1
    for k in range(n):
        zz = z * (1 + blur * k / max(n - 1, 1)); cw, ch = w / zz, h / zz
        x0 = min(max(center[0] - cw / 2, 0), w - cw); y0 = min(max(center[1] - ch / 2, 0), h - ch)
        acc += np.array(im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32)
    return Image.fromarray((acc / n).astype(np.uint8))
# --- línea de tiempo
NA, NB, NC = len(A), len(B), len(C)
TOTAL = NA + NB + NC
enc = None if ONLY else subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', 'video_v.mp4'], stdin=subprocess.PIPE)
for n in range(TOTAL):
    t = n / FPS
    if ONLY and not any(abs(t - o) < .5 / FPS for o in ONLY): continue
    if n < NA:
        im = bytes_to_img(A[n]); tl = (NA - 1 - n) / FPS
        if tl < .3: im = zoom_blur(im, (540, 980), 1 + (1 - tl / .3) ** 2 * 1.4, (1 - tl / .3) * .09)
        im = draw_titles(im, t)
    elif n < NA + NB:
        k = n - NA; im = vcrop(B[k], float(cx[min(k, len(cx) - 1)]), 1.0)
        if k < 8: im = zoom_blur(im, (540, 960), 1 + (1 - k / 8) ** 2 * .7, (1 - k / 8) * .08)
    else:
        k = n - NA - NB; p = k / max(NC - 1, 1)
        im = vcrop(C[k], 900 - 50 * p, 1.0 + .07 * (p ** 1.2))
    if ONLY: im.save(f'v_{t:.2f}.png')
    else: enc.stdin.write(im.tobytes())
if enc: enc.stdin.close(); enc.wait()
print('frames', NA, NB, NC, 'dur', TOTAL / FPS)
